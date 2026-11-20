# Call for testers — DeepSeek-V4.1-Flash IQ2_XXS on Volta / any GPU

We are opening a **community measurement line** for DeepSeek-V4.1-Flash
(ISTA-DAS IQ2_XXS, 2.00 bpw) on Strata. One V100 SXM2-32GB (sm_70) was the first
data point; we want yours. A single GPU, a single context length is enough — a
failed run is just as useful as a passing one.

EN first, RU below.

## Why

The journal's anchor line is Qwen3.8-Flash-Next IQ3_XXS on one V100. This model is a
different architecture and a different quantization (2.00 bpw), so it needs its own
comparable data points: how prefill and decode scale with context on real hardware,
and where the cliffs are. No quality ranking, no "my card is faster" contest — just
repeatable numbers and honest failures.

## What to do

1. Read [`TESTING_RULES.md`](../TESTING_RULES.md) and the journal
   [`RULES.md`](../RULES.md). Run the same arms you can fit in your context,
   with the same nonce / fresh-prompt discipline and >=3 repeats.
2. Save `results.json`, a short `README.md` with medians and ranges, the engine
   log excerpt, your launch config (redacted) and your script.
3. Send it in:
   - **PR** to [`ildargiv/ai-flight-log-v100`](https://github.com/ildargiv/ai-flight-log-v100):
     add `results/YYYY-MM-DD-<hardware>-dsv41/`, a `journal/entries/NNN.md` entry
     and one line in `journal/feed.jsonl` (or just open an issue with the raw files
     and we will write the entry with you);
   - **Issue** with the same files attached if you do not want to touch git.
4. A failure entry must have a class, a symptom ("how to recognise it") and a
   workaround ("what to do instead"). A slow card is not a failure. `<3 tok/s`
   is noise; decode without 4 repeats is an observation, not a conclusion.

We will keep the raw files, credit the contributor in the journal entry and
cross-link the result from the index. Ask questions in the issue — if the answer
affects the method, we add it to `TESTING_RULES.md` as a new numbered item
(append-only, like everything else here).

## RU

Открываем линию замеров DeepSeek-V4.1-Flash (ISTA-DAS IQ2_XXS, 2.00 bpw) на Strata.
Первая точка — V100 SXM2-32GB; нужны ваши. Достаточно одной карты и одного
контекста; провал — тоже запись, а не повод не присылать.

Прочитайте [`TESTING_RULES.md`](../TESTING_RULES.md) и [`RULES.md`](../RULES.md),
прогоните доступные вам рукавы с теми же свежими nonce-промптами и >=3 повторами,
сохраните `results.json`, лог, конфиг и скрипт. Пришлите PR или issue в
[ildargiv/ai-flight-log-v100](https://github.com/ildargiv/ai-flight-log-v100) —
запись в журнале и строку в feed сделаем вместе. Неудача оформляется с классом,
признаком и обходом; медленная карта — не неудача.
