Top-k 3, candidate pool 10, context budget 2700 characters (header included).

| Method | Hit@1 | Evidence Hit@3 | Context Evidence Rate | Gold in pool | MRR@pool | Avg context chunks | Median ms |
|---|---|---|---|---|---|---|---|
| dense | 7/9 (78%) | 7/9 (78%) | 7/9 (78%) | 9/9 | 0.821 | 3 | 245.5 |
| hybrid_rrf | 6/9 (67%) | 8/9 (89%) | 8/9 (89%) | 9/9 | 0.773 | 3 | 277.9 |
