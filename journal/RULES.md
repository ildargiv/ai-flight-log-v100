# Правила журнала, продолжение / Rules, continued

Пункты 1–8 — в [`../RULES.md`](../RULES.md); здесь — append-only продолжение (пункт 9 и далее).
EN: items 1–8 live in [`../RULES.md`](../RULES.md); this file is the append-only continuation.

9. **Env-тумблер считается применённым только после proof из environ живого движка**
   (`/proc/$(pgrep -x strata-host)/environ`, ДО первого замера). Каналы ненадёжны: preset-extra
   не переживает migration-restart; в config `env` ключ без префикса `STRATA_` молча не читается.
   «Не применилось» ≠ «эффекта нет» (урок №006→№012).
   - EN: an env switch counts as applied only after proof from the live engine's environment
     (`/proc/$(pgrep -x strata-host)/environ` on Linux; on Windows the process environment or the
     bench report's `configuration.experimental_options`), taken BEFORE the first measurement.
     Delivery channels are unreliable: a preset-extra does not survive migration-restart, and an
     `env` key without the `STRATA_` prefix is silently ignored. "Not applied" ≠ "no effect"
     (the №006→№012 lesson).
