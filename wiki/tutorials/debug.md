---
title: "Debug workflow"
topic: "AI Coding Workflows"
tags: [tutorial, debug, bug-fix, troubleshooting, agent]
created: 2026-04-28
updated: 2026-04-28
confidence: medium
sources:
  - https://docs.anthropic.com/en/docs/claude-code/overview
  - https://docs.anthropic.com/en/docs/build-with-claude/develop-tests
  - https://cursor.com/blog/agent-best-practices
visibility: public
---

# Debug workflow

## Tóm tắt

Debug workflow là cách tiếp cận có hệ thống để tìm nguyên nhân gốc của lỗi, tái hiện lỗi, sửa đúng chỗ, và xác minh fix bằng test hoặc run thực tế. Mục tiêu là tránh sửa theo triệu chứng rồi tạo thêm lỗi mới.

## Nội dung chính

Một vòng debug hiệu quả thường gồm:

1. Ghi lại triệu chứng thật rõ
2. Tìm bước tái hiện ổn định
3. Xác định phạm vi file / module liên quan
4. Kiểm tra log, lint, type error, test failure
5. Tìm root cause thay vì chữa cháy
6. Sửa tối thiểu để không phá hành vi tốt hiện tại
7. Chạy lại test / lint / app
8. Ghi nhận kết quả sau fix

Trong workflow có agent, nên để agent đọc:

- error message
- stack trace
- file liên quan
- code path xung quanh

sau đó yêu cầu nó đề xuất root cause và fix plan trước khi sửa.

## Thực hành / Ví dụ

Cách làm thực dụng:

- Nếu lỗi runtime: reproduce bằng đúng input gây lỗi
- Nếu lỗi build/type: chạy lại lệnh kiểm tra để lấy full trace
- Nếu lỗi logic: viết scenario nhỏ mô tả input → expected → actual
- Nếu lỗi sau refactor: so sánh diff cũ/mới để tìm invariant bị phá

Nên ưu tiên sửa theo thứ tự:

- lỗi chặn chạy
- lỗi gây sai dữ liệu
- lỗi làm giảm trải nghiệm
- lỗi hygiene / minor polish

## Lưu ý & Pitfalls

- Đừng sửa nhiều thứ cùng lúc nếu chưa biết root cause.
- Đừng bỏ qua log chỉ vì nhìn giống "noise".
- Nếu fix xong nhưng chưa verify, coi như chưa xong.
- Lỗi dễ tái phát nếu không ghi lại pattern và guardrail.

## Liên quan

- [[evals]] — debug cần tiêu chí để xác minh fix
- [[review]] — sau debug nên review diff để tránh regression
- [[ai-coding-workflows]] — debug là một phần của workflow AI coding
- [[bat-dau-vibe-coding]] — vibe coding cần kiểm tra sớm để debug nhanh
- [[claude-code]] — debug thường đi kèm tool-assisted coding

## Nguồn

- https://docs.anthropic.com/en/docs/claude-code/overview
- https://docs.anthropic.com/en/docs/build-with-claude/develop-tests
- https://cursor.com/blog/agent-best-practices
