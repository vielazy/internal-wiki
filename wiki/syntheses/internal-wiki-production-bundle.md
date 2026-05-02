---
title: "Internal Wiki Production Bundle"
topic: "Knowledge Ops & Productization"
tags: [bundle, internal-wiki, production, architecture, search, acl, sync]
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

# Internal Wiki Production Bundle

## Tóm tắt

Đây là bundle đọc nhanh cho toàn bộ lớp production của AI Coding Wiki. Nếu muốn hiểu cách dự án này nên đi vào internal production, đọc theo thứ tự bundle này sẽ cho cái nhìn đủ nhanh mà không phải mở quá nhiều page rời rạc.

## Reading order

### 1) Wiki architecture map
- [[wiki-architecture-map]]

Bản đồ điều hướng cấp cao cho toàn dự án.

### 2) Production recommendation
- [[internal-wiki-architecture-recommendation]]

Khuyến nghị kiến trúc production tổng thể.

### 3) Production checklist
- [[internal-wiki-production-checklist]]

Checklist triển khai theo lớp.

### 4) Auth / ACL / RLS flow
- [[supabase-auth-rls-backend-acl-flow]]

Flow end-to-end cho auth, ACL, và RLS.

### 5) ACL model
- [[supabase-auth-acl-model]]

Mô hình quyền cấp cơ bản cho internal wiki.

### 6) RLS vs app-layer ACL
- [[supabase-rls-vs-app-layer-acl]]

So sánh hai lớp quyền khác nhau.

### 7) Search strategy
- [[supabase-postgresql-search]]

Chiến lược search runtime trên Supabase/PostgreSQL.

## Ý nghĩa của bundle này

Bundle này giúp:
- human đọc kiến trúc production nhanh hơn
- LLM chọn đúng context page khi trả lời câu hỏi về runtime/internal wiki
- giảm việc phải đọc từng trang rời rạc
- giữ các chủ đề production có thứ tự logic

## Khi nào dùng bundle này

Dùng khi:
- cần review kiến trúc production
- cần giải thích flow auth/search/ACL/sync
- cần hiểu roadmap lên internal wiki
- cần định hướng làm tiếp theo cho runtime layer

## Liên quan

- [[wiki-architecture-map]] — bản đồ điều hướng chính
- [[internal-wiki-architecture-recommendation]] — khuyến nghị production tổng thể
- [[internal-wiki-production-checklist]] — checklist triển khai
- [[supabase-auth-rls-backend-acl-flow]] — flow auth + ACL + RLS
- [[supabase-postgresql-search]] — search strategy trong DB
- [[project-priority-plan]] — thứ tự việc cần làm

## Nguồn

- AI_CODING_WIKI_GUIDE.md
- PROJECT_PRIORITY_PLAN.md
- https://supabase.com/docs
- https://www.postgresql.org/docs/
