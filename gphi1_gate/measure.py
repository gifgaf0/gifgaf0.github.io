"""
G-Phi1 measurement (Steps 1-5 + two-leg verification). EDDINGTON-ISOLATED:
the comparison constant Phi = 2*pi - phi^2/(8*pi^2) appears in NO line here;
it enters only gphi1_compare.py, run after this writes gphi1_measurements.json.

Pre-registration: 334e15e7-G_PHI1_PREREGISTRATION.md (June 15 2026).
MV-G1 soft-disk GP: g=22, R=1, rho0=1, a*=1.4576 (R1/V4.36).
Healing length xi = 1/sqrt(2 g) (the convention that makes the pre-registered
tanh result exact: rate_tanh = ln(3)*(2 xi/a*) = 0.227 and r_inflect_tanh =
0.931 xi = 0.141 R -- logged choice, not tuned to any outcome).
"""
import json
import numpy as np
from scipy.ndimage import map_coordinates
from scipy.interpolate import UnivariateSpline
import gz1_core as core

G, R, RHO0 = 22.0, 1.0, 1.0
A_STAR = 1.4576
XI = 1.0 / np.sqrt(2.0 * G)            # = 0.150756 ; 2*xi/a* = 0.206855
SCALE = 2.0 * XI / A_STAR
S3 = np.sqrt(3.0)


# ---------------------------------------------------------------- Step 1 ------
def relax_rect_supercell(nx_cells=2, ny_cells=2, target_dx=0.013, steps=30000,
                         dtau=2.0e-3):
    """Triangular crystal in a rectangular box of nx_cells x ny_cells conventional
    rectangular cells (each a* wide, sqrt3*a* tall, 2 atoms). PBC. a* is locked
    by the commensurate box (the gate fixes a*=1.4576; it is not re-optimised)."""
    Lx = nx_cells * A_STAR
    Ly = ny_cells * S3 * A_STAR
    Nx = int(round(Lx / target_dx) / 2) * 2
    Ny = int(round(Ly / target_dx) / 2) * 2
    X, Y, KX, KY, K2, dx, dy = core.rect_grids(Nx, Ny, Lx, Ly)
    Uk = core.U_tilde(np.sqrt(K2))
    # seed triangular lattice of Gaussians
    d_row = S3 * A_STAR / 2.0
    centres = []
    nrows = 2 * ny_cells
    for jr in range(nrows):
        yk = jr * d_row
        xoff = (A_STAR / 2.0) if (jr % 2) else 0.0
        for ic in range(nx_cells):
            centres.append((ic * A_STAR + xoff, yk))
            centres.append((ic * A_STAR + xoff + A_STAR, yk))
    sigma = 0.35 * A_STAR
    psi = np.zeros((Nx, Ny))
    for (cx, cy) in centres:
        ddx = X - cx
        ddx -= Lx * np.round(ddx / Lx)
        ddy = Y - cy
        ddy -= Ly * np.round(ddy / Ly)
        psi += np.exp(-(ddx**2 + ddy**2) / (2 * sigma**2))
    psi = psi.astype(complex) + 1e-3
    psi, mu, res = core.relax_rect(psi, K2, Uk, dtau, steps, tol=1e-14,
                                   report_every=200)
    rho = psi**2
    return dict(rho=rho, X=X, Y=Y, dx=dx, dy=dy, Lx=Lx, Ly=Ly,
                Nx=Nx, Ny=Ny, mu=mu, residual=res)


