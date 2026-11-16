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

### S1: chạy thử agent (smoke test), không phải thử nghiệm cải thiện

- **Run:** `agent_dev_dense_b800_smoke_20261116T052845Z`. Mục đích: kiểm tra toàn bộ chuỗi Gemini → search → context → answer/abstain trước khi chạy đủ dev.
- **Code:** chạy lúc code chưa commit, nhưng mọi file code được sửa lần cuối trước lúc chạy (05:28:45 UTC) và được commit nguyên trạng ở `e839b10`. `run_metadata.json` ghi các file này là untracked tại thời điểm chạy.
- **Cấu hình:** baseline agent: dense, top-3, budget 800 ký tự, tối đa 3 search, `gemini-3.5-flash` (response ghi `modelVersion` = `gemini-3.6-flash` ở cả 14 lần gọi).
- **Câu chạy:** dev-q01, dev-q04, dev-q09, dev-u1.

| Câu | Status | Quan sát (chưa phải nhãn chấm tay chính thức) |
|---|---|---|
| dev-q09 | answered | "2.4 million people… 20 fatalities" `[B:wb-ppp-2024:p057s0:c001]`: khớp đáp án, citation trỏ đúng chunk evidence |
| dev-u1 | abstain | Từ chối sau 3 search; không bịa số liệu |
| dev-q01 | abstain | Từ chối nhầm: context chỉ có `p036s0:c000` (8.5 percent) qua cả 3 lượt; chunk evidence `p035s0:c003` (có 692 million) không nằm trong top-3 của các query agent tự viết |
| dev-q04 | abstain | Từ chối nhầm: lượt search 1 đưa `p041s0:c001` (791 ký tự) vào context; cả 3 lượt đều **tìm thấy** chunk evidence `p041s0:c000` (hạng 3, 3, 2) nhưng nó không vừa budget còn lại, vì `pack_context` giữ chunk cũ trước |

- **Lỗi dev #1 (dev-q04): context bị khóa bởi chunk đầu tiên.** Với budget 800, chunk của lượt search đầu chiếm gần hết budget; evidence tìm thấy ở lượt sau bị bỏ. Agent vẫn từ chối đúng với context nó thấy. Liên quan trực tiếp tới E2.
- **Lỗi dev #2 (dev-q01): thiếu một phần đáp án trong context.** Context chỉ chứa một chunk cùng chủ đề (tỷ lệ 8.5%) nhưng thiếu số người (692 million); agent từ chối thay vì trả lời một nửa. Ở đánh giá retrieval, câu hỏi gốc đưa chunk evidence lên hạng 3 của dense; còn 3 query agent tự viết lại ("extreme poverty 2024 share population people", "8.5 percent 2024 extreme poverty people million"…) không đưa được nó vào top-3. Liên quan tới E1 (xếp lại ứng viên) và E2 (chứa thêm chunk).
- **Thời gian và token:** mỗi lần gọi Gemini mất 15–37 s; mỗi câu 55–128 s (trung vị khoảng 92 s); tổng 12.575 token cho 4 câu (prompt 9.024, output 430, thinking 3.121). Ước tính chạy đủ 23 câu dev mất khoảng 35 phút và khoảng 70k token cho mỗi cấu hình.

### E1 và E2: kết quả retrieval trên dev

- **Runs:** `retrieval_dev_20261116T055416Z` (budget 800) và `retrieval_dev_20261116T055514Z` (budget 2.700), cùng commit `0eb4d4d`, cây code sạch (`dirty_files` chỉ liệt kê thư mục kết quả của chính các run). 20 câu dev có đáp án, top-3, pool 10, chi phí 0 USD.
- **Tái lập:** dense, BM25 và hybrid RRF ở budget 800 ra đúng số liệu của run `retrieval_dev_20261116T050028Z`.

| Phương pháp | Budget | Hit@1 | Evidence Hit@3 | MRR@10 | Context Evidence Rate | Context TB (ký tự) | Median ms |
|---|---|---|---|---|---|---|---|
| Dense (baseline) | 800 | 16/20 | 20/20 | 0.875 | 6/20 | 623.7 | 217 |
| BM25 | 800 | 18/20 | 20/20 | 0.950 | 7/20 | 624.7 | 1 |
| Hybrid RRF | 800 | 18/20 | 20/20 | 0.950 | 7/20 | 581.8 | 221 |
| Hybrid RRF + rerank (E1) | 800 | 18/20 | 20/20 | 0.950 | 8/20 | 602.0 | 639 |
| Dense | 2.700 | 16/20 | 20/20 | 0.875 | **20/20** | 2037.5 | 218 |
| BM25 | 2.700 | 18/20 | 20/20 | 0.950 | **20/20** | 2161.7 | 1 |
| Hybrid RRF | 2.700 | 18/20 | 20/20 | 0.950 | **20/20** | 2129.1 | 217 |
| Hybrid RRF + rerank | 2.700 | 18/20 | 20/20 | 0.950 | **20/20** | 2134.0 | 668 |

