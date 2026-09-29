"""ATR Lab matplotlib helper: brand fonts, style, palettes, colormaps and IEEE-ready export.

    import atr_plot as atr
    atr.use("ieee")                             # IEEE venue: 9 pt text, light mode
    fig, ax = atr.figure("single")              # 3.5 in wide (IEEE journal column); ICRA/IROS: "ieeeconf" (3.4 in)
    for i, (name, y) in enumerate(series.items()):
        ax.plot(x, y, label=name)               # colors follow the ATR categorical order
    atr.legend_top(ax)                          # 2+ series always get a legend
    atr.label_line_ends(ax)                     # direct labels: optional for <= 4 lines, required (with redundant_lines) for 5-8
    atr.save(fig, "figs/latency")               # -> latency.pdf, latency.svg, latency.png (300 dpi)

Contexts: "paper" (8 pt text, the floor for dense figures at non-IEEE venues), "ieee" (9 pt text: IEEE asks for
"approximately 9-10 point" at final size, so use it for ICRA, IROS, RA-L and T-RO), "slide" (16:9 decks, 14 pt floor),
"poster" (24 pt floor).
Widths for figure(): "single" 3.5 / "double" 7.16 in (IEEE journals, IEEEtran); "ieeeconf" 3.4 / "ieeeconf-double" 7.0 in
(ICRA and IROS, RAS PaperCept ieeeconf.cls); "slide", "slide-half", "poster"; or a number in inches.
Modes: "light" (white surface) or "dark" (ATR dark page #0D1521; for dark slides and dark web pages).

Rules this helper encodes (see ../../references for the full guide):
  * categorical colors are assigned in a fixed order and never cycled; > 8 series -> fold into "Other" or facet
  * series caps by chart form (validator results in dataviz-validation.txt):
      - stacked / grouped bars: all 8 slots (only neighbours touch; the fixed order is validated adjacent-pairs)
      - line charts: at most 4 colored series on color alone. Lines cross, so any two series can touch (an all-pairs
        layout). 5-8 lines need BOTH label_line_ends() and redundant_lines() (per-slot markers + dash patterns),
        or better, small multiples. At 7-8 lines some pairs merge for color-blind readers (orange/green).
      - scatter / bubble / maps / small multiples: at most 4 colored groups (slots 1-4 validate all-pairs)
  * gold (slot 2) is 2.0:1 on white: when gold is a thin line, add direct labels or markers (label_line_ends does both)
  * the plot area sits on the chart surface (white, or #0D1521 in dark mode), never on mist / panel / subtle surfaces
  * 2+ series always get a legend (legend_top); direct labels are added selectively, and are required for 5-8 lines
  * one y-axis per plot (no twinx); gridlines are solid hairlines on y only; labels use text colors, never series colors
  * status colors are reserved for good/bad meaning and never used as "series 5"
Fonts: matplotlib maps weight="light" to 200, which resolves to Source Sans 3 ExtraLight. For Light use weight=300.
Requires matplotlib >= 3.7. No other dependencies.
"""
from __future__ import annotations

import json
import math
import warnings
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.transforms as mtransforms
from matplotlib import font_manager
from matplotlib.colors import LinearSegmentedColormap, ListedColormap

KIT = Path(__file__).resolve().parent
FONT_DIR = KIT.parent / "fonts"
STYLE_FILE = KIT / "atr.mplstyle"
COLORS_FILE = KIT / "colors.json"

# IEEE column widths (inches). Journals (RA-L, T-RO) and IEEEtran conference mode: 3.5 / 7.16 in.
# ICRA and IROS use RAS PaperCept ieeeconf.cls (\textwidth 7.0 in, \columnsep 0.2 in): 3.4 / 7.0 in.
IEEE_SINGLE = 3.5
IEEE_DOUBLE = 7.16
IEEECONF_SINGLE = 3.4
IEEECONF_DOUBLE = 7.0
WIDTHS = {"single": IEEE_SINGLE, "column": IEEE_SINGLE, "double": IEEE_DOUBLE, "page": IEEE_DOUBLE,
          "ieeeconf": IEEECONF_SINGLE, "ieeeconf-single": IEEECONF_SINGLE, "ieeeconf-double": IEEECONF_DOUBLE,
          "slide": 9.2, "slide-half": 4.4, "poster": 14.0}


