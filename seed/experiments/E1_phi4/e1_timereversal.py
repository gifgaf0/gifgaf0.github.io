"""Seed section 2 reconciliation: can pair-free initial data make a pair with E just above 2 M_kink?

Argument (cross-check; also stated in DSV 2008, arXiv:0803.0670, p. 1): the phi^4 equation is
time-reversal invariant. A slow kink-antikink pair (v << v_c, E = 2 M gamma(v)) is captured,
and the bound state radiates. Reversing all velocities at a late time Tf gives initial data
with no kink (phi < 0 everywhere) and energy 2 M gamma(v), which evolves back into an outgoing
pair. So the classical infimum of the production energy over all initial data is 2 M.

This script demonstrates it on the lattice of phi4core.py (dx = 0.1, dt = 0.04, no absorbing
layer, box large enough that no radiation reaches the ends before 2 Tf):
  1. evolve kk_initial(v, x0 = 10) forward; Tf = first time after which max phi < 0 has held
     for 100 time units (bound state no longer reaches the barrier top);
  2. reverse velocities at Tf, check the data contain no pair and no zero of phi, record E/2M;
  3. evolve forward Tf with (a) the same dt (exact reversal up to round-off) and (b) dt/2 and
     dt/4 (not an exact inverse of the forward run), and test for an outgoing pair;
  4. fine-tuning probes: reversed data with radiation beyond |x| > R removed (phi = -1, pi = 0,
     cosine taper of width 20), and with relative noise added.
Writes e1_timereversal.json.
"""
import json
import time
import numpy as np
from phi4core import grid, Sim, kk_initial, count_pairs, positive_intervals, M_KINK

DX, DT, X0 = 0.1, 0.04, 10.0
TWO_M = 2 * M_KINK
rng = np.random.default_rng(7)


def forward_until_quiet(v, tmax, quiet=100.0):
    L = tmax + 200.0
    x = grid(L, DX)
    phi, pi = kk_initial(x, v, X0)
    sim = Sim(x, phi, pi, DT)
    E0 = sim.energy()
    nchunk = int(round(1.0 / DT))
    last_pos = 0.0
    hist = []
    while sim.t < tmax - 1e-9:
        sim.run(nchunk)
        mx = float(sim.phi.max())
        hist.append(round(mx, 4))
        if mx >= 0.0:
            last_pos = sim.t
        elif sim.t - last_pos >= quiet:
            break
    return x, sim, E0, last_pos, hist


def reverse_run(x, phi, pi, t_run, dt):
    sim = Sim(x, phi, pi, dt)
    E = sim.energy()
    n = int(round(t_run / dt))
    sim.run(n)
    ivs = [iv for iv in positive_intervals(x, sim.phi) if iv[1] - iv[0] > 1.0]
    return {"dt": dt, "E_over_2M": E / TWO_M, "n_pairs_end": count_pairs(x, sim.phi),
            "intervals_end": [[round(a, 3), round(b, 3), round(f, 3), round(m, 3)] for a, b, f, m in ivs][:5]}, sim


def taper(x, R, w=20.0):
    ax = np.abs(x)
    f = np.ones_like(x)
    m = (ax > R) & (ax < R + w)
    f[m] = 0.5 * (1 + np.cos(np.pi * (ax[m] - R) / w))
    f[ax >= R + w] = 0.0
    return f


out = {"dx": DX, "dt": DT, "x0": X0, "cases": []}
t_start = time.time()
for v in (0.1, 0.05):
    x, sim, E0, last_pos, hist = forward_until_quiet(v, tmax=4000.0)
    Tf = sim.t
    case = {"v": v, "gamma": 1 / np.sqrt(1 - v * v), "E_initial_over_2M": E0 / TWO_M,
            "last_time_phi_max_ge_0": last_pos, "Tf": Tf,
            "max_phi_last_100": float(max(hist[-100:])) if len(hist) >= 100 else None}
    phiR, piR = sim.phi.copy(), -sim.pi.copy()
    case["reversed_data"] = {"max_phi": float(phiR.max()), "n_positive_intervals": len(positive_intervals(x, phiR)),
                             "n_pairs": count_pairs(x, phiR), "E_over_2M": Sim(x, phiR, piR, DT).energy() / TWO_M,
                             "energy_within_|x|<50_over_2M": None}
    e_dens_mask = np.abs(x) < 50
    case["reversed_data"]["energy_within_|x|<50_over_2M"] = Sim(x, phiR, piR, DT).energy(mask=e_dens_mask) / TWO_M
    phi_init, _ = kk_initial(x, v, X0)
    runs = []
    for dt in (DT, DT / 2, DT / 4):
        r, s2 = reverse_run(x, phiR, piR, Tf, dt)
        r["max_abs_diff_vs_initial_kk"] = float(np.max(np.abs(s2.phi - phi_init)))
        runs.append(r)
    case["reverse_evolution"] = runs
    probes = []
    for R in (0.75 * Tf, 0.5 * Tf, 0.25 * Tf):
        f = taper(x, R)
        p_, q_ = -1.0 + f * (phiR + 1.0), f * piR
        r, _ = reverse_run(x, p_, q_, Tf, DT)
        r["probe"] = f"radiation beyond |x| > {R:.0f} removed"
        probes.append(r)
    for eps in (1e-8, 1e-5, 1e-3):
        p_ = phiR + eps * rng.standard_normal(x.size) * (np.abs(x) < 50.0)
        r, _ = reverse_run(x, p_, piR, Tf, DT)
        r["probe"] = f"white noise of amplitude {eps:g} added to phi for |x| < 50"
        probes.append(r)
    case["fine_tuning_probes"] = probes
    out["cases"].append(case)
    print(json.dumps(case, indent=1), flush=True)
out["runtime_s"] = time.time() - t_start
json.dump(out, open("e1_timereversal.json", "w"), indent=1, default=float)
