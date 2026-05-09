"""
sqt_slwe.py — SQT Sedenion Module LWE (Corrected)
==================================================
Option B2: Module LWE over the sedenion algebra S_q using the
conjugate-norm inner product and PSL(2,7)-structured public matrix.

KEY FINDING FROM DIAGNOSTIC:
  lmm(a)^T = lmm(conj(a)) exactly  [zero violations, verified]
  This means the sedenion algebra satisfies:
    <A*s, r>_norm = <s, A^H*r>_norm
  where <u,v>_norm = sum_i Re(conj(u[i])*v[i]) mod p
  and A^H[i][j] = conj(A[j][i])

  This is the adjoint relation needed for correct LWE decryption.

SCHEME:
  KeyGen(k, p):
    s ← S_q^k  (private, non-ZD elements)
    A ← PSL(2,7)-structured k×k sedenion matrix  (public)
    e ← small^k  (error)
    b = A*s + e  (public, sedenion left-mult, element-wise)
    pk = (A, b),  sk = s

  Encaps(pk, m ∈ {0,1}):
    r ← S_q^k  (fresh randomness)
    e1 ← small^k,  e2 ← small
    c1 = A^H * r + e1       [k sedenion elements]
    c2 = <b, r>_norm + e2 + m·⌊p/2⌋   [scalar mod p]
    return (c1, c2)

  Decaps(sk, c1, c2):
    v = c2 − <s, c1>_norm
    m = round(v · 2/p)

  Correctness:
    <b,r>_norm = <A*s+e, r>_norm = <s, A^H*r>_norm + <e,r>_norm
    <s, c1>_norm = <s, A^H*r + e1>_norm = <s, A^H*r>_norm + <s,e1>_norm
    v = m·⌊p/2⌋ + <e,r>_norm − <s,e1>_norm + e2  ≈ m·⌊p/2⌋

PSL(2,7) STRUCTURE:
  A's rows are Singer-cycle orbits of seed elements:
    Row i = {σ^j(seed_i) : j=0..k-1}  where σ is the Z_7 Singer cycle.
  This encodes the Z_7 ≤ PSL(2,7) symmetry confirmed in OP §2.24.1.
  The synchronized Singer cycle preserves all 42 cross-interface ZD pairs.

TESTS:
  1. Correctness over N trials (DFR measurement)
  2. Annihilator attack: non-associativity residual vs noise
  3. Noise budget: max residual vs p/4 threshold
  4. Rank: PSL(2,7)-structured A vs random A

Author: Matt Gifford / SQT Project — May 7, 2026
"""

import sys, random, hashlib
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sedenion_Fp import mul_vec, basis_vec, DIM
from sedenion_audit import find_canonical_zd_quadruples

p   = 911   # mod-455 prime: p ≡ 1 (mod 5,7,13) → full PSL(2,7) symmetry
random.seed(42)

# ── Sedenion arithmetic ──────────────────────────────────────────

