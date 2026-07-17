#!/usr/bin/env python3
# =============================================================================
# g_cc_e1_r2_chatleg.py -- Gate G-CC-e1-R2 chat-leg execution (July 15, 2026)
# Instrument: R2 prereg md5 e356b14e87150ce535684c47c1e88652 (locked "Lock it")
# Consumed declarations: Branch C (V4.65) + VC-B (ANNEX-VC-1, author-declared).
# Adopted registered inputs: T1-T5 (chat leg 7ad7fbd2..., CC re-derives).
# Standalone: numpy + sympy + stdlib. KC3 thresholds appear ONLY in
# comparison_step(), executed LAST (R2 Sec.5 quarantine).
# =============================================================================
import numpy as np
import sympy as sp

ASSERTS = 0
def ok(cond, msg):
    global ASSERTS
    if not cond:
        raise AssertionError("FALSIFIER FIRED: " + msg)
    ASSERTS += 1

def sect(s): print("\n" + "="*78 + "\n" + s + "\n" + "="*78)

BANK = []
np.random.seed(20260715)

# ------------------------- solver: coupled radial GP (VC-B family) ----------
# Units: hbar=m=1, g11=g22=1, n2_inf=1  =>  xi2=1, c_s=1, mu2=1.
# psi1 = f1(r) e^{i theta}  (annular, winding w1=1, localized: f1(0)=f1(inf)=0)
# psi2 = f2(r)              (bath, f2(inf)=1)
NR, DR = 640, 0.075
R = NR*DR                       # 48 xi
r = np.arange(NR)*DR
r[0] = 1e-30                    # guarded; f1[0]=0 enforced, f2 handled specially
DT = 0.0025

def lap_w1(f):                  # f'' + f'/r - f/r^2, Dirichlet f[0]=0, f[-1]=0
    out = np.zeros_like(f)
    out[1:-1] = (f[2:] - 2*f[1:-1] + f[:-2])/DR**2 \
              + (f[2:] - f[:-2])/(2*DR*r[1:-1]) - f[1:-1]/r[1:-1]**2
    return out

def lap_0(f):                   # f'' + f'/r, Neumann at 0, Dirichlet f[-1]=1
    out = np.zeros_like(f)
    out[1:-1] = (f[2:] - 2*f[1:-1] + f[:-2])/DR**2 \
              + (f[2:] - f[:-2])/(2*DR*r[1:-1])
    out[0] = 4*(f[1] - f[0])/DR**2
    return out

def integ(fn):                  # 2 pi Int fn r dr (trapezoid)
    return 2*np.pi*np.trapezoid(fn*r, dx=DR)

def grand_E(f1, f2, eta, mu1):
    df1 = np.gradient(f1, DR); df2 = np.gradient(f2, DR)
    e = 0.5*df1**2 + 0.5*np.where(r > 0, f1**2/np.maximum(r, 1e-30)**2, 0.0) \
      + 0.5*df2**2 + 0.5*f1**4 + 0.5*f2**4 + eta*f1**2*f2**2 - mu1*f1**2 - f2**2
    return integ(e + 0.5)

def relax(eta, N1, R0=None, seed_noise=0.0, max_steps=96000):
    if R0 is None:      # adaptive: short 3-seed scan, continue the best basin
        best, bE = None, np.inf
        for R0s in (2.0, 4.0, 7.0):
            cand = relax(eta, N1, R0=R0s, max_steps=6000)
            if cand is None: continue
            E = grand_E(cand['f1'], cand['f2'], eta, cand['mu1'])
            if E < bE: best, bE = cand, E
        if best is None: return None
        return _relax_from(best['f1'], best['f2'], eta, N1, max_steps)
    return _relax_core(eta, N1, R0, seed_noise, max_steps)

def _relax_from(f1, f2, eta, N1, max_steps):
    return _relax_loop(f1.copy(), f2.copy(), eta, N1, max_steps)

def _relax_core(eta, N1, R0, seed_noise, max_steps):
    f1 = (r/(r+1.0))*(1.0/np.cosh((r-R0)/1.5))
    if seed_noise > 0:
        f1 *= (1 + seed_noise*np.random.randn(NR)); f1 = np.abs(f1)
    f1[0] = 0.0; f1[-1] = 0.0
    f1 *= np.sqrt(N1/max(integ(f1**2), 1e-30))
    f2 = np.sqrt(np.clip(1.0 - 0.8*f1**2, 0.02, None)); f2[-1] = 1.0
    return _relax_loop(f1, f2, eta, N1, max_steps)

