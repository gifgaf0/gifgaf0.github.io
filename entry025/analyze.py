"""Entry 025 analysis. usage: analyze.py DATADIR ARM [--dry]
Refuses to run unless every file in manifest.json matches its SHA-256 (skipped with --dry).
Per run, sufficient statistics over the 4 congruence classes c (G-bit x [p≡1 mod 3]) are formed;
all SEs come from a run-block bootstrap of those (B=2000, fixed seed).
Decisive (12 total, alpha' = 0.01/12, two-sided):
  RATE    hits/eligible vs predicted Zywina rate
  R3      rate(p≡1 mod 3)/rate(p≡2 mod 3) vs predicted
  LAG1|C  lag-1 correlation of hit indicators of adjacent eligible primes, in excess of the
          congruence bookkeeping  sum_pairs mu_c mu_c'  (mu_c = pooled class rates); predicted 0
Report-only: raw LAG1 and its bookkeeping value; waiting times.
"""
import sys, glob, json, hashlib, numpy as np
from scipy.stats import norm
ALPHA = 0.01/12; ZC = norm.ppf(1-ALPHA/2)
def check_manifest():
    m = json.load(open("manifest.json"))
    for f, h in m["files"].items():
        if hashlib.sha256(open(f,"rb").read()).hexdigest() != h: sys.exit(f"MANIFEST MISMATCH: {f}")
def run_stats(cls, elig, hit):
    e = elig.astype(bool); c = cls[e].astype(int); h = hit[e].astype(np.int64)
    n = np.bincount(c, minlength=4); H = np.bincount(c, weights=h, minlength=4)
    pr = np.flatnonzero(e[:-1] & e[1:])           # adjacent in the prime sequence, both eligible
    c1, c2 = cls[pr].astype(int), cls[pr+1].astype(int); h1, h2 = hit[pr], hit[pr+1]
    k = 4*c1 + c2
    P  = np.bincount(k, minlength=16).reshape(4,4)
    B  = np.bincount(k, weights=h1*h2, minlength=16).reshape(4,4)
    A1 = np.bincount(k, weights=h1, minlength=16).reshape(4,4)
    A2 = np.bincount(k, weights=h2, minlength=16).reshape(4,4)
    return np.concatenate([n, H, P.ravel(), B.ravel(), A1.ravel(), A2.ravel()])
def derive(S):
    n, H = S[:4], S[4:8]; P, B, A1, A2 = (S[8+16*i:24+16*i].reshape(4,4) for i in range(4))
    rate = H.sum()/n.sum()
    r3 = ((H[1]+H[3])/(n[1]+n[3])) / ((H[0]+H[2])/(n[0]+n[2]))
    mu = np.where(n > 0, H/np.maximum(n,1), 0)
    N = P.sum(); m1, m2 = A1.sum()/N, A2.sum()/N
    v = np.sqrt((m1-m1*m1)*(m2-m2*m2))
    raw = (B.sum()/N - m1*m2)/v
    book = ((P*np.outer(mu,mu)).sum()/N - m1*m2)/v       # congruence bookkeeping
    return np.array([rate, r3, raw-book, raw, book])
if __name__ == "__main__":
    d, arm = sys.argv[1], sys.argv[2]
    if "--dry" not in sys.argv: check_manifest()
    pred = json.load(open("predictions.json"))["arms"][arm]
    files = sorted(glob.glob(f"{d}/{arm}_run*.npz")); R = []; bad = 0; waits = []
    for f in files:
        z = np.load(f); R.append(run_stats(z["cls"], z["elig"], z["hit"])); bad += int(z["bad"])
        idx = np.flatnonzero(z["hit"][z["elig"].astype(bool)]); waits += list(np.diff(idx))
    R = np.array(R); obs = derive(R.sum(0))
    rng = np.random.default_rng(25025)
    boot = np.array([derive(R[rng.integers(0, len(R), len(R))].sum(0)) for _ in range(2000)])
    se = boot.std(0, ddof=1)
    res = {"arm":arm, "runs":len(R), "integrity_failures":bad, "eligible":int(R[:, :4].sum()),
           "hits":int(R[:, 4:8].sum()), "adjacent_pairs":int(R[:, 8:24].sum()), "alpha_prime":ALPHA, "z_crit":ZC}
    for k, (name, target) in enumerate([("RATE", pred["rate"]), ("R3", pred["R3"]), ("LAG1_beyond_congruence", 0.0)]):
        zz = (obs[k]-target)/se[k]
        res[name] = dict(observed=obs[k], predicted=target, se=se[k], z=zz, p=2*norm.sf(abs(zz)),
                         as_predicted=bool(abs(zz) < ZC), detectable_80=(ZC+norm.ppf(0.8))*se[k])
    res["report_LAG1_raw"] = dict(observed=obs[3], se=se[3], bookkeeping=obs[4], bookkeeping_se=se[4])
    res["report_waiting_mean_eligible"] = float(np.mean(waits)) if waits else None
    print(json.dumps(res, indent=1, default=float))
