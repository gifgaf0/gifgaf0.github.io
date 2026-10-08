#!/usr/bin/env python3
"""A1 polarization gate -- first leg (chat leg) derivation.

Locked pre-registration: A1_PREREG.md, md5 d5f6aa3bd50743c5d69e54338494bb27.
Conventions: exactly those fixed in the second-leg dispatch (recorded in A1_DERIVATION.md):
  k(th,ph) = (sin th cos ph, sin th sin ph, cos th); m = dk/dth; n = (-sin ph, cos ph, 0)
  p = cos psi m + sin psi n;  q = -sin psi m + cos psi n
  e_+ = pp - qq, e_cross = pq + qp, e_x = pk + kp, e_y = qk + kq, e_b = pp + qq, e_l = sqrt2 kk
  D = (xx - yy)/2,  F_A = D:e_A.
Symbolic identities are checked exactly with the half-angle (Weierstrass) rational parametrization
cos a = (1 - t^2)/(1 + t^2), sin a = 2t/(1 + t^2): every trigonometric identity below becomes a
rational-function identity, decided by sympy.cancel.

Sections (run in this order; the comparison numbers enter only in section V, run last):
  K   kinematics: the TT projection of sym(k (x) a) vanishes identically
  H   helicity decomposition of sym(k (x) a) on the six-tensor basis
  A   antenna mapping (closed forms), common-grid JSON, psi spin-weight Fourier test + controls
  D   the substrate's own detector: mirror motion + probe transit time (acoustoelastic) -> G:eps
  I   inventory: what the substrate's field content allows at linear order
  B   bounded admixtures (texture, detector motion, second order)
  S1  binary radiation, structural: dipole condition, E2 vector vs tensor power, axis selection rule
  S2  pulsar timing: Earth-term overlap reduction functions (HD, vector, breathing)
  V   verdict inputs (quarantined, last)
"""
import json, hashlib, math
import numpy as np
import sympy as sp
from scipy import integrate

OUT, CHECKS = {}, []

def check(name, ok, detail=""):
    CHECKS.append((name, bool(ok), detail))
    print(("PASS " if ok else "FAIL ") + name + ("  [" + detail + "]" if detail else ""), flush=True)
    if not ok:
        raise SystemExit("check failed: " + name)

def md5(path):
    return hashlib.md5(open(path, "rb").read()).hexdigest()

check("prereg md5 matches the lock", md5("A1_PREREG.md") == "d5f6aa3bd50743c5d69e54338494bb27", md5("A1_PREREG.md"))

# ---------------------------------------------------------------- exact rational frame
T, U, V, W, L = sp.symbols("T U V W lambda", real=True)       # tan(theta/2), tan(phi/2), tan(psi/2), tan(chi/2)
cs = lambda t: ((1 - t**2)/(1 + t**2), 2*t/(1 + t**2))
cth, sth = cs(T); cph, sph = cs(U); cps, sps = cs(V); cch, sch = cs(W)
k = sp.Matrix([sth*cph, sth*sph, cth])
m = sp.Matrix([cth*cph, cth*sph, -sth])
nv = sp.Matrix([-sph, cph, 0])
p = cps*m + sps*nv
q = -sps*m + cps*nv
outer = lambda u, v: u*v.T
ddot = lambda A, B: sum(A[i, j]*B[i, j] for i in range(3) for j in range(3))
zero = lambda e: sp.cancel(sp.together(e)) == 0
allzero = lambda M: all(zero(v) for v in M)
I3 = sp.eye(3)
E = {"plus": outer(p, p) - outer(q, q), "cross": outer(p, q) + outer(q, p), "x": outer(p, k) + outer(k, p),
     "y": outer(q, k) + outer(k, q), "b": outer(p, p) + outer(q, q), "l": sp.sqrt(2)*outer(k, k)}
ORDER = ["plus", "cross", "x", "y", "b", "l"]
D = sp.diag(sp.Rational(1, 2), -sp.Rational(1, 2), 0)
check("frame: (m, n, k) orthonormal and right-handed", allzero(sp.Matrix([m.dot(m) - 1, nv.dot(nv) - 1, k.dot(k) - 1,
      m.dot(nv), m.dot(k), nv.dot(k)])) and allzero(m.cross(nv) - k))

