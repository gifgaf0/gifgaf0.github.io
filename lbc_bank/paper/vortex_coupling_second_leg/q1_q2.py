r"""Second-leg (blind) check, Q1 + Q2: moving 2D vortex background, linear terms.
Units hbar = m = 1.  Fourier convention f(q) = \int d^dx e^{-i q.x} f(x).
"""
import sympy as sp
import numpy as np

print("=" * 70)
print("Q1: straight vortex in d=2")
x, y, t = sp.symbols('x y t', real=True)
V, kap = sp.symbols('V kappa', positive=True)
X = x - V * t
thv = kap / (2 * sp.pi) * sp.atan2(y, X)
vx, vy = sp.diff(thv, x), sp.diff(thv, y)
print("v =", sp.simplify(vx), ",", sp.simplify(vy))
print("lap theta_v      =", sp.simplify(sp.diff(thv, x, 2) + sp.diff(thv, y, 2)))
print("div v            =", sp.simplify(sp.diff(vx, x) + sp.diff(vy, y)))
print("curl_z v (r!=0)  =", sp.simplify(sp.diff(vy, x) - sp.diff(vx, y)))
print("d_t theta_v + V.v =", sp.simplify(sp.diff(thv, t) + V * vx))
# circulation
phis = sp.symbols('varphi', real=True)
r0 = sp.symbols('r0', positive=True)
vx0 = sp.simplify(vx.subs(t, 0)); vy0 = sp.simplify(vy.subs(t, 0))
circ = sp.integrate(sp.simplify((vx0 * (-sp.sin(phis)) + vy0 * sp.cos(phis)).subs(
    {x: r0 * sp.cos(phis), y: r0 * sp.sin(phis)}) * r0), (phis, 0, 2 * sp.pi))
print("circulation      =", sp.simplify(circ))

# Fourier transform: v = zhat x grad psi, psi = (kappa/2pi) ln r ; FT[ln r] = -2pi/q^2
qx, qy = sp.symbols('q_x q_y', real=True)
q2 = qx**2 + qy**2
vq = sp.Matrix([-sp.I * kap * (-qy) / q2, -sp.I * kap * qx / q2])   # -i kappa (zhat x q)/q^2
print("v(q) = -i kappa (zhat x q)/q^2 =", list(sp.simplify(vq)))
print("q.v(q) =", sp.simplify(qx * vq[0] + qy * vq[1]))
print("i q x v(q) (z) =", sp.simplify(sp.I * (qx * vq[1] - qy * vq[0])), "(= kappa: point vorticity)")
print("moving: v(q,t) = v(q) exp(-i q.V t)  ->  source frequency omega = q.V")

# brute-force numerical FT with Gaussian window (window correction ~exp(-q^2 Rw^2/4), negligible)
def vortex_ft_numeric(qv, kappa=2 * np.pi, Rw=20.0, half=75.0, h=0.03):
    n = int(2 * half / h)
    xs = -half + (np.arange(n) + 0.5) * h          # offset grid avoids r = 0
    acc = np.zeros(2, dtype=complex)
    for i0 in range(0, n, 400):
        xx = xs[i0:i0 + 400][:, None]
        yy = xs[None, :]
        r2 = xx**2 + yy**2
        w = np.exp(-r2 / Rw**2) * np.exp(-1j * (qv[0] * xx + qv[1] * yy))
        fx = kappa / (2 * np.pi) * (-yy) / r2
        fy = kappa / (2 * np.pi) * (xx) / r2
        acc[0] += np.sum(fx * w); acc[1] += np.sum(fy * w)
    return acc * h * h

for qv in [(0.7, 0.4), (-1.1, 0.9)]:
    num = vortex_ft_numeric(qv)
    qq = qv[0]**2 + qv[1]**2
    ana = np.array([-1j * 2 * np.pi * (-qv[1]) / qq, -1j * 2 * np.pi * qv[0] / qq])
    print(f"  q={qv}: numeric v(q)={np.round(num, 5)}  analytic={np.round(ana, 5)}  "
          f"q.v_num={np.round(qv[0] * num[0] + qv[1] * num[1], 5)}")

print("=" * 70)
print("Q2: expansion to first order in fluctuations (with Galilean completion)")
eps = sp.symbols('epsilon')
rs, rn, al, ga, lam, mu = sp.symbols('rho_s rho_n alpha gamma lambda mu', positive=True)
rho = rs + rn
Th = sp.Function('Theta')(t, x, y)            # background vortex phase (generic)
phi = sp.Function('phi')(t, x, y)
dr = sp.Function('drho')(t, x, y)
ux = sp.Function('u_x')(t, x, y)
uy = sp.Function('u_y')(t, x, y)
U = sp.Function('U')(t, x, y)

