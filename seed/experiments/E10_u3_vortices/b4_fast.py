"""
E10 Route B, B4: numba kernels for b4_axi.Axi (speed only; same discrete functional term by term).
Checked against the numpy reference implementation in b4_axi (b4_checks.py, 'fast vs reference').

Conventions as b4_axi: complex gradients C with dE = Re Tr(C^+ dM); link gradients in A-form (dE = Re Tr(A^+ dU)).
G = diag(0, 1, 0) is hard-wired as 'keep column/row 1' (M G keeps column 1; G M keeps row 1).
"""
import numpy as np
from numba import njit

C16 = np.complex128


@njit(cache=True, inline='always')
def mul(A, B, C):
    for i in range(3):
        for k in range(3):
            C[i, k] = A[i, 0] * B[0, k] + A[i, 1] * B[1, k] + A[i, 2] * B[2, k]


@njit(cache=True, inline='always')
def muld(A, B, C):            # A B^+
    for i in range(3):
        for k in range(3):
            C[i, k] = A[i, 0] * np.conj(B[k, 0]) + A[i, 1] * np.conj(B[k, 1]) + A[i, 2] * np.conj(B[k, 2])


@njit(cache=True, inline='always')
def dmul(A, B, C):            # A^+ B
    for i in range(3):
        for k in range(3):
            C[i, k] = np.conj(A[0, i]) * B[0, k] + np.conj(A[1, i]) * B[1, k] + np.conj(A[2, i]) * B[2, k]


@njit(cache=True, inline='always')
def n2(A):
    s = 0.0
    for i in range(3):
        for k in range(3):
            s += A[i, k].real ** 2 + A[i, k].imag ** 2
    return s


@njit(cache=True)
def herm_nb(x, X):
    """params (N1, N2, 9) -> Hermitian (N1, N2, 3, 3) (u3common basis)."""
    N1, N2 = x.shape[0], x.shape[1]
    for i in range(N1):
        for j in range(N2):
            p = x[i, j]
            X[i, j, 0, 0] = p[0]; X[i, j, 1, 1] = p[1]; X[i, j, 2, 2] = p[2]
            X[i, j, 0, 1] = p[3] - 1j * p[6]; X[i, j, 1, 0] = p[3] + 1j * p[6]
            X[i, j, 0, 2] = p[4] - 1j * p[7]; X[i, j, 2, 0] = p[4] + 1j * p[7]
            X[i, j, 1, 2] = p[5] - 1j * p[8]; X[i, j, 2, 1] = p[5] + 1j * p[8]


@njit(cache=True)
def hgrad_nb(C, g, scale):
    """dE/dx_p = Re Tr(C^+ E_p), times scale, written to g (N1, N2, 9)."""
    N1, N2 = C.shape[0], C.shape[1]
    for i in range(N1):
        for j in range(N2):
            c = C[i, j]
            g[i, j, 0] = scale * c[0, 0].real; g[i, j, 1] = scale * c[1, 1].real; g[i, j, 2] = scale * c[2, 2].real
            g[i, j, 3] = scale * (c[0, 1].real + c[1, 0].real)
            g[i, j, 4] = scale * (c[0, 2].real + c[2, 0].real)
            g[i, j, 5] = scale * (c[1, 2].real + c[2, 1].real)
            g[i, j, 6] = scale * (c[1, 0].imag - c[0, 1].imag)
            g[i, j, 7] = scale * (c[2, 0].imag - c[0, 2].imag)
            g[i, j, 8] = scale * (c[2, 1].imag - c[1, 2].imag)


@njit(cache=True)
def link_adj(X, Ur, Uz, wr, wz, GX, AUr, AUz, dens, want_AU, want_dens):
    """sum_links w |U X(x+mu) U^+ - X(x)|^2 (adds to GX, AU, dens)."""
    Nr, Nz = X.shape[0], X.shape[1]
    T1 = np.empty((3, 3), C16); D = np.empty((3, 3), C16); T2 = np.empty((3, 3), C16); T3 = np.empty((3, 3), C16)
    E = 0.0
    for mu in range(2):
        for i in range(Nr - 1 if mu == 0 else Nr):
            for j in range(Nz if mu == 0 else Nz - 1):
                ip = i + 1 if mu == 0 else i
                jp = j if mu == 0 else j + 1
                if mu == 0:
                    u = Ur[i, j]; w = wr[i, j]
                else:
                    u = Uz[i, j]; w = wz[i, j]
                mul(u, X[ip, jp], T1)
                muld(T1, u, D)
                for a in range(3):
                    for b in range(3):
                        D[a, b] -= X[i, j, a, b]
                dd = w * n2(D)
                E += dd
                if want_dens:
                    dens[i, j] += 0.5 * dd; dens[ip, jp] += 0.5 * dd
                dmul(u, D, T2); mul(T2, u, T3)
                for a in range(3):
                    for b in range(3):
                        GX[ip, jp, a, b] += 2 * w * T3[a, b]
                        GX[i, j, a, b] -= 2 * w * D[a, b]
                if want_AU:
                    mul(D, T1, T2)
                    if mu == 0:
                        for a in range(3):
                            for b in range(3):
                                AUr[i, j, a, b] += 4 * w * T2[a, b]
                    else:
                        for a in range(3):
                            for b in range(3):
                                AUz[i, j, a, b] += 4 * w * T2[a, b]
    return E


