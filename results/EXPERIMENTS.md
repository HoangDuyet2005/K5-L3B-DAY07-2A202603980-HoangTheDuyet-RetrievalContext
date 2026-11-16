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

### S3: chạy thử model mới, sửa prompt về abstention (2026-11-16)

- **Run:** `agent_dev_dense_b800_smoke2_20261116T074153Z` (commit `288ad01`, `gemini-3.5-flash-lite`, dense/800), câu dev-q09 và dev-u1. Model mới nhanh hơn nhiều: 2,9–5,1 s mỗi câu (so với 55–128 s ở S1), không dùng thinking token; 6 request, 4.044 token.
- **dev-q09:** answered, đúng như S1 ("2.4 million… 20 fatalities" `[…p057s0:c001]`).
- **dev-u1 (thiếu bằng chứng):** nội dung là từ chối ("there is no specific data given for Vietnam's extreme poverty rate in 2024"), kèm con số toàn cầu 8.5% có trích dẫn đúng, nhưng model gọi tool `answer` thay vì `abstain`, nên status ghi `answered`. Model cũ (S1) dùng đúng `abstain` cho câu này.
- **Sửa (trước mọi lần chạy agent chính thức, áp dụng như nhau cho mọi cấu hình):** thêm vào system prompt: "Never call `answer` to say that the information is missing or not given; that case must be `abstain`." Sửa dựa trên quan sát ở dev, không dùng test.
- **Kiểm tra sau khi sửa:** run `agent_dev_dense_b800_promptcheck_20261116T074503Z` (prompt mới, trước khi commit), dense/800, ba câu dev: dev-u1 → abstain, dev-u3 → abstain (không nhầm với đoạn nói về carbon pricing), dev-q02 → answered (không từ chối quá mức). 10 request, 6.759 token, 4,2–6,6 s mỗi câu.
- Hai run S3 chỉ là kiểm tra kỹ thuật trên 5 câu dev, không dùng để chọn cấu hình; được lưu ngoài `results/` (thư mục tạm của phiên làm việc) vì chạy khi code chưa commit.

### B0: agent trên toàn bộ dev, baseline và ứng viên (2026-11-16)

- **Runs:** `agent_dev_dense_b800_baseline_20261116T074804Z` và `agent_dev_hybrid_rrf_b2700_candidate_20261116T075344Z`, commit `89e7f8b`, `gemini-3.5-flash-lite`, `max_searches` = 3, 23 câu dev mỗi cấu hình, 0 lỗi provider, 0 USD (free tier).
- **Nhãn:** Claude chấm nháp (`labels.csv`, `review_sheet.md`); B0 **không dùng để chốt cấu hình** vì phát hiện lỗi định dạng citation dưới đây và được thay bằng B1. Nhãn B0 giữ lại để đối chiếu trước/sau và không được học viên duyệt riêng.

| Chỉ số (nhãn nháp) | Baseline dense/800 | Ứng viên hybrid RRF/2.700 |
|---|---|---|
| Grounded answer 0/1/2, trung bình | 16/1/3, 0.35 | 2/0/18, 1.80 |
| Citation hợp lệ | 4/4 | 19/19 |
| Từ chối đúng (thiếu bằng chứng) | 3/3 | 2/3 |
| Từ chối nhầm (có đáp án) | 16/20 | 2/20 |
| Context Evidence Rate | 5/20 | 20/20 |
| Request / token / trung vị mỗi câu | 82 / 55.774 / 6,5 s | 53 / 47.091 / 2,6 s |

- **Lỗi dev #3: định dạng citation.** 4 câu trả lời có nội dung đúng bị validator loại (`invalid_citations`), chấm 0: baseline dev-q02, dev-q13 và ứng viên dev-q04 (model không chèn `[id]` vào văn bản, chỉ liệt kê trong `citations`); ứng viên dev-q05 (gộp hai ID trong một ngoặc `[id1, id2]`). Lỗi này không phụ thuộc retrieval và làm sai lệch cả hai cấu hình.
- **Lỗi dev #4: ứng viên dev-u1.** Model gọi `answer` để nói không có số liệu cho Vietnam, kèm câu gây hiểu nhầm về con số 8.5% (thực ra là toàn cầu); chấm là từ chối không đúng. Không sửa riêng cho câu này, để tránh chỉnh theo từng câu dev; ghi nhận là giới hạn.

### B1: sửa định dạng citation (giả thuyết ghi trước khi chạy)

- **Thay đổi (chung, áp dụng như nhau cho mọi cấu hình):** (1) system prompt yêu cầu mỗi ID trong ngoặc vuông riêng, đặt ngay sau câu nó hỗ trợ, và nói rõ câu trả lời không có ID trong văn bản sẽ bị loại; (2) validator chấp nhận dạng gộp `[id1, id2]` / `[id1; id2]`. Vẫn giữ yêu cầu của starter: mọi citation phải xuất hiện trong văn bản câu trả lời và nằm trong context.
- **Giả thuyết:** số câu bị loại vì `invalid_citations` giảm về 0 hoặc gần 0 ở cả hai cấu hình; grounded answer trung bình tăng tương ứng; các chỉ số khác (Context Evidence Rate, từ chối đúng) không đổi đáng kể. Model không xác định hoàn toàn (không đặt temperature), nên các câu khác có thể dao động nhẹ.
- **Tiêu chí chọn không đổi** (mục 1, bước B). B1 thay B0 làm kết quả bước B; học viên duyệt nhãn B1.

### B1: kết quả

- **Runs:** `agent_dev_dense_b800_b1-baseline_20261116T081407Z` và `agent_dev_hybrid_rrf_b2700_b1-candidate_20261116T081910Z`, commit `31b0dcd`, cây code sạch, `gemini-3.5-flash-lite`, 0 USD (free tier).

