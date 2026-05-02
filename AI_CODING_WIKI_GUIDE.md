# AI Coding Wiki — Master Guide

Tài liệu này là bản tham chiếu tổng quát cho toàn dự án. Khi chỉnh sửa, mở rộng, hoặc tự động hóa repo, ưu tiên tuân theo các nguyên tắc dưới đây.

## 1) Mục tiêu của dự án

AI Coding Wiki là knowledge base tự động về:
- vibe coding
- AI agents
- prompt engineering
- tool/workflow patterns
- knowledge management cho dự án AI

Mục tiêu dài hạn:
- giữ tri thức có cấu trúc, có nguồn, có thể truy hồi nhanh
- cho phép LLM đọc, viết, tổng hợp, và duy trì wiki một cách an toàn
- chuẩn bị nền tảng để phát triển thành app nội bộ với search, permissions, audit, và tutor/chat

## 2) Mô hình hệ thống

### Source of truth
- `raw/` là nguồn thô, immutable, read-only với LLM
- `wiki/` là content source of truth sau khi đã compile từ nguồn thô
- markdown là định dạng làm việc chính
- Obsidian là lớp authoring/exploration UI, không phải runtime search backend

### Derived state
- PostgreSQL là lớp derived state cho:
  - search
  - metadata
  - permissions
  - audit
  - runtime logs
  - session data
- không viết tay nội dung chuẩn trực tiếp vào DB
- mọi thay đổi content phải đi qua markdown/sync pipeline

### Runtime
- web viewer / API chỉ đọc từ file mode hoặc DB mode tùy môi trường
- production ưu tiên DB mode
- file mode chỉ dùng cho local/dev/debug

## 3) Bất biến quan trọng

1. Không sửa, xóa, hoặc overwrite file trong `raw/`.
2. Mọi trang wiki phải có front matter YAML đầy đủ.
3. Mỗi trang phải có `## Liên quan` và `## Nguồn`.
4. Mọi hoạt động ingest/discover/lint/query/sync phải được ghi log phù hợp.
5. Không hallucinate: nếu thiếu nguồn thì phải ghi gap.
6. Nội dung wiki phải grounded vào `raw/` hoặc URL cụ thể.
7. Search production phải chạy trên PostgreSQL, không scan file markdown trực tiếp.
8. Retrievial phải tôn trọng ACL/visibility trước khi render hoặc log.

## 4) Vai trò của Obsidian

Obsidian được dùng để:
- edit markdown
- browse graph/backlinks
- local search trong vault
- hỗ trợ review tri thức

Obsidian không được coi là:
- source of truth cho runtime
- search engine chính cho API/web app
- nơi lưu trạng thái nghiệp vụ runtime

## 5) Quy tắc content

### Trang wiki
Mỗi trang nên theo template này:

```markdown
---
title: "Tên trang"
topic: "Topic"
tags: [tag1, tag2]
created: YYYY-MM-DD
updated: YYYY-MM-DD
confidence: high | medium | low
sources: [raw/articles/file.md, https://url-goc.com]
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
- https://url-goc.com
```

### Cross-linking
- dùng `[[wikilink]]` để tạo liên kết chéo
- ưu tiên link hai chiều khi hợp lý
- mỗi page nên có ít nhất vài related links để giảm orphan pages

### Chất lượng
- atomic page: một concept chính
- grounded only
- có `confidence` rõ ràng
- nếu còn thiếu dữ liệu, đánh dấu gap thay vì bịa

## 6) Search architecture khuyến nghị

### Tầng 1 — lexical search
- PostgreSQL full-text search trên `pages`
- `tsvector` + `GIN index`
- ranking ưu tiên title, tags, excerpt, body

### Tầng 2 — fuzzy search
- `pg_trgm` cho typo, gần đúng, search ngắn
- hữu ích cho query kỹ thuật và tên viết tắt

### Tầng 3 — semantic search
- chỉ thêm khi corpus đủ lớn và nhu cầu thực sự rõ
- nên là lớp bổ sung, không thay lexical search

### Nguyên tắc search
- query runtime không scan toàn bộ markdown nếu có DB
- filter theo ACL/visibility trước khi trả kết quả
- log query để tune ranking và relevance

## 7) Sync & indexing

### Sync policy
- sync phải idempotent
- sync phải transaction-safe
- ưu tiên incremental sync
- dùng `content_hash` / `sync_state` để phát hiện thay đổi
- không overwrite content lịch sử nếu chưa archive revision

### Indexing policy
- `pages` là bảng chính cho content search
- `page_tags`, `page_links`, `page_sources`, `page_acl` là metadata/graph/access layers
- nếu search lớn dần, có thể thêm materialized view hoặc bảng search riêng

### Revision & history
Nên có khả năng truy vết thay đổi qua:
- `content_hash`
- revision history
- sync timestamp
- source file/path
- delta metadata

## 8) Permissions & safety

- hỗ trợ `public`, `internal`, `restricted`, `private`
- áp dụng quyền ở lúc retrieval, không chỉ ở UI
- backlinks, related pages, chat/tutor và search đều phải respect quyền
- query logs và runtime logs không được leak nội dung private

## 9) Observability

Tách rõ các lớp log:

### Wiki authoring log
- `wiki/LOG.md`
- dành cho ingest/discover/lint/refactor của knowledge base
- append only

### Runtime logs
- `query_logs`
- `runtime_activity_log`
- `chat_sessions`
- `chat_messages`
- `quiz_attempts`
- `tutor_progress`

### Sync logs
- lịch sử job sync
- hash / page count / error status
- last successful sync

## 10) Roadmap đề xuất

### Phase A — Wiki core
- maintain `raw/`, `wiki/`, `INDEX.md`, `LOG.md`
- discover → ingest → lint
- chuẩn hóa page template và cross-links

### Phase B — Search & retrieval
- PostgreSQL search
- GIN / trigram index
- ACL-aware retrieval
- query logs

### Phase C — Automation
- ingest từ video, repo, notes
- scheduled runs
- prompt library và reusable workflows

### Phase D — Internal productization
- viewer/dashboard
- permissions
- audit trail
- revision history
- backup/restore
- hybrid search
- tutor/chat agent

## 11) Khi sửa repo, ưu tiên gì

1. Giữ content grounded và có nguồn
2. Giữ markdown là chuẩn
3. Đồng bộ DB sau khi content thay đổi
4. Đừng làm runtime phụ thuộc Obsidian
5. Tối ưu search trên PostgreSQL trước khi nghĩ tới semantic layer
6. Tách rõ authoring, sync, runtime, observability

## 12) Khi không chắc

- ưu tiên `confidence: low`
- ghi gap rõ ràng
- không tự bịa nội dung
- nếu hai nguồn mâu thuẫn, đánh dấu contradiction thay vì cố hòa giải
