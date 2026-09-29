#!/usr/bin/env python3
"""Post-process proof-hazard-gold.pptx:
1. Replace ppt/theme/theme1.xml with the ATR Office theme (assets/tokens/office-theme/theme1.xml), verbatim.
2. Blank the alt text of decorative pictures (pptxgenjs falls back to the file path when altText is empty,
   so the generator tags them altText="decorative" and this step sets descr="")."""
import re, shutil, sys, zipfile, os

ROOT = '/Users/marcodotio/Developer/atr-lab-design-skill'
THEME = os.path.join(ROOT, 'atr-lab-design/assets/tokens/office-theme/theme1.xml')
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), 'proof-hazard-gold.pptx')
TMP = SRC + '.tmp'

theme = open(THEME, 'rb').read()
n_theme = n_decor = 0
with zipfile.ZipFile(SRC) as zin, zipfile.ZipFile(TMP, 'w', zipfile.ZIP_DEFLATED) as zout:
    for item in zin.infolist():
        data = zin.read(item.filename)
        if re.fullmatch(r'ppt/theme/theme\d+\.xml', item.filename):
            data = theme; n_theme += 1
        elif item.filename.startswith('ppt/slides/slide') and item.filename.endswith('.xml'):
            data, k = re.subn(rb'descr="decorative"', b'descr=""', data); n_decor += k
        zout.writestr(item, data)
shutil.move(TMP, SRC)
print(f'postprocess: replaced {n_theme} theme part(s), blanked {n_decor} decorative alt text(s) in {SRC}')
