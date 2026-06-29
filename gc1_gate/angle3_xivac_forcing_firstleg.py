#!/usr/bin/env python3
"""
G-C1 (angle-3): the xi_vac/a forcing test  (§2.64 inverse problem)
Self-contained roton/Bogoliubov linear-stability calc on the soft-core kernel.
Tests: is C = xi_vac/a forced to a pure number by triangular geometry, or a free knob
set by the roton kernel (interaction strength U, density rho)?
Eddington discipline: the target 100*phi appears ONLY in the final comparison block,
after every crystallization quantity is computed and frozen.  Imports no tool under test.
"""
import numpy as np
from scipy import special, integrate

# ---------------------------------------------------------------------------
# soft-core kernels V(r), dimensionless units: length = R, energy = hbar^2/(m R^2),
# hbar = m = 1.  Two kernel shapes bracket the framework's MV-G1 soft-core.
# ---------------------------------------------------------------------------
def Vtilde_softdisk(q, U=1.0, R=1.0):
    # V(r) = U for r<=R else 0 ; 2D FT = 2*pi*U * R*J1(qR)/q  (closed form)
    q = np.atleast_1d(np.asarray(q, float))
    out = np.empty_like(q)
    small = q < 1e-9
    out[small] = np.pi * U * R**2                      # Vtilde(0) = U*pi*R^2
    qq = q[~small]
    out[~small] = 2*np.pi*U*R*special.j1(qq*R)/qq
    return out if out.size > 1 else out[0]

def Vtilde_softcore6(q, U=1.0, R=1.0):
    # V(r) = U/(1+(r/R)^6) ; 2D FT = 2*pi * int_0^inf V(r) J0(qr) r dr  (numeric)
    def ft(qi):
        if qi < 1e-9:
            f = lambda r: U/(1+(r/R)**6) * r
            val,_ = integrate.quad(f, 0, 60*R, limit=200)
            return 2*np.pi*val
        f = lambda r: U/(1+(r/R)**6) * special.j0(qi*r) * r
        val,_ = integrate.quad(f, 0, 60*R, limit=400)
        return 2*np.pi*val
    q = np.atleast_1d(np.asarray(q, float))
    res = np.array([ft(qi) for qi in q])
    return res if res.size > 1 else res[0]

def roton_kmin(Vt, U=1.0, R=1.0):
    """k_min = argmin Vtilde(q) over the first negative lobe (the roton wavevector)."""
    qs = np.linspace(1e-3, 12.0/R, 4000)
    vt = Vt(qs, U, R)
    i = np.argmin(vt)
    # parabolic refine
    if 0 < i < len(qs)-1:
        x0,x1,x2 = qs[i-1],qs[i],qs[i+1]; y0,y1,y2 = vt[i-1],vt[i],vt[i+1]
        denom = (y0-2*y1+y2)
        kmin = x1 - 0.5*(x2-x0)*(y2-y0)/(4*(y1-0.5*(y0+y2))) if denom!=0 else x1
        kmin = x1 + 0.5*( (x1-x0)*(y2-y1)-(x2-x1)*(y0-y1) ) / ( (y2-y1)+(y0-y1) ) if abs((y2-y1)+(y0-y1))>1e-12 else x1
    else:
        kmin = qs[i]
    return kmin, vt[i]

def lattice_const(kmin):
    # triangular lattice: smallest reciprocal vector |G1| = 4*pi/(sqrt(3)*a) = kmin
    return 4*np.pi/(np.sqrt(3)*kmin)

def healing_length(Vt, U=1.0, R=1.0, rho=1.0):
    # GP healing length, uniform mean-field: mu = rho*Vtilde(0); xi = 1/sqrt(2*mu)
    mu = rho*Vt(0.0, U, R)
    return 1.0/np.sqrt(2*mu), mu

PHI = (1+np.sqrt(5))/2

print("="*78)
print("G-C1 (angle-3): xi_vac/a forcing test — roton linear-stability on soft-core kernel")
print("="*78)

for name, Vt in [("soft-disk (gamma->inf)", Vtilde_softdisk),
                 ("soft-core gamma=6     ", Vtilde_softcore6)]:
    kmin, vmin = roton_kmin(Vt, U=22.0, R=1.0)
    print(f"\n[{name}]  k_min*R = {kmin:.4f}   (Vtilde_min/U-shape located)")
    a = lattice_const(kmin)
    print(f"   a/R (triangular, a = 4pi/(sqrt3 k_min)) = {a:.4f}")

print("\n--- a/R is a pure number set by the KERNEL SHAPE (k_min*R), independent of U, rho ---")
print("    compare MV-G1 R1 value a* = 1.4576 (at R=1):")
kmin_sd,_ = roton_kmin(Vtilde_softdisk, 22.0, 1.0)
kmin_s6,_ = roton_kmin(Vtilde_softcore6, 22.0, 1.0)
print(f"      soft-disk  a/R = {lattice_const(kmin_sd):.4f}   (Δ vs 1.4576: {100*abs(lattice_const(kmin_sd)-1.4576)/1.4576:.1f}%)")
print(f"      gamma=6    a/R = {lattice_const(kmin_s6):.4f}   (Δ vs 1.4576: {100*abs(lattice_const(kmin_s6)-1.4576)/1.4576:.1f}%)")

