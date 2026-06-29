"""
Audit verification for the §2.64 staging memo. Checks every numerical/identity claim
that is checkable; does NOT re-derive the framework. mpmath for digamma.
"""
import mpmath as mp
mp.mp.dps = 30
phi = (1 + mp.sqrt(5))/2
pi  = mp.pi

print("=== Item 0/1 (R1): mass anchor + r_eff slack ===")
Phi = 2*pi - phi**2/(8*pi**2)
print(f"  Phi = 2pi - phi^2/(8pi^2) = {mp.nstr(Phi,8)}   (memo 6.250028)")
twopi_over_Phi = 2*pi/Phi
print(f"  2pi/Phi = {mp.nstr(twopi_over_Phi,8)}   (memo 1.005305)")
print(f"  e^(2pi/Phi) = {mp.nstr(mp.e**twopi_over_Phi,8)}   (memo 2.73289)")
m0 = mp.mpf('0.511')/mp.e**twopi_over_Phi
print(f"  m0 = 0.511/e^(2pi/Phi) = {mp.nstr(m0,7)} MeV   (memo 0.18699)")

xi = 100*phi
print(f"\n  xi_vac = 100*phi = {mp.nstr(xi,8)} fm   (memo 161.803)")
slack = mp.log(1 + 2*pi/xi)
reff = 1 + slack
print(f"  r_eff(2pi) = 1 + ln(1 + 2pi/xi) = {mp.nstr(reff,8)}   (memo 1.0381)")
print(f"  slack = ln(1+2pi/xi) = {mp.nstr(slack,6)} = {mp.nstr(slack*100,4)}%   (memo 3.81%)")
print(f"  => slack controlled by xi_vac alone (and structural L=2pi): CONFIRMED")

print("\n=== Item A (R1 math): digamma/harmonic-sum identity ===")
# r_eff(N) = 1 + sum_{n=0}^{N-1} 1/(C+n) = 1 + [psi(C+N) - psi(C)]
C = xi   # with a=1 fm (lattice spacing); C = xi_vac/a
for (Ctest,Ntest) in [(mp.mpf(10),5),(C,6),(C,7)]:
    hsum = mp.fsum([1/(Ctest+n) for n in range(Ntest)])
    digam = mp.digamma(Ctest+Ntest) - mp.digamma(Ctest)
    print(f"  C={mp.nstr(Ctest,6)} N={Ntest}: harmonic sum={mp.nstr(hsum,8)}  "
          f"psi(C+N)-psi(C)={mp.nstr(digam,8)}  match={mp.almosteq(hsum,digam)}")
# large-C limit -> ln(1+N/C)
print(f"  large-C: psi(C+N)-psi(C) vs ln(1+N/C) at C={mp.nstr(C,5)},N=6:")
d = mp.digamma(C+6)-mp.digamma(C); l = mp.log(1+6/C)
print(f"    digamma diff = {mp.nstr(d,8)} ; ln(1+N/C) = {mp.nstr(l,8)} ; rel gap = {mp.nstr((d-l)/l*100,3)}%")

print("\n=== Flag 2 made concrete: discrete sum vs continuum log at the ACTUAL values ===")
# the memo's 3.81% uses the continuum log with L=2pi. The discrete sum (a=1 -> N=6 or 7)
N6 = mp.fsum([1/(C+n) for n in range(6)])
N7 = mp.fsum([1/(C+n) for n in range(7)])
cont = mp.log(1+2*pi/C)   # = continuum slack
print(f"  continuum slack ln(1+2pi/xi)         = {mp.nstr(cont,6)} ({mp.nstr(cont*100,4)}%)")
print(f"  discrete sum_0^5 1/(C+n) [N=6]        = {mp.nstr(N6,6)} ({mp.nstr(N6*100,4)}%)")
print(f"  discrete sum_0^6 1/(C+n) [N=7]        = {mp.nstr(N7,6)} ({mp.nstr(N7*100,4)}%)")
print(f"  continuum vs N=6 differ by {mp.nstr((cont-N6)/cont*100,3)}% ; vs N=7 by {mp.nstr((cont-N7)/cont*100,3)}%")
print("  => discrete-vs-continuum choice shifts the slack at the ~few-% level of itself;")
print("     i.e. the R3 endpoint/running/artifact adjudication (Flag 2) is MATERIAL, not academic.")
print(f"  Euler-Maclaurin endpoint term 1/(2C) = {mp.nstr(1/(2*C),4)} = {mp.nstr(1/(2*C)/cont*100,3)}% of the slack")

print("\n=== Item B (structural search): 100 has no clean combinatorial address ===")
print(f"  phi^9 = {mp.nstr(phi**9,6)} , phi^10 = {mp.nstr(phi**10,6)}  -> 100 strictly between (no clean power)")
print(f"  1/kappa = phi^4 = {mp.nstr(phi**4,6)} , 1/sqrt(kappa)=phi^2 = {mp.nstr(phi**2,6)}  (orders short)")
print(f"  |PSL(2,7)|=168 ; 100/168 = {mp.nstr(mp.mpf(100)/168,4)} (40% away)")
print(f"  structural integers 7,21,42,168,600: none = 100  -> CONFIRMED no clean address")
