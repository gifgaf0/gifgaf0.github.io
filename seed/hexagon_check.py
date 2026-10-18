"""
hexagon_check.py — checks the torus and group facts in SEED.md, section 3.
Needs only numpy. Run: python3 hexagon_check.py

1. SU(3)'s maximal torus is the plane {θ1+θ2+θ3 = 0} modulo the hexagonal
   lattice Λ = {θ in Z^3 : θ1+θ2+θ3 = 0}.
2. The seven powers of D = diag(ζ, ζ², ζ⁴), ζ = e^(2πi/7), are seven points
   on that torus. The finer lattice through them cuts the torus into the
   7-vertex triangulation: K7, 14 triangles, two Fano families, one of them
   the octonion lines {i, i+1, i+3}.
3. The 120° Weyl rotation moves the points as x -> 4x. With D it generates
   Z7 ⋊ Z3 (order 21) inside SU(3), and that group preserves both families.
4. Klein's three matrices generate PSL(2,7) (order 168) inside SU(3) and
   preserve the Klein quartic x³y + y³z + z³x.
5. Klein's copy holds diag(ζ⁴, ζ², ζ), not D. The copy that holds
   <D, 120° turn> is its conjugate under the swap x <-> z (with a sign, so
   det = 1). It has order 168, preserves the mirror quartic xy³ + yz³ + zx³,
   and the order-21 group is maximal in it.
6. Only two Fano planes on Z7 are kept by x -> x+1, and the torus families
   are exactly those two, so one of them is bound to be the octonion lines.
7. SU(3)'s Weyl group (order 6) turns the torus only by 120°. G2's (order 12)
   adds turns by 60°, 180° and 300°, which keep the seven points but swap the
   two Fano families. No mirror in either group keeps the seven points.
"""
import cmath
import itertools

import numpy as np

# ---------- 1-3: the torus ----------
def in_lattice(v):
    return np.allclose(v, np.round(v)) and abs(v.sum()) < 1e-9

p = np.array([1, 2, -3]) / 7            # exp(2πi·p) = diag(ζ, ζ², ζ⁴); point "1"
turn = lambda v: np.roll(v, 1)          # Weyl 3-cycle = 120° rotation of the plane
label = lambda v: next((j for j in range(7) if in_lattice(v - j * p)), None)  # None: not one of the seven

print("120° turn sends point 1 to point", label(turn(p)))

# the six shortest steps of the finer lattice Λ + Zp, in angular order around point 0
steps = [s * v for v in (p, turn(p), turn(turn(p))) for s in (1, -1)]
u = np.array([1, -1, 0]) / np.sqrt(2)
w = np.array([1, 1, -2]) / np.sqrt(6)
steps.sort(key=lambda v: np.arctan2(v @ w, v @ u))
ring = [label(v) for v in steps]
print("neighbours of point 0:", sorted(ring), "-> every point touches every other (K7)")

tris = [(0, ring[i], ring[(i + 1) % 6]) for i in range(6)]
def orbit(ts):
    return {tuple(sorted((x + t) % 7 for x in tri)) for tri in ts for t in range(7)}
A, B = orbit(tris[0::2]), orbit(tris[1::2])

def is_fano(S):
    pairs = [pr for tri in S for pr in itertools.combinations(tri, 2)]
    return len(S) == 7 and len(pairs) == len(set(pairs)) == 21

octonion = {tuple(sorted((i % 7, (i + 1) % 7, (i + 3) % 7))) for i in range(7)}
print("triangles:", len(A | B), "| family A Fano:", is_fano(A), "| family B Fano:", is_fano(B))
print("one family is the octonion lines {i, i+1, i+3}:", octonion in (A, B))

image = lambda S, a, b: {tuple(sorted((a * x + b) % 7 for x in tri)) for tri in S}
print("x -> ax+b (a in 1,2,4) preserves both families:",
      all(image(S, a, b) == S for S in (A, B) for a in (1, 2, 4) for b in range(7)))

# ---------- 3-4: the groups inside SU(3) ----------
z = cmath.exp(2j * cmath.pi / 7)
C = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=complex)

def group(gens, cap=1000):
    key = lambda M: tuple(np.round(M, 6).ravel())
    I = np.eye(3, dtype=complex)
    seen, frontier = {key(I): I}, [I]
    while frontier and len(seen) <= cap:
        new = []
        for M in frontier:
            for g in gens:
                N = M @ g
                if key(N) not in seen:
                    seen[key(N)] = N
                    new.append(N)
        frontier = new
    return list(seen.values())

def in_su3(Ms):
    return all(np.allclose(M @ M.conj().T, np.eye(3)) and np.isclose(np.linalg.det(M), 1)
               for M in Ms)

