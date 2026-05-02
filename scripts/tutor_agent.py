from __future__ import annotations

import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from hashlib import sha256
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from wiki_runtime import build_chat_answer, search_pages


STOPWORDS = {
    "là", "la", "của", "cua", "và", "va", "the", "thi", "trong", "tren", "cho", "một", "mot", "những", "nhung", "này", "nay", "đó", "do", "khi", "nao", "nào", "vì", "vi", "sẽ", "se", "có", "co", "không", "khong", "nội", "noi", "dùng", "dung", "api", "local", "db", "database", "context", "db?"
}


@dataclass(frozen=True)
class TutorMessage:
    role: str
    content: str
    created_at: str


SYSTEM_INSTRUCTIONS = """Bạn là Tutor Agent cho AI Coding Wiki.
Nhiệm vụ:
- Dạy người dùng theo kiểu dễ hiểu, theo từng bước.
- Ưu tiên wiki nội bộ làm nguồn chính.
- Hỏi lại nếu câu hỏi mơ hồ hoặc thiếu ngữ cảnh.
- Trả lời ngắn gọn trước, rồi mới mở rộng nếu cần.
- Luôn đưa citations khi có nguồn wiki phù hợp.
- Nếu không có đủ nguồn, nói rõ giới hạn thay vì bịa.
"""


GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"


def groq_enabled() -> bool:
    return bool(os.getenv("GROQ_API_KEY", "").strip())


