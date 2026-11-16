# Nhật ký thử nghiệm Day 7

Mọi thử nghiệm chạy trên **dev** của benchmark đã khóa (`data/benchmark/questions.json`, sha256 `5f4c4046…`). Giả thuyết, dự đoán và tiêu chí chọn được ghi **trước khi chạy** và commit riêng; kết quả được ghi sau, kể cả khi không cải thiện. Test chỉ chạy một lần, sau khi khóa cấu hình.

**Về bộ dev:** 20 câu dev có đáp án được **tái sử dụng từ benchmark Day 6** (q01–q20), trong đó 5 câu (dev-q16 … dev-q20) từng là test Day 6. Tất cả đã được xem khi phát triển Day 6, nên chỉ dùng để chẩn đoán và chọn cấu hình, **không phải holdout** Day 7. Holdout Day 7 là bộ test mới (9 câu có đáp án + 3 câu thiếu bằng chứng), chưa dùng ở Day 6. 3 câu dev thiếu bằng chứng là câu mới.

## 0. Kết quả đã có (trước khi ghi file này)

Run `retrieval_dev_20261116T050028Z` (commit `f46c889`), 20 câu dev có đáp án, top-3, candidate pool 10, context budget 800 ký tự (starter `pack_context`, tính cả header).

| Phương pháp | Hit@1 | Evidence Hit@3 | MRR@10 | Context Evidence Rate |
|---|---|---|---|---|
| Dense (**baseline**, bắt buộc) | 16/20 | 20/20 | 0.875 | 6/20 |
| BM25 | 18/20 | 20/20 | 0.950 | 7/20 |
| Hybrid RRF (k = 60) | 18/20 | 20/20 | 0.950 | 7/20 |

Quan sát dẫn tới các giả thuyết dưới đây:
- 10–11 câu có chunk đúng ở hạng 1 nhưng khối chunk dài 804–877 ký tự (> 800), nên `pack_context` bỏ qua. Context trung bình chỉ khoảng 1 chunk.
- Lỗi top-1 của dense là chọn **đoạn cùng chủ đề nhưng sai đoạn** (dev-q01, dev-q04, dev-q19) hoặc thiếu khớp tên riêng (dev-q15 "Brazil"). Hybrid giữ được BM25 ở 18/20 nhưng không sửa được dev-q01 và dev-q19.
- Evidence Hit@3 đạt trần 20/20 với cả ba phương pháp: dev dễ ở mốc top-3 vì nhiều câu Day 6 dùng lại từ ngữ của nguồn. Đây là một giới hạn của benchmark, nên **không dùng Evidence Hit@3 một mình để chọn**; so sánh bằng Hit@1, MRR@10 và Context Evidence Rate.
- Context Evidence Rate thấp (6–7/20) là vấn đề chính cần xử lý trên dev.

## 1. Tiêu chí chọn cấu hình (chốt trước khi chạy E1, E2)

**Bước A, chọn ứng viên ở tầng retrieval** (không gọi model), theo thứ tự:
1. Context Evidence Rate trên dev cao nhất (evidence có tới được model không);
2. nếu bằng nhau: Hit@1 cao hơn;
3. nếu bằng nhau: MRR@10 cao hơn (chunk đúng đứng sớm hơn trong pool);
4. nếu vẫn bằng: context ngắn hơn (ít token gửi model hơn), rồi thời gian retrieval thấp hơn.

Evidence Hit@3 vẫn được báo cáo nhưng không dùng để chọn, vì đã đạt trần 20/20 trên dev.

**Bước B, xác nhận bằng agent trên dev** (Gemini; baseline dense/800 và ứng viên từ bước A, cùng 23 câu dev):
- Giữ ứng viên nếu điểm grounded answer trung bình (/2, chấm tay) **không thấp hơn** baseline và số câu thiếu bằng chứng được từ chối đúng **không ít hơn** baseline.
- Nếu không đạt: báo cáo lý do, chọn cấu hình có grounded answer cao hơn; hòa thì chọn cấu hình rẻ hơn (ít token hơn).

Không thay đổi tiêu chí này sau khi thấy kết quả. Nếu buộc phải thay đổi, ghi lý do và thời điểm.

## 2. Thử nghiệm dự kiến

### E1: rerank bằng cross-encoder

- **Thay đổi:** Hybrid RRF lấy top-10, sau đó `cross-encoder/ms-marco-MiniLM-L-6-v2` (chạy local qua sentence-transformers `CrossEncoder`, học viên duyệt ngày 2026-11-16) chấm lại từng cặp (câu hỏi, chunk), rồi lấy top-3. Budget giữ 800 để tách riêng tác động của rerank.
- **Giả thuyết:** cross-encoder đọc câu hỏi và chunk cùng lúc nên phân biệt được đoạn đúng với đoạn cùng chủ đề, là kiểu lỗi của dev-q01 và dev-q19.
- **Dự đoán:** Hit@1 > 18/20 và MRR@10 > 0.950; Evidence Hit@3 giữ 20/20; mỗi câu chậm thêm vài trăm ms trên CPU; không đổi chi phí tiền.
- **Rủi ro:** model huấn luyện trên MS MARCO (câu hỏi tìm kiếm web), có thể không hợp với câu hỏi số liệu dài; context vẫn bị giới hạn 800 nên Context Evidence Rate có thể không tăng.

### E2: nâng context budget

- **Thay đổi:** budget 800 → **2.700 ký tự** cho mọi phương pháp (dense, BM25, hybrid RRF, và E1). 2.700 ≥ 3 × 885 (khối chunk dài nhất) + 2 dấu phân cách, nên top-3 luôn vừa.
- **Giả thuyết:** Context Evidence Rate thấp chỉ vì chunk đúng dài hơn budget, không phải do xếp hạng sai.
- **Dự đoán:** Context Evidence Rate xấp xỉ Evidence Hit@3 (gần 20/20) với mọi phương pháp; context dài khoảng 3 lần, nên token input của agent tăng tương ứng.
- **Rủi ro:** context dài hơn có thể chứa đoạn gây nhiễu, làm agent trả lời sai hoặc trích dẫn sai; điều này chỉ đo được ở bước B.

## 3. Kết quả

(Ghi sau khi chạy: run ID, commit, bảng số liệu, so sánh với dự đoán, kết luận.)