# ----------------------------------------------------- Steps 2-3: profile -----
def void_and_profile(rho, dx, dy, Lx, Ly, n_ang=24, rmax_xi=3.0, dr_xi=1.0 / 20):
    """Step 2 void centre (global density min, sub-grid refined by parabola);
    Step 3 angular-averaged radial profile around it (periodic interpolation)."""
    iv, jv = np.unravel_index(np.argmin(rho), rho.shape)
    Nx, Ny = rho.shape
    # parabolic sub-grid refinement of the minimum in x and y
    def refine(a, b, c):
        den = (a - 2 * b + c)
        return 0.0 if abs(den) < 1e-30 else 0.5 * (a - c) / den
    sx = refine(rho[(iv - 1) % Nx, jv], rho[iv, jv], rho[(iv + 1) % Nx, jv])
    sy = refine(rho[iv, (jv - 1) % Ny], rho[iv, jv], rho[iv, (jv + 1) % Ny])
    xv = (iv + sx) * dx
    yv = (jv + sy) * dy
    rho_void = float(map_coordinates(rho, [[xv / dx], [yv / dy]],
                                     mode="grid-wrap", order=3)[0])
    rvals = np.arange(0.0, rmax_xi * XI + 1e-12, dr_xi * XI)
    ang = np.linspace(0, 2 * np.pi, n_ang, endpoint=False)
    prof = np.empty_like(rvals)
    for k, r in enumerate(rvals):
        xs = (xv + r * np.cos(ang)) / dx
        ys = (yv + r * np.sin(ang)) / dy
        prof[k] = map_coordinates(rho, [xs, ys], mode="grid-wrap",
                                  order=3).mean()
    return dict(xv=xv, yv=yv, rho_void=rho_void, r=rvals, rho_r=prof)


# ----------------------------------------------------- Step 4: inflection -----
def inflection_fd(r, rho_r):
    """Inflection = max |drho/dr| (where d2rho/dr2 = 0), finite differences."""
    drho = np.gradient(rho_r, r)
    # restrict to the rising region (positive slope, before any turn-over)
    kmax = int(np.argmax(drho))
    k = int(np.argmax(np.abs(drho[:max(kmax + 5, 5)])))
    # parabolic refine of the |slope| peak
    if 1 <= k < len(drho) - 1:
        a, b, c = abs(drho[k - 1]), abs(drho[k]), abs(drho[k + 1])
        den = a - 2 * b + c
        s = 0.0 if abs(den) < 1e-30 else 0.5 * (a - c) / den
    else:
        s = 0.0
    dr = r[1] - r[0]
    r_inf = r[k] + s * dr
    rho_inf = float(np.interp(r_inf, r, rho_r))
    return r_inf, rho_inf


def inflection_spline(r, rho_r):
    """Leg (a): analytic 2nd-derivative root of a smoothing-spline fit."""
    sp = UnivariateSpline(r, rho_r, k=4, s=1e-6 * np.sum(rho_r**2))
    rr = np.linspace(r[0], r[-1], 4000)
    d1 = sp.derivative(1)(rr)
    d2 = sp.derivative(2)(rr)
    # inflection in the rising region: d2 crosses zero where d1>0
    kmax = int(np.argmax(d1))
    seg = slice(0, max(kmax + 1, 2))
    d2s = d2[seg]
    sign = np.sign(d2s)
    idx = np.where(np.diff(sign) != 0)[0]
    if len(idx):
        i = idx[0]
        # linear interp of the zero crossing
        r0, r1 = rr[i], rr[i + 1]
        f0, f1 = d2s[i], d2s[i + 1]
        r_inf = r0 - f0 * (r1 - r0) / (f1 - f0)
    else:
        r_inf = rr[int(np.argmax(d1))]
    rho_inf = float(sp(r_inf))
    return float(r_inf), rho_inf


