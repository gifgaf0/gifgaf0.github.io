#!/usr/bin/env python3
"""Arithmetic behind the numbers that the October 4 revision of the draft adds or changes (first leg).

Plain-language summary: every new number in the revised draft is either read from the two-leg data files or follows
from them by the arithmetic below. Run from lbc_bank/paper/; it reads ../closure/ and prints one line per number.

  R1  radiation ratio of Sec. 7 with the corrected 3D speeds (was 9e10 with c1/c2 = 33.6)
  R2  loss length of Eq. (3): coefficient, a proton-size and a Planck-size defect, the size needed
  R3  the other way out of Eq. (3): how far F2, and by Eq. (1) M - rho*gamma, would have to drop
  R4  the vortex-ring flow vertex against the deficit vertex (Sec. 6)
  R5  Table 2: Z2/Z1 against (F2/F1)(c1/c2), the dispersion note in the caption
  R6  Table 2: the values at the coexistence boundary (linear interpolation 13.0-13.25, as build_v2.py) and the
      stable-phase ranges quoted in the text
  R7  Table 2: the new f_s entries, two legs (closure/fs_rows.json, closure/fs_rows_cc.json)
  R8  Table 2: the rows outside the blind comparison, recomputed with the second leg's code
  R9  Sec. 9: the Cox numbers
"""
import json, math

CL = "../closure/"
P = json.load(open(CL + "paper_tables_v2.json"))
A = json.load(open(CL + "jobA_2d.json"))
JC = {round(c["g"], 3): c for c in json.load(open(CL + "jobC_melt.json"))}
ok = True
def line(tag, txt, cond=True):
    global ok
    ok &= bool(cond)
    print(f"{tag}: {txt}{'' if cond else '   <-- FAIL'}")

# R1 radiation, quadrupole (l = 2) in d = 3: P2/P1 = (F2/F1) (c1/c2)^(2l+d+2)
rows3 = [r for r in P["three_d"]["K30"]["rows"] if abs(r["q"] - 0.15) < 1e-9]
rat = []
for r in rows3:
    F2 = r["F2"]; r12 = r["c1"] / r["c2"]
    rat.append(((F2 / (1 - F2)) * r12 ** 9, r12, r["dir"]))
lo, hi = min(rat), max(rat)
line("R1", f"c1/c2 = {min(x[1] for x in rat):.2f}-{max(x[1] for x in rat):.2f}; quadrupole P2/P1 = "
     f"{lo[0]:.3g} ({lo[2]}) to {hi[0]:.3g} ({hi[2]})  -> 'about 1e11'", 0.5e11 < lo[0] and hi[0] < 3e11)

# R2 loss length, Eq. (3)
tau, eps, cT, ck, F2 = 10.0, 1.0, 7.85, 9.38, 0.0017
coef = 16 * math.pi * tau / eps**2 * (cT / ck) ** 4 / F2
gam = 3e11 / 0.93827                       # 3e11 GeV protons
L_need = 3.0857e20                          # 10 kpc in m
xi_p, xi_pl = 1e-15, 1.616255e-35
short_p = L_need / (coef * gam * xi_p); short_pl = L_need / (coef * gam * xi_pl)
line("R2", f"Eq.(3) coefficient {coef:.4g} (-> 1.5e5); gamma {gam:.4g}; xi_req {L_need/(coef*gam):.3g} m (-> 'xi >~ 6e3 m'); "
     f"1 fm: ell = {coef*gam*xi_p:.3g} m, short by 10^{math.log10(short_p):.2f}; Planck: short by 10^{math.log10(short_pl):.2f}",
     abs(math.log10(short_p) - 19) < 0.5 and abs(math.log10(short_pl) - 39) < 0.5)
line("R2", f"Eq.(4) 1/(2 gamma^2) = {1/(2*gam**2):.3g}  (-> 5e-24)")

# R3 the coupling route: ell ~ 1/F2, F2 ~ (M - rho gamma)^2 at fixed other factors
line("R3", f"F2 would have to drop by 10^{math.log10(short_p):.2f} (to {F2/short_p:.2g} at 1 fm), "
     f"so M - rho*gamma by 10^{0.5*math.log10(short_p):.2f}  -> 'about one part in 1e9'", 9 <= 0.5*math.log10(short_p) < 10)

# R4 ring flow vertex vs deficit vertex: pi kappa R^2 v / (c_k^2 eps xi^3), kappa = 2 pi, R = xi = 1/c_k
v = 7.85
ratio = math.pi * (2 * math.pi) * v * (1 / ck) ** 2 / (ck ** 2 * eps * (1 / ck) ** 3)
line("R4", f"flow/deficit vertex = 2 pi^2 (v/c_k)/eps = {ratio:.3f} at v = {v}; on the second-sound Cherenkov cone "
     f"sin^2 = 1 - (c2/v)^2 = {1-(0.4706/v)**2:.4f}  -> 'an order of magnitude'", 10 <= ratio < 30)

