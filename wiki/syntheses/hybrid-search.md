---
title: "Hybrid Search for Large Wiki"
topic: "Knowledge Base & RAG"
tags: [hybrid-search, search, bm25, vector-search, rag]
created: 2026-04-20
updated: 2026-04-20
confidence: low
sources:
  - https://www.anthropic.com/learn/build-with-claude
  - https://www.anthropic.com/news/contextual-retrieval
  - https://modelcontextprotocol.io/introduction
---

# Hybrid Search for Large Wiki

## Tóm tắt

Khi wiki lớn lên, chỉ dựa vào brute-force đọc `INDEX.md` và file markdown là chưa đủ. Hybrid search kết hợp keyword search, metadata filtering, và vector search sẽ giúp tìm đúng trang nhanh hơn và giữ trải nghiệm tra cứu tốt.

## Nội dung chính

### Vì sao cần hybrid search

Với wiki nhỏ, agent có thể đọc `INDEX.md` rồi mở vài trang liên quan.
Khi wiki tăng lên hàng trăm trang, cách đó chậm và dễ bỏ sót.
Hybrid search giúp:
- tìm theo keyword chính xác
- tìm theo ngữ nghĩa gần đúng
- lọc theo topic, tags, confidence, visibility
- xếp hạng theo relevance

### Thành phần đề xuất

1. **BM25 / full-text search**
   - tốt cho query có keyword rõ ràng
   - nhanh và dễ giải thích

2. **Vector search**
   - tốt cho query mơ hồ hoặc semantic similarity
   - giúp tìm page liên quan dù không trùng từ khóa

3. **Metadata filter**
   - topic
   - tags
   - confidence
   - updated date
   - visibility (`public` / `internal`)

4. **Graph expansion**
   - backlinks
   - linked pages
   - sibling pages

### Cách dùng trong wiki này

- Dùng `INDEX.md` như catalog thô ở giai đoạn nhỏ
- Khi page count tăng, build search index riêng
- `tutor-agent` và future chat agent dùng hybrid search để chọn context
- `skill-graph` có thể feed vào ranking để cá nhân hóa

## Thực hành / Ví dụ

- Query "prompt best practices" → search theo keyword + semantic + topic `Prompt Engineering`
- Query "đi từ zero đến project chạy được" → gợi ý `bat-dau-vibe-coding`
- Query "repo ingest" → tìm `ingest_repo.py`, `prompt-library`, `AI Coding Workflows`

## Lưu ý & Pitfalls

- Đừng dùng vector search một mình nếu query có keyword rõ.
- Đừng bỏ metadata filter, vì nó rất quan trọng cho public/internal sau này.
- Nếu search index không được cập nhật cùng ingest, kết quả sẽ lệch.

## Liên quan

- [[rag]] — lớp retrieval nền tảng
- [[knowledge-base]] — nguồn tri thức để search
- [[contextual-retrieval]] — hướng cải thiện chất lượng retrieval
- [[tutor-agent]] — agent sẽ hưởng lợi từ hybrid search

## Nguồn

- https://www.anthropic.com/learn/build-with-claude
- https://www.anthropic.com/news/contextual-retrieval
- https://modelcontextprotocol.io/introduction
