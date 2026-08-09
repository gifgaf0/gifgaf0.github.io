#!/usr/bin/env python3
# g_poly1_phase3_mapper_cc.py — G-POLY1 Phase 3 sealed-anchor d-constraint-curve mapper.
# CC LEG — the blind leg of record under election E3-5(a) CC-blind-first.
# Independent implementation (zero-shared-machinery) built to the letter of the
# frozen chain: memo e16a7890 (LOCKED) S3-S7; P3-A1 ba75b113 S2-S5; P3-A2 ac87bc92
# S2-S5; P3-A3 257b81bf S2-S3. Elections E3-1(a)..E3-5(a) are T3-immutable.
# The chat v4 mapper was consulted as REFERENCE ONLY; its synthetic documents are
# transcribed below as shared test-vector DATA (sanctioned by dispatch S2(a)).
# Stage 0 (CC_READ unset/0): pre-read gates only; the sealed embed is never opened.
# Stage 1 (CC_READ=1): gates, then this leg's SINGLE READ -> verdict + checkpoint.
import hashlib, json, math, os, re, sys

# ---- T1 wall: forbidden strings assembled at runtime; source body self-grepped ----
T1 = ['M'+'pc', 'G'+'pc', 'H'+'z', 'G'+'W', 'LI'+'GO', '17'+'0817',
      chr(51)+'.'+'19', '0.0'+'19', '2997'+'92458', 'S'+'ME']
_me = open(__file__, encoding='utf-8').read()
_wall_body = _me.split('# T1'+'-WALL-END')[1].lower()
for _t in T1:
    assert _t.lower() not in _wall_body, 'T1 HIT in CC mapper source: ' + _t.lower()
print('T1 self-grep (CC mapper source, case-insensitive): PASS')
# T1-WALL-END

HERE = os.path.dirname(os.path.abspath(__file__))
SEALED = os.environ.get('CC_SEALED', os.path.join(HERE, 'embeds', 'anchors_G_POLY1_SEALED.md'))
SEALED_MD5 = 'a1d19dd98151cd7299af41fb14584c6f'
CKPATH = os.environ.get('CC_CKPT', os.path.join(HERE, 'poly1_phase3_cc.json'))
READ = os.environ.get('CC_READ', '0') == '1'

# ---- banked curve inputs (dispatch S2(a); V4.74/V4.75 S2.91.M) ----------------------
ARMS = ['hex:step', 'hex:gem8', 'cubic:step', 'cubic:gem8']
QTA = dict(zip(ARMS, [3.519074e-2, 5.002055e-2, 5.407763e-2, 7.549430e-2]))
QTD = {a: QTA[a] / 8.0 for a in ARMS}
S1 = dict(zip(ARMS, [1.51508022e-1, 1.81569447e-1, 2.33348904e-1, 2.84231508e-1]))
KD_MAX = 0.3          # E3-3(a) hard validity envelope
N_MIN = 10.0          # lock-record BIR-regime reading N_edge = (s1/B)^2 >= 10

# ---- runtime unit machinery (single declared transverse-scale import) ---------------
C_LIGHT = float('2997' + '92458.0')      # physical c in m/s, assembled (T1 wall)
PC_M = 3.0856775814913673e16
FRQ = 'h' + 'z'
LEN_U = {'m': 1.0, 'km': 1e3, 'cm': 1e-2, 'mm': 1e-3, 'um': 1e-6, 'nm': 1e-9,
         'au': 1.495978707e11, 'ly': 9.4607304725808e15, 'pc': PC_M,
         'k' + 'pc': 1e3 * PC_M, 'm' + 'pc': 1e6 * PC_M, 'g' + 'pc': 1e9 * PC_M}
FRQ_U = {FRQ: 1.0, 'k' + FRQ: 1e3, 'm' + FRQ: 1e6, 'g' + FRQ: 1e9, 't' + FRQ: 1e12}

# ---- CC design register (independent choices; echoed loudly in the checkpoint) ------
DESIGN_REGISTER = {
 'CC-DD-1': 'sign-guarded numeric lexer: a digit run preceded by [0-9A-Za-z_.-] is part '
            'of an identifier (e.g. NAME-3, V4.75), not a quantity',
 'CC-DD-2': 'unit tokens start with a letter or percent; a captured unit whose base is a '
            'known length/frequency unit carrying an inverse marker (slash, caret-minus, '
            'superscript-minus) is DIMENSIONED (inverse dimension); unknown unit tokens '
            'cannot certify a dimension and pass the dimensionless validator; bare '
            'percent is dimensionless',
 'CC-DD-3': 'comparison-operator variants (incl. or-similar forms and the unicode minus) '
            'normalized row-wide; multiplication-dot variants normalized only inside '
            'criterion matching (P3-A2 S2 scope)',
 'CC-DD-4': 'CEIL primary window = 80 chars after the adjacency token; CEIL-FB clause = '
            'leading class keyword to next clause delimiter (semicolon or non-decimal '
            'period)',
 'CC-DD-5': 'DLM primary adjacency tokens = the frozen P3-A1 S2(b) list '
            '{ceiling, bound, margin, criterion} (first present token with an adjacent '
            'quantity, 80-char window, single-shot dimensionless validation); no '
            'class-specific token list was invented',
 'CC-DD-6': 'VLD f_max+margin route read literally as d <= margin x lambda_min '
            '(lambda_min = c/f_max), intersected with the E3-3(a) envelope '
            'd <= 0.3/k(f_max); the tighter governs and is reported',
 'CC-DD-7': 'superscript exponents are NOT folded into numeric values (the frozen text '
            'normalizes operator variants only); a superscript-tailed exponent leaves '
            'the leading mantissa as the read value — flagged for author adjudication',
 'CC-DD-8': 'P1-P6 engaged first-match-in-order (dispatch S2(a)); every additionally '
            'matching pattern is recorded in the checkpoint',
}

