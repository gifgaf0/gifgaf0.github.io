"""E1d: colliding Gaussian packets of the phi^4 field itself (the seed's Model A).

Initial data (PLAN.md E1d), right-mover at -x0, left-mover at +x0:
  phi   = -1 + A G(x+x0) cos(k(x+x0)) + A G(x-x0) cos(k(x-x0)),  G(y) = exp(-y^2/(2 sigma^2))
  phi_t = A w_k G(x+x0) sin(k(x+x0)) - A w_k G(x-x0) sin(k(x-x0)),  w_k = sqrt(k^2 + 2)
  (narrow-band form of "phi_t from the linear dispersion"; group velocity v_g = k / w_k).
Fixed rules (no tuning): x0 = 4 sigma + 10; t_coll = x0 / v_g;
  T = max(t_coll + 400, 1.25 (t_coll + 100)); physical half-width Lphys = x0 + 4 sigma + 40,
  absorbing layer of width 50 beyond; dx = 0.1, dt = 0.04.
Production criterion (fixed in phi4core.py before any scan): a pair (interval with
phi > 0 longer than 4 sqrt2 and phi > 0.5 on >= 80% of it, searched over the whole
grid including the absorbing layer) at each of 0.80T, 0.85T, 0.90T, 0.95T and T.
Energy: from the discrete initial data, in units of 2 M_kink = 4 sqrt2 / 3.

Usage: python e1d_gauss.py <mode> [nproc]
  coarse    3D grid A x sigma x k
  sliceAk   2D slice in (A, k) at sigma = SLICE_SIGMA
  sliceAs   2D slice in (A, sigma) at k = SLICE_K
  phase     x0 shifts over one carrier-phase period at points near the slice boundary
  single    single-packet controls for the producing coarse runs
  dxcheck   coarse subset rerun at dx = 0.05
"""
import sys
import json
import time
import numpy as np
from multiprocessing import Pool
from phi4core import (grid, Sim, count_pairs, PERSIST_FRACS, M_KINK, free_quanta)

WSP = 50.0
GMAX = 1.0
CFL = 0.4
TWO_M = 2.0 * M_KINK

A_COARSE = np.round(np.arange(0.1, 1.5001, 0.1), 3)
S_COARSE = np.array([1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0, 12.0, 16.0])
K_COARSE = np.array([0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 2.5, 3.0])


def gauss_initial(x, A, sigma, k, x0, single=False, dphase=0.0):
    w = np.sqrt(k * k + 2.0)
    yl = x + x0
    yr = x - x0
    Gl = np.exp(-yl ** 2 / (2 * sigma ** 2))
    Gr = np.exp(-yr ** 2 / (2 * sigma ** 2))
    phi = -1.0 + A * Gl * np.cos(k * yl + dphase)
    pi = A * w * Gl * np.sin(k * yl + dphase)
    if not single:
        phi += A * Gr * np.cos(k * yr - dphase)
        pi += -A * w * Gr * np.sin(k * yr - dphase)
    return phi, pi


def setup(A, sigma, k, x0_shift=0.0):
    w = np.sqrt(k * k + 2.0)
    vg = k / w
    x0 = 4.0 * sigma + 10.0 + x0_shift
    t_coll = x0 / vg
    T = max(t_coll + 400.0, 1.25 * (t_coll + 100.0))
    Lphys = x0 + 4.0 * sigma + 40.0
    return vg, x0, t_coll, T, Lphys


def run_gauss(A, sigma, k, dx=0.1, single=False, x0_shift=0.0):
    vg, x0, t_coll, T, Lphys = setup(A, sigma, k, x0_shift)
    x = grid(Lphys + WSP, dx)
    phi, pi = gauss_initial(x, A, sigma, k, x0, single=single)
    dt = CFL * dx
    E0 = float(np.sum(_edens(phi, pi, dx)) * dx)
    Eq, Nlin = free_quanta(phi, pi, dx)
    sim = Sim(x, phi, pi, dt, Lphys=Lphys, W=WSP, gmax=GMAX)
    nT = int(round(T / dt))
    nchk = int(round(10.0 / dt))
    marks = sorted(set(range(nchk, nT + 1, nchk)) | {int(round(f * nT)) for f in PERSIST_FRACS})
    tchk, npairs = [0.0], [count_pairs(x, sim.phi)]
    done = 0
    persist = []
    pfr = {int(round(f * nT)) for f in PERSIST_FRACS}
    for m in marks:
        sim.run(m - done)
        done = m
        npp = count_pairs(x, sim.phi)
        if m % nchk == 0:
            tchk.append(m * dt)
            npairs.append(npp)
        if m in pfr:
            persist.append(npp)
    produced = all(n >= 1 for n in persist)
    npairs = np.array(npairs)
    first = None
    if produced:
        j = len(npairs) - 1
        while j > 0 and npairs[j - 1] >= 1:
            j -= 1
        first = float(tchk[j])
    return {"A": A, "sigma": sigma, "k": k, "vg": vg, "x0": x0, "t_coll": t_coll, "T": T,
            "dx": dx, "single": single, "E": E0, "E_over_2M": E0 / TWO_M,
            "E_quad": Eq, "N_lin": Nlin, "produced": bool(produced),
            "n_pairs_T": int(persist[-1]), "npairs_persist": persist,
            "pair_since": first, "max_pairs_seen": int(npairs.max()),
            "phi0_init_max": float(phi.max())}


