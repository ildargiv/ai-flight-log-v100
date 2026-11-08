# Flight log / Бортовой журнал

Index of dated entries. Language policy: root README is EN-first with a RU duplicate; entries are
written in the operator's language with an EN one-liner here (full RU→EN dubbing per entry is the
next step — dubbed entries are linked as `…-en.md`). Append-only — corrections are new entries,
see [`../RULES.md`](../RULES.md) and its continuation [`RULES.md`](RULES.md).

| № | Date | Engine | Class | EN one-liner | RU |
| --- | --- | --- | --- | --- | --- |
| [001](entries/001.md) | 2026-11-05 | 0.1.56→0.1.57-cuda12 | driver/config/hw/operator | V100 brought up: what blocked it (595 no-Volta, x1 link, 187 W ghost service, user_args), n=1 first numbers prefill 998–1633 / decode 75–81 | карта встала: чем не работала; первые цифры |
| [002](entries/002.md) | 2026-11-05 | 0.1.57-cuda12 | bench/success | standard-v1 complete, 21/21, sanity 12/12: prefill 1280/1584, decode 72/91, TTFT 0.7–10.4 (n=3) | протокол пройден с первого раза |
| [003](entries/003.md) | 2026-11-05 | 0.1.57 | bench/success | needle 32k/128k × depths 10/50/90: 6/6 FOUND; fresh-read prefill 1560/1364 tok/s; depth-90 arm is prefix-contaminated, 10%-only for the anchor | иглы 6/6, в якорь идут только 10% рукава |
| [004](entries/004.md) | 2026-11-05 | 0.1.57 | bench/success | needle 200,852 tokens x depths 10/50/90: 3/3; anchor prefill curve 1560/1364/1271 tok/s | полная контекстная линия 26.5K/106K/201K закрыта |
| [005](entries/005.md) | 2026-11-05 | 0.1.57 | bench/success | decode anchor n=4 idle: 70.4/68.6/63.4 tok/s at 4.5K/35K/139K (short arm not anchorable, spec-acceptance noise 73-114); prefill plateau re-confirmed | якорь декода зафиксирован, короткий рукав — шум спекуляции |
| [006](entries/006.md) | 2026-11-05 | 0.1.57 | failure-expected | paired A/B PF_WMMA at 35K n=4: prefill -0.1% vs claimed +10%, decode within noise; switch stays off | обещанного профита нет — дефолты остаются |
| [007](entries/007.md) | 2026-11-05 | 0.1.57 | neutral | engine calibrate: defaults hold (settings {}, nothing to apply); lead found: conv-cache may squeeze expert cache 15162->11857 | калибровка подтвердила дефолты; найдена улика по hit-rate |
|[008](entries/008.md) | 2026-11-05 | cuBLAS harness | INVALID — see 008-И | published before the run finished; its 134.5 / BF16 numbers were never measured | отменена корректировкой |
| [008-И](entries/008-И.md) | 2026-11-05 | cuBLAS harness | correction | real GEMM: fp16→fp32 med 90.75 TF/s; COMPUTE_16F accepted; D/E = harness bug; RULES: no entry before raw files | реальные числа; правила ужесточены |
| [009](entries/009.md) | 2026-11-05 | 0.1.57 | correction | conv-cache squeeze hypothesis refuted: expert cache 15289 both arms; hit-rate mystery = double-launch artifact; A kept by choice (capacity, not on/off) | гипотеза не выдержала A/B; загадка hit-rate закрыта |
| [010](entries/010.md) | 2026-11-05 | cuBLAS repaired | success | GEMM-bis all arms: A 90.62 (reprod of 008-И +0.15%), FP32 13.69, BF16 accepted-but-emulated 9.78 | линия GEMM закрыта: нативного BF16 нет числом |
| [011](entries/011.md) | 2026-11-05 | 0.1.57 | success | verified GDN A/B: +0.3% prefill = under noise; stays off | GDN на целом промпте невидим; выключен |
| [012](entries/012.md) | 2026-11-05 | 0.1.57 | correction | №006 invalidated (toggle never applied); verified PF_WMMA = +9.4% prefill; adoption awaits quality A/B; RULES #9 | переворот: тумблер работает, не применялся |
| [013](entries/013.md) | 2026-11-06 | 0.1.57 | success | PF_WMMA quality battery: 20/20 both arms, 0 substantive answer diffs (1 whitespace, also intra-stock), speed reproduced; adopt in agent profile, anchor stays stock | батарея чистая: качество не изменилось |
| [014](entries/014.md) · [EN](entries/014-en.md) | 2026-11-08 | 0.1.56-cuda12 | bench/success | V100-PCIE-32GB + IQ3_S: the sm_70 recipe replicated — PF_WMMA +5.5% prefill, decode core +5–7% (11/12 pairs, n=3 alternating; 4th round after a pause reversed), quality 24/24 identical | PCIe-карта: рецепт переносится, PF_WMMA +5.5%, decode +5–7% |
| [015](entries/015.md) · [EN](entries/015-en.md) | 2026-11-08 | 0.1.56 / 0.1.57 | neutral/harness/config | Line B opened as a frozen second hardware line (V100-PCIe + IQ3_S + 131K): 16K prefill parity with the anchor, what 14 Xeon cores buy (CPU expert path 18.4 GB/s > 12 GB/s PCIe link) and what they do not; cross-card deltas stay confounded until a crossing point is run | открыта линия B (PCIe-карта) как вторая контрольная; паритет по 16K prefill; что дают 14 ядер и чего они не дают; сравнение карт нерасщеплено |

