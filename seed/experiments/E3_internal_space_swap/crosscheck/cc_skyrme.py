#!/usr/bin/env python3
"""Independent cross-check of E3: hedgehog profile, G2 inertia tensor, embedded-hedgehog
baryon numbers, rotor energies in MeV, SU(3) refit.

Different methods from the original:
  * profile from scipy solve_bvp (collocation) on [eps, X] with a Robin condition from the
    asymptotic expansion (original: two-sided shooting);
  * inertia tensor computed in the 14-dim ADJOINT representation with structure constants of my
    own g2 basis (3-form construction, cc_g2.py), Lebedev angular quadrature and a mapped
    Gauss-Legendre radial rule (original: 7x7 matrices, Gauss x uniform angular grid);
    repeated in the 7 as a representation-independence check.
Units: x = e F r, M in F/e, I in 1/(e^3 F).
"""
import json, time
import numpy as np
from scipy.integrate import solve_bvp, quad, lebedev_rule
from scipy.linalg import expm

checks = []
def check(name, ok, val=None):
    checks.append({"check": name, "pass": bool(ok), "value": val})
    print(("PASS " if ok else "FAIL ") + name + ("" if val is None else f"  [{val}]"), flush=True)

# ------------------------------------------------------------------ profile
def rhs(x, y):
    F, P = y
    s, s2 = np.sin(F), np.sin(2 * F)
    num = s2 + 4 * s * s * s2 / x ** 2 - 2 * x * P - 4 * s2 * P ** 2
    return np.vstack([P, num / (x ** 2 + 8 * s * s)])

def solve_profile(X, eps=1e-5, tol=1e-11):
    def bc(ya, yb):
        # F(eps) = pi + F'(eps) eps (regular expansion F = pi + a x + O(x^3));  Robin at X from F ~ C/x^2 - C^3/(21 x^6)
        # use leading Robin: x F' + 2 F = O(x^-6) correction: x F' + 2F = 4 C^3/(21 x^6) ~ (4/21) F^3
        return np.array([ya[0] - np.pi - ya[1] * eps,
                         X * yb[1] + 2 * yb[0] - (4.0 / 21.0) * yb[0] ** 3])
    x = np.concatenate([np.linspace(eps, 5, 400), np.geomspace(5.01, X, 400)])
    F0 = np.where(x < 1e-3, np.pi - x, np.pi / (1 + (x / 1.4) ** 2 * (1 + 0 * x)))   # crude guess
    y0 = np.vstack([F0, np.gradient(F0, x)])
    sol = solve_bvp(rhs, bc, x, y0, tol=tol, max_nodes=200000, bc_tol=1e-12)
    return sol

profiles = {}
for X in (60.0, 120.0, 240.0):
    t0 = time.time()
    sol = solve_profile(X)
    a = sol.sol(sol.x[0])[1]
    C = sol.sol(X)[0] * X ** 2
    profiles[X] = sol
    print(f"X={X}: status={sol.status} nodes={sol.x.size} F'(0)={a:.10f} C~{C:.8f} rms_res={np.max(sol.rms_residuals):.2e}  {time.time()-t0:.1f}s", flush=True)

sol = profiles[240.0]
Xmax = 240.0
Fp0 = float(sol.sol(sol.x[0])[1])
# asymptotic coefficient: fit F = C/x^2 - C^3/(21 x^6) at X
FX = float(sol.sol(Xmax)[0])
from scipy.optimize import brentq
C = brentq(lambda c: c / Xmax ** 2 - c ** 3 / (21 * Xmax ** 6) - FX, 1, 20)

def prof(x):
    x = np.asarray(x, float)
    F = np.empty_like(x); P = np.empty_like(x)
    m = x <= Xmax
    if m.any():
        xm = np.maximum(x[m], sol.x[0])
        yy = sol.sol(xm)
        # regular extension below eps: F = pi + a x
        F[m] = np.where(x[m] < sol.x[0], np.pi + Fp0 * x[m], yy[0])
        P[m] = np.where(x[m] < sol.x[0], Fp0, yy[1])
    if (~m).any():
        xx = x[~m]
        F[~m] = C / xx ** 2 - C ** 3 / (21 * xx ** 6)
        P[~m] = -2 * C / xx ** 3 + 6 * C ** 3 / (21 * xx ** 7)
    return F, P

# radial integrals via mapped Gauss-Legendre on [0, inf): x = c s/(1-s)
def radial_rule(n, c=1.5):
    s, w = np.polynomial.legendre.leggauss(n)
    s = 0.5 * (s + 1); w = 0.5 * w
    x = c * s / (1 - s); jac = c / (1 - s) ** 2
    return x, w * jac

