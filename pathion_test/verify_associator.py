"""
Close (P_n) via the associator. The structural probe found G(p) = A(q1,q2,p).

  G(p)   := sigma(q2,p) sigma(p,p^delta) sigma(q1,p^delta) sigma(q2,q1)   [delta=q1^q2]
  A(i,j,k) := sigma(i,j) sigma(i^j,k) sigma(j,k) sigma(i,j^k)
             = associator sign of (e_i,e_j,e_k):  (e_i e_j)e_k = A * e_i(e_j e_k)

If  G(p) = A(q1,q2,p)  identically, then (P_n) -- "every PG(n-1,2) line is
witnessed" -- becomes exactly:

   (P_n')  for all distinct nonzero q1,q2 there is a p with A(q1,q2,p) = -1,
           i.e. e_{q1},e_{q2} fail to associate with SOME e_p.

That is the standard non-associativity of Cayley-Dickson algebras of dim>=8
(nucleus = base field). This script proves, for n=4..8:
  (L3) the identity  G(p) == A(q1,q2,p)  for ALL distinct nonzero q1,q2 and all
       valid p  (a finite, exhaustive check = a proof at each n);
  (L4) for every distinct nonzero q1,q2, #{p : A(q1,q2,p) = -1} >= 2^{n-1} > 0
       (so a witness always exists), and the count takes only the values seen.
"""
from itertools import combinations
from collections import Counter
from pathion128_pg52 import build_cd_table

def sigma_of(M, DIM):
    return [[M[i][j][1] for j in range(DIM)] for i in range(DIM)]

def assoc(sig, i, j, k):
    return sig[i][j]*sig[i^j][k]*sig[j][k]*sig[i][j^k]

if __name__=="__main__":
    print(f"{'n':>2} {'D':>4} | (L3) G==A identically | (L4) min witnesses | witness counts")
    print("-"*78)
    for nlev,D in [(4,16),(5,32),(6,64),(7,128),(8,256)]:
        M=build_cd_table(nlev); sig=sigma_of(M,D)
        identity_ok=True
        min_w=10**9
        wc=Counter()
        for q1,q2 in combinations(range(1,D),2):
            delta=q1^q2
            w=0
            for p in range(1,D):
                if p==0 or p==delta: continue
                p2=p^delta
                if p2==0 or p2==p: continue
                G  = sig[q2][p]*sig[p][p2]*sig[q1][p2]*sig[q2][q1]
                A  = assoc(sig,q1,q2,p)
                if G!=A: identity_ok=False
                if G==-1: w+=1
            min_w=min(min_w,w); wc[w]+=1
        powmin = 2**(nlev-1)
        print(f"{nlev:>2} {D:>4} | {str(identity_ok):>20} | {min_w:>6} "
              f"(2^(n-1)={powmin}) | {dict(sorted(wc.items()))}")

    # show the associator reading of one line explicitly at n=4
    print("\nAssociator reading (n=4, line {1,2,3}):")
    D=16; sig=sigma_of(build_cd_table(4),16)
    q1,q2=1,2
    nonassoc=[p for p in range(1,D) if p not in (0,q1^q2) and assoc(sig,q1,q2,p)==-1]
    assoc_p =[p for p in range(1,D) if p not in (0,q1^q2) and assoc(sig,q1,q2,p)==+1]
    print(f"  e1,e2 FAIL to associate with e_p for p in {nonassoc}  (these witness the line)")
    print(f"  e1,e2 associate with e_p for p in {assoc_p}  (no witness from these)")
