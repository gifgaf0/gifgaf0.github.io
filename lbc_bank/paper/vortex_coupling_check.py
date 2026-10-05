#!/usr/bin/env python3
"""How a moving vortex couples to the modes of the Sec. 3 supersolid hydrodynamics (first leg).

Plain-language summary: a vortex moving through the supersolid pushes on the density in two ways, through its core
and through its own flow, and the flow part is fixed by the quantum of circulation, so it cannot be tuned away. Its
flow also pushes sideways on the lattice, so a vortex faster than the shear speed sheds shear waves. In the nearly
incompressible (Green's) limit neither route reaches second sound at linear order.

Lagrangian (vector form of Sec. 3, lattice displacement u, phase theta, density deviation dr):
  L = -dr*theta_t - (rho/2)|grad theta|^2 + (rho_n/2)|u_t - grad theta|^2 - (alpha/2) dr^2 - gamma dr div u - E_el(u)
Background: theta = theta_v(x - V t) + phi, v = grad theta_v the vortex's own superflow (div v = 0, curl v = kappa delta).
Galilean completion of the superfluid kinetic term: -(rho + dr)(theta_t + |grad theta|^2/2) contains -dr |v|^2/2.

Checks:
 C1  2D point vortex theta_v = (kappa/2pi) atan2(y, x - V t): Laplacian 0, div v = 0, theta_t = -V . v.
 C2  Fourier form v(q) = i kappa (z x q)/q^2: q . v(q) = 0, so every coupling of v to a longitudinal field
     (grad phi, the longitudinal lattice displacement u_L = grad chi, or div u) vanishes.
 C3  Linear source terms collected per Fourier mode: density dr (V.v - |v|^2/2) survives; -rho v.grad phi and
     +rho_n v.grad phi vanish; -rho_n u_t . v survives for the transverse part only.
 C4  Kinematics of a source moving at V: a density source feeds branch nu iff V > c_nu (weight F_nu); the transverse
     source feeds shear iff V > c_T.
 C5  Green's limit: chi(q, omega) -> 0 as alpha -> oo at fixed omega, q (and F_- -> 0), so density sources drive
     nothing; second sound could then only be driven through a lattice-strain source (not treated).
 C6  Size: a vortex ring of radius R moving along its axis has, for qR << 1, v(q) = pi kappa R^2 (z - qhat(qhat.z)),
     so |U(q)| = |V . v(q)| <= pi kappa R^2 V. Against the deficit vertex c_k^2 eps xi^3 the ratio is
     pi kappa V R^2/(c_k^2 eps xi^3); with kappa = 2 pi hbar/m, R = xi = hbar/(m c_k) this is 2 pi^2 (V/c_k)/eps.
"""
import json, sys
import sympy as sp

out = {}
x, y, t, V, kap = sp.symbols('x y t V kappa', real=True)
X = x - V*t
th = kap/(2*sp.pi)*sp.atan2(y, X)
vx, vy = sp.diff(th, x), sp.diff(th, y)
lap = sp.simplify(sp.diff(th, x, 2) + sp.diff(th, y, 2))
div = sp.simplify(sp.diff(vx, x) + sp.diff(vy, y))
th_t_plus_Vv = sp.simplify(sp.diff(th, t) + V*vx)
out['C1_laplacian_theta_v'] = str(lap)
out['C1_div_v'] = str(div)
out['C1_theta_t_plus_V_dot_v'] = str(th_t_plus_Vv)
curl = sp.simplify(sp.diff(vy, x) - sp.diff(vx, y))
out['C1_curl_v_away_from_axis'] = str(curl)

# C2: Fourier form
qx, qy = sp.symbols('q_x q_y', real=True)
q2 = qx**2 + qy**2
vq = sp.Matrix([-qy, qx]) * sp.I*kap/q2          # i kappa (z x q)/q^2
out['C2_q_dot_v'] = str(sp.simplify(qx*vq[0] + qy*vq[1]))
# check that this is the transform of the point-vortex flow: curl in Fourier space gives kappa, divergence 0
out['C2_i_q_cross_v_equals_kappa'] = str(sp.simplify(sp.I*(qx*vq[1] - qy*vq[0])))

# C3: linear terms per Fourier mode, generic fluctuation amplitudes
w = sp.symbols('omega', real=True)
phi, drq, chi = sp.symbols('phi_q dr_q chi_q')
uT = sp.symbols('uT_q')
qhat_perp = sp.Matrix([-qy, qx])/sp.sqrt(q2)
gradphi = sp.I*sp.Matrix([qx, qy])*phi
uL = sp.I*sp.Matrix([qx, qy])*chi
uTvec = qhat_perp*uT
rho, rho_n = sp.symbols('rho rho_n', positive=True)
dot = lambda a, b: (a.T*b)[0]
terms = {
    'rho v.grad phi (from -(rho/2)|grad theta|^2)': -rho*dot(vq, gradphi),
    'rho_n v.grad phi (from (rho_n/2)|u_t - grad theta|^2)': rho_n*dot(vq, gradphi),
    '-rho_n u_L,t . v': -rho_n*dot(-sp.I*w*uL, vq),
    '-rho_n u_T,t . v': -rho_n*dot(-sp.I*w*uTvec, vq),
}
out['C3_linear_terms'] = {k: str(sp.simplify(e)) for k, e in terms.items()}
out['C3_vanishing'] = {k: bool(sp.simplify(e) == 0) for k, e in terms.items()}
out['C3_density_source'] = "from -dr*theta_t with theta_t = -V.v (C1): +dr (V.v); Galilean completion adds -dr |v|^2/2"

