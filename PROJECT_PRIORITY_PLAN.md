# AI Coding Wiki — Project Priority Plan

Tài liệu này là bản điều hướng ưu tiên cho các việc tiếp theo của dự án, dựa trên trạng thái hiện tại.

Nó nên được đọc cùng với:
- `AI_CODING_WIKI_GUIDE.md`
- `CLAUDE.md`
- `AGENTS.md`
- `README.md`

## Mục tiêu của bản này

- cho biết việc nào nên làm trước
- phân loại theo mức tác động
- tránh làm lan man sang các hạng mục chưa cần thiết
- giữ dự án đi đúng hướng: wiki source of truth, PostgreSQL derived state, Obsidian là authoring/exploration

---

## 1) Việc impact cao

Đây là các việc nên ưu tiên làm ngay vì tác động trực tiếp đến chất lượng hệ thống.

### A. Hoàn thiện search trên PostgreSQL
**Vì sao cao:** đây là nền tảng để app nội bộ chạy nhanh và scale được.

Nên làm:
- thêm full-text search index cho `pages`
- thêm `pg_trgm` cho fuzzy search
- chuẩn hóa ranking theo `title`, `tags`, `excerpt`, `body`
- đảm bảo search luôn ACL-aware
- log query để tune relevance

Kết quả mong đợi:
- search nhanh hơn rõ rệt
- giảm phụ thuộc vào scan file markdown
- trải nghiệm query ổn định hơn khi wiki lớn lên

### B. Chuẩn hóa sync markdown → PostgreSQL
**Vì sao cao:** nếu sync không ổn định thì mọi thứ phía trên đều yếu.

Nên làm:
- incremental sync
- idempotent sync
- transaction-safe sync
- sync state theo hash / timestamp
- có job log rõ ràng

Kết quả mong đợi:
- DB luôn phản ánh đúng content mới
- giảm drift giữa `wiki/` và DB
- dễ debug khi có lỗi ingest/update

### C. Đảm bảo permissions / ACL hoạt động thật sự ở runtime
**Vì sao cao:** đây là nền tảng để dự án tiến thành internal wiki.

Nên làm:
- enforce visibility khi search
- enforce ACL khi fetch page
- backlinks/related pages cũng phải respect quyền
- query logs không leak nội dung riêng tư

Kết quả mong đợi:
- an toàn hơn
- sẵn sàng cho nội bộ công ty
- ít rủi ro dữ liệu bị lộ

### D. Giữ cấu trúc tài liệu điều hướng nhất quán
**Vì sao cao:** hệ thống này là knowledge base, nên structure rất quan trọng.

Nên làm:
- `AI_CODING_WIKI_GUIDE.md` là bản master
- `CLAUDE.md` / `AGENTS.md` là entrypoint theo tool
- `README.md` trỏ rõ tới guide
- `wiki/INDEX.md` phản ánh đúng priorities hiện tại

Kết quả mong đợi:
- LLM và human đều có cùng điểm tham chiếu
- giảm mâu thuẫn tài liệu
- dễ tiếp tục mở rộng mà không vỡ quy ước

---

## 2) Việc impact medium

Đây là các việc nên làm sau khi đã ổn định nền tảng trên.

### A. Bổ sung page gap ưu tiên cao cho wiki
**Vì sao medium:** tăng coverage nhưng chưa phải bottleneck hạ tầng.

Nên viết thêm các page kiểu:
- `review` / code review with AI
- `debug` / debugging workflow with AI
- `tdd` / test-driven development with AI
- `plan-mode`
- `skills`
- `mcp` sâu hơn nếu cần

Kết quả mong đợi:
- wiki đầy hơn
- tutorial/workflow phong phú hơn
- graph và backlinks có chiều sâu hơn

### B. Mở rộng `tutorials/`
**Vì sao medium:** tutorial giúp thực hành, nhưng sau search/sync/ACL.

Nên có:
- tutorial end-to-end build app
- tutorial cho agent workflow
- tutorial cho ingest/search/review loop

