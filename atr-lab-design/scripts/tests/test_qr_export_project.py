"""Tests for qr_code.py, export_office.py, project.py and the hyperlink-colors regression.

Offline. Tests that need LibreOffice (soffice) or poppler (pdftoppm) skip when those are missing.
Run from the skill root: python -m pytest -q -p no:cacheprovider scripts/tests
"""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

import pytest

sys.dont_write_bytecode = True

import export_office  # noqa: E402
import project  # noqa: E402
import qr_code  # noqa: E402

SCRIPTS = Path(__file__).resolve().parents[1]
SKILL = SCRIPTS.parent
URL = "https://example.org/register"

try:
    export_office.find_soffice()
    HAS_SOFFICE = True
except export_office.ExportError:
    HAS_SOFFICE = False
HAS_PDFTOPPM = shutil.which("pdftoppm") is not None
needs_pdftoppm = pytest.mark.skipif(not HAS_PDFTOPPM, reason="poppler pdftoppm not installed")
needs_soffice = pytest.mark.skipif(not (HAS_SOFFICE and HAS_PDFTOPPM), reason="LibreOffice or pdftoppm missing")


# ----------------------------------------------------------------------------------------------- helpers
def _image_pdf(path: Path, pages):
    """Write an image-only PDF (one PIL image per page, Letter at 100 dpi)."""
    pages[0].save(str(path), save_all=True, append_images=pages[1:], resolution=100.0)
    return path


def _page_with_qr(url, tmp_path, name="q.png"):
    from PIL import Image
    png = qr_code.make_qr(url, tmp_path / name, size_in=1.5, dpi=300)
    page = Image.new("RGB", (850, 1100), "white")
    with Image.open(png) as q:
        page.paste(q.resize((300, 300), Image.NEAREST), (500, 700))
    return page


# ----------------------------------------------------------------------------------------------- qr_code
def test_make_qr_exact_size_quiet_zone_and_decode(tmp_path):
    from PIL import Image
    out = qr_code.make_qr(URL, tmp_path / "qr.png", size_in=1.15, dpi=600)
    info = qr_code.describe_qr(URL, 1.15, 600)
    with Image.open(out) as im:
        assert im.size == (690, 690)
        assert round(im.info["dpi"][0]) == 600
        px = im.convert("RGB")
        quiet = info["quiet_modules"] * info["module_px"]
        for x, y in [(0, 0), (quiet - 1, quiet - 1), (689, 689), (689 - quiet + 1, 0), (0, 689 - quiet + 1)]:
            assert px.getpixel((x, y)) == (255, 255, 255)
        colors = {c for _, c in px.getcolors(10)}
        assert colors == {(255, 255, 255), (0, 57, 118)}
    assert qr_code.decode_image(out) == [URL]


@pytest.mark.parametrize("kwargs, words", [
    ({"dark": "gold"}, "refused"),
    ({"dark": "#FFFFFF", "light": "#003976"}, "inverted"),
    ({"dark": "navy", "light": "#F3F6FA"}, "background"),
    ({"quiet": 3}, "quiet zone"),
    ({"size_in": 0.5}, "too small"),
])
def test_make_qr_refusals(tmp_path, kwargs, words):
    with pytest.raises(qr_code.QRError) as exc:
        qr_code.make_qr(URL, tmp_path / "x.png", **kwargs)
    assert words in str(exc.value)
    assert not (tmp_path / "x.png").exists()


@pytest.mark.parametrize("bad", ["", " https://example.org", "https://example.org/a b", "[registration_url]"])
def test_bad_urls_refused(bad):
    with pytest.raises(qr_code.QRError):
        qr_code.check_url(bad)


def test_url_kept_exactly_and_notes(tmp_path):
    tracked = "https://www.atr.cs.kent.edu/k12?utm_source=flyer&utm_medium=qr"
    out = qr_code.make_qr(tracked, tmp_path / "t.png", size_in=1.0)
    assert qr_code.decode_image(out) == [tracked]
    assert qr_code.fallback_text(tracked) == "www.atr.cs.kent.edu/k12?utm_source=flyer&utm_medium=qr"
    notes = qr_code.url_notes(tracked)
    assert any("tracking" in n for n in notes)
    assert any("shortener" in n for n in qr_code.url_notes("https://forms.gle/abc"))
    assert qr_code.url_notes(URL) == []
    assert "example.org/register is printed below it" in qr_code.alt_text(URL, "the registration form")


