#!/usr/bin/env python3
"""Post-process the ATR social templates written by build.js (pptxgenjs 4.0.1).

1. Replace ppt/theme/theme1.xml with the ATR Office theme (assets/tokens/office-theme/theme1.xml), verbatim.
2. Decorative pictures (the generator tags them altText="decorative"): set descr="" AND add the Office
   "decorative" extension inside <p:cNvPr>, which is what PowerPoint's Accessibility Checker reads (an empty
   descr alone is reported as "missing alternative text"). Slides and slide layouts.
3. Give every layout placeholder a real <a:lstStyle> built from its prompt run, so a new slide made from the
   layout in PowerPoint or Google Slides inherits the font, size, weight, colour, tracking, alignment and
   line spacing (pptxgenjs writes the prompt text with explicit run properties but an empty lstStyle, and
   inheritance only flows through lstStyle). Placeholders also get the conventional <a:spLocks noGrp="1"/>.
4. Restore type="pic" on picture placeholders (pptxgenjs drops it) on layouts and on filled slide pictures.
5. Make sure every text placeholder's <a:bodyPr> carries <a:normAutofit/> ("Shrink text on overflow"), on
   layouts and on slides; build.js asks for it (fit: 'shrink') and this is the safety net. Also copy the
   insets (0) and the anchor from each showcase slide placeholder onto the layout placeholder with the same
   idx, because pptxgenjs drops margin and valign on layout placeholders (see sync_layout_bodypr).
6. Strip hasCustomPrompt="1" from slide-level placeholders (it belongs on the layout only).
7. Remove pptxgenjs's empty "DEFAULT" white layout (part, rels, master reference, content-type override) so
   Home > New Slide offers only the eight branded layouts.
8. De-duplicate media: pptxgenjs embeds the same logo PNG once per layout; keep one copy per content hash and
   point every relationship at it (about 0.6 MB saved per file).
9. Drop content-type overrides for parts that do not exist (pptxgenjs writes phantom slideMasterN entries).

Usage: postprocess.py deck1.pptx [deck2.pptx ...]
"""
import copy, hashlib, os, posixpath, re, shutil, sys, zipfile
from lxml import etree

ROOT = '/Users/marcodotio/Developer/atr-lab-design-skill'
THEME = os.path.join(ROOT, 'atr-lab-design/assets/tokens/office-theme/theme1.xml')
NS = {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
      'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
      'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
      'rel': 'http://schemas.openxmlformats.org/package/2006/relationships',
      'ct': 'http://schemas.openxmlformats.org/package/2006/content-types'}
A = '{%s}' % NS['a']
P = '{%s}' % NS['p']
R = '{%s}' % NS['r']
REL = '{%s}' % NS['rel']
CT = '{%s}' % NS['ct']
ADEC_NS = 'http://schemas.microsoft.com/office/drawing/2017/decorative'
DECOR_URI = '{C183D7F6-B498-43B3-948B-1728B52AA6E4}'

# schema child order inside a:lvl1pPr (CT_TextParagraphProperties) and a:defRPr (CT_TextCharacterProperties)
PPR_ORDER = ['lnSpc', 'spcBef', 'spcAft', 'buClrTx', 'buClr', 'buSzTx', 'buSzPct', 'buSzPts', 'buFontTx', 'buFont',
             'buNone', 'buAutoNum', 'buChar', 'buBlip', 'tabLst', 'defRPr', 'extLst']
RPR_ORDER = ['ln', 'noFill', 'solidFill', 'gradFill', 'blipFill', 'pattFill', 'grpFill', 'effectLst', 'effectDag',
             'highlight', 'uLnTx', 'uLn', 'uFillTx', 'uFill', 'latin', 'ea', 'cs', 'sym', 'hlinkClick',
             'hlinkMouseOver', 'rtl', 'extLst']
RPR_DROP_ATTRS = {'lang', 'dirty', 'err', 'smtClean', 'altLang'}
AUTOFIT_TAGS = {A + 'noAutofit', A + 'normAutofit', A + 'spAutoFit'}


def rank(order):
    return lambda el: order.index(etree.QName(el).localname) if etree.QName(el).localname in order else 99


def tostring(root):
    return etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True)


