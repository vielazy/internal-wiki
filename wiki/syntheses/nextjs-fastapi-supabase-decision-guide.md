---
title: "Next.js + FastAPI + Supabase Decision Guide"
topic: "Web & App Development"
tags: [decision-guide, nextjs, fastapi, supabase, architecture, checklist]
created: 2026-04-28
updated: 2026-04-28
confidence: medium
sources:
  - https://nextjs.org/docs
  - https://fastapi.tiangolo.com/
  - https://supabase.com/docs
  - https://www.postgresql.org/docs/
visibility: public
---

# Next.js + FastAPI + Supabase Decision Guide

## Tóm tắt

Đây là bản rút gọn từ synthesis kiến trúc lớn, dùng như checklist quyết định nhanh khi build app với Next.js, FastAPI, và Supabase PostgreSQL. Mục tiêu là biết ngay nên đưa phần nào vào frontend, backend, hay database layer.

## Checklist quyết định nhanh

### Chọn Next.js khi:
- cần UI nhanh và đẹp
- cần routing rõ
- cần SSR / server components / interactive pages
- làm dashboard, wiki viewer, admin panel, search UI

### Chọn TypeScript khi:
- muốn type safety giữa UI và API
- muốn tránh mismatch payload
- có nhiều form / state / response shape

### Chọn Tailwind khi:
- muốn ship UI nhanh
- muốn design system đơn giản, thống nhất
- muốn internal tool nhìn gọn nhưng không tốn quá nhiều thời gian CSS

### Chọn FastAPI khi:
- cần business logic rõ
- cần search / sync / ACL / ranking endpoints
- cần validation, orchestration, audit hooks
- muốn backend dễ test và document

### Chọn Supabase khi:
- muốn Postgres managed
- muốn auth / storage / infra nhẹ hơn
- muốn có nền tảng cloud nhanh cho MVP hoặc internal app

## Kiến trúc mặc định nên dùng

- **Next.js** = frontend
- **FastAPI** = backend policy gate và application logic
- **Supabase PostgreSQL** = database/runtime state
- **Supabase Auth** = nếu cần auth managed
- **Supabase Storage** = nếu có file upload hoặc asset

## Quy tắc thực thi

- UI không xử lý ACL quyết định cuối cùng.
- Backend mới là nơi filter quyền và ranking search.
- DB là nơi search chạy, không phải nơi content được viết tay.
- Markdown là source of truth cho nội dung.
- Sync phải idempotent và transaction-safe.

## Khi nào không nên dùng full stack này

- app quá nhỏ, chỉ cần static page
- chỉ muốn 100% TypeScript fullstack, không cần backend riêng
- không cần auth/ACL/search phức tạp
- chưa có nhu cầu tách backend rõ ràng

## Khi nào nên ưu tiên stack này

- internal wiki
- knowledge platform
- document explorer
- AI assistant UI
- dashboard có search và permissions
- app cần Postgres rõ ràng và lâu dài

## Pitfalls

- Đừng để Next.js gánh hết logic nghiệp vụ.
- Đừng để Supabase auth và backend policy lệch nhau.
- Đừng để search logic nằm ở frontend.
- Đừng đọc markdown trực tiếp ở runtime production nếu DB đã có.

## Liên quan

- [[nextjs-fastapi-supabase-architecture]] — bản synthesis đầy đủ
- [[supabase-postgresql-search]] — strategy search trong Supabase/Postgres
- [[hybrid-search]] — khi corpus lớn lên
- [[ai-coding-workflows]] — workflow build/verify với AI

## Nguồn

- https://nextjs.org/docs
- https://fastapi.tiangolo.com/
- https://supabase.com/docs
- https://www.postgresql.org/docs/
