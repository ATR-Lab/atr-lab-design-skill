#!/usr/bin/env python3
"""
motion.py: animated backgrounds and the Teo cameo for slides and hallway TV slides
==================================================================================

The motion motifs are Lottie files built in LottieFiles Creator and kept in assets/motion/ (see its
README): a drifting triangle lattice with glowing cells, a blueprint grid with a scanning band, flowing
chevrons, and Teo, the lab's mascot, as a puppet rig that pops up, waves and ducks away. This module
recolours a motif for its ground, renders it with rlottie, lays it under the still design (calmed under
text, kept off logos, QR codes, photos and the hazard band), adds the cameo if asked, and encodes a
seamless 12-second loop as an H.264 MP4 plus a poster frame for the still version.

banner.py (--motion) and new_deck.py ("motion" in the spec) call it; you rarely need it directly.

Usage
-----
    python3 scripts/motion.py list [--json]
    python3 scripts/motion.py preview lattice-drift --ground navy -o lattice.mp4 [--strength subtle]
        [--size 1920x1080] [--seconds 12] [--teo-cameo] [--poster lattice.png]
    python3 scripts/motion.py check clip.mp4        # flash (WCAG 2.3.1) and loop-seam check of any MP4

Rules it enforces (references/graphic-elements.md section 8):
- Motifs move slowly and loop seamlessly: 12 s at 30 fps; the lattice and chevrons drift 16 px/s at 1080p.
- Nothing flashes: a frame-to-frame luminance check fails anything with more than 3 flashes in a second.
- Under text the motif is turned down until the ground shifts by at most 1.15:1, so the copy keeps its
  checked contrast; logos, QR codes, photos, charts and the hazard band get none of it.
- The Teo cameo appears only when asked for (--teo-cameo / "teo_cameo": true) and only where it touches
  no text, logo or QR code; otherwise it is refused.

Needs rlottie-python and numpy, plus ffmpeg (on PATH, or the imageio-ffmpeg package) to write MP4s.
"""
from __future__ import annotations

import argparse
import copy
import functools
import hashlib
import json
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Iterator, Optional

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import numpy as np  # noqa: E402
from PIL import Image, ImageFilter  # noqa: E402

import atr_brand as B  # noqa: E402

__version__ = "1.0.0"
MOTION_DIR = B.ASSETS / "motion"
FPS = 30
LOOP_FRAMES = 360                    # 12 s; every motif loops on this length
TEXT_SHIFT_MAX = 1.15                # largest contrast shift the motif may cause under text
CAMEO_HEIGHTS = (0.42, 0.38, 0.34, 0.30, 0.27, 0.24)   # cameo square as a share of the frame height, largest that fits
CAMEO_POSTER_FRAME = 150             # Teo up, eyes open, between the wave and the ear flicks
FLASH_LIMIT = 3                      # WCAG 2.3.1: no more than three flashes in any one second


class MotionError(RuntimeError):
    """A motion request that cannot be met (unknown motif, no room for the cameo, missing renderer)."""


# --------------------------------------------------------------------------- motifs and palettes
@dataclass(frozen=True)
class Motif:
    name: str
    file: str
    roles: dict                      # Lottie layer name -> palette role (None: keep as built, e.g. a matte)
    poster_frame: int
    summary: str


MOTIFS = {
    "lattice-drift": Motif(
        "lattice-drift", "lattice-drift.json",
        {"lines": "line", "glow-1": "glow", "glow-2": "glow", "glow-3": "glow", "glow-4": "glow"}, 45,
        "The 60-degree triangle lattice drifting right; one cell at a time glows and fades (3 s each)."),
    "grid-scan": Motif(
        "grid-scan", "grid-scan.json",
        {"grid-minor": "minor", "grid-major": "major", "nodes": "node", "nodes-lit": "lit", "scan": "scan",
         "scan-matte": None}, 120,
        "The blueprint grid, still, with a soft scan band sweeping left to right that lights the nodes it passes."),
    "chevron-flow": Motif(
        "chevron-flow", "chevron-flow.json", {"chevrons": "line"}, 0,
        "Rows of chevrons travelling right, tone on tone."),
}
CAMEO_FILE = "teo-cameo.json"