# R5 Z2/Z1 vs (F2/F1)(c1/c2)
dev = []
for r in P["rows"]:
    pred = r["F2"] / (1 - r["F2"]) * r["c1"] / r["c2"]
    dev.append((r["Z21"] / pred - 1, r["g"], r["label"]))
mx = max(dev, key=lambda x: abs(x[0]))
line("R5", "Z2/Z1 over (F2/F1)(c1/c2) - 1: " + ", ".join(f"{g:g}:{100*d:+.1f}%" for d, g, _ in dev)
     + f"; largest {100*mx[0]:+.1f}% at g = {mx[1]:g}  -> 'up to 9 %'", abs(mx[0]) < 0.095)

# R6 values at Lambda_c and the stable-phase ranges
m = P["melting"]; Lc = m["Lambda_c"]; w = (Lc - 13.0) / 0.25
r13, r1325 = A["ref_g13"], A["ref_g13.25"]
at = lambda k: (1 - w) * r13[k] + w * r1325[k]
S2c, F2c, Zc = at("S2"), at("F2"), at("Z21"); rc = m["ratio_at_Lambda_c"]
stab = [r for r in P["rows"] if r["phase"] == "stable"]
line("R6", f"Lambda_c = {Lc:.4f}; at Lambda_c: c2/cT {rc:.4f}, F2 {F2c:.4f} (json {m['F2_at_Lambda_c']:.4f}), "
     f"Z2/Z1 {Zc:.3f}, S2 {S2c:.4f}")
r_lo = min(r["ratio"] for r in stab); F_lo = min(r["F2"] for r in stab); S_lo = min(r["S2"] for r in stab)
line("R6", f"stable phase (rows marked stable, up to Lambda_c): c2/cT {r_lo:.3f}-{rc:.3f} (-> 0.07-0.77); "
     f"F2 {F_lo:.4f}-{F2c:.4f} (-> 0.3-41 %); S2 {S_lo:.4f}-{max(S2c, max(r['S2'] for r in stab)):.4f} (-> 64-80 %)",
     round(r_lo, 2) == 0.07 and round(rc, 2) == 0.77 and round(100*F_lo, 1) == 0.3 and round(100*F2c) == 41
     and round(100*S_lo) == 64 and round(100*S2c) == 80)
line("R6", f"g = 13.0 lies {Lc-13.0:.3f} below Lambda_c (metastable side): S2 there {r13['S2']:.4f} (table 0.81)")

# R7 new f_s, two legs
f1 = json.load(open(CL + "fs_rows.json")); f2 = json.load(open(CL + "fs_rows_cc.json"))
def fs(d, k):
    x = d[k]; return x["f_s"] if isinstance(x, dict) else x
pairs = [("soft_g44", "soft_g44", "0.0055"), ("soft_g34", "soft_g34", "0.018"), ("soft_g28", "soft_g28", "0.039"),
         ("g6_g35", "g6_g35", "0.094"), ("meta_g12.5", "meta_g12.5", "0.698"), ("meta_g12.4", "meta_g12.4", "0.74")]
for k1, k2, shown in pairs:
    a, b = fs(f1, k1), fs(f2, k2)
    nd = len(shown.split(".")[1])
    good = round(a, nd) == float(shown) and round(b, nd) == float(shown)
    line("R7", f"{k1}: first leg {a:.6f}, second-leg code {b:.6f} (diff {abs(a/b-1)*100:.3f} %); table '{shown}'", good)

# R8 rows outside the blind comparison: second-leg code vs the first leg
T2 = json.load(open(CL + "table2_cc_rows.json"))
first = {r["g"]: r for r in P["rows"] if r["kernel"] == "soft"}
for g in (12.5, 12.4):
    c = JC[g]; first[g] = {"astar": c["a"], "c2": c["c2"], "cT": c["cT"], "c1": c["c1"], "F2": c["F2"]}
worst = {}
for key, g in (("g34.0", 34.0), ("g20.0", 20.0), ("g18.0", 18.0), ("g15.0", 15.0), ("meta_g12.7", 12.7),
               ("meta_g12.5", 12.5), ("meta_g12.4", 12.4)):
    cc, fl = T2[key], first[g]
    for q in ("astar", "c2", "cT", "c1", "F2", "Z21", "S2", "f_s"):
        if q in fl and fl[q] is not None and cc.get(q) is not None:
            d = abs(cc[q] / fl[q] - 1)
            worst[(g, q)] = d
