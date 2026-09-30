#!/usr/bin/env python3
"""sa_build_pinned_inputs.py -- G-MSCS-A (staging memo v2, sections 3.1 and 9): builds the pinned-inputs file of record,
pinned_inputs_G_MSCS_A.json, from the seven banked sources on `main`, BY NAMED KEY (RFC 6901 JSON pointers, recorded in
the file's `provenance` block), with full-md5 and byte-count guards on every source.

Deterministic by construction: standard library only; every value is either copied from a source (JSON float parse,
exact round trip) or derived with +, -, *, / and sqrt (IEEE-754 correctly rounded); no transcendental function, no
numpy, no clock, no path, no host name in the output; sorted keys; a trailing LF. The same sources give the same bytes
on any platform with IEEE-754 doubles and Python >= 3.6.

No anchor value, no observational number is read or written. The only SI value is the W^EM_U near-component edge (the
ledger's regime scale of record, V4.77), read by key from the G-CI1 CC r2 checkpoint and cross-checked against the
ledger literal.

Usage:  python3 sa_build_pinned_inputs.py REPO_DIR [OUT_FILE]
        REPO_DIR  a clone of gifgaf0/gifgaf0.github.io at a commit whose seven source files carry the md5s below
                  (any commit at or after e1fa071 in which they are unchanged); the repository is only read.
        OUT_FILE  default ./pinned_inputs_G_MSCS_A.json (an existing file is overwritten)
Exit:   0 built and self-verified; 1 a guard failed (no output file is left behind); 2 usage error.

The file has two parts: `raw` (copied values; each field's source and pointer template in `provenance`) and `derived`
(reference values; a pure function of `raw`, `constants` and `grids`). Before exiting, the builder re-reads the written
file, re-derives `derived` from the file alone and requires bit identity, and re-reads every `raw` value from its
source by pointer and requires bit identity. The legs repeat both checks with their own code (F-CTRL-SA-PIN and
F-CTRL-SA-PIN-DERIVED). Point counts are printed from the generators and never written (rule 4)."""
import hashlib, json, math, os, sys
from fractions import Fraction

GATE = 'G-MSCS-A'
FILE_SCHEMA = 'g_mscs_a_pinned_inputs/1'
OUT_DEFAULT = 'pinned_inputs_G_MSCS_A.json'

SOURCES = {  # alias: (repository path, md5 of record, bytes of record)
    'G2chat': ('gmscs2_gate/g_mscs2_chatleg_checkpoint.json', '1c5b6b59829d2a6b9ae2b1a7a016832d', 31575),
    'G2cc':   ('gmscs2_gate/g_mscs2_ccleg_checkpoint.json',   '9961745d1e1857cfab6445d4754b5060', 68540),
    'G1chat': ('gmscs1_gate/g_mscs1_chatleg_checkpoint.json', 'c04c0b8ea34cfe60f231aa06828e6ce4', 33289),
    'G1cc':   ('gmscs1_gate/g_mscs1_ccleg_checkpoint.json',   '249e11dd53c4cb82f302b15d3c94c337', 24415),
    'DK24':   ('gmscs2_gate/diag_kappa24.json',               'b7952dfcaddcd1d98e424aee8ce5231f', 1917),
    'DQF':    ('gmscs2_gate/diag_quadform_basis.json',        'd84aa1fdce7dea1b1a5d24dfb8f13c18', 1119),
    'CI1':    ('gci1_gate/ci1_phase3_cc_r2.json',             '845ae6beb1b90fe34c540f843ffdb9f5', 45760),
}
KEYS = ['hex_step|a', 'hex_step|b', 'hex_gem8|a', 'hex_gem8|b',
        'cubic_step|001', 'cubic_step|111', 'cubic_gem8|001', 'cubic_gem8|111']
HEX = KEYS[:4]
CUBIC = KEYS[4:]
ARMS = ['E2_Hill', 'E2_HSmean', 'h_Hill']
PRIMARY = {'arm': 'E2_Hill', 'keys': ['hex_step|a', 'hex_gem8|a', 'cubic_step|001', 'cubic_gem8|001']}
LEDGER_WEM_EDGE = 3.7641664288e-33   # the V4.77 ledger literal; a cross-check only -- the pinned value is read by key

