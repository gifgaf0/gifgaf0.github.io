#!/usr/bin/env python3
"""g_s2c1_phase0_close.py — Gate G-S2C1 (display: Gate G-S2-ON-CONE), PHASE 0 CLOSE (chat leg).
Lock: prereg 2ea8ec13ffa3c32898cc24a3be605c64; T1 8cd89b9a82704accd89f7ff6f5e220b4; lock record f2f4d500.
PHASE1_AUTHORIZED = False (hard flag: no S2 ladder is computed or fitted here).

Three parts, all CONTROL-NOT-VERDICT:
 (A) SUBSTRATE DIAGNOSTIC on the recovered gz1 crystal (g = 22 soft-disk, n = 64, a* = 1.4576, mu = 55.946):
     un-clipped product-form BdG omega^2 = eig(L(L+2X)) at small k, n_b in {24, 32, 40}; L psi0 residual;
     spectral resolution; aliasing test (exact-product X vs grid-consistent X). Establishes whether the
     acoustic (Goldstone) sector is resolved to the precision the E-4 ladder needs.
 (B) ANALYTIC p6m CONTROL — nearest-neighbour central-force triangular lattice (K = m = a = 1), closed-form
     dispersion: validates the S2 projector (traceless-strain fraction; T -> 1, L -> 1/2 on mirror lines) and
     the E-4/E-5 fitter (residual r = a2 (ka)^2 + a4 (ka)^4 on the dyadic ladder) against independent
     closed-form series coefficients. F-CTRL-L: the L branch's KNOWN NONZERO a2 must be recovered.
 (C) F-CTRL-INJ — synthetic injection a2 = 10*tau = 1e-5 with noise at the F-CONV scale; recovery within tau.
"""
import sys, json, hashlib, os
import numpy as np
sys.path.insert(0, "/home/claude/s2c/gz1")
import gz1_core as gz
PHASE1_AUTHORIZED = False
TAU = 1.0e-6
LADDER = np.array([0.3 / 2**j for j in range(9)])       # E-4 dyadic ka: 0.3 ... 0.00117
def md5b(b): return hashlib.md5(b).hexdigest()

# =============================================================== (A) substrate diagnostic
A_STAR, MU, N = 1.4576, 55.946, 64
cell = gz.Cell(A_STAR, N); psi0 = np.load("/home/claude/s2c/gz1/psi0_polished_n64.npy").astype(float)
def LX(b, k):
    kgx = k[0] + b.m1 * cell.b1[0] + b.m2 * cell.b2[0]; kgy = k[1] + b.m1 * cell.b1[1] + b.m2 * cell.b2[1]
    L = np.diag(0.5 * (kgx**2 + kgy**2) - MU) + b.Vmat; L = 0.5 * (L + L.conj().T)
    D = gz.U_tilde(np.sqrt(kgx**2 + kgy**2)); X = b.P @ (D[:, None] * b.P); X = 0.5 * (X + X.conj().T)
    return L, X
diag = {"substrate": "gz1_rebuild psi0_polished_n64 md5 " + md5b(open("/home/claude/s2c/gz1/psi0_polished_n64.npy", "rb").read()),
        "a_star": A_STAR, "mu": MU, "goldstone_offset_product_form": {}, "hermitian_clipped_lowest": {}}
for nb in (24, 32, 40):
    b = gz.BdG(cell, psi0, MU, nb)
    row = {}
    for ka in (0.005, 0.02, 0.08):
        k = np.array([ka / A_STAR, 0.0]); L, X = LX(b, k)
        w2 = np.sort_complex(np.linalg.eigvals(L @ (L + 2 * X)))[:3].real
        row["ka=%.3f" % ka] = [float(x) for x in w2]
        if nb == 32:
            diag["hermitian_clipped_lowest"]["ka=%.3f" % ka] = [float(x) for x in b.omegas(k, nbands=3)]
    diag["goldstone_offset_product_form"]["n_b=%d" % nb] = row
