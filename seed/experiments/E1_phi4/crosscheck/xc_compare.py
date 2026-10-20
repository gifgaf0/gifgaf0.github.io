"""Compare the cross-check runs with the original E1 data files (data only, not code).
Writes crosscheck/xc_compare.json and prints a summary.  Works on partial results."""
import json, os, sys
import numpy as np
from scipy.stats import spearmanr

HERE = os.path.dirname(os.path.abspath(__file__))
ORIG = os.path.dirname(HERE)
sys.path.insert(0, HERE)


def jl(path):
    out = {}
    if os.path.exists(path):
        for line in open(path):
            try:
                r = json.loads(line)
            except Exception:
                continue
            out[(r['A'], r['sigma'], r['k'])] = r
    return out


def key(r):
    return (round(r['A'], 4), round(r['sigma'], 4), round(r['k'], 4))


res = {}
# ---------------- E1d coarse ----------------
mine = {}
for w in range(4):
    for kk, r in jl(os.path.join(HERE, f'xc_e1d_coarse_w{w}.jsonl')).items():
        mine[key(r)] = r
orig = {key(r): r for r in json.load(open(os.path.join(ORIG, 'e1d_coarse.json')))['runs']}
common = sorted(set(mine) & set(orig))
if common:
    a = np.array([orig[c]['produced'] for c in common]); b = np.array([mine[c]['prod'] for c in common])
    bm = np.array([mine[c]['prod_mine'] for c in common])
    Eo = np.array([orig[c]['E_over_2M'] for c in common]); Em = np.array([mine[c]['E_over_2M'] for c in common])
    hiE = Eo > 1.0
    d = dict(n=len(common), agree=float(np.mean(a == b)), agree_E_gt_2M=float(np.mean(a[hiE] == b[hiE])),
             n_hiE=int(hiE.sum()),
             orig_prod=int(a.sum()), mine_prod=int(b.sum()), both=int((a & b).sum()), orig_only=int((a & ~b).sum()),
             mine_only=int((~a & b).sum()), my_alt_test_agrees_with_my_report_test=float(np.mean(b == bm)),
             max_rel_E_diff=float(np.max(np.abs(Em / Eo - 1))),
             mine_prod_below_2M=int(np.sum(b & (Em < 1.0))))
    # per energy band
    bands = [0, 0.5, 1, 1.5, 2, 3, 4, 6, 8, 12, 16, 24, 32, 64, 1e9]
    rows = []
    for lo, hi in zip(bands[:-1], bands[1:]):
        m = (Eo >= lo) & (Eo < hi)
        if m.sum():
            rows.append([lo, hi, int(m.sum()), round(float(a[m].mean()), 3), round(float(b[m].mean()), 3)])
    d['frac_vs_E_orig_mine'] = rows
    A = np.array([c[0] for c in common]); S = np.array([c[1] for c in common]); K = np.array([c[2] for c in common])
    d['mine_prod_A_le_0.3'] = int(np.sum(b & (A <= 0.3)))
    d['orig_prod_A_le_0.3'] = int(np.sum(a & (A <= 0.3)))
    if b.any():
        j = np.argmin(np.where(b, Em, 1e9))
        d['mine_min_prod_E_over_2M'] = [float(Em[j]), common[j]]
    # matched-energy speed / width trends (my data, same bands as the original)
    vg = K / np.sqrt(K ** 2 + 2)
    tr = {}
    for lo, hi in [(2, 4), (4, 8), (8, 16)]:
        m = (Em >= lo) & (Em < hi)
        for name, x, vals in [('speed', vg, sorted(set(vg))), ('width', S, sorted(set(S)))]:
            fx, fy = [], []
            for v in vals:
                mm = m & (x == v)
                if mm.sum() >= 3:
                    fx.append(v); fy.append(float(b[mm].mean()))
            rho, p = spearmanr(fx, fy) if len(fx) > 2 else (np.nan, np.nan)
            tr[f'{name}_{lo}_{hi}'] = dict(x=[round(q, 3) for q in fx], frac=[round(q, 3) for q in fy], rho=float(rho), p=float(p))
    d['mine_trends'] = tr
    # fraction vs A (pooled) both
    d['frac_vs_A_orig_mine'] = [[float(Av), int((A == Av).sum()), round(float(a[A == Av].mean()), 3), round(float(b[A == Av].mean()), 3)] for Av in sorted(set(A))]
    # disagreement list
    d['disagreements'] = [[c, bool(orig[c]['produced']), bool(mine[c]['prod']), round(orig[c]['E_over_2M'], 2)] for c in common if orig[c]['produced'] != mine[c]['prod']]
    res['e1d_coarse'] = d
    print('E1d coarse: n=%d agree=%.3f (E>2M: %.3f, n=%d) orig_prod=%d mine_prod=%d both=%d orig_only=%d mine_only=%d maxrelE=%.1e' % (
        d['n'], d['agree'], d['agree_E_gt_2M'], d['n_hiE'], d['orig_prod'], d['mine_prod'], d['both'], d['orig_only'], d['mine_only'], d['max_rel_E_diff']))
    print('  frac vs E [lo,hi,n,orig,mine]:', rows)
    print('  A<=0.3 producers orig/mine:', d['orig_prod_A_le_0.3'], d['mine_prod_A_le_0.3'], ' mine below 2M:', d['mine_prod_below_2M'],
          ' mine min prod E/2M:', d.get('mine_min_prod_E_over_2M'))
    for kk, v in tr.items():
        print('  ', kk, v['rho'], v['p'], v['frac'])
    print('  frac vs A [A,n,orig,mine]:', d['frac_vs_A_orig_mine'])

