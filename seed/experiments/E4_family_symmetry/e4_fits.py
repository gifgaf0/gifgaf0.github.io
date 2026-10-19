"""
e4_fits.py -- E4 part 4: texture survey with least-squares fits (F21, Luhn-Nasri-Ramond framework).

Framework (LNR, arXiv:0706.2341): all fermions in the F21 triplet 3, one antitriplet familon per
SU(5) multiplet (phi10 for Q, u^c, e^c; phi5 for L, d^c; phi1 for nu^c), Higgs flavour singlets,
masses from the dimension-6 operators  psi psi' H xi xi'  (five F21 invariants for psi != psi',
two for psi = psi').  Mass matrices (rows = left-handed fields):
    M_e  = Dirac(u = <phi5>, u' = <phi10>; c^e)      M_D = Dirac(<phi5>, <phi1>; c^D)
    M_R  = Majorana(<phi1>; alpha)                    M_nu = -M_D M_R^-1 M_D^T
    M_u  = Majorana-type, symmetric (<phi10>; alpha_u) M_d = Dirac(<phi10>, <phi5>; c^d)
    Dirac(u,u';c):  M_ii = c0 u_i u'_i;  M_ij = c1 u_i u'_j + c2 u_j u'_i on O_A, c3 .. + c4 .. on O_B.
Texture class = alignment of each familon vev, from the vacua of the F21 familon potential
(LNR Sec. 3.2) plus a generic option:
    Z3 : (1,1,1)                      residual Z3, kappa > 0 vacuum with equal phases (0 params)
    P  : (e^{i f1}, e^{i f2}, 1)      kappa > 0 vacuum manifold, phases free; contains LNR's (-1,1,1) (2)
    Z7 : (0,0,1)                      kappa < 0 vacuum, ray fixed by Z7 (0)
    G  : generic (x1 e^{i f1}, x2 e^{i f2}, 1)   no alignment ("Cabibbo haze" by hand) (4)
and a coupling variant:
    min : LNR leading order (charged sectors: I3 only, c = (1,0,0,0,0); Dirac nu: c1=c2=c3=c4=beta)
    gen : all invariants with independent complex couplings (c0 = 1).
Plus the named class "LNR exact": phi10 = G, phi5 = (-1,1,1), phi1 = (1,1,1), beta = -1, alpha real.

Observables: leptons (7) me/mmu, mmu/mtau, r = Dm31^2/Dm21^2 (normal ordering), s12^2, s13^2, s23^2,
delta; quarks (8) mu/mc, mc/mt, md/ms, ms/mb, lambda, A, rhobar, etabar.  Errors: data_targets.py.
Survival rule (fixed before fitting): N_eff = rank of d(observables)/d(parameters) (generic);
dof = N_obs - N_eff.  dof >= 1: survives if p(chi2_min, dof) > 0.01.  dof <= 0: "accommodates"
(fits but predicts nothing) if chi2_min < 1, otherwise fails.
Run: python3 e4_fits.py   (checkpoints to out/fits.jsonl, log in out/fits.log; ~10-30 min on 1 core)
"""
import itertools
import json
import math
import os
import sys
import time
import zlib

import numba as nb
import numpy as np
from scipy.optimize import least_squares
from scipy.stats import chi2 as chi2dist

from data_targets import NUFIT, RATIOS, R_ATM_SOL, R_ATM_SOL_ERR, UTFIT

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
os.makedirs(OUT, exist_ok=True)
JSONL = os.path.join(OUT, "fits.jsonl")
LOG = os.path.join(OUT, "fits.log")

CODES = {"Z3": 0, "P": 1, "Z7": 2, "G": 3}
NPAR_ALIGN = {0: 0, 1: 2, 2: 0, 3: 4}

# observable targets as arrays for numba
LEP_T = np.array([RATIOS["me/mmu"][0], RATIOS["mmu/mtau"][0], R_ATM_SOL, NUFIT["s12sq"][0], NUFIT["s13sq"][0],
                  NUFIT["s23sq"][0], NUFIT["delta_deg"][0]])
