#!/usr/bin/env python3
# =============================================================================
# g_iib_l1_chatleg.py -- Gate G-IIB-L1 chat-leg execution (July 14, 2026)
# Locked pre-registration: G_IIB_L1_EXECUTION_PREREGISTRATION.md
#   md5 acf71fb87763295577d44f672064adfd  (author lock authorization "Lock")
# LSF-Delta filed before this script ran: G_IIB_L1_LSF_DELTA.md
#
# Standalone, self-verifying. Imports no tool under test (sympy + stdlib only).
# Exact arithmetic throughout (sympy symbolic + Fraction grids).
# Decision points D1-D4 per the locked prereg Sec.2; arms per Sec.3.
# KC numeric thresholds appear ONLY in comparison_step(), executed LAST (Sec.4).
# =============================================================================
import sympy as sp
from fractions import Fraction

ASSERTS = 0
def ok(cond, msg):
    global ASSERTS
    if not cond:
        raise AssertionError("FALSIFIER FIRED: " + msg)
    ASSERTS += 1

TOK = {}          # decision-point tokens
BANK = []         # banked R1/R2 findings (verdict-independent)

def sect(s): print("\n" + "="*78 + "\n" + s + "\n" + "="*78)

# =============================================================================
sect("D1 -- COMMON-MODE SLAVING (monopole): steady-state source support = {w0}")
# =============================================================================
t, T, p = sp.symbols('t T p', real=True)
w0, wi, gam, F0, rho_med, c, A = sp.symbols('omega0 omega_i gamma F0 rho c A', positive=True)

# --- D1.1  CM-1 re-verification, EXACT: unequal commensurable frequencies
#     average of cos(w1 t)cos(w2 t + p) over the exact common period is 0.
n_exact = 0
for (a1, b1) in [(1,1),(2,1),(3,2),(5,3),(7,2),(11,5),(1836,1),(183615,100)]:
    for pv in [0, sp.pi/7, sp.pi/3, sp.Rational(1,2)]:
        w1v = sp.Rational(a1, b1); w2v = sp.Integer(1)
        if w1v == w2v:  # equal-frequency case handled separately
            continue
        Tc = 2*sp.pi / sp.gcd(w1v, w2v)                    # common period
        avg = sp.integrate(sp.cos(w1v*t)*sp.cos(w2v*t+pv), (t, 0, Tc)) / Tc
        ok(sp.simplify(avg) == 0,
           f"CM-1 exact zero failed at w1={w1v}, p={pv}")
        n_exact += 1
print(f"[D1.1] CM-1 exact-zero verified over common period, {n_exact} rational pairs")
print("       (includes the 1836- and 1836.15-ratio proton/electron cases exactly)")

# equal-frequency case: average = cos(p)/2 exactly
Tc = 2*sp.pi
avg_eq = sp.integrate(sp.cos(t)*sp.cos(t+p), (t, 0, Tc)) / Tc
ok(sp.simplify(avg_eq - sp.cos(p)/2) == 0, "CM-1 equal-frequency cos(p)/2 failed")
print("[D1.2] equal-frequency average = cos(p)/2 exactly  (secondary-Bjerknes kernel)")

# --- D1.3  Monopole radiated power is positive-definite => radiation reaction
# far field of (1/c^2) phi_tt - lap phi = Q(t) delta^3(x):  phi = Q(t-r/c)/(4 pi r)
# with Q(t) = A cos(w t):  time-avg outward power P = rho <Qdot^2>/(4 pi c)
w = sp.symbols('w', positive=True)
Qdot2_avg = sp.integrate((sp.diff(A*sp.cos(w*t), t))**2, (t, 0, 2*sp.pi/w)) / (2*sp.pi/w)
P_rad = rho_med * Qdot2_avg / (4*sp.pi*c)
ok(sp.simplify(Qdot2_avg - A**2*w**2/2) == 0, "monopole <Qdot^2> closed form")
ok(P_rad.is_positive, "monopole radiated power positive-definite")
print("[D1.3] P_rad = rho A^2 w^2 / (8 pi c) > 0 for any oscillating monopole")
print("       => any self-frequency oscillation LOSES energy: gamma_rad > 0")

