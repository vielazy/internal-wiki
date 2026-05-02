from __future__ import annotations

import json
import os
import re
import secrets
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from hashlib import sha256
from pathlib import Path
from urllib.parse import quote

import jwt

PROJECT_ROOT = Path(__file__).resolve().parents[1]
WIKI_ROOT = PROJECT_ROOT / "wiki"
DOTENV_PATH = PROJECT_ROOT / ".env"
SCHEMA_TEMPLATE_PATH = PROJECT_ROOT / "scripts" / "db_init.sql"
SECTIONS = (
    "concepts",
    "tools",
    "tutorials",
    "agents",
    "code-patterns",
    "syntheses",
)
LOG_PATH = WIKI_ROOT / "LOG.md"
VISIBILITY_VALUES = {"public", "internal", "restricted", "private"}
ROLE_ORDER = {"viewer": 0, "editor": 1, "admin": 2}
JWT_ALGORITHM = "HS256"


@dataclass(frozen=True)
class DatabaseSettings:
    dsn: str
    schema: str = "public"


@dataclass(frozen=True)
class AuthSettings:
    roles: dict[str, str]
    public_role: str = "viewer"
    jwt_secret: str = "replace-this-with-a-long-random-secret"
    session_ttl_seconds: int = 86400

    def normalize_role(self, role: str | None) -> str:
        candidate = str(role or self.public_role).strip().lower()
        return candidate if candidate in ROLE_ORDER else self.public_role

    def can_access(self, viewer_role: str, required_role: str) -> bool:
        viewer_rank = ROLE_ORDER.get(self.normalize_role(viewer_role), 0)
        required_rank = ROLE_ORDER.get(self.normalize_role(required_role), 0)
        return viewer_rank >= required_rank

    def resolve_role_for_token(self, token: str | None) -> str:
        token_value = str(token or "").strip()
        if not token_value:
            return self.public_role
        for role, secret in self.roles.items():
            if token_value == secret:
                return self.normalize_role(role)
        try:
            payload = jwt.decode(token_value, self.jwt_secret, algorithms=[JWT_ALGORITHM])
            return self.normalize_role(payload.get("role"))
        except Exception:
            return self.public_role

    def issue_session_token(self, role: str, subject: str) -> tuple[str, str, str]:
        normalized_role = self.normalize_role(role)
        now = datetime.now(timezone.utc)
        expires = now + timedelta(seconds=self.session_ttl_seconds)
        session_id = secrets.token_urlsafe(24)
        payload = {
            "sub": subject,
            "sid": session_id,
            "role": normalized_role,
            "iat": int(now.timestamp()),
            "exp": int(expires.timestamp()),
        }
        token = jwt.encode(payload, self.jwt_secret, algorithm=JWT_ALGORITHM)
        return session_id, token, expires.isoformat()


def load_dotenv(path: Path = DOTENV_PATH) -> None:
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8-sig").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def _load_database_settings_from_env(prefix: str = "") -> DatabaseSettings | None:
    schema = os.getenv(f"{prefix}WIKI_DB_SCHEMA", os.getenv("WIKI_DB_SCHEMA", "public")).strip() or "public"
    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", schema):
        raise RuntimeError(f"WIKI_DB_SCHEMA không hợp lệ: {schema}")

    dsn = os.getenv(f"{prefix}DATABASE_URL", "").strip()
    if not dsn:
        host = os.getenv(f"{prefix}POSTGRES_HOST", os.getenv("POSTGRES_HOST", "")).strip()
        port = os.getenv(f"{prefix}POSTGRES_PORT", os.getenv("POSTGRES_PORT", "5432")).strip() or "5432"
        database = os.getenv(f"{prefix}POSTGRES_DB", os.getenv("POSTGRES_DB", "")).strip()
        user = os.getenv(f"{prefix}POSTGRES_USER", os.getenv("POSTGRES_USER", "")).strip()
        password = os.getenv(f"{prefix}POSTGRES_PASSWORD", os.getenv("POSTGRES_PASSWORD", "")).strip()
        if not all([host, port, database, user, password]):
            return None
        dsn = f"postgresql://{quote(user, safe='')}:{quote(password, safe='')}@{host}:{port}/{database}"

    if "connect_timeout=" not in dsn:
        joiner = "&" if "?" in dsn else "?"
        dsn = f"{dsn}{joiner}connect_timeout=30"
    if "sslmode=" not in dsn:
        joiner = "&" if "?" in dsn else "?"
        dsn = f"{dsn}{joiner}sslmode=require"
    if "connect_timeout=" not in dsn:
        joiner = "&" if "?" in dsn else "?"
        dsn = f"{dsn}{joiner}connect_timeout=30"
    if "sslmode=" not in dsn:
        joiner = "&" if "?" in dsn else "?"
        dsn = f"{dsn}{joiner}sslmode=require"
    return DatabaseSettings(dsn=dsn, schema=schema)


def load_database_settings() -> DatabaseSettings | None:
    load_dotenv()
    return _load_database_settings_from_env("")


