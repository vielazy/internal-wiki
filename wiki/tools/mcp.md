---
title: "Model Context Protocol (MCP)"
topic: "LLM Tools & Platforms"
tags: [mcp, protocol, tools, integrations]
created: 2026-04-20
updated: 2026-04-20
confidence: medium
sources:
  - https://modelcontextprotocol.io/introduction
  - https://modelcontextprotocol.io/specification
  - https://www.anthropic.com/news/model-context-protocol
---

# Model Context Protocol (MCP)

## Tóm tắt

MCP là protocol để kết nối LLM/agent với tools, data sources, và services bên ngoài theo cách chuẩn hóa. Nó giúp agent có thể truy cập context và hành động qua một interface nhất quán thay vì tích hợp riêng lẻ cho từng system.

## Nội dung chính

MCP giải quyết bài toán integration cho agentic workflows:

- Chuẩn hóa cách expose tools và resources
- Giảm nhu cầu viết custom connector cho từng app
- Hỗ trợ ecosystem plug-and-play giữa client và server
- Tạo nền cho agents truy cập dữ liệu nội bộ an toàn hơn

Trong wiki này, MCP được xem là một lớp hạ tầng quan trọng cho AI agents và coding assistants.

## Thực hành / Ví dụ

- Dùng MCP server để expose filesystem, docs, databases, hoặc internal APIs.
- Thiết kế server theo principle of least privilege.
- Tách rõ tool invocation khỏi model logic.

## Lưu ý & Pitfalls

- MCP không tự động làm agent tốt hơn; nó chỉ chuẩn hóa integration.
- Nếu server expose quá nhiều capability, rủi ro bảo mật tăng.
- Cần phân biệt context retrieval với execution tools.

## Liên quan

- [[ai-agents]] — agents thường dùng MCP để mở rộng tool access
- [[tool-use]] — MCP thường kết hợp với tool use trong agent loop

## Nguồn

- https://modelcontextprotocol.io/introduction
- https://modelcontextprotocol.io/specification
- https://www.anthropic.com/news/model-context-protocol
