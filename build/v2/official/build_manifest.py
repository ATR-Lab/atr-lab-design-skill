"""Build atr-lab-design/assets/logos/ksu/official-sources.json from the extracted official archives."""
import hashlib, json, os, sys
from collections import OrderedDict
from PIL import Image
import numpy as np

X = sys.argv[1]          # extracted folder
OUT = sys.argv[2]
RETRIEVED = "2026-11-03"
PAGE = "https://www.kent.edu/brand/logos"
ARCH = OrderedDict([
    ("stacked", OrderedDict(url="https://s3.amazonaws.com/undeniable.kent.edu/files/Kent+State+University+Stacked.zip",
                            bytes=10117985,
                            sha256="a5bae3e3a4d4769e03b270600a61227489c3208d5598734bb2338020e551e7ed",
                            root="Kent State University Stacked",
                            png_dir="Kent State University Stacked,PNGs",
                            eps_dir="Kent State University Stacked EPSs",
                            stem="kent_state_university_stacked_")),
    ("horizontal", OrderedDict(url="https://s3.amazonaws.com/undeniable.kent.edu/brand/kent-state-university-Horizontal.zip",
                               bytes=10105917,
                               sha256="88fc9f63910081e6d44531ccb7a19bc4615e2231aba9d0d2547a4c73cea75389",
                               root="kent state university Horizontal",
                               png_dir="kent state university Horizontal PNGs",
                               eps_dir="kent state university Horizontal EPSs",
                               stem="kent_state_university Horizontal_")),
])
# variant -> (png suffix per lockup, eps suffix per lockup, label, colors, background, use)
VARIANTS = [
    ("color", {"stacked": "2-color", "horizontal": "2G-CMYK"}, {"stacked": "2-color", "horizontal": "2-color"},
     "Two-color: KENT STATE and UNIVERSITY in Kent State Blue, sunburst in Kent State Gold",
     "Kent State Blue PMS 281 and Kent State Gold PMS 124 (EPS: spot colors)",
     "white or mist",
     "The default Kent State signature on white or mist: flyers, one-pagers, slides with a light background, "
     "documents, web pages."),
    ("white", {"stacked": "White", "horizontal": "White"}, {"stacked": "White", "horizontal": "White"},
     "All White Reverse", "white only", "navy or midnight (plain area)",
     "The Kent State signature on navy or midnight: poster headers, navy flyer bands, title slides, web footers."),
    ("reverse-gold", {"stacked": "124-White", "horizontal": "124-White"},
     {"stacked": "124-White", "horizontal": "124-White"},
     "Two-Color Reverse: white type with a Kent State Gold sunburst", "white and Kent State Gold PMS 124",
     "navy or midnight (plain area)",
     "Alternative to the all-white reverse on navy when the gold sunburst should show."),
    ("blue", {"stacked": "1-color", "horizontal": "1-color"}, {"stacked": "1-color", "horizontal": "1-color"},
     "All Blue (one color)", "Kent State Blue PMS 281 only", "white, mist or Kent State Gold",
     "One-color jobs and the only Kent State version for a gold background."),
]
MIN = {
    "stacked": OrderedDict(width_in=1.05, width_px=100,
                           why="Kent State minimum: one inch with UNIVERSITY at least one inch long; UNIVERSITY "
                               "spans 99.6% of the Stacked width. Screens: lab convention, UNIVERSITY at least 96 px."),
    "horizontal": OrderedDict(width_in=1.2, width_px=115,
                              why="Kent State minimum: UNIVERSITY at least one inch long; UNIVERSITY spans 84.3% of "
                                  "the Horizontal width (measured on the official PNG). Screens: lab convention, "
                                  "UNIVERSITY at least 96 px."),
}
CLEAR = {"stacked": 0.305, "horizontal": 0.493}  # K height / logo height, measured on the official PNG


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def pixel_sha(p):
    im = Image.open(p).convert("RGBA")
    return hashlib.sha256(im.tobytes()).hexdigest()