# ---------------------------------------------------------------- K: kinematics
print("\n== K: kinematics ==", flush=True)
a1, a2, a3 = sp.symbols("a1 a2 a3", real=True)
a = sp.Matrix([a1, a2, a3])
eps = (outer(k, a) + outer(a, k))/2
P = I3 - outer(k, k)
TT = P*eps*P - sp.Rational(1, 2)*P*(P*eps).trace()
check("K1 Lambda(k) sym(k (x) a) == 0 identically (all k, all a)", allzero(TT))
check("K2 reason: P k == 0 and tr(P eps) == 0", allzero(P*k) and zero((P*eps).trace()))

# ---------------------------------------------------------------- H: helicity decomposition
print("\n== H: helicity decomposition ==", flush=True)
G = sp.Matrix(6, 6, lambda i, j: sp.cancel(ddot(E[ORDER[i]], E[ORDER[j]])))
check("H1 basis Gram matrix == 2*I6", allzero(G - 2*sp.eye(6)))
aG = cch*p + sch*q + L*k                                  # a = cos(chi) p + sin(chi) q + lambda k
epsG = (outer(k, aG) + outer(aG, k))/2
c = {A: sp.cancel(ddot(epsG, E[A])/2) for A in ORDER}
check("H2 c_plus == c_cross == c_b == 0", zero(c["plus"]) and zero(c["cross"]) and zero(c["b"]))
check("H3 c_x == cos(chi)/2, c_y == sin(chi)/2", zero(c["x"] - cch/2) and zero(c["y"] - sch/2))
check("H4 c_l == lambda/sqrt2", zero(c["l"] - L/sp.sqrt(2)))
check("H5 eps == sum_A c_A e_A", allzero(sum((c[A]*E[A] for A in ORDER), sp.zeros(3, 3)) - epsG))
cs_sum = ((1 - (V + W)**2/(1 - V*W)**2)/(1 + (V + W)**2/(1 - V*W)**2), 2*((V + W)/(1 - V*W))/(1 + (V + W)**2/(1 - V*W)**2))
p_sum = cs_sum[0]*m + cs_sum[1]*nv                         # p at angle psi + chi (tan addition formula)
check("H6 cos(chi) p(psi) + sin(chi) q(psi) == p(psi + chi): the physical polarization angle is psi + chi",
      allzero(cch*p + sch*q - p_sum))
OUT["H_coefficients"] = {"c_plus": 0, "c_cross": 0, "c_x": "cos(chi)/2", "c_y": "sin(chi)/2", "c_b": 0, "c_l": "lambda/sqrt(2)"}

# ---------------------------------------------------------------- A: antenna mapping
print("\n== A: antenna mapping ==", flush=True)
F = {A: sp.cancel(ddot(D, E[A])) for A in ORDER}
c2t, s2t = cth**2 - sth**2, 2*sth*cth
c2p, s2p = cph**2 - sph**2, 2*sph*cph
c2s, s2s = cps**2 - sps**2, 2*sps*cps
expected = {
    "plus":  sp.Rational(1, 2)*(1 + cth**2)*c2p*c2s - cth*s2p*s2s,
    "cross": -sp.Rational(1, 2)*(1 + cth**2)*c2p*s2s - cth*s2p*c2s,
    "x":     sth*(cth*c2p*cps - s2p*sps),
    "y":     -sth*(cth*c2p*sps + s2p*cps),
    "b":     -sp.Rational(1, 2)*sth**2*c2p,
    "l":     sp.sqrt(2)/2*sth**2*c2p,
}
for A in ORDER:
    check("A1 F_%s closed form" % A, zero(F[A] - expected[A]))