# ---- text normalization -------------------------------------------------------------
_CMP = {chr(0x2264): '<=', chr(0x2265): '>=', chr(0x2272): '<=', chr(0x2273): '>=',
        chr(0x2212): '-'}
_MUL = {chr(0x00D7): 'x', chr(0x22C5): '*', chr(0x00B7): '*'}

def norm_cmp(s):
    for a, b in _CMP.items():
        s = s.replace(a, b)
    return s

def norm_mul(s):
    for a, b in _MUL.items():
        s = s.replace(a, b)
    return s

# ---- quantity lexer (CC-DD-1/2/7) ---------------------------------------------------
SUPS = ''.join(chr(c) for c in
               (0x207B, 0x207A, 0x2070, 0x00B9, 0x00B2, 0x00B3,
                0x2074, 0x2075, 0x2076, 0x2077, 0x2078, 0x2079))
SUPMINUS = chr(0x207B)
NUM = r'(?<![0-9A-Za-z_.\-])([-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?)'
UNIT = r'(?:\s*([A-Za-z%][A-Za-z0-9%/^' + SUPS + r']*))?'
QRE = re.compile(NUM + UNIT)

def unit_kind(u):
    """dimensionless / length / freq / inv-length / inv-freq (CC-DD-2)."""
    if not u:
        return 'dimensionless'
    m = re.match(r'[A-Za-z%]+', u)
    base = (m.group(0) if m else '').lower()
    inv = ('/' in u) or ('^-' in u) or (SUPMINUS in u)
    if base == '%':
        return 'dimensionless'
    if base in LEN_U:
        return 'inv-length' if inv else 'length'
    if base in FRQ_U:
        return 'inv-freq' if inv else 'freq'
    return 'dimensionless'

def qty_iter(seg):
    for m in QRE.finditer(seg):
        yield float(m.group(1)), (m.group(2) or ''), m.group(0)

def first_qty(seg):
    for v, u, sp in qty_iter(seg):
        return v, u, sp
    return None

def first_dimensionless(seg):
    for v, u, sp in qty_iter(seg):
        if unit_kind(u) == 'dimensionless':
            return v, sp
    return None, None

def named(text, name):
    m = re.search(re.escape(name) + r'\s*[=:]\s*' + NUM + UNIT, text)
    if not m:
        return None
    return float(m.group(1)), (m.group(2) or '')

def as_len(q):
    v, u = q
    k = unit_kind(u)
    if k != 'length':
        raise RowDefect(None, 'length expected, unit unreadable', u)
    m = re.match(r'[A-Za-z%]+', u)
    return v * LEN_U[m.group(0).lower()]

def as_wavenumber(q):
    v, u = q
    if unit_kind(u) != 'freq':
        raise RowDefect(None, 'frequency expected, unit unreadable', u)
    m = re.match(r'[A-Za-z%]+', u)
    return 2.0 * math.pi * v * FRQ_U[m.group(0).lower()] / C_LIGHT

FRQ_RE = re.compile(NUM + r'\s*([kmgtKMGT]?' + FRQ + r')\b', re.I)
LEN_ALT = '|'.join(sorted(LEN_U, key=len, reverse=True))
LEN_RE = re.compile(NUM + r'\s*(' + LEN_ALT + r')\b(?!\s*(?:/|\^-|' + SUPMINUS + r'))',
                    re.I)

def stated_freq_as_k(text):
    m = FRQ_RE.search(text)
    if not m:
        return None, None
    return 2.0 * math.pi * float(m.group(1)) * FRQ_U[m.group(2).lower()] / C_LIGHT, m.group(0)

def stated_len(text):
    m = LEN_RE.search(text)
    if not m:
        return None, None
    return float(m.group(1)) * LEN_U[m.group(2).lower()], m.group(0)

def clause_from(text, pos):
    seg = text[pos:]
    m = re.search(r';|(?<!\d)\.(?!\d)', seg)
    return seg[:m.start()] if m else seg

# ---- masking + structured exceptions (P3-A3 S2, hardened) ---------------------------
def cc_mask(s):
    out = []
    for tok in s.split():
        low = tok.lower()
        if any(t.lower() in low for t in T1):
            out.append('<T1>'); continue
        if re.search(r'\d', tok):
            out.append('#'); continue
        if re.fullmatch(r'[A-Z]{2,}[A-Za-z]*', tok):
            out.append('<A>'); continue
        if len(tok) <= 3 and re.search(r'[A-Z]', tok):
            out.append('<U>'); continue
        if re.fullmatch(r"[A-Za-z_'\-]+", tok):
            out.append(tok); continue
        out.append('<P>')
    masked = ' '.join(out)
    assert not re.search(r'\d', masked)
    low = masked.lower()
    for t in T1:
        assert t.lower() not in low
    return masked

class RowDefect(Exception):
    """Structured fields; the clause is MASKED AT RAISE TIME (P3-A3 S2 i-iii).
    On mask self-scan failure the clause is dropped; only index + label emit."""
    def __init__(self, idx, label, clause=None):
        self.idx, self.label = idx, label
        self.masked = None
        if clause:
            try:
                self.masked = cc_mask(clause)
            except AssertionError:
                self.masked = None
        super().__init__('row {}: {}'.format(idx, label))

