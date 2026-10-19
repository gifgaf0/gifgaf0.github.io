"""E1c: Dutta-Steer-Vachaspati (arXiv:0803.0670) breather trains in phi^4.

Initial data, eqs. (11)-(13) of DSV, as published:
  f(t,x) = -1 + sum_{n=-Nb..Nb, n!=0} (4/pi) arctan[ eta sin(omega T_n) / cosh(eta omega X_n) ]
  T_n = g [t - v_n (x - x0n)],  X_n = g [(x - x0n) - v_n t],  g = 1/sqrt(1-v^2)
  eta = sqrt(1-omega^2)/omega
  x0n = a + n d, v_n = -v (n > 0);  x0n = -a + n d, v_n = +v (n < 0)
  Nb = int[2/sqrt(1-omega^2)] + 1,  a = 10/sqrt(1-omega^2),  d = 2/sqrt(1-omega^2)
  phi(0,x) = f(0,x), phi_t(0,x) = f_t(0,x).
Lattice (our choice, DSV do not state it; their Fig. 1 spans -600..600):
  physical region |x| < 600 (or larger when a train does not fit, for omega > 0.99),
  absorbing layer of width 60 beyond it, evolved for one light-crossing time
  of the physical lattice, T = 2 Lphys.
Production, recorded three ways (pair = phi4core.count_pairs):
  produced_dsv      pair present at t = T (DSV: "kinks survived for at least the
                    duration of the simulation"); primary for E1c, as published;
  produced_persist  pair present at 0.80T, 0.85T, 0.90T, 0.95T, T (the criterion
                    fixed in phi4core.py for E1d);
  survives_to_1.5T  pair at T and at 1.1T ... 1.5T (robustness of the DSV call).

Usage: python e1c_dsv.py <mode> [nproc]
  mode = grid     omega 0.90..0.99 (0.01) x v 0.40..0.90 (0.02), dx 0.1
         fine     same omegas, v 0.41..0.89 (0.02) -> v step 0.01 when merged
         dxcheck  omega in {0.91, 0.95, 0.99}, v 0.40..0.90 (0.02), dx 0.05
         high     omega in {0.992, 0.995}, v 0.20..0.90 (0.02), dx 0.1
         example  (0.99, 0.43) with space-time record for the figure
"""
import sys
import json
import time
import numpy as np
from multiprocessing import Pool
from phi4core import grid, Sim, count_pairs, energy, PERSIST_FRACS, positive_intervals

WSP = 60.0
GMAX = 1.0
CFL = 0.4


def dsv_params(omega):
    s = np.sqrt(1.0 - omega * omega)
    Nb = int(np.floor(2.0 / s)) + 1
    a = 10.0 / s
    d = 2.0 / s
    eta = s / omega
    return Nb, a, d, eta


def dsv_initial(x, omega, v):
    Nb, a, d, eta = dsv_params(omega)
    g = 1.0 / np.sqrt(1.0 - v * v)
    phi = -np.ones_like(x)
    pi = np.zeros_like(x)
    for n in list(range(-Nb, 0)) + list(range(1, Nb + 1)):
        if n > 0:
            x0n, vn = a + n * d, -v
        else:
            x0n, vn = -a + n * d, +v
        T = -g * vn * (x - x0n)          # t = 0
        X = g * (x - x0n)
        ch = np.cosh(eta * omega * X)
        sh = np.sinh(eta * omega * X)
        u = eta * np.sin(omega * T) / ch
        du = eta * omega * g * (np.cos(omega * T) * ch + eta * vn * np.sin(omega * T) * sh) / ch ** 2
        phi += (4.0 / np.pi) * np.arctan(u)
        pi += (4.0 / np.pi) * du / (1.0 + u * u)
    return phi, pi


def train_extent(omega):
    Nb, a, d, eta = dsv_params(omega)
    return a + Nb * d + 5.0 / np.sqrt(1 - omega ** 2)


CHECK_DT = 10.0
EXT = 1.5          # evolve on to 1.5 T to test whether pairs seen at T survive


