#!/usr/bin/env python3
"""atr_design.py - one front door for the ATR Lab design skill's tools.

    python3 scripts/atr_design.py <command> [args...]
    python3 scripts/atr_design.py help              # this list

Commands built in here:
  assets find QUERY [--kind K] [--color C] [--format F] [--limit N] [--json]
                     search assets/index.json (aliases work: telepresence, roundel, kent-state);
                     on a miss it prints "did you mean" suggestions
  assets show ID     one record: every file, pixel size, use, minimum size (ID, path or file name)
  assets path QUERY [--kind K] [--color C] [--format F]
                     print the absolute path of the best match only (for scripts); exit 1 if none
  assets kinds       the asset kinds and counts
  layouts [TEMPLATE] [--layout NAME] [--json]
                     templates, or the layouts of one template, or one layout's fields, budgets and an
                     example spec slide (reads assets/templates/*-layouts.json via new_deck.py)
  doctor [--group G] [--json]
                     check the environment per feature group (core, office, qr, icons, figures, ai-images)
                     and print the exact fix command for each miss; exit 0 only when core passes
  banner ...         on-brand banners, headers and thumbnails (scripts/banner.py; --list-presets)

Commands handed to other modules (loaded only when used, so a missing optional package breaks only
its own command):
  official ...  -> official_assets.py (official Kent State artwork: fetch, verify, cache)
  qr ...        -> qr_code.py       export ... -> export_office.py      project ... -> project.py
  pptx ...      -> pptx_tools.py    flyer ...  -> pptx_tools.py flyer ...
  deck ...      -> new_deck.py      quad ...   -> quad_chart.py         social ... -> social_card.py
  check ...     -> brand_check.py   contrast ... -> contrast.py         signature ... -> email_signature.py
  brand ...     -> atr_brand.py (color, font, logo, icon, pattern lookups)
  index ...     -> asset_index.py (rebuild or --check assets/index.json)

Exit codes: a delegated command returns its module's code. Built-ins: 0 ok; 1 not found or usage
error; 2 doctor: a core check failed; 4 the command's module or one of its packages is missing
(the message names the fix; run `atr_design.py doctor`).
"""
from __future__ import annotations

import argparse
import importlib
import json
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
SKILL_ROOT = HERE.parent

# command -> (module, argv prefix, what it is)
DELEGATES = {
    "banner": ("banner", [], "on-brand banners, headers and thumbnails"),
    "official": ("official_assets", [], "official Kent State artwork: fetch, verify, cache"),
    "qr": ("qr_code", [], "QR codes at an exact physical size, decode and verify"),
    "export": ("export_office", [], "tagged PDF export with the brand fonts, inspect, render"),
    "project": ("project", [], "project manifest: status, build, export, replace-asset"),
    "pptx": ("pptx_tools", [], "PowerPoint helpers: scale, replace pictures, place QR codes"),
    "flyer": ("pptx_tools", ["flyer"], "event and workshop flyers"),
    "deck": ("new_deck", [], "build a deck, poster, flyer or quad from a JSON/YAML spec"),
    "quad": ("quad_chart", [], "quad charts"),
    "social": ("social_card", [], "social tiles from a JSON spec"),
    "check": ("brand_check", [], "brand linter for PPTX, DOCX, PDF, HTML, images"),
    "contrast": ("contrast", [], "WCAG contrast of tokens and colors"),
    "signature": ("email_signature", [], "email signatures"),
    "brand": ("atr_brand", [], "color, font, logo, icon and pattern lookups"),
    "index": ("asset_index", [], "rebuild or check assets/index.json"),
}
EXIT_UNAVAILABLE = 4

# Python import name -> (pip requirement, feature group)
PIP_NAMES = {"PIL": "Pillow>=10.0", "numpy": "numpy>=1.24", "fontTools": "fonttools>=4.40", "pptx": "python-pptx>=1.0",
             "lxml": "lxml>=4.9", "defusedxml": "defusedxml>=0.7", "qrcode": "qrcode[pil]>=7.4",
             "zxingcpp": "zxing-cpp>=2.2", "pypdf": "pypdf>=4.0", "scipy": "scipy>=1.10",
             "skimage": "scikit-image>=0.21", "vtracer": "vtracer>=0.6", "matplotlib": "matplotlib>=3.7",
             "yaml": "PyYAML>=6.0"}