# ground -> strength -> role -> (token, alpha). "full" is for bookend slides and TV slides, "subtle" for
# content slides. Roles a motif does not use are ignored.
PALETTES = {
    "lattice-drift": {
        "navy": {"full": {"line": ("gold", 0.12), "glow": ("sky", 0.30)},
                 "subtle": {"line": ("gold", 0.07), "glow": ("gold", 0.0)}},
        "midnight": {"full": {"line": ("navy", 1.0), "glow": ("sky", 0.28)},
                     "subtle": {"line": ("navy", 0.6), "glow": ("gold", 0.0)}},
        "gold": {"full": {"line": ("navy", 0.14), "glow": ("white", 0.30)},
                 "subtle": {"line": ("navy", 0.07), "glow": ("navy", 0.0)}},
        "white": {"full": {"line": ("line", 1.0), "glow": ("gold", 0.16)},
                  "subtle": {"line": ("line", 0.45), "glow": ("gold", 0.0)}},
    },
    "grid-scan": {
        "navy": {"full": {"minor": ("mist", 0.07), "major": ("mist", 0.16), "node": ("mist", 0.28),
                          "lit": ("gold", 0.85), "scan": ("sky", 0.14)},
                 "subtle": {"minor": ("mist", 0.04), "major": ("mist", 0.09), "node": ("mist", 0.14),
                            "lit": ("gold", 0.30), "scan": ("sky", 0.05)}},
        "midnight": {"full": {"minor": ("mist", 0.06), "major": ("mist", 0.14), "node": ("mist", 0.25),
                              "lit": ("gold", 0.85), "scan": ("sky", 0.14)},
                     "subtle": {"minor": ("mist", 0.04), "major": ("mist", 0.08), "node": ("mist", 0.12),
                                "lit": ("gold", 0.30), "scan": ("sky", 0.05)}},
        "gold": {"full": {"minor": ("navy", 0.06), "major": ("navy", 0.12), "node": ("navy", 0.22),
                          "lit": ("navy", 0.60), "scan": ("white", 0.22)},
                 "subtle": {"minor": ("navy", 0.03), "major": ("navy", 0.06), "node": ("navy", 0.10),
                            "lit": ("navy", 0.25), "scan": ("white", 0.10)}},
        "white": {"full": {"minor": ("line", 0.55), "major": ("line", 1.0), "node": ("line", 1.0),
                           "lit": ("sky", 0.70), "scan": ("sky", 0.07)},
                  "subtle": {"minor": ("line", 0.30), "major": ("line", 0.60), "node": ("line", 0.60),
                             "lit": ("sky", 0.30), "scan": ("sky", 0.03)}},
    },
    "chevron-flow": {
        "navy": {"full": {"line": ("midnight", 1.0)}, "subtle": {"line": ("midnight", 0.55)}},
        "midnight": {"full": {"line": ("navy", 1.0)}, "subtle": {"line": ("navy", 0.55)}},
        "gold": {"full": {"line": ("navy", 0.10)}, "subtle": {"line": ("navy", 0.05)}},
        "white": {"full": {"line": ("line", 1.0)}, "subtle": {"line": ("line", 0.45)}},
    },
}
GROUND_NAMES = ("navy", "midnight", "gold", "white")
STRENGTHS = ("full", "subtle")


def motif(name: str) -> Motif:
    if name not in MOTIFS:
        import difflib
        close = difflib.get_close_matches(str(name), list(MOTIFS), n=2, cutoff=0.4)
        raise MotionError(f"unknown motif '{name}'" + (f"; did you mean {', '.join(close)}?" if close else "")
                          + f" Motifs: {', '.join(MOTIFS)}")
    return MOTIFS[name]


def palette(name: str, ground: str, strength: str = "full") -> dict:
    """{role: (rgb tuple 0-255, alpha)} for a motif on a ground."""
    if ground not in GROUND_NAMES:
        raise MotionError(f"ground '{ground}': use {', '.join(GROUND_NAMES)}")
    if strength not in STRENGTHS:
        raise MotionError(f"strength '{strength}': use {', '.join(STRENGTHS)}")
    return {role: (B.rgb(tok), a) for role, (tok, a) in PALETTES[motif(name).name][ground][strength].items()}


def nearest_ground(rgb: tuple) -> str:
    """The palette ground closest to a field color (for a slide background image or a solid fill)."""
    return min(GROUND_NAMES, key=lambda g: sum((a - b) ** 2 for a, b in zip(B.rgb(g), rgb)))


