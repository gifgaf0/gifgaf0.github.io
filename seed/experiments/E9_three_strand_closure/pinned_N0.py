"""N = 0 control (P1, second half): pinned composite ring, E(R) should fall as R falls."""
import numpy as np, json, sys, time
from gl3 import GL3
N = 49; R = float(sys.argv[1])
g = GL3(N=N, h=0.5, eta=0.1)
f = g.ring_field((0, 0, 0), (0, 0, 1), R)
psi = np.stack([f, f, f]); A = np.zeros((3, N, N, N))
g.pin_ring([0, 1, 2], (0, 0, 0), (0, 0, 1), R)
t0 = time.time()
psi, A, r = g.minimize(psi, A, maxiter=700, gtol=1e-5)
E = g.energy_grad(g.pack(psi, A))[0] - g.vacuum_energy()
out = dict(N=N, R=R, E=float(E), iters=int(r.nit), converged=bool(r.success), gmax=float(np.abs(r.jac).max()),
           pinned_sites=int(g.pin.sum()), R_measured=g.core_radius(psi[1]), seconds=time.time() - t0)
json.dump(out, open(f'pinned_N0_R{R:g}.json', 'w'), indent=1); print(json.dumps(out))
