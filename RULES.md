# Правила журнала

> Пункты 1–8 — в этом файле; пункт 9 и далее — в [`journal/RULES.md`](journal/RULES.md)
> (append-only блок правил). EN: items 1–8 live here, item 9 and later in `journal/RULES.md`.

1. **Append-only.** Записи не редактируются задним числом. Ошибся в цифре — новая запись
   «Корректировка к №NNN». Старая остаётся как есть: ценность журнала в том, что видно,
   что и когда было известно.
2. **Неудача = запись того же ранга, что успех.** У каждого провала обязательны поля
   «как понять, что это оно» (признак/лог/цифра) и «что делать вместо» — иначе это жалоба,
   а не данные.
3. **Класс неудачи** — один из: `железо` / `драйвер` / `движок` / `конфиг` / `оператор`
   (моя ошибка в действиях) / `харнес` (ошибка измерения). По классу потом видно, где
   система сыпется чаще всего.
4. **Якорь.** Линия равнения одна: V100 SXM2-32GB + IQ3_XXS + 262K + `--kv int8` + бит-в-бит
   sm_70-тумблеры. Меряется при каждом стабильном релизе движка. Экспериментальные ветки
   (другие модели/кванты/тумблеры) — отдельные записи, якорь не двигают.
   - Дополнение 2026-11-08 (№015): помимо якоря допускается **фиксированная вспомогательная
     линия** — своя карта/квант/контекст и **неизменяемый** конфиг в `configs/`; правка конфига
     означает новую линию и новую запись. Сравнение железа ведётся только «линия ↔ линия»,
     таблица линий — в `journal/README.md`; линия не двигает якорь и не наследует его цифры.
     EN: besides the single anchor line, one frozen auxiliary line is allowed (own card / quant /
     context with an immutable config in `configs/`); hardware is compared only line ↔ line; the
     corridor table lives in `journal/README.md`; a line never moves the anchor nor inherits its
     numbers.
5. **Шум.** Decode без 4 повторов на idle-сервере — не вывод, а наблюдение. Разницу <3 tok/s
   записываем как «в пределах шума». Прогон с агентским трафиком помечается `under-traffic`.
6. **Машиночасть.** Каждая запись дублируется строкой в `journal.jsonl` (поля: id, date, kind
   (успех|неудача|нейтраль|корректировка), class, hardware, engine, summary, numbers,
   links). Graph-Tools/CHAI-режимы — только из jsonl.
   - Дополнение 2026-11-08 (№015): файл feed — `journal/feed.jsonl`; поле `hardware` обязательно
     начиная с №014 (slug машины: `v100-sxm2-32gb`, `v100-pcie-32gb`), старые строки не
     дописываются (п.1); `class` перечисляет все классы неудач внутри записи, включая `harness`,
     иначе счётчик «где система сыпется» (п.3) врёт.
     EN: the feed file is `journal/feed.jsonl`; `hardware` is mandatory from №014 and older rows
     are not back-filled; `class` must list every failure class inside the entry, `harness`
     included, otherwise the "where it breaks" tally (item 3) lies.
7. **Цифры — из движка** (engine timings / лог-строка `prompt ... = ... reused + ... read`),
   не из HTTP-стрима. Проверено на своей шкуре, см. №001.
8. Ссылки на сырьё: `results/` — JSON по протоколу, `logs/` — выдержки логов движка
   (обезличенные), `configs/` — конфиги запуска с `user_args`.
   - Дополнение 2026-11-08 (№015): заявления о питании и троттлинге — это тоже цифры, а значит
     требуют сырьё: рядом с прогоном пишется `results/<run>/power.log`
     (`nvidia-smi dmon -s pucvmet -d 1`), и на него ссылается запись. Вт/°C/pclk «на глаз» без
     файла не являются измерением (урок №014).
     EN: power and throttling claims are numbers too, so they need raw data: write
     `results/<run>/power.log` (`nvidia-smi dmon -s pucvmet -d 1`) next to the run and link it;
     W / °C / clocks quoted without a file are not a measurement (lesson of №014).
