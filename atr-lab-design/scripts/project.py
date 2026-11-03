#!/usr/bin/env python3
"""project.py - keep a set of ATR deliverables (flyer, poster, slides) in step with one project manifest.

A project manifest (project.json) holds the event facts once, the assets the artifacts use, and the artifacts
themselves (each a new_deck.py spec with {{facts.x}} placeholders, a template, output formats and a size). Edits
are scoped: change one fact, one artifact's fact, or one asset, then rebuild and re-export only what that change
reaches. Input hashes are recorded in .atr-project-state.json next to the manifest.

Manifest (JSON):
  {
    "name": "agentic-robotics-workshop", "title": "...",
    "facts": {"event_date": "Saturday, Nov. 7, 2026", "event_time": "11 a.m.-3 p.m. EST",
              "event_duration": "Four-hour workshop", "talk_duration": "45-minute", "lab_duration": "two-hour",
              "venue": "...", "audience": "...", "agenda": ["...", "..."], "requirements": "...",
              "workflow": [["Inspect", "detail"], ...], "registration_url": "https://example.org/register",
              "contact": "..."},
    "assets": {"tool-codex": {"path": "skill:assets/icons/png/ai-neural-net-navy.png"},
               "ksu-wordmark-white": {"path": "skill:assets/logos/ksu/ksu-wordmark-white.png",
                                      "match": "skill:assets/logos/ksu/ksu-wordmark-white.png", "scope": "all"}},
    "artifacts": {"flyer-letter": {"spec": "flyer.json", "template": "event-flyer", "output": "flyer-letter",
                                   "size": "8.5 x 11 in", "formats": ["pptx", "pdf", "png"],
                                   "lint_medium": "document"},
                  "poster-17x22": {"spec": "flyer.json", "template": "event-flyer-17x22", ...}}
  }

In a spec, "{{facts.NAME}}" is replaced by the fact (an artifact's own "facts" win over the project's), with
optional filters |printed (a URL without https://, to print under a QR code), |upper, |lower and |capitalize.
A string that is only "{{facts.NAME}}" takes a list fact (agenda, workflow) whole. "{{assets.ID}}" becomes the
asset's file path. "skill:" paths point into the skill. An empty or missing fact becomes a [NAME] placeholder,
which new_deck.py refuses unless the build is a --draft. An artifact "template" overrides the spec's, so one
spec builds every size profile (event-flyer, event-flyer-tabloid, event-flyer-17x22).

QR codes: on the event flyers, the spec's own field ("registration_qr": {"qr": {"url": "{{facts.registration_url}}"}})
makes new_deck.py draw the code at the template slot's size and print the clean URL; project.py records that URL
and verifies it in the exported PDF. For a template without a QR field, an artifact "qr" block ({"url", "slide",
"x", "y", "size_in"}, inches) makes the code at its final printed size (after "scale") and places it with
pptx_tools.place_qr, linked, with alt text, idempotent by shape name.

An asset with "match" replaces, in the built file, every picture whose bytes equal the match file (for example
the template's working-copy Kent State wordmark) with the asset's file (pptx_tools.replace_picture); "scope" limits
that to some artifacts. "scale" enlarges a built file with pptx_tools.scale_presentation; prefer a template
profile made for the size when one exists.

Commands (from anywhere; -p defaults to ./project.json):
  python3 scripts/project.py init ~/work/workshop --example workshop     # or a blank manifest without --example
  python3 scripts/project.py status -p project.json [--json]
  python3 scripts/project.py set registration_url https://example.org/register-now -p project.json
         [--artifact flyer-letter]                      # artifact-scoped fact; prints what it affects
  python3 scripts/project.py build -p project.json [--artifact flyer-letter] [--changed-only] [--draft]
  python3 scripts/project.py export -p project.json [--artifact NAME] [--changed-only] [--check-reachable] [--zip]
  python3 scripts/project.py replace-asset ksu-wordmark-white kent-white-stacked.png -p project.json
         [--scope flyer-letter,poster-17x22] [--no-build]

Folders: --work-dir (resolved specs, QR PNGs, build logs, lint JSON, rendered pages and contact sheets),
--cache-dir (downloads such as official artwork) and --out-dir (deliverables, qa-report.md, deliverables.json).
They default to work/, .atr-cache/ ($ATR_DESIGN_CACHE when set) and out/ next to the manifest, or to "dirs" in
the manifest. Nothing is ever written inside the skill: copy the shipped example out with `init --example`.

export writes, per artifact: <output>.pdf (tagged, LibreOffice, brand fonts), the inspection of that PDF, the QR
code decoded from the rendered PDF and compared to the expected URL, page PNGs (only changed pages with
--changed-only) and a contact sheet, and one qa-report.md that keeps three kinds of evidence apart: checked in
source and structure, verified in the exported PDF, and visual review still to do by a person.

Exit status: 0 done; 1 usage, manifest or environment error; 2 refused (placeholders in a final build, a write
into the skill, a refused QR request); 3 built or exported, but a check failed (lint errors, a PDF problem, a QR
code that does not decode to the expected URL, a failed new_deck.py build).
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import argparse  # noqa: E402
import copy  # noqa: E402
import datetime as _dt  # noqa: E402
import hashlib  # noqa: E402
import json  # noqa: E402
import os  # noqa: E402
import re  # noqa: E402
import shutil  # noqa: E402
import subprocess  # noqa: E402
import zipfile  # noqa: E402
from pathlib import Path  # noqa: E402

HERE = Path(__file__).resolve().parent
SKILL = HERE.parent
EXAMPLES = HERE / "examples" / "projects"
STATE_FILE = ".atr-project-state.json"
BUILD_VERSION = "1"     # bump when the build recipe changes in a way that should rebuild every artifact
FACT_KEYS = ["event_title", "eyebrow", "summary", "event_date", "event_time", "event_duration", "talk_duration",
             "lab_duration", "venue", "audience", "agenda", "requirements", "workflow", "registration_url",
             "contact"]
PLACEHOLDER_RE = re.compile(r"\{\{\s*(facts|assets)\.([A-Za-z0-9_.-]+?)\s*((?:\|\s*[a-z]+\s*)*)\}\}")
BRACKET_RE = re.compile(r"\[[^\[\]\n]{1,80}\]")
WORKING_COPY_WORDMARKS = ["assets/logos/ksu/ksu-wordmark-white.png", "assets/logos/ksu/ksu-wordmark-color.png"]
DEFAULT_LIMITS = [
    "PDF exported by LibreOffice; PowerPoint and Keynote can lay text out slightly differently.",
    "Review PDF at trim size: not a PDF/X print file and no bleed; get the printer's preflight and a proof.",
    "PDF tags show the export feature was used; they are not an accessibility conformance check.",
]
QR_LIMIT = "QR codes are decoded from a screen render of the PDF, not scanned by a phone from print."


class ProjectError(Exception):
    """A manifest, usage or environment problem (exit status 1)."""


class Refused(Exception):
    """A request the workflow refuses: writing into the skill, placeholders in a final build (exit status 2)."""


# ----------------------------------------------------------------------------------------------- basics
def now() -> str:
    """Local time stamp, ISO 8601 to the second."""
    return _dt.datetime.now().astimezone().isoformat(timespec="seconds")


def sha256_bytes(data: bytes) -> str:
    """SHA-256 hex digest of bytes."""
    return hashlib.sha256(data).hexdigest()


def sha256_file(path) -> str:
    """SHA-256 hex digest of a file."""
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def canon(obj) -> str:
    """Canonical JSON text (sorted keys) for hashing."""
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def in_skill(path) -> bool:
    """True when path is inside the skill folder (where projects must never write)."""
    try:
        Path(path).expanduser().resolve().relative_to(SKILL)
        return True
    except ValueError:
        return False


def _python() -> str:
    return sys.executable or "python3"


# ----------------------------------------------------------------------------------------------- project
class Project:
    """A loaded project manifest with its folders and state file."""

    def __init__(self, manifest, work_dir=None, cache_dir=None, out_dir=None):
        self.path = Path(manifest).expanduser().resolve()
        if not self.path.is_file():
            raise ProjectError(f"no project manifest at {self.path} (create one with: project.py init <folder>)")
        try:
            self.data = json.loads(self.path.read_text(encoding="utf-8"))
        except ValueError as exc:
            raise ProjectError(f"{self.path} is not valid JSON: {exc}") from exc
        if not isinstance(self.data.get("artifacts"), dict) or not self.data["artifacts"]:
            raise ProjectError(f"{self.path}: needs an \"artifacts\" object with at least one artifact")
        self.data.setdefault("facts", {})
        self.data.setdefault("assets", {})
        self.root = self.path.parent
        dirs = self.data.get("dirs") or {}
        cache_env = os.environ.get("ATR_DESIGN_CACHE")
        self.work_dir = self._dir(work_dir, dirs.get("work"), "work")
        self.cache_dir = self._dir(cache_dir, dirs.get("cache") or cache_env, ".atr-cache")
        self.out_dir = self._dir(out_dir, dirs.get("out"), "out")
        self.in_skill = in_skill(self.path)
        self.state_path = (self.work_dir if self.in_skill else self.root) / STATE_FILE
        self._template_media = {}

    def _dir(self, cli, manifest_value, default) -> Path:
        if cli:
            return Path(cli).expanduser().resolve()
        if manifest_value:
            p = Path(os.path.expanduser(str(manifest_value)))
            return (p if p.is_absolute() else self.root / p).resolve()
        return (self.root / default).resolve()

    # -- writing guards
    def check_writable(self, manifest_too=False) -> None:
        """Refuse to write into the skill: the folders, the state file and (for set/replace-asset) the manifest."""
        if manifest_too and self.in_skill:
            raise Refused(f"{self.path} is inside the skill; copy it out first: project.py init <folder> "
                          f"--example {self.root.name}")
        for label, d in (("work", self.work_dir), ("cache", self.cache_dir), ("out", self.out_dir),
                         ("state", self.state_path)):
            if in_skill(d):
                raise Refused(f"the {label} folder {d} is inside the skill; pass --work-dir, --cache-dir and "
                              "--out-dir outside it (or copy the project out with project.py init --example)")

    def save(self) -> None:
        """Write the manifest back (2-space JSON)."""
        self.check_writable(manifest_too=True)
        self.path.write_text(json.dumps(self.data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    def load_state(self) -> dict:
        """The state file as a dict ({} when there is none yet)."""
        try:
            return json.loads(self.state_path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return {}

    def save_state(self, state: dict) -> None:
        """Write the state file."""
        self.check_writable()
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        self.state_path.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    # -- paths and assets
    def resolve_path(self, value) -> Path:
        """Resolve 'skill:...' (skill root), '~/...', absolute or manifest-relative paths."""
        s = str(value)
        if s.startswith("skill:"):
            return (SKILL / s[len("skill:"):]).resolve()
        p = Path(os.path.expanduser(s))
        return (p if p.is_absolute() else self.root / p).resolve()

    def artifact(self, name) -> dict:
        """The manifest entry of one artifact, or ProjectError."""
        art = self.data["artifacts"].get(name)
        if art is None:
            raise ProjectError(f"no artifact '{name}' (artifacts: {', '.join(self.data['artifacts'])})")
        return art

    def facts_for(self, name) -> dict:
        """Project facts with the artifact's own facts on top."""
        facts = dict(self.data.get("facts") or {})
        facts.update(self.artifact(name).get("facts") or {})
        return facts

    def asset_entry(self, asset_id, artifact=None) -> dict:
        """The asset as the artifact sees it: the project entry with the artifact's own override on top."""
        base = self.data["assets"].get(asset_id)
        if base is None:
            raise ProjectError(f"no asset '{asset_id}' in {self.path.name} (assets: "
                               f"{', '.join(self.data['assets']) or 'none'})")
        entry = dict(base)
        if artifact:
            entry.update((self.artifact(artifact).get("assets") or {}).get(asset_id) or {})
        return entry

    def asset_path(self, asset_id, artifact=None) -> Path:
        """File path of an asset for an artifact."""
        entry = self.asset_entry(asset_id, artifact)
        if not entry.get("path"):
            raise ProjectError(f"asset '{asset_id}' has no \"path\"")
        p = self.resolve_path(entry["path"])
        if not p.is_file():
            raise ProjectError(f"asset '{asset_id}': file not found: {p}")
        return p

    def spec_source(self, name) -> dict:
        """The artifact's spec before substitution (inline dict, or the JSON/YAML file it names)."""
        art = self.artifact(name)
        spec = art.get("spec")
        if isinstance(spec, dict):
            return copy.deepcopy(spec)
        if not spec:
            raise ProjectError(f"artifact '{name}' has no \"spec\"")
        p = self.resolve_path(spec)
        if not p.is_file():
            raise ProjectError(f"artifact '{name}': spec not found: {p}")
        if p.suffix.lower() in (".yaml", ".yml"):
            try:
                import yaml
            except ImportError as exc:
                raise ProjectError("YAML specs need PyYAML (pip install pyyaml)") from exc
            return yaml.safe_load(p.read_text(encoding="utf-8"))
        return json.loads(p.read_text(encoding="utf-8"))

    def template_path(self, spec) -> Path:
        """The .pptx template a spec builds on (alias through new_deck.py's table, or a path)."""
        tpl = str(spec.get("template", "presentation"))
        if tpl.lower().endswith((".pptx", ".potx")):
            return self.resolve_path(tpl)
        import new_deck   # noqa: WPS433 (lazy: needs python-pptx)
        aliases = getattr(new_deck, "TEMPLATE_ALIASES", {})
        if tpl not in aliases:
            raise ProjectError(f"unknown template '{tpl}' (new_deck.py --list-templates)")
        return (SKILL / "assets" / "templates" / aliases[tpl]).resolve()

    def template_media(self, tpl: Path) -> set:
        """SHA-256 of every media file inside a template package (cached)."""
        key = str(tpl)
        if key not in self._template_media:
            hashes = set()
            try:
                with zipfile.ZipFile(tpl) as z:
                    for n in z.namelist():
                        if n.startswith(("ppt/media/", "word/media/")):
                            hashes.add(sha256_bytes(z.read(n)))
            except (OSError, zipfile.BadZipFile):
                pass
            self._template_media[key] = hashes
        return self._template_media[key]


