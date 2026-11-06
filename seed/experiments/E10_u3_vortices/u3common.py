"""
E10 Route B (B2/B3): shared helpers for the U(3) single-coupling model (PREREG_B2B3 §1).

Hermitian 3x3 matrices are carried as 9 real parameters x_p in the basis E_p:
  p = 0,1,2 : e_aa
  p = 3,4,5 : e_ab + e_ba            for (a,b) = (0,1),(0,2),(1,2)
  p = 6,7,8 : -i e_ab + i e_ba        for the same pairs
so X = sum_p x_p E_p.  If dE = Re Tr(C^dagger dX) for a (complex) matrix C, then dE/dx_p = Re Tr(C^dagger E_p).
"""
import numpy as np

PAIRS = ((0, 1), (0, 2), (1, 2))
EB = np.zeros((9, 3, 3), complex)
for _a in range(3):
    EB[_a, _a, _a] = 1.0
for _i, (_a, _b) in enumerate(PAIRS):
    EB[3 + _i, _a, _b] = 1.0; EB[3 + _i, _b, _a] = 1.0
    EB[6 + _i, _a, _b] = -1j; EB[6 + _i, _b, _a] = 1j
# metric Re Tr(E_p E_q)
METRIC = np.real(np.einsum('pab,qba->pq', EB, EB))


def herm(x):
    """(..., 9) real -> (..., 3, 3) Hermitian."""
    return np.einsum('...p,pab->...ab', x, EB)


def herm_params(X):
    """(..., 3, 3) Hermitian -> (..., 9) real (inverse of herm)."""
    out = np.empty(X.shape[:-2] + (9,))
    for a in range(3):
        out[..., a] = X[..., a, a].real
    for i, (a, b) in enumerate(PAIRS):
        out[..., 3 + i] = X[..., a, b].real
        out[..., 6 + i] = -X[..., a, b].imag
    return out


def herm_grad(C):
    """dE = Re Tr(C^dagger dX)  ->  dE/dx_p = Re Tr(C^dagger E_p)."""
    return np.real(np.einsum('...ba,pba->...p', C.conj(), EB))


def dag(X):
    return np.conj(np.swapaxes(X, -1, -2))


def fro2(X):
    return np.sum(np.abs(X) ** 2)


def rot12(alpha):
    """Global SU(3)_{C+F} element V with V e_1 = (cos a, sin a, 0)."""
    c, s = np.cos(alpha), np.sin(alpha)
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]], complex)


G_DIAG = np.diag([0.0, 1.0, 0.0]).astype(complex)       # PREREG §3: G = diag(0, 1, 0)


def m_bulk(lam):
    return min(1.0, lam)


# B1 / Eto 0810.4895 Table 1 targets (PREREG §2)
C1_TARGET = {0.8: 0.91231, 1.0: 1.00000, 1.2: 1.07922}
C2_TARGET = {0.8: 1.77407, 1.0: 2.00000, 1.2: 2.20944}
LAMBDAS = (0.8, 1.0, 1.2)
