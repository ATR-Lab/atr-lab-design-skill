#!/usr/bin/env python3
"""generate.py - drive Codex image generation for the ATR icon set (singles or sheets).

Usage:
  generate.py --out RAW_DIR [--names a,b,c | --group robotics | --all] [--ref ANCHOR.png ... | --no-ref]
              [--jobs 6] [--tag v2] [--sheet 3] [--manifest icons.json] [--prompts prompts.json]
              [--codex ../codex_image.sh] [--dry-run]

Defaults are resolved relative to this file, so it runs from any working directory: --ref is the style
anchor shipped next to it (scripts/icons/anchor.png, the chevron gripper every icon was matched to),
--codex is scripts/codex_image.sh and --manifest is scripts/icons/icons.json.

Each icon prompt = "Icon subject: <subject>. <style block> <reference note>" from icons.json (the
reference note is left out with --no-ref).
--sheet N asks for one N x N grid of icons per call (slice it with slice_sheet.py). Singles are the
CLI default; 3x3 sheets (--sheet 3) gave the more consistent results, see README.md.
Every call is appended to --prompts as {"name","file","prompt","refs","mode","tag","ok","seconds","time"}
so the set is reproducible. In the ATR build repo the canonical manifest is build/icons-src/prompts.json
(a dict with a "records" list; pass --prompts build/icons-src/prompts.json); it is append-only
(build/icons-src/rebuild_prompts.py never drops records). A plain JSON list also works; the default is
<out>/prompts.json.
"""
import argparse
import json
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    import fcntl  # POSIX: lock the prompts manifest across parallel generate.py runs
except ImportError:  # pragma: no cover (Windows: one run at a time is safe; records are appended in-process)
    fcntl = None

HERE = os.path.dirname(os.path.abspath(__file__))
ANCHOR = os.path.join(HERE, "anchor.png")                       # style anchor (= build/icons-src/anchor/anchor.png)
CODEX = os.path.abspath(os.path.join(HERE, "..", "codex_image.sh"))  # scripts/codex_image.sh


def load_manifest(path):
    with open(path) as f:
        return json.load(f)


def single_prompt(m, name, with_ref=True):
    ic = m["icons"][name]
    return f"Icon subject: {ic['subject']}. {m['style']}" + (f" {m['reference_note']}" if with_ref else "")


def sheet_prompt(m, names, n, with_ref=True):
    rows = []
    for r in range(n):
        chunk = names[r * n:(r + 1) * n]
        cells = "; ".join(f"cell {r * n + i + 1}: {m['icons'][nm]['subject']}" for i, nm in enumerate(chunk))
        rows.append(f"Row {r + 1} (left to right): {cells}.")
    grid = " ".join(rows)
    return (f"A {n} by {n} grid of {len(names)} separate, unrelated icons on ONE square canvas, evenly spaced "
            f"in equal invisible cells with wide empty green gutters between the icons, each icon centered in "
            f"its own cell and not touching its neighbours, no dividing lines, no cell borders. {grid} "
            f"{m['style'].replace('a single flat geometric monoline pictogram', 'every icon is a flat geometric monoline pictogram').replace('The subject is centered on a square canvas with about 12 percent empty green margin on every side.', 'Every icon is the same optical size and the same stroke thickness.')} "
            + (f"{m['reference_note']}" if with_ref else "")).rstrip()


