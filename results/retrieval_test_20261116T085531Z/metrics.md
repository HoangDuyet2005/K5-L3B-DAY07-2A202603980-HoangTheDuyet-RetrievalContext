Top-k 3, candidate pool 10, context budget 800 characters (header included).

| Method | Hit@1 | Evidence Hit@3 | Context Evidence Rate | Gold in pool | MRR@pool | Avg context chunks | Median ms |
|---|---|---|---|---|---|---|---|
| dense | 7/9 (78%) | 7/9 (78%) | 5/9 (56%) | 9/9 | 0.821 | 1.11 | 212.9 |
| hybrid_rrf | 6/9 (67%) | 8/9 (89%) | 5/9 (56%) | 9/9 | 0.773 | 1 | 206.1 |
