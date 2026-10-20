"""E1d illustration: space-time plots of two neighbouring Gaussian-packet collisions in the
(A, k) slice at sigma = 16 that end differently. Rule (no choice by eye): along k = 1.0, the
first A >= 0.8 whose production call differs from that at the next A step (+0.025).
Each run is redone with a recorded phi(x, t); a third panel runs the producing case as a single packet.
Writes e1d_example.json and fig_e1d_example.png.  Runtime ~10 s."""
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import e1d_gauss as G
from phi4core import grid, Sim, count_pairs

sl = json.load(open("e1d_sliceAk_16.0.json"))["runs"]
key = {(r["A"], r["k"]): r for r in sl}
As = sorted(set(r["A"] for r in sl))
kk = min(sorted(set(r["k"] for r in sl)), key=lambda k: abs(k - 1.0))
pick = None
for i, A in enumerate(As[:-1]):
    if A >= 0.8 - 1e-9 and key[(A, kk)]["produced"] != key[(As[i + 1], kk)]["produced"]:
        pick = (A, As[i + 1])
        break


def record(A, sigma, k, single=False):
    vg, x0, t_coll, T, Lphys = G.setup(A, sigma, k)
    x = grid(Lphys + G.WSP, 0.1)
    phi, pi = G.gauss_initial(x, A, sigma, k, x0, single=single)
    sim = Sim(x, phi, pi, 0.04, Lphys=Lphys, W=G.WSP, gmax=G.GMAX)
    every = int(round(2.0 / 0.04))
    rows = [sim.phi[::5].copy()]
    nT = int(round(T / 0.04))
    done = 0
    while done < nT:
        n = min(every, nT - done)
        sim.run(n)
        done += n
        rows.append(sim.phi[::5].copy())
    return x[::5], np.array(rows), T, count_pairs(x, sim.phi)


out = {"k": kk, "sigma": 16.0, "A_pair": pick, "runs": []}
fig, axs = plt.subplots(1, 3, figsize=(8.4, 3.5), sharey=True)
cases = [(pick[0], False), (pick[1], False), (pick[0] if key[(pick[0], kk)]["produced"] else pick[1], True)]
for ax, (A, single) in zip(axs, cases):
    xs, st, T, npair = record(A, 16.0, kk, single)
    r = key[(A, kk)]
    out["runs"].append({"A": A, "single_packet": single, "E_over_2M_pair_run": r["E_over_2M"],
                        "produced_scan_pair_run": r["produced"], "pairs_at_T_rerun": int(npair)})
    ax.imshow(st, origin="lower", aspect="auto", extent=[xs[0], xs[-1], 0, T], cmap="RdBu_r",
              vmin=-1.4, vmax=1.4, interpolation="nearest")
    ax.set_xlim(-140, 140)
    ax.set_xlabel("x")
    lab = ("single packet alone" if single else f"collision, E/2M={r['E_over_2M']:.1f}")
    ax.set_title(f"A={A}, k={kk}, sigma=16\n{lab}: " + ("pair" if npair else "no pair at T"), fontsize=7)
axs[0].set_ylabel("t")
fig.suptitle("E1d: two neighbouring Gaussian-packet collisions and a single-packet control (red: phi>0, blue: phi<0)", fontsize=8)
fig.tight_layout()
fig.savefig("fig_e1d_example.png", dpi=78)
json.dump(out, open("e1d_example.json", "w"), indent=1)
print(json.dumps(out, indent=1))
