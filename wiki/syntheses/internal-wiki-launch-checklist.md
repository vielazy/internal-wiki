---
title: "Internal Wiki Launch Checklist"
topic: "Knowledge Ops & Productization"
tags: [checklist, launch, internal-wiki, production, readiness]
created: 2026-04-28
updated: 2026-04-28
confidence: medium
sources:
  - AI_CODING_WIKI_GUIDE.md
  - PROJECT_PRIORITY_PLAN.md
  - https://supabase.com/docs
  - https://www.postgresql.org/docs/
visibility: public
---

# Internal Wiki Launch Checklist

## Tóm tắt

Đây là checklist “ready to launch” cho AI Coding Wiki khi chuyển từ knowledge base đang phát triển sang internal wiki có người dùng thật. Mục tiêu là đảm bảo core runtime, nội dung, search, ACL, logs, và vận hành đủ chắc trước khi mở rộng tiếp.

## Launch checklist

### 1) Core content readiness

- [ ] `raw/` vẫn immutable
- [ ] `wiki/` đầy đủ page cốt lõi
- [ ] mỗi page có front matter, Liên quan, Nguồn
- [ ] `wiki/INDEX.md` phản ánh đúng cấu trúc hiện tại
- [ ] các page gap quan trọng đã được tạo
- [ ] các synthesis chính đã có mặt

### 2) Search readiness

- [ ] PostgreSQL search đã chạy tốt
- [ ] full-text search index hoạt động
- [ ] trigram search sẵn sàng cho fuzzy query
- [ ] search ưu tiên title/tags/excerpt/body hợp lý
- [ ] search results ACL-aware
- [ ] search latency chấp nhận được với size hiện tại

### 3) Sync readiness

- [ ] sync markdown → DB ổn định
- [ ] sync incremental
- [ ] sync idempotent
- [ ] sync transaction-safe
- [ ] `content_hash` / `sync_state` được cập nhật đúng
- [ ] có thể rebuild DB từ markdown nếu cần

### 4) Permission readiness

- [ ] visibility model rõ ràng
- [ ] page ACL đã có nơi áp dụng
- [ ] backend là nơi enforce quyền cuối cùng
- [ ] frontend không tự quyết quyền
- [ ] backlinks / related pages / tutor retrieval cùng tuân thủ ACL
- [ ] query logs không leak nội dung private

### 5) Runtime readiness

- [ ] DB mode là đường chạy chính cho production
- [ ] file mode chỉ dùng cho dev/debug
- [ ] UI không đọc markdown trực tiếp ở runtime production
- [ ] search/query API trả dữ liệu đã lọc
- [ ] auth flow hoạt động end-to-end

### 6) Observability readiness

- [ ] `wiki/LOG.md` sạch và append-only
- [ ] runtime logs tách khỏi authoring logs
- [ ] query logs có thể dùng để tune search
- [ ] có sync/job trace rõ ràng
- [ ] có bản ghi lỗi và cách debug

### 7) Recovery readiness

- [ ] có backup plan cho DB
- [ ] có backup plan cho markdown vault
- [ ] có restore procedure
- [ ] có revision history plan nếu nội dung thay đổi nhiều
- [ ] có thể tái lập content từ source nếu DB hỏng

### 8) Documentation readiness

- [ ] `AI_CODING_WIKI_GUIDE.md` là master guide
- [ ] `PROJECT_PRIORITY_PLAN.md` phản ánh đúng ưu tiên
- [ ] `CLAUDE.md` / `AGENTS.md` nhất quán với guide
- [ ] `README.md` dẫn tới đúng tài liệu chính
- [ ] `wiki/INDEX.md` là cửa vào của content

## What to do before launch

1. Rà soát search + ACL + sync.
2. Confirm viewer/runtime đọc đúng DB mode.
3. Đảm bảo index và bundle tài liệu không lệch.
4. Chạy một vòng lint / query / smoke test.
5. Chỉ mở rộng thêm semantic/dashboard sau khi baseline đã ổn.

## Pitfalls

- Đừng launch khi search còn scan file markdown ở runtime production.
- Đừng launch khi permissions chưa được enforce ở backend.
- Đừng launch nếu sync còn drift giữa wiki và DB.
- Đừng launch nếu logs chưa tách rõ authoring/runtime.
- Đừng launch trước khi có đường recovery cơ bản.

## Liên quan

- [[internal-wiki-production-bundle]] — bundle đọc nhanh cho cụm production
- [[internal-wiki-production-checklist]] — checklist triển khai theo lớp
- [[internal-wiki-architecture-recommendation]] — kiến trúc production được khuyến nghị
- [[supabase-auth-rls-backend-acl-flow]] — flow auth + RLS + backend ACL
- [[project-priority-plan]] — thứ tự việc cần làm

## Nguồn

- AI_CODING_WIKI_GUIDE.md
- PROJECT_PRIORITY_PLAN.md
- https://supabase.com/docs
- https://www.postgresql.org/docs/
