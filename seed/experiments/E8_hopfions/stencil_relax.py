"""
stencil_relax.py -- reconciliation test (not a pass criterion): can a centred-difference energy, minimised by
Sutcliffe's own method (arrested Newton flow with the sigma-model kinetic term), hold the Q = 1 Hopf soliton at
dx = 0.1, and at what energy?

Background.  stencil_check.py showed that the 2nd-order centred-difference energy E_c2 of our relaxed dx = 0.1
fields reproduces Sutcliffe's Table 2 to <= 0.18% for Q = 1..7.  The cross-check objected that pure centred
functionals have grid-scale (k = pi) null modes, so a minimiser might not be able to hold a soliton with them
(its 4th-order centred L-BFGS relaxation unwound a Q = 1 soliton at h = 0.1875).  The Battye-Sutcliffe code
lineage (hep-th/9811077, hep-th/0103026) used 4th-order differences.  This script relaxes our Q = 1 dx = 0.1 field
under
    c2: D_i phi = (phi(x+e_i) - phi(x-e_i)) / 2h
    c4: D_i phi = (-phi(x+2e_i) + 8 phi(x+e_i) - 8 phi(x-e_i) + phi(x-2e_i)) / 12h, 2nd order one point from the
        boundary (as in Battye-Sutcliffe 2002, sec. 2.3.2)
with E = C0 h^3 sum_{interior x} [ sum_i |D_i phi|^2 + sum_{i<j} |D_i phi x D_j phi|^2 ] and its exact gradient,
starting from our relaxed field plus a small random tangent perturbation (amplitude 1e-4, fixed seed) that seeds
the grid-scale modes.  Monitored: E_c, our link/plaquette energy E_link of the same field (it penalises grid-scale
modes, so a growing E_link - E_c gap signals them), min phi_3, Hopf charge.

Usage: NUMBA_NUM_THREADS=2 python3 stencil_relax.py [--scheme c2|c4|both] [--tmax 50]
Restart-safe: checkpoints every 10 time units in SCRATCH/e8rec_stencil/.  Writes stencil_relax.json and
runs/stencil_relax_<scheme>.log.
"""
import argparse
import json
import os
import time
import numpy as np
from numba import njit, prange
import fs_lib as fs

HERE = os.path.dirname(os.path.abspath(__file__))
SCRATCH = '/tmp/claude-0/-home-user-gifgaf0-github-io/235fe351-6f97-5895-b3fd-a90496179b3c/scratchpad/E8_fields'
CKDIR = '/tmp/claude-0/-home-user-gifgaf0-github-io/235fe351-6f97-5895-b3fd-a90496179b3c/scratchpad/e8rec_stencil'
OUT = os.path.join(HERE, 'stencil_relax.json')
SUTCLIFFE_E1 = 1.204


@njit(inline='always')
def _coef(xi, s, N, order):
    """weight c_s of phi(x + s e) in h * D phi(x) along one axis, x at index xi along that axis"""
    if xi < 1 or xi > N - 2:
        return 0.0
    if order == 4 and xi >= 2 and xi <= N - 3:
        if s == 2:
            return -1.0 / 12.0
        if s == 1:
            return 8.0 / 12.0
        if s == -1:
            return -8.0 / 12.0
        if s == -2:
            return 1.0 / 12.0
        return 0.0
    if s == 1:
        return 0.5
    if s == -1:
        return -0.5
    return 0.0


@njit(parallel=True, fastmath=True)
def centred_pass1(phi, h, G, order):
    """energy (without C0) and G_d(x) = d(density)/d(D_d phi(x))"""
    N = phi.shape[0]
    e2s = np.zeros(N)
    e4s = np.zeros(N)
    for i in prange(1, N - 1):
        D = np.zeros((3, 3))
        e2 = 0.0
        e4 = 0.0
        for j in range(1, N - 1):
            for k in range(1, N - 1):
                idx = (i, j, k)
                for d in range(3):
                    for c in range(3):
                        D[d, c] = 0.0
                    for s in (-2, -1, 1, 2):
                        w = _coef(idx[d], s, N, order)
                        if w != 0.0:
                            if d == 0:
                                for c in range(3):
                                    D[d, c] += w * phi[i + s, j, k, c]
                            elif d == 1:
                                for c in range(3):
                                    D[d, c] += w * phi[i, j + s, k, c]
                            else:
                                for c in range(3):
                                    D[d, c] += w * phi[i, j, k + s, c]
                    for c in range(3):
                        D[d, c] /= h
                n0 = D[0, 0] ** 2 + D[0, 1] ** 2 + D[0, 2] ** 2
                n1 = D[1, 0] ** 2 + D[1, 1] ** 2 + D[1, 2] ** 2
                n2 = D[2, 0] ** 2 + D[2, 1] ** 2 + D[2, 2] ** 2
                d01 = D[0, 0] * D[1, 0] + D[0, 1] * D[1, 1] + D[0, 2] * D[1, 2]
                d12 = D[1, 0] * D[2, 0] + D[1, 1] * D[2, 1] + D[1, 2] * D[2, 2]
                d20 = D[2, 0] * D[0, 0] + D[2, 1] * D[0, 1] + D[2, 2] * D[0, 2]
                e2 += n0 + n1 + n2
                e4 += (n0 * n1 - d01 * d01) + (n1 * n2 - d12 * d12) + (n2 * n0 - d20 * d20)
                for c in range(3):
                    G[0, i, j, k, c] = 2 * D[0, c] + 2 * ((n1 + n2) * D[0, c] - d01 * D[1, c] - d20 * D[2, c])
                    G[1, i, j, k, c] = 2 * D[1, c] + 2 * ((n0 + n2) * D[1, c] - d01 * D[0, c] - d12 * D[2, c])
                    G[2, i, j, k, c] = 2 * D[2, c] + 2 * ((n0 + n1) * D[2, c] - d20 * D[0, c] - d12 * D[1, c])
        e2s[i] = e2
        e4s[i] = e4
    return e2s.sum() * h ** 3, e4s.sum() * h ** 3


