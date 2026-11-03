#!/usr/bin/env python3
"""export_office.py - export Office files to tagged PDF with the brand fonts, inspect the PDF and render pages.

Exports with LibreOffice in a private, throw-away profile that has the skill's fonts (assets/fonts/) installed, and
asks for a tagged PDF with bookmarks explicitly (UseTaggedPDF, ExportBookmarks). Then it reports what the PDF
actually contains (page count and sizes, tags, embedded fonts, link targets) and renders pages to PNG for review,
optionally only the pages whose content changed since the last render.

The report keeps three kinds of evidence apart:
  1. source and structure checks (what the .pptx or spec says; brand_check.py and new_deck.py do these)
  2. verified in the exported PDF (what this script reads from the file: tags, fonts, links, sizes)
  3. visual review still to do by a person (looking at the rendered pages, the printed proof, a phone scan)
PDF tags show that the export feature was used. They are not proof of full accessibility conformance (reading
order, alt text quality and contrast still need a person, or a PDF/UA checker).

Usage (from the skill root, atr-lab-design/):
  python3 scripts/export_office.py pdf flyer.pptx --out-dir out/ [--pages 1-2] [--no-tagged] [--render]
         [--dpi 150] [--qa-dir qa/] [--changed-pages] [--json]
  python3 scripts/export_office.py inspect out/flyer.pdf [--json]
  python3 scripts/export_office.py render out/flyer.pdf --out-dir qa/ [--pages 1,3-4] [--dpi 150]
         [--changed-pages] [--sheet]
  python3 scripts/export_office.py sheet qa/flyer-page-*.png -o qa/flyer-sheet.png [--cols 3]

--changed-pages renders only pages whose content hash differs from the last render into the same folder (hashes
are kept in <out-dir>/.atr-page-hashes.json). A page hash covers the page's extracted text, its drawing operators
and the bytes of its images, so a new font subset alone does not count as a change.

Env: SOFFICE=/path/to/soffice (LibreOffice binary), RENDER_TIMEOUT=240 (seconds).

Exit status: 0 done; 1 usage or environment error (no LibreOffice, no pdftoppm, missing package, bad file);
3 exported, but the PDF check found a problem (not tagged when tags were requested, fonts not embedded or a
non-brand font substituted).

Requires pypdf and Pillow; LibreOffice for `pdf`; poppler's pdftoppm for `render`.
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import argparse  # noqa: E402
import datetime as _dt  # noqa: E402
import glob  # noqa: E402
import hashlib  # noqa: E402
import json  # noqa: E402
import os  # noqa: E402
import re  # noqa: E402
import shutil  # noqa: E402
import subprocess  # noqa: E402
import tempfile  # noqa: E402
from pathlib import Path  # noqa: E402

HERE = Path(__file__).resolve().parent
SKILL = HERE.parent
FONT_DIR = SKILL / "assets" / "fonts"
HASH_FILE = ".atr-page-hashes.json"

FILTERS = {
    "impress_pdf_Export": ("pptx", "potx", "ppsx", "pptm", "ppt", "pps", "odp"),
    "writer_pdf_Export": ("docx", "dotx", "docm", "doc", "rtf", "odt"),
    "calc_pdf_Export": ("xlsx", "xlsm", "xls", "ods"),
    "draw_pdf_Export": ("odg",),
}
BRAND_FONTS = {"sourcesans3": "Source Sans 3", "robotoslab": "Roboto Slab", "sourcecodepro": "Source Code Pro"}
SYMBOL_FONTS = ("opensymbol",)
INK, LINE, SLATE = (27, 37, 51), (214, 222, 232), (74, 88, 104)


class ExportError(Exception):
    """An export or render that could not run (missing tool, LibreOffice failure, bad input)."""


# ----------------------------------------------------------------------------------------------- tools
def find_soffice() -> str:
    """Return the LibreOffice binary (SOFFICE env, PATH, then the usual install folders) or raise ExportError."""
    env = os.environ.get("SOFFICE")
    if env:
        if os.access(env, os.X_OK):
            return env
        raise ExportError(f"SOFFICE={env} is not executable")
    for name in ("soffice", "libreoffice"):
        hit = shutil.which(name)
        if hit:
            return hit
    candidates = ["/Applications/LibreOffice.app/Contents/MacOS/soffice",
                  str(Path.home() / "Applications/LibreOffice.app/Contents/MacOS/soffice"),
                  "/opt/homebrew/bin/soffice", "/usr/local/bin/soffice", "/usr/bin/soffice",
                  "/usr/lib/libreoffice/program/soffice", "/opt/libreoffice/program/soffice", "/snap/bin/libreoffice",
                  "C:/Program Files/LibreOffice/program/soffice.exe"]
    candidates += sorted(glob.glob("/opt/libreoffice*/program/soffice"))
    for c in candidates:
        if os.path.isfile(c) and os.access(c, os.X_OK):
            return c
    raise ExportError("LibreOffice not found. Install it (https://www.libreoffice.org/download/) or set "
                      "SOFFICE=/path/to/soffice")


def _pdftoppm() -> str:
    hit = shutil.which("pdftoppm")
    if not hit:
        raise ExportError("pdftoppm not found: install poppler (brew install poppler / apt install poppler-utils)")
    return hit


def _reader(pdf):
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise ExportError("reading PDFs needs pypdf: .venv/bin/pip install \"pypdf>=4.0\"") from exc
    return PdfReader(str(pdf))


def sha256_file(path) -> str:
    """SHA-256 of a file's bytes."""
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_pages(spec, count: int) -> list:
    """Turn '1,3-4', [1, 3] or 2 into a sorted list of 1-based page numbers within 1..count.

    Raises ValueError for pages outside the document or unreadable text."""
    if spec is None or spec == "" or spec == "all":
        return list(range(1, count + 1))
    if isinstance(spec, int):
        items = [spec]
    elif isinstance(spec, (list, tuple, set)):
        items = [int(x) for x in spec]
    else:
        items = []
        for part in str(spec).split(","):
            part = part.strip()
            if not part:
                continue
            m = re.fullmatch(r"(\d+)\s*-\s*(\d+)", part)
            if m:
                a, b = int(m.group(1)), int(m.group(2))
                if a > b:
                    raise ValueError(f"page range '{part}' runs backwards")
                items.extend(range(a, b + 1))
            elif part.isdigit():
                items.append(int(part))
            else:
                raise ValueError(f"cannot read page selection '{part}' (use 1,3-5)")
    bad = [p for p in items if p < 1 or p > count]
    if bad:
        raise ValueError(f"page(s) {', '.join(map(str, sorted(set(bad))))} outside 1-{count}")
    return sorted(set(items))


