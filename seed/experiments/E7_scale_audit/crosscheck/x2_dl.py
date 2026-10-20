#!/usr/bin/env python3
"""E7 second cross-check (x2): Demidov-Levkov (DL) model numbers and my own pixel reading of
their figures.

1. Model (arXiv:1103.0013 Eq. (9), read):  S = (1/g^2) int [ (d phi)^2/2 - V ],
   V = (1/2)(phi+1)^2 [1 - v W((phi-1)/a)],  W(x) = e^{-x^2}(x + x^3 + x^5),  a = 0.4.
   At delta rho = 0 the second minimum is degenerate (V = 0): v = 1/max_{x>0} W(x).
   m_-^2 = V''(-1) = 1.  Soliton: g^2 M_S = int sqrt(2V) dphi between the two vacua.
2. Figures: if the arXiv PDFs are in LITDIR, page 3 of 1103.0013v2 (Fig. 3b) and page 13 of
   1103.2133v2 (Fig. 7b) are rendered at 600 dpi with pdftoppm; the axes are calibrated on the
   tick MARKS found on the frame (not on the label text) and the solid red delta rho = 0 curve is
   traced column by column.  Without the PDFs the pixel readings recorded below (from the same
   procedure, 2026-10-19) are used.
Writes x2_dl.json.
"""
import json
import os
import subprocess
import sys
import tempfile
import numpy as np
from scipy.integrate import quad
from scipy.optimize import minimize_scalar, brentq

LITDIR = sys.argv[1] if len(sys.argv) > 1 else os.environ.get(
    "LITDIR", "/tmp/claude-0/-home-user-gifgaf0-github-io/235fe351-6f97-5895-b3fd-a90496179b3c/scratchpad/e7xc2/lit")
A = 0.4


def W(x):
    return np.exp(-x * x) * (x + x ** 3 + x ** 5)


def model():
    r = minimize_scalar(lambda x: -W(x), bounds=(0.1, 3.0), method="bounded",
                        options={"xatol": 1e-14})
    xs = r.x
    v = 1.0 / W(xs)
    phip = 1 + A * xs
    V = lambda p: 0.5 * (p + 1) ** 2 * (1 - v * W((p - 1) / A))
    # m_-^2 by finite differences
    h = 1e-4
    m2 = (V(-1 + h) - 2 * V(-1) + V(-1 - h)) / h ** 2
    m2p = (V(phip + h) - 2 * V(phip) + V(phip - h)) / h ** 2
    I, err = quad(lambda p: np.sqrt(max(2 * V(p), 0.0)), -1, phip, limit=400, epsabs=1e-13, epsrel=1e-13)
    # check: V >= 0 on [-1, phi+] and the minimum at phi+ is zero
    grid = np.linspace(-1, phip, 20001)
    return dict(v=v, x_star=xs, phi_plus=phip, m_minus_sq=m2, m_plus_sq=m2p,
                g2MS=I, two_g2MS=2 * I, quad_err=err, Vmin_on_interval=float(min(V(grid))))


def render(pdf, page, crop):
    from PIL import Image
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(["pdftoppm", "-f", str(page), "-l", str(page), "-r", "600", "-png", pdf,
                        os.path.join(tmp, "p")], check=True)
        fn = [f for f in os.listdir(tmp) if f.endswith(".png")][0]
        im = Image.open(os.path.join(tmp, fn)).convert("RGB").crop(crop)
        return np.array(im).astype(int)


def ticks_left(dark, spine, r0, r1):
    rows = np.where(dark[r0:r1, spine + 4])[0] + r0
    groups = np.split(rows, np.where(np.diff(rows) > 1)[0] + 1)
    return [float(np.mean(g)) for g in groups if g.size]


def ticks_bottom(dark, axis_row, c0, c1):
    cols = np.where(dark[axis_row - 6, c0:c1])[0] + c0
    groups = np.split(cols, np.where(np.diff(cols) > 1)[0] + 1)
    return [float(np.mean(g)) for g in groups if g.size]


