"""
G-TSH4 CC leg -- R-2 response (comparison stage, post-processing only; no GP compute).

Recompute the LOCKED Q-C statistic A_3D = max-from-mean spread of the TRANSVERSE
acoustic speeds over the E4/A-1.4 direction sets, from the CC leg's own frozen
elastic constants (Route S), via the Christoffel closed forms -- which is also the
C-POS control.  Map to the locked arms ISO-3D / UNDERDETERMINED-3D / ANISO-3D using
theta1=3%, theta2=10%.

Elastic constants from the frozen raw curvatures A=d2e/ddelta2 (energy/volume,
<n>=1 so per-particle=per-volume):
  hex:   C66=A_xy/4 ; C11-C12=A_dev/2 ; C11+C12=A_bi/2 ; C33=A_zz ; C44=A_xz/4 ;
         C13 from A_iso = 2C11 + C33 + 2C12 + 4C13  (hydrostatic hex closed form).
  cubic: C44=A_xz/4 ; C11-C12=A_dev/2 ; C11+2C12=A_iso/3.
Mass density rho=1 (mean density 1, m=1), so v^2 = Christoffel eigenvalue.
"""
import json
import numpy as np
import tsh4_selfgrep
tsh4_selfgrep.assert_clean(["tsh4_R2_christoffel.py"])

THETA1, THETA2 = 0.03, 0.10
S3 = np.sqrt(3.0)

def hex_constants(A):
    C66 = A['xy']['A']/4.0
    C11mC12 = A['dev']['A']/2.0
    C11pC12 = A['bi']['A']/2.0
    C11 = (C11pC12 + C11mC12)/2.0
    C12 = (C11pC12 - C11mC12)/2.0
    C33 = A['zz']['A']
    C44 = A['xz']['A']/4.0
    C13 = (A['iso']['A'] - 2*C11 - C33 - 2*C12)/4.0
    return dict(C11=C11, C12=C12, C13=C13, C33=C33, C44=C44, C66=C66)

def cubic_constants(A):
    C44 = A['xz']['A']/4.0
    C11mC12 = A['dev']['A']/2.0
    C11p2C12 = A['iso']['A']/3.0
    C12 = (C11p2C12 - C11mC12)/3.0
    C11 = C11mC12 + C12
    return dict(C11=C11, C12=C12, C44=C44)

def voigt6_hex(c):
    C11, C12, C13, C33, C44, C66 = c['C11'], c['C12'], c['C13'], c['C33'], c['C44'], c['C66']
    return np.array([
        [C11, C12, C13, 0, 0, 0],
        [C12, C11, C13, 0, 0, 0],
        [C13, C13, C33, 0, 0, 0],
        [0, 0, 0, C44, 0, 0],
        [0, 0, 0, 0, C44, 0],
        [0, 0, 0, 0, 0, C66]], float)

def voigt6_cubic(c):
    C11, C12, C44 = c['C11'], c['C12'], c['C44']
    return np.array([
        [C11, C12, C12, 0, 0, 0],
        [C12, C11, C12, 0, 0, 0],
        [C12, C12, C11, 0, 0, 0],
        [0, 0, 0, C44, 0, 0],
        [0, 0, 0, 0, C44, 0],
        [0, 0, 0, 0, 0, C44]], float)

_VOIGT = [(0, 0), (1, 1), (2, 2), (1, 2), (0, 2), (0, 1)]
def voigt_to_tensor(Cv):
    C = np.zeros((3, 3, 3, 3))
    for I, (i, j) in enumerate(_VOIGT):
        for J, (k, l) in enumerate(_VOIGT):
            val = Cv[I, J]
            for (a, b) in {(i, j), (j, i)}:
                for (cc, d) in {(k, l), (l, k)}:
                    C[a, b, cc, d] = val
    return C

