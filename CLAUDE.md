# AI Coding Wiki — CLAUDE.md
# Schema cho Claude Code | Đọc file này trước khi thực hiện bất kỳ lệnh nào

## Mục tiêu

AI Coding Wiki là knowledge base tự động về vibe coding, AI agents, prompt engineering, và workflow patterns.

Claude Code dùng repo này theo mô hình:
- `raw/` là nguồn thô, immutable
- `wiki/` là content source of truth
- PostgreSQL là derived state cho search, permissions, audit, và runtime data
- Obsidian là lớp authoring/exploration, không phải search backend chính

---

## Cấu trúc thư mục

```
ai-coding-wiki/
├── CLAUDE.md              ← File này — schema cho Claude Code
├── AGENTS.md              ← Schema cho Codex / Cursor / Antigravity
├── AI_CODING_WIKI_GUIDE.md← Master guide tổng quát cho cả repo
├── config.yaml            ← Cấu hình topics, sources, schedule
├── wiki-viewer.html       ← Viewer trên browser
│
├── raw/                   ← Nguồn thô — LLM KHÔNG ĐƯỢC SỬA CÁC FILE NÀY
│   ├── articles/
│   ├── notes/
│   ├── slides/
│   ├── videos/
│   └── repos/
│
├── wiki/                  ← Wiki do LLM viết & duy trì — output chính
│   ├── INDEX.md
│   ├── LOG.md
│   ├── concepts/
│   ├── tools/
│   ├── tutorials/
│   ├── agents/
│   ├── code-patterns/
│   └── syntheses/
│
├── outputs/
└── .discoveries/
```

---

## Invariants

### `raw/`
- KHÔNG BAO GIỜ sửa, xóa, overwrite file trong `raw/`
- `raw/` là immutable source data
- chỉ human mới thêm file vào `raw/`

### `wiki/`
- LLM là người duy nhất viết/sửa nội dung trong `wiki/`
- mọi page phải có front matter YAML đầy đủ
- mỗi page phải có `## Liên quan` và `## Nguồn`
- page phải atomic, grounded, có cross-links

### `LOG.md`
- mọi hành động ingest/discover/lint/query/sync phải được ghi log phù hợp
- append only
- format: `[YYYY-MM-DD HH:MM] [ACTION] mô tả ngắn`

### Search / runtime
- production search phải chạy trên PostgreSQL
- không scan markdown trực tiếp trong runtime production nếu DB đã có
- retrieval phải tôn trọng ACL/visibility
- Obsidian chỉ là authoring/exploration tool

---

## Page template

```markdown
---
title: "Tên trang"
topic: "Tên topic từ config.yaml"
tags: [tag1, tag2, tag3]
created: YYYY-MM-DD
updated: YYYY-MM-DD
confidence: high | medium | low
sources: [raw/articles/filename.md, https://url-goc.com]
visibility: public | internal | restricted | private
---

# Tên trang

## Tóm tắt
[1-2 câu mô tả cốt lõi]

## Nội dung chính
[Chi tiết, ví dụ, code snippets nếu có]

## Thực hành / Ví dụ
[Ví dụ cụ thể, prompt mẫu, hoặc bước thực hiện]

## Lưu ý & Pitfalls
[Điều cần tránh, common mistakes, gotchas]

## Liên quan
- [[trang-lien-quan-1]] — lý do liên quan
- [[trang-lien-quan-2]] — lý do liên quan

## Nguồn
- raw/articles/filename.md
- https://url-goc.com
```

---

## Quy trình làm việc

### Khi ingest
1. Đọc nguồn mới trong `raw/`
2. Trích xuất concept, pattern, insight
3. Tạo/cập nhật trang wiki tương ứng
4. Thêm cross-references
5. Đánh dấu contradiction nếu có
6. Cập nhật `wiki/INDEX.md`
7. Ghi log vào `wiki/LOG.md`
8. Nếu DB bật thì sync sang PostgreSQL

### Khi query
1. Đọc `wiki/INDEX.md` trước
2. Đọc các trang liên quan
3. Trả lời dựa trên wiki, không tự bịa
4. Nếu chưa đủ thông tin thì nói rõ gap
5. Ghi câu hỏi + kết quả vào `outputs/queries/`

### Khi lint
- tìm orphan pages
- tìm broken links
- tìm contradictions
- tìm pages confidence thấp
- tìm gaps theo topic

---

## PostgreSQL / internal mode

Khi DB được bật:
- `wiki/` vẫn là content source of truth
- DB chỉ là derived state để query nhanh hơn
- mọi sync phải idempotent và transaction-safe
- search/query phải ưu tiên DB mode
- runtime logs phải tách khỏi wiki authoring logs

### Nên có trong DB
- `pages`
- `page_tags`
- `page_links`
- `page_sources`
- `page_acl`
- `query_logs`
- `runtime_activity_log`
- `sync_state`
- `chat_sessions`
- `chat_messages`
- `tutor_progress`
- `quiz_attempts`

### Search policy
- baseline: PostgreSQL full-text search
- fuzzy: `pg_trgm`
- semantic search chỉ thêm sau khi cần
- permissions phải filter trước khi render

---

## Roadmap cốt lõi

### Phase 1 — File-based wiki core
- discover → ingest → lint
- giữ raw immutable
- giữ wiki/index/log ổn định

### Phase 2 — Content expansion
- mở rộng concepts/tools/tutorials/agents/code-patterns/syntheses
- tăng cross-link
- thêm tutorial end-to-end và synthesis so sánh

### Phase 3 — Automation agents
- video ingest agent
- repo ingest agent
- scheduled runs
- prompt library và reusable workflows

### Phase 4 — Productization for internal wiki
- PostgreSQL search/index/permissions/audit
- revision history
- backup/restore
- hybrid search
- viewer/dashboard nội bộ
- tutor/chat agent có ACL-aware retrieval

---

## Ngôn ngữ & phong cách

- Tiếng Việt là chính
- giữ nguyên technical terms tiếng Anh
- ngắn gọn, thực tế, giống đồng nghiệp developer
- nếu không chắc, đặt `confidence: low`

---

## Quy tắc chất lượng

1. Grounded only
2. No hallucination
3. Atomic pages
4. Link generously
5. Flag contradictions
6. Search production phải đi qua DB
7. Obsidian không phải runtime backend

---

## Automation

```bash
# Trong Claude Code session:
/loop 2h /llm-wiki run

# Hoặc crontab:
# 0 */2 * * * cd /path/to/ai-coding-wiki && claude --print "/llm-wiki run"
```
