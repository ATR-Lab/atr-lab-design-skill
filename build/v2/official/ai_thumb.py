import re, sys
from PIL import Image
def thumb(path):
    t = open(path, 'rb').read().decode('latin1').replace('\r', '\n')
    m = re.search(r'%AI7_Thumbnail: (\d+) (\d+) (\d+)\n%%BeginData: \d+ Hex Bytes\n(.*?)%%EndData', t, re.S)
    w, h = int(m.group(1)), int(m.group(2))
    hx = re.sub(r'[%\s]', '', m.group(4))
    b = bytes.fromhex(hx)
    i = b.find(b'RLE')
    pal = b[:i]; data = b[i+3:]
    out = bytearray(); k = 0
    while k < len(data):
        c = data[k]
        if c == 0xFD:
            n = data[k+1]; v = data[k+2]; out += bytes([v])*n; k += 3
        else:
            out.append(c); k += 1
    out = bytes(out[:w*h]).ljust(w*h, b'\xff')
    p = list(pal) + [0]*(768-len(pal))
    im = Image.frombytes('P', (w, h), out); im.putpalette(p[:768])
    return im.convert('RGB')
fs = sys.argv[2:]
ims = [thumb(f).resize((384, 120 if 'Horiz' in f else 368), Image.NEAREST) for f in fs]
H = sum(i.height + 10 for i in ims)
sheet = Image.new('RGB', (384, H), (200, 200, 200)); y = 0
for i in ims:
    sheet.paste(i, (0, y)); y += i.height + 10
sheet.save(sys.argv[1])
