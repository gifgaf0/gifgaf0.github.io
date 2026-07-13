#!/usr/bin/env sage
# -*- coding: utf-8 -*-
"""op_2_58_2d_estimator.sage — leaky-LWE-Estimator harness (Brief LEAKY-LWE Item 3).

Reads the OP-2.58.2d LWE parameters + hint structure from the on-branch
construction (per `op_2_58_2d_estimator_recon.md`), builds a DBDD instance
matching `build_scalar_lwe`, integrates perfect hints for the chosen
bracket (weak = F_L union complement, 2/block; strong = per-pair
complement, 12/block), and returns a predicted bikz via `DBDD_optimized`.

**LABEL — illustrative not binding.** The single-number bikz emitted here
is an R3 analytic prediction, not the OP-2.58.2d closure metric. The
binding number requires session-side integration of the per-block 21^k
guess cost (Phase 2), which the estimator does not model. Cite as: "R3
proxy, bracket = <weak|strong>, k = <7|14|32>, bikz = <n>, upper bound on
pair-classifier β per brief §1."

Prerequisites — see `estimator_setup.md`:
  - Sage 9.0+ (validated 10.x).
  - leaky-LWE-Estimator cloned; framework/ path exposed via
    LEAKY_LWE_PATH env var.
  - Validation gate PASSED (a documented example reproduced its reference
    bikz within ±1) BEFORE running this harness.

Usage:
    sage op_2_58_2d_estimator.sage --toy-k 7 --bracket weak
    sage op_2_58_2d_estimator.sage --toy-k 14 --bracket strong
    sage op_2_58_2d_estimator.sage --spec --bracket weak

The `--spec` flag runs at k=32, q=4_294_977_961. Strong-bracket spec
(384 hints) may be slow with DDGR successive integration; if so, the
fallback (May-Nowakowski single-stroke integrator, eprint 2023/777) is
recorded in the setup note for Phase 2. Not implemented here — brief §4.3
"Do not implement the fallback pre-emptively."
"""

from __future__ import print_function

import argparse
import os
import sys


# =============================================================================
# On-branch OP-2.58.2d parameters (READ from the construction; see recon memo)
# =============================================================================

SPEC_Q = 4_294_977_961
TOY_Q = 911
DIM = 16                    # sedenion dimension; from sedenion_Fp.DIM
SIGMA = 2                   # pinned per Brief 10.7 / §2.69.3
FANO_UNION_RANK = 14        # per D1; complement 2/block
KAB_RANK = 4                # per §2.58.B.1; complement 12/block
NUM_PAIRS = 21              # cross-edge pairs (a<b, {1..7})


def scalar_lwe_params(spec: bool, toy_k: int):
    """The base scalar-LWE parameters the estimator consumes (recon §1)."""
    if spec:
        k, q = 32, SPEC_Q
        h_s = 64
    else:
        assert toy_k in (7, 14), "toy_k must be 7 or 14 per pre-reg §3.1 secondary"
        k, q = toy_k, TOY_Q
        h_s = int(round(64.0 * k / 32.0))  # matches gen_toy_instance line 291
    n = k * DIM
    m = n                                   # one sample per scalar coordinate
    # DBDD variance target: the confined per-coordinate variance measured
    # empirically at σ=2 (Brief 10.7 §2.69.3 = 1.33). Using the empirical
    # value rather than σ² = 4 because the confinement to K_{a,b} drops
    # per-coord variance below the naive setting; DBDD uses this to compute
    # the target norm.
    sigma_var_percoord = 1.33
    return {
        "k": k, "n": n, "m": m, "q": q,
        "h_s": h_s, "sigma": SIGMA, "sigma_var_percoord": sigma_var_percoord,
    }