def red_trace(im, r0, r1, cols):
    R, G, B = im[..., 0], im[..., 1], im[..., 2]
    red = (R > 150) & (G < 120) & (B < 120)
    out = []
    for c in cols:
        rr = np.where(red[r0:r1, c])[0] + r0
        if rr.size and rr.max() - rr.min() < 20:
            out.append((c, float(rr.mean())))
    return out


def digitise_fig3b(pdf):
    # page 3, panel (b): upper panel (F at g^2 N = 0) and bottom axis
    im = render(pdf, 3, (3550, 400, 4750, 1700))
    dark = (im[..., 0] < 100) & (im[..., 1] < 100) & (im[..., 2] < 100)
    cols = dark[0:450].sum(0)
    spine = int(np.argmax(cols[150:300])) + 150
    yt = ticks_left(dark, spine, 40, 440)          # rows of 4.4, 4.2, 4.0 (top to bottom)
    yt = [y for y in yt if y > 40][:3]
    rows = dark.sum(1)
    axis_row = int(np.argmax(rows[1050:1300])) + 1050
    xt = ticks_bottom(dark, axis_row, spine + 20, 1130)   # 7, 8, 9, 10, 11
    py = (yt[2] - yt[0]) / 0.4                     # px per unit F
    px = (xt[-1] - xt[0]) / (len(xt) - 1)          # px per unit g^2 E
    Fval = lambda row: 4.0 + (yt[2] - row) / py
    Eval = lambda col: 7.0 + (col - xt[0]) / px
    tr = red_trace(im, 34, 440, range(spine + 3, 1131))
    E = np.array([Eval(c) for c, _ in tr]); F = np.array([Fval(r) for _, r in tr])
    out = dict(tick_rows_4p4_4p2_4p0=yt, tick_cols_7_to_11=xt, spine_col=spine,
               left_edge_g2E=Eval(spine + 0.5), right_edge_g2E=Eval(1133),
               F_left=float(F[0]), E_left=float(E[0]))
    for e in (7.0, 8.0, 9.0, 10.0, 11.0, 11.5):
        out[f"F_at_{e}"] = float(np.interp(e, E, F))
    pl = (E > 10.5)
    out["F_plateau_mean_E_gt_10p5"] = float(F[pl].mean())
    out["F_plateau_min"] = float(F.min())
    return out


def digitise_fig7b(pdf):
    im = render(pdf, 13, (2700, 1400, 4300, 2450))
    dark = (im[..., 0] < 90) & (im[..., 1] < 90) & (im[..., 2] < 90)
    cols = dark.sum(0)
    spine = int(np.argmax(cols[200:400])) + 200
    yt = ticks_left(dark, spine + 1, 112, 870)     # 4.4, 4.2, 4.0
    rows = dark.sum(1)
    axis_row = int(np.argmax(rows[800:950])) + 800
    xt = ticks_bottom(dark, axis_row, spine + 20, 1425)    # 7, 8, 9, 10
    py = (yt[2] - yt[0]) / 0.4
    px = (xt[-1] - xt[0]) / (len(xt) - 1)
    Nval = lambda row: 4.0 + (yt[2] - row) / py
    Eval = lambda col: 7.0 + (col - xt[0]) / px
    # the legend's red sample line sits around row ~505 between cols ~650 and ~900: skip rows < 700
    # for columns in that range
    tr = []
    for c, r in red_trace(im, 112, 870, range(spine + 3, 1428)):
        tr.append((c, r))
    R, G, B = im[..., 0], im[..., 1], im[..., 2]
    red = (R > 150) & (G < 120) & (B < 120)
    tr = []
    for c in range(spine + 3, 1428):
        rr = np.where(red[112:870, c])[0] + 112
        if 640 <= c <= 900:
            rr = rr[rr > 700]
        if rr.size and rr.max() - rr.min() < 20:
            tr.append((c, float(rr.mean())))
    E = np.array([Eval(c) for c, _ in tr]); N = np.array([Nval(r) for _, r in tr])
    out = dict(tick_rows_4p4_4p2_4p0=yt, tick_cols_7_to_10=xt, spine_col=spine,
               left_edge_g2E=Eval(spine + 0.5))
    for e in (6.4, 6.6, 7.0, 8.0, 9.0, 10.0, 10.4):
        out[f"g2Nmin_at_{e}"] = float(np.interp(e, E, N))
    out["g2Nmin_plateau_mean_E_gt_8p5"] = float(N[E > 8.5].mean())
    return out


