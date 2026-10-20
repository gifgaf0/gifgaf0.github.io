"""E5 cross-check extra: where does the neutron's enclosed charge Q_n(<R) peak? (massless ANW and AN84 massive)
Uses the cross-check's own profile and matrix densities.  Writes cc_extra.json."""
import json
import os
import sys

import numpy as np
from scipy.optimize import minimize_scalar

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cc_hedgehog as H   # noqa: E402
import cc_profile as P    # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
out = {}
hh = json.load(open(os.path.join(HERE, 'cc_hedgehog.json')))
for tag, beta, Fpi, e, Lam in (('massless_ANW', 0.0, 129.0, 5.45, hh['massless']['Lambda_tilde']),
                               ('massive_AN84', hh['massive_AN84']['beta'], 108.0, 4.84, hh['massive_AN84']['Lambda_tilde_matrix'])):
    pr = P.solve_profile(beta=beta, X=80.0 if beta == 0 else 50.0, xm=1.0 if beta == 0 else 1.5)
    fm = H.HBARC / (e * Fpi)

    def Qn(Rfm):
        cb, cl, _ = H.cut_integrals(pr, Rfm / fm, beta ** 2)
        return 0.5 * cb - 0.5 * cl / Lam
    r = minimize_scalar(lambda R: -Qn(R), bounds=(0.3, 1.5), method='bounded', options={'xatol': 1e-4})
    out[tag] = {'R_peak_fm': r.x, 'Qn_peak': -r.fun, 'Qn_1fm': Qn(1.0), 'Qn_0.5fm': Qn(0.5)}
    print(tag, out[tag])
json.dump(out, open(os.path.join(HERE, 'cc_extra.json'), 'w'), indent=1)
