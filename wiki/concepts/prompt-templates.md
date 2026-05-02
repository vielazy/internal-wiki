---
title: "Prompt Templates"
topic: "Prompt Engineering"
tags: [prompt-templates, prompts, reusable-patterns]
created: 2026-04-20
updated: 2026-04-20
confidence: low
sources:
  - https://www.anthropic.com/learn/build-with-claude
  - https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview
---

# Prompt Templates

## Tóm tắt

Prompt templates là các mẫu prompt tái sử dụng để chuẩn hóa cách giao task cho LLM hoặc agent. Chúng hữu ích khi team muốn giữ format ổn định, giảm noise, và dễ review hơn.

## Nội dung chính

Một prompt template thường gồm:

- Role / mục tiêu
- Context cần thiết
- Ràng buộc / guardrails
- Output format
- Tiêu chí thành công

Trong thực hành agentic coding, prompt templates giúp giảm lệ thuộc vào prompt ad hoc, đặc biệt cho các workflow lặp lại như review code, generate tests, hoặc create plans.

## Thực hành / Ví dụ

- Tạo template cho các task lặp lại như bug fix, code review, hoặc viết test.
- Đặt placeholders cho biến đầu vào.
- Giữ template ngắn nhưng đủ thông tin để agent không phải đoán.

## Lưu ý & Pitfalls

- Template quá dài có thể làm mất tính linh hoạt.
- Template tốt cho one-shot task chưa chắc tốt cho agent loop.
- Nếu team không có convention, templates dễ bị trôi theo thời gian.

## Liên quan

- [[prompt-engineering]] — nền tảng cho việc thiết kế templates
- [[ai-agents]] — prompt templates thường dùng trong agent workflows
- [[vibe-coding]] — templates giúp giao task cho coding agents nhất quán hơn

## Nguồn

- https://www.anthropic.com/learn/build-with-claude
- https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview
