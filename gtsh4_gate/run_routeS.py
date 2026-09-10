"""G-TSH4 CC leg -- Route S runner. Elastic curvatures on AB and FCC, both kernels.
Reads optimised lattice params from tsh4_phase0_measurements.json.
Writes tsh4_routeS_measurements.json."""
import json, time
import numpy as np
import tsh4_core as C
import tsh4_routeS as R
import tsh4_selfgrep
tsh4_selfgrep.assert_clean(["tsh4_core.py", "tsh4_routeS.py", "run_routeS.py"])

PPL = 26
HEX_MODES = ['xz', 'xy', 'dev', 'bi', 'zz', 'iso']
CUB_MODES = ['xz', 'dev', 'iso']

def kernels():
    lc_s, ks = C.lambda_c(C.step_khat, 40.0)
    gem = C.Gem8Khat(); lc_g, kg = C.lambda_c(gem, 25.0)
    return {'step': (C.step_khat, 2*lc_s), 'gem8': (gem, 2*lc_g)}

def main():
    ph = json.load(open("tsh4_phase0_measurements.json"))
    K = kernels()
    out = {'gate': 'G-TSH4', 'route': 'S (static-elastic curvatures)',
           'declared': dict(e0=0.02, npts=7, ppl=PPL,
                            convention='H->(I+eps)H0, <n>=1, Lambda fixed, psi re-relaxed'),
           'results': {}}
    for kname in ['step', 'gem8']:
        khat, Lam = K[kname]
        ab = ph['results'][kname]['structures']['AB']['params']
        fcc = ph['results'][kname]['structures']['FCC']['params']
        H_ab = R.H0_hex(ab[0], ab[1])
        H_fcc = R.H0_cubic(fcc[0])
        kout = {'AB': {}, 'FCC': {}}
        for m in HEX_MODES:
            t = time.time()
            cv = R.curvature('AB', H_ab, m, khat, Lam, PPL)
            cv['seconds'] = round(time.time()-t, 1)
            kout['AB'][m] = cv
            print("[%s] AB  %-4s A=%.4f A_odd=%.2e c4=%.3e res=%.1e %.0fs"
                  % (kname, m, cv['A'], cv['A_odd'], cv['c4'], cv['res_max'], cv['seconds']), flush=True)
        for m in CUB_MODES:
            t = time.time()
            cv = R.curvature('FCC', H_fcc, m, khat, Lam, PPL)
            cv['seconds'] = round(time.time()-t, 1)
            kout['FCC'][m] = cv
            print("[%s] FCC %-4s A=%.4f A_odd=%.2e c4=%.3e res=%.1e %.0fs"
                  % (kname, m, cv['A'], cv['A_odd'], cv['c4'], cv['res_max'], cv['seconds']), flush=True)
        # elastic constants from raw curvatures A = d2e/ddelta2 (energy per particle
        # = energy per volume since <n>=1).  Map curvatures -> C_ij:
        #   xy (eps_xy=eps_yx=d): e = 1/2 * (4 C66) d^2  -> A_xy = 4 C66
        #   dev(eps=diag(d,-d,0)): e = 1/2*(2(C11-C12)) d^2 -> A_dev = 2(C11-C12)
        A = kout['AB']
        C66 = A['xy']['A']/4.0
        C11mC12 = A['dev']['A']/2.0
        f_iso = abs(C66 - C11mC12/2.0)/abs(C66) if C66 != 0 else float('nan')
        kout['F_ISO'] = dict(C66=C66, C11_minus_C12=C11mC12,
                             half_C11mC12=C11mC12/2.0, residual=f_iso,
                             passed=bool(f_iso <= 0.02))
        print("[%s] F-ISO |C66-(C11-C12)/2|/C66 = %.3e  passed=%s"
              % (kname, f_iso, kout['F_ISO']['passed']), flush=True)
        out['results'][kname] = kout
    json.dump(out, open("tsh4_routeS_measurements.json", "w"), indent=1)
    print("WROTE tsh4_routeS_measurements.json")

if __name__ == "__main__":
    main()
