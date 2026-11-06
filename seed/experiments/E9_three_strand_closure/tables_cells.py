"""Print the per-start tables of REPORT_N1_cells.md from the trace JSONs: every recorded row (every 2
iterations) up to the first row with no vortex lines in any strand, then the final record.
usage: python3 tables_cells.py trace_N1_*_k*.json"""
import json, sys
def f(x, n=2): return f'{x:.{n}f}'
for tag in sys.argv[1:]:
    d = json.load(open(tag)); H = d['history']
    stop = next(i for i, r in enumerate(H) if sum(r['nseg']) == 0)
    rows = H[:stop + 1] + [dict(d['final'], final=True)]
    print(f'\n{tag}: iters={d["final"]["iters"]}, converged={d["final"]["converged"]}, msg={d["final"]["msg"]}\n')
    print('| it | E | R comp. | length comp. | R line 1 | centroid x line 1 | z_rms line 1 | length line 1 | wall gap 1 | open ends | W_z(1) | sep min / mean | Lk₁₂ |')
    print('|' + '---|' * 13)
    for r in rows:
        l1 = r.get('line1'); l2 = r.get('line2')
        sep = f"{r['gap12_min']:.2f} / {r['gap12_mean']:.2f}" if 'gap12_min' in r else '—'
        E = f"{r['E']:.3g}" if r['E'] < 1 else f"{r['E']:.1f}"
        lk = f"{r['Lk12']:.3f}" if l1 and l2 else '0 (no line 1)' if l2 else '0 (no lines)'
        print(f"| {r['it']}{' (final)' if r.get('final') else ''} | {E} | {f(l2['rxy_mean']) if l2 else '—'} | {f(l2['length'],1) if l2 else '0'} "
              f"| {f(l1['rxy_mean']) if l1 else '—'} | {f(l1['centroid'][0]) if l1 else '—'} | {f(l1['z_rms']) if l1 else '—'} | {f(l1['length'],1) if l1 else '0'} "
              f"| {f(l1['wall_gap']) if l1 else '—'} | {l1['open_ends'] if l1 else '—'} | {round(l1['Wz']) if l1 else '—'} | {sep} | {lk} |")
