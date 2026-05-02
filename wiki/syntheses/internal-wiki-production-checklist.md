---
title: "Internal Wiki Production Checklist"
topic: "Knowledge Ops & Productization"
tags: [checklist, internal-wiki, production, search, acl, sync, observability]
created: 2026-04-28
updated: 2026-04-28
confidence: medium
sources:
  - AI_CODING_WIKI_GUIDE.md
  - PROJECT_PRIORITY_PLAN.md
  - https://supabase.com/docs
  - https://www.postgresql.org/docs/
visibility: public
---

# Internal Wiki Production Checklist

## Tóm tắt

Đây là checklist triển khai cho AI Coding Wiki khi tiến gần hơn tới internal production. Mục tiêu là đảm bảo nội dung, search, ACL, sync, logs, và vận hành đủ ổn định trước khi mở rộng thêm tính năng.

## Checklist theo lớp

### 1) Content layer

- [ ] `raw/` vẫn immutable
- [ ] `wiki/` là source of truth
- [ ] mọi page có front matter đầy đủ
- [ ] mỗi page có `## Liên quan` và `## Nguồn`
- [ ] cross-link đủ để giảm orphan pages
- [ ] `wiki/INDEX.md` luôn phản ánh coverage hiện tại

### 2) Search layer

- [ ] PostgreSQL là runtime search engine chính
- [ ] full-text search index cho `pages`
- [ ] `pg_trgm` cho fuzzy search
- [ ] ranking ưu tiên title/tags/excerpt/body
- [ ] search query luôn ACL-aware
- [ ] query logs được ghi lại để tune relevance

### 3) Sync layer

- [ ] sync markdown → DB là incremental
- [ ] sync idempotent
- [ ] sync transaction-safe
- [ ] có `content_hash` / `sync_state`
- [ ] có job log rõ ràng
- [ ] khi content đổi thì DB reflect đúng và nhanh

### 4) Permission layer

- [ ] có visibility model `public/internal/restricted/private`
- [ ] `page_acl` có thể biểu đạt quyền chi tiết hơn nếu cần
- [ ] search results được filter trước khi trả
- [ ] backlinks / related pages được filter trước khi trả
- [ ] tutor/chat cũng ACL-aware
- [ ] query logs không leak nội dung private

### 5) Runtime layer

- [ ] UI không scan markdown trực tiếp khi DB mode đã sẵn sàng
- [ ] backend là nơi quyết định cuối cùng cho authz/ACL
- [ ] frontend chỉ render dữ liệu đã được phép
- [ ] viewer/dashboard tách rõ khỏi content source

### 6) Observability layer

- [ ] `wiki/LOG.md` chỉ ghi hoạt động xây wiki
- [ ] runtime logs tách riêng khỏi authoring logs
- [ ] có sync history / error trace
- [ ] có query logs để quan sát search behavior
- [ ] có khả năng audit các truy vấn và thay đổi quan trọng

### 7) Governance layer

- [ ] có revision history plan
- [ ] có backup / restore plan
- [ ] có người hoặc quy trình review page quan trọng
- [ ] có định nghĩa rõ vai trò của Supabase Auth, backend ACL, và RLS
- [ ] có tài liệu điều hướng nhất quán giữa guide / priority / tool entrypoints

## Thứ tự ưu tiên triển khai

1. Search trên PostgreSQL
2. Sync markdown → DB
3. ACL / visibility runtime
4. Tài liệu điều hướng nhất quán
5. Page gaps và tutorials
6. Logging / revision history
7. Semantic search hoặc dashboard phức tạp sau cùng

## Pitfalls cần tránh

- Không để frontend tự quyết quyền cuối cùng.
- Không để search runtime scan markdown nếu DB đã có.
- Không để logs lẫn authoring với runtime.
- Không để sync lệch giữa wiki và DB.
- Không mở rộng semantic search trước khi baseline search ổn định.

## Liên quan

- [[internal-wiki-architecture-recommendation]] — kiến trúc production được khuyến nghị
- [[wiki-architecture-map]] — bản đồ điều hướng tài liệu
- [[supabase-auth-rls-backend-acl-flow]] — flow auth + RLS + ACL
- [[supabase-postgresql-search]] — strategy search trên DB
- [[project-priority-plan]] — thứ tự việc cần làm

## Nguồn

- AI_CODING_WIKI_GUIDE.md
- PROJECT_PRIORITY_PLAN.md
- https://supabase.com/docs
- https://www.postgresql.org/docs/