# raw fields: (destination path under keys/<K>/, source alias, JSON pointer template, scope)
# scope: 'all' = every key; 'cubic' = cubic keys only; 'dqf' = the keys the chat quadform-basis diagnostic banks
FIELDS = [
    ('arms/E2_Hill/t4/kappa',      'G2chat', '/phase2/{K}/kappa44_E2', 'all'),
    ('arms/E2_Hill/t4/kappa_cc',   'G2cc',   '/phase2/{K}/kappa44_E2', 'all'),
    ('arms/E2_Hill/t4/S',          'G2chat', '/phase2/{K}/S4_E2', 'all'),
    ('arms/E2_Hill/t4/kappa3',     'G2chat', '/phase2/{K}/kappa444_E2', 'all'),
    ('arms/E2_Hill/t4/grid',       'G2chat', '/phase2/{K}/r_agg_E2_VRH', 'all'),
    ('arms/E2_HSmean/t4/kappa',    'G2chat', '/phase2/{K}/kappa44_E2_HS', 'all'),
    ('arms/E2_HSmean/t4/kappa_cc', 'G2cc',   '/phase2/{K}/kappa44_E2_HS', 'all'),
    ('arms/E2_HSmean/t4/grid',     'G2chat', '/phase2/{K}/r_agg_E2_HS', 'all'),
    ('arms/h_Hill/t4/kappa',       'G2chat', '/phase2/{K}/kappa44_h', 'all'),
    ('arms/h_Hill/t4/kappa_cc',    'G2cc',   '/phase2/{K}/kappa44_h', 'all'),
    ('arms/h_Hill/t4/S',           'G2chat', '/phase2/{K}/S4_h', 'all'),
    ('arms/h_Hill/t4/grid',        'G2chat', '/phase2/{K}/r_agg_h_VRH', 'all'),
    # the l = 2 family (G-MSCS1): mapped on hex keys; the null family on cubic keys (null N-3)
    ('arms/E2_Hill/t2/kappa',      'G1chat', '/phase2/{K}/kappa2_E2', 'all'),
    ('arms/E2_Hill/t2/kappa_cc',   'G1cc',   '/phase2/{K}/kappa2_E2', 'all'),
    ('arms/E2_Hill/t2/S',          'G1chat', '/phase2/{K}/S_t_E2', 'all'),
    ('arms/E2_Hill/t2/kappa3',     'G1chat', '/phase2/{K}/kappa3_E2', 'all'),
    ('arms/E2_Hill/t2/grid',       'G1chat', '/phase2/{K}/r_agg_E2_VRH', 'all'),
    ('arms/E2_HSmean/t2/kappa',    'G1chat', '/phase2/{K}/kappa2_E2_HS', 'all'),
    ('arms/E2_HSmean/t2/grid',     'G1chat', '/phase2/{K}/r_agg_E2_HS', 'all'),
    ('arms/h_Hill/t2/kappa',       'G1chat', '/phase2/{K}/kappa2_h', 'all'),
    ('arms/h_Hill/t2/kappa_cc',    'G1cc',   '/phase2/{K}/kappa2_h', 'all'),
    ('arms/h_Hill/t2/S',           'G1chat', '/phase2/{K}/S_t_h', 'all'),
    ('arms/h_Hill/t2/grid',        'G1chat', '/phase2/{K}/r_agg_h_VRH', 'all'),
    # the CC counterparts of every other coefficient the mapper uses (F-CTRL-SA-PIN covers each; v2 audit 13(c))
    ('arms/E2_Hill/t4/S_cc',       'G2cc',   '/phase2/{K}/S4_E2', 'all'),
    ('arms/E2_Hill/t4/kappa3_cc',  'G2cc',   '/phase2/{K}/kappa444_E2', 'all'),
    ('arms/h_Hill/t4/S_cc',        'G2cc',   '/phase2/{K}/S4_h', 'all'),
    ('arms/E2_Hill/t2/S_cc',       'G1cc',   '/phase2/{K}/S_t_E2', 'all'),
    ('arms/E2_Hill/t2/kappa3_cc',  'G1cc',   '/phase2/{K}/kappa3_E2', 'all'),
    ('arms/h_Hill/t2/S_cc',        'G1cc',   '/phase2/{K}/S_t_h', 'all'),
    # the (t2, t4) quadratic form, S2-E2 Hill arm (reading (i) on cubic keys: A-3.3)
    ('quadform/kappa22_fit7',      'G2chat', '/phase2/{K}/quadform/kappa22', 'all'),
    ('quadform/kappa22_fit7_cc',   'G2cc',   '/phase2/{K}/quadform/kappa22', 'all'),
    ('quadform/kappa24_fit7',      'G2chat', '/phase2/{K}/quadform/kappa24', 'all'),
    ('quadform/kappa44_fit7',      'G2chat', '/phase2/{K}/quadform/kappa44', 'all'),
    ('quadform/grid5x5_cc',        'G2cc',   '/phase2/{K}/quadform/x_grid_r_agg_E2_VRH', 'all'),
    ('quadform/cubic_terms_cc',    'G2cc',   '/phase2/{K}/quadform/x_cubic_terms_discarded', 'all'),
    ('quadform/reading_cc',        'G2cc',   '/phase2/{K}/quadform/x_reading', 'all'),
    ('quadform/basis_k7_chat',     'DQF',    '/{K}/k7', 'dqf'),
    ('quadform/basis_k12_chat',    'DQF',    '/{K}/k12', 'dqf'),
    ('kappa24_bi_chat',            'DK24',   '/{K}/kappa24_richardson', 'all'),
    ('kappa24_bi_cc',              'G2cc',   '/phase2/{K}/kappa24_richardson', 'all'),
    ('b1_Hill',                    'G2chat', '/phase2/{K}/biref_b1_VRH', 'all'),
    ('b1_Hill_cc',                 'G2cc',   '/phase2/{K}/biref_b1_VRH', 'all'),
    ('pure_l2_change_t1',          'DK24',   '/{K}/pure_l2_r_agg_change_t1', 'cubic'),
    ('A31_mixed_change_cc',        'G2cc',   '/extras/A3_diagnostics/A-3.1_mixed_r_agg_change_A29/{K}', 'cubic'),
]
GLOBAL_FIELDS = [  # (destination, alias, pointer)
    ('grids/t_grid',     'G2chat', '/t4_grid'),
    ('grids/t2t4_axis',  'G2chat', '/t2t4_grid'),
    ('regime/d_EM',      'CI1',    '/per_oom/x1/W_EM_union/0/1'),
]
CUBIC_TERM_ORDER = ['t2^3', 't2^2*t4', 't2*t4^2', 't4^3']            # the CC checkpoint's discarded-term order (A-2.9)
DQF_BASIS = ['t2^2', 't2*t4', 't4^2', 't2^3', 't2^2*t4', 't2*t4^2', 't4^3', 't2^4', 't2^3*t4', 't2^2*t4^2', 't2*t4^3', 't4^4']

