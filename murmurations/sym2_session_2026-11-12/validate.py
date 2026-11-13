"""Validation checks (integrity, not decisive tests). Reads the path-E class-number table.
V3: dimension-zero weights k=4,6,8,10,14 give Tr T_{p^2}=0 (mod two 31-bit primes), all p.
V3b: Kronecker-Hurwitz (k=2): sum_{|t|<=2p} H(4p^2-t^2) = 2p^2+p, exact, all p.
V2: exact trace vs PARI mfheckemat for small k,p.  V4: k=12 vs tau(p)^2-p^11.
V1: Sec. 2.2 identity (narrow window): direct per-k trace sum vs Poisson closed form."""
import sys, glob, json
import numpy as np
from math import pi, sqrt
import cypari2
from sym2lib import bump, dim_S

pari = cypari2.Pari(); pari.allocatemem(3 * 10**8)

def load(prefix):
    tab = {}
    for f in sorted(glob.glob(prefix + "_w*.npz")):
        z = dict(np.load(f))
        for i, p in enumerate(z["ps"]):
            a, b = z["offs"][i], z["offs"][i + 1]
            tab[int(p)] = (int(z["tlos"][i]), z["vals"][a:b])
    return tab

tab = load("data/HE")
ps = sorted(tab)
out = {"n_primes": len(ps), "pmax": max(ps)}

# full symmetric arrays over t in [-2p, 2p]
def full_t(p):
    tlo, v = tab[p]; assert tlo == 0 and len(v) == 2 * p
    t = np.arange(0, 2 * p + 1, dtype=np.int64)
    H12 = np.concatenate([v, [-1]])            # t = 2p -> H(0) = -1/12
    return t, H12

# ---- V3b Kronecker-Hurwitz, exact
bad_kh = []
for p in ps:
    t, H12 = full_t(p)
    s = int(H12[0]) + 2 * int(H12[1:].sum())
    if s != 12 * (2 * p * p + p):
        bad_kh.append(p)
out["V3b_KH_fail"] = bad_kh

# ---- V3 dimension zero mod q
qs = [2147483629, 2147483587]
bad_dz = []
for p in ps:
    t, H12 = full_t(p)
    for q in qs:
        n = (p * p) % q
        tq = t % q
        Pm1 = np.zeros_like(tq); P = np.ones_like(tq)   # P_1=0, P_2=1
        Pk = {2: P.copy()}
        for k in range(2, 14):
            Pn = (tq * P - n * Pm1) % q
            Pm1, P = P, Pn
            Pk[k + 1] = P.copy()
        Hq = H12 % q
        for k in (4, 6, 8, 10, 14):
            # sum over t in [-2p,2p]: t=0 once, others twice (P_k even in t for even k)
            terms = (Pk[k] * Hq) % q
            s = (int(terms[0]) + 2 * int(terms[1:].sum() % q)) % q
            hyp = (2 + pow(p, k - 1, q)) % q
            if (s + 12 * hyp) % q != 0:
                bad_dz.append((p, k, q))
out["V3_dimzero_fail"] = bad_dz

# exact trace of T_{p^2} on S_k(1) (integer)
def exact_trace(p, k):
    t, H12 = full_t(p)
    n = p * p
    tot = 0
    for ti, h in zip(t.tolist(), H12.tolist()):
        if h == 0: continue
        a, b = 0, 1          # P_1, P_2
        for _ in range(2, k):
            a, b = b, ti * b - n * a
        tot += (1 if ti == 0 else 2) * b * h
    num = -tot - 12 * (2 + p ** (k - 1))
    assert num % 24 == 0
    return num // 24

# ---- V2 vs PARI mfheckemat
v2 = []
for k in (12, 16, 20, 24, 30, 36, 48):
    mf = pari(f"mfinit([1,{k}],1)")
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47):
        tr_pari = int(pari.trace(pari.mfheckemat(mf, p * p)))
        v2.append((k, p, tr_pari == exact_trace(p, k)))
out["V2_mf_fail"] = [(k, p) for k, p, ok in v2 if not ok]
out["V2_n"] = len(v2)

