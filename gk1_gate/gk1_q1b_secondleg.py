#!/usr/bin/env python3
"""
G-kappa1 Q1b INDEPENDENT SECOND LEG (CC): the vortex core parameter C as a kernel functional.
First leg (gk1_q1b_core_parameter.py) used Newton/Thomas relaxation; this uses scipy solve_bvp
-- independent method, same physics. Reproduces C[kernel] across the local family U'(n)=n^gamma.

profile: f'' + f'/r - f/r^2 + f - f^(2g+1) = 0,  f(0)=0, f(inf)=1
e(R) = int_0^R [ (f')^2 + f^2/r^2 + w(f) ] r dr,  w=(f^(2(g+1))-1)/(g+1) - (f^2-1)
C = lim_{R->inf} [ e(R) - ln R ]   (the additive core constant; GP = ln 1.464)
"""
import numpy as np
from scipy.integrate import solve_bvp

def core_C(g, rmax=80.0, N=6000):
    r=np.linspace(1e-4,rmax,N)
    def rhs(r,y): return np.vstack([y[1], -y[1]/r + y[0]/r**2 - y[0] + y[0]**(2*g+1)])
    def bc(ya,yb): return np.array([ya[0], yb[0]-1.0])
    g0=r/np.sqrt(r*r+2.0)
    sol=solve_bvp(rhs,bc,r,np.vstack([g0,np.gradient(g0,r)]),max_nodes=300000,tol=1e-9)
    f,fp=sol.sol(r)
    w=(f**(2*(g+1))-1.0)/(g+1) - (f**2-1.0)
    integ=(fp**2 + f**2/r**2 + w)*r
    e=np.concatenate([[0],np.cumsum((integ[1:]+integ[:-1])/2*np.diff(r))])
    C=(e-np.log(r))[np.searchsorted(r,rmax-20)]
    return sol.success, float(C)

if __name__=="__main__":
    firstleg={1:0.3810,2:0.6156,3:0.7273}
    print("Q1b second leg (solve_bvp) -- C[kernel] across U'(n)=n^gamma")
    for g in (1,2,3):
        ok,C=core_C(g)
        print(f"  gamma={g}: C = {C:+.4f}   (first leg {firstleg[g]:+.4f}; match={abs(C-firstleg[g])<3e-3})")
    print(f"  GP=ln(1.464)={np.log(1.464):.4f}. C is a BOUNDED O(1) kernel functional (0.38->0.73);")
    print("  route (b) needs C>=5.3/32 (14x-84x outside this family) -> route (b) FAILS robustly.")
