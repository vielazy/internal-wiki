---
title: "Supabase RLS vs App-Layer ACL"
topic: "Knowledge Ops & Productization"
tags: [synthesis, supabase, rls, acl, permissions, postgresql]
created: 2026-04-28
updated: 2026-04-28
confidence: medium
sources:
  - https://supabase.com/docs
  - https://www.postgresql.org/docs/
visibility: public
---

# Supabase RLS vs App-Layer ACL

## Tóm tắt

Trong hệ thống dùng Supabase PostgreSQL, Row Level Security (RLS) và app-layer ACL là hai lớp bảo vệ khác nhau nhưng bổ trợ nhau. RLS bảo vệ dữ liệu ở tầng database, còn app-layer ACL cho phép backend kiểm soát logic truy cập phức tạp hơn, đặc biệt khi cần search, backlinks, tutor/chat, hoặc quyền theo role/user/team.

## Nội dung chính

### 1) RLS là gì

RLS là cơ chế của PostgreSQL cho phép quy định hàng nào user được phép thấy hoặc sửa ngay ở database layer. Đây là lớp bảo vệ rất mạnh vì query chỉ trả về dữ liệu hợp lệ theo policy.

### 2) App-layer ACL là gì

App-layer ACL là logic quyền được enforce ở backend/application layer. Ví dụ:

- kiểm tra role
- kiểm tra subject
- kiểm tra visibility
- kiểm tra membership theo team/project
- kiểm tra quyền trước khi search, fetch, hay render backlinks

### 3) Khi nào nên dùng RLS

RLS phù hợp khi:

- muốn DB tự chặn truy cập sai
- dữ liệu đa user, đa tenant
- cần safety level cao
- muốn giảm rủi ro query bypass từ client

### 4) Khi nào nên dùng app-layer ACL

App-layer ACL phù hợp khi:

- logic quyền phức tạp hơn row visibility đơn giản
- cần combine với search ranking
- cần quản lý backlinks/related pages/tutor answers
- cần log, audit, and custom permission semantics
- cần quyền theo page, role, user, group, hoặc context

### 5) Mô hình khuyến nghị cho dự án này

Khuyến nghị tốt nhất là kết hợp cả hai:

- **RLS** làm lớp phòng thủ cuối cùng trong database
- **app-layer ACL** làm lớp logic chính trong backend

Backend sẽ:
- xác định user/role từ auth
- filter page/search result theo quyền
- tạo query an toàn
- trả về dữ liệu đã được phép

RLS sẽ:
- chặn các truy vấn bypass ngoài ý muốn
- tăng safety nếu có bug ở backend

### 6) Trade-off

#### Chỉ dùng app-layer ACL
- dễ implement ban đầu
- linh hoạt
- nhưng phụ thuộc mạnh vào backend đúng

#### Chỉ dùng RLS
- rất mạnh ở DB
- nhưng có thể khó biểu đạt logic phức tạp
- search/ranking/business logic có thể trở nên cứng

#### Dùng cả hai
- an toàn nhất
- nhưng cần kỷ luật thiết kế rõ ràng
- phải tránh duplicate logic mơ hồ

## Thực hành / Ví dụ

Mô hình thực dụng cho internal wiki:

1. Backend xác thực user qua Supabase Auth
2. Backend xác định role/subject
3. Backend query DB với ACL-aware filters
4. RLS là lớp chặn cuối
5. UI chỉ nhận dữ liệu đã qua kiểm tra

## Lưu ý & Pitfalls

- Đừng giả định Supabase Auth tự xử lý hết authorization.
- Đừng để frontend quyết định quyền truy cập cuối cùng.
- Đừng tạo policy RLS quá phức tạp nếu app-layer ACL đã đủ rõ.
- Đừng bỏ quên search results, backlinks, và tutor/chat là các đường leak rất dễ quên.

## Liên quan

- [[supabase-auth-acl-model]] — mô hình auth + ACL tổng quát
- [[internal-wiki-architecture-recommendation]] — kiến trúc production được khuyến nghị
- [[nextjs-fastapi-supabase-architecture]] — architecture chi tiết theo stack
- [[supabase-postgresql-search]] — search layer trong Supabase/Postgres
- [[wiki-architecture-map]] — bản đồ điều hướng tài liệu

## Nguồn

- https://supabase.com/docs
- https://www.postgresql.org/docs/
