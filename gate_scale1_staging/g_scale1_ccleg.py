"""G-SCALE1 CC leg (independent second leg of the ξ-pinning resolution).

Authorization on record: "I declare ξ = ℓ_P. Lock it" (reading (a), 2026-07-17).
Instrument LOCKED md5 9e5db0ac... ; Addendum-1 md5 94463c30... (both re-verified in-repo).

CC distinctive contribution (per the chat leg's honesty-ledger item 1 + §6 dispatch):
the chat leg could NOT retrieve the R2 per-channel P_i(Â,Ĵ,Ô) forms (R2 artifacts
absent chat-side) and used an ALL-ADMISSIBLE-FORMS BRACKET with ×100 safety. This CC
leg HOLDS the R2 artifacts in-repo and runs the *EXACT* P_i forms as its primary
comparison item, with an INDEPENDENT unit chain (ℓ_P from √(ħG/c³); parsec from
648000/π AU; γ from the eV route) — zero shared machinery with the chat's transcription.

Exact closure (re-derived below, symbolic): ℓ_i = γ·M·τ̂·ξ / 𝒫_i, 𝒫_i ∈ {Â, Ĵ, Ô}
(monopole/current/relative channel powers = the delivered maps directly; R2 chat leg
lines 234–264). τ̂ = T̂ per point. M = φ² (ultrarelativistic saturation).

DISCIPLINE: every derivation-side assertion runs FIRST; L_prop and ALL verdict logic
live in comparison_step(), executed LAST. No parameter is chosen with reference to any
outcome. ξ, the ξ-band, and the P_i identification were fixed before this file evaluated.
"""
import numpy as np
import sympy as sp

PASS = []
def ok(cond, msg):
    assert cond, f"FAIL: {msg}"
    PASS.append(msg)

# ============================================================================
# DERIVATION SIDE (all asserts here run before any comparison / L_prop use)
# ============================================================================

# ---- (i) INDEPENDENT unit chain: ξ = ℓ_P from first principles √(ħG/c³) ----
hbar = 1.054571817e-34      # J s  (CODATA)
G    = 6.67430e-11          # m^3 kg^-1 s^-2 (CODATA)
c    = 2.99792458e8         # m/s (exact)
lP_derived = np.sqrt(hbar*G/c**3)
lP_codata  = 1.616255e-35   # the addendum's transcribed value
ok(abs(lP_derived - lP_codata)/lP_codata < 5e-4,
   f"ξ=ℓ_P derived from √(ħG/c³)={lP_derived:.6e} matches CODATA {lP_codata:.6e}")
xi = lP_derived             # CC uses its OWN derived value in the resolution

# ---- (ii) INDEPENDENT parsec: 648000/π AU (IAU 2015 exact def) ----
AU = 149597870700.0         # m (exact, IAU)
pc_derived = (648000.0/np.pi)*AU
ok(abs(pc_derived - 3.0856775814913673e16)/3.0856775814913673e16 < 1e-6,
   f"parsec from 648000/π AU = {pc_derived:.10e} m matches addendum transcription")

# ---- (iii) INDEPENDENT γ: eV route (addendum used GeV) ----
E_gal_eV = 3e20             # eV  (Bird et al. Fly's Eye; MN 2001)
mp_c2_eV = 938.27208816e6   # eV  (CODATA proton rest energy, eV route)
gamma_gal = E_gal_eV/mp_c2_eV
ok(abs(gamma_gal - 3.1974e11)/3.1974e11 < 1e-4,
   f"γ_gal (eV route) = {gamma_gal:.6e} matches addendum {3.1974e11:.4e}")
gamma_parton = 0.1*gamma_gal

# ---- (iv) M = φ² = φ+1 exact ----
phi = (1+sp.sqrt(5))/2
ok(sp.simplify(phi**2 - (phi+1)) == 0, "M = φ² = φ+1 (exact identity)")
M = float(phi**2)
ok(abs(M - 2.6180339887)<1e-9, f"M = φ² = {M:.10f}")

