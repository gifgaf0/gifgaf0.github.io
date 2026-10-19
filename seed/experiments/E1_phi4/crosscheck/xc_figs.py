"""Cross-check figure: (left) DSV (omega, v) map, original vs mine; (right) E1d coarse grid producing
fraction vs E/2M, original vs mine on the same points.  Small PNG."""
import json, os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
c = json.load(open(os.path.join(HERE, 'xc_compare.json')))
fig, ax = plt.subplots(1, 2, figsize=(9, 3.6), dpi=90)
if 'dsv' in c:
    for om, v in c['dsv']['per_omega'].items():
        o = float(om)
        ax[0].scatter([o - 0.0015] * len(v['orig']), v['orig'], marker='s', s=14, c='tab:blue', label='original (dx=0.1, leapfrog)' if om == '0.9' else None)
        ax[0].scatter([o + 0.0015] * len(v['mine']), v['mine'], marker='o', s=14, c='tab:orange', label='cross-check (dx=0.08, RK4)' if om == '0.9' else None)
    ax[0].set_xlabel('omega'); ax[0].set_ylabel('v'); ax[0].set_title('DSV trains: pair at t = T (v step 0.02)', fontsize=9)
    ax[0].legend(fontsize=7, loc='lower left'); ax[0].set_ylim(0.38, 0.92)
if 'e1d_coarse' in c:
    rows = c['e1d_coarse']['frac_vs_E_orig_mine']
    mid = [np.sqrt(max(r[0], 0.25) * min(r[1], 128)) for r in rows]
    ax[1].semilogx(mid, [r[3] for r in rows], 's-', label='original', c='tab:blue')
    ax[1].semilogx(mid, [r[4] for r in rows], 'o--', label='cross-check', c='tab:orange')
    ax[1].axvline(1.0, c='k', lw=0.6)
    ax[1].set_xlabel('E / 2M_kink'); ax[1].set_ylabel('fraction producing')
    ax[1].set_title('Gaussian packets, coarse grid (n=%d, call agreement %.0f%%)' % (c['e1d_coarse']['n'], 100 * c['e1d_coarse']['agree']), fontsize=9)
    ax[1].legend(fontsize=7)
fig.tight_layout()
fig.savefig(os.path.join(HERE, 'fig_crosscheck.png'))
print('saved', os.path.getsize(os.path.join(HERE, 'fig_crosscheck.png')), 'bytes')
