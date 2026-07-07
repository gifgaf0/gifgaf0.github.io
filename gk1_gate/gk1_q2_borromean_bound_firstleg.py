#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
G-k1 Q2 (chat-side first leg): the channel-(iii) bound on canon's Borromean
representative (three perpendicular golden ellipses, a=phi, b=1/phi;
sec 3.4-G2 / sec 3.09).  FLAG: the pre-reg names the CKS tight configuration;
this leg uses canon's exactly-specifiable standing representative, with the
CKS-exact evaluation assigned to the second leg.

Per the LSF-amended law: local line tension (xi units, rho*Gamma^2/4pi = 1)
    T(s) = ln( R_cut(s) ) + C,
    R_cut(s) = min( c1 / (xi*kappa(s)),  c2 * d(s) )
with kappa(s) the curvature, d(s) the nearest other-strand distance
(screening), c1 ~ 8 (isolated-ring value), c2 ~ 1; sensitivity over both.
C = 0.3810 (Q1b, GP kernel; kernel-conditional).

Outputs: thickness of the configuration; xi*kappa and d distributions;
T stats (mean, dispersion, range); the tight-unknot reference
T_ref = ln(c1) + C (a ring at xi*kappa = 1); delta = Tbar/T_ref - 1;
near-cusp (Jones-Roberts) arclength fraction; sensitivity table.
"""
import numpy as np

phi = (1 + np.sqrt(5))/2
a, b = phi, 1/phi
C_CORE = 0.3810

# --- build the three golden ellipses ------------------------------------
M = 3000
t = np.linspace(0, 2*np.pi, M, endpoint=False)
E3 = np.stack([a*np.cos(t), b*np.sin(t), 0*t], 1)
E1 = np.stack([0*t, a*np.cos(t), b*np.sin(t)], 1)
E2 = np.stack([b*np.sin(t), 0*t, a*np.cos(t)], 1)
strands = [E1, E2, E3]

# analytic curvature of (a cos t, b sin t)
kappa = a*b / (a*a*np.sin(t)**2 + b*b*np.cos(t)**2)**1.5     # same for each strand
ds = np.sqrt(a*a*np.sin(t)**2 + b*b*np.cos(t)**2) * (2*np.pi/M)  # arclength element
L_one = ds.sum()

# --- distances: nearest OTHER-strand distance per point ------------------
def min_dist_to(P, Q):
    # chunked cdist
    out = np.empty(len(P))
    for i in range(0, len(P), 500):
        d = np.linalg.norm(P[i:i+500, None, :] - Q[None, :, :], axis=2)
        out[i:i+500] = d.min(axis=1)
    return out

d_other = min_dist_to(strands[0], np.vstack([strands[1], strands[2]]))
# by symmetry (cyclic C3) the distribution is the same on each strand; verify on strand 2
d_other_2 = min_dist_to(strands[1], np.vstack([strands[0], strands[2]]))

# nonadjacent self-distance: genuinely OPPOSITE arcs only (arc separation >
# 25% of perimeter). A small index window misclassifies the two flanks of the
# high-curvature vertex as self-contact; for a CONVEX planar curve the bend
# flanks are governed by the curvature constraint, and the only true
# self-contact scale is across the interior (~2b). (First-run bug, corrected.)
P = strands[2]
self_min = np.inf
for i in range(0, M, 4):
    idx = (np.arange(M) - i) % M
    mask = (idx > M//4) & (idx < 3*M//4)
    self_min = min(self_min, np.linalg.norm(P[i] - P[mask], axis=1).min())

# --- thickness of the configuration --------------------------------------
r_curv_min = 1.0/kappa.max()
tau = min(r_curv_min, d_other.min()/2.0, self_min/2.0)
print("="*70)
print("G-k1 Q2: golden-ellipse Borromean, channel-(iii) bound (first leg)")
print("="*70)
print(f" min curvature radius        = {r_curv_min:.4f}   (= 1/phi^3? {1/phi**3:.4f})")
print(f" min inter-strand distance   = {d_other.min():.4f}  (/2 = {d_other.min()/2:.4f})")
print(f" min nonadjacent self-dist   = {self_min:.4f}  (/2 = {self_min/2:.4f})")
print(f" thickness tau = min of the three constraints = {tau:.4f}")
lim = ("curvature" if tau == r_curv_min else
       ("inter-strand contact" if tau == d_other.min()/2 else "self-contact"))
print(f" -> thickness-limiting constraint: {lim}")

# --- scale: tube radius = xi = tau ---------------------------------------
xk = kappa * tau                    # xi * kappa(s), in (0, 1]
dd = d_other / tau                  # distances in xi units
L_xi = 3 * L_one / tau              # total length in xi units
print(f"\n xi*kappa(s): min {xk.min():.4f}, max {xk.max():.4f}  (spread x{xk.max()/xk.min():.1f})")
print(f" d(s)/xi    : min {dd.min():.3f}, max {dd.max():.3f}")
print(f" total ropelength L/xi = {L_xi:.2f}   (per-strand {L_one/tau:.2f})")

frac_near_cusp = ds[xk > 0.5].sum()/L_one
print(f" near-cusp (Jones-Roberts) arclength fraction (xi*kappa > 0.5): {frac_near_cusp:.1%}")

# --- tension field and the bound -----------------------------------------
def tension_stats(c1, c2):
    Rcut = np.minimum(c1/xk, c2*dd)
    Rcut = np.maximum(Rcut, 2.0)          # floor: cutoff can't be inside the core
    T = np.log(Rcut) + C_CORE
    Tbar = (T*ds).sum()/L_one
    Tstd = np.sqrt(((T-Tbar)**2*ds).sum()/L_one)
    T_ref = np.log(c1) + C_CORE           # tight unknot: ring at xi*kappa = 1
    return Tbar, Tstd, T.min(), T.max(), T_ref

print("\n sensitivity table  (delta = Tbar/T_ref - 1; disp = Tstd/Tbar)")
print("  c1    c2   |  Tbar    Tmin   Tmax  | disp    delta_vs_unknot")
for c1 in (4.0, 8.0, 16.0):
    for c2 in (0.5, 1.0, 2.0):
        Tbar, Tstd, Tmin, Tmax, T_ref = tension_stats(c1, c2)
        print(f"  {c1:4.0f}  {c2:3.1f}  | {Tbar:6.3f} {Tmin:6.3f} {Tmax:6.3f} |"
              f" {Tstd/Tbar:6.1%}   {Tbar/T_ref-1:+7.1%}")

# headline case c1=8, c2=1
Tbar, Tstd, Tmin, Tmax, T_ref = tension_stats(8.0, 1.0)
print(f"\n HEADLINE (c1=8, c2=1):")
print(f"  mean tension Tbar = {Tbar:.3f}, dispersion = {Tstd/Tbar:.1%}, range [{Tmin:.3f}, {Tmax:.3f}]")
print(f"  tight-unknot reference T_ref = {T_ref:.3f}")
print(f"  delta (knot-dependent tension shift vs unknot) = {Tbar/T_ref-1:+.1%}")
print(f"  internal dispersion of T along the strand      = {Tstd/Tbar:.1%}")
print(f"  -> compare against the 0.03 ratio budget (pre-reg D2 threshold)")
print("\n NOTE (for the fold, not a decision here): canon's mass formula is")
print(" exponential in L (exp(L/Phi r_eff)); a knot-dependent tension shift maps")
print(" to an effective-length shift dL/L ~ delta, which the exponential")
print(" amplifies by L/(Phi*xi) e-folds -- the effective budget on delta may be")
print(" FAR tighter than 3%. Flagged; requires reading against sec 2.14's actual")
print(" consumption of L before any verdict is drawn from it.")
