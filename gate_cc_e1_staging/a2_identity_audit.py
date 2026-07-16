"""G-CC-e1 Amendment-2 PRE-AUTHORIZATION AUDIT (independent math check only).

NOT a CC leg. The CC leg is barred until {lock + A1 + A2 + VC declaration} are all in place
(A2 is DRAFT, VC undeclared). This script only verifies the two load-bearing EXACT claims of
the CORRECTED wake decomposition (A2.1), the ones whose predecessor (A1 D1b(iv)) was
machine-falsified -- so that the author can authorize A2 knowing the replacement is sound.

Claim 1 (A2.1, two-fluid momentum-flux identity):
   Sum_c rho_c u_c (x) u_c  =  J(x)J / rho_tot  +  (rho1 rho2 / rho_tot) Du (x) Du
   with J = rho1 u1 + rho2 u2, rho_tot = rho1+rho2, Du = u1-u2.
Claim 2 (A2.1 / T4): the interface overlap integral of rho1 rho2 / rho_tot for a tanh step
   equals w/2 exactly.
"""
import sympy as sp

def ok(c, m):
    if not c: raise AssertionError("FALSIFIER: " + m)
    print("  [OK]", m)

print("="*74)
print("CLAIM 1 -- two-fluid momentum-flux identity (exact, 3-vector tensor form)")
print("="*74)
r1, r2 = sp.symbols('rho1 rho2', positive=True)
u1 = sp.Matrix(sp.symbols('u1x u1y u1z', real=True))
u2 = sp.Matrix(sp.symbols('u2x u2y u2z', real=True))
rtot = r1 + r2
J = r1*u1 + r2*u2                          # total current
Du = u1 - u2
LHS = r1*(u1*u1.T) + r2*(u2*u2.T)          # Sum_c rho_c u_c (x) u_c
RHS = (J*J.T)/rtot + (r1*r2/rtot)*(Du*Du.T)
diff = sp.simplify(sp.Matrix(LHS - RHS))
ok(diff == sp.zeros(3, 3), "Sum rho_c u_c(x)u_c == J(x)J/rho_tot + (rho1 rho2/rho_tot) Du(x)Du")
# show the cross-term cancellation explicitly (the term A1 omitted lives in the Du(x)Du piece)
cross = sp.simplify((J*J.T)/rtot - (r1*(u1*u1.T) + r2*(u2*u2.T)) + (r1*r2/rtot)*(Du*Du.T))
ok(cross == sp.zeros(3,3), "cross terms cancel exactly (the relative-flow term is (rho1 rho2/rho_tot)Du(x)Du)")
# the RELATIVE-FLOW (spin-sector) term is winding-EVEN and unsuppressible: it depends on |Du|^2,
# not on the sign/winding of either u_c -> replacing u_c -> -u_c (counter-winding) leaves Du(x)Du's
# trace invariant in |Du|^2. Verify the trace (the scalar stress) is a function of |Du|^2:
tr_rel = sp.simplify(sp.trace((r1*r2/rtot)*(Du*Du.T)))
ok(sp.simplify(tr_rel - (r1*r2/rtot)*(Du.T*Du)[0]) == 0,
   "relative-flow stress trace = (rho1 rho2/rho_tot)|Du|^2 (winding-even, >=0)")
print("  => the corrected decomposition P_wake = eps^2 P_mono + eps_J^2 P_J + P_rel + P_cross")
print("     is exact; P_rel (the term A1 omitted) is the (rho1 rho2/rho_tot)|Du|^2 relative-flow")
print("     quadrupole -- winding-even, non-negative, unsuppressible by counter-winding. CONFIRMED.")

print()
print("="*74)
print("CLAIM 2 -- tanh-step interface overlap integral = w/2 (exact)")
print("="*74)
x, w = sp.symbols('x w', positive=True)
# immiscible complementary profiles: rho1 = rinf*f, rho2 = rinf*(1-f), rho_tot = rinf (const),
# f a tanh step of width w: f(x) = (1 - tanh(x/w))/2, going 1 -> 0 across the interface.
rinf = sp.symbols('rho_inf', positive=True)
f = (1 - sp.tanh(x/w))/2
rho1 = rinf*f; rho2 = rinf*(1 - f); rho_tot = sp.simplify(rho1 + rho2)
ok(sp.simplify(rho_tot - rinf) == 0, "complementary immiscible profiles: rho_tot = rho_inf (const)")
overlap_density = sp.simplify(rho1*rho2/rho_tot)                 # = rinf f(1-f)
ok(sp.simplify(overlap_density - rinf*f*(1-f)) == 0, "overlap density = rho_inf f(1-f)")
ok(sp.simplify(f*(1-f) - sp.Rational(1,4)*sp.sech(x/w)**2) == 0, "f(1-f) = (1/4) sech^2(x/w)")
# integral over the full line, normalized by rho_inf:
integ = sp.integrate(f*(1-f), (x, -sp.oo, sp.oo))
ok(sp.simplify(integ - w/2) == 0, "integral f(1-f) dx = w/2 EXACTLY (overlap = w/2)")
print("  => the P_rel support (rho1 rho2/rho_tot) is interface-localized with overlap integral")
print("     = w/2 exactly for the tanh step (T4 scaling). CONFIRMED.")

print()
print("="*74)
print("AUDIT SUMMARY -- both load-bearing exact claims of A2.1 VERIFIED")
print("="*74)
print("Claim 1 (two-fluid identity, incl. the previously-omitted relative-flow term): EXACT.")
print("Claim 2 (tanh-step overlap = w/2): EXACT.")
print("This is a PRE-AUTHORIZATION math audit only. NO CC leg dispatched (barred until")
print("{lock + A1 + A2-frozen + VC declaration}). No VC branch chosen (author-owned). No fold.")