@njit(parallel=True, fastmath=True)
def centred_pass2(G, h, grad, order):
    """grad(y) = h^2 sum_d sum_s c_s(y - s e_d) G_d(y - s e_d)"""
    N = grad.shape[0]
    h2 = h * h
    for i in prange(N):
        for j in range(N):
            for k in range(N):
                for c in range(3):
                    grad[i, j, k, c] = 0.0
                if i == 0 or j == 0 or k == 0 or i == N - 1 or j == N - 1 or k == N - 1:
                    continue
                for s in (-2, -1, 1, 2):
                    w = _coef(i - s, s, N, order)
                    if w != 0.0:
                        for c in range(3):
                            grad[i, j, k, c] += h2 * w * G[0, i - s, j, k, c]
                    w = _coef(j - s, s, N, order)
                    if w != 0.0:
                        for c in range(3):
                            grad[i, j, k, c] += h2 * w * G[1, i, j - s, k, c]
                    w = _coef(k - s, s, N, order)
                    if w != 0.0:
                        for c in range(3):
                            grad[i, j, k, c] += h2 * w * G[2, i, j, k - s, c]


def centred_energy_grad(phi, h, G, grad, order):
    e2, e4 = centred_pass1(phi, h, G, order)
    centred_pass2(G, h, grad, order)
    return e2, e4


def grad_check(order, seed=3):
    """finite-difference check of the gradient on a small random smooth-ish field"""
    rng = np.random.default_rng(seed)
    N = 14
    x = np.linspace(-1, 1, N)
    X, Y, Z = np.meshgrid(x, x, x, indexing='ij')
    v = np.stack([np.sin(2 * X + Y), np.cos(Y - Z), 1.5 + np.sin(X * Z)], -1) + 0.1 * rng.standard_normal((N, N, N, 3))
    phi = v / np.linalg.norm(v, axis=-1, keepdims=True)
    h = x[1] - x[0]
    G = np.zeros((3,) + phi.shape)
    g = np.zeros_like(phi)
    centred_energy_grad(phi, h, G, g, order)
    errs = []
    for (i, j, k, c) in [(5, 6, 7, 0), (2, 3, 4, 1), (1, 1, 12, 2), (7, 2, 9, 0), (12, 12, 1, 1)]:
        e = 1e-6
        p = phi.copy(); p[i, j, k, c] += e
        Ep = sum(centred_pass1(p, h, G, order))
        p[i, j, k, c] -= 2 * e
        Em = sum(centred_pass1(p, h, G, order))
        fd = (Ep - Em) / (2 * e)
        centred_energy_grad(phi, h, G, g, order)
        errs.append(abs(fd - g[i, j, k, c]) / max(1e-12, abs(fd)))
    return max(errs)


def log(fh, s):
    print(s, flush=True)
    fh.write(s + '\n')
    fh.flush()


