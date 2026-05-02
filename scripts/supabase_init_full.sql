-- Supabase SQL Editor init script for AI Coding Wiki
-- Run in order as a single script, or section by section if needed.

-- 1) Core schema and content tables
CREATE SCHEMA IF NOT EXISTS "public";

CREATE TABLE IF NOT EXISTS "public".pages (
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
    content_hash TEXT NOT NULL,
    synced_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_pages_section ON "public".pages (section);
CREATE INDEX IF NOT EXISTS idx_pages_topic ON "public".pages (topic);
CREATE INDEX IF NOT EXISTS idx_pages_slug ON "public".pages (slug);
CREATE INDEX IF NOT EXISTS idx_pages_visibility ON "public".pages (visibility);

CREATE TABLE IF NOT EXISTS "public".page_tags (
    page_id TEXT NOT NULL REFERENCES "public".pages (id) ON DELETE CASCADE,
    tag TEXT NOT NULL,
    position INTEGER NOT NULL,
    PRIMARY KEY (page_id, tag)
);

CREATE INDEX IF NOT EXISTS idx_page_tags_tag ON "public".page_tags (tag);

CREATE TABLE IF NOT EXISTS "public".page_sources (
    page_id TEXT NOT NULL REFERENCES "public".pages (id) ON DELETE CASCADE,
    source TEXT NOT NULL,
    position INTEGER NOT NULL,
    PRIMARY KEY (page_id, position)
);

CREATE TABLE IF NOT EXISTS "public".page_links (
    source_page_id TEXT NOT NULL REFERENCES "public".pages (id) ON DELETE CASCADE,
    target_slug TEXT NOT NULL,
    target_page_id TEXT REFERENCES "public".pages (id) ON DELETE SET NULL,
    position INTEGER NOT NULL,
    PRIMARY KEY (source_page_id, position)
);

CREATE INDEX IF NOT EXISTS idx_page_links_target_page_id ON "public".page_links (target_page_id);
CREATE INDEX IF NOT EXISTS idx_page_links_target_slug ON "public".page_links (target_slug);

CREATE TABLE IF NOT EXISTS "public".page_acl (
    id BIGSERIAL PRIMARY KEY,
    page_id TEXT NOT NULL REFERENCES "public".pages (id) ON DELETE CASCADE,
    subject_type TEXT NOT NULL,
    subject_value TEXT NOT NULL,
    permission TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP::TEXT
);

CREATE INDEX IF NOT EXISTS idx_page_acl_page_id ON "public".page_acl (page_id);
CREATE INDEX IF NOT EXISTS idx_page_acl_subject ON "public".page_acl (subject_type, subject_value);
CREATE UNIQUE INDEX IF NOT EXISTS uq_page_acl_rule ON "public".page_acl (page_id, subject_type, subject_value, permission);

CREATE TABLE IF NOT EXISTS "public".session_tokens (
    id BIGSERIAL PRIMARY KEY,
    session_id TEXT NOT NULL UNIQUE,
    role TEXT NOT NULL,
    token_hash TEXT NOT NULL,
    expires_at TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP::TEXT,
    last_seen_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP::TEXT,
    revoked_at TEXT
);

CREATE INDEX IF NOT EXISTS idx_session_tokens_role ON "public".session_tokens (role);
CREATE INDEX IF NOT EXISTS idx_session_tokens_expires_at ON "public".session_tokens (expires_at);

CREATE TABLE IF NOT EXISTS "public".activity_log (
    ordinal INTEGER PRIMARY KEY,
    logged_at TEXT NOT NULL,
    action TEXT NOT NULL,
    message TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_activity_logged_at ON "public".activity_log (logged_at);
CREATE INDEX IF NOT EXISTS idx_activity_action ON "public".activity_log (action);

CREATE TABLE IF NOT EXISTS "public".runtime_activity_log (
    id BIGSERIAL PRIMARY KEY,
    event_type TEXT NOT NULL,
    entity_type TEXT,
    entity_id TEXT,
    details_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP::TEXT
);

CREATE INDEX IF NOT EXISTS idx_runtime_activity_created_at ON "public".runtime_activity_log (created_at);
CREATE INDEX IF NOT EXISTS idx_runtime_activity_type ON "public".runtime_activity_log (event_type);

CREATE TABLE IF NOT EXISTS "public".query_logs (
    id BIGSERIAL PRIMARY KEY,
    question TEXT NOT NULL,
    page_ids_json TEXT NOT NULL DEFAULT '[]',
    answer_path TEXT,
    status TEXT NOT NULL DEFAULT 'saved',
    asked_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP::TEXT
);

CREATE INDEX IF NOT EXISTS idx_query_logs_asked_at ON "public".query_logs (asked_at);
CREATE INDEX IF NOT EXISTS idx_query_logs_status ON "public".query_logs (status);

CREATE TABLE IF NOT EXISTS "public".sync_state (
    sync_key TEXT PRIMARY KEY,
    last_synced_at TEXT NOT NULL,
    last_page_count INTEGER NOT NULL DEFAULT 0,
    last_content_hash TEXT NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS "public".chat_sessions (
    session_key TEXT PRIMARY KEY,
    role TEXT NOT NULL,
    subject TEXT,
    created_at TEXT NOT NULL,
    last_message_at TEXT NOT NULL,
    summary_json TEXT NOT NULL DEFAULT '{}'
);

CREATE TABLE IF NOT EXISTS "public".chat_messages (
    id BIGSERIAL PRIMARY KEY,
    session_key TEXT NOT NULL REFERENCES "public".chat_sessions (session_key) ON DELETE CASCADE,
    message_role TEXT NOT NULL,
    content TEXT NOT NULL,
    citations_json TEXT NOT NULL DEFAULT '[]',
    created_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_chat_messages_session_key ON "public".chat_messages (session_key);
CREATE INDEX IF NOT EXISTS idx_chat_messages_created_at ON "public".chat_messages (created_at);

CREATE TABLE IF NOT EXISTS "public".tutor_progress (
    subject_key TEXT NOT NULL,
    role TEXT NOT NULL,
    topic TEXT NOT NULL,
    last_question TEXT NOT NULL,
    last_answer TEXT NOT NULL,
    confidence TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    PRIMARY KEY (subject_key, topic)
);

CREATE TABLE IF NOT EXISTS "public".quiz_attempts (
    id BIGSERIAL PRIMARY KEY,
    subject_key TEXT NOT NULL,
    role TEXT NOT NULL,
    question TEXT NOT NULL,
    quiz_json TEXT NOT NULL DEFAULT '[]',
    created_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_quiz_attempts_subject_key ON "public".quiz_attempts (subject_key);
CREATE INDEX IF NOT EXISTS idx_quiz_attempts_created_at ON "public".quiz_attempts (created_at);

-- 2) Row Level Security
ALTER TABLE "public".pages ENABLE ROW LEVEL SECURITY;
ALTER TABLE "public".page_tags ENABLE ROW LEVEL SECURITY;
ALTER TABLE "public".page_sources ENABLE ROW LEVEL SECURITY;
ALTER TABLE "public".page_links ENABLE ROW LEVEL SECURITY;
ALTER TABLE "public".page_acl ENABLE ROW LEVEL SECURITY;
ALTER TABLE "public".session_tokens ENABLE ROW LEVEL SECURITY;
ALTER TABLE "public".activity_log ENABLE ROW LEVEL SECURITY;
ALTER TABLE "public".runtime_activity_log ENABLE ROW LEVEL SECURITY;
ALTER TABLE "public".query_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE "public".sync_state ENABLE ROW LEVEL SECURITY;
ALTER TABLE "public".chat_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE "public".chat_messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE "public".tutor_progress ENABLE ROW LEVEL SECURITY;
ALTER TABLE "public".quiz_attempts ENABLE ROW LEVEL SECURITY;

-- 3) Policies for init/admin runtime and backend runtime
DO $$
BEGIN
    -- pages
    DROP POLICY IF EXISTS "wiki_init can manage pages" ON "public".pages;
    CREATE POLICY "wiki_init can manage pages" ON "public".pages FOR ALL TO postgres USING (true) WITH CHECK (true);
    DROP POLICY IF EXISTS "wiki_backend can manage pages" ON "public".pages;
    CREATE POLICY "wiki_backend can manage pages" ON "public".pages FOR ALL TO wiki_backend USING (true) WITH CHECK (true);

    -- page_tags
    DROP POLICY IF EXISTS "wiki_init can manage page_tags" ON "public".page_tags;
    CREATE POLICY "wiki_init can manage page_tags" ON "public".page_tags FOR ALL TO postgres USING (true) WITH CHECK (true);
    DROP POLICY IF EXISTS "wiki_backend can manage page_tags" ON "public".page_tags;
    CREATE POLICY "wiki_backend can manage page_tags" ON "public".page_tags FOR ALL TO wiki_backend USING (true) WITH CHECK (true);

    -- page_sources
    DROP POLICY IF EXISTS "wiki_init can manage page_sources" ON "public".page_sources;
    CREATE POLICY "wiki_init can manage page_sources" ON "public".page_sources FOR ALL TO postgres USING (true) WITH CHECK (true);
    DROP POLICY IF EXISTS "wiki_backend can manage page_sources" ON "public".page_sources;
    CREATE POLICY "wiki_backend can manage page_sources" ON "public".page_sources FOR ALL TO wiki_backend USING (true) WITH CHECK (true);

    -- page_links
    DROP POLICY IF EXISTS "wiki_init can manage page_links" ON "public".page_links;
    CREATE POLICY "wiki_init can manage page_links" ON "public".page_links FOR ALL TO postgres USING (true) WITH CHECK (true);
    DROP POLICY IF EXISTS "wiki_backend can manage page_links" ON "public".page_links;
    CREATE POLICY "wiki_backend can manage page_links" ON "public".page_links FOR ALL TO wiki_backend USING (true) WITH CHECK (true);

    -- page_acl
    DROP POLICY IF EXISTS "wiki_init can manage page_acl" ON "public".page_acl;
    CREATE POLICY "wiki_init can manage page_acl" ON "public".page_acl FOR ALL TO postgres USING (true) WITH CHECK (true);
    DROP POLICY IF EXISTS "wiki_backend can manage page_acl" ON "public".page_acl;
    CREATE POLICY "wiki_backend can manage page_acl" ON "public".page_acl FOR ALL TO wiki_backend USING (true) WITH CHECK (true);

    -- session_tokens
    DROP POLICY IF EXISTS "wiki_init can manage session_tokens" ON "public".session_tokens;
    CREATE POLICY "wiki_init can manage session_tokens" ON "public".session_tokens FOR ALL TO postgres USING (true) WITH CHECK (true);
    DROP POLICY IF EXISTS "wiki_backend can manage session_tokens" ON "public".session_tokens;
    CREATE POLICY "wiki_backend can manage session_tokens" ON "public".session_tokens FOR ALL TO wiki_backend USING (true) WITH CHECK (true);

    -- activity_log
    DROP POLICY IF EXISTS "wiki_init can manage activity_log" ON "public".activity_log;
    CREATE POLICY "wiki_init can manage activity_log" ON "public".activity_log FOR ALL TO postgres USING (true) WITH CHECK (true);
    DROP POLICY IF EXISTS "wiki_backend can manage activity_log" ON "public".activity_log;
    CREATE POLICY "wiki_backend can manage activity_log" ON "public".activity_log FOR ALL TO wiki_backend USING (true) WITH CHECK (true);

    -- runtime_activity_log
    DROP POLICY IF EXISTS "wiki_init can manage runtime_activity_log" ON "public".runtime_activity_log;
    CREATE POLICY "wiki_init can manage runtime_activity_log" ON "public".runtime_activity_log FOR ALL TO postgres USING (true) WITH CHECK (true);
    DROP POLICY IF EXISTS "wiki_backend can manage runtime_activity_log" ON "public".runtime_activity_log;
    CREATE POLICY "wiki_backend can manage runtime_activity_log" ON "public".runtime_activity_log FOR ALL TO wiki_backend USING (true) WITH CHECK (true);

    -- query_logs
    DROP POLICY IF EXISTS "wiki_init can manage query_logs" ON "public".query_logs;
    CREATE POLICY "wiki_init can manage query_logs" ON "public".query_logs FOR ALL TO postgres USING (true) WITH CHECK (true);
    DROP POLICY IF EXISTS "wiki_backend can manage query_logs" ON "public".query_logs;
    CREATE POLICY "wiki_backend can manage query_logs" ON "public".query_logs FOR ALL TO wiki_backend USING (true) WITH CHECK (true);

    -- sync_state
    DROP POLICY IF EXISTS "wiki_init can manage sync_state" ON "public".sync_state;
    CREATE POLICY "wiki_init can manage sync_state" ON "public".sync_state FOR ALL TO postgres USING (true) WITH CHECK (true);
    DROP POLICY IF EXISTS "wiki_backend can manage sync_state" ON "public".sync_state;
    CREATE POLICY "wiki_backend can manage sync_state" ON "public".sync_state FOR ALL TO wiki_backend USING (true) WITH CHECK (true);

    -- tutor tables
    DROP POLICY IF EXISTS "wiki_init can manage chat_sessions" ON "public".chat_sessions;
    CREATE POLICY "wiki_init can manage chat_sessions" ON "public".chat_sessions FOR ALL TO postgres USING (true) WITH CHECK (true);
    DROP POLICY IF EXISTS "wiki_backend can manage chat_sessions" ON "public".chat_sessions;
    CREATE POLICY "wiki_backend can manage chat_sessions" ON "public".chat_sessions FOR ALL TO wiki_backend USING (true) WITH CHECK (true);

    DROP POLICY IF EXISTS "wiki_init can manage chat_messages" ON "public".chat_messages;
    CREATE POLICY "wiki_init can manage chat_messages" ON "public".chat_messages FOR ALL TO postgres USING (true) WITH CHECK (true);
    DROP POLICY IF EXISTS "wiki_backend can manage chat_messages" ON "public".chat_messages;
    CREATE POLICY "wiki_backend can manage chat_messages" ON "public".chat_messages FOR ALL TO wiki_backend USING (true) WITH CHECK (true);

    DROP POLICY IF EXISTS "wiki_init can manage tutor_progress" ON "public".tutor_progress;
    CREATE POLICY "wiki_init can manage tutor_progress" ON "public".tutor_progress FOR ALL TO postgres USING (true) WITH CHECK (true);
    DROP POLICY IF EXISTS "wiki_backend can manage tutor_progress" ON "public".tutor_progress;
    CREATE POLICY "wiki_backend can manage tutor_progress" ON "public".tutor_progress FOR ALL TO wiki_backend USING (true) WITH CHECK (true);

    DROP POLICY IF EXISTS "wiki_init can manage quiz_attempts" ON "public".quiz_attempts;
    CREATE POLICY "wiki_init can manage quiz_attempts" ON "public".quiz_attempts FOR ALL TO postgres USING (true) WITH CHECK (true);
    DROP POLICY IF EXISTS "wiki_backend can manage quiz_attempts" ON "public".quiz_attempts;
    CREATE POLICY "wiki_backend can manage quiz_attempts" ON "public".quiz_attempts FOR ALL TO wiki_backend USING (true) WITH CHECK (true);
END $$;

-- 4) Permissions helpers for backend role (safe to run if role exists)
GRANT USAGE ON SCHEMA public TO wiki_backend;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO wiki_backend;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO wiki_backend;

ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO wiki_backend;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT USAGE, SELECT ON SEQUENCES TO wiki_backend;

-- 5) Optional admin ownership notes
-- You can run the following only if needed and only from an owner/admin session:
-- ALTER TABLE public.pages OWNER TO postgres;
-- ALTER TABLE public.page_tags OWNER TO postgres;
-- ALTER TABLE public.page_sources OWNER TO postgres;
-- ALTER TABLE public.page_links OWNER TO postgres;
-- ALTER TABLE public.page_acl OWNER TO postgres;
-- ALTER TABLE public.session_tokens OWNER TO postgres;
-- ALTER TABLE public.activity_log OWNER TO postgres;
-- ALTER TABLE public.runtime_activity_log OWNER TO postgres;
-- ALTER TABLE public.query_logs OWNER TO postgres;
-- ALTER TABLE public.sync_state OWNER TO postgres;
-- ALTER TABLE public.chat_sessions OWNER TO postgres;
-- ALTER TABLE public.chat_messages OWNER TO postgres;
-- ALTER TABLE public.tutor_progress OWNER TO postgres;
-- ALTER TABLE public.quiz_attempts OWNER TO postgres;
