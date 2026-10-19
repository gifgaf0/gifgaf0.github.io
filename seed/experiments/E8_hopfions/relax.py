"""
relax.py -- energy minimisation of Faddeev-Skyrme Hopf solitons by arrested Newton flow.

Dynamics (sigma-model kinetic term only, as in Sutcliffe 2007):
    phi_tt = -(1/h^3) dE_lat/dphi  projected on the tangent plane of S^2,
    symplectic Euler: v += dt F ; phi += dt v ; renormalise ; project v;
    whenever the energy rises, v is set to zero ("arrested Newton flow").
(Energies in the flow are E/C0; reported energies include C0 = 1/(32 sqrt2 pi^2).)

Stages: the field is relaxed on a sequence of grids on the same box [-L, L]^3
(fixed boundary phi = e3), each stage starting from the cubic interpolation of the
previous stage's final field.

Usage:
  python3 relax.py --run NAME --map K32_Q7 --Lf 7.5 --stages 76:3000:2e-6,101:...,151:...
  stage spec  N:Tmax:tolE[:Tmin]  (Tmax = max flow time of the stage; stop when the relative
                             energy change over the last 20 time units is below tolE and
                             the stage has run at least Tmin time units, default 40)
Checkpoints (fields) go to the scratch directory given by --scratch; the log and a
JSON summary go to runs/NAME.*  inside the experiment directory.  Restart-safe: an
existing checkpoint for a stage is resumed.
"""
import argparse
import json
import os
import sys
import time
import numpy as np
import fs_lib as fs

HERE = os.path.dirname(os.path.abspath(__file__))
SCRATCH_DEFAULT = '/tmp/claude-0/-home-user-gifgaf0-github-io/235fe351-6f97-5895-b3fd-a90496179b3c/scratchpad/E8_fields'


def log(fh, s):
    fh.write(s + '\n')
    fh.flush()


