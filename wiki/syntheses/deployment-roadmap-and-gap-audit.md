---
title: "Deployment Roadmap and Gap Audit"
topic: "Internal Productization"
tags: [deployment, checklist, roadmap, gap-audit, vercel, supabase, agent-vm]
created: 2026-04-28
updated: 2026-04-28
confidence: medium
sources:
  - AI_CODING_WIKI_GUIDE.md
  - PROJECT_PRIORITY_PLAN.md
  - wiki/code-patterns/quiz-pack.schema.json
  - wiki/code-patterns/agent-vm-api-contract.md
visibility: internal
---

# Deployment Roadmap and Gap Audit

## Tóm tắt

Tài liệu này là checklist sống để theo dõi tiến độ đưa AI Coding Wiki lên web thật trên Supabase + Vercel, đồng thời audit các phần còn thiếu trước khi go-live. Mục tiêu là giữ kiến trúc sẵn sàng cho agent VM chạy ổn định về sau, thay vì chỉ làm một bản demo ngắn hạn.

## 1) Mục tiêu tổng thể

- đưa wiki nội bộ lên web thật
- giữ Supabase là source dữ liệu và auth chính
- dùng Vercel cho UI/runtime web
- chuẩn hóa search, tutor, quiz, upload, duplicate check, create page
- thiết kế sao cho agent VM tích hợp ổn định sau này

## 2) Kiến trúc deploy mục tiêu

### Runtime layers
- **Vercel**: web viewer/UI, API routes, upload form, admin panels
- **Supabase**: PostgreSQL, Auth, RLS, Storage, runtime tables
- **Agent VM**: consumer của quiz pack / learning tasks / background automation

### Data flow
1. User search/search + tutor.
2. Backend query Supabase.
3. Backend lọc ACL/visibility.
4. Backend trả kết quả + quiz pack.
5. Nếu user upload tài liệu, backend trích text, duplicate-check, đề xuất draft page.
6. Nếu phù hợp, backend tạo wiki page mới và sync DB.
7. Agent VM sau này có thể consume quiz pack và feedback loop.

## 3) Checklist triển khai web thật

### A. Repo and config readiness
- [ ] split env rõ local vs production
- [ ] `.env.example` đầy đủ và sạch secret
- [ ] secret thật không còn hardcode trong repo
- [ ] quyết định frontend runtime là Vercel app thay cho static-only viewer
- [ ] chuẩn hóa build/start scripts cho deploy

### B. Supabase readiness
- [ ] apply schema production lên Supabase
- [ ] seed `auth_accounts`
- [ ] verify `auth_accounts` dùng bcrypt
- [ ] verify `pages`, `page_links`, `page_tags`, `page_sources`, `page_acl`
- [ ] verify `chat_sessions`, `chat_messages`, `quiz_attempts`, `tutor_progress`
- [ ] verify `session_tokens`, `runtime_activity_log`, `sync_state`
- [ ] cấu hình Storage bucket cho upload tài liệu
- [ ] xác nhận RLS / ACL rule không leak nội dung private

### C. Viewer/UI readiness
- [ ] show public mode mặc định
- [ ] login modal chỉ còn 2 vai trò internal
- [ ] search results respect ACL
- [ ] tutor panel render gọn, không lộ nội dung nhạy cảm
- [ ] quiz panel hiển thị đầy đủ
- [ ] upload button và upload panel có mặt trên UI
- [ ] trạng thái đăng xuất xóa dữ liệu nội bộ khỏi màn hình hiện tại

### D. API readiness
- [ ] search endpoint
- [ ] tutor endpoint
- [ ] quiz-pack endpoint
- [ ] upload endpoint
- [ ] duplicate-check endpoint
- [ ] create wiki page endpoint
- [ ] session/status endpoint cho agent VM
- [ ] feedback endpoint cho agent VM

### E. Agent VM readiness
- [ ] quiz pack có JSON schema chuẩn
- [ ] API contract cho agent VM có endpoint rõ
- [ ] session key / trace ID được gắn cho mỗi interaction
- [ ] sourceMode / matchedBy / matchedCount được log
- [ ] retry / timeout / error handling có chuẩn
- [ ] agent VM không tự quyết quyền; backend enforce trước