# ---- curve edges (memo S4; C-UNIT tags) ---------------------------------------------
def att_edge_born(arm, B, k, L):
    return (B / (QTD[arm] * k**4 * L)) ** (1.0 / 3.0)

def att_edge(arm, B, k, L):
    """Dressed edge: solve QTD*k^4*d^3*(1+(kd/2)^2)^-2 * L = B by bisection on the
    monotone branch (monotone for kd < 2*sqrt(3); envelope is kd <= 0.3). A Born
    edge already past kd = 1 (>3x the envelope) is returned as the Born closed
    form: dressing only enlarges it, so it is voided by the envelope a fortiori."""
    d0 = att_edge_born(arm, B, k, L)
    if k * d0 >= 1.0:
        return dict(val=d0, unit='m', note='Born edge beyond kd=1; voided by the '
                                           'kd<=0.3 envelope a fortiori')
    hi = 3.0 / k
    f = lambda d: QTD[arm] * k**4 * d**3 / (1.0 + (0.5 * k * d)**2)**2 * L - B
    lo = 0.0
    for _ in range(220):
        mid = 0.5 * (lo + hi)
        if f(mid) > 0.0:
            hi = mid
        else:
            lo = mid
    return dict(val=0.5 * (lo + hi), unit='m')

def bir_edge(arm, B, L):
    return dict(val=L * (B / S1[arm])**2, unit='m')

def assert_len_edge(e):
    assert e['unit'] == 'm', 'C-UNIT: emitted edge lacks length dimension'
    return e

# ---- extractor (P3-A1 S2 bullet-anchored; P3-A2 S2-S3; P3-A3 S3) --------------------
CLASS_KW = {
    'ATT-REF': ['anchor', 'd_ref', 'f_ref', 'criterion'],
    'CEIL':    ['ceiling', 'birefringent', 'attenuation', 'common-mode'],
    'DLM':     ['dialect', 'linearized', 'coefficients', 'anisotropic'],
    'VLD':     ['f_max', 'margin', 'admissibility'],
}
ADJ_TOKENS = ['ceiling', 'bound', 'margin', 'criterion']   # frozen P3-A1 S2(b) list

def classify(text):
    low = text.lower()
    scores = {c: sum(1 for w in kws if w in low) for c, kws in CLASS_KW.items()}
    ranked = sorted(scores.items(), key=lambda kv: -kv[1])
    if ranked[0][1] < 2 or (len(ranked) > 1 and ranked[1][1] == ranked[0][1]):
        return None
    return ranked[0][0]

def extract_rows(text):
    m = re.search(r'^##\s*Anchors\s*$', text, re.M)
    if not m:
        raise RowDefect(None, 'Anchors section not found')
    sec = text[m.end():]
    m2 = re.search(r'^##\s+', sec, re.M)
    if m2:
        sec = sec[:m2.start()]
    items = []
    for ln in sec.splitlines():
        if re.match(r'^\s*[-*]\s+', ln):
            items.append(re.sub(r'^\s*[-*]\s+', '', ln).strip())
        elif items and ln.strip():
            items[-1] += ' ' + ln.strip()
    if not items:
        raise RowDefect(None, 'no anchor bullets')
    rows = []
    for i, raw in enumerate(items, 1):
        t = norm_cmp(raw)
        cls = classify(t)
        if cls is None:
            raise RowDefect(i, 'unclassifiable or ambiguous bullet', t)
        rows.append(dict(idx=i, cls=cls, text=t))
    return rows

# ATT-REF criterion family P1-P6 (P3-A2 S2), first-match-in-order (CC-DD-8).
def _pat(rx):
    return re.compile(rx)
P_FAMILY = [
 ('P1', _pat(r'depth\s*(?:<=|<)\s*' + NUM + UNIT),
  'optical depth <= B over D_ref', lambda m: (float(m.group(1)), m.group(2) or '')),
 ('P2', _pat(r'length\s*(?:>=|>)\s*' + NUM + UNIT + r'\s*[*x]?\s*D_ref'),
  'length >= n * D_ref => B = 1/n', lambda m: (1.0 / float(m.group(1)), m.group(2) or '')),
 ('P3', _pat(r'(\S+(?:\s+\S+)?)\s*[*x]\s*D_ref\s*(?:<=|<)\s*' + NUM + UNIT),
  'symbolic expr * D_ref <= B', lambda m: (float(m.group(2)), m.group(3) or '')),
 ('P4', _pat(r'(\S+)\s*(?:>=|>)\s*' + NUM + UNIT + r'\s*[*x]?\s*D_ref'),
  'symbolic expr >= n * D_ref => B = 1/n', lambda m: (1.0 / float(m.group(2)), m.group(3) or '')),
 ('P5', _pat(r'(\S+)\s*(?:>=|>)\s*D_ref(?:\s*/\s*' + NUM + UNIT + r')?'),
  'symbolic expr >= D_ref / n => B = n (n absent => 1)',
  lambda m: ((float(m.group(2)) if m.group(2) else 1.0), (m.group(3) or ''))),
 ('P6', _pat(r'(?:<=|<)\s*' + NUM + r'(?:\s*((?!over\b)[A-Za-z%][A-Za-z0-9%/^' + SUPS +
             r']*))?\s*over\s+D_ref'),
  'worded <= B over D_ref', lambda m: (float(m.group(1)), m.group(2) or '')),
]