def integrals(n):
    x, w = radial_rule(n)
    F, P = prof(x)
    s2 = np.sin(F) ** 2
    e2 = 4 * np.pi * x ** 2 * (1 / 8) * (P ** 2 + 2 * s2 / x ** 2)
    e4 = 4 * np.pi * x ** 2 * (1 / 2) * (s2 / x ** 2) * (s2 / x ** 2 + 2 * P ** 2)
    Lam = x ** 2 * s2 * (1 + 4 * (P ** 2 + s2 / x ** 2))
    J2 = x ** 2 * 2 * np.sin(F / 2) ** 2 * (1 + P ** 2 + 2 * s2 / x ** 2)   # 2 sin^2(F/2): no cancellation in the tail
    Bd = -(2 / np.pi) * s2 * P
    return dict(E2=float(w @ e2), E4=float(w @ e4), M=float(w @ (e2 + e4)), Lambda=float(w @ Lam),
                J2=float(w @ J2), B=float(w @ Bd))

r1 = integrals(400); r2 = integrals(800)
print("radial integrals n=400:", r1)
print("radial integrals n=800:", r2)
res = r2
M = res["M"]; Lam = res["Lambda"]
I1_rad = 2 * np.pi / 3 * Lam
I2_rad = np.pi / 2 * res["J2"]
check("virial E2 = E4 (|E2-E4|/M < 1e-8)", abs(res["E2"] - res["E4"]) / M < 1e-8, (res["E2"] - res["E4"]) / M)
check("baryon number of profile = 1", abs(res["B"] - 1) < 1e-8, res["B"])
check("radial quadrature converged (n=400 vs 800, rel < 1e-10 on M, Lambda, J2)",
      max(abs(r1[k] - r2[k]) / abs(r2[k]) for k in ("M", "Lambda", "J2")) < 1e-10)
# profile-X convergence
def M_of(solX, X):
    xs = np.linspace(solX.x[0], X, 200001)
    F, P = solX.sol(xs)
    s2 = np.sin(F) ** 2
    dens = 4 * np.pi * (x2 := xs ** 2) * ((1 / 8) * (P ** 2 + 2 * s2 / x2) + 0.5 * (s2 / x2) * (s2 / x2 + 2 * P ** 2))
    return np.trapezoid(dens, xs)
dFp = {X: float(profiles[X].sol(profiles[X].x[0])[1]) for X in profiles}
check("F'(0) stable under X = 60, 120, 240 (spread < 1e-8)", max(dFp.values()) - min(dFp.values()) < 1e-8, dFp)
Mtarget = 1.2315 * 3 * np.pi ** 2
print(f"M = {M:.9f}  (target 1.2315*3pi^2 = {Mtarget:.6f}, ratio M/3pi^2 = {M/(3*np.pi**2):.7f})")
print(f"Lambda = {Lam:.9f}  I1 = {I1_rad:.9f}   J2 = {res['J2']:.9f}  I2 = {I2_rad:.9f}  F'(0) = {Fp0:.10f}  C = {C:.9f}")
check("M_cl within 0.2% of 1.2315 x 3 pi^2", abs(M / Mtarget - 1) < 2e-3, M)
check("Lambda within 0.5% of 50.9", abs(Lam / 50.9 - 1) < 5e-3, Lam)
check("I2 within 1.5% of arctan-ansatz 40.5", abs(I2_rad / 40.5 - 1) < 1.5e-2, I2_rad)

# ------------------------------------------------------------------ G2 inertia tensor (adjoint rep)
gb = np.load("cc_g2_basis.npz")
f = gb["f"]; G7 = gb["G"]; basis_c = gb["basis_c"]; TL7 = gb["TL"]; TS7 = gb["TS"]
ad = np.array([f[a].T for a in range(14)])         # (ad_a)_{cb} = f_abc
Lc = basis_c[:3]                                   # long generators (components)

