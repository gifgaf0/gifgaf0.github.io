"""Independent GP solver probe for the G-CC-e1-R2 CC leg.

Method: imaginary-time SPLIT-STEP with an IMPLICIT Crank-Nicolson radial Laplacian
(tridiagonal solve) -- fundamentally different from the chat leg's explicit forward-Euler
normalized gradient flow. Own grid + own Simpson quadrature.

VC-B two-component GP, bath units hbar=m=g11=g22=1, n2_inf=1 (xi2=1, c_s=1, mu2=1):
  psi1 = f1(r) e^{i theta}  (annular winding w1=1; f1(0)=f1(inf)=0, norm N1 fixed)
  psi2 = f2(r)              (bath; f2'(0)=0, f2(inf)=1)
  GP:  mu1 f1 = -1/2 (f1'' + f1'/r - f1/r^2) + (f1^2 + eta f2^2) f1
        1  f2 = -1/2 (f2'' + f2'/r)          + (f2^2 + eta f1^2) f2
"""
import numpy as np
from scipy.linalg import solve_banded

# ---- own grid (different discretization from the chat's NR=640,DR=0.075) ----
NR, H = 800, 0.06
r = (np.arange(NR) + 0.5) * H            # CELL-CENTERED grid (chat: node-centered) -> avoids r=0
Rmax = r[-1]
def simpson(fn):                         # own quadrature: 2*pi * Int fn*r dr, Simpson
    from scipy.integrate import simpson as _s
    return 2*np.pi*_s(fn*r, dx=H)

# ---- Crank-Nicolson tridiagonal operator for K = -1/2 (d2/dr2 + 1/r d/dr - w^2/r^2) ----
def kinetic_bands(w):
    """Raw K bands (lo,di,up): K f = -1/2 (f'' + f'/r - w^2/r^2 f)."""
    lo = -0.5*(1.0/H**2 - 1.0/(2*H*r))                 # coeff of f_{i-1}
    di = -0.5*(-2.0/H**2 - w**2/r**2)                  # coeff of f_i
    up = -0.5*(1.0/H**2 + 1.0/(2*H*r))                 # coeff of f_{i+1}
    return lo, di, up
def apply_K(lo, di, up, f):
    out = di*f
    out[1:]  += lo[1:]*f[:-1]
    out[:-1] += up[:-1]*f[1:]
    return out
def imp_band(lo, di, up, dt, bc0, bcN):
    """Banded (I + dt/2 K) with boundary rows overwritten."""
    B = np.zeros((3, NR))
    B[0,1:] = dt/2*up[:-1]; B[1,:] = 1.0 + dt/2*di; B[2,:-1] = dt/2*lo[1:]
    if bc0 == 'D0': B[1,0]=1.0; B[0,1]=0.0
    elif bc0 == 'N0': B[1,0]=1.0; B[0,1]=-1.0
    if bcN == 'D0': B[1,-1]=1.0; B[2,-2]=0.0
    elif bcN == 'D1': B[1,-1]=1.0; B[2,-2]=0.0
    return B

def solve_component(f, bands, imp, dt, Vhalf, bc0, bcN, bcNval=0.0):
    """One split-step (Strang): potential half, CN diffusion, potential half."""
    lo, di, up = bands
    f = f*np.exp(-0.5*dt*Vhalf)                        # explicit nonlinear half
    rhs = f - 0.5*dt*apply_K(lo, di, up, f)            # (I - dt/2 K) f   [FIXED]
    if bc0 in ('D0','N0'): rhs[0] = 0.0
    if bcN == 'D0': rhs[-1] = 0.0
    elif bcN == 'D1': rhs[-1] = bcNval                 # = 1
    f = solve_banded((1,1), imp, rhs)
    f = f*np.exp(-0.5*dt*Vhalf)
    return f

def relax(eta, N1, R0=1.4, dt=0.02, steps=20000, tol=1e-9):
    # precompute kinetic bands + implicit matrices (dt fixed)
    b1 = kinetic_bands(1); imp1 = imp_band(*b1, dt, 'D0', 'D0')
    b2 = kinetic_bands(0); imp2 = imp_band(*b2, dt, 'N0', 'D1')
    # seed: annular winding tube of radius R0, bath complementary
    f1 = np.exp(-((r-R0)/1.0)**2) * (r/(r+0.5))
    f1[0]=0.0; f1[-1]=0.0
    f1 *= np.sqrt(N1/max(simpson(f1**2), 1e-30))
    f2 = np.sqrt(np.clip(1.0 - 0.9*f1**2, 0.02, None)); f2[-1]=1.0
    last=None
    for s in range(steps):
        V1 = f1**2 + eta*f2**2                          # mu1 via renormalization
        f1 = solve_component(f1, b1, imp1, dt, V1, 'D0', 'D0')
        f1 *= np.sqrt(N1/max(simpson(f1**2), 1e-30))    # enforce N1
        V2 = f2**2 + eta*f1**2 - 1.0                     # mu2=1 built in
        f2 = solve_component(f2, b2, imp2, dt, V2, 'N0', 'D1', bcNval=1.0)
        if s % 2000 == 1999:
            cur = simpson((1-f1**2-f2**2))
            if last is not None and abs(cur-last) < tol*max(1,abs(cur)):
                break
            last = cur
    # mu1 from the GP functional
    def lap_w1(f):
        o=np.zeros_like(f)
        o[1:-1]=(f[2:]-2*f[1:-1]+f[:-2])/H**2 + (f[2:]-f[:-2])/(2*H*r[1:-1]) - f[1:-1]/r[1:-1]**2
        return o
    mu1 = simpson(f1*(-0.5*lap_w1(f1) + (f1**2+eta*f2**2)*f1))/N1
    tail = simpson(np.where(r>0.8*Rmax, f1**2, 0.0))/N1
    Rtube = float(r[np.argmax(f1**2)])
    localized = tail < 1e-6
    return dict(f1=f1, f2=f2, mu1=mu1, tail=tail, Rtube=Rtube, localized=localized)

if __name__ == "__main__":
    # test at (eta=3, N1=10): chat checkpoint mu1=1.6234 Rtube=1.35; report Ahat=13.73 Jhat=4.43 Ohat=1.20 That=7.49
    sol = relax(3.0, 10.0)
    f1,f2 = sol['f1'], sol['f2']
    n1,n2 = f1**2, f2**2; ntot=n1+n2
    u2 = 1.0/r**2
    Ahat = simpson(1-ntot)
    Jhat = simpson(n1**2*u2/ntot)
    Ohat = simpson(n1*n2*u2/ntot)
    KE   = simpson(n1*u2)
    print(f"[CC solver @ eta=3,N1=10] localized={sol['localized']} tail={sol['tail']:.2e} "
          f"mu1={sol['mu1']:.4f} Rtube={sol['Rtube']:.2f}")
    print(f"  Ahat={Ahat:.3f} Jhat={Jhat:.3f} Ohat={Ohat:.3f}  (chat: 13.73/4.43/1.20)")
    print(f"  T2 trace identity J+O-KE max pointwise = {np.max(np.abs(Jhat+Ohat-KE)):.2e}")
    print(f"  (integrated) J+O={Jhat+Ohat:.4f}  KE={KE:.4f}  diff={abs(Jhat+Ohat-KE):.2e}")