def test_qr_cli_make_and_refuse(tmp_path, capsys):
    assert qr_code.main(["make", URL, "-o", str(tmp_path / "c.png"), "--size-in", "1.2"]) == 0
    out = capsys.readouterr().out
    assert "example.org/register" in out and "decode    ok" in out
    assert qr_code.main(["make", URL, "-o", str(tmp_path / "d.png"), "--color", "gold"]) == 2


@needs_pdftoppm
def test_verify_pdf_exact_and_modified(tmp_path):
    pdf = _image_pdf(tmp_path / "ok.pdf", [_page_with_qr(URL, tmp_path)])
    res = qr_code.verify_pdf(pdf, URL)
    assert res["ok"] and res["qr_match"] and not res["link_match"]
    assert res["pages"][0]["qr"] == [URL]
    # a destination with added tracking parameters is a different value: never accepted
    pdf2 = _image_pdf(tmp_path / "utm.pdf", [_page_with_qr(URL + "?utm_source=flyer", tmp_path, "u.png")])
    res2 = qr_code.verify_pdf(pdf2, URL)
    assert not res2["ok"] and not res2["qr_match"]
    assert any("parameters" in p for p in res2["problems"])
    assert qr_code.main(["verify", str(pdf2), "--url", URL]) == 3


# ----------------------------------------------------------------------------------------------- export_office
def test_parse_pages():
    assert export_office.parse_pages("1,3-4", 5) == [1, 3, 4]
    assert export_office.parse_pages(None, 3) == [1, 2, 3]
    assert export_office.parse_pages([2, 2, 1], 3) == [1, 2]
    with pytest.raises(ValueError):
        export_office.parse_pages("7", 3)
    with pytest.raises(ValueError):
        export_office.parse_pages("4-2", 5)


def test_contact_sheet_is_compact(tmp_path):
    from PIL import Image
    pngs = []
    for n in (1, 2, 3, 4):
        p = tmp_path / f"deck-page-{n:02d}.png"
        Image.new("RGB", (1500, 844), (0, 57, 118)).save(p)
        pngs.append(p)
    sheet = export_office.contact_sheet(pngs, tmp_path / "sheet.png", cols=3)
    with Image.open(sheet) as im:
        thumb_h = round(844 * 480 / 1500)
        assert im.width == 12 + 3 * (480 + 12)
        assert im.height == 12 + 2 * (thumb_h + 26 + 12)


def test_inspect_untagged_pdf_and_links(tmp_path):
    from PIL import Image
    from pypdf import PdfReader, PdfWriter
    from pypdf.annotations import Link
    pdf = _image_pdf(tmp_path / "plain.pdf", [Image.new("RGB", (850, 1100), "white")])
    w = PdfWriter(clone_from=PdfReader(str(pdf)))
    w.add_annotation(0, Link(rect=(50, 50, 200, 80), url=URL))
    linked = tmp_path / "linked.pdf"
    with open(linked, "wb") as fh:
        w.write(fh)
    ins = export_office.inspect_pdf(linked)
    assert ins["pages"] == 1
    assert ins["distinct_page_sizes_in"] == [[8.5, 11.0]]
    assert not ins["tagged"]["is_tagged"]
    assert any("not tagged" in p for p in ins["problems"])
    assert [ln["uri"] for ln in ins["links"]] == [URL]
    assert any("conformance" in n for n in ins["not_established"])


def test_classify_font():
    assert export_office.classify_font("SourceSans3-Bold") == "brand"
    assert export_office.classify_font("RobotoSlab-Regular") == "brand"
    assert export_office.classify_font("OpenSymbol") == "symbol"
    assert export_office.classify_font("DejaVuSans") == "substitute"
    assert export_office.classify_font("ArialMT") == "substitute"


