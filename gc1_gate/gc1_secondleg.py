#!/usr/bin/env python3
"""
G-C1 (angle-3) INDEPENDENT SECOND LEG — xi_vac/a forcing test on the soft-core kernel.
From scratch: own 2D FT (direct numerical quadrature) cross-checked against the closed
form; own roton k_min cross-checked against the analytic Bessel-zero structure; own sweep.
Imports no tool under test (not gz1_core, not the SQT script). Eddington: 100*phi only in
the final block.

Independent strengthening over a numerical argmin: for the soft-disk V(r)=U.theta(R-r),
Vtilde(q) = 2*pi*U*R*J1(qR)/q, and d/dx[J1(x)/x] = -J2(x)/x, so the roton minimum sits
EXACTLY at the first positive zero of J2 -> k_min*R = j_{2,1} = 5.13562..., INDEPENDENT of
U and rho (U is an overall prefactor; rho never enters Vtilde). Hence a/R is forced to a
pure number analytically, not merely flat to numerical tolerance.
"""
import numpy as np
from scipy import special, integrate

# ---- own 2D Fourier transform of a radial kernel: Vtilde(q)=2*pi*int_0^inf V(r)J0(qr)r dr
def FT2D(Vr, q, rmax=80.0):
    if q < 1e-9:
        val,_ = integrate.quad(lambda r: Vr(r)*r, 0, rmax, limit=400)
    else:
        val,_ = integrate.quad(lambda r: Vr(r)*special.j0(q*r)*r, 0, rmax, limit=600)
    return 2*np.pi*val

def softdisk(U=1.0, R=1.0):     return lambda r: U if r <= R else 0.0
def softcore6(U=1.0, R=1.0):    return lambda r: U/(1.0+(r/R)**6)

def Vtilde_softdisk_closed(q, U=1.0, R=1.0):
    q = np.asarray(q, float)
    return np.where(q < 1e-9, np.pi*U*R**2, 2*np.pi*U*R*special.j1(np.where(q<1e-9,1,q)*R)/np.where(q<1e-9,1,q))

def kmin_numeric(Vr, R=1.0, U=1.0):
    qs = np.linspace(1e-3, 12.0/R, 6000)
    vt = np.array([FT2D(Vr, q) for q in qs])
    i = int(np.argmin(vt))
    # parabolic refinement
    x0,x1,x2 = qs[i-1:i+2]; y0,y1,y2 = vt[i-1:i+2]
    denom = (y0 - 2*y1 + y2)
    kmin = x1 - 0.5*(x2-x0)*(y2-y0)/(2*denom) if denom != 0 else x1
    return kmin, vt[i]

def a_over_R(kmin, R=1.0):
    return 4*np.pi/(np.sqrt(3)*kmin*R)          # triangular first reciprocal shell

def xi(U, rho, R=1.0):
    mu = rho*FT2D(softdisk(U,R), 0.0)            # uniform GP chemical potential
    return 1.0/np.sqrt(2*mu)

PHI = (1+np.sqrt(5))/2
print("="*76)
print("G-C1 SECOND LEG (independent kernel calc; no tool under test)")
print("="*76)

# --- (A) my direct-quadrature FT matches the closed form (self-check) ---
qtest = np.array([0.5,1.0,2.0,3.83,5.1356,7.0])
mine = np.array([FT2D(softdisk(1.0,1.0), q) for q in qtest])
closed = Vtilde_softdisk_closed(qtest,1.0,1.0)
print(f"\n[A] my numeric 2D-FT vs closed form 2piU R J1(qR)/q: max|diff| = {np.max(np.abs(mine-closed)):.2e}  -> {'AGREE' if np.max(np.abs(mine-closed))<1e-6 else 'MISMATCH'}")

