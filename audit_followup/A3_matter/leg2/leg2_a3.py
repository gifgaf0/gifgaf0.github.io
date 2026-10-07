#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
leg2_a3.py -- BLIND SECOND LEG for A3 (numerics behind DR-A3-1,2,3,4,5,7).

Written without access to any first-leg file; only A3_PREREG.md and A3_LOCK.txt were read.
Run from anywhere:   python3 leg2_a3.py | tee leg2_output.txt
Writes leg2_results.json next to this file.

Method choices (deliberately not the "obvious" route where a choice exists):
  T1  closed form from exact arc angles (junction geometry), checked by Richardson-
      extrapolated inscribed polygons; tube embedding via the point-tangent (global)
      radius-of-curvature functional (thickness = inf rho_pt), exact point-to-arc
      distances, exact enumeration of doubly-critical self-chords; linking numbers via
      the exact polygon solid-angle formula (Banchoff / Klenin-Langowski) plus a
      disc-piercing count; link type via an explicit isotopy to three perpendicular
      ellipses and via Fox calculus on a generic projection of the actual 3-D curves.
  T2  inversion in closed form with the Lambert W function (branch -1) at 50 digits,
      cross-checked by plain bisection.
  T3  50-digit evaluation of the stated inputs.
  T4  Wirtinger presentation generated arc-by-arc from the closed-braid diagram of
      (s1 s2^-1)^3; abelianised Fox Jacobian; minors and gcd over Z[t]. Conway
      polynomial by skein recursion on descending diagrams; reduced Burau as a third
      route to Delta_L(t).
