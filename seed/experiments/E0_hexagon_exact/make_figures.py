#!/usr/bin/env python3
"""
make_figures.py -- the two diagrams for E0 (deterministic; geometry is computed exactly
with Fractions and converted to floats only for drawing).

  fig_torus_p6m.png
    (a) the SU(3) torus (plane / hexagonal lattice Lambda) with the seven points D^j and the
        triangulation cut by the finer lattice Lambda + Zp: the two families of 7 triangles
        (blue = octonion lines {i,i+1,i+3}, orange = {i,i+2,i+3});
    (b) the mirror lines of G2's affine Weyl group (p6m) with its 6-, 3- and 2-fold centres,
        and the seven points: no mirror maps the seven points to themselves.
Run: python3 make_figures.py
"""
import itertools
import os
from fractions import Fraction as F

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt                       # noqa: E402
from matplotlib.patches import Polygon                # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
SURFACE, INK, INK2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#d9d8d3"
BLUE, ORANGE = "#2a78d6", "#eb6834"                  # validated pair (dataviz validator: all checks pass)

u = (1, -1, 0)
w = (1, 1, -2)


def xy(v):
    """plane vector (sum 0) -> 2D drawing coordinates (orthonormal frame u/|u|, w/|w|)."""
    return (float(sum(a * b for a, b in zip(v, u))) / 2 ** 0.5, float(sum(a * b for a, b in zip(v, w))) / 6 ** 0.5)


def add(*vs):
    return tuple(sum(c) for c in zip(*vs))


def sc(k, v):
    return tuple(k * a for a in v)


b1, b2 = (F(1), F(-1), F(0)), (F(0), F(1), F(-1))
p = (F(1, 7), F(2, 7), F(-3, 7))
tp = (p[2], p[0], p[1])
a_v, c_v = p, add(p, tp)


def label(v):
    for j in range(7):
        d = add(v, sc(-j, p))
        if all(x.denominator == 1 for x in d) and sum(d) == 0:
            return j
    return None


octonion = {tuple(sorted(((i) % 7, (i + 1) % 7, (i + 3) % 7))) for i in range(7)}

fig, axes = plt.subplots(1, 2, figsize=(11.0, 5.3), dpi=110, facecolor=SURFACE)
for ax in axes:
    ax.set_facecolor(SURFACE)
    ax.set_aspect("equal")
    ax.axis("off")

# ---------------- (a) torus triangulation ----------------
ax = axes[0]
cell = [xy(sc(0, b1)), xy(b1), xy(add(b1, b2)), xy(b2)]
clip = Polygon(cell, closed=True, facecolor="none", edgecolor="none")
ax.add_patch(clip)
for m, n in itertools.product(range(-8, 9), repeat=2):
    x0 = add(sc(m, p), sc(n, tp))
    for tri, fam_is_up in (([x0, add(x0, a_v), add(x0, c_v)], True),
                           ([add(x0, a_v), add(add(x0, a_v), c_v), add(x0, c_v)], False)):
        pts = [xy(t) for t in tri]
        cx = sum(q[0] for q in pts) / 3
        cy = sum(q[1] for q in pts) / 3
        labs = tuple(sorted(label(t) for t in tri))
        col = BLUE if labs in octonion else ORANGE
        poly = Polygon(pts, closed=True, facecolor=col, alpha=0.30 if labs in octonion else 0.26,
                       edgecolor=SURFACE, linewidth=2.0)
        ax.add_patch(poly)
        poly.set_clip_path(clip)
# vertices with labels
for m, n in itertools.product(range(-8, 9), repeat=2):
    v = add(sc(m, p), sc(n, tp))
    X, Y = xy(v)
    # inside closed cell? test in Lambda coordinates
    al, be = v[0], -v[2]
    if -F(1, 100) <= al <= 1 + F(1, 100) and -F(1, 100) <= be <= 1 + F(1, 100):
        ax.plot(X, Y, "o", ms=8.5, color=INK, mec=SURFACE, mew=2, zorder=5)
        ax.annotate(str(label(v)), (X, Y), xytext=(5, 5), textcoords="offset points", fontsize=10, color=INK,
                    zorder=6)