CONSTANTS = {
    'D': 0.25,                        # E-SA-10(a): the fit window |t| <= 0.25 per family (D-12)
    'mu': 0.10,                       # E-SA-11(a): reach widening (D-22)
    'KD_CLIP': 0.3,                   # E-SA-4(a): long-wavelength envelope (D-21)
    'tau_agg': 1e-6,                  # rule 2: first-order slope tolerance (D-14)
    'kappa_floor': 1e-6,              # rule 2: coefficient-null tolerance (D-14)
    'zero_snap': 1e-12,               # S-SA-9: hull endpoints within this of zero are set to 0
    'trunc_threshold': 0.10,          # TRUNCATION-SENSITIVE (D-22)
    'nullfloor_threshold': 0.10,      # NULL-FLOOR-SENSITIVE (section 3.3)
    'recon_tol_abs_E2_Hill': 1e-8,    # F-CTRL-SA-RECON, S2-E2 Hill arm
    'recon_tol_rel_robust': 1e-3,     # F-CTRL-SA-RECON, robustness arms (kappa of record vs basis-independent)
    'pin_twoleg_tol_rel': 1e-4,       # F-CTRL-SA-PIN, chat vs CC banked coefficients
    'zero_ctrl_tol_abs': 1e-12,       # F-CTRL-SA-ZERO
    'l2null_t1_tol_abs': 1e-12,       # F-CTRL-SA-L2NULL (r_agg unchanged by t2 alone at t2 = 1)
    'edge_twoleg_tol_rel': 1e-10,     # section 6.4
    'mono_tol_rel': 1e-14,            # F-CTRL-SA-MONO
    'pin_derived_tol_rel': 1e-12,     # F-CTRL-SA-PIN-DERIVED: |leg - pinned| <= tol_rel*|pinned| + tol_abs
    'pin_derived_tol_abs': 1e-16,
    'oom_factors': [0.1, 1.0, 10.0],  # section 3.8
    'synthetic_t': [0.01, 0.1, 0.5],  # Phase 2 synthetic budgets b = |kappa| * t_syn^2 (C-SYN-1..5, 7..11, 14)
    'synthetic_t_tight': 1e-9,        # C-SYN-12: a budget tight enough that the NULL-FLOOR flag is exercised
    'synthetic_band_fractions': [0.25, 0.75],   # C-SYN-3 (robustness-only) and C-SYN-13 (MARGIN) interval rule
    'synthetic_k': {'silent': 1.0, 'void': 1e33},   # m^-1: every suite uses 'silent' for k_em_max and k_t_max; C-SYN-10 uses 'void'
    'synthetic_rules': {
        'margin_positive': '[h + f1*(w - h), h + f2*(w - h)], h = unions.hull_all[1], w = unions.widened_all[1]',
        'margin_negative': '[w + f1*(h - w), w + f2*(h - w)], w = unions.widened_all[0], h = unions.hull_all[0]',
        'robustness_only_positive': '[p + f1*(q - p), p + f2*(q - p)], p = unions.widened_primary[1], q = unions.hull_all[1]'},
    'rms': {'hexP2': math.sqrt(1 / 5), 'hexP4': 1 / 3, 'cubK4': math.sqrt(4 / 21)},
    'rms_closed_form': {'hexP2': 'sqrt(1/5)', 'hexP4': '1/3', 'cubK4': 'sqrt(4/21)'},
    'fam_rms': {'t2': 'hexP2', 't4_hex': 'hexP4', 't4_cubic': 'cubK4'},
}
GRIDS_FIXED = {
    'fit_window': 'abs(t) <= D, inclusive (the window both banked legs used; H-CC-1)',
    'richardson_pairs': {'one_param': [0.05, 0.1], 'two_param': [0.125, 0.25]},
    'richardson_formulas': {
        'odd':   '[4*O(h1) - O(h2)]/3, O(h) = [r(h) - r(-h)]/(2h)',
        'even':  '[4*E(h1) - E(h2)]/3, E(h) = [r(h) + r(-h) - 2*r(0)]/(2h^2)',
        'mixed': '[4*M(h1) - M(h2)]/3, M(h) = [R(h,h) - R(h,-h) - R(-h,h) + R(-h,-h)]/(4h^2)'},
    'grid5x5_layout': 'row-major, t2 outer, t4 inner: index = 5*i + j for (t2_axis[i], t4_axis[j])',
    'area_grid': {'lo': -0.25, 'hi': 0.25, 'nodes_per_axis': 201, 'node': 'lo + i*(hi - lo)/(nodes_per_axis - 1)'},
}
TOKENS = {
    'odf_reading': ['none', 'uniform', 'hexP2', 'hexP4', 'hexP2P4', 'cubK4', 'cubP2-i', 'cubP2-ii', 'cubP2K4-i', 'cubP2K4-ii'],
    'delta_def': 'tensor_over_EM_minus_1',
    'class': ['spd'],
    'reading_conformant': ['bound'],
    'reading_frozen_list': ['bound', 'ceiling', 'margin', 'criterion'],
    'geom': ['single', 'population'],
    'q': ['phase', 'group'],
}
STRUCTURE = {
    'keys': KEYS, 'hex_keys': HEX, 'cubic_keys': CUBIC, 'arms': ARMS, 'primary': PRIMARY,
    'robustness': {'arms': ['E2_HSmean', 'h_Hill'], 'keys': ['hex_step|b', 'hex_gem8|b', 'cubic_step|111', 'cubic_gem8|111']},
    'mapped_families': {'hex': ['t4', 't2'], 'cubic': ['t4']},
    'null_families': {'cubic': ['t2']},
    'kill_test_set': 'every key x every arm (E-SA-9(a)); the primary-only union is serialized for information',
}
ELECTIONS = {'E-SA-0': 'a', 'E-SA-1': 'a', 'E-SA-2': 'a', 'E-SA-3': 'a', 'E-SA-4': 'a', 'E-SA-5': 'a',
             'E-SA-6': 'a', 'E-SA-7': 'base 05302210 + the G-MSCS1 stratum', 'E-SA-8': 'a', 'E-SA-9': 'a',
             'E-SA-10': 'a', 'E-SA-11': 'a'}


class GuardError(Exception):
    pass


def guard(cond, msg):
    if not cond:
        raise GuardError(msg)


def ptr_get(doc, pointer):
    """RFC 6901 dereference (the '~1' and '~0' escapes honoured)."""
    guard(pointer.startswith('/'), 'bad pointer ' + pointer)
    cur = doc
    for tok in pointer[1:].split('/'):
        tok = tok.replace('~1', '/').replace('~0', '~')
        if isinstance(cur, list):
            guard(tok.isdigit() and int(tok) < len(cur), 'pointer index out of range: ' + pointer)
            cur = cur[int(tok)]
        else:
            guard(isinstance(cur, dict) and tok in cur, 'pointer key missing: ' + pointer)
            cur = cur[tok]
    return cur


def is_float_leaf(v):
    if isinstance(v, bool):
        return False
    if isinstance(v, float):
        return math.isfinite(v)
    if isinstance(v, list):
        return len(v) > 0 and all(is_float_leaf(x) for x in v)
    return False


def set_path(d, path, value):
    parts = path.split('/')
    for p in parts[:-1]:
        d = d.setdefault(p, {})
    guard(parts[-1] not in d, 'duplicate destination ' + path)
    d[parts[-1]] = value


def load_sources(repo):
    docs, meta = {}, {}
    for alias, (path, md5, nbytes) in SOURCES.items():
        full = os.path.join(repo, path)
        guard(os.path.isfile(full), 'source missing: ' + path)
        b = open(full, 'rb').read()
        h = hashlib.md5(b).hexdigest()
        guard(h == md5 and len(b) == nbytes, 'source md5/bytes mismatch: %s (got %s, %d B)' % (path, h, len(b)))
        docs[alias] = json.loads(b.decode('utf-8'))
        meta[alias] = {'path': path, 'md5': md5, 'bytes': nbytes}
    return docs, meta


def scope_keys(scope, docs):
    if scope == 'all':
        return KEYS
    if scope == 'cubic':
        return CUBIC
    if scope == 'dqf':
        return [k for k in KEYS if k in docs['DQF']]
    raise GuardError('unknown scope ' + scope)


