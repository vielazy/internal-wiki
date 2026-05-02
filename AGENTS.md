# AI Coding Wiki — AGENTS.md
# Schema cho Codex CLI | Cursor | Antigravity | Windsurf

## Mục tiêu

AI Coding Wiki là knowledge base tự động về vibe coding, AI agents, prompt engineering, và workflow patterns.

Repo này vận hành theo nguyên tắc:
- `raw/` là immutable source data
- `wiki/` là content source of truth
- PostgreSQL là derived state cho search, metadata, permissions, audit, và runtime data
- Obsidian là authoring/exploration UI, không phải search backend chính

## Cách dùng theo tool

| Tool | Cách gọi |
|---|---|
| Codex CLI | `codex "Đọc AGENTS.md và chạy discover → ingest → lint"` |
| Cursor | Chat: "Follow AGENTS.md. Chạy full cycle cho wiki" |
| Windsurf | Chat: "Đọc AGENTS.md, chạy /llm-wiki run" |
| Antigravity | `@llm-wiki run` |

## Cấu trúc repo

```
raw/          ← Nguồn thô — READ ONLY
wiki/         ← Output — LLM viết & duy trì
  concepts/
  tools/
  tutorials/
  agents/
  code-patterns/
  syntheses/
outputs/      ← Query results, digests
```

## Quy tắc cốt lõi

1. KHÔNG sửa file trong `raw/`.
2. Mọi page wiki phải có front matter YAML + `## Liên quan` + `## Nguồn`.
3. Ghi `wiki/LOG.md` sau mỗi hành động chính.
4. Grounded only — không có nguồn thì ghi gap.
5. Tiếng Việt là chính, technical terms giữ nguyên.
6. `wiki/` là content source of truth; DB chỉ là derived state cho metadata / search / permissions / audit.
7. Nếu DB bật, sau ingest hoặc cập nhật wiki phải sync DB; không viết tay content chuẩn trực tiếp vào DB.
8. Production search phải chạy trên PostgreSQL, không scan markdown trực tiếp nếu DB đã có.
9. Retrieval phải ACL-aware trước khi render hoặc log.
10. Obsidian chỉ là authoring/exploration tool.

## Search / runtime policy

- Baseline search: PostgreSQL full-text search trên `pages`
- Fuzzy search: `pg_trgm`
- Semantic search: chỉ bổ sung khi corpus và use case đủ rõ
- Search results phải được lọc theo `visibility` và `page_acl`
- Backlinks / related pages / tutor answers cũng phải tôn trọng quyền
- Query logs phải không leak nội dung private

## Sync policy

- Sync phải idempotent
- Sync phải transaction-safe
- Ưu tiên incremental sync
- Dùng `content_hash` / `sync_state` để phát hiện thay đổi
- Không overwrite lịch sử nếu chưa archive revision
- Nếu DB mode bật, search/query phải ưu tiên DB

## Roadmap bám theo khi làm việc

### Phase 1 — File-based wiki core
Mục tiêu: giữ hệ thống chạy ổn định bằng markdown + graph + log.

- `discover` — tìm nguồn mới theo `config.yaml`
- `ingest` — xử lý `raw/` → tạo/cập nhật wiki pages
- `lint` — health check: orphans, gaps, contradictions
- Duy trì `wiki/INDEX.md` và `wiki/LOG.md`
- Giữ `raw/` immutable, mọi tri thức đã compile đi vào `wiki/`

### Phase 2 — Content expansion
Mục tiêu: mở rộng độ phủ tri thức và cross-reference.

- Ưu tiên phủ đủ `concepts/`, `tools/`, `tutorials/`, `agents/`, `code-patterns/`, `syntheses/`
- Tạo synthesis khi cần so sánh tool/pattern
- Tạo tutorial khi cần hướng dẫn end-to-end
- Khi có file mới trong `raw/`, trích xuất concept/pattern/insight và thêm link chéo

### Phase 3 — Automation agents
Mục tiêu: tự động hóa ingest từ nhiều nguồn đầu vào.

- Video ingest agent: YouTube URL → transcript → raw markdown → ingest
- Repo ingest agent: GitHub repo URL → extract architecture/patterns/code examples → raw markdown → ingest
- Automation theo lịch: chạy discover → ingest → lint định kỳ
- Prompt library: lưu prompt templates, `CLAUDE.md`/`AGENTS.md` mẫu, reusable workflows

### Phase 4 — Productization for internal wiki
Mục tiêu: chuẩn bị cho wiki nội bộ công ty có public/internal content.

- Thêm DB cho metadata, permissions, audit, search index
- Giữ markdown làm content source of truth; DB sync từ `wiki/` để query nhanh hơn
- Thiết kế visibility: `public` / `internal` / `restricted` / `private`
- Build chat/tutor agent có context từ wiki và quyền truy cập
- Build skill graph / learning path theo user hoặc team
- Build viewer/dashboard để tra cứu, filter, graph view, recent updates
- Thêm revision history, backup/restore, observability cho sync/search
- Dùng hybrid search khi wiki lớn và nhu cầu semantic rõ ràng

## Query
Khi được hỏi câu hỏi:
- Đọc `wiki/INDEX.md` → tìm trang liên quan → đọc trang đó
- Trả lời từ wiki (không tự bịa)
- Lưu kết quả vào `outputs/queries/`

## Page Template

```markdown
---
title: "Tên trang"
topic: "Topic"
tags: [tag1, tag2]
created: YYYY-MM-DD
updated: YYYY-MM-DD
confidence: high | medium | low
sources: [raw/articles/file.md]
visibility: public | internal | restricted | private
---

# Tên trang

## Tóm tắt
[1-2 câu cốt lõi]

## Nội dung chính
[Chi tiết, ví dụ, code]

## Thực hành / Ví dụ
[Ví dụ cụ thể]

## Lưu ý & Pitfalls
[Common mistakes]

## Liên quan
- [[trang-lien-quan]] — lý do

## Nguồn
- raw/articles/filename.md
```

## LOG format

```markdown
[YYYY-MM-DD HH:MM] [DISCOVER] Tìm 5 nguồn mới về vibe coding
[YYYY-MM-DD HH:MM] [INGEST] Tạo trang concepts/react-agent-pattern.md
[YYYY-MM-DD HH:MM] [LINT] Phát hiện 2 orphan pages, 1 contradiction
[YYYY-MM-DD HH:MM] [QUERY] "So sánh ReAct vs Plan-and-Execute" → outputs/queries/
[YYYY-MM-DD HH:MM] [SYNC] Đồng bộ `wiki/` → PostgreSQL
[YYYY-MM-DD HH:MM] [DB] Khởi tạo schema / cập nhật viewer sang DB mode
[YYYY-MM-DD HH:MM] [CONFIG] Cập nhật roadmap cho content expansion / automation / productization
```
