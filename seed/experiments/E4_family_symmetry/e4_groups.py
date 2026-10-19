"""
e4_groups.py -- E4 part 1: the groups, their character tables, all irreps in a D-diagonal
basis, Kronecker products, branching rules and Clebsch-Gordan coefficients, checked against
Luhn, Nasri & Ramond (LNR) arXiv:0709.1447 (J. Math. Phys. 48, 123519) and arXiv:0706.2341
(Phys. Lett. B 652, 27).

Run:  python3 e4_groups.py        (about 10 s)
Writes out/groups.json and out/reps.npz (representation matrices used by later scripts).
"""
import json
import math
import os
import sys
import time

import numpy as np

from e4lib import (B7, OMEGA, ZETA, FiniteGroup, XMat, intertwiners, invariants,
                   recognize, recognize_char, seed_generators, xscalar_from_powers, B7_X)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
os.makedirs(OUT, exist_ok=True)
t0 = time.time()
CHECKS = {}


def check(name, ok, detail=""):
    CHECKS[name] = {"pass": bool(ok), "detail": detail}
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  ({detail})" if detail else ""))


# =====================================================================================
# 1. generators, exact relations, and the LNR basis
# =====================================================================================
X = seed_generators()
D, C, Rf = X["D"], X["C"], X["Rf"]
I3 = XMat.identity(3)


def xpow(M, k):
    out = I3
    for _ in range(k):
        out = out @ M
    return out


Cinv = xpow(C, 2)
check("D^7 = 1 (exact)", xpow(D, 7).is_identity())
check("C^3 = 1 (exact)", xpow(C, 3).is_identity())
check("C^-1 D C = D^4 (exact; LNR d^-1 c d = c^4 with c=D, d=C)", (Cinv @ D @ C).key() == xpow(D, 4).key())

# LNR's triplet generators, eqs. (22)-(23) of arXiv:0709.1447, built exactly
def lnr_matrix(entries):
    """entries[i][j] = dict power->coeff, overall factor i/sqrt7."""
    num = np.zeros((3, 3, 7), dtype=np.int64)
    gauss = {1: 1, 2: 1, 4: 1, 3: -1, 5: -1, 6: -1}
    for i in range(3):
        for j in range(3):
            for k1, c1 in entries[i][j].items():
                for k2, c2 in gauss.items():
                    num[i, j, (k1 + k2) % 7] += c1 * c2
    return XMat(num, 1)


A_lnr = lnr_matrix([[{2: 1, 5: -1}, {1: 1, 6: -1}, {4: 1, 3: -1}],
                    [{1: 1, 6: -1}, {4: 1, 3: -1}, {2: 1, 5: -1}],
                    [{4: 1, 3: -1}, {2: 1, 5: -1}, {1: 1, 6: -1}]])          # eq. (23)
B_lnr = lnr_matrix([[{3: 1, 6: -1}, {3: 1, 1: -1}, {1: 1, 0: -1}],
                    [{2: 1, 0: -1}, {6: 1, 5: -1}, {6: 1, 2: -1}],
                    [{5: 1, 4: -1}, {4: 1, 0: -1}, {5: 1, 3: -1}]])          # eq. (22)
check("seed Rf = LNR A^[3] (eq. 23), exactly", Rf.key() == A_lnr.key())
check("LNR B^[3] (eq. 22) = A D exactly, i.e. LNR AB = D", B_lnr.key() == (A_lnr @ D).key())
A, B = A_lnr, B_lnr
AB = A @ B
Ainv, Binv = A, xpow(B, 2)
comm = Ainv @ Binv @ A @ B
check("LNR presentation A^2 = B^3 = (AB)^7 = [A,B]^4 = 1 (exact)",
      xpow(A, 2).is_identity() and xpow(B, 3).is_identity() and xpow(AB, 7).is_identity()
      and xpow(comm, 4).is_identity())
AB2 = A @ B @ B
d_lnr = AB @ AB2 @ AB2 @ AB @ AB @ AB2                       # eq. (63): d = AB (AB^2)^2 (AB)^2 AB^2
check("LNR d (eq. 63) has order 3 and d^-1 c d = c^4 with c = AB = D",
      xpow(d_lnr, 3).is_identity() and (xpow(d_lnr, 2) @ D @ d_lnr).key() == xpow(D, 4).key())

# =====================================================================================
# 2. the groups
# =====================================================================================
F21 = FiniteGroup([D, C])
PSL = FiniteGroup([D, C, Rf])
check("|F21| = |<D,C>| = 21", F21.n == 21)
check("|PSL(2,7) seed copy| = |<D,C,Rf>| = 168", PSL.n == 168)
check("F21 inside the seed PSL(2,7) copy", all(PSL.contains(g) for g in F21.elems))
check("LNR's d is in F21", F21.contains(d_lnr))
# which element is d?
d_desc = None
for a in range(7):
    for k in (1, 2):
        cand = xpow(D, a) @ xpow(C, k) @ xpow(D, (7 - a) % 7)
        if cand.key() == d_lnr.key():
            d_desc = f"D^{a} C^{k} D^-{a}"
print("LNR d =", d_desc)
dC_same_class = F21.class_of[F21.idx(d_lnr)] == F21.class_of[F21.idx(C)]
print("d conjugate to C in F21:", dC_same_class)

# ---------------- F21 classes in LNR order: 1, Theta2(d), Theta3(d^2), Theta4(c), Theta5(c^3)
fD = F21.idx(D)
fd = F21.idx(d_lnr)
f_rep = [0, fd, F21.mt[fd, fd], fD, F21.idx(xpow(D, 3))]
f_cls = [int(F21.class_of[i]) for i in f_rep]
assert len(set(f_cls)) == 5
f_sizes = [len(F21.classes[c]) for c in f_cls]
check("F21 class sizes 1,7,7,3,3 (LNR)", f_sizes == [1, 7, 7, 3, 3], str(f_sizes))

