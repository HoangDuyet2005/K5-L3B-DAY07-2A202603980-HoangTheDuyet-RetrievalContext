# Báo cáo Day 7

Học viên: Hoàng Thế Duyệt · MSSV 2A202603980 · Lớp L3B. Cách chạy: [`src/README.md`](../../src/README.md). Nhật ký đầy đủ (giả thuyết ghi trước, run ID, commit): [`results/EXPERIMENTS.md`](../../results/EXPERIMENTS.md).

## Dữ liệu và benchmark

- **Nguồn, quyền sử dụng, số trang và số chunk:** World Bank, *Poverty, Prosperity, and Planet Report 2024: Pathways Out of the Polycrisis* (doi:10.1596/978-1-4648-2123-3), giấy phép CC BY 3.0 IGO. Corpus là phần Overview, PDF trang 35–73 (36 trang có nội dung) của file 300 trang; dùng lại từ Day 6. Index B của Day 6: 130 chunk theo đoạn văn (tối đa 800 ký tự). Text trong DB trùng từng byte với file JSONL đã commit ở Day 6 (so MD5 319/319 chunk).
- **Vector store, embedding model, phiên bản và số chiều:** PostgreSQL 16 + pgvector 0.8.7 (Docker Compose Day 6), bảng `day6_chunks`, cột `vector(768)`, tìm cosine chính xác; Day 7 kết nối ở chế độ chỉ đọc. Embedding `google/embeddinggemma-2` (sentence-transformers 6.3.0, torch 2.15.0, CPU), 768 chiều, float32, prompt query `SearchQuery`, chuẩn hóa; revision không cố định (kế thừa Day 6). Kiểm chứng tương thích: dense search Day 7 cho đúng top-3 và điểm của trace Day 6 (dev q01, q04 với B và C; chênh lệch điểm 0.0).
- **Agent model, cách chạy và phân chia dev/test:** `gemini-3.5-flash-lite` qua Gemini API (REST bằng `urllib`, không SDK), gói miễn phí, 0 USD. Ban đầu chọn `gemini-3.5-flash` nhưng gói miễn phí chỉ cho 20 request/ngày (lỗi 429 ở lần chạy dev đầu tiên), nên đổi sang bản Flash-Lite (500/ngày) **trước mọi lần chạy agent chính thức**. Benchmark 35 câu: **dev** 20 câu có đáp án + 3 câu thiếu bằng chứng; **test** 9 + 3. 20 câu dev được **tái sử dụng từ benchmark Day 6** (5 câu từng là test Day 6), đã xem khi phát triển nên chỉ dùng để chẩn đoán và chọn cấu hình, không phải holdout. Toàn bộ test là câu mới, lấy từ các trang chưa từng làm gold ở Day 6, khóa ở commit `dff6d78` trước mọi thử nghiệm.
- **Cách xác định câu có/thiếu evidence và tiêu chí chấm:** câu có đáp án có evidence nguyên văn nằm trọn trong một chunk B đúng trang và có trong text PDF (script `src/verify_benchmark.py`); dev-q05 có hai evidence thay thế vì evidence Day 6 vắt qua hai chunk. Câu thiếu bằng chứng gần chủ đề (Việt Nam, IDA21, giá carbon mỗi tấn, Pantawid, thất nghiệp thanh niên, tỷ lệ xuất khẩu than của Indonesia), được kiểm bằng tìm từ khóa trên toàn bộ 130 chunk và text PDF trang 35–73 (gồm cả nhãn hình), rồi đọc tay mọi chỗ khớp. Chấm theo BENCHMARK.md: grounded 0/1/2 (từ chối câu có đáp án = 0), citation hợp lệ = có trong context **và** hỗ trợ khẳng định, abstention đúng, context 0/1/2. Nhãn do Claude chấm nháp kèm lý do; học viên đọc và duyệt từng dòng (dev B1 46 dòng, test 24 dòng, đối chiếu PDF), không sửa dòng nào.

## Retrieval và thử nghiệm

Retrieval đo bằng câu hỏi gốc, top-3, pool 10, context đóng gói bằng `pack_context` của starter (budget tính bằng ký tự, gồm header). Filter section do người dùng cung cấp được áp dụng như nhau cho mọi phương pháp. Chi phí retrieval 0 USD (local); thời gian là trung vị mỗi query trên CPU.

