"""G-2a-S4 first leg (chat-side). Pre-registration: G_2a_S4_EXECUTION_PREREGISTRATION.md
P1: (C^2)^x3 under S3 x SU(2). Blind: dimensions reported, target consulted only in QUARANTINE UNSEAL.
P2: symmetry group of the Borromean rings complement; image of Isom+ in S3 on cusps.
"""
import numpy as np
import itertools

print("=" * 70)
print("P1 -- Schur-Weyl on (C^2)^(x)3")
print("=" * 70)

d = 2; n = 3; D = d ** n  # 8

def perm_op(p):
    """Operator on (C^2)^x3 permuting tensor factors by p (p maps slot i -> slot p[i])."""
    M = np.zeros((D, D))
    for idx in itertools.product(range(d), repeat=n):
        # vector e_{i0} x e_{i1} x e_{i2}  ->  slots rearranged: new[p[k]] = old[k]
        new = [0] * n
        for k in range(n):
            new[p[k]] = idx[k]
        r = new[0] * 4 + new[1] * 2 + new[2]
        c = idx[0] * 4 + idx[1] * 2 + idx[2]
        M[r, c] = 1.0
    return M

S3 = list(itertools.permutations(range(3)))
reps = {p: perm_op(p) for p in S3}
# sanity: homomorphism
for p in S3:
    for q in S3:
        pq = tuple(p[q[k]] for k in range(3))
        assert np.allclose(reps[p] @ reps[q], reps[pq])
print("S3 action on tensor slots: homomorphism verified (36 products).")

def sgn(p):
    s = 1
    for i in range(3):
        for j in range(i + 1, 3):
            if p[i] > p[j]:
                s = -s
    return s

# Isotypic projectors
P_sym  = sum(reps[p] for p in S3) / 6.0
P_alt  = sum(sgn(p) * reps[p] for p in S3) / 6.0
P_std  = np.eye(D) - P_sym - P_alt
for P in (P_sym, P_alt, P_std):
    assert np.allclose(P @ P, P)
d_sym, d_alt, d_std = [int(round(np.trace(P))) for P in (P_sym, P_alt, P_std)]
print(f"S3 isotypic dimensions: sym = {d_sym}, alt = {d_alt}, mixed(std) = {d_std}  (total {d_sym+d_alt+d_std} = {D})")

# Diagonal su(2): Jz, J+, J- on each factor, summed
sz = np.array([[0.5, 0], [0, -0.5]]); sp = np.array([[0, 1], [0, 0]]); sm = sp.T
def diag_op(s):
    I2 = np.eye(2)
    return (np.kron(np.kron(s, I2), I2) + np.kron(np.kron(I2, s), I2)
            + np.kron(np.kron(I2, I2), s))
Jz, Jp, Jm = diag_op(sz), diag_op(sp), diag_op(sm)
# su(2) commutes with S3 (bicommutant sanity)
for p in S3:
    for J in (Jz, Jp, Jm):
        assert np.allclose(reps[p] @ J, J @ reps[p])
print("Diagonal su(2) commutes with all of S3: verified.")

def onb(P, dim):
    w, v = np.linalg.eigh((P + P.T) / 2)
    cols = v[:, w > 0.5]
    assert cols.shape[1] == dim
    q, _ = np.linalg.qr(cols)
    return q

def su2_commutant_dim(B):
    """dim of {X : [X, J|_block] = 0 for J in su(2)} on the block spanned by columns of B."""
    m = B.shape[1]
    Js = [B.T @ J @ B for J in (Jz, Jp, Jm)]
    rows = []
    E = np.eye(m)
    for a in range(m):
        for b in range(m):
            X = np.outer(E[:, a], E[:, b])
            rows.append(np.concatenate([(J @ X - X @ J).reshape(-1) for J in Js]))
    A = np.array(rows)
    s = np.linalg.svd(A, compute_uv=False)
    return int(np.sum(s < 1e-9))

B_sym = onb(P_sym, d_sym)
B_std = onb(P_std, d_std)
c_sym = su2_commutant_dim(B_sym)
c_std = su2_commutant_dim(B_std)
print(f"su(2)-commutant dim on sym block   (dim {d_sym}): {c_sym}"
      f"  -> {'IRREDUCIBLE' if c_sym == 1 else 'reducible'}")
