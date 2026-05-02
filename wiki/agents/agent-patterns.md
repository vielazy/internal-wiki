---
title: Agent Patterns
topic: AI Agents
section: agents
visibility: internal
confidence: medium
tags:
  - agents
  - patterns
  - workflows
  - architecture
  - prompt-engineering
sources:
  - https://www.anthropic.com/engineering/building-effective-agents
---

# Agent Patterns

Trang này hệ thống hóa các pattern phổ biến khi xây agent và workflow. Mục tiêu là giúp bạn chọn đúng cấu trúc cho đúng bài toán, thay vì tăng độ phức tạp quá sớm.

## Bức tranh tổng quan

Trong bài viết của Anthropic, các pattern được chia thành hai nhóm lớn:

- **Workflow**: luồng xử lý được định nghĩa trước bằng code
- **Agent**: model tự quyết định bước tiếp theo, công cụ nào cần gọi và khi nào dừng

## Các pattern chính

### Augmented LLM

Đây là nền tảng cơ bản: một LLM được bổ sung retrieval, tools và memory. Nó là điểm khởi đầu tốt nếu bạn muốn giữ hệ thống đơn giản nhưng vẫn có khả năng truy xuất kiến thức và thao tác với môi trường.

### Prompt chaining

Tách nhiệm vụ thành chuỗi các bước cố định. Mỗi bước nhận output của bước trước.

Phù hợp khi:
- nhiệm vụ tách được thành các subtasks rõ ràng
- muốn tăng độ chính xác bằng cách giảm độ khó của từng bước

### Routing

Phân loại input rồi chuyển sang nhánh xử lý phù hợp.

Phù hợp khi:
- có nhiều loại request khác nhau
- mỗi loại cần prompt/tool riêng

### Parallelization

Chạy nhiều tác vụ cùng lúc rồi hợp nhất kết quả.

Phù hợp khi:
- các subtasks độc lập với nhau
- muốn tăng tốc hoặc cần nhiều góc nhìn

### Orchestrator-workers

Một LLM trung tâm chia nhỏ nhiệm vụ cho các worker rồi tổng hợp lại.

Phù hợp khi:
- không đoán trước được các subtasks
- cần linh hoạt trong cách phân rã bài toán

### Evaluator-optimizer

Một LLM tạo đầu ra, một LLM khác đánh giá và phản hồi để cải tiến liên tục.

Phù hợp khi:
- có tiêu chí đánh giá rõ
- cần lặp nhiều vòng để nâng chất lượng

## Cách chọn pattern

Một cách thực dụng là bắt đầu theo thứ tự này:

1. Prompt đơn giản
2. Augmented LLM
3. Workflow cố định
4. Agent tự trị

Nếu một bài toán giải được bằng cách đơn giản hơn, đừng vội dùng agent.

## Khi nào nên ưu tiên workflow hơn agent

Workflow phù hợp hơn khi:
- đầu vào khá ổn định
- các bước xử lý biết trước
- cần tính dự đoán được cao

Agent phù hợp hơn khi:
- số bước không đoán trước được
- cần ra quyết định động
- phải phản ứng với môi trường thực

## Ghi nhớ thực dụng

- Giảm abstraction nếu nó làm khó debug
- Dùng tool interface rõ ràng, có tài liệu tốt
- Kiểm thử hành vi tool trước khi đưa vào production
- Đánh giá hiệu quả bằng số liệu thay vì cảm tính

## Liên quan

Trang này là nền tảng để đọc tiếp những trang nội bộ khác như:
- Tutor Agent
- Multi-Agent
- bài viết Anthropic gốc về effective agents

Để hệ thống tự sinh backlink, các trang khác trong wiki có thể nhắc trực tiếp đến trang này bằng slug `[[agent-patterns]]`.
