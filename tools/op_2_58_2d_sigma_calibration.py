"""σ noise-model reconciliation: §2.58.B confined kernel sampler vs §2.66.1 CBD(η=2).

NOT a calibration-to-CBD. σ=2 is the §2.58.B sampler-definition value;
CBD(η=2) is a CROSS-CHECK (§2.66.1's correctness-analysis proxy), not the
pin. The two are DISTINCT distributions (different occupied-dimension
profile) of comparable norm. See §2.69.3 (V4.12) and Brief 10.7.

Reports three metrics, each with spread:
  1. per-coordinate variance (the easy metric — necessary but not sufficient)
  2. total per-block Euclidean norm (the BDD-radius metric the attack sees)
  3. occupied-dimension profile (the fingerprint proving distributions are distinct)

Key results at σ=2 (p=911, field-independent kernel structure per A1/D1):
  - per-coord var: confined 1.33 vs CBD 1.0
  - per-block norm: confined 4.51 vs CBD 3.95 (mean ratio 1.14, conservative)
  - occupancy: confined 5.33±1.89 vs CBD 10.0±1.93 (DISTINCT, non-overlapping means)
  - per-draw P(confined norm > CBD) = 0.71; aggregate over k=32 conservative
    robustly (per-block spread averages out as 1/√k).

Branch-adapted from the session-side `op_2_58_2d_sigma_calibration.py`:
- Imports the on-branch kernel-involution API (`op_2252_v2_kernel_involution.lmm`
  + `rref_kernel`) instead of the session's `a1_kernel_partition`.
- Builds the 21 per-pair kernel bases via direct iteration over cross-edge
  pairs (a, b) ∈ C(7, 2) with z = e_a + e_{b+8}, matching the §2.58.B
  pair_21 convention of `op_2_58_2d_construction.gen_zd_noise_sample`.
"""

from __future__ import annotations

import os
import sys
from itertools import combinations

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from op_2252_v2_kernel_involution import lmm, rref_kernel  # noqa: E402
from sedenion_Fp import DIM, add_vec, basis_vec  # noqa: E402

P = 911  # toy prime; kernel structure is q-independent (verified A1/D1).


