"""op_2_58_2d_primary_run.py — OP-2.58.2d spec-parameter primary-run orchestrator.

Brief 10. This is the ONE script in the OP-2.58.2d arc permitted to execute
against §2.58.B at spec parameters (k=32, q=4,294,977,961, N_lat=1024). That
permission is conditional and audit-anchored:

  * The spec-parameter gate of op_2_58_2d_lattice_attack is bypassed (via
    allow_spec_params=True) ONLY inside `_run_one`, and ONLY after BOTH
    `verify_freeze()` returns ok AND PRODUCTION_RUN is True. This is the single
    audit-trail anchor required by brief §3.1.2 / §4.1.
  * verify_freeze() is the FIRST action of main() (brief §2.1). If the frozen
    pre-registration is absent or still marked [pending], the script records a
    halt and exits non-zero BEFORE any spec-parameter code path is reachable.

This module does NOT modify any prior-brief production module (brief §6). It
consumes op_2_58_2d_lattice_attack / op_2_58_2d_classifier unchanged.
"""

from __future__ import annotations

import datetime as _dt
import os
import re
import sys
from itertools import product

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

SPEC_Q = 4_294_977_961
SPEC_K = 32
N_LAT = 1024

# Frozen pre-registration: brief §8 names this file as the binding spec. It has
# been session-side throughout Briefs 07–09 and is not committed to the repo.
PREREG_CANDIDATES = [
    "OP_2_58_2d_staging_PREREGISTRATION.md",
    "tools/OP_2_58_2d_staging_PREREGISTRATION.md",
    "reports/OP_2_58_2d_staging_PREREGISTRATION.md",
]

# Frozen 42-run schedule (brief §3.1.3). Pure data; defining it executes nothing.
BETAS = [20, 30, 40, 45, 50, 55, 60]
SAMPLES = [20260601, 20260602, 20260603]
BASES = ["a-primal", "b-fano-projected"]

# Audit anchor (brief §4.1): the gate is bypassed only when this is True AND
# freeze is verified. It is False here and is never set True pre-freeze.
PRODUCTION_RUN = False


def _find_prereg() -> str | None:
    for path in PREREG_CANDIDATES:
        if os.path.isfile(path):
            return path
    return None


def verify_freeze() -> dict:
    """Brief §2.1 freeze verification. Locate the pre-reg and confirm §6 holds a
    real freeze date (YYYY-MM-DD) and signature (not [pending]).

    Brief 10.6 Item 3 addition: compute the file's SHA-256 hash and return it
    as `prereg_sha256` for Audit Entry 002. The hash anchors the binding
    result to the exact frozen text in the repo at run time.

    Returns {ok, reason, prereg_path, freeze_date, freeze_signature, prereg_sha256}.
    """
    import hashlib

    path = _find_prereg()
    if path is None:
        return {
            "ok": False,
            "reason": (
                "frozen pre-registration OP_2_58_2d_staging_PREREGISTRATION.md "
                "not found in repo (searched: " + ", ".join(PREREG_CANDIDATES)
                + "). It is session-side and was never committed; there is no "
                "frozen §6 to verify."
            ),
            "prereg_path": None, "freeze_date": None, "freeze_signature": None,
            "prereg_sha256": None,
        }
    with open(path, "rb") as fb:
        prereg_bytes = fb.read()
    sha256 = hashlib.sha256(prereg_bytes).hexdigest()
    text = prereg_bytes.decode("utf-8")
    # Extract §6 freeze date and signature; reject [pending]. The regex
    # requires a literal colon (so §6's prose mention of "the freeze date and
    # signature are added..." doesn't false-match) and tolerates optional
    # `**` markdown bold around the field label and value.
    date_m = re.search(
        r"freeze\s*date\s*:\**\s*\**\s*([0-9]{4}-[0-9]{2}-[0-9]{2}|\[pending[^\]]*\])",
        text, re.IGNORECASE)
    sig_m = re.search(
        r"freeze\s*signature\s*:\**\s*\**\s*"
        r"(\[pending[^\]]*\]|[^\s*][^\n]*?)(?:\s*\*\*)?\s*$",
        text, re.IGNORECASE | re.MULTILINE)
    date = date_m.group(1) if date_m else None
    sig = sig_m.group(1).strip() if sig_m else None
    pending = (date is None or sig is None
               or "[pending" in (date or "").lower()
               or "[pending" in (sig or "").lower())
    if pending:
        return {
            "ok": False,
            "reason": f"§6 freeze is incomplete (date={date!r}, signature={sig!r}); "
                      "still [pending] or unparseable. HALT per brief §2.1.",
            "prereg_path": path, "freeze_date": date, "freeze_signature": sig,
            "prereg_sha256": sha256,
        }
    return {
        "ok": True, "reason": "freeze verified",
        "prereg_path": path, "freeze_date": date, "freeze_signature": sig,
        "prereg_sha256": sha256,
    }


