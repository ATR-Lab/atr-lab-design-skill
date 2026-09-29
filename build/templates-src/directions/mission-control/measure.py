#!/usr/bin/env python3
"""Fit check: wrap each planned text block with the real brand TTF metrics and report lines/width.
Usage: venv python measure.py   (edit BLOCKS below)"""
from PIL import ImageFont
FL = "/private/tmp/claude-501/-Users-marcodotio-Developer-atr-lab-design-skill/80375296-6f20-4da8-a711-62359143039a/scratchpad/fontlib/"
FONTS = {"bold": "SourceSans3-Bold.ttf", "semi": "SourceSans3-Semibold.ttf", "reg": "SourceSans3-Regular.ttf",
         "slab": "RobotoSlab-Regular.ttf", "mono": "SourceCodePro-Regular.ttf"}

def width_in(text, font, pt, tracking_pt=0.0):
    f = ImageFont.truetype(FL + FONTS[font], int(pt * 10))  # 10x for precision
    return (f.getlength(text) / 10 + tracking_pt * len(text)) / 72

def wrap(text, font, pt, box_w, tracking=0.0):
    words, lines, cur = text.split(" "), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if width_in(t, font, pt, tracking) <= box_w or not cur:
            cur = t
        else:
            lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

# (label, text, font, pt, box width in, tracking pt)
BLOCKS = [
    ("S1 title l1", "Immersive Teleoperation", "bold", 44, 5.6, 0),
    ("S1 title l2", "for Physical AI", "bold", 44, 5.6, 0),
    ("S1 subtitle", "[Subtitle: session, track or a one-line description]", "reg", 24, 5.6, 0),
    ("S1 name", "[Presenter Name], [Role]", "bold", 18, 5.6, 0),
    ("S1 lab", "Advanced Telerobotics Research Lab", "reg", 18, 5.6, 0),
    ("S1 dept", "Department of Computer Science, Kent State University", "reg", 18, 5.6, 0),
    ("S1 hud", "[VENUE]  //  [MONTH D, YYYY]", "mono", 14, 6.2, 1.2),
    ("S2 item1", "Context and motivation", "semi", 24, 4.48, 0),
    ("S2 item2", "Immersive teleoperation", "semi", 24, 4.48, 0),
    ("S2 item3", "[Project name]: system and approach", "semi", 24, 4.48, 0),
    ("S2 item4", "Results and lessons learned", "semi", 24, 4.48, 0),
    ("S2 item5", "Outlook and collaboration", "semi", 24, 4.48, 0),
    ("S2 card v1", "[Conference name]", "reg", 18, 2.27, 0),
    ("S2 card v3", "[40 min + Q&A]", "reg", 18, 2.27, 0),
    ("S3 title", "Telepresence and tele-embodiment", "bold", 44, 6.8, 0),
    ("S3 sub", "How an operator sees, moves and acts through a remote robot", "reg", 24, 6.8, 0),
    ("S4 h1", "Telepresence", "semi", 24, 2.87, 0),
    ("S4 h2", "Tele-embodiment", "semi", 24, 2.87, 0),
    ("S4 h3", "Physical AI", "semi", 24, 2.87, 0),
    ("S4 b1", "Mobile robots that carry a remote person's video, audio and motion across a network.", "reg", 18, 2.87, 0),
    ("S4 b2", "Immersive interfaces (VR, tracked controllers, haptics) that let an operator act through a distant robot.", "reg", 18, 2.87, 0),
    ("S4 b3", "Perception, planning and learning that let robots handle routine work and hand control back when it matters.", "reg", 18, 2.87, 0),
    ("S5 sub", "The operator's loop", "semi", 24, 3.63, 0),
    ("S5 bul1", "Head and hand motion in VR map onto the robot's joints", "reg", 18, 3.28, 0),
    ("S5 bul2", "Commands cross the network; video and haptic cues return", "reg", 18, 3.28, 0),
    ("S5 bul3", "Latency, bandwidth and safety limits shape the interface", "reg", 18, 3.28, 0),
    ("S5 fig", "FIG. 01 // CONCEPT ILLUSTRATION", "mono", 14, 4.57, 1.2),
    ("S5 title", "Tele-embodiment: act through a remote robot", "bold", 32, 9.0, 0),
    ("S6 title", "Results: [task completion time by interface]", "bold", 32, 9.0, 0),
    ("S6 eyebrow", "KEY RESULT", "mono", 14, 2.27, 1.2),
    ("S6 label", "[Lower mean task time than the baseline]", "reg", 18, 2.27, 0),
    ("S6 ph", "PLACEHOLDER VALUES", "mono", 14, 2.27, 1.2),
    ("S6 source", "SOURCE // [STUDY OR DATASET], N = [24]", "mono", 14, 5.93, 1.2),
    ("S7 thanks", "Thank you", "bold", 60, 6.2, 0),
    ("S7 lab", "Advanced Telerobotics Research Lab", "semi", 24, 6.2, 0),
    ("S7 dept", "Department of Computer Science, Kent State University", "reg", 18, 6.2, 0),
    ("S7 addr1", "241 Mathematical Sciences Building", "reg", 18, 5.8, 0),
    ("S7 addr2", "1300 Lefton Esplanade, Kent, OH 44242-0001", "reg", 18, 5.8, 0),
    ("S7 social", "@atrlab_kent on X  //  ATR-Lab on GitHub", "reg", 18, 5.8, 0),
    ("HUD left", "ATR LAB // KENT STATE UNIVERSITY", "mono", 14, 6.2, 1.2),
]
for label, t, f, pt, bw, tr in BLOCKS:
    lines = wrap(t, f, pt, bw, tr)
    w = max(width_in(l, f, pt, tr) for l in lines)
    flag = "" if len(lines) == 1 else f"  <-- {len(lines)} lines"
    print(f"{label:12s} {pt:>3}pt box {bw:.2f}in  max line {w:.2f}in{flag}")
    if len(lines) > 1:
        for l in lines: print("      |", l)
