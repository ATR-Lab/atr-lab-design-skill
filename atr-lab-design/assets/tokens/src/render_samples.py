#!/usr/bin/env python3
"""Render QA sample charts with atr_plot (line, bar, heatmap, scatter, milestones; paper + slide + dark).

    python atr-lab-design/assets/tokens/src/render_samples.py [outdir]
Default outdir: build/qa/tokens/ at the repo root. Data are synthetic (seeded) placeholders, not lab results.
"""
import sys
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import atr_plot as atr  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402

OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE.parents[3] / "build" / "qa" / "tokens"
OUT.mkdir(parents=True, exist_ok=True)
rng = np.random.default_rng(7)


def line(ctx="paper", mode="light", name="sample_line"):
    atr.use(ctx, mode)
    fig, ax = atr.figure("single" if ctx == "paper" else "slide", aspect=0.62 if ctx == "paper" else 0.46)
    x = np.arange(0, 11)
    for i, (lab, k) in enumerate([("Proposed", 0.34), ("Baseline A", 0.24), ("Baseline B", 0.17)]):
        y = 100 * (1 - np.exp(-k * x)) + rng.normal(0, 1.2, x.size)
        ax.plot(x, y, label=lab)
    ax.set_xlabel("Training episodes (x1000)")
    ax.set_ylabel("Task success (%)")
    ax.set_title("Success rate by method")
    ax.set_ylim(0, 105)
    ax.set_xlim(0, 10)
    atr.label_line_ends(ax)
    return atr.save(fig, OUT / name, close=True)


def bar(ctx="paper", mode="light", name="sample_bar"):
    atr.use(ctx, mode)
    fig, ax = atr.figure("double" if ctx == "paper" else "slide", aspect=0.34 if ctx == "paper" else 0.46)
    cats = ["Grasp", "Place", "Navigate", "Inspect", "Handover"]
    series = ["Teleop", "Shared", "Autonomous", "Hybrid"]
    w = 0.8 / len(series)
    xs = np.arange(len(cats))
    for i, s in enumerate(series):
        vals = rng.uniform(40, 95, len(cats))
        b = ax.bar(xs + (i - (len(series) - 1) / 2) * w, vals, width=w * 0.92, label=s)
        if s == "Hybrid":
            atr.label_bars(ax, b, fmt="{:.0f}")
    ax.set_xticks(xs, cats)
    ax.set_ylabel("Completion (%)")
    ax.set_title("Task completion by control mode")
    ax.set_ylim(0, 105)
    ax.tick_params(axis="x", length=0)
    atr.legend_top(ax)
    return atr.save(fig, OUT / name, close=True)


def heatmap(name="sample_heatmap"):
    atr.use("paper")
    fig, axs = atr.figure("double", aspect=0.33, ncols=2)
    a = rng.gamma(2.0, 1.0, (8, 12))
    im = axs[0].imshow(a, cmap="atr_navy", aspect="auto")
    axs[0].set_title("Sequential (atr_navy): latency (ms)")
    fig.colorbar(im, ax=axs[0], shrink=0.9)
    d = np.clip(rng.normal(0, 1, (8, 12)).cumsum(axis=1) / 3, -2.5, 2.5)
    im2 = axs[1].imshow(d, cmap="atr_navy_bronze", vmin=-2.5, vmax=2.5, aspect="auto")
    axs[1].set_title("Diverging (atr_navy_bronze): delta vs. baseline")
    fig.colorbar(im2, ax=axs[1], shrink=0.9)
    for ax in axs:
        ax.grid(False)
        ax.set_xlabel("Trial")
        ax.set_ylabel("Operator")
        for s in ax.spines.values():
            s.set_visible(False)
    return atr.save(fig, OUT / name, close=True)


def scatter(name="sample_scatter"):
    atr.use("paper")
    fig, ax = atr.figure("single", aspect=0.8)
    for i, lab in enumerate(["Novice", "Intermediate", "Expert"]):
        n = 40
        x = rng.normal(2 + i * 1.3, 0.6, n)
        y = 60 - i * 12 + rng.normal(0, 6, n)
        ax.scatter(x, y, s=18, label=lab, linewidths=0.6, alpha=0.95, zorder=3)
    ax.set_xlabel("Hours of practice")
    ax.set_ylabel("Completion time (s)")
    ax.set_title("Operator skill vs. time")
    ax.grid(axis="both")
    ax.legend(loc="upper right", markerscale=1.2)
    return atr.save(fig, OUT / name, close=True)