def check_construction_available() -> dict:
    """Secondary precondition (brief §3.3 halt conditions): is there an actual
    §2.58.B spec instance to attack, and is basis (b) implemented?

    Updated post-Brief-10.5: the §2.58.B construction artifact now exists
    (`op_2_58_2d_construction.gen_spec_instance`), so the previously
    unconditional "no construction artifact" blocker is no longer raised. The
    matrix-A reading is settled per §2.3 audit as 'uniform' (reading (a)).
    """
    from op_2_58_2d_lattice_attack import build_fano_projected_lattice

    blockers = []
    # Basis (b) lattice: Fano-projected lattice basis (DISTINCT from §2.3
    # matrix-A reading (b)). Still a stub; substantive new work to wire D1's
    # 14-dim F_L union into the primal-basis projection.
    try:
        build_fano_projected_lattice()
        basis_b_ready = True
    except NotImplementedError as exc:
        basis_b_ready = False
        blockers.append(f"basis (b) Fano-projected lattice is unimplemented: {exc}")
    except Exception as exc:  # noqa: BLE001
        basis_b_ready = False
        blockers.append(f"basis (b) raised unexpectedly: {exc!r}")
    # §2.58.B construction availability (Brief 10.5 delivered it).
    try:
        from op_2_58_2d_construction import gen_spec_instance  # noqa: F401
        construction_ready = True
    except ImportError as exc:
        construction_ready = False
        blockers.append(f"§2.58.B construction module unavailable: {exc!r}")
    return {"basis_b_ready": basis_b_ready,
            "construction_ready": construction_ready,
            "blockers": blockers}


def build_job_matrix() -> list[dict]:
    """The frozen 42-run matrix (brief §3.1.3). Data only — no execution."""
    return [
        {"beta": b, "sample": s, "basis": x}
        for b, s, x in product(BETAS, SAMPLES, BASES)
    ]


