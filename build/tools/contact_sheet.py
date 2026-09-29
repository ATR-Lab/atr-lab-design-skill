#!/usr/bin/env python3
"""Usage: contact_sheet.py out.png img1 img2 ... [--cols 3] [--width 1800] [--bg 808080]
Tiles images (alpha composited on --bg) with filename labels, for fast visual QA."""
import sys, math
from PIL import Image, ImageDraw
args=sys.argv[1:]; out=args.pop(0); cols=3; width=1800; bg=(128,128,128)
files=[]
i=0
while i<len(args):
    if args[i]=='--cols': cols=int(args[i+1]); i+=2
    elif args[i]=='--width': width=int(args[i+1]); i+=2
    elif args[i]=='--bg': h=args[i+1]; bg=tuple(int(h[j:j+2],16) for j in (0,2,4)); i+=2
    else: files.append(args[i]); i+=1
cell=width//cols; pad=8; lab=18
ims=[Image.open(f).convert('RGBA') for f in files]
rows=math.ceil(len(ims)/cols)
heights=[]
for r in range(rows):
    row=ims[r*cols:(r+1)*cols]
    heights.append(max(int(im.height*(cell-2*pad)/im.width) for im in row)+lab+2*pad)
sheet=Image.new('RGB',(width,sum(heights)),bg); d=ImageDraw.Draw(sheet); y=0
for r in range(rows):
    for c,(im,f) in enumerate(zip(ims[r*cols:(r+1)*cols],files[r*cols:(r+1)*cols])):
        w=cell-2*pad; h=int(im.height*w/im.width); t=im.resize((w,h))
        base=Image.new('RGBA',(w,h),bg+(255,)); base.alpha_composite(t)
        sheet.paste(base.convert('RGB'),(c*cell+pad,y+pad)); d.text((c*cell+pad,y+pad+h+2),f.split('/')[-1][:60],fill=(0,0,0))
    y+=heights[r]
sheet.save(out); print(out)