# ---------------- single-packet controls ----------------
sp = jl(os.path.join(HERE, 'xc_e1d_single.jsonl'))
osing = {key(r): r for r in json.load(open(os.path.join(ORIG, 'e1d_single.json')))['runs']}
if sp:
    ks = [key(r) for r in sp.values()]
    my_s = np.array([sp_r['prod'] for sp_r in sp.values()])
    comm = [k for k in ks if k in osing]
    agree = [sp[(k[0], k[1], k[2])]['prod'] == osing[k]['produced'] for k in comm] if comm else []
    res['single'] = dict(n=len(sp), mine_single_prod=int(my_s.sum()), frac=float(my_s.mean()),
                         n_common_with_orig=len(comm), agree_with_orig=float(np.mean(agree)) if agree else None,
                         orig_frac_on_common=float(np.mean([osing[k]['produced'] for k in comm])) if comm else None)
    print('single-packet controls:', res['single'])

# ---------------- constant-k line on sigma=16 slice ----------------
ln = jl(os.path.join(HERE, 'xc_e1d_line_s16.0_k1.0.jsonl'))
if ln:
    sl = json.load(open(os.path.join(ORIG, 'e1d_sliceAk_16.0.json')))['runs']
    ol = {round(r['A'], 4): r['produced'] for r in sl if abs(r['k'] - 1.0) < 1e-9}
    As = sorted(ln.keys())
    seq_m = [ln[a]['prod'] for a in As]
    seq_o = [ol.get(round(a[0], 4)) for a in As]
    sw = lambda s: int(sum(1 for i in range(1, len(s)) if s[i] != s[i - 1] and s[i] is not None and s[i - 1] is not None))
    res['line_s16_k1'] = dict(n=len(As), A=[a[0] for a in As], mine=seq_m, orig=seq_o, switches_mine=sw(seq_m), switches_orig=sw(seq_o),
                              agree=float(np.mean([m == o for m, o in zip(seq_m, seq_o) if o is not None])),
                              first_prod_A_mine=next((a[0] for a, m in zip(As, seq_m) if m), None),
                              first_prod_A_orig=next((a[0] for a, m in zip(As, seq_o) if m), None))
    print('line sigma=16 k=1:', {k: v for k, v in res['line_s16_k1'].items() if k not in ('A', 'mine', 'orig')})
    print('   mine:', ''.join('1' if m else '0' for m in seq_m))
    print('   orig:', ''.join('1' if m else ('0' if m is not None else '?') for m in seq_o))

