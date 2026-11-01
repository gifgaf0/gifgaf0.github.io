"""Instrument checks for PREREG_chiral_loop.md §3 (items 1-3), the gamma = 0 bitwise identity, the start check,
and the 1D sign-convention comparison with chiral1d.py. Items 4 (regression) and 5 (C0) are separate runs.
usage: python3 chiral_loop_checks.py   (prints; the committed output is chiral_loop_checks_output.txt)
"""
import numpy as np, json, platform, scipy
from gl3 import GL3, check_grad as gl3_check_grad
from gl3_chiral import GL3Chiral, check_grad
from starts import start_fields
from linking import analyse

print(f'python {platform.python_version()}, numpy {np.__version__}, scipy {scipy.__version__}')
E9 = 1 / np.sqrt(12.0)

# ---------------------------------------------------------------- 1. gradient
print('\n== 1. gradient check of the full functional')
print('gl3.check_grad (gamma absent, reference):           ', gl3_check_grad())
print('gl3-style check, GL3Chiral gamma = 0.3:              ', check_grad(gamma=0.3))
print('gl3-style check, GL3Chiral gamma = -0.3:             ', check_grad(gamma=-0.3))
for gam in (0.3, -0.3):
    g = GL3Chiral(N=6, h=0.5, eta=0.1, gamma=gam); rng = np.random.default_rng(0)
    v = rng.normal(size=9 * g.nsite) * 0.5; E, gr = g.energy_grad(v)
    idx = rng.choice(v.size, 400, replace=False); eps = 1e-3
    rel = []; zabs = []
    for i in idx:
        f = lambda t: (lambda vp: (vp.__setitem__(i, vp[i] + t), g.energy_grad(vp)[0])[1])(v.copy())
        fd = (f(-2 * eps) - 8 * f(-eps) + 8 * f(eps) - f(2 * eps)) / (12 * eps)
        if gr[i] == 0.0: zabs.append(abs(fd))
        else: rel.append(abs(fd - gr[i]) / abs(gr[i]))
    print(f'5-point stencil (step 1e-3), gamma = {gam:+.1f}, 400 random components: worst |fd-g|/|g| over the '
          f'{len(rel)} with g != 0 = {max(rel):.3e}; {len(zabs)} have g == 0 exactly (unused link slices / no '
          f'dependence), max |fd| there = {max(zabs) if zabs else 0:.1e}')
# chiral term alone
g = GL3Chiral(N=7, h=0.5, eta=0.1, gamma=0.3); rng = np.random.default_rng(1)
psi = rng.normal(size=(3, 7, 7, 7)) + 1j * rng.normal(size=(3, 7, 7, 7)); A = rng.normal(size=(3, 7, 7, 7))
E0, gp, gA = g.chiral_energy_grad(psi, A); gv = np.concatenate([gp.real.ravel(), gp.imag.ravel(), gA.ravel()])
v = g.pack(psi, A); worst = 0.0
def Ech(vv):
    p, a = g.unpack(vv); return g.chiral_energy_grad(p, a, with_grad=False)[0]
for i in rng.choice(v.size, 400, replace=False):
    if gv[i] == 0.0: continue
    eps = 1e-3; f = lambda t: Ech((lambda vp: (vp.__setitem__(i, vp[i] + t), vp)[1])(v.copy()))
    fd = (f(-2 * eps) - 8 * f(-eps) + 8 * f(eps) - f(2 * eps)) / (12 * eps)
    worst = max(worst, abs(fd - gv[i]) / abs(gv[i]))
print(f'chiral term alone, 5-point, N = 7, 400 components: worst relative error {worst:.3e}')

