#!/usr/bin/env python3
"""Brand-font text-fit check for the ATR print collateral (the judges' measure.py step).

Two modes:
  measure.py "text" <font-key> <pt>            -> printed width in inches (Source Sans 3 and Arial fallback)
  measure.py --check deck.pptx [--min-slack 0.0] [--min-scale 0.7] [--quiet]
       walks every text box on slides and slide layouts, estimates the lines each paragraph needs in the
       brand font (and in Arial, ~8-9% wider), and flags boxes whose estimated text height exceeds the box
       height. Boxes with "Shrink text on overflow" (<a:normAutofit/>) are allowed to overflow as long as the
       shrink needed to fit stays at or above --min-scale (PowerPoint reduces the type in steps down to that
       size); they are reported as "autofit: shrinks to NN%" and only flagged below the floor. Estimates use
       real advance widths and the exact line spacing written in the XML (spcPts) or 1.2 x size when none is set.

Font keys: sans, sans-bold, black, semibold, slab, slab-bold, slab-semi, mono, arial, arial-bold.
Fonts resolve from atr-lab-design/assets/fonts (shipped with the skill), then the session fontlib as a fallback.
"""
import sys, re, os, zipfile
from fontTools.ttLib import TTFont
from defusedxml import ElementTree as ET

ROOT = '/Users/marcodotio/Developer/atr-lab-design-skill'
FONT_DIRS = [
    os.path.join(ROOT, 'atr-lab-design/assets/fonts'),
    '/private/tmp/claude-501/-Users-marcodotio-Developer-atr-lab-design-skill/80375296-6f20-4da8-a711-62359143039a/scratchpad/fontlib',
]
FILES = {
    'sans': 'source-sans-3/SourceSans3-Regular.ttf', 'sans-bold': 'source-sans-3/SourceSans3-Bold.ttf', 'black': 'source-sans-3/SourceSans3-Black.ttf',
    'semibold': 'source-sans-3/SourceSans3-Semibold.ttf', 'slab': 'roboto-slab/RobotoSlab-Regular.ttf', 'slab-bold': 'roboto-slab/RobotoSlab-Bold.ttf',
    'slab-semi': 'roboto-slab/RobotoSlab-SemiBold.ttf', 'mono': 'source-code-pro/SourceCodePro-Regular.ttf',
    'arial': '/System/Library/Fonts/Supplemental/Arial.ttf', 'arial-bold': '/System/Library/Fonts/Supplemental/Arial Bold.ttf',
}
_cache = {}


def font_path(rel):
    if rel.startswith('/'):
        return rel
    for d in FONT_DIRS:
        for cand in (os.path.join(d, rel), os.path.join(d, os.path.basename(rel))):
            if os.path.exists(cand):
                return cand
    raise FileNotFoundError(f'font {rel} not found in {FONT_DIRS}')


def font(key):
    if key not in _cache:
        t = TTFont(font_path(FILES[key]))
        _cache[key] = (t, t['hmtx'].metrics, t.getBestCmap(), t['head'].unitsPerEm)
    return _cache[key]


def width_in(text, key, pt, tracking_pt=0.0):
    t, hm, cmap, upm = font(key)
    units = 0
    for ch in text:
        g = cmap.get(ord(ch))
        units += hm[g][0] if g else hm['.notdef'][0]
    return units / upm * pt / 72 + tracking_pt / 72 * max(0, len(text) - 1)


def key_for(face, bold):
    face = (face or 'Source Sans 3').lower()
    if 'black' in face: return 'black'
    if 'semibold' in face and 'source sans' in face: return 'semibold'
    if 'roboto slab semibold' in face: return 'slab-semi'
    if 'roboto slab' in face: return 'slab-bold' if bold else 'slab'
    if 'source code' in face: return 'mono'
    return 'sans-bold' if bold else 'sans'


def wrap_lines(text, key, pt, box_w, tracking=0.0):
    """Greedy word wrap; returns the number of lines."""
    lines = 0
    for para in text.split('\n'):
        words = para.split(' ')
        cur = ''
        n = 1
        for w in words:
            trial = (cur + ' ' + w).strip()
            if cur and width_in(trial, key, pt, tracking) > box_w:
                n += 1; cur = w
            else:
                cur = trial
        lines += n
    return lines


