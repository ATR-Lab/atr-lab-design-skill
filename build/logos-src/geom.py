"""Vector helpers for the traced curves (see trace.py for the curve format)."""
import copy

import numpy as np


def xform(curves, s=1.0, tx=0.0, ty=0.0):
    out = copy.deepcopy(curves)
    for c in out:
        c["start"] = [c["start"][0] * s + tx, c["start"][1] * s + ty]
        for seg in c["segs"]:
            for i in range(1, len(seg), 2):
                seg[i] = seg[i] * s + tx
                seg[i + 1] = seg[i + 1] * s + ty
    return out


def sample_points(curves, n=24):
    pts = []
    for c in curves:
        p0 = np.array(c["start"])
        for seg in c["segs"]:
            if seg[0] == "P":
                b = np.array(seg[1:3])
                pts += [p0, b]
                p0 = b
            elif seg[0] == "L":
                a = np.array(seg[1:3]); b = np.array(seg[3:5])
                pts += [p0, a, b]
                p0 = b
            else:
                c1 = np.array(seg[1:3]); c2 = np.array(seg[3:5]); p3 = np.array(seg[5:7])
                t = np.linspace(0, 1, n)[:, None]
                pts += list((1 - t) ** 3 * p0 + 3 * (1 - t) ** 2 * t * c1 + 3 * (1 - t) * t ** 2 * c2 + t ** 3 * p3)
                p0 = p3
    return np.array(pts)


def bbox(curves):
    p = sample_points(curves)
    return float(p[:, 0].min()), float(p[:, 1].min()), float(p[:, 0].max()), float(p[:, 1].max())


def curve_bbox(c):
    return bbox([c])


def to_d(curves, prec=2, rel=False):
    """Path data. Absolute (M/L/C) by default. rel=True writes compact relative commands
    (l/c, implicit repetition). Coordinates are first rounded to the grid 10^-prec in ABSOLUTE
    space and the deltas are taken between rounded points (integer arithmetic), so relative
    output has no accumulated drift: it renders identically to the absolute form."""
    f = "%." + str(prec) + "f"

    def n(v):
        s = f % v
        s = s.rstrip("0").rstrip(".") if "." in s else s
        return "0" if s in ("-0", "") else s

    if not rel:
        parts = []
        for c in curves:
            parts.append("M%s %s" % (n(c["start"][0]), n(c["start"][1])))
            for seg in c["segs"]:
                if seg[0] == "P":
                    parts.append("L%s %s" % tuple(n(v) for v in seg[1:3]))
                elif seg[0] == "L":
                    parts.append("L%s %s %s %s" % tuple(n(v) for v in seg[1:5]))
                else:
                    parts.append("C%s %s %s %s %s %s" % tuple(n(v) for v in seg[1:7]))
            parts.append("Z")
        return "".join(parts)

    K = 10 ** prec

    def q(v):
        return int(round(v * K))

    def num(i):
        s = str(abs(i) // K) + (("." + ("%0" + str(prec) + "d") % (abs(i) % K)).rstrip("0") if abs(i) % K else "")
        return ("-" + s) if i < 0 else s

    def nums(vals):
        out = ""
        for i, v in enumerate(vals):
            s = num(v)
            out += s if (i == 0 or s.startswith("-")) else " " + s
        return out

    parts = []
    for c in curves:
        cx, cy = q(c["start"][0]), q(c["start"][1])
        sx, sy = cx, cy
        parts.append("M" + nums([cx, cy]))
        last = None
        for seg in c["segs"]:
            pts = [(q(seg[i]), q(seg[i + 1])) for i in range(1, len(seg), 2)]
            if seg[0] == "C":
                (x1, y1), (x2, y2), (x, y) = pts
                if last == "c":
                    parts.append((" " if not num(x1 - cx).startswith("-") else "") + nums([x1 - cx, y1 - cy, x2 - cx, y2 - cy, x - cx, y - cy]))
                else:
                    parts.append("c" + nums([x1 - cx, y1 - cy, x2 - cx, y2 - cy, x - cx, y - cy]))
                last = "c"; cx, cy = x, y
            else:
                for (x, y) in pts:
                    if (x, y) == (cx, cy):
                        continue
                    if last == "l":
                        parts.append((" " if not num(x - cx).startswith("-") else "") + nums([x - cx, y - cy]))
                    else:
                        parts.append("l" + nums([x - cx, y - cy]))
                    last = "l"; cx, cy = x, y
        parts.append("z")
    return "".join(parts)


def svg_doc(w, h, layers, title, desc=None, prec=2, uid=None, rel=False):
    """layers: list of (hex_color, curves). One <path> per colour layer, even-odd fill
    (potrace output never overlaps itself, so even-odd renders holes correctly).
    uid: unique id stem (e.g. the file name) so several logos can be inlined on one HTML
    page without duplicate ids; the accessible name comes from <title> via aria-labelledby."""
    f = "%." + str(prec) + "f"
    body = []
    for color, curves in layers:
        if not curves:
            continue
        body.append('<path fill="%s" fill-rule="evenodd" d="%s"/>' % (color, to_d(curves, prec, rel=rel)))
    W = (f % w).rstrip("0").rstrip("."); H = (f % h).rstrip("0").rstrip(".")
    tid = "%s-title" % (uid or "atr-logo")
    d = "<desc>%s</desc>" % desc if desc else ""
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %s %s" width="%s" height="%s" role="img" '
            'aria-labelledby="%s"><title id="%s">%s</title>%s%s</svg>\n' % (W, H, W, H, tid, tid, title, d, "".join(body)))


