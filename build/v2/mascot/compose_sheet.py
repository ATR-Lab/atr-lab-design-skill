"""Compose assets/mascot/teo-character-sheet.png from the keyed views and expressions in out/ (key_split.py)."""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
SKILL = Path(sys.argv[1] if len(sys.argv) > 1 else Path.home()/'Active/atr-lab-design-skill-v2/atr-lab-design')
S = SKILL/'assets'; O = Path(__file__).with_name('out')
F = lambda n, s: ImageFont.truetype(str(S/'fonts'/n), s)
NAVY, GOLD, SKY, INK, SLATE, LINE = '#003976', '#EFAB00', '#2C8ECD', '#1B2533', '#4A5868', '#D6DEE8'
W, H = 3200, 2120
im = Image.new('RGB', (W, H), 'white'); d = ImageDraw.Draw(im)
d.rectangle((0, 0, W, 300), fill=NAVY)
d.text((120, 58), 'Teo', font=F('roboto-slab/RobotoSlab-Bold.ttf', 140), fill='white')
d.text((128, 222), 'Character sheet · mascot of the Advanced Telerobotics Research Lab',
       font=F('source-sans-3/SourceSans3-Semibold.ttf', 44), fill=GOLD)
lock = Image.open(S/'logos/png/atr-horizontal-short-twotone-reverse-1000.png').convert('RGBA'); lw = 520
lock = lock.resize((lw, int(lock.height*lw/lock.width)), Image.LANCZOS); im.paste(lock, (W-lw-120, (300-lock.height)//2), lock)
def label(x, y, t): d.text((x, y), t, font=F('source-sans-3/SourceSans3-Semibold.ttf', 34), fill=SLATE, anchor='mm')
def head(x, y, t, sub):
    d.text((x, y), t, font=F('source-sans-3/SourceSans3-Bold.ttf', 54), fill=NAVY)
    d.text((x, y+68), sub, font=F('source-sans-3/SourceSans3-Regular.ttf', 34), fill=SLATE)
def row(names, labels, y, x0, x1, size):
    step = (x1-x0)/len(names)
    for i, (n, lb) in enumerate(zip(names, labels)):
        p = Image.open(O/f'teo-{n}.png').convert('RGBA').resize((size, size), Image.LANCZOS); cx = int(x0+step*(i+.5))
        im.paste(p, (cx-size//2, y), p); label(cx, y+size+30, lb)
views = ['front', 'three-quarter', 'side', 'back']; vl = ['Front', 'Three-quarter', 'Side', 'Back']
head(120, 350, 'Head form (default)', 'Floating head and gloved hands. Use for emoji, stickers, avatars, chat and small art.')
row(views, vl, 470, 80, 1600, 330)
head(1700, 350, 'Full body (full-figure scenes only)', 'Navy suit, white limbs. Event signs, K-12 material, illustrations.')
row(['body-'+v for v in views], vl, 470, 1640, 3140, 330)
d.line((1640, 360, 1640, 880), fill=LINE, width=3)
head(120, 960, 'Expressions', 'The screen face carries the emotion; the shell, ear pods and antenna never change.')
ex = ['happy', 'thinking', 'surprised', 'sorry', 'determined', 'laughing', 'confused', 'sleeping', 'excited']
row(ex, [e.capitalize() for e in ex], 1080, 80, 3140, 280)
head(120, 1500, 'Colors', 'Brand tokens only. Outline 5-8% of the head width, always navy.')
for i, (t, u, c) in enumerate([('Navy  #003976', 'Screen face, outline, suit', NAVY), ('White  #FFFFFF', 'Shell, gloves', 'white'),
                               ('Sky  #2C8ECD', 'Eyes, ear pods, cuffs', SKY), ('Gold  #EFAB00', 'Smile, antenna tip', GOLD)]):
    x = 120+i*380; d.rounded_rectangle((x, 1640, x+110, 1750), radius=18, fill=c, outline=NAVY, width=4)
    d.text((x, 1770), t, font=F('source-sans-3/SourceSans3-Bold.ttf', 32), fill=INK)
    d.text((x, 1812), u, font=F('source-sans-3/SourceSans3-Regular.ttf', 28), fill=SLATE)
d.text((1700, 1500), 'Rules', font=F('source-sans-3/SourceSans3-Bold.ttf', 54), fill=NAVY)
rules = [('Do', 'Keep proportions, colors and the navy outline exactly as shown.'),
         ('Do', 'Use Teo for the Discord bot, chat, K-12 and event fun.'),
         ('Do', 'Pair Teo with the ATR logo as a separate element.'),
         ("Don't", 'Put Teo inside, on or in place of the ATR mark, lockups or roundel.'),
         ("Don't", 'Use Teo on formal pieces: letterhead, certificates, press, grants.'),
         ("Don't", 'Show Teo as a real lab robot, or put text on its screen face.')]
for i, (k, t) in enumerate(rules):
    y = 1590+i*62
    d.text((1700, y), k, font=F('source-sans-3/SourceSans3-Bold.ttf', 32), fill=NAVY if k == 'Do' else '#B63B35')
    d.text((1820, y), t, font=F('source-sans-3/SourceSans3-Regular.ttf', 32), fill=INK)
d.text((120, H-44-70), 'Teo is an illustrated character, not a photo of a lab robot. Files and usage: assets/mascot/ and references/mascot.md',
       font=F('source-sans-3/SourceSans3-Regular.ttf', 30), fill=SLATE)
tile = Image.open(S/'patterns/hazard-tile-gold-navy-h96.png').convert('RGB'); bh = 44
t = tile.resize((int(tile.width*bh/tile.height), bh), Image.LANCZOS)
for x in range(0, W, t.width): im.paste(t, (x, H-bh))
im.save(Path(__file__).with_name('teo-character-sheet.png'), optimize=True)
