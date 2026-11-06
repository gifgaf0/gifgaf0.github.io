"""Read-only tables for REPORT_chiral1d.md from chiral1d_results.json.
Handedness is recomputed here from the sign of the gamma-free chiral density (chiral/gamma):
negative = right-handed (NOTE §1.1 convention: u = (cos qz, sin qz, 0), q > 0, gives u.curl u = -q).
The 'handedness' field written by chiral1d.py used the sign of the gamma-weighted chiral energy, which is
negative at any favourable state for either sign of gamma; it is not used (REPORT deviation)."""
import json, numpy as np
R = json.load(open('chiral1d_results.json'))
cases = [(nk, eta) for eta in (0.1, 0.0) for nk in ('z', 'diag', 'perp')]

def hand(chiral, gamma):
    dens = chiral/gamma
    return 'R' if dens < -1e-12 else ('L' if dens > 1e-12 else '0')

print('## gamma_c')
print('| n | eta | gamma_c (A free) [bracket] | gamma_lin (A free) | gamma_c (A=0) [bracket] | gamma_lin (A=0) | ratio Afree/A0 |')
for nk, eta in cases:
    a = R['gamma_c'][f'{nk}_eta{eta}_Afree']; b = R['gamma_c'][f'{nk}_eta{eta}_A0']
    la = R['linear'][f'{nk}_eta{eta}_Afree']; lb = R['linear'][f'{nk}_eta{eta}_A0']
    print(f"| {nk} | {eta} | {a['gamma_c']:.5f} [{a['bracket'][0]:.5f}, {a['bracket'][1]:.5f}] | {la['gamma_lin']:.5f} (q={la['q']:.3f}) "
          f"| {b['gamma_c']:.5f} [{b['bracket'][0]:.5f}, {b['bracket'][1]:.5f}] | {lb['gamma_lin']:.5f} (q={lb['q']:.3f}) | {a['gamma_c']/b['gamma_c']:.3f} |")

def nonconv(tag):
    h = R['gamma_c'][tag]['history']; tot = sum(len(v) for v in h.values()); nc = sum(1 for v in h.values() for r in v if not r['success'])
    msgs = {}
    for v in h.values():
        for r in v:
            if not r['success']: msgs[r['message'][:24]] = msgs.get(r['message'][:24], 0)+1
    mg = max([r['maxgrad'] for v in h.values() for r in v if not r['success']] or [0])
    return tot, nc, msgs, mg
print('\n## solves in the gamma_c searches')
for k in R['gamma_c']:
    tot, nc, msgs, mg = nonconv(k); print(f'| {k} | {tot} | {nc} | {msgs} | {mg:.1e} |')

print('\n## optimum diagnostics')
print('| case | gamma | P* | q* | q* (1/xi) | seed | hand | gain | grad | pot | jos | mag | chiral | chiral_twist | chiral_AS | <|S|/|psi|^2> | cone mean [min,max] | director turn (deg/cell) | amp spread | rho_k | winding_k | conv |')
for tag, d in R['optimum'].items():
    gm = 1.1*R['gamma_c'][tag.replace('_g0.01', '')]['gamma_c'] if not tag.endswith('_g0.01') else 0.01
    ev = 3*(0.5*d['josephson']*0)  # placeholder (unused)
    print(f"| {tag} | {gm:.5f} | {d['P_star']:.3f} | {d['q_star']:.4f} | {d['q_star_xi']:.4f} | {d['seed']} | {hand(d['chiral'], gm)} | {d['gain']:+.3e} | "
          f"{d['gradient']:.4e} | {d['potential']:.4e} | {d['josephson']:.4e} | {d['magnetic']:.3e} | {d['chiral']:+.4e} | {d['chiral_twist']:+.3e} | {d['chiral_AS']:+.3e} | "
          f"{d['S_over_rho_mean']:.4f} | {d['cone_deg_mean']:.2f} [{d['cone_deg_min']:.2f}, {d['cone_deg_max']:.2f}] | {d['director_turn_deg']:+.2f} | {d['amp_spread']:.4f} | "
          f"{np.round(d['rho_k_mean'], 4).tolist()} | {np.round(d['winding_k'], 3).tolist()} | {d['success']} |")

print('\n## gain vs P at the optimum (min over seeds)')
for tag, d in R['optimum'].items():
    c = d['gain_vs_P']; print(tag, ' '.join(f"{float(k):.2f}:{v:+.2e}" for k, v in c.items()))

print('\n## mirror')
for tag, m in R['mirror'].items():
    g11 = 1.1*R['gamma_c'][tag]['gamma_c']; o = R['optimum'][tag]
    at = m['at_-1.1gc']
    dec = {k: (v['unstable'], f"{v['min_gain']:+.2e}") for k, v in m.items() if k != 'at_-1.1gc'}
    print(f"| {tag} | {dec} | +g: gain {o['gain']:+.4e} P* {o['P_star']:.3f} hand {hand(o['chiral'], g11)} turn {o['director_turn_deg']:+.2f} "
          f"| -g: gain {at['gain']:+.4e} P* {at['P_star']:.3f} hand {hand(at['chiral'], -g11)} turn {at['director_turn_deg']:+.2f} |")

print('\n## calc 2b')
print('| case | gamma | A | gain | P* | chiral | chiral_AS (all A) | chiral_AperpS | <|S|> | <|S|/|psi|^2> | magnetic | A_perp rms | A_par mean |')
for tag, d in R['calc2b'].items():
    print(f"| {tag} | | | {d['gain']:+.3e} | {d['P_star']:.3f} | {d['chiral']:+.3e} | {d['chiral_AS']:+.3e} | {d['chiral_AperpS']:+.3e} | {d['S_mean']:.4f} | "
          f"{d['S_over_rho_mean']:.4f} | {d['magnetic']:.3e} | {d['A_perp_rms']:.3e} | {d['A_par_mean']:+.3e} |")

print('\n## calc 2c (P5)')
for tag, d in R['calc2c'].items():
    u, r = d['unrelaxed'], d['relaxed']
    print(f"| {tag} | gamma {d['gamma']:.5f} | unrelaxed chiral {u['chiral']:+.2e} (chiral/gamma {u['chiral']/d['gamma']:+.2e}) grad {u['gradient']:.4e} "
          f"| relaxed chiral {r['chiral']:+.3e} grad {r['gradient']:.4e} ratio {d['chiral_over_grad']:+.3e} | gain {r['gain']:+.3e} "
          f"| winding_k {np.round(r['winding_k'], 3).tolist()} rel12 {r['winding_rel12']:+.3f} | amp_min {np.round(r['amp_min'], 4).tolist()} "
          f"| <|S|/rho> {r['S_over_rho_mean']:.4f} | {d['message']} nit {d['nit']} |")
