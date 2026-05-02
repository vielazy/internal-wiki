---
title: "AI Agents"
topic: "AI Agents"
tags: [ai-agents, tool-use, mcp, skills, orchestration]
created: 2026-04-20
updated: 2026-04-20
confidence: medium
sources:
  - https://www.anthropic.com/learn/build-with-claude
  - https://docs.anthropic.com/en/docs/build-with-claude/tool-use/overview
  - https://modelcontextprotocol.io/introduction
  - https://www.anthropic.com/engineering/building-effective-agents
  - https://cursor.com/blog/agent-best-practices
---

# AI Agents

## Tóm tắt

AI agents là hệ thống LLM có khả năng plan, dùng tools, và lặp lại hành động để hoàn thành task phức tạp. Các building blocks quan trọng gồm tool use, context management, memory, evaluation, và orchestration.

## Nội dung chính

Các nguồn chính thức hiện tập trung vào vài trục chính:

- Tool use: agent gọi external tools/API để lấy dữ liệu hoặc hành động
- Planning: agent cần bước lập kế hoạch trước khi thực thi
- MCP: chuẩn để kết nối agent với tools và systems bên ngoài
- Skills: cách đóng gói capability chuyên biệt để agent dùng khi cần
- Verification: agent cần tự kiểm tra output bằng tests, review, hoặc evals

Cursor nhấn mạnh agent harness gồm instructions, tools, và model. Anthropic mở rộng hệ sinh thái bằng Claude Code, MCP, và Skills.

## Thực hành / Ví dụ

- Dùng tool use khi agent cần dữ liệu realtime hoặc thao tác ngoài LLM.
- Dùng MCP để chuẩn hóa integration với server/tool bên ngoài.
- Thiết kế agent loop có bước verify rõ ràng sau khi act.
- Khi task dài, cho agent tạo plan và checkpoint theo từng phase.

## Lưu ý & Pitfalls

- Agent không phải chỉ là chat bot có function calling.
- Nếu tool surface quá rộng và không có guardrails, agent dễ làm sai.
- Thiếu evals khiến khó biết agent đang tốt lên hay xấu đi.

## Liên quan

- [[vibe-coding]] — agentic workflows là nền của vibe coding
- [[prompt-engineering]] — prompt tốt giúp agent hoạt động ổn định hơn
- [[mcp]] — chuẩn kết nối tools và services cho agents
- [[tool-use]] — cơ chế agent gọi công cụ bên ngoài

## Nguồn

- https://www.anthropic.com/learn/build-with-claude
- https://docs.anthropic.com/en/docs/build-with-claude/tool-use/overview
- https://modelcontextprotocol.io/introduction
- https://www.anthropic.com/engineering/building-effective-agents
- https://cursor.com/blog/agent-best-practices
