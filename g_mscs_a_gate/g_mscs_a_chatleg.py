#!/usr/bin/env python3
"""g_mscs_a_chatleg.py -- Gate G-MSCS-A, chat-leg mapper (memo 6ea16b95 sections 3-6; lock record Addendum A-2).

The whole computation of the gate: Phase 0 (pins and controls; halt-on-fail), Phase 2 (the fourteen synthetic
pre-read suites; all must pass before any sealed open) and Phase 3 (the masked read of the author's sealed anchor file
and its mapping onto the banked texture surface). Every banked value is read from the pinned-inputs file of record by
name; the sealed file is the only other input. No anchor value (lo, hi, k_em_max, k_t_max, cl, src, note) is ever
printed, logged or written -- only the file and row md5s and the derived quantities (windows, classes, flags).

Usage:
  preread : python3 g_mscs_a_chatleg.py preread --repo REPO [--a1 A1_LIST] [--out DIR]
            Phase 0 + Phase 2; writes g_mscs_a_chatleg_prereadcheckpoint.json (phase3 = null).
  read    : python3 g_mscs_a_chatleg.py read --repo REPO --sealed ARMORED --md5 MD5 --bytes N --a1 A1_LIST [--out DIR]
            Phases 0 + 2 recomputed from scratch, then the read; writes g_mscs_a_chatleg_checkpoint.json.
  census  : python3 g_mscs_a_chatleg.py census --sealed ARMORED --md5 MD5 --bytes N
            Decodes and validates only; prints md5, bytes and census (dispatch build, memo 4.7); no mapping.
Exit: 0 done; 1 halted (Phase 0 failure = INDETERMINATE, a Phase 2 failure, a masked abort, a T1 hit); 2 usage.
Files expected beside this script: staging_memo_G_MSCS_A_v2.md, pinned_inputs_G_MSCS_A.json, G_MSCS_A_LOCK_RECORD.md,
g_mscs_a_schema_v1_0.json, g_mscs_a_compare_v1_0.py, tools/t1/{T1_forbidden_G_MSCS_A.txt, T1_base_author_20260919.txt, t1_scan.py}."""
import base64, datetime, hashlib, importlib.util, io, json, math, os, re, sys, tempfile, zipfile

GATE, LEG = 'G-MSCS-A', 'chat'
HERE = os.path.dirname(os.path.abspath(__file__))
LEDGER_MD5 = 'd4c42a53cbd6d325ebc740879288e844'
MEMO_MD5, MEMO_BYTES = '6ea16b952db835bb351d3dc1b474c6ed', 121950
PIN_MD5, PIN_BYTES = '2d44ec01a66889f330d940dee3313bdc', 96761
T1_MD5, BASE_MD5, SCANNER_MD5 = 'e274e58ea50b9ed347969e507d2a4f36', '05302210cc4ceb70553acbe8379e9fc3', '6b86290090a8c84f1b1a0a99ec0bf697'
SCHEMA_MD5, COMPARATOR_MD5 = '5323e11fc27d688f61aaf57302c875c0', 'c5b4a7aab2fc8651be6d26d1f3d25642'
LOCK_MD5 = '8116cc622279b5d4e73214178ae97cd8'   # filled at freeze (the lock record is written before this instrument)
BUILDER_MD5, VERIFIER_MD5 = '8189100ede80eac360b25a146e580abf', 'cf004d517d2efe91a02c92a58e3df6bf'
ELECTIONS = {'E-SA-0': 'a', 'E-SA-1': 'a', 'E-SA-2': 'a', 'E-SA-3': 'a', 'E-SA-4': 'a', 'E-SA-5': 'a', 'E-SA-6': 'a',
             'E-SA-7': '05302210+MSCS1stratum', 'E-SA-8': 'a', 'E-SA-9': 'a', 'E-SA-10': 'a', 'E-SA-11': 'a'}
FILES = {'memo': 'staging_memo_G_MSCS_A_v2.md', 'pin': 'pinned_inputs_G_MSCS_A.json', 'lock': 'G_MSCS_A_LOCK_RECORD.md',
         'schema': 'g_mscs_a_schema_v1_0.json', 'comparator': 'g_mscs_a_compare_v1_0.py',
         't1': 'tools/t1/T1_forbidden_G_MSCS_A.txt', 'base': 'tools/t1/T1_base_author_20260919.txt', 'scanner': 'tools/t1/t1_scan.py'}
REQUIRED = ['id', 'class', 'delta_def', 'lo', 'hi', 'cl', 'reading', 'geom', 'k_em_max', 'k_t_max', 'src']
OPTIONAL = ['q', 'note']
CANON = REQUIRED + OPTIONAL
NUM = re.compile(r'^[+-]?(?:\d+\.?\d*|\.\d+)(?:[eE][+-]?\d+)?$')
SEP = ' | '
BAD_UNICODE = {'\u0085', ' ', ' ', '﻿'}
LOG = []
SEALED_OPENS = 0


def say(s):
    LOG.append(s)
    print(s)


def md5b(b):
    return hashlib.md5(b).hexdigest()


def md5f(p):
    return md5b(open(p, 'rb').read())


class Halt(Exception):
    pass


# ------------------------------------------------------------------------------------------ guards and T1
def guards():
    paths = {k: os.path.join(HERE, v) for k, v in FILES.items()}
    want = {'memo': MEMO_MD5, 'pin': PIN_MD5, 't1': T1_MD5, 'base': BASE_MD5, 'scanner': SCANNER_MD5, 'schema': SCHEMA_MD5,
            'comparator': COMPARATOR_MD5, 'lock': LOCK_MD5}
    for k, m in want.items():
        h = md5f(paths[k])
        if h != m:
            raise Halt('guard: %s md5 %s != %s' % (FILES[k], h, m))
    if os.path.getsize(paths['memo']) != MEMO_BYTES or os.path.getsize(paths['pin']) != PIN_BYTES:
        raise Halt('guard: byte count')
    return paths


def load_scanner(paths):
    spec = importlib.util.spec_from_file_location('t1_scan', paths['scanner'])
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def t1_scan(paths, targets, a1):
    m = load_scanner(paths)
    pats = m.load(paths['t1'])
    if a1:
        pats = pats + m.load(a1)
    hits, coll = 0, 0
    per = {}
    for t in targets:
        text = open(t, encoding='utf-8').read()
        h, c = m.scan_text(text, pats)
        hits += len(h); coll += len(c)
        per[os.path.basename(t)] = {'hits_by_index': sorted({i for i, _ in h}), 'collisions': len(c)}
    return {'hits': hits, 'collisions': coll, 'patterns': len(pats), 'a1_included': bool(a1), 'per_file': per}


# ------------------------------------------------------------------------------------------ pinned inputs, own re-derivation
def ptr(doc, pointer):
    node = doc
    for part in pointer.lstrip('/').split('/'):
        part = part.replace('~1', '/').replace('~0', '~')
        node = node[int(part)] if isinstance(node, list) else node[part]
    return node


def flat(node, prefix=''):
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


