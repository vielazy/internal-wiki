# LLM Wiki Skill — AI Coding Wiki

Skill này định nghĩa các lệnh `/llm-wiki` cho Claude Code.
Đọc `CLAUDE.md` ở root để biết schema đầy đủ trước khi thực thi.

## Trigger

Skill này được gọi khi user dùng lệnh `/llm-wiki [command]`

## Mapping lệnh

### `/llm-wiki run`
Thực hiện tuần tự: discover → ingest → lint → cập nhật INDEX.md → ghi LOG.md

### `/llm-wiki discover`
1. Đọc config.yaml để lấy danh sách topics và keywords
2. Tìm kiếm web cho từng topic (ưu tiên priority: high trước)
3. Đánh giá relevance (1-5), lưu những nguồn ≥ 3 vào .discoveries/
4. Báo cáo: "Tìm được X nguồn mới, Y nguồn có relevance cao"

### `/llm-wiki ingest [optional: file]`
1. Quét raw/ để tìm files chưa được xử lý (so sánh với LOG.md)
2. Với mỗi file: đọc → extract → tạo/cập nhật wiki page theo template
3. Tạo cross-references, đánh dấu contradictions
4. Cập nhật wiki/INDEX.md
5. Append vào wiki/LOG.md

### `/llm-wiki query "[câu hỏi]"`
1. Đọc wiki/INDEX.md
2. Xác định trang liên quan
3. Đọc các trang đó
4. Trả lời grounded từ wiki
5. Lưu vào outputs/queries/YYYY-MM-DD.md

### `/llm-wiki lint`
Kiểm tra và báo cáo:
- Orphan pages (không được link tới)
- Broken internal links
- Pages với confidence: low
- Topics chưa có coverage
- Contradictions chưa được resolve
Output: outputs/lint-YYYY-MM-DD.md

### `/llm-wiki status`
Đọc wiki/INDEX.md + wiki/LOG.md, báo cáo nhanh:
- Tổng số trang, phân bố theo topic
- Số file raw/ chưa ingest
- Ngày chạy gần nhất
- Top gaps

### `/llm-wiki digest`
Tóm tắt tuần/ngày: nguồn mới, trang mới, insights nổi bật
Output: outputs/digest-YYYY-MM-DD.md

### `/llm-wiki init "[Topic]"`
1. Thêm topic vào config.yaml
2. Tạo folder wiki/[topic-slug]/
3. Tạo trang INDEX cho topic
4. Chạy discover cho topic mới

## Quy tắc khi thực thi

- Luôn ghi LOG.md sau mỗi action
- Không sửa raw/ dù bất kỳ lý do gì
- Nếu không chắc, đặt confidence: low và ghi rõ
- Tiếng Việt là chính, giữ nguyên technical terms
