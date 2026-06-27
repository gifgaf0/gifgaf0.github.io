"""op_2_58_2d_bkz_driver.py — Hardened BKZ driver for the OP-2.58.2d primary run.

Brief 11 Item 2. Single consolidation point for the load-bearing
implementation pins the pre-reg names. The smoke test established them;
this module hard-asserts them so a misconfiguration fails fast instead of
silently corrupting (or hanging) the binding 42-run schedule.

Pinned guards (each raises immediately on violation; no silent fallback):

  - **`float_type="ld"`** (pre-reg §3.3.1): default GSO precision hits a
    non-terminating "infinite loop in babai" on q-ary lattices at this
    scale. This is the one bug that does not error — it hangs a multi-day
    run forever. `reduce_lll` and `reduce_bkz` here refuse any other
    float_type.
  - **Exact modulus** (Brief 11 §2c): `assert_spec_q(q)` raises unless
    q == 4_294_977_961 exactly. "q=2³²" is shorthand only; the modulus is
    2³² + 10,665.
  - **−A_scalarᵀ sign convention** (pre-reg §3.6): `round_trip_check`
    verifies the target z·B = (e, s, 1) holds exactly, at both q=911 and
    q=SPEC_Q. The +A_scalarᵀ basis does not round-trip and is rejected.
  - **`PRODUCTION_RUN` gate** (Brief 11 §2d): `assert_spec_gate_enforced`
    confirms the spec-parameter gate catches invocations via the sys.modules
    lookup (the bare-import isinstance check fails because sys.path creates
    two SpecParamsRefused class objects).

All four are pre-flight assertions; calling code is expected to invoke
`run_preflight(q)` once before any spec-parameter dispatch.
"""

from __future__ import annotations

import os
import sys
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

SPEC_Q = 4_294_977_961
SPEC_K = 32

ALLOWED_FLOAT_TYPES = ("ld",)  # long-double GSO ONLY for q-ary spec lattices.


# ---------------------------------------------------------------------------
# Pre-flight 1: float_type="ld" hard guard
# ---------------------------------------------------------------------------


class FloatTypeRefused(RuntimeError):
    """Raised when a reduction is requested without the pre-reg-pinned
    `float_type="ld"`. The default-precision path hits an infinite-loop
    babai condition on q-ary lattices; pre-reg §3.3.1 hard-pins `ld`."""


def _assert_ld(float_type: str | None) -> None:
    if float_type not in ALLOWED_FLOAT_TYPES:
        raise FloatTypeRefused(
            f"refusing reduction with float_type={float_type!r}: pre-reg §3.3.1 "
            f"hard-pins float_type='ld'. Default precision hits the babai "
            f"infinite loop on q-ary lattices; allowed values: {ALLOWED_FLOAT_TYPES!r}."
        )


def reduce_lll(A_mat, *, method: str = "proved", float_type: str = "ld",
               precision: int = 128) -> Any:
    """LLL with the pinned precision. Raises FloatTypeRefused on any other
    float_type. `method="proved"` + `float_type="ld"` + `precision=128`
    matches the proof-of-life run that completed LLL at k=4 spec-Q without
    babai-loop or precision overflow."""
    _assert_ld(float_type)
    from fpylll import LLL
    LLL.reduction(A_mat, method=method, float_type=float_type, precision=precision)
    return A_mat


def reduce_bkz(A_mat, beta: int, *, max_loops: int = 4,
               float_type: str = "ld", flags: int | None = None) -> Any:
    """BKZ-β with the pinned precision. Raises FloatTypeRefused on any
    other float_type."""
    _assert_ld(float_type)
    from fpylll import BKZ
    if flags is None:
        flags = BKZ.AUTO_ABORT | BKZ.MAX_LOOPS
    par = BKZ.Param(block_size=beta, max_loops=max_loops, flags=flags)
    BKZ.reduction(A_mat, par, float_type=float_type)
    return A_mat


