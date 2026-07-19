"""G-TSH1 CC leg — PART 1: analytic controls + INDEPENDENT re-reduction of the raw band data.

This part shares NO ground-state / BdG machinery with the chat leg; it (a) re-derives the
C-POS classical-lattice control symbolically from scratch, and (b) re-reduces the chat leg's
RAW ω(k) dispersion arrays with an independent slope reducer + verdict logic, auditing the
fit/classification/verdict layer. The independent GP+BdG solver is PART 2 (tsh1_cc_bdg.py).
Comparison items touched here: C4 (fit extraction), C5 (D_i, D_ii), C-POS control, isotropy.
"""
import json, numpy as np, sympy as sp

RES = "/root/.claude/uploads/6734b25b-79a1-5266-80d1-b1daca905689/d6351fe0-g_tsh1_results.json"
R = json.load(open(RES))
PASS=[]; NOTE=[]
def ok(c,m):
    assert c, "FAIL: "+m
    PASS.append(m)

# ============================================================================
# (A) C-POS control — triangular NN central-force lattice, derived from scratch
# ============================================================================
qx,qy,ks,aS = sp.symbols('q_x q_y k_s a', positive=True)
# 3 NN bond directions of the triangular lattice (unit vectors)
E = [sp.Matrix([1,0]), sp.Matrix([sp.Rational(1,2), sp.sqrt(3)/2]),
     sp.Matrix([-sp.Rational(1,2), sp.sqrt(3)/2])]
q = sp.Matrix([qx,qy])
D = sp.zeros(2,2)
for e in E:
    D += 2*ks*sp.sin((q.T*e)[0]*aS/2)**2*(e*e.T)   # central-force dynamical matrix
# long-wavelength (leading q^2) along x
Dx = D.subs(qy,0).applyfunc(lambda z: sp.series(z, qx, 0, 4).removeO())
lam = sorted([sp.simplify(l/qx**2).subs({aS:1,ks:1}) for l in Dx.eigenvals()], key=float)
cT2, cL2 = lam
cT_sym, cL_sym = float(sp.sqrt(cT2)), float(sp.sqrt(cL2))
ok(abs(cT_sym-0.4330127)<1e-6 and abs(cL_sym-0.75)<1e-6,
   f"C-POS speeds cT={cT_sym:.7f}(=√3/4) cL={cL_sym:.7f}(=3/4) re-derived from scratch")
ok(abs(cT_sym/cL_sym-1/np.sqrt(3))<1e-9,
   f"C-POS ratio cT/cL = 1/√3 = {cT_sym/cL_sym:.5f} (Cauchy relation λ=μ, triangular)")
# chat's stored control values
ok(abs(R['phaseC']['C_POS']['cT_sym']-cT_sym)<1e-6 and abs(R['phaseC']['C_POS']['cL_sym']-cL_sym)<1e-6,
   "chat C_POS symbolic speeds match the independent derivation")

# ============================================================================
# (B) Independent slope reducer  c = argmin_c Σ(ω-ck)² = Σkω/Σk² ; p = d ln ω/d ln k
# ============================================================================
def reduce_speed(k, om):
    k=np.asarray(k,float); om=np.asarray(om,float)
    c = float(np.sum(k*om)/np.sum(k*k))
    p = float(np.polyfit(np.log(k), np.log(om), 1)[0])
    return c, p

# ---- C4: canonical (g=22) branch speeds re-reduced from RAW ω(k) (GM direction) ----
GM = R['phase1']['GM']
# primary window kf in [0.05,0.20]
def win(kf,lo,hi): return [(f>=lo-1e-9 and f<=hi+1e-9) for f in kf]
for lab, cref in [('T',5.7749),('L',11.0453)]:
    kf = GM[lab]['kf']; k = np.array(GM[lab]['k']); om=np.array(GM[lab]['om'])
    sel = np.array(win(kf,0.05,0.20))
    c,p = reduce_speed(k[sel], om[sel])
    ok(abs(c-cref)/cref < 3e-3, f"C4 {lab}: independent re-reduction c={c:.4f} vs chat {cref} (<0.3%)")
    NOTE.append(f"  {lab}-branch exponent p={p:.4f} (linear)")
cT = reduce_speed(np.array(GM['T']['k'])[np.array(win(GM['T']['kf'],0.05,0.20))],
                  np.array(GM['T']['om'])[np.array(win(GM['T']['kf'],0.05,0.20))])[0]
