"""Independent check of the LBC exploration result.

1. Re-derive the T=0 supersolid longitudinal response from the Son / Yoo-Dorsey Lagrangian
   L2 = -drho*theta_t - rho/2 (theta_x)^2 + rho_n/2 (u_t - theta_x)^2
        - alpha/2 drho^2 - gamma drho u_x - M/2 u_x^2 - V drho
   by solving the linear equations of motion symbolically (no use of the agent's formula).
2. Partial-fraction it and compare the lower-branch f-sum share with the agent's
   F_- = (c*^2 - c_-^2)/(c_+^2 - c_-^2), c*^2 = rho_s M/(rho_n rho).
3. Plug in the agent's measured moduli; compare with its hydro json and its BdG json.
4. Compressibility sum rule; radiation-ratio scaling at fixed vertex.
"""
import json
import sympy as sp

U = "/home/claude/lbc_exploration/"

# ---------- 1. symbolic derivation
w, q = sp.symbols("omega q", positive=True)
rho, rs, rn, al, ga, M, V = sp.symbols("rho rho_s rho_n alpha gamma M V", positive=True)
dr, th, u = sp.symbols("drho theta u")
I = sp.I
# plane waves exp(i(qx - wt)):  d_t -> -i w,  d_x -> i q
# EOM from varying drho, theta, u (derived by hand from L2, see docstring):
#  drho : -theta_t - alpha drho - gamma u_x - V = 0
#  theta: drho_t + rho_s theta_xx + rho_n u_xt = 0        (two-fluid continuity)
#  u    : rho_n (u_tt - theta_xt) = gamma drho_x + M u_xx (lattice momentum)
e1 = I*w*th - al*dr - ga*I*q*u - V
e2 = -I*w*dr - rs*q**2*th + rn*q*w*u
e3 = rn*(-w**2*u - q*w*th) - (ga*I*q*dr - M*q**2*u)
sol = sp.solve([e1, e2, e3], [dr, th, u], dict=True)[0]
chi = sp.simplify((sol[dr]/V).subs(rs, rho - rn))
num, den = sp.fraction(sp.factor(chi))
print("chi numerator  :", sp.factor(num))
print("chi denominator:", sp.expand(den))
static = sp.simplify(chi.subs(w, 0))
print("static chi     :", static, " (expect -M/(alpha M - gamma^2))")

# ---------- 2. partial fractions in x = w^2/q^2
x = sp.symbols("x")
chi_x = sp.simplify(chi.subs(w, sp.sqrt(x)*q))           # = rho * (x - c*^2)/((x-c+^2)(x-c-^2)) up to sign
den_x = sp.Poly(sp.expand(sp.fraction(sp.factor(chi_x))[1]), x)
print("dispersion poly (x = w^2/q^2):", den_x.as_expr())

# ---------- 3. numbers
H = json.load(open(U + "lbc_hydro.json"))
E = H["elastic"]
f_s = E["f_s"]
vals = {rho: 1, rn: 1 - f_s, al: E["alpha_R"], ga: E["gamma"], M: E["M_R"]}
a = 1*E["alpha_R"] - 2*E["gamma"] + E["M_R"]/(1 - f_s)
b = (f_s/(1 - f_s))*(E["alpha_R"]*E["M_R"] - E["gamma"]**2)
disc = (a*a - 4*b)**0.5
cp2, cm2 = (a + disc)/2, (a - disc)/2
cs2 = f_s*E["M_R"]/(1 - f_s)
roots = sorted(float(r) for r in sp.Poly(den_x.as_expr().subs(vals), x).nroots())
print(f"\nroots of my dispersion poly: c-^2={roots[0]:.6f} c+^2={roots[1]:.6f}  | agent formula: {cm2:.6f} {cp2:.6f}")
# residues of my chi at the two poles -> f-sum shares (chi -> rho q^2 sum F/(w^2 - c^2 q^2))
chi_num = sp.lambdify(x, sp.simplify(chi_x.subs(vals).subs(q, 1)))   # chi(x) = rho * sum F/(x - c^2)
eps = 1e-7
F_minus_mine = abs(chi_num(roots[0] + eps)*eps)
F_plus_mine = abs(chi_num(roots[1] + eps)*eps)
F_minus_agent = (cs2 - cm2)/(cp2 - cm2)
print(f"F_- mine={F_minus_mine:.6f}  agent={F_minus_agent:.6f}  json={H['prediction']['F_minus']:.6f};  F_+ mine={F_plus_mine:.6f}")
c_kappa2 = E["alpha_R"] - E["gamma"]**2/E["M_R"]
print(f"compressibility sum rule: sum F/c^2 = {F_minus_agent/cm2 + (1-F_minus_agent)/cp2:.6f}  vs 1/c_kappa^2 = {1/c_kappa2:.6f}")
print(f"c_T = sqrt(mu/rho_n) = {(E['mu_R']/(1-f_s))**0.5:.4f};  Cauchy check lambda/mu = {E['Cxxyy']/E['mu_R']:.4f}")

# ---------- BdG comparison (canonical point, kf = 0.05)
R = json.load(open(U + "lbc_results.json"))
for row in R["soft_g22"]["rows"]:
    if abs(row["kf"] - 0.05) < 1e-9:
        m = row["modes"]
        print(f"BdG {row['dir']}: c2={m[0]['om']/row['q']:.4f} cT={m[1]['om']/row['q']:.4f} c1={m[2]['om']/row['q']:.4f} "
              f"F2={m[0]['fshare']:.4f} Z2/Z1={m[0]['Z']/m[2]['Z']:.4f} static2={m[0]['sshare']:.4f} "
              f"chi_static_direct={row['static_direct']:.5f} (hydro {H['prediction']['chi_static_percell']:.5f})")

# ---------- 4. radiation ratio, 3D, fixed density vertex
D3 = json.load(open(U + "lbc_3d.json"))
for r in D3["rows"]:
    if r["dir"] == "basal_GM" and abs(r["q"] - 0.15) < 1e-9:
        c2 = r["om"][0]/r["q"]; c1 = r["om"][6]/r["q"]; z21 = r["Z"][0]/r["Z"][6]
        F21 = r["fshare"][0]/r["fshare"][6]
print(f"\n3D basal: c2={c2:.4f} c1={c1:.3f} c1/c2={c1/c2:.2f} Z2/Z1={z21:.4f}")
print(f"agent's estimate (c1/c2)^5 * Z2/Z1          = {(c1/c2)**5*z21:.2e}")
# P_nu ∝ Omega * |V(q_nu)|^2 * Z_nu(q_nu) * q_nu^(d-1)/c_nu,  Z = z q,  |V|^2 ∝ q^(2l)
for l, name in ((0, "monopole"), (1, "dipole"), (2, "quadrupole")):
    print(f"fixed-vertex {name:10s} P2/P1 = (z2/z1)(c1/c2)^{2*l+4} = {z21*(c1/c2)**(2*l+4):.2e}")
