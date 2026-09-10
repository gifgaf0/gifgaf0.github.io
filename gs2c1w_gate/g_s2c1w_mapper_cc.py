#!/usr/bin/env python3
"""g_s2c1w_mapper_cc.py — Gate G-S2C1-W, CC leg instrument (independent, from the frozen chain).

Built FROM SCRATCH under G_S2C1_W_CC_DISPATCH_INBAND.md §3 step 5: own lexer (NAMED-KEY
binding for `B =` and `k = ... /m`), own Born edge, own fixed-point dressing, own union,
own comparison-last gate. Implements staging memo §3.2–3.7, §4 under the locked elections
E-W-1(a) (a_phys interval; window edge at a_phys.lo), E-W-2(a) (GK column for the window
edge, GM for the robustness arm), E-W-3(a) (this leg's OWN a2 column), E-W-5(a), E-W-6(a)
(edge of record = Born a2-only; dressed reported), E-W-7(a) (reinstatement NONE), and the
ratified defaults D-W-1/4/5/6/7. Falsifiers per memo §7: F-W-PIN, F-W-ENV, F-W-L, F-W-DRESS,
F-W-MONO, F-W-T1, F-W-CENSUS.

Order of execution (each stage halts the chain on failure):
  1. T1 self-grep of this source and the scanner source (base ∪ A1, D-W-7 rule);
  2. F-W-PIN (pinned-inputs md5 + every memo §2 value at 1e-12 rel; the four G-POLY1
     edges pinned from the in-repo blind-leg checkpoint, md5-asserted, byte-values);
  3. pre-read suites on SYNTHETIC values (disjoint from anything sealed);
  4. the sealed read (single read; md5 + bytes + census asserted at open; masked X-1
     abort on any defect; the sealed text never appears in any output);
  5. per-arm records, robustness arm, union, intersection — serialized and hashed
     (pre_comparison_md5) BEFORE
  6. the comparison (INERT / TIGHTENED / FAIL-L; OOM x10 / x0.1; reinstatement NONE);
  7. checkpoint per schema v1.0, T1-scanned, hashed.
"""
import argparse, hashlib, json, math, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import t1_scan_cc as t1


# ---------------------------------------------------------------- halt classes
class MaskedAbort(Exception):
    """X-1 masked abort: carries a defect CLASS only — never sealed text."""
    def __init__(self, defect_class, read_spent=True):
        super().__init__(f'X-1 MASKED ABORT [{defect_class}]')
        self.defect_class = defect_class
        self.read_spent = read_spent


class S9Halt(Exception):
    """S9-class instrument halt (F-W-MONO and kin): never a finding."""


class GuardError(Exception):
    """Comparison-last guard violation."""


class PinHalt(Exception):
    """F-W-PIN masked halt (pre-open; no read spent)."""


# ------------------------------------------------------- pinned expectations
# Hard pins transcribed from the LOCKED staging memo §2 (md5 1ebb6a82...) and the
# lock record §5. E-W-3(a): this leg uses the CC a2 column. Cross-asserted against
# pinned_inputs_G_S2C1_W.json at 1e-12 rel before anything else runs.
ARMS = ['hex:step', 'hex:gem8', 'cubic:step', 'cubic:gem8']
EXPECT = {
    'a2_L_cc': {'GK': -0.01324, 'GM': -0.02063},
    'a2_L_chat': {'GK': -0.012794, 'GM': -0.019933},
    'ci_rel': 0.035,
    'a2_agg': {'hex:step': -0.01834766, 'hex:gem8': -0.02593369,
               'cubic:step': -0.02853747, 'cubic:gem8': -0.03971398},
    'a4_agg': {'hex:step': 0.0695, 'hex:gem8': 0.099,
               'cubic:step': 0.1068, 'cubic:gem8': 0.1493},
    'D0': {'hex:step': -0.0205, 'hex:gem8': -0.0289,
           'cubic:step': -0.0315, 'cubic:gem8': -0.0437},
    'Q_T_a': {'hex:step': 0.03519074, 'hex:gem8': 0.05002055,
              'cubic:step': 0.05407763, 'cubic:gem8': 0.0754943},
    's1': {'hex:step': 0.151508022, 'hex:gem8': 0.181569447,
           'cubic:step': 0.233348904, 'cubic:gem8': 0.284231508},
    'gpoly1_edges_m': {'hex:step': 2.1213132100130068, 'hex:gem8': 1.8866794048346085,
                       'cubic:step': 1.838266105289967, 'cubic:gem8': 1.6447865351995365},
    'gpoly1_union_upper_m': 2.1213132100130068,
    'l_P_m': 1.616255e-35,
    'C_lo': 0.0213, 'C_hi': 0.0851,
    'a_phys_lo_m': 1.8992420681551118e-34,
    'a_phys_hi_m': 7.588051643192489e-34,
}
CONSTS = {
    'KD_CLIP': 0.3,
    'DELTA4_THRESHOLD': 0.10,
    'FP_TOL_REL': 1e-15,
    'FP_MAX_ITER': 200,
    'c_q': {'phase': 1, 'group': 3},
    'oom_factors': [10.0, 0.1],
    'pin_rel_tol': 1e-12,
}
LOCK = {
    'memo': '1ebb6a82fcb24e207b164a654eb94dd1',
    'lock_record': '5f963ed8d7eff9f803da5c1eea2f841a',
    't1_base': '20ba1e7eab5a3bbffe510b4840edbc57',
    't1_a1': '735eae308aa7baec19f23da5602a2d82',
    'pinned_inputs': 'd1edc69b16dfd0b728a48cd8389b322b',
    'sealed_declared': '8c7d59f64057e372d7b1ff760667a7c2',
}
SEALED_DECLARED = {'md5': '8c7d59f64057e372d7b1ff760667a7c2', 'bytes': 154,
                   'rows': 1, 'per_class': {'disp': 1}, 'fields_per_row': 8}
