#!/usr/bin/env python3
"""Official Kent State wordmark files: list, fetch, verify and locate them.

The skill ships a *working copy* of the Kent State Stacked wordmark (assets/logos/ksu/, colors corrected,
still old raster artwork) for drafts. Anything shared, printed or published needs Kent State's official
file. Kent State publishes the files at https://www.kent.edu/brand/logos but grants no redistribution
license, so the skill ships only a manifest, assets/logos/ksu/official-sources.json: for every variant the
lab uses, the source page, exact download URL, archive member, SHA-256, size and minimum size. This script
downloads the archive, takes out the member, checks its SHA-256 and keeps it in a cache outside the skill:
    ${ATR_DESIGN_CACHE:-~/.cache/atr-lab-design}/official/

Usage (paths relative to the skill root):
    python3 scripts/official_assets.py list                        # ids, variants, sizes, cached or not
    python3 scripts/official_assets.py fetch ksu-stacked-white-png # one file (prints its cached path)
    python3 scripts/official_assets.py fetch all                   # every file in the manifest
    python3 scripts/official_assets.py fetch ksu-stacked-color-png --archive ~/Downloads/Stacked.zip
                                                                   # use an archive you downloaded yourself
    python3 scripts/official_assets.py path ksu-stacked-color-png  # cached path, or the fetch command to run
    python3 scripts/official_assets.py verify some-logo.png        # is this file an official one? (exact SHA-256)
Options: --cache-dir DIR (default above), --manifest FILE (another manifest), --json (machine-readable).

A failed download is a network problem, not evidence that the artwork is unavailable: the script retries
with backoff, then looks for the archive link on the source page, and says what to try next.

Ids: ksu-<stacked|horizontal>-<color|white|reverse-gold|blue>-<png|eps>, plus ksu-<lockup>-color-cmyk-eps.
color = two-color on white or mist; white = all-white reverse on navy; reverse-gold = white with a gold
sunburst on navy; blue = All Blue (the only version for a gold background). PNGs are 300 ppi rasters
(Stacked 1022 x 976 px, Horizontal 1792 x 523 px); EPS files are the vector masters for print.

Module use (scripts/ on sys.path):
    import official_assets as oa
    oa.manifest()                  # the manifest dict
    oa.fetch("ksu-stacked-white-png")   # -> Path in the cache (downloads once, verifies SHA-256)
    oa.verify("logo.png")          # -> {"id": ..., "asset": {...}} for an exact SHA-256 match, else None
    oa.identify(data_bytes)        # -> official / working-copy / unknown, used by brand_check.py

Exit status: 0 = done (verify: the file is official; path: the file is cached),
             1 = no match (verify), not cached yet (path), or a downloaded file failed its checksum,
             2 = could not run (unknown id, unreadable manifest or file, bad archive),
             3 = network failure after retries (try again; see the message).
Standard library only; Pillow (optional) adds pixel-level matching in identify().
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import re
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path
from typing import Dict, Iterable, List, Optional

sys.dont_write_bytecode = True  # keep the skill folder free of __pycache__

SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KSU_DIR = os.path.join(SKILL_ROOT, "assets", "logos", "ksu")
MANIFEST_PATH = os.path.join(KSU_DIR, "official-sources.json")
# The skill's own working copies of the Stacked wordmark (old raster artwork, colors corrected).
# name -> (path in the skill, the official file that replaces it)
WORKING_COPIES = {
    "ksu-wordmark-color.png": ("assets/logos/ksu/ksu-wordmark-color.png", "ksu-stacked-color-png"),
    "ksu-wordmark-white.png": ("assets/logos/ksu/ksu-wordmark-white.png", "ksu-stacked-white-png"),
}
USER_AGENT = "atr-lab-design-official-assets/1.0 (+https://www.kent.edu/brand/logos)"
RETRIES = 3
BACKOFF_S = (2.0, 5.0, 10.0)
TIMEOUT_S = 60
MAX_ARCHIVE_BYTES = 200 * 1024 * 1024
SCRIPT = "python3 scripts/official_assets.py"


class OfficialAssetError(Exception):
    """A problem that stops a command (exit status 2 unless a subclass says otherwise)."""

    exit_code = 2


class NetworkError(OfficialAssetError):
    """A download failed after every retry. Not evidence that the artwork is unavailable."""

    exit_code = 3


class ChecksumError(OfficialAssetError):
    """A file did not match the SHA-256 recorded in the manifest."""

    exit_code = 1


# --------------------------------------------------------------------------- manifest

_MANIFEST_CACHE: Dict[str, dict] = {}


def manifest(path: Optional[str] = None) -> dict:
    """Load the official-sources manifest (default: assets/logos/ksu/official-sources.json)."""
    p = os.path.abspath(path or MANIFEST_PATH)
    if p not in _MANIFEST_CACHE:
        try:
            with open(p, encoding="utf-8") as f:
                data = json.load(f)
        except OSError as e:
            raise OfficialAssetError(f"Cannot read the manifest {p}: {e}") from e
        except ValueError as e:
            raise OfficialAssetError(f"The manifest {p} is not valid JSON: {e}") from e
        if not isinstance(data, dict) or not isinstance(data.get("assets"), list):
            raise OfficialAssetError(f"The manifest {p} has no 'assets' list.")
        _MANIFEST_CACHE[p] = data
    return _MANIFEST_CACHE[p]


def assets(man: Optional[dict] = None) -> List[dict]:
    """Every asset entry of a manifest, in manifest order."""
    return list((man or manifest())["assets"])


def get_asset(asset_id: str, man: Optional[dict] = None) -> dict:
    """The manifest entry for one id; raises OfficialAssetError (with the valid ids) if unknown."""
    for a in assets(man):
        if a.get("id") == asset_id:
            return a
    ids = ", ".join(a.get("id", "?") for a in assets(man))
    raise OfficialAssetError(f"Unknown asset id '{asset_id}'. Known ids: {ids}.")


def resolve_cache_dir(override: Optional[str] = None) -> Path:
    """The cache folder: --cache-dir, else ${ATR_DESIGN_CACHE:-~/.cache/atr-lab-design}/official."""
    if override:
        return Path(os.path.expanduser(override))
    base = os.environ.get("ATR_DESIGN_CACHE") or os.path.join("~", ".cache", "atr-lab-design")
    return Path(os.path.expanduser(base)) / "official"


def file_name(asset: dict) -> str:
    """Cached file name for an asset: its id without the trailing format tag, plus the extension."""
    aid, fmt = asset["id"], asset.get("format", "bin")
    stem = re.sub(r"-(png|eps|pdf|svg|jpg)$", "", aid)
    return f"{stem}.{fmt}"


def cached_path(asset_id: str, cache: Optional[str] = None, man: Optional[dict] = None) -> Path:
    """Where the asset lives (or will live) in the cache. Does not check that it exists."""
    return resolve_cache_dir(cache) / file_name(get_asset(asset_id, man))


def fetch_command(asset_id: str) -> str:
    """The command that fetches one asset."""
    return f"{SCRIPT} fetch {asset_id}"


# --------------------------------------------------------------------------- checksums

def sha256_bytes(data: bytes) -> str:
    """Hex SHA-256 of bytes."""
    return hashlib.sha256(data).hexdigest()


def sha256_file(path) -> str:
    """Hex SHA-256 of a file, read in chunks."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def pixel_sha256(data: bytes) -> Optional[str]:
    """SHA-256 of the decoded RGBA pixels (same artwork re-saved by another app); None without Pillow."""
    try:
        from PIL import Image
    except ImportError:  # pragma: no cover
        return None
    try:
        im = Image.open(io.BytesIO(data))
        im.load()
        return sha256_bytes(im.convert("RGBA").tobytes())
    except Exception:
        return None


