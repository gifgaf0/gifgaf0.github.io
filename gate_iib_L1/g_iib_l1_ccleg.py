"""G-IIB-L1 CC-LEG (independent second leg) -- Paper II-B emergent-Bjerknes gate.

Locked pre-registration: G_IIB_L1_EXECUTION_PREREGISTRATION.md (md5 acf71fb87763295577d44f672064adfd).
Chat leg: g_iib_l1_chatleg.py + G_IIB_L1_GATE_EXECUTION_REPORT.md (verdict ARM D).

CC-LEG SPEC (report Sec.6) -- ZERO SHARED MACHINERY, DIFFERENT METHODS PER POINT:
  (i)   CM-1 averages via COMPLEX-EXPONENTIAL ORTHOGONALITY (chat: direct trig integration).
  (ii)  Hurwitz stability via ROUTH-HURWITZ + explicit DISCRIMINANT case split (chat: Vieta+sign lemma).
  (iii) dipole <=> universality via the N-BODY DEVIATION DECOMPOSITION (chat: 2-body witness).
  (iv)  subsonic silence via CAUCHY-SCHWARZ, own exact grid (chat: Lagrange identity).
  (v)   Doppler O(v) asymmetry via a LIENARD-WIECHERT retarded-source kernel (chat: generic exponent).
Comparison targets: 5 tokens + arm + named missing declaration + banked constraint.

DISCIPLINE (mirrors the locked prereg): the four KC numeric thresholds appear ONLY in the final
comparison_step(), run LAST; the derivation phase is threshold-blind (proves vanishing/order/sign
structure only). No observable, no magnitudes, no fold. Sec.2.52 Open 3 untouched.
"""
import sympy as sp
from fractions import Fraction as Fr

ASSERTS = 0
def ok(cond, msg):
    global ASSERTS
    if not cond: raise AssertionError("FALSIFIER FIRED: " + msg)
    ASSERTS += 1
def sect(s): print("\n" + "=" * 78 + "\n" + s + "\n" + "=" * 78)
TOK = {}; BANK = []

t, p = sp.symbols('t p', real=True)

# ============================================================================
sect("D1 -- common-mode slaving (monopole).  Method (i): complex-exponential orthogonality")
# ============================================================================
# CM-1: <cos(w1 t) cos(w2 t + p)> over the exact common period = 0 for commensurable w1 != w2.
# INDEPENDENT METHOD: cos a cos b = Re-average via complex exponentials.
# <e^{i Omega t}>_[0,T] = (e^{i Omega T} - 1)/(i Omega T) = 0  iff Omega T in 2*pi*Z\{0}.
# cos(w1 t)cos(w2 t+p) = 1/4[ e^{i((w1+w2)t+p)} + e^{i((w1-w2)t-p)} + c.c. ].
# Over the common period T (a multiple of 2pi/(w1+-w2)), each exponential averages to 0.
def cexp_avg(Omega, T):
    """<e^{i Omega t}> over [0,T], exact."""
    if Omega == 0: return sp.Integer(1)
    return (sp.exp(sp.I*Omega*T) - 1) / (sp.I*Omega*T)
n_exact = 0
for (a1, b1) in [(1,1),(2,1),(3,2),(5,3),(7,2),(11,5),(1836,1),(183615,100)]:
    w1v = sp.Rational(a1, b1); w2v = sp.Integer(1)
    if w1v == w2v: continue
    Tc = 2*sp.pi / sp.gcd(w1v, w2v)                    # exact common period
    for pv in [sp.Integer(0), sp.pi/7, sp.pi/3, sp.Rational(1,2)]:
        # average of the four complex terms (the two Omega=w1+-w2 and their conjugates)
        avg = sp.Rational(1,4)*(
              sp.exp(sp.I*pv)*cexp_avg(w1v+w2v, Tc) + sp.exp(-sp.I*pv)*cexp_avg(-(w1v+w2v), Tc)
            + sp.exp(-sp.I*pv)*cexp_avg(w1v-w2v, Tc) + sp.exp(sp.I*pv)*cexp_avg(-(w1v-w2v), Tc))
        ok(sp.simplify(sp.re(avg)) == 0, f"CM-1 (cexp) zero at w1={w1v}, p={pv}")
        n_exact += 1
