from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import time
import unicodedata
from dataclasses import dataclass
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import jwt

from tutor_agent import build_tutor_reply
from upload_extractor import build_draft_from_text, extract_text_from_upload
from storage_client import upload_to_supabase_storage
from wiki_api_helpers import build_quiz_pack_from_pages, duplicate_check_payload
from wiki_runtime import (
    PROJECT_ROOT,
    AuthSettings,
    DatabaseSettings,
    authenticate_db_account,
    build_bootstrap_from_db,
    build_bootstrap_from_files,
    build_chat_answer,
    enrich_page_from_files,
    fetch_page_from_db,
    load_auth_settings,
    load_database_settings,
    open_db_connection,
    scan_pages,
    set_search_path,
    search_pages,
)


def slugify(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", str(text))
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]+", "-", ascii_text.lower()).strip("-") or "page"


@dataclass(frozen=True)
class RepositoryState:
    mode: str
    db_settings: DatabaseSettings | None = None
    auth_settings: AuthSettings | None = None

    def build_bootstrap(self, role: str = "viewer", subject: str | None = None) -> dict[str, object]:
        if self.mode == "db" and self.db_settings:
            return build_bootstrap_from_db(self.db_settings, role=role, subject=subject)
        return build_bootstrap_from_files(role=role, subject=subject)

    def fetch_page(self, page_id: str, role: str = "viewer", subject: str | None = None) -> dict[str, object] | None:
        if self.mode == "db" and self.db_settings:
            return fetch_page_from_db(self.db_settings, page_id, role=role, subject=subject)
        return enrich_page_from_files(page_id, role=role, subject=subject)

    def role_from_token(self, token: str | None) -> str:
        if self.auth_settings:
            return self.auth_settings.resolve_role_for_token(token)
        return "viewer"

    def auth(self) -> AuthSettings:
        return self.auth_settings or load_auth_settings()


def resolve_repository(db_mode: str) -> RepositoryState:
    auth_settings = load_auth_settings()
    if db_mode == "file":
        return RepositoryState(mode="file", auth_settings=auth_settings)
    settings = load_database_settings()
    if not settings:
        if db_mode == "required":
            raise RuntimeError("DB mode được yêu cầu nhưng chưa có DATABASE_URL hoặc POSTGRES_*.")
        return RepositoryState(mode="file", auth_settings=auth_settings)
    return RepositoryState(mode="db", db_settings=settings, auth_settings=auth_settings)


