"""
cc_texture.py -- independent re-implementation of the E4 texture survey in the LNR framework
(arXiv:0706.2341 Sec. 4), written from the paper and the E4 report's class definitions only.

Mass matrices (LNR's displayed general forms):
  Dirac(u, u'; c0..c4):  M_ii = c0 u_i u'_i;  O_A={(1,3),(3,2),(2,1)}: c1 u_i u'_j + c2 u_j u'_i;
                         O_B={(1,2),(2,3),(3,1)}: c3 u_i u'_j + c4 u_j u'_i
  Maj(u; a):             diag(u_i^2) + a (u_i u_j)_{i != j}
  M_e = Dirac(phi5, phi10)  (rows L),  M_D = Dirac(phi5, phi1),  M_R = Maj(phi1; alpha),
  M_nu = -M_D M_R^-1 M_D^T,  M_u = Maj(phi10; alpha_u),  M_d = Dirac(phi10, phi5) (rows Q).
Alignments: Z3 (1,1,1); P (e^{if1}, e^{if2}, 1); Z7 (0,0,1); G (x1 e^{if1}, x2 e^{if2}, 1).
Variants: 'min' = LNR leading order (charged sectors c0 only, alpha_u = 0; M_D with c1..c4 = beta);
          'gen' = every invariant an independent complex coupling (c0 = 1 by normalisation).
          Couplings complex in both (my reading of the report); plus a sensitivity variant
          'minreal' (alpha, beta real) that is NOT part of the original survey.
Observables, errors and survival rule as stated in the E4 report. Deterministic (fixed seeds).
Resumable: appends one JSON line per class to out/texture_cc.jsonl.
"""
import json, math, cmath, os, sys, time, zlib, itertools
import numpy as np
from scipy.optimize import least_squares
from scipy.stats import chi2 as chi2dist

base = "/home/user/gifgaf0.github.io/seed/experiments/E4_family_symmetry/crosscheck/out/"
JL = base + "texture_cc.jsonl"

# ---------------------------------------------------------------- data (my own read of the sources)
# Huang & Zhou 2009.04851v2 Tables 2-3, full SM at M_Z
mt, mb, mc, ms, md, mu = 168.26, 2.839, 0.620, 0.05316, 0.00267, 0.00123
dmt, dmb, dmc, dms, dmd, dmu = 0.75, 0.026, 0.017, 0.00461, 0.00019, 0.00021
mtau, mmu, me = 1.72856, 0.101766, 0.48307e-3
dmtau, dmmu, dme = 0.00028, 0.000023, 0.00045e-3
def ratio(a, da, b, db):
    rel = math.hypot(da / a, db / b)
    return a / b, max(rel, 0.10)
LEP_MASS = [ratio(me, dme, mmu, dmmu), ratio(mmu, dmmu, mtau, dmtau)]
QRK_MASS = [ratio(mu, dmu, mc, dmc), ratio(mc, dmc, mt, dmt), ratio(md, dmd, ms, dms), ratio(ms, dms, mb, dmb)]
R_NU = (2.534e-3 / 7.49e-5, (2.534e-3 / 7.49e-5) * math.hypot(0.19 / 7.49, 0.024 / 2.534))
NU = {"s12sq": (0.307, 0.275, 0.345), "s13sq": (0.02195, 0.02023, 0.02376), "s23sq": (0.561, 0.430, 0.596), "delta": (177., 96., 422.)}
CK = [(0.22519, 0.00083), (0.828, 0.011), (0.1609, 0.0095), (0.347, 0.010)]

def apull(name, x):
    bf, lo, hi = NU[name]
    return (x - bf) / ((hi - bf) / 3 if x > bf else (bf - lo) / 3)
def dpull(d):
    if d is None: return 0.0
    return min((apull("delta", d + k * 360) for k in (-1, 0, 1)), key=abs)

