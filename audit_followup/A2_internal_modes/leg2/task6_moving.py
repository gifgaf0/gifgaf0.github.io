"""A2 leg 2 -- Task 6: moving objects and the internal (perpendicular) branch omega = k^2/(2m).  m = hbar = 1.

(a)/(c) linear source s(x - vt) in the lab (condensate) frame:  i d_t chi = -(1/2) lap chi + s(x - vt).
     Golden rule: F = int d^dk/(2pi)^d 2pi |s_k|^2 delta(k^2/2 - k.v) k_par.
     -> brute-force quadrature with a smeared delta in 2D and 3D, small-v exponents, closed forms
        F_2D = m^2 |s(0)|^2 v,  F_3D = m^3 |s(0)|^2 v^2 / pi;
     -> 1D time-dependent simulation (dipole source, s(0) = 0, IR-regular) vs the golden rule at several v
        (emission at every v > 0, no threshold).
(b) bound state of a co-moving well (Poschl-Teller -sech^2, E_b = 1/2) in a uniform background, lab-frame
     simulation at v up to 2 (above the naive sqrt(2 E_b) = 1): the Galilean-boosted bound state is exact.
(d) same, with a lattice potential A cos(G x) at rest (G = 2): emission iff G v >= E_b (first order),
     decay rate vs Fermi golden rule with the exact reflectionless continuum states.
"""
import json
import numpy as np

OUT = {}

# ------------------------------------------------------------------------------------------- (c) quadrature
def s_gauss(k, s0=1.0, sig=1.0):
    return s0 * np.exp(-k ** 2 * sig ** 2 / 2)


def F2D_quad(v, eta=None, nk=4000, nphi=721):
    """2D: F = (1/2pi) int k dk dphi |s|^2 delta_eta(k^2/2 - k v cos phi) k cos phi."""
    if eta is None:
        eta = 0.02 * v * v
    kmax = 3.0 * v   # the resonance lies at k <= 2v
    k = np.linspace(1e-6, kmax, nk)
    phi = np.linspace(-np.pi, np.pi, nphi)
    K, P = np.meshgrid(k, phi, indexing="ij")
    arg = K ** 2 / 2 - K * v * np.cos(P)
    delta = np.exp(-arg ** 2 / (2 * eta ** 2)) / (np.sqrt(2 * np.pi) * eta)
    integrand = K * s_gauss(K) ** 2 * delta * K * np.cos(P)
    return np.trapezoid(np.trapezoid(integrand, phi, axis=1), k) / (2 * np.pi)


def F3D_quad(v, eta=None, nk=4000, nc=801):
    """3D: F = (1/(2pi)^2) int k^2 dk 2pi dc |s|^2 delta_eta(k^2/2 - k v c) k c."""
    if eta is None:
        eta = 0.02 * v * v
    kmax = 3.0 * v   # the resonance lies at k <= 2v
    k = np.linspace(1e-6, kmax, nk)
    c = np.linspace(-1, 1, nc)
    K, C = np.meshgrid(k, c, indexing="ij")
    arg = K ** 2 / 2 - K * v * C
    delta = np.exp(-arg ** 2 / (2 * eta ** 2)) / (np.sqrt(2 * np.pi) * eta)
    integrand = K ** 2 * s_gauss(K) ** 2 * delta * K * C
    return 2 * np.pi * np.trapezoid(np.trapezoid(integrand, c, axis=1), k) / (2 * np.pi) ** 2


def F2D_exact(v):  # delta resolved: k* = 2 v cos(phi)
    phi = np.linspace(-np.pi / 2, np.pi / 2, 20001)
    ks = 2 * v * np.cos(phi)
    return np.trapezoid(ks ** 2 / v * s_gauss(ks) ** 2, phi) / (2 * np.pi)


def F3D_exact(v):
    c = np.linspace(0, 1, 20001)
    ks = 2 * v * c
    return 2 * np.pi * np.trapezoid(ks ** 3 / v * s_gauss(ks) ** 2, c) / (2 * np.pi) ** 2