OUT["A_patterns"] = {
    "F_plus": "(1+cos^2 th)/2 cos2ph cos2psi - cos th sin2ph sin2psi",
    "F_cross": "-(1+cos^2 th)/2 cos2ph sin2psi - cos th sin2ph cos2psi",
    "F_x": "sin th (cos th cos2ph cos psi - sin2ph sin psi)",
    "F_y": "-sin th (cos th cos2ph sin psi + sin2ph cos psi)",
    "F_b": "-(1/2) sin^2 th cos2ph", "F_l": "(sqrt2/2) sin^2 th cos2ph = -sqrt2 F_b"}
RT = sp.cancel(ddot(D, epsG.subs(L, 0)))
RL = sp.cancel(ddot(D, outer(k, k)))
check("A2 R(transverse) == (cos chi F_x + sin chi F_y)/2", zero(RT - (cch*F["x"] + sch*F["y"])/2))
check("A3 R(transverse) == (1/2) sin th [cos th cos2ph cos(psi+chi) - sin2ph sin(psi+chi)]",
      zero(RT - sp.Rational(1, 2)*sth*(cth*c2p*cs_sum[0] - s2p*cs_sum[1])))
check("A4 R(longitudinal) == F_l/sqrt2 == (1/2) sin^2 th cos2ph", zero(RL - F["l"]/sp.sqrt(2)) and zero(RL - sth**2*c2p/2))
check("A5 F_l == -sqrt2 F_b (breathing and longitudinal patterns degenerate for an L-shaped detector)",
      zero(F["l"] + sp.sqrt(2)*F["b"]))

# numerics on the common grid (identical grid to the second-leg dispatch)
def frame(t, f, s):
    kk = np.array([math.sin(t)*math.cos(f), math.sin(t)*math.sin(f), math.cos(t)])
    mm = np.array([math.cos(t)*math.cos(f), math.cos(t)*math.sin(f), -math.sin(t)])
    nn = np.array([-math.sin(f), math.cos(f), 0.0])
    return kk, math.cos(s)*mm + math.sin(s)*nn, -math.sin(s)*mm + math.cos(s)*nn
def basis(kk, pp, qq):
    o = np.outer
    return {"plus": o(pp, pp) - o(qq, qq), "cross": o(pp, qq) + o(qq, pp), "x": o(pp, kk) + o(kk, pp),
            "y": o(qq, kk) + o(kk, qq), "b": o(pp, pp) + o(qq, qq), "l": math.sqrt(2)*o(kk, kk)}
Dn = np.diag([0.5, -0.5, 0.0])
TH = [0.3, 0.9, 1.5, 2.2, 2.9]; PH = [0.0, 0.7, 2.1, 4.0]; PS = [0.0, 0.4, 1.1]; CH = [0.0, 0.5, 1.3]
grid = {"transverse": [], "longitudinal": []}
worst_tensor = 0.0
for t in TH:
    for f in PH:
        for s in PS:
            kk, pp, qq = frame(t, f, s)
            Eb = basis(kk, pp, qq)
            for x in CH:
                av = math.cos(x)*pp + math.sin(x)*qq
                ep = 0.5*(np.outer(kk, av) + np.outer(av, kk))
                cc = {A: float(np.sum(ep*Eb[A]))/2 for A in ORDER}
                worst_tensor = max(worst_tensor, abs(cc["plus"]), abs(cc["cross"]))
                grid["transverse"].append({"theta": t, "phi": f, "psi": s, "chi": x, "c_plus": cc["plus"],
                    "c_cross": cc["cross"], "c_x": cc["x"], "c_y": cc["y"], "c_b": cc["b"], "c_l": cc["l"],
                    "R": float(np.sum(Dn*ep))})
            ep = np.outer(kk, kk)
            cc = {A: float(np.sum(ep*Eb[A]))/2 for A in ORDER}
            grid["longitudinal"].append({"theta": t, "phi": f, "psi": s, "c_plus": cc["plus"], "c_cross": cc["cross"],
                "c_x": cc["x"], "c_y": cc["y"], "c_b": cc["b"], "c_l": cc["l"], "R": float(np.sum(Dn*ep))})
