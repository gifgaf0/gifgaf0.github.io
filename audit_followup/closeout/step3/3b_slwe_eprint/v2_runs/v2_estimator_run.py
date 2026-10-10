#!/usr/bin/env python3
"""SLWE note, version 2 (October 10, 2026): lattice-estimator runs added for version 2 of the note.

Same tool, commit and cost model as audit_followup/phase_c/C1/estimator/c1_estimator_run.py (malb/lattice-estimator
@ 53da5982597709ba0fdf94ea37a84d822310fd84, passagemath 10.8.12, default attack set and cost model). The cases:

  v2_collapsed_n76     version 2 after the rank collapse: the noise is the secret of a 76-dimensional instance with
                       1024 - 76 = 948 samples (Section 3 of the note; the analogue of C1's rank_collapse_n76).
  v2_uniform_n1024     version 2's parameters with a uniform matrix: n = 1024, q = 911, weight-64 ternary secret,
                       CBD(2) noise, m = 1024 (one public key).
  q3329_uniform_n512   the q = 3329 row of the working specification's security table (k = 32, n = 512), uniform matrix.
  q911_dense_n512      the q = 911 row (k = 32, n = 512) with a dense ternary secret instead of weight 64.
  v1_dense_n512        version 1's setting (n = 512, q = 4 294 977 961) with a dense ternary secret instead of weight 64.

The weight-64 cases at n = 512 and q in {4 294 977 961, 2731, 911} are C1's and are not rerun here.
Run under Sage (passagemath) with the estimator checkout on PYTHONPATH:
    python3 v2_estimator_run.py [case ...]     (all cases by default; results merged into v2_estimator_results.json)
"""
import json, os, sys, time
from sage.all import log, RR
from sage.version import version as SAGE_VERSION
from estimator import LWE, ND

HERE = os.path.dirname(os.path.abspath(__file__))
Q1 = 4294977961
CASES = [
    ("v2_collapsed_n76", LWE.Parameters(n=76, q=911, Xs=ND.CenteredBinomial(2), Xe=ND.CenteredBinomial(2), m=948,
                                        tag="version 2 after the rank collapse: secret = noise on 76 coordinates")),
    ("v2_uniform_n1024", LWE.Parameters(n=1024, q=911, Xs=ND.SparseTernary(32, 32, 1024), Xe=ND.CenteredBinomial(2),
                                        m=1024, tag="version 2's parameters, uniform A, one public key")),
    ("q3329_uniform_n512", LWE.Parameters(n=512, q=3329, Xs=ND.SparseTernary(32, 32, 512), Xe=ND.CenteredBinomial(2),
                                          m=512, tag="working specification's q = 3329 row, uniform A")),
    ("q911_dense_n512", LWE.Parameters(n=512, q=911, Xs=ND.Uniform(-1, 1), Xe=ND.CenteredBinomial(2), m=512,
                                       tag="q = 911, n = 512, dense ternary secret, uniform A")),
    ("v1_dense_n512", LWE.Parameters(n=512, q=Q1, Xs=ND.Uniform(-1, 1), Xe=ND.CenteredBinomial(2), m=512,
                                     tag="version 1's setting, dense ternary secret, uniform A")),
]
which = sys.argv[1:] or [c[0] for c in CASES]
path = os.path.join(HERE, "v2_estimator_results.json")
out = json.load(open(path)) if os.path.exists(path) else {}
out["_environment"] = {"sage": "passagemath " + SAGE_VERSION, "estimator_commit": "53da5982597709ba0fdf94ea37a84d822310fd84",
                       "python": sys.version.split()[0]}
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
    rec["min_attack"] = min(rec["full_log2_rop"], key=rec["full_log2_rop"].get)
    out[name] = rec
    print(name, "min log2 rop =", round(rec["min_log2_rop"], 1), "(" + rec["min_attack"] + ")",
          {k: round(x, 1) for k, x in rec["full_log2_rop"].items()}, flush=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1)
        fh.write("\n")