assets = []
for lockup, a in ARCH.items():
    for var, pngs, epss, label, colors, bg, use in VARIANTS:
        for fmt in ("png", "eps") + (("eps-cmyk",) if var == "color" else ()):
            if fmt == "png":
                member = f"{a['root']}/{a['png_dir']}/{a['stem']}{pngs[lockup]}.png"
            elif fmt == "eps":
                member = f"{a['root']}/{a['eps_dir']}/{a['stem']}{epss[lockup]}.eps"
            else:
                member = f"{a['root']}/{a['eps_dir']}/{a['stem']}CMYK.eps"
            p = os.path.join(X, member)
            aid = f"ksu-{lockup}-{var}-" + {"png": "png", "eps": "eps", "eps-cmyk": "cmyk-eps"}[fmt]
            e = OrderedDict()
            e["id"] = aid
            e["lockup"] = lockup
            e["variant"] = var
            e["label"] = label if fmt != "eps-cmyk" else "Two-color, process CMYK build"
            e["format"] = "png" if fmt == "png" else "eps"
            e["kind"] = "raster" if fmt == "png" else "vector"
            e["colors"] = colors if fmt != "eps-cmyk" else "process CMYK equivalents of PMS 281 and PMS 124"
            e["background"] = bg
            e["archive"] = lockup
            e["member"] = member
            e["sha256"] = sha(p)
            e["bytes"] = os.path.getsize(p)
            if fmt == "png":
                im = Image.open(p)
                e["pixels"] = list(im.size)
                e["pixel_sha256"] = pixel_sha(p)
                e["native_ppi"] = 300
                e["vector_master"] = f"ksu-{lockup}-{var}-eps"
            else:
                head = open(p, "rb").read(4000).decode("latin1")
                import re
                bb = re.search(r"%%HiResBoundingBox: ([\d. ]+)", head).group(1).split()
                e["size_pt"] = [round(float(bb[2]), 2), round(float(bb[3]), 2)]
                e["raster_preview"] = f"ksu-{lockup}-{var}-png"
            e["min_size"] = MIN[lockup]
            e["clear_space"] = OrderedDict(k_height_ratio=CLEAR[lockup],
                                           rule="Keep the height of the K in KENT clear on every side.")
            if fmt == "png":
                e["intended_use"] = use + " PNG: on-screen use and office files (300 ppi at "
                e["intended_use"] += (f"{e['pixels'][0] / 300:.2f} in wide"
                                      f"; still 150 ppi or more up to {e['pixels'][0] / 150:.1f} in wide on posters).")
            elif fmt == "eps":
                e["intended_use"] = use + " EPS: vector master for commercial print, large format and vendors."
            else:
                e["intended_use"] = "Vector master for printers that ask for process (CMYK) art instead of spot colors."
            e["retrieved"] = RETRIEVED
            assets.append(e)

m = OrderedDict()
m["schema"] = "atr-lab-design/official-sources/1"
m["description"] = ("Official Kent State University wordmark files the ATR Lab uses, with their exact source and "
                    "checksum. The files themselves are not in the skill: fetch them with "
                    "scripts/official_assets.py fetch <id|all>, which verifies each SHA-256.")
m["publisher"] = "Kent State University, Division of University Communications and Marketing (UCM)"
m["source_page"] = PAGE
m["terms"] = OrderedDict(
    redistribution="not granted",
    summary=("Kent State publishes these files for download on its brand site but states no redistribution "
             "license. All official marks and logos are registered trademarks of Kent State University and "
             "\"may not be used without permission\"; licensing requests go to the Office of General Counsel. "
             "So the skill ships this manifest and a fetch command, not the files."),
    pages=["https://www.kent.edu/brand/logos",
           "https://www.kent.edu/ucm/ownership-kent-state-university-marks-and-logos"],
    checked=RETRIEVED)
m["retrieved"] = RETRIEVED
m["archives"] = OrderedDict()
for k, a in ARCH.items():
    m["archives"][k] = OrderedDict(url=a["url"], source_page=PAGE, bytes=a["bytes"], sha256=a["sha256"],
                                   sha256_note="checksum of the archive when retrieved; Kent State may re-zip it, so "
                                               "only the member checksums below are enforced",
                                   retrieved=RETRIEVED)
m["not_listed"] = [
    "Black, CMYK reverse and JPG versions (in the same archives; not used by the lab)",
    "Horizontal 2G-RGB PNG (UNIVERSITY in gold; the lab uses the 2G-CMYK PNG, which matches the 2-color EPS)",
    "University Seal (permissions required), K Emblem and all athletics marks (the lab does not use them)",
]
m["assets"] = assets
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(m, f, indent=2, ensure_ascii=False)
    f.write("\n")
print(len(assets), "assets")
