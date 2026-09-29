"""Shared helpers for the ATR logo asset pipeline (deterministic processing only:
thresholding, alpha-from-luminance, cropping, exact recoloring, compositing, tracing)."""
import os
import numpy as np
from PIL import Image

REPO = "/Users/marcodotio/Developer/atr-lab-design-skill"
SCRATCH = "/private/tmp/claude-501/-Users-marcodotio-Developer-atr-lab-design-skill/80375296-6f20-4da8-a711-62359143039a/scratchpad"
MEDIA = f"{SCRATCH}/render/presx/ppt/media"
SRC = {
    "lockup": f"{REPO}/assets/ATR_Lab_logo-04-21-2021.png",
    "seal605": f"{REPO}/assets/atr-lab-logo-round-04-21-2021.png",
    "seal": f"{MEDIA}/image5.png",
    "mark": f"{MEDIA}/image6.png",
    "badge_gold": f"{MEDIA}/image2.png",
    "badge_white": f"{MEDIA}/image4.png",
    "ksu": f"{MEDIA}/image3.png",
    "stacked_art": f"{MEDIA}/image7.jpg",   # lab's own stacked artwork (gold on white, hazard frame)
}
OUT = f"{REPO}/atr-lab-design/assets/logos"
QA = f"{REPO}/build/qa/logos"
WORK = f"{REPO}/build/logos-src/work"

NAVY = (0x00, 0x39, 0x76)
GOLD = (0xEF, 0xAB, 0x00)
BLACK = (0x00, 0x00, 0x00)
WHITE = (0xFF, 0xFF, 0xFF)
MIST = (0xF3, 0xF6, 0xFA)


def hexc(c):
    return "#%02X%02X%02X" % c


def rgba(path):
    return np.array(Image.open(path).convert("RGBA")).astype(np.float64)


def lum(a):
    return 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]


def coverage_from_luminance(path, ink_lum=None):
    """Black line art (possibly with alpha): composite on white, then
    coverage = (255 - L) / (255 - L_ink). White (incl. white fill) -> 0."""
    a = rgba(path)
    al = a[..., 3] / 255.0
    L = al * lum(a) + (1 - al) * 255.0
    if ink_lum is None:
        ink_lum = float(np.percentile(L[al > 0.99], 1)) if (al > 0.99).any() else 0.0
    return np.clip((255.0 - L) / (255.0 - ink_lum), 0, 1)


def coverage_from_alpha(path):
    """Single flat colour art on transparency: coverage = alpha."""
    return rgba(path)[..., 3] / 255.0


def save_gray(arr01, path):
    Image.fromarray(np.clip(arr01 * 255 + 0.5, 0, 255).astype(np.uint8), "L").save(path)


def iou(a, b):
    a = a.astype(bool); b = b.astype(bool)
    return float((a & b).sum()) / float((a | b).sum())
