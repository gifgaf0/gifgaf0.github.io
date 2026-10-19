"""
finalize_stage.py -- record a relaxation stage whose process died (container restart) after its
last checkpoint was written but before relax.py wrote the stage summary.

Loads <scratch>/<run>_N<N>.phi.npy (the last stored field, phi_good at state.json['t']), recomputes
energy, Hopf charge, hedgehog count and min phi3 exactly as relax.py does at the end of a stage, and
appends the stage record to runs/<run>.json with converged = False, stopped = True and a note.
No further relaxation is done.

Usage: NUMBA_NUM_THREADS=1 python3 finalize_stage.py --run Q7_K32 --N 151 [--L 7.5]
"""
import argparse
import json
import os
import numpy as np
import fs_lib as fs

HERE = os.path.dirname(os.path.abspath(__file__))
SCRATCH = '/tmp/claude-0/-home-user-gifgaf0-github-io/235fe351-6f97-5895-b3fd-a90496179b3c/scratchpad/E8_fields'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--run', required=True)
    ap.add_argument('--N', type=int, required=True)
    ap.add_argument('--L', type=float, default=7.5)
    ap.add_argument('--note', default='process killed by a container restart; stage recorded from its last checkpoint '
                                      '(field stored at state.t); a stop file had been issued by stop_watcher.py')
    a = ap.parse_args()
    ck = os.path.join(SCRATCH, f'{a.run}_N{a.N}')
    st = json.load(open(ck + '.state.json'))
    if st.get('done'):
        print('stage already finished by relax.py; nothing to do')
        return
    phi = np.load(ck + '.phi.npy')
    x, h = fs.grid(a.N, a.L)
    e2, e4 = fs.energy_grad(phi, h, np.zeros_like(phi), False)
    Q, nhh, _ = fs.hopf_charge(phi, h)
    rec = dict(N=a.N, h=h, L=a.L, t=st['t'], converged=False, stopped=True, wall_s=None,
               E=fs.C0 * (e2 + e4), E2=fs.C0 * e2, E4=fs.C0 * e4, Q=Q, hedgehogs=nhh,
               minphi3=float(fs.min_phi3(phi)), last=st['hist'][-1] if st['hist'] else None, note=a.note)
    # cross-check against the last logged record at the same flow time
    last = st['hist'][-1]
    print(f"recomputed E = {rec['E']:.7f} at t = {st['t']:.3f};  logged E at t = {last['t']}: {last['E']:.7f};  "
          f"rel diff {abs(rec['E'] / last['E'] - 1):.1e};  Q = {Q:+.4f}, hedgehogs {nhh}, min phi3 {rec['minphi3']:.6f}")
    # wall time of the stage from the log is not available reliably; estimate from log timestamps if present
    summ_path = os.path.join(HERE, 'runs', a.run + '.json')
    summary = json.load(open(summ_path))
    summary['stages'] = [s for s in summary['stages'] if s['N'] != a.N] + [rec]
    json.dump(summary, open(summ_path, 'w'), indent=1, default=float)
    with open(os.path.join(HERE, 'runs', a.run + '.log'), 'a') as fh:
        fh.write(f'# stage N={a.N} finalized from checkpoint by finalize_stage.py: {json.dumps(rec, default=float)}\n')


if __name__ == '__main__':
    main()
