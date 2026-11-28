basalt-bench: starting /home/omarchy/build/lapilli-v100/bin/basalt (log: /home/omarchy/bench-A2-logs/engine.log)
basalt-bench: engine: warning: this CPU has no AVX-512: the expert kernels run on AVX-2 (multi-token for the i-quant gate/up rows)
basalt-bench: loading 77.5 GiB
basalt-bench: loading 5.2 / 77.5 GiB (6%)
basalt-bench: loading 10.4 / 77.5 GiB (13%)
basalt-bench: loading 15.7 / 77.5 GiB (20%)
basalt-bench: loading 20.9 / 77.5 GiB (26%)
basalt-bench: loading 26.2 / 77.5 GiB (33%)
basalt-bench: loading 30.6 / 77.5 GiB (39%)
basalt-bench: loading 34.3 / 77.5 GiB (44%)
basalt-bench: loading 37.9 / 77.5 GiB (48%)
basalt-bench: loading 41.4 / 77.5 GiB (53%)
basalt-bench: loading 44.9 / 77.5 GiB (57%)
basalt-bench: loading 48.4 / 77.5 GiB (62%)
basalt-bench: loading 52.1 / 77.5 GiB (67%)
basalt-bench: loading 55.6 / 77.5 GiB (71%)
basalt-bench: loading 59.3 / 77.5 GiB (76%)
basalt-bench: loading 62.8 / 77.5 GiB (81%)
basalt-bench: loading 66.4 / 77.5 GiB (85%)
basalt-bench: loading 70.1 / 77.5 GiB (90%)
basalt-bench: loading 73.9 / 77.5 GiB (95%)
basalt-bench: engine: warning: mid_chain: device not covered (80 SMs, 98304 B optin smem; need 16, 101376): the unfused kernels run
basalt-bench: engine: warning: fallback: GDN qkv + z without dense_tc_pair (types 8 / 8)
basalt-bench: loading weights 77.5 / 77.5 GiB done (190 s)
basalt-bench: engine ready in 194 s
  run 1 conv    68.4 tok/s, 1005 tokens
  run 1 struct  146.7 tok/s, 7230 tokens
  run 1 prose   72.1 tok/s, 1179 tokens
  run 1 pp16384 16676 tokens, 1441 t/s engine, 1422 t/s wall
  run 1 pp32768 33323 tokens, 1466 t/s engine, 1460 t/s wall
  run 1 pp65536 66617 tokens, 1455 t/s engine, 1452 t/s wall
  run 1 pp131072 133205 tokens, 1331 t/s engine, 1329 t/s wall
basalt-bench  build 6f0a1e6bca  power limit 300 W

| test      |  t/s | accept % | draft len |
| --------- | ---: | -------: | --------: |
| pp16384   | 1441 |        - |         - |
| pp32768   | 1466 |        - |         - |
| pp65536   | 1455 |        - |         - |
| pp131072  | 1331 |        - |         - |
| tg conv   |   68 |     68.2 |      2.20 |
| tg struct |  147 |     98.0 |      6.92 |
| tg prose  |   72 |     63.7 |      1.78 |