def call_groq_chat(messages: list[dict[str, str]], model: str | None = None, temperature: float = 0.2) -> str:
    api_key = os.getenv("GROQ_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("GROQ_API_KEY chưa được cấu hình.")
    payload = {
        "model": model or os.getenv("GROQ_MODEL", "llama-3.1-70b-versatile"),
        "messages": messages,
        "temperature": temperature,
    }
    request = Request(
        GROQ_API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urlopen(request, timeout=60) as response:
            data = json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError) as exc:
        raise RuntimeError(f"Gọi Groq API thất bại: {exc}") from exc
    choices = data.get("choices") or []
    if not choices:
        raise RuntimeError("Groq API không trả về choices.")
    message = choices[0].get("message") or {}
    content = message.get("content") or ""
    return str(content).strip()


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def make_session_id(subject: str, question: str) -> str:
    digest = sha256(f"{subject}:{question}:{now_iso()}".encode("utf-8")).hexdigest()[:24]
    return f"tutor-{digest}"


def normalize_query(text: str) -> list[str]:
    cleaned = " ".join(str(text or "").lower().split())
    cleaned = cleaned.replace("?", " ").replace(",", " ").replace(".", " ").replace(":", " ")
    tokens = []
    for token in cleaned.split():
        token = token.strip()
        if not token or token in STOPWORDS or len(token) <= 2:
            continue
        tokens.append(token)
    return tokens


def score_page(question: str, page: dict[str, Any], tokens: list[str]) -> int:
    haystack = " ".join([
        str(page.get("title", "")),
        str(page.get("topic", "")),
        str(page.get("section", "")),
        str(page.get("excerpt", "")),
        str(page.get("body", ""))[:4000],
        " ".join(map(str, page.get("tags", []))),
        " ".join(map(str, page.get("headings", []))),
        " ".join(map(str, page.get("sources", []))),
    ]).lower()
    score = 0
    for token in tokens:
        if token in haystack:
            score += 4
        if token in str(page.get("title", "")).lower():
            score += 5
        if token in str(page.get("topic", "")).lower():
            score += 3
        if token in str(page.get("section", "")).lower():
            score += 2
    if question.lower() in haystack:
        score += 15
    if str(page.get("excerpt", "")).lower() in question.lower():
        score += 6
    return score


def _can_access_visibility(role: str, visibility: str) -> bool:
    visibility = str(visibility or "public").strip().lower()
    if visibility == "public":
        return True
    if role == "admin":
        return True
    if role == "editor":
        return visibility != "private"
    return False


def build_tutor_context(question: str, pages: list[dict[str, Any]], role: str, subject: str | None = None, limit: int = 8) -> dict[str, Any]:
    tokens = normalize_query(question)
    answer_payload = build_chat_answer(question, pages, role=role, subject=subject, limit=limit)
    candidate_pages: list[dict[str, Any]] = []
    for page in pages:
        if str(page.get("visibility", "public")) not in {"public", "internal", "restricted", "private"}:
            continue
        if not _can_access_visibility(role, str(page.get("visibility", "public"))):
            continue
        candidate_pages.append(page)
    scored = []
    for page in candidate_pages:
        scored.append((score_page(question, page, tokens), page))
    scored.sort(key=lambda item: (-item[0], str(item[1].get("title", "")).lower()))
    top_pages = [page for score, page in scored if score > 0][:limit]
    if not top_pages:
        top_pages = search_pages(question, pages, role=role, subject=subject, limit=limit)
    context_pages = []
    for page in top_pages:
        context_pages.append(
            {
                "id": page["id"],
                "title": page["title"],
                "topic": page.get("topic"),
                "section": page.get("section"),
                "excerpt": page.get("excerpt"),
                "path": page.get("path"),
                "visibility": page.get("visibility", "public"),
                "tags": page.get("tags", []),
                "headings": page.get("headings", []),
                "sources": page.get("sources", []),
                "relatedSlugs": page.get("relatedSlugs", []),
            }
        )
    return {
        "system": SYSTEM_INSTRUCTIONS,
        "question": question,
        "query_tokens": tokens,
        "context_pages": context_pages,
        "answer_payload": answer_payload,
        "candidateCount": len(candidate_pages),
    }


def _is_public_role(role: str) -> bool:
    return str(role or "viewer").strip().lower() == "viewer"


def _safe_public_answer(question: str, primary_source: dict[str, Any] | None, alternatives: list[dict[str, Any]], matched_by: str, matched_count: int) -> str:
    if primary_source:
        visibility = str(primary_source.get("visibility") or "public").lower()
        if visibility == "public":
            return "Tôi đã tìm thấy tài liệu phù hợp, nhưng ở chế độ công khai chỉ hiển thị tiêu đề và gợi ý mở trang chi tiết sau khi đăng nhập."
        return "Đây là tài liệu nội bộ. Hãy đăng nhập để xem chi tiết."
    if alternatives:
        return "Tôi đã tìm thấy một số tài liệu liên quan, nhưng nội dung chi tiết đang bị giới hạn theo quyền hiện tại."
    if matched_by == "token":
        return "Tôi nhận diện được từ khóa liên quan, nhưng chưa đủ ngữ cảnh để hiển thị chi tiết an toàn."
    return "Mình chưa tìm thấy tài liệu phù hợp trong phạm vi quyền hiện tại."


def build_tutor_reply(question: str, pages: list[dict[str, Any]], role: str, subject: str | None = None, limit: int = 5) -> dict[str, Any]:
    payload = build_tutor_context(question, pages, role=role, subject=subject, limit=limit)
    answer_payload = payload["answer_payload"]
    citations = answer_payload.get("citations", [])
    context_pages = payload["context_pages"]
    topic = (context_pages[0]["topic"] if context_pages else "general")
    query_tokens = payload.get("query_tokens", [])
    follow_ups = [
        "Bạn có muốn mình giải thích sâu hơn từng phần không?",
        "Bạn có muốn mình tạo thêm quiz ngắn để kiểm tra không?",
    ] if citations else ["Bạn có muốn mình tìm thêm tài liệu nội bộ liên quan không?"]
    quiz = []
    if citations:
        quiz = [
            {"question": "Điểm chính nào là quan trọng nhất trong nội dung vừa học?", "type": "short_answer"},
            {"question": "Tutor Agent nên làm gì khi câu hỏi còn mơ hồ?", "type": "short_answer"},
        ]

    raw_answer = str(answer_payload.get("answer") or "").strip()
    answer_source = "local"
    context_strength = "none"
    if context_pages:
        context_strength = "db"
    elif query_tokens:
        context_strength = "token"

    primary_source = None
    alternatives: list[dict[str, Any]] = []
    if context_pages:
        primary_source = context_pages[0]
        alternatives = context_pages[1:]

    is_public = _is_public_role(role)
    answer = raw_answer or "Mình chưa tìm thấy nguồn phù hợp để trả lời chính xác."

    if is_public:
        answer = _safe_public_answer(question, primary_source, alternatives, context_strength, len(context_pages))
    else:
        if groq_enabled():
            system = payload["system"]
            context_blocks = []
            for idx, page in enumerate(context_pages, start=1):
                context_blocks.append(
                    f"[{idx}] {page['title']} | section={page['section']} | topic={page['topic']} | visibility={page['visibility']}\n"
                    f"excerpt: {page.get('excerpt') or ''}\n"
                    f"tags: {', '.join(map(str, page.get('tags', [])))}\n"
                    f"headings: {', '.join(h.get('title', '') if isinstance(h, dict) else str(h) for h in page.get('headings', []))}\n"
                    f"sources: {', '.join(map(str, page.get('sources', [])))}\n"
                    f"related: {', '.join(map(str, page.get('relatedSlugs', [])))}\n"
                )
            prompt = [
                {
                    "role": "system",
                    "content": (
                        system
                        + "\n\nBạn phải ưu tiên các đoạn context được cung cấp bên dưới. Nếu context đủ thì không được trả lời 'không biết'."
                        + "\nNếu câu hỏi dài nhưng vẫn cùng chủ đề, hãy suy luận từ context gần đúng nhất và nêu citations cụ thể."
                        + "\nKết quả trả về phải ưu tiên câu trả lời đúng nhất lên trên cùng; các lựa chọn liên quan khác để sau."
                    ),
                },
                {
                    "role": "user",
                    "content": "\n".join([
                        "Hãy đóng vai tutor trả lời câu hỏi dựa trên tài liệu wiki và context DB bên dưới.",
                        f"Câu hỏi: {question}",
                        f"Query tokens: {', '.join(query_tokens) or '-'}",
                        f"Context strength: {context_strength}",
                        "",
                        "Tài liệu liên quan:",
                        *(context_blocks if context_blocks else ["- Không có context tương ứng, hãy trả lời ở mức tổng quát và nêu rõ thiếu dữ liệu"]),
                        "",
                        "Yêu cầu đầu ra:",
                        "- Trả lời chính xác nhất có thể",
                        "- Nếu có thể, liệt kê citations theo title/page",
                        "- Không được nói 'không có trong db' nếu context đã cho đủ thông tin",
                    ]),
                },
            ]
            try:
                groq_answer = call_groq_chat(prompt)
                if groq_answer:
                    answer = groq_answer
                    answer_source = "groq"
            except Exception:
                answer_source = "local"

        if answer_source != "groq":
            if context_strength == "db":
                answer_source = "local-db"
            elif context_strength == "token":
                answer_source = "local-token"
            else:
                answer_source = "local-none"

    if is_public and primary_source and str(primary_source.get("visibility") or "public").lower() != "public":
        answer_source = "local-public-redacted"

    return {
        "answer": answer,
        "citations": citations,
        "followUps": follow_ups,
        "quiz": quiz,
        "confidence": "medium" if citations else "low",
        "contextPages": context_pages,
        "topic": topic,
        "sessionKey": make_session_id(subject or role, question),
        "answerSource": answer_source,
        "queryTokens": query_tokens,
        "matchedBy": context_strength,
        "matchedCount": len(context_pages),
        "candidateCount": payload.get("candidateCount", 0),
        "primarySource": primary_source,
        "alternatives": alternatives,
        "topResultTitle": primary_source.get("title") if primary_source else "",
        "topResultPath": primary_source.get("path") if primary_source else "",
        "topResultTopic": primary_source.get("topic") if primary_source else "",
        "topResultVisibility": primary_source.get("visibility") if primary_source else "",
        "topResultExcerpt": primary_source.get("excerpt") if primary_source else "",
    }
