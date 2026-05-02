---
title: "CLAUDE.md Template"
topic: "Code Patterns"
tags: [claude-md, template, vibe-coding, instructions]
created: 2026-04-20
updated: 2026-04-20
confidence: medium
sources:
  - https://www.anthropic.com/learn/build-with-claude
  - https://cursor.com/blog/agent-best-practices
---

# CLAUDE.md Template

Trang này cung cấp một template chuẩn cho `CLAUDE.md` trong vibe coding projects, cùng giải thích từng section để agent hiểu rõ cách làm việc trong repo.

## Template

```markdown
# Project Name

## Mục tiêu
- Repo này làm gì?
- Kết quả mong muốn là gì?

## Stack
- Framework / language
- Package manager
- Test runner
- Lint / format tools

## Cách chạy
- Install dependencies
- Dev server
- Build
- Test
- Lint

## Quy ước code
- Naming conventions
- Folder structure
- Component / module patterns
- TypeScript / JavaScript conventions

## Workflow cho agent
- Luôn đọc README, AGENTS, và wiki liên quan trước khi sửa lớn
- Với task lớn, tạo plan trước khi code
- Chạy tests/lint sau mỗi thay đổi đáng kể
- Giữ diff nhỏ và có thể review được

## File quan trọng
- Path tới entrypoints
- Path tới canonical examples
- Path tới test files mẫu

## Cấm / tránh
- Không sửa file generated
- Không chạm raw data hoặc artifact immutable
- Không thay đổi config nếu không cần thiết

## Ghi chú thêm
- Link tới docs nội bộ
- Link tới wiki pages liên quan
```

## Giải thích từng section

### Mục tiêu
Giúp agent hiểu nhanh repo này tồn tại để làm gì.

### Stack
Cho agent biết công cụ nào đang dùng để tránh đoán sai lệnh.

### Cách chạy
Là phần cực kỳ quan trọng để agent biết verify như thế nào.

### Quy ước code
Giảm style drift và tránh diff không đồng nhất.

### Workflow cho agent
Đây là nơi bạn “điều khiển” hành vi mặc định của agent.

### File quan trọng
Giúp agent tìm đúng canonical files nhanh hơn.

### Cấm / tránh
Chặn các hành vi dễ gây lỗi hoặc phá structure.

## Thực hành / Ví dụ

- Giữ `CLAUDE.md` ngắn, thực dụng, không biến thành handbook dài.
- Link tới các file canonical thay vì copy toàn bộ style guide.
- Cập nhật khi agent lặp lại một lỗi cụ thể.

## Liên quan

- [[prompt-templates]] — dùng template prompt để giao task nhất quán
- [[vibe-coding]] — workflow agent-centric cần instructions rõ
- [[ai-coding-workflows]] — phần verify và plan của workflow
- [[agent-patterns]] — nền tảng để agent hoạt động ổn định

## Nguồn

- https://www.anthropic.com/learn/build-with-claude
- https://cursor.com/blog/agent-best-practices
