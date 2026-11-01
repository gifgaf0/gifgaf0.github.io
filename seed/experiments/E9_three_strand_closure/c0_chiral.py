"""C0 (PREREG_chiral_loop.md §3 item 5): uniform vacuum + noise of amplitude 0.05 relaxes back to the vacuum.
Noise: N(0, 0.05) on every free variable (Re psi, Im psi, A), numpy default_rng(0). 65^3, eta = 0.1, h = 0.5,
kappa = 2, open boundaries; the same minimizer call as trace_N1_chiral.py (GL3.minimize, maxiter 4000, gtol 1e-5).
Pass: final E above vacuum <= 1e-5 and no vortex segments.
usage: python3 c0_chiral.py GAMMA [N]
"""
import numpy as np, json, sys, time
from gl3_chiral import GL3Chiral, S_field
from linking import vortex_segments
gamma = float(sys.argv[1]); N = int(sys.argv[2]) if len(sys.argv) > 2 else 65
g = GL3Chiral(N=N, h=0.5, eta=0.1, gamma=gamma)
f0 = np.sqrt(1 + g.eta)
v = g.pack(f0 * np.ones((3, N, N, N), complex), np.zeros((3, N, N, N)))
v = v + 0.05 * np.random.default_rng(0).normal(size=v.size)
psi, A = g.unpack(v)
t0 = time.time(); hist = []
def cb(x):
    hist.append(None)
    if len(hist) % 50 == 0:
        print(json.dumps(dict(it=len(hist), E=float(g.energy_grad(x)[0] - g.vacuum_energy()), t=time.time() - t0)), flush=True)
E0 = g.energy_grad(v)[0] - g.vacuum_energy()
psi, A, r = g.minimize(psi, A, maxiter=4000, gtol=1e-5, callback=cb)
E = g.energy_grad(g.pack(psi, A))[0] - g.vacuum_energy()
sp, w = g.split(psi, A)
nseg = [len(vortex_segments(psi[k], g.h, -(N // 2) * g.h)[0]) for k in range(3)]
dev = np.abs(psi - f0)                       # deviation from the gamma = 0 vacuum, per strand and site
idx = np.indices((N, N, N)); dface = np.min(np.stack([idx, N - 1 - idx]), axis=(0, 1))   # sites from nearest face
dens = g.chiral_density(psi, A)
Sn = np.linalg.norm(S_field(psi), axis=0)
layers = {}
for d in range(0, 6):
    m = dface == d
    layers[d] = dict(max_dev=float(dev[:, m].max()), S_mean=float(Sn[m].mean()), E_chi=float(dens[m].sum()))
m = dface >= 6
layers['>=6'] = dict(max_dev=float(dev[:, m].max()), S_mean=float(Sn[m].mean()), E_chi=float(dens[m].sum()))
out = dict(gamma=gamma, N=N, noise='N(0,0.05) on every variable, default_rng(0)', E_start=float(E0), E_end=float(E),
           nseg_end=nseg, split_end=sp, iters=int(r.nit), converged=bool(r.success), msg=str(r.message),
           seconds=time.time() - t0, max_dev_from_vacuum=float(dev.max()), by_distance_from_face=layers,
           passes=bool(E <= 1e-5 and sum(nseg) == 0))
json.dump(out, open(f'c0_chiral_N{N}_g{gamma:+g}.json', 'w'), indent=1)
print('FINAL', json.dumps(out))
