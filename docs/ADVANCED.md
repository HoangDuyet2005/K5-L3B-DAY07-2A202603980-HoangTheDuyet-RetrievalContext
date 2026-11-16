# Thử thách nâng cao — Hoàng Thế Duyệt (2A202603980)

Tài liệu này mô tả phần nâng cao theo [ADVANCED.md](../ADVANCED.md): tài liệu, index, benchmark, cách chạy,
kết quả và giới hạn. Code ở `src/adv/`, dữ liệu ở `data/advanced/`, kết quả ở `results/advanced/`.

## 1. Tài liệu

| Mục | Giá trị |
|---|---|
| Tên | World Bank. 2024. *Poverty, Prosperity, and Planet Report 2024: Pathways Out of the Polycrisis*. Washington, DC: World Bank |
| DOI / nguồn | doi:10.1596/978-1-4648-2123-3 — https://www.worldbank.org/en/publication/poverty-prosperity-and-planet |
| Phiên bản | Bản PDF đầy đủ, 300 trang; sha256 ghi trong `data/advanced/index_stats.json` (`pdf_sha256`) |
| Quyền sử dụng | Creative Commons Attribution CC BY 3.0 IGO (được sao chép, phân phối, chuyển thể khi ghi nguồn) |
| Nội dung trực quan | 95 nhãn FIGURE, 19 nhãn TABLE, 4 MAP trong lớp text; 114 trang có ít nhất một hình/bảng/bản đồ |

File PDF không nằm trong repo (9 MB); tải từ nguồn trên rồi truyền đường dẫn qua `--pdf`. Mọi số trang trong
phần này là **số trang PDF** (1–300), không phải số in trên trang.

Các mô tả hình/bảng trong `data/advanced/` là bản chuyển thể do model tạo từ tài liệu gốc của World Bank
(CC BY 3.0 IGO); đây không phải bản chính thức của World Bank.

## 2. Index

Lệnh: `python -m src.adv.ingest --pdf "<đường dẫn PDF>"` → `data/advanced/chunks.json`,
`data/advanced/index_stats.json`, `data/advanced/vision_raw/pNNN.json`.

- **Text (cả 300 trang):** lớp text của PDF đọc bằng `pypdf`, cắt theo dòng thành chunk khoảng 1.800 ký tự,
  chồng lấn khoảng 200 ký tự. ID `adv:pNNNtK`, metadata có `pdf_page` và `content_type: text`.
- **Hình, bảng, bản đồ (114 trang có nhãn FIGURE/TABLE/MAP):** mỗi trang được tách thành PDF một trang và gửi
  cho model vision `gemini-3.1-flash-lite` (Gemini API, gói miễn phí). Model trả JSON, mỗi hình/bảng một mục:
  nhãn, loại (`table`/`chart`/`map`/`diagram`), tiêu đề, **bbox** `[ymin, xmin, ymax, xmax]` theo thang 0–1000
  trên trang, và nội dung (bảng: chép lại dạng Markdown; biểu đồ: trục, đơn vị, chú giải, nhãn số, xu hướng;
  sơ đồ/bản đồ: các thành phần và chú giải). Mỗi mục thành một chunk `adv:pNNNvK` với metadata `label`,
  `title`, `bbox`, `content_type`, `described_by`.
- **Liên kết về bản gốc:** mọi chunk có `page` (trang PDF); chunk trực quan có thêm nhãn hình và bbox để tìm
  đúng vùng trên trang. Phản hồi thô của model lưu theo từng trang trong `vision_raw/` để đối chiếu.
- **Truy xuất:** BM25 (`src/lexical.py`, k1 = 1,5, b = 0,75) trên toàn bộ chunk text + trực quan. Không dùng
  embedding: embedding lại 300 trang bằng CPU không kịp thời hạn; đây là giới hạn đã biết (mục 6).
- **Vì sao chọn cách này:** tài liệu có lớp text tốt nên không cần OCR; bảng và sơ đồ phần lớn đọc được từ
  lớp text nhưng mất cấu trúc hàng/cột và nhóm, còn biểu đồ thì giá trị nằm trong hình. Mô tả bằng vision
  model đưa cấu trúc đó về dạng text để BM25 tìm được, và agent trích dẫn được đúng hình.
- **Kiểm tra nội dung trích xuất:** mô tả do model tạo không được coi là đúng. Đáp án benchmark được viết từ
  tài liệu gốc; `python -m src.adv.bench check --pdf ...` đối chiếu mọi đoạn evidence với lớp text của trang
  PDF gốc (không dùng index). Vị trí hàng/cột/panel/chú giải do người chấm xem trang gốc để xác nhận.

Thống kê index và các trang không xử lý được: xem mục 5.

## 3. Benchmark

