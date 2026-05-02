from __future__ import annotations

import json
from typing import Any

from wiki_runtime import content_hash_for_text, duplicate_candidates_for_text, open_db_connection, scan_pages, set_search_path


def build_quiz_pack_from_pages(query: str, pages: list[dict[str, Any]], role: str, subject: str | None = None, limit: int = 4) -> dict[str, Any]:
    visible_pages = pages
    candidates = duplicate_candidates_for_text(query, visible_pages, limit=limit)
    primary = candidates[0] if candidates else None
    secondary = candidates[1:]
    quiz = []
    if primary:
        quiz = [
            {"type": "short_answer", "question": f"{primary['title']} đang giải quyết vấn đề gì?"},
            {"type": "compare", "question": f"So sánh ý chính của {primary['title']} với một giải pháp khác mà bạn biết."},
        ]
    return {
        "query": query,
        "topic": primary.get("topic") if primary else "general",
        "primarySource": primary,
        "secondaryResults": secondary,
        "quiz": quiz,
        "followUps": [
            "Bạn có muốn mở tài liệu liên quan không?",
            "Bạn có muốn tạo page mới từ nội dung này không?",
        ],
        "sourceMode": "local-db",
        "matchedBy": "db" if candidates else "none",
        "matchedCount": len(candidates),
        "sessionKey": f"quiz:{role}:{subject or 'anonymous'}",
    }


def duplicate_check_payload(query: str, pages: list[dict[str, Any]], limit: int = 5) -> dict[str, Any]:
    matches = duplicate_candidates_for_text(query, pages, limit=limit)
    return {
        "isDuplicate": bool(matches and matches[0].get("score", 0) >= 40),
        "matches": matches,
        "contentHash": content_hash_for_text(query),
    }


def list_public_pages(settings) -> list[dict[str, Any]]:
    from wiki_runtime import build_bootstrap_from_db
    bootstrap = build_bootstrap_from_db(settings, role="viewer")
    return bootstrap.get("pages", [])
