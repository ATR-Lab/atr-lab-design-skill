"""Regression set for scripts/pptx_tools.py: inherited placeholders, two-line titles, fixed line spacing,
logo replacement, QR placement and repeated edits being no-ops. Offline; uses the shipped templates."""
from __future__ import annotations

import hashlib
import os
from pathlib import Path

import pytest
from pptx import Presentation
from pptx.oxml.ns import qn

import pptx_tools as T

SKILL = Path(__file__).resolve().parents[2]
TEMPLATES = SKILL / "assets" / "templates"
EVENT = TEMPLATES / "ATR-Event-Flyer-Letter.pptx"
LEGACY = TEMPLATES / "ATR-Flyer-Letter.pptx"
EMU_IN = 914400


def _png(path, size=(200, 100), color=(180, 30, 30)):
    from PIL import Image
    Image.new("RGB", size, color).save(path)
    return path


def _layout_shape(prs, name):
    for lay in prs.slide_layouts:
        for shp in lay.shapes:
            if shp.name == name:
                return shp
    raise AssertionError(f"no layout shape {name!r}")


# --------------------------------------------------------------------------- titles and fields

def test_find_title_by_type_where_shapes_title_fails():
    slide = Presentation(str(LEGACY)).slides[0]
    assert slide.shapes.title is None            # the legacy flyer's title has idx 109, not 0
    title = T.find_title(slide)
    assert title is not None
    assert "Physical AI" in title.text_frame.text


def test_field_names_from_layout_json_and_legacy_aliases():
    prs = Presentation(str(EVENT))
    names = T.field_names(prs.slide_layouts[0])
    assert names[0] == "event_title" and names[103] == "event_date" and names[119] == "registration_qr"
    legacy = Presentation(str(LEGACY))
    lnames = T.field_names(legacy.slide_layouts[0])
    assert lnames[128] == "cta_url"              # semantic name from flyer-layouts.json
    slide = legacy.slides[0]
    assert T.find_field(slide, "ph128")._element is T.find_field(slide, "cta_url")._element   # ph<idx> still resolves


def test_set_named_field_is_idempotent_and_keeps_formatting(tmp_path):
    prs = Presentation(str(EVENT))
    slide = prs.slides[0]
    shp = T.find_field(slide, "event_title")
    before_ppr = shp.text_frame._txBody.find(qn("a:p")).find(qn("a:pPr"))
    assert T.set_named_field(slide, "event_title", "Two-line\ntitle") is True
    assert T.set_named_field(slide, "event_title", "Two-line\ntitle") is False      # second application: no-op
    paras = shp.text_frame.paragraphs
    assert [p.text for p in paras] == ["Two-line", "title"]
    after_ppr = shp.text_frame._txBody.find(qn("a:p")).find(qn("a:pPr"))
    assert (before_ppr is None) == (after_ppr is None)
    out = tmp_path / "t.pptx"
    prs.save(str(out))
    assert T.find_field(Presentation(str(out)).slides[0], "event_title").text_frame.text == "Two-line\ntitle"


def test_set_named_field_unknown_name_lists_fields():
    slide = Presentation(str(EVENT)).slides[0]
    with pytest.raises(T.ToolError) as exc:
        T.set_named_field(slide, "nope", "x")
    assert "event_date" in str(exc.value)


# --------------------------------------------------------------------------- scaling

def test_snapshot_marks_inherited_placeholders():
    prs = Presentation(str(EVENT))
    snap = T.snapshot_geometry(prs)
    slide_entries = [v for v in snap.values() if v["kind"] == "slide" and "placeholder" in v]
    assert slide_entries and all(v["inherited"] for v in slide_entries)
    layout_entries = {v["placeholder"]["idx"]: v for v in snap.values() if v["kind"] == "layout" and "placeholder" in v}
    for v in slide_entries:
        assert v["left"] == layout_entries[v["placeholder"]["idx"]]["left"]


def test_scale_inherited_once_and_typography_together(tmp_path):
    prs = Presentation(str(EVENT))
    before = T.snapshot_geometry(prs)
    ksu = _layout_shape(prs, "Kent State signature")
    ratio0 = ksu.width / ksu.height
    alt0 = ksu._element.xpath(".//p:cNvPr")[0].get("descr")
    title_layout = next(p for p in prs.slide_layouts[0].placeholders if p.placeholder_format.idx == 0)
    ln0 = int(title_layout._element.find(".//" + qn("a:lnSpc") + "/" + qn("a:spcPts")).get("val"))
    sz0 = int(title_layout._element.find(".//" + qn("a:defRPr")).get("sz"))
    rep = T.scale_presentation(prs, 2.0)
    assert rep["mismatches"] == [] and rep["page_in"] == [17.0, 22.0]
    after = T.snapshot_geometry(prs)
    for key, old in before.items():
        new = after[key]
        if old["left"] is None:
            continue
        assert abs(new["left"] - old["left"] * 2) <= 2 and abs(new["height"] - old["height"] * 2) <= 2, key
        assert new["inherited"] == old["inherited"]          # slide placeholders still follow the layout
    assert abs(ksu.width / ksu.height - ratio0) < 1e-6         # picture aspect preserved
    assert ksu._element.xpath(".//p:cNvPr")[0].get("descr") == alt0
    assert int(title_layout._element.find(".//" + qn("a:lnSpc") + "/" + qn("a:spcPts")).get("val")) == ln0 * 2
    assert int(title_layout._element.find(".//" + qn("a:defRPr")).get("sz")) == sz0 * 2
    # the two-line showcase title survives as two paragraphs
    title = T.find_title(prs.slides[0])
    assert len(title.text_frame.paragraphs) == 2
    out = tmp_path / "big.pptx"
    prs.save(str(out))
    assert Presentation(str(out)).slide_width == 17 * EMU_IN


