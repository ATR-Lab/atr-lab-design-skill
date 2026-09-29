#!/usr/bin/env python3
"""Refresh build/icons-src/prompts.json without ever dropping a record.

generate.py appends one record per Codex call (under a file lock). This script
  (a) reconstructs every planned record, because a prompt is a pure function of (manifest, names,
      mode): the anchor candidates, the sheets-vs-singles test, production sheets A-E and the fix
      rounds generated from the alt manifests in fix/ (see PLAN and FIX_PLAN below);
  (b) unions them with the records already in prompts.json and with every list-form */prompts.json
      under build/icons-src, keyed by (file, tag). Existing records win (they carry the real timing
      and error fields); reconstructed ones only fill gaps. Nothing is ever removed;
  (c) refreshes the embedded "selection" from selection.json and the "exists" flag of every record;
  (d) writes prompts.json.bak before overwriting.

Subjects are reworded over time, so the wording in force when each batch was generated is kept:
ORIGINAL_SUBJECTS (five subjects as they were for sheets A-D and the test batch) and
subjects-at-E.json (every subject as it was for sheet E and before the fix rounds; icons.json now
carries the adopted fix-round wording for the regenerated icons).
"""
import glob
import json
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "atr-lab-design", "scripts", "icons"))
from generate import single_prompt, sheet_prompt, load_manifest  # noqa: E402

MANIFEST = os.path.join(ROOT, "atr-lab-design", "scripts", "icons", "icons.json")
ANCHOR = os.path.join(HERE, "anchor", "anchor.png")
MARK = "$SCRATCH/render/presx/ppt/media/image6.png"
CANON = os.path.join(HERE, "prompts.json")

# subjects as they were when sheets A-D (and the test batch) were generated
ORIGINAL_SUBJECTS = {
    "ai-neural-net": "a neural network diagram: three vertical columns of small hexagonal nodes (two nodes, then three nodes, then two nodes) fully connected between neighbouring columns by straight diagonal lines",
    "digital-twin": "a digital twin: two identical isometric cubes side by side, the left cube drawn as a solid outlined cube and the right cube drawn as a wireframe with its hidden edges visible, joined by a short horizontal double-ended arrow",
    "path-planning": "path planning: a small square start marker at the bottom left and a diamond goal marker at the top right, connected by a dashed route line made of straight segments that turns at right angles around a small square obstacle in the middle",
    "simulation": "a physics simulation: an isometric ground plane drawn as a diamond-shaped wireframe grid of 3 by 3 cells with a small isometric wireframe cube standing on top of it",
    "lidar-sensor": "a lidar sensor: a small octagonal sensor puck on a short vertical stem, emitting three straight scan rays that fan out to the upper right at different angles",
}

PLAN = {
    "A": "telepresence-robot,teleoperation,haptic-glove,quadruped,mobile-rover,lidar-sensor,camera-vision,ai-neural-net,digital-twin",
    "B": "ros-graph,simulation,wireless-link,joystick,flight-simulator,path-planning,human-robot-interaction,safety-shield,embedded-chip",
    "C": "team,k12-outreach,workshop-idea,award,calendar-event,location,website-globe,code,dataset",
    "D": "milestone-flag,partnership,funding,presentation,results-chart,video-demo,teleoperation,digital-twin,partnership",
    "E": "ai-neural-net,digital-twin,path-planning,simulation,lidar-sensor,quadruped,website-globe,partnership,teleoperation",
}
TEST_SHEET = "vr-headset,drone-uav,student,humanoid,email,publication,robotic-arm,mechanical-gear,launch-rocket"
TEST_SINGLES = "vr-headset,drone-uav,student,humanoid,email,publication"

