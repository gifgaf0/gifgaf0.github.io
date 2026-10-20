"""
stencil_check.py -- diagnostic for the comparison with Sutcliffe's table (not a pass criterion).

Question: how large is the O(dx^2) error of our link/plaquette lattice energy compared with a standard
second-order centred-difference energy, E_c = C0 h^3 sum_x [ sum_i |D_i phi|^2 + sum_{i<j} |D_i phi x D_j phi|^2 ],
D_i phi = (phi(x+e_i) - phi(x-e_i)) / 2h ?  (Sutcliffe 2007 says only "a finite difference scheme"; we do not
know his stencil.)  Both are evaluated on the same smooth analytic field, the W = Z1/Z0 rational-map field with
the Gaussian profile f = pi exp(-r^2/4), whose continuum energy E = 1.5225976 is known from Gauss-Legendre
quadrature (check_ansatz_energy.json), on the box [-7.5, 7.5]^3 at dx = 0.2, 0.15, 0.1.
Also evaluated on the relaxed dx = 0.1 fields of all runs (same field, two energy functionals).
Writes stencil_check.json.  Usage: NUMBA_NUM_THREADS=1 python3 stencil_check.py   (about 1 minute)
"""
import json
import os
import numpy as np
import fs_lib as fs

HERE = os.path.dirname(os.path.abspath(__file__))
SCRATCH = '/tmp/claude-0/-home-user-gifgaf0-github-io/235fe351-6f97-5895-b3fd-a90496179b3c/scratchpad/E8_fields'
E_QUAD = json.load(open(os.path.join(HERE, 'check_ansatz_energy.json')))['gauss_w2']['E_quadrature'][-1]


def gauss_field(N, L=7.5):
    x, h = fs.grid(N, L)
    X1, X2, X3 = np.meshgrid(x, x, x, indexing='ij')
    rr = np.sqrt(X1 ** 2 + X2 ** 2 + X3 ** 2)
    ff = np.pi * np.exp(-rr ** 2 / 4)
    sf = np.where(rr > 0, np.sin(ff) / np.where(rr > 0, rr, 1), 0.0)
    Z1 = (X1 + 1j * X2) * sf
    Z0 = np.cos(ff) + 1j * X3 * sf
    pq = Z1 * np.conj(Z0); pp = np.abs(Z1) ** 2; qq = np.abs(Z0) ** 2
    p = np.stack([2 * pq.real, 2 * pq.imag, qq - pp], -1) / (pp + qq)[..., None]
    fs.set_boundary(p)
    return p, h


def centred_energy(phi, h):
    """C0 * h^3 * sum over interior points of the centred-difference energy density (slab by slab)."""
    N = phi.shape[0]
    E2 = E4 = 0.0
    for i in range(1, N - 1):
        c = np.s_[1:-1]
        Dx = (phi[i + 1, c, c] - phi[i - 1, c, c]) / (2 * h)
        Dy = (phi[i, 2:, c] - phi[i, :-2, c]) / (2 * h)
        Dz = (phi[i, c, 2:] - phi[i, c, :-2]) / (2 * h)
        E2 += (Dx ** 2).sum() + (Dy ** 2).sum() + (Dz ** 2).sum()
        E4 += sum((np.cross(a, b) ** 2).sum() for a, b in ((Dx, Dy), (Dy, Dz), (Dz, Dx)))
    return fs.C0 * h ** 3 * E2, fs.C0 * h ** 3 * E4


def main():
    out = dict(E_quadrature=E_QUAD, gauss_w2=[])
    for N in (76, 101, 151):
        p, h = gauss_field(N)
        e2, e4 = fs.energy_grad(p, h, np.zeros_like(p), False)
        Elink = fs.C0 * (e2 + e4)
        c2, c4 = centred_energy(p, h)
        Ec = c2 + c4
        rec = dict(h=h, E_link=Elink, E_centred=Ec, rel_err_link=Elink / E_QUAD - 1, rel_err_centred=Ec / E_QUAD - 1,
                   error_ratio_centred_over_link=(Ec - E_QUAD) / (Elink - E_QUAD))
        out['gauss_w2'].append(rec)
        print(f"[gauss w=2] h={h:.3f}: link {Elink:.6f} ({100 * rec['rel_err_link']:+.3f}%)  centred {Ec:.6f} "
              f"({100 * rec['rel_err_centred']:+.3f}%)  error ratio {rec['error_ratio_centred_over_link']:.2f}")
    # relaxed dx = 0.1 fields of all runs: the same field under the two energy functionals
    target = {'Q1_A11': 1.204, 'Q2_A21': 1.967, 'Q3_A31': 2.754, 'Q4_A22': 3.445, 'Q5_K32': 4.095, 'Q6_L22': 4.650, 'Q7_K32': 5.242}
    out['relaxed_dx0p1'] = {}
    for run, Et in target.items():
        ck = os.path.join(SCRATCH, f'{run}_N151.phi.npy')
        if not os.path.exists(ck):
            continue
        p = np.load(ck)
        x, h = fs.grid(151, 7.5)
        e2, e4 = fs.energy_grad(p, h, np.zeros_like(p), False)
        El = fs.C0 * (e2 + e4)
        c2, c4 = centred_energy(p, h)
        out['relaxed_dx0p1'][run] = dict(E_link=El, E_centred=c2 + c4, rel_centred_vs_link=(c2 + c4) / El - 1,
                                         sutcliffe=Et, rel_link_vs_sutcliffe=El / Et - 1, rel_centred_vs_sutcliffe=(c2 + c4) / Et - 1)
        print(f"[relaxed {run}, dx=0.1] link {El:.5f} ({100 * (El / Et - 1):+.2f}% vs table)  centred {c2 + c4:.5f} "
              f"({100 * ((c2 + c4) / Et - 1):+.2f}% vs table {Et})")
    json.dump(out, open(os.path.join(HERE, 'stencil_check.json'), 'w'), indent=1)


if __name__ == '__main__':
    main()