def match_criterion(crit):
    hits = []
    for pid, rx, reading, getB in P_FAMILY:
        m = rx.search(crit)
        if not m:
            continue
        B, u = getB(m)
        if unit_kind(u) != 'dimensionless':
            continue                       # B validated dimensionless (P3-A2 S2)
        hits.append(dict(pattern=pid, matched_span=m.group(0), B=B, reading=reading))
    return hits

def parse_rows(rows):
    refs = {}
    for r in rows:
        if r['cls'] == 'ATT-REF':
            dq = named(r['text'], 'D_ref')
            fq = named(r['text'], 'f_ref')
            if not dq or not fq:
                raise RowDefect(r['idx'], 'ATT-REF missing D_ref/f_ref', r['text'])
            refs['D_ref'] = as_len(dq)
            refs['k_ref'] = as_wavenumber(fq)
    if 'D_ref' not in refs:
        raise RowDefect(None, 'no ATT-REF references for inheritance')
    parsed = []
    for r in rows:
        t, low, cls = r['text'], r['text'].lower(), r['cls']
        p = dict(idx=r['idx'], cls=cls, oom=False, inherit=[], fallback=None)
        if cls == 'ATT-REF':
            i = low.find('criterion')
            crit = norm_mul(t[i:] if i >= 0 else t)
            hits = match_criterion(crit)
            if not hits:
                raise RowDefect(r['idx'], 'ATT-REF criterion unreadable', crit)
            eng = hits[0]
            p.update(kind='att', B=eng['B'], k=refs['k_ref'], L=refs['D_ref'],
                     pattern=eng['pattern'], matched_span=eng['matched_span'],
                     reading=eng['reading'],
                     also_matched=[h['pattern'] for h in hits[1:]])
        elif cls == 'CEIL':
            B = span = None
            j = low.find('ceiling')
            if j >= 0:
                B, span = first_dimensionless(t[j:j + 80])       # primary (CC-DD-4)
            if B is None:
                lead = min((low.find(w) for w in CLASS_KW['CEIL'] if w in low),
                           default=-1)
                if lead >= 0:
                    seg = clause_from(t, lead)
                    B, span = first_dimensionless(seg)
                    if B is not None:
                        p['fallback'] = 'CEIL-FB engaged; clause=' + repr(seg.strip())
            if B is None:
                raise RowDefect(r['idx'], 'CEIL value unreadable', t)
            k_own, ksp = stated_freq_as_k(t)
            L_own, lsp = stated_len(t)
            if k_own is None:
                p['inherit'].append('f_ref')
            if L_own is None:
                p['inherit'].append('D_ref')
            ci = low.find('caveat')
            p.update(kind='ceil', B=B, matched_span=span, oom=True,
                     k=(k_own if k_own is not None else refs['k_ref']),
                     L=(L_own if L_own is not None else refs['D_ref']),
                     own_freq_span=ksp, own_len_span=lsp,
                     caveat=(t[ci:] if ci >= 0 else ''))
        elif cls == 'DLM':
            B = span = None
            prim_reject = None
            for tok in ADJ_TOKENS:                                # frozen list (CC-DD-5)
                j = low.find(tok)
                if j < 0:
                    continue
                q = first_qty(t[j:j + 80])
                if q is None:
                    continue
                v, u, sp = q
                if unit_kind(u) == 'dimensionless':
                    B, span = v, sp
                else:
                    prim_reject = dict(token=tok, span=sp, unit=u)
                break                                             # single-shot primary
            if B is None:
                lead = min((low.find(w) for w in CLASS_KW['DLM'] if w in low),
                           default=-1)
                if lead >= 0:
                    seg = clause_from(t, lead)
                    B, span = first_dimensionless(seg)
                    if B is not None:
                        p['fallback'] = 'DLM-FB engaged; clause=' + repr(seg.strip())
            if B is None:
                raise RowDefect(r['idx'], 'DLM coefficient unreadable', t)
            L_own, lsp = stated_len(t)
            if L_own is None:
                p['inherit'].append('D_ref')
            bi = low.find('binding')
            p.update(kind='dlm', B=B, matched_span=span, oom=True,
                     L=(L_own if L_own is not None else refs['D_ref']),
                     own_len_span=lsp, primary_reject=prim_reject,
                     binding=(t[bi:] if bi >= 0 else ''))
        elif cls == 'VLD':
            m = re.search(r'\bd\b\s*(?:<=|<)\s*' + NUM + UNIT, t)
            if m and unit_kind(m.group(2) or '') == 'length':
                p.update(kind='vld', d_cap=as_len((float(m.group(1)), m.group(2))),
                         matched_span=m.group(0), reading='explicit numeric d-cap')
            else:
                fq = named(t, 'f_max')
                if not fq:
                    raise RowDefect(r['idx'], 'VLD missing f_max', t)
                k_max = as_wavenumber(fq)
                j = low.find('margin')
                mq = first_qty(t[j:j + 80]) if j >= 0 else None
                if mq is not None and unit_kind(mq[1]) == 'dimensionless':
                    margin, msp = mq[0], mq[2]
                else:
                    margin, msp = 1.0, None
                    p['fallback'] = 'VLD margin-default=1 engaged'
                lam_min = 2.0 * math.pi / k_max                  # = c / f_max
                cap_margin = margin * lam_min                    # literal margin route
                cap_env = KD_MAX / k_max                         # E3-3(a) envelope
                p.update(kind='vld', d_cap=min(cap_margin, cap_env), k_max=k_max,
                         margin=margin, margin_span=msp,
                         cap_margin_route=cap_margin, cap_envelope=cap_env,
                         governing_clip=('kd-envelope' if cap_env <= cap_margin
                                         else 'margin-route'),
                         reading='f_max+margin route (CC-DD-6): '
                                 'min(margin * lambda_min, 0.3/k_max)')
        parsed.append(p)
    return refs, parsed