def _edens(phi, pi, dx):
    from phi4core import energy_density
    return energy_density(phi, pi, dx, -1.0, -1.0)


def _job(a):
    A, s, k, dx, single, sh = a
    return run_gauss(A, s, k, dx, single, sh)


def run_jobs(jobs, nproc, tag):
    t0 = time.time()
    jobs = sorted(jobs, key=lambda j: -setup(j[0], j[1], j[2])[3] * setup(j[0], j[1], j[2])[4] / j[3] ** 2)
    res = []
    with Pool(nproc) as pool:
        for i, r in enumerate(pool.imap_unordered(_job, jobs, chunksize=4)):
            r["x0_shift"] = 0.0
            res.append(r)
            if (i + 1) % 200 == 0:
                print(f"[{tag}] {i + 1}/{len(jobs)} {time.time() - t0:.0f} s", flush=True)
    return res, time.time() - t0


SLICE_SIGMA = None   # set from the coarse scan, rule in REPORT.md
SLICE_K = None

if __name__ == "__main__":
    mode = sys.argv[1]
    nproc = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    extra = sys.argv[3:]
    if mode == "coarse":
        jobs = [(float(A), float(s), float(k), 0.1, False, 0.0)
                for A in A_COARSE for s in S_COARSE for k in K_COARSE]
    elif mode == "sliceAk":
        sig = float(extra[0])
        As = np.round(np.linspace(0.05, 1.5, 59), 4)      # step 0.025
        ks = np.round(np.linspace(0.2, 3.0, 57), 4)       # step 0.05
        jobs = [(float(A), sig, float(k), 0.1, False, 0.0) for A in As for k in ks]
    elif mode == "sliceAs":
        kk = float(extra[0])
        As = np.round(np.linspace(0.05, 1.5, 59), 4)
        ss = np.round(np.exp(np.linspace(np.log(1.0), np.log(16.0), 57)), 4)
        jobs = [(float(A), float(s), kk, 0.1, False, 0.0) for A in As for s in ss]
    elif mode == "single":
        src = json.load(open("e1d_coarse.json"))["runs"]
        jobs = [(r["A"], r["sigma"], r["k"], 0.1, True, 0.0) for r in src if r["produced"]]
    elif mode == "dxcheck":
        rng = np.random.default_rng(12345)
        src = json.load(open("e1d_coarse.json"))["runs"]
        src = [r for r in src if r["E_over_2M"] > 1.0]
        pick = rng.choice(len(src), size=min(300, len(src)), replace=False)
        jobs = [(src[i]["A"], src[i]["sigma"], src[i]["k"], 0.05, False, 0.0) for i in sorted(pick)]
    elif mode == "phase":
        # points of the (A,k) slice adjacent to a production change, x0 shifted over one
        # carrier-phase period 2 pi k / m^2 in 8 steps (collision phase psi = -x0 m^2 / k)
        sl = json.load(open(extra[0]))["runs"]
        rng = np.random.default_rng(2026)
        key = {(r["A"], r["k"]): r for r in sl}
        As = sorted(set(r["A"] for r in sl))
        ks = sorted(set(r["k"] for r in sl))
        bnd = []
        for i, A in enumerate(As):
            for j, k in enumerate(ks):
                p = key[(A, k)]["produced"]
                nb = [key[(As[ii], ks[jj])]["produced"] for ii, jj in
                      ((i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1))
                      if 0 <= ii < len(As) and 0 <= jj < len(ks)]
                if any(q != p for q in nb):
                    bnd.append((A, k))
        sel = [bnd[i] for i in sorted(rng.choice(len(bnd), size=min(60, len(bnd)), replace=False))]
        sig = sl[0]["sigma"]
        jobs = []
        for A, k in sel:
            per = 2 * np.pi * k / 2.0
            for q in range(8):
                jobs.append((A, sig, k, 0.1, False, float(q * per / 8)))
    else:
        raise SystemExit("unknown mode")
    t0 = time.time()
    if mode == "phase":
        res = []
        with Pool(nproc) as pool:
            for r, j in zip(pool.imap(_job, jobs, chunksize=4), jobs):
                r["x0_shift"] = j[5]
                res.append(r)
        dt_run = time.time() - t0
    else:
        res, dt_run = run_jobs(jobs, nproc, mode)
    tag = mode + ("_" + "_".join(extra) if extra and mode != "phase" else "")
    json.dump({"mode": mode, "args": extra, "runs": res, "runtime_s": dt_run},
              open(f"e1d_{tag}.json", "w"), indent=1)
    npro = sum(r["produced"] for r in res)
    print(f"[{tag}] {len(res)} runs, {npro} producing, {dt_run:.0f} s")
