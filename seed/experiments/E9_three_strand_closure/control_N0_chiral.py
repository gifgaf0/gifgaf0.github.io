"""N = 0 control (P1): a composite ring with no twist should shrink. Free relaxation from R0.
control_N0_chiral.py: copy of control_N0.py using gl3_chiral.GL3Chiral with gamma as an argument; maxiter and the
record interval are optional arguments (defaults 600 and 25, as in control_N0.py); each record adds the energy split and the vortex segment counts.
usage: python3 control_N0_chiral.py N R0 GAMMA [MAXITER EVERY]"""
import numpy as np, json, sys, time
from gl3_chiral import GL3Chiral
from linking import vortex_segments
N = int(sys.argv[1]) if len(sys.argv) > 1 else 49
R0 = float(sys.argv[2]) if len(sys.argv) > 2 else 6.0
gamma = float(sys.argv[3])
maxiter = int(sys.argv[4]) if len(sys.argv) > 4 else 600
every = int(sys.argv[5]) if len(sys.argv) > 5 else 25
g = GL3Chiral(N=N, h=0.5, eta=0.1, gamma=gamma)
f = g.ring_field((0, 0, 0), (0, 0, 1), R0)
psi = np.stack([f, f, f]); A = np.zeros((3, N, N, N))
E0 = g.energy_grad(g.pack(psi, A))[0] - g.vacuum_energy()
hist = []; t0 = time.time()
def cb(v):
    if len(hist) % every == 0:
        p, a_ = g.unpack(v); E = g.energy_grad(v)[0] - g.vacuum_energy()
        hist.append(dict(it=len(hist), E=float(E), R2=g.core_radius(p[1]), R1=g.core_radius(p[0]), **g.split(p, a_)[0],
                         nseg=[len(vortex_segments(p[k], g.h, -(N // 2) * g.h)[0]) for k in range(3)], t=time.time() - t0))
        print(json.dumps(hist[-1]), flush=True)
    else:
        hist.append(None)
psi, A, r = g.minimize(psi, A, maxiter=maxiter, callback=cb)
E = g.energy_grad(g.pack(psi, A))[0] - g.vacuum_energy()
out = dict(N=N, h=0.5, R0=R0, gamma=gamma, maxiter=maxiter, every=every, split_end=g.split(psi, A)[0], nseg_end=[len(vortex_segments(psi[k], g.h, -(N // 2) * g.h)[0]) for k in range(3)], E_start=float(E0), E_end=float(E), R_end=g.core_radius(psi[1]),
           iters=int(r.nit), converged=bool(r.success), msg=str(r.message), seconds=time.time() - t0,
           history=[x for x in hist if x])
json.dump(out, open(f'control_N0_chiral_N{N}_R{R0:g}_g{gamma:+g}.json', 'w'), indent=1)
print('FINAL', json.dumps({k: out[k] for k in ('E_start', 'E_end', 'R_end', 'iters', 'converged', 'seconds')}))
