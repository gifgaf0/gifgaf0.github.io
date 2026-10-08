#!/usr/bin/env python3
"""
m_magnetic_moments.py -- C2 batch, math_B leg, item (m): quark-model magnetic moments, exact.

Independent computation (no other script consulted).  sympy, exact rationals.

Space: three quarks, each in C^2 (flavour u, d) (x) C^2 (spin up, down); total dimension 4^3 = 64.
Colour is totally antisymmetric and suppressed, so the spin (x) flavour part must be totally
symmetric under the 6 permutations of the three quarks (SU(6) quark model).

States are DEFINED as joint eigenvectors (no hand-written wavefunctions):
  nucleon N(spin 1/2, M = +1/2):  totally symmetric, S^2 = 3/4, S_z = 1/2, n_u = 2 (p) or 1 (n)
  Delta (spin 3/2, M = +3/2):     totally symmetric, S^2 = 15/4, S_z = 3/2, n_u = 3, 2, 1, 0
Each defining system has a 1-dimensional solution space (checked).  Isospin is then checked
(I^2 = 3/4 for N, 15/4 for Delta) as a consistency test, not imposed.

Magnetic-moment operator: mu_hat = sum_i mu_{q_i} sigma_z^(i), i.e. mu_u on a u quark, mu_d on a d quark.
Reported: mu_p, mu_n, mu(Delta^{++,+,0,-}); in the proton <sum over u quarks sigma_z> and <sigma_z(d)>;
and the values at mu_u = -2 mu_d.
"""
import itertools
import sympy as sp

mu_u, mu_d = sp.symbols("mu_u mu_d")

# single-quark basis: index = 2*f + s,  f: 0 = u, 1 = d;  s: 0 = up, 1 = down
I2 = sp.eye(2)
sx = sp.Matrix([[0, 1], [1, 0]])
sy = sp.Matrix([[0, -sp.I], [sp.I, 0]])
sz = sp.Matrix([[1, 0], [0, -1]])
Pu = sp.Matrix([[1, 0], [0, 0]])
Pd = sp.Matrix([[0, 0], [0, 1]])


def kron(*ms):
    out = ms[0]
    for m in ms[1:]:
        out = sp.kronecker_product(out, m)
    return out


def one_quark(flav_op, spin_op, i):
    """operator acting as flav_op (x) spin_op on quark i (0,1,2), identity elsewhere."""
    single = kron(flav_op, spin_op)  # 4x4, index 2*f + s
    facs = [sp.eye(4)] * 3
    facs = list(facs)
    facs[i] = single
    return kron(*facs)


