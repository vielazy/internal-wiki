---
title: "TDD workflow"
topic: "AI Coding Workflows"
tags: [tutorial, tdd, testing, quality, agent]
created: 2026-04-28
updated: 2026-04-28
confidence: medium
sources:
  - https://docs.anthropic.com/en/docs/build-with-claude/develop-tests
  - https://www.anthropic.com/learn/build-with-claude
visibility: public
---

# TDD workflow

## Tóm tắt

TDD workflow là cách viết test trước hoặc ít nhất là đặt tiêu chí kiểm chứng trước khi implement, để code bám đúng hành vi mong muốn. Trong môi trường AI coding, TDD giúp agent không đi quá xa khỏi yêu cầu và giảm số vòng sửa lỗi sau đó.

## Nội dung chính

Một vòng TDD cơ bản gồm:

1. Viết test cho hành vi mong muốn
2. Chạy test để thấy fail
3. Implement tối thiểu để test pass
4. Refactor mà không làm test hỏng
5. Lặp lại với hành vi tiếp theo

TDD hữu ích đặc biệt khi:

- feature có nhiều edge case
- logic dễ regression
- muốn agent không tự phát minh behavior mới
- cần confidence cao trước khi merge

Trong AI coding, không nhất thiết mọi thứ đều phải TDD cứng nhắc. Nhưng ít nhất nên có:

- test hoặc check cho luồng quan trọng
- acceptance criteria rõ ràng
- verification step sau mỗi thay đổi lớn

## Thực hành / Ví dụ

Cách áp dụng đơn giản:

- xác định hành vi nhỏ nhất có thể test
- viết tên test mô tả rõ outcome
- giữ test gần feature code
- nếu chưa viết test tự động được thì viết checklist verify thủ công

Với agent, nên yêu cầu:

- nêu test cases trước khi code
- sau code phải chạy lại test
- báo rõ test nào pass/fail

## Lưu ý & Pitfalls

- Đừng viết test quá rộng ngay từ đầu.
- Đừng coi TDD là cản trở tốc độ; nó thường giảm vòng sửa về sau.
- Nếu test không mô tả behavior thật, test pass cũng vô nghĩa.
- TDD kém hiệu quả nếu requirements chưa rõ.

## Liên quan

- [[evals]] — TDD và eval đều cần tiêu chí kiểm chứng rõ
- [[review]] — sau khi pass test vẫn nên review diff
- [[debug]] — debug dùng test để tái hiện và xác minh fix
- [[ai-coding-workflows]] — TDD là một workflow quan trọng khi code với AI
- [[bat-dau-vibe-coding]] — tutorial này khuyến nghị verify sớm, TDD là một cách làm điều đó

## Nguồn

- https://docs.anthropic.com/en/docs/build-with-claude/develop-tests
- https://www.anthropic.com/learn/build-with-claude