def relax_stage(phi, h, Tmax, tolE, fh, ckpt_path, dt_fac=0.1, log_every=10.0, q_every=100.0,
                t0=0.0, vel=None, hist=None, tmin=40.0):
    """Arrested Newton flow.  Safeguard against the explicit-integration instability:
    at every log time the field is stored if the energy went down over the interval;
    if instead the energy rose, or more than 20% of the steps in the interval were
    arrested, the stored field is restored and dt is reduced by 0.7 (logged)."""
    N = phi.shape[0]
    dt = dt_fac * h
    grad = np.zeros_like(phi)
    if vel is None:
        vel = np.zeros_like(phi)
    if hist is None:
        hist = []
    e2, e4 = fs.energy_grad(phi, h, grad, True)
    E = e2 + e4
    t = t0
    nreset = 0
    last_log = t
    last_q = t - q_every  # compute Q at stage start
    last_ck = time.time()
    Ehist = [(t, E)]
    wall0 = time.time()
    converged = False
    phi_good = phi.copy()
    E_good = E
    t_good = t
    steps_int = 0
    resets_int = 0
    while t < Tmax:
        fmax, fsum = fs.anf_step(phi, vel, grad, h, dt)
        t += dt
        steps_int += 1
        e2n, e4n = fs.energy_grad(phi, h, grad, True)
        En = e2n + e4n
        if En > E:
            fs.zero_field(vel)
            nreset += 1
            if En > E * (1 + 1e-11):
                resets_int += 1
        E, e2, e4 = En, e2n, e4n
        Ehist.append((t, E))
        if t - last_log >= log_every - 1e-9:
            last_log = t
            if E > E_good * (1 + 1e-9) or resets_int > 0.2 * steps_int or not np.isfinite(E):
                log(fh, f'# instability safeguard at t={t:.3f}: E={fs.C0*E:.6f} vs stored {fs.C0*E_good:.6f}, '
                        f'resets {resets_int}/{steps_int}; restoring t={t_good:.3f}, dt {dt:.5f} -> {0.7*dt:.5f}')
                phi[...] = phi_good
                fs.zero_field(vel)
                dt *= 0.7
                t = t_good
                last_log = t
                e2, e4 = fs.energy_grad(phi, h, grad, True)
                E = e2 + e4
                Ehist = [(tt, ee) for (tt, ee) in Ehist if tt <= t_good]
                steps_int = 0
                resets_int = 0
                continue
            phi_good[...] = phi
            E_good = E
            t_good = t
            steps_int = 0
            resets_int = 0
            mp = fs.min_phi3(phi)
            rec = dict(t=round(t, 4), E=fs.C0 * E, E2=fs.C0 * e2, E4=fs.C0 * e4, vir=(e2 - e4) / E,
                       Frms=np.sqrt(fsum), Fmax=fmax, minphi3=mp, resets=nreset, dt=dt)
            if t - last_q >= q_every - 1e-9:
                last_q = t
                Q, nhh, _ = fs.hopf_charge(phi, h)
                rec['Q'] = Q
                rec['hedgehogs'] = nhh
            hist.append(rec)
            log(fh, json.dumps(rec))
            # convergence: relative change over last 20 time units
            told = t - 20.0
            Eold = None
            for (tt, ee) in reversed(Ehist):
                if tt <= told:
                    Eold = ee
                    break
            if Eold is not None and abs(Eold - E) / E < tolE and t > tmin:
                converged = True
                break
            if len(Ehist) > 20000:
                Ehist = Ehist[-10000:]
        if time.time() - last_ck > 300:
            np.save(ckpt_path + '.phi.npy', phi_good)
            np.save(ckpt_path + '.vel.npy', np.zeros_like(vel))
            json.dump(dict(t=t_good, hist=hist), open(ckpt_path + '.state.json', 'w'))
            last_ck = time.time()
    np.save(ckpt_path + '.phi.npy', phi)
    np.save(ckpt_path + '.vel.npy', vel)
    json.dump(dict(t=t, hist=hist, done=True, converged=converged), open(ckpt_path + '.state.json', 'w'))
    return phi, t, converged, hist, time.time() - wall0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--run', required=True)
    ap.add_argument('--map', required=True)
    ap.add_argument('--Lf', type=float, default=7.5)
    ap.add_argument('--L', type=float, default=7.5)
    ap.add_argument('--offset', default='0.05,0.03,0.02')
    ap.add_argument('--squash', default='1,1,1')
    ap.add_argument('--stages', required=True)
    ap.add_argument('--dtfac', type=float, default=0.1)
    ap.add_argument('--scratch', default=SCRATCH_DEFAULT)
    ap.add_argument('--init_from', default=None, help='start from a saved field .npy instead of the rational map')
    a = ap.parse_args()
    os.makedirs(os.path.join(HERE, 'runs'), exist_ok=True)
    os.makedirs(a.scratch, exist_ok=True)
    fh = open(os.path.join(HERE, 'runs', a.run + '.log'), 'a')
    summ_path = os.path.join(HERE, 'runs', a.run + '.json')
    summary = json.load(open(summ_path)) if os.path.exists(summ_path) else dict(run=a.run, map=a.map, Lf=a.Lf, L=a.L,
                                                                              offset=a.offset, stages=[])
    log(fh, f'# start {time.ctime()} args={vars(a)}')
    stages = []
    for s in a.stages.split(','):
        parts = s.split(':')
        tmin = float(parts[3]) if len(parts) > 3 else 40.0
        stages.append((int(parts[0]), float(parts[1]), float(parts[2]), tmin))
    phi = None
    off = tuple(float(v) for v in a.offset.split(','))
    sq = tuple(float(v) for v in a.squash.split(','))
    for si, (N, Tmax, tolE, tmin) in enumerate(stages):
        x, h = fs.grid(N, a.L)
        ck = os.path.join(a.scratch, f'{a.run}_N{N}')
        done = [st for st in summary['stages'] if st['N'] == N]
        if done and os.path.exists(ck + '.phi.npy'):
            phi = np.load(ck + '.phi.npy')
            log(fh, f'# stage N={N} already done, loaded')
            continue
        vel = None
        t0 = 0.0
        hist = None
        if os.path.exists(ck + '.state.json') and os.path.exists(ck + '.phi.npy'):
            st = json.load(open(ck + '.state.json'))
            phi = np.load(ck + '.phi.npy')
            vel = np.load(ck + '.vel.npy')
            t0 = st['t']
            hist = st['hist']
            log(fh, f'# resuming stage N={N} at t={t0}')
        elif phi is None:
            if a.init_from:
                phi0 = np.load(a.init_from)
                phi = fs.interpolate_field(phi0, N, a.L) if phi0.shape[0] != N else phi0.copy()
            else:
                phi, h = fs.rational_map_field(N, fs.MAPS[a.map][1], L=a.L, Lf=a.Lf, offset=off, squash=sq)
            Q, nhh, _ = fs.hopf_charge(phi, h)
            e2, e4 = fs.energy_grad(phi, h, np.zeros_like(phi), False)
            log(fh, f'# initial field N={N}: E={fs.C0*(e2+e4):.6f} Q={Q:.4f} hedgehogs={nhh}')
            summary['initial'] = dict(N=N, E=fs.C0 * (e2 + e4), Q=Q)
        else:
            phi = fs.interpolate_field(phi, N, a.L)
            e2, e4 = fs.energy_grad(phi, h, np.zeros_like(phi), False)
            log(fh, f'# interpolated to N={N}: E={fs.C0*(e2+e4):.6f}')
        log(fh, f'# stage N={N} h={h:.5f} Tmax={Tmax} tolE={tolE} dt={a.dtfac*h:.5f}')
        phi, t, conv, hist, wall = relax_stage(phi, h, Tmax, tolE, fh, ck, dt_fac=a.dtfac, t0=t0, vel=vel, hist=hist,
                                               tmin=tmin)
        e2, e4 = fs.energy_grad(phi, h, np.zeros_like(phi), False)
        Q, nhh, _ = fs.hopf_charge(phi, h)
        rec = dict(N=N, h=h, L=a.L, t=t, converged=conv, wall_s=wall, E=fs.C0 * (e2 + e4), E2=fs.C0 * e2,
                   E4=fs.C0 * e4, Q=Q, hedgehogs=nhh, minphi3=float(fs.min_phi3(phi)),
                   last=hist[-1] if hist else None)
        summary['stages'] = [st for st in summary['stages'] if st['N'] != N] + [rec]
        json.dump(summary, open(summ_path, 'w'), indent=1, default=float)
        log(fh, f'# stage N={N} finished: {json.dumps(rec, default=float)}')
    log(fh, f'# end {time.ctime()}')


if __name__ == '__main__':
    main()
