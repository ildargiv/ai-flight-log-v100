# Inkling-2-Mini UD-IQ1_S mainline smoke (llama.cpp, V100 SXM2)

- Date: 2026-11-23
- Hardware: Tesla V100-SXM2-32GB (sm_70), Xeon E5-2673 v3, 125GB RAM, Omarchy Linux 7.2.15-1-omarchy
- Engine: llama-server b12648 (CUDA 12.8 build), mainline GGUF
- Model: `Inkling-2-Mini-UD-IQ1_S-mainline.gguf` (7.3G), alias `inkling-2-mini-ud-iq1s-mainline`
- Launch: `llama-server -m /home/omarchy/Models/_tmp/Inkling-2-Mini-UD-IQ1_S-mainline.gguf -ngl 99 -c 32768 --host 0.0.0.0 --port 8081 --alias inkling-2-mini-ud-iq1s-mainline --jinja`
- Benchmark: fresh nonce per request, `temperature=0`, `max_tokens=128`, `stream=false`, 3 runs/arm, warmup excluded
- Arms: ~1k/4k/16k prompt tokens (actual prompt_tokens from usage)

## Results

| Arm target | prompt_tokens (med) | prefill tok/s med [min,max] | decode tok/s med [min,max] | prompt_ms med [min,max] | cached_tokens | notes |
|---:|---:|---:|---:|---:|---:|---|
| 1024 | 1115 | 634.14 [43.62,655.20] | 35.02 [35.01,35.05] | 1758.3 [1681.9,25514.4] | [0, 13, 0] | cold prefill outlier in run1; run2 had cached_tokens=13 (cache artifact) |
| 4096 | 4334 | 508.17 [507.50,508.31] | 32.49 [32.45,32.50] | 8528.6 [8526.3,8539.8] | [0, 0, 0] |  |
| 16384 | 17294 | 354.74 [354.43,355.55] | 31.23 [31.21,31.24] | 48745.6 [48642.5,48793.9] | [0, 0, 0] |  |

## Notes

- This is a **smoke/observation** run, not an anchor and not comparable to DeepSeek/Qwen anchor lines (different model, engine, quant, ruleset).
- 1k run1 prefill was 43.62 tok/s while runs2/3 were 655.20/634.14 tok/s; likely cold/warmup effect. Reported honestly; exclude run1 for prefill conclusions.
- 1k run2 reported `cached_tokens=13` despite fresh nonce; flagged as cache artifact. Other runs report `cached_tokens=0`.
- Decode is stable across arms (~35.0 to ~31.2 tok/s median).
- GPU observed at 100% utilization during 16k arm, ~13.2GB/32GB VRAM used, ~209W.

## Files

- `results.json` - raw per-request results
- `inkling_smoke.py` - benchmark script
- `run-config.txt` - launch/config summary
