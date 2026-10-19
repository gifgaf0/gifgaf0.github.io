"""Cross-check E2, step 4: SU(3) rigid rotor with Gelfand-Tsetlin patterns + exact Haar integrals.

Independent of the original's method (explicit tensor-power irreps and CG null spaces):
  * irrep content of (p,q) from Gelfand-Tsetlin patterns: top row (p+q, q, 0),
      m13 >= m12 >= m23 >= m22 >= m33,  m12 >= m11 >= m22,
      I = (m12-m22)/2, I3 = m11-(m12+m22)/2, Y = m12+m22-(2/3)(p+2q);
    checked against the Weyl dimension formula and the second-order index
    sum_states I3^2 = sum_states (3/4) Y^2 = C2 dim/8, with C2 = (p^2+q^2+pq+3p+3q)/3.
  * Wess-Zumino constraint Y_R = N_c B/3 (imported from Witten 1983 / DPP, as in the report);
    J = isospin of the Y = N_c/3 states.
  * rotor E = M + C2/(2I2) + (1/(2I1)-1/(2I2)) J(J+1) - N_c^2/(24 I2)   (DPP hep-ph/9703373)
  * collective matrix elements <R nu, s|D_ab|R nu, s> = d_R int dA |D^R_{nu s}(A)|^2 D_ab(A)
    evaluated EXACTLY by Weingarten calculus on U(3) (= SU(3) for these balanced polynomials),
    with the Weingarten function from the pseudo-inverse of the Gram matrix d^{#cycles}.
  * PDG 2026 masses read independently through the pdg package.
Inputs: the hedgehog numbers M, Lambda, J2, C from xc_hedgehog.json (my own shooting run).
Writes xc_rotor.json.  Deterministic.
"""
import json, math, time, itertools
from fractions import Fraction as Fr
import numpy as np
import sympy as sp

OUT = '/home/user/gifgaf0.github.io/seed/experiments/E2_skyrme_su3/crosscheck/'
t0 = time.time()
H = json.load(open(OUT + 'xc_hedgehog.json'))
Mc, Lam, J2, Cc = H['M'], H['Lambda'], H['J2'], H['C']
I1c = 2*math.pi/3*Lam
I2c = math.pi/2*J2
ratio = I1c/I2c
checks = {}


# ---------------------------------------------------------------- Gelfand-Tsetlin content
def gt_states(p, q):
    m13, m23, m33 = p + q, q, 0
    out = []
    for m12 in range(m23, m13 + 1):
        for m22 in range(m33, m23 + 1):
            for m11 in range(m22, m12 + 1):
                I2 = m12 - m22                      # 2I
                I3x2 = 2*m11 - (m12 + m22)          # 2 I3
                Yx3 = 3*(m12 + m22) - 2*(p + 2*q)   # 3Y
                out.append((I2, I3x2, Yx3))
    return out


def dim(p, q):
    return (p + 1)*(q + 1)*(p + q + 2)//2


def C2(p, q):
    return Fr(p*p + q*q + p*q + 3*p + 3*q, 3)


def name(p, q):
    d = dim(p, q)
    s = str(d)
    if q > p:
        s += 'bar'
    # distinguish inequivalent irreps of equal dimension
    same = [(a, b) for a in range(0, 40) for b in range(0, 40) if dim(a, b) == d and a >= b]
    if len(same) > 1 and (max(p, q), min(p, q)) != same[0]:
        s += "'"*same.index((max(p, q), min(p, q)))
    return s + '(%d,%d)' % (p, q)


bad = []
for p in range(0, 17):
    for q in range(0, 17 - p):
        st = gt_states(p, q)
        if len(st) != dim(p, q):
            bad.append(('dim', p, q))
        sI3 = sum(Fr(s[1], 2)**2 for s in st)
        sY = sum(Fr(3, 4)*Fr(s[2], 3)**2 for s in st)
        if not (sI3 == sY == C2(p, q)*dim(p, q)/8):
            bad.append(('index', p, q))
        # every isospin multiplet complete: count of each (I,Y) is a multiple of 2I+1 and multiplicity-free
        from collections import Counter
        cnt = Counter((s[0], s[2]) for s in st)
        if any(v != k[0] + 1 for k, v in cnt.items()):
            bad.append(('mult', p, q))