def _pip_fix(module: str) -> str:
    req = PIP_NAMES.get(module, module)
    if sys.prefix == getattr(sys, "base_prefix", sys.prefix):
        return (f"python3 -m venv .venv && .venv/bin/pip install '{req}'   "
                "(or every package: .venv/bin/pip install -r scripts/requirements.txt), then run with .venv/bin/python")
    return f"{sys.executable} -m pip install '{req}'"


def run_delegate(cmd: str, argv: list) -> int:
    """Import the command's module lazily and call its main(argv)."""
    mod_name, prefix, _ = DELEGATES[cmd]
    try:
        mod = importlib.import_module(mod_name)
    except ModuleNotFoundError as exc:
        missing = (exc.name or "").split(".")[0]
        if missing == mod_name:
            print(f"the '{cmd}' command is not available in this copy of the skill (scripts/{mod_name}.py is "
                  "missing). Update the skill, or run `atr_design.py help` for the commands it has.", file=sys.stderr)
        else:
            print(f"the '{cmd}' command needs the Python package '{PIP_NAMES.get(missing, missing)}', which is not "
                  f"installed. Fix: {_pip_fix(missing)}\nCheck everything: python3 scripts/atr_design.py doctor",
                  file=sys.stderr)
        return EXIT_UNAVAILABLE
    except ImportError as exc:
        print(f"the '{cmd}' command could not load: {exc}. Run: python3 scripts/atr_design.py doctor", file=sys.stderr)
        return EXIT_UNAVAILABLE
    except SystemExit as exc:          # modules that exit on a missing dependency at import time
        print(str(exc), file=sys.stderr)
        return EXIT_UNAVAILABLE
    main = getattr(mod, "main", None)
    if main is None:
        print(f"scripts/{mod_name}.py has no main(); it cannot be run through atr_design.py", file=sys.stderr)
        return EXIT_UNAVAILABLE
    try:
        rc = main(prefix + list(argv))
    except SystemExit as exc:          # argparse --help / errors inside the module
        rc = exc.code if isinstance(exc.code, int) else (0 if exc.code is None else 1)
    return int(rc or 0)


