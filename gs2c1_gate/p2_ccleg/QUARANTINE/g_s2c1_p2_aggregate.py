#!/usr/bin/env python3
"""g_s2c1_p2_aggregate.py — Gate G-S2C1, PHASE 3 / PROBE P2 (aggregate), chat leg.
Lock: prereg 2ea8ec13; T1 8cd89b9a; record f2f4d500; A-1 8bf51bd0; A-2 a9bda086; ADDENDUM P2 2feff442dfd08a379443d893b8c7761b
(locked before this file was written). E-P2-1 (a): channel = polarization-averaged transverse shear cone.
Machinery: the recovered G-POLY1 instrument poly1_fullprec_ccleg.py (branch gvbkof @ 231b555a, manifest-verified) imported
as a module for Ξ (SO(3) covariance), Φ_TM(μ) kernels, the pinned tensors, and alpha_finite (the Im-part tie-in).
New step: the real-part partner J_M(k) = PV∫ q^4 F_M(q,k)/(k_M^2 - q^2) dq by Cauchy-weight quadrature + regular tail.
All quantities in substrate units with a_g = 1. T1 self-scan at start. Per-phase JSON checkpoints (E8).
"""
import sys, os, json, math, hashlib, time
import numpy as np
from scipy.integrate import quad
sys.path.insert(0, "/home/claude/s2c/gpoly1")
import poly1_fullprec_ccleg as P
T0 = time.time()
def log(s): print("[%6.1fs] %s" % (time.time() - T0, s), flush=True)
def md5b(b): return hashlib.md5(b).hexdigest()
def ckpt(name, obj):
    b = (json.dumps(obj, indent=1, sort_keys=True, default=str) + "\n").encode(); open(name, "wb").write(b)
    log("checkpoint %s md5 %s (%d B)" % (name, md5b(b), len(b))); return md5b(b)
pats = [l.rstrip("\n") for l in open("/home/claude/s2c/t1_forbidden_G_S2_ON_CONE.txt", encoding="utf-8") if l.strip()]
src = open(os.path.abspath(__file__), encoding="utf-8").read().lower()
assert not [p for p in pats if p.lower() in src], "T1 self-scan hit"
ADDENDUM_P2 = "2feff442dfd08a379443d893b8c7761b"
assert md5b(open("/home/claude/s2c/lock/G_S2_ON_CONE_LOCK_RECORD_ADDENDUM_P2.md", "rb").read()) == ADDENDUM_P2, "P2 addendum md5 mismatch — halt"
TAU_AGG = 1e-6
LADDER = [0.3 / 2**j for j in range(9)] + [0.005, 0.01, 0.015, 0.02, 0.03]
LADDER = sorted(set(LADDER), reverse=True)

# ------------------------------------------------------------------ substrates (identical construction to the recovered main())
raw = open(P.INPUT, "rb").read(); assert md5b(raw) == P.INPUT_MD5, "input md5 mismatch — halt"
v = json.loads(raw)["vrh"]
cfg = {}
cs = v["hex:step"]["C_over_rho"];   cfg["step_hex"]   = ("hex",   [cs[k] for k in ("C11", "C12", "C13", "C33", "C44", "C66")])
cs = v["hex:gem8"]["C_over_rho"];   cfg["gem8_hex"]   = ("hex",   [cs[k] for k in ("C11", "C12", "C13", "C33", "C44", "C66")])
cs = v["cubic:step"]["C_over_rho"]; cfg["step_cubic"] = ("cubic", [cs["C11"], cs["C12"], cs["C44"]])
cs = v["cubic:gem8"]["C_over_rho"]; cfg["gem8_cubic"] = ("cubic", [cs["C11"], cs["C12"], cs["C44"]])
banked = json.load(open("/home/claude/s2c/gpoly1/poly1_phase1full_cc.json"))["phase1b"]

