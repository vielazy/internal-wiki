---
title: "Cursor Agent"
topic: "LLM Tools & Platforms"
tags: [cursor, agent, ide, coding-assistant]
created: 2026-04-20
updated: 2026-04-20
confidence: medium
sources:
  - https://cursor.com/blog/agent-best-practices
  - https://cursor.com/blog/2-0
  - https://cursor.com/blog/plan-mode
---

# Cursor Agent

## Tóm tắt

Cursor Agent là coding assistant trong IDE được thiết kế theo hướng agent-centric: nó tìm context, tạo plan, sửa code, và lặp lại với review/verification loop. Đây là một trong những công cụ tiêu biểu nhất cho vibe coding hiện đại.

## Nội dung chính

Các điểm nổi bật từ nguồn Cursor:

- Agent harness gồm instructions, tools, model
- Plan Mode cho phép nghiên cứu và chờ duyệt trước khi build
- Context retrieval bằng search tools thay vì nhồi file thủ công
- Hỗ trợ parallel agents, cloud agents, và worktrees
- Có review flow để kiểm tra diff sau khi agent hoàn tất

Cursor chuyển dần trải nghiệm từ editor-centric sang agent-centric, nghĩa là UI và workflow xoay quanh việc giao việc cho agent thay vì chỉ gõ code trực tiếp.

## Thực hành / Ví dụ

- Dùng Plan Mode cho refactor lớn hoặc feature mới.
- Để agent tự tìm file liên quan khi bạn chưa chắc file canonical.
- Chạy review pass sau khi agent xong để kiểm tra logic và edge cases.

## Lưu ý & Pitfalls

- Agent mạnh không đồng nghĩa với việc bỏ review.
- Nếu prompt quá rộng, agent có thể chọn sai hướng.
- Task lớn nên tách thành plan và execution.

## Liên quan

- [[vibe-coding]] — Cursor là ví dụ thực tế cho vibe coding workflow
- [[ai-agents]] — Cursor agent là implementation của agent harness
- [[ai-coding-workflows]] — Cursor hỗ trợ workflow plan/build/verify
- [[plan-mode]] — pattern plan-first được Cursor chính thức hóa

## Nguồn

- https://cursor.com/blog/agent-best-practices
- https://cursor.com/blog/2-0
- https://cursor.com/blog/plan-mode