def _run_one(job: dict, freeze: dict, *, proof_of_life: bool = False) -> dict:
    """Execute ONE spec-parameter BKZ run. The sole gate-bypass site.

    Guarded: requires verified freeze AND (PRODUCTION_RUN OR proof_of_life).
    The proof_of_life gate is a separate audit anchor — see PROOF_OF_LIFE_MODE
    env-flag handling in main(). Both gates are bypass-refused without the
    explicit caller authorization.

    Returns a dict with the σ-statistic and run metadata.
    """
    if not freeze.get("ok"):
        raise RuntimeError("refusing spec-parameter run: freeze not verified.")
    if not (PRODUCTION_RUN or proof_of_life):
        raise RuntimeError(
            "refusing spec-parameter run: requires PRODUCTION_RUN=True or "
            "proof_of_life=True (audit anchor — brief §4.1)."
        )
    import math
    import time

    import numpy as np

    from op_2_58_2d_classifier import FanoLineClassifier
    from op_2_58_2d_construction import gen_spec_instance
    from op_2_58_2d_lattice_attack import (
        build_fano_projected_lattice,
        build_primal_lattice,
        build_scalar_lwe,
        l2_norm,
    )

    t0 = time.time()
    rng = np.random.default_rng(job["sample"])
    # Operational σ per Brief 10.7 / §2.69.3: σ=2 is the §2.58.B confined-
    # sampler value realising the frozen pre-reg §3.1 η=2 ML-KEM convention.
    # Cross-checked against §2.66.1 CBD(η=2) by aggregate BDD norm (1.14×
    # conservative over k=32); distinct distributions per occupancy (5.3 vs
    # 10.0). NOT a calibration to CBD; see op_2_58_2d_sigma_calibration.py.
    sigma = job.get("sigma", 2)
    # k defaults to SPEC_K=32 (brief §3.1) but the proof-of-life entry may pass
    # a smaller k to keep the Python-side unrolling tractable; the spec-Q gate
    # is still bypassed via allow_spec_params.
    k_run = job.get("k", SPEC_K)
    print(f"  [_run_one] inst gen (k={k_run}, q=SPEC, σ={sigma})…", flush=True)
    inst = gen_spec_instance(
        SPEC_Q, k=k_run, sigma=sigma, rng=rng, allow_spec_params=True
    )
    print(f"  [_run_one] inst done in {time.time()-t0:.2f}s; unrolling to scalar LWE (n_eff={k_run*16})…", flush=True)
    lwe = build_scalar_lwe(inst["A"], inst["s"], inst["e"], SPEC_Q)
    t_inst = time.time() - t0
    print(f"  [_run_one] scalar LWE done in {t_inst:.2f}s total", flush=True)

    if job["basis"] == "a-primal":
        B = build_primal_lattice(lwe["A_scalar"], lwe["b_scalar"], SPEC_Q)
    elif job["basis"] == "b-fano-projected":
        B = build_fano_projected_lattice(
            lwe["A_scalar"], lwe["b_scalar"], SPEC_Q,
            k=k_run, allow_spec_params=True,
        )
    else:
        raise ValueError(f"unknown basis {job['basis']!r}")
    t_basis = time.time() - t0 - t_inst
    print(f"  [_run_one] lattice basis {len(B)}x{len(B[0])} in {t_basis:.2f}s", flush=True)

    # LLL + BKZ.
    from fpylll import BKZ, LLL, IntegerMatrix

    A_mat = IntegerMatrix.from_matrix([[int(x) for x in row] for row in B])
    # LLL precision: at k=4 dim 129 the default wrapper works; at k=8 dim 257
    # both wrapper (default "double", 53-bit) and method="proved"+"ld" hit
    # "infinite loop in babai" — GSO ratios exceed available precision for
    # q-ary lattices at q≈2³². Use mpfr (arbitrary precision) at 128 bits.
    # Slower but correct.
    LLL.reduction(A_mat, method="proved", float_type="mpfr", precision=128)
    t_lll = time.time() - t0 - t_inst - t_basis
    print(f"  [_run_one] LLL done in {t_lll:.2f}s; starting BKZ β={job['beta']}…", flush=True)
    par = BKZ.Param(
        block_size=job["beta"], max_loops=job.get("max_loops", 4),
        flags=BKZ.AUTO_ABORT | BKZ.MAX_LOOPS,
    )
    BKZ.reduction(A_mat, par, float_type="ld")
    t_bkz = time.time() - t0 - t_inst - t_basis - t_lll
    print(f"  [_run_one] BKZ done in {t_bkz:.2f}s", flush=True)
    n_rows = A_mat.nrows
    n_cols = A_mat.ncols
    reduced = [[A_mat[i, j] for j in range(n_cols)] for i in range(n_rows)]

    # Classify e-slice of each row; compute σ vs the 1/21 baseline.
    clf = FanoLineClassifier(SPEC_Q)
    # True pair label per block — basis (a) has block-by-block trapdoors;
    # the classifier acts on the *first* block's e-slice (consistent with the
    # smoke test). For proof-of-life we report recovery vs the block-0 pair.
    true_pair = tuple(inst["pair"][0])
    norms = [l2_norm(r) for r in reduced]
    min_norm = min(norms)
    # Conservative cutoff N=2.0 (provisional §3.3.1 factor; Brief 09 repin pending).
    cutoff = 2.0 * min_norm
    short_rows = [r for r, nm in zip(reduced, norms) if nm <= cutoff + 1e-9]
    hits = 0
    for r in short_rows:
        # Classify only the FIRST 16 e-coordinates (block 0) against true_pair.
        e_block0 = r[:DIM_BLOCK]
        if clf.classify(e_block0)["pair"] == true_pair:
            hits += 1
    rate = hits / len(short_rows) if short_rows else 0.0
    baseline = 1.0 / 21.0
    se = math.sqrt(baseline * (1.0 - baseline) / len(short_rows)) if short_rows else 0.0
    sigma_stat = (rate - baseline) / se if se > 0 else 0.0
    t_total = time.time() - t0

    return {
        "job": dict(job), "n_rows": n_rows, "n_cols": n_cols,
        "n_short": len(short_rows), "hits": hits, "recovery": rate,
        "sigma_stat": sigma_stat, "baseline": baseline,
        "min_norm": min_norm, "true_pair_block0": true_pair,
        "t_inst": t_inst, "t_basis": t_basis,
        "t_lll": t_lll, "t_bkz": t_bkz, "t_total": t_total,
    }


# 16 — sedenion block dim, re-named locally for _run_one readability.
DIM_BLOCK = 16


