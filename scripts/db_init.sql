CREATE SCHEMA IF NOT EXISTS "__WIKI_SCHEMA__";
CREATE EXTENSION IF NOT EXISTS pg_trgm;

CREATE TABLE IF NOT EXISTS "__WIKI_SCHEMA__".pages (
    id TEXT PRIMARY KEY,
    slug TEXT NOT NULL,
    title TEXT NOT NULL,
    topic TEXT NOT NULL,
    section TEXT NOT NULL,
    path TEXT NOT NULL UNIQUE,
    created TEXT NOT NULL,
    updated TEXT NOT NULL,
    confidence TEXT NOT NULL,
    visibility TEXT NOT NULL DEFAULT 'public',
    excerpt TEXT NOT NULL DEFAULT '',
    body TEXT NOT NULL DEFAULT '',
    word_count INTEGER NOT NULL DEFAULT 0,
    headings_json TEXT NOT NULL DEFAULT '[]',
    search_vector TEXT NOT NULL DEFAULT '',
    content_hash TEXT NOT NULL,
    synced_at TEXT NOT NULL
);

ALTER TABLE "__WIKI_SCHEMA__".pages ADD COLUMN IF NOT EXISTS search_vector TEXT NOT NULL DEFAULT '';
ALTER TABLE "__WIKI_SCHEMA__".pages ADD COLUMN IF NOT EXISTS headings_json TEXT NOT NULL DEFAULT '[]';
ALTER TABLE "__WIKI_SCHEMA__".pages ADD COLUMN IF NOT EXISTS visibility TEXT NOT NULL DEFAULT 'public';
ALTER TABLE "__WIKI_SCHEMA__".pages ADD COLUMN IF NOT EXISTS excerpt TEXT NOT NULL DEFAULT '';
ALTER TABLE "__WIKI_SCHEMA__".pages ADD COLUMN IF NOT EXISTS body TEXT NOT NULL DEFAULT '';
ALTER TABLE "__WIKI_SCHEMA__".pages ADD COLUMN IF NOT EXISTS word_count INTEGER NOT NULL DEFAULT 0;
ALTER TABLE "__WIKI_SCHEMA__".pages ADD COLUMN IF NOT EXISTS content_hash TEXT NOT NULL DEFAULT '';
ALTER TABLE "__WIKI_SCHEMA__".pages ADD COLUMN IF NOT EXISTS synced_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP::text;

CREATE INDEX IF NOT EXISTS idx_pages_section ON "__WIKI_SCHEMA__".pages (section);
CREATE INDEX IF NOT EXISTS idx_pages_topic ON "__WIKI_SCHEMA__".pages (topic);
CREATE INDEX IF NOT EXISTS idx_pages_slug ON "__WIKI_SCHEMA__".pages (slug);
CREATE INDEX IF NOT EXISTS idx_pages_visibility ON "__WIKI_SCHEMA__".pages (visibility);
CREATE INDEX IF NOT EXISTS idx_pages_search_vector ON "__WIKI_SCHEMA__".pages USING GIN (search_vector gin_trgm_ops);
CREATE INDEX IF NOT EXISTS idx_pages_title_trgm ON "__WIKI_SCHEMA__".pages USING GIN (title gin_trgm_ops);
CREATE INDEX IF NOT EXISTS idx_pages_excerpt_trgm ON "__WIKI_SCHEMA__".pages USING GIN (excerpt gin_trgm_ops);
CREATE INDEX IF NOT EXISTS idx_pages_body_trgm ON "__WIKI_SCHEMA__".pages USING GIN (body gin_trgm_ops);

CREATE TABLE IF NOT EXISTS "__WIKI_SCHEMA__".page_tags (
    page_id TEXT NOT NULL REFERENCES "__WIKI_SCHEMA__".pages (id) ON DELETE CASCADE,
    tag TEXT NOT NULL,
    position INTEGER NOT NULL,
    PRIMARY KEY (page_id, tag)
);