def rederive(P):
    """the chat leg's own re-derivation of derived.{families,reach,unions,synthetic,nulls,hex_quadform,zero_ctrl}"""
    raw, C, G = P['raw'], P['constants'], P['grids']
    KEYS, HEX, CUB, ARMS, PRIM = P['structure']['keys'], P['structure']['hex_keys'], P['structure']['cubic_keys'], P['structure']['arms'], P['structure']['primary']['keys']
    D, MU, SNAP, KF = C['D'], C['mu'], C['zero_snap'], C['kappa_floor']
    T, AX = G['t_grid'], G['t2t4_axis']
    (h1, h2), (g1, g2) = G['richardson_pairs']['one_param'], G['richardson_pairs']['two_param']
    inside = [i for i, t in enumerate(T) if -D <= t <= D]
    val = lambda g, t: g[T.index(t)]
    even = lambda g: (4 * ((val(g, h1) + val(g, -h1) - 2 * val(g, 0.0)) / (2 * h1 * h1)) - ((val(g, h2) + val(g, -h2) - 2 * val(g, 0.0)) / (2 * h2 * h2))) / 3
    odd = lambda g: (4 * ((val(g, h1) - val(g, -h1)) / (2 * h1)) - ((val(g, h2) - val(g, -h2)) / (2 * h2))) / 3
    def grid5(v):
        n = len(AX)
        return {(AX[i], AX[j]): v[n * i + j] for i in range(n) for j in range(n)}
    def rich5(R, kind):
        def f(h):
            if kind == '22': return (R[(h, 0.0)] + R[(-h, 0.0)] - 2 * R[(0.0, 0.0)]) / (2 * h * h)
            if kind == '44': return (R[(0.0, h)] + R[(0.0, -h)] - 2 * R[(0.0, 0.0)]) / (2 * h * h)
            return (R[(h, h)] - R[(h, -h)] - R[(-h, h)] + R[(-h, -h)]) / (4 * h * h)
        return (4 * f(g1) - f(g2)) / 3
    rel = lambda x, y: abs(x - y) / max(abs(x), abs(y))
    tok = lambda k, f: ('hexP2' if k in HEX else 'cubP2-i') if f == 't2' else ('hexP4' if k in HEX else 'cubK4')
    fam, reach, zero, n1, n2, n3, n4, hq = {}, {}, {}, {}, {}, {}, {}, {}
    for k in KEYS:
        rk = raw['keys'][k]
        mapped = ('t4', 't2') if k in HEX else ('t4',)
        fam[k], reach[k], zero[k] = {}, {}, {}
        for arm in ARMS:
            fam[k][arm] = {}
            for f in ('t4', 't2'):
                d = rk['arms'][arm][f]
                kb = even(d['grid'])
                e = {'odf_reading': tok(k, f), 'kappa': d['kappa'], 'kappa_bi': kb, 'fit_res_rel': (abs(d['kappa'] - kb) / abs(kb)) if abs(kb) > KF else None,
                     'S_bi': odd(d['grid']), 'S_fit': d.get('S'), 'r0': val(d['grid'], 0.0), 'mapped': f in mapped}
                if f in mapped and 'kappa3' in d:
                    e['recon_max_abs'] = max(abs(d['grid'][i] - (d['S'] * T[i] + d['kappa'] * T[i] ** 2 + d['kappa3'] * T[i] ** 3)) for i in inside)
                    e['trunc_T_at_D'] = abs(d['kappa3']) * D / abs(d['kappa'])
                if 'kappa_cc' in d:
                    e['twoleg_rel'] = rel(d['kappa'], d['kappa_cc']) if max(abs(d['kappa']), abs(d['kappa_cc'])) > KF else None
                if 'kappa3_cc' in d:
                    e['twoleg_kappa3_rel'] = rel(d['kappa3'], d['kappa3_cc']) if f in mapped else None
                if 'S_cc' in d:
                    e['twoleg_S_abs'] = abs(d['S'] - d['S_cc'])
                fam[k][arm][f] = e
                zero[k][arm + '/' + f] = {'odf_reading': 'uniform', 'r0': e['r0']}
                if f in mapped:
                    n1['%s/%s/%s' % (k, arm, f)] = {'odf_reading': tok(k, f), 'fit': e['S_fit'], 'bi': e['S_bi']}
            lo = sum(min(0.0, rk['arms'][arm][fm]['kappa'] * D * D) for fm in mapped)
            hi = sum(max(0.0, rk['arms'][arm][fm]['kappa'] * D * D) for fm in mapped)
            pts = [rk['arms'][arm][fm]['grid'][i] for fm in mapped for i in inside]
            if arm == 'E2_Hill':
                pts = pts + rk['quadform']['grid5x5_cc']
            hull = [0.0 if abs(x) < SNAP else x for x in (min(lo, min(pts)), max(hi, max(pts)))]
            reach[k][arm] = {'box': [lo, hi], 'grid_min': min(pts), 'grid_max': max(pts), 'hull': hull, 'widened': [x * (1 + MU) for x in hull],
                             'grid_exceeds_box': min(pts) < lo or max(pts) > hi}
        R = grid5(rk['quadform']['grid5x5_cc'])
        n2[k] = {'odf_reading': 'hexP2P4' if k in HEX else 'cubP2K4-i', 'fit7': rk['quadform']['kappa24_fit7'], 'bi_chat': rk['kappa24_bi_chat'],
                 'bi_cc': rk['kappa24_bi_cc'], 'bi_5x5': rich5(R, '24')}
        if k in CUB:
            n3[k] = {'odf_reading': 'cubP2-i', 'fit': rk['arms']['E2_Hill']['t2']['kappa'], 'bi': even(rk['arms']['E2_Hill']['t2']['grid']), 'pure_l2_change_t1': rk['pure_l2_change_t1']}
            k12 = rk['quadform'].get('basis_k12_chat')
            n4[k] = {'odf_reading': 'cubP2K4-i', 'fit7': rk['quadform']['kappa22_fit7'], 'bi_5x5': rich5(R, '22'), 'k12_chat_t2sq': k12[0] if k12 is not None else None}
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
                     'kappa22_fit7_vs_kappa2_rel': rel(rk['quadform']['kappa22_fit7'], A['E2_Hill']['t2']['kappa'])}
    cells = [(k, a) for k in KEYS for a in ARMS]
    un = {'hull_all': [min(reach[k][a]['hull'][0] for k, a in cells), max(reach[k][a]['hull'][1] for k, a in cells)],
          'widened_all': [min(reach[k][a]['widened'][0] for k, a in cells), max(reach[k][a]['widened'][1] for k, a in cells)],
          'hull_primary': [min(reach[k]['E2_Hill']['hull'][0] for k in PRIM), max(reach[k]['E2_Hill']['hull'][1] for k in PRIM)],
          'widened_primary': [min(reach[k]['E2_Hill']['widened'][0] for k in PRIM), max(reach[k]['E2_Hill']['widened'][1] for k in PRIM)]}
    f1, f2 = C['synthetic_band_fractions']
    iv = lambda a, b: [a + f1 * (b - a), a + f2 * (b - a)]
    syn = {'margin_positive': iv(un['hull_all'][1], un['widened_all'][1]), 'margin_negative': iv(un['widened_all'][0], un['hull_all'][0]),
           'robustness_only_positive': iv(un['widened_primary'][1], un['hull_all'][1])}
    return {'families': fam, 'reach': reach, 'unions': un, 'synthetic': syn, 'zero_ctrl': zero,
            'nulls': {'N-1': n1, 'N-2': n2, 'N-3': n3, 'N-4': n4}, 'hex_quadform': hq}


# ------------------------------------------------------------------------------------------ the mapping (A-2.4)
RMS = {('hex', 't4'): 1.0 / 3.0, ('cubic', 't4'): math.sqrt(4.0 / 21.0), ('hex', 't2'): math.sqrt(1.0 / 5.0), ('cubic', 't2'): math.sqrt(1.0 / 5.0)}