**E1 (rerank), so với dự đoán:** **không xác nhận.** Hit@1 giữ 18/20 và MRR@10 giữ 0.950, không vượt như dự đoán. Rerank sửa đúng một lỗi "cùng chủ đề, sai đoạn" theo giả thuyết: dev-q01 đưa chunk evidence từ hạng 2 lên hạng 1. Nhưng nó làm hỏng dev-q05 (hạng 1 xuống hạng 2) và không sửa được dev-q19 (vẫn hạng 2), nên tổng không đổi. Context Evidence Rate ở budget 800 tăng 7 → 8/20 (nhờ dev-q01). Retrieval chậm thêm khoảng 420 ms mỗi câu trên CPU. Rủi ro ghi trước ("model MS MARCO có thể không hợp câu hỏi số liệu") phù hợp với kết quả hòa này.

**E2 (budget 2.700), so với dự đoán:** **xác nhận.** Context Evidence Rate tăng từ 6–8/20 lên 20/20 ở cả 4 phương pháp, bằng Evidence Hit@3, như dự đoán. Nguyên nhân Context Evidence Rate thấp đúng là budget, không phải xếp hạng. Đổi lại, context dài hơn khoảng 3,3–3,7 lần (khoảng 600 → khoảng 2.040–2.160 ký tự), nên token input của agent tăng tương ứng.

**Bước A (tiêu chí ở mục 1), áp dụng đúng thứ tự đã chốt:**
1. Context Evidence Rate: 4 cấu hình budget 2.700 hòa 20/20; các cấu hình 800 bị loại.
2. Hit@1: BM25, hybrid RRF, hybrid RRF + rerank hòa 18/20; dense (16/20) bị loại.
3. MRR@10: ba cấu hình còn lại hòa 0.950.
4. Context ngắn hơn: hybrid RRF 2129.1 < rerank 2134.0 < BM25 2161.7.

→ **Ứng viên: hybrid RRF, budget 2.700.** Chênh lệch ở bước 4 rất nhỏ (khoảng 5–33 ký tự trung bình), nên trên dev ba ứng viên gần như ngang nhau; việc chọn hybrid RRF là theo đúng tiêu chí đã ghi, không phải vì nó tốt hơn rõ rệt. Metric này đo bằng **câu hỏi gốc**; agent sẽ tự viết query, nên bước B (agent trên dev) mới là xác nhận thực tế.

**Bước B, dự kiến:** chạy agent Gemini đủ 23 câu dev cho baseline (dense, 800) và ứng viên (hybrid RRF, 2.700), cùng `max_searches` = 3, rồi chấm tay grounded answer, citation và abstention.

### Sự cố S2: hết hạn mức gói miễn phí, đổi agent model (2026-11-16)

- **Chuyện gì xảy ra:** lần chạy bước B đầu tiên (baseline dense/800, commit `8d3450e`, bắt đầu 07:19 UTC) chạy được dev-q01 (abstain) và dev-q02 (answered); từ dev-q03 trở đi mọi câu báo `error`. Request chẩn đoán trả về `HTTP 429 RESOURCE_EXHAUSTED: generate_content_free_tier_requests, limit: 20, model: gemini-3.6-flash` (quota `GenerateRequestsPerDayPerProjectPerModel-FreeTier`). Gói miễn phí của `gemini-3.5-flash` (Google phục vụ bằng `gemini-3.6-flash`) chỉ cho 20 request/ngày; chạy thử ở chặng 0 và S1 cùng 9 request của lần chạy này đã dùng hết.
- **Xử lý:** dừng lần chạy ở dev-q07. Không có file kết quả nào được giữ, vì code cũ chỉ ghi trace khi chạy xong cả lượt, nên kết quả của dev-q01 và dev-q02 bị mất; lần chạy này không được dùng để chọn cấu hình.
- **Đổi agent model** (học viên duyệt) sang `gemini-3.5-flash-lite`: cùng thế hệ 3.5, gói miễn phí 500 request/ngày (theo trang Rate limit của AI Studio, project của học viên). Dự phòng: `gemini-3.1-flash-lite` (500/ngày). Việc đổi xảy ra **trước mọi lần chạy agent chính thức**; baseline và ứng viên dùng cùng model mới. Run thử S1 giữ lại làm tư liệu và được ghi rõ là dùng model cũ.
- **Sửa code để không lặp lại:** ghi trace ngay sau mỗi câu; dừng cả lượt khi gặp lỗi hết hạn mức trong ngày (lỗi 429 tạm thời theo phút vẫn được thử lại); `run_metadata.json` ghi `completed` và `aborted_reason`.
