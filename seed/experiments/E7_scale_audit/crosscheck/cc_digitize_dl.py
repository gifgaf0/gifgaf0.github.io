#!/usr/bin/env python3
"""E7 cross-check: digitise Demidov-Levkov Fig. 3b (arXiv:1103.0013v2, two-particle exponent F at
g^2 N = 0) and Fig. 7b (arXiv:1103.2133v2, classical lower boundary g^2 N_min) from the PDFs.

Usage:  python3 cc_digitize_dl.py <dir containing 1103.0013v2.pdf and 1103.2133v2.pdf>
The PDFs are NOT in the repo (arXiv GCS mirror, kept in the scratchpad).  Pages are rendered with
pdftoppm; the red delta-rho = 0 curve is located by colour; axes are calibrated from the centres
of the tick-label glyphs (verified: the '1.2' label of Fig. 3b sits exactly on the panel-break
line, i.e. label centres mark the tick values).  Writes cc_dl_digitized.json.
"""
import json
import os
import subprocess
import sys
import tempfile
import numpy as np
from PIL import Image


def render(pdf, page, dpi, tmp):
    base = os.path.join(tmp, "p")
    subprocess.run(["pdftoppm", "-f", str(page), "-l", str(page), "-r", str(dpi), "-png", pdf, base], check=True)
    fn = [f for f in os.listdir(tmp) if f.startswith("p") and f.endswith(".png")][0]
    im = np.array(Image.open(os.path.join(tmp, fn)).convert("RGB")).astype(int)
    os.remove(os.path.join(tmp, fn))
    return im


def clusters(idx, gap):
    out = []
    s = p = idx[0]
    for c in idx[1:]:
        if c > p + gap:
            out.append((s, p)); s = c
        p = c
    out.append((s, p))
    return [(a + b) / 2 for a, b in out], out


def fig3b(pdf, tmp):
    im = render(pdf, 3, 600, tmp)
    x0, y0 = 1180 * 3, 135 * 3                    # Fig. 3b region on page 3 (600 dpi)
    sub = im[y0:y0 + 1400, x0:x0 + 1250]
    R, G, B = sub[..., 0], sub[..., 1], sub[..., 2]
    dark = (R < 100) & (G < 100) & (B < 100)
    red = (R > 180) & (G < 80) & (B < 80)
    # y labels of the upper panel: 4.4, 4.2, 4.0 (first three clusters in columns 100-200)
    rows = np.nonzero(dark[:440, 100:200].any(axis=1))[0]
    yc, _ = clusters(rows, 3)
    ylab = dict(zip([4.4, 4.2, 4.0], yc[:3]))
    py = np.polyfit([ylab[4.4], ylab[4.2], ylab[4.0]], [4.4, 4.2, 4.0], 1)
    # x labels: 7, 8, 9, 10, 11 in rows 1140-1200
    cols = np.nonzero(dark[1140:1200, 300:1200].any(axis=0))[0] + 300
    xc, raw = clusters(cols, 12)
    # merge two-digit labels ("10", "11") whose digits are separate clusters
    merged = []
    i = 0
    while i < len(raw):
        if i + 1 < len(raw) and raw[i + 1][0] - raw[i][1] < 30:
            merged.append((raw[i][0] + raw[i + 1][1]) / 2); i += 2
        else:
            merged.append((raw[i][0] + raw[i][1]) / 2); i += 1
    xvals = [7, 8, 9, 10, 11][:len(merged)]
    px = np.polyfit(merged[:len(xvals)], xvals, 1)
    xs = np.arange(0, sub.shape[1])
    curve = []
    for x in xs:
        yy = np.nonzero(red[:430, x])[0]
        if len(yy):
            curve.append((np.polyval(px, x), np.polyval(py, yy.mean())))
    curve = np.array(curve)
    g2E, F = curve[:, 0], curve[:, 1]
    res = dict(left_edge_g2E=float(g2E.min()), F_at_left_edge=float(F[np.argmin(g2E)]),
               F_min=float(F.min()), g2E_at_F_min=float(g2E[np.argmin(F)]),
               F_at_g2E_11p5=float(np.interp(11.5, g2E, F)), right_edge_g2E=float(g2E.max()),
               F_at_right_edge=float(F[np.argmax(g2E)]),
               axis_cal=dict(y_label_centres=ylab, x_label_centres=dict(zip(map(str, xvals), merged))),
               sample=[(float(a), float(b)) for a, b in curve[::60]])
    return res


