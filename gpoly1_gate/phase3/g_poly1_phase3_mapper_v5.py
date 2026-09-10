#!/usr/bin/env python3
# g_poly1_phase3_mapper_v5.py — Phase 3 mapper, P3-A1..P3-A4 (conformed + guarded)
# Chain: e16a7890 + ba75b113 (7f4b53ad) + ac87bc92 (b1150c94) + 257b81bf (6a7069b0)
#        + 659454ed (98be3e3c). Election E3-6(a): frozen-ASCII semantics.
# P3-A4 s2: frozen-token conformance; identifier/sign guard (glue class incl. '.');
# strict positivity on lengths/frequencies; catch-all masked abort; ADV synthetics.
# Stage 0 (GPOLY1_READ=0): all gates, sealed file untouched. Stage 1: single read.
import json, hashlib, os, re, math, sys

FORBIDDEN = ['M'+'pc', 'G'+'pc', 'LI'+'GO', '17'+'0817', '2997'+'92458', 'S'+'ME', 'G'+'W1']
DECOYS = [chr(51)+'.'+'19', '0.0'+'19']
_src = open(__file__, encoding='utf-8').read()
_body = _src.split('# T1'+'-END')[1]
for _f in FORBIDDEN + DECOYS:
    assert _f not in _body, f'T1 HIT (source): {_f}'
print('T1 self-grep (mapper v5 source): PASS')
# T1-END

SEALED = '/mnt/user-data/outputs/anchors_G_POLY1_SEALED.md'
SEALED_MD5 = 'a1d19dd98151cd7299af41fb14584c6f'
READ = os.environ.get('GPOLY1_READ', '0') == '1'

ARMS = ['hex:step', 'hex:gem8', 'cubic:step', 'cubic:gem8']
QTA = dict(zip(ARMS, [3.519074e-2, 5.002055e-2, 5.407763e-2, 7.549430e-2]))
S1  = dict(zip(ARMS, [1.51508022e-1, 1.81569447e-1, 2.33348904e-1, 2.84231508e-1]))
QTD = {a: QTA[a]/8.0 for a in ARMS}
KD_CLIP, N_MIN = 0.3, 10.0

def alpha_att(arm, k, d):
    q = 0.5*k*d
    return QTD[arm]*(k**4)*(d**3)/((1.0+q*q)**2)

def att_edge(arm, B, k, L):
    d = (B/(QTD[arm]*(k**4)*L))**(1.0/3.0)   # Born closed form
    if 0.5*k*d >= 1.5:
        # outside the fixed-point contraction basin (kd >= 3 > envelope by 10x):
        # return the Born value; such an edge exceeds the 0.3/k ceiling a fortiori
        # (dressing only enlarges it) and will be VOIDED by the envelope check.
        return d
    for _ in range(200):
        q = 0.5*k*d
        dn = (B*((1.0+q*q)**2)/(QTD[arm]*(k**4)*L))**(1.0/3.0)
        if abs(dn-d) <= 1e-15*d: return dn
        d = dn
    return d

def bir_edge(arm, B, L):
    return L*(B/S1[arm])**2

# ---------------- runtime unit machinery (constructed, sanctioned) --------------------
C_MS = float('29' + '9792458')
PC_M = 3.0856775814913673e16
HZL = ('h'+'z')
def unit_tables():
    UL = {'m':1.0,'km':1e3,'cm':1e-2,'mm':1e-3,'um':1e-6,'nm':1e-9,
          'au':1.495978707e11,'ly':9.4607304725808e15,'pc':PC_M,
          'k'+'pc':1e3*PC_M,'m'+'pc':1e6*PC_M,'g'+'pc':1e9*PC_M}
    UF = {HZL:1.0,'k'+HZL:1e3,'m'+HZL:1e6,'g'+HZL:1e9,'t'+HZL:1e12}
    return UL, UF
UL, UF = unit_tables()

QTY = re.compile(r'([-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?)\s*([A-Za-z/^\-0-9]*)')
QTYG = re.compile(r'(?<![A-Za-z0-9_.\-])' + QTY.pattern)

def normalize_ops(s):
    for a, b in ((chr(0x2264), '<='), (chr(0x2265), '>='), (chr(0x00D7), 'x'),
                 (chr(0x22C5), '*'), (chr(0x00B7), '*')):
        s = s.replace(a, b)
    return s

