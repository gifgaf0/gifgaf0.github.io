"""op_2_58_2d_F1_signed_lift_test.py — F1 signed-lift discrimination test (Brief 08).

Runs the production classifier (signed-lift ON) and the disabled-lift variant
(signed-lift OFF) on the same planted ZD-noise input — random α_j ∈ {−1,0,+1}
combinations of the four K_{a,b} kernel basis vectors, N=500, seed 20260527
(the commit-766c6f5 Path B generation protocol) — and measures pair-classifier
and line-classifier recovery for each. Produces the 4-number matrix the F1
closure (§3.2 of the brief) is read from.

Before the recovery rates are trusted, §3.3 disable-path validation runs:
it confirms a candidate entry near q arrives at the projection as a large
positive value under the disabled lift (not its centred equivalent), and that
the production lift still centres it.

Toy scale q=911 only. No spec parameters, no §2.58.B execution.
"""

from __future__ import annotations

import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from op_2_58_2d_classifier import TOY_P, _clean_kernel_vectors  # noqa: E402
from op_2_58_2d_classifier_no_lift import NoLiftFanoLineClassifier  # noqa: E402

SEED = 20260527
N = 500


def instrument_disable_path(p: int = TOY_P) -> dict:
    """§3.1 / §3.3 instrumentation: confirm the signed-lift is actually
    disabled. Build a candidate whose entries are large residues near q and
    check the value reaching the Euclidean projection step under each variant.
    """
    on = NoLiftFanoLineClassifier(p, disable_signed_lift=False)   # production
    off = NoLiftFanoLineClassifier(p, disable_signed_lift=True)   # disabled

    # A candidate with residues near q: e.g. 910, 909, ... at q=911 these are
    # the centred values -1, -2, ... . Pad to a full 16-block candidate.
    near_q = [p - 1, p - 2, p - 3, p - 4, p - 5] + [0] * 11
    before = list(near_q[:5])
    after_on = on._lift(near_q)[:5].tolist()
    after_off = off._lift(near_q)[:5].tolist()

    # Disabled path must keep residues near q as large positives (≥ q-5).
    off_is_large_positive = all(x >= p - 5 for x in after_off)
    # Production path must centre them to small negatives.
    on_is_centred = all(x < 0 for x in after_on)

    return {
        "p": p,
        "candidate_before_lift_first5": before,
        "after_lift_ON_first5": after_on,
        "after_lift_OFF_first5": after_off,
        "disabled_keeps_large_positive": off_is_large_positive,
        "production_centres_to_negative": on_is_centred,
        "disable_path_valid": off_is_large_positive and on_is_centred,
    }


def _pair_to_line_map(clf) -> dict:
    m = {}
    for L in clf.lines:
        a, b, c = sorted(L)
        for pr in [(a, b), (a, c), (b, c)]:
            m[pr] = L
    return m


def measure_recovery(clf, seed: int = SEED, n: int = N) -> dict:
    """Planted ZD-noise recovery for a given classifier instance.

    Identical sampling stream regardless of lift state, so ON vs OFF are
    measured on the same inputs."""
    rng = np.random.default_rng(seed)
    pair_to_line = _pair_to_line_map(clf)
    pair_hits = 0
    line_hits = 0
    for _ in range(n):
        a, b = clf.pairs[rng.integers(len(clf.pairs))]
        basis = _clean_kernel_vectors(a, b, clf.p)
        while True:
            alpha = rng.integers(-1, 2, size=4)
            if alpha.any():
                break
        z = sum(al * bv for al, bv in zip(alpha, basis))
        res = clf.classify(z)
        pair_hits += res["pair"] == (a, b)
        line_hits += res["fano_line"] == pair_to_line[(a, b)]
    return {"pair": pair_hits / n, "line": line_hits / n, "n": n}


def run() -> dict:
    instr = instrument_disable_path(TOY_P)

    clf_on = NoLiftFanoLineClassifier(TOY_P, disable_signed_lift=False)
    clf_off = NoLiftFanoLineClassifier(TOY_P, disable_signed_lift=True)

    with_lift = measure_recovery(clf_on)
    without_lift = measure_recovery(clf_off)

    return {
        "instrumentation": instr,
        "with_lift": with_lift,
        "without_lift": without_lift,
    }


def main() -> None:
    out = run()
    instr = out["instrumentation"]
    print("=" * 70)
    print("F1 — signed-lift discrimination test (q=911, seed=20260527, N=500)")
    print("=" * 70)
    print("\n[§3.3 disable-path validation / instrumentation]")
    print(f"  candidate (first 5)        : {instr['candidate_before_lift_first5']}")
    print(f"  after lift ON  (production): {instr['after_lift_ON_first5']}")
    print(f"  after lift OFF (disabled)  : {instr['after_lift_OFF_first5']}")
    print(f"  disabled keeps ≥ q-5 (+910): {instr['disabled_keeps_large_positive']}")
    print(f"  production centres to neg  : {instr['production_centres_to_negative']}")
    print(f"  DISABLE PATH VALID         : {instr['disable_path_valid']}")
    if not instr["disable_path_valid"]:
        print("  *** disable path invalid — F1 result NOT meaningful; fix before recording ***")
        sys.exit(1)

    wl, nl = out["with_lift"], out["without_lift"]
    print("\n[recovery rates — 4-number matrix]")
    print(f"  {'':<22}{'with lift':<14}{'without lift':<14}")
    print(f"  {'pair classifier':<22}{wl['pair']:<14.3%}{nl['pair']:<14.3%}")
    print(f"  {'line classifier':<22}{wl['line']:<14.3%}{nl['line']:<14.3%}")
    print(f"\n  chance: pair 1/21 = {1/21:.3%}, line 1/7 = {1/7:.3%}")


if __name__ == "__main__":
    main()