def bracket_hint_count(bracket: str, k: int) -> int:
    """Number of perfect hints per bracket (recon §2)."""
    if bracket == "weak":
        return 2 * k          # F_L union complement (attacker-free)
    if bracket == "strong":
        return 12 * k         # per-pair K_{a,b} complement (needs 21^k guess)
    raise ValueError(f"unknown bracket {bracket!r}; use 'weak' or 'strong'")


# =============================================================================
# leaky-LWE-Estimator import
# =============================================================================


def _import_estimator():
    """Add the estimator's framework/ to sys.path and import DBDD_optimized.

    Location is either the LEAKY_LWE_PATH env var (recommended per setup
    note) or a set of standard fall-back locations."""
    candidates = []
    env = os.environ.get("LEAKY_LWE_PATH")
    if env:
        candidates.append(env)
    home = os.path.expanduser("~")
    candidates += [
        os.path.join(home, "tools", "leaky-LWE-Estimator", "framework"),
        os.path.join(home, "leaky-LWE-Estimator", "framework"),
        "/opt/leaky-LWE-Estimator/framework",
    ]
    for c in candidates:
        if os.path.isdir(c):
            sys.path.insert(0, c)
            try:
                from framework.DBDD_optimized import DBDD_optimized      # noqa: F401
                from framework.instance_gen import build_LWE_instance    # noqa: F401
                return c
            except ImportError:
                try:
                    from DBDD_optimized import DBDD_optimized            # noqa: F401
                    return c
                except ImportError:
                    continue
    raise ImportError(
        "leaky-LWE-Estimator framework/ not found. Set LEAKY_LWE_PATH env var "
        "or clone the repo per estimator_setup.md §2."
    )


# =============================================================================
# Hint vectors per bracket
# =============================================================================


def _fano_union_complement_basis(q):
    """The 2-vector per-block complement of the F_L union.

    Delegates to the on-branch _fano_union_basis to keep the harness
    consistent with the ratified basis-(b) reading (I) F_L-restriction.
    Complement = null-space of the rank-14 F_L union basis matrix inside
    the DIM=16 ambient block. Returns 2 length-DIM vectors of Sage
    IntegerModRing(q) entries."""
    # Route through the on-branch computation for identity with the
    # `build_fano_projected_lattice` path.
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))))  # hybrid_kem/tools/ → repo root
    sys.path.insert(0, os.path.join(project_root, "tools"))
    from op_2_58_2d_lattice_attack import _fano_union_basis
    F_basis = _fano_union_basis(q)          # 14 length-DIM vectors
    # Compute null-space over Q (integer field), then lift to F_q. The 2 null
    # vectors are the F_L⊥ complement; they annihilate every e_d whose
    # dominant support is inside F_L (i.e., every e produced by gen_zd_noise
    # per §2.58.B, since K_{a,b} ⊂ F_L union for all (a,b)).
    from sage.all import Matrix, QQ, IntegerModRing
    M = Matrix(QQ, F_basis)                  # 14 × DIM
    ns = M.right_kernel().basis()            # should have length DIM - 14 = 2
    Zq = IntegerModRing(q)
    return [[Zq(int(x)) for x in v] for v in ns]


def _per_pair_kab_complement_basis(q, a, b):
    """The 12-vector complement of K_{a,b} inside the DIM=16 block for a
    single per-block pair (a, b).

    Requires the pair (a, b) — this is the strong-bracket hint model that
    presumes per-block pair oracle (or 21^k guess cost). Delegates to
    op_2252_v2_kernel_involution for the K_{a,b} basis."""
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))))
    sys.path.insert(0, os.path.join(project_root, "tools"))
    from sedenion_Fp import add_vec, basis_vec
    from op_2252_v2_kernel_involution import lmm, rref_kernel
    from sage.all import Matrix, QQ, IntegerModRing
    z = add_vec(basis_vec(a), basis_vec(b + 8), q)
    K = rref_kernel(lmm(z, q), q)            # 4 length-DIM vectors
    M = Matrix(QQ, [[int(x) for x in v] for v in K])
    ns = M.right_kernel().basis()            # length DIM - 4 = 12
    Zq = IntegerModRing(q)
    return [[Zq(int(x)) for x in v] for v in ns]


