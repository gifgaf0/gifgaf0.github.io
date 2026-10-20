#!/usr/bin/env python3
"""
E3 extra: SU(3) content of the low G2 multiplets (G2 -> SU(3), the stabiliser of e_6), from
explicit representation matrices: the su(3) Casimir (Gell-Mann normalisation, C2(3) = 4/3,
C2(8) = 3, C2(6) = 10/3, C2(10) = 6, C2(15) = 16/3, C2(27) = 8) restricted to each G2 irrep
inside 7, 14, Sym^2 7, 7 x 14, Sym^2 14, Lambda^2 14.  Also the hypercharge-isospin content of the
J = 1 rotor state (the 14), to show where SU(3) octets sit inside the G2 spectrum.
Writes su3_branching_results.json.
"""
import json
import numpy as np

alg = np.load("g2_basis.npz")
basis, TG = alg["basis"], alg["TG"]
G = list(basis)
adT = lambda T: np.array([[-np.trace((T @ b - b @ T) @ a) for b in G] for a in G])
I7, I14 = np.eye(7), np.eye(14)
SU3_C2 = {0.0: "1", 4 / 3: "3+3bar", 3.0: "8", 10 / 3: "6+6bar", 6.0: "10+10bar", 16 / 3: "15+15bar", 8.0: "27",
          28 / 3: "15'+15'bar", 25 / 3: "24+24bar", 12.0: "35+35bar", 15.0: "28+28bar", 31 / 3: "21+21bar", 9: "?"}
SU3_DIM = {"1": 1, "3+3bar": 3, "8": 8, "6+6bar": 6, "10+10bar": 10, "15+15bar": 15, "27": 27, "15'+15'bar": 15,
           "24+24bar": 24, "35+35bar": 35, "28+28bar": 28, "21+21bar": 21}


def sym_proj(n, sign):
    P = np.zeros((n * n, n * n))
    for i in range(n):
        for j in range(n):
            P[i * n + j, i * n + j] += 0.5
            P[j * n + i, i * n + j] += 0.5 * sign
    w, V = np.linalg.eigh(P)
    return V[:, w > 0.5]


def rep_factory(kind):
    if kind == "7":
        return lambda T: T
    if kind == "14":
        return adT
    if kind == "7x14":
        return lambda T: np.kron(T, I14) + np.kron(I7, adT(T))
    gen, sign = {"Sym2(7)": ("7", 1), "Sym2(14)": ("14", 1), "Lam2(14)": ("14", -1)}[kind]
    n = 7 if gen == "7" else 14
    Q = sym_proj(n, sign)
    base = (lambda T: T) if gen == "7" else adT
    return lambda T: Q.T @ (np.kron(base(T), np.eye(n)) + np.kron(np.eye(n), base(T))) @ Q


out = {}
for kind in ["7", "14", "Sym2(7)", "7x14", "Sym2(14)", "Lam2(14)"]:
    R = rep_factory(kind)
    C = -sum(R(g) @ R(g) for g in G)
    C = 0.5 * (C + C.T)
    C3 = -sum(R(t) @ R(t) for t in TG)
    C3 = 0.5 * (C3 + C3.T)
    w, V = np.linalg.eigh(C)
    for c in sorted(set(np.round(w, 6))):
        Vc = V[:, np.abs(w - c) < 1e-5]
        d = Vc.shape[1]
        e3 = np.linalg.eigvalsh(Vc.T @ C3 @ Vc)
        content = {}
        for val in sorted(set(np.round(e3, 6))):
            mult = int(np.sum(np.abs(e3 - val) < 1e-5))
            key = min(SU3_C2, key=lambda k: abs(k - val))
            name = SU3_C2[key] if abs(key - val) < 1e-5 else f"C2={val}"
            dim = SU3_DIM.get(name, 1)
            dd = dim * (2 if "bar" in name else 1)
            content[name] = mult // dd
        label = f"G2 irrep dim {d}, C2 = {c:g}"
        if label not in out:
            out[label] = content
            print(f"{label:28s} -> SU(3): " + " + ".join(f"{v} x {k}" if v > 1 else k for k, v in content.items()))
with open("su3_branching_results.json", "w") as fh:
    json.dump(out, fh, indent=1)
