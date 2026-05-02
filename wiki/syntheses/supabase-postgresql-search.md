---
title: "Supabase PostgreSQL Search Strategy"
topic: "Knowledge Ops & Productization"
tags: [synthesis, supabase, postgresql, search, full-text-search, pg_trgm, acl]
created: 2026-04-28
updated: 2026-04-28
confidence: medium
sources:
  - https://www.postgresql.org/docs/
  - https://supabase.com/docs
visibility: public
---

# Supabase PostgreSQL Search Strategy

## Tóm tắt

Nếu bạn đang dùng PostgreSQL trên Supabase, cách search bền nhất là để PostgreSQL làm search engine chính cho dữ liệu wiki, thay vì scan markdown ở runtime. Kết hợp full-text search, trigram search, metadata filter, và ACL-aware retrieval sẽ cho kết quả nhanh và ổn định hơn nhiều khi corpus tăng lên.

## Nội dung chính

### 1) Vai trò của PostgreSQL trong search

PostgreSQL nên giữ toàn bộ lớp search runtime cho wiki:

- full-text search cho query rõ keyword
- fuzzy search cho typo hoặc query ngắn
- ranking theo title / tags / excerpt / body
- filter theo visibility / ACL
- query logs để tune relevance

Với Supabase, PostgreSQL là phần lõi nhất của runtime search chứ không chỉ là nơi lưu dữ liệu.

### 2) Full-text search là baseline

Dùng `tsvector` cho các trường như:

- `title`
- `topic`
- `excerpt`
- `body`
- `tags` hoặc text hóa metadata liên quan

Đây là tầng search mặc định vì:
- nhanh
- dễ giải thích
- phù hợp với query kỹ thuật
- hỗ trợ ranking tốt

### 3) Trigram search cho fuzzy query

`pg_trgm` hữu ích khi:
- user gõ sai chính tả
- query có tên viết tắt
- query gần đúng nhưng không trùng hẳn từ khóa

Trong thực tế, nhiều query kỹ thuật ngắn sẽ hưởng lợi lớn từ trigram.

### 4) ACL-aware retrieval

Search tốt nhưng không đủ; kết quả phải đúng quyền.

Cần đảm bảo:
- filter page theo visibility trước
- filter theo `page_acl` trước khi trả results
- backlinks và related pages cũng phải respect quyền
- query logs không leak private data

### 5) Indexing strategy

Nên ưu tiên:

- `GIN` index cho `tsvector`
- trigram index cho text trường chính
- tách metadata tables rõ ràng
- sync index cùng lúc với content sync

### 6) Data model khuyến nghị

Các bảng chính cho search:

- `pages`
- `page_tags`
- `page_links`
- `page_sources`
- `page_acl`
- `sync_state`
- `query_logs`

Nếu lớn hơn nữa, có thể thêm:
- bảng search riêng
- materialized view cho ranking/cache

### 7) Khi nào cần semantic search

Semantic search chỉ nên thêm khi:
- corpus lớn hơn đáng kể
- full-text + trigram không đủ
- query bắt đầu mang tính mô tả ý nghĩa, không chỉ keyword

Nó nên là lớp bổ sung, không thay baseline search.

### 8) Khuyến nghị cho project này

Với AI Coding Wiki, một pipeline search tốt nên là:

1. Markdown là source of truth
2. Sync content sang PostgreSQL trên Supabase
3. Build full-text / trigram search index
4. Search backend filter ACL
5. UI gọi backend, không scan markdown trực tiếp

## Thực hành / Ví dụ

Gợi ý luồng implementation:

- thêm cột `search_vector` cho `pages`
- tạo GIN index
- bật `pg_trgm`
- rank theo title/tags/excerpt/body
- log search query để quan sát behavior

Query flow:

- user search
- backend validate quyền
- Postgres trả result
- backend post-process ranking / snippets
- UI render results

## Lưu ý & Pitfalls

- Đừng dùng vector search một mình nếu query có keyword rõ.
- Đừng để DB search không theo sync; kết quả sẽ lệch.
- Đừng bỏ ACL ở tầng search.
- Đừng phụ thuộc runtime vào đọc file markdown nếu DB đã có.

## Liên quan

- [[nextjs-fastapi-supabase-architecture]] — kiến trúc tổng cho stack app
- [[hybrid-search]] — chiến lược search khi wiki lớn
- [[ai-coding-workflows]] — workflow build/verify với AI
- [[knowledge-base]] — nền tảng knowledge retrieval
- [[rag]] — khi muốn thêm semantic layer

## Nguồn

- https://www.postgresql.org/docs/
- https://supabase.com/docs
