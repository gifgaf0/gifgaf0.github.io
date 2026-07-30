"""G-TSH4 CC leg -- Route D runner. BdG transverse branches on AB and FCC at the
step kernel (A-1.3), full E4 direction sets (A-1.4). Reads optimised params from
tsh4_phase0_measurements.json. Writes tsh4_routeD_measurements.json.

Declared before any Q-D quantity (KNOB): kernel=step; self-consistent truncated
ground state at |G|<=GCUT so psi0 is stationary in the BdG basis; |q| set
{0.08,0.16,0.24}; transverse = the two lowest-slope gapless (acoustic) branches;
Goldstone check omega(q->0)->0; F-ISO dyn = Gamma->K vs Gamma->M slope <=2%."""
import json, time
import numpy as np
import tsh4_core as C
import tsh4_routeD as D
import tsh4_selfgrep
tsh4_selfgrep.assert_clean(["tsh4_core.py", "tsh4_routeD.py", "run_routeD.py"])

GCUT = 18.0
PPL = 28
QMAGS = [0.08, 0.16, 0.24]
S3 = np.sqrt(3.0)

def ev(x): x = int(round(x)); return x + (x & 1)

DIRS_AB = {  # Cartesian directions in the orthorhombic hex cell
    'GammaM_basal': [1, 0, 0],
    'GammaK_basal': [np.cos(np.pi/6), np.sin(np.pi/6), 0],
    'GammaA_axial': [0, 0, 1],
    'oblique45':    [1, 0, 1],
}
DIRS_FCC = {
    '100': [1, 0, 0],
    '110': [1, 1, 0],
    '111': [1, 1, 1],
    'oblique_110plane': [1, 1, np.sqrt(2)],   # 45 deg between [110] and [001]
}

def run_structure(name, H, sites, khat, Lam):
    lens = np.linalg.norm(H, axis=0)
    n = tuple(ev(PPL*l) for l in lens)
    cell = C.Cell(list(np.diag(H)) if np.allclose(H, np.diag(np.diag(H))) else lens, n)
    # build orthorhombic Cell (all our optimised cells are orthorhombic/cubic)
    cell = C.Cell([H[0,0], H[1,1], H[2,2]], n)
    kg = C.khat_grid(cell, khat)
    psi0 = cell.seed(sites, 0.24*H[0,0])
    psi, mu, e, res = D.relax_truncated(cell, kg, Lam, GCUT, psi0)
    basis = D.PWBasis(H, psi, GCUT)
    # q=0 stability: exactly one ~zero acoustic mode, no negative omega^2
    ev0 = D.bdg_omega2(basis, khat, Lam, mu, np.zeros(3), nlow=6)
    dirs = DIRS_AB if name == 'AB' else DIRS_FCC
    branches = {}
    for lbl, dv in dirs.items():
        branches[lbl] = D.acoustic_branches(basis, khat, Lam, mu, dv, QMAGS, nlow=5)
    out = dict(params=[float(H[i, i]) for i in range(3)] if name != 'FCC' else [float(H[0,0])],
               e_trunc=e, mu=mu, res=res, NG=basis.NG, gcut=GCUT,
               omega2_q0=[float(x) for x in ev0], branches=branches)
    return out

def kernels():
    lc_s, _ = C.lambda_c(C.step_khat, 40.0)
    return C.step_khat, 2*lc_s

def main():
    ph = json.load(open("tsh4_phase0_measurements.json"))
    khat, Lam = kernels()
    ab = ph['results']['step']['structures']['AB']['params']
    fcc = ph['results']['step']['structures']['FCC']['params']
    H_ab = np.diag([ab[0], ab[0]*S3, ab[1]]).astype(float)
    H_fcc = np.diag([fcc[0], fcc[0], fcc[0]]).astype(float)
    out = {'gate': 'G-TSH4', 'route': 'D (dynamical BdG)', 'kernel': 'step',
           'declared': dict(gcut=GCUT, ppl=PPL, qmags=QMAGS,
                            transverse='two lowest-slope gapless branches (A-1.3)')}
    t = time.time()
    out['AB'] = run_structure('AB', H_ab, C.STRUCTURES['AB']['sites'], khat, Lam)
    print("AB done %.0fs NG=%d q0min=%.4f" % (time.time()-t, out['AB']['NG'], min(out['AB']['omega2_q0'])), flush=True)
    t = time.time()
    out['FCC'] = run_structure('FCC', H_fcc, C.STRUCTURES['FCC']['sites'], khat, Lam)
    print("FCC done %.0fs NG=%d q0min=%.4f" % (time.time()-t, out['FCC']['NG'], min(out['FCC']['omega2_q0'])), flush=True)
    json.dump(out, open("tsh4_routeD_measurements.json", "w"), indent=1)
    print("WROTE tsh4_routeD_measurements.json")

if __name__ == "__main__":
    main()
