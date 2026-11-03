"""Offline tests for scripts/official_assets.py and the Kent State wordmark verdicts in brand_check.py.

Nothing here touches the network: downloads are faked with monkeypatch, and the "official" files are small
fixtures registered in a temporary manifest.
"""
from __future__ import annotations

import hashlib
import io
import json
import os
import re
import urllib.error
import zipfile

import pytest

import official_assets as oa

PIL = pytest.importorskip("PIL")
from PIL import Image  # noqa: E402

SKILL_ROOT = oa.SKILL_ROOT
WORKING_WHITE = os.path.join(SKILL_ROOT, "assets", "logos", "ksu", "ksu-wordmark-white.png")
WORKING_COLOR = os.path.join(SKILL_ROOT, "assets", "logos", "ksu", "ksu-wordmark-color.png")


# --------------------------------------------------------------------------- fixtures

def _png_bytes(size=(40, 30), color=(0, 57, 118, 255), compress=6):
    im = Image.new("RGBA", size, (0, 0, 0, 0))
    im.paste(Image.new("RGBA", (size[0] - 10, size[1] - 10), color), (5, 5))
    buf = io.BytesIO()
    im.save(buf, "PNG", compress_level=compress)
    return buf.getvalue()


@pytest.fixture
def fake(tmp_path, monkeypatch):
    """A fake archive (zip with a PNG and an EPS), a manifest describing it, and an isolated cache."""
    png = _png_bytes()
    eps = b"%!PS-Adobe-3.0 EPSF-3.0\n%%BoundingBox: 0 0 10 10\n"
    zpath = tmp_path / "Fake Stacked.zip"
    with zipfile.ZipFile(zpath, "w") as z:
        z.writestr("Fake Stacked/PNGs/fake_White.png", png)
        z.writestr("Fake Stacked/EPSs/fake_White.eps", eps)
    man = {
        "schema": "atr-lab-design/official-sources/1",
        "source_page": "https://example.invalid/brand/logos",
        "archives": {"stacked": {"url": "https://example.invalid/files/Fake+Stacked.zip",
                                 "source_page": "https://example.invalid/brand/logos"}},
        "assets": [
            {"id": "ksu-stacked-white-png", "lockup": "stacked", "variant": "white", "format": "png",
             "kind": "raster", "archive": "stacked", "member": "Fake Stacked/PNGs/fake_White.png",
             "sha256": hashlib.sha256(png).hexdigest(), "bytes": len(png), "pixels": [40, 30],
             "pixel_sha256": hashlib.sha256(Image.open(io.BytesIO(png)).convert("RGBA").tobytes()).hexdigest(),
             "vector_master": "ksu-stacked-white-eps"},
            {"id": "ksu-stacked-white-eps", "lockup": "stacked", "variant": "white", "format": "eps",
             "kind": "vector", "archive": "stacked", "member": "Fake Stacked/EPSs/fake_White.eps",
             "sha256": hashlib.sha256(eps).hexdigest(), "bytes": len(eps)},
        ],
    }
    mpath = tmp_path / "official-sources.json"
    mpath.write_text(json.dumps(man))
    cache = tmp_path / "cache"
    monkeypatch.setattr(oa.time, "sleep", lambda s: None)

    def no_network(*a, **k):
        raise AssertionError("the test tried to use the network")
    monkeypatch.setattr(oa, "_download_once", no_network)
    monkeypatch.setattr(oa, "discover_archive_urls", no_network)
    return {"png": png, "eps": eps, "zip": zpath, "man": man, "manifest": str(mpath), "cache": str(cache),
            "tmp": tmp_path}


# --------------------------------------------------------------------------- the shipped manifest

def test_shipped_manifest_is_complete():
    man = oa.manifest()
    ids = [a["id"] for a in man["assets"]]
    assert len(ids) == len(set(ids))
    for need in ("ksu-stacked-color-png", "ksu-stacked-white-png", "ksu-horizontal-color-png",
                 "ksu-horizontal-white-png", "ksu-stacked-color-eps", "ksu-stacked-white-eps",
                 "ksu-horizontal-color-eps", "ksu-horizontal-white-eps"):
        assert need in ids
    assert man["terms"]["redistribution"] == "not granted"
    for a in man["assets"]:
        assert re.fullmatch(r"[0-9a-f]{64}", a["sha256"]), a["id"]
        assert a["bytes"] > 0 and a["member"] and a["retrieved"]
        assert a["archive"] in man["archives"]
        assert a["min_size"]["width_in"] >= 1.0
        assert a["intended_use"]
        if a["format"] == "png":
            assert a["pixels"][0] > 0 and re.fullmatch(r"[0-9a-f]{64}", a["pixel_sha256"])
            assert a["vector_master"] in ids
    for arch in man["archives"].values():
        assert arch["url"].startswith("https://") and arch["source_page"] == "https://www.kent.edu/brand/logos"


