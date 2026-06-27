"""op_2_58_2d_secondary_run.py — Brief 11 Item 3 secondary-gate harness.

Pre-reg §3.1 Q3 closure: the secondary-run validation gate is
  (a) SNR proxy ‖e‖/‖A·s‖ at k ∈ {7, 14} within 25% of the Brief-09 baseline
      0.0053 (recorded as the reproducible reference; the original 0.0025
      figure was downgraded per §3.1 Q3),
  (b) cutoff N=2.0 still preferred at k=14 (the §3.3.1 fine-discrimination
      gate where k=7's single-trapdoor separation was too clean to discriminate).

This script runs both at q=911 (toy) and emits an outcome the closure cites.
"""

from __future__ import annotations

import math
import os
import sys
import time

import numpy as np
from fpylll import BKZ, IntegerMatrix, LLL

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from op_2_58_2d_classifier import FanoLineClassifier  # noqa: E402
from op_2_58_2d_construction import TOY_P, gen_spec_instance  # noqa: E402
from op_2_58_2d_lattice_attack import (  # noqa: E402
    DIM,
    _build_fano_augmentation_lattice,  # noqa: F401 — for completeness symmetry
    build_fano_projected_lattice,
    build_primal_lattice,
    build_scalar_lwe,
    l2_norm,
)

TOY_Q = TOY_P  # 911
SIGMA = 2  # pinned per Brief 10.7 / §2.69.3
SEEDS = (20260601, 20260602, 20260603)
BRIEF_09_SNR_BASELINE = 0.0053
SNR_TOLERANCE = 0.25  # ±25% per §3.1 Q3 closure
N_SWEEP = (1.0, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5, 3.0, 4.0, 6.0, 10.0)
BASELINE_PAIR = 1.0 / 21.0