GPOLY1_CKPT_MD5 = '2064bd7b4ed4f7b2b4e09bafdc0cf85a'


def md5_bytes(b):
    return hashlib.md5(b).hexdigest()


def md5_file(p):
    with open(p, 'rb') as fh:
        return md5_bytes(fh.read())


def rel_dev(a, b):
    return abs(a - b) / max(abs(b), 1e-300)


# ------------------------------------------------------------------ F-W-PIN
def f_w_pin(pinned_path, gpoly1_ckpt_path):
    got_md5 = md5_file(pinned_path)
    if got_md5 != LOCK['pinned_inputs']:
        raise PinHalt('F-W-PIN [INPUTS-MD5]')
    with open(pinned_path, encoding='utf-8') as fh:
        pj = json.load(fh)
    checks, worst = 0, 0.0

    def pin(actual, expected):
        nonlocal checks, worst
        checks += 1
        r = rel_dev(float(actual), float(expected))
        worst = max(worst, r)
        if r > CONSTS['pin_rel_tol']:
            raise PinHalt('F-W-PIN [VALUE]')

    pin(pj['a2_L_lattice']['cc']['GK'], EXPECT['a2_L_cc']['GK'])
    pin(pj['a2_L_lattice']['cc']['GM'], EXPECT['a2_L_cc']['GM'])
    pin(pj['a2_L_lattice']['chat']['GK'], EXPECT['a2_L_chat']['GK'])
    pin(pj['a2_L_lattice']['chat']['GM'], EXPECT['a2_L_chat']['GM'])
    pin(pj['a2_L_lattice']['ci_rel'], EXPECT['ci_rel'])
    for arm in ARMS:
        pin(pj['a2_agg_grain'][arm], EXPECT['a2_agg'][arm])
        pin(pj['a4_agg_grain_diagnostic'][arm], EXPECT['a4_agg'][arm])
        pin(pj['D0_static_born_shift'][arm], EXPECT['D0'][arm])
        pin(pj['Q_T_a'][arm], EXPECT['Q_T_a'][arm])
        pin(pj['s1'][arm], EXPECT['s1'][arm])
        pin(pj['gpoly1_pinned_edges_m'][arm], EXPECT['gpoly1_edges_m'][arm])
    pin(pj['gpoly1_W_union_upper_m'], EXPECT['gpoly1_union_upper_m'])
    ch = pj['a_phys_chain_E_W_1a']
    pin(ch['l_P_m'], EXPECT['l_P_m'])
    pin(ch['C_ratio_xi_over_a']['lo'], EXPECT['C_lo'])
    pin(ch['C_ratio_xi_over_a']['hi'], EXPECT['C_hi'])
    pin(ch['a_phys_m']['lo'], EXPECT['a_phys_lo_m'])
    pin(ch['a_phys_m']['hi'], EXPECT['a_phys_hi_m'])
    # chain identity a_phys = l_P / C (lo edge from C.hi, hi edge from C.lo)
    pin(EXPECT['l_P_m'] / EXPECT['C_hi'], EXPECT['a_phys_lo_m'])
    pin(EXPECT['l_P_m'] / EXPECT['C_lo'], EXPECT['a_phys_hi_m'])
    cj = pj['constants']
    pin(cj['KD_CLIP'], CONSTS['KD_CLIP'])
    pin(cj['DELTA4_THRESHOLD'], CONSTS['DELTA4_THRESHOLD'])
    pin(cj['FP_TOL_REL'], CONSTS['FP_TOL_REL'])
    pin(cj['FP_MAX_ITER'], CONSTS['FP_MAX_ITER'])
    pin(cj['c_q']['phase'], CONSTS['c_q']['phase'])
    pin(cj['c_q']['group'], CONSTS['c_q']['group'])
    pin(cj['oom_factors'][0], CONSTS['oom_factors'][0])
    pin(cj['oom_factors'][1], CONSTS['oom_factors'][1])
    pin(cj['pin_rel_tol'], CONSTS['pin_rel_tol'])

    # the four G-POLY1 edges pinned from the in-repo blind-leg checkpoint (byte-values)
    got_gp = md5_file(gpoly1_ckpt_path)
    if got_gp != GPOLY1_CKPT_MD5:
        raise PinHalt('F-W-PIN [GPOLY1-CKPT-MD5]')
    with open(gpoly1_ckpt_path, encoding='utf-8') as fh:
        gp = json.load(fh)
    for arm in ARMS:
        if gp['per_arm'][arm]['W'][1] != EXPECT['gpoly1_edges_m'][arm]:
            raise PinHalt('F-W-PIN [GPOLY1-EDGE]')
        if gp['per_arm'][arm]['cls'] != 'P-2':
            raise PinHalt('F-W-PIN [GPOLY1-CLASS]')
    if gp['W_union'][0][1] != EXPECT['gpoly1_union_upper_m']:
        raise PinHalt('F-W-PIN [GPOLY1-UNION]')

    # report-only tie-in (F-W-PIN consistency, non-verdict)
    ratios = [EXPECT['a2_agg'][a] / EXPECT['Q_T_a'][a] for a in ARMS]
    mean_ratio = sum(ratios) / len(ratios)
    spread = max(abs(r / mean_ratio - 1.0) for r in ratios)
    return {'status': 'PASS', 'pinned_inputs_md5': got_md5, 'gpoly1_ckpt_md5': got_gp,
            'values_checked': checks, 'max_rel_dev': worst,
            'tie_in_report_only': {'mean_a2agg_over_QTa': mean_ratio,
                                   'spread_rel': spread}}