def page_count(pdf) -> int:
    """Number of pages in a PDF."""
    return len(_reader(pdf).pages)


# ----------------------------------------------------------------------------------------------- export
def export_pdf(src, out_dir, tagged=True, pages=None, bookmarks=True, timeout=None) -> Path:
    """Export src (.pptx, .docx, .xlsx, .odp ...) to <out_dir>/<stem>.pdf with LibreOffice and return the path.

    LibreOffice runs headless with a private throw-away profile that has the skill's TTFs installed, so the brand
    fonts render without a system install. tagged requests UseTaggedPDF and bookmarks ExportBookmarks explicitly;
    pages ('1-3,5' or a list) exports only those pages."""
    src = Path(src).expanduser().resolve()
    if not src.is_file():
        raise ExportError(f"no such file: {src}")
    ext = src.suffix.lower().lstrip(".")
    filt = next((f for f, exts in FILTERS.items() if ext in exts), None)
    if not filt:
        raise ExportError(f"unsupported file type '.{ext}' (expected .pptx, .docx, .xlsx, .odp, .odt, .odg ...)")
    soffice = find_soffice()
    out_dir = Path(out_dir).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    options = {"UseTaggedPDF": {"type": "boolean", "value": "true" if tagged else "false"},
               "ExportBookmarks": {"type": "boolean", "value": "true" if bookmarks else "false"}}
    if pages:
        sel = pages if isinstance(pages, str) else ",".join(str(p) for p in pages)
        options["PageRange"] = {"type": "string", "value": sel}
    timeout = float(timeout or os.environ.get("RENDER_TIMEOUT", 240))
    with tempfile.TemporaryDirectory(prefix="atr-export-") as tmp:
        tmp = Path(tmp)
        fonts = tmp / "profile" / "user" / "fonts"
        fonts.mkdir(parents=True)
        if FONT_DIR.is_dir():
            for f in FONT_DIR.rglob("*"):
                if f.suffix.lower() in (".ttf", ".otf"):
                    shutil.copy2(f, fonts / f.name)
        (tmp / "in").mkdir()
        (tmp / "out").mkdir()
        plain = tmp / "in" / f"input.{ext}"   # a plain name: odd characters cannot trip LibreOffice
        shutil.copy2(src, plain)
        cmd = [soffice, "-env:UserInstallation=" + (tmp / "profile").as_uri(), "--headless", "--norestore",
               "--nolockcheck", "--convert-to", "pdf:" + filt + ":" + json.dumps(options),
               "--outdir", str(tmp / "out"), str(plain)]
        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        except subprocess.TimeoutExpired as exc:
            raise ExportError(f"LibreOffice timed out after {timeout:.0f} s (raise RENDER_TIMEOUT)") from exc
        produced = tmp / "out" / "input.pdf"
        if proc.returncode != 0 or not produced.is_file() or produced.stat().st_size == 0:
            raise ExportError(f"LibreOffice did not produce a PDF (status {proc.returncode}):\n"
                              f"{proc.stdout}\n{proc.stderr}".strip())
        dest = out_dir / (src.stem + ".pdf")
        shutil.copy2(produced, dest)
    return dest