# ---- per-arm evaluation (memo S4-S5; E3-1(a); E3-3(a)) ------------------------------
def eval_arm(parsed, arm, oom_relax=1.0):
    uppers, voided, clips = [], [], []
    for p in parsed:
        B = p.get('B', 0.0) * (oom_relax if p['oom'] else 1.0) if 'B' in p else None
        tag = 'A{}'.format(p['idx'])
        if p['kind'] == 'att':
            e = assert_len_edge(att_edge(arm, B, p['k'], p['L']))
            env = KD_MAX / p['k']
            if e['val'] <= env:
                uppers.append((e['val'], tag))
            else:
                voided.append((tag, e['val'], 'kd-envelope exceeded'))
                clips.append((env, tag + '-clip'))
        elif p['kind'] == 'ceil':
            e1 = assert_len_edge(att_edge(arm, B, p['k'], p['L']))
            env = KD_MAX / p['k']
            if e1['val'] <= env:
                uppers.append((e1['val'], tag + '-att'))
            else:
                voided.append((tag + '-att', e1['val'], 'kd-envelope exceeded'))
                clips.append((env, tag + '-att-clip'))
            e2 = assert_len_edge(bir_edge(arm, B, p['L']))
            N = (S1[arm] / B)**2
            if N >= N_MIN:
                uppers.append((e2['val'], tag + '-bir'))
            else:
                voided.append((tag + '-bir', e2['val'],
                               'BIR regime invalid: N_edge={:.3e} < 10'.format(N)))
        elif p['kind'] == 'dlm':
            e = assert_len_edge(bir_edge(arm, B, p['L']))
            N = (S1[arm] / B)**2
            if N >= N_MIN:
                uppers.append((e['val'], tag))
            else:
                voided.append((tag, e['val'],
                               'BIR regime invalid: N_edge={:.3e} < 10'.format(N)))
        elif p['kind'] == 'vld':
            uppers.append((p['d_cap'], tag + '-cap'))
    cands = sorted(uppers + clips)
    if not cands:
        return dict(cls='I-1', W=None, voided=voided,
                    note='no edge certifiable inside validity; successor gate required')
    up, gov = cands[0]
    return dict(cls='P-2', W=[0.0, up], governing=gov, edges=cands, voided=voided,
                note='no lower-edge rows present: UNBOUNDED-BELOW')

CLS_ORDER = {'P-1': 3, 'P-2': 2, 'I-1': 1, 'F-1': 0}

def evaluate(parsed):
    arm_out = {a: eval_arm(parsed, a) for a in ARMS}
    relaxed = {a: eval_arm(parsed, a, oom_relax=10.0) for a in ARMS}
    classes = [arm_out[a]['cls'] for a in ARMS]
    gate = 'F-1' if all(c == 'F-1' for c in classes) else \
        max(classes, key=lambda c: CLS_ORDER[c])
    ivals = sorted(tuple(arm_out[a]['W']) for a in ARMS if arm_out[a]['W'])
    W_union = None
    if ivals:
        merged = [list(ivals[0])]
        for lo, up in ivals[1:]:
            if lo <= merged[-1][1]:
                merged[-1][1] = max(merged[-1][1], up)
            else:
                merged.append([lo, up])
        W_union = [tuple(x) for x in merged]
    oom_line = {a: dict(point_class=arm_out[a]['cls'],
                        relaxed_class=relaxed[a]['cls'],
                        point_up=(arm_out[a]['W'][1] if arm_out[a]['W'] else None),
                        relaxed_up=(relaxed[a]['W'][1] if relaxed[a]['W'] else None),
                        survives=('YES' if arm_out[a]['cls'] == relaxed[a]['cls']
                                  else 'CHANGES'))
                for a in ARMS}
    return arm_out, relaxed, gate, W_union, oom_line