def run_dsv(omega, v, dx=0.1, record=False):
    Lphys = max(600.0, np.ceil(train_extent(omega) / 50.0) * 50.0)
    T = 2.0 * Lphys
    x = grid(Lphys + WSP, dx)
    phi, pi = dsv_initial(x, omega, v)
    dt = CFL * dx
    sim = Sim(x, phi, pi, dt, Lphys=Lphys, W=WSP, gmax=GMAX)
    inner = np.abs(x) <= Lphys
    E0 = sim.energy(mask=inner)
    E0_all = sim.energy()
    nchk = int(round(CHECK_DT / dt))
    nT = int(round(T / dt))
    n_end = int(round(EXT * T / dt))
    tchk, npairs = [0.0], [count_pairs(x, sim.phi)]
    st = None
    rec_every = int(round(4.0 / dt))
    if record:
        sub = slice(None, None, 10)
        st = [sim.phi[sub].copy()]
        marks = sorted(set(range(nchk, n_end + 1, nchk)) | set(range(rec_every, n_end + 1, rec_every)))
    else:
        marks = list(range(nchk, n_end + 1, nchk))
    done = 0
    E_T = None
    for m in marks:
        sim.run(m - done)
        done = m
        if m % nchk == 0:
            tchk.append(m * dt)
            npairs.append(count_pairs(x, sim.phi))
        if m == nT:
            E_T = sim.energy(mask=inner)
            ivs_T = positive_intervals(x, sim.phi)
        if record and m % rec_every == 0:
            st.append(sim.phi[sub].copy())
    tchk = np.array(tchk)
    npairs = np.array(npairs)

    def at(f):
        return int(npairs[np.argmin(np.abs(tchk - f * T))])
    persist = [at(f) for f in PERSIST_FRACS]
    ext = [at(f) for f in (1.1, 1.2, 1.3, 1.4, 1.5)]
    present = npairs >= 1
    # start of the last uninterrupted stretch with a pair, up to T
    first_cont = None
    k = int(np.argmin(np.abs(tchk - T)))
    if present[k]:
        j = k
        while j > 0 and present[j - 1]:
            j -= 1
        first_cont = float(tchk[j])
    out = {"omega": omega, "v": v, "dx": dx, "Lphys": Lphys, "T": T,
           "Nb": dsv_params(omega)[0], "E0": E0, "E0_incl_sponge": E0_all,
           "produced_dsv": bool(at(1.0) >= 1),
           "produced_persist": bool(all(n >= 1 for n in persist)),
           "survives_to_1.5T": bool(at(1.0) >= 1 and all(n >= 1 for n in ext)),
           "n_pairs_T": at(1.0), "npairs_persist_checks": persist, "npairs_ext_checks": ext,
           "pair_continuously_present_since": first_cont,
           "final_positive_intervals_T": [iv for iv in ivs_T if iv[1] - iv[0] > 1.0][:20],
           "E_T_inner": E_T,
           "npairs_series": npairs.astype(int).tolist()}
    out["produced"] = out["produced_dsv"]
    if record:
        out["spacetime"] = np.array(st)
        out["x_sub"] = x[::10]
    return out


def _job(a):
    return run_dsv(*a)


if __name__ == "__main__":
    mode = sys.argv[1]
    nproc = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    t0 = time.time()
    oms = np.round(np.arange(0.90, 0.9901, 0.01), 3)
    if mode == "grid":
        jobs = [(float(o), float(v), 0.1) for o in oms for v in np.round(np.arange(0.40, 0.9001, 0.02), 3)]
    elif mode == "fine":
        jobs = [(float(o), float(v), 0.1) for o in oms for v in np.round(np.arange(0.41, 0.8901, 0.02), 3)]
    elif mode == "dxcheck":
        jobs = [(float(o), float(v), 0.05) for o in (0.91, 0.95, 0.99) for v in np.round(np.arange(0.40, 0.9001, 0.02), 3)]
    elif mode == "high":
        jobs = [(float(o), float(v), 0.1) for o in (0.992, 0.995) for v in np.round(np.arange(0.20, 0.9001, 0.02), 3)]
    elif mode == "example":
        r = run_dsv(0.99, 0.43, 0.1, record=True)
        np.savez_compressed("e1c_example_spacetime.npz", st=r.pop("spacetime").astype(np.float32),
                            x=r.pop("x_sub"), dt_rec=4.0)
        r["runtime_s"] = time.time() - t0
        json.dump(r, open("e1c_example.json", "w"), indent=1)
        print(json.dumps(r, indent=1))
        sys.exit(0)
    else:
        raise SystemExit("unknown mode")
    # longest jobs first
    jobs = sorted(jobs, key=lambda j: -train_extent(j[0]) / j[2])
    with Pool(nproc) as pool:
        res = []
        for i, r in enumerate(pool.imap_unordered(_job, jobs, chunksize=1)):
            res.append(r)
            if (i + 1) % 20 == 0:
                print(f"[{mode}] {i + 1}/{len(jobs)} done, {time.time() - t0:.0f} s", flush=True)
    res = sorted(res, key=lambda r: (r["omega"], r["v"]))
    json.dump({"mode": mode, "runs": res, "runtime_s": time.time() - t0},
              open(f"e1c_{mode}.json", "w"), indent=1)
    for o in sorted(set(r["omega"] for r in res)):
        row = "".join(("X" if r["survives_to_1.5T"] else "x") if r["produced_dsv"] else "."
                      for r in res if r["omega"] == o)
        print(f"omega={o:.3f} {row}")
    print(f"[{mode}] total {time.time() - t0:.0f} s")
