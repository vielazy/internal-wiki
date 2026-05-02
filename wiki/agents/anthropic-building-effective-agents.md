---
title: Building Effective AI Agents
topic: AI Agents
section: agents
visibility: internal
confidence: medium
tags:
  - agents
  - workflows
  - anthropic
  - prompt-engineering
sources:
  - https://www.anthropic.com/engineering/building-effective-agents
---

# Building Effective AI Agents

Bài viết này tổng hợp các nguyên tắc cốt lõi từ bài viết của Anthropic về cách xây dựng agent hiệu quả. Điểm nhấn chính là: bắt đầu đơn giản, chỉ tăng độ phức tạp khi thật sự cần, và ưu tiên những pattern có thể đo lường, debug và kiểm soát được.

Bài này có thể liên quan tới các trang khác về agent, workflows, prompting và tool use trong wiki nội bộ.

## Ý chính

- Agent tốt thường không bắt đầu từ framework phức tạp.
- Các workflow đơn giản, có thể ghép nối, thường hiệu quả hơn trong nhiều bài toán thực tế.
- Nên phân biệt rõ giữa workflow và agent tự trị.
- Càng tiến gần production, càng phải chú ý đến công cụ, kiểm thử và khả năng quan sát.

## Các building block phổ biến

Các pattern dưới đây có thể đặt cạnh những mô tả nền tảng trong trang Agent Patterns để đối chiếu nhanh giữa lý thuyết và cách triển khai.

### 1. Augmented LLM

Đây là nền tảng cơ bản nhất: một LLM được tăng cường bằng retrieval, tools và memory. Mục tiêu là giúp model có thể truy xuất thông tin, gọi công cụ và giữ lại ngữ cảnh phù hợp với bài toán.

### 2. Prompt chaining

Chia một nhiệm vụ thành nhiều bước nối tiếp nhau. Mỗi bước xử lý output của bước trước.

Phù hợp khi:
- nhiệm vụ có thể tách thành các subtasks cố định
- muốn đánh đổi latency để lấy độ chính xác cao hơn

### 3. Routing

Phân loại input rồi chuyển sang nhánh xử lý phù hợp.

Phù hợp khi:
- có nhiều loại request khác nhau
- mỗi loại cần prompt hoặc tool riêng

### 4. Parallelization

Chạy nhiều tác vụ con song song rồi tổng hợp kết quả.

Phù hợp khi:
- có thể tách việc theo chiều ngang
- cần nhiều góc nhìn hoặc nhiều lần đánh giá

### 5. Orchestrator-workers

Một LLM trung tâm chia việc cho các worker rồi tổng hợp lại.

Phù hợp khi:
- không đoán trước được số lượng subtasks
- bài toán cần linh hoạt và thích ứng

### 6. Evaluator-optimizer

Một LLM tạo câu trả lời, một LLM khác đánh giá và phản hồi để tối ưu dần.

Phù hợp khi:
- có tiêu chí đánh giá rõ
- cần vòng lặp cải tiến nhiều lần

## Khi nào nên dùng agent

Agent phù hợp với bài toán mở, khó dự đoán số bước cần làm và cần tương tác với môi trường thật. Tuy nhiên, agent tự trị thường tốn chi phí hơn và có thể tích lũy lỗi nếu không có guardrails tốt.

## Khi nào không nên dùng agent

Nếu một bài toán có thể giải bằng:
- một prompt đơn
- retrieval tốt
- hoặc một workflow đơn giản

thì không nên vội vàng chuyển sang agent phức tạp.

## Frameworks

Framework có thể giúp bắt đầu nhanh, nhưng cũng có thể thêm lớp trừu tượng gây khó debug. Cách tiếp cận an toàn là:

- dùng LLM API trực tiếp khi có thể
- hiểu rõ code phía dưới nếu dùng framework
- chỉ thêm abstraction khi nó thật sự mang lại lợi ích

## Bài học thực dụng

- Giữ thiết kế đơn giản
- Công khai rõ planning steps khi cần
- Đầu tư nghiêm túc vào tool interface và documentation
- Kiểm thử công cụ cẩn thận trước khi đưa vào production

## Tóm tắt

Thông điệp chính của bài viết là: không phải cứ xây hệ thống phức tạp là tốt. Hãy bắt đầu từ cấu trúc đơn giản nhất có thể, đo lường hiệu quả, rồi mới nâng cấp dần theo nhu cầu thực tế.
