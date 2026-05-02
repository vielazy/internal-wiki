---
title: "Review workflow"
topic: "AI Coding Workflows"
tags: [tutorial, review, diff, code-review, agent]
created: 2026-04-28
updated: 2026-04-28
confidence: medium
sources:
  - https://cursor.com/blog/agent-best-practices
  - https://www.anthropic.com/learn/build-with-claude
  - https://docs.anthropic.com/en/docs/claude-code/overview
visibility: public
---

# Review workflow

## Tóm tắt

Review workflow là cách dùng AI agent để đọc diff, phát hiện vấn đề logic, kiểm tra scope, và giảm rủi ro trước khi merge. Mục tiêu không chỉ là tìm bug, mà còn xác nhận rằng thay đổi vẫn bám đúng brief và không làm lệch kiến trúc.

## Nội dung chính

Một review tốt thường đi theo chuỗi:

1. Xác định mục tiêu của thay đổi
2. Đọc diff và phần code liên quan
3. Kiểm tra tính nhất quán với kiến trúc hiện tại
4. Tìm lỗi logic, edge cases, và regression risk
5. Xác nhận test/lint/run coverage
6. Tổng kết mức độ rủi ro và đề xuất fix

Khi dùng agent để review, nên ưu tiên các câu hỏi cụ thể như:

- Diff này có đúng với mục tiêu ban đầu không?
- Có chỗ nào phá invariants hiện tại không?
- Có import, component, hay function nào bị lặp không?
- Có thiếu test cho đường đi quan trọng không?
- Có gì làm giảm maintainability về sau không?

Review workflow đặc biệt hữu ích khi dự án dùng nhiều tự động hóa, vì agent có thể tạo diff đúng cú pháp nhưng sai ý đồ.

## Thực hành / Ví dụ

Một review loop thực dụng:

- Agent tạo thay đổi
- Human hoặc agent khác đọc diff
- Tách review thành 3 lớp:
  - correctness
  - architecture
  - maintainability
- Ghi lại các issue theo mức độ:
  - blocker
  - should-fix
  - nice-to-have

Nếu review chỉ nói chung chung như "looks good", nó gần như không có giá trị. Nên yêu cầu review nêu rõ file, đoạn logic, và lý do.

## Lưu ý & Pitfalls

- Không review bằng cảm giác, phải bám diff cụ thể.
- Đừng để review quá rộng; chia theo module hoặc feature.
- Nếu thay đổi lớn, nên review sau từng lát nhỏ thay vì đợi cuối.
- Review phải kiểm tra cả side effects, không chỉ nhìn code mới.

## Liên quan

- [[bat-dau-vibe-coding]] — review là một checkpoint quan trọng trong vibe coding
- [[evals]] — review cần tiêu chí rõ ràng để so sánh baseline và new diff
- [[ai-coding-workflows]] — review là một bước trong workflow code với AI
- [[claude-code]] — workflow review thường đi cùng agentic coding
- [[cursor-agent]] — có thể dùng agent để hỗ trợ đọc diff và phản biện

## Nguồn

- https://cursor.com/blog/agent-best-practices
- https://www.anthropic.com/learn/build-with-claude
- https://docs.anthropic.com/en/docs/claude-code/overview
