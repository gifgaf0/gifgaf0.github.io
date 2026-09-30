#!/usr/bin/env python3
"""sa_verify_pinned_inputs.py -- G-MSCS-A (staging memo v2, section 9): an independent check of the pinned-inputs file,
written separately from the builder (no shared code) for the author's pre-lock verification. Revised after the v2 audit:
it trusts nothing in the file under test -- the keys, arms, pointers, constants, tokens and structure it expects are
written into this script -- and it re-derives EVERY leaf of the file's `derived` block with its own code.

Checks:
 (1) the seven sources on disk carry the md5s and byte counts of record (written here), and the file's `sources` block
     says the same;
 (2) the file's `provenance` block equals the pointer map written here, field for field (a redirected pointer fails);
     every `raw` value equals its source value through that pointer, bit for bit; the `raw` block holds exactly the
     expected leaves (none missing, none extra); the number of comparisons equals the expected number;
 (3) `constants`, `tokens`, `structure`, `grids`, `_meta` (the embedded builder md5 included: it must name the builder
     of record, written here) and `rms_exact_check` equal the values written here (the rms closed forms re-verified in
     exact rational arithmetic);
 (4) a full re-derivation of `derived` from the file's own `raw` block with this script's code: every leaf of the
     file's `derived` block is compared (floats within |d| <= 1e-12*|x| + 1e-16 -- a few leaves differ from the
     builder's in the last bits because the arithmetic is ordered differently; types, strings, booleans and nulls
     exactly), the two leaf sets are identical, and the count is reported. Tampering below that tolerance is caught
     by the whole-file md5, which the author compares with the md5 of record;
 (5) no point count is written in the file (rule 4).

Usage:  python3 sa_verify_pinned_inputs.py REPO_DIR PINNED_FILE [BUILDER_FILE]
        (with BUILDER_FILE, the md5 embedded in the file must equal that file's md5)
Exit:   0 all checks pass; 1 any check fails; 2 usage.  Prints no value that the memo does not already print."""
import hashlib, json, math, os, sys
from fractions import Fraction

SOURCES = {
    'G2chat': ('gmscs2_gate/g_mscs2_chatleg_checkpoint.json', '1c5b6b59829d2a6b9ae2b1a7a016832d', 31575),
    'G2cc':   ('gmscs2_gate/g_mscs2_ccleg_checkpoint.json',   '9961745d1e1857cfab6445d4754b5060', 68540),
    'G1chat': ('gmscs1_gate/g_mscs1_chatleg_checkpoint.json', 'c04c0b8ea34cfe60f231aa06828e6ce4', 33289),
    'G1cc':   ('gmscs1_gate/g_mscs1_ccleg_checkpoint.json',   '249e11dd53c4cb82f302b15d3c94c337', 24415),
    'DK24':   ('gmscs2_gate/diag_kappa24.json',               'b7952dfcaddcd1d98e424aee8ce5231f', 1917),
    'DQF':    ('gmscs2_gate/diag_quadform_basis.json',        'd84aa1fdce7dea1b1a5d24dfb8f13c18', 1119),
    'CI1':    ('gci1_gate/ci1_phase3_cc_r2.json',             '845ae6beb1b90fe34c540f843ffdb9f5', 45760),
}
HEXK = ['hex_step|a', 'hex_step|b', 'hex_gem8|a', 'hex_gem8|b']
CUBK = ['cubic_step|001', 'cubic_step|111', 'cubic_gem8|001', 'cubic_gem8|111']
ALLK = HEXK + CUBK
ARMS = ['E2_Hill', 'E2_HSmean', 'h_Hill']
PRIM = ['hex_step|a', 'hex_gem8|a', 'cubic_step|001', 'cubic_gem8|001']
TOL_REL, TOL_ABS = 1e-12, 1e-16

# -------------------------------------------------------------------- the expected pointer map, generated from a table
KAPPA_NAME = {('E2_Hill', 't4'): 'kappa44_E2', ('E2_HSmean', 't4'): 'kappa44_E2_HS', ('h_Hill', 't4'): 'kappa44_h',
              ('E2_Hill', 't2'): 'kappa2_E2', ('E2_HSmean', 't2'): 'kappa2_E2_HS', ('h_Hill', 't2'): 'kappa2_h'}
GRID_NAME = {'E2_Hill': 'r_agg_E2_VRH', 'E2_HSmean': 'r_agg_E2_HS', 'h_Hill': 'r_agg_h_VRH'}
S_NAME = {('E2_Hill', 't4'): 'S4_E2', ('h_Hill', 't4'): 'S4_h', ('E2_Hill', 't2'): 'S_t_E2', ('h_Hill', 't2'): 'S_t_h'}
K3_NAME = {'t4': 'kappa444_E2', 't2': 'kappa3_E2'}
HAS_KAPPA_CC = {('E2_Hill', 't4'), ('E2_HSmean', 't4'), ('h_Hill', 't4'), ('E2_Hill', 't2'), ('h_Hill', 't2')}