# ------------------------------------------------------------------- lexer
Q_TOKENS = ('phase', 'group')


def unwrap(field):
    """CC-DD lexer normalization: the author-supplied sealed serialization wraps
    token fields in markdown inline-code (one symmetric backtick pair). The pair
    is formatting, not content — it is stripped before token interpretation.
    (The declared census of record already reads through it.)"""
    s = field.strip()
    if len(s) >= 2 and s[0] == '`' and s[-1] == '`':
        s = s[1:-1].strip()
    return s


def _named_number(field, key, unit=None):
    """NAMED-KEY binding: the field must read `<key> = <value>[ <unit>]` exactly.
    Returns the numeric value(s); a band form `<key> = [v1, v2] <unit>` is allowed
    for the wavenumber key. Never echoes the field text on failure."""
    s = unwrap(field)
    if not s.startswith(key):
        raise MaskedAbort('NAMED-KEY')
    s = s[len(key):].lstrip()
    if not s.startswith('='):
        raise MaskedAbort('NAMED-KEY')
    s = s[1:].strip()
    if unit is not None:
        if not s.endswith(unit):
            raise MaskedAbort('UNIT')
        s = s[:-len(unit)].strip()
    band = None
    if s.startswith('[') and s.endswith(']'):
        parts = s[1:-1].split(',')
        if len(parts) != 2:
            raise MaskedAbort('BAND-FORM')
        try:
            band = (float(parts[0]), float(parts[1]))
        except ValueError:
            raise MaskedAbort('NUMBER-FORM')
        if not (band[0] > 0.0 and band[1] > band[0]):
            raise MaskedAbort('NEGATIVITY')
        return band
    try:
        val = float(s)
    except ValueError:
        raise MaskedAbort('NUMBER-FORM')
    if not val > 0.0:
        raise MaskedAbort('NEGATIVITY')
    return val


def parse_row(row):
    """Lex one sealed row (8 pipe-delimited fields: 7 content + trailing empty).
    Returns a masked record: class, q, B, k (eval wavenumber), band, row_md5.
    Identifier fields (f1/f2/f6) are consumed for structure only and never returned."""
    fields = row.split('|')
    if len(fields) != 8 or fields[7] != '':
        raise MaskedAbort('FIELD-COUNT')
    f0 = unwrap(fields[0])
    if f0 != 'disp':
        raise MaskedAbort('KIND')
    if not fields[1].strip() or not fields[2].strip():
        raise MaskedAbort('EMPTY-FIELD')
    q = unwrap(fields[3])
    if q not in Q_TOKENS:
        raise MaskedAbort('Q-TOKEN')
    B = _named_number(fields[4], 'B')
    if isinstance(B, tuple):
        raise MaskedAbort('BAND-FORM')
    kval = _named_number(fields[5], 'k', unit='/m')
    if isinstance(kval, tuple):
        band, k_eval = kval, kval[1]        # D-W-6: band evaluated at the upper edge
    else:
        band, k_eval = None, kval
    if not fields[6].strip():
        raise MaskedAbort('EMPTY-FIELD')
    return {'cls': f0, 'q': q, 'B': B, 'k': k_eval, 'band': band,
            'row_md5': md5_bytes(row.encode('utf-8'))}


