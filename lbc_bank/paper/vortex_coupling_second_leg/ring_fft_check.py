r"""Independent numerical check of the ring formula: build the real-space (core-regularized)
Biot-Savart velocity field on a 3D grid, FFT it, compare zhat.v(q) with
   2 pi kappa R J1(q_perp R) q_perp/q^2 * [q delta K1(q delta)]   (last factor = core regularization).
"""
import numpy as np
from scipy.special import j1, k1
import sys, time

R, kappa, delta = 1.0, 2 * np.pi, 0.3
def run(L, N, nseg=256):
    t0 = time.time()
    dx = L / N
    xs = -L / 2 + dx * np.arange(N)
    X, Y, Z = np.meshgrid(xs, xs, xs, indexing='ij')
    vx = np.zeros_like(X); vy = np.zeros_like(X); vz = np.zeros_like(X)
    ph = 2 * np.pi * (np.arange(nseg) + 0.5) / nseg
    dph = 2 * np.pi / nseg
    for p in ph:
        cx, cy = R * np.cos(p), R * np.sin(p)
        lx, ly = -R * np.sin(p) * dph, R * np.cos(p) * dph      # dl (lz = 0)
        rx, ry, rz = X - cx, Y - cy, Z
        f = (kappa / (4 * np.pi)) / (rx * rx + ry * ry + rz * rz + delta**2)**1.5
        # dl x r = (ly rz - 0*ry, 0*rx - lx rz, lx ry - ly rx)
        vx += ly * rz * f
        vy += -lx * rz * f
        vz += (lx * ry - ly * rx) * f
    k = np.fft.fftfreq(N, d=dx) * 2 * np.pi
    phase = np.exp(-1j * k * (-L / 2))
    def ft(a):
        F = np.fft.fftn(a) * dx**3
        return F * phase[:, None, None] * phase[None, :, None] * phase[None, None, :]
    Fx, Fy, Fz = ft(vx), ft(vy), ft(vz)
    print(f"L={L}, N={N}, dx={dx:.4f}, build+FFT {time.time()-t0:.1f}s")
    for idx in [(1, 0, 0), (2, 0, 0), (3, 0, 0), (4, 0, 0), (0, 0, 1), (0, 0, 2), (0, 0, 3), (0, 0, 4), (1, 0, 1), (2, 0, 2), (3, 0, 3), (2, 1, 1)]:
        i, j, l = idx
        qv = np.array([k[i], k[j], k[l]]); qn = np.linalg.norm(qv); qp = np.hypot(qv[0], qv[1])
        vnum = np.array([Fx[i, j, l], Fy[i, j, l], Fz[i, j, l]])
        exact_z = (2 * np.pi * kappa * R * j1(qp * R) * qp / qn**2) * (qn * delta * k1(qn * delta))
        small = np.pi * kappa * R**2 * (qp / qn)**2
        print(f"  n={idx} qR={qn*R:.3f} sin^2={(qp/qn)**2:.3f}: zhat.v FFT={vnum[2].real:+.5f}"
              f" (Im {abs(vnum[2].imag):.1e})  exact={exact_z:+.5f}  small-qR={small:+.5f}"
              f"  rel.err={abs(vnum[2].real-exact_z)/max(abs(exact_z),1e-12):.2e}  |q.v|/|v|q={abs(qv@vnum)/(np.linalg.norm(vnum)*qn+1e-30):.1e}")
    sys.stdout.flush()

run(24.0, 128)
# run(30.0, 160)  # second box: same lowest-mode (L-independent) truncation offset; see ring_fft_check.out history