json.dump(grid, open("leg1_grid.json", "w"), indent=1)
check("A6 grid: max |c_plus|, |c_cross| over the transverse grid <= 1e-15", worst_tensor <= 1e-15, "%.1e" % worst_tensor)

# psi spin-weight Fourier test, with controls
rng = np.random.default_rng(20261007)
def harmonics(fun, N=64):
    s = np.arange(N)*2*math.pi/N
    Fh = np.fft.rfft(np.array([fun(x) for x in s]))/N
    return np.array([abs(Fh[j]) for j in range(5)])
def resp(kind, t, f, s):
    kk, pp, qq = frame(t, f, s)
    ep = {"transverse": 0.5*(np.outer(kk, pp) + np.outer(pp, kk)), "longitudinal": np.outer(kk, kk),
          "tensor_control": np.outer(pp, pp) - np.outer(qq, qq), "breathing_control": np.outer(pp, pp) + np.outer(qq, qq)}[kind]
    return float(np.sum(Dn*ep))
sky = [(math.acos(rng.uniform(-1, 1)), rng.uniform(0, 2*math.pi)) for _ in range(40)]
sw = {}
for kind in ["transverse", "longitudinal", "tensor_control", "breathing_control"]:
    agg = np.zeros(5)
    for (t, f) in sky:
        agg = np.maximum(agg, harmonics(lambda s: resp(kind, t, f, s)))
    sw[kind] = [float(v) for v in agg]
    print("   %-18s max |harmonic m|, m = 0..4: %s" % (kind, ", ".join("%.1e" % v for v in agg)))
OUT["A_spin_weight_max_harmonics_m0_to_m4"] = sw
only = lambda h, keep, tol: h[keep] > 1e-3 and max(h[j] for j in range(5) if j != keep) <= tol
check("A7 transverse (S2): only |m| = 1", only(sw["transverse"], 1, 1e-15))
check("A8 longitudinal: only m = 0", only(sw["longitudinal"], 0, 1e-15))
check("A9 control: tensor wave shows only |m| = 2", only(sw["tensor_control"], 2, 1e-15))
check("A10 control: breathing wave shows only m = 0", only(sw["breathing_control"], 0, 1e-15))
Gr = rng.normal(size=(3, 3, 3, 3))                         # an arbitrary anisotropic linear response map
def resp_aniso(t, f, s):
    kk, pp, qq = frame(t, f, s)
    Ge = np.einsum("ijkl,kl->ij", Gr, 0.5*(np.outer(kk, pp) + np.outer(pp, kk)))
    return float(np.sum(Dn*0.5*(Ge + Ge.T)))
agg = np.zeros(5)
for (t, f) in sky:
    agg = np.maximum(agg, harmonics(lambda s: resp_aniso(t, f, s)))
OUT["A_random_anisotropic_map_max_harmonics"] = [float(v) for v in agg]
check("A11 arbitrary anisotropic response map: S2 still shows only |m| = 1", only(agg, 1, 1e-14),
      ", ".join("%.1e" % v for v in agg))

# ---------------------------------------------------------------- D: the substrate's own detector
print("\n== D: the substrate's own detector ==", flush=True)
# S2 wave in the untextured aggregate: u = a f(t - k.x/c_T), a perpendicular to k; strain eps = sym(k (x) a)(-f'/c_T).
# Mirrors: X = B u at long wavelength, B = beta*1 + betaL*kk (any linear, rotation-covariant response of the
# mirror to the local wave fields in the isotropic aggregate; complex, frequency-dependent coefficients allowed).
# The knot-lattice vertex of record, -rho_n udot.v_s (second-sound paper Sec. 6, derived twice), is of this form.
# Probe ("light") = short-wavelength transverse phonon of the same medium (CI-W/EM-IN). In material
# coordinates its speed in the homogeneously strained isotropic aggregate is
#   W = c_T [1 + (al1 tr eps + al2 N.eps.N + al3 P.eps.P)/2]
# (the most general isotropic linear form, even in the probe polarization P; objectivity removes rotations).
# Round trip: T = 2 L_mat / W  =>  dT/T = dL_mat/L - dW/W.
beta, betaL, al1, al2, al3 = sp.symbols("beta beta_L alpha1 alpha2 alpha3", real=True)
xh, yh, zh = sp.Matrix([1, 0, 0]), sp.Matrix([0, 1, 0]), sp.Matrix([0, 0, 1])
def transit(nvec, pvec, avec):
    B = beta*I3 + betaL*outer(k, k)
    ew = (outer(k, avec) + outer(avec, k))/2
    eX = (outer(k, B*avec) + outer(B*avec, k))/2
    return (nvec.T*(eX - ew)*nvec)[0] - (al1*ew.trace() + al2*(nvec.T*ew*nvec)[0] + al3*(pvec.T*ew*pvec)[0])/2
