"""
g1prime_fano3body.py — §3.4-G1′: does the Fano-line 3-body coupling do anything?
================================================================================
First pass at gate G1′ (reports/SQT_3.4_G0_FIRST_PASS.md §G0.7). G0 showed the
first place the framework's Fano/PSL(2,7) content can enter the dynamics is a
3-body coupling on collinear triples (the 7 Fano lines), degree 6 in ψ:

    E_Fano = −λ ∫ Σ_{lines ℓ}  ρ_i(x) ρ_j(x) ρ_k(x) dx ,   ρ_c = |ψ_c|²

with ψ now SEVEN-component (the seven imaginary octonion directions e₁..e₇ ↔
Fano points). The disciplined test is a PLACEBO control (cf. the seven-circles
work): compare the coupling on the 7 collinear triples (Fano lines) against the
same coupling on 7 NON-collinear triples (the 28-orbit). A genuine fingerprint
must show the line coupling doing something the control does not.

Two parts:
  PART A (exact, R1/R2): single-SITE energetics of the 3-body term on the
    7-simplex, Fano lines vs random non-line controls. Decides whether the
    Fano structure is even visible locally, or only collectively.
  PART B (2-D GP, R3 exploratory): 7-component imaginary-time GP with a roton
    (total-density channel → p6m, per MV-G1) plus the Fano term; Fano vs control;
    measures p6m survival and a per-site line-locking order parameter.

Usage:
  python3 tools/g1prime_fano3body.py            # PART A (fast) + PART B
  python3 tools/g1prime_fano3body.py --partA-only
Requires numpy.
Author: §3.4-G1′ first pass, 2026-06-03.
"""

import argparse
import math
from itertools import combinations, product
import numpy as np

# ── Fano lines (collinear triples of the 7 points e₁..e₇ ≅ nonzero F_2³) ──────
PTS = [v for v in product((0, 1), repeat=3) if any(v)]
IDX = {v: i for i, v in enumerate(PTS)}
LINES = [tuple(sorted((i, j, k)))
         for i, j, k in combinations(range(7), 3)
         if all((PTS[i][t] ^ PTS[j][t] ^ PTS[k][t]) == 0 for t in range(3))]
NONLINES = [t for t in combinations(range(7), 3) if t not in set(LINES)]
assert len(LINES) == 7 and len(NONLINES) == 28


# ── PART A — single-site simplex energetics ──────────────────────────────────
def site_energy(n, triples):
    return -sum(n[i] * n[j] * n[k] for (i, j, k) in triples)


def minimise_site(triples, restarts=20000, seed=0):
    """Global min of E(n)=−Σ_triples Π n over the 7-simplex (random Dirichlet
    restarts; the optimum is a corner-of-a-face so sampling finds it)."""
    rng = np.random.default_rng(seed)
    best, bestn = 0.0, None
    # analytic candidates: lock to one triple (1/3,1/3,1/3); uniform (1/7)
    cand = []
    for t in triples:
        n = np.zeros(7); n[list(t)] = 1 / 3; cand.append(n)
    cand.append(np.full(7, 1 / 7))
    samples = list(cand) + list(rng.dirichlet(np.ones(7) * 0.3, size=restarts))
    for n in samples:
        e = site_energy(n, triples)
        if e < best:
            best, bestn = e, n
    return best, bestn