def expected_provenance():
    P = {}
    def put(dest, src, ptr, scope='all'):
        P['keys/<K>/' + dest] = {'src': src, 'pointer': ptr, 'scope': scope}
    for arm in ARMS:
        for fam in ('t4', 't2'):
            g = 'G2' if fam == 't4' else 'G1'
            base = 'arms/%s/%s/' % (arm, fam)
            put(base + 'kappa', g + 'chat', '/phase2/{K}/' + KAPPA_NAME[(arm, fam)])
            put(base + 'grid', g + 'chat', '/phase2/{K}/' + GRID_NAME[arm])
            if (arm, fam) in HAS_KAPPA_CC:
                put(base + 'kappa_cc', g + 'cc', '/phase2/{K}/' + KAPPA_NAME[(arm, fam)])
            if (arm, fam) in S_NAME:
                put(base + 'S', g + 'chat', '/phase2/{K}/' + S_NAME[(arm, fam)])
                put(base + 'S_cc', g + 'cc', '/phase2/{K}/' + S_NAME[(arm, fam)])
            if arm == 'E2_Hill':
                put(base + 'kappa3', g + 'chat', '/phase2/{K}/' + K3_NAME[fam])
                put(base + 'kappa3_cc', g + 'cc', '/phase2/{K}/' + K3_NAME[fam])
    for q, leg in (('kappa22', 'chat'), ('kappa24', 'chat'), ('kappa44', 'chat')):
        put('quadform/%s_fit7' % q, 'G2' + leg, '/phase2/{K}/quadform/' + q)
    put('quadform/kappa22_fit7_cc', 'G2cc', '/phase2/{K}/quadform/kappa22')
    put('quadform/grid5x5_cc', 'G2cc', '/phase2/{K}/quadform/x_grid_r_agg_E2_VRH')
    put('quadform/cubic_terms_cc', 'G2cc', '/phase2/{K}/quadform/x_cubic_terms_discarded')
    put('quadform/reading_cc', 'G2cc', '/phase2/{K}/quadform/x_reading')
    put('quadform/basis_k7_chat', 'DQF', '/{K}/k7', 'dqf')
    put('quadform/basis_k12_chat', 'DQF', '/{K}/k12', 'dqf')
    put('kappa24_bi_chat', 'DK24', '/{K}/kappa24_richardson')
    put('kappa24_bi_cc', 'G2cc', '/phase2/{K}/kappa24_richardson')
    put('b1_Hill', 'G2chat', '/phase2/{K}/biref_b1_VRH')
    put('b1_Hill_cc', 'G2cc', '/phase2/{K}/biref_b1_VRH')
    put('pure_l2_change_t1', 'DK24', '/{K}/pure_l2_r_agg_change_t1', 'cubic')
    put('A31_mixed_change_cc', 'G2cc', '/extras/A3_diagnostics/A-3.1_mixed_r_agg_change_A29/{K}', 'cubic')
    P['grids/t_grid'] = {'src': 'G2chat', 'pointer': '/t4_grid', 'scope': 'global'}
    P['grids/t2t4_axis'] = {'src': 'G2chat', 'pointer': '/t2t4_grid', 'scope': 'global'}
    P['raw/regime/d_EM'] = {'src': 'CI1', 'pointer': '/per_oom/x1/W_EM_union/0/1', 'scope': 'global'}
    return P