def lookup_sha256(digest: str, man: Optional[dict] = None) -> Optional[dict]:
    """The manifest entry whose file SHA-256 equals digest, else None."""
    digest = digest.lower()
    for a in assets(man):
        if str(a.get("sha256", "")).lower() == digest:
            return a
    return None


def verify(path, man: Optional[dict] = None) -> Optional[dict]:
    """Exact SHA-256 match of a file against the manifest.

    Returns {"id", "sha256", "asset", "match": "sha256"} for an official file, else None."""
    digest = sha256_file(path)
    a = lookup_sha256(digest, man)
    if a is None:
        return None
    return {"id": a["id"], "sha256": digest, "asset": a, "match": "sha256"}


# --------------------------------------------------------------------------- overrides and identification

def load_overrides(paths: Optional[Iterable[str]]) -> List[dict]:
    """Extra official references the user vouches for (brand_check.py --official-manifest).

    Each path may be: a manifest in this script's schema ({"assets": [...]}); a provenance map like
    {"name.png": {"sha256": ..., "source": ...}, ...} (what a project records after downloading); or an
    image file itself, whose SHA-256 is then trusted as official. Returns a list of
    {"id", "sha256", "pixel_sha256" (optional), "source"}."""
    out: List[dict] = []
    for p in paths or []:
        if not os.path.isfile(p):
            raise OfficialAssetError(f"Official manifest override not found: {p}")
        with open(p, "rb") as f:
            data = f.read()
        parsed = None
        if p.lower().endswith(".json"):
            try:
                parsed = json.loads(data.decode("utf-8"))
            except ValueError as e:
                raise OfficialAssetError(f"{p} is not valid JSON: {e}") from e
        if parsed is None:  # an image (or any file): trust its exact bytes
            out.append({"id": os.path.basename(p), "sha256": sha256_bytes(data),
                        "pixel_sha256": pixel_sha256(data), "source": p})
            continue
        if isinstance(parsed, dict) and isinstance(parsed.get("assets"), list):
            for a in parsed["assets"]:
                if isinstance(a, dict) and a.get("sha256"):
                    out.append({"id": a.get("id") or a.get("member") or "override", "sha256": a["sha256"].lower(),
                                "pixel_sha256": a.get("pixel_sha256"), "source": p})
        elif isinstance(parsed, dict):
            for name, rec in parsed.items():
                if isinstance(rec, dict) and rec.get("sha256"):
                    out.append({"id": name, "sha256": str(rec["sha256"]).lower(),
                                "pixel_sha256": rec.get("pixel_sha256"), "source": p})
        else:
            raise OfficialAssetError(f"{p}: expected a JSON object (manifest or provenance map).")
    return out