def build_raw(docs):
    guard(list(docs['G2chat']['phase2'].keys()) == KEYS, 'G-MSCS2 chat key set/order differs from the pinned key list')
    for alias in ('G2cc', 'G1chat', 'G1cc', 'DK24'):
        src = docs[alias]['phase2'] if 'phase2' in docs[alias] else docs[alias]
        guard(sorted(src.keys()) == sorted(KEYS), 'key set differs in ' + alias)
    raw = {'keys': {}}
    for k in KEYS:
        raw['keys'][k] = {'branch': 'hex' if k in HEX else 'cubic'}
    for dest, alias, ptmpl, scope in FIELDS:
        for k in scope_keys(scope, docs):
            v = ptr_get(docs[alias], ptmpl.format(K=k))
            if dest == 'quadform/reading_cc':
                guard(isinstance(v, str), 'reading is not a string')
            else:
                guard(is_float_leaf(v), 'non-float or non-finite value at %s:%s' % (alias, ptmpl.format(K=k)))
            set_path(raw['keys'][k], dest, v)
    glob = {}
    for dest, alias, p in GLOBAL_FIELDS:
        v = ptr_get(docs[alias], p)
        guard(is_float_leaf(v), 'non-float global at ' + p)
        set_path(glob, dest, v)
    # structural assertions on the global values
    guard(ptr_get(docs['G1chat'], '/t_grid') == glob['grids']['t_grid'], 'the G-MSCS1 t grid differs from the G-MSCS2 t4 grid')
    wem = ptr_get(docs['CI1'], '/per_oom/x1/W_EM_union')
    guard(len(wem) == 1 and wem[0][0] == 0.0, 'W^EM_U near component is not a single floor-adjoining interval')
    guard(glob['regime']['d_EM'] == LEDGER_WEM_EDGE, 'W^EM_U edge differs from the V4.77 ledger literal')
    for arr in (glob['grids']['t_grid'],):
        for h in GRIDS_FIXED['richardson_pairs']['one_param'] + [0.0]:
            guard(h in arr and -h in arr, 'one-parameter Richardson step missing from the t grid')
    for h in GRIDS_FIXED['richardson_pairs']['two_param'] + [0.0]:
        guard(h in glob['grids']['t2t4_axis'] and -h in glob['grids']['t2t4_axis'], 'two-parameter step missing')
    for k in KEYS:
        q = raw['keys'][k]['quadform']
        guard(len(q['grid5x5_cc']) == len(glob['grids']['t2t4_axis']) ** 2, '5x5 grid length')
        guard(len(q['cubic_terms_cc']) == len(CUBIC_TERM_ORDER), 'cubic-term list length')
        for arm in ARMS:
            for fam in ('t4', 't2'):
                guard(len(raw['keys'][k]['arms'][arm][fam]['grid']) == len(glob['grids']['t_grid']), 'grid length')
    for k in raw['keys']:
        q = raw['keys'][k]['quadform']
        if 'basis_k12_chat' in q:
            guard(len(q['basis_k12_chat']) == len(DQF_BASIS) and len(q['basis_k7_chat']) == 7, 'k7/k12 length')
            guard([q['basis_k7_chat'][i] for i in range(3)] == [q['kappa22_fit7'], q['kappa24_fit7'], q['kappa44_fit7']],
                  'the diagnostic k7[0..2] do not reproduce the fit7 kappa22, kappa24, kappa44 (basis order unconfirmed)')
            for i, c in zip(range(3, 7), q['cubic_terms_cc']):
                a = q['basis_k7_chat'][i]
                guard(abs(a - c) <= 1e-4 * max(abs(a), abs(c)) + 1e-12,
                      'the diagnostic k7[3..6] do not match the CC named cubic terms (basis order unconfirmed)')
                b = q['basis_k12_chat'][i]
                guard(abs(a - b) <= 1e-8 * max(abs(a), abs(b)) + 1e-15,
                      'the diagnostic k12[3..6] do not match k7[3..6] (shared order unconfirmed)')
    return raw, glob


