---
title: "Prompt Templates"
topic: "Prompt Engineering"
tags: [prompt-templates, patterns, vibe-coding, reusable-prompts]
created: 2026-04-20
updated: 2026-04-20
confidence: medium
sources:
  - https://www.anthropic.com/learn/build-with-claude
  - https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview
  - https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices
---

# Prompt Templates

Trang này mở rộng từ `wiki/concepts/prompt-templates.md` bằng cách tập trung vào các mẫu prompt thực chiến khi vibe coding.

## Tóm tắt

Prompt templates là các pattern prompt tái sử dụng để giao việc cho agent ổn định hơn. Khi vibe coding, templates giúp chuẩn hóa cách yêu cầu plan, debug, refactor, viết test, và review diff.

## Collection các pattern hay dùng

### 1. Plan-first prompt
Dùng khi task lớn.

Mục tiêu: bắt agent nghiên cứu và trả plan trước khi sửa code.

```text
Hãy đọc codebase liên quan, xác định file cần chạm, rồi đưa ra plan ngắn gọn gồm các bước implement, kiểm tra, và rủi ro trước khi viết code.
```

### 2. Debug prompt
Dùng khi có bug hoặc lỗi runtime.

```text
Hãy tìm nguyên nhân gốc của bug này, nêu 2-3 giả thuyết, kiểm tra từng giả thuyết bằng evidence trong code, rồi đề xuất fix nhỏ nhất có thể.
```

### 3. Refactor prompt
Dùng khi muốn cải tổ code mà không đổi behavior.

```text
Hãy refactor phần này để dễ đọc hơn nhưng không thay đổi behavior. Giữ diff nhỏ, giải thích từng thay đổi, và chạy lint/test sau khi sửa.
```

### 4. Test-generation prompt
Dùng khi cần coverage.

```text
Hãy viết test cho case bình thường và edge cases quan trọng nhất. Dựa trên existing test style của repo và không thay đổi implementation cho tới khi test fail trước.
```

### 5. Review prompt
Dùng để review diff của agent hoặc của người.

```text
Hãy review thay đổi này như một senior reviewer: tìm bug, edge cases, naming issues, và chỗ nào có thể làm đơn giản hơn. Chỉ ra mức độ nghiêm trọng cho từng issue.
```

### 6. Small-step implementation prompt
Dùng để giảm risk.

```text
Hãy implement theo từng bước nhỏ. Mỗi bước xong hãy dừng lại, tóm tắt thay đổi và hỏi trước khi đi tiếp sang bước tiếp theo.
```

## Thực hành / Ví dụ

- Khi dùng Cursor hoặc Claude Code, lưu templates này vào `.cursor/` hoặc docs nội bộ để tái sử dụng.
- Tùy task, chỉ giữ 1-2 mục tiêu chính trong prompt để tránh loãng.
- Nếu agent đi sai hướng, quay lại template plan-first hoặc debug.

## Lưu ý & Pitfalls

- Template tốt phải ngắn và có mục đích rõ.
- Nếu chèn quá nhiều context, template trở thành rác.
- Luôn yêu cầu verify khi task có thể đo được.

## Liên quan

- [[prompt-templates]] — bản khái niệm gốc trong concepts/
- [[claude-md-template]] — template file hướng dẫn cho project
- [[vibe-coding]] — bối cảnh dùng prompt templates trong workflow AI
- [[agent-patterns]] — prompt templates thường điều khiển patterns này

## Nguồn

- https://www.anthropic.com/learn/build-with-claude
- https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview
- https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices
