"""Read-only tables for REPORT_chiral_loop.md from the trace_N1_chiral_*.json, control_N0_chiral_*.json, c0_chiral_*.json.
usage: python3 tables_chiral_loop.py > log_tables_chiral_loop.txt
"""
import json, glob, os
import numpy as np

G = ['+0.1', '-0.1', '+0.2', '-0.2', '+0.3', '-0.3']

def f(x, n=2):
    return '—' if x is None else f'{x:.{n}f}'

def load(start, g, N=65):
    p = f'trace_N1_chiral_{start}_N{N}_R6_g{g}.json'
    return json.load(open(p)) if os.path.exists(p) else None

def first_nolines(h):
    for d in h:
        if sum(d['nseg']) == 0: return d['it']
    return None

def first_no(h, k):
    for d in h:
        if d['nseg'][k] == 0: return d['it']
    return None

def geom_table(run):
    h = run['history']; fin = run['final']
    print('| it | E | R s2 / s3 | len s2 / s3 | R line 1 | centroid x 1 | z_rms 1 | len 1 | wall gap 1 | open ends | W_z(1) | sep min / mean | Lk₁₂ / Lk₁₃ |')
    print('|---|---|---|---|---|---|---|---|---|---|---|---|---|')
    rows = []
    for d in h:
        rows.append(d)
        if sum(d['nseg']) == 0: break
    for d in rows + [dict(fin, it=f"{fin['iters']} (final)")]:
        l1 = d.get('line1'); l2 = d.get('line2'); l3 = d.get('line3')
        lc = f"{d['nseg'][1]*0.5:.1f}/{d['nseg'][2]*0.5:.1f}"
        sep = f"{d['gap12_min']:.2f} / {d['gap12_mean']:.2f}" if 'gap12_min' in d else '—'
        lk = f"{d['Lk12']:.3f} / {d['Lk13']:.3f}" if (d['nseg'][0] and d['nseg'][1]) else '0 (no line 1)' if d['nseg'][0] == 0 and d['nseg'][1] else ('0 (no lines)' if sum(d['nseg']) == 0 else f"{d['Lk12']:.3f} / {d['Lk13']:.3f}")
        E = d['E']; Es = f'{E:.1f}' if abs(E) >= 1 else f'{E:.2e}'
        print(f"| {d['it']} | {Es} | {f(l2['rxy_mean']) if l2 else '—'} / {f(l3['rxy_mean']) if l3 else '—'} | {lc} | "
              f"{f(l1['rxy_mean']) if l1 else '—'} | {f(l1['centroid'][0]) if l1 else '—'} | {f(l1['z_rms']) if l1 else '—'} | "
              f"{d['nseg'][0]*0.5:.1f} | {f(l1['wall_gap']) if l1 else '—'} | {l1['open_ends'] if l1 else '—'} | "
              f"{round(l1['Wz']) if l1 else '—'} | {sep} | {lk} |")

def energy_table(run):
    h = run['history']; fin = run['final']
    print('| it | E | E_grad | E_mag | E_V | E_χ | E_χ (A·S part) | ⟨\\|S\\|/\\|ψ\\|²⟩_w | E_χ near line 1 | virial |')
    print('|---|---|---|---|---|---|---|---|---|---|')
    rows = []
    for d in h:
        rows.append(d)
        if sum(d['nseg']) == 0: break
    for d in rows + [dict(fin, it=f"{fin['iters']} (final)")]:
        E = d['E']; Es = f'{E:.1f}' if abs(E) >= 1 else f'{E:.2e}'
        print(f"| {d['it']} | {Es} | {d['E_grad']:.1f} | {d['E_mag']:.2f} | {d['E_V']:.1f} | {d['E_chi']:.1f} | {d['E_chi_AS']:.2f} | "
              f"{f(d['S_rho_wgrad'], 3)} | {f(d['E_chi_near1'], 2)} | {f(d['virial'], 3)} |")

def surface_sub_virial(run):
    """Descriptive: virial residual of (record - final record), i.e. with the final (line-free) state's split subtracted."""
    fin = run['final']
    if sum(fin['nseg']) != 0: return None
    out = []
    for d in run['history']:
        if sum(d['nseg']) == 0: break
        x = {k: d[k] - fin[k] for k in ('E_grad', 'E_mag', 'E_V', 'E_chi')}
        num = x['E_grad'] - x['E_mag'] + 2 * x['E_chi'] + 3 * x['E_V']
        den = abs(x['E_grad']) + abs(x['E_mag']) + 2 * abs(x['E_chi']) + 3 * abs(x['E_V'])
        out.append((d['it'], num / den))
    return out

# ----------------------------------------------------------------- C0
print('## C0')
for g in ('+0.3', '-0.3'):
    p = f'c0_chiral_N65_g{g}.json'
    if os.path.exists(p):
        c = json.load(open(p))
        print(f"gamma {g}: E_start {c['E_start']:.1f}, E_end {c['E_end']:.4f}, nseg {c['nseg_end']}, iters {c['iters']}, {c['msg']}, split {c['split_end']}, passes(literal) {c['passes']}")
        for k, v in c['by_distance_from_face'].items():
            print(f"   layer {k}: E_chi {v['E_chi']:.3f}, mean |S| {v['S_mean']:.2e}, max |psi - f0| {v['max_dev']:.4f}")