def test_official_files_are_not_shipped_in_the_skill():
    shipped = set()
    for d, _, files in os.walk(os.path.join(SKILL_ROOT, "assets")):
        for f in files:
            with open(os.path.join(d, f), "rb") as fh:
                shipped.add(hashlib.sha256(fh.read()).hexdigest())
    assert not shipped & {a["sha256"] for a in oa.manifest()["assets"]}


def test_default_cache_is_outside_the_skill(monkeypatch, tmp_path):
    monkeypatch.delenv("ATR_DESIGN_CACHE", raising=False)
    assert not str(oa.resolve_cache_dir()).startswith(SKILL_ROOT)
    monkeypatch.setenv("ATR_DESIGN_CACHE", str(tmp_path))
    assert oa.resolve_cache_dir() == tmp_path / "official"


# --------------------------------------------------------------------------- fetch, verify, path

def test_fetch_from_archive_verifies_and_caches(fake):
    man = oa.manifest(fake["manifest"])
    p = oa.fetch("ksu-stacked-white-png", fake["cache"], man, archive=str(fake["zip"]))
    assert p.name == "ksu-stacked-white.png" and p.read_bytes() == fake["png"]
    assert oa.path("ksu-stacked-white-png", fake["cache"], man) == p
    assert oa.path("ksu-stacked-white-eps", fake["cache"], man) is None
    # cached and matching: no archive and no network needed the second time
    assert oa.fetch("ksu-stacked-white-png", fake["cache"], man) == p
    assert oa.verify(p, man)["id"] == "ksu-stacked-white-png"


def test_fetch_rejects_a_changed_file(fake):
    man = json.loads(json.dumps(fake["man"]))
    man["assets"][0]["sha256"] = "0" * 64
    with pytest.raises(oa.ChecksumError):
        oa.fetch("ksu-stacked-white-png", fake["cache"], man, archive=str(fake["zip"]))
    assert not os.path.exists(os.path.join(fake["cache"], "ksu-stacked-white.png"))


def test_fetch_missing_member_and_unknown_id(fake):
    man = json.loads(json.dumps(fake["man"]))
    man["assets"][0]["member"] = "Fake Stacked/PNGs/gone.png"
    with pytest.raises(oa.OfficialAssetError, match="no member"):
        oa.fetch("ksu-stacked-white-png", fake["cache"], man, archive=str(fake["zip"]))
    with pytest.raises(oa.OfficialAssetError, match="Unknown asset id"):
        oa.fetch("ksu-nope", fake["cache"], man)


def test_network_failure_retries_and_explains(fake, monkeypatch):
    calls = []

    def fail(url, dest):
        calls.append(url)
        raise urllib.error.URLError("temporary failure in name resolution")

    def page_fail(page, kw):
        raise urllib.error.URLError("offline")
    monkeypatch.setattr(oa, "_download_once", fail)
    monkeypatch.setattr(oa, "discover_archive_urls", page_fail)
    man = oa.manifest(fake["manifest"])
    with pytest.raises(oa.NetworkError) as e:
        oa.fetch("ksu-stacked-white-png", fake["cache"], man)
    assert len(calls) == oa.RETRIES
    msg = str(e.value)
    assert "not evidence that the official artwork is unavailable" in msg
    assert "--archive" in msg and e.value.exit_code == 3


def test_failed_url_then_link_from_source_page(fake, monkeypatch):
    alt = "https://example.invalid/brand/Fake-Stacked-v2.zip"

    def dl(url, dest):
        if url != alt:
            raise urllib.error.HTTPError(url, 403, "Forbidden", None, None)
        dest.write_bytes(fake["zip"].read_bytes())
    monkeypatch.setattr(oa, "_download_once", dl)
    monkeypatch.setattr(oa, "discover_archive_urls", lambda page, kw: [alt])
    p = oa.fetch("ksu-stacked-white-png", fake["cache"], oa.manifest(fake["manifest"]))
    assert p.read_bytes() == fake["png"]


def test_cli_list_path_verify(fake, capsys):
    base = ["--manifest", fake["manifest"], "--cache-dir", fake["cache"]]
    assert oa.main(base + ["path", "ksu-stacked-white-png"]) == 1
    assert "fetch ksu-stacked-white-png" in capsys.readouterr().err
    assert oa.main(base + ["fetch", "all", "--archive", str(fake["zip"])]) == 0
    capsys.readouterr()
    assert oa.main(base + ["--json", "list"]) == 0
    rows = json.loads(capsys.readouterr().out)["assets"]
    assert all(r["cached"] for r in rows)
    cached = os.path.join(fake["cache"], "ksu-stacked-white.png")
    assert oa.main(base + ["verify", cached]) == 0
    assert "verified (ksu-stacked-white-png" in capsys.readouterr().out
    other = fake["tmp"] / "other.png"
    other.write_bytes(_png_bytes(color=(239, 171, 0, 255)))
    assert oa.main(base + ["verify", str(other)]) == 1
    assert "provenance is not verified" in capsys.readouterr().out
    assert oa.main(base + ["fetch", "ksu-nope"]) == 2