class WikiRequestHandler(SimpleHTTPRequestHandler):
    repository = RepositoryState(mode="file")

    def _cors_origin(self) -> str:
        return os.getenv("WIKI_CORS_ORIGIN", "*")

    def _send_cors_headers(self) -> None:
        origin = self._cors_origin()
        self.send_header("Access-Control-Allow-Origin", origin)
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, X-Wiki-Token")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Credentials", "true")

    def do_OPTIONS(self) -> None:
        self.send_response(204)
        self._send_cors_headers()
        self.end_headers()

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, directory=str(PROJECT_ROOT), **kwargs)

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/api/bootstrap":
            self._handle_bootstrap(parsed); return
        if parsed.path == "/api/page":
            self._handle_page(parsed); return
        if parsed.path == "/api/session":
            self._handle_session(parsed); return
        if parsed.path == "/api/me":
            self._handle_me(parsed); return
        if parsed.path == "/api/search":
            self._handle_search(parsed); return
        if parsed.path == "/api/chat":
            self._handle_chat(parsed); return
        if parsed.path == "/api/quiz-pack":
            self._handle_quiz_pack(parsed); return
        if parsed.path == "/api/upload":
            self._handle_upload(parsed); return
        if parsed.path == "/api/duplicate-check":
            self._handle_duplicate_check(parsed); return
        if parsed.path == "/api/wiki-pages":
            self._handle_wiki_pages(parsed); return
        if parsed.path == "/api/upload-artifacts":
            self._handle_upload_artifacts(parsed); return
        if parsed.path == "/api/tutor":
            self._handle_tutor(parsed); return
        if parsed.path == "/api/tutor-history":
            self._handle_tutor_history(parsed); return
        if parsed.path == "/":
            self.path = "/wiki-viewer.html"
        super().do_GET()

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/api/login":
            self._handle_login(); return
        if parsed.path == "/api/logout":
            self._handle_logout(); return
        if parsed.path == "/api/chat":
            self._handle_chat(parsed); return
        if parsed.path == "/api/tutor":
            self._handle_tutor(parsed); return
        if parsed.path == "/api/upload-artifacts":
            self._handle_upload_artifacts(parsed); return
        if parsed.path == "/api/wiki-pages":
            self._handle_wiki_pages(parsed); return
        self.send_error(404, "Not Found")

    def _token_from_request(self, parsed) -> str:
        query = parse_qs(parsed.query)
        token = query.get("token", [""])[0]
        if not token:
            token = self.headers.get("X-Wiki-Token", "")
        auth_header = self.headers.get("Authorization", "")
        if auth_header.lower().startswith("bearer ") and not token:
            token = auth_header.split(" ", 1)[1].strip()
        return token

    def _role_and_subject(self, parsed) -> tuple[str, str | None]:
        token = self._token_from_request(parsed)
        if not token:
            return self.repository.role_from_token(None), None
        if token.count(".") == 2:
            secret = os.getenv("WIKI_JWT_SECRET", "replace-this-with-a-long-random-secret")
            try:
                payload = jwt.decode(token, secret, algorithms=["HS256"])
                return str(payload.get("role") or "viewer").strip().lower() or "viewer", str(payload.get("sub") or "") or None
            except Exception:
                return "viewer", None
        return self.repository.role_from_token(token), None

    def _read_json_body(self) -> dict[str, object]:
        length = int(self.headers.get("Content-Length", "0") or "0")
        if length <= 0:
            return {}
        raw = self.rfile.read(length)
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            return {}
        try:
            payload = json.loads(text) if text else {}
        except json.JSONDecodeError:
            return {}
        return payload if isinstance(payload, dict) else {}

    def _read_multipart_body(self) -> tuple[dict[str, str], bytes | None, str]:
        ctype = self.headers.get('Content-Type', '')
        if not ctype.startswith('multipart/form-data'):
            return {}, None, ''
        boundary = None
        for part in ctype.split(';'):
            part = part.strip()
            if part.startswith('boundary='):
                boundary = part.split('=', 1)[1].strip('"')
                break
        length = int(self.headers.get('Content-Length', '0') or '0')
        raw = self.rfile.read(length) if length > 0 else b''
        fields: dict[str, str] = {}
        file_bytes: bytes | None = None
        filename = ''
        if not boundary:
            return fields, file_bytes, filename
        delimiter = ('--' + boundary).encode('utf-8')
        for chunk in raw.split(delimiter):
            chunk = chunk.strip(b'\r\n')
            if not chunk or chunk == b'--':
                continue
            headers_blob, _, body = chunk.partition(b'\r\n\r\n')
            headers_text = headers_blob.decode('utf-8', errors='ignore')
            if 'name="' not in headers_text:
                continue
            name = headers_text.split('name="', 1)[1].split('"', 1)[0]
            if 'filename="' in headers_text:
                filename = headers_text.split('filename="', 1)[1].split('"', 1)[0]
                file_bytes = body.rstrip(b'\r\n')
            else:
                fields[name] = body.decode('utf-8', errors='ignore').rstrip('\r\n')
        return fields, file_bytes, filename

    def _session_claims(self, role: str, subject: str) -> dict[str, object]:
        ttl = int(os.getenv("WIKI_SESSION_TTL_SECONDS", "86400") or "86400")
        now = int(time.time())
        return {"sub": subject, "role": role, "iat": now, "exp": now + ttl}

    def _sign_token(self, role: str, subject: str) -> tuple[str, str, int]:
        secret = os.getenv("WIKI_JWT_SECRET", "replace-this-with-a-long-random-secret")
        claims = self._session_claims(role, subject)
        token = jwt.encode(claims, secret, algorithm="HS256")
        session_id = f"{subject}:{claims['iat']}"
        return session_id, token, int(claims["exp"])

    def _persist_session(self, session_id: str, role: str, token: str, expires_at: int) -> None:
        if not self.repository.db_settings:
            return
        try:
            with open_db_connection(self.repository.db_settings) as connection:
                set_search_path(connection, self.repository.db_settings)
                with connection.transaction():
                    connection.execute(
                        """
                        INSERT INTO session_tokens (session_id, role, token_hash, expires_at)
                        VALUES (%s, %s, %s, %s)
                        ON CONFLICT (session_id) DO UPDATE SET
                            role = EXCLUDED.role,
                            token_hash = EXCLUDED.token_hash,
                            expires_at = EXCLUDED.expires_at,
                            last_seen_at = CURRENT_TIMESTAMP::text,
                            revoked_at = NULL
                        """,
                        (session_id, role, hashlib.sha256(token.encode("utf-8")).hexdigest(), time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(expires_at))),
                    )
        except Exception:
            return

    def _log_tutor_activity(self, question: str, role: str, subject: str | None, payload: dict[str, object]) -> None:
        if not self.repository.db_settings:
            return
        try:
            page_ids = [c.get("id") for c in payload.get("citations", []) if isinstance(c, dict)]
            session_key = str(payload.get("sessionKey") or f"{role}:{subject or 'anonymous'}")
            topic = str(payload.get("topic") or (payload.get("contextPages", [{}])[0].get("topic") if payload.get("contextPages") else "general"))
            details = {
                "question": question,
                "role": role,
                "subject": subject,
                "confidence": payload.get("confidence"),
                "page_ids": page_ids,
                "followUps": payload.get("followUps", []),
                "quiz": payload.get("quiz", []),
                "topic": topic,
            }
            with open_db_connection(self.repository.db_settings) as connection:
                set_search_path(connection, self.repository.db_settings)
                with connection.transaction():
                    connection.execute(
                        """
                        INSERT INTO chat_sessions (session_key, role, subject, created_at, last_message_at, summary_json)
                        VALUES (%s, %s, %s, CURRENT_TIMESTAMP::text, CURRENT_TIMESTAMP::text, %s)
                        ON CONFLICT (session_key) DO UPDATE SET
                            last_message_at = EXCLUDED.last_message_at,
                            summary_json = EXCLUDED.summary_json
                        """,
                        (session_key, role, subject, json.dumps({"latestQuestion": question, "topic": topic}, ensure_ascii=False)),
                    )
                    connection.execute(
                        """
                        INSERT INTO chat_messages (session_key, message_role, content, citations_json, created_at)
                        VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP::text)
                        """,
                        (session_key, "user", question, "[]"),
                    )
                    connection.execute(
                        """
                        INSERT INTO chat_messages (session_key, message_role, content, citations_json, created_at)
                        VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP::text)
                        """,
                        (session_key, "assistant", str(payload.get("answer") or ""), json.dumps(payload.get("citations", []), ensure_ascii=False)),
                    )
                    connection.execute(
                        """
                        INSERT INTO tutor_progress (subject_key, role, topic, last_question, last_answer, confidence, updated_at)
                        VALUES (%s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP::text)
                        ON CONFLICT (subject_key, topic) DO UPDATE SET
                            last_question = EXCLUDED.last_question,
                            last_answer = EXCLUDED.last_answer,
                            confidence = EXCLUDED.confidence,
                            updated_at = EXCLUDED.updated_at
                        """,
                        (
                            subject or role,
                            role,
                            topic,
                            question,
                            str(payload.get("answer") or ""),
                            str(payload.get("confidence") or "low"),
                        ),
                    )
                    connection.execute(
                        """
                        INSERT INTO quiz_attempts (subject_key, role, question, quiz_json, created_at)
                        VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP::text)
                        """,
                        (subject or role, role, question, json.dumps(payload.get("quiz", []), ensure_ascii=False)),
                    )
                    connection.execute(
                        """
                        INSERT INTO runtime_activity_log (event_type, entity_type, entity_id, details_json)
                        VALUES (%s, %s, %s, %s)
                        """,
                        ("tutor_answer", "chat", session_key, json.dumps(details, ensure_ascii=False)),
                    )
        except Exception:
            return

    def _format_tutor_summary(self, payload: dict[str, object], role: str) -> dict[str, object]:
        primary = payload.get("primarySource") or {}
        question = str(payload.get("question") or "")
        answer_source = str(payload.get("answerSource") or "local-db")
        matched_by = str(payload.get("matchedBy") or "db")
        matched_count = int(payload.get("matchedCount") or 0)
        top_result = {
            "id": primary.get("id"),
            "title": primary.get("title"),
            "path": primary.get("path"),
            "topic": primary.get("topic"),
            "section": primary.get("section"),
            "visibility": primary.get("visibility", "public"),
            "excerpt": primary.get("excerpt", ""),
        } if isinstance(primary, dict) else None
        return {
            "answer": "",
            "answerSource": answer_source,
            "matchedBy": matched_by,
            "matchedCount": matched_count,
            "primarySource": top_result,
            "alternatives": [
                {
                    "id": item.get("id"),
                    "title": item.get("title"),
                    "path": item.get("path"),
                    "topic": item.get("topic"),
                    "section": item.get("section"),
                    "visibility": item.get("visibility", "public"),
                    "excerpt": item.get("excerpt", ""),
                }
                for item in (payload.get("alternatives") or [])[:4]
                if isinstance(item, dict)
            ],
            "followUps": payload.get("followUps", []),
            "quiz": payload.get("quiz", []),
            "confidence": payload.get("confidence", "low"),
            "topic": payload.get("topic", "general"),
            "sessionKey": payload.get("sessionKey"),
            "role": role,
            "question": question,
        }

    def _handle_session(self, parsed) -> None:
        role, subject = self._role_and_subject(parsed)
        self.respond_json({"role": role, "subject": subject})

    def _handle_me(self, parsed) -> None:
        role, subject = self._role_and_subject(parsed)
        self.respond_json({"role": role, "subject": subject})

    def _handle_login(self) -> None:
        body = self._read_json_body()
        role = str(body.get("role") or "viewer").strip().lower()
        password = str(body.get("password") or "").strip()
        subject = str(body.get("subject") or role)
        if role == "viewer":
            session_id, token, expires_at = self._sign_token(role, subject)
            self._persist_session(session_id, role, token, expires_at)
            self.respond_json({"role": role, "token": token, "session_id": session_id, "expires_in": int(os.getenv("WIKI_SESSION_TTL_SECONDS", "86400") or "86400")})
            return
        if role not in {"editor", "admin"}:
            self.respond_json({"error": "Unsupported role"}, status=400)
            return
        if not self.repository.db_settings:
            self.respond_json({"error": "Database auth is not configured"}, status=500)
            return
        account = authenticate_db_account(self.repository.db_settings, role, password)
        if not account:
            self.respond_json({"error": "Invalid credentials"}, status=401)
            return
        subject = str(account.get("username") or subject)
        session_id, token, expires_at = self._sign_token(role, subject)
        self._persist_session(session_id, role, token, expires_at)
        self.respond_json({"role": role, "token": token, "session_id": session_id, "expires_in": int(os.getenv("WIKI_SESSION_TTL_SECONDS", "86400") or "86400")})

    def _handle_logout(self) -> None:
        self.respond_json({"ok": True})

    def _handle_bootstrap(self, parsed) -> None:
        try:
            role, subject = self._role_and_subject(parsed)
            self.respond_json(self.repository.build_bootstrap(role=role, subject=subject))
        except Exception as exc:
            self.respond_json({"error": f"Không thể build bootstrap: {exc}"}, status=500)

    def _handle_page(self, parsed) -> None:
        query = parse_qs(parsed.query)
        page_id = query.get("id", [""])[0]
        if not page_id:
            self.respond_json({"error": "Missing page id."}, status=400)
            return
        role, subject = self._role_and_subject(parsed)
        try:
            page = self.repository.fetch_page(page_id, role=role, subject=subject)
        except Exception as exc:
            self.respond_json({"error": f"Không thể đọc page: {exc}"}, status=500)
            return
        if not page:
            self.respond_json({"error": f"Page not found or access denied: {page_id}"}, status=404)
            return
        self.respond_json(page)

    def _handle_search(self, parsed) -> None:
        query = parse_qs(parsed.query)
        q = query.get("q", [""])[0]
        role, subject = self._role_and_subject(parsed)
        limit = int(query.get("limit", ["10"])[0])
        if self.repository.mode == "db" and self.repository.db_settings:
            results = search_pages_in_db(self.repository.db_settings, q, role=role, subject=subject, limit=limit)
        else:
            results = search_pages(q, scan_pages(), role=role, subject=subject, limit=limit)
        self.respond_json({"query": q, "role": role, "results": results})

    def _handle_chat(self, parsed) -> None:
        query = parse_qs(parsed.query)
        body = self._read_json_body()
        question = str(body.get("question") or query.get("q", [""])[0])
        role, subject = self._role_and_subject(parsed)
        pages = scan_pages() if self.repository.mode == "file" else []
        if self.repository.mode == "db" and self.repository.db_settings:
            bootstrap = build_bootstrap_from_db(self.repository.db_settings, role=role, subject=subject)
            pages = bootstrap.get("pages", [])  # type: ignore[assignment]
        answer = build_chat_answer(question, pages, role=role, subject=subject)
        self.respond_json(answer)

    def _handle_quiz_pack(self, parsed) -> None:
        body = self._read_json_body()
        query = parse_qs(parsed.query)
        question = str(body.get("query") or query.get("q", [""])[0]).strip()
        role, subject = self._role_and_subject(parsed)
        pages = scan_pages() if self.repository.mode == "file" else []
        if self.repository.mode == "db" and self.repository.db_settings:
            bootstrap = build_bootstrap_from_db(self.repository.db_settings, role=role, subject=subject)
            pages = bootstrap.get("pages", [])  # type: ignore[assignment]
        self.respond_json(build_quiz_pack_from_pages(question, pages, role=role, subject=subject))

    def _handle_duplicate_check(self, parsed) -> None:
        body = self._read_json_body()
        query = parse_qs(parsed.query)
        text = str(body.get("content") or body.get("query") or query.get("q", [""])[0]).strip()
        role, subject = self._role_and_subject(parsed)
        pages = scan_pages() if self.repository.mode == "file" else []
        if self.repository.mode == "db" and self.repository.db_settings:
            bootstrap = build_bootstrap_from_db(self.repository.db_settings, role=role, subject=subject)
            pages = bootstrap.get("pages", [])  # type: ignore[assignment]
        self.respond_json(duplicate_check_payload(text, pages))

    def _handle_upload(self, parsed) -> None:
        body = self._read_json_body()
        role, subject = self._role_and_subject(parsed)
        filename = str(body.get("filename") or "upload.txt")
        title = str(body.get("title") or filename.rsplit(".", 1)[0])
        topic = str(body.get("topic") or "general")
        content_text = str(body.get("content") or body.get("text") or "")
        if not content_text.strip():
            self.respond_json({"error": "Missing upload content"}, status=400)
            return
        pages = scan_pages() if self.repository.mode == "file" else []
        if self.repository.mode == "db" and self.repository.db_settings:
            bootstrap = build_bootstrap_from_db(self.repository.db_settings, role=role, subject=subject)
            pages = bootstrap.get("pages", [])  # type: ignore[assignment]
        duplicate = duplicate_check_payload(content_text, pages)
        payload = {
            "uploadId": hashlib.sha256(f"{filename}:{time.time()}".encode("utf-8")).hexdigest()[:16],
            "status": "received",
            "filename": filename,
            "title": title,
            "topic": topic,
            "duplicateCheck": duplicate,
            "contentHash": duplicate.get("contentHash"),
            "contentText": content_text,
        }
        self.respond_json(payload)

    def _handle_upload_artifacts(self, parsed) -> None:
        role, subject = self._role_and_subject(parsed)
        if role != 'editor':
            self.respond_json({"error": "Upload artifacts require editor role"}, status=403)
            return
        if not self.repository.db_settings:
            self.respond_json({"error": "Database is not configured"}, status=500)
            return
        fields: dict[str, str] = {}
        file_bytes: bytes | None = None
        filename = ''
        ctype = self.headers.get('Content-Type', '')
        if ctype.startswith('multipart/form-data'):
            fields, file_bytes, filename = self._read_multipart_body()
        else:
            body = self._read_json_body()
            fields = {k: str(v) for k, v in body.items()}
            file_bytes = None
        if file_bytes is None:
            self.respond_json({"error": "Missing file upload"}, status=400)
            return
        upload_name = filename or fields.get('filename') or 'upload.bin'
        extracted = extract_text_from_upload(upload_name, file_bytes)
        title = fields.get('title') or Path(upload_name).stem
        topic = fields.get('topic') or 'general'
        tags = [t.strip() for t in (fields.get('tags') or '').split(',') if t.strip()]
        pages = scan_pages() if self.repository.mode == 'file' else []
        if self.repository.mode == 'db' and self.repository.db_settings:
            bootstrap = build_bootstrap_from_db(self.repository.db_settings, role=role, subject=subject)
            pages = bootstrap.get('pages', [])  # type: ignore[assignment]
        duplicate = duplicate_check_payload(extracted, pages)
        artifact_hash = hashlib.sha256(file_bytes).hexdigest()
        draft = build_draft_from_text(title=title, topic=topic, content_text=extracted[:12000], tags=tags)
        storage_result = upload_to_supabase_storage(filename=f"{artifact_hash}/{upload_name}", data=file_bytes or b'', content_type=self.headers.get('Content-Type', 'application/octet-stream'))
        stored = {
            'uploadId': hashlib.sha256(f"{upload_name}:{time.time()}".encode('utf-8')).hexdigest()[:16],
            'filename': upload_name,
            'title': title,
            'topic': topic,
            'contentHash': artifact_hash,
            'duplicateCheck': duplicate,
            'draft': draft,
            'contentText': extracted,
            'storagePath': storage_result.storage_path if storage_result else f'uploads/{artifact_hash}/{upload_name}',
            'public_url': storage_result.public_url if storage_result else None,
            'signed_url': storage_result.signed_url if storage_result else None,
            'publicUrl': storage_result.public_url if storage_result else None,
            'signedUrl': storage_result.signed_url if storage_result else None,
        }
        with open_db_connection(self.repository.db_settings) as connection:
            set_search_path(connection, self.repository.db_settings)
            with connection.transaction():
                artifact_row = connection.execute(
                    """
                    INSERT INTO upload_artifacts (uploaded_by, filename, title, topic, content_text, content_hash, duplicate_json, status)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id
                    """,
                    (subject or role, upload_name, title, topic, extracted, artifact_hash, json.dumps(duplicate, ensure_ascii=False), 'received'),
                ).fetchone()
                artifact_id = int(artifact_row['id']) if artifact_row else None
                draft_page = f"drafts/{artifact_hash[:12]}"
                draft_payload = json.dumps({**draft, 'storagePath': stored['storagePath'], 'publicUrl': stored['publicUrl'], 'signedUrl': stored['signedUrl']}, ensure_ascii=False)
                connection.execute(
                    """
                    INSERT INTO wiki_drafts (uploaded_artifact_id, page_id, title, topic, section, visibility, content_hash, draft_json, status)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (page_id) DO UPDATE SET
                        title = EXCLUDED.title,
                        topic = EXCLUDED.topic,
                        section = EXCLUDED.section,
                        visibility = EXCLUDED.visibility,
                        content_hash = EXCLUDED.content_hash,
                        draft_json = EXCLUDED.draft_json,
                        status = EXCLUDED.status,
                        updated_at = CURRENT_TIMESTAMP
                    """,
                    (artifact_id, draft_page, title, topic, 'syntheses', 'internal', artifact_hash, draft_payload, 'draft'),
                )
        self.respond_json(stored)

    def _handle_wiki_pages(self, parsed) -> None:
        body = self._read_json_body()
        role, subject = self._role_and_subject(parsed)
        title = str(body.get("title") or "Untitled").strip()
        topic = str(body.get("topic") or "general").strip()
        section = str(body.get("section") or "syntheses").strip()
        visibility = str(body.get("visibility") or "internal").strip()
        content = str(body.get("content") or "").strip()
        tags = [t.strip() for t in str(body.get("tags") or "").split(",") if t.strip()]
        if not title or not content:
            self.respond_json({"error": "title and content are required"}, status=400)
            return
        page_id = str(body.get("pageId") or hashlib.sha256(f"{title}:{content}".encode("utf-8")).hexdigest()[:16])
        slug = slugify(title)
        excerpt = content[:280].strip()
        word_count = len(content.split())
        heading_rows = []
        headings_json = json.dumps([], ensure_ascii=False)
        created_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        with open_db_connection(self.repository.db_settings) as connection:
            set_search_path(connection, self.repository.db_settings)
            with connection.transaction():
                connection.execute(
                    """
                    INSERT INTO pages (id, slug, title, topic, section, path, created, updated, confidence, visibility, excerpt, body, word_count, headings_json)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO UPDATE SET
                        slug = EXCLUDED.slug,
                        title = EXCLUDED.title,
                        topic = EXCLUDED.topic,
                        section = EXCLUDED.section,
                        path = EXCLUDED.path,
                        updated = EXCLUDED.updated,
                        confidence = EXCLUDED.confidence,
                        visibility = EXCLUDED.visibility,
                        excerpt = EXCLUDED.excerpt,
                        body = EXCLUDED.body,
                        word_count = EXCLUDED.word_count,
                        headings_json = EXCLUDED.headings_json
                    """,
                    (page_id, slug, title, topic, section, f"{section}/{slug}", created_at, created_at, "draft", visibility, excerpt, content, word_count, headings_json),
                )
                connection.execute("DELETE FROM page_tags WHERE page_id = %s", (page_id,))
                for idx, tag in enumerate(tags):
                    connection.execute(
                        "INSERT INTO page_tags (page_id, tag, position) VALUES (%s, %s, %s)",
                        (page_id, tag, idx),
                    )
                connection.execute("DELETE FROM page_sources WHERE page_id = %s", (page_id,))
                for idx, source in enumerate([f"upload:{page_id}"]):
                    connection.execute(
                        "INSERT INTO page_sources (page_id, source, position) VALUES (%s, %s, %s)",
                        (page_id, source, idx),
                    )
        result = {
            "pageId": page_id,
            "status": "created",
            "title": title,
            "topic": topic,
            "section": section,
            "visibility": visibility,
            "createdBy": subject or role,
        }
        self.respond_json(result)

    def _handle_tutor(self, parsed) -> None:
        query = parse_qs(parsed.query)
        body = self._read_json_body()
        question = str(body.get("question") or query.get("q", [""])[0])
        role, subject = self._role_and_subject(parsed)
        pages = scan_pages() if self.repository.mode == "file" else []
        if self.repository.mode == "db" and self.repository.db_settings:
            bootstrap = build_bootstrap_from_db(self.repository.db_settings, role=role, subject=subject)
            pages = bootstrap.get("pages", [])  # type: ignore[assignment]
        payload = build_tutor_reply(question, pages, role=role, subject=subject)
        summary = self._format_tutor_summary(payload, role)
        self._log_tutor_activity(question, role, subject, summary)
        self.respond_json(summary)

    def _handle_tutor_history(self, parsed) -> None:
        role, subject = self._role_and_subject(parsed)
        query = parse_qs(parsed.query)
        q = str(query.get("q", [""])[0]).strip().lower()
        limit = int(query.get("limit", ["20"])[0])
        if not self.repository.db_settings:
            self.respond_json({"items": [], "role": role, "subject": subject, "mode": "file"})
            return
        try:
            with open_db_connection(self.repository.db_settings) as connection:
                set_search_path(connection, self.repository.db_settings)
                sessions = list(connection.execute(
                    """
                    SELECT session_key, role, subject, created_at, last_message_at, summary_json
                    FROM chat_sessions
                    ORDER BY last_message_at DESC
                    LIMIT %s
                    """,
                    (limit,),
                ))
                progress_rows = list(connection.execute(
                    """
                    SELECT subject_key, role, topic, last_question, last_answer, confidence, updated_at
                    FROM tutor_progress
                    ORDER BY updated_at DESC
                    LIMIT %s
                    """,
                    (limit,),
                ))
                quiz_rows = list(connection.execute(
                    """
                    SELECT subject_key, role, question, quiz_json, created_at
                    FROM quiz_attempts
                    ORDER BY created_at DESC
                    LIMIT %s
                    """,
                    (limit,),
                ))
                messages = list(connection.execute(
                    """
                    SELECT session_key, message_role, content, citations_json, created_at
                    FROM chat_messages
                    ORDER BY created_at DESC
                    LIMIT %s
                    """,
                    (limit * 2,),
                ))
        except Exception as exc:
            self.respond_json({"error": f"Không thể đọc lịch sử tutor: {exc}"}, status=500)
            return
        items = []
        for row in sessions:
            summary = json.loads(row["summary_json"] or "{}")
            combined = " ".join([str(row["session_key"]), str(row["role"]), str(row["subject"] or ""), str(summary.get("latestQuestion") or ""), str(summary.get("topic") or "")]).lower()
            if q and q not in combined:
                continue
            items.append(
                {
                    "session_key": row["session_key"],
                    "role": row["role"],
                    "subject": row["subject"],
                    "created_at": row["created_at"],
                    "last_message_at": row["last_message_at"],
                    "summary": summary,
                }
            )
        progress = [
            {
                "subject_key": row["subject_key"],
                "role": row["role"],
                "topic": row["topic"],
                "last_question": row["last_question"],
                "last_answer": row["last_answer"],
                "confidence": row["confidence"],
                "updated_at": row["updated_at"],
            }
            for row in progress_rows
        ]
        quiz = [
            {
                "subject_key": row["subject_key"],
                "role": row["role"],
                "question": row["question"],
                "quiz": json.loads(row["quiz_json"] or "[]"),
                "created_at": row["created_at"],
            }
            for row in quiz_rows
        ]
        recent_messages = [
            {
                "session_key": row["session_key"],
                "message_role": row["message_role"],
                "content": row["content"],
                "citations": json.loads(row["citations_json"] or "[]"),
                "created_at": row["created_at"],
            }
            for row in messages
        ]
        self.respond_json({"items": items, "progress": progress, "quizAttempts": quiz, "messages": recent_messages, "role": role, "subject": subject, "mode": "db"})

    def respond_json(self, payload: dict[str, object], status: int = 200) -> None:
        body = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status)
        self._send_cors_headers()
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args) -> None:
        sys.stdout.write("%s - - [%s] %s\n" % (self.address_string(), self.log_date_time_string(), format % args))