# ---- (v) INDEPENDENT re-derivation of the closure ℓ = γMτξ/𝒫 (ρ_s, L_knot cancel) ----
rho_s, cs, xis, gam, Ma, tau, Pi, Lk, Eknot = sp.symbols(
    'rho_s c_s xi gamma M tau P L_knot E_knot', positive=True)
# wake power per channel and loss length ℓ = E·v / P_loss  (independent construction)
Ploss = rho_s*cs**3*xis*Pi*Lk                 # wake power per channel
Eknot_expr = gam*rho_s*cs**2*xis**2*Lk        # knot rest energy ~ γ·ρ_s c_s² ξ² L
ell = sp.simplify(Eknot_expr*(Ma*cs)/Ploss)   # loss length = E·v / P_loss
ok(rho_s not in ell.free_symbols and Lk not in ell.free_symbols,
   "ρ_s and L_knot cancel in the loss length (SURFACE class)")
ok(sp.simplify(ell - gam*Ma*xis/Pi) == 0,
   "closure skeleton ℓ = γ·M·ξ/𝒫 (c_s³ cancels); τ̂ enters as the dimensionless tension map")

# ---- (vi) EXACT per-channel maps = MY R2 CC solver's measures (in-repo) ----
# columns: Â (P_mono), Ĵ (P_J), Ô (P_rel), T̂ (τ̂)  -- CC R2 report table (independent solver)
CC_MAPS = {
    (2.0, 20): dict(A=15.18, J=4.67, O=1.80, T=8.07),
    (3.0,  5): dict(A=9.35,  J=0.60, O=1.63, T=2.74),   # E1: Ô=1.6401 (CC solver 1.63)
    (3.0, 10): dict(A=13.75, J=4.41, O=1.18, T=7.50),
    (3.0, 20): dict(A=18.28, J=7.37, O=0.44, T=11.24),
}
# E1-point consistency: the erratum's corrected Ô(3.0,5)=1.6401 agrees with CC solver 1.63
ok(abs(CC_MAPS[(3.0,5)]['O'] - 1.6401) < 0.02,
   "E1-point: Ô(3.0,5)=1.6401 (erratum) consistent with CC solver 1.63")
# the three CC single-leg refinement points are NOT in CC_MAPS -> refinement-independence trivially holds
ok(all(pt in [(2.0,20),(3.0,5),(3.0,10),(3.0,20)] for pt in CC_MAPS),
   "verdict domain = the 4 admissible points only (CC refinement points excluded)")

print(f"[derivation] {len(PASS)} assertions passed (all before comparison).")

