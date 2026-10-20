"""E1e: number of quanta in the smallest producing initial states (PLAN.md E1e).

Scaling. For L = 1/2 (dPhi)^2 - (lambda/4)(Phi^2 - v^2)^2 put Phi = v phi,
x = x~ / (sqrt(lambda) v). Then S = v^2 S~[phi] with S~ the action in the units
used everywhere in E1 (V = (phi^2-1)^2/4, m~ = sqrt2). Classical dynamics does
not depend on phi0 = v, and with hbar = 1
    E_phys / m_phys = v^2 E~ / sqrt2 = phi0^2 E~ / m~,     phi0^2 = m_phys^2 / (2 lambda)
so the quanta count of a classical initial state is
    N = E/m = phi0^2 E~/sqrt2,   N * lambda / m^2 = E~ / (2 sqrt2).
lambda/m^2 is the dimensionless coupling in 1+1 D. Two counts are reported:
  N_E   = E/m (PLAN.md definition: every quantum counted at rest energy m),
  N_lin = sum_q (|pi_q|^2 + w_q^2 |delta_q|^2)/(2 w_q) of the fluctuation about phi = -1
          (free-field occupation number; N_lin <= N_E up to the quartic terms).
Energy threshold alone: E >= 2 M_kink  =>  N_E * lambda/m^2 >= 2/3.

Inputs: e1c_grid.json, e1c_fine.json, e1c_high.json, e1c_example.json (DSV trains),
        e1d_coarse.json, e1d_single.json, e1d_slice*.json (Gaussian packets).
Runs single-packet controls for the lowest-E and lowest-N_lin producing Gaussian
runs that have none yet (a few seconds). Writes e1e_results.json.
"""
import glob
import json
import os
import numpy as np
from phi4core import M_KINK, grid, free_quanta
from e1c_dsv import dsv_initial
import e1d_gauss as G

SQ2 = np.sqrt(2.0)
TWO_M = 2.0 * M_KINK


def lam_units(E):
    return {"E_tilde": E, "E_over_2M": E / TWO_M, "N_E_over_phi0sq": E / SQ2,
            "N_E_times_lambda_over_m2": E / (2 * SQ2)}


out = {"conventions": "N*lambda/m^2 = E~/(2 sqrt2); phi0^2 = m^2/(2 lambda); hbar = 1; E~ in V=(phi^2-1)^2/4 units",
       "threshold_2M_kink": lam_units(TWO_M)}

# ------------------------------------------------------------ DSV trains
dsv = []
for fn in ("e1c_grid.json", "e1c_fine.json", "e1c_high.json"):
    if os.path.exists(fn):
        dsv += json.load(open(fn))["runs"]
ex = json.load(open("e1c_example.json"))
dsv.append(ex)
dsv_out = {}
for crit in ("produced_dsv", "survives_to_1.5T", "produced_persist"):
    sel = [r for r in dsv if r[crit]]
    if not sel:
        dsv_out[crit] = None
        continue
    rE = min(sel, key=lambda r: r["E0"])
    x = grid(max(660.0, rE["Lphys"] + 60.0), 0.1)
    phi, pi = dsv_initial(x, rE["omega"], rE["v"])
    Eq, Nl = free_quanta(phi, pi, 0.1)
    d = {"omega": rE["omega"], "v": rE["v"], "n_producing": len(sel), **lam_units(rE["E0"]),
         "N_lin_over_phi0sq": Nl, "N_lin_times_lambda_over_m2": Nl / 2.0}
    # smallest N_lin among producing runs
    best = None
    for r in sel:
        x = grid(max(660.0, r["Lphys"] + 60.0), 0.1)
        phi, pi = dsv_initial(x, r["omega"], r["v"])
        _, n = free_quanta(phi, pi, 0.1)
        if best is None or n < best[0]:
            best = (n, r["omega"], r["v"], r["E0"])
    d["min_N_lin_run"] = {"omega": best[1], "v": best[2], "E_over_2M": best[3] / TWO_M,
                          "N_lin_over_phi0sq": best[0], "N_lin_times_lambda_over_m2": best[0] / 2.0}
    dsv_out[crit] = d