LEP_LO = np.array([RATIOS["me/mmu"][1], RATIOS["mmu/mtau"][1], R_ATM_SOL_ERR, NUFIT["s12sq"][1], NUFIT["s13sq"][1],
                   NUFIT["s23sq"][1], NUFIT["delta_deg"][1]])
LEP_HI = np.array([RATIOS["me/mmu"][1], RATIOS["mmu/mtau"][1], R_ATM_SOL_ERR, NUFIT["s12sq"][2], NUFIT["s13sq"][2],
                   NUFIT["s23sq"][2], NUFIT["delta_deg"][2]])
Q_T = np.array([RATIOS["mu/mc"][0], RATIOS["mc/mt"][0], RATIOS["md/ms"][0], RATIOS["ms/mb"][0],
                UTFIT["lambda"][0], UTFIT["A"][0], UTFIT["rhobar"][0], UTFIT["etabar"][0]])
Q_S = np.array([RATIOS["mu/mc"][1], RATIOS["mc/mt"][1], RATIOS["md/ms"][1], RATIOS["ms/mb"][1],
                UTFIT["lambda"][1], UTFIT["A"][1], UTFIT["rhobar"][1], UTFIT["etabar"][1]])
LEP_NAMES = ["me/mmu", "mmu/mtau", "r=Dm31^2/Dm21^2", "s12^2", "s13^2", "s23^2", "delta_deg"]
Q_NAMES = ["mu/mc", "mc/mt", "md/ms", "ms/mb", "lambda", "A", "rhobar", "etabar"]
CAP = 1e3


@nb.njit(cache=True)
def flavon(p, idx, code):
    u = np.zeros(3, dtype=np.complex128)
    if code == 0:
        u[0] = 1.0; u[1] = 1.0; u[2] = 1.0
    elif code == 1:
        u[0] = np.exp(1j * p[idx]); u[1] = np.exp(1j * p[idx + 1]); u[2] = 1.0
        idx += 2
    elif code == 2:
        u[2] = 1.0
    else:
        u[0] = np.exp(p[idx]) * np.exp(1j * p[idx + 2])
        u[1] = np.exp(p[idx + 1]) * np.exp(1j * p[idx + 3])
        u[2] = 1.0
        idx += 4
    return u, idx


@nb.njit(cache=True)
def dirac(u, up, c):
    M = np.zeros((3, 3), dtype=np.complex128)
    for i in range(3):
        M[i, i] = c[0] * u[i] * up[i]
    # O_A = (0,2),(2,1),(1,0)   O_B = (0,1),(1,2),(2,0)
    for (i, j) in ((0, 2), (2, 1), (1, 0)):
        M[i, j] = c[1] * u[i] * up[j] + c[2] * u[j] * up[i]
    for (i, j) in ((0, 1), (1, 2), (2, 0)):
        M[i, j] = c[3] * u[i] * up[j] + c[4] * u[j] * up[i]
    return M


@nb.njit(cache=True)
def majorana(u, alpha):
    M = np.zeros((3, 3), dtype=np.complex128)
    for i in range(3):
        for j in range(3):
            if i == j:
                M[i, j] = u[i] * u[i]
            else:
                M[i, j] = alpha * u[i] * u[j]
    return M


@nb.njit(cache=True)
def coupl(p, idx, variant, kind):
    """kind 0: charged Dirac (min: I3 only); kind 1: neutrino Dirac (min: beta); returns c(5), idx."""
    c = np.zeros(5, dtype=np.complex128)
    c[0] = 1.0
    if variant == 0:
        if kind == 1:
            b = p[idx] + 1j * p[idx + 1]
            idx += 2
            for k in range(1, 5):
                c[k] = b
    else:
        for k in range(1, 5):
            c[k] = p[idx] + 1j * p[idx + 1]
            idx += 2
    return c, idx


