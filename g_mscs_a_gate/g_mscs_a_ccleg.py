#!/usr/bin/env python3
"""g_mscs_a_ccleg.py -- Gate G-MSCS-A, the CC-leg instrument (built blind: from the locked memo sections 1, 3-6, the
lock record's Addendum A-2, the frozen schema and the pinned-inputs file only; its own parser, binder and class logic;
the chat mapper stayed quarantined while this was written).

Standard library only. Every invocation: md5 + byte guards on the memo, the pinned file, the lock record, the gate T1
list, the base list, T1-A1, the scanner, the schema and the comparator; a T1 scan of this file, the memo, the pinned
file, the lock record, the schema and the comparator under the gate list plus A1 (halt on any hit, no override); then
Phase 0 (twelve controls, halt-on-fail) and Phase 2 (fourteen synthetic suites) from scratch. `preread` stops there and
writes g_mscs_a_ccleg_prereadcheckpoint.json (phase3 = null). `read` goes on to Phase 3: the armored sealed file is
decoded only then, parsed masked, mapped, OOM-scaled, and g_mscs_a_ccleg_checkpoint.json is written and T1-scanned
after writing (deleted on a hit). No value of the sealed file (lo, hi, k_em_max, k_t_max, cl, src, note) is ever printed,
logged or serialized -- only its md5, byte count, census, row md5s and the derived classes, flags and edges.

Usage:  python3 g_mscs_a_ccleg.py preread [--inputs DIR] [--flag TEXT]
        python3 g_mscs_a_ccleg.py read    [--inputs DIR] [--flag TEXT]
Exit: 0 on a completed run; 1 on a halt (INDETERMINATE), a T1 hit or a masked abort; 2 on usage.
No point count is typed anywhere in this file: every count is computed from the pinned generators.
"""
import base64, hashlib, importlib.util, io, json, math, os, re, sys, tempfile, time, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
GATE, LEG, INSTRUMENT = 'G-MSCS-A', 'cc', os.path.basename(os.path.abspath(__file__))
LEDGER_BASE_MD5 = 'd4c42a53cbd6d325ebc740879288e844'
MEMO, PINNED, LOCK = 'staging_memo_G_MSCS_A_v2.md', 'pinned_inputs_G_MSCS_A.json', 'G_MSCS_A_LOCK_RECORD.md'
SCHEMA, COMPARATOR = 'g_mscs_a_schema_v1_0.json', 'g_mscs_a_compare_v1_0.py'
T1_LIST, T1_BASE, T1_A1, SCANNER = ('tools/t1/T1_forbidden_G_MSCS_A.txt', 'tools/t1/T1_base_author_20260919.txt',
                                    'tools/t1/t1_forbidden_G_MSCS_A_A1.txt', 'tools/t1/t1_scan.py')
GUARDS = {  # locked artifact -> (md5, bytes), from the lock record section 1 and the dispatch inventory
    MEMO: ('6ea16b952db835bb351d3dc1b474c6ed', 121950),
    PINNED: ('2d44ec01a66889f330d940dee3313bdc', 96761),
    LOCK: ('8116cc622279b5d4e73214178ae97cd8', 17923),
    T1_LIST: ('e274e58ea50b9ed347969e507d2a4f36', 1482),
    T1_BASE: ('05302210cc4ceb70553acbe8379e9fc3', 143),
    T1_A1: ('3b753b3a371a162fc2ab21b9eed51bd5', 1030),
    SCANNER: ('6b86290090a8c84f1b1a0a99ec0bf697', 1967),
    SCHEMA: ('5323e11fc27d688f61aaf57302c875c0', 9436),
    COMPARATOR: ('c5b4a7aab2fc8651be6d26d1f3d25642', 16850),
}
T1_SCANNED = [MEMO, PINNED, LOCK, SCHEMA, COMPARATOR]          # plus this file itself
SEALED_ARMOR = 'sealed/anchors_G_MSCS_A_SEALED.md.b64'
SEALED_MD5, SEALED_BYTES = 'cfd62dcf060427ac3402604e6c3284ff', 177   # the author's stated md5 and byte count (unarmored)
PREREAD_CK, READ_CK = 'g_mscs_a_ccleg_prereadcheckpoint.json', 'g_mscs_a_ccleg_checkpoint.json'
ELECTIONS = {'E-SA-0': 'a', 'E-SA-1': 'a', 'E-SA-2': 'a', 'E-SA-3': 'a', 'E-SA-4': 'a', 'E-SA-5': 'a', 'E-SA-6': 'a',
             'E-SA-7': '05302210+MSCS1stratum', 'E-SA-8': 'a', 'E-SA-9': 'a', 'E-SA-10': 'a', 'E-SA-11': 'a'}
FORBIDDEN_KEYS = {'lo', 'hi', 'k_em_max', 'k_t_max', 'src', 'note', 'cl'}
CLASS_PRECEDENCE = ['INDETERMINATE', 'VOID', 'ANCHOR-INCONSISTENT', 'KILL-IN-D', 'TUNED', 'MARGIN-ONLY',
                    'WINDOW-DELIVERED', 'INERT-IN-D']
PHASE0_ITEMS = ['F-CTRL-SA-PIN', 'F-CTRL-SA-PIN-DERIVED', 'F-CTRL-SA-ZERO', 'F-CTRL-SA-RECON', 'F-CTRL-SA-S',
                'F-CTRL-SA-K24', 'F-CTRL-SA-L2NULL', 'F-CTRL-SA-SIGN', 'F-CTRL-SA-GRID', 'F-CTRL-SA-MONO',
                'F-CTRL-SA-MASK', 'F-CTRL-SA-T1']
PHASE0_ODF = {'F-CTRL-SA-PIN': 'none', 'F-CTRL-SA-PIN-DERIVED': 'none', 'F-CTRL-SA-ZERO': 'uniform',
              'F-CTRL-SA-RECON': 'hexP4/cubK4/hexP2', 'F-CTRL-SA-S': 'hexP2/hexP4/cubK4',
              'F-CTRL-SA-K24': 'hexP2P4/cubP2K4-i', 'F-CTRL-SA-L2NULL': 'cubP2-ii/cubP2-i/cubP2K4-i',
              'F-CTRL-SA-SIGN': 'none', 'F-CTRL-SA-GRID': 'none', 'F-CTRL-SA-MONO': 'none', 'F-CTRL-SA-MASK': 'none',
              'F-CTRL-SA-T1': 'none'}
CUBP2_II_IDENTITY = ('cubP2-ii: the octahedrally symmetrized l=2 perturbation is identically zero (the octahedral group '
                     'has no l=2 invariant; for <001>, sum_i P2(e_i . z) = 0), so r_agg is unchanged by t2 at every '
                     'order -- asserted symbolically, no number')
# A-2.2 SIGN and A-2.5 C-SYN-2 / C-SYN-8 name two extra synthetic strengths beside constants.synthetic_t
SYN_T_ASYM_LO, SYN_T_ASYM_HI, SYN_T_OUTER = 0.1, 0.05, 0.2
# --------------------------------------------------------------------------------------------- run-time state
STATE = {'sealed_opens_before_phase3': 0, 'phase3_active': False, 'log': [], 'synthetic_secrets': []}


class Halt(Exception):
    pass


class MaskedAbort(Exception):
    """a sealed-file format failure: carries a reason code only, never a value"""


def log(msg=''):
    STATE['log'].append(msg)
    print(msg)
    sys.stdout.flush()


def md5b(b):
    return hashlib.md5(b).hexdigest()


def read(rel):
    return open(os.path.join(HERE, rel), 'rb').read()


def guard_all():
    seen = {}
    for rel, (want, nbytes) in GUARDS.items():
        b = read(rel)
        h = md5b(b)
        if h != want or len(b) != nbytes:
            raise Halt('GUARD %s: md5 %s bytes %d (expected %s, %d)' % (rel, h, len(b), want, nbytes))
        seen[rel] = h
    return seen


def load_scanner():
    spec = importlib.util.spec_from_file_location('t1_scan_frozen', os.path.join(HERE, SCANNER))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def t1_scan(scanner, pats, rels):
    """scan the named files under the pattern list with the frozen scanner's rule; hits by index only"""
    out, total_hits, total_coll = {}, 0, 0
    for rel in rels:
        text = read(rel).decode('utf-8', 'replace')
        hits, coll = scanner.scan_text(text, pats)
        out[rel] = {'hits': len(hits), 'hit_indices': sorted({i for i, _ in hits}), 'collisions': len(coll)}
        total_hits += len(hits)
        total_coll += len(coll)
    return out, total_hits, total_coll


def t1_scan_text(scanner, pats, text):
    hits, coll = scanner.scan_text(text, pats)
    return len(hits), len(coll)


# --------------------------------------------------------------------------------------------- pointers, leaves
def jptr(doc, ptr):
    """RFC 6901"""
    if ptr == '':
        return doc
    if not ptr.startswith('/'):
        raise Halt('pointer must start with /')
    cur = doc
    for tok in ptr[1:].split('/'):
        tok = tok.replace('~1', '/').replace('~0', '~')
        cur = cur[int(tok)] if isinstance(cur, list) else cur[tok]
    return cur


def leaves(node, path=''):
    if isinstance(node, dict):
        for k in sorted(node):
            yield from leaves(node[k], path + '/' + k)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from leaves(v, '%s/%d' % (path, i))
    else:
        yield path, node


def walk_keys(node):
    if isinstance(node, dict):
        for k, v in node.items():
            yield k
            yield from walk_keys(v)
    elif isinstance(node, list):
        for v in node:
            yield from walk_keys(v)


