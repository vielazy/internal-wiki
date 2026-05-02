---
title: Multi-Agent
topic: AI Agents
section: agents
visibility: internal
confidence: medium
tags:
  - agents
  - coordination
  - workflow
  - collaboration
sources:
  - https://www.anthropic.com/engineering/building-effective-agents
---

# Multi-Agent

Multi-Agent là mô hình trong đó nhiều agent hoặc nhiều vai trò agent cùng tham gia giải quyết một bài toán. Mỗi agent có thể đảm nhiệm một phần nhiệm vụ riêng, rồi kết quả được hợp nhất lại ở bước cuối.

## Khi nào nên dùng

Mô hình nhiều agent phù hợp khi:

- bài toán có nhiều góc nhìn cần xem xét
- các phần việc có thể tách rời
- cần kiểm tra chéo giữa các lời giải
- muốn kết hợp agent chuyên biệt cho từng vai trò

## Ví dụ vai trò

Một hệ multi-agent có thể gồm:

- **Planner**: phân rã nhiệm vụ
- **Researcher**: tìm và tổng hợp dữ liệu
- **Writer**: viết câu trả lời cuối
- **Reviewer**: kiểm tra chất lượng và độ chính xác

## Lợi ích

- dễ chia nhỏ trách nhiệm
- có thể tăng chất lượng nhờ phản biện chéo
- phù hợp cho nhiệm vụ có cấu trúc phức tạp

## Rủi ro

- tăng độ trễ
- tăng chi phí
- dễ tạo ra “nhiễu phối hợp” nếu vai trò không rõ ràng

## Cách giữ hệ thống gọn

Trước khi chuyển sang multi-agent, nên xem liệu một workflow đơn giản hoặc một agent duy nhất có đủ không. Chỉ dùng nhiều agent khi sự phức tạp đó thực sự mang lại lợi ích đo được.

## Liên quan

Trang này thường được đọc cùng với các nội dung về:

- Agent Patterns
- prompt chaining
- orchestrator-workers
- evaluator-optimizer

Các bài viết khác trong wiki có thể tạo backlink tự nhiên bằng cách nhắc tới slug `[[multi-agent]]` khi bàn về phối hợp nhiều agent.
