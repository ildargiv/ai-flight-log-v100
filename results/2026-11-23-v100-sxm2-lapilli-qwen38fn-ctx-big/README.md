# Big-context sweep — Qwen3.8-Flash-Next UD-Q4_K_XL (Basalt) on Tesla V100 SXM2-32GB (lapilli-v100)

Measured 2026-11-23. Continuation of №019 on the same engine/model/host, with `max_context` raised to 262144. **Not the anchor** (RULES #4).

## Hardware and software

- GPU: Tesla V100-SXM2-32GB, 32 GiB VRAM, driver 580.178.04. Host: Xeon E5-2673 v3 (24 vCPU), 125 GB RAM, Omarchy Linux kernel 7.2.15-1-omarchy.
- Engine: `lapilli-v100` / `basalt`, git `024d61c`, sm_70 build, CUDA 12.9 runtime libs.
- Model: `Qwen3.8-Flash-Next UD-Q4_K_XL.basalt` (~108 GiB), source `jesdga/Qwen3.8-Flash-Next-Basalt`.
- Serve config: `serve-262k.json` with `engine.max-context=262144`, `--engine-bin .../bin/basalt`.
- Other GPU work: none during sweep.

## Method

- Script: [`bench_lapilli_sweep.py`](bench_lapilli_sweep.py) (defensive `log_since` fix).
- Arms: 32768 / 65536 / 131072 target prompt tokens; actual 32757 / 65539 / 131066.
- 4 runs/arm, `max_tokens=256`, `temperature=0`, `stream=true`.
- Thinking off: `chat_template_kwargs.enable_thinking=false`.
- Fresh nonce prompt per request; `reused_tokens==0` in all 12 rows.
- Prefill/decode: engine SSE timings. TTFT: client monotonic clock, first non-empty content.

## Results (medians, n=4)

| Target arm | Actual prompt tok | Reused | Prefill tok/s | Decode tok/s | TTFT s | Total s |
|---:|---:|---:|---:|---:|---:|---:|
| 32768 | 32757 | 0 | 1549.7 | 81.75 | 21.30 | 24.35 |
| 65536 | 65539 | 0 | 1470.75 | 77.90 | 44.66 | 47.90 |
| 131072 | 131066 | 0 | 1329.7 | 71.25 | 98.71 | 102.24 |

Raw: [`results.json`](results.json). Config: [`run-config.json`](run-config.json).

## Observations

- All 12 requests `ok`, `reused=0`.
- Prefill stays high through 128k (1.33–1.55k tok/s median), gradually declining with context length.
- Decode declines modestly 81.75 -> 77.90 -> 71.25 tok/s across 32k/64k/128k.
- Compared to №018 (Strata dsv41, DeepSeek-V4.1-Flash IQ2_XXS, same host): much higher prefill/decode and lower TTFT, but different model/engine/format — not a clean A/B.
- Engine log per-request lines not captured by script (`engine_log_line: null`); timings from SSE.

## Reproduce

```bash
python3 bench_lapilli_sweep.py --sizes 32768,65536,131072 --runs 4 --cap 256 --out ./bench-lapilli-qwen38fn-ctx-big
```