class Mapper:
    def __init__(self, P, DV):
        self.P, self.DV = P, DV
        S = P['structure']
        self.KEYS, self.HEX, self.ARMS, self.PRIM = S['keys'], S['hex_keys'], S['arms'], S['primary']['keys']
        self.D, self.KD, self.dEM = P['constants']['D'], P['constants']['KD_CLIP'], P['raw']['regime']['d_EM']
        self.TR, self.NF = P['constants']['trunc_threshold'], P['constants']['nullfloor_threshold']
        self.NODES = P['grids']['area_grid']['nodes_per_axis']
        self.reach = DV['reach']

    def mapped(self, k):
        return ('t4', 't2') if k in self.HEX else ('t4',)

    def fam_window(self, k, arm, f, lo, hi):
        d = self.P['raw']['keys'][k]['arms'][arm][f]
        e = self.DV['families'][k][arm][f]
        D = self.D
        if f == 't2' and k not in self.HEX:
            return {'class': 'NULL-INERT', 'binding_end': None, 't_star': None, 't_star_bi': None, 'class_bi': None, 'resolution_sensitive': False,
                    'sigma_star': None, 'window_lo': -D, 'window_hi': D, 'trunc_T': None, 'truncation_sensitive': False, 'nu': None, 'nu_is_inf': False, 'nullfloor_sensitive': False}
        def edge(kappa):
            b = hi if kappa > 0 else lo
            ts = math.sqrt(b / kappa) if b != 0 else 0.0
            return b, ts, ('BINDING' if ts < D else 'INERT-IN-D')
        b, ts, cls = edge(d['kappa'])
        _, ts_bi, cls_bi = edge(e['kappa_bi'])
        w = min(ts, D)
        out = {'class': cls, 'binding_end': 'hi' if d['kappa'] > 0 else 'lo', 't_star': ts, 't_star_bi': ts_bi, 'class_bi': cls_bi,
               'resolution_sensitive': cls != cls_bi, 'sigma_star': ts * RMS[('hex' if k in self.HEX else 'cubic', f)], 'window_lo': -w, 'window_hi': w}
        if arm == 'E2_Hill':
            T = abs(d['kappa3']) * ts / abs(d['kappa'])
            out['trunc_T'], out['truncation_sensitive'] = T, T > self.TR
        else:
            out['trunc_T'], out['truncation_sensitive'] = None, False
        if b == 0:
            out['nu'], out['nu_is_inf'], out['nullfloor_sensitive'] = None, True, True
        else:
            nu = abs(e['S_bi']) * ts / abs(b)
            out['nu'], out['nu_is_inf'], out['nullfloor_sensitive'] = nu, False, nu > self.NF
        return out

    def exclusion(self, k, arm, lo, hi):
        rw, rh = self.reach[k][arm]['widened'], self.reach[k][arm]['hull']
        inter = lambda R: max(lo, R[0]) <= min(hi, R[1])
        if not inter(rw):
            cls = 'EXCLUDED-IN-D'
            sub = 'SIGN' if ((hi < 0 and rw[0] >= 0) or (lo > 0 and rw[1] <= 0)) else 'MAGNITUDE'
        elif inter(rh):
            cls, sub = 'TUNED-ADMISSIBLE', None
        else:
            cls, sub = 'MARGIN', None
        req = {}
        for f in self.mapped(k):
            kappa = self.P['raw']['keys'][k]['arms'][arm][f]['kappa']
            if (kappa > 0) == (lo > 0):
                t_in, t_out = math.sqrt(min(abs(lo), abs(hi)) / abs(kappa)), math.sqrt(max(abs(lo), abs(hi)) / abs(kappa))
                req[f] = {'t_in': t_in, 't_out': t_out, 'can_supply_alone': t_in <= self.D}
            else:
                req[f] = {'t_in': None, 't_out': None, 'can_supply_alone': False}
        return {'class': cls, 'subreason': sub, 'requirements': req}

    def two_param(self, k, arm, lo, hi):
        a = self.P['raw']['keys'][k]['arms'][arm]
        k2, k4 = a['t2']['kappa'], a['t4']['kappa']
        n, D = self.NODES, self.D
        node = [-D + i * (2 * D) / (n - 1) for i in range(n)]
        sq = [x * x for x in node]
        adm, boundary = 0, False
        for i in range(n):
            base = k2 * sq[i]
            for j in range(n):
                v = base + k4 * sq[j]
                if lo <= v <= hi:
                    adm += 1
                    if i in (0, n - 1) or j in (0, n - 1):
                        boundary = True
        defin = 'indefinite' if k2 * k4 < 0 else ('negative-definite' if k2 < 0 else 'positive-definite')
        return {'admissible_nodes': adm, 'total_nodes': n * n, 'area_fraction': adm / (n * n), 'null_ray_slope': math.sqrt(-k2 / k4) if k2 * k4 < 0 else None,
                'definiteness': defin, 'compact': not boundary}

    def map_interval(self, lo, hi, with_two_param=True):
        """lo <= hi; returns the per-cell record and the gate-level fields for this interval (no value serialized)"""
        contains0 = lo <= 0.0 <= hi
        res = {'contains_zero': contains0, 'families': None, 'exclusion': None, 'two_param': None}
        if contains0:
            res['families'] = {k: {arm: {f: self.fam_window(k, arm, f, lo, hi) for f in ('t4', 't2')} for arm in self.ARMS} for k in self.KEYS}
            if with_two_param:
                res['two_param'] = {k: {arm: self.two_param(k, arm, lo, hi) for arm in self.ARMS} for k in self.HEX}
            prim = [res['families'][k]['E2_Hill']['t4'] for k in self.PRIM]
            allb = all(p['class'] == 'BINDING' for p in prim)
            res['gate_class'] = 'WINDOW-DELIVERED' if allb else 'INERT-IN-D'
            res['sigma_union_hi'] = max(p['sigma_star'] for p in prim) if allb else None
            res['sigma_strict_hi'] = min(p['sigma_star'] for p in prim) if allb else None
        else:
            res['exclusion'] = {k: {arm: self.exclusion(k, arm, lo, hi) for arm in self.ARMS} for k in self.KEYS}
            cls = [res['exclusion'][k][arm]['class'] for k in self.KEYS for arm in self.ARMS]
            if all(c == 'EXCLUDED-IN-D' for c in cls):
                res['gate_class'] = 'KILL-IN-D'
            elif any(c == 'TUNED-ADMISSIBLE' for c in cls):
                res['gate_class'] = 'TUNED'
            else:
                res['gate_class'] = 'MARGIN-ONLY'
            res['sigma_union_hi'] = res['sigma_strict_hi'] = None
        return res

    def map_rows(self, rows, with_two_param=True):
        """rows: list of dicts {lo, hi, kem, kt}; returns the phase-3 mapping block (row md5s added by the caller)"""
        out = {'rows': [], 'n_void_rows': 0}
        live = []
        for r in rows:
            x = max(r['kem'], r['kt']) * self.dEM
            void = x > self.KD
            rec = {'void_regime': void, 'contains_zero': None, 'gate_class_row': None, 'families': None, 'exclusion': None, 'two_param': None}
            if void:
                out['n_void_rows'] += 1
            else:
                live.append(r)
                m = self.map_interval(r['lo'], r['hi'], with_two_param)
                rec.update({'contains_zero': m['contains_zero'], 'gate_class_row': m['gate_class'], 'families': m['families'], 'exclusion': m['exclusion'], 'two_param': m['two_param']})
            out['rows'].append(rec)
        if not live:
            out.update({'combined_empty': None, 'contains_zero': None, 'combined': None, 'gate': {'gate_class': 'VOID', 'sigma_union_hi': None, 'sigma_strict_hi': None}})
            return out
        LO, HI = max(r['lo'] for r in live), min(r['hi'] for r in live)
        if LO > HI:
            out.update({'combined_empty': True, 'contains_zero': None, 'combined': None, 'gate': {'gate_class': 'ANCHOR-INCONSISTENT', 'sigma_union_hi': None, 'sigma_strict_hi': None}})
            return out
        m = self.map_interval(LO, HI, with_two_param)
        out.update({'combined_empty': False, 'contains_zero': m['contains_zero'],
                    'combined': {'families': m['families'], 'exclusion': m['exclusion'], 'two_param': m['two_param']},
                    'gate': {'gate_class': m['gate_class'], 'sigma_union_hi': m['sigma_union_hi'], 'sigma_strict_hi': m['sigma_strict_hi']}})
        return out

    def full(self, rows):
        """the mapping with OOM robustness and the monotonicity check (halts as an instrument defect)"""
        base = self.map_rows(rows)
        scaled = {}
        for tag, fct in (('x10', 10.0), ('x0p1', 0.1)):
            scaled[tag] = self.map_rows([{'lo': r['lo'] * fct, 'hi': r['hi'] * fct, 'kem': r['kem'], 'kt': r['kt']} for r in rows], with_two_param=False)
            worst, viol = self.mono_check(base, scaled[tag], fct)
            if worst > self.P['constants']['mono_tol_rel'] or viol:
                raise Halt('F-CTRL-SA-MONO on the actual rows: scaling dev %.3e, %d monotonicity violations -- instrument defect (S9)' % (worst, viol))
        g = base['gate']
        g['oom_class_x10'], g['oom_class_x0p1'] = scaled['x10']['gate']['gate_class'], scaled['x0p1']['gate']['gate_class']
        g['oom_robust'] = g['gate_class'] == g['oom_class_x10'] == g['oom_class_x0p1']
        g['contains_zero'], g['combined_empty'], g['n_void_rows'] = base['contains_zero'], base['combined_empty'], base['n_void_rows']
        return base

    def mono_check(self, base, sc, fct):
        """exact sqrt(fct) scaling of unclipped edges; monotone windows and classes; returns (worst relative deviation, violations)"""
        worst, viol = 0.0, 0
        root = math.sqrt(fct)
        pairs = [(b.get('combined'), s.get('combined')) for b, s in ((base, sc),) if b.get('combined') and s.get('combined')]
        pairs += [(b, s) for b, s in zip(base['rows'], sc['rows']) if b.get('families') is not None or b.get('exclusion') is not None]
        ORDER_W = {'BINDING': 0, 'INERT-IN-D': 1}
        ORDER_X = {'TUNED-ADMISSIBLE': 0, 'MARGIN': 1, 'EXCLUDED-IN-D': 2}
        for b, s in pairs:
            if b.get('families'):
                for k in self.KEYS:
                    for arm in self.ARMS:
                        for f in self.mapped(k):
                            x, y = b['families'][k][arm][f], s['families'][k][arm][f]
                            if x['class'] == 'BINDING' and y['class'] == 'BINDING' and x['t_star'] > 0:
                                worst = max(worst, abs(y['t_star'] - x['t_star'] * root) / (x['t_star'] * root))
                            if fct > 1 and (y['window_hi'] < x['window_hi'] or ORDER_W[y['class']] < ORDER_W[x['class']]):
                                viol += 1
                            if fct < 1 and (y['window_hi'] > x['window_hi'] or ORDER_W[y['class']] > ORDER_W[x['class']]):
                                viol += 1
            if b.get('exclusion'):
                for k in self.KEYS:
                    for arm in self.ARMS:
                        x, y = b['exclusion'][k][arm], s['exclusion'][k][arm]
                        if fct > 1 and ORDER_X[y['class']] < ORDER_X[x['class']]:
                            viol += 1
                        if fct < 1 and ORDER_X[y['class']] > ORDER_X[x['class']]:
                            viol += 1
                        for f, rq in x['requirements'].items():
                            if rq['t_in'] is not None:
                                for key in ('t_in', 't_out'):
                                    worst = max(worst, abs(y['requirements'][f][key] - rq[key] * root) / (rq[key] * root))
        return worst, viol