def load_admin_database_settings() -> DatabaseSettings | None:
    load_dotenv()
    return _load_database_settings_from_env("ADMIN_")


def load_auth_settings() -> AuthSettings:
    load_dotenv()
    raw_roles = os.getenv("WIKI_AUTH_ROLES", "{}").strip()
    try:
        parsed = json.loads(raw_roles) if raw_roles else {}
    except json.JSONDecodeError as exc:
        raise RuntimeError("WIKI_AUTH_ROLES không hợp lệ, phải là JSON object.") from exc
    if not isinstance(parsed, dict):
        raise RuntimeError("WIKI_AUTH_ROLES phải là JSON object.")
    normalized: dict[str, str] = {}
    for role, secret in parsed.items():
        role_name = str(role).strip().lower()
        if role_name in ROLE_ORDER:
            normalized[role_name] = str(secret)
    public_role = os.getenv("WIKI_PUBLIC_ROLE", "viewer").strip().lower() or "viewer"
    if public_role not in ROLE_ORDER:
        public_role = "viewer"
    jwt_secret = os.getenv("WIKI_JWT_SECRET", "replace-this-with-a-long-random-secret").strip()
    ttl_raw = os.getenv("WIKI_SESSION_TTL_SECONDS", "86400").strip()
    try:
        ttl = int(ttl_raw)
    except ValueError:
        ttl = 86400
    return AuthSettings(roles=normalized, public_role=public_role, jwt_secret=jwt_secret, session_ttl_seconds=ttl)


def load_auth_accounts_from_db(settings: DatabaseSettings) -> dict[str, dict[str, object]]:
    with open_db_connection(settings) as connection:
        set_search_path(connection, settings)
        rows = list(connection.execute("SELECT role, username, password_hash, display_name, active FROM auth_accounts WHERE active = 1"))
    accounts: dict[str, dict[str, object]] = {}
    for row in rows:
        role = str(row["role"]).strip().lower()
        accounts[role] = {
            "username": str(row["username"]),
            "password_hash": str(row["password_hash"]),
            "display_name": str(row["display_name"]),
            "active": bool(row["active"]),
        }
    return accounts


def authenticate_db_account(settings: DatabaseSettings, role: str, password: str) -> dict[str, object] | None:
    role_name = str(role).strip().lower()
    if role_name not in {"editor", "admin"}:
        return None
    with open_db_connection(settings) as connection:
        set_search_path(connection, settings)
        row = connection.execute(
            "SELECT role, username, password_hash, display_name, active FROM auth_accounts WHERE role = %s AND active = 1 LIMIT 1",
            (role_name,),
        ).fetchone()
    if not row:
        return None
    import bcrypt  # type: ignore
    password_hash = str(row["password_hash"])
    if not password_hash.startswith("$2"):
        return None
    if bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8")):
        return {"role": str(row["role"]), "username": str(row["username"]), "display_name": str(row["display_name"])}
    return None


def content_hash_for_text(text: str) -> str:
    return sha256(text.encode("utf-8")).hexdigest()


def duplicate_candidates_for_text(text: str, pages: list[dict[str, object]], limit: int = 5) -> list[dict[str, object]]:
    query = str(text or "").lower()
    scored: list[tuple[int, dict[str, object]]] = []
    for page in pages:
        haystack = " ".join([
            str(page.get("title", "")),
            str(page.get("topic", "")),
            str(page.get("section", "")),
            str(page.get("excerpt", "")),
            str(page.get("body", ""))[:5000],
        ]).lower()
        score = 0
        if query and query in haystack:
            score += 50
        for token in set(re.findall(r"[a-z0-9_\-]{4,}", query)):
            if token in haystack:
                score += 10
        overlap = len(set(query.split()) & set(haystack.split()))
        score += overlap
        if score > 0:
            scored.append((score, page))
    scored.sort(key=lambda item: (-item[0], str(item[1].get("title", "")).lower()))
    return [
        {
            "id": page.get("id"),
            "title": page.get("title"),
            "path": page.get("path"),
            "topic": page.get("topic"),
            "section": page.get("section"),
            "visibility": page.get("visibility", "public"),
            "excerpt": page.get("excerpt", ""),
            "score": score,
        }
        for score, page in scored[:limit]
    ]


def require_psycopg():
    try:
        import psycopg  # type: ignore
        from psycopg.rows import dict_row  # type: ignore
    except ImportError as exc:
        raise RuntimeError("Thiếu dependency PostgreSQL. Cài requirements.txt hoặc ít nhất `psycopg[binary]`.") from exc
    return psycopg, dict_row


def open_db_connection(settings: DatabaseSettings):
    psycopg, dict_row = require_psycopg()
    return psycopg.connect(settings.dsn, row_factory=dict_row)


def set_search_path(connection, settings: DatabaseSettings) -> None:
    connection.execute(f'SET search_path TO "{settings.schema}", public')