# ---------------------------------------------------------------- matrices
OA = [(0, 2), (2, 1), (1, 0)]; OB = [(0, 1), (1, 2), (2, 0)]
def dirac(u, v, c):
    M = np.zeros((3, 3), dtype=complex)
    for i in range(3): M[i, i] = c[0] * u[i] * v[i]
    for (i, j) in OA: M[i, j] = c[1] * u[i] * v[j] + c[2] * u[j] * v[i]
    for (i, j) in OB: M[i, j] = c[3] * u[i] * v[j] + c[4] * u[j] * v[i]
    return M
def maj(u, a):
    M = a * np.outer(u, u)
    for i in range(3): M[i, i] = u[i] ** 2
    return M

ALIGN_NPAR = {"Z3": 0, "P": 2, "Z7": 0, "G": 4}
def vev(kind, p):
    if kind == "Z3": return np.ones(3, dtype=complex)
    if kind == "Z7": return np.array([0, 0, 1], dtype=complex)
    if kind == "P": return np.array([cmath.exp(1j * p[0]), cmath.exp(1j * p[1]), 1])
    if kind == "G": return np.array([math.exp(p[0]) * cmath.exp(1j * p[1]), math.exp(p[2]) * cmath.exp(1j * p[3]), 1])

# ---------------------------------------------------------------- observables
def left_basis(M):
    U, s, Vh = np.linalg.svd(M)
    o = np.argsort(s)
    return U[:, o], s[o]
def mix_angles(U):
    Ua = np.abs(U)
    s13sq = min(Ua[0, 2] ** 2, 1.0); c13sq = 1 - s13sq
    if c13sq < 1e-15: return 0.0, 1.0, 0.0, None
    s12sq = Ua[0, 1] ** 2 / c13sq; s23sq = Ua[1, 2] ** 2 / c13sq
    J = np.imag(U[0, 0] * U[1, 1] * np.conj(U[0, 1]) * np.conj(U[1, 0]))
    s12, s23, s13 = math.sqrt(s12sq), math.sqrt(s23sq), math.sqrt(s13sq)
    c12, c23 = math.sqrt(max(0, 1 - s12sq)), math.sqrt(max(0, 1 - s23sq))
    den = s12 * c12 * s23 * c23 * s13
    if den < 1e-9: return s12sq, s13sq, s23sq, None
    cosd = (Ua[1, 0] ** 2 - s12sq * c23 ** 2 - c12 ** 2 * s23sq * s13sq) / (2 * den)
    sind = J / (den * c13sq)
    return s12sq, s13sq, s23sq, math.degrees(math.atan2(sind, cosd)) % 360

BIG = 1e3
def lepton_obs(Me, Mnu):
    Ue, se = left_basis(Me)
    Un, sn = left_basis(Mnu)
    Un = Un.conj()                     # nu^T M nu convention: M = U* diag U^dagger
    if se[2] <= 0 or se[0] / se[2] < 1e-14 or sn[2] <= 0: return None
    U = Ue.conj().T @ Un
    a = mix_angles(U)
    d21, d31 = sn[1] ** 2 - sn[0] ** 2, sn[2] ** 2 - sn[0] ** 2
    r = d31 / d21 if d21 > 1e-14 * sn[2] ** 2 else 1e12
    return dict(me_mmu=se[0] / se[1], mmu_mtau=se[1] / se[2], r=r, s12sq=a[0], s13sq=a[1], s23sq=a[2], delta=a[3],
                gap_e=min(np.diff(se)) / se[2], rank_e=se[0] / se[2], gap_nu=min(np.diff(sn)) / sn[2])
def lepton_res(o):
    if o is None: return np.full(7, BIG)
    res = [math.log(max(o["me_mmu"], 1e-300) / LEP_MASS[0][0]) / LEP_MASS[0][1],
           math.log(max(o["mmu_mtau"], 1e-300) / LEP_MASS[1][0]) / LEP_MASS[1][1],
           (min(o["r"], 1e6) - R_NU[0]) / R_NU[1],
           apull("s12sq", o["s12sq"]), apull("s13sq", o["s13sq"]), apull("s23sq", o["s23sq"]), dpull(o["delta"])]
    return np.array(res)