# --------------------------------------------------------------------------- identify and overrides

def test_identify_official_working_copy_unknown(fake):
    man = oa.manifest(fake["manifest"])
    assert oa.identify(fake["png"], man=man)["status"] == "official"
    # same pixels, different encoding: official by pixels, not by checksum
    resaved = Image.open(io.BytesIO(fake["png"]))
    buf = io.BytesIO()
    resaved.save(buf, "PNG", compress_level=1)
    assert buf.getvalue() != fake["png"]
    r = oa.identify(buf.getvalue(), man=man)
    assert (r["status"], r["how"]) == ("official", "pixels")
    assert oa.identify(buf.getvalue(), man=man, pixels=False)["status"] == "unknown"
    with open(WORKING_WHITE, "rb") as f:
        w = oa.identify(f.read(), man=man)
    assert (w["status"], w["replacement"]) == ("working-copy", "ksu-stacked-white-png")
    assert oa.identify(_png_bytes(color=(1, 2, 3, 255)), man=man)["status"] == "unknown"


def test_overrides_accept_provenance_map_and_image(fake, tmp_path):
    img = tmp_path / "downloaded.png"
    img.write_bytes(_png_bytes(color=(9, 9, 9, 255)))
    prov = tmp_path / "brand-asset-sources.json"
    prov.write_text(json.dumps({"kent-state-white.png": {"sha256": "AB" * 32, "source": "https://x"}}))
    ov = oa.load_overrides([str(img), str(prov)])
    assert {o["id"] for o in ov} == {"downloaded.png", "kent-state-white.png"}
    assert "ab" * 32 in {o["sha256"] for o in ov}
    r = oa.identify(img.read_bytes(), overrides=ov, man=oa.manifest(fake["manifest"]))
    assert (r["status"], r["source"]) == ("official", str(img))
    with pytest.raises(oa.OfficialAssetError):
        oa.load_overrides([str(tmp_path / "missing.json")])


# --------------------------------------------------------------------------- brand_check verdicts

@pytest.fixture
def bc():
    import brand_check
    brand_check._OVERRIDES.clear()
    return brand_check


def _ksu_findings(bc, capsys, argv):
    capsys.readouterr()
    bc.main(["--json"] + argv)
    rep = json.loads(capsys.readouterr().out)
    return [f for f in rep["findings"] if f["check"] == "logo-ksu"]


def _altered_working_copy(path):
    """The working copy with a few pixels changed: same shape (dHash), different file and pixels."""
    im = Image.open(WORKING_WHITE).convert("RGBA")
    for x in range(5):
        im.putpixel((x, 0), (255, 255, 255, 255))
    im.save(path)
    return path


def test_brand_check_three_distinct_verdicts(bc, capsys, tmp_path):
    altered = _altered_working_copy(tmp_path / "ksu-from-somewhere.png")
    wc = _ksu_findings(bc, capsys, [WORKING_WHITE])
    un = _ksu_findings(bc, capsys, [str(altered)])
    bc._OVERRIDES.clear()
    off = _ksu_findings(bc, capsys, ["--official-manifest", str(altered), str(altered)])
    verdicts = [(f[0]["where"]["provenance"], f[0]["severity"]) for f in (off, wc, un)]
    # on a deliverable the draft logo is a warning; the other two verdicts are info
    assert verdicts == [("official", "info"), ("working-copy", "warning"), ("unknown", "info")]
    msgs = [f[0]["message"] for f in (off, wc, un)]
    assert msgs[0].startswith("Official Kent State wordmark, verified (ksu-from-somewhere.png")
    assert "working copy" in msgs[1] and "not the official file" in msgs[1]
    assert "provenance not verified" in msgs[2]
    assert "working copy" not in msgs[0] and "working copy" not in msgs[2].split("(no exact")[0]
    assert "official_assets.py fetch ksu-stacked-white-png" in wc[0]["fix"]
    assert "official_assets.py verify" in un[0]["fix"]
    # an official verdict carries no warning
    assert not [f for f in off if f["severity"] != "info"]


