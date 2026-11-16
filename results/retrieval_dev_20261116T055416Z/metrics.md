Top-k 3, candidate pool 10, context budget 800 characters (header included).

| Method | Hit@1 | Evidence Hit@3 | Context Evidence Rate | Gold in pool | MRR@pool | Avg context chunks | Median ms |
|---|---|---|---|---|---|---|---|
| dense | 16/20 (80%) | 20/20 (100%) | 6/20 (30%) | 20/20 | 0.875 | 1.05 | 217.3 |
| bm25 | 18/20 (90%) | 20/20 (100%) | 7/20 (35%) | 20/20 | 0.95 | 1 | 0.9 |
| hybrid_rrf | 18/20 (90%) | 20/20 (100%) | 7/20 (35%) | 20/20 | 0.95 | 1 | 221.3 |
| hybrid_rrf_rerank | 18/20 (90%) | 20/20 (100%) | 8/20 (40%) | 20/20 | 0.95 | 1 | 638.6 |
