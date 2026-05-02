---
title: "Supabase Auth + ACL Model"
topic: "Knowledge Ops & Productization"
tags: [synthesis, supabase, auth, acl, permissions, internal-wiki]
created: 2026-04-28
updated: 2026-04-28
confidence: medium
sources:
  - https://supabase.com/docs
  - https://www.postgresql.org/docs/
visibility: public
---

# Supabase Auth + ACL Model

## Tóm tắt

Với internal wiki hoặc knowledge platform, Supabase Auth nên được xem là lớp nhận diện người dùng, còn quyền truy cập thật sự phải được enforce ở backend và database layer. Mô hình này giúp tách rõ authentication, authorization, và content retrieval.

## Nội dung chính

### 1) Phân biệt auth và ACL

- **Authentication**: ai đang đăng nhập?
- **Authorization / ACL**: người đó được phép xem gì?

Supabase Auth phù hợp để xác thực user và phát JWT/session, nhưng không nên là nơi duy nhất chứa logic quyền. Quyền truy cập nội dung cần được kiểm tra ở backend hoặc DB query layer.

### 2) Mô hình quyền khuyến nghị

Một mô hình đơn giản nhưng đủ dùng:

- `public` — ai cũng xem được
- `internal` — chỉ người trong hệ thống
- `restricted` — chỉ role cao hơn hoặc nhóm cụ thể
- `private` — chỉ admin hoặc owner

Ngoài visibility, có thể thêm `page_acl` cho rule chi tiết hơn theo role/user/group.

### 3) Nơi enforce quyền

Quyền nên được áp dụng ở nhiều điểm:

- search results
- page fetch
- related pages
- backlinks
- tutor/chat retrieval
- query logs và export

Nếu chỉ enforce ở UI, dữ liệu vẫn có thể lộ qua API hoặc logs.

### 4) Khuyến nghị triển khai trong Supabase/Postgres

- lưu `visibility` ngay trong `pages`
- lưu rule chi tiết trong `page_acl`
- backend đọc claims từ Supabase Auth
- backend áp ACL trước khi trả response
- query search filter theo quyền từ đầu

### 5) Khi nào cần ACL phức tạp hơn

Nên tăng độ phức tạp chỉ khi thật sự cần:

- có nhiều team / group
- có nội dung per-client / per-project
- có tài liệu nhạy cảm
- có compliance hoặc audit yêu cầu cao

Nếu chưa đến mức đó, mô hình role + visibility là đủ.

## Thực hành / Ví dụ

Một flow hợp lý:

1. User đăng nhập bằng Supabase Auth
2. Backend nhận token và xác định role/subject
3. Backend query Postgres với filter ACL
4. Backend trả page/search result đã được lọc
5. UI render mà không tự quyết quyền cuối cùng

## Lưu ý & Pitfalls

- Đừng dùng Supabase Auth như toàn bộ authorization system.
- Đừng để frontend tự quyết quyền hiển thị nội dung private.
- Đừng quên filter ACL cho search và backlinks.
- Đừng để query logs chứa thông tin riêng tư.

## Liên quan

- [[nextjs-fastapi-supabase-architecture]] — kiến trúc tổng cho stack app
- [[supabase-postgresql-search]] — search layer trong Supabase/Postgres
- [[project-priority-plan]] — ưu tiên các việc liên quan đến ACL/runtime
- [[ai-coding-wiki-guide]] — policy nền tảng của dự án

## Nguồn

- https://supabase.com/docs
- https://www.postgresql.org/docs/
