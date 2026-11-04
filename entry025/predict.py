"""Entry 025 frozen predictions. Reads no data. Prints JSON to stdout.
Refined Koblitz conjecture (Zywina 2011): among primes p near u, the rate at which
|E(F_p)|/t is prime is C_{E,t} / (log(u+1) - log t)   [Zywina eq. (1.1), (7.1)].
"""
import json, itertools
from mpmath import mp, mpf, log, pi, quad
import sympy
mp.dps = 30
C_GENERIC = mpf("0.505166168239435774")            # Zywina Remark 2.6
SERRE_37 = 37**3 - 2*37**2 - 37 + 3                 # Zywina Prop 4.2, D = 37 ≡ 1 (mod 4)
C_37 = C_GENERIC * (1 + mpf(1)/SERRE_37)

def c_cm(B=2*10**6):
    # Zywina §7, y^2 = x^3 - x (isogenous to 32a1, same #E(F_p)); t = 8, p ≡ 1 (mod 4)
    P = mpf(1)
    for l in sympy.primerange(3, B):
        ch = 1 if l % 4 == 1 else -1; l = mpf(l)
        P *= (1 - ch*(l*l-l-1)/((l-ch)*(l-1)**2)) / (1 - ch/l)
    return 4/pi*P   # 4/pi = 1/L(1,chi_-4) = prod_{l odd}(1-chi(l)/l); remaining product converges absolutely
C_CM = c_cm()

def mean_rate(C, t, b):
    # estimand: each run has a fixed number of primes from a start uniform on [2^(b-1), 2^b),
    # so the expected pooled rate is the unweighted mean of the local rate over u
    a, z = mpf(2)**(b-1), mpf(2)**b
    return quad(lambda u: C/(log(u+1)-log(t)), [a, z]) / (z - a)

# mod-3 controls (ratio of rates, p ≡ 1 vs p ≡ 2 mod 3), derived from the mod-3 image:
#  37a1: G(3)=GL2(F3); P(3 | #E | det=1) = 9/24, det=2: 12/24  ->  (1-3/8)/(1-1/2) = 5/4
#  CM:   split p, Frobenius λ ∈ F_9^* (3 inert in Z[i]), equidistributed in each norm fibre;
#        P(λ=1 | N=1) = 1/4, N=2: 0  ->  (1-1/4)/1 = 3/4
def gl2_ratio(l=3):
    e = {1:0,2:0}; tot = {1:0,2:0}
    for a,b,c,d in itertools.product(range(l), repeat=4):
        det = (a*d-b*c) % l
        if det == 0: continue
        tot[det] += 1; e[det] += ((1-a)*(1-d)-b*c) % l == 0
    return (1-mpf(e[1])/tot[1])/(1-mpf(e[2])/tot[2])
R3_37 = gl2_ratio(); R3_CM = mpf(3)/4

ARMS = {"A37_64":("37a1",64), "B37_128":("37a1",128), "CCM_128":("cm",128), "DCM_256":("cm",256),
        "DRY37_40":("37a1",40), "DRYCM_48":("cm",48)}   # DRY*: pipeline dry runs only, not tests
out = {"C_generic":str(C_GENERIC), "C_37a1":str(C_37), "C_CM_t8":str(C_CM), "arms":{}}
for k,(curve,b) in ARMS.items():
    C,t = (C_37,1) if curve=="37a1" else (C_CM,8)
    r = mean_rate(C,t,b)
    out["arms"][k] = {"curve":curve, "bits":b, "t":t, "rate":float(r),
        "R3":float(R3_37 if curve=="37a1" else R3_CM), "lag1_corr":0.0,
        "mean_primes_scanned_to_prime_order": float((1/r) if curve=="37a1" else 2/r)}
print(json.dumps(out, indent=1))
