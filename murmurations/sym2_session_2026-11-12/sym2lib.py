"""Core computations for the Sym^2-scale exploratory statistics (unfrozen, exploratory)."""
import numpy as np
from math import pi, log2

def dim_S(k):
    k = np.asarray(k)
    d = k // 12 - (k % 12 == 2)
    return np.where(k >= 4, d, 0).astype(float)

def bump(v):
    v = np.asarray(v, dtype=float)
    out = np.zeros_like(v)
    m = np.abs(v) < 1
    out[m] = np.exp(-1.0 / (1.0 - v[m] ** 2))
    return out

def Xof(K):
    return ((K - 1) / (2 * pi)) ** 2

def window(K, kind, theta=0.9):
    """Return (ks, w): even weights k>=4 with nonzero weight."""
    ks = np.arange(4, 4 * K + 8, 2)
    if kind == "C":   # conductor window Phi(X_k/X), v = log2(X_k/X)
        w = bump(np.log2(Xof(ks) / Xof(K)))
    elif kind == "N":  # narrow window H0((k-K)/K^theta)
        w = bump((ks - K) / K ** theta)
    else:
        raise ValueError(kind)
    m = w > 0
    return ks[m], w[m]

def W_of_alpha(alpha, ks, w, chunk=4000):
    """W(alpha) = sum_k w_k sin((k-1) alpha), vectorized over alpha."""
    alpha = np.asarray(alpha, dtype=float)
    out = np.empty_like(alpha)
    km1 = (ks - 1).astype(float)
    for i in range(0, len(alpha), chunk):
        out[i:i + chunk] = np.sin(np.outer(alpha[i:i + chunk], km1)) @ w
    return out

def class_masks(ks):
    return {"c0": (ks % 4 == 0), "c2": (ks % 4 == 2)}

def per_prime(p, t, H12, ks, w):
    """Per-class pieces for one prime p, given t (>=0, <2p) and 12*H(4p^2-t^2).
    Returns dict of numerators (elliptic, hyperbolic, identity) and denominators per class."""
    p = int(p)
    t = np.asarray(t, dtype=np.int64)
    H = np.asarray(H12, dtype=float) / 12.0
    mult = np.where(t == 0, 1.0, 2.0)
    alpha = 2.0 * np.arcsin(np.sqrt((2 * p - t) / (4.0 * p)))
    sin_a = np.sqrt((2.0 * p - t) * (2.0 * p + t)) / (2.0 * p)
    coef = -(1.0 / (2 * p)) * mult * H / sin_a          # multiplies W_c(alpha_t)
    res = {}
    for c, m in class_masks(ks).items():
        kc, wc = ks[m], w[m]
        Wc = W_of_alpha(alpha, kc, wc)
        res[f"ell_{c}"] = float(np.sum(coef * Wc))   # float64 sum; terms O(1) magnitude
        res[f"hyp_{c}"] = float(np.sum(wc * (-0.5 - np.exp((1 - kc) * np.log(p)))))
        res[f"id_{c}"] = float(np.sum(wc * (kc - 1) / (12.0 * p)))
        res[f"D_{c}"] = float(np.sum(wc * dim_S(kc)))
    return res

def alpha_cut(ks, w, tau=1e-4, ngrid=400001):
    """Largest alpha in (0, pi/2] with |W_c| >= tau*max|W_c| for either class c
    (S1-only truncation: uses W0+W2) -- returns cut for S1 combined weight."""
    al = np.linspace(0, pi / 2, ngrid)[1:]
    W = W_of_alpha(al, ks, w)
    Wm = np.abs(W).max()
    idx = np.where(np.abs(W) >= tau * Wm)[0].max()
    return al[min(idx + 1, len(al) - 1)]
