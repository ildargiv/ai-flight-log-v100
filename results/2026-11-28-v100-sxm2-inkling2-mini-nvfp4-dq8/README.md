# 2026-11-28 · V100 SXM2 32 GB · Inkling 2 Mini NVFP4 DQ8 (Lapilli/Basalt v0.6.0-v100.1)

Сырьё к записи [`journal/entries/021.md`](../../journal/entries/021.md).

## Что мерили

Полный тест модели **Inkling 2 Mini NVFP4 DQ8** (`Inkling-2-Mini-NVFP4-DQ8.basalt`, 19 GiB, SHA256 `f7b4e5f8e17681c4735a7dfc51ffd8e805c44184fad4e1778b13187d79dc3787`) на **Lapilli/Basalt v0.6.0-v100.1** (`6f0a1e6bca-dirty`, CUDA 12.9, gcc-14, sm_70, `BASALT_MODELS=qwen4exp;inkling2`).

Железо: 1× Tesla V100-SXM2-32GB, driver 580.178.04, Xeon E5-2673 v3 (24 cores), 125 GiB RAM. Сервер: `--gpu 0 --kv fp16 --vram-reserve-mib 700 --port 8080 --alias Inkling-2-Mini`, `spec=8`, ctx 65536.

## Команды

Базовый прогон (4 повтора, depth-decode 64):

```bash
basalt-bench --model /home/omarchy/build/lapilli-v100/models/Inkling-2-Mini-NVFP4-DQ8.basalt \
  --engine bin/basalt --fixtures data/bench/inkling2 \
  -t conv,struct,prose -p 16384,32768,65536 \
  -r 4 --depth-decode 64 --seed 1 --logs /home/omarchy/inkling-bench-logs \
  --kv fp16 --vram-reserve-mib 700 --gpu 0 -o json
```

Глубокий prefill (2 повтора, depth-decode 64, ctx 505469):

```bash
basalt-bench --model /home/omarchy/build/lapilli-v100/models/Inkling-2-Mini-NVFP4-DQ8.basalt \
  --engine bin/basalt --fixtures data/bench/inkling2 \
  -p 131072,262144,524288 \
  -r 2 --depth-decode 64 --seed 1 --logs /home/omarchy/inkling-deep-logs \
  --kv fp16 --vram-reserve-mib 700 --gpu 0 -o json
```

## Базовый прогон (mean ± stddev, n=4)

| test | tok/s mean | stddev | accept % | draft len | README |
|---|---:|---:|---:|---:|---:|
| tg conv | 121.19 | 0.71 | 67.54 | 1.59 | 121 |
| tg struct | 215.72 | 3.58 | 97.74 | 5.48 | 214 |
| tg prose | 101.63 | 0.29 | 50.98 | 1.22 | — |
| pp16384 | 1427.07 | 8.71 | — | — | 1567 |
| pp32768 | 1351.77 | 6.80 | — | — | 1459 |
| pp65536 | 1218.03 | 3.28 | — | — | — |

Decode после prefill (depth-decode 64, из progress log): после 32k ~90.5–93.4 tok/s, после 64k ~76.7–78.2 tok/s (наблюдения run 1–2).

## Глубокий prefill (mean ± stddev, n=2)

| test | prompt tokens | tok/s mean | stddev | decode after prefill (run 1 / run 2) |
|---|---:|---:|---:|---:|
| pp131072 | 126361 | 1019.12 | 15.39 | 57.7 / 61.7 tok/s |
| pp262144 | 252705 | 679.63 | 1.90 | 44.6 / 48.4 tok/s |
| pp524288 | 505393 | 466.85 | 0.88 | 26.3 / 25.7 tok/s |

512k префилл прошёл на одной V100 32GB без OOM; во время глубокого прогона GPU была загружена ~31.7 GiB, часть экспертного кэша ушла в RAM (`ram_experts_mib=7059`, `expert_tiers=main/72/8006,peer/0/0,ram/56/7059,file/0/0`).

## Файлы

- `inkling-full.json` — сырой JSON базового прогона.
- `inkling-deep.json` — сырой JSON глубокого прогона.
- `inkling-full-run.log`, `inkling-deep-run.log` — логи запуска.
- `inkling-bench-progress.log`, `inkling-deep-progress.log` — прогресс/итоговые строки bench.
- `inkling-serve.log` — лог сервера (smoke/API проверки).