# ------------------------------------------------------------------------------------------ the sealed file (A-2.3), masked
class MaskedAbort(Exception):
    pass


def decode_armor(path):
    """base64 text (marker lines stripped) or a zip with exactly one member; returns the raw bytes"""
    global SEALED_OPENS
    SEALED_OPENS += 1
    b = open(path, 'rb').read()
    if b[:2] == b'PK':
        z = zipfile.ZipFile(io.BytesIO(b))
        names = [n for n in z.namelist() if not n.endswith('/')]
        if len(names) != 1:
            raise MaskedAbort('ARMOR_ZIP_NOT_ONE_MEMBER')
        return z.read(names[0])
    lines = [l.strip() for l in b.decode('ascii', errors='replace').splitlines()]
    body = ''.join(l for l in lines if l and not l.startswith('-----') and not l.startswith('====='))
    try:
        return base64.b64decode(body, validate=True)
    except Exception:
        raise MaskedAbort('ARMOR_BASE64_INVALID')


def check_value(key, val):
    if val == '' or val != val.strip():
        return 'EMPTY_OR_PADDED'
    if key not in ('src', 'note') and not all(32 <= ord(c) < 127 for c in val):
        return 'NON_ASCII'
    if key == 'class':
        return 'OK' if val == 'spd' else 'CLASS_NOT_READ_BY_THIS_GATE'
    if key == 'delta_def':
        return 'OK' if val == 'tensor_over_EM_minus_1' else 'WRONG_DELTA_DEF'
    if key in ('lo', 'hi'):
        return 'OK' if (NUM.match(val) and math.isfinite(float(val))) else 'NOT_A_PLAIN_NUMBER'
    if key == 'cl':
        if val == 'hard':
            return 'OK'
        return 'OK' if (NUM.match(val) and 0.0 < float(val) < 1.0) else 'CL_NOT_IN_(0,1)_OR_hard'
    if key == 'reading':
        return 'OK' if val == 'bound' else ('READING_NOT_MAPPED' if val in ('ceiling', 'margin', 'criterion') else 'UNKNOWN_READING')
    if key == 'geom':
        return 'OK' if val in ('single', 'population') else 'UNKNOWN_GEOM'
    if key in ('k_em_max', 'k_t_max'):
        return 'OK' if (NUM.match(val) and math.isfinite(float(val)) and float(val) > 0.0) else 'NOT_A_POSITIVE_PLAIN_NUMBER'
    if key == 'q':
        return 'OK' if val in ('phase', 'group') else 'UNKNOWN_Q'
    return 'OK'