CREATE INDEX IF NOT EXISTS idx_page_tags_tag ON "__WIKI_SCHEMA__".page_tags (tag);

CREATE TABLE IF NOT EXISTS "__WIKI_SCHEMA__".page_sources (
    page_id TEXT NOT NULL REFERENCES "__WIKI_SCHEMA__".pages (id) ON DELETE CASCADE,
    source TEXT NOT NULL,
    position INTEGER NOT NULL,
    PRIMARY KEY (page_id, position)
);

CREATE TABLE IF NOT EXISTS "__WIKI_SCHEMA__".page_links (
    source_page_id TEXT NOT NULL REFERENCES "__WIKI_SCHEMA__".pages (id) ON DELETE CASCADE,
    target_slug TEXT NOT NULL,
    target_page_id TEXT REFERENCES "__WIKI_SCHEMA__".pages (id) ON DELETE SET NULL,
    position INTEGER NOT NULL,
    PRIMARY KEY (source_page_id, position)
);

CREATE INDEX IF NOT EXISTS idx_page_links_target_page_id ON "__WIKI_SCHEMA__".page_links (target_page_id);
CREATE INDEX IF NOT EXISTS idx_page_links_target_slug ON "__WIKI_SCHEMA__".page_links (target_slug);

CREATE TABLE IF NOT EXISTS "__WIKI_SCHEMA__".page_acl (
    id BIGSERIAL PRIMARY KEY,
    page_id TEXT NOT NULL REFERENCES "__WIKI_SCHEMA__".pages (id) ON DELETE CASCADE,
    subject_type TEXT NOT NULL,
    subject_value TEXT NOT NULL,
    permission TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP::TEXT
);

CREATE INDEX IF NOT EXISTS idx_page_acl_page_id ON "__WIKI_SCHEMA__".page_acl (page_id);
CREATE INDEX IF NOT EXISTS idx_page_acl_subject ON "__WIKI_SCHEMA__".page_acl (subject_type, subject_value);
CREATE UNIQUE INDEX IF NOT EXISTS uq_page_acl_rule ON "__WIKI_SCHEMA__".page_acl (page_id, subject_type, subject_value, permission);

CREATE TABLE IF NOT EXISTS "__WIKI_SCHEMA__".session_tokens (
    id BIGSERIAL PRIMARY KEY,
    session_id TEXT NOT NULL UNIQUE,
    role TEXT NOT NULL,
    token_hash TEXT NOT NULL,
    expires_at TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP::TEXT,
    last_seen_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP::TEXT,
    revoked_at TEXT
);

CREATE INDEX IF NOT EXISTS idx_session_tokens_role ON "__WIKI_SCHEMA__".session_tokens (role);
CREATE INDEX IF NOT EXISTS idx_session_tokens_expires_at ON "__WIKI_SCHEMA__".session_tokens (expires_at);

CREATE TABLE IF NOT EXISTS "__WIKI_SCHEMA__".auth_accounts (
    id BIGSERIAL PRIMARY KEY,
    role TEXT NOT NULL UNIQUE,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    display_name TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP::TEXT,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP::TEXT,
    active INTEGER NOT NULL DEFAULT 1
);

CREATE INDEX IF NOT EXISTS idx_auth_accounts_role ON "__WIKI_SCHEMA__".auth_accounts (role);
CREATE INDEX IF NOT EXISTS idx_auth_accounts_username ON "__WIKI_SCHEMA__".auth_accounts (username);

CREATE TABLE IF NOT EXISTS "__WIKI_SCHEMA__".upload_artifacts (
    id BIGSERIAL PRIMARY KEY,
    uploaded_by TEXT NOT NULL,
    filename TEXT NOT NULL,
    title TEXT NOT NULL,
    topic TEXT NOT NULL,
    content_text TEXT NOT NULL,
    content_hash TEXT NOT NULL,
    duplicate_json TEXT NOT NULL DEFAULT '[]',
    status TEXT NOT NULL DEFAULT 'received',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP::TEXT
);

