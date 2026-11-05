"""scripts/permission_slip.py: the slip builds from the letterhead, lints clean, keeps its two pages and its rules,
and fills one event's details. Offline; no LibreOffice (the PDF export is not exercised)."""
from __future__ import annotations

import json
import re
import subprocess
import sys
import zipfile
from pathlib import Path

import permission_slip as P

SCRIPTS = Path(__file__).resolve().parents[1]
SKILL = SCRIPTS.parent
WORKING_COPY = SKILL / "assets" / "logos" / "ksu" / "ksu-wordmark-color.png"


def _build(tmp_path, *args):
    out = tmp_path / "slip.docx"
    assert P.main(["-o", str(out), *args]) == 0
    with zipfile.ZipFile(out) as z:
        parts = {n: z.read(n).decode("utf-8", "replace") for n in z.namelist() if n.endswith(".xml")}
    text = re.sub(r"<[^>]+>", "", parts["word/document.xml"])
    return out, parts, text


def _lint(path):
    r = subprocess.run([sys.executable, str(SCRIPTS / "brand_check.py"), str(path), "--json"],
                       capture_output=True, text=True, timeout=120)
    data = json.loads(r.stdout)
    report = data[0] if isinstance(data, list) else data
    return [f for f in report["findings"] if f["severity"] == "error"]


def test_blank_slip_has_two_pages_the_rules_and_no_lint_errors(tmp_path):
    out, parts, text = _build(tmp_path)
    assert parts["word/document.xml"].count("<w:pageBreakBefore/>") == 1
    assert "only if your child is 14 or older" in text and "one to one" in text
    assert "Jong-Hoon Kim (jkim72@kent.edu)" in text
    assert "Saying no changes nothing" in text and "publish your child's name or school" in text
    assert "[lab contact: name, kent.edu email]" in text
    assert "Policy 3342-5-19" in parts["word/footer1.xml"]
    assert "Kent State University" in parts["word/header1.xml"]
    assert "word/media/6d2a10a3363ae9fd5078839d2b8ab327439e6fc3.png" not in zipfile.ZipFile(out).namelist()
    assert _lint(out) == []


def test_event_details_wordmark_and_final(tmp_path):
    out, parts, text = _build(tmp_path, "--event", "Open lab", "--date", "Nov. 20, 2026",
                              "--contact", "Pat Doe, pdoe@kent.edu", "--sticker", "a red sticker",
                              "--removal-days", "5", "--ksu-wordmark", str(WORKING_COPY), "--final")
    assert "Open lab" in text and "Nov. 20, 2026" in text
    assert "Pat Doe, pdoe@kent.edu" in text and "a red sticker" in text and "within 5 business days" in text
    assert "[" not in text
    assert "Draft" not in parts["word/footer1.xml"]
    assert 'cx="971550"' in parts["word/header1.xml"]


def test_refuses_to_write_inside_the_skill():
    assert P.main(["-o", str(SCRIPTS / "slip.docx")]) == 2
    assert not (SCRIPTS / "slip.docx").exists()
