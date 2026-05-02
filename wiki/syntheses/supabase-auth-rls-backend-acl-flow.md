---
title: "Supabase Auth + RLS + Backend ACL Flow"
topic: "Knowledge Ops & Productization"
tags: [synthesis, supabase, auth, rls, acl, flow, permissions]
created: 2026-04-28
updated: 2026-04-28
confidence: medium
sources:
  - https://supabase.com/docs
  - https://www.postgresql.org/docs/
visibility: public
---

# Supabase Auth + RLS + Backend ACL Flow

## Tóm tắt

Đây là flow end-to-end khuyến nghị cho internal wiki: Supabase Auth xác thực user, backend xác định context và enforce ACL logic, PostgreSQL RLS chặn ở tầng cuối, và UI chỉ render dữ liệu đã được phép. Mục tiêu là vừa an toàn, vừa đủ linh hoạt cho search, backlinks, page fetch, và tutor/chat.

## Flow khuyến nghị

### Bước 1 — Authentication

User đăng nhập qua Supabase Auth để nhận danh tính và session/token hợp lệ.

Tầng này trả lời câu hỏi:
- ai đang đăng nhập?
- session có hợp lệ không?

### Bước 2 — Context resolution ở backend

Backend đọc token/session để xác định:
- role
- subject/user id
- team/group context nếu có
- các quyền ứng dụng liên quan

Tầng này trả lời câu hỏi:
- user này thuộc vai trò nào?
- được phép truy cập lớp dữ liệu nào?

### Bước 3 — ACL-aware query ở backend

Backend áp dụng ACL logic trước khi query hoặc khi build query.

Ví dụ:
- lọc theo `visibility`
- lọc theo `page_acl`
- lọc theo project/team nếu có
- search results phải đi qua cùng logic này
- backlinks/related pages cũng phải được filter

### Bước 4 — RLS ở database

RLS là lớp chặn cuối cùng trên PostgreSQL.

Mục đích:
- ngăn query bypass ngoài ý muốn
- bảo vệ data nếu backend có bug
- tăng safety cho multi-tenant hoặc internal content

### Bước 5 — UI render kết quả đã lọc

Frontend chỉ hiển thị:
- page đã được phép
- search result đã lọc
- backlinks/related pages đã lọc
- tutor/chat response đã kiểm tra quyền

UI không nên là nơi quyết định quyền cuối cùng.

## Khi nào dùng flow này

Flow này phù hợp khi bạn có:
- internal wiki
- public/internal/private content
- search runtime trên DB
- auth người dùng thật
- nhu cầu audit hoặc traceability
- tutor/chat hoặc query API có thể leak dữ liệu nếu kiểm soát kém

## Ưu điểm

- an toàn hơn so với chỉ dùng UI filter
- backend vẫn linh hoạt cho business logic
- RLS làm lớp bảo vệ cuối cùng
- dễ mở rộng khi thêm team/group hoặc tenant

## Trade-off

- phức tạp hơn chỉ dùng auth đơn giản
- cần đồng bộ giữa backend ACL và RLS policy
- phải test kỹ search/backlinks/chat flow
- cần kỷ luật trong thiết kế query layer

## Pitfalls

- Không để Supabase Auth tự gánh toàn bộ authorization.
- Không để frontend tự quyết quyền cuối cùng.
- Không quên filter search, backlinks, related pages, và tutor/chat.
- Không viết policy RLS quá phức tạp nếu backend ACL đã đủ rõ.
- Không leak private content vào logs hoặc snippets.

## Checklist triển khai

- [ ] Supabase Auth dùng cho authentication
- [ ] Backend xác định role/subject/context
- [ ] Backend áp ACL cho search và page fetch
- [ ] RLS bật trên bảng quan trọng
- [ ] UI chỉ render output đã được phép
- [ ] Query logs không leak nội dung private
- [ ] Backlinks/related pages cũng respect quyền
- [ ] Tutor/chat retrieval cũng ACL-aware

## Liên quan

- [[supabase-auth-acl-model]] — mô hình auth + ACL tổng quát
- [[supabase-rls-vs-app-layer-acl]] — so sánh RLS và ACL layer
- [[internal-wiki-architecture-recommendation]] — kiến trúc production được khuyến nghị
- [[nextjs-fastapi-supabase-architecture]] — kiến trúc stack chi tiết
- [[wiki-architecture-map]] — bản đồ điều hướng tài liệu

## Nguồn

- https://supabase.com/docs
- https://www.postgresql.org/docs/
