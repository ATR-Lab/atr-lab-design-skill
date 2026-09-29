#!/usr/bin/env python3
"""Post-process a pptxgenjs deck (or a docx-js document) for the ATR Lab collateral set.

1. Replace ppt/theme/theme*.xml (or word/theme/theme1.xml) with the ATR Office theme
   (assets/tokens/office-theme/theme1.xml), verbatim.
2. Blank the alt text of pictures tagged "decorative": pptxgenjs falls back to the file path when
   altText is empty, so the generators tag decoration altText="decorative" and this step writes descr="".
   Applied to slides, slide layouts and slide masters (the bands and fields live on the layouts).
3. Make layout placeholders inherit properly. pptxgenjs writes a default <a:bodyPr> (0.1 in insets, no
   anchor, no autofit) and an empty <a:lstStyle/> for placeholders on slide layouts, while the slide copies
   carry the full properties. For every layout placeholder this step (a) copies the <a:bodyPr> of the same
   placeholder (same idx) from the first slide that uses the layout, and (b) builds <a:lstStyle><a:lvl1pPr>
   from the prompt paragraph's <a:pPr> and first <a:rPr>, so a box inserted with New Slide gets the same
   margins, anchor, shrink-on-overflow, font, size, colour, tracking and line spacing as the shipped slides.

4. Drop the empty "DEFAULT" layout that pptxgenjs always writes (no slide uses it; it only clutters the
   layout gallery students pick from): the part, its rels, the master's sldLayoutId and rel, and the
   content-type override.

Usage: postprocess.py file.pptx [file2.pptx ...]
"""
import re, shutil, sys, zipfile, os

ROOT = '/Users/marcodotio/Developer/atr-lab-design-skill'
THEME = os.path.join(ROOT, 'atr-lab-design/assets/tokens/office-theme/theme1.xml')
theme = open(THEME, 'rb').read()

PART_RE = re.compile(r'ppt/(slides|slideLayouts|slideMasters)/[^/]+\.xml$')
SP_RE = re.compile(rb'<p:sp>.*?</p:sp>', re.S)
PH_IDX_RE = re.compile(rb'<p:ph\b[^>]*?idx="(\d+)"', re.S)
BODYPR_RE = re.compile(rb'<a:bodyPr\b[^>]*?(?:/>|>.*?</a:bodyPr>)', re.S)
PPR_RE = re.compile(rb'<a:pPr\b([^>]*?)(?:/>|>(.*?)</a:pPr>)', re.S)
RPR_RE = re.compile(rb'<a:rPr\b([^>]*?)(?:/>|>(.*?)</a:rPr>)', re.S)
LST_RE = re.compile(rb'<a:lstStyle\s*/>')


def slide_layout_map(parts):
    """slideN.xml -> slideLayoutM.xml from the slide rels."""
    m = {}
    for name, data in parts.items():
        mm = re.fullmatch(r'ppt/slides/_rels/(slide\d+)\.xml\.rels', name)
        if mm:
            t = re.search(rb'Target="\.\./slideLayouts/(slideLayout\d+\.xml)"', data)
            if t:
                m[f'ppt/slides/{mm.group(1)}.xml'] = 'ppt/slideLayouts/' + t.group(1).decode()
    return m


def placeholder_bodyprs(slide_xml):
    out = {}
    for sp in SP_RE.findall(slide_xml):
        idx = PH_IDX_RE.search(sp)
        body = BODYPR_RE.search(sp)
        if idx and body and idx.group(1) not in out:
            out[idx.group(1)] = body.group(0)
    return out


def fix_layout(layout_xml, bodyprs):
    n = 0

    def fix_sp(m):
        nonlocal n
        sp = m.group(0)
        idx = PH_IDX_RE.search(sp)
        if not idx:
            return sp
        # (a) bodyPr from the slide copy
        if idx.group(1) in bodyprs:
            sp = BODYPR_RE.sub(lambda _: bodyprs[idx.group(1)], sp, count=1)
        # (b) lstStyle from the prompt paragraph
        ppr, rpr = PPR_RE.search(sp), RPR_RE.search(sp)
        if LST_RE.search(sp) and rpr:
            pattrs = ppr.group(1) if ppr else b''
            pkids = (ppr.group(2) or b'') if ppr else b''
            rattrs = re.sub(rb'\s+(lang|dirty)="[^"]*"', b'', rpr.group(1))
            rkids = rpr.group(2) or b''
            lst = (b'<a:lstStyle><a:lvl1pPr' + pattrs + b'>' + pkids + b'<a:defRPr' + rattrs + b'>' + rkids + b'</a:defRPr></a:lvl1pPr></a:lstStyle>')
            sp = LST_RE.sub(lambda _: lst, sp, count=1)
        n += 1
        return sp

    return SP_RE.sub(fix_sp, layout_xml), n


