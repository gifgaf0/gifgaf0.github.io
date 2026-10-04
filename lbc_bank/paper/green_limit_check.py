#!/usr/bin/env python3
"""Green's (incompressible) limit of the zero-temperature supersolid hydrodynamics of Sec. 3.

Plain-language summary: if the condensate is made nearly incompressible, one longitudinal
sound runs off to infinite speed and the other (second sound) settles at c_*. This script
checks where c_* sits relative to the shear speed c_T, what mechanical stability forces on
it, and what the Cosserat-supersolid proposal's own parameters (f_s = 4/5, crystalline
K/mu = 5/3, K_sf/mu ~ 3e40) give.

Checks (all symbolic unless marked numeric):
 1. Plane waves of the Sec. 3 Lagrangian give the dispersion polynomial quoted in the paper.
 2. alpha -> oo at fixed gamma: c_-^2 -> c_*^2 = rho_s M / (rho rho_n); c_+^2 ~ rho alpha.
 3. alpha -> oo with gamma = g sqrt(alpha): c_-^2 -> rho_s (M - g^2) / (rho rho_n).
 4. c_*^2 / c_T^2 = f_s M / mu, with c_T^2 = mu / rho_n and f_s = rho_s / rho.
 5. Isotropic d-dim lattice: M = K + 2(d-1)mu/d; stability (alpha K > gamma^2, mu > 0) gives
    M - gamma^2/alpha > 2(d-1)mu/d, so in Green's limit c_-^2/c_T^2 > 2(d-1) f_s / d.
    Guaranteed c_- > c_T iff f_s >= d/(2(d-1)): 3/4 in 3D, 1 in 2D.
 6. Numeric (mpmath, 60 digits): Cox mapping, finite K_sf/mu = 3.0e40, gamma = 0 and the
    marginal-stability gamma; and his stated range 0.49 <= f_s <= 0.98.
"""
import json, sys
import sympy as sp
import mpmath as mp

out = {}

# ---------- 1. dispersion from the Lagrangian ----------
t, x = sp.symbols('t x', real=True)
rho_s, rho_n, alpha, gam, M, mu, V = sp.symbols('rho_s rho_n alpha gamma M mu V', positive=True)
rho = rho_s + rho_n
w, q = sp.symbols('omega q', positive=True)
th = sp.Function('theta')(t, x); dr = sp.Function('dr')(t, x); u = sp.Function('u')(t, x)
L = (-dr*sp.diff(th, t) - rho/2*sp.diff(th, x)**2 + rho_n/2*(sp.diff(u, t) - sp.diff(th, x))**2
     - alpha/2*dr**2 - gam*dr*sp.diff(u, x) - M/2*sp.diff(u, x)**2)
from sympy.calculus.euler import euler_equations
eqs = euler_equations(L, [th, dr, u], [t, x])
A, B, C = sp.symbols('A B C')
sub = {th: A*sp.exp(sp.I*(q*x - w*t)), dr: B*sp.exp(sp.I*(q*x - w*t)), u: C*sp.exp(sp.I*(q*x - w*t))}
rows = []
for e in eqs:
    ex = sp.simplify((e.lhs - e.rhs).subs(sub).doit() / sp.exp(sp.I*(q*x - w*t)))
    rows.append([sp.expand(ex).coeff(v) for v in (A, B, C)])
Mat = sp.Matrix(rows)
det = sp.factor(sp.simplify(Mat.det()))
X = sp.symbols('X', positive=True)  # X = omega^2/q^2
poly_paper = rho_n*X**2 - (M + rho*rho_n*alpha - 2*rho_n*gam)*X + rho_s*(alpha*M - gam**2)
detX = sp.simplify(det.subs(w, sp.sqrt(X)*q))
ratio = sp.simplify(detX / poly_paper)
out['1_dispersion_matches_paper'] = bool(sp.simplify(sp.diff(ratio, X)) == 0 and ratio != 0)
out['1_ratio_det_over_paper_poly'] = str(ratio)

# ---------- 2. Green's limit at fixed gamma ----------
a = rho*alpha - 2*gam + M/rho_n
b = (rho_s/rho_n)*(alpha*M - gam**2)
cm2 = (a - sp.sqrt(a**2 - 4*b))/2
cp2 = (a + sp.sqrt(a**2 - 4*b))/2
lim_m = sp.limit(cm2, alpha, sp.oo)
cstar2 = rho_s*M/(rho*rho_n)
out['2_lim_cminus2_fixed_gamma'] = str(sp.simplify(lim_m))
out['2_equals_cstar2'] = bool(sp.simplify(lim_m - cstar2) == 0)
out['2_lim_cplus2_over_rho_alpha'] = str(sp.limit(cp2/(rho*alpha), alpha, sp.oo))

# ---------- 3. Green's limit with gamma = g sqrt(alpha) ----------
g = sp.symbols('g', positive=True)
cm2g = cm2.subs(gam, g*sp.sqrt(alpha))
lim_mg = sp.limit(cm2g, alpha, sp.oo)
out['3_lim_cminus2_gamma_scaling'] = str(sp.simplify(lim_mg))
out['3_equals_rho_s(M-g^2)/(rho rho_n)'] = bool(sp.simplify(lim_mg - rho_s*(M - g**2)/(rho*rho_n)) == 0)

