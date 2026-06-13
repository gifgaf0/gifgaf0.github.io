"""
comparison_step.py — GZ1 final step (REBUILD). RUN LAST.
This is the ONLY file in the instrument that loads, computes, or compares to
the target constant (Eddington isolation, prereg + report §0). It reads the
already-written phase4_fits.json / phase2.json / phase3a_line.json and maps the
t-landscape onto the pre-registered outcome arms.
"""
import json
import math


def main():
    zeta = 1.0 - math.pi / math.sqrt(12.0)          # the ONLY occurrence
    lo, hi = zeta - 0.005, zeta + 0.005             # PASS window [0.0881, 0.0981]

    with open("phase4_fits.json") as f:
        fits = json.load(f)
    with open("phase2.json") as f:
        d_row = json.load(f)["d_row"]
    with open("phase3a_line.json") as f:
        ph3a = json.load(f)

    print("=" * 72)
    print("G-zeta1 COMPARISON STEP (run last; target enters only here)")
    print("=" * 72)
    print(f"target = {zeta:.7f}   PASS window [{lo:.4f}, {hi:.4f}]   "
          f"d_row = {d_row}")
    print()

    gap_tags = [t for t in fits if t.startswith("gap")]
    band_tags = [t for t in fits if t.startswith("band")]
    tmin, tmin_tag = None, None
    print("t landscape (per-layer amplitude factor t = exp(-kappa*d_row)):")
    for tag in gap_tags:
        t = math.exp(-fits[tag]["kappa_fit"] * d_row)
        inwin = lo <= t <= hi
        print(f"  {tag:10s} omega={fits[tag]['omega']:>6}  t = {t:.4f}"
              f"   {'IN WINDOW' if inwin else 'outside window'}"
              f"   (x{t/zeta:.1f} target)")
        if tmin is None or t < tmin:
            tmin, tmin_tag = t, tag
    for tag in band_tags:
        print(f"  {tag:10s} omega={fits[tag]['omega']:>6}  t -> 1 "
              f"(in-band Bloch retention; lossless periodic medium)")
    print()

    acoustic_max = ph3a["acoustic_max"]
    goldstones = ph3a["sanity"]["gate_b"]
    print(f"quasi-static density channel: gapless acoustic branch 0 -> "
          f"{acoustic_max} ({'3 Goldstone zeros' if goldstones else 'check failed'})"
          f" => t -> 1 in the omega->0 sector")
    print()

    any_pass = any(lo <= math.exp(-fits[t]["kappa_fit"] * d_row) <= hi
                   for t in gap_tags)
    print("VERDICT (pre-registered outcome mapping):")
    if goldstones and acoustic_max > 5.0:
        print("  PRIMARY  — DEGENERATE: the registered channel (quasi-static")
        print("  density response) is gapless and transparent (t -> 1); the")
        print("  per-layer-attenuation ontology is not realised by this crystal.")
    if not any_pass:
        print(f"  ALTERNATIVE — INFORMATIVE-FAIL: minimum t over all stop bands =")
        print(f"  {tmin:.4f} at {tmin_tag} — a factor {tmin/zeta:.1f}x above the")
        print(f"  target; no frequency in the computed band structure yields t in")
        print(f"  the PASS window.")
    else:
        print("  A gap t fell inside the PASS window — would be reported as")
        print("  conditional on an (out-of-gate) frequency-selection mechanism.")
    print()
    print("expected reproduction (report §5/§6): DEGENERATE arm; min t ~ 0.36 at")
    print("Gap A (~3.9x target); nothing approaches the window.")


if __name__ == "__main__":
    main()