# --------------------------------------------------------------------------- assets
def cmd_assets(argv: list) -> int:
    """assets find | show | path | kinds."""
    import asset_index as AI
    ap = argparse.ArgumentParser(prog="atr_design.py assets", description="Search the ATR asset index.")
    ap.add_argument("action", choices=["find", "show", "path", "kinds"])
    ap.add_argument("query", nargs="*")
    ap.add_argument("--kind", help="logo, badge, icon, icon-svg, pattern, background, illustration, template, font ...")
    ap.add_argument("--color", help="variant: navy, gold, white, ink, twotone-reverse ...")
    ap.add_argument("--format", dest="fmt", help="png, svg, pptx ...")
    ap.add_argument("--limit", type=int, default=12)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    q = " ".join(a.query)
    if a.action == "kinds":
        idx = AI.load_index()
        if a.json:
            print(json.dumps({"kinds": idx["kinds"], "counts": idx["counts"]}, indent=1))
        else:
            for k, desc in idx["kinds"].items():
                print(f"{k:<14} {idx['counts'][k]:>4}  {desc}")
        return 0
    if a.action == "show":
        rec = AI.get(q)
        if not rec:
            hits = AI.search(q, limit=1)
            rec = hits[0] if len(hits) == 1 else None
        if not rec:
            print(f"no asset '{q}'. Did you mean: {', '.join(AI.suggest(q)) or 'nothing close'}", file=sys.stderr)
            return 1
        if a.json:
            print(json.dumps(rec, indent=1, ensure_ascii=False))
        else:
            _print_record(rec)
        return 0
    if not q and not a.kind:
        print("give a query, e.g.: assets find telepresence --kind badge", file=sys.stderr)
        return 1
    hits = AI.search(q, kind=a.kind, color=a.color, fmt=a.fmt, limit=None)
    corrected = None
    if not hits:
        sugg = AI.suggest(q)
        # retry with the closest spelling when it is unambiguous enough to be useful
        for s in sugg:
            alt = AI.search(s.split("/", 1)[-1].replace("-", " "), kind=a.kind, color=a.color, fmt=a.fmt, limit=None)
            if alt:
                hits, corrected = alt, s
                break
        if not hits:
            print(f"nothing matches '{q}'" + (f" (kind {a.kind})" if a.kind else "")
                  + f". Did you mean: {', '.join(sugg) or 'nothing close'}?\n"
                  "Try fewer words, or list a kind: atr_design.py assets find --kind badge", file=sys.stderr)
            return 1
        print(f"nothing matches '{q}'; showing results for '{corrected}'", file=sys.stderr)
    if a.action == "path":
        print(SKILL_ROOT / hits[0]["path"])
        return 0
    shown = hits[:a.limit] if a.limit else hits
    if a.json:
        print(json.dumps([AI.brief(h) for h in shown], indent=1, ensure_ascii=False))
    else:
        for h in shown:
            px = "x".join(str(v) for v in h["px"]) if h.get("px") else ""
            print(f"{h['id']:<44} {px:>10}  {h['path']}")
            print(f"{'':<44} {'':>10}  {h['use_for'][:110]}")
        if len(hits) > len(shown):
            print(f"... {len(hits) - len(shown)} more (--limit 0 for all)")
    return 0


def _print_record(rec: dict):
    print(f"{rec['id']}  ({rec['kind']})")
    for k in ("name", "variant", "path", "px", "size_in", "formats", "use_for", "placement", "aliases", "keywords",
              "min_px", "min_dimension", "min_print_in", "clear_space_x_over_height", "aspect_w_over_h", "backgrounds",
              "roles", "note"):
        if rec.get(k) not in (None, "", []):
            v = rec[k]
            if isinstance(v, list):
                v = ", ".join(str(x) for x in v)
            print(f"  {k:<26} {v}")
    print("  files:")
    for f in rec["files"]:
        px = "x".join(str(v) for v in f["px"]) if f.get("px") else ""
        print(f"    {f['path']}  {f['format']}  {px}")


# --------------------------------------------------------------------------- layouts
def _example_value(field: dict):
    kind = field["kind"]
    if kind == "pic":
        return "assets/illustrations/illus-telepresence.png"
    if kind == "chart":
        return {"type": "bar", "categories": ["A", "B"], "series": [{"name": "Value", "values": [1, 2]}],
                "alt": "What the chart shows"}
    if kind == "tbl":
        return {"header": ["Column", "Column"], "rows": [["Cell", "Cell"]]}
    if kind == "media":
        return "demo.mp4"
    prompt = (field.get("_prompt") or "").strip()
    if prompt and len(prompt) <= 80 and "\n" not in prompt:
        return prompt if "[" in prompt else f"[{prompt}]"
    if "para" in field.get("budget", ""):
        return [f"[{field['field']} point]", f"[{field['field']} point]"]
    budget = field.get("budget", "-")
    return f"[{field['field']}" + (f": {budget}]" if budget and budget != "-" else "]")