def ckm_obs(V):
    Va = np.abs(V)
    den = math.hypot(Va[0, 0], Va[0, 1])
    lam = Va[0, 1] / den if den > 1e-15 else 0.0
    A = Va[1, 2] / (lam * Va[0, 1]) if lam * Va[0, 1] > 1e-15 else 1e6
    x = V[1, 0] * np.conj(V[1, 2])
    z = -(V[0, 0] * np.conj(V[0, 2])) / x if abs(x) > 1e-15 else 1e6
    return lam, A, z.real, z.imag
def quark_obs(Mu, Md):
    Uu, su = left_basis(Mu); Ud, sd = left_basis(Md)
    if su[2] <= 0 or sd[2] <= 0 or su[0] / su[2] < 1e-14 or sd[0] / sd[2] < 1e-14: return None
    V = Uu.conj().T @ Ud
    lam, A, rb, eb = ckm_obs(V)
    return dict(mu_mc=su[0] / su[1], mc_mt=su[1] / su[2], md_ms=sd[0] / sd[1], ms_mb=sd[1] / sd[2], lam=lam, A=A, rhob=rb, etab=eb,
                gap_u=min(np.diff(su)) / su[2], gap_d=min(np.diff(sd)) / sd[2], rank_u=su[0] / su[2], rank_d=sd[0] / sd[2],
                perm=float(np.min(np.max(np.abs(V), axis=1))))
def quark_res(o):
    if o is None: return np.full(8, BIG)
    ms_ = [o["mu_mc"], o["mc_mt"], o["md_ms"], o["ms_mb"]]
    res = [math.log(max(x, 1e-300) / t[0]) / t[1] for x, t in zip(ms_, QRK_MASS)]
    res += [(min(max(v, -1e6), 1e6) - t[0]) / t[1] for v, t in zip((o["lam"], o["A"], o["rhob"], o["etab"]), CK)]
    return np.array(res)

# ---------------------------------------------------------------- classes
def cplx(p, k):  # complex from two reals
    return complex(p[k], p[k + 1])

def make_lepton(var, a5, a10, a1):
    n5, n10, n1 = ALIGN_NPAR[a5], ALIGN_NPAR[a10], ALIGN_NPAR[a1]
    if var == "gen": ncoup = 8 + 8 + 2
    elif var == "min": ncoup = 2 + 2
    elif var == "minreal": ncoup = 2
    npar = n5 + n10 + n1 + ncoup
    def build(p):
        i = 0
        u5 = vev(a5, p[i:i + n5]); i += n5
        u10 = vev(a10, p[i:i + n10]); i += n10
        u1 = vev(a1, p[i:i + n1]); i += n1
        if var == "gen":
            ce = [1] + [cplx(p, i + 2 * k) for k in range(4)]; i += 8
            cd = [1] + [cplx(p, i + 2 * k) for k in range(4)]; i += 8
            al = cplx(p, i); i += 2
        else:
            ce = [1, 0, 0, 0, 0]
            if var == "min":
                al = cplx(p, i); be = cplx(p, i + 2); i += 4
            else:
                al = p[i]; be = p[i + 1]; i += 2
            cd = [1, be, be, be, be]
        Me = dirac(u5, u10, ce)
        MD = dirac(u5, u1, cd)
        MR = maj(u1, al)
        return Me, MD, MR
    def obs(p):
        Me, MD, MR = build(p)
        if abs(np.linalg.det(MR)) < 1e-13 * max(1e-300, np.abs(MR).max() ** 3): return None, dict(MR_singular=True)
        Mnu = -MD @ np.linalg.solve(MR, MD.T)
        o = lepton_obs(Me, Mnu)
        return o, dict(MR_singular=False)
    return npar, obs