| Cấu hình | Phương pháp, top-k, filter, rerank, context budget | Giả thuyết / thay đổi | Split | Hit@1 | Evidence Hit@3 | Context Evidence Rate | Thời gian / chi phí |
|---|---|---|---|---|---|---|---|
| Baseline | Dense (EmbeddingGemma + pgvector), top-3, filter người dùng, không rerank, 800 ký tự | Phương pháp bắt buộc | dev | 16/20 (80%) | 20/20 (100%) | 6/20 (30%) | 213 ms; 0 USD |
| Phương pháp 2 | BM25 (k1 1.5, b 0.75, `\w+` casefold), top-3, 800 | Khớp từ khóa, tên riêng | dev | 18/20 (90%) | 20/20 (100%) | 7/20 (35%) | 1 ms; 0 USD |
| Phương pháp 3 | Hybrid RRF (dense + BM25, k = 60, pool 10 mỗi bên), top-3, 800 | Gộp thứ hạng hai phương pháp, không cần chuẩn hóa điểm | dev | 18/20 (90%) | 20/20 (100%) | 7/20 (35%) | 221 ms; 0 USD |
| Cải thiện 1 (E1) | Hybrid RRF top-10 → rerank `ms-marco-MiniLM-L6-v2` → top-3, 800 | Cross-encoder phân biệt đoạn đúng với đoạn cùng chủ đề; dự đoán Hit@1 > 18/20 | dev | 18/20 (90%) | 20/20 (100%) | 8/20 (40%) | 639 ms; 0 USD |
| Cải thiện 2 (E2) | Hybrid RRF, top-3, **2.700** ký tự | Context Evidence Rate thấp vì chunk đúng dài hơn 800 ký tự bị bỏ; dự đoán gần bằng Hit@3 | dev | 18/20 (90%) | 20/20 (100%) | **20/20 (100%)** | 217 ms; 0 USD; context 582 → 2.129 ký tự |
| Cấu hình đã chọn | Hybrid RRF, top-3, 2.700, tối đa 3 search | Khóa ở commit `4f38a31` | test | 6/9 (67%) | 8/9 (89%) | 8/9 (89%) | 278 ms; 0 USD |
| Baseline | Dense, top-3, 800 | | test | 7/9 (78%) | 7/9 (78%) | 5/9 (56%) | 213 ms; 0 USD |

MRR@10: dev dense 0.875, BM25/hybrid/rerank 0.950; test dense 0.821, hybrid 0.773. Evidence Hit@3 đạt trần 20/20 trên dev, nên không dùng để chọn.

E1 là phương pháp mới đồng thời là thử cải thiện; **E1 không cải thiện**: rerank sửa dev-q01 (hạng 2 → 1) nhưng làm hỏng dev-q05 (1 → 2), Hit@1 và MRR giữ nguyên, chậm thêm khoảng 420 ms. **E2 xác nhận giả thuyết** ở cả 4 phương pháp. Tiêu chí chọn ghi trước (commit `501c617`): Context Evidence Rate → Hit@1 → MRR → context ngắn hơn → thời gian. Ba ứng viên ở budget 2.700 hòa ba tiêu chí đầu; hybrid RRF có context ngắn nhất (2.129 so với 2.134 và 2.162 ký tự). Chênh lệch rất nhỏ, nên hybrid được chọn vì đúng tiêu chí đã ghi chứ không vì vượt trội. Bước B (agent trên dev) xác nhận lựa chọn.

**Hai lỗi dev chính, nguyên nhân, cách thử và kết quả:**
1. **dev-q04: context bị khóa bởi chunk đầu tiên.** Ở lần chạy thử với budget 800, lượt search đầu đưa `p041s0:c001` (791 ký tự) vào context; cả 3 lượt search đều tìm thấy chunk evidence `p041s0:c000` (hạng 3, 3, 2) nhưng nó không vừa phần budget còn lại vì `pack_context` giữ chunk cũ trước. Agent từ chối trung thực. Cách thử: E2 (budget 2.700). Kết quả: với cấu hình chọn, dev-q04 trả lời đúng "7 in 10" kèm citation đúng chunk (grounded 2).
2. **dev-q01: thiếu một phần đáp án.** Context chỉ có chunk tỷ lệ 8.5% (`p036s0:c000`), thiếu con số 692 triệu (`p035s0:c003`). Với câu hỏi gốc dense xếp chunk evidence hạng 3, nhưng 3 query agent tự viết lại không đưa được nó vào top-3. Baseline trả lời được một nửa (grounded 1). Cách thử: E1 (rerank đưa chunk lên hạng 1) và E2 (chứa 3 chunk). Kết quả: cấu hình chọn trả lời đủ "8.5 percent … 692 million" (grounded 2).

