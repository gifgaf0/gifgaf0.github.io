#!/usr/bin/env python3
"""E7 reconciliation: read the Demidov-Levkov curves from the VECTOR data in the arXiv PDFs.

Both figures are gnuplot output embedded as vector paths, so the curve vertices can be read
exactly (no pixel digitisation, no eye reading):
  * arXiv:1103.0013v2, Fig. 3b (page 3), upper panel: two-particle exponent F(E) (g^2 N = 0);
  * arXiv:1103.2133v2, Fig. 7b (page 13): classical lower boundary g^2 N_min(E) at delta rho = 0.
The page is converted to SVG with pdftocairo (poppler), stroked paths and glyph placements are
parsed, the axes are calibrated on the tick marks, and the tick-label glyph sequences are checked
for consistency with the labels read off the rendered figure (e.g. "4.4" = [g4, '.', g4]).

Usage: python3 e7_dl_digitize.py [LITDIR]   (LITDIR holds 1103.0013v2.pdf and 1103.2133v2.pdf;
default $E7_LITDIR). If the PDFs are absent the committed dl_digitized.json is left unchanged.
Writes dl_digitized.json. Deterministic, < 5 s.
"""
import json, os, re, subprocess, sys, tempfile
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'dl_digitized.json')


def svg_of_page(pdf, page):
    with tempfile.TemporaryDirectory() as td:
        f = os.path.join(td, 'p.svg')
        subprocess.run(['pdftocairo', '-svg', '-f', str(page), '-l', str(page), pdf, f], check=True)
        return open(f).read()


def stroked_paths(svg):
    """List of (stroke colour, [subpath arrays of page coords (x right, y DOWN)])."""
    out = []
    for m in re.finditer(r'<path([^>]*)/>', svg):
        a = m.group(1)
        if 'stroke=' not in a:
            continue
        d = re.search(r' d="([^"]*)"', a).group(1)
        st = re.search(r'stroke="([^"]*)"', a).group(1).replace(' ', '')
        tr = re.search(r'transform="matrix\(([^)]*)\)"', a)
        T = [float(x) for x in tr.group(1).split(',')] if tr else [1, 0, 0, 1, 0, 0]
        subs, cur, buf = [], [], []
        for t in re.findall(r'[MLCZ]|-?\d+\.?\d*(?:e-?\d+)?', d):
            if t == 'M':
                if cur:
                    subs.append(np.array(cur))
                cur = []
                continue
            if t in 'LCZ':
                continue
            buf.append(float(t))
            if len(buf) == 2:
                x, y = buf; buf = []
                cur.append((T[0] * x + T[2] * y + T[4], T[1] * x + T[3] * y + T[5]))
        if cur:
            subs.append(np.array(cur))
        out.append((st, subs))
    return out


def glyph_uses(svg):
    return [(g, float(x), float(y)) for g, x, y in
            re.findall(r'<use xlink:href="#(glyph-[\d-]+)" x="([-\d.]+)" y="([-\d.]+)"/>', svg)]


def label_at(uses, xlo, xhi, y, tol=3.5):
    """glyph id sequence of the label whose baseline is within tol below/above y, sorted by x."""
    sel = sorted([(x, g) for g, x, yy in uses if xlo < x < xhi and abs(yy - y) < tol])
    return [g for _, g in sel]


