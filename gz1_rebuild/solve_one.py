"""
solve_one.py — GZ1 Phase 4b (REBUILD): one driven-strip frequency-domain solve
Driven BdG response (prereg §5):  (L+X-w-i.eta)u + Xv = -S ; Xu + (L+X+w+i.eta)v = 0,
S = psi0-masked isotropic Gaussian density source at the row-0 site (sigma = 0.5).
GMRES; per-row envelope (max |drho| per wrap-aware row window); fit conventions
decoded from the original phase4_fits.json (see gz1_core.envelope_fit).
Writes phase4_<tag>.json + profile_<tag>.npy.   Usage: solve(tag, omega, eta)
"""
import json
import numpy as np
import gz1_core as core

_strip = None


def get_strip():
    global _strip
    if _strip is None:
        z = np.load("strip_cache.npz")
        s = core.Strip(float(z["a_star"]), Nx=24, Ny=192, nrows=16)
        s.psi0 = z["psi0"]
        s.mu = float(z["mu"])
        rho = s.psi0**2
        s.V = np.fft.ifft2(s.Uk * np.fft.fft2(rho)).real
        _strip = s
    return _strip


def solve(tag, omega, eta, rtol=1e-6, maxiter=400):
    s = get_strip()
    src = s.gaussian_source(sigma=0.5, row=0)
    drho, resid = s.solve_response(omega, eta, src, rtol=rtol, maxiter=maxiter)
    amp = s.row_envelope(drho)
    np.save(f"profile_{tag}.npy", amp)
    rec = dict(omega=omega, eta=eta, resid=resid)
    rec.update(core.envelope_fit(amp, s.d))
    # reorder to the original schema
    out = {k: rec[k] for k in ["omega", "eta", "resid", "wrap_min_row",
                               "clean_ratios", "t_ratio_median", "t_ratio_spread",
                               "kappa_fit", "t_fit", "fit_r2", "rows_rel"]}
    with open(f"phase4_{tag}.json", "w") as f:
        json.dump(out, f, indent=1)
    print(f"  {tag}: omega={omega} eta={eta} resid={resid:.2e} "
          f"kappa={out['kappa_fit']} t={out['t_fit']} r2={out['fit_r2']}")
    return out


if __name__ == "__main__":
    import sys
    solve(sys.argv[1], float(sys.argv[2]), float(sys.argv[3]))
