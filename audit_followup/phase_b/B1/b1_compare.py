#!/usr/bin/env python3
"""B1: compare the first leg (b1_results.json) with the blind second leg (leg2/leg2_results.json), per B1_PREREG.md."""
import json, sys

a = json.load(open("b1_results.json"))
b = json.load(open("leg2/leg2_results.json"))
rows = []
def check(name, va, vb, ok):
    rows.append((name, va, vb, ok))

for rho in ("3", "3bar"):
    for n in "0123":
        check(f"sector color rho={rho} N={n}", a["C1_sector_colors"][rho][n], b["sector_colors"][rho][n],
              a["C1_sector_colors"][rho][n] == b["sector_colors"][rho][n])
check("additive", a["C2_additive"], b["additive"], a["C2_additive"] == b["additive"])
check("an option reproduces paper Y", a["C3_any_reproduces_Y"], b["any_option_reproduces_paper_Y"],
      a["C3_any_reproduces_Y"] == b["any_option_reproduces_paper_Y"])
check("an option reproduces paper table", a["C3_any_reproduces_table"], b["any_option_reproduces_paper_table"],
      a["C3_any_reproduces_table"] == b["any_option_reproduces_paper_table"])
check("paper labels realizable", a["C3_paper_labels_possible"], b["paper_labels_realizable"],
      a["C3_paper_labels_possible"] == b["paper_labels_realizable"])
for rho in ("3", "3bar"):
    for n in "0123":
        pa, pb = a["C4"][rho][n], b["induced_pairs"][rho][n]
        check(f"induced pair rho={rho} N={n}", pa, pb, pa[0] == pb[0] and pa[1] == pb[1] and bool(pa[2]) == bool(pb[2]))
for k in ("sin_vs_Vus_direct", "sin_vs_lambda_fit", "tan_vs_Vus_over_Vud_direct", "tan_vs_Kmu2_over_Vud", "tan_vs_fit"):
    va, vb = a["C5_pulls"][k], b["pulls"][k]
    check(f"pull {k}", va, vb, abs(va - vb) <= 0.01)
c6 = a["C6"]
for ka, kb in (("aut_order", "aut_order"), ("equals_AGL17", "equals_AGL17"), ("keeps_each_Fano_plane", "keeps_each_family"),
               ("orientation_preserving", "orientation_preserving"), ("orientation_reversing", "orientation_reversing"),
               ("stab_S7_FanoPlus", "stab_S7_family_plus"), ("stab_cap_aut", "stab_cap_aut")):
    check(f"C6 {ka}", c6[ka], b[kb], c6[ka] == b[kb])

w = max(len(r[0]) for r in rows)
for name, va, vb, ok in rows:
    print(f"{name:<{w}}  leg1={va!s:<28} leg2={vb!s:<28} {'PASS' if ok else 'FAIL'}")
n_ok = sum(r[3] for r in rows)
print(f"\n{n_ok}/{len(rows)} PASS")
sys.exit(0 if n_ok == len(rows) else 1)