# ---------------------------------------------------------------------------
# Pre-flight 2: exact modulus assertion
# ---------------------------------------------------------------------------


class ModulusRefused(RuntimeError):
    """Raised when the pinned modulus check fails. q = 4,294,977,961 exactly;
    NOT 2**32 (4,294,967,296), and NOT any other value."""


def _is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True


def assert_spec_q(q: int) -> None:
    """Pre-reg §3.1 / Brief 11 §2c: q must be exactly 4_294_977_961 = 2³² + 10665,
    prime, q ≡ 1 (mod 455). Fails loudly on 2³² (4_294_967_296), 2³²−1, or
    any other value."""
    if q != SPEC_Q:
        raise ModulusRefused(
            f"refusing q={q}: pre-reg §3.1 pins q=4_294_977_961 (= 2**32 + 10665). "
            f"'q=2**32' is shorthand only; the modulus is 2**32 + 10665, NOT 2**32. "
            f"Got delta = {q - SPEC_Q} from the pinned value."
        )
    # Belt-and-braces: the pinned value's prime / mod-455 properties.
    if not _is_prime(q):
        raise ModulusRefused(f"q={q} is not prime; the pinned modulus must be.")
    if q % 455 != 1:
        raise ModulusRefused(
            f"q={q} does not satisfy q ≡ 1 (mod 455); got q%455={q % 455}."
        )


# ---------------------------------------------------------------------------
# Pre-flight 3: −A_scalarᵀ sign-convention round-trip gate
# ---------------------------------------------------------------------------


def round_trip_check(q: int, k: int = 7, seed: int = 20260601) -> dict:
    """Verify the pre-reg §3.6 −A_scalarᵀ sign convention by exact round-trip:
    build a toy instance at (q, k), construct the primal basis, recover the
    integer coefficient vector z, and verify z·B = v_target = (e, s, 1) exactly.

    Works at q=911 (toy gate) and q=SPEC_Q (spec gate; uses allow_spec_params=True
    just for the round-trip — no BKZ run). Returns norms + a `pass` flag.
    """
    from op_2_58_2d_lattice_attack import (
        build_primal_lattice,
        build_scalar_lwe,
        gen_toy_instance,
        l2_norm,
        recover_lattice_coeffs,
        target_vector,
        vec_mat_mul,
    )

    inst = gen_toy_instance(seed=seed, q=q, k=k, allow_spec_params=(q == SPEC_Q))
    lwe = build_scalar_lwe(inst["A"], inst["s"], inst["e"], q)
    B = build_primal_lattice(lwe["A_scalar"], lwe["b_scalar"], q)
    z = recover_lattice_coeffs(
        lwe["A_scalar"], inst["s_scalar_signed"], inst["e_scalar_signed"],
        lwe["b_scalar"], q,
    )
    reconstructed = vec_mat_mul(z, B)
    v_target = target_vector(inst["e_scalar_signed"], inst["s_scalar_signed"])
    matches = (reconstructed == v_target)
    return {
        "q": q, "k": k, "n_eff": lwe["n_eff"], "N_lat": len(B),
        "v_target_norm": l2_norm(v_target),
        "reconstructed_matches_target": matches,
        "pass": bool(matches),
    }


# ---------------------------------------------------------------------------
# Pre-flight 4: PRODUCTION_RUN gate-enforcement (sys.modules lookup)
# ---------------------------------------------------------------------------