checks['GT patterns: dimension, index sum rule, multiplicity-free U(2) branching (p+q<=16)'] = not bad
print('GT consistency failures:', bad)


def allowed(Nc, pqmax):
    """list of (p,q,J) with a Y = Nc/3 isospin multiplet of isospin J."""
    res = []
    for p in range(0, pqmax + 1):
        for q in range(0, pqmax + 1 - p):
            Js = sorted({Fr(s[0], 2) for s in gt_states(p, q) if s[2] == Nc})   # 3Y == Nc
            for J in Js:
                res.append((p, q, J))
    return res


def Erot(p, q, J, Nc, invI1, invI2):
    """rotor energy above M (MeV if invI in MeV)"""
    J = float(J)
    return float(C2(p, q))*invI2/2 + (invI1/2 - invI2/2)*J*(J + 1) - Nc*Nc*invI2/24


# ------------------------------------------------- N_c parity and lowest multiplets
parity = {}
lowest = {}
for Nc in range(1, 16):
    pqmax = 16 if Nc <= 7 else 30
    al = allowed(Nc, pqmax)
    ok = all((int(2*J) - Nc) % 2 == 0 for (_, _, J) in al)
    tri = all((p - q - Nc) % 3 == 0 for (p, q, _) in al)
    parity[Nc] = dict(n_states=len(al), parity_ok=ok, triality_ok=tri)
    # order with the profile's I1/I2 (any overall scale): units 1/I1 = 1
    lev = sorted(al, key=lambda t: (Erot(t[0], t[1], t[2], Nc, 1.0, ratio), t))
    lowest[Nc] = [(name(p, q), str(J), Erot(p, q, J, Nc, 1.0, ratio) - Erot(*lev[0], Nc, 1.0, ratio)) for p, q, J in lev[:6]]
checks['N_c parity: 2J = N_c mod 2 for every allowed state, N_c = 1..15'] = all(v['parity_ok'] for v in parity.values())
checks['allowed irreps have triality p-q = N_c mod 3'] = all(v['triality_ok'] for v in parity.values())
for Nc in range(1, 8):
    print('N_c=%d:' % Nc, ', '.join('%s J=%s' % (a, b) for a, b, _ in lowest[Nc][:4]))

# ---------------------------------------------------------- exact level differences
i1, i2 = sp.symbols('I1 I2', positive=True)
def Esym(p, q, J, Nc=3):
    J = sp.Rational(J.numerator, J.denominator)
    return sp.Rational(C2(p, q).numerator, C2(p, q).denominator)/(2*i2) + (1/(2*i1) - 1/(2*i2))*J*(J + 1) - sp.Rational(Nc*Nc, 24)/i2
E8 = Esym(1, 1, Fr(1, 2)); E10 = Esym(3, 0, Fr(3, 2)); E10b = Esym(0, 3, Fr(1, 2))
E27a = Esym(2, 2, Fr(3, 2)); E27b = Esym(2, 2, Fr(1, 2))
ESU2N = sp.Rational(3, 8)/i1
diffs = {'E8-M': sp.simplify(E8), 'E10-E8': sp.simplify(E10 - E8), 'E10bar-E8': sp.simplify(E10b - E8),
         'E27(3/2)-E10bar': sp.simplify(E27a - E10b), 'E8-ESU2(N)': sp.simplify(E8 - ESU2N)}
for k, v in diffs.items():
    print('  %-16s = %s' % (k, v))
checks['E(10)-E(8) = 3/(2I1) exactly'] = sp.simplify(diffs['E10-E8'] - sp.Rational(3, 2)/i1) == 0
checks['E(10bar)-E(8) = 3/(2I2) exactly'] = sp.simplify(diffs['E10bar-E8'] - sp.Rational(3, 2)/i2) == 0
checks['E(8)-E_SU2(N) = 3/(4I2) exactly'] = sp.simplify(diffs['E8-ESU2(N)'] - sp.Rational(3, 4)/i2) == 0
low3 = [(a, b) for a, b, _ in lowest[3][:4]]
checks['lowest Y_R=1 multiplets: 8(1/2), 10(3/2), 10bar(1/2), then 27'] = (
    low3[0] == ('8(1,1)', '1/2') and low3[1] == ('10(3,0)', '3/2') and low3[2] == ('10bar(0,3)', '1/2')
    and low3[3][0].startswith('27'))

