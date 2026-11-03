"""Key the chroma-green sheets, split them into single figures, add a navy outline."""
import numpy as np
from PIL import Image, ImageFilter
from pathlib import Path
OUT=Path('out'); OUT.mkdir(exist_ok=True)
NAVY=(0,57,118,255)

def key(path):
    a=np.array(Image.open(path).convert('RGB')).astype(np.int32)
    r,g,b=a[...,0],a[...,1],a[...,2]
    spill=g-np.maximum(r,b)                      # >0 means greenish
    alpha=np.clip(255-(spill-40)*255//60,0,255)  # spill<=40 opaque, >=100 transparent
    alpha=np.where(spill<=40,255,alpha).astype(np.uint8)
    g2=np.where(spill>0,np.maximum(r,b),g)       # despill
    rgba=np.dstack([r,g2,b,alpha]).astype(np.uint8)
    im=Image.fromarray(rgba,'RGBA')
    # drop specks
    return im

def outlined(im,px):
    a=im.getchannel('A').point(lambda v:255 if v>60 else 0)
    ring=a.filter(ImageFilter.MaxFilter(px*2+1)).filter(ImageFilter.GaussianBlur(0.8))
    base=Image.new('RGBA',im.size,NAVY); base.putalpha(ring)
    return Image.alpha_composite(base,im)

def trim(im,pad):
    bbox=im.getchannel('A').point(lambda v:255 if v>20 else 0).getbbox()
    c=im.crop(bbox); W=max(c.size)+pad*2
    sq=Image.new('RGBA',(W,W),(0,0,0,0)); sq.paste(c,((W-c.width)//2,(W-c.height)//2),c); return sq

def split_cols(im,n):
    a=np.array(im.getchannel('A'))>20; cols=a.sum(0)>0
    segs=[];start=None
    for x,v in enumerate(cols):
        if v and start is None: start=x
        if not v and start is not None: segs.append([start,x]); start=None
    if start is not None: segs.append([start,len(cols)])
    while len(segs)>n:  # merge the smallest gap
        gaps=[segs[i+1][0]-segs[i][1] for i in range(len(segs)-1)]; i=int(np.argmin(gaps))
        segs[i]=[segs[i][0],segs[i+1][1]]; del segs[i+1]
    return [im.crop((s,0,e,im.height)) for s,e in segs]

for sheet,names,size in [('turnaround-a.png',['front','three-quarter','side','back'],768),
                         ('turnaround-b.png',['body-front','body-three-quarter','body-side','body-back'],768)]:
    for nm,part in zip(names,split_cols(key(sheet),4)):
        f=outlined(trim(part,24),5); f=f.resize((size,size),Image.LANCZOS); f.save(OUT/f'teo-{nm}.png',optimize=True)
ex=key('expressions-a.png'); W,H=ex.size
names=['happy','thinking','surprised','sorry','determined','laughing','confused','sleeping','excited']
for i,nm in enumerate(names):
    cell=ex.crop(((i%3)*W//3,(i//3)*H//3,(i%3+1)*W//3,(i//3+1)*H//3))
    from scipy import ndimage
    a=np.array(cell.getchannel('A'))>20; lab,n=ndimage.label(a)
    edge=set(np.unique(np.concatenate([lab[0],lab[-1],lab[:,0],lab[:,-1]])))-{0}
    sizes=ndimage.sum(a,lab,range(n+1)); small={l for l in edge if sizes[l]<0.02*a.size}
    arr=np.array(cell); arr[np.isin(lab,list(small)),3]=0; cell=Image.fromarray(arr,'RGBA')
    f=outlined(trim(cell,20),4).resize((512,512),Image.LANCZOS); f.save(OUT/f'teo-{nm}.png',optimize=True)
print(sorted(p.name for p in OUT.iterdir()))
