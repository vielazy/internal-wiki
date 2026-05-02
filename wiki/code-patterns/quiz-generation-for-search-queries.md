---
title: "Quiz Generation for Search Queries"
topic: "AI Coding Workflows"
tags: [quiz, agents, search, tutor, retrieval, vm-agent]
created: 2026-04-28
updated: 2026-04-28
confidence: medium
sources:
  - AI_CODING_WIKI_GUIDE.md
  - PROJECT_PRIORITY_PLAN.md
  - https://www.postgresql.org/docs/
  - https://supabase.com/docs
visibility: public
---

# Quiz Generation for Search Queries

## Tóm tắt

Đây là hướng dẫn để biến nội dung người dùng nhập vào thanh tìm kiếm thành quiz/learning tasks cho agent chạy sau này trên máy ảo. Ý tưởng là: query search không chỉ trả về page, mà còn có thể sinh ra các câu hỏi kiểm tra hiểu biết, gợi ý luyện tập, và follow-up prompts phù hợp với topic đang tìm.

## Mục tiêu của feature

- biến search thành learning loop
- giúp tutor/agent tạo quiz đúng theo nội dung user đang quan tâm
- hỗ trợ cá nhân hóa cho agent chạy trên VM sau này
- giữ quiz grounded vào wiki content, không bịa kiến thức ngoài nguồn

## Luồng khuyến nghị

### 1) User nhập query

Ví dụ:
- `RLS vs app-layer ACL`
- `TDD workflow`
- `Next.js FastAPI Supabase architecture`

### 2) Search backend lấy context

Backend search phải trả về:
- page phù hợp nhất
- secondary results
- visibility
- topic / section / tags
- excerpt hoặc summary đã lọc quyền

### 3) Quiz generator đọc context

Quiz generator nên tạo:
- 1 câu hỏi nhận biết cơ bản
- 1 câu hỏi so sánh / phân tích
- 1 câu hỏi ứng dụng thực tế
- 1 câu hỏi “pitfall” để kiểm tra hiểu sai thường gặp

### 4) Lưu quiz artifact

Nếu agent chạy trên máy ảo, quiz có thể được lưu thành:
- JSON cho machine-readable pipeline
- markdown cho human review
- DB record để trace tiến trình học

## Cách tạo quiz tốt

### Nguyên tắc 1 — Grounded only

Quiz phải dựa trên:
- title
- topic
- excerpt
- headings
- sources
- related pages

Không tạo câu hỏi về chi tiết không có trong context.

### Nguyên tắc 2 — Từ dễ đến khó

Quiz nên đi theo level:
1. recall
2. comprehension
3. application
4. comparison
5. debugging / pitfall identification

### Nguyên tắc 3 — Bám mục tiêu học

Nếu query là về:
- `search` → quiz về ranking, ACL, index
- `ACL` → quiz về visibility, RLS, app-layer rules
- `workflow` → quiz về steps, checkpoints, verification
- `architecture` → quiz về component boundaries, trade-offs

## Mẫu quiz đề xuất

### Loại 1 — Short answer
- `RLS khác gì app-layer ACL?`
- `Vì sao search production nên chạy trên PostgreSQL?`

### Loại 2 — Multiple choice
- `Trong 4 lựa chọn dưới đây, đâu là lớp enforce quyền cuối cùng?`

### Loại 3 — Compare / contrast
- `So sánh Supabase Auth và backend ACL`

### Loại 4 — Scenario-based
- `Nếu người dùng public search thấy tài liệu internal, bạn sẽ xử lý thế nào?`

### Loại 5 — Pitfall detection
- `Điều gì nguy hiểm nếu frontend tự quyết quyền truy cập?`

## Format output khuyến nghị

Quiz generator nên trả về một object kiểu:

```json
{
  "query": "RLS vs app-layer ACL",
  "topic": "Knowledge Ops & Productization",
  "primarySource": {
    "title": "Supabase Auth + RLS + Backend ACL Flow",
    "path": "wiki/syntheses/supabase-auth-rls-backend-acl-flow.md"
  },
  "secondaryResults": [
    {
      "title": "Supabase RLS vs App-Layer ACL",
      "path": "wiki/syntheses/supabase-rls-vs-app-layer-acl.md"
    }
  ],
  "quiz": [
    {
      "type": "short_answer",
      "question": "RLS và app-layer ACL khác nhau ở điểm nào?",
      "answerHint": "RLS là lớp DB, ACL là lớp backend"
    }
  ],
  "sourceMode": "local-db | groq | hybrid"
}
```

## Tích hợp với agent chạy trên VM

Khi agent chạy trên máy ảo, flow nên là:

1. user nhập query/search
2. search backend trả results
3. quiz generator sinh quiz từ context
4. agent chạy trên VM đọc quiz
5. agent trả lời / học / verify
6. kết quả được log lại để tái sử dụng

## Gợi ý triển khai sau này

### Option A — Search-triggered quiz

Mỗi query search đều có thể kích hoạt quiz generation nếu:
- query đủ dài
- query thuộc topic học tập
- user bật chế độ học

### Option B — Tutor-triggered quiz

Chỉ tạo quiz khi người dùng bấm nút Tutor hoặc Hỏi thêm.

### Option C — Agent-driven quiz

Agent VM nhận quiz và tự chạy vòng:
- generate
- solve
- self-check
- retry

## Lưu ý & Pitfalls

- Đừng tạo quiz từ query quá ngắn hoặc quá mơ hồ.
- Đừng để quiz lộ nội dung private cho public user.
- Đừng tạo quá nhiều quiz một lúc; ưu tiên 2–4 câu chất lượng hơn 10 câu rác.
- Đừng dùng quiz chỉ để “cho có”; quiz phải phục vụ learning objective rõ ràng.
- Đừng quên lưu `sourceMode` để biết quiz đến từ local DB hay LLM.

## Liên quan

- [[quiz-and-learning-agent-workflow]] — workflow học tập dựa trên query
- [[supabase-auth-rls-backend-acl-flow]] — flow auth + RLS + backend ACL
- [[supabase-postgresql-search]] — search strategy trong DB
- [[internal-wiki-production-checklist]] — checklist production cho internal wiki
- [[project-priority-plan]] — thứ tự ưu tiên hiện tại

## Nguồn

- AI_CODING_WIKI_GUIDE.md
- PROJECT_PRIORITY_PLAN.md
- https://www.postgresql.org/docs/
- https://supabase.com/docs