out["dsv_trains"] = dsv_out

# ------------------------------------------------------------ Gaussian packets
co = json.load(open("e1d_coarse.json"))["runs"]
single = {}
if os.path.exists("e1d_single.json"):
    for r in json.load(open("e1d_single.json"))["runs"]:
        single[(r["A"], r["sigma"], r["k"])] = r["produced"]
gruns = [dict(r, src="coarse") for r in co]
for fn in sorted(f for f in glob.glob("e1d_slice*.json") if not f.endswith("_single.json")):
    gruns += [dict(r, src=os.path.basename(fn)) for r in json.load(open(fn))["runs"]]
prod = [r for r in gruns if r["produced"]]


def single_control(r):
    key = (r["A"], r["sigma"], r["k"])
    if key not in single:
        single[key] = G.run_gauss(r["A"], r["sigma"], r["k"], 0.1, True)["produced"]
    return single[key]


g_out = {"n_runs": len(gruns), "n_producing": len(prod)}
for name, keyf in (("min_E", lambda r: r["E"]), ("min_N_lin", lambda r: r["N_lin"])):
    srt = sorted(prod, key=keyf)
    first_any = srt[0]
    sc = single_control(first_any)
    first_coll = None
    for r in srt[:60]:
        if not single_control(r):
            first_coll = r
            break
    def pack(r):
        return {"A": r["A"], "sigma": r["sigma"], "k": r["k"], "vg": r["vg"], "src": r["src"],
                **lam_units(r["E"]), "N_lin_over_phi0sq": r["N_lin"], "N_lin_times_lambda_over_m2": r["N_lin"] / 2.0,
                "single_packet_alone_produces": single[(r["A"], r["sigma"], r["k"])]}
    g_out[name + "_any"] = pack(first_any)
    g_out[name + "_collision_only"] = pack(first_coll) if first_coll else None
out["gaussian_packets"] = g_out

# local probe around the smallest-N_lin producer (e1d_probe_min.py, not preregistered)
if os.path.exists("e1d_probe_min.json"):
    pm = json.load(open("e1d_probe_min.json"))
    lp = [r for r in pm["local"] if r["produced"]]
    g_out["probe_local"] = {"around": pm["local_grid_around"], "n": len(pm["local"]), "n_produced": len(lp),
                            "dx0.05_rerun_of_top5": pm["dx0.05"], "single_packet_top5": pm["single"],
                            "phase_shifts_produced": pm["phase_summary"]}
    if lp:
        r = min(lp, key=lambda q: q["N_lin"])
        g_out["probe_local"]["min_N_lin_producing"] = {"A": r["A"], "k": r["k"], "E_over_2M": r["E_over_2M"],
                                                       "N_lin_over_phi0sq": r["N_lin"],
                                                       "N_lin_times_lambda_over_m2": r["N_lin"] / 2.0}

# robust minima: producers whose call is reproduced at dx = 0.05 (e1d_probe_min.py)
rob = {}
if os.path.exists("e1d_probe_min.json"):
    rep = {(r["A"], r["sigma"], r["k"]): r["produced"] for r in pm["dx0.05"]}
    cand_runs = {(r["A"], r["sigma"], r["k"]): r for r in pm["top5_by_N_lin"] + pm.get("top5_by_E", [])}
    good = [dict(r, reproduced=rep.get(kk)) for kk, r in cand_runs.items()]
    g_out["dx0.05_reproduction_of_smallest_producers"] = good
    ok = [r for r in good if r["reproduced"]]
    if ok:
        rN = min(ok, key=lambda r: r["N_lin"])
        rE = min(ok, key=lambda r: r["E_over_2M"])
        rob["min_N_lin_reproduced"] = {"A": rN["A"], "sigma": rN["sigma"], "k": rN["k"], "E_over_2M": rN["E_over_2M"],
                                       "N_E_times_lambda_over_m2": rN["E_over_2M"] * TWO_M / (2 * SQ2),
                                       "N_lin_over_phi0sq": rN["N_lin"], "N_lin_times_lambda_over_m2": rN["N_lin"] / 2.0}
        rob["min_E_reproduced"] = {"A": rE["A"], "sigma": rE["sigma"], "k": rE["k"], "E_over_2M": rE["E_over_2M"],
                                   "N_E_times_lambda_over_m2": rE["E_over_2M"] * TWO_M / (2 * SQ2),
                                   "N_lin_over_phi0sq": rE["N_lin"], "N_lin_times_lambda_over_m2": rE["N_lin"] / 2.0}
