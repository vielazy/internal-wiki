---
title: "Next.js + TypeScript + Tailwind + FastAPI + Supabase Architecture"
topic: "Web & App Development"
tags: [synthesis, nextjs, typescript, tailwind, fastapi, supabase, postgresql, architecture]
created: 2026-04-28
updated: 2026-04-28
confidence: medium
sources:
  - https://nextjs.org/docs
  - https://www.tailwindcss.com/docs
  - https://fastapi.tiangolo.com/
  - https://supabase.com/docs
  - https://www.postgresql.org/docs/
visibility: public
---

# Next.js + TypeScript + Tailwind + FastAPI + Supabase Architecture

## Tóm tắt

Đây là một stack rất hợp cho internal tools, knowledge apps, dashboards, và agent-facing products. Next.js + TypeScript + Tailwind xử lý UI và trải nghiệm người dùng, FastAPI xử lý business logic và API, còn Supabase cung cấp PostgreSQL, auth, storage, và một số dịch vụ managed khác.

Vì bạn đang dùng PostgreSQL trên Supabase, lựa chọn hợp lý nhất là coi Supabase như lớp hạ tầng managed cho Postgres/Auth/Storage, còn FastAPI là lớp application backend để giữ logic truy xuất, ACL, ranking, sync, và các quy tắc nghiệp vụ rõ ràng.

## Nội dung chính

### 1) Vai trò của từng lớp

**Next.js**
- render UI
- điều phối routing, server components, client components
- phù hợp cho product UI, search UI, document viewer, admin console

**TypeScript**
- giữ type safety ở frontend và các shared contracts
- giảm lỗi khi truyền payload giữa UI và API
- rất hữu ích nếu repo có nhiều page, form, hoặc query states

**Tailwind CSS**
- tăng tốc xây UI nhất quán
- phù hợp cho internal product cần ship nhanh nhưng vẫn muốn design system gọn
- dễ chuẩn hóa component spacing, typography, states

**FastAPI**
- xử lý business logic
- cung cấp search endpoints, sync endpoints, permission-aware retrieval
- phù hợp khi backend cần rõ ranh giới, validation, và tự document API

**Supabase**
- cung cấp PostgreSQL managed
- hỗ trợ auth, storage, và hệ sinh thái tooling xung quanh Postgres
- phù hợp khi muốn giảm chi phí vận hành hạ tầng cơ bản

### 2) Kiến trúc khuyến nghị cho repo của bạn

Với bối cảnh AI Coding Wiki, kiến trúc nên là:

- **Next.js** làm frontend
- **FastAPI** làm backend chính
- **Supabase PostgreSQL** là database layer
- **Supabase Auth** nếu muốn auth nhanh và managed
- **Supabase Storage** nếu có attachment hoặc asset upload

Luồng chuẩn:

1. User mở Next.js UI
2. UI gọi FastAPI
3. FastAPI đọc PostgreSQL trên Supabase
4. FastAPI áp ACL / visibility / ranking
5. FastAPI trả data sạch cho UI
6. UI render, filter, search, và hiển thị backlinks / metadata

### 3) Hai biến thể kiến trúc

#### Model A — FastAPI-first

Dùng khi:
- business logic phức tạp
- search / permissions / sync cần kiểm soát chặt
- muốn backend độc lập, dễ test

Ưu điểm:
- ranh giới rõ
- dễ tối ưu search và policy ở một chỗ
- phù hợp internal wiki / knowledge platform

#### Model B — Supabase-centric

Dùng khi:
- muốn ship nhanh
- auth và storage cần managed ngay
- logic backend chưa quá phức tạp

Ưu điểm:
- ít code infra hơn
- nhanh ra MVP
- hợp cho CRUD app nhỏ

Nhược điểm:
- nếu search, ACL, sync, audit phức tạp, backend logic dễ bị phân tán
- khó giữ policy thống nhất nếu app lớn lên

### 4) Decision matrix

