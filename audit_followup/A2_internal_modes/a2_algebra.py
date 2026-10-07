#!/usr/bin/env python3
"""A2 / DR-A2-2 and DR-A2-3 (first leg): invariant counts by the Molien-Weyl integral, and Watanabe-Murayama counts.

Invariant counts: dim (Sym^d V)^G = integral over G of h_d(eigenvalues of g on V_C), with the Weyl integration formula
for G2 (12 roots, |W| = 12) on its maximal torus, exact quadrature on a uniform grid (the integrand is a trigonometric
polynomial of bounded degree), the U(1) factors integrated the same way and Z3 averaged. T-even counts are taken from
the invariant rings written out explicitly (the Molien count without T is the cross-check of each ring).
Watanabe-Murayama: broken generators = rank of {T_a psi} (as real vectors in R^16); rho_ab = psi^dagger [T_a, T_b] psi;
n_B = rank(rho)/2, n_A = n_BG - 2 n_B.  G2 generators are computed as the derivations of the octonion table.
Locked pre-registration: A2_PREREG.md md5 fd2e95973de02d9a0e6d719cb579ccc0."""
import itertools, json, math, hashlib
import numpy as np
REPO = "/home/claude/gifgaf0.github.io"
assert hashlib.md5(open(REPO + "/audit_followup/A2_internal_modes/A2_PREREG.md", "rb").read()).hexdigest() == "fd2e95973de02d9a0e6d719cb579ccc0"
OUT = {}

# ------------------------------------------------------------------ Molien-Weyl counts
def h_from_power_sums(p, dmax):
    h = [1.0 + 0j]
    for n in range(1, dmax + 1):
        h.append(sum(p[k]*h[n - k] for k in range(1, n + 1))/n)
    return h
def molien_counts(group, space, dmax=8, N=40, NB=24):
    """space: 'R14' (7-sector only) or 'R16'. group: 'a' (G2xU1_global), 'b' (G2xU1_psi0), 'c' (G2xU1_psi0xZ3)."""
    th = 2*np.pi*np.arange(N)/N; be = 2*np.pi*np.arange(NB)/NB
    A, B = np.meshgrid(th, th, indexing="ij")
    w7 = [0*A, A, -A, B, -B, A + B, -(A + B)]                       # weights of the 7 (1 + 3 + 3bar)
    roots = [A, -A, B, -B, A + B, -(A + B), A - B, B - A, 2*A + B, -(2*A + B), A + 2*B, -(A + 2*B)]
    weyl = np.ones_like(A, dtype=complex)
    for r in roots:
        weyl *= (1 - np.exp(1j*r))
    weyl = weyl/12.0                                                  # |W(G2)| = 12
    totals = np.zeros(dmax + 1)
    if group == "a":
        phase_cases = [(bb, bb, 1.0/NB) for bb in be]                # (psi0 phase, 7-sector phase, weight)
    elif group == "b":
        phase_cases = [(bb, 0.0, 1.0/NB) for bb in be]
    else:
        phase_cases = [(bb, 2*np.pi*j/3, 1.0/(3*NB)) for bb in be for j in range(3)]
    for (b0, g7, wt) in phase_cases:
        eig = []
        if space == "R16":
            eig += [np.exp(1j*b0) + 0*A, np.exp(-1j*b0) + 0*A]
        for w in w7:
            eig += [np.exp(1j*(w + g7)), np.exp(1j*(w - g7))]          # 7 (x) (e^{i g} + e^{-i g})
        p = [None] + [sum(e**k for e in eig) for k in range(1, dmax + 1)]
        h = h_from_power_sums(p, dmax)
        for d in range(dmax + 1):
            totals[d] += wt*np.real(np.mean(h[d]*weyl))
    return [int(round(x)) for x in totals], [float(x) for x in totals]
OUT["molien"] = {}
for space in ("R14", "R16"):
    for grp in ("a", "b", "c"):
        cnt, raw = molien_counts(grp, space)
        dev = max(abs(r - c) for r, c in zip(raw, cnt))
        OUT["molien"][f"{space}_{grp}"] = dict(counts_deg0_to_8=cnt, max_rounding_dev=dev)
        print(f"Molien {space} group ({grp}): dims at degree 0..8 = {cnt}   (max |raw - int| = {dev:.1e})")

