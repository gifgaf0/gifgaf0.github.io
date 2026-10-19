#!/usr/bin/env python3
"""E7 figures from results_raw.json / hedgehog.json (run e7_audit.py first). Deterministic."""
import json, os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(HERE, 'results_raw.json')))
INK, INK2, GRID = '#0b0b0b', '#52514e', '#d9d8d4'
S1, S2, S3 = '#2a78d6', '#eb6834', '#1baf7a'
plt.rcParams.update({'font.size': 9, 'axes.edgecolor': INK2, 'axes.labelcolor': INK, 'xtick.color': INK2,
                     'ytick.color': INK2, 'axes.grid': True, 'grid.color': GRID, 'grid.linewidth': 0.6,
                     'axes.spines.top': False, 'axes.spines.right': False, 'figure.facecolor': '#fcfcfb',
                     'axes.facecolor': '#fcfcfb', 'savefig.facecolor': '#fcfcfb'})

sk = R['skyrme']; a1 = sk['a1']; Lam = R['inputs']['hedgehog']['Lambda']; c0 = sk['c0']['B']
el = sk['electron']
e = np.geomspace(1, 1e5, 400)

# ---------------- figure 1: size vs Compton wavelength, and quantum/classical ratios
fig, ax = plt.subplots(1, 2, figsize=(9.0, 3.6))
a = ax[0]
a.loglog(e, c0 / e**2, color=S1, lw=2)
a.text(150, c0 / 150**2 * 8, r'$MR/\hbar c = c_0/e^2$' + f', $c_0 = {c0:.1f}$', color=INK, fontsize=8)
pr = sk['proton']
a.plot([5.45], [pr['MR_classical']['value']], 'o', color=S2, ms=7, mec='#fcfcfb', mew=1.5, zorder=5)
a.annotate('proton fold (ANW, e = 5.45)', (5.45, pr['MR_classical']['value']), xytext=(30, 15), color=INK, fontsize=8,
           arrowprops=dict(arrowstyle='-', color=INK2, lw=0.6))
for name, ls in [('LEP', '-'), ('SEED', '--')]:
    y = el[name]['MR_required_max']; ee = el[name]['B']['e_min']
    a.axhline(y, color=INK2, lw=1, ls=ls)
    a.plot([ee], [y], 'o', color=S3, ms=7, mec='#fcfcfb', mew=1.5, zorder=5)
    lab = r'electron, $R<1.1\times10^{-4}$ fm (LEP)' if name == 'LEP' else r'electron, $R<10^{-3}$ fm (SEED)'
    a.text(1.2, y * (0.35 if name == 'LEP' else 1.6), lab + f': e > {ee:.3g}', color=INK, fontsize=7.5)
emax = sk['semiclassical_floor']['rot_over_M_le_1.0']['e_max']
a.axvline(emax, color=INK2, lw=1, ls=':')
a.text(emax * 1.15, 3e-3, 'rotor energy\n= fold mass', color=INK2, fontsize=7.5)
a.set_xlabel('Skyrme coupling e'); a.set_ylabel(r'$R/\lambda_C = MR/\hbar c$  (baryon rms radius)')
a.set_title('Fold size in units of its Compton wavelength', fontsize=9, color=INK, loc='left')
a.set_ylim(1e-8, 2e2)
b = ax[1]
rot = 9 * e**4 / (16 * np.pi * Lam * a1)
b.loglog(e, rot, color=S1, lw=2, label=r'rotor $E_{rot}/M = 9e^4/(16\pi\Lambda a_1)$')
b.loglog(e, e**2 / c0, color=S2, lw=2, label=r'$\hbar/(MR) = e^2/c_0$ (loop-size proxy)')
b.axhline(1, color=INK2, lw=1, ls=':')
b.axvline(el['LEP']['B']['e_min'], color=INK2, lw=1)
b.text(el['LEP']['B']['e_min'] * 0.8, 1e-3, 'electron (LEP)', rotation=90, ha='right', color=INK2, fontsize=7.5)
b.axvline(5.45, color=INK2, lw=1, ls='--')
b.text(5.45 * 0.85, 1e8, 'proton', rotation=90, ha='right', color=INK2, fontsize=7.5)
b.set_xlabel('Skyrme coupling e'); b.set_ylabel('quantum correction / classical mass')
b.set_title('Semiclassical expansion parameters', fontsize=9, color=INK, loc='left')
b.legend(frameon=False, fontsize=7.5, loc='upper left')
b.set_ylim(1e-4, 1e15)
fig.tight_layout()
fig.savefig(os.path.join(HERE, 'fig_scale.png'), dpi=110)