# ---------------------------------------------------------------- PDG inputs and fits
import warnings
warnings.filterwarnings('ignore')
import pdg
api = pdg.connect()
mm = lambda mc: api.get_particle_by_mcid(mc).mass*(1000 if api.get_particle_by_mcid(mc).mass < 10 else 1)
raw = {'p': mm(2212), 'n': mm(2112), 'Lambda': mm(3122), 'Sigma+': mm(3222), 'Sigma0': mm(3212),
       'Sigma-': mm(3112), 'Xi0': mm(3322), 'Xi-': mm(3312), 'Sigma*+': mm(3224), 'Sigma*0': mm(3214),
       'Sigma*-': mm(3114), 'Xi*0': mm(3324), 'Xi*-': mm(3314), 'Omega-': mm(3334)}
dsum = api.get('B033M').summary_values()[0]
raw['Delta'] = float(dsum.value)
iso = {'N': (raw['p'] + raw['n'])/2, 'Lambda': raw['Lambda'],
       'Sigma': (raw['Sigma+'] + raw['Sigma0'] + raw['Sigma-'])/3, 'Xi': (raw['Xi0'] + raw['Xi-'])/2,
       'Delta': raw['Delta'], 'Sigma*': (raw['Sigma*+'] + raw['Sigma*0'] + raw['Sigma*-'])/3,
       'Xi*': (raw['Xi*0'] + raw['Xi*-'])/2, 'Omega': raw['Omega-']}
c8 = (2*iso['N'] + iso['Lambda'] + 3*iso['Sigma'] + 2*iso['Xi'])/8
c10 = (4*iso['Delta'] + 3*iso['Sigma*'] + 2*iso['Xi*'] + iso['Omega'])/10
print('PDG 2026 isospin averages:', {k: round(v, 3) for k, v in iso.items()})
print('octet centre %.4f  decuplet centre %.4f' % (c8, c10))


def params_from(invI1, Mcl):
    Fe = Mcl/Mc                    # F_pi/e  [MeV]
    e3F = invI1*I1c                # e^3 F_pi [MeV]
    e = (e3F/Fe)**0.25
    return dict(e=e, Fpi=Fe*e, invI1=invI1, invI2=e3F/I2c, Mcl=Mcl, eF=e*Fe*e)


# ANW: SU(2) rotor, M_N = M + 3/(8I1), M_D = M + 15/(8I1)
anw = params_from((1232.0 - 939.0)/1.5, 939.0 - 0.375*(1232.0 - 939.0)/1.5)
# SU(3) refit: E(8) = c8, E(10) = c10, I1/I2 from the profile
invI1r = (c10 - c8)/1.5
invI2r = invI1r*ratio
ref = params_from(invI1r, c8 - 0.375*invI1r - 0.75*invI2r)
assert abs(ref['invI2'] - invI2r) < 1e-9
for tag, P in (('ANW', anw), ('SU3refit', ref)):
    P['gA_SU2'] = 2*math.pi*Cc/(3*P['e']**2)
    lv = sorted(allowed(3, 12), key=lambda t: Erot(*t, 3, P['invI1'], P['invI2']))
    P['levels'] = [(name(p, q), str(J), P['Mcl'] + Erot(p, q, J, 3, P['invI1'], P['invI2'])) for p, q, J in lv[:10]]
    P['E8_minus_ESU2N'] = 0.75*P['invI2']
    print('%-8s F_pi = %.4f MeV  e = %.5f  1/I1 = %.3f  1/I2 = %.3f  M_cl = %.3f  g_A(SU2 form) = %.4f' %
          (tag, P['Fpi'], P['e'], P['invI1'], P['invI2'], P['Mcl'], P['gA_SU2']))
    print('          levels:', '; '.join('%s J=%s %.1f' % t for t in P['levels'][:9]))

