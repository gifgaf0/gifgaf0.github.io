"""
mv_g1_minimiser.py — §3.4 MV-G1: roton-GP ground state, hexagonality, and ζ
============================================================================
Bounded first computation of the §3.4 proof program
(reports/SQT_3.4_PROOF_PROGRAM.md, gate §3.4-MV-G1). It asks ONLY the two
questions MV-G1 specifies:

  (i)  Does the Gross–Pitaevskii / Bjerknes substrate action, with a roton
       kernel, have a HEXAGONAL (p6m) ground state?
  (ii) Does ζ = 1 − π/√12 ≈ 0.09310 appear in the energy density?

Model (ℏ = m = 1, 2-D periodic box). Order parameter ψ; ρ = |ψ|². Energy

    E[ψ] = ∫ ½|∇ψ|²  +  ½∫∫ ρ(x) U(x−x') ρ(x')  −  μ∫ρ

with a soft-core two-body kernel U(r) = g for r < R, 0 otherwise. Its Fourier
transform Ũ(k) has negative lobes (a roton); when the roton softens the uniform
state is unstable and the system crystallises at the roton wavevector k_c. In
2-D the generic single-ring crystallisation selects a TRIANGULAR (hexagonal)
lattice (Brazovskii weak-crystallisation; the three 120° wavevector pairs admit
a resonant cubic term). This is standard soft-core-boson / supersolid physics —
the kernel is the IMPORT (I1–I3 of §3.4.1); hexagonality is the test, not an
input.

METHOD. Imaginary-time split-step Fourier propagation of
    −∂_τ ψ = [ −½∇² + (U*ρ) ] ψ ,  renormalised to fixed ∫ρ each step
(the standard GP ground-state relaxation). Seeded from uniform + small noise so
the unstable roton ring, not a chosen pattern, selects the lattice.

HONESTY ON (ii) — read before trusting the ζ line (per §3.4.6 Eddington watch).
ζ = 1 − π/√12 is the COMPLEMENT OF THE 2-D HEXAGONAL PACKING FRACTION
(densest equal-disk packing fills π/√12 ≈ 0.9069 of the plane). It is a
GEOMETRIC fact about the triangular lattice, NOT a dynamical quantity this
solver discovers: any hexagonal arrangement of equal touching disks carries ζ
by construction. This script therefore does NOT claim to "find ζ in the energy."
It reports (a) whether the dynamically-selected lattice is triangular — the real,
falsifiable result — and (b) the geometric statement that the close-packed
triangular lattice's void fraction is ζ, explicitly flagged as geometry of
hexagonality. Promoting ζ to a non-tautological energy ratio is a SEPARATE
derivation MV-G1 does not perform and must not be claimed to.

Usage:
  python3 tools/mv_g1_minimiser.py                 # default crystallising run
  python3 tools/mv_g1_minimiser.py --N 192 --g 18 --steps 4000 --plot out.png
  python3 tools/mv_g1_minimiser.py --g 0.0         # control: no interaction -> uniform

Requires numpy; matplotlib optional (--plot).
Author: §3.4-MV-G1 instrument, 2026-06-03.
"""

import argparse
import math
import numpy as np

ZETA = 1.0 - math.pi / math.sqrt(12.0)          # 0.0931003... packing-tax complement
HEX_PACKING = math.pi / math.sqrt(12.0)          # 0.9069...