def read_sealed(path, declared):
    """Single sealed read: md5 + bytes + census asserted at open (F-W-CENSUS);
    any pre-parse defect aborts with the read NOT spent."""
    with open(path, 'rb') as fh:
        raw = fh.read()
    if md5_bytes(raw) != declared['md5'] or len(raw) != declared['bytes']:
        raise MaskedAbort('SEALED-MD5', read_spent=False)
    text = raw.decode('utf-8')
    if not text.endswith('\n'):
        raise MaskedAbort('SERIALIZATION', read_spent=False)
    rows = text[:-1].split('\n')
    if len(rows) != declared['rows']:
        raise MaskedAbort('CENSUS', read_spent=False)
    census = {}
    for row in rows:
        if row.startswith('|'):
            raise MaskedAbort('SERIALIZATION', read_spent=False)
        parts = row.split('|')
        if len(parts) != declared['fields_per_row']:
            raise MaskedAbort('CENSUS', read_spent=False)
        cls0 = unwrap(parts[0])
        census[cls0] = census.get(cls0, 0) + 1
    if census != declared['per_class']:
        raise MaskedAbort('CENSUS', read_spent=False)
    return [parse_row(r) for r in rows], {'rows': len(rows), 'per_class': census,
                                          'fields_per_row': declared['fields_per_row']}


# ------------------------------------------------------------ edge machinery
def dressed_root(B_prime, c_q, a2_mag, a4, x_born):
    """Root of c_q*(a2_mag*x^2 - a4*x^4) = B_prime in x = kd, below the turnover;
    fixed-point iteration seeded at the Born value, bisection fallback."""
    if a4 <= 0.0:
        return x_born, 'CONVERGED', 0.0
    x_turn = math.sqrt(a2_mag / (2.0 * a4))
    f_max = c_q * (a2_mag * x_turn ** 2 - a4 * x_turn ** 4)
    if B_prime > f_max:
        return None, 'NO-ROOT-BEYOND-TURNOVER', None
    x = x_born
    for _ in range(CONSTS['FP_MAX_ITER']):
        x_next = math.sqrt((B_prime / c_q + a4 * x ** 4) / a2_mag)
        if x_next > x_turn:
            x_next = x_turn
        if abs(x_next - x) <= CONSTS['FP_TOL_REL'] * max(x_next, 1e-300):
            x = x_next
            break
        x = x_next
    else:
        lo, hi = x_born, x_turn                      # contraction-basin fallback
        for _ in range(200):
            mid = 0.5 * (lo + hi)
            if c_q * (a2_mag * mid ** 2 - a4 * mid ** 4) < B_prime:
                lo = mid
            else:
                hi = mid
        x = 0.5 * (lo + hi)
    resid = abs(c_q * (a2_mag * x ** 2 - a4 * x ** 4) - B_prime) / max(B_prime, 1e-300)
    return x, 'CONVERGED', resid


def eval_disp(anc, arm, a2_L, a_phys, a2_agg, a4_agg, budget_factor=1.0):
    """One disp anchor on one arm (memo §3.4). Returns the full per-anchor record."""
    c_q = CONSTS['c_q'][anc['q']]
    B = anc['B'] * budget_factor
    k = anc['k']
    F_L = c_q * abs(a2_L) * (k * a_phys) ** 2
    B_prime = B - F_L
    fail_base = B_prime <= 0.0
    fail_relaxed = (anc['B'] * budget_factor * 10.0 - F_L) <= 0.0
    fail_L = fail_base and fail_relaxed              # EG-9: election-robust only
    rec = {'anchor': anc['idx'], 'q': anc['q'], 'c_q': c_q, 'F_L': F_L,
           'B_prime': B_prime, 'fail_L': fail_L, 'oom_fragile': fail_base and not fail_L,
           'edge_born_m': None, 'kd': None, 'voided': False, 'envelope_ceiling_m': None,
           'delta4': None, 'dressing_sensitive': False,
           'edge_dressed_m': None, 'dressed_status': 'NOT-EVALUATED'}
    if fail_base:
        return rec
    a2m = abs(a2_agg)
    kd = math.sqrt(B_prime / (c_q * a2m))
    edge = kd / k
    rec['kd'] = kd
    rec['edge_born_m'] = edge
    if kd > CONSTS['KD_CLIP']:
        rec['voided'] = True                         # F-W-ENV: a VOID can only widen
        rec['envelope_ceiling_m'] = CONSTS['KD_CLIP'] / k
    rec['delta4'] = abs(a4_agg) * kd ** 2 / a2m
    rec['dressing_sensitive'] = rec['delta4'] > CONSTS['DELTA4_THRESHOLD']  # F-W-DRESS
    x_d, status, resid = dressed_root(B_prime, c_q, a2m, a4_agg, kd)
    rec['dressed_status'] = status
    rec['dressed_residual'] = resid
    rec['edge_dressed_m'] = (x_d / k) if x_d is not None else None
    if anc.get('band'):
        k1, k2 = anc['band']                         # D-W-6: full sweep serialized
        sweep = []
        for i in range(9):
            kk = k1 + (k2 - k1) * i / 8.0
            fl = c_q * abs(a2_L) * (kk * a_phys) ** 2
            bp = B - fl
            sweep.append([kk, (math.sqrt(bp / (c_q * a2m)) / kk) if bp > 0 else None])
        rec['band_sweep'] = sweep
    return rec