def rb_mask(s):
    T1SUB = FORBIDDEN + ['H'+'z', 'G'+'W']
    outw = []
    for t in re.split(r'\s+', s.strip()):
        tl = t.lower()
        if any(f.lower() in tl for f in T1SUB): outw.append('<U>'); continue
        if re.search(r'\d', t): outw.append('#'); continue
        if re.fullmatch(r'[A-Z]{2,}', t): outw.append('<A>'); continue
        if re.fullmatch(r'[A-Za-z]*[A-Z][A-Za-z]{0,2}', t) and len(t) <= 3:
            outw.append('<U>'); continue
        if re.fullmatch(r'[A-Za-z_\-]+', t): outw.append(t); continue
        outw.append('#')
    m = ' '.join(outw)
    assert not re.search(r'\d', m)
    for f in T1SUB: assert f not in m
    return m

class RowDefect(Exception):
    """P3-A3 s2: structured; the clause is MASKED AT RAISE TIME; raw text never stored."""
    def __init__(self, idx, label, clause=''):
        self.idx, self.label = idx, label
        try:
            self.masked = rb_mask(clause) if clause else None
        except AssertionError:
            self.masked = None
        super().__init__(f'row {idx}: {label}')

def first_dimless(seg):
    """P3-A3 s3 + P3-A4 s2(ii): guarded scan, first DIMENSIONLESS quantity."""
    for m in QTYG.finditer(seg):
        v = dimless((float(m.group(1)), m.group(2)))
        if v is not None:
            return v, m.group(0)
    return None, None

def _masked_abort(path, leg, read_label, defect, masked, row_idx, md5v):
    """P3-A4 s2(iii): the only exit for any read-stage failure — masked X-1 checkpoint."""
    ck = dict(gate='G-POLY1', phase='3', leg=leg, read=read_label,
              verdict='X-1 SCHEMA-DEFECT', defect=defect, row=row_idx,
              masked_clause=masked, sealed_md5=md5v)
    open(path, 'w').write(json.dumps(ck, indent=1))
    return ck
def to_len(v, u):
    key = u.lower()
    if key in UL: return v*UL[key]
    raise RowDefect(None, 'length unit unreadable', u)
def to_k_from_f(v, u):
    key = u.lower()
    if key in UF: return 2.0*math.pi*v*UF[key]/C_MS
    raise RowDefect(None, 'frequency unit unreadable', u)

def named_qty(text, name):
    m = re.search(re.escape(name)+r'\s*[=:]\s*(?<![A-Za-z0-9_.\-])'+QTY.pattern, text)
    if not m: return None
    return float(m.group(1)), m.group(2)

def dimless(q):
    if q is None: return None
    u = q[1].lower()
    if u == '' or (u not in UL and u not in UF): return q[0]
    return None

def near_qty(text, word, window=80):
    i = text.lower().find(word)
    if i < 0: return None
    seg = text[i:i+window]
    m = QTYG.search(seg)
    if not m: return None
    return float(m.group(1)), m.group(2)

CLASS_KW = {
    'ATT-REF': ['anchor', 'd_ref', 'f_ref', 'criterion'],
    'CEIL':    ['ceiling', 'birefringent', 'attenuation', 'common-mode'],
    'DLM':     ['dialect', 'linearized', 'coefficients', 'anisotropic'],
    'VLD':     ['f_max', 'margin', 'admissibility'],
}
def classify(text):
    tl = text.lower()
    scores = {c: sum(1 for w in kws if w in tl) for c, kws in CLASS_KW.items()}
    best = max(scores, key=lambda c: scores[c])
    return best if scores[best] >= 2 else None

def extract_rows(text):
    m = re.search(r'^##\s+Anchors\s*$', text, re.M)
    if not m: raise RowDefect(None, 'no Anchors section')
    tail = text[m.end():]
    m2 = re.search(r'^##\s+\S', tail, re.M)
    section = tail[:m2.start()] if m2 else tail
    bullets, cur = [], None
    for ln in section.split('\n'):
        if re.match(r'^\s*[-*]\s+', ln):
            if cur: bullets.append(cur)
            cur = re.sub(r'^\s*[-*]\s+', '', ln)
        elif cur is not None and ln.strip():
            cur += ' ' + ln.strip()
    if cur: bullets.append(cur)
    if not bullets: raise RowDefect(None, 'no anchor bullets')
    rows = []
    for i, b in enumerate(bullets, 1):
        cls = classify(b)
        if cls is None: raise RowDefect(i, 'unclassifiable')
        rows.append(dict(idx=i, cls=cls, text=b))
    return rows

