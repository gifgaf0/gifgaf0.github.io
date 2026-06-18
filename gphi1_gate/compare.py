"""
G-Phi1 Step 6 -- EDDINGTON STEP, run last. This is the ONLY file in the gate
that contains the comparison constant Phi = 2*pi - phi^2/(8*pi^2) (phi = golden
ratio). It reads the frozen measurements and applies the pre-registered arm map.
"""
import json
import numpy as np

PHI_GOLDEN = (1.0 + np.sqrt(5.0)) / 2.0
PHI = 2.0 * np.pi - PHI_GOLDEN**2 / (8.0 * np.pi**2)     # 6.25003
RATE_TARGET = 1.0 / PHI                                   # 0.160
RATE_TANH = 0.227                                         # pre-registered analytic


def main():
    with open("gphi1_measurements.json") as f:
        m = json.load(f)
    rate = m["step5"]["rate_actual"]
    boundary = m["step5"]["rate_is_window_boundary_artifact"]
    pc = m["premise_check"]

    gap_to_tanh = abs(rate - RATE_TANH) / RATE_TANH
    gap_to_target = abs(rate - RATE_TARGET) / RATE_TARGET
    fraction_closed = (RATE_TANH - rate) / (RATE_TANH - RATE_TARGET)

    if gap_to_target < 0.05:
        arm = "A"
    elif gap_to_tanh < 0.10:
        arm = "B"
    else:
        arm = "C"

    premise_falsified = not pc["interior_inflection_in_window"]
    # auditor decision (2026-06-16): a falsified premise overrides the mechanical
    # arm -- the registered inflection-rate probe is ill-posed for this state.
    verdict = "INCONCLUSIVE (premise falsified)" if premise_falsified \
        else f"ARM {arm}"

    print("=" * 70)
    print("G-Phi1 COMPARISON STEP (Eddington; Phi enters only here)")
    print("=" * 70)
    print(f"Phi = 2*pi - phi^2/(8*pi^2) = {PHI:.5f}   1/Phi = {RATE_TARGET:.5f}")
    print(f"rate_tanh (registered)      = {RATE_TANH}")
    print(f"rate_actual (Step 5)        = {rate:.5f}"
          f"   [window-boundary artifact = {boundary}]")
    print()
    print(f"  gap_to_tanh    = {gap_to_tanh:.4f}")
    print(f"  gap_to_target  = {gap_to_target:.4f}")
    print(f"  fraction_closed= {fraction_closed:.4f}")
    print()
    print(f"mechanical arm (pre-registered map, Step 6): ARM {arm}  [SUPERSEDED]")
    print(f"RECORDED VERDICT: {verdict}")
    print()
    print("-" * 70)
    print("PREMISE CHECK (decisive -- read before trusting the mechanical arm):")
    print(f"  interior inflection inside registered 0..3xi window? "
          f"{pc['interior_inflection_in_window']}")
    print(f"  rho/rho0 at tanh inflection radius 0.931xi = "
          f"{pc['rho_at_tanh_radius_0p931xi']:.4f}  (tanh: 0.3333)")
    print(f"  TRUE interior inflection at {pc['true_inflection_r_over_xi']:.2f} xi,"
          f" rho/rho0 = {pc['true_inflection_rho_over_rho0']:.3f}  (>1)")
    print("  => the registered tanh-vortex premise (heal to rho0, inflection")
    print("     near 0.931xi at rho/rho0~1/3) is FALSIFIED by the ground state;")
    print("     rate_actual is the density at the 3xi cutoff, not an inflection.")

    out = dict(Phi=PHI, rate_target=RATE_TARGET, rate_tanh=RATE_TANH,
               rate_actual=rate, gap_to_tanh=gap_to_tanh,
               gap_to_target=gap_to_target, fraction_closed=fraction_closed,
               mechanical_arm=arm, recorded_verdict=verdict,
               rate_is_window_boundary_artifact=boundary,
               premise_falsified=premise_falsified)
    with open("gphi1_verdict.json", "w") as f:
        json.dump(out, f, indent=1)
    print("\ngphi1_verdict.json written")


if __name__ == "__main__":
    main()