def drop_default_layout(parts):
    """Remove the unused pptxgenjs DEFAULT layout. Returns the number of parts removed (0 if a slide uses it)."""
    lay = next((n for n in parts if re.fullmatch(r'ppt/slideLayouts/slideLayout\d+\.xml', n)
                and re.search(rb'<p:cSld\b[^>]*\bname="DEFAULT"', parts[n])), None)
    if not lay:
        return 0
    base = lay.split('/')[-1]
    for n, data in parts.items():
        if re.fullmatch(r'ppt/slides/_rels/slide\d+\.xml\.rels', n) and b'slideLayouts/' + base.encode() in data:
            return 0
    removed = 0
    for mrels in [n for n in parts if re.fullmatch(r'ppt/slideMasters/_rels/slideMaster\d+\.xml\.rels', n)]:
        master = mrels.replace('_rels/', '').replace('.rels', '')
        rel = re.search(rb'<Relationship\b[^>]*?Target="\.\./slideLayouts/' + re.escape(base.encode()) + rb'"[^>]*?/>', parts[mrels])
        if not rel:
            continue
        rid = re.search(rb'\bId="([^"]+)"', rel.group(0)).group(1)
        parts[mrels] = parts[mrels].replace(rel.group(0), b'')
        parts[master], k = re.subn(rb'<p:sldLayoutId\b[^>]*\br:id="' + re.escape(rid) + rb'"[^>]*/>', b'', parts[master])
        if k != 1:
            raise SystemExit(f'postprocess: expected one sldLayoutId for {base} in {master}, found {k}')
    for n in (lay, lay.replace('slideLayouts/', 'slideLayouts/_rels/') + '.rels'):
        if n in parts:
            del parts[n]; removed += 1
    ct = '[Content_Types].xml'
    parts[ct] = re.sub(rb'<Override\b[^>]*PartName="/' + re.escape(lay.encode()) + rb'"[^>]*/>', b'', parts[ct])
    return removed


def process(src):
    tmp = src + '.tmp'
    n_theme = n_decor = n_ph = 0
    with zipfile.ZipFile(src) as zin:
        infos = zin.infolist()
        parts = {i.filename: zin.read(i.filename) for i in infos}
    for name in list(parts):
        if re.fullmatch(r'(ppt|word)/theme/theme\d+\.xml', name):
            parts[name] = theme; n_theme += 1
        elif PART_RE.fullmatch(name):
            parts[name], k = re.subn(rb'descr="decorative"', b'descr=""', parts[name]); n_decor += k
    # step 3: layout placeholders inherit from their slides
    layout_of = slide_layout_map(parts)
    done = set()
    for slide, layout in sorted(layout_of.items(), key=lambda kv: int(re.search(r'\d+', kv[0].split('/')[-1]).group())):
        if layout in done or layout not in parts:
            continue
        parts[layout], k = fix_layout(parts[layout], placeholder_bodyprs(parts[slide]))
        n_ph += k
        done.add(layout)
    # step 4: no empty DEFAULT layout in the gallery (pptx only)
    n_drop = drop_default_layout(parts) if src.endswith('.pptx') else 0
    with zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as zout:
        for item in infos:
            if item.filename in parts:
                zout.writestr(item, parts[item.filename])
    shutil.move(tmp, src)
    print(f'postprocess: {os.path.basename(src)}: replaced {n_theme} theme part(s), blanked {n_decor} decorative alt text(s), fixed {n_ph} layout placeholder(s), dropped {n_drop} DEFAULT layout part(s)')


for f in sys.argv[1:]:
    process(f)
