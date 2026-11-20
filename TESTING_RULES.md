# Testing rules — DeepSeek-V4.1-Flash IQ2_XXS on Strata sm_70

Rules for measuring **this model** so results from different machines can be compared side by side.
They extend the journal's [`RULES.md`](RULES.md) and follow the
[Strata community benchmark guide](https://github.com/Niko1221/Strata/blob/main/docs/COMMUNITY_BENCHMARKS.md).
This is one experimental branch: DeepSeek-V4.1-Flash, ISTA-DAS IQ2_XXS (2.00 bpw),
custom `maya-ds4` pack. It does **not** move the journal's Qwen3.8-Flash-Next IQ3_XXS
anchor (RULES #4).

## 1. What to measure

One fixed set of arms on every machine: fresh (non-reused) prompts of about
**1k, 4k, 16k, 32k, 64k, 128k** tokens; the same **256-token** generation cap;
at least **3 runs per arm** (4 preferred for decode — RULES #5). Record:

- **prefill**, tok/s — engine timing (`timings.prompt_per_second`) together with
  `prompt_n` (freshly read) and `cache_n` (reused) tokens;
- **decode**, tok/s — engine timing (`timings.predicted_per_second`). Never divide
  generated tokens by the whole request time;
- **TTFT**, s — client clock, from request sent to the first non-empty content token;
  ignore keep-alives and empty deltas; state whether the first token is reasoning or answer;
- **reused / read tokens** — from `usage.prompt_tokens_details.cached_tokens` and
  `timings`; a fresh arm must report `reused == 0`, otherwise the arm is not a valid
  prefill comparison;
- **memory** — VRAM and RAM at idle and at peak, if measurable;
- **failures, timeouts, OOM and refused requests** — record as failures, never drop.

## 2. How to run

1. Engine: `strata-dsv41`, source build for `sm_70` (CUDA 12), pack `maya-ds4`,
   model id `deepseek-v4.1-flash-iq2xxs`, `--max-context 260000`. Report the exact
   BUILD_ID / source commit and every launch argument (with secrets removed).
2. Close other GPU work; the server must be idle. If any agent or other traffic touches it
   during the run, mark the entry `under-traffic` and do not use it for decode conclusions.
3. Warm up with one short request (~24 output tokens), excluded from results.
4. Prompts: deterministic synthetic records such as
   `record000001: alpha beta gamma delta ...`, each request prefixed with a unique
   `[bench <nonce>]` tag. A new nonce per run means no prefix-cache help.
   Target length must be within ±2% of the arm, verified via `usage.prompt_tokens`.
5. Thinking off: `reasoning_effort: "none"` and
   `chat_template_kwargs: {"enable_thinking": false}`. Greedy `temperature: 0`,
   `max_tokens: 256`. If the model stops early, record the actual generated count.
6. Stream `/v1/chat/completions`; take speed numbers from the engine's `timings`
   object in the last chunk, TTFT from the client clock.
7. Save raw data in `results/YYYY-MM-DD-<hardware>-dsv41/`: `results.json`
   (every request), `README.md` (medians and ranges), `engine-log-excerpt.txt`,
   the launch config and the measurement script. See our
   [`results/2026-11-20-v100-sxm2-dsv41-context/`](results/2026-11-20-v100-sxm2-dsv41-context/)
   and its `ctx_sweep.py` for a working example.

## 3. What not to do

- Do not merge this model/quant with the Qwen IQ3_XXS/262K/`--kv int8` anchor line (RULES #4).
- Do not publish decode from a single run: without 4 repeats it is an observation,
  not a conclusion (RULES #5). A difference of <3 tok/s is "within noise".
- Do not call a prefill arm "cold" if the engine has already answered requests:
  report reused tokens explicitly.
- Do not place a journal entry before the raw result files exist (RULES #9 / №008-И).
- Do not publish home paths, IP addresses, keys or private prompts: redact them.

## 4. Where to send results

Open a pull request to [`ildargiv/ai-flight-log-v100`](https://github.com/ildargiv/ai-flight-log-v100)
with a `results/` folder, a `journal/entries/NNN.md` entry and one line in
`journal/feed.jsonl`. If a PR is not possible, open a GitHub issue with the same raw files.
A failure is a first-class entry: give its class
(`железо` / `драйвер` / `движок` / `конфиг` / `оператор` / `харнес`), the symptom
("how to recognise it") and the workaround ("what to do instead").

---

# Правила тестирования (RU)

Измеряйте ту же модель одинаково, чтобы цифры разных машин можно было сравнивать.
Это экспериментальная ветка (DeepSeek-V4.1-Flash, ISTA-DAS IQ2_XXS 2.00 bpw, пак `maya-ds4`),
она не двигает якорную линию Qwen IQ3_XXS/262K (RULES #4).

Рукавы: свежие промпты ~1k/4k/16k/32k/64k/128k токенов, кап генерации 256,
минимум 3 прогона на рукав (для decode лучше 4). Скорость prefill/decode — из
`timings` движка, TTFT — клиентскими часами, `reused` на свежих рукавах обязан быть 0.
Уникальный nonce в каждом промпте, thinking выключен, greedy, ноль лишней нагрузки на GPU.
Сырьё: `results.json` + выдержка лога + конфиг + скрипт. Результат — PR с записью
журнала и строкой в `journal/feed.jsonl`; неудача оформляется наравне с успехом
(класс, признак, обход). Цифры публикуются только после появления сырых файлов.