# --------------------------------------------------------------------------- Lottie recolouring
@functools.lru_cache(maxsize=None)
def _file_hash(file: str) -> str:
    return hashlib.sha256((MOTION_DIR / file).read_bytes()).hexdigest()


@functools.lru_cache(maxsize=None)
def _load(file: str) -> dict:
    return json.loads((MOTION_DIR / file).read_text(encoding="utf-8"))


def _paint(items: list, rgb01: list, alpha: float) -> None:
    """Set every fill, stroke and gradient in a shape list to one color, scaling its opacity by alpha."""
    for it in items:
        ty = it.get("ty")
        if ty == "gr":
            _paint(it.get("it", []), rgb01, alpha)
        elif ty in ("fl", "st"):
            it["c"] = {"a": 0, "k": rgb01 + [1]}
            it["o"] = {"a": 0, "k": 100 * alpha}
        elif ty in ("gf", "gs"):
            n = it["g"]["p"]
            k = list(it["g"]["k"]["k"])
            for i in range(n):
                k[4 * i + 1:4 * i + 4] = rgb01
            it["g"]["k"]["k"] = k
            it["o"] = {"a": 0, "k": 100 * alpha}


def recolor(anim: dict, roles: dict, pal: dict) -> dict:
    """A copy of a motif with each named layer painted in its role's color and strength. A layer whose
    role has alpha 0 is hidden; a layer mapped to None (a matte source) is left as built."""
    out = copy.deepcopy(anim)
    for layer in out["layers"]:
        role = roles.get(layer.get("nm"))
        if role is None or role not in pal:
            continue
        rgb, alpha = pal[role]
        if alpha <= 0:
            layer["hd"] = True
            continue
        _paint(layer.get("shapes", []), [c / 255 for c in rgb], alpha)
    return out


# --------------------------------------------------------------------------- rendering
def _rlottie():
    try:
        from rlottie_python import LottieAnimation
    except ImportError as e:
        raise MotionError("motion needs rlottie-python: .venv/bin/pip install rlottie-python") from e
    return LottieAnimation


class Renderer:
    """Renders one Lottie animation to premultiplied RGBA float arrays at a fixed size."""

    def __init__(self, anim: dict, size: tuple):
        self.size = size
        self._anim = _rlottie().from_data(json.dumps(anim))
        self.frames = int(round(anim["op"] - anim.get("ip", 0)))

    def frame(self, n: int) -> np.ndarray:
        w, h = self.size
        buf = self._anim.lottie_animation_render(frame_num=n % self.frames, width=w, height=h)
        bgra = np.frombuffer(buf, dtype=np.uint8).reshape(h, w, 4)
        return bgra[..., [2, 1, 0, 3]].astype(np.float32) / 255.0        # premultiplied RGBA


@functools.lru_cache(maxsize=4)
def cameo_extent(probe: int = 200) -> tuple:
    """Where Teo can appear inside the cameo square, as fractions (x0, y0, x1, y1) of its side: the union
    of every frame's visible pixels, so a placement keeps all of the motion clear of text and logos."""
    r = Renderer(_load(CAMEO_FILE), (probe, probe))
    acc = np.zeros((probe, probe), dtype=bool)
    for n in range(0, r.frames, 3):
        acc |= r.frame(n)[..., 3] > 0.02
    ys, xs = np.nonzero(acc)
    return (xs.min() / probe, ys.min() / probe, (xs.max() + 1) / probe, (ys.max() + 1) / probe)


# --------------------------------------------------------------------------- masks
def text_level(pal: dict, ground_rgb: tuple) -> float:
    """The largest mask value under text that keeps every role within TEXT_SHIFT_MAX of the ground."""
    g = np.array(ground_rgb, dtype=float) / 255
    worst = 1.0
    for rgb, alpha in pal.values():
        if alpha <= 0:
            continue
        c = np.array(rgb, dtype=float) / 255
        lo, hi = 0.0, 1.0
        if _shift(g, g + (c - g) * alpha) <= TEXT_SHIFT_MAX:
            continue
        for _ in range(30):
            mid = (lo + hi) / 2
            if _shift(g, g + (c - g) * alpha * mid) <= TEXT_SHIFT_MAX:
                lo = mid
            else:
                hi = mid
        worst = min(worst, lo)
    return worst