def su2_l(xyz):
    """SU(2) left current l_i = U^dag d_i U, U = exp(2F n.t) = cos F - i sin F n.sigma, t = -i sigma/2.
    returns components c[i, a] with l_i = sum_a c[i,a] t_a, at points xyz (N,3)."""
    r = np.linalg.norm(xyz, axis=1)
    n = xyz / r[:, None]
    F, P = prof(r)
    sF, cF = np.sin(F), np.cos(F)
    sig = np.array([[[0, 1], [1, 0]], [[0, -1j], [1j, 0]], [[1, 0], [0, -1]]], complex)
    ns = np.einsum('na,aij->nij', n, sig)
    U = cF[:, None, None] * np.eye(2) - 1j * sF[:, None, None] * ns
    Ud = np.conj(np.transpose(U, (0, 2, 1)))
    t = -0.5j * sig
    c = np.zeros((len(r), 3, 3))
    for i in range(3):
        dn = (np.eye(3)[i][None, :] - n[:, i:i + 1] * n) / r[:, None]      # d_i n_a
        dns = np.einsum('na,aij->nij', dn, sig)
        dU = (-sF * P * n[:, i])[:, None, None] * np.eye(2) - 1j * (cF * P * n[:, i])[:, None, None] * ns \
             - 1j * sF[:, None, None] * dns
        l = Ud @ dU
        for a in range(3):
            c[:, i, a] = (-2 * np.einsum('ij,nji->n', t[a], l)).real
    return c, F, n, r

def inertia_adjoint(nr, leb_order, rule_c=1.5):
    xr, wr = radial_rule(nr, rule_c)
    nodes, wl = lebedev_rule(leb_order)
    nodes = nodes.T
    I = np.zeros((14, 14)); Bsum = 0.0; Esum = 0.0
    for k in range(nr):
        xyz = xr[k] * nodes
        c, F, n, r = su2_l(xyz)
        lcomp = np.einsum('nia,ab->nib', c, Lc)                 # l_i components in g2 basis (N,3,14)
        Xc = 2 * F[:, None] * np.einsum('na,ab->nb', n, Lc)      # X = 2F n.T^L
        adX = np.einsum('nb,bij->nij', Xc, ad)
        AdUinv = expm(-adX)                                     # Ad(U0^{-1}) on components
        Mmat = AdUinv - np.eye(14)[None]                        # column a = components of M_a
        # [M_a, l_i]^e = f_cde M_a^c l_i^d
        Ml = np.einsum('cde,nca,nid->niae', f, Mmat, lcomp)
        dens = (np.einsum('nca,ncb->nab', Mmat, Mmat) + np.einsum('niae,nibe->nab', Ml, Ml)) / 16.0
        I += wr[k] * xr[k] ** 2 * np.einsum('n,nab->ab', wl, dens)
        # static energy and baryon density from components (checks of the current)
        l2 = np.einsum('nia,nia->n', lcomp, lcomp)
        comm = np.einsum('abc,nia,njb->nijc', f, lcomp, lcomp)
        e = l2 / 32 + np.einsum('nijc,nijc->n', comm, comm) / 64
        eps = np.zeros((3, 3, 3)); eps[0, 1, 2] = eps[1, 2, 0] = eps[2, 0, 1] = 1; eps[0, 2, 1] = eps[2, 1, 0] = eps[1, 0, 2] = -1
        # B = (1/96 pi^2) eps_ijk <l_i,[l_j,l_k]> with <.,.> = -Tr_7, N=1/2 (sign fixed below)
        bdens = np.einsum('ijk,nic,njkc->n', eps, lcomp, comm) / (96 * np.pi ** 2)
        Bsum += wr[k] * xr[k] ** 2 * (wl @ bdens)
        Esum += wr[k] * xr[k] ** 2 * (wl @ e)
    return I, Bsum, Esum

t0 = time.time()
I_a, B_a, E_a = inertia_adjoint(160, 23)
print(f"adjoint inertia (160 radial, Lebedev 23): {time.time()-t0:.1f}s", flush=True)
t0 = time.time()
I_b, B_b, E_b = inertia_adjoint(240, 31, rule_c=2.5)
print(f"adjoint inertia (240 radial, Lebedev 31, other map): {time.time()-t0:.1f}s", flush=True)
ev = np.linalg.eigvalsh(I_b)
print("eigenvalues:", ev)
Iblk = basis_c @ I_b @ basis_c.T
off = max(np.abs(Iblk[:3, 3:]).max(), np.abs(Iblk[3:6, 6:]).max(), np.abs(Iblk[3:6, :3]).max())
I1_3d = np.mean(np.diag(Iblk)[:3]); I2_3d = np.mean(np.linalg.eigvalsh(Iblk[6:, 6:])); I0_3d = np.abs(Iblk[3:6, 3:6]).max()
print(f"I1(3D) = {I1_3d:.10f}  I2(3D) = {I2_3d:.10f}  short block max |I| = {I0_3d:.2e}  off-block = {off:.2e}")
check("quadrature-rule independence of inertia tensor (two radial maps/Lebedev orders), rel < 1e-9",
      np.abs(I_a - I_b).max() / I1_3d < 1e-9, float(np.abs(I_a - I_b).max()))