def diff_signal(config, avec):
    (n1, p1), (n2, p2) = ((xh, zh), (yh, zh)) if config == "vertical" else ((xh, yh), (yh, xh))
    return transit(n1, p1, avec) - transit(n2, p2, avec)
aT0 = cch*p + sch*q
RT0 = ddot(D, (outer(k, aT0) + outer(aT0, k))/2)
gain = {"transverse_vertical": 2*(beta - 1 - al2/2), "transverse_horizontal": 2*(beta - 1 - al2/2 + al3/2),
        "longitudinal_vertical": 2*(beta + betaL - 1 - al2/2), "longitudinal_horizontal": 2*(beta + betaL - 1 - al2/2 + al3/2)}
check("D1 S2 wave, same (vertical) probe polarization in both arms: S == 2(beta-1-al2/2) D:eps",
      zero(diff_signal("vertical", aT0) - gain["transverse_vertical"]*RT0))
check("D2 S2 wave, probe polarization perpendicular to each arm: S == 2(beta-1-al2/2+al3/2) D:eps",
      zero(diff_signal("horizontal", aT0) - gain["transverse_horizontal"]*RT0))
check("D3 longitudinal wave, vertical probe: S == 2(beta+betaL-1-al2/2) D:kk",
      zero(diff_signal("vertical", k) - gain["longitudinal_vertical"]*RL))
check("D4 longitudinal wave, perpendicular probe: S == 2(beta+betaL-1-al2/2+al3/2) D:kk",
      zero(diff_signal("horizontal", k) - gain["longitudinal_horizontal"]*RL))
OUT["D_detector_gain"] = {kk_: str(vv) for kk_, vv in gain.items()}
# => the substrate's interferometer reads S2 as kappa (cos chi F_x + sin chi F_y)/2: the standard vector patterns.

# ---------------------------------------------------------------- I: inventory
print("\n== I: inventory ==", flush=True)
# Field content of record (G-2a-A1 Phase 0): psi in C (x) O = 16 real fields, spatial scalars, with the spatial-internal
# direct product (F-A1-1 silent: no spin-orbit-type locking); in the crystal, one spatial vector field u.
# In an isotropic medium linear modes carry definite helicity: scalars give h = 0, a vector gives h = 0, +-1.
# Helicity +-2 needs a propagating field with two spatial indices; the field content has none.  An internal plane
# wave dpsi_b f(t - k.x/c) carries no polarization vector, so any linear detector functional of it is psi-free:
dpsi = sp.symbols("dpsi0:16", real=True); gco = sp.symbols("g0:16", real=True)
lin = sum(g_*d_ for g_, d_ in zip(gco, dpsi))*sth**2*c2p          # any detector-geometry factor
check("I1 internal (scalar) waves: linear response independent of the polarization angle (m = 0 only)", sp.diff(lin, V) == 0)
OUT["I_inventory"] = "16 spatial scalars (h=0) + one vector u (h=0,+-1); no rank-2 propagating field; agrees with K = empty (G-CI1)"