def test_page_hashes_stable_and_sensitive(tmp_path):
    from PIL import Image
    a = [Image.new("RGB", (850, 1100), "white"), Image.new("RGB", (850, 1100), (0, 57, 118))]
    b = [Image.new("RGB", (850, 1100), "white"), Image.new("RGB", (850, 1100), (239, 171, 0))]
    h1 = export_office.page_hashes(_image_pdf(tmp_path / "a1.pdf", a))
    h2 = export_office.page_hashes(_image_pdf(tmp_path / "a2.pdf", a))
    h3 = export_office.page_hashes(_image_pdf(tmp_path / "b.pdf", b))
    assert h1 == h2
    assert h1[0] == h3[0] and h1[1] != h3[1]


@needs_pdftoppm
def test_render_changed_pages_only(tmp_path):
    from PIL import Image
    pdf = tmp_path / "doc.pdf"
    _image_pdf(pdf, [Image.new("RGB", (850, 1100), "white"), Image.new("RGB", (850, 1100), (0, 57, 118))])
    qa = tmp_path / "qa"
    first, allp = export_office.render_changed(pdf, qa, dpi=30)
    assert [p.name for p in first] == ["doc-page-01.png", "doc-page-02.png"]
    again, _ = export_office.render_changed(pdf, qa, dpi=30)
    assert again == []
    _image_pdf(pdf, [Image.new("RGB", (850, 1100), "white"), Image.new("RGB", (850, 1100), (239, 171, 0))])
    third, allp = export_office.render_changed(pdf, qa, dpi=30)
    assert [p.name for p in third] == ["doc-page-02.png"]
    assert all(p.is_file() for p in allp)


# ----------------------------------------------------------------------------------------------- project
def _init(tmp_path) -> Path:
    folder = tmp_path / "workshop"
    assert project.cmd_init(folder, example="workshop") == 0
    return folder / "project.json"


def test_substitute_filters_and_placeholders():
    rec = {"facts": set(), "empty": set(), "assets": set()}
    facts = {"url": "https://example.org/r", "d": "two-hour", "empty": " "}
    out = project.substitute({"a": "{{facts.url|printed}}", "b": ["{{ facts.d|capitalize }} lab"],
                              "c": "{{facts.empty}} and {{facts.missing}}", "_comment": "{{facts.url}}",
                              "img": "{{assets.fig}}"}, facts, lambda k: f"/abs/{k}.png", rec)
    assert out == {"a": "example.org/r", "b": ["Two-hour lab"], "c": "[empty] and [missing]",
                   "_comment": "{{facts.url}}", "img": "/abs/fig.png"}
    assert rec["empty"] == {"empty", "missing"} and rec["assets"] == {"fig"}


def test_init_refuses_inside_skill_and_example_is_read_only(tmp_path):
    with pytest.raises(project.Refused):
        project.cmd_init(SKILL / "scripts" / "examples" / "projects" / "new-one")
    proj = project.Project(SKILL / "scripts" / "examples" / "projects" / "workshop" / "project.json")
    with pytest.raises(project.Refused):
        proj.check_writable()
    with pytest.raises(project.Refused):
        proj.check_writable(manifest_too=True)
    st = project.project_status(proj)   # reading is fine
    assert set(st["artifacts"]) == {"flyer-letter", "flyer-tabloid", "poster-17x22", "deck"}


def test_set_fact_affects_only_artifacts_that_use_it(tmp_path, capsys):
    manifest = _init(tmp_path)
    proj = project.Project(manifest)
    before = project._hashes(proj)
    assert project.cmd_set(proj, "registration_url", "https://example.org/new") == 0
    out = capsys.readouterr().out
    assert "affects  flyer-letter, flyer-tabloid, poster-17x22" in out and "unchanged deck" in out
    after = project._hashes(project.Project(manifest))
    assert before["deck"] == after["deck"]
    assert before["flyer-letter"] != after["flyer-letter"]
    # an artifact-scoped fact reaches only that artifact
    proj = project.Project(manifest)
    before = project._hashes(proj)
    project.cmd_set(proj, "event_duration", "Half-day workshop", artifact="poster-17x22")
    after = project._hashes(project.Project(manifest))
    assert [n for n in before if before[n] != after[n]] == ["poster-17x22"]


