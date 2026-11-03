"""
E10 B3, symmetry-breaking check of the radial reduction (descriptive, added after b3_compare2d.py).
b3_compare2d.py starts the 2D minimisation from the equivariant (radial) configuration, and the lattice symmetry is
preserved by the gradient, so an equivariant saddle would not be detected there.  Here the h = 0.25 2D solution
(from b3_compare2d's checkpoint) is perturbed by random, symmetry-breaking noise (amplitude 0.05 in every real
component of H on interior sites and of W on all links) and re-minimised.  If the equivariant configuration is a
local minimum, the energy returns to the same value and the rot90 asymmetry decays.
Run: python3 b3_perturb2d.py > log_b3_perturb2d.txt  -> b3_perturb2d.json
"""
import os
os.environ.setdefault('OMP_NUM_THREADS', '1')
import numpy as np, json, time
from scipy.optimize import minimize
from u3common import rot12
from u3radial import Radial
from u3lattice import Lattice2D, OPTS2D

LAM, K, Q, ALPHA = 1.0, 0.2, 3.0, np.pi / 4
R = Radial(LAM, dr=0.05, rmax=20.0, relax_alpha=False)
ROPTS = dict(maxiter=50000, maxfun=100000, gtol=1e-10, ftol=1e-15, maxcor=20)
r0 = minimize(R.make_fg(0, 0), R.initial(), jac=True, method='L-BFGS-B', options=ROPTS)
r1 = minimize(R.make_fg(K, Q), r0.x, jac=True, method='L-BFGS-B', options=ROPTS)
h, a, _ = R.profiles(r1.x)
Lt = Lattice2D(LAM, L=160, h=0.25)
v_eq = Lt.from_radial(h, a, R.r, (1, 0, 0), V=rot12(ALPHA))      # sets the Dirichlet boundary values
v_ref = np.load('/tmp/claude-0/ckpt/cmp_L160.npy')
fg, st = Lt.make_fg(K, Q)
E_ref = fg(v_ref)[0]
rng = np.random.default_rng(7)
v0 = v_ref + 0.05 * rng.normal(size=v_ref.size)
E0 = fg(v0)[0]


def asym(v):
    H, _ = Lt.unpack(v); d = np.abs(np.linalg.det(H)); return float(np.max(np.abs(d - np.rot90(d))))


t = time.time()
res = minimize(fg, v0, jac=True, method='L-BFGS-B', options=OPTS2D)
out = dict(E_reference=float(E_ref), asym_reference=asym(v_ref), E_perturbed_start=float(E0), asym_start=asym(v0),
           E_final=float(res.fun), asym_final=asym(res.x), rel_dE=float(res.fun / E_ref - 1), I_final=float(st['I']),
           success=bool(res.success), message=str(res.message), nit=int(res.nit), seconds=time.time() - t)
print(json.dumps(out, indent=1), flush=True)
json.dump(out, open('b3_perturb2d.json', 'w'), indent=1)
