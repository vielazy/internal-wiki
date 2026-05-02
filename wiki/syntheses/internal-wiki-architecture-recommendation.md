---
title: "Internal Wiki Architecture Recommendation"
topic: "Knowledge Ops & Productization"
tags: [synthesis, internal-wiki, architecture, recommendation, postgresql, supabase]
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

# Internal Wiki Architecture Recommendation

## Tóm tắt

Khuyến nghị hiện tại cho AI Coding Wiki là giữ markdown làm nguồn nội dung, dùng PostgreSQL trên Supabase làm runtime state, và để backend enforce search, ACL, audit, và sync. Mô hình này cân bằng tốt giữa tốc độ phát triển, khả năng scale, và tính an toàn cho nội bộ.

## Khuyến nghị chính

### 1) Content layer

- `raw/` là nguồn thô immutable
- `wiki/` là content source of truth
- Obsidian là editor/graph/search UI cho authoring

### 2) Runtime layer

- PostgreSQL là nơi search và metadata sống
- API/backend là nơi enforce quyền và business rules
- UI chỉ render dữ liệu đã được lọc

### 3) Search layer

- full-text search là baseline
- trigram search là fuzzy layer
- semantic search chỉ thêm sau
- search phải ACL-aware ngay từ đầu

### 4) Permission layer

- dùng Supabase Auth nếu cần auth managed
- dùng visibility + page ACL cho authorization
- enforce quyền ở backend/DB, không chỉ ở frontend

### 5) Sync layer

- sync markdown → DB phải idempotent
- sync phải transaction-safe
- dùng hash/state để phát hiện drift
- runtime không đọc markdown trực tiếp khi DB mode đã sẵn sàng

## Kiến trúc khuyến nghị cho dự án này

### Frontend
- Next.js cho UI, browse, search, graph, dashboard
- Tailwind cho styling nhanh và nhất quán
- TypeScript để giữ contract rõ giữa UI và API

### Backend
- FastAPI cho search API, sync API, permission-aware retrieval, tutor/chat orchestration
- backend là lớp quyết định cuối cùng cho ACL

### Data
- Supabase PostgreSQL cho pages, tags, links, sources, ACL, logs, sessions
- Supabase Auth nếu cần đăng nhập managed

## Không nên làm

- Không để runtime production scan markdown trực tiếp nếu DB đã có
- Không để frontend tự quyết quyền cuối cùng
- Không coi Obsidian là search engine backend
- Không nhét tất cả logic vào một lớp duy nhất

## Khi nào kiến trúc này phù hợp

- internal wiki có public/internal/restricted/private content
- có search thường xuyên
- có nhu cầu audit và traceability
- có người dùng nội bộ hoặc team collaboration
- muốn giữ content bằng markdown nhưng runtime vẫn nhanh

## Khi nào cần nâng cấp thêm

- corpus lớn hơn nhiều
- search semantic trở nên cần thiết
- ACL phức tạp theo nhóm/tenant/project
- có audit/compliance nặng
- cần workflow approval hoặc revision governance

## Checklist triển khai

- [ ] Content nằm trong markdown
- [ ] DB sync ổn định
- [ ] Search chạy trên PostgreSQL
- [ ] ACL enforced ở backend
- [ ] Logs tách theo loại
- [ ] Revision history có plan
- [ ] Backup/restore có plan
- [ ] UI không phụ thuộc runtime scan file

## Liên quan

- [[nextjs-fastapi-supabase-architecture]] — kiến trúc chi tiết theo stack
- [[nextjs-fastapi-supabase-decision-guide]] — checklist quyết định nhanh
- [[supabase-postgresql-search]] — strategy search trên Supabase/Postgres
- [[supabase-auth-acl-model]] — mô hình auth + ACL
- [[wiki-architecture-map]] — bản đồ điều hướng tài liệu
- [[project-priority-plan]] — thứ tự việc cần làm

## Nguồn

- AI_CODING_WIKI_GUIDE.md
- PROJECT_PRIORITY_PLAN.md
- https://supabase.com/docs
- https://www.postgresql.org/docs/