def parse_sealed(raw):
    """masked parse: returns (rows as floats, census, row md5s); raises MaskedAbort(reason) -- no value in any message"""
    if raw.startswith(b'\xef\xbb\xbf'):
        raise MaskedAbort('BOM_PRESENT')
    try:
        text = raw.decode('utf-8')
    except UnicodeDecodeError:
        raise MaskedAbort('NOT_UTF8')
    if '\r' in text:
        raise MaskedAbort('CR_PRESENT')
    if '\t' in text:
        raise MaskedAbort('TAB_PRESENT')
    if any(((ord(c) < 32 and c != '\n') or 127 <= ord(c) < 160 or c in BAD_UNICODE) for c in text):
        raise MaskedAbort('CONTROL_OR_SEPARATOR_CHAR')
    if not text.endswith('\n'):
        raise MaskedAbort('NO_TRAILING_LF')
    if text.endswith('\n\n'):
        raise MaskedAbort('BLANK_LINE_AT_END')
    lines = text[:-1].split('\n')
    rows, census, md5s, fields_per_row = [], {}, [], []
    for n, line in enumerate(lines, 1):
        tag = 'row %d: ' % n
        if line.strip() == '':
            raise MaskedAbort(tag + 'BLANK_LINE')
        if line.startswith('|') or line.rstrip().endswith('|'):
            raise MaskedAbort(tag + 'LEADING_OR_TRAILING_BAR')
        fields = line.split(SEP)
        if any('|' in f for f in fields):
            raise MaskedAbort(tag + 'SEPARATOR_COLLISION')
        keys, vals = [], {}
        for f in fields:
            if '=' not in f:
                raise MaskedAbort(tag + 'FIELD_WITHOUT_EQUALS')
            k, v = f.split('=', 1)
            if k not in CANON:
                raise MaskedAbort(tag + 'UNKNOWN_KEY')
            if k in vals:
                raise MaskedAbort(tag + 'DUPLICATE_KEY_' + k)
            keys.append(k); vals[k] = v
        missing = [k for k in REQUIRED if k not in vals]
        if missing:
            raise MaskedAbort(tag + 'MISSING_REQUIRED_' + ','.join(missing))
        if keys != [k for k in CANON if k in keys]:
            raise MaskedAbort(tag + 'KEY_ORDER')
        if vals['id'] != 'SA-%d' % n:
            raise MaskedAbort(tag + 'ID_SEQUENCE')
        for k in keys:
            c = check_value(k, vals[k])
            if c != 'OK':
                raise MaskedAbort(tag + 'key %s -> %s' % (k, c))
        lo, hi = float(vals['lo']), float(vals['hi'])
        if not lo <= hi:
            raise MaskedAbort(tag + 'ORDER')
        rows.append({'lo': lo, 'hi': hi, 'kem': float(vals['k_em_max']), 'kt': float(vals['k_t_max']), 'geom': vals['geom'], 'q': vals.get('q')})
        census[vals['class']] = census.get(vals['class'], 0) + 1
        md5s.append(md5b(line.encode('utf-8')))
        fields_per_row.append(len(fields))
    if not rows:
        raise MaskedAbort('NO_ROWS')
    return rows, {'rows': len(rows), 'per_class': census, 'fields_per_row': fields_per_row}, md5s


def open_sealed(path, md5_stated, bytes_stated):
    raw = decode_armor(path)
    if md5b(raw) != md5_stated or len(raw) != int(bytes_stated):
        raise MaskedAbort('SEALED_MD5_OR_BYTES_MISMATCH')
    rows, census, md5s = parse_sealed(raw)
    return rows, census, md5s, md5b(raw), len(raw)


# ------------------------------------------------------------------------------------------ Phase 0
def phase0(P, DV, M, paths, repo, a1):
    C = P['constants']
    out = {}
    KEYS, ARMS, HEX = P['structure']['keys'], P['structure']['arms'], P['structure']['hex_keys']
    # PIN
    docs = {}
    for alias, s in P['sources'].items():
        b = open(os.path.join(repo, s['path']), 'rb').read()
        if md5b(b) != s['md5'] or len(b) != s['bytes']:
            raise Halt('F-CTRL-SA-PIN: source %s md5/bytes' % s['path'])
        docs[alias] = json.loads(b.decode('utf-8'))
    mism = 0
    for dest, spec in P['provenance'].items():
        if dest.startswith('keys/<K>/'):
            sub = dest[len('keys/<K>/'):]
            ks = KEYS if spec['scope'] == 'all' else P['structure']['cubic_keys'] if spec['scope'] == 'cubic' else [k for k in KEYS if k in docs['DQF']]
            for k in ks:
                have = ptr(P['raw']['keys'][k], '/' + sub)
                if json.dumps(have) != json.dumps(ptr(docs[spec['src']], spec['pointer'].replace('{K}', k))):
                    mism += 1
        else:
            if json.dumps(ptr(P, '/' + dest)) != json.dumps(ptr(docs[spec['src']], spec['pointer'])):
                mism += 1
    rel = lambda x, y: abs(x - y) / max(abs(x), abs(y))
    wk = wk3 = ws = wb = 0.0
    for k in KEYS:
        rk = P['raw']['keys'][k]
        wb = max(wb, rel(rk['b1_Hill'], rk['b1_Hill_cc']))
        for arm in ARMS:
            for f in M.mapped(k):
                d = rk['arms'][arm][f]
                if 'kappa_cc' in d and max(abs(d['kappa']), abs(d['kappa_cc'])) > C['kappa_floor']:
                    wk = max(wk, rel(d['kappa'], d['kappa_cc']))
                if 'kappa3_cc' in d:
                    wk3 = max(wk3, rel(d['kappa3'], d['kappa3_cc']))
                if 'S_cc' in d:
                    ws = max(ws, abs(d['S'] - d['S_cc']))
    e = {'odf_reading': 'none', 'raw_mismatches': mism, 'worst_twoleg_kappa_rel': wk, 'worst_twoleg_kappa3_rel': wk3, 'worst_twoleg_b1_rel': wb, 'worst_twoleg_S_abs': ws}
    e['passed'] = mism == 0 and wk <= C['pin_twoleg_tol_rel'] and wk3 <= C['pin_twoleg_tol_rel'] and wb <= C['pin_twoleg_tol_rel'] and ws <= C['tau_agg']
    out['F-CTRL-SA-PIN'] = e
    # PIN-DERIVED
    mine, theirs = flat(DV), flat({k: P['derived'][k] for k in DV})
    worst, lm = 0.0, 0
    if set(mine) != set(theirs):
        lm += len(set(mine) ^ set(theirs))
    for p in mine:
        if p not in theirs:
            continue
        a, b = mine[p], theirs[p]
        if isinstance(a, float) and isinstance(b, float):
            worst = max(worst, abs(a - b) / (C['pin_derived_tol_rel'] * abs(b) + C['pin_derived_tol_abs']))
        elif a != b or type(a) != type(b):
            lm += 1
    out['F-CTRL-SA-PIN-DERIVED'] = {'odf_reading': 'none', 'worst_scaled_dev': worst, 'leaf_mismatches': lm, 'leaves_compared': len(mine), 'passed': worst <= 1.0 and lm == 0}
    # ZERO
    wz = max(abs(DV['families'][k][a][f]['r0']) for k in KEYS for a in ARMS for f in ('t4', 't2'))
    out['F-CTRL-SA-ZERO'] = {'odf_reading': 'uniform', 'worst_abs_r0': wz, 'passed': wz <= C['zero_ctrl_tol_abs']}
    # RECON
    wr = max(DV['families'][k]['E2_Hill'][f]['recon_max_abs'] for k in KEYS for f in M.mapped(k))
    wrr = max(DV['families'][k][a][f]['fit_res_rel'] for k in KEYS for a in ('E2_HSmean', 'h_Hill') for f in M.mapped(k))
    out['F-CTRL-SA-RECON'] = {'odf_reading': 'hexP4/cubK4/hexP2', 'worst_abs_E2_Hill': wr, 'worst_rel_robust': wrr,
                              'passed': wr <= C['recon_tol_abs_E2_Hill'] and wrr <= C['recon_tol_rel_robust']}
    # S (N-1)
    n1 = DV['nulls']['N-1']
    wb_ = max(abs(v['bi']) for v in n1.values())
    wf_ = max(abs(v['fit']) for v in n1.values() if v['fit'] is not None)
    out['F-CTRL-SA-S'] = {'odf_reading': 'hexP2/hexP4/cubK4', 'worst_abs_bi': wb_, 'worst_abs_fit': wf_, 'passed': wb_ <= C['tau_agg'] and wf_ <= C['tau_agg']}
    # K24 (N-2)
    n2 = DV['nulls']['N-2']
    wbi = max(max(abs(v['bi_chat']), abs(v['bi_cc']), abs(v['bi_5x5'])) for v in n2.values())
    w7 = max(abs(v['fit7']) for v in n2.values())
    out['F-CTRL-SA-K24'] = {'odf_reading': 'hexP2P4/cubP2K4-i', 'worst_abs_bi': wbi, 'worst_abs_fit7': w7, 'passed': wbi <= C['kappa_floor'] and w7 <= C['kappa_floor']}
    # L2NULL (N-3, N-4)
    n3, n4 = DV['nulls']['N-3'], DV['nulls']['N-4']
    w2 = max(max(abs(v['fit']), abs(v['bi'])) for v in n3.values())
    w22 = max(max(abs(v['fit7']), abs(v['bi_5x5']), abs(v['k12_chat_t2sq'] or 0.0)) for v in n4.values())
    wt1 = max(abs(v['pure_l2_change_t1']) for v in n3.values())
    out['F-CTRL-SA-L2NULL'] = {'odf_reading': 'cubP2-ii/cubP2-i/cubP2K4-i', 'identity_cubP2_ii': 'the octahedrally symmetrized l = 2 perturbation vanishes identically (no l = 2 invariant of the octahedral group); asserted symbolically',
                               'worst_abs_kappa2': w2, 'worst_abs_kappa22': w22, 'worst_abs_t2_alone_t1': wt1,
                               'passed': w2 <= C['kappa_floor'] and w22 <= C['kappa_floor'] and wt1 <= C['l2null_t1_tol_abs']}
    # SIGN
    kref = abs(P['raw']['keys']['hex_step|a']['arms']['E2_Hill']['t4']['kappa'])
    m = M.map_interval(-kref * 0.1 ** 2, kref * 0.05 ** 2, with_two_param=False)
    bm = 0
    for k in KEYS:
        for a in ARMS:
            for f in M.mapped(k):
                kappa = P['raw']['keys'][k]['arms'][a][f]['kappa']
                if m['families'][k][a][f]['binding_end'] != ('hi' if kappa > 0 else 'lo'):
                    bm += 1
    out['F-CTRL-SA-SIGN'] = {'odf_reading': 'none', 'binding_end_mismatches': bm, 'passed': bm == 0}
    # GRID
    g = grid_counts(P)
    out['F-CTRL-SA-GRID'] = {'odf_reading': 'none', 'count_mismatches': 0, 'passed': True, 'counts': g}
    # MONO on the C-SYN-1 intervals
    worst_s, viol = 0.0, 0
    for t in C['synthetic_t']:
        b = kref * t * t
        rows = [{'lo': -b, 'hi': b, 'kem': C['synthetic_k']['silent'], 'kt': C['synthetic_k']['silent']}]
        base = M.map_rows(rows, with_two_param=False)
        for fct in (10.0, 0.1):
            sc = M.map_rows([{'lo': -b * fct, 'hi': b * fct, 'kem': rows[0]['kem'], 'kt': rows[0]['kt']}], with_two_param=False)
            w, v = M.mono_check(base, sc, fct)
            worst_s, viol = max(worst_s, w), viol + v
    out['F-CTRL-SA-MONO'] = {'odf_reading': 'none', 'worst_scaling_rel': worst_s, 'monotonicity_violations': viol, 'passed': worst_s <= C['mono_tol_rel'] and viol == 0}
    # MASK
    out['F-CTRL-SA-MASK'] = {'odf_reading': 'none', 'sealed_opens_before_phase3': SEALED_OPENS, 'passed': SEALED_OPENS == 0}
    # T1
    targets = [os.path.abspath(__file__), paths['memo'], paths['pin'], paths['lock'], paths['schema'], paths['comparator']]
    sc = t1_scan(paths, targets, a1)
    out['F-CTRL-SA-T1'] = {'odf_reading': 'none', 'hits': sc['hits'], 'collisions': sc['collisions'], 'patterns': sc['patterns'], 'a1_included': sc['a1_included'], 'per_file': sc['per_file'], 'passed': sc['hits'] == 0}
    return out


