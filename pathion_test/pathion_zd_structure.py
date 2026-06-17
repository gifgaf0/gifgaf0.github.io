"""
32D ("pathion") zero-divisor structure vs the 16D (sedenion) structure.

QUESTION (pre-registered before running):
  Does the 32D two-term zero-divisor set decompose predictably in terms of
  the 16D sedenion zero-divisors? Specifically:
   (A) How many two-term ZD index-quadruples does 32D have, vs 84 at 16D?
   (B) Of the 32D ZDs, how many live ENTIRELY in the lower 16D copy
       (indices 1..15)? Prediction: exactly the 16D count (the sedenion
       subalgebra sits inside, its ZDs persist).
   (C) How many are NEW (use at least one index in 16..31)?
   (D) Do the new ones organize by the same e_a*e_b = +-e_c "line" combinatorics
       (the analog of the Fano structure), i.e. is the index quadruple
       always a "doubly-pure" pattern {a,b,c,d} with a fixed XOR/parity relation?

This reuses the project's build_cd_table convention exactly (CD doubling,
conj flips imaginary sign). It is a NEW computation, not in the literature.
Eddington note: no target value is consulted; counts are reported as found.
"""
from itertools import combinations

# ---- CD multiplication table (same convention as sedenion_Fp.py) -----------
def build_cd_table(n_levels):
    dim = 2 ** n_levels
    def conj_sign(idx):
        return (idx, 1) if idx == 0 else (idx, -1)
    mult = {0: {0: (0, 1)}}
    # base level 0
    cur = [[(0,1)]]
    dim_prev = 1
    for _ in range(n_levels):
        dim_new = dim_prev * 2
        new = [[(0,1)]*dim_new for _ in range(dim_new)]
        for i in range(dim_new):
            for j in range(dim_new):
                # decompose into (a,b),(c,d) halves
                if i < dim_prev:
                    a, b = i, None
                else:
                    a, b = None, i - dim_prev
                if j < dim_prev:
                    c, d = j, None
                else:
                    c, d = None, j - dim_prev
                re_terms = []  # (index, sign) accumulator for lower half
                im_terms = []  # for upper half
                # (a,b)(c,d) = (ac - conj(d)b, da + b conj(c))
                # ac
                if a is not None and c is not None:
                    k,s = cur[a][c]; re_terms.append((k, s))
                # - conj(d) b
                if d is not None and b is not None:
                    cd_i, cd_s = conj_sign(d)
                    k,s = cur[cd_i][b]; re_terms.append((k, -cd_s*s))
                # d a  -> upper
                if d is not None and a is not None:
                    k,s = cur[d][a]; im_terms.append((k, s))
                # b conj(c) -> upper
                if b is not None and c is not None:
                    cc_i, cc_s = conj_sign(c)
                    k,s = cur[b][cc_i]; im_terms.append((k, cc_s*s))
                # collapse (single-term expected for basis products)
                acc = {}
                for k,s in re_terms:
                    acc[k] = acc.get(k,0)+s
                for k,s in im_terms:
                    kk = k + dim_prev
                    acc[kk] = acc.get(kk,0)+s
                nz = [(k,s) for k,s in acc.items() if s != 0]
                assert len(nz) <= 1, f"non-monomial at ({i},{j}): {nz}"
                new[i][j] = nz[0] if nz else (0,0)
        cur = new
        dim_prev = dim_new
    return cur

def make_ops(MULT, DIM, p):
    def basis(i):
        v=[0]*DIM; v[i]=1; return v
    def mul(x,y):
        r=[0]*DIM
        for i in range(DIM):
            if x[i]==0: continue
            for j in range(DIM):
                if y[j]==0: continue
                k,s = MULT[i][j]
                if s: r[k]=(r[k]+x[i]*y[j]*s)%p
        return r
    def is_zero(v): return all(c%p==0 for c in v)
    def add(x,y): return [(a+b)%p for a,b in zip(x,y)]
    def scale(x,s): return [(c*s)%p for c in x]
    return basis,mul,is_zero,add,scale