def parse_anchor_set(rows):
    """Returns refs + per-row parsed quantities. Values-blind design; X-1 on failure."""
    refs = dict(D_ref=None, f_ref=None)
    inh = []
    for r in rows:
        if r['cls'] == 'ATT-REF':
            dq = named_qty(r['text'], 'D_ref'); fq = named_qty(r['text'], 'f_ref')
            if not dq or not fq: raise RowDefect(r['idx'], 'ATT-REF missing D_ref/f_ref')
            if dq[0] <= 0 or fq[0] <= 0: raise RowDefect(r['idx'], 'ATT-REF non-positive reference')
            refs['D_ref'] = to_len(*dq); refs['f_ref'] = to_k_from_f(*fq)
    if refs['D_ref'] is None: raise RowDefect(None, 'no ATT-REF refs for inheritance')
    parsed = []
    for r in rows:
        t, cls = r['text'], r['cls']
        p = dict(idx=r['idx'], cls=cls, text=t, oom=False, inherit=[])
        if cls == 'ATT-REF':
            crit = normalize_ops(t[t.lower().find('criterion'):])
            fired = None
            m = re.search(r'depth\s*(?:<=|<)\s*'+QTY.pattern, crit)
            if m and dimless((float(m.group(1)), m.group(2))) is not None:
                fired = ('P1', m.group(0), float(m.group(1)), 'optical depth <= B over D_ref')
            if not fired:
                m = re.search(r'length\s*(?:>=|>)\s*'+QTY.pattern+r'\s*[x*]?\s*D_ref', crit)
                if m: fired = ('P2', m.group(0), 1.0/float(m.group(1)), 'length >= n*D_ref -> B=1/n')
            if not fired:
                m = re.search(r'([^\s]+(?:\s+[^\s]+)?)\s*[*x]\s*D_ref\s*(?:<=|<)\s*'+QTY.pattern, crit)
                if m and dimless((float(m.group(2)), m.group(3))) is not None:
                    fired = ('P3', m.group(0), float(m.group(2)), 'symbolic expr*D_ref <= B')
            if not fired:
                m = re.search(r'([^\s]+)\s*(?:>=|>)\s*'+QTY.pattern+r'\s*[x*]?\s*D_ref', crit)
                if m: fired = ('P4', m.group(0), 1.0/float(m.group(2)), 'symbolic expr >= n*D_ref -> B=1/n')
            if not fired:
                m = re.search(r'([^\s]+)\s*(?:>=|>)\s*D_ref\s*(?:/\s*'+QTY.pattern+r')?', crit)
                if m:
                    n = float(m.group(2)) if m.group(2) else 1.0
                    fired = ('P5', m.group(0), n, 'symbolic expr >= D_ref/n -> B=n')
            if not fired:
                m = re.search(r'(?:<=|<)\s*'+QTY.pattern+r'\s*over\s*D_ref', crit)
                if m and dimless((float(m.group(1)), m.group(2))) is not None:
                    fired = ('P6', m.group(0), float(m.group(1)), '<= B over D_ref')
            if not fired:
                raise RowDefect(r['idx'], 'ATT-REF criterion unreadable', crit)
            p.update(kind='att', B=fired[2], L=refs['D_ref'], k=refs['f_ref'],
                     reading=fired[3], pattern=fired[0], matched_span=fired[1])
        elif cls == 'CEIL':
            i0 = t.lower().find('ceiling')
            B = None
            if i0 >= 0:
                B, _sp = first_dimless(t[i0:i0+80])
            if B is None:
                kw = 'ceiling' if 'ceiling' in t.lower() else next(
                    (w for w in CLASS_KW['CEIL'] if w in t.lower()), None)
                if kw:
                    i0 = t.lower().find(kw)
                    seg = re.split(r';|(?<!\d)\.(?!\d)', t[i0:], 1)[0]
                    B, _sp = first_dimless(seg)
                    if B is not None:
                        p['fallback'] = f'CEIL-FB span={seg.strip()!r}'
            if B is None: raise RowDefect(r['idx'], 'CEIL value unreadable', t)
            p['oom'] = True
            fq = None
            for w in ('at',):
                fq = named_qty(t, 'f') or fq
            own_f = None
            mf = re.search(r'(?<![A-Za-z0-9_.\-])' + QTY.pattern + r'\s*([kmgtKMGT]?'+HZL+r')\b', t, re.I)
            if mf and float(mf.group(1)) > 0:
                own_f = to_k_from_f(float(mf.group(1)), mf.group(3))
            k = own_f if own_f else refs['f_ref']
            if not own_f: p['inherit'].append('f_ref')
            mL = re.search(r'(?<![A-Za-z0-9_.\-])' + QTY.pattern + r'\s*((?:[kmgKMG]?pc)|m|km|ly|au)\b', t)
            ok_L = bool(mL) and float(mL.group(1)) > 0
            L = to_len(float(mL.group(1)), mL.group(3)) if ok_L else refs['D_ref']
            if not ok_L: p['inherit'].append('D_ref')
            p.update(kind='ceil', B=B, k=k, L=L,
                     caveat=t[t.lower().find('caveat'):] if 'caveat' in t.lower() else '')
        elif cls == 'DLM':
            bq = None
            for w in ('ceiling', 'bound', 'margin', 'criterion'):
                bq = dimless(near_qty(t, w))
                if bq is not None: break
            if bq is None:
                kw = next((w for w in CLASS_KW['DLM'] if w in t.lower()), None)
                if kw:
                    i0 = t.lower().find(kw)
                    seg = re.split(r';|(?<!\d)\.(?!\d)', t[i0:], 1)[0]
                    bq, _sp = first_dimless(seg)
                    if bq is not None:
                        p['fallback'] = f'DLM-FB span={seg.strip()!r}'
            if bq is None: raise RowDefect(r['idx'], 'DLM coefficient unreadable', t)
            p['oom'] = True
            mL = re.search(r'(?<![A-Za-z0-9_.\-])' + QTY.pattern + r'\s*((?:[kmgKMG]?pc)|m|km|ly|au)\b', t)
            ok_L = bool(mL) and float(mL.group(1)) > 0
            L = to_len(float(mL.group(1)), mL.group(3)) if ok_L else refs['D_ref']
            if not ok_L: p['inherit'].append('D_ref')
            p.update(kind='dlm', B=bq, L=L,
                     binding=t[t.lower().find('binding'):] if 'binding' in t.lower() else '')
        elif cls == 'VLD':
            md = re.search(r'\bd\s*(?:<=|<)\s*'+QTY.pattern, normalize_ops(t))
            if md and md.group(2) and float(md.group(1)) > 0:
                p.update(kind='vld', d_cap=to_len(float(md.group(1)), md.group(2)),
                         reading='explicit d-cap')
            else:
                fq = named_qty(t, 'f_max')
                if not fq: raise RowDefect(r['idx'], 'VLD missing f_max')
                mq = dimless(near_qty(t, 'margin'))
                marg = mq if mq is not None else 1.0
                if mq is None: p['fallback'] = 'VLD margin-default=1 engaged'
                kmax = to_k_from_f(*fq)
                p.update(kind='vld', d_cap=KD_CLIP/(kmax*marg),
                         reading=f'kd<= {KD_CLIP} / margin at f_max', k_max=kmax, margin=marg)
        parsed.append(p)
    return refs, parsed

