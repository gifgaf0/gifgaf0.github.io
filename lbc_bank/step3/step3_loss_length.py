#!/usr/bin/env python3
"""Step 3: re-evaluate the V4.67 KC3 loss length on the measured 3D slow branch.
Inputs taken verbatim from V4.67 (ledger 2.91.G/H): l = gamma*M*tau*xi/P per channel; maps (A,J,O,T)
at the four two-leg R1 points (Ohat(3.0,5) per erratum E1 = 1.6401); xi = l_P; gamma = 3.1974e11;
L_prop = 3.0857e20 m (galactic, Moore-Nelson); M_old = phi^2 (retired fluid branch c_s = phi^-2 c).
Change: the radiating branch is the measured 3D slow branch (G-TSH4 AB/hcp, step kernel, Lambda = 2 Lambda_c):
f-sum share F2 and speed c2 from lbc_3d.json. Drag at fixed vertex: d=3 point source
(rho F/4 pi v^2) Int q^3 |V|^2 dq; filament (per length) (rho F/2 pi v^2) S(M) Int q^2 |V|^2 dq,
S(M) = 1/sqrt(1-1/M^2).  Substrate units for speeds; c = c_T (ANNEX-CDEF-1)."""
import json, math
import numpy as np
phi = (1+5**0.5)/2
lP, gam, Lprop = 1.616255e-35, 3.1974e11, 3.0857e20
pts = {(2.0,20):(15.17,4.68,1.82,8.06), (3.0,5):(9.35,0.61,1.6401,2.74),
       (3.0,10):(13.73,4.43,1.20,7.49), (3.0,20):(18.26,7.41,0.45,11.23)}
def ell(M, tau, P, xi=lP): return gam*M*tau*xi/P
# --- reproduce V4.67 corners (single most/least favourable channel, per-point pairing)
cand = [(ell(phi**2, T, P), k, ch) for k,(A,J,O,T) in pts.items() for ch,P in (("A",A),("J",J),("O",O))]
lmax = max(cand); lmin = min(cand)
o_best = math.log10(lmax[0]/Lprop); o_worst = math.log10(lmin[0]/Lprop)
print(f"V4.67 reproduced: most favourable {lmax[1]} {lmax[2]}: {o_best:+.2f} orders; least {lmin[1]} {lmin[2]}: {o_worst:+.2f}")
A,J,O,T = pts[(3.0,20)]
xi_req_old = Lprop*O/(gam*phi**2*T)
# --- measured 3D slow branch
D = json.load(open("/home/claude/lbc_exploration/lbc_3d.json"))
rows = D["rows"]
F2 = [r["fshare"][0] for r in rows]; c2 = [r["om"][0]/r["q"] for r in rows]
cT = [min(r["om"][4], r["om"][5])/r["q"] for r in rows]; cTmean = 7.68   # G-TSH4 dynamical transverse mean
F2_lo, F2_hi = min(F2), max(F2)
c2v = float(np.median(c2)); M_new = cTmean/c2v
S = lambda M: 1/math.sqrt(1-1/M**2)
print(f"3D slow branch: F2 in [{F2_lo:.5f}, {F2_hi:.5f}], c2 = {c2v:.4f} (c2/c_T = {c2v/cTmean:.4f}), M_new = c/c2 = {M_new:.2f}; "
      f"S(phi^2) = {S(phi**2):.5f}, S(M_new) = {S(M_new):.5f}")
# compressibility speed of the 3D substrate (static sum, per volume, rho = 1)
r0 = [r for r in rows if r["dir"]=="basal_GM" and abs(r["q"]-0.15)<1e-9][0]
ckappa = math.sqrt(r0["vol"]/r0["chi_direct"]); cs_decl = cTmean/phi**2
print(f"3D compressibility speed c_kappa = {ckappa:.3f} = {ckappa/cTmean:.3f} c_T (declared fluid c_s = {1/phi**2:.3f} c)")
out = {}
for name, fac in (("fixed vertex, filament (main)", lambda F: (S(phi**2)/S(M_new))/F),
                  ("fixed vertex, point source",    lambda F: 1/F),
                  ("closure literal, M -> c/c2",    lambda F: (M_new/phi**2)/F),
                  ("fixed dressed static deficit",  lambda F: (S(phi**2)/S(M_new))/F/((ckappa/cs_decl)**4))):
    lo, hi = fac(F2_hi), fac(F2_lo)
    d_lo, d_hi = math.log10(lo), math.log10(hi)
    out[name] = dict(factor=[lo, hi], orders_recovered=[d_lo, d_hi],
                     headline=[o_best+d_lo, o_best+d_hi], least=[o_worst+d_lo, o_worst+d_hi],
                     xi_req_m=[xi_req_old/hi, xi_req_old/lo])
    print(f"{name:32s}: x{lo:9.1f} .. x{hi:9.1f}  (+{d_lo:.2f} .. +{d_hi:.2f} orders) -> most favourable "
          f"{o_best+d_lo:+.2f} .. {o_best+d_hi:+.2f}; least {o_worst+d_lo:+.2f} .. {o_worst+d_hi:+.2f}; "
          f"xi_req {xi_req_old/hi:.2e} .. {xi_req_old/lo:.2e} m")
print(f"xi_req (V4.67 pairing, reproduced) = {xi_req_old:.3e} m")
json.dump(dict(V467=dict(best=o_best, worst=o_worst, xi_req=xi_req_old), F2=[F2_lo,F2_hi], c2=c2v, M_new=M_new,
               c_kappa=ckappa, readings=out), open("step3_loss_length.json","w"), indent=1)
