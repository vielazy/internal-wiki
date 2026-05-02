---
title: "Tool Use"
topic: "AI Agents"
tags: [tool-use, function-calling, agents, orchestration]
created: 2026-04-20
updated: 2026-04-20
confidence: medium
sources:
  - https://docs.anthropic.com/en/docs/build-with-claude/tool-use/overview
  - https://www.anthropic.com/learn/build-with-claude
  - https://cursor.com/blog/agent-best-practices
---

# Tool Use

## Tóm tắt

Tool use là cơ chế cho phép LLM/agent gọi công cụ bên ngoài để lấy dữ liệu, thực hiện hành động, hoặc kiểm chứng kết quả. Đây là nền tảng quan trọng của agentic coding và multi-step workflows.

## Nội dung chính

Một agent có tool use tốt thường có các đặc điểm:

- Biết khi nào cần gọi tool thay vì đoán
- Có schema rõ cho input/output của tool
- Có bước xác nhận hoặc verify sau khi tool trả kết quả
- Giới hạn quyền của tool theo task

Tool use thường đi kèm với planning và orchestration. Model không chỉ tạo text, mà còn điều phối hành động qua tools.

## Thực hành / Ví dụ

- Dùng tool để search codebase thay vì yêu cầu model nhớ mọi thứ.
- Dùng terminal hoặc test runner để verify output trước khi trả lời.
- Tách tool cho read-only vs write actions.

## Lưu ý & Pitfalls

- Tool quá mạnh mà không có guardrails sẽ nguy hiểm.
- Nếu không kiểm tra tool results, agent có thể tin vào dữ liệu sai.
- Khi prompt không rõ, agent có thể gọi tool sai thời điểm.

## Liên quan

- [[ai-agents]] — tool use là capability cốt lõi của agents
- [[mcp]] — protocol thường dùng để expose tools
- [[vibe-coding]] — coding with AI dựa mạnh vào tool-enabled agents

## Nguồn

- https://docs.anthropic.com/en/docs/build-with-claude/tool-use/overview
- https://www.anthropic.com/learn/build-with-claude
- https://cursor.com/blog/agent-best-practices