# --------------------------------------------------------------------------- tokens
def _load_tokens() -> dict:
    with open(COLORS_FILE, encoding="utf-8") as f:
        return json.load(f)


_TOK = _load_tokens()


def token(path: str) -> str:
    """Resolve a DTCG color token path (e.g. 'color.brand.navy' or 'color.semantic.light.text.primary') to hex."""
    node = _TOK
    for p in path.split("."):
        node = node[p]
    v = node["$value"]
    while isinstance(v, str) and v.startswith("{"):
        v = token(v.strip("{}"))
    return v


def _group(path: str) -> list[str]:
    node = _TOK
    for p in path.split("."):
        node = node[p]
    keys = sorted((k for k in node if not k.startswith("$")), key=int)
    return [token(f"{path}.{k}") for k in keys]


NAVY = token("color.brand.navy")
GOLD = token("color.brand.gold")
INK = token("color.functional.ink")
SLATE = token("color.functional.slate")
BRONZE = token("color.functional.bronze")
MIST = token("color.functional.mist")
CATEGORICAL = _group("color.dataviz.categorical.light")
CATEGORICAL_DARK = _group("color.dataviz.categorical.dark")
CATEGORICAL_NAMES = ["ATR Navy", "ATR Gold", "Sky", "Brick", "Teal", "Orange", "Plum", "Field Green"]
SEQ_NAVY = _group("color.dataviz.sequential.navy.light")
SEQ_GOLD = _group("color.dataviz.sequential.gold.light")
SEQ_NAVY_DARK = _group("color.dataviz.sequential.navy.dark")   # 900 -> 50: low values recede into the dark surface
SEQ_GOLD_DARK = _group("color.dataviz.sequential.gold.dark")
DIVERGING = _group("color.dataviz.diverging.navy-bronze.light")
DIVERGING_DARK = _group("color.dataviz.diverging.navy-bronze.dark")
STATUS = {r: token(f"color.status.{r}.fg") for r in ("success", "warning", "danger", "info")}
CHROME = {m: {k: token(f"color.dataviz.chrome.{m}.{k}") for k in ("surface", "grid", "axis", "tick", "label", "muted")}
          for m in ("light", "dark")}

# Milestone markers for quad-chart schedules: shape + color + label, never color alone.
MILESTONE = {
    "complete":    dict(marker="^", facecolor=token("color.milestone.complete.fill"), edgecolor=token("color.milestone.complete.stroke"), label="Complete"),
    "on-track":    dict(marker="o", facecolor=token("color.milestone.on-track.fill"), edgecolor=token("color.milestone.on-track.stroke"), label="On track"),
    "at-risk":     dict(marker="D", facecolor=token("color.milestone.at-risk.fill"), edgecolor=token("color.milestone.at-risk.stroke"), label="At risk"),
    "late":        dict(marker="s", facecolor=token("color.milestone.late.fill"), edgecolor=token("color.milestone.late.stroke"), label="Late"),
    "not-started": dict(marker="^", facecolor=token("color.milestone.not-started.fill"), edgecolor=token("color.milestone.not-started.stroke"), label="Not started"),
}


# --------------------------------------------------------------------------- fonts
_REGISTERED: list[str] | None = None


def register_fonts(font_dir: str | Path | None = None) -> list[str]:
    """Register the brand TTFs shipped in assets/fonts with matplotlib (no system install needed).

    Returns the family names now available. Safe to call repeatedly.
    """
    global _REGISTERED
    if _REGISTERED is not None and font_dir is None:
        return _REGISTERED
    d = Path(font_dir) if font_dir else FONT_DIR
    fams = set()
    for ttf in sorted(d.rglob("*.ttf")):
        font_manager.fontManager.addfont(str(ttf))
        fams.add(font_manager.FontProperties(fname=str(ttf)).get_name())
    if not fams:
        warnings.warn(f"No brand fonts found in {d}; falling back to Arial/DejaVu Sans.")
    _REGISTERED = sorted(fams)
    return _REGISTERED