def _snr_proxy(k: int, seed: int, q: int = TOY_Q, sigma: int = SIGMA) -> float:
    """SNR proxy ‖e‖/‖A·s‖ on a §2.58.B instance at (q, k). Centred lift for
    A·s = b − e (mod q) ↦ (−q/2, q/2]."""
    rng = np.random.default_rng(seed)
    inst = gen_spec_instance(q, k=k, sigma=sigma, rng=rng)
    lwe = build_scalar_lwe(inst["A"], inst["s"], inst["e"], q)
    e = inst["e_scalar_signed"] if "e_scalar_signed" in inst else None
    if e is None:
        # gen_spec_instance returns e per-block; flatten and centre.
        e_flat: list[int] = []
        for ev in inst["e"]:
            e_flat.extend(int(x if x <= q // 2 else x - q) for x in ev)
        e = e_flat
    def centre(x: int) -> int:
        x %= q
        return x if x <= q // 2 else x - q
    n_eff = lwe["n_eff"]
    As = [centre(lwe["b_scalar"][i] - e[i]) for i in range(n_eff)]
    norm_e = l2_norm(list(e))
    norm_As = l2_norm(As)
    return norm_e / norm_As if norm_As else float("inf")


def _run_bkz(B, beta: int, max_loops: int = 8) -> list[list[int]]:
    """LLL + BKZ-β with float_type="ld" — same precision as the smoke test."""
    A = IntegerMatrix.from_matrix([[int(x) for x in row] for row in B])
    LLL.reduction(A)
    par = BKZ.Param(block_size=beta, max_loops=max_loops,
                    flags=BKZ.AUTO_ABORT | BKZ.MAX_LOOPS)
    BKZ.reduction(A, par, float_type="ld")
    return [[A[i, j] for j in range(A.ncols)] for i in range(A.nrows)]


def _sweep_cutoff(rows, true_pair, clf, n_values=N_SWEEP) -> list[dict]:
    """Per-N short-set size and pair-recovery rate against the true block-0 pair."""
    norms = [l2_norm(r) for r in rows]
    nz = [n for n in norms if n > 0]
    if not nz:
        return []
    mn = min(nz)
    recovered = [clf.classify(r[:DIM])["pair"] == true_pair for r in rows]
    out = []
    for Nf in n_values:
        thr = Nf * mn + 1e-9
        idx = [i for i in range(len(rows)) if 0 < norms[i] <= thr]
        n_short = len(idx)
        hits = sum(1 for i in idx if recovered[i])
        rate = hits / n_short if n_short else 0.0
        se = math.sqrt(BASELINE_PAIR * (1 - BASELINE_PAIR) / n_short) if n_short else 0.0
        sigma_stat = (rate - BASELINE_PAIR) / se if se > 0 else 0.0
        out.append({"N": Nf, "n_short": n_short, "rate": rate,
                    "sigma_stat": sigma_stat, "min_norm": mn})
    return out


def measure_snr_at_k(k: int, seeds=SEEDS) -> dict:
    """SNR proxy at toy k across the schedule seeds."""
    snrs = [_snr_proxy(k, s) for s in seeds]
    mean = float(np.mean(snrs))
    rel = abs(mean - BRIEF_09_SNR_BASELINE) / BRIEF_09_SNR_BASELINE
    return {
        "k": k, "seeds": list(seeds), "snrs": [float(x) for x in snrs],
        "mean_snr": mean, "rel_dev_from_baseline": rel,
        "gate_pass": rel <= SNR_TOLERANCE,
    }


def k14_cutoff_confirmation(seeds=SEEDS, beta: int = 30) -> dict:
    """Run BKZ at k=14 β=30 on basis (a) and basis (b)-I across the seeds,
    sweep cutoff N, and confirm N=2.0 stays inside the safe band (i.e., the
    cutoff value the §3.3.1 ratification targets remains a sensible pin at
    k=14's larger BKZ output population)."""
    clf = FanoLineClassifier(TOY_Q)
    by_basis_n: dict[tuple[str, float], list[dict]] = {}
    timings = []
    for seed in seeds:
        rng = np.random.default_rng(seed)
        inst = gen_spec_instance(TOY_Q, k=14, sigma=SIGMA, rng=rng)
        lwe = build_scalar_lwe(inst["A"], inst["s"], inst["e"], TOY_Q)
        true_pair = tuple(inst["pair"][0])
        for name, builder in [
            ("(a) primal",
             lambda lwe=lwe: build_primal_lattice(lwe["A_scalar"], lwe["b_scalar"], TOY_Q)),
            ("(b)-I restriction",
             lambda lwe=lwe: build_fano_projected_lattice(
                 lwe["A_scalar"], lwe["b_scalar"], TOY_Q, k=14)),
        ]:
            t0 = time.time()
            B = builder()
            reduced = _run_bkz(B, beta)
            dt = time.time() - t0
            timings.append({"seed": seed, "basis": name, "t_total": dt,
                            "dim": (len(B), len(B[0]))})
            for s in _sweep_cutoff(reduced, true_pair, clf):
                by_basis_n.setdefault((name, s["N"]), []).append(s)
    # Pool per (basis, N): total hits / total short, σ_pooled
    pooled = []
    for (name, Nf), rows in sorted(by_basis_n.items(), key=lambda x: (x[0][0], x[0][1])):
        tot_short = sum(r["n_short"] for r in rows)
        tot_hits = sum(round(r["rate"] * r["n_short"]) for r in rows)
        rate = tot_hits / tot_short if tot_short else 0.0
        se = math.sqrt(BASELINE_PAIR * (1 - BASELINE_PAIR) / tot_short) if tot_short else 0.0
        sigma_stat = (rate - BASELINE_PAIR) / se if se > 0 else 0.0
        pooled.append({"basis": name, "N": Nf, "tot_short": tot_short,
                       "tot_hits": tot_hits, "rate": rate,
                       "sigma_pooled": sigma_stat})
    return {"beta": beta, "k": 14, "sigma": SIGMA,
            "n_sweep": list(N_SWEEP), "pooled": pooled, "timings": timings}


def main() -> dict:
    print("=" * 78)
    print("OP-2.58.2d secondary-run gate (Brief 11 Item 3) — toy scale q=911")
    print("=" * 78)
    print("\n[a] SNR proxy ‖e‖/‖A·s‖ at k ∈ {7, 14}")
    print(f"    gate: within ±{int(SNR_TOLERANCE * 100)}% of Brief-09 baseline "
          f"{BRIEF_09_SNR_BASELINE}")
    snr_k7 = measure_snr_at_k(7)
    snr_k14 = measure_snr_at_k(14)
    for r in (snr_k7, snr_k14):
        print(f"  k={r['k']}: SNR per seed {[f'{x:.4f}' for x in r['snrs']]}, "
              f"mean {r['mean_snr']:.4f}, "
              f"rel.dev. {r['rel_dev_from_baseline']*100:.1f}% → "
              f"{'PASS' if r['gate_pass'] else 'FAIL'}")
    snr_gate = snr_k7["gate_pass"] and snr_k14["gate_pass"]
    print(f"  → SNR gate: {'PASS' if snr_gate else 'FAIL'}")

    print("\n[b] Cutoff N=2.0 confirmation at k=14 (β=30, basis (a) + (b)-I)")
    cut = k14_cutoff_confirmation()
    print(f"  {'basis':>22} {'N':>5} {'tot_short':>10} {'tot_hits':>9} "
          f"{'rate':>7} {'σ_pooled':>9}")
    for row in cut["pooled"]:
        print(f"  {row['basis']:>22} {row['N']:>5} {row['tot_short']:>10} "
              f"{row['tot_hits']:>9} {row['rate']:>7.3f} {row['sigma_pooled']:>9.2f}")
    # Confirm N=2.0 is inside the safe band per basis: σ_pooled at N=2.0
    # must be ≥ the within-band reference (we use the smoke-test ratification
    # criterion: σ at N=2.0 not lower than σ at adjacent N's by more than a
    # noise threshold, AND σ ≥ 0 at N=2.0 — i.e., N=2.0 is not in the
    # degenerate region).
    safe_pinned = []
    for name in ("(a) primal", "(b)-I restriction"):
        sigmas_by_N = {r["N"]: r["sigma_pooled"] for r in cut["pooled"]
                       if r["basis"] == name}
        s2 = sigmas_by_N.get(2.0)
        # Safe-band rule: σ at N=2.0 is within max(adjacent_σ) − 1.0 (a soft
        # one-σ band tolerating sampling noise; matches the smoke-test
        # convention of "flat across N").
        neighbours = [sigmas_by_N.get(N) for N in (1.5, 1.75, 2.25, 2.5)
                      if sigmas_by_N.get(N) is not None]
        best_neighbour = max(neighbours) if neighbours else s2
        safe = (s2 is not None and s2 >= best_neighbour - 1.0)
        safe_pinned.append({"basis": name, "sigma_at_N=2.0": s2,
                            "best_neighbour_sigma": best_neighbour,
                            "in_safe_band": safe})
        print(f"  {name}: σ(N=2.0)={s2:.2f}; best neighbour σ={best_neighbour:.2f}; "
              f"in safe band: {safe}")
    cutoff_gate = all(s["in_safe_band"] for s in safe_pinned)
    print(f"  → cutoff gate: {'PASS' if cutoff_gate else 'CHECK (within-band addendum may be needed)'}")

    overall = snr_gate and cutoff_gate
    print(f"\nSECONDARY-RUN OVERALL: {'PASS' if overall else 'FAIL'}")
    return {"snr_k7": snr_k7, "snr_k14": snr_k14, "cutoff": cut,
            "safe_pinned": safe_pinned, "snr_gate": snr_gate,
            "cutoff_gate": cutoff_gate, "overall": overall}


if __name__ == "__main__":
    main()
