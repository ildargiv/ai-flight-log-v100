# Общий preflight для протоколов P1–P4

Выполняется перед **каждым** плечом, результат пишется в `results/<run>/env_proof.txt`.
Плечо без proof-файла в расчёт не идёт (RULES #9, уроки №006→№012, №015).

```bash
pid=$(pgrep -x strata-host) || { echo "FAIL: нет strata-host"; exit 1; }
[ "$(pgrep -cx strata-host)" = 1 ] || { echo "FAIL: больше одного движка (гонка №001/№009)"; exit 1; }

{
  date -Is
  echo "== environ";  tr '\0' '\n' < /proc/$pid/environ | grep '^STRATA_' | sort
  echo "== cmdline";  tr '\0' ' '  < /proc/$pid/cmdline; echo
  echo "== gpu";      nvidia-smi --query-gpu=name,power.limit,temperature.gpu,clocks.sm,memory.used --format=csv,noheader
  echo "== link";     sudo lspci -vv -d 10de:1db5 | grep -E 'LnkSta:'
  echo "== mem";      grep -E 'MemAvailable|Cached|SwapFree' /proc/meminfo
  echo "== psi";      cat /proc/pressure/memory
} | tee env_proof.txt
```

Условия допуска плеча:

| проверка | требование | откуда урок |
| --- | --- | --- |
| один `strata-host` | ровно 1 процесс | №001, №009 |
| environ | содержит ровно те `STRATA_*`, что заявлены для плеча | №012, №015 |
| cmdline | заявленные `--spec`, `--draft-conf`, `--kv-resident`, cache-флаги присутствуют | №015 (не тот профиль после `--start-again`) |
| линк | `Speed 8GT/s, Width x16` | №001 |
| лимит | 300 W | №001 (сервис-наследие 187 W) |
| сервер | idle: `live.state != generating`, `live.queued == 0` | RULES #5 |
| память | `full avg10` в PSI = 0.00 перед стартом | гипотеза о давлении RAM |

Общие правила замера:

- тайминги — только engine `timings` (RULES #7); nonce-префикс, `cache_n == 0` на каждом
  измеренном запросе;
- порядок плеч чередуется (ABBA или латинский квадрат), первый круг после любой паузы
  отбрасывается как warm-up (урок №017);
- на каждый запрос пишется: температура, мощность, `clocks.sm`, draft accepted/total,
  expert hit, KV streaming hit, major page faults процесса
  (`awk '{print $12}' /proc/$pid/stat` до и после);
- после серии конфиг возвращается на бэкап, возврат подтверждается тем же proof.