# ------------------------------------------------------------------ kernels
def build(name, nb=10, na=12):
    sym, cc = cfg[name]
    M6 = P.voigt_hex(*cc) if sym == "hex" else P.voigt_cubic(*cc)
    C4 = P.tensor_from_voigt(M6); KVg, GVg, KRg, GRg = P.gen_chain(M6)
    Xi, _ = P.xi_quadrature(C4, nb=nb, na=na)
    lam, mu = KVg - 2.0 * GVg / 3.0, GVg
    return Xi, math.sqrt(mu), math.sqrt(lam + 2.0 * mu)
def phi_table(Xi, inc, n):
    xg, wg = np.polynomial.legendre.leggauss(n)
    return {M: (xg, wg, np.array([P.phi_pm(Xi, inc, M, x) for x in xg])) for M in ("T", "L")}
def F_of(tab, M, q, k):
    xg, wg, ph = tab[M]; return float(np.sum(wg * ph / (1.0 + k * k + q * q - 2.0 * k * q * xg) ** 2))
def J_M(tab, M, k, kM, Qmax=50.0, epsrel=1e-10):
    """PV∫_0^∞ q^4 F_M(q,k)/(kM^2 - q^2) dq = -PV∫ [q^4 F/(kM+q)]/(q - kM) dq  (Cauchy weight) + regular tail."""
    g = lambda q: -q ** 4 * F_of(tab, M, q, k) / (kM + q)
    pv, _ = quad(g, 0.0, Qmax, weight="cauchy", wvar=kM, epsabs=0.0, epsrel=epsrel, limit=400)
    tail, _ = quad(lambda q: q ** 4 * F_of(tab, M, q, k) / (kM * kM - q * q), Qmax, np.inf, epsabs=0.0, epsrel=epsrel, limit=400)
    return pv + tail
def D_of(tab, Vinc, VT, VL, k, **kw):
    out = 0.0
    for M, VM in (("T", VT), ("L", VL)):
        out += (1.0 / (Vinc ** 2 * VM ** 2)) * J_M(tab, M, k, k * Vinc / VM, **kw)
    return out / math.pi
def D0_closed(tab, Vinc, VT, VL):
    out = 0.0
    for M, VM in (("T", VT), ("L", VL)):
        xg, wg, ph = tab[M]; out += (1.0 / (Vinc ** 2 * VM ** 2)) * float(np.sum(wg * ph))
    return -0.25 * out
def D2_analytic(tab, Vinc, VT, VL):
    """k^2 coefficient of D from (i) ∂F/∂(k^2) at fixed pole and (ii) the pole shift k_M^2 = k^2 r_M^2:
       D2 = (1/π) Σ_M N_M [ -∫ q^2 F2(q) dq - r_M^2 ∫ F0(q) dq ],  F2 = -2 I0/A^3 + 12 q^2 I2/A^4, A = 1+q^2."""
    out = 0.0
    for M, VM in (("T", VT), ("L", VL)):
        xg, wg, ph = tab[M]; I0 = float(np.sum(wg * ph)); I2 = float(np.sum(wg * ph * xg ** 2)); rM2 = (Vinc / VM) ** 2
        t1, _ = quad(lambda q: -q * q * (-2.0 * I0 / (1 + q * q) ** 3 + 12.0 * q * q * I2 / (1 + q * q) ** 4), 0, np.inf, epsrel=1e-12)
        t2, _ = quad(lambda q: -rM2 * I0 / (1 + q * q) ** 2, 0, np.inf, epsrel=1e-12)
        out += (1.0 / (Vinc ** 2 * VM ** 2)) * (t1 + t2)
    return out / math.pi
def alpha_tie(tab, VT, VL, k):
    out = 0.0
    for M, VM in (("T", VT), ("L", VL)):
        kM = k * VT / VM; out += k * kM ** 3 / (2.0 * VT * VT * VM * VM) * F_of(tab, M, kM, k)
    return out