def run_one(codex, out, prompt, refs):
    t0 = time.time()
    cmd = [codex, out, prompt] + list(refs)
    p = subprocess.run(cmd, capture_output=True, text=True)
    ok = p.returncode == 0 and os.path.exists(out) and os.path.getsize(out) > 0
    return ok, time.time() - t0, (p.stderr or "")[-400:]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", required=True)
    ap.add_argument("--ref", action="append", default=None,
                    help="reference image(s); repeatable (default: the style anchor scripts/icons/anchor.png)")
    ap.add_argument("--no-ref", action="store_true", help="generate without a reference image")
    ap.add_argument("--names", default="")
    ap.add_argument("--group", default="")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--jobs", type=int, default=6)
    ap.add_argument("--tag", default="", help="suffix for output file names, e.g. v2 -> name-v2.png")
    ap.add_argument("--sheet", type=int, default=0, help="N: generate N x N sheets instead of singles")
    ap.add_argument("--manifest", default=os.path.join(HERE, "icons.json"))
    ap.add_argument("--prompts", default=None, help="prompts manifest to append to (default OUT/prompts.json; "
                    "in the ATR build repo pass build/icons-src/prompts.json)")
    ap.add_argument("--codex", default=CODEX, help="path to codex_image.sh (default: ../codex_image.sh next to "
                    "this folder, i.e. scripts/codex_image.sh)")
    ap.add_argument("--skip-existing", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    m = load_manifest(a.manifest)
    if a.all:
        names = list(m["icons"].keys())
    elif a.group:
        names = m["groups"][a.group]
    else:
        names = [n for n in a.names.split(",") if n]
    missing = [n for n in names if n not in m["icons"]]
    if missing:
        sys.exit(f"unknown icon names: {missing}")
    codex = a.codex
    refs = [] if a.no_ref else (a.ref or [ANCHOR])
    for r in refs:
        if not os.path.isfile(r):
            sys.exit(f"reference image not found: {r}")
    if not a.dry_run and not os.path.isfile(codex):
        sys.exit(f"codex_image.sh not found: {codex} (pass --codex)")
    os.makedirs(a.out, exist_ok=True)
    prompts_path = a.prompts or os.path.join(a.out, "prompts.json")
    tag = f"-{a.tag}" if a.tag else ""

    def append_record(rec):
        """Append under an exclusive lock and re-read first, so parallel generate.py runs never clobber each other."""
        lock_path = prompts_path + ".lock"
        with open(lock_path, "w") as lk:
            if fcntl:
                fcntl.flock(lk, fcntl.LOCK_EX)
            try:
                log = json.load(open(prompts_path)) if os.path.exists(prompts_path) else []
            except json.JSONDecodeError:
                log = []
            if isinstance(log, dict):
                # canonical manifest ({style_block, reference_note, anchor, selection, records})
                log.setdefault("records", []).append(rec)
            else:
                log.append(rec)
            tmp = prompts_path + ".tmp"
            json.dump(log, open(tmp, "w"), indent=1)
            os.replace(tmp, prompts_path)
            if fcntl:
                fcntl.flock(lk, fcntl.LOCK_UN)

    jobs = []
    if a.sheet:
        n = a.sheet
        for i in range(0, len(names), n * n):
            chunk = names[i:i + n * n]
            fname = f"sheet-{i // (n * n) + 1:02d}{tag}.png"
            jobs.append({"name": ",".join(chunk), "file": os.path.join(a.out, fname), "prompt": sheet_prompt(m, chunk, n, bool(refs)), "mode": f"sheet{n}x{n}"})
    else:
        for nm in names:
            jobs.append({"name": nm, "file": os.path.join(a.out, f"{nm}{tag}.png"), "prompt": single_prompt(m, nm, bool(refs)), "mode": "single"})
    if a.skip_existing:
        jobs = [j for j in jobs if not os.path.exists(j["file"])]
    if a.dry_run:
        for j in jobs:
            print(j["file"]); print("  " + j["prompt"][:200] + "...")
        return
    print(f"{len(jobs)} generation(s), {a.jobs} concurrent, refs={refs}", flush=True)
    with ThreadPoolExecutor(max_workers=a.jobs) as ex:
        futs = {ex.submit(run_one, codex, j["file"], j["prompt"], refs): j for j in jobs}
        for f in as_completed(futs):
            j = futs[f]
            ok, secs, err = f.result()
            rec = {"name": j["name"], "file": os.path.relpath(j["file"], os.path.dirname(prompts_path)), "prompt": j["prompt"],
                   "refs": [os.path.abspath(r) for r in refs], "mode": j["mode"], "tag": a.tag, "ok": ok,
                   "seconds": round(secs), "time": time.strftime("%Y-%m-%dT%H:%M:%S")}
            if not ok:
                rec["error"] = err
            append_record(rec)
            print(("ok   " if ok else "FAIL ") + f"{j['name']}  {secs:.0f}s", flush=True)


if __name__ == "__main__":
    main()