CREATE INDEX IF NOT EXISTS idx_upload_artifacts_created_at ON "__WIKI_SCHEMA__".upload_artifacts (created_at);
CREATE INDEX IF NOT EXISTS idx_upload_artifacts_hash ON "__WIKI_SCHEMA__".upload_artifacts (content_hash);

CREATE TABLE IF NOT EXISTS "__WIKI_SCHEMA__".wiki_drafts (
    id BIGSERIAL PRIMARY KEY,
    uploaded_artifact_id BIGINT REFERENCES "__WIKI_SCHEMA__".upload_artifacts (id) ON DELETE SET NULL,
    page_id TEXT UNIQUE,
    title TEXT NOT NULL,
    topic TEXT NOT NULL,
    section TEXT NOT NULL,
    visibility TEXT NOT NULL DEFAULT 'internal',
    content_hash TEXT NOT NULL,
    draft_json TEXT NOT NULL DEFAULT '{}',
    status TEXT NOT NULL DEFAULT 'draft',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP::TEXT,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP::TEXT
);

CREATE INDEX IF NOT EXISTS idx_wiki_drafts_status ON "__WIKI_SCHEMA__".wiki_drafts (status);

CREATE TABLE IF NOT EXISTS "__WIKI_SCHEMA__".activity_log (
    ordinal INTEGER PRIMARY KEY,
    logged_at TEXT NOT NULL,
    action TEXT NOT NULL,
    message TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_activity_logged_at ON "__WIKI_SCHEMA__".activity_log (logged_at);
CREATE INDEX IF NOT EXISTS idx_activity_action ON "__WIKI_SCHEMA__".activity_log (action);

CREATE TABLE IF NOT EXISTS "__WIKI_SCHEMA__".runtime_activity_log (
    id BIGSERIAL PRIMARY KEY,
    event_type TEXT NOT NULL,
    entity_type TEXT,
    entity_id TEXT,
    details_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP::TEXT
);

CREATE INDEX IF NOT EXISTS idx_runtime_activity_created_at ON "__WIKI_SCHEMA__".runtime_activity_log (created_at);
CREATE INDEX IF NOT EXISTS idx_runtime_activity_type ON "__WIKI_SCHEMA__".runtime_activity_log (event_type);

CREATE TABLE IF NOT EXISTS "__WIKI_SCHEMA__".query_logs (
    id BIGSERIAL PRIMARY KEY,
    question TEXT NOT NULL,
    page_ids_json TEXT NOT NULL DEFAULT '[]',
    answer_path TEXT,
    status TEXT NOT NULL DEFAULT 'saved',
    asked_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP::TEXT
);

CREATE INDEX IF NOT EXISTS idx_query_logs_asked_at ON "__WIKI_SCHEMA__".query_logs (asked_at);
CREATE INDEX IF NOT EXISTS idx_query_logs_status ON "__WIKI_SCHEMA__".query_logs (status);

CREATE TABLE IF NOT EXISTS "__WIKI_SCHEMA__".sync_state (
    sync_key TEXT PRIMARY KEY,
    last_synced_at TEXT NOT NULL,
    last_page_count INTEGER NOT NULL DEFAULT 0,
    last_content_hash TEXT NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS "__WIKI_SCHEMA__".chat_sessions (
    session_key TEXT PRIMARY KEY,
    role TEXT NOT NULL,
    subject TEXT,
    created_at TEXT NOT NULL,
    last_message_at TEXT NOT NULL,
    summary_json TEXT NOT NULL DEFAULT '{}'
);

CREATE TABLE IF NOT EXISTS "__WIKI_SCHEMA__".chat_messages (
    id BIGSERIAL PRIMARY KEY,
    session_key TEXT NOT NULL REFERENCES "__WIKI_SCHEMA__".chat_sessions (session_key) ON DELETE CASCADE,
    message_role TEXT NOT NULL,
    content TEXT NOT NULL,
    citations_json TEXT NOT NULL DEFAULT '[]',
    created_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_chat_messages_session_key ON "__WIKI_SCHEMA__".chat_messages (session_key);
CREATE INDEX IF NOT EXISTS idx_chat_messages_created_at ON "__WIKI_SCHEMA__".chat_messages (created_at);

CREATE TABLE IF NOT EXISTS "__WIKI_SCHEMA__".tutor_progress (
    subject_key TEXT NOT NULL,
    role TEXT NOT NULL,
    topic TEXT NOT NULL,
    last_question TEXT NOT NULL,
    last_answer TEXT NOT NULL,
    confidence TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    PRIMARY KEY (subject_key, topic)
);

CREATE TABLE IF NOT EXISTS "__WIKI_SCHEMA__".quiz_attempts (
    id BIGSERIAL PRIMARY KEY,
    subject_key TEXT NOT NULL,
    role TEXT NOT NULL,
    question TEXT NOT NULL,
    quiz_json TEXT NOT NULL DEFAULT '[]',
    created_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_quiz_attempts_subject_key ON "__WIKI_SCHEMA__".quiz_attempts (subject_key);
CREATE INDEX IF NOT EXISTS idx_quiz_attempts_created_at ON "__WIKI_SCHEMA__".quiz_attempts (created_at);

ALTER TABLE "__WIKI_SCHEMA__".pages ENABLE ROW LEVEL SECURITY;
ALTER TABLE "__WIKI_SCHEMA__".page_tags ENABLE ROW LEVEL SECURITY;
ALTER TABLE "__WIKI_SCHEMA__".page_sources ENABLE ROW LEVEL SECURITY;
ALTER TABLE "__WIKI_SCHEMA__".page_links ENABLE ROW LEVEL SECURITY;
ALTER TABLE "__WIKI_SCHEMA__".page_acl ENABLE ROW LEVEL SECURITY;
ALTER TABLE "__WIKI_SCHEMA__".session_tokens ENABLE ROW LEVEL SECURITY;
ALTER TABLE "__WIKI_SCHEMA__".activity_log ENABLE ROW LEVEL SECURITY;
ALTER TABLE "__WIKI_SCHEMA__".runtime_activity_log ENABLE ROW LEVEL SECURITY;
ALTER TABLE "__WIKI_SCHEMA__".query_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE "__WIKI_SCHEMA__".sync_state ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "wiki_init can manage pages" ON "__WIKI_SCHEMA__".pages;
CREATE POLICY "wiki_init can manage pages"
ON "__WIKI_SCHEMA__".pages
FOR ALL
TO postgres
USING (true)
WITH CHECK (true);

DROP POLICY IF EXISTS "wiki_backend can manage pages" ON "__WIKI_SCHEMA__".pages;
CREATE POLICY "wiki_backend can manage pages"
ON "__WIKI_SCHEMA__".pages
FOR ALL
TO wiki_backend
USING (true)
WITH CHECK (true);

DROP POLICY IF EXISTS "wiki_init can manage page_tags" ON "__WIKI_SCHEMA__".page_tags;
CREATE POLICY "wiki_init can manage page_tags"
ON "__WIKI_SCHEMA__".page_tags
FOR ALL
TO postgres
USING (true)
WITH CHECK (true);

DROP POLICY IF EXISTS "wiki_backend can manage page_tags" ON "__WIKI_SCHEMA__".page_tags;
CREATE POLICY "wiki_backend can manage page_tags"
ON "__WIKI_SCHEMA__".page_tags
FOR ALL
TO wiki_backend
USING (true)
WITH CHECK (true);

DROP POLICY IF EXISTS "wiki_init can manage page_sources" ON "__WIKI_SCHEMA__".page_sources;
CREATE POLICY "wiki_init can manage page_sources"
ON "__WIKI_SCHEMA__".page_sources
FOR ALL
TO postgres
USING (true)
WITH CHECK (true);

DROP POLICY IF EXISTS "wiki_backend can manage page_sources" ON "__WIKI_SCHEMA__".page_sources;
CREATE POLICY "wiki_backend can manage page_sources"
ON "__WIKI_SCHEMA__".page_sources
FOR ALL
TO wiki_backend
USING (true)
WITH CHECK (true);

DROP POLICY IF EXISTS "wiki_init can manage page_links" ON "__WIKI_SCHEMA__".page_links;
CREATE POLICY "wiki_init can manage page_links"
ON "__WIKI_SCHEMA__".page_links
FOR ALL
TO postgres
USING (true)
WITH CHECK (true);

DROP POLICY IF EXISTS "wiki_backend can manage page_links" ON "__WIKI_SCHEMA__".page_links;
CREATE POLICY "wiki_backend can manage page_links"
ON "__WIKI_SCHEMA__".page_links
FOR ALL
TO wiki_backend
USING (true)
WITH CHECK (true);

DROP POLICY IF EXISTS "wiki_init can manage page_acl" ON "__WIKI_SCHEMA__".page_acl;
CREATE POLICY "wiki_init can manage page_acl"
ON "__WIKI_SCHEMA__".page_acl
FOR ALL
TO postgres
USING (true)
WITH CHECK (true);

DROP POLICY IF EXISTS "wiki_backend can manage page_acl" ON "__WIKI_SCHEMA__".page_acl;
CREATE POLICY "wiki_backend can manage page_acl"
ON "__WIKI_SCHEMA__".page_acl
FOR ALL
TO wiki_backend
USING (true)
WITH CHECK (true);

DROP POLICY IF EXISTS "wiki_init can manage session_tokens" ON "__WIKI_SCHEMA__".session_tokens;
CREATE POLICY "wiki_init can manage session_tokens"
ON "__WIKI_SCHEMA__".session_tokens
FOR ALL
TO postgres
USING (true)
WITH CHECK (true);

DROP POLICY IF EXISTS "wiki_backend can manage session_tokens" ON "__WIKI_SCHEMA__".session_tokens;
CREATE POLICY "wiki_backend can manage session_tokens"
ON "__WIKI_SCHEMA__".session_tokens
FOR ALL
TO wiki_backend
USING (true)
WITH CHECK (true);

DROP POLICY IF EXISTS "wiki_init can manage activity_log" ON "__WIKI_SCHEMA__".activity_log;
CREATE POLICY "wiki_init can manage activity_log"
ON "__WIKI_SCHEMA__".activity_log
FOR ALL
TO postgres
USING (true)
WITH CHECK (true);

DROP POLICY IF EXISTS "wiki_backend can manage activity_log" ON "__WIKI_SCHEMA__".activity_log;
CREATE POLICY "wiki_backend can manage activity_log"
ON "__WIKI_SCHEMA__".activity_log
FOR ALL
TO wiki_backend
USING (true)
WITH CHECK (true);

DROP POLICY IF EXISTS "wiki_init can manage runtime_activity_log" ON "__WIKI_SCHEMA__".runtime_activity_log;
CREATE POLICY "wiki_init can manage runtime_activity_log"
ON "__WIKI_SCHEMA__".runtime_activity_log
FOR ALL
TO postgres
USING (true)
WITH CHECK (true);

DROP POLICY IF EXISTS "wiki_backend can manage runtime_activity_log" ON "__WIKI_SCHEMA__".runtime_activity_log;
CREATE POLICY "wiki_backend can manage runtime_activity_log"
ON "__WIKI_SCHEMA__".runtime_activity_log
FOR ALL
TO wiki_backend
USING (true)
WITH CHECK (true);

DROP POLICY IF EXISTS "wiki_init can manage query_logs" ON "__WIKI_SCHEMA__".query_logs;
CREATE POLICY "wiki_init can manage query_logs"
ON "__WIKI_SCHEMA__".query_logs
FOR ALL
TO postgres
USING (true)
WITH CHECK (true);

DROP POLICY IF EXISTS "wiki_backend can manage query_logs" ON "__WIKI_SCHEMA__".query_logs;
CREATE POLICY "wiki_backend can manage query_logs"
ON "__WIKI_SCHEMA__".query_logs
FOR ALL
TO wiki_backend
USING (true)
WITH CHECK (true);

DROP POLICY IF EXISTS "wiki_init can manage sync_state" ON "__WIKI_SCHEMA__".sync_state;
CREATE POLICY "wiki_init can manage sync_state"
ON "__WIKI_SCHEMA__".sync_state
FOR ALL
TO postgres
USING (true)
WITH CHECK (true);

DROP POLICY IF EXISTS "wiki_backend can manage sync_state" ON "__WIKI_SCHEMA__".sync_state;
CREATE POLICY "wiki_backend can manage sync_state"
ON "__WIKI_SCHEMA__".sync_state
FOR ALL
TO wiki_backend
USING (true)
WITH CHECK (true);

DROP POLICY IF EXISTS "wiki_init can manage chat_sessions" ON "__WIKI_SCHEMA__".chat_sessions;
CREATE POLICY "wiki_init can manage chat_sessions"
ON "__WIKI_SCHEMA__".chat_sessions
FOR ALL
TO postgres
USING (true)
WITH CHECK (true);

DROP POLICY IF EXISTS "wiki_backend can manage chat_sessions" ON "__WIKI_SCHEMA__".chat_sessions;
CREATE POLICY "wiki_backend can manage chat_sessions"
ON "__WIKI_SCHEMA__".chat_sessions
FOR ALL
TO wiki_backend
USING (true)
WITH CHECK (true);

DROP POLICY IF EXISTS "wiki_init can manage chat_messages" ON "__WIKI_SCHEMA__".chat_messages;
CREATE POLICY "wiki_init can manage chat_messages"
ON "__WIKI_SCHEMA__".chat_messages
FOR ALL
TO postgres
USING (true)
WITH CHECK (true);

DROP POLICY IF EXISTS "wiki_backend can manage chat_messages" ON "__WIKI_SCHEMA__".chat_messages;
CREATE POLICY "wiki_backend can manage chat_messages"
ON "__WIKI_SCHEMA__".chat_messages
FOR ALL
TO wiki_backend
USING (true)
WITH CHECK (true);

DROP POLICY IF EXISTS "wiki_init can manage tutor_progress" ON "__WIKI_SCHEMA__".tutor_progress;
CREATE POLICY "wiki_init can manage tutor_progress"
ON "__WIKI_SCHEMA__".tutor_progress
FOR ALL
TO postgres
USING (true)
WITH CHECK (true);

DROP POLICY IF EXISTS "wiki_backend can manage tutor_progress" ON "__WIKI_SCHEMA__".tutor_progress;
CREATE POLICY "wiki_backend can manage tutor_progress"
ON "__WIKI_SCHEMA__".tutor_progress
FOR ALL
TO wiki_backend
USING (true)
WITH CHECK (true);

DROP POLICY IF EXISTS "wiki_init can manage quiz_attempts" ON "__WIKI_SCHEMA__".quiz_attempts;
CREATE POLICY "wiki_init can manage quiz_attempts"
ON "__WIKI_SCHEMA__".quiz_attempts
FOR ALL
TO postgres
USING (true)
WITH CHECK (true);

DROP POLICY IF EXISTS "wiki_backend can manage quiz_attempts" ON "__WIKI_SCHEMA__".quiz_attempts;
CREATE POLICY "wiki_backend can manage quiz_attempts"
ON "__WIKI_SCHEMA__".quiz_attempts
FOR ALL
TO wiki_backend
USING (true)
WITH CHECK (true);
