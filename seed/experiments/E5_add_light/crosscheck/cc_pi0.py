"""E5 cross-check: pi0 -> gamma gamma from the gauged Wess-Zumino term (independent derivation).

Starting point (read in the source): Bernstein & Holstein, arXiv:1112.4809v2, eq. (67)-(68):
  L_A = -(N_c/48 pi^2) eps^{mu nu a b} [ e A_mu Tr(Q L_nu L_a L_b - Q R_nu R_a R_b) + i e^2 F_{mu nu} A_a T_b ]
  T_b = Tr[Q^2 L_b - Q^2 R_b + (1/2) Q U Q U^+ L_b - (1/2) Q U^+ Q U R_b],  L = dU U^+, R = dU^+ U,
  U = exp(i tau.pi/F_pi) with F_pi = 92.21 MeV (their eq. 1 convention).
Steps (sympy):
  1. expand T_b to first order in the pion fields (explicit 2x2 matrices);
  2. read off L = c eps F A d pi0 ;
  3. compute the decay amplitude by substituting plane waves (explicit momenta and polarisation vectors in
     the pi0 rest frame, all index placements explicit), sum |M|^2 over photon polarisations, and form
     Gamma = sum|M|^2 / (32 pi m)  (two-body phase space, 1/2 for identical photons);
  4. compare with alpha^2 m^3 N_c^2 / (576 pi^3 f^2) and evaluate with PDG 2026 / PrimEx-II.
"""
import json
import os

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
out = {}
LOG = []


def log(*a):
    s = ' '.join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


f, e, Nc, m = sp.symbols('f e N_c m', positive=True)
p1, p2, p3 = sp.symbols('pi1 pi2 pi3', real=True)
d1, d2, d3 = sp.symbols('dpi1 dpi2 dpi3', real=True)      # d_beta pi^a at fixed beta
t = sp.symbols('t')                                      # bookkeeping for first order
t1 = sp.Matrix([[0, 1], [1, 0]]); t2 = sp.Matrix([[0, -sp.I], [sp.I, 0]]); t3 = sp.Matrix([[1, 0], [0, -1]])
one = sp.eye(2)


def T_beta(Q):
    phi = t * (p1 * t1 + p2 * t2 + p3 * t3) / f
    dphi = t * (d1 * t1 + d2 * t2 + d3 * t3) / f
    # U = exp(i phi) to second order in t (enough for first-order T after products)
    U = one + sp.I * phi - phi * phi / 2
    Ud = one - sp.I * phi - phi * phi / 2
    dU = sp.I * dphi - (dphi * phi + phi * dphi) / 2
    dUd = -sp.I * dphi - (dphi * phi + phi * dphi) / 2
    Lb = dU * Ud
    Rb = dUd * U
    T = (Q * Q * Lb - Q * Q * Rb + sp.Rational(1, 2) * Q * U * Q * Ud * Lb - sp.Rational(1, 2) * Q * Ud * Q * U * Rb).trace()
    T = sp.expand(T)
    return sp.simplify(T.coeff(t, 1)), sp.simplify(T.coeff(t, 0))


Qstd = sp.diag(sp.Rational(2, 3), -sp.Rational(1, 3))
T1, T0 = T_beta(Qstd)
log('T_beta at first order (standard charges):', T1, '  zeroth order:', T0)
out['T_beta_first_order'] = str(T1)
# general charges Q = diag(qu, qd)
qu, qd = sp.symbols('q_u q_d')
T1g, _ = T_beta(sp.diag(qu, qd))
log('T_beta at first order, Q = diag(qu,qd):', sp.factor(T1g))

# coefficient: L = -(N_c/48 pi^2) i e^2 eps F_{mu nu} A_a T_b  ->  L = cF eps F_{mu nu} A_a d_b pi0
cF = sp.simplify(-(Nc / (48 * sp.pi ** 2)) * sp.I * e ** 2 * T1.coeff(d3))
log('L = cF eps^{mu nu a b} F_{mu nu} A_a d_b pi0 with cF =', cF)
out['cF_coefficient_of_epsFAdpi'] = str(cF)
out['coefficient_of_eps_dA_A_dpi'] = str(sp.simplify(2 * cF))

# ---------------------------------------------------------------- amplitude with explicit vectors
g = sp.diag(1, -1, -1, -1)
eps4 = sp.LeviCivita


def lower(v):
    return [sum(g[i, j] * v[j] for j in range(4)) for i in range(4)]


k1u = [m / 2, 0, 0, m / 2]
k2u = [m / 2, 0, 0, -m / 2]
pu = [k1u[i] + k2u[i] for i in range(4)]
pols = [[0, 1, 0, 0], [0, 0, 1, 0]]          # transverse to both photons (along z)
k1, k2, pp = lower(k1u), lower(k2u), lower(pu)


def amp(e1u, e2u):
    e1, e2 = lower(e1u), lower(e2u)
    # plane waves: A -> e1 e^{ik1x} + e2 e^{ik2x} (outgoing: d -> +ik), pi -> e^{-ipx} (d -> -ip)
    # F_{mu nu}(photon j) = i(k_mu e_nu - k_nu e_mu);  the bilinear term has photon 1 in F and 2 in A, + (1<->2)
    M = 0
    for mu in range(4):
        for nu in range(4):
            for a in range(4):
                for b in range(4):
                    E = eps4(mu, nu, a, b)
                    if E == 0:
                        continue
                    F1 = sp.I * (k1[mu] * e1[nu] - k1[nu] * e1[mu])
                    F2 = sp.I * (k2[mu] * e2[nu] - k2[nu] * e2[mu])
                    M += E * (F1 * e2[a] + F2 * e1[a]) * (-sp.I * pp[b])
    return sp.simplify(cF * M)        # L_int = cF (...); i M = i * (vertex) -> M = vertex