# ---------------------------------------------------------------- B: bounded admixtures
print("\n== B: bounded admixtures ==", flush=True)
t_max = 1.2355e-6                      # G-MSCS-A (V4.87) sigma-union on the l = 4 texture strength; hex l = 2 <= 6.46e-7
v_c = 369.82e3/299792458.0             # solar-system speed relative to the CMB frame (assumed substrate rest frame)
def tt_fraction_motion(kap, vc, N=20000):
    vhat = np.array([0.3, -0.5, 0.81]); vhat /= np.linalg.norm(vhat)
    num = den = 0.0
    for _ in range(N):
        t = math.acos(rng.uniform(-1, 1)); f = rng.uniform(0, 2*math.pi); s0 = rng.uniform(0, 2*math.pi)
        kk, pp, qq = frame(t, f, s0)
        Ge = 0.5*(np.outer(kk, pp) + np.outer(pp, kk)) + kap*vc*0.5*(np.outer(vhat, pp) + np.outer(pp, vhat))
        Pk = np.eye(3) - np.outer(kk, kk)
        TTp = Pk @ Ge @ Pk - 0.5*Pk*np.trace(Pk @ Ge)
        num += np.sum(TTp*TTp); den += np.sum(Ge*Ge)
    return num/den
fT = tt_fraction_motion(1.0, v_c)
OUT["B_bounds"] = {"texture_strength_max": t_max, "v_over_c": v_c, "motion_TT_power_fraction_toy": fT,
                   "motion_TT_power_fraction_over_vc2": fT/v_c**2, "second_order_relative_amplitude": 1e-21}
print("   texture <= %.2e (amplitude order); motion v/c = %.3e; toy TT power fraction %.2e = %.2f (v/c)^2" % (t_max, v_c, fT, fT/v_c**2))
check("B1 motion-induced TT power fraction (Lambda reading only) is O((v/c)^2), < 1e-5", fT < 1e-5)

# ---------------------------------------------------------------- S1: binary radiation (structural)
print("\n== S1: binary radiation (structural) ==", flush=True)
# exact sphere averages of degree <= 8 polynomials: Gauss-Legendre (8 nodes) x uniform (16 nodes) is exact to degree 15
xg, wg = np.polynomial.legendre.leggauss(8)
nodes = [(ct, 2*math.pi*j/16) for ct in xg for j in range(16)]
wts = [w*(2*math.pi/16) for w in wg for j in range(16)]
def sph(fun):
    return sum(w*fun(np.array([math.sqrt(1 - ct**2)*math.cos(f), math.sqrt(1 - ct**2)*math.sin(f), ct])) for (ct, f), w in zip(nodes, wts))
ratios_v, ratios_t = [], []
for _ in range(6):
    Qr = rng.normal(size=(3, 3)); Qr = 0.5*(Qr + Qr.T); Qr -= np.eye(3)*np.trace(Qr)/3
    QQ = float(np.sum(Qr*Qr))
    def vec(n_):
        Pn = np.eye(3) - np.outer(n_, n_); v_ = Pn @ (Qr @ n_); return float(v_ @ v_)
    def ten(n_):
        Pn = np.eye(3) - np.outer(n_, n_); Tt = Pn @ Qr @ Pn - 0.5*Pn*np.trace(Pn @ Qr); return float(np.sum(Tt*Tt))
    ratios_v.append(sph(vec)/QQ); ratios_t.append(sph(ten)/QQ)
check("S1a integral |P_perp Q n|^2 dOmega == (4 pi/5) Q:Q (vector E2 angular integral)",
      max(abs(r - 4*math.pi/5) for r in ratios_v) < 1e-12)
check("S1b integral Lambda(n):(Q Q) dOmega == (8 pi/5) Q:Q (tensor angular integral)",
      max(abs(r - 8*math.pi/5) for r in ratios_t) < 1e-12)