# ----------------------------------------------------------------- P1
print('\n## P1 controls')
for g in ('+0.3', '-0.3'):
    p = f'control_N0_chiral_N65_R6_g{g}.json'
    if not os.path.exists(p): continue
    c = json.load(open(p))
    print(f"gamma {g}: E_start {c['E_start']:.1f} E_end {c['E_end']:.4f} R_end {c['R_end']} nseg_end {c['nseg_end']} iters {c['iters']} {c['msg']} split_end {c['split_end']}")
    print('| it | E | R (strand 2) | R (strand 1) | nseg | E_grad | E_mag | E_V | E_χ | E_χ (A·S) |')
    print('|---|---|---|---|---|---|---|---|---|---|')
    hs = c['history']
    nz = None
    for i, d in enumerate(hs):
        if sum(d['nseg']) == 0 and nz is None: nz = i
    show = [d for i, d in enumerate(hs) if (nz is None or i <= nz) and (d['it'] % 4 == 0 or i == nz)]
    for d in show:
        print(f"| {d['it']} | {d['E']:.1f} | {d['R2']:.2f} | {d['R1']:.2f} | {d['nseg']} | {d['E_grad']:.1f} | {d['E_mag']:.2f} | {d['E_V']:.1f} | {d['E_chi']:.1f} | {d['E_chi_AS']:.2f} |")

# ----------------------------------------------------------------- main
print('\n## main runs')
for g in G:
    for s in 'AB':
        run = load(s, g)
        if run is None: continue
        fin = run['final']
        print(f"\n### start {s}, gamma {g}: iters {fin['iters']}, {fin['msg']}, final E {fin['E']:.4f}, nseg {fin['nseg']}, "
              f"all lines gone at it {first_nolines(run['history'])}, line 1 gone at it {first_no(run['history'], 0)}, "
              f"time {fin['t']:.0f} s")
        geom_table(run); print(); energy_table(run)
        sv = surface_sub_virial(run)
        if sv: print('surface-subtracted virial (it, value):', ', '.join(f'{i}: {v:+.3f}' for i, v in sv))

# ----------------------------------------------------------------- P3 and delays
print('\n## P3 and delay comparison')
for s in 'AB':
    g0 = json.load(open(f'trace_N1_{s}_N65_R6.json'))
    h0 = {d['it']: d for d in g0['history']}
    Es = [d['E'] for d in g0['history']]
    print(f"start {s}, gamma = 0: E monotone over records: {all(Es[k] <= Es[k-1] for k in range(1, len(Es)))}")
    print(f"start {s}, gamma = 0: lines gone at it {first_nolines(g0['history'])}, line 1 gone at it {first_no(g0['history'], 0)}, final iters {g0['final']['iters']}")
    for a in ('0.1', '0.2', '0.3'):
        rp, rm = load(s, '+' + a), load(s, '-' + a)
        if rp is None or rm is None: continue
        hp = {d['it']: d for d in rp['history']}; hm = {d['it']: d for d in rm['history']}
        common = sorted(set(hp) & set(hm))
        rel = [(i, abs(hp[i]['E'] - hm[i]['E']) / max(abs(hm[i]['E']), abs(hp[i]['E']))) for i in common if i > 0]
        big = [i for i, r in rel if r > 0.01]
        mx = max(rel, key=lambda t: t[1]) if rel else None
        # restricted to records where at least one run still has lines
        live = [(i, r) for i, r in rel if sum(hp[i]['nseg']) + sum(hm[i]['nseg']) > 0]
        mxl = max(live, key=lambda t: t[1]) if live else None
        print(f"  |gamma| {a}: +: lines gone {first_nolines(rp['history'])}, line1 gone {first_no(rp['history'], 0)}, final iters {rp['final']['iters']}; "
              f"-: lines gone {first_nolines(rm['history'])}, line1 gone {first_no(rm['history'], 0)}, final iters {rm['final']['iters']}")
        print(f"     P3: matched iterations {len(rel)}; max rel dE {mx[1]:.4f} at it {mx[0]}; while lines exist: max {mxl[1]:.4f} at it {mxl[0]}; "
              f"records with > 1 %: {len(big)} (first {big[:1]})")
        e0 = [f"{i}:{hp[i]['E']:.1f}/{hm[i]['E']:.1f}/{h0[i]['E']:.1f}" for i in common if i in h0 and i % 8 == 0 and i <= 48]
        both1 = [(i, abs(hp[i]['E'] - hm[i]['E']) / max(abs(hm[i]['E']), abs(hp[i]['E'])), abs(hp[i]['E'] - hm[i]['E'])) for i in common if i > 0 and hp[i]['nseg'][0] and hm[i]['nseg'][0]]
        m1 = max(both1, key=lambda t: t[1])
        bothany = [(i, abs(hp[i]['E'] - hm[i]['E']) / max(abs(hm[i]['E']), abs(hp[i]['E']))) for i in common if i > 0 and sum(hp[i]['nseg']) and sum(hm[i]['nseg'])]
        ma = max(bothany, key=lambda t: t[1])
        absmax = max((abs(hp[i]['E'] - hm[i]['E']), i) for i in common)
        print(f"     P3 while strand 1's line exists in both runs (it <= {both1[-1][0]}): max rel dE {m1[1]:.4f} at it {m1[0]} (|dE| {m1[2]:.1f}); "
              f"while any line exists in both: max {ma[1]:.4f} at it {ma[0]}; max |dE| over all matched records {absmax[0]:.2f} at it {absmax[1]}")
        for lab, run in (('+', rp), ('-', rm)):
            Es = [d['E'] for d in run['history']]
            inc = [run['history'][k]['it'] for k in range(1, len(Es)) if Es[k] > Es[k - 1]]
            print(f"     E monotone non-increasing over records ({lab}): {not inc} {inc[:5]}")
        print('     E(+)/E(-)/E(0) at it:', ' '.join(e0))