def run(scheme, tmax, results):
    order = 2 if scheme == 'c2' else 4
    os.makedirs(CKDIR, exist_ok=True)
    os.makedirs(os.path.join(HERE, 'runs'), exist_ok=True)
    fh = open(os.path.join(HERE, 'runs', f'stencil_relax_{scheme}.log'), 'a')
    N = 151
    x, h = fs.grid(N, 7.5)
    ck_phi = os.path.join(CKDIR, f'{scheme}.phi.npy')
    ck_vel = os.path.join(CKDIR, f'{scheme}.vel.npy')
    ck_st = os.path.join(CKDIR, f'{scheme}.state.json')
    res = results.setdefault(scheme, dict(order=order, history=[]))
    res['grad_check_rel_err'] = grad_check(order)
    log(fh, f'# scheme {scheme}: gradient check max rel err {res["grad_check_rel_err"]:.2e}')
    if os.path.exists(ck_st):
        st = json.load(open(ck_st))
        phi = np.load(ck_phi); vel = np.load(ck_vel)
        t, dt, nreset = st['t'], st['dt'], st['nreset']
        res['history'] = st['history']
        log(fh, f'# resumed at t={t:.2f}')
    else:
        phi = np.load(os.path.join(SCRATCH, 'Q1_A11_N151.phi.npy'))
        e2l, e4l = fs.energy_grad(phi, h, np.zeros_like(phi), False)
        G0 = np.zeros((3,) + phi.shape)
        c2, c4 = centred_pass1(phi, h, G0, order)
        res['start_unperturbed'] = dict(E_link=fs.C0 * (e2l + e4l), E_centred=fs.C0 * (c2 + c4))
        del G0
        rng = np.random.default_rng(20261019)
        pert = 1e-4 * rng.standard_normal(phi.shape)
        phi = phi + pert
        phi /= np.linalg.norm(phi, axis=-1, keepdims=True)
        fs.set_boundary(phi)
        vel = np.zeros_like(phi)
        t, dt, nreset = 0.0, 0.1 * h, 0
        res['perturbation'] = 'iid normal, amplitude 1e-4 per component, seed 20261019, renormalised; boundary reset to e3'
    G = np.zeros((3,) + phi.shape)
    grad = np.zeros_like(phi)
    e2, e4 = centred_energy_grad(phi, h, G, grad, order)
    E = e2 + e4
    phi_good = phi.copy(); E_good = E; t_good = t
    last_log = t
    wall0 = time.time()
    steps_int = resets_int = 0

    def record(t, E, e2, e4):
        e2l, e4l = fs.energy_grad(phi, h, np.zeros_like(phi), False)
        Q, nhh, _ = fs.hopf_charge(phi, h)
        rec = dict(t=round(t, 3), E_centred=fs.C0 * E, E2c=fs.C0 * e2, E4c=fs.C0 * e4, E_link=fs.C0 * (e2l + e4l),
                   Q=-Q, hedgehogs=nhh, minphi3=fs.min_phi3(phi), resets=nreset, dt=dt, wall=time.time() - wall0)
        res['history'].append(rec)
        log(fh, json.dumps(rec))
        return rec

    if not res['history']:
        record(t, E, e2, e4)
    while t < tmax - 1e-9:
        fs.anf_step(phi, vel, grad, h, dt)
        t += dt
        steps_int += 1
        e2n, e4n = centred_energy_grad(phi, h, G, grad, order)
        En = e2n + e4n
        if En > E:
            fs.zero_field(vel)
            nreset += 1
            if En > E * (1 + 1e-11):
                resets_int += 1
        E, e2, e4 = En, e2n, e4n
        if t - last_log >= 2.0 - 1e-9:
            last_log = t
            if E > E_good * (1 + 1e-9) or resets_int > 0.2 * steps_int or not np.isfinite(E):
                log(fh, f'# safeguard at t={t:.2f}: restoring t={t_good:.2f}, dt {dt:.5f} -> {0.7 * dt:.5f}')
                phi[...] = phi_good; fs.zero_field(vel); dt *= 0.7; t = t_good; last_log = t
                e2, e4 = centred_energy_grad(phi, h, G, grad, order); E = e2 + e4
                steps_int = resets_int = 0
                continue
            phi_good[...] = phi; E_good = E; t_good = t
            steps_int = resets_int = 0
            rec = record(t, E, e2, e4)
            if abs(t / 10 - round(t / 10)) < 1e-6:
                np.save(ck_phi, phi); np.save(ck_vel, vel)
                json.dump(dict(t=t, dt=dt, nreset=nreset, history=res['history']), open(ck_st, 'w'))
            if rec['minphi3'] > -0.5 or abs(rec['Q']) < 0.5:
                log(fh, '# soliton lost (min phi3 > -0.5 or |Q| < 0.5): stop')
                res['unwound_at_t'] = t
                break
    H = res['history']
    res['final'] = H[-1]
    if len(H) >= 6:
        res['rel_change_last_10'] = H[-1]['E_centred'] / H[-6]['E_centred'] - 1
    res['final_vs_sutcliffe'] = H[-1]['E_centred'] / SUTCLIFFE_E1 - 1
    np.save(ck_phi, phi); np.save(ck_vel, vel)
    json.dump(dict(t=t, dt=dt, nreset=nreset, history=res['history']), open(ck_st, 'w'))
    fh.close()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--scheme', default='both')
    ap.add_argument('--tmax', type=float, default=50.0)
    a = ap.parse_args()
    results = json.load(open(OUT)) if os.path.exists(OUT) else {}
    results['description'] = ('Q = 1, dx = 0.1, box [-7.5,7.5]^3, fixed boundary: our relaxed link/plaquette field (+1e-4 '
                              'random perturbation) relaxed under centred-difference energies by arrested Newton flow; '
                              'energies in Sutcliffe units')
    for sc in (['c2', 'c4'] if a.scheme == 'both' else [a.scheme]):
        run(sc, a.tmax, results)
        json.dump(results, open(OUT, 'w'), indent=1)
        r = results[sc]
        print(f"[{sc}] final E_centred {r['final']['E_centred']:.5f} (vs Sutcliffe 1.204: {100 * r['final_vs_sutcliffe']:+.2f}%), "
              f"E_link {r['final']['E_link']:.5f}, Q {r['final']['Q']:.4f}, minphi3 {r['final']['minphi3']:.4f}, "
              f"unwound: {r.get('unwound_at_t')}")


if __name__ == '__main__':
    main()
