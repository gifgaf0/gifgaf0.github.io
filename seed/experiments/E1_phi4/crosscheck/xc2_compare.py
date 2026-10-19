"""Cross-check comparison (second pass).  Reads the cross-check outputs
  * first cross-check code (6th-order FD + RK4, dx = 0.08):  xc_e1a.json, xc_e1b_summary.json,
    xc_e1c_example.json, xc_e1c_map.jsonl, xc_e1d_coarse_w*.jsonl, xc_e1d_line_*.jsonl, xc_e1d_single.jsonl
  * second cross-check code (Fourier + exact-linear Yoshida splitting):  xc2_dsv.jsonl, xc2_gauss_w*.jsonl,
    xc2_targets.jsonl
and the ORIGINAL agent's data files (data only), and writes xc2_compare.json.  Works on partial results.
"""
import json, os, glob
import numpy as np
from scipy.stats import spearmanr

HERE = os.path.dirname(os.path.abspath(__file__))
ORIG = os.path.dirname(HERE)
SQ2 = np.sqrt(2.0)
MK = 2 * SQ2 / 3


def jl(path):
    out = []
    for p in sorted(glob.glob(path)):
        for line in open(p):
            try:
                out.append(json.loads(line))
            except Exception:
                pass
    return out


def key3(r):
    return (round(r['A'], 4), round(r['sigma'], 4), round(r['k'], 4))


res = {}

# ------------------------------------------------------------------ E1a, E1b (first cross-check code)
a = json.load(open(os.path.join(HERE, 'xc_e1a.json')))
res['e1a'] = dict(M_bvp=a['bvp_L25.0']['M'], M_rel_err=a['bvp_L25.0']['rel_err'],
                  omega_s_cheb=a['cheb_N240_L30.0']['omega_s'], omega_s_rel_err=a['cheb_N240_L30.0']['rel_err'],
                  omega_s_time=a['time_domain']['omega_s'], omega_s_time_rel_err=a['time_domain']['rel_err'])
b = json.load(open(os.path.join(HERE, 'xc_e1b_summary.json')))
ob = json.load(open(os.path.join(ORIG, 'e1b_analysis.json')))
res['e1b'] = dict(vc=b['vc'], vc_bracket=b['vc_bracket'], vc_dt002=b['vc_dt002'], windows=b['windows'],
                  w1_dt002=b['w1_dt002'],
                  T12=[v[1] - v[0] for v in b['bounce_times'].values()],
                  vc_minus_target=b['vc'] - 0.2598, vc_minus_orig_dt0=b['vc'] - 0.26005625,
                  w1_minus_orig_dt0=[b['windows'][0][0] - 0.19256458, b['windows'][0][1] - 0.20342708])
print('E1a', res['e1a'])
print('E1b', {k: res['e1b'][k] for k in ('vc', 'windows', 'vc_minus_target', 'vc_minus_orig_dt0', 'w1_minus_orig_dt0', 'T12')})

# ------------------------------------------------------------------ E1c
og = {}
for f in ['e1c_grid.json', 'e1c_fine.json', 'e1c_high.json']:
    for r in json.load(open(os.path.join(ORIG, f)))['runs']:
        og[(round(r['omega'], 3), round(r['v'], 3))] = r
xm = {}
for r in jl(os.path.join(HERE, 'xc_e1c_map.jsonl')):
    xm[(round(r['omega'], 3), round(r['v'], 3))] = r
comm = sorted(set(og) & set(xm))
A_ = np.array([og[c]['produced_dsv'] for c in comm])
B_ = np.array([xm[c]['pair_T'] for c in comm])
Eo = np.array([og[c]['E0'] for c in comm])
Em = np.array([xm[c]['E_over_2M'] * 2 * MK for c in comm])
per = {}
for om in sorted(set(c[0] for c in comm)):
    cs = [c for c in comm if c[0] == om]
    per[str(om)] = dict(n=len(cs), fd6=[c[1] for c in cs if xm[c]['pair_T']], orig=[c[1] for c in cs if og[c]['produced_dsv']],
                        orig_all_v_step001=sorted(k[1] for k, r in og.items() if k[0] == om and r['produced_dsv']))
med_x = [(float(o), float(np.median(v['fd6']))) for o, v in per.items() if v['fd6'] and float(o) <= 0.99]
rho_x = spearmanr([m[0] for m in med_x], [m[1] for m in med_x])
# DSV Fig. 2, our own reading of the published figure (rendered from the arXiv PDF), +-0.01
DSV_READ = {0.90: [(0.76, 0.86)], 0.92: [(0.74, 0.74), (0.76, 0.84)], 0.94: [(0.67, 0.67), (0.71, 0.80)],
            0.96: [(0.59, 0.59), (0.62, 0.62), (0.65, 0.66), (0.69, 0.72)], 0.98: [(0.49, 0.49), (0.54, 0.55)],
            0.99: [(0.43, 0.43)]}


def dsv_says(om, v):
    for lo, hi in DSV_READ.get(om, []):
        if lo - 0.005 <= v <= hi + 0.005:
            return True
    return False


