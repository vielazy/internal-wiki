# Wiki Log — AI Coding Wiki

> Nhật ký tự động — APPEND ONLY, không xóa entries cũ.
> Mọi hành động của LLM đều được ghi ở đây.

---

[2026-04-20 00:00] [INIT] Khởi tạo AI Coding Wiki. Tạo cấu trúc thư mục, CLAUDE.md, AGENTS.md, config.yaml, wiki/INDEX.md.
[2026-04-20 00:10] [DISCOVER] Tìm và lưu nguồn mới cho Vibe Coding, AI Agents, Prompt Engineering vào .discoveries/.
[2026-04-20 00:10] [INGEST] Tạo 3 trang concepts đầu tiên: vibe-coding, ai-agents, prompt-engineering.
[2026-04-20 00:10] [INDEX] Cập nhật wiki/INDEX.md với 3 pages mới.
[2026-04-20 00:20] [LINT] Phát hiện broken links tới [[mcp]], [[tool-use]], [[prompt-templates]], [[evals]] từ các trang concepts.
[2026-04-20 00:20] [INGEST] Tạo các trang còn thiếu: tools/mcp, concepts/tool-use, concepts/prompt-templates, concepts/evals.
[2026-04-20 00:20] [INDEX] Cập nhật wiki/INDEX.md với cross-references mới và thống kê hiện tại.
[2026-04-20 00:30] [DISCOVER] Tìm nguồn cho LLM Tools & Platforms, Knowledge Base & RAG, Web & App Development, AI Coding Workflows.
[2026-04-20 00:30] [INGEST] Tạo 6 trang mới: tools/cursor-agent, tools/claude-code, concepts/rag, concepts/knowledge-base, concepts/evals, concepts/ai-coding-workflows.
[2026-04-20 00:30] [INDEX] Cập nhật wiki/INDEX.md với 9 pages tổng cộng.
[2026-04-20 00:40] [LINT] Kiểm tra toàn wiki: không có broken links, không có contradictions.
[2026-04-20 00:40] [INGEST] Tạo tutorials/bat-dau-vibe-coding và syntheses/so-sanh-tools.
[2026-04-20 00:40] [INDEX] Cập nhật wiki/INDEX.md với tutorials/ và syntheses/ coverage ban đầu.
[2026-04-20 00:50] [CONFIG] Thêm .obsidian/app.json để loại trừ system files khỏi graph.
[2026-04-20 00:50] [REFACTOR] Bổ sung cross-references cho ai-coding-workflows, plan-mode, contextual-retrieval, cursor-agent-best-practices để giảm isolated pages.
[2026-04-20 00:50] [INDEX] Cập nhật wiki/INDEX.md với 20 pages và coverage mới cho agents/code-patterns.
[2026-04-20 01:00] [CONFIG] Cập nhật roadmap cho content expansion / automation / productization.
[2026-04-20 01:10] [CONFIG] Cập nhật README cho automation và prompt library.
[2026-04-20 01:20] [AUTOMATION] Thêm scripts/run_cycle.ps1 và scripts/setup_scheduler.ps1 cho Windows Task Scheduler.
[2026-04-20 01:30] [CODE] Tinh chỉnh repo ingest agent và cập nhật README cho bước automation tiếp theo.
[2026-04-20 01:40] [INGEST] Tạo wiki/code-patterns/prompt-library.md cho prompt templates dùng lại.
[2026-04-20 01:50] [INGEST] Tạo wiki/agents/tutor-agent.md cho chat/tutor agent đọc wiki trước khi trả lời.
[2026-04-20 01:50] [INDEX] Cập nhật wiki/INDEX.md với agents/tutor-agent và tổng 22 pages.
[2026-04-20 02:00] [INGEST] Tạo skill-graph và learning-path để track skill progress.
[2026-04-20 02:00] [INDEX] Cập nhật wiki/INDEX.md với 24 pages.
[2026-04-20 02:10] [INGEST] Tạo syntheses/hybrid-search để chuẩn bị search tốt hơn cho wiki lớn.
[2026-04-20 02:10] [INDEX] Cập nhật wiki/INDEX.md với 25 pages.
[2026-04-20 14:42] [CODE] Nâng cấp wiki-viewer từ dashboard tĩnh sang local app động, đọc runtime data từ wiki/ và wiki/LOG.md qua scripts/wiki_server.py.
[2026-04-20 14:42] [CONFIG] Cập nhật README với hướng dẫn chạy dynamic viewer và debug bootstrap JSON.
[2026-04-20 14:59] [INDEX] Đồng bộ lại wiki/INDEX.md với số file thực tế trong wiki/ và bổ sung links tới mcp, prompt-library.
[2026-04-20 15:17] [DB] Thêm PostgreSQL MVP theo mô hình hybrid: .env.example, requirements.txt, docker-compose.yml, db_init.sql, sync_wiki_to_db.py.
[2026-04-20 15:17] [CODE] Refactor scripts/wiki_server.py sang file/db mode và tách logic runtime chung vào scripts/wiki_runtime.py.
[2026-04-20 15:17] [CONFIG] Cập nhật AGENTS.md và README.md cho workflow markdown source of truth + PostgreSQL derived state.
[2026-04-28 00:00] [CONFIG] Đồng bộ lại config.yaml theo master guide: thêm Knowledge Ops & Productization, search_mode PostgreSQL, và Obsidian role rõ ràng.
[2026-04-28 00:00] [INDEX] Xác nhận lại wiki/INDEX.md như nguồn điều hướng chính cho query, giữ topic coverage hiện tại.
[2026-04-28 00:00] [CODE] Cập nhật runtime search để ưu tiên PostgreSQL khi DB mode bật, giữ file mode cho dev/debug.
[2026-04-28 00:00] [DOCS] Thêm AI_CODING_WIKI_GUIDE.md làm master guide và cập nhật README/CLAUDE.md/AGENTS.md theo mô hình source-of-truth mới.