`data/advanced/benchmark/questions.json` (đáp án, evidence, lý do) và `cases.json` (chỉ ID, nhóm, câu hỏi —
thứ duy nhất agent được thấy là câu hỏi). Dev/test được chia trước khi chạy agent.

| Split | Bảng | Ảnh/sơ đồ | Biểu đồ | Multi-hop | Text | Thiếu bằng chứng | Tổng |
|---|---:|---:|---:|---:|---:|---:|---:|
| dev | 4 | 2 | 3 | 2 | 4 | 3 | 18 |
| test | 6 | 5 | 5 | 4 | 4 | 6 | 30 |

Mỗi câu có ID, nhóm chính, câu hỏi, đáp án mong đợi hoặc hành vi từ chối, evidence (trang PDF, vị trí
hàng/cột/panel/chú giải, đoạn trích) và lý do. Câu thiếu bằng chứng ghi cách kiểm tra trong tài liệu
(`absence_check`). Các câu thiếu bằng chứng đều là "gần đúng": cùng bảng/chỉ số nhưng sai năm, sai nước hoặc
sai hàng.

Cách chấm test: đạt/không đạt từng câu theo ADVANCED.md §3, ghi trong `labels.csv` của run (cột `pass`,
`reason`, `checked_against`, `reviewer`).

Lượt hai cho sơ đồ/bản đồ: 11 trang có mục `diagram` hoặc `map` được mô tả lại bằng model mạnh hơn
(`--redo-kinds diagram,map --vision-model gemini-3.5-flash`, Google phục vụ bằng `gemini-3.6-flash`); bản lượt
một giữ trong `data/advanced/vision_raw_first_pass/`. Lý do: trên dev, mô tả lượt một của Figure B3.1.1 (tr. 201)
gộp sai cả bảy điều kiện vào nhóm "unable to cope".

## 4. Cách chạy

Chạy từ thư mục gốc repo, bằng Python có `pypdf` (venv Day 6) và `GEMINI_API_KEY` trong `.env`:

```
python -m src.adv.ingest --pdf "<PDF>"                                   # text + vision lượt một
python -m src.adv.ingest --pdf "<PDF>" --redo-kinds diagram,map --vision-model gemini-3.5-flash
python -m src.adv.bench build                                            # cases.json + kiểm tra số câu mỗi nhóm
python -m src.adv.bench check --pdf "<PDF>"                              # evidence có trong lớp text trang gốc?
python -m src.adv.run --split dev --label d3                             # cấu hình đã chốt là mặc định
python -m src.adv.run --split test --allow-test --label final
python -m src.adv.review sheet --run results/advanced/<run>              # review_sheet.md + labels.csv
python -m src.adv.review aggregate --run results/advanced/<run>          # metrics.json
```

Mỗi run lưu `traces.jsonl` (truy vấn, kết quả retrieval, context, tool call, câu trả lời, citation, thời gian,
token, lỗi cho từng câu) và `run_metadata.json` (cấu hình, prompt, hash đầu vào).

## 5. Kết quả

### Index

| Mục | Giá trị |
|---|---|
| Trang | 300; 293 trang có text; 10 trang gần như không có text (1, 2, 3, 5, 14, 18, 32, 194, 297, 299: bìa, trang trống, trang mở chương) nên không có nội dung để index |
| Chunk | 730: 612 text, 89 chart, 19 table, 6 diagram, 4 map |
| Trang trực quan | 114 trang, 0 trang lỗi, 0 trang không parse được JSON |
| Model mô tả | `gemini-3.1-flash-lite` 103 trang; `gemini-3.6-flash` 11 trang (lượt hai) |

Ảnh hưởng của phần không xử lý được: không có trang nào có hình/bảng bị bỏ. Hình không có nhãn
FIGURE/TABLE/MAP trong lớp text (nếu có, ví dụ ảnh trang trí mở chương) không được gửi cho vision model.

### Thử nghiệm trên dev (18 câu)

| Run | Cấu hình | Đạt | Ghi chú |
|---|---|---:|---|
| d1 | BM25, top-k 6, budget 16.000, prompt v1, vòng lặp gốc | 15/18 | Sai: dev-01 (bảng dài không được xếp hạng), dev-11 (retrieval), dev-u1 (trả lời số của năm khác) |
| d2 | BM25 + tra nhãn, top-k 8, budget 24.000, prompt v2, chỉ cho từ chối khi hết lượt tìm | 15/18 | Sửa được dev-01; nhưng model dùng `answer` để nói "không có thông tin" (dev-11, dev-u1, dev-u3) |
| d3 (chốt) | như d2 nhưng cho từ chối sớm + tìm dự phòng bằng chính câu hỏi + coi câu trả lời "không có thông tin" là từ chối; index lượt hai | 17/18 | Sai: dev-11 (retrieval không trả về tr. 201/52) |