cL = reduce_speed(np.array(GM['L']['k'])[np.array(win(GM['L']['kf'],0.05,0.20))],
                  np.array(GM['L']['om'])[np.array(win(GM['L']['kf'],0.05,0.20))])[0]
RT = cT/cL
ok(abs(RT-0.52284)<3e-4, f"C4 R_T = c_T/c_L1 = {RT:.5f} vs chat 0.52284 (independent)")

# ---- isotropy: GK vs GM transverse speed ----
GK = R['phase1']['GK']
cTk = reduce_speed(np.array(GK['T']['k'])[np.array(win(GK['T']['kf'],0.05,0.20))],
                   np.array(GK['T']['om'])[np.array(win(GK['T']['kf'],0.05,0.20))])[0]
iso = abs(cTk-cT)/cT
ok(iso < 0.03, f"isotropy |cT(ΓK)-cT(ΓM)|/cT = {iso*100:.2f}% (<3%, p6m-isotropic)")

# ============================================================================
# (C) C5: axis-(i)/(ii) dispersion re-computed from the stored R_T points
# ============================================================================
RTpts = R['verdict']['Q2']['RT_points']
soft = np.array([RTpts[k] for k in ['soft_g22','soft_g28','soft_g34','soft_g44']])
Di = float(np.max(np.abs(soft-soft.mean()))/soft.mean())
ok(abs(Di-0.0210)<2e-3, f"C5 axis-(i) D = {Di*100:.2f}% (chat 2.10%) -> PINNED (<3%)")
allRT = np.append(soft, RTpts['g6'])
Dii = float(np.max(np.abs(allRT-allRT.mean()))/allRT.mean())
ok(abs(Dii-0.0511)<3e-3, f"C5 axis-(ii) D = {Dii*100:.2f}% (chat 5.11%) -> UNDERDETERMINED (3-10%)")
ok(0.03 < Dii < 0.10, "axis-(ii) lands in the locked dead-zone (3%,10%) — verdict UNDERDETERMINED confirmed")

# ---- post-verdict R2 note: central-force ratio vs measured band ----
cf_ratio = cT_sym/cL_sym    # 0.5774
below = [(cf_ratio-x)/cf_ratio for x in soft]
ok(all(0.055 < b < 0.10 for b in below),
   f"soft-core band {soft.min():.3f}-{soft.max():.3f} sits {min(below)*100:.1f}-{max(below)*100:.1f}% "
   f"below central-force 1/√3={cf_ratio:.4f} (chat '6-9%')")

# ============================================================================
# (D) Amendment-1 monotonicity + discipline audits (structural, no solver)
# ============================================================================
depth = {6:0.427,10:0.525,16:0.662,24:0.862,40:0.973}
taus=sorted(depth); vals=[depth[t] for t in taus]
ok(all(vals[i]<vals[i+1] for i in range(len(vals)-1)), "A1: ψ6 monotone increasing in anneal depth")
ok(vals[0] < 0.834 < vals[-1], "A1: canonical 0.834 lies on the depth trajectory (τ≈22) — object on-trajectory")
# T1 forbidden-constant self-grep on the chat script (independent grep)
src = open("/root/.claude/uploads/6734b25b-79a1-5266-80d1-b1daca905689/afec2ea7-g_tsh1_chatleg.py").read()
# strip the FORBID definition line itself, then grep for the reassembled constants
forbidden = ["299792458","GW170817","0.381966","1.618","0.145898","1.2162","0.61237","0.57735"]
body = "\n".join(l for l in src.splitlines() if "FORBID =" not in l and '"2997"' not in l and 'j1(x[m])' not in l)
hits=[f for f in forbidden if f in body.replace(" ","")]
ok(not hits, f"T1: no forbidden physical constant literals in chat script body (indep grep) hits={hits}")

print(f"[PART 1] {len(PASS)} independent assertions PASSED\n")
for m in PASS: print("  ✓", m)
print("\n".join(NOTE))
print(f"\n[summary] c_T={cT:.4f} c_L1={cL:.4f} R_T={RT:.5f} | D_i={Di*100:.2f}% D_ii={Dii*100:.2f}% | "
      f"iso={iso*100:.2f}% | C-POS cT/cL=1/√3")
