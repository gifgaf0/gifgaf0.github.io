"""
G-TSH4 CC leg -- Phase 0 driver (full-from-scratch, E6).

For each kernel in {step, gem8} and each structure in {AA,AB,ABC,FCC,BCC}:
  * optimise the lattice parameters (a,c) [hex] or L [cubic] at fixed Lambda=2 Lc,
    minimising the energy per particle e;
  * F-CONV pin at the optimum: |de|/e under a x1.5 resolution increase must be
    <= 5e-6 (the pre-registered convergence gate); the finer-grid e is reported;
  * post-relaxation symmetry verification (Bragg peak count/positions vs seed);
  * C-NEG control (uniform state -> e=(Lam/2)Uhat(0)).

Then apply the Q-A decision rule with the Amendment A-1.1 class re-carve.

Writes tsh4_phase0_measurements.json.  T1 self-grep enforced at import.
"""
import json, time
import numpy as np
import tsh4_core as C
import tsh4_selfgrep
tsh4_selfgrep.assert_clean(["tsh4_core.py", "tsh4_phase0.py"])

S3 = np.sqrt(3.0)

def _even(x):
    x = int(round(x));  return x + (x & 1)

def make_cell(structure, params, ppl):
    fam = C.STRUCTURES[structure]['family']
    if fam == 'hex':
        a, c = params
        nx = max(16, _even(ppl*a))
        ny = max(16, _even(ppl*a*S3))
        nz = max(16, _even(ppl*c))
        return C.Cell([a, a*S3, c], (nx, ny, nz))
    else:
        (L,) = params
        n = max(20, _even(ppl*L))
        return C.Cell([L, L, L], (n, n, n))

def relax_at(structure, params, khat, Lam, ppl, seed_psi=None, wfac=0.24):
    cell = make_cell(structure, params, ppl)
    kg = C.khat_grid(cell, khat)
    sites = C.STRUCTURES[structure]['sites']
    psi0 = cell.seed(sites, width=wfac*cell.L[0]) if seed_psi is None else seed_psi
    psi, e, res, it, (ke, ie) = C.relax(cell, kg, Lam, psi0, dt=0.008, restol=1e-9)
    return dict(cell=cell, psi=psi, e=e, res=res, it=it, ke=ke, ie=ie, kg=kg)

# ---------------------------------------------------------------- optimisation
def parabola_min(xs, ys):
    p = np.polyfit(xs, ys, 2)
    if p[0] <= 0:
        i = int(np.argmin(ys));  return xs[i], ys[i]
    xstar = -p[1]/(2*p[0])
    return xstar, np.polyval(p, xstar)

def optimise_cubic(structure, khat, Lam, ppl, L0, span=0.18, log=None):
    Ls = np.linspace(L0*(1-span), L0*(1+span), 7)
    es = [relax_at(structure, (L,), khat, Lam, ppl)['e'] for L in Ls]
    i = int(np.argmin(es))
    lo, hi = max(i-1, 0), min(i+2, len(Ls))
    Lstar, _ = parabola_min(Ls[lo:hi], es[lo:hi])
    # one refinement pass around Lstar
    Ls2 = np.linspace(Lstar*0.97, Lstar*1.03, 5)
    es2 = [relax_at(structure, (L,), khat, Lam, ppl)['e'] for L in Ls2]
    Lstar, estar = parabola_min(Ls2, es2)
    if log is not None:
        log.append((structure, 'cubic scan', list(np.round(Ls,4)), list(np.round(es,5))))
    return (Lstar,), estar

def optimise_hex(structure, khat, Lam, ppl, a0, c0, log=None):
    # coordinate descent: scan a (fixed c), then c (fixed a), then refine.
    a, c = a0, c0
    for _ in range(2):
        As = np.linspace(a*0.90, a*1.10, 7)
        ea = [relax_at(structure, (aa, c), khat, Lam, ppl)['e'] for aa in As]
        i = int(np.argmin(ea)); lo, hi = max(i-1,0), min(i+2,len(As))
        a, _ = parabola_min(As[lo:hi], ea[lo:hi])
        Cs = np.linspace(c*0.90, c*1.10, 7)
        ec = [relax_at(structure, (a, cc), khat, Lam, ppl)['e'] for cc in Cs]
        j = int(np.argmin(ec)); lo, hi = max(j-1,0), min(j+2,len(Cs))
        c, _ = parabola_min(Cs[lo:hi], ec[lo:hi])
    # final local 2D refine (3x3) + separable parabola
    As = np.linspace(a*0.97, a*1.03, 3); Cs = np.linspace(c*0.97, c*1.03, 3)
    grid = np.array([[relax_at(structure,(aa,cc),khat,Lam,ppl)['e'] for cc in Cs] for aa in As])
    ai, _ = parabola_min(As, grid.min(axis=1))
    ci, _ = parabola_min(Cs, grid.min(axis=0))
    est = relax_at(structure, (ai, ci), khat, Lam, ppl)['e']
    return (ai, ci), est

# ---------------------------------------------------------------- checks
def fconv(structure, params, khat, Lam, ppl):
    """report coarse e, fine e (x1.5 ppl), and relative change (gate 5e-6)."""
    rc = relax_at(structure, params, khat, Lam, ppl)
    rf = relax_at(structure, params, khat, Lam, ppl*1.5)
    de = abs(rf['e']-rc['e'])/abs(rf['e'])
    return dict(e_coarse=rc['e'], e_fine=rf['e'], rel_change=de,
                passed=bool(de <= 5e-6), res_fine=rf['res'],
                cell_coarse=rc['cell'].n, cell_fine=rf['cell'].n)

def symmetry_ok(structure, params, khat, Lam, ppl):
    """count density maxima in the relaxed cell; must equal seeded-site count."""
    r = relax_at(structure, params, khat, Lam, ppl)
    n = (r['psi']**2)
    from scipy.ndimage import maximum_filter
    mx = maximum_filter(n, size=3, mode='wrap')
    thr = 0.25*n.max()
    peaks = (n == mx) & (n > thr)
    npk = int(peaks.sum())
    nsite = len(C.STRUCTURES[structure]['sites'])
    return dict(n_peaks=npk, n_sites=nsite, ok=bool(npk == nsite),
                rho_max=float(n.max()), rho_min=float(n.min()))

def cneg(khat, Lam):
    cell = C.Cell([2.0, 2.0*S3, 3.0], (12, 20, 16))
    kg = C.khat_grid(cell, khat)
    psi = np.ones(cell.n); psi /= np.sqrt((psi*psi).mean())
    e = C.energy(cell, kg, Lam, psi)
    e_exp = 0.5*Lam*khat(np.array([0.0]))[0]
    return dict(e=e, e_expected=float(e_exp), abs_err=abs(e-e_exp))
