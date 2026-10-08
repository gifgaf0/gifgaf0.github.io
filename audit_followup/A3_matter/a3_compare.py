#!/usr/bin/env python3
"""A3 two-leg comparison: first leg (a3_results.json) against the blind second leg (leg2/leg2_results.json).
Agreement criterion (A3_PREREG.md): numbers to 1e-6 relative (closed forms exactly); identical classifications."""
import json, hashlib
H = "/home/claude/gifgaf0.github.io/audit_followup/A3_matter"
assert hashlib.md5(open(H + "/A3_PREREG.md", "rb").read()).hexdigest() == "e2f1090cac3b097c0d2d205146c8b67c"
L1 = json.load(open(H + "/a3_results.json")); L2 = json.load(open(H + "/leg2/leg2_results.json"))
f = float
rows = []
def num(name, a, b, tol=1e-6):
    a, b = f(a), f(b)
    rel = abs(a - b) / max(abs(b), 1e-300) if b != 0 else abs(a - b)
    rows.append((name, f"{a:.12g}", f"{b:.12g}", f"{rel:.1e}", "PASS" if rel <= tol else "FAIL"))
def cls(name, a, b):
    rows.append((name, str(a), str(b), "-", "PASS" if a == b else "FAIL"))
T1, T2, T3, T4 = L2["T1"], L2["T2"], L2["T3"], L2["T4"]
num("four-arc total length (per tube radius)", L1["four_arc"]["total_length_per_radius"], T1["L_total"])
num("four-arc component length", L1["four_arc"]["component_length"], T1["L_component"])
num("link thickness (tube radius)", L1["embedding"]["link_thickness"], T1["thickness_link"])
num("min inter-component distance", L1["embedding"]["min_inter_component_refined"], T1["min_intercomponent_distance"])
num("single-component thickness 2(sqrt7-1)/2", L1["embedding"]["doubly_critical_exact"]/2, T1["thickness_single_component"])
cls("pairwise linking numbers", sorted(L1["linking"].values()), [0.0, 0.0, 0.0])
num("L(m_p; 20/6)", L1["mass"]["L_B_inverted"], T2["a"]["L"])
num("m_p at L = 58.006", L1["mass"]["m_p_at_58006"], T2["b"]["m_at_58_006"])
num("m_p at four-arc length", L1["mass"]["m_p_at_four_arc"], T2["b"]["m_at_T1_length"])
num("A/Zf reproducing 80.95", L1["mass"]["AZ_for_8095"], T2["c"]["aoz_exact_for_80_95"])
cls("nearest p/q for 80.95", f"{L1['mass']['nearest_pq'][0]}/{L1['mass']['nearest_pq'][1]}", T2["c"]["nearest_rational"])
num("L(m_p; 1/2)", L1["mass"]["L_inverted_nearest_pq"], T2["c"]["L_with_nearest"])
num("L(m_p; 70/6)", L1["mass"]["L_inverted_A70"], T2["d"]["L_70_6"])
num("m(70/6, 58.006)", L1["mass"]["m_at_58006_A70"], T2["d"]["m_70_6_at_58_006"])
num("m(1, 2pi) continuum r_eff", L1["mass"]["m_e_continuum_reff"], T2["m_at_Ae_1_L_2pi"])
A = L1["alexander"]
cls("multivariable Delta", A["multivariable"].replace(" ", ""), T4["multivariable_factored"].replace(" ", ""))
cls("Delta(t,t,t)", A["diag"].replace(" ", ""), T4["delta_ttt_factored"].replace(" ", ""))
cls("one-variable Delta_L", A["one_var"].replace(" ", ""), T4["delta_L_factored"].replace(" ", ""))
cls("sum of squares Delta(t,t,t)", A["diag_sum_sq"], T4["sumsq_delta_ttt"])
cls("sum of squares Delta_L", A["one_var_sum_sq"], T4["sumsq_delta_L"])
names = {"up": "Up", "down": "Down", "charm": "Charm", "bottom": "Bottom", "top": "Top", "tau": "Tau", "W": "W", "Z": "Z"}
l2rows = {r["name"]: r for r in T3["rows"]}
for r in L1["mass_table"]:
    q = l2rows[names[r["row"]]]
    num(f"{r['row']}: predicted mass", r["pred"], q["recomputed"])
    num(f"{r['row']}: error vs PDG 2024 (%)", r["err_pct"], q["err_pct_recomputed"])
    v1 = "NOT HOLDING" if r["rule"].startswith("NOT") else ("holds" if r["rule"] in ("holds", "within 2%") else "reported")
    v2 = q.get("verdict_recomputed", "reported")
    v2 = "holds" if v2 == "holds" else ("NOT HOLDING" if v2 == "NOT HOLDING" else "reported")
    cls(f"{r['row']}: DR-A3-7 classification", v1, v2)
imp = L2["implied_by_rules"]
v = L1["verdicts"]
cls("DR-A3-2 verification (1) fails", v["verification1_fails"], "FAILS" in json.dumps(imp["DR-A3-2"]))
cls("DR-A3-2 clause 2 fires", v["clause2_fires"], False if "not triggered" in json.dumps(imp["DR-A3-2"]) else True)
w = max(len(r[0]) for r in rows)
lines = [f"{'quantity':{w}s} | first leg | second leg | rel diff | result", "-"*(w + 60)]
lines += [f"{r[0]:{w}s} | {r[1]} | {r[2]} | {r[3]} | {r[4]}" for r in rows]
npass = sum(r[4] == "PASS" for r in rows)
lines.append(f"\n{npass}/{len(rows)} PASS")
lines.append("second-leg implied_by_rules: " + json.dumps(imp, ensure_ascii=False))
open(H + "/a3_compare_output.txt", "w").write("\n".join(lines) + "\n")
print("\n".join(lines))