M2 = sum(sp.simplify(amp(a_, b_) * sp.conjugate(amp(a_, b_))) for a_ in pols for b_ in pols)
M2 = sp.simplify(M2)
Gam = sp.simplify(M2 / (32 * sp.pi * m))
alpha = sp.symbols('alpha', positive=True)
Gam_a = sp.simplify(Gam.subs(e, sp.sqrt(4 * sp.pi * alpha)))
target = alpha ** 2 * m ** 3 * Nc ** 2 / (576 * sp.pi ** 3 * f ** 2)
log('sum|M|^2 =', M2)
log('Gamma =', Gam_a, '   ratio to alpha^2 m^3 N_c^2/(576 pi^3 f^2):', sp.simplify(Gam_a / target))
out['sum_M2'] = str(M2)
out['Gamma_symbolic'] = str(Gam_a)
out['Gamma_over_PLAN_formula'] = str(sp.simplify(Gam_a / target))
# amplitude magnitude A in M = A eps(k1,e1,k2,e2): |eps(k1,e1,k2,e2)| = m^2/2 for (x,y) polarisations
Aamp = sp.simplify(sp.sqrt(M2 / 2) / (m ** 2 / 2))
log('|A| =', Aamp, '  (standard e^2 N_c/(12 pi^2 f)):', sp.simplify(Aamp / (e ** 2 * Nc / (12 * sp.pi ** 2 * f))))
out['A'] = str(Aamp)

# N_c dependence: amplitude factor N_c * 3 Tr(Q^2 tau3)/3 -> fixed charges vs anomaly-consistent charges
fac_fixed = sp.simplify(Nc * (Qstd ** 2 * t3).trace())
Qc = sp.diag(sp.Rational(1, 2) + 1 / (2 * Nc), -sp.Rational(1, 2) + 1 / (2 * Nc))
fac_cons = sp.simplify(Nc * (Qc ** 2 * t3).trace())
log('N_c Tr(Q^2 tau3): fixed charges', fac_fixed, ';  anomaly-consistent charges', fac_cons)
out['Nc_TrQ2tau3_fixed'] = str(fac_fixed); out['Nc_TrQ2tau3_consistent'] = str(fac_cons)

# ---------------------------------------------------------------- numbers
try:
    import pdg
    api = pdg.connect()
    m_pi0 = api.get('S009M').best_summary().value
    tau = api.get('S009T').best_summary().value
    tau_e = api.get('S009T').best_summary().error
    bf = [b for b in api.get_particle_by_name('pi0').exclusive_branching_fractions() if '2gamma' in b.description][0]
    BR, BRe = bf.value, bf.error
    src = 'pdg package (PDG 2026)'
except Exception as ex:   # pragma: no cover
    m_pi0, tau, tau_e, BR, BRe, src = 134.9768, 8.43e-17, 0.13e-17, 0.98823, 0.00034, f'fallback ({ex})'
hbar = 6.582119569e-16      # eV s
alpha_num = 1 / 137.035999177   # CODATA 2022
G_pdg = hbar / tau * BR
G_pdg_e = G_pdg * ((tau_e / tau) ** 2 + (BRe / BR) ** 2) ** 0.5
Gf = sp.lambdify((alpha, m, Nc, f), Gam_a)
prim, prim_e = 7.802, 0.117
res = {'m_pi0_MeV': m_pi0, 'alpha': alpha_num, 'source': src, 'Gamma_PDG2026_eV': G_pdg, 'Gamma_PDG2026_err_eV': G_pdg_e}
for name, fv, nc in (('Nc3_f92.21', 92.21, 3), ('Nc1_f92.21', 92.21, 1), ('Nc3_f64.5_ANW', 64.5, 3)):
    res[name] = Gf(alpha_num, m_pi0, nc, fv) * 1e6
# fold's own f from the hedgehog cross-check if available
try:
    hh = json.load(open(os.path.join(HERE, 'cc_hedgehog.json')))
    for k, fv in hh['f_values'].items():
        res[f'Nc3_f_{k}'] = Gf(alpha_num, m_pi0, 3, fv) * 1e6
        res[f'f_{k}'] = fv
except Exception as ex:
    log('  (cc_hedgehog.json not available yet:', ex, ')')
res['pull_PrimExII'] = (res['Nc3_f92.21'] - prim) / prim_e
res['pull_PDG2026'] = (res['Nc3_f92.21'] - G_pdg) / G_pdg_e
res['pull_Nc1_PrimExII'] = (res['Nc1_f92.21'] - prim) / prim_e
res['f_for_PrimExII_central'] = 92.21 * (res['Nc3_f92.21'] / prim) ** 0.5
for k, v in res.items():
    log(f'  {k:28s} {v}')
out['numbers'] = res
with open(os.path.join(HERE, 'cc_pi0.json'), 'w') as fh:
    json.dump(out, fh, indent=1)
with open(os.path.join(HERE, 'cc_pi0_log.txt'), 'w') as fh:
    fh.write('\n'.join(LOG) + '\n')
