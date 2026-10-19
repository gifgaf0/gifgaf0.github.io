#!/usr/bin/env python3
"""
E5 symbolic derivations (sympy). Standalone, deterministic.

Units: e = F_pi = 1 (F_pi in the 186-MeV convention), so lengths are in 1/(e F_pi),
energies in F_pi/e, moments of inertia in 1/(e^3 F_pi), currents integrated over space
(axial charge) in 1/e^2.  Metric (+,-,-,-), eps^{0123} = +1.

Lagrangian (ANW):  L = (1/16) Tr(d_mu U d^mu U^+) + (1/32) Tr([L_mu,L_nu][L^mu,L^nu]),
                   L_mu = U^+ d_mu U.

What is derived here, from the Lagrangian alone:
 1. static hedgehog energy density  -> compare with the ANW closed form
 2. SU(2) moment of inertia lambda   -> compare with (2pi/3) int x^2 s^2 [1+4(F'^2+s^2/x^2)]
 3. SU(3) strange moment of inertia  -> compare with Kopeliovich's (pi/2) int x^2(1-c)(1+F'^2+2s^2/x^2)
 4. vector (isospin) Noether current: charge of the rotating hedgehog = lambda*Omega,
    static spatial current V^k_b = eps_{kbl} n_l g(r), hedgehog identity int r g d^3x = (3/2) lambda
 5. baryon current: B^0 = -(1/2pi^2) s^2 F'/r^2, B^k = B^0 (Omega x x)_k  (rigid transport)
 6. magnetic moments: mu^{I=0} = <r^2>_{I=0} J/(6 lambda), mu^{I=1}_p = lambda/6, so
    mu_{p,n} = 2 M_N [<r^2>/(12 lambda) +- lambda/6]  (nuclear magnetons)
 7. axial current; g_A from the sphere integral with the pion-pole (shape) correction and
    from the asymptotic tail: g_A = 2 pi C/(3 e^2); compare with the D-formula quoted for ANW
 8. ANW rotor operators: su(2) algebra, I_k = -D_kl J_l, <p up|D_33|p up> = -1/3
 9. pi0 -> gamma gamma from the gauged Wess-Zumino term (Bernstein-Holstein eq. 67, Witten 1983)
10. one light cone: quadratic Lagrangian of the gauged Skyrme + Maxwell + pion-mass model
    (10d: the gauged WZ term expanded in all fields has no part below cubic order; 9g: its cubic part is the pi0 vertex)
11. vacuum stress tensor T_mu nu = V0 g_mu nu  (mostly-minus metric), p = -rho, frame-free
Writes symbolic_results.json (radial integrands as sympy strings for the numerical script).
Reconciliation (after the independent cross-check): 10d, formerly asserted "by inspection", is computed; 5c and 7b test the
exact value and sign instead of "up to sign"; 9g added.  39 checks, all computed.
"""
import json, math, random, sys, time
import sympy as sp

t_start = time.time()
random.seed(12345)
I = sp.I
CHECKS = []          # (name, passed, detail)


def check(name, ok, detail=""):
    CHECKS.append({"check": name, "passed": bool(ok), "detail": str(detail)})
    print(("PASS " if ok else "FAIL ") + name + ("  [" + str(detail) + "]" if detail else ""))
    sys.stdout.flush()


# ---------------------------------------------------------------- matrices
t1 = sp.Matrix([[0, 1], [1, 0]])
t2 = sp.Matrix([[0, -I], [I, 0]])
t3 = sp.Matrix([[1, 0], [0, -1]])
one2 = sp.eye(2)
tau = [t1, t2, t3]

s, c, Fp, r = sp.symbols('s c Fp r', real=True)          # sin F, cos F, F'(r), radius
n1, n2, n3 = sp.symbols('n1 n2 n3', real=True)
nv = [n1, n2, n3]
W1, W2, W3 = sp.symbols('W1 W2 W3', real=True)            # body = physical angular velocity
Wv = [W1, W2, W3]
Fsym = sp.symbols('F', real=True)
W4 = sp.symbols('W4', real=True)                          # strange-direction angular velocity


def tr(M):
    return sp.expand(M.trace())


def comm(A, B):
    return A * B - B * A


def dfact2(k):
    return 1 if k <= 0 else k * dfact2(k - 2)


def sph_avg(expr, vars3=nv):
    """Average a polynomial in n1,n2,n3 over the unit sphere (exact monomial formula)."""
    expr = sp.expand(expr)
    if expr == 0:
        return sp.Integer(0)
    P = sp.Poly(expr, *vars3)
    out = 0
    for (k1, k2, k3), coef in P.terms():
        if k1 % 2 or k2 % 2 or k3 % 2:
            continue
        K = k1 + k2 + k3
        out += coef * sp.Rational(dfact2(k1 - 1) * dfact2(k2 - 1) * dfact2(k3 - 1), dfact2(K + 1))
    return sp.expand(out)


def numeq(e1, e2, extra=None, ntest=6, tol=1e-11):
    """Numerically compare two expressions in (s,c,Fp,r[,n,W]) with s=sinF, c=cosF and |n|=1."""
    worst = 0.0
    for _ in range(ntest):
        Fv = random.uniform(0.2, 2.9)
        sub = {s: math.sin(Fv), c: math.cos(Fv), Fp: random.uniform(-2.0, -0.05),
               r: random.uniform(0.2, 4.0), Fsym: Fv}
        v = [random.gauss(0, 1) for _ in range(3)]
        nn = math.sqrt(sum(x * x for x in v))
        for k in range(3):
            sub[nv[k]] = v[k] / nn
            sub[Wv[k]] = random.uniform(-1, 1)
        sub[W4] = random.uniform(-1, 1)
        if extra:
            sub.update(extra())
        a = complex(sp.N(e1.subs(sub), 30))
        b = complex(sp.N(e2.subs(sub), 30))
        worst = max(worst, abs(a - b) / max(1.0, abs(b)))
    return worst < tol, worst