def main() -> int:
    parser = argparse.ArgumentParser(description="Serve the AI Coding Wiki viewer with file mode or PostgreSQL-backed runtime data.")
    parser.add_argument("--host", default=os.getenv("HOST", "0.0.0.0"), help="Host to bind.")
    parser.add_argument("--port", type=int, default=int(os.getenv("PORT", "8008")), help="Port to bind.")
    parser.add_argument("--db-mode", choices=("auto", "file", "required"), default="auto", help="auto: dùng PostgreSQL nếu có cấu hình, file: luôn đọc markdown, required: bắt buộc PostgreSQL.")
    parser.add_argument("--dump-bootstrap", action="store_true", help="Print bootstrap JSON once and exit.")
    args = parser.parse_args()
    repository = resolve_repository(args.db_mode)
    if args.dump_bootstrap:
        token = os.getenv("WIKI_API_TOKEN", "")
        role, subject = repository.role_from_token(token), None
        payload = json.dumps(repository.build_bootstrap(role=role, subject=subject), ensure_ascii=False, indent=2) + "\n"
        sys.stdout.buffer.write(payload.encode("utf-8"))
        return 0
    WikiRequestHandler.repository = repository
    server = ThreadingHTTPServer((args.host, args.port), partial(WikiRequestHandler))
    mode_label = f"db:{repository.db_settings.schema}" if repository.mode == "db" and repository.db_settings else "file"
    print(f"AI Coding Wiki dynamic viewer running at http://{args.host}:{args.port} [{mode_label}]", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down viewer...", flush=True)
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
