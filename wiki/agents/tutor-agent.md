---
title: Tutor Agent
topic: AI Agents
section: agents
visibility: internal
confidence: medium
tags:
  - agents
  - tutoring
  - workflow
  - education
  - prompt-design
sources:
  - https://www.anthropic.com/engineering/building-effective-agents
---

# Tutor Agent

Tutor Agent là một kiểu agent hỗ trợ học tập: giải thích từng bước, hỏi lại khi thiếu ngữ cảnh và điều chỉnh độ sâu của câu trả lời theo mức hiểu của người dùng.

## Mục tiêu thiết kế

Một tutor tốt không chỉ trả lời đúng, mà còn phải:

- dẫn dắt người học đi đúng hướng
- giải thích có cấu trúc
- tránh “nhảy cóc” qua các bước quan trọng
- nhận biết khi nào cần hỏi thêm thay vì đoán

## Hành vi mong muốn

### 1. Hỏi lại khi thiếu dữ kiện

Nếu câu hỏi mơ hồ, tutor nên hỏi để làm rõ thay vì suy diễn quá mức.

### 2. Giải thích theo lớp

Câu trả lời nên có thể đi từ:

- bản tóm tắt ngắn
- đến giải thích chi tiết
- đến ví dụ thực tế

### 3. Giữ tiến trình hội thoại

Tutor cần nhớ người học đang ở đâu trong mạch giải thích để không lặp lại quá nhiều hoặc đi quá nhanh.

### 4. Ưu tiên an toàn và tính sư phạm

Nếu một cách giải thích có thể gây hiểu nhầm, tutor nên chọn cách đơn giản hơn, an toàn hơn và dễ kiểm chứng hơn.

## Khi nào dùng tutor agent

Phù hợp cho:

- trợ lý học tập nội bộ
- hướng dẫn thao tác từng bước
- giải thích tài liệu kỹ thuật
- hỗ trợ onboarding cho người mới

## Các pattern liên quan

Tutor Agent thường dùng tốt với:

- prompt chaining để chia bài giảng thành từng phần
- evaluator-optimizer để cải thiện câu trả lời
- retrieval để lấy đúng tài liệu tham chiếu

## Kết nối với wiki nội bộ

Trang này là một mảnh ghép thực tế khi bạn muốn xây agent theo hướng đào tạo và giải thích, thay vì chỉ tạo câu trả lời ngắn.

Các bài viết khác có thể tạo backlink tự nhiên bằng cách nhắc tới slug `[[tutor-agent]]` khi nói về thiết kế agent sư phạm.
