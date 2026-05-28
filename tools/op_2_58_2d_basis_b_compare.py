"""op_2_58_2d_basis_b_compare.py — Brief 10.6 Item 1 toy-scale ratification harness.

Reproduces the comparison numbers cited in
`op_2_58_2d_basis_b_ratification.md` §3. Runs basis (a) primal, basis (b)-I
F_L-restriction, and basis (b)-II F_L-augmentation at k=7, q=911, σ=2, β=30
across 3 seeds; reports per-seed and pooled pair-recovery rates against the
§3.3.1 N=2.0×min_norm cutoff with the 1/21 chance baseline.

Toy scale only. Re-uses the §2.58.B construction (Brief 10.5) for the planted
trapdoor and `FanoLineClassifier` (§3.3) for pair recovery.
"""

from __future__ import annotations

import os
import sys
import time

import numpy as np
from fpylll import BKZ, LLL, IntegerMatrix

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from op_2_58_2d_classifier import FanoLineClassifier  # noqa: E402
from op_2_58_2d_construction import TOY_P, gen_spec_instance  # noqa: E402
from op_2_58_2d_lattice_attack import (  # noqa: E402
    DIM,
    _build_fano_augmentation_lattice,
    build_fano_projected_lattice,
    build_primal_lattice,
    build_scalar_lwe,
    l2_norm,
)

TOY_Q = TOY_P  # 911
K = 7
SIGMA = 2
BETA = 30
SEEDS = (20260601, 20260602, 20260603)
CUTOFF_FACTOR = 2.0  # §3.3.1
BASELINE = 1.0 / 21.0


def _run_bkz(B, beta, max_loops=8):
    A = IntegerMatrix.from_matrix([[int(x) for x in row] for row in B])
    LLL.reduction(A)
    par = BKZ.Param(block_size=beta, max_loops=max_loops,
                    flags=BKZ.AUTO_ABORT | BKZ.MAX_LOOPS)
    BKZ.reduction(A, par, float_type="ld")
    return [[A[i, j] for j in range(A.ncols)] for i in range(A.nrows)]


def _score(rows, true_pair, clf, cutoff_factor=CUTOFF_FACTOR):
    norms = [l2_norm(r) for r in rows]
    nz = [n for n in norms if n > 0]
    if not nz:
        return {"n_short": 0, "hits": 0, "rate": 0.0, "min_norm": 0.0}
    mn = min(nz)
    thr = cutoff_factor * mn + 1e-9
    short = [r for r, n in zip(rows, norms) if 0 < n <= thr]
    hits = sum(1 for r in short if clf.classify(r[:DIM])["pair"] == true_pair)
    return {"n_short": len(short), "hits": hits,
            "rate": hits / len(short) if short else 0.0, "min_norm": mn}


def compare(seeds=SEEDS, k=K, q=TOY_Q, sigma=SIGMA, beta=BETA) -> dict:
    clf = FanoLineClassifier(q)
    bases = [
        ("(a) primal",
         lambda lwe: build_primal_lattice(lwe["A_scalar"], lwe["b_scalar"], q)),
        ("(b)-I restriction",
         lambda lwe: build_fano_projected_lattice(lwe["A_scalar"], lwe["b_scalar"], q, k=k)),
        ("(b)-II augmentation",
         lambda lwe: _build_fano_augmentation_lattice(lwe["A_scalar"], lwe["b_scalar"], q, k)),
    ]
    rows_out: list[dict] = []
    for seed in seeds:
        rng = np.random.default_rng(seed)
        inst = gen_spec_instance(q, k=k, sigma=sigma, rng=rng)
        lwe = build_scalar_lwe(inst["A"], inst["s"], inst["e"], q)
        true_pair = tuple(inst["pair"][0])
        for name, builder in bases:
            t0 = time.time()
            B = builder(lwe)
            reduced = _run_bkz(B, beta)
            dt = time.time() - t0
            s = _score(reduced, true_pair, clf)
            rows_out.append({"seed": seed, "basis": name,
                             "nrows": len(B), "ncols": len(B[0]),
                             "true_pair": true_pair, "t_total": dt, **s})
    return {"k": k, "q": q, "sigma": sigma, "beta": beta,
            "cutoff_factor": CUTOFF_FACTOR, "baseline": BASELINE,
            "rows": rows_out}


def main() -> None:
    res = compare()
    print("=== basis-(b) ratification: (a) vs (I) restriction vs (II) augmentation ===")
    print(f"k={res['k']}, q={res['q']}, σ={res['sigma']}, β={res['beta']}, "
          f"cutoff N={res['cutoff_factor']}, baseline 1/21≈{res['baseline']:.4f}")
    print()
    hdr = (f"{'seed':>10} {'basis':>22} {'dim_r x dim_c':>15} "
           f"{'n_short':>8} {'hits':>5} {'rate':>7} {'min_norm':>9} {'t(s)':>7}")
    print(hdr)
    print("-" * len(hdr))
    for r in res["rows"]:
        print(f"{r['seed']:>10} {r['basis']:>22} {r['nrows']:>5}x{r['ncols']:<8} "
              f"{r['n_short']:>8} {r['hits']:>5} {r['rate']:>7.3f} "
              f"{r['min_norm']:>9.2f} {r['t_total']:>7.2f}")
    print()
    print("=== pooled per basis (across seeds) ===")
    print(f"{'basis':>22} {'tot_short':>10} {'tot_hits':>9} {'pool_rate':>10}")
    for name in ["(a) primal", "(b)-I restriction", "(b)-II augmentation"]:
        sel = [r for r in res["rows"] if r["basis"] == name]
        ts = sum(r["n_short"] for r in sel)
        th = sum(r["hits"] for r in sel)
        rate = th / ts if ts else 0.0
        print(f"{name:>22} {ts:>10} {th:>9} {rate:>10.4f}")


if __name__ == "__main__":
    main()