# ring descriptions (T acts psi -> conj psi): generators and their T-parity; count T-even monomials to degree 6
def ring_count(gens, dmax=6, relations_from=99):
    """gens: list of (degree, T_parity +1/-1). Free polynomial ring (no relation below degree 'relations_from')."""
    cnt_all = [0]*(dmax + 1); cnt_even = [0]*(dmax + 1)
    for exps in itertools.product(*[range(dmax//d + 1) for d, _ in gens]):
        deg = sum(e*d for e, (d, _) in zip(exps, gens))
        if deg > dmax:
            continue
        par = 1
        for e, (_, t) in zip(exps, gens):
            par *= t**e
        cnt_all[deg] += 1
        if par == 1:
            cnt_even[deg] += 1
    return cnt_all, cnt_even
RINGS = {   # degree<=6: no relation among these generators below degree 8 (the first syzygies are in degree 8 and 12)
    "R14_a": [(2, 1), (4, 1)],                                  # N, |S|^2
    "R14_b": [(2, 1), (2, 1), (2, -1)],                         # u.u, v.v, u.v
    "R14_c": [(2, 1), (4, 1), (6, 1), (6, -1)],                 # N, |S|^2, Re S^3, Im S^3
    "R16_a": [(2, 1), (2, 1), (4, 1), (4, 1), (4, -1)],         # |psi0|^2, N, |S|^2, Re psi0^2 Sbar, Im psi0^2 Sbar
    "R16_b": [(2, 1), (2, 1), (2, 1), (2, -1)],                 # |psi0|^2, u.u, v.v, u.v
    "R16_c": [(2, 1), (2, 1), (4, 1), (6, 1), (6, -1)],         # |psi0|^2, N, |S|^2, Re S^3, Im S^3
}
OUT["rings"] = {}
for key, gens in RINGS.items():
    ca, ce = ring_count(gens)
    mol = OUT["molien"][key]["counts_deg0_to_8"][:7]
    OUT["rings"][key] = dict(all=ca, T_even=ce, matches_molien=(ca == mol))
    print(f"ring {key}: all {ca[2]}/{ca[4]}/{ca[6]}  T-even {ce[2]}/{ce[4]}/{ce[6]}  (deg 2/4/6)  matches Molien: {ca == mol}")
    assert ca == mol, key

# ------------------------------------------------------------------ octonions, g2, Watanabe-Murayama
LINES = [(i % 7 + 1, (i + 1) % 7 + 1, (i + 3) % 7 + 1) for i in range(7)]       # {i, i+1, i+3} mod 7, labels 1..7
mult = np.zeros((8, 8, 8))                                                       # e_i e_j = sum_k mult[i,j,k] e_k
for i in range(8):
    mult[0, i, i] = mult[i, 0, i] = 1
for i in range(1, 8):
    mult[i, i, 0] = -1
for (a, b, c) in LINES:
    for (x, y, z) in ((a, b, c), (b, c, a), (c, a, b)):
        mult[x, y, z] = 1; mult[y, x, z] = -1
def omul(x, y):
    return np.einsum("i,j,ijk->k", x, y, mult)
# derivations: D antisymmetric on Im O (7x7), D(e_i e_j) = D(e_i) e_j + e_i D(e_j)
basis_so7 = []
for i in range(7):
    for j in range(i + 1, 7):
        M = np.zeros((7, 7)); M[i, j] = 1; M[j, i] = -1; basis_so7.append(M)
rows = []
for a_ in range(1, 8):
    for b_ in range(1, 8):
        ea = np.eye(8)[a_]; eb = np.eye(8)[b_]
        cols = []
        for M in basis_so7:
            D8 = np.zeros((8, 8)); D8[1:, 1:] = M
            cols.append(D8 @ omul(ea, eb) - omul(D8 @ ea, eb) - omul(ea, D8 @ eb))
        rows.append(np.array(cols).T)
Cmat = np.vstack(rows)
_, s, Vt = np.linalg.svd(Cmat)
null = Vt[np.sum(s > 1e-9):]
g2 = [sum(c*M for c, M in zip(v, basis_so7)) for v in null]
OUT["g2_dimension"] = len(g2)
print(f"derivation algebra of the octonion table: dim = {len(g2)} (g2 expects 14)")
assert len(g2) == 14
# is the table an octonion algebra? (alternative: (x x) y = x (x y))
rng = np.random.default_rng(1)
x, y = rng.normal(size=8), rng.normal(size=8)
assert np.allclose(omul(omul(x, x), y), omul(x, omul(x, y))), "table not alternative"

def gen8(M7=None, phase0=0.0, phase7=0.0, full=None):
    """anti-Hermitian 8x8 generator: real antisymmetric M7 on the 7-sector, i*phase on e0 and/or 7-sector."""
    if full is not None:
        return full
    T = np.zeros((8, 8), complex)
    if M7 is not None:
        T[1:, 1:] = M7
    T[0, 0] += 1j*phase0
    T[1:, 1:] += 1j*phase7*np.eye(7)
    return T
def wm(psi, gens):
    vecs = np.array([np.concatenate([(T @ psi).real, (T @ psi).imag]) for T in gens])
    nbg = int(np.linalg.matrix_rank(vecs, tol=1e-9))
    rho = np.array([[np.vdot(psi, (Ta @ Tb - Tb @ Ta) @ psi) for Tb in gens] for Ta in gens])
    rk = int(np.linalg.matrix_rank(rho, tol=1e-9))
    return dict(n_BG=nbg, rank_rho=rk, n_B=rk//2, n_A=nbg - 2*(rk//2))
so7 = [gen8(M) for M in basis_so7]
g2g = [gen8(M) for M in g2]
u1_0 = gen8(phase0=1.0); u1_7 = gen8(phase7=1.0); u1_glob = gen8(phase0=1.0, phase7=1.0)
u8 = []
for i in range(8):
    for j in range(8):
        if i < j:
            M = np.zeros((8, 8), complex); M[i, j] = 1; M[j, i] = -1; u8.append(M)
            M = np.zeros((8, 8), complex); M[i, j] = 1j; M[j, i] = 1j; u8.append(M)
        elif i == j:
            M = np.zeros((8, 8), complex); M[i, i] = 1j; u8.append(M)
e = np.eye(8, dtype=complex)
u = np.zeros(8); u[1] = 1; v = np.zeros(8); v[2] = 1
VACUA = {
    "P0 (U(8), any direction; here e0)": (e[0], {"U(8) [dynamics of record]": u8}),
    "P0 (U(8), a 7-sector direction)": (e[3], {"U(8) [dynamics of record]": u8}),
    "R (psi = e0)": (e[0], {"G2xU1psi0 [action]": g2g + [u1_0], "SO7xU1psi0xU1_7 [deg<=4 accidental]": so7 + [u1_0, u1_7]}),
    "P7 (psi = e1)": (e[1], {"G2xU1psi0 [action]": g2g + [u1_0], "SO7xU1psi0xU1_7 [deg<=4 accidental]": so7 + [u1_0, u1_7]}),
    "F7 (psi = (e1 + i e2)/sqrt2)": ((e[1] + 1j*e[2])/math.sqrt(2), {"G2xU1psi0 [action]": g2g + [u1_0], "SO7xU1psi0xU1_7 [deg<=4 accidental]": so7 + [u1_0, u1_7]}),
    "I7 (psi = 0.9 e1 + 0.4 i e2)": ((0.9*e[1] + 0.4j*e[2]), {"SO7xU1psi0xU1_7 [deg<=4 accidental]": so7 + [u1_0, u1_7]}),
    "MP (psi = 0.6 e0 + 0.8 e1)": ((0.6*e[0] + 0.8*e[1]), {"SO7xU1psi0xU1_7 [deg<=4 accidental]": so7 + [u1_0, u1_7]}),
    "MF (psi = 0.6 e0 + 0.8 (e1 + i e2)/sqrt2)": ((0.6*e[0] + 0.8*(e[1] + 1j*e[2])/math.sqrt(2)), {"SO7xU1psi0xU1_7 [deg<=4 accidental]": so7 + [u1_0, u1_7]}),
    "MI (psi = 0.6 e0 + 0.7 e1 + 0.3 i e2)": ((0.6*e[0] + 0.7*e[1] + 0.3j*e[2]), {"SO7xU1psi0xU1_7 [deg<=4 accidental]": so7 + [u1_0, u1_7]}),
}
OUT["watanabe_murayama"] = {}
for name, (psi, groups) in VACUA.items():
    psi = psi/np.linalg.norm(psi)
    for gname, gens in groups.items():
        r = wm(psi, gens)
        OUT["watanabe_murayama"][f"{name} | {gname}"] = r
        print(f"WM {name:44s} {gname:38s} n_BG={r['n_BG']:2d} rank(rho)={r['rank_rho']:2d} -> quadratic n_B={r['n_B']}  linear n_A={r['n_A']}")
json.dump(OUT, open(REPO + "/audit_followup/A2_internal_modes/a2_algebra.json", "w"), indent=1, default=float)
print("done")
