import sys, json, numpy as np
sys.path.insert(0, "/home/claude/sqt_persp/gate_tsh1_staging"); import g_tsh1_chatleg as T
sys.path.insert(0, "/home/claude/lbc_exploration"); from lbc_weights import bdg_full
from gsolve2d import tight
a = 1.4574710087903182
st, _ = T.polish(T.relax_cell(a, 22.0, "soft", Nc=96)); st, rl, rn = tight(st)
unit = 2*np.pi/a; out = {}
for kf in (0.01, 0.03, 0.05, 0.10):
    r = bdg_full(st, 22.0, "soft", kf*unit*np.array([1.0, 0.0]), n=32)
    om, Z = r["om"], r["Z"]; ok = om > 1e-9
    out[kf] = dict(chi_direct=r["chi_static"], chi_modesum=float(np.sum(2*Z[ok]/om[ok])))
    print(kf, out[kf], flush=True)
json.dump(out, open("chi_g22_v2.json", "w"), indent=1)
