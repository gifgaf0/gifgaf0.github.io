"""N = 1 twisted closure (P2). Free relaxation from a Hopf-linked start.
usage: python3 run_N1.py START N R0 MAXITER     e.g.  python3 run_N1.py A 49 6 4000
START A: strands 2,3 on a ring of radius R0 in the z=0 plane; strand 1 on a ring of radius R0 in the x-z plane
         centred at (R0,0,0): a Hopf link.
START B: strands 2,3 as above; strand 1 on a (1,1) helix of minor radius 2 around the ring core (PREREG §9).
Both starts are built in starts.py (Amendment B); each links the composite ring once (|Lk| = 1).
Checkpoints every 100 iterations: energy, strand core radii, fields saved to .npz for later analysis.
Verdict rules are in PREREG.md (Amendment A). This script prints no verdict.
"""
import numpy as np, json, sys, time
from gl3 import GL3
start, N, R0, maxiter = sys.argv[1], int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4])
g = GL3(N=N, h=0.5, eta=0.1)
from starts import start_fields   # Amendment B: corrected starts
psi = start_fields(g, start, R0); A = np.zeros((3, N, N, N))
tag = f'N1_{start}_N{N}_R{R0:g}'
hist = []; t0 = time.time(); it = [0]
def diag(v):
    p, a = g.unpack(v); E = g.energy_grad(v)[0] - g.vacuum_energy()
    m1 = np.abs(p[0]) ** 2 < 0.25
    return dict(it=it[0], E=float(E), R23=g.core_radius(p[1]), n_core1=int(m1.sum()),
                core1_rmean=float(np.sqrt(g.x[m1] ** 2 + g.y[m1] ** 2).mean()) if m1.any() else 0.0,
                core1_zrms=float(np.sqrt((g.z[m1] ** 2).mean())) if m1.any() else 0.0, t=time.time() - t0)
def cb(v):
    it[0] += 1
    if it[0] % 100 == 0:
        d = diag(v); hist.append(d); print(json.dumps(d), flush=True)
        p, a = g.unpack(v); np.savez_compressed(f'{tag}_ckpt.npz', psi=p, A=a, it=it[0])
print(json.dumps(diag(g.pack(psi, A))), flush=True)
psi, A, r = g.minimize(psi, A, maxiter=maxiter, gtol=1e-5, callback=cb)
final = diag(g.pack(psi, A)); final.update(converged=bool(r.success), msg=str(r.message), iters=int(r.nit))
np.savez_compressed(f'{tag}_final.npz', psi=psi, A=A)
json.dump(dict(start=start, N=N, R0=R0, history=hist, final=final), open(f'{tag}.json', 'w'), indent=1)
print('FINAL', json.dumps(final))