EXPECTED_CONSTANTS = {
    'D': 0.25, 'mu': 0.10, 'KD_CLIP': 0.3, 'tau_agg': 1e-6, 'kappa_floor': 1e-6, 'zero_snap': 1e-12,
    'trunc_threshold': 0.10, 'nullfloor_threshold': 0.10, 'recon_tol_abs_E2_Hill': 1e-8, 'recon_tol_rel_robust': 1e-3,
    'pin_twoleg_tol_rel': 1e-4, 'zero_ctrl_tol_abs': 1e-12, 'l2null_t1_tol_abs': 1e-12, 'edge_twoleg_tol_rel': 1e-10,
    'mono_tol_rel': 1e-14, 'pin_derived_tol_rel': 1e-12, 'pin_derived_tol_abs': 1e-16, 'oom_factors': [0.1, 1.0, 10.0],
    'synthetic_t': [0.01, 0.1, 0.5], 'synthetic_t_tight': 1e-9, 'synthetic_band_fractions': [0.25, 0.75],
    'synthetic_k': {'silent': 1.0, 'void': 1e33},
    'synthetic_rules': {
        'margin_positive': '[h + f1*(w - h), h + f2*(w - h)], h = unions.hull_all[1], w = unions.widened_all[1]',
        'margin_negative': '[w + f1*(h - w), w + f2*(h - w)], w = unions.widened_all[0], h = unions.hull_all[0]',
        'robustness_only_positive': '[p + f1*(q - p), p + f2*(q - p)], p = unions.widened_primary[1], q = unions.hull_all[1]'},
    'rms': {'hexP2': math.sqrt(0.2), 'hexP4': 1.0 / 3.0, 'cubK4': math.sqrt(4.0 / 21.0)},
    'rms_closed_form': {'hexP2': 'sqrt(1/5)', 'hexP4': '1/3', 'cubK4': 'sqrt(4/21)'},
    'fam_rms': {'t2': 'hexP2', 't4_hex': 'hexP4', 't4_cubic': 'cubK4'},
}
EXPECTED_TOKENS = {
    'odf_reading': ['none', 'uniform', 'hexP2', 'hexP4', 'hexP2P4', 'cubK4', 'cubP2-i', 'cubP2-ii', 'cubP2K4-i', 'cubP2K4-ii'],
    'delta_def': 'tensor_over_EM_minus_1', 'class': ['spd'], 'reading_conformant': ['bound'],
    'reading_frozen_list': ['bound', 'ceiling', 'margin', 'criterion'], 'geom': ['single', 'population'], 'q': ['phase', 'group'],
}
EXPECTED_STRUCTURE = {
    'keys': ALLK, 'hex_keys': HEXK, 'cubic_keys': CUBK, 'arms': ARMS, 'primary': {'arm': 'E2_Hill', 'keys': PRIM},
    'robustness': {'arms': ['E2_HSmean', 'h_Hill'], 'keys': ['hex_step|b', 'hex_gem8|b', 'cubic_step|111', 'cubic_gem8|111']},
    'mapped_families': {'hex': ['t4', 't2'], 'cubic': ['t4']}, 'null_families': {'cubic': ['t2']},
    'kill_test_set': 'every key x every arm (E-SA-9(a)); the primary-only union is serialized for information',
}
EXPECTED_GRIDS_FIXED = {
    'fit_window': 'abs(t) <= D, inclusive (the window both banked legs used; H-CC-1)',
    'richardson_pairs': {'one_param': [0.05, 0.1], 'two_param': [0.125, 0.25]},
    'richardson_formulas': {
        'odd':   '[4*O(h1) - O(h2)]/3, O(h) = [r(h) - r(-h)]/(2h)',
        'even':  '[4*E(h1) - E(h2)]/3, E(h) = [r(h) + r(-h) - 2*r(0)]/(2h^2)',
        'mixed': '[4*M(h1) - M(h2)]/3, M(h) = [R(h,h) - R(h,-h) - R(-h,h) + R(-h,-h)]/(4h^2)'},
    'grid5x5_layout': 'row-major, t2 outer, t4 inner: index = 5*i + j for (t2_axis[i], t4_axis[j])',
    'area_grid': {'lo': -0.25, 'hi': 0.25, 'nodes_per_axis': 201, 'node': 'lo + i*(hi - lo)/(nodes_per_axis - 1)'},
}
EXPECTED_META = {
    'gate': 'G-MSCS-A', 'file_schema': 'g_mscs_a_pinned_inputs/1', 'builder': 'sa_build_pinned_inputs.py',
    'base_ledger_md5': 'd4c42a53cbd6d325ebc740879288e844',
    'elections_applied': {'E-SA-0': 'a', 'E-SA-1': 'a', 'E-SA-2': 'a', 'E-SA-3': 'a', 'E-SA-4': 'a', 'E-SA-5': 'a',
                          'E-SA-6': 'a', 'E-SA-7': 'base 05302210 + the G-MSCS1 stratum', 'E-SA-8': 'a', 'E-SA-9': 'a',
                          'E-SA-10': 'a', 'E-SA-11': 'a'},
    'cubic_term_order': ['t2^3', 't2^2*t4', 't2*t4^2', 't4^3'],
    'dqf_basis_order': ['t2^2', 't2*t4', 't4^2', 't2^3', 't2^2*t4', 't2*t4^2', 't4^3', 't2^4', 't2^3*t4', 't2^2*t4^2', 't2*t4^3', 't4^4'],
    'contents': 'banked values by named key + fixed constants, grid generators and tokens + a derived reference section; no anchor value; no observational number; no point count',
    'dqf_basis_note': 'index order of the chat quadform-basis diagnostic; asserted by this builder: k7[0..2] equal the fit7 kappa22, kappa24, kappa44 of the same key bit for bit and k7[3..6] equal the CC named cubic terms to 1e-4 relative; k12[3..6] equal k7[3..6] to 1e-8 relative (the shared order); the k12 quartic indices 7..11 follow the monomial order and are not independently confirmed (no instrument reads them)',
}
EXPECTED_BUILDER_MD5 = '8189100ede80eac360b25a146e580abf'   # the builder of record (staging memo v2); the file must name it

