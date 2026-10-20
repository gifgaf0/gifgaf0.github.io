"""E5 cross-check: electric charges of the SU(3) rotor states, via Gelfand-Tsetlin patterns
(independent of the original's branching-rule / weight-peeling code).

GT pattern for SU(3) irrep (p,q): top row (p+q, q, 0), middle (m12, m22), bottom m11 with interlacing.
  I = (m12 - m22)/2,  I3 = m11 - (m12 + m22)/2,  Y = (m12 + m22) - (2/3)(p + 2q).
Charges with left-gauged Q = diag(2/3,-1/3,-1/3) are Q = I3 + Y/2.  Allowed irreps (WZ constraint) contain
right hypercharge Y_R = N_c/3; spin J = isospin of the Y = N_c/3 states.
"""
import json
import os
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))


def states(p, q):
    top = (p + q, q, 0)
    out = []
    for m12 in range(top[1], top[0] + 1):
        for m22 in range(top[2], top[1] + 1):
            for m11 in range(m22, m12 + 1):
                I = Fr(m12 - m22, 2)
                I3 = Fr(m11) - Fr(m12 + m22, 2)
                Y = Fr(m12 + m22) - Fr(2, 3) * (p + 2 * q)
                out.append((I, I3, Y))
    return out


def dim(p, q):
    return (p + 1) * (q + 1) * (p + q + 2) // 2


def casimir(p, q):
    return Fr(p * p + q * q + p * q + 3 * p + 3 * q, 3)


def allowed(Nc, pmax=6):
    YR = Fr(Nc, 3)
    res = []
    for p in range(pmax + 1):
        for q in range(pmax + 1):
            st = states(p, q)
            assert len(st) == dim(p, q)
            Js = sorted({s[0] for s in st if s[2] == YR})
            if Js:
                res.append(((p, q), Js, st))
    res.sort(key=lambda r: (casimir(*r[0]), r[0]))
    return res


log = []
names = {(1, 1): '8', (3, 0): '10', (0, 3): '10bar', (2, 2): '27'}
summary = {}
allint = True
for (pq, Js, st) in allowed(3)[:6]:
    Q = sorted({s[1] + s[2] / 2 for s in st})
    integ = all(x.denominator == 1 for x in Q)
    # Gell-Mann-Nishijima with S = Y - B (B = 1): Q = I3 + (B + S)/2 holds identically; check charge range
    nm = names.get(pq, str(pq))
    if pq in names:
        allint &= integ
        summary[nm] = {'pq': pq, 'dim': dim(*pq), 'J': [str(j) for j in Js], 'charges': [str(x) for x in Q],
                       'integer': integ,
                       'exotics': sorted({(str(s[0]), str(s[2]), str(s[1] + s[2] / 2)) for s in st
                                          if s[2] == 2 or (s[1] + s[2] / 2) in (2, -2)})}
    log.append(f'{nm:6s} (p,q)={pq} dim={dim(*pq):3d} C2={casimir(*pq)} J={[str(j) for j in Js]} charges={[str(x) for x in Q]} integer={integ}')
# SU(2): Q = I3 + B/2 for I = J
su2 = {str(Fr(2 * k + 1, 2)): [str(Fr(m, 2) + Fr(1, 2)) for m in range(2 * k + 1, -2 * k - 2, -2)] for k in range(3)}
log.append(f'SU(2) I=J: charges {su2}')
# check: Y=1 members of every SU(3) irrep reproduce Q = I3 + 1/2
ok = all((s[1] + s[2] / 2) == s[1] + Fr(1, 2) for (pq, Js, st) in allowed(3)[:6] for s in st if s[2] == 1)
log.append(f'Y=1 members obey Q = I3 + B/2: {ok};  all charges of 8,10,10bar,27 integer: {allint}')
# N_c dependence (extra in the original): nonstrange members of the lowest irrep, fixed quark charges
nc_rows = []
for Nc in (1, 3, 5, 7, 9):
    pq, Js, st = allowed(Nc)[0]
    YR = Fr(Nc, 3)
    Qs = sorted({s[1] + s[2] / 2 for s in st if s[2] == YR})
    nc_rows.append({'N_c': Nc, 'lowest': pq, 'J': [str(j) for j in Js], 'Q_fixed_charges_YR_states': [str(x) for x in Qs]})
    log.append(f'N_c={Nc}: lowest {pq} J={[str(j) for j in Js]} Q(Y=N_c/3 states, fixed quark charges)={[str(x) for x in Qs]}')
for line in log:
    print(line)
json.dump({'irreps': summary, 'su2': su2, 'Y1_obeys_I3_plus_half': ok, 'all_integer': allint, 'Nc_rows': nc_rows},
          open(os.path.join(HERE, 'cc_charges.json'), 'w'), indent=1, default=str)
open(os.path.join(HERE, 'cc_charges_log.txt'), 'w').write('\n'.join(log) + '\n')