def eval_arm(anchors, arm, pins, budget_factor=1.0):
    """Per-arm window W'_A (memo §3.5): min over the pinned G-POLY1 edge and every
    non-VOIDED disp edge of record (Born, E-W-6(a)). No vld rows exist at this gate."""
    a2_L, a_phys = pins['a2_L_window'], pins['a_phys_window']
    recs = [eval_disp(a, arm, a2_L, a_phys, pins['a2_agg'][arm], pins['a4_agg'][arm],
                      budget_factor) for a in anchors]
    pinned_edge = pins['gpoly1_edges_m'][arm]
    if any(r['fail_L'] for r in recs):
        return {'arm_class': 'FAIL-L', 'W_upper_m': None, 'governing': 'FAIL-L',
                'disp': recs, 'pinned_gpoly1_edge_m': pinned_edge}
    candidates = [(pinned_edge, 'pinned_gpoly1')]
    for r in recs:
        if r['edge_born_m'] is not None and not r['voided']:
            candidates.append((r['edge_born_m'], f"disp:{r['anchor']}"))
    upper, governing = min(candidates)
    all_voided = all(r['voided'] or r['edge_born_m'] is None for r in recs)
    cls = 'VOID-DISP' if all_voided else "P-2'"
    return {'arm_class': cls, 'W_upper_m': upper, 'governing': governing,
            'disp': recs, 'pinned_gpoly1_edge_m': pinned_edge}


def eval_all_arms(anchors, pins):
    per_arm = {}
    for arm in ARMS:
        base = eval_arm(anchors, arm, pins, 1.0)
        rel10 = eval_arm(anchors, arm, pins, CONSTS['oom_factors'][0])
        tight = eval_arm(anchors, arm, pins, CONSTS['oom_factors'][1])
        base['oom_robust'] = (rel10['arm_class'] == base['arm_class']
                              == tight['arm_class'])
        base['oom_relaxed_upper'] = rel10['W_upper_m']
        base['oom_tightened_upper'] = tight['W_upper_m']
        per_arm[arm] = base
    return per_arm


def union_of(per_arm):
    finite = {a: r['W_upper_m'] for a, r in per_arm.items() if r['W_upper_m'] is not None}
    if not finite:
        return {'W_union_prime': None, 'union_governing_arm': None, 'W_intersection': None}
    gov = max(finite, key=lambda a: finite[a])
    return {'W_union_prime': [0.0, finite[gov]],
            'union_governing_arm': gov,
            'W_intersection': [0.0, min(finite.values())]}


def compare_gate(pre_comparison_md5, per_arm, union, pinned_upper):
    """Comparison of record — LAST (EG-4). Refuses to run before the per-arm and
    union records are serialized and hashed (comparison-last guard)."""
    if not pre_comparison_md5:
        raise GuardError('comparison attempted before serialization + hash')
    fail_arms = [a for a in ARMS if per_arm[a]['arm_class'] == 'FAIL-L']
    if fail_arms:
        cls = 'FAIL-L'
        upper = union['W_union_prime'][1] if union['W_union_prime'] else None
    else:
        upper = union['W_union_prime'][1]
        if upper > pinned_upper * (1.0 + CONSTS['pin_rel_tol']):
            raise S9Halt('F-W-MONO: union exceeds the pinned edge — instrument defect')
        cls = 'INERT' if rel_dev(upper, pinned_upper) <= CONSTS['pin_rel_tol'] else 'TIGHTENED'
    return {'class': cls,
            'W_union_prime_upper_m': upper,
            'W_union_pinned_upper_m': pinned_upper,
            'per_arm_classes': {a: per_arm[a]['arm_class'] for a in ARMS},
            'per_arm_governing': {a: per_arm[a]['governing'] for a in ARMS},
            'reinstatement': 'NONE'}                 # E-W-7(a)


# --------------------------------------------------------------- robustness
def robustness_arm(anchors, pins):
    """E-W-1(a)/E-W-2(a) serialization: the maximal-floor reading (GM column,
    a_phys.hi) per anchor — non-verdict; FAIL-L is only ever declared from the
    window reading via EG-9 inside eval_disp."""
    out = []
    for a in anchors:
        c_q = CONSTS['c_q'][a['q']]
        F_L = c_q * abs(pins['a2_L_robust']) * (a['k'] * pins['a_phys_robust']) ** 2
        out.append({'anchor': a['idx'], 'q': a['q'], 'F_L_GM_aphys_hi': F_L,
                    'B_prime': a['B'] - F_L, 'floor_consumes_budget': (a['B'] - F_L) <= 0.0})
    return out


