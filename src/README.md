# Bài làm Day 7: cách cài đặt và chạy

Agent RAG dùng **Gemini** để tìm bằng chứng trong kho Day 6 (PostgreSQL + pgvector), trả lời có citation tới chunk hoặc từ chối khi không đủ bằng chứng. Nhật ký thử nghiệm: [`results/EXPERIMENTS.md`](../results/EXPERIMENTS.md). Báo cáo: [`report/individual/2A202603980_HoangTheDuyet.md`](../report/individual/2A202603980_HoangTheDuyet.md).

## Thành phần

| Thành phần | Lựa chọn |
|---|---|
| Corpus | World Bank, *Poverty, Prosperity, and Planet Report 2024*, phần Overview (PDF trang 35–73), CC BY 3.0 IGO; 130 chunk (index B của Day 6) |
| Vector store | PostgreSQL 16 + pgvector 0.8.7 (Docker Compose của Day 6), bảng `day6_chunks`, `vector(768)`, tìm cosine chính xác |
| Embedding | `google/embeddinggemma-2` (sentence-transformers, local CPU), 768 chiều, float32, prompt query `SearchQuery`, chuẩn hóa; giống hệt Day 6 |
| Retrieval | dense (pgvector), BM25 (thư viện chuẩn), hybrid RRF (k = 60), rerank cross-encoder `cross-encoder/ms-marco-MiniLM-L6-v2` (revision cố định) |
| Agent model | `gemini-3.5-flash-lite` qua Gemini API (REST, `urllib`, không SDK), gói miễn phí |
| Cấu hình chọn | hybrid RRF, top-3, context 2.700 ký tự, tối đa 3 search; baseline: dense, context 800 ký tự |

| File | Việc |
|---|---|
| `config.py` | Mọi lựa chọn kỹ thuật (model, index, filter); đọc `.env` cho secret |
| `day6.py` | Đọc Day 6 chỉ đọc (read-only), đổi chunk sang định dạng Day 7, embed query, dense search |
| `lexical.py`, `hybrid.py`, `rerank.py` | BM25, RRF, rerank |
| `eval_retrieval.py` | Benchmark retrieval: Hit@1, Evidence Hit@3, MRR@10, Context Evidence Rate |
| `gemini.py`, `agent.py`, `run_agent.py` | Client Gemini, vòng lặp agent (search / answer / abstain), chạy agent và ghi trace |
| `review.py` | Tạo bảng chấm tay, tổng hợp nhãn bằng `starter/agent_metrics.py` |
| `check_day6.py`, `verify_benchmark.py` | Kiểm tra kết nối Day 6, export chunk, kiểm tra benchmark |

## 1. Chuẩn bị

1. **Kho Day 6.** Cần repo Day 6 ([K5-L3B-DAY06-HoangTheDuyet-2A202603980-DataIngestion](https://github.com/HoangDuyet2005/K5-L3B-DAY06-HoangTheDuyet-2A202603980-DataIngestion)) đã ingest (strategy A 189 dòng, B 130 dòng). Bật database:
   ```bash
   cd <repo Day 6>/starter && docker compose up -d
   ```
   Nếu volume trống, chạy lại `python -m src.run ingest` của Day 6 (xem README Day 6).
2. **Python 3.11** và các package (phiên bản giống Day 6, để query embedding khớp index):
   ```bash
   python -m venv .venv
   .venv/Scripts/python -m pip install -r requirements.txt
   ```
   Có thể dùng luôn venv của Day 6 (`<repo Day 6>/starter/.venv`), là môi trường đã dùng cho mọi kết quả trong `results/`.
3. **Biến môi trường:** chép `.env.example` thành `.env`, điền `GEMINI_API_KEY` (Google AI Studio). `.env` không được commit.
4. **PDF gốc** (chỉ cần cho `verify_benchmark`): tải từ link trong `data/benchmark/README.md`, sha256 `0f22fde0…af746`.

Lần đầu chạy sẽ tải `google/embeddinggemma-2` và (nếu dùng rerank) `cross-encoder/ms-marco-MiniLM-L6-v2` (khoảng 90 MB) từ Hugging Face.

## 2. Chạy (từ thư mục gốc repo)

```bash
# Kiểm tra kết nối Day 6 và tạo lại file chunk dùng cho BM25/hybrid (sha256 a78d0825…bd78b)
python -m src.check_day6 info
python -m src.check_day6 export --output starter/data/day6/chunks_B.json

# Kiểm tra benchmark đã khóa (evidence nằm trong chunk đúng trang và trong text PDF)
python -m src.verify_benchmark --chunks starter/data/day6/chunks_B.json --pdf "<PDF>"

# Retrieval trên dev (không gọi Gemini)
python -m src.eval_retrieval --split dev --chunks starter/data/day6/chunks_B.json \
    --methods dense,bm25,hybrid_rrf,hybrid_rrf_rerank --budget 800      # và --budget 2700

# Agent trên dev: baseline và cấu hình chọn
python -m src.run_agent --split dev --method dense --budget 800 --chunks starter/data/day6/chunks_B.json
python -m src.run_agent --split dev --method hybrid_rrf --budget 2700 --chunks starter/data/day6/chunks_B.json

# Bảng chấm tay và tổng hợp nhãn
python -m src.review sheet --run results/<run> --chunks starter/data/day6/chunks_B.json
python -m src.review aggregate --run results/<run>

# Test: chỉ sau khi khóa cấu hình (cần cờ --allow-test)
python -m src.eval_retrieval --split test --allow-test --methods dense,hybrid_rrf --budget 2700 --chunks starter/data/day6/chunks_B.json
python -m src.run_agent --split test --allow-test --method hybrid_rrf --budget 2700 --chunks starter/data/day6/chunks_B.json

# Unit test (offline, không cần DB hay model)
python -m unittest discover -s tests -v
```

Mỗi lần chạy tạo một thư mục trong `results/` gồm trace từng câu (`traces*.jsonl`), `run_metadata.json` (commit, sha256 benchmark và corpus, cấu hình, phiên bản model và package, thời gian, token) và, với agent, `review_sheet.md`, `labels.csv`, `reviews.json`, `agent_metrics.json` sau khi chấm.

## 3. Lưu ý tái lập

- **Gemini không xác định hoàn toàn** (không đặt temperature) và Google có thể phục vụ bản model mới dưới cùng tên; trace ghi `modelVersion` của từng lần gọi. Chạy lại có thể khác vài câu.
- **Gói miễn phí:** `gemini-3.5-flash-lite` cho 15 request/phút và 500 request/ngày (trang Rate limit của AI Studio, 2026-11-16). Client giãn cách 4,5 s, thử lại theo `retryDelay`, và dừng khi hết hạn mức ngày (trace vẫn được ghi sau mỗi câu). Ở gói miễn phí, Google có thể dùng prompt và câu trả lời để cải thiện sản phẩm; dữ liệu gửi đi chỉ là báo cáo công khai và câu hỏi tự viết.
- Retrieval (dense, BM25, RRF, rerank) là xác định: chạy lại ra đúng thứ hạng và điểm.
- `google/embeddinggemma-2` không cố định revision (kế thừa từ Day 6); reranker cố định revision `233902d2…`.
- `starter/data/` bị `.gitignore`; file chunk được tạo lại bằng lệnh `export` ở trên và kiểm tra bằng sha256.
