---
title: "Vibe Coding"
topic: "Vibe Coding"
tags: [vibe-coding, agentic-coding, cursor, claude-code]
created: 2026-04-20
updated: 2026-04-20
confidence: medium
sources:
  - https://cursor.com/blog/agent-best-practices
  - https://cursor.com/blog/cursor-3
  - https://cursor.com/blog/scaling-agents
  - https://cursor.com/blog/self-driving-codebases
  - https://www.anthropic.com/learn/build-with-claude
---

# Vibe Coding

## Tóm tắt

Vibe coding là cách làm software trong đó AI agent đóng vai trò driver thực thi, còn human đóng vai trò director: đặt mục tiêu, kiểm tra kế hoạch, review kết quả. Cách làm này nhấn mạnh plan-first, context management, và verification loop.

## Nội dung chính

Các nguồn gần đây cho thấy vibe coding không còn chỉ là "prompt rồi nhận code". Workflow hiệu quả thường có các thành phần sau:

- Agent harness rõ ràng: instructions, tools, model
- Bắt đầu bằng plan trước khi code
- Để agent tự tìm context thay vì nhồi quá nhiều file
- Chia nhỏ task và dùng review loop sau mỗi bước
- Dùng parallel agents hoặc cloud agents cho task lớn

Cursor mô tả một interface centered around agents, cho thấy trải nghiệm coding đang chuyển từ editor-centric sang agent-centric.

Anthropic cũng đẩy mạnh các workflow liên quan đến Claude Code, tool use, skills, và agent patterns.

## Thực hành / Ví dụ

- Với task lớn, hãy yêu cầu agent tạo plan trước.
- Chỉ định rõ file canonical hoặc pattern cần theo.
- Sau khi agent sửa xong, chạy review và lint trước khi merge.
- Nếu agent đi sai hướng, quay lại plan thay vì cố sửa dần bằng prompt ngắn.

## Lưu ý & Pitfalls

- Không nên xem vibe coding là cách bỏ qua review; ngược lại review càng quan trọng hơn.
- Nhồi quá nhiều context có thể làm agent nhiễu và kém tập trung.
- Task lớn mà không có plan thường tạo ra diff khó kiểm soát.

## Liên quan

- [[ai-agents]] — vibe coding thường dựa trên agent harness và tool use
- [[ai-coding-workflows]] — workflow tổng quát để plan, build, verify với AI
- [[prompt-engineering]] — prompt rõ ràng giúp agent làm việc tốt hơn
- [[cursor-agent]] — ví dụ thực tế về agent-centric coding trong IDE
- [[claude-code]] — workflow và tooling liên quan đến Claude Code

## Nguồn

- https://cursor.com/blog/agent-best-practices
- https://cursor.com/blog/cursor-3
- https://cursor.com/blog/scaling-agents
- https://cursor.com/blog/self-driving-codebases
- https://www.anthropic.com/learn/build-with-claude