Kết quả mong đợi:
- tăng tính ứng dụng của wiki
- giúp người đọc làm theo dễ hơn

### C. Tách rõ log runtime và log authoring
**Vì sao medium:** hệ thống đã có log, cần chuẩn hóa thêm để khỏi rối.

Nên làm:
- `wiki/LOG.md` chỉ cho hoạt động xây wiki
- DB logs chỉ cho runtime / query / tutor / sync
- output files chỉ cho query/digest/lint

Kết quả mong đợi:
- dễ truy vết
- dễ maintain
- giảm nhầm lẫn giữa hoạt động của LLM và hoạt động của user

### D. Thêm revision history nếu content bắt đầu thay đổi nhiều
**Vì sao medium:** hữu ích, nhưng có thể làm sau khi sync/search đã ổn.

Nên làm:
- `page_revisions`
- content hash theo phiên bản
- archive snapshots nếu cần

Kết quả mong đợi:
- rollback dễ hơn
- audit rõ hơn
- debug content drift tốt hơn

### E. Mở rộng Obsidian workflow nếu muốn dùng sâu hơn
**Vì sao medium:** có ích cho authoring/graph, nhưng không quyết định runtime.

Nên làm:
- đảm bảo vault clean
- tối ưu backlinks / graph
- giữ wikilink chuẩn

Kết quả mong đợi:
- trải nghiệm duyệt knowledge tốt hơn
- authoring thuận tiện hơn

---

## 3) Việc để sau

Đây là các việc hữu ích nhưng chưa cần làm ngay với trạng thái hiện tại.

### A. Semantic / embedding search full scale
**Lý do để sau:**
- lexical search + trigram + ranking thường đủ ở giai đoạn này
- semantic layer chỉ nên thêm khi corpus lớn hơn hoặc use case rõ hơn

### B. Product dashboard lớn / UI phức tạp
**Lý do để sau:**
- backend/search/sync/ACL quan trọng hơn giao diện đẹp lúc này
- UI nên theo sau khi core runtime đã ổn

### C. Multi-agent orchestration nâng cao
**Lý do để sau:**
- cần sau khi core wiki/search đã ổn định
- nếu làm sớm dễ phức tạp hóa hệ thống

### D. Các automation mở rộng chưa có nhu cầu rõ
Ví dụ:
- ingest từ nhiều nguồn exotic
- workflow tự động quá phức tạp
- nhiều agent phụ trợ chưa thật sự cần

**Lý do để sau:**
- dễ tạo thêm maintenance burden
- chưa chắc tăng giá trị ngay

### E. Chuẩn hóa quá sâu phần productization enterprise
Ví dụ:
- ACL phức tạp theo nhóm/role hierarchy lớn
- policy engine riêng
- audit compliance level cao

**Lý do để sau:**
- chỉ cần khi dự án thật sự vào production nội bộ với nhu cầu lớn hơn

---

## 4) Thứ tự khuyến nghị thực thi

Nếu phải chọn thứ tự cụ thể, nên đi như sau:

1. Hoàn thiện PostgreSQL search
2. Chuẩn hóa sync markdown → DB
3. Enforce ACL / visibility ở runtime
4. Giữ docs điều hướng nhất quán
5. Bổ sung page gaps quan trọng
6. Mở rộng tutorials
7. Chuẩn hóa logging / revision history
8. Sau đó mới nghĩ tới semantic search và dashboard lớn

---

## 5) Chốt nhanh theo trạng thái hiện tại

### Nên làm ngay
- search DB
- sync ổn định
- ACL-aware runtime
- điều hướng tài liệu thống nhất

### Nên làm tiếp sau đó
- page gaps
- tutorials
- log/revision cleanup

### Để sau
- semantic search lớn
- UI/dashboard nặng
- multi-agent phức tạp

---

## 6) Ghi chú sử dụng

Tài liệu này là bản điều hướng thực tế, không phải roadmap cố định.
Khi dự án đổi trạng thái, hãy cập nhật lại ưu tiên theo nguyên tắc:
- impact trực tiếp lên search/runtime trước
- content coverage sau
- experimental features để sau cùng
