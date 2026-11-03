"""Turn the Higgsfield renders (transparent PNGs) into assets/mascot/ files for Teo v2."""
import sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageFilter, ImageDraw
from scipy import ndimage
G = Path(__file__).parent; M = Path(sys.argv[1])
NAVY = (0, 57, 118, 255)

def clean(im, min_frac=0.004, edge_frac=0.02):
    """Drop tiny specks and small fragments touching the edge (neighbour bleed)."""
    a = np.array(im.getchannel('A')) > 24; lab, n = ndimage.label(a)
    sizes = ndimage.sum(a, lab, range(n + 1)); arr = np.array(im)
    edge = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    for l in range(1, n + 1):
        if sizes[l] < min_frac * a.sum() * 0.05 or (l in edge and sizes[l] < edge_frac * a.size):
            arr[lab == l, 3] = 0
    return Image.fromarray(arr, 'RGBA')

def trim_square(im, pad_frac=0.06, size=512):
    bb = im.getchannel('A').point(lambda v: 255 if v > 24 else 0).getbbox(); c = im.crop(bb)
    W = int(max(c.size) * (1 + 2 * pad_frac)); sq = Image.new('RGBA', (W, W), (0, 0, 0, 0))
    sq.paste(c, ((W - c.width) // 2, (W - c.height) // 2), c)
    return sq.resize((size, size), Image.LANCZOS)

def split_cols(im, n):
    a = np.array(im.getchannel('A')) > 24; cols = a.sum(0) > 0; segs = []; s = None
    for x, v in enumerate(cols):
        if v and s is None: s = x
        if not v and s is not None: segs.append([s, x]); s = None
    if s is not None: segs.append([s, len(cols)])
    while len(segs) > n:
        gaps = [segs[i + 1][0] - segs[i][1] for i in range(len(segs) - 1)]; i = int(np.argmin(gaps))
        segs[i] = [segs[i][0], segs[i + 1][1]]; del segs[i + 1]
    return [im.crop((a_, 0, b_, im.height)) for a_, b_ in segs]

def die_cut(im, size=320, border=14, outline=5):
    src = trim_square(im, 0.07, 640); a = src.getchannel('A').point(lambda v: 255 if v > 40 else 0)
    a = Image.fromarray(ndimage.binary_fill_holes(np.array(a) > 0).astype('uint8') * 255)
    white = a.filter(ImageFilter.MaxFilter(border * 2 + 1)).filter(ImageFilter.GaussianBlur(1.2))
    navy = white.filter(ImageFilter.MaxFilter(outline * 2 + 1)).filter(ImageFilter.GaussianBlur(1))
    out = Image.new('RGBA', src.size, (0, 0, 0, 0))
    l = Image.new('RGBA', src.size, NAVY); l.putalpha(navy); out = Image.alpha_composite(out, l)
    w = Image.new('RGBA', src.size, (255, 255, 255, 255)); w.putalpha(white); out = Image.alpha_composite(out, w)
    out = Image.alpha_composite(out, src)
    return trim_square(out, 0.02, size)

for sheet, names in [('gen1/turn-0.png', ['front', 'three-quarter', 'side', 'back']),
                     ('gen1/turn-2.png', ['body-front', 'body-three-quarter', 'body-side', 'body-back'])]:
    for nm, part in zip(names, split_cols(clean(Image.open(G / sheet).convert('RGBA')), 4)):
        trim_square(part).save(M / 'views' / f'teo-{nm}.png', optimize=True)
ex = Image.open(G / 'gen2/expressions.png').convert('RGBA'); W, H = ex.size
for i, nm in enumerate(['happy', 'thinking', 'surprised', 'sorry', 'determined', 'laughing', 'confused', 'sleeping', 'excited']):
    cell = clean(ex.crop(((i % 3) * W // 3, (i // 3) * H // 3, (i % 3 + 1) * W // 3, (i // 3 + 1) * H // 3)))
    trim_square(cell).save(M / 'expressions' / f'teo-{nm}.png', optimize=True)
for e in ['wave', 'think', 'thumbsup', 'party', 'love', 'sweat', 'estop', 'sleep']:
    trim_square(clean(Image.open(G / f'gen2/teo_{e}.png').convert('RGBA')), 0.03, 256).save(M / 'emoji' / f'teo_{e}.png', optimize=True)
for src, dst in [('wave', 'teo-hello'), ('think', 'teo-hmm'), ('thumbsup', 'teo-nice'), ('party', 'teo-party'), ('estop', 'teo-e-stop')]:
    die_cut(clean(Image.open(G / f'gen2/teo_{src}.png').convert('RGBA'))).save(M / 'stickers' / f'{dst}.png', optimize=True)
# avatar: the head-only happy expression on navy, about 76% of the square (reads at 40 px in a circle)
ex0 = Image.open(G / "gen2/expressions.png").convert("RGBA"); head = trim_square(clean(ex0.crop((0, 0, ex0.width // 3, ex0.height // 3))), 0.0, 780)
av = Image.new('RGBA', (1024, 1024), NAVY); av.alpha_composite(head, ((1024 - 780) // 2, (1024 - 780) // 2 + 20))
av.convert('RGB').save(M / 'teo-avatar.png', optimize=True)
# generation references, 1024 px
ref = M / 'references'
for p in ref.glob('*.png'): p.unlink()
for src, dst in [('refs/lead-ref-hero.png', 'lead-ref-hero.png'), ('refs/lead-ref-stickers.png', 'lead-ref-stickers.png'),
                 ('gen1/turn-0.png', 'ref-turnaround-head.png'), ('gen1/turn-2.png', 'ref-turnaround-body.png'), ('gen2/expressions.png', 'ref-expressions.png')]:
    i = Image.open(G / src); i.thumbnail((1024, 1024)); i.save(ref / dst, optimize=True)
print('done')