@nb.njit(cache=True)
def mix_obs(U):
    a = np.abs(U) ** 2
    s13 = a[0, 2]
    c13 = 1.0 - s13
    s12 = a[0, 1] / c13 if c13 > 1e-15 else 0.0
    s23 = a[1, 2] / c13 if c13 > 1e-15 else 0.0
    J = (U[1, 2] * np.conj(U[0, 2]) * U[0, 1] * np.conj(U[1, 1])).imag
    den = 2.0 * math.sqrt(s12 * (1 - s12) * s23 * (1 - s23) * s13)
    if den > 1e-14:
        cosd = (a[1, 0] - s12 * (1 - s23) - (1 - s12) * s23 * s13) / den
        sind = J / (den / 2.0 * c13)
        if cosd > 1.0:
            cosd = 1.0
        if cosd < -1.0:
            cosd = -1.0
        d = math.degrees(math.atan2(sind, cosd)) % 360.0
    else:
        d = np.nan
    return s12, s13, s23, d


@nb.njit(cache=True)
def lepton_obs(p, a10, a5, a1, variant, lnr_exact):
    idx = 0
    u10, idx = flavon(p, idx, a10)
    if lnr_exact:
        u5 = np.array([-1.0 + 0j, 1.0 + 0j, 1.0 + 0j])
        u1 = np.array([1.0 + 0j, 1.0 + 0j, 1.0 + 0j])
        ce = np.zeros(5, dtype=np.complex128); ce[0] = 1.0
        cD = np.zeros(5, dtype=np.complex128); cD[0] = 1.0
        for k in range(1, 5):
            cD[k] = -1.0
        alpha = p[idx] + 0j
        idx += 1
    else:
        u5, idx = flavon(p, idx, a5)
        u1, idx = flavon(p, idx, a1)
        ce, idx = coupl(p, idx, variant, 0)
        cD, idx = coupl(p, idx, variant, 1)
        alpha = p[idx] + 1j * p[idx + 1]
        idx += 2
    Me = dirac(u5, u10, ce)
    MD = dirac(u5, u1, cD)
    MR = majorana(u1, alpha)
    out = np.full(7, np.nan)
    det = np.linalg.det(MR)
    if abs(det) < 1e-300:
        return out
    Mnu = -(MD @ np.linalg.inv(MR) @ MD.T)
    we, Ve = np.linalg.eigh(Me @ Me.conj().T)
    wn, Vn = np.linalg.eigh(Mnu @ Mnu.conj().T)
    me = np.sqrt(np.maximum(we, 0.0))
    out[0] = me[0] / me[1] if me[1] > 0 else np.nan
    out[1] = me[1] / me[2] if me[2] > 0 else np.nan
    dd = wn[1] - wn[0]
    out[2] = (wn[2] - wn[0]) / dd if dd > 0 else np.nan
    U = Ve.conj().T @ Vn
    s12, s13, s23, d = mix_obs(U)
    out[3] = s12; out[4] = s13; out[5] = s23; out[6] = d
    return out


@nb.njit(cache=True)
def quark_obs(p, a10, a5, variant):
    idx = 0
    u10, idx = flavon(p, idx, a10)
    u5, idx = flavon(p, idx, a5)
    if variant == 0:
        alu = 0.0 + 0j
        cd = np.zeros(5, dtype=np.complex128); cd[0] = 1.0
    else:
        alu = p[idx] + 1j * p[idx + 1]
        idx += 2
        cd, idx = coupl(p, idx, 1, 0)
    Mu = majorana(u10, alu)
    Md = dirac(u10, u5, cd)
    wu, Vu = np.linalg.eigh(Mu @ Mu.conj().T)
    wd, Vd = np.linalg.eigh(Md @ Md.conj().T)
    mu = np.sqrt(np.maximum(wu, 0.0))
    md = np.sqrt(np.maximum(wd, 0.0))
    out = np.full(8, np.nan)
    out[0] = mu[0] / mu[1] if mu[1] > 0 else np.nan
    out[1] = mu[1] / mu[2] if mu[2] > 0 else np.nan
    out[2] = md[0] / md[1] if md[1] > 0 else np.nan
    out[3] = md[1] / md[2] if md[2] > 0 else np.nan
    V = Vu.conj().T @ Vd
    a11 = abs(V[0, 0]); a12 = abs(V[0, 1]); a23 = abs(V[1, 2])
    n = math.sqrt(a11 * a11 + a12 * a12)
    if n > 1e-12:
        lam = a12 / n
        out[4] = lam
        out[5] = a23 / (lam * lam * n) if lam > 1e-12 else np.nan
        den = V[1, 0] * np.conj(V[1, 2])
        if abs(den) > 1e-300:
            z = -V[0, 0] * np.conj(V[0, 2]) / den
            out[6] = z.real
            out[7] = z.imag
    return out