# ---------------- F21 irreps (numeric matrices on all 21 elements)
rep3_F = F21.num.copy()
rep3b_F = np.conj(rep3_F)
N_idx = [F21.idx(xpow(D, a)) for a in range(7)]                      # normal Z7
z3_label = np.zeros(F21.n, dtype=int)
for g in range(F21.n):
    for k in range(3):
        x = g
        for _ in range(k):
            x = F21.mt[x, F21.inv[fd]]
        if x in N_idx:
            z3_label[g] = k
rep1_F = np.ones((F21.n, 1, 1), dtype=complex)
rep1p_F = (OMEGA ** z3_label).reshape(-1, 1, 1).astype(complex)      # chi_1'(d) = w (LNR)
rep1pp_F = np.conj(rep1p_F)
F_IRREPS = {"1": rep1_F, "1'": rep1p_F, "1''": rep1pp_F, "3": rep3_F, "3b": rep3b_F}
for nm, r in F_IRREPS.items():
    check(f"F21 irrep {nm} is a homomorphism", F21.check_hom(r) < 1e-12)


def char_table(G, irreps, cls_order):
    tab = {}
    for nm, r in irreps.items():
        chi = G.char_from_rep(r)
        tab[nm] = [chi[c] for c in cls_order]
    return tab


chiF = char_table(F21, F_IRREPS, f_cls)
sizesF = np.array(f_sizes)
# orthogonality
okF = True
names_F = list(F_IRREPS)
for a in names_F:
    for b in names_F:
        ip = np.sum(sizesF * np.conj(chiF[a]) * chiF[b]) / 21
        okF &= abs(ip - (a == b)) < 1e-12
check("F21 character orthogonality (rows), 5 irreps = 5 classes, sum d^2 = 21",
      okF and sum(int(round(chiF[n][0].real)) ** 2 for n in names_F) == 21)
lnr_F = {"1": [1, 1, 1, 1, 1], "1'": [1, OMEGA, OMEGA ** 2, 1, 1], "1''": [1, OMEGA ** 2, OMEGA, 1, 1],
         "3": [3, 0, 0, B7, np.conj(B7)], "3b": [3, 0, 0, np.conj(B7), B7]}
check("F21 character table = LNR Sec. 5 table (classes 1, 7Th2(d), 7Th3(d^2), 3Th4(c), 3Th5(c^3))",
      all(np.allclose(chiF[n], lnr_F[n]) for n in names_F))
# exact check of the b7 entry: trace of D is exactly b7
check("Tr D = b7 = zeta+zeta^2+zeta^4 exactly", D.trace() == B7_X)

# ---------------- PSL classes in LNR order: 1, A, B, [A,B], AB, AB^2
p_rep = [0, PSL.idx(A), PSL.idx(B), PSL.idx(comm), PSL.idx(AB), PSL.idx(AB2)]
p_cls = [int(PSL.class_of[i]) for i in p_rep]
assert len(set(p_cls)) == 6
p_sizes = [len(PSL.classes[c]) for c in p_cls]
p_orders = [int(PSL.order[i]) for i in p_rep]
check("PSL classes: sizes 1,21,56,42,24,24 with orders 1,2,3,4,7,7 (LNR)",
      p_sizes == [1, 21, 56, 42, 24, 24] and p_orders == [1, 2, 3, 4, 7, 7], f"{p_sizes} {p_orders}")
pD, pC, pR = PSL.idx(D), PSL.idx(C), PSL.idx(Rf)
GENS_P = [pD, pC, pR]
GENS_F = [fD, F21.idx(C)]

# ---------------- PSL irreps
rep3 = PSL.num.copy()
rep3b = np.conj(rep3)
rep1 = np.ones((PSL.n, 1, 1), dtype=complex)
# sextet: symmetric square in LNR's basis, eq. (26): |1}=|11'>,|2}=|22'>,|3}=|33'>,
# |4}=(|12'>+|21'>)/sqrt2, |5}=(|31'>+|13'>)/sqrt2, |6}=(|23'>+|32'>)/sqrt2
K6 = np.zeros((9, 6), dtype=complex)
s = 1 / math.sqrt(2)
for col, terms in enumerate([[(0, 0, 1)], [(1, 1, 1)], [(2, 2, 1)],
                             [(0, 1, s), (1, 0, s)], [(2, 0, s), (0, 2, s)], [(1, 2, s), (2, 1, s)]]):
    for (i, j, c) in terms:
        K6[3 * i + j, col] = c
rep33 = np.einsum("nab,ncd->nacbd", rep3, rep3).reshape(PSL.n, 9, 9)
rep6_lnr = np.einsum("ia,nij,jb->nab", K6.conj(), rep33, K6)
# octet: adjoint in LNR's Gell-Mann basis, eq. (43): |A) = (1/sqrt2) sum (lambda_A)_ij |i>|jbar>
lam = np.zeros((8, 3, 3), dtype=complex)
lam[0][0, 1] = lam[0][1, 0] = 1
lam[1][0, 1], lam[1][1, 0] = -1j, 1j
lam[2][0, 0], lam[2][1, 1] = 1, -1
lam[3][0, 2] = lam[3][2, 0] = 1
lam[4][0, 2], lam[4][2, 0] = -1j, 1j
lam[5][1, 2] = lam[5][2, 1] = 1
lam[6][1, 2], lam[6][2, 1] = -1j, 1j
lam[7] = np.diag([1, 1, -2]) / math.sqrt(3)
K8 = np.array([lam[a].reshape(9) for a in range(8)]).T / math.sqrt(2)     # (9,8): |i>|jbar> coefficients
rep33b = np.einsum("nab,ncd->nacbd", rep3, rep3b).reshape(PSL.n, 9, 9)
rep8_lnr = np.einsum("ia,nij,jb->nab", K8.conj(), rep33b, K8)
for nm, r in (("6 (LNR basis)", rep6_lnr), ("8 (LNR basis)", rep8_lnr)):
    check(f"PSL {nm} is a homomorphism", PSL.check_hom(r) < 1e-10)

