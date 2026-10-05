# Longitudinal branch coupling — expectation, written BEFORE any spectral-weight computation
(exploration mode; base V4.88; substrate units; date 2026-10-03)

Question: which longitudinal branch does a localized density source couple to at linear order
on the MV-G1 p6m supersolid (g=22 soft-core): first sound c_L1 = 11.045 or second sound c_2 = 1.765?

Expectation: BOTH, generically. The second-sound (lower longitudinal) density weight is NOT
symmetry-forbidden. Reasoning (T=0 supersolid hydrodynamics, Son/Yoo-Dorsey Lagrangian
L = -rho(dtheta/dt + (grad theta)^2/2) + (rho_n/2)(du/dt - grad theta)^2 - e(rho, u_ij)):
  chi(q,w) = q^2 (rho_n rho w^2 - rho_s M q^2) / [rho_n w^4 - (M + rho_n rho a - 2 rho_n g) q^2 w^2 + rho_s (a M - g^2) q^4]
  with a = d2e/drho2, M = uniaxial modulus at fixed rho, g = d2e/drho du.
  f-sum share of the lower branch:  F_- = (c_*^2 - c_-^2)/(c_+^2 - c_-^2),  c_*^2 = rho_s M/(rho_n rho).
  => F_- = 0 only if c_-^2 = rho_s M/(rho_n rho): a tuning condition, not a symmetry.
  Only the transverse branch has symmetry-forced zero density weight (on the symmetry lines).
Numbers I expect (rough, g=22, strongly modulated psi6=0.97 so f_s well below 1):
  F_- ~ 0.1-0.3 of the f-sum;  spectral weight ratio Z_-/Z_+ = (F_-/F_+)(c_+/c_-) ~ O(1);
  static (w=0) response dominated by the lower branch (share ~ F/c^2).
Consequence if confirmed: a knot with direct density coupling radiates into the c_2 branch
for v > c_2 ~ 0.31 c (ANNEX-CDEF-1 units) -> KC3 applies to the direct-coupling class.
Falsifier of the expectation: Z_-(q)/q -> 0 as q -> 0 at the canonical point AND across g,
or Z_- below ~1e-3 of Z_+ with no trend.