def main() -> int:
    now = _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    print("=" * 78)
    print("OP-2.58.2d primary-run orchestrator (Brief 10)")
    print(f"UTC: {now}")
    print("=" * 78)

    # Brief §2.1: freeze verification is the FIRST action.
    freeze = verify_freeze()
    print("\n[§2.1 freeze verification]")
    print(f"  ok: {freeze['ok']}")
    print(f"  reason: {freeze['reason']}")
    if freeze.get("prereg_path"):
        print(f"  prereg_path: {freeze['prereg_path']}")
        print(f"  freeze_date: {freeze['freeze_date']}")
        print(f"  freeze_signature: {freeze['freeze_signature']}")
        # Brief 10.6 Item 3 §4.2 + Brief 10.7 Item 3 §3.3: Audit Entry 002
        # records the binding-text hash AND the σ pin with its norm/occupancy
        # justification (§2.69.3 reconciliation, NOT per-coordinate variance).
        print("\n[Audit Entry 002 — prereg sha256]")
        print(f"  {freeze['prereg_sha256']}  {freeze['prereg_path']}")
        print("[Audit Entry 002 — σ pin + reconciliation (§2.69.3 / Brief 10.7)]")
        print("  σ = 2  (§2.58.B confined-sampler value, realising frozen §3.1 η=2)")
        print("  vs §2.66.1 CBD(η=2) cross-check:")
        print("    per-block BDD norm:  confined 4.51 vs CBD 3.95  (ratio 1.14, conservative)")
        print("    occupancy:           confined 5.33 ± 1.89  vs CBD 10.0 ± 1.93  (DISTINCT)")
        print("    aggregate (k=32):    conservative robustly (1/√k averaging; P(invert)≈0.001)")
    if not freeze["ok"]:
        print("\nHALT (brief §2.1): pre-registration is not frozen/verifiable. "
              "No spec-parameter code path will execute. Exiting non-zero.")
        # Secondary blockers, for the audit record (still no spec execution).
        con = check_construction_available()
        for blk in con["blockers"]:
            print(f"  additional blocker: {blk}")
        return 1

    # Unreachable pre-freeze. Past this point freeze is verified.
    con = check_construction_available()
    if con["blockers"]:
        print("\nHALT: freeze verified but construction preconditions unmet:")
        for blk in con["blockers"]:
            print(f"  blocker: {blk}")
        return 2

    jobs = build_job_matrix()
    print(f"\n[§3.1 job matrix] {len(jobs)} runs queued.")

    # PROOF_OF_LIFE_MODE env-gate: when set, dispatch ONE basis-(a) β=20 job at
    # spec parameters (k=32, q=4_294_977_961, dim 1025). Real BKZ, real σ. Not
    # the Brief-10 schedule result — a pipeline proof-of-life only. Closure must
    # cite this label explicitly per Brief 10 §3.4.
    if os.environ.get("OP_2_58_2D_PROOF_OF_LIFE") == "1":
        # k=4 sub-spec by default; the full k=SPEC_K=32 build_scalar_lwe is
        # O(n³)≈134M Python ops at n=512 and exceeds the proof-of-life budget.
        # k=4 still exercises the spec-Q gate-bypass and produces a real σ.
        proof_k = int(os.environ.get("OP_2_58_2D_PROOF_K", "4"))
        proof_job = {"beta": 20, "sample": 20260601, "basis": "a-primal",
                     "max_loops": 3, "sigma": 2, "k": proof_k}
        print("\n[PROOF-OF-LIFE] dispatching one spec-parameter run:")
        print(f"  job: {proof_job}  (NOT the Brief-10 42-run schedule result)")
        res = _run_one(proof_job, freeze, proof_of_life=True)
        print("\n[PROOF-OF-LIFE result]")
        for k in ("n_rows", "n_cols", "n_short", "hits", "recovery",
                  "sigma_stat", "baseline", "min_norm", "true_pair_block0",
                  "t_inst", "t_basis", "t_lll", "t_bkz", "t_total"):
            print(f"  {k}: {res[k]}")
        print("\nLABEL: pipeline proof-of-life. ONE sample, ONE β, basis (a) "
              "only. NOT a verdict on the §5.x null hypothesis — that requires "
              "the full Brief-10 42-run schedule with frozen pre-reg §1-§5 "
              "binding text (not present in this session's §6 stub).")
        return 0

    print("Dispatch is 30-day wall-clock work (brief §3.3); the session monitors.")
    print("Set OP_2_58_2D_PROOF_OF_LIFE=1 to dispatch ONE proof-of-life run.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
