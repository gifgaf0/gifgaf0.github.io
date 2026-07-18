"""ANNEX-SC-1 pre-authorization audit: FROZEN INPUTS ONLY.
Verifies the discretion-free transcriptions in Addendum 1 and the memo constants.
NO comparison is formed: l_i = g*M*tau*xi/P and the inequality l_i >= L_prop are
NOT computed here -- that is the quarantined, authorization-gated resolution step.
"""
from math import sqrt, isclose, log10

# --- CODATA / source constants as transcribed ---
mp_c2 = 0.93827208816            # GeV, CODATA proton rest energy
E_gal = 3e11                    # GeV (Bird et al. Fly's Eye event; MN 2001 stated value)
pc    = 3.0856775814913673e16    # m (1 parsec, exact-ish CODATA/IAU)
lP    = 1.616255e-35             # m (Planck length, CODATA)

print("== Addendum 1 input transcriptions ==")
# galactic gamma (whole-knot, survival-favorable)
g_gal = E_gal/mp_c2
print(f"gamma_gal  = E/(mp c^2) = {g_gal:.6e}   memo: 3.1974e11   ok={isclose(g_gal,3.1974e11,rel_tol=1e-4)}")
g_parton = 0.1*E_gal/mp_c2
print(f"gamma_part = 0.1E/(mpc^2)= {g_parton:.6e}   memo: 3.1974e10   ok={isclose(g_parton,3.1974e10,rel_tol=1e-4)}")

# traversal lengths
L_gal  = 10e3*pc                # 10 kpc
L_xgal = 2e9*pc                 # 2 Gpc
print(f"L_gal  = 10 kpc = {L_gal:.16e} m   memo: 3.0856775814913673e20   ok={isclose(L_gal,3.0856775814913673e20,rel_tol=0,abs_tol=1e6)}")
print(f"L_xgal = 2 Gpc  = {L_xgal:.16e} m   memo: 6.1713551629827346e25   ok={isclose(L_xgal,6.1713551629827346e25,rel_tol=0,abs_tol=1e12)}")

# "strictly harder by 5.3 orders" claim
orders = log10(L_xgal/L_gal)
print(f"log10(L_xgal/L_gal) = {orders:.4f}   memo: 5.3 orders   ok={isclose(orders,5.3,abs_tol=0.05)}")

# --- memo constants (frozen inputs, NOT the comparison) ---
print("\n== Memo constants ==")
phi = (1+sqrt(5))/2
print(f"phi = {phi:.12f}")
print(f"phi^2 - (phi+1) = {phi**2-(phi+1):.2e}   (M = phi^2 = phi+1 exact identity)   ok={isclose(phi**2,phi+1,rel_tol=0,abs_tol=1e-12)}")
print(f"phi^2 (= M) = {phi**2:.6f}   memo: 2.618   ok={isclose(phi**2,2.618,abs_tol=5e-4)}")
print(f"c_s = phi^-2 c  ->  phi^-2 = {phi**-2:.6f}")

# robustness band endpoints (G-C1, banked V4.48) -- pre-frozen, flip-check only
print("\n== Robustness band (pre-frozen, flip-check ONLY; NOT evaluated here) ==")
print(f"xi/a band [0.0213, 0.0851] (sub-cell); xi in [0.0213, 1]*lP; lP = {lP:e} m")
print("\nNOTE: no comparison, no l_i, no PASS/FAIL formed. Resolution is §6-gated.")