def test_brand_check_official_from_shipped_manifest_checksum(bc, monkeypatch, tmp_path, capsys):
    """A file whose SHA-256 is in the manifest is official even though it looks like the working copy."""
    altered = _altered_working_copy(tmp_path / "official.png")
    digest = hashlib.sha256(altered.read_bytes()).hexdigest()
    man = {"assets": [{"id": "ksu-stacked-white-png", "lockup": "stacked", "format": "png", "kind": "raster",
                       "sha256": digest, "vector_master": "ksu-stacked-white-eps"}]}
    monkeypatch.setattr(oa, "manifest", lambda path=None: man)
    f = _ksu_findings(bc, capsys, [str(altered)])
    assert f[0]["where"]["provenance"] == "official"
    assert "verified (ksu-stacked-white-png; exact SHA-256" in f[0]["message"]


@pytest.mark.parametrize("mode", ["--template", "--guidance"])
def test_brand_check_working_copy_is_info_in_template_and_guidance_mode(bc, capsys, tmp_path, mode):
    altered = _altered_working_copy(tmp_path / "ksu-from-somewhere.png")
    wc = _ksu_findings(bc, capsys, [mode, WORKING_WHITE])
    assert [(f["where"]["provenance"], f["severity"]) for f in wc] == [("working-copy", "info")]
    un = _ksu_findings(bc, capsys, [mode, str(altered)])
    assert [(f["where"]["provenance"], f["severity"]) for f in un] == [("unknown", "info")]


def _summary(bc, capsys, argv):
    capsys.readouterr()
    code = bc.main(["--json"] + argv)
    return code, json.loads(capsys.readouterr().out)["summary"]


def test_strict_blocks_a_deliverable_with_the_working_copy(bc, capsys, tmp_path):
    for logo, name in ((WORKING_COLOR, "draft.pptx"), (str(_altered_working_copy(tmp_path / "x.png")), "unk.pptx")):
        deck = _pptx_with_logo(tmp_path, logo, 1.06, name)
        f = _ksu_findings(bc, capsys, [str(deck)])
        _, deliverable = _summary(bc, capsys, [str(deck)])
        _, template = _summary(bc, capsys, ["--template", str(deck)])
        if logo == WORKING_COLOR:
            assert [(x["where"]["provenance"], x["severity"]) for x in f] == [("working-copy", "warning")]
            assert deliverable["warning"] == template["warning"] + 1
            assert bc.main(["--strict", str(deck)]) == 1
        else:  # provenance not verified stays info in both modes
            assert [(x["where"]["provenance"], x["severity"]) for x in f] == [("unknown", "info")]
            assert deliverable["warning"] == template["warning"]
    capsys.readouterr()


def _pptx_with_logo(tmp_path, img_path, width_in, name="flyer.pptx"):
    pptx = pytest.importorskip("pptx")
    from pptx.util import Inches
    prs = pptx.Presentation()
    prs.slide_width, prs.slide_height = Inches(8.5), Inches(11)
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    pic = slide.shapes.add_picture(str(img_path), Inches(6), Inches(0.5), width=Inches(width_in))
    pic._element.nvPicPr.cNvPr.set("descr", "Kent State University")
    out = tmp_path / name
    prs.save(out)
    return out


def test_brand_check_effective_ppi_and_minimum_size(bc, capsys, tmp_path):
    ok = _pptx_with_logo(tmp_path, WORKING_COLOR, 1.06, "ok.pptx")
    f = _ksu_findings(bc, capsys, ["--template", str(ok)])  # template mode: the working copy itself is info
    assert [x["severity"] for x in f] == ["info"]
    assert "ppi effective, fine for print documents" in f[0]["message"]
    small = Image.open(WORKING_COLOR).resize((128, 122), Image.LANCZOS)
    lowres = tmp_path / "ksu-small.png"
    small.save(lowres)
    soft = _pptx_with_logo(tmp_path, lowres, 1.06, "soft.pptx")
    f = _ksu_findings(bc, capsys, ["--template", str(soft)])
    warn = [x for x in f if x["severity"] == "warning"]
    assert len(warn) == 1 and "below the 200 ppi minimum for print documents" in warn[0]["message"]
    tiny = _pptx_with_logo(tmp_path, WORKING_COLOR, 0.8, "tiny.pptx")
    f = _ksu_findings(bc, capsys, ["--template", str(tiny)])
    warn = [x for x in f if x["severity"] == "warning"]
    assert len(warn) == 1 and "under Kent State's minimum of 1.05 in" in warn[0]["message"]


def test_brand_check_still_flags_retired_marks(bc):
    # perceptual matching for prohibited marks is unchanged
    rids = {r[0] for r in bc.LOGO_REFS}
    assert {"retired-block-atr", "athletic-flash", "ksu-wordmark"} <= rids
    assert bc.LOGO_INFO["athletic-flash"][0] == "error" and bc.LOGO_INFO["retired-block-atr"][0] == "error"