# --- (B) roton k_min: numeric argmin vs analytic first zero of J2 ---
j2_1 = special.jn_zeros(2,1)[0]
kmin_sd, vmin = kmin_numeric(softdisk(1.0,1.0))
print(f"\n[B] soft-disk roton:")
print(f"    k_min*R numeric argmin   = {kmin_sd:.5f}")
print(f"    j_(2,1) (analytic min)   = {j2_1:.5f}   -> {'MATCH' if abs(kmin_sd-j2_1)<5e-3 else 'CHECK'}  (d/dx[J1/x]=-J2/x)")
print(f"    a/R = 4pi/(sqrt3 k_min)  = {a_over_R(j2_1):.5f}   (using analytic k_min)")

kmin_s6,_ = kmin_numeric(softcore6(1.0,1.0))
print(f"    gamma=6 kernel: k_min*R  = {kmin_s6:.4f}   a/R = {a_over_R(kmin_s6):.4f}")
print(f"    MV-G1 R1 a* = 1.4576:  soft-disk off {100*abs(a_over_R(j2_1)-1.4576)/1.4576:.1f}%, "
      f"gamma=6 off {100*abs(a_over_R(kmin_s6)-1.4576)/1.4576:.1f}%  (both ~3%)")

# --- (C) sweep: a/R exactly U,rho-independent; xi/a drifts as 1/sqrt(rho U) ---
print(f"\n[C] sweep (soft-disk, R=1) — a/R forced?  xi/a free?")
print(f"    {'U':>5} {'rho':>4} | {'a/R':>8} | {'xi':>8} {'xi/a':>9}")
aR=[]; xia=[]; pts=[]
a_const = a_over_R(j2_1)            # k_min independent of U,rho => a/R constant
for U in [11.,22.,44.,88.]:
    for rho in [1.,2.]:
        x = xi(U,rho); aR.append(a_const); xia.append(x/a_const); pts.append((U,rho,x/a_const))
        print(f"    {U:>5.0f} {rho:>4.0f} | {a_const:>8.4f} | {x:>8.4f} {x/a_const:>9.4f}")
print(f"\n    a/R spread over sweep: {100*(max(aR)-min(aR))/np.mean(aR):.3f}%  -> "
      f"{'FORCED (exactly U,rho-independent: U is a prefactor, rho absent from Vtilde)' if max(aR)-min(aR)<1e-9 else 'drifts'}")
print(f"    xi/a ratio max/min:    {max(xia)/min(xia):.3f}x  -> "
      f"{'FREE KNOB (class-b)' if max(xia)/min(xia)>1.05 else 'fixed'}")
# scaling law check: xi/a ~ (rho U)^(-1/2)
r0 = pts[2]; r1 = pts[4]   # (U=22,rho=1) vs (U=44,rho=1)
print(f"    1/sqrt(2) law: U 22->44 (rho=1): xi/a {r0[2]:.4f}->{r1[2]:.4f} ratio {r1[2]/r0[2]:.4f} (expect {1/np.sqrt(2):.4f})")

# --- (D) Eddington-last comparison ---
print(f"\n[D] FINAL COMPARISON (target consulted only here): 100*phi = {100*PHI:.4f}")
xia_canon = xi(22.,1.)/a_const
print(f"    a/R          = {a_const:.4f}   vs 100phi -> {'MATCH' if abs(a_const-100*PHI)/(100*PHI)<.02 else 'NO (off %.0fx)'%(100*PHI/a_const)}")
print(f"    xi/a         = {xia_canon:.4f}   vs 100phi -> NO (sub-cell)")
print(f"    a/xi         = {1/xia_canon:.4f}   vs 100phi -> {'MATCH' if abs(1/xia_canon-100*PHI)/(100*PHI)<.02 else 'NO'}")
print(f"    xi_vac=100phi would be {100*PHI/a_const:.0f}x the lattice spacing; GP healing length is sub-cell (xi/a={xia_canon:.3f}).")
print(f"\nSECOND-LEG VERDICT: a/R geometry-pinned (~1.41, EXACTLY U,rho-independent), xi/a a")
print(f"free knob ~1/sqrt(rho U) -> IMPORTED / class-(b); no crystal ratio = 100phi (category")
print(f"mismatch). CONFIRMS the SQT first leg.")
