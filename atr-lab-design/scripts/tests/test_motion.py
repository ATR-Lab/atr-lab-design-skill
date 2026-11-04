"""Tests for motion.py, banner.py --motion and deck motion backgrounds (small sizes and short clips)."""
from __future__ import annotations

import json
import zipfile
from pathlib import Path

import numpy as np
import pytest

pytest.importorskip("rlottie_python")

SCRIPTS = Path(__file__).resolve().parent.parent
SKILL = SCRIPTS.parent

import motion  # noqa: E402


@pytest.fixture(autouse=True)
def _cache(tmp_path, monkeypatch):
    monkeypatch.setenv("ATR_DESIGN_CACHE", str(tmp_path / "cache"))


def _need_ffmpeg():
    try:
        motion.ffmpeg_exe()
    except motion.MotionError:
        pytest.skip("ffmpeg not available")


def test_every_motif_file_has_its_role_layers():
    for m in motion.MOTIFS.values():
        names = {layer["nm"] for layer in motion._load(m.file)["layers"]}
        assert set(m.roles) <= names, m.name
        anim = motion._load(m.file)
        assert (anim["w"], anim["h"], anim["fr"], anim["op"]) == (1920, 1080, 30, motion.LOOP_FRAMES)
    cameo = motion._load(motion.CAMEO_FILE)
    assert cameo["op"] == motion.LOOP_FRAMES and cameo["layers"][0]["nm"] == "teo"


def test_recolor_paints_roles_hides_zero_alpha_and_keeps_mattes():
    m = motion.MOTIFS["grid-scan"]
    pal = motion.palette("grid-scan", "navy", "full")
    pal["minor"] = (pal["minor"][0], 0.0)
    out = motion.recolor(motion._load(m.file), m.roles, pal)
    layers = {layer["nm"]: layer for layer in out["layers"]}
    assert layers["grid-minor"].get("hd") is True
    assert json.dumps(layers["scan-matte"]) == json.dumps(
        next(x for x in motion._load(m.file)["layers"] if x["nm"] == "scan-matte"))
    fills = json.dumps(layers["nodes-lit"]["shapes"])
    gold = [round(c / 255, 4) for c in pal["lit"][0]]
    assert all(str(v)[:5] in fills for v in gold)


def test_unknown_motif_and_ground_are_refused():
    with pytest.raises(motion.MotionError, match="did you mean"):
        motion.motif("lattice-drfit")
    with pytest.raises(motion.MotionError):
        motion.palette("lattice-drift", "red")


def test_text_level_keeps_contrast_shift_under_limit():
    for name in motion.MOTIFS:
        for ground in motion.GROUND_NAMES:
            for strength in motion.STRENGTHS:
                pal = motion.palette(name, ground, strength)
                g = motion.B.rgb(ground)
                level = motion.text_level(pal, g)
                gn = np.array(g) / 255
                for rgb, a in pal.values():
                    mixed = gn + (np.array(rgb) / 255 - gn) * a * level
                    assert motion._shift(gn, mixed) <= motion.TEXT_SHIFT_MAX + 1e-3


def test_subtle_white_runs_at_full_level_under_text():
    assert motion.text_level(motion.palette("lattice-drift", "white", "subtle"), (255, 255, 255)) == 1.0


def test_mask_zero_on_hard_zones_and_reduced_on_text():
    z = motion.Zones(hard=[[0, 0, 40, 40]], text=[[100, 100, 160, 140]])
    m = motion.build_mask((200, 200), z, 0.4, feather=3)
    assert m[:40, :40].max() == 0
    assert abs(float(m[120, 130]) - 0.4) < 0.02
    assert m[190, 190] > 0.99


def test_cameo_placement_clears_zones_and_refuses_when_blocked():
    z = motion.Zones(text=[[0, 0, 1300, 1080]])
    x, y, side = motion.place_cameo((1920, 1080), z)
    ex = motion.cameo_extent()
    assert x + ex[0] * side >= 1300 and y + side == 1080
    band = [0, 1000, 1920, 1080]
    x, y, side = motion.place_cameo((1920, 1080), motion.Zones(hard=[band], behind=[band], floor=1000))
    assert y + side == 1000
    with pytest.raises(motion.MotionError, match="no room"):
        motion.place_cameo((1920, 1080), motion.Zones(text=[[0, 300, 1920, 1080]]))


def test_flash_meter_flags_a_strobe():
    meter = motion.FlashMeter()
    for n in range(60):
        meter.add(n, np.full((36, 64, 3), float(n % 2), dtype=np.float32))
    rep = meter.report()
    assert rep["flash_ok"] is False and rep["flashes_per_second_max"] > motion.FLASH_LIMIT


def test_full_loop_is_seamless_and_flash_free(tmp_path):
    _need_ffmpeg()
    from PIL import Image
    for name in motion.MOTIFS:
        job = motion.MotionJob(Image.new("RGB", (192, 108), motion.B.rgb("navy")), name, "navy")
        poster, rep = motion.render_job(job, tmp_path / f"{name}.mp4")
        assert rep["frames"] == motion.LOOP_FRAMES and rep["flash_ok"] and rep["loop_ok"], (name, rep)
        assert poster.size == (192, 108)
    rep = motion.check_file(tmp_path / "lattice-drift.mp4")
    assert rep["flash_ok"] and rep["frames"] == motion.LOOP_FRAMES


