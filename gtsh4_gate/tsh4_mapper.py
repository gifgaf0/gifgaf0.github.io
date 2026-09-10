"""
G-TSH4 CC leg -- quarantined theta-mapper (run LAST).

Consumes only the FROZEN measurement files (Phase 0 ordered e-list + delta_E;
Route S raw curvatures; Route D slopes if certified) and applies the Eddington
thresholds theta1=3%, theta2=10% -- which appear in NO other file (KNOB/Eddington
discipline).  Its own T1 self-grep runs at import.

Elastic-constant map from raw curvatures A = d2e/ddelta2 (energy per particle =
energy per volume since <n>=1):
  hex:   A_xy = 4 C66 ;  A_dev = 2(C11-C12) ;  A_bi = 2(C11+C12) ;
         A_zz = C33   ;  A_xz = 4 C44        ;  A_iso = 9 B (=C33+2C11+2C12+... )*
  cubic: A_xz = 4 C44 ;  A_dev = 2(C11-C12) ;  A_iso -> bulk
  (*A_iso reported raw; not decomposed -- volume-changing convention declared.)

Anisotropy measures (the MEASUREMENT; basal-vs-axial difference, per A-1.5/A-1.6):
  hex shear:   S_aniso = |C44 - C66| / C66            (axial vs basal shear)
  hex compr.:  P_aniso = |C33 - C11| / C11            (axial vs basal compression)
  cubic Zener: Z = 2 C44 / (C11 - C12)  ; |Z-1| is the cubic anisotropy.

theta classification of an anisotropy x:  x<=theta1 ISOTROPIC ; theta1<x<=theta2
MILD ; x>theta2 THREE-D-DISTINCT.
"""
import json
import numpy as np
import tsh4_selfgrep
tsh4_selfgrep.assert_clean(["tsh4_mapper.py"])

THETA1 = 0.03
THETA2 = 0.10

def classify(x):
    if x <= THETA1: return "ISOTROPIC"
    if x <= THETA2: return "MILD"
    return "THREE-D-DISTINCT"

CLOSE_PACKED = {'AB', 'ABC', 'FCC'}       # A-1.1 close-packed p6m stacks (ABC==FCC)
NON_CP = {'AA', 'BCC'}

def qa_verdict(estruct, delta_E):
    """A-1.1 class re-carve on the per-kernel energy dict {struct: e}."""
    items = sorted(estruct.items(), key=lambda kv: kv[1])
    e1_struct, e1 = items[0]
    cp_min = min((estruct[s] for s in estruct if s in CLOSE_PACKED), default=np.inf)
    ncp_min = min((estruct[s] for s in estruct if s in NON_CP), default=np.inf)
    class_lo, class_hi = sorted([cp_min, ncp_min])
    margin = (class_hi - class_lo)/abs(class_lo)
    argmin_class = 'close-packed' if cp_min <= ncp_min else 'non-close-packed'
    if margin <= delta_E:
        verdict = "DEGENERATE-STRUCTURE (halt E5b)"
    elif argmin_class == 'close-packed':
        verdict = "STACK-SELECTED"
    else:
        verdict = "NON-STACK-SELECTED"
    # stacking sub-question (demoted, not verdict-bearing): hcp(AB) vs fcc(FCC/ABC)
    ab = estruct.get('AB'); fcc = estruct.get('FCC')
    stack_gap = (max(ab, fcc)-min(ab, fcc))/abs(min(ab, fcc)) if ab and fcc else None
    stack_pref = ('hcp(AB)' if ab < fcc else 'fcc(FCC)') if ab and fcc else None
    return dict(order=[(s, round(e, 6)) for s, e in items],
                argmin=e1_struct, cp_min=cp_min, ncp_min=ncp_min,
                class_margin=margin, delta_E=delta_E, verdict=verdict,
                stacking_subgap=stack_gap, stacking_pref=stack_pref)

def elastic_from_A(A, family):
    if family == 'hex':
        C66 = A['xy']['A']/4.0
        C11mC12 = A['dev']['A']/2.0
        C11pC12 = A['bi']['A']/2.0
        C11 = (C11pC12 + C11mC12)/2.0
        C12 = (C11pC12 - C11mC12)/2.0
        C33 = A['zz']['A']
        C44 = A['xz']['A']/4.0
        return dict(C11=C11, C12=C12, C33=C33, C44=C44, C66=C66,
                    C11_minus_C12=C11mC12)
    else:
        C44 = A['xz']['A']/4.0
        C11mC12 = A['dev']['A']/2.0
        return dict(C44=C44, C11_minus_C12=C11mC12)

def qc_mapping(routeS):
    out = {}
    for k in routeS['results']:
        R = routeS['results'][k]
        ec_ab = elastic_from_A(R['AB'], 'hex')
        S_an = abs(ec_ab['C44']-ec_ab['C66'])/ec_ab['C66']
        P_an = abs(ec_ab['C33']-ec_ab['C11'])/ec_ab['C11']
        ec_fcc = elastic_from_A(R['FCC'], 'cubic')
        Z = 2*ec_fcc['C44']/ec_fcc['C11_minus_C12']
        out[k] = dict(
            AB=dict(C=ec_ab,
                    shear_aniso=S_an, shear_class=classify(S_an),
                    compr_aniso=P_an, compr_class=classify(P_an),
                    F_ISO_residual=R['F_ISO']['residual'], F_ISO_pass=R['F_ISO']['passed']),
            FCC=dict(C=ec_fcc, zener=Z, zener_aniso=abs(Z-1.0),
                     zener_class=classify(abs(Z-1.0))))
    return out

def main():
    ph = json.load(open("tsh4_phase0_measurements.json"))
    rs = json.load(open("tsh4_routeS_measurements.json"))
    out = {'gate': 'G-TSH4', 'mapper': 'quarantined, run last',
           'thresholds': dict(theta1=THETA1, theta2=THETA2, delta_E=ph['delta_E']),
           'QA': {}, 'QC': {}}
    for k in ph['results']:
        estruct = {s: ph['results'][k]['structures'][s]['e_reported']
                   for s in ph['results'][k]['structures']}
        out['QA'][k] = qa_verdict(estruct, ph['delta_E'])
    out['QC'] = qc_mapping(rs)
    try:
        rd = json.load(open("tsh4_routeD_measurements.json"))
        out['QD'] = {'status': rd.get('status', 'see routeD file')}
    except FileNotFoundError:
        out['QD'] = {'status': 'NOT CERTIFIED / deferred (see report)'}
    json.dump(out, open("tsh4_mapper_output.json", "w"), indent=1)
    for k in out['QA']:
        v = out['QA'][k]
        print("[%s] Q-A %s  argmin=%s class_margin=%.4f (delta_E=%g) | stacking: %s gap=%.2e"
              % (k, v['verdict'], v['argmin'], v['class_margin'], v['delta_E'],
                 v['stacking_pref'], v['stacking_subgap']))
        q = out['QC'][k]
        print("     AB shear_aniso=%.3f(%s) compr_aniso=%.3f(%s) | FCC Zener=%.3f aniso=%.3f(%s)"
              % (q['AB']['shear_aniso'], q['AB']['shear_class'],
                 q['AB']['compr_aniso'], q['AB']['compr_class'],
                 q['FCC']['zener'], q['FCC']['zener_aniso'], q['FCC']['zener_class']))
    print("WROTE tsh4_mapper_output.json")

if __name__ == "__main__":
    main()