NS = {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main', 'p': 'http://schemas.openxmlformats.org/presentationml/2006/main'}
EMU = 914400


def check(pptx, min_slack=0.0, min_scale=0.7, quiet=False):
    z = zipfile.ZipFile(pptx)
    parts = sorted(n for n in z.namelist() if re.match(r'ppt/(slides|slideLayouts)/[^/]+\.xml$', n))
    bad = 0
    shrunk = 0
    for part in parts:
        root = ET.fromstring(z.read(part))
        for sp in root.iter(f'{{{NS["p"]}}}sp'):
            tx = sp.find('p:txBody', NS)
            xfrm = sp.find('.//a:xfrm', NS)
            if tx is None or xfrm is None:
                continue
            ext = xfrm.find('a:ext', NS)
            bw, bh = int(ext.get('cx')) / EMU, int(ext.get('cy')) / EMU
            body = tx.find('a:bodyPr', NS)
            ins = 0.0
            autofit = False
            if body is not None:
                ins = (int(body.get('lIns', 91440)) + int(body.get('rIns', 91440))) / EMU
                autofit = body.find('a:normAutofit', NS) is not None
            paras = tx.findall('a:p', NS)
            total_h = {'brand': 0.0, 'arial': 0.0}
            preview = ''
            for p in paras:
                runs = p.findall('a:r', NS)
                text = ''.join((r.find('a:t', NS).text or '') for r in runs if r.find('a:t', NS) is not None)
                if not text.strip():
                    continue
                rpr = runs[0].find('a:rPr', NS) if runs else None
                pt = int(rpr.get('sz', '1800')) / 100 if rpr is not None and rpr.get('sz') else 18
                bold = rpr is not None and rpr.get('b') == '1'
                latin = rpr.find('a:latin', NS) if rpr is not None else None
                face = latin.get('typeface') if latin is not None else 'Source Sans 3'
                spc = int(rpr.get('spc', '0')) / 100 if rpr is not None and rpr.get('spc') else 0.0
                ppr = p.find('a:pPr', NS)
                ls = None; after = 0.0; indent = 0.0
                if ppr is not None:
                    pts = ppr.find('a:lnSpc/a:spcPts', NS)
                    if pts is not None: ls = int(pts.get('val')) / 100
                    pct = ppr.find('a:lnSpc/a:spcPct', NS)
                    if pct is not None: ls = pt * 1.2 * int(pct.get('val')) / 100000
                    aft = ppr.find('a:spcAft/a:spcPts', NS)
                    if aft is not None: after = int(aft.get('val')) / 100
                    if ppr.get('marL'): indent = int(ppr.get('marL')) / EMU
                if ls is None: ls = pt * 1.2
                usable = max(0.1, bw - ins - indent)
                preview = preview or text[:48]
                for label, fkey in (('brand', key_for(face, bold)), ('arial', 'arial-bold' if bold or 'black' in face.lower() or 'semibold' in face.lower() else 'arial')):
                    n = wrap_lines(text, fkey, pt, usable, spc)
                    total_h[label] += (n * ls + after) / 72
            if not preview:
                continue
            flag = ''
            over = total_h['brand'] > bh + 1e-6
            over_arial = total_h['arial'] > bh + 1e-6
            if (over or over_arial) and autofit:
                # shrink needed: text height scales roughly with the type size (width and spacing both shrink)
                scale = min(bh / total_h['brand'] if over else 1.0, bh / total_h['arial'] if over_arial else 1.0)
                if scale < min_scale:
                    flag = f'shrinks to {scale * 100:.0f}% (< {min_scale * 100:.0f}% floor)'
                else:
                    shrunk += 1
                    if not quiet:
                        print(f'{part.split("/")[-1]:20s} {"autofit: shrinks to " + format(scale * 100, ".0f") + "%":28s} box {bw:.2f}x{bh:.2f} in, needs {total_h["brand"]:.2f} (Arial {total_h["arial"]:.2f}): "{preview}"')
            elif over: flag = 'OVERFLOW (brand font)'
            elif over_arial: flag = 'overflow in Arial fallback'
            elif bh - total_h['brand'] < min_slack: flag = 'tight'
            if flag:
                bad += 1
                print(f'{part.split("/")[-1]:20s} {flag:28s} box {bw:.2f}x{bh:.2f} in, needs {total_h["brand"]:.2f} (Arial {total_h["arial"]:.2f}): "{preview}"')
    print(f'{pptx.split("/")[-1]}: {bad} flagged text box(es), {shrunk} within the autofit floor')
    return bad


if __name__ == '__main__':
    a = sys.argv[1:]
    if a and a[0] == '--check':
        slack, scale, quiet = 0.0, 0.7, False
        files = []
        i = 1
        while i < len(a):
            if a[i] == '--min-slack': slack = float(a[i + 1]); i += 2
            elif a[i] == '--min-scale': scale = float(a[i + 1]); i += 2
            elif a[i] == '--quiet': quiet = True; i += 1
            else: files.append(a[i]); i += 1
        sys.exit(1 if sum(check(f, slack, scale, quiet) for f in files) else 0)
    text, key, pt = a[0], a[1], float(a[2])
    print(f'{width_in(text, key, pt):.2f} in ({key} {pt} pt); Arial: {width_in(text, "arial-bold" if "bold" in key or key=="black" else "arial", pt):.2f} in')
