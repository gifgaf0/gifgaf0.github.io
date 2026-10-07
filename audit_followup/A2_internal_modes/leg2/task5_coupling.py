"""A2 leg 2 -- Task 5: linear coupling of the internal (perpendicular) sector.

Background psi_vac(x) = phi0(x) nhat, GP dynamics i d_t psi = (-(1/2) lap + U*rho - mu) psi, psi in C^8.
Checks:
 (1) symbolic: density and current carry no term linear in chi (chi perp nhat);
 (2) numerical: on a PERIODIC background with a soft-core kernel, the Hessian of the GP energy has
     (a) no perp-parallel cross block, (b) a perp block that commutes with the complex structure
     (no anomalous chi chi term), equal to chi^dag L_perp chi with L_perp = -(1/2)lap + U*rho0 - mu;
     the parallel block does NOT commute with the complex structure (Bogoliubov pairing present);
 (3) dynamics: 8-component GP with a moving density vertex V(x - vt)|psi|^2: N_perp is conserved
     (seeded perp noise is not amplified); contrast: a vertex that mixes nhat with a perp direction
     linearly emits perp quanta at a small velocity.
"""
import json
import numpy as np
import sympy as sp

rng = np.random.default_rng(42)
OUT = {}

# ---------------------------------------------------------------- (1) symbolic
x = sp.symbols("x", real=True)
eps = sp.symbols("epsilon", positive=True)
phi0 = sp.Function("phi0", real=True)(x)
dpar_r, dpar_i = sp.Function("dr", real=True)(x), sp.Function("di", real=True)(x)
chis = [(sp.Function(f"cr{k}", real=True)(x), sp.Function(f"ci{k}", real=True)(x)) for k in range(2, 9)]
# WLOG nhat = e_1 (rho and j are U(8)-invariant, so a unitary taking nhat to e_1 maps chi perp nhat to chi perp e_1)
psi = [phi0 + eps * (dpar_r + sp.I * dpar_i)] + [eps * (a + sp.I * b) for (a, b) in chis]
rho = sum(sp.expand(p * sp.conjugate(p)) for p in psi)
j = sum(sp.im(sp.expand(sp.conjugate(p) * sp.diff(p, x))) for p in psi)
rho1 = sp.simplify(sp.diff(rho, eps).subs(eps, 0))
j1 = sp.simplify(sp.diff(j, eps).subs(eps, 0))
chi_syms = set(s for c in chis for s in c)
OUT["symbolic"] = dict(rho_linear=str(rho1), j_linear=str(j1),
                       rho_linear_contains_chi=bool(rho1.atoms(sp.Function) & chi_syms),
                       j_linear_contains_chi=bool(j1.atoms(sp.Function) & chi_syms))

# numeric version with a general (random) nhat
nhat = rng.normal(size=8) + 1j * rng.normal(size=8); nhat /= np.linalg.norm(nhat)
Pperp = np.eye(8) - np.outer(nhat, nhat.conj())
chi = Pperp @ (rng.normal(size=8) + 1j * rng.normal(size=8))
lin = []
for e in (1e-2, 1e-3, 1e-4):
    lin.append(float((np.linalg.norm(1.3 * nhat + e * chi) ** 2 - 1.3 ** 2) / e))
OUT["numeric_density_derivative_along_perp(should->0 like eps)"] = lin

# ---------------------------------------------------------------- (2) Hessian on a periodic background
M, L = 24, 12.0
dx = L / M
xs = np.arange(M) * dx
phi = 1.0 + 0.35 * np.cos(2 * np.pi * 2 * xs / L) + 0.1 * np.sin(2 * np.pi * 3 * xs / L)   # arbitrary periodic profile
mu = 0.7
a_core = 1.3
dist = np.abs(xs[:, None] - xs[None, :]); dist = np.minimum(dist, L - dist)
Uker = 0.8 * (dist < a_core)            # soft-core (step) kernel
lap = (np.roll(np.eye(M), 1, axis=0) + np.roll(np.eye(M), -1, axis=0) - 2 * np.eye(M)) / dx ** 2