chi3 = PSL.char_from_rep(rep3)
chi6 = PSL.char_from_rep(rep6_lnr)
chi8 = PSL.char_from_rep(rep8_lnr)
chi3b = np.conj(chi3)
chi1 = np.ones(len(PSL.classes), dtype=complex)
chi36 = chi3 * chi6
m3b = PSL.inner(chi3b, chi36)
m8 = PSL.inner(chi8, chi36)
chi7 = chi36 - chi3b - chi8
check("3 x 6 contains 3bar and 8 once; remainder chi7 = chi(3x6) - chi(3bar) - chi(8) is irreducible",
      abs(m3b - 1) < 1e-12 and abs(m8 - 1) < 1e-12 and abs(PSL.inner(chi7, chi7) - 1) < 1e-12)
# build the 7 by projection from 3 x 6
rep36 = np.einsum("nab,ncd->nacbd", rep3, rep6_lnr).reshape(PSL.n, 18, 18)
chi7_el = chi7[PSL.class_of]
P7 = 7 / PSL.n * np.einsum("n,nij->ij", np.conj(chi7_el), rep36)
u, sv, vh = np.linalg.svd(P7)
Q7 = u[:, :7]
check("projector onto the 7 has rank 7", np.sum(sv > 1e-8) == 7)
rep7_raw = np.einsum("ia,nij,jb->nab", Q7.conj(), rep36, Q7)
check("PSL 7 is a homomorphism", PSL.check_hom(rep7_raw) < 1e-10)


def adapt_basis(rep, iD, iC, iR, label_1p_by_C):
    """Rewrite rep in a D-diagonal basis adapted to F21 = <D,C>:
    blocks [1, 1', 1'', 3 (weights 1,2,4), 3bar (weights 6,5,3)] in which D and C act
    exactly as in the standard F21 irreps.  Phases: first block vector's largest component
    real positive; each later block's first vector chosen so that <first|rho(Rf)|v_b> > 0
    (if that entry vanishes, a later block is used as reference)."""
    dim = rep.shape[1]
    w, V = np.linalg.eig(rep[iD])
    wt = np.round(np.angle(w) / (2 * np.pi) * 7).astype(int) % 7
    spaces = {k: V[:, wt == k] for k in range(7)}
    for k in range(7):
        if spaces[k].shape[1]:
            q, _ = np.linalg.qr(spaces[k])
            spaces[k] = q
    blocks = []
    E0 = spaces[0]
    if E0.shape[1]:
        Cr = E0.conj().T @ rep[iC] @ E0
        cw, cv = np.linalg.eig(Cr)
        for target, name in ((1, "1"), (label_1p_by_C, "1'"), (np.conj(label_1p_by_C), "1''")):
            sel = np.where(np.abs(cw - target) < 1e-8)[0]
            for s_ in sel:
                v = E0 @ cv[:, s_]
                blocks.append((name, [v / np.linalg.norm(v)]))
    for k in range(spaces[1].shape[1]):
        v1 = spaces[1][:, k]
        blocks.append(("3", [v1, rep[iC] @ rep[iC] @ v1, rep[iC] @ v1]))
    for k in range(spaces[6].shape[1]):
        v6 = spaces[6][:, k]
        blocks.append(("3b", [v6, rep[iC] @ rep[iC] @ v6, rep[iC] @ v6]))
    # phases
    first = blocks[0][1][0]
    j = int(np.argmax(np.abs(first)))
    ph = np.conj(first[j]) / abs(first[j])
    blocks[0] = (blocks[0][0], [v * ph for v in blocks[0][1]])
    ref = blocks[0][1][0]
    for b in range(1, len(blocks)):
        vb = blocks[b][1][0]
        amp = ref.conj() @ rep[iR] @ vb
        if abs(amp) < 1e-8:
            for bb in range(1, b):
                amp = blocks[bb][1][0].conj() @ rep[iR] @ vb
                if abs(amp) > 1e-8:
                    break
        ph = np.conj(amp) / abs(amp) if abs(amp) > 1e-8 else 1.0
        blocks[b] = (blocks[b][0], [v * ph for v in blocks[b][1]])
    U = np.column_stack([v for _, vs in blocks for v in vs])
    assert U.shape == (dim, dim)
    assert np.allclose(U.conj().T @ U, np.eye(dim), atol=1e-10)
    new = np.einsum("ia,nij,jb->nab", U.conj(), rep, U)
    return new, [nm for nm, _ in blocks], U


# 1' is defined by chi_1'(d) = w; if d is conjugate to C then chi_1'(C) = w too
label_C = OMEGA if dC_same_class else OMEGA ** 2
rep6, blocks6, U6 = adapt_basis(rep6_lnr, pD, pC, pR, label_C)
rep7, blocks7, U7 = adapt_basis(rep7_raw, pD, pC, pR, label_C)
rep8, blocks8, U8 = adapt_basis(rep8_lnr, pD, pC, pR, label_C)
P_IRREPS = {"1": rep1, "3": rep3, "3b": rep3b, "6": rep6, "7": rep7, "8": rep8}
for nm, r in P_IRREPS.items():
    check(f"PSL irrep {nm}: homomorphism in the F21-adapted D-diagonal basis", PSL.check_hom(r) < 1e-10)
