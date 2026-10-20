#!/usr/bin/env python3
"""Cross-check E8: fourth-order link/plaquette Richardson energy E_R4 = (4 E_lp(h) - E_lp(2h))/3
of the original finest (dx = 0.1) and dx = 0.15 fields, and of my own analytic test field.
Writes xc_R4_fields.json."""
import json, os
import numpy as np
import xc_lib3d as X
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = '/tmp/claude-0/-home-user-gifgaf0-github-io/235fe351-6f97-5895-b3fd-a90496179b3c/scratchpad/E8_fields'
out = {}
for run in ['Q1_A11', 'Q2_A21', 'Q3_A31', 'Q4_A22', 'Q5_K32', 'Q6_L22', 'Q7_K32']:
    ent = {}
    for N in (101, 151):
        phi = np.ascontiguousarray(np.load(os.path.join(SRC, f'{run}_N{N}.phi.npy')))
        h = 15.0 / (N - 1)
        E = X.LPEnergy(N, 'R4')(phi, h)[0]
        ent[f'E_R4_N{N}'] = E
        if N == 151:
            ent['E_R4'] = E
    out[run] = ent
    print(run, ent, flush=True)
json.dump(out, open(os.path.join(HERE, 'xc_R4_fields.json'), 'w'), indent=1)