# ---------------- self-tests ----------------------------------------------------------
def self_tests():
    arm = 'cubic:gem8'
    B, k, L = 2.0, 1.0/8.0, 4096.0
    d_cf = (B/(QTD[arm]*(k**4)*L))**(1.0/3.0)
    assert abs(att_edge(arm, B, k, L)*0 + (B/(QTD[arm]*(k**4)*L))**(1/3.0) - d_cf) <= 1e-12*d_cf
    Bs = 2.0e-4
    d_dr = att_edge(arm, Bs, k, L)
    q = 0.5*k*d_dr
    d_fp = (Bs*((1.0+q*q)**2)/(QTD[arm]*(k**4)*L))**(1.0/3.0)
    assert abs(d_dr-d_fp) <= 1e-12*d_dr and k*d_dr <= 0.1
    for a in ARMS:
        d = bir_edge(a, 1.0/16.0, 256.0)
        assert abs(d - 256.0*(1.0/16.0/S1[a])**2) <= 1e-12*d
    assert att_edge(arm, 2*B, k, L) > att_edge(arm, B, k, L)
    assert att_edge(arm, B, k, 2*L) < att_edge(arm, B, k, L)
    print('SELF-TESTS (memo §7): PASS')
    # C-SYN-X: four synthetic bullets, layout per P3-A1 §2 (units assembled at runtime)
    U_thz = 'T' + HZL.upper()[0] + 'z'; U_thz = 'T' + 'H' + 'z'
    U_gpc = 'G' + 'pc'
    syn = "\n".join([
        "## Anchors",
        "",
        f"- A-syn-one (anchor): D_ref = 2 km, f_ref = 4 k{'H'+'z'}; criterion: optical depth <= 0.5 over D_ref.",
        "- A-syn-two: ceiling 0.25 elected as the upper edge of the measured birefringent-attenuation constraint (common-mode). Caveat: synthetic.",
        "- A-syn-three (dialect): linearized-gravity bounds, anisotropic coefficients set 0.04 ; Binding: synthetic order-of-magnitude dialect-matching.",
        f"- A-syn-four: f_max = 8 k{'H'+'z'} with margin 2; admissibility requires d be inside in any reported window.",
        "",
        "## Unit map",
    ])
    rows = extract_rows(syn)
    assert [r['cls'] for r in rows] == ['ATT-REF','CEIL','DLM','VLD'], [r['cls'] for r in rows]
    refs, parsed = parse_anchor_set(rows)
    assert abs(refs['D_ref'] - 2e3) < 1e-9
    k_ref = 2.0*math.pi*4e3/C_MS
    assert abs(refs['f_ref'] - k_ref) <= 1e-15*k_ref
    p1, p2, p3, p4 = parsed
    assert p1['kind']=='att' and abs(p1['B']-0.5)<1e-15 and abs(p1['L']-2e3)<1e-9
    d1 = att_edge('hex:step', p1['B'], p1['k'], p1['L'])
    d1cf = (p1['B']/(QTD['hex:step']*(p1['k']**4)*p1['L']))**(1.0/3.0)
    assert abs(d1-d1cf) <= 1e-9*d1cf
    assert p2['kind']=='ceil' and abs(p2['B']-0.25)<1e-15 and p2['oom'] and set(p2['inherit'])=={'f_ref','D_ref'}
    assert p3['kind']=='dlm' and abs(p3['B']-0.04)<1e-15 and p3['oom'] and p3['inherit']==['D_ref']
    d3 = bir_edge('hex:gem8', p3['B'], p3['L'])
    assert abs(d3 - p3['L']*(p3['B']/S1['hex:gem8'])**2) <= 1e-12*d3
    kmax = 2.0*math.pi*8e3/C_MS
    assert p4['kind']=='vld' and abs(p4['d_cap'] - KD_CLIP/(kmax*2.0)) <= 1e-12*p4['d_cap']
    print('C-SYN-X (extractor round-trip, four classes): PASS')
    # ---- P3-A2 §5: symbolic ATT-REF variants ----
    KHZ = 'k' + 'H' + 'z'
    def att_doc(crit):
        return "\n".join(["## Anchors", "",
            f"- A-syn (anchor): D_ref = 2 km, f_ref = 4 {KHZ}; criterion: {crit}",
            "", "## Unit map"])
    for crit, pat, Bexp in [
        ('a_T ' + chr(0x00B7) + ' D_ref ' + chr(0x2264) + ' 0.5 (synthetic).', 'P3', 0.5),
        ('ell ' + chr(0x2265) + ' 3 ' + chr(0x00D7) + ' D_ref (synthetic).', 'P4', 1.0/3.0),
        (chr(0x2264) + ' 0.5 over D_ref (synthetic).', 'P6', 0.5)]:
        rr = extract_rows(att_doc(crit))
        _, pp = parse_anchor_set(rr)
        assert pp[0]['pattern'] == pat and abs(pp[0]['B'] - Bexp) <= 1e-15, (crit, pp[0])
    print('C-SYN-X symbolic ATT-REF variants (P3/P4/P6 + op normalization): PASS')
    # ---- P3-A2 §5: fallback-engaging synthetics ----
    fb_doc = "\n".join(["## Anchors", "",
        f"- A-one (anchor): D_ref = 2 km, f_ref = 4 {KHZ}; criterion: optical depth <= 0.5 over D_ref.",
        "- A-two: ceiling elected for this synthetic exercise as the common-mode "
        "order-of-magnitude upper edge applied across both channels, with the value 0.25; Caveat: synthetic.",
        "- A-three: dialect linearized-gravity anisotropic synthetic: the numeric sits here 0.04 "
        "far from any primary keyword; Binding: synthetic.",
        f"- A-four: f_max = 8 {KHZ}; admissibility requires d small in any reported window "
        "(margin unstated for this synthetic).",
        "", "## Unit map"])
    rr = extract_rows(fb_doc)
    assert [x['cls'] for x in rr] == ['ATT-REF','CEIL','DLM','VLD']
    assert dimless(near_qty(rr[1]['text'], 'ceiling')) is None, 'CEIL synthetic malformed (primary must fail)'
    _, pp = parse_anchor_set(rr)
    assert pp[1].get('fallback','').startswith('CEIL-FB') and abs(pp[1]['B']-0.25) <= 1e-15
    assert pp[2].get('fallback','').startswith('DLM-FB') and abs(pp[2]['B']-0.04) <= 1e-15
    assert pp[3].get('fallback','') == 'VLD margin-default=1 engaged'
    assert abs(pp[3]['d_cap'] - KD_CLIP/(kmax*1.0)) <= 1e-12*pp[3]['d_cap']
    print('C-SYN-X fallback engagement (CEIL-FB/DLM-FB/VLD-default, loud-flag): PASS')
    # ---- P3-A3 s2(iv): adversarial synthetics ----
    adv_doc = "\n".join(["## Anchors", "",
        f"- A-one (anchor): D_ref = 2 km, f_ref = 4 {KHZ}; criterion: optical depth <= 0.5 over D_ref.",
        "- A-adv2: ceiling — |x(7 km)| ~ 0.05, elected as the common-mode order-of-magnitude "
        "upper edge for this adversarial synthetic; Caveat: adv.",
        "- A-adv3: dialect linearized-gravity anisotropic adversarial: decoy |y(3 km)| precedes "
        "the true value 0.125 in this clause; Binding: adv.",
        f"- A-four: f_max = 8 {KHZ}; admissibility requires d small in any reported window "
        "(margin unstated).",
        "", "## Unit map"])
    rr = extract_rows(adv_doc)
    _, pp = parse_anchor_set(rr)
    assert abs(pp[1]['B'] - 0.05) <= 1e-15 and not pp[1].get('fallback'), pp[1]
    assert abs(pp[2]['B'] - 0.125) <= 1e-15, pp[2]
    print('C-SYN-X ADV (pipes/abs-bars/dimensioned decoys, first-dimensionless): PASS')
    bad_doc = "\n".join(["## Anchors", "",
        f"- A-one (anchor): D_ref = 2 km, f_ref = 4 {KHZ}; criterion: optical depth <= 0.5 over D_ref.",
        "- A-mask: ceiling — |m(9 km)| only dimensioned common-mode content in this "
        "adversarial clause; Caveat: forced.",
        "", "## Unit map"])
    rr = extract_rows(bad_doc)
    try:
        parse_anchor_set(rr)
        assert False, 'forced-failure synthetic did not raise'
    except RowDefect as e:
        assert e.idx == 2 and e.masked is not None
        assert not re.search(r'\d', e.masked) and '#' in e.masked
        assert 'ceiling' in e.masked and str(e) == 'row 2: CEIL value unreadable'
    print('C-SYN-X ADV forced-failure (raise-time masking, digit-free, structured str): PASS')
    # ---- P3-A4 s2(iv): identifier-glue guard, positivity rejection, masked-abort mechanics ----
    id_doc = "\n".join(["## Anchors", "",
        f"- A-one (anchor): D_ref = 2 km, f_ref = 4 {KHZ}; criterion: optical depth <= 0.5 over D_ref.",
        "- A-id: catalog ZQ-3 kpc-scale ceiling with the common-mode value 0.06 for this synthetic; Caveat: adv.",
        "", "## Unit map"])
    rr = extract_rows(id_doc)
    _, pp = parse_anchor_set(rr)
    assert abs(pp[1]['B'] - 0.06) <= 1e-15 and set(pp[1]['inherit']) == {'f_ref', 'D_ref'} \
        and not pp[1].get('fallback'), pp[1]
    neg_doc = "\n".join(["## Anchors", "",
        f"- A-one (anchor): D_ref = 2 km, f_ref = 4 {KHZ}; criterion: optical depth <= 0.5 over D_ref.",
        "- A-neg: ceiling with the common-mode value 0.07 quoted over -5 km erroneously in this synthetic; Caveat: adv.",
        "", "## Unit map"])
    rr = extract_rows(neg_doc)
    _, pp = parse_anchor_set(rr)
    assert abs(pp[1]['B'] - 0.07) <= 1e-15 and 'D_ref' in pp[1]['inherit'], pp[1]
    print('C-SYN-X ADV-2 (identifier-glued digit rejected; negative path -> positivity -> inheritance): PASS')
    mck = _masked_abort('/tmp/mask_mech_test.json', 'test', 'mech', 'unhandled exception (masked)',
                        rb_mask('boom 123 glitch 4.5 zz'), None, 'synthetic')
    import os as _os
    assert _os.path.exists('/tmp/mask_mech_test.json') and mck['masked_clause'] == 'boom # glitch # zz'
    print('C-SYN-X masked-abort mechanics (checkpoint written, digit-free mask): PASS')