check("F21 branching from the explicit bases: 6 = 3+3bar, 7 = 1+3+3bar, 8 = 1'+1''+3+3bar",
      blocks6 == ["3", "3b"] and blocks7 == ["1", "3", "3b"] and blocks8 == ["1'", "1''", "3", "3b"],
      f"6:{blocks6} 7:{blocks7} 8:{blocks8}")
# D and C act exactly as the standard F21 matrices on each block
def std_block(nm, g):
    return {"1": rep1_F, "1'": rep1p_F, "1''": rep1pp_F, "3": rep3_F, "3b": rep3b_F}[nm][F21.idx(g)]


okb = True
for r, bl in ((rep6, blocks6), (rep7, blocks7), (rep8, blocks8)):
    for g, gi in ((D, pD), (C, pC)):
        blk = [std_block(nm, g) for nm in bl]
        Mstd = np.zeros_like(r[gi])
        o = 0
        for b in blk:
            dd = b.shape[0]
            Mstd[o:o + dd, o:o + dd] = b
            o += dd
        okb &= np.allclose(r[gi], Mstd, atol=1e-10)
check("in the 6, 7, 8 bases D and C are block-diagonal standard F21 matrices", okb)

chiP = char_table(PSL, P_IRREPS, p_cls)
names_P = list(P_IRREPS)
sizesP = np.array(p_sizes)
okP = all(abs(np.sum(sizesP * np.conj(chiP[a]) * chiP[b]) / 168 - (a == b)) < 1e-10
          for a in names_P for b in names_P)
check("PSL character orthogonality, 6 irreps = 6 classes, sum d^2 = 168",
      okP and sum(int(round(chiP[n][0].real)) ** 2 for n in names_P) == 168)
b7, b7c = B7, np.conj(B7)
lnr_P = {"1": [1, 1, 1, 1, 1, 1], "3": [3, -1, 0, 1, b7, b7c], "3b": [3, -1, 0, 1, b7c, b7],
         "6": [6, 2, 0, 0, -1, -1], "7": [7, -1, 1, -1, 0, 0], "8": [8, 0, -1, 0, 1, 1]}
check("PSL character table = LNR Sec. 3 table", all(np.allclose(chiP[n], lnr_P[n]) for n in names_P))

# =====================================================================================
# 3. Kronecker products
# =====================================================================================
def decompose(G, chi_prod_el, irreps_chi_el):
    out = {}
    for nm, ch in irreps_chi_el.items():
        m = np.sum(np.conj(ch) * chi_prod_el) / G.n
        mi = int(round(m.real))
        assert abs(m - mi) < 1e-9
        if mi:
            out[nm] = mi
    return out


def chis_el(G, irreps):
    return {nm: np.trace(r, axis1=1, axis2=2) for nm, r in irreps.items()}


def sym_antisym(G, chi_el):
    sq = np.array([chi_el[G.mt[g, g]] for g in range(G.n)])
    return (chi_el ** 2 + sq) / 2, (chi_el ** 2 - sq) / 2


def fmt(dec):
    return " + ".join((f"{m}x" if m > 1 else "") + nm for nm, m in dec.items())


kron = {}
for Gname, G, irreps in (("F21", F21, F_IRREPS), ("PSL", PSL, P_IRREPS)):
    ce = chis_el(G, irreps)
    names = list(irreps)
    tab = {}
    for i, a in enumerate(names):
        for b in names[i:]:
            if a == "1" or b == "1":
                continue
            key = f"{a} x {b}"
            if a == b:
                s_, a_ = sym_antisym(G, ce[a])
                tab[key] = {"sym": decompose(G, s_, ce), "antisym": decompose(G, a_, ce)}
            else:
                tab[key] = decompose(G, ce[a] * ce[b], ce)
    kron[Gname] = tab
    print(f"--- {Gname} Kronecker products")
    for k, v in tab.items():
        if "sym" in v:
            print(f"  {k} = ({fmt(v['sym'])})_s + ({fmt(v['antisym'])})_a")
        else:
            print(f"  {k} = {fmt(v)}")

# LNR tables (bars restored: the PDF text drops them; restored by conjugation symmetry and
# dimension, see REPORT.md)
lnr_kron_F = {"1' x 1'": {"1''": 1}, "1' x 1''": {"1": 1}, "1' x 3": {"3": 1}, "1' x 3b": {"3b": 1},
              "3 x 3": {"sym": {"3": 1, "3b": 1}, "antisym": {"3b": 1}},
              "3 x 3b": {"1": 1, "1'": 1, "1''": 1, "3": 1, "3b": 1}}
lnr_kron_P = {"3 x 3": {"sym": {"6": 1}, "antisym": {"3b": 1}}, "3 x 3b": {"1": 1, "8": 1},
              "3 x 6": {"3b": 1, "7": 1, "8": 1}, "3b x 6": {"3": 1, "7": 1, "8": 1},
              "3 x 7": {"6": 1, "7": 1, "8": 1}, "3b x 7": {"6": 1, "7": 1, "8": 1},
              "3 x 8": {"3": 1, "6": 1, "7": 1, "8": 1}, "3b x 8": {"3b": 1, "6": 1, "7": 1, "8": 1},
              "6 x 6": {"sym": {"1": 1, "6": 2, "8": 1}, "antisym": {"7": 1, "8": 1}},
              "6 x 7": {"3": 1, "3b": 1, "6": 1, "7": 2, "8": 2},
              "6 x 8": {"3": 1, "3b": 1, "6": 2, "7": 2, "8": 2},
              "7 x 7": {"sym": {"1": 1, "6": 2, "7": 1, "8": 1}, "antisym": {"3": 1, "3b": 1, "7": 1, "8": 1}},
              "7 x 8": {"3": 1, "3b": 1, "6": 2, "7": 2, "8": 3},
              "8 x 8": {"sym": {"1": 1, "6": 2, "7": 1, "8": 2}, "antisym": {"3": 1, "3b": 1, "7": 2, "8": 1}}}