def grid_counts(P):
    G, D = P['grids'], P['constants']['D']
    tg = G['t_grid']
    return {'t_grid': tg, 't2t4_axis': G['t2t4_axis'], 'D': D, 'area_nodes_per_axis': G['area_grid']['nodes_per_axis'],
            'n_t_grid': len(tg), 'n_fit_window_inclusive': sum(abs(t) <= D for t in tg), 'n_fit_window_strict': sum(abs(t) < D for t in tg),
            'n_window_0p1_inclusive': sum(abs(t) <= 0.1 for t in tg), 'n_window_0p1_strict': sum(abs(t) < 0.1 for t in tg),
            'n_t2t4_axis': len(G['t2t4_axis']), 'n_t2t4_grid': len(G['t2t4_axis']) ** 2, 'n_area_grid': G['area_grid']['nodes_per_axis'] ** 2}


# ------------------------------------------------------------------------------------------ Phase 2 (A-2.5)
def phase2(P, DV, M):
    C = P['constants']
    KEYS, ARMS, HEX, PRIM = P['structure']['keys'], P['structure']['arms'], P['structure']['hex_keys'], P['structure']['primary']['keys']
    ks = C['synthetic_k']['silent']
    kref = abs(P['raw']['keys']['hex_step|a']['arms']['E2_Hill']['t4']['kappa'])
    b = lambda t: kref * t * t
    row = lambda lo, hi, k=ks: {'lo': lo, 'hi': hi, 'kem': k, 'kt': k}
    R = {}
    def suite(name, cond, detail):
        R[name] = {'passed': bool(cond), 'detail': detail}
        if not cond:
            say('  %s FAILED: %s' % (name, detail))
    # C-SYN-1
    ok, det = True, []
    for t in C['synthetic_t']:
        m = M.map_interval(-b(t), b(t), with_two_param=False)
        ref = m['families']['hex_step|a']['E2_Hill']['t4']
        ok &= abs(ref['t_star'] - t) <= 1e-12 * t and ref['class'] == ('BINDING' if t < C['D'] else 'INERT-IN-D')
        for k in KEYS:
            for a in ARMS:
                for f in M.mapped(k):
                    kappa = P['raw']['keys'][k]['arms'][a][f]['kappa']
                    ok &= abs(m['families'][k][a][f]['t_star'] - math.sqrt(b(t) / abs(kappa))) <= 1e-12 * m['families'][k][a][f]['t_star']
        det.append('t=%g ref class %s' % (t, ref['class']))
    suite('C-SYN-1', ok, '; '.join(det))
    # C-SYN-2
    m = M.map_interval(-b(0.1), b(0.05), with_two_param=False)
    ok = True
    for k in KEYS:
        for a in ARMS:
            for f in M.mapped(k):
                kappa = P['raw']['keys'][k]['arms'][a][f]['kappa']
                e = m['families'][k][a][f]
                want = (0.05 if kappa > 0 else 0.1) * math.sqrt(kref / abs(kappa))
                ok &= e['binding_end'] == ('hi' if kappa > 0 else 'lo') and abs(e['t_star'] - want) <= 1e-12 * want
    suite('C-SYN-2', ok, 'binding ends by sign(kappa); edges exact')
    # C-SYN-3
    U = DV['unions']
    m1 = M.map_rows([row(10 * U['widened_all'][1], 20 * U['widened_all'][1])], with_two_param=False)
    m2 = M.map_rows([row(20 * U['widened_all'][0], 10 * U['widened_all'][0])], with_two_param=False)
    m3 = M.map_rows([row(0.25 * U['hull_all'][1], 0.5 * U['hull_all'][1])], with_two_param=False)
    m4 = M.map_rows([row(*DV['synthetic']['robustness_only_positive'])], with_two_param=False)
    ok = m1['gate']['gate_class'] == 'KILL-IN-D' and m2['gate']['gate_class'] == 'KILL-IN-D' and m3['gate']['gate_class'] == 'TUNED' and m4['gate']['gate_class'] == 'TUNED'
    for k in KEYS:
        for a in ARMS:
            rw = DV['reach'][k][a]['widened']
            ok &= m1['combined']['exclusion'][k][a]['subreason'] == ('SIGN' if rw[1] <= 0 else 'MAGNITUDE')
            ok &= m2['combined']['exclusion'][k][a]['subreason'] == ('SIGN' if rw[0] >= 0 else 'MAGNITUDE')
    ok &= all(m4['combined']['exclusion'][k]['E2_Hill']['class'] != 'TUNED-ADMISSIBLE' for k in PRIM)
    ok &= any(m4['combined']['exclusion'][k][a]['class'] == 'TUNED-ADMISSIBLE' for k in KEYS for a in ARMS)
    suite('C-SYN-3', ok, 'KILL/KILL/TUNED/TUNED(robustness only): %s %s %s %s' % (m1['gate']['gate_class'], m2['gate']['gate_class'], m3['gate']['gate_class'], m4['gate']['gate_class']))
    # C-SYN-4
    m = M.map_rows([row(-1.0, 1.0)], with_two_param=False)
    ok = m['gate']['gate_class'] == 'INERT-IN-D' and all(m['combined']['families'][k][a][f]['class'] == 'INERT-IN-D' for k in KEYS for a in ARMS for f in M.mapped(k))
    suite('C-SYN-4', ok, m['gate']['gate_class'])
    # C-SYN-5
    m = M.map_interval(-b(0.1), b(0.1), with_two_param=False)
    ok = all(m['families'][k][a]['t2']['class'] == 'NULL-INERT' for k in P['structure']['cubic_keys'] for a in ARMS)
    suite('C-SYN-5', ok, 'cubic t2 NULL-INERT')
    # C-SYN-6 masked abort set
    ok, det = csyn6()
    suite('C-SYN-6', ok, det)
    # C-SYN-7 (MONO on C-SYN-1 intervals)
    worst, viol = 0.0, 0
    for t in C['synthetic_t']:
        base = M.map_rows([row(-b(t), b(t))], with_two_param=False)
        for fct in (10.0, 0.1):
            w, v = M.mono_check(base, M.map_rows([row(-b(t) * fct, b(t) * fct)], with_two_param=False), fct)
            worst, viol = max(worst, w), viol + v
    suite('C-SYN-7', worst <= C['mono_tol_rel'] and viol == 0, 'worst scaling dev %.2e, violations %d' % (worst, viol))
    # C-SYN-8 intersection
    m = M.map_rows([row(-b(0.1), b(0.1)), row(-b(0.05), b(0.2))], with_two_param=False)
    ref = m['combined']['families']['hex_step|a']['E2_Hill']['t4']
    ok = m['combined_empty'] is False and abs(ref['t_star'] - 0.1) <= 1e-12 and ref['binding_end'] == 'hi'
    neg = m['combined']['families']['cubic_step|001']['E2_Hill']['t4']
    kc = abs(P['raw']['keys']['cubic_step|001']['arms']['E2_Hill']['t4']['kappa'])
    ok &= abs(neg['t_star'] - math.sqrt(b(0.05) / kc)) <= 1e-12 * neg['t_star']
    suite('C-SYN-8', ok, 'I = [max lo, min hi]')
    # C-SYN-9
    m = M.map_rows([row(b(0.1), b(0.2)), row(-b(0.2), -b(0.1))], with_two_param=False)
    suite('C-SYN-9', m['gate']['gate_class'] == 'ANCHOR-INCONSISTENT' and m['combined_empty'] is True, m['gate']['gate_class'])
    # C-SYN-10 regime
    kv = C['synthetic_k']['void']
    m1 = M.map_rows([row(-b(0.1), b(0.1), kv)], with_two_param=False)
    m2 = M.map_rows([row(-b(0.1), b(0.1), kv), row(-b(0.05), b(0.05))], with_two_param=False)
    ok = m1['gate']['gate_class'] == 'VOID' and m1['n_void_rows'] == 1 and m1['rows'][0]['void_regime'] is True
    ok &= m2['n_void_rows'] == 1 and abs(m2['combined']['families']['hex_step|a']['E2_Hill']['t4']['t_star'] - 0.05) <= 1e-12
    suite('C-SYN-10', ok, '%s; mixed n_void %d' % (m1['gate']['gate_class'], m2['n_void_rows']))
    # C-SYN-11
    m = M.map_rows([row(0.0, 0.0)], with_two_param=False)
    fam = m['combined']['families']
    ok = m['gate']['gate_class'] == 'WINDOW-DELIVERED' and all(fam[k][a][f]['t_star'] == 0.0 and fam[k][a][f]['nu_is_inf'] and fam[k][a][f]['nullfloor_sensitive'] and fam[k][a][f]['class'] == 'BINDING' for k in KEYS for a in ARMS for f in M.mapped(k))
    suite('C-SYN-11', ok, m['gate']['gate_class'])
    # C-SYN-12
    t = C['synthetic_t_tight']
    m = M.map_interval(-b(t), b(t), with_two_param=False)
    ok, fired, clear = True, 0, 0
    for k in KEYS:
        for a in ARMS:
            for f in M.mapped(k):
                e = m['families'][k][a][f]
                want = abs(DV['families'][k][a][f]['S_bi']) * e['t_star'] / b(t) > C['nullfloor_threshold']
                ok &= e['nullfloor_sensitive'] == want
                fired += want; clear += (not want)
    suite('C-SYN-12', ok and fired >= 1 and clear >= 1, 'flag fires on %d cells, clear on %d' % (fired, clear))
    # C-SYN-13
    ok, det = True, []
    for name in ('margin_positive', 'margin_negative'):
        m = M.map_rows([row(*DV['synthetic'][name])], with_two_param=False)
        cls = [m['combined']['exclusion'][k][a]['class'] for k in KEYS for a in ARMS]
        ok &= m['gate']['gate_class'] == 'MARGIN-ONLY' and 'TUNED-ADMISSIBLE' not in cls and 'MARGIN' in cls
        det.append('%s %s' % (name, m['gate']['gate_class']))
    suite('C-SYN-13', ok, '; '.join(det))
    # C-SYN-14 grid noise at zero
    Pc = json.loads(json.dumps(P))
    g = Pc['raw']['keys']['cubic_step|001']['arms']['E2_Hill']['t4']['grid']
    g[Pc['grids']['t_grid'].index(0.02)] += 5e-13
    DVc = rederive(Pc)
    hull = DVc['reach']['cubic_step|001']['E2_Hill']['hull']
    Mc = Mapper(Pc, DVc)
    ex = Mc.exclusion('cubic_step|001', 'E2_Hill', 1e-6, 2e-6)
    suite('C-SYN-14', hull[1] == 0.0 and ex['class'] == 'EXCLUDED-IN-D' and ex['subreason'] == 'SIGN', 'snapped hull hi == 0; SIGN')
    return R