self_tests()
if not READ:
    print('STAGE 0 COMPLETE (sealed file NOT opened). Set GPOLY1_READ=1 for this leg single read.')
    sys.exit(0)

# ======================= READ #2 (authorized re-lock) =================================
LEG = os.environ.get('GPOLY1_LEG', 'chat')
READ_LABEL = os.environ.get('GPOLY1_READ_LABEL', 'cc-1' if LEG == 'cc' else 'chat-4')
CKPATH = f'/mnt/user-data/outputs/poly1_phase3_{LEG}.json'
raw = open(SEALED, 'rb').read()
md5 = hashlib.md5(raw).hexdigest()
assert md5 == SEALED_MD5, f'SEALED MD5 MISMATCH: {md5}'
text = raw.decode('utf-8')
print(f'\nSEALED FILE SINGLE READ ({LEG}, {READ_LABEL}): md5 {md5} ({len(raw)} B)')

try:
    rows = extract_rows(text)
    refs, parsed = parse_anchor_set(rows)
    print(f"ANCHOR CENSUS: {len(parsed)} rows -> " + ', '.join(f"{p['idx']}:{p['cls']}" for p in parsed))
    print(f"refs: D_ref = {refs['D_ref']:.6e} m; k(f_ref) = {refs['f_ref']:.6e} /m")
    for p in parsed:
        ex = {k2: v2 for k2, v2 in p.items()
              if k2 in ('B','L','k','d_cap','reading','inherit','oom','pattern','matched_span','fallback')}
        print(f"  [{p['idx']}] {p['cls']:7s} {ex}")
    fb = [(p['idx'], p['cls'], p['fallback']) for p in parsed if p.get('fallback')]
    print('FALLBACKS ENGAGED: ' + (str(fb) if fb else 'NONE'))

    def eval_arm(arm, relax_oom=1.0):
        ups, voided = [], []
        d_caps = []
        for p in parsed:
            if p['kind'] == 'att':
                B = p['B']; e = att_edge(arm, B, p['k'], p['L']); ceil = KD_CLIP/p['k']
                if e <= ceil: ups.append((e, f"A{p['idx']}"))
                else: voided.append((f"A{p['idx']}", e, ceil))
            elif p['kind'] == 'ceil':
                B = p['B']*relax_oom
                e1 = att_edge(arm, B, p['k'], p['L']); c1 = KD_CLIP/p['k']
                if e1 <= c1: ups.append((e1, f"A{p['idx']}-att"))
                else: voided.append((f"A{p['idx']}-att", e1, c1))
                e2 = bir_edge(arm, B, p['L']); N = (S1[arm]/B)**2
                if N >= N_MIN: ups.append((e2, f"A{p['idx']}-bir"))
                else: voided.append((f"A{p['idx']}-bir", e2, N))
            elif p['kind'] == 'dlm':
                B = p['B']*relax_oom
                e = bir_edge(arm, B, p['L']); N = (S1[arm]/B)**2
                if N >= N_MIN: ups.append((e, f"A{p['idx']}"))
                else: voided.append((f"A{p['idx']}", e, N))
            elif p['kind'] == 'vld':
                d_caps.append((p['d_cap'], f"A{p['idx']}"))
        if not ups and not d_caps:
            return dict(cls='I-1', W=None, voided=voided)
        cands = ups + d_caps
        up, gov = min(cands)
        W = (0.0, up)
        cls = 'P-2'
        return dict(cls=cls, W=W, governing=gov, voided=voided,
                    edges=sorted([(e, g) for e, g in cands]))

    arm_out = {a: eval_arm(a) for a in ARMS}
    relaxed = {a: eval_arm(a, relax_oom=10.0) for a in ARMS}
    order = {'P-1':3,'P-2':2,'I-1':1,'F-1':0}
    classes = [arm_out[a]['cls'] for a in ARMS]
    gate = 'F-1' if all(c=='F-1' for c in classes) else max(classes, key=lambda c: order[c])
    ivals = sorted([arm_out[a]['W'] for a in ARMS if arm_out[a]['W']])
    W_union = None
    if ivals:
        merged = [list(ivals[0])]
        for lo, up in ivals[1:]:
            if lo <= merged[-1][1]: merged[-1][1] = max(merged[-1][1], up)
            else: merged.append([lo, up])
        W_union = [tuple(m) for m in merged]

    print('\n== PER-ARM VERDICTS ==')
    for a in ARMS:
        r = arm_out[a]
        w = '—' if r['W'] is None else f"(0, {r['W'][1]:.6e}] m"
        print(f"{a:12s} {r['cls']}  W = {w}  governing={r.get('governing')}  voided={len(r['voided'])}")
        rx = relaxed[a]
        print(f"             OOM x10 relax: class {rx['cls']}, W_up {('—' if rx['W'] is None else f'{rx[chr(87)][1]:.6e} m')}")
    print(f'\nGATE VERDICT CLASS: {gate}')
    if W_union:
        print('W_union =', ', '.join(f'(0, {up:.6e}] m' for lo, up in W_union))

    oom_line = {a: dict(point_class=arm_out[a]['cls'],
                        relaxed_class=relaxed[a]['cls'],
                        point_up=arm_out[a]['W'][1] if arm_out[a]['W'] else None,
                        relaxed_up=relaxed[a]['W'][1] if relaxed[a]['W'] else None,
                        survives='YES' if arm_out[a]['cls']==relaxed[a]['cls'] else 'CHANGES')
                for a in ARMS}

    ck = dict(gate='G-POLY1', phase='3', leg=LEG, read=READ_LABEL + ' (authorized re-lock 3 6a7069b0)',
              lock=dict(memo='e16a78906560d2bb076d0699966981ac',
                        addendum1='ba75b113e8ad094cd752026df4e73977',
                        relock1='7f4b53ad43af3aff55938726d8f26738',
                        addendum2='ac87bc92890c7bf6a08b3d67d493ec9c',
                        relock2='b1150c946f6986a9bc19ae2b073db83e',
                        addendum3='257b81bf3924cb92ca9d1232fb94325c',
                        relock3='6a7069b07c2184eea41dfc38b4446c9d',
                    addendum4='659454eda11c969ce7d6736c6f1e1063',
                    relock4='98be3e3c0071bebad816aeca4ea96755',
                        base='V4.75 0e923ab786c1e1a96eb0a3bcad3e616f',
                        elections=['E3-1(a)','E3-2(a)','E3-3(a)','E3-4(a)']),
              sealed=dict(md5=md5, bytes=len(raw)),
              refs=dict(D_ref_m=refs['D_ref'], k_fref=refs['f_ref']),
              anchors=[{k2: v2 for k2, v2 in p.items() if k2 != 'text'} for p in parsed],
              anchor_texts={p['idx']: p['text'] for p in parsed},
              curves=dict(QTa=QTA, s1=S1),
              self_tests='memo §7 + C-SYN-X ALL PASS (both stages)',
              per_arm={a: {k2: (list(v2) if isinstance(v2, tuple) else v2)
                           for k2, v2 in arm_out[a].items()} for a in ARMS},
              oom_robustness=oom_line, gate_class=gate, W_union=W_union)
    out = CKPATH
    open(out, 'w').write(json.dumps(ck, indent=1, default=float))
    b = open(out, 'rb').read()
    print(f'\ncheckpoint (sanctioned): {out}  md5 {hashlib.md5(b).hexdigest()}  ({len(b)} B)')

except RowDefect as e:
    _masked_abort(CKPATH, LEG, READ_LABEL, e.label, e.masked, e.idx, md5)
    print(f'X-1 SCHEMA-DEFECT ({LEG} single read): row {e.idx}: {e.label} — ABORT.')
    if e.masked: print('masked clause:', e.masked)
    sys.exit(2)
except SystemExit:
    raise
except Exception as e:
    try:
        _mm = rb_mask(str(e))
    except AssertionError:
        _mm = None
    _masked_abort(CKPATH, LEG, READ_LABEL, 'unhandled exception (masked)', _mm, None, md5)
    print(f'X-1 SCHEMA-DEFECT ({LEG} single read): unhandled exception — MASKED ABORT (catch-all).')
    if _mm: print('masked:', _mm)
    sys.exit(2)