# ---------------- DSV ----------------
dsv = {}
p = os.path.join(HERE, 'xc_e1c_map.jsonl')
if os.path.exists(p):
    for line in open(p):
        try:
            r = json.loads(line); dsv[(round(r['omega'], 3), round(r['v'], 3))] = r
        except Exception:
            pass
og = {}
for f in ['e1c_grid.json', 'e1c_fine.json', 'e1c_high.json']:
    fp = os.path.join(ORIG, f)
    if os.path.exists(fp):
        for r in json.load(open(fp))['runs']:
            og[(round(r['omega'], 3), round(r['v'], 3))] = r
if dsv:
    comm = sorted(set(dsv) & set(og))
    a = np.array([og[c]['produced_dsv'] for c in comm]); b = np.array([dsv[c]['pair_T'] for c in comm])
    Eo = np.array([og[c]['E0'] for c in comm]); Em = np.array([dsv[c]['E_over_2M'] * 2 * 2 * np.sqrt(2) / 3 for c in comm])
    per = {}
    for om in sorted(set(c[0] for c in comm)):
        per[str(om)] = dict(mine=[c[1] for c in comm if c[0] == om and dsv[c]['pair_T']],
                            orig=[c[1] for c in comm if c[0] == om and og[c]['produced_dsv']])
    med = [(float(om), float(np.median(v['mine']))) for om, v in per.items() if v['mine'] and float(om) <= 0.99]
    rho = spearmanr([m[0] for m in med], [m[1] for m in med]) if len(med) > 2 else (np.nan, np.nan)
    res['dsv'] = dict(n=len(comm), agree=float(np.mean(a == b)), orig_prod=int(a.sum()), mine_prod=int(b.sum()),
                      max_rel_E_diff=float(np.max(np.abs(Em / Eo - 1))), per_omega=per,
                      spearman_omega_median_v=[float(rho[0]), float(rho[1])],
                      mine_prod_v_ge_0_85=int(sum(dsv[c]['pair_T'] for c in comm if c[1] >= 0.85)),
                      mine_prod_omega_gt_099=[c for c in dsv if c[0] > 0.99 and dsv[c]['pair_T']],
                      n_omega_gt_099=len([c for c in dsv if c[0] > 0.99]),
                      disagreements=[[c, bool(og[c]['produced_dsv']), bool(dsv[c]['pair_T'])] for c in comm if og[c]['produced_dsv'] != dsv[c]['pair_T']],
                      survive_mine_frac=float(np.mean([dsv[c]['pair_end'] for c in comm if dsv[c]['pair_T']])) if b.any() else None)
    print('DSV: n=%d agree=%.3f orig_prod=%d mine_prod=%d maxrelE=%.1e rho=%s' % (len(comm), res['dsv']['agree'], a.sum(), b.sum(), res['dsv']['max_rel_E_diff'], rho))
    for om, v in per.items():
        print('   omega', om, 'mine', v['mine'], ' orig', v['orig'])
    print('   disagreements', res['dsv']['disagreements'])
    print('   omega>0.99 mine producing:', res['dsv']['mine_prod_omega_gt_099'], 'of', res['dsv']['n_omega_gt_099'])
ex = os.path.join(HERE, 'xc_e1c_example.json')
if os.path.exists(ex):
    r = json.load(open(ex))
    res['dsv_example'] = {k: r[k] for k in r if k != 'hist'}
    print('DSV example:', res['dsv_example'])

# ---------------- E1b ----------------
sb = os.path.join(HERE, 'xc_e1b_summary.json')
if os.path.exists(sb):
    s = json.load(open(sb))
    res['e1b'] = {k: s[k] for k in s if k != 'scan'}
    print('E1b:', json.dumps(res['e1b']))
json.dump(res, open(os.path.join(HERE, 'xc_compare.json'), 'w'), indent=1, default=str)