def _lum(c: np.ndarray) -> float:
    lin = np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    return float(0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2])


def _shift(a: np.ndarray, b: np.ndarray) -> float:
    la, lb = _lum(a), _lum(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


@dataclass
class Zones:
    """Rectangles (x0, y0, x1, y1) in output pixels: where the motif must stay off (hard), where it is
    turned down (text), and which hard zones the cameo may rise from behind (behind: an edge band). floor is
    the y the cameo rises from: the top of a bottom band, so the band hides where Teo is cut off."""
    hard: list = field(default_factory=list)
    text: list = field(default_factory=list)
    behind: list = field(default_factory=list)
    floor: Optional[float] = None


def build_mask(size: tuple, zones: Zones, level: float, feather: float) -> np.ndarray:
    """1 where the motif runs at full strength, `level` under text, 0 on hard zones; edges feathered."""
    w, h = size
    m = Image.new("L", (w, h), 255)
    for r in zones.text:
        m.paste(int(round(255 * level)), tuple(int(round(v)) for v in _clip(r, w, h)))
    for r in zones.hard:
        m.paste(0, tuple(int(round(v)) for v in _clip(r, w, h)))
    if feather > 0:
        m = m.filter(ImageFilter.GaussianBlur(feather))
        for r in zones.hard:                                    # blur must not lift a hard zone off zero
            m.paste(0, tuple(int(round(v)) for v in _clip(r, w, h)))
    return np.asarray(m, dtype=np.float32) / 255.0


def _clip(r, w, h):
    return (max(0, r[0]), max(0, r[1]), min(w, r[2]), min(h, r[3]))


def _hits(a, b) -> bool:
    return a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]


def place_cameo(size: tuple, zones: Zones, prefer: str = "right") -> tuple:
    """(x, y, side) of the cameo square: bottom edge on the floor (the frame bottom, or the top of a bottom
    band he rises from behind), largest size first, scanning from the preferred side for a spot where all of his motion stays
    clear of every zone except the bands he passes behind. Raises MotionError when there is none."""
    w, h = size
    ex = cameo_extent()
    pad = 0.012 * w
    step = max(4, int(0.01 * w))
    blockers = [z for z in zones.hard if z not in zones.behind] + zones.text
    for share in CAMEO_HEIGHTS:
        side = int(round(share * h))
        y = int(round(zones.floor if zones.floor is not None else h)) - side
        xs = list(range(w - side, -side, -step)) if prefer == "right" else list(range(-side, w - side, step))
        for x in xs:
            body = (x + ex[0] * side - pad, y + ex[1] * side - pad, x + ex[2] * side + pad, y + ex[3] * side + pad)
            if body[0] < 0 or body[2] > w:
                continue
            if not any(_hits(body, z) for z in blockers):
                return x, y, side
    raise MotionError("no room for the Teo cameo: every spot along the bottom edge touches text, a logo, "
                      "the QR code or a photo; shorten the copy, drop the image, or leave the cameo out")


# --------------------------------------------------------------------------- composition
@dataclass
class MotionJob:
    """One animated background: the still ground (RGB image at the output size), the motif and palette,
    the zones, an optional foreground (RGBA, drawn on top: text, logos, bands) and an optional cameo."""
    ground: Image.Image
    motif: Optional[str]                 # None: a still ground (a cameo on its own)
    ground_name: str
    strength: str = "full"
    zones: Zones = field(default_factory=Zones)
    foreground: Optional[Image.Image] = None
    cameo: bool = False
    cameo_prefer: str = "right"
    seconds: float = LOOP_FRAMES / FPS

    @property
    def size(self) -> tuple:
        return self.ground.size

    @property
    def poster_index(self) -> int:
        if self.cameo:
            return CAMEO_POSTER_FRAME
        return motif(self.motif).poster_frame if self.motif else 0

    def key(self) -> str:
        """A content hash: equal jobs make byte-equal videos, so callers can cache and share them."""
        h = hashlib.sha256()
        h.update(json.dumps([PALETTES.get(self.motif), _file_hash(motif(self.motif).file) if self.motif else None,
                             _file_hash(CAMEO_FILE) if self.cameo else None]).encode())
        h.update(json.dumps([__version__, self.motif, self.ground_name, self.strength, self.cameo,
                             self.cameo_prefer, round(self.seconds, 3), list(self.size),
                             self.zones.hard, self.zones.text, self.zones.behind, self.zones.floor]).encode())
        h.update(self.ground.convert("RGB").tobytes())
        if self.foreground is not None:
            h.update(self.foreground.tobytes())
        return h.hexdigest()[:16]