@njit(cache=True)
def link_H(H, Ur, Uz, wr, wz, GH, AUr, AUz):
    Nr, Nz = H.shape[0], H.shape[1]
    D = np.empty((3, 3), C16); T2 = np.empty((3, 3), C16)
    E = 0.0
    for mu in range(2):
        for i in range(Nr - 1 if mu == 0 else Nr):
            for j in range(Nz if mu == 0 else Nz - 1):
                ip = i + 1 if mu == 0 else i
                jp = j if mu == 0 else j + 1
                if mu == 0:
                    u = Ur[i, j]; w = wr[i, j]
                else:
                    u = Uz[i, j]; w = wz[i, j]
                mul(u, H[ip, jp], D)
                for a in range(3):
                    for b in range(3):
                        D[a, b] -= H[i, j, a, b]
                E += w * n2(D)
                dmul(u, D, T2)
                for a in range(3):
                    for b in range(3):
                        GH[ip, jp, a, b] += 2 * w * T2[a, b]
                        GH[i, j, a, b] -= 2 * w * D[a, b]
                muld(D, H[ip, jp], T2)
                if mu == 0:
                    for a in range(3):
                        for b in range(3):
                            AUr[i, j, a, b] += 2 * w * T2[a, b]
                else:
                    for a in range(3):
                        for b in range(3):
                            AUz[i, j, a, b] += 2 * w * T2[a, b]
    return E


@njit(cache=True)
def plaq(Ur, Uz, wp, AUr, AUz):
    """sum_p wp (3 - Re Tr(a b c^+ d^+)), a = Ur[i,j], b = Uz[i+1,j], c = Ur[i,j+1], d = Uz[i,j]."""
    Nr1, Nz1 = wp.shape[0], wp.shape[1]
    ab = np.empty((3, 3), C16); dc = np.empty((3, 3), C16); T = np.empty((3, 3), C16); P = np.empty((3, 3), C16)
    E = 0.0
    for i in range(Nr1):
        for j in range(Nz1):
            a = Ur[i, j]; b = Uz[i + 1, j]; c = Ur[i, j + 1]; d = Uz[i, j]
            mul(a, b, ab); mul(d, c, dc)
            muld(ab, dc, P)                     # ab (dc)^+ = a b c^+ d^+
            tr = P[0, 0].real + P[1, 1].real + P[2, 2].real
            cf = wp[i, j]
            E += cf * (3.0 - tr)
            muld(dc, b, T)                      # dc b^+
            for x in range(3):
                for y in range(3):
                    AUr[i, j, x, y] -= cf * T[x, y]
            dmul(a, dc, T)                      # a^+ dc
            for x in range(3):
                for y in range(3):
                    AUz[i + 1, j, x, y] -= cf * T[x, y]
            dmul(d, ab, T)                      # d^+ ab
            for x in range(3):
                for y in range(3):
                    AUr[i, j + 1, x, y] -= cf * T[x, y]
            muld(ab, c, T)                      # ab c^+
            for x in range(3):
                for y in range(3):
                    AUz[i, j, x, y] -= cf * T[x, y]
    return E