@nb.njit(cache=True)
def lepton_pulls(o):
    r = np.empty(7)
    for k in range(7):
        x = o[k]
        if not np.isfinite(x) or x <= 0 and k < 3:
            r[k] = CAP
            continue
        if k < 2:
            r[k] = math.log(x / LEP_T[k]) / LEP_LO[k]
        elif k == 6:
            dlt = (x - LEP_T[6] + 180.0) % 360.0 - 180.0
            r[k] = dlt / (LEP_HI[6] if dlt > 0 else LEP_LO[6])
        else:
            dlt = x - LEP_T[k]
            r[k] = dlt / (LEP_HI[k] if dlt > 0 else LEP_LO[k])
        if r[k] > CAP:
            r[k] = CAP
        if r[k] < -CAP:
            r[k] = -CAP
    if not np.isfinite(o[6]):
        r[6] = 0.0 if (np.isfinite(o[4]) and o[4] < 1e-12) else CAP   # delta undefined when s13 = 0
    return r


@nb.njit(cache=True)
def quark_pulls(o):
    r = np.empty(8)
    for k in range(8):
        x = o[k]
        if not np.isfinite(x) or (k < 4 and x <= 0):
            r[k] = CAP
            continue
        if k < 4:
            r[k] = math.log(x / Q_T[k]) / Q_S[k]
        else:
            r[k] = (x - Q_T[k]) / Q_S[k]
        if r[k] > CAP:
            r[k] = CAP
        if r[k] < -CAP:
            r[k] = -CAP
    return r


def class_list():
    classes = []
    names = ["Z3", "P", "Z7", "G"]
    for var in ("min", "gen"):
        for a10, a5, a1 in itertools.product(names, repeat=3):
            classes.append({"sector": "lepton", "variant": var, "phi10": a10, "phi5": a5, "phi1": a1})
        for a10, a5 in itertools.product(names, repeat=2):
            classes.append({"sector": "quark", "variant": var, "phi10": a10, "phi5": a5})
    classes.append({"sector": "lepton", "variant": "LNR exact", "phi10": "G", "phi5": "(-1,1,1)", "phi1": "(1,1,1)"})
    return classes


def cname(c):
    if c["sector"] == "lepton":
        return f"lepton|{c['variant']}|phi10={c['phi10']}|phi5={c['phi5']}|phi1={c['phi1']}"
    return f"quark|{c['variant']}|phi10={c['phi10']}|phi5={c['phi5']}"


def npar(c):
    if c["sector"] == "lepton":
        if c["variant"] == "LNR exact":
            return 4 + 1
        n = sum(NPAR_ALIGN[CODES[c[k]]] for k in ("phi10", "phi5", "phi1"))
        n += (0 + 2) if c["variant"] == "min" else (8 + 8)
        return n + 2
    n = sum(NPAR_ALIGN[CODES[c[k]]] for k in ("phi10", "phi5"))
    return n + (0 if c["variant"] == "min" else 2 + 8)