# ----------------------------- Leg (b): independent solver (oblique cell) -----
def cell_solver_inflection(n=160):
    """Second GP solver, different discretisation: the oblique PRIMITIVE-cell
    fractional-grid relaxer (gz1_core.Cell). Radially average around its void
    via Cartesian->fractional periodic sampling, then FD inflection."""
    cell = core.Cell(A_STAR, n)
    psi, mu, res = cell.relax(steps=12000, dtau=2e-3, noise=0.0)
    rho = psi**2
    iv, jv = np.unravel_index(np.argmin(rho), rho.shape)
    # fractional coords of the void
    f1v, f2v = iv / n, jv / n
    xv = f1v * cell.a1[0] + f2v * cell.a2[0]
    yv = f1v * cell.a1[1] + f2v * cell.a2[1]
    # inverse of [a1 a2] to map Cartesian offset -> fractional
    M = np.array([cell.a1, cell.a2]).T
    Minv = np.linalg.inv(M)
    rvals = np.arange(0.0, 3.0 * XI + 1e-12, XI / 20)
    ang = np.linspace(0, 2 * np.pi, 24, endpoint=False)
    prof = np.empty_like(rvals)
    for k, r in enumerate(rvals):
        cart = np.stack([xv + r * np.cos(ang), yv + r * np.sin(ang)])
        frac = Minv @ cart                      # (2, n_ang)
        coords = [frac[0] * n, frac[1] * n]
        prof[k] = map_coordinates(rho, coords, mode="grid-wrap", order=3).mean()
    r_inf, rho_inf = inflection_fd(rvals, prof)
    return dict(r_inflect=r_inf, rho_inflect=rho_inf,
                rho_void=float(rho[iv, jv]), mu=mu, residual=res,
                r=rvals.tolist(), rho_r=prof.tolist())