# ---------------------------------------------------------------- 2. reality and gauge invariance
print('\n== 2. reality and gauge invariance (random states)')
for seed in range(5):
    N = 9; g = GL3Chiral(N=N, h=0.5, eta=0.1, gamma=0.3); rng = np.random.default_rng(100 + seed)
    psi = rng.normal(size=(3, N, N, N)) + 1j * rng.normal(size=(3, N, N, N)); A = rng.normal(size=(3, N, N, N))
    C = g.chiral_complex(psi, A); Ec = g.chiral_energy_grad(psi, A, gamma=1.0, with_grad=False)[0]
    dens = g.chiral_density(psi, A, gamma=1.0).sum()
    # smooth gauge transformation
    alpha = 1.3 * np.sin(0.4 * g.x + 0.2) * np.cos(0.3 * g.y) + 0.7 * np.sin(0.5 * g.z - 0.1 * g.x) + 0.5
    psi2 = psi * np.exp(1j * alpha); A2 = A.copy()
    for j in range(3):
        lo = [slice(None)] * 3; hi = [slice(None)] * 3; lo[j] = slice(0, N - 1); hi[j] = slice(1, N)
        A2[j][tuple(lo)] += (alpha[tuple(hi)] - alpha[tuple(lo)]) / (g.e * g.h)
    Ec2 = g.chiral_energy_grad(psi2, A2, gamma=1.0, with_grad=False)[0]
    Et = g.energy_grad(g.pack(psi, A))[0]; Et2 = g.energy_grad(g.pack(psi2, A2))[0]
    print(f'seed {100+seed}: |Im|/|Re| = {abs(C.imag)/abs(C.real):.2e}; |Re C - E_chi(code)|/|E_chi| = '
          f'{abs(C.real-Ec)/abs(Ec):.2e}; |sum density - E_chi|/|E_chi| = {abs(dens-Ec)/abs(Ec):.2e}; '
          f'gauge: chiral rel change {abs(Ec2-Ec)/abs(Ec):.2e}, total (gamma 0.3) rel change {abs(Et2-Et)/abs(Et):.2e}')

# ---------------------------------------------------------------- 3. parity
print('\n== 3. parity (inversion x -> -x, psi -> -psi(-x), A -> -A(-x) as vectors; N odd, grid symmetric about 0)')
def invert(psi, A):
    P = -psi[:, ::-1, ::-1, ::-1]
    Ai = np.stack([-np.roll(A[j][::-1, ::-1, ::-1], -1, axis=j) for j in range(3)])
    return P, Ai
for seed in range(3):
    N = 9; g = GL3Chiral(N=N, h=0.5, eta=0.1, gamma=0.3); rng = np.random.default_rng(200 + seed)
    psi = rng.normal(size=(3, N, N, N)) + 1j * rng.normal(size=(3, N, N, N)); A = rng.normal(size=(3, N, N, N))
    for j in range(3):   # zero the unused last link slice so the inversion is a bijection on used links
        s = [slice(None)] * 3; s[j] = N - 1; A[j][tuple(s)] = 0.0
    Pp, PA = invert(psi, A)
    E1 = g.chiral_energy_grad(psi, A, with_grad=False)[0]; E2 = g.chiral_energy_grad(Pp, PA, with_grad=False)[0]
    gm = GL3Chiral(N=N, h=0.5, eta=0.1, gamma=-0.3)
    Ep = g.energy_grad(g.pack(Pp, PA))[0]; Em = gm.energy_grad(g.pack(psi, A))[0]
    print(f'seed {200+seed}: E_chi(P state)/E_chi(state) = {E2/E1!r}; |E_+g(P state) - E_-g(state)|/|E| = {abs(Ep-Em)/abs(Em):.2e}')

# ---------------------------------------------------------------- gamma = 0 identity
print('\n== gamma = 0: GL3Chiral.energy_grad vs GL3.energy_grad (bitwise)')
rng = np.random.default_rng(5)
g0 = GL3(N=9, h=0.5, eta=0.1); gc = GL3Chiral(N=9, h=0.5, eta=0.1, gamma=0.0)
v = rng.normal(size=9 * g0.nsite)
a, b = g0.energy_grad(v), gc.energy_grad(v)
print('random state N = 9: E equal', a[0] == b[0], '; gradient array_equal', np.array_equal(a[1], b[1]))
g0 = GL3(N=65, h=0.5, eta=0.1); gc = GL3Chiral(N=65, h=0.5, eta=0.1, gamma=0.0)
psi = start_fields(g0, 'B', 6.0); v = g0.pack(psi, np.zeros((3, 65, 65, 65)))
a, b = g0.energy_grad(v), gc.energy_grad(v)
print('start B, 65^3: E equal', a[0] == b[0], '; gradient array_equal', np.array_equal(a[1], b[1]))

