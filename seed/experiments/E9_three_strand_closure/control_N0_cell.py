"""N = 0 control (P1): a composite ring with no twist should shrink. Free relaxation from R0.
control_N0_cell.py: copy of control_N0.py; only e, eta as arguments and kappa, eta in the output tag differ.
usage: python3 control_N0_cell.py N R0 E ETA"""
import numpy as np, json, sys, time
from gl3 import GL3
N = int(sys.argv[1]) if len(sys.argv) > 1 else 49
R0 = float(sys.argv[2]) if len(sys.argv) > 2 else 6.0
e, eta = float(sys.argv[3]), float(sys.argv[4])
g = GL3(N=N, h=0.5, e=e, eta=eta)
f = g.ring_field((0, 0, 0), (0, 0, 1), R0)
psi = np.stack([f, f, f]); A = np.zeros((3, N, N, N))
E0 = g.energy_grad(g.pack(psi, A))[0] - g.vacuum_energy()
hist = []; t0 = time.time()
def cb(v):
    if len(hist) % 25 == 0:
        p, _ = g.unpack(v); E = g.energy_grad(v)[0] - g.vacuum_energy()
        hist.append(dict(it=len(hist), E=float(E), R2=g.core_radius(p[1]), R1=g.core_radius(p[0]), t=time.time() - t0))
        print(json.dumps(hist[-1]), flush=True)
    else:
        hist.append(None)
psi, A, r = g.minimize(psi, A, maxiter=600, callback=cb)
E = g.energy_grad(g.pack(psi, A))[0] - g.vacuum_energy()
out = dict(N=N, h=0.5, R0=R0, E_start=float(E0), E_end=float(E), R_end=g.core_radius(psi[1]),
           iters=int(r.nit), converged=bool(r.success), msg=str(r.message), seconds=time.time() - t0,
           history=[x for x in hist if x])
json.dump(out, open(f'control_N0_N{N}_R{R0:g}_k{1 / (e * np.sqrt(3)):.3g}_eta{eta:g}.json', 'w'), indent=1)
print('FINAL', json.dumps({k: out[k] for k in ('E_start', 'E_end', 'R_end', 'iters', 'converged', 'seconds')}))
