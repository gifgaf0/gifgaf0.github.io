"""E1c reconciliation: is the DSV example point (omega, v) = (0.99, 0.43) a converged producer?

The independent cross-check found that the original call (pair at T at dx = 0.1, dt = 0.04)
depends on (dx, dt). This script settles it with a time integrator of higher order:

  scheme "lf"  the original velocity-Verlet step of phi4core.py (second order in dt);
  scheme "y4"  Yoshida's fourth-order symmetric composition of the same velocity-Verlet step
               (weights w1, w0, w1 with w1 = 1/(2 - 2^(1/3)), w0 = -2^(1/3) w1), including the
               exact exponential damping split of the absorbing layer in every sub-step.

Space is the original fourth-order stencil; the initial data, lattice (Lphys = 600, layer
width 60, gmax = 1), run length (to 1.5 T, T = 1200) and pair test are exactly those of
e1c_dsv.py / phi4core.py. Convergence is judged by agreement of the call, of the time the pair
first appears, and of the trajectory phi(0, t) between resolutions.

Usage: python e1c_reconcile.py [nproc]      (resumable: finished runs are kept in
       e1c_reconcile.jsonl and skipped; phi(0, t) records go to reconcile_data/)
"""
import sys
import os
import json
import time
import numpy as np
import numba as nb
from multiprocessing import Pool
from phi4core import grid, sponge, force, count_pairs, positive_intervals, energy, Sim
from e1c_dsv import dsv_initial, train_extent, WSP, GMAX

OUT = "e1c_reconcile.jsonl"
DATA = "reconcile_data"
CBRT2 = 2.0 ** (1.0 / 3.0)
W1 = 1.0 / (2.0 - CBRT2)
W0 = -CBRT2 * W1
CHECK_DT = 10.0
REC_DT = 0.5


@nb.njit(cache=True, fastmath=False)
def _vv(phi, pi, F, h, inv12dx2, bL, bR, damp):
    n = phi.size
    hh = 0.5 * h
    for i in range(n):
        pi[i] = pi[i] * damp[i] + hh * F[i]
        phi[i] += h * pi[i]
    force(phi, F, inv12dx2, bL, bR)
    for i in range(n):
        pi[i] = (pi[i] + hh * F[i]) * damp[i]


@nb.njit(cache=True, fastmath=False)
def yoshida4(phi, pi, F, dt, nsteps, inv12dx2, bL, bR, d1, d0, w1, w0, ic, rec):
    for s in range(nsteps):
        _vv(phi, pi, F, w1 * dt, inv12dx2, bL, bR, d1)
        _vv(phi, pi, F, w0 * dt, inv12dx2, bL, bR, d0)
        _vv(phi, pi, F, w1 * dt, inv12dx2, bL, bR, d1)
        rec[s] = phi[ic]


class SimY4(Sim):
    def __init__(self, x, phi, pi, dt, Lphys, W, gmax):
        super().__init__(x, phi, pi, dt, Lphys=Lphys, W=W, gmax=gmax)
        gam = self.gamma
        self.d1 = np.exp(-0.5 * gam * W1 * dt)
        self.d0 = np.exp(-0.5 * gam * W0 * dt)

    def run(self, nsteps):
        rec = np.empty(nsteps)
        yoshida4(self.phi, self.pi, self.F, self.dt, nsteps, self.inv12dx2, self.bL, self.bR,
                 self.d1, self.d0, W1, W0, self.ic, rec)
        self.nstep += nsteps
        self.t = self.nstep * self.dt
        return rec


def key_of(omega, v, dx, dt, scheme):
    return f"{scheme}_om{omega:.3f}_v{v:.3f}_dx{dx:g}_dt{dt:g}"


