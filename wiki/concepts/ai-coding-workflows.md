---
title: "AI Coding Workflows"
topic: "AI Coding Workflows"
tags: [workflow, planning, review, testing, ai-coding]
created: 2026-04-20
updated: 2026-04-20
confidence: medium
sources:
  - https://cursor.com/blog/agent-best-practices
  - https://www.anthropic.com/learn/build-with-claude
  - https://docs.anthropic.com/en/docs/build-with-claude/develop-tests
---

# AI Coding Workflows

## Tóm tắt

AI coding workflows là tập hợp các bước để dùng LLM/agent hiệu quả khi lập trình: plan, context gathering, implement, verify, review, và lặp lại. Đây là lớp thực hành giúp vibe coding trở nên ổn định và có thể kiểm soát.

## Nội dung chính

Một workflow tốt thường gồm:

- Xác định mục tiêu và ràng buộc
- Cho agent tìm context liên quan
- Tạo plan trước khi code với task lớn
- Implement theo step nhỏ
- Chạy tests/lint/review sau mỗi thay đổi
- Ghi lại kết quả để dùng lại về sau

## Thực hành / Ví dụ

- Với feature mới, bắt đầu bằng plan mode hoặc prompt yêu cầu plan.
- Với bug, yêu cầu agent điều tra nguyên nhân gốc và verify fix bằng test.
- Với refactor, giữ diff nhỏ và kiểm tra mọi thay đổi bằng lint/test.

## Lưu ý & Pitfalls

- Không verify thì AI coding dễ trông đúng nhưng sai ngầm.
- Context quá rộng làm agent mất focus.
- Workflow thiếu checkpoints thường dẫn đến diff lớn và khó review.

## Liên quan

- [[vibe-coding]] — bối cảnh làm việc với AI để code
- [[agent-patterns]] — nền tảng kiến trúc cho workflow agentic
- [[plan-mode]] — pattern plan-first cho task lớn
- [[evals]] — kiểm chứng output của workflow

## Nguồn

- https://cursor.com/blog/agent-best-practices
- https://www.anthropic.com/learn/build-with-claude
- https://docs.anthropic.com/en/docs/build-with-claude/develop-tests