- **Cần auth nhanh** → Supabase tốt
- **Cần API logic rõ** → FastAPI tốt
- **Cần search/ranking/ACL chuẩn** → FastAPI + PostgreSQL tốt hơn
- **Cần UI nhanh, đẹp, tương tác cao** → Next.js + Tailwind tốt
- **Cần managed Postgres** → Supabase tốt
- **Cần internal wiki / dashboard / agent UI** → stack này rất hợp

### 5) Supabase PostgreSQL trong stack này nên đóng vai trò gì

Với setup hiện tại, PostgreSQL trên Supabase nên là:

- nguồn dữ liệu chính cho pages, tags, links, sources, ACL
- nơi chạy full-text search và fuzzy search
- nơi giữ runtime metadata như sessions, logs, sync state
- nơi query backend đọc để phục vụ UI

Nên tránh:
- coi Supabase/Postgres như nơi viết content thủ công thay cho markdown
- dùng nhiều logic content trực tiếp ở UI mà không qua backend policy

### 6) Khi nào stack này là lựa chọn đúng

Stack này rất hợp nếu bạn đang làm:
- internal wiki
- knowledge dashboard
- document explorer
- AI tutor / chat interface
- search-heavy web app
- admin console có permissions
- app có nhiều trang nhưng đội nhỏ

### 7) Pitfalls cần tránh

- Không để Next.js tự gánh logic nghiệp vụ phức tạp nếu backend đã có FastAPI.
- Không để Supabase auth và backend auth tách policy mà không có rule chung.
- Không để search logic nằm rải rác ở frontend.
- Không để UI đọc markdown trực tiếp trong production nếu DB đã là runtime layer.
- Không trộn content source of truth với runtime cache.

### 8) Conventions nên giữ

- Types được chia sẻ rõ ràng giữa UI và API nếu cần.
- Validation và ACL nằm ở backend.
- UI chỉ render, submit, filter, và show state.
- Search ranking, logging, sync, audit đều ở backend/DB.
- Migration, schema, và policy đi qua một pipeline rõ.

### 9) Khuyến nghị cho dự án này

Nếu mục tiêu là app nội bộ ổn định và lâu dài, nên chọn:

- Next.js + TypeScript + Tailwind cho UI
- FastAPI cho backend chính
- Supabase PostgreSQL làm DB managed
- Supabase Auth/Storage chỉ khi đúng nhu cầu

Đây là lựa chọn cân bằng giữa tốc độ phát triển và khả năng kiểm soát kiến trúc.

## Thực hành / Ví dụ

Một setup thực tế có thể tách như sau:

- `apps/web` → Next.js + TypeScript + Tailwind
- `apps/api` → FastAPI
- `db/` hoặc `infra/` → Supabase schema / migrations
- `wiki/` → markdown source of truth
- sync pipeline → markdown → PostgreSQL

Ví dụ luồng search:

- UI gửi query
- FastAPI search pages trong PostgreSQL
- backend trả results đã lọc ACL
- UI render cards, backlinks, snippets

## Lưu ý & Pitfalls

- Supabase rất mạnh, nhưng đừng để nó làm mờ ranh giới giữa content và runtime.
- FastAPI nên giữ vai trò policy gate thay vì chỉ là proxy mỏng nếu app có ACL/search logic.
- Nếu chỉ cần MVP nhỏ, stack này có thể hơi nhiều lớp; nhưng với internal wiki, đó là trade-off đáng giá.

## Liên quan

- [[hybrid-search]] — search khi corpus lớn hơn
- [[ai-coding-workflows]] — quy trình build/verify với AI
- [[rag]] — nếu sau này thêm semantic retrieval
- [[cursor-agent]] — nếu dùng agent để xây UI/backend nhanh hơn
- [[knowledge-base]] — nền tảng tri thức của app

## Nguồn

- https://nextjs.org/docs
- https://www.tailwindcss.com/docs
- https://fastapi.tiangolo.com/
- https://supabase.com/docs
- https://www.postgresql.org/docs/
