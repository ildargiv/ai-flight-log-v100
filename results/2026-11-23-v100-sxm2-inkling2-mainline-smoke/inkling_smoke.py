import json, time, urllib.request, hashlib, os, random, string
BASE="http://127.0.0.1:8081/v1/chat/completions"
MODEL="inkling-2-mini-ud-iq1s-mainline"
OUT="/home/omarchy/build/inkling-smoke-results.json"
ARMS=[1024,4096,16384]
RUNS=3
MAX_TOKENS=128

def make_prompt(target_tokens, nonce):
    # rough approx: 1 token ~ 4 chars; use deterministic filler
    words=("alpha beta gamma delta epsilon zeta eta theta iota kappa lambda mu nu xi omicron pi rho sigma tau upsilon phi chi psi omega " * 40).split()
    prefix=f"[bench {nonce}] record000001: "
    # build by repeating records
    recs=[]
    i=1
    while True:
        rec=f"record{i:06d}: {' '.join(random.Random(i).choices(words,k=16))}. "
        recs.append(rec)
        text=prefix+"".join(recs)
        # estimate tokens
        if len(text)/4 >= target_tokens: break
        i+=1
    return text

random.seed(42)
results=[]
# warmup
try:
    body=json.dumps({"model":MODEL,"messages":[{"role":"user","content":"Say OK"}],"max_tokens":8,"temperature":0}).encode()
    req=urllib.request.Request(BASE,data=body,headers={"Content-Type":"application/json"})
    urllib.request.urlopen(req,timeout=120).read()
    print("warmup ok")
except Exception as e:
    print("warmup err",e)

for target in ARMS:
    for run in range(1,RUNS+1):
        nonce=''.join(random.choices(string.ascii_lowercase+string.digits,k=12))
        prompt=make_prompt(target,nonce)
        body=json.dumps({"model":MODEL,"messages":[{"role":"user","content":prompt}],"max_tokens":MAX_TOKENS,"temperature":0,"stream":False}).encode()
        req=urllib.request.Request(BASE,data=body,headers={"Content-Type":"application/json"})
        t0=time.time()
        err=None; data=None; ttft=None
        try:
            resp=urllib.request.urlopen(req,timeout=600).read().decode()
            t1=time.time()
            data=json.loads(resp)
        except Exception as e:
            t1=time.time(); err=str(e)
        rec={"target_tokens":target,"run":run,"nonce":nonce,"prompt_chars":len(prompt),"wall_s":t1-t0,"error":err}
        if data:
            usage=data.get("usage",{})
            timings=data.get("timings",{})
            rec.update({
                "prompt_tokens":usage.get("prompt_tokens"),
                "completion_tokens":usage.get("completion_tokens"),
                "cached_tokens":(usage.get("prompt_tokens_details") or {}).get("cached_tokens"),
                "prompt_per_second":timings.get("prompt_per_second"),
                "predicted_per_second":timings.get("predicted_per_second"),
                "prompt_ms":timings.get("prompt_ms"),
                "predicted_ms":timings.get("predicted_ms"),
                "finish_reason":(data.get("choices") or [{}])[0].get("finish_reason"),
            })
        results.append(rec)
        print(json.dumps({"target":target,"run":run,"err":err,"pt":rec.get("prompt_tokens"),"pp_s":rec.get("prompt_per_second"),"tg_s":rec.get("predicted_per_second")}), flush=True)
with open(OUT,"w") as f: json.dump({"model":MODEL,"base":BASE,"arms":ARMS,"runs":RUNS,"max_tokens":MAX_TOKENS,"results":results},f,indent=2)
print("saved",OUT)
