#!/usr/bin/env python3
# arm_mapper.py — Gate G-TSH2, P4. QUARANTINED: thresholds live only here; run after the P3 freeze.
# Lock: G_TSH2_PREREGISTRATION_LOCKED.md, md5 99eb26a5d8ff1e32c54d5cff40386098. A-2 semantics.
import json
TH1, TH2 = 0.03, 0.10
R = json.load(open('/home/claude/gtsh2/gtsh2_results.json'))
anch = R['anchors']
PW = list(anch['step_RT']) + list(anch['gam6_RT'])
used, excluded = [], []
for K in ('K3', 'K4', 'K5'):
    d = R['kernels'][K]
    if d.get('excluded') or 'R_T' not in d:
        excluded.append((K, d.get('flags')))
    else:
        PW.append(d['R_T']); used.append(K)
K6 = R['kernels']['K6']
if K6.get('excluded') or 'R_T' not in K6:
    PX = None; excluded.append(('K6', K6.get('flags')))
else:
    PX = PW + [K6['R_T']]
def D(pool):
    m = sum(pool)/len(pool)
    return max(abs(x - m)/m for x in pool), m
DW, mW = D(PW)
print(f"P_W ({len(PW)} pts): {[round(x,5) for x in PW]}")
print(f"D_W = {100*DW:.3f}%  (mean {mW:.5f})")
if PX is None:
    print("K6 excluded -> D_X unavailable; reachable arms restrict to {KNOB, UNDERDETERMINED-2}")
    arm = 'KNOB' if DW > TH2 else 'UNDERDETERMINED-2'
    DX = None
else:
    DX, mX = D(PX)
    print(f"P_X ({len(PX)} pts): {[round(x,5) for x in PX]}")
    print(f"D_X = {100*DX:.3f}%  (mean {mX:.5f})")
    if DW <= TH1 and DX <= TH1:
        arm = 'DERIVED-RATIO'
    elif DW <= TH1 and DX > TH2:
        arm = 'KERNEL-CLASS-PINNED'
    elif DW > TH2:
        arm = 'KNOB'
    else:
        arm = 'UNDERDETERMINED-2'
print("excluded kernels:", excluded)
print("ARM VERDICT:", arm)
json.dump(dict(D_W=DW, D_X=DX, arm=arm, pool_W=PW, pool_X=PX,
               excluded=[e[0] for e in excluded]),
          open('/home/claude/gtsh2/arm_verdict.json', 'w'), indent=1)