# ------------------------------------------------ exact Haar integrals (Weingarten calculus)
def perms(n):
    return list(itertools.permutations(range(n)))


def ncycles(pm):
    seen = set(); c = 0
    for i in range(len(pm)):
        if i not in seen:
            c += 1; j = i
            while j not in seen:
                seen.add(j); j = pm[j]
    return c


WG = {}
def weingarten(n, d):
    if (n, d) not in WG:
        P = perms(n)
        idx = {pm: k for k, pm in enumerate(P)}
        inv = lambda pm: tuple(np.argsort(pm))
        comp = lambda a, b: tuple(a[b[i]] for i in range(n))
        G = np.array([[float(d)**ncycles(comp(inv(s), t)) for t in P] for s in P])
        Wm = np.linalg.pinv(G)
        WG[(n, d)] = (P, {pm: Wm[0, idx[pm]] for pm in P})   # Wg(sigma) = Wm[e, sigma]
    return WG[(n, d)]


def haar(poly, d):
    """poly: dict {(Aidx tuple, Abaridx tuple): coeff}, Aidx = ((i,j),...) ; returns int dU over U(d)."""
    tot = 0.0
    for (a, b), c in poly.items():
        n = len(a)
        if n != len(b):
            continue
        if n == 0:
            tot += c; continue
        P, W = weingarten(n, d)
        for s in P:
            if any(a[k][0] != b[s[k]][0] for k in range(n)):
                continue
            for t in P:
                if any(a[k][1] != b[t[k]][1] for k in range(n)):
                    continue
                # sigma, tau -> Wg(tau sigma^-1)
                sinv = tuple(np.argsort(s))
                w = tuple(t[sinv[i]] for i in range(n))
                tot += c*W[w]
    return tot


def pmul(x, y):
    out = {}
    for (a1, b1), c1 in x.items():
        for (a2, b2), c2 in y.items():
            k = (tuple(sorted(a1 + a2)), tuple(sorted(b1 + b2)))
            out[k] = out.get(k, 0) + c1*c2
    return {k: v for k, v in out.items() if abs(v) > 1e-15}


def pconj(x):
    return {(b, a): np.conj(c) for (a, b), c in x.items()}


def adjD(Xl, Xr, d):
    """<Xl| A Xr A^+ > = Tr(Xl^+ A Xr A^+) as polynomial; Xl, Xr dxd matrices."""
    out = {}
    for i, j, k, l in itertools.product(range(d), repeat=4):
        c = np.conj(Xl[j, i])*Xr[k, l]          # Tr(Xl^+ A Xr A^+) = sum Xl^+_{ij} A_jk Xr_kl conj(A_il)
        if c != 0:
            key = (((j, k),), ((i, l),))
            out[key] = out.get(key, 0) + c
    return out


lam = np.zeros((8, 3, 3), complex)
lam[0][0, 1] = lam[0][1, 0] = 1; lam[1][0, 1] = -1j; lam[1][1, 0] = 1j
lam[2][0, 0] = 1; lam[2][1, 1] = -1; lam[3][0, 2] = lam[3][2, 0] = 1
lam[4][0, 2] = -1j; lam[4][2, 0] = 1j; lam[5][1, 2] = lam[5][2, 1] = 1
lam[6][1, 2] = -1j; lam[6][2, 1] = 1j; lam[7] = np.diag([1, 1, -2])/math.sqrt(3)
Dab = lambda a, b, d=3: {k: v/2 for k, v in adjD(lam[a][:d, :d].conj().T, lam[b][:d, :d], d).items()}  # (1/2)Tr(l_a A l_b A^+)


def E(i, j, d=3):
    m = np.zeros((d, d), complex); m[i, j] = 1; return m


# octet states (adjoint, Hilbert-Schmidt normalised): weight of E_ij is w_i - w_j, w = u,d,s
oct_states = {'p': E(0, 2), 'n': E(1, 2), 'Sigma+': E(0, 1), 'Sigma0': (E(0, 0) - E(1, 1))/math.sqrt(2),
              'Lambda': (E(0, 0) + E(1, 1) - 2*E(2, 2))/math.sqrt(6), 'Xi0': E(2, 1), 'Xi-': E(2, 0)}
