"""
check_mixing.py -- ground truth for the mixing-matrix part of the "flavor cube" page.
Needs only numpy. Run: python3 check_mixing.py
Writes mixing.json next to this file. Exits 1 (and writes nothing) if any check fails.

The data, the chi^2 and the angle extraction are imported from experiment E4
(seed/experiments/E4_family_symmetry: data_targets.py and e4lib.py), so the conventions are
literally the same as E4's; nothing here re-types a number that E4 already defines.

Conventions (E4's)
  * PDG standard parametrization  U = R23 . U13(delta) . R12  with
        R12 = [[c12, s12, 0], [-s12, c12, 0], [0, 0, 1]]
        U13 = [[c13, 0, s13 e^{-i delta}], [0, 1, 0], [-s13 e^{i delta}, 0, c13]]
        R23 = [[1, 0, 0], [0, c23, s23], [0, -s23, c23]]
    Rows = flavour / up type (e, mu, tau or u, c, t); columns = mass / down type
    (nu1, nu2, nu3 or d, s, b).  Checked equal to e4lib.pdg_matrix.
  * Observables from a matrix: e4lib.angles_from_U (s12^2 = |U_e2|^2/(1-|U_e3|^2), ...,
    delta from |U_mu1|^2 and J, in [0, 360) deg; nan when s12 c12 s23 c23 s13 = 0) and
    J = Im(U_mu3 U_e3* U_e2 U_mu2*).
  * PMNS chi^2 = data_targets.chi2_pmns: NuFIT 6.0 (arXiv:2410.05380v1 Table 1, IC19 without
    SK atmospheric, normal ordering) with one-sided sigma = (3sigma edge - best fit)/3 for
    s12^2, s13^2, s23^2 and delta; the delta pull uses the periodic representative
    delta + 360 k with the smallest |pull| (pull_delta_deg) and is 0 when delta is undefined.
  * CKM chi^2 = data_targets.chi2_ckm: UTfit 2022 (arXiv:2212.03894v1, full fit) Gaussian in
    lambda, A, rhobar, etabar, extracted by e4lib.wolfenstein_from_V
    (lambda = |V_us|/sqrt(|V_ud|^2+|V_us|^2), A = |V_cb|/(lambda^2 sqrt(|V_ud|^2+|V_us|^2)),
    rhobar + i etabar = -V_ud V_ub* / (V_cd V_cb*)).
  * Wolfenstein -> angles (PDG, exact): s12 = lambda, s23 = A lambda^2,
    s13 e^{i delta} = A lambda^3 (rhobar + i etabar) sqrt(1 - A^2 lambda^4)
                      / ( sqrt(1 - lambda^2) [1 - A^2 lambda^4 (rhobar + i etabar)] ).
    This is the exact inverse of the rhobar + i etabar definition above, so the round trip
    is exact to rounding.
  * p-value of a hand-set point (nothing fitted, 4 observables, chi^2 with 4 dof):
    p = exp(-x/2) (1 + x/2).  E4's Z2-partial classes were 2-parameter fits, so E4 stored
    their p with 2 dof (p = exp(-x/2)); both are written out.
  * "Cube" (real rotation for display): O = R23 . R13(s13') . R12 with s13' = s13 sign(cos delta)
    (+1 when delta is undefined or cos delta = 0), i.e. delta rounded to the nearer of 0 and
    180 deg.  As active rotations O = Rx(-theta23) Ry(theta13') Rz(-theta12), and O's columns are
    the mass axes written in flavour coordinates, so |O_ij|^2 = cos^2(flavour axis i, mass axis j).
    O = U exactly when delta is 0 or 180 deg (up to the sign convention for s13 at 180).
    Row e and column 3 of |U|^2 do not depend on delta, so |O|^2 always reproduces them; the
    cube's error sits in the four (mu, tau) x (1, 2) entries.  A trimaximal column 1 or 2 (TM1,
    TM2) is therefore not visible in the cube unless delta is near 0 or 180 deg.

Presets
  ckm_utfit         UTfit 2022 central (lambda, A, rhobar, etabar) -> angles; chi2 = 0.
  ckm_sin_3_13      lambda = 3/13, rest UTfit.  Compared also with the PDG 2024 numbers quoted
                    in the gauge paper v6.4 (|V_us| = 0.22431(85), global lambda = 0.22501(68)).
  ckm_tan_3_13      lambda = 3/sqrt(178), i.e. tan theta12 = |V_us|/|V_ud| = 3/13.  Compared with
                    the paper's tan theta_C = 0.2304(9), 0.2311(4), 0.2309(7).
  none              identity (no mixing).  PMNS chi2 = E4's best F21 lepton pattern (2459.1);
                    the CKM chi2 is undefined (lambda = 0 makes A = |V_cb|/lambda^2 undefined).
  pmns_nufit        NuFIT best fit (chi2 = 0).
  tbm               tri-bimaximal (s12^2 = 1/3, s13^2 = 0, s23^2 = 1/2).
  e4_z7, e4_tm1, e4_tm2   E4's PSL(2,7) Z2-partial survivors (results.json "z2_partial_PSL").
  e4_psl_full_best  E4's best PSL(2,7) full-residual lepton pattern (Z3 x Z7, Dirac nu).
                    results.json only carries it rounded (chi2 = 162.1); the full-precision
                    entry is E4's out/yukawa.json "residual_patterns" (results.json is
                    assembled from that file by collect_results.py).

Sources: E4 data_targets.py / e4lib.py / results.json / out/yukawa.json;
audit_followup/closeout/step2/2a_gauge_paper/Gifford_Csaszar_Gauge_Group_v6_4_2026_FINAL.md
Section 6.1 for the PDG 2024 numbers.
"""
import itertools
import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
E4 = os.path.join(REPO, "seed", "experiments", "E4_family_symmetry")
sys.path.insert(0, E4)