def build_lststyle(txbody):
    """Return a new a:lstStyle element derived from the first paragraph of txbody, or None."""
    p = txbody.find(A + 'p')
    if p is None:
        return None
    ppr = p.find(A + 'pPr')
    r = p.find(A + 'r')
    rpr = r.find(A + 'rPr') if r is not None else None
    lst = etree.Element(A + 'lstStyle')
    lvl = etree.SubElement(lst, A + 'lvl1pPr')
    if ppr is not None:
        for k, v in ppr.attrib.items():
            if k != 'lvl':
                lvl.set(k, v)
        for child in ppr:
            lvl.append(copy.deepcopy(child))
    d = etree.SubElement(lvl, A + 'defRPr')
    if rpr is not None:
        for k, v in rpr.attrib.items():
            if k not in RPR_DROP_ATTRS:
                d.set(k, v)
        for child in rpr:
            d.append(copy.deepcopy(child))
    # sort children into schema order (defRPr must come after the bullet elements)
    lvl[:] = sorted(list(lvl), key=rank(PPR_ORDER))
    d[:] = sorted(list(d), key=rank(RPR_ORDER))
    return lst


def fix_pic_types(root):
    """pptxgenjs 4.0.1 drops type="pic" (it indexes its type map twice), so picture placeholders come out as
    untyped object placeholders. Restore the type on layout shapes named "Picture Placeholder ..." and on
    every slide picture that sits in a placeholder."""
    n = 0
    for sp in list(root.iter(P + 'sp')) + list(root.iter(P + 'pic')):
        tag = 'nvSpPr' if sp.tag == P + 'sp' else 'nvPicPr'
        nv = sp.find(P + tag)
        if nv is None:
            continue
        ph = nv.find(P + 'nvPr/' + P + 'ph')
        cnvpr = nv.find(P + 'cNvPr')
        if ph is None or ph.get('type'):
            continue
        if sp.tag == P + 'pic' or (cnvpr is not None and (cnvpr.get('name') or '').startswith('Picture Placeholder')):
            ph.set('type', 'pic')
            n += 1
    return n


def mark_decorative(root):
    """descr="decorative" -> descr="" plus the Office decorative extension in cNvPr."""
    n = 0
    for cnvpr in root.iter(P + 'cNvPr'):
        if cnvpr.get('descr') != 'decorative':
            continue
        cnvpr.set('descr', '')
        extlst = cnvpr.find(A + 'extLst')
        if extlst is None:
            extlst = etree.SubElement(cnvpr, A + 'extLst')
        ext = etree.SubElement(extlst, A + 'ext')
        ext.set('uri', DECOR_URI)
        dec = etree.SubElement(ext, '{%s}decorative' % ADEC_NS, nsmap={'adec': ADEC_NS})
        dec.set('val', '1')
        n += 1
    return n


def ensure_autofit(root):
    """Every text placeholder body gets <a:normAutofit/> unless an autofit choice is already present."""
    n = 0
    for sp in root.iter(P + 'sp'):
        nvpr = sp.find(P + 'nvSpPr/' + P + 'nvPr')
        ph = nvpr.find(P + 'ph') if nvpr is not None else None
        if ph is None or ph.get('type') == 'pic':
            continue
        bodypr = sp.find(P + 'txBody/' + A + 'bodyPr')
        if bodypr is None:
            continue
        if any(c.tag in AUTOFIT_TAGS for c in bodypr):
            continue
        # schema order: prstTxWarp?, (autofit choice)?, scene3d?, ... -> insert after prstTxWarp if present
        idx = 0
        for i, c in enumerate(bodypr):
            if c.tag == A + 'prstTxWarp':
                idx = i + 1
        bodypr.insert(idx, etree.Element(A + 'normAutofit'))
        n += 1
    return n


def fix_slide(data):
    root = etree.fromstring(data)
    n_pic = fix_pic_types(root)
    n_dec = mark_decorative(root)
    n_fit = ensure_autofit(root)
    n_prompt = 0
    for ph in root.iter(P + 'ph'):
        if 'hasCustomPrompt' in ph.attrib:
            del ph.attrib['hasCustomPrompt']
            n_prompt += 1
    return tostring(root), dict(pic=n_pic, dec=n_dec, fit=n_fit, prompt=n_prompt)