Số đạt của d1 và d2 là do đọc trace, không có `labels.csv`; d3 có `labels.csv` và `metrics.json`.
Cấu hình và hash được ghi vào `results/advanced/LOCK.json` trước khi chạy test. Test chỉ chạy một lần.

### Test (30 câu) — `results/advanced/test_final_20261116T113544Z/`

| Nhóm | Đạt |
|---|---:|
| Bảng | 6/6 |
| Ảnh, sơ đồ | 5/5 |
| Biểu đồ | 5/5 |
| Multi-hop | 4/4 |
| Text | 4/4 |
| Thiếu bằng chứng | 6/6 |
| **Tổng** | **30/30 (100%)** |

Lỗi hệ thống: 0. Thời gian: 367 giây cho 30 câu (trung vị 9,7 giây/câu). 69 lần gọi model, 226.118 token
(222.065 prompt, 4.053 output). Chi phí: 0 USD (Gemini API gói miễn phí).

**Trạng thái nhãn:** nhãn trong `labels.csv` hiện là **bản nháp do Claude soạn** bằng cách so câu trả lời với
đáp án và kiểm tra tự động rằng mọi con số trong câu trả lời có trong lớp text của trang PDF gốc được trích
dẫn. Người làm bài phải xem trang PDF gốc để xác nhận từng câu (đặc biệt vị trí hàng/cột, panel, chú giải của
các câu bảng, biểu đồ, sơ đồ) rồi đổi cột `reviewer`. Con số 30/30 chỉ có giá trị sau bước này.

Các câu cần nhìn kỹ khi duyệt:
- `adv-test-09` (và `adv-dev-05`): trả lời đúng nhóm nhưng trích dẫn Figure BO.3.1 ở tr. 52, bản sao của cùng
  sơ đồ trong phần Overview, thay vì tr. 201. Quy tắc chấp nhận bản sao được ghi trong `questions.json` trước
  khi chạy test. Cách chia hai nhóm trong sơ đồ chưa được người xem xác nhận.
- `adv-test-14`: thanh biểu đồ không in số; agent trả lời "khoảng 60%" (Table 1.1 ghi 59).
- `adv-test-16`: cần xác nhận trên hình rằng các nước được nêu nằm ở cụm bên phải.

## 6. Phân tích lỗi và giới hạn

- **Retrieval chỉ dùng từ khóa.** dev-11 hỏi "indicator covers how many economies" nhưng BM25 xếp các đoạn lặp
  nhiều "risk/climate/hazards" lên trước và không trả về đoạn "103 economies ... 86 percent". Không có stemming
  hay embedding. Câu hỏi diễn đạt xa từ ngữ của tài liệu sẽ dễ trượt.
- **Mô tả hình do model tạo có thể sai.** Đã gặp một lỗi cấu trúc (Figure B3.1.1). Chỉ 11 trang sơ đồ/bản đồ
  được mô tả lại; 89 mô tả biểu đồ chưa được kiểm tra từng cái. Giá trị "approx." đọc từ trục là ước lượng.
- **Benchmark dễ hơn câu hỏi tự nhiên.** Phần lớn câu nêu thẳng nhãn hình/bảng, và tra nhãn là một phần của
  retriever. Câu biểu đồ ưu tiên hình có in nhãn số (kiểm chứng được bằng lớp text). Kết quả 100% không nói
  lên chất lượng với câu hỏi không nêu nhãn hoặc phải ước lượng từ trục.
- **Người viết benchmark không xem được ảnh trang.** Benchmark được Claude soạn từ lớp text của PDF gốc (không
  có công cụ render trang); mọi evidence được kiểm tra tự động với lớp text, còn bố cục hình thì chưa.
- **Bộ lọc "không có thông tin".** Câu trả lời chứa cụm như "does not provide" bị chuyển thành từ chối. Một câu
  trả lời đúng nhưng có kèm cụm này cũng sẽ bị chuyển thành từ chối (chưa gặp trên dev/test).
- **Gói miễn phí.** Google có thể dùng prompt và phản hồi để cải thiện sản phẩm và người duyệt có thể đọc;
  tài liệu là bản công khai CC BY nên không có dữ liệu riêng tư. Giới hạn 500 yêu cầu/ngày của model quyết
  định số lần chạy dev.
- **Một lần chạy.** Nhiệt độ 0 nhưng model không tất định hoàn toàn; chưa đo độ dao động giữa các lần chạy.

## 7. File nộp

`src/adv/` (code), `data/advanced/chunks.json`, `index_stats.json`, `vision_raw/`, `vision_raw_first_pass/`,
`data/advanced/benchmark/`, `results/advanced/` (3 run dev, 1 run test, `LOCK.json`), tài liệu này.
