---
title: "Skill Graph"
topic: "AI Coding Workflows"
tags: [skill-graph, learning-path, tracking, personalization]
created: 2026-04-20
updated: 2026-04-20
confidence: low
sources:
  - https://www.anthropic.com/learn/build-with-claude
  - https://cursor.com/blog/agent-best-practices
---

# Skill Graph

## Tóm tắt

Skill graph là cách biểu diễn các kỹ năng, chủ đề, và mức độ nắm vững của người học dưới dạng graph để gợi ý lộ trình học tiếp theo. Trong AI Coding Wiki, skill graph giúp track tiến độ học và đề xuất topic còn thiếu.

## Nội dung chính

Skill graph có thể gồm:

- Node: skill, concept, tool, workflow
- Edge: prerequisite, related, next-step, review-needed
- Metadata: level, confidence, last-reviewed, source coverage

### Mục tiêu

- Biết user/team đang học tới đâu
- Phát hiện skill nào còn gap
- Gợi ý topic tiếp theo phù hợp
- Dùng cho tutor/chat agent để cá nhân hóa trả lời

### Cách biểu diễn

Skill graph có thể được build từ:
- wiki topics và pages
- tags trong front matter
- query history
- learned topics theo user

## Thực hành / Ví dụ

- Nếu user đã đọc `vibe-coding` và `ai-agents`, gợi ý tiếp `prompt-engineering` hoặc `ai-coding-workflows`.
- Nếu user mới học `cursor-agent`, đề xuất `plan-mode` và `evals`.

## Lưu ý & Pitfalls

- Skill graph quá chi tiết sẽ khó duy trì.
- Nếu không có tín hiệu thật từ hành vi user, graph dễ thành danh sách tĩnh.
- Nên bắt đầu từ topic-level trước, không cần model quá phức tạp.

## Liên quan

- [[ai-coding-workflows]] — nền workflow để track skill progress
- [[tutor-agent]] — agent có thể dùng skill graph để cá nhân hóa
- [[prompt-library]] — giúp học theo pattern thực chiến
- [[evals]] — kiểm tra tiến bộ qua bài test / challenge

## Nguồn

- https://www.anthropic.com/learn/build-with-claude
- https://cursor.com/blog/agent-best-practices