def fig3b(pdf):
    svg = svg_of_page(pdf, 3)
    P = stroked_paths(svg); U = glyph_uses(svg)
    red = 'rgb(100%,0%,0%)'
    # panel b, upper part: the single red path with x > 440 lying entirely above y = 100
    cands = [s for st, subs in P if st == red for s in subs
             if s[:, 0].min() > 440 and s[:, 1].max() < 100 and len(s) > 5]
    assert len(cands) == 1, f"expected one upper-panel red curve, found {len(cands)}"
    curve = cands[0]
    x_left = curve[:, 0].min()
    # y ticks: short horizontal black segments starting at the panel's left axis (x ~ 451.8), y < 100
    blk = 'rgb(0%,0%,0%)'
    segs = [s for st, subs in P if st == blk for s in subs if len(s) == 2]
    axis_x = min(s[:, 0].min() for s in segs if abs(s[0, 0] - x_left) < 2 and abs(s[0, 1] - s[1, 1]) > 20)
    yt = sorted({round(s[0, 1], 3) for s in segs
                 if abs(s[0, 1] - s[1, 1]) < 1e-6 and abs(min(s[:, 0]) - axis_x) < 0.01
                 and 0.5 < abs(s[0, 0] - s[1, 0]) < 2 and s[0, 1] < 100})
    assert len(yt) == 3, yt
    labels_y = [label_at(U, axis_x - 20, axis_x, y + 2.39) for y in yt]   # top to bottom
    # expected "4.4", "4.2", "4.0": same first glyph and '.', last glyph of the top label = first glyph
    g4, dot = labels_y[0][0], labels_y[0][1]
    consistent_y = (all(l[0] == g4 and l[1] == dot and len(l) == 3 for l in labels_y)
                    and labels_y[0][2] == g4 and len({l[2] for l in labels_y}) == 3)
    Fvals = [4.4, 4.2, 4.0]
    # x ticks along the bottom axis of panel b (y ~ 184.8), short vertical segments
    xt = sorted({round(s[0, 0], 3) for s in segs if abs(s[0, 0] - s[1, 0]) < 1e-6
                 and 0.5 < abs(s[0, 1] - s[1, 1]) < 2 and s[:, 1].max() > 180 and s[0, 0] > axis_x + 1})
    assert len(xt) == 5, xt     # 7, 8, 9, 10, 11 (the tick at the left edge is labelled 2 g^2 M_S)
    labels_x = [label_at(U, x - 6, x + 3, 194.37) for x in xt]
    consistent_x = (len(labels_x[3]) == 2 and len(labels_x[4]) == 2 and labels_x[4][0] == labels_x[4][1]
                    and labels_x[3][0] == labels_x[4][0] and labels_x[3][1] == labels_y[2][2])   # "10","11"; '0' as in "4.0"
    Evals = [7, 8, 9, 10, 11]
    ky = np.polyfit(yt, Fvals, 1); kx = np.polyfit(xt, Evals, 1)
    resid_y = float(np.max(np.abs(np.polyval(ky, yt) - Fvals))); resid_x = float(np.max(np.abs(np.polyval(kx, xt) - Evals)))
    g2E = np.polyval(kx, curve[:, 0]); F = np.polyval(ky, curve[:, 1])
    i_min = int(np.argmin(F))
    return dict(source="arXiv:1103.0013v2 Fig. 3b upper panel (g^2 N = 0), vector path from the PDF",
                tick_label_glyphs=dict(y=labels_y, x=labels_x, consistent_y=bool(consistent_y), consistent_x=bool(consistent_x)),
                calibration=dict(y_ticks_pt=yt, y_values=Fvals, x_ticks_pt=xt, x_values=Evals,
                                 linear_fit_max_resid=dict(F=resid_y, g2E=resid_x),
                                 F_per_pt=float(ky[0]), left_axis_g2E=float(np.polyval(kx, axis_x))),
                vertices=[[round(float(a), 4), round(float(b), 4)] for a, b in zip(g2E, F)],
                F_threshold_first_vertex=dict(g2E=float(g2E[0]), F=float(F[0])),
                F_at_g2E_11p5=float(np.interp(11.5, g2E, F)),
                F_min=dict(value=float(F[i_min]), at_g2E=float(g2E[i_min])),
                F_at_g2E_11p7_last=float(F[-1]),
                reading_uncertainty=float(abs(ky[0]) * 0.1 + resid_y),
                uncertainty_note="0.1 pt positional uncertainty (gnuplot coordinate grid) times |dF/dpt| plus tick-fit residual")