# ---------------- figure 2: vacuum ratios and pair suppression
fig, ax = plt.subplots(1, 2, figsize=(9.0, 3.6), gridspec_kw=dict(width_ratios=[1.1, 1]))
a = ax[0]
rat = R['vacuum']['ratios_scale4_over_rhoL']
names = list(rat.keys()); vals = [rat[k]['log10'] for k in names]
short = [n.split(' (')[0] if not n.startswith('Higgs') else 'Higgs potential depth' for n in names]
short = ['$f_\\pi^4$', 'Skyrme-fit $f^4$', '$m_e^4$', '$v_{EW}^4$', '$m_H^2v^2/8$', 'reduced $M_{Pl}^4$', '$M_{Pl}^4$']
y = np.arange(len(vals))
a.barh(y, vals, color=S1, height=0.6)
for yi, v in zip(y, vals):
    a.text(v + 2, yi, f'{v:.1f}', va='center', color=INK, fontsize=8)
a.set_yticks(y); a.set_yticklabels(short); a.invert_yaxis()
a.set_xlim(0, 140); a.set_xlabel(r'$\log_{10}(\mathrm{scale}^4/\rho_\Lambda)$')
a.set_title(r'Vacuum tension vs natural scales, $\rho_\Lambda=(2.24\ \mathrm{meV})^4$', fontsize=9, color=INK, loc='left')
a.grid(axis='y', visible=False)
b = ax[1]
g2 = np.geomspace(3e-3, 30, 400)
for F, col, lab in [(3.93, S1, 'F = 3.93 (high-energy plateau)'), (4.45, S2, 'F = 4.45 (at threshold)')]:
    b.semilogx(g2, -F / g2 / np.log(10), color=col, lw=2, label=lab)
alpha = 1 / 137.036
b.axvline(alpha, color=INK2, lw=1, ls='--'); b.text(alpha * 0.85, -150, r'$g^2=\alpha$', color=INK2, fontsize=8, ha='right')
b.axvline(4 * np.pi * alpha, color=INK2, lw=1, ls=':'); b.text(4 * np.pi * alpha * 1.15, -120, r'$4\pi\alpha$', color=INK2, fontsize=8)
b.axvspan(1.7, 30, color=GRID, alpha=0.5, lw=0)
b.text(2.0, -60, 'unsuppressed:\n$M_S \\lesssim 2m$', color=INK, fontsize=7.5)
b.set_ylim(-260, 5); b.set_xlabel(r'fold-sector coupling $g^2$ (action $=S_0/g^2$)')
b.set_ylabel(r'$\log_{10} P_{2\to S\bar S}$ (exponent only)')
b.set_title('Two-particle fold-pair suppression (Demidov-Levkov)', fontsize=9, color=INK, loc='left')
b.legend(frameon=False, fontsize=7.5, loc='lower right')
fig.tight_layout()
fig.savefig(os.path.join(HERE, 'fig_vacuum_pairs.png'), dpi=110)
for f in ['fig_scale.png', 'fig_vacuum_pairs.png']:
    print(f, os.path.getsize(os.path.join(HERE, f)) // 1024, 'KB')