def fits(ks, dl):
    ks = np.array(ks); dl = np.array(dl); res = {}
    for label, cols in (("basis2", (2, 4)), ("basis3", (2, 3, 4))):
        def fit(sel):
            X = np.stack([ks[sel] ** p for p in cols], axis=1); c, *_ = np.linalg.lstsq(X, dl[sel], rcond=None)
            r = dl[sel] - X @ c; return c, float(np.sqrt(np.mean(r * r)))
        c, rms = fit(ks > 0)
        cis = [fit(ks <= e)[0] for e in (0.15, 0.075)]
        res[label] = {"coef": {"k%d" % p: float(c[i]) for i, p in enumerate(cols)}, "rms": rms,
                      "ci": {"k%d" % p: float(max(abs(cc[i] - c[i]) for cc in cis)) for i, p in enumerate(cols)}}
    return res

# ------------------------------------------------------------------ Phase 0: pin reproduction (F-AGG-PIN)
log("P2 phase 0: pin reproduction of the Q_T quartet")
pin = {}
KER = {}
for name in cfg:
    Xi, VT, VL = build(name); tab = phi_table(Xi, "T", 24)     # int_phi uses n=24 GL in the recovered instrument
    iTT = float(np.sum(tab["T"][1] * tab["T"][2])); iTL = float(np.sum(tab["L"][1] * tab["L"][2]))
    QTT = iTT / (2.0 * VT ** 4); QTL = VT * iTL / (2.0 * VL ** 5); QT = QTT + QTL
    b = banked[name]; rel = abs(QT / b["Q_T_a"] - 1.0)
    pin[name] = {"Q_T_a": QT, "banked": b["Q_T_a"], "rel": rel, "digits7_match": ("%.6e" % QT) == ("%.6e" % b["Q_T_a"]), "VT0": VT, "VL0": VL, "VT0_banked": b["VT0"], "VL0_banked": b["VL0"]}
    log("  %-11s Q_T_a %.6e banked %.6e rel %.1e ; V_T %.6f (banked %.6f) V_L %.6f" % (name, QT, b["Q_T_a"], rel, VT, b["VT0"], VL))
    KER[name] = (Xi, VT, VL)
pin_ok = all(p["digits7_match"] and p["rel"] < 1e-10 for p in pin.values())
ckpt("s2c1_p2_phase0_pin.json", {"pin": pin, "F_AGG_PIN_pass": bool(pin_ok), "addendum_P2": ADDENDUM_P2})
if not pin_ok: log("F-AGG-PIN FAILED — A5-agg HALT"); sys.exit(2)

# ------------------------------------------------------------------ Phase 1: D(k) ladders, T channel (E-P2-1 (a)) + L control
log("P2 phase 1: dispersion ladders (T channel of record; L channel control)")
ph1 = {}
for name in cfg:
    Xi, VT, VL = KER[name]; rec = {"VT": VT, "VL": VL, "channels": {}}
    for inc, Vinc in (("T", VT), ("L", VL)):
        tab = phi_table(Xi, inc, 64)
        D0 = D0_closed(tab, Vinc, VT, VL); Dk = [D_of(tab, Vinc, VT, VL, k) for k in LADDER]
        Dtiny = D_of(tab, Vinc, VT, VL, 1e-4)
        rec["channels"][inc] = {"D0_closed": D0, "D_at_1e-4": Dtiny, "D0_consistency_rel": abs(Dtiny / D0 - 1.0), "ladder_k": LADDER, "D": Dk,
                                "Delta": [d - D0 for d in Dk], "D2_analytic": D2_analytic(tab, Vinc, VT, VL)}
        if inc == "T":
            grid = banked[name]["kTa_grid"]; al = [alpha_tie(tab, VT, VL, k) for k in grid]
            tab24 = phi_table(Xi, "T", 24); al24 = [alpha_tie(tab24, VT, VL, k) for k in grid]
            rec["alpha_tie_in"] = {"grid": grid, "alpha_here_n64": al, "alpha_here_n24": al24, "alpha_banked": banked[name]["alpha_T_a"],
                                   "max_rel_n24": max(abs(a / b - 1.0) for a, b in zip(al24, banked[name]["alpha_T_a"])),
                                   "max_rel_n64": max(abs(a / b - 1.0) for a, b in zip(al, banked[name]["alpha_T_a"]))}
        log("  %-11s %s: D0 %+.6e (k=1e-4: %+.6e) ; Delta(0.3) %+.4e Delta(0.0375) %+.4e ; D2_analytic %+.6e" % (name, inc, D0, Dtiny, rec["channels"][inc]["Delta"][0], rec["channels"][inc]["Delta"][3], rec["channels"][inc]["D2_analytic"]))
    log("  %-11s alpha tie-in vs banked: max rel (n=24 nodes as banked) %.1e ; (n=64) %.1e" % (name, rec["alpha_tie_in"]["max_rel_n24"], rec["alpha_tie_in"]["max_rel_n64"]))
    ph1[name] = rec
