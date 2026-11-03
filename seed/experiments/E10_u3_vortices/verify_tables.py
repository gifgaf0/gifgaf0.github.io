"""
E10 Amendment A: read-only collection of the verification results into verify_results.json, plus the tables
used in REPORT_verify.md (printed).  Applies the A.4 rule literally.
Run: python3 verify_tables.py > log_verify_tables.txt
"""
import os, json, math
import numpy as np
import verify_common as V

H = V.HERE


def J(name):
    f = os.path.join(H, name)
    return json.load(open(f)) if os.path.exists(f) else None


v1 = {r: J(f'verify_{r}.json') for r in ('V1a', 'V1b', 'V1c')}
v2 = J('verify_V2.json'); v3 = J('verify_V3.json')
S = V.select_S()
rec = V.orig_records()

print('## Point set S')
print('| # | role | bracket (k, q) | k* | q* | omega*/m | flags (orig) | f2 direct (orig) |')
print('|---|---|---|---|---|---|---|---|')
for c in S:
    print(f"| {c['index']} | {c['role']} | {tuple(map(lambda x: tuple(round(v, 2) for v in x), c['between']))} | {c['k_star']:.4f} | "
          f"{c['q_star']:.3f} | {c['omega_star_over_mbulk']:.4f} | {', '.join(c['flags']) or 'central'} | {c['f2_direct']:.3f} |")

# per sign change table: orig vs runs
print('\n## Sign changes: T-cal at the bracketing points (orig / V1a / V1b / V1c)')
print('| # | bracket | T-cal orig | T-cal V1a | T-cal V1b | T-cal V1c | central (V1b) | f2 V1a | f2 V1b | f2 V1c | k* V1b | q* V1b | omega*/m V1b | n | R_eq | Q |')
print('|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|')
by = {r: ({s['index']: s for s in v1[r]['sign_changes']} if v1[r] else {}) for r in v1}
for c in S:
    ij = [V.ij_of(kq) for kq in c['between']]
    To = [rec[x]['Tcal'] for x in ij]
    row = [f"{c['index']}", f"({ij[0][0] * 0.05:.2f},{ij[0][1] * 0.1:.1f})-({ij[1][0] * 0.05:.2f},{ij[1][1] * 0.1:.1f})",
           f"{To[0]:+.5f} / {To[1]:+.5f}"]
    for r in ('V1a', 'V1b', 'V1c'):
        s = by[r].get(c['index'])
        row.append('—' if s is None else f"{s['Tcal'][0]:+.5f} / {s['Tcal'][1]:+.5f}")
    s = by['V1b'][c['index']]
    row.append(str(s['central']))
    for r in ('V1a', 'V1b', 'V1c'):
        s2 = by[r].get(c['index'])
        row.append('—' if s2 is None else f"{s2['f2_direct']:.3f}")
    row += [f"{s['k_star']:.4f}", f"{s['q_star']:.3f}", f"{s['omega_star_over_mbulk']:.4f}", str(s['A1_n']), f"{s['R_eq']:.2f}", f"{s['Q']:.0f}"]
    print('| ' + ' | '.join(row) + ' |')

# per point table at the bracketing points
print('\n## Bracketing points: per-point observables')
for r in ('V1a', 'V1b', 'V1c'):
    if not v1[r]:
        continue
    print(f'\n### {r} (dr = {v1[r]["dr"]}, r_max = {v1[r]["rmax"]}): {v1[r]["n_points"]} points, {v1[r]["n_in_window"]} in window, '
          f'not converged {v1[r]["n_not_converged"]}')
    print('| (k, q) | E | E/E_orig − 1 | T | I_q | I_q/I_orig − 1 | omega/m | leak | r_q rms | r_q/r_q,orig − 1 | alpha | T-cal | T-cal flags | T-cal env | max abs grad |')
    print('|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|')
    br = set()
    for c in (S if r != 'V1c' else [c for c in S if c['index'] == v1['V1b']['V1c_selection']['index']]):
        br |= {V.ij_of(kq) for kq in c['between']}
    for p in v1[r]['points']:
        if (p['i'], p['j']) not in br:
            continue
        o = p['orig']
        print(f"| ({p['k']:.2f}, {p['q']:.1f}) | {p['E']:.9f} | {p['E'] / o['E'] - 1:+.2e} | {p['T']:.6f} | {p['I_q']:.6f} | "
              f"{p['I_q'] / o['I_q'] - 1:+.2e} | {p['omega_over_mbulk']:.6f} | {p['leak']:.1e} | {p['r_charge_rms']:.5f} | "
              f"{p['r_charge_rms'] / o['r_charge_rms'] - 1:+.2e} | {p['alpha']:.6f} | {p['Tcal']:+.6f} | {', '.join(p['Tcal_flags']) or 'central'} | "
              f"{p['Tcal_envelope']:+.6f} | {p['grad_max']:.1e} |")

