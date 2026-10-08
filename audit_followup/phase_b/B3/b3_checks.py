#!/usr/bin/env python3
"""B3 checks (explicit computation, no tables consulted).

(1) F7* and PSL(2,7). Paper VII §3.4 and calculator v1.9 state "F7* = {1,...,6} ⊂ PSL(2,7), F7* ≅ Z6".
    Check: the element orders of PSL(2,7); the diagonal torus of SL(2,7) and its image in PSL(2,7);
    the stabilizer of a non-collinear triple (a "Fano triangle") in GL(3,2) ≅ PSL(2,7).
(2) The L column. Arithmetic behind the convention finding: the trefoil per diameter vs per radius, the
    Denne–Diao–Sullivan lower bound in both conventions, and the up-quark output if its L were per radius.
"""
import itertools, json, math

# ---------- (1a) PSL(2,7) as 2x2 matrices over F7 modulo ±I
p = 7
def mul2(a, b):
    return ((a[0]*b[0] + a[1]*b[2]) % p, (a[0]*b[1] + a[1]*b[3]) % p,
            (a[2]*b[0] + a[3]*b[2]) % p, (a[2]*b[1] + a[3]*b[3]) % p)
SL = [m for m in itertools.product(range(p), repeat=4) if (m[0]*m[3] - m[1]*m[2]) % p == 1]
I2 = (1, 0, 0, 1)
def order(m, mul, ident, proj=None):
    k, x = 1, m
    while (x if proj is None else proj(x)) != ident:
        x = mul(x, m); k += 1
    return k
def canon(m):  # representative of {m, -m}
    return min(m, tuple((-v) % p for v in m))
PSL = sorted({canon(m) for m in SL})
ord_psl = {}
for m in PSL:
    o = order(m, mul2, I2, proj=canon)
    ord_psl[o] = ord_psl.get(o, 0) + 1
torus = [(a, 0, 0, pow(a, p - 2, p)) for a in range(1, p)]          # diag(a, a^-1) in SL(2,7)
torus_orders = sorted(order(t, mul2, I2) for t in torus)
torus_image = sorted({canon(t) for t in torus})
gen = (3, 0, 0, 5)                                                   # diag(3, 5): 3 is a generator of F7*
res1 = {
    "SL(2,7) order": len(SL), "PSL(2,7) order": len(PSL),
    "PSL(2,7) element orders {order: count}": dict(sorted(ord_psl.items())),
    "PSL(2,7) has an element of order 6": 6 in ord_psl,
    "SL(2,7) diagonal torus: element orders": torus_orders,
    "order of diag(3,5) in SL(2,7)": order(gen, mul2, I2),
    "image of the torus in PSL(2,7): size": len(torus_image),
}

# ---------- (1b) GL(3,2) on the Fano plane PG(2,2): stabilizer of a non-collinear triple
def mul3(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(3)) % 2 for j in range(3)) for i in range(3))
def det3(m):
    return (m[0][0]*(m[1][1]*m[2][2] - m[1][2]*m[2][1]) - m[0][1]*(m[1][0]*m[2][2] - m[1][2]*m[2][0])
            + m[0][2]*(m[1][0]*m[2][1] - m[1][1]*m[2][0])) % 2
GL = [m for m in (tuple(tuple(r[i*3:(i+1)*3]) for i in range(3)) for r in itertools.product((0, 1), repeat=9))
      if det3(m) == 1]
pts = [v for v in itertools.product((0, 1), repeat=3) if any(v)]
def act(m, v):
    return tuple(sum(m[i][k] * v[k] for k in range(3)) % 2 for i in range(3))
def collinear(a, b, c):
    return tuple((x + y) % 2 for x, y in zip(a, b)) == c
triangles = [t for t in itertools.combinations(pts, 3) if not collinear(*t)]
T = {(1, 0, 0), (0, 1, 0), (0, 0, 1)}
stab = [m for m in GL if {act(m, v) for v in T} == T]
perms = {tuple(sorted(T).index(act(m, v)) for v in sorted(T)) for m in stab}
abelian = all(mul3(a, b) == mul3(b, a) for a in stab for b in stab)
I3 = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
stab_orders = sorted(order(m, mul3, I3) for m in stab)
res2 = {
    "GL(3,2) order": len(GL), "points": len(pts), "non-collinear triples (triangles)": len(triangles),
    "|Stab(triangle)|": len(stab), "Stab abelian": abelian, "Stab element orders": stab_orders,
    "permutations of the three points realized": len(perms), "Stab ≅ S3 (all 6 permutations, faithful)": len(perms) == 6 and len(stab) == 6,
}

# ---------- (2) the L column
L_tref_D = 16.372                       # the calculator's up-quark L
L_tref_R_PP2014 = 32.7429345            # Przybył & Pierański 2014, per tube radius
DDS_D = 15.66                           # Denne, Diao & Sullivan 2006, length over diameter
phi = (1 + 5 ** 0.5) / 2
PHI = 2 * math.pi - phi ** 2 / (8 * math.pi ** 2)
m0 = 0.511 / math.exp(2 * math.pi / PHI)
xi = 100 * phi
def mass(A, Zf, L):
    return m0 * (A / Zf) * math.exp(L / (PHI * (1 + math.log(1 + L / xi))))
res3 = {
    "trefoil per diameter from PP2014 (32.7429345/2)": L_tref_R_PP2014 / 2,
    "calculator up-quark L": L_tref_D,
    "DDS lower bound per radius (2 x 15.66)": 2 * DDS_D,
    "quark L values below the per-radius bound": [L for L in (16.372, 21.04, 23.60, 29.13, 37.31) if L < 2 * DDS_D],
    "up quark output at L = 16.372 (MeV)": mass(3, 3, 16.372),
    "up quark output at L = 32.7429 (per radius, MeV)": mass(3, 3, L_tref_R_PP2014),
    "electron output at L = 2π (per radius, MeV)": mass(1, 1, 2 * math.pi),
}
out = {"F7_and_PSL27": res1, "fano_triangle_stabilizer": res2, "L_column": res3}
for sec, d in out.items():
    print(f"== {sec}")
    for k, v in d.items():
        print(f"  {k}: {v}")
json.dump(out, open("b3_checks.json", "w"), indent=1, ensure_ascii=False)