# Prefactors (Landau & Lifshitz Vol. 2): vector E2, Gaussian units, D_ab = 3 Qbar_ab (charge-weighted):
#   dI/dOmega = |D''' x n|^2/(144 pi c^5)  ->  I = D'''^2/(180 c^5) = Qbar'''^2/(20 c^5);
# GR: dP/dOmega = (G/8 pi c^5) Lambda:I'''I'''  ->  P = G I'''^2/(5 c^5).  With charge q = sqrt(G) m (a vector channel
# whose static force has Newton's magnitude):
ratio = (9.0/(144*math.pi)*(4*math.pi/5))/((1.0/(8*math.pi))*(8*math.pi/5))
OUT["S1_E2_vector_over_GR_power_same_static_strength"] = ratio
print("   P(vector E2) / P(GR quadrupole) at equal static strength = %.6f" % ratio)
check("S1c the ratio is exactly 1/4", abs(ratio - 0.25) < 1e-15)
w = sp.symbols("w", real=True)
Qb = sp.Matrix([[sp.cos(w), sp.sin(w), 0], [sp.sin(w), -sp.cos(w), 0], [0, 0, 0]])   # binary in the xy-plane, 2 Omega t = w
Pz = I3 - outer(zh, zh)
check("S1d vector E2 emission along the orbital axis vanishes (J_z = +-2 cannot leave as helicity +-1)", all(sp.simplify(v) == 0 for v in Pz*(Qb*zh)))
TTz = Pz*Qb*Pz - sp.Rational(1, 2)*Pz*(Pz*Qb).trace()
check("S1e GR emission along the orbital axis is maximal (TT norm^2 = 2, nonzero)", sp.simplify(ddot(TTz, TTz)) == 2)
g1, g2, m1, m2 = sp.symbols("g1 g2 m1 m2", positive=True)
rv = sp.Matrix(sp.symbols("r1 r2 r3", real=True))
dip = g1*m1*(m2/(m1 + m2))*rv + g2*m2*(-m1/(m1 + m2))*rv
check("S1f binary dipole = (g1 - g2) m1 m2/(m1+m2) r: absent iff the charge-to-mass ratio is universal",
      all(sp.simplify(v) == 0 for v in dip - (g1 - g2)*m1*m2/(m1 + m2)*rv))

# ---------------------------------------------------------------- S2: pulsar timing ORFs
print("\n== S2: pulsar-timing overlap reduction functions (Earth term) ==", flush=True)
def orf(kind, xi):
    p1 = np.array([0.0, 0.0, 1.0]); p2 = np.array([math.sin(xi), 0.0, math.cos(xi)])
    def integrand(f, ct):
        st = math.sqrt(max(0.0, 1 - ct*ct))
        kk = np.array([st*math.cos(f), st*math.sin(f), ct])
        mm = np.array([ct*math.cos(f), ct*math.sin(f), -st]); nn_ = np.array([-math.sin(f), math.cos(f), 0.0])
        pols = {"tensor": [np.outer(mm, mm) - np.outer(nn_, nn_), np.outer(mm, nn_) + np.outer(nn_, mm)],
                "vector": [np.outer(mm, kk) + np.outer(kk, mm), np.outer(nn_, kk) + np.outer(kk, nn_)],
                "breathing": [np.outer(mm, mm) + np.outer(nn_, nn_)]}[kind]
        tot = 0.0
        for e in pols:
            tot += (0.5*(p1 @ e @ p1)/(1.0 + kk @ p1))*(0.5*(p2 @ e @ p2)/(1.0 + kk @ p2))
        return tot
    # integrable singularities where k = -p1 (ct = -1) and k = -p2 (ct = -cos xi, f = pi)
    val, err = integrate.nquad(integrand, [[0.0, 2*math.pi], [-1.0, 1.0]],
                               opts=[{"points": [math.pi], "limit": 400, "epsabs": 1e-12, "epsrel": 1e-11},
                                     {"points": [-math.cos(xi)], "limit": 400, "epsabs": 1e-11, "epsrel": 1e-10}])
    return 3.0/(8*math.pi)*val
def hd(xi):
    x = (1 - math.cos(xi))/2
    return 0.5 - 0.25*x + 1.5*x*math.log(x)
tab = []
for xi in [0.35, 0.7, 1.0, 1.4, 1.8, 2.2, 2.6, 3.0]:
    row = {"xi": xi, "tensor": orf("tensor", xi), "HD_closed": hd(xi), "vector": orf("vector", xi),
           "breathing": orf("breathing", xi), "breathing_closed": (3 + math.cos(xi))/8}
    tab.append(row)
    print("   xi=%.2f  tensor %.8f (HD %.8f)  vector %.8f  breathing %.8f (closed %.8f)" %
          (xi, row["tensor"], row["HD_closed"], row["vector"], row["breathing"], row["breathing_closed"]), flush=True)
