"""Assemble crosscheck.json (second cross-check pass).  Run after xc2_compare.py and xc2_audit.py."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
c = json.load(open(os.path.join(HERE, 'xc2_compare.json')))
vals = json.load(open(os.path.join(HERE, 'xc2_audit_values.json')))['independent_values']
oc = json.load(open(os.path.join(HERE, 'xc2_origcode_dsv_example.json')))
col = json.load(open(os.path.join(HERE, 'xc2_origcode_col099.json')))
text = json.load(open(os.path.join(HERE, 'xc2_audit_text.json')))

out = dict(
    experiment='E1 phi^4 in 1+1 D (PLAN.md section 4, E1a-E1e): independent cross-check (second pass)',
    methods=dict(
        code1='xc_core.py / xc_e1c.py / xc_e1d.py: 6th-order centred FD + classical RK4, dx = 0.08, dt = 0.032, cubic sponge; '
              'xc_e1b.py: Fourier pseudo-spectral + RK4, x0 = 15, periodic box of half-length 260 with sponge; '
              'xc_e1a.py: scipy solve_bvp collocation and Chebyshev collocation',
        code2='xc2_spec.py: Fourier pseudo-spectral, linear Klein-Gordon part propagated exactly, nonlinear force and sponge as '
              'kicks, Strang splitting composed to 4th order (Yoshida); dx = 0.1 (0.05 checks), dt = 0.02',
        original='4th-order FD + velocity Verlet, dx = 0.1 (0.05), dt = 0.4 dx, quadratic sponge',
        original_code_diagnosis='xc2_diag_origcode_dsv.py, xc2_diag_origcode_col099.py: the original e1c_dsv.py/phi4core.py, '
                                'run unmodified from a scratch copy at other (dx, dt)'),
    numbers=c,
    original_code_diagnosis=dict(dsv_example=oc, omega_099_column=col),
    independent_values=vals,
    claim_audit=text['claim_audit'],
    issues=text['issues'],
    overall=text['overall'],
    summary=text['summary'],
)
json.dump(out, open(os.path.join(HERE, 'crosscheck.json'), 'w'), indent=1, default=str)
print('wrote crosscheck.json:', len(vals), 'values,', len(text['claim_audit']), 'claims,', len(text['issues']), 'issues')