def make_lnr_exact():
    # phi5 = (-1,1,1), phi1 = (1,1,1), beta = -1, alpha real free; phi10 = G (moduli matter only); min charged sector
    def obs(p):
        u10 = vev("G", [p[0], 0.0, p[1], 0.0]); al = p[2]
        u5 = np.array([-1, 1, 1], dtype=complex); u1 = np.ones(3, dtype=complex)
        Me = dirac(u5, u10, [1, 0, 0, 0, 0])
        MD = dirac(u5, u1, [1, -1, -1, -1, -1]); MR = maj(u1, al)
        if abs(np.linalg.det(MR)) < 1e-13: return None, dict(MR_singular=True)
        return lepton_obs(Me, -MD @ np.linalg.solve(MR, MD.T)), dict(MR_singular=False)
    return 3, obs

def make_quark(var, a10, a5):
    n10, n5 = ALIGN_NPAR[a10], ALIGN_NPAR[a5]
    ncoup = 2 + 8 if var == "gen" else 0
    npar = n10 + n5 + ncoup
    def obs(p):
        i = 0
        u10 = vev(a10, p[i:i + n10]); i += n10
        u5 = vev(a5, p[i:i + n5]); i += n5
        if var == "gen":
            au = cplx(p, i); i += 2
            cdd = [1] + [cplx(p, i + 2 * k) for k in range(4)]
        else:
            au = 0; cdd = [1, 0, 0, 0, 0]
        Mu = maj(u10, au); Md = dirac(u10, u5, cdd)
        return quark_obs(Mu, Md), {}
    return npar, obs

def classes(include_minreal=False):
    out = []
    al = ["Z3", "P", "Z7", "G"]
    vars_l = ["min", "gen"] + (["minreal"] if include_minreal else [])
    for var in vars_l:
        for a5, a10, a1 in itertools.product(al, al, al):
            out.append((f"lep:{var}:phi5={a5},phi10={a10},phi1={a1}", "lepton") + make_lepton(var, a5, a10, a1))
    if not include_minreal or True:
        out.append(("lep:LNR-exact(alpha free, phi10=G moduli)", "lepton") + make_lnr_exact())
    for var in ["min", "gen"]:
        for a10, a5 in itertools.product(al, al):
            out.append((f"qrk:{var}:phi10={a10},phi5={a5}", "quark") + make_quark(var, a10, a5))
    return out

# ---------------------------------------------------------------- tools
def random_point(rng, npar):
    # phases uniform, log-moduli N(0,1.5), coupling real/imag parts N(0,1.5): crude but generic
    return rng.normal(0, 1.5, npar) + rng.uniform(0, 2 * math.pi, npar) * (rng.random(npar) < 0.5)

def residual_fn(sector, obs):
    def f(p):
        o, _ = obs(p)
        return lepton_res(o) if sector == "lepton" else quark_res(o)
    return f

def structural(sector, obs, npar, rng, npts=40):
    dead_all, reasons = True, set()
    for _ in range(npts):
        p = rng.normal(0, 1.0, npar) + rng.uniform(-math.pi, math.pi, npar) * 0.5
        o, extra = obs(p)
        why = []
        if sector == "lepton":
            if extra.get("MR_singular"): why.append("M_R singular")
            elif o is None: why.append("M_e rank<3")
            else:
                if o["rank_e"] < 1e-9: why.append("M_e rank<3")
                if o["gap_e"] < 1e-9: why.append("M_e degenerate pair")
                if o["gap_nu"] < 1e-9: why.append("light nu degenerate pair")
        else:
            if o is None: why.append("M_u or M_d rank<3")
            else:
                if o["gap_u"] < 1e-9 or o["gap_d"] < 1e-9: why.append("M_u/M_d degenerate pair")
                if o["perm"] > 1 - 1e-9: why.append("CKM is a permutation")
        if not why: dead_all = False
        reasons |= set(why)
    return dead_all, sorted(reasons)

