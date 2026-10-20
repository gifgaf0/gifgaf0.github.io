"""E1 verification pass (added by the resumed run; not preregistered).

V1  reproducibility: rerun stored E1b/E1c/E1d runs with the stored code and compare the calls.
V2  energy conservation of the integrator with no absorbing layer (Gaussian collision, kink collision).
V3  single-packet self-folding: convergence of the call in dx and dt for two self-folding packets
    and one non-folding packet.
Writes e1_verify.json. Runtime ~3-4 min on 2 processes.
Usage: NUMBA_NUM_THREADS=1 python e1_verify.py
"""
import json
import time
import numpy as np
from multiprocessing import Pool
from phi4core import grid, Sim, kk_initial, count_pairs, M_KINK
import e1d_gauss as G
import e1b_kkbar as B



def v1_gauss(args):
    A, s, k = args
    return run_g(A, s, k, 0.1, 0.4, False)


def run_g(A, s, k, dx, cfl, single):
    G.CFL = cfl
    r = G.run_gauss(A, s, k, dx=dx, single=single)
    return {kk: r[kk] for kk in ("A", "sigma", "k", "dx", "single", "produced", "E_over_2M",
                                 "pair_since", "n_pairs_T", "max_pairs_seen")} | {"cfl": cfl}


def v1_kk(v):
    B.CFL = 0.4
    r = B.collide(v, 12.0, 0.05, 600.0)
    return {"v": v, "label": r["label"], "nb": r["nb"]}


def v3(args):
    A, s, k, dx, cfl, single = args
    return run_g(A, s, k, dx, cfl, single)


def energy_check(kind):
    """Integrate without absorbing layer on a large grid until just before anything reaches the
    edge; return the relative energy drift."""
    dx = 0.05
    dt = 0.02
    if kind == "gauss":
        A, s, k = 0.8, 2.0, 0.5
        x0 = 4 * s + 10
        x = grid(400.0, dx)
        phi, pi = G.gauss_initial(x, A, s, k, x0)
        tend = 300.0
    else:
        x = grid(400.0, dx)
        phi, pi = kk_initial(x, 0.2, 12.0)
        tend = 300.0
    sim = Sim(x, phi, pi, dt, Lphys=None)
    E0 = sim.energy()
    Es = [E0]
    nchunk = int(round(10.0 / dt))
    while sim.t < tend - 1e-9:
        sim.run(nchunk)
        Es.append(sim.energy())
    Es = np.array(Es)
    return {"kind": kind, "dx": dx, "dt": dt, "t_end": sim.t, "E0": E0,
            "max_rel_drift": float(np.max(np.abs(Es - E0)) / E0),
            "final_rel_drift": float((Es[-1] - E0) / E0)}


if __name__ == "__main__":
    t0 = time.time()
    out = {}
    # ---------------- V1
    co = json.load(open("e1d_coarse.json"))["runs"]
    key = {(r["A"], r["sigma"], r["k"]): r for r in co}
    rng = np.random.default_rng(7)
    pick = [(0.8, 2.0, 0.5), (1.4, 1.0, 0.25), (0.6, 4.0, 0.5)]
    for i in rng.choice(len(co), size=9, replace=False):
        r = co[int(i)]
        pick.append((r["A"], r["sigma"], r["k"]))
    base = json.load(open("e1b_base.json"))["runs"]
    bkey = {round(r["v"], 7): r for r in base}
    vs = [0.2, 0.225, 0.25, 0.258, 0.2605, 0.27]
    with Pool(2) as pool:
        rg = pool.map(v1_gauss, pick, chunksize=1)
        rk = pool.map(v1_kk, vs, chunksize=1)
        en = pool.map(energy_check, ["gauss", "kk"])
        v3jobs = []
        for (A, s, k, single) in [(0.5, 16.0, 0.25, True), (0.925, 16.0, 1.0, True), (0.3, 16.0, 0.25, True),
                                  (0.8, 2.0, 0.5, False)]:
            for dx, cfl in [(0.1, 0.4), (0.05, 0.4), (0.025, 0.4), (0.05, 0.1)]:
                v3jobs.append((A, s, k, dx, cfl, single))
        r3 = pool.map(v3, v3jobs, chunksize=1)
    v1g = []
    for r in rg:
        s = key[(r["A"], r["sigma"], r["k"])]
        v1g.append({"A": r["A"], "sigma": r["sigma"], "k": r["k"], "stored": s["produced"], "rerun": r["produced"],
                    "E_stored": s["E_over_2M"], "E_rerun": r["E_over_2M"]})
    v1k = []
    for r in rk:
        s = bkey.get(round(r["v"], 7))
        v1k.append({"v": r["v"], "stored": s["label"] if s else None, "rerun": r["label"]})
    ex = json.load(open("e1c_example.json"))
    out["V1_reproducibility"] = {"gauss": v1g, "kkbar": v1k,
                                 "all_gauss_agree": all(a["stored"] == a["rerun"] and abs(a["E_stored"] - a["E_rerun"]) < 1e-9
                                                        for a in v1g),
                                 "all_kkbar_agree": all(a["stored"] == a["rerun"] for a in v1k if a["stored"] is not None)}
    out["V2_energy_conservation"] = en
    out["V3_single_packet_convergence"] = r3
    out["runtime_s"] = time.time() - t0
    json.dump(out, open("e1_verify.json", "w"), indent=1)
    print("V1 gauss agree:", out["V1_reproducibility"]["all_gauss_agree"],
          " kkbar agree:", out["V1_reproducibility"]["all_kkbar_agree"])
    for a in v1g:
        print("  ", a)
    for a in v1k:
        print("  ", a)
    print("V2:", json.dumps(en, indent=1))
    print("V3 (A, sigma, k, single, dx, cfl -> produced, pair_since):")
    for r in r3:
        print(f"   {r['A']:.3f} {r['sigma']:5.1f} {r['k']:.2f} single={r['single']} dx={r['dx']:.3f} "
              f"dt={r['dx'] * r['cfl']:.4f} -> {r['produced']} since={r['pair_since']} max_pairs={r['max_pairs_seen']}")
    print(f"runtime {time.time() - t0:.0f} s")