# ----------------------------------------------------------------------------------------------- resolve
def _apply_filters(value: str, filters: list) -> str:
    for f in filters:
        if f == "printed":
            import qr_code
            value = qr_code.fallback_text(value)
        elif f == "upper":
            value = value.upper()
        elif f == "lower":
            value = value.lower()
        elif f == "capitalize":
            value = value[:1].upper() + value[1:]
        else:
            raise ProjectError(f"unknown filter |{f} (use |printed, |upper, |lower or |capitalize)")
    return value


def substitute(obj, facts: dict, asset_lookup, record: dict):
    """Replace {{facts.x}} and {{assets.id}} in every string of obj (recursively); record what was used.

    record gets 'facts' (names used), 'empty' (used but empty or missing) and 'assets' (ids used)."""
    if isinstance(obj, dict):
        return {k: (v if k in ("_comment", "comment") else substitute(v, facts, asset_lookup, record))
                for k, v in obj.items()}
    if isinstance(obj, list):
        return [substitute(v, facts, asset_lookup, record) for v in obj]
    if not isinstance(obj, str):
        return obj
    whole = PLACEHOLDER_RE.fullmatch(obj.strip())
    if whole and whole.group(1) == "facts" and not whole.group(3):
        val = facts.get(whole.group(2))
        if isinstance(val, (list, dict)):        # a list fact (agenda, workflow) replaces the whole value
            record["facts"].add(whole.group(2))
            if not val:
                record["empty"].add(whole.group(2))
                return f"[{whole.group(2)}]"
            return copy.deepcopy(val)

    def repl(m):
        kind, key, raw_filters = m.group(1), m.group(2), m.group(3) or ""
        filters = [f.strip() for f in raw_filters.split("|") if f.strip()]
        if kind == "facts":
            record["facts"].add(key)
            val = facts.get(key)
            if val is None or (isinstance(val, str) and not val.strip()):
                record["empty"].add(key)
                return f"[{key}]"
            return _apply_filters(str(val), filters)
        record["assets"].add(key)
        return str(asset_lookup(key))

    return PLACEHOLDER_RE.sub(repl, obj)


def spec_qr_urls(spec: dict) -> list:
    """URLs of QR codes a spec asks new_deck.py to make: any slide value (or "fields" value) shaped like
    {"qr": {"url": ...}}, or a slide-level "qr": {"url": ...} (the alias)."""
    urls = []
    for sl in spec.get("slides", []) or []:
        if not isinstance(sl, dict):
            continue
        values = list(sl.items()) + list((sl.get("fields") or {}).items())
        for key, val in values:
            if key == "qr" and isinstance(val, dict) and val.get("url"):
                urls.append(str(val["url"]))
            elif isinstance(val, dict) and isinstance(val.get("qr"), dict) and val["qr"].get("url"):
                urls.append(str(val["qr"]["url"]))
    return urls