def layout_data(template: str) -> dict:
    """Layouts of a template as a dict (name, purpose, when, fields with budgets, showcase slides)."""
    import new_deck as ND
    tpl = ND.Template(template)
    out = {"template": template, "file": str(Path(tpl.path).relative_to(SKILL_ROOT)) if str(tpl.path).startswith(
        str(SKILL_ROOT)) else str(tpl.path),
           "layouts_json": str(Path(tpl.spec_path).relative_to(SKILL_ROOT)) if tpl.spec_path else None,
           "slide_in": [round(tpl.slide_w, 3), round(tpl.slide_h, 3)], "layouts": [], "showcase_slides": []}
    for i, layout in enumerate(tpl.prs.slide_layouts):
        jl = tpl.json_layout(layout) or {}
        entry = {"index": i, "name": layout.name, "purpose": jl.get("purpose", ""), "when": jl.get("when", ""),
                 "fields": []}
        for s in tpl.slots(layout):
            f = {"field": s.name, "kind": s.kind, "budget": s.budget_str()}
            about = (s.meta.get("purpose") or s.meta.get("prompt") or "").strip()
            if about:
                f["about"] = about[:200]
            f["_prompt"] = s.meta.get("prompt") or ""
            entry["fields"].append(f)
        out["layouts"].append(entry)
    for n, slide in enumerate(tpl.prs.slides, 1):
        out["showcase_slides"].append({"from_slide": n, "layout": slide.slide_layout.name,
                                       "named_shapes": [sh.name for sh in slide.shapes if not sh.is_placeholder]})
    return out


def _match_layout(name: str, layouts: list) -> tuple:
    import difflib
    names = [L["name"] for L in layouts]
    low = name.strip().lower()
    for L in layouts:
        if L["name"].lower() in (low, "atr - " + low) or str(L["index"]) == low:
            return L, []
    sub = [L for L in layouts if low in L["name"].lower()]
    if len(sub) == 1:
        return sub[0], []
    cands = [L["name"] for L in sub] or difflib.get_close_matches(name, names, n=4, cutoff=0.3)
    return None, cands


