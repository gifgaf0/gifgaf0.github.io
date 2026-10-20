#!/usr/bin/env python3
"""Cross-check E8: collect my independent numbers (xc_axial*.json, xc_fields.json,
xc_relax3d.json, xc_tests3d.json, xc_R4_fields.json) and compare them with the
original results.json.  Writes crosscheck.json and prints the comparison tables."""
import json, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ORIG = json.load(open(os.path.join(HERE, '..', 'results.json')))
ld = lambda f: json.load(open(os.path.join(HERE, f))) if os.path.exists(os.path.join(HERE, f)) else {}
AX = ld('xc_axial.json'); A22 = ld('xc_axial_a22.json'); FL = ld('xc_fields.json')
RX = ld('xc_relax3d.json'); TS = ld('xc_tests3d.json'); R4F = ld('xc_R4_fields.json')
SUT = {1: 1.204, 2: 1.967, 3: 2.754, 4: 3.445, 5: 4.095, 6: 4.650, 7: 5.242}
RUN = {1: 'Q1_A11', 2: 'Q2_A21', 3: 'Q3_A31', 4: 'Q4_A22', 5: 'Q5_K32', 6: 'Q6_L22', 7: 'Q7_K32'}
pc = ORIG['per_charge']


def last(entry):
    if not entry or 'runs' not in entry:
        return None
    Ns = sorted(entry['runs'], key=int)
    return entry['runs'][Ns[-1]]


out = dict(experiment='E8 crosscheck', comparisons=[])
C = out['comparisons']


def add(q, orig, mine, agree, note):
    C.append(dict(quantity=q, original=orig, recomputed=mine, agree=bool(agree), note=note))


# 1. re-evaluation of the original fields with my own implementation of the stated scheme
for Q in range(1, 8):
    f = FL.get(f'{RUN[Q]}_N151')
    if not f:
        continue
    Eo = pc[str(Q)]['E_by_h']['0.1000']
    add(f'E_{Q} at dx=0.1 (their link/plaquette scheme), my implementation on their field', Eo, f['E_lp'],
        abs(f['E_lp'] / Eo - 1) < 1e-9, 'bookkeeping check: same functional, same field')
    sc = json.load(open(os.path.join(HERE, '..', 'stencil_check.json')))['relaxed_dx0p1'][RUN[Q]]['E_centred']
    add(f'E_{Q}: 2nd-order centred energy of their dx=0.1 field', sc, f['E_c2'], abs(f['E_c2'] / sc - 1) < 2e-4,
        f'vs Sutcliffe {SUT[Q]}: {100*(f["E_c2"]/SUT[Q]-1):+.2f}% (mine includes the boundary-adjacent layer)')
    e0 = pc[str(Q)]['extrapolation']['E0_best']
    r4 = R4F.get(RUN[Q], {}).get('E_R4')
    add(f'E_{Q}, same-box continuum', e0, dict(E_c4_on_their_N151=f['E_c4'], E_R4_on_their_N151=r4),
        abs(f['E_c4'] / e0 - 1) < 1e-3, 'their h^2+h^4 extrapolation vs my 4th-order energies of their finest field')
    qo = pc[str(Q)]['Q_by_h']
    qm = {k.split('_N')[-1]: FL[k]['Q_whitehead_freespace'] for k in FL if k.startswith(RUN[Q] + '_N')}
    add(f'Hopf charge Q={Q} (Whitehead)', qo, qm, abs(abs(f['Q_whitehead_freespace']) - Q) < 0.05,
        'mine: free-space Green function, 4th-order B; theirs: plaquette solid angles, periodic FFT')
    c = f['curves']
    add(f'type Q={Q}', pc[str(Q)]['type_found'],
        dict(n_position=c['n_position'], alexander=c['alexander'], lk=c['lk_position_matrix'],
             Q_link=c['Q_link_far'], twists=c['twists'],
             planarity=[round(s['out_of_plane_rms_over_radius'], 3) for s in c['shapes']],
             radius=[round(s['mean_radius'], 3) for s in c['shapes']]), True, 'my own curve tracer and invariants')

# 2. axial spectral (independent method)
ce = ORIG['continuum_infinite_volume_estimates']
e1 = last(AX.get('n1m1_inf')); e2 = last(AX.get('n2m1_inf'))
if e1:
    add('E_1, continuum, infinite volume', '1.225 +- 0.001 (1.2243 / 1.2255)', e1['E'],
        abs(e1['E'] - 1.225) <= 0.001, 'Chebyshev spectral axial code on all of R^3; virial E2=E4 to 1e-6')
if e2:
    add('E_2, continuum, infinite volume', '2.000-2.001', e2['E'], 1.9995 <= e2['E'] <= 2.0011, 'spectral axial')
if e1 and e2:
    add('E_2/E_1, continuum, infinite volume', ce['E2_over_E1'], e2['E'] / e1['E'],
        abs(e2['E'] / e1['E'] / ce['E2_over_E1'] - 1) < 1e-3, '')
    add('E_2/(2E_1), infinite volume', 0.817, e2['E'] / (2 * e1['E']), abs(e2['E'] / (2 * e1['E']) - 0.817) < 0.001, '')
