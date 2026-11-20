# Context sweep — DeepSeek-V4.1-Flash IQ2_XXS on Tesla V100 SXM2-32GB (Strata sm_70)

Measured 2026-11-20. First context-length data point for this model as a separate
experimental line (see journal entry №018). **Not the anchor**: Qwen3.8-Flash-Next
IQ3_XXS / 262K / `--kv int8` stays the anchor (RULES #4).

## Hardware and software

- GPU: Tesla V100-SXM2-32GB, 32 GiB VRAM, driver 580.178.04, CUDA 13.0 reported by
  the driver; power cap 300 W; idle temperature 50–58 °C during setup. Second host in
  the fleet: Xeon E5-2673 v3 (24 vCPU), 125 GB RAM, Omarchy Linux kernel 7.2.15.
- Storage: OS/home on SATA SSD; model pack `maya-ds4`, Engram, dspark and mmproj
  symlinked from a separate NVMe (HFM256GDJTNG-8310A) mounted at `/mnt/nvme`.
- Engine: `strata-dsv41 0.1.59 build 712fec6b4`, source build for `sm_70`, CUDA 12.9.1.
- Model: DeepSeek-V4.1-Flash, ISTA-DAS IQ2_XXS, 2.00 bpw, pack `maya-ds4`,
  model id `deepseek-v4.1-flash-iq2xxs`, `--max-context 260000`.
- Launch config (redacted): [`run-config.json`](run-config.json).
- Other GPU work: none; server idle except this sweep. No `under-traffic` marker.

## Method

Script: [`ctx_sweep.py`](ctx_sweep.py). Six arms — 1k, 4k, 16k, 32k, 64k, 128k prompt
tokens, four runs each, 256-token output cap, greedy, thinking off. Each request
uses a unique `[bench <nonce>]` prefix and deterministic synthetic record filler;
`reused == 0` on every measured run. Calibration: ~15.33 tokens/word, overhead ~18.
Warm-up and length-probing requests are excluded from the summary.

Prefill/decode throughput are the engine's own `timings` from the last stream chunk;
TTFT is client-side (first non-empty content delta). The engine log lines were matched
to requests by prompt-token count and are included in
[`engine-log-excerpt.txt`](engine-log-excerpt.txt). `results.json` holds every request
and the medians/ranges.

## Results

_To be filled from the completed raw JSON._

| arm | actual prompt t | reused | prefill tok/s (median, min–max) | decode tok/s (median, min–max) | TTFT s | CPU lane % |
| --- | ---: | ---: | --- | --- | --- | --- |
| 1K | 1,024 | 0 | 160.2 (160.2–160.7) | 12.1 (10.9–13.7) | 6.4 | 3.6 |
| 4K | 4,079 | 0 | 270.3 (269.6–272.3) | 13.2 (12.8–13.5) | 15.1 | 3.3 |
| 16K | 16,385 | 0 | 468.4 (466.9–470.4) | 11.6 (11.3–12.8) | 35.0 | 2.5 |
| 32K | 32,754 | 0 | 492.9 (484.3–496.8) | 11.4 (10.6–12.5) | 66.5 | 1.7 |
| 64K | 65,520 | 0 | 584.1 (582.8–584.3) | 11.6 (8.7–11.9) | 112.3 | 1.1 |
| 128K | 131,055 | 0 | 626.7 (624.5–627.6) | 10.4 (9.9–11.1) | 209.4 | 0.65 |

`results.json` was reconstructed from the server's raw per-run digest lines and its
printed summary after the SSH link dropped during the final file transfer; every row
comes from an actual measured request (24 rows, n=4 per arm).

## Limitations

- Single engine session, single GPU; no second-build A/B and no quality battery here.
- Decode on the 1k arm is dominated by drafting/speculation noise; per RULES #5 it is
  an observation, not a conclusion. Differences below 3 tok/s are within noise.
- The 128k arm fits in the 260k context but has no needle/recall check in this run.
- Other host in fleet (Ryzen 5600G) not measured for this model — do not transfer these
  numbers to the anchor card.