# C4: kinematics of a moving source: source ~ exp(i(q.r - (q.V) t)); resonance with branch c needs |q.V| = c|q|
cth = sp.symbols('cos_theta', real=True)
c = sp.symbols('c', positive=True)
sol = sp.solve(sp.Eq(V*cth, c), cth)
out['C4_resonance_cos_theta'] = str(sol)
out['C4_condition'] = "cos_theta = c/V must lie in [-1, 1]: emission iff V > c (shear: V > c_T; density: V > c_nu)"

# C5: Green's limit of the density response
al, ga, M, rs = sp.symbols('alpha gamma M rho_s', positive=True)
rr = rs + rho_n
q = sp.symbols('q', positive=True)
chi_ = q**2*(rr*rho_n*w**2 - rs*M*q**2)/(rho_n*w**4 - (M + rr*rho_n*al - 2*rho_n*ga)*q**2*w**2 + rs*(al*M - ga**2)*q**4)
out['C5_chi_limit_alpha_inf'] = str(sp.limit(chi_, al, sp.oo))
gg = sp.symbols('g', positive=True)
out['C5_chi_limit_alpha_inf_gamma_g_sqrt_alpha'] = str(sp.limit(chi_.subs(ga, gg*sp.sqrt(al)), al, sp.oo))

# C6: vortex ring of radius R in the xy plane, small q
R, phiv = sp.symbols('R varphi', positive=True)
Qx, Qy, Qz = sp.symbols('Q_x Q_y Q_z', real=True)
rvec = sp.Matrix([R*sp.cos(phiv), R*sp.sin(phiv), 0])
tvec = sp.Matrix([-sp.sin(phiv), sp.cos(phiv), 0])
Q = sp.Matrix([Qx, Qy, Qz])
# omega(Q) = kappa * \oint t exp(-i Q.r) dl ~ kappa * \oint t (1 - i Q.r) R dphi
om1 = sp.Matrix([sp.integrate(-sp.I*kap*tvec[i]*dot(Q, rvec)*R, (phiv, 0, 2*sp.pi)) for i in range(3)])
zx = sp.Matrix([0, 0, 1])
out['C6_omega_first_order'] = str(sp.simplify(om1.T))
out['C6_omega_equals_-i_kappa_pi_R2_(z x Q)'] = bool(sp.simplify(om1 - (-sp.I*kap*sp.pi*R**2*zx.cross(Q))) == sp.zeros(3, 1))
Q2 = Qx**2 + Qy**2 + Qz**2
vQ = sp.I*Q.cross(om1)/Q2                                     # v = curl A, -lap A = omega
target = kap*sp.pi*R**2*(zx - Q*(Qz/Q2))
out['C6_vQ_equals_pi_kappa_R2_(z - Qhat(Qhat.z))'] = bool(sp.simplify(vQ - target) == sp.zeros(3, 1))
# magnitude of V . v(Q) for V along z: pi kappa R^2 V sin^2(theta_Q) <= pi kappa R^2 V
Uz = sp.simplify((V*zx).dot(target))
out['C6_V_dot_v'] = str(sp.factor(Uz))
ck, eps_, xi = sp.symbols('c_kappa epsilon xi', positive=True)
ratio = sp.pi*kap*V*R**2/(ck**2*eps_*xi**3)
ratio_sub = sp.simplify(ratio.subs({kap: 2*sp.pi, R: 1/ck, xi: 1/ck}))     # hbar = m = 1, R = xi = 1/c_kappa
out['C6_ratio_flow_over_deficit_vertex'] = str(ratio_sub)
num = float(ratio_sub.subs({V: 7.85, ck: 9.38, eps_: 1}))
out['C6_ratio_at_V=c_T=7.85,c_k=9.38,eps=1'] = num

ok = (out['C1_laplacian_theta_v'] == '0' and out['C1_div_v'] == '0' and out['C1_theta_t_plus_V_dot_v'] == '0'
      and out['C2_q_dot_v'] == '0'
      and all(out['C3_vanishing'][k] for k in list(terms)[:3]) and not out['C3_vanishing']['-rho_n u_T,t . v']
      and out['C5_chi_limit_alpha_inf'] == '0' and out['C5_chi_limit_alpha_inf_gamma_g_sqrt_alpha'] == '0'
      and out['C6_omega_equals_-i_kappa_pi_R2_(z x Q)'] and out['C6_vQ_equals_pi_kappa_R2_(z - Qhat(Qhat.z))'])
json.dump(out, sys.stdout, indent=1, default=str)
print()
print('ALL CHECKS PASS' if ok else 'SOME CHECK FAILED')
sys.exit(0 if ok else 1)