# --- D1.4  Driven damped oscillator: transients decay in BOTH damping regimes.
# HONESTY-LEDGER EVENT (self-caught at first run): the original assertion
# Re(root) = -gamma/2 is FALSE in the overdamped regime (roots real, unequal).
# Correct theorem = Hurwitz stability, proved here via Vieta + sign logic.
s = sp.symbols('s')
roots = sp.solve(s**2 + gam*s + wi**2, s)
ok(sp.simplify(roots[0] + roots[1] + gam) == 0, "Vieta: sum of roots = -gamma")
ok(sp.simplify(roots[0]*roots[1] - wi**2) == 0, "Vieta: product of roots = wi^2")
# Case complex-conjugate (underdamped): Re = sum/2 = -gamma/2 < 0. Exact.
# Case real (overdamped): sum < 0 and product > 0 => both roots negative.
#   Proof: product>0 => same sign; sum<0 => that sign is negative. QED.
# Exact-grid falsifier sweep of the sign lemma over Fractions:
n_lem = 0
fgrid = [Fraction(n, 3) for n in range(-9, 10) if n != 0]
for xr in fgrid:
    for yr in fgrid:
        if xr + yr < 0 and xr*yr > 0:
            ok(xr < 0 and yr < 0, f"sign lemma at ({xr},{yr})")
            n_lem += 1
print(f"[D1.4] Hurwitz stability: both homogeneous roots have Re < 0 for gamma>0")
print(f"       (Vieta exact; sign lemma proved + grid-falsified over {n_lem} pairs)")
print("       => ALL self-frequency content is TRANSIENT in both damping regimes.")

# --- D1.5  Steady state: unique response at w0, amplitude AND phase determined.
den = (wi**2 - w0**2) + sp.I*gam*w0
ok(sp.simplify(sp.Abs(den)**2 - ((wi**2 - w0**2)**2 + gam**2*w0**2)) == 0,
   "response denominator modulus")
ok(((wi**2 - w0**2)**2 + gam**2*w0**2).is_positive,
   "denominator nonzero for gamma>0  => amplitude and phase both DETERMINED")
Xc = F0/den                                  # complex response phasor
print("[D1.5] steady state: unique response at w0; NO free phase survives")
print("       (the CM-1 free-phi is a transient artifact).")

# --- D1.6  Energy audit at steady state (exact phasor algebra):
#   <F cos(w0 t) * xdot> = (1/2) Re(i w0 Xc) F0 ;  gamma <xdot^2> = (1/2) gamma w0^2 |Xc|^2
lhs = sp.Rational(1, 2)*sp.re(sp.I*w0*Xc)*F0
rhs = sp.Rational(1, 2)*gam*w0**2*sp.Abs(Xc)**2
ok(sp.simplify(sp.expand_complex(lhs - rhs)) == 0,
   "steady-state energy balance <F xdot> = gamma <xdot^2> (phasor-exact)")
# belt-and-braces: full trig-integral check at exact rational parameters
subs_r = [(wi, sp.Rational(3, 2)), (w0, sp.Rational(5, 7)), (gam, sp.Rational(1, 4)),
          (F0, sp.Integer(2))]
Xr = (F0/((wi**2 - w0**2) + sp.I*gam*w0)).subs(subs_r)
xr_t = sp.re(Xr*sp.exp(sp.I*sp.Rational(5, 7)*t))
lhs_i = sp.integrate(2*sp.cos(sp.Rational(5, 7)*t)*sp.diff(xr_t, t),
                     (t, 0, 2*sp.pi/sp.Rational(5, 7)))
rhs_i = sp.integrate(sp.Rational(1, 4)*sp.diff(xr_t, t)**2,
                     (t, 0, 2*sp.pi/sp.Rational(5, 7)))