# ------------------------------------------------------------------ polygon simplification
def _dp(pts, tol):
    """Douglas-Peucker on an open polyline (N x 2). Returns kept indices (sorted)."""
    keep = np.zeros(len(pts), bool)
    keep[0] = keep[-1] = True
    stack = [(0, len(pts) - 1)]
    while stack:
        i, j = stack.pop()
        if j <= i + 1:
            continue
        a, b = pts[i], pts[j]
        ab = b - a
        L = np.hypot(*ab)
        seg = pts[i + 1:j]
        if L < 1e-12:
            d = np.hypot(*(seg - a).T)
        else:
            d = np.abs(ab[0] * (seg[:, 1] - a[1]) - ab[1] * (seg[:, 0] - a[0])) / L
        k = int(d.argmax())
        if d[k] > tol:
            m = i + 1 + k
            keep[m] = True
            stack += [(i, m), (m, j)]
    return np.where(keep)[0]


def simplify_polygon(curves, tol, n=16):
    """Straight-edged art only (the ATR mark is pure straight-line geometry): sample every
    traced curve densely and replace it by its Douglas-Peucker polygon (tolerance `tol` in the
    curves' own units). Removes the Bezier 'staircase' wobble potrace leaves on long straight
    edges; every output segment is a straight line (SVG L)."""
    out = []
    for c in curves:
        p = sample_points([c], n)
        # drop consecutive duplicates
        keep = np.r_[True, np.hypot(*np.diff(p, axis=0).T) > 1e-9]
        p = p[keep]
        if np.hypot(*(p[0] - p[-1])) < 1e-9:
            p = p[:-1]
        # split the closed ring at the two mutually farthest points, simplify both halves
        i0 = 0
        i1 = int(np.hypot(*(p - p[i0]).T).argmax())
        i0 = int(np.hypot(*(p - p[i1]).T).argmax())
        p = np.roll(p, -i0, axis=0)
        i1 = (i1 - i0) % len(p)
        ring = np.vstack([p, p[:1]])
        k1 = _dp(ring[:i1 + 1], tol)
        k2 = _dp(ring[i1:], tol) + i1
        idx = list(k1) + list(k2[1:-1])
        q = ring[idx]
        segs = []
        for j in range(1, len(q)):
            segs.append(["P", float(q[j][0]), float(q[j][1])])
        segs.append(["P", float(q[0][0]), float(q[0][1])])
        out.append({"start": [float(q[0][0]), float(q[0][1])], "segs": segs})
    return out


def _densify(c, step=0.25):
    """Points every `step` units along a traced curve (polylines exact, Beziers sampled)."""
    p = sample_points([c], 24)
    keep = np.r_[True, np.hypot(*np.diff(p, axis=0).T) > 1e-9]
    p = p[keep]
    if np.hypot(*(p[0] - p[-1])) < 1e-9:
        p = p[:-1]
    ring = np.vstack([p, p[:1]])
    out = []
    for a, b in zip(ring[:-1], ring[1:]):
        n = max(1, int(np.ceil(np.hypot(*(b - a)) / step)))
        t = np.arange(n)[:, None] / n
        out.append(a + t * (b - a))
    return np.vstack(out)


def _fit_line(pts):
    """Total-least-squares line through pts: (point on line, unit direction)."""
    m = pts.mean(0)
    u, s, vt = np.linalg.svd(pts - m, full_matrices=False)
    return m, vt[0]


