#!/usr/bin/env python3
"""A4 first-leg checks (locked pre-registration A4_PREREG.md md5 7b876a2720da53884933b0a512ca8df8).

DR-A4-2: symbolic re-derivation of the classical facts used against §2.90
  (a) centre of dilatation in isotropic linear elasticity (3D and 2D): traceless strain outside the core, so zero
      interaction energy with a second centre of dilatation (Eshelby 1956);
  (a') general force dipoles: interaction energy homogeneous of degree -3 in the separation (Kelvin Green's function);
  (b) a 1/r interaction needs net forces (monopoles): monopole-monopole energy is degree -1;
  (c) uniform tension (prestress) keeps the Navier form with shifted constants: the dilatation field still solves it,
      the Green's function stays homogeneous of degree -1.
DR-A4-3: order-of-magnitude KC-EP sensitivities for MICROSCOPE's Ti/Pt pair.
"""
import json, hashlib, math
import sympy as sp

H = "/home/claude/gifgaf0.github.io/audit_followup/A4_gravity"
assert hashlib.md5(open(H + "/A4_PREREG.md", "rb").read()).hexdigest() == "7b876a2720da53884933b0a512ca8df8"
OUT = {}
x, y, z, lam = sp.symbols("x y z lambda", positive=True)
X = sp.Matrix([x, y, z]); r = sp.sqrt(x**2 + y**2 + z**2)
mu, nu, T, C = sp.symbols("mu nu T C", positive=True)

# (a) centre of dilatation, 3D: u = C x / r^3
u = C*X/r**3
eps = sp.Matrix(3, 3, lambda i, j: sp.Rational(1, 2)*(sp.diff(u[i], X[j]) + sp.diff(u[j], X[i])))
tr3 = sp.simplify(eps.trace())
# Navier operator mu lap u + (lambda_L + mu) grad div u with u = C x/r^3: both terms vanish away from 0
lamL = sp.symbols("lambda_L", positive=True)
lap = lambda f: sum(sp.diff(f, v, 2) for v in X)
div = sum(sp.diff(u[i], X[i]) for i in range(3))
navier = sp.simplify(sp.Matrix([mu*lap(u[i]) + (lamL + mu)*sp.diff(div, X[i]) for i in range(3)]))
print("(a) 3D centre of dilatation u = C x/r^3:  tr(eps) =", tr3, ";  Navier residual =", list(navier))
OUT["a_3d_trace"] = str(tr3); OUT["a_3d_navier_residual_zero"] = all(sp.simplify(c) == 0 for c in navier)
# interaction energy with a second centre of dilatation (isotropic dipole P delta_ij): W = -P tr eps = 0
P = sp.symbols("P")
OUT["a_W_dilatation_pair"] = str(sp.simplify(-P*tr3))
# 2D: u = C (x, y)/rho^2
rho = sp.sqrt(x**2 + y**2)
u2 = sp.Matrix([C*x/rho**2, C*y/rho**2])
tr2 = sp.simplify(sp.diff(u2[0], x) + sp.diff(u2[1], y))
print("(a) 2D centre of dilatation u = C x/rho^2: tr(eps) =", tr2)
OUT["a_2d_trace"] = str(tr2)

# (a') Kelvin Green's function and two general force dipoles
def kelvin(mu_, nu_):
    G = sp.zeros(3, 3)
    for i in range(3):
        for j in range(3):
            G[i, j] = ((3 - 4*nu_)*sp.KroneckerDelta(i, j) + X[i]*X[j]/r**2) / (16*sp.pi*mu_*(1 - nu_)*r)
    return G
G = kelvin(mu, nu)
# check G solves Navier with unit point force away from the origin (mu lap G + (lambda+mu) grad div G = 0 for r>0)
lam_of = 2*mu*nu/(1 - 2*nu)
res = []
for k in range(3):
    col = G[:, k]
    dv = sum(sp.diff(col[i], X[i]) for i in range(3))
    res += [sp.simplify(mu*lap(col[i]) + (lam_of + mu)*sp.diff(dv, X[i])) for i in range(3)]
print("(a') Kelvin G solves Navier away from 0:", all(c == 0 for c in res))
OUT["kelvin_solves_navier"] = all(c == 0 for c in res)
def dipole_strain(Pm, Gm):
    # displacement of a force dipole P_kl at the origin: u_i = -P_kl d_l G_ik
    uu = sp.Matrix([-sum(Pm[k, l]*sp.diff(Gm[i, k], X[l]) for k in range(3) for l in range(3)) for i in range(3)])
    return sp.Matrix(3, 3, lambda i, j: sp.Rational(1, 2)*(sp.diff(uu[i], X[j]) + sp.diff(uu[j], X[i])))
p1, p3, q1, q3 = sp.symbols("p1 p3 q1 q3")
P_tet = sp.diag(p1, p1, p3); Q_tet = sp.diag(q1, q1, q3)
eps_tet = dipole_strain(P_tet, G)
W = sp.simplify(-sum(Q_tet[i, j]*eps_tet[i, j] for i in range(3) for j in range(3)))
W_scaled = sp.simplify(W.subs({x: lam*x, y: lam*y, z: lam*z}, simultaneous=True) / W)
print("(a') tetragonal force dipoles: W(lambda x)/W(x) =", W_scaled)
W_iso = sp.simplify(W.subs({p3: p1, q3: q1}))
print("(a') isotropic limit (p1=p3, q1=q3): W =", W_iso)
# angular average of W over directions on a sphere (isotropic medium): integrate in spherical coordinates
th, ph, R0 = sp.symbols("theta phi R0", positive=True)
W_sph = sp.simplify(W.subs({x: R0*sp.sin(th)*sp.cos(ph), y: R0*sp.sin(th)*sp.sin(ph), z: R0*sp.cos(th)}, simultaneous=True))
W_avg = sp.simplify(sp.integrate(sp.integrate(W_sph*sp.sin(th), (ph, 0, 2*sp.pi)), (th, 0, sp.pi)) / (4*sp.pi))
print("(a') orientation average of the tetragonal dipole-dipole energy:", W_avg)
OUT["dipole_W_scaling"] = str(W_scaled); OUT["dipole_W_isotropic_limit"] = str(W_iso); OUT["dipole_W_angular_average"] = str(W_avg)