vs = np.array([0.02, 0.04, 0.08, 0.16, 0.32])
F2q = np.array([F2D_quad(v) for v in vs]); F3q = np.array([F3D_quad(v) for v in vs])
F2e = np.array([F2D_exact(v) for v in vs]); F3e = np.array([F3D_exact(v) for v in vs])
p2 = np.polyfit(np.log(vs[:3]), np.log(F2q[:3]), 1)[0]
p3 = np.polyfit(np.log(vs[:3]), np.log(F3q[:3]), 1)[0]
OUT["c_golden_rule_drag"] = dict(
    source="s(k) = exp(-k^2/2), s(0) = 1, m = 1",
    v=vs.tolist(),
    F2D_quadrature=F2q.tolist(), F2D_delta_resolved=F2e.tolist(), F2D_closed_form_small_v=(vs).tolist(),
    F3D_quadrature=F3q.tolist(), F3D_delta_resolved=F3e.tolist(), F3D_closed_form_small_v=(vs ** 2 / np.pi).tolist(),
    fitted_exponent_2D=float(p2), fitted_exponent_3D=float(p3))


# ------------------------------------------------------------------------------------------- 1D simulations
def sech(x):
    ax = np.abs(x)
    return 2 * np.exp(-ax) / (1 + np.exp(-2 * ax))


def absorber(x, xa, width, strength):
    eta = np.zeros_like(x)
    m = np.abs(x) > xa
    eta[m] = strength * ((np.abs(x[m]) - xa) / width) ** 2
    return eta


def source_run(v, V0=0.1, w=1.0, T=150.0, Nx=4096, Lx=800.0, dt=0.01):
    x = np.arange(Nx) * Lx / Nx - Lx / 2
    k = 2 * np.pi * np.fft.fftfreq(Nx, d=Lx / Nx)
    chi = np.zeros(Nx, complex)
    kin = np.exp(-1j * dt * 0.5 * k ** 2)
    t = 0.0; rec = []; x0 = -100.0
    while t < T - 1e-12:
        xx = x - x0 - v * (t + dt / 2)
        s = V0 * (xx / w) * np.exp(-xx ** 2 / (2 * w ** 2))
        chi = chi - 1j * dt * s
        chi = np.fft.ifft(kin * np.fft.fft(chi))
        t += dt
        if abs(t / 10 - round(t / 10)) < 1e-6:
            dc = np.fft.ifft(1j * k * np.fft.fft(chi))
            rec.append((round(t, 3), float(np.sum(np.imag(np.conj(chi) * dc)) * Lx / Nx)))
    tt = np.array([r[0] for r in rec]); PP = np.array([r[1] for r in rec])
    sel = tt >= 0.5 * T
    slope = float(np.polyfit(tt[sel], PP[sel], 1)[0])
    ks = 2 * v
    F = 2 * (V0 * ks * w ** 2 * np.sqrt(2 * np.pi) * np.exp(-ks ** 2 * w ** 2 / 2)) ** 2
    return slope, float(F)


src = {}
for v in (0.1, 0.2, 0.3, 0.5):
    T = 300.0 if v < 0.15 else 150.0
    sl, F = source_run(v, T=T, Lx=(1200.0 if v < 0.15 else 800.0), Nx=(6144 if v < 0.15 else 4096))
    src[str(v)] = dict(dPdt_sim=sl, golden_rule=F, ratio=sl / F)
OUT["a_c_1D_moving_source_simulation"] = dict(source="dipole s(x) = 0.1 (x/w) exp(-x^2/2w^2), w = 1 (s(0) = 0, IR-regular in 1D)",
                                               results=src)