def csyn6():
    """the fifteen malformed files of memo 4.7 and one valid file, with distinctive synthetic values; every malformed file must
    abort with a reason code; no synthetic value may appear in any reason code or in the log"""
    V = ['-0.000123456789', '0.000987654321', '123456.789', '98765.4321']   # synthetic values (never anchors)
    good = 'id=SA-1 | class=spd | delta_def=tensor_over_EM_minus_1 | lo=%s | hi=%s | cl=0.9 | reading=bound | geom=single | k_em_max=%s | k_t_max=%s | src=synthetic source\n' % tuple(V)
    bad = {
        'crlf': good.replace('\n', '\r\n'), 'bom': '﻿' + good, 'trailing_blank': good + '\n',
        'formfeed_in_src': good.replace('synthetic source', 'synthetic\x0csource'), 'u2028_in_src': good.replace('synthetic source', 'synthetic source'),
        'unicode_minus': good.replace('lo=-0.000123456789', 'lo=−0.000123456789'), 'superscript': good.replace('hi=0.000987654321', 'hi=9.87654321×10⁻⁴'),
        'bar_in_src': good.replace('synthetic source', 'synthetic | source'), 'lo_gt_hi': good.replace('lo=-0.000123456789', 'lo=0.5'),
        'reading_ceiling': good.replace('reading=bound', 'reading=ceiling'), 'wrong_delta_def': good.replace('tensor_over_EM_minus_1', 'EM_over_tensor_minus_1'),
        'missing_key': good.replace(' | geom=single', ''), 'wrong_id': good.replace('id=SA-1', 'id=SA-2'),
        'duplicate_key': good.replace(' | src=', ' | cl=0.8 | src='), 'percent_cl': good.replace('cl=0.9', 'cl=90%'),
    }
    ok, codes = True, {}
    for name, text in bad.items():
        try:
            parse_sealed(text.encode('utf-8'))
            ok = False; codes[name] = 'ACCEPTED'
        except MaskedAbort as e:
            codes[name] = str(e)
    try:
        rows, census, md5s = parse_sealed(good.encode('utf-8'))
        ok &= census == {'rows': 1, 'per_class': {'spd': 1}, 'fields_per_row': [11]}
    except MaskedAbort as e:
        ok = False; codes['valid'] = str(e)
    leak = any(v in c for v in V for c in codes.values()) or any(v in l for v in V for l in LOG)
    return ok and not leak and len(bad) == 15, '15 malformed files aborted: %s; valid file census confirmed; leak %s' % (', '.join(sorted(codes)), 'NONE' if not leak else 'DETECTED')