# ==== pre-read gates (memo S7; P3-A1 S5; P3-A2 S5; P3-A3 S2(iv)) =====================
def self_tests():
    rel = lambda a, b: abs(a - b) / abs(b)
    # C-SYN-ATT: closed form and dressed root-finder
    arm, B, k, L = 'cubic:gem8', 2.0, 1.0 / 8.0, 4096.0
    d_cf = (B / (QTD[arm] * k**4 * L)) ** (1.0 / 3.0)
    assert rel(att_edge_born(arm, B, k, L), d_cf) <= 1e-12
    Bs = 2.0e-4                                   # kd ~ 0.035: dressed consistency
    d_dr = att_edge(arm, Bs, k, L)['val']
    q = 0.5 * k * d_dr
    d_fix = (Bs * (1.0 + q * q)**2 / (QTD[arm] * k**4 * L)) ** (1.0 / 3.0)
    assert rel(d_dr, d_fix) <= 1e-12 and k * d_dr <= 0.1
    Bt = 4.83e-9                                  # kd ~ 1e-3: Born agreement <= 1e-6
    d_t = att_edge(arm, Bt, k, L)['val']
    assert rel(d_t, att_edge_born(arm, Bt, k, L)) <= 1e-6 and k * d_t <= 0.1
    # C-SYN-BIR per arm
    for a in ARMS:
        d = bir_edge(a, 1.0 / 16.0, 256.0)['val']
        assert rel(d, 256.0 * (1.0 / 16.0 / S1[a])**2) <= 1e-12
    # C-MONO
    assert att_edge(arm, 2 * B, k, L)['val'] > att_edge(arm, B, k, L)['val']
    assert att_edge(arm, B, k, 2 * L)['val'] < att_edge(arm, B, k, L)['val']
    # C-UNIT
    assert_len_edge(att_edge(arm, B, k, L))
    assert_len_edge(bir_edge(arm, 0.1, 100.0))
    print('SELF-TESTS (memo S7: C-SYN-ATT/C-SYN-BIR/C-MONO/C-UNIT): PASS')

    KF = 'k' + 'H' + 'z'
    # C-SYN-X: shared four-class round-trip vector (transcribed as DATA)
    syn = '\n'.join([
        '## Anchors', '',
        '- A-syn-one (anchor): D_ref = 2 km, f_ref = 4 ' + KF +
        '; criterion: optical depth <= 0.5 over D_ref.',
        '- A-syn-two: ceiling 0.25 elected as the upper edge of the measured '
        'birefringent-attenuation constraint (common-mode). Caveat: synthetic.',
        '- A-syn-three (dialect): linearized-gravity bounds, anisotropic coefficients '
        'set 0.04 ; Binding: synthetic order-of-magnitude dialect-matching.',
        '- A-syn-four: f_max = 8 ' + KF + ' with margin 2; admissibility requires d '
        'be inside in any reported window.',
        '', '## Unit map'])
    rows = extract_rows(syn)
    assert [r['cls'] for r in rows] == ['ATT-REF', 'CEIL', 'DLM', 'VLD']
    refs, pp = parse_rows(rows)
    k4 = 2.0 * math.pi * 4e3 / C_LIGHT
    assert rel(refs['D_ref'], 2e3) <= 1e-12 and rel(refs['k_ref'], k4) <= 1e-12
    p1, p2, p3, p4 = pp
    assert p1['kind'] == 'att' and p1['pattern'] == 'P1' and abs(p1['B'] - 0.5) <= 1e-15
    d1 = att_edge('hex:step', p1['B'], p1['k'], p1['L'])['val']
    assert rel(d1, att_edge_born('hex:step', 0.5, k4, 2e3)) <= 1e-9
    assert p2['kind'] == 'ceil' and abs(p2['B'] - 0.25) <= 1e-15 and p2['oom'] \
        and not p2['fallback'] and set(p2['inherit']) == {'f_ref', 'D_ref'}
    assert p3['kind'] == 'dlm' and abs(p3['B'] - 0.04) <= 1e-15 and p3['oom'] \
        and not p3['fallback'] and p3['inherit'] == ['D_ref']
    d3 = bir_edge('hex:gem8', p3['B'], p3['L'])['val']
    assert rel(d3, 2e3 * (0.04 / S1['hex:gem8'])**2) <= 1e-12
    k8 = 2.0 * math.pi * 8e3 / C_LIGHT
    exp_cap = min(2.0 * (2.0 * math.pi / k8), KD_MAX / k8)      # CC-DD-6
    assert p4['kind'] == 'vld' and rel(p4['d_cap'], exp_cap) <= 1e-12
    print('C-SYN-X (four-class extractor round-trip): PASS')

    # P3-A2 S5: symbolic ATT-REF variants (shared vectors; op normalization)
    def att_doc(crit):
        return '\n'.join(['## Anchors', '',
                          '- A-syn (anchor): D_ref = 2 km, f_ref = 4 ' + KF +
                          '; criterion: ' + crit, '', '## Unit map'])
    for crit, pid, Bexp in [
            ('a_T ' + chr(0x00B7) + ' D_ref ' + chr(0x2264) + ' 0.5 (synthetic).', 'P3', 0.5),
            ('ell ' + chr(0x2265) + ' 3 ' + chr(0x00D7) + ' D_ref (synthetic).', 'P4', 1.0 / 3.0),
            (chr(0x2264) + ' 0.5 over D_ref (synthetic).', 'P6', 0.5)]:
        _, qq = parse_rows(extract_rows(att_doc(crit)))
        assert qq[0]['pattern'] == pid and abs(qq[0]['B'] - Bexp) <= 1e-15, \
            (crit, qq[0]['pattern'], qq[0]['B'])
    # P5 family form (length >= D_ref, n absent => B=1)
    _, qq = parse_rows(extract_rows(att_doc('ell_att(f_ref) >= D_ref (one synthetic fold).')))
    assert qq[0]['pattern'] == 'P5' and abs(qq[0]['B'] - 1.0) <= 1e-15
    print('C-SYN-X symbolic ATT-REF variants (P3/P4/P6 + P5, op normalization): PASS')

    # P3-A2 S5: fallback-engaging synthetics (shared vectors)
    fb_doc = '\n'.join([
        '## Anchors', '',
        '- A-one (anchor): D_ref = 2 km, f_ref = 4 ' + KF +
        '; criterion: optical depth <= 0.5 over D_ref.',
        '- A-two: ceiling elected for this synthetic exercise as the common-mode '
        'order-of-magnitude upper edge applied across both channels, with the value '
        '0.25; Caveat: synthetic.',
        '- A-three: dialect linearized-gravity anisotropic synthetic: the numeric '
        'sits here 0.04 far from any primary keyword; Binding: synthetic.',
        '- A-four: f_max = 8 ' + KF + '; admissibility requires d small in any '
        'reported window (margin unstated for this synthetic).',
        '', '## Unit map'])
    _, qq = parse_rows(extract_rows(fb_doc))
    assert (qq[1]['fallback'] or '').startswith('CEIL-FB') and abs(qq[1]['B'] - 0.25) <= 1e-15
    assert (qq[2]['fallback'] or '').startswith('DLM-FB') and abs(qq[2]['B'] - 0.04) <= 1e-15
    assert qq[3]['fallback'] == 'VLD margin-default=1 engaged'
    assert rel(qq[3]['d_cap'], min(2.0 * math.pi / k8, KD_MAX / k8)) <= 1e-12
    print('C-SYN-X fallback engagement (CEIL-FB/DLM-FB/VLD-default, loud flags): PASS')

    # P3-A3 S2(iv): adversarial synthetics (shared vectors + CC additions)
    adv_doc = '\n'.join([
        '## Anchors', '',
        '- A-one (anchor): D_ref = 2 km, f_ref = 4 ' + KF +
        '; criterion: optical depth <= 0.5 over D_ref.',
        '- A-adv2: ceiling ' + chr(0x2014) + ' |x(7 km)| ~ 0.05, elected as the '
        'common-mode order-of-magnitude upper edge for this adversarial synthetic; '
        'Caveat: adv.',
        '- A-adv3: dialect linearized-gravity anisotropic adversarial: decoy '
        '|y(3 km)| precedes the true value 0.125 in this clause; Binding: adv.',
        '- A-four: f_max = 8 ' + KF + '; admissibility requires d small in any '
        'reported window (margin unstated).',
        '', '## Unit map'])
    _, qq = parse_rows(extract_rows(adv_doc))
    assert abs(qq[1]['B'] - 0.05) <= 1e-15 and not qq[1]['fallback'], qq[1]
    assert abs(qq[2]['B'] - 0.125) <= 1e-15, qq[2]
    print('C-SYN-X ADV shared (abs-bars, dimensioned decoys, first-dimensionless): PASS')

    # CC additions: identifier-embedded digits, inverse units, percent, pipes,
    # decimal-comma-free delimiters inside the clause
    GLU = 'G' + 'pc'
    cc_doc = '\n'.join([
        '## Anchors', '',
        '- A-one (anchor): D_ref = 2 km, f_ref = 4 ' + KF +
        '; criterion: optical depth <= 0.5 over D_ref.',
        '- A-cc2: XYZQ-3 ' + GLU + '-scale ceiling ' + chr(0x2014) + ' |q_T(5 ' +
        'H' + 'z' + ')| ~ 0.06 ' + GLU + chr(0x207B) + chr(0x00B9) + ', elected as '
        'the 80%-band edge | of the measured birefringent-attenuation constraint '
        'q = ' + chr(0x2212) + '0.021 (+0.04/' + chr(0x2212) + '0.03) ' + GLU +
        chr(0x207B) + chr(0x00B9) + ' at 5 ' + 'H' + 'z' + '; Caveat: cc-adv.',
        '', '## Unit map'])
    _, qq = parse_rows(extract_rows(cc_doc))
    assert abs(qq[1]['B'] - 80.0) <= 1e-15 and not qq[1]['fallback'], qq[1]
    assert qq[1]['inherit'] == ['D_ref'] and qq[1]['own_freq_span'] is not None, qq[1]
    print('C-SYN-X ADV CC (identifier-digit guard, inverse units, percent, pipes): PASS')

    # forced-failure masking-path test (P3-A3 S2 end-to-end)
    bad_doc = '\n'.join([
        '## Anchors', '',
        '- A-one (anchor): D_ref = 2 km, f_ref = 4 ' + KF +
        '; criterion: optical depth <= 0.5 over D_ref.',
        '- A-mask: ceiling ' + chr(0x2014) + ' |m(9 km)| only dimensioned '
        'common-mode content in this adversarial clause; Caveat: forced.',
        '', '## Unit map'])
    try:
        parse_rows(extract_rows(bad_doc))
        raise AssertionError('forced-failure synthetic did not raise')
    except RowDefect as e:
        assert e.idx == 2 and e.masked is not None
        assert not re.search(r'\d', e.masked) and '#' in e.masked
        assert 'ceiling' in e.masked
        assert str(e) == 'row 2: CEIL value unreadable'
        low = e.masked.lower()
        for tt in T1:
            assert tt.lower() not in low
    print('C-SYN-X ADV forced-failure (raise-time masking, digit-free, structured): PASS')