check("inertia eigenvalue multiplicities 3 x 0, 8 x I2, 3 x I1",
      np.allclose(ev[:3], 0, atol=1e-9) and np.allclose(ev[3:11], ev[3], rtol=1e-10) and np.allclose(ev[11:], ev[11], rtol=1e-10))
check("block diagonal in (3,1)+(1,3)+(2,4) basis (off-block < 1e-10)", off < 1e-10, float(off))
check("long block I1(3D) = (2pi/3) Lambda (rel < 1e-8)", abs(I1_3d / I1_rad - 1) < 1e-8, (I1_3d, I1_rad))
check("(2,4) block I2(3D) = Kopeliovich radial formula (rel < 1e-8)", abs(I2_3d / I2_rad - 1) < 1e-8, (I2_3d, I2_rad))
check("short block zero (< 1e-12)", I0_3d < 1e-12, float(I0_3d))
check("static energy from g2 currents (adjoint route) = M", abs(E_b / M - 1) < 1e-9, (E_b, M))
check("|B| from g2 currents with (1/2)Tr_7 normalisation = 1", abs(abs(B_b) - 1) < 1e-9, B_b)

# ------------------------------------------------------------------ same in the 7 (representation independence)
def inertia_7(nr, leb_order):
    xr, wr = radial_rule(nr)
    nodes, wl = lebedev_rule(leb_order); nodes = nodes.T
    Tb = np.einsum('ab,bij->aij', basis_c, G7)   # adapted basis, 7x7
    TLm = TL7
    I = np.zeros((14, 14))
    for k in range(nr):
        xyz = xr[k] * nodes
        c, F, n, r = su2_l(xyz)
        l7 = np.einsum('nia,ajk->nijk', c, TLm)
        U = expm(2 * F[:, None, None] * np.einsum('na,ajk->njk', n, TLm))
        Ut = np.transpose(U, (0, 2, 1))
        Mm = np.einsum('nij,ajk,nkl->nail', Ut, Tb, U) - Tb[None]
        Mn = Mm  # (N,14,7,7)
        tr1 = -np.einsum('naij,nbji->nab', Mn, Mn)
        com = np.einsum('naij,nqjk->nqaik', Mn, l7) - np.einsum('nqij,najk->nqaik', l7, Mn)
        tr2 = -np.einsum('nqaij,nqbji->nab', com, com)
        dens = (tr1 + tr2) / 16.0
        I += wr[k] * xr[k] ** 2 * np.einsum('n,nab->ab', wl, dens)
    return I
t0 = time.time()
I7 = inertia_7(120, 23)
print(f"7-dim inertia: {time.time()-t0:.1f}s")
I7b = I7   # inertia_7 already works in the adapted basis
check("7-dim (Tr_7) inertia equals adjoint-rep result (rel < 1e-8)", np.abs(I7b - Iblk).max() / I1_3d < 1e-8,
      float(np.abs(I7b - Iblk).max()))

# ------------------------------------------------------------------ embedded hedgehogs in other SU(2)'s: E and B scale with index
# For U = exp(2F n.T) with T an index-k su(2), l_i = sum c_i^a T_a and <T_a,T_b> = k delta_ab, so every
# quadratic and cubic invariant scales by k: E = k M, B = k. Verify numerically for the short root (k=3) via adjoint route.
TSc = basis_c[3:6] * np.sqrt(3)
def EB_embedded(Tc, nr=120, leb=23):
    xr, wr = radial_rule(nr)
    nodes, wl = lebedev_rule(leb); nodes = nodes.T
    eps = np.zeros((3, 3, 3)); eps[0, 1, 2] = eps[1, 2, 0] = eps[2, 0, 1] = 1; eps[0, 2, 1] = eps[2, 1, 0] = eps[1, 0, 2] = -1
    Es = 0; Bs = 0
    for k in range(nr):
        c, F, n, r = su2_l(xr[k] * nodes)
        lc = np.einsum('nia,ab->nib', c, Tc)
        comm = np.einsum('abc,nia,njb->nijc', f, lc, lc)
        e = np.einsum('nia,nia->n', lc, lc) / 32 + np.einsum('nijc,nijc->n', comm, comm) / 64
        bd = np.einsum('ijk,nic,njkc->n', eps, lc, comm) / (96 * np.pi ** 2)
        Es += wr[k] * xr[k] ** 2 * (wl @ e); Bs += wr[k] * xr[k] ** 2 * (wl @ bd)
    return Es, Bs
Es3, Bs3 = EB_embedded(TSc)
check("short-root hedgehog: E = 3 M, |B| = 3", abs(Es3 / M - 3) < 1e-8 and abs(abs(Bs3) - 3) < 1e-8, (Es3 / M, Bs3))

