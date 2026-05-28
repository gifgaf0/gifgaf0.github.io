"""Tests for op_2_58_2d_sigma_calibration (Brief 10.7 / §2.69.3).

Locks the load-bearing claims of the σ noise-model reconciliation so a future
refactor cannot silently flip them:
  - conservative-direction in the BDD norm metric (mean_norm_ratio > 1, in
    the expected 1.05–1.25 band);
  - distinct distributions via the occupancy fingerprint (non-overlapping
    means);
  - 1/√k aggregate-averaging assumption (per-block independence) verified at
    k=32 by the √k-prediction match, the CV collapse, and the aggregate
    inversion probability.
"""

from __future__ import annotations

from tools.op_2_58_2d_sigma_calibration import aggregate_independence, reconcile


def test_sigma_reconciliation():
    """§2.69.3: σ=2 confined noise is conservative vs CBD(η=2) in the BDD
    norm metric, and the distributions are distinct (occupancy fingerprint)."""
    r = reconcile(sigma=2, eta=2, N=20000)
    # Conservative direction in the BDD metric (aggregate):
    assert r["mean_norm_ratio"] > 1.0, (
        f"confined σ=2 norm must exceed CBD(η=2) (conservative); "
        f"got ratio {r['mean_norm_ratio']:.3f}"
    )
    assert 1.05 < r["mean_norm_ratio"] < 1.25, (
        f"norm ratio out of expected band; got {r['mean_norm_ratio']:.3f}"
    )
    # Distinct distributions (occupancy means non-overlapping):
    assert r["conf_occ_mean"] < 7 and r["cbd_occ_mean"] > 9, (
        f"occupancy must be distinct: confined {r['conf_occ_mean']:.1f} "
        f"vs CBD {r['cbd_occ_mean']:.1f}"
    )


def test_sigma_aggregate_independence():
    """§2.69.3: per-block noise draws are independent, so the conservative
    direction is robust at the aggregate (k=32) BDD radius the attack sees.
    Locks the load-bearing 1/√k averaging assumption."""
    a = aggregate_independence(sigma=2, eta=2, k=32, n_instances=2000)
    # Aggregate matches the independent-draw sqrt(k) prediction:
    assert a["agg_match_pct"] < 1.0, (
        f"aggregate norm must match √k independent prediction; "
        f"got {a['agg_match_pct']:.2f}% deviation (independence may fail)"
    )
    # CV collapses ~√32 (independence signature):
    assert 4.5 < a["cv_ratio"] < 8.0, (
        f"per-block→aggregate CV ratio should be ≈√32≈5.66; "
        f"got {a['cv_ratio']:.2f}"
    )
    # Conservative direction robust at aggregate:
    assert a["p_inversion_aggregate"] < 0.05, (
        f"P(confined aggregate < CBD aggregate) must be small; "
        f"got {a['p_inversion_aggregate']:.4f}"
    )
