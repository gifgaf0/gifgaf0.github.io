"""EXPLORATORY tail-bound helpers on top of followup_AB/gengine.py (unchanged).
One G_k matrix serves every character mod Q0; contraction per character."""
import sys, math, numpy as np
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from gengine import Model, CHI, lichtblau, gl_nodes, delta_all, primes_upto

def chi_vec(m, name):
    return np.array([CHI[name](u) for u in m.units], float)

def contract(m, Gm, k, name):
    x = chi_vec(m, name); lam = m.lam
    return float(x @ (lam * (-lam) ** (k - 2) * m.P @ Gm @ m.P) @ x) / m.phi

def c0(m, name):
    x = chi_vec(m, name)
    return float(x @ (m.lam * m.M0) @ x) / m.phi

def terms(Q0, names, y, k, N, prime_set=None):
    m = Model(Q0, CHI[names[0]], y)
    if k == 0: return {n: c0(m, n) for n in names}
    Gm = m.G(k, N, prime_set)
    return {n: contract(m, Gm, k, n) for n in names}

# ---------- Monte Carlo (geometric importance sampling) ----------
def mc_tail(Q0, names, y, k, nsamp, prime_set, batch=200_000, seed=1, antithetic=True):
    """Estimate c_k(all) - c_k(prime_set) via
       c_k = ((-1)^{k-2}/phi) sum_{A0} E[(P^T chi)_{A0} (P chi)_{A_{k-1}} Delta_k],
       s_i ~ iid Geometric(lam) on {1,2,...}. Every start residue A0 is used for each gap draw
       (exact stratification over A0).  Antithetic: U -> 1-U in the inverse-CDF draw."""
    m = Model(Q0, CHI[names[0]], y); ph = m.phi; lam = m.lam; a = m.a
    xs = {n: chi_vec(m, n) for n in names}
    L = {n: m.P.T @ xs[n] for n in names}; Rv = {n: m.P @ xs[n] for n in names}
    steps = np.array(m.steps) // 2                       # half-units per step from each residue
    cyc = np.concatenate([[0], np.cumsum(np.tile(steps, 2))])  # cumulative offsets over two periods
    per = int(steps.sum())                                 # half-units per full cycle of phi steps
    rng = np.random.default_rng(seed)
    acc = {n: [] for n in names}
    done = 0
    while done < nsamp:
        nb = min(batch, nsamp - done)
        U = rng.random((k - 1, nb))
        Us = [U, 1 - U] if antithetic else [U]
        vals = {n: 0.0 for n in names}
        for UU in Us:
            s = 1 + np.floor(np.log(UU) / math.log(a)).astype(np.int64)   # Geometric(lam), P(s=m)=lam a^{m-1}
            S = np.vstack([np.zeros(nb, np.int64), np.cumsum(s, axis=0)])  # cumulative steps
            for R in range(ph):
                # half-unit offset after t steps from residue R
                def off(t):
                    q, r = np.divmod(t, ph)
                    return q * per + (cyc[R + r] - cyc[R])
                pts = [off(S[i]) for i in range(k)]
                Nhalf = int(pts[-1].max())
                D = delta_all(pts, Nhalf, m.excl, None) - delta_all(pts, Nhalf, m.excl, set(prime_set))
                end = (R + S[-1]) % ph
                for n in names:
                    vals[n] = vals[n] + L[n][R] * Rv[n][end] * D
        for n in names:
            acc[n].append(((-1) ** (k - 2) / ph) * vals[n] / len(Us))
        done += nb
    out = {}
    for n in names:
        v = np.concatenate(acc[n]); out[n] = (float(v.mean()), float(v.std(ddof=1) / math.sqrt(len(v))), len(v))
    return out

def mc_tail_multi(Q0, names, y, k, nsamp, cut_sets, batch=100_000, seed=1):
    """Same estimator, common random numbers: returns per cutoff label the tail c_k(all)-c_k(P)
    and per-sample arrays (for SEs of differences between cutoffs)."""
    m = Model(Q0, CHI[names[0]], y); ph = m.phi; a = m.a
    xs = {n: chi_vec(m, n) for n in names}
    Lv = {n: m.P.T @ xs[n] for n in names}; Rv = {n: m.P @ xs[n] for n in names}
    steps = np.array(m.steps) // 2
    cyc = np.concatenate([[0], np.cumsum(np.tile(steps, 2))]); per = int(steps.sum())
    rng = np.random.default_rng(seed)
    acc = {(lab, n): [] for lab in cut_sets for n in names}
    done = 0
    while done < nsamp:
        nb = min(batch, nsamp - done)
        U = rng.random((k - 1, nb))
        vals = {(lab, n): np.zeros(nb) for lab in cut_sets for n in names}
        for UU in (U, 1 - U):
            s = 1 + np.floor(np.log(UU) / math.log(a)).astype(np.int64)
            S = np.vstack([np.zeros(nb, np.int64), np.cumsum(s, axis=0)])
            for R in range(ph):
                def off(t):
                    q, r = np.divmod(t, ph); return q * per + (cyc[R + r] - cyc[R])
                pts = [off(S[i]) for i in range(k)]
                Nhalf = int(pts[-1].max())
                Dall = delta_all(pts, Nhalf, m.excl, None)
                end = (R + S[-1]) % ph
                for lab, P in cut_sets.items():
                    D = Dall - delta_all(pts, Nhalf, m.excl, set(P))
                    for n in names:
                        vals[(lab, n)] += Lv[n][R] * Rv[n][end] * D
        for key in vals:
            acc[key].append(((-1) ** (k - 2) / ph) * vals[key] / 2)
        done += nb
    return {key: np.concatenate(v) for key, v in acc.items()}