fails = []
def check(ok, what):
    if not ok:
        fails.append(what)
    return ok

def get(doc, pointer):
    node = doc
    for part in pointer.lstrip('/').split('/'):
        part = part.replace('~1', '/').replace('~0', '~')
        node = node[int(part)] if isinstance(node, list) else node[part]
    return node

def flat(node, prefix=''):
    """leaf paths of a JSON tree; lists of numbers are expanded element by element"""
    out = {}
    if isinstance(node, dict):
        for k, v in node.items():
            out.update(flat(v, (prefix + '/' + k) if prefix else k))
    elif isinstance(node, list):
        for i, v in enumerate(node):
            out.update(flat(v, '%s[%d]' % (prefix, i)))
    else:
        out[prefix] = node
    return out

def same(a, b):
    if type(a) != type(b):
        return False
    if isinstance(a, float):
        return abs(a - b) <= TOL_REL * abs(b) + TOL_ABS
    return a == b

# ------------------------------------------------------------------------------- the independent re-derivation
def rederive(raw, C, G):
    D, MU, SNAP, KF = C['D'], C['mu'], C['zero_snap'], C['kappa_floor']
    T, AX = G['t_grid'], G['t2t4_axis']
    a1, a2 = G['richardson_pairs']['one_param']
    b1, b2 = G['richardson_pairs']['two_param']
    inside = [i for i in range(len(T)) if -D <= T[i] <= D]

    def val(g, t):
        return dict(zip(T, g))[t]
    def even(g):
        e = lambda h: (val(g, h) + val(g, -h) - 2.0 * val(g, 0.0)) / (2.0 * h * h)
        return (4.0 * e(a1) - e(a2)) / 3.0
    def odd(g):
        o = lambda h: (val(g, h) - val(g, -h)) / (2.0 * h)
        return (4.0 * o(a1) - o(a2)) / 3.0
    def grid5(v):
        n = len(AX)
        return {(AX[i], AX[j]): v[i * n + j] for i in range(n) for j in range(n)}
    def rich5(R, kind):
        def f(h):
            if kind == '22':
                return (R[(h, 0.0)] + R[(-h, 0.0)] - 2.0 * R[(0.0, 0.0)]) / (2.0 * h * h)
            if kind == '44':
                return (R[(0.0, h)] + R[(0.0, -h)] - 2.0 * R[(0.0, 0.0)]) / (2.0 * h * h)
            return (R[(h, h)] - R[(h, -h)] - R[(-h, h)] + R[(-h, -h)]) / (4.0 * h * h)
        return (4.0 * f(b1) - f(b2)) / 3.0
    def relative(x, y):
        return abs(x - y) / max(abs(x), abs(y))
    def token(k, fam):
        if k in HEXK:
            return 'hexP2' if fam == 't2' else 'hexP4'
        return 'cubP2-i' if fam == 't2' else 'cubK4'

    fam_out, reach, zero, n1, n2, n3, n4, hq = {}, {}, {}, {}, {}, {}, {}, {}
    for k in ALLK:
        rk = raw['keys'][k]
        mapped = ('t4', 't2') if k in HEXK else ('t4',)
        fam_out[k], reach[k], zero[k] = {}, {}, {}
        for arm in ARMS:
            fam_out[k][arm] = {}
            for fam in ('t4', 't2'):
                f = rk['arms'][arm][fam]
                kb = even(f['grid'])
                e = {'odf_reading': token(k, fam), 'kappa': f['kappa'], 'kappa_bi': kb,
                     'fit_res_rel': (abs(f['kappa'] - kb) / abs(kb)) if abs(kb) > KF else None,
                     'S_bi': odd(f['grid']), 'S_fit': f['S'] if 'S' in f else None,
                     'r0': val(f['grid'], 0.0), 'mapped': fam in mapped}
                if fam in mapped and 'kappa3' in f:
                    e['recon_max_abs'] = max(abs(f['grid'][i] - (f['S'] * T[i] + f['kappa'] * T[i] ** 2 + f['kappa3'] * T[i] ** 3)) for i in inside)
                    e['trunc_T_at_D'] = abs(f['kappa3']) * D / abs(f['kappa'])
                if 'kappa_cc' in f:
                    e['twoleg_rel'] = relative(f['kappa'], f['kappa_cc']) if max(abs(f['kappa']), abs(f['kappa_cc'])) > KF else None
                if 'kappa3_cc' in f:
                    e['twoleg_kappa3_rel'] = relative(f['kappa3'], f['kappa3_cc']) if fam in mapped else None
                if 'S_cc' in f:
                    e['twoleg_S_abs'] = abs(f['S'] - f['S_cc'])
                fam_out[k][arm][fam] = e
                zero[k][arm + '/' + fam] = {'odf_reading': 'uniform', 'r0': e['r0']}
                if fam in mapped:
                    n1['%s/%s/%s' % (k, arm, fam)] = {'odf_reading': token(k, fam), 'fit': e['S_fit'], 'bi': e['S_bi']}
            lo = sum(min(0.0, rk['arms'][arm][fm]['kappa'] * D * D) for fm in mapped)
            hi = sum(max(0.0, rk['arms'][arm][fm]['kappa'] * D * D) for fm in mapped)
            pts = [rk['arms'][arm][fm]['grid'][i] for fm in mapped for i in inside]
            if arm == 'E2_Hill':
                pts = pts + rk['quadform']['grid5x5_cc']
            hull = [min(lo, min(pts)), max(hi, max(pts))]
            hull = [0.0 if abs(x) < SNAP else x for x in hull]
            reach[k][arm] = {'box': [lo, hi], 'grid_min': min(pts), 'grid_max': max(pts), 'hull': hull,
                             'widened': [x * (1.0 + MU) for x in hull], 'grid_exceeds_box': min(pts) < lo or max(pts) > hi}
        R = grid5(rk['quadform']['grid5x5_cc'])
        n2[k] = {'odf_reading': 'hexP2P4' if k in HEXK else 'cubP2K4-i', 'fit7': rk['quadform']['kappa24_fit7'],
                 'bi_chat': rk['kappa24_bi_chat'], 'bi_cc': rk['kappa24_bi_cc'], 'bi_5x5': rich5(R, '24')}
        if k in CUBK:
            n3[k] = {'odf_reading': 'cubP2-i', 'fit': rk['arms']['E2_Hill']['t2']['kappa'],
                     'bi': even(rk['arms']['E2_Hill']['t2']['grid']), 'pure_l2_change_t1': rk['pure_l2_change_t1']}
            k12 = rk['quadform'].get('basis_k12_chat')
            n4[k] = {'odf_reading': 'cubP2K4-i', 'fit7': rk['quadform']['kappa22_fit7'], 'bi_5x5': rich5(R, '22'),
                     'k12_chat_t2sq': k12[0] if k12 is not None else None}
        else:
            A = rk['arms']
            q22, q44, q24 = rich5(R, '22'), rich5(R, '44'), rich5(R, '24')
            hq[k] = {'k22_bi_5x5': q22, 'k44_bi_5x5': q44, 'k24_bi_5x5': q24,
                     'null_ray_slope': {'E2_Hill_bi5x5': math.sqrt(-q22 / q44),
                                        'E2_Hill_bi': math.sqrt(-even(A['E2_Hill']['t2']['grid']) / even(A['E2_Hill']['t4']['grid'])),
                                        'E2_Hill_fit': math.sqrt(-A['E2_Hill']['t2']['kappa'] / A['E2_Hill']['t4']['kappa']),
                                        'E2_HSmean_bi': math.sqrt(-even(A['E2_HSmean']['t2']['grid']) / even(A['E2_HSmean']['t4']['grid'])),
                                        'E2_HSmean_fit': math.sqrt(-A['E2_HSmean']['t2']['kappa'] / A['E2_HSmean']['t4']['kappa'])},
                     'h_Hill_form': 'negative-definite' if (A['h_Hill']['t2']['kappa'] < 0 and A['h_Hill']['t4']['kappa'] < 0) else 'not negative-definite',
                     'kappa22_fit7_vs_kappa2_rel': relative(rk['quadform']['kappa22_fit7'], A['E2_Hill']['t2']['kappa'])}
    cells = [(k, arm) for k in ALLK for arm in ARMS]
    un = {'hull_all': [min(reach[k][a]['hull'][0] for k, a in cells), max(reach[k][a]['hull'][1] for k, a in cells)],
          'widened_all': [min(reach[k][a]['widened'][0] for k, a in cells), max(reach[k][a]['widened'][1] for k, a in cells)],
          'hull_primary': [min(reach[k]['E2_Hill']['hull'][0] for k in PRIM), max(reach[k]['E2_Hill']['hull'][1] for k in PRIM)],
          'widened_primary': [min(reach[k]['E2_Hill']['widened'][0] for k in PRIM), max(reach[k]['E2_Hill']['widened'][1] for k in PRIM)]}
    f1, f2 = C['synthetic_band_fractions']
    iv = lambda a, b: [a + f1 * (b - a), a + f2 * (b - a)]
    syn = {'margin_positive': iv(un['hull_all'][1], un['widened_all'][1]),
           'margin_negative': iv(un['widened_all'][0], un['hull_all'][0]),
           'robustness_only_positive': iv(un['widened_primary'][1], un['hull_all'][1])}
    # summary
    trip = [(k, arm, fam) for k in ALLK for arm in ARMS for fam in ('t4', 't2')]
    FF = lambda k, arm, fam: fam_out[k][arm][fam]
    b1r = {k: abs(raw['keys'][k]['b1_Hill'] / raw['keys'][k]['arms']['E2_Hill']['t4']['kappa']) for k in ALLK}
    def mx(values):
        values = list(values)
        return max(values)
    ratio_pos = lambda k, a: reach[k][a]['hull'][1] / reach[k][a]['box'][1]
    ratio_neg = lambda k, a: reach[k][a]['hull'][0] / reach[k][a]['box'][0]
    n1_arm = lambda arm: [v for kk, v in n1.items() if kk.split('/')[1] == arm]
    summary = {
        'b1_over_kappa44': b1r,
        'b1_dominance_at_D_min': min(b1r.values()) / D,
        'k_fire_WEM': C['KD_CLIP'] / raw['regime']['d_EM'],
        'trunc_T_at_D_max': mx(FF(k, 'E2_Hill', fam)['trunc_T_at_D'] for k in ALLK for fam in ('t4', 't2') if 'trunc_T_at_D' in FF(k, 'E2_Hill', fam)),
        'recon_max_abs_E2_Hill': {fam: mx(FF(k, 'E2_Hill', fam)['recon_max_abs'] for k in ALLK if 'recon_max_abs' in FF(k, 'E2_Hill', fam)) for fam in ('t4', 't2')},
        'zero_ctrl_max_abs': mx(abs(FF(*t)['r0']) for t in trip),
        'pure_l2_change_t1_max': mx(abs(raw['keys'][k]['pure_l2_change_t1']) for k in CUBK),
        'twoleg_rel_max': mx(FF(*t)['twoleg_rel'] for t in trip if FF(*t).get('twoleg_rel') is not None),
        'twoleg_rel_max_by_arm_family': {'%s/%s' % (arm, fam): mx(FF(k, arm, fam)['twoleg_rel'] for k in ALLK if FF(k, arm, fam).get('twoleg_rel') is not None)
                                         for arm in ARMS for fam in ('t4', 't2') if any(FF(k, arm, fam).get('twoleg_rel') is not None for k in ALLK)},
        'twoleg_kappa3_rel_max': mx(FF(*t)['twoleg_kappa3_rel'] for t in trip if FF(*t).get('twoleg_kappa3_rel') is not None),
        'twoleg_S_abs_max': mx(FF(*t)['twoleg_S_abs'] for t in trip if FF(*t).get('twoleg_S_abs') is not None),
        'b1_twoleg_rel_max': mx(relative(raw['keys'][k]['b1_Hill'], raw['keys'][k]['b1_Hill_cc']) for k in ALLK),
        'quadform_kappa22_twoleg_rel_max': mx(relative(raw['keys'][k]['quadform']['kappa22_fit7'], raw['keys'][k]['quadform']['kappa22_fit7_cc']) for k in HEXK),
        'fit_res_max_by_arm': {arm: mx(FF(k, arm, fam)['fit_res_rel'] for k in ALLK for fam in ('t4', 't2')
                                       if FF(k, arm, fam)['mapped'] and FF(k, arm, fam)['fit_res_rel'] is not None) for arm in ARMS},
        'hs_over_hill_minus_1': {k: {fam: raw['keys'][k]['arms']['E2_HSmean'][fam]['kappa'] / raw['keys'][k]['arms']['E2_Hill'][fam]['kappa'] - 1
                                     for fam in (('t4', 't2') if k in HEXK else ('t4',))} for k in ALLK},
        'grid_excess_over_box_max': {'positive_side': mx(ratio_pos(k, a) for k, a in cells if reach[k][a]['box'][1] > 0),
                                     'negative_side': mx(ratio_neg(k, a) for k, a in cells if reach[k][a]['box'][0] < 0)},
        'grid_excess_over_box_max_by_arm': {arm: mx([ratio_pos(k, arm) for k in ALLK if reach[k][arm]['box'][1] > 0]
                                                    + [ratio_neg(k, arm) for k in ALLK if reach[k][arm]['box'][0] < 0]) for arm in ARMS},
        'null_max_abs': {
            'N-1_bi_by_arm': {arm: mx(abs(v['bi']) for v in n1_arm(arm)) for arm in ARMS},
            'N-1_fit_by_arm': {arm: mx(abs(v['fit']) for v in n1_arm(arm)) for arm in ARMS if all(v['fit'] is not None for v in n1_arm(arm))},
            'N-2_by_estimator_hex': {e: mx(abs(n2[k][e]) for k in HEXK) for e in ('fit7', 'bi_chat', 'bi_cc', 'bi_5x5')},
            'N-2_by_estimator_cubic': {e: mx(abs(n2[k][e]) for k in CUBK) for e in ('fit7', 'bi_chat', 'bi_cc', 'bi_5x5')},
            'N-3_fit': mx(abs(v['fit']) for v in n3.values()), 'N-3_bi': mx(abs(v['bi']) for v in n3.values()),
            'N-4_fit7': mx(abs(v['fit7']) for v in n4.values()), 'N-4_bi_5x5': mx(abs(v['bi_5x5']) for v in n4.values()),
            'N-4_k12_chat': mx(abs(v['k12_chat_t2sq']) for v in n4.values() if v['k12_chat_t2sq'] is not None)},
    }
    return {'families': fam_out, 'reach': reach, 'unions': un, 'synthetic': syn, 'zero_ctrl': zero,
            'nulls': {'N-1': n1, 'N-2': n2, 'N-3': n3, 'N-4': n4}, 'hex_quadform': hq, 'summary': summary}