def _flat(v):
    if isinstance(v, dict) and "sym" in v and not v["antisym"]:
        return v["sym"]
    return v


okKF = all(_flat(kron["F21"][k]) == v for k, v in lnr_kron_F.items())
check("F21 Kronecker products = LNR (3x3 = (3+3bar)_s + 3bar_a; 3x3bar = 1+1'+1''+3+3bar; 1'x1' = 1''; ...)", okKF)
okKP = all(kron["PSL"][k] == v for k, v in lnr_kron_P.items())
bad = [k for k, v in lnr_kron_P.items() if kron["PSL"][k] != v]
check("PSL(2,7) Kronecker products = LNR table (all 14 entries)", okKP, f"mismatch: {bad}" if bad else "")

# =====================================================================================
# 4. branching rules
# =====================================================================================
# PSL -> F21 (restriction to the F21 elements)
f_in_p = [PSL.idx(g) for g in F21.elems]
ceF = chis_el(F21, F_IRREPS)
branch_PF = {}
for nm, r in P_IRREPS.items():
    chi_res = np.trace(r[f_in_p], axis1=1, axis2=2)
    branch_PF[nm] = decompose(F21, chi_res, ceF)
lnr_PF = {"1": {"1": 1}, "3": {"3": 1}, "3b": {"3b": 1}, "6": {"3": 1, "3b": 1},
          "7": {"1": 1, "3": 1, "3b": 1}, "8": {"1'": 1, "1''": 1, "3": 1, "3b": 1}}
check("PSL(2,7) -> F21 branching = LNR (6=3+3bar, 7=1+3+3bar, 8=1'+1''+3+3bar)", branch_PF == lnr_PF,
      str(branch_PF))


# SU(3) -> PSL via Jacobi-Trudi characters on the eigenvalues of each element
def schur_char(eigs, p, q):
    lam_ = (p + q, q, 0)
    def h(k):
        if k < 0:
            return 0
        tot = 0
        for a in range(k + 1):
            for b in range(k - a + 1):
                tot += eigs[0] ** a * eigs[1] ** b * eigs[2] ** (k - a - b)
        return tot
    M = np.array([[h(lam_[i] - i + j) for j in range(3)] for i in range(3)], dtype=complex)
    return np.linalg.det(M)


eig_el = [np.linalg.eigvals(m) for m in PSL.num]
ceP = chis_el(PSL, P_IRREPS)
su3 = {"(1,0)": (1, 0), "(0,1)": (0, 1), "(2,0)": (2, 0), "(0,2)": (0, 2), "(1,1)": (1, 1),
       "(3,0)": (3, 0), "(2,1)": (2, 1), "(4,0)": (4, 0), "(0,5)": (0, 5), "(1,3)": (1, 3), "(2,2)": (2, 2)}
branch_SU3 = {}
for nm, (p, q) in su3.items():
    chi = np.array([schur_char(e, p, q) for e in eig_el])
    dim = int(round(chi[0].real))
    branch_SU3[nm] = {"dim": dim, "decomp": decompose(PSL, chi, ceP)}
# LNR table (dimension content as printed; the PDF loses bars, so the 3/3bar labels are checked
# only up to conjugation)
lnr_SU3 = {"(1,0)": [3], "(0,1)": [3], "(2,0)": [6], "(0,2)": [6], "(1,1)": [8], "(3,0)": [3, 7],
           "(2,1)": [7, 8], "(4,0)": [1, 6, 8], "(0,5)": [3, 3, 7, 8], "(1,3)": [3, 6, 7, 8], "(2,2)": [6, 6, 7, 8]}
dimof = {"1": 1, "3": 3, "3b": 3, "6": 6, "7": 7, "8": 8}
okSU = all(sorted(sum([[dimof[k]] * m for k, m in branch_SU3[n]["decomp"].items()], [])) == sorted(v)
           for n, v in lnr_SU3.items())
check("SU(3) -> PSL(2,7) branching dimensions = LNR table (11 irreps up to (2,2))", okSU,
      "; ".join(f"{n}:{fmt(branch_SU3[n]['decomp'])}" for n in su3))

# LNR sextet/octet/septet conventions
D6_lnr = rep6_lnr[pD]
check("LNR eq. (33): A^[6]B^[6] = diag(eta^2, eta^4, eta, eta^3, eta^5, eta^6) in LNR's sextet basis",
      np.allclose(D6_lnr, np.diag(ZETA ** np.array([2, 4, 1, 3, 5, 6]))))
check("LNR: Tr A^[6] = 2", abs(np.trace(rep6_lnr[pR]) - 2) < 1e-12)
Cmat = np.zeros((6, 6))
for (i, j) in ((0, 4), (1, 3), (2, 5)):
    Cmat[i, j] = Cmat[j, i] = 1
check("LNR eq. (38): C (15,24,36 entries) is the invariant bilinear of the sextet: g^T C g = C",
      all(np.allclose(rep6_lnr[g].T @ Cmat @ rep6_lnr[g], Cmat) for g in GENS_P))
c1, c2, c3 = (math.cos(2 * n * math.pi / 7) for n in (1, 2, 3))
s1, s2, s3 = (math.sin(2 * n * math.pi / 7) for n in (1, 2, 3))
D8_expected = np.zeros((8, 8))
for (a, b, c_, s_) in ((0, 1, c1, s1), (3, 4, c3, s3), (5, 6, c2, s2)):
    D8_expected[a, a] = D8_expected[b, b] = c_
    D8_expected[a, b], D8_expected[b, a] = s_, -s_
