"""Exploratory (post-data): untruncated-HL mod-4 same-residue deficit for consecutive PAIRS,
by absorbing small primes P into the modulus Q = 4*prod(P) in LO-S eq. (2.16) and marginalizing
to classes mod 4. With P = () this is (2.16) at q = 4 itself. Uses run020/predict/los216.py unchanged."""
import sys, math, json, time
import numpy as np
from scipy.signal import oaconvolve
sys.path.insert(0, sys.argv[1]); import los216

def arrays(Q, a, y):
    ph = los216.phi(Q); L = math.log(y)
    alpha = 1 - Q / (ph * L); kappa = Q / (ph * alpha * L)
    lw = math.log(alpha) * ph / Q
    H = int(math.ceil(39.0 / -lw)) + Q
    S = los216.S_table(Q, H); S0 = S - 1.0
    t = np.arange(H + 1)
    c = (np.gcd(t + a, Q) == 1).astype(float); c[0] = 0.0
    S0z = S0.copy(); S0z[0] = 0.0
    P1 = np.concatenate([[0.0], np.cumsum(c * S0z)[:-1]])
    conv = oaconvolve(c, S0z)[:H + 1]
    Qa = np.concatenate([[0.0], np.cumsum(c * conv)[:-1]])
    return ph, alpha, kappa, lw, H, S, P1, conv, Qa, c

def same_total(P, y):
    """(same-residue-mod-4 density, total pair density) at height y."""
    Q = 4 * math.prod(P)
    U = [a for a in range(1, Q) if math.gcd(a, Q) == 1]
    same = tot = 0.0
    for a in U:
        ph, alpha, kappa, lw, H, S, P1, conv, Qa, c = arrays(Q, a, y)
        h = np.arange(1, H + 1); keep = np.gcd(h + a, Q) == 1; h = h[keep]
        T = np.exp(lw * h) * (S[h] - kappa * (P1[h] + conv[h]) + kappa ** 2 * Qa[h])
        v = h % Q
        byv = np.bincount(v, weights=T, minlength=Q)
        cnt = np.concatenate([[0], np.cumsum(c[1:Q + 1])])       # cnt[k] = #adm t in [1,k]
        for vv in np.nonzero(byv)[0]:
            h0 = vv if vv else Q
            eps = cnt[h0 - 1] - ph * h0 / Q
            d = alpha ** eps * byv[vv]
            tot += d
            if vv % 4 == 0: same += d
    return same, tot

def deficit_local(P, y):
    s, t = same_total(P, y); return (0.5 - s / t) / 2

def deficit_range(P, x1, x2, nodes):
    u, wts = np.polynomial.legendre.leggauss(nodes)
    lo, hi = math.log(x1), math.log(x2)
    S = T = 0.0
    for uu, wt in zip((hi - lo) / 2 * u + (hi + lo) / 2, wts):
        y = math.exp(uu); s, t = same_total(P, y); S += wt * y * s; T += wt * y * t
    return (0.5 - S / T) / 2

if __name__ == "__main__":
    ladder = [(), (3,), (3, 5), (3, 5, 7), (3, 5, 7, 11)]
    heights = [("022", "range", 1e3, 1e8 - 2e5, 24), ("023-A", "range", 1e8, 1e9, 8),
               ("024-A", "range", 1e9, 2e9, 6), ("2^64", "local", 2 ** 63.5), ("2^128", "local", 2 ** 127.5)]
    out = {}
    for hgt in heights:
        name = hgt[0]; out[name] = {}
        for P in ladder:
            t0 = time.time()
            e = deficit_range(P, *hgt[2:]) if hgt[1] == "range" else deficit_local(P, hgt[2])
            out[name]["x".join(map(str, P)) or "none"] = e
            base = out[name]["none"]
            print(f"{name:6s} P={str(P):16s} eps={e:.6f}  ratio_to_216={e/base:.4f}  ({time.time()-t0:.0f}s)", flush=True)
        json.dump(out, open(sys.argv[2], "w"), indent=1)
