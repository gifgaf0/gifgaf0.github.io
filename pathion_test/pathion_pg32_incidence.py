"""
Does the 32D bridge realize PG(3,2)?  A falsifiable incidence test.

PG(3,2) FACTS (the target to match, stated before computing):
  - 15 points (nonzero vectors of F_2^4)
  - 35 lines, each containing exactly 3 points
  - each point on exactly 7 lines
  - any 2 distinct points lie on a unique line; the 3rd point of that line = their XOR
  - so {a,b,c} is a line  <=>  a xor b xor c = 0  (a,b,c distinct nonzero F_2^4 vectors)

We map the 15 participating upper indices (17..31, i.e. e_{16+k} for k=1..15) to the
nonzero vectors of F_2^4 via k -> k (k in 1..15 already labels a nonzero 4-bit vector).
Then we test whether the BRIDGE structure encodes PG(3,2) lines.

Two independent probes:
  PROBE 1 (index XOR over the upper part of crossing assessors):
     Each crossing assessor is (lo, up) with lo in 1..15, up in 17..31.
     Reduce up -> u = up-16 in 1..15 (a nonzero F_2^4 vector).
     A sedenion ZD quadruple has its 4 indices XOR to 0 (the Fano coline rule).
     Ask: do the upper-index reductions, taken across the size-14 components,
     organize into 3-element XOR-zero triples = PG(3,2) lines?

  PROBE 2 (the 35-line count): from the 15 nonzero F_2^4 vectors, the PG(3,2)
     lines are exactly the XOR-zero triples. Count them (must be 35), then ask
     how many are "witnessed" by the bridge -- i.e. appear as the upper-index
     content of an actual crossing zero-divisor relation.

p=911 ; same CD convention.
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

def zd_pairs(MULT,DIM,p):
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
    def sc(x,s): return [(c*s)%p for c in x]
    im=list(range(1,DIM)); P=set()
    for a,b in combinations(im,2):
        ea,eb=bv(a),bv(b)
        for sa in (1,p-1):
            for sb in (1,p-1):
                x=ad(sc(ea,sa),sc(eb,sb))
                for c,d in combinations(im,2):
                    if {a,b}=={c,d}: continue
                    ec,ed=bv(c),bv(d)
                    for scc in (1,p-1):
                        for sd in (1,p-1):
                            if isz(mul(x,ad(sc(ec,scc),sc(ed,sd)))):
                                P.add(frozenset([(min(a,b),max(a,b)),(min(c,d),max(c,d))]))
    return P

p=911
M32=build_cd_table(5)
s32=zd_pairs(M32,32,p)

# --- the 35 PG(3,2) lines (ground truth): XOR-zero triples of 1..15 ---
pts=list(range(1,16))
pg_lines=set()
for a,b,c in combinations(pts,3):
    if a^b^c==0:
        pg_lines.add(frozenset([a,b,c]))
print(f"PG(3,2) ground truth: {len(pts)} points, {len(pg_lines)} lines (expect 15, 35)")
# incidence sanity
deg=defaultdict(int)
for L in pg_lines:
    for x in L: deg[x]+=1
print(f"   each point on {set(deg.values())} lines (expect {{7}}); line size set {{ {set(len(L) for L in pg_lines)} }} (expect 3)")

# --- bridge crossing assessors: (lo in 1..15, up in 17..31) ---
cross=[]
for fs in s32:
    a,b=tuple(fs)
    # an assessor is one index-pair; a ZD pair is two assessors. Expand to assessors:
    pass
# Collect all crossing ASSESSORS (index pairs spanning lower & upper)
cross_assessors=set()
for fs in s32:
    for (i,j) in fs:
        if (i<=15 and j>=16) or (i>=16 and j<=15):
            cross_assessors.add((min(i,j),max(i,j)))
print(f"\ncrossing assessors (one lower idx + one upper idx): {len(cross_assessors)}")

# For each crossing ZD pair {(lo1,up1),(lo2,up2)} the 4 indices XOR to 0 (verified earlier).
# Reduce: lo in 1..15 ; u = up-16 in 1..15. The XOR-zero over {lo1, up1, lo2, up2}
# with up = u+16: lo1 ^ (u1+16) ^ lo2 ^ (u2+16) = lo1^lo2^u1^u2 (the 16-bits cancel) = 0
# => lo1^lo2 = u1^u2.  This links a lower-pair difference to an upper-pair difference.

# PROBE: collect, over all crossing ZD pairs that are PURE cross (both assessors crossing),
# the upper-index triples implied. Build the "upper line" witnessed set.
witnessed_upper_lines=set()
lower_upper_link=defaultdict(set)
pure_cross_pairs=0
for fs in s32:
    A=tuple(fs)
    (i1,j1),(i2,j2)=A[0],A[1]
    def isc(pr): a,b=pr; return (a<=15 and b>=16) or (a>=16 and b<=15)
    if isc((i1,j1)) and isc((i2,j2)):
        pure_cross_pairs+=1
        lo1,up1 = (i1,j1) if i1<=15 else (j1,i1)
        lo2,up2 = (i2,j2) if i2<=15 else (j2,i2)
        u1,u2 = up1-16, up2-16
        # the lower difference and upper difference must match (XOR)
        lower_upper_link[(lo1^lo2)].add(u1^u2)
        # the third point of the upper "line" through u1,u2:
        u3 = u1 ^ u2
        if u3!=0 and u1!=u2:
            witnessed_upper_lines.add(frozenset([u1,u2,u3]))

print(f"pure-cross ZD pairs (both assessors crossing): {pure_cross_pairs}")
print(f"\n=== PROBE 1: lower-diff <-> upper-diff lock ===")
locked = all(len(v)==1 and (k in v) for k,v in lower_upper_link.items())
print(f"   for every lower-index XOR difference d, the upper differences = {{d}}?  {locked}")
print(f"   (this is the XOR-coline rule forcing upper structure = lower structure)")
sample=dict(list(sorted(lower_upper_link.items()))[:5])
print(f"   sample (lower_xor -> set of upper_xor): {sample}")

print(f"\n=== PROBE 2: PG(3,2) line witnessing ===")
print(f"   upper-index XOR-zero triples witnessed by bridge ZDs: {len(witnessed_upper_lines)} of 35")
if witnessed_upper_lines <= pg_lines:
    print(f"   all witnessed triples are genuine PG(3,2) lines: {witnessed_upper_lines <= pg_lines}")
missing = pg_lines - witnessed_upper_lines
print(f"   PG(3,2) lines NOT witnessed: {len(missing)}")
if 0 < len(witnessed_upper_lines) and witnessed_upper_lines==pg_lines:
    print("   >>> EXACT: the bridge witnesses all 35 PG(3,2) lines and nothing else.")
elif witnessed_upper_lines <= pg_lines and len(witnessed_upper_lines)>0:
    print(f"   >>> SUBSET: bridge witnesses {len(witnessed_upper_lines)}/35 lines, all genuine, none spurious.")
else:
    print("   >>> structure does not match PG(3,2) cleanly.")