# right index: Y_R = +1, J = 1/2: s_up/s_dn = E_13 / E_23 (T_R3 = +1/2 / -1/2)
s_up, s_dn = E(0, 2), E(1, 2)


def melem(state, s, a, b):
    D = adjD(state, s, 3)
    return 8*haar(pmul(pmul(D, pconj(D)), Dab(a, b)), 3).real


norm_chk = 8*haar(pmul(adjD(oct_states['p'], s_up, 3), pconj(adjD(oct_states['p'], s_up, 3))), 3).real
D33_SU3 = {'s=E13': melem(oct_states['p'], s_up, 2, 2), 's=E23': melem(oct_states['p'], s_dn, 2, 2)}
# SU(2): spin-1/2 wave function D^{1/2}_{m s}(A) = A_{ms}; D_33 = (1/2)Tr(tau3 A tau3 A^+)
A11 = {(((0, 0),), ()): 1.0}; A12 = {(((0, 1),), ()): 1.0}
D33_SU2 = {'s=1': 2*haar(pmul(pmul(A11, pconj(A11)), Dab(2, 2, 2)), 2).real,
           's=2': 2*haar(pmul(pmul(A12, pconj(A12)), Dab(2, 2, 2)), 2).real}
print('normalisation 8 int |D_ps|^2 = %.12f' % norm_chk)
print('<p|D33|p>: SU(2)', D33_SU2, '  SU(3) octet', D33_SU3)
gA_factor = abs(D33_SU3['s=E13'])/abs(D33_SU2['s=1'])
checks['SU(2) |<p|D33|p>| = 1/3'] = abs(abs(D33_SU2['s=1']) - 1/3) < 1e-12 and abs(D33_SU2['s=1'] + D33_SU2['s=2']) < 1e-12
checks['SU(3) octet |<p|D33|p>| = 7/30, ratio 7/10'] = abs(abs(D33_SU3['s=E13']) - 7/30) < 1e-12 and abs(gA_factor - 0.7) < 1e-12

# D88 in the octet and in the decuplet
D88_oct = {k: melem(v, s_up, 7, 7) for k, v in oct_states.items()}
D88_oct_dn = {k: melem(v, s_dn, 7, 7) for k, v in oct_states.items()}
print('octet <D88>:', {k: round(v, 12) for k, v in D88_oct.items()})


def sym3(occ):
    """normalised symmetric tensor for occupation (n_u, n_d, n_s) -> list of (index triple, amp)."""
    idx = [0]*occ[0] + [1]*occ[1] + [2]*occ[2]
    ps = sorted(set(itertools.permutations(idx)))
    a = 1/math.sqrt(len(ps))
    return [(t, a) for t in ps]


def decD(occl, occr):
    """<l| A x A x A |r> as polynomial"""
    out = {}
    for tl, al in sym3(occl):
        for tr, ar in sym3(occr):
            key = (tuple(sorted(zip(tl, tr))), ())
            out[key] = out.get(key, 0) + al*ar
    return out


dec_states = {'Delta++': (3, 0, 0), 'Delta0': (1, 2, 0), 'Sigma*+': (2, 0, 1), 'Sigma*0': (1, 1, 1),
              'Xi*0': (1, 0, 2), 'Omega-': (0, 0, 3)}
sR = (3, 0, 0)      # Y_R = 1, J = 3/2, J3 = 3/2 (any J3: D_88 is right-isoscalar)
D88_dec = {}
for k, occ in dec_states.items():
    D = decD(occ, sR)
    nrm = 10*haar(pmul(D, pconj(D)), 3).real
    D88_dec[k] = 10*haar(pmul(pmul(D, pconj(D)), Dab(7, 7)), 3).real
    assert abs(nrm - 1) < 1e-12, nrm
