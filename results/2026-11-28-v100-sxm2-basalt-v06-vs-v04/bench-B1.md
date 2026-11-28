basalt-bench: starting /home/omarchy/build/lapilli-v100/bin/basalt.v0.4.backup (log: /home/omarchy/bench-B1-logs/engine.log)
basalt-bench: engine: warning: this CPU has no AVX-512: the expert kernels run on AVX-2 (multi-token for the i-quant gate/up rows)
basalt-bench: engine: warning: mid_chain: device not covered (80 SMs, 98304 B optin smem; need 16, 101376): the unfused kernels run
basalt-bench: engine: warning: fallback: GDN qkv + z without dense_tc_pair (types 8 / 8)
basalt-bench: engine ready in 184 s
  run 1 conv    67.1 tok/s, 1009 tokens
  run 1 struct  145.4 tok/s, 7230 tokens
  run 1 prose   72.5 tok/s, 1086 tokens
  run 1 pp16384 16676 tokens, 1434 t/s engine, 1412 t/s wall
  run 1 pp32768 33323 tokens, 1472 t/s engine, 1466 t/s wall
  run 1 pp65536 66617 tokens, 1459 t/s engine, 1456 t/s wall
  run 1 pp131072 133205 tokens, 1332 t/s engine, 1330 t/s wall
basalt-bench  build 6f0a1e6bca  power limit 300 W

| test      |  t/s | accept % | draft len |
| --------- | ---: | -------: | --------: |
| pp16384   | 1434 |        - |         - |
| pp32768   | 1472 |        - |         - |
| pp65536   | 1459 |        - |         - |
| pp131072  | 1332 |        - |         - |
| tg conv   |   67 |     67.5 |      2.00 |
| tg struct |  145 |     97.7 |      6.92 |
| tg prose  |   72 |     65.3 |      1.83 |