_WORKING: Optional[List[dict]] = None


def working_copies() -> List[dict]:
    """The skill's working-copy wordmark files with their file and pixel SHA-256 (computed once)."""
    global _WORKING
    if _WORKING is None:
        _WORKING = []
        for name, (rel, official) in WORKING_COPIES.items():
            p = os.path.join(SKILL_ROOT, rel)
            if os.path.isfile(p):
                with open(p, "rb") as f:
                    data = f.read()
                _WORKING.append({"id": name, "path": rel, "replacement": official, "sha256": sha256_bytes(data),
                                 "pixel_sha256": pixel_sha256(data)})
    return _WORKING


def identify(data: bytes, overrides: Optional[List[dict]] = None, man: Optional[dict] = None,
             pixels: bool = True) -> dict:
    """Provenance of image bytes: never guessed from looks, only from exact matches.

    Returns {"status": "official" | "working-copy" | "unknown", "id": str|None, "how": "sha256" |
    "pixels" | None, "asset": manifest entry or None, "source": str|None, "replacement": official id for
    a working copy, else None}.
    official: the file's SHA-256 equals a manifest entry or an override; with pixels=True, also when the
    decoded pixels are identical to an official PNG (the same file re-saved by an office app).
    working-copy: the bytes or pixels equal the skill's assets/logos/ksu/ksu-wordmark-*.png."""
    digest = sha256_bytes(data)
    try:
        man = man or manifest()
    except OfficialAssetError:
        man = {"assets": []}
    a = lookup_sha256(digest, man)
    if a is not None:
        return {"status": "official", "id": a["id"], "how": "sha256", "asset": a, "source": "manifest"}
    for o in overrides or []:
        if o["sha256"] == digest:
            return {"status": "official", "id": o["id"], "how": "sha256", "asset": None, "source": o["source"]}
    for w in working_copies():
        if w["sha256"] == digest:
            return {"status": "working-copy", "id": w["id"], "how": "sha256", "asset": None, "source": w["path"],
                    "replacement": w["replacement"]}
    if pixels:
        px = pixel_sha256(data)
        if px:
            for a in assets(man):
                if a.get("pixel_sha256") == px:
                    return {"status": "official", "id": a["id"], "how": "pixels", "asset": a, "source": "manifest"}
            for o in overrides or []:
                if o.get("pixel_sha256") == px:
                    return {"status": "official", "id": o["id"], "how": "pixels", "asset": None,
                            "source": o["source"]}
            for w in working_copies():
                if w["pixel_sha256"] == px:
                    return {"status": "working-copy", "id": w["id"], "how": "pixels", "asset": None,
                            "source": w["path"], "replacement": w["replacement"]}
    return {"status": "unknown", "id": None, "how": None, "asset": None, "source": None}




# --------------------------------------------------------------------------- downloading

def _ssl_context():
    try:
        import ssl
        try:
            import certifi  # type: ignore
            return ssl.create_default_context(cafile=certifi.where())
        except ImportError:
            return ssl.create_default_context()
    except Exception:  # pragma: no cover
        return None


