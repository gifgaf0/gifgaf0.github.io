#!/usr/bin/env python3
"""A3 first leg: the matter sector (ropelength units and check, proton lengths, inversion, Alexander convention, mass table).

Locked pre-registration: A3_PREREG.md md5 e2f1090cac3b097c0d2d205146c8b67c.
Methods (chosen to differ from the blind second leg where a choice exists):
  - four-arc length: closed form 48*arctan(sqrt 7) plus a sampled-polyline length with Richardson extrapolation;
  - tube embedding: KD-tree nearest distances on dense samples, then local refinement on arc parameters;
    doubly-critical self-distance by local minimisation from a grid of starts;
  - linking numbers: exact signed-crossing count in a generic projection of the polygons;
  - inversions: Newton's method with the analytic derivative;
  - Alexander polynomials: Fox calculus on the 3-generator closed-braid presentation (Artin action) of (s1 s2^-1)^3,
    plus the reduced Burau formula for the one-variable polynomial.
"""
import json, math, hashlib, itertools, sys
import numpy as np
from scipy.spatial import cKDTree
from scipy.optimize import minimize
import sympy as sp

HERE = "/home/claude/gifgaf0.github.io/audit_followup/A3_matter"
assert hashlib.md5(open(HERE + "/A3_PREREG.md", "rb").read()).hexdigest() == "e2f1090cac3b097c0d2d205146c8b67c"
OUT = {}
def say(*a):
    print(*a, flush=True)

# ---------------------------------------------------------------------------------------------------------------
# 1. Four-arc Borromean configuration (DR-A3-1)
# ---------------------------------------------------------------------------------------------------------------
r7 = math.sqrt(7.0)
a, b, R = r7 + 1.0, r7 - 1.0, 2.0           # half-diagonals (major along x, minor along y), arc radius = contact distance
beta = math.atan2(b, a)                      # = arctan(sqrt7) - pi/4
# component C1 in z = 0: lobes (convex) about (0, +-b), waists (concave) about (+-a, 0); tangent points at side midpoints
arcs = [  # (centre, start angle, signed sweep)  -- counter-clockwise traversal of the curve
    ((0.0,  b), -beta,           math.pi + 2*beta),   # top lobe: from M(a/2,b/2) over (0,b+2) to M(-a/2,b/2)
    ((-a, 0.0),  beta,          -2*beta),             # left waist: through (-b,0)
    ((0.0, -b),  math.pi - beta, math.pi + 2*beta),   # bottom lobe: through (0,-b-2)
    (( a, 0.0),  math.pi + beta, -2*beta),            # right waist: through (b,0)
]
def arc_points(n_per_rad):
    pts, tans = [], []
    for (cx, cy), th0, sw in arcs:
        m = max(8, int(abs(sw) * n_per_rad))
        th = th0 + sw * np.arange(m) / m
        pts.append(np.stack([cx + R*np.cos(th), cy + R*np.sin(th), 0*th], 1))
        s = np.sign(sw)
        tans.append(np.stack([-s*np.sin(th), s*np.cos(th), 0*th], 1))
    return np.vstack(pts), np.vstack(tans)
# continuity check at the joins (positions and tangents)
joins = []
for k in range(4):
    (cx, cy), th0, sw = arcs[k]; (dx, dy), ph0, sw2 = arcs[(k + 1) % 4]
    p_end = np.array([cx + R*math.cos(th0 + sw), cy + R*math.sin(th0 + sw)])
    p_beg = np.array([dx + R*math.cos(ph0), dy + R*math.sin(ph0)])
    s1, s2 = np.sign(sw), np.sign(sw2)
    t_end = np.array([-s1*math.sin(th0 + sw), s1*math.cos(th0 + sw)])
    t_beg = np.array([-s2*math.sin(ph0), s2*math.cos(ph0)])
    joins.append((float(np.linalg.norm(p_end - p_beg)), float(np.linalg.norm(t_end - t_beg))))
