"""
qlink_coarse.py -- reconciliation check (not a relaxation): estimator-free Hopf charge of the coarsest fields.

The cross-check found that at dx = 0.2 the Whitehead-integral charge depends on the estimator: our solid-angle
estimator (exact plaquette solid angles, periodic FFT) deviates from the integer by at most 0.017, a
fourth-order-difference estimator with a free-space Green function by up to 0.086 (Q = 7), above the 0.05
criterion for Q = 4-7.  analyze.py computed the linking-number charge only on the two finest fields of each run.
This script computes it on the dx = 0.2 (N = 76) and dx = 0.15 (N = 101) fields of every charge: the total linking
number between the position curve (phi = -e3) and the linking curve (phi = (sqrt(2mu-mu^2), 0, -1+mu), mu = 0.1),
in 3 random projections, with the sign convention of analyze.py.  It also repeats the solid-angle Whitehead charge.

Usage: NUMBA_NUM_THREADS=1 python3 qlink_coarse.py     (a few minutes; writes qlink_coarse.json)
"""
import json
import os
import numpy as np
import fs_lib as fs

HERE = os.path.dirname(os.path.abspath(__file__))
SCRATCH = '/tmp/claude-0/-home-user-gifgaf0-github-io/235fe351-6f97-5895-b3fd-a90496179b3c/scratchpad/E8_fields'
MU = 0.1
LINK_TARGET = (np.sqrt(2 * MU - MU ** 2), 0.0, -1 + MU)
RUNS = {1: 'Q1_A11', 2: 'Q2_A21', 3: 'Q3_A31', 4: 'Q4_A22', 5: 'Q5_K32', 6: 'Q6_L22', 7: 'Q7_K32'}


def main():
    out = dict(description='linking-number Hopf charge (estimator-free) and solid-angle Whitehead charge of the '
                           'coarse fields; Sutcliffe sign convention', fields={})
    for Q, run in RUNS.items():
        for N in (76, 101):
            p = os.path.join(SCRATCH, f'{run}_N{N}.phi.npy')
            if not os.path.exists(p):
                continue
            phi = np.load(p)
            x, h = fs.grid(N, 7.5)
            Qw, nhh, _ = fs.hopf_charge(phi, h, workers=1)
            pos, pinfo = fs.preimage_curves(phi, h, L=7.5)
            lnk, linfo = fs.preimage_curves(phi, h, L=7.5, target=LINK_TARGET)
            allc = pos + lnk
            lks = [-fs.linking_matrix(allc, seed=s)[0] for s in (1, 5, 9)]
            npos = len(pos)
            qlink = [float(L[:npos, npos:].sum()) for L in lks]
            rec = dict(Q_nominal=Q, N=N, h=h, Q_whitehead_solid_angle=-Qw, dev_whitehead=abs(-Qw - Q), hedgehogs=nhh,
                       n_position=npos, n_linking=len(lnk), Q_from_linking_3_projections=qlink,
                       linking_consistent=bool(all(abs(q - qlink[0]) < 1e-9 for q in qlink)),
                       Q_link_equals_nominal=bool(all(abs(q - Q) < 1e-9 for q in qlink)))
            out['fields'][f'{run}_N{N}'] = rec
            print(f'{run} N={N} h={h:.3f}: Q_W(solid angle) {-Qw:.4f}  Q_link {qlink}  npos {npos} nlink {len(lnk)}', flush=True)
    out['all_Q_link_integer_and_nominal'] = bool(all(r['Q_link_equals_nominal'] for r in out['fields'].values()))
    json.dump(out, open(os.path.join(HERE, 'qlink_coarse.json'), 'w'), indent=1, default=float)


if __name__ == '__main__':
    main()
