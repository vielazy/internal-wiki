---
title: "Bắt đầu vibe coding"
topic: "Web & App Development"
tags: [tutorial, vibe-coding, cursor, claude-code, nextjs]
created: 2026-04-20
updated: 2026-04-20
confidence: medium
sources:
  - https://cursor.com/blog/agent-best-practices
  - https://cursor.com/blog/plan-mode
  - https://www.anthropic.com/learn/build-with-claude
  - https://docs.anthropic.com/en/docs/claude-code/overview
---

# Bắt đầu vibe coding

## Tóm tắt

Tutorial này hướng dẫn từ zero đến khi có một project chạy được bằng AI. Mục tiêu là dùng agent để tạo plan, scaffold app, verify bằng test/run, và lặp lại cho tới khi có bản đầu tiên usable.

## Chuẩn bị

Bạn cần:

- Một coding assistant như Cursor Agent hoặc Claude Code
- Một project trống hoặc repo mới
- Một mục tiêu nhỏ, rõ ràng, ví dụ: "tạo app ghi chú đơn giản"
- Thói quen review diff và chạy lint/test sau mỗi vòng

## Bước 1: Chọn scope nhỏ

Đừng bắt đầu bằng "build the next SaaS". Hãy chọn một app nhỏ có thể hoàn thành trong vài vòng:

- Todo app
- Note-taking app
- Landing page có form
- Mini dashboard đọc dữ liệu mock

Scope nhỏ giúp agent tập trung và giúp bạn kiểm tra nhanh hơn.

## Bước 2: Viết brief rõ ràng

Giao cho agent một brief ngắn nhưng cụ thể:

- App làm gì
- Những màn hình chính
- Dữ liệu mẫu nào cần có
- Stack mong muốn
- Tiêu chí hoàn thành

Ví dụ mục tiêu: tạo app Next.js + TypeScript + Tailwind với 1 trang danh sách note, 1 form thêm note, và lưu tạm trong state.

## Bước 3: Bắt đầu bằng plan

Theo best practices, hãy yêu cầu agent làm plan trước khi code.

Trong plan nên có:

- Cấu trúc file
- Các bước implementation
- Test hoặc kiểm tra cần chạy
- Điểm cần review thủ công

Nếu plan quá dài hoặc lan man, yêu cầu rút gọn lại trước khi thực thi.

## Bước 4: Để agent scaffold project

Yêu cầu agent:

- Tạo project structure
- Cài dependencies cần thiết
- Tạo component/page cơ bản
- Thiết lập scripts chạy dev/build/lint

Nếu bạn dùng Cursor, hãy để agent tự tìm context trong repo thay vì dán quá nhiều file.

## Bước 5: Chạy app sớm

Ngay khi có skeleton, yêu cầu agent chạy app và kiểm tra:

- Có build được không
- Có lỗi type/lint không
- Trang đầu có render không

Đây là điểm quan trọng của vibe coding: không chờ tới cuối mới test.

## Bước 6: Lặp từng lát nhỏ

Sau khi bản đầu chạy được:

- Thêm một feature nhỏ mỗi lần
- Mỗi lần sửa xong đều verify
- Dùng review để kiểm tra logic, layout, edge cases

Ví dụ thứ tự tốt:
1. Layout
2. Data model
3. Form
4. Persistence
5. Validation
6. Polish

## Bước 7: Dùng tool đúng chỗ

Một số nguyên tắc:

- Dùng search tool để tìm code thay vì nhớ bằng tay
- Dùng terminal hoặc test runner để xác minh
- Dùng plan mode cho task lớn
- Không để agent viết quá nhiều thứ cùng lúc

## Bước 8: Khi bị lệch hướng, quay lại plan

Nếu agent tạo ra diff không đúng ý:

- Dừng lại
- Sửa plan
- Chạy lại từ đầu

Đây thường nhanh hơn việc prompt thêm liên tục.

## Checklist hoàn thành

- [ ] Có project chạy được
- [ ] Có ít nhất 1 luồng end-to-end hoàn chỉnh
- [ ] Có lint/test pass
- [ ] Có review diff cuối cùng
- [ ] Có note lại những pattern hữu ích

## Liên quan

- [[vibe-coding]] — nền tảng workflow và mindset
- [[cursor-agent]] — một công cụ điển hình cho vibe coding
- [[claude-code]] — tool tương tự cho workflow agentic
- [[plan-mode]] — cơ chế plan-first trước khi code
- [[ai-agents]] — khái niệm agent đằng sau workflow

## Nguồn

- https://cursor.com/blog/agent-best-practices
- https://cursor.com/blog/plan-mode
- https://www.anthropic.com/learn/build-with-claude
- https://docs.anthropic.com/en/docs/claude-code/overview
