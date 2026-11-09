# A/B raw: PF_WMMA live proof and engine 0.1.59 (2026-11-09)

Machine-readable arm summary: `arms.json`. Raw engine-timing records:

- `stock-0157-fresh.jsonl`
- `pf-0157-fresh.jsonl`
- `stock-0159-fresh.jsonl`
- `pf-0159-fresh.jsonl`

Each JSONL line contains one measured request (`kind=16k` or `35k`; warm-up lines are
not written to the arm files) with engine `timings`, actual prompt token count,
`cache_n`, draft acceptance, expert hit rate, GPU temp/power/clocks, and wall time.

## Method

- Same machine/profile: Tesla V100 SXM2-32GB, driver 580.178.04, profile `launch-lan-open`,
  Qwen3.8-Flash-Next IQ3_XXS, `max-context 262144`, `--kv int8 --kv-resident 32768`,
  conversation cache 12/16384, prompt cache 12, dflash2 draft, capped starter
  `ulimit -l 8192`.
- Arms are fresh starts; engine proof is taken from the live `strata-host` process env.
- Requests are non-streaming JSON to `/v1/chat/completions`, but speed numbers are the
  engine-provided `timings` (`prompt_per_second`, `predicted_per_second`), not client wall time.
- Prompt bodies are the frozen standard-v1 16K body plus a 16K+16K+4K body. Each request
  has a unique nonce prefix; every measured arm has `cache_n == 0`.
- Greedy (`temperature=0`, `top_p=1`, `seed=1`), `max_tokens=256`, warm-up 35K discarded.
- GPU state sampled before and after each request; server confirmed idle before every
  request (`live.state != generating`, `live.queued == 0`).

## Arm medians

| arm | case | prefill tok/s | decode tok/s | draft acc. | expert hit |
|---|---:|---:|---:|---:|---:|
| 0.1.57 stock | 16K | 1437.3 | 83.2 | 75.9% | 99.65% |
| 0.1.57 stock | 35K | 1481.2 | 79.3 | 69.9% | 99.65% |
| 0.1.57 + PF_WMMA | 16K | 1559.8 | 90.7 | 81.5% | 99.65% |
| 0.1.57 + PF_WMMA | 35K | 1603.0 | 77.8 | 74.2% | 99.70% |
| 0.1.59 stock | 16K | 1425.0 | 77.6 | 72.2% | 99.60% |
| 0.1.59 stock | 35K | 1461.2 | 83.7 | 76.2% | 99.50% |
| 0.1.59 + PF_WMMA | 16K | 1544.8 | 80.9 | 77.1% | 99.55% |
| 0.1.59 + PF_WMMA | 35K | 1608.3 | 78.3 | 75.2% | 99.65% |

## Paired medians

- `PF 0.1.57` vs `stock 0.1.57`: prefill **+8.32%** median, 8/8 wins.
- `PF 0.1.59` vs `stock 0.1.59`: prefill **+9.96%** median, 8/8 wins.
- `PF 0.1.59` vs `PF 0.1.57`: prefill **−0.21%** median, 2/8 wins — engine parity/no speed gain.
- `stock 0.1.59` vs `stock 0.1.57`: prefill **−0.95%** median, 0/8 wins — no speed gain.

Decode is intentionally not promoted: acceptance changes run-to-run and the sign differs by
prompt size. See entry №015.
