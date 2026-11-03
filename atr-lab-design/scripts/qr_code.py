#!/usr/bin/env python3
"""qr_code.py - make, decode and verify ATR Lab QR codes at an exact printed size.

Make a QR code as a PNG that is exactly the physical size you ask for (quiet zone included), check it decodes,
and then check the code again where it matters: in the final exported PDF. The destination is encoded exactly as
given. This script never adds tracking parameters, never shortens or "cleans" a URL and never substitutes a
different one; if you want UTM tags, put them in the URL you pass.

Rules it enforces (references/web-and-digital.md section 9, references/posters.md section 8):
  - dark modules navy #003976 or black #000000 on a white #FFFFFF background; gold, low-contrast and inverted
    codes are refused
  - a quiet zone of at least 4 modules on every side, inside the image (the PNG may carry a little more white
    so that its pixel size is exact)
  - at least 0.8 in wide, quiet zone included (handouts and flyers); larger for posters and banners
  - error correction M by default (L, M, Q or H on request)

Usage (from the skill root, atr-lab-design/):
  python3 scripts/qr_code.py make "https://example.org/register" -o qr.png --size-in 1.25 [--dpi 600]
         [--ecc M] [--color navy|black] [--json]
  python3 scripts/qr_code.py decode qr.png [more.png ...] [--json]
  python3 scripts/qr_code.py verify flyer.pdf --url "https://example.org/register" [--pages 1,3-4] [--dpi 200]
         [--require-link] [--check-reachable] [--json]

`make` prints the printed fallback (the address to print under the code) and the alt text to use.
`verify` renders the PDF pages (poppler pdftoppm), decodes every QR code on them, compares each decoded value to
--url character for character, and reads the PDF's link annotations. --check-reachable then makes one HTTP GET and
reports it separately: "the page answered" is not "a form was submitted".

Exit status: 0 done / verified; 1 usage or environment error (missing package, missing pdftoppm, bad file);
2 refused (colors, quiet zone, size, URL with spaces); 3 verification failed (no QR, a different value, a
modified link) or, with --check-reachable, the page did not answer with a 2xx/3xx status.

Requires qrcode[pil] (make), zxing-cpp (decode, verify), pypdf (link annotations) and Pillow:
  .venv/bin/pip install "qrcode[pil]>=7.4" "zxing-cpp>=2.2" "pypdf>=4.0"
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import argparse  # noqa: E402
import datetime as _dt  # noqa: E402
import json  # noqa: E402
import re  # noqa: E402
import tempfile  # noqa: E402
from pathlib import Path  # noqa: E402
from urllib.parse import parse_qsl, urlsplit  # noqa: E402

HERE = Path(__file__).resolve().parent

NAVY = "#003976"
BLACK = "#000000"
WHITE = "#FFFFFF"
ALLOWED_DARK = {"navy": NAVY, "black": BLACK}
MIN_QUIET = 4
MIN_SIZE_IN = 0.8
ECC_LEVELS = ("L", "M", "Q", "H")
TRACKING_KEYS = ("utm_", "fbclid", "gclid", "mc_cid", "mc_eid", "_hsenc", "_hsmi", "igshid")
SHORTENERS = ("forms.gle", "bit.ly", "tinyurl.com", "t.co", "goo.gl", "ow.ly", "buff.ly", "rebrand.ly", "cutt.ly")


class QRError(Exception):
    """A request the QR rules refuse (colors, quiet zone, size, URL); exit status 2 on the command line."""


# ----------------------------------------------------------------------------------------------- helpers
def _norm_hex(value: str) -> str:
    """Return '#RRGGBB' for a token name (navy, black, white) or a hex color."""
    v = str(value).strip().lower()
    names = {"navy": NAVY, "black": BLACK, "white": WHITE, "gold": "#EFAB00"}
    if v in names:
        return names[v]
    if re.fullmatch(r"#?[0-9a-f]{3}", v):
        v = v.lstrip("#")
        v = "".join(c * 2 for c in v)
    v = v.lstrip("#")
    if not re.fullmatch(r"[0-9a-f]{6}", v):
        raise QRError(f"'{value}' is not a color; use navy, black or a #RRGGBB hex value")
    return "#" + v.upper()


def _rgb(hex_color: str) -> tuple:
    h = hex_color.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _luminance(rgb) -> float:
    def lin(c):
        c = c / 255.0
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (lin(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a: str, b: str) -> float:
    """WCAG contrast ratio between two hex colors."""
    la, lb = _luminance(_rgb(a)), _luminance(_rgb(b))
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def check_colors(dark: str, light: str) -> tuple:
    """Return (dark, light) as '#RRGGBB' or raise QRError: navy or black modules on white only."""
    d, lt = _norm_hex(dark), _norm_hex(light)
    if _luminance(_rgb(d)) > _luminance(_rgb(lt)):
        raise QRError(f"inverted code refused: dark modules {d} are lighter than the background {lt}. "
                      "Use navy or black modules on white; many phones cannot read light-on-dark codes")
    if lt != WHITE:
        raise QRError(f"background {lt} refused: the light modules and quiet zone must be white #FFFFFF "
                      "(place the white code on a navy or photo panel instead of tinting it)")
    if d not in ALLOWED_DARK.values():
        raise QRError(f"module color {d} refused (contrast {contrast(d, lt):.1f}:1 on white): use navy {NAVY} "
                      f"or black {BLACK}. Gold and tints fail on many phones")
    return d, lt


def check_url(url: str) -> str:
    """Return the URL unchanged, or raise QRError if it is empty or has spaces or control characters.

    The value is never rewritten: no trimming of slashes, no added parameters, no scheme changes."""
    if not isinstance(url, str) or not url:
        raise QRError("the QR destination is empty")
    if url != url.strip() or re.search(r"\s", url) or any(ord(c) < 32 for c in url):
        raise QRError(f"the QR destination {url!r} contains spaces or line breaks; pass the exact address")
    if re.match(r"^\[.*\]$", url) or "[" in url or "]" in url:
        raise QRError(f"the QR destination {url!r} is still a [placeholder]")
    return url


def url_notes(url: str) -> list:
    """Plain-English notes about a destination (shortener, tracking parameters, http). Never changes it."""
    notes = []
    parts = urlsplit(url)
    if parts.scheme == "http":
        notes.append("the address uses http://, not https://; confirm it with the page owner")
    elif parts.scheme not in ("https", "mailto", "tel"):
        notes.append(f"the address has no https:// scheme ({parts.scheme or 'none'}); phones may treat it as text")
    host = (parts.hostname or "").lower()
    if host in SHORTENERS:
        notes.append(f"{host} is a link shortener; Kent State guidance prefers the full address, but an explicitly "
                     "supplied link is kept as given")
    keys = [k for k, _ in parse_qsl(parts.query, keep_blank_values=True)]
    tracked = [k for k in keys if k.lower().startswith(TRACKING_KEYS)]
    if tracked:
        notes.append("the address carries tracking parameters (" + ", ".join(tracked) + "); they were supplied "
                     "with it and are encoded as given")
    return notes


def fallback_text(url: str) -> str:
    """The address to print under the code: the exact URL without its https:// prefix.

    Everything after the scheme (host, www., path, query) is kept, so the printed text leads to the same page."""
    for prefix in ("https://", "http://"):
        if url.startswith(prefix):
            return url[len(prefix):]
    if url.startswith("mailto:"):
        return url[len("mailto:"):]
    return url


def alt_text(url: str, destination: str = "", where: str = "below it") -> str:
    """Alt text for a placed code: 'QR code to <destination>; the address <printed> is printed below it.'"""
    dest = destination.strip() or fallback_text(url)
    return f"QR code to {dest}; the address {fallback_text(url)} is printed {where}."


def _qrcode():
    try:
        import qrcode  # noqa: F401
        from qrcode import constants
        return qrcode, constants
    except ImportError as exc:
        raise RuntimeError("QR generation needs the qrcode package with Pillow: "
                           ".venv/bin/pip install \"qrcode[pil]>=7.4\" (scripts/requirements.txt, group qr)") from exc


def matrix(url: str, ecc: str = "M", quiet: int = MIN_QUIET) -> tuple:
    """Return (rows, version) for the code, rows of booleans including the quiet zone on every side."""
    qrcode, constants = _qrcode()
    level = {"L": constants.ERROR_CORRECT_L, "M": constants.ERROR_CORRECT_M,
             "Q": constants.ERROR_CORRECT_Q, "H": constants.ERROR_CORRECT_H}
    ecc_u = str(ecc).upper()
    if ecc_u not in level:
        raise QRError(f"error correction '{ecc}' is not one of L, M, Q, H (M is the default)")
    q = qrcode.QRCode(error_correction=level[ecc_u], box_size=1, border=int(quiet))
    q.add_data(url)
    q.make(fit=True)
    return q.get_matrix(), q.version


def describe_qr(url: str, size_in: float = 1.0, dpi: int = 600, ecc: str = "M", quiet: int = MIN_QUIET,
                dark: str = NAVY, light: str = WHITE) -> dict:
    """Validate a request and describe the code it makes (version, modules, module size, fallback, alt, notes)."""
    check_url(url)
    d, lt = check_colors(dark, light)
    if int(quiet) < MIN_QUIET:
        raise QRError(f"quiet zone of {quiet} modules refused: the QR standard needs at least {MIN_QUIET}")
    if float(size_in) < MIN_SIZE_IN:
        raise QRError(f"{size_in} in is too small: a printed code, quiet zone included, is at least "
                      f"{MIN_SIZE_IN} in wide (and a tenth of the scanning distance)")
    rows, version = matrix(url, ecc, quiet)
    n = len(rows)
    target = int(round(float(size_in) * int(dpi)))
    module_px = target // n
    if module_px < 2:
        raise QRError(f"{dpi} dpi gives {target} px for {n} modules ({target / n:.1f} px each); raise --dpi")
    return {
        "url": url, "version": version, "ecc": str(ecc).upper(), "quiet_modules": int(quiet),
        "modules_with_quiet_zone": n, "size_in": float(size_in), "dpi": int(dpi), "pixels": target,
        "module_px": module_px, "module_mm": round(float(size_in) * 25.4 / n, 3),
        "dark": d, "light": lt, "contrast": round(contrast(d, lt), 2),
        "scan_distance_max_in": round(float(size_in) * 10, 1),
        "printed_fallback": fallback_text(url), "alt": alt_text(url), "notes": url_notes(url),
    }


# ----------------------------------------------------------------------------------------------- make
def make_qr(url, out_path, size_in=1.0, dpi=600, ecc="M", quiet=MIN_QUIET, dark=NAVY, light=WHITE) -> Path:
    """Write a PNG QR code of exactly size_in x size_in inches at dpi (quiet zone included) and return its path.

    Modules are whole pixels; the few pixels left over after round(size_in * dpi) // modules are added as extra
    white around the code, so the quiet zone is never smaller than `quiet` modules and the file's pixel size and
    dpi tag give the exact physical size. Raises QRError for refused colors, quiet zones, sizes or URLs."""
    from PIL import Image

    info = describe_qr(url, size_in, dpi, ecc, quiet, dark, light)
    rows, _ = matrix(url, ecc, quiet)
    n, m, target = len(rows), info["module_px"], info["pixels"]
    small = Image.new("1", (n, n), 1)
    px = small.load()
    for y, row in enumerate(rows):
        for x, on in enumerate(row):
            if on:
                px[x, y] = 0
    code = small.resize((n * m, n * m), Image.NEAREST)
    canvas = Image.new("RGB", (target, target), _rgb(info["light"]))
    off = (target - n * m) // 2
    dark_img = Image.new("RGB", code.size, _rgb(info["dark"]))
    canvas.paste(dark_img, (off, off), mask=code.point(lambda v: 255 if v == 0 else 0).convert("L"))
    out = Path(out_path).expanduser()
    out.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(str(out), dpi=(int(dpi), int(dpi)), optimize=True)
    return out


# ----------------------------------------------------------------------------------------------- decode
def _zxing():
    try:
        import zxingcpp
        return zxingcpp
    except ImportError as exc:
        raise RuntimeError("QR decoding needs zxing-cpp: .venv/bin/pip install \"zxing-cpp>=2.2\" "
                           "(scripts/requirements.txt, group qr)") from exc


def decode_pil(image) -> list:
    """Decode every QR code in a PIL image; return the decoded strings in reading order."""
    zx = _zxing()
    img = image.convert("L") if image.mode not in ("L", "RGB") else image
    kwargs = {"formats": zx.BarcodeFormat.QRCode}
    try:
        results = zx.read_barcodes(img, text_mode=zx.TextMode.Plain, **kwargs)
    except (AttributeError, TypeError):
        results = zx.read_barcodes(img, **kwargs)
    found = []
    for r in results:
        pos = getattr(r, "position", None)
        key = (pos.top_left.y, pos.top_left.x) if pos is not None else (0, 0)
        found.append((key, r.text))
    return [t for _, t in sorted(found)]


def decode_image(path) -> list:
    """Decode every QR code in an image file; return the decoded strings (empty list if none)."""
    from PIL import Image
    with Image.open(str(path)) as im:
        im.load()
        return decode_pil(im)


# ----------------------------------------------------------------------------------------------- verify
def _link_annotations(pdf_path: Path) -> dict:
    """Return {page_number: [uri, ...]} for every URI link annotation in the PDF (needs pypdf)."""
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise RuntimeError("reading PDF links needs pypdf: .venv/bin/pip install \"pypdf>=4.0\"") from exc
    out = {}
    reader = PdfReader(str(pdf_path))
    for i, page in enumerate(reader.pages, 1):
        uris = []
        for ref in page.get("/Annots") or []:
            annot = ref.get_object()
            if annot.get("/Subtype") != "/Link":
                continue
            action = annot.get("/A")
            action = action.get_object() if action is not None else None
            if action is not None and action.get("/URI") is not None:
                uri = action.get("/URI")
                uris.append(uri.decode("utf-8", "replace") if isinstance(uri, bytes) else str(uri))
        out[i] = uris
    return out


def _near_miss(value: str, expected: str) -> bool:
    """True when value looks like the expected destination but differs (added parameters, other scheme...)."""
    if value == expected:
        return False
    a, b = urlsplit(value), urlsplit(expected)

    def host(parts):
        h = (parts.hostname or "").lower()
        return h[4:] if h.startswith("www.") else h
    same_place = host(a) == host(b) and a.path.rstrip("/") == b.path.rstrip("/")
    return same_place or value.startswith(expected) or expected.startswith(value)


def verify_pdf(pdf_path, expected_url, dpi=200, pages=None) -> dict:
    """Render the PDF pages, decode every QR code and compare each to expected_url exactly; read link annotations.

    pages: None for every page, or a list of 1-based page numbers (or a '1,3-4' string).
    Returns a dict with per-page decoded values and links, 'qr_match' (the expected value was decoded at least
    once), 'qr_mismatches' (codes that decode to anything else), 'link_match' (a link annotation points exactly to
    expected_url), 'link_near_misses' (links to the same page with a different address), 'problems' and 'ok'."""
    import export_office  # same folder; renders with pdftoppm

    pdf = Path(pdf_path).expanduser().resolve()
    check_url(expected_url)
    if not pdf.is_file():
        raise FileNotFoundError(f"no such PDF: {pdf}")
    page_list = export_office.parse_pages(pages, export_office.page_count(pdf)) if pages else None
    links = _link_annotations(pdf)
    result = {"pdf": str(pdf), "expected_url": expected_url, "dpi": int(dpi),
              "checked_at": _dt.datetime.now().astimezone().isoformat(timespec="seconds"),
              "pages": [], "qr_match": False, "qr_mismatches": [], "link_match": False,
              "link_near_misses": [], "problems": [], "ok": False}
    with tempfile.TemporaryDirectory(prefix="atr-qr-verify-") as tmp:
        pngs = export_office.render(pdf, Path(tmp), dpi=dpi, pages=page_list)
        for png in pngs:
            n = int(re.search(r"-page-(\d+)\.png$", png.name).group(1))
            values = decode_image(png)
            page_links = links.get(n, [])
            result["pages"].append({"page": n, "qr": values, "links": page_links})
            for v in values:
                if v == expected_url:
                    result["qr_match"] = True
                else:
                    result["qr_mismatches"].append({"page": n, "value": v})
            for uri in page_links:
                if uri == expected_url:
                    result["link_match"] = True
                elif _near_miss(uri, expected_url):
                    result["link_near_misses"].append({"page": n, "uri": uri})
    if not any(p["qr"] for p in result["pages"]):
        result["problems"].append("no QR code could be decoded from the rendered pages")
    elif not result["qr_match"]:
        result["problems"].append("no QR code on the rendered pages decodes to the expected address")
    for mm in result["qr_mismatches"]:
        extra = ""
        if _near_miss(mm["value"], expected_url):
            extra = " (same page, different address: parameters or scheme changed)"
        result["problems"].append(f"page {mm['page']}: a QR code decodes to {mm['value']!r}, "
                                  f"not {expected_url!r}{extra}")
    for nm in result["link_near_misses"]:
        result["problems"].append(f"page {nm['page']}: a link points to {nm['uri']!r}, a modified form of "
                                  f"{expected_url!r}")
    result["ok"] = not result["problems"]
    return result


def check_reachable(url: str, timeout: float = 15.0) -> dict:
    """One HTTP GET to url (redirects followed). Reports whether the page answered, never that a form worked."""
    import urllib.error
    import urllib.request

    req = urllib.request.Request(url, headers={"User-Agent": "atr-lab-design qr_code.py (reachability check)"})
    out = {"url": url, "checked_at": _dt.datetime.now().astimezone().isoformat(timespec="seconds"),
           "reachable": False, "status": None, "final_url": None, "error": None,
           "meaning": "The page answered an HTTP GET. This does not show that a form can be submitted or that a "
                      "response was recorded; nothing was submitted."}
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:  # noqa: S310 (user-requested check)
            out["status"] = resp.status
            out["final_url"] = resp.geturl()
            out["reachable"] = 200 <= resp.status < 400
    except urllib.error.HTTPError as exc:
        out["status"], out["error"] = exc.code, str(exc)
    except Exception as exc:  # noqa: BLE001 (report any network failure in plain words)
        out["error"] = str(exc)
    if not out["reachable"]:
        out["meaning"] = ("The page did not answer with a success status. Check the address with its owner; a "
                          "network failure here does not prove the page is down for everyone.")
    return out


# ----------------------------------------------------------------------------------------------- CLI
def _print_verify(res: dict) -> None:
    print(f"PDF       {res['pdf']}")
    print(f"expected  {res['expected_url']}")
    for p in res["pages"]:
        qr = ", ".join(repr(v) for v in p["qr"]) or "no QR code"
        print(f"  page {p['page']}: {qr}" + (f"; links: {', '.join(p['links'])}" if p["links"] else ""))
    print(("ok        " if res["qr_match"] else "FAIL      ")
          + ("a QR code in the rendered PDF decodes to exactly the expected address"
             if res["qr_match"] else "the expected address was not decoded from the rendered PDF"))
    print(("ok        " if res["link_match"] else "note      ")
          + ("a PDF link annotation points to exactly the expected address" if res["link_match"]
             else "no PDF link annotation points to the expected address (the code still scans; "
                  "digital readers cannot click it)"))
    for prob in res["problems"]:
        print(f"PROBLEM   {prob}")
    reach = res.get("reachability")
    if reach:
        state = f"HTTP {reach['status']}" if reach["status"] else f"no answer ({reach['error']})"
        print(f"reachable {'yes' if reach['reachable'] else 'NO'}: {state}"
              + (f", final address {reach['final_url']}" if reach.get("final_url") else ""))
        print(f"          {reach['meaning']}")
    else:
        print("reachable not checked (add --check-reachable for one HTTP GET)")
    print("not shown a phone scan of the printed proof; do that before printing")


def main(argv=None) -> int:
    """Command-line entry point: make, decode or verify. Returns the exit status."""
    ap = argparse.ArgumentParser(prog="qr_code.py", formatter_class=argparse.RawDescriptionHelpFormatter,
                                 description="Make ATR QR codes at an exact printed size, decode them and verify "
                                             "them in the final PDF.",
                                 epilog="Exit status: 0 ok, 1 usage or environment error, 2 refused, "
                                        "3 verification failed.")
    sub = ap.add_subparsers(dest="cmd")
    mk = sub.add_parser("make", help="write a QR PNG at an exact size")
    mk.add_argument("url")
    mk.add_argument("-o", "--output", required=True, help="output .png")
    mk.add_argument("--size-in", type=float, default=1.0, help="printed width in inches, quiet zone included")
    mk.add_argument("--dpi", type=int, default=600)
    mk.add_argument("--ecc", default="M", choices=ECC_LEVELS)
    mk.add_argument("--quiet", type=int, default=MIN_QUIET, help="quiet zone in modules (at least 4)")
    mk.add_argument("--color", default="navy", help="dark modules: navy (default) or black")
    mk.add_argument("--json", action="store_true")
    dc = sub.add_parser("decode", help="decode QR codes in image files")
    dc.add_argument("images", nargs="+")
    dc.add_argument("--json", action="store_true")
    vf = sub.add_parser("verify", help="decode QR codes from the rendered PDF and compare to the URL")
    vf.add_argument("pdf")
    vf.add_argument("--url", required=True, help="the exact expected address")
    vf.add_argument("--dpi", type=int, default=200)
    vf.add_argument("--pages", help="pages to check, e.g. 1 or 1,3-4 (default: all)")
    vf.add_argument("--require-link", action="store_true", help="fail when no link annotation matches")
    vf.add_argument("--check-reachable", action="store_true", help="also make one HTTP GET (network)")
    vf.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    if not a.cmd:
        ap.print_help()
        return 1
    try:
        if a.cmd == "make":
            dark = ALLOWED_DARK.get(a.color.lower(), a.color)
            info = describe_qr(a.url, a.size_in, a.dpi, a.ecc, a.quiet, dark)
            out = make_qr(a.url, a.output, a.size_in, a.dpi, a.ecc, a.quiet, dark)
            decoded = decode_image(out) if _has_zxing() else None
            info.update({"path": str(out.resolve()), "decoded": decoded,
                         "decodes_exactly": (decoded == [a.url]) if decoded is not None else None})
            if a.json:
                print(json.dumps(info, indent=2))
            else:
                print(f"wrote {out}  ({info['size_in']} in at {info['dpi']} dpi = {info['pixels']} px; version "
                      f"{info['version']}, ECC {info['ecc']}, {info['modules_with_quiet_zone']} modules with a "
                      f"{info['quiet_modules']}-module quiet zone, {info['module_mm']} mm per module)")
                print(f"encodes   {a.url}")
                print(f"print     {info['printed_fallback']}   (under the code, as plain text)")
                print(f"alt text  {info['alt']}")
                print(f"scans from up to about {info['scan_distance_max_in']} in")
                for note in info["notes"]:
                    print(f"note      {note}")
                if decoded is None:
                    print("decode    not checked (zxing-cpp is not installed)")
                elif info["decodes_exactly"]:
                    print("decode    ok: the PNG decodes to exactly this address")
                else:
                    print(f"decode    FAIL: the PNG decodes to {decoded!r}")
            return 0 if info["decodes_exactly"] in (True, None) else 3
        if a.cmd == "decode":
            res = {p: decode_image(p) for p in a.images}
            if a.json:
                print(json.dumps(res, indent=2))
            else:
                for p, vals in res.items():
                    print(f"{p}: " + (", ".join(vals) if vals else "no QR code found"))
            return 0 if all(res.values()) else 3
        if a.cmd == "verify":
            res = verify_pdf(a.pdf, a.url, a.dpi, a.pages)
            if a.require_link and not res["link_match"]:
                res["problems"].append("no PDF link annotation points to the expected address (--require-link)")
                res["ok"] = False
            if a.check_reachable:
                res["reachability"] = check_reachable(a.url)
            if a.json:
                print(json.dumps(res, indent=2))
            else:
                _print_verify(res)
            reach_ok = res.get("reachability", {}).get("reachable", True)
            return 0 if res["ok"] and reach_ok else 3
    except QRError as exc:
        print(f"qr_code.py: refused: {exc}", file=sys.stderr)
        return 2
    except (RuntimeError, FileNotFoundError, OSError, ValueError) as exc:
        print(f"qr_code.py: {exc}", file=sys.stderr)
        return 1
    return 1


def _has_zxing() -> bool:
    try:
        _zxing()
        return True
    except RuntimeError:
        return False


if __name__ == "__main__":
    sys.exit(main())