D = np.diag([z, z**2, z**4])
F21 = group([D, C])
print("|<D, 120° turn>| =", len(F21), "| inside SU(3):", in_su3(F21))

Dk = np.diag([z**4, z**2, z])           # Klein's labelling; his copy holds Dk, not D (see 5)
R = (1j / np.sqrt(7)) * np.array([[z - z**6, z**2 - z**5, z**4 - z**3],
                                  [z**2 - z**5, z**4 - z**3, z - z**6],
                                  [z**4 - z**3, z - z**6, z**2 - z**5]])
PSL = group([Dk, C, R])
print("|<Klein's matrices>| =", len(PSL), "| inside SU(3):", in_su3(PSL))

v = np.random.default_rng(0).normal(size=3) + 1j * np.random.default_rng(1).normal(size=3)
quartic = lambda x: x[0]**3 * x[1] + x[1]**3 * x[2] + x[2]**3 * x[0]
print("Klein quartic preserved by the generators:",
      all(np.isclose(quartic(M @ v), quartic(v)) for M in (Dk, C, R)))

# ---------- 5: which copy of PSL(2,7) holds <D, 120° turn> ----------
def contains(G, H):
    return all(any(np.allclose(h, g) for g in G) for h in H)

print("<D, 120° turn> inside Klein's own copy:", contains(PSL, F21))
flip = -np.array([[0, 0, 1], [0, 1, 0], [1, 0, 0]], dtype=complex)   # x <-> z, times -1 so det = 1
Rf = flip @ R @ np.linalg.inv(flip)
print("flip in SU(3):", in_su3([flip]),
      "| flip sends Dk to D:", np.allclose(flip @ Dk @ np.linalg.inv(flip), D))
PSLf = group([D, C, Rf])
print("flipped copy: order", len(PSLf), "| inside SU(3):", in_su3(PSLf),
      "| holds <D, 120° turn>:", contains(PSLf, F21))
mirror = lambda x: x[0] * x[1]**3 + x[1] * x[2]**3 + x[2] * x[0]**3
print("flipped copy preserves the mirror quartic xy³ + yz³ + zx³:",
      all(np.isclose(mirror(M @ v), mirror(v)) for M in (D, C, Rf)))
print("order-21 group maximal in it:",
      all(len(group([D, C, g])) == 168 for g in PSLf if not contains(F21, [g])))

# ---------- 6: the octonion match is forced ----------
cyclic = {frozenset(orbit([tri])) for tri in itertools.combinations(range(7), 3)
          if is_fano(orbit([tri]))}
print("Fano planes on Z7 kept by x -> x+1:", len(cyclic),
      "| the torus families are exactly these:", {frozenset(A), frozenset(B)} == cyclic)

# ---------- 7: the Weyl groups of SU(3) and G2 on the seven points ----------
refl = lambda r: np.eye(3) - 2 * np.outer(r, r) / (r @ r)
long_roots = [np.eye(3)[i] - np.eye(3)[j] for i, j in ((0, 1), (1, 2), (0, 2))]   # SU(3)'s roots
short_roots = [np.eye(3)[i] - np.ones(3) / 3 for i in range(3)]                   # G2 adds these

def weyl(roots):
    gens = [refl(r) for r in roots]
    G, frontier = [np.eye(3)], [np.eye(3)]
    while frontier:
        new = []
        for M in frontier:
            for g in gens:
                N = g @ M
                if not any(np.allclose(N, X) for X in G):
                    G.append(N)
                    new.append(N)
        frontier = new
    return G

lattice_basis = (np.array([1., -1, 0]), np.array([0., 1, -1]))
for name, roots in (("SU(3)", long_roots), ("G2", long_roots + short_roots)):
    Wg = weyl(roots)
    mirrors = [g for g in Wg if np.linalg.det(g) < 0]
    print(f"Weyl({name}): order {len(Wg)} | keeps Λ:",
          all(in_lattice(g @ b) for g in Wg for b in lattice_basis),
          "| mirrors that keep the seven points:",
          sum(label(g @ p) is not None for g in mirrors), "of", len(mirrors))
    rows = []
    for g in Wg:
        if np.linalg.det(g) < 0:
            continue
        angle = round(np.degrees(np.arctan2((g @ u) @ w, (g @ u) @ u))) % 360
        k = label(g @ p)
        if k is None:
            fate = "moves the seven points"
        elif image(A, k, 0) == A and image(B, k, 0) == B:
            fate = f"x -> {k}x, keeps both families"
        elif image(A, k, 0) == B and image(B, k, 0) == A:
            fate = f"x -> {k}x, swaps the families"
        else:
            fate = f"x -> {k}x, other"
        rows.append((angle, fate))
    for angle, fate in sorted(rows):
        print(f"   turn {angle:>3}°: {fate}")
