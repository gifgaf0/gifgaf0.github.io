r"""Second-leg (blind) check, Q5: vortex ring (radius R, axis z, moving along z at V) in d=3.
omega(x) = kappa \oint dl delta^3(x - X);  v(q) = i q x omega(q) / q^2  (div-free Biot-Savart).
"""
import sympy as sp
import numpy as np
from scipy.special import j1

# --- exact line-integral vorticity transform vs closed form -------------------
def omega_q_numeric(qv, R=1.0, kappa=2 * np.pi, n=4096):
    ph = 2 * np.pi * np.arange(n) / n
    X = R * np.stack([np.cos(ph), np.sin(ph), 0 * ph], 1)
    dl = R * np.stack([-np.sin(ph), np.cos(ph), 0 * ph], 1)
    ph_ = np.exp(-1j * X @ np.asarray(qv))
    return kappa * (dl * ph_[:, None]).sum(0) * (2 * np.pi / n)

def omega_q_closed(qv, R=1.0, kappa=2 * np.pi):
    qv = np.asarray(qv, float); qp = np.hypot(qv[0], qv[1])
    if qp == 0: return np.zeros(3, complex)
    qph = np.array([qv[0], qv[1], 0]) / qp
    return -2j * np.pi * kappa * R * j1(qp * R) * np.cross([0, 0, 1], qph)

def v_q(qv, om):
    qv = np.asarray(qv, float)
    return 1j * np.cross(qv, om) / (qv @ qv)

print("omega(q): numeric line integral vs closed form -2 pi i kappa R J1(q_perp R) (z x qhat_perp)")
for qv in [(0.3, 0.1, 0.2), (1.7, -0.4, 0.9), (0.05, 0.02, -0.03)]:
    a, b = omega_q_numeric(qv), omega_q_closed(qv)
    print(f"  q={qv}: max|diff| = {np.max(np.abs(a - b)):.2e}")

# --- symbolic small-qR form ------------------------------------------------
qp_, qz, R, kap, V, th = sp.symbols('q_perp q_z R kappa V vartheta', positive=True)
q = sp.sqrt(qp_**2 + qz**2)
a = sp.symbols('a', positive=True)
print("2 J1(a)/a =", sp.series(2 * sp.besselj(1, a) / a, a, 0, 5))
# exact: v(q) = 2 pi kappa R J1(q_perp R) (q_perp zhat - q_z qhat_perp)/q^2
#            = kappa pi R^2 [2 J1(q_perp R)/(q_perp R)] (1 - qhat qhat) . zhat
Vdotv_exact = 2 * sp.pi * kap * R * V * sp.besselj(1, qp_ * R) * qp_ / q**2
Vdotv_small = sp.simplify(sp.series(Vdotv_exact.subs({qp_: a * sp.sin(th) / R, qz: a * sp.cos(th) / R}), a, 0, 3).removeO())
print("V.v(q) small qR =", sp.simplify(Vdotv_small))

# numerical check of v(q) -> kappa pi R^2 (zhat - qhat (qhat.zhat)) at small q
for qv in [(1e-3, 0, 0), (0, 0, 1e-3), (7e-4, 0, 7e-4), (3e-4, 4e-4, -2e-4)]:
    vv = v_q(qv, omega_q_numeric(qv))
    qh = np.asarray(qv) / np.linalg.norm(qv)
    pred = np.pi * 2 * np.pi * (np.array([0, 0, 1]) - qh * qh[2])
    print(f"  qhat={np.round(qh,3)}: v(q)={np.round(vv.real,5)}  pred={np.round(pred,5)}  |Im|={np.max(np.abs(vv.imag)):.1e}"
          f"  q.v={abs(np.dot(qv, vv)):.1e}")

# --- sizes --------------------------------------------------------------------
kv, eps, Vv, ck = 2 * np.pi, 1.0, 7.85, 9.38
Rv = xi = 1 / ck
vv_max = np.pi * kv * Vv * Rv**2
deficit = ck**2 * eps * xi**3
print("\nRatio |V.v(q)| / (c^2 eps xi^3) = pi kappa V R^2 sin^2(th) / (eps c^2 xi^3)")
print("  with R = xi = 1/c:  = (pi kappa/eps)(V/c) sin^2(th)")
print(f"  |V.v|max = pi kappa V R^2 = {vv_max:.5f};  deficit vertex = {deficit:.5f};  ratio(th=90deg) = {vv_max/deficit:.4f}")
print(f"  2 pi^2 V/c = {2*np.pi**2*Vv/ck:.4f};  angle-avg <sin^2>=2/3 -> {2/3*vv_max/deficit:.4f};  ratio^2 = {(vv_max/deficit)**2:.1f}")
print(f"  V/c = {Vv/ck:.4f}  (< 1: no Cherenkov cone at speed c)")
for c_low in [0.5 * ck, 0.7 * ck]:
    print(f"   on Cherenkov cone of a slower branch c={c_low:.3f}: sin^2 = 1-c^2/V^2 = {1-(c_low/Vv)**2:.4f}"
          f" -> ratio {vv_max/deficit*(1-(c_low/Vv)**2):.3f}")
# finite-qR factor 2J1(x)/x at a few qR
for qR in [0.1, 0.3, 1.0]:
    print(f"   qR={qR}: 2J1(qR)/(qR) = {2*j1(qR)/qR:.4f}  (q perp V)")

# --- context: Kelvin thin-ring speed at R = xi ------------------------------------
pref = kv / (4 * np.pi * Rv)
print(f"\nThin-ring speed kappa/(4 pi R)[ln(8R/xi) - a] at R=xi: prefactor {pref:.4f}, ln 8 = {np.log(8):.4f}")
for acore, lab in [(0.25, 'solid core 1/4'), (0.5, 'hollow core 1/2'), (0.615, 'GP (Roberts-Grant) 0.615')]:
    print(f"   {lab:26s}: V = {pref*(np.log(8)-acore):.3f}")
print(f"   V = 7.85 requires a = {np.log(8) - Vv/pref:.3f}")
# Bernoulli source at q->0 for the ring (thin-ring kinetic energy per density), rough
for acore, lab in [(7 / 4, 'solid'), (2.0, 'hollow'), (1.615, 'GP')]:
    print(f"   Bernoulli FT(|v|^2/2)(q->0) ~ (kappa^2 R/2)(ln 8R/xi - {acore}) [{lab}] = {kv**2*Rv/2*(np.log(8)-acore):.4f}")