def christoffel_speeds(C4, nhat):
    n = np.asarray(nhat, float); n = n/np.linalg.norm(n)
    Gamma = np.einsum('ijkl,j,l->ik', C4, n, n)
    w, V = np.linalg.eigh(Gamma)                 # w = rho v^2 (rho=1)
    speeds = np.sqrt(np.clip(w, 0, None))
    # longitudinal = eigenvector most parallel to n; other two transverse
    para = np.abs(V.T @ n)
    long_idx = int(np.argmax(para))
    trans = [speeds[i] for i in range(3) if i != long_idx]
    return dict(all_speeds=sorted(float(s) for s in speeds),
                longitudinal=float(speeds[long_idx]),
                transverse=sorted(float(t) for t in trans),
                long_purity=float(para[long_idx]))

DIRS_AB = {
    'GammaM_basal': [1, 0, 0],
    'GammaK_basal': [np.cos(np.pi/6), np.sin(np.pi/6), 0],
    'GammaA_axial': [0, 0, 1],
    'oblique45':    [1, 0, 1],
}
DIRS_FCC = {
    '100': [1, 0, 0],
    '110': [1, 1, 0],
    '111': [1, 1, 1],
    'oblique_110plane': [1, 1, np.sqrt(2)],
}

def A3D_from_transverse(perdir):
    vals = []
    for d in perdir:
        vals.extend(perdir[d]['transverse'])
    vals = np.array(vals)
    mean = vals.mean()
    max_from_mean = float(np.max(np.abs(vals-mean))/mean)
    spread_minmax = float((vals.max()-vals.min())/mean)
    arm = ('ISO-3D' if max_from_mean <= THETA1 else
           'UNDERDETERMINED-3D' if max_from_mean <= THETA2 else 'ANISO-3D')
    return dict(transverse_speeds=[float(v) for v in vals], mean=float(mean),
                A_3D_max_from_mean=max_from_mean, spread_minmax=spread_minmax,
                arm=arm)

def main():
    rs = json.load(open("tsh4_routeS_measurements.json"))
    out = {'gate': 'G-TSH4', 'response': 'R-2 (locked transverse A_3D, C-POS Christoffel)',
           'note': 'post-processing on frozen Route-S C_ij; no GP compute; rho=1',
           'thresholds': dict(theta1=THETA1, theta2=THETA2), 'results': {}}
    for k in rs['results']:
        R = rs['results'][k]
        c_ab = hex_constants(R['AB']); c_fcc = cubic_constants(R['FCC'])
        C4_ab = voigt_to_tensor(voigt6_hex(c_ab))
        C4_fcc = voigt_to_tensor(voigt6_cubic(c_fcc))
        pd_ab = {d: christoffel_speeds(C4_ab, DIRS_AB[d]) for d in DIRS_AB}
        pd_fcc = {d: christoffel_speeds(C4_fcc, DIRS_FCC[d]) for d in DIRS_FCC}
        a3_ab = A3D_from_transverse(pd_ab); a3_fcc = A3D_from_transverse(pd_fcc)
        out['results'][k] = dict(
            AB=dict(constants=c_ab, perdir=pd_ab, A_3D=a3_ab),
            FCC=dict(constants=c_fcc, perdir=pd_fcc, A_3D=a3_fcc))
        print("[%s] AB  C13=%.2f  A_3D(transverse)=%.4f -> %s   (basal K vs M trans: %s / %s)"
              % (k, c_ab['C13'], a3_ab['A_3D_max_from_mean'], a3_ab['arm'],
                 np.round(pd_ab['GammaK_basal']['transverse'],4),
                 np.round(pd_ab['GammaM_basal']['transverse'],4)))
        print("[%s] FCC A_3D(transverse)=%.4f -> %s"
              % (k, a3_fcc['A_3D_max_from_mean'], a3_fcc['arm']))
    json.dump(out, open("tsh4_R2_christoffel_output.json", "w"), indent=1)
    print("WROTE tsh4_R2_christoffel_output.json")

if __name__ == "__main__":
    main()