# ----------------------------------------------------------------------------------------------- inspect
def _font_entries(resources, seen, out, page_no, depth=0):
    if resources is None or depth > 6:
        return
    resources = resources.get_object()
    fonts = resources.get("/Font")
    if fonts is not None:
        for _, ref in fonts.get_object().items():
            f = ref.get_object()
            key = id(f) if not hasattr(ref, "idnum") else (ref.idnum, ref.generation)
            subtype = str(f.get("/Subtype", ""))
            base = str(f.get("/BaseFont", "")) or ("(Type 3 font)" if subtype == "/Type3" else "(unnamed)")
            desc = f.get("/FontDescriptor")
            if subtype == "/Type0":
                kids = f.get("/DescendantFonts")
                if kids:
                    desc = kids.get_object()[0].get_object().get("/FontDescriptor")
            desc = desc.get_object() if desc is not None else None
            embedded = subtype == "/Type3" or bool(desc is not None and any(
                k in desc for k in ("/FontFile", "/FontFile2", "/FontFile3")))
            name = re.sub(r"^/", "", base)
            subset = bool(re.match(r"^[A-Z]{6}\+", name))
            name = re.sub(r"^[A-Z]{6}\+", "", name)
            entry = out.setdefault(name, {"name": name, "type": subtype.lstrip("/"), "embedded": embedded,
                                          "subset": subset, "pages": []})
            entry["embedded"] = entry["embedded"] and embedded
            if page_no not in entry["pages"]:
                entry["pages"].append(page_no)
            seen.add(key)
    xobjs = resources.get("/XObject")
    if xobjs is not None:
        for _, ref in xobjs.get_object().items():
            x = ref.get_object()
            if x.get("/Subtype") == "/Form":
                _font_entries(x.get("/Resources"), seen, out, page_no, depth + 1)


def classify_font(name: str) -> str:
    """'brand', 'symbol' (LibreOffice's OpenSymbol, used for bullets) or 'substitute' for a PDF font name."""
    key = re.sub(r"[^a-z0-9]", "", name.lower())
    if any(k in key for k in BRAND_FONTS):
        return "brand"
    if any(k in key for k in SYMBOL_FONTS):
        return "symbol"
    return "substitute"