theta = Th + eps * phi
D = eps * dr
u = (eps * ux, eps * uy)
dtth = sp.diff(theta, t)
gx, gy = sp.diff(theta, x), sp.diff(theta, y)
uxx, uyy = sp.diff(u[0], x), sp.diff(u[1], y)
uxy = (sp.diff(u[0], y) + sp.diff(u[1], x)) / 2
Eel = lam / 2 * (uxx + uyy)**2 + mu * (uxx**2 + uyy**2 + 2 * uxy**2)
kin_n = rn / 2 * ((sp.diff(u[0], t) - gx)**2 + (sp.diff(u[1], t) - gy)**2)
rest = kin_n - al / 2 * D**2 - ga * D * (uxx + uyy) - Eel - U * D

L_given = -D * dtth - rho / 2 * (gx**2 + gy**2) + rest                     # quadratic L as given
L_comp = -(rho + D) * (dtth + (gx**2 + gy**2) / 2) + rest                  # Galilean completion

vxs, vys, Vs = sp.symbols('v_x v_y V')
def lin(L):
    L1 = sp.expand(sp.diff(L, eps).subs(eps, 0))
    # background moves rigidly: d_t Theta = -V d_x Theta (V along x)
    L1 = L1.subs(sp.Derivative(Th, t), -V * sp.Derivative(Th, x))
    L1 = L1.subs({sp.Derivative(Th, x): vxs, sp.Derivative(Th, y): vys})
    return sp.collect(sp.expand(L1), [dr, sp.Derivative(phi, x), sp.Derivative(phi, y),
                                      sp.Derivative(phi, t), sp.Derivative(ux, t), sp.Derivative(uy, t)])
L1g = lin(L_given)
L1c = lin(L_comp)
print("linear terms, given quadratic L :\n   ", L1g)
print("linear terms, Galilean-completed:\n   ", L1c)
print("completed - given:", sp.simplify(L1c - L1g))
# check the quadratic background-dependent cross terms introduced by completion
L2c = sp.expand(sp.diff(L_comp, eps, 2).subs(eps, 0) / 2)
L2g = sp.expand(sp.diff(L_given, eps, 2).subs(eps, 0) / 2)
dq = sp.expand(L2c - L2g)
dq = dq.subs(sp.Derivative(Th, t), -V * sp.Derivative(Th, x)).subs(
    {sp.Derivative(Th, x): vxs, sp.Derivative(Th, y): vys})
print("extra QUADRATIC terms from completion:", sp.factor(dq))

# group by field
coef_drho = sp.simplify(L1c.coeff(dr))
print("coefficient of drho :", coef_drho, "   [= V.v - |v|^2/2 - U]")
cphi = [sp.simplify(L1c.coeff(sp.Derivative(phi, s))) for s in (x, y, t)]
print("coeffs of (phi_x, phi_y, phi_t):", cphi, "  -> -rho_s v.grad(phi) - rho d_t phi")
cu = [sp.simplify(L1c.coeff(sp.Derivative(w, t))) for w in (ux, uy)]
print("coeffs of (d_t u_x, d_t u_y):", cu, "  -> -rho_n v.d_t u")

# numerical spatial integrals with the actual 2D vortex (kappa=2pi) and smooth test functions
print("-- spatial integrals with test fields (vortex at origin, V = x-hat) --")
h = 0.01; half = 12.0
xs = -half + (np.arange(int(2 * half / h)) + 0.5) * h
XX, YY = np.meshgrid(xs, xs, indexing='ij')
R2 = XX**2 + YY**2
vX = -YY / R2; vY = XX / R2                              # kappa/2pi = 1
a = (1.3, -0.7); s = 0.8
G = np.exp(-((XX - a[0])**2 + (YY - a[1])**2) / s**2)
Gx = -2 * (XX - a[0]) / s**2 * G; Gy = -2 * (YY - a[1]) / s**2 * G
I_phi = np.sum(vX * Gx + vY * Gy) * h * h               # int v.grad(phi), phi = G
I_uL = I_phi                                             # u_L = grad(chi), chi = G : same integral
I_uT = np.sum(vX * (-Gy) + vY * (Gx)) * h * h           # u_T = zhat x grad(psi), psi = G
I_drho = np.sum(vX * G) * h * h                          # int (V.v) drho, V = x-hat, drho = G
B = 0.5 * (vX**2 + vY**2)
I_bern = np.sum(B * G) * h * h
print(f"  int v.grad(phi)       = {I_phi:+.2e}   (vanishes: div v = 0)")
print(f"  int v.d_t u_L (shape) = {I_uL:+.2e}   (vanishes: v transverse)")
print(f"  int v.u_T (shape)     = {I_uT:+.4f}   (survives)")
print(f"  int (V.v) drho        = {I_drho:+.4f}   (survives)")
print(f"  int |v|^2/2 drho      = {I_bern:+.4f}   (survives)")
