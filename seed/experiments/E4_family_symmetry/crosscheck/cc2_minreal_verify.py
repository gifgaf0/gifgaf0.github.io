"""
cc2_minreal_verify.py -- second-pass, independent verification of the sensitivity found in the first
cross-check pass: LNR's 'min' lepton classes with REAL alpha, beta (LNR's own convention, alpha = beta = -1
integers; phases only in the vevs) contain classes that fit NuFIT 6.0 with dof = 1.

Independent of cc_texture.py (no import): own mass matrices (from the exact invariant forms of
cc2_exact_invariants.py), own observable extraction (eigh of hermitian squares; delta from the
|U_tau1|^2 invariant and the sign of J, i.e. a different rephasing invariant than |U_mu1|^2), own fits.

Reduction used (exact for the 'min' variant): the charged-lepton matrix is diag(u5_i u10_i); with
phi10 = G its two moduli reproduce m_e/m_mu and m_mu/m_tau exactly and its ordering selects any row
permutation of U_nu.  So chi2_total = min over 6 row orders of chi2_nu(neutrino parameters), and
N_eff = 2 + rank d(r, s12, s13, s23, delta)/d(neutrino parameters).

Classes (neutrino parameters): A: phi5 = Z3, phi1 = P (f1, f2, alpha, beta)
                               B: phi5 = P,  phi1 = Z3 (g1, g2, alpha, beta)
                               C: phi5 = P,  phi1 = P (g1, g2, f1, f2, alpha, beta)
Each with real (alpha, beta) and, for comparison, complex (alpha, beta).
Writes out/minreal_verify_cc2.json.
"""
import json, math, cmath, itertools
import numpy as np
from scipy.optimize import least_squares
from scipy.stats import chi2 as chi2dist

OUT, CHECKS = {}, {}
def check(name, ok):
    CHECKS[name] = bool(ok); print(("PASS " if ok else "FAIL ") + name)

# NuFIT 6.0, IC19 w/o SK-atm, NO (Table 1, read in 2410.05380v1): bf, 3sigma low, 3sigma high
NF = {"s12": (0.307, 0.275, 0.345), "s13": (0.02195, 0.02023, 0.02376), "s23": (0.561, 0.430, 0.596), "d": (177.0, 96.0, 422.0)}
RN = 2.534e-3 / 7.49e-5; SR = RN * math.hypot(0.19 / 7.49, 0.024 / 2.534)
def pull(k, x):
    bf, lo, hi = NF[k]
    return (x - bf) / ((hi - bf) / 3 if x > bf else (bf - lo) / 3)
def dpull(d):  # delta respects the 3sigma interval 96..422: use the representative closest in pull
    return min((pull("d", d + 360 * k) for k in (-1, 0, 1)), key=abs)

def dirac(up, u, c):
    M = np.zeros((3, 3), complex)
    for i in range(3): M[i, i] = c[0] * up[i] * u[i]
    for (i, j) in ((0, 1), (1, 2), (2, 0)): M[i, j] = c[1] * up[i] * u[j] + c[2] * up[j] * u[i]
    for (i, j) in ((0, 2), (1, 0), (2, 1)): M[i, j] = c[3] * up[i] * u[j] + c[4] * up[j] * u[i]
    return M
def maj(u, a):
    M = a * np.outer(u, u)
    np.fill_diagonal(M, u ** 2)
    return M
def Pvev(g1, g2): return np.array([cmath.exp(1j * g1), cmath.exp(1j * g2), 1.0])
ONE = np.ones(3, complex)

def nu_obs(Mnu, perm):
    # holomorphic convention nu^T M nu: M = U* diag U^dagger  ->  U = eigenvectors of M^dagger M
    H = Mnu.conj().T @ Mnu
    m2, U = np.linalg.eigh(H)                 # ascending masses^2 -> normal ordering labels 1,2,3
    U = U[list(perm), :]
    a = np.abs(U) ** 2
    s13 = a[0, 2]; c13 = 1 - s13
    s12 = a[0, 1] / c13; s23 = a[1, 2] / c13
    J = np.imag(U[0, 0] * U[1, 1] * np.conj(U[0, 1]) * np.conj(U[1, 0]))
    c12, c23 = 1 - s12, 1 - s23
    den = 2 * math.sqrt(max(0.0, s12 * c12 * s23 * c23 * s13))
    # |U_tau1|^2 = s12 s23 + c12 c23 s13 - 2 sqrt(...) cos(delta)
    cosd = (s12 * s23 + c12 * c23 * s13 - a[2, 0]) / den if den > 1e-12 else 1.0
    cosd = max(-1.0, min(1.0, cosd))
    d = math.degrees(math.acos(cosd))
    if J < 0: d = 360 - d
    r = (m2[2] - m2[0]) / (m2[1] - m2[0]) if m2[1] - m2[0] > 1e-300 else 1e9
    return dict(r=r, s12=s12, s13=s13, s23=s23, d=d, J=J, m=np.sqrt(np.abs(m2)))

def make(cls, cplx):
    # parameter vector: vev phases, then alpha, beta (real) or (Re a, Im a, Re b, Im b)
    nv = {"A": 2, "B": 2, "C": 4}[cls]
    def build(p):
        if cls == "A": u5, u1 = ONE, Pvev(p[0], p[1])
        if cls == "B": u5, u1 = Pvev(p[0], p[1]), ONE
        if cls == "C": u5, u1 = Pvev(p[0], p[1]), Pvev(p[2], p[3])
        q = p[nv:]
        a, b = (complex(q[0], q[1]), complex(q[2], q[3])) if cplx else (q[0], q[1])
        MD = dirac(u5, u1, [1, b, b, b, b]); MR = maj(u1, a)
        return -MD @ np.linalg.solve(MR, MD.T)
    return nv + (4 if cplx else 2), build

