"""
final_fits.py — GZ1 Phase 4c (REBUILD): probe sweep -> phase4_fits.json
Probes: midgaps of the REBUILT phase-3a gaps (eta=0.02) — never frequencies
chosen by proximity to any target — plus the original in-band controls
(omega = 20.0, 13.4, 5.0 at eta=0.1) and the eta-independence check at Gap A
midgap (eta=0.05). In-band: Bloch retention t = 1 (lossless periodic medium);
the fits there document the ABSENCE of exponential decay. Field-by-field deltas
vs originals/phase4_fits.json are printed for the rebuild report.
"""
import json
import numpy as np
from solve_one import solve


def main():
    with open("phase3a_line.json") as f:
        gaps = json.load(f)["gaps"]
    (Alo, Ahi), (A2lo, A2hi), (Blo, Bhi) = gaps[0], gaps[1], gaps[2]
    probes = [
        ("gapA_mid", round((Alo + Ahi) / 2, 2), 0.02),
        ("gapA2_mid", round((A2lo + A2hi) / 2, 2), 0.02),
        ("gapB_mid", round((Blo + Bhi) / 2, 2), 0.02),
        ("band_20", 20.0, 0.1),
        ("band_134", 13.4, 0.1),
        ("band_50", 5.0, 0.1),
    ]
    fits = {}
    for tag, w, eta in probes:
        fits[tag] = solve(tag, w, eta)
    with open("phase4_fits.json", "w") as f:
        json.dump(fits, f, indent=1)

    # eta-independence check at Gap A midgap (reported separately, as original)
    eta05 = solve("gapA_eta05", probes[0][1], 0.05)
    kA, kA5 = fits["gapA_mid"]["kappa_fit"], eta05["kappa_fit"]
    print(f"\neta-independence at Gap A: kappa(0.02)={kA}  kappa(0.05)={kA5}"
          f"  shift={100*abs(kA5-kA)/kA:.2f}%  (originals: 0.8061 vs 0.8087)")

    # per-period products (2-row Bloch beats: A2 + in-band)
    for tag in ["gapA2_mid", "band_134", "band_20"]:
        r = fits[tag]["clean_ratios"]
        prods = [round(r[i] * r[i + 1], 4) for i in range(0, len(r) - 1, 2)]
        print(f"per-period products {tag}: {prods}")

    # field-by-field comparison with the surviving original
    try:
        with open("originals/phase4_fits.json") as f:
            orig = json.load(f)
        print("\nFIELD-BY-FIELD vs ORIGINAL (rebuilt | original | delta):")
        for tag in fits:
            if tag not in orig:
                continue
            for key in ["omega", "kappa_fit", "t_fit", "t_ratio_median", "fit_r2",
                        "wrap_min_row"]:
                a, b = fits[tag][key], orig[tag][key]
                d = (a - b) if isinstance(a, (int, float)) else "-"
                print(f"  {tag:10s} {key:15s} {a!s:>9} | {b!s:>9} | "
                      f"{d if isinstance(d, str) else round(d, 4)}")
    except FileNotFoundError:
        print("originals/phase4_fits.json not present — deltas skipped")


if __name__ == "__main__":
    main()
