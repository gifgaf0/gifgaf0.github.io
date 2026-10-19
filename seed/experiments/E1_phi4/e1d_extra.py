"""E1d robustness runs added by the resumed run (not preregistered). Resumable: every finished run
is appended to a .jsonl checkpoint, and finished runs are skipped on restart.

Modes
  coarse_oneway   the coarse 3D grid of e1d_gauss.py with one-way initial velocity: phi(x,0) is the
                  same Gaussian x cosine, and every Fourier component of each packet is given the
                  velocity of a free wave moving toward the centre,
                    phi_t = Re IFFT[ -i w_q 2 Theta(+-q) FFT(packet) ],  w_q = sqrt(q^2 + 2),
                  so each packet is an exact solution of the linearised equation moving one way.
                  (The baseline uses the narrow-band form phi_t = +-A w_k G sin(.), which for
                  k sigma ~ 1 also launches part of each packet outward.)
  single_oneway   the right-moving packet alone, for every producing coarse_oneway point.
  slice_dx05      the (A, sigma) slice at k = 1 (same 59 x 57 grid as e1d_sliceAs_1.0.json) at
                  dx = 0.05, dt = 0.02 (baseline dx = 0.1, dt = 0.04), narrow-band initial data.
  slice_dx05_single  single-packet controls at dx = 0.05 for the producing slice_dx05 points.
All other rules (x0, T, box, absorbing layer, pair test) are those of e1d_gauss.py.
Usage: python e1d_extra.py <mode> [nproc]   ->  e1d_<mode>.jsonl
"""
import sys
import json
import os
import time
import numpy as np
from multiprocessing import Pool
import e1d_gauss as G
from phi4core import grid, Sim, count_pairs, PERSIST_FRACS, energy_density, free_quanta

TWO_M = G.TWO_M


def oneway_initial(x, A, sigma, k, x0, single=False):
    dx = x[1] - x[0]
    q = 2 * np.pi * np.fft.fftfreq(x.size, d=dx)
    w = np.sqrt(q * q + 2.0)
    yl = x + x0
    pr = A * np.exp(-yl ** 2 / (2 * sigma ** 2)) * np.cos(k * yl)       # right-mover at -x0
    phi = -1.0 + pr
    th = np.where(q > 0, 1.0, np.where(q == 0, 0.5, 0.0))
    pi = np.real(np.fft.ifft(-1j * w * 2.0 * th * np.fft.fft(pr)))
    if not single:
        yr = x - x0
        pl = A * np.exp(-yr ** 2 / (2 * sigma ** 2)) * np.cos(k * yr)    # left-mover at +x0
        phi = phi + pl
        thl = np.where(q < 0, 1.0, np.where(q == 0, 0.5, 0.0))
        pi = pi + np.real(np.fft.ifft(-1j * w * 2.0 * thl * np.fft.fft(pl)))
    return phi, pi


def run_custom(A, sigma, k, dx=0.1, single=False, oneway=False):
    vg, x0, t_coll, T, Lphys = G.setup(A, sigma, k)
    x = grid(Lphys + G.WSP, dx)
    if oneway:
        phi, pi = oneway_initial(x, A, sigma, k, x0, single=single)
    else:
        phi, pi = G.gauss_initial(x, A, sigma, k, x0, single=single)
    dt = G.CFL * dx
    E0 = float(np.sum(energy_density(phi, pi, dx, -1.0, -1.0)) * dx)
    Eq, Nlin = free_quanta(phi, pi, dx)
    sim = Sim(x, phi, pi, dt, Lphys=Lphys, W=G.WSP, gmax=G.GMAX)
    nT = int(round(T / dt))
    marks = sorted({int(round(f * nT)) for f in PERSIST_FRACS})
    done, persist = 0, []
    for m in marks:
        sim.run(m - done)
        done = m
        persist.append(count_pairs(x, sim.phi))
    return {"A": A, "sigma": sigma, "k": k, "vg": vg, "dx": dx, "single": single, "oneway": oneway,
            "E": E0, "E_over_2M": E0 / TWO_M, "N_lin": Nlin, "produced": bool(all(n >= 1 for n in persist)),
            "npairs_persist": persist}


def _job(a):
    return run_custom(*a)


def main(mode, nproc):
    out = f"e1d_{mode}.jsonl"
    if mode == "coarse_oneway":
        jobs = [(float(A), float(s), float(k), 0.1, False, True)
                for A in G.A_COARSE for s in G.S_COARSE for k in G.K_COARSE]
    elif mode == "single_oneway":
        src = [json.loads(l) for l in open("e1d_coarse_oneway.jsonl")]
        jobs = [(r["A"], r["sigma"], r["k"], 0.1, True, True) for r in src if r["produced"]]
    elif mode == "slice_dx05":
        As = np.round(np.linspace(0.05, 1.5, 59), 4)
        ss = np.round(np.exp(np.linspace(np.log(1.0), np.log(16.0), 57)), 4)
        jobs = [(float(A), float(s), 1.0, 0.05, False, False) for A in As for s in ss]
    elif mode == "slice_dx05_single":
        src = [json.loads(l) for l in open("e1d_slice_dx05.jsonl")]
        jobs = [(r["A"], r["sigma"], r["k"], 0.05, True, False) for r in src if r["produced"]]
    else:
        raise SystemExit("unknown mode")
    done = set()
    if os.path.exists(out):
        for l in open(out):
            try:
                r = json.loads(l)
            except json.JSONDecodeError:
                continue
            done.add((r["A"], r["sigma"], r["k"]))
    todo = [j for j in jobs if (j[0], j[1], j[2]) not in done]
    # longest first (cost ~ T * box / dx^2)
    todo.sort(key=lambda j: -G.setup(j[0], j[1], j[2])[3] * G.setup(j[0], j[1], j[2])[4])
    print(f"[{mode}] {len(jobs)} jobs, {len(done)} already done, {len(todo)} to run", flush=True)
    t0 = time.time()
    with Pool(nproc) as pool, open(out, "a") as f:
        for i, r in enumerate(pool.imap_unordered(_job, todo, chunksize=2)):
            f.write(json.dumps(r) + "\n")
            f.flush()
            if (i + 1) % 100 == 0:
                print(f"[{mode}] {i + 1}/{len(todo)} {time.time() - t0:.0f} s", flush=True)
    rs = [json.loads(l) for l in open(out)]
    print(f"[{mode}] complete: {len(rs)} runs, {sum(r['produced'] for r in rs)} producing, "
          f"{time.time() - t0:.0f} s this session", flush=True)


if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 2)