# fix rounds: (alt manifest in fix/, tag, mode, names). Singles are written as fix/<name>-<tag>.png,
# sheets as fix/sheet-01-<tag>.png (generate.py naming).
FIX_SINGLES_1 = "simulation,digital-twin,partnership,ai-neural-net,flight-simulator,funding,wireless-link,dataset"
FIX_SHEET = "simulation,digital-twin,partnership,ai-neural-net,teleoperation,quadruped,path-planning,ros-graph,flight-simulator"
FIX_ROUND3 = "ai-neural-net,simulation,digital-twin,dataset,funding"
FIX_ROUND4 = "ai-neural-net,dataset,joystick,lidar-sensor,haptic-glove,funding,camera-vision"
FIX_PLAN = [
    ("alt-A.json", "fix-v1", "single", FIX_SINGLES_1, "fix round 1: reworded subjects for the thin / ambiguous icons"),
    ("alt-S.json", "S-v1", "sheet3x3", FIX_SHEET, "fix round 1: sheet with heavier wording for the stroke-floor outliers"),
    ("alt-S.json", "S-v2", "sheet3x3", FIX_SHEET, "fix round 1: sheet with heavier wording for the stroke-floor outliers"),
    ("alt-B.json", "fix-v2", "single", FIX_SINGLES_1, "fix round 2: second candidate wording"),
    ("alt-C.json", "fix-v3", "single", FIX_ROUND3, "fix round 3: chunky band / strut phrasing, new metaphors"),
    ("alt-D.json", "fix-v4", "single", FIX_ROUND3, "fix round 3: chunky band / strut phrasing, new metaphors"),
    ("alt-E.json", "fix-v5", "single", FIX_ROUND4, "fixer pass: 2x2 neural net, hollow dataset/joystick/funding/camera, lidar chevrons, glove"),
    ("alt-F.json", "fix-v6", "single", FIX_ROUND4, "fixer pass: second wording of the same subjects"),
]


def with_subjects(m, subjects):
    m = json.loads(json.dumps(m))
    for k, v in subjects.items():
        if k in m["icons"]:
            m["icons"][k]["subject"] = v
    return m


def reconstruct():
    m_now = load_manifest(MANIFEST)
    at_e = os.path.join(HERE, "subjects-at-E.json")
    m_e = with_subjects(m_now, json.load(open(at_e))) if os.path.exists(at_e) else m_now
    m_old = with_subjects(m_e, ORIGINAL_SUBJECTS)
    records = []
    # 1. anchor candidates (prompts saved at generation time)
    anchors = json.load(open(os.path.join(HERE, "anchor", "prompts.json")))
    for name, prompt in anchors.items():
        refs = [MARK] if name == "gripper-d" else []
        records.append({"name": "gripper", "file": f"anchor/{name}.png", "prompt": prompt, "refs": refs, "mode": "single (anchor candidate)", "tag": name, "ok": True,
                        "note": "style anchor candidates; gripper-b chosen as anchor.png"})
    # 2. sheets-vs-singles test (old manifest, anchor reference)
    for n in TEST_SINGLES.split(","):
        records.append({"name": n, "file": f"test-singles/{n}.png", "prompt": single_prompt(m_old, n), "refs": [ANCHOR], "mode": "single", "tag": "test", "ok": True})
    records.append({"name": TEST_SHEET, "file": "test-sheets/sheet-01.png", "prompt": sheet_prompt(m_old, TEST_SHEET.split(","), 3), "refs": [ANCHOR], "mode": "sheet3x3", "tag": "test", "ok": True,
                    "note": "the nine cells of this sheet were selected for the final set"})
    # 3. production sheets
    for s in "ABCD":
        for v in ("v1", "v2"):
            records.append({"name": PLAN[s], "file": f"sheets/sheet-01-{s}-{v}.png", "prompt": sheet_prompt(m_old, PLAN[s].split(","), 3), "refs": [ANCHOR], "mode": "sheet3x3", "tag": f"{s}-{v}", "ok": True})
    for v in ("v1", "v2", "v3"):
        records.append({"name": PLAN["E"], "file": f"sheets/sheet-01-E-{v}.png", "prompt": sheet_prompt(m_e, PLAN["E"].split(","), 3), "refs": [ANCHOR], "mode": "sheet3x3", "tag": f"E-{v}", "ok": True,
                        "note": "regeneration sheet with reworded subjects (no thin lines / dashes)"})
    # 4. fix rounds from the alt manifests
    for alt, tag, mode, names, note in FIX_PLAN:
        path = os.path.join(HERE, "fix", alt)
        if not os.path.exists(path):
            continue
        m_alt = load_manifest(path)
        if mode == "single":
            for n in names.split(","):
                records.append({"name": n, "file": f"fix/{n}-{tag}.png", "prompt": single_prompt(m_alt, n), "refs": [ANCHOR], "mode": "single", "tag": tag, "ok": True, "note": note})
        else:
            records.append({"name": names, "file": f"fix/sheet-01-{tag}.png", "prompt": sheet_prompt(m_alt, names.split(","), 3), "refs": [ANCHOR], "mode": mode, "tag": tag, "ok": True, "note": note})
    return records