# ---- V4 tau
v4bad = []
for p in [q for q in ps if q <= 400]:
    tp = int(pari.ramanujantau(p))
    if exact_trace(p, 12) != tp * tp - p ** 11:
        v4bad.append(p)
out["V4_tau_fail"] = v4bad
out["V4_n"] = len([q for q in ps if q <= 400])

# ---- V1 Sec 2.2 identity (narrow window), K = 150 and 300
def Hhat(eta):
    v = np.linspace(-1, 1, 4001); f = bump(v); eta = np.atleast_1d(eta)
    out = np.empty(len(eta))
    for i in range(0, len(eta), 500):
        out[i:i+500] = np.trapezoid(f[None, :] * np.cos(np.outer(eta[i:i+500], v)), v, axis=1)
    return out

v1 = []
for K in (150, 300):
    sig = K ** 0.9
    ks = np.arange(4, 4 * K, 2); h = bump((ks - K) / sig); m = h > 0; ks, h = ks[m], h[m]
    X = ((K - 1) / (2 * pi)) ** 2; N = X / 4
    D = float(np.sum(h * dim_S(ks)))
    cand = [p for p in ps if p <= 5 * X]
    pick = [cand[int(i)] for i in np.linspace(len(cand) * 0.05, len(cand) - 1, 8)]
    for p in pick:
        t, H12 = full_t(p); t, H12 = t[:-1], H12[:-1].astype(float) / 12   # |t|<2p
        mult = np.where(t == 0, 1.0, 2.0)
        x = t / (2.0 * p)
        # direct: per-k trace via Chebyshev recurrence U_{k-2}(x), summed with weights
        U0, U1 = np.ones_like(x), 2 * x              # U_0, U_1
        Ud = {0: U0, 1: U1}
        for j in range(2, int(ks.max()) - 1):
            U0, U1 = U1, 2 * x * U1 - U0
            if j + 2 in set(ks.tolist()): Ud[j] = U1
        direct_ell = 0.0
        for kk, hk in zip(ks, h):
            direct_ell += hk * (-(1 / (2 * p)) * np.sum(mult * H12 * Ud[kk - 2]))
        # closed form (Sec 2.2)
        al = 2 * np.arcsin(np.sqrt((2 * p - t) / (4.0 * p)))
        sa = np.sqrt((2.0 * p - t) * (2.0 * p + t)) / (2.0 * p)
        L = pi * H12 / (2 * p * sa)
        closed_ell = -(sig / (2 * pi)) * np.sum(mult * L * np.sin((K - 1) * al) * Hhat(sig * al))
        H0 = Hhat(0.0)[0]
        hyp_direct = float(np.sum(h * (-0.5 - np.exp((1 - ks) * np.log(p)))))
        V_direct = sqrt(N) * (direct_ell + hyp_direct + float(np.sum(h * (ks - 1) / (12 * p)))) / D
        V_closed = (-(3 / (pi**2 * H0)) * ((K - 1) / (K - 7)) * np.sum(mult * L * np.sin((K - 1) * al) * Hhat(sig * al))
                    - 6 * sqrt(N) / (K - 7) + sqrt(N) * (K - 1) / ((K - 7) * p))
        v1.append(dict(K=K, p=p, x=p / X, ell_direct=direct_ell, ell_closed=float(closed_ell),
                       V_direct=V_direct, V_closed=float(V_closed),
                       hyp_direct=hyp_direct, hyp_closed=-sig * H0 / 4,
                       D=D, D_closed=sig * H0 * (K - 7) / 24))
out["V1"] = v1
json.dump(out, open("data/validation.json", "w"), indent=1, default=float)
print(json.dumps({k: v for k, v in out.items() if k != "V1"}, default=float))
for r in v1:
    print(f"K={r['K']} p={r['p']} x={r['x']:.2f} ell dir={r['ell_direct']:.6e} closed={r['ell_closed']:.6e} "
          f"| V dir={r['V_direct']:.6f} closed={r['V_closed']:.6f} | D {r['D']:.3f}/{r['D_closed']:.3f}")