# ---------------------------------------------------------------- hedgehog at a generic point
tn = n1 * t1 + n2 * t2 + n3 * t3
U0 = c * one2 + I * s * tn
U0d = c * one2 - I * s * tn
# d_i n_j = (delta_ij - n_i n_j)/r ; d_i F = F' n_i
dU = [-s * Fp * nv[i] * one2 + I * c * Fp * nv[i] * tn + I * s * (tau[i] - nv[i] * tn) / r for i in range(3)]
Lsp = [sp.expand(U0d * dU[i]) for i in range(3)]       # L_i = U^+ d_i U
Rsp = [sp.expand(dU[i] * U0d) for i in range(3)]       # R_i = d_i U U^+
Wtau = W1 * t1 + W2 * t2 + W3 * t3
dU0t = (I / 2) * comm(Wtau, U0)                         # d_0 U at A = 1, A^+ dA/dt = (i/2) W.tau
L0 = sp.expand(U0d * dU0t)

# sanity: unitarity on the constraint surface
ok, w = numeq(sp.Matrix(U0d * U0 - one2).norm(), sp.Integer(0))
check("U0 unitary on |n|=1, s^2+c^2=1", ok, w)

# 1. static energy density
E2 = sum(tr(dU[i] * dU[i].H) for i in range(3)) / 16
E4 = -sum(tr(comm(Lsp[i], Lsp[j]) * comm(Lsp[i], Lsp[j])) for i in range(3) for j in range(3)) / 32
eps_static = sph_avg(E2 + E4)
eps_ANW = sp.Rational(1, 8) * (Fp**2 + 2 * s**2 / r**2) + sp.Rational(1, 2) * (s**2 / r**2) * (s**2 / r**2 + 2 * Fp**2)
ok, w = numeq(eps_static, eps_ANW)
check("1. static energy density = (1/8)(F'^2+2s^2/r^2) + (1/2)(s^2/r^2)(s^2/r^2+2F'^2)", ok, w)
# also: anisotropy-free (energy density is spherically symmetric)
ok, w = numeq(sp.expand(E2 + E4), eps_ANW)
check("1b. energy density is spherically symmetric pointwise", ok, w)

# 2. SU(2) moment of inertia from the kinetic Lagrangian
Lkin = tr(dU0t * dU0t.H) / 16 - sum(tr(comm(L0, Lsp[i]) * comm(L0, Lsp[i])) for i in range(3)) / 16
Lkin_avg = sph_avg(Lkin)
lam_dens_expected = sp.Rational(1, 6) * s**2 * (1 + 4 * (Fp**2 + s**2 / r**2))   # per unit volume
ok, w = numeq(Lkin_avg, lam_dens_expected * (W1**2 + W2**2 + W3**2) / 2)
check("2. L_kin = (lambda/2) W^2 with lambda = (2pi/3) int x^2 s^2 [1+4(F'^2+s^2/x^2)] dx", ok, w)

# 3. SU(3) strange moment of inertia (3x3 embedding)
def emb3(M2):
    M = sp.zeros(3, 3)
    M[0:2, 0:2] = M2
    return M


U3 = emb3(U0); U3[2, 2] = 1
U3d = emb3(U0d); U3d[2, 2] = 1
dU3 = [emb3(dU[i]) for i in range(3)]
L3 = [sp.expand(U3d * dU3[i]) for i in range(3)]
lam4 = sp.Matrix([[0, 0, 1], [0, 0, 0], [1, 0, 0]])
dU3t = (I / 2) * comm(W4 * lam4, U3)
L03 = sp.expand(U3d * dU3t)
Lkin3 = tr(dU3t * dU3t.H) / 16 - sum(tr(comm(L03, L3[i]) * comm(L03, L3[i])) for i in range(3)) / 16
Lkin3_avg = sph_avg(Lkin3)
I2_dens_expected = sp.Rational(1, 8) * (1 - c) * (1 + Fp**2 + 2 * s**2 / r**2)
ok, w = numeq(Lkin3_avg, I2_dens_expected * W4**2 / 2)
check("3. L_kin(W4) = (I2/2) W4^2 with I2 = (pi/2) int x^2 (1-c)(1+F'^2+2s^2/x^2) dx", ok, w)
# I1 in the same 3x3 normalisation equals lambda
lam3m = emb3(t3)
dU3t3 = (I / 2) * comm(W3 * lam3m, U3)
L03b = sp.expand(U3d * dU3t3)
Lkin3b = tr(dU3t3 * dU3t3.H) / 16 - sum(tr(comm(L03b, L3[i]) * comm(L03b, L3[i])) for i in range(3)) / 16
ok, w = numeq(sph_avg(Lkin3b), lam_dens_expected * W3**2 / 2)
check("3b. 3x3 embedding reproduces I1 = lambda (same generator normalisation lambda_a/2)", ok, w)
# lambda_8 direction: zero inertia
lam8 = sp.diag(1, 1, -2) / sp.sqrt(3)
dU3t8 = (I / 2) * comm(lam8, U3)
check("3c. lambda_8 commutes with the embedded hedgehog (zero inertia, WZ-constrained)",
      sp.simplify(dU3t8) == sp.zeros(3, 3), "")

# 4. vector (isospin) Noether current for U -> e^{i eps.tau/2} U e^{-i eps.tau/2}
#    j^mu_a = dL/d(d_mu eps^a) = -(1/8) Tr(L^mu i X_a) + (1/8) Tr(i X_a [L_nu,[L^mu,L^nu]]),
#    X_a = (U^+ tau_a U - tau_a)/2
XV = [sp.expand((U0d * tau[a] * U0 - tau[a]) / 2) for a in range(3)]
XA = [sp.expand((U0d * tau[a] * U0 + tau[a]) / 2) for a in range(3)]
dbl = [sp.expand(sum((comm(Lsp[k], comm(Lsp[j], Lsp[k])) for k in range(3)), sp.zeros(2, 2))) for j in range(3)]
dbl0 = sp.expand(sum((comm(Lsp[k], comm(L0, Lsp[k])) for k in range(3)), sp.zeros(2, 2)))


def Vspace(a, j, X=XV):
    # static: L^j = -L_j ; [L_nu,[L^j,L^nu]] = sum_k [L_k,[L_j,L_k]]
    return sp.expand(I / 8 * tr(Lsp[j] * X[a]) + I / 8 * tr(X[a] * dbl[j]))