def isnum(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def rel_dev(a, b):
    m = max(abs(a), abs(b))
    return 0.0 if m == 0 else abs(a - b) / m


# --------------------------------------------------------------------------------------------- the pinned inputs
class Pinned:
    def __init__(self, P, S):
        self.P = P
        self.S = S
        st, c, g = P['structure'], P['constants'], P['grids']
        self.keys, self.hex, self.cubic = list(st['keys']), list(st['hex_keys']), list(st['cubic_keys'])
        self.arms = list(st['arms'])
        self.primary_arm, self.primary_keys = st['primary']['arm'], list(st['primary']['keys'])
        self.robust_arms = list(st['robustness']['arms'])
        self.mapped = {'hex': list(st['mapped_families']['hex']), 'cubic': list(st['mapped_families']['cubic'])}
        self.null_fams = {'cubic': list(st['null_families']['cubic'])}
        self.D, self.KD, self.mu = c['D'], c['KD_CLIP'], c['mu']
        self.floor, self.tau, self.snap = c['kappa_floor'], c['tau_agg'], c['zero_snap']
        self.trunc_thr, self.nf_thr = c['trunc_threshold'], c['nullfloor_threshold']
        self.pin_rel, self.pin_abs = c['pin_derived_tol_rel'], c['pin_derived_tol_abs']
        self.twoleg_rel, self.zero_tol = c['pin_twoleg_tol_rel'], c['zero_ctrl_tol_abs']
        self.recon_abs, self.recon_rel = c['recon_tol_abs_E2_Hill'], c['recon_tol_rel_robust']
        self.l2_t1_abs, self.mono_rel = c['l2null_t1_tol_abs'], c['mono_tol_rel']
        self.syn_t, self.syn_tight = list(c['synthetic_t']), c['synthetic_t_tight']
        self.band = list(c['synthetic_band_fractions'])
        self.k_silent, self.k_void = c['synthetic_k']['silent'], c['synthetic_k']['void']
        self.oom = list(c['oom_factors'])
        self.t_grid, self.axis = list(g['t_grid']), list(g['t2t4_axis'])
        self.rp1, self.rp2 = list(g['richardson_pairs']['one_param']), list(g['richardson_pairs']['two_param'])
        self.area_lo, self.area_hi, self.area_n = g['area_grid']['lo'], g['area_grid']['hi'], g['area_grid']['nodes_per_axis']
        self.d_EM = P['raw']['regime']['d_EM']
        self.raw = P['raw']['keys']
        # rms per family from the closed forms; asserted against constants.rms
        self.rms = {'hexP2': math.sqrt(1.0 / 5.0), 'hexP4': 1.0 / 3.0, 'cubK4': math.sqrt(4.0 / 21.0)}
        for k, v in self.rms.items():
            if c['rms'][k] != v:
                raise Halt('rms closed form %s differs from constants.rms' % k)
        # constants cross-checked against the frozen schema's tolerances
        T = S['tolerances']
        for a, b in (('D', 'D'), ('KD_CLIP', 'KD_CLIP'), ('kappa_floor', 'kappa_floor'), ('mu', 'mu'),
                     ('tau_agg', 'tau_agg'), ('trunc_threshold', 'trunc_threshold'),
                     ('nullfloor_threshold', 'nullfloor_threshold'), ('pin_derived_tol_rel', 'pin_derived_rel'),
                     ('pin_derived_tol_abs', 'pin_derived_abs'), ('pin_twoleg_tol_rel', 'pin_twoleg_rel'),
                     ('zero_ctrl_tol_abs', 'zero_ctrl_abs'), ('recon_tol_abs_E2_Hill', 'recon_abs_E2_Hill'),
                     ('recon_tol_rel_robust', 'recon_rel_robust'), ('l2null_t1_tol_abs', 'l2null_t1_abs'),
                     ('mono_tol_rel', 'mono_rel'), ('edge_twoleg_tol_rel', 'edge_twoleg_rel')):
            if c[a] != T[b]:
                raise Halt('constant %s differs between the pinned file and the schema' % a)
        if P['_meta']['gate'] != GATE or S['gate'] != GATE:
            raise Halt('gate label')
        if S['keys'] != self.keys or S['arms'] != self.arms or S['primary']['keys'] != self.primary_keys:
            raise Halt('structure differs between the pinned file and the schema')
        if S['elections'] != ELECTIONS or P['_meta']['elections_applied']['E-SA-7'] != 'base 05302210 + the G-MSCS1 stratum':
            raise Halt('elections')
        self.i0 = self.t_grid.index(0.0)
        self.n_axis = len(self.axis)

    def branch(self, K):
        return 'hex' if K in self.hex else 'cubic'

    def fam_list(self, K):
        """every family in the pinned layout for this key: mapped ones first, then the null family"""
        return self.mapped[self.branch(K)] + self.null_fams.get(self.branch(K), [])

    def is_mapped(self, K, F):
        return F in self.mapped[self.branch(K)]

    def odf(self, K, F):
        if F == 't2':
            return 'hexP2' if K in self.hex else 'cubP2-i'
        return 'hexP4' if K in self.hex else 'cubK4'

    def rms_of(self, K, F):
        return self.rms['hexP2'] if F == 't2' else (self.rms['hexP4'] if K in self.hex else self.rms['cubK4'])

    def cells(self):
        for K in self.keys:
            for A in self.arms:
                for F in self.mapped[self.branch(K)]:
                    yield K, A, F

    def idx5(self, i, j):
        return self.n_axis * i + j


# --------------------------------------------------------------------------------------------- the derivations
def rich_even(pin, r, h1, h2):
    tg = pin.t_grid

    def E(h):
        return (r[tg.index(h)] + r[tg.index(-h)] - 2.0 * r[pin.i0]) / (2.0 * h * h)
    return (4.0 * E(h1) - E(h2)) / 3.0


def rich_odd(pin, r, h1, h2):
    tg = pin.t_grid

    def O(h):
        return (r[tg.index(h)] - r[tg.index(-h)]) / (2.0 * h)
    return (4.0 * O(h1) - O(h2)) / 3.0


def grid5(pin, R, t2, t4):
    return R[pin.idx5(pin.axis.index(t2), pin.axis.index(t4))]


def rich_mixed(pin, R, h1, h2):
    def M(h):
        return (grid5(pin, R, h, h) - grid5(pin, R, h, -h) - grid5(pin, R, -h, h) + grid5(pin, R, -h, -h)) / (4.0 * h * h)
    return (4.0 * M(h1) - M(h2)) / 3.0


def rich_even_5x5(pin, R, along, h1, h2):
    """even part along one axis of the 5x5 grid, the other coordinate at 0"""
    def val(h):
        return grid5(pin, R, h, 0.0) if along == 't2' else grid5(pin, R, 0.0, h)

    def E(h):
        return (val(h) + val(-h) - 2.0 * val(0.0)) / (2.0 * h * h)
    return (4.0 * E(h1) - E(h2)) / 3.0


def derive_families(pin):
    out = {}
    h1, h2 = pin.rp1
    for K in pin.keys:
        out[K] = {}
        for A in pin.arms:
            out[K][A] = {}
            for F in pin.fam_list(K):
                d = pin.raw[K]['arms'][A][F]
                grid, kappa = d['grid'], d['kappa']
                mapped = pin.is_mapped(K, F)
                kbi = rich_even(pin, grid, h1, h2)
                rec = {'kappa': kappa, 'kappa_bi': kbi, 'S_bi': rich_odd(pin, grid, h1, h2), 'S_fit': d.get('S'),
                       'mapped': mapped, 'odf_reading': pin.odf(K, F), 'r0': grid[pin.i0],
                       'fit_res_rel': (abs(kappa - kbi) / abs(kbi)) if mapped else None}
                # the two-leg relatives are serialized on the mapped families and null on the null family (the pinned layout)
                if 'kappa_cc' in d:
                    rec['twoleg_rel'] = rel_dev(kappa, d['kappa_cc']) if mapped else None
                if 'kappa3_cc' in d:
                    rec['twoleg_kappa3_rel'] = rel_dev(d['kappa3'], d['kappa3_cc']) if mapped else None
                if 'S_cc' in d:
                    rec['twoleg_S_abs'] = abs(d['S'] - d['S_cc'])
                if A == pin.primary_arm and mapped:
                    S, k3 = d['S'], d['kappa3']
                    worst = 0.0
                    for t, r in zip(pin.t_grid, grid):
                        if abs(t) <= pin.D:
                            worst = max(worst, abs(r - (S * t + kappa * t * t + k3 * t * t * t)))
                    rec['recon_max_abs'] = worst
                    rec['trunc_T_at_D'] = abs(k3) * pin.D / abs(kappa)
                out[K][A][F] = rec
    return out


def snap0(pin, x):
    return 0.0 if abs(x) <= pin.snap else x


def build_reach(pin, fam, grids_override=None):
    """R^h and R^w per key and arm; grids_override lets a suite substitute one one-parameter grid"""
    out = {}
    D2 = pin.D * pin.D
    for K in pin.keys:
        out[K] = {}
        for A in pin.arms:
            lo_box = hi_box = 0.0
            vals = []
            for F in pin.mapped[pin.branch(K)]:
                kap = fam[K][A][F]['kappa']
                lo_box += min(0.0, kap * D2)
                hi_box += max(0.0, kap * D2)
                grid = pin.raw[K]['arms'][A][F]['grid']
                if grids_override and (K, A, F) in grids_override:
                    grid = grids_override[(K, A, F)]
                vals += [r for t, r in zip(pin.t_grid, grid) if abs(t) <= pin.D]
            if A == pin.primary_arm:
                vals += list(pin.raw[K]['quadform']['grid5x5_cc'])
            gmin, gmax = min(vals), max(vals)
            hull = [snap0(pin, min(lo_box, gmin)), snap0(pin, max(hi_box, gmax))]
            out[K][A] = {'box': [lo_box, hi_box], 'grid_min': gmin, 'grid_max': gmax,
                         'grid_exceeds_box': bool(gmin < lo_box or gmax > hi_box), 'hull': hull,
                         'widened': [(1.0 + pin.mu) * hull[0], (1.0 + pin.mu) * hull[1]]}
    return out


def build_unions(pin, reach):
    def union(cells, which):
        return [min(reach[K][A][which][0] for K, A in cells), max(reach[K][A][which][1] for K, A in cells)]
    all_cells = [(K, A) for K in pin.keys for A in pin.arms]
    prim = [(K, pin.primary_arm) for K in pin.primary_keys]
    return {'hull_all': union(all_cells, 'hull'), 'hull_primary': union(prim, 'hull'),
            'widened_all': union(all_cells, 'widened'), 'widened_primary': union(prim, 'widened')}


def build_synthetic(pin, U):
    f1, f2 = pin.band
    w, h = U['widened_all'][0], U['hull_all'][0]
    neg = [w + f1 * (h - w), w + f2 * (h - w)]
    h, w = U['hull_all'][1], U['widened_all'][1]
    pos = [h + f1 * (w - h), h + f2 * (w - h)]
    p, q = U['widened_primary'][1], U['hull_all'][1]
    rob = [p + f1 * (q - p), p + f2 * (q - p)]
    return {'margin_negative': neg, 'margin_positive': pos, 'robustness_only_positive': rob}


def build_nulls(pin, fam):
    h1, h2 = pin.rp2
    N1, N2, N3, N4 = {}, {}, {}, {}
    for K, A, F in pin.cells():
        N1['%s/%s/%s' % (K, A, F)] = {'bi': fam[K][A][F]['S_bi'], 'fit': fam[K][A][F]['S_fit'], 'odf_reading': pin.odf(K, F)}
    for K in pin.keys:
        q = pin.raw[K]['quadform']
        N2[K] = {'fit7': q['kappa24_fit7'], 'bi_chat': pin.raw[K]['kappa24_bi_chat'], 'bi_cc': pin.raw[K]['kappa24_bi_cc'],
                 'bi_5x5': rich_mixed(pin, q['grid5x5_cc'], h1, h2),
                 'odf_reading': 'hexP2P4' if K in pin.hex else 'cubP2K4-i'}
    for K in pin.cubic:
        q = pin.raw[K]['quadform']
        f = fam[K][pin.primary_arm]['t2']
        N3[K] = {'fit': f['kappa'], 'bi': f['kappa_bi'], 'odf_reading': 'cubP2-i', 'pure_l2_change_t1': pin.raw[K]['pure_l2_change_t1']}
        N4[K] = {'fit7': q['kappa22_fit7'], 'bi_5x5': rich_even_5x5(pin, q['grid5x5_cc'], 't2', h1, h2),
                 'k12_chat_t2sq': (q['basis_k12_chat'][0] if 'basis_k12_chat' in q else None), 'odf_reading': 'cubP2K4-i'}
    return {'N-1': N1, 'N-2': N2, 'N-3': N3, 'N-4': N4}


def build_hex_quadform(pin, fam):
    h1, h2 = pin.rp2
    out = {}
    for K in pin.hex:
        q = pin.raw[K]['quadform']
        R = q['grid5x5_cc']
        k22, k44, k24 = (rich_even_5x5(pin, R, 't2', h1, h2), rich_even_5x5(pin, R, 't4', h1, h2), rich_mixed(pin, R, h1, h2))
        k2 = fam[K][pin.primary_arm]['t2']['kappa']
        slopes = {}
        for A in [a for a in pin.arms if a != 'h_Hill']:
            slopes[A + '_fit'] = math.sqrt(-fam[K][A]['t2']['kappa'] / fam[K][A]['t4']['kappa'])
            slopes[A + '_bi'] = math.sqrt(-fam[K][A]['t2']['kappa_bi'] / fam[K][A]['t4']['kappa_bi'])
        slopes[pin.primary_arm + '_bi5x5'] = math.sqrt(-k22 / k44)
        hk2, hk4 = fam[K]['h_Hill']['t2']['kappa'], fam[K]['h_Hill']['t4']['kappa']
        form = 'negative-definite' if (hk2 < 0 and hk4 < 0) else ('positive-definite' if (hk2 > 0 and hk4 > 0) else 'indefinite')
        out[K] = {'k22_bi_5x5': k22, 'k24_bi_5x5': k24, 'k44_bi_5x5': k44,
                  'kappa22_fit7_vs_kappa2_rel': abs(q['kappa22_fit7'] - k2) / abs(q['kappa22_fit7']),
                  'null_ray_slope': slopes, 'h_Hill_form': form}
    return out


def build_zero_ctrl(pin):
    return {K: {'%s/%s' % (A, F): {'odf_reading': 'uniform', 'r0': pin.raw[K]['arms'][A][F]['grid'][pin.i0]}
                for A in pin.arms for F in pin.fam_list(K)} for K in pin.keys}


def rederive(pin):
    fam = derive_families(pin)
    reach = build_reach(pin, fam)
    unions = build_unions(pin, reach)
    return {'families': fam, 'reach': reach, 'unions': unions, 'synthetic': build_synthetic(pin, unions),
            'nulls': build_nulls(pin, fam), 'hex_quadform': build_hex_quadform(pin, fam), 'zero_ctrl': build_zero_ctrl(pin)}


def compare_leaves(mine, pinned, rel, absf):
    a, b = dict(leaves(mine)), dict(leaves(pinned))
    mism, worst, missing, extra = 0, 0.0, sorted(set(b) - set(a)), sorted(set(a) - set(b))
    for p in sorted(set(a) & set(b)):
        x, y = a[p], b[p]
        if isnum(x) and isnum(y):
            sc = abs(x - y) / (rel * abs(y) + absf)
            worst = max(worst, sc)
            if sc > 1.0:
                mism += 1
        elif x != y or type(x) != type(y):
            mism += 1
    return mism + len(missing) + len(extra), worst, missing, extra, len(a)


# --------------------------------------------------------------------------------------------- the mapping
class Mapper:
    def __init__(self, pin, fam, reach):
        self.pin, self.fam, self.reach = pin, fam, reach

    def family_record(self, K, A, F, lo, hi):
        pin, f = self.pin, self.fam[K][A][F]
        if not pin.is_mapped(K, F):
            return {'class': 'NULL-INERT', 't_star': None, 't_star_bi': None, 'class_bi': None, 'resolution_sensitive': None,
                    'sigma_star': None, 'window_lo': -pin.D, 'window_hi': pin.D, 'trunc_T': None, 'truncation_sensitive': None,
                    'nu': None, 'nu_is_inf': None, 'nullfloor_sensitive': None, 'binding_end': None}

        def edge(kappa):
            b = hi if kappa > 0 else lo
            if b == 0:
                return b, 0.0
            q = b / kappa
            if q < 0:
                raise Halt('instrument defect: b/kappa < 0 on an interval containing 0')
            return b, math.sqrt(q)
        b, ts = edge(f['kappa'])
        cls = 'BINDING' if ts < pin.D else 'INERT-IN-D'
        bbi, tsbi = edge(f['kappa_bi'])
        clsbi = 'BINDING' if tsbi < pin.D else 'INERT-IN-D'
        rec = {'class': cls, 't_star': ts, 't_star_bi': tsbi, 'class_bi': clsbi, 'resolution_sensitive': cls != clsbi,
               'sigma_star': ts * pin.rms_of(K, F),
               'window_lo': -ts if cls == 'BINDING' else -pin.D, 'window_hi': ts if cls == 'BINDING' else pin.D,
               'binding_end': 'hi' if f['kappa'] > 0 else 'lo'}
        if A == pin.primary_arm:
            T = abs(pin.raw[K]['arms'][A][F]['kappa3']) * ts / abs(f['kappa'])
            rec['trunc_T'], rec['truncation_sensitive'] = T, bool(T > pin.trunc_thr)
        else:
            rec['trunc_T'], rec['truncation_sensitive'] = None, False
        if b == 0:
            rec['nu'], rec['nu_is_inf'], rec['nullfloor_sensitive'] = None, True, True
        else:
            nu = abs(f['S_bi']) * ts / abs(b)
            rec['nu'], rec['nu_is_inf'], rec['nullfloor_sensitive'] = nu, False, bool(nu > pin.nf_thr)
        return rec

    def exclusion_record(self, K, A, lo, hi):
        pin = self.pin
        Rw, Rh = self.reach[K][A]['widened'], self.reach[K][A]['hull']
        if hi < Rw[0] or lo > Rw[1]:
            cls = 'EXCLUDED-IN-D'
            sub = 'SIGN' if ((hi < 0 and Rw[0] >= 0) or (lo > 0 and Rw[1] <= 0)) else 'MAGNITUDE'
        elif not (hi < Rh[0] or lo > Rh[1]):
            cls, sub = 'TUNED-ADMISSIBLE', None
        else:
            cls, sub = 'MARGIN', None
        sgn = 1 if lo > 0 else -1
        out = {}
        for F in pin.mapped[pin.branch(K)]:
            kap = self.fam[K][A][F]['kappa']
            rec = {'class': cls, 'subreason': sub, 't_in': None, 't_out': None, 'can_supply_alone': None}
            if (kap > 0) == (sgn > 0):
                t_in = math.sqrt(min(abs(lo), abs(hi)) / abs(kap))
                rec['t_in'], rec['t_out'], rec['can_supply_alone'] = t_in, math.sqrt(max(abs(lo), abs(hi)) / abs(kap)), bool(t_in <= pin.D)
            out[F] = rec
        return out

    def two_param(self, K, A, lo, hi):
        pin = self.pin
        k2, k44 = self.fam[K][A]['t2']['kappa'], self.fam[K][A]['t4']['kappa']
        n, a_lo, a_hi = pin.area_n, pin.area_lo, pin.area_hi
        nodes = [a_lo + i * (a_hi - a_lo) / (n - 1) for i in range(n)]
        last = n - 1
        adm, total, boundary = 0, 0, False
        sq4 = [k44 * t4 * t4 for t4 in nodes]
        for i, t2 in enumerate(nodes):
            s2 = k2 * t2 * t2
            for j in range(n):
                total += 1
                v = s2 + sq4[j]
                if lo <= v <= hi:
                    adm += 1
                    if i == 0 or i == last or j == 0 or j == last:
                        boundary = True
        prod = k2 * k44
        return {'area_fraction': adm / total, 'admissible_nodes': adm, 'total_nodes': total,
                'null_ray_slope': (math.sqrt(-k2 / k44) if prod < 0 else None),
                'definiteness': ('indefinite' if prod < 0 else ('negative-definite' if k2 < 0 else 'positive-definite')),
                'compact': not boundary}

    def map_interval(self, lo, hi):
        pin = self.pin
        if lo <= 0 <= hi:
            fam = {K: {A: {F: self.family_record(K, A, F, lo, hi) for F in pin.fam_list(K)} for A in pin.arms} for K in pin.keys}
            tp = {K: {A: self.two_param(K, A, lo, hi) for A in pin.arms} for K in pin.hex}
            return {'contains_zero': True, 'families': fam, 'exclusion': None, 'two_param': tp}
        exc = {K: {A: self.exclusion_record(K, A, lo, hi) for A in pin.arms} for K in pin.keys}
        return {'contains_zero': False, 'families': None, 'exclusion': exc, 'two_param': None}

    def gate_class(self, m):
        pin = self.pin
        if m['contains_zero']:
            fam = m['families']
            ok = all(fam[K][pin.primary_arm]['t4']['class'] == 'BINDING' for K in pin.primary_keys)
            return 'WINDOW-DELIVERED' if ok else 'INERT-IN-D'
        classes = [m['exclusion'][K][A][pin.mapped[pin.branch(K)][0]]['class'] for K in pin.keys for A in pin.arms]
        if all(c == 'EXCLUDED-IN-D' for c in classes):
            return 'KILL-IN-D'
        if any(c == 'TUNED-ADMISSIBLE' for c in classes):
            return 'TUNED'
        return 'MARGIN-ONLY'

    def map_rows(self, rows, scale=1.0):
        """rows: list of dicts with lo, hi, k_em_max, k_t_max (floats) and id, row_md5; never serialized as such"""
        pin = self.pin
        out_rows, ints = [], []
        for r in rows:
            x = max(r['k_em_max'], r['k_t_max']) * pin.d_EM
            void = bool(x > pin.KD)
            rec = {'id': r['id'], 'row_md5': r.get('row_md5'), 'void_regime': void,
                   'contains_zero': None, 'families': None, 'exclusion': None, 'two_param': None}
            if not void:
                lo, hi = r['lo'] * scale, r['hi'] * scale
                ints.append((lo, hi))
                rec.update(self.map_interval(lo, hi))
            out_rows.append(rec)
        n_void = sum(1 for r in out_rows if r['void_regime'])
        res = {'n_void_rows': n_void, 'rows': out_rows, 'combined': None, 'combined_empty': False, 'contains_zero': None,
               'sigma_union_hi': None, 'sigma_strict_hi': None}
        if not ints:
            res['gate_class'] = 'VOID'
            return res
        lo, hi = max(a for a, _ in ints), min(b for _, b in ints)
        if lo > hi:
            res['combined_empty'] = True
            res['gate_class'] = 'ANCHOR-INCONSISTENT'
            return res
        m = self.map_interval(lo, hi)
        res['contains_zero'] = m['contains_zero']
        res['combined'] = {'families': m['families'], 'exclusion': m['exclusion'], 'two_param': m['two_param']}
        res['gate_class'] = self.gate_class(m)
        sig = None
        if m['contains_zero']:
            recs = [m['families'][K][pin.primary_arm]['t4'] for K in pin.primary_keys]
            if all(r['class'] == 'BINDING' for r in recs):
                sig = (max(r['sigma_star'] for r in recs), min(r['sigma_star'] for r in recs))
        res['sigma_union_hi'], res['sigma_strict_hi'] = (sig if sig else (None, None))
        return res

    def map_with_oom(self, rows):
        base = self.map_rows(rows)
        up = self.map_rows(rows, scale=self.pin.oom[2])
        down = self.map_rows(rows, scale=self.pin.oom[0])
        if self.pin.oom[1] != 1.0:
            raise Halt('oom factors')
        worst, viol, notes = mono_check(self.pin, base, up, down)
        return base, up, down, worst, viol, notes


def mono_check(pin, base, up, down):
    """A-2.2 MONO / memo 3.8: exact sqrt(10) / sqrt(0.1) scaling of unclipped raw edges; monotone clipped windows and classes"""
    worst, viol, notes = 0.0, 0, []
    if base['combined'] is None or up['combined'] is None or down['combined'] is None:
        return worst, viol, ['no combined interval on some scaling; nothing to check']
    su, sd = math.sqrt(pin.oom[2]), math.sqrt(pin.oom[0])
    if base['contains_zero']:
        rank = {'BINDING': 0, 'INERT-IN-D': 1}
        for K, A, F in pin.cells():
            b, u, d = (x['combined']['families'][K][A][F] for x in (base, up, down))
            if b['t_star'] > 0:
                worst = max(worst, abs(u['t_star'] / b['t_star'] - su) / su, abs(d['t_star'] / b['t_star'] - sd) / sd)
            if b['t_star_bi'] > 0:
                worst = max(worst, abs(u['t_star_bi'] / b['t_star_bi'] - su) / su, abs(d['t_star_bi'] / b['t_star_bi'] - sd) / sd)
            if rank[u['class']] < rank[b['class']] or u['window_hi'] < b['window_hi']:
                viol += 1
                notes.append('x10 narrowed %s/%s/%s' % (K, A, F))
            if rank[d['class']] > rank[b['class']] or d['window_hi'] > b['window_hi']:
                viol += 1
                notes.append('x0.1 widened %s/%s/%s' % (K, A, F))
    else:
        rank = {'TUNED-ADMISSIBLE': 0, 'MARGIN': 1, 'EXCLUDED-IN-D': 2}
        for K, A, F in pin.cells():
            b, u, d = (x['combined']['exclusion'][K][A][F] for x in (base, up, down))
            for key in ('t_in', 't_out'):
                if b[key] is not None and b[key] > 0:
                    worst = max(worst, abs(u[key] / b[key] - su) / su, abs(d[key] / b[key] - sd) / sd)
            if rank[u['class']] < rank[b['class']]:
                viol += 1
                notes.append('x10 moved %s/%s toward admissible' % (K, A))
            if rank[d['class']] > rank[b['class']]:
                viol += 1
                notes.append('x0.1 moved %s/%s toward excluded' % (K, A))
    return worst, viol, notes


# --------------------------------------------------------------------------------------------- the masked parser
REQUIRED = ['id', 'class', 'delta_def', 'lo', 'hi', 'cl', 'reading', 'geom', 'k_em_max', 'k_t_max', 'src']
OPTIONAL = ['q', 'note']
CANON = REQUIRED + OPTIONAL
FREE_TEXT = {'src', 'note'}
NUM_RE = re.compile(r'^[+-]?(?:\d+\.?\d*|\.\d+)(?:[eE][+-]?\d+)?$')
BAD_UNICODE = {'\u0085', ' ', ' ', '﻿'}
SEP = ' | '


def is_bad_char(c):
    o = ord(c)
    return (o < 32 and c != '\n') or (127 <= o < 160) or c in BAD_UNICODE


def plain_number(s):
    if not NUM_RE.match(s):
        return None
    try:
        v = float(s)
    except ValueError:
        return None
    return v if math.isfinite(v) else None


def parse_masked(raw, tokens):
    """A-2.3 / memo 4.1-4.4. Returns (rows, census, row_md5s); raises MaskedAbort(reason) -- the reason never carries a value."""
    if raw.startswith(b'\xef\xbb\xbf'):
        raise MaskedAbort('BOM')
    try:
        text = raw.decode('utf-8')
    except UnicodeDecodeError:
        raise MaskedAbort('NOT_UTF8')
    if any(is_bad_char(c) for c in text):
        raise MaskedAbort('CONTROL_OR_SEPARATOR_CHAR')
    if not text.endswith('\n'):
        raise MaskedAbort('NO_FINAL_LF')
    if text.endswith('\n\n'):
        raise MaskedAbort('BLANK_LINE_AT_END')
    row_bytes = raw[:-1].split(b'\n')
    rows, md5s, fields_per_row, per_class = [], [], [], {}
    for n, rb in enumerate(row_bytes, 1):
        line = rb.decode('utf-8')
        tag = 'row %d' % n
        if line.strip() == '':
            raise MaskedAbort(tag + ' BLANK_LINE')
        if line.startswith('|') or line.endswith('|'):
            raise MaskedAbort(tag + ' LEADING_OR_TRAILING_BAR')
        fields = line.split(SEP)
        if any('|' in f for f in fields):
            raise MaskedAbort(tag + ' SEPARATOR_COLLISION')
        keys, vals = [], {}
        for f in fields:
            if '=' not in f:
                raise MaskedAbort(tag + ' FIELD_WITHOUT_EQUALS')
            k, v = f.split('=', 1)
            if k not in CANON:
                raise MaskedAbort(tag + ' UNKNOWN_KEY')
            if k in vals:
                raise MaskedAbort(tag + ' DUPLICATE_KEY ' + k)
            keys.append(k)
            vals[k] = v
        missing = [k for k in REQUIRED if k not in vals]
        if missing:
            raise MaskedAbort(tag + ' MISSING_KEY ' + ','.join(missing))
        if keys != [k for k in CANON if k in vals]:
            raise MaskedAbort(tag + ' KEY_ORDER')
        for k, v in vals.items():
            if v == '' or v != v.strip():
                raise MaskedAbort(tag + ' EMPTY_OR_PADDED ' + k)
            if k not in FREE_TEXT and not all(32 <= ord(c) < 127 for c in v):
                raise MaskedAbort(tag + ' NON_ASCII ' + k)
        if vals['id'] != 'SA-%d' % n:
            raise MaskedAbort(tag + ' ID_SEQUENCE')
        if vals['class'] not in tokens['class']:
            raise MaskedAbort(tag + ' CLASS_NOT_READ_BY_THIS_GATE')
        if vals['delta_def'] != tokens['delta_def']:
            raise MaskedAbort(tag + ' WRONG_DELTA_DEF')
        lo, hi = plain_number(vals['lo']), plain_number(vals['hi'])
        if lo is None or hi is None:
            raise MaskedAbort(tag + ' NOT_A_PLAIN_NUMBER lo/hi')
        if not lo <= hi:
            raise MaskedAbort(tag + ' ORDER')
        cl = vals['cl']
        if cl != 'hard':
            c = plain_number(cl)
            if c is None or not (0.0 < c < 1.0):
                raise MaskedAbort(tag + ' CL_NOT_IN_OPEN_UNIT_INTERVAL_OR_hard')
        if vals['reading'] not in tokens['reading_conformant']:
            raise MaskedAbort(tag + (' READING_NOT_MAPPED' if vals['reading'] in tokens['reading_frozen_list'] else ' UNKNOWN_READING'))
        if vals['geom'] not in tokens['geom']:
            raise MaskedAbort(tag + ' UNKNOWN_GEOM')
        kem, kt = plain_number(vals['k_em_max']), plain_number(vals['k_t_max'])
        if kem is None or kt is None or kem <= 0 or kt <= 0:
            raise MaskedAbort(tag + ' K_NOT_A_POSITIVE_PLAIN_NUMBER')
        if 'q' in vals and vals['q'] not in tokens['q']:
            raise MaskedAbort(tag + ' UNKNOWN_Q')
        rows.append({'id': vals['id'], 'lo': lo, 'hi': hi, 'k_em_max': kem, 'k_t_max': kt, 'row_md5': md5b(rb)})
        md5s.append(md5b(rb))
        fields_per_row.append(len(fields))
        per_class[vals['class']] = per_class.get(vals['class'], 0) + 1
    if not rows:
        raise MaskedAbort('NO_ROWS')
    return rows, {'rows': len(rows), 'per_class': per_class, 'fields_per_row': fields_per_row}, md5s


def unarmor(raw):
    """base64 text (marker lines stripped, whitespace ignored) or a zip with exactly one member"""
    if raw[:2] == b'PK':
        with zipfile.ZipFile(io.BytesIO(raw)) as z:
            names = z.namelist()
            if len(names) != 1:
                raise MaskedAbort('ZIP_MEMBER_COUNT')
            return z.read(names[0])
    body = ''.join(l for l in raw.decode('ascii', 'replace').splitlines() if not l.startswith('====='))
    return base64.b64decode(re.sub(r'\s+', '', body), validate=True)


def open_sealed(rel):
    if not STATE['phase3_active']:
        STATE['sealed_opens_before_phase3'] += 1
        raise Halt('MASK: sealed open attempted outside Phase 3')
    data = unarmor(read(rel))
    h = md5b(data)
    if h != SEALED_MD5 or len(data) != SEALED_BYTES:
        raise Halt('SEALED identity: md5 %s bytes %d (stated %s, %d)' % (h, len(data), SEALED_MD5, SEALED_BYTES))
    return data, h, len(data)


# --------------------------------------------------------------------------------------------- Phase 0
def phase0(pin, scanner, pats, sources, t1_result, derived_mine):
    P, R, res = pin.P, {}, {}

    def item(name, passed, floats, detail):
        e = {'passed': bool(passed), 'odf_reading': PHASE0_ODF[name], 'detail': detail}
        e.update(floats)
        R[name] = e
        log('  %-24s %s  %s' % (name, 'PASS' if passed else 'FAIL', ' '.join('%s=%s' % (k, repr(v)) for k, v in floats.items())))
        if not passed:
            raise Halt('Phase 0 %s failed -> INDETERMINATE' % name)

    # PIN: identity, re-read through provenance, two-leg agreement
    prov, dqf_keys = P['provenance'], set(sources['DQF'].keys())
    n_checked, mism, covered = 0, 0, set()
    for field, spec in prov.items():
        src = sources[spec['src']]
        if field.startswith('keys/<K>/'):
            sub = field[len('keys/<K>/'):]
            for K in pin.keys:
                if spec['scope'] == 'cubic' and K not in pin.cubic:
                    continue
                if spec['scope'] == 'dqf' and K not in dqf_keys:
                    continue
                want = jptr(pin.raw[K], '/' + sub)
                got = jptr(src, spec['pointer'].replace('{K}', K))
                n_checked += 1
                covered.add('/keys/%s/%s' % (K, sub))
                if json.dumps(want, sort_keys=True) != json.dumps(got, sort_keys=True):
                    mism += 1
        else:
            want = jptr(P, '/' + field) if field.startswith('raw/') else jptr(P['grids'], '/' + field[len('grids/'):])
            got = jptr(src, spec['pointer'])
            n_checked += 1
            covered.add('/' + field[len('raw/'):] if field.startswith('raw/') else '/grids/' + field[len('grids/'):])
            if json.dumps(want, sort_keys=True) != json.dumps(got, sort_keys=True):
                mism += 1
    raw_leaf_paths = {p for p, _ in leaves(P['raw'])}
    uncovered = []
    for p in sorted(raw_leaf_paths):
        base = re.sub(r'/\d+$', '', p)
        while base and base not in covered and re.search(r'/\d+$', base):
            base = re.sub(r'/\d+$', '', base)
        if p in covered or base in covered:
            continue
        if p.endswith('/branch') and jptr(P['raw'], p) == pin.branch(p.split('/')[2]):
            continue
        uncovered.append(p)
    wk = wk3 = wb1 = wS = 0.0
    for K in pin.keys:
        for A in pin.arms:
            for F in pin.fam_list(K):
                d = pin.raw[K]['arms'][A][F]
                if 'kappa_cc' in d and max(abs(d['kappa']), abs(d['kappa_cc'])) > pin.floor:
                    wk = max(wk, rel_dev(d['kappa'], d['kappa_cc']))
                if 'kappa3_cc' in d and max(abs(d['kappa3']), abs(d['kappa3_cc'])) > pin.floor:
                    wk3 = max(wk3, rel_dev(d['kappa3'], d['kappa3_cc']))
                if 'S_cc' in d:
                    wS = max(wS, abs(d['S'] - d['S_cc']))
        q = pin.raw[K]['quadform']
        if max(abs(q['kappa22_fit7']), abs(q['kappa22_fit7_cc'])) > pin.floor:
            wk = max(wk, rel_dev(q['kappa22_fit7'], q['kappa22_fit7_cc']))
        wb1 = max(wb1, rel_dev(pin.raw[K]['b1_Hill'], pin.raw[K]['b1_Hill_cc']))
    ok = (mism == 0 and not uncovered and wk <= pin.twoleg_rel and wk3 <= pin.twoleg_rel and wb1 <= pin.twoleg_rel and wS <= pin.tau)
    item('F-CTRL-SA-PIN', ok, {'raw_mismatches': mism, 'worst_twoleg_kappa_rel': wk, 'worst_twoleg_kappa3_rel': wk3,
                               'worst_twoleg_b1_rel': wb1, 'worst_twoleg_S_abs': wS},
         'pinned md5 guarded; %d values re-read through provenance pointers from the seven sources at their md5s; raw leaves not covered by a pointer: %d' % (n_checked, len(uncovered)))
    res['pin'] = {'values_checked': n_checked, 'raw_leaves': len(raw_leaf_paths), 'uncovered': uncovered}

    # PIN-DERIVED
    pinned_derived = {k: v for k, v in P['derived'].items() if k != 'summary'}
    mism, worst, missing, extra, nleaves = compare_leaves(derived_mine, pinned_derived, pin.pin_rel, pin.pin_abs)
    item('F-CTRL-SA-PIN-DERIVED', mism == 0 and worst <= 1.0, {'leaf_mismatches': mism, 'worst_scaled_dev': worst},
         '%d leaves re-derived with this instrument; missing %d, extra %d' % (nleaves, len(missing), len(extra)))
    res['derived_leaves'] = nleaves

    # ZERO
    w = max(abs(pin.raw[K]['arms'][A][F]['grid'][pin.i0]) for K in pin.keys for A in pin.arms for F in pin.fam_list(K))
    item('F-CTRL-SA-ZERO', w <= pin.zero_tol, {'worst_abs_r0': w}, 'the banked grid value at t = 0 on every key, arm and family')

    # RECON
    fam = derived_mine['families']
    wE = max(fam[K][pin.primary_arm][F]['recon_max_abs'] for K in pin.keys for F in pin.mapped[pin.branch(K)])
    wR = max(fam[K][A][F]['fit_res_rel'] for K, A, F in pin.cells() if A in pin.robust_arms)
    item('F-CTRL-SA-RECON', wE <= pin.recon_abs and wR <= pin.recon_rel, {'worst_abs_E2_Hill': wE, 'worst_rel_robust': wR},
         'three-term reconstruction on the primary arm inside D; fit vs basis-independent kappa on the robustness arms')

    # S (N-1)
    wb = max(abs(fam[K][A][F]['S_bi']) for K, A, F in pin.cells())
    wf = max(abs(fam[K][A][F]['S_fit']) for K, A, F in pin.cells() if fam[K][A][F]['S_fit'] is not None)
    item('F-CTRL-SA-S', wb <= pin.tau and wf <= pin.tau, {'worst_abs_bi': wb, 'worst_abs_fit': wf}, 'first-order slope null on every mapped cell')

    # K24 (N-2)
    N2 = derived_mine['nulls']['N-2']
    wb = max(max(abs(N2[K]['bi_chat']), abs(N2[K]['bi_cc']), abs(N2[K]['bi_5x5'])) for K in pin.keys)
    wf = max(abs(N2[K]['fit7']) for K in pin.keys)
    item('F-CTRL-SA-K24', wb <= pin.floor and wf <= pin.floor, {'worst_abs_bi': wb, 'worst_abs_fit7': wf}, 'kappa24 on all eight keys: chat diagnostic, CC checkpoint, own 5x5 mixed Richardson, fit7')

    # L2NULL (N-3, N-4)
    N3, N4 = derived_mine['nulls']['N-3'], derived_mine['nulls']['N-4']
    w2 = max(max(abs(N3[K]['fit']), abs(N3[K]['bi'])) for K in pin.cubic)
    w22 = max(max(abs(N4[K]['fit7']), abs(N4[K]['bi_5x5']), abs(N4[K]['k12_chat_t2sq'] or 0.0)) for K in pin.cubic)
    wt1 = max(abs(pin.raw[K]['pure_l2_change_t1']) for K in pin.cubic)
    item('F-CTRL-SA-L2NULL', w2 <= pin.floor and w22 <= pin.floor and wt1 <= pin.l2_t1_abs,
         {'worst_abs_kappa2': w2, 'worst_abs_kappa22': w22, 'worst_abs_t2_alone_t1': wt1}, CUBP2_II_IDENTITY)

    # SIGN
    mapper = Mapper(pin, fam, derived_mine['reach'])
    kref = abs(fam['hex_step|a'][pin.primary_arm]['t4']['kappa'])
    m = mapper.map_interval(-kref * SYN_T_ASYM_LO ** 2, kref * SYN_T_ASYM_HI ** 2)
    bad = 0
    for K, A, F in pin.cells():
        r, kap = m['families'][K][A][F], fam[K][A][F]['kappa']
        want_end = 'hi' if kap > 0 else 'lo'
        want_t = (SYN_T_ASYM_HI if kap > 0 else SYN_T_ASYM_LO) * math.sqrt(kref / abs(kap))
        if r['binding_end'] != want_end or abs(r['t_star'] - want_t) > 1e-12 * want_t:
            bad += 1
    item('F-CTRL-SA-SIGN', bad == 0, {'binding_end_mismatches': bad}, 'asymmetric synthetic interval: hi binds where kappa > 0, lo where kappa < 0, on every mapped cell')

    # GRID
    counts = grid_counts(pin)
    enum = {'n_t_grid': len(list(pin.t_grid)), 'n_fit_window_inclusive': len([t for t in pin.t_grid if abs(t) <= pin.D]),
            'n_fit_window_strict': len([t for t in pin.t_grid if abs(t) < pin.D]),
            'n_window_0p1_inclusive': len([t for t in pin.t_grid if abs(t) <= 0.1]),
            'n_window_0p1_strict': len([t for t in pin.t_grid if abs(t) < 0.1]),
            'n_t2t4_axis': len(pin.axis), 'n_t2t4_grid': len([(a, b) for a in pin.axis for b in pin.axis]),
            'n_area_grid': len([(i, j) for i in range(pin.area_n) for j in range(pin.area_n)])}
    cm = sum(1 for k in counts if counts[k] != enum[k])
    item('F-CTRL-SA-GRID', cm == 0, {'count_mismatches': cm}, 'every count computed from the generators (formula vs enumeration)')

    # MONO on the C-SYN-1 intervals
    worst, viol = 0.0, 0
    for t in pin.syn_t:
        b = kref * t * t
        rows = [{'id': 'SA-1', 'lo': -b, 'hi': b, 'k_em_max': pin.k_silent, 'k_t_max': pin.k_silent}]
        _, _, _, w, v, _ = mapper.map_with_oom(rows)
        worst, viol = max(worst, w), viol + v
    item('F-CTRL-SA-MONO', worst <= pin.mono_rel and viol == 0, {'worst_scaling_rel': worst, 'monotonicity_violations': viol},
         'C-SYN-1 intervals scaled x10 and x0.1: exact sqrt scaling of raw edges, monotone windows and classes')

    # MASK
    item('F-CTRL-SA-MASK', STATE['sealed_opens_before_phase3'] == 0, {'sealed_opens_before_phase3': STATE['sealed_opens_before_phase3']},
         'the sealed file is opened only in Phase 3; md5, bytes and census asserted at every open; masked parser')

    # T1
    per_file, hits, coll = t1_result
    item('F-CTRL-SA-T1', hits == 0, {'hits': hits, 'collisions': coll}, 'instrument, memo, pinned file, lock record, schema, comparator under gate list + A1')
    return R, res, mapper


def grid_counts(pin):
    tg = pin.t_grid
    return {'n_t_grid': len(tg), 'n_fit_window_inclusive': sum(abs(t) <= pin.D for t in tg), 'n_fit_window_strict': sum(abs(t) < pin.D for t in tg),
            'n_window_0p1_inclusive': sum(abs(t) <= 0.1 for t in tg), 'n_window_0p1_strict': sum(abs(t) < 0.1 for t in tg),
            'n_t2t4_axis': len(pin.axis), 'n_t2t4_grid': len(pin.axis) ** 2, 'n_area_grid': pin.area_n ** 2}


# --------------------------------------------------------------------------------------------- Phase 2
def synthetic_rows(pin, intervals, k=None):
    k = pin.k_silent if k is None else k
    return [{'id': 'SA-%d' % (i + 1), 'lo': lo, 'hi': hi, 'k_em_max': k, 'k_t_max': k} for i, (lo, hi) in enumerate(intervals)]


def phase2(pin, mapper, derived_mine, tokens, scanner, pats):
    fam, U, SYN = derived_mine['families'], derived_mine['unions'], derived_mine['synthetic']
    kref = abs(fam['hex_step|a'][pin.primary_arm]['t4']['kappa'])
    res = {}

    def suite(name, passed, detail):
        res[name] = {'passed': bool(passed), 'detail': detail}
        log('  %-9s %s  %s' % (name, 'PASS' if passed else 'FAIL', detail))

    def budget(t):
        return kref * t * t

    def fam_of(m, K, A, F):
        return m['combined']['families'][K][A][F]

    def exc_of(m, K, A):
        return m['combined']['exclusion'][K][A][pin.mapped[pin.branch(K)][0]]

    # C-SYN-1
    ok, notes = True, []
    for t in pin.syn_t:
        m = mapper.map_rows(synthetic_rows(pin, [(-budget(t), budget(t))]))
        r = fam_of(m, 'hex_step|a', pin.primary_arm, 't4')
        ok &= abs(r['t_star'] - t) <= 1e-12 * t and r['class'] == ('BINDING' if t < pin.D else 'INERT-IN-D')
        for K, A, F in pin.cells():
            want = math.sqrt(budget(t) / abs(fam[K][A][F]['kappa']))
            ok &= abs(fam_of(m, K, A, F)['t_star'] - want) <= 1e-12 * want
        notes.append('%s:%s' % (t, m['gate_class']))
    suite('C-SYN-1', ok, 'symmetric budgets on the reference cell and every cell; gate ' + ', '.join(notes))
    # C-SYN-2
    m = mapper.map_rows(synthetic_rows(pin, [(-budget(SYN_T_ASYM_LO), budget(SYN_T_ASYM_HI))]))
    ok = True
    for K, A, F in pin.cells():
        kap, r = fam[K][A][F]['kappa'], fam_of(m, K, A, F)
        want = (SYN_T_ASYM_HI if kap > 0 else SYN_T_ASYM_LO) * math.sqrt(kref / abs(kap))
        ok &= r['binding_end'] == ('hi' if kap > 0 else 'lo') and abs(r['t_star'] - want) <= 1e-12 * want
    suite('C-SYN-2', ok, 'asymmetric interval: binding ends by sign(kappa), t* by the binding end on every cell')
    # C-SYN-3
    Up, Um, Hp = U['widened_all'][1], U['widened_all'][0], U['hull_all'][1]
    m1 = mapper.map_rows(synthetic_rows(pin, [(10 * Up, 20 * Up)]))
    ok1 = m1['gate_class'] == 'KILL-IN-D'
    for K in pin.keys:
        for A in pin.arms:
            e, Rw = exc_of(m1, K, A), derived_mine['reach'][K][A]['widened']
            ok1 &= e['class'] == 'EXCLUDED-IN-D' and e['subreason'] == ('MAGNITUDE' if Rw[1] > 0 else 'SIGN')
    m2 = mapper.map_rows(synthetic_rows(pin, [(20 * Um, 10 * Um)]))
    ok2 = m2['gate_class'] == 'KILL-IN-D'
    for K in pin.keys:
        for A in pin.arms:
            e, Rw = exc_of(m2, K, A), derived_mine['reach'][K][A]['widened']
            ok2 &= e['class'] == 'EXCLUDED-IN-D' and e['subreason'] == ('MAGNITUDE' if Rw[0] < 0 else 'SIGN')
    m3 = mapper.map_rows(synthetic_rows(pin, [(0.25 * Hp, 0.5 * Hp)]))
    ok3 = m3['gate_class'] == 'TUNED' and any(exc_of(m3, K, A)['class'] == 'TUNED-ADMISSIBLE' for K in pin.keys for A in pin.arms)
    m4 = mapper.map_rows(synthetic_rows(pin, [tuple(SYN['robustness_only_positive'])]))
    prim_tuned = any(exc_of(m4, K, pin.primary_arm)['class'] == 'TUNED-ADMISSIBLE' for K in pin.primary_keys)
    rob_tuned = any(exc_of(m4, K, A)['class'] == 'TUNED-ADMISSIBLE' for K in pin.keys for A in pin.arms if not (A == pin.primary_arm and K in pin.primary_keys))
    ok4 = m4['gate_class'] == 'TUNED' and not prim_tuned and rob_tuned
    suite('C-SYN-3', ok1 and ok2 and ok3 and ok4, 'excluding-zero intervals: (i) %s (ii) %s (iii) %s (iv) %s' % (m1['gate_class'], m2['gate_class'], m3['gate_class'], m4['gate_class']))
    # C-SYN-4
    m = mapper.map_rows(synthetic_rows(pin, [(-1.0, 1.0)]))
    suite('C-SYN-4', m['gate_class'] == 'INERT-IN-D' and all(fam_of(m, K, A, F)['class'] == 'INERT-IN-D' for K, A, F in pin.cells()), 'wide interval: INERT-IN-D everywhere; gate ' + m['gate_class'])
    # C-SYN-5
    ok = True
    for t in pin.syn_t:
        m = mapper.map_rows(synthetic_rows(pin, [(-budget(t), budget(t))]))
        for K in pin.cubic:
            for A in pin.arms:
                for F in pin.null_fams['cubic']:
                    r = fam_of(m, K, A, F)
                    ok &= r['class'] == 'NULL-INERT' and r['window_lo'] == -pin.D and r['window_hi'] == pin.D and r['t_star'] is None
    suite('C-SYN-5', ok, 'the fcc t2 family is NULL-INERT with window D under C-SYN-1')
    # C-SYN-6
    ok, codes = csyn6(tokens)
    suite('C-SYN-6', ok, 'fifteen malformed files abort masked with reason codes; the valid file parses; no synthetic value in any output: ' + '; '.join(codes))
    # C-SYN-7
    worst, viol = 0.0, 0
    for t in pin.syn_t:
        _, _, _, w, v, _ = mapper.map_with_oom(synthetic_rows(pin, [(-budget(t), budget(t))]))
        worst, viol = max(worst, w), viol + v
    suite('C-SYN-7', worst <= pin.mono_rel and viol == 0, 'OOM on the C-SYN-1 intervals: worst scaling rel %r, violations %d' % (worst, viol))
    # C-SYN-8
    m = mapper.map_rows(synthetic_rows(pin, [(-budget(SYN_T_ASYM_LO), budget(SYN_T_ASYM_LO)), (-budget(SYN_T_ASYM_HI), budget(SYN_T_OUTER))]))
    r = fam_of(m, 'hex_step|a', pin.primary_arm, 't4')
    r2 = fam_of(m, 'hex_step|a', pin.primary_arm, 't2')
    ok = (abs(r['t_star'] - SYN_T_ASYM_LO) <= 1e-12 * SYN_T_ASYM_LO and r['binding_end'] == 'hi'
          and abs(r2['t_star'] - SYN_T_ASYM_HI * math.sqrt(kref / abs(fam['hex_step|a'][pin.primary_arm]['t2']['kappa']))) <= 1e-12 and r2['binding_end'] == 'lo'
          and m['combined_empty'] is False and m['n_void_rows'] == 0 and len(m['rows']) == 2)
    suite('C-SYN-8', ok, 'two consistent rows: the intersection is mapped (upper end from row 1, lower end from row 2)')
    # C-SYN-9
    m = mapper.map_rows(synthetic_rows(pin, [(budget(SYN_T_ASYM_LO), budget(SYN_T_OUTER)), (-budget(SYN_T_OUTER), -budget(SYN_T_ASYM_LO))]))
    suite('C-SYN-9', m['gate_class'] == 'ANCHOR-INCONSISTENT' and m['combined_empty'] and m['combined'] is None, 'two disjoint rows: ' + m['gate_class'])
    # C-SYN-10
    t = pin.syn_t[1]
    ma = mapper.map_rows(synthetic_rows(pin, [(-budget(t), budget(t))], k=pin.k_void))
    rows = synthetic_rows(pin, [(-budget(t), budget(t))], k=pin.k_void) + synthetic_rows(pin, [(-budget(t), budget(t))])
    rows[1]['id'] = 'SA-2'
    mb = mapper.map_rows(rows)
    mc = mapper.map_rows(synthetic_rows(pin, [(-budget(t), budget(t))]))
    ok = (ma['gate_class'] == 'VOID' and ma['rows'][0]['void_regime'] and ma['n_void_rows'] == 1 and ma['combined'] is None
          and mb['rows'][0]['void_regime'] and not mb['rows'][1]['void_regime'] and mb['n_void_rows'] == 1
          and json.dumps(mb['combined'], sort_keys=True) == json.dumps(mc['combined'], sort_keys=True) and mb['gate_class'] == mc['gate_class'])
    suite('C-SYN-10', ok, 'regime clause: a void-k row is VOID-REGIME; alone -> gate %s; with a silent row the silent row alone is mapped' % ma['gate_class'])
    # C-SYN-11
    m = mapper.map_rows(synthetic_rows(pin, [(0.0, 0.0)]))
    ok = m['gate_class'] == 'WINDOW-DELIVERED'
    for K, A, F in pin.cells():
        r = fam_of(m, K, A, F)
        ok &= r['t_star'] == 0.0 and r['nu'] is None and r['nu_is_inf'] is True and r['nullfloor_sensitive'] is True and r['class'] == 'BINDING'
    suite('C-SYN-11', ok, 'the point interval: t* = 0, nu infinite, NULL-FLOOR set, BINDING on every mapped cell; gate ' + m['gate_class'])
    # C-SYN-12
    b = budget(pin.syn_tight)
    m = mapper.map_rows(synthetic_rows(pin, [(-b, b)]))
    ok, nset, nclear = True, 0, 0
    for K, A, F in pin.cells():
        r, f = fam_of(m, K, A, F), fam[K][A][F]
        ts = math.sqrt(b / abs(f['kappa']))
        want = abs(f['S_bi']) * ts / b > pin.nf_thr
        ok &= r['nullfloor_sensitive'] == want
        nset += want
        nclear += not want
    suite('C-SYN-12', ok and nset >= 1 and nclear >= 1, 'tight budget: the null-floor flag recomputed per cell; set on %d cells, clear on %d' % (nset, nclear))
    # C-SYN-13
    ok, notes = True, []
    for name in ('margin_positive', 'margin_negative'):
        m = mapper.map_rows(synthetic_rows(pin, [tuple(SYN[name])]))
        cl = [exc_of(m, K, A)['class'] for K in pin.keys for A in pin.arms]
        ok &= m['gate_class'] == 'MARGIN-ONLY' and 'TUNED-ADMISSIBLE' not in cl and 'MARGIN' in cl
        notes.append('%s:%s' % (name, m['gate_class']))
    suite('C-SYN-13', ok, 'the pinned MARGIN-band intervals: ' + ', '.join(notes))
    # C-SYN-14
    K0, A0 = 'cubic_step|001', pin.primary_arm
    grid = list(pin.raw[K0]['arms'][A0]['t4']['grid'])
    grid[pin.t_grid.index(0.02)] += 5e-13
    reach2 = build_reach(pin, fam, {(K0, A0, 't4'): grid})
    grid0 = list(pin.raw[K0]['arms'][A0]['t4']['grid'])
    grid0[pin.i0] += 5e-13
    reach3 = build_reach(pin, fam, {(K0, A0, 't4'): grid0})
    m2 = Mapper(pin, fam, reach2)
    mm = m2.map_rows(synthetic_rows(pin, [(0.25 * Hp, 0.5 * Hp)]))
    e = mm['combined']['exclusion'][K0][A0]['t4']
    ok = (reach2[K0][A0]['hull'][1] == 0.0 and reach2[K0][A0]['widened'][1] == 0.0 and reach3[K0][A0]['hull'][1] == 0.0
          and e['class'] == 'EXCLUDED-IN-D' and e['subreason'] == 'SIGN')
    suite('C-SYN-14', ok, 'grid noise at zero: the rebuilt hull upper end snaps to 0 (perturbation at t = 0.02, and at t = 0 as an extra check); a positive interval classes SIGN')
    return res


def csyn6(tokens):
    """memo 4.7: fifteen malformed synthetic files and one valid one, parsed masked; no synthetic value may leak"""
    lo, hi, cl, kem, kt, src = '-0.0031415926', '0.0027182818', '0.8642', '1234.5678', '8765.4321', 'SYNTHETIC-SOURCE-QZX'
    # the leak search uses the full value strings and their long digit runs only (a short fragment could match an md5 by chance)
    secrets = [lo, hi, cl, kem, kt, src, '3141592', '2718281', '1234.5678', '8765.4321', 'SYNTHETIC-SOURCE']
    STATE['synthetic_secrets'] = secrets

    def row(**over):
        f = {'id': 'SA-1', 'class': 'spd', 'delta_def': 'tensor_over_EM_minus_1', 'lo': lo, 'hi': hi, 'cl': cl, 'reading': 'bound',
             'geom': 'single', 'k_em_max': kem, 'k_t_max': kt, 'src': src}
        f.update(over)
        return ' | '.join('%s=%s' % (k, f[k]) for k in REQUIRED if k in f)
    valid = (row() + '\n').encode('utf-8')
    cases = {
        'CRLF': (row() + '\r\n').encode('utf-8'),
        'BOM': b'\xef\xbb\xbf' + valid,
        'trailing blank line': valid + b'\n',
        'form feed in src': (row(src='SYN\x0cTHETIC') + '\n').encode('utf-8'),
        'U+2028 in src': (row(src='SYN THETIC') + '\n').encode('utf-8'),
        'Unicode minus': (row(lo='−0.0031415926') + '\n').encode('utf-8'),
        'superscript form': (row(hi='2.7×10⁻³') + '\n').encode('utf-8'),
        'bar in src': (row(src='SYN|THETIC') + '\n').encode('utf-8'),
        'lo > hi': (row(lo=hi, hi=lo) + '\n').encode('utf-8'),
        'reading=ceiling': (row(reading='ceiling') + '\n').encode('utf-8'),
        'wrong delta_def': (row(delta_def='EM_over_tensor_minus_1') + '\n').encode('utf-8'),
        'missing key': ((' | '.join(f for f in row().split(' | ') if not f.startswith('geom='))) + '\n').encode('utf-8'),
        'wrong id': (row(id='SA-2') + '\n').encode('utf-8'),
        'duplicate key': (row() + ' | cl=' + cl + '\n').encode('utf-8'),
        'percent-form cl': (row(cl='86.42%') + '\n').encode('utf-8'),
    }
    tmp = tempfile.mkdtemp(prefix='g_mscs_a_csyn6_')
    ok, codes, texts = True, [], []
    for name, data in cases.items():
        path = os.path.join(tmp, re.sub(r'\W+', '_', name) + '.md')
        open(path, 'wb').write(data)
        try:
            parse_masked(open(path, 'rb').read(), tokens)
            ok = False
            codes.append('%s -> NO ABORT' % name)
        except MaskedAbort as e:
            codes.append('%s -> %s' % (name, e))
        os.remove(path)
    path = os.path.join(tmp, 'valid.md')
    open(path, 'wb').write(valid)
    try:
        rows, census, md5s = parse_masked(open(path, 'rb').read(), tokens)
        ok &= census['rows'] == 1 and census['per_class'] == {'spd': 1} and census['fields_per_row'] == [len(REQUIRED)] and md5s[0] == md5b(valid[:-1])
        codes.append('valid -> parsed, census %d row' % census['rows'])
    except MaskedAbort as e:
        ok = False
        codes.append('valid -> %s' % e)
    os.remove(path)
    os.rmdir(tmp)
    leak = [s for s in secrets if any(s in c for c in codes)]
    if leak:
        ok = False
        codes.append('LEAK in reason codes')
    return ok, codes


# --------------------------------------------------------------------------------------------- checkpoint
def secrets_absent(text):
    return [s for s in STATE['synthetic_secrets'] if s in text]


def write_checkpoint(ck, rel, scanner, pats):
    bad = sorted({k for k in walk_keys(ck) if k in FORBIDDEN_KEYS})
    if bad:
        raise Halt('checkpoint carries a forbidden key: ' + ', '.join(bad))
    coll = 0
    for _ in range(8):
        ck['T1_post_write'] = {'hits': 0, 'collisions': coll}
        text = json.dumps(ck, sort_keys=True, indent=1, allow_nan=False) + '\n'
        h, c = t1_scan_text(scanner, pats, text)
        if h:
            raise Halt('T1 post-write: %d hit(s) in the checkpoint; not written' % h)
        if c == coll:
            break
        coll = c
    else:
        raise Halt('T1 post-write collision count did not reach a fixed point')
    if secrets_absent(text):
        raise Halt('a synthetic value of C-SYN-6 appears in the checkpoint; not written')
    path = os.path.join(HERE, rel)
    open(path, 'wb').write(text.encode('ascii'))
    h2, c2 = t1_scan_text(scanner, pats, open(path, 'rb').read().decode('utf-8'))
    if h2:
        os.remove(path)
        raise Halt('T1 post-write re-scan hit; checkpoint deleted')
    return md5b(text.encode('ascii')), len(text), c2


def identity_block(pin, guards, instrument_md5, flag):
    P, S = pin.P, pin.S
    return {'gate': GATE, 'leg': LEG, 'instrument': INSTRUMENT, 'instrument_md5': instrument_md5,
            'utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), 'activation_flag': flag,
            'memo_lock_md5': guards[MEMO], 'memo_lock_bytes': GUARDS[MEMO][1], 'lock_record_md5': guards[LOCK],
            'pinned_inputs_md5': guards[PINNED], 'pinned_inputs_bytes': GUARDS[PINNED][1],
            'builder_md5': P['_meta']['builder_md5'], 'verifier_md5': S['verifier_md5'],
            't1_list_md5': guards[T1_LIST], 't1_base_md5': guards[T1_BASE], 't1_a1_md5': guards[T1_A1], 'scanner_md5': guards[SCANNER],
            'schema_md5': guards[SCHEMA], 'comparator_md5': guards[COMPARATOR], 'ledger_base_md5': LEDGER_BASE_MD5,
            'elections': dict(ELECTIONS)}


def grids_block(pin):
    g = {'t_grid': list(pin.t_grid), 't2t4_axis': list(pin.axis), 'D': pin.D, 'area_lo': pin.area_lo, 'area_hi': pin.area_hi,
         'area_nodes_per_axis': pin.area_n, 'richardson_pairs': {'one_param': list(pin.rp1), 'two_param': list(pin.rp2)},
         'oom_factors': list(pin.oom)}
    g.update(grid_counts(pin))
    return g


# --------------------------------------------------------------------------------------------- main
def main(argv):
    if len(argv) < 2 or argv[1] not in ('preread', 'read'):
        print(__doc__)
        return 2
    mode = argv[1]
    inputs = argv[argv.index('--inputs') + 1] if '--inputs' in argv else 'inputs'
    flag = argv[argv.index('--flag') + 1] if '--flag' in argv else None
    t0 = time.time()
    try:
        log('%s %s leg, mode %s' % (GATE, LEG, mode))
        guards = guard_all()
        instrument_md5 = md5b(open(os.path.abspath(__file__), 'rb').read())
        log('guards: %d locked artifacts at their md5 and byte counts; instrument md5 %s' % (len(guards), instrument_md5))
        scanner = load_scanner()
        pats = scanner.load(os.path.join(HERE, T1_LIST)) + scanner.load(os.path.join(HERE, T1_A1))
        per_file, hits, coll = t1_scan(scanner, pats, T1_SCANNED + [INSTRUMENT])
        for rel, r in per_file.items():
            log('  T1 %-32s %s hits=%d collisions=%d' % (rel, 'HIT' if r['hits'] else 'CLEAN', r['hits'], r['collisions']))
        if hits:
            raise Halt('T1: %d hit(s) under the gate list + A1; halting (no override)' % hits)
        S = json.loads(read(SCHEMA).decode('ascii'))
        P = json.loads(read(PINNED).decode('ascii'))
        pin = Pinned(P, S)
        sources = {}
        for alias, spec in P['sources'].items():
            b = open(os.path.join(inputs, spec['path']), 'rb').read()
            if md5b(b) != spec['md5'] or len(b) != spec['bytes']:
                raise Halt('source %s (%s): md5 %s bytes %d differ from the pinned record' % (alias, spec['path'], md5b(b), len(b)))
            sources[alias] = json.loads(b.decode('utf-8'))
        log('sources: %d files at their md5s under %s' % (len(sources), inputs))
        derived_mine = rederive(pin)
        log('Phase 0')
        R0, extra0, mapper = phase0(pin, scanner, pats, sources, (per_file, hits, coll), derived_mine)
        log('Phase 2')
        R2 = phase2(pin, mapper, derived_mine, P['tokens'], scanner, pats)
        if not all(v['passed'] for v in R2.values()):
            raise Halt('Phase 2: a suite failed; no sealed open')
        ck = identity_block(pin, guards, instrument_md5, flag)
        ck.update({'phase0': R0, 'nulls': derived_mine['nulls'], 'grids': grids_block(pin), 'phase2': R2, 'phase3': None,
                   'extras': {'t1_scan': per_file, 'pin': extra0['pin'], 'derived_leaves_rederived': extra0['derived_leaves'],
                              'unions_rederived': derived_mine['unions'], 'synthetic_rederived': derived_mine['synthetic'],
                              'method': 'pure Python; own RFC 6901 binder over the seven pinned sources; own masked parser; '
                                        'Richardson even/odd/mixed parts as pinned; hull-and-widen reach; area grid enumerated from the pinned generator'}})
        if mode == 'preread':
            ck['extras']['elapsed_seconds'] = round(time.time() - t0, 3)
            h, n, c = write_checkpoint(ck, PREREAD_CK, scanner, pats)
            log('pre-read checkpoint written: %s md5 %s %d B; post-write T1 hits 0 collisions %d' % (PREREAD_CK, h, n, c))
            return 0
        # -------------------------------------------------------------------------------- Phase 3
        log('Phase 3')
        STATE['phase3_active'] = True
        data, smd5, sbytes = open_sealed(SEALED_ARMOR)
        try:
            rows, census, row_md5s = parse_masked(data, P['tokens'])
        except MaskedAbort as e:
            log('masked abort: %s (the read is not spent; no value emitted)' % e)
            return 1
        log('sealed: md5 %s bytes %d census %s row md5s %s' % (smd5, sbytes, json.dumps(census, sort_keys=True), row_md5s))
        base, up, down, worst, viol, notes = mapper.map_with_oom(rows)
        if viol or worst > pin.mono_rel:
            raise Halt('MONO on the actual rows: instrument defect (S9): violations %d worst %r %s' % (viol, worst, notes))
        gate = {'gate_class': base['gate_class'], 'sigma_union_hi': base['sigma_union_hi'], 'sigma_strict_hi': base['sigma_strict_hi'],
                'oom_class_x10': up['gate_class'], 'oom_class_x0p1': down['gate_class'],
                'oom_robust': bool(base['gate_class'] == up['gate_class'] == down['gate_class']),
                'contains_zero': base['contains_zero'], 'combined_empty': base['combined_empty'], 'n_void_rows': base['n_void_rows']}
        if gate['gate_class'] not in CLASS_PRECEDENCE:
            raise Halt('gate class outside the precedence list')
        ck['phase3'] = {'sealed_md5': smd5, 'sealed_bytes': sbytes, 'census': census, 'row_md5s': row_md5s, 't1_a1_md5': guards[T1_A1],
                        'n_void_rows': base['n_void_rows'], 'combined_empty': base['combined_empty'], 'contains_zero': base['contains_zero'],
                        'rows': base['rows'], 'combined': base['combined'], 'gate': gate}

        def cell_classes(m):
            if m['combined'] is None:
                return None
            if m['contains_zero']:
                return {'%s/%s/%s' % (K, A, F): m['combined']['families'][K][A][F]['class'] for K in pin.keys for A in pin.arms for F in pin.fam_list(K)}
            return {'%s/%s' % (K, A): m['combined']['exclusion'][K][A][pin.mapped[pin.branch(K)][0]]['class'] for K in pin.keys for A in pin.arms}
        ck['extras']['oom'] = {'x10': {'gate_class': up['gate_class'], 'cells': cell_classes(up), 'combined': up['combined']},
                               'x0p1': {'gate_class': down['gate_class'], 'cells': cell_classes(down), 'combined': down['combined']},
                               'mono_worst_scaling_rel': worst, 'mono_violations': viol}
        ck['extras']['elapsed_seconds'] = round(time.time() - t0, 3)
        h, n, c = write_checkpoint(ck, READ_CK, scanner, pats)
        log('gate class %s (x10 %s, x0.1 %s, OOM-robust %s); sigma_union_hi %r sigma_strict_hi %r' % (
            gate['gate_class'], gate['oom_class_x10'], gate['oom_class_x0p1'], gate['oom_robust'], gate['sigma_union_hi'], gate['sigma_strict_hi']))
        log('checkpoint written: %s md5 %s %d B; post-write T1 hits 0 collisions %d' % (READ_CK, h, n, c))
        return 0
    except Halt as e:
        log('HALT: %s' % e)
        return 1
    finally:
        leak = secrets_absent('\n'.join(STATE['log']))
        if leak:
            print('WARNING: a C-SYN-6 synthetic value reached stdout')


if __name__ == '__main__':
    sys.exit(main(sys.argv))