# ---------------------------------------------------------------- derived: a pure function of (raw, constants, grids)
def derive(raw, constants, grids):
    D, MU, SNAP = constants['D'], constants['mu'], constants['zero_snap']
    tg, ax = grids['t_grid'], grids['t2t4_axis']
    h1, h2 = grids['richardson_pairs']['one_param']
    g1, g2 = grids['richardson_pairs']['two_param']
    ind = [i for i, t in enumerate(tg) if abs(t) <= D]

    def at(arr, t):
        return arr[tg.index(t)]

    def rich_odd(arr):
        O = lambda h: (at(arr, h) - at(arr, -h)) / (2 * h)
        return (4 * O(h1) - O(h2)) / 3

    def rich_even(arr):
        E = lambda h: (at(arr, h) + at(arr, -h) - 2 * at(arr, 0.0)) / (2 * h * h)
        return (4 * E(h1) - E(h2)) / 3

    def grid5(arr):
        n = len(ax)
        return {(ax[i], ax[j]): arr[n * i + j] for i in range(n) for j in range(n)}

    def e22(R, h):
        return (R[(h, 0.0)] + R[(-h, 0.0)] - 2 * R[(0.0, 0.0)]) / (2 * h * h)

    def e44(R, h):
        return (R[(0.0, h)] + R[(0.0, -h)] - 2 * R[(0.0, 0.0)]) / (2 * h * h)

    def m24(R, h):
        return (R[(h, h)] - R[(h, -h)] - R[(-h, h)] + R[(-h, -h)]) / (4 * h * h)

    def rich2(f, R):
        return (4 * f(R, g1) - f(R, g2)) / 3

    def rel(a, b):
        return abs(a - b) / max(abs(a), abs(b))

    def snap(x):
        return 0.0 if abs(x) < SNAP else x

    def tok(k, fam):
        if fam == 't2':
            return 'hexP2' if k in HEX else 'cubP2-i'
        return 'hexP4' if k in HEX else 'cubK4'

    out = {'families': {}, 'reach': {}, 'unions': {}, 'nulls': {'N-1': {}, 'N-2': {}, 'N-3': {}, 'N-4': {}},
           'hex_quadform': {}, 'zero_ctrl': {}, 'summary': {}}
    for k in KEYS:
        rk = raw['keys'][k]
        out['families'][k], out['reach'][k], out['zero_ctrl'][k] = {}, {}, {}
        mapped = ['t4', 't2'] if k in HEX else ['t4']
        for arm in ARMS:
            out['families'][k][arm] = {}
            for fam in ('t4', 't2'):
                f = rk['arms'][arm][fam]
                kb = rich_even(f['grid'])
                e = {'odf_reading': tok(k, fam), 'kappa': f['kappa'], 'kappa_bi': kb,
                     'fit_res_rel': (abs(f['kappa'] - kb) / abs(kb)) if abs(kb) > constants['kappa_floor'] else None,
                     'S_bi': rich_odd(f['grid']), 'S_fit': f.get('S'), 'r0': at(f['grid'], 0.0),
                     'mapped': fam in mapped}
                if 'kappa3' in f and fam in mapped:
                    e['recon_max_abs'] = max(abs(f['grid'][i] - (f['S'] * tg[i] + f['kappa'] * tg[i] * tg[i]
                                                                  + f['kappa3'] * tg[i] * tg[i] * tg[i])) for i in ind)
                    e['trunc_T_at_D'] = abs(f['kappa3']) * D / abs(f['kappa'])
                if 'kappa_cc' in f:
                    e['twoleg_rel'] = rel(f['kappa'], f['kappa_cc']) if (abs(f['kappa']) > constants['kappa_floor'] or abs(f['kappa_cc']) > constants['kappa_floor']) else None
                if 'kappa3_cc' in f:
                    e['twoleg_kappa3_rel'] = rel(f['kappa3'], f['kappa3_cc']) if fam in mapped else None
                if 'S_cc' in f:
                    e['twoleg_S_abs'] = abs(f['S'] - f['S_cc'])
                out['families'][k][arm][fam] = e
                out['zero_ctrl'][k]['%s/%s' % (arm, fam)] = {'odf_reading': 'uniform', 'r0': e['r0']}
                if fam in mapped:
                    out['nulls']['N-1']['%s/%s/%s' % (k, arm, fam)] = {'odf_reading': tok(k, fam), 'fit': f.get('S'),
                                                                       'bi': e['S_bi']}
            # reach: hull of the second-order box and every banked grid value inside D, then widened by (1 + mu)
            ks = [rk['arms'][arm][fam]['kappa'] for fam in mapped]
            box_lo, box_hi = 0.0, 0.0
            for x in ks:
                box_lo += min(0.0, x * D * D)
                box_hi += max(0.0, x * D * D)
            vals = [rk['arms'][arm][fam]['grid'][i] for fam in mapped for i in ind]
            if arm == 'E2_Hill':
                vals = vals + list(rk['quadform']['grid5x5_cc'])
            hull = [snap(min(box_lo, min(vals))), snap(max(box_hi, max(vals)))]
            out['reach'][k][arm] = {'box': [box_lo, box_hi], 'grid_min': min(vals), 'grid_max': max(vals), 'hull': hull,
                                    'widened': [hull[0] * (1 + MU), hull[1] * (1 + MU)],
                                    'grid_exceeds_box': (min(vals) < box_lo) or (max(vals) > box_hi)}
        # nulls N-2 (kappa24, every key), N-3 and N-4 (cubic)
        R = grid5(rk['quadform']['grid5x5_cc'])
        out['nulls']['N-2'][k] = {'odf_reading': 'hexP2P4' if k in HEX else 'cubP2K4-i',
                                  'fit7': rk['quadform']['kappa24_fit7'], 'bi_chat': rk['kappa24_bi_chat'],
                                  'bi_cc': rk['kappa24_bi_cc'], 'bi_5x5': rich2(m24, R)}
        if k in CUBIC:
            f2 = rk['arms']['E2_Hill']['t2']
            out['nulls']['N-3'][k] = {'odf_reading': 'cubP2-i', 'fit': f2['kappa'], 'bi': rich_even(f2['grid']),
                                      'pure_l2_change_t1': rk['pure_l2_change_t1']}
            q = rk['quadform']
            out['nulls']['N-4'][k] = {'odf_reading': 'cubP2K4-i', 'fit7': q['kappa22_fit7'], 'bi_5x5': rich2(e22, R),
                                      'k12_chat_t2sq': q['basis_k12_chat'][0] if 'basis_k12_chat' in q else None}
        else:
            a = rk['arms']
            hq = {'k22_bi_5x5': rich2(e22, R), 'k44_bi_5x5': rich2(e44, R), 'k24_bi_5x5': rich2(m24, R)}
            hq['null_ray_slope'] = {
                'E2_Hill_bi5x5': math.sqrt(-hq['k22_bi_5x5'] / hq['k44_bi_5x5']),
                'E2_Hill_bi': math.sqrt(-rich_even(a['E2_Hill']['t2']['grid']) / rich_even(a['E2_Hill']['t4']['grid'])),
                'E2_Hill_fit': math.sqrt(-a['E2_Hill']['t2']['kappa'] / a['E2_Hill']['t4']['kappa']),
                'E2_HSmean_bi': math.sqrt(-rich_even(a['E2_HSmean']['t2']['grid']) / rich_even(a['E2_HSmean']['t4']['grid'])),
                'E2_HSmean_fit': math.sqrt(-a['E2_HSmean']['t2']['kappa'] / a['E2_HSmean']['t4']['kappa'])}
            hq['h_Hill_form'] = ('negative-definite' if (a['h_Hill']['t2']['kappa'] < 0 and a['h_Hill']['t4']['kappa'] < 0)
                                 else 'not negative-definite')
            hq['kappa22_fit7_vs_kappa2_rel'] = rel(rk['quadform']['kappa22_fit7'], a['E2_Hill']['t2']['kappa'])
            out['hex_quadform'][k] = hq
    # unions
    def union(sel, which):
        items = [out['reach'][k][arm][which] for k in KEYS for arm in ARMS if sel(k, arm)]
        return [min(x[0] for x in items), max(x[1] for x in items)]
    prim = lambda k, arm: arm == PRIMARY['arm'] and k in PRIMARY['keys']
    every = lambda k, arm: True
    out['unions'] = {'widened_all': union(every, 'widened'), 'widened_primary': union(prim, 'widened'),
                     'hull_all': union(every, 'hull'), 'hull_primary': union(prim, 'hull')}
    f1, f2 = constants['synthetic_band_fractions']
    u = out['unions']
    def band(lo_end, hi_end):
        return [lo_end + f1 * (hi_end - lo_end), lo_end + f2 * (hi_end - lo_end)]
    out['synthetic'] = {'margin_positive': band(u['hull_all'][1], u['widened_all'][1]),
                        'margin_negative': band(u['widened_all'][0], u['hull_all'][0]),
                        'robustness_only_positive': band(u['widened_primary'][1], u['hull_all'][1])}
    # summary constants quoted by the memo (nothing hand-computed)
    b1r = {k: abs(raw['keys'][k]['b1_Hill'] / raw['keys'][k]['arms']['E2_Hill']['t4']['kappa']) for k in KEYS}
    fams = [(k, arm, fam) for k in KEYS for arm in ARMS for fam in ('t4', 't2')]
    s = out['summary']
    s['b1_over_kappa44'] = b1r
    s['b1_dominance_at_D_min'] = min(b1r.values()) / D
    s['k_fire_WEM'] = constants['KD_CLIP'] / raw['regime']['d_EM']
    s['trunc_T_at_D_max'] = max(out['families'][k]['E2_Hill'][f]['trunc_T_at_D'] for k in KEYS for f in ('t4', 't2')
                                if 'trunc_T_at_D' in out['families'][k]['E2_Hill'][f])
    s['recon_max_abs_E2_Hill'] = {f: max(out['families'][k]['E2_Hill'][f]['recon_max_abs'] for k in KEYS
                                         if 'recon_max_abs' in out['families'][k]['E2_Hill'][f]) for f in ('t4', 't2')}
    s['zero_ctrl_max_abs'] = max(abs(out['families'][k][arm][fam]['r0']) for k, arm, fam in fams)
    s['pure_l2_change_t1_max'] = max(abs(raw['keys'][k]['pure_l2_change_t1']) for k in CUBIC)
    s['twoleg_rel_max'] = max(out['families'][k][arm][fam]['twoleg_rel'] for k, arm, fam in fams
                              if out['families'][k][arm][fam].get('twoleg_rel') is not None)
    s['twoleg_rel_max_by_arm_family'] = {'%s/%s' % (arm, fam): max(out['families'][k][arm][fam]['twoleg_rel'] for k in KEYS
                                                                    if out['families'][k][arm][fam].get('twoleg_rel') is not None)
                                         for arm in ARMS for fam in ('t4', 't2')
                                         if any(out['families'][k][arm][fam].get('twoleg_rel') is not None for k in KEYS)}
    s['twoleg_kappa3_rel_max'] = max(out['families'][k][arm][fam]['twoleg_kappa3_rel'] for k, arm, fam in fams
                                     if out['families'][k][arm][fam].get('twoleg_kappa3_rel') is not None)
    s['twoleg_S_abs_max'] = max(out['families'][k][arm][fam]['twoleg_S_abs'] for k, arm, fam in fams
                                if out['families'][k][arm][fam].get('twoleg_S_abs') is not None)
    s['b1_twoleg_rel_max'] = max(rel(raw['keys'][k]['b1_Hill'], raw['keys'][k]['b1_Hill_cc']) for k in KEYS)
    s['quadform_kappa22_twoleg_rel_max'] = max(rel(raw['keys'][k]['quadform']['kappa22_fit7'], raw['keys'][k]['quadform']['kappa22_fit7_cc']) for k in HEX)
    s['fit_res_max_by_arm'] = {arm: max(out['families'][k][arm][fam]['fit_res_rel'] for k in KEYS for fam in ('t4', 't2')
                                        if out['families'][k][arm][fam]['mapped'] and out['families'][k][arm][fam]['fit_res_rel'] is not None)
                               for arm in ARMS}
    s['hs_over_hill_minus_1'] = {k: {f: raw['keys'][k]['arms']['E2_HSmean'][f]['kappa'] / raw['keys'][k]['arms']['E2_Hill'][f]['kappa'] - 1
                                     for f in (['t4', 't2'] if k in HEX else ['t4'])} for k in KEYS}
    pos = [out['reach'][k][arm]['hull'][1] / out['reach'][k][arm]['box'][1] for k in KEYS for arm in ARMS if out['reach'][k][arm]['box'][1] > 0]
    neg = [out['reach'][k][arm]['hull'][0] / out['reach'][k][arm]['box'][0] for k in KEYS for arm in ARMS if out['reach'][k][arm]['box'][0] < 0]
    s['grid_excess_over_box_max'] = {'positive_side': max(pos), 'negative_side': max(neg)}
    s['grid_excess_over_box_max_by_arm'] = {arm: max([out['reach'][k][arm]['hull'][1] / out['reach'][k][arm]['box'][1] for k in KEYS if out['reach'][k][arm]['box'][1] > 0]
                                                     + [out['reach'][k][arm]['hull'][0] / out['reach'][k][arm]['box'][0] for k in KEYS if out['reach'][k][arm]['box'][0] < 0])
                                            for arm in ARMS}
    n2 = out['nulls']['N-2']
    s['null_max_abs'] = {
        'N-1_bi_by_arm': {arm: max(abs(v['bi']) for kk, v in out['nulls']['N-1'].items() if kk.split('/')[1] == arm) for arm in ARMS},
        'N-1_fit_by_arm': {arm: max(abs(v['fit']) for kk, v in out['nulls']['N-1'].items() if kk.split('/')[1] == arm)
                           for arm in ARMS if all(v['fit'] is not None for kk, v in out['nulls']['N-1'].items() if kk.split('/')[1] == arm)},
        'N-2_by_estimator_hex': {e: max(abs(n2[k][e]) for k in HEX) for e in ('fit7', 'bi_chat', 'bi_cc', 'bi_5x5')},
        'N-2_by_estimator_cubic': {e: max(abs(n2[k][e]) for k in CUBIC) for e in ('fit7', 'bi_chat', 'bi_cc', 'bi_5x5')},
        'N-3_fit': max(abs(v['fit']) for v in out['nulls']['N-3'].values()),
        'N-3_bi': max(abs(v['bi']) for v in out['nulls']['N-3'].values()),
        'N-4_fit7': max(abs(v['fit7']) for v in out['nulls']['N-4'].values()),
        'N-4_bi_5x5': max(abs(v['bi_5x5']) for v in out['nulls']['N-4'].values()),
        'N-4_k12_chat': max(abs(v['k12_chat_t2sq']) for v in out['nulls']['N-4'].values() if v['k12_chat_t2sq'] is not None)}
    return out