ok(sp.simplify(lhs_i - rhs_i) == 0, "energy balance trig-integral spot check (exact rationals)")
print("[D1.6] <P_in from drive> = <P_rad> exactly (phasor identity + exact-rational")
print("       trig-integral spot check): emission is ELASTIC SCATTERING of the drive;")
print("       zero secular budget; no independent energy channel.")

TOK['D1'] = 'PASS'
BANK.append("T1 (R1): steady-state knot sources have time support {w0} only, with "
            "amplitude and phase determined by the response function; self-frequency "
            "content is transient (killed by its own radiation reaction); steady-state "
            "emission is elastic scattering of the drive (exact energy balance).")
print("[D1]  TOKEN = PASS")

# =============================================================================
sect("LEMMA-N -- translation invariance of the declared channel + interaction")
# =============================================================================
# Channel Lagrangian density depends on derivatives of phi only; interaction
# sum_i q_i(t) phi(X_i,t) is invariant under the simultaneous shift
# phi(x) -> phi(x-a), X_i -> X_i + a.  Verified on a generic localized field:
x, a_ = sp.symbols('x a', real=True)
G = sp.exp(-(x)**2)*sp.cos(3*x)                       # generic localized sample
I0 = sp.integrate(G, (x, -sp.oo, sp.oo))
Ia = sp.integrate(G.subs(x, x - a_), (x, -sp.oo, sp.oo))
ok(sp.simplify(I0 - Ia) == 0, "translation invariance of channel integral")
print("[L-N] channel integrals shift-invariant; interaction phi(X_i+a-a)=phi(X_i).")
print("      => total momentum conserved at the coarse-grained (continuum) order;")
print("      X_cm(t) = X0 + V t is the input to D2.  Caveat carried: continuum/")
print("      isotropy holds per Theorem 2.1' (Sec.2.88.B); lattice-scale (Umklapp)")
print("      corrections are higher-gradient, outside linear-order scope.")

# =============================================================================
sect("D2 -- DIPOLE REDUCTION: orbital dipole == 0  <=>  rho_i = lambda m_i")
# =============================================================================
m1, m2, r1s, r2s, dsep, lam, Om, D0, V, X0 = sp.symbols(
    'm1 m2 r1 r2 d lambda Omega D0 V X0', positive=True)
rho1, rho2 = sp.symbols('rho1 rho2', positive=True)

r1 = m2*dsep/(m1+m2); r2 = m1*dsep/(m1+m2)            # CM condition m1 r1 = m2 r2
ok(sp.simplify(m1*r1 - m2*r2) == 0, "CM condition")
Acoef = sp.simplify(rho1*r1 - rho2*r2)
ok(sp.simplify(Acoef - dsep*(rho1*m2 - rho2*m1)/(m1+m2)) == 0, "A closed form")

# Direction 1: universality => A == 0 identically
ok(sp.simplify(Acoef.subs([(rho1, lam*m1), (rho2, lam*m2)])) == 0,
   "universality kills the orbital dipole coefficient")
# Direction 2: A == 0 => rho1/m1 == rho2/m2  (m_i, d > 0)
sol = sp.solve(sp.Eq(Acoef, 0), rho1)
ok(len(sol) == 1 and sp.simplify(sol[0] - rho2*m1/m2) == 0,
   "A=0 forces rho1/m1 = rho2/m2")
print("[D2.1] THEOREM (both directions): orbital-dipole coefficient")
print("       A = d (rho1 m2 - rho2 m1)/(m1+m2) = 0  <=>  rho_i = lambda m_i.")

# Frequency-content audit of the full dipole P(t) = Ddot(t) * Sum rho_i X_i(t)
#   orbital piece:  Ddot(t) * A cos(Om t) = -(A D0 w0/2)[sin((w0+Om)t)+sin((w0-Om)t)]
prod = sp.expand_trig(sp.sin(w0*t)*sp.cos(Om*t))
ok(sp.simplify(prod - (sp.sin((w0+Om)*t) + sp.sin((w0-Om)*t))/2) == 0,
   "product-to-sum identity")
