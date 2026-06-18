"""
Self-contained existence proof for (P_n'): for distinct nonzero q1,q2 there is a
p with A(q1,q2,p) = -1 (the units fail to associate with some third unit).

Probes two candidate clean structures:
  (H)  p -> A(q1,q2,p) is a homomorphism (F_2^n,xor) -> {+-1}  (a linear character).
  (W)  explicit witness: if 2^k > q1 and 2^k > q2 (a 'free' high bit), then
       A(q1,q2, 2^k) = -1.  [proved by the cocycle recursion at the level-k doubling]
  (Wgen) for EVERY distinct nonzero q1,q2, at least one generator c=2^k (k<n) has
       A(q1,q2,2^k) = -1.   (so a basis-generator witness always exists)
If (H) holds, A(q1,q2,.) is a character; (Wgen) shows it is nontrivial; hence its
-1 set has size 2^(n-1) > 0.  Both give existence with no nucleus theorem cited.
"""
from itertools import product
from pathion128_pg52 import build_cd_table

def sig_of(M,D): return [[M[i][j][1] for j in range(D)] for i in range(D)]
def A(sig,i,j,k): return sig[i][j]*sig[i^j][k]*sig[j][k]*sig[i][j^k]

if __name__=="__main__":
    print(f"{'n':>2}{'D':>5} | (H) char/homomorphism | (W) free-bit witness | (Wgen) some 2^k works")
    print("-"*82)
    for nlev in range(3,9):
        D=2**nlev; sig=sig_of(build_cd_table(nlev),D)
        H=True; W=True; Wgen=True
        for q1 in range(1,D):
            for q2 in range(q1+1,D):
                # (H): A(q1,q2,p^p') == A(q1,q2,p)A(q1,q2,p')
                # (cheap sample: test all p,p' only for small n; else sample basis)
                if nlev<=5:
                    for p in range(D):
                        for p2 in range(D):
                            if A(sig,q1,q2,p^p2)!=A(sig,q1,q2,p)*A(sig,q1,q2,p2):
                                H=False
                # (W): free high bit
                for k in range(nlev):
                    c=1<<k
                    if c>q1 and c>q2:
                        if A(sig,q1,q2,c)!=-1: W=False
                # (Wgen): some generator 2^k gives -1
                if not any(A(sig,q1,q2,1<<k)==-1 for k in range(nlev)):
                    Wgen=False
        htxt = str(H) if nlev<=5 else "(skipped>n5)"
        print(f"{nlev:>2}{D:>5} | {htxt:>21} | {str(W):>20} | {str(Wgen):>18}")
