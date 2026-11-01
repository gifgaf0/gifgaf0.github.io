"""Descriptive: linear threshold of the vacuum restricted to REAL perturbations of psi (the director/amplitude sector,
S = 0 to first order; A does not couple at second order). Same lattice functional as chiral1d.py; Fourier blocks
q = 2 pi m / P over the P grid, q <= 6."""
import numpy as np, json, chiral1d as C
def mineig(n, eta, g, P, m):
    ch = C.Chain(n, eta, g, P, Afree=False); xv = ch.vacuum(); M = ch.M; s = np.arange(M)*ch.h; q = 2*np.pi*m/P
    B = []
    for f in range(3):
        for fn in ((np.cos, np.sin) if m > 0 else (np.cos,)):
            v = np.zeros(xv.size); v[f*M:(f+1)*M] = fn(q*s) if m > 0 else 1.0; B.append(v/np.linalg.norm(v))
    B = np.array(B).T; t = 1e-6
    HB = np.array([(ch.energy_grad(xv+t*B[:, i])[1]-ch.energy_grad(xv-t*B[:, i])[1])/(2*t) for i in range(B.shape[1])]).T
    Hs = B.T@HB; return np.linalg.eigvalsh(0.5*(Hs+Hs.T))[0]
out = {}
for nk in ('z', 'diag', 'perp'):
    for eta in (0.1, 0.0):
        def unst(g):
            for P in C.P_GRID:
                for m in range(0, int(6*P/(2*np.pi))+1):
                    if mineig(C.NHAT[nk], eta, g, P, m) < -1e-9: return (P, m)
            return None
        lo, hi = 0.0, 8.0
        while hi-lo > 1e-3:
            mid = 0.5*(lo+hi)
            if unst(mid): hi = mid
            else: lo = mid
        P, m = unst(hi); out[f'{nk}_eta{eta}'] = dict(gamma_lin_director=hi, P=float(P), m=m, q=2*np.pi*m/P)
        print(nk, eta, out[f'{nk}_eta{eta}'], flush=True)
json.dump(out, open('director_lin_chiral1d.json', 'w'), indent=1)