def _download_once(url: str, dest: Path) -> None:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=TIMEOUT_S, context=_ssl_context()) as r:  # noqa: S310 (https only)
        total = 0
        with open(dest, "wb") as f:
            while True:
                chunk = r.read(1 << 20)
                if not chunk:
                    break
                total += len(chunk)
                if total > MAX_ARCHIVE_BYTES:
                    raise OfficialAssetError(f"{url} is larger than {MAX_ARCHIVE_BYTES >> 20} MB; refusing it.")
                f.write(chunk)


def download(url: str, dest: Path, retries: int = RETRIES, log=None) -> None:
    """Download url to dest with retries and backoff. Raises NetworkError after the last attempt."""
    if not url.lower().startswith("https://"):
        raise OfficialAssetError(f"Refusing a non-https download URL: {url}")
    dest.parent.mkdir(parents=True, exist_ok=True)
    last = None
    for attempt in range(1, retries + 1):
        tmp = dest.with_name(dest.name + ".part")
        try:
            _download_once(url, tmp)
            os.replace(tmp, dest)
            return
        except OfficialAssetError:
            raise
        except (urllib.error.URLError, OSError, TimeoutError) as e:  # HTTPError is a URLError
            last = e
            if tmp.exists():
                tmp.unlink()
            if attempt < retries:
                wait = BACKOFF_S[min(attempt - 1, len(BACKOFF_S) - 1)]
                if log:
                    log(f"  download attempt {attempt}/{retries} failed ({_describe(e)}); retrying in {wait:g} s")
                time.sleep(wait)
    raise NetworkError(f"Could not download {url} after {retries} attempts (last error: {_describe(last)}).")


def _describe(e) -> str:
    if isinstance(e, urllib.error.HTTPError):
        return f"HTTP {e.code} {e.reason}"
    if isinstance(e, urllib.error.URLError):
        r = e.reason
        if "CERTIFICATE" in str(r).upper():
            return (f"{r}; this Python has no CA certificates: pip install certifi, or run "
                    "'Install Certificates.command' from the python.org installer")
        return str(r)
    return f"{type(e).__name__}: {e}"


def discover_archive_urls(source_page: str, keyword: str) -> List[str]:
    """Archive links on the source page whose URL contains keyword (case-insensitive). Network."""
    req = urllib.request.Request(source_page, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=TIMEOUT_S, context=_ssl_context()) as r:  # noqa: S310
        html = r.read(5 * 1024 * 1024).decode("utf-8", "replace")
    out = []
    for href in re.findall(r'href="([^"]+\.zip)"', html, flags=re.I):
        url = urllib.parse.urljoin(source_page, href.replace("&amp;", "&"))
        if keyword.lower() in urllib.parse.unquote_plus(url).lower() and url not in out:
            out.append(url)
    return out


def _archive_path(name: str, cache: Path) -> Path:
    return cache / "archives" / f"{name}.zip"


def get_archive(name: str, man: dict, cache: Path, log=None, archive_override: Optional[str] = None) -> Path:
    """A local copy of one archive: --archive, the cached copy, the manifest URL, or a link found on the
    source page, in that order. Raises NetworkError with next steps if every download fails."""
    if archive_override:
        p = Path(os.path.expanduser(archive_override))
        if not p.is_file():
            raise OfficialAssetError(f"Archive not found: {p}")
        return p
    arch = man.get("archives", {}).get(name)
    if not arch:
        raise OfficialAssetError(f"The manifest has no archive '{name}'.")
    dest = _archive_path(name, cache)
    if dest.is_file() and zipfile.is_zipfile(dest):
        return dest
    if log:
        log(f"Downloading the official '{name}' archive from {arch['url']}")
    errors = []
    try:
        download(arch["url"], dest, log=log)
        return dest
    except NetworkError as e:
        errors.append(str(e))
    page = arch.get("source_page") or man.get("source_page")
    if page:
        try:
            found = [u for u in discover_archive_urls(page, name) if u != arch["url"]]
        except (urllib.error.URLError, OSError, TimeoutError) as e:
            found = []
            errors.append(f"Could not read the source page {page} ({_describe(e)}).")
        for u in found:
            if log:
                log(f"  trying the link found on {page}: {u}")
            try:
                download(u, dest, log=log)
                return dest
            except NetworkError as e:
                errors.append(str(e))
    raise NetworkError(
        " ".join(errors) + "\nThis is a download problem, not evidence that the official artwork is unavailable: "
        f"Kent State links the archive from {page or arch['url']}. Next steps: run the same command again "
        "in a minute; check the network, VPN or proxy; or open the source page in a browser, download the "
        f"'{name}' archive yourself and run: {SCRIPT} fetch <id> --archive <downloaded.zip>")