def apply_schema(settings: DatabaseSettings) -> None:
    sql_template = SCHEMA_TEMPLATE_PATH.read_text(encoding="utf-8")
    sql = sql_template.replace("__WIKI_SCHEMA__", settings.schema)
    with open_db_connection(settings) as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql)
        connection.commit()


def iso_date_from_timestamp(timestamp: float) -> str:
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")


def split_frontmatter(text: str) -> tuple[dict[str, object], str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text.strip()
    frontmatter_lines: list[str] = []
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            body = "\n".join(lines[index + 1 :]).strip()
            return parse_frontmatter(frontmatter_lines), body
        frontmatter_lines.append(line)
    return {}, text.strip()


def parse_frontmatter(lines: list[str]) -> dict[str, object]:
    data: dict[str, object] = {}
    current_list_key: str | None = None
    for raw_line in lines:
        stripped = raw_line.strip()
        if not stripped:
            continue
        if stripped.startswith("- ") and current_list_key:
            data.setdefault(current_list_key, [])
            values = data[current_list_key]
            if isinstance(values, list):
                values.append(parse_scalar(stripped[2:].strip()))
            continue
        current_list_key = None
        if ":" not in stripped:
            continue
        key, value = stripped.split(":", 1)
        key = key.strip()
        value = value.strip()
        if not value:
            data[key] = []
            current_list_key = key
            continue
        data[key] = parse_scalar(value)
    return data


def parse_scalar(value: str) -> object:
    value = value.strip()
    if not value:
        return ""
    if value[0] in {'"', "'"} and value[-1] == value[0]:
        return value[1:-1]
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [parse_scalar(item.strip()) for item in inner.split(",")]
    return value


def extract_summary(body: str) -> str:
    summary_match = re.search(r"^##\s+Tóm tắt\s*$([\s\S]*?)(?=^##\s+|\Z)", body, flags=re.MULTILINE)
    if summary_match:
        candidate = " ".join(line.strip() for line in summary_match.group(1).splitlines() if line.strip())
        if candidate:
            return candidate
    for paragraph in re.split(r"\n\s*\n", body):
        cleaned = paragraph.strip()
        if cleaned and not cleaned.startswith("#"):
            return " ".join(cleaned.split())
    return ""


def extract_related_slugs(body: str) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for slug in re.findall(r"\[\[([^\]]+)\]\]", body):
        cleaned = slug.strip()
        if cleaned and cleaned not in seen:
            seen.add(cleaned)
            ordered.append(cleaned)
    return ordered


def extract_headings(body: str) -> list[dict[str, object]]:
    headings: list[dict[str, object]] = []
    for line in body.splitlines():
        match = re.match(r"^(#{1,3})\s+(.+?)\s*$", line.strip())
        if not match:
            continue
        title = match.group(2).strip()
        headings.append({"level": len(match.group(1)), "title": title, "anchor": slugify(title)})
    return headings


def slugify(value: str) -> str:
    lowered = value.casefold()
    normalized = re.sub(r"[^\w\s-]", "", lowered)
    compact = re.sub(r"[-\s]+", "-", normalized).strip("-")
    return compact or "section"


def count_words(text: str) -> int:
    return len(re.findall(r"\b[\w-]+\b", text, flags=re.UNICODE))


def normalize_visibility(value: object) -> str:
    visibility = str(value or "public").strip().lower()
    return visibility if visibility in VISIBILITY_VALUES else "public"


def scan_pages() -> list[dict[str, object]]:
    pages: list[dict[str, object]] = []
    for section in SECTIONS:
        section_dir = WIKI_ROOT / section
        if not section_dir.exists():
            continue
        for path in sorted(section_dir.glob("*.md")):
            raw_text = path.read_text(encoding="utf-8-sig")
            metadata, body = split_frontmatter(raw_text)
            file_stat = path.stat()
            title = str(metadata.get("title") or path.stem.replace("-", " ").title())
            topic = str(metadata.get("topic") or section.replace("-", " ").title())
            tags = metadata.get("tags")
            sources = metadata.get("sources")
            acl = metadata.get("acl")
            created = str(metadata.get("created") or iso_date_from_timestamp(file_stat.st_ctime))
            updated = str(metadata.get("updated") or iso_date_from_timestamp(file_stat.st_mtime))
            pages.append({
                "id": f"{section}/{path.stem}",
                "slug": path.stem,
                "title": title,
                "topic": topic,
                "section": section,
                "path": path.relative_to(PROJECT_ROOT).as_posix(),
                "created": created,
                "updated": updated,
                "confidence": str(metadata.get("confidence") or "unknown"),
                "visibility": normalize_visibility(metadata.get("visibility")),
                "tags": tags if isinstance(tags, list) else [],
                "sources": sources if isinstance(sources, list) else [],
                "acl": acl if isinstance(acl, list) else [],
                "excerpt": extract_summary(body),
                "relatedSlugs": extract_related_slugs(body),
                "headings": extract_headings(body),
                "wordCount": count_words(body),
                "body": body,
                "contentHash": sha256(raw_text.encode("utf-8")).hexdigest(),
            })
    pages.sort(key=lambda item: (item["section"], str(item["title"]).casefold()))
    return pages


def build_page_summary(page: dict[str, object]) -> dict[str, object]:
    return {
        "id": page["id"],
        "slug": page["slug"],
        "title": page["title"],
        "topic": page["topic"],
        "section": page["section"],
        "path": page["path"],
        "updated": page["updated"],
        "confidence": page["confidence"],
        "tags": page["tags"],
        "excerpt": page["excerpt"],
        "wordCount": page["wordCount"],
        "visibility": page.get("visibility", "public"),
        "acl": page.get("acl", []),
    }


def acl_entry_permission(entry: object) -> str:
    if isinstance(entry, dict):
        return str(entry.get("permission") or "read").strip().lower()
    return "read"


def acl_entry_subject(entry: object) -> tuple[str, str] | None:
    if isinstance(entry, dict):
        subject_type = str(entry.get("subject_type") or entry.get("subjectType") or "").strip().lower()
        subject_value = str(entry.get("subject_value") or entry.get("subjectValue") or "").strip().lower()
        if subject_type and subject_value:
            return subject_type, subject_value
    return None


def role_allows_visibility(role: str, visibility: str) -> bool:
    visibility = normalize_visibility(visibility)
    if visibility == "public":
        return True
    if visibility == "internal":
        return ROLE_ORDER.get(role, 0) >= ROLE_ORDER["viewer"]
    if visibility == "restricted":
        return ROLE_ORDER.get(role, 0) >= ROLE_ORDER["editor"]
    if visibility == "private":
        return ROLE_ORDER.get(role, 0) >= ROLE_ORDER["admin"]
    return False


def acl_allows_access(page: dict[str, object], role: str, subject: str | None = None) -> bool:
    if not role_allows_visibility(role, str(page.get("visibility", "public"))):
        return False
    acl_rules = page.get("acl") or []
    if not isinstance(acl_rules, list) or not acl_rules:
        return True
    normalized_subject = str(subject or "").strip().lower()
    normalized_role = str(role or "viewer").strip().lower()
    allowed = False
    for entry in acl_rules:
        if not isinstance(entry, dict):
            continue
        permission = acl_entry_permission(entry)
        subject_type, subject_value = acl_entry_subject(entry) or ("", "")
        if permission not in {"read", "view", "allow"}:
            continue
        if subject_type == "role" and subject_value == normalized_role:
            allowed = True
        elif subject_type == "user" and subject_value and subject_value == normalized_subject:
            allowed = True
        elif subject_type == "public" and subject_value in {"*", "true", "yes", "1"}:
            allowed = True
    return allowed or normalized_role == "admin"


def filter_pages_for_role(pages: list[dict[str, object]], role: str, subject: str | None = None) -> list[dict[str, object]]:
    return [page for page in pages if acl_allows_access(page, role, subject=subject)]


def resolve_slug_match(slug: str, current_page: dict[str, object], slug_index: dict[str, list[dict[str, object]]]) -> dict[str, object] | None:
    matches = slug_index.get(slug, [])
    if not matches:
        return None
    if len(matches) == 1:
        return matches[0]
    for candidate in matches:
        if candidate["section"] == current_page["section"]:
            return candidate
    for candidate in matches:
        if candidate["topic"] == current_page["topic"]:
            return candidate
    return matches[0]


def parse_log(limit: int | None = 10) -> list[dict[str, str]]:
    if not LOG_PATH.exists():
        return []
    entries: list[dict[str, str]] = []
    pattern = re.compile(r"^\[(?P<timestamp>[^\]]+)\]\s+\[(?P<action>[^\]]+)\]\s+(?P<message>.+)$")
    for line in LOG_PATH.read_text(encoding="utf-8-sig").splitlines():
        match = pattern.match(line.strip())
        if not match:
            continue
        entries.append(match.groupdict())
    if limit is None:
        return entries
    return list(reversed(entries[-limit:]))


def enrich_page_from_files(page_id: str, pages: list[dict[str, object]] | None = None, role: str = "viewer", subject: str | None = None) -> dict[str, object] | None:
    pages = filter_pages_for_role(pages or scan_pages(), role, subject=subject)
    by_id = {page["id"]: page for page in pages}
    slug_index: dict[str, list[dict[str, object]]] = defaultdict(list)
    for page in pages:
        slug_index[str(page["slug"])].append(page)
    page = by_id.get(page_id)
    if not page:
        return None
    related_pages: list[dict[str, object]] = []
    seen_related: set[str] = set()
    for slug in page["relatedSlugs"]:
        related_page = resolve_slug_match(str(slug), page, slug_index)
        if not related_page:
            continue
        related_id = str(related_page["id"])
        if related_id in seen_related or related_id == page_id:
            continue
        seen_related.add(related_id)
        related_pages.append(build_page_summary(related_page))
    backlinks: list[dict[str, object]] = []
    seen_backlinks: set[str] = set()
    page_slug = str(page["slug"])
    for candidate in pages:
        candidate_id = str(candidate["id"])
        if candidate_id == page_id:
            continue
        if page_slug in candidate["relatedSlugs"] and candidate_id not in seen_backlinks:
            seen_backlinks.add(candidate_id)
            backlinks.append(build_page_summary(candidate))
    payload = build_page_summary(page)
    payload.update({"created": page["created"], "sources": page["sources"], "body": page["body"], "headings": page["headings"], "relatedPages": related_pages, "backlinks": backlinks})
    return payload


def build_bootstrap_from_files(role: str = "viewer", subject: str | None = None) -> dict[str, object]:
    pages = filter_pages_for_role(scan_pages(), role, subject=subject)
    section_counts = Counter(str(page["section"]) for page in pages)
    topics = sorted({str(page["topic"]) for page in pages})
    latest_updated = max((str(page["updated"]) for page in pages), default="-")
    return {"mode": "file", "role": role, "generatedAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "stats": {"pageCount": len(pages), "topicCount": len(topics), "sectionCount": sum(1 for section in SECTIONS if section_counts.get(section)), "latestUpdated": latest_updated}, "sections": [{"name": section, "count": section_counts.get(section, 0)} for section in SECTIONS if section_counts.get(section, 0)], "topics": topics, "pages": [build_page_summary(page) for page in pages], "recentUpdates": parse_log()}


def sync_database(settings: DatabaseSettings) -> dict[str, int]:
    pages = scan_pages()
    logs = parse_log(limit=None)
    slug_index: dict[str, list[dict[str, object]]] = defaultdict(list)
    page_ids = {str(page["id"]) for page in pages}
    content_hash = sha256("".join(str(page["contentHash"]) for page in pages).encode("utf-8")).hexdigest()
    for page in pages:
        slug_index[str(page["slug"])].append(page)
    with open_db_connection(settings) as connection:
        set_search_path(connection, settings)
        with connection.transaction():
            for page in pages:
                connection.execute(
                    """
                    INSERT INTO pages (
                        id, slug, title, topic, section, path,
                        created, updated, confidence, visibility,
                        excerpt, body, word_count, headings_json, content_hash, synced_at
                    )
                    VALUES (
                        %(id)s, %(slug)s, %(title)s, %(topic)s, %(section)s, %(path)s,
                        %(created)s, %(updated)s, %(confidence)s, %(visibility)s,
                        %(excerpt)s, %(body)s, %(word_count)s, %(headings_json)s, %(content_hash)s, %(synced_at)s
                    )
                    ON CONFLICT (id) DO UPDATE SET
                        slug = EXCLUDED.slug,
                        title = EXCLUDED.title,
                        topic = EXCLUDED.topic,
                        section = EXCLUDED.section,
                        path = EXCLUDED.path,
                        created = EXCLUDED.created,
                        updated = EXCLUDED.updated,
                        confidence = EXCLUDED.confidence,
                        visibility = EXCLUDED.visibility,
                        excerpt = EXCLUDED.excerpt,
                        body = EXCLUDED.body,
                        word_count = EXCLUDED.word_count,
                        headings_json = EXCLUDED.headings_json,
                        content_hash = EXCLUDED.content_hash,
                        synced_at = EXCLUDED.synced_at
                    """,
                    {"id": page["id"], "slug": page["slug"], "title": page["title"], "topic": page["topic"], "section": page["section"], "path": page["path"], "created": page["created"], "updated": page["updated"], "confidence": page["confidence"], "visibility": page["visibility"], "excerpt": page["excerpt"], "body": page["body"], "word_count": page["wordCount"], "headings_json": json.dumps(page["headings"], ensure_ascii=False), "content_hash": page["contentHash"], "synced_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")},
                )
            connection.execute("DELETE FROM page_links")
            connection.execute("DELETE FROM page_sources")
            connection.execute("DELETE FROM page_tags")
            for page in pages:
                unique_tags = list(dict.fromkeys(str(tag) for tag in page["tags"]))
                for index, tag in enumerate(unique_tags, start=1):
                    connection.execute("INSERT INTO page_tags (page_id, tag, position) VALUES (%s, %s, %s) ON CONFLICT (page_id, tag) DO UPDATE SET position = EXCLUDED.position", (page["id"], tag, index))
                for index, source in enumerate(page["sources"], start=1):
                    connection.execute("INSERT INTO page_sources (page_id, source, position) VALUES (%s, %s, %s) ON CONFLICT (page_id, position) DO UPDATE SET source = EXCLUDED.source", (page["id"], str(source), index))
                for index, slug in enumerate(page["relatedSlugs"], start=1):
                    target_page_id = None
                    related_page = resolve_slug_match(str(slug), page, slug_index)
                    if related_page:
                        candidate_id = str(related_page["id"])
                        if candidate_id in page_ids and candidate_id != page["id"]:
                            target_page_id = candidate_id
                    connection.execute("INSERT INTO page_links (source_page_id, target_slug, target_page_id, position) VALUES (%s, %s, %s, %s) ON CONFLICT (source_page_id, position) DO UPDATE SET target_slug = EXCLUDED.target_slug, target_page_id = EXCLUDED.target_page_id", (page["id"], str(slug), target_page_id, index))
            connection.execute("INSERT INTO sync_state (sync_key, last_synced_at, last_page_count, last_content_hash) VALUES ('wiki', %s, %s, %s) ON CONFLICT (sync_key) DO UPDATE SET last_synced_at = EXCLUDED.last_synced_at, last_page_count = EXCLUDED.last_page_count, last_content_hash = EXCLUDED.last_content_hash", (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), len(pages), content_hash))
    return {"pages": len(pages), "tags": sum(len(page["tags"]) for page in pages), "sources": sum(len(page["sources"]) for page in pages), "links": sum(len(page["relatedSlugs"]) for page in pages), "activity": len(logs)}