# ----------------------------------------------------------------- main -------
def main():
    print("Step 1: relax rectangular supercell ...", flush=True)
    sc = relax_rect_supercell()
    print(f"  grid {sc['Nx']}x{sc['Ny']} dx={sc['dx']:.4f}  mu={sc['mu']:.4f}"
          f"  residual={sc['residual']:.2e}", flush=True)

    print("Steps 2-3: void + radial profile (registered window 0..3 xi) ...",
          flush=True)
    pf = void_and_profile(sc["rho"], sc["dx"], sc["dy"], sc["Lx"], sc["Ly"])
    print(f"  void at ({pf['xv']:.4f},{pf['yv']:.4f})  rho_void={pf['rho_void']:.5f}"
          f"  rho_max={sc['rho'].max():.4f}", flush=True)
    # extended diagnostic profile (premise check): is there an interior inflection
    # at all within the registered window, and where is the TRUE inflection?
    pfx = void_and_profile(sc["rho"], sc["dx"], sc["dy"], sc["Lx"], sc["Ly"],
                           rmax_xi=5.5)

    print("Step 4: inflection (FD + spline-fit leg a) ...", flush=True)
    r_fd, rho_fd = inflection_fd(pf["r"], pf["rho_r"])
    r_sp, rho_sp = inflection_spline(pf["r"], pf["rho_r"])
    dr = pf["r"][1] - pf["r"][0]
    boundary_hit = bool(abs(r_fd - pf["r"][-1]) < 1.5 * dr)
    # true (interior) inflection on the extended profile
    rx, px = pfx["r"], pfx["rho_r"]
    d1x = np.gradient(px, rx)
    ktrue = int(np.argmax(d1x))
    rtrue = rx[ktrue]
    rho_true = float(px[ktrue])
    rho_at_tanh_radius = float(np.interp(0.931 * XI, rx, px))
    print(f"  *** registered window: max|drho/dr| at r={r_fd:.4f}"
          f" ({r_fd/XI:.3f} xi); boundary_hit={boundary_hit}", flush=True)
    print(f"  *** TRUE interior inflection: r={rtrue:.4f} ({rtrue/XI:.3f} xi),"
          f" rho/rho0={rho_true:.4f}  (>1: profile overshoots rho0)", flush=True)
    print(f"  *** rho at tanh-inflection radius 0.931 xi = {rho_at_tanh_radius:.4f}"
          f"  (tanh predicts 0.3333)", flush=True)
    print(f"  FD:     r_inflect={r_fd:.5f} ({r_fd/XI:.4f} xi)  rho/rho0={rho_fd:.5f}",
          flush=True)
    print(f"  spline: r_inflect={r_sp:.5f} ({r_sp/XI:.4f} xi)  rho/rho0={rho_sp:.5f}",
          flush=True)

    print("Leg (b): independent oblique-cell solver ...", flush=True)
    cb = cell_solver_inflection()
    print(f"  cell:   r_inflect={cb['r_inflect']:.5f} ({cb['r_inflect']/XI:.4f} xi)"
          f"  rho/rho0={cb['rho_inflect']:.5f}  rho_void={cb['rho_void']:.5f}",
          flush=True)

    # two-leg agreement on r_inflect (rect-grid FD vs oblique-cell solver)
    twoleg = abs(r_fd - cb["r_inflect"]) / r_fd
    fit_vs_fd = abs(r_fd - r_sp) / r_fd
    print(f"  two-leg |rect - cell|/rect = {100*twoleg:.2f}%  (require <5%)",
          flush=True)

    # Step 5: compounding rate (primary = FD on the fine rect grid)
    rho_inflect = rho_fd
    rate_actual = -np.log(rho_inflect / RHO0) * SCALE
    dev_r_from_tanh = (r_fd - 0.931 * XI) / (0.931 * XI)

    out = dict(
        params=dict(g=G, R=R, rho0=RHO0, a_star=A_STAR, xi=XI,
                    two_xi_over_astar=SCALE, xi_convention="1/sqrt(2 g)"),
        step1=dict(Nx=sc["Nx"], Ny=sc["Ny"], dx=sc["dx"], Lx=sc["Lx"],
                   Ly=sc["Ly"], mu=sc["mu"], residual=sc["residual"],
                   rho_max=float(sc["rho"].max())),
        step2=dict(void_x=pf["xv"], void_y=pf["yv"], rho_void=pf["rho_void"]),
        step3=dict(r=pf["r"].tolist(), rho_r=pf["rho_r"].tolist()),
        step4=dict(r_inflect_fd=r_fd, rho_inflect_fd=rho_fd,
                   r_inflect_spline=r_sp, rho_inflect_spline=rho_sp,
                   r_inflect_over_xi=r_fd / XI,
                   dev_r_from_tanh_0p931xi=dev_r_from_tanh,
                   inflection_at_window_boundary=boundary_hit),
        premise_check=dict(
            note=("registered probe assumes a tanh-like vortex healing to rho0 "
                  "with an interior inflection near 0.931 xi at rho/rho0~1/3"),
            interior_inflection_in_window=(not boundary_hit),
            true_inflection_r_over_xi=rtrue / XI,
            true_inflection_rho_over_rho0=rho_true,
            rho_at_tanh_radius_0p931xi=rho_at_tanh_radius,
            tanh_rho_at_its_inflection=1.0 / 3.0,
            profile_extended_r=rx.tolist(),
            profile_extended_rho=px.tolist()),
        step5=dict(rho_inflect_over_rho0=rho_inflect / RHO0,
                   rate_actual=rate_actual,
                   rate_is_window_boundary_artifact=boundary_hit),
        verification=dict(method_a="analytic 2nd-deriv of smoothing-spline fit",
                          method_b="oblique primitive-cell GP solver (n=160)",
                          r_inflect_cell=cb["r_inflect"],
                          rho_inflect_cell=cb["rho_inflect"],
                          rho_void_cell=cb["rho_void"],
                          cell_mu=cb["mu"], cell_residual=cb["residual"],
                          twoleg_rel_diff=twoleg, fit_vs_fd_rel_diff=fit_vs_fd,
                          twoleg_pass=bool(twoleg < 0.05)),
    )
    with open("gphi1_measurements.json", "w") as f:
        json.dump(out, f, indent=1)
    print("\nrate_actual = %.5f  (rho_inflect/rho0 = %.5f)" %
          (rate_actual, rho_inflect / RHO0), flush=True)
    print("gphi1_measurements.json written  (NO Phi used here -- Eddington)",
          flush=True)


if __name__ == "__main__":
    main()