def fetch(asset_id: str, cache_dir: Optional[str] = None, man: Optional[dict] = None, log=None,
          archive: Optional[str] = None, force: bool = False) -> Path:
    """Download (once), extract and verify one official asset; returns its path in the cache.

    A cached file is reused only if its SHA-256 still matches. The archive member is checked against the
    manifest SHA-256 before anything is written, so the cache never holds an unverified file."""
    man = man or manifest()
    a = get_asset(asset_id, man)
    cache = resolve_cache_dir(cache_dir)
    dest = cache / file_name(a)
    if not force and dest.is_file() and sha256_file(dest) == a["sha256"].lower():
        return dest
    zpath = get_archive(a["archive"], man, cache, log=log, archive_override=archive)
    try:
        with zipfile.ZipFile(zpath) as z:
            try:
                data = z.read(a["member"])
            except KeyError:
                raise OfficialAssetError(
                    f"{zpath} has no member '{a['member']}'. Kent State may have reorganized the archive: "
                    f"check {man.get('source_page')} and update assets/logos/ksu/official-sources.json.") from None
    except zipfile.BadZipFile as e:
        if not archive:
            try:
                zpath.unlink()
            except OSError:
                pass
        raise OfficialAssetError(f"{zpath} is not a valid zip archive ({e}); run the command again.") from e
    got = sha256_bytes(data)
    if got != a["sha256"].lower():
        raise ChecksumError(
            f"{a['member']} has SHA-256 {got}, but the manifest expects {a['sha256']}. Kent State may have "
            "updated the artwork: compare it with the source page, then update the manifest entry (sha256, "
            "bytes, pixels, retrieved) if the new file is the official one. Nothing was cached.")
    dest.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(dest.parent), prefix=".tmp-", suffix="." + a.get("format", "bin"))
    with os.fdopen(fd, "wb") as f:
        f.write(data)
    os.replace(tmp, dest)
    return dest


def fetch_many(ids: List[str], cache_dir: Optional[str] = None, man: Optional[dict] = None, log=None,
               archive: Optional[str] = None, force: bool = False) -> Dict[str, Path]:
    """fetch() for several ids; each archive is downloaded at most once."""
    return {i: fetch(i, cache_dir, man, log=log, archive=archive, force=force) for i in ids}


def path(asset_id: str, cache_dir: Optional[str] = None, man: Optional[dict] = None) -> Optional[Path]:
    """The cached, verified path of an asset, or None if it is not cached (or no longer matches)."""
    man = man or manifest()
    a = get_asset(asset_id, man)
    p = resolve_cache_dir(cache_dir) / file_name(a)
    if p.is_file() and sha256_file(p) == a["sha256"].lower():
        return p
    return None


# --------------------------------------------------------------------------- CLI

def _size(a: dict) -> str:
    if a.get("pixels"):
        return f"{a['pixels'][0]} x {a['pixels'][1]} px"
    if a.get("size_pt"):
        return f"vector {a['size_pt'][0] / 72:.2f} x {a['size_pt'][1] / 72:.2f} in"
    return ""


def _err(msg: str) -> None:
    print(f"official_assets.py: {msg}", file=sys.stderr)