def _count_outline(items) -> int:
    n = 0
    for it in items or []:
        n += _count_outline(it) if isinstance(it, list) else 1
    return n


def inspect_pdf(pdf) -> dict:
    """Report what an exported PDF contains: pages, page sizes (in), tags (MarkInfo/Marked, StructTreeRoot, Lang),
    embedded fonts (brand, symbol or substitute such as Arial or DejaVu), link targets and bookmarks.

    'problems' lists what fails the export contract (untagged, a font not embedded, a non-brand substitution);
    'not_established' lists what this check cannot show."""
    pdf = Path(pdf).expanduser().resolve()
    if not pdf.is_file():
        raise ExportError(f"no such PDF: {pdf}")
    r = _reader(pdf)
    root = r.trailer["/Root"].get_object()
    mark = root.get("/MarkInfo")
    marked = bool(mark is not None and bool(mark.get_object().get("/Marked", False)))
    struct = root.get("/StructTreeRoot") is not None
    lang = str(root.get("/Lang", "")) or None
    fonts, seen, sizes, links, internal = {}, set(), [], [], 0
    for i, page in enumerate(r.pages, 1):
        box = page.mediabox
        w, h = float(box.width) / 72.0, float(box.height) / 72.0
        if int(page.get("/Rotate", 0) or 0) % 180:
            w, h = h, w
        sizes.append({"page": i, "width_in": round(w, 3), "height_in": round(h, 3)})
        _font_entries(page.get("/Resources"), seen, fonts, i)
        for ref in page.get("/Annots") or []:
            a = ref.get_object()
            if a.get("/Subtype") != "/Link":
                continue
            act = a.get("/A")
            act = act.get_object() if act is not None else None
            if act is not None and act.get("/URI") is not None:
                uri = act.get("/URI")
                uri = uri.decode("utf-8", "replace") if isinstance(uri, bytes) else str(uri)
                rect = [round(float(v) / 72.0, 2) for v in a.get("/Rect", [])]
                links.append({"page": i, "uri": uri, "rect_in": rect})
            else:
                internal += 1
    try:
        bookmarks = _count_outline(r.outline)
    except Exception:  # noqa: BLE001 (a broken outline is reported as none)
        bookmarks = 0
    font_list = sorted(fonts.values(), key=lambda f: f["name"])
    for f in font_list:
        f["class"] = classify_font(f["name"])
    info = r.metadata or {}
    problems = []
    if not (marked and struct):
        problems.append("the PDF is not tagged (MarkInfo/Marked " + ("yes" if marked else "no")
                        + ", StructTreeRoot " + ("yes" if struct else "no") + ")")
    for f in font_list:
        if not f["embedded"]:
            problems.append(f"font {f['name']} is not embedded")
        if f["class"] == "substitute":
            problems.append(f"font {f['name']} is not a brand font (a substitution; is a brand font missing "
                            f"from the profile or misspelled in the file?) on page(s) "
                            + ", ".join(map(str, f["pages"])))
    distinct = sorted({(s["width_in"], s["height_in"]) for s in sizes})
    return {
        "pdf": str(pdf), "sha256": sha256_file(pdf), "pages": len(r.pages), "page_sizes_in": sizes,
        "distinct_page_sizes_in": [list(d) for d in distinct],
        "tagged": {"marked": marked, "struct_tree_root": struct, "lang": lang, "is_tagged": marked and struct},
        "fonts": font_list, "links": links, "internal_links": internal, "bookmarks": bookmarks,
        "title": str(info.get("/Title", "") or ""), "producer": str(info.get("/Producer", "") or ""),
        "problems": problems,
        "not_established": [
            "Tags show the tagged-PDF export feature was used; they do not establish accessibility conformance "
            "(reading order, alt text quality and color contrast need a person or a PDF/UA checker).",
            "Embedded fonts do not show the text fits its boxes or looks right: look at the rendered pages.",
            "This is a review PDF at trim size, not a PDF/X print file with bleed; get the printer's preflight.",
        ],
    }