def two_term_zd_quadruples(MULT, DIM, p, verbose_every=0):
    """All canonical two-term ZD index quadruples (a,b,c,d) with +-1 coeffs."""
    basis,mul,is_zero,add,scale = make_ops(MULT,DIM,p)
    imag = list(range(1,DIM))
    quads = set()
    cnt=0
    for a,b in combinations(imag,2):
        ea,eb = basis(a),basis(b)
        for sa in (1,p-1):
            for sb in (1,p-1):
                x = add(scale(ea,sa),scale(eb,sb))
                for c,d in combinations(imag,2):
                    if {a,b}=={c,d}: continue
                    ec,ed = basis(c),basis(d)
                    for sc in (1,p-1):
                        for sd in (1,p-1):
                            y = add(scale(ec,sc),scale(ed,sd))
                            if is_zero(mul(x,y)):
                                quads.add((a,b,c,d))
        cnt+=1
        if verbose_every and cnt%verbose_every==0:
            print(f"   {cnt}/{len(imag)*(len(imag)-1)//2} done, {len(quads)} quads")
    return quads

if __name__=="__main__":
    p = 911   # same prime the project uses (p mod 455 == 1)
    print(f"p={p}, p mod 455={p%455}")

    # ---- 16D sanity: must reproduce the known 84-pair structure -----------
    print("\n=== 16D (sedenions): reproduce the known structure ===")
    M16 = build_cd_table(4); D16=16
    q16 = two_term_zd_quadruples(M16,D16,p)
    # unordered {(a,b),(c,d)} count
    un16=set()
    for (a,b,c,d) in q16:
        un16.add(frozenset([(min(a,b),max(a,b)),(min(c,d),max(c,d))]))
    print(f"   ordered index-quadruples: {len(q16)}")
    print(f"   unordered ZD pairs: {len(un16)}   (literature: 84)")

    # ---- 32D ("pathions") --------------------------------------------------
    print("\n=== 32D (pathions): full two-term ZD enumeration ===")
    M32 = build_cd_table(5); D32=32
    q32 = two_term_zd_quadruples(M32,D32,p,verbose_every=5)
    un32=set()
    for (a,b,c,d) in q32:
        un32.add(frozenset([(min(a,b),max(a,b)),(min(c,d),max(c,d))]))
    print(f"   ordered index-quadruples: {len(q32)}")
    print(f"   unordered ZD pairs: {len(un32)}")

    # ---- DECOMPOSITION: lower-copy vs new ---------------------------------
    print("\n=== Decomposition of 32D ZD pairs ===")
    lower=set(); crossing=set(); upper=set()
    for fs in un32:
        idxs=[]
        for (i,j) in fs: idxs+= [i,j]
        in_lower = all(1<=k<=15 for k in idxs)
        in_upper = all(16<=k<=31 for k in idxs)
        if in_lower: lower.add(fs)
        elif in_upper: upper.add(fs)
        else: crossing.add(fs)
    print(f"   entirely in lower 16D copy (idx 1..15):  {len(lower)}  (predict 84 = the sedenion ZDs)")
    print(f"   entirely in upper indices (16..31):       {len(upper)}")
    print(f"   crossing (mix lower & upper):             {len(crossing)}")
    print(f"   total:                                     {len(lower)+len(upper)+len(crossing)} = {len(un32)}")
    print(f"   NEW at 32D (upper + crossing):            {len(upper)+len(crossing)}")
    if len(lower)==len(un16):
        print(f"   >>> CONFIRMED: the 84 sedenion ZD pairs embed unchanged in 32D")
    else:
        print(f"   >>> sedenion pairs do NOT embed 1:1 ({len(lower)} vs {len(un16)})")

    # ---- structure of the NEW ones: index-XOR pattern ---------------------
    print("\n=== Structure probe: XOR pattern of each ZD pair's 4 indices ===")
    def xor4(fs):
        idxs=[]
        for (i,j) in fs: idxs+=[i,j]
        x=0
        for k in idxs: x^=k
        return x
    from collections import Counter
    xc_lower = Counter(xor4(fs) for fs in lower)
    xc_cross = Counter(xor4(fs) for fs in crossing)
    xc_upper = Counter(xor4(fs) for fs in upper)
    print(f"   lower-copy ZD pairs, index XOR distribution: {dict(xc_lower)}")
    print(f"   crossing ZD pairs,   index XOR distribution: {dict(xc_cross)}")
    print(f"   upper-only ZD pairs, index XOR distribution: {dict(xc_upper)}")
    print("   (XOR=0 over the 4 indices is the sedenion 'Fano-coline' signature;")
    print("    a clean single value across a class = a structured, not random, set)")