def Vtime(a, X=XV):
    # L^0 = L_0 ; [L_nu,[L^0,L^nu]] = -sum_k [L_k,[L_0,L_k]]
    return sp.expand(-I / 8 * tr(L0 * X[a]) - I / 8 * tr(X[a] * dbl0))


V0 = [Vtime(a) for a in range(3)]
ok_all = True; worst = 0
for a in range(3):
    okk, ww = numeq(sph_avg(V0[a]), lam_dens_expected * Wv[a])
    ok_all &= okk; worst = max(worst, ww)
check("4a. isospin charge density of the rotating hedgehog averages to lambda(r) W_a (I^N = lambda W)", ok_all, worst)
Vst = [[Vspace(a, j) for j in range(3)] for a in range(3)]
g_r = sp.expand(sum(sph_avg(sp.LeviCivita(k, b, l) * nv[l] * Vst[b][k]) for k in range(3) for b in range(3) for l in range(3)) / 2)
resid = sp.Integer(0)
ok_all = True; worst = 0
for b in range(3):
    for k in range(3):
        target = sum(sp.LeviCivita(k, b, l) * nv[l] for l in range(3)) * g_r
        okk, ww = numeq(Vst[b][k], target)
        ok_all &= okk; worst = max(worst, ww)
check("4b. static isovector current has the form V^k_b = eps_{kbl} n_l g(r)", ok_all, worst)
# hedgehog identity: V^0_a = (W x x)_j V^j_a pointwise
ok_all = True; worst = 0
for a in range(3):
    WxX = [sum(sp.LeviCivita(j, k, l) * Wv[k] * nv[l] * r for k in range(3) for l in range(3)) for j in range(3)]
    okk, ww = numeq(V0[a], sum(WxX[j] * Vst[a][j] for j in range(3)))
    ok_all &= okk; worst = max(worst, ww)
check("4c. hedgehog identity V^0_a = (W x x)_j V^j_a (rotation in isospace = rotation in space)", ok_all, worst)
ok, w = numeq(sp.Rational(2, 3) * r * g_r, lam_dens_expected)
check("4d. (2/3) r g(r) = lambda density  =>  int r g d^3x = (3/2) lambda  =>  mu^{I=1}_p = lambda/6", ok, w)

# 5. baryon current B^mu = kappa eps^{mu nu rho sigma} Tr(L_nu L_rho L_sigma)
Lall = [L0] + Lsp
def Bmu(mu):
    tot = 0
    for nu in range(4):
        for rho in range(4):
            for sg in range(4):
                e = sp.LeviCivita(mu, nu, rho, sg)
                if e != 0:
                    tot += e * tr(Lall[nu] * Lall[rho] * Lall[sg])
    return sp.expand(tot)


B0raw = Bmu(0)
B0_expected = -s**2 * Fp / (2 * sp.pi**2 * r**2)
# choose kappa so that B^0 is the positive baryon density for F(0)=pi, F'<0
kap_val = sp.nsimplify(sp.N(B0_expected.subs({s: 0.6, c: 0.8, Fp: -0.7, r: 1.3}) / B0raw.subs({s: 0.6, c: 0.8, Fp: -0.7, r: 1.3, n1: 0, n2: 0, n3: 1}), 20) * sp.pi**2) / sp.pi**2
ok, w = numeq(kap_val * B0raw, B0_expected)
check("5a. B^0 = kappa eps^{0ijk}Tr(L_i L_j L_k) = -(1/2pi^2) s^2 F'/r^2 with kappa = %s" % kap_val, ok, w)
ok_all = True; worst = 0
for k in range(3):
    Bk = kap_val * Bmu(k + 1)
    WxX = sum(sp.LeviCivita(k, a, l) * Wv[a] * nv[l] * r for a in range(3) for l in range(3))
    okk, ww = numeq(Bk, B0_expected * WxX)
    ok_all &= okk; worst = max(worst, ww)
check("5b. B^k = B^0 (W x x)_k : the baryon current is rigidly transported by the physical rotation", ok_all, worst)
# (reconciliation) strict: the value is exactly -1/(24 pi^2) with L = U^+ dU, eps^{0123} = +1 and B = +1 for F(0) = pi.
# Its magnitude is the standard 1/(24 pi^2); the sign depends only on those conventions (eps_{0123} vs eps^{0123}, L vs R).
check("5c. kappa = -1/(24 pi^2) exactly (magnitude = standard 1/(24 pi^2); the sign follows from eps^{0123}=+1, L = U^+ dU, B = +1)",
      sp.simplify(kap_val + 1 / (24 * sp.pi**2)) == 0, kap_val)

# 6. magnetic moments (structure)
#   isoscalar EM current = B^mu/2 (N_c=3, see section 9 helper); mu = (1/2) int x x J
#   mu^{I=0} = (1/2)(1/2) int rho_B x x (W x x) = (1/6) <r^2>_B W ; J = lambda W  => <r^2> J/(6 lambda)
xs = [r * nv[i] for i in range(3)]
WxX = [sum(sp.LeviCivita(j, k, l) * Wv[k] * xs[l] for k in range(3) for l in range(3)) for j in range(3)]
mu0 = [sp.Rational(1, 2) * sum(sp.LeviCivita(i, j, k) * xs[j] * sp.Rational(1, 2) * WxX[k] for j in range(3) for k in range(3)) for i in range(3)]
mu0avg = [sph_avg(m) for m in mu0]
ok = all(sp.simplify(mu0avg[i] - r**2 * Wv[i] / 6) == 0 for i in range(3))
check("6a. angular average of (1/2) x x (B/2 with B^0=1)(W x x) = r^2 W/6  =>  mu^{I=0} = <r^2> J/(6 lambda)", ok, mu0avg)
#   isovector: (1/2) int eps_ijk x_j V^k_b = (1/3) delta_ib int r g  (V^k_b = eps_kbl n_l g)
mu1 = [[sp.Rational(1, 2) * sph_avg(sum(sp.LeviCivita(i, j, k) * xs[j] * sp.LeviCivita(k, b, l) * nv[l] for j in range(3) for k in range(3) for l in range(3))) for b in range(3)] for i in range(3)]
ok = all(sp.simplify(mu1[i][b] - (sp.Rational(1, 3) * r if i == b else 0)) == 0 for i in range(3) for b in range(3))
check("6b. (1/2) <eps_ijk x_j eps_kbl n_l> = (r/3) delta_ib  =>  mu^{I=1}_i = D_3i (1/3) int r g d^3x", ok, "")