# ------------------------------------------------------------ pre-read suites
def run_suites(pins_real):
    """Every suite runs on SYNTHETIC values disjoint from anything sealed
    (round decimals never used by the pinned inputs). All must pass pre-read."""
    R = {}
    syn = {'a2_agg': {a: -0.02 for a in ARMS}, 'a4_agg': {a: 0.08 for a in ARMS},
           'gpoly1_edges_m': {a: 2.0 for a in ARMS},
           'a2_L_window': -0.01, 'a_phys_window': 2e-34,
           'a2_L_robust': -0.02, 'a_phys_robust': 8e-34}

    def anc(B, k, q='phase', idx=0, band=None):
        return {'idx': idx, 'cls': 'disp', 'q': q, 'B': B, 'k': k, 'band': band,
                'row_md5': '0' * 32}

    # 1. Born edge vs hand value: B=1.8e-4, a2=-0.02, F_L~0, k=5 -> kd=sqrt(9e-3)
    r = eval_disp(anc(1.8e-4, 5.0), 'hex:step', syn['a2_L_window'], syn['a_phys_window'],
                  -0.02, 0.08)
    R['born_edge_hand'] = (rel_dev(r['edge_born_m'], 0.018973665961010276) < 1e-12
                          and rel_dev(r['kd'], 0.09486832980505137) < 1e-12)

    # 2. envelope VOID: B=0.01 -> kd=sqrt(0.5)>0.3 -> VOIDED with ceiling 0.3/k
    r = eval_disp(anc(1e-2, 5.0), 'hex:step', syn['a2_L_window'], syn['a_phys_window'],
                  -0.02, 0.08)
    R['envelope_void'] = r['voided'] and rel_dev(r['envelope_ceiling_m'], 0.06) < 1e-12

    # 3. FAIL-L election-robust vs fragile (synthetic floor F_L=0.03 via a_phys=1, k=1, c_q=3)
    r_rob = eval_disp(anc(1e-3, 1.0, q='group'), 'hex:step', -0.01, 1.0, -0.02, 0.08)
    r_fra = eval_disp(anc(5e-3, 1.0, q='group'), 'hex:step', -0.01, 1.0, -0.02, 0.08)
    R['fail_L_robust'] = r_rob['fail_L'] and not r_rob['oom_fragile']
    R['fail_L_fragile'] = (not r_fra['fail_L']) and r_fra['oom_fragile']

    # 4. Delta4 both sides + dressed fixed point + no-root-beyond-turnover
    r_lo = eval_disp(anc(2e-5, 5.0), 'hex:step', syn['a2_L_window'], syn['a_phys_window'],
                     -0.02, 0.08)     # kd^2=1e-3 -> Delta4=4e-3 < 0.10
    r_hi = eval_disp(anc(6e-4, 5.0), 'hex:step', syn['a2_L_window'], syn['a_phys_window'],
                     -0.02, 0.08)     # kd^2=0.03 -> Delta4=0.12 > 0.10
    R['delta4_below'] = (not r_lo['dressing_sensitive']) and r_lo['delta4'] < 0.10
    R['delta4_above'] = r_hi['dressing_sensitive'] and r_hi['delta4'] > 0.10
    R['dressed_residual'] = (r_hi['dressed_status'] == 'CONVERGED'
                             and r_hi['dressed_residual'] is not None
                             and r_hi['dressed_residual'] <= 1e-12
                             and r_hi['edge_dressed_m'] > r_hi['edge_born_m'])
    x_d, status, _ = dressed_root(2e-3, 1.0, 0.02, 0.08, math.sqrt(0.1))
    R['no_root_beyond_turnover'] = status == 'NO-ROOT-BEYOND-TURNOVER' and x_d is None

    # 5. phase/group edge ratio sqrt(3) at zero floor
    r_p = eval_disp(anc(1.8e-4, 5.0, q='phase'), 'hex:step', 0.0, 0.0, -0.02, 0.08)
    r_g = eval_disp(anc(1.8e-4, 5.0, q='group'), 'hex:step', 0.0, 0.0, -0.02, 0.08)
    R['c_q_ratio_sqrt3'] = rel_dev(r_p['edge_born_m'] / r_g['edge_born_m'],
                                   math.sqrt(3.0)) < 1e-12

    # 6. malformed-row masked aborts (each must raise the right defect class,
    #    and no abort message may echo row content)
    sent = ('SYNTHX1', 'SYNTHX2', 'SYNTHX3')
    good = f'disp|{sent[0]}|{sent[1]}|phase|B = 2.5e-4|k = 4.0 /m|{sent[2]}|'
    bad = {'FIELD-COUNT': good.rsplit('|', 2)[0] + '|',
           'FIELD-COUNT#2': f'disp|{sent[0]}|{sent[1]}|phase|B = 2.5e-4|k = 4.0 /m|extra|bar|',
           'NAMED-KEY': good.replace('B = ', 'budget = '),
           'NEGATIVITY': good.replace('B = 2.5e-4', 'B = -2.5e-4'),
           'UNIT': good.replace(' /m', ''),
           'Q-TOKEN': good.replace('phase', 'speed'),
           'KIND': good.replace('disp|', 'att|', 1)}
    ok = parse_row(good)
    R['lexer_good_row'] = (ok['B'] == 2.5e-4 and ok['k'] == 4.0 and ok['q'] == 'phase')
    mask_ok = True
    for want, row in bad.items():
        try:
            parse_row(row)
            R[f'abort_{want}'] = False
        except MaskedAbort as e:
            R[f'abort_{want}'] = e.defect_class == want.split('#')[0]
            mask_ok &= not any(s in str(e) for s in sent)
    R['abort_messages_masked'] = mask_ok

    # 7. census mismatch: two rows against a declared census of one; read NOT spent
    import tempfile
    two = (good + '\n' + good + '\n').encode('utf-8')
    with tempfile.NamedTemporaryFile('wb', suffix='.md', delete=False) as fh:
        fh.write(two)
    try:
        read_sealed(fh.name, {'md5': md5_bytes(two), 'bytes': len(two),
                              'rows': 1, 'per_class': {'disp': 1}, 'fields_per_row': 8})
        R['census_mismatch'] = False
    except MaskedAbort as e:
        R['census_mismatch'] = e.defect_class == 'CENSUS' and not e.read_spent
    finally:
        os.unlink(fh.name)

    # 8. comparison-last guard
    try:
        compare_gate(None, {}, {}, 2.0)
        R['comparison_last_guard'] = False
    except GuardError:
        R['comparison_last_guard'] = True

    # 9. F-W-MONO trap: synthetic union wider than the pinned edge must halt as S9
    syn_arm = {a: {'arm_class': "P-2'", 'W_upper_m': 3.0, 'governing': 'disp:0'}
               for a in ARMS}
    try:
        compare_gate('deadbeef', syn_arm, {'W_union_prime': [0.0, 3.0],
                                           'union_governing_arm': 'hex:step',
                                           'W_intersection': [0.0, 3.0]}, 2.0)
        R['f_w_mono_trap'] = False
    except S9Halt:
        R['f_w_mono_trap'] = True

    # 10. masking self-scan: a serialized synthetic checkpoint fragment must not
    #     carry any sealed-text sentinel (only class/q/numbers/row_md5 survive)
    frag = json.dumps({'anchors': [{k: ok[k] for k in
                                    ('cls', 'q', 'B', 'k', 'row_md5')}]})
    R['masking_self_scan'] = not any(s in frag for s in sent)

    # 11. band rule D-W-6: evaluated at the upper band edge; sweep serialized
    rb = eval_disp(anc(1.8e-4, 5.0, band=(2.0, 5.0)), 'hex:step', 0.0, 0.0, -0.02, 0.08)
    R['band_upper_edge'] = (rel_dev(rb['edge_born_m'], 0.018973665961010276) < 1e-12
                            and len(rb.get('band_sweep', [])) == 9
                            and rb['band_sweep'][0][1] > rb['band_sweep'][-1][1])

    # 12. inline-code unwrap: one symmetric backtick pair per field is formatting,
    #     not content — the wrapped row must lex identically (row_md5 aside)
    wrapped = ('`disp`|' + f'{sent[0]}|{sent[1]}|' + '`phase`|`B = 2.5e-4`|'
               + '`k = 4.0 /m`|' + f'{sent[2]}|')
    w = parse_row(wrapped)
    R['inline_code_unwrap'] = (w['cls'] == ok['cls'] and w['q'] == ok['q']
                               and w['B'] == ok['B'] and w['k'] == ok['k']
                               and w['row_md5'] != ok['row_md5'])

    R['ALL'] = all(v for v in R.values())
    return R


