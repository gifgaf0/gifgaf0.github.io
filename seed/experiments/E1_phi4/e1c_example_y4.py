"""E1c reconciliation figure: the DSV example column omega = 0.99 with fourth-order time stepping.

Runs (0.99, 0.41) and (0.99, 0.43) with the y4 integrator of e1c_reconcile.py at dx = 0.05, dt = 0.02 (calls converged
in e1c_reconcile.jsonl), recording phi(x, t) every 4 time units, and plots them next to the original leapfrog run of
(0.99, 0.43) at dx = 0.1, dt = 0.04 (e1c_example_spacetime.npz), whose late pair was the original 'example' call.
Writes e1c_example_y4.npz and fig_e1c_example_y4.png.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from phi4core import grid, count_pairs
from e1c_dsv import dsv_initial, WSP, GMAX
from e1c_reconcile import SimY4

DX, DT, REC = 0.05, 0.02, 4.0


def run(v):
    Lphys = 600.0
    T = 2 * Lphys
    x = grid(Lphys + WSP, DX)
    phi, pi = dsv_initial(x, 0.99, v)
    sim = SimY4(x, phi, pi, DT, Lphys, WSP, GMAX)
    sub = slice(None, None, 20)
    st = [sim.phi[sub].copy()]
    n = int(round(REC / DT))
    npairs = []
    for _ in range(int(round(1.5 * T / REC))):
        sim.run(n)
        st.append(sim.phi[sub].copy())
        npairs.append(count_pairs(x, sim.phi))
    return np.array(st, dtype=np.float32), x[sub], np.array(npairs)


res = {v: run(v) for v in (0.41, 0.43)}
np.savez_compressed("e1c_example_y4.npz", **{f"st_{v}": res[v][0] for v in res}, x=res[0.41][1],
                    **{f"npairs_{v}": res[v][2] for v in res}, dt_rec=REC)
orig = np.load("e1c_example_spacetime.npz")
panels = [("(0.99, 0.41), 4th order, dx 0.05, dt 0.02", res[0.41][0], res[0.41][1], REC),
          ("(0.99, 0.43), 4th order, dx 0.05, dt 0.02", res[0.43][0], res[0.43][1], REC),
          ("(0.99, 0.43), original leapfrog, dx 0.1, dt 0.04", orig["st"], orig["x"], float(orig["dt_rec"]))]
fig, axs = plt.subplots(1, 3, figsize=(9.6, 3.6), sharey=True)
for ax, (title, st, xs, dtr) in zip(axs, panels):
    tt = np.arange(st.shape[0]) * dtr
    ax.imshow(st, origin="lower", aspect="auto", extent=[xs[0], xs[-1], tt[0], tt[-1]], cmap="RdBu_r",
              vmin=-1.3, vmax=1.3, interpolation="nearest")
    ax.axhline(1200, color="k", lw=0.6, ls="--")
    ax.set_xlim(-400, 400)
    ax.set_xlabel("x")
    ax.set_title(title, fontsize=7.5)
axs[0].set_ylabel("t  (dashed: T = 1200)")
fig.suptitle("E1c reconciliation: phi(x, t) in the DSV example column (red: phi > 0)", fontsize=9)
fig.tight_layout()
fig.savefig("fig_e1c_example_y4.png", dpi=95)
for v in res:
    np_ = res[v][2]
    first = (np.argmax(np_ >= 1) + 1) * REC if (np_ >= 1).any() else None
    print(f"v = {v}: pair at T: {bool(np_[int(1200 / REC) - 1] >= 1)}, first pair at t = {first}")