Các lỗi khác ở dev (đã ghi trong EXPERIMENTS.md): lỗi định dạng citation (4 câu trả lời đúng bị validator loại vì thiếu `[id]` hoặc gộp `[id1, id2]`) được sửa bằng prompt và chấp nhận dạng gộp (B0 → B1, giả thuyết ghi trước, xác nhận); model Flash-Lite đôi khi dùng tool `answer` để nói "không có thông tin" (đã thêm luật vào prompt, giảm nhưng không hết); và dev-u1 bị bịa (xem bảng ví dụ).

## Agent và đánh giá

- **Tool, số lượt gọi, điều kiện dừng, cách chọn context và xử lý lỗi:** ba tool `search(query)`, `answer(answer, citations)`, `abstain(reason)`; function calling mode ANY, lượt đầu chỉ được search, tối đa 3 search, hết lượt search thì chỉ còn answer/abstain. Mỗi lượt gọi model là một request mới gồm câu hỏi, các query đã chạy và context tích lũy (không gửi gold, không gửi nhãn). Context = `pack_context` trên mọi chunk đã truy xuất theo thứ tự (khử trùng ID, giữ chunk cũ trước, chunk không vừa budget bị bỏ). Câu trả lời chỉ được chấp nhận khi mọi citation có trong context và xuất hiện trong ngoặc vuông trong văn bản; nếu không thì thành abstain (`invalid_citations`). Nội dung chunk được đánh dấu là dữ liệu không đáng tin trong system prompt. Lỗi provider và DB được ghi `status: error` và báo riêng; client giãn cách 4,5 s, thử lại theo `retryDelay`, dừng khi hết hạn mức ngày; trace được ghi sau mỗi câu.

| Cấu hình / split | Tool use | Số lượt gọi | Grounded answer 0/1/2 và trung bình | Citation hợp lệ | Câu có citation | Abstention đúng | Từ chối nhầm |
|---|---|---|---|---|---|---|---|
| Baseline dense/800 / dev (B1) | 23/23 | 80 model calls; search 1 lần: 6 câu, 3 lần: 17 | 13/1/6; 0.65 | 8/9 | 9/9 | 2/3 | 12/20 |
| Chọn hybrid RRF/2.700 / dev (B1) | 22/22 (1 lỗi 429 báo riêng) | 53; 1 lần: 18, 3 lần: 4 | 0/0/19; 2.00 | 20/21 | 20/20 | 2/3 | 0/19 |
| Baseline dense/800 / test | 12/12 | 38; 1 lần: 5, 3 lần: 7 | 4/0/5; 1.11 | 5/7 | 7/7 | 2/3 | 3/9 |
| **Chọn hybrid RRF/2.700 / test** | 12/12 | 32; 1 lần: 8, 3 lần: 4 | 1/0/8; **1.78** | **8/8** | 8/8 | **3/3** | **1/9** |

Chấm context (test, 0/1/2): baseline 4/0/5, cấu hình chọn 1/0/8. Context Evidence Rate của agent (context cuối): baseline 5/9, cấu hình chọn 8/9.

