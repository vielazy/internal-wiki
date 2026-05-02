# Wiki Index — AI Coding Wiki

> Danh mục tự động — được LLM cập nhật sau mỗi lần ingest.
> Cập nhật lần cuối: 2026-04-20

## Thống kê

| Topic | Số trang | Cập nhật gần nhất |
|---|---|---|
| concepts/ | 13 | 2026-04-20 |
| tools/ | 3 | 2026-04-20 |
| tutorials/ | 1 | 2026-04-20 |
| agents/ | 3 | 2026-04-20 |
| code-patterns/ | 3 | 2026-04-20 |
| syntheses/ | 2 | 2026-04-20 |
| **Tổng** | **25** | 2026-04-20 |

## Topics

### Vibe Coding
_Kỹ thuật lập trình với AI làm driver, human làm director_
- [[vibe-coding]] — nền tảng agentic coding và plan-first workflow
- [[software-is-changing-again]] — Software 3.0, partial autonomy, AI on the leash

### AI Agents
_Kiến trúc, patterns và implementation của AI agents_
- [[ai-agents]] — tool use, MCP, skills, và orchestration
- [[agent-patterns]] — ReAct, Plan-and-Execute, memory, tool-use loop
- [[multi-agent]] — orchestration và handoff giữa agents
- [[tutor-agent]] — agent đọc wiki trước khi trả lời, lưu Q&A vào outputs/

### Prompt Engineering
_Kỹ thuật viết prompt hiệu quả cho LLMs_
- [[prompt-engineering]] — structured prompts, guardrails, evaluation
- [[prompt-templates]] — mẫu prompt tái sử dụng cho workflows lặp lại

### LLM Tools & Platforms
_Các công cụ, framework và platform AI coding phổ biến_
- [[cursor-agent]] — agent-centric IDE workflow, plan mode, review loop
- [[claude-code]] — coding workflow của Anthropic trong hệ sinh thái Claude
- [[mcp]] — protocol chuẩn hóa để agent kết nối tools, data sources, và services

### Knowledge Base & RAG
_Xây dựng hệ thống knowledge base với LLM_
- [[knowledge-base]] — markdown knowledge base, structure, cross-links
- [[rag]] — retrieval augmented generation trên corpus có cấu trúc
- [[contextual-retrieval]] — retrieval theo ngữ cảnh để tăng độ chính xác

### Web & App Development
_Stack và patterns để build ứng dụng qua vibe coding_
- [[bat-dau-vibe-coding]] — tutorial từ zero đến project chạy được bằng AI
- [[review]] — tutorial về quy trình review diff và kiểm tra thay đổi
- [[debug]] — tutorial về debug có hệ thống theo root cause và verify
- [[tdd]] — tutorial về TDD cho AI coding workflows

### Syntheses — Architecture & Production
- [[wiki-architecture-map]] — bản đồ điều hướng kiến trúc và tài liệu dự án
- [[internal-wiki-architecture-recommendation]] — khuyến nghị kiến trúc production cho internal wiki
- [[internal-wiki-production-bundle]] — bundle đọc nhanh cho toàn bộ lớp production
- [[internal-wiki-production-checklist]] — checklist triển khai production cho internal wiki
- [[internal-wiki-launch-checklist]] — checklist sẵn sàng launch internal wiki
- [[deployment-roadmap-and-gap-audit]] — roadmap triển khai + gap audit trước go-live
- [[supabase-auth-rls-backend-acl-flow]] — flow end-to-end cho auth + RLS + backend ACL
- [[supabase-auth-acl-model]] — mô hình auth + ACL cho internal wiki
- [[supabase-rls-vs-app-layer-acl]] — so sánh RLS và app-layer ACL
- [[supabase-postgresql-search]] — strategy search trong Supabase/Postgres

### Syntheses — Stack & Search
- [[nextjs-fastapi-supabase-architecture]] — synthesis lớn cho stack Next.js + TypeScript + Tailwind + FastAPI + Supabase
- [[nextjs-fastapi-supabase-decision-guide]] — checklist rút gọn để chọn kiến trúc nhanh
- [[hybrid-search]] — hướng search khi wiki lớn lên
- [[so-sanh-tools]] — so sánh các công cụ / workflows quan trọng

### AI Coding Workflows
_Quy trình, checklist và best practices khi code với AI_
- [[evals]] — đánh giá output của prompt, agent, retrieval và app workflows
- [[ai-coding-workflows]] — workflow tổng quát để plan, build, verify với AI
- [[skill-graph]] — track kỹ năng, mức độ nắm vững, và gaps
- [[learning-path]] — lộ trình học theo thứ tự hợp lý từ cơ bản đến nâng cao
- [[project-priority-plan]] — bản điều hướng ưu tiên theo impact cho các việc tiếp theo

### Code Patterns
- [[claude-md-template]] — template chuẩn cho instructions file trong project
- [[prompt-library]] — thư viện prompt đã kiểm chứng cho ingest, query, lint, automation
- [[prompt-templates]] — các prompt pattern tái sử dụng khi vibe coding
- [[quiz-pack.schema.json]] — schema chuẩn cho quiz pack
- [[agent-vm-api-contract]] — API contract cho agent VM sau này
- [[quiz-generation-for-search-queries]] — cách sinh quiz từ nội dung search query
- [[quiz-and-learning-agent-workflow]] — workflow quiz + learning agent chạy trên VM

## Gaps được phát hiện
> _(Được cập nhật bởi `/llm-wiki lint`)

- Coverage đã khá tốt; tiếp theo nên mở rộng `tutorials/` với thêm stack thực chiến
- `Web & App Development` còn mỏng, nên bổ sung tutorial và synthesis cho Next.js / TypeScript / Tailwind / FastAPI / Supabase
- Có thể bổ sung thêm pages cho `rag`, `mcp`, `skills`, và `plan-mode` nếu muốn sâu hơn
- Nên thêm các page thuộc nhóm `Knowledge Ops & Productization` để phản ánh hướng scale mới
- Đã thêm 3 tutorial gap ưu tiên cao: `review`, `debug`, `tdd`
- Đã thêm synthesis lớn cho stack `Next.js + TypeScript + Tailwind + FastAPI + Supabase`

## Hướng dẫn sử dụng Index này

Khi LLM nhận lệnh query, đọc file này trước để biết trang nào tồn tại,
rồi mới đọc các trang cụ thể. Không đọc toàn bộ wiki khi không cần.

## Hướng ưu tiên tiếp theo

- Mở rộng search & retrieval trên PostgreSQL thay vì đọc file trực tiếp ở runtime production
- Bổ sung revision history và sync metadata nếu cần audit/rollback
- Tăng coverage cho `tutorials/` và `syntheses/`
- Bổ sung các trang còn thiếu cho `rag`, `mcp`, `skills`, và `plan-mode` khi có nguồn phù hợp
- Ưu tiên theo dõi `PROJECT_PRIORITY_PLAN.md` để biết việc nào impact cao, medium, hoặc để sau
