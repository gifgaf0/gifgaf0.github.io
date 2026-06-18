"""
Validate the analytic reduction used in the inductive proof sketch.

The sketch claims a crossing (bridge) pair { (p1, D+q1), (p2, D+q2) } in A_{n+1}
(D = 2^n) is a two-term zero divisor IFF
  (i)  difference-lock:  p1^p2 == q1^q2   (forced by index-XOR=0), AND
  (ii) cocycle condition (dagger):
         sigma_n(q2,p1) == -sigma_n(p1,p2)*sigma_n(q2,q1)*sigma_n(q1,p2)
where sigma_n is the level-n CD sign cocycle (lower-block of A_{n+1}).

This script checks, against the honest brute-force ZD test:
  (A) the cocycle recursion / table gives sigma; build sigma_n from the table.
  (B) for EVERY crossing pair, "brute says ZD"  ==  "(i) and (ii) hold".
  (C) property (P_n): for every distinct nonzero q1,q2 there EXISTS a lower pair
      (p1,p2) with p1^p2=q1^q2 satisfying (dagger) -> every PG(n-1,2) line is
      witnessed. (This is the completeness statement the induction needs.)

Run at the doubling A_4->A_5 (32D) in full brute, and (P_n) alone at n=4..7.
"""
from itertools import combinations
from pathion128_pg52 import build_cd_table

def sigma_of(M, DIM):
    return [[M[i][j][1] for j in range(DIM)] for i in range(DIM)]

def crossing_zd_brute(M, DIMup, p):
    """All crossing two-term canonical ZD pairs in A_{n+1} (DIMup = 2^{n+1})."""
    D = DIMup//2
    def bv(i): v=[0]*DIMup; v[i]=1; return v
    def mul(x,y):
        r=[0]*DIMup
        for i in range(DIMup):
            if x[i]==0: continue
            for j in range(DIMup):
                if y[j]==0: continue
                k,s=M[i][j]
                if s: r[k]=(r[k]+x[i]*y[j]*s)%p
        return r
    def isz(v): return all(c%p==0 for c in v)
    def ad(x,y): return [(a+b)%p for a,b in zip(x,y)]
    def sc(x,s): return [(c*s)%p for c in x]
    im=list(range(1,DIMup)); P=set()
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
    # keep only pure-crossing pairs (both assessors span lower/upper)
    def isc(pr): a,b=pr; return (a<D and b>=D) or (a>=D and b<D)
    return {fs for fs in P if all(isc(pr) for pr in fs)}

def analytic_is_crossing_zd(sig, D, assessorpair):
    """Does (i)+(ii) hold for a crossing pair {(p1,D+q1),(p2,D+q2)}?"""
    prs=list(assessorpair)
    if len(prs)!=2: return False
    def split(pr):
        a,b=pr
        lo = a if a<D else b
        up = (b if a<D else a) - D
        return lo, up
    p1,q1 = split(prs[0]); p2,q2 = split(prs[1])
    if p1==p2 or q1==q2: return False
    if (p1^p2) != (q1^q2): return False           # (i) difference-lock
    # (ii) dagger
    lhs = sig[q2][p1]
    rhs = -sig[p1][p2]*sig[q2][q1]*sig[q1][p2]
    return lhs==rhs

def property_Pn(sig, D):
    """For every distinct nonzero q1,q2 in F_2^n (n=log2 D), is there a nonzero
       p not in {0,delta} with (dagger)?  Returns (#lines, #witnessed)."""
    pts=list(range(1,D))
    lines=set(frozenset([a,b,a^b]) for a,b in combinations(pts,2) if (a^b)!=0)
    witnessed=set()
    for q1,q2 in combinations(pts,2):
        delta=q1^q2
        ok=False
        for p1 in range(1,D):
            if p1==0 or p1==delta: continue
            p2=p1^delta
            if p2==0 or p2==p1: continue
            if sig[q2][p1] == -sig[p1][p2]*sig[q2][q1]*sig[q1][p2]:
                ok=True; break
        if ok:
            witnessed.add(frozenset([q1,q2,delta]))
    return len(lines), len(witnessed)

if __name__=="__main__":
    p=911
    print("=== (B) analytic reduction vs brute force, doubling A_4->A_5 (32D) ===")
    M5=build_cd_table(5)            # A_5 = 32D ; lower block = A_4, D=16
    sig4=sigma_of(M5,16)           # sigma_4 = lower-block signs
    brute=crossing_zd_brute(M5,32,p)
    D=16
    def involves_generator(fs):
        # generator e_D has reduction 0: upper index == D exactly
        return any((D in pr) for pr in fs)
    brute_gen   = {fs for fs in brute if involves_generator(fs)}
    brute_nonz  = brute - brute_gen
    print(f"  brute crossing ZD pairs total: {len(brute)}  "
          f"(generator-involving {len(brute_gen)}, nonzero-reduction {len(brute_nonz)})")

    # analytic set on the NONZERO-reduction domain (the proof's domain)
    cross_nonz=[(lo, D+up) for lo in range(1,D) for up in range(1,D)]
    analytic_nonz=set()
    for A1,A2 in combinations(cross_nonz,2):
        fs=frozenset([A1,A2])
        if analytic_is_crossing_zd(sig4,D,fs):
            analytic_nonz.add(fs)
    print(f"  analytic (diff-lock+dagger), nonzero domain: {len(analytic_nonz)}")
    print(f"  identical to brute-nonzero: {analytic_nonz==brute_nonz}   <<< reduction validated")
    if analytic_nonz!=brute_nonz:
        print(f"  brute-only {len(brute_nonz-analytic_nonz)}, "
              f"analytic-only {len(analytic_nonz-brute_nonz)}")

    print("\n=== (C) property (P_n): every PG(n-1,2) line witnessed via (dagger) ===")
    for nlev,D in [(4,16),(5,32),(6,64),(7,128)]:
        M=build_cd_table(nlev+1)
        sig=sigma_of(M,D)
        nlines,nwit=property_Pn(sig,D)
        print(f"  n={nlev} (doubling to {2*D}D, PG({nlev-1},2)): "
              f"lines={nlines}, witnessed via (dagger)={nwit}, all={nlines==nwit}")