import data_targets as DT                                   # noqa: E402
from e4lib import angles_from_U, pdg_matrix, wolfenstein_from_V   # noqa: E402

GAUGE_PAPER = os.path.join("audit_followup", "closeout", "step2", "2a_gauge_paper",
                           "Gifford_Csaszar_Gauge_Group_v6_4_2026_FINAL.md")
# PDG 2024 numbers as quoted in the gauge paper v6.4, Section 6.1 (|V_cb| is PDG 2022 there).
PDG24 = {
    "source": GAUGE_PAPER + " Section 6.1 (PDG 2024 as quoted there)",
    "Vus": (0.22431, 0.00085),
    "lambda_global_fit": (0.22501, 0.00068),
    "Vud": (0.97367, 0.00032),
    "tan_thetaC_averaged_Vus": (0.2304, 0.0009),
    "tan_thetaC_Kmu2_pimu2": (0.2311, 0.0004),
    "tan_thetaC_global_fit": (0.2309, 0.0007),
    "Vcb_PDG2022": (0.0408, 0.0014),
}
PAPER_EXPECT = {   # what the paper states, for the checks
    "sin": {"Vus": 7.6, "lambda_global_fit": 8.5},
    "tan": {"tan_thetaC_averaged_Vus": 0.4, "tan_thetaC_Kmu2_pimu2": -0.8, "tan_thetaC_global_fit": -0.2},
}

CHECKS = []


def check(cid, holds, value):
    holds = bool(holds)
    CHECKS.append({"id": cid, "holds": holds, "value": str(value)})
    print(f"  {'PASS' if holds else 'FAIL'}  {cid}: {value}")
    return holds


# ------------------------------------------------------------------ matrices
def _cs(ssq):
    return math.sqrt(ssq), math.sqrt(1.0 - ssq)


def R12(s12sq):
    s, c = _cs(s12sq)
    return np.array([[c, s, 0.0], [-s, c, 0.0], [0.0, 0.0, 1.0]])


def R23(s23sq):
    s, c = _cs(s23sq)
    return np.array([[1.0, 0.0, 0.0], [0.0, c, s], [0.0, -s, c]])


def U13(s13sq, delta_deg):
    s, c = _cs(s13sq)
    d = 0.0 if delta_deg is None else math.radians(delta_deg)
    e = complex(math.cos(d), math.sin(d))
    return np.array([[c, 0, s / e], [0, 1, 0], [-s * e, 0, c]], dtype=complex)


def R13_signed(s13signed):
    s, c = s13signed, math.sqrt(1.0 - s13signed ** 2)
    return np.array([[c, 0.0, s], [0.0, 1.0, 0.0], [-s, 0.0, c]])


def U_pdg(s12sq, s13sq, s23sq, delta_deg):
    return R23(s23sq) @ U13(s13sq, delta_deg) @ R12(s12sq)


def cube_sign(delta_deg, tol=1e-12):
    if delta_deg is None or not math.isfinite(delta_deg):
        return 1
    cd = math.cos(math.radians(delta_deg))
    if abs(cd) < tol:
        return 1
    return 1 if cd > 0 else -1


def O_cube(s12sq, s13sq, s23sq, delta_deg):
    sg = cube_sign(delta_deg)
    return R23(s23sq) @ R13_signed(sg * math.sqrt(s13sq)) @ R12(s12sq), sg


def jarlskog(U):
    return float(np.imag(U[1, 2] * np.conj(U[0, 2]) * U[0, 1] * np.conj(U[1, 1])))


def p_value_4(x):
    return math.exp(-x / 2.0) * (1.0 + x / 2.0)


def log10_p_value_4(x):
    return (-x / 2.0 + math.log1p(x / 2.0)) / math.log(10.0)


def angles_from_wolfenstein(lam, A, rb, eb):
    """PDG exact relations -> (s12^2, s13^2, s23^2, delta_deg)."""
    w = complex(rb, eb)
    z = (A * lam ** 3 * w * math.sqrt(1.0 - A ** 2 * lam ** 4)
         / (math.sqrt(1.0 - lam ** 2) * (1.0 - A ** 2 * lam ** 4 * w)))
    s12, s23, s13 = lam, A * lam ** 2, abs(z)
    delta = math.degrees(math.atan2(z.imag, z.real)) % 360.0
    return s12 ** 2, s13 ** 2, s23 ** 2, delta


def mat(M, nd=None):
    M = np.asarray(M)
    return [[float(x) for x in row] for row in M]


def fnan(x):
    x = float(x)
    return x if math.isfinite(x) else None


