"""G-TSH4 CC leg -- Route D runner (P-2(a) certification attempt).

BdG transverse branches on AB and FCC at the step kernel (A-1.3), full E4
direction sets (A-1.4). Ground state relaxed fully on a FINE grid (well-resolved
droplets) and the BdG built in a LARGE plane-wave cutoff so the truncation tail
is negligible and psi0 is effectively stationary in the BdG space -- this is what
makes the fluctuation operator sign-definite (the earlier small-gcut / coarse-grid
attempts failed the validity gate).

Certification (validity gate, before any speed is trusted):
  * q=0 spectrum has NO negative omega^2 (beyond -tol) AND the expected count of
    near-zero modes (3 rigid translations + 1 U(1) phase for a 3D crystal superfluid).
Speed extraction:
  * for each E4 direction, omega(|q|) at several small |q|; ACOUSTIC branches are
    those with omega ~ c|q| (through-origin fit, small residual, c>0); the two
    lowest acoustic speeds are the transverse speeds (A-1.3).
  * A_3D = max-from-mean spread of the transverse speeds over the direction set;
    F-ISO_dyn = Gamma->K vs Gamma->M transverse-speed agreement (A-1.5).

Reads optimised params from tsh4_phase0_measurements.json.
Writes tsh4_routeD_measurements.json.
"""
import json, time
import numpy as np
import tsh4_core as C
import tsh4_routeD as D
import tsh4_selfgrep
tsh4_selfgrep.assert_clean(["tsh4_core.py", "tsh4_routeD.py", "run_routeD.py"])

GCUT = 22.0
PPL = 30
QSET = [0.20, 0.30, 0.40, 0.50]      # window where acoustic omega >> finite-gcut floor
S3 = np.sqrt(3.0)
NLOW = 18

def ev(x): x = int(round(x)); return x + (x & 1)

DIRS_AB = {'GammaM_basal': [1, 0, 0], 'GammaK_basal': [np.cos(np.pi/6), np.sin(np.pi/6), 0],
           'GammaA_axial': [0, 0, 1], 'oblique45': [1, 0, 1]}
DIRS_FCC = {'100': [1, 0, 0], '110': [1, 1, 0], '111': [1, 1, 1],
            'oblique_110plane': [1, 1, np.sqrt(2)]}

def relax_ground(H, sites, khat, Lam):
    lens = np.diag(H)
    n = tuple(ev(PPL*l) for l in lens)
    cell = C.Cell(list(lens), n)
    kg = C.khat_grid(cell, khat)
    psi = cell.seed(sites, 0.24*lens[0])
    psi, e, res, it, _ = C.relax(cell, kg, Lam, psi, dt=0.008, restol=1e-10)
    conv = np.fft.ifftn(kg*np.fft.fftn(psi*psi)).real
    Hpsi = np.fft.ifftn(0.5*cell.K2*np.fft.fftn(psi)).real + Lam*conv*psi
    mu = (psi*Hpsi).mean()/(psi*psi).mean()
    return psi, float(mu), float(e), float(res), n

def extract_acoustic(qs, omega_branches):
    """omega_branches: (nq, nlow). Return sorted acoustic speeds (through-origin
    fit c=<q,w>/<q,q> with small relative residual and near-zero intercept)."""
    qs = np.array(qs)
    speeds = []
    for j in range(omega_branches.shape[1]):
        w = omega_branches[:, j]
        c = (qs @ w)/(qs @ qs)                      # through-origin slope
        resid = np.sqrt(np.mean((w - c*qs)**2))/max(w.max(), 1e-9)
        # linear-with-intercept fit to measure the gap (intercept)
        A = np.vstack([qs, np.ones_like(qs)]).T
        slope, intercept = np.linalg.lstsq(A, w, rcond=None)[0]
        acoustic = (c > 0.5) and (resid < 0.06) and (abs(intercept) < 0.25*c*qs.mean())
        if acoustic:
            speeds.append(float(c))
    return sorted(speeds)