# ---------------------------------------------------------------- starts
print('\n== starts at 65^3, R0 = 6')
print([analyse(start_fields(g0, s, 6.0)) for s in 'AB'])
for s in 'AB':
    p = start_fields(g0, s, 6.0); A0 = np.zeros((3, 65, 65, 65))
    for gam in (0.1, 0.2, 0.3):
        Ep = GL3Chiral(N=65, eta=0.1, gamma=gam).chiral_energy_grad(p, A0, with_grad=False)[0]
        print(f'start {s}: E_chi at iteration 0, gamma = +{gam}: {Ep:+.6e}  (gamma = -{gam}: {-Ep:+.6e})')

# ---------------------------------------------------------------- 1D sign convention
print('\n== 1D sign convention: chiral1d.Chain (n = z, P = 10, M = 20, h = 0.5) vs GL3Chiral on a 41^3 slab')
import chiral1d
M, P = 20, 10.0; N3 = 2 * M + 1
for label in ('director helix', 'complex texture with A'):
    for gam in (0.3, -0.3):
        ch = chiral1d.Chain(np.array([0., 0., 1.]), 0.1, gam, P, Afree=True, M=M)
        s = np.arange(M) * ch.h; q = 2 * np.pi / P; f0 = np.sqrt(1.1)
        if label == 'director helix':
            psi1 = f0 * np.stack([np.cos(q * s), np.sin(q * s), 0 * s]).astype(complex)
            a = np.zeros(M); c = np.zeros((2, M))
        else:
            ph = np.stack([0 * s, 2 * np.pi / 3 + 0.5 * np.sin(q * s), 4 * np.pi / 3 + 0.3 * np.cos(2 * q * s)])
            amp = f0 * (1 + 0.1 * np.stack([np.cos(q * s), np.sin(2 * q * s), 0 * s]))
            psi1 = amp * np.exp(1j * ph)
            a = 0.4 * np.sin(q * s); c = np.stack([0.3 * np.cos(q * s), -0.2 + 0.1 * np.sin(q * s)])
        x1 = ch.pack(psi1, a, c); pt = ch.parts(x1)
        val1 = pt['chiral'] / P
        g3 = GL3Chiral(N=N3, h=0.5, eta=0.1, gamma=gam)
        iz = np.arange(N3) % M
        psi3 = np.broadcast_to(psi1[:, iz][:, None, None, :], (3, N3, N3, N3)).copy()
        A3 = np.zeros((3, N3, N3, N3))
        A3[0][:] = c[0][iz][None, None, :]; A3[1][:] = c[1][iz][None, None, :]; A3[2][:] = a[iz][None, None, :]
        dens = g3.chiral_density(psi3, A3)
        sub = dens[1:N3 - 1, 1:N3 - 1, M // 2:M // 2 + M]
        val3 = sub.sum() / (g3.h ** 3 * sub.size)
        print(f'{label:24s} gamma = {gam:+.1f}: chiral1d chiral/length = {val1:+.8e} '
              f'(link {pt["chiral_link"]/P:+.4e}, A_perp.S {pt["chiral_AperpS"]/P:+.4e}); '
              f'gl3_chiral density (interior, one period) = {val3:+.8e}; rel. diff {abs(val3-val1)/abs(val1):.2e}')
    if label == 'director helix':
        print(f'   continuum value for the helix: -gamma f^2 q = {-0.3*1.1*q:+.6e} (gamma = 0.3); lattice -gamma f^2 sin(qh)/h = {-0.3*1.1*np.sin(q*0.5)/0.5:+.6e}')