def run_one(job):
    omega, v, dx, dt, scheme = job
    t0 = time.time()
    Lphys = max(600.0, np.ceil(train_extent(omega) / 50.0) * 50.0)
    T = 2.0 * Lphys
    x = grid(Lphys + WSP, dx)
    phi, pi = dsv_initial(x, omega, v)
    S = SimY4 if scheme == "y4" else Sim
    sim = S(x, phi, pi, dt, Lphys=Lphys, W=WSP, gmax=GMAX)
    inner = np.abs(x) <= Lphys
    E0 = sim.energy(mask=inner)
    nchk = int(round(CHECK_DT / dt))
    nT = int(round(T / dt))
    n_end = int(round(1.5 * T / dt))
    nrec = int(round(REC_DT / dt))
    tchk, npairs, outer = [0.0], [count_pairs(x, sim.phi)], [0.0]
    phi0 = [float(sim.phi[sim.ic])]
    done = 0
    E_T, ivs_T = None, []
    while done < n_end:
        rec = sim.run(nchk)
        done += nchk
        phi0.extend(rec[nrec - 1::nrec].tolist())
        tchk.append(done * dt)
        npairs.append(count_pairs(x, sim.phi))
        ivs = [iv for iv in positive_intervals(x, sim.phi) if iv[1] - iv[0] > 4 * np.sqrt(2)]
        outer.append(max([iv[1] for iv in ivs], default=0.0))
        if done == nT:
            E_T = sim.energy(mask=inner)
            ivs_T = [iv for iv in positive_intervals(x, sim.phi) if iv[1] - iv[0] > 1.0][:20]
    tchk = np.array(tchk)
    npairs = np.array(npairs)
    present = npairs >= 1

    def at(f):
        return int(npairs[np.argmin(np.abs(tchk - f * T))])
    kT = int(np.argmin(np.abs(tchk - T)))
    first_cont = None
    if present[kT]:
        j = kT
        while j > 0 and present[j - 1]:
            j -= 1
        first_cont = float(tchk[j])
    first_any = float(tchk[np.argmax(present)]) if present.any() else None
    k = key_of(omega, v, dx, dt, scheme)
    os.makedirs(DATA, exist_ok=True)
    np.save(os.path.join(DATA, k + "_phi0.npy"), np.array(phi0, dtype=np.float32))
    out = {"key": k, "omega": omega, "v": v, "dx": dx, "dt": dt, "scheme": scheme, "T": T, "Lphys": Lphys,
           "E0": E0, "E_T_inner": E_T,
           "produced_dsv": bool(at(1.0) >= 1),
           "survives_to_1.5T": bool(at(1.0) >= 1 and all(at(f) >= 1 for f in (1.1, 1.2, 1.3, 1.4, 1.5))),
           "pair_continuously_present_since": first_cont, "first_pair_any": first_any,
           "n_pairs_T": at(1.0), "outer_zero_series": [round(o, 2) for o in outer],
           "intervals_T": ivs_T, "npairs_series": npairs.astype(int).tolist(),
           "wall_s": time.time() - t0}
    return out


# lowest-energy producers of the original map after (0.90, 0.73) and (0.95, 0.62), in order of E (e1c_grid/fine.json)
E_CANDIDATES = [(0.94, 0.67), (0.95, 0.63), (0.95, 0.77), (0.96, 0.59), (0.94, 0.79), (0.95, 0.64),
                (0.91, 0.85), (0.93, 0.70), (0.90, 0.76), (0.94, 0.78), (0.94, 0.69), (0.92, 0.72)]