def inspection_lines(ins: dict) -> list:
    """Plain-English 'verified in the PDF' lines for an inspect_pdf() result."""
    t = ins["tagged"]
    sizes = "; ".join(f"{w:g} x {h:g} in" for w, h in ins["distinct_page_sizes_in"])
    lines = [f"{ins['pages']} page(s), {sizes}",
             "tagged: MarkInfo/Marked " + ("yes" if t["marked"] else "no") + ", StructTreeRoot "
             + ("yes" if t["struct_tree_root"] else "no") + (f", language {t['lang']}" if t["lang"] else "")]
    by = {"brand": [], "symbol": [], "substitute": []}
    for f in ins["fonts"]:
        by[f["class"]].append(f["name"] + ("" if f["embedded"] else " (NOT embedded)"))
    lines.append("brand fonts embedded: " + (", ".join(by["brand"]) or "none"))
    if by["symbol"]:
        lines.append("symbol fonts (bullets): " + ", ".join(by["symbol"]))
    if by["substitute"]:
        lines.append("NON-BRAND fonts: " + ", ".join(by["substitute"]))
    if ins["links"]:
        for ln in ins["links"]:
            lines.append(f"link on page {ln['page']}: {ln['uri']}")
    else:
        lines.append("no URI link annotations")
    lines.append(f"{ins['bookmarks']} bookmark(s)")
    return lines


# ----------------------------------------------------------------------------------------------- page hashes
def _hash_xobject(x, h, depth):
    sub = x.get("/Subtype")
    if sub == "/Image":
        try:
            h.update(hashlib.sha256(x.get_data()).digest())
        except Exception:  # noqa: BLE001 (an unreadable stream still hashes by its raw bytes)
            h.update(hashlib.sha256(getattr(x, "_data", b"") or b"").digest())
        for k in ("/Width", "/Height", "/SMask"):
            if k == "/SMask" and x.get(k) is not None:
                _hash_xobject(x[k].get_object(), h, depth + 1)
            elif k != "/SMask":
                h.update(str(x.get(k)).encode())
    elif sub == "/Form" and depth < 6:
        _hash_stream(x, x.get("/Resources"), h, depth + 1)


def _hash_stream(stream_obj, resources, h, depth=0):
    from pypdf.generic import ContentStream, NumberObject, FloatObject
    resources = resources.get_object() if resources is not None else {}
    xobjs = resources.get("/XObject")
    xobjs = xobjs.get_object() if xobjs is not None else {}
    try:
        ops = ContentStream(stream_obj, None).operations
    except Exception:  # noqa: BLE001
        data = stream_obj.get_data() if hasattr(stream_obj, "get_data") else b""
        h.update(hashlib.sha256(data).digest())
        return
    for operands, op in ops:
        opn = op.decode("latin-1") if isinstance(op, bytes) else str(op)
        if opn in ("Tj", "TJ", "'", '"', "BDC", "BMC", "EMC", "MP", "DP"):
            h.update(opn.encode())          # text comes from extract_text(); marked content is tagging only
            continue
        if opn == "Do":
            h.update(b"Do")
            if operands and operands[0] in xobjs:
                _hash_xobject(xobjs[operands[0]].get_object(), h, depth)
            continue
        if opn in ("Tf", "gs"):
            h.update(opn.encode())
            nums = [o for o in operands if isinstance(o, (NumberObject, FloatObject, int, float))]
            h.update(repr([round(float(n), 2) for n in nums]).encode())
            continue
        parts = [opn]
        for o in operands:
            if isinstance(o, (NumberObject, FloatObject, int, float)):
                parts.append(f"{float(o):.2f}")
            else:
                parts.append(str(o))
        h.update(" ".join(parts).encode("utf-8", "replace"))


