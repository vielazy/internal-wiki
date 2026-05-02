---
title: "Wiki Architecture Map"
topic: "Knowledge Ops & Productization"
tags: [synthesis, architecture, map, guide, priorities, wiki]
created: 2026-04-28
updated: 2026-04-28
confidence: medium
sources:
  - AI_CODING_WIKI_GUIDE.md
  - PROJECT_PRIORITY_PLAN.md
  - CLAUDE.md
  - AGENTS.md
visibility: public
---

# Wiki Architecture Map

## Tóm tắt

Đây là bản đồ điều hướng cấp cao cho toàn dự án AI Coding Wiki. Mục tiêu là giúp human và LLM biết đọc file nào trước, hiểu vai trò của từng lớp tài liệu, và tránh lẫn giữa content source, priority plan, và runtime rules.

## Bản đồ tài liệu

### 1) AI_CODING_WIKI_GUIDE.md

Master guide của toàn repo.

Nó trả lời các câu hỏi:
- hệ thống này là gì
- source of truth là gì
- Obsidian đóng vai trò gì
- PostgreSQL dùng để làm gì
- policy về sync, search, permissions, logs là gì

### 2) PROJECT_PRIORITY_PLAN.md

Tài liệu ưu tiên hành động.

Nó trả lời:
- việc nào impact cao
- việc nào làm sau
- thứ tự thực thi hợp lý
- hiện trạng project nên đi theo hướng nào

### 3) CLAUDE.md và AGENTS.md

Entrypoint theo tool.

Chúng trả lời:
- agent nào nên đọc file nào
- quy tắc làm việc khi sửa repo
- page template
- logging policy
- search/runtime policy

### 4) wiki/

Knowledge base output.

Gồm:
- concepts
- tools
- tutorials
- agents
- code-patterns
- syntheses

Đây là lớp nội dung mà LLM duy trì và mở rộng.

### 5) outputs/

Nơi lưu query results, digest, lint outputs, và các bản record phát sinh.

### 6) raw/

Nguồn thô immutable.

Không sửa trực tiếp bằng LLM.

## Luồng làm việc đề xuất

1. Đọc `AI_CODING_WIKI_GUIDE.md`
2. Đọc `PROJECT_PRIORITY_PLAN.md`
3. Đọc `CLAUDE.md` hoặc `AGENTS.md` tùy tool
4. Với câu hỏi về content, đọc `wiki/INDEX.md`
5. Với việc sửa nội dung, cập nhật page trong `wiki/`
6. Nếu thay đổi ảnh hưởng runtime, sync sang PostgreSQL
7. Ghi log vào `wiki/LOG.md` hoặc output file phù hợp

## Khi nào đọc file nào

### Khi muốn hiểu kiến trúc
- đọc `AI_CODING_WIKI_GUIDE.md`
- đọc `wiki-architecture-map.md`

### Khi muốn biết việc nào làm trước
- đọc `PROJECT_PRIORITY_PLAN.md`

### Khi muốn thực thi theo tool
- đọc `CLAUDE.md` hoặc `AGENTS.md`

### Khi muốn tra cứu tri thức
- đọc `wiki/INDEX.md`
- rồi mở các page liên quan

## Pitfalls thường gặp

- Đọc wiki pages mà quên master guide → dễ lệch policy
- Chỉ nhìn priority plan mà quên rule source of truth → dễ sửa sai layer
- Nhầm Obsidian search với runtime search → dễ thiết kế sai backend
- Quên ACL khi retrieval → dễ leak nội dung riêng tư

## Liên quan

- [[ai-coding-wiki-guide]] — master policy của toàn repo
- [[project-priority-plan]] — thứ tự việc cần làm
- [[supabase-auth-acl-model]] — mô hình quyền cho internal wiki
- [[supabase-postgresql-search]] — search strategy trên DB
- [[nextjs-fastapi-supabase-architecture]] — kiến trúc app tổng

## Nguồn

- AI_CODING_WIKI_GUIDE.md
- PROJECT_PRIORITY_PLAN.md
- CLAUDE.md
- AGENTS.md
