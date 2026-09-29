#!/usr/bin/env python3
"""QA for the generated tokens: aliases resolve, brand hexes are exact, claimed contrasts hold.

    python atr-lab-design/assets/tokens/src/check_tokens.py      (exit 1 on any failure)
"""
import json, os, sys, re
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from colorlib import contrast  # noqa: E402

tok = json.load(open(os.path.join(OUT, "colors.json")))
fails = []


def get(path):
    node = tok
    for p in path.split("."):
        node = node[p]
    return node


def resolve(v, seen=()):
    if isinstance(v, str) and v.startswith("{"):
        path = v.strip("{}")
        if path in seen:
            raise ValueError("alias cycle " + path)
        return resolve(get(path)["$value"], seen + (path,))
    return v


def walk(node, path=""):
    if isinstance(node, dict):
        if "$value" in node:
            yield path, node
        for k, v in node.items():
            if not k.startswith("$"):
                yield from walk(v, f"{path}.{k}" if path else k)


n = 0
for path, t in walk(tok):
    n += 1
    try:
        h = resolve(t["$value"])
        if not re.fullmatch(r"#[0-9A-F]{6}", h):
            fails.append(f"{path}: bad hex {h}")
    except Exception as e:  # noqa: BLE001
        fails.append(f"{path}: {e}")

EXPECT = {"color.brand.navy": "#003976", "color.brand.gold": "#EFAB00", "color.ksu.midnight": "#00295F", "color.ksu.sky": "#2C8ECD",
          "color.ksu.flash": "#FFD702", "color.ksu.steel": "#96A0A5", "color.ksu.silver": "#B5B8B5", "color.functional.ink": "#1B2533",
          "color.functional.slate": "#4A5868", "color.functional.bronze": "#8A6100", "color.functional.mist": "#F3F6FA",
          "color.functional.line": "#D6DEE8", "color.functional.white": "#FFFFFF"}
for p, h in EXPECT.items():
    if resolve(get(p)["$value"]) != h:
        fails.append(f"{p} != {h}")

R = lambda p: resolve(get(p)["$value"])  # noqa: E731
checks = []
for mode in ("light", "dark"):
    sp = f"color.semantic.{mode}"
    page, panel = R(sp + ".bg.page"), R(sp + ".bg.panel")
    for t in ("primary", "secondary", "muted", "accent"):
        checks += [(f"{mode} text.{t} on page", R(f"{sp}.text.{t}"), page, 4.5), (f"{mode} text.{t} on panel", R(f"{sp}.text.{t}"), panel, 4.5)]
    checks += [(f"{mode} link on page", R(sp + ".link"), page, 4.5), (f"{mode} link.visited on page", R(sp + ".link.visited"), page, 4.5),
               (f"{mode} link.hover on page", R(sp + ".link.hover"), page, 4.5),
               (f"{mode} text.on-navy", R(sp + ".text.on-navy"), R(sp + ".bg.inverse"), 4.5),
               (f"{mode} text.on-navy-secondary", R(sp + ".text.on-navy-secondary"), R(sp + ".bg.inverse"), 4.5),
               (f"{mode} text.on-navy-accent", R(sp + ".text.on-navy-accent"), R(sp + ".bg.inverse"), 4.5),
               (f"{mode} link.on-navy", R(sp + ".link.on-navy"), R(sp + ".bg.inverse"), 4.5),
               (f"{mode} text.on-gold", R(sp + ".text.on-gold"), R(sp + ".bg.accent"), 4.5),
               (f"{mode} text.on-gold-strong", R(sp + ".text.on-gold-strong"), R(sp + ".bg.accent"), 4.5),
               (f"{mode} border.strong on page (non-text)", R(sp + ".border.strong"), page, 3.0),
               (f"{mode} focus.ring on page (non-text)", R(sp + ".focus.ring"), page, 3.0),
               (f"{mode} focus.ring on panel (non-text)", R(sp + ".focus.ring"), panel, 3.0),
               (f"{mode} focus.ring on navy (non-text)", R(sp + ".focus.ring"), R(sp + ".bg.inverse"), 3.0),
               (f"{mode} focus.ring-on-gold (non-text)", R(sp + ".focus.ring-on-gold"), R(sp + ".bg.accent"), 3.0)]
for role in ("success", "warning", "danger", "info"):
    s = f"color.status.{role}"
    checks += [(f"status.{role}.fg on white", R(s + ".fg"), "#FFFFFF", 4.5), (f"status.{role}.fg on mist", R(s + ".fg"), "#F3F6FA", 4.5),
               (f"status.{role}.fg on bg", R(s + ".fg"), R(s + ".bg"), 4.5), (f"status.{role}.on-solid", R(s + ".on-solid"), R(s + ".solid"), 4.5),
               (f"status.{role}.fg-dark on dark page", R(s + ".fg-dark"), R("color.semantic.dark.bg.page"), 4.5),
               (f"status.{role}.fg-dark on bg-dark", R(s + ".fg-dark"), R(s + ".bg-dark"), 4.5)]
for m in ("complete", "on-track", "at-risk", "late", "not-started"):
    checks.append((f"milestone.{m}.stroke on white (non-text)", R(f"color.milestone.{m}.stroke"), "#FFFFFF", 3.0))
