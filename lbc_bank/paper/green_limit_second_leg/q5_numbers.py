#!/usr/bin/env python3
"""
Q5 numbers (3D isotropic), units mu = 1, rho = 1.
  rho_s = f_s, rho_n = 1 - f_s, alpha = 3.0e40 (rho^2 alpha = 3.0e40 mu),
  K = 5/3 (fixed-density bulk), M = K + 4 mu/3 = 3, c_T^2 = mu/rho_n.
Dispersion: X^2 - S X + P = 0, S = rho alpha - 2 gamma + M/rho_n, P = (rho_s/rho_n)(alpha M - gamma^2).
c-^2 evaluated cancellation-free as 2P/(S + sqrt(S^2 - 4P)); mpmath at 100 digits.
Independent check: numerical eigenvalues of the 4x4 Hamiltonian generator in mpmath.
"""
import mpmath as mp
mp.mp.dps = 100

mu, rho = mp.mpf(1), mp.mpf(1)
alpha = mp.mpf('3.0e40')
K = mp.mpf(5)/3
d = 3
M = K + 2*(d - 1)*mu/d          # = 3

def speeds(fs, gamma):
    rs, rn = fs*rho, (1 - fs)*rho
    S = rho*alpha - 2*gamma + M/rn
    P = rs/rn*(alpha*M - gamma**2)
    root = mp.sqrt(S**2 - 4*P)
    cp2 = (S + root)/2
    cm2 = 2*P/(S + root)
    cT2 = mu/rn
    return mp.sqrt(cm2/cT2), mp.sqrt(cp2/cT2)

def ham_speeds(fs, gamma, qv=1):
    rs, rn = fs*rho, (1 - fs)*rho
    j = mp.mpc(0, 1)
    A = mp.matrix([[0, -alpha, -j*qv*gamma, 0],
                   [rho*qv**2, 0, 0, -j*qv],
                   [j*qv, 0, 0, 1/rn],
                   [0, j*qv*gamma, -M*qv**2, 0]])
    ev = mp.eig(A, left=False, right=False)
    om = sorted(set(mp.nstr(abs(mp.re(j*e))/qv, 40) for e in ev), key=lambda s: mp.mpf(s))
    cT = mp.sqrt(mu/rn)
    return [mp.mpf(o)/cT for o in om]

def show(label, fs, gamma):
    cm, cp = speeds(fs, gamma)
    print(f"{label:46s} c-/cT = {mp.nstr(cm, 12):>16s}   c+/cT = {mp.nstr(cp, 12)}")
    return cm, cp

fs = mp.mpf(4)/5
print("f_s = 4/5, K/mu = 5/3, M/mu = 3, rho^2 alpha/mu = 3e40;  gamma in units mu/rho")
cm0, cp0 = show("(i)  gamma = 0", fs, 0)
gmarg = mp.sqrt(alpha*K)
print(f"     marginal |gamma| = sqrt(alpha K) = {mp.nstr(gmarg, 12)}")
for delta in ('1e-6', '1e-12', '1e-30', '0'):
    for sgn in (+1, -1):
        show(f"(ii) gamma = {'+' if sgn > 0 else '-'}sqrt(aK)(1-{delta})", fs, sgn*gmarg*(1 - mp.mpf(delta)))

print("\nGreen-limit closed forms at f_s = 4/5:")
print("  sqrt(f_s M/mu)        =", mp.nstr(mp.sqrt(fs*M/mu), 12), "  (gamma = 0 / fixed gamma)")
print("  sqrt(f_s (M-K)/mu)    =", mp.nstr(mp.sqrt(fs*(M - K)/mu), 12), "  (gamma^2 -> alpha K) = 4(b) bound sqrt(4 f_s/3)")
print("  sqrt(rho_n rho alpha/mu) =", mp.nstr(mp.sqrt((1 - fs)*rho*alpha/mu), 12), "  leading c+/cT")
print("  finite-alpha deviations:  (i) c-/cT - sqrt(f_s M/mu) =",
      mp.nstr(cm0 - mp.sqrt(fs*M/mu), 5))
cm_ii, _ = speeds(fs, gmarg)
print("                            (ii,+,delta=0) c-/cT - sqrt(4 f_s/3) =",
      mp.nstr(cm_ii - mp.sqrt(4*fs/3), 5))

print("\nHamiltonian-route cross-check (mpmath eig of 4x4 generator):")
for lab, gam in (("gamma=0", 0), ("gamma=+marg", gmarg*(1 - mp.mpf('1e-12')))):
    hs = ham_speeds(fs, gam)
    cm, cp = speeds(fs, gam)
    print(f"  {lab:12s} eig-> c/cT = {[mp.nstr(h, 12) for h in hs]}   rel.diff = "
          f"{mp.nstr(abs(hs[0]/cm - 1), 3)}, {mp.nstr(abs(hs[-1]/cp - 1), 3)}")

print("\ngamma = 0 at other f_s (same K, alpha); 4(b) bound sqrt(2(d-1) f_s/d) = sqrt(4 f_s/3):")
for f in ('0.49', '0.98'):
    fsv = mp.mpf(f)
    cm, cp = speeds(fsv, 0)
    print(f"  f_s = {f}: c-/cT = {mp.nstr(cm, 10)}  (c-^2/cT^2 = {mp.nstr(cm**2, 10)}),"
          f"  bound c-/cT > {mp.nstr(mp.sqrt(4*fsv/3), 10)}  (c-^2/cT^2 > {mp.nstr(4*fsv/3, 10)}),"
          f"  c+/cT = {mp.nstr(cp, 8)}")

# ---- floating-point pitfall: naive quadratic formula in double precision
import math
def naive(fs_, gamma_):
    rs, rn = fs_, 1 - fs_
    S = 3.0e40 - 2*gamma_ + 3.0/rn
    P = rs/rn*(3.0e40*3.0 - gamma_**2)
    disc = S*S - 4*P
    return (S - math.sqrt(disc))/2*rn, (2*P/(S + math.sqrt(disc)))*rn
print("\nfloat64, f_s=0.8, gamma=0: naive (S-sqrt(S^2-4P))/2 -> c-^2/cT^2 =", naive(0.8, 0.0)[0],
      "; stable 2P/(S+sqrt) ->", naive(0.8, 0.0)[1])