def build_bootstrap_from_db(settings: DatabaseSettings, role: str = "viewer", subject: str | None = None) -> dict[str, object]:
    with open_db_connection(settings) as connection:
        set_search_path(connection, settings)
        sync_state = connection.execute("SELECT last_synced_at, last_page_count, last_content_hash FROM sync_state WHERE sync_key = 'wiki'").fetchone()
        page_rows = list(connection.execute("""
                SELECT p.id, p.slug, p.title, p.topic, p.section, p.path, p.updated,
                       p.confidence, p.visibility, p.excerpt, p.word_count,
                       COALESCE((SELECT array_agg(pt.tag ORDER BY pt.position) FROM page_tags pt WHERE pt.page_id = p.id), ARRAY[]::text[]) AS tags,
                       COALESCE((SELECT json_agg(json_build_object('subject_type', a.subject_type, 'subject_value', a.subject_value, 'permission', a.permission) ORDER BY a.id) FROM page_acl a WHERE a.page_id = p.id), '[]'::json) AS acl
                FROM pages p
                ORDER BY p.section ASC, lower(p.title) ASC
                """))
        sections = list(connection.execute("SELECT section AS name, COUNT(*) AS count FROM pages GROUP BY section ORDER BY section ASC"))
        latest = connection.execute("SELECT COALESCE(MAX(updated), '-') AS latest_updated FROM pages").fetchone()
        recent_updates = list(connection.execute("SELECT logged_at AS timestamp, action, message FROM activity_log ORDER BY ordinal DESC LIMIT 10"))
    pages = [{"id": row["id"], "slug": row["slug"], "title": row["title"], "topic": row["topic"], "section": row["section"], "path": row["path"], "updated": row["updated"], "confidence": row["confidence"], "visibility": row["visibility"], "tags": list(row["tags"] or []), "excerpt": row["excerpt"], "wordCount": row["word_count"], "acl": json.loads(row["acl"] or "[]")} for row in page_rows]
    visible_pages = filter_pages_for_role(pages, role, subject=subject)
    visible_sections = Counter(str(page["section"]) for page in visible_pages)
    visible_topics = sorted({str(page["topic"]) for page in visible_pages})
    return {"mode": "db", "role": role, "generatedAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "syncState": sync_state, "stats": {"pageCount": len(visible_pages), "topicCount": len(visible_topics), "sectionCount": len([section for section in sections if visible_sections.get(section["name"], 0)]), "latestUpdated": latest["latest_updated"] if latest else "-"}, "sections": [{"name": section["name"], "count": visible_sections.get(section["name"], 0)} for section in sections if visible_sections.get(section["name"], 0)], "topics": visible_topics, "pages": visible_pages, "recentUpdates": recent_updates}


def fetch_page_from_db(settings: DatabaseSettings, page_id: str, role: str = "viewer", subject: str | None = None) -> dict[str, object] | None:
    with open_db_connection(settings) as connection:
        set_search_path(connection, settings)
        page = connection.execute("SELECT id, slug, title, topic, section, path, created, updated, confidence, visibility, excerpt, body, word_count, headings_json FROM pages WHERE id = %s", (page_id,)).fetchone()
        if not page:
            return None
        tags = [row["tag"] for row in connection.execute("SELECT tag FROM page_tags WHERE page_id = %s ORDER BY position ASC", (page_id,))]
        sources = [row["source"] for row in connection.execute("SELECT source FROM page_sources WHERE page_id = %s ORDER BY position ASC", (page_id,))]
        acl_rows = list(connection.execute("SELECT subject_type, subject_value, permission FROM page_acl WHERE page_id = %s ORDER BY id ASC", (page_id,)))
        related_rows = list(connection.execute("SELECT p.id, p.slug, p.title, p.topic, p.section, p.path, p.updated, p.confidence, p.visibility, p.excerpt, p.word_count FROM page_links l JOIN pages p ON p.id = l.target_page_id WHERE l.source_page_id = %s ORDER BY l.position ASC", (page_id,)))
        backlink_rows = list(connection.execute("SELECT p.id, p.slug, p.title, p.topic, p.section, p.path, p.updated, p.confidence, p.visibility, p.excerpt, p.word_count FROM page_links l JOIN pages p ON p.id = l.source_page_id WHERE l.target_page_id = %s ORDER BY lower(p.title) ASC", (page_id,)))
    page_payload = {"id": page["id"], "slug": page["slug"], "title": page["title"], "topic": page["topic"], "section": page["section"], "path": page["path"], "created": page["created"], "updated": page["updated"], "confidence": page["confidence"], "visibility": page["visibility"], "tags": tags, "excerpt": page["excerpt"], "wordCount": page["word_count"], "body": page["body"], "headings": json.loads(page["headings_json"] or "[]"), "sources": sources, "acl": [{"subject_type": row["subject_type"], "subject_value": row["subject_value"], "permission": row["permission"]} for row in acl_rows], "relatedPages": [], "backlinks": []}
    if not acl_allows_access(page_payload, role, subject=subject):
        return None
    page_payload["relatedPages"] = [{"id": row["id"], "slug": row["slug"], "title": row["title"], "topic": row["topic"], "section": row["section"], "path": row["path"], "updated": row["updated"], "confidence": row["confidence"], "visibility": row["visibility"], "tags": [], "excerpt": row["excerpt"], "wordCount": row["word_count"], "acl": []} for row in related_rows if acl_allows_access({"visibility": row["visibility"], "acl": []}, role, subject=subject)]
    page_payload["backlinks"] = [{"id": row["id"], "slug": row["slug"], "title": row["title"], "topic": row["topic"], "section": row["section"], "path": row["path"], "updated": row["updated"], "confidence": row["confidence"], "visibility": row["visibility"], "tags": [], "excerpt": row["excerpt"], "wordCount": row["word_count"], "acl": []} for row in backlink_rows if acl_allows_access({"visibility": row["visibility"], "acl": []}, role, subject=subject)]
    return page_payload


def _score_text_query(query: str, title: str, topic: str, section: str, excerpt: str, body: str, tags: list[object] | None = None, acl: list[object] | None = None) -> tuple[int, int]:
    normalized = " ".join(str(query or "").lower().split())
    haystack = " ".join([
        str(title or ""),
        str(topic or ""),
        str(section or ""),
        str(excerpt or ""),
        " ".join(map(str, tags or [])),
        " ".join(map(str, acl or [])),
        str(body or ""),
    ]).lower()
    score = 0
    if normalized in haystack:
        score += 30 + haystack.count(normalized) * 2
    if str(title or "").lower() in normalized:
        score += 15
    if normalized.startswith(str(title or "").lower()):
        score += 10
    query_tokens = [token for token in re.findall(r"[a-z0-9_\-]+", normalized) if len(token) > 1 and token not in {"toi", "cho", "la", "gi", "giup", "the", "co", "trong", "voi", "va", "de", "mot", "nhung", "nhu", "tai", "ve", "cua", "anh", "chi", "em", "ban", "please", "help", "tell", "me", "about"}]
    if query_tokens:
        token_hits = sum(1 for token in query_tokens if token in haystack)
        score += token_hits * 5
        if token_hits < max(1, len(query_tokens) // 2):
            return 0, len(haystack)
    return score, len(haystack)


def search_pages(query: str, pages: list[dict[str, object]], role: str = "viewer", subject: str | None = None, limit: int = 10) -> list[dict[str, object]]:
    normalized = " ".join(str(query or "").lower().split())
    if not normalized:
        return []
    results: list[tuple[int, int, dict[str, object]]] = []
    for page in filter_pages_for_role(pages, role, subject=subject):
        score, haystack_len = _score_text_query(
            normalized,
            str(page.get("title", "")),
            str(page.get("topic", "")),
            str(page.get("section", "")),
            str(page.get("excerpt", "")),
            str(page.get("body", "")),
            page.get("tags", []),
            page.get("acl", []),
        )
        if score > 0:
            results.append((score, haystack_len, build_page_summary(page)))
    results.sort(key=lambda item: (-item[0], item[1], str(item[2]["title"]).lower()))
    return [item[2] for item in results[:limit]]


def build_search_clause(query: str) -> str:
    normalized = " ".join(str(query or "").lower().split())
    tokens = [token for token in re.findall(r"[a-z0-9_\-]+", normalized) if len(token) > 1]
    if not tokens:
        return ""
    terms = [f"title ILIKE '%{normalized}%'", f"topic ILIKE '%{normalized}%'", f"excerpt ILIKE '%{normalized}%'", f"body ILIKE '%{normalized}%'", f"search_vector ILIKE '%{normalized}%'" ]
    terms.extend([f"title ILIKE '%{token}%'"] for token in tokens)
    return normalized


def search_pages_in_db(settings: DatabaseSettings, query: str, role: str = "viewer", subject: str | None = None, limit: int = 10) -> list[dict[str, object]]:
    normalized = " ".join(str(query or "").lower().split())
    if not normalized:
        return []
    with open_db_connection(settings) as connection:
        set_search_path(connection, settings)
        rows = list(connection.execute(
            """
            SELECT p.id, p.slug, p.title, p.topic, p.section, p.path, p.updated,
                   p.confidence, p.visibility, p.excerpt, p.body, p.word_count,
                   COALESCE((SELECT array_agg(pt.tag ORDER BY pt.position) FROM page_tags pt WHERE pt.page_id = p.id), ARRAY[]::text[]) AS tags,
                   COALESCE((SELECT json_agg(json_build_object('subject_type', a.subject_type, 'subject_value', a.subject_value, 'permission', a.permission) ORDER BY a.id) FROM page_acl a WHERE a.page_id = p.id), '[]'::json) AS acl
            FROM pages p
            ORDER BY p.section ASC, lower(p.title) ASC
            """
        ))
    scored: list[tuple[int, int, dict[str, object]]] = []
    for row in rows:
        page = {
            "id": row["id"],
            "slug": row["slug"],
            "title": row["title"],
            "topic": row["topic"],
            "section": row["section"],
            "path": row["path"],
            "updated": row["updated"],
            "confidence": row["confidence"],
            "visibility": row["visibility"],
            "tags": list(row["tags"] or []),
            "excerpt": row["excerpt"],
            "wordCount": row["word_count"],
            "acl": json.loads(row["acl"] or "[]"),
        }
        if not acl_allows_access(page, role, subject=subject):
            continue
        score, haystack_len = _score_text_query(normalized, str(row["title"]), str(row["topic"]), str(row["section"]), str(row["excerpt"]), str(row["body"]), list(row["tags"] or []), page.get("acl", []))
        if score > 0:
            scored.append((score, haystack_len, build_page_summary(page)))
    scored.sort(key=lambda item: (-item[0], item[1], str(item[2]["title"]).lower()))
    return [item[2] for item in scored[:limit]]


def search_pages_in_db(settings: DatabaseSettings, query: str, role: str = "viewer", subject: str | None = None, limit: int = 10) -> list[dict[str, object]]:
    normalized = " ".join(str(query or "").lower().split())
    if not normalized:
        return []
    with open_db_connection(settings) as connection:
        set_search_path(connection, settings)
        rows = list(connection.execute(
            """
            SELECT p.id, p.slug, p.title, p.topic, p.section, p.path, p.updated,
                   p.confidence, p.visibility, p.excerpt, p.body, p.word_count,
                   COALESCE((SELECT array_agg(pt.tag ORDER BY pt.position) FROM page_tags pt WHERE pt.page_id = p.id), ARRAY[]::text[]) AS tags,
                   COALESCE((SELECT json_agg(json_build_object('subject_type', a.subject_type, 'subject_value', a.subject_value, 'permission', a.permission) ORDER BY a.id) FROM page_acl a WHERE a.page_id = p.id), '[]'::json) AS acl
            FROM pages p
            ORDER BY p.section ASC, lower(p.title) ASC
            """
        ))
    scored: list[tuple[int, int, dict[str, object]]] = []
    for row in rows:
        page = {
            "id": row["id"],
            "slug": row["slug"],
            "title": row["title"],
            "topic": row["topic"],
            "section": row["section"],
            "path": row["path"],
            "updated": row["updated"],
            "confidence": row["confidence"],
            "visibility": row["visibility"],
            "tags": list(row["tags"] or []),
            "excerpt": row["excerpt"],
            "wordCount": row["word_count"],
            "acl": json.loads(row["acl"] or "[]"),
        }
        if not acl_allows_access(page, role, subject=subject):
            continue
        score, haystack_len = _score_text_query(normalized, str(row["title"]), str(row["topic"]), str(row["section"]), str(row["excerpt"]), str(row["body"]), list(row["tags"] or []), page.get("acl", []))
        if score > 0:
            scored.append((score, haystack_len, build_page_summary(page)))
    scored.sort(key=lambda item: (-item[0], item[1], str(item[2]["title"]).lower()))
    return [item[2] for item in scored[:limit]]


def build_chat_answer(question: str, pages: list[dict[str, object]], role: str = "viewer", subject: str | None = None, limit: int = 5) -> dict[str, object]:
    matches = search_pages(question, pages, role=role, subject=subject, limit=limit)
    citations = []
    bullets = []
    for page in matches:
        citations.append({"id": page["id"], "title": page["title"], "path": page["path"], "visibility": page.get("visibility", "public")})
        bullets.append(f"- {page['title']} ({page['section']}): {page.get('excerpt') or 'Không có tóm tắt'}")
    answer = "\n".join(bullets) if bullets else "Không tìm thấy tài liệu phù hợp trong phạm vi quyền hiện tại."
    return {"question": question, "role": role, "answer": answer, "citations": citations, "matchCount": len(matches)}
