#!/usr/bin/env python3
"""Run build/tools/codex_image.sh for named prompts from prompts.json, N at a time.

Usage:
  generate.py [--jobs 5] [--suffix _v2] name1 name2 ...   (names as in prompts.json "images")
  generate.py --all
Output: build/illustrations-src/raw/<name><suffix>.png ; per-image log in logs/.
The {STYLE} placeholder in each prompt is replaced with the shared _style_anchor text,
so the exact prompt sent is what the README manifest prints (prompt + anchor).
"""
import json, subprocess, sys, os, time
from concurrent.futures import ThreadPoolExecutor

ROOT = "/Users/marcodotio/Developer/atr-lab-design-skill"
SRC = f"{ROOT}/build/illustrations-src"
TOOL = f"{ROOT}/build/tools/codex_image.sh"

args = sys.argv[1:]
jobs = 5; suffix = ""; names = []
i = 0
while i < len(args):
    if args[i] == "--jobs": jobs = int(args[i+1]); i += 2
    elif args[i] == "--suffix": suffix = args[i+1]; i += 2
    elif args[i] == "--all": names = None; i += 1
    else: names.append(args[i]); i += 1

spec = json.load(open(f"{SRC}/prompts.json"))
style = spec["_style_anchor"]
images = spec["images"]
if names is None: names = list(images)

def run(name):
    p = images[name]["prompt"].replace("{STYLE}", style)
    out = f"{SRC}/raw/{name}{suffix}.png"
    # optional style-reference images ("refs": paths relative to build/illustrations-src/)
    refs = [os.path.join(SRC, r) for r in images[name].get("refs", [])]
    t = time.time()
    with open(f"{SRC}/logs/{name}{suffix}.log", "w") as log:
        r = subprocess.run([TOOL, out, p] + refs, stdout=log, stderr=subprocess.STDOUT)
    ok = r.returncode == 0 and os.path.exists(out)
    print(f"{'OK ' if ok else 'FAIL'} {name}{suffix} {time.time()-t:.0f}s", flush=True)
    return ok

with ThreadPoolExecutor(max_workers=jobs) as ex:
    results = list(ex.map(run, names))
print("done:", sum(results), "/", len(names), flush=True)