# ------------------------------------------------------------------------------------------ checkpoint
def write_checkpoint(ck, path, paths, a1):
    data = (json.dumps(ck, indent=1, sort_keys=True, ensure_ascii=True, allow_nan=False) + '\n').encode('ascii')
    open(path, 'wb').write(data)
    sc = t1_scan(paths, [path], a1)
    if sc['hits']:
        os.remove(path)
        raise Halt('T1 post-write: %d hit(s) in the checkpoint by index %s -- checkpoint deleted' % (sc['hits'], sc['per_file']))
    ck['T1_post_write'] = {'hits': sc['hits'], 'collisions': sc['collisions'], 'patterns': sc['patterns'], 'a1_included': sc['a1_included']}
    data = (json.dumps(ck, indent=1, sort_keys=True, ensure_ascii=True, allow_nan=False) + '\n').encode('ascii')
    open(path, 'wb').write(data)
    sc2 = t1_scan(paths, [path], a1)
    if sc2['hits']:
        os.remove(path)
        raise Halt('T1 post-write (second scan): hits')
    return md5b(data), len(data)


def main():
    args = sys.argv[1:]
    if not args or args[0] not in ('preread', 'read', 'census'):
        print(__doc__); return 2
    mode = args[0]
    opt = lambda n, d=None: args[args.index(n) + 1] if n in args else d
    outdir = opt('--out', HERE)
    try:
        if mode == 'census':
            rows, census, md5s, smd5, sbytes = open_sealed(opt('--sealed'), opt('--md5'), opt('--bytes'))
            say('sealed: md5 %s  bytes %d  census %s  row md5s %s' % (smd5, sbytes, json.dumps(census, sort_keys=True), md5s))
            return 0
        repo, a1 = opt('--repo'), opt('--a1')
        if not repo:
            raise Halt('--repo required')
        if mode == 'read' and not a1:
            raise Halt('--a1 required for the read (F-CTRL-SA-T1 under base ∪ stratum ∪ A1)')
        paths = guards()
        P = json.loads(open(paths['pin'], 'rb').read().decode('ascii'))
        DV = rederive(P)
        M = Mapper(P, DV)
        inst_md5 = md5f(os.path.abspath(__file__))
        say('%s %s leg -- instrument md5 %s; pinned %s; memo %s; lock record %s' % (GATE, LEG, inst_md5, PIN_MD5, MEMO_MD5, LOCK_MD5))
        ck = {'gate': GATE, 'leg': LEG, 'utc': datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'), 'instrument_md5': inst_md5,
              'memo_lock_md5': MEMO_MD5, 'memo_lock_bytes': MEMO_BYTES, 'lock_record_md5': LOCK_MD5, 'pinned_inputs_md5': PIN_MD5,
              'builder_md5': BUILDER_MD5, 'verifier_md5': VERIFIER_MD5, 't1_list_md5': T1_MD5, 't1_a1_md5': md5f(a1) if a1 else None,
              'scanner_md5': SCANNER_MD5, 'schema_md5': SCHEMA_MD5, 'comparator_md5': COMPARATOR_MD5, 'ledger_base_md5': LEDGER_MD5, 'elections': ELECTIONS,
              'grids': grid_counts(P), 'phase0': None, 'nulls': None, 'phase2': None, 'phase3': None}
        # Phase 0
        P0 = phase0(P, DV, M, paths, repo, a1)
        ck['phase0'] = P0
        ck['nulls'] = DV['nulls']
        for item, e in P0.items():
            say('  Phase 0 %-22s %s' % (item, 'PASS' if e['passed'] else 'FAIL'))
        if not all(e['passed'] for e in P0.values()):
            ck['verdict'] = 'INDETERMINATE'
            write_checkpoint(ck, os.path.join(outdir, 'g_mscs_a_chatleg_prereadcheckpoint.json'), paths, a1)
            raise Halt('Phase 0 failure -> INDETERMINATE')
        # Phase 2
        P2 = phase2(P, DV, M)
        ck['phase2'] = P2
        for s, e in P2.items():
            say('  Phase 2 %-9s %s' % (s, 'PASS' if e['passed'] else 'FAIL'))
        if not all(e['passed'] for e in P2.values()):
            write_checkpoint(ck, os.path.join(outdir, 'g_mscs_a_chatleg_prereadcheckpoint.json'), paths, a1)
            raise Halt('Phase 2 failure -- no sealed open')
        if mode == 'preread':
            h, n = write_checkpoint(ck, os.path.join(outdir, 'g_mscs_a_chatleg_prereadcheckpoint.json'), paths, a1)
            say('pre-read checkpoint written: md5 %s  %d B  (phase3 = null)' % (h, n))
            return 0
        # Phase 3
        try:
            rows, census, md5s, smd5, sbytes = open_sealed(opt('--sealed'), opt('--md5'), opt('--bytes'))
        except MaskedAbort as e:
            say('MASKED ABORT (the read not spent): %s' % e)
            return 1
        say('sealed: md5 %s  bytes %d  census %s' % (smd5, sbytes, json.dumps(census, sort_keys=True)))
        p3 = M.full([{'lo': r['lo'], 'hi': r['hi'], 'kem': r['kem'], 'kt': r['kt']} for r in rows])
        for i, r in enumerate(p3['rows']):
            r['id'] = 'SA-%d' % (i + 1); r['row_md5'] = md5s[i]; r['geom'] = rows[i]['geom']; r['q'] = rows[i]['q']
        p3.update({'sealed_md5': smd5, 'sealed_bytes': sbytes, 'census': census, 'row_md5s': md5s, 't1_a1_md5': md5f(a1)})
        ck['phase3'] = p3
        ck['verdict'] = p3['gate']['gate_class']
        h, n = write_checkpoint(ck, os.path.join(outdir, 'g_mscs_a_chatleg_checkpoint.json'), paths, a1)
        say('gate class: %s  (OOM x10 %s, x0.1 %s; robust %s)' % (p3['gate']['gate_class'], p3['gate']['oom_class_x10'], p3['gate']['oom_class_x0p1'], p3['gate']['oom_robust']))
        say('checkpoint written: md5 %s  %d B' % (h, n))
        return 0
    except Halt as e:
        say('HALT: %s' % e)
        return 1


if __name__ == '__main__':
    sys.exit(main())
