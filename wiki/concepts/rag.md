---
title: "Retrieval Augmented Generation (RAG)"
topic: "Knowledge Base & RAG"
tags: [rag, retrieval, embeddings, knowledge-base]
created: 2026-04-20
updated: 2026-04-20
confidence: medium
sources:
  - https://www.anthropic.com/learn/build-with-claude
  - https://docs.anthropic.com/en/docs/build-with-claude/embeddings
  - https://www.anthropic.com/news/contextual-retrieval
---

# Retrieval Augmented Generation (RAG)

## Tóm tắt

RAG là kỹ thuật kết hợp retrieval từ nguồn ngoài với generation của LLM để trả lời dựa trên dữ liệu cập nhật hoặc domain-specific. Đây là nền tảng của nhiều knowledge base và assistant system.

## Nội dung chính

Anthropic đặt RAG như một building block quan trọng trong Build with Claude:

- Dùng embeddings để biểu diễn nội dung
- Retrieve những chunk liên quan nhất theo query
- Đưa context đã truy xuất vào LLM để sinh câu trả lời
- Có thể kết hợp contextual retrieval để tăng độ chính xác

Trong wiki này, RAG là cầu nối giữa raw knowledge sources và các trang syntheses/answers.

## Thực hành / Ví dụ

- Chunk tài liệu theo semantic boundaries thay vì cắt tùy tiện.
- Lưu metadata để dễ filter và trace nguồn.
- Đánh giá retrieval quality độc lập với generation quality.

## Lưu ý & Pitfalls

- RAG không thay thế việc thiết kế corpus tốt.
- Retrieval kém sẽ kéo generation đi sai.
- Không phải câu hỏi nào cũng cần RAG; đôi khi knowledge base tĩnh là đủ.

## Liên quan

- [[knowledge-base]] — knowledge base là lớp lưu trữ tri thức cho RAG
- [[embeddings]] — vector representations dùng cho retrieval
- [[contextual-retrieval]] — kỹ thuật cải thiện RAG theo Anthropic

## Nguồn

- https://www.anthropic.com/learn/build-with-claude
- https://docs.anthropic.com/en/docs/build-with-claude/embeddings
- https://www.anthropic.com/news/contextual-retrieval
