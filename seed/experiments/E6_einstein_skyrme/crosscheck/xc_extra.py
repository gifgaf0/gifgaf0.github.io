#!/usr/bin/env python3
"""
Extra cross-check items (isotropic-gauge spectral solutions, xc_iso.py):
  1. both branches at alpha = 0.04037 (the continuation driver stepped over this pair),
     reached from the fold solution along the pseudo-arclength branch;
  2. upper branch -> Bartnik-McKinnon: extrapolation of sqrt(alpha) m(inf) to alpha = 0 with several
     fit forms, and b_BM = b^2 alpha / 2 (w = cos F = -1 + b^2 x^2/2, x = sqrt(alpha) y);
  3. flat-profile diagnostics quoted in the report: p_r >= 0 everywhere, p_r/rho at the centre.
"""
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import xc_iso as X

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'out')
res = {}

# ---- 1. alpha = 0.04037 on both branches
z = np.load(os.path.join(OUT, 'xc_fold_U.npy'))
NL = np.load(os.path.join(OUT, 'xc_fold_grid.npy'))
g = X.Grid(int(NL[0]), float(NL[1]))
U0, a0 = z[:-1], z[-1]
W = 100.0
J = X.jac(U0, a0, g); J[:, -1] /= W
t = np.linalg.svd(J)[2][-1]
if X.central(U0 + 1e-4 * t[:-1], g)['b_schw'] < X.central(U0, g)['b_schw']:
    t = -t
Y0 = np.concatenate([U0, [a0 * W]])


def on_branch(h):
    Yp = Y0 + h * t
    Yh, ok = X.corrector(Yp.copy(), t, Yp, g, W)
    return Yh[:-1], Yh[-1] / W


target = 0.04037
for side, sgn in (('lower', -1), ('upper', +1)):
    lo, hi = 0.0, sgn * 0.02
    while on_branch(hi)[1] > target:
        hi *= 1.5
    for k in range(80):
        hm = 0.5 * (lo + hi)
        Uh, ah = on_branch(hm)
        if ah > target:
            lo = hm
        else:
            hi = hm
        if abs(hi - lo) < 1e-13:
            break
    Us, ok = X.newton(Uh, target, g)
    c = X.central(Us, g); mm = X.masses(Us, target, g)
    res['alpha_0.04037_' + side] = dict(b_schw=c['b_schw'], m_int=mm['m_int'], m_adm_tail=mm['m_adm_tail'], A0=c['A0'])
    print('alpha=0.04037 %s: b=%.6f m=%.7f (adm tail %.7f) A0=%.6f' % (side, c['b_schw'], mm['m_int'], mm['m_adm_tail'], c['A0']))

# ---- 2. Bartnik-McKinnon limit
up = json.load(open(os.path.join(OUT, 'xc_upper.json')))
al = np.array([r['alpha'] for r in up]); sm = np.array([r['sqrt_alpha_m'] for r in up])
bb = np.array([r['b_schw'] for r in up])
bBM = bb ** 2 * al / 2
sel = al <= 3.1e-4
fits = {}
A = np.vstack([np.ones(sel.sum()), al[sel]]).T
fits['linear_alpha<=3e-4'] = float(np.linalg.lstsq(A, sm[sel], rcond=None)[0][0])
A = np.vstack([np.ones(sel.sum()), np.sqrt(al[sel]), al[sel]]).T
fits['1,sqrt(a),a_alpha<=3e-4'] = float(np.linalg.lstsq(A, sm[sel], rcond=None)[0][0])
sel2 = al <= 1.1e-3
A = np.vstack([np.ones(sel2.sum()), np.sqrt(al[sel2]), al[sel2]]).T
fits['1,sqrt(a),a_alpha<=1e-3'] = float(np.linalg.lstsq(A, sm[sel2], rcond=None)[0][0])
A = np.vstack([np.ones(sel2.sum()), al[sel2], al[sel2] * np.log(al[sel2])]).T
fits['1,a,a*log(a)_alpha<=1e-3'] = float(np.linalg.lstsq(A, sm[sel2], rcond=None)[0][0])
A = np.vstack([np.ones(sel.sum()), np.sqrt(al[sel]), al[sel]]).T
fits['bBM_1,sqrt(a),a'] = float(np.linalg.lstsq(A, bBM[sel], rcond=None)[0][0])
A = np.vstack([np.ones(sel.sum()), al[sel]]).T
fits['bBM_linear'] = float(np.linalg.lstsq(A, bBM[sel], rcond=None)[0][0])
res['BM'] = dict(alpha=al.tolist(), sqrt_alpha_m=sm.tolist(), bBM_est=bBM.tolist(), extrapolations=fits,
                 literature_BM_n1=dict(m=0.828648, b=0.453716, source='Bartnik-McKinnon 1988; standard value (Volkov-Gal\'tsov review) quoted from memory, not re-read'))
for a_, s_, b_ in zip(al, sm, bBM):
    print('upper alpha=%.1e sqrt(a) m=%.7f  b^2 a/2=%.6f' % (a_, s_, b_))
print('extrapolations:', json.dumps(fits, indent=1))

# ---- 3. flat-profile diagnostics
gf = X.Grid(100, 1.5)
Uf, ok = X.newton(X.flat_guess(gf), 0.0, gf)
(Fi, Fx, Fxx), (Pi, Px, Pxx), (Ai, Ax, Axx) = X.pointwise(Uf, gf)[0]
args = (gf.x, Fi, Fx, Fxx, Pi, Px, Pxx, Ai, Ax, Axx)
rho = X.f_rho(*args); pr = X.f_pr(*args); pt = X.f_pt(*args)
b = X.central(Uf, gf)['b_schw']
pr0_rho0_exact = (-0.5 * b ** 2 + 0.5 * b ** 4) / (1.5 * b ** 2 + 1.5 * b ** 4)
res['flat_diag'] = dict(min_pr_over_rho=float(np.min(pr / rho)), pr0_over_rho0=pr0_rho0_exact,
                        min_pr=float(np.min(pr)), pt_sign_change=bool(np.any(pt > 0) and np.any(pt < 0)))
print('flat: min p_r/rho = %.4f, min p_r = %.3e, p_r/rho at centre (series) = %.5f' % (np.min(pr / rho), np.min(pr), pr0_rho0_exact))
json.dump(res, open(os.path.join(OUT, 'xc_extra.json'), 'w'), indent=1, default=float)