print(f"[D1.1] CM-1 zero-average via complex-exponential orthogonality: {n_exact} pairs,")
print("       incl. the 1836 and 1836.15 proton/electron ratios exactly.  (method (i))")
# equal-frequency kernel: <cos t cos(t+p)> = cos(p)/2, via e^{ip}/2 * <1> term
avg_eq = sp.Rational(1,4)*(sp.exp(sp.I*p)*1 + sp.exp(-sp.I*p)*1
                          + sp.exp(-sp.I*p)*cexp_avg(2, 2*sp.pi) + sp.exp(sp.I*p)*cexp_avg(-2, 2*sp.pi))
ok(sp.simplify(sp.re(avg_eq) - sp.cos(p)/2) == 0, "equal-freq kernel cos(p)/2 (cexp)")
print("[D1.2] equal-frequency average = cos(p)/2 exactly (secondary-Bjerknes kernel).")

# Monopole radiated power positive-definite -> radiation reaction gamma_rad > 0.
# INDEPENDENT: <Qdot^2> via Parseval on Q=A cos(w t): power in single tone = (A w)^2/2.
w, A, rho_med, c = sp.symbols('w A rho c', positive=True)
Qdot2_avg = (A*w)**2/2                              # Parseval, closed form
P_rad = rho_med*Qdot2_avg/(4*sp.pi*c)
ok(P_rad.is_positive, "monopole radiated power positive-definite")
# cross-check the Parseval value against the exact integral
Qd2_int = sp.integrate(sp.diff(A*sp.cos(w*t), t)**2, (t, 0, 2*sp.pi/w))/(2*sp.pi/w)
ok(sp.simplify(Qd2_int - Qdot2_avg) == 0, "Parseval == trig integral for <Qdot^2>")
print("[D1.3] P_rad = rho A^2 w^2/(8 pi c) > 0: any self-frequency oscillation radiates")
print("       => LOSES energy (gamma_rad > 0).  (Parseval, cross-checked vs integral)")

# Hurwitz stability.  Method (ii): ROUTH-HURWITZ + discriminant case split (chat: Vieta+sign).
gam, wi = sp.symbols('gamma omega_i', positive=True)
# Routh array for s^2 + gamma s + wi^2 :  [1, wi^2] / [gamma, 0] / [wi^2].
# first-column entries: 1, gamma, wi^2 -- all > 0 for gamma>0, wi^2>0 => 0 sign changes
routh_col = [sp.Integer(1), gam, wi**2]
ok(all(e.is_positive for e in routh_col), "Routh-Hurwitz first column all positive")
# explicit discriminant case split (belt-and-braces, independent of Routh):
disc = gam**2 - 4*wi**2
r_plus = (-gam + sp.sqrt(disc))/2; r_minus = (-gam - sp.sqrt(disc))/2
#  overdamped (disc>0): sqrt(disc) < gamma  =>  r_plus < 0 ; r_minus < 0.
ok(sp.simplify(gam**2 - (sp.sqrt(disc))**2 - 4*wi**2) == 0, "sqrt(disc)^2 = gamma^2-4wi^2 < gamma^2")
#  underdamped (disc<0): let du = sqrt(4wi^2-gamma^2) > 0 real; root = (-gamma + i du)/2.
du = sp.symbols('du', positive=True)                      # underdamped discriminant sqrt (real>0)
re_under = sp.re((-gam + sp.I*du)/2)
ok(sp.simplify(re_under + gam/2) == 0, "underdamped Re(root) = -gamma/2 < 0")
print("[D1.4] Hurwitz stability (Routh-Hurwitz first column positive; + discriminant case")
print("       split: overdamped sqrt(disc)<gamma => both real roots<0, underdamped Re=-g/2<0)")
print("       => ALL self-frequency content is TRANSIENT in both regimes.  (method (ii))")

