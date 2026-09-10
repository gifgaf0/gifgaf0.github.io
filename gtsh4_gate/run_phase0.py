"""G-TSH4 CC leg -- Phase 0 execution runner. Writes tsh4_phase0_measurements.json."""
import json, time, sys
import numpy as np
import tsh4_core as C
import tsh4_phase0 as P
import tsh4_selfgrep
tsh4_selfgrep.assert_clean(["tsh4_core.py", "tsh4_phase0.py", "run_phase0.py"])

PPL = 20                      # points per unit length for optimisation
KERNELS = {}
lc_s, ks_s = C.lambda_c(C.step_khat, 40.0)
KERNELS['step'] = dict(khat=C.step_khat, Lam=2*lc_s, Lam_c=lc_s, kstar=ks_s)
gem = C.Gem8Khat()
lc_g, ks_g = C.lambda_c(gem, 25.0)
KERNELS['gem8'] = dict(khat=gem, Lam=2*lc_g, Lam_c=lc_g, kstar=ks_g)

# initial lattice guesses (a,c) / L -- seeds only, optimiser refines
INIT = {'AA': (1.33, 1.15), 'AB': (1.33, 2.30), 'ABC': (1.33, 3.45),
        'FCC': (1.63,), 'BCC': (1.33,)}

def run_kernel(kname):
    K = KERNELS[kname]; khat, Lam = K['khat'], K['Lam']
    out = dict(kernel=kname, Lambda=Lam, Lambda_c=K['Lam_c'], kstar=K['kstar'],
               structures={})
    out['C_NEG'] = P.cneg(khat, Lam)
    for s in ['AA', 'AB', 'ABC', 'FCC', 'BCC']:
        t = time.time()
        if C.STRUCTURES[s]['family'] == 'hex':
            (a, c), e = P.optimise_hex(s, khat, Lam, PPL, *INIT[s])
            params = (a, c)
        else:
            (L,), e = P.optimise_cubic(s, khat, Lam, PPL, INIT[s][0])
            params = (L,)
        fc = P.fconv(s, params, khat, Lam, PPL)
        sym = P.symmetry_ok(s, params, khat, Lam, PPL)
        rec = dict(params=[float(x) for x in params], e_opt=float(e),
                   e_reported=float(fc['e_fine']), fconv=fc, symmetry=sym,
                   seconds=round(time.time()-t, 1))
        if C.STRUCTURES[s]['family'] == 'hex':
            rec['c_over_a'] = float(params[1]/params[0])
        out['structures'][s] = rec
        print("[%s] %-4s params=%s e=%.6f (fine=%.6f) fconv=%.1e/%s sym=%s %.0fs"
              % (kname, s, np.round(params,4), e, fc['e_fine'], fc['rel_change'],
                 fc['passed'], sym['ok'], rec['seconds']), flush=True)
    return out

if __name__ == "__main__":
    res = {'gate': 'G-TSH4', 'leg': 'CC full-from-scratch (E6)',
           'functional': 'e = <1/2|grad psi|^2> + (Lam/2)<n (Uhat*n)>, <n>=1',
           'coupling_convention': 'Lambda = 2.0 * Lambda_c (roton threshold)',
           'delta_E': 1e-4, 'ppl_opt': PPL, 'results': {}}
    for kname in ['step', 'gem8']:
        t = time.time()
        res['results'][kname] = run_kernel(kname)
        print("== kernel %s done in %.0fs ==" % (kname, time.time()-t), flush=True)
    with open("tsh4_phase0_measurements.json", "w") as f:
        json.dump(res, f, indent=1)
    print("WROTE tsh4_phase0_measurements.json")