OUT["S2_orf_table"] = tab
check("S2a tensor ORF == Hellings-Downs closed form (<= 1e-7)", max(abs(r["tensor"] - r["HD_closed"]) for r in tab) <= 1e-7)
check("S2b breathing ORF == (3 + cos xi)/8 (<= 1e-7)", max(abs(r["breathing"] - r["breathing_closed"]) for r in tab) <= 1e-7)
bV = np.array([3*math.log(2/(1 - math.cos(r["xi"]))) - 4*math.cos(r["xi"]) - 3 for r in tab])
vals = np.array([r["vector"] for r in tab])
Afit = float(bV @ vals/(bV @ bV)); resid = float(np.max(np.abs(vals - Afit*bV)))
OUT["S2_vector_fit"] = {"A": Afit, "max_resid": resid, "A_rational": str(sp.nsimplify(Afit, tolerance=1e-7, rational=True))}
print("   vector ORF = A [3 ln(2/(1 - cos xi)) - 4 cos xi - 3], A = %.9f (~ %s), max residual %.1e" % (Afit, OUT["S2_vector_fit"]["A_rational"], resid))
check("S2c vector ORF has the closed form A [3 ln(2/(1-cos xi)) - 4 cos xi - 3] (residual <= 1e-7)", resid <= 1e-7)

# ---------------------------------------------------------------- V: verdict inputs (quarantined, last)
print("\n== V: verdict inputs (quarantined; comparison numbers enter here only) ==", flush=True)
# R-2. Gapless branch speeds of the instantiated substrate, from the ledger's two-leg record (V4.90 bracket on Sec. 2.91.V):
# 3D AB/hcp: second sound 0.471; shear 7.75-8.04 (direction- and polarization-dependent); first sound 16.1-17.0.
ratios = {"c2/cT": (0.471/8.04, 0.471/7.75), "c1/cT": (16.1/8.04, 17.0/7.75)}
OUT["V_branch_speed_ratios_3D"] = ratios
off = min(abs(ratios["c2/cT"][1] - 1), abs(ratios["c1/cT"][0] - 1))
print("   3D c2/cT = %.3f-%.3f, c1/cT = %.3f-%.3f" % (ratios["c2/cT"] + ratios["c1/cT"]))
# GW170817 / GRB 170817A: -3e-15 <= (v_GW - v_EM)/v_EM <= +7e-16 (ApJL 848, L13 (2017)).
check("V1 R-2: no helicity-0 branch lies on the c_T cone (closest |c/cT - 1| >> 1e-15)", off > 1e-2, "%.3f" % off)
OUT["V_anchors"] = {"GW170817_log10BF_tensor_over_vector": "20.81 +- 0.08", "GW170817_log10BF_tensor_over_scalar": "23.09 +- 0.08",
                    "GW170814_BF_tensor_over_vector": "> 200", "GW170814_BF_tensor_over_scalar": "> 1000",
                    "Takeda2021_lnB_tensor_over_vector_GW170817": "21.078 (51.043 with jet prior)"}
no_tensor = worst_tensor <= 1e-15 and sw["transverse"][2] <= 1e-15 and agg[2] <= 1e-14
check("V2 rule input: the S2 response has no tensor component (spin-weight reading; TT reading in the untextured aggregate)", no_tensor)
OUT["V_rule_outcome"] = "no tensor component -> clause 1: the reading 'the spin-2 radiative sector shares the transverse channel' is FALSIFIED by GW170817's polarization test"
OUT["checks"] = {"passed": sum(1 for c_ in CHECKS if c_[1]), "total": len(CHECKS)}
json.dump(OUT, open("leg1_results.json", "w"), indent=1, default=str)
print("\nALL %d CHECKS PASS" % len(CHECKS))
