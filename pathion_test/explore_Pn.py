"""
Exploration toward a proof of (P_n) -- the cocycle completeness property.

(P_n): for all distinct nonzero q1,q2 in F_2^n (delta=q1^q2), exists nonzero
p not in {0,delta} with
   G(p) := sigma_n(q2,p) sigma_n(p,p^delta) sigma_n(q1,p^delta) sigma_n(q2,q1) = -1.

Goals:
  1. confirm a witness always exists (#witnesses >= 1), and tabulate the
     distribution of #witnesses over all (q1,q2) -- is it constant? nice formula?
  2. test candidate UNIFORM witness rules p=f(q1,q2) that might be provable.
  3. probe structure: is G(p)=-1 equivalent to a known relation (internal-ZD
     resonance / anticommutativity / associator) on the 4 points {q1,q2,p,p^delta}?
"""
from itertools import combinations
from collections import Counter
from pathion128_pg52 import build_cd_table

def sigma_of(M, DIM):
    return [[M[i][j][1] for j in range(DIM)] for i in range(DIM)]

def witnesses(sig, D, q1, q2):
    delta=q1^q2
    out=[]
    for p in range(1,D):
        if p==0 or p==delta: continue
        p2=p^delta
        if p2==0 or p2==p: continue
        G = sig[q2][p]*sig[p][p2]*sig[q1][p2]*sig[q2][q1]
        if G==-1: out.append(p)
    return out

def assoc(sig, i, j, k):
    """associator sign A(i,j,k) = sigma(i,j)sigma(i^j,k)sigma(j,k)sigma(i,j^k)."""
    return sig[i][j]*sig[i^j][k]*sig[j][k]*sig[i][j^k]

if __name__=="__main__":
    for nlev,D in [(4,16),(5,32),(6,64)]:
        M=build_cd_table(nlev)
        sig=sigma_of(M,D)
        cnt=Counter()
        total_pairs=0
        minw=10**9
        # candidate uniform rules to test
        rule_hits={"p=q1^q2nonsense":0}
        examples=[]
        for q1,q2 in combinations(range(1,D),2):
            w=witnesses(sig,D,q1,q2)
            cnt[len(w)]+=1; total_pairs+=1; minw=min(minw,len(w))
            if len(examples)<3 and nlev==4:
                examples.append((q1,q2,w))
        print(f"n={nlev} (D={D}): pairs={total_pairs}, min #witnesses={minw}, "
              f"#witness distribution={dict(sorted(cnt.items()))}")
        if examples:
            for q1,q2,w in examples:
                print(f"    e.g. q1={q1},q2={q2},delta={q1^q2}: witnesses p={w}")

    # structural probe at n=4: is G(p)=-1 <=> some clean relation?
    print("\n=== structural probe n=4 ===")
    D=16; M=build_cd_table(4); sig=sigma_of(M,D)
    # test: does p chosen so that {q1,q2,p,p^delta} has all-pairs internal-ZD
    # resonance correlate? Also test associator pattern.
    # Hypothesis A: G(p) = -1  <=>  associator A(q2,p,p^delta-ish) ... explore raw.
    q1,q2=1,2; delta=q1^q2
    print(f"  q1={q1} q2={q2} delta={delta}")
    for p in range(1,D):
        if p in (0,delta): continue
        p2=p^delta
        if p2 in (0,p): continue
        G = sig[q2][p]*sig[p][p2]*sig[q1][p2]*sig[q2][q1]
        Aqpp = assoc(sig,q1,q2,p)
        print(f"    p={p:2d} p^delta={p2:2d}  G={G:+d}  A(q1,q2,p)={Aqpp:+d}")
