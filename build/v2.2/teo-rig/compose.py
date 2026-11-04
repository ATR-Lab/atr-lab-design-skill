"""Assemble the rig parts into Teo's rest pose (sheet pixels) and write a preview plus the layout numbers."""
import json, sys
from PIL import Image, ImageDraw

P = {k: Image.open(f"parts/teo-{k}.png").convert("RGBA") for k in ["head", "ear-left", "ear-right", "hand-wave", "hand-rest"]}
# where each part's top-left sits on a 1400x1400 canvas; head at (254, 520)
HX, HY = 254, 520
L = {
    "ear-left":  (HX + 10,  HY - 262, 14),   # x, y, rotation (deg, + = counter-clockwise)
    "ear-right": (HX + 531, HY - 262, -14),
    "head":      (HX, HY, 0),
    "hand-wave": (HX - 190, HY + 300, 12),
}
FACE = dict(cx=HX + 447, cy=HY + 318, eye_dx=118, eye_rx=34, eye_ry=40, eye_y=-28, mouth_y=58)
GOLD, ORANGE = (239, 171, 0, 255), (240, 120, 40, 255)


def face(im):
    d = ImageDraw.Draw(im)
    c, cy = FACE["cx"], FACE["cy"]
    for sx in (-1, 1):
        x = c + sx * FACE["eye_dx"]; y = cy + FACE["eye_y"]
        d.ellipse((x - FACE["eye_rx"], y - FACE["eye_ry"], x + FACE["eye_rx"], y + FACE["eye_ry"]), fill=GOLD)
        for k in range(3):
            bx = x - 30 + k * 22; by = y + 70
            d.line((bx, by + 10, bx + 10, by - 6), fill=ORANGE, width=7)
    my = cy + FACE["mouth_y"]
    d.line([(c - 52, my - 10), (c - 26, my + 14), (c, my - 6), (c + 26, my + 14), (c + 52, my - 10)], fill=GOLD, width=12, joint="curve")


def assemble(order=("ear-left", "ear-right", "head", "hand-wave")):
    can = Image.new("RGBA", (1400, 1400), (0, 57, 118, 255))
    for k in order:
        x, y, r = L[k]
        im = P[k].rotate(r, resample=Image.BICUBIC, expand=True) if r else P[k]
        can.alpha_composite(im, (x - (im.width - P[k].width) // 2, y - (im.height - P[k].height) // 2))
        if k == "head":
            face(can)
    return can


if __name__ == "__main__":
    assemble().resize((700, 700)).save(sys.argv[1] if len(sys.argv) > 1 else "/tmp/claude-501/v22/rig.png")
