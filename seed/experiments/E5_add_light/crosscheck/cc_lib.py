"""Cross-check library for E5 (independent of the original E5 scripts).

Everything here works at the level of the matrix Lagrangian

    L = (1/16) Tr(d_mu U d^mu U^+) + (1/32) Tr([L_mu, L_nu][L^mu, L^nu]) + (beta^2/16) Tr(U + U^+ - 2)

in dimensionless units (x = e F r, t = e F t_phys, L_phys = (eF)^4/e^2 * L), metric (+,-,-,-),
L_mu = U^+ d_mu U.  Noether currents are obtained by *differentiating this Lagrangian numerically*
(exact 5-point stencil: L is a polynomial of degree <= 4 in each d_mu U), never from closed-form
current formulas.  The baryon current is evaluated from its matrix definition.
"""
import numpy as np

I2 = np.eye(2, dtype=complex)
TAU = np.array([[[0, 1], [1, 0]], [[0, -1j], [1j, 0]], [[1, 0], [0, -1]]], dtype=complex)
GMET = np.array([1.0, -1.0, -1.0, -1.0])


def dag(M):
    return np.conj(np.swapaxes(M, -1, -2))


def tr(M):
    return np.trace(M, axis1=-2, axis2=-1)


def lagrangian(U, dU, beta2=0.0, parts=False):
    """U: (N,n,n); dU: (N,4,n,n) = d_mu U (lower index).  Returns L (N,) (dimensionless)."""
    Ud = dag(U)
    L2 = np.zeros(U.shape[0])
    for mu in range(4):
        L2 += GMET[mu] * tr(dU[:, mu] @ dag(dU[:, mu])).real
    L2 /= 16.0
    Lm = [Ud @ dU[:, mu] for mu in range(4)]
    L4 = np.zeros(U.shape[0])
    for mu in range(4):
        for nu in range(mu + 1, 4):
            Cm = Lm[mu] @ Lm[nu] - Lm[nu] @ Lm[mu]
            L4 += 2.0 * GMET[mu] * GMET[nu] * tr(Cm @ Cm).real   # (mu,nu) and (nu,mu)
    L4 /= 32.0
    n = U.shape[-1]
    Lmass = beta2 / 16.0 * (tr(U + Ud).real - 2.0 * n) if beta2 else np.zeros(U.shape[0])
    if parts:
        return L2, L4, Lmass
    return L2 + L4 + Lmass


def noether(U, dU, mu, X, beta2=0.0, h=0.5):
    """j^mu = sum_A dL/d(d_mu phi^A) delta phi^A, with delta U = X (tangent at U).
    Exact for a polynomial of degree <= 4 in the perturbation (5-point central stencil)."""
    vals = []
    for s in (-2, -1, 1, 2):
        d2 = dU.copy()
        d2[:, mu] = d2[:, mu] + s * h * X
        vals.append(lagrangian(U, d2, beta2))
    fm2, fm1, fp1, fp2 = vals
    return (fm2 - 8 * fm1 + 8 * fp1 - fp2) / (12 * h)


def levi4():
    import itertools
    eps = np.zeros((4, 4, 4, 4))
    for p in itertools.permutations(range(4)):
        # parity of permutation
        sgn = 1
        pl = list(p)
        for i in range(4):
            for j in range(i + 1, 4):
                if pl[i] > pl[j]:
                    sgn = -sgn
        eps[p] = sgn
    return eps


EPS4 = levi4()


def baryon_current(U, dU):
    """B^mu = (1/24 pi^2) eps^{mu nu a b} Tr(L_nu L_a L_b), eps^{0123} = +1 (raw sign convention;
    the overall sign is reported, not assumed)."""
    Ud = dag(U)
    Lm = [Ud @ dU[:, mu] for mu in range(4)]
    B = np.zeros((U.shape[0], 4))
    for mu in range(4):
        acc = np.zeros(U.shape[0], dtype=complex)
        for nu in range(4):
            for a in range(4):
                for b in range(4):
                    e = EPS4[mu, nu, a, b]
                    if e != 0:
                        acc += e * tr(Lm[nu] @ Lm[a] @ Lm[b])
        B[:, mu] = (acc / (24 * np.pi ** 2)).real
    return B


def hedgehog(xv, F, Fp):
    """U0 = cos F + i sin F n.tau and its spatial derivatives d_i U0 (i = 1..3), for points xv (N,3)."""
    r = np.linalg.norm(xv, axis=1)
    n = xv / r[:, None]
    s, c = np.sin(F), np.cos(F)
    ntau = np.einsum('ni,ijk->njk', n, TAU)
    U = c[:, None, None] * I2 + 1j * s[:, None, None] * ntau
    dU = np.zeros((xv.shape[0], 3, 2, 2), dtype=complex)
    for i in range(3):
        dn_tau = (TAU[i][None] - n[:, i][:, None, None] * ntau) / r[:, None, None]  # d_i (n.tau)
        dU[:, i] = (-s * Fp * n[:, i])[:, None, None] * I2 \
            + 1j * (c * Fp * n[:, i])[:, None, None] * ntau + 1j * s[:, None, None] * dn_tau
    return U, dU


