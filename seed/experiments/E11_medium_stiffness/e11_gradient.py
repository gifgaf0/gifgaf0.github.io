"""
E11 D1/D2: gradient expansion of the unit-model lattice energy (PLAN.md §7) and its numerical check.

Lattice energy (simple cubic, spacing a = 1):
  E_align = J * sum_links (1 - n_x . n_{x+mu})
  E_link  = K * sum_plaquettes (1 - cos(Omega_p / 2)),  Omega_p = signed solid angle of the plaquette's 4 directors

Continuum expansion (derived in REPORT.md §2):
  E_align = J * int [ 1/2 sum_mu |d_mu n|^2  -  1/24 sum_mu |d_mu^2 n|^2 ]  + O(a^6)
  E_link  = K * int [ 1/8 sum_{mu<nu} F_{mu nu}^2 ] + higher order,   F_{mu nu} = n . (d_mu n x d_nu n)

Check (D1): for a smooth Hopf-charge-1 texture of size L, the lattice sums must match the continuum
integrals of the same texture, with relative error falling with L, and agreement to 1 % at small wavenumber.
"""
import numpy as np, json, sys

def hopf_texture(X, Y, Z, L):
    """Localized Hopf-charge-1 texture: rotor U = cos f + i sin f (r_hat . sigma), f = pi exp(-(r/L)^2), n = U sigma_3 U^dag.
    U has degree 1 as a map R^3 -> S^3 and n is its Hopf projection, so the Hopf charge is 1; n -> (0,0,1) like exp(-(r/L)^2)."""
    r = np.sqrt(X * X + Y * Y + Z * Z) + 1e-300
    f = np.pi * np.exp(-(r / L) ** 2)
    c, s = np.cos(f), np.sin(f)
    a0, a1, a2, a3 = c, s * X / r, s * Y / r, s * Z / r        # U = a0 + i (a . sigma)
    # n = U sigma_3 U^dag = rotation of e_z by the SO(3) image of U
    n1 = 2 * (a1 * a3 + a0 * a2)
    n2 = 2 * (a2 * a3 - a0 * a1)
    n3 = a0 ** 2 - a1 ** 2 - a2 ** 2 + a3 ** 2
    return np.stack([n1, n2, n3])

def tri_solid_angle(a, b, c):
    num = np.einsum('i...,i...->...', a, np.cross(b, c, axis=0))
    den = 1 + np.einsum('i...,i...->...', a, b) + np.einsum('i...,i...->...', b, c) + np.einsum('i...,i...->...', c, a)
    return 2 * np.arctan2(num, den)

def lattice_energies(N, L):
    ax = np.arange(N) - (N - 1) / 2
    X, Y, Z = np.meshgrid(ax, ax, ax, indexing='ij')
    n = hopf_texture(X, Y, Z, L)
    Ea = 0.0
    for mu in range(3):
        sl0 = [slice(None)] * 4; sl1 = [slice(None)] * 4
        sl0[mu + 1] = slice(0, N - 1); sl1[mu + 1] = slice(1, N)
        Ea += np.sum(1 - np.sum(n[tuple(sl0)] * n[tuple(sl1)], axis=0))
    El = 0.0; Qsum = 0.0
    for mu, nu in ((0, 1), (0, 2), (1, 2)):
        def sh(dm, dn):
            s = [slice(None)] * 4
            for d in range(3):
                lo = (dm if d == mu else 0) + (dn if d == nu else 0)
                s[d + 1] = slice(lo, N - 1 + lo) if d in (mu, nu) else slice(None)
            return n[tuple(s)]
        n00, n10, n11, n01 = sh(0, 0), sh(1, 0), sh(1, 1), sh(0, 1)
        Om = tri_solid_angle(n00, n10, n11) + tri_solid_angle(n00, n11, n01)
        El += np.sum(1 - np.cos(Om / 2))
    return Ea, El

def continuum_integrals(N, L, sub=4):
    """Integrals of the continuum densities over the same box [-(N-1)/2, (N-1)/2]^3, fine grid, 4th-order FD."""
    h = 1.0 / sub
    half = (N - 1) / 2
    ax = np.arange(-half - 2 * h, half + 2 * h + h / 2, h)
    X, Y, Z = np.meshgrid(ax, ax, ax, indexing='ij')
    n = hopf_texture(X, Y, Z, L)
    def d1(f, ax_):
        return (-np.roll(f, -2, ax_) + 8 * np.roll(f, -1, ax_) - 8 * np.roll(f, 1, ax_) + np.roll(f, 2, ax_)) / (12 * h)
    def d2(f, ax_):
        return (-np.roll(f, -2, ax_) + 16 * np.roll(f, -1, ax_) - 30 * f + 16 * np.roll(f, 1, ax_) - np.roll(f, 2, ax_)) / (12 * h * h)
    D = [d1(n, a + 1) for a in range(3)]
    DD = [d2(n, a + 1) for a in range(3)]
    inner = (slice(None),) + (slice(2, -2),) * 3
    w = np.ones(len(ax) - 4); w[0] = w[-1] = 0.5        # trapezoid on the interior grid
    W = (w[:, None, None] * w[None, :, None] * w[None, None, :]) * h ** 3
    e2 = 0.5 * sum(np.sum(Di ** 2, axis=0) for Di in D)
    e4a = -(1 / 24) * sum(np.sum(Di ** 2, axis=0) for Di in DD)
    F2 = 0
    for mu, nu in ((0, 1), (0, 2), (1, 2)):
        F = np.einsum('i...,i...->...', n, np.cross(D[mu], D[nu], axis=0))
        F2 = F2 + F ** 2
    eF = F2 / 8
    I = lambda dens: float(np.sum(dens[inner[1:]] * W))
    return I(e2), I(e4a), I(eF)

if __name__ == '__main__':
    out = []
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 40
    for L in [float(x) for x in (sys.argv[2:] or ['2', '3', '4', '6'])]:
        Ea, El = lattice_energies(N, L)
        c2, c4a, cF = continuum_integrals(N, L)
        rec = dict(N=N, L=L, lattice_align=Ea, cont_align_2nd=c2, cont_align_2nd_4th=c2 + c4a,
                   relerr_align_2nd=(Ea - c2) / Ea, relerr_align_4th=(Ea - c2 - c4a) / Ea,
                   lattice_link=El, cont_link_F2=cF, relerr_link=(El - cF) / El)
        out.append(rec); print(json.dumps({k: (round(v, 6) if isinstance(v, float) else v) for k, v in rec.items()}), flush=True)
    json.dump(out, open(f'e11_D1_N{N}.json', 'w'), indent=1)