def test_status_reports_draft_asset_and_empty_fact(tmp_path):
    manifest = _init(tmp_path)
    proj = project.Project(manifest)
    proj.data["facts"]["registration_url"] = ""
    st = project.project_status(proj)
    fl = st["artifacts"]["flyer-letter"]
    assert fl["build"] == "never built"
    assert "registration_url" in fl["facts_empty"] and "[registration_url]" in fl["placeholders"]
    assert any(a["id"] == "ksu-wordmark-white" and a["status"] == "draft" for a in fl["assets"])
    assert st["empty_facts"] == ["registration_url"]
    assert st["artifacts"]["deck"]["placeholders"] == []


def test_build_spec_qr_once_linked_and_skips_unchanged(tmp_path, capsys):
    from pptx import Presentation
    manifest = _init(tmp_path)
    proj = project.Project(manifest)
    assert project.cmd_build(proj, ["flyer-letter"], run_lint=False) == 0
    state = json.loads((manifest.parent / project.STATE_FILE).read_text())
    entry = state["artifacts"]["flyer-letter"]
    assert entry["qr"]["placed_by"].startswith("new_deck.py") and entry["qr"]["png_decodes"]
    assert abs(entry["qr"]["size_in"] - 1.0) < 0.01          # the Letter template's QR slot
    prs = Presentation(entry["pptx"])
    qrs = [s for s in prs.slides[0].shapes if s.name == "registration_qr"]
    assert len(qrs) == 1 and qrs[0].click_action.hyperlink.address == URL
    texts = [s.text for s in prs.slides[0].shapes if s.has_text_frame]
    assert "example.org/register" in texts
    capsys.readouterr()
    assert project.cmd_build(project.Project(manifest), ["flyer-letter"], changed_only=True, run_lint=False) == 0
    assert "skipped flyer-letter" in capsys.readouterr().out
    # a final build with an empty fact is refused; a draft build goes through without a QR code
    proj = project.Project(manifest)
    proj.data["facts"]["registration_url"] = ""
    assert project.cmd_build(proj, ["flyer-letter"], run_lint=False) == 2
    assert project.cmd_build(proj, ["flyer-letter"], draft=True, run_lint=False) == 0
    state = json.loads((manifest.parent / project.STATE_FILE).read_text())
    assert "QR skipped" in " ".join(state["artifacts"]["flyer-letter"]["steps"])


def test_poster_profile_has_no_type_floor_errors(tmp_path):
    manifest = _init(tmp_path)
    assert project.cmd_build(project.Project(manifest), ["poster-17x22"]) == 0
    entry = json.loads((manifest.parent / project.STATE_FILE).read_text())["artifacts"]["poster-17x22"]
    assert entry["lint"]["medium"] == "poster" and entry["lint"]["errors"] == 0
    assert entry["qr"]["png_decodes"] and abs(entry["qr"]["size_in"] - 1.9) < 0.01


def test_project_level_qr_on_a_template_without_qr_field(tmp_path):
    from pptx import Presentation
    manifest = _init(tmp_path)
    data = json.loads(manifest.read_text())
    data["artifacts"] = {"legacy": {
        "spec": {"template": "flyer", "slides": [{"layout": "Event flyer", "title": "Open lab"}]},
        "output": "legacy", "qr": {"url": "{{facts.registration_url}}", "x": 6.65, "y": 8.66, "size_in": 1.15,
                                   "name": "Registration QR code"}}}
    manifest.write_text(json.dumps(data))
    for _ in range(2):
        assert project.cmd_build(project.Project(manifest), run_lint=False) == 0
    entry = json.loads((manifest.parent / project.STATE_FILE).read_text())["artifacts"]["legacy"]
    prs = Presentation(entry["pptx"])
    qrs = [s for s in prs.slides[0].shapes if s.name == "Registration QR code"]
    assert len(qrs) == 1 and qrs[0].click_action.hyperlink.address == URL
    assert abs(qrs[0].width / 914400 - 1.15) < 0.001
    assert "printed below it" in qrs[0]._element.xpath(".//p:cNvPr")[0].get("descr")