def _stack_block_hints(per_block_vecs, k, n_ambient):
    """Extend per-block hint vectors to the full n_ambient = k·DIM error
    space by zero-padding: each block's hint is nonzero only in that
    block's DIM=16 coord range. Returns a list of length-n_ambient vectors."""
    hints = []
    from sage.all import IntegerModRing
    for i in range(k):
        for v in per_block_vecs[i]:
            padded = [0] * n_ambient
            for d in range(DIM):
                padded[i * DIM + d] = int(v[d])
            hints.append(padded)
    return hints


# =============================================================================
# Predicted bikz
# =============================================================================


def predict_bikz(params, bracket, verbose=True):
    """Build the DBDD instance from `params` (recon §1), integrate the
    bracket's perfect hints (recon §2), and return `DBDD_optimized`'s
    bikz + hint-integration diagnostics."""
    estimator_path = _import_estimator()
    from framework.DBDD_optimized import DBDD_optimized
    from sage.all import (
        RR, ZZ, IntegerModRing, block_diagonal_matrix, identity_matrix,
        random_matrix, sqrt, vector,
    )

    n, m, q = params["n"], params["m"], params["q"]
    h_s = params["h_s"]
    sigma_var = params["sigma_var_percoord"]

    if verbose:
        print(f"[params] n={n} m={m} q={q} h_s={h_s} sigma_var_percoord={sigma_var}")
        print(f"[bracket] {bracket}: {bracket_hint_count(bracket, params['k'])} total hints")

    # Build a placeholder LWE instance matching the params. For the
    # analytic bikz the concrete A does not affect the estimator's
    # prediction (DBDD is dimension/variance-driven); use a random A over
    # F_q so the framework's DBDD constructor accepts it.
    Zq = IntegerModRing(q)
    A = random_matrix(Zq, m, n)              # not the deployed A, but same shape
    # Placeholder secret / error (values discarded by the estimator; only
    # distribution parameters matter for the bikz prediction).
    s = vector(ZZ, [0] * n)
    e = vector(ZZ, [0] * m)
    b = A * s + e

    # Configure DBDD_optimized with the confined-noise variance and
    # sparse-ternary secret density h_s/n.
    dbdd = DBDD_optimized(
        A, b, s, e, q,
        sigma=sqrt(sigma_var),               # per-coord std ≈ 1.155
        secret_type="sparse_ternary",
        weight=h_s,
    )

    # Build the bracket's hint vectors and integrate as perfect hints on e.
    if bracket == "weak":
        # Union-level: same 2 F_L⊥ vectors per block for every block.
        per_block = _fano_union_complement_basis(q)
        per_block_list = [per_block] * params["k"]
    elif bracket == "strong":
        # Per-pair: the strong-bracket assumes an oracle for the per-block
        # (a_i, b_i). For the ILLUSTRATIVE bikz we choose a canonical pair
        # per block (e.g., (1,2) for every block) — the estimator's bikz
        # depends only on the hint dimensionality and its independence,
        # not on the specific pair choice, so any per-block pair choice
        # gives the same bikz. The per-block pair variability shows up in
        # the 21^k GUESS cost, which is session-side (not modeled here).
        a_default, b_default = 1, 2
        per_pair = _per_pair_kab_complement_basis(q, a_default, b_default)
        per_block_list = [per_pair] * params["k"]
    else:
        raise ValueError(bracket)

    hint_vecs = _stack_block_hints(per_block_list, params["k"], n)

    # Integrate hints one at a time (DDGR successive integration).
    for h_i, v in enumerate(hint_vecs):
        # DBDD API: integrate_perfect_hint on the error subspace with l=0
        # ⇔ the noise-annihilation form ⟨e, v⟩ = 0.
        v_sage = vector(ZZ, v)
        dbdd.integrate_perfect_hint(v_sage, 0, direction="error")
        if verbose and (h_i + 1) % 50 == 0:
            print(f"  integrated {h_i + 1}/{len(hint_vecs)} hints...")

    bikz = dbdd.estimate_attack(silent=False)

    return {
        "bracket": bracket, "params": params,
        "n_hints_integrated": len(hint_vecs),
        "predicted_bikz": float(bikz),
        "estimator_path": estimator_path,
    }


