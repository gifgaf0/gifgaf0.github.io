"""op_2_58_2d_bkz_smoke.py — BKZ smoke test / §3.3.1 cutoff repin (Brief 09).

Toy-scale instrument validation for the §3.3.1 short-vector cutoff. It does NOT
pass or fail the pre-registration; it empirically characterises the
cutoff-vs-recovery behaviour so the provisional factor-of-2.0 can be ratified,
repinned, or flagged unstable.

Pipeline (per brief §2.1):
  1. Build the primal LWE lattice (the −A_scalarᵀ basis of §3.6) from a toy
     instance whose error e is a *planted* ZD-noise vector with a known
     generating pair (a, b) — the toy-scale stand-in for a §2.58.B trapdoor.
  2. Run BKZ at β ∈ {20, 30} on the basis (fpylll).
  3. For each BKZ output vector, classify the e-slice (first n_eff coords) with
     the §3.3 projection classifier; recovery = its argmax-pair == true (a, b).
  4. Sweep the cutoff N (short = norm ≤ N · shortest-norm) and report the
     recovery rate and short-set size at each N.
  5. Repeat across three seeds and pool.

DISCIPLINE (brief §4): toy scale only (q = 911, k ∈ {7, 14}). The spec gate of
op_2_58_2d_lattice_attack.gen_toy_instance is inherited and tested. This module
does NOT modify the classifier or the lattice-attack module — it consumes them.
"""

from __future__ import annotations

import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from op_2_58_2d_lattice_attack import (  # noqa: E402
    DIM,
    build_primal_lattice,
    build_scalar_lwe,
    gen_toy_instance,
    l2_norm,
    target_vector,
)
from op_2_58_2d_classifier import (  # noqa: E402
    TOY_P,
    FanoLineClassifier,
    _clean_kernel_vectors,
)

BASELINE = 1.0 / 21.0  # chance pair-recovery (21 unordered pairs)
N_VALUES = [1.0, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5, 3.0, 4.0, 6.0, 10.0]
SAMPLE_SEEDS = [20260601, 20260602, 20260603]
BETAS = [20, 30]


def _planted_zd_noise_e(pair: tuple[int, int], seed: int, k: int, q: int) -> list[int]:
    """Length-(k·16) error: a ZD-noise vector (random α∈{−1,0,+1} combination of
    the four K_{a,b} kernel basis vectors) placed in block 0, zeros elsewhere.

    This is a clean toy stand-in for a §2.58.B trapdoor: e lies in K_{a,b}, so
    the §3.3 classifier recovers (a, b) from it exactly (in-subspace ratio 1.0).
    """
    a, b = pair
    basis = _clean_kernel_vectors(a, b, q)
    rng = np.random.default_rng(seed)
    while True:
        alpha = rng.integers(-1, 2, size=4)
        if alpha.any():
            break
    z = sum(al * bv for al, bv in zip(alpha, basis))
    e_scalar = [0] * (k * DIM)
    for d in range(DIM):
        e_scalar[d] = int(z[d])
    return e_scalar


def build_leakage_instance(
    seed: int, k: int = 7, q: int = TOY_P, allow_spec_params: bool = False
) -> dict:
    """Toy LWE instance with a planted ZD-noise error. Inherits the spec gate
    of gen_toy_instance (raises SpecParamsRefused on spec-scale q/k)."""
    inst = gen_toy_instance(seed=seed, q=q, k=k, allow_spec_params=allow_spec_params)
    clf_pairs = list(FanoLineClassifier(q).pairs)
    true_pair = clf_pairs[np.random.default_rng(seed).integers(len(clf_pairs))]
    e_scalar = _planted_zd_noise_e(true_pair, seed, k, q)
    e_sed = [[e_scalar[i * DIM + d] % q for d in range(DIM)] for i in range(k)]
    lwe = build_scalar_lwe(inst["A"], inst["s"], e_sed, q)
    B = build_primal_lattice(lwe["A_scalar"], lwe["b_scalar"], q)
    v_target = target_vector(e_scalar, inst["s_scalar_signed"])
    return {
        "seed": seed, "k": k, "q": q,
        "true_pair": tuple(true_pair),
        "e_scalar": e_scalar,
        "s_scalar_signed": inst["s_scalar_signed"],
        "A_scalar": lwe["A_scalar"], "b_scalar": lwe["b_scalar"],
        "n_eff": lwe["n_eff"], "B": B,
        "v_target": v_target, "v_target_norm": l2_norm(v_target),
        "inst": inst,
    }