def page_hashes(pdf) -> list:
    """One content hash per page: extracted text, drawing operators (numbers rounded) and image bytes.

    Font subset names and glyph ids are left out, so re-exporting an unchanged page gives the same hash."""
    r = _reader(pdf)
    out = []
    for page in r.pages:
        h = hashlib.sha256()
        box = page.mediabox
        h.update(f"{float(box.width):.1f}x{float(box.height):.1f}".encode())
        try:
            h.update((page.extract_text() or "").encode("utf-8", "replace"))
        except Exception:  # noqa: BLE001
            pass
        contents = page.get_contents()
        if contents is not None:
            _hash_stream(contents, page.get("/Resources"), h)
        for ref in page.get("/Annots") or []:
            a = ref.get_object()
            act = a.get("/A")
            if act is not None and act.get_object().get("/URI") is not None:
                h.update(str(act.get_object().get("/URI")).encode("utf-8", "replace"))
        out.append(h.hexdigest())
    return out


def _load_hashes(out_dir: Path) -> dict:
    try:
        return json.loads((out_dir / HASH_FILE).read_text())
    except (OSError, ValueError):
        return {}


def changed_pages(pdf, out_dir, dpi=150) -> list:
    """1-based pages of pdf whose content hash differs from the last render into out_dir (or whose PNG is missing,
    or that were rendered at another dpi)."""
    pdf = Path(pdf)
    out_dir = Path(out_dir)
    old = _load_hashes(out_dir).get(pdf.stem, {})
    new = page_hashes(pdf)
    width = max(2, len(str(len(new))))
    changed = []
    for i, hv in enumerate(new, 1):
        png = out_dir / f"{pdf.stem}-page-{i:0{width}d}.png"
        if old.get("dpi") != dpi or old.get("pages", {}).get(str(i)) != hv or not png.is_file():
            changed.append(i)
    return changed


def save_page_hashes(pdf, out_dir, dpi=150) -> None:
    """Record the current page hashes of pdf in <out_dir>/.atr-page-hashes.json."""
    pdf = Path(pdf)
    out_dir = Path(out_dir)
    data = _load_hashes(out_dir)
    data[pdf.stem] = {"dpi": dpi, "pages": {str(i): hv for i, hv in enumerate(page_hashes(pdf), 1)},
                      "pdf_sha256": sha256_file(pdf),
                      "saved_at": _dt.datetime.now().astimezone().isoformat(timespec="seconds")}
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / HASH_FILE).write_text(json.dumps(data, indent=2) + "\n")


# ----------------------------------------------------------------------------------------------- render
def render(pdf, out_dir, dpi=150, pages=None) -> list:
    """Render PDF pages to <out_dir>/<stem>-page-NN.png with pdftoppm and return the PNG paths in page order.

    pages: None for all, or a list / '1,3-4' string of 1-based page numbers. Stale PNGs of a page that no longer
    exists are removed when every page is rendered."""
    pdf = Path(pdf).expanduser().resolve()
    out_dir = Path(out_dir).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    tool = _pdftoppm()
    count = page_count(pdf)
    sel = parse_pages(pages, count) if pages is not None else list(range(1, count + 1))
    width = max(2, len(str(count)))
    out = []
    for n in sel:
        base = out_dir / f"{pdf.stem}-page-{n:0{width}d}"
        subprocess.run([tool, "-r", str(int(dpi)), "-f", str(n), "-l", str(n), "-png", "-singlefile",
                        str(pdf), str(base)], check=True, capture_output=True)
        out.append(base.with_suffix(".png"))
    if pages is None:
        for old in out_dir.glob(f"{glob.escape(pdf.stem)}-page-*.png"):
            m = re.search(r"-page-(\d+)\.png$", old.name)
            if m and (int(m.group(1)) > count or len(m.group(1)) != width):
                old.unlink()
    return out


def render_changed(pdf, out_dir, dpi=150) -> tuple:
    """Render only the pages whose content changed since the last render into out_dir; record the new hashes.

    Returns (rendered_pngs, all_page_pngs)."""
    pdf = Path(pdf).expanduser().resolve()
    out_dir = Path(out_dir).expanduser().resolve()
    todo = changed_pages(pdf, out_dir, dpi)
    rendered = render(pdf, out_dir, dpi, todo) if todo else []
    save_page_hashes(pdf, out_dir, dpi)
    count = page_count(pdf)
    width = max(2, len(str(count)))
    for old in out_dir.glob(f"{glob.escape(pdf.stem)}-page-*.png"):
        m = re.search(r"-page-(\d+)\.png$", old.name)
        if m and (int(m.group(1)) > count or len(m.group(1)) != width):
            old.unlink()
    allp = [out_dir / f"{pdf.stem}-page-{i:0{width}d}.png" for i in range(1, count + 1)]
    return rendered, allp