| Chỉ số | Baseline dense/800 | Ứng viên hybrid RRF/2.700 |
|---|---|---|
| Lỗi provider (báo riêng, không chấm) | 0 | 1 (dev-q17: HTTP 429 vượt 15 request/phút sau 2 lần thử lại) |
| Tool use | 23/23 | 22/22 |
| Grounded answer 0/1/2, trung bình /2 | 13/1/6, 0.65 | 0/0/19, 2.00 |
| Citation hợp lệ (trong context và hỗ trợ) | 8/9 | 20/21 |
| Câu trả lời có citation | 9/9 | 20/20 |
| Từ chối đúng (thiếu bằng chứng) | 2/3 | 2/3 |
| Từ chối nhầm (có đáp án) | 12/20 | 0/19 |
| Context Evidence Rate | 6/20 | 19/19 |
| Model calls / token / trung vị mỗi câu | 80 / 57.782 / 4,9 s | 53 / 49.652 / 3,1 s |

- **So với giả thuyết B1:** **xác nhận.** `invalid_citations` giảm từ 2 + 2 (B0) về 0 + 0; grounded trung bình tăng (baseline 0.35 → 0.65, ứng viên 1.80 → 2.00).
- **Tác dụng phụ (lỗi dev #5):** prompt mới ("câu trả lời không có ID sẽ bị loại") làm model đôi khi gọi `answer` kèm citation để nói rằng không có thông tin, thay vì `abstain`: baseline dev-q05 (chấm 0) và baseline dev-u1 (nội dung từ chối đúng, nhưng status `answered` nên tính là không từ chối).
- **Lỗi dev #6, nghiêm trọng: ứng viên dev-u1 bịa.** Câu trả lời "The poverty rate in Vietnam fell from 38 percent in 1990 to 8.5 percent in 2024" trích `p036s0:c000`; chunk này nói về tỷ lệ **toàn cầu**, không nhắc Vietnam. Validator cho qua vì ID có trong context; chỉ chấm tay mới phát hiện. Metric nhị phân "từ chối đúng" tính baseline dev-u1 (từ chối đúng nội dung, sai tool) và ứng viên dev-u1 (bịa) như nhau, nên cần đọc kèm nhãn citation.
- **Bước B (tiêu chí mục 1):** grounded ứng viên 2.00 ≥ baseline 0.65 → đạt; từ chối đúng 2/3 = 2/3, không ít hơn baseline → đạt. **→ Chọn hybrid RRF, budget 2.700.**
- **Nhãn:** Claude chấm nháp; học viên đọc `review_sheet.md`, duyệt toàn bộ 46 dòng `labels.csv` ngày 2026-11-16 và không sửa dòng nào (cột `reviewer`). Số liệu trong bảng là từ `agent_metrics.json` sau khi duyệt.
- **Sửa hạ tầng trước test (không đổi hành vi agent):** để không mất câu vì giới hạn 15 request/phút như dev-q17, client Gemini giãn cách request tối thiểu 4,5 s (khoảng 13 request/phút), thử lại tối đa 4 lần và chờ đúng `retryDelay` do server trả về.

## 4. Khóa cấu hình trước test (2026-11-16)

Cấu hình dưới đây được chốt trên dev và khóa bằng **commit chứa mục này**, trước mọi lần chạy trên test. Sau khi thấy kết quả test, không thay đổi code, prompt, tham số hay nhãn dev; mọi thay đổi bắt buộc (nếu có) sẽ được ghi rõ là sau test và không được báo như kết quả holdout.

| | **Cấu hình chọn** | **Baseline** |
|---|---|---|
| Retrieval | Hybrid RRF: dense (EmbeddingGemma `google/embeddinggemma-2`, pgvector `day6_chunks` index B) + BM25 (k1 1.5, b 0.75); RRF k = 60, pool 10 mỗi retriever | Dense (cùng embedding và index) |
| Top-k mỗi lần search | 3 | 3 |
| Context | starter `pack_context`, theo thứ tự truy xuất, **2.700 ký tự** (tính cả header) | 800 ký tự |
| Filter | `filter` do người dùng cung cấp trong câu hỏi, áp dụng như nhau | như nhau |
| Agent | `gemini-3.5-flash-lite` (Gemini API free tier, REST), tools search / answer / abstain, function calling mode ANY, tối đa 3 search, system prompt trong `src/agent.py` | như nhau |
| Client | giãn cách 4,5 s, thử lại tối đa 4 lần theo `retryDelay`, dừng khi hết hạn mức ngày | như nhau |

**Quy trình test (chạy một lần, cờ `--allow-test`):**
1. Retrieval: `python -m src.eval_retrieval --split test --allow-test --methods dense,hybrid_rrf --budget 800` và `--budget 2700` → Hit@1, Evidence Hit@3, MRR@10, Context Evidence Rate trên 9 câu test có đáp án.
2. Agent: `python -m src.run_agent --split test --allow-test` cho baseline (`--method dense --budget 800`) và cấu hình chọn (`--method hybrid_rrf --budget 2700`), 12 câu mỗi cấu hình.
3. Chấm tay **toàn bộ** test (9 câu có đáp án + 3 câu thiếu bằng chứng, cho cả hai cấu hình): grounded answer 0/1/2, citation hỗ trợ, abstention, và **context 0/1/2** cho mọi câu có đáp án (BENCHMARK.md §2 yêu cầu ít nhất 5). Lỗi provider được báo riêng.
4. Không chạy lại test để "lấy kết quả tốt hơn". Nếu một lần chạy bị lỗi hạ tầng (ví dụ hết hạn mức ngày), chỉ chạy tiếp các câu chưa chạy và ghi rõ.