def _intersect(p1, d1, p2, d2):
    A = np.array([d1, -d2]).T
    if abs(np.linalg.det(A)) < 1e-9:
        return None
    t = np.linalg.solve(A, p2 - p1)
    return p1 + t[0] * d1


def fit_polygon(curves, corner_tol=0.75, trim=1.5, min_fit=4.0, merge_deg=1.0, max_shift=2.0):
    """Straight-edged art only (the ATR mark: straight strokes, 45/60 degree angles, no
    curves). Re-fits each traced outline as a true polygon:
      1. Douglas-Peucker (tolerance `corner_tol`) finds the corners of the traced outline;
      2. every edge between two corners is replaced by the total-least-squares line through
         the traced points on it (points within `trim` of either corner are ignored, so the
         anti-aliasing round-off at corners does not bias the edge);
      3. neighbouring edges that are within `merge_deg` degrees of each other are one edge;
      4. vertices = intersections of neighbouring fitted edges (sharp corners). If an
         intersection moves more than `max_shift` from the traced corner (very acute tip),
         the traced corner is kept instead.
    Output segments are straight lines only. All units = the curves' own (source px)."""
    out = []
    for c in curves:
        P = _densify(c)
        n = len(P)
        # corners by DP on the closed ring (split at two mutually far points)
        i1 = int(np.hypot(*(P - P[0]).T).argmax())
        i0 = int(np.hypot(*(P - P[i1]).T).argmax())
        P = np.roll(P, -i0, axis=0)
        i1 = (i1 - i0) % n
        ring = np.vstack([P, P[:1]])
        k = sorted(set(list(_dp(ring[:i1 + 1], corner_tol)) + list(_dp(ring[i1:], corner_tol) + i1)))
        k = [i % n for i in k]
        k = sorted(set(k))
        # edges between consecutive corners
        edges = []
        for a, b in zip(k, k[1:] + [k[0] + n]):
            idx = np.arange(a, b + 1) % n
            pts = P[idx]
            L = np.hypot(*(pts[-1] - pts[0]))
            if L >= min_fit + 2 * trim:
                d0 = np.hypot(*(pts - pts[0]).T); d1 = np.hypot(*(pts - pts[-1]).T)
                sel = pts[(d0 > trim) & (d1 > trim)]
                if len(sel) >= 3:
                    edges.append({"a": a, "b": b, "pts": pts, "line": _fit_line(sel), "fit": True})
                    continue
            m = (pts[0] + pts[-1]) / 2
            d = pts[-1] - pts[0]
            d = d / (np.hypot(*d) or 1)
            edges.append({"a": a, "b": b, "pts": pts, "line": (m, d), "fit": False})
        # merge nearly-collinear neighbours (refit on the union)
        changed = True
        while changed and len(edges) > 3:
            changed = False
            for i in range(len(edges)):
                e, f = edges[i], edges[(i + 1) % len(edges)]
                ang = np.degrees(np.arccos(min(1.0, abs(float(np.dot(e["line"][1], f["line"][1]))))))
                if ang < merge_deg and (e["fit"] or f["fit"]):
                    pts = np.vstack([e["pts"], f["pts"][1:]])
                    d0 = np.hypot(*(pts - pts[0]).T); d1 = np.hypot(*(pts - pts[-1]).T)
                    sel = pts[(d0 > trim) & (d1 > trim)]
                    ne = {"a": e["a"], "b": f["b"], "pts": pts, "line": _fit_line(sel if len(sel) >= 3 else pts), "fit": True}
                    j = (i + 1) % len(edges)
                    if j == 0:
                        edges = [ne] + edges[1:i]
                    else:
                        edges = edges[:i] + [ne] + edges[j + 1:]
                    changed = True
                    break
        # vertices
        V = []
        for i in range(len(edges)):
            e, f = edges[i - 1], edges[i]
            corner = e["pts"][-1]
            x = _intersect(e["line"][0], e["line"][1], f["line"][0], f["line"][1])
            if x is None or np.hypot(*(x - corner)) > max_shift:
                V.append(corner)
            else:
                V.append(x)
        V = np.array(V)
        segs = [["P", float(v[0]), float(v[1])] for v in V[1:]] + [["P", float(V[0][0]), float(V[0][1])]]
        out.append({"start": [float(V[0][0]), float(V[0][1])], "segs": segs})
    return out