g_out["robust"] = rob

# DSV: walk up the producing trains in E (and in N_lin) until one is reproduced at dx = 0.05
from e1c_dsv import run_dsv
dxc = {}
if os.path.exists("e1c_dxcheck.json"):
    dxc = {(r["omega"], r["v"]): r["produced_dsv"] for r in json.load(open("e1c_dxcheck.json"))["runs"]}


def nlin_dsv(r):
    x = grid(max(660.0, r["Lphys"] + 60.0), 0.1)
    phi, pi = dsv_initial(x, r["omega"], r["v"])
    return free_quanta(phi, pi, 0.1)[1]


dd = dsv_out.get("produced_dsv")
if dd:
    selp = [r for r in dsv if r["produced_dsv"] and r.get("dx", 0.1) == 0.1]
    for r in selp:
        r["_nlin"] = nlin_dsv(r)
    for tag, keyf in (("min_E", lambda r: r["E0"]), ("min_N_lin", lambda r: r["_nlin"])):
        tried = []
        for r in sorted(selp, key=keyf)[:8]:
            kk = (r["omega"], r["v"])
            rep = dxc[kk] if kk in dxc else run_dsv(r["omega"], r["v"], 0.05)["produced_dsv"]
            tried.append({"omega": r["omega"], "v": r["v"], "E_over_2M": r["E0"] / TWO_M, "N_lin_over_phi0sq": r["_nlin"],
                          "reproduced_dx0.05": bool(rep)})
            if rep:
                dd[f"{tag}_reproduced_dx0.05"] = {**tried[-1], **lam_units(r["E0"]),
                                                  "N_lin_times_lambda_over_m2": r["_nlin"] / 2.0}
                break
        dd[f"{tag}_dx0.05_walk"] = tried

# ------------------------------------------------------------ implication
cands = {}
if rob.get("min_N_lin_reproduced"):
    cands["gaussian_reproduced_at_dx0.05"] = rob["min_N_lin_reproduced"]["N_lin_times_lambda_over_m2"]
dd = dsv_out.get("produced_dsv")
if dd and dd.get("min_N_lin_reproduced_dx0.05"):
    cands["dsv_reproduced_at_dx0.05"] = dd["min_N_lin_reproduced_dx0.05"]["N_lin_times_lambda_over_m2"]
c_min = float(min(cands.values())) if cands else float("nan")
out["smallest_classical_N_lin_times_lambda_over_m2_found"] = c_min
out["smallest_raw_not_reproduced"] = {"gaussian_any": g_out["min_N_lin_any"]["N_lin_times_lambda_over_m2"]}
out["implication"] = {
    "statement": "classical production found only for N >= c m^2/lambda (c from producing runs that reproduce at "
                 "dx = 0.05); c is an upper bound on the true minimum (searched sets only)",
    "c": c_min, "candidates": cands,
    "N_needed_at_lambda_over_m2": {str(g): c_min / g for g in (1.0, 0.1, 0.01, 0.001)},
    "coupling_where_N_equals_2": c_min / 2.0,
    "coupling_where_N_equals_10": c_min / 10.0}
json.dump(out, open("e1e_results.json", "w"), indent=1, default=float)
print(json.dumps(out, indent=1, default=float))
