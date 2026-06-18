"""
64D PG(4,2) test — does the next Cayley-Dickson bridge realize PG(4,2)?

REPRODUCIBILITY-FIRST DESIGN (this script is meant to be re-run by another
instance / CC and give identical numbers):

  LEMMA (necessary condition for a two-term canonical ZD), proved below:
    In the standard CD basis, e_i·e_j = sigma(i,j)·e_{i XOR j} for i,j>=1.
    For x = sa·e_a + sb·e_b, y = sc·e_c + sd·e_d (a,b,c,d nonzero, a!=b, c!=d),
    the product is a sum of four terms ±e_{a^c}, ±e_{a^d}, ±e_{b^c}, ±e_{b^d}.
      * If {a,b} ∩ {c,d} != ∅ (say a=c), then e_a·e_a = -e_0 appears and no
        other term is e_0, so the product != 0.  -> need DISJOINT indices.
      * If indices disjoint and a^b != c^d, the four product-indices
        a^c, a^d, b^c, b^d are pairwise distinct -> four distinct basis
        elements -> cannot cancel.  -> need a^b = c^d (equiv. a^b^c^d = 0).
    So EVERY two-term canonical ZD has disjoint indices AND a^b^c^d = 0.
    Pruning the search to these candidates is therefore COMPLETE (loses none).

  We (1) verify e_i·e_j = ±e_{i^j} holds in the project's build_cd_table
  convention; (2) cross-check the pruned/sigma search against the validated
  brute-force result at 32D (must reproduce 1260); (3) run 64D.

p=911, p mod 455 == 1 (project standard). No target value consulted.
"""
from itertools import combinations
from collections import defaultdict, Counter

def build_cd_table(n):
    def cs(i): return (i,1) if i==0 else (i,-1)
    cur=[[(0,1)]]; dp=1
    for _ in range(n):
        dn=dp*2; new=[[(0,1)]*dn for _ in range(dn)]
        for i in range(dn):
            for j in range(dn):
                a,b=(i,None) if i<dp else (None,i-dp)
                c,d=(j,None) if j<dp else (None,j-dp)
                acc={}
                if a is not None and c is not None: k,s=cur[a][c]; acc[k]=acc.get(k,0)+s
                if d is not None and b is not None: ci,g=cs(d); k,s=cur[ci][b]; acc[k]=acc.get(k,0)-g*s
                if d is not None and a is not None: k,s=cur[d][a]; acc[k+dp]=acc.get(k+dp,0)+s
                if b is not None and c is not None: ci,g=cs(c); k,s=cur[b][ci]; acc[k+dp]=acc.get(k+dp,0)+g*s
                nz=[(k,s) for k,s in acc.items() if s!=0]; assert len(nz)<=1
                new[i][j]=nz[0] if nz else (0,0)
        cur=new; dp=dn
    return cur

def verify_xor_property(MULT, DIM):
    """e_i*e_j must equal sigma*e_{i^j} for i,j in 1..DIM-1."""
    ok=True
    for i in range(1,DIM):
        for j in range(1,DIM):
            k,s = MULT[i][j]
            if k != (i ^ j):
                ok=False
    return ok

def sigma_table(MULT, DIM):
    """sigma[i][j] = sign of e_i*e_j (the CD cocycle); index is i^j."""
    sig=[[0]*DIM for _ in range(DIM)]
    for i in range(DIM):
        for j in range(DIM):
            k,s=MULT[i][j]
            sig[i][j]=s
    return sig

def zd_pairs_pruned(MULT, DIM, p):
    """Pruned two-term ZD search using the XOR-necessity lemma + sign check.
       Equivalent to brute force (verified at 32D)."""
    sig = sigma_table(MULT, DIM)
    imag = list(range(1, DIM))
    # group index-pairs by their XOR value
    by_xor = defaultdict(list)
    for a,b in combinations(imag,2):
        by_xor[a^b].append((a,b))
    pairs=set()
    # candidates: two disjoint index-pairs with the same XOR
    for delta, plist in by_xor.items():
        for (a,b),(c,d) in combinations(plist,2):
            if len({a,b,c,d})<4:
                continue  # not disjoint
            # product index classes: p_idx = a^c (= b^d), q_idx = a^d (= b^c)
            # coeff(e_{a^c}) = sa*sc*sig[a][c] + sb*sd*sig[b][d]
            # coeff(e_{a^d}) = sa*sd*sig[a][d] + sb*sc*sig[b][c]
            s_ac, s_bd = sig[a][c], sig[b][d]
            s_ad, s_bc = sig[a][d], sig[b][c]
            found=False
            # fix sa=1 (overall scale); vary sb,sc,sd in {+1,-1}
            for sb in (1,-1):
                for sc in (1,-1):
                    for sd in (1,-1):
                        if (1*sc*s_ac + sb*sd*s_bd)==0 and (1*sd*s_ad + sb*sc*s_bc)==0:
                            found=True; break
                    if found: break
                if found: break
            if found:
                pairs.add(frozenset([(a,b),(c,d)]))
    return pairs