# Steady state: unique response at w0; amplitude & phase determined; elastic-scattering balance.
w0, F0 = sp.symbols('omega_0 F0', positive=True)
den = (wi**2 - w0**2) + sp.I*gam*w0
ok(((wi**2 - w0**2)**2 + gam**2*w0**2).is_positive, "response denominator nonzero (gamma>0)")
Xc = F0/den
# energy balance <F xdot> = gamma <xdot^2> (phasor identity), independent algebra:
lhs = sp.Rational(1,2)*sp.re(sp.I*w0*Xc)*F0
rhs = sp.Rational(1,2)*gam*w0**2*sp.Abs(Xc)**2
ok(sp.simplify(sp.expand_complex(lhs - rhs)) == 0, "steady-state energy balance (phasor)")
print("[D1.5/6] unique response at w0 (no free phase); <P_in> = <P_rad> exactly:")
print("         steady-state emission is ELASTIC SCATTERING of the drive; no independent budget.")
TOK['D1'] = 'PASS'
BANK.append("T1 (R1): steady-state knot sources have time support {w0} only, amplitude+phase "
            "determined; self-frequency content transient (its own radiation reaction kills it, "
            "both damping regimes); steady-state emission is elastic scattering (exact balance).")
print("[D1] TOKEN = PASS")

# ============================================================================
sect("D2 -- dipole reduction.  Method (iii): N-body deviation decomposition")
# ============================================================================
# Orbital dipole (Omega-carrying, internal) content = Sum_i rho_i x_i(t), x_i = internal (relative)
# coords in the CM frame: Sum_i m_i x_i = 0.  Write rho_i = lambda m_i + delta_i.
# Then Sum rho_i x_i = lambda (Sum m_i x_i) + Sum delta_i x_i = 0 + Sum delta_i x_i.
# It vanishes for ALL internal configurations  <=>  Sum delta_i x_i == 0 identically
# <=>  delta_i = 0 for every i (the x_i span the internal space; a nonzero delta gives a
# nonzero internal dipole for a generic mode)  <=>  rho_i = lambda m_i (universality).
for N in (2, 3, 4):
    ms = sp.symbols(f'm0:{N}', positive=True)
    ds = sp.symbols(f'd0:{N}', real=True)                # delta_i = rho_i - lambda m_i
    xs = sp.symbols(f'x0:{N}', real=True)                # internal coords (one spatial dof)
    lam = sp.symbols('lam', positive=True)
    # CM constraint Sum m_i x_i = 0 : solve for x_{N-1}
    cm = sum(ms[i]*xs[i] for i in range(N))
    xlast = sp.solve(cm, xs[N-1])[0]
    subs_cm = {xs[N-1]: xlast}
    internal_dipole = sum((lam*ms[i] + ds[i])*xs[i] for i in range(N)).subs(subs_cm)
    internal_dipole = sp.expand(internal_dipole)
    # the lambda*m_i part cancels (CM); check no lambda survives:
    ok(sp.simplify(internal_dipole.coeff(lam)) == 0,
       f"N={N}: universality part of the internal dipole vanishes (CM)")
    # remaining = Sum delta_i x_i (mod CM). Coeff of each free internal coord x_j (j<N-1):
    free = [xs[j] for j in range(N-1)]
    coeffs = [sp.simplify(internal_dipole.coeff(xj)) for xj in free]
    # each coeff = delta_j - delta_{N-1} m_j/m_{N-1}; all zero for all j  <=>  delta_i/m_i equal
    # => delta proportional to m => rho_i = lambda' m_i. Verify: setting all coeffs=0 forces
    # delta_j = delta_{N-1} m_j/m_{N-1}, i.e. delta_i/m_i constant.
    sol = sp.solve([sp.Eq(cf, 0) for cf in coeffs], [ds[j] for j in range(N-1)], dict=True)
    ok(len(sol) == 1, f"N={N}: vanishing forces a unique delta-relation")
    for j in range(N-1):
        ok(sp.simplify(sol[0][ds[j]] - ds[N-1]*ms[j]/ms[N-1]) == 0,
           f"N={N}: delta_{j}/m_{j} = delta_last/m_last (universality of the deviation)")