def fix_layout(data):
    root = etree.fromstring(data)
    n_ph = 0
    fix_pic_types(root)
    n_dec = mark_decorative(root)
    for sp in root.iter(P + 'sp'):
        nvpr = sp.find(P + 'nvSpPr/' + P + 'nvPr')
        ph = nvpr.find(P + 'ph') if nvpr is not None else None
        if ph is None:
            continue
        cnv = sp.find(P + 'nvSpPr/' + P + 'cNvSpPr')
        if cnv is not None:
            cnv.attrib.pop('txBox', None)
            if cnv.find(A + 'spLocks') is None:
                etree.SubElement(cnv, A + 'spLocks').set('noGrp', '1')
        if ph.get('type') == 'pic':
            continue
        txbody = sp.find(P + 'txBody')
        if txbody is None:
            continue
        new = build_lststyle(txbody)
        if new is None:
            continue
        old = txbody.find(A + 'lstStyle')
        if old is not None:
            txbody.replace(old, new)
        else:
            bodypr = txbody.find(A + 'bodyPr')
            txbody.insert(list(txbody).index(bodypr) + 1 if bodypr is not None else 0, new)
        n_ph += 1
    n_fit = ensure_autofit(root)
    return tostring(root), dict(ph=n_ph, dec=n_dec, fit=n_fit)


def layout_name(data):
    root = etree.fromstring(data)
    csld = root.find(P + 'cSld')
    return csld.get('name') if csld is not None else None


def rels_targets(data):
    root = etree.fromstring(data)
    return [(r.get('Id'), r.get('Target')) for r in root.iter(REL + 'Relationship')]


def remove_default_layout(parts):
    """Delete the 'DEFAULT' layout part and every reference to it. Refuses if a slide uses it."""
    victims = [n for n in parts if re.fullmatch(r'ppt/slideLayouts/slideLayout\d+\.xml', n) and layout_name(parts[n]) == 'DEFAULT']
    removed = 0
    for lay in victims:
        base = posixpath.basename(lay)
        for n in parts:
            if re.fullmatch(r'ppt/slides/_rels/slide\d+\.xml\.rels', n) and any(t.endswith('/' + base) for _, t in rels_targets(parts[n])):
                raise SystemExit(f'{lay} is used by {n}; not removing')
        for n in [k for k in parts if re.fullmatch(r'ppt/slideMasters/_rels/slideMaster\d+\.xml\.rels', k)]:
            root = etree.fromstring(parts[n])
            rid = None
            for r in list(root.iter(REL + 'Relationship')):
                if r.get('Target').endswith('/' + base):
                    rid = r.get('Id'); root.remove(r)
            parts[n] = tostring(root)
            if rid:
                mn = n.replace('/_rels/', '/').replace('.rels', '')
                mroot = etree.fromstring(parts[mn])
                for sid in list(mroot.iter(P + 'sldLayoutId')):
                    if sid.get(R + 'id') == rid:
                        sid.getparent().remove(sid)
                parts[mn] = tostring(mroot)
        parts.pop(lay, None)
        parts.pop('ppt/slideLayouts/_rels/' + base + '.rels', None)
        removed += 1
    return removed


def dedupe_media(parts):
    """Keep one copy per content hash under ppt/media and rewrite every .rels target."""
    by_hash, alias = {}, {}
    for n in sorted(k for k in parts if k.startswith('ppt/media/')):
        h = hashlib.sha1(parts[n]).hexdigest()
        if h in by_hash:
            alias[n] = by_hash[h]
        else:
            by_hash[h] = n
    if not alias:
        return 0
    for n in [k for k in parts if k.endswith('.rels')]:
        root = etree.fromstring(parts[n])
        changed = False
        for r in root.iter(REL + 'Relationship'):
            t = r.get('Target') or ''
            if r.get('TargetMode') == 'External' or 'media/' not in t:
                continue
            abs_t = posixpath.normpath(posixpath.join(posixpath.dirname(n).replace('/_rels', ''), t))
            if abs_t in alias:
                r.set('Target', posixpath.relpath(alias[abs_t], posixpath.dirname(n).replace('/_rels', '')))
                changed = True
        if changed:
            parts[n] = tostring(root)
    for n in alias:
        del parts[n]
    return len(alias)


BODYPR_SYNC = ('lIns', 'tIns', 'rIns', 'bIns', 'anchor', 'wrap')