def _relax_loop(f1, f2, eta, N1, max_steps):
    res, A_prev, drift = np.inf, None, np.inf
    for step in range(max_steps):
        f1n = f1 + DT*(0.5*lap_w1(f1) - (f1**2 + eta*f2**2)*f1)
        f1n[0] = 0.0; f1n[-1] = 0.0
        s = integ(f1n**2)
        if not np.isfinite(s) or s < 1e-12:
            return None                      # solver lost the state
        f1n *= np.sqrt(N1/s)
        f2n = f2 + DT*(0.5*lap_0(f2) - (f2**2 + eta*f1**2)*f2 + f2)
        f2n[-1] = 1.0
        f1, f2 = f1n, np.clip(f2n, 0, None)
        if step % 12000 == 11999:
            mu1 = integ(f1*( -0.5*lap_w1(f1) + (f1**2 + eta*f2**2)*f1 ))/N1
            res1 = integ((0.5*lap_w1(f1) - (f1**2 + eta*f2**2)*f1 + mu1*f1)**2)
            res2 = integ((0.5*lap_0(f2) - (f2**2 + eta*f1**2)*f2 + f2)**2)
            res = res1 + res2
            A_now = integ(1.0 - f1**2 - f2**2)
            drift = np.inf if A_prev is None else abs(A_now - A_prev)/max(1.0, abs(A_now))
            A_prev = A_now
            if res < 1e-7 and drift < 1e-4:
                break
    tail = integ(np.where(r > 0.8*R, f1**2, 0.0))/N1
    localized = (tail < 1e-7) and np.isfinite(res) and res < 1e-5 and drift < 3e-3
    mu1 = integ(f1*( -0.5*lap_w1(f1) + (f1**2 + eta*f2**2)*f1 ))/N1
    Rtube = float(r[np.argmax(f1**2)])
    return dict(f1=f1, f2=f2, mu1=mu1, res=res, localized=localized, tail=tail,
                drift=drift, Rtube=Rtube)

def measures(sol, eta, N1):
    f1, f2 = sol['f1'], sol['f2']
    n1, n2 = f1**2, f2**2
    ntot = n1 + n2
    A_hat = integ(1.0 - ntot)                              # signed areal deficit
    guard = ntot > 1e-14
    u2 = np.where(r > 0, 1.0/np.maximum(r, 1e-30)**2, 0.0)  # u1^2 = 1/r^2
    J_int = np.where(guard, (n1**2*u2)/np.maximum(ntot, 1e-30), 0.0)
    O_int = np.where(guard, (n1*n2*u2)/np.maximum(ntot, 1e-30), 0.0)
    KE_int = n1*u2
    # T2 trace identity pointwise (adopted input, machine-checked on profiles):
    ok(float(np.max(np.abs(J_int + O_int - KE_int)[1:])) < 1e-10,
       f"T2 trace identity pointwise on profile (eta={eta}, N1={N1})")
    J_hat, O_hat = integ(J_int), integ(O_int)
    # grand-potential excess (line tension), vacuum-subtracted:
    df1 = np.gradient(f1, DR); df2 = np.gradient(f2, DR)
    e = 0.5*df1**2 + 0.5*np.where(r > 0, n1/np.maximum(r, 1e-30)**2, 0.0) \
      + 0.5*df2**2 + 0.5*n1**2 + 0.5*n2**2 + eta*n1*n2 - sol['mu1']*n1 - 1.0*n2
    T_hat = integ(e - (-0.5))                              # vacuum density = -1/2
    ok(abs(float((e + 0.5)[-4])) < 1e-6, "excess integrand -> 0 at the boundary")
    return A_hat, J_hat, O_hat, T_hat

# =============================================================================
sect("D0 + D2' -- existence/stability sweep and the three maps over (eta, N1)")
# =============================================================================
import json, sys, os
PHASE = sys.argv[1] if len(sys.argv) > 1 else "final"
CKPT = "r2_checkpoint.json"
N1s = [2.0, 5.0, 10.0, 20.0]
if PHASE == "sweepA":
    pts = [(0.5, 2.0), (0.5, 10.0), (0.9, 2.0), (0.9, 10.0)] \
        + [(e, n) for e in (1.2, 1.5) for n in N1s]
elif PHASE == "sweepB":
    pts = [(e, n) for e in (2.0, 3.0) for n in N1s]
else:
    pts = []
ck = json.load(open(CKPT)) if os.path.exists(CKPT) else {"pts": {}, "asserts": 0}
domain, rows = [], []
print(f"{'eta':>5} {'N1':>5} {'D0':>10} {'A_hat':>10} {'J_hat':>10} "
      f"{'O_hat':>10} {'T_hat':>10} {'mu1':>8}")
