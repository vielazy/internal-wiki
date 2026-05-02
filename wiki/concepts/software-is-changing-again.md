---
title: "Software Is Changing (Again)"
topic: "Vibe Coding"
tags: [software-3.0, vibe-coding, llm, autonomy, partial-autonomy]
created: 2026-04-20
updated: 2026-04-20
confidence: medium
sources:
  - raw/videos/2026-04-20-andrej-karpathy-software-is-changing-again.md
---

# Software Is Changing (Again)

## Tóm tắt

Bài nói của Andrej Karpathy nhấn mạnh rằng software đang bước sang một programming paradigm mới: software 1.0 là code, software 2.0 là weights, và software 3.0 là prompts viết bằng English để program LLMs. Từ đó, nhiều sản phẩm sẽ chuyển sang mô hình partial autonomy, nơi AI generate còn human verify.

## Nội dung chính

Các ý chính trong video:

- Software thay đổi lớn theo từng thời kỳ, và LLM tạo ra một paradigm mới.
- Prompts trở thành một dạng program.
- LLM giống một kiểu operating system mới: context windows như memory, model như compute.
- AI apps hiệu quả thường là partial autonomy apps, không phải full autonomy ngay lập tức.
- Human vẫn là bottleneck trong verify loop, nên GUI và diff-based review rất quan trọng.
- “Keep the AI on the leash”: chia task nhỏ, prompt cụ thể, kiểm tra từng bước.
- Nhiều sản phẩm tương lai sẽ được xây “for agents”, không chỉ cho người dùng human.

## Thực hành / Ví dụ

- Dùng AI để generate code theo từng chunk nhỏ thay vì giao cả repo một lần.
- Thiết kế workflow có bước verify rõ ràng: diff, test, review.
- Khi làm docs hoặc products, nghĩ đến việc làm chúng “LLM-friendly”.
- Cân nhắc tự động hóa từng phần, không cần nhảy ngay đến full agent autonomy.

## Lưu ý & Pitfalls

- Không nên hiểu vibe coding là bỏ review; Karpathy nhấn mạnh verify loop rất quan trọng.
- Diff quá lớn sẽ làm human trở thành bottleneck.
- LLM có superpowers nhưng cũng có hallucination, prompt injection, và memory limitations.
- “Year of agents” không phải một thời điểm cố định; đây là một hành trình dài.

## Liên quan

- [[vibe-coding]] — framing chung về coding với AI
- [[ai-coding-workflows]] — workflow nhỏ-chặt-verify theo từng bước
- [[agent-patterns]] — kiến trúc agent cần để giữ AI “on the leash”
- [[prompt-engineering]] — prompt cụ thể giúp tăng tỷ lệ verify thành công
- [[cursor-agent]] — ví dụ thực tế của partial autonomy trong IDE

## Nguồn

- raw/videos/2026-04-20-andrej-karpathy-software-is-changing-again.md