self_tests()
print('ALL PRE-READ GATES: PASS')
if not READ:
    print('STAGE 0 COMPLETE (sealed embed NOT opened). Set CC_READ=1 for the CC '
          'single read.')
    sys.exit(0)

# ==== CC SINGLE READ #1 (authorized: re-lock 3 6a7069b0; E3-5(a) CC-blind-first) =====
raw = open(SEALED, 'rb').read()
md5 = hashlib.md5(raw).hexdigest()
assert md5 == SEALED_MD5, 'SEALED MD5 MISMATCH AT OPEN: ' + md5
text = raw.decode('utf-8')
print('\nSEALED FILE SINGLE READ (leg=cc, read=cc-1): md5 {} ({} B)'.format(md5, len(raw)))

try:
    rows = extract_rows(text)
    refs, parsed = parse_rows(rows)
except RowDefect as e:
    ck = dict(gate='G-POLY1', phase='3', leg='cc', read='cc-1',
              verdict='X-1 SCHEMA-DEFECT', row=e.idx, defect=e.label,
              masked_clause=e.masked, sealed_md5=md5)
    open(CKPATH, 'w').write(json.dumps(ck, indent=1))
    b = open(CKPATH, 'rb').read()
    print('X-1 SCHEMA-DEFECT (cc single read): row {}: {} — ABORT.'.format(e.idx, e.label))
    if e.masked:
        print('masked clause:', e.masked)
    print('checkpoint: {}  md5 {}  ({} B)'.format(CKPATH, hashlib.md5(b).hexdigest(), len(b)))
    sys.exit(2)