def grad_real(v):
    """v = (Re psi, Im psi) flattened as [2][8][M]; returns dE/dv for
    E = sum dx [ (1/2)|grad psi|^2 - mu rho ] + (1/2) sum dx^2 rho U rho."""
    a = v[: 8 * M].reshape(8, M); b = v[8 * M:].reshape(8, M)
    rho = (a ** 2 + b ** 2).sum(0)
    Ur = Uker @ rho * dx
    ga = dx * (-(a @ lap.T) - 2 * mu * a + 2 * Ur * a)
    gb = dx * (-(b @ lap.T) - 2 * mu * b + 2 * Ur * b)
    return np.concatenate([ga.ravel(), gb.ravel()])


def embed(c):  # complex (8, M) -> real vector
    return np.concatenate([c.real.ravel(), c.imag.ravel()])


psi0 = np.outer(nhat, phi)
v0 = embed(psi0)
dim = 16 * M
H = np.zeros((dim, dim))
h = 1e-5
for i in range(dim):
    e = np.zeros(dim); e[i] = h
    H[:, i] = (grad_real(v0 + e) - grad_real(v0 - e)) / (2 * h)
H = 0.5 * (H + H.T)
# complex structure J (multiplication by i): (a, b) -> (-b, a)
Jc = np.zeros((dim, dim))
Jc[: 8 * M, 8 * M:] = -np.eye(8 * M)
Jc[8 * M:, : 8 * M] = np.eye(8 * M)
# orthonormal real bases of the parallel (nhat-line, complex) and perp subspaces at every point
basis8 = np.linalg.qr(np.column_stack([nhat] + [rng.normal(size=8) + 1j * rng.normal(size=8) for _ in range(7)]))[0]
basis8[:, 0] = nhat  # (QR may change phase; restore)
for k in range(1, 8):
    basis8[:, k] -= basis8[:, :k] @ (basis8[:, :k].conj().T @ basis8[:, k])
    basis8[:, k] /= np.linalg.norm(basis8[:, k])
def subspace(cols):
    vecs = []
    for c in cols:
        for xi in range(M):
            for ph in (1.0, 1j):
                f = np.zeros((8, M), dtype=complex)
                f[:, xi] = ph * basis8[:, c]
                vecs.append(embed(f))
    return np.array(vecs).T
Qpar = subspace([0]); Qperp = subspace(range(1, 8))
Hpp = Qperp.T @ H @ Qperp
Hqq = Qpar.T @ H @ Qpar
Hpq = Qperp.T @ H @ Qpar
Jpp = Qperp.T @ Jc @ Qperp
Jqq = Qpar.T @ Jc @ Qpar
# L_perp operator as a real quadratic form on the perp subspace: E2 = (1/2) X^T H X = dx * chi^dag L chi
Lperp = -0.5 * lap + np.diag(Uker @ (phi ** 2) * dx) - mu * np.eye(M)
# build expected (1/2) H_perp = dx * L_perp acting on each perp component (real and imag parts)
exp_half = np.zeros_like(Hpp)
# Qperp column order: for c in 1..7, for xi, for (re, im)
ncol = Qperp.shape[1]
idx = lambda c, xi, ph: ((c * M) + xi) * 2 + ph
for c in range(7):
    for xi in range(M):
        for xj in range(M):
            for ph in range(2):
                exp_half[idx(c, xi, ph), idx(c, xj, ph)] = dx * Lperp[xi, xj]
OUT["periodic_background_hessian"] = dict(
    grid=M, L=L, kernel="step U0=0.8, a=1.3", profile="1+0.35cos(4pi x/L)+0.1 sin(6pi x/L)",
    norm_H=float(np.abs(H).max()),
    perp_parallel_cross_block_max=float(np.abs(Hpq).max()),
    perp_block_commutator_with_i_max=float(np.abs(Hpp @ Jpp - Jpp @ Hpp).max()),
    parallel_block_commutator_with_i_max=float(np.abs(Hqq @ Jqq - Jqq @ Hqq).max()),
    perp_block_minus_2dx_Lperp_max=float(np.abs(0.5 * Hpp - exp_half).max()))

