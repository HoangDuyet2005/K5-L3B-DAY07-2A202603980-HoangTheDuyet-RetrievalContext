Top-k 3, candidate pool 10, context budget 2700 characters (header included).

| Method | Hit@1 | Evidence Hit@3 | Context Evidence Rate | Gold in pool | MRR@pool | Avg context chunks | Median ms |
|---|---|---|---|---|---|---|---|
| dense | 16/20 (80%) | 20/20 (100%) | 20/20 (100%) | 20/20 | 0.875 | 3 | 217.9 |
| bm25 | 18/20 (90%) | 20/20 (100%) | 20/20 (100%) | 20/20 | 0.95 | 3 | 0.7 |
| hybrid_rrf | 18/20 (90%) | 20/20 (100%) | 20/20 (100%) | 20/20 | 0.95 | 3 | 217.4 |
| hybrid_rrf_rerank | 18/20 (90%) | 20/20 (100%) | 20/20 (100%) | 20/20 | 0.95 | 3 | 668.1 |
