"""Tests for the WS1 toolkit: atr_brand.py, asset_index.py (+ assets/index.json), atr_design.py, banner.py and
the icons/chroma_key.py outline options. Fast and offline (no LibreOffice, no network)."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parent.parent
SKILL = SCRIPTS.parent
ASSETS = SKILL / "assets"

import asset_index as AI  # noqa: E402
import atr_brand as B  # noqa: E402
import atr_design as D  # noqa: E402


# --------------------------------------------------------------------------- atr_brand
def test_colors_come_from_tokens():
    tokens = json.loads((ASSETS / "tokens" / "colors.json").read_text())
    assert B.color("navy") == tokens["color"]["brand"]["navy"]["$value"]
    assert B.color("gold") == tokens["color"]["brand"]["gold"]["$value"]
    assert B.rgb("navy") == (0, 57, 118)
    assert B.color("gold-700") == B.color("bronze")
    assert B.color("text-primary") == B.color("ink")
    assert B.color("#003976") == "#003976"


def test_unknown_color_suggests():
    with pytest.raises(KeyError) as e:
        B.color("nvy")
    assert "navy" in str(e.value)


@pytest.mark.parametrize("role", ["sans", "sans-semibold", "sans-bold", "sans-black", "slab", "slab-bold", "mono"])
def test_font_roles(role):
    p = B.font_path(role)
    assert p.exists() and p.suffix == ".ttf"
    f = B.font(role, 32)
    assert f.size == 32


def test_font_role_unknown():
    with pytest.raises(KeyError):
        B.font_path("comic")


def test_logo_paths():
    p = B.logo_path("horizontal-short", "twotone-reverse")
    assert p.name == "atr-horizontal-short-twotone-reverse-3000.png" and p.exists()
    assert B.logo_path("roundel", "navy", fmt="svg").name == "atr-seal-navy.svg"
    assert B.logo_path("mark", "gold", size=800).name == "atr-mark-gold-1000.png"
    assert B.logo_path("horizontal", "reverse").name == "atr-horizontal-twotone-reverse-3000.png"
    assert B.logo_path("ksu", "white").name == "ksu-wordmark-white.png"
    with pytest.raises(KeyError) as e:
        B.logo_path("mark", "twotone")
    assert "variants" in str(e.value)
    with pytest.raises(KeyError):
        B.logo_path("hexagon", "navy")


def test_logo_rules_match_manifest():
    r = B.logo_rules("horizontal-short")
    assert r["min_screen_px"] == 180 and r["min_dimension"] == "width"
    assert abs(r["clear_x_over_height"] - 0.329) < 1e-6
    assert B.logo_variant_for("navy", "horizontal-short") == "twotone-reverse"
    assert B.logo_variant_for("navy", "mark") == "gold"
    assert B.logo_variant_for("white", "stacked") == "navy"


def test_icon_paths_resolve_aliases():
    p = B.icon_path("telepresence", "navy", badge=True)
    assert p.name == "telepresence-robot-badge-navy.png" and p.exists()
    assert B.icon_path("telepresence-badge-navy", badge=True).name == "telepresence-robot-badge-navy.png"
    assert B.icon_path("drone", "gold").name == "drone-uav-gold.png"
    assert B.icon_path("code", fmt="svg").name == "code.svg"
    assert B.icon_path("code", "mask").name == "code-mask.png"
    with pytest.raises(KeyError) as e:
        B.icon_path("telepresense")
    assert "telepresence-robot" in str(e.value)
    with pytest.raises(KeyError):
        B.icon_path("code", "white", badge=True)


def test_pattern_paths():
    assert B.pattern_path("hazard-tile-gold-navy").name == "hazard-tile-gold-navy-h96.png"
    assert B.pattern_path("triangle-lattice-tile-navy-on-midnight", fmt="svg").suffix == ".svg"
    with pytest.raises(KeyError):
        B.pattern_path("polka-dots")


# --------------------------------------------------------------------------- asset index
def test_index_is_current():
    fresh = AI.dumps(AI.build_index())
    assert (ASSETS / "index.json").read_text(encoding="utf-8") == fresh, \
        "assets/index.json is stale: run python3 scripts/asset_index.py"


def test_index_is_deterministic():
    assert AI.dumps(AI.build_index()) == AI.dumps(AI.build_index())


def test_index_covers_every_asset_once():
    idx = AI.build_index()
    paths = [f["path"] for r in idx["assets"] for f in r["files"]]
    assert len(paths) == len(set(paths))
    on_disk = {p.relative_to(SKILL).as_posix() for p in ASSETS.rglob("*")
               if p.is_file() and p.name not in AI.SKIP_NAMES and not p.name.startswith(".")
               and "__pycache__" not in p.parts}
    assert set(paths) == on_disk
    assert all(r["use_for"] for r in idx["assets"])
    ids = [r["id"] for r in idx["assets"]]
    assert len(ids) == len(set(ids))


def test_index_records_carry_sizes_and_minimums():
    rec = AI.get("logo/horizontal-short-navy")
    assert rec["min_px"] == 180 and rec["px"] == [3000, 1140]
    assert set(rec["formats"]) == {"png", "svg"} and len(rec["files"]) == 3
    assert AI.get("icon/teleoperation-navy")["min_px"] == 32
    assert "roundel" in AI.get("logo/seal-navy")["aliases"]
    assert "kent-state" in AI.get("ksu-wordmark/white")["aliases"]


@pytest.mark.parametrize("query,kind,expect", [
    ("telepresence-badge-navy", None, "badge/telepresence-robot-navy"),
    ("telepresence", "badge", "badge/telepresence-robot-gold"),
    ("roundel navy", None, "logo/seal-navy"),
    ("kent state", None, "ksu-wordmark/color"),
    ("hazard tile navy", None, "pattern/hazard-tile-gold-navy-h96"),
    ("drone", "icon", "icon/drone-uav-gold"),
])
def test_search(query, kind, expect):
    hits = AI.search(query, kind=kind)
    assert hits and hits[0]["id"] == expect


def test_search_miss_suggests():
    assert AI.search("telepresense badge") == []
    assert any("telepresence" in s for s in AI.suggest("telepresense badge"))


def test_readme_brace_expansion():
    assert AI._expand_braces("a-{1,2}.{svg,png}") == ["a-1.svg", "a-1.png", "a-2.svg", "a-2.png"]


# --------------------------------------------------------------------------- atr_design CLI
def run_cli(*args):
    return subprocess.run([sys.executable, str(SCRIPTS / "atr_design.py"), *args], capture_output=True, text=True,
                          env={"PYTHONDONTWRITEBYTECODE": "1", "PATH": "/usr/bin:/bin"})


def test_cli_assets_path_and_miss():
    r = run_cli("assets", "path", "telepresence", "badge", "navy")
    assert r.returncode == 0 and r.stdout.strip().endswith("telepresence-robot-badge-navy.png")
    r = run_cli("assets", "find", "zzqqxx")
    assert r.returncode == 1 and "Did you mean" in r.stderr
    r = run_cli("assets", "find", "telepresense", "--json")      # misspelt: corrected, with a note
    assert r.returncode == 0 and "showing results for" in r.stderr


def test_cli_unknown_command():
    r = run_cli("bannr")
    assert r.returncode == 1 and "banner" in r.stderr


def test_cli_missing_module_is_friendly(monkeypatch, capsys):
    monkeypatch.setitem(D.DELEGATES, "nothing", ("module_that_does_not_exist_xyz", [], "test"))
    assert D.run_delegate("nothing", []) == D.EXIT_UNAVAILABLE
    assert "not available" in capsys.readouterr().err


def test_doctor_core_runs():
    checks = D.doctor_checks(["core"])
    names = {c["check"] for c in checks}
    assert "brand fonts (assets/fonts)" in names and "cache dir writable" in names
    assert all(c["fix"] for c in checks if not c["ok"])


def test_layouts_presentation():
    pytest.importorskip("pptx")
    data = D.layout_data("presentation")
    L, _ = D._match_layout("title + content", data["layouts"])
    assert L and L["name"] == "ATR - Title + Content"
    assert {"title", "body"} <= {f["field"] for f in L["fields"]}


# --------------------------------------------------------------------------- banner
banner = pytest.importorskip("banner")


@pytest.mark.parametrize("preset", sorted(banner.PRESETS))
def test_every_preset_renders(preset):
    spec = {"preset": preset}
    if banner.PRESETS[preset].layout == "tile":
        spec["icon"] = "email"
    else:
        spec["title"] = "ATR Lab"
    img, meta = banner.render(spec)
    p = banner.PRESETS[preset]
    assert img.size == (p.w, p.h)
    if "text" in meta:
        sizes = meta["text"]["sizes_px"]
        assert sizes["title"] >= meta["floors_px"]["title"]


def test_banner_any_size_and_deterministic():
    a, _ = banner.render({"size": "777x333", "title": "Odd size"})
    b, _ = banner.render({"size": "777x333", "title": "Odd size"})
    assert a.size == (777, 333) and a.tobytes() == b.tobytes()


def test_banner_ground_is_token_navy():
    img, _ = banner.render({"preset": "github-header", "title": "x", "art": "none"})
    assert img.getpixel((800, 5)) == B.rgb("navy")


def test_banner_refuses_text_on_band():
    with pytest.raises(banner.RefusedError):
        banner.render({"preset": "discord-banner", "title": "On the band", "text_box": [40, 500, 600, 40]})


def test_banner_refuses_keep_out():
    with pytest.raises(banner.RefusedError):
        banner.render({"preset": "discord-invite-splash", "title": "Middle", "text_box": [800, 500, 400, 100]})


def test_banner_refuses_copy_that_does_not_fit():
    with pytest.raises(banner.RefusedError):
        banner.render({"preset": "thumbnail-square", "icon": "email",
                       "title": "A sentence far too long to read on a 72 pixel thumbnail"})


def test_banner_refuses_small_lockup_and_facts_and_placeholders():
    with pytest.raises(banner.RefusedError):
        banner.render({"preset": "github-header", "lockup": "horizontal", "lockup_height": 60, "title": "x"})
    with pytest.raises(banner.RefusedError):
        banner.render({"preset": "github-header", "title": "Follow @atr_kent"})
    with pytest.raises(banner.PlaceholderError):
        banner.render({"preset": "github-header", "title": "[Repo name]"})


def test_banner_lockup_keeps_clear_space_and_minimum():
    _, meta = banner.render({"preset": "github-header", "title": "x"})
    box = meta["lockup"]["box"]
    clear = meta["lockup"]["clear_x"]
    assert box[0] >= clear - 1 and box[1] >= clear - 1
    w = box[2] - box[0]
    assert w * meta["display_width"] / 1600 >= 180 - 1


def test_banner_thumbnail_glyph_reads_at_72():
    _, meta = banner.render({"preset": "thumbnail-square", "icon": "email"})
    assert meta["glyph_display_px"] >= 24


def test_banner_cli(tmp_path):
    out = tmp_path / "h.png"
    r = subprocess.run([sys.executable, str(SCRIPTS / "banner.py"), "--preset", "github-header", "--title", "Teo",
                        "--safe-zones", "-o", str(out)], capture_output=True, text=True,
                       env={"PYTHONDONTWRITEBYTECODE": "1", "PATH": "/usr/bin:/bin"})
    assert r.returncode == 0, r.stderr
    assert out.exists() and (tmp_path / "h-zones.png").exists()
    r = subprocess.run([sys.executable, str(SCRIPTS / "banner.py"), "--preset", "nope"], capture_output=True,
                       text=True)
    assert r.returncode == 1


# --------------------------------------------------------------------------- chroma_key outline
def _green_source(path):
    from PIL import Image, ImageDraw
    im = Image.new("RGB", (400, 400), (0, 255, 0))
    ImageDraw.Draw(im).rectangle([120, 120, 280, 280], fill=(255, 255, 255))
    im.save(path)


def _run_ck(*args):
    return subprocess.run([sys.executable, str(SCRIPTS / "icons" / "chroma_key.py"), *map(str, args)],
                          capture_output=True, text=True, env={"PYTHONDONTWRITEBYTECODE": "1", "PATH": "/usr/bin:/bin"})


def test_chroma_key_outline_and_die_cut(tmp_path):
    pytest.importorskip("scipy")
    pytest.importorskip("skimage")
    from PIL import Image
    src = tmp_path / "g.png"
    _green_source(src)
    plain, outl, die = tmp_path / "p.png", tmp_path / "o.png", tmp_path / "d.png"
    assert _run_ck(src, plain, "--keep-color").returncode == 0
    assert _run_ck(src, outl, "--keep-color", "--outline", "1B2533", "--outline-px", "8").returncode == 0
    assert _run_ck(src, die, "--keep-color", "--die-cut").returncode == 0
    p, o, d = (Image.open(x).convert("RGBA") for x in (plain, outl, die))
    bp, bo, bd = (im.getchannel("A").getbbox() for im in (p, o, d))
    assert bo[0] < bp[0] and bd[0] < bo[0]                     # outline grows outward; die cut further
    mid = 256
    edge = bp[0]
    assert o.getpixel((edge - 4, mid))[:3] == (27, 37, 51)       # the outline color just outside the artwork
    assert d.getpixel((bd[0] + 2, mid))[:3] == B.rgb("navy")     # navy rim on the die cut
    assert d.getpixel((edge - 6, mid))[:3] == (255, 255, 255)    # white border inside the rim
    assert o.getpixel((mid, mid))[:3] == (255, 255, 255)         # artwork untouched