D8_expected[2, 2] = D8_expected[7, 7] = 1
check("LNR eq. (45): (AB)^[8] in the Gell-Mann basis is the block rotation (c1,s1 | 1 | c3,s3 | c2,s2 | 1), "
      "printed in LNR's row convention (eq. 28: A|i> = sum_m a_im |m>), i.e. the transpose of our column-convention matrix",
      np.allclose(rep8_lnr[pD].T, D8_expected, atol=1e-12) and not np.allclose(rep8_lnr[pD], D8_expected, atol=1e-12))
check("LNR eq. (54): (AB)^[7] has eigenvalues 1, eta, ..., eta^6 (our 7 basis is D-diagonal)",
      np.allclose(rep7[pD], np.diag(np.diag(rep7[pD])), atol=1e-10)
      and sorted((np.round(np.angle(np.diag(rep7[pD])) / (2 * np.pi) * 7).astype(int) % 7).tolist()) == list(range(7)))
check("A^[8] (LNR basis) real symmetric with (A^[8])^2 = 1 (LNR below eq. 46)",
      np.allclose(rep8_lnr[pR].imag, 0, atol=1e-12) and np.allclose(rep8_lnr[pR], rep8_lnr[pR].T)
      and np.allclose(rep8_lnr[pR] @ rep8_lnr[pR], np.eye(8)))
# LNR A^[8], eq. (46), all 64 entries (times 1/7), as read from the PDF text after removing the
# extensible-bracket glyphs "0 1 B C @ A" that pdftotext mixes into the first and last columns
r3_ = math.sqrt(3)
A8_lnr = np.array([
    [2 - 2 * c1, 0, 2 * c1 + 2 * c2 - 4 * c3, 2 - 2 * c2, 0, 2 - 2 * c3, 0, 2 * r3_ * (c1 - c2)],
    [0, -2 - 2 * c1 + 4 * c2, 0, 0, 2 + 2 * c2 - 4 * c3, 0, -2 + 4 * c1 - 2 * c3, 0],
    [2 * c1 + 2 * c2 - 4 * c3, 0, -c1 + 2 * c2 - c3, -4 * c1 + 2 * c2 + 2 * c3, 0, 2 * c1 - 4 * c2 + 2 * c3, 0, r3_ * (c1 - c3)],
    [2 - 2 * c2, 0, -4 * c1 + 2 * c2 + 2 * c3, 2 - 2 * c3, 0, 2 - 2 * c1, 0, 2 * r3_ * (c2 - c3)],
    [0, 2 + 2 * c2 - 4 * c3, 0, 0, -2 + 4 * c1 - 2 * c3, 0, 2 + 2 * c1 - 4 * c2, 0],
    [2 - 2 * c3, 0, 2 * c1 - 4 * c2 + 2 * c3, 2 - 2 * c1, 0, 2 - 2 * c2, 0, 2 * r3_ * (c3 - c1)],
    [0, -2 + 4 * c1 - 2 * c3, 0, 0, 2 + 2 * c1 - 4 * c2, 0, -2 - 2 * c2 + 4 * c3, 0],
    [2 * r3_ * (c1 - c2), 0, r3_ * (c1 - c3), 2 * r3_ * (c2 - c3), 0, 2 * r3_ * (c3 - c1), 0, c1 - 2 * c2 + c3]]) / 7
check("LNR eq. (46): all 64 entries of A^[8] (Gell-Mann basis) reproduced",
      np.allclose(rep8_lnr[pR].real, A8_lnr, atol=1e-12), f"max dev {np.max(np.abs(rep8_lnr[pR].real - A8_lnr)):.1e}")

# =====================================================================================
# 5. Clebsch-Gordan coefficients in the D-diagonal basis
# =====================================================================================
def tensor_rep(r1, r2):
    n, d1, _ = r1.shape
    d2 = r2.shape[1]
    return np.einsum("nab,ncd->nacbd", r1, r2).reshape(n, d1 * d2, d1 * d2)


def swap_op(d):
    S = np.zeros((d * d, d * d))
    for i in range(d):
        for j in range(d):
            S[d * j + i, d * i + j] = 1
    return S


def cg_split(src, tgt, gens, same=None):
    """Intertwiners src -> tgt as columns; if same=d, split into symmetric / antisymmetric."""
    Ks = intertwiners(src, tgt, gens)
    if same is None or len(Ks) == 0:
        return {"": Ks}
    S = swap_op(same)
    out = {"s": [], "a": []}
    for sign, key in ((1, "s"), (-1, "a")):
        cand = [(K + sign * S @ K) / 2 for K in Ks]
        # independent ones
        M = np.array([c.ravel() for c in cand])
        u, sv, vh = np.linalg.svd(M)
        r = int(np.sum(sv > 1e-8))
        for k in range(r):
            K = vh[k].conj().reshape(Ks[0].shape) if False else None
        # orthonormal basis of the span, mapped back to intertwiner shape
        Q, _ = np.linalg.qr(M.T)
        for k in range(r):
            out[key].append(Q[:, k].reshape(Ks[0].shape))
    return out


def normalize_cg(K):
    """Normalize so that K^dagger K = 1 (isometry) and make the first nonzero entry real positive."""
    K = K / math.sqrt(np.real(np.trace(K.conj().T @ K)) / K.shape[1])
    flat = K.T.ravel()
    j = int(np.argmax(np.abs(flat) > 1e-9))
    return K * (np.conj(flat[j]) / abs(flat[j]))


def cg_table(K, d1, d2, lab1="i", lab2="j'"):
    """Human-readable: target component -> sum of coefficient |i>|j'>."""
    rows = []
    for t in range(K.shape[1]):
        terms = []
        for i in range(d1):
            for j in range(d2):
                c = K[d1 * 0 + i * d2 + j, t]
                if abs(c) > 1e-9:
                    terms.append(f"{recognize(c)} |{i + 1}>|{j + 1}'>")
        rows.append(" + ".join(terms))
    return rows