class Composer:
    """Turns a MotionJob into RGB frames."""

    def __init__(self, job: MotionJob):
        self.job = job
        w, h = job.size
        self.ground = np.asarray(job.ground.convert("RGB"), dtype=np.float32) / 255.0
        self.level = 1.0
        self.motif = None
        if job.motif:
            m = motif(job.motif)
            pal = palette(m.name, job.ground_name, job.strength)
            mean = tuple(int(v) for v in np.round(self.ground.reshape(-1, 3).mean(0) * 255))
            self.level = text_level(pal, mean)
            self.mask = build_mask(job.size, job.zones, self.level, feather=0.012 * h)[..., None]
            self.motif = Renderer(recolor(_load(m.file), m.roles, pal), job.size)
        self.cameo_box = None
        self.cameo = None
        if job.cameo:
            x, y, side = place_cameo(job.size, job.zones, job.cameo_prefer)
            self.cameo_box = (x, y, side)
            self.cameo = Renderer(_load(CAMEO_FILE), (side, side))
        self.fg = None
        if job.foreground is not None:
            fg = np.asarray(job.foreground.convert("RGBA"), dtype=np.float32) / 255.0
            self.fg = np.concatenate([fg[..., :3] * fg[..., 3:], fg[..., 3:]], axis=2)

    def frame(self, n: int) -> np.ndarray:
        out = self.ground.copy()
        if self.motif is not None:
            f = self.motif.frame(n)
            out = out * (1 - f[..., 3:] * self.mask) + f[..., :3] * self.mask
        if self.cameo is not None:
            x, y, side = self.cameo_box
            c = self.cameo.frame(n)
            w, h = self.job.size
            x0, y0, x1, y1 = max(0, x), max(0, y), min(w, x + side), min(h, y + side)
            cc = c[y0 - y:y1 - y, x0 - x:x1 - x]
            region = out[y0:y1, x0:x1]
            out[y0:y1, x0:x1] = region * (1 - cc[..., 3:]) + cc[..., :3]
        if self.fg is not None:
            out = out * (1 - self.fg[..., 3:]) + self.fg[..., :3]
        return out

    def frames(self) -> Iterator[np.ndarray]:
        for n in range(int(round(self.job.seconds * FPS))):
            yield self.frame(n)

    def poster(self) -> Image.Image:
        return to_image(self.frame(self.job.poster_index))


def to_image(f: np.ndarray) -> Image.Image:
    return Image.fromarray(np.clip(f * 255 + 0.5, 0, 255).astype(np.uint8), "RGB")


# --------------------------------------------------------------------------- encoding and checks
def ffmpeg_exe() -> str:
    exe = shutil.which("ffmpeg")
    if exe:
        return exe
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError as e:
        raise MotionError("writing MP4 needs ffmpeg (brew install ffmpeg) or .venv/bin/pip install "
                          "imageio-ffmpeg") from e


