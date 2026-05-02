---
title: "Agent VM API Contract"
topic: "AI Coding Workflows"
tags: [api, contract, agent-vm, quiz, tutor, vm]
created: 2026-04-28
updated: 2026-04-28
confidence: medium
sources:
  - AI_CODING_WIKI_GUIDE.md
  - PROJECT_PRIORITY_PLAN.md
visibility: public
---

# Agent VM API Contract

## Tóm tắt

Đây là API contract đề xuất cho agent VM trong tương lai. Contract này cho phép backend cung cấp quiz pack, agent VM giải quiz hoặc chạy task học tập, rồi trả kết quả và feedback ngược lại để lưu vào wiki runtime logs.

## Mục tiêu

- chuẩn hóa luồng search → quiz → agent VM → feedback
- để agent VM và backend hiểu cùng một schema
- giữ khả năng mở rộng sang tutor/chat/learning progress
- tách rõ public vs internal context

## Endpoints đề xuất

### 1) `POST /api/agent/quiz-pack`

Tạo quiz pack từ query hoặc topic.

Request:
```json
{
  "query": "RLS vs app-layer ACL",
  "visibility": "public",
  "role": "viewer",
  "limit": 4
}
```

Response:
```json
{
  "query": "RLS vs app-layer ACL",
  "topic": "Knowledge Ops & Productization",
  "primarySource": {
    "id": "syntheses/supabase-rls-vs-app-layer-acl",
    "title": "Supabase RLS vs App-Layer ACL",
    "path": "wiki/syntheses/supabase-rls-vs-app-layer-acl.md",
    "section": "syntheses",
    "visibility": "public",
    "excerpt": "..."
  },
  "secondaryResults": [],
  "quiz": [],
  "sourceMode": "local-db"
}
```

### 2) `POST /api/agent/solve`

Agent VM nhận quiz pack và trả lời.

Request:
```json
{
  "sessionKey": "agent-quiz-123",
  "quizPack": { }
}
```

Response:
```json
{
  "sessionKey": "agent-quiz-123",
  "status": "completed",
  "answers": [
    {
      "question": "RLS và app-layer ACL khác nhau ở điểm nào?",
      "answer": "...",
      "confidence": "medium"
    }
  ],
  "feedback": {
    "sourceMode": "local-db",
    "matchedBy": "db"
  }
}
```

### 3) `GET /api/agent/session/:sessionKey`

Lấy trạng thái session đang chạy.

Response:
```json
{
  "sessionKey": "agent-quiz-123",
  "status": "running",
  "createdAt": "...",
  "updatedAt": "..."
}
```

### 4) `POST /api/agent/feedback`

Gửi feedback sau khi agent xong.

Request:
```json
{
  "sessionKey": "agent-quiz-123",
  "correctness": "partial",
  "notes": "Need stronger explanation of RLS layer",
  "sourceMode": "local-db"
}
```

Response:
```json
{
  "ok": true
}
```

## Field rules

### sourceMode
Giá trị gợi ý:
- `local-db`
- `local-token`
- `local-public-redacted`
- `groq`
- `hybrid`

### visibility
- public request chỉ được nhận dữ liệu public
- internal request có thể nhận nội dung rộng hơn nhưng vẫn phải respect ACL

### quizPack
Quiz pack phải theo schema chuẩn ở `quiz-pack.schema.json`.

## Runtime notes

- Agent VM không nên tự đoán quyền truy cập.
- Backend phải là nơi quyết định kết quả nào được đưa vào quiz pack.
- Nếu query nội bộ nhưng role public, response chỉ nên trả title / redacted metadata.
- Logs cần tách riêng giữa generation, solve, feedback, và tutor history.

## Error handling

Nên chuẩn hóa lỗi:
- `400` — request invalid
- `401` — unauthenticated
- `403` — unauthorized
- `404` — session không tồn tại
- `409` — session conflict
- `500` — internal error

## Liên quan

- [[quiz-pack.schema.json]] — schema chuẩn cho quiz pack
- [[quiz-generation-for-search-queries]] — cách sinh quiz từ query
- [[quiz-and-learning-agent-workflow]] — workflow học tập qua VM agent
- [[supabase-auth-rls-backend-acl-flow]] — flow auth + ACL + RLS
- [[internal-wiki-production-checklist]] — checklist production

## Nguồn

- AI_CODING_WIKI_GUIDE.md
- PROJECT_PRIORITY_PLAN.md