def preflight(dv, constants):
    """The Phase-0 criteria that depend on pinned values only, evaluated at build time (the legs repeat them at Phase 0
    with their own code). A failure means the banked record itself cannot pass a control: nothing is written."""
    s, n = dv['summary'], dv['nulls']
    tau, kf = constants['tau_agg'], constants['kappa_floor']
    robust_res = max(dv['families'][k][arm][f]['fit_res_rel'] for k in KEYS for arm in ('E2_HSmean', 'h_Hill') for f in ('t4', 't2')
                     if dv['families'][k][arm][f]['mapped'])
    checks = [
        ('F-CTRL-SA-PIN two-leg kappa (rel)', s['twoleg_rel_max'], constants['pin_twoleg_tol_rel']),
        ('F-CTRL-SA-PIN two-leg quadform kappa22 (rel)', s['quadform_kappa22_twoleg_rel_max'], constants['pin_twoleg_tol_rel']),
        ('F-CTRL-SA-PIN two-leg cubic coefficient kappa3 (rel)', s['twoleg_kappa3_rel_max'], constants['pin_twoleg_tol_rel']),
        ('F-CTRL-SA-PIN two-leg b1 (rel)', s['b1_twoleg_rel_max'], constants['pin_twoleg_tol_rel']),
        ('F-CTRL-SA-PIN two-leg first-order slope S (abs)', s['twoleg_S_abs_max'], constants['tau_agg']),
        ('F-CTRL-SA-ZERO r(0) (abs)', s['zero_ctrl_max_abs'], constants['zero_ctrl_tol_abs']),
        ('F-CTRL-SA-RECON S2-E2 Hill t4 (abs)', s['recon_max_abs_E2_Hill']['t4'], constants['recon_tol_abs_E2_Hill']),
        ('F-CTRL-SA-RECON S2-E2 Hill t2 (abs)', s['recon_max_abs_E2_Hill']['t2'], constants['recon_tol_abs_E2_Hill']),
        ('F-CTRL-SA-RECON robustness arms kappa vs bi (rel)', robust_res, constants['recon_tol_rel_robust']),
        ('F-CTRL-SA-S N-1 bi (abs)', max(abs(v['bi']) for v in n['N-1'].values()), tau),
        ('F-CTRL-SA-S N-1 fit where banked (abs)', max(abs(v['fit']) for v in n['N-1'].values() if v['fit'] is not None), tau),
        ('F-CTRL-SA-K24 N-2 every estimator (abs)', max(max(abs(v[e]) for e in ('fit7', 'bi_chat', 'bi_cc', 'bi_5x5')) for v in n['N-2'].values()), kf),
        ('F-CTRL-SA-L2NULL N-3 fit and bi (abs)', max(max(abs(v['fit']), abs(v['bi'])) for v in n['N-3'].values()), kf),
        ('F-CTRL-SA-L2NULL N-4 fit7, bi, k12 (abs)', max(max(abs(v['fit7']), abs(v['bi_5x5']), abs(v['k12_chat_t2sq'] or 0.0)) for v in n['N-4'].values()), kf),
        ('F-CTRL-SA-L2NULL t2 alone at t2 = 1 (abs)', s['pure_l2_change_t1_max'], constants['l2null_t1_tol_abs']),
    ]
    for name, val, tol in checks:
        guard(val <= tol, 'preflight failed: %s = %.3e > %.1e' % (name, val, tol))
    return checks


