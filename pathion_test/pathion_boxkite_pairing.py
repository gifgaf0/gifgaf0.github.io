"""
Test the R2 reading: are the seven size-12 bridge components exactly the
lower<->upper pairings of corresponding sedenion box-kites?

FALSIFIABLE CLAIM (pre-registered):
  Each size-12 crossing component C splits as 6 lower-assessors + 6 upper-assessors,
  AND  (a) the 6 lower assessors are EXACTLY one of the 7 sedenion box-kites;
       (b) the 6 upper assessors are the +16 index-shift image of that SAME box-kite.
  If (a)+(b) hold for all 7 size-12 components -> reading CONFIRMED (the bridge
  stitches each box-kite to its own image).
  Any deviation (split != 6+6, lower set not a box-kite, upper != image) -> reading FAILS.

Also probe the fifteen size-14 components: lower/upper/mixed assessor counts,
and whether their index structure points at PG(3,2) (15 points).

Same CD convention, p=911.
"""
from itertools import combinations
from collections import defaultdict, Counter

def build_cd_table(n_levels):
    def cs(idx): return (idx,1) if idx==0 else (idx,-1)
    cur=[[(0,1)]]; dp=1
    for _ in range(n_levels):
        dn=dp*2; new=[[(0,1)]*dn for _ in range(dn)]
        for i in range(dn):
            for j in range(dn):
                a,b=(i,None) if i<dp else (None,i-dp)
                c,d=(j,None) if j<dp else (None,j-dp)
                acc={}
                if a is not None and c is not None: k,s=cur[a][c]; acc[k]=acc.get(k,0)+s
                if d is not None and b is not None: ci,csg=cs(d); k,s=cur[ci][b]; acc[k]=acc.get(k,0)-csg*s
                if d is not None and a is not None: k,s=cur[d][a]; acc[k+dp]=acc.get(k+dp,0)+s
                if b is not None and c is not None: ci,csg=cs(c); k,s=cur[b][ci]; acc[k+dp]=acc.get(k+dp,0)+csg*s
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

def graph(pairs):
    adj=defaultdict(set); nodes=set()
    for fs in pairs:
        u,v=tuple(fs); nodes|={u,v}; adj[u].add(v); adj[v].add(u)
    return nodes,adj

def comps(nodes,adj):
    seen=set(); out=[]
    for n in nodes:
        if n in seen: continue
        st=[n]; c=set()
        while st:
            u=st.pop()
            if u in seen: continue
            seen.add(u); c.add(u); st.extend(adj[u]-seen)
        out.append(c)
    return out

p=911
M16=build_cd_table(4); M32=build_cd_table(5)

# sedenion box-kites (the 7 reference components, as assessor sets)
s16=zd_pairs(M16,16,p)
n16,a16=graph(s16)
boxkites=[frozenset(c) for c in comps(n16,a16)]
print(f"sedenion box-kites: {len(boxkites)} components, sizes {sorted(len(b) for b in boxkites)}")

# 32D crossing stratum
s32=zd_pairs(M32,32,p)
def is_cross(fs):
    idx=[k for pr in fs for k in pr]
    return not all(1<=k<=15 for k in idx) and not all(16<=k<=31 for k in idx)
cross={fs for fs in s32 if is_cross(fs)}
nC,aC=graph(cross)
cc=comps(nC,aC)
size12=[c for c in cc if len(c)==12]
size14=[c for c in cc if len(c)==14]
print(f"\ncrossing components: {len(cc)} total; size-12: {len(size12)}, size-14: {len(size14)}")

def shift_down(asr):  # map an upper assessor (16..31) to lower by -16 on any idx>=16
    return tuple(sorted((k-16 if k>=16 else k) for k in asr))

print("\n=== Size-12 components: box-kite pairing test ===")
all_confirmed=True
for i,c in enumerate(size12):
    lower=set(); upper=set(); mixed=set()
    for asr in c:
        a,b=asr
        if a<=15 and b<=15: lower.add(asr)
        elif a>=16 and b>=16: upper.add(asr)
        else: mixed.add(asr)
    # (a) split 6+6?
    split_ok = (len(lower)==6 and len(upper)==6 and len(mixed)==0)
    # (b) lower 6 == one sedenion box-kite?
    lower_fs=frozenset(lower)
    is_bk = lower_fs in boxkites
    # (c) upper 6 shifted down == same box-kite?
    upper_shifted=frozenset(shift_down(a) for a in upper)
    upper_is_image = (upper_shifted == lower_fs)
    ok = split_ok and is_bk and upper_is_image
    all_confirmed &= ok
    bk_id = boxkites.index(lower_fs) if is_bk else None
    print(f"  C{i}: split6+6={split_ok}  lower=box-kite#{bk_id}  upper=image-of-same={upper_is_image}  -> {'OK' if ok else 'DEVIATION'}")
    if not split_ok:
        print(f"       counts lower/upper/mixed = {len(lower)}/{len(upper)}/{len(mixed)}")

print(f"\n  >>> Size-12 = box-kite self-pairings: {'CONFIRMED for all 7' if all_confirmed else 'READING FAILS'}")

print("\n=== Size-14 components: lower/upper/mixed composition ===")
comp_profiles=Counter()
for c in size14:
    lo=up=mx=0
    for a,b in c:
        if a<=15 and b<=15: lo+=1
        elif a>=16 and b>=16: up+=1
        else: mx+=1
    comp_profiles[(lo,up,mx)]+=1
print(f"   (lower,upper,mixed) assessor-count profiles across the 15 size-14 comps:")
for prof,cnt in sorted(comp_profiles.items()):
    print(f"      {prof}: {cnt} components")

# PG(3,2) probe: collect the distinct upper indices used across all size-14 comps
up_indices=set()
for c in size14:
    for a,b in c:
        for k in (a,b):
            if k>=16: up_indices.add(k)
print(f"   distinct upper indices (16..31) used by size-14 comps: {len(up_indices)} of 16")
print(f"   (PG(3,2) has 15 points; the 15 nonzero vectors of F_2^4)")
