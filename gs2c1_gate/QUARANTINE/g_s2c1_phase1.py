#!/usr/bin/env python3
"""g_s2c1_phase1.py — Gate G-S2C1 (display: Gate G-S2-ON-CONE), PHASE 1 (chat leg).
Lock: prereg 2ea8ec13ffa3c32898cc24a3be605c64; T1 8cd89b9a82704accd89f7ff6f5e220b4; lock record f2f4d500;
Phase-0 checkpoint eae2bbd734f5129dd1e51efcbb55dd3d. PHASE1_AUTHORIZED = True (author directive, Sept 2, 2026).

Substrate (E-3, record §2.91.K G-TSH3 first passing): 2-D GP, hbar = m = 1, GEM-8 kernel U(r) = g exp(-r^8),
g* = 20, hexagonal (p6m) cell a* = 1.46059, mu = 53.225, rho0 ~ 1 (substrate units throughout, T4).
Energy E[psi] = int 1/2|grad psi|^2 + 1/2 int int rho U rho - mu int rho  (gz1 convention).

Steps (directive 1-4):
 1. RE-CRYSTALLIZATION at fixed mu: semi-implicit imaginary time, then Newton-Krylov polish to
    ||L psi0|| / ||psi0|| <= 1e-10  (L = -1/2 lap - mu + U*rho0).  HALT if not reached.
 2. WARD-Gamma: un-clipped product-form BdG omega^2 = eig(L(L+2X)) at Gamma and ka = 0.005; the three
    Goldstone modes must satisfy |omega^2| <= 1e-8.  HALT if not.
 3. LADDER: dyadic ka in [0.3/2^8, 0.3] (E-4), directions Gamma-K and Gamma-M, n_b in {32, 40}; Hermitian
    BdG form (admissible only because lambda_min(L) >= -1e-12 after the polish; cross-checked against the
    product form at two rungs); eigenvectors -> density-fluctuation amplitude psi0*f -> polarisation fit onto
    {d_x rho0, d_y rho0, rho0} -> o2 (traceless-strain fraction); T = branch of maximal o2 (>= theta_id 0.90);
    c = lim omega/k from the speed set; r(k) = omega_T/(c k) - 1 fitted on {(ka)^2,(ka)^4}; window-stability CI.
 4. CHECKPOINT (F-DISP / F-ISO / F-MIX / F-CONV evaluated chat-side; arms NOT declared — two-leg + Phase 2/3).
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
psi = np.load("/home/claude/s2c/gz1/psi0_polished_n64.npy").astype(float)
psi /= np.sqrt((psi * psi).mean())
log("seed residual %.3e" % residual(psi))
# semi-implicit imaginary time at FIXED mu: (1 + dt/2 K2) psi_new = psi + dt*(mu psi - (U*rho) psi)
dt = 0.004; denom = 1.0 + 0.5 * dt * K2
for it in range(1, 40001):
    rhs = psi + dt * (MU * psi - conv(psi * psi) * psi)
    psi_new = np.fft.ifft2(np.fft.fft2(rhs) / denom).real
    if not np.all(np.isfinite(psi_new)): log("imaginary-time blow-up — halving dt"); dt *= 0.5; denom = 1.0 + 0.5 * dt * K2; continue
    psi = psi_new
    if it % 2000 == 0:
        res = residual(psi); log("  imag-time it %5d residual %.3e <rho> %.6f" % (it, res, (psi * psi).mean()))
        if res < 1e-7: break
res_it = residual(psi); log("imaginary-time done: residual %.3e, <rho> = %.6f" % (res_it, (psi * psi).mean()))
# Newton-Krylov polish to the strict threshold
def F(v): return Lop(v.reshape(N, N), v.reshape(N, N)).ravel()
x = psi.ravel().copy(); res_nk = res_it
for rnd in range(6):
    try:
        x = newton_krylov(F, x, f_tol=1e-14, f_rtol=1e-14, maxiter=30, method="lgmres", inner_maxiter=60, verbose=False)
    except Exception as e:
        log("newton_krylov round %d ended: %s" % (rnd, str(e)[:80]))
    res_nk = residual(x.reshape(N, N)); log("  NK round %d residual %.3e" % (rnd, res_nk))
    if res_nk <= THR_RES: break
psi0 = x.reshape(N, N)
rho0 = psi0 * psi0; mean_rho = float(rho0.mean())
coef = np.fft.fft2(psi0) / N**2; P = np.abs(coef)**2
m = np.fft.fftfreq(N, 1 / N).astype(int); M1, M2 = np.meshgrid(m, m, indexing="ij"); R = np.sqrt(M1**2 + M2**2)
spec24 = float(P[R >= 24].sum() / P.sum())
E_kin = 0.5 * np.sum(K2 * np.abs(coef)**2); rhat = np.fft.fft2(rho0) / N**2; E_int = 0.5 * np.sum(cell.Uk * np.abs(rhat)**2)
step1 = {"residual_imaginary_time": res_it, "residual_after_NK": res_nk, "threshold": THR_RES, "pass": bool(res_nk <= THR_RES),
         "mean_rho": mean_rho, "energy_per_area_kin": float(E_kin), "energy_per_area_int": float(E_int),
         "psi0_spectral_weight_beyond_m24": spec24, "psi0_md5": md5b(psi0.tobytes()), "grid_n": N,
         "bragg_peak_ratio_rho": float(np.sort(np.abs(rhat).ravel())[-2] / np.abs(rhat[0, 0]))}
np.save("psi0_gem8_n64.npy", psi0)
log("STEP 1 %s: residual %.3e (thr %.0e), <rho> %.6f, spectral tail(|m|>=24) %.1e" % ("PASS" if step1["pass"] else "FAIL", res_nk, THR_RES, mean_rho, spec24))
if not step1["pass"]:
    json.dump({"step1": step1, "halt": "RE-CRYSTALLIZATION THRESHOLD NOT REACHED"}, open("g_s2c1_phase1_checkpoint.json", "w"), indent=1); sys.exit(2)

# ------------------------------------------------------------------ BdG (plane waves) with the gem8 kernel
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

# ------------------------------------------------------------------ 2. WARD-Gamma
b32 = BdG(32)
w2G = b32.product_w2(np.array([0.0, 0.0])); w2k = b32.product_w2(np.array([0.005 / A_STAR, 0.0]))
lam_min_G = float(np.linalg.eigvalsh(b32.LX(np.array([0.0, 0.0]))[0])[0])
ward = {"product_form_w2_Gamma_3lowest": [[float(z.real), float(z.imag)] for z in w2G],
        "product_form_w2_ka0.005_3lowest": [[float(z.real), float(z.imag)] for z in w2k],
        "lambda_min_L_Gamma": lam_min_G, "threshold_abs_w2": THR_WARD,
        "pass": bool(max(abs(z) for z in w2G) <= THR_WARD and lam_min_G >= -1e-12)}
log("STEP 2 WARD-Gamma %s: |w2| at Gamma %s ; lambda_min(L) %.2e" % ("PASS" if ward["pass"] else "FAIL", ["%.2e" % abs(z) for z in w2G], lam_min_G))
if not ward["pass"]:
    json.dump({"step1": step1, "step2_ward": ward, "halt": "WARD-GAMMA FAILED"}, open("g_s2c1_phase1_checkpoint.json", "w"), indent=1); sys.exit(2)

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
def run(n_b):
    bdg = BdG(n_b); out = {"n_b": n_b, "speeds": {}, "T": {}, "L1": {}, "ident": {}, "fmix_min_o2_T": {}, "lam_min_L_min": 0.0, "xcheck_product_vs_hermitian": {}}
    for d in ("GK", "GM"):
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
        log("  [%s n_b=%d] T: a2 = %+.6e (ci %.1e)  a4 = %+.6e (ci %.1e)  rms %.1e | L1 control: a2 = %+.6e | min o2(T) %.4f" % (d, n_b, out["T"][d]["a2"], out["T"][d]["ci_a2"], out["T"][d]["a4"], out["T"][d]["ci_a4"], out["T"][d]["fit_rms"], out["L1"][d]["a2"], out["fmix_min_o2_T"][d]))
    return out
runs = {}
for n_b in (32, 40):
    log("=== ladder n_b = %d ===" % n_b); runs[str(n_b)] = run(n_b)
r32, r40 = runs["32"], runs["40"]
conv = {}
for d in ("GK", "GM"):
    for nm in ("T", "L1", "PH"): conv["c_%s_%s_rel" % (nm, d)] = abs(r40["speeds"][d][nm] / r32["speeds"][d][nm] - 1.0)
    conv["a2_T_%s_abs" % d] = abs(r40["T"][d]["a2"] - r32["T"][d]["a2"]); conv["a4_T_%s_abs" % d] = abs(r40["T"][d]["a4"] - r32["T"][d]["a4"])
fconv_pass = all(conv["c_T_%s_rel" % d] <= 1e-6 and conv["a2_T_%s_abs" % d] <= 1e-7 for d in ("GK", "GM"))
iso_T = abs(r40["speeds"]["GK"]["T"] / r40["speeds"]["GM"]["T"] - 1.0)
fmix_pass = all(r40["fmix_min_o2_T"][d] >= THETA_ID for d in ("GK", "GM"))
fdisp = {d: {"a2": r40["T"][d]["a2"], "a4": r40["T"][d]["a4"], "ci_a2": r40["T"][d]["ci_a2"], "ci_a4": r40["T"][d]["ci_a4"],
             "a2_zero_at_tau": bool(abs(r40["T"][d]["a2"]) <= max(TAU, r40["T"][d]["ci_a2"])), "a4_zero_at_tau": bool(abs(r40["T"][d]["a4"]) <= max(TAU, r40["T"][d]["ci_a4"]))} for d in ("GK", "GM")}
ck = {"gate": "G-S2C1", "phase": 1, "leg": "chat", "PHASE1_AUTHORIZED": True, "prereg_md5": "2ea8ec13ffa3c32898cc24a3be605c64",
      "t1_md5": "8cd89b9a82704accd89f7ff6f5e220b4", "lock_record_md5": "f2f4d50029fb5be3122a885c48a7e04f", "phase0_md5": "eae2bbd734f5129dd1e51efcbb55dd3d",
      "substrate": {"kernel": "GEM-8 g exp(-r^8), 2-D", "g": G_STAR, "a_star": A_STAR, "mu": MU, "grid_n": N, "kernel_U0": KER.U0},
      "step1_recrystallization": step1, "step2_ward_gamma": ward, "step3_ladder": {"ladder_ka": LADDER, "speed_ka": SPEED, "runs": runs},
      "F_CONV_32_vs_40": conv, "F_CONV_pass": fconv_pass, "F_ISO_cT_split": iso_T, "F_ISO_pass": bool(iso_T <= THETA_ISO),
      "F_MIX_pass": fmix_pass, "F_DISP_chatleg": fdisp, "tau": TAU, "theta_id": THETA_ID, "theta_iso": THETA_ISO,
      "arms": "NOT DECLARED — two-leg comparison (CC) and Phase 2/3 (aggregate) pending; chat-leg single-crystal result only"}
ob = (json.dumps(ck, indent=1, sort_keys=True, default=str) + "\n").encode(); open("g_s2c1_phase1_checkpoint.json", "wb").write(ob)
log("F-CONV 32->40: " + ", ".join("%s=%.2e" % kv for kv in conv.items()) + "  -> %s" % ("PASS" if fconv_pass else "FAIL"))
log("F-ISO c_T split GK/GM = %.3e -> %s ; F-MIX min o2(T) %s -> %s" % (iso_T, "PASS" if iso_T <= THETA_ISO else "FAIL", r40["fmix_min_o2_T"], "PASS" if fmix_pass else "FAIL"))
for d in ("GK", "GM"): log("F-DISP chat-leg %s: a2 = %+.6e (ci %.1e) zero@tau=%s ; a4 = %+.6e (ci %.1e) zero@tau=%s" % (d, fdisp[d]["a2"], fdisp[d]["ci_a2"], fdisp[d]["a2_zero_at_tau"], fdisp[d]["a4"], fdisp[d]["ci_a4"], fdisp[d]["a4_zero_at_tau"]))
log("checkpoint g_s2c1_phase1_checkpoint.json md5 %s (%d B) ; psi0_gem8_n64.npy md5 %s" % (md5b(ob), len(ob), step1["psi0_md5"]))