# 7. axial current, U -> e^{i eps.tau/2} U e^{i eps.tau/2}, X^A_a = (U^+ tau_a U + tau_a)/2
Ast = [[Vspace(a, j, XA) for j in range(3)] for a in range(3)]
S1 = sp.expand(sum(sph_avg(Ast[a][a]) for a in range(3)))          # 3 f1 + f2
S2 = sp.expand(sum(sph_avg(nv[a] * nv[j] * Ast[a][j]) for a in range(3) for j in range(3)))  # f1 + f2
f1_r = sp.expand((S1 - S2) / 2)          # (3 f1 + f2) - (f1 + f2) = 2 f1
f2_r = sp.expand(S2 - f1_r)
ok_all = True; worst = 0
for a in range(3):
    for j in range(3):
        okk, ww = numeq(Ast[a][j], f1_r * (1 if a == j else 0) + f2_r * nv[a] * nv[j])
        ok_all &= okk; worst = max(worst, ww)
check("7a. static axial current has the form A^j_a = f1(r) delta_aj + f2(r) n_a n_j", ok_all, worst)
GA_dens = sp.expand(f1_r + f2_r / 3)        # sphere-integral density of int A^a_i = delta_ai * int (f1+f2/3)
# literature D-formula (as quoted for ANW in prior_address): g_A = -(pi/(3e^2)) int x^2 [F' + sin2F/x
#   + 4( sin2F F'^2/x + 2 s^2 F'/x^2 + s^2 sin2F/x^3 )] dx   (per unit x; sin2F = 2 s c)
D_dens = Fp + 2 * s * c / r + 4 * (2 * s * c * Fp**2 / r + 2 * s**2 * Fp / r**2 + s**2 * 2 * s * c / r**3)
# int_sphere d^3x A^j_a = delta_aj * G_sphere, G_sphere = int 4 pi r^2 (f1 + f2/3) dr.  Proton matrix element:
# <p up| int A^3_3 |p up> = <D_33> G_sphere = -G_sphere/3 = g_A/2 (generator tau/2)  ->  g_A(sphere) = (2/3)|G_sphere|.
# Massless pions: the pion pole q_i q_j/q^2 removes 1/3 of the angular average, so g_A = (3/2) g_A(sphere) = |G_sphere|.
# Compare G_sphere with the D-formula quoted for ANW, g_A = -(pi/3e^2) int x^2 D dx.
ok, w = numeq(4 * sp.pi * GA_dens, (sp.pi / 3) * D_dens)
ok2, w2 = numeq(4 * sp.pi * GA_dens, -(sp.pi / 3) * D_dens)
# (reconciliation) strict sign: G_sphere = -(pi/3) int x^2 D dx, the sign of the literature formula g_A = -(pi/3e^2) int x^2 D dx
check("7b. derived axial density matches the D-formula with the literature sign: 4 pi (f1+f2/3) = -(pi/3) D",
      ok2 and not ok, "rel.dev with -: %.2e ; with +: %.2e" % (w2, w))
# Large-r tail: with F = C/r^2 small, f1 -> k/r^3, f2 -> -3k/r^3 with k = -C/4  =>  g_A = (8pi/3)|k| = 2 pi C/3
Csym, eps_ = sp.symbols('C epsilon', positive=True)
Ftail = eps_ * Csym / r**2
tail_sub = {s: sp.sin(Ftail), c: sp.cos(Ftail), Fp: sp.diff(Ftail, r)}
f1_tail = sp.series(f1_r.subs(tail_sub), eps_, 0, 2).removeO().subs(eps_, 1)
f2_tail = sp.series(f2_r.subs(tail_sub), eps_, 0, 2).removeO().subs(eps_, 1)
check("7c. tail: f1 -> -(C/4)/r^3, f2 -> +(3C/4)/r^3 (pion field ~ d_j(n_a/r^2)); g_A(tail) = 2 pi C/(3 e^2)",
      sp.simplify(f1_tail + Csym / (4 * r**3)) == 0 and sp.simplify(f2_tail - 3 * Csym / (4 * r**3)) == 0,
      "f1=%s, f2=%s" % (f1_tail, f2_tail))

# 8. ANW collective-coordinate operators on S^3 (a0 = a4)
a0, a1, a2, a3 = sp.symbols('a0 a1 a2 a3', real=True)
av = [a1, a2, a3]
psi = sp.Function('psi')(a0, a1, a2, a3)


def Iop(k, f):
    l, m = [(1, 2), (2, 0), (0, 1)][k]
    return sp.I / 2 * (a0 * sp.diff(f, av[k]) - av[k] * sp.diff(f, a0) - (av[l] * sp.diff(f, av[m]) - av[m] * sp.diff(f, av[l])))


def Jop(k, f):
    l, m = [(1, 2), (2, 0), (0, 1)][k]
    return sp.I / 2 * (av[k] * sp.diff(f, a0) - a0 * sp.diff(f, av[k]) - (av[l] * sp.diff(f, av[m]) - av[m] * sp.diff(f, av[l])))


Amat = a0 * one2 + I * (a1 * t1 + a2 * t2 + a3 * t3)
Dmat = sp.Matrix(3, 3, lambda a, b: sp.expand(sp.Rational(1, 2) * (tau[a] * Amat * tau[b] * Amat.H).trace()))
# test polynomial
ftest = a0**2 * a1 + 3 * a1 * a2 * a3 - a2**3 + a0 * a3**2 + a1**2 * a0 * a2
ok_alg = sp.expand(Iop(0, Iop(1, ftest)) - Iop(1, Iop(0, ftest)) - sp.I * Iop(2, ftest)) == 0 and \
         sp.expand(Jop(0, Jop(1, ftest)) - Jop(1, Jop(0, ftest)) - sp.I * Jop(2, ftest)) == 0