cg = {}
print("--- F21 Clebsch-Gordan coefficients (D-diagonal basis; 3: weights (1,2,4), 3bar: (6,5,3))")
F33 = tensor_rep(rep3_F, rep3_F)
F33b = tensor_rep(rep3_F, rep3b_F)
cgF = {}
for tgt in ("3", "3b"):
    res = cg_split(F33, F_IRREPS[tgt], GENS_F, same=3)
    for sa, Ks in res.items():
        for k, K in enumerate(Ks):
            K = normalize_cg(K)
            cgF[f"3x3 -> {tgt}_{sa}"] = cg_table(K, 3, 3)
for tgt in ("1", "1'", "1''", "3", "3b"):
    Ks = intertwiners(F33b, F_IRREPS[tgt], GENS_F)
    for K in Ks:
        cgF[f"3x3bar -> {tgt}"] = cg_table(normalize_cg(K), 3, 3)
for k, v in cgF.items():
    print(f"  {k}:")
    for comp, row in enumerate(v):
        print(f"      component {comp + 1}: {row}")
cg["F21"] = cgF


# LNR's F21 CG vectors, eqs. (64)-(66), checked as intertwiners (convention-free check)
def is_intertwiner(K, src, tgt, gens):
    return all(np.allclose(src[g] @ K, K @ tgt[g], atol=1e-10) for g in gens)


def vec(terms, d1=3, d2=3):
    v = np.zeros(d1 * d2, dtype=complex)
    for (i, j, c) in terms:
        v[(i - 1) * d2 + (j - 1)] += c
    return v


h = 1 / math.sqrt(2)
r3 = 1 / math.sqrt(3)
lnr_cg = {
    "(3x3)_s -> 3": [[(3, 3, 1)], [(1, 1, 1)], [(2, 2, 1)]],
    "(3x3)_s -> 3bar": [[(3, 2, h), (2, 3, h)], [(1, 3, h), (3, 1, h)], [(2, 1, h), (1, 2, h)]],
    "(3x3)_a -> 3bar": [[(3, 2, h), (2, 3, -h)], [(1, 3, h), (3, 1, -h)], [(2, 1, h), (1, 2, -h)]],
    "3x3bar -> 3": [[(2, 1, 1)], [(3, 2, 1)], [(1, 3, 1)]],
    "3x3bar -> 3bar": [[(1, 2, 1)], [(2, 3, 1)], [(3, 1, 1)]],
    "3x3bar -> 1": [[(1, 1, r3), (2, 2, r3), (3, 3, r3)]],
    "3x3bar -> 1'": [[(1, 1, r3), (2, 2, r3 * OMEGA ** 2), (3, 3, r3 * OMEGA)]],
    "3x3bar -> 1''": [[(1, 1, r3), (2, 2, r3 * OMEGA), (3, 3, r3 * OMEGA ** 2)]],
}
tgt_of = {"3": rep3_F, "3bar": rep3b_F, "1": rep1_F, "1'": rep1p_F, "1''": rep1pp_F}
lnr_cg_ok = {}
lnr_cg_ok_row = {}
for k, comps in lnr_cg.items():
    K = np.column_stack([vec(c) for c in comps])
    src = F33 if "3x3bar" not in k else F33b
    tgt = tgt_of[k.split("-> ")[1]]
    lnr_cg_ok[k] = bool(is_intertwiner(K, src, tgt, GENS_F))
    # LNR's row convention (eq. 28): coefficient vectors transform with the transposed matrices
    lnr_cg_ok_row[k] = bool(all(np.allclose(src[g].T @ K, K @ tgt[g].T, atol=1e-10) for g in GENS_F))
check("LNR F21 Clebsch-Gordan coefficients (eqs. 64-66) are intertwiners in LNR's own row convention "
      "(eq. 28), with the seed matrices (component order as printed)", all(lnr_cg_ok_row.values()), str(lnr_cg_ok_row))
check("in the column convention used here the same holds except that LNR's 1' and 1'' singlet "
      "combinations exchange (omega <-> omega^2); all triplet CGs agree in both conventions",
      all(v for k, v in lnr_cg_ok.items() if "1'" not in k) and not lnr_cg_ok["3x3bar -> 1'"]
      and not lnr_cg_ok["3x3bar -> 1''"]
      and is_intertwiner(np.column_stack([vec(c) for c in lnr_cg["3x3bar -> 1'"]]), F33b, rep1pp_F, GENS_F)
      and is_intertwiner(np.column_stack([vec(c) for c in lnr_cg["3x3bar -> 1''"]]), F33b, rep1p_F, GENS_F))

print("--- PSL(2,7) Clebsch-Gordan coefficients, multiplicities from explicit intertwiners")
cgP_mult = {}
pairs = [("3", "3"), ("3", "3b"), ("3", "6"), ("3", "7"), ("3", "8"), ("3b", "6"), ("6", "6"),
         ("6", "7"), ("7", "7"), ("7", "8"), ("8", "8"), ("6", "8")]
CG_STORE = {}
okmult = True
for a, b in pairs:
    T = tensor_rep(P_IRREPS[a], P_IRREPS[b])
    for tgt in names_P:
        Ks = intertwiners(T, P_IRREPS[tgt], GENS_P)
        if Ks:
            cgP_mult[f"{a} x {b} -> {tgt}"] = len(Ks)
            CG_STORE[f"PSL|{a}|{b}|{tgt}"] = np.stack([normalize_cg(K) for K in Ks])
        key = f"{a} x {b}" if f"{a} x {b}" in kron["PSL"] else f"{b} x {a}"
        kv = kron["PSL"][key]
        expected = (kv["sym"].get(tgt, 0) + kv["antisym"].get(tgt, 0)) if "sym" in kv else kv.get(tgt, 0)
        okmult &= (len(Ks) == expected)