def bound_run(v, A=0.0, G=2.0, T=200.0, Nx=8192, Lx=1000.0, dt=0.005, x0=-250.0):
    """Lab frame: i d_t chi = -(1/2) chi'' - sech^2(x - x0 - v t) chi + A cos(G x) chi; initial state =
    Galilean-boosted bound state e^{i v x} sech(x - x0)/sqrt(2). Returns |<boosted bound state(t)|chi(t)>|^2."""
    x = np.arange(Nx) * Lx / Nx - Lx / 2
    dx = Lx / Nx
    k = 2 * np.pi * np.fft.fftfreq(Nx, d=dx)
    kin = np.exp(-1j * dt * 0.5 * k ** 2)
    absorb = np.exp(-dt * absorber(x, 0.42 * Lx, 0.08 * Lx, 2.0))
    chi = np.exp(1j * v * x) * sech(x - x0) / np.sqrt(2)
    Vlat = A * np.cos(G * x)
    t = 0.0; rec = []
    nstep = int(round(T / dt))
    for n in range(nstep):
        Vh = -sech(x - x0 - v * (t + dt / 2)) ** 2 + Vlat
        ph = np.exp(-1j * (dt / 2) * Vh)
        chi = ph * chi
        chi = np.fft.ifft(kin * np.fft.fft(chi))
        chi = ph * chi * absorb
        t += dt
        if (n + 1) % int(round(5.0 / dt)) == 0:
            ref = np.exp(1j * v * x) * sech(x - x0 - v * t) / np.sqrt(2)
            ov = abs(np.sum(np.conj(ref) * chi) * dx) ** 2
            rec.append((round(t, 3), float(ov)))
    return rec


def fgr_rate(v, A, G=2.0, Eb=0.5):
    """First-order Fermi golden rule (object frame) with exact reflectionless continuum states of -sech^2:
    psi_k = (tanh x - i k) e^{i k x} / (sqrt(2 pi) sqrt(1 + k^2)),  bound b = sech x / sqrt 2."""
    Ef = G * v - Eb
    if Ef <= 0:
        return 0.0
    kk = np.sqrt(2 * Ef)
    xq = np.linspace(-40, 40, 200001)
    b = 1 / np.cosh(xq) / np.sqrt(2)
    tot = 0.0
    for ksgn in (kk, -kk):
        psik = (np.tanh(xq) - 1j * ksgn) * np.exp(1j * ksgn * xq) / (np.sqrt(2 * np.pi) * np.sqrt(1 + ksgn ** 2))
        # absorption term of A cos(G(xi + v t)): (A/2) e^{-i G xi} e^{-i G v t}
        Mk = np.trapezoid(np.conj(psik) * np.exp(-1j * G * xq) * b, xq)
        tot += abs(0.5 * A * Mk) ** 2 / abs(ksgn)
    return 2 * np.pi * tot


def decay_rate(rec, tmin=60.0):
    t = np.array([r[0] for r in rec]); p = np.array([r[1] for r in rec])
    sel = t >= tmin
    return float(-np.polyfit(t[sel], np.log(p[sel]), 1)[0])


uni = {}
for v in (0.4, 1.0, 2.0):
    rec = bound_run(v, A=0.0)
    uni[str(v)] = dict(min_overlap=min(r[1] for r in rec), final_overlap=rec[-1][1])
OUT["b_uniform_background_bound_state"] = dict(E_b=0.5, naive_threshold_sqrt_2Eb=1.0, results=uni)

lat = {}
for (v, A) in ((0.1, 0.1), (0.2, 0.1), (0.4, 0.1), (0.4, 0.05), (0.7, 0.1), (1.0, 0.1)):
    rec = bound_run(v, A=A)
    lat[f"v={v},A={A}"] = dict(Gv=2.0 * v, emits_first_order=bool(2.0 * v > 0.5),
                               overlap_t5=rec[0][1], overlap_final=rec[-1][1],
                               fitted_decay_rate=decay_rate(rec), fgr_rate=fgr_rate(v, A))
OUT["d_crystal_bound_state"] = dict(G=2.0, E_b=0.5, first_order_threshold_v=0.25, results=lat)

print(json.dumps(OUT, indent=1))
with open("task6_results.json", "w") as fh:
    json.dump(OUT, fh, indent=1)