def fig7b(pdf, tmp):
    im = render(pdf, 13, 600, tmp)
    # Fig. 7b region on page 13 at 600 dpi: approx x 2900..4200, y 950..2050 (from a 200-dpi preview)
    x0, y0 = 2700, 1350
    sub = im[y0:y0 + 1150, x0:x0 + 1500]
    R, G, B = sub[..., 0], sub[..., 1], sub[..., 2]
    dark = (R < 100) & (G < 100) & (B < 100)
    red = (R > 180) & (G < 80) & (B < 80)
    # axis box: longest dark vertical / horizontal lines
    colsum = dark.sum(axis=0); rowsum = dark.sum(axis=1)
    axl = int(np.argmax(colsum[:400]))
    axb = int(np.argmax(rowsum[500:])) + 500
    # y labels left of the axis: 4.4, 4.2, 4 (top to bottom)
    rows = np.nonzero(dark[:axb, max(axl - 160, 0):axl - 15].any(axis=1))[0]
    yc, _ = clusters(rows, 5)
    yvals = [4.4, 4.2, 4.0]
    py = np.polyfit(yc[-3:], yvals, 1)
    # x labels under the axis: 6 7 8 9 10
    cols = np.nonzero(dark[axb + 20:axb + 120, axl - 30:].any(axis=0))[0] + axl - 30
    _, raw = clusters(cols, 12)
    merged = []
    i = 0
    while i < len(raw):
        if i + 1 < len(raw) and raw[i + 1][0] - raw[i][1] < 30:
            merged.append((raw[i][0] + raw[i + 1][1]) / 2); i += 2
        else:
            merged.append((raw[i][0] + raw[i][1]) / 2); i += 1
    xvals = [6, 7, 8, 9, 10][:len(merged)]
    px = np.polyfit(merged[:len(xvals)], xvals, 1)
    curve = []
    for x in range(axl + 3, sub.shape[1]):
        yy = np.nonzero(red[:axb - 3, x])[0]
        if len(yy):
            _, cl = clusters(yy, 4)          # lowest red cluster = the curve (legend line lies above it)
            a, b = cl[-1]
            curve.append((np.polyval(px, x), np.polyval(py, 0.5 * (a + b))))
    curve = np.array(curve)
    g2E, g2N = curve[:, 0], curve[:, 1]
    hi = g2E > 9.0
    return dict(g2Nmin_high_energy_mean=float(g2N[hi].mean()), g2Nmin_high_energy_range=[float(g2N[hi].min()), float(g2N[hi].max())],
                g2N_at_left=float(g2N[np.argmin(g2E)]), g2E_left=float(g2E.min()),
                axis_cal=dict(y_label_centres=dict(zip(map(str, yvals), yc[-3:])), x_label_centres=dict(zip(map(str, xvals), merged))),
                sample=[(float(a), float(b)) for a, b in curve[::60]])


def main():
    d = sys.argv[1] if len(sys.argv) > 1 else "."
    out = {}
    with tempfile.TemporaryDirectory() as tmp:
        out["fig3b_1103.0013v2"] = fig3b(os.path.join(d, "1103.0013v2.pdf"), tmp)
        out["fig7b_1103.2133v2"] = fig7b(os.path.join(d, "1103.2133v2.pdf"), tmp)
    print(json.dumps({k: {kk: vv for kk, vv in v.items() if kk != "sample"} for k, v in out.items()}, indent=1))
    with open("cc_dl_digitized.json", "w") as f:
        json.dump(out, f, indent=1)


if __name__ == "__main__":
    main()