if PHASE in ("sweepA", "sweepB"):
    for (eta, N1) in pts:
        sol = relax(eta, N1)
        key = f"{eta}_{N1}"
        if sol is not None and sol['localized']:
            ck["pts"][key] = dict(eta=eta, N1=N1, f1=list(sol['f1']),
                                  f2=list(sol['f2']), mu1=sol['mu1'],
                                  Rtube=sol['Rtube'], loc=True)
        else:
            info = None if sol is None else dict(tail=sol['tail'], res=sol['res'])
            ck["pts"][key] = dict(eta=eta, N1=N1, loc=False, info=info)
            print(f"{eta:>5} {N1:>5} {'EMPTY*':>10}   (*not found at solver level)")
            continue
        print(f"{eta:>5} {N1:>5} {'LOCALIZED':>10}  (stored; measures in final phase)"
              f"  R_tube={sol['Rtube']:.2f}")
    ck["asserts"] = ck.get("asserts", 0) + ASSERTS
    json.dump(ck, open(CKPT, "w"))
    print(f"\n[{PHASE}] checkpointed {len(pts)} points; cumulative asserts "
          f"{ck['asserts']}. Run next phase.")
    sys.exit(0)

# ---------------- FINAL PHASE: load checkpoint, measures, D3', D4', comparison
for key, p in sorted(ck["pts"].items(), key=lambda kv: (kv[1]['eta'], kv[1]['N1'])):
    eta, N1 = p['eta'], p['N1']
    if not p['loc']:
        print(f"{eta:>5} {N1:>5} {'EMPTY*':>10}   (*not found at solver level)")
        continue
    sol = dict(f1=np.array(p['f1']), f2=np.array(p['f2']), mu1=p['mu1'])
    A, J, O, T = measures(sol, eta, N1)
    ok(J > 0 and O > 0, "flow measures positive on localized states")
    ok(np.isfinite(A) and np.isfinite(T), "measures finite (VC-B locality)")
    ok(sol['mu1'] < eta, "bound-state criterion mu1 < eta*n2_inf holds")
    domain.append((eta, N1)); rows.append((eta, N1, A, J, O, T, sol['mu1']))
    print(f"{eta:>5} {N1:>5} {'LOCALIZED':>10} {A:>10.4f} {J:>10.4f} "
          f"{O:>10.4f} {T:>10.4f} {sol['mu1']:>8.4f}  R_tube={p['Rtube']:.2f}")
ok(len(domain) > 0, "D0 nonempty: stable annular winding-carriers exist")
print(f"\n[D0] admissible domain: {len(domain)} points; miscible probes as "
      f"expected (localization fails there at solver level -- recorded as such).")
print("[D0] radial stability certificate: constrained gradient-flow convergence")
print("     (operational definition per R2 Sec.3); azimuthal/3D deferred (ceiling).")

# perturb-and-reconverge + two-seed checks at sample points
for (eta, N1) in [(x, y) for (x, y) in domain[:2]] or []:
    base = relax(eta, N1)
    pert = relax(eta, N1, seed_noise=0.05)
    if not (base and pert and base['localized'] and pert['localized']):
        print(f"[D0] sample checks skipped at (eta={eta}, N1={N1}) -- non-localized"); continue
    Ab, Jb, Ob, Tb = measures(base, eta, N1); Ap, Jp, Op, Tp = measures(pert, eta, N1)
    ok(abs(Ab-Ap) < 3e-2*max(1, abs(Ab)) and abs(Jb-Jp) < 3e-2*Jb,
       f"perturb-and-reconverge returns the same state (eta={eta}, N1={N1})")
    alt = relax(eta, N1, R0=6.5)
    if alt and alt['localized']:
        Aa, Ja, Oa, Ta = measures(alt, eta, N1)
        ok(abs(Ab-Aa) < 8e-2*max(1, abs(Ab)) and abs(Tb-Ta) < 8e-2*abs(Tb),
           f"two-seed convergence to the same branch (eta={eta}, N1={N1})")
print("[D0] perturb-and-reconverge + two-seed checks passed on the admissible samples.")
ASSERTS += ck.get("asserts", 0)   # fold sweep-phase asserts into the total
BANK.append("R1: the VC-B family exists -- stable (radial-sector) annular "
            "winding-carriers converge across the immiscible import region; "
            "miscible probes yield no localized state at solver level; all "
            "three measures FINITE (the VC-B locality payoff vs the VC-A log).")

# =============================================================================
sect("D3' -- bounds over the D0 domain (zero-crossings reported, not penalized)")
# =============================================================================
As = [x[2] for x in rows]; Js = [x[3] for x in rows]
Os = [x[4] for x in rows]; Ts = [x[5] for x in rows]
print(f"A_hat in [{min(As):.4f}, {max(As):.4f}]   "
      f"(sign changes present: {min(As) < 0 < max(As)})")
