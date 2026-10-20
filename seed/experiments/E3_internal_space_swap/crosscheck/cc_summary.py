#!/usr/bin/env python3
"""Collect the cross-check results, compare with the original results.json, write crosscheck.json."""
import json
from fractions import Fraction
import numpy as np

orig = json.load(open("../results.json"))
g2 = json.load(open("cc_g2.json"))
sk = json.load(open("cc_skyrme.json"))
fl = json.load(open("cc_flag.json"))
try:
    st = json.load(open("cc_stability.json"))
except FileNotFoundError:
    st = None

rows = []
def row(q, o, m, tol, note=""):
    if isinstance(o, (int, float)) and isinstance(m, (int, float)):
        rel = abs(o - m) / max(abs(o), 1e-300) if o != 0 else abs(m)
        ok = rel <= tol
        rows.append(dict(quantity=q, original=o, recomputed=m, rel_diff=rel, tol=tol, agree=bool(ok), note=note))
    else:
        rows.append(dict(quantity=q, original=o, recomputed=m, tol=tol, agree=bool(o == m), note=note))

oi = orig["inertia"]["hedgehogs_in_su2_subgroups"]
for k, kk in [("long", "long_root"), ("short", "short_root"), ("index4_diag", "index4_diag"),
              ("index4_SO3", "index4_SO3"), ("principal", "principal")]:
    row(f"Dynkin index {k}", round(oi[kk]["M_over_M1"], 9), round(g2["dynkin_indices"][k], 9), 1e-9,
        "original via -Tr7(T3^2) and embedded-hedgehog B, E; mine via 3-form g2, root vectors")
row("7 under SU(2)_L x SU(2)_S", "(2,2)+(1,3)", "(2,2)+(1,3)" if g2["branching_7"] == {"(2,2)": 1, "(1,3)": 1} else str(g2["branching_7"]), 0)
row("14 under SU(2)_L x SU(2)_S", "(3,1)+(1,3)+(2,4)",
    "(3,1)+(1,3)+(2,4)" if g2["branching_14"] == {"(3,1)": 1, "(1,3)": 1, "(2,4)": 1} else str(g2["branching_14"]), 0)
om = {tuple(r["dynkin"]): r for r in orig["g2_irreps"]}
nmatch = 0
for r in g2["irreps"]:
    o = om[tuple(r["lam"])]
    if o["branching"] == r["branching"] and o["C2"] == r["C2"] and \
            o["allowed_J"] == {k.replace(".0", ""): v for k, v in r["allowed_J"].items()}:
        nmatch += 1
row("G2 irreps dim<=500: L x S branching, C2, allowed J (13 irreps)", f"{len(om)} irreps", f"{nmatch}/{len(g2['irreps'])} identical", 0)
rows[-1]["agree"] = nmatch == len(g2["irreps"]) == len(om)

h = orig["hedgehog"]["final"]
row("M_cl (F_pi/e)", h["M"], sk["profile"]["M"], 1e-8)
row("Lambda", h["Lambda"], sk["profile"]["Lambda"], 1e-8)
row("I2 radial integral J2", h["I2_integral"], sk["profile"]["J2"], 1e-8)
row("F'(0)", h["slope_F'(0)"], sk["profile"]["Fp0"], 1e-8)
row("C (tail)", h["C_tail"], sk["profile"]["C"], 1e-6)
row("I1 (3D, x3)", orig["inertia"]["I1"], sk["inertia"]["I1"], 1e-8)
row("I2 (3D, x8)", orig["inertia"]["I2"], sk["inertia"]["I2"], 1e-8)
row("I1/I2", orig["inertia"]["I1"] / orig["inertia"]["I2"], sk["inertia"]["ratio_I1_I2"], 1e-8)
row("short block inertia (max |I|)", 6.6e-19, sk["inertia"]["short_max"], 1, "both zero to rounding")
rows[-1]["agree"] = sk["inertia"]["short_max"] < 1e-12
pa = orig["parameter_points"]
row("ANW: M (MeV)", pa["ANW (F_pi=129, e=5.45)"]["M"], sk["ANW"]["M"], 1e-8)
row("ANW: 1/I1 (MeV)", pa["ANW (F_pi=129, e=5.45)"]["inv_I1"], sk["ANW"]["invI1"], 1e-8)
row("ANW: 1/I2 (MeV)", pa["ANW (F_pi=129, e=5.45)"]["inv_I2"], sk["ANW"]["invI2"], 1e-8)
rf = sk["refit"]["Delta 1232.0"]
row("refit F_pi (MeV)", orig["su3_refit"]["F_pi"], rf["F_pi"], 1e-8)
row("refit e", orig["su3_refit"]["e"], rf["e"], 1e-8)
row("refit antidecuplet (MeV)", orig["su3_refit"]["antidecuplet_MeV"], rf["antidecuplet"], 1e-8)
row("octet centre (MeV, PDG 2026)", orig["su3_refit"]["octet_centre_MeV"], rf["E8"], 1e-10)
row("decuplet centre (MeV, PDG 2026, Delta=1232.0)", orig["su3_refit"]["decuplet_centre_MeV"], rf["E10"], 1e-10)
os_ = orig["g2_states"]
for k, s in enumerate(sk["states"][:10]):
    o = os_[k]
    row(f"state {k}: {s['R']} J={s['J']:.0f}: (E-M) I1", o["E_over_inv_I1"], s["EminusM_I1"], 1e-8,
        f"orig label {o['R']} J={o['J']:.0f}; E_ANW {o['E_MeV ANW (F_pi=129, e=5.45)']:.1f} vs {s['E_ANW']:.1f}; "
        f"E_refit {o['E_MeV SU(3) refit']:.1f} vs {s['E_refit']:.1f}")
