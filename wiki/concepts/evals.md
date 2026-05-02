---
title: "Evaluations"
topic: "AI Coding Workflows"
tags: [evals, evaluation, testing, quality]
created: 2026-04-20
updated: 2026-04-20
confidence: medium
sources:
  - https://www.anthropic.com/learn/build-with-claude
  - https://docs.anthropic.com/en/docs/build-with-claude/develop-tests
  - https://docs.anthropic.com/en/docs/test-and-evaluate/eval-tool
---

# Evaluations

## Tóm tắt

Evaluations là cách đo chất lượng output của LLM/agent bằng tiêu chí hoặc dataset rõ ràng, thay vì dựa vào cảm giác chủ quan. Trong AI coding workflows, evals là lớp kiểm chứng quan trọng để biết agent, prompt, hoặc retrieval có thực sự tốt lên hay không.

## Nội dung chính

Anthropic đặt evaluations như một phần của vòng lặp build with Claude:

- Có structured tests cho output nhất quán
- Dùng eval tool để kiểm tra behavior
- Đánh giá riêng retrieval, generation, và end-to-end workflow
- Lặp lại sau mỗi thay đổi quan trọng

Evals đặc biệt quan trọng khi làm agentic systems vì một diff trông hợp lý vẫn có thể sai về logic, coverage, hoặc safety.

## Thực hành / Ví dụ

- Tạo test cases đại diện cho các tình huống quan trọng.
- Định nghĩa pass/fail criteria trước khi chạy.
- So sánh baseline và new version bằng cùng một bộ eval.

## Lưu ý & Pitfalls

- Evals mơ hồ sẽ không giúp ra quyết định.
- Chỉ đo output cuối cùng có thể bỏ sót lỗi ở retrieval hoặc intermediate steps.
- Nên tránh overfitting vào một bộ test nhỏ.

## Liên quan

- [[ai-coding-workflows]] — evals là một phần của workflow tốt khi code với AI
- [[rag]] — cần eval riêng cho retrieval
- [[prompt-engineering]] — eval giúp so sánh prompt variants

## Nguồn

- https://www.anthropic.com/learn/build-with-claude
- https://docs.anthropic.com/en/docs/build-with-claude/develop-tests
- https://docs.anthropic.com/en/docs/test-and-evaluate/eval-tool