ax.add_patch(Polygon(cell, closed=True, facecolor="none", edgecolor=INK2, linewidth=1.2, linestyle="--", zorder=4))
xs = [c[0] for c in cell]
ys = [c[1] for c in cell]
ax.set_xlim(min(xs) - 0.15, max(xs) + 0.15)
ax.set_ylim(min(ys) - 0.30, max(ys) + 0.10)
ax.set_title("(a) SU(3) torus = plane / Λ, cut by Λ + ℤp", fontsize=11, color=INK, loc="left", pad=28)
ax.text(0.0, 1.0, "dashed: one cell of Λ (opposite sides identified); labels j = D^j\n"
        "7 vertices, 21 edges, 14 triangles: χ= 0, every pair joined (K₇)",
        transform=ax.transAxes, fontsize=8.5, color=INK2, ha="left", va="bottom")
from matplotlib.patches import Patch  # noqa: E402
ax.legend(handles=[Patch(facecolor=BLUE, alpha=0.45, label="{i, i+1, i+3}  (octonion lines)"),
                   Patch(facecolor=ORANGE, alpha=0.40, label="{i, i+2, i+3}")],
          loc="lower left", fontsize=8.5, frameon=False, labelcolor=INK, bbox_to_anchor=(0.0, 0.0), ncol=2)

# ---------------- (b) p6m mirror pattern of G2's affine Weyl group ----------------
ax = axes[1]
third = (F(1, 3),) * 3
E = [tuple(F(int(i == k)) for k in range(3)) for i in range(3)]
long_r = [add(E[i], sc(-1, E[j])) for i, j in ((0, 1), (1, 2), (0, 2))]
short_r = [add(E[i], sc(-1, third)) for i in range(3)]
R = 1.55
ax.set_xlim(-R, R)
ax.set_ylim(-R * 0.92, R * 0.92)


def line_through(alpha, k):
    """points x in the plane with (alpha, x) = k, drawn as a long segment."""
    al = xy(alpha)
    n2 = al[0] ** 2 + al[1] ** 2
    a3 = float(sum(x * x for x in alpha))
    # in drawing coords (alpha, x) = (al . X) since the frame is orthonormal
    base = (k * al[0] / n2, k * al[1] / n2)
    d = (-al[1], al[0])
    L = 5
    return [(base[0] - L * d[0], base[1] - L * d[1]), (base[0] + L * d[0], base[1] + L * d[1])]


for alpha in long_r + short_r:
    for k in range(-8, 9):
        seg = line_through(alpha, k)
        ax.plot([seg[0][0], seg[1][0]], [seg[0][1], seg[1][1]], color=GRID, lw=1.0, zorder=1)
# rotation centres (from e0_exact.py, Lambda coordinates): 6-fold at Lambda, 3-fold at (1/3,2/3),(2/3,1/3), 2-fold at halves
cent = {6: [(F(0), F(0))], 3: [(F(1, 3), F(2, 3)), (F(2, 3), F(1, 3))],
        2: [(F(0), F(1, 2)), (F(1, 2), F(0)), (F(1, 2), F(1, 2))]}
mk = {6: ("h", 9.5), 3: ("^", 7.5), 2: ("D", 5.0)}
for order, cs in cent.items():
    first = True
    for (al_, be_) in cs:
        for m, n in itertools.product(range(-4, 5), repeat=2):
            v = add(sc(al_ + m, b1), sc(be_ + n, b2))
            X, Y = xy(v)
            if abs(X) < R and abs(Y) < R * 0.92:
                ax.plot(X, Y, mk[order][0], ms=mk[order][1], color=INK2, mec=SURFACE, mew=1.2, zorder=3,
                        label=(f"{order}-fold centre" if first else None))
                first = False
first = True
for m, n in itertools.product(range(-12, 13), repeat=2):
    v = add(sc(m, p), sc(n, tp))
    X, Y = xy(v)
    if abs(X) < R and abs(Y) < R * 0.92 and label(v) != 0:
        ax.plot(X, Y, "o", ms=5.5, color=BLUE, mec=SURFACE, mew=1.0, zorder=4,
                label=("the seven points (Λ + ℤp; point 0 = 6-fold centres)" if first else None))
        first = False
ax.set_title("(b) G₂ affine Weyl group: mirror lines = p6m", fontsize=11, color=INK, loc="left", pad=16)
ax.legend(loc="upper center", fontsize=8.5, frameon=False, labelcolor=INK, ncol=2,
          bbox_to_anchor=(0.5, -0.01))
ax.text(0.0, 1.0, "the seven points lie on no mirror except at the 6-fold centres: the turns keep them, no mirror does",
        transform=ax.transAxes, fontsize=8.5, color=INK2, ha="left", va="bottom")
fig.tight_layout()
out = os.path.join(HERE, "fig_torus_p6m.png")
fig.savefig(out, facecolor=SURFACE)
print("wrote", out, os.path.getsize(out), "bytes")