def exact_rms_checks():
    """<P2^2> = 1/5, <P4^2> = 1/9 (Legendre orthogonality over mu in [-1, 1]) and <K4~^2> = 4/21, <K4~> = 0 over the
    unit sphere, K4~ = (5/2)(x^4 + y^4 + z^4 - 3/5), from the exact sphere moments
    <x^2a y^2b z^2c> = (2a-1)!!(2b-1)!!(2c-1)!!/(2s+1)!!, s = a + b + c.  Exact rational arithmetic."""
    def dfact(n):
        r = 1
        while n > 1:
            r *= n
            n -= 2
        return r

    def mom(a, b, c):
        return Fraction(dfact(2 * a - 1) * dfact(2 * b - 1) * dfact(2 * c - 1), dfact(2 * (a + b + c) + 1))

    def leg_sq(coeffs):  # <p(mu)^2> over mu uniform in [-1, 1]; p given by {power: coefficient}
        tot = Fraction(0)
        for i, ci in coeffs.items():
            for j, cj in coeffs.items():
                n = i + j
                tot += ci * cj * (Fraction(1, n + 1) if n % 2 == 0 else 0)
        return tot
    P2 = {2: Fraction(3, 2), 0: Fraction(-1, 2)}
    P4 = {4: Fraction(35, 8), 2: Fraction(-30, 8), 0: Fraction(3, 8)}
    S1 = 3 * mom(2, 0, 0)
    S2 = 3 * mom(4, 0, 0) + 6 * mom(2, 2, 0)
    K4_mean = Fraction(5, 2) * (S1 - Fraction(3, 5))
    K4_sq = Fraction(25, 4) * (S2 - 2 * Fraction(3, 5) * S1 + Fraction(9, 25))
    res = {'P2_sq': leg_sq(P2), 'P4_sq': leg_sq(P4), 'K4_sq': K4_sq, 'K4_mean': K4_mean}
    guard(res == {'P2_sq': Fraction(1, 5), 'P4_sq': Fraction(1, 9), 'K4_sq': Fraction(4, 21), 'K4_mean': Fraction(0)},
          'rms closed forms failed the exact check')
    return {k: str(v) for k, v in res.items()}


def assemble(raw, glob, meta, builder_md5):
    grids = dict(GRIDS_FIXED)
    grids.update(glob['grids'])
    constants = dict(CONSTANTS)
    raw_all = {'keys': raw['keys'], 'regime': glob['regime']}
    prov = {'keys/<K>/' + dest: {'src': alias, 'pointer': ptmpl, 'scope': scope} for dest, alias, ptmpl, scope in FIELDS}
    for dest, alias, p in GLOBAL_FIELDS:
        prov[dest if not dest.startswith('regime/') else 'raw/' + dest] = {'src': alias, 'pointer': p, 'scope': 'global'}
    doc = {
        '_meta': {'gate': GATE, 'file_schema': FILE_SCHEMA, 'builder': 'sa_build_pinned_inputs.py',
                  'builder_md5': builder_md5, 'base_ledger_md5': 'd4c42a53cbd6d325ebc740879288e844',
                  'contents': 'banked values by named key + fixed constants, grid generators and tokens + a derived '
                              'reference section; no anchor value; no observational number; no point count',
                  'elections_applied': ELECTIONS,
                  'cubic_term_order': CUBIC_TERM_ORDER, 'dqf_basis_order': DQF_BASIS,
                  'dqf_basis_note': 'index order of the chat quadform-basis diagnostic; asserted by this builder: k7[0..2] '
                                    'equal the fit7 kappa22, kappa24, kappa44 of the same key bit for bit and k7[3..6] '
                                    'equal the CC named cubic terms to 1e-4 relative; k12[3..6] equal k7[3..6] to 1e-8 '
                                    'relative (the shared order); the k12 quartic indices 7..11 follow the monomial order '
                                    'and are not independently confirmed (no instrument reads them)'},
        'sources': meta,
        'provenance': prov,
        'structure': STRUCTURE,
        'tokens': TOKENS,
        'constants': constants,
        'grids': grids,
        'raw': raw_all,
        'rms_exact_check': exact_rms_checks(),
    }
    doc['derived'] = derive(raw_all_for_derive(raw_all), constants, grids)
    return doc