class FlashMeter:
    """WCAG 2.3.1 general-flash check on a 32x18 grid of the frame: a transition is a change of 10 % or more
    in relative luminance where the darker state is below 0.80, over more than 2.5 % of the frame (about a
    10-degree field at viewing distance); a flash is a pair of opposite transitions."""

    def __init__(self):
        self.prev = None
        self.events: list = []        # (frame, sign)
        self.seam: list = []
        self.first = None

    @staticmethod
    def _grid(f: np.ndarray) -> np.ndarray:
        lin = np.where(f <= 0.04045, f / 12.92, ((f + 0.055) / 1.055) ** 2.4)
        lum = lin[..., 0] * 0.2126 + lin[..., 1] * 0.7152 + lin[..., 2] * 0.0722
        h, w = lum.shape
        gh, gw = 18, 32
        return lum[: h // gh * gh, : w // gw * gw].reshape(gh, h // gh, gw, w // gw).mean(axis=(1, 3))

    def add(self, n: int, f: np.ndarray) -> None:
        g = self._grid(f)
        if self.first is None:
            self.first = g
        if self.prev is not None:
            d = g - self.prev
            big = (np.abs(d) >= 0.10) & (np.minimum(g, self.prev) < 0.80)
            if big.mean() > 0.025:
                self.events.append((n, int(np.sign(d[big].mean()))))
            self.seam.append(float(np.abs(d).mean()))
        self.prev = g

    def report(self) -> dict:
        flashes = []
        for (a, sa), (b, sb) in zip(self.events, self.events[1:]):
            if sa != sb:
                flashes.append(b)
        worst = max((sum(1 for t in flashes if s <= t < s + FPS) for s in flashes), default=0)
        steady = float(np.median(self.seam)) if self.seam else 0.0
        seam = float(np.abs(self.first - self.prev).mean()) if self.first is not None else 0.0
        return {"flashes_per_second_max": worst, "flash_ok": worst <= FLASH_LIMIT,
                "seam_delta": round(seam, 5), "frame_delta_median": round(steady, 5),
                "loop_ok": seam <= max(3 * steady, 0.004)}


def encode(frames: Iterator[np.ndarray], size: tuple, out: Path, crf: int = 18,
           progress: Optional[Callable[[int], None]] = None) -> dict:
    """Write frames to an H.264 MP4 (yuv420p, 30 fps, no audio, faststart) and measure them on the way."""
    w, h = size
    if w % 2 or h % 2:
        raise MotionError(f"video size {w}x{h} must be even in both directions")
    level = "4.1" if w * h <= 1920 * 1088 else "5.1"
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = out.with_suffix(".part.mp4")
    cmd = [ffmpeg_exe(), "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{w}x{h}",
           "-r", str(FPS), "-i", "-", "-an", "-c:v", "libx264", "-preset", "slow", "-crf", str(crf),
           "-tune", "animation", "-profile:v", "high", "-level", level, "-pix_fmt", "yuv420p",
           "-x264-params", "keyint=60:min-keyint=60:scenecut=0", "-threads", "4", "-movflags", "+faststart",
           "-metadata", "comment=ATR Lab motion background", str(tmp)]
    meter = FlashMeter()
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    n = 0
    try:
        for n, f in enumerate(frames):
            meter.add(n, f)
            proc.stdin.write(np.clip(f * 255 + 0.5, 0, 255).astype(np.uint8).tobytes())
            if progress:
                progress(n)
    finally:
        proc.stdin.close()
        rc = proc.wait()
    if rc != 0:
        tmp.unlink(missing_ok=True)
        raise MotionError(f"ffmpeg failed ({rc}) writing {out}")
    os.replace(tmp, out)
    rep = meter.report()
    rep.update({"frames": n + 1, "seconds": round((n + 1) / FPS, 2), "size": [w, h], "bytes": out.stat().st_size})
    return rep


def render_job(job: MotionJob, out: Path, progress=None) -> tuple:
    """Encode a job to `out` (MP4). Returns (poster RGB image, report dict). Refuses a clip that flashes."""
    comp = Composer(job)
    rep = encode(comp.frames(), job.size, out, progress=progress)
    rep.update({"motif": job.motif or "none", "ground": job.ground_name, "strength": job.strength,
                "text_level": round(comp.level, 3), "poster_frame": job.poster_index})
    if comp.cameo_box:
        rep["cameo_box"] = list(comp.cameo_box)
    if not rep["flash_ok"]:
        out.unlink(missing_ok=True)
        raise MotionError(f"{out.name}: {rep['flashes_per_second_max']} flashes in one second (limit {FLASH_LIMIT})")
    return comp.poster(), rep


def cache_dir() -> Path:
    """${ATR_DESIGN_CACHE:-~/.cache/atr-lab-design}/motion: rendered loops, keyed by content."""
    base = os.environ.get("ATR_DESIGN_CACHE") or os.path.join("~", ".cache", "atr-lab-design")
    p = Path(base).expanduser() / "motion"
    p.mkdir(parents=True, exist_ok=True)
    return p


def render_cached(job: MotionJob, progress=None) -> tuple:
    """(mp4 path, poster PNG path, report) for a job, reusing an earlier render of the same job."""
    key = job.key()
    d = cache_dir()
    stem = f"{job.motif or 'still'}{'-teo' if job.cameo else ''}-{key}"
    mp4, png, rep_path = d / f"{stem}.mp4", d / f"{stem}.png", d / f"{stem}.json"
    if mp4.exists() and png.exists() and rep_path.exists():
        return mp4, png, json.loads(rep_path.read_text())
    poster, rep = render_job(job, mp4, progress=progress)
    poster.save(png, optimize=True)
    rep_path.write_text(json.dumps(rep))
    return mp4, png, rep


def check_file(path: Path) -> dict:
    """Decode an MP4 and run the flash and loop-seam checks on it."""
    probe = subprocess.run([ffmpeg_exe(), "-i", str(path)], capture_output=True, text=True).stderr
    import re
    m = re.search(r"Video:.*?(\d{2,5})x(\d{2,5})", probe)
    if not m:
        raise MotionError(f"{path}: no video stream")
    w, h = int(m.group(1)), int(m.group(2))
    sw, sh = 320, max(2, int(round(320 * h / w / 2)) * 2)
    proc = subprocess.run([ffmpeg_exe(), "-loglevel", "error", "-i", str(path), "-vf", f"scale={sw}:{sh}",
                           "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True)
    raw = np.frombuffer(proc.stdout, dtype=np.uint8).reshape(-1, sh, sw, 3)
    meter = FlashMeter()
    for n, f in enumerate(raw):
        meter.add(n, f.astype(np.float32) / 255)
    rep = meter.report()
    rep.update({"frames": len(raw), "seconds": round(len(raw) / FPS, 2), "size": [w, h]})
    return rep


# --------------------------------------------------------------------------- CLI
def _size(s: str) -> tuple:
    w, h = (int(v) for v in s.lower().split("x"))
    return w, h


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="ATR Lab motion backgrounds (Lottie motifs to looping MP4).")
    sub = ap.add_subparsers(dest="cmd", required=True)
    ls = sub.add_parser("list", help="list the motifs, grounds and strengths")
    ls.add_argument("--json", action="store_true")
    pv = sub.add_parser("preview", help="render a motif on a plain ground")
    pv.add_argument("motif")
    pv.add_argument("--ground", default="navy", choices=GROUND_NAMES)
    pv.add_argument("--strength", default="full", choices=STRENGTHS)
    pv.add_argument("--size", default="1920x1080")
    pv.add_argument("--seconds", type=float, default=LOOP_FRAMES / FPS)
    pv.add_argument("--teo-cameo", action="store_true", help="add the Teo cameo (only when asked for)")
    pv.add_argument("--poster", help="also write the poster frame (PNG or JPEG)")
    pv.add_argument("-o", "--out", required=True)
    ck = sub.add_parser("check", help="flash and loop-seam check of an MP4")
    ck.add_argument("mp4")
    a = ap.parse_args(argv)
    try:
        if a.cmd == "list":
            info = {n: {"summary": m.summary, "file": f"assets/motion/{m.file}", "poster_frame": m.poster_frame,
                        "grounds": list(GROUND_NAMES), "strengths": list(STRENGTHS)} for n, m in MOTIFS.items()}
            info["teo-cameo"] = {"summary": "Teo pops up, waves, blinks and ducks away; only on request.",
                                 "file": f"assets/motion/{CAMEO_FILE}"}
            if a.json:
                print(json.dumps(info, indent=2))
            else:
                for n, v in info.items():
                    print(f"{n:14s} {v['summary']}")
            return 0
        if a.cmd == "check":
            rep = check_file(Path(a.mp4))
            print(json.dumps(rep, indent=2))
            return 0 if rep["flash_ok"] and rep["loop_ok"] else 2
        size = _size(a.size)
        job = MotionJob(Image.new("RGB", size, B.rgb(a.ground)), a.motif, a.ground, a.strength,
                        cameo=a.teo_cameo, seconds=a.seconds)
        poster, rep = render_job(job, Path(a.out), progress=None)
        if a.poster:
            p = Path(a.poster)
            if p.suffix.lower() in (".jpg", ".jpeg"):
                poster.save(p, quality=92, subsampling=0)
            else:
                poster.save(p, optimize=True)
        print(json.dumps(rep, indent=2))
        return 0
    except MotionError as e:
        print(f"motion.py: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