def assert_spec_gate_enforced() -> None:
    """Verify the spec-parameter gate of op_2_58_2d_lattice_attack actually
    catches spec-Q invocations. Per pre-reg §3.3.1, the repo's sys.path import
    pattern creates two SpecParamsRefused class objects (one per import path);
    a naive `isinstance` against the bare-imported class silently fails. This
    uses the sys.modules lookup pattern documented in
    `tools/test_op_2_58_2d_bkz_smoke.py`.

    Raises RuntimeError if the gate fails to refuse a spec-parameter call
    with allow_spec_params=False.
    """
    # Importing lattice_attack also registers it in sys.modules.
    from op_2_58_2d_lattice_attack import gen_toy_instance  # noqa: F401
    refused_cls = sys.modules["op_2_58_2d_lattice_attack"].SpecParamsRefused
    try:
        gen_toy_instance(q=SPEC_Q, k=4, allow_spec_params=False)
    except refused_cls:
        return  # gate enforced — pre-flight pass
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(
            f"PRODUCTION_RUN gate raised the wrong exception class "
            f"(expected SpecParamsRefused via sys.modules lookup; got {type(exc).__name__}). "
            f"This means the spec-parameter gate is NOT enforced via the test's "
            f"class-identity check; a naive isinstance would silently fail. "
            f"Fix the import pattern before flipping PRODUCTION_RUN."
        ) from exc
    raise RuntimeError(
        "PRODUCTION_RUN gate FAILED: gen_toy_instance(q=SPEC_Q, allow_spec_params=False) "
        "completed without raising. The pre-reg §3.1 spec-parameter gate is not "
        "enforcing. Do NOT flip PRODUCTION_RUN."
    )


# ---------------------------------------------------------------------------
# Aggregated pre-flight
# ---------------------------------------------------------------------------


def run_preflight(q: int = SPEC_Q, verbose: bool = True) -> dict:
    """Run all four Brief 11 §2 pre-flight gates. Each individual gate raises
    on failure; this aggregates the pass results so the orchestrator can log
    them as an audit-trail block before any spec dispatch.
    """
    results: dict[str, Any] = {}
    # 2a: float_type="ld" guard (constructive: try both correct and wrong).
    try:
        _assert_ld("ld")
    except FloatTypeRefused as exc:
        raise RuntimeError("ld guard rejected the pinned value") from exc
    refused = False
    try:
        _assert_ld("double")
    except FloatTypeRefused:
        refused = True
    if not refused:
        raise RuntimeError("ld guard FAILED to refuse float_type='double'")
    results["float_type_ld_guard"] = "PASS"
    if verbose:
        print("  [preflight 2a] float_type='ld' guard: PASS")
    # 2b: round-trip at toy q
    rt_toy = round_trip_check(q=911, k=7)
    if not rt_toy["pass"]:
        raise RuntimeError(f"toy round-trip FAILED: {rt_toy}")
    results["round_trip_q_toy"] = rt_toy
    if verbose:
        print(f"  [preflight 2b] −A^T round-trip at q=911 k=7: PASS "
              f"(N_lat={rt_toy['N_lat']}, ‖v_target‖={rt_toy['v_target_norm']:.2f})")
    # 2b: round-trip at spec q (small k to keep it fast)
    rt_spec = round_trip_check(q=SPEC_Q, k=4)
    if not rt_spec["pass"]:
        raise RuntimeError(f"spec round-trip FAILED: {rt_spec}")
    results["round_trip_q_spec"] = rt_spec
    if verbose:
        print(f"  [preflight 2b] −A^T round-trip at q=SPEC k=4: PASS "
              f"(N_lat={rt_spec['N_lat']}, ‖v_target‖={rt_spec['v_target_norm']:.2f})")
    # 2c: exact-q assertion
    assert_spec_q(q)
    results["exact_q_assertion"] = "PASS"
    if verbose:
        print(f"  [preflight 2c] exact-q assertion (q={q}): PASS")
    # 2d: PRODUCTION_RUN gate enforced
    assert_spec_gate_enforced()
    results["production_run_gate_enforced"] = "PASS"
    if verbose:
        print("  [preflight 2d] PRODUCTION_RUN gate (sys.modules lookup): PASS")
    return results


if __name__ == "__main__":
    print("OP-2.58.2d BKZ driver — Brief 11 §2 pre-flight gates")
    res = run_preflight()
    print("\nAll four pre-flight gates PASS.")