# --------------------------------------------------------------------------- colormaps
def _srgb_to_lin(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _lin_to_srgb(c):
    c = min(1.0, max(0.0, c))
    return 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055


def _hex_to_oklab(h):
    h = h.lstrip("#")
    r, g, b = (_srgb_to_lin(int(h[i:i + 2], 16) / 255) for i in (0, 2, 4))
    l_ = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m_ = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s_ = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    l_, m_, s_ = (math.copysign(abs(v) ** (1 / 3), v) for v in (l_, m_, s_))
    return (0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_,
            1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_,
            0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_)


def _oklab_to_rgb(L, a, b):
    l_ = (L + 0.3963377774 * a + 0.2158037573 * b) ** 3
    m_ = (L - 0.1055613458 * a - 0.0638541728 * b) ** 3
    s_ = (L - 0.0894841775 * a - 1.2914855480 * b) ** 3
    r = 4.0767416621 * l_ - 3.3077115913 * m_ + 0.2309699292 * s_
    g = -1.2684380046 * l_ + 2.6097574011 * m_ - 0.3413193965 * s_
    bb = -0.0041960863 * l_ - 0.7034186147 * m_ + 1.7076147010 * s_
    return tuple(_lin_to_srgb(v) for v in (r, g, bb))


def oklab_cmap(name: str, stops: list[str], n: int = 256) -> ListedColormap:
    """Build a perceptually smooth colormap by interpolating the stops in OKLab."""
    labs = [_hex_to_oklab(h) for h in stops]
    out = []
    for i in range(n):
        t = i / (n - 1) * (len(labs) - 1)
        k = min(int(t), len(labs) - 2)
        f = t - k
        lab = tuple(labs[k][j] + (labs[k + 1][j] - labs[k][j]) * f for j in range(3))
        out.append(_oklab_to_rgb(*lab))
    return ListedColormap(out, name=name)


def register_colormaps() -> None:
    """Register the ATR colormaps with matplotlib, each with an _r (reversed) twin:

    atr_navy, atr_gold, atr_navy_bronze            light surfaces (low = light)
    atr_navy_dark, atr_gold_dark, atr_navy_bronze_dark   dark surfaces (low = dark, recedes into #0D1521)
    """
    maps = {
        "atr_navy": SEQ_NAVY,
        "atr_gold": SEQ_GOLD,
        "atr_navy_bronze": DIVERGING,
        "atr_navy_dark": SEQ_NAVY_DARK,
        "atr_gold_dark": SEQ_GOLD_DARK,
        "atr_navy_bronze_dark": DIVERGING_DARK,
    }
    for name, stops in maps.items():
        cm = oklab_cmap(name, stops)
        for c in (cm, cm.reversed(name + "_r")):
            if c.name not in mpl.colormaps:
                mpl.colormaps.register(c)


# --------------------------------------------------------------------------- style
_CONTEXT = {
    "paper":  {"font.size": 8, "axes.titlesize": 9, "axes.labelsize": 8, "xtick.labelsize": 8, "ytick.labelsize": 8,
               "legend.fontsize": 8, "figure.titlesize": 9, "lines.linewidth": 1.5, "lines.markersize": 4.5,
               "axes.linewidth": 0.6, "grid.linewidth": 0.6, "figure.figsize": (IEEE_SINGLE, 2.4)},
    # IEEE asks for "approximately 9-10 point" text at final size: the paper context raised to 9 pt
    "ieee":   {"font.size": 9, "axes.titlesize": 9, "axes.labelsize": 9, "xtick.labelsize": 9, "ytick.labelsize": 9,
               "legend.fontsize": 9, "figure.titlesize": 10, "lines.linewidth": 1.5, "lines.markersize": 4.5,
               "axes.linewidth": 0.6, "grid.linewidth": 0.6, "figure.figsize": (IEEE_SINGLE, 2.4)},
    "slide":  {"font.size": 16, "axes.titlesize": 20, "axes.labelsize": 16, "xtick.labelsize": 14, "ytick.labelsize": 14,
               "legend.fontsize": 14, "figure.titlesize": 22, "lines.linewidth": 3.0, "lines.markersize": 9,
               "axes.linewidth": 1.0, "grid.linewidth": 1.0, "xtick.major.size": 6, "xtick.major.width": 1.0,
               "figure.figsize": (9.2, 4.2), "axes.titlepad": 12},
    "poster": {"font.size": 28, "axes.titlesize": 36, "axes.labelsize": 28, "xtick.labelsize": 24, "ytick.labelsize": 24,
               "legend.fontsize": 24, "figure.titlesize": 40, "lines.linewidth": 5.0, "lines.markersize": 14,
               "axes.linewidth": 1.6, "grid.linewidth": 1.4, "xtick.major.size": 10, "xtick.major.width": 1.6,
               "figure.figsize": (14, 8), "axes.titlepad": 18},
}


def use(context: str = "paper", mode: str = "light", fonts: bool = True) -> None:
    """Apply the ATR style. context: paper | ieee | slide | poster. mode: light | dark."""
    if context not in _CONTEXT:
        raise ValueError(f"context must be one of {list(_CONTEXT)}")
    if mode not in ("light", "dark"):
        raise ValueError("mode must be 'light' or 'dark'")
    if fonts:
        register_fonts()
    register_colormaps()
    plt.style.use(str(STYLE_FILE))
    mpl.rcParams.update(_CONTEXT[context])
    mpl.rcParams["image.cmap"] = "atr_navy" if mode == "light" else "atr_navy_dark"
    if mode == "dark":
        ch = CHROME["dark"]
        mpl.rcParams.update({
            "figure.facecolor": ch["surface"], "axes.facecolor": ch["surface"], "savefig.facecolor": ch["surface"],
            "text.color": ch["label"], "axes.labelcolor": ch["label"], "axes.titlecolor": ch["label"],
            "axes.edgecolor": ch["axis"], "xtick.color": ch["axis"], "ytick.color": ch["axis"],
            "xtick.labelcolor": ch["tick"], "ytick.labelcolor": ch["tick"], "grid.color": ch["grid"],
            "patch.edgecolor": ch["surface"], "scatter.edgecolors": ch["surface"],
            "axes.prop_cycle": mpl.cycler(color=CATEGORICAL_DARK),
        })


def colors(n: int | None = None, mode: str = "light") -> list[str]:
    """The categorical palette in its fixed order (first n slots)."""
    pal = CATEGORICAL if mode == "light" else CATEGORICAL_DARK
    if n is not None and n > len(pal):
        raise ValueError(f"{n} series exceeds the 8 categorical slots: fold the tail into 'Other' or facet.")
    return pal[:n] if n else list(pal)


# --------------------------------------------------------------------------- figures & export
def figure(width="single", aspect: float = 0.68, height: float | None = None, **subplots_kw):
    """Create a figure at a publication width: 'single' (3.5 in), 'double' (7.16 in), 'ieeeconf' (3.4 in, ICRA/IROS),
    'ieeeconf-double' (7.0 in), 'slide', 'slide-half', 'poster', or a number (in)."""
    w = WIDTHS.get(width, width) if isinstance(width, str) else float(width)
    h = height if height is not None else round(w * aspect, 3)
    return plt.subplots(figsize=(w, h), **subplots_kw)


def save(fig, stem: str | Path, formats=("pdf", "svg", "png"), dpi: int | None = None, line_art: bool = False,
         close: bool = False, exact: bool = True) -> list[Path]:
    """Export a figure. PNG at 300 dpi (color/halftone) or 600 dpi (line_art=True), per IEEE graphics guidance.

    exact=True keeps the page size exactly the figure size (e.g. 3.5 in for an IEEE column; constrained layout
    keeps labels inside). exact=False trims to the drawn content (bbox_inches="tight").
    PDFs embed TrueType (Type 42) fonts, never Type 3; SVG text is converted to paths so it renders identically anywhere.
    """
    stem = Path(stem)
    stem.parent.mkdir(parents=True, exist_ok=True)
    dpi = dpi or (600 if line_art else 300)
    out = []
    for fmt in formats:
        p = stem.with_suffix("." + fmt)
        fig.savefig(p, dpi=dpi if fmt in ("png", "jpg", "tif", "tiff") else None,
                    bbox_inches=None if exact else "tight")
        out.append(p)
    if close:
        plt.close(fig)
    return out


# --------------------------------------------------------------------------- labeling helpers
def label_line_ends(ax, lines=None, fmt="{label}", dx_pt: float | None = None, markers: bool = True, min_gap_frac: float = 0.07):
    """Direct-label each line at its right end.

    Text uses the label (ink) color; identity comes from a colored end-dot with a surface-colored ring.
    Labels that would collide are spread apart and tied back to their line end with a thin leader.
    When a line carries its own marker (redundant_lines), the label also gets a key glyph in the line's color and
    shape, so each label can be matched to its line without following the leader.
    Up to 4 lines: optional (the legend suffices). 5-8 lines: required, together with redundant_lines()
    (call redundant_lines() first so the end-dots reuse each line's marker).
    Many converging series read better as small multiples.
    """
    lines = lines or [l for l in ax.get_lines() if not l.get_label().startswith("_")]
    if not lines:
        return []
    fig = ax.figure
    fig.canvas.draw()  # settle constrained layout so point offsets are right
    y0, y1 = ax.get_ylim()
    span = (y1 - y0) or 1.0
    h_pts = ax.get_window_extent().height * 72 / fig.dpi
    ends = sorted(([float(l.get_xdata()[-1]), float(l.get_ydata()[-1]), l] for l in lines), key=lambda e: e[1])
    ys = [e[1] for e in ends]
    gap = span * min_gap_frac
    for i in range(1, len(ys)):
        ys[i] = max(ys[i], ys[i - 1] + gap)
    overflow = ys[-1] - y1
    if overflow > 0:
        ys = [y - overflow for y in ys]
    txt = mpl.rcParams["axes.labelcolor"]
    surface = mpl.rcParams["axes.facecolor"]
    leader = mpl.rcParams["xtick.color"]
    dot = mpl.rcParams["lines.markersize"] * 1.15
    if dx_pt is None:
        dx_pt = (dot / 2 + 3) if markers else 4
    mew = max(0.8, mpl.rcParams["lines.markeredgewidth"] * 1.5)
    out = []
    for (x, y, l), ly in zip(ends, ys):
        own = l.get_marker() not in (None, "None", "none", "", " ")  # set by redundant_lines()
        mk = l.get_marker() if own else "o"
        if markers:
            ax.plot([x], [y], marker=mk, ms=dot, color=l.get_color(), mec=surface, mew=mew,
                    zorder=l.get_zorder() + 1, clip_on=False, label="_nolegend_")
        dy = (ly - y) / span * h_pts
        tx = dx_pt
        if markers and own:  # key glyph at the label: [leader] -> glyph -> text
            k = dot * 0.9
            ax.plot([x], [y], marker=mk, ms=k, color=l.get_color(), mec=surface, mew=mew * 0.8, clip_on=False,
                    label="_nolegend_", zorder=l.get_zorder() + 1,
                    transform=mtransforms.offset_copy(ax.transData, fig=fig, x=dx_pt + k / 2, y=dy, units="points"))
            if abs(dy) > 1.0:
                ax.annotate("", xy=(x, y), xytext=(dx_pt - 1, dy), textcoords="offset points", annotation_clip=False,
                            arrowprops=dict(arrowstyle="-", lw=0.5, color=leader, shrinkA=0, shrinkB=dot / 2 + 1))
            tx = dx_pt + k + 3
            arrow = None
        else:
            arrow = dict(arrowstyle="-", lw=0.5, color=leader, shrinkA=1, shrinkB=3) if abs(dy) > 1.0 else None
        out.append(ax.annotate(fmt.format(label=l.get_label(), y=y), xy=(x, y), xytext=(tx, dy),
                               textcoords="offset points", va="center", ha="left", color=txt,
                               fontsize=mpl.rcParams["legend.fontsize"], annotation_clip=False, arrowprops=arrow))
    return out


# Redundant encodings per categorical slot (index 0 = slot 1). Keyed to the slot, not the plotting order, so a
# series keeps its marker and dash when a filter removes others (identity follows the entity, like color).
# Slots 1-4 are separable by color alone (validated all-pairs) and stay solid; slots 5-8 carry a dash pattern too.
MARKERS = ["o", "s", "^", "D", "v", "P", "X", "h"]
DASHES = ["-", "-", "-", "-", (0, (5, 2)), (0, (1, 1.6)), (0, (6, 1.8, 1.2, 1.8)), (0, (8, 2, 1.2, 2, 1.2, 2))]


def _slot_of(color) -> int | None:
    """Categorical slot index (0-based) of a color in either mode, or None if it is not a palette color."""
    h = mpl.colors.to_hex(color).upper()
    for pal in (CATEGORICAL, CATEGORICAL_DARK):
        if h in pal:
            return pal.index(h)
    return None


def redundant_lines(ax, lines=None, markers: bool = True, dashes: bool = True, n_markers: int = 7):
    """Add per-slot markers and dash patterns so line identity never rests on color alone.

    Required for 5-8 line series (lines cross, so every pair can touch and hues 5+ are not pairwise-separable);
    use it together with label_line_ends(). Markers get a surface-colored ring and are thinned to about
    n_markers per line. The legend picks up the markers and dashes automatically.
    """
    lines = lines or [l for l in ax.get_lines() if not l.get_label().startswith("_")]
    surface = mpl.rcParams["axes.facecolor"]
    for i, l in enumerate(lines):
        slot = _slot_of(l.get_color())
        slot = i if slot is None else slot
        if dashes:
            l.set_linestyle(DASHES[slot % len(DASHES)])
        if markers:
            n = len(l.get_xdata())
            l.set_marker(MARKERS[slot % len(MARKERS)])
            l.set_markevery(max(1, round(n / n_markers)) if n > n_markers else None)
            l.set_markerfacecolor(l.get_color())
            l.set_markeredgecolor(surface)
            l.set_markeredgewidth(max(0.6, mpl.rcParams["lines.markeredgewidth"]))
            l.set_markersize(mpl.rcParams["lines.markersize"] * 1.1)
    return lines


def label_bars(ax, bars, fmt="{:,.0f}", inside: bool = False, pad_pt: float = 2):
    """Value labels at bar tips (or centered inside with inside=True). Text color, never the series color."""
    labels = [fmt.format(b.get_height()) for b in bars]
    color = mpl.rcParams["axes.labelcolor"]
    return ax.bar_label(bars, labels=labels, padding=0 if inside else pad_pt, color=color,
                        fontsize=mpl.rcParams["legend.fontsize"], label_type="center" if inside else "edge")


def legend_top(ax, ncols: int | None = None, **kw):
    """Legend above the plot (one row by default), left-aligned; pushes the (left) title up so they never collide.
    With ncols < series count, entries are reordered so each row reads left to right in slot order."""
    handles, labels = ax.get_legend_handles_labels()
    ncols = ncols or len(labels)
    n = len(labels)
    if 0 < ncols < n and n % ncols == 0:  # matplotlib fills columns first; reorder so rows read in slot order
        nrows = n // ncols
        order = [(i % nrows) * ncols + i // nrows for i in range(n)]
        handles, labels = [handles[k] for k in order], [labels[k] for k in order]
    leg = ax.legend(handles, labels, ncols=ncols, loc="lower left", bbox_to_anchor=(0, 1.0), borderaxespad=0.3,
                    frameon=False, **kw)
    fig = ax.figure
    fig.canvas.draw()
    h_pts = leg.get_window_extent().height * 72 / fig.dpi
    for loc in ("left", "center", "right"):
        t = ax.get_title(loc=loc)
        if t:
            ax.set_title(t, loc=loc, pad=h_pts + mpl.rcParams["axes.titlepad"])
    return leg


def milestone(ax, x, y, state: str, size: float | None = None, **kw):
    """Plot a quad-chart schedule milestone marker (shape + color by state)."""
    st = MILESTONE[state]
    ms = size or mpl.rcParams["lines.markersize"] * 1.6
    return ax.plot([x], [y], linestyle="none", marker=st["marker"], ms=ms, mfc=st["facecolor"], mec=st["edgecolor"],
                   mew=max(1.0, mpl.rcParams["lines.markeredgewidth"] * 1.4), label=st["label"], **kw)


def source_note(fig, text: str):
    """Small source/credit line under the figure, left aligned, in the muted text color."""
    return fig.text(0.0, -0.02, text, ha="left", va="top", fontsize=mpl.rcParams["font.size"] * 0.85,
                    color=mpl.rcParams["xtick.labelcolor"], transform=fig.transFigure)


__all__ = ["use", "figure", "save", "colors", "register_fonts", "register_colormaps", "oklab_cmap", "token",
           "label_line_ends", "redundant_lines", "label_bars", "legend_top", "milestone", "source_note",
           "NAVY", "GOLD", "INK", "SLATE", "BRONZE", "MIST",
           "CATEGORICAL", "CATEGORICAL_DARK", "CATEGORICAL_NAMES", "SEQ_NAVY", "SEQ_GOLD", "SEQ_NAVY_DARK", "SEQ_GOLD_DARK",
           "DIVERGING", "DIVERGING_DARK", "MARKERS", "DASHES", "STATUS", "MILESTONE", "CHROME", "IEEE_SINGLE", "IEEE_DOUBLE",
           "IEEECONF_SINGLE", "IEEECONF_DOUBLE", "WIDTHS"]