def _label_font(size):
    from PIL import ImageFont
    for name in ("SourceSans3-Semibold.ttf", "SourceSans3-Regular.ttf"):
        p = FONT_DIR / "source-sans-3" / name
        if p.is_file():
            return ImageFont.truetype(str(p), size)
    return ImageFont.load_default()


def contact_sheet(pngs, out, cols=3, thumb_w=None, gap=12, label=True) -> Path:
    """Lay rendered pages out in a compact grid with page numbers and return the sheet's path.

    Each cell is as wide as thumb_w (default: 900 px for one page, 640 for two, else 480) and as tall as the
    tallest page in its row, so portrait and landscape pages leave little empty space."""
    from PIL import Image, ImageDraw

    paths = [Path(p) for p in pngs]
    if not paths:
        raise ExportError("no pages for a contact sheet")
    cols = max(1, min(int(cols), len(paths)))
    thumb_w = int(thumb_w or (900 if len(paths) == 1 else 640 if len(paths) == 2 else 480))
    thumbs = []
    for i, p in enumerate(paths, 1):
        with Image.open(p) as im:
            im = im.convert("RGB")
            scale = thumb_w / im.width
            th = im.resize((thumb_w, max(1, int(round(im.height * scale)))), Image.LANCZOS)
        m = re.search(r"-page-(\d+)\.png$", p.name)
        thumbs.append((th, int(m.group(1)) if m else i))
    label_h = 26 if label else 0
    rows = [thumbs[i:i + cols] for i in range(0, len(thumbs), cols)]
    row_h = [max(t.height for t, _ in row) + label_h for row in rows]
    width = gap + cols * (thumb_w + gap)
    height = gap + sum(h + gap for h in row_h)
    sheet = Image.new("RGB", (width, height), LINE)
    draw = ImageDraw.Draw(sheet)
    font = _label_font(17)
    y = gap
    for row, rh in zip(rows, row_h):
        x = gap
        for th, n in row:
            sheet.paste(th, (x, y))
            draw.rectangle([x - 1, y - 1, x + th.width, y + th.height], outline=SLATE)
            if label:
                draw.text((x, y + th.height + 4), f"Page {n}", fill=INK, font=font)
            x += thumb_w + gap
        y += rh + gap
    out = Path(out).expanduser()
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(str(out), optimize=True)
    return out


# ----------------------------------------------------------------------------------------------- CLI
def _print_inspection(ins: dict) -> None:
    print(f"PDF  {ins['pdf']}")
    print("Verified in the PDF:")
    for ln in inspection_lines(ins):
        print(f"  - {ln}")
    if ins["problems"]:
        print("Problems:")
        for p in ins["problems"]:
            print(f"  - {p}")
    print("Not established by this check (visual and human review):")
    for p in ins["not_established"]:
        print(f"  - {p}")