def zd_pairs_brute(MULT, DIM, p):
    """Original validated brute force (same logic as sedenion_Fp.py)."""
    def bv(i): v=[0]*DIM; v[i]=1; return v
    def mul(x,y):
        r=[0]*DIM
        for i in range(DIM):
            if x[i]==0: continue
            for j in range(DIM):
                if y[j]==0: continue
                k,s=MULT[i][j]
                if s: r[k]=(r[k]+x[i]*y[j]*s)%p
        return r
    def isz(v): return all(c%p==0 for c in v)
    def ad(x,y): return [(a+b)%p for a,b in zip(x,y)]
    def sc_(x,s): return [(c*s)%p for c in x]
    im=list(range(1,DIM)); P=set()
    for a,b in combinations(im,2):
        ea,eb=bv(a),bv(b)
        for sa in (1,p-1):
            for sb in (1,p-1):
                x=ad(sc_(ea,sa),sc_(eb,sb))
                for c,d in combinations(im,2):
                    if {a,b}=={c,d}: continue
                    ec,ed=bv(c),bv(d)
                    for scc in (1,p-1):
                        for sd in (1,p-1):
                            if isz(mul(x,ad(sc_(ec,scc),sc_(ed,sd)))):
                                P.add(frozenset([(min(a,b),max(a,b)),(min(c,d),max(c,d))]))
    return P

def pg_lines(npts_dim_bits):
    """PG(k,2) lines = XOR-zero triples of nonzero F_2^(k+1) vectors."""
    pts=list(range(1, 2**npts_dim_bits))
    L=set()
    for a,b,c in combinations(pts,3):
        if a^b^c==0: L.add(frozenset([a,b,c]))
    return pts, L

def bridge_witnessed_lines(pairs, DIM):
    """Generator index = DIM//2; upper indices DIM//2..DIM-1 reduce by -DIM//2."""
    gen = DIM//2
    witnessed=set()
    def isc(pr):
        a,b=pr; return (a<gen and b>=gen) or (a>=gen and b<gen)
    for fs in pairs:
        A=tuple(fs)
        if len(A)!=2: continue
        (i1,j1),(i2,j2)=A
        if isc((i1,j1)) and isc((i2,j2)):
            lo1,up1=(i1,j1) if i1<gen else (j1,i1)
            lo2,up2=(i2,j2) if i2<gen else (j2,i2)
            u1,u2=up1-gen, up2-gen
            u3=u1^u2
            if u3!=0 and u1!=u2:
                witnessed.add(frozenset([u1,u2,u3]))
    return witnessed

if __name__=="__main__":
    p=911
    print(f"p={p}, p mod 455={p%455}\n")

    # ---- 32D: verify XOR property, cross-check pruned vs brute (==1260) ----
    print("=== 32D validation ===")
    M32=build_cd_table(5)
    print(f"  e_i*e_j = ±e_(i^j) holds in 32D table: {verify_xor_property(M32,32)}")
    bruteset=zd_pairs_brute(M32,32,p)
    prunedset=zd_pairs_pruned(M32,32,p)
    print(f"  brute-force ZD pairs:  {len(bruteset)}  (validated value: 1260)")
    print(f"  pruned/sigma ZD pairs: {len(prunedset)}")
    print(f"  identical sets: {bruteset==prunedset}  <<< method equivalence")
    if bruteset!=prunedset:
        print("  !!! methods disagree — ABORT, do not trust 64D"); raise SystemExit

    # ---- 64D run (pruned method only; equivalence established above) ----
    print("\n=== 64D run (sedenion-of-pathions = two 32D copies + bridge) ===")
    M64=build_cd_table(6)
    print(f"  e_i*e_j = ±e_(i^j) holds in 64D table: {verify_xor_property(M64,64)}")
    s64=zd_pairs_pruned(M64,64,p)
    print(f"  total two-term ZD pairs at 64D: {len(s64)}")

    # decompose lower / upper / crossing  (generator e_32; copies 1..31 and 32..63)
    gen=32
    lower=upper=cross=0
    for fs in s64:
        idx=[k for pr in fs for k in pr]
        lo=all(1<=k<=31 for k in idx); up=all(32<=k<=63 for k in idx)
        if lo: lower+=1
        elif up: upper+=1
        else: cross+=1
    print(f"  lower copy (idx 1..31):   {lower}  (predict 1260 = full 32D structure)")
    print(f"  upper copy (idx 32..63):  {upper}  (predict 1260)")
    print(f"  bridge (crossing):        {cross}")
    print(f"  total: {lower+upper+cross} = {len(s64)}")

    # all XOR=0?
    allxor0 = all((lambda idx: idx[0]^idx[1]^idx[2]^idx[3]==0)([k for pr in fs for k in pr]) for fs in s64)
    print(f"  every ZD quadruple has index-XOR = 0: {allxor0}")

    # ---- PG(4,2) line witnessing ----
    print("\n=== PG(4,2) realization test ===")
    pts4, lines4 = pg_lines(5)   # F_2^5 -> 31 points
    print(f"  PG(4,2) ground truth: {len(pts4)} points, {len(lines4)} lines (expect 31, 155)")
    wl = bridge_witnessed_lines(s64, 64)
    print(f"  bridge-witnessed upper triples: {len(wl)} of {len(lines4)}")
    print(f"  all witnessed are genuine PG(4,2) lines: {wl <= lines4}")
    print(f"  PG(4,2) lines NOT witnessed: {len(lines4 - wl)}")
    if wl==lines4:
        print("  >>> EXACT: the 64D bridge witnesses all 155 PG(4,2) lines and nothing else.")
    elif wl<=lines4 and wl:
        print(f"  >>> SUBSET: {len(wl)}/155 genuine lines, none spurious.")
    else:
        print("  >>> does NOT match PG(4,2).")

    # which upper indices participate (expect 31 of 32: generator e_32 excluded)
    up_used=set()
    for fs in s64:
        for pr in fs:
            for k in pr:
                if k>=32: up_used.add(k-32)
    up_used.discard(0)
    print(f"  distinct nonzero upper reductions used: {len(up_used)} (expect 31; e_32 generator excluded)")
