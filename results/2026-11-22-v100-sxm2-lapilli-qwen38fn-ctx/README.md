# Context sweep — Qwen3.8-Flash-Next UD-Q4_K_XL (Basalt) on Tesla V100 SXM2-32GB (lapilli-v100)

Measured 2026-11-22. Experimental line: `lapilli-v100` / `basalt` (git `024d61c`, sm_70 build)
serving `Qwen3.8-Flash-Next UD-Q4_K_XL.basalt` (~108 GiB). **Not the anchor**: Qwen3.8-Flash-Next
IQ3_XXS / 262K / `--kv int8` stays the anchor (RULES #4). Different engine, format, quant/package,
and context limit.

## Hardware and software

- GPU: Tesla V100-SXM2-32GB, 32 GiB VRAM, driver 580.178.04. Host: Xeon E5-2673 v3 (24 vCPU),
  125 GB RAM, Omarchy Linux kernel 7.2.15-1-omarchy. Same second host as №018.
- Engine: `lapilli-v100` / `basalt`, git `024d61c`, CUDA 12.9 runtime libs via `LD_LIBRARY_PATH`.
  Served via `.venv/bin/python -m serve.server --engine-bin .../bin/basalt --model ...Qwen3.8-FN-UD-Q4_K_XL.basalt --port 8080 --host 0.0.0.0`.
- Model: `Qwen3.8-Flash-Next UD-Q4_K_XL`, Basalt package, source `jesdga/Qwen3.8-Flash-Next-Basalt`,
  file size 115964116992 bytes (~108 GiB). Loaded with `max_context=8192`.
- Launch/runtime config: [`run-config.json`](run-config.json).
- Other GPU work: none during sweep; DeepSeek `strata-dsv41` was stopped before loading lapilli.

## Method

- Script: [`bench_lapilli_sweep.py`](bench_lapilli_sweep.py), standard library only.
- Arms: target 1024 / 4096 / 6144 prompt tokens; actual measured prompt tokens 1228 / 4908 / 7370.
  8192-target arm not run because server reported `max_context=8192` and the 7370-token arm was already near limit.
- 4 runs per arm, `max_tokens=256`, `temperature=0`, `stream=true`.
- Thinking off: `chat_template_kwargs.enable_thinking=false`.
- Fresh nonce-tagged prompt per request; `reused_tokens==0` in all 12 rows.
- Prefill/decode: engine timings from SSE `timings` (`prompt_per_second`, `predicted_per_second`).
- TTFT: client monotonic clock, first non-empty content delta.
- Draft/speculative stats recorded from SSE (`draft_n`, `draft_n_accepted`) where present.

## Results (medians, n=4)

| Target arm | Actual prompt tok | Reused | Read | Prefill tok/s | Decode tok/s | Draft acc/offered | TTFT s | Total s |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1024 | 1228 | 0 | 1228 | 658.40 | 83.35 | 21/24 (typical) | 1.96 | 4.93 |
| 4096 | 4908 | 0 | 4908 | 1107.40 | 94.05 | 22/24 (typical) | 4.55 | 7.16 |
| 6144 | 7370 | 0 | 7370 | 1350.25 | 86.10 | 21/24 (typical) | 5.57 | 8.43 |

Full per-run rows, min/max, and metadata: [`results.json`](results.json).
Engine/log excerpt: [`engine-log-excerpt.txt`](engine-log-excerpt.txt).

## Observations

- `reused_tokens` is 0 for every request; prompt cache reuse did not affect the sweep.
- Prefill throughput increases with prompt length in this range (658 -> 1107 -> 1350 tok/s median),
  while decode stays ~83-94 tok/s. This is an observation on this engine/model/context window, not a general claim.
- Draft acceptance is high in sampled rows (21-22 accepted out of 24 offered).
- The 6K arm reached actual 7370 prompt tokens, close to the server `max_context=8192` with 256 generation cap; larger context arms were not attempted.

## Reproduce

```bash
# on server, with lapilli-v100 serving on 127.0.0.1:8080 and model loaded
python3 bench_lapilli_sweep.py --sizes 1024,4096,6144 --runs 4 --cap 256 --out ./bench-lapilli-qwen38fn-ctx
```

Raw data: `results.json`, `bench_lapilli_sweep.py`, `engine-log-excerpt.txt`, `run-config.json`.