# readings recorded by this script on 2026-10-19 (used only if the PDFs are absent)
RECORDED = {
    "fig3b": {"F_plateau_mean_E_gt_10p5": 3.844, "F_at_11.5": 3.845, "F_left": 4.48, "left_edge_g2E": 6.234},
    "fig7b": {"g2Nmin_plateau_mean_E_gt_8p5": 3.978},
}


def main():
    res = {"model": model()}
    m = res["model"]
    print(f"DL model: v = {m['v']:.9f}, phi+ = {m['phi_plus']:.9f}, m_-^2 = {m['m_minus_sq']:.6f}, "
          f"m_+^2 = {m['m_plus_sq']:.6f}, 2 g^2 M_S = {m['two_g2MS']:.9f}, min V = {m['Vmin_on_interval']:.2e}")
    p3 = os.path.join(LITDIR, "1103.0013v2.pdf")
    p7 = os.path.join(LITDIR, "1103.2133v2.pdf")
    if os.path.exists(p3) and os.path.exists(p7):
        res["fig3b"] = digitise_fig3b(p3)
        res["fig7b"] = digitise_fig7b(p7)
        res["source"] = "digitised now from " + LITDIR
    else:
        res.update(RECORDED)
        res["source"] = "recorded readings (PDFs absent)"
    print("Fig 3b:", {k: (round(v, 4) if isinstance(v, float) else v) for k, v in res["fig3b"].items()})
    print("Fig 7b:", {k: (round(v, 4) if isinstance(v, float) else v) for k, v in res["fig7b"].items()})
    F_hi = res["fig3b"]["F_plateau_mean_E_gt_10p5"]
    F_lo = res["fig3b"]["F_left"]
    NP = m["two_g2MS"]                    # g^2 N_pair = 2 g^2 M_S / m_-
    der = {"F_plateau": F_hi, "F_threshold": F_lo,
           "kappa_hi": F_hi / NP, "kappa_lo": F_lo / NP,
           "g2_P0p1": F_hi / np.log(10), "g2_P1e": F_hi, "g2_P0p5": F_hi / np.log(2)}
    der["MS_over_m_at_P0p1"] = (NP / 2) / der["g2_P0p1"]
    der["MS_over_m_at_P1e"] = (NP / 2) / der["g2_P1e"]
    der["MS_over_m_at_P0p5"] = (NP / 2) / der["g2_P0p5"]
    der["Nmin_over_Npair"] = res["fig7b"]["g2Nmin_plateau_mean_E_gt_8p5"] / NP
    # a hypothetical fold-like suppression exp(-F/g^2) for QED, two identifications of g^2
    alpha = 1 / 137.035999177
    der["log10_exp_minus_F_over_alpha"] = -F_hi / alpha / np.log(10)
    der["log10_exp_minus_F_over_4pi_alpha"] = -F_hi / (4 * np.pi * alpha) / np.log(10)
    der["log10_with_original_F3p93_alpha"] = -3.93 / alpha / np.log(10)
    der["log10_with_original_F3p93_4pi_alpha"] = -3.93 / (4 * np.pi * alpha) / np.log(10)
    res["derived"] = der
    print("derived:", {k: round(v, 4) for k, v in der.items()})
    with open("x2_dl.json", "w") as fh:
        json.dump(res, fh, indent=1, default=float)


if __name__ == "__main__":
    main()