"""
import json
import math
import os
import sys
import time
from fractions import Fraction
from functools import lru_cache

import numpy as np
import mpmath as mp
import sympy as sp
from scipy.spatial import cKDTree

mp.mp.dps = 50
HERE = os.path.dirname(os.path.abspath(__file__))
RES = {"meta": {"script": "leg2_a3.py", "mp_dps": mp.mp.dps,
                "numpy": np.__version__, "sympy": sp.__version__, "mpmath": mp.__version__,
                "python": sys.version.split()[0]}}
T_START = time.time()


def P(*a):
    print(*a, flush=True)


def ns(x, n=20):
    return mp.nstr(mp.mpf(x), n)


def hdr(s):
    P("")
    P("=" * 78)
    P(s)
    P("=" * 78)


# =============================================================================
# T1  Four-arc Borromean configuration
# =============================================================================
S7 = math.sqrt(7.0)
AH = S7 + 1.0   # major half-diagonal: centres of the CONCAVE (waist) arcs, on the u axis
BH = S7 - 1.0   # minor half-diagonal: centres of the CONVEX (lobe) arcs, on the v axis
RA = 2.0        # arc radius = contact distance = 2 x (tube radius 1)
BETA = math.atan2(BH, AH)   # half-angle at the rhombus vertex; 2*BETA = asin(3/4)

# (name, centre (u,v), start angle, signed sweep). Traversed in this order; C^1 at the joins.
ARCS = [
    ("lobe(+v)",  (0.0,  BH), -BETA,           math.pi + 2 * BETA),   # convex, ccw
    ("waist(-u)", (-AH, 0.0),  BETA,           -2 * BETA),            # concave, cw
    ("lobe(-v)",  (0.0, -BH),  math.pi - BETA, math.pi + 2 * BETA),   # convex, ccw
    ("waist(+u)", (AH, 0.0),   math.pi + BETA, -2 * BETA),            # concave, cw
]
ARC_LEN = np.array([RA * abs(a[3]) for a in ARCS])
CUM = np.concatenate([[0.0], np.cumsum(ARC_LEN)])
LCOMP = float(CUM[-1])
EX, EY, EZ = np.eye(3)
# plane frames (e_u, e_v); C2 = sigma(C1), C3 = sigma(C2) with sigma(x,y,z) = (z,x,y)
FRAMES = [(EX, EY), (EY, EZ), (EZ, EX)]
NORMALS = [np.cross(a, b) for a, b in FRAMES]


def curve_uv(s):
    """planar curve and unit tangent at arc-length positions s (array)."""
    s = np.mod(np.asarray(s, float), LCOMP)
    k = np.clip(np.searchsorted(CUM, s, side="right") - 1, 0, 3)
    uv = np.empty((len(s), 2))
    tg = np.empty((len(s), 2))
    for j, (_, c, a0, sw) in enumerate(ARCS):
        m = k == j
        th = a0 + np.sign(sw) * (s[m] - CUM[j]) / RA
        uv[m, 0] = c[0] + RA * np.cos(th)
        uv[m, 1] = c[1] + RA * np.sin(th)
        tg[m, 0] = -np.sign(sw) * np.sin(th)
        tg[m, 1] = np.sign(sw) * np.cos(th)
    return uv, tg, k


def sample_with_midpoints(h):
    """sample each arc at an even number of equal angular steps (mid-points are samples)."""
    out_uv, out_tg, out_k, out_s = [], [], [], []
    for j, (_, c, a0, sw) in enumerate(ARCS):
        n = max(2, 2 * int(round(ARC_LEN[j] / (2 * h))))
        q = np.arange(n) / n
        th = a0 + sw * q
        out_uv.append(np.stack([c[0] + RA * np.cos(th), c[1] + RA * np.sin(th)], 1))
        out_tg.append(np.sign(sw) * np.stack([-np.sin(th), np.cos(th)], 1))
        out_k.append(np.full(n, j))
        out_s.append(CUM[j] + ARC_LEN[j] * q)
    return (np.vstack(out_uv), np.vstack(out_tg), np.concatenate(out_k), np.concatenate(out_s))


def embed(uv, comp):
    eu, ev = FRAMES[comp]
    return uv[:, :1] * eu[None, :] + uv[:, 1:2] * ev[None, :]


def arc3d(comp, j):
    _, c, a0, sw = ARCS[j]
    eu, ev = FRAMES[comp]
    centre = c[0] * eu + c[1] * ev
    lo = min(a0, a0 + sw)
    return centre, eu, ev, lo, abs(sw)


def dist_to_component(X, comp):
    """exact Euclidean distance from points X (n,3) to component `comp` (union of 4 arcs)."""
    best = np.full(len(X), np.inf)
    for j in range(4):
        centre, eu, ev, lo, width = arc3d(comp, j)
        d = X - centre
        x, y, hgt = d @ eu, d @ ev, d @ np.cross(eu, ev)
        rho = np.hypot(x, y)
        th = np.arctan2(y, x)
        inside = np.mod(th - lo, 2 * np.pi) <= width
        dfull = np.sqrt(hgt ** 2 + (rho - RA) ** 2)
        e0 = centre + RA * (math.cos(lo) * eu + math.sin(lo) * ev)
        e1 = centre + RA * (math.cos(lo + width) * eu + math.sin(lo + width) * ev)
        dend = np.minimum(np.linalg.norm(X - e0, axis=1), np.linalg.norm(X - e1, axis=1))
        best = np.minimum(best, np.where(inside, dfull, dend))
    return best


def min_rho_pt(X, T, grp, mode, chunk=96):
    """thickness functional: min over ordered pairs x != y of |x-y|^2 / (2 |T(y) x (x-y)|)
    (radius of the circle through x tangent to the curve at y). mode: 'all','same','cross'."""
    best, arg = np.inf, None
    M = len(X)
    for a in range(0, M, chunk):
        Y, TY, gY = X[a:a + chunk], T[a:a + chunk], grp[a:a + chunk]
        D = X[None, :, :] - Y[:, None, :]
        num = np.einsum("ijk,ijk->ij", D, D)
        cr = np.cross(TY[:, None, :], D)
        den = 2.0 * np.sqrt(np.einsum("ijk,ijk->ij", cr, cr))
        with np.errstate(divide="ignore", invalid="ignore"):
            rho = np.where(den > 0, num / den, np.inf)
        rho[num == 0] = np.inf
        if mode != "all":
            same = gY[:, None] == grp[None, :]
            rho[~same if mode == "same" else same] = np.inf
        i = np.unravel_index(np.argmin(rho), rho.shape)
        if rho[i] < best:
            best, arg = float(rho[i]), (a + int(i[0]), int(i[1]))
    return best, arg


def lk_solid_angle(Pp, Qq, chunk=128):
    """exact Gauss linking integral of two closed polygons (signed solid angles / 4 pi)."""
    P1, P2 = Pp, np.roll(Pp, -1, axis=0)
    Q1, Q2 = Qq[None], np.roll(Qq, -1, axis=0)[None]

    def unit(v):
        return v / np.linalg.norm(v, axis=-1, keepdims=True)

    tot = 0.0
    for a in range(0, len(Pp), chunk):
        r1, r2 = P1[a:a + chunk, None], P2[a:a + chunk, None]
        r13, r14, r23, r24 = Q1 - r1, Q2 - r1, Q1 - r2, Q2 - r2
        n1 = unit(np.cross(r13, r14)); n2 = unit(np.cross(r14, r24))
        n3 = unit(np.cross(r24, r23)); n4 = unit(np.cross(r23, r13))
        dot = lambda u, v: np.clip(np.einsum("ijk,ijk->ij", u, v), -1.0, 1.0)
        om = np.arcsin(dot(n1, n2)) + np.arcsin(dot(n2, n3)) + np.arcsin(dot(n3, n4)) + np.arcsin(dot(n4, n1))
        sg = np.sign(np.einsum("ijk,ijk->ij", np.cross(Q2 - Q1, r2 - r1), r13))
        tot += float(np.sum(om * sg))
    return tot / (4 * math.pi)


def winding(poly2d, q):
    d = poly2d - q
    ang = np.arctan2(d[:, 1], d[:, 0])
    dang = np.diff(np.concatenate([ang, ang[:1]]))
    dang = (dang + np.pi) % (2 * np.pi) - np.pi
    return int(round(dang.sum() / (2 * np.pi)))


def radial_C(theta):
    """polar radius of the four-arc planar curve (it is star-shaped about its centre)."""
    th = np.mod(np.asarray(theta) + np.pi, 2 * np.pi) - np.pi
    e = np.stack([np.cos(th), np.sin(th)], 1)

    def root(c, sgn):
        ec = e @ np.array(c)
        disc = ec ** 2 - (c[0] ** 2 + c[1] ** 2) + RA ** 2   # negative only off the arc's own sector
        return ec + sgn * np.sqrt(np.maximum(disc, 0.0))

    wr, wl = np.abs(th) <= BETA, np.abs(th) >= np.pi - BETA
    lt, lb = (~wr) & (~wl) & (th > 0), (~wr) & (~wl) & (th < 0)
    r = np.empty_like(th)
    r[wr] = root((AH, 0.0), -1)[wr]
    r[wl] = root((-AH, 0.0), -1)[wl]
    r[lt] = root((0.0, BH), +1)[lt]
    r[lb] = root((0.0, -BH), +1)[lb]
    return r


def radial_E(theta, p=BH, q=AH):
    return 1.0 / np.sqrt(np.cos(theta) ** 2 / p ** 2 + np.sin(theta) ** 2 / q ** 2)


def diagram_from_polygons(polys, view):
    """generic projection -> crossings -> Wirtinger data (arcs, relations) for Fox calculus."""
    v = np.asarray(view, float); v /= np.linalg.norm(v)
    a = np.array([1.0, 0, 0]) if abs(v[0]) < 0.9 else np.array([0, 1.0, 0])
    e1 = a - (a @ v) * v; e1 /= np.linalg.norm(e1); e2 = np.cross(v, e1)   # e1 x e2 = v
    S0, S1, C, K, NC = [], [], [], [], []
    for c, Pc in enumerate(polys):
        n = len(Pc)
        S0.append(Pc); S1.append(np.roll(Pc, -1, axis=0))
        C.append(np.full(n, c)); K.append(np.arange(n)); NC.append(np.full(n, n))
    S0, S1 = np.vstack(S0), np.vstack(S1)
    C, K, NC = np.concatenate(C), np.concatenate(K), np.concatenate(NC)
    p0 = np.stack([S0 @ e1, S0 @ e2], 1); r = np.stack([S1 @ e1, S1 @ e2], 1) - p0
    h0, h1 = S0 @ v, S1 @ v
    M = len(S0); found = []
    for a0 in range(0, M, 200):
        I = np.arange(a0, min(M, a0 + 200))
        Pp, Rr = p0[I][:, None], r[I][:, None]
        QP = p0[None] - Pp
        W = r[None]
        den = Rr[..., 0] * W[..., 1] - Rr[..., 1] * W[..., 0]
        with np.errstate(divide="ignore", invalid="ignore"):
            s = (QP[..., 0] * W[..., 1] - QP[..., 1] * W[..., 0]) / den
            u = (QP[..., 0] * Rr[..., 1] - QP[..., 1] * Rr[..., 0]) / den
        ok = (den != 0) & (s >= 0) & (s < 1) & (u >= 0) & (u < 1)
        ok &= np.arange(M)[None, :] > I[:, None]
        same = C[I][:, None] == C[None, :]
        dk = np.mod(K[I][:, None] - K[None, :], NC[None, :])
        ok &= ~(same & ((dk == 0) | (dk == 1) | (dk == NC[None, :] - 1)))
        for ii, jj in zip(*np.nonzero(ok)):
            found.append((int(I[ii]), int(jj), float(s[ii, jj]), float(u[ii, jj])))
    passages = {c: [] for c in range(len(polys))}
    X = []
    for (i, j, s, u) in found:
        di, dj = h0[i] + s * (h1[i] - h0[i]), h0[j] + u * (h1[j] - h0[j])
        (ov, so), (un, su) = ((i, s), (j, u)) if di > dj else ((j, u), (i, s))
        cr = r[ov][0] * r[un][1] - r[ov][1] * r[un][0]
        ang = abs(cr) / (np.linalg.norm(r[ov]) * np.linalg.norm(r[un]))
        X.append(dict(oc=int(C[ov]), op=float(K[ov] + so), uc=int(C[un]), up=float(K[un] + su),
                      sign=int(np.sign(cr)), gap=float(abs(di - dj)), sin_angle=float(ang)))
        passages[int(C[ov])].append(float(K[ov] + so))
    unders = {c: sorted(x["up"] for x in X if x["uc"] == c) for c in range(len(polys))}
    arc_id, arc_comp = {}, []
    for c in range(len(polys)):
        for jj in range(max(1, len(unders[c]))):
            arc_id[(c, jj)] = len(arc_comp); arc_comp.append(c)

    def arc_at(c, pos):
        U = unders[c]
        if not U:
            return arc_id[(c, 0)]
        jj = int(np.searchsorted(U, pos, side="right")) - 1
        return arc_id[(c, jj if jj >= 0 else len(U) - 1)]

    rels = []
    for x in X:
        U = unders[x["uc"]]; jj = U.index(x["up"])
        rels.append((arc_id[(x["uc"], jj)], arc_at(x["oc"], x["op"]),
                     arc_id[(x["uc"], (jj - 1) % len(U))], x["sign"]))
    return arc_comp, rels, X


def run_T1():
    hdr("T1  Four-arc Borromean configuration (DR-A3-1)")
    out = {}
    # ---- (a) construction --------------------------------------------------
    P("Rhombus: side 4, half-diagonals a = sqrt7+1 = %.15f (u axis), b = sqrt7-1 = %.15f (v axis)" % (AH, BH))
    P("  check a^2+b^2 = %.15f (=16), 2a-2b = %.15f (=4)" % (AH ** 2 + BH ** 2, 2 * AH - 2 * BH))
    P("Choice: CONVEX lobes = arcs centred at the minor-diagonal vertices (0,+-b);")
    P("        CONCAVE waists = arcs centred at the major-diagonal vertices (+-a,0).")
    P("  (Opposite assignment: waists centred at (0,+-b) would reach v = b-2 = -0.354 and -b+2 = +0.354,")
    P("   i.e. cross each other, and the far point would sit at sqrt7+3, not sqrt7+1. Rejected.)")
    P("  lobe sweep = pi + asin(3/4) = %.12f rad (%.6f deg); waist sweep = asin(3/4) = %.12f rad (%.6f deg)"
      % (math.pi + 2 * BETA, math.degrees(math.pi + 2 * BETA), 2 * BETA, math.degrees(2 * BETA)))
    joins = []
    for j in range(4):
        _, c, a0, sw = ARCS[j]
        _, c2, b0, sw2 = ARCS[(j + 1) % 4]
        pe = np.array(c) + RA * np.array([math.cos(a0 + sw), math.sin(a0 + sw)])
        ps = np.array(c2) + RA * np.array([math.cos(b0), math.sin(b0)])
        te = np.sign(sw) * np.array([-math.sin(a0 + sw), math.cos(a0 + sw)])
        ts_ = np.sign(sw2) * np.array([-math.sin(b0), math.cos(b0)])
        joins.append((float(np.linalg.norm(pe - ps)), float(np.linalg.norm(te - ts_)), pe.tolist()))
    P("Joins (position gap, tangent gap, join point):")
    for g in joins:
        P("   %.2e  %.2e  (%.12f, %.12f)" % (g[0], g[1], g[2][0], g[2][1]))
    turning = sum(a[3] for a in ARCS)
    P("Total turning = %.15f (2 pi = %.15f)" % (turning, 2 * math.pi))
    P("Arc table (component C1 in the xy-plane; C2 = sigma(C1), C3 = sigma(C2), sigma(x,y,z)=(z,x,y)):")
    arc_rows = []
    for comp in range(3):
        for j, (nm, c, a0, sw) in enumerate(ARCS):
            centre, eu, ev, lo, width = arc3d(comp, j)
            others = [(o, float(dist_to_component(centre[None], o)[0])) for o in range(3) if o != comp]
            host = min(others, key=lambda t: t[1])
            row = dict(component=comp + 1, arc=nm, kind="convex" if sw > 0 else "concave",
                       centre=[round(float(x), 15) for x in centre], radius=RA,
                       sweep_rad=abs(sw), length=RA * abs(sw),
                       centre_lies_on_component=host[0] + 1, centre_distance_to_it=host[1])
            arc_rows.append(row)
            P("  C%d %-9s %-7s centre (%+.6f,%+.6f,%+.6f) sweep %.12f rad  len %.12f  centre on C%d (dist %.1e)"
              % (comp + 1, nm, row["kind"], *centre, abs(sw), RA * abs(sw), host[0] + 1, host[1]))
    out["arcs"] = arc_rows
    out["joins_max_position_gap"] = max(g[0] for g in joins)
    out["joins_max_tangent_gap"] = max(g[1] for g in joins)

    # ---- (b) length ---------------------------------------------------------
    asin34 = mp.asin(mp.mpf(3) / 4)
    Ltot = 12 * mp.pi + 24 * asin34
    Lcomp = 4 * mp.pi + 8 * asin34
    alt1 = 12 * mp.pi + 24 * mp.atan(3 / mp.sqrt(7))
    alt2 = 12 * mp.pi + 48 * mp.atan((mp.sqrt(7) - 1) / (mp.sqrt(7) + 1))
    P("")
    P("(b) per component: 2 lobes x 2(pi+asin(3/4)) + 2 waists x 2 asin(3/4) = 4 pi + 8 asin(3/4)")
    P("    L_total = 12 pi + 24 asin(3/4) = 12 pi + 24 atan(3/sqrt7) = 12 pi + 48 atan((sqrt7-1)/(sqrt7+1))")
    P("    L_total   = %s" % ns(Ltot, 25))
    P("    L_comp    = %s" % ns(Lcomp, 25))
    P("    alt forms = %s , %s" % (ns(alt1, 25), ns(alt2, 25)))
    P("    float sum of R|sweep| over 12 arcs = %.15f" % (3 * LCOMP))
    # Richardson-extrapolated inscribed polygons (vertices uniform in a global parameter, not aligned to joins)
    pl = []
    for N in (2000, 4000, 8000, 16000):
        s = (np.arange(N) + 0.3819660113) * LCOMP / N
        uv, _, _ = curve_uv(s)
        pl.append(3 * float(np.sum(np.linalg.norm(np.roll(uv, -1, 0) - uv, axis=1))))
    r1 = [(4 * pl[i + 1] - pl[i]) / 3 for i in range(3)]
    r2 = [(16 * r1[i + 1] - r1[i]) / 15 for i in range(2)]
    P("    inscribed polygons N=2k..16k: %s" % ", ".join("%.12f" % x for x in pl))
    P("    Richardson (h^2): %s ; (h^4): %s" % (", ".join("%.12f" % x for x in r1), ", ".join("%.12f" % x for x in r2)))
    P("    |extrapolated - closed form| = %.2e" % abs(r2[-1] - float(Ltot)))
    rel_5805 = (Ltot - mp.mpf("58.05")) / mp.mpf("58.05")
    rel_58006 = (Ltot - mp.mpf("58.006")) / mp.mpf("58.006")
    P("    rel. diff vs CKS02 'about 58.05' = %s (%.5f %%); vs 58.006 = %s (%.5f %%)"
      % (ns(rel_5805, 8), float(rel_5805) * 100, ns(rel_58006, 8), float(rel_58006) * 100))
    out.update(L_total_closed_form="12*pi + 24*asin(3/4)", L_total=ns(Ltot, 25), L_component=ns(Lcomp, 25),
               L_total_12digits=mp.nstr(Ltot, 12), polygon_lengths=pl, richardson_h4=r2,
               richardson_abs_err=abs(r2[-1] - float(Ltot)),
               rel_diff_vs_58_05=float(rel_5805), rel_diff_vs_58_006=float(rel_58006),
               within_0p2pct_of_58_05=bool(abs(rel_5805) < mp.mpf("0.002")))

    # ---- (c) embedding of unit tubes ----------------------------------------
    P("")
    P("(c) Embedding of radius-1 tubes")
    uv, tg, kk, ss = sample_with_midpoints(0.008)
    Xs = [embed(uv, c) for c in range(3)]
    Ts = [embed(tg, c) for c in range(3)]
    # curvature radius: analytic 2 on every arc; numeric circumradius of consecutive triples
    sG = (np.arange(30000) + 0.123456789) * LCOMP / 30000
    uvG, _, kG = curve_uv(sG)
    p0, p1, p2 = uvG, np.roll(uvG, -1, 0), np.roll(uvG, -2, 0)
    a_, b_, c_ = p1 - p0, p2 - p1, p2 - p0
    cr = np.abs(a_[:, 0] * b_[:, 1] - a_[:, 1] * b_[:, 0])
    circ = np.linalg.norm(a_, axis=1) * np.linalg.norm(b_, axis=1) * np.linalg.norm(c_, axis=1) / (2 * cr)
    P("    curvature radius: analytic 2 on all 12 arcs; numeric min circumradius of triples = %.12f" % circ.min())
    out["min_curvature_radius_numeric"] = float(circ.min())
    out["curvature_radius_analytic"] = 2.0
    # inter-component distances: exact point-to-arc distances from dense samples
    uvD, _, kD, _ = sample_with_midpoints(0.001)
    pair_min = {}
    contact_frac = {}
    for i in range(3):
        Xi = embed(uvD, i)
        dists = {j: dist_to_component(Xi, j) for j in range(3) if j != i}
        for j, d in dists.items():
            pair_min["C%d->C%d" % (i + 1, j + 1)] = float(d.min())
            contact_frac["C%d->C%d" % (i + 1, j + 1)] = float(np.mean(np.abs(d - 2.0) < 1e-12))
        dmin_any = np.minimum(*dists.values())
        contact_frac["C%d->any" % (i + 1)] = float(np.mean(np.abs(dmin_any - 2.0) < 1e-12))
    for k_, v_ in pair_min.items():
        P("    min dist %s = %.16f   (fraction of C_i samples at exactly 2 +- 1e-12: %.4f)" % (k_, v_, contact_frac[k_]))
    P("    fraction of each component in contact (dist = 2 to some other component): %s"
      % ", ".join("%s %.6f" % (k_, v_) for k_, v_ in contact_frac.items() if "any" in k_))
    trees = [cKDTree(embed(uvD, c)) for c in range(3)]
    kd = {}
    for i in range(3):
        for j in range(i + 1, 3):
            d, _ = trees[j].query(embed(uvD, i))
            kd["C%d-C%d" % (i + 1, j + 1)] = float(d.min())
    P("    KD-tree cross-check (sample-to-sample, h=1e-3): %s" % kd)
    out.update(min_intercomponent_distance=min(pair_min.values()), intercomponent_pair_min=pair_min,
               contact_fraction=contact_frac, kdtree_pair_min=kd)
    # thickness functional on the whole link and on each component
    Xall, Tall = np.vstack(Xs), np.vstack(Ts)
    grp = np.concatenate([np.full(len(uv), c) for c in range(3)])
    th_all, arg_all = min_rho_pt(Xall, Tall, grp, "all")
    th_same, arg_same = min_rho_pt(Xall, Tall, grp, "same")
    th_cross, _ = min_rho_pt(Xall, Tall, grp, "cross")
    P("    thickness (inf of point-tangent radius rho_pt over %d samples):" % len(Xall))
    P("      whole link   = %.15f  (pair: %s / %s)" % (th_all, Xall[arg_all[1]].round(6), Xall[arg_all[0]].round(6)))
    P("      same comp    = %.15f  (sqrt7-1 = %.15f)" % (th_same, S7 - 1))
    P("      cross comp   = %.15f" % th_cross)
    out.update(thickness_link=th_all, thickness_single_component=th_same, thickness_cross_pairs=th_cross)
    # doubly-critical self-chords, exact enumeration (planar curve: chord lies on the line of centres)
    def on_arc(pnt, j, tol=1e-9):
        _, c, a0, sw = ARCS[j]
        d = np.array(pnt) - np.array(c)
        if abs(np.hypot(*d) - RA) > tol:
            return False
        lo, w = min(a0, a0 + sw), abs(sw)
        return (math.atan2(d[1], d[0]) - lo) % (2 * math.pi) <= w + tol
    dcs = []
    for j in range(4):
        for l in range(j, 4):
            cj, cl = np.array(ARCS[j][1]), np.array(ARCS[l][1])
            if j == l:
                if abs(ARCS[j][3]) > math.pi:
                    dcs.append((2 * RA, ARCS[j][0], ARCS[l][0]))
                continue
            e = (cl - cj) / np.linalg.norm(cl - cj)
            for sx in (1, -1):
                for sy in (1, -1):
                    x, y = cj + sx * RA * e, cl + sy * RA * e
                    d = float(np.linalg.norm(x - y))
                    if d > 1e-9 and on_arc(x, j) and on_arc(y, l):
                        dcs.append((d, ARCS[j][0], ARCS[l][0]))
    dcs.sort()
    P("    doubly-critical self-chords (exact): " + "; ".join("%.12f [%s,%s]" % t for t in dcs))
    P("      min = %.15f  (2(sqrt7-1) = %.15f)" % (dcs[0][0], 2 * (S7 - 1)))
    out["doubly_critical_self_chords"] = [dict(length=t[0], arcs=[t[1], t[2]]) for t in dcs]
    out["min_doubly_critical_self_distance"] = dcs[0][0]
    # non-local self distance with explicit arc-length cut-offs
    sN = (np.arange(4000) + 0.5) * LCOMP / 4000
    uvN, _, _ = curve_uv(sN)
    D = np.linalg.norm(uvN[:, None] - uvN[None], axis=2)
    sep = np.abs(sN[:, None] - sN[None])
    sep = np.minimum(sep, LCOMP - sep)
    nl = {}
    for cut in (math.pi, 2 * math.pi):
        nl["%.6f" % cut] = float(D[sep >= cut].min())
    P("    min self-distance over pairs with arc separation >= pi : %.9f ; >= 2pi : %.9f"
      % (nl["%.6f" % math.pi], nl["%.6f" % (2 * math.pi)]))
    out["min_selfdistance_by_arc_cutoff"] = nl
    # enclosing / central ball
    allD = np.linalg.norm(np.vstack([embed(uvD, c) for c in range(3)]), axis=1)
    P("    max |core| = %.15f (sqrt7+1 = %.15f) -> tube inside sphere radius %.15f (sqrt7+2)" % (allD.max(), S7 + 1, allD.max() + 1))
    P("    min |core| = %.15f (sqrt7-1 = %.15f) -> tube clears ball radius %.15f (sqrt7-2)" % (allD.min(), S7 - 1, allD.min() - 1))
    out.update(max_core_radius=float(allD.max()), min_core_radius=float(allD.min()),
               enclosing_sphere=float(allD.max() + 1), central_ball=float(allD.min() - 1))

    # ---- (d) linking numbers and piercing pattern ----------------------------
    P("")
    P("(d) Linking numbers (exact polygon solid-angle formula) and disc piercings")
    th_ = np.linspace(0, 2 * np.pi, 400, endpoint=False)
    circA = np.stack([np.cos(th_), np.sin(th_), 0 * th_], 1)
    circB = np.stack([1 + np.cos(th_), 0 * th_, np.sin(th_)], 1)
    circC = np.stack([5 + np.cos(th_), 0 * th_, np.sin(th_)], 1)
    P("    test: Hopf pair lk = %.12f ; separated pair lk = %.12f" % (lk_solid_angle(circA, circB), lk_solid_angle(circA, circC)))
    sP = (np.arange(1500) + 0.2718281828) * LCOMP / 1500
    uvP, _, _ = curve_uv(sP)
    poly = [embed(uvP, c) for c in range(3)]
    lks = {}
    for i in range(3):
        for j in range(i + 1, 3):
            lks["lk(C%d,C%d)" % (i + 1, j + 1)] = lk_solid_angle(poly[i], poly[j])
    P("    " + ", ".join("%s = %+.3e" % kv for kv in lks.items()))
    out["linking_numbers"] = lks
    pierce = {}
    for i in range(3):
        eu, ev = FRAMES[i]; nrm = NORMALS[i]
        for j in range(3):
            if j == i:
                continue
            Q = poly[j]; h = Q @ nrm; h2 = np.roll(h, -1)
            idx = np.nonzero(h * h2 < 0)[0]
            ev_ = []
            for k in idx:
                lam = h[k] / (h[k] - h2[k])
                X = Q[k] + lam * (Q[(k + 1) % len(Q)] - Q[k])
                q2 = np.array([X @ eu, X @ ev])
                ev_.append(dict(point=X.round(9).tolist(), inside=bool(winding(uvP, q2) != 0),
                                direction=int(np.sign(h2[k] - h[k]))))
            ins = [e for e in ev_ if e["inside"]]
            pierce["C%d through D%d" % (j + 1, i + 1)] = dict(
                plane_crossings=len(ev_), piercings=len(ins), signs=[e["direction"] for e in ins],
                signed_sum=int(sum(e["direction"] for e in ins)), points=[e["point"] for e in ins])
    for k_, v_ in pierce.items():
        P("    %s: plane crossings %d, disc piercings %d, signs %s, signed sum %d, at %s"
          % (k_, v_["plane_crossings"], v_["piercings"], v_["signs"], v_["signed_sum"], v_["points"]))
    out["piercings"] = pierce
    cyclic = all(pierce["C%d through D%d" % ((i + 1) % 3 + 1, i + 1)]["piercings"] == 2 and
                 pierce["C%d through D%d" % ((i + 1) % 3 + 1, i + 1)]["signed_sum"] == 0 and
                 pierce["C%d through D%d" % ((i + 2) % 3 + 1, i + 1)]["piercings"] == 0 for i in range(3))
    P("    cyclic pattern (D_i pierced twice, opposite signs, by C_(i+1) only): %s" % cyclic)
    out["cyclic_piercing_pattern"] = cyclic
    # isotopy to three perpendicular ellipses (semi-axes sqrt7-1 < sqrt7+1) by radial interpolation
    tq = np.linspace(-np.pi, np.pi, 4000, endpoint=False) + 1e-4
    ucheck = np.stack([radial_C(tq) * np.cos(tq), radial_C(tq) * np.sin(tq)], 1)
    rad_err = float(np.abs(dist_to_component(embed(ucheck, 0), 0)).max())
    iso = []
    for sv in np.linspace(0, 1, 41):
        rr = (1 - sv) * radial_C(tq) + sv * radial_E(tq)
        uvs = np.stack([rr * np.cos(tq), rr * np.sin(tq)], 1)
        comps = [embed(uvs, c) for c in range(3)]
        dm = min(float(cKDTree(comps[j]).query(comps[i])[0].min()) for i in range(3) for j in range(i + 1, 3))
        iso.append((float(sv), dm, float(rr.min())))
    P("    radial-graph check: max |radial_C point - curve| = %.2e" % rad_err)
    P("    isotopy r_s = (1-s) r_C + s r_E (ellipse semi-axes sqrt7-1, sqrt7+1; axis points fixed):")
    P("      min over s of min inter-component distance = %.6f ; min radius = %.6f ; at s=1 (ellipses) %.6f"
      % (min(t[1] for t in iso), min(t[2] for t in iso), iso[-1][1]))
    out["isotopy_to_ellipses"] = dict(min_intercomponent_distance_over_family=min(t[1] for t in iso),
                                      min_radius_over_family=min(t[2] for t in iso), samples=len(iso),
                                      radial_function_error=rad_err)
    out["_polys_for_T4"] = poly   # removed before JSON dump
    # ellipse configuration (s = 1), for the same Fox check
    tE = np.linspace(0, 2 * np.pi, 1500, endpoint=False) + 0.001
    uvE = np.stack([radial_E(tE) * np.cos(tE), radial_E(tE) * np.sin(tE)], 1)
    out["_polys_ellipse"] = [embed(uvE, c) for c in range(3)]

    # ---- (e) units -----------------------------------------------------------
    P("")
    P("(e) L per tube RADIUS   = %s" % ns(Ltot, 20))
    P("    L per tube DIAMETER = %s" % ns(Ltot / 2, 20))
    out["L_per_tube_radius"] = ns(Ltot, 20)
    out["L_per_tube_diameter"] = ns(Ltot / 2, 20)
    return out, Ltot


# =============================================================================
# T2 / T3  mass function
# =============================================================================
PHI_G = (1 + mp.sqrt(5)) / 2
BIGPHI = 2 * mp.pi - PHI_G ** 2 / (8 * mp.pi ** 2)
XI = 100 * PHI_G
M0 = mp.mpf("0.511") / mp.exp(2 * mp.pi / BIGPHI)
MP_PROTON = mp.mpf("938.272")


def reff(L):
    return 1 + mp.log(1 + L / XI)


def mass(aoz, L):
    return M0 * aoz * mp.exp(L / (BIGPHI * reff(L)))


def invert_lambertw(m, aoz):
    """L = xi (u-1), u = -c W_{-1}( -(1/c) e^{-1-1/c} ), c = Phi ln(m/(m0 A/Zf)) / xi."""
    K = mp.log(m / (M0 * aoz))
    c = K * BIGPHI / XI
    zarg = -(1 / c) * mp.exp(-1 - 1 / c)
    w = mp.lambertw(zarg, -1)
    assert abs(mp.im(w)) < mp.mpf(10) ** -40
    return XI * (-c * mp.re(w) - 1)


def invert_bisect(m, aoz, lo=mp.mpf(0), hi=mp.mpf(2000)):
    target = mp.log(m)
    for _ in range(200):
        mid = (lo + hi) / 2
        if mp.log(mass(aoz, mid)) > target:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2


def run_T2(Lt1):
    hdr("T2  Mass-formula inversions (DR-A3-2/3/4)")
    out = {}
    P("phi = %s" % ns(PHI_G, 25))
    P("Phi = 2 pi - phi^2/(8 pi^2) = %s" % ns(BIGPHI, 25))
    P("xi  = 100 phi = %s" % ns(XI, 25))
    P("m0  = 0.511/exp(2 pi/Phi) = %s MeV" % ns(M0, 25))
    P("note: m(A/Zf=1, L=2 pi) = %s MeV under the formula as stated (r_eff(2 pi) = %s, not 1)"
      % (ns(mass(1, 2 * mp.pi), 15), ns(reff(2 * mp.pi), 15)))
    out["m_at_Ae_1_L_2pi"] = ns(mass(1, 2 * mp.pi), 20)
    out.update(phi=ns(PHI_G, 30), Phi=ns(BIGPHI, 30), xi=ns(XI, 30), m0_MeV=ns(M0, 30))
    aoz = mp.mpf(20) / 6
    La = invert_lambertw(MP_PROTON, aoz)
    Lb = invert_bisect(MP_PROTON, aoz)
    P("")
    P("(a) L(m_p=938.272; A/Zf=20/6) = %s   [Lambert W_-1]" % ns(La, 25))
    P("                               = %s   [bisection]   |diff| = %s" % (ns(Lb, 25), ns(abs(La - Lb), 3)))
    P("    back-substitution m = %s MeV" % ns(mass(aoz, La), 20))
    P("    L - 60.194 = %s  (DR-A3-4 window +-0.001: %s)" % (ns(La - mp.mpf("60.194"), 10),
                                                            abs(La - mp.mpf("60.194")) <= mp.mpf("0.001")))
    out["a"] = dict(L=ns(La, 25), L_12=mp.nstr(La, 12), L_bisect=ns(Lb, 25), minus_60_194=ns(La - mp.mpf("60.194"), 12),
                    within_0p001_of_60_194=bool(abs(La - mp.mpf("60.194")) <= mp.mpf("0.001")),
                    rel_diff_from_60_194=float((La - mp.mpf("60.194")) / mp.mpf("60.194")))
    P("")
    m58 = mass(aoz, mp.mpf("58.006")); mT1 = mass(aoz, Lt1)
    P("(b) m(20,6, L=58.006)        = %s MeV  (m/m_p - 1 = %s)" % (ns(m58, 20), ns(m58 / MP_PROTON - 1, 8)))
    P("    m(20,6, L=T1=%s) = %s MeV  (m/m_p - 1 = %s)" % (ns(Lt1, 15), ns(mT1, 20), ns(mT1 / MP_PROTON - 1, 8)))
    out["b"] = dict(m_at_58_006=ns(m58, 20), m_at_T1_length=ns(mT1, 20),
                    rel_to_mp_58_006=float(m58 / MP_PROTON - 1), rel_to_mp_T1=float(mT1 / MP_PROTON - 1))
    P("")
    L80 = mp.mpf("80.95")
    aoz80 = MP_PROTON / (M0 * mp.exp(L80 / (BIGPHI * reff(L80))))
    cands = sorted({Fraction(p, q) for p in range(1, 21) for q in range(1, 21)},
                   key=lambda f: abs(mp.mpf(f.numerator) / f.denominator - aoz80))
    best = cands[0]
    Lbest = invert_lambertw(MP_PROTON, mp.mpf(best.numerator) / best.denominator)
    P("(c) A/Zf reproducing L=80.95 exactly: %s" % ns(aoz80, 20))
    P("    nearest p/q (p,q<=20): %s ; next: %s" % (best, ", ".join(
        "%s (%s)" % (f, ns(mp.mpf(f.numerator) / f.denominator - aoz80, 4)) for f in cands[1:4])))
    P("    L(m_p; A/Zf=%s) = %s ; rel diff from 80.95 = %s (%.5f %%)"
      % (best, ns(Lbest, 20), ns((Lbest - L80) / L80, 8), float((Lbest - L80) / L80) * 100))
    P("    (for reference 50 phi = xi/2 = %s ; 80.95/(xi/2) - 1 = %s)" % (ns(XI / 2, 15), ns(L80 / (XI / 2) - 1, 6)))
    out["c"] = dict(aoz_exact_for_80_95=ns(aoz80, 20), nearest_rational=str(best),
                    next_rationals=[str(f) for f in cands[1:4]], L_with_nearest=ns(Lbest, 20),
                    rel_diff_from_80_95=float((Lbest - L80) / L80),
                    within_0p1pct=bool(abs((Lbest - L80) / L80) < mp.mpf("0.001")),
                    xi_over_2=ns(XI / 2, 20), rel_80_95_vs_xi_over_2=float(L80 / (XI / 2) - 1))
    P("")
    aoz70 = mp.mpf(70) / 6
    L70 = invert_lambertw(MP_PROTON, aoz70)
    L70b = invert_bisect(MP_PROTON, aoz70)
    m70 = mass(aoz70, mp.mpf("58.006"))
    P("(d) L(m_p; A/Zf=70/6) = %s  (bisection %s)" % (ns(L70, 20), ns(L70b, 20)))
    P("    m(70,6, L=58.006) = %s MeV ; m(70,6, L=T1) = %s MeV" % (ns(m70, 20), ns(mass(aoz70, Lt1), 20)))
    out["d"] = dict(L_70_6=ns(L70, 20), L_70_6_12=mp.nstr(L70, 12), m_70_6_at_58_006=ns(m70, 20),
                    m_70_6_at_T1=ns(mass(aoz70, Lt1), 20))
    # monotonicity (uniqueness of the inversion)
    Ls = [mp.mpf(x) / 4 for x in range(1, 2000)]
    mono = all(mass(1, Ls[i + 1]) > mass(1, Ls[i]) for i in range(len(Ls) - 1))
    P("    m(L) strictly increasing on (0,500]: %s (inversion unique)" % mono)
    out["monotone"] = mono
    return out


def run_T3():
    hdr("T3  Mass table (DR-A3-7)")
    Lq = BIGPHI * PHI_G ** 2
    mW = M0 * PHI_G ** 27
    mZ = mW / mp.sqrt(1 - PHI_G ** -3)
    rows = [
        ("Up", "3", "3", "16.372", mass(mp.mpf(3) / 3, mp.mpf("16.372")), "2.039", "2.16", "0.07"),
        ("Down", "11", "9", "21.04", mass(mp.mpf(11) / 9, mp.mpf("21.04")), "4.589", "4.70", "0.07"),
        ("Charm", "5", "1/48", "23.60", mass(mp.mpf(5) * 48, mp.mpf("23.60")), "1245.7", "1273.0", "4.6"),
        ("Bottom", "119", "3/4", "37.31", mass(mp.mpf(119) * 4 / 3, mp.mpf("37.31")), "4162.6", "4183", "7"),
        ("Top", "119", "1/(8 phi^4)", "37.31", mass(119 * 8 * PHI_G ** 4, mp.mpf("37.31")), "171185", "172570", "290"),
        ("Tau", "3", "1/(2 pi)", "3 Phi phi^2 = %s" % ns(3 * Lq, 15), mass(3 * 2 * mp.pi, 3 * Lq), "1752.4", "1776.93", "0.09"),
        ("W", "-", "-", "m0 phi^27", mW, "82128", "80369.2", "13.3"),
        ("Z", "-", "-", "m_W/sqrt(1-phi^-3)", mZ, "93964", "91188.0", "2.0"),
    ]
    out = {"rows": []}
    P("%-7s %-26s %-22s %-10s %-10s %-9s | %-9s %-9s | %-9s %-9s | %-12s"
      % ("row", "inputs (A, Zf, L)", "recomputed", "printed", "rec/prt-1", ">0.1%?",
         "err% rec", "pull rec", "err% prt", "pull prt", "verdict"))
    for name, A, Zf, L, pred, prt, obs, sig in rows:
        prt_, obs_, sig_ = mp.mpf(prt), mp.mpf(obs), mp.mpf(sig)
        rd = pred / prt_ - 1
        e_rec, e_prt = (pred - obs_) / obs_, (prt_ - obs_) / obs_
        p_rec, p_prt = (pred - obs_) / sig_, (prt_ - obs_) / sig_

        def verdict(val, err):
            if name in ("W", "Z"):
                return "reported (>2%%: %s)" % ("yes" if abs(err) > mp.mpf("0.02") else "no")
            if name == "Up":
                inside = (obs_ - sig_) <= val <= (obs_ + sig_)
                return "NOT HOLDING" if not inside else "holds"
            return "NOT HOLDING" if abs(err) > mp.mpf("0.02") else "holds"

        v_rec, v_prt = verdict(pred, e_rec), verdict(prt_, e_prt)
        P("%-7s %-26s %-22s %-10s %+.3e %-9s | %+8.4f%% %+9.3f | %+8.4f%% %+9.3f | %s / %s"
          % (name, "%s, %s, %s" % (A, Zf, L if len(L) < 12 else L[:12]), ns(pred, 15), prt, float(rd),
             "FLAG" if abs(rd) > mp.mpf("0.001") else "ok", float(e_rec) * 100, float(p_rec),
             float(e_prt) * 100, float(p_prt), v_rec, v_prt))
        out["rows"].append(dict(name=name, A=A, Zf=Zf, L=L, recomputed=ns(pred, 20), printed=prt,
                                rel_recomputed_vs_printed=float(rd), flag_gt_0p1pct=bool(abs(rd) > mp.mpf("0.001")),
                                pdg=obs, sigma=sig, err_pct_recomputed=float(e_rec) * 100, pull_recomputed=float(p_rec),
                                err_pct_printed=float(e_prt) * 100, pull_printed=float(p_prt),
                                verdict_recomputed=v_rec, verdict_printed=v_prt,
                                up_1sigma_interval=[float(obs_ - sig_), float(obs_ + sig_)] if name == "Up" else None))
    P("Lq = Phi phi^2 = %s ; tau L = 3 Lq = %s" % (ns(Lq, 20), ns(3 * Lq, 20)))
    nh = [r["name"] for r in out["rows"] if r["verdict_recomputed"] == "NOT HOLDING"]
    nh2 = [r["name"] for r in out["rows"] if r["verdict_printed"] == "NOT HOLDING"]
    P("NOT HOLDING rows (recomputed): %s ; (printed): %s" % (nh, nh2))
    out["not_holding_recomputed"], out["not_holding_printed"] = nh, nh2
    out["Lq"], out["tau_L"] = ns(Lq, 20), ns(3 * Lq, 20)
    return out


# =============================================================================
# T4  Alexander polynomials by Fox calculus; Conway by skein; Burau
# =============================================================================
TV = sp.symbols("t1 t2 t3 t4")
T, Z = sp.symbols("t z")


def braid_components(word, n):
    perm = []
    for p in range(n):
        pos = p
        for a in word:
            i = abs(a)
            if pos == i - 1:
                pos = i
            elif pos == i:
                pos = i - 1
        perm.append(pos)
    seen, comps = [False] * n, []
    for p in range(n):
        if not seen[p]:
            cyc, q = [], p
            while not seen[q]:
                seen[q] = True; cyc.append(q); q = perm[q]
            comps.append(cyc)
    return perm, comps


def braid_wirtinger(word, n):
    """closed-braid diagram, strands run downward, positions 0..n-1 left to right.
    sigma_i (a=+i): strand at position i (0-based i) moves left OVER the strand moving right
    -> positive crossing (d_over x d_under > 0 toward the viewer). a=-i: the mirror crossing."""
    perm, comps = braid_components(word, n)
    comp_at = {}
    for ci, cyc in enumerate(comps):
        for p in cyc:
            comp_at[p] = ci
    parent = list(range(n)); arc_comp = [comp_at[p] for p in range(n)]
    cur, curc = list(range(n)), [comp_at[p] for p in range(n)]
    rels = []
    for a in word:
        i = abs(a); Lp, Rp = i - 1, i
        if a > 0:
            ov, uin, uc, oc = cur[Rp], cur[Lp], curc[Lp], curc[Rp]
            new = len(arc_comp); arc_comp.append(uc); parent.append(new)
            rels.append((new, ov, uin, +1))
            cur[Lp], cur[Rp], curc[Lp], curc[Rp] = ov, new, oc, uc
        else:
            ov, uin, uc, oc = cur[Lp], cur[Rp], curc[Rp], curc[Lp]
            new = len(arc_comp); arc_comp.append(uc); parent.append(new)
            rels.append((new, ov, uin, -1))
            cur[Rp], cur[Lp], curc[Rp], curc[Lp] = ov, new, oc, uc

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x
    for p in range(n):
        ra, rb = find(cur[p]), find(p)
        if ra != rb:
            parent[ra] = rb
    roots = sorted({find(x) for x in range(len(parent))})
    lab = {r_: k for k, r_ in enumerate(roots)}
    comp_of = [None] * len(roots)
    for x in range(len(parent)):
        k = lab[find(x)]
        assert comp_of[k] in (None, arc_comp[x])
        comp_of[k] = arc_comp[x]
    rels = [(lab[find(o)], lab[find(v)], lab[find(i)], s) for (o, v, i, s) in rels]
    return comp_of, rels, len(comps)


def fox_matrix(comp_of, rels, var):
    """relator  x_over^s x_in x_over^-s x_out^-1 ; abelianised Fox derivatives."""
    ng = len(comp_of)
    M = []
    for (o, v, i, s) in rels:
        word = [(v, s), (i, 1), (v, -s), (o, -1)]
        row = [sp.Integer(0)] * ng
        pref = sp.Integer(1)
        for g, e in word:
            tg = var[comp_of[g]]
            if e == 1:
                row[g] += pref; pref = pref * tg
            else:
                pref = pref / tg; row[g] -= pref
        M.append([sp.expand(x) for x in row])
    return M


def clear_rows(M):
    out = []
    for row in M:
        dens = [sp.fraction(sp.together(x))[1] for x in row]
        L = sp.lcm_list(dens) if dens else 1
        out.append([sp.expand(sp.cancel(x * L)) for x in row])
    return out


def normalize(expr, gens):
    expr = sp.together(sp.expand(expr))
    num, den = sp.fraction(expr)
    num = sp.expand(num)
    if num == 0:
        return sp.Integer(0)
    Pn = sp.Poly(num, *gens)
    mins = [min(m[k] for m in Pn.monoms()) for k in range(len(gens))]
    mono = sp.Mul(*[g ** k for g, k in zip(gens, mins)])
    q = sp.expand(sp.cancel(num / mono))
    if sp.Poly(q, *gens).LC() < 0:
        q = -q
    return sp.expand(q)


def minor_det(M, r0, c0):
    sub = [[M[i][j] for j in range(len(M[0])) if j != c0] for i in range(len(M)) if i != r0]
    return sp.expand(sp.Matrix(sub).det(method="berkowitz"))


def alexander_multivar(comp_of, rels, mu, all_minors=True):
    var = TV[:mu]
    M = clear_rows(fox_matrix(comp_of, rels, var))
    vals = set()
    first = None
    nr, nc = len(M), len(M[0])
    pairs = [(r0, c0) for r0 in range(nr) for c0 in range(nc)] if all_minors else \
        sorted({(0, 0), (nr - 1, nc - 1), (nr // 2, 0), (0, nc // 2)})
    for r0, c0 in pairs:
        if True:
            d = minor_det(M, r0, c0)
            if mu >= 2:
                q, rem = sp.div(sp.Poly(d, *var), sp.Poly(var[comp_of[c0]] - 1, *var))
                assert rem.is_zero, "minor not divisible by (t_c - 1)"
                d = q.as_expr()
            nd = normalize(d, var)
            vals.add(sp.srepr(nd))
            if first is None:
                first = nd
    assert len(vals) == 1, "minors disagree up to units"
    return first, M


def alexander_onevar(comp_of, rels):
    M = clear_rows(fox_matrix(comp_of, rels, [T] * (max(comp_of) + 1)))
    g = sp.Integer(0)
    for r0 in range(len(M)):
        for c0 in range(len(M[0])):
            g = sp.gcd(g, minor_det(M, r0, c0))
    return normalize(g, [T])


def first_bad_crossing(word, n):
    _, comps = braid_components(word, n)
    first, order = {}, []
    for cyc in comps:
        start = pos = cyc[0]
        while True:
            for idx, a in enumerate(word):
                i = abs(a)
                if pos == i - 1 or pos == i:
                    over = (pos == i) if a > 0 else (pos == i - 1)
                    if idx not in first:
                        first[idx] = over; order.append(idx)
                    pos = i if pos == i - 1 else i - 1
            if pos == start:
                break
    for idx in order:
        if not first[idx]:
            return idx, len(comps)
    return None, len(comps)


@lru_cache(maxsize=None)
def conway(word, n):
    """Conway polynomial: nabla(L+) - nabla(L-) = z nabla(L0); descending diagram = trivial link."""
    idx, nc = first_bad_crossing(word, n)
    if idx is None:
        return sp.Integer(1) if nc == 1 else sp.Integer(0)
    a = word[idx]
    sw = word[:idx] + (-a,) + word[idx + 1:]
    sm = word[:idx] + word[idx + 1:]
    return sp.expand(conway(sw, n) + (Z if a > 0 else -Z) * conway(sm, n))


def burau_alexander(word, n):
    """reduced Burau: Delta(closure) = (1-t)/(1-t^n) det(I - psi_r(beta)), up to units."""
    def gen(i):
        m = sp.eye(n - 1)
        k = i - 1
        if k - 1 >= 0:
            m[k, k - 1] = T
        m[k, k] = -T
        if k + 1 <= n - 2:
            m[k, k + 1] = 1
        return m
    G = {i: gen(i) for i in range(1, n)}
    B = sp.eye(n - 1)
    for a in word:
        B = B * (G[a] if a > 0 else G[-a].inv())
    d = sp.cancel((sp.eye(n - 1) - B).det() * (1 - T) / (1 - T ** n))
    return normalize(d, [T]), G


def coeffs(poly_expr, var):
    return [int(c) for c in sp.Poly(poly_expr, var).all_coeffs()]


def run_T4(polys_T1, polys_ell):
    hdr("T4  Alexander polynomials by Fox calculus (DR-A3-5)")
    out = {}
    tests = [("unknot s1 (B2)", (1,), 2), ("trefoil s1^3 (B2)", (1, 1, 1), 2),
             ("figure-eight (s1 s2^-1)^2", (1, -2, 1, -2), 3), ("Hopf s1^2", (1, 1), 2),
             ("T(2,4) s1^4", (1, 1, 1, 1), 2), ("Whitehead s1 s2^-1 s1 s2^-2", (1, -2, 1, -2, -2), 3)]
    P("Validation on known links (Fox multivariable | Fox one-variable | Conway skein | Burau):")
    val = []
    for nm, w, n in tests:
        comp_of, rels, mu = braid_wirtinger(w, n)
        dm, _ = alexander_multivar(comp_of, rels, mu)
        d1 = alexander_onevar(comp_of, rels)
        cz = conway(w, n)
        bu, _ = burau_alexander(w, n)
        P("  %-30s mu=%d  Delta=%s | %s | nabla=%s | %s" % (nm, mu, sp.factor(dm), sp.factor(d1), cz, sp.factor(bu)))
        val.append(dict(link=nm, word=list(w), mu=mu, multivar=str(sp.factor(dm)), onevar=str(sp.factor(d1)),
                        conway=str(cz), burau=str(sp.factor(bu))))
    out["validation"] = val
    # ---- Borromean rings ----------------------------------------------------------
    w = (1, -2, 1, -2, 1, -2)
    comp_of, rels, mu = braid_wirtinger(w, 3)
    P("")
    P("Borromean rings = closure of (s1 s2^-1)^3 in B3: %d arcs, %d crossings, %d components" % (len(comp_of), len(rels), mu))
    P("Wirtinger presentation (generator x_k = meridian of arc k; arc -> component):")
    P("  arcs: " + ", ".join("x%d->C%d" % (k + 1, c + 1) for k, c in enumerate(comp_of)))
    pres = []
    for (o, v, i, s) in rels:
        txt = "x%d = x%d%s x%d x%d%s   (crossing sign %+d)" % (o + 1, v + 1, "" if s > 0 else "^-1", i + 1, v + 1,
                                                                "^-1" if s > 0 else "", s)
        pres.append(txt); P("  " + txt)
    out["wirtinger_presentation"] = dict(arcs_to_component=[c + 1 for c in comp_of], relations=pres)
    dm, M = alexander_multivar(comp_of, rels, mu)
    P("Fox Jacobian (abelianised, rows cleared of negative powers):")
    for row in M:
        P("  [" + ", ".join(str(x) for x in row) + "]")
    dmf = sp.factor(dm)
    P("(a) Delta(t1,t2,t3) = %s  = %s   (same for all 36 choices of deleted row/column)" % (dm, dmf))
    t1, t2, t3 = TV[:3]
    sym = normalize(dm.subs({t1: 1 / t1, t2: 1 / t2, t3: 1 / t3}), [t1, t2, t3])
    P("    symmetry Delta(1/t) ~ Delta(t): %s ; Torres Delta(t1,t2,1) = %s" % (sp.expand(sym - dm) == 0, sp.expand(dm.subs(t3, 1))))
    dd = normalize(dm.subs({t1: T, t2: T, t3: T}), [T])
    P("(b) Delta(t,t,t) = %s = %s ; coefficients %s" % (dd, sp.factor(dd), coeffs(dd, T)))
    d1 = alexander_onevar(comp_of, rels)
    P("(c) Delta_L(t) = gcd of all 36 (n-1)-minors at t_i = t = %s = %s ; coefficients %s" % (d1, sp.factor(d1), coeffs(d1, T)))
    torres = sp.expand(d1 - normalize((T - 1) * dd, [T])) == 0
    P("    Torres: Delta_L(t) == (t-1) Delta(t,t,t) up to units: %s" % torres)
    ssq_dd = sum(c * c for c in coeffs(dd, T)); ssq_d1 = sum(c * c for c in coeffs(d1, T))
    P("(d) sum of squared coefficients: Delta(t,t,t) -> %d ; Delta_L(t) -> %d" % (ssq_dd, ssq_d1))
    cz = conway(w, 3)
    conv_alex = normalize(sp.expand(cz.subs(Z, sp.sqrt(T) - 1 / sp.sqrt(T)) * T ** 4), [T])
    bu, G = burau_alexander(w, 3)
    braid_rel = sp.simplify(G[1] * G[2] * G[1] - G[2] * G[1] * G[2]) == sp.zeros(2, 2)
    P("Cross-checks: Conway (skein recursion on descending diagrams) nabla(z) = %s" % cz)
    P("    nabla(t^1/2 - t^-1/2) normalised = %s ; equals Delta_L: %s" % (sp.factor(conv_alex), sp.expand(conv_alex - d1) == 0))
    P("    reduced Burau (braid relation holds: %s): Delta = %s ; equals Delta_L: %s"
      % (braid_rel, sp.factor(bu), sp.expand(bu - d1) == 0))
    out.update(multivariable=str(dm), multivariable_factored=str(dmf), symmetric=bool(sp.expand(sym - dm) == 0),
               delta_ttt=str(dd), delta_ttt_factored=str(sp.factor(dd)), delta_ttt_coeffs=coeffs(dd, T),
               delta_L=str(d1), delta_L_factored=str(sp.factor(d1)), delta_L_coeffs=coeffs(d1, T),
               torres_holds=bool(torres), sumsq_delta_ttt=ssq_dd, sumsq_delta_L=ssq_d1,
               conway=str(cz), conway_matches=bool(sp.expand(conv_alex - d1) == 0),
               burau=str(sp.factor(bu)), burau_matches=bool(sp.expand(bu - d1) == 0))
    # ---- the T1 geometry itself: projection -> Wirtinger -> Fox ---------------------------
    P("")
    P("T1 geometry cross-check: generic projection of the actual 3-D curves -> Wirtinger -> Fox")
    geo = {}
    for label, polys in (("four-arc configuration", polys_T1), ("three perpendicular ellipses", polys_ell)):
        for view in ((1.0, 1.013, 0.987), (0.31, -0.77, 0.56)):
            arc_comp, rr, X = diagram_from_polygons(polys, view)
            dmv, _ = alexander_multivar(arc_comp, rr, 3, all_minors=False)
            same = sp.expand(dmv - dm) == 0
            lkp = {}
            for i in range(3):
                for j in range(i + 1, 3):
                    lkp["%d%d" % (i + 1, j + 1)] = sum(x["sign"] for x in X if {x["oc"], x["uc"]} == {i, j}) / 2
            P("  %-30s view %-20s crossings %2d  min depth gap %.4f  min sin(angle) %.3f  Delta = %s  same as braid: %s  lk %s"
              % (label, str(view), len(X), min(x["gap"] for x in X), min(x["sin_angle"] for x in X),
                 sp.factor(dmv), same, lkp))
            geo["%s %s" % (label, view)] = dict(crossings=len(X), delta=str(sp.factor(dmv)), same_as_braid=bool(same),
                                               lk_from_crossings=lkp, min_depth_gap=min(x["gap"] for x in X))
            # 2-component sublinks of the projected diagram
            if view == (1.0, 1.013, 0.987):
                for drop in range(3):
                    keep = [c for c in range(3) if c != drop]
                    ac2, rr2, X2 = diagram_from_polygons([polys[c] for c in keep], view)
                    d2, _ = alexander_multivar(ac2, rr2, 2, all_minors=False)
                    geo["%s sublink without C%d" % (label, drop + 1)] = str(d2)
                    P("      sublink without C%d: Delta(t1,t2) = %s" % (drop + 1, d2))
    out["projection_check"] = geo
    return out


def run_summary(t1o, t2o, t3o, t4o, Lt1):
    """Applies the locked DR-A3 rules to the numbers above. Provenance facts (which ledger text
    derives which value; the units of Paper VII E.1.1) are taken from A3_PREREG.md's quotations,
    not from the ledger itself, which this leg did not open."""
    hdr("SUMMARY: numbers -> locked rules (as implied by this leg's numbers)")
    out = {}
    L58006 = mp.mpf("58.006")
    U = min(L58006, Lt1)
    within = t1o["within_0p2pct_of_58_05"]
    P("DR-A3-1  four-arc length %s ; within 0.2%% of 58.05: %s -> 58.05 and 58.006 are per unit tube RADIUS"
      % (mp.nstr(Lt1, 12), within))
    P("         Paper VII E.1.1 quoted in prereg as 'L/R (arc-length divided by tube radius)' -> UNITS MATCH")
    out["DR-A3-1"] = dict(L_fourarc=mp.nstr(Lt1, 15), within_0p2pct=within,
                          verdict="UNITS MATCH (given prereg's quotation of E.1.1)")
    c1 = U < mp.mpf("59.894")
    c2 = Lt1 < mp.mpf("58.005")
    P("DR-A3-2  U = min(58.006, %s) = %s ; U < 59.894: %s -> verification (1) %s -> %s"
      % (mp.nstr(Lt1, 10), mp.nstr(U, 10), c1, "FAILS" if c1 else "passes",
         "RETRACTS to Conjecture status" if c1 else "no retraction"))
    P("         (diameter convention, for completeness: U/2 = %s < 59.894: %s)" % (mp.nstr(U / 2, 8), U / 2 < mp.mpf("59.894")))
    P("         clause 2: configuration shorter than 58.005 computed here: %s -> %s"
      % (c2, "fires" if c2 else "not triggered as written (58.006 is an upper bound on the minimum, not a lower bound)"))
    P("         m_p(20/6) at L=58.006: %s MeV ; at L=%s: %s MeV" % (t2o["b"]["m_at_58_006"][:12], mp.nstr(Lt1, 10),
                                                                  t2o["b"]["m_at_T1_length"][:12]))
    out["DR-A3-2"] = dict(U=mp.nstr(U, 10), clause1="FAILS -> RETRACTS to Conjecture status" if c1 else "passes",
                          clause2="not triggered as written" if not c2 else "fires")
    rel60 = t2o["a"]["rel_diff_from_60_194"]
    rel80 = t2o["c"]["rel_diff_from_80_95"]
    cls = {"60.194": "(I) inversion with A/Zf = 20/6 = 10/3 (rel. diff %.2e)" % rel60,
           "58.05": "(G) explicit embedded four-arc configuration, length %s" % mp.nstr(Lt1, 10),
           "80.95": "(I) inversion with A/Zf = %s (rel. diff %.2e)" % (t2o["c"]["nearest_rational"], rel80)}
    for k_, v_ in cls.items():
        P("DR-A3-3  %-7s %s   [%s U = %s]" % (k_, v_, "above" if mp.mpf(k_) > U else "not above", mp.nstr(U, 6)))
    P("         (I) values retired as lengths. Shortest (G) among the three = 58.05 (four-arc, %s);"
      % mp.nstr(Lt1, 10))
    P("         58.006 (CFKSW B0, quoted, not computed here) is shorter, so the ideal minimum <= 58.006.")
    out["DR-A3-3"] = cls
    w4 = t2o["a"]["within_0p001_of_60_194"]
    P("DR-A3-4  L(m_p; 20/6) - 60.194 = %s ; within +-0.001: %s -> %s"
      % (t2o["a"]["minus_60_194"][:12], w4,
         "proton 0.000% and neutron -0.138% are calibration outputs (annotation)" if w4 else "no annotation"))
    out["DR-A3-4"] = dict(within=w4)
    P("DR-A3-5  sum sq coeff: Delta(t,t,t) = %d ; Delta_L(t) = %d -> %s"
      % (t4o["sumsq_delta_ttt"], t4o["sumsq_delta_L"],
         "differ: annotate 'A = 20' with both; 20 is the diagonal Delta(t,t,t) without the Torres factor (t-1)"
         if t4o["sumsq_delta_ttt"] != t4o["sumsq_delta_L"] else "equal"))
    out["DR-A3-5"] = dict(sumsq_delta_ttt=t4o["sumsq_delta_ttt"], sumsq_delta_L=t4o["sumsq_delta_L"])
    P("DR-A3-7  NOT HOLDING rows (recomputed) %s ; (printed) %s ; any row >0.1%% off print: %s"
      % (t3o["not_holding_recomputed"], t3o["not_holding_printed"], any(r["flag_gt_0p1pct"] for r in t3o["rows"])))
    for r in t3o["rows"]:
        if r["name"] in ("W", "Z"):
            P("         %s error %+.4f%% (pull %+.1f) -- reported" % (r["name"], r["err_pct_recomputed"], r["pull_recomputed"]))
    out["DR-A3-7"] = dict(not_holding=t3o["not_holding_recomputed"])
    return out


def main():
    t1o, Lt1 = run_T1()
    t2o = run_T2(Lt1)
    t3o = run_T3()
    t4o = run_T4(t1o.pop("_polys_for_T4"), t1o.pop("_polys_ellipse"))
    RES["T1"], RES["T2"], RES["T3"], RES["T4"] = t1o, t2o, t3o, t4o
    RES["implied_by_rules"] = run_summary(t1o, t2o, t3o, t4o, Lt1)
    RES["meta"]["runtime_s"] = round(time.time() - T_START, 1)
    with open(os.path.join(HERE, "leg2_results.json"), "w") as f:
        json.dump(RES, f, indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))
    hdr("done in %.1f s; wrote leg2_results.json" % (time.time() - T_START))


if __name__ == "__main__":
    main()
