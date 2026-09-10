#!/usr/bin/env python3
"""g_s2c1_phase1_ladder.py — Gate G-S2C1 (display: Gate G-S2-ON-CONE), PHASE 1 LADDER (chat leg).
Lock: prereg 2ea8ec13; T1 8cd89b9a; lock record f2f4d500; ADDENDUM A-1 8bf51bd0 (WARD-Gamma redefined:
(a) analytic-mode Ward residual <= 1e-9 AND (b) Hermitian-form Goldstone |omega^2| <= 1e-8 with lambda_min(L) >= -1e-12
at EVERY k). Author directive September 3, 2026. PHASE1_AUTHORIZED = True.
Derived from the halted g_s2c1_phase1.py (c987a1a6): kernel table, hex cell, GP operators, BdG (Hermitian form of record
with eigenvectors; product-form cross-check), polarisation fit, classifier, kvec, fit_r copied VERBATIM. Step 1 replaced by
loading the banked gem8 state psi0_gem8_n64.npy (array md5 asserted b27fa004...; residual re-verified <= 1e-10). Step 2 = A-1.
Ladder at n_b in {24, 32, 40}; product-form cross-checks at LADDER[0] and LADDER[4]; F-CONV across 24/32/40; the dense floor
enters the a2 CI through the n_b-change term. T1 self-scan at start. Substrate units throughout.
"""
import sys, os, json, hashlib, time
import numpy as np
from scipy.integrate import quad
from scipy.special import j0, gamma as Gamma
from scipy.interpolate import CubicSpline
from scipy.optimize import newton_krylov
sys.path.insert(0, "/home/claude/s2c/gz1")
import gz1_core as gz
PHASE1_AUTHORIZED = True
T0 = time.time()
def log(s): print("[%7.1fs] %s" % (time.time() - T0, s), flush=True)
def md5b(b): return hashlib.md5(b).hexdigest()

G_STAR, A_STAR, MU = 20.0, 1.46059, 53.225
N = 64
TAU, THETA_ID, THETA_ISO = 1e-6, 0.90, 0.01
LADDER = [0.3 / 2**j for j in range(9)]
SPEED = [0.005, 0.01, 0.015, 0.02, 0.03]
THR_RES, THR_WARD = 1e-10, 1e-8

# ------------------------------------------------------------------ 1. gem8 kernel (2-D FT, table + spline)
class Gem8_2D:
    """U_tilde(q) = 2 pi g int_0^inf r exp(-r^8) J0(q r) dr ; U_tilde(0) = 2 pi g Gamma(1/4)/8."""
    def __init__(self, g, qmax=200.0, nq=4001):
        self.g = g; self.U0 = 2 * np.pi * g * Gamma(0.25) / 8.0
        qt = np.linspace(0.0, qmax, nq); vals = np.empty_like(qt); vals[0] = self.U0
        for i, q in enumerate(qt[1:], 1):
            v, _ = quad(lambda r: r * np.exp(-r**8) * j0(q * r), 0.0, 2.5, limit=400, epsabs=1e-13, epsrel=1e-12)
            vals[i] = 2 * np.pi * g * v
        self.spline = CubicSpline(qt, vals); self.qmax = qmax
    def __call__(self, q):
        q = np.asarray(q, float); return np.where(q > self.qmax, 0.0, self.spline(np.minimum(q, self.qmax)))
log("building gem8 kernel table")
KER = Gem8_2D(G_STAR)
cell = gz.Cell(A_STAR, N); cell.Uk = KER(np.sqrt(cell.G2))     # override the soft-disk kernel on the cell grid
K2 = cell.G2
log("kernel U(0) = %.6f ; U(|b1|) = %.6f" % (KER.U0, KER(np.linalg.norm(cell.b1))))

# ------------------------------------------------------------------ GP operators on the hex cell (fractional grid, FFT)
def conv(field): return np.fft.ifft2(cell.Uk * np.fft.fft2(field)).real
def Lop(psi, f):
    """(L f) = -1/2 lap f - mu f + (U*rho0) f  with rho0 = psi^2."""
    return np.fft.ifft2(0.5 * K2 * np.fft.fft2(f)).real - MU * f + conv(psi * psi) * f
def residual(psi):
    r = Lop(psi, psi); return float(np.sqrt((r * r).mean() / (psi * psi).mean()))