def residuals(build, perm):
    def f(p):
        try:
            o = nu_obs(build(p), perm)
        except (np.linalg.LinAlgError, ValueError, ZeroDivisionError):
            return np.full(5, 1e3)
        if not all(np.isfinite([o["r"], o["s12"], o["s13"], o["s23"], o["d"]])):
            return np.full(5, 1e3)
        return np.array([(min(o["r"], 1e6) - RN) / SR, pull("s12", o["s12"]), pull("s13", o["s13"]), pull("s23", o["s23"]), dpull(o["d"])])
    return f

def rank(f, p, h=1e-6):
    J = np.array([(f(p + h * e) - f(p - h * e)) / (2 * h) for e in np.eye(len(p))]).T
    s = np.linalg.svd(J, compute_uv=False)
    return int((s > 1e-7 * s[0]).sum()), s

PERMS = list(itertools.permutations(range(3)))
CK = "/home/user/gifgaf0.github.io/seed/experiments/E4_family_symmetry/crosscheck/out/minreal_verify_cc2.ckpt.jsonl"
import os
res_all = {}
if os.path.exists(CK):
    for line in open(CK):
        if line.strip():
            q = json.loads(line); res_all[q["label"]] = q["rec"]
for cls in ("A", "B", "C"):
    for cplx in (False, True):
        npar, build = make(cls, cplx)
        if f"{cls}/{'complex' if cplx else 'real'}" in res_all:
            print("  (checkpoint) class", f"{cls}/{'complex' if cplx else 'real'}", {k: res_all[f"{cls}/{'complex' if cplx else 'real'}"][k] for k in ("N_eff", "dof", "chi2", "p")}, flush=True)
            continue
        rng = np.random.default_rng(1000 + ord(cls) + 7 * cplx)
        best = (np.inf, None, None)
        for perm in PERMS:
            f = residuals(build, perm)
            for _ in range(40):
                p0 = np.concatenate([rng.uniform(-math.pi, math.pi, npar - (4 if cplx else 2)), rng.normal(0, 1.5, 4 if cplx else 2)])
                r = least_squares(f, p0, method="trf" if len(p0) > 5 else "lm", xtol=1e-13, ftol=1e-13, max_nfev=4000)
                c = float(np.sum(r.fun ** 2))
                if c < best[0]: best = (c, r.x.copy(), perm)
        c, px, perm = best
        f = residuals(build, perm)
        # generic rank at several random points and at the best fit
        rk = max([rank(f, px)[0]] + [rank(f, np.concatenate([rng.uniform(-3, 3, npar - (4 if cplx else 2)), rng.normal(0, 1, 4 if cplx else 2)]))[0] for _ in range(4)])
        neff = 2 + rk; dof = 7 - neff
        p = float(1 - chi2dist.cdf(c, dof)) if dof >= 1 else None
        o = nu_obs(build(px), perm)
        lab = f"{cls}/{'complex' if cplx else 'real'}"
        res_all[lab] = dict(npar_nu=npar, rank_nu=rk, N_eff=neff, dof=dof, chi2=c, p=p, perm=perm, best_p=px.tolist(),
                            obs={k: (float(v) if k != "m" else list(map(float, v))) for k, v in o.items()},
                            pulls=list(map(float, f(px))))
        with open(CK, "a") as fh: fh.write(json.dumps(dict(label=lab, rec=res_all[lab]), default=str) + "\n")
        print(f"  class {lab:10s} npar_nu={npar} rank={rk} N_eff={neff} dof={dof} chi2={c:.4g} p={p} "
              f"r={o['r']:.3f} s12={o['s12']:.4f} s13={o['s13']:.5f} s23={o['s23']:.4f} delta={o['d']:.1f}", flush=True)
OUT["classes"] = res_all
A, B, C = res_all["A/real"], res_all["B/real"], res_all["C/real"]
check("real (alpha, beta): class A (phi5=Z3, phi1=P) has N_eff = 6 (dof 1) and fits with p > 0.01", A["dof"] == 1 and A["p"] > 0.01)
check("real (alpha, beta): class B (phi5=P, phi1=Z3) has N_eff = 6 (dof 1) and fits with p > 0.01", B["dof"] == 1 and B["p"] > 0.01)
check("real (alpha, beta): class C (phi5=P, phi1=P) has dof >= 1 and fits with p > 0.01", C["dof"] >= 1 and C["p"] > 0.01)
check("complex (alpha, beta) (the original's convention): classes A, B, C have dof = 0 (accommodate only)",
      all(res_all[f"{k}/complex"]["dof"] == 0 and res_all[f"{k}/complex"]["chi2"] < 1 for k in "ABC"))
check("first-pass minima (A/real 0.395, B/real 0.444, from cc_minreal_detail) reached or improved (chi2 <= first pass + 0.05)",
      A["chi2"] <= 0.395 + 0.05 and B["chi2"] <= 0.444 + 0.05)
OUT["checks"] = CHECKS; OUT["all_pass"] = all(CHECKS.values())
json.dump(OUT, open("/home/user/gifgaf0.github.io/seed/experiments/E4_family_symmetry/crosscheck/out/minreal_verify_cc2.json", "w"), indent=1, default=str)
print(f"\n{sum(CHECKS.values())}/{len(CHECKS)} checks pass")