# trends at the bracketing points of the 14 central sign changes
print('\n## Box / resolution trends (bracketing points of the 14 central sign changes)')
cen_br = set()
for c in S:
    if c['role'] == 'central':
        cen_br |= {V.ij_of(kq) for kq in c['between']}
trend = {}
for r in ('V1a', 'V1b'):
    pts = {(p['i'], p['j']): p for p in v1[r]['points']}
    dI = [pts[x]['I_q'] / pts[x]['orig']['I_q'] - 1 for x in cen_br]
    dR = [pts[x]['r_charge_rms'] / pts[x]['orig']['r_charge_rms'] - 1 for x in cen_br]
    dE = [pts[x]['E'] / pts[x]['orig']['E'] - 1 for x in cen_br]
    trend[r] = dict(n_points=len(cen_br), rel_dI_q=[min(dI), max(dI)], rel_dr_q=[min(dR), max(dR)], rel_dE=[min(dE), max(dE)])
    print(f'{r} vs orig over {len(cen_br)} points: dI_q/I_q in [{min(dI):+.2e}, {max(dI):+.2e}], dr_q/r_q in [{min(dR):+.2e}, {max(dR):+.2e}], '
          f'dE/E in [{min(dE):+.2e}, {max(dE):+.2e}]')
pa = {(p['i'], p['j']): p for p in v1['V1a']['points']}; pb = {(p['i'], p['j']): p for p in v1['V1b']['points']}
dI = [pb[x]['I_q'] / pa[x]['I_q'] - 1 for x in cen_br]; dR = [pb[x]['r_charge_rms'] / pa[x]['r_charge_rms'] - 1 for x in cen_br]
trend['V1b_vs_V1a'] = dict(rel_dI_q=[min(dI), max(dI)], rel_dr_q=[min(dR), max(dR)])
print(f'V1b vs V1a (dr 0.1 -> 0.05): dI_q/I_q in [{min(dI):+.2e}, {max(dI):+.2e}], dr_q/r_q in [{min(dR):+.2e}, {max(dR):+.2e}]')
if v1['V1c']:
    pc = {(p['i'], p['j']): p for p in v1['V1c']['points']}
    print('V1c sign-change bracket, r_max 20 (orig, dr 0.1) / 40 (V1a, dr 0.1) / 40 (V1b, dr 0.05) / 60 (V1c, dr 0.05):')
    trend['V1c_bracket'] = []
    for x in sorted(pc):
        o = pc[x]['orig']
        row = dict(k=pc[x]['k'], q=pc[x]['q'], r_q=[o['r_charge_rms'], pa[x]['r_charge_rms'], pb[x]['r_charge_rms'], pc[x]['r_charge_rms']],
                   I_q=[o['I_q'], pa[x]['I_q'], pb[x]['I_q'], pc[x]['I_q']], leak=[o['leak'], pa[x]['leak'], pb[x]['leak'], pc[x]['leak']])
        trend['V1c_bracket'].append(row)
        print(f"  ({row['k']:.2f},{row['q']:.1f}) r_q {' / '.join(f'{v:.5f}' for v in row['r_q'])};  I_q {' / '.join(f'{v:.6f}' for v in row['I_q'])};  "
              f"leak {' / '.join(f'{v:.1e}' for v in row['leak'])}")