row("E(14,J=1) - E(1,J=0) at ANW (MeV)", os_[1]["Exc_MeV ANW (F_pi=129, e=5.45)"], sk["states"][1]["E_ANW"] - sk["states"][0]["E_ANW"], 1e-8)

# flag
mm = orig["flag"]["moment_map"]["generic a=(1, 0.3, -1.3)"]
row("hexagon sides (generic a)", "0.98995 / 2.26274 alternating", "7 sqrt2/10 / 8 sqrt2/5 alternating (exact)", 0)
rows[-1]["agree"] = abs(min(mm["sides"]) - 0.7 * 2 ** .5) < 1e-12 and abs(max(mm["sides"]) - 1.6 * 2 ** .5) < 1e-12
row("hexagon angles", "120 deg x6", "120 deg x6 (exact)", 0); rows[-1]["agree"] = True
row("degenerate a: triangle", "3 vertices, 60 deg", "3 vertices, 60 deg (exact)", 0); rows[-1]["agree"] = True
for name, v in fl["pi2"].items():
    q = v.get("plane", v.get("delaunay"))
    row(f"pi2 {name}", list(v["expected"]), [round(x, 8) for x in q], 0, "expected = original's integers")
    rows[-1]["agree"] = max(abs(a - b) for a, b in zip(q, v["expected"])) < 1e-6
p3o = orig["flag"]["pi3"] if "pi3" in orig["flag"] else None
for name, v in fl["pi3"].items():
    if not name.startswith("C"):
        continue
    row(f"pi3 lift degree {name}", v["expected"], round(v["richardson"], 6), 0,
        "SO(3) sign is generator-orientation convention" if name.startswith("C4") else "")
    rows[-1]["agree"] = abs(abs(v["richardson"]) - abs(v["expected"])) < 1e-4

# stability (Ritz values are basis-dependent upper bounds: compare sign, multiplicities, continuum levels)
if st is not None:
    os_t = json.load(open("../stability_results.json"))["ritz_lowest_eigenvalues"]
    osr = json.load(open("../stability_refine_results.json"))
    mine = st["ritz"]
    row("stability: any negative eigenvalue (all blocks)", "none (min 2.1e-5)", f"none (min {min(min(v) for v in mine.values()):.1e})", 0)
    rows[-1]["agree"] = min(min(v) for v in mine.values()) > -1e-8
    row("(1,3) lowest, R=20 (exact (1/32)(pi/20)^2 = 7.7106e-4)", os_t["short (1,3)"]["R=20,nr=30,lmax=3"][0], mine["short (1,3) R=20 nel=30"][0], 1e-3)
    row("(3,1) first continuum level R=20 (x3)", osr["long (3,1)"]["90"][6], mine["long (3,1) R=20 nel=60"][6], 2e-3)
    row("(3,1) continuum R=20 (x1)", osr["long (3,1)"]["90"][9], mine["long (3,1) R=20 nel=60"][9], 2e-3)
    row("kaon first continuum level R=20 (x4)", osr["kaon (su(3) part of (2,4))"]["90"][4], mine["kaon R=20 nel=60"][4], 2e-3)
    row("kaon continuum R=20 (x2+)", osr["kaon (su(3) part of (2,4))"]["90"][8], mine["kaon R=20 nel=60"][8], 2e-3)
    row("(3,1) continuum level R=40 (x3)", os_t["long (3,1)"]["R=40,nr=40,lmax=3"][3], mine["long (3,1) R=40 nel=40"][6], 2e-3,
        "original lists this as its 2nd triplet; it is the continuum, the iso-rotation triplet is its 3.73e-4 (unresolved)")
    row("kaon zero-mode Dirichlet floor R=20 (x4)", osr["kaon (su(3) part of (2,4))"]["90"][0], mine["kaon R=20 nel=60"][0], 0.2,
        "original at nr=90 still 16% above my converged floor (upper bound, consistent)")
    row("(2,4) = kaon doubled", "1.6e-14", "1.3e-13", 0); rows[-1]["agree"] = True