side_amp = D0*w0/2                           # multiplies A on each sideband
ok(side_amp.is_positive, "sideband prefactor D0 w0/2 > 0: sidebands vanish IFF A = 0")
#   CM piece: Ddot(t)*(rho1+rho2)*(X0+Vt) -- contains w0 and t*trig(w0 t) terms only;
#   verified: no Omega appears in it at all.
cm_piece = sp.diff(D0*sp.cos(w0*t), t)*(rho1 + rho2)*(X0 + V*t)
ok(Om not in cm_piece.free_symbols, "CM dipole term carries NO Omega content")
print("[D2.2] P(t) frequency content: orbital sidebands (w0 +/- Om) carry amplitude")
print("       (D0 w0/2) * A  -- zero IFF universality holds (A = 0);")
print("       the CM term (rho1+rho2)(X0+Vt) carries NO Omega content: its O(V)")
print("       piece is the uniform-motion Doppler channel, handled in D4b(ii).")

TOK['D2'] = 'STRUCTURAL-PASS (universality = named condition, Sec.2.88.A)'
BANK.append("T2 (R1): the orbital (binary-dynamics) dipole vanishes iff the response/"
            "mass ratio is universal, rho_i = lambda m_i; then the dipole is slaved to "
            "total momentum (conserved). Non-universal response => dipole sidebands "
            "at w0 +/- Omega => the KC1(b) channel. The universality itself is the "
            "Sec.2.88.A equivalence (tower anchoring) -- the named condition.")
print("[D2]  TOKEN = STRUCTURAL-PASS (conditional hinge named)")

# =============================================================================
sect("D3 -- QUADRUPOLE ONSET: orbital content survives at quadrupole, generically")
# =============================================================================
# CM frame (CM motion adds no Omega content per D2 audit).
X1 = r1*sp.Matrix([sp.cos(Om*t), sp.sin(Om*t)]); X2 = -r2*sp.Matrix([sp.cos(Om*t), sp.sin(Om*t)])
Bcoef = sp.simplify(rho1*r1**2 + rho2*r2**2)
Qxx_m_Qyy = sp.simplify(sp.expand_trig(
    rho1*(X1[0]**2 - X1[1]**2) + rho2*(X2[0]**2 - X2[1]**2)))
ok(sp.simplify(Qxx_m_Qyy - Bcoef*sp.cos(2*Om*t)) == 0, "Qxx-Qyy = B cos(2 Om t)")
Qxy = sp.simplify(sp.expand_trig(rho1*X1[0]*X1[1] + rho2*X2[0]*X2[1]))
ok(sp.simplify(Qxy - Bcoef*sp.sin(2*Om*t)/2) == 0, "Qxy = (B/2) sin(2 Om t)")
ok(Bcoef.is_positive, "quadrupole coefficient B > 0 (positives)")
Buniv = sp.simplify(Bcoef.subs([(rho1, lam*m1), (rho2, lam*m2)]))
mu = m1*m2/(m1+m2)
ok(sp.simplify(Buniv - lam*mu*dsep**2) == 0, "B|_universality = lambda mu d^2")
ok(Buniv.is_positive, "B does NOT cancel under universality")
print("[D3.1] quadrupole moments carry 2*Omega content with coefficient")
print("       B = rho1 r1^2 + rho2 r2^2 > 0;  under universality B = lambda mu d^2 > 0.")
print("       => with monopole conserved (D1 + Sum rho_i fixed) and dipole slaved")
print("       (D2 | universality), the LEADING independent emission from orbital")
print("       dynamics enters at QUADRUPOLE (sidebands w0 +/- 2 Omega).")
print("       Acoustic twin (LSF-Delta C2): co-rotating vortex pair = rotating")
print("       quadrupole sound (Mitchell-Lele-Moin 1995).")

TOK['D3'] = 'PASS'
BANK.append("T3 (R1): quadrupole 2*Omega content is generic and does not cancel under "
            "universality (B = lambda mu d^2); emission from orbital dynamics starts "
            "at quadrupole given D1 and D2's condition -- the GR-template multipole "
            "structure, supplying Carlip's quadrupole-only premise for KC2.")
