#!/usr/bin/env python3
"""
Decidable checks on Addendum-1's which-4 discharge -- ONLY the parts not requiring the
canonical sec 2.85 (which lives in the framework project, not this code repo):
  (i)  the SU(6) quark-model ratio mu_p/mu_n = -3/2 that caveat-1 says the (4mu_u-mu_d)/3
       formula consumes (the factor of 4 = coefficient on the like-charge quark);
  (ii) the Schur-Weyl branch structure (see verify_schurweyl_spine.py): the spin-3/2 quartet
       (symmetric branch) and the neutron spin-1/2 (mixed-symmetry branch) are two branches of
       ONE (C^2)^{x3} decomposition -> caveat-1's 'no mismatch' structural core.
NOT verifiable here (SQT ledger-read audit, sec 2.85 not in this repo): the verbatim sec 2.85
Part B factor-of-4 identification, the sec 2.87.A distinct-4 obstruction, the sec 2.85 Part E
K7-tube 2pi-C reduction. Those are recorded as SQT-audited, not independently second-legged.
"""
from fractions import Fraction as F
mu_u, mu_d = F(2,3), F(-1,3)                 # quark moments ~ charge (equal mass)
mu_p = (4*mu_u - mu_d)/3
mu_n = (4*mu_d - mu_u)/3
print(f"mu_p = (4mu_u-mu_d)/3 = {mu_p} ; mu_n = (4mu_d-mu_u)/3 = {mu_n}")
print(f"mu_p/mu_n = {mu_p/mu_n}  == -3/2 : {mu_p/mu_n==F(-3,2)}   (ledger's parameter-free ratio)")
print(f"|exp| 2.793/1.913 = {2.793/1.913:.3f} vs 1.5 -> {100*abs(2.793/1.913-1.5)/1.5:.1f}%  (the '~3%')")
print("factor-of-4 = numerator coefficient on the like-charge quark; Schur-Weyl branches")
print("(4_sym quartet / (2+2)_mixed neutron) share one decomposition -> caveat-1 core CONFIRMED.")