sigma = lambda P: P[:, [2, 0, 1]]           # (x,y,z) -> (z,x,y)
L_comp_closed = 16 * math.atan(r7)
L_total_closed = 48 * math.atan(r7)
alt_form = 12*math.pi + 24*math.asin(0.75)
say("=== DR-A3-1  four-arc Borromean configuration (tube radius 1, arc radius 2)")
say(f"  join gaps (position, tangent): {[(f'{p:.1e}', f'{t:.1e}') for p, t in joins]}")
say(f"  per-arc sweeps (deg): lobe {math.degrees(math.pi + 2*beta):.6f}, waist {math.degrees(2*beta):.6f}")
say(f"  component length 16*arctan(sqrt7) = {L_comp_closed:.12f};  total 48*arctan(sqrt7) = {L_total_closed:.12f}")
say(f"  identity check: 48 atan(sqrt7) - (12 pi + 24 asin(3/4)) = {L_total_closed - alt_form:.2e}")
# polyline length with Richardson extrapolation
lens = []
for npr in (200, 400, 800):
    P, _ = arc_points(npr); Pc = np.vstack([P, P[:1]])
    lens.append(float(np.linalg.norm(np.diff(Pc, axis=0), axis=1).sum()))
rich = lens[2] + (lens[2] - lens[1]) / 3.0
say(f"  polyline component lengths {lens} -> Richardson {rich:.12f} (closed {L_comp_closed:.12f}, diff {rich - L_comp_closed:.1e})")
OUT["four_arc"] = dict(component_length=L_comp_closed, total_length_per_radius=L_total_closed,
                       total_length_per_diameter=L_total_closed/2, polyline_richardson_component=rich,
                       vs_CKS02_5805_rel=(L_total_closed - 58.05)/58.05, vs_58006_rel=(L_total_closed - 58.006)/58.006,
                       lobe_sweep_deg=math.degrees(math.pi + 2*beta), waist_sweep_deg=math.degrees(2*beta))

# embedding checks
P1, T1 = arc_points(2000)
C = [P1, sigma(P1), sigma(sigma(P1))]
dmin_inter = []
for i, j in ((0, 1), (1, 2), (0, 2)):
    d, _ = cKDTree(C[j]).query(C[i])
    dmin_inter.append(float(d.min()))
say(f"  min inter-component distance on dense samples (KD-tree): {[f'{x:.9f}' for x in dmin_inter]}")
# refine the inter-component minimum on exact arcs: param (arc k, angle) for C1 vs arc for C2
def arc_pt(k, t, which):
    (cx, cy), th0, sw = arcs[k]; th = th0 + sw*t
    p = np.array([cx + R*math.cos(th), cy + R*math.sin(th), 0.0])
    return p if which == 0 else (np.array([p[2], p[0], p[1]]) if which == 1 else np.array([p[1], p[2], p[0]]))
best = 1e9
for k1 in range(4):
    for k2 in range(4):
        for t1 in np.linspace(0, 1, 9):
            for t2 in np.linspace(0, 1, 9):
                f = lambda x: float(np.linalg.norm(arc_pt(k1, min(max(x[0], 0), 1), 0) - arc_pt(k2, min(max(x[1], 0), 1), 1)))
                r = minimize(f, [t1, t2], method="Nelder-Mead", options=dict(xatol=1e-12, fatol=1e-14, maxiter=4000))
                best = min(best, r.fun)