# ---------------------------------------------------------------- (3) 8-component GP dynamics
def gp_run(vertex, v, T=60.0, Nx=1024, Lx=200.0, g=1.0, rho0=1.0, dt=0.01, seed_amp=1e-6, V0=0.5, w=1.0):
    """Split-step 8-component GP; records N_perp(t) and the perp-sector momentum P_perp(t)."""
    xg = np.arange(Nx) * Lx / Nx - Lx / 2
    k = 2 * np.pi * np.fft.fftfreq(Nx, d=Lx / Nx)
    n = np.zeros(8, dtype=complex); n[0] = 1.0
    m = np.zeros(8, dtype=complex); m[1] = 1.0
    psi = np.sqrt(rho0) * np.outer(n, np.ones(Nx)).astype(complex)
    r = np.random.default_rng(1)
    noise = seed_amp * (r.normal(size=(8, Nx)) + 1j * r.normal(size=(8, Nx)))
    noise[0] = 0
    psi = psi + noise
    mu = g * rho0
    Pp = np.eye(8) - np.outer(n, n.conj())
    Nperp = lambda p: float(np.sum(np.abs(Pp @ p) ** 2) * Lx / Nx)
    def Pperp_mom(p):
        c = Pp @ p
        dc = np.fft.ifft(1j * k * np.fft.fft(c, axis=1), axis=1)
        return float(np.sum(np.imag(np.conj(c) * dc)) * Lx / Nx)
    kin = np.exp(-1j * dt * 0.5 * k ** 2)
    t = 0.0
    rec = [(0.0, Nperp(psi), Pperp_mom(psi))]
    x0 = -100.0
    while t < T - 1e-12:
        xx = xg - x0 - v * (t + dt / 2)
        prof = (xx / w) if vertex == "mix" else 1.0      # mixing vertex: odd profile (s(0)=0, IR-regular in 1D)
        Vx = V0 * prof * np.exp(-(xx ** 2) / (2 * w ** 2))
        for half in (0, 1):
            rho = np.sum(np.abs(psi) ** 2, axis=0)
            scal = g * rho - mu
            if vertex == "density":
                psi = psi * np.exp(-1j * (dt / 2) * (scal + Vx))
            else:  # mixing vertex V(x-vt) psi^dag (n m^dag + m n^dag) psi : eigen-decomposed per point
                psi = psi * np.exp(-1j * (dt / 2) * scal)
                a = psi[0].copy(); b = psi[1].copy()
                cth = np.cos(dt / 2 * Vx); sth = np.sin(dt / 2 * Vx)
                psi[0] = cth * a - 1j * sth * b
                psi[1] = cth * b - 1j * sth * a
            if half == 0:
                psi = np.fft.ifft(kin * np.fft.fft(psi, axis=1), axis=1)
        t += dt
        if abs(t / 5 - round(t / 5)) < 1e-9:
            rec.append((round(t, 6), Nperp(psi), Pperp_mom(psi)))
    return rec


res_density = gp_run("density", v=0.3)
V0m, wm_, vm = 0.02, 1.0, 0.3   # linear-response regime (at V0=0.1 part of the momentum is shared nonlinearly with the parallel sector)
res_mix = gp_run("mix", v=vm, seed_amp=0.0, V0=V0m, w=wm_, T=150.0, Nx=4096, Lx=800.0)
# 1D golden rule for the linear source s(x) = V0 (x/w) exp(-x^2/2w^2) sqrt(rho0) into omega = k^2/2:
# |s_k| = V0 |k| w^2 sqrt(2pi) exp(-k^2 w^2/2); momentum-transfer rate F = |s(k*)|^2 k*/v, k* = 2v -> F = 2|s(2v)|^2
sk = lambda kk: V0m * abs(kk) * wm_ ** 2 * np.sqrt(2 * np.pi) * np.exp(-kk ** 2 * wm_ ** 2 / 2)
F_gr = 2 * sk(2 * vm) ** 2
tt = np.array([r[0] for r in res_mix]); PP = np.array([r[2] for r in res_mix])
sel = tt >= 60
slope = float(np.polyfit(tt[sel], PP[sel], 1)[0])
OUT["gp_dynamics"] = dict(
    note="uniform 8-component condensate rho0=1, g=1 (c_s=1); vertex moves at v=0.3 c_s (subsonic: phonon Landau channel closed)",
    density_vertex_Nperp_vs_t=res_density,
    density_vertex_Nperp_rel_change=float(abs(res_density[-1][1] - res_density[0][1]) / res_density[0][1]),
    mixing_vertex=dict(V0=V0m, w=wm_, v=vm, record_t_Nperp_Pperp=res_mix,
                       Pperp_slope_t_ge_60=slope, golden_rule_F_1D=float(F_gr),
                       ratio=float(slope / F_gr)),
)
print(json.dumps(OUT, indent=1, default=str))
with open("task5_results.json", "w") as fh:
    json.dump(OUT, fh, indent=1, default=str)