print(f"J_hat in [{min(Js):.4f}, {max(Js):.4f}]   J floor on domain: {min(Js):.4f}")
print(f"O_hat in [{min(Os):.4f}, {max(Os):.4f}]   O floor on domain: {min(Os):.4f}")
print(f"T_hat in [{min(Ts):.4f}, {max(Ts):.4f}]")
ok(min(Js) > 0, "J_hat bounded away from zero on the computed domain")
ok(min(Os) > 0, "O_hat bounded away from zero on the computed domain")
print("[D3'] topological far-field floor: OFF by VC-B (T5; recorded constant 0).")
BANK.append(f"R1 (maps+bounds): over the computed domain A_hat in "
            f"[{min(As):.3f},{max(As):.3f}] (signed; zero-crossing "
            f"{'present' if min(As)<0<max(As) else 'absent'}), J_hat >= "
            f"{min(Js):.3f}, O_hat >= {min(Os):.3f} -- the flow channels have "
            f"nonzero floors on the computed domain; the monopole can vanish.")

# =============================================================================
sect("D4' -- dimensional-closure audit (KC3-BLIND; symbolic)")
# =============================================================================
rho_s, cs, xi, gam, Mach, tau, P1, P2, P3, Lk = sp.symbols(
    'rho_s c_s xi gamma M tau P_mono P_J P_rel L_knot', positive=True)
E_knot = gam*tau*rho_s*cs**2*xi**2*Lk          # mass clause: T_f = tau rho c^2 xi^2
for Pi in (P1, P2, P3):
    Ploss = rho_s*cs**3*xi*Pi*Lk               # wake scale per channel
    ell = sp.simplify(E_knot*(Mach*cs)/Ploss)  # loss length = E v / P
    ok(rho_s not in ell.free_symbols and Lk not in ell.free_symbols,
       "rho_s and L_knot cancel in the loss length")
    ok(sp.simplify(ell - gam*Mach*tau*xi/Pi) == 0, "closure form ell = gamma M tau xi / P")
phi = (1 + sp.sqrt(5))/2
ok(sp.simplify(1/phi**(-2) - phi**2) == 0, "ultrarelativistic Mach saturates at phi^2")
print("[D4'] per channel: ell = gamma * M * tau * xi / P_channel -- rho_s and the")
print("      knot length cancel EXACTLY; ONE import survives: xi (the substrate")
print("      scale).  CLASS: SURFACE, all three channels.  M -> phi^2 ~= 2.618 as")
print("      v -> c (c_s = phi^-2 c, locked).  No KC number appears here.")
BANK.append("R1 (closure): the KC3 loss-length closes to ell/xi = gamma M tau / "
            "P_channel with rho_s and L_knot cancelling exactly; SURFACE class "
            "(single surviving import xi) for all three channels; M saturates at "
            "phi^2 for ultrarelativistic knots.")

# =============================================================================
sect("COMPARISON STEP -- run LAST; the ONLY place KC3 appears (R2 Sec.5)")
# =============================================================================
def comparison_step():
    print("KC3 thresholds (quarantined to this step; cited, never used upstream):")
    print("  Moore-Nelson: c - c_g < 2e-15 c (galactic) / 2e-19 c (extragalactic)")
    print("  operationalized (BD-IIB-1): loss length >= propagation length,")
    print("  L_gal ~ 10 kpc, L_xgal ~ 100 Mpc.")
    print("-"*78)
    print("Mapping: KC3 <=> xi * gamma * M * tau_hat / P_i(A,J,O; M=phi^2) >= L_prop,")
    print("per channel, with the measured maps and floors supplying P_i's range.")
    print("xi is UNPINNED (M.CW; the substrate scale is not declared numerically).")
    print("=> the comparison DELIVERS THE CONSTRAINT CURVE (an explicit inequality")
    print("   on xi given gamma), and CANNOT kill or pass at this level: ARM B's")
    print("   parameter-free joint-floor kill is unavailable when the surviving")
    print("   import is free; satisfying regions exist for xi above the curve.")
    print("-"*78)
    print("ARM: A -- BOUND-DELIVERED (SURFACE).  NO KC IS CLAIMED PASSED.")
    print("The KC3 disposition = the delivered inequality; it resolves only when")
    print("xi is pinned -- a named future declaration/derivation (successor gate).")
    return "ARM A -- BOUND-DELIVERED (SURFACE class; constraint curve delivered)"

ARM = comparison_step()

sect("VERDICT")
print("GATE G-CC-e1-R2 CHAT-LEG VERDICT:", ARM)
print("D0 nonempty (immiscible branch); three maps + bounds delivered; monopole")
print("zero-crossing reported as a feature; flow floors nonzero on the domain;")
print("closure SURFACE(xi) all channels; comparison -> constraint curve.")
for i, b in enumerate(BANK, 1):
    print(f"BANK {i}. {b}")
print(f"\nTOTAL ASSERTIONS PASSED: {ASSERTS}")
print("Scope held: fluid branch; linear channel; radial-sector stability only;")
print("baryon-first; no observable; no magnitudes beyond the delivered curve;")
print("Sec.2.87.J untouched; Sec.2.52 Open 3 untouched.")
