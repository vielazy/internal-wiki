---
title: "Contextual Retrieval"
topic: "Knowledge Base & RAG"
tags: [contextual-retrieval, rag, retrieval, context]
created: 2026-04-20
updated: 2026-04-20
confidence: low
sources:
  - https://www.anthropic.com/news/contextual-retrieval
  - https://www.anthropic.com/learn/build-with-claude
---

# Contextual Retrieval

## Tóm tắt

Contextual retrieval là cách lấy thông tin từ knowledge base hoặc corpus dựa trên ngữ cảnh của câu hỏi, thay vì chỉ matching từ khóa đơn thuần. Mục tiêu là tăng độ chính xác và giảm tình trạng retrieval thiếu phần quan trọng.

## Nội dung chính

Trong thực hành RAG, retrieval tốt thường cần:

- Query hiểu được intent và domain context
- Chunking hợp lý
- Ranking hoặc reranking theo relevance
- Kết hợp metadata và cross-links

Anthropic nhấn mạnh contextual retrieval như một cách cải thiện chất lượng dữ liệu đầu vào cho model, nhất là khi corpus lớn hoặc page có cấu trúc phức tạp.

## Thực hành / Ví dụ

- Dùng metadata topic/tags để lọc candidate pages trước khi rank.
- Kết hợp link graph với text similarity.
- Kiểm tra retrieval bằng evals thay vì chỉ nhìn một vài ví dụ.

## Lưu ý & Pitfalls

- Retrieval theo context vẫn có thể bỏ sót nếu chunking kém.
- Nếu corpus thiếu chuẩn hóa, ranking dễ nhiễu.
- Không nên lẫn contextual retrieval với generation logic.

## Liên quan

- [[rag]] — lớp tổng quát của retrieval augmented generation
- [[knowledge-base]] — corpus nguồn cho retrieval
- [[evals]] — kiểm tra chất lượng retrieval

## Nguồn

- https://www.anthropic.com/news/contextual-retrieval
- https://www.anthropic.com/learn/build-with-claude