# ---------------------------------------------------------------------------
# TEST 1: does a/R drift when we vary U, rho at fixed R?  (expect NO — geometry-pinned)
# TEST 2: does xi/a drift when we vary U, rho at fixed R? (expect YES — free knob)
# ---------------------------------------------------------------------------
print("\n" + "="*78)
print("PARAMETER SWEEP (soft-disk; fixed R=1) — a/R fixed?  xi/a fixed or drifting?")
print("="*78)
print(f"{'U':>6} {'rho':>5} | {'k_min*R':>8} {'a/R':>8} | {'xi':>8} {'xi/a':>9}")
rows=[]
for U in [11.0, 22.0, 44.0, 88.0]:
    for rho in [1.0, 2.0]:
        kmin,_ = roton_kmin(Vtilde_softdisk, U, 1.0)
        a = lattice_const(kmin)
        xi, mu = healing_length(Vtilde_softdisk, U, 1.0, rho)
        rows.append((U,rho,kmin,a,xi,xi/a))
        print(f"{U:>6.0f} {rho:>5.0f} | {kmin:>8.4f} {a:>8.4f} | {xi:>8.4f} {xi/a:>9.4f}")

aR = [r[3] for r in rows]
xia = [r[5] for r in rows]
print(f"\n  a/R   range over sweep: [{min(aR):.4f}, {max(aR):.4f}]   spread {100*(max(aR)-min(aR))/np.mean(aR):.2f}%  -> {'FIXED (geometry-pinned)' if (max(aR)-min(aR))/np.mean(aR)<0.01 else 'drifts'}")
print(f"  xi/a  range over sweep: [{min(xia):.4f}, {max(xia):.4f}]   ratio max/min {max(xia)/min(xia):.2f}x  -> {'FIXED' if max(xia)/min(xia)<1.05 else 'DRIFTS (free knob -> class-b)'}")
print(f"  xi/a scaling check: doubling U at fixed rho multiplies xi/a by ~1/sqrt(2)={1/np.sqrt(2):.4f}")
print(f"     U=22->44 (rho=1): xi/a {rows[2][5]:.4f} -> {rows[4][5]:.4f}  ratio {rows[4][5]/rows[2][5]:.4f}")

# ---------------------------------------------------------------------------
# EDDINGTON-LAST: only now consult the target.  Is any crystallization ratio = 100*phi?
# ---------------------------------------------------------------------------
print("\n" + "="*78)
print("FINAL COMPARISON (target consulted only here): xi_vac = 100*phi = %.4f" % (100*PHI))
print("="*78)
a_canon = lattice_const(kmin_sd)
xi_canon, _ = healing_length(Vtilde_softdisk, 22.0, 1.0, 1.0)
xia_canon = xi_canon/a_canon
print(f"  geometry-pinned a/R          = {a_canon:.4f}   vs 100phi={100*PHI:.3f}  -> {'MATCH' if abs(a_canon-100*PHI)/(100*PHI)<0.02 else 'NO (off by %.0fx)'%(100*PHI/a_canon)}")
print(f"  xi/a (canonical)             = {xia_canon:.4f}   vs 100phi={100*PHI:.3f}  -> {'MATCH' if abs(xia_canon-100*PHI)/(100*PHI)<0.02 else 'NO'}")
print(f"  1/(xi/a) (canonical)         = {1/xia_canon:.4f}   vs 100phi={100*PHI:.3f}  -> {'MATCH' if abs(1/xia_canon-100*PHI)/(100*PHI)<0.02 else 'NO'}")
print(f"  a/xi (canonical)             = {1/xia_canon:.4f}")
print(f"\n  Scale check: xi_vac=100phi=161.8 in 'lattice cells' vs GP healing length xi={xi_canon:.3f} cells")
print(f"     -> GP healing length is SUB-CELL (xi/a={xia_canon:.3f}); xi_vac would be {100*PHI/a_canon:.0f}x the lattice spacing")
print(f"     -> xi_vac (a macroscopic ~{100*PHI:.0f}-cell scale) is NOT the GP-crystal healing length (sub-cell). Identification category-mismatched.")
print("\nVERDICT INPUTS (for the pre-registered arms):")
print("  (1) a/R geometry-pinned to a pure number (~1.4) independent of U,rho  -> spacing IS forced by k_min")
print("  (2) xi/a DRIFTS with U,rho at fixed R (~1/sqrt(U rho))                -> C=xi/a is a FREE KNOB (class-b)")
print("  (3) no crystallization ratio equals 100phi; xi_vac is a macroscopic scale the local crystal does not set")
print("  => IMPORTED / class-(b), with the DEGENERATE-identification caveat. 'FORCED-MATCH' breach does NOT fire.")
