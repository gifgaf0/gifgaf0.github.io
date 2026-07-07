#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
G-k1 Q1b (chat-side first leg): the vortex core parameter as a kernel functional.

Line tension of a straight vortex:  T(R) = 2*pi*rho*(hbar^2/2m)*[ ln(R/xi) + C ]
The kernel enters ONLY through C (LSF Finding 1; Amit-Gross / Roberts-Grant).
This leg:
  (1) verifies the GP value from scratch:  C(GP) = 0.3809  (ln 1.464)
  (2) demonstrates C = C[kernel] with no residual freedom, across the local
      family  U'(n) = n^gamma  (gamma = 1 is GP; cf. the subcritical-NLS family
      in the LSF report where the same variation is used in print).
Nonlocal (roton) kernel evaluation: flagged for the second leg (Berloff-Roberts
method); NOT claimed here.

Vortex profile ODE (units: xi-analog = 1, rho_inf = 1, mu = 1):
    f'' + f'/r - f/r^2 + f - f^(2*gamma+1) = 0,   f(0)=0, f(inf)=1
Energy excess per unit length / (2*pi):
    e(R) = int_0^R [ (f')^2 + f^2/r^2 + w(f) ] r dr,
    w(f) = (f^(2(gamma+1)) - 1)/(gamma+1) - (f^2 - 1)   [ = (1-f^2)^2/2 at gamma=1 ]
    C = lim_{R->inf} [ e(R) - ln R ]
"""
import numpy as np

def solve_profile(gamma, Rmax=60.0, N=24000, iters=80):
    h = Rmax / N
    r = np.linspace(h, Rmax, N)
    f = r / np.sqrt(r*r + 2.0)                    # initial guess
    f[-1] = 1.0 - 1.0/(2*gamma*Rmax*Rmax)         # asymptotic BC
    def thomas(a, b, c, d):
        n = len(d); cp = np.zeros(n); dp = np.zeros(n)
        cp[0] = c[0]/b[0]; dp[0] = d[0]/b[0]
        for i in range(1, n):
            m = b[i] - a[i]*cp[i-1]
            cp[i] = c[i]/m
            dp[i] = (d[i] - a[i]*dp[i-1])/m
        x = np.zeros(n); x[-1] = dp[-1]
        for i in range(n-2, -1, -1):
            x[i] = dp[i] - cp[i]*x[i+1]
        return x
    for _ in range(iters):
        F = np.zeros(N); Ja = np.zeros(N); Jb = np.zeros(N); Jc = np.zeros(N)
        fm = np.empty(N); fp = np.empty(N)
        fm[0] = 0.0;        fm[1:] = f[:-1]        # f(0)=0
        fp[:-1] = f[1:];    fp[-1] = f[-1]
        # residual on interior nodes (last node held fixed by BC)
        F = (fp - 2*f + fm)/h**2 + (fp - fm)/(2*h*r) - f/r**2 + f - f**(2*gamma+1)
        Ja = 1.0/h**2 - 1.0/(2*h*r)                # d/df_{i-1}
        Jb = -2.0/h**2 - 1.0/r**2 + 1.0 - (2*gamma+1)*f**(2*gamma)
        Jc = 1.0/h**2 + 1.0/(2*h*r)                # d/df_{i+1}
        F[-1] = 0.0; Ja[-1] = 0.0; Jb[-1] = 1.0; Jc[-1] = 0.0
        df = thomas(Ja, Jb, Jc, -F)
        f = f + np.clip(df, -0.2, 0.2)
        f = np.clip(f, 0.0, 1.2)
        f[-1] = 1.0 - 1.0/(2*gamma*Rmax*Rmax)
    res = np.max(np.abs(F[:-1]))
    return r, f, h, res

def core_constant(gamma, Rmax=60.0):
    r, f, h, res = solve_profile(gamma, Rmax=Rmax)
    fp = np.gradient(f, h)
    w = (f**(2*(gamma+1)) - 1.0)/(gamma+1) - (f**2 - 1.0)
    integrand = (fp**2 + (f**2)/r**2 + w) * r
    e = np.cumsum(integrand)*h
    C_of_R = e - np.log(r)
    # small-r piece of f^2/r^2 is finite (f ~ a r); cumulative from h ok.
    # report at several R to show convergence
    idx = [np.searchsorted(r, x) for x in (20.0, 40.0, Rmax-1)]
    return C_of_R, r, idx, res

print("="*70)
print("G-k1 Q1b: core parameter C as a kernel functional (chat-side first leg)")
print("="*70)
for gamma in (1, 2, 3):
    C_of_R, r, idx, res = core_constant(gamma)
    vals = ", ".join(f"C(R={r[i]:.0f})={C_of_R[i]:+.4f}" for i in idx)
    print(f" kernel U'(n)=n^{gamma}:  {vals}   [ODE residual {res:.1e}]")
print()
print(" checks: gamma=1 is GP; literature value C_GP = 0.3809 (= ln 1.464,")
print("         Pitaevskii-Stringari / Roberts-Grant).")
print(" claim tested: C is fully determined by the kernel (no residual freedom)")
print(" -> if C(gamma) converges per kernel and differs across kernels, the")
print("    functional dependence is demonstrated; the SQT value C[K_roton]")
print("    is then an evaluation (Berloff-Roberts method), NOT a new import.")
