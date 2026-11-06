"""P5 (Calculation 2c) relaxation trace: re-runs the 2c relaxations exactly as chiral1d.py does (same seed, same
solver options) with a callback recording, every iteration, min over s of |psi_k| and the largest nearest-neighbour
phase step of each component, so that the way the winding is lost can be read off. Writes p5_trace_chiral1d.json."""
import json, numpy as np, chiral1d as C
from scipy.optimize import minimize
R = json.load(open('chiral1d_results.json')); out = {}
for eta in (0.1, 0.0):
    gc = R['gamma_c'][f'z_eta{eta}_Afree']['gamma_c']
    for Af in (True, False):
        ch = C.Chain(C.NHAT['z'], eta, gc, 20.0, Af); x0 = ch.winding_seed(); tr = []
        def cb(x):
            psi, a, c = ch.unpack(ch.axial_gauge(x)); amp = np.abs(psi).min(1)
            step = np.abs(np.angle(np.roll(psi, -1, axis=1)*np.conj(psi))).max(1)
            w = np.angle(np.roll(psi, -1, axis=1)*np.conj(psi)).sum(1)/(2*np.pi)
            tr.append(dict(amp_min=amp.tolist(), max_phase_step=step.tolist(), winding=np.round(w, 6).tolist(), E=ch.energy_grad(x)[0]/ch.P - C.e_vac(eta)))
        r = minimize(ch.energy_grad, x0, jac=True, method='L-BFGS-B', options=C.SOLVER, callback=cb)
        amin = np.array([t['amp_min'] for t in tr]); wind = np.array([t['winding'][0] for t in tr])
        ch_it = [i for i in range(1, len(wind)) if round(wind[i]) != round(wind[i-1])]
        tag = f"eta{eta}_{'Afree' if Af else 'A0'}"
        out[tag] = dict(gamma=gc, nit=int(r.nit), final_gain=float(r.fun/ch.P - C.e_vac(eta)),
                        min_amp_over_path=amin.min(0).tolist(), iter_of_min=amin.argmin(0).tolist(),
                        winding_change_iters=ch_it,
                        at_change=[tr[i] for i in ch_it], h=ch.h,
                        trace_every10=tr[::10])
        print(tag, 'nit', r.nit, 'min |psi_k| along path', np.round(amin.min(0), 4), 'at iter', amin.argmin(0),
              'winding psi_1 changes at iters', ch_it, [ (np.round(tr[i]['amp_min'],4).tolist(), np.round(tr[i]['max_phase_step'],3).tolist()) for i in ch_it])
json.dump(out, open('p5_trace_chiral1d.json', 'w'), indent=1)
