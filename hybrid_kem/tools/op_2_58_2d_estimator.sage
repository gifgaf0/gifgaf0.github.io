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


def _project_root():
    """Repo root (containing tools/). Under `sage`, __file__ is a temp preparsed
    file, so prefer the OP_PROJECT_ROOT env var; fall back to __file__ heuristics."""
    env = os.environ.get("OP_PROJECT_ROOT")
    if env and os.path.isdir(os.path.join(env, "tools")):
        return env
    here = os.path.dirname(os.path.abspath(__file__))
    cand = os.path.dirname(os.path.dirname(here))
    if os.path.isdir(os.path.join(cand, "tools")):
        return cand
    raise RuntimeError("repo root not found; set OP_PROJECT_ROOT to the gifgaf0.github.io checkout.")


def _framework_path():
    """Locate the estimator's framework/ directory (the .sage files are
    Sage-loaded, NOT Python-imported: they use the Sage preparser)."""
    env = os.environ.get("LEAKY_LWE_PATH")
    cands = ([env] if env else []) + [
        os.path.expanduser("~/tools/leaky-LWE-Estimator/framework"),
        os.path.expanduser("~/leaky-LWE-Estimator/framework"),
        "/root/leaky-LWE-Estimator/framework",
        "/opt/leaky-LWE-Estimator/framework",
    ]
    for c in cands:
        if c and os.path.isdir(c):
            return c
    raise ImportError("leaky-LWE-Estimator framework/ not found; set LEAKY_LWE_PATH "
                      "(see estimator_setup.md §1.0/§2).")


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
    project_root = _project_root()
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
    project_root = _project_root()
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
    """Build the DBDD instance from `params` (recon §1) via the estimator's
    supported `initialize_from_LWE_instance` path, integrate the bracket's
    perfect hints on the error block (recon §2), and return the bikz.

    Coordinate convention (verified against the framework): the estimator's
    combined secret is [e (m coords); s (n coords); 1], i.e. ERROR FIRST, so
    a block-i error hint lives on coords [i*DIM : (i+1)*DIM]."""
    fw = _framework_path()
    # The framework is Sage (.sage) — bring its globals in via load(); this runs
    # under `sage this_harness.sage`. initialize_from_LWE_instance, DBDD_optimized,
    # vector, ZZ etc. become available in the global namespace after the load.
    G = globals()
    if "initialize_from_LWE_instance" not in G:
        # instance_gen.sage load()s its deps via CWD-relative "../framework/...",
        # so run the load from inside framework/ (then restore CWD).
        _cwd = os.getcwd()
        os.chdir(fw)
        try:
            load(fw + "/instance_gen.sage")        # noqa: F821 (sage builtin)
        finally:
            os.chdir(_cwd)

    n, m, q, k = params["n"], params["m"], params["q"], params["k"]
    h_s, sigma_var = params["h_s"], params["sigma_var_percoord"]
    if verbose:
        print(f"[params] n={n} m={m} q={q} h_s={h_s} sigma_var_percoord={sigma_var}")
        print(f"[bracket] {bracket}: {bracket_hint_count(bracket, k)} total hints")

    # Distributions as dict laws (recon §1):
    #  - error: confined per-coord variance sigma_var on {-SIGMA,0,+SIGMA};
    #    P(±SIGMA)=p with 2*p*SIGMA^2 = sigma_var.
    #  - secret: sparse-ternary weight h_s over n coords -> {-1:h_s/2n,0:.,1:h_s/2n}.
    p = sigma_var / (2.0 * SIGMA * SIGMA)
    D_e = {-SIGMA: p, 0: 1.0 - 2 * p, SIGMA: p}
    qs = h_s / (2.0 * n)
    D_s = {-1: qs, 0: 1.0 - 2 * qs, 1: qs}

    A, b, dbdd = initialize_from_LWE_instance(         # noqa: F821
        DBDD_optimized, n, q, m, D_e, D_s, verbosity=0)   # noqa: F821
    beta0, delta0 = dbdd.estimate_attack(silent=True)
    if verbose:
        print(f"[baseline] no hints: bikz={float(beta0):.2f} delta={float(delta0):.6f}")

    # Per-block hint bases (recon §2), routed through the on-branch construction.
    if bracket == "weak":
        per_block = _fano_union_complement_basis(q)       # 2 length-DIM vecs
    elif bracket == "strong":
        per_block = _per_pair_kab_complement_basis(q, 1, 2)  # 12; pair-invariant bikz
    else:
        raise ValueError(bracket)

    # Embed into the full [e; s] space (error first) and integrate as perfect
    # hints <e, v> = 0 (l=0), one per block per basis vector.
    n_hints = 0
    for i in range(k):
        for w in per_block:
            full = [0] * (m + n)
            for d in range(DIM):
                val = int(w[d]) % q                       # center-lift F_q -> [-q/2, q/2]
                if val > q // 2:
                    val -= q
                full[i * DIM + d] = val                   # error block i, coord d
            dbdd.integrate_perfect_hint(vector(ZZ, full), 0)   # noqa: F821
            n_hints += 1
            if verbose and n_hints % 50 == 0:
                print(f"  integrated {n_hints} hints...")

    beta, delta = dbdd.estimate_attack(silent=True)
    return {
        "bracket": bracket, "params": params,
        "n_hints_integrated": n_hints,
        "baseline_bikz": float(beta0),
        "predicted_bikz": float(beta),
        "predicted_delta": float(delta),
        "estimator_path": fw,
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
    # ENV-VAR mode (robust under `sage script.sage`, which otherwise grabs --flags):
    #   OP_SPEC=1 | OP_TOY_K=7|14 ; OP_BRACKET=weak|strong ; OP_QUIET=1
    # Falls back to argparse (for Matt's box: `python op_..._estimator.py --toy-k 7 --bracket weak`).
    env_bracket = os.environ.get("OP_BRACKET")
    if env_bracket:
        class _A: pass
        args = _A()
        args.spec = os.environ.get("OP_SPEC", "") not in ("", "0")
        args.toy_k = int(os.environ.get("OP_TOY_K", "7"))
        args.bracket = env_bracket
        args.quiet = os.environ.get("OP_QUIET", "") not in ("", "0")
    else:
        p = argparse.ArgumentParser()
        p.add_argument("--spec", action="store_true")
        p.add_argument("--toy-k", type=int, default=7, choices=[7, 14])
        p.add_argument("--bracket", required=True, choices=["weak", "strong"])
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


# Run directly. (Under `sage script.sage`, Sage exec's the preparsed file with a
# module __name__ that is not "__main__", so guard on the CLI entry differently:
# this file is only ever executed as a harness, never imported.)
if __name__ != "__imported_as_module__":
    main()
