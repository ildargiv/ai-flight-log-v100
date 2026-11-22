#!/usr/bin/env python3
"""Context-length sweep for Qwen3.8-Flash-Next UD-Q4_K_XL on lapilli-v100 (V100 sm_70).

Same methodology as ctx_sweep.py: fresh nonce prompts (reused==0), engine timings
for prefill/decode, client TTFT, thinking off, greedy, 256-token cap, >=3 runs/arm.
Standard library only.
"""
import argparse, datetime, json, os, re, statistics, time, urllib.request
from pathlib import Path

BASE = os.environ.get("BENCH_URL", "http://127.0.0.1:8080")
MODEL = os.environ.get("BENCH_MODEL", "Qwen3.8-Flash-Next UD-Q4_K_XL")
LOG = os.environ.get("BENCH_LOG", "/home/omarchy/build/lapilli-v100/lapilli-serve.log")
WORDS = ("alpha beta gamma delta epsilon zeta eta theta iota kappa lambda mu "
         "nu xi omicron pi rho sigma tau upsilon phi chi psi omega").split()

def filler(n):
    return "\n".join("record%06d: " % i + " ".join(WORDS[(i + j) % len(WORDS)] for j in range(8))
                     for i in range(1, n + 1))

def log_pos():
    try: return Path(LOG).stat().st_size
    except OSError: return 0

def log_since(pos, tokens):
    try:
        with open(LOG, "rb") as f:
            f.seek(pos); text = f.read().decode("utf-8", "replace")
    except OSError:
        return None
    for line in reversed(text.splitlines()):
        if str(tokens) in line and ("prompt" in line.lower() or "pp=" in line.lower()):
            return (line[:400], None)
    return None

def request(prompt, cap=256, timeout=3600):
    body = {"model": MODEL, "stream": True, "max_tokens": cap, "temperature": 0,
            "chat_template_kwargs": {"enable_thinking": False},
            "messages": [{"role": "user", "content": prompt}]}
    req = urllib.request.Request(BASE + "/v1/chat/completions", data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    t0 = time.perf_counter(); first = None; usage = timings = None; err = None; text = []
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            for raw in r:
                line = raw.decode("utf-8", "replace").strip()
                if not line.startswith("data:"): continue
                d = line[5:].strip()
                if d == "[DONE]": break
                try: j = json.loads(d)
                except ValueError: continue
                if j.get("error"): err = str(j["error"])[:300]
                for ch in j.get("choices") or []:
                    piece = (ch.get("delta") or {}).get("content") or ""
                    if piece and first is None: first = time.perf_counter() - t0
                    if piece: text.append(piece)
                if j.get("usage"): usage = j["usage"]
                if j.get("timings"): timings = j["timings"]
    except Exception as e:
        err = repr(e)[:300]
    return {"first": first, "total": time.perf_counter() - t0, "usage": usage,
            "timings": timings, "text": "".join(text), "err": err}

def prompt_tokens(r): return (r.get("usage") or {}).get("prompt_tokens")

def calibrate(nonce):
    pts = []
    for words in (200, 800):
        r = request("[cal-%s-%d] %s" % (nonce, words, filler(words)), cap=1)
        pts.append(prompt_tokens(r))
    if not all(pts) or pts[1] <= pts[0]:
        return 15.3, 20.0
    slope = (pts[1] - pts[0]) / 600.0
    return slope, max(0.0, pts[0] - 200 * slope)

def digest(r, target, run, nonce, log_line, cpu_lane):
    u, t = r.get("usage") or {}, r.get("timings") or {}
    cached = (u.get("prompt_tokens_details") or {}).get("cached_tokens")
    if cached is None: cached = t.get("cache_n")
    read = t.get("prompt_n")
    if read is None and u.get("prompt_tokens") is not None and cached is not None:
        read = u["prompt_tokens"] - cached
    gen = u.get("completion_tokens") or 0
    dec = t.get("predicted_per_second")
    if dec is None and r["first"] is not None and gen > 1 and r["total"] > r["first"]:
        dec = round((gen - 1) / (r["total"] - r["first"]), 1)
    return {"arm": str(target), "run": run, "nonce": nonce, "target_tokens": target,
            "ok": r["err"] is None and r["first"] is not None, "err": r["err"],
            "prompt_tokens": u.get("prompt_tokens"), "reused_tokens": cached,
            "read_tokens": read, "generated_tokens": gen,
            "prompt_tps": t.get("prompt_per_second"), "decode_tps": dec,
            "prompt_ms": t.get("prompt_ms"), "decode_ms": t.get("predicted_ms"),
            "ttft_s": None if r["first"] is None else round(r["first"], 3),
            "total_s": round(r["total"], 3),
            "drafts_offered": t.get("draft_n"), "drafts_accepted": t.get("draft_n_accepted"),
            "cpu_lane_pct": cpu_lane, "engine_log_line": log_line}

def stat(rows, key):
    v = [r[key] for r in rows if isinstance(r.get(key), (int, float))]
    if not v: return None
    return {"median": round(statistics.median(v), 2), "min": round(min(v), 2),
            "max": round(max(v), 2), "n": len(v)}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sizes", default="1024,4096,6144")
    ap.add_argument("--runs", type=int, default=4)
    ap.add_argument("--cap", type=int, default=256)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    sizes = [int(x) for x in a.sizes.split(",")]
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    nonce_base = str(int(time.time()))
    slope, overhead = calibrate(nonce_base)
    print("calibrated: %.4f tokens/word, overhead %.1f" % (slope, overhead), flush=True)
    rows = []
    for target in sizes:
        words = max(20, int((target - overhead) / slope))
        for run in range(1, a.runs + 1):
            nonce = "%s-%d-r%d" % (nonce_base, target, run)
            prompt = "[bench %s] %s" % (nonce, filler(words))
            pos = log_pos(); r = request(prompt, cap=a.cap)
            actual = prompt_tokens(r)
            ll, cpu = log_since(pos, actual) if actual else (None, None)
            d = digest(r, target, run, nonce, ll, cpu); rows.append(d)
            print("%6d run%d: actual=%s reused=%s read=%s prefill=%s decode=%s ttft=%s err=%s" %
                  (target, run, d["prompt_tokens"], d["reused_tokens"], d["read_tokens"],
                   d["prompt_tps"], d["decode_tps"], d["ttft_s"], d["err"]), flush=True)
            (out / "results.json").write_text(json.dumps({"meta": {"date": datetime.date.today().isoformat(),
                 "base": BASE, "model": MODEL, "cap": a.cap, "runs": a.runs, "sizes": sizes,
                 "slope": slope, "overhead": overhead}, "rows": rows}, ensure_ascii=False, indent=2), encoding="utf-8")
    summary = {}
    for target in sizes:
        arm = [r for r in rows if r["target_tokens"] == target and r["ok"]]
        summary[str(target)] = {k: stat(arm, k) for k in ("prompt_tokens","reused_tokens","read_tokens",
                                  "generated_tokens","prompt_tps","decode_tps","ttft_s","total_s","cpu_lane_pct")}
    result = {"meta": {"date": datetime.date.today().isoformat(), "base": BASE, "model": MODEL,
             "cap": a.cap, "runs": a.runs, "sizes": sizes, "slope": slope, "overhead": overhead,
             "timings_source": "engine (timings in last SSE chunk)",
             "ttft_source": "client monotonic clock, first non-empty content",
             "thinking": "off (chat_template_kwargs.enable_thinking=false)"},
             "summary": summary, "rows": rows}
    (out / "results.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2), flush=True)

if __name__ == "__main__":
    main()