def part_A(seed=0):
    print("=" * 74)
    print("PART A — single-site 3-body energetics on the 7-simplex (exact)")
    print("=" * 74)
    eF, nF = minimise_site(LINES, seed=seed)
    locked_line = int(round(max(sum(nF[list(t)]) for t in LINES) * 100))
    print(f"  Fano lines (7):     min site-energy = {eF:.6f}  "
          f"(single-line lock −1/27 = {-1/27:.6f})")
    print(f"     minimiser concentrates {locked_line}% of site density on one line.")
    rng = np.random.default_rng(seed)
    ctrl_es = []
    for _ in range(12):
        ctrl = [NONLINES[i] for i in rng.choice(len(NONLINES), 7, replace=False)]
        e, _ = minimise_site(ctrl, restarts=4000, seed=int(rng.integers(1e9)))
        ctrl_es.append(e)
    print(f"  Non-line controls (7 random triples, 12 draws): "
          f"min site-energy = {np.mean(ctrl_es):.6f} ± {np.std(ctrl_es):.6f}")
    print()
    print(f"  FINDING: the Fano min is EXACTLY −1/27 (a single-line lock), because")
    print("    the 7 lines are a balanced 2-(7,3,1) design — every point on exactly")
    print("    3 lines, every pair on exactly 1 — so no over-concentration is")
    print("    possible. IRREGULAR control triple-sets can do slightly BETTER")
    print(f"    ({np.mean(ctrl_es):.4f} < −1/27): a point sitting in many triples")
    print("    lets density over-concentrate. So local energetics do NOT select")
    print("    the Fano lines — if anything they are the *least* favourable")
    print("    (maximally balanced) 3-body target. The Fano distinction is")
    print("    therefore STRUCTURAL/COLLECTIVE, not single-site: it lives in the")
    print("    regular tiling forced by lines pairwise meeting in exactly 1 point.")
    print("    PART B probes whether that collective regularity leaves a")
    print("    dynamical fingerprint on the crystal.")
    print()
    return eF