def theta_deg(ssq):
    return math.degrees(math.asin(math.sqrt(min(max(ssq, 0.0), 1.0))))


def permutation_match(A, B):
    """min over row/column permutations P, Q of max |A - P B Q|."""
    best = (float("inf"), None, None)
    for pr in itertools.permutations(range(3)):
        for pc in itertools.permutations(range(3)):
            d = float(np.max(np.abs(A - B[np.ix_(pr, pc)])))
            if d < best[0]:
                best = (d, pr, pc)
    return best


def find_column(A, target):
    """column j of A whose entries (as a multiset) are closest to target; returns j, max diff."""
    t = np.sort(np.asarray(target, dtype=float))
    diffs = [float(np.max(np.abs(np.sort(A[:, j]) - t))) for j in range(3)]
    j = int(np.argmin(diffs))
    return j, diffs[j]


# ------------------------------------------------------------------ E4 references
def load_e4():
    with open(os.path.join(E4, "results.json")) as f:
        res = json.load(f)
    with open(os.path.join(E4, "out", "yukawa.json")) as f:
        yuk = json.load(f)
    return res, yuk


def pick_z2(res, G_l, target_sorted):
    for o in res["z2_partial_PSL"]:
        if o["G_l"] == G_l and np.max(np.abs(np.sort(o["fixed_column_abs2"]) - np.sort(target_sorted))) < 1e-5:
            return o
    raise KeyError((G_l, target_sorted))


def best_lepton_pattern(yuk, group):
    rows = [o for o in yuk["residual_patterns"][group] if o["kind"].startswith("lepton")]
    return min(rows, key=lambda o: o["chi2"])


# ------------------------------------------------------------------ one preset
def compute_preset(pid, sector, s12sq, s13sq, s23sq, delta_deg, definition, wolf_in=None, e4=None):
    U = U_pdg(s12sq, s13sq, s23sq, delta_deg)
    absU2 = np.abs(U) ** 2
    out = {"id": pid, "sector": sector, "definition": definition,
           "s12sq": float(s12sq), "s13sq": float(s13sq), "s23sq": float(s23sq),
           "delta_deg": None if delta_deg is None else float(delta_deg)}
    out["theta12_deg"] = theta_deg(s12sq)
    out["theta13_deg"] = theta_deg(s13sq)
    out["theta23_deg"] = theta_deg(s23sq)

    # round trip through E4's extractor
    a12, a13, a23, d_rad, J_e4 = angles_from_U(U)
    d_rt = math.degrees(d_rad) if np.isfinite(d_rad) else None
    out["roundtrip_e4_angles_from_U"] = {"s12sq": float(a12), "s13sq": float(a13), "s23sq": float(a23),
                                         "delta_deg": d_rt}
    rt_err = max(abs(a12 - s12sq), abs(a13 - s13sq), abs(a23 - s23sq))
    if delta_deg is not None and d_rt is not None:
        dd = (d_rt - delta_deg + 180.0) % 360.0 - 180.0
        rt_delta_err = abs(dd)
    else:
        rt_delta_err = 0.0 if (d_rt is None) == (delta_deg is None or s13sq == 0.0) else float("inf")
    out["_rt_err"] = (rt_err, rt_delta_err)

    out["U_re"] = mat(U.real)
    out["U_im"] = mat(U.imag)
    out["absU2"] = mat(absU2)
    out["J"] = jarlskog(U)
    out["_U"] = U

    # chi2
    if sector in ("lepton", "both"):
        c2p, detp = DT.chi2_pmns(U)
        out["chi2_pmns"] = float(c2p)
        out["pulls_pmns"] = detp["pulls"]
    if sector in ("quark", "both"):
        lam, A, rb, eb = wolfenstein_from_V(U)
        wolf = {"lambda": fnan(lam), "A": fnan(A), "rhobar": fnan(rb), "etabar": fnan(eb)}
        if wolf["rhobar"] is None and wolf["etabar"] is not None:
            # e4lib returns complex("nan") when V_cd V_cb* = 0, and complex("nan").imag == 0.0,
            # so E4 reports etabar = 0.0 for an undefined rhobar + i etabar.
            wolf["etabar"] = None
            out["wolfenstein_note"] = ("rhobar + i etabar undefined (V_cd V_cb* = 0); e4lib.wolfenstein_from_V returns "
                                       "etabar = %r there because complex('nan').imag == 0.0" % float(eb))
        out["wolfenstein_from_V"] = wolf
        defined = all(v is not None for v in wolf.values())
        c2c, detc = DT.chi2_ckm(U)
        if defined:
            out["chi2_ckm"] = float(c2c)
            out["pulls_ckm"] = detc["pulls"]
        else:
            out["chi2_ckm"] = None
            out["pulls_ckm"] = None
            out["chi2_ckm_note"] = ("undefined: wolfenstein_from_V gives lambda = %r, A = %r (|V_cb|/lambda^2 with "
                                    "lambda = 0), rhobar + i etabar = nan; E4's chi2_ckm would return a penalty "
                                    "%.6g (pull 1e3 for each non-finite value, i.e. A and rhobar, plus the lambda "
                                    "pull %.2f and an etabar pull %.2f from etabar = 0.0)"
                                    % (float(lam), float(A), c2c, detc["pulls"]["lambda"], detc["pulls"]["etabar"]))
            out["e4_chi2_ckm_penalty"] = float(c2c)
        if wolf_in is not None:
            out["wolfenstein_input"] = dict(zip(("lambda", "A", "rhobar", "etabar"), map(float, wolf_in)))
            out["_wolf_rt"] = max(abs(a - b) for a, b in zip((lam, A, rb, eb), wolf_in))
        out["Vud"], out["Vus"], out["Vub"] = float(abs(U[0, 0])), float(abs(U[0, 1])), float(abs(U[0, 2]))
        out["Vcb"], out["Vtd"], out["Vts"] = float(abs(U[1, 2])), float(abs(U[2, 0])), float(abs(U[2, 1]))
        out["tan_theta12"] = float(abs(U[0, 1]) / abs(U[0, 0]))

    if sector == "lepton":
        chi2, pulls = out["chi2_pmns"], out["pulls_pmns"]
    elif sector == "quark":
        chi2, pulls = out["chi2_ckm"], out["pulls_ckm"]
    else:  # both: the page's headline chi2 is the lepton one (the CKM one is undefined)
        chi2, pulls = out["chi2_pmns"], out["pulls_pmns"]
    out["chi2"] = chi2
    out["pulls"] = pulls
    if chi2 is None:
        out["p_value"] = None
        out["log10_p_value"] = None
    else:
        out["p_value"] = p_value_4(chi2)
        out["log10_p_value"] = log10_p_value_4(chi2)
    out["p_value_formula"] = "exp(-x/2)(1+x/2) (4 observables, nothing fitted)"

    # cube
    O, sg = O_cube(s12sq, s13sq, s23sq, delta_deg)
    out["cube_delta_deg"] = 0 if sg > 0 else 180
    out["cube_s13_signed"] = sg * math.sqrt(s13sq)
    out["cube_angles_deg"] = {"theta12": out["theta12_deg"], "theta13_signed": sg * out["theta13_deg"],
                              "theta23": out["theta23_deg"],
                              "as_active_rotations": "O = Rx(-theta23) Ry(theta13_signed) Rz(-theta12)"}
    out["cube_matrix"] = mat(O)
    out["cube_absO2"] = mat(O ** 2)
    out["max_abs_diff_O_vs_U"] = float(np.max(np.abs(O ** 2 - absU2)))
    out["_O"] = O

    # E4 reference
    out["e4_reference_chi2"] = None
    if e4 is not None:
        out["e4_reference"] = e4
        out["e4_reference_chi2"] = e4.get("chi2")
    return out