check("8a. ANW I_k and J_k obey the standard su(2) algebra [X1,X2] = i X3", ok_alg, "")
# I_k = -D_kl J_l on functions of a restricted to S^3: check on the test polynomial, project with a^2 = 1
ok_rel = True
for k in range(3):
    lhs = Iop(k, ftest)
    rhs = -sum(Dmat[k, l] * Jop(l, ftest) for l in range(3))
    diff = sp.expand(lhs - rhs)
    # D_kl contains a^2 factors; compare on the sphere numerically
    for _ in range(4):
        v = [random.gauss(0, 1) for _ in range(4)]
        nn = math.sqrt(sum(x * x for x in v))
        val = complex(diff.subs({a0: v[0] / nn, a1: v[1] / nn, a2: v[2] / nn, a3: v[3] / nn}))
        ok_rel &= abs(val) < 1e-12
check("8b. operator identity I_k = -D_kl(A) J_l holds on S^3 (hedgehog: isospin = -rotated spin)", ok_rel, "")


def s3_avg(expr):
    P = sp.Poly(sp.expand(expr), a0, a1, a2, a3)
    out = 0
    for ks, coef in P.terms():
        if any(k % 2 for k in ks):
            continue
        K = sum(ks)
        num = 1
        for k in ks:
            num *= dfact2(k - 1)
        den = 1
        for j in range(K // 2):
            den *= (4 + 2 * j)
        out += coef * sp.Rational(num, den)
    return out


p_up = a1 + I * a2
norm = s3_avg(sp.expand(p_up * sp.conjugate(p_up)))
D33 = s3_avg(sp.expand(sp.conjugate(p_up) * Dmat[2, 2] * p_up)) / norm
I3p = sp.simplify(Iop(2, p_up) / p_up); J3p = sp.simplify(Jop(2, p_up) / p_up)
check("8c. |p up> = (a1 + i a2)/pi has I3 = +1/2, J3 = +1/2 and <D_33> = -1/3", I3p == sp.Rational(1, 2) and J3p == sp.Rational(1, 2) and D33 == sp.Rational(-1, 3), "I3=%s J3=%s D33=%s" % (I3p, J3p, D33))
# Wigner-Eckart cross-check: I^N_a = +D_ab J_b with I^N = -I^ANW gives <D_33> = +1/3 for the charge +1 state
# in the Noether labelling, and (V^N, +1/3) -> mu^{I=1}_p = (1/3)(1/3)(3/2)lambda = +lambda/6; same with (V^std, -1/3).

# 9. pi0 -> gamma gamma from the gauged WZ term (Bernstein-Holstein eq. 67; Witten 1983)
#    L_A = -(Nc/48pi^2) eps^{mu nu al be} [ e A_mu Tr(Q L_nu L_al L_be - Q R_nu R_al R_be)
#                                           + i e^2 F_mu nu A_al T_be ],
#    T_be = Tr(Q^2 L_be - Q^2 R_be + (1/2) Q U Q U^+ L_be - (1/2) Q U^+ Q U R_be),
#    L = dU U^+, R = dU^+ U, U = exp(i pi^a tau_a / f)   (f = 92 MeV convention)
f_, ee, Nc = sp.symbols('f e N_c', positive=True)
pis = sp.symbols('pi1 pi2 pi3', real=True)
dpis = sp.symbols('dpi1 dpi2 dpi3', real=True)    # d_beta pi^a for one fixed beta
Q2 = sp.diag(sp.Rational(2, 3), sp.Rational(-1, 3))
lin = sp.Symbol('lin')
Phi = sum((pis[a] * tau[a] for a in range(3)), sp.zeros(2, 2)) / f_
dPhi = sum((dpis[a] * tau[a] for a in range(3)), sp.zeros(2, 2)) / f_
Ulin = one2 + I * lin * Phi - lin**2 * Phi * Phi / 2
dUlin = I * lin * dPhi - lin**2 * (dPhi * Phi + Phi * dPhi) / 2
Udlin = one2 - I * lin * Phi - lin**2 * Phi * Phi / 2
dUdlin = -I * lin * dPhi - lin**2 * (dPhi * Phi + Phi * dPhi) / 2
Lb = dUlin * Udlin
Rb = dUdlin * Ulin
Tb = (Q2 * Q2 * Lb - Q2 * Q2 * Rb + Q2 * Ulin * Q2 * Udlin * Lb / 2 - Q2 * Udlin * Q2 * Ulin * Rb / 2).trace()
Tb1 = sp.expand(sp.diff(Tb, lin).subs(lin, 0))
check("9a. linear part of T_beta = i (3 Tr(Q^2 tau_3)) d_beta pi0 / f = i d_beta pi0 / f; pi+- do not couple (Tr Q^2 tau_{1,2} = 0)",
      sp.simplify(Tb1 - I * dpis[2] / f_) == 0, "T_beta(1) = %s" % Tb1)
# isoscalar EM current from the e^1 term in SU(2): Tr(tau3 * antisym(LLL)) = 0, so only Tr(Q)/2 = 1/6 survives:
#   N_c * (1/48pi^2) * 2 * (1/6) eps Tr(LLL) = (N_c/6) * (1/24pi^2) eps Tr(LLL) = (N_c/6) B^mu  ->  B/2 for N_c = 3
ok_t3 = True
for (A_, B_, C_) in [(t1, t2, t3), (t1 + t2, t3 - t1, 2 * t2 + t3)]:
    anti = sum((sp.LeviCivita(i, j, k) * [A_, B_, C_][i] * [A_, B_, C_][j] * [A_, B_, C_][k] for i in range(3) for j in range(3) for k in range(3)), sp.zeros(2, 2))
    ok_t3 &= sp.simplify((t3 * anti).trace()) == 0 and sp.simplify(anti - anti[0, 0] * one2) == sp.zeros(2, 2)
check("9b. antisymmetrised product of three su(2) elements is proportional to 1 (so Q = I3 + (N_c/6) B: B/2 at N_c=3)", ok_t3, "")
# amplitude: L_int = K eps^{mu nu al be} (d_mu A_nu - d_nu A_mu) A_al d_be pi0, with
#   K = -(i Nc e^2/(48 pi^2)) * (i/f) = Nc e^2/(48 pi^2 f)
K = -(I * Nc * ee**2 / (48 * sp.pi**2)) * (I / f_)
K = sp.simplify(K)
m = sp.symbols('m', positive=True)
g = sp.diag(1, -1, -1, -1)
p4 = sp.Matrix([m, 0, 0, 0])
k1 = sp.Matrix([m / 2, 0, 0, m / 2]); k2 = sp.Matrix([m / 2, 0, 0, -m / 2])
pols = [sp.Matrix([0, 1, 0, 0]), sp.Matrix([0, 0, 1, 0])]
low = lambda v: g * v


def amp(e1, e2):
    # outgoing photons: A -> eps* e^{ikx}, d -> i k ; incoming pion: d -> -i p ; two contractions
    tot = 0
    for (ka, ea, kb, eb) in [(k1, e1, k2, e2), (k2, e2, k1, e1)]:
        kl, el, ebl, pl = low(ka), low(ea), low(eb), low(p4)
        for mu in range(4):
            for nu in range(4):
                for al in range(4):
                    for be in range(4):
                        lc = sp.LeviCivita(mu, nu, al, be)
                        if lc == 0:
                            continue
                        tot += lc * ((I * kl[mu]) * el[nu] - (I * kl[nu]) * el[mu]) * ebl[al] * (-I * pl[be])
    return sp.expand(K * tot)


M2 = sum(sp.expand(amp(e1, e2) * sp.conjugate(amp(e1, e2))) for e1 in pols for e2 in pols)
alpha = sp.symbols('alpha', positive=True)
Gamma = sp.simplify((sp.Rational(1, 2) * M2 / (2 * m) / (8 * sp.pi)).subs(ee, sp.sqrt(4 * sp.pi * alpha)))
Gamma_expected = alpha**2 * m**3 * Nc**2 / (576 * sp.pi**3 * f_**2)
check("9c. Gamma(pi0->gg) from the gauged WZ term = alpha^2 m^3 N_c^2/(576 pi^3 f^2)", sp.simplify(Gamma - Gamma_expected) == 0, "Gamma = %s" % Gamma)
Acoef = sp.simplify(sp.sqrt(sp.expand(M2 / 2)) / (m**2 / 2))     # |M| = A |eps(k1,e1,k2,e2)| with sum |eps..|^2 = m^4/2
check("9d. amplitude coefficient A = N_c e^2/(12 pi^2 f) (= e^2/(4 pi^2 f) at N_c = 3, B-H eq. 70)",
      sp.simplify(Acoef - Nc * ee**2 / (12 * sp.pi**2 * f_)) == 0, "A = %s" % Acoef)
# B-H eq. 69 second line: written as (e^2 Nc/(24 pi^2 F)) F F~ pi0. With F~^{mu nu} = (1/2) eps F, the coefficient
# that reproduces eq. 70 is e^2 Nc/(48 pi^2 F): K eps (dA-dA) A d pi = K pi F F~ (integrate by parts).
check("9e. equivalent effective coupling: L = g pi0 F_mu nu F~^{mu nu} with g = K = N_c e^2/(48 pi^2 f) (B-H eq. 69 2nd line has 24 pi^2: factor-2 F~ normalisation)",
      sp.simplify(K - Nc * ee**2 / (48 * sp.pi**2 * f_)) == 0, "K = %s" % K)
# N_c-dependence with anomaly-consistent charges Q = diag(1/2+1/(2Nc), -1/2+1/(2Nc)) (Baer-Wiese):
QNc = sp.diag(sp.Rational(1, 2) + 1 / (2 * Nc), -sp.Rational(1, 2) + 1 / (2 * Nc))
fac_fixed = sp.simplify(Nc * (Q2 * Q2 * t3).trace())
fac_cons = sp.simplify(Nc * (QNc * QNc * t3).trace())
check("9f. amplitude factor N_c Tr(Q^2 tau3): fixed charges -> N_c/3 ; anomaly-consistent charges -> 1 (N_c-independent)",
      sp.simplify(fac_fixed - Nc / 3) == 0 and sp.simplify(fac_cons - 1) == 0, "fixed=%s, consistent=%s" % (fac_fixed, fac_cons))

# 10. one light cone: quadratic Lagrangian of gauged Skyrme + mass + Maxwell around U = 1
F0, es, mpi, qe = sp.symbols('F_pi e_s m_pi q', positive=True)
ph = sp.symbols('p1 p2 p3', real=True)
dph = [[sp.Symbol('dp%d_%d' % (a, mu), real=True) for mu in range(4)] for a in range(3)]
Asym = [sp.Symbol('A%d' % mu, real=True) for mu in range(4)]
dA = [[sp.Symbol('dA%d_%d' % (mu, nu), real=True) for nu in range(4)] for mu in range(4)]   # d_mu A_nu
lam_ = sp.Symbol('lam_', real=True)
QEM = t3 / 2 + one2 / 6
Th = sum((ph[a] * tau[a] for a in range(3)), sp.zeros(2, 2)) * 2 / F0
dTh = [sum((dph[a][mu] * tau[a] for a in range(3)), sp.zeros(2, 2)) * 2 / F0 for mu in range(4)]
U_ = one2 + I * lam_ * Th - lam_**2 * Th * Th / 2 - I * lam_**3 * Th * Th * Th / 6
Ud_ = one2 - I * lam_ * Th - lam_**2 * Th * Th / 2 + I * lam_**3 * Th * Th * Th / 6
dU_ = [I * lam_ * dTh[mu] - lam_**2 * (dTh[mu] * Th + Th * dTh[mu]) / 2 for mu in range(4)]
DU = [dU_[mu] + I * qe * lam_ * Asym[mu] * comm(QEM, U_) for mu in range(4)]
DUd = [DU[mu].H for mu in range(4)]
ginv = [1, -1, -1, -1]


def trunc(expr, order=2):
    """keep powers lam_^0..lam_^order of a scalar expression"""
    P = sp.Poly(sp.expand(expr), lam_)
    return sp.expand(sum(coef * lam_**k[0] for k, coef in P.terms() if k[0] <= order))


def truncM(M, order=2):
    return M.applyfunc(lambda e: trunc(e, order) if e != 0 else e)


DU2 = [truncM(DU[mu]) for mu in range(4)]
DUd2 = [truncM(DUd[mu]) for mu in range(4)]
L2q = sum(ginv[mu] * trunc((DU2[mu] * DUd2[mu]).trace()) for mu in range(4)) * F0**2 / 16
Lmq = (F0**2 * mpi**2 / 16) * trunc((U_ + Ud_ - 2 * one2).trace())
# Skyrme term: L_mu = U^+ D_mu U vanishes at zeroth order in the fields, so [L_mu,L_nu][L^mu,L^nu] = O(fields^4)
Lmu0 = [sp.simplify((Ud_ * DU[mu]).subs(lam_, 0)) for mu in range(4)]
L4_quad = 0 if all(M == sp.zeros(2, 2) for M in Lmu0) else None
Fmn = [[lam_ * (dA[mu][nu] - dA[nu][mu]) for nu in range(4)] for mu in range(4)]
LMax = -sp.Rational(1, 4) * sum(ginv[mu] * ginv[nu] * Fmn[mu][nu]**2 for mu in range(4) for nu in range(4))


def order2(expr):
    return sp.expand(sp.expand(expr).coeff(lam_, 2))


L2_quad = order2(L2q); Lm_quad = order2(Lmq); LM_quad = order2(LMax)
kin_expected = sp.Rational(1, 2) * sum(ginv[mu] * dph[a][mu]**2 for a in range(3) for mu in range(4))
check("10a. quadratic part of (F^2/16)Tr(DU DU^+) = (1/2) d_mu pi^a d^mu pi^a (no photon-pion mixing at this order)",
      sp.simplify(L2_quad - kin_expected) == 0, "")
check("10b. quadratic part of the mass term = -(1/2) m_pi^2 pi^a pi^a", sp.simplify(Lm_quad + mpi**2 * sum(p**2 for p in ph) / 2) == 0, "")
check("10c. L_mu = U^+ D_mu U vanishes at zeroth order, so the Skyrme term [L,L]^2 starts at 4th order (no quadratic part)", L4_quad == 0, "")
# (reconciliation) 10d was hard-coded True "by inspection" in the first run; it is now computed.
# Gauged WZ term in SU(2) (Bernstein-Holstein eq. 67, as transcribed in section 9), with the photon and the pions each carrying
# one power of the bookkeeping parameter lam_:  L_WZ = -(N_c/48 pi^2) eps^{mu nu al be} [ q A_mu Tr(Q L_nu L_al L_be - Q R R R)
#   + i q^2 F_mu nu A_al T_be ],  L = dU U^+, R = dU^+ U, T as in section 9.  Every factor (A, F, L, R, T) starts at order 1, so the
# product needs only order-1 pieces up to total order 3; dU_ (order 2) and U_ (order 3) are more than enough.
Ncw = sp.symbols('N_c', positive=True)
Aw = [lam_ * Asym[mu] for mu in range(4)]
Fw = [[lam_ * (dA[mu][nu] - dA[nu][mu]) for nu in range(4)] for mu in range(4)]
dUd_ = [dU_[mu].H for mu in range(4)]
Lw = [truncM(dU_[mu] * Ud_, 2) for mu in range(4)]
Rw = [truncM(dUd_[mu] * U_, 2) for mu in range(4)]
Tw = [trunc((QEM * QEM * Lw[b] - QEM * QEM * Rw[b] + QEM * U_ * QEM * Ud_ * Lw[b] / 2
             - QEM * Ud_ * QEM * U_ * Rw[b] / 2).trace(), 2) for b in range(4)]
wz1 = 0
wz2 = 0
for mu in range(4):
    for nu in range(4):
        for al in range(4):
            for be in range(4):
                lc = sp.LeviCivita(mu, nu, al, be)
                if lc == 0:
                    continue
                LLL = truncM(truncM(Lw[nu] * Lw[al], 3) * Lw[be], 3)
                RRR = truncM(truncM(Rw[nu] * Rw[al], 3) * Rw[be], 3)
                wz1 += lc * trunc(Aw[mu] * (QEM * LLL - QEM * RRR).trace(), 3)
                wz2 += lc * trunc(Fw[mu][nu] * Aw[al] * Tw[be], 3)
LWZ = sp.expand(-(Ncw / (48 * sp.pi**2)) * (qe * wz1 + I * qe**2 * wz2))
wz_orders = [sp.simplify(sp.expand(LWZ).coeff(lam_, k)) if k else sp.simplify(LWZ.subs(lam_, 0)) for k in range(4)]
check("10d. gauged WZ term expanded in all fields: no part of order 0, 1 or 2 (no quadratic part; computed)",
      all(o == 0 for o in wz_orders[:3]) and wz_orders[3] != 0,
      "orders 0-2: %s; order 3 nonzero: %s" % (wz_orders[:3], wz_orders[3] != 0))
# the cubic part is the pi0 A dA vertex; written with d_mu A_nu its coefficient is N_c q^2/(24 pi^2 f), f = F_pi/2 (Th = 2 pi.tau/F_pi)
f_half = F0 / 2
cubic_expected = (Ncw * qe**2 / (24 * sp.pi**2 * f_half)) * sum(
    sp.LeviCivita(mu, nu, al, be) * dA[mu][nu] * Asym[al] * dph[2][be]
    for mu in range(4) for nu in range(4) for al in range(4) for be in range(4) if sp.LeviCivita(mu, nu, al, be) != 0)
check("9g. that cubic part = (N_c e^2/(24 pi^2 f)) eps^{mu nu al be} d_mu A_nu A_al d_be pi0 = (N_c e^2/(48 pi^2 f)) eps F_mu nu A_al d_be pi0 "
      "(only pi0 couples)", sp.simplify(wz_orders[3] - cubic_expected) == 0, "")
# Fourier: pions (k^2 - m^2) = 0 ; photon M^{mu nu} = -k^2 g^{mu nu} + k^mu k^nu
w_, kx, ky, kz = sp.symbols('omega k_x k_y k_z', real=True)
kup = sp.Matrix([w_, kx, ky, kz]); ksq = w_**2 - kx**2 - ky**2 - kz**2
gup = sp.diag(1, -1, -1, -1)
Mph = -ksq * gup + kup * kup.T
# physical (non-gauge) solutions: rank of M; for k^2 != 0 rank 3 with null vector k (pure gauge only)
num_k = {w_: sp.Rational(7, 5), kx: sp.Rational(1, 3), ky: sp.Rational(-1, 2), kz: sp.Rational(2, 7)}
rank_off = Mph.subs(num_k).rank()
kk = sp.sqrt(sp.Rational(1, 9) + sp.Rational(1, 4) + sp.Rational(4, 49))
on_shell = {w_: kk, kx: sp.Rational(1, 3), ky: sp.Rational(-1, 2), kz: sp.Rational(2, 7)}
rank_on = sp.simplify(Mph.subs(on_shell)).rank()
check("10e. Maxwell: off the cone (k^2!=0) M(k) has rank 3, null space = pure gauge k^mu; on the cone rank 1 (two transverse photons + gauge)",
      rank_off == 3 and rank_on == 1, "rank(k^2!=0)=%d, rank(k^2=0)=%d" % (rank_off, rank_on))
# dispersion and boost invariance
kmag = sp.symbols('kmag', positive=True)
om_pi = sp.sqrt(kmag**2 + mpi**2)
vgroup = sp.diff(om_pi, kmag)
check("10f. pion: omega^2 = k^2 + m^2, group velocity k/omega < 1 -> 1 as k -> oo; photon omega = |k| (phase=group=1)",
      sp.limit(vgroup, kmag, sp.oo) == 1, "v_g = %s" % sp.simplify(vgroup))
beta = sp.symbols('beta', real=True)
gam = 1 / sp.sqrt(1 - beta**2)
Bx = sp.Matrix([[gam, -gam * beta, 0, 0], [-gam * beta, gam, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
kb = Bx * kup
ksq_b = kb[0]**2 - kb[1]**2 - kb[2]**2 - kb[3]**2
check("10g. k^2 is boost invariant, so both dispersion relations hold in every frame (one cone, no preferred frame)",
      sp.simplify(ksq_b - ksq) == 0, "")

# 11. vacuum stress tensor with a general metric: L = (F^2/16) g^{mu nu} Tr(d_mu U d_nu U^+) + Skyrme(g) + mass - V0
V0s = sp.symbols('V0', real=True)
gs = sp.Matrix(4, 4, lambda i, j: sp.Symbol('g%d%d' % (min(i, j), max(i, j))))
dUs = [sp.Matrix(2, 2, lambda i, j: sp.Symbol('u%d_%d%d' % (mu, i, j))) for mu in range(4)]
Ls = [dUs[mu] for mu in range(4)]   # at U = 1, L_mu = d_mu U
Lag = (F0**2 / 16) * sum(gs[mu, nu] * (dUs[mu] * dUs[nu].T).trace() for mu in range(4) for nu in range(4)) \
    + sum(gs[mu, al] * gs[nu, be] * (comm(Ls[mu], Ls[nu]) * comm(Ls[al], Ls[be])).trace()
          for mu in range(4) for nu in range(4) for al in range(4) for be in range(4)) / (32 * es**2) - V0s
gflat = sp.diag(1, -1, -1, -1)
subs_flat = {gs[i, j]: gflat[i, j] for i in range(4) for j in range(4)}
subs_vac = {sym: 0 for M_ in dUs for sym in M_}
Tmn = sp.zeros(4, 4)
for mu in range(4):
    for nu in range(4):
        dL = sp.diff(Lag, gs[mu, nu]) * (1 if mu == nu else sp.Rational(1, 2))   # symmetric metric
        Tmn[mu, nu] = sp.simplify((2 * dL - gflat[mu, nu] * Lag).subs(subs_vac).subs(subs_flat))
check("11a. vacuum (U=1, dU=0): T_mu nu = 2 dL/dg^{mu nu} - g_mu nu L = V0 g_mu nu (mostly-minus; = -V0 g in mostly-plus)",
      sp.simplify(Tmn - V0s * gflat) == sp.zeros(4, 4), str(Tmn.tolist()))
rho_v = Tmn[0, 0]
p_v = Tmn[1, 1]     # perfect fluid at rest: T_mu nu = (rho+p) u u - p g  ->  T_11 = p (g_11 = -1)
check("11b. rho = T_00 = V0 and p = T_11 = -V0: p = -rho (taut vacuum)", sp.simplify(rho_v + p_v) == 0, "rho=%s p=%s" % (rho_v, p_v))
Tb_boost = sp.simplify(Bx.T * Tmn * Bx)
check("11c. boosted vacuum T_mu nu is unchanged (Lambda^T g Lambda = g): same in every frame", sp.simplify(Tb_boost - Tmn) == sp.zeros(4, 4), "")

# ---------------------------------------------------------------- export radial integrands (per unit volume)
out = {
    "units": "e = F_pi = 1 (F_pi in the 186-MeV convention); r in 1/(e F_pi); per-unit-volume densities",
    "energy_density": str(sp.simplify(eps_static.subs(c**2, 1 - s**2))),
    "lambda_density": str(lam_dens_expected),
    "lambda_density_derived_from_isospin_charge": str(sp.simplify(sph_avg(V0[0]).coeff(W1).subs(c**2, 1 - s**2))),
    "I2_density": str(I2_dens_expected),
    "vector_g": str(sp.simplify(g_r)),
    "baryon_density": str(B0_expected),
    "axial_f1": str(sp.simplify(f1_r)),
    "axial_f2": str(sp.simplify(f2_r)),
    "axial_sphere_density_f1_plus_f2_over_3": str(sp.simplify(GA_dens)),
    "kappa_baryon": str(kap_val),
    "pi0_amplitude_coefficient": str(Acoef),
    "pi0_width_formula": str(Gamma),
    "pi0_effective_coupling_K": str(K),
    "vacuum_T": str(Tmn.tolist()),
    "checks": CHECKS,
    "n_pass": sum(1 for x in CHECKS if x["passed"]),
    "n_fail": sum(1 for x in CHECKS if not x["passed"]),
    "runtime_s": round(time.time() - t_start, 1),
}
with open(__file__.replace("symbolic_derivations.py", "symbolic_results.json"), "w") as fh:
    json.dump(out, fh, indent=1)
print("\n%d checks passed, %d failed, %.1f s" % (out["n_pass"], out["n_fail"], out["runtime_s"]))