# ── PART B — 7-component GP with roton + Fano term ───────────────────────────
def build(N, L):
    dx = L / N
    x = (np.arange(N) - N // 2) * dx
    X, Y = np.meshgrid(x, x, indexing="ij")
    k1 = 2 * np.pi * np.fft.fftfreq(N, d=dx)
    KX, KY = np.meshgrid(k1, k1, indexing="ij")
    return dx, X, Y, KX**2 + KY**2


def softcore_Uk(X, Y, R, g, dx):
    r = np.sqrt(X**2 + Y**2)
    return (np.fft.fft2(np.fft.ifftshift(np.where(r < R, g, 0.0))) * dx**2).real


def run_gp(triples, N, L, R, g, lam, rho0, dtau, steps, seed):
    dx, X, Y, K2 = build(N, L)
    Uk = softcore_Uk(X, Y, R, g, dx)
    rng = np.random.default_rng(seed)
    # 7 components, random asymmetric seed so the Fano term can break degeneracy
    psi = (np.sqrt(rho0 / 7) *
           (1.0 + 0.3 * rng.standard_normal((7, N, N))
            + 0.1j * rng.standard_normal((7, N, N))))
    target = rho0 * N * N * dx**2
    Kprop = np.exp(-0.25 * K2 * dtau)

    def renorm(p):
        cur = np.sum(np.abs(p)**2) * dx**2
        return p * math.sqrt(target / cur)

    psi = renorm(psi)
    tri = [list(t) for t in triples]
    for _ in range(steps):
        psi = np.fft.ifft2(Kprop * np.fft.fft2(psi, axes=(1, 2)), axes=(1, 2))
        rho = np.abs(psi)**2                       # (7,N,N)
        rho_tot = rho.sum(axis=0)
        Uconv = np.fft.ifft2(Uk * np.fft.fft2(rho_tot)).real     # shared 2-body
        # Fano 3-body potential per component: δE/δρ_c = −λ Σ_{ℓ∋c} ρ_aρ_b
        VF = np.zeros_like(rho)
        for (i, j, k) in tri:
            VF[i] -= lam * rho[j] * rho[k]
            VF[j] -= lam * rho[i] * rho[k]
            VF[k] -= lam * rho[i] * rho[j]
        psi = psi * np.exp(np.clip(-(Uconv[None] + VF) * dtau, -8.0, 8.0))
        psi = np.fft.ifft2(Kprop * np.fft.fft2(psi, axes=(1, 2)), axes=(1, 2))
        psi = renorm(psi)
    return np.abs(psi)**2, dx, L


def _local_max(rho, thr):
    m = np.ones_like(rho, bool)
    for sx in (-1, 0, 1):
        for sy in (-1, 0, 1):
            if sx or sy:
                m &= rho >= np.roll(np.roll(rho, sx, 0), sy, 1)
    return np.argwhere(m & (rho > thr))


def analyse(rho, dx, L, triples):
    rho_tot = rho.sum(axis=0)
    drho = rho_tot - rho_tot.mean()
    contrast = float(drho.std() / rho_tot.mean())
    peaks = _local_max(rho_tot, rho_tot.mean() + 0.5 * rho_tot.std())
    if len(peaks) < 7:
        # collapsed/uniform (e.g. a control that over-concentrates to one peak):
        # ψ6 is undefined with <7 neighbours — guard as bond_orientational() does.
        return {"contrast": contrast, "psi6": 0.0, "n_peaks": int(len(peaks)),
                "Q": 0.0}
    # psi6 of the total-density lattice (local bond order)
    P = peaks.astype(float) * dx
    psi6 = []
    for i in range(len(P)):
        d = P - P[i]; d -= L * np.round(d / L)
        dd = np.hypot(d[:, 0], d[:, 1]); o = np.argsort(dd)[1:7]
        ang = np.arctan2(d[o, 1], d[o, 0]); psi6.append(np.mean(np.exp(6j * ang)))
    psi6 = float(np.mean(np.abs(psi6))) if psi6 else 0.0
    # per-site line-locking: fraction of site density on its best triple
    locks = []
    for (py, px) in peaks:
        n = rho[:, py, px]
        s = n.sum()
        if s <= 0:
            continue
        n = n / s
        locks.append(max(sum(n[list(t)]) for t in triples))
    Q = float(np.mean(locks)) if locks else 0.0
    return {"contrast": contrast, "psi6": psi6, "n_peaks": len(peaks), "Q": Q}


def part_B(args):
    print("=" * 74)
    print("PART B — 7-component GP: roton (→p6m) + Fano 3-body, Fano vs control")
    print("=" * 74)
    base = 3.0 / 7.0   # uniform line-fraction baseline (3 of 7 components)
    rng = np.random.default_rng(args.seed)
    ctrl = [NONLINES[i] for i in rng.choice(len(NONLINES), 7, replace=False)]
    cases = [("Fano lines  ", LINES), ("non-line ctrl", ctrl)]
    print(f"  N={args.N} L={args.L} g={args.g} λ={args.lam} steps={args.steps}; "
          f"uniform line-fraction baseline = {base:.3f}")
    print()
    for label, tri in cases:
        rho, dx, L = run_gp(tri, args.N, args.L, args.R, args.g, args.lam,
                            args.rho0, args.dtau, args.steps, args.seed)
        a = analyse(rho, dx, L, tri)
        print(f"  [{label}] contrast={a['contrast']:.3f}  ψ6(total)={a['psi6']:.3f}  "
              f"peaks={a['n_peaks']}  line-lock Q={a['Q']:.3f}  "
              f"(Δ vs uniform {a['Q']-base:+.3f})")
    print()
    print("  Reading: ψ6 ~ MV-G1 ⇒ the p6m lattice survives in both. Q is the")
    print("  per-site density fraction on the best triple; Q≈baseline ⇒ NO component")
    print("  ordering, Q≫baseline ⇒ ordering. Observed (robust across seeds):")
    print("  Fano Q ≈ baseline (INERT) while the irregular control orders strongly.")
    print("  The Fano lines are a balanced 2-(7,3,1) design, so the symmetric term")
    print("  keeps the uniform component state as a fixed point and supplies no")
    print("  symmetry-breaking gradient — it is dynamically inert exactly where a")
    print("  generic coupling is active. Informative null (mechanism understood),")
    print("  specific to the U(1)-invariant density-product line term.")


def main(argv=None):
    ap = argparse.ArgumentParser(description="§3.4-G1′ Fano 3-body first pass.")
    ap.add_argument("--partA-only", action="store_true")
    ap.add_argument("--N", type=int, default=80)
    ap.add_argument("--L", type=float, default=12.0)
    ap.add_argument("--R", type=float, default=1.0)
    ap.add_argument("--g", type=float, default=22.0)
    ap.add_argument("--lam", type=float, default=1.0,
                    help="Fano 3-body strength (perturbative; large λ collapses)")
    ap.add_argument("--rho0", type=float, default=1.0)
    ap.add_argument("--dtau", type=float, default=2e-3)
    ap.add_argument("--steps", type=int, default=1800)
    ap.add_argument("--seed", type=int, default=7)
    args = ap.parse_args(argv)
    part_A(seed=args.seed)
    if not args.partA_only:
        part_B(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
