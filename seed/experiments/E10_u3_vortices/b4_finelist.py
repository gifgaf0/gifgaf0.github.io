"""Runs whose h = 0.25 end state is non-collapsing (b4_analyse.classify != collapse): re-relaxed at h = 0.125."""
import b4_analyse as A
for k in ('M3a', 'M3b', 'M5a', 'M5b', 'C-a', 'C-b', 'C-c', 'C-d', 'C-d5'):
    r = A.load(k)
    if r is None or 'end' not in r:
        continue
    if k.startswith('C-d'):
        print(k); continue          # no vortex by construction: 'non-collapsing' read as 'every no-vortex end state'
    if A.classify(r)['cls'] != 'collapse':
        print(k)