print(f"su(2)-commutant dim on mixed block (dim {d_std}): {c_std}"
      f"  -> {'IRREDUCIBLE' if c_std == 1 else 'reducible'}")
print(f"alt block dim = {d_alt} (Alt^3(C^2) vanishes: {'yes' if d_alt == 0 else 'NO'})")

# Casimir on sym block -> spin content, reported structurally (j value), no target named
C2 = Jz @ Jz + 0.5 * (Jp @ Jm + Jm @ Jp)
c2_sym = np.linalg.eigvalsh(B_sym.T @ C2 @ B_sym)
c2_std = np.linalg.eigvalsh(B_std.T @ C2 @ B_std)
print(f"Casimir eigenvalues, sym block:   {np.round(c2_sym, 6)}")
print(f"Casimir eigenvalues, mixed block: {np.round(c2_std, 6)}")

# Doubling-incompatibility check: SU(2)-isotypic content of Sym^3(C^2) vs the binary doubling C^2 (+) C^2
# doubling of the per-strand carrier: Casimir spectrum = {3/4 x4}; compare
c2_doubling = np.linalg.eigvalsh(np.kron(np.eye(2), sz @ sz + 0.5 * (sp @ sm + sm @ sp)))
same = np.allclose(np.sort(c2_sym), np.sort(c2_doubling))
print(f"Casimir spectrum of binary doubling C^2 (+) C^2: {np.round(c2_doubling, 6)}")
print(f"Sym block == binary doubling as SU(2)-module?  {same}  "
      f"({'COLLISION' if same else 'INCOMPATIBLE -- ternary object confirmed'})")

print()
print("=" * 70)
print("P2 -- Borromean rings complement: symmetry group and cusp action")
print("=" * 70)
import snappy
M = snappy.Manifold("6^3_2")   # Borromean rings complement
print("Manifold:", M, "| cusps:", M.num_cusps(), "| volume:", M.volume())
G = M.symmetry_group()
print("Symmetry group:", G, "| order:", G.order())
print("Owns orientation-reversing symmetries:", G.is_amphicheiral() if hasattr(G, "is_amphicheiral") else "n/a")
isos = G.isometries()
print(f"Number of isometries returned: {len(isos)}")

def cusp_perm(iso):
    ci = iso.cusp_images()
    return tuple(ci)

def is_or_preserving(iso):
    # orientation preserved iff every cusp map has det +1 (consistent across cusps for an isometry)
    mats = iso.cusp_maps()
    dets = [m[0][0] * m[1][1] - m[0][1] * m[1][0] for m in mats]
    assert all(d == dets[0] for d in dets), f"mixed dets {dets}"
    return dets[0] == 1

full_perms, plus_perms = set(), set()
n_plus = 0
for iso in isos:
    p = cusp_perm(iso)
    full_perms.add(p)
    if is_or_preserving(iso):
        n_plus += 1
        plus_perms.add(p)
print(f"Orientation-preserving isometries: {n_plus} / {len(isos)}")
print(f"Cusp permutations realized by FULL group:  {sorted(full_perms)}  (count {len(full_perms)})")
print(f"Cusp permutations realized by Isom+:       {sorted(plus_perms)}  (count {len(plus_perms)})")
transpositions = [(1, 0, 2), (0, 2, 1), (2, 1, 0)]
tr_plus = [t for t in transpositions if t in plus_perms]
print(f"Transpositions realized orientation-preservingly: {tr_plus}")
print(f"H-P2 verdict: image of Isom+ in S3 is "
      f"{'ALL of S3' if len(plus_perms) == 6 else ('A3 only' if plus_perms == {(0,1,2),(1,2,0),(2,0,1)} else str(sorted(plus_perms)))}")

print()
print("=" * 70)
print("QUARANTINE UNSEAL (targets consulted only now)")
print("=" * 70)
print(f"Quarantined target integer (factor): 4.  Computed d_sym = {d_sym}.  Match: {d_sym == 4}")
print(f"Quarantined spin value: j = 3/2 (Casimir 15/4 = 3.75). "
      f"Sym-block Casimir all equal 3.75: {np.allclose(c2_sym, 3.75)}")
print("Distinct-48 flag check: |Isom(BRC)| =", G.order(),
      "-- same integer as |2O| = 48; provenance distinct; NO identification made by this gate.")
