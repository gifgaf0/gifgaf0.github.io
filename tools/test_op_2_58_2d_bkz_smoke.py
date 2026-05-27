"""Tests for op_2_58_2d_bkz_smoke (Brief 09). Toy scale q=911 only.

Fast tests cover the spec-parameter gate, the planted-leakage instance, the
Item-2 sanity check, and the pure cutoff-sweep/σ arithmetic with a stub
classifier. One slow end-to-end test runs a single β=30 BKZ reduction and
asserts the toy uSVP is solved and the trapdoor recovered.
"""

from __future__ import annotations

import math
import sys

import pytest

from tools.op_2_58_2d_bkz_smoke import (
    BASELINE,
    build_leakage_instance,
    item2_sanity_check,
    run_bkz,
    sigma_vs_baseline,
    snr_proxy,
    sweep_cutoff,
)
from tools.op_2_58_2d_classifier import TOY_P, FanoLineClassifier
from tools.op_2_58_2d_lattice_attack import SPEC_K, SPEC_Q, l2_norm

# The smoke harness imports the lattice module via a bare (sys.path) import, so
# the exception it raises is op_2_58_2d_lattice_attack.SpecParamsRefused — a
# different class object than tools.op_2_58_2d_lattice_attack.SpecParamsRefused.
# Grab the harness's actual class so pytest.raises matches.
SpecParamsRefused = sys.modules["op_2_58_2d_lattice_attack"].SpecParamsRefused


# --- spec-parameter gate (brief §3.1 / §4.1) ------------------------------


def test_spec_params_refused_by_default():
    with pytest.raises(SpecParamsRefused):
        build_leakage_instance(seed=20260601, k=SPEC_K, q=SPEC_Q)


def test_spec_q_alone_refused():
    with pytest.raises(SpecParamsRefused):
        build_leakage_instance(seed=20260601, k=7, q=SPEC_Q)


# --- planted leakage instance ---------------------------------------------


def test_planted_e_lies_in_true_pair_kernel():
    clf = FanoLineClassifier(TOY_P)
    inst = build_leakage_instance(20260601, k=7)
    res = clf.classify(inst["e_scalar"])
    assert res["pair"] == inst["true_pair"]
    assert math.isclose(res["pair_ratio"], 1.0, abs_tol=1e-9)


def test_target_is_short_relative_to_gh():
    inst = build_leakage_instance(20260601, k=7)
    # Target ‖(e,s,1)‖ is tiny; the lattice is a large-gap uSVP instance.
    assert inst["v_target_norm"] < 20.0
    assert len(inst["B"]) == 2 * inst["n_eff"] + 1


def test_item2_sanity_passes():
    clf = FanoLineClassifier(TOY_P)
    assert item2_sanity_check(clf)["pass"] is True


# --- σ arithmetic ----------------------------------------------------------


def test_sigma_zero_for_empty_set():
    assert sigma_vs_baseline(0.0, 0) == 0.0


def test_sigma_at_baseline_is_zero():
    assert abs(sigma_vs_baseline(BASELINE, 100)) < 1e-12


def test_sigma_positive_above_baseline():
    s = sigma_vs_baseline(1.0, 3)
    assert s > 5.0  # 3/3 recoveries is > 5σ above 1/21


# --- cutoff sweep arithmetic (stub classifier, no BKZ) --------------------


class _StubClf:
    """Classifies by a marker in coordinate 0 of the e-slice: 7 → (1,7),
    else → (1,2). Lets us test sweep_cutoff without real geometry."""

    def classify(self, v):
        return {"pair": (1, 7) if v[0] == 7 else (1, 2)}


def test_sweep_cutoff_counts_thresholds_and_recovery():
    n_eff = 16
    dim = 2 * n_eff + 1
    # row A: short (norm ~7), recovers (marker 7). rows B,C: longer, no marker.
    rowA = [7] + [0] * (dim - 1)
    rowB = [0] * dim
    rowB[5] = 20  # norm 20
    rowC = [0] * dim
    rowC[6] = 100  # norm 100
    rows = [rowA, rowB, rowC]
    out = sweep_cutoff(rows, n_eff, true_pair=(1, 7), clf=_StubClf(),
                       n_values=[1.0, 3.0, 20.0])
    by_n = {r["N"]: r for r in out}
    # min norm = 7. N=1.0 → only rowA; recovery 1.0.
    assert by_n[1.0]["n_short"] == 1
    assert by_n[1.0]["recovery"] == 1.0
    # N=3.0 → threshold 21 → rowA (7) + rowB (20); recovery 1/2.
    assert by_n[3.0]["n_short"] == 2
    assert math.isclose(by_n[3.0]["recovery"], 0.5)
    # N=20.0 → threshold 140 → all three; recovery 1/3.
    assert by_n[20.0]["n_short"] == 3
    assert math.isclose(by_n[20.0]["recovery"], 1 / 3)


# --- SNR proxy -------------------------------------------------------------


def test_snr_proxy_is_finite_and_small():
    sn = snr_proxy(20260601, k=7)
    assert 0.0 < sn["snr_ratio"] < 0.1
    assert sn["norm_e"] > 0 and sn["norm_As"] > 0


# --- slow end-to-end BKZ ---------------------------------------------------


def test_bkz_beta30_solves_and_recovers():
    """β=30 reduces the toy lattice to the trapdoor and recovers the true pair.

    Slow (~15s): one real BKZ-30 reduction at dim 225."""
    clf = FanoLineClassifier(TOY_P)
    inst = build_leakage_instance(20260601, k=7)
    rows = run_bkz(inst["B"], beta=30)
    min_norm = min(l2_norm(r) for r in rows)
    assert min_norm < 1.5 * inst["v_target_norm"]  # uSVP solved
    sweep = sweep_cutoff(rows, inst["n_eff"], inst["true_pair"], clf,
                         n_values=[2.0])
    assert sweep[0]["recovery"] == 1.0