def _strings(obj, skip=("_comment", "comment")):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k not in skip:
                yield from _strings(v, skip)
    elif isinstance(obj, list):
        for v in obj:
            yield from _strings(v, skip)
    elif isinstance(obj, str):
        yield obj


def resolve_artifact(proj: Project, name: str) -> dict:
    """Resolve one artifact: substituted spec, QR request, assets used, unresolved placeholders, input hashes."""
    art = proj.artifact(name)
    facts = proj.facts_for(name)
    record = {"facts": set(), "empty": set(), "assets": set()}
    missing_assets = []

    def lookup(asset_id):
        try:
            return proj.asset_path(asset_id, name)
        except ProjectError as exc:
            missing_assets.append(str(exc))
            return f"[asset {asset_id}]"

    spec = substitute(proj.spec_source(name), facts, lookup, record)
    if art.get("template"):          # one spec, several template profiles (Letter, Tabloid, 17 x 22)
        spec["template"] = art["template"]
    qr = None
    if art.get("qr"):
        qr = substitute(copy.deepcopy(art["qr"]), facts, lookup, record)
    spec_qr = spec_qr_urls(spec)
    brackets = sorted({b for s in _strings(spec) for b in BRACKET_RE.findall(s)})
    for u in spec_qr:
        brackets = sorted(set(brackets) | set(BRACKET_RE.findall(u)))
    if qr and BRACKET_RE.search(str(qr.get("url", ""))):
        brackets = sorted(set(brackets) | set(BRACKET_RE.findall(str(qr.get("url", "")))))
    tpl = proj.template_path(spec)
    # assets with "match" that this artifact's template carries, in scope
    used = set(record["assets"])
    tpl_media = proj.template_media(tpl) if tpl.is_file() else set()
    for aid, entry in proj.data["assets"].items():
        if not entry.get("match"):
            continue
        scope = entry.get("scope", "all")
        if scope != "all" and name not in (scope if isinstance(scope, list) else [scope]):
            continue
        mp = proj.resolve_path(entry["match"])
        if mp.is_file() and sha256_file(mp) in tpl_media:
            used.add(aid)
    asset_hashes = {}
    for aid in sorted(used):
        try:
            asset_hashes[aid] = sha256_file(proj.asset_path(aid, name))
        except ProjectError as exc:
            missing_assets.append(str(exc))
    scale = float(art.get("scale", 1.0) or 1.0)
    inputs = {
        "spec": sha256_bytes(canon(spec).encode()),
        "template": sha256_file(tpl) if tpl.is_file() else "missing",
        "assets": asset_hashes,
        "qr": sha256_bytes(canon(qr).encode()) if qr else None,
        "scale": scale,
        "post": sha256_bytes(canon({k: art.get(k) for k in ("lint_medium", "output", "formats")}).encode()),
        "tools": sha256_file(HERE / "pptx_tools.py")[:16] if (HERE / "pptx_tools.py").is_file() else None,
        "recipe": BUILD_VERSION + ":" + sha256_file(HERE / "new_deck.py")[:16],
    }
    return {
        "name": name, "artifact": art, "spec": spec, "qr": qr, "spec_qr": spec_qr, "template": str(tpl),
        "facts_used": sorted(record["facts"]), "facts_empty": sorted(record["empty"]),
        "assets_used": sorted(used), "missing_assets": missing_assets, "placeholders": brackets,
        "scale": scale, "inputs": inputs, "input_hash": sha256_bytes(canon(inputs).encode()),
        "output": art.get("output") or name,
    }


def changed_inputs(old: dict, new: dict) -> list:
    """Names of the inputs that differ between two 'inputs' dicts (spec, template, asset ids, qr ...)."""
    if not old:
        return ["never built"]
    out = []
    for k in ("spec", "template", "qr", "scale", "post", "recipe", "tools"):
        if old.get(k) != new.get(k):
            out.append(k)
    oa, na = old.get("assets") or {}, new.get("assets") or {}
    for aid in sorted(set(oa) | set(na)):
        if oa.get(aid) != na.get(aid):
            out.append(f"asset {aid}")
    return out


# ----------------------------------------------------------------------------------------------- assets
def classify_asset(proj: Project, asset_id: str, artifact=None) -> dict:
    """Describe an asset's provenance: official (checksum match), draft (working copy), changed or plain file."""
    entry = proj.asset_entry(asset_id, artifact)
    out = {"id": asset_id, "path": entry.get("path"), "status": "file", "detail": ""}
    try:
        p = proj.asset_path(asset_id, artifact)
    except ProjectError as exc:
        out.update(status="missing", detail=str(exc))
        return out
    digest = sha256_file(p)
    out["sha256"] = digest
    if entry.get("sha256") and entry["sha256"] != digest:
        out.update(status="changed", detail="the file differs from the sha256 recorded in the manifest")
        return out
    try:
        import official_assets   # WS2; optional
        hit = official_assets.verify(p)
    except Exception:  # noqa: BLE001 (module missing or manifest unreadable: fall through)
        hit = None
    if hit:
        out.update(status="official", detail="exact SHA-256 match with the official asset manifest ("
                   + str(hit.get("id", hit.get("name", "official-sources.json"))) + ")")
        return out
    for rel in WORKING_COPY_WORDMARKS:
        wc = SKILL / rel
        if wc.is_file() and sha256_file(wc) == digest:
            out.update(status="draft", detail="working copy of the Kent State wordmark shipped with the templates; "
                       "replace it with the official file from kent.edu/brand/logos before sharing")
            return out
    if entry.get("status"):
        out.update(status=str(entry["status"]), detail=str(entry.get("note", "")))
    return out


def _pptx_tools():
    try:
        import pptx_tools
    except ImportError as exc:   # pragma: no cover (shipped with the skill)
        raise ProjectError(f"scripts/pptx_tools.py is needed for asset swaps, scaling and QR placement ({exc})")
    return pptx_tools


def swap_asset(prs, match_path: Path, new_path: Path, alt=None) -> int:
    """Replace every picture whose bytes equal match_path with new_path (pptx_tools.replace_picture by SHA-256).

    Idempotent: pictures that already hold the new bytes are left alone. Returns the number replaced."""
    if sha256_file(match_path) == sha256_file(new_path):
        return 0
    results = _pptx_tools().replace_picture(prs, sha256_file(match_path), new_path, alt=alt)
    return sum(1 for r in results if r.get("status") == "replaced")


def place_project_qr(prs, png: Path, qr: dict, scale: float, url: str, alt: str) -> None:
    """Put a project-level QR picture on its slide at (x, y) * scale, size_in * scale, linked, with alt text.

    For templates without a QR field (the legacy flyer). Uses pptx_tools.place_qr, idempotent by shape name."""
    slide_no = int(qr.get("slide", 1))
    if not 1 <= slide_no <= len(prs.slides):
        raise ProjectError(f"qr.slide {slide_no} is outside 1-{len(prs.slides)}")
    size = float(qr.get("size_in", 1.0)) * scale
    box = (float(qr["x"]) * scale, float(qr["y"]) * scale, size, size)
    _pptx_tools().place_qr(prs.slides[slide_no - 1], png, name=str(qr.get("name", "QR code")), alt=alt, box=box,
                           url=url if qr.get("link", True) else None)


# ----------------------------------------------------------------------------------------------- build
def _run(cmd, cwd=None, timeout=600) -> subprocess.CompletedProcess:
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout, env=env)


def lint(path: Path, medium: str, report_path: Path) -> dict:
    """Run brand_check.py --json on a built file; save the JSON and return a summary with the top findings."""
    cmd = [_python(), str(HERE / "brand_check.py"), "--json", str(path)]
    if medium:
        cmd[3:3] = ["--medium", medium]
    proc = _run(cmd)
    try:
        data = json.loads(proc.stdout)
    except ValueError:
        return {"at": now(), "ok": False, "error": (proc.stderr or proc.stdout).strip()[:2000]}
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(data, indent=2) + "\n")
    summ = data.get("summary", {})
    findings = [f"{f.get('severity')}: {f.get('check')}: {f.get('message')} ({f.get('location', '')})"
                for f in data.get("findings", []) if f.get("severity") in ("error", "warning", "info")]
    return {"at": now(), "medium": data.get("medium", medium), "errors": summ.get("error", 0),
            "warnings": summ.get("warning", 0), "infos": summ.get("info", 0), "findings": findings[:25],
            "report": str(report_path), "ok": summ.get("error", 0) == 0}


