---
title: "Hướng dẫn thêm tài liệu vào raw/"
url: ""
author: "System"
discovered: 2026-04-20
topic: "Meta"
---

# Cách thêm tài liệu

Đặt file của bạn vào đúng thư mục con:

- `raw/articles/`   ← Blog posts, bài báo, papers (copy/paste text hoặc .md)
- `raw/notes/`      ← Ghi chú cá nhân khi học, khi code
- `raw/slides/`     ← Nội dung từ slide deck (export ra text hoặc .md)
- `raw/videos/`     ← YouTube URL, transcript, hoặc tóm tắt từ video
- `raw/repos/`      ← Code patterns, README hay từ GitHub repos

Sau khi thêm file, chạy: `/llm-wiki ingest`

## Format file markdown (khuyên dùng)

```markdown
---
title: "Tiêu đề tài liệu"
url: "https://nguon-goc.com/bai-viet"
author: "Tên tác giả"
discovered: 2026-04-20
topic: "Vibe Coding"
---

Nội dung ở đây...
```

## Xóa file này

File này chỉ là hướng dẫn. Khi bạn đã quen, có thể xóa.