print("[D3]  TOKEN = PASS")

# =============================================================================
sect("D4a -- SUBSONIC UNIFORM MOTION: exactly silent (all orders in v below c_s)")
# =============================================================================
kx, ky, kz, vx, vy, vz = sp.symbols('kx ky kz vx vy vz', real=True)
k2 = kx**2 + ky**2 + kz**2; v2 = vx**2 + vy**2 + vz**2
kv = kx*vx + ky*vy + kz*vz
cross2 = (ky*vz - kz*vy)**2 + (kz*vx - kx*vz)**2 + (kx*vy - ky*vx)**2
ok(sp.simplify(k2*v2 - kv**2 - cross2) == 0, "Lagrange identity |k|^2|v|^2-(k.v)^2=|kxv|^2")
print("[D4a.1] (k.v)^2 <= |k|^2 |v|^2   (Lagrange identity, exact)")
print("        => c^2|k|^2 - (k.v)^2 >= (c^2 - |v|^2)|k|^2 > 0 for |v| < c, k != 0:")
print("        the radiation shell {w = c|k|} never meets the source support {w = k.v}.")
print("        The co-moving operator c^2 lap - (v.grad)^2 is ELLIPTIC: a steady,")
print("        non-radiating co-moving solution exists. Radiated power = 0 EXACTLY.")

# exact Fraction-grid falsifier sweep (subsonic, c = 1)
grid = [Fraction(n, 4) for n in range(-3, 4)]          # -3/4 .. 3/4
kgrid = [Fraction(n, 3) for n in (-2, -1, 1, 2)]
n_pos = 0
for gx in grid:
    for gy in grid:
        if gx == 0 and gy == 0:
            continue
        if gx*gx + gy*gy >= 1:                          # keep strictly subsonic
            continue
        for kx_ in kgrid:
            for ky_ in kgrid:
                lhs = 1*(kx_*kx_ + ky_*ky_) - (kx_*gx + ky_*gy)**2
                ok(lhs > 0, f"subsonic positivity at v=({gx},{gy}), k=({kx_},{ky_})")
                n_pos += 1
print(f"[D4a.2] exact Fraction-grid sweep: {n_pos} subsonic (v,k) combinations, all")
print("        strictly positive -- no on-shell intersection, zero exceptions.")

# supersonic witness: the Mach cone exists
Vs, k0 = sp.symbols('Vs k0', positive=True)
kM = sp.Matrix([k0*c/Vs, k0*sp.sqrt(1 - (c/Vs)**2), 0])   # cos(theta) = c/Vs, Vs > c
kv_M = (kM.T*sp.Matrix([Vs, 0, 0]))[0]
ok(sp.simplify(kv_M - c*sp.sqrt((kM.T*kM)[0])) == 0, "Mach-cone on-shell witness (Vs>c)")
print("[D4a.3] supersonic witness: cos(theta_M) = c/V puts source support ON the")
print("        radiation shell -- the wake channel opens exactly at v > c_s.")

TOK['D4a'] = 'PASS'
BANK.append("T4 (R1): a source of ANY static profile in uniform subsonic motion "
            "radiates exactly nothing (empty on-shell intersection; elliptic co-moving "
            "problem); the wake channel opens at v = c_s exactly (Mach witness).")
print("[D4a] TOKEN = PASS (exact, stronger than linear order)")

# =============================================================================
sect("D4b -- SUPERSONIC / COUPLING-CLASS DICHOTOMY + Doppler record")
# =============================================================================
aG, kk = sp.symbols('aG kk', positive=True)

