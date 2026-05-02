---
title: "Project Priority Plan"
topic: "AI Coding Workflows"
tags: [planning, priorities, roadmap, wiki-ops]
created: 2026-04-28
updated: 2026-04-28
confidence: high
sources:
  - ../LOG.md
  - ../../AI_CODING_WIKI_GUIDE.md
  - ../../CLAUDE.md
  - ../../AGENTS.md
  - ../../PROJECT_PRIORITY_PLAN.md
visibility: public
---

# Project Priority Plan

## Tóm tắt

Trang này tóm tắt thứ tự ưu tiên hiện tại của dự án theo tác động: việc nào cần làm ngay, việc nào làm sau khi nền tảng đã ổn, và việc nào để sau cùng.

## Nội dung chính

### Impact cao

- Hoàn thiện search trên PostgreSQL
- Chuẩn hóa sync markdown → PostgreSQL
- Enforce permissions / ACL ở runtime
- Giữ tài liệu điều hướng nhất quán giữa `README.md`, `AI_CODING_WIKI_GUIDE.md`, `CLAUDE.md`, `AGENTS.md`

### Impact medium

- Bổ sung các page gap quan trọng như `review`, `debug`, `tdd`, `plan-mode`
- Mở rộng `tutorials/` với các tutorial thực chiến
- Tách rõ log authoring và log runtime
- Thêm revision history khi content thay đổi nhiều
- Mở rộng Obsidian workflow nếu cần

### Để sau

- Semantic / embedding search full scale
- Dashboard/UI lớn
- Multi-agent orchestration nâng cao
- Automation mở rộng chưa có nhu cầu rõ
- Productization enterprise quá sâu

## Thực hành / Ví dụ

Khi quyết định việc tiếp theo, ưu tiên:
1. search
2. sync
3. ACL
4. điều hướng tài liệu
5. page gap và tutorial

## Lưu ý & Pitfalls

- Đừng ưu tiên semantic search trước khi lexical search và trigram đã ổn
- Đừng làm UI lớn nếu backend/search/sync còn yếu
- Đừng để Obsidian bị hiểu nhầm là runtime search backend
- Đừng viết nội dung runtime trực tiếp vào DB

## Liên quan
- [[ai-coding-workflows]] — đây là bản điều hướng thực thi theo workflow
- [[knowledge-base]] — nền tảng knowledge base của dự án
- [[rag]] — hướng semantic retrieval có thể bổ sung sau
- [[tutor-agent]] — agent đọc wiki và trả lời theo ngữ cảnh

## Nguồn
- ../../AI_CODING_WIKI_GUIDE.md
- ../../CLAUDE.md
- ../../AGENTS.md
- ../../PROJECT_PRIORITY_PLAN.md
- ../LOG.md