def test_banner_motion_keeps_the_still_design(tmp_path):
    _need_ffmpeg()
    pytest.importorskip("zxingcpp")
    import banner
    spec = {"preset": "signage-16x9", "size": "960x540", "eyebrow": "Workshop", "title": "Agentic robotics",
            "details": ["Sat., Nov. 22, 10 a.m."], "qr": "https://example.org/register", "qr_label": "Scan to register",
            "motion": "lattice-drift", "teo_cameo": True, "motion_seconds": 2}
    poster, meta = banner.render_motion(spec, tmp_path / "tv.mp4")
    assert (tmp_path / "tv.mp4").exists() and poster.size == (960, 540)
    assert meta["qr"]["decoded"] is True and meta["motion"]["flash_ok"]
    still, _ = banner.render(dict(spec, art="none"))
    tx0, ty0, tx1, ty1 = meta["text"]["box"]
    a = np.asarray(poster, dtype=float)[ty0:ty1, tx0:tx1]
    b = np.asarray(still, dtype=float)[ty0:ty1, tx0:tx1]
    assert np.abs(a - b).mean() < 4                        # text block unchanged apart from the calmed motif
    cx, cy, side = meta["motion"]["cameo_box"]
    assert cx >= tx1 or cy >= ty1


def test_banner_cameo_refused_when_no_room(tmp_path):
    _need_ffmpeg()
    import banner
    spec = {"preset": "slide-16x9", "size": "960x540", "title": "A very long title that fills the slide edge to edge",
            "subtitle": "And a subtitle", "image": str(SKILL / "assets/mascot/views/teo-front.png"),
            "image_pos": "center", "teo_cameo": True, "motion_seconds": 1}
    try:
        banner.render_motion(spec, tmp_path / "x.mp4")
    except banner.RefusedError as exc:
        assert "no room" in str(exc)


def test_deck_motion_background_is_decorative_looping_and_behind(tmp_path, monkeypatch):
    _need_ffmpeg()
    import deck_motion
    import new_deck
    monkeypatch.setattr(deck_motion, "VIDEO_PX", (320, 180))
    original = motion.MotionJob.__init__

    def short(self, *a, **k):
        original(self, *a, **k)
        self.seconds = 0.5
    monkeypatch.setattr(motion.MotionJob, "__init__", short)
    spec = json.loads((SCRIPTS / "examples/decks/minimal.json").read_text())
    spec["motion"] = "chevron-flow"
    spec["slides"][-1]["teo_cameo"] = True
    for s in spec["slides"]:
        if s.get("image"):
            s["image"] = str(SKILL / s["image"])
    spec.pop("output")
    sp = tmp_path / "deck.json"
    sp.write_text(json.dumps(spec))
    out = tmp_path / "deck.pptx"
    assert new_deck.main([str(sp), "-o", str(out)]) == 0
    with zipfile.ZipFile(out) as z:
        mp4s = [n for n in z.namelist() if n.endswith(".mp4")]
        slide1 = z.read("ppt/slides/slide1.xml").decode()
        slide2 = z.read("ppt/slides/slide2.xml").decode()
    assert len(mp4s) == 3
    for xml in (slide1, slide2):
        assert 'showMasterSp="0"' in xml and 'repeatCount="indefinite"' in xml and 'mute="1"' in xml
        tree_start = xml.index("<p:spTree>")
        first_shape = xml.index("<p:pic>", tree_start)
        assert deck_motion.SHAPE_NAME in xml[first_shape:first_shape + 400]
    from pptx import Presentation
    prs = Presentation(str(out))
    for shp in prs.slides[0].shapes:
        if shp.shape_type == 13:
            el = shp._element.find(".//{http://schemas.openxmlformats.org/presentationml/2006/main}cNvPr")
            assert el.get("descr") or "decorative" in json.dumps(str(el.xpath(".//*")))


def test_deck_motion_spec_errors():
    import deck_motion
    with pytest.raises(deck_motion.MotionSpecError):
        deck_motion.deck_config({"motif": "lattice-drift", "speed": 2})
    with pytest.raises(deck_motion.MotionSpecError):
        deck_motion.deck_config({"motif": "lattice-drift", "content": "loud"})
    deck = deck_motion.deck_config("grid-scan")
    assert deck_motion.plan(deck, {}, "ATR - Title").strength == "full"
    assert deck_motion.plan(deck, {}, "ATR - Title + Content").strength == "subtle"
    assert deck_motion.plan(deck, {"motion": "none"}, "ATR - Title") is None
    assert deck_motion.plan(deck_motion.deck_config({"motif": "grid-scan", "content": "none"}), {},
                            "ATR - Table") is None
    assert deck_motion.plan(None, {"teo_cameo": True}, "ATR - Thank You").cameo is True