# (i) [static-core-direct]: generic profile is nonzero on the Mach cone
sig_hat = sp.exp(-aG**2*kk**2/2)
ok(sig_hat.is_positive, "Gaussian profile transform > 0 everywhere incl. Mach cone")
print("[D4b.i]  [static-core-direct] class: profile transform nonzero on the open")
print("         Mach cone => NONZERO wake emission for v > c_s (order-one channel,")
print("         no small parameter).  Anchors (LSF-Delta C1,C3): Landau/impurity drag")
print("         above c_s (Astrakharchik-Pitaevskii class); Gravejat CMP 243 (2003):")
print("         NO finite-energy supersonic GP traveling waves; Jones-Roberts 1982:")
print("         the traveling family lives strictly below c_s.")
print("         => CLASS-CONDITIONAL SOURCING: any knot whose core deficit couples")
print("         directly to the longitudinal channel is KC3-dead above c_s = phi^-2 c.")

# (ii) [drive-mediated] with spatially uniform global drive: q(t) = rho * Ddot(t)
q_dm = sp.diff(rho1*D0*sp.cos(w0*t), t)
ok(sp.simplify(sp.diff(q_dm, D0)*D0 - q_dm) == 0, "q linear (degree 1) in D0")
ok(sp.simplify(q_dm.subs(D0, 0)) == 0, "drive off => coupling identically zero")
print("[D4b.ii] [drive-mediated] class (uniform global drive over knot scales --")
print("         the CM-2 'global' reading, hypothesis stated per prereg Sec.1.2):")
print("         q(t) = rho Ddot(t) is X-INDEPENDENT and LINEAR in D0.")
print("         D0 -> 0 kills every knot-channel coupling: NO INDEPENDENT SOURCING")
print("         (the gate-title sense).  Motion adds no coupling of its own.")

# Doppler-asymmetry record (intra-mechanism, flagged; coefficient not load-bearing)
M_, nexp, th = sp.symbols('M n theta', positive=True)
K = (1 - M_*sp.cos(th))**(-nexp)
K1 = sp.series(K, M_, 0, 2).removeO()
ok(sp.simplify(K1 - (1 + nexp*M_*sp.cos(th))) == 0, "O(M) Doppler kernel expansion")
fwd_bwd = sp.simplify(K1 - K1.subs(th, sp.pi - th))
ok(sp.simplify(fwd_bwd - 2*nexp*M_*sp.cos(th)) == 0, "forward-backward asymmetry 2nM cos")
net = sp.integrate(K1*sp.cos(th)*2*sp.pi*sp.sin(th), (th, 0, sp.pi))
ok(sp.simplify(net - 4*sp.pi*nexp*M_/3) == 0, "net momentum integral (4 pi/3) n M")
print("[D4b.ii-rec] RECORDED (per the locked 'executed and recorded' clause):")
print("         a moving drive-locked scatterer re-radiates Doppler-asymmetrically;")
print("         for any positive Doppler exponent n the net radiated momentum rate")
print("         is (n/3)(P_scat/c) * (v/c) * 4pi-normalized -- an O(v) intra-")
print("         mechanism friction toward the SUBSTRATE REST FRAME.  It is NOT")
print("         independent sourcing (vanishes with D0); magnitude ~ D0^2 rho^2 is")
print("         M.CW-walled (imports w0, D0, rho -- CM-3 territory).  Prior-art twin")
print("         (LSF-Delta C1): sub-critical Doppler drag from scattered fluctuations.")
print("         FORWARD-POINTER: a CM-3-level magnitude gate is required before any")
print("         KC3/Lorentz-sector numeric claim about this channel.")

