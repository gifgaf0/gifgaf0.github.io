# Frozen-candidate prediction code: constants and local rates. Reads no data.
from mpmath import mp, mpf, log, pi, quad, inf
import itertools, sympy
mp.dps = 30
def primes(n): return list(sympy.primerange(2, n))
# --- brute-force local densities over GL2(F_l) (checks the closed forms) ---
def gl2_counts(l):
    eig1 = {d:0 for d in range(1,l)}; tot = {d:0 for d in range(1,l)}
    for a,b,c,d in itertools.product(range(l), repeat=4):
        det=(a*d-b*c)%l
        if det==0: continue
        tot[det]+=1
        if ((1-a)*(1-d)-b*c)%l==0: eig1[det]+=1
    return eig1, tot
for l in (2,3,5,7):
    e,t=gl2_counts(l)
    frac=sum(e.values())/sum(t.values())
    closed=(l**3-2*l)/((l*l-1)*(l*l-l))
    print(f"l={l}: P(l|#E) brute {frac:.6f} closed {closed:.6f}; by det:", {d:f"{e[d]}/{t[d]}" for d in t})
# --- generic non-CM constant C (Zywina Remark 2.6: 0.505166168239435774) ---
def C_generic(B=10**7):
    P=mpf(1)
    for l in sympy.primerange(2,B):
        l=mpf(l); P*=1-(l*l-l-1)/((l-1)**3*(l+1))
    # tail ~ prod(1-1/l^2) over l>=B: negligible-ish; estimate via sum 1/l^2 ~ 1/(B log B)
    return P*(1-mpf(1)/(B*log(B)))
C=C_generic()
C37 = C*(1+mpf(1)/(37**3-2*37**2-37+3))   # Zywina Prop 4.2, D=37 ≡ 1 mod 4
print("C generic", C, " C_37a1", C37, " Serre correction 1/", 37**3-2*37**2-37+3)
# --- CM constant (Zywina §7): prod_{l odd} (1 - chi(l)(l^2-l-1)/((l-chi)(l-1)^2)),
#     written as (4/pi) * prod [f_l/(1-chi/l)], the latter absolutely convergent
def C_cm(B=10**7):
    P=mpf(1)
    for l in sympy.primerange(3,B):
        ch=1 if l%4==1 else -1; l=mpf(l)
        f=1-ch*(l*l-l-1)/((l-ch)*(l-1)**2)
        P*=f/(1-ch/l)
    return 4/pi*P
Ccm=C_cm(); print("C_CM t=8", Ccm, "(Zywina: 1.067350894)")
# --- integrals (Zywina eq. 1.1 / 7.1) for calibration at 1e9 ---
I1 = quad(lambda u: 1/(log(u+1)*log(u)), [2, 1e3, 1e6, 1e9])
I8 = quad(lambda u: 1/((log(u+1)-log(8))*log(u)), [9, 1e3, 1e6, 1e9])
print("pred 37a1 1e9 (from 2):", C37*I1, " pred CM 1e9:", Ccm/2*I8, " pred zyw serre 1e9 (10/9 C):", mpf(10)/9*C*I1)
# --- local rates at random-start heights y = 2^(b-0.5) ---
for b in (64,128,256):
    y=mpf(2)**(b-mpf(0.5))
    print(f"b={b}: r_37 = {float(C37/log(y+1)):.6e}  r_CM(p=1 mod 4, t=8) = {float(Ccm/(log(y+1)-log(8))):.6e}")
