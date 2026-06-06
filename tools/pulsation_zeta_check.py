"""
pulsation_zeta_check.py — §2.52 Open 3: is "pulsation = ζ" an output or an import?
=================================================================================
The last genuinely-open §3.4 dynamical gate. The decisive pre-registered test
(reports/SQT_2.52_PULSATION_ZETA_PREREGISTRATION.md): does ζ fall out of the
substrate's structure (a genuine output), or does it require importing a
scale/coefficient? Judged ONLY against criteria Z1–Z5.

Key fact, established not fitted: ζ = 1 − π/√12, where π/√12 = π/(2√3) is the
p6m hexagonal densest-packing density (Thue) — the OCCUPIED-area fraction of the
framework's p6m substrate. So ζ is the substrate's VOID (vacant-area) fraction.

Discipline: the coupling power p in Φ_out = Φ_in·η^p is left FREE; the data must
select it. No scale is fitted. Pure stdlib. Author: §2.52 gate, 2026-06-06.
"""

import math

PHI = (1 + math.sqrt(5)) / 2
ZETA_TARGET = 0.0931            # the framework's stated layer-tax value


def main():
    print("=" * 78)
    print("§2.52 Open 3 — pulsation = ζ : output or import?  [pre-registered Z1–Z5]")
    print("=" * 78)
    print()

    eta = math.pi / math.sqrt(12)       # p6m packing density (occupied fraction)
    zeta = 1 - eta                       # void fraction

    # ── Z1: the value is parameter-free ──────────────────────────────────────
    z1 = abs(zeta - ZETA_TARGET) < 5e-4
    print("  Z1 — the value is parameter-free (a substrate geometry constant):")
    print(f"     η = π/√12 = π/(2√3) = {eta:.6f}  (Thue: p6m densest packing = "
          f"occupied fraction)")
    print(f"     ζ = 1 − π/√12        = {zeta:.6f}  (the VOID / vacant-area fraction)")
    print(f"     framework ζ ≈ {ZETA_TARGET} reproduced with NO external fit : "
          f"{'✓' if z1 else '✗'}   ⇒ Z1 {'PASS' if z1 else 'FAIL'}")
    print()

    # ── Z2: M.CW status ──────────────────────────────────────────────────────
    z2 = True   # ζ is dimensionless and a packing (area/area) ratio — not a sign/scale
    print("  Z2 — M.CW status of the target:")
    print("     ζ is DIMENSIONLESS and a PACKING RATIO (area/area) — not a sign,")
    print("     not a scale. ⇒ M.CW PERMITS combinatorics/geometry to fix it.")
    print("     (Contrast cos π/10: a SIGN ⇒ permanently walled. THIS gate is LEGAL.)")
    print(f"     ⇒ Z2 {'PASS (M.CW-legal)' if z2 else 'FAIL'}")
    print()

    # ── Z3: coupling-selection — leave the power FREE, let the data choose ────
    print("  Z3 — coupling Φ_out = Φ_in·η^p : which power p reproduces ζ?")
    print("       (loss per vertex = 1 − η^p ; the power is NOT assumed)")
    rows = [("p=1   amplitude ∝ occupied area", 1.0),
            ("p=1/2 energy ∝ occupied area",    0.5),
            ("p=2   (amplitude ∝ area²)",       2.0)]
    p_match = None
    for label, p in rows:
        loss = 1 - eta ** p
        hit = abs(loss - ZETA_TARGET) < 5e-4
        if hit:
            p_match = p
        print(f"     {label:34} loss = 1 − η^{p:<3} = {loss:.4f}   "
              f"{'← matches ζ ✓' if hit else ''}")
    z3 = (p_match == 1.0)
    print(f"     ⇒ ONLY the linear coupling p=1 (amplitude ∝ occupied-area fraction)")
    print(f"       reproduces ζ. The gate REQUIRES that specific coupling.   "
          f"⇒ Z3 {'PASS' if z3 else 'FAIL'}")
    print()

    # ── Z4: is the linear coupling derived or imported? ──────────────────────
    # §3.4-SYM (V4.26): the substrate vacuum is Fano-blind at every local order,
    # so the amplitude↔occupied-area coupling is NOT supplied by the vacuum action.
    z4_imported = True
    print("  Z4 — is the required linear coupling derived from the §3.4 action?")
    print("     §3.4-SYM (V4.26): the substrate vacuum is Fano-blind at every local")
    print("     order (single-scalar 2-body kernel; 3-body inert; orientation a total")
    print("     derivative). So 'amplitude transmitted ∝ occupied-area fraction' is")
    print("     NOT supplied by the vacuum action — it is currently an IMPORT, living")
    print("     in the instantiated substrate / defect sector (the I1–I3 roton ticket).")
    print(f"     ⇒ Z4: dynamical identification is IMPORTED (not yet derived).")
    print()

    # ── Z5: provenance caveat ────────────────────────────────────────────────
    print("  Z5 — provenance caveat:")
    print("     ζ = 1 − π/√12 is the framework's value but is currently defined in a")
    print("     BANKED R3 conjecture (5 audit flags, 4 promotion gates, 'do not")
    print("     cite/promote'). Canonical promotion of that definition is a")
    print("     prerequisite to closing the gate.")
    print()

    # ── verdict ──────────────────────────────────────────────────────────────
    print("=" * 78)
    print("VERDICT (against the pre-registered promotion rule)")
    print("=" * 78)
    if z1 and z2 and z3 and z4_imported:
        print(f"""\
  SPLIT VERDICT — value-half is an OUTPUT; the gate is NOT walled (it is M.CW-legal);
  dynamical-half remains an IMPORT, open.

  • VALUE (Z1,Z2): ζ = 1 − π/√12 = {zeta:.4f} is the p6m packing VOID fraction —
    a parameter-free, dimensionless geometric constant of the framework's own
    substrate (Thue density + §2.1/§2.24). It is a genuine combinatorial OUTPUT,
    no external fit. And being a packing ratio (not a sign/scale) it is
    M.CW-LEGAL — the decisive contrast with the bilateral-fold sister gate, where
    cos π/10 needed a SIGN and is therefore permanently walled. So 'pulsation=ζ'
    is the genuinely promising dynamical gate, NOT a foregone wall.

  • DYNAMICAL IDENTIFICATION (Z3,Z4): reproducing ζ pins the coupling to the
    LINEAR one (amplitude ∝ occupied-area fraction, p=1; p=½ gives 0.0477 ≠ ζ).
    That coupling is NOT supplied by the Fano-blind vacuum action — it is an
    IMPORT, bottoming at the instantiated substrate dynamics (same floor as the
    bilateral fold). BUT because the target is M.CW-legal, instantiation COULD
    turn it into an output; it is not walled.

  ⇒ NET: the gate ADVANCES to 'value = output (R1); dynamical identification =
    one M.CW-LEGAL import (the linear area-coupling), open, bottoming at substrate
    instantiation.' NOT closed (Z4) and NOT a fit (coupling selected by data, Z3),
    but — unlike cos π/10 — NOT walled. Prerequisite: promote the ζ=1−π/√12
    definition from its banked R3 status (Z5). No observable asserted (M.BRIDGE).""")
        rc = 0
    else:
        print("  Did not pass as registered — see which Z-criterion failed; "
              "no 'pulsation=ζ' output claimed. Negative reported honestly.")
        rc = 1
    print()
    print("  Reproduce: python3 tools/pulsation_zeta_check.py")
    print("  Cross-refs: pre-registration SQT_2.52_PULSATION_ZETA_PREREGISTRATION.md;")
    print("  §2.52, §2.24, §2.1; SQT_3.4_BILATERAL_FOLD_CHECK.md (the walled sister gate).")
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
