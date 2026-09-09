#!/usr/bin/env python3
"""g_s2c1w_compare_v1_0.py — frozen two-leg comparator for G-S2C1-W (C-W-1..C-W-6; memo §8.4). Frozen pre-chat-emission (D-W-9).
Usage: g_s2c1w_compare_v1_0.py <chat_ckpt.json> <cc_ckpt.json>
Exit 0 ALL PASS; 1 MISS (S9); 3 CC checkpoint ABSENT or md5 != declared (comparison OUTSTANDING, nothing compared)."""
import sys, os, json, hashlib
CC_DECLARED_MD5 = '97f26c04f982b1cc1694f4a47bdce882'      # lock record addendum 1 §4
SCHEMA = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'g_s2c1w_schema_v1_0.json')))
def md5f(p): return hashlib.md5(open(p, 'rb').read()).hexdigest()
def rel(a, b): return abs(a - b) / max(abs(b), SCHEMA['tolerances']['abs_floor'])
def get(d, path):
    for k in path:
        if isinstance(d, list): d = d[int(k)]
        elif isinstance(d, dict) and k in d: d = d[k]
        else: return None
    return d
def main():
    chat_p, cc_p = sys.argv[1], sys.argv[2]
    rec = {'comparator': 'g_s2c1w_compare_v1_0.py', 'cc_declared_md5': CC_DECLARED_MD5}
    if not os.path.exists(cc_p):
        rec.update({'status': 'OUTSTANDING', 'reason': 'CC checkpoint file ABSENT — a hash cannot be compared to values; C-W-1..6 not executed'})
        print(json.dumps(rec, indent=1)); sys.exit(3)
    got = md5f(cc_p); rec['cc_file_md5'] = got
    if got != CC_DECLARED_MD5:
        rec.update({'status': 'OUTSTANDING', 'reason': 'CC checkpoint md5 != declared; not the checkpoint of record'})
        print(json.dumps(rec, indent=1)); sys.exit(3)
    A, B = json.load(open(chat_p)), json.load(open(cc_p))
    miss, items = [], 0
    def cmp(path, tol=None, exact=False, label=None):
        nonlocal items
        items += 1; a, b = get(A, path), get(B, path); lab = label or '/'.join(map(str, path))
        if a is None or b is None:
            miss.append((lab, 'REPRESENTATIONAL: key absent on ' + ('both' if a is None and b is None else 'chat' if a is None else 'cc'))); return
        if exact or isinstance(a, (str, bool)) or a is None:
            if a != b: miss.append((lab, f'{a!r} != {b!r}'))
        else:
            if a is None and b is None: return
            if (a is None) != (b is None): miss.append((lab, f'{a!r} vs {b!r}')); return
            r = rel(float(a), float(b))
            if r > tol: miss.append((lab, f'rel dev {r:.3e} > {tol}'))
    T = SCHEMA['tolerances']
    # C-W-3 sealed identity
    cmp(['sealed', 'md5'], exact=True); cmp(['sealed', 'census'], exact=True); cmp(['sealed', 'bytes'], exact=True)
    # C-W-5 pinned inputs identity
    for k in SCHEMA['lock_keys']: cmp(['lock', k], exact=True)
    # C-W-4 lexer readings
    na, nb = len(A.get('anchors', [])), len(B.get('anchors', []))
    if na != nb: miss.append(('anchors/count', f'{na} vs {nb}'))
    for i in range(min(na, nb)):
        for k in ('idx', 'cls', 'q', 'row_md5'): cmp(['anchors', i, k], exact=True)
        for k in ('B', 'k'): cmp(['anchors', i, k], tol=1e-12)
    # C-W-1 edges of record + C-W-2 classes
    for arm in SCHEMA['arms']:
        cmp(['per_arm', arm, 'W_upper_m'], tol=T['rel_exact']); cmp(['per_arm', arm, 'pinned_gpoly1_edge_m'], tol=1e-12)
        cmp(['per_arm', arm, 'governing'], exact=True); cmp(['per_arm', arm, 'arm_class'], exact=True); cmp(['per_arm', arm, 'oom_robust'], exact=True)
        for i in range(min(na, nb)):
            for k in SCHEMA['disp_keys']:
                if k in ('fail_L', 'voided', 'dressing_sensitive', 'dressed_status', 'q', 'anchor', 'c_q'): cmp(['per_arm', arm, 'disp', i, k], exact=True)
                else: cmp(['per_arm', arm, 'disp', i, k], tol=T['rel_F_L_dependent'] if k in SCHEMA['F_L_dependent_fields'] else T['rel_exact'])
    cmp(['union', 'W_union_prime', 1], tol=T['rel_exact']); cmp(['union', 'union_governing_arm'], exact=True); cmp(['union', 'W_intersection', 1], tol=T['rel_exact'])
    for k in ('class', 'oom_robust', 'reinstatement'): cmp(['comparison', k], exact=True)
    cmp(['comparison', 'W_union_prime_upper_m'], tol=T['rel_exact']); cmp(['comparison', 'W_union_pinned_upper_m'], tol=1e-12)
    cmp(['comparison', 'per_arm_classes'], exact=True); cmp(['comparison', 'per_arm_governing'], exact=True)
    # C-W-6 T1 zero hits
    cmp(['t1_checkpoint_scan', 'hits'], exact=True); cmp(['t1_source_scan', 'hits'], exact=True)
    if get(A, ['t1_checkpoint_scan', 'hits']) not in (0, None) or get(B, ['t1_checkpoint_scan', 'hits']) not in (0, None): miss.append(('t1', 'nonzero hits'))
    rec.update({'items': items, 'miss': miss, 'status': 'ALL PASS' if not miss else f'MISS x{len(miss)} (S9)'})
    print(json.dumps(rec, indent=1)); sys.exit(0 if not miss else 1)
if __name__ == '__main__': main()