def line_many(ctx="paper", mode="light", name="sample_line_many"):
    """8 line series: the 5-8 rule in action (redundant_lines + label_line_ends)."""
    atr.use(ctx, mode)
    fig, ax = atr.figure("double" if ctx == "paper" else "slide", aspect=0.42 if ctx == "paper" else 0.5)
    x = np.arange(0, 21)
    names = ["Teleop", "Shared", "Autonomous", "Hybrid", "VR teleop", "Haptic", "Gesture", "Voice"]
    for i, lab in enumerate(names):
        y = 20 + 70 * (1 - np.exp(-(0.08 + 0.025 * i) * x)) + rng.normal(0, 1.0, x.size) - i * 2.5
        ax.plot(x, y, label=lab)
    atr.redundant_lines(ax)
    atr.label_line_ends(ax, min_gap_frac=0.065)
    ax.set_xlabel("Session")
    ax.set_ylabel("Task success (%)")
    ax.set_title("8 series: markers + dashes + end labels (placeholder data)")
    ax.set_ylim(0, 100)
    ax.set_xlim(0, 20)
    return atr.save(fig, OUT / name, formats=("png",), close=True)


def stacked8(ctx="slide", mode="dark", name="sample_stacked8_slide_dark"):
    """All 8 slots touching in fixed order (stacked bars: the adjacent-pairs form)."""
    atr.use(ctx, mode)
    fig, ax = atr.figure("slide", aspect=0.46)
    cats = ["Q1", "Q2", "Q3", "Q4", "Q5"]
    bottom = np.zeros(len(cats))
    names = ["Teleop", "Shared", "Autonomous", "Hybrid", "VR teleop", "Haptic", "Gesture", "Voice"]
    for i, lab in enumerate(names):
        v = rng.uniform(4, 14, len(cats))
        ax.bar(cats, v, bottom=bottom, width=0.6, label=lab, linewidth=1.5, edgecolor=mpl_surface())
        bottom += v
    ax.set_ylabel("Hours (placeholder)")
    ax.set_title("Stacked bars use all 8 slots in order")
    ax.tick_params(axis="x", length=0)
    atr.legend_top(ax, ncols=4)
    return atr.save(fig, OUT / name, formats=("png",), close=True)


def mpl_surface():
    import matplotlib as mpl
    return mpl.rcParams["axes.facecolor"]


def heatmap_dark(name="sample_heatmap_slide_dark"):
    atr.use("slide", "dark")
    fig, axs = atr.figure("slide", aspect=0.42, ncols=2)
    a = rng.gamma(2.0, 1.0, (8, 12))
    im = axs[0].imshow(a, aspect="auto")  # default dark cmap = atr_navy_dark
    axs[0].set_title("atr_navy_dark (default)")
    fig.colorbar(im, ax=axs[0], shrink=0.9)
    d = np.clip(rng.normal(0, 1, (8, 12)).cumsum(axis=1) / 3, -2.5, 2.5)
    im2 = axs[1].imshow(d, cmap="atr_navy_bronze_dark", vmin=-2.5, vmax=2.5, aspect="auto")
    axs[1].set_title("atr_navy_bronze_dark")
    fig.colorbar(im2, ax=axs[1], shrink=0.9)
    for ax in axs:
        ax.grid(False)
        ax.set_xticks([])
        ax.set_yticks([])
        for sp in ax.spines.values():
            sp.set_visible(False)
    return atr.save(fig, OUT / name, formats=("png",), close=True)


def milestones(name="sample_milestones"):
    atr.use("slide")
    fig, ax = atr.figure("slide", aspect=0.3)
    states = ["complete", "complete", "on-track", "at-risk", "late", "not-started"]
    names = ["Design review", "Prototype", "Integration", "Field test", "User study", "Final report"]
    for i, (st, nm) in enumerate(zip(states, names)):
        atr.milestone(ax, i, 0, st, size=18)
        ax.annotate(f"{nm}\n{atr.MILESTONE[st]['label']}", (i, 0), xytext=(0, -22), textcoords="offset points",
                    ha="center", va="top", fontsize=14)
    ax.axhline(0, color=atr.CHROME["light"]["axis"], lw=1.2, zorder=0)
    ax.set_xlim(-0.6, len(states) - 0.4)
    ax.set_ylim(-1, 0.5)
    ax.axis("off")
    ax.set_title("Milestone states (shape + label + color)", loc="left")
    return atr.save(fig, OUT / name, formats=("png",), close=True)


if __name__ == "__main__":
    outs = []
    outs += line()
    outs += bar()
    outs += heatmap()
    outs += scatter()
    outs += line("slide", "light", "sample_line_slide")
    outs += line("slide", "dark", "sample_line_slide_dark")
    outs += bar("slide", "dark", "sample_bar_slide_dark")
    outs += milestones()
    outs += line_many()
    outs += line_many("slide", "dark", "sample_line_many_slide_dark")
    outs += stacked8()
    outs += heatmap_dark()
    for p in outs:
        print(p)