# ------------------------------------------------------------------- driver
def canonical(obj):
    return json.dumps(obj, indent=1, sort_keys=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--pinned', required=True)
    ap.add_argument('--t1-base', required=True)
    ap.add_argument('--t1-a1', required=True)
    ap.add_argument('--gpoly1-ckpt', required=True)
    ap.add_argument('--sealed', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--suites-out')
    ap.add_argument('--selftest-only', action='store_true')
    args = ap.parse_args()

    here = os.path.dirname(os.path.abspath(__file__))
    self_path = os.path.abspath(__file__)
    scanner_path = os.path.join(here, 't1_scan_cc.py')

    # ---- stage 1: T1 self-grep (F-W-T1) — every instrument at every invocation
    if md5_file(args.t1_base) != LOCK['t1_base'] or md5_file(args.t1_a1) != LOCK['t1_a1']:
        raise PinHalt('F-W-PIN [T1-LIST-MD5]')
    pats = t1.load_patterns([args.t1_base, args.t1_a1])
    src_hits, src_logged = 0, 0
    for p in (self_path, scanner_path):
        h, l = t1.scan_file(pats, p)
        src_hits += len(h)
        src_logged += len(l)
    if src_hits:
        raise S9Halt('F-W-T1: forbidden pattern in instrument source')
    print(f'[1] T1 self-grep: {len(pats)} distinct patterns, 0 hits, '
          f'{src_logged} logged (formatting-collision class)')

    # ---- stage 2: F-W-PIN
    pin_report = f_w_pin(args.pinned, args.gpoly1_ckpt)
    print(f"[2] F-W-PIN: PASS ({pin_report['values_checked']} values, "
          f"max rel dev {pin_report['max_rel_dev']:.3e})")

    # ---- stage 3: pre-read suites (synthetic, disjoint)
    suites = run_suites(None)
    n_ok = sum(1 for k, v in suites.items() if k != 'ALL' and v)
    n_all = sum(1 for k in suites if k != 'ALL')
    print(f'[3] pre-read suites: {n_ok}/{n_all} PASS')
    if args.suites_out:
        with open(args.suites_out, 'w', encoding='utf-8') as fh:
            fh.write(canonical(suites) + '\n')
    if not suites['ALL']:
        raise S9Halt('pre-read suite failure — no sealed open')
    if args.selftest_only:
        print('selftest-only: stopping before any sealed open')
        return

    # ---- stage 4: the sealed read (single; F-W-CENSUS; masked X-1)
    anchors_raw, census = read_sealed(args.sealed, SEALED_DECLARED)
    anchors = []
    for i, a in enumerate(anchors_raw):
        a['idx'] = i
        anchors.append(a)
    print(f"[4] sealed read: md5 asserted, census {census['rows']} row "
          f"{census['per_class']}, {len(anchors)} anchor(s) parsed (masked)")

    # synthetic-disjointness assertion (H-item if ever false)
    syn_values = {1.8e-4, 1e-2, 1e-3, 5e-3, 2e-5, 6e-4, 2.5e-4, 5.0, 4.0, 1.0, 2.0}
    disjoint = all(a['B'] not in syn_values and a['k'] not in syn_values
                   for a in anchors)

    # ---- stage 5: per-arm records, robustness arm, union — serialize + hash
    pins = {'a2_agg': EXPECT['a2_agg'], 'a4_agg': EXPECT['a4_agg'],
            'gpoly1_edges_m': EXPECT['gpoly1_edges_m'],
            'a2_L_window': EXPECT['a2_L_cc']['GK'],       # E-W-2(a), E-W-3(a)
            'a_phys_window': EXPECT['a_phys_lo_m'],       # E-W-1(a), D-W-1
            'a2_L_robust': EXPECT['a2_L_cc']['GM'],
            'a_phys_robust': EXPECT['a_phys_hi_m']}
    per_arm = eval_all_arms(anchors, pins)
    union = union_of(per_arm)
    robust = robustness_arm(anchors, pins)
    anchors_masked = [{'idx': a['idx'], 'cls': a['cls'], 'q': a['q'],
                       'B': a['B'], 'k': a['k'], 'row_md5': a['row_md5']}
                      for a in anchors]
    pre_block = {'sealed': {'md5': SEALED_DECLARED['md5'],
                            'bytes': SEALED_DECLARED['bytes'], 'census': census},
                 'anchors': anchors_masked, 'per_arm': per_arm,
                 'robustness_arm': robust, 'union': union}
    pre_md5 = md5_bytes(canonical(pre_block).encode('utf-8'))
    print(f'[5] per-arm + union serialized; pre_comparison_md5 {pre_md5}')

    # ---- stage 6: comparison of record (LAST)
    comparison = compare_gate(pre_md5, per_arm, union, EXPECT['gpoly1_union_upper_m'])
    oom_states = []
    for f in CONSTS['oom_factors']:
        pa = {arm: eval_arm(anchors, arm, pins, f) for arm in ARMS}
        un = union_of(pa)
        oom_states.append(compare_gate('oom-arm', pa, un,
                                       EXPECT['gpoly1_union_upper_m'])['class'])
    comparison['oom_robust'] = all(s == comparison['class'] for s in oom_states)
    print(f"[6] comparison: {comparison['class']} "
          f"(OOM-ROBUST={comparison['oom_robust']}; reinstatement NONE)")

    # ---- stage 7: checkpoint per schema v1.0; T1-scan; hash
    ckpt = {
        'gate': 'G-S2C1-W', 'leg': 'cc',
        'read': {'leg_read_index': 1, 'policy': 'single sealed read; md5 + census asserted at open',
                 'synthetics_disjoint_from_sealed': disjoint},
        'instrument_md5': md5_file(self_path),
        'lock': LOCK,
        't1_patterns': len(pats),
        'pinned_gate': pin_report,
        'sealed': pre_block['sealed'],
        'anchors': anchors_masked,
        'per_arm': per_arm,
        'robustness_arm': robust,
        'union': union,
        'pre_comparison_md5': pre_md5,
        'comparison': comparison,
        't1_source_scan': {'hits': 0, 'logged': src_logged,
                           'files': ['g_s2c1w_mapper_cc.py', 't1_scan_cc.py']},
    }
    body = canonical(ckpt)
    h, l = t1.scan_text(pats, body)
    if h:
        raise S9Halt('F-W-T1: forbidden pattern in checkpoint serialization')
    ckpt['t1_checkpoint_scan'] = {'hits': 0, 'logged': len(l),
                                  'note': 'numeric collisions logged, not fatal (D-W-7); '
                                          'scan taken over the pre-scan serialization'}
    out_text = canonical(ckpt) + '\n'
    with open(args.out, 'w', encoding='utf-8') as fh:
        fh.write(out_text)
    print(f'[7] checkpoint written: {args.out} md5 {md5_bytes(out_text.encode("utf-8"))} '
          f'({len(out_text.encode("utf-8"))} B); t1 checkpoint scan 0 hits, {len(l)} logged')


if __name__ == '__main__':
    try:
        main()
    except (MaskedAbort, S9Halt, GuardError, PinHalt) as e:
        print(f'HALT: {e}', file=sys.stderr)
        sys.exit(2)