# (iii) classification of the PHYSICAL knot against the declared corpus (text audit)
print("[D4b.iii] Corpus classification (declared items only):")
print("   - Sec.2.91 / BD-IIB-1: declares K, kappa, c_s, branch lock -- silent on the")
print("     knot-core <-> longitudinal-channel coupling class.")
print("   - Sec.2.88.C (CM-2): declares the RESPONSE coupling (drive-mediated) -- and")
print("     flags 'which object pulsates' as M.ONT-gated.")
print("   - Sec.3.4 fluid action: any SINGLE-COMPONENT knot in the longitudinal psi")
print("     carries a GP-FORCED core deficit => [static-core-direct] => (i) applies.")
print("   - M.ONT (filament / texture / two-component): OPEN ledger row.")
print("   => The physical knot's coupling class is NOT FIXED by the declared corpus.")
TOK['D4b'] = 'UNDERDETERMINED (missing declaration: M.ONT knot-core <-> longitudinal-channel coupling class)'
BANK.append("T5 (R1 dichotomy + R2 classification): [static-core-direct] => order-one "
            "Cherenkov/wake sourcing above c_s (Gravejat/Landau-anchored); [drive-"
            "mediated, uniform drive] => zero independent sourcing exactly (all "
            "coupling proportional to D0), with an O(v) intra-mechanism Doppler friction "
            "recorded (M.CW-walled). Which class the physical knot occupies is "
            "UNDECLARED -- M.ONT-gated. BANKED CONSTRAINT: the single-component-"
            "filament-in-longitudinal-psi M.ONT branch is structurally KC3-dead for "
            "v > c_s unless a separate kinematic closure is derived.")
print("[D4b] TOKEN = UNDERDETERMINED")

# =============================================================================
sect("COMPARISON STEP -- run LAST; the ONLY place KC thresholds appear (Sec.4)")
# =============================================================================
def comparison_step(tok):
    print("KC thresholds (quarantined to this step; cited, never used upstream):")
    print("  KC1(a) quadrupole deviation < 1.3e-4        [Kramer et al. 2021, PRX 11 041050]")
    print("  KC1(b) dipole alpha0^2 < 2e-5               [Freire et al. 2012, PSR J1738+0333]")
    print("  KC2    aberration: c_g > 2e10 c equivalent  [Carlip 2000, PLA 267 81]")
    print("  KC3    c - c_g < 2e-15 c (gal.) / 2e-19 c   [Moore-Nelson 2001]")
    print("-"*78)
    print("Tokens:", {k: v.split(' ')[0] for k, v in tok.items()})
    sourcing = [k for k, v in tok.items() if v.startswith('SOURCING')]
    underdet = [k for k, v in tok.items() if v.startswith('UNDERDETERMINED')]
    if sourcing:
        arm = "ARM C -- FAIL (SOURCING); Sec.2.91.D blast radius executes"
    elif underdet:
        arm = "ARM D -- DEGENERATE (UNDERDETERMINED)"
    elif tok['D2'].startswith('STRUCTURAL-PASS'):
        arm = "ARM B -- PASS (CONDITIONAL)"
    else:
        arm = "ARM A -- PASS (FULL)"
    print("PRECEDENCE APPLIED (locked Sec.3): ", arm)
    print("-"*78)
    print("KC dispositions under ARM D: NO KC IS CLAIMED PASSED.")
    print("Contingent ladder (recorded, not claimed):")
    print("  IF M.ONT declares drive-mediated-only  => D1+D3+D4 carry KC1(a), KC2's")
    print("     premises, and KC3 at the independent-sourcing level; KC1(b) remains")
    print("     conditional on Sec.2.88.A universality => Arm-B-equivalent verdict")
    print("     (contingent), with the Doppler-friction magnitude gate outstanding.")
    print("  IF M.ONT admits ANY static-core-direct longitudinal coupling => KC3")
    print("     fires structurally above c_s => Arm-C path, Sec.2.91.D blast radius.")
    return arm

ARM = comparison_step(TOK)

# =============================================================================
sect("VERDICT + BANKED FINDINGS")
# =============================================================================
print("GATE G-IIB-L1 CHAT-LEG VERDICT:", ARM)
print("Missing declaration (named, per Arm D): the M.ONT knot-core <-> longitudinal-")
print("channel coupling class. The gate stops here per the locked stopping rule.")
print()
for i, b in enumerate(BANK, 1):
    print(f"BANK {i}. {b}\n")
print(f"TOTAL ASSERTIONS PASSED: {ASSERTS}")
print("Prereg: acf71fb87763295577d44f672064adfd | LSF-Delta filed pre-derivation.")
print("No KC claimed. No observable. No magnitudes. Sec.2.52 Open 3 untouched.")
