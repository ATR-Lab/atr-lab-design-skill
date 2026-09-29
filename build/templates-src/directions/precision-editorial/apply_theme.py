#!/usr/bin/env python3
"""Post-process a pptxgenjs deck: replace ppt/theme/theme1.xml with the ATR Lab Office theme
(atr-lab-design/assets/tokens/office-theme/theme1.xml), verbatim. Rewrites the zip in place.
Usage: apply_theme.py deck.pptx"""
import sys, zipfile, shutil, os, tempfile

ROOT = "/Users/marcodotio/Developer/atr-lab-design-skill"
THEME = os.path.join(ROOT, "atr-lab-design/assets/tokens/office-theme/theme1.xml")

def main(pptx):
    theme = open(THEME, "rb").read()
    tmp = tempfile.mktemp(suffix=".pptx", dir=os.path.dirname(os.path.abspath(pptx)))
    replaced = []
    with zipfile.ZipFile(pptx) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename.startswith("ppt/theme/theme") and item.filename.endswith(".xml"):
                data = theme
                replaced.append(item.filename)
            zout.writestr(item, data)
    shutil.move(tmp, pptx)
    print("theme replaced in:", ", ".join(replaced) or "NONE (no theme part found)")

if __name__ == "__main__":
    main(sys.argv[1])