def fig7b(pdf):
    svg = svg_of_page(pdf, 13)
    P = stroked_paths(svg); U = glyph_uses(svg)
    red = 'rgb(100%,0%,0%)'; blk = 'rgb(0%,0%,0%)'
    subs = [s for st, ss in P if st == red for s in ss if len(s) > 10]
    assert len(subs) == 1, len(subs)       # the delta rho = 0 solid line (its 2-point legend sample is dropped)
    curve = subs[0]
    segs = [s for st, ss in P if st == blk for s in ss]
    # frame = the closed black 4-point rectangle; ticks = short segments starting on its left/bottom edges
    frame = [s for s in segs if len(s) == 4 and np.ptp(s[:, 0]) > 100]
    assert frame, "frame not found"
    x0, y1 = frame[0][:, 0].min(), frame[0][:, 1].max()
    hl = sorted({round(s[0, 1], 3) for s in segs if len(s) == 2 and np.ptp(s[:, 1]) < 1e-6
                 and abs(s[0, 0] - x0) < 0.01 and 1 < np.ptp(s[:, 0]) < 3})
    vl = sorted({round(s[0, 0], 3) for s in segs if len(s) == 2 and np.ptp(s[:, 0]) < 1e-6
                 and abs(s[0, 1] - y1) < 0.01 and 1 < np.ptp(s[:, 1]) < 3})
    assert len(hl) == 3 and len(vl) == 5, (hl, vl)
    labels_y = [label_at(U, 320, 357, y + 3.57) for y in hl]     # top to bottom: "4.4", "4.2", "4"
    Nvals = [4.4, 4.2, 4.0]
    consistent = (labels_y[0][-3:-1] == labels_y[1][-3:-1] and labels_y[0][-1] == labels_y[0][-3]
                  and labels_y[2][-1] == labels_y[0][-3])
    Evals = [6, 7, 8, 9, 10]
    ky = np.polyfit(hl, Nvals, 1); kx = np.polyfit(vl, Evals, 1)
    g2E = np.polyval(kx, curve[:, 0]); g2N = np.polyval(ky, curve[:, 1])
    hi = g2E >= 8.5
    return dict(source="arXiv:1103.2133v2 Fig. 7b, delta rho = 0 solid line, vector path from the PDF",
                tick_label_glyphs=dict(y=labels_y, consistent=bool(consistent)),
                calibration=dict(y_grid_pt=hl, y_values=Nvals, x_grid_pt=vl, x_values=Evals),
                g2Nmin_near_threshold=dict(g2E=float(g2E[0]), value=float(g2N[0]), at_6p25=float(np.interp(6.25, g2E, g2N))),
                g2Nmin_high_energy_mean_8p5_to_10p5=float(np.mean(g2N[hi])),
                g2Nmin_high_energy_range=[float(g2N[hi].min()), float(g2N[hi].max())],
                g2Nmin_at_10p5=float(g2N[-1]))


def main():
    lit = sys.argv[1] if len(sys.argv) > 1 else os.environ.get('E7_LITDIR', '')
    p1 = os.path.join(lit, '1103.0013v2.pdf'); p2 = os.path.join(lit, '1103.2133v2.pdf')
    if not (lit and os.path.exists(p1) and os.path.exists(p2)):
        print(f"PDFs not found in '{lit}': keeping committed {os.path.basename(OUT)}")
        return
    res = dict(method="vector-path extraction (pdftocairo -svg), axes calibrated on tick marks",
               fig3b=fig3b(p1), fig7b=fig7b(p2))
    json.dump(res, open(OUT, 'w'), indent=1)
    a, b = res['fig3b'], res['fig7b']
    print("Fig. 3b (two-particle exponent F, g^2 N = 0)")
    print(f"  tick-label glyph consistency: y {a['tick_label_glyphs']['consistent_y']}, x {a['tick_label_glyphs']['consistent_x']}")
    print(f"  left axis at g^2E = {a['calibration']['left_axis_g2E']:.4f} (2 g^2 M_S = 6.2358 by quadrature)")
    print(f"  F at first vertex (g^2E = {a['F_threshold_first_vertex']['g2E']:.3f}) = {a['F_threshold_first_vertex']['F']:.4f}")
    print(f"  F(g^2E = 11.5) = {a['F_at_g2E_11p5']:.4f};  min F = {a['F_min']['value']:.4f} at g^2E = {a['F_min']['at_g2E']:.2f};"
          f"  reading uncertainty ~{a['reading_uncertainty']:.4f}")
    print("  vertices (g^2E, F):", ', '.join(f"({u:.2f}, {v:.3f})" for u, v in a['vertices']))
    print("Fig. 7b (classical g^2 N_min, delta rho = 0)")
    print(f"  tick-label glyph consistency: {b['tick_label_glyphs']['consistent']}")
    print(f"  near threshold g^2N_min({b['g2Nmin_near_threshold']['g2E']:.2f}) = {b['g2Nmin_near_threshold']['value']:.3f}")
    print(f"  high energy (8.5-10.5): mean {b['g2Nmin_high_energy_mean_8p5_to_10p5']:.4f}, range {b['g2Nmin_high_energy_range']}")


if __name__ == '__main__':
    main()