# =============================================================================
# Schedule β context (for the one-line comparison per brief §4.4)
# =============================================================================

SCHEDULE_BETAS = (20, 30, 40, 45, 50, 55, 60)


def schedule_context(bikz: float) -> str:
    """One-line comparison of predicted bikz against the schedule β-set.

    Per brief §1: "the estimator's bikz is an upper bound on the β at
    which OP-2.58.2d's pair classifier would fire." So if bikz ≤ some
    scheduled β, the schedule is *predicted* to return positive at or
    before that β. This is R3 only."""
    hits = [b for b in SCHEDULE_BETAS if bikz <= b]
    if not hits:
        return (f"[R3] bikz {bikz:.1f} exceeds every scheduled β "
                f"(max {SCHEDULE_BETAS[-1]}) — schedule predicted NULL")
    first = hits[0]
    return (f"[R3] bikz {bikz:.1f} ≤ β={first} — schedule predicted "
            f"positive at or before β={first} (upper bound; illustrative "
            f"not binding)")


# =============================================================================
# CLI
# =============================================================================


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--spec", action="store_true",
                   help="Run at spec parameters (k=32, q=4,294,977,961). "
                        "Overrides --toy-k. Strong-bracket may be slow "
                        "(384 hints); see brief §4.3 fallback note.")
    p.add_argument("--toy-k", type=int, default=7, choices=[7, 14],
                   help="Toy k ∈ {7, 14} per pre-reg §3.1 secondary run.")
    p.add_argument("--bracket", required=True, choices=["weak", "strong"],
                   help="Weak = F_L union complement (2/block, "
                        "attacker-free). Strong = per-pair K_{a,b} "
                        "complement (12/block, requires 21^k guess).")
    p.add_argument("--quiet", action="store_true")
    args = p.parse_args()

    params = scalar_lwe_params(spec=args.spec, toy_k=args.toy_k)

    print("=" * 78)
    print("OP-2.58.2d leaky-LWE-Estimator R3 proxy")
    print(f"  regime: {'SPEC' if args.spec else 'TOY'}  k={params['k']}  "
          f"n={params['n']}  q={params['q']}  h_s={params['h_s']}  "
          f"σ_var={params['sigma_var_percoord']}")
    print(f"  bracket: {args.bracket}  "
          f"({bracket_hint_count(args.bracket, params['k'])} hints total)")
    print("=" * 78)

    result = predict_bikz(params, args.bracket, verbose=not args.quiet)

    print()
    print(f"[R3 illustrative — NOT the binding OP-2.58.2d closure]")
    print(f"  predicted bikz: {result['predicted_bikz']:.2f}")
    print(f"  {schedule_context(result['predicted_bikz'])}")
    if args.bracket == "strong":
        guess = NUM_PAIRS ** params["k"]
        print(f"  strong-bracket guess cost: 21^{params['k']} = "
              f"{guess:.3e} pair-tuples (per-block regime; session's Phase-2 "
              f"job to model meet-in-the-middle or refinements).")
    print()
    print("Label: R3 analytic proxy. Does NOT close OP-2.58.2 or OP-2.58.2d. "
          "Does NOT substitute for the empirical 42-run schedule. Frozen "
          "pre-reg untouched (running an estimator is not lattice-reduction "
          "against the construction). See op_2_58_2d_estimator_recon.md.")


if __name__ == "__main__":
    main()
