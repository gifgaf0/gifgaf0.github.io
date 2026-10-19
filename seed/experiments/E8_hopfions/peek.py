"""
peek.py -- quick look at an in-progress checkpoint: energy, Q, curves, type.
Usage: NUMBA_NUM_THREADS=1 python3 peek.py RUN N [L]
"""
import sys
import json
import os
import numpy as np
import fs_lib as fs
import analyze as an

run, N = sys.argv[1], int(sys.argv[2])
L = float(sys.argv[3]) if len(sys.argv) > 3 else 7.5
ck = os.path.join(an.SCRATCH, f'{run}_N{N}')
phi = np.load(ck + '.phi.npy')
st = json.load(open(ck + '.state.json'))
h = 2 * L / (N - 1)
e2, e4 = fs.energy_grad(phi, h, np.zeros_like(phi), False)
a, pos, lnk = an.analyse_field(phi, h, L)
typ, axial = an.classify(a)
print(f"{run} N={N} t={st['t']:.1f} E={fs.C0 * (e2 + e4):.6f} Q={a['Q']:.4f} type={typ} comps={a['n_position']} "
      f"alex={a['alexander']} lk={a['lk_position_position']} twist={a['twist_per_component']} slice={a['slice_degrees']} "
      f"asym={a['inertia_axial_asym']:.4f} shapes={[(round(s['out_of_plane_rms_over_radius'], 3), round(s['radius_std_over_mean'], 3)) for s in a['loop_shapes']]} "
      f"tube={a['tube_components']}")