def sync_layout_bodypr(parts):
    """pptxgenjs drops margin (insets) and valign (anchor) on layout placeholders but keeps them on the showcase
    slide made from that layout. Without this a fresh slide inherits PowerPoint's default insets (0.1 in sides,
    0.05 in top and bottom), sits 10 px off the mark's left edge and, worse, its one-line boxes are 10 px too
    short for their exact line pitch, which makes shrink-on-overflow collapse the text. Copy each slide
    placeholder's bodyPr attributes onto the layout placeholder with the same idx."""
    n = 0
    for sname in [k for k in parts if re.fullmatch(r'ppt/slides/slide\d+\.xml', k)]:
        rels = parts.get('ppt/slides/_rels/' + posixpath.basename(sname) + '.rels')
        if rels is None:
            continue
        lay = None
        for _, t in rels_targets(rels):
            if 'slideLayouts/' in t:
                lay = posixpath.normpath(posixpath.join('ppt/slides', t))
        if lay is None or lay not in parts:
            continue
        sroot = etree.fromstring(parts[sname])
        attrs = {}
        for sp in sroot.iter(P + 'sp'):
            ph = sp.find(P + 'nvSpPr/' + P + 'nvPr/' + P + 'ph')
            bodypr = sp.find(P + 'txBody/' + A + 'bodyPr')
            if ph is not None and bodypr is not None and ph.get('idx'):
                attrs[ph.get('idx')] = {k: v for k, v in bodypr.attrib.items() if k in BODYPR_SYNC}
        lroot = etree.fromstring(parts[lay])
        for sp in lroot.iter(P + 'sp'):
            ph = sp.find(P + 'nvSpPr/' + P + 'nvPr/' + P + 'ph')
            bodypr = sp.find(P + 'txBody/' + A + 'bodyPr')
            if ph is None or bodypr is None or ph.get('idx') not in attrs:
                continue
            for k, v in attrs[ph.get('idx')].items():
                bodypr.set(k, v)
            n += 1
        parts[lay] = tostring(lroot)
    return n


def prune_content_types(parts):
    ct = etree.fromstring(parts['[Content_Types].xml'])
    n = 0
    for ov in list(ct.iter(CT + 'Override')):
        if ov.get('PartName').lstrip('/') not in parts:
            ct.remove(ov); n += 1
    parts['[Content_Types].xml'] = tostring(ct)
    return n


def process(src):
    theme = open(THEME, 'rb').read()
    with zipfile.ZipFile(src) as zin:
        infos = zin.infolist()
        parts = {i.filename: zin.read(i.filename) for i in infos}
    stats = dict(theme=0, dec=0, ph=0, pic=0, fit=0, prompt=0)
    for name in list(parts):
        if re.fullmatch(r'ppt/theme/theme\d+\.xml', name):
            parts[name] = theme; stats['theme'] += 1
        elif re.fullmatch(r'ppt/slideLayouts/slideLayout\d+\.xml', name):
            parts[name], k = fix_layout(parts[name])
            stats['ph'] += k['ph']; stats['dec'] += k['dec']; stats['fit'] += k['fit']
        elif re.fullmatch(r'ppt/slides/slide\d+\.xml', name):
            parts[name], k = fix_slide(parts[name])
            stats['pic'] += k['pic']; stats['dec'] += k['dec']; stats['fit'] += k['fit']; stats['prompt'] += k['prompt']
    n_sync = sync_layout_bodypr(parts)
    n_default = remove_default_layout(parts)
    n_media = dedupe_media(parts)
    n_ct = prune_content_types(parts)
    tmp = src + '.tmp'
    with zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as zout:
        for i in infos:                       # keep the original order; [Content_Types].xml stays first
            if i.filename in parts:
                zout.writestr(i, parts[i.filename])
    shutil.move(tmp, src)
    size = os.path.getsize(src) / 1e6
    print(f'postprocess: {os.path.basename(src)}: theme x{stats["theme"]}, decorative x{stats["dec"]}, layout placeholders styled '
          f'x{stats["ph"]}, slide pictures typed pic x{stats["pic"]}, autofit added x{stats["fit"]}, prompts stripped x{stats["prompt"]}, '
          f'layout bodyPr synced x{n_sync}, DEFAULT layout removed x{n_default}, media duplicates removed x{n_media}, phantom overrides x{n_ct}, {size:.2f} MB')


if __name__ == '__main__':
    for f in sys.argv[1:]:
        process(f)