Machine feed: [`feed.jsonl`](feed.jsonl). Raw bench data: [`../results/`](../results/). Rules
continuation (пункт 9+): [`RULES.md`](RULES.md).

## Hardware lines / Линии железа (RULES #4)

Сравнение железа ведётся только «линия ↔ линия»; ячейки — медианы standard-v1, n=3, конфиг линии
с включёнными sm_70-тумблерами. EN: hardware is compared only line ↔ line; cells are standard-v1
medians, n=3, line config with the sm_70 switches on.

| Line | Hardware | Quant | Context | Prefill 4k / 16k | Decode 4k / 16k | Decode short | Peak W | Engine | Last entry |
| --- | --- | --- | ---: | --- | --- | ---: | ---: | --- | --- |
| **A — anchor / якорь** | V100 SXM2-32GB 300 W · Ryzen 5 5600G 6c/12t · 96 GiB RAM | IQ3_XXS | 262 144 | 1280 / 1584 | 72.8 / 71.9 | 90.8 | 300 | 0.1.57 | [013](entries/013.md) |
| **B — reference / вспомогательная** | V100 PCIe-32GB 250 W · Xeon E5-2690 v4 14c/28t · 63.8 GiB RAM | IQ3_S | 131 072 | 1247.1 / 1583.9 | 66.1 / 74.1 | 72.7 | 237\* | 0.1.56 | [015](entries/015.md) |

Configs: line A — `configs/agent-profile-env.json` + README «Model and configuration»; line B —
[`../configs/v100-pcie-iq3s-131k.json`](../configs/v100-pcie-iq3s-131k.json) (frozen).

Notes / замечания:
- Line B decode is an observation, not a conclusion (RULES #5): the 4th alternating round after a
  pause reversed it (№014). / Декод линии B — наблюдение: 4-й круг после паузы дал обратный результат.
- Line B stock arm (switches off): prefill 1220.7 / 1538.3, decode 69.5 / 66.2 — recipe delta on
  this card +2.2 / +3.0% prefill. / Тумблеры выключены: дельта рецепта на этой карте +2.2 / +3.0%.
- \* Peak W of line B is operator-reported, no raw file yet (RULES #8 addendum). / Пик Вт линии B
  назван оператором, сырья пока нет.
- A↔B deltas mix card + power + quant + context + engine in one number; they become readable only
  after the crossing point (same quant on both cards). См. №015, «Неудачное».