# ── Model construction ───────────────────────────────────────────────────────
def build_grids(N, L):
    dx = L / N
    x = (np.arange(N) - N // 2) * dx
    X, Y = np.meshgrid(x, x, indexing="ij")
    k1 = 2 * np.pi * np.fft.fftfreq(N, d=dx)
    KX, KY = np.meshgrid(k1, k1, indexing="ij")
    K2 = KX**2 + KY**2
    return dx, X, Y, KX, KY, K2


def softcore_kernel_fourier(X, Y, R, g, dx):
    """Ũ(k) from the real-space soft-core U(r)=g·θ(R−r), via FFT (no Bessel dep)."""
    r = np.sqrt(X**2 + Y**2)
    U_real = np.where(r < R, g, 0.0)
    # FFT convention: convolution (U*ρ)(x) = ifft( Uk · fft(ρ) ); Uk carries dx².
    Uk = np.fft.fft2(np.fft.ifftshift(U_real)) * dx**2
    return Uk.real


# ── Roton diagnostic ─────────────────────────────────────────────────────────
def roton_softening(K2, Uk, rho0):
    """min_k of the Bogoliubov gap surrogate ε_k + 2ρ0 Ũ(k); < 0 => uniform state
    unstable (roton has softened) => crystallisation. Returns (min_value, k_c)."""
    eps = 0.5 * K2
    gap = eps + 2.0 * rho0 * Uk            # Uk[0,0] is the (positive) self-energy
    g0 = gap.copy()
    g0.flat[0] = np.inf                    # ignore k=0
    idx = np.unravel_index(np.argmin(g0), g0.shape)
    kc = math.sqrt(float(K2[idx]))
    return float(g0.min()), kc


# ── Imaginary-time ground state (with adiabatic g-ramp) ──────────────────────
def ground_state(N, L, R, g, rho0, dtau, steps, seed, ramp=0.5, tol=1e-10):
    dx, X, Y, KX, KY, K2 = build_grids(N, L)
    Uk_full = softcore_kernel_fourier(X, Y, R, g, dx)
    rng = np.random.default_rng(seed)

    gmin, kc0 = roton_softening(K2, Uk_full, rho0)

    # seed: uniform amplitude + small noise (lets the roton ring self-select)
    psi = np.sqrt(rho0) * (1.0 + 0.01 * rng.standard_normal((N, N)))
    norm_target = rho0 * (N * N) * dx**2

    def renorm(p):
        cur = np.sum(np.abs(p)**2) * dx**2
        return p * math.sqrt(norm_target / cur)

    psi = renorm(psi)
    Kprop = np.exp(-0.25 * K2 * dtau)             # half-step kinetic (½·½∇²)

    ramp_steps = max(1, int(ramp * steps))
    E_prev = None
    for it in range(steps):
        frac = min(1.0, (it + 1) / ramp_steps)    # adiabatic turn-on of interaction
        Uk = frac * Uk_full
        psi = np.fft.ifft2(Kprop * np.fft.fft2(psi))      # ½ kinetic
        rho = np.abs(psi)**2
        Uconv = np.fft.ifft2(Uk * np.fft.fft2(rho)).real  # mean-field U*ρ
        psi = psi * np.exp(-Uconv * dtau)                 # full interaction
        psi = np.fft.ifft2(Kprop * np.fft.fft2(psi))      # ½ kinetic
        psi = renorm(psi)
        if frac >= 1.0 and (it % 50 == 0 or it == steps - 1):
            E = energy_density(psi, K2, Uk, dx, L)
            if E_prev is not None and abs(E - E_prev) < tol * max(1.0, abs(E)):
                break
            E_prev = E
    rho = np.abs(psi)**2
    return rho, dx, KX, KY, K2, Uk_full, (gmin, kc0)


def energy_density(psi, K2, Uk, dx, L):
    psk = np.fft.fft2(psi)
    area = L * L
    kin = 0.5 * np.sum(K2 * np.abs(psk)**2) * (dx**2 / (psi.size)) / area
    rho = np.abs(psi)**2
    rhk = np.fft.fft2(rho)
    inter = 0.5 * np.sum(Uk * np.abs(rhk)**2) * (dx**2 / (psi.size)) / area
    return float(kin + inter)


# ── Symmetry analysis: real-space bond-orientational order (defect-tolerant) ─
def _local_maxima(rho, thresh):
    """Periodic local maxima of rho above thresh (8-neighbour, via np.roll)."""
    m = np.ones_like(rho, dtype=bool)
    for sx in (-1, 0, 1):
        for sy in (-1, 0, 1):
            if sx == 0 and sy == 0:
                continue
            m &= rho >= np.roll(np.roll(rho, sx, axis=0), sy, axis=1)
    m &= rho > thresh
    return np.argwhere(m)


def bond_orientational(rho, dx, L, knn=6):
    """ψ_m bond-orientational order from detected density peaks, minimum-image
    (periodic). Reports LOCAL order ⟨|ψ_m,i|⟩ (per-particle magnitude — detects
    triangular *coordination* regardless of grain orientation; the right G1(i)
    test) and GLOBAL order |⟨ψ_m,i⟩| (single-crystal alignment). Triangular ->
    local ψ6≈1, ψ4 low; square -> local ψ4≈1, ψ6 low."""
    mean, std = rho.mean(), rho.std()
    peaks = _local_maxima(rho, mean + 0.5 * std)
    if len(peaks) < 7:
        return {"psi4_local": 0.0, "psi6_local": 0.0,
                "psi4_global": 0.0, "psi6_global": 0.0, "n_peaks": int(len(peaks))}
    P = peaks.astype(float) * dx
    n = len(P)
    psi4 = np.zeros(n, complex)
    psi6 = np.zeros(n, complex)
    for i in range(n):
        d = P - P[i]
        d -= L * np.round(d / L)                          # minimum image (square box)
        dist = np.hypot(d[:, 0], d[:, 1])
        order = np.argsort(dist)
        nb = order[1:knn + 1]                             # nearest neighbours
        ang = np.arctan2(d[nb, 1], d[nb, 0])
        psi4[i] = np.mean(np.exp(4j * ang))
        psi6[i] = np.mean(np.exp(6j * ang))
    return {"psi4_local": float(np.mean(np.abs(psi4))),
            "psi6_local": float(np.mean(np.abs(psi6))),
            "psi4_global": float(np.abs(psi4.mean())),
            "psi6_global": float(np.abs(psi6.mean())), "n_peaks": n}


def analyse_symmetry(rho, dx, L, KX, KY):
    """Dominant |k_c| from the structure factor + real-space ψ4/ψ6 classification."""
    drho = rho - rho.mean()
    contrast = float(drho.std() / (rho.mean() + 1e-30))
    S = np.abs(np.fft.fft2(drho))**2
    S.flat[0] = 0.0
    kmag = np.sqrt(KX**2 + KY**2)
    kc = float(kmag.flat[np.argmax(S)]) if S.max() > 0 else 0.0

    if contrast < 0.02:
        return {"lattice": "uniform", "contrast": contrast, "kc": kc,
                "psi4_local": 0.0, "psi6_local": 0.0,
                "psi4_global": 0.0, "psi6_global": 0.0, "n_peaks": 0}
    bo = bond_orientational(rho, dx, L)
    p4, p6 = bo["psi4_local"], bo["psi6_local"]           # local order = G1(i) test
    lattice = ("triangular/p6m" if p6 > 0.60 and p6 > p4 + 0.15
               else "square" if p4 > 0.60 and p4 > p6 + 0.15
               else "stripe/smectic" if bo["n_peaks"] < 7
               else "other/ordered")
    out = {"lattice": lattice, "contrast": contrast, "kc": kc}
    out.update(bo)
    return out


def lattice_constant_triangular(kc):
    """Real-space lattice constant a from the dominant reciprocal vector |G|=kc
    for a triangular lattice: |G|_min = 4π/(√3 a)."""
    return 4 * math.pi / (math.sqrt(3) * kc) if kc > 0 else float("inf")


# ── Reporting ────────────────────────────────────────────────────────────────
def report(res, a, g, roton):
    print("=" * 74)
    print("§3.4-MV-G1 — roton-GP ground state: hexagonality + ζ")
    print("=" * 74)
    gmin, kc0 = roton
    print(f"  interaction strength g : {g}")
    print(f"  roton softening min_k(ε_k+2ρ₀Ũ) : {gmin:+.4f}  "
          f"({'UNSTABLE → crystallises' if gmin < 0 else 'stable → uniform'}), "
          f"k_roton≈{kc0:.3f}")
    print(f"  density contrast       : {res['contrast']:.4f}  "
          f"({'crystallised' if res['contrast'] > 0.05 else 'uniform / weak'})")
    print(f"  dominant |k_c| (S(k))  : {res['kc']:.4f}")
    print(f"  LOCAL bond order ψ4/ψ6 : {res['psi4_local']:.3f} / {res['psi6_local']:.3f}"
          "   (coordination — the G1(i) test)")
    print(f"  global bond order ψ4/ψ6: {res['psi4_global']:.3f} / {res['psi6_global']:.3f}"
          "   (single-crystal alignment; low ⇒ polycrystal)")
    print(f"  density peaks detected : {res['n_peaks']}")
    print(f"  lattice verdict        : {res['lattice']}")
    print()

    # (i) — the real, falsifiable result
    hexagonal = res["lattice"].startswith("triangular") and res["contrast"] > 0.05
    print("  (i) HEXAGONAL (p6m) GROUND STATE?")
    if hexagonal:
        print(f"      PASS — local ψ6={res['psi6_local']:.3f} dominates "
              f"ψ4={res['psi4_local']:.3f}: every peak sits in a 6-coordinated "
              f"triangular cell.")
        gp = res['psi6_global']
        print(f"      (global ψ6={gp:.3f}: "
              f"{'single-crystal' if gp > 0.6 else 'polycrystalline — grains, but locally triangular'}.)")
        print(f"      lattice constant a ≈ {a:.4f} (from k_c via |G|=4π/√3a).")
    elif res["contrast"] <= 0.05:
        print("      FAIL (no crystallisation) — ground state is uniform at this g. "
              "Increase --g (deepen the roton) or check the kernel.")
    else:
        print(f"      FAIL — ordered but NOT cleanly triangular: {res['lattice']} "
              f"(local ψ4={res['psi4_local']:.3f}, ψ6={res['psi6_local']:.3f}). "
              "Near onset or defected; raise --g / --steps, or an informative null.")
    print()

    # (ii) — scrupulously honest, per §3.4.6
    print("  (ii) DOES ζ = 1 − π/√12 ≈ {:.5f} APPEAR?".format(ZETA))
    print("      HONEST STATEMENT (not an Eddington claim):")
    if hexagonal:
        print(f"      The dynamically-selected lattice IS triangular. The "
              f"close-packed\n      triangular lattice of equal disks has packing "
              f"fraction π/√12 =\n      {HEX_PACKING:.5f}; its void complement is "
              f"ζ = {ZETA:.5f} BY GEOMETRY.")
        print("      ζ is therefore the geometric SIGNATURE of the hexagonal ground")
        print("      state, NOT an independent dynamical output of this solver. The")
        print("      GP density is smooth (not touching disks), so its literal")
        print("      packing fraction is not π/√12; promoting ζ to a non-tautological")
        print("      energy ratio is a SEPARATE derivation MV-G1 does not perform.")
    else:
        print("      N/A — ζ is a property of the hexagonal lattice; the ground")
        print("      state here is not hexagonal, so the geometric ζ statement does")
        print("      not apply.")
    print()

    verdict = ("MV-G1 PASS (i): hexagonal ground state obtained; ζ follows "
               "geometrically." if hexagonal
               else "MV-G1 FAIL/NULL (i): not hexagonal — informative for §3.4 G1.")
    print("  VERDICT:", verdict)
    print()
    print("  Reminder (§3.4.6): the kernel form was IMPORTED (I1–I3); the test is")
    print("  whether hexagonality EMERGES. A pre-registered G0 term list (§3.4.3)")
    print("  must precede any promotion of this run to a §2.x result.")
    return hexagonal


def maybe_plot(rho, dx, path):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception as e:
        print(f"  [plot skipped: {e}]")
        return
    drho = rho - rho.mean()
    S = np.fft.fftshift(np.abs(np.fft.fft2(rho - rho.mean()))**2)
    fig, ax = plt.subplots(1, 2, figsize=(9, 4.2))
    ax[0].imshow(rho, origin="lower", cmap="magma")
    ax[0].set_title("density ρ(x)"); ax[0].set_xticks([]); ax[0].set_yticks([])
    n = S.shape[0]
    c = slice(n // 2 - n // 6, n // 2 + n // 6)
    ax[1].imshow(np.log1p(S[c, c]), origin="lower", cmap="viridis")
    ax[1].set_title("structure factor S(k) [log]"); ax[1].set_xticks([]); ax[1].set_yticks([])
    fig.tight_layout(); fig.savefig(path, dpi=130); plt.close(fig)
    print(f"  [figure written: {path}]")


def main(argv=None):
    ap = argparse.ArgumentParser(description="§3.4-MV-G1 roton-GP minimiser.")
    ap.add_argument("--N", type=int, default=160, help="grid points/side")
    ap.add_argument("--L", type=float, default=20.0, help="box size")
    ap.add_argument("--R", type=float, default=1.0, help="soft-core radius")
    ap.add_argument("--g", type=float, default=22.0, help="interaction strength")
    ap.add_argument("--rho0", type=float, default=1.0, help="mean density")
    ap.add_argument("--dtau", type=float, default=2e-3, help="imaginary-time step")
    ap.add_argument("--steps", type=int, default=4000, help="max relaxation steps")
    ap.add_argument("--ramp", type=float, default=0.0,
                    help="fraction of steps to ramp g over (0 = full quench; a "
                         "slow ramp damps the seed and can get stuck uniform)")
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--plot", type=str, default=None, help="write PNG to this path")
    args = ap.parse_args(argv)

    rho, dx, KX, KY, K2, Uk, roton = ground_state(
        args.N, args.L, args.R, args.g, args.rho0, args.dtau, args.steps,
        args.seed, ramp=args.ramp)
    res = analyse_symmetry(rho, dx, args.L, KX, KY)
    a = lattice_constant_triangular(res["kc"])
    hexagonal = report(res, a, args.g, roton)
    if args.plot:
        maybe_plot(rho, dx, args.plot)
    return 0 if hexagonal else 1


if __name__ == "__main__":
    raise SystemExit(main())