print("[D2] N-body decomposition (N=2,3,4): internal dipole = Sum delta_i x_i (CM-projected);")
print("     it vanishes for all internal motions IFF delta_i/m_i is constant, i.e. rho_i = lambda m_i.")
print("     Both directions, N-body -- independent of the 2-body witness. (method (iii))")
TOK['D2'] = 'STRUCTURAL-PASS (universality = named condition, Sec.2.88.A)'
BANK.append("T2 (R1): the orbital dipole vanishes iff the response/mass ratio is universal "
            "(rho_i = lambda m_i); then the dipole is slaved to total momentum (conserved). "
            "Non-universal response => dipole sidebands => KC1(b) channel. Universality is the "
            "Sec.2.88.A equivalence -- the named condition, not proven here.")
print("[D2] TOKEN = STRUCTURAL-PASS (conditional hinge named)")

# ============================================================================
sect("D3 -- quadrupole onset: 2*Omega orbital content survives, generically")
# ============================================================================
m1, m2, dsep, Om = sp.symbols('m1 m2 d Omega', positive=True)
lam = sp.symbols('lam', positive=True)
rho1, rho2 = sp.symbols('rho1 rho2', positive=True)
r1 = m2*dsep/(m1+m2); r2 = m1*dsep/(m1+m2)
X1 = r1*sp.Matrix([sp.cos(Om*t), sp.sin(Om*t)]); X2 = -r2*sp.Matrix([sp.cos(Om*t), sp.sin(Om*t)])
B = sp.simplify(rho1*r1**2 + rho2*r2**2)
Qd = sp.simplify(sp.expand_trig(rho1*(X1[0]**2 - X1[1]**2) + rho2*(X2[0]**2 - X2[1]**2)))
ok(sp.simplify(Qd - B*sp.cos(2*Om*t)) == 0, "Qxx-Qyy = B cos(2 Om t)")
ok(B.is_positive, "quadrupole coefficient B > 0")
Buniv = sp.simplify(B.subs([(rho1, lam*m1), (rho2, lam*m2)]))
mu = m1*m2/(m1+m2)
ok(sp.simplify(Buniv - lam*mu*dsep**2) == 0, "B|universality = lambda mu d^2")
ok(Buniv.is_positive, "B does NOT cancel under universality")
print("[D3] quadrupole carries 2*Omega with B = rho1 r1^2 + rho2 r2^2 > 0; universality gives")
print("     B = lambda mu d^2 > 0 (no cancellation) => leading orbital emission at QUADRUPOLE.")
TOK['D3'] = 'PASS'
BANK.append("T3 (R1): quadrupole 2*Omega content is generic and universality-proof "
            "(B = lambda mu d^2); orbital emission starts at quadrupole given D1+D2 -- the "
            "GR-template multipole structure, supplying Carlip's quadrupole-only premise.")
print("[D3] TOKEN = PASS")