# ---------- 4. ratio to the shear speed ----------
cT2 = mu/rho_n
fs = sp.symbols('f_s', positive=True)
r = sp.simplify((cstar2/cT2).subs(rho_s, fs*(rho_s + rho_n)))
r = sp.simplify(r.subs(rho_n, sp.Symbol('rn', positive=True)))
out['4_cstar2_over_cT2'] = str(sp.simplify(cstar2/cT2))
out['4_equals_fs_M_over_mu'] = bool(sp.simplify(cstar2/cT2 - (rho_s/rho)*M/mu) == 0)

# ---------- 5. isotropic stability bound ----------
d, K = sp.symbols('d K', positive=True)
lam = K - 2*mu/d                     # Lame lambda at fixed density
M_iso = sp.simplify(lam + 2*mu)      # uniaxial modulus C_xxxx
out['5_M_iso'] = str(M_iso)
out['5_M_iso_equals_K_plus_2(d-1)mu/d'] = bool(sp.simplify(M_iso - (K + 2*(d - 1)*mu/d)) == 0)
# dilatation block energy: (alpha/2) dr^2 + gamma dr e + (K/2) e^2 -> positive definite iff alpha>0, K>0, alpha K > gamma^2
dr_, e_ = sp.symbols('dr e')
Q = alpha/2*dr_**2 + gam*dr_*e_ + K/2*e_**2
H = sp.hessian(Q, (dr_, e_))
out['5_dilatation_block_det'] = str(sp.factor(H.det()))
# Green-limit c_-^2 / c_T^2 = f_s (M - gamma^2/alpha)/mu = f_s (K - gamma^2/alpha + 2(d-1)mu/d)/mu  >  2(d-1) f_s/d
thr = sp.solve(sp.Eq(2*(d - 1)*fs/d, 1), fs)[0]
out['5_threshold_fs_general'] = str(sp.simplify(thr))
out['5_threshold_fs_3D'] = str(thr.subs(d, 3))
out['5_threshold_fs_2D'] = str(thr.subs(d, 2))

# ---------- 6. numbers: the Cosserat-supersolid mapping ----------
mp.mp.dps = 60
def lower_speed2(fs_, M_over_mu, Ksf_over_mu, gamma_frac):
    """rho = 1, c_T = 1 (mu = rho_n). gamma = gamma_frac * sqrt(alpha * K_lat) (0 = no coupling, ->1 marginal)."""
    rho_ = mp.mpf(1); rn = 1 - mp.mpf(fs_); rs = mp.mpf(fs_)
    mu_ = rn                                  # c_T^2 = mu/rho_n = 1
    M_ = mp.mpf(M_over_mu)*mu_
    K_lat = M_ - mp.mpf(4)/3*mu_              # 3D isotropic
    alpha_ = mp.mpf(Ksf_over_mu)*mu_/rho_**2  # K_sf = rho^2 alpha
    gam_ = mp.mpf(gamma_frac)*mp.sqrt(alpha_*K_lat)
    a_ = rho_*alpha_ - 2*gam_ + M_/rn
    b_ = (rs/rn)*(alpha_*M_ - gam_**2)
    disc = mp.sqrt(a_**2 - 4*b_)
    return (a_ - disc)/2 if a_ > 0 else None, (a_ + disc)/2
res = {}
for fs_ in ('0.80', '0.49', '0.75', '0.98'):
    for gf in ('0', '0.999999'):
        cm2n, cp2n = lower_speed2(fs_, 3, '3.0e40', gf)
        res[f'fs={fs_},gamma_frac={gf}'] = dict(c_minus_over_cT=float(mp.sqrt(cm2n)), c_plus_over_cT=float(mp.sqrt(cp2n)))
out['6_cox_mapping_numeric'] = res
out['6_closed_forms_3D'] = {
    'fs=4/5, M=3mu, gamma=0: sqrt(f_s M/mu)': float(mp.sqrt(mp.mpf('0.8')*3)),
    'fs=4/5, stability floor: sqrt(4 f_s/3)': float(mp.sqrt(mp.mpf('0.8')*4/3)),
    'fs=0.49..0.98, M=3mu, gamma=0': [float(mp.sqrt(3*mp.mpf('0.49'))), float(mp.sqrt(3*mp.mpf('0.98')))],
    'fs=0.49..0.98, stability floor': [float(mp.sqrt(mp.mpf(4)/3*mp.mpf('0.49'))), float(mp.sqrt(mp.mpf(4)/3*mp.mpf('0.98')))],
}
# 6b. General d (added after the two-leg comparison; it is the substitution d -> 2, 3, 4 into the
# bound 2(d-1) f_s/d and threshold d/(2(d-1)) that both legs derived): the floor at f_s = 4/5.
out['6b_general_d'] = {f'd={dd}': dict(threshold_fs=str(sp.Rational(dd, 2*(dd - 1))),
                                       floor_at_fs_4_5=float(mp.sqrt(mp.mpf(2*(dd - 1))/dd*mp.mpf('0.8'))))
                       for dd in (2, 3, 4)}
json.dump(out, sys.stdout, indent=1, default=str)
print()
ok = (out['1_dispersion_matches_paper'] and out['2_equals_cstar2'] and out['3_equals_rho_s(M-g^2)/(rho rho_n)']
      and out['4_equals_fs_M_over_mu'] and out['5_M_iso_equals_K_plus_2(d-1)mu/d']
      and out['5_threshold_fs_3D'] == '3/4' and out['5_threshold_fs_2D'] == '1')
print('ALL SYMBOLIC CHECKS PASS' if ok else 'SOME CHECK FAILED')
sys.exit(0 if ok else 1)