rows = []
for c in comm:
    if c[0] in DSV_READ:
        rows.append((dsv_says(*c), bool(og[c]['produced_dsv']), bool(xm[c]['pair_T'])))
rows = np.array(rows)
dsvcmp = dict(n_points=int(len(rows)), n_dsv_producing=int(rows[:, 0].sum()),
              orig_hits=int((rows[:, 0] & rows[:, 1]).sum()), orig_false_pos=int((~rows[:, 0] & rows[:, 1]).sum()),
              fd6_hits=int((rows[:, 0] & rows[:, 2]).sum()), fd6_false_pos=int((~rows[:, 0] & rows[:, 2]).sum()))
res['e1c_map'] = dict(n_common=len(comm), agree=float(np.mean(A_ == B_)), orig_prod=int(A_.sum()), fd6_prod=int(B_.sum()),
                      both=int((A_ & B_).sum()), orig_only=int((A_ & ~B_).sum()), fd6_only=int((~A_ & B_).sum()),
                      max_rel_E_diff=float(np.max(np.abs(Em / Eo - 1))), per_omega=per,
                      spearman_fd6=[float(rho_x[0]), float(rho_x[1])],
                      fd6_prod_v_ge_086=int(sum(xm[c]['pair_T'] for c in xm if c[1] >= 0.86 and c[0] <= 0.99)),
                      n_v_ge_086=int(sum(1 for c in xm if c[1] >= 0.86 and c[0] <= 0.99)),
                      fd6_prod_omega_gt_099=int(sum(xm[c]['pair_T'] for c in xm if c[0] > 0.99)),
                      n_omega_gt_099=int(sum(1 for c in xm if c[0] > 0.99)),
                      fd6_survive_frac=float(np.mean([xm[c]['pair_end'] for c in xm if xm[c]['pair_T']])),
                      vs_dsv_reading=dsvcmp)
print('E1c map: n=%d agree=%.3f orig=%d fd6=%d both=%d orig_only=%d fd6_only=%d  rho_fd6=%.3f' % (
    len(comm), res['e1c_map']['agree'], A_.sum(), B_.sum(), (A_ & B_).sum(), (A_ & ~B_).sum(), (~A_ & B_).sum(), rho_x[0]))
for o, v in per.items():
    print('   omega %s  fd6 %s | orig %s' % (o, v['fd6'], v['orig']))
print('   vs DSV reading:', dsvcmp)

# example point
ex1 = json.load(open(os.path.join(HERE, 'xc_e1c_example.json')))
oex = json.load(open(os.path.join(ORIG, 'e1c_example.json')))
ex = dict(orig=dict(first=oex['pair_continuously_present_since'], pair_at_T=oex['produced_dsv'],
                    interval_at_T=oex['final_positive_intervals_T'], survives=oex['survives_to_1.5T']),
          fd6_dx008=dict(first=ex1['first_pair_t'], pair_at_T=ex1['pair_at_T'], pair_at_end=ex1['pair_at_end']))
for r in jl(os.path.join(HERE, 'xc2_dsv.jsonl')):
    ex['spec_om%.2f_v%.2f_dx%g_dt%g' % (r['omega'], r['v'], r['dx'], r['dt'])] = dict(
        first=r['first_pair_t'], pair_at_T=r['pair_at_T'], width_at_T=r['width_at_T'], pair_at_end=r['pair_at_end'],
        persistent_from=r['persistent_from'], E_over_2M=r['E_over_2M'],
        orig_call=(og.get((round(r['omega'], 3), round(r['v'], 3)), {}).get('produced_dsv')))
res['e1c_example'] = ex
print('E1c example:', json.dumps(ex, indent=0))

# ------------------------------------------------------------------ E1d
orig = {key3(r): r for r in json.load(open(os.path.join(ORIG, 'e1d_coarse.json')))['runs']}
odx = {key3(r): r for r in json.load(open(os.path.join(ORIG, 'e1d_dxcheck.json')))['runs']}
fd6 = {key3(r): r for r in jl(os.path.join(HERE, 'xc_e1d_coarse_w*.jsonl'))}
spec = {key3(r): r for r in jl(os.path.join(HERE, 'xc2_gauss_w*.jsonl'))}

cm = sorted(set(orig) & set(fd6))
a1 = np.array([orig[c]['produced'] for c in cm]); b1 = np.array([fd6[c]['prod'] for c in cm])
E1 = np.array([orig[c]['E_over_2M'] for c in cm])
bands = [0, 1, 1.5, 2, 3, 4, 6, 8, 12, 16, 24, 32, 64, 1e9]
fr = []
for lo, hi in zip(bands[:-1], bands[1:]):
    m = (E1 >= lo) & (E1 < hi)
    if m.sum():
        fr.append([lo, hi, int(m.sum()), round(float(a1[m].mean()), 3), round(float(b1[m].mean()), 3)])
