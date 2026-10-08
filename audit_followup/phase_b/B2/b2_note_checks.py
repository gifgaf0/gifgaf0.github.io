#!/usr/bin/env python3
"""B2: checks of statements in the attached note (PSL27_Spectral_Rigidity_corrected_v2_1.docx) that v3 touches or relies on."""
import itertools
import numpy as np
P = {1: (1,0,0), 2: (0,1,0), 3: (0,0,1), 4: (1,1,0), 5: (1,0,1), 6: (0,1,1), 7: (1,1,1)}
name = {v: k for k, v in P.items()}
def act(M, v):
    return tuple(int(x) % 2 for x in (np.array(M) @ np.array(v)))
lines = [frozenset(t) for t in itertools.combinations(range(1, 8), 3)
         if all((P[t[0]][i] + P[t[1]][i] + P[t[2]][i]) % 2 == 0 for i in range(3))]
assert len(lines) == 7
L = {"L1": frozenset({2,3,6}), "L2": frozenset({2,5,7}), "L3": frozenset({3,4,7}), "L4": frozenset({4,5,6})}
assert all(l in lines for l in L.values()) and all(1 not in l for l in L.values())
g1 = [[1,0,0],[0,0,1],[0,1,0]]; g2 = [[1,1,0],[0,1,1],[0,0,1]]
def on_lines(M):
    img = {}
    for k, l in L.items():
        im = frozenset(name[act(M, P[p])] for p in l)
        img[k] = [kk for kk, ll in L.items() if ll == im][0]
    return img
def order(M):
    A = np.array(M) % 2; X = A.copy(); k = 1
    while not np.array_equal(X % 2, np.eye(3, dtype=int)):
        X = (X @ A) % 2; k += 1
    return k
g1g2 = (np.array(g1) @ np.array(g2)) % 2
print("g1 fixes P1:", act(g1, P[1]) == P[1], "| g2 fixes P1:", act(g2, P[2]) is not None and act(g2, P[1]) == P[1])
print("orders: g1", order(g1), "g2", order(g2), "g1g2", order(g1g2), "| g1g2 =", g1g2.tolist())
print("g1 on lines:", on_lines(g1))
print("g2 on lines:", on_lines(g2))
# compose as permutations: (g1 g2)(L) = g1(g2(L))
p1, p2 = on_lines(g1), on_lines(g2)
prod = {k: p1[p2[k]] for k in L}
print("g1g2 on lines (apply g2 then g1):", prod)
# group generated: size and isomorphism to S4 via faithful action on the 4 lines
def mat_key(M): return tuple(int(x) for x in (np.array(M) % 2).flatten())
G = {mat_key(np.eye(3, dtype=int))}; frontier = [np.eye(3, dtype=int)]
while frontier:
    new = []
    for X in frontier:
        for g in (g1, g2):
            Y = (X @ np.array(g)) % 2
            if mat_key(Y) not in G:
                G.add(mat_key(Y)); new.append(Y)
    frontier = new
print("|<g1,g2>| =", len(G), "| all fix P1:", all(act(np.array(k).reshape(3,3), P[1]) == P[1] for k in G))
# Appendix A: h1, h2 flag stabilizer
h1 = [[1,1,0],[0,1,0],[0,0,1]]; h2 = [[1,0,0],[0,1,1],[0,0,1]]
h1h2 = (np.array(h1) @ np.array(h2)) % 2
print("Appendix A: h1h2 =", h1h2.tolist(), "order", order(h1h2), "| h2h1 =", ((np.array(h2) @ np.array(h1)) % 2).tolist())
L124 = frozenset({1,2,4})
print("h1, h2 preserve L124:", all(frozenset(name[act(h, P[p])] for p in L124) == L124 for h in (h1, h2)))
# Section 4.1: full-group Laplacian eigenvalues with S = class 2A: 1 - chi(2A)/dim
chi2A = {"rho1": (1, 1), "rho3": (3, -1), "rho3'": (3, -1), "rho6": (6, 2), "rho7": (7, -1), "rho8": (8, 0)}
from fractions import Fraction as F
ev = {k: 1 - F(c, d) for k, (d, c) in chi2A.items()}
print("Delta^G eigenvalues:", {k: str(v) for k, v in ev.items()}, "| rho7-rho6 =", ev["rho7"] - ev["rho6"], "| rho8-rho6 =", ev["rho8"] - ev["rho6"])