def main(argv=None) -> int:
    """Command-line entry point: pdf, inspect, render or sheet. Returns the exit status."""
    ap = argparse.ArgumentParser(prog="export_office.py", formatter_class=argparse.RawDescriptionHelpFormatter,
                                 description="Export Office files to tagged PDF with the ATR fonts, inspect the PDF "
                                             "and render pages.",
                                 epilog="Exit status: 0 done, 1 usage or environment error, 3 PDF check problem.")
    sub = ap.add_subparsers(dest="cmd")
    p = sub.add_parser("pdf", help="export to PDF (tagged, bookmarks) and inspect it")
    p.add_argument("src")
    p.add_argument("--out-dir", required=True)
    p.add_argument("--pages", help="export only these pages, e.g. 1-3,5")
    p.add_argument("--no-tagged", action="store_true", help="do not request a tagged PDF")
    p.add_argument("--render", action="store_true", help="also render pages and a contact sheet")
    p.add_argument("--qa-dir", help="folder for rendered pages (default: <out-dir>/<stem>-pages)")
    p.add_argument("--dpi", type=int, default=150)
    p.add_argument("--changed-pages", action="store_true", help="render only pages that changed")
    p.add_argument("--json", action="store_true")
    i = sub.add_parser("inspect", help="report pages, tags, fonts and links of a PDF")
    i.add_argument("pdf")
    i.add_argument("--json", action="store_true")
    r = sub.add_parser("render", help="render PDF pages to PNG")
    r.add_argument("pdf")
    r.add_argument("--out-dir", required=True)
    r.add_argument("--pages")
    r.add_argument("--dpi", type=int, default=150)
    r.add_argument("--changed-pages", action="store_true")
    r.add_argument("--sheet", action="store_true", help="also write <stem>-sheet.png")
    s = sub.add_parser("sheet", help="make a compact contact sheet from page PNGs")
    s.add_argument("pngs", nargs="+")
    s.add_argument("-o", "--output", required=True)
    s.add_argument("--cols", type=int, default=3)
    a = ap.parse_args(argv)
    if not a.cmd:
        ap.print_help()
        return 1
    try:
        if a.cmd == "pdf":
            pdf = export_pdf(a.src, a.out_dir, tagged=not a.no_tagged, pages=a.pages)
            ins = inspect_pdf(pdf)
            if a.no_tagged:   # untagged was asked for: report it, do not fail on it
                ins["problems"] = [p for p in ins["problems"] if not p.startswith("the PDF is not tagged")]
            res = {"pdf": str(pdf), "inspection": ins}
            if a.render:
                qa = Path(a.qa_dir) if a.qa_dir else Path(a.out_dir) / f"{pdf.stem}-pages"
                if a.changed_pages:
                    done, allp = render_changed(pdf, qa, a.dpi)
                else:
                    done = allp = render(pdf, qa, a.dpi)
                    save_page_hashes(pdf, qa, a.dpi)
                res["rendered"] = [str(x) for x in done]
                res["sheet"] = str(contact_sheet(allp, qa / f"{pdf.stem}-sheet.png"))
            if a.json:
                print(json.dumps(res, indent=2))
            else:
                print(f"wrote {pdf}")
                _print_inspection(ins)
                if a.render:
                    print(f"rendered {len(res['rendered'])} page(s); contact sheet {res['sheet']}. "
                          "Look at every rendered page.")
            return 3 if ins["problems"] else 0
        if a.cmd == "inspect":
            ins = inspect_pdf(a.pdf)
            if a.json:
                print(json.dumps(ins, indent=2))
            else:
                _print_inspection(ins)
            return 3 if ins["problems"] else 0
        if a.cmd == "render":
            if a.changed_pages:
                if a.pages:
                    raise ValueError("use --pages or --changed-pages, not both")
                done, allp = render_changed(a.pdf, a.out_dir, a.dpi)
                unchanged = len(allp) - len(done)
                print(f"rendered {len(done)} changed page(s); {unchanged} unchanged page(s) kept")
            else:
                done = render(a.pdf, a.out_dir, a.dpi, a.pages)
                allp = done
                if not a.pages:
                    save_page_hashes(a.pdf, a.out_dir, a.dpi)
            for pth in done:
                print(pth)
            if a.sheet:
                print("contact sheet", contact_sheet(allp, Path(a.out_dir) / f"{Path(a.pdf).stem}-sheet.png"))
            return 0
        if a.cmd == "sheet":
            print(contact_sheet(a.pngs, a.output, a.cols))
            return 0
    except (ExportError, ValueError, OSError, subprocess.CalledProcessError) as exc:
        print(f"export_office.py: {exc}", file=sys.stderr)
        return 1
    return 1


if __name__ == "__main__":
    sys.exit(main())
