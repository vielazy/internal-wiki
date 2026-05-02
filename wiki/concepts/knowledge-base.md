---
title: "Knowledge Base"
topic: "Knowledge Base & RAG"
tags: [knowledge-base, markdown, wiki, documentation]
created: 2026-04-20
updated: 2026-04-20
confidence: low
sources:
  - https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
  - https://www.anthropic.com/learn/build-with-claude
---

# Knowledge Base

## Tóm tắt

Knowledge base là hệ thống tổ chức tri thức thành các trang có cấu trúc để LLM và human cùng tra cứu, cập nhật, và tái sử dụng. Với AI Coding Wiki, markdown-based knowledge base là trung tâm của toàn bộ workflow.

## Nội dung chính

Một knowledge base tốt thường có:

- Cấu trúc topic rõ ràng
- Front matter để lưu metadata
- Cross-references giữa các trang
- Nguồn gốc dữ liệu rõ ràng
- Quy tắc cập nhật nhất quán

So với RAG, knowledge base là lớp nội dung và tổ chức tri thức; RAG là cơ chế truy xuất và sinh trả lời trên nền tri thức đó.

## Thực hành / Ví dụ

- Dùng markdown pages với front matter để dễ index.
- Ghi rõ nguồn và confidence cho từng page.
- Tạo index và log để trace thay đổi.

## Lưu ý & Pitfalls

- Knowledge base mà không có nguồn sẽ dễ hallucinate.
- Nếu không có cross-reference, nội dung dễ bị silo.
- Cần quy ước naming để tránh trùng lặp page.

## Liên quan

- [[rag]] — cơ chế truy xuất trên knowledge base
- [[contextual-retrieval]] — cách retrieval dựa vào ngữ cảnh để tăng độ chính xác
- [[evals]] — kiểm tra chất lượng nội dung và retrieval
- [[prompt-templates]] — templates giúp tạo trang tri thức nhất quán

## Nguồn

- https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
- https://www.anthropic.com/learn/build-with-claude