DIM = 64
labels = []
for q in itertools.product(range(4), repeat=3):
    labels.append("".join(("u" if x // 2 == 0 else "d") + ("^" if x % 2 == 0 else "v") for x in q))


def perm_op(perm):
    """permute the three tensor factors: |q0 q1 q2> -> |q_perm^-1 ...> (position i goes to perm[i])."""
    M = sp.zeros(DIM, DIM)
    for idx, q in enumerate(itertools.product(range(4), repeat=3)):
        newq = [None] * 3
        for i in range(3):
            newq[perm[i]] = q[i]
        jdx = newq[0] * 16 + newq[1] * 4 + newq[2]
        M[jdx, idx] = 1
    return M


SZ = [one_quark(I2, sz, i) for i in range(3)]
SX = [one_quark(I2, sx, i) for i in range(3)]
SY = [one_quark(I2, sy, i) for i in range(3)]
PU = [one_quark(Pu, I2, i) for i in range(3)]
PD = [one_quark(Pd, I2, i) for i in range(3)]
TX = [one_quark(sx, I2, i) for i in range(3)]
TY = [one_quark(sy, I2, i) for i in range(3)]
TZ = [one_quark(sz, I2, i) for i in range(3)]

Sx = sum(SX, sp.zeros(DIM)) / 2
Sy = sum(SY, sp.zeros(DIM)) / 2
Sz = sum(SZ, sp.zeros(DIM)) / 2
S2 = Sx * Sx + Sy * Sy + Sz * Sz
Ix = sum(TX, sp.zeros(DIM)) / 2
Iy = sum(TY, sp.zeros(DIM)) / 2
Iz = sum(TZ, sp.zeros(DIM)) / 2
I2op = Ix * Ix + Iy * Iy + Iz * Iz
Nu = sum(PU, sp.zeros(DIM))
SWAP01 = perm_op((1, 0, 2))
SWAP12 = perm_op((0, 2, 1))
ALLPERMS = [perm_op(p) for p in itertools.permutations(range(3))]
SYM = sum(ALLPERMS, sp.zeros(DIM)) / 6

MU = sum(((mu_u * PU[i] + mu_d * PD[i]) * SZ[i] for i in range(3)), sp.zeros(DIM))
SZU = sum((PU[i] * SZ[i] for i in range(3)), sp.zeros(DIM))  # sum of sigma_z over u quarks
SZD = sum((PD[i] * SZ[i] for i in range(3)), sp.zeros(DIM))  # sum of sigma_z over d quarks
EYE = sp.eye(DIM)


def state(s2, sz_val, nu):
    A = sp.Matrix.vstack(SWAP01 - EYE, SWAP12 - EYE, S2 - s2 * EYE, Sz - sz_val * EYE, Nu - nu * EYE)
    ns = A.nullspace()
    assert len(ns) == 1, f"solution space dimension {len(ns)}"
    v = ns[0]
    # clear denominators, fix sign so the first nonzero entry is positive
    den = sp.ilcm(*[sp.fraction(x)[1] for x in v])
    v = v * den
    g = 0
    for x in v:
        g = sp.igcd(g, int(x))
    v = v / g
    first = next(x for x in v if x != 0)
    if first < 0:
        v = -v
    return v


def expval(v, O):
    return sp.simplify((v.T * O * v)[0, 0] / (v.T * v)[0, 0])


def show(v):
    terms = [f"{int(v[i]):+d}|{labels[i]}>" for i in range(DIM) if v[i] != 0]
    return " ".join(terms) + f"   (norm^2 = {int((v.T * v)[0, 0])})"


def main():
    print("=" * 78)
    print("ITEM (m) -- quark-model magnetic moments, exact (math_B leg)")
    print("=" * 78)
    print(f"dimension of the 3-quark spin(x)flavour space: {DIM}")
    print(f"rank of the total symmetrizer (dim of the totally symmetric subspace): {SYM.rank()}")
    # decomposition of the symmetric subspace by (S, I)
    B = SYM.columnspace()
    Bm = sp.Matrix.hstack(*B)
    # S^2 and I^2 restricted (they commute with permutations)
    S2r = (Bm.T * Bm).inv() * Bm.T * S2 * Bm
    I2r = (Bm.T * Bm).inv() * Bm.T * I2op * Bm
    print(f"eigenvalues of S^2 on the symmetric subspace: {S2r.eigenvals()}")
    print(f"eigenvalues of I^2 on the symmetric subspace: {I2r.eigenvals()}")
    print(f"S^2 and I^2 commute on it: {sp.simplify(S2r * I2r - I2r * S2r) == sp.zeros(S2r.rows)}")
    # joint (S, I) content: dimension of {S^2 = a, I^2 = b}
    for a in (sp.Rational(3, 4), sp.Rational(15, 4)):
        for b in (sp.Rational(3, 4), sp.Rational(15, 4)):
            M = sp.Matrix.vstack(S2r - a * sp.eye(S2r.rows), I2r - b * sp.eye(S2r.rows))
            print(f"   dim(sym; S^2 = {a}, I^2 = {b}) = {len(M.nullspace())}")

    p = state(sp.Rational(3, 4), sp.Rational(1, 2), 2)
    n = state(sp.Rational(3, 4), sp.Rational(1, 2), 1)
    print("\nproton (spin up):  ", show(p))
    print("neutron (spin up): ", show(n))
    print(f"   proton  I^2 = {expval(p, I2op)}, I_z = {expval(p, Iz)}, S^2 = {expval(p, S2)}, S_z = {expval(p, Sz)}")
    print(f"   neutron I^2 = {expval(n, I2op)}, I_z = {expval(n, Iz)}")
    # proton is an exact eigenvector of I^2 (not only in expectation)
    print(f"   I^2 p == (3/4) p exactly: {I2op * p == sp.Rational(3, 4) * p};  I^2 n == (3/4) n: {I2op * n == sp.Rational(3, 4) * n}")

    mup = sp.factor(expval(p, MU))
    mun = sp.factor(expval(n, MU))
    print(f"\nmu_p = {mup}")
    print(f"mu_n = {mun}")
    print(f"   in the proton: <sum over u quarks sigma_z> = {expval(p, SZU)}, <sigma_z(d)> = {expval(p, SZD)}")
    print(f"   in the neutron: <sum over d quarks sigma_z> = {expval(n, SZD)}, <sigma_z(u)> = {expval(n, SZU)}")

    deltas = {}
    for name, nu in (("Delta++ (uuu)", 3), ("Delta+  (uud)", 2), ("Delta0  (udd)", 1), ("Delta-  (ddd)", 0)):
        v = state(sp.Rational(15, 4), sp.Rational(3, 2), nu)
        deltas[name] = v
        print(f"\n{name} (S = 3/2, M = 3/2): {show(v)}")
        print(f"   I^2 = {expval(v, I2op)}; mu = {sp.factor(expval(v, MU))};"
              f" <sum_u sigma_z> = {expval(v, SZU)}, <sum_d sigma_z> = {expval(v, SZD)}")

    sub = {mu_u: -2 * mu_d}
    print("\nat mu_u = -2 mu_d:")
    print(f"   mu_p = {sp.simplify(mup.subs(sub))},  mu_n = {sp.simplify(mun.subs(sub))},"
          f"  mu_p/mu_n = {sp.simplify(mup.subs(sub) / mun.subs(sub))}")
    for name, v in deltas.items():
        print(f"   mu({name.split()[0]}) = {sp.simplify(expval(v, MU).subs(sub))}")
    print("\ngeneral ratio mu_p/mu_n =", sp.simplify(mup / mun))
    print("check against closed forms:",
          sp.simplify(mup - (4 * mu_u - mu_d) / 3) == 0, sp.simplify(mun - (4 * mu_d - mu_u) / 3) == 0,
          sp.simplify(expval(deltas['Delta0  (udd)'], MU) - (mu_u + 2 * mu_d)) == 0)


if __name__ == "__main__":
    main()