| Query ID | Loại câu | Tool call và kết quả | Câu trả lời và citation | Nhãn, lý do |
|---|---|---|---|---|
| test-a1 (chọn) | Có đáp án, direct | 1 search "low income countries extreme poverty 2024 share" → context `p041s0:c000`, `p039s0:c000`, `p066s0:c000` | "In 2024, 43 percent of people in low-income countries are in extreme poverty [B:wb-ppp-2024:p039s0:c000]" | Grounded 2, citation hỗ trợ, context 2. Baseline (800) chỉ có `p036s0:c000` trong context nên từ chối |
| test-u1 (chọn) | Thiếu bằng chứng, câu bẫy | 3 search về Pantawid / Yolanda → context có `p056s0:c001` (nhắc Pantawid nhưng số hộ là của Kenya) | abstain: "… supported recipients … but they do not state the exact number of households" | Từ chối đúng, không lấy số 100,000/200,000 của Kenya |
| dev-u1 (chọn, B1) | Thiếu bằng chứng, **lỗi** | 3 search về Vietnam → context `p036s0:c000` (tỷ lệ toàn cầu) | "The poverty rate in Vietnam fell from 38 percent in 1990 to 8.5 percent in 2024 [B:wb-ppp-2024:p036s0:c000]" | **Bịa**: chunk không nhắc Vietnam; citation có trong context (validator cho qua) nhưng không hỗ trợ. Abstention sai, citation 0 |
| test-a3 (cả hai) | Có đáp án, **lỗi retrieval** | 3 search về chỉ số rủi ro khí hậu → context `p049`, `p051`, không có `p052s0:c001` | abstain: không có số nước được bao phủ | Grounded 0, context 0. Hybrid xếp chunk evidence hạng 8 với câu hỏi gốc; agent từ chối trung thực |

- **Đường dẫn trace, nhãn, lệnh chạy, thời gian và chi phí:** retrieval `results/retrieval_dev_20261116T055416Z`, `…055514Z`, `results/retrieval_test_20261116T085531Z`, `…085609Z`; agent dev `results/agent_dev_*_b1-*`; agent test `results/agent_test_dense_b800_test-baseline_20261116T085657Z`, `results/agent_test_hybrid_rrf_b2700_test-selected_20261116T090045Z`. Mỗi thư mục có `traces*.jsonl`, `run_metadata.json` (commit, sha256 benchmark và corpus, cấu hình, phiên bản), và với agent `review_sheet.md`, `labels.csv`, `agent_metrics.json`. Lệnh chạy: `src/README.md`. Thời gian: retrieval khoảng 1 phút mỗi run (gồm 12–17 s nạp model); agent dev 270 s (baseline) và 264 s (chọn); agent test 200 s và 152 s. Token agent: dev 57.782 và 49.652; test 27.740 và 30.821 (không có thinking token). Chi phí: 0 USD (Gemini free tier, model và DB local).
- **Kết quả trước/sau, ví dụ lỗi, đánh đổi và giới hạn:**
  - Trước/sau trên test: grounded 1.11 → 1.78, từ chối nhầm 3/9 → 1/9, từ chối đúng 2/3 → 3/3, citation hợp lệ 5/7 → 8/8, Context Evidence Rate 5/9 → 8/9.
  - Đánh đổi: context dài khoảng 3,2 lần (665 → 2.138 ký tự) nhưng agent cần ít lượt gọi hơn (38 → 32 trên test) nên token chỉ tăng khoảng 11% và thời gian mỗi câu giảm (17,4 → 10,4 s). Thời gian retrieval của hybrid và dense gần như nhau (200–280 ms mỗi query, phần lớn là embed query; BM25 khoảng 1 ms). Trên test hybrid thua dense ở Hit@1 (6/9 so với 7/9) nhưng thắng Evidence Hit@3 (8/9 so với 7/9); với context 3 chunk, Hit@3 quan trọng hơn Hit@1. Rerank không đáng chi phí trên dữ liệu này.
  - Giới hạn:
    - Dev là 20 câu Day 6 tái sử dụng, dùng lại từ ngữ của nguồn, nên Hit@3 đạt trần và BM25 được lợi; test chỉ 9 + 3 câu, mỗi câu khoảng 11 điểm phần trăm.
    - Corpus chỉ có một tài liệu nên chủ đề lặp giữa dev và test.
    - Agent không xác định hoàn toàn (không đặt temperature); Google phục vụ model dưới tên alias (lần đầu `gemini-3.5-flash` trả `modelVersion` `gemini-3.6-flash`).
    - Validator chỉ kiểm ID, không kiểm nội dung (dev-u1 bịa vẫn qua); metric abstention nhị phân không phân biệt "từ chối đúng nội dung nhưng sai tool" với "bịa".
    - EmbeddingGemma không cố định revision.
    - Gói miễn phí có hạn mức (15 request/phút, 500/ngày) và Google có thể dùng dữ liệu gửi lên; dữ liệu chỉ gồm báo cáo công khai và câu hỏi tự viết.
    - Nhãn do AI chấm nháp và học viên duyệt; có thể còn thiên lệch của người soạn benchmark.

## Thử thách nâng cao (nếu thực hiện)

Không thực hiện.