def rms_exact():
    def dfac(n):
        return 1 if n <= 1 else n * dfac(n - 2)
    def sph(a, b, c):   # <x^a y^b z^c> on the unit sphere, a, b, c even
        return Fraction(dfac(a - 1) * dfac(b - 1) * dfac(c - 1), dfac(a + b + c + 1))
    mu = lambda n: Fraction(1, n + 1) if n % 2 == 0 else Fraction(0)
    p2 = {0: Fraction(-1, 2), 2: Fraction(3, 2)}
    p4 = {0: Fraction(3, 8), 2: Fraction(-15, 4), 4: Fraction(35, 8)}
    sq = lambda p: sum(p[i] * p[j] * mu(i + j) for i in p for j in p)
    s1 = sph(4, 0, 0) + sph(0, 4, 0) + sph(0, 0, 4)
    s2 = sph(8, 0, 0) + sph(0, 8, 0) + sph(0, 0, 8) + 2 * (sph(4, 4, 0) + sph(4, 0, 4) + sph(0, 4, 4))
    k4m = Fraction(5, 2) * (s1 - Fraction(3, 5))
    k4s = Fraction(25, 4) * (s2 - Fraction(6, 5) * s1 + Fraction(9, 25))
    return {'P2_sq': str(sq(p2)), 'P4_sq': str(sq(p4)), 'K4_sq': str(k4s), 'K4_mean': str(k4m)}