def _drop_placeholder_qr(spec: dict) -> dict:
    """Draft builds: remove spec QR values whose URL is still a [placeholder] (the panel keeps its text)."""
    for sl in spec.get("slides", []) or []:
        for holder in (sl, sl.get("fields") or {}):
            for key in list(holder):
                val = holder[key]
                url = None
                if key == "qr" and isinstance(val, dict):
                    url = val.get("url")
                elif isinstance(val, dict) and isinstance(val.get("qr"), dict):
                    url = val["qr"].get("url")
                if url is not None and BRACKET_RE.search(str(url)):
                    del holder[key]
    return spec


def build_artifact(proj: Project, res: dict, draft=False, run_lint=True) -> dict:
    """Build one resolved artifact: new_deck.py, asset swaps, scaling, QR, lint; copy the .pptx to the out folder.

    Returns the artifact's new state entry ('ok' False when new_deck.py refused or failed)."""
    name, art = res["name"], res["artifact"]
    work = proj.work_dir / name
    work.mkdir(parents=True, exist_ok=True)
    spec = res["spec"]
    if draft and any(BRACKET_RE.search(u) for u in res["spec_qr"]):
        spec = _drop_placeholder_qr(copy.deepcopy(spec))
    spec_file = work / "spec.resolved.json"
    spec_file.write_text(json.dumps(spec, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    raw = work / f"{res['output']}.new_deck.pptx"
    nd_files = work / "new_deck-files"
    if nd_files.is_dir():
        shutil.rmtree(nd_files)
    cmd = [_python(), str(HERE / "new_deck.py"), str(spec_file), "-o", str(raw), "--work-dir", str(nd_files)]
    if draft:
        cmd.append("--allow-placeholders")
    proc = _run(cmd, cwd=str(proj.root))
    log = (proc.stdout or "") + (proc.stderr or "")
    (work / "new_deck.log").write_text(log, encoding="utf-8")
    entry = {"input_hash": res["input_hash"], "inputs": res["inputs"], "built_at": now(), "draft": bool(draft),
             "new_deck": {"status": proc.returncode,
                          "warnings": [ln[9:].strip() for ln in log.splitlines() if ln.startswith("WARNING")],
                          "infos": [ln[9:].strip() for ln in log.splitlines() if ln.startswith("info")],
                          "refusals": [ln.strip() for ln in (proc.stderr or "").splitlines()
                                       if ln.startswith("  ")],
                          "log": str(work / "new_deck.log")},
             "facts_used": res["facts_used"], "assets_used": res["assets_used"],
             "placeholders": res["placeholders"], "ok": False}
    if proc.returncode not in (0, 3) or not raw.is_file():
        entry["error"] = "new_deck.py " + ("refused the spec" if proc.returncode == 2 else "failed") + \
            f" (status {proc.returncode}); see {work / 'new_deck.log'}"
        return entry
    from pptx import Presentation
    prs = Presentation(str(raw))
    steps = []
    for aid in res["assets_used"]:
        a = proj.asset_entry(aid, name)
        if not a.get("match"):
            continue
        n = swap_asset(prs, proj.resolve_path(a["match"]), proj.asset_path(aid, name), a.get("alt"))
        if n:
            steps.append(f"asset {aid}: replaced {n} picture(s) (pptx_tools.replace_picture)")
    if res["scale"] != 1.0:
        _pptx_tools().scale_presentation(prs, res["scale"])
        steps.append(f"scaled x{res['scale']:g} (pptx_tools.scale_presentation)")
    qr_state = None
    if res["qr"] and not res["spec_qr"] and draft and BRACKET_RE.search(str(res["qr"].get("url", ""))):
        steps.append("QR skipped: its URL is still a placeholder (draft build)")
    elif res["qr"] and not res["spec_qr"]:
        import qr_code
        q = res["qr"]
        url = str(q.get("url", ""))
        size = float(q.get("size_in", 1.0)) * res["scale"]
        png = work / f"{res['output']}-qr.png"
        info = qr_code.describe_qr(url, size, int(q.get("dpi", 600)), q.get("ecc", "M"),
                                   int(q.get("quiet", 4)), q.get("color", qr_code.NAVY))
        qr_code.make_qr(url, png, size, int(q.get("dpi", 600)), q.get("ecc", "M"), int(q.get("quiet", 4)),
                        q.get("color", qr_code.NAVY))
        alt = q.get("alt") or qr_code.alt_text(url, q.get("destination", ""), q.get("where", "below it"))
        place_project_qr(prs, png, q, res["scale"], url, alt)
        decoded = qr_code.decode_image(png)
        qr_state = {"url": url, "png": str(png), "png_sha256": sha256_file(png), "size_in": size,
                    "printed_fallback": info["printed_fallback"], "alt": alt, "version": info["version"],
                    "ecc": info["ecc"], "notes": info["notes"], "png_decodes": decoded == [url],
                    "made_at": now()}
        steps.append(f"QR {size:g} in placed on slide {q.get('slide', 1)}")
    elif res["spec_qr"] and draft and any(BRACKET_RE.search(u) for u in res["spec_qr"]):
        steps.append("QR skipped: its URL is still a placeholder (draft build)")
    elif res["spec_qr"]:
        import qr_code
        url = res["spec_qr"][0]
        pngs = sorted(nd_files.glob("qr-*.png")) if nd_files.is_dir() else []
        decoded = qr_code.decode_image(pngs[0]) if pngs else None
        qr_state = {"url": url, "placed_by": "new_deck.py (spec QR field)", "made_at": now(),
                    "png": str(pngs[0]) if pngs else None, "png_decodes": decoded == [url] if pngs else None,
                    "printed_fallback": qr_code.fallback_text(url), "notes": qr_code.url_notes(url)}
        if pngs:
            from PIL import Image
            with Image.open(pngs[0]) as im:
                dpi = (im.info.get("dpi") or (600, 600))[0]
                qr_state["size_in"] = round(im.width / float(dpi), 3)
        if len(set(res["spec_qr"])) > 1:
            steps.append("note: the spec has QR codes to more than one address; only the first is verified")
    built = work / f"{res['output']}.pptx"
    prs.save(str(built))
    entry["steps"] = steps
    entry["qr"] = qr_state
    if run_lint:
        entry["lint"] = lint(built, art.get("lint_medium", ""), work / "brand-check.json")
    proj.out_dir.mkdir(parents=True, exist_ok=True)
    deliverable = proj.out_dir / built.name
    shutil.copy2(built, deliverable)
    entry.update(pptx=str(deliverable), pptx_sha256=sha256_file(deliverable), ok=True)
    return entry


def select_artifacts(proj: Project, names) -> list:
    """Artifact names from a comma list (or all of them)."""
    if not names:
        return list(proj.data["artifacts"])
    out = []
    for chunk in names:
        for n in str(chunk).split(","):
            n = n.strip()
            if n:
                proj.artifact(n)
                out.append(n)
    return out


def cmd_build(proj: Project, names=None, changed_only=False, draft=False, run_lint=True, quiet=False) -> int:
    """Build the selected artifacts (only those whose inputs changed with changed_only). Returns exit status."""
    proj.check_writable()
    state = proj.load_state()
    arts = state.setdefault("artifacts", {})
    status = 0
    built, skipped = [], []
    for name in select_artifacts(proj, names):
        res = resolve_artifact(proj, name)
        if res["missing_assets"]:
            print(f"{name}: " + "; ".join(res["missing_assets"]), file=sys.stderr)
            status = max(status, 1)
            continue
        old = arts.get(name, {})
        current = (old.get("input_hash") == res["input_hash"] and old.get("ok")
                   and old.get("pptx") and Path(old["pptx"]).is_file()
                   and sha256_file(old["pptx"]) == old.get("pptx_sha256"))
        if changed_only and current:
            skipped.append(name)
            continue
        if res["placeholders"] and not draft:
            print(f"{name}: REFUSED: unresolved placeholders {', '.join(res['placeholders'])}"
                  + (f" (empty facts: {', '.join(res['facts_empty'])})" if res["facts_empty"] else "")
                  + ". Set the facts (project.py set NAME VALUE) or build a --draft.", file=sys.stderr)
            status = max(status, 2)
            continue
        why = changed_inputs(old.get("inputs") or {}, res["inputs"])
        try:
            entry = build_artifact(proj, res, draft=draft, run_lint=run_lint)
        except Exception as exc:  # noqa: BLE001 (one failing artifact must not stop the others)
            name_err = type(exc).__name__
            if name_err == "QRError":
                print(f"{name}: QR refused: {exc}", file=sys.stderr)
                status = max(status, 2)
            else:
                print(f"{name}: build failed: {exc}", file=sys.stderr)
                status = max(status, 3)
            continue
        if old.get("export"):
            entry["export"] = old["export"]     # kept; status shows it as stale until export runs
        arts[name] = entry
        built.append(name)
        if not entry["ok"]:
            print(f"{name}: {entry.get('error')}", file=sys.stderr)
            for r in entry["new_deck"]["refusals"]:
                print(f"    {r.strip()}", file=sys.stderr)
            status = max(status, 3)
            continue
        lint_s = entry.get("lint") or {}
        lint_txt = (f"lint {lint_s.get('errors', '?')} error(s), {lint_s.get('warnings', '?')} warning(s)"
                    if lint_s else "lint skipped")
        if lint_s and not lint_s.get("ok", True):
            status = max(status, 3)
        if not quiet:
            print(f"built   {name}: {entry['pptx']}  (changed: {', '.join(why) or 'forced rebuild'}; "
                  f"{len(entry['new_deck']['warnings'])} build warning(s); {lint_txt})")
            for st in entry.get("steps", []):
                print(f"        {st}")
    state["updated_at"] = now()
    state.setdefault("log", []).append({"at": now(), "command": "build", "built": built, "skipped": skipped})
    state["log"] = state["log"][-50:]
    proj.save_state(state)
    if not quiet and skipped:
        print(f"skipped {', '.join(skipped)} (inputs unchanged)")
    return status


# ----------------------------------------------------------------------------------------------- export
def _parse_size(text) -> tuple:
    m = re.match(r"\s*([\d.]+)\s*[x×]\s*([\d.]+)", str(text or ""))
    return (float(m.group(1)), float(m.group(2))) if m else None


def export_artifact(proj: Project, name: str, entry: dict, changed_only=True, dpi=150,
                    check_reachable=False) -> dict:
    """Export one built artifact: tagged PDF, inspection, QR verification, changed-page renders, contact sheet."""
    import export_office
    import qr_code
    art = proj.artifact(name)
    pptx = Path(entry["pptx"])
    formats = art.get("formats") or ["pptx", "pdf"]
    pdf = export_office.export_pdf(pptx, proj.out_dir, tagged=True)
    ins = export_office.inspect_pdf(pdf)
    ex = {"at": now(), "pptx_sha256": entry["pptx_sha256"], "pdf": str(pdf), "pdf_sha256": ins["sha256"],
          "inspection": {k: ins[k] for k in ("pages", "distinct_page_sizes_in", "tagged", "fonts", "links",
                                             "bookmarks", "problems")},
          "inspection_lines": export_office.inspection_lines(ins), "problems": list(ins["problems"])}
    want = _parse_size(art.get("size"))
    if want:
        sizes = [tuple(s) for s in ins["distinct_page_sizes_in"]]
        ok = all(abs(w - want[0]) < 0.02 and abs(h - want[1]) < 0.02 for w, h in sizes)
        ex["size_check"] = {"declared": art.get("size"), "ok": ok}
        if not ok:
            ex["problems"].append(f"page size {sizes} differs from the declared {art.get('size')}")
    url = (entry.get("qr") or {}).get("url")
    if url:
        ver = qr_code.verify_pdf(pdf, url, dpi=200)
        if check_reachable:
            ver["reachability"] = qr_code.check_reachable(url)
        ex["qr_verify"] = ver
        if not ver["ok"]:
            ex["problems"].extend(ver["problems"])
    qa = proj.work_dir / "qa" / name
    if changed_only:
        rendered, allp = export_office.render_changed(pdf, qa, dpi)
    else:
        allp = export_office.render(pdf, qa, dpi)
        export_office.save_page_hashes(pdf, qa, dpi)
        rendered = allp
    sheet = export_office.contact_sheet(allp, qa / f"{pdf.stem}-sheet.png")
    ex.update(rendered_pages=[_page_no(p) for p in rendered], all_pages=len(allp), qa_dir=str(qa),
              sheet=str(sheet), page_pngs=[str(p) for p in allp], dpi=dpi)
    if "png" in formats:
        pngs = []
        for p in allp:
            dest = proj.out_dir / (pdf.stem + ".png" if len(allp) == 1 else f"{pdf.stem}-page-{_page_no(p):02d}.png")
            if _page_no(p) in ex["rendered_pages"] or not dest.is_file():
                shutil.copy2(p, dest)
            pngs.append(str(dest))
        ex["png"] = pngs
    if "pdf" not in formats:
        ex["note"] = "PDF exported for QA only (pdf is not in formats)"
    ex["ok"] = not ex["problems"]
    return ex


def _page_no(p) -> int:
    m = re.search(r"-page-(\d+)\.png$", str(p))
    return int(m.group(1)) if m else 0


def cmd_export(proj: Project, names=None, changed_only=False, dpi=150, check_reachable=False,
               make_zip=False) -> int:
    """Export, inspect, verify and render the selected built artifacts; write qa-report.md. Returns exit status."""
    proj.check_writable()
    state = proj.load_state()
    arts = state.setdefault("artifacts", {})
    status = 0
    done, skipped = [], []
    for name in select_artifacts(proj, names):
        entry = arts.get(name)
        if not entry or not entry.get("ok") or not entry.get("pptx") or not Path(entry["pptx"]).is_file():
            print(f"{name}: not built yet (run project.py build)", file=sys.stderr)
            status = max(status, 1)
            continue
        res = resolve_artifact(proj, name)
        if res["input_hash"] != entry.get("input_hash"):
            print(f"{name}: WARNING the build is stale (changed: "
                  f"{', '.join(changed_inputs(entry.get('inputs') or {}, res['inputs']))}); exporting the last "
                  "build. Run build --changed-only first.", file=sys.stderr)
        old = entry.get("export") or {}
        pdf_ok = old.get("pdf") and Path(old["pdf"]).is_file()
        if changed_only and pdf_ok and old.get("pptx_sha256") == entry.get("pptx_sha256"):
            skipped.append(name)
            continue
        try:
            ex = export_artifact(proj, name, entry, changed_only=changed_only, dpi=dpi,
                                 check_reachable=check_reachable)
        except Exception as exc:  # noqa: BLE001
            print(f"{name}: export failed: {exc}", file=sys.stderr)
            status = max(status, 3 if not isinstance(exc, (FileNotFoundError,)) else 1)
            continue
        entry["export"] = ex
        done.append(name)
        if not ex["ok"]:
            status = max(status, 3)
        qv = ex.get("qr_verify")
        qtxt = ""
        if qv:
            qtxt = ("; QR decoded from the PDF = " + qv["expected_url"]) if qv["qr_match"] else "; QR NOT verified"
        rendered = ex["rendered_pages"]
        print(f"exported {name}: {ex['pdf']}  ({ex['inspection']['pages']} page(s); re-rendered "
              f"{len(rendered)} of {ex['all_pages']}: {', '.join(map(str, rendered)) or 'none'}{qtxt})")
        for p in ex["problems"]:
            print(f"         PROBLEM {p}")
    state["updated_at"] = now()
    state.setdefault("log", []).append({"at": now(), "command": "export", "exported": done, "skipped": skipped})
    state["log"] = state["log"][-50:]
    proj.save_state(state)
    if skipped:
        print(f"skipped {', '.join(skipped)} (built file unchanged since its last export)")
    write_deliverables(proj, state)
    report = write_qa_report(proj, state, done)
    print(f"QA report {report}")
    if make_zip:
        print(f"package  {write_zip(proj, state)}")
    return status


def write_deliverables(proj: Project, state: dict) -> Path:
    """Write <out>/deliverables.json: every deliverable file with its SHA-256."""
    out = {"project": proj.data.get("name", proj.root.name), "updated_at": now(), "artifacts": {}}
    for name, entry in (state.get("artifacts") or {}).items():
        files = []
        for key in ("pptx",):
            if entry.get(key) and Path(entry[key]).is_file():
                files.append(entry[key])
        ex = entry.get("export") or {}
        if ex.get("pdf") and Path(ex["pdf"]).is_file():
            files.append(ex["pdf"])
        files += [p for p in ex.get("png", []) if Path(p).is_file()]
        out["artifacts"][name] = {"built_at": entry.get("built_at"), "exported_at": ex.get("at"),
                                  "files": {Path(f).name: sha256_file(f) for f in files}}
    dest = proj.out_dir / "deliverables.json"
    dest.write_text(json.dumps(out, indent=2) + "\n")
    return dest


def write_zip(proj: Project, state: dict) -> Path:
    """Zip every current deliverable plus qa-report.md and deliverables.json into the out folder."""
    name = re.sub(r"[^a-z0-9-]+", "-", str(proj.data.get("name", proj.root.name)).lower()).strip("-")
    dest = proj.out_dir / f"{name}-deliverables.zip"
    data = json.loads((proj.out_dir / "deliverables.json").read_text())
    with zipfile.ZipFile(dest, "w", zipfile.ZIP_DEFLATED) as z:
        for art in data["artifacts"].values():
            for fn in art["files"]:
                z.write(proj.out_dir / fn, fn)
        for extra in ("qa-report.md", "deliverables.json"):
            if (proj.out_dir / extra).is_file():
                z.write(proj.out_dir / extra, extra)
    return dest


# ----------------------------------------------------------------------------------------------- report
def limits_for(art: dict, has_qr: bool) -> list:
    """Export limitations that apply to one artifact (the defaults, the QR one, and the artifact's own)."""
    return DEFAULT_LIMITS + ([QR_LIMIT] if has_qr else []) + list(art.get("limits") or [])


def write_qa_report(proj: Project, state: dict, exported_now=()) -> Path:
    """Write <out>/qa-report.md with, per artifact, source checks, PDF-verified facts and the visual review to do."""
    title = proj.data.get("title") or proj.data.get("name") or proj.root.name
    L = [f"# QA report: {title}", "",
         f"Generated {now()} by `project.py export` from `{proj.path}`.", "",
         "Three kinds of evidence are kept apart below. **Checked in source** means the spec and the .pptx were "
         "read (new_deck.py, brand_check.py). **Verified in the PDF** means the exported file itself was read "
         "or rendered and decoded. **Visual review** lists what a person still has to look at; a clean lint "
         "result is never a render check.", "",
         "| Artifact | Built | Lint (source) | PDF (verified) | QR in PDF | Pages re-rendered this run |",
         "|---|---|---|---|---|---|"]
    arts = state.get("artifacts") or {}
    for name in proj.data["artifacts"]:
        e = arts.get(name) or {}
        ex = e.get("export") or {}
        lint_s = e.get("lint") or {}
        lint_txt = f"{lint_s.get('errors', '-')} errors, {lint_s.get('warnings', '-')} warnings" if lint_s else "-"
        pdf_txt = "-"
        if ex:
            stale = ex.get("pptx_sha256") != e.get("pptx_sha256")
            tagged = "tagged" if ex["inspection"]["tagged"]["is_tagged"] else "NOT tagged"
            pdf_txt = f"{ex['inspection']['pages']} p., {tagged}" + (", STALE" if stale else "") + \
                ("" if ex.get("ok") else ", problems")
        qr_txt = "-"
        if ex.get("qr_verify"):
            qr_txt = "exact match" if ex["qr_verify"]["qr_match"] and ex["qr_verify"]["ok"] else "FAILED"
        rr = ", ".join(map(str, ex.get("rendered_pages", []))) if name in exported_now else "not exported this run"
        L.append(f"| {name} | {e.get('built_at', 'never')} | {lint_txt} | {pdf_txt} | {qr_txt} | {rr or 'none'} |")
    L.append("")
    for name in proj.data["artifacts"]:
        e = arts.get(name) or {}
        art = proj.artifact(name)
        ex = e.get("export") or {}
        L += [f"## {name}", ""]
        if not e:
            L += ["Not built yet.", ""]
            continue
        L.append(f"Deliverable: `{e.get('pptx')}`" + (f", `{ex.get('pdf')}`" if ex else ""))
        if ex and name not in exported_now:
            L.append(f"Not re-exported this run; the PDF evidence below is from {ex.get('at')}.")
        L += ["", "### 1. Checked in source and structure", ""]
        nd = e.get("new_deck") or {}
        L.append(f"- new_deck.py build at {e.get('built_at')}: status {nd.get('status')}, "
                 f"{len(nd.get('warnings', []))} warning(s)" + (" (draft build)" if e.get("draft") else ""))
        for w in nd.get("warnings", [])[:10]:
            L.append(f"  - {w}")
        lint_s = e.get("lint") or {}
        if lint_s:
            L.append(f"- brand_check.py ({lint_s.get('medium')}) at {lint_s.get('at')}: {lint_s.get('errors')} "
                     f"error(s), {lint_s.get('warnings')} warning(s), {lint_s.get('infos')} info")
            for f in lint_s.get("findings", [])[:10]:
                L.append(f"  - {f}")
        else:
            L.append("- brand_check.py: not run")
        L.append("- Facts used: " + (", ".join(e.get("facts_used", [])) or "none")
                 + "; unresolved placeholders: " + (", ".join(e.get("placeholders", [])) or "none"))
        for aid in e.get("assets_used", []):
            c = classify_asset(proj, aid, name)
            L.append(f"- Asset {aid}: {c['status']}" + (f" ({c['detail']})" if c["detail"] else ""))
        q = e.get("qr")
        if q and q.get("png"):
            bits = [f"QR PNG {q['size_in']:g} in" if q.get("size_in") else "QR PNG",
                    f"made by {q.get('placed_by', 'project.py')}"]
            if q.get("version"):
                bits.append(f"version {q['version']}, ECC {q['ecc']}")
            L.append("- " + ", ".join(bits) + "; 4-module quiet zone; the PNG decodes to the URL: "
                     + ("yes" if q.get("png_decodes") else "NO") + f". Printed fallback: `{q.get('printed_fallback')}`"
                     + (f". Alt text: \"{q['alt']}\"" if q.get("alt") else ""))
            for n in q.get("notes", []):
                L.append(f"  - {n}")
        for st in e.get("steps", []):
            L.append(f"- Build step: {st}")
        L += ["", "### 2. Verified in the exported PDF", ""]
        if not ex:
            L.append("- Not exported yet.")
        else:
            if ex.get("pptx_sha256") != e.get("pptx_sha256"):
                L.append("- **STALE**: the .pptx was rebuilt after this PDF was exported.")
            L.append(f"- Exported {ex.get('at')}: `{ex.get('pdf')}` (SHA-256 {ex.get('pdf_sha256', '')[:16]}...)")
            for ln in ex.get("inspection_lines", []):
                L.append(f"- {ln}")
            sc = ex.get("size_check")
            if sc:
                L.append(f"- Page size matches the declared {sc['declared']}: {'yes' if sc['ok'] else 'NO'}")
            qv = ex.get("qr_verify")
            if qv:
                for p in qv["pages"]:
                    vals = ", ".join(f"`{v}`" for v in p["qr"]) or "no QR code"
                    L.append(f"- Page {p['page']} rendered at {qv['dpi']} dpi and decoded: {vals}")
                L.append(f"- Decoded value equals the expected `{qv['expected_url']}` exactly: "
                         f"{'yes' if qv['qr_match'] else 'NO'}; PDF link annotation to it: "
                         f"{'yes' if qv['link_match'] else 'no'}")
                reach = qv.get("reachability")
                if reach:
                    state_txt = f"HTTP {reach['status']}" if reach["status"] else f"no answer ({reach['error']})"
                    L.append(f"- Reachability at {reach['checked_at']}: {state_txt}. {reach['meaning']}")
                else:
                    L.append("- Reachability: not checked (export --check-reachable makes one HTTP GET). "
                             "A reachable page would still not show that a form submission works.")
            for p in ex.get("problems", []):
                L.append(f"- **Problem:** {p}")
        L += ["", "### 3. Visual review still to do (by a person)", ""]
        if ex:
            L.append(f"- [ ] Look at the contact sheet `{ex.get('sheet')}` and every full-size page in "
                     f"`{ex.get('qa_dir')}` (re-rendered this run: "
                     f"{', '.join(map(str, ex.get('rendered_pages', []))) if name in exported_now else 'none'}).")
        L.append("- [ ] Text fits its boxes, nothing overlaps, links and the printed address read clearly on "
                 "their background.")
        if q:
            L.append("- [ ] Scan the QR code with an iPhone and an Android phone from a 100% printed proof at the "
                     "intended distance.")
            L.append("- [ ] Open the destination and confirm it is the intended page; submitting the form is a "
                     "separate check.")
        L.append("- [ ] For print: printer preflight and a hard proof (color, trim).")
        L += ["", "### Export limitations", ""]
        for lim in limits_for(art, bool(q)):
            L.append(f"- {lim}")
        L.append("")
    dest = proj.out_dir / "qa-report.md"
    proj.out_dir.mkdir(parents=True, exist_ok=True)
    dest.write_text("\n".join(L).rstrip() + "\n", encoding="utf-8")
    return dest


# ----------------------------------------------------------------------------------------------- status
def project_status(proj: Project) -> dict:
    """Readiness per artifact: build state, facts and placeholders, assets, lint, export, QR, limits."""
    state = proj.load_state()
    arts = state.get("artifacts") or {}
    facts = proj.data.get("facts") or {}
    empty_facts = sorted(k for k, v in facts.items() if v is None or (isinstance(v, str) and not v.strip()))
    out = {"project": str(proj.path), "work_dir": str(proj.work_dir), "out_dir": str(proj.out_dir),
           "cache_dir": str(proj.cache_dir), "state_file": str(proj.state_path), "empty_facts": empty_facts,
           "artifacts": {}}
    for name in proj.data["artifacts"]:
        art = proj.artifact(name)
        e = arts.get(name) or {}
        try:
            res = resolve_artifact(proj, name)
        except ProjectError as exc:
            out["artifacts"][name] = {"error": str(exc)}
            continue
        changed = changed_inputs(e.get("inputs") or {}, res["inputs"]) if e else ["never built"]
        build_state = "never built" if not e else ("current" if not changed and e.get("ok") else "stale")
        assets = [classify_asset(proj, aid, name) for aid in res["assets_used"]]
        ex = e.get("export") or {}
        export_state = "not exported"
        if ex:
            export_state = "current" if ex.get("pptx_sha256") == e.get("pptx_sha256") else "stale"
        qv = ex.get("qr_verify") or {}
        ready = (build_state == "current" and export_state == "current" and not res["placeholders"]
                 and not any(a["status"] in ("draft", "missing", "changed") for a in assets)
                 and (e.get("lint") or {}).get("ok", False) and ex.get("ok", False)
                 and not (e.get("new_deck") or {}).get("warnings"))
        out["artifacts"][name] = {
            "output": res["output"], "spec": art.get("spec") if isinstance(art.get("spec"), str) else "(inline)",
            "template": Path(res["template"]).name, "size": art.get("size"),
            "build": build_state, "changed_inputs": changed if build_state != "current" else [],
            "built_at": e.get("built_at"), "draft_build": e.get("draft", False),
            "build_warnings": (e.get("new_deck") or {}).get("warnings", []),
            "facts_used": res["facts_used"], "facts_empty": res["facts_empty"],
            "placeholders": res["placeholders"], "assets": assets,
            "lint": {k: (e.get("lint") or {}).get(k) for k in ("at", "medium", "errors", "warnings", "infos")}
            if e.get("lint") else None,
            "export": export_state, "exported_at": ex.get("at"),
            "pdf_tagged": (ex.get("inspection") or {}).get("tagged", {}).get("is_tagged") if ex else None,
            "pdf_problems": ex.get("problems", []) if ex else [],
            "rendered_at": ex.get("at"), "rendered_pages_last_run": ex.get("rendered_pages"),
            "qr_url": (res["qr"] or {}).get("url") if res["qr"] else ((res["spec_qr"] or [None])[0]),
            "qr_verified": ({"at": qv.get("checked_at"), "url": qv.get("expected_url"), "match": qv.get("qr_match"),
                             "link": qv.get("link_match")} if qv else None),
            "limits": limits_for(art, bool(res["qr"] or res["spec_qr"])),
            "checks_pass": bool(ready),
        }
    return out


def _print_status(st: dict) -> None:
    print(f"project   {st['project']}")
    print(f"folders   work {st['work_dir']}\n          out  {st['out_dir']}\n          cache {st['cache_dir']}")
    if st["empty_facts"]:
        print(f"facts     empty: {', '.join(st['empty_facts'])}")
    for name, a in st["artifacts"].items():
        print()
        if a.get("error"):
            print(f"{name}: ERROR {a['error']}")
            continue
        print(f"{name}  ({a['spec']} on {a['template']}" + (f", {a['size']}" if a.get("size") else "") + ")"
              + ("  CHECKS PASS (visual review still to do)" if a["checks_pass"] else "  NOT READY"))
        build = a["build"] + (f" (changed: {', '.join(a['changed_inputs'])})"
                              if a["changed_inputs"] and a["build"] != "never built" else "")
        print(f"  build         {build}" + (f", built {a['built_at']}" if a["built_at"] else "")
              + (" [draft]" if a["draft_build"] else ""))
        for w in a["build_warnings"]:
            print(f"  build warning {w}")
        print(f"  facts         {', '.join(a['facts_used']) or 'none'}"
              + (f"; EMPTY: {', '.join(a['facts_empty'])}" if a["facts_empty"] else ""))
        print(f"  placeholders  {', '.join(a['placeholders']) or 'none'}")
        for asset in a["assets"]:
            flag = asset["status"].upper() if asset["status"] in ("draft", "missing", "changed") else asset["status"]
            print(f"  asset         {asset['id']}: {flag}" + (f" - {asset['detail']}" if asset["detail"] else ""))
        lint_s = a["lint"]
        print("  lint          " + (f"{lint_s['errors']} error(s), {lint_s['warnings']} warning(s), "
                                    f"{lint_s['infos']} info ({lint_s['medium']}) at {lint_s['at']}"
                                    if lint_s else "not run"))
        exp = a["export"] + (f" at {a['exported_at']}" if a["exported_at"] else "")
        if a["pdf_tagged"] is not None:
            exp += ", tagged" if a["pdf_tagged"] else ", NOT tagged"
        print(f"  export        {exp}")
        for p in a["pdf_problems"]:
            print(f"                PROBLEM {p}")
        if a["qr_url"]:
            qv = a["qr_verified"]
            if qv:
                same = qv["url"] == a["qr_url"]
                print(f"  QR            {a['qr_url']}: " + (
                    ("decoded from the PDF at " + str(qv["at"]) if qv["match"] else "NOT decoded from the PDF")
                    if same else f"last verified for a different URL ({qv['url']}); re-export"))
            else:
                print(f"  QR            {a['qr_url']}: not verified in a PDF yet")
        print(f"  limits        {a['limits'][0]}")
        for lim in a["limits"][1:]:
            print(f"                {lim}")


# ----------------------------------------------------------------------------------------------- init / set
BLANK = {
    "schema": "atr-project/1", "name": "", "title": "",
    "facts": {k: "" for k in FACT_KEYS},
    "assets": {
        "tool-claude-code": {"path": "skill:assets/icons/png/code-navy.png",
                             "note": "Stand-in icon for the tools row; replace it with the vendor's official icon."},
        "tool-codex": {"path": "skill:assets/icons/png/ai-neural-net-navy.png",
                       "note": "Stand-in icon for the tools row; replace it with the vendor's official icon."},
        "ksu-wordmark-white": {
        "path": "skill:assets/logos/ksu/ksu-wordmark-white.png",
        "match": "skill:assets/logos/ksu/ksu-wordmark-white.png", "scope": "all",
        "alt": "Kent State University wordmark.",
        "note": "Working copy in the templates; replace it with the official file before sharing."}},
    "artifacts": {"flyer-letter": {"spec": "flyer.json", "template": "event-flyer", "output": "flyer-letter",
                                   "size": "8.5 x 11 in", "formats": ["pptx", "pdf", "png"],
                                   "lint_medium": "document"}},
}


def cmd_init(folder, example=None, name=None, force=False) -> int:
    """Create a project folder with project.json (blank, or a copy of a shipped example). Returns exit status."""
    dest = Path(folder).expanduser().resolve()
    if in_skill(dest):
        raise Refused(f"{dest} is inside the skill; create projects somewhere else")
    manifest = dest / "project.json"
    if manifest.exists() and not force:
        raise ProjectError(f"{manifest} exists (pass --force to overwrite)")
    dest.mkdir(parents=True, exist_ok=True)
    if example:
        src = EXAMPLES / example
        if not (src / "project.json").is_file():
            avail = ", ".join(sorted(p.name for p in EXAMPLES.iterdir() if (p / "project.json").is_file()))
            raise ProjectError(f"no example '{example}' (examples: {avail or 'none'})")
        for f in sorted(src.iterdir()):
            if f.is_file() and f.suffix.lower() in (".json", ".yaml", ".yml", ".png", ".jpg", ".svg"):
                shutil.copy2(f, dest / f.name)
        data = json.loads(manifest.read_text(encoding="utf-8"))
    else:
        data = copy.deepcopy(BLANK)
        data["name"] = name or dest.name
        data["title"] = name or dest.name
        manifest.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        shutil.copy2(EXAMPLES / "workshop" / "flyer.json", dest / "flyer.json")
        print("note: flyer.json is the workshop example's event-flyer spec; fill the facts in project.json and edit "
              "the spec's fixed text and tools (see scripts/examples/projects/workshop/)")
    if name:
        data["name"] = name
    data.pop("_comment", None)
    proj_tmp = dest / "project.json"
    proj_tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    proj = Project(proj_tmp)
    for aid, entry in proj.data["assets"].items():   # record checksums so later changes are noticed
        try:
            entry["sha256"] = sha256_file(proj.asset_path(aid))
        except ProjectError:
            pass
    proj.save()
    print(f"created {manifest}")
    print(f"next: project.py status -p {manifest}; project.py build -p {manifest}")
    return 0


def _affected(proj: Project, before: dict) -> tuple:
    changed, same = [], []
    for name in proj.data["artifacts"]:
        try:
            h = resolve_artifact(proj, name)["input_hash"]
        except ProjectError:
            h = None
        (changed if before.get(name) != h else same).append(name)
    return changed, same


def _hashes(proj: Project) -> dict:
    out = {}
    for name in proj.data["artifacts"]:
        try:
            out[name] = resolve_artifact(proj, name)["input_hash"]
        except ProjectError:
            out[name] = None
    return out


def cmd_set(proj: Project, fact: str, value: str, artifact=None) -> int:
    """Set a project fact (or an artifact's own fact) and print which artifacts the change reaches."""
    proj.check_writable(manifest_too=True)
    before = _hashes(proj)
    target = proj.artifact(artifact).setdefault("facts", {}) if artifact else proj.data["facts"]
    old = target.get(fact)
    value = value.replace("\\n", "\n")
    if old == value:
        print(f"{fact} is already {value!r}; nothing changes")
        return 0
    target[fact] = value
    known = set(proj.data["facts"]) | set(FACT_KEYS)
    if not artifact and fact not in known:
        print(f"note: '{fact}' is a new fact; specs reach it as {{{{facts.{fact}}}}}")
    proj.save()
    changed, same = _affected(proj, before)
    where = f"artifact {artifact}" if artifact else "project"
    print(f"set {fact} ({where}): {old!r} -> {value!r}")
    print("affects  " + (", ".join(changed) or "no artifact (no spec uses it)"))
    if same:
        print("unchanged " + ", ".join(same))
    if changed:
        print("next     project.py build --changed-only, then project.py export --changed-only")
    return 0


def cmd_replace_asset(proj: Project, asset_id: str, new_path: str, scope=None, build=True, draft=False) -> int:
    """Point an asset at a new file (everywhere, or only for the artifacts in scope) and rebuild what uses it.

    Idempotent: replacing with the same file again changes nothing and rebuilds nothing."""
    proj.check_writable(manifest_too=True)
    proj.asset_entry(asset_id)
    if str(new_path).startswith("official:"):
        try:
            import official_assets
        except ImportError as exc:
            raise ProjectError("official:<id> needs scripts/official_assets.py") from exc
        p = Path(official_assets.fetch(str(new_path)[len("official:"):], cache_dir=proj.cache_dir / "official"))
    else:
        p = Path(new_path).expanduser().resolve()
    if not p.is_file():
        raise ProjectError(f"replacement file not found: {p}")
    digest = sha256_file(p)
    try:
        rel = str(p.relative_to(proj.root))
    except ValueError:
        rel = str(p)
    before = _hashes(proj)
    targets = select_artifacts(proj, [scope]) if scope else None
    if targets:
        for name in targets:
            over = proj.artifact(name).setdefault("assets", {}).setdefault(asset_id, {})
            if over.get("sha256") == digest and over.get("path") == rel:
                continue
            over.update(path=rel, sha256=digest)
    else:
        entry = proj.data["assets"][asset_id]
        if not (entry.get("sha256") == digest and entry.get("path") == rel):
            entry.update(path=rel, sha256=digest)
    changed, same = _affected(proj, before)
    state = proj.load_state()
    stale = [n for n in proj.data["artifacts"]
             if (state.get("artifacts", {}).get(n) or {}).get("input_hash") != before.get(n)]
    if not changed:
        print(f"{asset_id} already uses {p.name} ({digest[:12]}) " + (f"for {', '.join(targets)}" if targets
                                                                         else "everywhere") + "; nothing to rebuild")
        return 0
    proj.save()
    c = classify_asset(proj, asset_id, (targets or [None])[0])
    print(f"replaced {asset_id} with {p} ({c['status']}" + (f": {c['detail']}" if c["detail"] else "") + ")")
    print("affects  " + ", ".join(changed))
    if same:
        print("unchanged " + ", ".join(same))
    if stale:
        print("note     already stale before this change: " + ", ".join(stale))
    if build:
        return cmd_build(proj, changed, changed_only=True, draft=draft)
    return 0


# ----------------------------------------------------------------------------------------------- CLI
def main(argv=None) -> int:
    """Command-line entry point. Returns the exit status."""
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("-p", "--project", default="project.json", help="manifest (default ./project.json)")
    common.add_argument("--work-dir", help="intermediate files (default: work/ next to the manifest)")
    common.add_argument("--cache-dir", help="downloads cache (default: .atr-cache/ next to the manifest)")
    common.add_argument("--out-dir", help="deliverables (default: out/ next to the manifest)")
    ap = argparse.ArgumentParser(prog="project.py", formatter_class=argparse.RawDescriptionHelpFormatter,
                                 description="Keep ATR deliverables in step with one project manifest: scoped "
                                             "edits, changed-only rebuilds and exports, QA evidence.",
                                 epilog="Exit status: 0 done, 1 usage or manifest error, 2 refused, 3 a check "
                                        "failed.")
    sub = ap.add_subparsers(dest="cmd")
    i = sub.add_parser("init", help="create a project folder with project.json")
    i.add_argument("folder")
    i.add_argument("--example", help="copy a shipped example (workshop)")
    i.add_argument("--name")
    i.add_argument("--force", action="store_true")
    s = sub.add_parser("status", parents=[common], help="readiness of every artifact")
    s.add_argument("--json", action="store_true")
    st = sub.add_parser("set", parents=[common], help="set a fact and show what it affects")
    st.add_argument("fact")
    st.add_argument("value")
    st.add_argument("--artifact", help="set the fact for this artifact only")
    b = sub.add_parser("build", parents=[common], help="build artifacts from their specs")
    b.add_argument("--artifact", action="append", help="artifact name(s), comma-separated or repeated")
    b.add_argument("--changed-only", action="store_true", help="skip artifacts whose inputs did not change")
    b.add_argument("--draft", action="store_true", help="allow [placeholders] (a draft, not for sharing)")
    b.add_argument("--no-lint", action="store_true")
    e = sub.add_parser("export", parents=[common], help="PDF, inspection, QR check, renders and qa-report.md")
    e.add_argument("--artifact", action="append")
    e.add_argument("--changed-only", action="store_true",
                   help="only artifacts rebuilt since their last export, and only their changed pages")
    e.add_argument("--dpi", type=int, default=150)
    e.add_argument("--check-reachable", action="store_true", help="one HTTP GET to each QR destination")
    e.add_argument("--zip", action="store_true", help="also write <name>-deliverables.zip")
    r = sub.add_parser("replace-asset", parents=[common], help="point an asset at a new file and rebuild users")
    r.add_argument("asset_id")
    r.add_argument("path", help="new file, or official:<id> (scripts/official_assets.py)")
    r.add_argument("--scope", help="only these artifacts (comma-separated); default every artifact")
    r.add_argument("--no-build", action="store_true")
    r.add_argument("--draft", action="store_true")
    a = ap.parse_args(argv)
    if not a.cmd:
        ap.print_help()
        return 1
    try:
        if a.cmd == "init":
            return cmd_init(a.folder, a.example, a.name, a.force)
        proj = Project(a.project, a.work_dir, a.cache_dir, a.out_dir)
        if a.cmd == "status":
            st_ = project_status(proj)
            if a.json:
                print(json.dumps(st_, indent=2, ensure_ascii=False))
            else:
                _print_status(st_)
            return 0
        if a.cmd == "set":
            return cmd_set(proj, a.fact, a.value, a.artifact)
        if a.cmd == "build":
            return cmd_build(proj, a.artifact, a.changed_only, a.draft, not a.no_lint)
        if a.cmd == "export":
            return cmd_export(proj, a.artifact, a.changed_only, a.dpi, a.check_reachable, a.zip)
        if a.cmd == "replace-asset":
            return cmd_replace_asset(proj, a.asset_id, a.path, a.scope, not a.no_build, a.draft)
    except Refused as exc:
        print(f"project.py: refused: {exc}", file=sys.stderr)
        return 2
    except ProjectError as exc:
        print(f"project.py: {exc}", file=sys.stderr)
        return 1
    return 1


if __name__ == "__main__":
    sys.exit(main())
