"""The event/workshop flyer: authored from a content spec by field name (no placeholder indices, no
coordinates), at Letter, Tabloid and 17 x 22 in; QR and tools fields; defaults; legacy flyer aliases."""
from __future__ import annotations

import json
import re
import subprocess
import sys
import types
from pathlib import Path

import pytest
from pptx import Presentation

import new_deck

SKILL = Path(__file__).resolve().parents[2]
SPEC = SKILL / "scripts" / "examples" / "print" / "event-workshop.json"
EMU_IN = 914400


@pytest.fixture
def fake_qr(monkeypatch):
    """A stand-in qr_code module (same make_qr contract) so the tests need neither WS3's file nor a QR library."""
    mod = types.ModuleType("qr_code")
    calls = []

    def make_qr(url, out_path, size_in=1.0, dpi=600, ecc="M", quiet=4, dark="#003976", light="#FFFFFF"):
        from PIL import Image, ImageDraw
        px = int(round(size_in * dpi))
        im = Image.new("RGB", (px, px), light)
        d = ImageDraw.Draw(im)
        q = px // 10
        d.rectangle([q, q, px - q, px - q], outline=dark, width=max(2, px // 40))
        Path(out_path).parent.mkdir(parents=True, exist_ok=True)
        im.save(out_path)
        calls.append((url, size_in, dpi))
        return Path(out_path)

    mod.make_qr = make_qr
    mod.calls = calls
    monkeypatch.setitem(sys.modules, "qr_code", mod)
    return mod


def _build(spec_path, out, *args):
    return new_deck.main([str(spec_path), "-o", str(out), *args])


@pytest.mark.parametrize("template", ["event-flyer", "event-flyer-tabloid", "event-flyer-17x22"])
def test_workshop_flyer_from_content_spec(tmp_path, fake_qr, template):
    out = tmp_path / f"{template}.pptx"
    assert _build(SPEC, out, "--template", template) == 0
    prs = Presentation(str(out))
    assert len(prs.slides) == 1
    slide = prs.slides[0]
    by_name = {s.name: s for s in slide.shapes}
    # named fields on the slide, filled from the spec
    assert by_name["event_title"].text_frame.text == "Build robots\nwith AI agents"
    assert by_name["event_date"].text_frame.text == "Saturday, Nov. 7, 2026"
    assert by_name["venue"].text_frame.text.startswith("Mathematical Sciences Building")
    # workflow spread over three steps, detail at level 2
    step = by_name["step1"].text_frame
    assert [p.text for p in step.paragraphs] == ["Inspect", "Understand the failing case"]
    assert step.paragraphs[1].level == 1
    # defaults that follow other fields
    assert by_name["agenda_title"].text_frame.text == "What you will do"
    assert by_name["tools_label"].text_frame.text == "TOOLS COVERED"
    assert by_name["registration_label"].text_frame.text == "SCAN TO REGISTER"
    assert by_name["registration_url"].text_frame.text == "example.org/register"
    # QR: generated through qr_code.make_qr at the slot's size, hyperlinked, alt text names the URL
    qr = by_name["registration_qr"]
    assert qr.click_action.hyperlink.address == "https://example.org/register"
    assert "example.org/register" in qr._element.xpath(".//p:cNvPr")[0].get("descr")
    assert fake_qr.calls and fake_qr.calls[-1][0] == "https://example.org/register"
    assert abs(qr.width - qr.height) <= 2                                  # square, not cropped
    # tools row: icons kept as pictures with plain labels, inside the layout's region
    assert by_name["Tool 1 label"].text_frame.text == "Claude Code" and by_name["Tool 2 label"].text_frame.text == "Codex"
    region = json.loads((SKILL / "assets" / "templates" / f"event-flyer-{template.split('event-flyer')[1].strip('-') or 'letter'}-layouts.json").read_text())
    box = region["layouts"][0]["regions"]["tools_row"]["box_in"]
    for n in (1, 2):
        icon = by_name[f"Tool {n} icon"]
        assert box["x"] * EMU_IN - 2 <= icon.left and icon.left + icon.width <= (box["x"] + box["w"]) * EMU_IN + 2
        assert icon._element.xpath(".//p:cNvPr")[0].get("descr")
    # nothing on the hazard band, signatures separate from each other and from the tools row
    band_h = prs.slide_width / 20
    for shp in slide.shapes:
        assert shp.top >= band_h + 0.25 * EMU_IN, shp.name
    lay = {s.name: s for s in slide.slide_layout.shapes}
    atr, ksu = lay["ATR signature"], lay["Kent State signature"]
    assert atr.left + atr.width < ksu.left - 0.5 * EMU_IN
    assert ksu.top + ksu.height < by_name["Tool 1 icon"].top
    # no leftover prompts
    for shp in slide.shapes:
        if shp.has_text_frame:
            assert "[" not in shp.text_frame.text, shp.name


def test_spec_uses_names_only():
    spec = json.loads(SPEC.read_text())
    for sl in spec["slides"]:
        for key, value in sl.items():
            assert not re.fullmatch(r"ph\d+", key), key
            assert key not in ("images", "textboxes", "shapes"), key
            assert not (isinstance(value, dict) and "box" in value), key


def test_qr_alias_and_missing_qr_module(tmp_path, fake_qr, monkeypatch):
    spec = json.loads(SPEC.read_text())
    sl = spec["slides"][0]
    sl["qr"] = sl.pop("registration_qr")["qr"]
    p = tmp_path / "alias.json"
    p.write_text(json.dumps(spec))
    out = tmp_path / "alias.pptx"
    assert _build(p, out) == 0
    names = {s.name for s in Presentation(str(out)).slides[0].shapes}
    assert "registration_qr" in names
    # without a qr_code module the build stops with a clear message instead of a traceback
    monkeypatch.setitem(sys.modules, "qr_code", None)
    assert _build(p, tmp_path / "noqr.pptx", "--template", "event-flyer") == 1


def test_qr_needs_full_url(tmp_path, fake_qr):
    spec = json.loads(SPEC.read_text())
    spec["slides"][0]["registration_qr"] = {"qr": {"url": "forms.gle/abc"}}
    p = tmp_path / "bad.json"
    p.write_text(json.dumps(spec))
    assert _build(p, tmp_path / "bad.pptx") == 1


def test_partial_workflow_warns_about_fixed_plates(tmp_path, fake_qr, capsys):
    spec = json.loads(SPEC.read_text())
    spec["slides"][0]["workflow"] = [["Inspect", "Only one step"]]
    p = tmp_path / "one.json"
    p.write_text(json.dumps(spec))
    assert _build(p, tmp_path / "one.pptx") == 0
    assert "1 of 3 workflow steps" in capsys.readouterr().out


def test_legacy_flyer_fields_by_name_and_by_index(tmp_path):
    tpl = new_deck.Template("flyer")
    slots = tpl.slots(tpl.find_layout("Event flyer"))
    assert new_deck.lookup(slots, "cta_url").idx == 128
    assert new_deck.lookup(slots, "ph128").idx == 128
    assert new_deck.lookup(slots, "when").idx == 113


def test_existing_example_deck_still_builds(tmp_path):
    out = tmp_path / "minimal.pptx"
    assert new_deck.main([str(SKILL / "scripts" / "examples" / "decks" / "minimal.json"), "-o", str(out)]) == 0
    assert len(Presentation(str(out)).slides) == 3


def test_brand_check_passes_on_the_built_flyer(tmp_path, fake_qr):
    out = tmp_path / "flyer.pptx"
    assert _build(SPEC, out) == 0
    res = subprocess.run([sys.executable, str(SKILL / "scripts" / "brand_check.py"), str(out)],
                         capture_output=True, text=True, env={"PYTHONDONTWRITEBYTECODE": "1", "PATH": "/usr/bin:/bin"})
    assert res.returncode == 0, res.stdout + res.stderr
    assert "0 error(s)" in res.stdout
