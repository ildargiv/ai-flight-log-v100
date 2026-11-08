# AI Flight Log — Tesla V100 SXM2 32 GB (Volta, sm_70)

Measured on 2026-11-05 by **ildargiv**, ongoing. Third card in the fleet line:
[rtx3060-strata-tuning](https://github.com/ildargiv/rtx3060-strata-tuning) →
[cmp90hx-strata-tuning](https://github.com/ildargiv/cmp90hx-strata-tuning) → this one.

This repo is a **flight log**, not a one-shot benchmark: dated entries, append-only, and a failed
measurement is a first-class entry with the same rank as a passing one. Rules:
[[`RULES.md`](RULES.md), template: [[`TEMPLATE.md`](TEMPLATE.md),
index + machine-readable feed: [`journal/README.md`](journal/README.md) /
[[`journal/feed.jsonl`](journal/feed.jsonl). Anchor line (comparable over time): one V100
SXM2-32GB, Qwen3.8-Flash-Next IQ3_XXS, 262,144 context, `--kv int8`, bit-exact sm_70 switches on.
From 2026-11-08 there is also one **frozen auxiliary line** (line B: V100-PCIe-32GB at 250 W,
IQ3_S, 131,072 context, [`configs/v100-pcie-iq3s-131k.json`](configs/v100-pcie-iq3s-131k.json)) used
to check whether a tuning recipe travels between machines; it never moves the anchor and never
inherits its numbers. Lines table: [journal/README.md → Hardware lines](journal/README.md).

## Hardware and software

- GPU: Tesla V100 SXM2 32 GB, GV100GL, PCI ID `10de:1db5`, subsystem `10de:1249`, SXM2-to-PCIe
  adapter. Link: PCIe 3.0 x16 (`LnkSta 8GT/s x16`; first seating read **x1** — see entry №001).
  ECC enabled, 0 errors. Power limit 300 W. No outputs (compute-only); display runs on the iGPU.
- CPU: Ryzen 5 5600G (6c/12t, Cezanne iGPU drives the desktop). RAM 96 GB (16+32+16+32, 3200 MT/s).
- OS: Ubuntu 22.04.5, kernel 6.8.0-138, Secure Boot off. Driver `nvidia-driver-580-server`
  **580.178.04** — R580 is the last NVIDIA branch with Volta; the `-open` module is Turing+ only.
- Strata: terminal/app 0.2.10, engine **0.1.57 linux-x86_64-cuda-cuda12** from the signed feed
  (release binaries 404 for the cuda12 asset; the feed carries it). No host CUDA toolkit needed.

## Model and configuration

Qwen3.8-Flash-Next GSQ-RCO IQ3_XXS (71 GB, 2 shards, native-experts), pack `iq3_xxs`, dflash2/MTP
drafting, context 262144, `--kv int8 --kv-resident 32768`, expert-cache auto (~19.25 GiB VRAM,
11,857 experts), conversation cache 12 slots / 16 GiB (`user_args`), env:
`STRATA_SM70_TABLE=1 STRATA_FUSE_DECODE=1 STRATA_ARGMAX_ROWS_SM70=1 STRATA_GR_NORM_FAST=1`
(all bit-exact per `docs/NVIDIA_V100.md`). No `STRATA_ROUTE_PRIOR` (3060-era compensation).
Full snippets: [`configs/`](configs/).

## Method

Engine's own timings; fresh-nonce prompts (`0 reused` on fresh arms), warm-up discarded; standard
protocol via `strata bench run` (suite standard-v1). Details per entry.

## Results

**№002 — standard-v1, complete, 21/21 requests, sanity 12/12** (median, min–max, n=3; 2 min 25 s
after model load; idle server):

| Case | Prompt tok/s | Decode tok/s | TTFT s |
| --- | --- | --- | --- |
| prompt-4k | 1,280 (1238–1288) | 72.8 (72.3–80.4) | 3.22 |
| prompt-16k | 1,584 (1558–1656) | 71.9 (71.7–75.1) | 10.37 |
| short | n/a per protocol | 90.8 (83.0–93.5) | 0.71 |

Raw: [`results/2026-11-05-standard-v100-sxm2-r1/`](results/2026-11-05-standard-v100-sxm2-r1/).
Community V100-32GB corridor (other hosts): prefill 1127–1633, decode 54–77 — we sit at its top.
Our RTX 3060 (unlocked fast config): prefill 684–745 → ~1.9–2.3×, decode 61 → 1.18–1.48× without
the quality-suspect prior.

**№001 first pass (n=1, nonce):** prefill 998/1535/1633 tok/s at 1.7K/8.4K/25K tokens, decode
75.5–81.1; dialogue continuation reused 47,218/47,265 prompt tokens (TTFT 2 s at 47K). Needle
(`tools/needle_bench.py`): **9/9 found** across 26.5K/106K/200.8K actual prompt tokens × depths
10/50/90 (entries №003–№004; the 200K arm closed the model's full 262,144 context). Anchor fresh-read
prefill curve: **1,560 → 1,364 → 1,271 tok/s** at 26.5K/106K/201K — flat tail, no cliff.
**№005 decode anchor (n=4, idle):** decode **70.4 / 68.6 / 63.4** tok/s at 4.5K/35K/139K prompt
tokens; prefill plateau 1,417–1,554 re-confirmed on independent nonces; the ~1.2K short arm
(105.5 ±20) is spec-acceptance noise and is explicitly *not* anchorable. Vs our unlocked 3060:
+10% decode at 139K without ROUTE_PRIOR, prefill ×2.3 at 35K.
**№006→№012: a published verdict, overturned by its own method.** №006 measured `PF_WMMA`
at −0.1% — but the switch had never reached the engine (preset-extra is lost on migration-restart).
Verified retest (direct launch, environ proof): **PF_WMMA = +9.4% prefill** (1701 vs 1555, n=4,
13/16 pairs), matching community's +10%. It is not bit-exact, so adoption waits for a quality A/B;
the anchor stays stock. `GDN_REC_WARP` (+0.3%, №011, properly verified) is genuinely below noise.

**№013 quality A/B of `PF_WMMA`** (fresh-load batteries, environ-proofed arms): 20/20 × 20/20 on an
auto-checked task battery; answers sha-identical 19/20, the single diff being JSON whitespace that
also appears within the stock arm itself — zero substantive divergences. Direction of the speed gain
reproduced (+6–24% fresh long-task prefill). Adopted for the agent profile; the release anchor stays
stock until a long-agentic quality diff (candidate №014).

## Memory structure: the DeepInfer practices, measured here

We do not run DeepInfer itself — it targets SM100/Ascend 950 and CUDA 13, none of which Volta can
even execute. But its feature list is a good checklist of what inference memory really consists
of, and every item it names has a Strata counterpart we configured and measured on this card
(entries №002–№004 cite the raw data):

| DeepInfer practice | Strata counterpart on this machine | What we actually measured |
| --- | --- | --- |
| External KV-cache system (not in their release) | three-tier engine-side cache: `--prompt-cache 12` VRAM checkpoints → conversation-cache 12 slots / 16 GiB RAM parking → `SAVE/RESTORE` disk sessions (`--session-save-reclaim`) | dialogue continuation re-read **47 of 47,265** tokens (TTFT 2 s); evictions after tuning: 19→0 |
| KV management (resident window + streaming) | `--kv int8 --kv-resident 32768`, KV streaming | engine reports **97.9–99.0%** of KV block reads hit VRAM while holding 200K-token sessions in RAM |
| MoE expert placement (EP + EPLB) | `--expert-cache auto` (11,857 experts resident, ~19.25 GiB), no `ROUTE_PRIOR` (that was the 12 GB card's compensation) | hit on a clean single instance: 93–98% (№009; the early 66–75% readings were the documented double-launch race, no squeeze from the conversation cache) |
| Confidence-scheduled verification | dflash2 drafting, `--spec 6 --draft-conf 0.8` | drafts accepted, e.g. 98/122; decode 72–91 tok/s in standard-v1 |
| Asynchronous scheduling / batch-invariance | sm_70 build paths: #540 attention, `prompt_attn_v70` (`mma.m8n8k4`), bit-exact `SM70_TABLE`+`FUSE_DECODE`+`ARGMAX_ROWS`+`GR_NORM` | fresh-read prefill curve 1,560→1,364→1,271 tok/s (26.5K/106K/201K), answers bit-stable at defaults |
| Deterministic measurement | greedy, engine-own timings, nonce prompts, `0 reused` on fresh arms | sanity 12/12, 21/21 protocol requests |

What has no single-GPU desktop equivalent: prefill/decode disaggregation and DP load balancing —
the analogy deliberately stops there, same as in our [RTX 3060 log](https://github.com/ildargiv/rtx3060-strata-tuning).

## Gotchas (the failures, in order — each one is an entry with repro steps)

1. Driver 595-open: Volta simply not supported (branch + open-module), `nvidia-smi` dead on arrival.
2. GitHub release has no cuda12 engine (404); the signed feed does.
3. `setup.py --cuda 12` doesn't see the components manager and tries to re-download the 47 GB
   model → symlink `engine-cuda12/` + `--gguf-dir`.
4. A 3060-era systemd service silently capped the V100 at 187 W on first test restart.
5. SXM2 adapter first seating: `LnkSta x1 (downgraded)` → decode 47.5 instead of 75+.
6. Runtime regenerates launch configs from presets: hand-edit `args` gets wiped — `user_args`
   only; profile migration needs `--allow-source-migration --if-source-sha256` from `--plan`.
7. Operator mistakes kept in the log too (sudo -S vs heredoc stdin collision; wrong pid kill;
   autostart racing a manual server start).

## What this card is not

No unlock needed or possible (Volta has no GeForce half-rate gate — tensor is full rate stock;
measured in №008-И after №008 had to be corrected (published before the run finished):
fp16→fp32 median **90.75 TF/s** (73–78% of the 125 spec; ×1.86 our unlocked 3060). `COMPUTE_16F`
accepted on Volta, closing the rc-15 gap the 3060 runbook left open. FP32/BF16 completed after the harness fix
(№010): FP32 pedantic 13.69 TF/s (87% of spec); BF16 accepted on sm_70 but **emulated at 9.78
TF/s** — slower than FP32, no native tensor path — which numbers-out why the engine converts
BF16→FP16 on Volta (`STRATA_BF16_TC`). No BF16/INT8 tensor, no CUDA 13, no DeepSeek V4.1-Flash class packs —
Volta support is security-only to ~2028, and this log documents the tail end honestly.

## License

Text, scripts, configs, results: MIT. Model weights, packs and NVIDIA components keep their own licenses.

---

# Русская версия (кратко)

Живой бортовой журнал третьей карты парка: Tesla V100 SXM2 32 GB (Volta, sm_70), Strata 0.1.57
(готовый cuda12-движок из подписного фида), драйвер 580.178.04-server (последняя ветка с Volta),
Ubuntu 22.04, 5600G, 96 ГБ RAM 3200. Правила журнала: append-only; неудачная запись = равноценная
запись с признаком и обходом; якорная линия — IQ3_XXS/262K/`--kv int8`/бит-в-бит sm_70-тумблеры.
С 2026-11-08 есть и **замороженная вспомогательная линия B** (V100-PCIe-32GB 250 Вт, IQ3_S,
131 072, `configs/v100-pcie-iq3s-131k.json`) — она проверяет, переносится ли настройка между
машинами; якорь она не двигает и его цифры не наследует. Таблица линий — в `journal/README.md`.

**standard-v1 (протокол): complete, 21/21, sanity 12/12, n=3:** prefill **1280** (4k) / **1584**
(16k) tok/s, decode **72.8** / **71.9**, короткий прогон 90.8, TTFT 0.7–10.4 с — верх community-
коридора V100 (1127–1633 / 54–77). Против нашей разблокированной 3060: prefill ×1.9–2.3, decode
×1.18–1.48, и без подозрительного prior. Первый диалоговый тест: из 47265 токенов продолжения
движок дочитал **47** — кэш разговоров работает.

Неудачи, вошедшие в журнал: 595 не знает Volta; cuda12-движка нет на GitHub-релизах (есть в фиде);
setup перекачивает модель (лечится `--gguf-dir`); сервис-наследие резал карту до 187 Вт; первое
посаживание адаптера — линк ×1 (decode падал до 47.5); ручные правки конфигов затираются runtime'ом
(канал `user_args`); плюс операторские ошибки без купюр. Иглы 26.5K/106K/200.8K × глубины 10/50/90 — **9/9** (№003–№004), полный контекст 262,144 закрыт; кривая fresh-read prefill 1560→1364→1271 tok/s. Якорь декода (№005, n=4, idle): **70.4/68.6/63.4 tok/s** на 4.5K/35K/139K; короткий рукав — шум спекуляции, не якорится. A/B `PF_WMMA` (№006→№012): первый тест был невалиден (тумблер не попадал в движок); верифицированный перезамер даёт **+9.4%** prefill — обещание community подтвердилось; adoption на паузе до quality-A/B, якорь остаётся stock. `GDN_REC_WARP` (№011): +0.3% — действительно под шумом. Quality-A/B `PF_WMMA` (№013): батареи 20/20 против 20/20, ответы совпадают (единственная разница — пробел в JSON, тот же класс флуктуации живёт и внутри stock), скорость подтвердила направление; тумблер включён в агентский профиль, якорь релизов остаётся stock. GEMM (№008-И, корректировка к поспешной №008): **90.75 TF/s** медиана fp16→fp32 (×1.86 против нашей разблокированной 3060); COMPUTE_16F принят — зазор runbook закрыт реальным прогоном; FP32/BF16 домерены после ремонта харнеса (№010): FP32 13.69, BF16 принят, но эмуляция 9.78 TF/s — медленнее FP32; нативного BF16 нет, обоснован конверт движка в FP16.

Память настроена по мотивам DeepInfer (сам он на Volta не запускается — SM100/CUDA13): трёхслойный кэш разговоров (чекпойнты в VRAM → парковка 12 слотов/16 ГиБ в RAM → дисковые сессии SAVE/RESTORE), KV int8-стриминг с 97.9–99% попаданий в VRAM, детерминированные замеры. Маппинг «практика DeepInfer → наша настройка → цифра» — в разделе «Memory structure: the DeepInfer practices» выше.

Подписка: Watch → Releases, каждый выпуск = запись журнала. Мини-статьи для постов:
[`outreach/`](outreach/).