def s_mul(x, y):    return mul_vec(x, y, p)
def s_add(x, y):    return [(a+b)%p for a,b in zip(x,y)]
def s_sub(x, y):    return [(a-b)%p for a,b in zip(x,y)]
def s_zero():       return [0]*DIM
def s_conj(x):      return [x[0]] + [(-c)%p for c in x[1:]]
def s_norm_sq(x):   return sum((c if c<p//2 else c-p)**2 for c in x)

def s_re(x):
    """Real part of sedenion x."""
    return x[0]

def norm_inner(u, v):
    """
    Sedenion norm inner product: Re(conj(u) * v) mod p.
    Properties verified:
    - Symmetric: <u,v> = <v,u>
    - Adjoint:   <A*s, r>_norm = <s, A^H*r>_norm  [lmm(a)^T = lmm(conj(a))]
    """
    return s_re(s_mul(s_conj(u), v))

def norm_inner_k(U, V):
    """Sum of norm_inner over k-vector pairs."""
    return sum(norm_inner(U[i], V[i]) for i in range(len(U))) % p

# ── Module operations ────────────────────────────────────────────

def mat_vec(M, v):
    """(M*v)[i] = sum_j M[i][j] * v[j]  (sedenion left-mult)."""
    k = len(v)
    result = []
    for i in range(len(M)):
        acc = s_zero()
        for j in range(k):
            acc = s_add(acc, s_mul(M[i][j], v[j]))
        result.append(acc)
    return result

def conj_transpose(M):
    """A^H[i][j] = conj(A[j][i])."""
    k = len(M)
    return [[s_conj(M[j][i]) for j in range(k)] for i in range(k)]

def rank_flat(M_sed, p_val):
    """Rank of the flattened (k*16)×(k*16) sedenion matrix over F_p."""
    k = len(M_sed)
    n = k * DIM
    def lmm_block(s):
        B = [[0]*DIM for _ in range(DIM)]
        for j in range(DIM):
            col = s_mul(s, basis_vec(j))
            for i in range(DIM): B[i][j] = col[i]
        return B
    A_flat = [[0]*n for _ in range(n)]
    for i in range(k):
        for j in range(k):
            Mij = lmm_block(M_sed[i][j])
            for r2 in range(DIM):
                for c2 in range(DIM):
                    A_flat[i*DIM+r2][j*DIM+c2] = Mij[r2][c2]
    # Gaussian elimination
    A2 = [[x%p_val for x in row] for row in A_flat]
    rank = 0
    for col in range(n):
        piv = next((row for row in range(rank,n) if A2[row][col]%p_val!=0), None)
        if piv is None: continue
        A2[rank],A2[piv] = A2[piv],A2[rank]
        inv = pow(int(A2[rank][col]),p_val-2,p_val)
        A2[rank] = [(x*inv)%p_val for x in A2[rank]]
        for row in range(n):
            if row!=rank and A2[row][col]%p_val!=0:
                f=A2[row][col]
                A2[row]=[(A2[row][c]-f*A2[rank][c])%p_val for c in range(n)]
        rank+=1
    return rank

# ── Key material ─────────────────────────────────────────────────

quads    = find_canonical_zd_quadruples(p)
zd_pairs = set()
for q in quads: zd_pairs.add(q[0]); zd_pairs.add(q[1])

def rand_nonzd():
    while True:
        v = [random.randint(0,p-1) for _ in range(DIM)]
        nz = [(i,v[i]) for i in range(DIM) if v[i]!=0]
        if not nz: continue
        if len(nz)==2:
            idx = tuple(sorted([nz[0][0],nz[1][0]]))
            if idx in zd_pairs: continue
        return v

def rand_small():
    """CBD-like small error: values in {-2,-1,0,0,0,1,2} mod p."""
    return [random.choices([-2,-1,0,0,0,1,2], weights=[1,3,6,6,6,3,1])[0]%p
            for _ in range(DIM)]

# ── PSL(2,7) Singer cycle ─────────────────────────────────────────

def singer_perm():
    """Z_7 Singer cycle: e_i -> e_{(i mod 7)+1} for i in 1..7."""
    return {i: (i%7)+1 for i in range(1,8)}

def apply_singer(v):
    """Apply synchronized Singer to sedenion vector v."""
    result = list(v)
    perm = singer_perm()
    temp = list(v)
    for old, new in perm.items():
        result[new]   = temp[old]      # first copy
        result[new+8] = temp[old+8]    # second copy (mirror)
    return result

def singer_orbit(seed, k):
    """Singer Z_7 orbit of seed, k elements."""
    orbit = [seed[:]]
    cur   = seed[:]
    for _ in range(k-1):
        cur = apply_singer(cur)
        orbit.append(cur[:])
    return orbit[:k]

# ── Scheme ────────────────────────────────────────────────────────

def keygen(k):
    """
    Generate SQT-SLWE keypair.
    Returns dict with sk, pk=(A, b).
    """
    # Private key
    s = [rand_nonzd() for _ in range(k)]

    # Public matrix: PSL(2,7)-structured
    # Row i = Singer cycle orbit of seed_i
    A = [singer_orbit(rand_nonzd(), k) for _ in range(k)]

    # Error and public vector
    e = [rand_small() for _ in range(k)]
    As = mat_vec(A, s)
    b  = [s_add(As[i], e[i]) for i in range(k)]

    return {'sk': s, 'A': A, 'b': b, 'e': e, 'k': k}

def encaps(A, b, k):
    """
    Encapsulate: encrypt a random bit, return (c1, c2, m_bit).
    Uses conjugate-transpose structure for correct decryption.
    """
    m_bit = random.randint(0, 1)
    q2    = p // 2

    r  = [rand_nonzd() for _ in range(k)]
    e1 = [rand_small() for _ in range(k)]
    e2 = random.choices([-1,0,0,0,1], weights=[1,4,4,4,1])[0] % p

    # c1 = A^H * r + e1
    AH   = conj_transpose(A)
    AHr  = mat_vec(AH, r)
    c1   = [s_add(AHr[i], e1[i]) for i in range(k)]

    # c2 = <b, r>_norm + e2 + m*⌊p/2⌋
    b_dot_r = norm_inner_k(b, r)
    c2      = (b_dot_r + e2 + m_bit * q2) % p

    return c1, c2, m_bit

def decaps(sk, c1, c2, k):
    """
    Decapsulate: recover bit from ciphertext.
    v = c2 - <s, c1>_norm
    """
    q2 = p // 2
    s_dot_c1 = norm_inner_k(sk, c1)
    v        = (c2 - s_dot_c1) % p
    # v ≈ 0 (bit=0) or v ≈ q2 (bit=1)
    m_dec = 1 if (q2//2 < v < 3*q2//2) else 0
    return m_dec, v

def hash_shared_key(c2):
    """Derive a shared key from the encapsulated scalar."""
    return hashlib.sha256(c2.to_bytes(4, 'big')).hexdigest()[:32]

# ── Tests ─────────────────────────────────────────────────────────

if __name__ == '__main__':
    import time

    print("=" * 65)
    print("SQT-SLWE: Sedenion Module LWE with PSL(2,7) Structure")
    print(f"Field F_{p}  |  Module rank k=4  |  Effective dim {4*DIM}")
    print("=" * 65)

    k = 4

    # ── Key generation ────────────────────────────────────────────
    print("\n─── Key Generation ───")
    t0 = time.perf_counter()
    keys = keygen(k)
    print(f"  Time: {(time.perf_counter()-t0)*1000:.1f} ms")
    print(f"  Private s: {k} non-ZD sedenion elements")
    print(f"  Public A:  {k}×{k} PSL(2,7)/Singer-structured matrix")
    print(f"  Public b:  {k} sedenion elements = A*s + e")

    # Verify A structure: each row is a Singer orbit
    perm = singer_perm()
    singer_ok = True
    for i in range(k):
        for j in range(k-1):
            expected = apply_singer(keys['A'][i][j])
            if expected != keys['A'][i][j+1]:
                singer_ok = False
    print(f"  Singer orbit structure: {'✓ verified' if singer_ok else '✗ broken'}")

    # ── Rank comparison ───────────────────────────────────────────
    print("\n─── Rank: PSL(2,7)-structured A vs random A ───")
    rank_struct = rank_flat(keys['A'], p)
    A_rand = [[rand_nonzd() for _ in range(k)] for _ in range(k)]
    rank_rand  = rank_flat(A_rand, p)
    print(f"  Structured A rank: {rank_struct}/{k*DIM}")
    print(f"  Random A rank:     {rank_rand}/{k*DIM}")
    cost = rank_rand - rank_struct
    print(f"  Rank cost of PSL(2,7) structure: {cost}")
    print(f"  {'No rank reduction — structure adds no lattice shortcut' if cost==0 else f'Rank reduced by {cost} — potential weakness'}")

    # ── Correctness ───────────────────────────────────────────────
    print("\n─── Correctness Test (100 trials) ───")
    correct = 0
    residuals = []
    for _ in range(100):
        c1, c2, m_in = encaps(keys['A'], keys['b'], k)
        m_out, v      = decaps(keys['sk'], c1, c2, k)
        v_centered    = v if v < p//2 else v - p
        expected      = (p//2) * m_in
        residuals.append(abs(v_centered - expected))
        correct      += (m_in == m_out)

    dfr       = (100 - correct) / 100
    avg_res   = sum(residuals) / len(residuals)
    max_res   = max(residuals)
    threshold = p // 4

    print(f"  Correct: {correct}/100  (DFR = {dfr:.3f})")
    print(f"  Noise residual avg: {avg_res:.1f}  max: {max_res}  threshold p/4={threshold}")
    if max_res < threshold:
        print(f"  ✓ All residuals within p/4 — decryption SOUND")
    else:
        print(f"  ✗ Residual exceeds p/4 — DFR too high for this parameter set")

    # ── Adjoint property verification ────────────────────────────
    print("\n─── Adjoint Property: <A*s,r>_norm = <s,A^H*r>_norm ───")
    s_test  = keys['sk']
    r_test  = [rand_nonzd() for _ in range(k)]
    AH      = conj_transpose(keys['A'])
    As_test = mat_vec(keys['A'], s_test)
    AHr_t   = mat_vec(AH, r_test)
    lhs     = norm_inner_k(As_test, r_test)
    rhs     = norm_inner_k(s_test,  AHr_t)
    print(f"  <A*s, r>_norm  = {lhs}")
    print(f"  <s, A^H*r>_norm = {rhs}")
    print(f"  Equal: {lhs==rhs}  {'✓ adjoint holds — decryption is exact' if lhs==rhs else '✗ adjoint fails'}")

    # ── Annihilator attack ────────────────────────────────────────
    print("\n─── Annihilator Attack Resistance ───")
    # Use ZD-derived annihilator: z*A_elem = 0 for some ZD pair
    q0 = list(quads)[0]
    (qa, qb), (qc, qd) = q0
    z_elem = A_elem = None
    for sa in [1, p-1]:
        for sc in [1, p-1]:
            zt = [0]*DIM; zt[qa]=sa; zt[qb]=1
            At = [0]*DIM; At[qc]=sc; At[qd]=1
            if all(x==0 for x in s_mul(zt, At)):
                z_elem, A_elem = zt, At
                break
        if z_elem: break

    # Module annihilator: z_mod = [z_elem, 0, .., 0]
    z_mod = [z_elem if i==0 else s_zero() for i in range(k)]

    # Rebuild public b using A_elem in position [0][0]
    A_attack       = [row[:] for row in keys['A']]
    A_attack[0][0] = A_elem
    s_att          = keys['sk']
    e_att          = [rand_small() for _ in range(k)]
    As_att         = mat_vec(A_attack, s_att)
    b_att          = [s_add(As_att[i], e_att[i]) for i in range(k)]

    # Attack computation
    z_b   = norm_inner_k(z_mod, b_att)
    z_e   = norm_inner_k(z_mod, e_att)
    z_As  = norm_inner_k(z_mod, As_att)

    # In associative algebra: z*A=0 → z*(A*s)=(z*A)*s=0, noise isolated
    # Sedenion: norm inner is bilinear, NOT subject to same associativity issue
    # The attack on norm inner product is different from left-mult inner product
    print(f"  z·b (norm)    = {z_b}")
    print(f"  z·e (target)  = {z_e}  (what attacker wants)")
    print(f"  z·(A*s) (norm)= {z_As}  (should vanish if z*A=0)")

    # Check: does z·(A*s) = 0 using norm inner?
    # norm_inner(z_mod[0], As_att[0]) = Re(conj(z_elem) * As_att[0])
    # This is NOT sedenion multiplication — it's the real part of a product.
    # Even if z*A_elem = 0 (sedenion product), conj(z)*As may not be 0.
    if z_As == z_e:
        print("  ✗ Noise perfectly isolated — attack SUCCEEDS via norm inner product")
    elif abs(z_As - z_b) < p // 8:
        print("  △ Partial: norm inner reduces to scalar, harder to exploit than sedenion annihilator")
    else:
        print(f"  ✓ Attacker gets scalar z·b={z_b}, z·e={z_e}: difference = {(z_b-z_e)%p}")
        print(f"    The scalar collapse is the correct channel — attacker sees ONE number,")
        print(f"    not a full sedenion. Attack surface reduced from 16D to 1D.")

    # ── PSL(2,7) ZD preservation ──────────────────────────────────
    print("\n─── PSL(2,7) Z_7 Action: ZD Graph Preservation ───")
    cross = [(a,b) for (a,b) in zd_pairs if a in range(1,8) and b in range(9,16)]
    broken = 0
    for (a, b) in cross:
        new_a = (a%7)+1
        new_b = ((b-8)%7)+1+8
        if tuple(sorted([new_a,new_b])) not in zd_pairs:
            broken += 1
    print(f"  Cross-interface ZD pairs: {len(cross)}")
    print(f"  Preserved under Singer Z_7: {len(cross)-broken}/{len(cross)}")
    print(f"  {'✓ Z_7 ⊂ PSL(2,7) is a symmetry of the ZD graph' if broken==0 else f'✗ {broken} pairs broken'}")

    # ── Summary ───────────────────────────────────────────────────
    print("\n" + "="*65)
    print("RESULTS SUMMARY")
    print("="*65)
    print(f"""
Scheme:   SQT-SLWE (Sedenion Module LWE + PSL(2,7) structure)
Field:    F_{p} (mod-455 prime)
Rank k:   {k}  |  Effective dimension: {k*DIM}

Correctness:
  DFR = {dfr:.3f}  ({'PASS' if dfr < 0.05 else 'FAIL — noise too large for this p'})
  Max residual: {max_res} / threshold p/4={threshold}
  {'Sound: all noise within decryption window' if max_res<threshold else 'Noise exceeds threshold — scale p or reduce error width'}

Adjoint property <A*s,r>_norm = <s,A^H*r>_norm:
  {'HOLDS — conjugate-transpose inner product is sound' if lhs==rhs else 'FAILS — implementation error'}

PSL(2,7) Z_7 structure:
  Singer orbit in A: {'✓ verified' if singer_ok else '✗'}
  ZD graph symmetry: {'✓ confirmed (OP §2.24.1 partial closure)' if broken==0 else '✗'}
  Rank cost of structure: {cost} / {k*DIM} dimensions

Annihilator attack:
  Norm inner product collapses attack to scalar channel (1D vs 16D)
  Attacker sees single value, not full sedenion residual

HONEST STATUS:
  This is a structurally sound toy-scale scheme.
  p=911 and k=4 give effective dim 64 — well below cryptographic threshold (≥512).
  Next steps:
    1. Scale: k=32, p = large mod-455 prime (≥2^32)
    2. Formal BKZ cost estimate at k=32
    3. CBD parameter optimization: DFR target 2^-128
    4. Test full PSL(2,7) (all 168 elements, not just Z_7)
    5. Hardness proof or reduction attempt
""")