def main(argv=None) -> int:
    """Command-line entry point; returns the exit status."""
    ap = argparse.ArgumentParser(
        prog="official_assets.py",
        description="List, fetch, verify and locate the official Kent State wordmark files recorded in "
                    "assets/logos/ksu/official-sources.json.",
        epilog="Exit status: 0 done, 1 no match / not cached / checksum mismatch, 2 could not run, "
               "3 network failure after retries (a failed download does not mean the artwork is unavailable).")
    ap.add_argument("--manifest", help="manifest to use instead of assets/logos/ksu/official-sources.json")
    ap.add_argument("--cache-dir", help="cache folder (default ${ATR_DESIGN_CACHE:-~/.cache/atr-lab-design}/official)")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    sub = ap.add_subparsers(dest="cmd", metavar="command")
    sub.add_parser("list", help="every official asset with variant, size and cache state")
    pf = sub.add_parser("fetch", help="download, extract and verify assets into the cache")
    pf.add_argument("ids", nargs="+", metavar="id|all")
    pf.add_argument("--archive", help="use this already-downloaded archive instead of the network")
    pf.add_argument("--force", action="store_true", help="extract again even if the cached file matches")
    pv = sub.add_parser("verify", help="exact SHA-256 check of files against the manifest")
    pv.add_argument("files", nargs="+")
    pp = sub.add_parser("path", help="cached path of an asset, or the command that fetches it")
    pp.add_argument("id")
    # subcommand options may also come before the command
    for p in (pf, pv, pp):
        p.add_argument("--cache-dir", dest="cache_dir_sub", help=argparse.SUPPRESS)
        p.add_argument("--json", dest="json_sub", action="store_true", help=argparse.SUPPRESS)
    opts = ap.parse_args(argv)
    if not opts.cmd:
        ap.print_help()
        return 2
    cdir = getattr(opts, "cache_dir_sub", None) or opts.cache_dir
    as_json = opts.json or getattr(opts, "json_sub", False)
    try:
        man = manifest(opts.manifest)
        if opts.cmd == "list":
            rows = []
            for a in assets(man):
                p = path(a["id"], cdir, man)
                rows.append({"id": a["id"], "lockup": a.get("lockup"), "variant": a.get("variant"),
                             "format": a.get("format"), "size": _size(a), "background": a.get("background"),
                             "cached": str(p) if p else None})
            if as_json:
                print(json.dumps({"cache_dir": str(resolve_cache_dir(cdir)), "assets": rows}, indent=2))
            else:
                print(f"Official Kent State wordmarks (source: {man.get('source_page')}; "
                      f"cache: {resolve_cache_dir(cdir)})")
                for r in rows:
                    state = "cached" if r["cached"] else "not cached"
                    print(f"  {r['id']:<34} {r['format']:<4} {r['size']:<22} on {r['background']:<32} {state}")
                print(f"Fetch: {SCRIPT} fetch <id|all>")
            return 0
        if opts.cmd == "fetch":
            ids = [a["id"] for a in assets(man)] if opts.ids == ["all"] else opts.ids
            for i in ids:
                get_asset(i, man)  # fail early on a typo
            log = (lambda m: print(m, file=sys.stderr))
            got = fetch_many(ids, cdir, man, log=log, archive=opts.archive, force=opts.force)
            if as_json:
                print(json.dumps({k: str(v) for k, v in got.items()}, indent=2))
            else:
                for k, v in got.items():
                    print(f"{k}: {v}  (SHA-256 verified)")
            return 0
        if opts.cmd == "verify":
            status, out = 0, []
            for f in opts.files:
                if not os.path.isfile(f):
                    _err(f"no such file: {f}")
                    status = 2
                    continue
                v = verify(f, man)
                if v:
                    out.append({"file": f, "official": True, "id": v["id"], "sha256": v["sha256"]})
                else:
                    status = max(status, 1)
                    ident = identify(open(f, "rb").read(), man=man, pixels=True)
                    out.append({"file": f, "official": False, "sha256": sha256_file(f),
                                "status": ident["status"], "id": ident["id"], "how": ident["how"],
                                "replacement": ident.get("replacement")})
            if as_json:
                print(json.dumps(out[0] if len(out) == 1 else out, indent=2))
            else:
                for r in out:
                    if r["official"]:
                        print(f"{r['file']}: official Kent State wordmark, verified ({r['id']}, exact SHA-256).")
                    elif r["status"] == "official":
                        print(f"{r['file']}: same pixels as the official {r['id']}, but not the same file "
                              "(re-saved). Use the fetched original for print.")
                    elif r["status"] == "working-copy":
                        print(f"{r['file']}: the skill's working copy ({r['id']}), not the official file. "
                              f"Fetch the official one: {fetch_command(r['replacement'])}")
                    else:
                        print(f"{r['file']}: not one of the official files in the manifest (SHA-256 "
                              f"{r['sha256'][:16]}...), so its provenance is not verified. List the official "
                              f"files with: {SCRIPT} list")
            return status
        if opts.cmd == "path":
            p = path(opts.id, cdir, man)
            if as_json:
                print(json.dumps({"id": opts.id, "path": str(p) if p else None,
                                  "fetch": None if p else fetch_command(opts.id)}))
            elif p:
                print(p)
            else:
                print(f"{opts.id} is not cached yet. Run: {fetch_command(opts.id)}", file=sys.stderr)
            return 0 if p else 1
    except OfficialAssetError as e:
        _err(str(e))
        return e.exit_code
    return 2


if __name__ == "__main__":
    sys.exit(main())
