#!/usr/bin/env python3
"""C1 DR-C1-2: the lattice estimator (malb/lattice-estimator @ 53da5982597709ba0fdf94ea37a84d822310fd84) on the SLWE spec
parameters with a uniform public matrix, and (descriptive) on the instance left after the rank collapse.
Run under Sage (passagemath 10.8.12) with the estimator checkout on PYTHONPATH."""
import json, sys, time
from sage.all import log, RR
from estimator import LWE, ND

Q = 4294977961
CASES = [
    ("spec_uniform_m512", LWE.Parameters(n=512, q=Q, Xs=ND.SparseTernary(32, 32, 512), Xe=ND.CenteredBinomial(2),
                                         m=512, tag="SLWE spec, uniform A, one public key")),
    ("spec_uniform_m1024", LWE.Parameters(n=512, q=Q, Xs=ND.SparseTernary(32, 32, 512), Xe=ND.CenteredBinomial(2),
                                          m=1024, tag="SLWE spec, uniform A, public key + one ciphertext")),
    ("rank_collapse_n76", LWE.Parameters(n=76, q=Q, Xs=ND.CenteredBinomial(2), Xe=ND.CenteredBinomial(2),
                                         m=436, tag="after the rank collapse: secret = noise on 76 coordinates")),
    # descriptive (added after the pre-registered runs): the two smallest primes = 1 (mod 455), same n, secret and noise
    ("uniform_q911", LWE.Parameters(n=512, q=911, Xs=ND.SparseTernary(32, 32, 512), Xe=ND.CenteredBinomial(2),
                                    m=512, tag="descriptive: q = 911, uniform A")),
    ("uniform_q2731", LWE.Parameters(n=512, q=2731, Xs=ND.SparseTernary(32, 32, 512), Xe=ND.CenteredBinomial(2),
                                     m=512, tag="descriptive: q = 2731, uniform A")),
]
which = sys.argv[1:] or [c[0] for c in CASES]
out = {}
for name, params in CASES:
    if name not in which:
        continue
    rec = {"params": str(params)}
    t0 = time.time()
    rough = LWE.estimate.rough(params)
    rec["rough"] = {k: {kk: str(vv) for kk, vv in v.items()} for k, v in rough.items()}
    rec["rough_seconds"] = round(time.time() - t0, 1)
    t0 = time.time()
    full = LWE.estimate(params)
    rec["full"] = {k: {kk: str(vv) for kk, vv in v.items()} for k, v in full.items()}
    rec["full_log2_rop"] = {k: float(RR(log(v["rop"], 2))) for k, v in full.items()}
    rec["full_seconds"] = round(time.time() - t0, 1)
    rec["min_log2_rop"] = min(rec["full_log2_rop"].values())
    out[name] = rec
    print(name, "min log2 rop =", round(rec["min_log2_rop"], 1), flush=True)
    json.dump(out, open(f"c1_estimator_{'_'.join(which)}.json", "w"), indent=1)
