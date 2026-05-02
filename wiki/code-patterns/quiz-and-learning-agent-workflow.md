---
title: "Quiz and Learning Agent Workflow"
topic: "AI Coding Workflows"
tags: [workflow, quiz, agent, vm, learning, tutor]
created: 2026-04-28
updated: 2026-04-28
confidence: medium
sources:
  - AI_CODING_WIKI_GUIDE.md
  - PROJECT_PRIORITY_PLAN.md
  - https://www.postgresql.org/docs/
visibility: public
---

# Quiz and Learning Agent Workflow

## Tóm tắt

Đây là workflow tổng quát để agent tạo quiz từ nội dung người dùng search, rồi chạy trên máy ảo để luyện tập, kiểm tra, hoặc tự học. Workflow này hữu ích khi bạn muốn chuyển search query thành một vòng học chủ động.

## Workflow đề xuất

### 1) Capture query

Người dùng nhập query vào search box hoặc tutor box.

Ví dụ:
- `debug workflow`
- `Next.js FastAPI Supabase architecture`
- `RLS vs app-layer ACL`

### 2) Resolve context

Backend lấy:
- primary result
- secondary results
- topic
- tags
- excerpt
- visibility
- ACL information

### 3) Build quiz pack

Quiz pack nên gồm:
- 1–2 câu recall
- 1 câu compare/contrast
- 1 câu scenario
- 1 câu pitfall

### 4) Route to agent VM

Agent trên VM nhận quiz pack và thực hiện:
- đọc context
- trả lời quiz
- ghi output
- so sánh với answer hint hoặc source notes

### 5) Log results

Nên lưu:
- query gốc
- quiz pack JSON
- agent answer
- correctness/feedback
- timestamp
- source mode

## Khi nào workflow này hữu ích

- khi muốn build tutor tự học trên VM
- khi muốn tạo bài kiểm tra sau search
- khi muốn agent tự luyện topic trong wiki
- khi muốn có loop học liên tục thay vì search một lần rồi thôi

## Design notes

### Nếu query là public

- quiz chỉ dùng nội dung public
- không đưa nội dung private vào quiz

### Nếu query là internal

- quiz có thể chi tiết hơn
- nhưng vẫn phải respect ACL

### Nếu query mơ hồ

- quiz generator nên hỏi lại hoặc giảm độ khó

## Pitfalls

- Đừng tạo quiz không liên quan tới query.
- Đừng để agent VM trả lời mà không có source context.
- Đừng để nội dung private lọt vào quiz pack public.
- Đừng log raw nội dung nhạy cảm vào file công khai.

## Liên quan

- [[quiz-generation-for-search-queries]] — cách sinh quiz từ query
- [[supabase-auth-rls-backend-acl-flow]] — flow auth + ACL + RLS
- [[internal-wiki-production-checklist]] — checklist production
- [[wiki-architecture-map]] — bản đồ điều hướng tài liệu

## Nguồn

- AI_CODING_WIKI_GUIDE.md
- PROJECT_PRIORITY_PLAN.md
- https://www.postgresql.org/docs/