def make_fun(c):
    if c["sector"] == "lepton":
        if c["variant"] == "LNR exact":
            return (lambda p: lepton_obs(p, 3, 0, 0, 0, True)), lepton_pulls, 7
        a10, a5, a1 = (CODES[c[k]] for k in ("phi10", "phi5", "phi1"))
        v = 0 if c["variant"] == "min" else 1
        return (lambda p: lepton_obs(p, a10, a5, a1, v, False)), lepton_pulls, 7
    a10, a5 = CODES[c["phi10"]], CODES[c["phi5"]]
    v = 0 if c["variant"] == "min" else 1
    return (lambda p: quark_obs(p, a10, a5, v)), quark_pulls, 8


def random_start(c, rng, n):
    """phases uniform, log-moduli of generic vevs uniform in (-8, 0), couplings normal."""
    p = rng.normal(size=n)
    # mark which entries are phases / log-moduli by rebuilding the layout
    lay = layout(c)
    for k, t in enumerate(lay):
        if t == "phase":
            p[k] = rng.uniform(0, 2 * np.pi)
        elif t == "logmod":
            p[k] = rng.uniform(-8, 0)
        elif t == "coup":
            p[k] = rng.normal() * rng.choice([0.03, 0.3, 1.0, 3.0])
    return p


def layout(c):
    lay = []
    def al(code):
        if code == 1:
            lay.extend(["phase", "phase"])
        elif code == 3:
            lay.extend(["logmod", "logmod", "phase", "phase"])
    if c["sector"] == "lepton":
        if c["variant"] == "LNR exact":
            al(3)
            lay.append("coup")
            return lay
        for k in ("phi10", "phi5", "phi1"):
            al(CODES[c[k]])
        lay.extend(["coup"] * (2 if c["variant"] == "min" else 16))
        lay.extend(["coup", "coup"])
        return lay
    for k in ("phi10", "phi5"):
        al(CODES[c[k]])
    if c["variant"] == "gen":
        lay.extend(["coup"] * 10)
    return lay


def jac_rank(obsf, p, nobs, h=1e-6):
    """rank of d(observable)/d(parameter) with observables normalized by their target scale."""
    base = obsf(p)
    if not np.all(np.isfinite(base[:nobs - (1 if nobs == 7 else 0)])):
        return None
    J = np.zeros((nobs, len(p)))
    scale = np.where(np.abs(base) > 1e-12, np.abs(base), 1.0)
    for k in range(len(p)):
        dp = np.zeros_like(p)
        dp[k] = h
        o1, o2 = obsf(p + dp), obsf(p - dp)
        d = (o1 - o2) / (2 * h)
        if nobs == 7:
            dd = ((o1[6] - o2[6] + 180) % 360 - 180) / (2 * h)
            d[6] = dd
        J[:, k] = d / scale
    J[~np.isfinite(J)] = 0
    if J.size == 0:
        return 0
    sv = np.linalg.svd(J, compute_uv=False)
    return int(np.sum(sv > 1e-7 * max(sv[0], 1e-300)))


def prescreen(c, obsf, nobs, rng, n=200):
    """Structural check from random points: massless states, degeneracies, singular M_R."""
    npr = npar(c)
    bad_mass = 0
    finite = 0
    for _ in range(n):
        p = random_start(c, rng, npr)
        o = obsf(p)
        ratios = o[:2] if c["sector"] == "lepton" else o[:4]
        if np.all(np.isfinite(ratios)):
            finite += 1
            if np.min(ratios) < 1e-9 or np.max(ratios) > 1 - 1e-9:
                bad_mass += 1
        else:
            bad_mass += 1
    if bad_mass == n:
        return "structural: a massless or exactly degenerate state (or singular M_R) at every sampled point"
    return None