def n_eff(f, npar, rng, npts=4, p_best=None):
    best = 0
    pts = [rng.normal(0, 1.0, npar) for _ in range(npts)] + ([p_best] if p_best is not None else [])
    for p in pts:
        h = 1e-6
        f0 = f(p)
        if np.any(np.abs(f0) >= BIG): continue
        Jm = np.zeros((len(f0), npar))
        for k in range(npar):
            e = np.zeros(npar); e[k] = h
            Jm[:, k] = (f(p + e) - f(p - e)) / (2 * h)
        s = np.linalg.svd(Jm, compute_uv=False)
        if s[0] == 0: continue
        best = max(best, int((s > 1e-6 * s[0]).sum()))
    return best

def fit(f, npar, rng, nstart, nfev_start=200, nfev_polish=1000):
    best = (np.inf, None)
    for k in range(nstart):
        p0 = random_point(rng, npar)
        try:
            r = least_squares(f, p0, method="trf", x_scale=1.0, max_nfev=nfev_start * (npar + 1), xtol=1e-12, ftol=1e-12, gtol=1e-12)
        except Exception:
            continue
        c = float(np.sum(r.fun ** 2))
        if c < best[0]: best = (c, r.x.copy())
        if c < 1e-12: break
    if best[1] is not None and nfev_polish:
        r = least_squares(f, best[1], method="trf", x_scale=1.0, max_nfev=nfev_polish * (npar + 1), xtol=1e-14, ftol=1e-14, gtol=1e-14)
        c = float(np.sum(r.fun ** 2))
        if c < best[0]: best = (c, r.x.copy())
    return best

def done_names():
    if not os.path.exists(JL): return set()
    return {json.loads(l)["name"] for l in open(JL) if l.strip()}

def main():
    global JL
    include_minreal = "--minreal" in sys.argv
    if include_minreal: JL = base + "texture_cc_minreal.jsonl"   # sensitivity variant, separate file
    cls = classes(include_minreal)
    done = done_names()
    t0 = time.time()
    for name, sector, npar, obs in cls:
        if name in done: continue
        if include_minreal and ":minreal:" not in name: continue
        seed = zlib.crc32(("cc" + name).encode())
        rng = np.random.default_rng(seed)
        dead, why = structural(sector, obs, npar, rng)
        f = residual_fn(sector, obs)
        nobs = 7 if sector == "lepton" else 8
        if npar == 0:
            c = float(np.sum(f(np.zeros(0)) ** 2)); px = np.zeros(0)
        else:
            if dead: c, px = fit(f, npar, rng, 3, nfev_start=100, nfev_polish=0)
            else: c, px = fit(f, npar, rng, 60 if npar <= 5 else 12)   # small classes: cheap, more starts (poles in alpha)
        ne = n_eff(f, npar, rng, p_best=px) if npar > 0 else 0
        dof = nobs - ne
        if dead: verdict = "excluded (structural)"
        elif dof >= 1: verdict = "SURVIVES" if (1 - chi2dist.cdf(c, dof)) > 0.01 else "excluded"
        else: verdict = "accommodates (no prediction)" if c < 1 else "excluded"
        o = None
        if px is not None:
            oo, _ = obs(px)
            o = {k: (v if not isinstance(v, (np.floating,)) else float(v)) for k, v in (oo or {}).items()}
        rec = dict(name=name, sector=sector, npar=npar, n_eff=ne, dof=dof, chi2=c, verdict=verdict, structural_dead=dead,
                   why=why, best_obs=o, best_p=None if px is None else list(map(float, px)),
                   pulls=None if px is None else list(map(float, f(px))) if npar > 0 else list(map(float, f(np.zeros(0)))))
        with open(JL, "a") as fh: fh.write(json.dumps(rec) + "\n")
        print(f"[{time.time() - t0:7.1f}s] {name:55s} npar={npar:2d} neff={ne} chi2={c:11.4g} {verdict} {why if dead else ''}", flush=True)

if __name__ == "__main__":
    main()