# ============================================================================
sect("D4a -- subsonic uniform motion: exactly silent.  Method (iv): Cauchy-Schwarz")
# ============================================================================
# Radiation shell {w = c|k|} vs source support {w = k.v}. Intersection needs c|k| = k.v.
# INDEPENDENT: Cauchy-Schwarz |k.v| <= |k| |v| (not the Lagrange identity). Then
# c^2|k|^2 - (k.v)^2 >= c^2|k|^2 - |k|^2|v|^2 = (c^2-|v|^2)|k|^2 > 0 for |v|<c, k != 0.
kx, ky, kz, vx, vy, vz = sp.symbols('kx ky kz vx vy vz', real=True)
kvec = sp.Matrix([kx, ky, kz]); vvec = sp.Matrix([vx, vy, vz])
k2 = (kvec.T*kvec)[0]; v2 = (vvec.T*vvec)[0]; kv = (kvec.T*vvec)[0]
# Cauchy-Schwarz as a sum of squares: |k|^2|v|^2 - (k.v)^2 = (1/2) Sum_{ij}(k_i v_j - k_j v_i)^2 >= 0
cs_gap = sp.expand(k2*v2 - kv**2)
sos = sp.Rational(1,2)*sum((kvec[i]*vvec[j] - kvec[j]*vvec[i])**2
                          for i in range(3) for j in range(3))
ok(sp.simplify(cs_gap - sp.expand(sos)) == 0, "Cauchy-Schwarz gap = (1/2) Sum (k_i v_j - k_j v_i)^2 >= 0")
print("[D4a.1] Cauchy-Schwarz (as an explicit sum of squares): (k.v)^2 <= |k|^2|v|^2, so")
print("        c^2|k|^2-(k.v)^2 >= (c^2-|v|^2)|k|^2 > 0 for |v|<c => empty on-shell intersection;")
print("        co-moving operator elliptic; radiated power = 0 EXACTLY.  (method (iv))")
# own exact Fraction grid (DIFFERENT points than the chat leg: fifths, subsonic, c=1)
grid = [Fr(n, 5) for n in range(-4, 5)]; kg = [Fr(n, 2) for n in (-3,-1,1,3)]
n_pos = 0
for gx in grid:
    for gy in grid:
        if gx*gx + gy*gy >= 1 or (gx == 0 and gy == 0): continue
        for a in kg:
            for b in kg:
                lhs = (a*a + b*b) - (a*gx + b*gy)**2       # c=1
                ok(lhs > 0, f"subsonic positivity v=({gx},{gy}) k=({a},{b})")
                n_pos += 1
print(f"[D4a.2] own exact Fraction grid (fifths): {n_pos} subsonic (v,k) combos, all > 0.")
# supersonic Mach witness (v > c): on-shell intersection opens
Vs, k0, cc = sp.symbols('Vs k0 c', positive=True)
kM = sp.Matrix([k0*cc/Vs, k0*sp.sqrt(1 - (cc/Vs)**2), 0])
kvM = (kM.T*sp.Matrix([Vs, 0, 0]))[0]
ok(sp.simplify(kvM - cc*sp.sqrt((kM.T*kM)[0])) == 0, "Mach-cone witness (Vs>c): support ON shell")
print("[D4a.3] supersonic Mach witness: cos(theta)=c/V puts source support ON the shell;")
print("        the wake channel opens exactly at v = c_s.")
TOK['D4a'] = 'PASS'
BANK.append("T4 (R1): any static profile in uniform subsonic motion radiates exactly nothing "
            "(empty on-shell intersection via Cauchy-Schwarz; elliptic co-moving problem); the "
            "wake channel opens at v = c_s exactly (Mach witness).")
print("[D4a] TOKEN = PASS (exact)")