# (b) monopole-monopole: W = -F2 . u1(x), u1 = G F1  -> degree -1
F1 = sp.Matrix(sp.symbols("F1x F1y F1z")); F2 = sp.Matrix(sp.symbols("F2x F2y F2z"))
Wm = sp.simplify(-(F2.T*(G*F1))[0])
Wm_scaled = sp.simplify(Wm.subs({x: lam*x, y: lam*y, z: lam*z}, simultaneous=True) / Wm)
print("(b) monopole-monopole: W(lambda x)/W(x) =", Wm_scaled, " (the only 1/r term; it needs net forces F1, F2 != 0)")
OUT["monopole_W_scaling"] = str(Wm_scaled)
# monopole-dipole: degree -2
eps_mono = sp.Matrix(3, 3, lambda i, j: sp.Rational(1, 2)*(sp.diff((G*F1)[i], X[j]) + sp.diff((G*F1)[j], X[i])))
Wmd = sp.simplify(-sum(Q_tet[i, j]*eps_mono[i, j] for i in range(3) for j in range(3)))
Wmd_scaled = sp.simplify(Wmd.subs({x: lam*x, y: lam*y, z: lam*z}, simultaneous=True) / Wmd)
print("(b) monopole-dipole: W(lambda x)/W(x) =", Wmd_scaled)
OUT["monopole_dipole_W_scaling"] = str(Wmd_scaled)

# (c) uniform tension T: geometric-stiffness term T lap u added -> mu' = mu + T, lambda' = lambda - T (same Navier form)
navierT = sp.simplify(sp.Matrix([(mu + T)*lap(u[i]) + (lamL + mu)*sp.diff(div, X[i]) for i in range(3)]))
print("(c) prestressed Navier operator on the dilatation field: residual =", list(navierT))
OUT["c_prestress_dilatation_residual_zero"] = all(sp.simplify(c) == 0 for c in navierT)

# ---------------------------------------------------------------------------------------------------------------
# DR-A4-3: KC-EP sensitivities for Ti / Pt (order of magnitude)
# ---------------------------------------------------------------------------------------------------------------
eta_c, s_stat, s_sys = -1.5e-15, 2.3e-15, 1.5e-15
eta_2s = abs(eta_c) + 2*math.hypot(s_stat, s_sys)            # ~2-sigma bound on |eta|
m_e_u = 5.48579909e-4                                       # electron mass in u
mu_c2 = 931.494                                             # MeV
def semf(A, Z):                                             # binding energy (MeV), standard SEMF coefficients
    av, as_, ac, aa = 15.75, 17.8, 0.711, 23.7
    return av*A - as_*A**(2/3) - ac*Z*(Z - 1)/A**(1/3) - aa*(A - 2*Z)**2/A
mats = {"Ti": (22, 47.867), "Pt": (78, 195.084)}           # Z, standard atomic weight
f = {}
for k, (Z, A) in mats.items():
    f[k] = dict(electron=Z*m_e_u/A, binding=semf(A, Z)/(A*mu_c2), coulomb=0.711*Z*(Z - 1)/A**(1/3)/(A*mu_c2),
                neutron_excess=(A - 2*Z)/A)
sens = {}
print(f"\nKC-EP: MICROSCOPE eta(Ti,Pt) = {eta_c:.1e} +- {s_stat:.1e} (stat) +- {s_sys:.1e} (syst); 2-sigma |eta| < {eta_2s:.1e}")
for comp in ("electron", "binding", "coulomb", "neutron_excess"):
    d = abs(f["Ti"][comp] - f["Pt"][comp])
    sens[comp] = dict(f_Ti=f["Ti"][comp], f_Pt=f["Pt"][comp], delta_f=d, delta_coupling_bound=eta_2s/d)
    print(f"  {comp:15s} f_Ti = {f['Ti'][comp]:.3e}  f_Pt = {f['Pt'][comp]:.3e}  |df| = {d:.2e}  -> anomalous coupling |delta| < {eta_2s/d:.0e}")
OUT["kcep"] = dict(eta=eta_c, sigma_stat=s_stat, sigma_sys=s_sys, eta_bound_2sigma=eta_2s, components=sens)
# what §2.90's own hierarchy implies if non-topological field energy (binding + Coulomb) does not gravitate
eta_290 = abs((f["Ti"]["binding"]) - (f["Pt"]["binding"]))
print(f"  if binding energy carried no persistent deficit (the §2.90 'transient, no topology: zero' class): |eta| ~ {eta_290:.1e}"
      f" = {eta_290/eta_2s:.0e} x the MICROSCOPE bound")
OUT["kcep"]["eta_if_binding_not_gravitating"] = eta_290
json.dump(OUT, open(H + "/a4_results.json", "w"), indent=1, default=str)
print("\ndone")