def cmd_layouts(argv: list) -> int:
    """layouts [TEMPLATE] [--layout NAME] [--json]."""
    ap = argparse.ArgumentParser(prog="atr_design.py layouts",
                                 description="Fields, budgets and an example for the template layouts.")
    ap.add_argument("template", nargs="?", help="presentation, quad, flyer, poster-48x36, social-square ... or a .pptx")
    ap.add_argument("--layout", help="one layout (name, part of a name, or index)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    try:
        import new_deck as ND
    except ImportError as exc:
        missing = getattr(exc, "name", "") or "pptx"
        print(f"layouts needs {PIP_NAMES.get(missing, missing)}: {_pip_fix(missing)}", file=sys.stderr)
        return EXIT_UNAVAILABLE
    except SystemExit:                  # new_deck prints its own install hint and exits
        return EXIT_UNAVAILABLE
    if not a.template:
        rows = sorted(ND.TEMPLATE_ALIASES.items())
        if a.json:
            print(json.dumps({k: f"assets/templates/{v}" for k, v in rows}, indent=1))
        else:
            for k, v in rows:
                print(f"  {k:<20} assets/templates/{v}")
            print("\nNext: atr_design.py layouts <template> [--layout NAME] [--json]")
        return 0
    try:
        data = layout_data(a.template)
    except Exception as exc:  # SpecError and friends from new_deck
        print(f"cannot read template '{a.template}': {exc}", file=sys.stderr)
        return 1
    if a.layout:
        L, cands = _match_layout(a.layout, data["layouts"])
        if L is None:
            print(f"no single layout matches '{a.layout}' in {data['file']}"
                  + (f"; candidates: {'; '.join(cands)}" if cands else "")
                  + f". Layouts: {'; '.join(x['name'] for x in data['layouts'])}", file=sys.stderr)
            return 1
        example = {"template": a.template, "slides": [
            {"layout": L["name"], "fields": {f["field"]: _example_value(f) for f in L["fields"]}}]}
        for f in L["fields"]:
            if f["kind"] == "pic":
                example["slides"][0]["fields"][f["field"] + "_alt"] = "What the picture shows"
        out = {"template": a.template, "file": data["file"], "slide_in": data["slide_in"], "layout": L["name"],
               "index": L["index"], "purpose": L["purpose"], "when": L["when"],
               "fields": [{k: v for k, v in f.items() if not k.startswith("_")} for f in L["fields"]],
               "showcase_slides": [s for s in data["showcase_slides"] if s["layout"] == L["name"]],
               "example": example}
        if a.json:
            print(json.dumps(out, indent=1, ensure_ascii=False))
        else:
            print(f"{L['name']}  ({data['file']}, {data['slide_in'][0]:g} x {data['slide_in'][1]:g} in)")
            for k in ("purpose", "when"):
                if L[k]:
                    print(f"  {k}: {L[k]}")
            for f in L["fields"]:
                print(f"  {f['field']:<18} {f['kind']:<6} {f['budget']:<28} {(f.get('about') or '')[:80]}")
            for s in out["showcase_slides"]:
                print(f"  showcase slide {s['from_slide']} (clone with \"from_slide\"): "
                      + ", ".join(s["named_shapes"][:10]))
            print("\nexample spec:\n" + json.dumps(example, indent=1, ensure_ascii=False))
        return 0
    for L in data["layouts"]:
        L["fields"] = [{k: v for k, v in f.items() if not k.startswith("_")} for f in L["fields"]]
    if a.json:
        print(json.dumps(data, indent=1, ensure_ascii=False))
    else:
        print(f"{data['file']}  ({data['slide_in'][0]:g} x {data['slide_in'][1]:g} in)  "
              f"field names from: {data['layouts_json'] or 'placeholder introspection'}")
        for L in data["layouts"]:
            print(f"  [{L['index']}] {L['name']}: " + ", ".join(f["field"] for f in L["fields"]))
        print("\nOne layout in full: atr_design.py layouts " + a.template + " --layout \"<name>\" [--json]")
    return 0


# --------------------------------------------------------------------------- doctor
def _cache_dir() -> Path:
    return Path(os.environ.get("ATR_DESIGN_CACHE") or Path.home() / ".cache" / "atr-lab-design").expanduser()


def _sys_fix(tool: str) -> str:
    mac = platform.system() == "Darwin"
    fixes = {
        "soffice": ("brew install --cask libreoffice", "sudo apt-get install -y libreoffice-impress libreoffice-writer"),
        "pdftoppm": ("brew install poppler", "sudo apt-get install -y poppler-utils"),
        "pdffonts": ("brew install poppler", "sudo apt-get install -y poppler-utils"),
        "rsvg-convert": ("brew install librsvg", "sudo apt-get install -y librsvg2-bin"),
        "codex": ("npm install -g @openai/codex && codex login", "npm install -g @openai/codex && codex login"),
    }
    m, l = fixes.get(tool, (f"install {tool}", f"install {tool}"))
    return m if mac else l


def _find_soffice() -> Optional[str]:
    env = os.environ.get("SOFFICE")
    if env and os.access(env, os.X_OK):
        return env
    for c in ("soffice", "libreoffice"):
        p = shutil.which(c)
        if p:
            return p
    for p in ("/Applications/LibreOffice.app/Contents/MacOS/soffice",
              str(Path.home() / "Applications/LibreOffice.app/Contents/MacOS/soffice"),
              "/usr/lib/libreoffice/program/soffice", "/opt/libreoffice/program/soffice"):
        if os.access(p, os.X_OK):
            return p
    return None


def _check_module(name: str, min_version: Optional[str] = None) -> tuple:
    try:
        mod = importlib.import_module(name)
    except Exception as exc:
        return False, f"not importable ({type(exc).__name__})"
    ver = getattr(mod, "__version__", None) or getattr(mod, "VERSION", None) or ""
    if name == "PIL":
        from PIL import __version__ as ver  # noqa: F811
    if min_version and ver:
        def tup(v):
            return tuple(int(x) for x in str(v).split(".")[:2] if x.isdigit())
        if tup(ver) < tup(min_version):
            return False, f"version {ver} is older than {min_version}"
    return True, f"{ver}".strip() or "ok"


GROUPS = ["core", "office", "qr", "icons", "figures", "ai-images"]


def doctor_checks(groups: Optional[list] = None) -> list:
    """Run the environment checks; returns [{group, check, ok, detail, fix, required}]."""
    out = []

    def add(group, check, ok, detail, fix="", required=True):
        out.append({"group": group, "check": check, "ok": bool(ok), "detail": detail, "fix": "" if ok else fix,
                    "required": required})
    want = set(groups or GROUPS)
    if "core" in want:
        v = sys.version_info
        add("core", "python >= 3.9", v >= (3, 9), f"{v.major}.{v.minor}.{v.micro} ({sys.executable})",
            "install Python 3.9 or newer (brew install python@3.12) and create a venv with it")
        for mod, minv in (("PIL", "10.0"), ("numpy", "1.24")):
            ok, det = _check_module(mod, minv)
            add("core", PIP_NAMES[mod].split(">")[0], ok, det, _pip_fix(mod))
        ok, det = _check_module("fontTools")
        add("core", "fonttools (kerning, optional)", ok, det, _pip_fix("fontTools"), required=False)
        from asset_index import FONT_ROLES
        fonts_dir = SKILL_ROOT / "assets" / "fonts"
        missing = [r for r, f in FONT_ROLES.items() if not (fonts_dir / f).exists()]
        add("core", "brand fonts (assets/fonts)", not missing,
            f"{len(FONT_ROLES) - len(missing)}/{len(FONT_ROLES)} roles" + (f"; missing {', '.join(missing)}" if missing else ""),
            "restore assets/fonts from the skill repository (git checkout -- atr-lab-design/assets/fonts)")
        tok = SKILL_ROOT / "assets" / "tokens" / "colors.json"
        try:
            json.loads(tok.read_text(encoding="utf-8"))
            add("core", "color tokens", True, "assets/tokens/colors.json")
        except (OSError, ValueError) as exc:
            add("core", "color tokens", False, str(exc), "restore assets/tokens/colors.json from the repository")
        idx = SKILL_ROOT / "assets" / "index.json"
        try:
            import PIL  # noqa: F401  (pixel sizes in the index need Pillow)
            can_build = True
        except ImportError:
            can_build = False
        if idx.exists() and not can_build:
            add("core", "asset index", True, "assets/index.json present (freshness needs Pillow to check)",
                required=False)
        elif idx.exists():
            try:
                import asset_index as AI
                fresh = AI.dumps(AI.build_index()) == idx.read_text(encoding="utf-8")
                add("core", "asset index", True if fresh else False,
                    "assets/index.json is current" if fresh else "assets/index.json is stale (assets changed)",
                    "python3 scripts/asset_index.py", required=False)
            except Exception as exc:  # pragma: no cover
                add("core", "asset index", False, str(exc), "python3 scripts/asset_index.py", required=False)
        else:
            add("core", "asset index", False, "assets/index.json is missing", "python3 scripts/asset_index.py",
                required=False)
        cache = _cache_dir()
        try:
            cache.mkdir(parents=True, exist_ok=True)
            probe = cache / ".write-test"
            probe.write_text("ok")
            probe.unlink()
            add("core", "cache dir writable", True, str(cache))
        except OSError as exc:
            add("core", "cache dir writable", False, f"{cache}: {exc}",
                f"export ATR_DESIGN_CACHE=/a/writable/folder   (or: mkdir -p {cache} && chmod u+w {cache})")
    if "office" in want:
        for mod, minv in (("pptx", "1.0"), ("lxml", "4.9"), ("defusedxml", None)):
            ok, det = _check_module(mod, minv)
            add("office", PIP_NAMES[mod].split(">")[0], ok, det, _pip_fix(mod))
        so = _find_soffice()
        add("office", "LibreOffice (soffice)", so, so or "not found", _sys_fix("soffice"))
        for t in ("pdftoppm", "pdffonts"):
            p = shutil.which(t)
            add("office", t, p, p or "not found", _sys_fix(t))
        ok, det = _check_module("yaml")
        add("office", "PyYAML (YAML specs, optional)", ok, det, _pip_fix("yaml"), required=False)
    if "qr" in want:
        for mod in ("qrcode", "zxingcpp", "pypdf"):
            ok, det = _check_module(mod)
            add("qr", PIP_NAMES[mod].split(">")[0].split("[")[0], ok, det, _pip_fix(mod))
        p = shutil.which("pdftoppm")
        add("qr", "pdftoppm (verify QR codes in PDFs)", p, p or "not found", _sys_fix("pdftoppm"))
    if "icons" in want:
        for mod in ("scipy", "skimage", "vtracer"):
            ok, det = _check_module(mod)
            add("icons", PIP_NAMES[mod].split(">")[0], ok, det, _pip_fix(mod))
        p = shutil.which("rsvg-convert")
        add("icons", "rsvg-convert (SVG to PNG)", p, p or "not found", _sys_fix("rsvg-convert"), required=False)
    if "figures" in want:
        ok, det = _check_module("matplotlib", "3.7")
        add("figures", "matplotlib", ok, det, _pip_fix("matplotlib"))
    if "ai-images" in want:
        codex = os.environ.get("CODEX_BIN") or shutil.which("codex")
        add("ai-images", "Codex CLI", codex, codex or "not found", _sys_fix("codex"))
        if codex:
            try:
                r = subprocess.run([codex, "login", "status"], capture_output=True, text=True, timeout=20)
                msg = (r.stdout + r.stderr).strip().splitlines()
                add("ai-images", "codex logged in", r.returncode == 0, msg[0] if msg else f"exit {r.returncode}",
                    "codex login")
            except (OSError, subprocess.TimeoutExpired) as exc:
                add("ai-images", "codex logged in", False, f"codex login status failed: {exc}", "codex login")
    return out


def cmd_doctor(argv: list) -> int:
    """doctor [--group G] [--json]; exit 0 only when every required core check passes."""
    ap = argparse.ArgumentParser(prog="atr_design.py doctor", description="Check the environment per feature group.")
    ap.add_argument("--group", action="append", choices=GROUPS, help="only this group (repeatable); core always runs")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    groups = sorted(set((a.group or GROUPS) + ["core"]), key=GROUPS.index)
    checks = doctor_checks(groups)
    core_ok = all(c["ok"] for c in checks if c["group"] == "core" and c["required"])
    if a.json:
        summary = {g: all(c["ok"] for c in checks if c["group"] == g and c["required"]) for g in groups}
        print(json.dumps({"core_ok": core_ok, "groups": summary, "checks": checks}, indent=1))
        return 0 if core_ok else 2
    for g in groups:
        rows = [c for c in checks if c["group"] == g]
        good = all(c["ok"] for c in rows if c["required"])
        print(f"[{'ok' if good else 'MISSING'}] {g}")
        for c in rows:
            mark = "ok  " if c["ok"] else ("MISS" if c["required"] else "warn")
            print(f"   {mark} {c['check']:<34} {c['detail']}")
            if not c["ok"]:
                print(f"        fix: {c['fix']}")
    print("\ncore " + ("passes: the skill's core scripts will run." if core_ok else
                       "FAILS: fix the lines marked MISS above first."))
    return 0 if core_ok else 2


# --------------------------------------------------------------------------- main
BUILTINS = {"assets": cmd_assets, "layouts": cmd_layouts, "doctor": cmd_doctor}


def main(argv=None) -> int:
    """Dispatch `atr_design.py <command> ...`."""
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv or argv[0] in ("help", "-h", "--help"):
        print(__doc__)
        return 0
    cmd, rest = argv[0], argv[1:]
    if cmd in BUILTINS:
        try:
            return BUILTINS[cmd](rest)
        except SystemExit as exc:
            return exc.code if isinstance(exc.code, int) else (0 if exc.code is None else 1)
    if cmd in DELEGATES:
        return run_delegate(cmd, rest)
    import difflib
    close = difflib.get_close_matches(cmd, list(BUILTINS) + list(DELEGATES), n=3, cutoff=0.5)
    print(f"unknown command '{cmd}'" + (f"; did you mean {', '.join(close)}?" if close else "")
          + " Run: python3 scripts/atr_design.py help", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