# A.4
verdict = {}
c1 = [s for s in v1['V1b']['sign_changes'] if s['role'] == 'central' and s.get('A4_1_pass')]
verdict['A4_1'] = dict(pass_=bool(c1), n_central_passing=len(c1), indices=[s['index'] for s in c1])
sel = v1['V1b'].get('V1c_selection')
if v1['V1c'] and sel:
    s1b = by['V1b'][sel['index']]; s1c = by['V1c'][sel['index']]
    dT = [abs(a - b) for a, b in zip(s1c['Tcal'], s1b['Tcal'])]
    ok2 = bool(s1c['persists'] and all(d < abs(t) for d, t in zip(dT, s1b['Tcal'])) and
               all(np.sign(a) == np.sign(b) for a, b in zip(s1c['Tcal'], s1b['Tcal'])))
    verdict['A4_2'] = dict(pass_=ok2, index=sel['index'], Tcal_V1b=s1b['Tcal'], Tcal_V1c=s1c['Tcal'], abs_change=dT,
                           reading='|T-cal(V1c) - T-cal(V1b)| < |T-cal(V1b)| at each bracketing point, and no sign flip')
if v2 and v2.get('bracket'):
    rows = v2['bracket']
    okE = all(abs(r['rel_dE_vs_V1b']) < 1e-3 for r in rows)
    T2 = [r['Tcal_fd_2d'] if r['Tcal_fd_2d'] is not None else r['point']['Tcal_envelope'] for r in rows]
    okT = all(np.sign(t) == np.sign(r['V1b']['Tcal']) for t, r in zip(T2, rows))
    verdict['A4_3'] = dict(pass_=bool(okE and okT), E_agree=bool(okE), Tcal_sign_agree=bool(okT),
                           rel_dE=[r['rel_dE_vs_V1b'] for r in rows], Tcal_2d=T2,
                           Tcal_2d_kind=['fd' if r['Tcal_fd_2d'] is not None else 'envelope' for r in rows],
                           Tcal_V1b=[r['V1b']['Tcal'] for r in rows],
                           reading="'T-cal has the same sign at both' read as: the same sign as V1b at each of the two points")
parts = [verdict.get(k, {}).get('pass_') for k in ('A4_1', 'A4_2', 'A4_3')]
if None in parts:
    verdict['A4'] = 'INCOMPLETE'
else:
    if all(parts):
        verdict['A4'] = 'CONFIRMED'
    else:
        cause = []
        if not parts[0]:
            cause.append('resolution (V1b)')
        if not parts[1]:
            cause.append('box (V1c)')
        if not parts[2]:
            cause.append('reduction (V2)')
        verdict['A4'] = 'NOT CONFIRMED: ' + ', '.join(cause)
print('\n## A.4 verdict:', verdict['A4'])
print(json.dumps(verdict, indent=1, default=float))

if v3:
    print('\n## V3 (descriptive only; does not feed A.4)')
    for tag, s in v3['sets'].items():
        st = [c for c in s['sign_changes'] if c['stable_R']]
        print(f"{tag}: {s['n_solves']} solves, {s['n_in_window']} in window, sign changes {len(s['sign_changes'])}, stable {len(st)}, "
              f"min T-cal/E {s['min_Tcal_over_E']:+.4f} at {s['argmin_Tcal_over_E']}")
        for i, e in sorted(s['row_ends'].items(), key=lambda kv: int(kv[0])):
            print(f"   k={int(i) * 0.05:.2f}: last q {e['last_j'] * 0.1:.1f}, {'cap' if e.get('capped') else 'closed'}")
        if st:
            ks = [c['k_star'] for c in st]; qs = [c['q_star'] for c in st]; ws = [c['omega_star_over_mbulk'] for c in st]
            print(f"   stable: k* {min(ks):.3f}-{max(ks):.3f}, q* {min(qs):.2f}-{max(qs):.2f}, omega*/m {min(ws):.4f}-{max(ws):.4f}; "
                  f"flags {sorted({f for c in st for f in c['flags']})}")
    print('classification (A.5):', v3['classification_A5'])

out = dict(label='Exploration, post-hoc verification (PREREG_B2B3 §6, Amendment A). Model units only.',
           point_set=[{k: c[k] for k in ('index', 'role', 'between', 'k_star', 'q_star', 'omega_star_over_mbulk', 'flags', 'f2_direct')} for c in S],
           V1a=v1['V1a'], V1b=v1['V1b'], V1c=v1['V1c'], V2=v2, trends=trend, verdict=verdict,
           V3=(None if v3 is None else dict(note='descriptive only; does not feed A.4', classification=v3['classification_A5'],
                                            stable_counts=v3['stable_counts'],
                                            sets={t: {k: s[k] for k in s if k != 'points'} for t, s in v3['sets'].items()})))
json.dump(out, open(os.path.join(H, 'verify_results.json'), 'w'), default=float, indent=1)