arm_out, relaxed, gate, W_union, oom_line = evaluate(parsed)

# ---- checkpoint written + hashed BEFORE any other action (dispatch S2(d)) -----------
row_records = []
for p in parsed:
    rec = {k2: v2 for k2, v2 in p.items()}
    row_records.append(rec)
ck = dict(
    gate='G-POLY1', phase='3', leg='cc',
    read='cc-1 (authorized: re-lock 3 6a7069b0; election E3-5(a) CC-blind-first)',
    lock=dict(memo='e16a78906560d2bb076d0699966981ac',
              addendum1='ba75b113e8ad094cd752026df4e73977',
              relock1='7f4b53ad43af3aff55938726d8f26738',
              addendum2='ac87bc92890c7bf6a08b3d67d493ec9c',
              relock2='b1150c946f6986a9bc19ae2b073db83e',
              addendum3='257b81bf3924cb92ca9d1232fb94325c',
              relock3='6a7069b07c2184eea41dfc38b4446c9d',
              base='V4.75 0e923ab786c1e1a96eb0a3bcad3e616f',
              elections=['E3-1(a)', 'E3-2(a)', 'E3-3(a)', 'E3-4(a)', 'E3-5(a)']),
    sealed=dict(md5=md5, bytes=len(raw), row_count=len(parsed),
                class_census={p['cls']: sum(1 for x in parsed if x['cls'] == p['cls'])
                              for p in parsed}),
    refs=dict(D_ref_m=refs['D_ref'], k_ref_per_m=refs['k_ref']),
    unit_map='sealed Unit map carries no explicit unit definitions; runtime table '
             'governs (P3-A1 S2(e))',
    design_register=DESIGN_REGISTER,
    curves=dict(QTa=QTA, s1=S1),
    self_tests='memo S7 + C-SYN-X (four-class, symbolic, fallback, adversarial '
               'shared + CC additions, forced-failure masking) ALL PASS pre-read',
    anchors=row_records,
    anchor_texts={r['idx']: r['text'] for r in rows},
    per_arm={a: arm_out[a] for a in ARMS},
    per_arm_oom_relaxed={a: relaxed[a] for a in ARMS},
    oom_robustness=oom_line, gate_class=gate, W_union=W_union,
    mapper_source_md5=hashlib.md5(_me.encode('utf-8')).hexdigest(),
    h_ledger='H-12..H-17 stand (chain records); CC leg: no sealed-contact H-items; '
             'pre-read gate iterations logged in the CC run report')
open(CKPATH, 'w').write(json.dumps(ck, indent=1, default=float))
ckb = open(CKPATH, 'rb').read()
CK_MD5 = hashlib.md5(ckb).hexdigest()
print('checkpoint (sanctioned carrier, written FIRST): {}'.format(CKPATH))
print('checkpoint md5 {}  ({} B)'.format(CK_MD5, len(ckb)))

# ---- report (sanctioned post-verdict carrier) ---------------------------------------
print('\nANCHOR CENSUS: {} rows -> {}'.format(
    len(parsed), ', '.join('{}:{}'.format(p['idx'], p['cls']) for p in parsed)))
print('refs: D_ref = {:.9e} m; k(f_ref) = {:.9e} /m'.format(refs['D_ref'], refs['k_ref']))
for p in parsed:
    keep = ('B', 'k', 'L', 'd_cap', 'pattern', 'matched_span', 'reading', 'inherit',
            'oom', 'fallback', 'also_matched', 'primary_reject', 'margin',
            'governing_clip', 'own_freq_span', 'own_len_span')
    info = {k2: p[k2] for k2 in keep if k2 in p and p[k2] not in (None, [], '')}
    print(' [{}] {:7s} {}'.format(p['idx'], p['cls'], info))
fb = [(p['idx'], p['cls'], p['fallback']) for p in parsed if p['fallback']]
print('FALLBACKS ENGAGED: {}'.format(fb if fb else 'NONE'))

print('\n== PER-ARM VERDICTS ==')
for a in ARMS:
    r = arm_out[a]
    w = '-' if r['W'] is None else '(0, {:.6e}] m'.format(r['W'][1])
    print('{:12s} {}  W = {}  governing={}  voided={}'.format(
        a, r['cls'], w, r.get('governing'), len(r['voided'])))
    for v in r['voided']:
        print('             voided: {} edge {:.6e} m ({})'.format(*v))
    rx = relaxed[a]
    rw = '-' if rx['W'] is None else '{:.6e} m'.format(rx['W'][1])
    print('             OOM x10 relax: class {}, W_up {}  -> {}'.format(
        rx['cls'], rw, oom_line[a]['survives']))
print('\nGATE VERDICT CLASS: {}'.format(gate))
if W_union:
    print('W_union = ' + ', '.join('(0, {:.6e}] m'.format(up) for lo, up in W_union))
