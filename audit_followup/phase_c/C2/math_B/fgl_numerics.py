#!/usr/bin/env python3
"""
fgl_numerics.py -- C2 batch, math_B leg, items (f), (g), (l).  mpmath at 50 significant digits.

(f) arctan(1/sqrt 2) in radians and degrees; identify 54.74 deg.
(g) ln(4 pi)/ln 7 (base-independent) versus the ledger's 1.286.
(l) 84/arctan(1/sqrt 2) (radians) and 240/sqrt 3 against CODATA alpha^-1 = 137.035999177.
"""
from mpmath import mp, mpf, atan, acos, asin, sqrt, pi, log, log10, degrees, nstr

mp.dps = 50


def pct(x):
    return nstr(100 * x, 6) + " %"


def main():
    print("=" * 78)
    print("ITEMS (f), (g), (l) -- numerics (math_B leg, mpmath 50 digits)")
    print("=" * 78)

    # ---------------- (f)
    a = atan(1 / sqrt(2))
    print("\n(f) arctan(1/sqrt 2)")
    print("   arctan(1/sqrt2)            =", nstr(a, 20), "rad =", nstr(degrees(a), 20), "deg")
    print("   arcsin(1/sqrt3)            =", nstr(degrees(asin(1 / sqrt(3))), 20), "deg  (same angle)")
    print("   arctan(sqrt2)              =", nstr(degrees(atan(sqrt(2))), 20), "deg")
    print("   arccos(1/sqrt3)            =", nstr(degrees(acos(1 / sqrt(3))), 20), "deg  (the 'magic angle')")
    print("   90 deg - arctan(1/sqrt2)   =", nstr(90 - degrees(a), 20), "deg")
    print("   2*arctan(1/sqrt2)          =", nstr(degrees(2 * a), 20), "deg = arccos(1/3) =",
          nstr(degrees(acos(mpf(1) / 3)), 20))
    print("   ledger value 54.74 deg: |54.74 - arctan(sqrt2) in deg| =", nstr(abs(mpf('54.74') - degrees(atan(sqrt(2)))), 6))
    print("   consistency with the ledger's alpha formula: 84/arctan(1/sqrt2) [rad] =", nstr(84 / a, 12),
          "; 84/(54.7356 deg in rad) =", nstr(84 / atan(sqrt(2)), 12))

    # ---------------- (g)
    r = log(4 * pi) / log(7)
    print("\n(g) log(4 pi)/log 7")
    print("   ln(4 pi) =", nstr(log(4 * pi), 20), "; ln 7 =", nstr(log(7), 20))
    print("   ln(4 pi)/ln 7       =", nstr(r, 20))
    print("   log10(4 pi)/log10 7 =", nstr(log10(4 * pi) / log10(7), 20), " (base-independent)")
    print("   ledger 1.286: relative deviation (1.286 - r)/r =", pct((mpf('1.286') - r) / r))
    print("   7^1.286 =", nstr(mpf(7) ** mpf('1.286'), 10), " vs 4 pi =", nstr(4 * pi, 10))
    print("   for reference: 9/7 =", nstr(mpf(9) / 7, 10))

    # ---------------- (l)
    c = mpf('137.035999177')  # CODATA 2022 alpha^-1 (value specified in the task)
    x1 = 84 / a
    x2 = 240 / sqrt(3)
    print("\n(l) alpha^-1 leading values vs CODATA alpha^-1 =", nstr(c, 12))
    for name, x in (("84/arctan(1/sqrt2)", x1), ("240/sqrt3", x2)):
        print(f"   {name:20s} = {nstr(x, 15)}")
        print(f"      x - CODATA             = {nstr(x - c, 10)}")
        print(f"      (x - CODATA)/CODATA    = {pct((x - c) / c)}")
        print(f"      (x - CODATA)/x         = {pct((x - c) / x)}")
        print(f"      ln(x/CODATA)           = {pct(log(x / c))}")
    print("   0.003 % of CODATA =", nstr(c * mpf('0.00003'), 6), "(absolute half-width of a 0.003% match)")
    print("   correction needed from 84/arctan(1/sqrt2): CODATA - x =", nstr(c - x1, 10),
          "(the subtracted 'correction terms' must total", nstr(x1 - c, 10), ")")
    print("   correction needed from 240/sqrt3:        CODATA - x =", nstr(c - x2, 10))
    print("   ledger '1.099% gap between 240/sqrt3 and 137.036' vs computed:",
          pct((x2 - c) / c), "(rel. CODATA) /", pct((x2 - c) / x2), "(rel. 240/sqrt3)")
    print("   with 137.036 exactly:", pct((x2 - 137.036) / mpf('137.036')))
    print("   sides of CODATA: 84/arctan(1/sqrt2) is", "below" if x1 < c else "above",
          "; 240/sqrt3 is", "below" if x2 < c else "above")


if __name__ == "__main__":
    main()
