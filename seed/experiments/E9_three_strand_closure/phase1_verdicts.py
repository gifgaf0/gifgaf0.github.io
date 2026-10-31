"""
E9 option 4, Phase 1: apply PREREG_option4 §5 (P1-P3, P5) as amended by §9.4 to phase1_results.json. Read-only on
the run data; it adds a 'verdicts' block to phase1_results.json and prints the tables used in REPORT_phase1.md.

Readings (flagged in REPORT_phase1.md §8):
- R_f of a main run is the rho of the psi winding zero (mean over the three strands' zeros; plaquette resolution h/2).
- R_f of a C-d run (no psi winding by construction) is the sigma-weighted radius int rho |s|^2 / int |s|^2.
- "within 10 %" is |R_1 - R_2| / mean(R_1, R_2) <= 0.10.
- A single C-d run is classified with the P2 arms minus the two-start test (only one C-d start is specified).
- COLLAPSE: no winding zero left (main) / no sigma left (C-d), or R_f < 2 xi = 1.41.
  EXPANDS: R_f within the 4-unit edge band (R_f > 28). LEAK: leak > 1 % or omega >= m_vac.
  A run that hit maxiter is MARGINAL (not an end state). Otherwise: finite R_f, omega < m_vac, leak < 1 %, E < m_vac Q.
Run: python3 phase1_verdicts.py
"""
import json, numpy as np

XI2 = np.sqrt(2.0)          # 2 xi, xi = 1/sqrt 2
EDGE = 32.0 - 4.0
d = json.load(open('phase1_results.json'))
R = d['runs']; sel = d['selection']
k = sel['k_star']


def arm(o, use_sigma_radius=False):
    f = o['final']
    if o['hit_maxiter']:
        return 'MARGINAL (hit maxiter)', None
    if use_sigma_radius:
        Rf = f['R_sigma_weighted'] if f['I'] > 1e-6 else None
        ring = Rf is not None and f['sigma_max'] > 0.05
    else:
        Rf = f['R_core'] if (f['one_zero_per_strand'] and all(w == 1 for w in f['net_winding'])) else None
        ring = Rf is not None
    if not ring or Rf < XI2:
        return 'COLLAPSE', Rf
    if Rf > EDGE:
        return 'EXPANDS', Rf
    if f['leak_frac'] > 0.01 or f['omega_over_mvac'] >= 1:
        return 'LEAK', Rf
    if not f['E_lt_mvacQ']:
        return 'MARGINAL (E >= m_vac Q)', Rf
    return 'candidate (finite R_f, omega < m_vac, leak < 1 %, E < m_vac Q)', Rf


V = {}
# P1: C-a must collapse
ca = R['Ca_n0_Q0']['final']
p1 = (not any(ca['winding_zeros'])) and abs(ca['E']) < 1e-3 and ca['I'] < 1e-6
V['P1'] = dict(holds=bool(p1), C_a_final_E=ca['E'], C_a_zeros=[len(z) for z in ca['winding_zeros']], C_a_I=ca['I'])
print('P1 (C-a collapses):', p1, f"E = {ca['E']:.2e}, I = {ca['I']:.2e}")

for n in (7, 10):
    a, b = R[f'main_n{n}_R1.0'], R[f'main_n{n}_R1.5']
    (va, Ra), (vb, Rb) = arm(a), arm(b)
    same = Ra is not None and Rb is not None and abs(Ra - Rb) / (0.5 * (Ra + Rb)) <= 0.10
    main = 'STABLE (axisymmetric)' if (va.startswith('candidate') and vb.startswith('candidate') and same) else \
        (va if va == vb else f'{va} / {vb}')
    cd = R[f'Cd_n{n}']; vcd, Rcd = arm(cd, use_sigma_radius=True)
    cd_stable = vcd.startswith('candidate')
    if main.startswith('STABLE'):
        q = 'STABLE, string not required' if cd_stable else (
            'STABLE, string-supported' if vcd in ('COLLAPSE', 'LEAK') else f'STABLE; C-d ended {vcd} (not in the §9.4 table)')
    else:
        q = main
    ce = R['Ce_Q7' if n == 7 else 'Ce_Q10']['final']
    Em = 0.5 * (a['final']['E'] + b['final']['E'])
    Req = n / k; Rf = 0.5 * (Ra + Rb) if (Ra and Rb) else None
    p3 = dict(R_eq=Req, R_f=Rf, rel=(Rf / Req - 1) if Rf else None, holds=bool(Rf and abs(Rf / Req - 1) <= 0.25),
              R_sigma_weighted=a['final']['R_sigma_weighted'], rel_sigma=a['final']['R_sigma_weighted'] / Req - 1)
    V[f'n{n}'] = dict(start_R1=dict(arm=va, R_f=Ra), start_R15=dict(arm=vb, R_f=Rb),
                      same_R_f_within_10pct=bool(same), main=main,
                      C_d=dict(arm=vcd + ' (single run; two-start test not applicable)', R_f_sigma=Rcd,
                               E_Cd_minus_E_main=cd['final']['E'] - Em),
                      verdict=q, E_main=Em, mvacQ=a['final']['mvacQ'], E_over_mvacQ=Em / a['final']['mvacQ'],
                      E_lump=ce['E'], E_minus_E_lump=Em - ce['E'],
                      C_e_qualifier='metastable (E_lump < E)' if ce['E'] < Em else 'not metastable vs lump',
                      E_Cd_minus_E_lump=cd['final']['E'] - ce['E'], P3=p3)
    print(f'n = {n}: starts {va} (R_f={Ra}) / {vb} (R_f={Rb}); same R_f within 10 %: {same}; main: {main}')
    print(f'   C-d: {vcd}, R_sigma = {Rcd:.3f}, E_Cd - E_main = {cd["final"]["E"] - Em:+.2f}  ->  {q}')
    print(f'   C-e: E_lump = {ce["E"]:.2f}, E - E_lump = {Em - ce["E"]:+.2f} -> {V[f"n{n}"]["C_e_qualifier"]}')
    print(f'   P3: R_f = {Rf}, R_eq = {Req:.3f}, R_f/R_eq - 1 = {p3["rel"]:+.3f}, holds (25 %): {p3["holds"]}')
s7, s10 = V['n7']['verdict'], V['n10']['verdict']
V['n_dependence'] = 'n-dependent (n = 10 carries forward)' if s7.split(',')[0] != s10.split(',')[0] else 'same at n = 7 and n = 10'
V['carried_forward'] = s10
V['phase2'] = 'runs' if s10 == 'STABLE, string-supported' else 'does not run (§9.4: Phase 2 runs only on STABLE, string-supported)'
cb, cc = R['Cb_n7_Q0']['final'], R['Cc_n0_Q7']['final']
V['P5'] = dict(C_b=dict(E=cb['E'], I=cb['I'], zeros=[len(z) for z in cb['winding_zeros']]),
               C_c=dict(E=cc['E'], I=cc['I'], zeros=[len(z) for z in cc['winding_zeros']], R_sigma=cc['R_sigma_weighted'],
                        E_minus_E_lump_Q7=cc['E'] - R['Ce_Q7']['final']['E']))
print('n-dependence:', V['n_dependence'], '| carried forward:', V['carried_forward'], '| Phase 2:', V['phase2'])
print('P5:', json.dumps(V['P5']))
d['verdicts'] = V
json.dump(d, open('phase1_results.json', 'w'), default=float)