for i in range(1, 9):
    if i != 2:
        checks.append((f"data light {i} on white (non-text)", R(f"color.dataviz.categorical.light.{i}"), "#FFFFFF", 3.0))
    checks.append((f"data dark {i} on dark page (non-text)", R(f"color.dataviz.categorical.dark.{i}"), R("color.dataviz.chrome.dark.surface"), 3.0))

for mode in ("light", "dark"):
    sp = f"color.semantic.{mode}"
    for t in ("primary", "secondary"):
        checks.append((f"{mode} text.{t} on subtle", R(f"{sp}.text.{t}"), R(sp + ".bg.subtle"), 4.5))

for name, fg, bg, need in checks:
    r = contrast(fg, bg)
    status = "PASS" if r >= need else "FAIL"
    if status == "FAIL":
        fails.append(f"{name}: {r:.2f} < {need}")
    print(f"[{status}] {name:48s} {fg} on {bg}  {r:5.2f} (need {need})")

# Documented exceptions: these must stay BELOW the bar, or the docs that forbid them are stale.
exceptions = [("light text.muted on subtle (documented: not allowed)", R("color.semantic.light.text.muted"), R("color.semantic.light.bg.subtle"), 4.5),
              ("dark text.muted on subtle (documented: not allowed)", R("color.semantic.dark.text.muted"), R("color.semantic.dark.bg.subtle"), 4.5),
              ("dark data 1 on dark panel (documented: charts not on panel)", R("color.dataviz.categorical.dark.1"), R("color.semantic.dark.bg.panel"), 3.0)]
for name, fg, bg, need in exceptions:
    r = contrast(fg, bg)
    if r >= need:
        fails.append(f"{name}: now {r:.2f} >= {need}; the docs that forbid it are stale")
    print(f"[NOTE] {name:48s} {fg} on {bg}  {r:5.2f} (< {need}, documented)")

# Structure: sequential ramps have the same stop count in both modes.
for r in ("navy", "gold"):
    nl = len([k for k in get(f"color.dataviz.sequential.{r}.light") if not k.startswith("$")])
    nd = len([k for k in get(f"color.dataviz.sequential.{r}.dark") if not k.startswith("$")])
    if nl != nd:
        fails.append(f"sequential.{r}: {nl} light stops vs {nd} dark stops")

# CSS: every data/chart variable in :root is overridden in BOTH dark blocks (a missing one keeps its light value).
css = open(os.path.join(OUT, "tokens.css"), encoding="utf-8").read()
root = css[css.index(":root {"):css.index("}", css.index(":root {"))]
media = re.search(r"@media \(prefers-color-scheme: dark\) \{\s*:root:not\(\[data-theme=\"light\"\]\) \{(.*?)\}\s*\}", css, re.S).group(1)
toggle = re.search(r":root\[data-theme=\"dark\"\] \{(.*?)\}", css, re.S).group(1)
data_vars = set(re.findall(r"(--atr-(?:data|seq|div|chart)-[\w-]+):", root))
for label, block in (("prefers-color-scheme dark", media), ("data-theme=dark", toggle)):
    missing = sorted(data_vars - set(re.findall(r"(--atr-[\w-]+):", block)))
    if missing:
        fails.append(f"tokens.css {label} block does not override: {', '.join(missing)}")
if not any("tokens.css" in f for f in fails):
    print(f"tokens.css: all {len(data_vars)} data/chart variables are overridden in both dark blocks")

# CSS base layer: brand fields must re-point the page colors that headings, small text, eyebrows and links set,
# or they compute to ink/slate on navy and navy-600/bronze on gold (all below AA).
layer = css[css.index("@layer atr.base {"):]
for sel, var in ((".atr-on-navy :is(h1, h2, h3, h4, h5, h6)", "--atr-text-on-navy"),
                 (".atr-on-navy :is(small, figcaption, .atr-small, .atr-lead)", "--atr-text-on-navy-secondary"),
                 (".atr-on-navy .atr-eyebrow", "--atr-text-on-navy-accent"),
                 (".atr-on-navy a, .atr-on-navy a:visited", "--atr-link-on-navy"),
                 (".atr-on-gold :is(h1, h2, h3, h4, h5, h6, small, figcaption, .atr-small, .atr-lead, .atr-eyebrow)", "--atr-text-on-gold"),
                 (".atr-on-gold a, .atr-on-gold a:visited", "--atr-text-on-gold-strong")):
    if not re.search(re.escape(sel) + r" \{ color: var\(" + re.escape(var) + r"\)", layer):
        fails.append(f"tokens.css @layer atr.base: missing override {sel} -> {var}")
if not any("@layer atr.base" in f for f in fails):
    print("tokens.css: on-navy / on-gold overrides present in @layer atr.base")

# Tailwind: every brand / KSU / functional name exists as atr-<name>.
tw = open(os.path.join(OUT, "tailwind.preset.js"), encoding="utf-8").read()
for grp in ("brand", "ksu", "functional"):
    for k in (k for k in get(f"color.{grp}") if not k.startswith("$")):
        if not re.search(rf'^\s+"{re.escape(k)}": ', tw, re.M):
            fails.append(f"tailwind.preset.js missing atr-{k}")

print(f"\n{n} tokens resolved; {len(checks)} contrast checks; {len(fails)} failures")
for f in fails:
    print("  FAIL", f)
sys.exit(1 if fails else 0)