res['e1d_coarse_fd6'] = dict(n=len(cm), agree=float(np.mean(a1 == b1)), agree_E_gt_2M=float(np.mean(a1[E1 > 1] == b1[E1 > 1])),
                             orig_prod=int(a1.sum()), fd6_prod=int(b1.sum()), both=int((a1 & b1).sum()),
                             orig_only=int((a1 & ~b1).sum()), fd6_only=int((~a1 & b1).sum()), frac_vs_E=fr,
                             fd6_prod_below_2M=int(sum(fd6[c]['prod'] and fd6[c]['E_over_2M'] < 1 for c in cm)),
                             fd6_prod_A_le_03=int(sum(fd6[c]['prod'] and c[0] <= 0.3 for c in cm)))
# original's own dx-halving agreement on its 300 points, for reference
cdx = sorted(set(odx) & set(orig))
res['e1d_orig_dx_selfagree'] = float(np.mean([orig[c]['produced'] == odx[c]['produced'] for c in cdx]))
# original's dx check restricted to E > 2M
res['e1d_orig_dx_selfagree_E_gt_2M'] = float(np.mean([orig[c]['produced'] == odx[c]['produced'] for c in cdx if orig[c]['E_over_2M'] > 1]))
print('E1d coarse (orig vs FD6):', {k: v for k, v in res['e1d_coarse_fd6'].items() if k != 'frac_vs_E'})
print('   frac vs E [lo,hi,n,orig,fd6]:', fr)
print('   original dx 0.1 vs 0.05 self-agreement: %.3f (E>2M %.3f, n=%d)' % (res['e1d_orig_dx_selfagree'], res['e1d_orig_dx_selfagree_E_gt_2M'], len(cdx)))

if spec:
    cs = sorted(spec)
    o = np.array([orig[c]['produced'] for c in cs]); s_ = np.array([spec[c]['prod'] for c in cs])
    f_ = np.array([fd6[c]['prod'] for c in cs])
    Es = np.array([orig[c]['E_over_2M'] for c in cs])
    hi = Es > 1
    sm = np.array([spec[c]['prod_mine'] for c in cs])
    three = dict(n=len(cs), n_E_gt_2M=int(hi.sum()), orig_prod=int(o.sum()), spec_prod=int(s_.sum()), fd6_prod=int(f_.sum()),
                 agree_spec_orig=float(np.mean(s_ == o)), agree_spec_fd6=float(np.mean(s_ == f_)), agree_fd6_orig=float(np.mean(f_ == o)),
                 agree_spec_orig_E_gt_2M=float(np.mean(s_[hi] == o[hi])), agree_fd6_orig_E_gt_2M=float(np.mean(f_[hi] == o[hi])),
                 agree_spec_fd6_E_gt_2M=float(np.mean(s_[hi] == f_[hi])),
                 all_three_agree=float(np.mean((s_ == o) & (f_ == o))),
                 majority_vs_orig=float(np.mean(((s_.astype(int) + f_.astype(int) + o.astype(int)) >= 2) == o)),
                 spec_own_test_vs_report_test=float(np.mean(sm == s_)),
                 max_rel_E_diff=float(max(abs(spec[c]['E_over_2M'] / orig[c]['E_over_2M'] - 1) for c in cs)),
                 spec_prod_below_2M=int(sum(spec[c]['prod'] and spec[c]['E_over_2M'] < 1 for c in cs)),
                 disagreements=[[list(c), bool(orig[c]['produced']), bool(spec[c]['prod']), bool(fd6[c]['prod']), round(orig[c]['E_over_2M'], 2)]
                                for c in cs if orig[c]['produced'] != spec[c]['prod']])
    # point-level comparison of the sample at the original's dx = 0.05 where available
    cso = [c for c in cs if c in odx]
    if cso:
        three['n_with_orig_dx005'] = len(cso)
        three['agree_spec_orig_dx005'] = float(np.mean([spec[c]['prod'] == odx[c]['produced'] for c in cso]))
        three['agree_orig_dx01_dx005'] = float(np.mean([orig[c]['produced'] == odx[c]['produced'] for c in cso]))
    res['e1d_sample_spec'] = three
    print('E1d random sample (spectral):', {k: v for k, v in three.items() if k != 'disagreements'})

tg = jl(os.path.join(HERE, 'xc2_targets.jsonl'))
res['e1d_targets'] = [{k: r[k] for k in ('A', 'sigma', 'k', 'single', 'oneway', 'dx', 'dt', 'E_over_2M', 'N_lin', 'prod', 'rep')} for r in tg]
for r in res['e1d_targets']:
    r['N_E_lam_over_m2'] = r['E_over_2M'] * 2 * MK / (2 * SQ2)
    r['N_lin_lam_over_m2'] = r['N_lin'] / 2
    print('   target', r)

# ------------------------------------------------------------------ E1e
e = json.load(open(os.path.join(HERE, 'xc_e1e.json')))
res['e1e_fd6'] = e
res['e1e_floor'] = 2 * MK / (2 * SQ2)
print('E1e floor N lam/m^2 =', res['e1e_floor'])
for kk, vv in e.items():
    print('   ', kk, {q: round(w, 4) for q, w in vv.items()})

json.dump(res, open(os.path.join(HERE, 'xc2_compare.json'), 'w'), indent=1, default=str)
print('wrote xc2_compare.json')