# ------------------------------------------------------------------ main
def main():
    res, yuk = load_e4()
    print("check_mixing.py  (E4 data and chi2 imported from", os.path.relpath(E4, REPO) + ")")
    print()
    presets = []

    # ---- consistency of the matrix builder with E4
    print("[conventions]")
    rng = np.random.default_rng(7)
    err = 0.0
    for _ in range(200):
        s = rng.uniform(0, 1, 3)
        d = rng.uniform(0, 360)
        err = max(err, float(np.max(np.abs(U_pdg(*s, d) - pdg_matrix(*s, math.radians(d))))))
    check("C1 R23.U13.R12 equals e4lib.pdg_matrix (200 random points)", err < 1e-14, f"max |diff| = {err:.2e}")
    err_u = 0.0
    err_rt = 0.0
    for _ in range(200):
        s = rng.uniform(0.001, 0.999, 3)
        d = rng.uniform(0, 360)
        U = U_pdg(*s, d)
        err_u = max(err_u, float(np.max(np.abs(U.conj().T @ U - np.eye(3)))))
        a12, a13, a23, dr, _ = angles_from_U(U)
        dd = abs((math.degrees(dr) - d + 180) % 360 - 180)
        err_rt = max(err_rt, abs(a12 - s[0]), abs(a13 - s[1]), abs(a23 - s[2]), dd * 1e-3)
    check("C2 U unitary and e4lib.angles_from_U inverts it (200 random points)",
          err_u < 1e-14 and err_rt < 1e-9, f"unitarity {err_u:.1e}, angle round trip {err_rt:.1e}")
    # pull of delta: E4 convention spot values
    pd = {d: DT.pull_delta_deg(d) for d in (0.0, 87.5, 96.0, 177.0, 270.0, 359.0, 422.0 - 360.0)}
    check("C3 E4 delta pull: 0 at 177, -3 at 96, +3 at 422 = 62 deg, +2.24 at 0 deg",
          abs(pd[177.0]) < 1e-12 and abs(pd[96.0] + 3) < 1e-12 and abs(pd[62.0] - 3) < 1e-12
          and abs(pd[0.0] - 183 / (245 / 3)) < 1e-12,
          ", ".join(f"{k:g}->{v:+.4f}" for k, v in pd.items()))

    # ---- CKM presets
    print()
    print("[quark presets]")
    ut = {k: DT.UTFIT[k][0] for k in ("lambda", "A", "rhobar", "etabar")}
    ckm_defs = [
        ("ckm_utfit", ut["lambda"], "UTfit 2022 central values (lambda, A, rhobar, etabar) converted exactly to PDG angles"),
        ("ckm_sin_3_13", 3.0 / 13.0, "lambda = sin theta12 = 3/13; A, rhobar, etabar at UTfit 2022"),
        ("ckm_tan_3_13", 3.0 / math.sqrt(178.0), "lambda = 3/sqrt(178), i.e. tan theta12 = 3/13; A, rhobar, etabar at UTfit 2022"),
    ]
    for pid, lam, definition in ckm_defs:
        w_in = (lam, ut["A"], ut["rhobar"], ut["etabar"])
        s12sq, s13sq, s23sq, dlt = angles_from_wolfenstein(*w_in)
        p = compute_preset(pid, "quark", s12sq, s13sq, s23sq, dlt, definition, wolf_in=w_in)
        check(f"{pid}: wolfenstein_from_V(V) returns the inputs", p["_wolf_rt"] < 1e-12,
              f"max |diff| = {p['_wolf_rt']:.1e}")
        # comparisons
        cmp = {}

        def pull(x, key):
            v, s = PDG24[key]
            return (x - v) / s
        cmp["lambda_vs_UTfit"] = (lam - DT.UTFIT["lambda"][0]) / DT.UTFIT["lambda"][1]
        cmp["lambda_vs_PDG2024_Vus"] = pull(lam, "Vus")
        cmp["matrix_Vus_vs_PDG2024_Vus"] = pull(p["Vus"], "Vus")
        cmp["lambda_vs_PDG2024_lambda_global_fit"] = pull(lam, "lambda_global_fit")
        cmp["matrix_Vud_vs_PDG2024_Vud"] = pull(p["Vud"], "Vud")
        for k in ("tan_thetaC_averaged_Vus", "tan_thetaC_Kmu2_pimu2", "tan_thetaC_global_fit"):
            cmp["tan_theta12_vs_" + k] = pull(p["tan_theta12"], k)
        cmp["matrix_Vcb_vs_Vcb_PDG2022"] = pull(p["Vcb"], "Vcb_PDG2022")
        p["comparisons_pulls"] = cmp
        presets.append(p)
        if pid == "ckm_utfit":
            check("ckm_utfit: chi2_ckm = 0", p["chi2"] < 1e-12, f"chi2 = {p['chi2']:.2e}")
        if pid == "ckm_sin_3_13":
            ok = (abs(cmp["lambda_vs_PDG2024_Vus"] - 7.6) < 0.05 and abs(cmp["lambda_vs_PDG2024_lambda_global_fit"] - 8.5) < 0.05)
            check("ckm_sin_3_13: 3/13 is 7.6 sigma above |V_us| and 8.5 sigma above global lambda (paper v6.4)",
                  ok, f"{cmp['lambda_vs_PDG2024_Vus']:+.3f}, {cmp['lambda_vs_PDG2024_lambda_global_fit']:+.3f}; "
                      f"vs UTfit lambda {cmp['lambda_vs_UTfit']:+.3f}")
        if pid == "ckm_tan_3_13":
            check("ckm_tan_3_13: tan theta12 = |V_us|/|V_ud| = 3/13 exactly",
                  abs(p["tan_theta12"] - 3 / 13) < 1e-15, f"{p['tan_theta12']!r}")
            got = [cmp["tan_theta12_vs_" + k] for k in PAPER_EXPECT["tan"]]
            ok = all(abs(g - e) < 0.05 for g, e in zip(got, PAPER_EXPECT["tan"].values()))
            check("ckm_tan_3_13: pulls vs tan theta_C 0.2304(9), 0.2311(4), 0.2309(7) are +0.4, -0.8, -0.2 (paper v6.4)",
                  ok, ", ".join(f"{g:+.3f}" for g in got) + f"; vs UTfit lambda {cmp['lambda_vs_UTfit']:+.3f}")

    # ---- none
    print()
    print("[none]")
    f21 = best_lepton_pattern(yuk, "F21")
    p = compute_preset("none", "both", 0.0, 0.0, 0.0, None, "identity matrix (no mixing)",
                       e4={"chi2": f21["chi2"], "what": "E4 best F21 full-residual lepton pattern "
                           f"({f21['G1']} x {f21['G2']}, {f21['kind']}), |U|^2 a permutation matrix",
                           "file": "seed/experiments/E4_family_symmetry/out/yukawa.json residual_patterns.F21",
                           "results_json_value": next(o["value"] for o in res["findings"]
                                                      if o["quantity"].startswith("F21: best full-residual-symmetry lepton"))})
    d, _, _ = permutation_match(np.array(p["absU2"]), np.array(f21["absU2_canonical"]))
    check("none: |U|^2 = identity is a row/column permutation of E4's F21 best pattern", d < 1e-12, f"{d:.1e}")
    rel = abs(p["chi2_pmns"] - f21["chi2"]) / f21["chi2"]
    check("none: PMNS chi2 reproduces E4's F21 best lepton pattern", rel < 1e-3,
          f"{p['chi2_pmns']:.10g} vs E4 {f21['chi2']:.10g} (rel {rel:.1e})")
    check("none: CKM chi2 undefined (lambda = 0, A and rhobar + i etabar undefined)", p["chi2_ckm"] is None,
          f"wolfenstein = {p['wolfenstein_from_V']}; E4 penalty would be {p['e4_chi2_ckm_penalty']:.6g}")
    presets.append(p)

    # ---- lepton presets
    print()
    print("[lepton presets]")
    nf = {k: DT.NUFIT[k][0] for k in ("s12sq", "s13sq", "s23sq", "delta_deg")}
    p = compute_preset("pmns_nufit", "lepton", nf["s12sq"], nf["s13sq"], nf["s23sq"], nf["delta_deg"],
                       "NuFIT 6.0 best fit (IC19 w/o SK-atm, NO)")
    check("pmns_nufit: chi2 = 0", p["chi2"] < 1e-12, f"chi2 = {p['chi2']:.2e}")
    presets.append(p)

    p = compute_preset("tbm", "lepton", 1.0 / 3.0, 0.0, 0.5, None, "tri-bimaximal: s12^2 = 1/3, s13^2 = 0, s23^2 = 1/2")
    U = p["_U"].real
    cols = {1: np.array([2, -1, 1]) / math.sqrt(6), 2: np.array([1, 1, -1]) / math.sqrt(3),
            3: np.array([0, 1, 1]) / math.sqrt(2)}
    errs = {j: float(np.max(np.abs(U[:, j - 1] - v))) for j, v in cols.items()}
    check("tbm: columns are (2,-1,1)/sqrt6, (1,1,-1)/sqrt3, (0,1,1)/sqrt2 (signs as stated)",
          max(errs.values()) < 1e-15 and float(np.max(np.abs(p["_U"].imag))) == 0.0,
          ", ".join(f"col{j} {e:.1e}" for j, e in errs.items()))
    ex = np.array([1.0, 0.0, 0.0])
    n2 = U[:, 1]
    proj = ex - (ex @ n2) * n2
    proj /= np.linalg.norm(proj)
    e_proj = float(np.max(np.abs(proj - U[:, 0])))
    check("tbm: column 1 = e axis projected on the plane perpendicular to column 2, normalized", e_proj < 1e-15,
          f"proj = {np.round(proj * math.sqrt(6), 12).tolist()}/sqrt6, |diff| {e_proj:.1e}")
    p["tbm_columns"] = {"col1": "(2,-1,1)/sqrt6", "col2": "(1,1,-1)/sqrt3", "col3": "(0,1,1)/sqrt2",
                        "col1_is_normalized_projection_of_e_perp_col2": bool(e_proj < 1e-15)}
    check("tbm: chi2 (s13^2 = 0 dominates; delta undefined -> pull 0)", p["pulls"]["delta"] == 0.0,
          f"chi2 = {p['chi2']:.6f}, pulls {', '.join(f'{k} {v:+.4f}' for k, v in p['pulls'].items())}")
    presets.append(p)

    # ---- E4 Z2-partial survivors
    z2_defs = [
        ("e4_z7", "Z7", [0.131512, 0.204495, 0.663993], None,
         "E4 PSL(2,7) Z2-partial survivor G_l = Z7, G_nu = Z2 (<Z7, Z2> = PSL(2,7)): best fit"),
        ("e4_tm1", "Z3", [2 / 3, 1 / 6, 1 / 6], 0,
         "E4 PSL(2,7) Z2-partial survivor G_l = Z3, G_nu = Z2, fixed column (2/3, 1/6, 1/6) = TM1 (<Z3, Z2> = S4): best fit"),
        ("e4_tm2", "Z3", [1 / 3, 1 / 3, 1 / 3], 1,
         "E4 PSL(2,7) Z2-partial survivor G_l = Z3, G_nu = Z2, fixed column (1/3, 1/3, 1/3) = TM2 (<Z3, Z2> = A4): best fit"),
    ]
    for pid, gl, target, col_expected, definition in z2_defs:
        o = pick_z2(res, gl, target)
        b = o["best"]
        e4ref = {"chi2": o["chi2"], "p_value": o["p_value"], "p_value_dof": 2,
                 "p_value_note": "E4 fitted 2 parameters (theta, phi) to 4 observables: p = exp(-chi2/2)",
                 "best": b, "fixed_column_abs2": o["fixed_column_abs2"], "G_l": o["G_l"], "G_nu": o["G_nu"],
                 "file": "seed/experiments/E4_family_symmetry/results.json z2_partial_PSL"}
        p = compute_preset(pid, "lepton", b["s12sq"], b["s13sq"], b["s23sq"], b["delta_deg"], definition, e4=e4ref)
        rel = abs(p["chi2"] - o["chi2"]) / o["chi2"]
        check(f"{pid}: chi2 reproduces E4", rel < 1e-3, f"{p['chi2']:.10f} vs E4 {o['chi2']:.10f} (rel {rel:.1e})")
        dp = max(abs(p["pulls"][k] - b["pulls"][k]) for k in b["pulls"])
        dJ = abs(p["J"] - b["J"])
        check(f"{pid}: pulls and J reproduce E4", dp < 1e-9 and dJ < 1e-12, f"max pull diff {dp:.1e}, J diff {dJ:.1e}")
        A = np.array(p["absU2"])
        j, dcol = find_column(A, target)
        tol = 1e-6 if col_expected is None else 1e-9
        okc = dcol < tol and (col_expected is None or j == col_expected)
        check(f"{pid}: fixed column {np.round(target, 6).tolist()} appears in |U|^2", okc,
              f"column {j + 1} (nu{j + 1}) = {np.round(A[:, j], 9).tolist()}, max diff {dcol:.1e}")
        p["fixed_column"] = {"column_index_1based": j + 1, "values_in_row_order": A[:, j].tolist(),
                             "max_diff_vs_target": dcol, "target_sorted": sorted(target)}
        p["e4_p_value_2dof"] = o["p_value"]
        O2 = p["_O"] ** 2
        jc, dcube = find_column(O2, target)
        p["fixed_column"]["in_cube_absO2"] = {
            "best_column_1based": jc + 1, "max_diff_vs_target": dcube,
            "same_column_values_in_row_order": O2[:, j].tolist(),
            "note": "the cube rounds delta to %d deg; only row e and column 3 of |U|^2 are delta-independent"
                    % p["cube_delta_deg"]}
        print(f"  info  {pid}: in the cube |O|^2 the fixed column is lost: best column {jc + 1}, "
              f"max diff {dcube:.3f} (column {j + 1} of |O|^2 = {np.round(O2[:, j], 6).tolist()})")
        presets.append(p)

    # ---- E4 PSL full-residual best lepton pattern
    psl = best_lepton_pattern(yuk, "PSL")
    b = psl["best"]
    finding = next(o for o in res["findings"] if o["quantity"].startswith("PSL: best full-residual-symmetry lepton"))
    e4ref = {"chi2": psl["chi2"], "p_value": psl["p_value"], "p_value_dof": 4, "best": b,
             "absU2_canonical": psl["absU2_canonical"], "G1": psl["G1"], "G2": psl["G2"], "kind": psl["kind"],
             "count": psl["count"],
             "file": "seed/experiments/E4_family_symmetry/out/yukawa.json residual_patterns.PSL "
                     "(results.json findings only has the rounded value)",
             "results_json_value": finding["value"], "results_json_note": finding["note"]}
    p = compute_preset("e4_psl_full_best", "lepton", b["s12sq"], b["s13sq"], b["s23sq"], b["delta_deg"],
                       f"E4 best PSL(2,7) full-residual lepton pattern ({psl['G1']} x {psl['G2']}, {psl['kind']}), "
                       "no free parameter; delta = 0 (stored as %.3g deg)" % b["delta_deg"], e4=e4ref)
    rel = abs(p["chi2"] - psl["chi2"]) / psl["chi2"]
    check("e4_psl_full_best: chi2 reproduces E4 (162.1)", rel < 1e-3 and finding["value"].startswith("chi2 = 162.1"),
          f"{p['chi2']:.10f} vs E4 {psl['chi2']:.10f} (rel {rel:.1e}); results.json: '{finding['value']}'")
    dpv = abs(p["p_value"] - psl["p_value"]) / psl["p_value"]
    check("e4_psl_full_best: 4-dof p-value equals E4's stored p", dpv < 1e-9, f"{p['p_value']:.6e} vs {psl['p_value']:.6e}")
    d, _, _ = permutation_match(np.array(p["absU2"]), np.array(psl["absU2_canonical"]))
    check("e4_psl_full_best: |U|^2 is a row/column permutation of E4's canonical |U|^2", d < 1e-6, f"{d:.1e}")
    presets.append(p)

    # ---- generic checks over all presets
    print()
    print("[all presets]")
    worst_rt = max(max(q["_rt_err"]) for q in presets)
    check("angles_from_U(U) returns every preset's s_ij^2 and delta", worst_rt < 1e-9, f"max diff {worst_rt:.1e}")
    worst_o = max(float(np.max(np.abs(q["_O"].T @ q["_O"] - np.eye(3)))) for q in presets)
    worst_det = max(abs(np.linalg.det(q["_O"]) - 1) for q in presets)
    check("cube O is a rotation (O^T O = 1, det O = +1)", worst_o < 1e-14 and worst_det < 1e-14,
          f"{worst_o:.1e}, {worst_det:.1e}")
    worst_cp = 0.0
    for q in presets:
        if q["delta_deg"] is None or q["cube_delta_deg"] == 0 and abs(q["delta_deg"] % 360) < 1e-9:
            worst_cp = max(worst_cp, q["max_abs_diff_O_vs_U"])
    check("O reproduces |U|^2 exactly when delta is undefined or 0", worst_cp < 1e-15, f"{worst_cp:.1e}")
    worst_inv = 0.0
    for q in presets:
        A, O2 = np.array(q["absU2"]), q["_O"] ** 2
        worst_inv = max(worst_inv, float(np.max(np.abs(A[0, :] - O2[0, :]))), float(np.max(np.abs(A[:, 2] - O2[:, 2]))))
    check("row e and column 3 of |O|^2 equal those of |U|^2 for every preset (delta-independent entries)",
          worst_inv < 1e-15, f"{worst_inv:.1e}; the cube error sits in the mu/tau x 1/2 block")
    worst_J = 0.0
    for q in presets:
        s12, c12 = _cs(q["s12sq"])
        s13, c13 = _cs(q["s13sq"])
        s23, c23 = _cs(q["s23sq"])
        d = 0.0 if q["delta_deg"] is None else math.radians(q["delta_deg"])
        worst_J = max(worst_J, abs(q["J"] - s12 * c12 * s23 * c23 * s13 * c13 ** 2 * math.sin(d)))
    check("J = Im(U_mu3 U_e3* U_e2 U_mu2*) = s12 c12 s23 c23 s13 c13^2 sin delta", worst_J < 1e-16, f"{worst_J:.1e}")

    # ---- table
    print()
    hdr = (f"{'id':18s} {'s12^2':>10s} {'s13^2':>11s} {'s23^2':>10s} {'delta':>9s} {'chi2':>12s} "
           f"{'p(4dof)':>9s} {'J':>10s} {'cube':>4s} {'max|O2-U2|':>10s} {'E4 chi2':>12s}")
    print(hdr)
    print("-" * len(hdr))
    for q in presets:
        dl = "undef" if q["delta_deg"] is None else f"{q['delta_deg']:.3f}"
        c2 = "undef" if q["chi2"] is None else f"{q['chi2']:.6g}"
        pv = "-" if q["p_value"] is None else f"{q['p_value']:.3g}"
        e4c = "-" if q["e4_reference_chi2"] is None else f"{q['e4_reference_chi2']:.6g}"
        print(f"{q['id']:18s} {q['s12sq']:10.6f} {q['s13sq']:11.3e} {q['s23sq']:10.6f} {dl:>9s} {c2:>12s} "
              f"{pv:>9s} {q['J']:10.3e} {q['cube_delta_deg']:4d} {q['max_abs_diff_O_vs_U']:10.2e} {e4c:>12s}")
    print()
    for q in presets:
        if q["pulls"]:
            print(f"  {q['id']:18s} pulls: " + ", ".join(f"{k} {v:+.4f}" for k, v in q["pulls"].items()))
        if "comparisons_pulls" in q:
            print(f"  {'':18s} vs PDG24/paper: " + ", ".join(f"{k.replace('_vs_', ' vs ')} {v:+.3f}"
                                                         for k, v in q["comparisons_pulls"].items()))
    print()
    print("|U|^2 and cube O per preset:")
    for q in presets:
        print(f"  {q['id']}  (cube delta = {q['cube_delta_deg']})")
        for r1, r2 in zip(q["absU2"], q["cube_matrix"]):
            print("     |U|^2 " + " ".join(f"{x:9.6f}" for x in r1) + "    O " + " ".join(f"{x:+9.6f}" for x in r2))

    # ---- data block
    data = {"NuFIT": {"source": DT.NUFIT["source"],
                      "sigma_convention": "one-sided sigma = (3sigma edge - best fit)/3 on each side (E4 data_targets.py)",
                      "delta_pull": "periodic: representative delta + 360 k with the smallest |pull| (data_targets.pull_delta_deg); 0 if delta undefined"},
            "UTfit": {"source": DT.UTFIT["source"], "convention": "Gaussian; lambda, A, rhobar, etabar from e4lib.wolfenstein_from_V"},
            "PDG2024_quoted_by_gauge_paper_v6_4": {"source": PDG24["source"]},
            "p_value_formula": "p = exp(-chi2/2) (1 + chi2/2): chi2 with 4 dof (hand-set point, 4 observables, nothing fitted)",
            "e4_folder": os.path.relpath(E4, REPO)}
    for k in ("s12sq", "s13sq", "s23sq", "delta_deg"):
        bf, lo, hi = DT.NUFIT[k]
        data["NuFIT"][k] = {"best_fit": bf, "sigma_lo": lo, "sigma_hi": hi,
                            "range_3sigma": [bf - 3 * lo, bf + 3 * hi],
                            "published_1sigma_lo_hi": list(DT.NUFIT_1SIGMA[k])}
    for k in ("lambda", "A", "rhobar", "etabar"):
        data["UTfit"][k] = {"value": DT.UTFIT[k][0], "sigma": DT.UTFIT[k][1]}
    for k, v in PDG24.items():
        if k != "source":
            data["PDG2024_quoted_by_gauge_paper_v6_4"][k] = {"value": v[0], "sigma": v[1]}
    data["PDG2024_quoted_by_gauge_paper_v6_4"]["note"] = (
        "Vcb is PDG 2022 per the paper; tan theta_C values are |V_us|/|V_ud| from the averaged |V_us|, "
        "from K_mu2/pi_mu2, and from the global fit")

    for q in presets:
        for k in [k for k in q if k.startswith("_")]:
            del q[k]

    all_ok = all(c["holds"] for c in CHECKS)
    print()
    print(f"{sum(c['holds'] for c in CHECKS)}/{len(CHECKS)} checks pass")
    if not all_ok:
        print("FAIL: mixing.json not written")
        sys.exit(1)
    doc = {"generated_by": "flavor_cube/check_mixing.py",
           "conventions": __doc__.split("Presets")[0].strip(),
           "data": data, "presets": presets, "checks": CHECKS, "all_pass": all_ok}
    path = os.path.join(HERE, "mixing.json")
    with open(path, "w") as f:
        json.dump(doc, f, indent=1, allow_nan=False)
    print("wrote", os.path.relpath(path, REPO))


if __name__ == "__main__":
    main()
