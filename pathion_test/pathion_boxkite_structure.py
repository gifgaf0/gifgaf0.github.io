"""
Box-kite organization of the 32D pathion zero-divisors, vs the sedenion 7-box-kite structure.

SEDENION BASELINE (literature, Moreno/Cawagas):
  - 42 assessors (imaginary index pairs that participate in a ZD)
  - organized into 7 box-kites of 6 assessors each (3 Row-A + 3 Row-B); 6x7=42
  - a box-kite = a maximal set of mutually co-dividing assessors (octahedron)

PRE-REGISTERED 32D QUESTIONS:
  (1) How many distinct ASSESSORS (index pairs) appear among the 1260 ZD pairs?
  (2) Build the "co-assessor" graph: nodes = assessors, edge = the two assessors
      form a canonical ZD pair together. What are its connected components?
  (3) Do the components have a box-kite-like uniform size/structure?
      Sedenion analog: the assessor graph organizes into 7 octahedra (box-kites).
  (4) Separate the 3 strata (lower/upper/crossing) and ask whether each stratum's
      assessors organize the same way.

No target value consulted; structure reported as found. Same CD convention,
same prime p=911 (p mod 455 == 1) as the project's sedenion tool.
"""
from itertools import combinations
from collections import defaultdict, Counter

def build_cd_table(n_levels):
    def conj_sign(idx): return (idx,1) if idx==0 else (idx,-1)
    cur=[[(0,1)]]; dim_prev=1
    for _ in range(n_levels):
        dim_new=dim_prev*2
        new=[[(0,1)]*dim_new for _ in range(dim_new)]
        for i in range(dim_new):
            for j in range(dim_new):
                a,b=(i,None) if i<dim_prev else (None,i-dim_prev)
                c,d=(j,None) if j<dim_prev else (None,j-dim_prev)
                acc={}
                if a is not None and c is not None:
                    k,s=cur[a][c]; acc[k]=acc.get(k,0)+s
                if d is not None and b is not None:
                    ci,cs=conj_sign(d); k,s=cur[ci][b]; acc[k]=acc.get(k,0)-cs*s
                if d is not None and a is not None:
                    k,s=cur[d][a]; kk=k+dim_prev; acc[kk]=acc.get(kk,0)+s
                if b is not None and c is not None:
                    ci,cs=conj_sign(c); k,s=cur[b][ci]; kk=k+dim_prev; acc[kk]=acc.get(kk,0)+cs*s
                nz=[(k,s) for k,s in acc.items() if s!=0]
                assert len(nz)<=1
                new[i][j]=nz[0] if nz else (0,0)
        cur=new; dim_prev=dim_new
    return cur

def two_term_zd_quadruples(MULT,DIM,p):
    def basis(i):
        v=[0]*DIM; v[i]=1; return v
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
    def add(x,y): return [(a+b)%p for a,b in zip(x,y)]
    def sca(x,s): return [(c*s)%p for c in x]
    imag=list(range(1,DIM)); pairs=set()
    for a,b in combinations(imag,2):
        ea,eb=basis(a),basis(b)
        for sa in (1,p-1):
            for sb in (1,p-1):
                x=add(sca(ea,sa),sca(eb,sb))
                for c,d in combinations(imag,2):
                    if {a,b}=={c,d}: continue
                    ec,ed=basis(c),basis(d)
                    for sc in (1,p-1):
                        for sd in (1,p-1):
                            if isz(mul(x,add(sca(ec,sc),sca(ed,sd)))):
                                pairs.add(frozenset([(min(a,b),max(a,b)),(min(c,d),max(c,d))]))
    return pairs

def assessor_graph(pairs):
    """nodes = assessors (index pairs), edges = co-dividing assessor pairs."""
    adj=defaultdict(set); nodes=set()
    for fs in pairs:
        a,b=tuple(fs)
        nodes.add(a); nodes.add(b); adj[a].add(b); adj[b].add(a)
    return nodes,adj

def components(nodes,adj):
    seen=set(); comps=[]
    for n in nodes:
        if n in seen: continue
        stack=[n]; comp=set()
        while stack:
            u=stack.pop()
            if u in seen: continue
            seen.add(u); comp.add(u)
            stack.extend(adj[u]-seen)
        comps.append(comp)
    return comps

def report(name, pairs):
    nodes,adj=assessor_graph(pairs)
    comps=components(nodes,adj)
    degs=Counter(len(adj[n]) for n in nodes)
    csizes=Counter(len(c) for c in comps)
    print(f"\n--- {name} ---")
    print(f"   ZD pairs: {len(pairs)}")
    print(f"   distinct assessors (nodes): {len(nodes)}")
    print(f"   co-assessor edges: {sum(len(adj[n]) for n in nodes)//2}")
    print(f"   connected components: {len(comps)}  | sizes: {dict(sorted(csizes.items()))}")
    print(f"   assessor degree distribution: {dict(sorted(degs.items()))}")
    return nodes,adj,comps

if __name__=="__main__":
    p=911
    print(f"p={p}, p mod 455={p%455}")

    print("\n========== SEDENION BASELINE (16D) ==========")
    M16=build_cd_table(4)
    s16=two_term_zd_quadruples(M16,16,p)
    n16,a16,c16=report("16D all ZD pairs",s16)
    # box-kite check: literature says 7 box-kites of 6 assessors, 42 assessors total
    print(f"   >>> sedenion check: {len(n16)} assessors (lit: 42), "
          f"{len(c16)} components (lit: 7 box-kites)")
    if c16:
        sizes=sorted(len(c)for c in c16)
        print(f"   >>> component sizes: {sizes}  (lit: seven 6-assessor box-kites)")

    print("\n========== PATHIONS (32D) ==========")
    M32=build_cd_table(5)
    s32=two_term_zd_quadruples(M32,32,p)

    # full
    n32,a32,c32=report("32D all ZD pairs",s32)

    # strata
    def stratum(pairs,which):
        out=set()
        for fs in pairs:
            idx=[k for pr in fs for k in pr]
            lo=all(1<=k<=15 for k in idx); up=all(16<=k<=31 for k in idx)
            if which=='lower' and lo: out.add(fs)
            elif which=='upper' and up: out.add(fs)
            elif which=='crossing' and not lo and not up: out.add(fs)
        return out

    report("32D lower-copy stratum",   stratum(s32,'lower'))
    report("32D upper stratum",        stratum(s32,'upper'))
    nC,aC,cC=report("32D crossing stratum (the bridge)", stratum(s32,'crossing'))

    # Does the crossing stratum organize into uniform units?
    print("\n=== Bridge (crossing) organization summary ===")
    csz=Counter(len(c) for c in cC)
    print(f"   crossing components and their sizes: {dict(sorted(csz.items()))}")
    print(f"   total crossing components: {len(cC)}")
    # how many assessors does each box-kite-like unit hold; is it uniform?
    if len(set(len(c) for c in cC))==1 and cC:
        print(f"   >>> UNIFORM: every crossing component has {len(cC[0])} assessors")
    else:
        print(f"   >>> NON-uniform component sizes in the bridge")
