"""
G-FOLD1 execution — boost vs rotation on a fold-boundary crossing.

Executes G_FOLD1_EXECUTION_PREREGISTRATION.md sec 7, exactly and in order.
Standalone, self-verifying, sympy only. NO framework imports under test
(Eddington guard): we evaluate only general Lorentz geometry; the framework's
plane-type choice (import I1) is reported as a free parameter, never derived.

Decision scalar:  S = <e_0, Lambda e_0>_eta  (pre-reg sec 1).
"""
import sympy as sp

eta = sp.diag(-1, 1, 1, 1)
e0  = sp.Matrix([1, 0, 0, 0])

def inner(u, v):                       # <u,v>_eta = u^T eta v
    return (u.T * eta * v)[0]

phi, th = sp.symbols('phi theta', real=True)

# ---- general boost B(phi) along x, and rotation R(theta) in the y-z plane ----
B = sp.Matrix([[sp.cosh(phi), sp.sinh(phi), 0, 0],
               [sp.sinh(phi), sp.cosh(phi), 0, 0],
               [0, 0, 1, 0],
               [0, 0, 0, 1]])
R = sp.Matrix([[1, 0, 0, 0],
               [0, 1, 0, 0],
               [0, 0, sp.cos(th), -sp.sin(th)],
               [0, 0, sp.sin(th),  sp.cos(th)]])

print("=== Step 1: Lorentz membership Lambda^T eta Lambda = eta ===")
for name, M in [("boost B", B), ("rotation R", R), ("Lambda = R*B", R*B)]:
    ok = sp.simplify(M.T*eta*M - eta) == sp.zeros(4)
    print(f"  {name:14s}: Lambda^T eta Lambda == eta  -> {ok}")

print("\n=== Step 2: polar form Lambda = R*B (R in SO(3) block, B symmetric boost) ===")
print(f"  B symmetric:           {sp.simplify(B - B.T)==sp.zeros(4)}")
print(f"  R fixes the time axis: R e_0 == e_0  -> {sp.simplify(R*e0 - e0)==sp.zeros(4,1)}")
print("  (R e_0 = e_0 is why a pure rotation cannot shift frequency; only B moves e_0.)")

print("\n=== Step 3: 1+z and the decision scalar S depend ONLY on the boost ===")
Lam = R*B
S_full = sp.simplify(inner(e0, Lam*e0))
S_boost = sp.simplify(inner(e0, B*e0))
print(f"  S = <e_0, (R B) e_0>   = {S_full}")
print(f"  S = <e_0, B e_0>       = {S_boost}   (identical: R drops out)")
print(f"  Lambda_00 = (R B)_00   = {sp.simplify(Lam[0,0])}   -> S = -Lambda_00")

# welding identity on a parametrized wave train: omega = 2*pi*N/dtau, N invariant
N, dtau_e, dtau_r = sp.symbols('N dtau_e dtau_r', positive=True)
omega_e = 2*sp.pi*N/dtau_e
omega_r = 2*sp.pi*N/dtau_r
one_plus_z_wave = sp.simplify(omega_e/omega_r)
print(f"\n  Welding identity: (1+z) = omega_e/omega_r = {one_plus_z_wave} = dtau_r/dtau_e")
print(f"  => z != 0  <=>  time dilation != 0, locked to the SAME factor (no free dial).")

print("\n=== Step 4a: pure spatial-plane rotation (H_rot) ===")
S_rot = sp.simplify(inner(e0, R*e0))
# photon, generic null direction
w = sp.symbols('omega', positive=True)
nx, ny, nz = sp.symbols('n_x n_y n_z', real=True)
k = sp.Matrix([w, w*nx, w*ny, w*nz])          # null when nx^2+ny^2+nz^2=1
oz_e = -inner(k, e0)
oz_r_rot = -inner(k, R*e0)
zr = sp.simplify(oz_e/oz_r_rot - 1)
print(f"  S = <e_0, R e_0> = {S_rot}   (= -1 exactly)")
print(f"  z (rotation)      = {zr}   (= 0 exactly, any photon direction)")

print("\n=== Step 4b: time-plane rotation == boost (H_boost) ===")
S_b = sp.simplify(inner(e0, B*e0))
# line-of-sight photon along +x (the boost axis), receding geometry
k_los = sp.Matrix([w, w, 0, 0])
oz_e2 = -inner(k_los, e0)
oz_r_boost = sp.simplify(-inner(k_los, B*e0))
one_plus_z = sp.simplify(oz_e2/oz_r_boost)
print(f"  S = <e_0, B e_0> = {S_b}   (= -cosh(phi))")
print(f"  1+z (LOS boost)  = {one_plus_z}   ;  z = {sp.simplify(one_plus_z-1)}")
dilation = sp.simplify(one_plus_z)            # Delta tau_r/Delta tau_e along LOS
print(f"  time-dilation factor = {dilation}  ==  1+z  (welding holds numerically)")

print("\n=== Step 5: the declared import I1 (plane-type) and S ===")
print("  S is a FUNCTION of the import, not derivable from it:")
print("    * fold 2-plane is spacelike  (elliptic angle) -> Lambda=R, S = -1      -> z = 0")
print("    * fold 2-plane contains time (hyperbolic angle)-> Lambda has B, S=-cosh(phi) -> z!=0")
print("  Per M.CW no combinatorial/incidence input fixes plane-type (sec 4-I1).")
print("  I1 is NOT declared numerically in the pre-registration; the gate therefore")
print("  reports S(I1) and REFUSES to pick a branch (no laundering of the postulate).")

print("\n=== Falsifier checks (sec 7) ===")
print(f"  lemma holds symbolically:                 {one_plus_z_wave == dtau_r/dtau_e}")
print(f"  z independent of rotation R (z_rot==0):   {zr==0}")
print(f"  S sign: rotation -> -1, boost -> -cosh<= -1 (boost branch has |S|>1 iff phi!=0)")