def run_bkz(B: list[list[int]], beta: int, max_loops: int = 8) -> list[list[int]]:
    """LLL then BKZ-β (fplll C++, long-double GSO, auto-abort); return rows.

    fpylll's row convention matches the module's z·B convention, so basis rows
    are lattice vectors directly. Long-double ("ld") precision is used because
    the default double GSO hits an "infinite loop in babai" on some of these
    q-ary bases; "ld" is robust and deterministic across the smoke-test seeds."""
    from fpylll import BKZ, LLL, IntegerMatrix

    N = len(B)
    A = IntegerMatrix.from_matrix([[int(x) for x in row] for row in B])
    LLL.reduction(A)
    par = BKZ.Param(block_size=beta, max_loops=max_loops,
                    flags=BKZ.AUTO_ABORT | BKZ.MAX_LOOPS)
    BKZ.reduction(A, par, float_type="ld")
    return [[A[i, j] for j in range(N)] for i in range(N)]


def sigma_vs_baseline(rate: float, n: int, baseline: float = BASELINE) -> float:
    """Z-score of an observed recovery rate against the Binomial(n, baseline)
    null. Returns 0.0 for an empty short-set."""
    if n == 0:
        return 0.0
    se = math.sqrt(baseline * (1.0 - baseline) / n)
    return (rate - baseline) / se if se > 0 else 0.0


def sweep_cutoff(rows, n_eff, true_pair, clf, n_values=N_VALUES) -> list[dict]:
    """For each cutoff N, the short-set size and pair-recovery rate."""
    norms = [l2_norm(r) for r in rows]
    min_norm = min(norms)
    # Per-vector recovery, computed once.
    recovered = [clf.classify(r[:n_eff])["pair"] == true_pair for r in rows]
    out = []
    for Nf in n_values:
        thr = Nf * min_norm
        idx = [i for i in range(len(rows)) if norms[i] <= thr + 1e-9]
        n_short = len(idx)
        hits = sum(1 for i in idx if recovered[i])
        rate = hits / n_short if n_short else 0.0
        out.append({
            "N": Nf, "n_short": n_short, "recovery": rate,
            "min_norm": min_norm, "threshold": thr,
            "sigma": sigma_vs_baseline(rate, n_short),
        })
    return out


def item2_sanity_check(clf: FanoLineClassifier, seed: int = SAMPLE_SEEDS[0], k: int = 7) -> dict:
    """§3.2: the planted e (near-trapdoor vector) must argmax to its true pair
    with confidence ratio ≈ 1.0. Confirms the lattice→classifier handoff."""
    inst = build_leakage_instance(seed, k=k)
    res = clf.classify(inst["e_scalar"])
    ok = res["pair"] == inst["true_pair"] and abs(res["pair_ratio"] - 1.0) < 1e-6
    return {
        "true_pair": inst["true_pair"], "argmax_pair": res["pair"],
        "pair_ratio": res["pair_ratio"], "pass": ok,
    }


def snr_proxy(seed: int, k: int = 7, q: int = TOY_P) -> dict:
    """§3.5 conditional: SNR proxy ‖e‖/‖A·s‖ on the GENERIC toy instance
    (sparse-uniform η=2 error — the toy analog of the spec noise), not the
    planted-ZD error."""
    inst = gen_toy_instance(seed=seed, q=q, k=k)
    lwe = build_scalar_lwe(inst["A"], inst["s"], inst["e"], q)
    e = inst["e_scalar_signed"]
    # A·s (centred) = b − e (mod q), lifted to (−q/2, q/2].
    def centre(x):
        x %= q
        return x if x <= q // 2 else x - q
    As = [centre(lwe["b_scalar"][i] - e[i]) for i in range(lwe["n_eff"])]
    ne, nas = l2_norm(e), l2_norm(As)
    return {"seed": seed, "norm_e": ne, "norm_As": nas,
            "snr_ratio": (ne / nas) if nas else float("inf")}