check("PSL intertwiner counts (explicit null spaces) equal character multiplicities for 12 products", okmult)
K = CG_STORE["PSL|3|3|3b"][0]
print("  3x3 -> 3bar (antisymmetric, epsilon tensor):")
for row in cg_table(K, 3, 3):
    print("     ", row)
K = CG_STORE["PSL|3|3|6"][0]
print("  3x3 -> 6 (first components, F21-adapted basis):")
for row in cg_table(K, 3, 3)[:6]:
    print("     ", row)
eps_ok = True
Keps = np.zeros((9, 3), dtype=complex)
for (i, j, k_, sgn) in ((1, 2, 0, 1), (2, 0, 1, 1), (0, 1, 2, 1), (2, 1, 0, -1), (0, 2, 1, -1), (1, 0, 2, -1)):
    Keps[3 * i + j, k_] = sgn / math.sqrt(2)
check("PSL 3x3 -> 3bar is the epsilon tensor (as in SU(3))",
      is_intertwiner(Keps, tensor_rep(rep3, rep3), rep3b, GENS_P))
check("PSL 3x3bar -> 8 via Gell-Mann matrices (LNR eq. 43/44) is an intertwiner onto LNR's 8",
      is_intertwiner(K8, tensor_rep(rep3, rep3b), rep8_lnr, GENS_P))
check("PSL 3x3 -> 6 via LNR eq. (26) is an intertwiner onto LNR's 6",
      is_intertwiner(K6, tensor_rep(rep3, rep3), rep6_lnr, GENS_P))
# reality: 6, 7, 8 real (Frobenius-Schur indicator +1), 3 complex (0)
fs = {}
for nm, r in P_IRREPS.items():
    chi_sq = np.array([np.trace(r[PSL.mt[g, g]]) for g in range(PSL.n)])
    fs[nm] = int(round(np.real(np.sum(chi_sq)) / PSL.n))
fsF = {}
for nm, r in F_IRREPS.items():
    chi_sq = np.array([np.trace(r[F21.mt[g, g]]) for g in range(F21.n)])
    fsF[nm] = int(round(np.real(np.sum(chi_sq)) / F21.n))
check("Frobenius-Schur indicators: PSL 3,3bar complex (0); 1,6,7,8 real (+1); F21 3,3bar,1',1'' complex",
      fs == {"1": 1, "3": 0, "3b": 0, "6": 1, "7": 1, "8": 1} and fsF == {"1": 1, "1'": 0, "1''": 0, "3": 0, "3b": 0},
      f"PSL {fs} F21 {fsF}")

# =====================================================================================
# 6. save
# =====================================================================================
np.savez_compressed(os.path.join(OUT, "reps.npz"),
                    **{f"F21_{k}": v for k, v in F_IRREPS.items()},
                    **{f"PSL_{k}": v for k, v in P_IRREPS.items()},
                    F21_mt=F21.mt, PSL_mt=PSL.mt, F21_order=F21.order, PSL_order=PSL.order,
                    F21_gens=np.array(GENS_F), PSL_gens=np.array(GENS_P), F21_in_PSL=np.array(f_in_p),
                    PSL_class_of=PSL.class_of, F21_class_of=F21.class_of,
                    **{k.replace("|", "__"): v for k, v in CG_STORE.items()})


def cstr(z):
    return recognize_char(complex(z))


res = {
    "conventions": {
        "zeta": "exp(2 pi i/7)", "omega": "exp(2 pi i/3)", "b7": "(-1+i sqrt7)/2 = zeta+zeta^2+zeta^4",
        "D": "diag(zeta, zeta^2, zeta^4)", "C": "[[0,1,0],[0,0,1],[1,0,0]]",
        "Rf": "flip R flip^-1 (hexagon_check.py) = LNR A^[3] exactly",
        "LNR_d": d_desc, "d_conjugate_to_C": bool(dC_same_class),
        "basis": "3: D-weights (1,2,4); 3bar: (6,5,3); 6,7,8: F21-adapted D-diagonal blocks "
                 "[1,1',1'',3,3bar] with D, C standard on each block",
        "1prime": "chi_1'(d) = omega (LNR); d is conjugate to C, so chi_1'(C) = omega",
        "F21_classes": ["1", "7 Theta2(d)", "7 Theta3(d^2)", "3 Theta4(c=D)", "3 Theta5(c^3)"],
        "PSL_classes": ["1", "21 C2(A)", "56 C3(B)", "42 C4([A,B])", "24 C5(AB=D)", "24 C6(AB^2)"],
    },
    "orders": {"F21": F21.n, "PSL": PSL.n},
    "char_table_F21": {n: [cstr(z) for z in chiF[n]] for n in names_F},
    "char_table_PSL": {n: [cstr(z) for z in chiP[n]] for n in names_P},
    "kronecker_F21": kron["F21"], "kronecker_PSL": kron["PSL"],
    "branching_PSL_to_F21": branch_PF,
    "branching_SU3_to_PSL": branch_SU3,
    "frobenius_schur": {"PSL": fs, "F21": fsF},
    "cg_F21": cg["F21"],
    "cg_PSL_multiplicities": cgP_mult,
    "lnr_cg_intertwiner_checks_column": lnr_cg_ok, "lnr_cg_intertwiner_checks_row": lnr_cg_ok_row,
    "checks": CHECKS,
    "all_pass": all(v["pass"] for v in CHECKS.values()),
    "runtime_s": round(time.time() - t0, 1),
}
with open(os.path.join(OUT, "groups.json"), "w") as f:
    json.dump(res, f, indent=1, default=str)
print(f"\n{sum(v['pass'] for v in CHECKS.values())}/{len(CHECKS)} checks pass; runtime {time.time() - t0:.1f} s")
sys.exit(0 if res["all_pass"] else 1)