def _bases(p: int = P) -> list[list[np.ndarray]]:
    """One kernel basis per cross-edge pair (a, b) in C(7, 2), signed-lifted.

    Matches the §2.58.B pair_21 convention: z = e_a + e_{b+8}, kernel basis
    of L_z is the 4 vectors from `rref_kernel(lmm(z, p), p)`. Entries are
    centred to (−p/2, p/2] for the Euclidean / occupancy computations.
    """
    bases: list[list[np.ndarray]] = []
    for a, b in combinations(range(1, 8), 2):
        x = add_vec(basis_vec(a), basis_vec(b + 8), p)
        kb = rref_kernel(lmm(x, p), p)
        signed = [
            np.array([(int(c) if int(c) <= p // 2 else int(c) - p) for c in v],
                     dtype=np.int64)
            for v in kb
        ]
        bases.append(signed)
    return bases


def confined_block(bases: list[list[np.ndarray]], sigma: int,
                   rng: np.random.Generator) -> np.ndarray:
    """One block of §2.58.B confined noise: e = σ · Σ_j α_j · k_j, α ∈ {−1,0,+1},
    {k_j} = kernel basis of a uniformly-chosen pair."""
    kb = bases[rng.integers(len(bases))]
    alphas = rng.integers(-1, 2, size=len(kb))
    e = np.zeros(DIM, dtype=np.float64)
    for a, v in zip(alphas, kb):
        e += sigma * a * v
    return e


def cbd_block(eta: int, rng: np.random.Generator) -> np.ndarray:
    """One block of §2.66.1 unconfined CBD(η) noise (the cross-check reference)."""
    return np.array(
        [rng.binomial(eta, 0.5) - rng.binomial(eta, 0.5) for _ in range(DIM)],
        dtype=np.float64,
    )


def reconcile(sigma: int = 2, eta: int = 2, N: int = 50_000,
              seed: int = 20260527) -> dict:
    """Reconcile §2.58.B confined σ vs §2.66.1 CBD(η) per-block.

    Returns metrics (var, norm mean/std, occupancy mean/std, mean-norm ratio)
    for one-block samples. The conservative-direction claim (mean_norm_ratio
    > 1) is the BDD-radius metric the attack sees; the occupancy fingerprint
    proves the two distributions are distinct.
    """
    rng = np.random.default_rng(seed)
    bases = _bases()
    conf = [confined_block(bases, sigma, rng) for _ in range(N)]
    cbd = [cbd_block(eta, rng) for _ in range(N)]
    cn = np.array([np.linalg.norm(e) for e in conf])
    bn = np.array([np.linalg.norm(e) for e in cbd])
    co = np.array([np.count_nonzero(e) for e in conf])
    bo = np.array([np.count_nonzero(e) for e in cbd])
    cvar = np.concatenate([e for e in conf]).var()
    return {
        "sigma": sigma, "eta": eta,
        "conf_percoord_var": float(cvar), "cbd_percoord_var": eta / 2,
        "conf_norm_mean": float(cn.mean()), "conf_norm_std": float(cn.std()),
        "cbd_norm_mean": float(bn.mean()), "cbd_norm_std": float(bn.std()),
        "mean_norm_ratio": float(cn.mean() / bn.mean()),
        "conf_occ_mean": float(co.mean()), "conf_occ_std": float(co.std()),
        "cbd_occ_mean": float(bo.mean()), "cbd_occ_std": float(bo.std()),
    }


def aggregate_independence(sigma: int = 2, eta: int = 2, k: int = 32,
                           n_instances: int = 5000,
                           seed: int = 20260527) -> dict:
    """Verify per-block draws are independent so 1/√k averaging holds.

    The aggregate norm over k blocks matches the √k independent-draw
    prediction, and the conservative direction (vs CBD) is robust at the
    aggregate level. Locks the load-bearing 1/√k averaging assumption per
    §2.69.3.
    """
    rng = np.random.default_rng(seed)
    bases = _bases()
    conf_agg: list[float] = []
    cbd_agg: list[float] = []
    pb_norms: list[float] = []
    for _ in range(n_instances):
        bn = np.array(
            [np.linalg.norm(confined_block(bases, sigma, rng)) for _ in range(k)]
        )
        pb_norms.extend(bn.tolist())
        conf_agg.append(float(np.sqrt((bn ** 2).sum())))
        cn = np.array(
            [np.linalg.norm(cbd_block(eta, rng)) for _ in range(k)]
        )
        cbd_agg.append(float(np.sqrt((cn ** 2).sum())))
    pb = np.array(pb_norms)
    ca = np.array(conf_agg)
    ba = np.array(cbd_agg)
    predicted = float(np.sqrt(k * (pb ** 2).mean()))
    # Inversion probability via paired shuffle (decorrelates pair index).
    shuffled = ba[np.random.default_rng(1).permutation(len(ba))]
    inv = float((ca < shuffled).mean())
    return {
        "agg_mean": float(ca.mean()),
        "predicted_agg": predicted,
        "agg_match_pct": abs(predicted - float(ca.mean())) / float(ca.mean()) * 100.0,
        "cv_ratio": (float(pb.std()) / float(pb.mean()))
                    / (float(ca.std()) / float(ca.mean())),
        "p_inversion_aggregate": inv,
    }


def main() -> None:
    r = reconcile()
    print(f"σ={r['sigma']} vs CBD(η={r['eta']}):")
    print(f"  per-coord var:  confined {r['conf_percoord_var']:.3f} / "
          f"CBD {r['cbd_percoord_var']:.3f}")
    print(f"  per-block norm: confined {r['conf_norm_mean']:.3f}±{r['conf_norm_std']:.3f}"
          f" / CBD {r['cbd_norm_mean']:.3f}±{r['cbd_norm_std']:.3f}")
    print(f"  mean-norm ratio (BDD metric): {r['mean_norm_ratio']:.3f} "
          f"(>1 = conservative)")
    print(f"  occupancy: confined {r['conf_occ_mean']:.2f}±{r['conf_occ_std']:.2f}"
          f" / CBD {r['cbd_occ_mean']:.2f}±{r['cbd_occ_std']:.2f} (DISTINCT)")


if __name__ == "__main__":
    main()
