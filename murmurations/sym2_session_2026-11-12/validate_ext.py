"""Integrity checks (not tests) on the K=200 extension table data/HEx_w*.npz:
Kronecker-Hurwitz exact, and dimension-zero k=4,6,8,10,14 mod two 31-bit primes (same as validate.py V3b/V3)."""
import glob, json, numpy as np
tab = {}
for f in sorted(glob.glob("data/HEx_w*.npz")):
    z = dict(np.load(f))
    for i, p in enumerate(z["ps"]):
        a, b = z["offs"][i], z["offs"][i+1]; assert z["tlos"][i] == 0; tab[int(p)] = z["vals"][a:b]
kh, dz = [], []
for p, v in tab.items():
    assert len(v) == 2*p
    H12 = np.concatenate([v, [-1]]); t = np.arange(0, 2*p+1, dtype=np.int64)
    if int(H12[0]) + 2*int(H12[1:].sum()) != 12*(2*p*p+p): kh.append(p)
    for q in (2147483629, 2147483587):
        n = (p*p) % q; tq = t % q; Pm1 = np.zeros_like(tq); P = np.ones_like(tq); Pk = {}
        for k in range(2, 14):
            Pm1, P = P, (tq*P - n*Pm1) % q; Pk[k+1] = P.copy()
        Hq = H12 % q
        for k in (4, 6, 8, 10, 14):
            terms = (Pk[k]*Hq) % q; s = (int(terms[0]) + 2*int(terms[1:].sum() % q)) % q
            if (s + 12*((2 + pow(p, k-1, q)) % q)) % q: dz.append((p, k, q))
out = dict(n_primes=len(tab), pmin=min(tab), pmax=max(tab), KH_fail=kh, dimzero_fail=dz)
json.dump(out, open("validation_ext.json", "w"), indent=1); print(out)