big = sorted(worst.items(), key=lambda x: -x[1])
line("R8", "largest gaps: " + ", ".join(f"g={g:g} {q} {100*d:.2f}%" for (g, q), d in big[:4]))
others = [d for (g, q), d in worst.items() if not (g == 12.4 and q == "c1")]
line("R8", f"all other entries agree to {100*max(others):.2f} % (c1 at 12.4: see table2_cc_g124_modecheck.log)",
     max(others) < 0.005)

# R10 Eq. (3) takes the hydrodynamic response up to q ~ 1/xi = c_kappa; the 3D zone edge of the AB stack (a, c of Sec. 4)
a3, c3 = 1.386, 2.260
zK, zM, zA = 4 * math.pi / (3 * a3), 2 * math.pi / (math.sqrt(3) * a3), math.pi / c3
qmax = ck                                      # 1/xi with xi = 1/c_kappa (hbar = m = 1)
lo_cut, hi_cut = 4 * math.log10(qmax / max(zK, zM, zA)), 4 * math.log10(qmax / min(zK, zM, zA))
line("R10", f"zone edge |K| {zK:.2f}, |M| {zM:.2f}, |A| {zA:.2f}; drag ~ q_max^4, so a cut there lowers it by "
     f"10^{lo_cut:.2f}-10^{hi_cut:.2f}  -> 'two to three orders'; proton-size shortfall then "
     f"10^{math.log10(short_p)-hi_cut:.1f}-10^{math.log10(short_p)-lo_cut:.1f}", 1.5 < lo_cut and hi_cut < 3.5)
line("R10", f"flow vertex on the second-sound cone: |V|^2 ratio {(ratio*(1-(0.4706/v)**2))**2:.0f} = "
     f"10^{2*math.log10(ratio*(1-(0.4706/v)**2)):.2f}  -> 'shortens ell by about two orders'")

# R11 Table 2 caption and Method: what separates Z2/Z1 from the two-branch value, and how flat Z/q is
for lab in ("soft_g22", "soft_g14", "soft_g13.5", "ref_g13", "ref_g12.7"):
    r = A[lab]; rows = [x for x in r["rows"] if x["dir"] == "GM"]
    ref = [x for x in rows if abs(x["kf"] - 0.05) < 1e-12][0]
    qq = ref["q"]; w2, w1 = ref["c_Lm"] * qq, ref["c_Lp"] * qq
    norm = ref["Z_Lm"] * w2 / ref["F_Lm"]; F1 = ref["Z_Lp"] * w1 / norm; F2 = ref["F_Lm"]
    Z21 = ref["Z_Lm"] / ref["Z_Lp"]
    two_q = F2 / (1 - F2) * w1 / w2; two_s = F2 / (1 - F2) * r["c1"] / r["c2"]
    z2 = [x["Z_Lm"] / x["q"] for x in rows]; z1 = [x["Z_Lp"] / x["q"] for x in rows]
    line("R11", f"{lab}: gapped modes' f-sum share at 0.05 {1-F1-F2:.4f}; Z2/Z1 vs two-branch value {Z21/two_s-1:+.2%} "
         f"(gapped {Z21/two_q-1:+.2%}, dispersion {two_q/two_s-1:+.2%}); Z2/q spread over the window "
         f"{max(z2)/min(z2)-1:.1%}, Z1/q {max(z1)/min(z1)-1:.1%}")

# R12 the S5 evaluation quoted beside Eq. (3) (closure checkpoint, two-leg)
ckp = json.load(open(CL + "lbc_chat_checkpoint_v2.json"))["loss"]
line("R12", f"S5: xi_req {ckp['xi_req_main_m'][0]:.3g}-{ckp['xi_req_main_m'][1]:.3g} m (-> 'xi >~ 2e4 m'); Planck shortfall "
     f"{ckp['main_headline_orders'][0]:.2f} to {ckp['main_headline_orders'][1]:.2f} orders (-> '39 orders')")

# R13 'one part in 1e9 or better': |M - rho gamma|/M needed, with M/(rho gamma) = 11.4 at g = 22
need = (1 - 1 / 11.42) / math.sqrt(short_p)
line("R13", f"|M - rho*gamma|/M must fall from {1-1/11.42:.3f} to {need:.2g}  -> 'one part in 1e9 or better'", need < 1e-9)

# R9 Cox
fs_c = 0.8
for d in (3, 4):
    print(f"R9: d = {d}: c_-/c_T >= sqrt(f_s * 2(d-1)/d) = {math.sqrt(fs_c*2*(d-1)/d):.4f}; "
          f"f_s threshold d/[2(d-1)] = {d/(2*(d-1)):.4f}")
print(f"R9: K/mu = 5/3 -> M = K + 4mu/3 = 3 mu -> c_-/c_T = sqrt(0.8*3) = {math.sqrt(2.4):.4f}")
print("ALL REVISION NUMBERS CHECK" if ok else "SOME CHECK FAILED")