b = gz.BdG(cell, psi0, MU, 32)
L0, X0 = LX(b, np.array([0.0, 0.0]))
coef = np.fft.fft2(psi0) / N**2
def pw(field):
    c = np.fft.fft2(field) / N**2; v = np.zeros(len(b.m1), complex)
    ok = (np.abs(b.m1) < N // 2) & (np.abs(b.m2) < N // 2); v[ok] = c[b.m1[ok] % N, b.m2[ok] % N]; return v
v0 = pw(psi0); vd = pw(np.fft.ifft2(1j * cell.Gx * np.fft.fft2(psi0)).real)
diag["L_psi0_residual_rel"] = float(np.linalg.norm(L0 @ v0) / np.linalg.norm(v0))
diag["L_psi0_residual_rel_over_mu"] = diag["L_psi0_residual_rel"] / MU      # = the rebuild's logged residual_polished
diag["ward_residual_translation_mode_rel"] = float(np.linalg.norm((L0 + 2 * X0) @ vd) / np.linalg.norm(vd))
P = np.abs(coef)**2; m = np.fft.fftfreq(N, 1 / N).astype(int); M1, M2 = np.meshgrid(m, m, indexing="ij"); R = np.sqrt(M1**2 + M2**2)
diag["psi0_spectral_weight_beyond_m16"] = float(P[R >= 16].sum() / P.sum())
diag["kernel_grid_vs_analytic_max_abs_diff"] = float(np.abs(cell.Uk - gz.U_tilde(np.sqrt(cell.Gx**2 + cell.Gy**2))).max())
# what the ladder needs: |omega^2 offset| << (c k_min)^2 with k_min = 0.00117/a*; c unknown pre-Phase-1, so the
# threshold is stated on the stationarity residual that produced the offset (offset/residual ratio measured here).
off = abs(diag["goldstone_offset_product_form"]["n_b=32"]["ka=0.005"][0])
diag["offset_per_unit_residual"] = off / diag["L_psi0_residual_rel"]
diag["PHASE1_STATIONARITY_THRESHOLD_proposed"] = {"L_psi0_residual_rel_max": 1e-10, "goldstone_omega2_offset_abs_max": 1e-8,
    "rationale": "offset scales ~%.0f x residual; at ka=1.17e-3 (k=%.2e) an acoustic omega^2 ~ (c k)^2 is O(1e-6..1e-5) for c = O(1..3); 1%% of that is 1e-8" % (diag["offset_per_unit_residual"], LADDER[-1] / A_STAR)}
substrate_ready = off < 1e-8

# =============================================================== (B) analytic p6m control (harmonic triangular lattice)
TH = np.array([0.0, np.pi / 3, 2 * np.pi / 3])
def D_ctrl(kx, ky):
    D = np.zeros((2, 2))
    for t in TH:
        ax, ay = np.cos(t), np.sin(t); f = 2 * (1 - np.cos(kx * ax + ky * ay))
        D += f * np.outer([ax, ay], [ax, ay])
    return D
def o2_of(khat, e):
    """traceless-strain fraction of S = (i/2)(k e^T + e k^T) (identical formula to the harness's fit_polarisation)."""
    kx, ky = khat; S = 0.5j * np.array([[2 * kx * e[0], kx * e[1] + ky * e[0]], [kx * e[1] + ky * e[0], 2 * ky * e[1]]])
    E2 = S - 0.5 * np.trace(S) * np.eye(2); return float(np.linalg.norm(E2)**2 / np.linalg.norm(S)**2)
def analytic(psi, branch):
    c2 = lambda p, q: sum(np.cos(psi - t)**p * np.sin(psi - t)**q for t in TH)
    if branch == "L": s4, s6, s8 = c2(4, 0), c2(6, 0), c2(8, 0)
    else:             s4, s6, s8 = c2(2, 2), c2(4, 2), c2(6, 2)
    alpha, beta = -s6 / (12 * s4), s8 / (360 * s4)
    return float(np.sqrt(s4)), float(alpha / 2), float(beta / 2 - alpha**2 / 8)
def fit_speed_and_residual(ka, omega):
    """E-4/E-5 pipeline as in the harness: c from omega/k = c + b (ka)^2 on the small-k end, then r = omega/(c k) - 1 fitted on {(ka)^2,(ka)^4}."""
    small = ka <= 0.03
    Xs = np.stack([np.ones(small.sum()), ka[small]**2], axis=1)
    c = float(np.linalg.lstsq(Xs, omega[small] / ka[small], rcond=None)[0][0])
    r = omega / (c * ka) - 1.0
    X = np.stack([ka**2, ka**4], axis=1); coef, *_ = np.linalg.lstsq(X, r, rcond=None)
    return c, float(coef[0]), float(coef[1]), r
def window_ci(ka, omega, edges=(0.3, 0.15, 0.075)):
    full = fit_speed_and_residual(ka, omega)
    return max(abs(fit_speed_and_residual(ka[ka <= e], omega[ka <= e])[1] - full[1]) for e in edges[1:])
ctrl = {"projector_mirror_line_exact": True, "F-CTRL-L": {}, "T_branch_diagnostic_CONTROL_NOT_VERDICT": {}}
kas = np.sort(np.concatenate([LADDER, np.array([0.005, 0.01, 0.015, 0.02, 0.03])]))
for name, psi in (("Gamma-K", 0.0), ("Gamma-M", np.pi / 6)):
    khat = np.array([np.cos(psi), np.sin(psi)])
    wT, wL = [], []
    for ka in kas:
        lam, V = np.linalg.eigh(D_ctrl(*(ka * khat)))
        o2s = [o2_of(khat, V[:, j]) for j in range(2)]
        jT = int(np.argmax(o2s)); jL = 1 - jT
        if not (abs(o2s[jT] - 1.0) < 1e-12 and abs(o2s[jL] - 0.5) < 1e-12): ctrl["projector_mirror_line_exact"] = False
        wT.append(np.sqrt(lam[jT])); wL.append(np.sqrt(lam[jL]))
    wT, wL = np.array(wT), np.array(wL)
    for br, w in (("L", wL), ("T", wT)):
        c, a2, a4, r = fit_speed_and_residual(kas, w); ci = window_ci(kas, w)
        ca, a2a, a4a = analytic(psi, br)
        rec = {"c_fit": c, "c_analytic": ca, "a2_fit": a2, "a2_analytic": a2a, "a4_fit": a4, "a4_analytic": a4a,
               "ci_a2_window": ci, "abs_err_a2": abs(a2 - a2a)}
        if br == "L":
            rec["known_nonzero"] = bool(abs(a2a) > TAU)
            rec["pass"] = bool(abs(a2 - a2a) <= max(ci, TAU) and abs(a2a) > TAU)
            ctrl["F-CTRL-L"][name] = rec
        else:
            ctrl["T_branch_diagnostic_CONTROL_NOT_VERDICT"][name] = rec
# a2 recovery precision of the elected two-term basis on the elected window (the fitter's own bias, control-measured)
ctrl["fitter_a2_bias_max_abs"] = max(v["abs_err_a2"] for v in ctrl["F-CTRL-L"].values())

# =============================================================== (C) F-CTRL-INJ (synthetic)
rng = np.random.default_rng(20260902); a2_inj, noise = 10 * TAU, 1e-8
X = np.stack([LADDER**2, LADDER**4], axis=1)
rec = np.array([np.linalg.lstsq(X, a2_inj * LADDER**2 + noise * rng.standard_normal(len(LADDER)), rcond=None)[0][0] for _ in range(200)])
inj = {"a2_injected": a2_inj, "noise_abs": noise, "a2_recovered_mean": float(rec.mean()), "a2_recovered_sd": float(rec.std()),
       "ci95": [float(np.percentile(rec, 2.5)), float(np.percentile(rec, 97.5))]}
inj["pass"] = bool(abs(rec.mean() - a2_inj) <= TAU and inj["ci95"][0] <= a2_inj <= inj["ci95"][1])

# =============================================================== checkpoint + report
out = {"gate": "G-S2C1", "phase": 0, "leg": "chat", "status": "CONTROL-NOT-VERDICT", "PHASE1_AUTHORIZED": PHASE1_AUTHORIZED,
       "prereg_md5": "2ea8ec13ffa3c32898cc24a3be605c64", "t1_md5": md5b(open("/home/claude/s2c/t1_forbidden_G_S2_ON_CONE.txt", "rb").read()),
       "lock_record_md5": "f2f4d50029fb5be3122a885c48a7e04f", "ladder_ka": [float(x) for x in LADDER], "tau": TAU,
       "A_substrate_diagnostic": diag, "B_analytic_control": ctrl, "C_F_CTRL_INJ": inj,
       "readiness": {"harness_projector_fitter": "READY" if (ctrl["projector_mirror_line_exact"] and all(v["pass"] for v in ctrl["F-CTRL-L"].values()) and inj["pass"]) else "INSTRUMENT-LIMITED",
                     "substrate_gz1_for_acoustic_ladder": "READY" if substrate_ready else "NOT READY — stationarity/Goldstone offset (see A); Phase 1 prerequisite: re-crystallize at gem8 (E-3) to the proposed threshold and verify WARD-Gamma before any ladder"}}
ob = (json.dumps(out, indent=1, sort_keys=True, default=str) + "\n").encode()
open("g_s2c1_phase0_checkpoint.json", "wb").write(ob)
print("=== (A) SUBSTRATE DIAGNOSTIC (recovered gz1 crystal) ===")
print("L psi0 residual (rel) %.4e  (= %.3e x mu; rebuild logged residual_polished 0.00227)" % (diag["L_psi0_residual_rel"], diag["L_psi0_residual_rel_over_mu"]))
print("Ward residual on translation mode (L+2X) d_x psi0: %.4e" % diag["ward_residual_translation_mode_rel"])
for nb, row in diag["goldstone_offset_product_form"].items(): print("product-form lowest omega^2 %s: %s" % (nb, {k: [round(x, 4) for x in v] for k, v in row.items()}))
print("Hermitian-clipped lowest omegas (n_b=32):", {k: [round(x, 6) for x in v] for k, v in diag["hermitian_clipped_lowest"].items()})
print("psi0 spectral weight beyond |m|>=16: %.1e ; kernel grid-vs-analytic max diff: %.1e" % (diag["psi0_spectral_weight_beyond_m16"], diag["kernel_grid_vs_analytic_max_abs_diff"]))
print("offset per unit residual ~ %.0f ; proposed Phase-1 thresholds: %s" % (diag["offset_per_unit_residual"], diag["PHASE1_STATIONARITY_THRESHOLD_proposed"]))
print("=== (B) ANALYTIC p6m CONTROL ===")
print("projector mirror-line exactness (T->1, L->1/2):", "PASS" if ctrl["projector_mirror_line_exact"] else "FAIL")
for n, v in ctrl["F-CTRL-L"].items(): print("F-CTRL-L %-8s c_fit %.6f (an %.6f)  a2_fit %+.6e (an %+.6e) err %.1e ci %.1e -> %s" % (n, v["c_fit"], v["c_analytic"], v["a2_fit"], v["a2_analytic"], v["abs_err_a2"], v["ci_a2_window"], "PASS" if v["pass"] else "FAIL"))
for n, v in ctrl["T_branch_diagnostic_CONTROL_NOT_VERDICT"].items(): print("control-T %-8s a2_fit %+.6e (an %+.6e) a4_fit %+.4e (an %+.4e)" % (n, v["a2_fit"], v["a2_analytic"], v["a4_fit"], v["a4_analytic"]))
print("=== (C) F-CTRL-INJ === injected %.1e recovered %.4e +/- %.1e CI95 %s -> %s" % (a2_inj, inj["a2_recovered_mean"], inj["a2_recovered_sd"], [round(x, 9) for x in inj["ci95"]], "PASS" if inj["pass"] else "FAIL"))
print("READINESS:", out["readiness"])
print("checkpoint g_s2c1_phase0_checkpoint.json md5 %s (%d B)" % (md5b(ob), len(ob)))