# seed: gz1 polished state (hex, one peak per cell) reused as the initial guess, renormalised to <rho> = 1

# ------------------------------------------------------------------ 1. banked gem8 state (Phase 1 item 1, PASSED)
psi0 = np.load("/home/claude/s2c/psi0_gem8_n64.npy").astype(float)
assert hashlib.md5(psi0.tobytes()).hexdigest() == "b27fa00495ef686b0184ea29c455b4db", "banked psi0 md5 mismatch"
rho0 = psi0 * psi0
res0 = residual(psi0)
assert res0 <= THR_RES, "banked state residual %.3e > %.1e" % (res0, THR_RES)
step1 = {"psi0_md5": "b27fa00495ef686b0184ea29c455b4db", "residual_reverified": float(res0), "mean_rho": float(rho0.mean()), "source": "Phase-1 item 1 (halt report b0e6790c)"}
log("STEP 1 banked state: residual %.3e <= %.0e ; <rho> = %.6f" % (res0, THR_RES, rho0.mean()))

class BdG:
    def __init__(self, n_b):
        self.n_b = n_b; n = N
        c = np.fft.fft2(psi0) / n**2; rc = np.fft.fft2(rho0) / n**2; Vc = cell.Uk * rc
        mm = np.fft.fftfreq(n_b, d=1.0 / n_b).astype(int); MM1, MM2 = np.meshgrid(mm, mm, indexing="ij")
        self.m1, self.m2 = MM1.ravel(), MM2.ravel()
        def look(C, d1, d2):
            out = np.zeros(d1.shape, complex); ok = (np.abs(d1) < n // 2) & (np.abs(d2) < n // 2)
            out[ok] = C[d1[ok] % n, d2[ok] % n]; return out
        D1 = self.m1[:, None] - self.m1[None, :]; D2 = self.m2[:, None] - self.m2[None, :]
        self.P = look(c, D1, D2); self.P = 0.5 * (self.P + self.P.conj().T)
        self.V = look(Vc, D1, D2); self.V = 0.5 * (self.V + self.V.conj().T)
        self.kgx0 = self.m1 * cell.b1[0] + self.m2 * cell.b2[0]; self.kgy0 = self.m1 * cell.b1[1] + self.m2 * cell.b2[1]
    def LX(self, k):
        kgx, kgy = k[0] + self.kgx0, k[1] + self.kgy0
        L = np.diag(0.5 * (kgx**2 + kgy**2) - MU) + self.V; L = 0.5 * (L + L.conj().T)
        D = KER(np.sqrt(kgx**2 + kgy**2)); X = self.P @ (D[:, None] * self.P); X = 0.5 * (X + X.conj().T)
        return L, X
    def product_w2(self, k, nlow=3):
        L, X = self.LX(k); w2 = np.linalg.eigvals(L @ (L + 2 * X)); i = np.argsort(w2.real)[:nlow]; return w2[i]
    def modes(self, k, nbands=8):
        L, X = self.LX(k); lam, U = np.linalg.eigh(L); lam_min = float(lam[0])
        lam = np.where(lam < 0, 0.0, lam)                       # admissible only when lam_min >= -1e-12 (checked)
        Lh = (U * np.sqrt(lam)) @ U.conj().T
        M = Lh @ (L + 2.0 * X) @ Lh; M = 0.5 * (M + M.conj().T)
        w2, H = np.linalg.eigh(M); idx = np.argsort(w2)[:nbands]
        w = np.sqrt(np.clip(w2[idx], 0.0, None)); Fv = Lh @ H[:, idx]      # f = u + v
        amps = []
        for j in range(len(idx)):
            cf = np.zeros((N, N), complex); ok = (np.abs(self.m1) < N // 2) & (np.abs(self.m2) < N // 2)
            cf[self.m1[ok] % N, self.m2[ok] % N] = Fv[ok, j]
            amps.append(psi0 * (np.fft.ifft2(cf) * N**2))
        return w, amps, lam_min, w2[idx]


# ------------------------------------------------------------------ 2. WARD-Gamma per ADDENDUM A-1
def cell_grad0(field):
    Fh = np.fft.fft2(field); return np.fft.ifft2(1j * cell.Gx * Fh).real, np.fft.ifft2(1j * cell.Gy * Fh).real
def pw(field, bdg):
    c = np.fft.fft2(field) / N**2; v = np.zeros(len(bdg.m1), complex)
    ok = (np.abs(bdg.m1) < N // 2) & (np.abs(bdg.m2) < N // 2); v[ok] = c[bdg.m1[ok] % N, bdg.m2[ok] % N]; return v
dpx, dpy = cell_grad0(psi0)
ward = {"A1_threshold_analytic": 1e-9, "A1_threshold_hermitian_w2": 1e-8, "lambda_min_L_floor": -1e-12, "by_nb": {}}
BDGS = {nb: BdG(nb) for nb in (24, 32, 40)}
for nb, bdg in BDGS.items():
    L0, X0 = bdg.LX(np.array([0.0, 0.0])); M0 = L0 + 2 * X0
    vx, vy = pw(dpx, bdg), pw(dpy, bdg)
    wa = {"dx": float(np.linalg.norm(M0 @ vx) / np.linalg.norm(vx)), "dy": float(np.linalg.norm(M0 @ vy) / np.linalg.norm(vy))}
    w, amps, lmn, w2 = bdg.modes(np.array([0.0, 0.0]), nbands=4)
    pf = bdg.product_w2(np.array([0.0, 0.0]), nlow=3)
    ward["by_nb"][str(nb)] = {"analytic_ward_residual": wa, "hermitian_goldstone_abs_w2_max": float(np.max(np.abs(w2[:3]))),
                              "hermitian_w2_4lowest": [float(x) for x in w2], "lambda_min_L_Gamma": lmn,
                              "product_form_abs_w2_max_xcheck": float(max(abs(z) for z in pf)),
                              "pass_a": bool(max(wa.values()) <= 1e-9), "pass_b": bool(np.max(np.abs(w2[:3])) <= 1e-8 and lmn >= -1e-12)}
    log("STEP 2 A-1 n_b=%d: (a) analytic Ward %.2e/%.2e ; (b) Hermitian Goldstone |w2| max %.2e, lambda_min(L) %+.2e ; product x-check %.2e -> %s" % (
        nb, wa["dx"], wa["dy"], ward["by_nb"][str(nb)]["hermitian_goldstone_abs_w2_max"], lmn, ward["by_nb"][str(nb)]["product_form_abs_w2_max_xcheck"],
        "PASS" if (ward["by_nb"][str(nb)]["pass_a"] and ward["by_nb"][str(nb)]["pass_b"]) else "FAIL"))
ward["pass_all_nb"] = bool(all(v["pass_a"] and v["pass_b"] for v in ward["by_nb"].values()))
if not ward["pass_all_nb"]:
    json.dump({"step1": step1, "step2_ward_A1": ward, "halt": "WARD-Gamma (A-1) FAILED at Gamma"}, open("g_s2c1_phase1_ladder_checkpoint.json", "w"), indent=1); sys.exit(2)
LAM_FLOOR_VIOLATIONS = []   # (b) is enforced at EVERY k inside run() via lam_min tracking

# ------------------------------------------------------------------ 3. ladder

def cell_grad(field):
    Fh = np.fft.fft2(field); return np.fft.ifft2(1j * cell.Gx * Fh).real, np.fft.ifft2(1j * cell.Gy * Fh).real
DRX, DRY = cell_grad(rho0)
BASIS = np.stack([DRX.ravel(), DRY.ravel(), rho0.ravel()], axis=1).astype(complex)
def polarisation(w_amp, k):
    cf, *_ = np.linalg.lstsq(BASIS, w_amp.ravel(), rcond=None)
    resid = w_amp.ravel() - BASIS @ cf; R2 = 1.0 - np.vdot(resid, resid).real / np.vdot(w_amp.ravel(), w_amp.ravel()).real
    a = cf[:2]; gs = np.linalg.norm(BASIS[:, :2] @ a)**2 / max(np.linalg.norm(BASIS @ cf)**2, 1e-300)
    kx, ky = k; S = 0.5j * np.array([[2 * kx * a[0], kx * a[1] + ky * a[0]], [kx * a[1] + ky * a[0], 2 * ky * a[1]]])
    E2 = S - 0.5 * np.trace(S) * np.eye(2); nS = np.linalg.norm(S)**2
    return float(R2), float(gs), (float(np.linalg.norm(E2)**2 / nS) if nS > 0 else float("nan"))
def classify(k, w, amps):
    rows = []
    for j in range(len(w)):
        R2, gs, o2 = polarisation(amps[j], k); rows.append(dict(j=j, omega=float(w[j]), R2=R2, grad_share=gs, o2=o2))
    lat = [r for r in rows if r["R2"] >= 0.90 and r["grad_share"] >= 0.5]
    T = max(lat, key=lambda r: r["o2"]) if lat else None
    Ls = [r for r in lat if r is not T and r["o2"] < THETA_ID]; L1 = min(Ls, key=lambda r: r["omega"]) if Ls else None
    others = [r for r in rows if r is not T and r is not L1]; PH = min(others, key=lambda r: r["omega"]) if others else None
    return rows, T, L1, PH
def kvec(ka, d):
    k = ka / A_STAR; th = 0.0 if d == "GK" else -np.pi / 6.0; return np.array([k * np.cos(th), k * np.sin(th)])
def fit_r(ka, r):
    X = np.stack([ka**2, ka**4], axis=1); cf, *_ = np.linalg.lstsq(X, r, rcond=None)
    return float(cf[0]), float(cf[1]), float(np.sqrt(np.mean((r - X @ cf)**2)))
def run(n_b, dirs=("GK", "GM")):
    bdg = BdG(n_b); out = {"n_b": n_b, "speeds": {}, "T": {}, "L1": {}, "ident": {}, "fmix_min_o2_T": {}, "lam_min_L_min": 0.0, "xcheck_product_vs_hermitian": {}}
    for d in dirs:
        cT, cL, cP, kas = [], [], [], []
        for ka in SPEED:
            k = kvec(ka, d); w, amps, lmn, _ = bdg.modes(k); out["lam_min_L_min"] = min(out["lam_min_L_min"], lmn)
            rows, T, L1, PH = classify(k, w, amps)
            if T is None or L1 is None or PH is None: log("  [%s %d ka=%.4f] classification incomplete %s" % (d, n_b, ka, [(r["j"], round(r["R2"], 3), round(r["o2"], 3)) for r in rows[:5]])); continue
            kas.append(ka); cT.append(T["omega"] / (ka / A_STAR)); cL.append(L1["omega"] / (ka / A_STAR)); cP.append(PH["omega"] / (ka / A_STAR))
        X = np.stack([np.ones(len(kas)), np.array(kas)**2], axis=1); sp = {}
        for nm, arr in (("T", cT), ("L1", cL), ("PH", cP)): sp[nm] = float(np.linalg.lstsq(X, np.array(arr), rcond=None)[0][0])
        out["speeds"][d] = sp; log("  [%s n_b=%d] speeds k->0: PH %.5f  T %.5f  L1 %.5f  (R_T = c_T/c_L1 = %.5f)" % (d, n_b, sp["PH"], sp["T"], sp["L1"], sp["T"] / sp["L1"]))
        rT, rL, used, o2T = [], [], [], []
        for ka in LADDER:
            k = kvec(ka, d); w, amps, lmn, w2 = bdg.modes(k); out["lam_min_L_min"] = min(out["lam_min_L_min"], lmn)
            rows, T, L1, PH = classify(k, w, amps)
            if T is None or L1 is None: log("  [%s n_b=%d ladder ka=%.5f] classification incomplete — dropped, logged" % (d, n_b, ka)); continue
            used.append(ka); rT.append(T["omega"] / (sp["T"] * ka / A_STAR) - 1.0); rL.append(L1["omega"] / (sp["L1"] * ka / A_STAR) - 1.0); o2T.append(T["o2"])
            out["ident"].setdefault(d, []).append(dict(ka=ka, T=dict(j=T["j"], omega=T["omega"], R2=round(T["R2"], 5), o2=round(T["o2"], 5)), L1=dict(j=L1["j"], omega=L1["omega"], o2=round(L1["o2"], 5)), PH=dict(j=PH["j"], omega=PH["omega"]) if PH else None))
            if ka in (LADDER[0], LADDER[4]):
                pw2 = bdg.product_w2(k, nlow=4); out["xcheck_product_vs_hermitian"]["%s_ka=%.4f" % (d, ka)] = {"product": [float(z.real) for z in pw2], "hermitian": [float(z) for z in w2[:4]]}
        ka_u = np.array(used)
        for nm, r in (("T", rT), ("L1", rL)):
            a2, a4, rms = fit_r(ka_u, np.array(r))
            edges = (0.3, 0.15, 0.075); cis = [fit_r(ka_u[ka_u <= e], np.array(r)[ka_u <= e]) for e in edges[1:]]
            out[nm][d] = dict(ka=used, r=[float(x) for x in r], a2=a2, a4=a4, fit_rms=rms, ci_a2=max(abs(c[0] - a2) for c in cis), ci_a4=max(abs(c[1] - a4) for c in cis))
        out["fmix_min_o2_T"][d] = float(min(o2T))
        # A-1 explicit floor term: sigma_r(ka) = floor_w2(n_b) / (2 omega_T^2); weighted LSQ reported ALONGSIDE the elected unweighted fit
        floor_w2 = ward["by_nb"][str(n_b)]["hermitian_goldstone_abs_w2_max"]
        omT = np.array([e["T"]["omega"] for e in out["ident"][d]]); sig = floor_w2 / (2.0 * omT**2)
        Xw = np.stack([ka_u**2, ka_u**4], axis=1) / sig[:, None]; cw, *_ = np.linalg.lstsq(Xw, np.array(rT) / sig, rcond=None)
        out["T"][d]["a2_floor_weighted"] = float(cw[0]); out["T"][d]["a4_floor_weighted"] = float(cw[1]); out["T"][d]["floor_sigma_r"] = [float(x) for x in sig]
        # framework label convention (G-TSH3): c_L1 = the higher of the two non-T gapless speeds
        out["speeds"][d]["c_L1_framework"] = max(sp["L1"], sp["PH"]); out["speeds"][d]["R_T_framework"] = sp["T"] / max(sp["L1"], sp["PH"])
        log("  [%s n_b=%d] T floor-weighted: a2_w = %+.6e  a4_w = %+.6e ; R_T(framework label) = %.5f" % (d, n_b, cw[0], cw[1], out["speeds"][d]["R_T_framework"]))
        log("  [%s n_b=%d] T: a2 = %+.6e (ci %.1e)  a4 = %+.6e (ci %.1e)  rms %.1e | L1 control: a2 = %+.6e | min o2(T) %.4f" % (d, n_b, out["T"][d]["a2"], out["T"][d]["ci_a2"], out["T"][d]["a4"], out["T"][d]["ci_a4"], out["T"][d]["fit_rms"], out["L1"][d]["a2"], out["fmix_min_o2_T"][d]))
    return out

import argparse
ap = argparse.ArgumentParser(); ap.add_argument("--stage", required=True)   # nb24 | nb32 | nb40GK | nb40GM | assemble
args = ap.parse_args()
def stage_file(tag): return "s2c1_ladder_stage_%s.json" % tag
if args.stage.startswith("nb"):
    nb = int(args.stage[2:4]); dirs = ("GK", "GM") if len(args.stage) == 4 else (args.stage[4:],)
    log("=== ladder stage %s: n_b = %d dirs %s ===" % (args.stage, nb, dirs))
    out = run(nb, dirs); out["ward"] = ward; out["step1"] = step1
    ob = (json.dumps(out, indent=1, sort_keys=True, default=str) + "\n").encode(); open(stage_file(args.stage), "wb").write(ob)
    log("stage %s written md5 %s (%d B)" % (args.stage, md5b(ob), len(ob))); sys.exit(0)
# ---- assemble: merge stage files
def load(tag): return json.load(open(stage_file(tag)))
runs = {"24": load("nb24"), "32": load("nb32")}
g40, m40 = load("nb40GK"), load("nb40GM")
r40m = {"n_b": 40, "speeds": {**g40["speeds"], **m40["speeds"]}, "T": {**g40["T"], **m40["T"]}, "L1": {**g40["L1"], **m40["L1"]},
        "ident": {**g40["ident"], **m40["ident"]}, "fmix_min_o2_T": {**g40["fmix_min_o2_T"], **m40["fmix_min_o2_T"]},
        "lam_min_L_min": min(g40["lam_min_L_min"], m40["lam_min_L_min"]), "xcheck_product_vs_hermitian": {**g40["xcheck_product_vs_hermitian"], **m40["xcheck_product_vs_hermitian"]}}
runs["40"] = r40m
stage_md5 = {t: md5b(open(stage_file(t), "rb").read()) for t in ("nb24", "nb32", "nb40GK", "nb40GM")}
LAM_FLOOR_VIOLATIONS = [(nb, runs[str(nb)]["lam_min_L_min"]) for nb in (24, 32, 40) if runs[str(nb)]["lam_min_L_min"] < -1e-12]

r24, r32, r40 = runs["24"], runs["32"], runs["40"]
conv = {}
for d in ("GK", "GM"):
    for nm in ("T", "L1", "PH"):
        conv["c_%s_%s_rel_32v40" % (nm, d)] = abs(r40["speeds"][d][nm] / r32["speeds"][d][nm] - 1.0)
        conv["c_%s_%s_rel_24v32" % (nm, d)] = abs(r32["speeds"][d][nm] / r24["speeds"][d][nm] - 1.0)
    conv["a2_T_%s_abs_32v40" % d] = abs(r40["T"][d]["a2"] - r32["T"][d]["a2"]); conv["a2_T_%s_abs_24v32" % d] = abs(r32["T"][d]["a2"] - r24["T"][d]["a2"])
    conv["a4_T_%s_abs_32v40" % d] = abs(r40["T"][d]["a4"] - r32["T"][d]["a4"])
fconv_pass = all(conv["c_T_%s_rel_32v40" % d] <= 1e-6 and conv["a2_T_%s_abs_32v40" % d] <= 1e-7 for d in ("GK", "GM"))
iso_T = abs(r40["speeds"]["GK"]["T"] / r40["speeds"]["GM"]["T"] - 1.0)
fmix_pass = all(r40["fmix_min_o2_T"][d] >= THETA_ID for d in ("GK", "GM"))
fdisp = {}
for d in ("GK", "GM"):
    a2, a4 = r40["T"][d]["a2"], r40["T"][d]["a4"]
    ci2 = max(r40["T"][d]["ci_a2"], conv["a2_T_%s_abs_32v40" % d], conv["a2_T_%s_abs_24v32" % d])   # window + basis (dense-floor) terms, A-1
    ci4 = max(r40["T"][d]["ci_a4"], conv["a4_T_%s_abs_32v40" % d])
    fdisp[d] = {"a2": a2, "a4": a4, "ci_a2_total": ci2, "ci_a4_total": ci4, "a2_zero_at_tau": bool(abs(a2) <= max(TAU, ci2)),
                "a4_zero_at_tau": bool(abs(a4) <= max(TAU, ci4)), "a2_resolved_nonzero": bool(abs(a2) > max(TAU, ci2)), "a4_resolved_nonzero": bool(abs(a4) > max(TAU, ci4))}
def arm_indication(d):
    f = fdisp[d]
    if r40["fmix_min_o2_T"][d] < THETA_ID: return "A4 CHANNEL-UNDEFINED (F-MIX)"
    if not fconv_pass or LAM_FLOOR_VIOLATIONS: return "A5 INSTRUMENT-LIMITED (F-CONV / lambda_min floor)"
    if f["a2_resolved_nonzero"]: return "A3 DISPERSIVE-O(k^2)"
    if f["a2_zero_at_tau"] and f["a4_resolved_nonzero"]: return "A2 ON-CONE-PROTECTED-O(k^4)"
    if f["a2_zero_at_tau"] and f["a4_zero_at_tau"]: return "A1 ON-CONE-EXACT (single-crystal P1 only; P2 aggregate pending)"
    return "A5 INSTRUMENT-LIMITED at tau (CI > tau, a2 unresolved)"
arms = {d: arm_indication(d) for d in ("GK", "GM")}
rel_conv = {d: {"a2_rel_32v40": abs(r40["T"][d]["a2"] - r32["T"][d]["a2"]) / abs(r40["T"][d]["a2"]), "a2_rel_24v32": abs(r32["T"][d]["a2"] - r24["T"][d]["a2"]) / abs(r32["T"][d]["a2"]),
                "a2w_rel_32v40": abs(r40["T"][d]["a2_floor_weighted"] - r32["T"][d]["a2_floor_weighted"]) / abs(r40["T"][d]["a2_floor_weighted"]),
                "a2w_rel_24v32": abs(r32["T"][d]["a2_floor_weighted"] - r24["T"][d]["a2_floor_weighted"]) / abs(r32["T"][d]["a2_floor_weighted"]),
                "a2_floor_weighted_nb40": r40["T"][d]["a2_floor_weighted"], "a4_floor_weighted_nb40": r40["T"][d]["a4_floor_weighted"],
                "sign_stable_all_nb": bool(np.sign(r24["T"][d]["a2"]) == np.sign(r32["T"][d]["a2"]) == np.sign(r40["T"][d]["a2"]) == np.sign(r40["T"][d]["a2_floor_weighted"]))} for d in ("GK", "GM")}
ck = {"gate": "G-S2C1", "phase": "1-ladder", "leg": "chat", "PHASE1_AUTHORIZED": True, "prereg_md5": "2ea8ec13ffa3c32898cc24a3be605c64",
      "t1_md5": "8cd89b9a82704accd89f7ff6f5e220b4", "lock_record_md5": "f2f4d50029fb5be3122a885c48a7e04f", "addendum_A1_md5": "8bf51bd05c691f3f03d796b231cdd262",
      "phase0_md5": "eae2bbd734f5129dd1e51efcbb55dd3d", "phase1_halt_checkpoint_md5": "eeedcfa594a24915fa9c10c6abbd0a4e", "stage_file_md5": stage_md5,
      "substrate": {"kernel": "GEM-8 g exp(-r^8), 2-D", "g": G_STAR, "a_star": A_STAR, "mu": MU, "grid_n": N, "kernel_U0": KER.U0},
      "step1_banked_state": step1, "step2_ward_gamma_A1": ward, "lambda_min_floor_violations_in_ladder": LAM_FLOOR_VIOLATIONS,
      "step3_ladder": {"ladder_ka": LADDER, "speed_ka": SPEED, "runs": runs},
      "F_CONV": conv, "F_CONV_pass": fconv_pass, "F_ISO_cT_split": iso_T, "F_ISO_pass": bool(iso_T <= THETA_ISO),
      "F_MIX_min_o2_T": r40["fmix_min_o2_T"], "F_MIX_pass": fmix_pass, "F_DISP_chatleg": fdisp, "tau": TAU, "theta_id": THETA_ID, "theta_iso": THETA_ISO,
      "arm_indication_chatleg": arms, "a2_relative_convergence_and_weighted": rel_conv, "R_T_framework_label_nb40": {d: r40["speeds"][d]["R_T_framework"] for d in ("GK", "GM")}, "registered_expectation": "DISPERSIVE (Eddington trap 4)",
      "verdict": "NOT DECLARED — two-leg (CC) comparison and Phase 2/3 (aggregate) pending; chat-leg single-crystal INDICATION only"}
ob = (json.dumps(ck, indent=1, sort_keys=True, default=str) + "\n").encode(); open("g_s2c1_phase1_ladder_checkpoint.json", "wb").write(ob)
log("F-CONV: " + ", ".join("%s=%.2e" % kv for kv in conv.items() if "T_" in kv[0] or "c_T" in kv[0]) + "  -> %s" % ("PASS" if fconv_pass else "FAIL"))
log("F-ISO c_T split GK/GM = %.3e -> %s ; F-MIX min o2(T) %s -> %s ; lambda floor violations %s" % (iso_T, "PASS" if iso_T <= THETA_ISO else "FAIL", r40["fmix_min_o2_T"], "PASS" if fmix_pass else "FAIL", LAM_FLOOR_VIOLATIONS))
for d in ("GK", "GM"): log("F-DISP chat-leg %s: a2 = %+.6e (CI %.1e) ; a4 = %+.6e (CI %.1e) -> %s" % (d, fdisp[d]["a2"], fdisp[d]["ci_a2_total"], fdisp[d]["a4"], fdisp[d]["ci_a4_total"], arms[d]))
for d in ("GK", "GM"): log("a2 relative convergence %s: unweighted 24v32 %.2e 32v40 %.2e | floor-weighted 24v32 %.2e 32v40 %.2e | sign stable %s" % (d, rel_conv[d]["a2_rel_24v32"], rel_conv[d]["a2_rel_32v40"], rel_conv[d]["a2w_rel_24v32"], rel_conv[d]["a2w_rel_32v40"], rel_conv[d]["sign_stable_all_nb"]))
log("checkpoint g_s2c1_phase1_ladder_checkpoint.json md5 %s (%d B)" % (md5b(ob), len(ob)))
