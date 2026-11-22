# DeepSeek-V4.1-Flash IQ1_M (ISTA-DAS 1.75bpw) on Strata — no-DSpark vs DSpark A/B (V100 SXM2-32GB)

Measured 2026-11-23. **Not the anchor** (RULES #4). Same host/model/pack family, only DSpark toggled.

## Hardware and software
- GPU: Tesla V100-SXM2-32GB, 32 GiB, driver 580.178.04. Host: Xeon E5-2673 v3 (24 vCPU), 125 GB RAM, Omarchy Linux kernel 7.2.15-1-omarchy.
- Engine: Strata `strata-dsv41` (build-dsv41), serve wrapper `Strata-0.2.13/serve/server.py`, CUDA 12.9 runtime libs.
- Model: `DeepSeek-V4.1-Flash-1017-GSQ-RCO-IQ1_M` (ISTA-DAS 1.75bpw, 4 GGUF shards) from USB/Elements; engram `DeepSeek-V4.1-Flash-Engram-IQ4_NL.gguf`; dspark `dspark-DeepSeek-V4.1-Flash-1017-Q8_0.gguf`; mmproj `mmproj-DeepSeek-V4.1-Flash-1017-BF16.gguf`.
- Pack: rebuilt with `Strata-0.2.13/tools/dsv41/pack_gguf.py` because existing `maya-ds4` pack was IQ2_XXS-specific. No-DSpark pack `/mnt/nvme/maya-ds4-iq1m-new`; DSpark pack `/mnt/nvme/maya-ds4-iq1m-dspark` (3 MTP blocks, +mmproj).

## Config
- Common: `--gpus 0 --max-context 260000 --cpu-threads 20 --mmap-experts off --prefill-chunk 16384 --vision off --eos 1`, `kv=fp4`.
- no-DSpark: `--dspark off`, model `deepseek-v4.1-flash-iq1m`.
- DSpark: `--dspark on`, model `deepseek-v4.1-flash-iq1m-dspark`.

## Method
- Script: [`bench_lapilli_sweep.py`](bench_lapilli_sweep.py) via env `BENCH_URL/MODEL/LOG`.
- Sizes: 1024, 4096, 16384, 32768 target prompt tokens; n=4/arm; cap 256; temperature 0; `chat_template_kwargs.enable_thinking=false`.
- Fresh nonce prompt per request; `reused_tokens==0` in all rows.
- Prefill/decode: engine SSE timings. TTFT: client monotonic clock.

## Results (medians)

| Arm | prompt tok | no-DSpark prefill | DSpark prefill | no-DSpark decode | DSpark decode | no-DSpark TTFT | DSpark TTFT |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1k | 1024.0 | 164.8 | 157.1 | 13.8 | 11.2 | 6.22 | 6.54 |
| 4k | 4079.0 | 293.85 | 283.4 | 13.55 | 11.35 | 13.9 | 14.41 |
| 16k | 16385.0 | 518.9 | 523.6 | 13.4 | 10.35 | 31.62 | 31.33 |
| 32k | 32754.0 | 580.7 | 585.8 | 12.8 | 10.15 | 56.49 | 55.98 |

## Observations
- All 32/32 requests ok, `reused_tokens==0`.
- DSpark did **not** improve decode on this quant/config; decode was ~15-21% lower with DSpark enabled. Prefill/TTFT near parity/noise.
- DSpark may need different tuning or may not pay off for this IQ1_M/offload shape; not investigated further.

## Raw
- [`results-no-dspark.json`](results-no-dspark.json)
- [`results-dspark.json`](results-dspark.json)
- [`serve-no-dspark.json`](serve-no-dspark.json)
- [`serve-dspark.json`](serve-dspark.json)
- [`bench_lapilli_sweep.py`](bench_lapilli_sweep.py)
