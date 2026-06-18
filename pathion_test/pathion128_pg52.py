"""
128D PG(5,2) test -- third consecutive Cayley-Dickson doubling.

Continues the verified recursion PG(2,2) [octonions] -> PG(3,2) [16->32] ->
PG(4,2) [32->64].  Claim under test: the 64D->128D bridge realizes PG(5,2)
exactly (63 points = nonzero F_2^6 vectors, 651 lines = XOR-zero triples),
with the doubling generator e_64 excluded, and the two 64D copies (1..63 and
64..127) embedded intact.

METHOD (same discipline as pathion64_pg42.py):
  The two-term canonical ZD lemma (proved in pathion64_pg42.py header) is
  dimension-general: a two-term canonical ZD must have DISJOINT indices and
  a^b^c^d = 0; pruning to those candidates is COMPLETE. The pruned/sigma search
  uses only the CD cocycle sigma(i,j) in {+1,-1} -- NO prime appears -- so the
  result is field-class-independent by construction. Implementation is validated
  by reproducing the brute-force ZD set at 32D (in this script) and, separately,
  at 64D (pathion64_brute_check.py, run alongside). The XOR property
  e_i*e_j = +-e_{i^j} is verified at 32/64/128 before any count is trusted.

No target value consulted; counts reported as found (Eddington guard).
"""
from itertools import combinations
from collections import defaultdict

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
    for i in range(1,DIM):
        for j in range(1,DIM):
            k,_=MULT[i][j]
            if k != (i ^ j): return False
    return True

def sigma_table(MULT, DIM):
    return [[MULT[i][j][1] for j in range(DIM)] for i in range(DIM)]

def zd_pairs_pruned(MULT, DIM):
    """Pruned two-term ZD search (disjoint + XOR=0 + sign cancellation).
       Field-class-independent: uses only sigma in {+1,-1}, no prime."""
    sig = sigma_table(MULT, DIM)
    imag = list(range(1, DIM))
    by_xor = defaultdict(list)
    for a,b in combinations(imag,2):
        by_xor[a^b].append((a,b))
    pairs=set()
    for delta, plist in by_xor.items():
        for (a,b),(c,d) in combinations(plist,2):
            if len({a,b,c,d})<4: continue
            s_ac,s_bd = sig[a][c],sig[b][d]
            s_ad,s_bc = sig[a][d],sig[b][c]
            found=False
            for sb in (1,-1):
                for sc in (1,-1):
                    for sd in (1,-1):
                        if (sc*s_ac + sb*sd*s_bd)==0 and (sd*s_ad + sb*sc*s_bc)==0:
                            found=True; break
                    if found: break
                if found: break
            if found:
                pairs.add(frozenset([(a,b),(c,d)]))
    return pairs

def zd_pairs_brute(MULT, DIM, p):
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

def pg_lines(bits):
    pts=list(range(1, 2**bits))
    L=set()
    for a,b,c in combinations(pts,3):
        if a^b^c==0: L.add(frozenset([a,b,c]))
    return pts, L

def bridge_witnessed_lines(pairs, DIM):
    gen = DIM//2
    witnessed=set()
    def isc(pr):
        a,b=pr; return (a<gen and b>=gen) or (a>=gen and b<gen)
    for fs in pairs:
        A=tuple(fs)
        if len(A)!=2: continue
        (i1,j1),(i2,j2)=A
        if isc((i1,j1)) and isc((i2,j2)):
            up1=i1 if i1>=gen else j1
            up2=i2 if i2>=gen else j2
            u1,u2=up1-gen, up2-gen
            u3=u1^u2
            if u3!=0 and u1!=u2:
                witnessed.add(frozenset([u1,u2,u3]))
    return witnessed

if __name__=="__main__":
    p=911
    print(f"p={p} (used only for the 32D brute equivalence leg; pruned method is prime-free)\n")

    # ---- 32D implementation validation: pruned == brute ----
    print("=== 32D implementation check (pruned vs brute) ===")
    M32=build_cd_table(5)
    print(f"  XOR property holds at 32D: {verify_xor_property(M32,32)}")
    b32=zd_pairs_brute(M32,32,p); pr32=zd_pairs_pruned(M32,32)
    print(f"  brute={len(b32)}  pruned={len(pr32)}  identical={b32==pr32}  (expect 1260, True)")
    if b32!=pr32:
        print("  !!! pruned != brute at 32D -- ABORT"); raise SystemExit

    # ---- 64D sanity (pruned; equivalence proven separately in brute_check) ----
    print("\n=== 64D recheck (pruned) ===")
    M64=build_cd_table(6)
    print(f"  XOR property holds at 64D: {verify_xor_property(M64,64)}")
    s64=zd_pairs_pruned(M64,64)
    print(f"  64D total pruned ZD pairs: {len(s64)}  (expect 13020)")

    # ---- 128D run ----
    print("\n=== 128D run (sedenion-of-64D = two 64D copies + bridge) ===")
    M128=build_cd_table(7)
    print(f"  XOR property holds at 128D: {verify_xor_property(M128,128)}")
    s128=zd_pairs_pruned(M128,128)
    print(f"  total two-term ZD pairs at 128D: {len(s128)}")

    gen=64
    lower=upper=cross=0
    for fs in s128:
        idx=[k for pr in fs for k in pr]
        lo=all(1<=k<=63 for k in idx); up=all(64<=k<=127 for k in idx)
        if lo: lower+=1
        elif up: upper+=1
        else: cross+=1
    print(f"  lower copy (idx 1..63):    {lower}  (predict 13020 = full 64D structure)")
    print(f"  upper copy (idx 64..127):  {upper}  (predict 13020)")
    print(f"  bridge (crossing):         {cross}")
    print(f"  total: {lower+upper+cross} = {len(s128)}")

    allxor0 = all((lambda i: i[0]^i[1]^i[2]^i[3]==0)([k for pr in fs for k in pr]) for fs in s128)
    print(f"  every ZD quadruple has index-XOR = 0: {allxor0}")

    # ---- PG(5,2) line witnessing ----
    print("\n=== PG(5,2) realization test ===")
    pts5, lines5 = pg_lines(6)   # F_2^6 -> 63 points
    deg=defaultdict(int)
    for L in lines5:
        for x in L: deg[x]+=1
    print(f"  PG(5,2) ground truth: {len(pts5)} points, {len(lines5)} lines "
          f"(expect 63, 651); each point on {set(deg.values())} lines (expect {{31}})")
    wl = bridge_witnessed_lines(s128, 128)
    print(f"  bridge-witnessed upper triples: {len(wl)} of {len(lines5)}")
    print(f"  all witnessed are genuine PG(5,2) lines: {wl <= lines5}")
    print(f"  PG(5,2) lines NOT witnessed: {len(lines5 - wl)}")
    if wl==lines5:
        print("  >>> EXACT: the 128D bridge witnesses all 651 PG(5,2) lines and nothing else.")
    elif wl<=lines5 and wl:
        print(f"  >>> SUBSET: {len(wl)}/651 genuine lines, none spurious.")
    else:
        print("  >>> does NOT match PG(5,2).")

    up_used=set()
    for fs in s128:
        for pr in fs:
            for k in pr:
                if k>=64: up_used.add(k-64)
    up_used.discard(0)
    print(f"  distinct nonzero upper reductions used: {len(up_used)} (expect 63; e_64 generator excluded)")