def run_full_sweep(betas=BETAS, seeds=SAMPLE_SEEDS, k: int = 7, q: int = TOY_P) -> dict:
    clf = FanoLineClassifier(q)
    rows_out = []
    for beta in betas:
        for seed in seeds:
            inst = build_leakage_instance(seed, k=k, q=q)
            reduced = run_bkz(inst["B"], beta)
            min_reduced = min(l2_norm(r) for r in reduced)
            solved = min_reduced < 1.5 * inst["v_target_norm"]
            for row in sweep_cutoff(reduced, inst["n_eff"], inst["true_pair"], clf):
                row.update({"beta": beta, "seed": seed, "k": k,
                            "true_pair": inst["true_pair"],
                            "target_norm": inst["v_target_norm"],
                            "bkz_min_norm": min_reduced, "solved_usvp": solved})
                rows_out.append(row)
    return {"k": k, "q": q, "rows": rows_out}


def pooled(rows, beta, Nf):
    """Pool recovery across seeds at fixed (β, N): total hits / total short."""
    sel = [r for r in rows if r["beta"] == beta and abs(r["N"] - Nf) < 1e-9]
    tot_short = sum(r["n_short"] for r in sel)
    tot_hits = sum(round(r["recovery"] * r["n_short"]) for r in sel)
    rate = tot_hits / tot_short if tot_short else 0.0
    return {"beta": beta, "N": Nf, "tot_short": tot_short, "tot_hits": tot_hits,
            "rate": rate, "sigma": sigma_vs_baseline(rate, tot_short)}


def main() -> None:
    q = TOY_P
    clf = FanoLineClassifier(q)
    print("=" * 78)
    print("OP-2.58.2d BKZ smoke test (Brief 09) — toy scale q=911, k=7")
    print("=" * 78)

    s = item2_sanity_check(clf)
    print(f"\n[Item 2] known-leakage sanity: planted e → argmax {s['argmax_pair']} "
          f"(true {s['true_pair']}), ratio {s['pair_ratio']:.4f} — "
          f"{'PASS' if s['pass'] else 'FAIL'}")
    if not s["pass"]:
        print("  *** sanity FAILED — lattice→classifier handoff bug; brief blocked ***")
        sys.exit(1)

    res = run_full_sweep(k=7)
    rows = res["rows"]
    print("\n[Item 3] cutoff sweep (per (β, seed, N); k=7)")
    hdr = f"{'β':>3} {'seed':>9} {'N':>5} {'n_short':>8} {'recov':>7} {'σ':>7} {'minNorm':>9} {'solved':>7}"
    print(hdr)
    print("-" * len(hdr))
    for r in rows:
        print(f"{r['beta']:>3} {r['seed']:>9} {r['N']:>5} {r['n_short']:>8} "
              f"{r['recovery']:>7.3f} {r['sigma']:>7.2f} {r['bkz_min_norm']:>9.2f} "
              f"{str(r['solved_usvp']):>7}")

    print("\n[Item 3] pooled across seeds at each (β, N)")
    hdr2 = f"{'β':>3} {'N':>5} {'tot_short':>10} {'tot_hits':>9} {'rate':>7} {'σ_pooled':>9}"
    print(hdr2)
    print("-" * len(hdr2))
    for beta in BETAS:
        for Nf in N_VALUES:
            p = pooled(rows, beta, Nf)
            print(f"{beta:>3} {Nf:>5} {p['tot_short']:>10} {p['tot_hits']:>9} "
                  f"{p['rate']:>7.3f} {p['sigma']:>9.2f}")

    print("\n[Item 5] SNR proxy ‖e‖/‖A·s‖ on generic toy instances (η=2)")
    for seed in SAMPLE_SEEDS:
        sn = snr_proxy(seed)
        print(f"  seed {seed}: ‖e‖={sn['norm_e']:.2f} ‖A·s‖={sn['norm_As']:.1f} "
              f"SNR={sn['snr_ratio']:.6f}")


if __name__ == "__main__":
    main()