def embed3(M2):
    """embed (N,2,2) into (N,3,3) upper-left block, 1 in (3,3) for U; for derivatives use embed3d."""
    N = M2.shape[0]
    M3 = np.zeros((N, 3, 3), dtype=complex)
    M3[:, :2, :2] = M2
    M3[:, 2, 2] = 1.0
    return M3


def embed3d(M2):
    N = M2.shape[0]
    M3 = np.zeros((N, 3, 3), dtype=complex)
    M3[:, :2, :2] = M2
    return M3


GELL = np.zeros((8, 3, 3), dtype=complex)
GELL[0][0, 1] = GELL[0][1, 0] = 1
GELL[1][0, 1] = -1j; GELL[1][1, 0] = 1j
GELL[2][0, 0] = 1; GELL[2][1, 1] = -1
GELL[3][0, 2] = GELL[3][2, 0] = 1
GELL[4][0, 2] = -1j; GELL[4][2, 0] = 1j
GELL[5][1, 2] = GELL[5][2, 1] = 1
GELL[6][1, 2] = -1j; GELL[6][2, 1] = 1j
GELL[7] = np.diag([1, 1, -2]) / np.sqrt(3)


def sphere_rule(nth=10, nph=12):
    """product rule on S^2, exact for polynomials in n of degree < min(2 nth, nph)."""
    xg, wg = np.polynomial.legendre.leggauss(nth)
    ph = (np.arange(nph) + 0.5) * 2 * np.pi / nph
    ct = np.repeat(xg, nph)
    w = np.repeat(wg, nph) * (2 * np.pi / nph)
    phi = np.tile(ph, nth)
    st = np.sqrt(1 - ct ** 2)
    n = np.stack([st * np.cos(phi), st * np.sin(phi), ct], axis=1)
    return n, w   # sum w = 4 pi


# ---------------------------------------------------------------- collective quantisation on S^3
def su2_from_a(a):
    """A = a0 + i a.tau for a (..,4)."""
    return a[..., 0, None, None] * I2 + 1j * np.einsum('...i,ijk->...jk', a[..., 1:], TAU)


def a_from_su2(A):
    a0 = tr(A).real / 2
    ai = np.stack([(tr(TAU[i] @ A) / (2j)).real for i in range(3)], axis=-1)
    return np.concatenate([a0[..., None], ai], axis=-1)


def generator_matrix(side, a_idx, eps=1e-6):
    """Matrix G (4x4) acting on coefficient vectors c of linear wavefunctions psi(A) = c.a, for
    Q psi(A) = -i d/de psi(A') with A' = exp(i e tau_a/2) A (side='L') or A exp(i e tau_a/2) (side='R').
    The map a -> a' is linear: a' = M(e) a, so psi(A') = c.(M a) = (M^T c).a."""
    def Mof(e):
        g = np.cos(e / 2) * I2 + 1j * np.sin(e / 2) * TAU[a_idx]
        M = np.zeros((4, 4))
        for j in range(4):
            aj = np.zeros(4); aj[j] = 1
            A = su2_from_a(aj)
            Ap = g @ A if side == 'L' else A @ g
            M[:, j] = a_from_su2(Ap)
        return M
    dM = (Mof(eps) - Mof(-eps)) / (2 * eps)
    return -1j * dM.T


def R_adj(A):
    """R_ab(A) = (1/2) Tr(tau_a A tau_b A^+)."""
    R = np.zeros(A.shape[:-2] + (3, 3))
    for a in range(3):
        for b in range(3):
            R[..., a, b] = 0.5 * tr(TAU[a] @ A @ TAU[b] @ dag(A)).real
    return R


def quadform_of(fun):
    """Symmetric 4x4 K with fun(a) = a^T K a for a quadratic function fun of real a (4,)."""
    K = np.zeros((4, 4))
    E = np.eye(4)
    for i in range(4):
        K[i, i] = fun(E[i])
    for i in range(4):
        for j in range(i + 1, 4):
            K[i, j] = K[j, i] = 0.5 * (fun(E[i] + E[j]) - K[i, i] - K[j, j])
    return K


def s3_expect(c, K):
    """<psi| a^T K a |psi> / <psi|psi> for psi = c.a, uniform measure on S^3:
    E[a_i a_j a_k a_l] = (d_ij d_kl + d_ik d_jl + d_il d_jk)/24, E[a_i a_j] = d_ij/4."""
    P = np.real(np.outer(np.conj(c), c))
    P = 0.5 * (P + P.T)
    num = (np.trace(P) * np.trace(K) + 2 * np.trace(P @ K)) / 24.0
    den = np.trace(P) / 4.0
    return num / den