def test_scale_twice_is_not_a_double_scale_of_slide_placeholders():
    prs = Presentation(str(EVENT))
    ph = next(p for p in prs.slides[0].placeholders if p.placeholder_format.idx == 103)
    left0 = ph.left
    T.scale_presentation(prs, 1.5)
    assert abs(ph.left - left0 * 1.5) <= 2


def test_type_floor_report_and_lift():
    prs = Presentation(str(EVENT))
    T.scale_presentation(prs, 2.0)                               # 17 x 22: brand_check calls it a poster
    low = T.type_floor_report(prs)
    assert low and all(item["floor_pt"] == 24.0 and item["size_pt"] < 24 for item in low)
    n = T.lift_type_floor(prs, 24.0)
    assert n > 0
    assert T.type_floor_report(prs) == []
    assert T.lift_type_floor(prs, 24.0) == 0                      # idempotent


def test_17x22_profile_already_meets_the_poster_floor():
    prs = Presentation(str(TEMPLATES / "ATR-Event-Flyer-17x22.pptx"))
    assert T.type_floor_report(prs) == []


# --------------------------------------------------------------------------- pictures

def test_replace_picture_by_name_keeps_height_anchor_and_alt(tmp_path):
    prs = Presentation(str(EVENT))
    ksu = _layout_shape(prs, "Kent State signature")
    right0, h0 = ksu.left + ksu.width, ksu.height
    alt0 = ksu._element.xpath(".//p:cNvPr")[0].get("descr")
    new = _png(tmp_path / "wide.png", (200, 100))
    res = T.replace_picture(prs, "Kent State signature", new)
    assert [r["status"] for r in res] == ["replaced"]
    assert ksu.height == h0 and abs(ksu.width - h0 * 2) <= 2 and abs(ksu.left + ksu.width - right0) <= 2
    assert ksu._element.xpath(".//p:cNvPr")[0].get("descr") == alt0
    blob = prs.slide_layouts[0].part.related_part(ksu._element.xpath(".//a:blip/@r:embed")[0]).blob
    assert hashlib.sha256(blob).hexdigest() == hashlib.sha256(new.read_bytes()).hexdigest()
    res2 = T.replace_picture(prs, "Kent State signature", new)
    assert [r["status"] for r in res2] == ["unchanged"]          # second application changes nothing
    out = tmp_path / "r.pptx"
    prs.save(str(out))
    Presentation(str(out))


def test_replace_picture_by_sha256_and_scope(tmp_path):
    prs = Presentation(str(EVENT))
    atr = _layout_shape(prs, "ATR signature")
    blob = prs.slide_layouts[0].part.related_part(atr._element.xpath(".//a:blip/@r:embed")[0]).blob
    sha = hashlib.sha256(blob).hexdigest()
    new = _png(tmp_path / "logo.png", (300, 114))
    assert T.replace_picture(prs, sha, new, scope="slides") == []          # nothing on slides carries it
    res = T.replace_picture(prs, sha, new, scope="layouts")
    assert res and all(r["status"] == "replaced" for r in res)


def test_place_qr_is_idempotent_by_name(tmp_path):
    prs = Presentation(str(EVENT))
    slide = prs.slides[0]
    n0 = len(slide.shapes)
    png1 = _png(tmp_path / "q1.png", (120, 120), (0, 0, 0))
    pic = T.place_qr(slide, png1, name="QR code", box=(1, 1, 1, 1), url="https://example.org/r")
    assert len(slide.shapes) == n0 + 1 and pic.click_action.hyperlink.address == "https://example.org/r"
    assert "example.org" in pic._element.xpath(".//p:cNvPr")[0].get("descr")
    rels0 = len(slide.part.rels)
    T.place_qr(slide, png1, name="QR code", box=(1, 1, 1, 1), url="https://example.org/r")
    assert len(slide.shapes) == n0 + 1 and len(slide.part.rels) == rels0     # no duplicate shape or part
    png2 = _png(tmp_path / "q2.png", (120, 120), (0, 0, 60))
    pic2 = T.place_qr(slide, png2, name="QR code", url="https://example.org/r")
    assert len(slide.shapes) == n0 + 1 and pic2.left == pic.left and pic2.width == pic.width


# --------------------------------------------------------------------------- CLI

def test_cli_fields_and_scale(tmp_path, capsys):
    assert T.main(["fields", str(EVENT), "--slide", "1"]) == 0
    out = capsys.readouterr().out
    assert "event_date" in out and "title (by type)" in out
    big = tmp_path / "big.pptx"
    assert T.main(["scale", str(EVENT), "-o", str(big), "--page", "17x22", "--min-pt", "24"]) == 0
    assert "lifted" in capsys.readouterr().out
    assert Presentation(str(big)).slide_height == 22 * EMU_IN
    png = _png(tmp_path / "p.png")
    assert T.main(["replace-picture", str(EVENT), "--match", "no-such-picture", "--with", str(png), "-o", str(tmp_path / "x.pptx")]) == 2
    assert not os.path.exists(tmp_path / "x.pptx")