### F. Observability and recovery
- [ ] query logs không leak private content
- [ ] runtime activity log đầy đủ
- [ ] sync state có thể rebuild lại
- [ ] backup / restore plan
- [ ] no silent failure cho upload / duplicate / create page

## 4) Gap audit hiện tại

### Có sẵn
- [x] sync markdown → PostgreSQL
- [x] DB search/tutor cơ bản
- [x] ACL-aware render/runtime
- [x] quiz pack schema
- [x] agent VM API contract draft
- [x] DB auth accounts model
- [x] bcrypt dependency
- [x] login viewer/public/internals separation

### Còn thiếu hoặc cần hoàn thiện trước khi go-live
- [ ] UI upload button/panel
- [ ] API upload file
- [ ] duplicate check endpoint
- [ ] create wiki page endpoint
- [ ] draft preview/review flow cho page mới
- [ ] search → quiz pack generation endpoint gắn vào UI rõ ràng hơn
- [ ] agent VM status/heartbeat endpoint
- [ ] production-grade error banners and retry UX
- [ ] backend validation cho file types/size
- [ ] storage path convention cho uploaded docs
- [ ] virus/safety scan placeholder hoặc basic allowlist
- [ ] seed/migration script hoàn chỉnh cho auth_accounts production
- [ ] end-to-end smoke test checklist

## 5) Tích hợp upload → duplicate-check → create page

### Proposed flow
1. User upload tài liệu.
2. Backend lưu file vào Storage.
3. Backend extract text.
4. Backend chạy duplicate check so với pages hiện có.
5. Nếu duplicate cao, trả match list để review.
6. Nếu mới, tạo draft wiki page.
7. User/internal reviewer confirm.
8. Page được sync vào DB và render trong viewer.

### Required APIs
- `POST /api/upload`
- `POST /api/duplicate-check`
- `POST /api/wiki-pages`
- optional `POST /api/wiki-pages/:id/approve`

## 6) Tích hợp chatbot quản lý tương tác

### Bot capabilities
- search DB
- tạo quiz theo topic user search
- read uploaded documents
- duplicate check
- draft page creation
- follow-up suggestions
- session logging

### Bot constraints
- always ACL-aware
- public mode redacted
- internal mode full context nhưng vẫn respect visibility
- agent VM consume outputs, not source of truth

## 7) Agent VM stability design

### Must-haves
- deterministic session IDs
- traceable `sourceMode`
- idempotent request handling
- retries with backoff
- bounded context window
- stored quiz packs
- answer/feedback persistence
- no direct trust in frontend claims

### Recommended runtime contracts
- `quiz-pack.schema.json` là format chuẩn
- `agent-vm-api-contract.md` là hợp đồng giao tiếp
- `runtime_activity_log` để trace all actions
- `chat_sessions` / `quiz_attempts` để phục hồi trạng thái

## 8) Next implementation order

1. Add upload UI + backend endpoint.
2. Add duplicate-check API.
3. Add create wiki page API.
4. Wire quiz-pack generation into UI.
5. Add agent VM status/feedback endpoints.
6. Create end-to-end smoke tests.
7. Prepare Vercel deploy config.

## 9) Lưu ý & Pitfalls

- Đừng launch khi upload chưa có duplicate check.
- Đừng để public mode hiển thị nội dung internal sau logout.
- Đừng để agent VM tự do chạm vào DB without backend gating.
- Đừng để search trả excerpt private cho role public.
- Đừng bỏ qua retry/error UX trước go-live.

## 10) Liên quan

- [[quiz-pack.schema.json]] — schema chuẩn cho quiz pack
- [[agent-vm-api-contract]] — hợp đồng API cho agent VM
- [[quiz-generation-for-search-queries]] — cách sinh quiz từ search query
- [[quiz-and-learning-agent-workflow]] — workflow học tập qua VM agent
- [[internal-wiki-production-checklist]] — checklist production
- [[internal-wiki-launch-checklist]] — checklist go-live

## 11) Nguồn

- AI_CODING_WIKI_GUIDE.md
- PROJECT_PRIORITY_PLAN.md
- wiki/code-patterns/quiz-pack.schema.json
- wiki/code-patterns/agent-vm-api-contract.md