print('decuplet <D88>:', {k: round(v, 12) for k, v in D88_dec.items()})
exp_oct = {'p': 0.3, 'n': 0.3, 'Lambda': 0.1, 'Sigma+': -0.1, 'Sigma0': -0.1, 'Xi0': -0.2, 'Xi-': -0.2}
exp_dec = {'Delta++': 1/8, 'Delta0': 1/8, 'Sigma*+': 0.0, 'Sigma*0': 0.0, 'Xi*0': -1/8, 'Omega-': -1/4}
checks['<D88> octet (N,L,S,X) = (3,1,-1,-2)/10, decuplet = Y/8'] = (
    all(abs(D88_oct[k] - v) < 1e-12 for k, v in exp_oct.items()) and
    all(abs(D88_dec[k] - v) < 1e-12 for k, v in exp_dec.items()))

# optional first-order breaking H' = -alpha D88 + beta Y, centres fixed at the PDG centres
mult = [('N', c8, 0.3, 1), ('Lambda', c8, 0.1, 0), ('Sigma', c8, -0.1, 0), ('Xi', c8, -0.2, -1),
        ('Delta', c10, 1/8, 1), ('Sigma*', c10, 0.0, 0), ('Xi*', c10, -1/8, -1), ('Omega', c10, -0.25, -2)]
Amat = np.array([[-d, y] for _, _, d, y in mult]); bvec = np.array([iso[n] - c for n, c, _, _ in mult])
(alpha, beta), *_ = np.linalg.lstsq(Amat, bvec, rcond=None)
resid = bvec - Amat@np.array([alpha, beta])
rms = math.sqrt(np.mean(resid**2))
print('first-order fit (unweighted, 8 multiplets): alpha = %.2f MeV, beta = %.2f MeV, rms = %.2f MeV, max |res| %.2f (%s)'
      % (alpha, beta, rms, np.max(np.abs(resid)), mult[int(np.argmax(np.abs(resid)))][0]))
guad = 8*(iso['N'] + iso['Xi*']) + 3*iso['Sigma'] - (11*iso['Lambda'] + 8*iso['Sigma*'])
gmo = 2*(iso['N'] + iso['Xi']) - (3*iso['Lambda'] + iso['Sigma'])
sp1 = (iso['Sigma*'] - iso['Delta']) - (iso['Xi*'] - iso['Sigma*'])
sp2 = (iso['Xi*'] - iso['Sigma*']) - (iso['Omega'] - iso['Xi*'])
print('Guadagnini LHS-RHS %.3f MeV (%.4f%%); GMO %.3f MeV (%.3f%%); spacing %.2f, %.2f MeV' %
      (guad, 100*guad/(11*iso['Lambda'] + 8*iso['Sigma*']), gmo, 100*gmo/(3*iso['Lambda'] + iso['Sigma']), sp1, sp2))

# degeneracy under exact SU(3): H_rot depends only on C2(p,q) and J(J+1) -> each (R,J) block is
# d_R (2J+1)-fold degenerate.  (Nothing to compute beyond the formula; recorded as such.)

for k, v in checks.items():
    print('CHECK %-85s %s' % (k, 'PASS' if v else 'FAIL'))
out = dict(I1_coef=I1c, I2_coef=I2c, I1_over_I2=ratio, parity={str(k): v for k, v in parity.items()},
           lowest={str(k): v for k, v in lowest.items()}, level_differences={k: str(v) for k, v in diffs.items()},
           pdg_raw=raw, pdg_iso=iso, octet_centre=c8, decuplet_centre=c10, ANW=anw, SU3refit=ref,
           D33_SU2=D33_SU2, D33_SU3=D33_SU3, gA_SU3_factor=gA_factor, D88_octet=D88_oct, D88_octet_sdn=D88_oct_dn,
           D88_decuplet=D88_dec, breaking_fit=dict(alpha=alpha, beta=beta, rms=rms, residuals=dict(zip([m[0] for m in mult], resid))),
           guadagnini=guad, gmo=gmo, spacing=[sp1, sp2],
           checks=checks, all_pass=all(checks.values()), runtime_s=time.time() - t0)
json.dump(out, open(OUT + 'xc_rotor.json', 'w'), indent=1, default=lambda o: float(o) if not isinstance(o, (Fr,)) else str(o))
print('all checks pass:', all(checks.values()), ' runtime %.1f s' % (time.time() - t0))