say(f"  refined min distance C1-C2 over exact arcs: {best:.12f}  (contact distance 2 => tube radius 1)")
# contact structure: distance from each sampled point of C1 to C2 and C3 (should be >= 2 everywhere, = 2 on contact arcs)
d12, _ = cKDTree(C[1]).query(C[0]); d13, _ = cKDTree(C[2]).query(C[0])
frac_contact = float(np.mean(np.minimum(d12, d13) < 2 + 1e-3))
say(f"  fraction of C1 samples within 1e-3 of contact with C2 or C3: {frac_contact:.4f}")
# doubly-critical self-distance of one component (non-local): local minimisation of |g(s)-g(t)| from a grid, |s-t| large
Pd, Td = arc_points(400); n = len(Pd)
sarc = np.linspace(0, 1, n, endpoint=False)
D = np.linalg.norm(Pd[:, None, :] - Pd[None, :, :], axis=2)
ii, jj = np.meshgrid(np.arange(n), np.arange(n), indexing="ij")
sep = np.minimum(np.abs(ii - jj), n - np.abs(ii - jj)) * (L_comp_closed / n)
cand = []
for cut in (math.pi, 0.25*L_comp_closed):
    M = np.where(sep >= cut, D, np.inf)
    cand.append(float(M.min()))