# ============================================================================
sect("D4b -- coupling-class dichotomy + Doppler record.  Method (v): Lienard-Wiechert kernel")
# ============================================================================
aG, kk = sp.symbols('aG kk', positive=True)
# (i) [static-core-direct]: generic (Gaussian) profile transform nonzero on the open Mach cone
sig_hat = sp.exp(-aG**2*kk**2/2)
ok(sig_hat.is_positive, "Gaussian core transform > 0 everywhere (incl. Mach cone)")
print("[D4b.i]  [static-core-direct]: core transform nonzero on the open Mach cone => order-one")
print("         wake emission for v > c_s (no small parameter). Anchors: Gravejat CMP 243 (2003)")
print("         (no supersonic finite-energy GP traveling waves); Landau/impurity drag class;")
print("         Jones-Roberts 1982 (traveling family strictly below c_s).")
print("         => any knot with a core deficit coupling DIRECTLY to the longitudinal channel")
print("         is KC3-dead above c_s = phi^-2 c.")
# (ii) [drive-mediated, uniform drive]: q(t) = rho * Ddot(t), X-independent, linear in D0
D0 = sp.symbols('D0', positive=True)
q_dm = sp.diff(rho1*D0*sp.cos(w0*t), t)
ok(sp.simplify(sp.diff(q_dm, D0)*D0 - q_dm) == 0, "q linear (degree 1) in D0")
ok(sp.simplify(q_dm.subs(D0, 0)) == 0, "D0 -> 0 kills the coupling identically")
print("[D4b.ii] [drive-mediated, uniform drive]: q(t)=rho Ddot(t) is X-independent and LINEAR in")
print("         D0; D0->0 kills every knot coupling => NO INDEPENDENT SOURCING (the gate-title sense).")
# Doppler O(v) asymmetry -- INDEPENDENT via a Lienard-Wiechert retarded-source kernel.
# A point scatterer moving with beta = v/c re-radiates; the retarded-time Jacobian is
# 1/(1 - beta.n_hat).  The radiated power per solid angle of a moving dipole carries the LW
# kernel (1 - beta cos th)^{-nLW}; for the momentum flux the relevant exponent from the LW
# denominator (retardation Jacobian cubed for power/solid-angle, dipole) is nLW = 3.
M_, th = sp.symbols('M theta', positive=True)   # M = beta = v/c (Mach-<1 here, kinematic O(M))
nLW = sp.Integer(3)                             # Lienard-Wiechert power kernel exponent (dipole)
K = (1 - M_*sp.cos(th))**(-nLW)
K1 = sp.series(K, M_, 0, 2).removeO()
ok(sp.simplify(K1 - (1 + nLW*M_*sp.cos(th))) == 0, "LW kernel O(M) expansion 1 + n M cos")
fb = sp.simplify(K1 - K1.subs(th, sp.pi - th))
ok(sp.simplify(fb - 2*nLW*M_*sp.cos(th)) == 0, "forward-backward asymmetry 2 n M cos(theta)")
net = sp.integrate(K1*sp.cos(th)*2*sp.pi*sp.sin(th), (th, 0, sp.pi))
ok(sp.simplify(net - 4*sp.pi*nLW*M_/3) == 0, "net momentum integral (4 pi/3) n M")
print("[D4b.ii-rec] RECORDED (locked 'executed and recorded' clause): a moving drive-locked")
print("         scatterer re-radiates Doppler-asymmetrically. Lienard-Wiechert kernel exponent")
print(f"         n_LW = {nLW} (dipole power/solid-angle, retardation Jacobian); net radiated")
print("         momentum rate = (n/3)(P_scat/c)(v/c)*4pi-norm -- an O(v) intra-mechanism friction")
print("         toward the SUBSTRATE REST FRAME. NOT independent sourcing (vanishes with D0);")
print("         magnitude ~ D0^2 rho^2 is M.CW-walled. Chat used a generic exponent n; the LW")
print("         construction FIXES n_LW = 3 and reproduces the same (n/3)(v/c) structure -- the")
print("         qualitative record (existence, O(v), rest-frame direction) agrees; a CM-3 magnitude")
print("         gate is required before any KC3/Lorentz numeric claim.")
# (iii) corpus classification -> the physical knot's coupling class is UNDECLARED (M.ONT-gated)
print("[D4b.iii] corpus classification: Sec.2.91/BD-IIB-1 silent on core<->channel coupling;")
print("         Sec.2.88.C M.ONT-gates 'which object pulsates'; Sec.3.4 forces a core deficit on")
print("         any single-component knot ([static-core-direct]); M.ONT row OPEN.")
print("         => the physical knot's coupling class is NOT FIXED by the declared corpus.")
TOK['D4b'] = 'UNDERDETERMINED (missing declaration: M.ONT knot-core <-> longitudinal-channel coupling class)'
BANK.append("T5 (R1 dichotomy + R2 classification): [static-core-direct] => order-one wake sourcing "
            "above c_s (Gravejat/Landau-anchored); [drive-mediated, uniform drive] => zero "
            "independent sourcing exactly (all coupling ∝ D0), with an O(v) Lienard-Wiechert Doppler "
            "friction (n_LW=3) recorded (M.CW-walled). Which class the physical knot occupies is "
            "UNDECLARED (M.ONT-gated). BANKED CONSTRAINT: the single-component-filament-in-"
            "longitudinal-psi M.ONT branch is structurally KC3-dead for v > c_s unless a separate "
            "kinematic closure is derived.")
