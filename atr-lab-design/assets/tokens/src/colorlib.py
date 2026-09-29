"""Small, dependency-free color math used to build and verify the ATR Lab tokens.

sRGB <-> linear <-> OKLab/OKLCH (Bjorn Ottosson), WCAG 2.x contrast,
CVD simulation (Machado-Oliveira-Fernandes 2009, severity 1.0) and OKLab delta E x100,
matching the dataviz skill's validator so numbers agree.
"""
import math

def hex2rgb(h):
    h = h.strip().lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

def rgb2hex(rgb):
    return "#" + "".join(f"{max(0, min(255, int(round(c)))):02X}" for c in rgb)

def s2lin(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

def lin2s(c):
    c = max(0.0, min(1.0, c))
    return 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055

def lin(h):
    return [s2lin(c / 255) for c in hex2rgb(h)]

def rel_lum(h):
    r, g, b = lin(h)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def contrast(a, b):
    la, lb = sorted([rel_lum(a), rel_lum(b)], reverse=True)
    return (la + 0.05) / (lb + 0.05)

def lin2oklab(r, g, b):
    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    l, m, s = (math.copysign(abs(v) ** (1 / 3), v) for v in (l, m, s))
    return (0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s,
            1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s,
            0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s)

def oklab2lin(L, a, b):
    l = L + 0.3963377774 * a + 0.2158037573 * b
    m = L - 0.1055613458 * a - 0.0638541728 * b
    s = L - 0.0894841775 * a - 1.2914855480 * b
    l, m, s = l ** 3, m ** 3, s ** 3
    return (4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
            -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
            -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s)

def oklab(h):
    return lin2oklab(*lin(h))

def oklch(h):
    L, a, b = oklab(h)
    C = math.hypot(a, b)
    H = (math.degrees(math.atan2(b, a)) + 360) % 360
    return L, C, H

def in_gamut_lin(rgb, eps=1e-6):
    return all(-eps <= c <= 1 + eps for c in rgb)

def oklch2hex(L, C, H, fit=True):
    """OKLCH -> hex. With fit=True, chroma is reduced (hue and L held) until in sRGB gamut."""
    def conv(c):
        a, b = c * math.cos(math.radians(H)), c * math.sin(math.radians(H))
        return oklab2lin(L, a, b)
    rgb = conv(C)
    if fit and not in_gamut_lin(rgb):
        lo, hi = 0.0, C
        for _ in range(40):
            mid = (lo + hi) / 2
            if in_gamut_lin(conv(mid)):
                lo = mid
            else:
                hi = mid
        rgb = conv(lo)
    return rgb2hex([lin2s(c) * 255 for c in rgb])

def max_chroma(L, H):
    lo, hi = 0.0, 0.5
    for _ in range(40):
        mid = (lo + hi) / 2
        a, b = mid * math.cos(math.radians(H)), mid * math.sin(math.radians(H))
        if in_gamut_lin(oklab2lin(L, a, b)):
            lo = mid
        else:
            hi = mid
    return lo

MACHADO = {
    "protan": [[0.152286, 1.052583, -0.204868], [0.114503, 0.786281, 0.099216], [-0.003882, -0.048116, 1.051998]],
    "deutan": [[0.367322, 0.860646, -0.227968], [0.280085, 0.672501, 0.047413], [-0.011820, 0.042940, 0.968881]],
    "tritan": [[1.255528, -0.076749, -0.178779], [-0.078411, 0.930809, 0.147602], [0.004733, 0.691367, 0.303900]],
}

def simulate(h, kind):
    r, g, b = lin(h)
    M = MACHADO[kind]
    cl = lambda c: max(0.0, min(1.0, c))
    return [cl(M[i][0] * r + M[i][1] * g + M[i][2] * b) for i in range(3)]

def delta_e(h1, h2, kind=None):
    a = lin2oklab(*(simulate(h1, kind) if kind else lin(h1)))
    b = lin2oklab(*(simulate(h2, kind) if kind else lin(h2)))
    return 100 * math.dist(a, b)

def rgb_to_cmyk_naive(h):
    """Naive device-independent RGB->CMYK (for reference only; use the KSU-published CMYK for brand colors)."""
    r, g, b = (c / 255 for c in hex2rgb(h))
    k = 1 - max(r, g, b)
    if k >= 1:
        return (0, 0, 0, 100)
    c, m, y = ((1 - x - k) / (1 - k) for x in (r, g, b))
    return tuple(int(round(v * 100)) for v in (c, m, y, k))
