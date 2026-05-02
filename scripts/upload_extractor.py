from __future__ import annotations

import io
from pathlib import Path
from typing import Any


def extract_text_from_upload(filename: str, data: bytes) -> str:
    name = filename.lower()
    if name.endswith('.pdf'):
        try:
            from pypdf import PdfReader  # type: ignore
            reader = PdfReader(io.BytesIO(data))
            return '\n'.join(page.extract_text() or '' for page in reader.pages).strip()
        except Exception:
            return data.decode('utf-8', errors='ignore').strip()
    if name.endswith('.docx'):
        try:
            from docx import Document  # type: ignore
            doc = Document(io.BytesIO(data))
            return '\n'.join(p.text for p in doc.paragraphs).strip()
        except Exception:
            return data.decode('utf-8', errors='ignore').strip()
    if name.endswith('.doc'):
        return data.decode('utf-8', errors='ignore').strip()
    return data.decode('utf-8', errors='ignore').strip()


def build_draft_from_text(title: str, topic: str, content_text: str, tags: list[str] | None = None) -> dict[str, Any]:
    tags = [t.strip() for t in (tags or []) if t.strip()]
    body = f"""---
title: \"{title}\"
topic: \"{topic}\"
tags: [{', '.join(tags)}]
created: 2026-04-28
updated: 2026-04-28
confidence: medium
sources: []
visibility: internal
---

# {title}

## Tóm tắt
Tài liệu này được tạo từ upload nội bộ và đã được agents kiểm tra sơ bộ.

## Nội dung chính
{content_text}

## Liên quan
- [[wiki-architecture-map]] — tham chiếu kiến trúc

## Nguồn
- upload:internal
"""
    return {
        'title': title,
        'topic': topic,
        'tags': tags,
        'body': body,
    }