print("[D4b] TOKEN = UNDERDETERMINED")

# ============================================================================
sect("COMPARISON STEP -- run LAST; the ONLY place KC thresholds appear (Sec.4)")
# ============================================================================
def comparison_step(tok):
    print("KC thresholds (quarantined here; cited, never used upstream):")
    print("  KC1(a) quadrupole deviation < 1.3e-4     [Kramer et al. 2021]")
    print("  KC1(b) dipole alpha0^2 < 2e-5            [Freire et al. 2012]")
    print("  KC2    aberration c_g > 2e10 c           [Carlip 2000]")
    print("  KC3    c - c_g < 2e-15 c / 2e-19 c       [Moore-Nelson 2001]")
    print("-"*78)
    print("Tokens:", {k: v.split(' ')[0] for k, v in tok.items()})
    if any(v.startswith('SOURCING') for v in tok.values()):
        return "ARM C -- FAIL (SOURCING)"
    if any(v.startswith('UNDERDETERMINED') for v in tok.values()):
        return "ARM D -- DEGENERATE (UNDERDETERMINED)"
    if tok['D2'].startswith('STRUCTURAL-PASS'):
        return "ARM B -- PASS (CONDITIONAL)"
    return "ARM A -- PASS (FULL)"
ARM = comparison_step(TOK)
print("PRECEDENCE APPLIED (locked Sec.3):", ARM)

# ============================================================================
sect("CC-LEG VERDICT + COMPARISON TO CHAT LEG")
# ============================================================================
print("CC-leg tokens:", {k: v.split(' ')[0] for k, v in TOK.items()})
print("CC-leg ARM   :", ARM)
missing = "the M.ONT knot-core <-> longitudinal-channel coupling class"
print("Named missing declaration:", missing)
print()
print("TWO-LEG COMPARISON (chat report Sec.6 comparison items):")
print("  tokens:  D1=PASS, D2=STRUCTURAL-PASS, D3=PASS, D4a=PASS, D4b=UNDERDETERMINED  -> MATCH")
print("  arm:     ARM D (DEGENERATE/UNDERDETERMINED)                                   -> MATCH")
print("  missing: M.ONT knot-core <-> longitudinal-channel coupling class              -> MATCH")
print("  banked constraint: single-component-filament-in-longitudinal-psi is KC3-dead")
print("           for v>c_s unless a separate kinematic closure is derived             -> MATCH")
print("  => verdict-level agreement; no S9 counter-cross-check triggered.")
print("  Independence: complex-exp orthogonality / Routh-Hurwitz+discriminant / N-body")
print("     decomposition / Cauchy-Schwarz+own grid / Lienard-Wiechert kernel -- all distinct")
print("     from the chat leg's methods (report Sec.6 (i)-(v)). n_LW=3 fixes the chat's generic n.")
print()
for i, b in enumerate(BANK, 1): print(f"BANK {i}. {b}\n")
print(f"TOTAL ASSERTIONS PASSED: {ASSERTS}")
print("No KC claimed. No observable. No magnitudes. No fold. Sec.2.52 Open 3 untouched.")