@njit(cache=True)
def sites_static_twist(H, P, ws, wm, lam, n, GH, GP):
    """potential ws (lam^2/4)|1 - H H^+|^2 and twist site term wm |P H - n H G|^2."""
    Nr, Nz = H.shape[0], H.shape[1]
    M = np.empty((3, 3), C16); T = np.empty((3, 3), C16); Y = np.empty((3, 3), C16)
    Ep = 0.0; Et = 0.0
    for i in range(Nr):
        for j in range(Nz):
            h = H[i, j]
            muld(h, h, M)
            for a in range(3):
                for b in range(3):
                    M[a, b] = (1.0 if a == b else 0.0) - M[a, b]
            Ep += ws[i, j] * 0.25 * lam * lam * n2(M)
            mul(M, h, T)
            for a in range(3):
                for b in range(3):
                    GH[i, j, a, b] -= lam * lam * ws[i, j] * T[a, b]
            mul(P[i, j], h, Y)
            for a in range(3):
                Y[a, 1] -= n * h[a, 1]
            w = wm[i, j]
            Et += w * n2(Y)
            mul(P[i, j], Y, T)
            for a in range(3):
                T[a, 1] -= n * Y[a, 1]
            for a in range(3):
                for b in range(3):
                    GH[i, j, a, b] += 2 * w * T[a, b]
            muld(Y, h, T)
            for a in range(3):
                for b in range(3):
                    GP[i, j, a, b] += 2 * w * T[a, b]
    return Ep, Et


@njit(cache=True)
def sites_K(X, H, P, ws, wm, s, use_comm, GX, GH, GP, dens, want_grads, want_dens):
    """use_comm: wm |[P, X]|^2 ; always ws |X H + s H G|^2."""
    Nr, Nz = H.shape[0], H.shape[1]
    Z = np.empty((3, 3), C16); T = np.empty((3, 3), C16); T2 = np.empty((3, 3), C16); Y = np.empty((3, 3), C16)
    K = 0.0
    for i in range(Nr):
        for j in range(Nz):
            x = X[i, j]; p = P[i, j]; h = H[i, j]
            d = 0.0
            if use_comm:
                mul(p, x, Z); mul(x, p, T)
                for a in range(3):
                    for b in range(3):
                        Z[a, b] -= T[a, b]
                w = wm[i, j]
                d += w * n2(Z)
                mul(p, Z, T); mul(Z, p, T2)
                for a in range(3):
                    for b in range(3):
                        GX[i, j, a, b] += 2 * w * (T[a, b] - T2[a, b])
                if want_grads:
                    mul(Z, x, T); mul(x, Z, T2)
                    for a in range(3):
                        for b in range(3):
                            GP[i, j, a, b] += 2 * w * (T[a, b] - T2[a, b])
            mul(x, h, Y)
            if s != 0.0:
                for a in range(3):
                    Y[a, 1] += s * h[a, 1]
            w = ws[i, j]
            d += w * n2(Y)
            muld(Y, h, T)
            for a in range(3):
                for b in range(3):
                    GX[i, j, a, b] += 2 * w * T[a, b]
            if want_grads:
                mul(x, Y, T)
                if s != 0.0:
                    for a in range(3):
                        T[a, 1] += s * Y[a, 1]
                for a in range(3):
                    for b in range(3):
                        GH[i, j, a, b] += 2 * w * T[a, b]
            K += d
            if want_dens:
                dens[i, j] += d
    return K


@njit(cache=True)
def expi_from_eig(mu, V, U):
    """U = V diag(exp(i mu)) V^+ for stacks (N1, N2, 3), (N1, N2, 3, 3)."""
    N1, N2 = mu.shape[0], mu.shape[1]
    for i in range(N1):
        for j in range(N2):
            for a in range(3):
                for b in range(3):
                    s = 0j
                    for k in range(3):
                        s += V[i, j, a, k] * np.exp(1j * mu[i, j, k]) * np.conj(V[i, j, b, k])
                    U[i, j, a, b] = s


@njit(cache=True)
def pullback(A, mu, V, scale, g):
    """dE = Re Tr(A^+ dU), U = exp(i X): C with dE = Re Tr(C^+ dX) (Daleckii-Krein, as u3lattice.expi_pullback);
    then g = scale * (dE/dx_p) for X = h W (pass scale = h)."""
    N1, N2 = mu.shape[0], mu.shape[1]
    At = np.empty((3, 3), np.complex128); T = np.empty((3, 3), np.complex128); C = np.empty((1, 1, 3, 3), np.complex128)
    gg = np.empty((1, 1, 9))
    for i in range(N1):
        for j in range(N2):
            v = V[i, j]
            dmul(v, A[i, j], T); mul(T, v, At)
            for a in range(3):
                for b in range(3):
                    d = mu[i, j, a] - mu[i, j, b]; s = mu[i, j, a] + mu[i, j, b]
                    x = 0.5 * d
                    sn = 1.0 if abs(x) < 1e-12 else np.sin(x) / x
                    gam = 1j * np.exp(0.5j * s) * sn
                    At[a, b] = At[a, b] * np.conj(gam)
            mul(v, At, T); muld(T, v, C[0, 0])
            hgrad_nb(C, gg, scale)
            for p in range(9):
                g[i, j, p] = gg[0, 0, p]