def raw_all_for_derive(raw_all):
    return {'keys': raw_all['keys'], 'regime': raw_all['regime']}


def serialize(doc):
    return (json.dumps(doc, indent=1, sort_keys=True, ensure_ascii=True, allow_nan=False) + '\n').encode('ascii')


def verify_written(path, docs):
    b = open(path, 'rb').read()
    d = json.loads(b.decode('ascii'))
    # (1) derived is a pure function of the file's own raw / constants / grids
    guard(serialize_part(derive(raw_all_for_derive(d['raw']), d['constants'], d['grids'])) == serialize_part(d['derived']),
          'derived section does not re-derive bit-identically from the written file')
    # (2) every raw value equals its source by pointer, bit for bit
    n = 0
    for dest, alias, ptmpl, scope in FIELDS:
        for k in scope_keys(scope, docs):
            v_src = ptr_get(docs[alias], ptmpl.format(K=k))
            cur = d['raw']['keys'][k]
            for p in dest.split('/'):
                cur = cur[p]
            guard(json.dumps(cur) == json.dumps(v_src) and cur == v_src, 'raw value differs from source: %s %s' % (k, dest))
            n += 1
    for dest, alias, p in GLOBAL_FIELDS:
        cur = d['grids'][dest.split('/')[1]] if dest.startswith('grids/') else d['raw']['regime'][dest.split('/')[1]]
        guard(cur == ptr_get(docs[alias], p), 'global value differs from source: ' + dest)
        n += 1
    # (3) the round trip is byte-stable
    guard(serialize(d) == b, 'serialization is not byte-stable')
    return b, n


def serialize_part(x):
    return json.dumps(x, sort_keys=True, ensure_ascii=True, allow_nan=False)


def counts(doc):
    g, D = doc['grids'], doc['constants']['D']
    tg = g['t_grid']
    return {'t_grid': len(tg),
            'fit_window_0.25_inclusive': len([t for t in tg if abs(t) <= D]),
            'fit_window_0.25_strict': len([t for t in tg if abs(t) < D]),
            'window_0.1_inclusive': len([t for t in tg if abs(t) <= 0.1]),
            'window_0.1_strict': len([t for t in tg if abs(t) < 0.1]),
            't2t4_axis': len(g['t2t4_axis']), 't2t4_grid': len(g['t2t4_axis']) ** 2,
            'area_grid': g['area_grid']['nodes_per_axis'] ** 2,
            'raw_keys': len(doc['raw']['keys'])}


def main():
    if len(sys.argv) not in (2, 3):
        print(__doc__)
        return 2
    repo = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) == 3 else OUT_DEFAULT
    guard(sys.float_info.mant_dig == 53, 'IEEE-754 double precision required')
    builder_md5 = hashlib.md5(open(os.path.abspath(__file__), 'rb').read()).hexdigest()
    docs, meta = load_sources(repo)
    raw, glob = build_raw(docs)
    doc = assemble(raw, glob, meta, builder_md5)
    pre = preflight(doc['derived'], doc['constants'])
    data = serialize(doc)
    with open(out, 'wb') as fh:
        fh.write(data)
    try:
        b, n = verify_written(out, docs)
    except Exception:
        os.remove(out)
        raise
    dv, c = doc['derived'], counts(doc)
    print('G-MSCS-A pinned inputs -- builder md5 %s' % builder_md5)
    print('sources (7, full md5 + bytes verified):')
    for a, m in meta.items():
        print('  %-7s %s  %s  %6d B' % (a, m['md5'], m['path'], m['bytes']))
    print('counts from the generators (printed, never written): %s' % ', '.join('%s %d' % kv for kv in c.items()))
    print('self-verification: derived re-derived bit-identically from the written file; %d raw values equal their sources by pointer; byte-stable round trip' % n)
    print('rms exact: %s' % doc['rms_exact_check'])
    print('preflight on banked values (the legs repeat these at Phase 0):')
    for name, val, tol in pre:
        print('  PASS %-52s %.2e <= %.0e' % (name, val, tol))
    print('\nS2-E2 Hill coefficients (memo section 0 table):')
    print('  %-15s %15s %15s %9s %15s %15s' % ('key', 'k44 record', 'k44 bi', 'res', 'k2 record', 'k2 bi'))
    for k in KEYS:
        f4, f2 = dv['families'][k]['E2_Hill']['t4'], dv['families'][k]['E2_Hill']['t2']
        print('  %-15s %+15.6e %+15.6e %9.2e %+15.6e %+15.6e' % (k, f4['kappa'], f4['kappa_bi'], f4['fit_res_rel'], f2['kappa'], f2['kappa_bi']))
    print('\nreach R^w = (1 + mu) * hull (memo section 0 table):')
    for k in KEYS:
        print('  %-15s ' % k + '  '.join('%s [%+.3e, %+.3e]' % (arm, *dv['reach'][k][arm]['widened']) for arm in ARMS))
    u = dv['unions']
    print('\nunions: widened all [%+.4e, %+.4e]  widened primary [%+.4e, %+.4e]' % (*u['widened_all'], *u['widened_primary']))
    print('        hull all    [%+.4e, %+.4e]  hull primary    [%+.4e, %+.4e]' % (*u['hull_all'], *u['hull_primary']))
    print('synthetic intervals: ' + '  '.join('%s [%+.4e, %+.4e]' % (k, *v) for k, v in sorted(dv['synthetic'].items())))
    print('\nhex null-ray slopes |t4/t2|:')
    for k in HEX:
        print('  %-12s ' % k + '  '.join('%s %.4f' % kv for kv in sorted(dv['hex_quadform'][k]['null_ray_slope'].items())) + '  S2-h: ' + dv['hex_quadform'][k]['h_Hill_form'])
    s = dv['summary']
    print('\nsummary:')
    for key in sorted(s):
        v = s[key]
        if isinstance(v, dict):
            print('  %s: %s' % (key, {kk: (('%.4g' % vv) if isinstance(vv, float) else {a: '%.4g' % b for a, b in vv.items()}) for kk, vv in v.items()}))
        else:
            print('  %s: %.6g' % (key, v))
    print('\nwrote %s  md5 %s  %d B' % (out, hashlib.md5(b).hexdigest(), len(b)))
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except GuardError as e:
        print('GUARD FAILED: %s' % e)
        sys.exit(1)