def fit_class(c, log):
    rng = np.random.default_rng(zlib.crc32(cname(c).encode()))
    obsf, pullf, nobs = make_fun(c)
    n = npar(c)
    t0 = time.time()
    dead = prescreen(c, obsf, nobs, rng)
    if n == 0:
        p = np.zeros(0)
        r = pullf(obsf(p))
        return {"name": cname(c), **c, "n_par": 0, "n_eff": 0, "n_obs": nobs, "chi2": float(np.sum(r ** 2)),
                "structural": dead, "best_obs": obsf(p).tolist(), "pulls": r.tolist(), "params": [],
                "time_s": time.time() - t0}
    best = (np.inf, None)
    n_starts = 4 if dead else min(60, 16 + 2 * n)
    fun = lambda p: pullf(obsf(p))
    for s in range(n_starts):
        p0 = random_start(c, rng, n)
        try:
            res = least_squares(fun, p0, method="trf", max_nfev=200 * (n + 1), xtol=1e-12, ftol=1e-12, gtol=1e-12)
        except Exception as e:
            continue
        c2 = float(np.sum(res.fun ** 2))
        if c2 < best[0]:
            best = (c2, res.x.copy())
    if best[1] is None:
        return {"name": cname(c), **c, "n_par": n, "n_eff": None, "n_obs": nobs, "chi2": float("inf"),
                "structural": dead, "time_s": time.time() - t0}
    # polish
    res = least_squares(fun, best[1], method="trf", max_nfev=2000 * (n + 1), xtol=1e-15, ftol=1e-15, gtol=1e-15)
    if np.sum(res.fun ** 2) < best[0]:
        best = (float(np.sum(res.fun ** 2)), res.x.copy())
    pbest = best[1]
    ranks = [jac_rank(obsf, pbest, nobs)]
    for _ in range(3):
        rr = jac_rank(obsf, random_start(c, rng, n), nobs)
        ranks.append(rr)
    ranks = [x for x in ranks if x is not None]
    n_eff = max(ranks) if ranks else None
    o = obsf(pbest)
    r = pullf(o)
    return {"name": cname(c), **c, "n_par": n, "n_eff": n_eff, "n_obs": nobs, "chi2": best[0],
            "structural": dead, "best_obs": [float(x) for x in o], "pulls": [float(x) for x in r],
            "params": [float(x) for x in pbest], "n_starts": n_starts, "time_s": time.time() - t0}


def verdict(rec):
    if rec.get("structural"):
        return "excluded (structural)" if rec["chi2"] > 1 else "check"
    n_eff = rec["n_eff"] if rec["n_eff"] is not None else rec["n_par"]
    dof = rec["n_obs"] - n_eff
    rec["dof"] = dof
    if dof >= 1:
        p = float(chi2dist.sf(rec["chi2"], dof))
        rec["p_value"] = p
        return "SURVIVES" if p > 0.01 else "excluded"
    rec["p_value"] = None
    return "accommodates (no prediction)" if rec["chi2"] < 1 else "excluded"


def main():
    done = {}
    if os.path.exists(JSONL):
        with open(JSONL) as f:
            for line in f:
                rec = json.loads(line)
                done[rec["name"]] = rec
    classes = class_list()
    t0 = time.time()
    # warm up numba
    lepton_obs(np.zeros(30), 0, 0, 0, 1, False)
    quark_obs(np.zeros(30), 0, 0, 1)
    with open(LOG, "a") as log, open(JSONL, "a") as out:
        log.write(f"start {time.ctime()} : {len(classes)} classes, {len(done)} already done\n")
        log.flush()
        for k, c in enumerate(classes):
            nm = cname(c)
            if nm in done:
                continue
            rec = fit_class(c, log)
            rec["verdict"] = verdict(rec)
            out.write(json.dumps(rec) + "\n")
            out.flush()
            log.write(f"[{k + 1}/{len(classes)}] {nm}: n_par={rec['n_par']} n_eff={rec.get('n_eff')} "
                      f"chi2={rec['chi2']:.3g} -> {rec['verdict']} ({rec['time_s']:.1f}s, total {time.time() - t0:.0f}s)\n")
            log.flush()
        log.write(f"done {time.ctime()} total {time.time() - t0:.0f}s\n")


if __name__ == "__main__":
    main()
