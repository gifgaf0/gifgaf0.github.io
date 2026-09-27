#!/usr/bin/env python3
"""diag_kappa24.py -- post-run DIAGNOSTIC (not a checkpoint; not verdict-bearing): (1) Richardson estimates of the
cross coefficient kappa24 from mixed second differences at h and h/2 (error O(h^4)), hex P2+P4 family and the cubic
inherited (non-symmetrized, descriptor-axis) P2 term + K4-tilde; (2) the mixed-term r_agg change that A-2.9's
F-CTRL-L2NULL r_agg clause would have measured on cubic; (3) the pure l = 2 r_agg change on cubic (exact null)."""
import json, math, sys, importlib.util
import numpy as np
spec = importlib.util.spec_from_file_location('inst', '/home/claude/gmscs2/g_mscs2_chatleg.py'); I = importlib.util.module_from_spec(spec); spec.loader.exec_module(I)
vrh = json.load(open(I.X1))['vrh']; K, W = I.sphere_grid(I.N_THETA, I.N_PHI)
def mixed_odf(sym, axis, cm, t2, t4):
    if sym == 'hex': return I.ODF('P4', t2=t2, t4=t4)
    base = I.ODF('K4', axis_c=axis, cmarg=cm, t4=t4)
    class _M(I.ODF):
        def w_so3(self, Rs): return base.w_so3(Rs) + t2 * I.P2((Rs @ axis)[:, 2])
        def w_marg(self, n): return base.w_marg(n) + t2 * I.P2(n[:, 2])
    return _M('K4', axis_c=axis, cmarg=cm, t4=t4)
def r(sym, c4, odf):
    ag = I.aggregate_tensors(c4, odf, None); return I.species_stats(sym, ag['H'], K, W, odf, want_labels=False)['r_xtal_E2']
out = {}
for cfg, (sym, vk) in I.CONFIGS.items():
    for key, symm, axis, cm in I.config_keys(cfg):
        c4 = I.c4_from_constants(sym, vrh[vk]['C_over_rho'], symm)
        def D(h):
            f = lambda a, b: r(sym, c4, mixed_odf(sym, axis, cm, a, b))
            return (f(h, h) - f(h, -h) - f(-h, h) + f(-h, -h)) / (4 * h * h)
        d1, d2 = D(0.02), D(0.01); k24 = (4 * d2 - d1) / 3.0
        rec = {'kappa24_richardson': k24, 'D_h0p02': d1, 'D_h0p01': d2}
        if sym == 'cubic':
            r00 = r(sym, c4, I.ODF('iso')); r20 = r(sym, c4, I.ODF('l2', axis_c=axis, t=1.0))
            rA = r(sym, c4, mixed_odf(sym, axis, cm, 0.0, 0.25)); rB = r(sym, c4, mixed_odf(sym, axis, cm, 0.25, 0.25))
            rec.update({'pure_l2_r_agg_change_t1': abs(r20 - r00), 'mixed_r_agg_change_A29': abs(rB - rA), 'r_agg_0_0p25': rA, 'r_agg_0p25_0p25': rB})
        out[key] = rec; print(key, {k: f'{v:+.3e}' for k, v in rec.items()}, flush=True)
json.dump(out, open('/home/claude/gmscs2/diag_kappa24.json', 'w'), indent=1)
