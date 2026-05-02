---
title: "Prompt Library"
topic: "Code Patterns"
tags: [prompt-library, prompts, claude-md, agents-md, reusable-workflows]
created: 2026-04-20
updated: 2026-04-20
confidence: medium
sources:
  - raw/repos/ingest_repo.py
  - raw/videos/ingest_video.py
  - wiki/code-patterns/claude-md-template.md
  - wiki/code-patterns/prompt-templates.md
---

# Prompt Library

## Tóm tắt

Prompt library là nơi lưu các prompt patterns đã chứng minh hiệu quả trong workflow của dự án: ingest, query, lint, automation và template cho `CLAUDE.md` / `AGENTS.md`.

## Nội dung chính

### 1. Prompt cho ingest YouTube video

```text
Follow AGENTS.md. Đọc raw/videos/[file].md, trích xuất transcript, xác định concept chính, tạo hoặc cập nhật wiki page phù hợp và ghi LOG.md.
```

### 2. Prompt cho ingest GitHub repo

```text
Follow AGENTS.md. Đọc raw/repos/[file].md, trích xuất architecture decisions, patterns, code examples, tạo hoặc cập nhật wiki page phù hợp và ghi LOG.md.
```

### 3. Prompt cho query wiki

```text
Follow AGENTS.md. Đọc wiki/INDEX.md trước, chọn các trang liên quan, trả lời grounded từ wiki và lưu kết quả vào outputs/queries/.
```

### 4. Prompt cho lint

```text
Follow AGENTS.md. Chạy lint toàn wiki, liệt kê broken links, orphan pages, gaps và contradictions. Nếu có vấn đề, ghi rõ file liên quan và hướng xử lý.
```

### 5. Template cho CLAUDE.md / AGENTS.md

Dùng các template trong `wiki/code-patterns/claude-md-template.md` và `wiki/code-patterns/prompt-templates.md` để tạo cấu hình chuẩn cho các project mới.

## Thực hành / Ví dụ

- Dùng prompt ngắn, có action rõ ràng.
- Luôn nêu file cụ thể khi đã biết.
- Giữ convention “Follow AGENTS.md” để thống nhất hành vi agent.

## Lưu ý & Pitfalls

- Prompt library nên lưu các prompt đã kiểm chứng, không phải mọi prompt thử nghiệm.
- Nếu prompt quá dài, nên tách thành nhiều template nhỏ.
- Nên dùng link chéo tới các trang khái niệm để tránh trùng lặp.

## Liên quan

- [[claude-md-template]] — template instructions file cho project
- [[prompt-templates]] — các pattern prompt tái sử dụng
- [[ingest-repo]] — workflow ingest repo từ GitHub URL
- [[ingest-video]] — workflow ingest video từ YouTube URL

## Nguồn

- raw/repos/ingest_repo.py
- raw/videos/ingest_video.py
- wiki/code-patterns/claude-md-template.md
- wiki/code-patterns/prompt-templates.md
