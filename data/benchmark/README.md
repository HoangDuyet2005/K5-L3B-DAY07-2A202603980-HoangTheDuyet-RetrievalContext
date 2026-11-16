# Benchmark Day 7

Corpus: World Bank, *Poverty, Prosperity, and Planet Report 2024*, Overview (PDF pages 35–73), CC BY 3.0 IGO. Index: Day 6 `day6_chunks`, strategy B (130 chunks). Questions are in English, the language of the corpus.

| Split | Có đáp án | Thiếu bằng chứng | Nguồn |
|---|---:|---:|---|
| dev | 20 | 3 | 20 câu Day 6 (q01–q20) + 3 câu mới |
| test | 9 | 3 | Toàn bộ mới, viết cho Day 7 |
| **Tổng** | **29** | **6** | 35 câu |

## Files

- `questions.json`: câu có đáp án theo [định dạng Day 7](../README.md): `id`, `split`, `question`, `expected_answer`, `gold` (`source_id`, `page` = trang PDF, `evidence` nguyên văn), cùng `type`, `section`, `filter` (nếu có), `origin`, `review_status`, `review_note`. Dùng cho retrieval metrics (`starter/baseline.py`).
- `cases.json`: mọi câu, có `answerable`, `expected_behavior`; câu thiếu bằng chứng có `absence_reason` và `absence_check`. Dùng cho agent và `starter/agent_metrics.py`.

Agent và retriever chỉ được nhận `question` và `filter`. Không đưa `expected_answer`, `gold`, `absence_reason` hay nhãn vào model, query hoặc filter.

## Chia split

- Cả 20 câu Day 6 (gồm 5 câu test Day 6) đã được xem khi phát triển Day 6, nên chỉ dùng làm **dev** Day 7.
- Câu test có đáp án lấy từ các trang chưa từng làm gold ở Day 6 (39, 47, 52, 53, 56, 60, 63, 70, 72). Trang 42 được dùng làm evidence thay thế cho dev-q05 nên không dùng cho test.
- Corpus chỉ có một tài liệu nên chủ đề (nghèo đói, IDA, rủi ro khí hậu, phát thải) lặp giữa dev và test. Rủi ro rò rỉ này được ghi nhận, không loại bỏ được.
- Benchmark được viết và khóa trước mọi lần chạy retrieval hay agent của Day 7.

## Evidence

- Mỗi evidence phải nằm trọn trong một chunk B đúng `source_id` và trang, và xuất hiện trong text pypdf của trang đó sau khi gộp khoảng trắng.
- dev-q05: evidence Day 6 vắt qua hai chunk (p41 c002 và c003), nên được thay bằng hai evidence thay thế, mỗi cái nằm trong một chunk: định nghĩa ở p41 và định nghĩa trong Box O.1 ở p42.
- Câu `metadata_filter` có `filter.section` do người dùng nêu trong câu hỏi; section này chứa chunk gold, và cùng chủ đề có xuất hiện ở section khác.

## Câu thiếu bằng chứng

Mỗi câu gần chủ đề của corpus. Cách kiểm tra: tìm từ khóa trong `absence_check.keywords` (không phân biệt hoa thường) trên toàn bộ 130 chunk B và text pypdf của PDF trang 35–73, gồm cả nhãn hình; sau đó đọc tay mọi chỗ khớp. Không kết luận thiếu bằng chứng chỉ vì top-k không tìm thấy.

| ID | Chỗ khớp từ khóa | Kết luận khi đọc tay |
|---|---|---|
| dev-u1 | không có | Không nhắc tới Vietnam |
| dev-u2 | không có | Không nhắc tới IDA21 hay replenishment |
| dev-u3 | p58 c000 (`carbon price`) | Chỉ nói độ phủ carbon pricing và xu hướng giá tổng, không có giá mỗi tấn hay mức khuyến nghị |
| test-u1 | p56 c001 (`philippines`, `pantawid`) | Có nói chương trình hỗ trợ sau bão nhưng không có số hộ; số 100,000/200,000 là của Kenya |
| test-u2 | không có | Không nhắc tới unemployment hay youth |
| test-u3 | p62 c005; nhãn hình PDF 65, 71 (`indonesia`) | p62 chỉ nói Indonesia là nước xuất khẩu than lớn thứ hai; p65 là tên nước trên biểu đồ phát thải/GDP; p65 và p71 không có "coal" hay "export" |

## Kiểm tra lại

```bash
<day6>/starter/.venv/Scripts/python.exe -m src.check_day6 export --output starter/data/day6/chunks_B.json
<day6>/starter/.venv/Scripts/python.exe -m src.verify_benchmark --chunks starter/data/day6/chunks_B.json --pdf "<PDF>"
```

Kết quả mong đợi: `"ok": true`, `chunks_B.json` sha256 `a78d08254714780fbf43c0d3f1d8a16f002d716ba4ccc78956b309674f6bd78b`.

## Trạng thái

Bản nháp do trợ lý AI soạn. Học viên đã đối chiếu từng câu test, dev-q05 và các câu thiếu bằng chứng với PDF ngày 2026-11-16 (`review_status` = `student_reviewed_2026-11-16`). Benchmark được khóa bằng commit trước mọi lần chạy thử nghiệm; `verify_report.json` ghi sha256 của các file lúc khóa. Không sửa `questions.json` hoặc `cases.json` sau khi khóa; nếu buộc phải sửa, ghi lý do và tạo phiên bản mới.