def test_replace_asset_is_idempotent_and_scoped(tmp_path, capsys):
    from PIL import Image
    manifest = _init(tmp_path)
    new = tmp_path / "wordmark.png"
    with Image.open(SKILL / "assets/logos/ksu/ksu-wordmark-white.png") as im:
        im = im.copy()
    im.putpixel((0, 0), (1, 2, 3, 255) if im.mode == "RGBA" else (1, 2, 3))
    im.save(new)
    proj = project.Project(manifest)
    before = project._hashes(proj)
    assert project.cmd_replace_asset(proj, "ksu-wordmark-white", str(new), scope="flyer-letter", build=False) == 0
    text1 = manifest.read_text()
    after = project._hashes(project.Project(manifest))
    assert [n for n in before if before[n] != after[n]] == ["flyer-letter"]
    capsys.readouterr()
    assert project.cmd_replace_asset(project.Project(manifest), "ksu-wordmark-white", str(new),
                                     scope="flyer-letter", build=False) == 0
    assert "nothing to rebuild" in capsys.readouterr().out
    assert manifest.read_text() == text1


def test_swap_asset_uses_pptx_tools_and_is_idempotent(tmp_path):
    from PIL import Image
    from pptx import Presentation
    prs = Presentation(str(SKILL / "assets/templates/ATR-Event-Flyer-Letter.pptx"))
    match = SKILL / "assets/logos/ksu/ksu-wordmark-white.png"
    new = tmp_path / "wordmark.png"
    with Image.open(match) as im:
        im = im.copy()
    im.putpixel((0, 0), (1, 2, 3, 255) if im.mode == "RGBA" else (1, 2, 3))
    im.save(new)
    assert project.swap_asset(prs, match, match) == 0          # same bytes: nothing to do
    assert project.swap_asset(prs, match, new) >= 1
    assert project.swap_asset(prs, match, new) == 0            # nothing matches any more


# ----------------------------------------------------------------------------------------------- with LibreOffice
@needs_soffice
def test_export_verify_then_changed_only_url_revision(tmp_path, capsys):
    manifest = _init(tmp_path)
    arts = ["flyer-letter,poster-17x22"]
    assert project.cmd_build(project.Project(manifest), arts, run_lint=False) == 0
    assert project.cmd_export(project.Project(manifest), arts) == 0
    state = json.loads((manifest.parent / project.STATE_FILE).read_text())
    for name in ("flyer-letter", "poster-17x22"):
        ex = state["artifacts"][name]["export"]
        assert ex["inspection"]["tagged"]["is_tagged"]
        assert all(f["class"] != "substitute" for f in ex["inspection"]["fonts"])
        assert ex["qr_verify"]["qr_match"] and ex["qr_verify"]["link_match"]
        assert ex["size_check"]["ok"]
    new_url = "https://example.org/register-2"
    project.cmd_set(project.Project(manifest), "registration_url", new_url)
    capsys.readouterr()
    assert project.cmd_build(project.Project(manifest), arts, changed_only=True, run_lint=False) == 0
    assert project.cmd_export(project.Project(manifest), arts, changed_only=True) == 0
    out = capsys.readouterr().out
    assert out.count("re-rendered 1 of 1") == 2
    state = json.loads((manifest.parent / project.STATE_FILE).read_text())
    for name in ("flyer-letter", "poster-17x22"):
        assert qr_code.verify_pdf(state["artifacts"][name]["export"]["pdf"], new_url)["ok"]
    report = (manifest.parent / "out" / "qa-report.md").read_text()
    for heading in ("Checked in source and structure", "Verified in the exported PDF",
                    "Visual review still to do (by a person)"):
        assert heading in report


@needs_soffice
def test_hyperlink_color_regression(tmp_path):
    sys.path.insert(0, str(SCRIPTS / "examples" / "regressions" / "hyperlink-colors"))
    try:
        import check_hyperlink_colors as chk
    finally:
        sys.path.pop(0)
    res = chk.run_check(tmp_path, dpi=100)
    assert res["ok"], res["unexpected_failures"]
    by = {c["id"]: c for c in res["cases"]}
    assert by["plain-gold-on-navy"]["honored"] and by["plain-gold-on-navy"]["contrast_on_surface"] >= 4.5
    assert by["shape-link-gold-on-navy"]["honored"]
    assert len(res["links"]) >= 3