ckpt("s2c1_p2_phase1_ladders.json", ph1)

# ------------------------------------------------------------------ Phase 2: fits, analytic control, F-CONV (Ξ doubling, μ nodes, Qmax)
log("P2 phase 2: fits + controls + F-CONV")
ph2 = {}
for name in cfg:
    Xi, VT, VL = KER[name]; r = {"channels": {}}
    for inc in ("T", "L"):
        ch = ph1[name]["channels"][inc]; f = fits(ch["ladder_k"], ch["Delta"])
        a2_2, a2_3 = f["basis2"]["coef"]["k2"], f["basis3"]["coef"]["k2"]; ci = max(f["basis2"]["ci"]["k2"], f["basis3"]["ci"]["k2"])
        disagree = abs(a2_2 - a2_3) > ci
        a2_rec = a2_3 if disagree else a2_2
        an = ch["D2_analytic"]; an_ok = abs(a2_3 - an) <= max(f["basis3"]["ci"]["k2"], 1e-9 * abs(an))
        r["channels"][inc] = {"fits": f, "a2_basis2": a2_2, "a2_basis3": a2_3, "a3_basis3": f["basis3"]["coef"]["k3"], "a4_basis3": f["basis3"]["coef"]["k4"],
                              "bases_disagree_beyond_CI": bool(disagree), "a2_of_record": a2_rec, "basis_of_record": "basis3" if disagree else "basis2",
                              "D2_analytic": an, "F_AGG_ANALYTIC_rel": abs(a2_3 / an - 1.0), "F_AGG_ANALYTIC_pass": bool(an_ok), "CI_a2": ci}
    # F-CONV on the T channel: Ξ doubling, μ-node doubling, Qmax doubling — on D2_analytic and on Delta(0.3), Delta(0.0375)
    Xi2, _, _ = build(name, nb=20, na=24); tabT = phi_table(Xi, "T", 64); tabT2 = phi_table(Xi2, "T", 64); tabT128 = phi_table(Xi, "T", 128)
    D2a, D2b, D2c = D2_analytic(tabT, VT, VT, VL), D2_analytic(tabT2, VT, VT, VL), D2_analytic(tabT128, VT, VT, VL)
    dA = D_of(tabT, VT, VT, VL, 0.3); dB = D_of(tabT2, VT, VT, VL, 0.3); dC = D_of(tabT128, VT, VT, VL, 0.3); dQ = D_of(tabT, VT, VT, VL, 0.3, Qmax=100.0)
    r["F_CONV"] = {"D2_xi_doubling_rel": abs(D2b / D2a - 1.0), "D2_mu128_rel": abs(D2c / D2a - 1.0), "D03_xi_doubling_rel": abs(dB / dA - 1.0),
                   "D03_mu128_rel": abs(dC / dA - 1.0), "D03_Qmax100_rel": abs(dQ / dA - 1.0)}
    r["F_CONV_pass"] = bool(r["F_CONV"]["D2_xi_doubling_rel"] <= 1e-6 and r["F_CONV"]["D2_mu128_rel"] <= 1e-9 and r["F_CONV"]["D03_Qmax100_rel"] <= 1e-9 and r["F_CONV"]["D03_xi_doubling_rel"] <= 1e-6)
    tie = ph1[name]["alpha_tie_in"]["max_rel_n24"]; r["F_AGG_KK_pass"] = bool(tie <= 1e-9)
    T = r["channels"]["T"]; Lc = r["channels"]["L"]
    r["F_AGG_L_pass"] = bool(abs(Lc["a2_of_record"]) > max(TAU_AGG, Lc["CI_a2"]) and Lc["F_AGG_ANALYTIC_pass"])
    a2 = T["a2_of_record"]; ci = T["CI_a2"]
    if not (r["F_CONV_pass"] and r["F_AGG_KK_pass"] and T["F_AGG_ANALYTIC_pass"]): arm = "A5-agg INSTRUMENT-LIMITED"
    elif abs(a2) > max(TAU_AGG, ci): arm = "A3-agg DISPERSIVE (grain-scale k^2)"
    elif abs(T["a3_basis3"]) > TAU_AGG or abs(T["a4_basis3"]) > TAU_AGG: arm = "A2-agg PROTECTED (a2 = 0 at tau_agg; a3/a4 nonzero)"
    else: arm = "A1-agg ON-CONE-EXACT (aggregate, Born order)"
    r["arm_class"] = arm; r["a2_over_QT"] = a2 / banked[name]["Q_T_a"]
    log("  %-11s T: a2(b2) %+.6e a2(b3) %+.6e a3 %+.4e a4 %+.4e | analytic D2 %+.6e (rel %.1e) | CI %.1e | rec %s -> %s" % (name, T["a2_basis2"], T["a2_basis3"], T["a3_basis3"], T["a4_basis3"], T["D2_analytic"], T["F_AGG_ANALYTIC_rel"], ci, T["basis_of_record"], arm))
    log("  %-11s L ctrl: a2(b3) %+.6e analytic %+.6e (rel %.1e) ; F-CONV %s ; KK %s ; a2/Q_T %+.4f" % (name, Lc["a2_basis3"], Lc["D2_analytic"], Lc["F_AGG_ANALYTIC_rel"], r["F_CONV"], r["F_AGG_KK_pass"], r["a2_over_QT"]))
    ph2[name] = r