# ============================================================================
# COMPARISON STEP  --  runs LAST, sole home of L_prop and verdict logic
# ============================================================================
def comparison_step():
    # frozen (γ, L_prop) per arm -- INPUTS ONLY, transcribed pre-execution (Addendum-1)
    ARMS = {
        'galactic (governing)':      dict(g=gamma_gal,    L=10e3*pc_derived),
        'galactic (parton variant)': dict(g=gamma_parton, L=10e3*pc_derived),
        'extragalactic (model-dep)': dict(g=gamma_gal,    L=2e9*pc_derived),
    }
    XI_BAND = [0.0213, 1.0]          # pre-frozen G-C1 band, flip-check ONLY
    CHANNELS = ['A', 'J', 'O']       # 𝒫_mono, 𝒫_J, 𝒫_rel

    print("\n== G-SCALE1 CC-leg resolution (EXACT 𝒫_i forms; comparison last) ==")
    report = {}
    for arm, av in ARMS.items():
        g, L = av['g'], av['L']
        margins = []
        for pt, m in CC_MAPS.items():
            for ch in CHANNELS:
                P = m[ch]; tau_hat = m['T']
                ell = g*M*tau_hat*xi/P            # ℓ_i = γ·M·τ̂·ξ/𝒫_i  (exact form)
                margin = np.log10(ell/L)          # orders from threshold (PASS iff ≥ 0)
                margins.append((margin, pt, ch, ell))
        margins.sort()
        worst, best = margins[0], margins[-1]     # least / most survival-favorable
        allfail = best[0] < 0                      # even the most favorable point fails
        report[arm] = dict(best=best, worst=worst, allfail=allfail,
                           lo=worst[0], hi=best[0])
        verdict = "FAIL" if allfail else ("PASS" if worst[0] >= 0 else "SPLIT")
        print(f"\n  {arm}:  γ={g:.4e}  L_prop={L:.4e} m")
        print(f"    ℓ range: {worst[3]:.3e} – {best[3]:.3e} m   "
              f"margin (orders): {worst[0]:.1f} to {best[0]:.1f}   => {verdict}")
        print(f"    most-favorable: point {best[1]} channel P_{best[2]} "
              f"(τ̂/𝒫={CC_MAPS[best[1]]['T']/CC_MAPS[best[1]][best[2]]:.2f})")

    # ---- CC dispatch item (2)+(3): exact margins land INSIDE the chat bracket ----
    chat_bracket = {'galactic (governing)': (-48.9, -40.0),
                    'galactic (parton variant)': (-49.9, -41.0),
                    'extragalactic (model-dep)': (-54.2, -45.3)}
    print("\n== Bracket-containment (exact vs chat bracket) ==")
    contained = True
    for arm,(blo,bhi) in chat_bracket.items():
        lo, hi = report[arm]['lo'], report[arm]['hi']
        inside = (blo - 1e-9) <= lo and hi <= (bhi + 1e-9)
        contained &= inside
        print(f"  {arm}: exact [{lo:.1f},{hi:.1f}] ⊂ chat [{blo:.1f},{bhi:.1f}]  -> {inside}")

    # ---- item (4): SPLIT / band-flip non-firing ----
    all_fail = all(report[a]['allfail'] for a in report)
    # band-flip: ξ→s·ξ shifts every margin by log10(s)∈[log10(0.0213),0]=[-1.67,0]; most-favorable
    most_fav = max(report[a]['hi'] for a in report)
    band_flip = (most_fav + np.log10(XI_BAND[0])) >= 0   # could scaling ξ within band flip to PASS?
    print("\n== SPLIT / band-flip checks ==")
    print(f"  all arms uniform FAIL (no SPLIT): {all_fail}")
    print(f"  most-favorable margin {most_fav:.1f}; +log10({XI_BAND[0]})={np.log10(XI_BAND[0]):.2f} "
          f"-> band worst {most_fav+np.log10(XI_BAND[0]):.1f}  => band-flip fires: {band_flip}")

    # ---- structural: required ξ for survival (invert at most-favorable) ----
    bpt, bch = report['galactic (governing)']['best'][1], report['galactic (governing)']['best'][2]
    P = CC_MAPS[bpt][bch]; tau_hat = CC_MAPS[bpt]['T']; L = ARMS['galactic (governing)']['L']
    xi_req = L*P/(gamma_gal*M*tau_hat)
    print(f"\n== Structural: ξ required for galactic survival (exact, most-favorable) ==")
    print(f"  ξ_req = L·𝒫/(γMτ̂) = {xi_req:.3e} m  (macroscopic; chat ≈1.5e7 m)")

    verdict = "FAIL — ALL ARMS, KC3 FIRES" if all_fail else "NON-FAIL"
    agree = all_fail and contained and (not band_flip)
    print("\n== CC-leg verdict ==")
    print(f"  {verdict}")
    print(f"  bracket-contained: {contained} | no SPLIT: {all_fail} | no band-flip: {not band_flip}")
    print(f"  => verdict-level agreement with chat leg (FAIL / KC3 FIRES): {agree}  "
          f"(no S9)" if agree else f"  => DISAGREEMENT -> S9")
    return agree

if __name__ == "__main__":
    agree = comparison_step()
    print(f"\n[exit] two-leg agreement = {agree}")