def main():
    if len(sys.argv) not in (3, 4):
        print(__doc__); return 2
    repo, path = sys.argv[1], sys.argv[2]
    blob = open(path, 'rb').read()
    print('pinned file: md5 %s  %d B' % (hashlib.md5(blob).hexdigest(), len(blob)))
    F = json.loads(blob.decode('ascii'))
    check(sorted(F) == sorted(['_meta', 'sources', 'provenance', 'structure', 'tokens', 'constants', 'grids', 'raw', 'rms_exact_check', 'derived']), 'top-level blocks')
    # (1) sources
    src = {}
    for alias, (rel_path, md5, n) in SOURCES.items():
        b = open(os.path.join(repo, rel_path), 'rb').read()
        check(hashlib.md5(b).hexdigest() == md5 and len(b) == n, 'source md5/bytes: ' + rel_path)
        src[alias] = json.loads(b.decode('utf-8'))
    check(F['sources'] == {a: {'path': p, 'md5': m, 'bytes': n} for a, (p, m, n) in SOURCES.items()}, 'the sources block')
    # (2) provenance and raw
    EP = expected_provenance()
    check(F['provenance'] == EP, 'the provenance block differs from the expected pointer map')
    n_cmp, covered = 0, set()
    for dest, spec in EP.items():
        if dest.startswith('keys/<K>/'):
            sub = dest[len('keys/<K>/'):]
            ks = ALLK if spec['scope'] == 'all' else CUBK if spec['scope'] == 'cubic' else [k for k in ALLK if k in src['DQF']]
            for k in ks:
                want = get(src[spec['src']], spec['pointer'].replace('{K}', k))
                try:
                    have = get(F['raw']['keys'][k], '/' + sub)
                except (KeyError, IndexError, TypeError):
                    check(False, 'raw value missing: %s %s' % (k, sub)); continue
                check(json.dumps(have) == json.dumps(want), 'raw != source: %s %s' % (k, sub))
                covered.add('keys/%s/%s' % (k, sub)); n_cmp += 1
        else:
            want = get(src[spec['src']], spec['pointer'])
            have = get(F, '/' + dest)
            check(json.dumps(have) == json.dumps(want), 'global != source: ' + dest)
            n_cmp += 1
    expect_cmp = sum(len(ALLK) if s['scope'] == 'all' else len(CUBK) if s['scope'] == 'cubic' else (sum(1 for k in ALLK if k in src['DQF']) if s['scope'] == 'dqf' else 1)
                     for s in EP.values())
    check(n_cmp == expect_cmp, 'comparison count')
    check(sorted(F['raw']) == ['keys', 'regime'] and sorted(F['raw']['regime']) == ['d_EM'] and sorted(F['raw']['keys']) == sorted(ALLK), 'raw block shape')
    raw_leaves = set()
    for k in ALLK:
        check(F['raw']['keys'][k].get('branch') == ('hex' if k in HEXK else 'cubic'), 'branch of ' + k)
        for p in flat({kk: vv for kk, vv in F['raw']['keys'][k].items() if kk != 'branch'}):
            raw_leaves.add('keys/%s/%s' % (k, p.split('[')[0]))
    check(raw_leaves == covered, 'raw leaves without a pointer, or pointers without a raw leaf')
    print('provenance: %d values equal their sources through the pointer map written here (expected %d); %d raw fields, all covered' % (n_cmp, expect_cmp, len(covered)))
    # (3) constants, tokens, structure, grids, meta, rms
    check(F['constants'] == EXPECTED_CONSTANTS, 'constants')
    check(F['tokens'] == EXPECTED_TOKENS, 'tokens')
    check(F['structure'] == EXPECTED_STRUCTURE, 'structure')
    g_fixed = {k: v for k, v in F['grids'].items() if k not in ('t_grid', 't2t4_axis')}
    check(g_fixed == EXPECTED_GRIDS_FIXED and sorted(F['grids']) == sorted(list(EXPECTED_GRIDS_FIXED) + ['t_grid', 't2t4_axis']), 'grids')
    m = F['_meta']
    check(all(m.get(k) == v for k, v in EXPECTED_META.items()), '_meta')
    check(sorted(m) == sorted(list(EXPECTED_META) + ['builder_md5']), '_meta fields')
    check(m.get('builder_md5') == EXPECTED_BUILDER_MD5, 'the embedded builder md5 is not the builder of record')
    check(isinstance(m.get('builder_md5'), str) and len(m['builder_md5']) == 32 and all(c in '0123456789abcdef' for c in m['builder_md5']), 'builder md5 field')
    if len(sys.argv) == 4:
        check(hashlib.md5(open(sys.argv[3], 'rb').read()).hexdigest() == m['builder_md5'], 'the embedded builder md5 differs from the builder file')
    check(F['rms_exact_check'] == rms_exact() == {'P2_sq': '1/5', 'P4_sq': '1/9', 'K4_sq': '4/21', 'K4_mean': '0'}, 'rms exact check')
    # (4) full re-derivation
    mine = flat(rederive(F['raw'], F['constants'], F['grids']))
    theirs = flat(F['derived'])
    check(set(mine) == set(theirs), 'derived leaf sets differ (%d here, %d in the file)' % (len(mine), len(theirs)))
    bad = [p for p in theirs if p in mine and not same(mine[p], theirs[p])]
    for p in bad[:10]:
        check(False, 'derived mismatch: ' + p)
    n_num = sum(1 for v in theirs.values() if isinstance(v, float))
    print('re-derivation: all %d derived leaves compared (%d numeric within %.0e rel + %.0e abs; the rest exact); %d mismatches'
          % (len(theirs), n_num, TOL_REL, TOL_ABS, len(bad)))
    # (5) rule 4
    words = [p for p in flat(F) if any(w in p.split('/')[-1].split('[')[0].lower() for w in ('count', 'n_points', 'npts', 'num_points'))]
    check(not words, 'a count-like field is written')
    T = F['grids']['t_grid']
    print('counts computed here: t grid %d; |t| <= D: %d inclusive / %d strict; |t| <= 0.1: %d / %d; 5x5 %d; area %d' % (
        len(T), sum(abs(t) <= 0.25 for t in T), sum(abs(t) < 0.25 for t in T), sum(abs(t) <= 0.1 for t in T),
        sum(abs(t) < 0.1 for t in T), len(F['grids']['t2t4_axis']) ** 2, F['grids']['area_grid']['nodes_per_axis'] ** 2))
    if fails:
        print('RESULT: FAIL (%d)' % len(fails))
        for f in fails[:20]:
            print('  ' + f)
        return 1
    print('RESULT: PASS')
    return 0

if __name__ == '__main__':
    sys.exit(main())