def key(r):
    return (r["file"], r.get("tag", ""))


def main():
    canon = json.load(open(CANON)) if os.path.exists(CANON) else {}
    existing = list(canon.get("records", [])) if isinstance(canon, dict) else list(canon)
    merged = {key(r): r for r in existing}
    order = [key(r) for r in existing]
    added = {"list-form": 0, "reconstructed": 0}
    # list-form manifests written by generate.py without --prompts (file paths are relative to that file)
    for path in sorted(glob.glob(os.path.join(HERE, "*", "**", "prompts.json"), recursive=True)):
        try:
            recs = json.load(open(path))
        except json.JSONDecodeError:
            continue
        if not isinstance(recs, list):
            continue
        for r in recs:
            if not isinstance(r, dict) or "file" not in r:
                continue
            r = dict(r)
            r["file"] = os.path.relpath(os.path.join(os.path.dirname(path), r["file"]), HERE)
            if key(r) not in merged:
                merged[key(r)] = r
                order.append(key(r))
                added["list-form"] += 1
    for r in reconstruct():
        if key(r) not in merged:
            merged[key(r)] = r
            order.append(key(r))
            added["reconstructed"] += 1
    records = [merged[k] for k in order]
    assert len(records) >= len(existing), "refusing to drop records"
    for r in records:
        r["exists"] = os.path.exists(os.path.join(HERE, r["file"]))
        if r.get("mode", "").startswith("sheet") and r["file"].endswith(".png"):
            # provenance for sliced cells: <dir>/cells/<name>-<tag>.png (or <name>.png for the untagged test sheet)
            d = os.path.dirname(r["file"])
            tag = r.get("tag", "")
            cells = {}
            for n in r["name"].split(","):
                for cand in ([f"{d}/cells/{n}-{tag}.png"] if tag and tag != "test" else []) + [f"{d}/cells/{n}.png"]:
                    if os.path.exists(os.path.join(HERE, cand)):
                        cells[n] = cand
                        break
            if cells:
                r["cells"] = cells
    m_now = load_manifest(MANIFEST)
    out = {"style_block": m_now["style"], "reference_note": m_now["reference_note"], "anchor": "anchor/anchor.png (= anchor/gripper-b.png)",
           "selection": json.load(open(os.path.join(HERE, "selection.json"))), "records": records}
    if os.path.exists(CANON):
        shutil.copy2(CANON, CANON + ".bak")
    tmp = CANON + ".tmp"
    json.dump(out, open(tmp, "w"), indent=1)
    os.replace(tmp, CANON)
    print(f"{len(existing)} existing records kept; added {added['list-form']} from list-form manifests and "
          f"{added['reconstructed']} reconstructed; {len(records)} total, {sum(r['exists'] for r in records)} files present")


if __name__ == "__main__":
    main()