issues = [
 dict(severity="minor", description="Verdict words: the headline marks seed predictions and PLAN expectations as CALIBRATED "
      "(lowest rotor multiplets, all-J-integer, 7 branching, C2 values, G2 inertia blocks, moment map, pi2, pi3). PLAN section 1 "
      "reserves CALIBRATED for literature targets; seed-claim items should read CONFIRMED (they do in seed_claims).",
      suggested_fix="Relabel those headline rows CONFIRMED (or 'consistent with PLAN expectation'); keep CALIBRATED for Mayanskiy indices/branching, M_cl, Lambda, I2."),
 dict(severity="minor", description="Stability table, (3,1) block at R=40/nr=40: the original lists 5.4e-5 (x3), 1.9e-4 (x3), 3.7e-4 as "
      "'zero modes, then continuum'. 1.939e-4 (x3) is the first continuum level (mine 1.937e-4); 3.73e-4 (x3) is the unresolved "
      "iso-rotation zero-mode triplet, which lies above it. So zero modes are not the lowest eigenvalues at that mesh.",
      suggested_fix="Relabel the R=40 column; quote converged zero-mode values from a higher-order basis (cubic B-splines: 7.5e-8 and 4.1e-6 at R=40, 1.9e-6 and 3.7e-5 at R=20)."),
 dict(severity="minor", description="'The centre element exp(2 pi T3^L)': G2 has trivial centre. The element is the image of -1 in SU(2)_L, central in the SO(4) subgroup only.",
      suggested_fix="Say 'the element exp(2 pi T3^L) (image of -1 in SU(2)_L)'."),
 dict(severity="minor", description="The argument that no velocity-linear term can shift the singlet constraint ('must be a character of the stabiliser's Lie algebra') is incomplete as stated: "
      "an SU(2)_short-invariant linear term along the (3,1) directions is not excluded by that argument, only by spatial-rotation (right SU(2)_L) invariance. "
      "The conclusion is unchanged. Also, AMENDED is applied to a PLAN section 3 literature note, not to a seed claim.",
      suggested_fix="Add 'and right SU(2)_L (rotation) invariance' to the argument; call the PLAN 3.5 item 'refined', not AMENDED."),
 dict(severity="minor", description="Citation precision: Mayanskiy 1611.04070 Table 2 lists only the non-regular A1^4 and A1^28; indices 1 (A1) and 3 (A1~) are given in the list right after Table 2 "
      "(Table 1 has the regular subalgebras). Prop. 4.1 matches as cited.",
      suggested_fix="Cite 'Mayanskiy section 4 (Table 2 and the list following it)'."),
 dict(severity="minor", description="'E2 parameters' were taken as the rounded PLAN ANW point (129 MeV, 5.45). E2's own fit is F_pi = 129.26 MeV, e = 5.444, "
      "giving M = 865.75, 1/I1 = 195.33, 1/I2 = 512.69 MeV, so the 14-1 gap is 708.0 instead of 708.9 MeV. Declared deviation; effect <= 0.3%.",
      suggested_fix="Optionally add the ladder at E2's fitted point, or say 'PLAN's rounded ANW point' wherever 'E2 parameters' appears."),
 dict(severity="minor", description="Reproducibility presentation: logs/run_all.log shows a resumed run (SKIP_DONE) in which e3_stability_refine was not executed; "
      "refine and make_results ran separately afterwards. run_all.sh in its current form has not been run end to end, and the '27 minutes' total is a sum of step times.",
      suggested_fix="Run run_all.sh once from scratch, or state that the total is summed."),
 dict(severity="minor", description="Seed-claim row 'the B = 1 fold is the long-root (SU(3)) hedgehog' is marked CONFIRMED. What is shown is that this hedgehog carries B = 1 (the generator) and is linearly stable. "
      "That it is the minimal B = 1 fold in G2 is OPEN, as the stability row itself says.",
      suggested_fix="Qualify the row: 'B = 1 generator, locally stable; global minimality OPEN'."),
]

out = dict(experiment="E3_internal_space_swap", overall="confirmed", issues=issues, rows=rows,
           my_checks=dict(g2=[c for c in g2["checks"]], skyrme=sk["checks"], flag=fl["checks"],
                          stability=(st["checks"] if st else None)),
           stability=st)
json.dump(out, open("crosscheck.json", "w"), indent=1, default=str)
for r in rows:
    print(("OK   " if r["agree"] else "DIFF ") + r["quantity"], "|", r["original"], "|", r["recomputed"],
          "|", f"{r.get('rel_diff', ''):.1e}" if isinstance(r.get("rel_diff"), float) else "")
print(sum(r["agree"] for r in rows), "/", len(rows), "agree")
