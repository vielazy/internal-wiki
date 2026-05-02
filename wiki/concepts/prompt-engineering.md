---
title: "Prompt Engineering"
topic: "Prompt Engineering"
tags: [prompt-engineering, prompts, claude, best-practices]
created: 2026-04-20
updated: 2026-04-20
confidence: medium
sources:
  - https://www.anthropic.com/learn/build-with-claude
  - https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview
  - https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices
  - https://github.com/anthropics/courses/blob/master/prompt_engineering_interactive_tutorial/README.md
  - https://github.com/anthropics/courses/blob/master/real_world_prompting/README.md
---

# Prompt Engineering

## Tóm tắt

Prompt engineering là kỹ thuật thiết kế instruction để LLM hiểu đúng mục tiêu, format, và ràng buộc của task. Với Claude/agent workflows, trọng tâm hiện nay là structured prompts, model-specific best practices, và iterative evaluation.

## Nội dung chính

Các nguồn Anthropic cho thấy prompt tốt thường có các đặc điểm:

- Mục tiêu rõ ràng, không mơ hồ
- Output format cụ thể
- Ràng buộc và tiêu chí thành công minh bạch
- Có ví dụ hoặc tutorial khi task phức tạp
- Tùy chỉnh theo model và use case

Prompt engineering không chỉ là viết câu hay hơn. Nó là cách tạo điều kiện để model thực hiện task ổn định hơn, đặc biệt khi prompt được dùng trong agent loop hoặc production workflow.

## Thực hành / Ví dụ

- Viết rõ đầu ra mong muốn thay vì chỉ mô tả chung chung.
- Nếu task phức tạp, chia thành steps hoặc cung cấp rubric.
- Dùng tutorial thực hành để benchmark prompt trên nhiều trường hợp.
- Khi prompt dùng cho agent, thêm guardrails và verification step.

## Lưu ý & Pitfalls

- Prompt dài không đồng nghĩa prompt tốt.
- Một prompt tốt cho model này có thể kém hơn trên model khác.
- Không nên bỏ qua eval; cảm giác "có vẻ ổn" thường không đủ.

## Liên quan

- [[ai-agents]] — prompt là lớp điều khiển agent behavior
- [[vibe-coding]] — vibe coding phụ thuộc mạnh vào prompt chất lượng
- [[prompt-templates]] — các mẫu prompt tái sử dụng
- [[evals]] — đo hiệu quả của prompt theo dữ liệu thật

## Nguồn

- https://www.anthropic.com/learn/build-with-claude
- https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview
- https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices
- https://github.com/anthropics/courses/blob/master/prompt_engineering_interactive_tutorial/README.md
- https://github.com/anthropics/courses/blob/master/real_world_prompting/README.md