# ------------------------------------------------------------------ MeV, refit
I1 = I1_3d; I2 = I2_3d
ratio = I1 / I2
def mev(Fpi, e):
    return dict(M=M * Fpi / e, invI1=e ** 3 * Fpi / I1, invI2=e ** 3 * Fpi / I2)
anw = mev(129.0, 5.45)
print("ANW:", anw)
# PDG centres (own query)
try:
    import pdg
    api = pdg.connect()
    def mass(pdgid):
        return api.get(pdgid).mass * 1000.0
    names = None
    oct_ids = ["S016", "S017", "S018", "S019", "S020", "S021", "S022", "S023"]
    octet = []
    for nm in ["p", "n", "Lambda", "Sigma+", "Sigma0", "Sigma-", "Xi0", "Xi-"]:
        octet.append(api.get_particles_by_name(nm)[0].mass * 1000.0)
    dec = []
    for nm in ["Sigma(1385)+", "Sigma(1385)0", "Sigma(1385)-", "Xi(1530)0", "Xi(1530)-", "Omega-"]:
        dec.append(api.get_particles_by_name(nm)[0].mass * 1000.0)
    src = "pdg package"
except Exception as ex:
    print("pdg query failed:", ex)
    octet = None; dec = None; src = "failed"
print("octet masses:", octet)
print("decuplet (excluding Delta):", dec)
def fit(E8, E10):
    e3F = (E10 - E8) * I1 / 1.5
    rot8 = (3 / (8 * I1) + 3 / (4 * I2)) * e3F
    FoverE = (E8 - rot8) / M
    e = (e3F / FoverE) ** 0.25
    Fpi = FoverE * e
    return Fpi, e, E8 + 1.5 * e3F / I2
refit = {}
if octet is not None and len(octet) == 8 and len(dec) == 6:
    E8 = float(np.mean(octet))
    for dm, lab in [(1232.0, "Delta 1232.0"), (1210.0 + 0 * 1, "Delta pole-ish 1210 (sensitivity only)")]:
        E10 = float((4 * dm + sum(dec)) / 10)
        Fpi, e, a10 = fit(E8, E10)
        refit[lab] = dict(E8=E8, E10=E10, F_pi=Fpi, e=e, antidecuplet=a10)
        print(lab, refit[lab])
F_r, e_r = refit["Delta 1232.0"]["F_pi"], refit["Delta 1232.0"]["e"]
ref = mev(F_r, e_r)
print("refit point:", ref)

g2 = json.load(open("cc_g2.json"))
states = []
for s in g2["allowed_states"]:
    from fractions import Fraction
    c2 = float(Fraction(s["C2"])); J = s["J"]
    u = J * (J + 1) / 2 + (c2 - J * (J + 1)) / 2 * ratio          # (E-M)*I1
    states.append(dict(R=s["R"], C2=s["C2"], J=J, EminusM_I1=u,
                       E_ANW=anw["M"] + u * anw["invI1"], E_refit=ref["M"] + u * ref["invI1"]))
states.sort(key=lambda z: z["EminusM_I1"])
for s in states[:12]:
    print(f"{s['R']:>10} J={s['J']:.0f} (E-M)I1={s['EminusM_I1']:.4f}  E_ANW={s['E_ANW']:.1f}  E_refit={s['E_refit']:.1f}")
check("lowest state 1 (J=0), next 14 (J=1)", states[0]["R"].startswith("1[") and states[1]["R"].startswith("14[") and states[1]["J"] == 1)

json.dump({"checks": checks,
           "profile": dict(Fp0=Fp0, C=C, M=M, Lambda=Lam, J2=res["J2"], E2=res["E2"], E4=res["E4"], B=res["B"],
                           I1_radial=I1_rad, I2_radial=I2_rad, Fp0_vs_X=dFp),
           "inertia": dict(eigenvalues=ev.tolist(), I1=I1_3d, I2=I2_3d, short_max=I0_3d, offblock=off,
                           ratio_I1_I2=ratio, I7_vs_adj=float(np.abs(I7b - Iblk).max())),
           "embedded_short_root": dict(E_over_M=Es3 / M, B=Bs3),
           "ANW": anw, "refit": refit, "refit_point": ref, "states": states[:14]},
          open("cc_skyrme.json", "w"), indent=1)
np.savez("cc_profile.npz", x=sol.x, F=sol.y[0], P=sol.y[1], C=C, Xmax=Xmax)
nf = sum(not c["pass"] for c in checks)
print(f"\n{len(checks) - nf}/{len(checks)} checks passed")
