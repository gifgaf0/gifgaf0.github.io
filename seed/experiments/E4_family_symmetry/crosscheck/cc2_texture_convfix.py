"""
cc2_texture_convfix.py -- second-pass repair of a convention slip in the first-pass cc_texture.py.

cc_texture.lepton_obs took U_e = left singular vectors of M_e (the 'L-bar M_e e_R' convention) but
U_nu = CONJUGATE left singular vectors of M_nu (the holomorphic 'nu^T M nu' convention).  For the LNR
operators (holomorphic in all fields) the consistent choice is the holomorphic one for both, i.e.
U_e = conj(left singular vectors of M_e).  (The original E4 code uses the 'bar' convention for both,
which is the complex conjugate of the holomorphic PMNS: same angles, delta -> -delta; equivalent for fits.)
The slip is harmless whenever M_e is real up to row/column phases -- every 'min' class (M_e diagonal) and
every class with phi5 in {Z3, Z7} (conjugating phi10 and the couplings then gives the same set) -- but it
changes the model for the 'gen' classes with phi5 in {P, G}.  This script refits ALL 64 'gen' lepton
classes with the consistent convention (first-pass fitting code otherwise unchanged) and compares with
the original verdicts.  Output: out/texture_cc2_convfix.jsonl, out/texture_cc2_convfix.log.
"""
import json, math, os, sys, time, zlib
import numpy as np
from scipy.stats import chi2 as chi2dist
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cc_texture as T

JL = T.base + "texture_cc2_convfix.jsonl"

def lepton_obs_consistent(Me, Mnu):
    Ue, se = T.left_basis(Me)
    Ue = Ue.conj()                     # holomorphic L M_e e^c:  M_e = U_e* diag V^dagger
    Un, sn = T.left_basis(Mnu)
    Un = Un.conj()                     # holomorphic nu^T M nu:  M = U* diag U^dagger
    if se[2] <= 0 or se[0] / se[2] < 1e-14 or sn[2] <= 0: return None
    U = Ue.conj().T @ Un
    a = T.mix_angles(U)
    d21, d31 = sn[1] ** 2 - sn[0] ** 2, sn[2] ** 2 - sn[0] ** 2
    r = d31 / d21 if d21 > 1e-14 * sn[2] ** 2 else 1e12
    return dict(me_mmu=se[0] / se[1], mmu_mtau=se[1] / se[2], r=r, s12sq=a[0], s13sq=a[1], s23sq=a[2], delta=a[3],
                gap_e=min(np.diff(se)) / se[2], rank_e=se[0] / se[2], gap_nu=min(np.diff(sn)) / sn[2])
T.lepton_obs = lepton_obs_consistent   # make_lepton's closure looks the name up at call time

done = set()
if os.path.exists(JL):
    done = {json.loads(l)["name"] for l in open(JL) if l.strip()}
t0 = time.time()
for name, sector, npar, obs in T.classes(False):
    if ":gen:" not in name or sector != "lepton" or name in done: continue
    rng = np.random.default_rng(zlib.crc32(("cc2fix" + name).encode()))
    dead, why = T.structural(sector, obs, npar, rng)
    f = T.residual_fn(sector, obs)
    if dead: c, px = T.fit(f, npar, rng, 3, nfev_start=100, nfev_polish=0)
    else: c, px = T.fit(f, npar, rng, 12)
    ne = T.n_eff(f, npar, rng, p_best=px)
    dof = 7 - ne
    if dead: verdict = "excluded (structural)"
    elif dof >= 1: verdict = "SURVIVES" if (1 - chi2dist.cdf(c, dof)) > 0.01 else "excluded"
    else: verdict = "accommodates (no prediction)" if c < 1 else "excluded"
    rec = dict(name=name, npar=npar, n_eff=ne, dof=dof, chi2=c, verdict=verdict, why=why)
    with open(JL, "a") as fh: fh.write(json.dumps(rec) + "\n")
    print(f"[{time.time() - t0:6.1f}s] {name:45s} npar={npar} neff={ne} chi2={c:.4g} {verdict}", flush=True)

# compare with the original results.json
ORIG = json.load(open(os.path.join(os.path.dirname(T.base.rstrip('/')), "..", "results.json")))
def key_orig(n):
    p = n.split("|"); d = dict(x.split("=") for x in p[2:]); return (d["phi5"], d["phi10"], d["phi1"])
orig = {key_orig(c["name"]): c for c in ORIG["texture_survey_all"] if c["name"].startswith("lepton|gen|")}
mine = {}
for l in open(JL):
    r = json.loads(l); d = dict(x.split("=") for x in r["name"].split(":")[2].split(",")); mine[(d["phi5"], d["phi10"], d["phi1"])] = r
dis = [(k, orig[k]["verdict_final"], mine[k]["verdict"], orig[k]["n_eff"], mine[k]["n_eff"]) for k in orig
       if orig[k]["verdict_final"] != mine[k]["verdict"] or (mine[k]["verdict"] != "excluded (structural)" and orig[k]["n_eff"] != mine[k]["n_eff"])]
print(f"gen lepton classes compared: {len(orig)}; verdict/N_eff disagreements with the original: {len(dis)}")
for d in dis: print("  ", d)
print("PASS" if not dis else "FAIL", "consistent-convention refit of the 64 'gen' lepton classes reproduces the original verdicts and N_eff")
