"""Split the Higgsfield rig-kit sheet (transparent PNG) into one trimmed PNG per part."""
import sys
from pathlib import Path
import numpy as np
from PIL import Image
from scipy import ndimage

NAMES = ["head", "ear-left", "ear-right", "hand-wave", "hand-rest"]   # sheet order: top row L-R, bottom row L-R


def split(sheet: Path, out: Path, pad: int = 8):
    im = Image.open(sheet).convert("RGBA")
    a = np.array(im.getchannel("A")) > 24
    lab, n = ndimage.label(ndimage.binary_closing(a, iterations=3))
    sizes = ndimage.sum(a, lab, range(1, n + 1))
    keep = [i + 1 for i in np.argsort(sizes)[::-1][:len(NAMES)]]
    boxes = []
    for l in keep:
        ys, xs = np.where(lab == l)
        boxes.append((l, xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
    rows = sorted(boxes, key=lambda b: b[2])
    top = sorted([b for b in boxes if b[2] < im.height * 0.4], key=lambda b: b[1])
    bottom = sorted([b for b in boxes if b[2] >= im.height * 0.4], key=lambda b: b[1])
    arr = np.array(im)
    out.mkdir(parents=True, exist_ok=True)
    for name, (l, x0, y0, x1, y1) in zip(NAMES, top + bottom):
        part = arr.copy()
        part[lab != l, 3] = 0                                # drop neighbours and specks
        crop = Image.fromarray(part).crop((max(0, x0 - pad), max(0, y0 - pad), x1 + pad, y1 + pad))
        crop.save(out / f"teo-{name}.png", optimize=True)
        print(name, crop.size, (x0, y0))


if __name__ == "__main__":
    split(Path(sys.argv[1]), Path(sys.argv[2]))
