"""BD-IIB-1 CC-leg replication (zero shared machinery).

Verifies the algebra of the Paper II-B acoustic-metric R3 bridge declaration
(BRIDGE_DECLARATION_IIB_ACOUSTIC_METRIC_R3.md, S10 scope items 1-5), independently:
exact golden-ratio arithmetic in Q(sqrt5) + a dimensional check + decimals.

Scope (per the memo): ALGEBRA ONLY. No data consulted, no observable evaluated. R3 off-ledger.
This leg checks forms/values; it makes NO physical claim, does NOT fold, and takes NO position
on the kill conditions (KC1/KC2), the branch lock, or the M.ONT A-SHEAR flag.
"""
from fractions import Fraction as Fr
import math

# ---- exact arithmetic in Q(sqrt5): number = a + b*sqrt5, a,b rational ----
class G:
    __slots__=('a','b')
    def __init__(s,a,b=0): s.a=Fr(a); s.b=Fr(b)
    def __add__(s,o): o=s._c(o); return G(s.a+o.a, s.b+o.b)
    def __sub__(s,o): o=s._c(o); return G(s.a-o.a, s.b-o.b)
    def __mul__(s,o): o=s._c(o); return G(s.a*o.a+5*s.b*o.b, s.a*o.b+s.b*o.a)
    __rmul__=__mul__; __radd__=__add__
    def __neg__(s): return G(-s.a,-s.b)
    def inv(s):
        d=s.a*s.a-5*s.b*s.b            # norm; (a+b√5)(a-b√5)=a^2-5b^2
        return G(s.a/d, -s.b/d)
    def __truediv__(s,o): o=s._c(o); return s*o.inv()
    def __eq__(s,o): o=s._c(o); return s.a==o.a and s.b==o.b
    @staticmethod
    def _c(o): return o if isinstance(o,G) else G(o)
    def val(s): return float(s.a)+float(s.b)*math.sqrt(5)
    def __repr__(s):
        if s.b==0: return f"{s.a}"
        return f"{s.a} + {s.b}*sqrt5"

phi = G(Fr(1,2), Fr(1,2))             # (1+sqrt5)/2
print("="*66); print("BD-IIB-1 CC-leg replication (exact Q(sqrt5))"); print("="*66)
print(f"phi = (1+sqrt5)/2 = {phi.val():.12f}")

# defining relation
assert phi*phi == phi + 1
print(f"[def] phi^2 = phi + 1: OK")

# ITEM 2: exact forms phi^-2 = 2 - phi ; phi^-4 = 5 - 3 phi
inv2 = (phi*phi).inv()
assert inv2 == G(2) - phi, inv2
print(f"[2] phi^-2 = 2 - phi (exact): OK   (= {inv2.val():.12f})")
inv4 = (phi*phi*phi*phi).inv()
assert inv4 == G(5) - G(3)*phi, inv4
print(f"[2] phi^-4 = 5 - 3*phi (exact): OK  (= {inv4.val():.12f})")

kappa = inv4                          # kappa = phi^-4 = 5 - 3 phi
print(f"    kappa = phi^-4 = {kappa.val():.12f}  (memo: 0.145898033750)")
assert abs(kappa.val()-0.145898033750) < 1e-11

# ITEM 3: fluid-branch c_s/c = sqrt(kappa) = phi^-2 = 2 - phi
# exact: (c_s/c)^2 = kappa and c_s/c = phi^-2 -> check (phi^-2)^2 == kappa
assert inv2*inv2 == kappa
cs_over_c = inv2.val()
print(f"[3] c_s/c = sqrt(kappa) = phi^-2 = 2-phi = {cs_over_c:.12f}  (memo: 0.381966011250)")
assert abs(cs_over_c-0.381966011250) < 1e-11

# ITEM 4: solid branch c_L/c = sqrt(kappa + 4/3); nu = (3k-2)/(2(3k+1)); stability -1<nu<1/2
kap_plus = kappa + G(Fr(4,3))         # exact kappa + 4/3
cL_over_c = math.sqrt(kap_plus.val())
print(f"[4] c_L/c = sqrt(kappa + 4/3) = {cL_over_c:.12f}  (memo: 1.216236558850)")
assert abs(cL_over_c-1.216236558850) < 1e-11
nu = (G(3)*kappa - G(2)) / (G(2)*(G(3)*kappa + G(1)))   # exact rational-in-Q(sqrt5)
print(f"[4] nu = (3k-2)/(2(3k+1)) = {nu.val():.12f}  (memo: -0.543337382198)")
assert abs(nu.val()-(-0.543337382198)) < 1e-11
stable = (-1 < nu.val() < 0.5)
print(f"    isotropic stability -1 < nu < 1/2: {stable}; auxetic (nu<0): {nu.val()<0}")
assert stable and nu.val()<0

# ITEM 5: Lucas cross-check phi^4 + phi^-4 = 7 (exact) = L_4
phi4 = phi*phi*phi*phi
assert phi4 + inv4 == G(7)
print(f"[5] phi^4 + phi^-4 = {(phi4+inv4)} = 7 exact (Lucas L_4).  "
      f"[memo S2.3: EXCLUDED from any mechanical role -- noted, not used]")

# ITEM 1: dimensional identity K = Z0^2 / rho_s = Pa  (units as [kg,m,s] exponent vectors)
def U(kg=0,m=0,s=0): return (Fr(kg),Fr(m),Fr(s))
def usub(a,b): return tuple(a[i]-b[i] for i in range(3))
def uadd(a,b): return tuple(a[i]+b[i] for i in range(3))
Z0  = U(kg=1, m=-2, s=-1)             # specific acoustic impedance Pa*s/m = kg m^-2 s^-1
rho = U(kg=1, m=-3, s=0)              # substrate density kg m^-3
K   = usub(uadd(Z0,Z0), rho)          # Z0^2 / rho_s
Pa  = U(kg=1, m=-1, s=-2)             # pascal
print(f"[1] [Z0^2/rho_s] = {tuple(str(x) for x in K)} (kg,m,s exponents); [Pa] = "
      f"{tuple(str(x) for x in Pa)}: {K==Pa}")
assert K==Pa
# A-Z0: Z0 = rho_s * c_s -> [rho_s][c] = kg m^-3 * m s^-1 = kg m^-2 s^-1 = [Z0]
rho_cs = uadd(rho, U(m=1,s=-1))
print(f"    A-Z0 dim: [rho_s * c_s] = {tuple(str(x) for x in rho_cs)} == [Z0]: {rho_cs==Z0}")
assert rho_cs==Z0
# and kappa = K/(rho_s c^2) dimensionless
kap_dim = usub(K, uadd(rho, U(m=2,s=-2)))
print(f"    kappa = K/(rho_s c^2) dimensionless: {kap_dim==U()}")
assert kap_dim==U()

print("="*66)
print("ALL 5 CC-leg replication items VERIFIED (exact algebra + dimensions).")
print("Scope held: algebra only; no data; no fold; no position on KC1/KC2, the branch lock,")
print("or the A-SHEAR M.ONT flag. R3 off-ledger; fold only post-V4.63 at explicit authorization.")
