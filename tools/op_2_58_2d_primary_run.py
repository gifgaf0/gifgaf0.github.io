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

    Returns {ok, reason, prereg_path, freeze_date, freeze_signature}.
    """
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
        }
    with open(path, encoding="utf-8") as f:
        text = f.read()
    # Extract §6 freeze date and signature; reject [pending].
    date_m = re.search(r"freeze\s*date[:\s]*([0-9]{4}-[0-9]{2}-[0-9]{2}|\[pending[^\]]*\])",
                       text, re.IGNORECASE)
    sig_m = re.search(r"freeze\s*signature[:\s]*(\[pending[^\]]*\]|\S.*)", text, re.IGNORECASE)
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
        }
    return {
        "ok": True, "reason": "freeze verified",
        "prereg_path": path, "freeze_date": date, "freeze_signature": sig,
    }


def check_construction_available() -> dict:
    """Secondary precondition (brief §3.3 halt conditions): is there an actual
    §2.58.B spec instance to attack, and is basis (b) implemented?"""
    from op_2_58_2d_lattice_attack import build_fano_projected_lattice

    blockers = []
    # Basis (b): Fano-projected lattice.
    try:
        build_fano_projected_lattice()
        basis_b_ready = True
    except NotImplementedError as exc:
        basis_b_ready = False
        blockers.append(f"basis (b) Fano-projected lattice is unimplemented: {exc}")
    except Exception as exc:  # noqa: BLE001
        basis_b_ready = False
        blockers.append(f"basis (b) raised unexpectedly: {exc!r}")
    # §2.58.B construction: there is no spec-parameter §2.58.B instance generator
    # in the repo; gen_toy_instance produces generic synthetic LWE, not §2.58.B.
    blockers.append(
        "no §2.58.B spec-parameter construction artifact in repo: "
        "gen_toy_instance produces generic synthetic LWE, not the §2.58.B "
        "Fano-line-structured instance the primary run must attack."
    )
    return {"basis_b_ready": basis_b_ready, "blockers": blockers}


def build_job_matrix() -> list[dict]:
    """The frozen 42-run matrix (brief §3.1.3). Data only — no execution."""
    return [
        {"beta": b, "sample": s, "basis": x}
        for b, s, x in product(BETAS, SAMPLES, BASES)
    ]


def _run_one(job: dict, freeze: dict) -> dict:
    """Execute ONE spec-parameter BKZ run. The sole gate-bypass site.

    Guarded so it is unreachable unless freeze is verified AND PRODUCTION_RUN.
    Pre-freeze this raises before constructing anything at spec scale.
    """
    if not (freeze.get("ok") and PRODUCTION_RUN):
        raise RuntimeError(
            "refusing spec-parameter run: requires verified freeze AND "
            "PRODUCTION_RUN=True (the brief §4.1 audit anchor). This guard "
            "must never be bypassed pre-freeze."
        )
    # Intentionally not implemented further: the primary run is 30-day wall-clock
    # work (brief §3.3) and depends on the frozen pre-reg + §2.58.B construction,
    # neither of which is available. Reaching here pre-freeze is a logic error.
    raise NotImplementedError(
        "spec-parameter run body is not invoked: preconditions (frozen pre-reg, "
        "§2.58.B construction, basis (b)) are unmet. See op_2_58_2d_closure status."
    )


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
    print(f"\n[§3.1 job matrix] {len(jobs)} runs queued (NOT dispatched here).")
    print("Dispatch is 30-day wall-clock work (brief §3.3); the session monitors.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
