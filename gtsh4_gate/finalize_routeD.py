"""G-TSH4 CC leg -- Route D disposition finalizer.

Records the certified part (BdG solver validated against the analytic uniform
Bogoliubov spectrum, the C-NEG dynamical control) and the honest non-certification
of the crystal transverse-branch measurement in THIS execution.  Writes
tsh4_routeD_measurements.json for the comparison stage (C4/C5)."""
import json
import numpy as np
import tsh4_core as C
import tsh4_routeD as D
import tsh4_selfgrep
tsh4_selfgrep.assert_clean(["tsh4_core.py", "tsh4_routeD.py", "finalize_routeD.py"])

def main():
    lc_s, _ = C.lambda_c(C.step_khat, 40.0); Lam_s = 2*lc_s
    gem = C.Gem8Khat(); lc_g, _ = C.lambda_c(gem, 25.0); Lam_g = 2*lc_g
    cneg = {}
    for kn, kh, Lam in [('step', C.step_khat, Lam_s), ('gem8', gem, Lam_g)]:
        rows = D.uniform_bdg_check(kh, Lam)
        cneg[kn] = dict(max_abs_err=max(r[3] for r in rows),
                        rows=[dict(q=r[0], omega2_num=r[1], omega2_analytic=r[2],
                                   abs_err=r[3]) for r in rows])
    out = {
      'gate': 'G-TSH4', 'route': 'D (dynamical BdG transverse branches)',
      'kernel_declared': 'step (A-1.3)',
      'status': 'NON-CERTIFIED (crystal transverse speeds deferred)',
      'solver_control_C_NEG_uniform_Bogoliubov': dict(
          formula='omega^2(k) = (k^2/2)(k^2/2 + 2 Lambda Uhat(k))',
          agreement='machine precision', detail=cneg),
      'why_not_certified': [
          'The plane-wave BdG operator omega^2 = L0^{1/2}(L0+2X)L0^{1/2} is exact '
          'in the uniform limit (agreement ~1e-14, both kernels), validating the '
          'Hartree+exchange assembly on the diagonal channel.',
          'For the crystal, using the full-grid ground state truncated to |G|<=gcut '
          'the amplitude Hessian (L0+2X) acquires spurious negative eigenvalues as '
          'gcut grows -- a ground-state/BdG basis inconsistency, not physics.',
          'Relaxing psi0 self-consistently INSIDE the cutoff removes the inconsistency '
          'in principle, but at the resolution needed to resolve psi0 (spectral weight '
          'beyond |G|=14 ~2e-3) the truncated imaginary-time relaxation did not reach '
          'a low enough in-subspace residual for a sign-definite (PSD) fluctuation '
          'operator at the compute available in this execution.',
          'Reporting negative/near-zero omega^2 as transverse speeds would be false; '
          'per A-1.6 the Route-S static-elastic speeds are reported as the elastic '
          'result and Route-D dynamical slopes are DEFERRED.'],
      'comparison_note': 'Surface at C4/C5 as gate-fragility (S9-lite eligible). '
          'The chat-leg Route-D (full E4 set on AB+FCC@step) is the authoritative '
          'dynamical leg per A-1.3; CC-leg Route-D is not adjudicated here.',
      'Q_B_statement': 'Not issued by the CC leg (Route-D non-certified).'}
    json.dump(out, open("tsh4_routeD_measurements.json", "w"), indent=1)
    for kn in cneg:
        print("C-NEG uniform Bogoliubov [%s]: max|err| = %.2e" % (kn, cneg[kn]['max_abs_err']))
    print("Route D status:", out['status'])
    print("WROTE tsh4_routeD_measurements.json")

if __name__ == "__main__":
    main()
