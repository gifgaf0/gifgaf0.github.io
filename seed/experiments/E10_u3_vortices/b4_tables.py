"""
E10 Route B, B4: collect everything into b4_results.json and print the report tables (read-only).
Run: python3 b4_tables.py > log_b4_tables.txt
"""
import os, json
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
HD = os.path.join(HERE, 'b4_hist')
RUNS = ['REG', 'M3a', 'M3b', 'M5a', 'M5b', 'C-a', 'C-b', 'C-c', 'C-d', 'C-d5']
FINE = ['M3a', 'M3b', 'M5a', 'M5b', 'C-d', 'C-d5']


def load(tag):
    f = os.path.join(HD, tag + '.json')
    return json.load(open(f)) if os.path.exists(f) else None


def f(x, p=4):
    if x is None:
        return '—'
    if isinstance(x, (int, np.integer)):
        return str(x)
    if abs(x) != 0 and (abs(x) < 1e-3 or abs(x) >= 1e5):
        return f'{x:.2e}'
    return f'{x:.{p}f}'


def row(o, Q):
    tau = o['tau'] if (o['tau'] is not None and 0 <= o['tau'] <= 1) else None
    return (f"| {o['iter']} | {f(o['E'], 4)} | {f(o['E'] / Q, 5) if Q else '—'} | {f(o['R_f'], 3)} | {o['n_vortex_plaquettes']} | "
            f"{f(o['R_q'], 3)} | {f(o['r_q'], 3)} | {f(o['I'], 2)} | {f(o['omega'], 5)} | {f(o['omega_over_mbulk'], 5)} | "
            f"{f(o['leak'])} | {f(tau, 6) if tau is not None else ('undef.' if o['tau'] is not None else '—')} |")


HDR = ('| iter | E | E/(m Q) | R_f | vortex plaq. | R_q | r_q | I | ω | ω/m | leak | τ |\n'
       '|---|---|---|---|---|---|---|---|---|---|---|---|')


if __name__ == '__main__':
    out = dict(label='Exploration', prereg='PREREG_B4.md', runs={}, fine={})
    for r in RUNS:
        rec = load(r)
        if rec is None:
            continue
        out['runs'][r] = rec
        Q = rec['spec']['Q']
        print(f'\n### {r}  (n = {rec["spec"]["n"]}, Q = {Q:.4f}, R0 = {rec["spec"]["R0"]}, mode {rec["spec"]["mode"]})')
        print(f'stop: {rec.get("end", {}).get("message")}; iterations {rec.get("end", {}).get("iter")}; '
              f'max|grad| {rec.get("end", {}).get("grad_max")}; restarts {rec.get("restarts")}; '
              f'memory resets {rec.get("end", {}).get("memory_resets")}; seconds {f(rec.get("end", {}).get("seconds"), 0)}')
        print(HDR)
        H = rec['history']
        sel = [o for o in H if o['iter'] % 500 == 0 and not o.get('final')] + [H[-1]]
        for o in sel:
            print(row(o, Q))
    print('\n### h = 0.125 re-relaxations')
    print('| run | E (h=0.25) | E (h=0.125) | rel ΔE | R_f (0.25) | R_f (0.125) | rel ΔR_f | passes (<5 %, <1e-3) | iters | stop |')
    print('|---|---|---|---|---|---|---|---|---|---|')
    for r in FINE:
        c, fi = load(r), load(r + '_fine')
        if c is None or fi is None or 'end' not in fi:
            continue
        out['fine'][r] = fi
        ec, ef = c['end'], fi['end']
        dE = abs(ef['E'] / ec['E'] - 1)
        if ec['R_f'] is not None and ef['R_f'] is not None:
            dR = abs(ef['R_f'] / ec['R_f'] - 1); ok = dR < 0.05 and dE < 1e-3
            print(f"| {r} | {f(ec['E'], 4)} | {f(ef['E'], 4)} | {f(dE)} | {ec['R_f']} | {ef['R_f']} | {f(dR)} | {'yes' if ok else 'NO'} | {ef['iter']} | {ef['message']} |")
        else:
            print(f"| {r} | {f(ec['E'], 4)} | {f(ef['E'], 4)} | {f(dE)} | — | — | — | E only: {'yes' if dE < 1e-3 else 'NO'} | {ef['iter']} | {ef['message']} |")
    print('\n### lump size (C-c, C-d, C-d5 end states; descriptive): charge-weighted 3D rms radius about the origin')
    import b4_run as BR
    from u3common import herm
    out['lump_size'] = {}
    for r in ('C-c', 'C-d', 'C-d5'):
        fp = os.path.join(HERE, 'b4_fields', r + '.npz')
        if not os.path.exists(fp):
            continue
        A, _, _ = BR.make(r, 0.25); A.cg_tol = 1e-12
        v = np.load(fp)['x']
        H, Wr, Wz, Pt = A.unpack(v); U, _ = A.links(Wr, Wz); P = A.Pfull(Pt)
        I, xw, _ = A.K_solve(H, U, P)
        dens = np.zeros((A.Nr, A.Nz)); A.K_full(H, U, P, herm(xw), 1.0, grads=False, dens=dens)
        r3 = float(np.sqrt(np.sum(dens * (A.RHO ** 2 + A.Z ** 2)) / dens.sum()))
        cum = [float(dens[np.hypot(A.RHO, A.Z) < R].sum() / dens.sum()) for R in (5, 10, 15)]
        d2 = np.abs(np.linalg.det(H))
        out['lump_size'][r] = dict(r_rms_3D=r3, charge_within_r5_r10_r15=cum, detH_at_origin=float(d2[0, A.Nz // 2]))
        print(f'{r}: r_rms(3D) = {r3:.3f}; charge fraction within r < 5, 10, 15: {cum}; |det H| at origin {d2[0, A.Nz // 2]:.3e}')
    v = os.path.join(HERE, 'b4_verdicts.json')
    if os.path.exists(v):
        out['verdicts'] = json.load(open(v))
    for k in ('b4_checks.json', 'b4_straight.json'):
        out[k[:-5]] = json.load(open(os.path.join(HERE, k)))
    json.dump(out, open(os.path.join(HERE, 'b4_results.json'), 'w'), default=float, separators=(',', ':'))
    print('\nwritten b4_results.json')
