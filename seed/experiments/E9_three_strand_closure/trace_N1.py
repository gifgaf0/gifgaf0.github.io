"""Diagnostic re-run of run_N1.py with fine-grained history. Same model, same start, same minimizer call
(L-BFGS-B is deterministic, so the trajectory is the one run_N1.py follows); only the callback differs.
usage: python3 trace_N1.py START N R0 MAXITER EVERY
Records every EVERY iterations: energy above vacuum, composite ring radius, strand 1 loop geometry,
linking number of strand 1's vortex lines with strand 2's and strand 3's (linking.py), and the closest
approach of any vortex line to the box faces. Prints no verdict.
"""
import numpy as np, json, sys, time
from gl3 import GL3
from linking import vortex_segments, linking
start, N, R0, maxiter, every = sys.argv[1], int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
g = GL3(N=N, h=0.5, eta=0.1)
f23 = g.ring_field((0, 0, 0), (0, 0, 1), R0)
if start == 'A':   f1 = g.ring_field((R0, 0, 0), (0, 1, 0), R0)
elif start == 'B': f1 = g.ring_field((R0, 0, 0), (1, 0, 0), 2.0)
else: raise SystemExit('START must be A or B')
psi = np.stack([f1, f23, f23]); A = np.zeros((3, N, N, N))
half = (N // 2) * g.h; ax0 = -half
tag = f'trace_N1_{start}_N{N}_R{R0:g}'
hist = []; t0 = time.time(); it = [0]

def diag(v):
    p, a = g.unpack(v); E = g.energy_grad(v)[0] - g.vacuum_energy()
    s = [vortex_segments(p[k], g.h, ax0) for k in range(3)]
    mid = [(s0 + s1) / 2 for s0, s1 in s]
    d = dict(it=it[0], E=float(E), nseg=[len(m) for m in mid])
    for k in range(3):
        if len(mid[k]):
            m = mid[k]; rc = np.sqrt(m[:, 0] ** 2 + m[:, 1] ** 2)
            d[f'line{k+1}'] = dict(length=len(m) * g.h, centroid=[float(c) for c in m.mean(0)],
                                   rxy_mean=float(rc.mean()), rxy_min=float(rc.min()), rxy_max=float(rc.max()),
                                   z_rms=float(np.sqrt((m[:, 2] ** 2).mean())),
                                   wall_gap=float(half - np.abs(m).max()))
    for k in range(3):
        if len(mid[k]):
            # closure: every dual node must have equal in- and out-degree (else the line ends on a box face)
            from collections import Counter
            c = Counter()
            for q in np.round(s[k][0] / g.h * 4).astype(int): c[tuple(q)] -= 1
            for q in np.round(s[k][1] / g.h * 4).astype(int): c[tuple(q)] += 1
            d[f'line{k+1}']['open_ends'] = sum(1 for v_ in c.values() if v_ != 0)
            # winding of the line around the z-axis (linking with the z-axis; the axis is far from all cores)
            ph0 = np.arctan2(s[k][0][:, 1], s[k][0][:, 0]); ph1 = np.arctan2(s[k][1][:, 1], s[k][1][:, 0])
            d[f'line{k+1}']['Wz'] = float(np.sum((ph1 - ph0 + np.pi) % (2 * np.pi) - np.pi) / (2 * np.pi))
    if len(mid[0]) and len(mid[1]):
        # closest approach of strand 1's line to strand 2's line
        dd = np.min(np.linalg.norm(mid[0][:, None] - mid[1][None], axis=-1), axis=1)
        d['gap12_min'] = float(dd.min()); d['gap12_mean'] = float(dd.mean())
    d['Lk12'] = float(linking(*s[0], *s[1])) if len(mid[0]) and len(mid[1]) else 0.0
    d['Lk13'] = float(linking(*s[0], *s[2])) if len(mid[0]) and len(mid[2]) else 0.0
    d['R23_gl3'] = g.core_radius(p[1]); d['t'] = time.time() - t0
    return d

save = sys.argv[6] if len(sys.argv) > 6 else None
def cb(v):
    it[0] += 1
    if save and it[0] % every == 0 and it[0] <= 60:
        p_, a_ = g.unpack(v); np.savez_compressed(f'{save}/it{it[0]:04d}.npz', psi=p_, A=a_)
    if it[0] % every == 0:
        d = diag(v); hist.append(d); print(json.dumps(d), flush=True)

d0 = diag(g.pack(psi, A)); hist.append(d0); print(json.dumps(d0), flush=True)
psi, A, r = g.minimize(psi, A, maxiter=maxiter, gtol=1e-5, callback=cb)
final = diag(g.pack(psi, A)); final.update(converged=bool(r.success), msg=str(r.message), iters=int(r.nit))
json.dump(dict(start=start, N=N, R0=R0, every=every, history=hist, final=final), open(f'{tag}.json', 'w'), indent=1)
print('FINAL', json.dumps(final))