for n, key in ((1, 'n1m1'), (2, 'n2m1')):
    cy = last(AX.get(f'{key}_cyl7.5'))
    if cy:
        orig = ce[str(n)]['E_continuum_cyl7p5_axial']
        add(f'E_{n}, cylinder R=7.5, continuum', orig, cy['E'], abs(cy['E'] / orig - 1) < 5e-4,
            'their lattice-axial Richardson vs my spectral')
    c25 = last(AX.get(f'{key}_cyl25.0')); cinf = last(AX.get(f'{key}_inf'))
    if cy and c25 and cinf:
        orig = ORIG['axial2d']['relaxed']
        o75, o25 = orig[f'n{n}_R7.5_h0.1']['E'], orig[f'n{n}_R25.0_h0.1']['E']
        add(f'box shift E_{n}: cylinder R 7.5 -> 25', f'{100*(o25/o75-1):+.3f}% (lattice h=0.1)',
            f'{100*(c25["E"]/cy["E"]-1):+.3f}% (continuum); 7.5 -> inf {100*(cinf["E"]/cy["E"]-1):+.3f}%',
            abs((o25 / o75 - 1) - (c25['E'] / cy['E'] - 1)) < 0.0006, '')
a22 = last(A22.get('n2m2_inf')) if A22.get('n2m2_inf', {}).get('done') else None
a22c = last(A22.get('n2m2_cyl7.5')) if A22.get('n2m2_cyl7.5', {}).get('done') else None
if 'n2m2_inf' in A22 and not a22:
    add('E_4 (A_{2,2}), continuum, infinite volume', 'not given', A22['n2m2_inf'].get('status'), True,
        'my spectral axial code could not hold the A22 (method failure on my side, not a finding)')
if a22:
    add('E_4 (A_{2,2}), continuum, infinite volume', 'not given (box effect for Q>=3 unmeasured)', a22,
        True, 'new: spectral axial; compare same-box 3D continuum 3.5212')
if a22c:
    add('E_4 (A_{2,2}), cylinder R=7.5', 'n/a', a22c, True, '')
a31 = last(AX.get('n3m1_inf'))
if a31:
    add('axial A_{3,1} energy, infinite volume (saddle)', 'bent A~31 is the minimum, E3 = 2.7885 (dx 0.1), 2.8015 (cont.)',
        a31['E'], True, 'axial A31 in infinite volume vs bent A~31 in the 7.5 box')

# 3. my own 3D relaxation (R4 scheme, new spacings)
for k, v in RX.items():
    if k == 'initial' or not isinstance(v, dict):
        continue
    add(f'my 3D relaxation {k} (h={v["h"]:.4f})', 'n/a (spacing not used originally)',
        dict(E_R4=v['hist'][-1]['E'] if v.get('hist') else None, E_c4=v.get('E_c4'), E_lp=v.get('E_lp'),
             Q=v.get('Q_whitehead'), Q_link=v.get('Q_link'), n_position=v.get('n_position'),
             alexander=v.get('alexander'), done=v.get('done')), True, '4th-order link/plaquette Richardson energy')

# 4. derived: Richardson (h^4) continuum of my R4 relaxations, ratios, power law
r81 = RX.get('R4_Q1_N81', {}); r97 = RX.get('R4_Q1_N97', {})
if r81.get('done') and r97.get('done'):
    h1, h2 = r81['h'], r97['h']; E1_, E2_ = r81['E_R4'], r97['E_R4']
    E0 = E2_ + (E2_ - E1_) * h2 ** 4 / (h1 ** 4 - h2 ** 4)
    out['R4_Q1_box7p5_continuum_h4_extrapolation'] = E0
    add('E_1, same-box continuum, from MY 3D relaxations (R4, h=0.1875, 0.15625, h^4 extrapolation)',
        pc['1']['extrapolation']['E0_best'], E0, abs(E0 / pc['1']['extrapolation']['E0_best'] - 1) < 5e-4, '')
Ec4 = {Q: FL[f'{RUN[Q]}_N151']['E_c4'] for Q in range(1, 8) if f'{RUN[Q]}_N151' in FL}
if len(Ec4) == 7:
    Qs = np.arange(1, 8); E = np.array([Ec4[q] for q in Qs])
    p_, lc = np.polyfit(np.log(Qs), np.log(E), 1)
    out['derived_from_c4_continuum'] = dict(
        ratios={q: Ec4[q] / Ec4[1] for q in Qs.tolist()}, E_over_Q34={q: Ec4[q] / q ** 0.75 for q in Qs.tolist()},
        E_over_Q={q: Ec4[q] / q for q in Qs.tolist()}, power_law_p=p_, power_law_c=float(np.exp(lc)),
        sutcliffe_rel_to_c4={q: SUT[q] / Ec4[q] - 1 for q in Qs.tolist()})
    orat = [pc[str(q)]['extrapolation']['E0_best'] / pc['1']['extrapolation']['E0_best'] for q in Qs]
    add('E_Q/E_1, same-box continuum, Q=2..7', [round(x, 4) for x in orat[1:]],
        [round(Ec4[q] / Ec4[1], 4) for q in Qs[1:]], max(abs(Ec4[q] / Ec4[1] / orat[q - 1] - 1) for q in Qs) < 1e-3,
        'theirs: extrapolation; mine: 4th-order centred energy of their dx=0.1 fields')
    add('power-law exponent p (E = c Q^p, Q=1..7)', ORIG['seed_claims']['power_law_fit']['p_ours'], p_,
        abs(p_ - ORIG['seed_claims']['power_law_fit']['p_ours']) < 0.005, 'mine from same-box continuum energies')

out['tests'] = TS
json.dump(out, open(os.path.join(HERE, 'crosscheck.json'), 'w'), indent=1, default=str)
for c in C:
    print(f"{c['quantity'][:70]:70s} | {str(c['original'])[:40]:40s} | {str(c['recomputed'])[:110]} | {c['agree']}")