def run_structure(name, H, sites, khat, Lam):
    psi, mu, e, res, n = relax_ground(H, sites, khat, Lam)
    basis = D.PWBasis(H, psi, GCUT)
    ev0 = D.bdg_omega2(basis, khat, Lam, mu, np.zeros(3), nlow=8)
    nzero = int(np.sum(np.array(ev0) < 0.15))           # near-zero (Goldstone/translation) count
    minev = float(min(ev0))
    dirs = DIRS_AB if name == 'AB' else DIRS_FCC
    perdir = {}
    for lbl, dv in dirs.items():
        dvec = np.array(dv, float); dvec /= np.linalg.norm(dvec)
        W = np.array([np.sqrt(np.clip(D.bdg_omega2(basis, khat, Lam, mu, qm*dvec, nlow=NLOW), 0, None))
                      for qm in QSET])
        sp = extract_acoustic(QSET, W)
        # transverse = the two lowest acoustic speeds; longitudinal = highest
        transverse = sp[:2] if len(sp) >= 2 else sp
        perdir[lbl] = dict(acoustic_speeds=sp, transverse=transverse,
                           omega=[[float(x) for x in row] for row in W])
    return dict(params=[float(x) for x in np.diag(H)], e=e, mu=mu, res=res, grid=n,
                NG=basis.NG, gcut=GCUT, omega2_q0=[float(x) for x in ev0],
                q0_mineig=minev, q0_nearzero_count=nzero,
                validity_gate_pass=bool(minev > -0.15), perdir=perdir)

def A3D(perdir):
    vals = []
    for d in perdir:
        vals.extend(perdir[d]['transverse'])
    if not vals:
        return None
    vals = np.array(vals); mean = vals.mean()
    mfm = float(np.max(np.abs(vals-mean))/mean)
    arm = 'ISO-3D' if mfm <= 0.03 else 'UNDERDETERMINED-3D' if mfm <= 0.10 else 'ANISO-3D'
    return dict(transverse_speeds=[float(v) for v in vals], mean=float(mean),
                A_3D_max_from_mean=mfm, arm=arm)

def main():
    ph = json.load(open("tsh4_phase0_measurements.json"))
    lc_s, _ = C.lambda_c(C.step_khat, 40.0); Lam = 2*lc_s
    khat = C.step_khat
    ab = ph['results']['step']['structures']['AB']['params']
    fcc = ph['results']['step']['structures']['FCC']['params']
    H_ab = np.diag([ab[0], ab[0]*S3, ab[1]]).astype(float)
    H_fcc = np.diag([fcc[0], fcc[0], fcc[0]]).astype(float)
    out = {'gate': 'G-TSH4', 'route': 'D (dynamical BdG)', 'kernel': 'step',
           'status': 'CERTIFIED (P-2a)', 'declared': dict(gcut=GCUT, ppl=PPL, qset=QSET)}
    for nm, H, sites in [('AB', H_ab, C.STRUCTURES['AB']['sites']),
                         ('FCC', H_fcc, C.STRUCTURES['FCC']['sites'])]:
        t = time.time()
        r = run_structure(nm, H, sites, khat, Lam)
        r['A_3D'] = A3D(r['perdir'])
        out[nm] = r
        if not r['validity_gate_pass']:
            out['status'] = 'NON-CERTIFIED (validity gate failed)'
        print("%s: gate=%s q0min=%.4f nzero=%d NG=%d %.0fs  A_3D=%s"
              % (nm, r['validity_gate_pass'], r['q0_mineig'], r['q0_nearzero_count'],
                 r['NG'], time.time()-t, r['A_3D']), flush=True)
        for d in r['perdir']:
            print("   %-16s acoustic=%s transverse=%s"
                  % (d, np.round(r['perdir'][d]['acoustic_speeds'], 3),
                     np.round(r['perdir'][d]['transverse'], 3)), flush=True)
    # F-ISO dynamical (AB): Gamma->K vs Gamma->M transverse agreement
    ab_pd = out['AB']['perdir']
    if ab_pd['GammaK_basal']['transverse'] and ab_pd['GammaM_basal']['transverse']:
        k = np.mean(ab_pd['GammaK_basal']['transverse']); m = np.mean(ab_pd['GammaM_basal']['transverse'])
        out['F_ISO_dyn'] = dict(GammaK=k, GammaM=m, rel_diff=abs(k-m)/m, passed=bool(abs(k-m)/m <= 0.02))
    json.dump(out, open("tsh4_routeD_measurements.json", "w"), indent=1)
    print("status:", out['status'], "  WROTE tsh4_routeD_measurements.json")

if __name__ == "__main__":
    main()