def jobs_list():
    J = []
    om = 0.99
    # A. decisive: fourth-order time stepping on the column, and the two key points refined
    J += [(om, v, 0.05, 0.02, "y4") for v in (0.41, 0.43)]
    J += [(om, 0.43, 0.1, 0.04, "lf")]                     # must reproduce the original call (pair since 1160)
    J += [(om, v, 0.05, 0.01, "y4") for v in (0.41, 0.43)]
    J += [(om, v, 0.025, 0.01, "y4") for v in (0.41, 0.43)]
    J += [(om, v, 0.05, 0.0025, "lf") for v in (0.41, 0.43)]  # leapfrog with dt -> 0 at fixed dx
    J += [(om, round(v, 3), 0.05, 0.02, "y4") for v in np.arange(0.38, 0.5001, 0.01) if round(v, 3) not in (0.41, 0.43)]
    # D. the DSV trains that set the E1e quanta count: (0.95, 0.62) (lowest producer reproduced at dx = 0.05)
    #    and (0.90, 0.73) (raw lowest), with fourth-order time stepping
    J += [(o, v, 0.05, 0.02, "y4") for o, v in ((0.95, 0.62), (0.90, 0.73))]
    # C. the original leapfrog at other (dx, dt), as run by the cross-check on a copy of the original code
    J += [(om, 0.41, 0.1, 0.04, "lf")]
    J += [(om, v, dx, dt, "lf") for v in (0.41, 0.43) for dx, dt in ((0.1, 0.02), (0.05, 0.02), (0.025, 0.005))]
    J += [(o, v, 0.025, 0.01, "y4") for o, v in ((0.95, 0.62), (0.90, 0.73))]
    # E. (0.95, 0.62) turned out unconverged: look for the lowest-energy DSV producer that is converged.
    #    Pass 1: the 12 next-lowest-energy producers of the original map at y4 (0.05, 0.02);
    #    pass 2 (built from pass-1 results already on disk): y4 (0.025, 0.01) for those that produced.
    J += [(o, v, 0.05, 0.02, "y4") for o, v in E_CANDIDATES]
    done = {}
    if os.path.exists(OUT):
        for line in open(OUT):
            if line.strip():
                r = json.loads(line)
                done[r["key"]] = r
    J += [(o, v, 0.025, 0.01, "y4") for o, v in E_CANDIDATES
          if done.get(key_of(o, v, 0.05, 0.02, "y4"), {}).get("produced_dsv")]
    # B. finer checks
    J += [(om, v, 0.025, 0.005, "y4") for v in (0.41, 0.43)]
    J += [(om, round(v, 3), 0.025, 0.01, "y4") for v in (0.39, 0.40, 0.42, 0.44, 0.45)]
    J += [(om, v, 0.0125, 0.005, "y4") for v in (0.41, 0.43)]
    # F. second reconciliation pass (added after the first pass was interrupted): finish the (dx, dt) ladder at
    #    v = 0.40 and 0.42, scan between the 0.01 grid points at and near 0.41-0.43, and resolution-check the
    #    hole that DSV name, (0.91, 0.82), with its neighbours (original map: 0.80 and 0.83 produce, 0.81-0.82 not)
    J += [(om, 0.40, 0.05, 0.01, "y4"), (om, 0.40, 0.025, 0.005, "y4"), (om, 0.42, 0.025, 0.005, "y4")]
    J += [(om, v, dx, dt, "y4") for v in (0.405, 0.415, 0.425, 0.435) for dx, dt in ((0.05, 0.02), (0.025, 0.01))]
    J += [(0.91, v, dx, dt, "y4") for v in (0.80, 0.81, 0.82, 0.83) for dx, dt in ((0.05, 0.02), (0.025, 0.01))]
    # G. added after the finest run of (0.99, 0.43) (y4, dx = 0.0125, dt = 0.005) produced a pair at t = 870 while the
    #    four coarser y4 settings did not: the late fate of the central oscillation is chaotic, so estimate the local
    #    production probability instead, from neighbouring initial data inside DSV's 0.01-wide v cell (step 0.001),
    #    around 0.43 and, as a control, around the converged producer 0.41. y4 at (0.05, 0.02).
    J += [(om, round(0.43 + d, 3), 0.05, 0.02, "y4") for d in (-0.004, -0.003, -0.002, -0.001, 0.001, 0.002, 0.003, 0.004)]
    J += [(om, round(0.41 + d, 3), 0.05, 0.02, "y4") for d in (-0.004, -0.003, -0.002, -0.001, 0.001, 0.002, 0.003, 0.004)]
    return J


if __name__ == "__main__":
    nproc = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    done = set()
    if os.path.exists(OUT):
        for line in open(OUT):
            if line.strip():
                done.add(json.loads(line)["key"])
    todo = [j for j in jobs_list() if key_of(*j) not in done]
    print(f"{len(done)} done, {len(todo)} to run", flush=True)
    t0 = time.time()
    with Pool(nproc) as pool:
        for r in pool.imap(run_one, todo, chunksize=1):
            with open(OUT, "a") as f:
                f.write(json.dumps(r) + "\n")
            print(f"{r['key']}: pair_at_T={r['produced_dsv']} since={r['pair_continuously_present_since']} "
                  f"first={r['first_pair_any']} survives1.5T={r['survives_to_1.5T']} "
                  f"E0={r['E0']:.6f} E_T={r['E_T_inner']:.6f} wall={r['wall_s']:.0f}s  [{time.time() - t0:.0f}s]",
                  flush=True)
    print("all done", flush=True)