# doubly-critical pairs: chord perpendicular to both tangents, away from the diagonal
crit = []
for p in range(0, n, 3):
    for q in range(p + n//8, p + n - n//8, 3):
        q %= n
        v = Pd[q] - Pd[p]; dv = np.linalg.norm(v)
        if dv < 1e-9: continue
        if abs(np.dot(v, Td[p]))/dv < 0.02 and abs(np.dot(v, Td[q]))/dv < 0.02:
            crit.append(dv)
dc = float(min(crit)) if crit else float("nan")
say(f"  component self-distance: min over arc-separation >= pi: {cand[0]:.6f}; >= L/4: {cand[1]:.6f}; "
    f"min doubly-critical chord (approx) {dc:.4f}  (2(sqrt7-1) = {2*b:.6f})")
OUT["embedding"] = dict(min_inter_component_kdtree=dmin_inter, min_inter_component_refined=best, curvature_radius=2.0,
                        self_dist_sep_ge_pi=cand[0], self_dist_sep_ge_quarter=cand[1], doubly_critical_min=dc,
                        doubly_critical_exact=2*b, link_thickness=best/2, frac_contact=frac_contact,
                        enclosing_radius_centerline=float(max(np.linalg.norm(P1, axis=1))),
                        central_ball_centerline=float(min(np.linalg.norm(P1, axis=1))))
say(f"  centerline max |x| = {OUT['embedding']['enclosing_radius_centerline']:.9f} (sqrt7+1 = {r7+1:.9f}); "
    f"min |x| = {OUT['embedding']['central_ball_centerline']:.9f} (sqrt7-1 = {r7-1:.9f})")

# linking numbers: exact signed crossings in a generic projection
def linking_number(A, B, direction):
    d = direction/np.linalg.norm(direction)
    e1 = np.cross(d, [0.3, 0.5, 0.7]); e1 /= np.linalg.norm(e1); e2 = np.cross(d, e1)
    def proj(X): return np.stack([X @ e1, X @ e2], 1), X @ d
    A2, Ah = proj(A); B2, Bh = proj(B)
    An, Bn = np.roll(A2, -1, 0), np.roll(B2, -1, 0); Ahn, Bhn = np.roll(Ah, -1), np.roll(Bh, -1)
    tot = 0
    for i in range(len(A2)):
        p, r = A2[i], An[i] - A2[i]
        q, s = B2, Bn - B2
        rxs = r[0]*s[:, 1] - r[1]*s[:, 0]
        qp = q - p
        with np.errstate(divide="ignore", invalid="ignore"):
            t = (qp[:, 0]*s[:, 1] - qp[:, 1]*s[:, 0]) / rxs
            u = (qp[:, 0]*r[1] - qp[:, 1]*r[0]) / rxs
        hit = (np.abs(rxs) > 1e-14) & (t >= 0) & (t < 1) & (u >= 0) & (u < 1)
        for k in np.nonzero(hit)[0]:
            hA = Ah[i] + t[k]*(Ahn[i] - Ah[i]); hB = Bh[k] + u[k]*(Bhn[k] - Bh[k])
            sign = np.sign(rxs[k]) * (1 if hA > hB else -1)
            tot += sign
    return tot / 2.0
Pl, _ = arc_points(60)
Cl = [Pl, sigma(Pl), sigma(sigma(Pl))]
lk = {f"{i+1}{j+1}": float(linking_number(Cl[i], Cl[j], np.array([0.137, 0.291, 0.947]))) for i, j in ((0, 1), (1, 2), (0, 2))}
say(f"  linking numbers (signed crossings, generic projection): {lk}")
# piercing pattern: where does C_j cross the plane of C_i, inside or outside C_i's region?
from matplotlib.path import Path as MPath
def region_path(i):
    P, _ = arc_points(400)
    return MPath(P[:, :2])
pierce = {}
plane_axes = {0: (2, (0, 1)), 1: (0, (1, 2)), 2: (1, (2, 0))}   # C1 in z=0 (x,y); C2 = sigma(C1) in x=0 (y,z); C3 in y=0 (z,x)
base = region_path(0)
for i in range(3):
    ax_n, (u, v) = plane_axes[i]
    for j in range(3):
        if i == j: continue
        X = Cl[j]; Xn = np.roll(X, -1, 0)
        h, hn = X[:, ax_n], Xn[:, ax_n]
        cr = np.nonzero((h >= 0) != (hn >= 0))[0]          # half-open sides: a sample exactly on the plane is counted once
        res = []
        for k in cr:
            t = h[k] / (h[k] - hn[k]); p = X[k] + t*(Xn[k] - X[k])
            res.append((round(float(p[u]), 6), round(float(p[v]), 6), bool(base.contains_point((p[u], p[v]))), int(np.sign(hn[k] - h[k]))))
        pierce[f"C{j+1} through plane of C{i+1}"] = res
for k, v in pierce.items():
    say(f"  {k}: {v}")
OUT["linking"] = lk; OUT["piercing"] = {k: [list(x) for x in v] for k, v in pierce.items()}

# ---------------------------------------------------------------------------------------------------------------
# 2. Mass function, inversions (DR-A3-2/3/4)
# ---------------------------------------------------------------------------------------------------------------
phi = (1 + math.sqrt(5)) / 2
PHI = 2*math.pi - phi**2/(8*math.pi**2)
XI = 100*phi
M0_EXACT = 0.511 / math.exp(2*math.pi/PHI)
reff = lambda L: 1 + math.log(1 + L/XI)
def mass(AZ, L, m0=M0_EXACT): return m0*AZ*math.exp(L/(PHI*reff(L)))
def invert(AZ, m, m0=M0_EXACT):
    L = 60.0                                    # Newton on g(L) = L/(PHI reff(L)) - ln(m/(m0 AZ))
    target = math.log(m/(m0*AZ))
    for _ in range(100):
        r = reff(L); g = L/(PHI*r) - target
        dg = (r - L/(XI + L)) / (PHI*r*r)
        step = g/dg; L -= step
        if abs(step) < 1e-15: break
    return L
mp = 938.272
say("\n=== DR-A3-2/3/4  mass-formula numbers")
say(f"  Phi = {PHI:.12f}; xi_vac = {XI:.9f}; m0 = 0.511/exp(2pi/Phi) = {M0_EXACT:.12f} MeV")
L_B = invert(20/6, mp); L_B_rounded_m0 = invert(20/6, mp, 0.18699)
say(f"  L(m_p; A/Zf = 20/6) = {L_B:.10f} (exact m0); {L_B_rounded_m0:.10f} (m0 = 0.18699 as in sqt_open_problem_5.py)")
mp_58006 = mass(20/6, 58.006); mp_4arc = mass(20/6, L_total_closed)
say(f"  m(20/6, L=58.006) = {mp_58006:.6f} MeV ({100*(mp_58006/mp - 1):+.3f}%);  m(20/6, L={L_total_closed:.4f}) = {mp_4arc:.6f} MeV ({100*(mp_4arc/mp - 1):+.3f}%)")
AZ_8095 = mp / (M0_EXACT*math.exp(80.95/(PHI*reff(80.95))))
best_pq = min(((p, q) for p in range(1, 21) for q in range(1, 21)), key=lambda pq: (abs(pq[0]/pq[1] - AZ_8095), pq[1]))
L_half = invert(best_pq[0]/best_pq[1], mp)
say(f"  A/Zf reproducing L = 80.95: {AZ_8095:.10f}; nearest p/q (<=20) = {best_pq[0]}/{best_pq[1]}; invert -> L = {L_half:.8f} "
    f"(rel diff from 80.95 {(L_half - 80.95)/80.95:+.2e}); xi_vac/2 = {XI/2:.6f}")
L_A70 = invert(70/6, mp); m_A70 = mass(70/6, 58.006)
say(f"  A = 70 (one-variable Alexander): L(m_p) = {L_A70:.8f}; m(70/6, 58.006) = {m_A70:.4f} MeV")
say(f"  electron check: m(1, 2pi) with the continuum r_eff = {mass(1, 2*math.pi):.6f} MeV (r_eff(2pi) = {reff(2*math.pi):.6f}; "
    f"the definitional r_eff = 1 gives 0.511)")
OUT["mass"] = dict(PHI=PHI, xi_vac=XI, m0_exact=M0_EXACT, L_B_inverted=L_B, L_B_inverted_m0_018699=L_B_rounded_m0,
                   m_p_at_58006=mp_58006, m_p_at_four_arc=mp_4arc, AZ_for_8095=AZ_8095, nearest_pq=list(best_pq),
                   L_inverted_nearest_pq=L_half, xi_vac_half=XI/2, L_inverted_A70=L_A70, m_at_58006_A70=m_A70,
                   m_e_continuum_reff=mass(1, 2*math.pi))
# verdict mechanics
U = min(58.006, L_total_closed)
OUT["verdicts"] = dict(U=U, verification1_window=[60.194 - 0.3, 60.194 + 0.3], verification1_fails=bool(U < 59.894),
                       U_diameter=U/2, verification1_fails_diameter=bool(U/2 < 59.894),
                       clause2_fires=bool(L_total_closed < 58.006 - 0.001),
                       paper_vii_E13_row=("[58.006, 59.894): prediction falsified at leading order" if 58.006 <= 58.006 < 59.894 else "?"),
                       L_B_within_0p001=bool(abs(L_B - 60.194) <= 1e-3) or bool(abs(L_B_rounded_m0 - 60.194) <= 1e-3))
say(f"  U = {U:.6f} < 59.894: verification (1) FAILS = {OUT['verdicts']['verification1_fails']}; clause 2 fires = {OUT['verdicts']['clause2_fires']}")

# ---------------------------------------------------------------------------------------------------------------
# 3. Alexander polynomials by Fox calculus on the closed-braid presentation (DR-A3-5)
# ---------------------------------------------------------------------------------------------------------------
say("\n=== DR-A3-5  Alexander polynomials of the Borromean rings = closure of (s1 s2^-1)^3")
# free-group words: list of (gen, exp) with gen in 0..2
def inv(w): return [(g, -e) for g, e in reversed(w)]
def red(w):
    out = []
    for x in w:
        if out and out[-1][0] == x[0] and out[-1][1] == -x[1]: out.pop()
        else: out.append(x)
    return out
def apply(aut, w):                      # aut: dict gen -> word (image of x_gen)
    res = []
    for g, e in w:
        res += aut[g] if e == 1 else inv(aut[g])
    return red(res)
X = lambda g: [(g, 1)]
def sigma_aut(i, sgn):                  # Artin action of s_i^{+-1}
    aut = {g: X(g) for g in range(3)}
    if sgn == 1:
        aut[i] = red(X(i) + X(i + 1) + inv(X(i))); aut[i + 1] = X(i)
    else:
        aut[i] = X(i + 1); aut[i + 1] = red(inv(X(i + 1)) + X(i) + X(i + 1))
    return aut
word = [(0, 1), (1, -1)] * 3                      # s1 s2^-1 s1 s2^-1 s1 s2^-1
images = {g: X(g) for g in range(3)}
for (i, sgn) in word:                             # compose: beta = s_{i1} o s_{i2} o ... applied to generators
    a_ = sigma_aut(i, sgn)
    images = {g: apply(a_, images[g]) for g in range(3)}
# permutation of the closure: strand components from abelianisation of images (each image is conjugate of some x_j)
perm = {g: [h for h, e in images[g] if True] for g in range(3)}
t = sp.symbols("t1 t2 t3"); T = sp.symbols("t")
# component of strand g: the image of x_g is a conjugate of x_{pi(g)}; components = cycles of pi
def exponent_sum(w):
    s = [0, 0, 0]
    for g, e in w: s[g] += e
    return s
pi_map = {}
for g in range(3):
    es = exponent_sum(images[g]); j = [k for k in range(3) if es[k] == 1 and sum(es) == 1]
    pi_map[g] = j[0] if j else None
say(f"  braid permutation on strands: {pi_map}  (identity => 3 components)")
comp = {0: 0, 1: 1, 2: 2}
ab = lambda g: t[comp[g]]
def fox(w, j):                                    # Fox derivative d w / d x_j, abelianised
    res = sp.Integer(0); pref = sp.Integer(1)
    for g, e in w:
        if e == 1:
            if g == j: res += pref
            pref = pref*ab(g)
        else:
            pref = pref/ab(g)
            if g == j: res -= pref
    return sp.expand(res)
rels = [red(images[g] + inv(X(g))) for g in range(3)]   # relations beta(x_g) x_g^-1
Amat = sp.Matrix(3, 3, lambda r, c: fox(rels[r], c))
minors = {}
for dr in range(3):
    for dc in range(3):
        M = Amat.copy(); M.row_del(dr); M.col_del(dc)
        minors[(dr, dc)] = sp.factor(sp.simplify(M.det()))
say("  2x2 minors of the Alexander matrix (row deleted, column deleted):")
for k, v in minors.items():
    say(f"    {k}: {v}")
# Torres/Fox: minor(dr, dc) = +- monomial * (t_{c(dc)} - 1) * Delta(t1,t2,t3) * (t_{c(dr)}-1)/(t_{c(dr)}-1) ... extract Delta
m00 = minors[(0, 0)]
Delta = sp.factor(sp.cancel(m00 / (t[comp[0]] - 1)))
# normalise away units +- monomials
def strip_units(expr, syms):
    num, den = sp.fraction(sp.factor(expr))
    f = sp.factor_list(num)
    keep = sp.Integer(1)
    for fac, mult in f[1]:
        if fac.is_Symbol or (fac.is_Pow and fac.base.is_Symbol): continue
        if sp.Poly(fac, *syms).is_monomial: continue
        keep *= fac**mult
    return sp.expand(keep)
Delta_n = strip_units(Delta, t)
say(f"  multivariable Delta(t1,t2,t3) (up to units) = {sp.factor(Delta_n)}")
diag = sp.expand(Delta_n.subs({t[0]: T, t[1]: T, t[2]: T}))
one_var_torres = sp.expand((T - 1)*diag)
# one-variable directly: all meridians -> t in the Alexander matrix, normalised (n-1)-minor
A1 = Amat.subs({t[0]: T, t[1]: T, t[2]: T})
M = A1.copy(); M.row_del(0); M.col_del(0)
one_var_direct = strip_units(sp.factor(M.det()), [T])
# reduced Burau: Delta(t) = (1 - t)/(1 - t^3) * det(I - psi(beta))
def burau_red(i, sgn):
    if i == 0:
        Bm = sp.Matrix([[-T, 1], [0, 1]])
    else:
        Bm = sp.Matrix([[1, 0], [T, -T]])
    return Bm if sgn == 1 else Bm.inv()
Bw = sp.eye(2)
for (i, sgn) in word: Bw = Bw*burau_red(i, sgn)
burau = sp.factor(sp.simplify((1 - T)/(1 - T**3) * (sp.eye(2) - Bw).det()))
burau_n = strip_units(burau, [T])
coef = lambda p: [int(c) for c in sp.Poly(p, T).all_coeffs()]
sq = lambda p: sum(c*c for c in coef(p))
say(f"  Delta(t,t,t) = {sp.factor(diag)}  coefficients {coef(diag)}  sum of squares {sq(diag)}")
say(f"  one-variable (Torres (t-1)Delta(t,t,t)) = {sp.factor(one_var_torres)}  coefficients {coef(one_var_torres)}  sum of squares {sq(one_var_torres)}")
say(f"  one-variable (direct minor, units stripped) = {sp.factor(one_var_direct)};  reduced Burau = {sp.factor(burau_n)}")
OUT["alexander"] = dict(multivariable=str(sp.factor(Delta_n)), diag=str(sp.factor(diag)), diag_coeffs=coef(diag),
                        diag_sum_sq=sq(diag), one_var=str(sp.factor(one_var_torres)), one_var_coeffs=coef(one_var_torres),
                        one_var_sum_sq=sq(one_var_torres), one_var_direct=str(sp.factor(one_var_direct)),
                        burau=str(sp.factor(burau_n)),
                        agree=bool(sp.simplify(one_var_direct - one_var_torres) == 0 or sp.simplify(one_var_direct + one_var_torres) == 0)
                              and bool(sp.simplify(burau_n - one_var_torres) == 0 or sp.simplify(burau_n + one_var_torres) == 0))

# ---------------------------------------------------------------------------------------------------------------
# 4. Mass table (DR-A3-7)
# ---------------------------------------------------------------------------------------------------------------
say("\n=== DR-A3-7  mass table: reproduction and PDG 2024")
Lq = PHI*phi**2
rows = [  # name, A, Zf, L, printed prediction, PDG 2024 (value, sigma)
    ("up",     3,   3,                  16.372, 2.039,    (2.16, 0.07)),
    ("down",   11,  9,                  21.04,  4.589,    (4.70, 0.07)),
    ("charm",  5,   1/48,               23.60,  1245.7,   (1273.0, 4.6)),
    ("bottom", 119, 3/4,                37.31,  4162.6,   (4183.0, 7.0)),
    ("top",    119, 1/(8*phi**4),       37.31,  171185.0, (172570.0, 290.0)),
    ("tau",    3,   1/(2*math.pi),      3*Lq,   1752.4,   (1776.93, 0.09)),
]
table = []
for name, A_, Zf, L, printed, (obs, sig) in rows:
    pred = mass(A_/Zf, L)
    table.append(dict(row=name, A=A_, Zf=Zf, L=L, pred=pred, printed=printed, rel_vs_printed=(pred - printed)/printed,
                      pdg=obs, sigma=sig, err_pct=100*(pred - obs)/obs, err_pct_printed=100*(printed - obs)/obs,
                      pull=(pred - obs)/sig))
mW = M0_EXACT*phi**27; mZ = mW/math.sqrt(1 - phi**-3)
for name, pred, printed, (obs, sig) in (("W", mW, 82128.0, (80369.2, 13.3)), ("Z", mZ, 93964.0, (91188.0, 2.0))):
    table.append(dict(row=name, pred=pred, printed=printed, rel_vs_printed=(pred - printed)/printed, pdg=obs, sigma=sig,
                      err_pct=100*(pred - obs)/obs, err_pct_printed=100*(printed - obs)/obs, pull=(pred - obs)/sig))
for r_ in table:
    flag = ""
    if r_["row"] == "up":
        flag = "NOT HOLDING (outside PDG 2024 1-sigma)" if abs(r_["pred"] - r_["pdg"]) > r_["sigma"] else "holds"
    elif r_["row"] in ("W", "Z"):
        flag = "reported"
    else:
        flag = "NOT HOLDING (>2%)" if abs(r_["err_pct"]) > 2.0 else "within 2%"
    r_["rule"] = flag
    say(f"  {r_['row']:6s} pred {r_['pred']:12.4f} (printed {r_['printed']}, rel {r_['rel_vs_printed']:+.1e})  PDG24 {r_['pdg']} +- {r_['sigma']}"
        f"  err {r_['err_pct']:+.3f}% (printed {r_['err_pct_printed']:+.3f}%)  pull {r_['pull']:+.1f}  -> {flag}")
OUT["mass_table"] = table
OUT["dof"] = dict(rows=8, per_row_selected_continuous=["Zf(up)=3", "Zf(down)=9", "Zf(charm)=1/48", "Zf(bottom)=3/4",
                                                        "Zf(top)=kappa/8", "Zf(tau)=1/2pi", "W exponent 27", "Z angle sin^2=phi^-3"],
                  shared_selected=["xi_vac = 100 phi"],
                  discrete_shared=["r_eff(2pi) := 1 normalisation (the 3.81% slack; a common ~3.8% factor on every row)"],
                  discrete_per_row=["knot assignment", "A convention (crossing number for up; Alexander sum of squares otherwise; "
                                    "Delta(t,t,t) for the proton)", "L thickness convention (lead)"])
OUT["dof"]["residual"] = OUT["dof"]["rows"] - len(OUT["dof"]["per_row_selected_continuous"]) - len(OUT["dof"]["shared_selected"])
say(f"  degrees of freedom: {OUT['dof']['rows']} rows - {len(OUT['dof']['per_row_selected_continuous'])} per-row selected inputs "
    f"- {len(OUT['dof']['shared_selected'])} shared continuous selection = {OUT['dof']['residual']} "
    f"(discrete selections listed separately, not counted)")

# ---------------------------------------------------------------------------------------------------------------
# 5. Reconnection: the size of the protection a Borromean baryon would need (DR-A3-6; order of magnitude only)
# ---------------------------------------------------------------------------------------------------------------
yr = 365.25*86400.0
tau_p = 2.4e34*yr                                   # Super-K, tau/B(p -> e+ pi0) > 2.4e34 yr (90% CL)
l_P, c_light, hbar_MeVs = 1.616255e-35, 2.99792458e8, 6.582119569e-22
nu_core = c_light/(0.358*l_P)                       # V4.40's xi_phys = 0.358 l_P, at speed c
nu_had = 938.272/hbar_MeVs                          # m_p c^2 / hbar
S_core, S_had = math.log(nu_core*tau_p), math.log(nu_had*tau_p)
say(f"\n=== DR-A3-6  required suppression exp(-S) < 1/(nu tau_p), tau_p > 2.4e34 yr = {tau_p:.3e} s")
say(f"  core rate c/xi_phys = {nu_core:.3e} /s -> S >= {S_core:.1f};  hadronic rate m_p c^2/hbar = {nu_had:.3e} /s -> S >= {S_had:.1f}")
OUT["reconnection"] = dict(tau_p_s=tau_p, nu_core=nu_core, S_core=S_core, nu_had=nu_had, S_had=S_had)
json.dump(OUT, open(HERE + "/a3_results.json", "w"), indent=1, default=float)
json.dump(OUT, open(HERE + "/a3_results.json", "w"), indent=1, default=float)
say("\ndone")