uni = {n: ph2[n]["a2_over_QT"] for n in ph2}
spread = (max(uni.values()) - min(uni.values())) / abs(np.mean(list(uni.values())))
summary = {"gate": "G-S2C1", "phase": "3 / P2 aggregate", "leg": "chat", "election_E_P2_1": "(a)", "addendum_P2_md5": ADDENDUM_P2, "tau_agg": TAU_AGG,
           "a2_agg_of_record_T": {n: ph2[n]["channels"]["T"]["a2_of_record"] for n in ph2}, "a3_agg_T": {n: ph2[n]["channels"]["T"]["a3_basis3"] for n in ph2},
           "a4_agg_T": {n: ph2[n]["channels"]["T"]["a4_basis3"] for n in ph2}, "D0_T": {n: ph1[n]["channels"]["T"]["D0_closed"] for n in ph1},
           "arm_class_by_substrate": {n: ph2[n]["arm_class"] for n in ph2}, "F_AGG_UNI_a2_over_QT": uni, "F_AGG_UNI_spread_rel": float(spread),
           "registered_expectation": "DISPERSIVE (k^3 non-analytic term pre-registered)", "verdict": "chat-leg P2 class only; two-leg (CC) pending; no window action"}
ckpt("s2c1_p2_phase2_fits.json", {"per_substrate": ph2, "summary": summary})
log("F-AGG-UNI: a2_agg/Q_T = %s ; spread %.2e" % ({n: round(x, 5) for n, x in uni.items()}, spread))
log("P2 COMPLETE (chat leg).")
