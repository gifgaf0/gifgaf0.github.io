#!/usr/bin/env python3
"""
crosscheck_mixing.py -- independent second computation of mixing-matrix numbers.

Written from scratch (no import of the repo's e4lib.py / data_targets.py).  The conventions and
the data values were transcribed by hand from
    seed/experiments/E4_family_symmetry/data_targets.py and e4lib.py
so that a convention slip in either implementation shows up as a difference.

Conventions
  U = R23 * U13(delta) * R12   (built by matrix multiplication, not from a closed form)
    R12 = [[c12, s12, 0], [-s12, c12, 0], [0, 0, 1]]
    U13 = [[c13, 0, s13 e^{-i delta}], [0, 1, 0], [-s13 e^{i delta}, 0, c13]]
    R23 = [[1, 0, 0], [0, c23, s23], [0, -s23, c23]]
  rows = flavor / up-type, columns = mass / down-type.
  Observables are extracted from |U|^2 and a rephasing-invariant quartet:
    s13^2 = |U_e3|^2, s12^2 = |U_e2|^2 / c13^2, s23^2 = |U_mu3|^2 / c13^2,
    W = U_e2 U_mu3 U_e3^* U_mu2^*   (J = Im W),
    W + s12^2 s23^2 s13^2 c13^2 = s12 c12 s23 c23 s13 c13^2 e^{i delta}  ->  delta = arg(...)
  (E4 instead takes cos delta from |U_mu1|^2 and sin delta from J; the two must agree.)
  chi2_PMNS: one-sided sigmas (3sigma edge - bf)/3, delta periodic representative with smallest |pull|.
  chi2_CKM: Wolfenstein lambda, A, rhobar, etabar (UTfit 2022) from V, Gaussian.
  p-value of a hand-set point, 4 observables, 0 parameters: p = exp(-x/2) (1 + x/2).
"""
import json
import math
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
E4DIR = os.path.join(HERE, "..", "..", "seed", "experiments", "E4_family_symmetry")

# ----------------------------------------------------------------- data (transcribed)
NUFIT_BF = {"s12sq": 0.307, "s13sq": 0.02195, "s23sq": 0.561, "delta_deg": 177.0}
NUFIT_3SIG = {"s12sq": (0.275, 0.345), "s13sq": (0.02023, 0.02376), "s23sq": (0.430, 0.596),
              "delta_deg": (96.0, 422.0)}
SIG = {k: ((NUFIT_BF[k] - NUFIT_3SIG[k][0]) / 3.0, (NUFIT_3SIG[k][1] - NUFIT_BF[k]) / 3.0)
       for k in NUFIT_BF}                     # (sigma below, sigma above)
UTFIT = {"lambda": (0.22519, 0.00083), "A": (0.828, 0.011), "rhobar": (0.1609, 0.0095),
         "etabar": (0.347, 0.010)}
# gauge paper v6.4 (audit_followup/closeout/step2/2a_gauge_paper/..._FINAL.md, Section 6.1)
PDG24_VUS = (0.22431, 0.00085)
PDG24_LAMBDA_GLOBAL = (0.22501, 0.00068)
TAN_C = {"tan_avg_Vus_over_Vud": (0.2304, 0.0009), "tan_Kmu2_pimu2": (0.2311, 0.0004),
         "tan_global_fit": (0.2309, 0.0007)}


# ----------------------------------------------------------------- matrices
def r12(s):
    c = math.sqrt(1 - s * s)
    return np.array([[c, s, 0], [-s, c, 0], [0, 0, 1]], dtype=complex)


def r23(s):
    c = math.sqrt(1 - s * s)
    return np.array([[1, 0, 0], [0, c, s], [0, -s, c]], dtype=complex)


def r13_real(s):
    """R13 with signed sine s (s may be negative); c = +sqrt(1 - s^2)."""
    c = math.sqrt(1 - s * s)
    return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]], dtype=float)


def u13(s, delta):
    c = math.sqrt(1 - s * s)
    return np.array([[c, 0, s * np.exp(-1j * delta)], [0, 1, 0], [-s * np.exp(1j * delta), 0, c]],
                    dtype=complex)


def pdg_U_from_sines(s12, s13, s23, delta):
    return r23(s23) @ u13(s13, delta) @ r12(s12)


def pdg_U(s12sq, s13sq, s23sq, delta_rad):
    return pdg_U_from_sines(math.sqrt(s12sq), math.sqrt(s13sq), math.sqrt(s23sq), delta_rad)


def cube_O(s12, s13, s23, delta):
    """Real 'cube' rotation O = R23 R13(s13') R12, s13' = s13 sign(cos delta) (+1 if undefined/0)."""
    if delta is None or not np.isfinite(delta):
        sgn = 1.0
    else:
        cd = math.cos(delta)
        sgn = -1.0 if cd < 0 else 1.0
    s13p = s13 * sgn
    c12, c23 = math.sqrt(1 - s12 ** 2), math.sqrt(1 - s23 ** 2)
    R12 = np.array([[c12, s12, 0], [-s12, c12, 0], [0, 0, 1]])
    R23 = np.array([[1, 0, 0], [0, c23, s23], [0, -s23, c23]])
    O = R23 @ r13_real(s13p) @ R12
    return O, (0.0 if sgn > 0 else 180.0)


# ----------------------------------------------------------------- extraction
def extract(U, tol=1e-12):
    A = np.abs(U) ** 2
    s13sq = float(A[0, 2])
    c13sq = 1.0 - s13sq
    s12sq = float(A[0, 1] / c13sq) if c13sq > 1e-15 else 0.0
    s23sq = float(A[1, 2] / c13sq) if c13sq > 1e-15 else 0.0
    W = U[0, 1] * U[1, 2] * np.conj(U[0, 2]) * np.conj(U[1, 1])
    J = float(np.imag(U[1, 2] * np.conj(U[0, 2]) * U[0, 1] * np.conj(U[1, 1])))
    norm = math.sqrt(max(s12sq * (1 - s12sq) * s23sq * (1 - s23sq) * s13sq, 0.0)) * c13sq
    if norm > tol:
        Z = W + s12sq * s23sq * s13sq * c13sq
        delta = math.atan2(Z.imag, Z.real) % (2 * math.pi)
        zmod_err = abs(abs(Z) - norm)          # internal consistency (unitarity of the PDG form)
    else:
        delta, zmod_err = None, 0.0
    return dict(s12sq=s12sq, s13sq=s13sq, s23sq=s23sq, delta=delta, J=J, zmod_err=zmod_err)


def delta_alt_from_tau1(U, ex):
    """Alternative delta: cos from |U_tau1|^2, sin from J (different entry than E4's |U_mu1|^2)."""
    s12sq, s13sq, s23sq = ex["s12sq"], ex["s13sq"], ex["s23sq"]
    if ex["delta"] is None:
        return None
    s12, s13, s23 = map(math.sqrt, (s12sq, s13sq, s23sq))
    c12, c23, c13 = math.sqrt(1 - s12sq), math.sqrt(1 - s23sq), math.sqrt(1 - s13sq)
    # |U_tau1|^2 = s12^2 s23^2 + c12^2 c23^2 s13^2 - 2 s12 c12 s23 c23 s13 cos d
    k = 2 * s12 * c12 * s23 * c23 * s13
    cosd = (s12sq * s23sq + c12 ** 2 * c23 ** 2 * s13sq - abs(U[2, 0]) ** 2) / k
    sind = ex["J"] / (k / 2 * c13 ** 2)
    return math.atan2(sind, max(-1.0, min(1.0, cosd))) % (2 * math.pi)


# ----------------------------------------------------------------- chi2
def pull_side(x, key):
    bf = NUFIT_BF[key]
    lo, hi = SIG[key]
    d = x - bf
    return d / (hi if d > 0 else lo)


def pull_delta_deg(ddeg):
    if ddeg is None:
        return 0.0
    best = None
    for k in range(-3, 4):
        x = ddeg + 360.0 * k
        p = pull_side(x, "delta_deg")
        if best is None or abs(p) < abs(best):
            best = p
    return best


def chi2_pmns_from(ex):
    ddeg = None if ex["delta"] is None else math.degrees(ex["delta"])
    pulls = {"s12sq": pull_side(ex["s12sq"], "s12sq"), "s13sq": pull_side(ex["s13sq"], "s13sq"),
             "s23sq": pull_side(ex["s23sq"], "s23sq"), "delta": pull_delta_deg(ddeg)}
    return sum(v * v for v in pulls.values()), pulls


def wolfenstein(V, tiny=1e-14):
    aud, aus, acb = abs(V[0, 0]), abs(V[0, 1]), abs(V[1, 2])
    r = math.hypot(aud, aus)
    lam = aus / r if r > 0 else None
    A = acb / (lam ** 2 * r) if (lam is not None and lam > tiny) else None
    den = V[1, 0] * np.conj(V[1, 2])
    if abs(den) > tiny:
        z = -V[0, 0] * np.conj(V[0, 2]) / den
        rb, eb = float(z.real), float(z.imag)
    else:
        rb = eb = None
    return {"lambda": lam, "A": A, "rhobar": rb, "etabar": eb}


def chi2_ckm_from(wf):
    pulls, defined = {}, True
    for k, (v0, s) in UTFIT.items():
        if wf[k] is None:
            pulls[k] = None
            defined = False
        else:
            pulls[k] = (wf[k] - v0) / s
    c2 = sum(v * v for v in pulls.values()) if defined else None
    return c2, pulls


def ckm_sines_from_wolfenstein(lam, A, rb, eb):
    """Exact PDG relations."""
    s12 = lam
    s23 = A * lam ** 2
    rho = complex(rb, eb)
    z13 = A * lam ** 3 * rho * math.sqrt(1 - A ** 2 * lam ** 4) / (
        math.sqrt(1 - lam ** 2) * (1 - A ** 2 * lam ** 4 * rho))
    return s12, abs(z13), s23, math.atan2(z13.imag, z13.real) % (2 * math.pi)


def pvalue4(x):
    if x is None:
        return None
    return math.exp(-x / 2) * (1 + x / 2)


def pvalue2(x):
    return math.exp(-x / 2)


# ----------------------------------------------------------------- E4 stored references
def load_e4():
    res = json.load(open(os.path.join(E4DIR, "results.json")))
    yk = json.load(open(os.path.join(E4DIR, "out", "yukawa.json")))
    z2 = res["z2_partial_PSL"]

    def pick(G_l, col):
        for e in z2:
            if e["G_l"] == G_l and all(abs(a - b) < 1e-5 for a, b in zip(sorted(e["fixed_column_abs2"]), sorted(col))):
                return e
        raise KeyError((G_l, col))

    z7 = [e for e in z2 if e["G_l"] == "Z7"]
    assert len(z7) == 1
    tm1 = pick("Z3", (2 / 3, 1 / 6, 1 / 6))
    tm2 = pick("Z3", (1 / 3, 1 / 3, 1 / 3))
    psl = sorted([e for e in yk["residual_patterns"]["PSL"] if e["kind"].startswith("lepton")],
                 key=lambda e: e["chi2"])[0]
    f21 = sorted([e for e in yk["residual_patterns"]["F21"] if e["kind"].startswith("lepton")],
                 key=lambda e: e["chi2"])[0]
    # E4's tri-bimaximal texture (LNR exact): 7-observable chi2 whose 3 mass-ratio pulls are ~0
    tbm = res["texture_survey_best_predictive"]["lepton"]
    # does results.json itself hold the 162 pattern?
    raw = open(os.path.join(E4DIR, "results.json")).read()
    psl_in_results = ("162.0921" in raw)
    return dict(z7=z7[0], tm1=tm1, tm2=tm2, psl=psl, f21=f21, tbm=tbm, psl_in_results=psl_in_results)


# ----------------------------------------------------------------- per-preset report
def r(x, n=15):
    if x is None:
        return None
    return float(x)


def mat_list(M):
    return [[float(v) for v in row] for row in M]


def report(pid, U, sector, notes="", e4_ref=None, extra=None):
    ex = extract(U)
    s12, s13, s23 = map(math.sqrt, (ex["s12sq"], ex["s13sq"], ex["s23sq"]))
    ddeg = None if ex["delta"] is None else math.degrees(ex["delta"])
    absU2 = np.abs(U) ** 2
    O, cube_d = cube_O(s12, s13, s23, ex["delta"])
    diffO = float(np.max(np.abs(O ** 2 - absU2)))
    out = {"id": pid, "sector": sector,
           "s12sq": ex["s12sq"], "s13sq": ex["s13sq"], "s23sq": ex["s23sq"],
           "delta_deg": ddeg,
           "theta12_deg": math.degrees(math.asin(s12)), "theta13_deg": math.degrees(math.asin(s13)),
           "theta23_deg": math.degrees(math.asin(s23)),
           "absU2": mat_list(absU2), "J": ex["J"],
           "unitarity_err": float(np.max(np.abs(U.conj().T @ U - np.eye(3)))),
           "delta_extraction_consistency": ex["zmod_err"],
           "cube_delta_deg": cube_d, "cube_matrix_O": mat_list(O), "max_abs_diff_O_vs_U": diffO}
    alt = delta_alt_from_tau1(U, ex)
    if alt is not None and ex["delta"] is not None:
        dd = math.remainder(math.degrees(alt) - ddeg, 360.0)
        out["delta_alt_tau1_minus_quartet_deg"] = dd
    c2p, pp = chi2_pmns_from(ex)
    wf = wolfenstein(U)
    c2c, pc = chi2_ckm_from(wf)
    if sector in ("lepton", "both"):
        out["chi2_pmns"] = c2p
        out["pulls_pmns"] = pp
    if sector in ("quark", "both"):
        out["chi2_ckm"] = c2c
        out["wolfenstein"] = wf
        out["pulls_ckm"] = pc
    main = c2p if sector in ("lepton", "both") else c2c
    out["chi2"] = main
    out["pulls"] = pp if sector in ("lepton", "both") else pc
    out["p_value"] = pvalue4(main)
    out["log10_p_value"] = None if main is None else (-main / 2 + math.log1p(main / 2)) / math.log(10)
    out["e4_reference_chi2"] = e4_ref
    out["notes"] = notes
    if extra:
        out.update(extra)
    return out


def main():
    E4 = load_e4()
    presets, checks = [], []

    def chk(cid, holds, value):
        checks.append({"id": cid, "holds": bool(holds), "value": str(value)})

    # ---------------- CKM presets
    def ckm_preset(pid, lam, notes, extra_fn=None):
        A, rb, eb = UTFIT["A"][0], UTFIT["rhobar"][0], UTFIT["etabar"][0]
        s12, s13, s23, d = ckm_sines_from_wolfenstein(lam, A, rb, eb)
        V = pdg_U_from_sines(s12, s13, s23, d)
        rep = report(pid, V, "quark", notes)
        wf = rep["wolfenstein"]
        rt = max(abs(wf["lambda"] - lam), abs(wf["A"] - A), abs(wf["rhobar"] - rb), abs(wf["etabar"] - eb))
        rep["input_wolfenstein"] = {"lambda": lam, "A": A, "rhobar": rb, "etabar": eb}
        rep["wolfenstein_roundtrip_maxdev"] = rt
        rep["Vus_abs"] = float(abs(V[0, 1]))
        rep["Vud_abs"] = float(abs(V[0, 0]))
        rep["tan_theta12"] = float(abs(V[0, 1]) / abs(V[0, 0]))
        rep["delta_minus_arg_rhoeta_deg"] = rep["delta_deg"] - math.degrees(math.atan2(eb, rb))
        if extra_fn:
            extra_fn(rep, V)
        return rep, rt

    rep, rt = ckm_preset("ckm_utfit", UTFIT["lambda"][0],
                         "UTfit 2022 central values converted exactly with the PDG relations")
    chk("ckm_utfit_roundtrip_chi2_zero", rep["chi2_ckm"] < 1e-12 and rt < 1e-12,
        f"chi2_ckm={rep['chi2_ckm']:.3e}, max |wolfenstein - input| = {rt:.3e}")
    presets.append(rep)

    def sin_extra(rep, V):
        lam = rep["input_wolfenstein"]["lambda"]
        rep["lambda_pulls"] = {
            "vs_UTfit_2022": (lam - UTFIT["lambda"][0]) / UTFIT["lambda"][1],
            "vs_PDG2024_Vus_0.22431(85)": (lam - PDG24_VUS[0]) / PDG24_VUS[1],
            "vs_PDG2024_global_lambda_0.22501(68)": (lam - PDG24_LAMBDA_GLOBAL[0]) / PDG24_LAMBDA_GLOBAL[1],
            "Vus_of_V_vs_PDG2024_Vus": (rep["Vus_abs"] - PDG24_VUS[0]) / PDG24_VUS[1]}

    rep, rt = ckm_preset("ckm_sin_3_13", 3 / 13, "lambda = sin theta12 = 3/13; A, rhobar, etabar at UTfit",
                         sin_extra)
    lp = rep["lambda_pulls"]
    chk("ckm_sin_3_13_roundtrip", rt < 1e-12, f"max dev {rt:.2e}")
    chk("ckm_sin_3_13_pulls_7.6_8.5", abs(lp["vs_PDG2024_Vus_0.22431(85)"] - 7.6) < 0.05
        and abs(lp["vs_PDG2024_global_lambda_0.22501(68)"] - 8.5) < 0.05,
        f"vs |Vus| {lp['vs_PDG2024_Vus_0.22431(85)']:.4f}, vs global lambda "
        f"{lp['vs_PDG2024_global_lambda_0.22501(68)']:.4f}, vs UTfit {lp['vs_UTfit_2022']:.4f}")
    presets.append(rep)

    def tan_extra(rep, V):
        lam = rep["input_wolfenstein"]["lambda"]
        t = rep["tan_theta12"]
        rep["lambda_pulls"] = {
            "vs_UTfit_2022": (lam - UTFIT["lambda"][0]) / UTFIT["lambda"][1],
            "vs_PDG2024_Vus_0.22431(85)_using_|Vus|": (rep["Vus_abs"] - PDG24_VUS[0]) / PDG24_VUS[1],
            "vs_PDG2024_global_lambda_0.22501(68)": (lam - PDG24_LAMBDA_GLOBAL[0]) / PDG24_LAMBDA_GLOBAL[1]}
        rep["tan_pulls"] = {k: (t - v) / s for k, (v, s) in TAN_C.items()}

    rep, rt = ckm_preset("ckm_tan_3_13", 3 / math.sqrt(178),
                         "lambda = 3/sqrt(178) so tan theta12 = |V_us|/|V_ud| = 3/13; A, rhobar, etabar at UTfit",
                         tan_extra)
    tp = rep["tan_pulls"]
    chk("ckm_tan_3_13_tan_exact", abs(rep["tan_theta12"] - 3 / 13) < 1e-14,
        f"|Vus|/|Vud| - 3/13 = {rep['tan_theta12'] - 3 / 13:.2e}")
    chk("ckm_tan_3_13_pulls_+0.4_-0.8_-0.2",
        abs(tp["tan_avg_Vus_over_Vud"] - 0.4) < 0.05 and abs(tp["tan_Kmu2_pimu2"] + 0.8) < 0.05
        and abs(tp["tan_global_fit"] + 0.2) < 0.05,
        f"{tp['tan_avg_Vus_over_Vud']:+.4f}, {tp['tan_Kmu2_pimu2']:+.4f}, {tp['tan_global_fit']:+.4f}; "
        f"lambda vs UTfit {rep['lambda_pulls']['vs_UTfit_2022']:+.4f}")
    presets.append(rep)

    # ---------------- none (identity)
    U = np.eye(3, dtype=complex)
    rep = report("none", U, "both",
                 "identity: PMNS delta undefined (pull 0). CKM: lambda = 0, so A = |V_cb|/(lambda^2 ...) "
                 "is 0/0 and rhobar+i etabar has V_cd V_cb^* = 0 in the denominator: chi2_ckm undefined "
                 "(E4's chi2_ckm would substitute pull 1e3 for the three non-finite parameters).",
                 e4_ref=E4["f21"]["chi2"])
    rep["chi2_ckm_defined"] = False
    rep["lambda_pull_vs_UTfit"] = (0.0 - UTFIT["lambda"][0]) / UTFIT["lambda"][1]
    rep["e4_style_penalised_chi2_ckm"] = rep["lambda_pull_vs_UTfit"] ** 2 + 3 * 1e6
    chk("none_chi2_pmns_2459", abs(rep["chi2_pmns"] - E4["f21"]["chi2"]) < 1e-9,
        f"{rep['chi2_pmns']:.10f} vs E4 F21 best lepton {E4['f21']['chi2']:.10f}")
    presets.append(rep)

    # ---------------- PMNS NuFIT
    U = pdg_U(0.307, 0.02195, 0.561, math.radians(177.0))
    rep = report("pmns_nufit", U, "lepton", "NuFIT 6.0 best fit")
    chk("pmns_nufit_chi2_zero", rep["chi2_pmns"] < 1e-20, f"{rep['chi2_pmns']:.3e}")
    presets.append(rep)

    # ---------------- TBM
    U = pdg_U(1 / 3, 0.0, 0.5, 0.0)
    rep = report("tbm", U, "lepton",
                 "tri-bimaximal; s13 = 0 so delta undefined (pull 0). E4 reference = its LNR-exact texture "
                 "(exactly TBM), a 7-observable chi2 whose 3 mass-ratio pulls are ~1e-8.",
                 e4_ref=E4["tbm"]["chi2"])
    expect = {1: np.array([2, -1, 1]) / math.sqrt(6), 2: np.array([1, 1, -1]) / math.sqrt(3),
              3: np.array([0, 1, 1]) / math.sqrt(2)}
    colerr = {j: float(np.max(np.abs(U[:, j - 1] - expect[j]))) for j in (1, 2, 3)}
    rep["tbm_columns"] = {f"col{j}": [float(v.real) for v in U[:, j - 1]] for j in (1, 2, 3)}
    rep["tbm_column_errors_vs_stated"] = colerr
    e = np.array([1.0, 0, 0])
    v2 = expect[2]
    proj = e - (e @ v2) * v2
    proj /= np.linalg.norm(proj)
    rep["tbm_proj_e_perp_col2"] = proj.tolist()
    chk("tbm_columns_signs", max(colerr.values()) < 1e-15,
        f"col1=(2,-1,1)/sqrt6, col2=(1,1,-1)/sqrt3, col3=(0,1,1)/sqrt2; max err {max(colerr.values()):.1e}")
    chk("tbm_col1_is_projection_of_e_perp_col2", np.max(np.abs(proj - U[:, 0].real)) < 1e-15,
        f"proj = {np.round(proj * math.sqrt(6), 12).tolist()}/sqrt6")
    presets.append(rep)

    # ---------------- E4 survivors
    def e4_preset(pid, ent, notes, extra_fn=None):
        b = ent["best"]
        U = pdg_U(b["s12sq"], b["s13sq"], b["s23sq"], math.radians(b["delta_deg"]))
        rep = report(pid, U, "lepton", notes, e4_ref=ent["chi2"])
        rep["e4_input"] = {k: b[k] for k in ("s12sq", "s13sq", "s23sq", "delta_deg", "J")}
        rep["e4_pulls"] = b["pulls"]
        rep["max_pull_diff_vs_e4"] = max(abs(rep["pulls_pmns"][k] - b["pulls"][k]) for k in b["pulls"])
        rep["J_diff_vs_e4"] = rep["J"] - b["J"]
        if "p_value" in ent:
            rep["e4_stored_p_value"] = ent["p_value"]
        if extra_fn:
            extra_fn(rep, U, ent)
        return rep

    def fixed_col(rep, U, ent):
        A2 = np.abs(U) ** 2
        col = sorted(ent["fixed_column_abs2"])
        hits = [j + 1 for j in range(3) if np.max(np.abs(np.sort(A2[:, j]) - col)) < 2e-6]
        rep["e4_fixed_column_abs2"] = ent["fixed_column_abs2"]
        rep["fixed_column_found_in_U_columns"] = hits
        rep["fixed_column_rows_e_mu_tau"] = {f"col{j}": A2[:, j - 1].tolist() for j in hits}

    rep = e4_preset("e4_z7", E4["z7"],
                    "PSL(2,7) Z2-partial survivor G_l = Z7, G_nu = Z2 (results.json z2_partial_PSL). "
                    "E4's own p_value uses 2 dof (theta, phi fitted); p_value here is the 4-dof hand-set formula.",
                    fixed_col)
    presets.append(rep)
    chk("e4_z7_chi2", abs(rep["chi2_pmns"] - 2.1328) < 5e-5 and abs(rep["chi2_pmns"] - rep["e4_reference_chi2"]) < 1e-8,
        f"{rep['chi2_pmns']:.10f} vs E4 {rep['e4_reference_chi2']:.10f}; fixed col in U col {rep['fixed_column_found_in_U_columns']}")

    rep = e4_preset("e4_tm1", E4["tm1"],
                    "PSL(2,7) Z2-partial survivor G_l = Z3, fixed column (2/3,1/6,1/6) = TM1", fixed_col)
    presets.append(rep)
    chk("e4_tm1_chi2", abs(rep["chi2_pmns"] - 2.5407) < 5e-5 and abs(rep["chi2_pmns"] - rep["e4_reference_chi2"]) < 1e-8,
        f"{rep['chi2_pmns']:.10f} vs E4 {rep['e4_reference_chi2']:.10f}; col1 = {np.round(rep['absU2'][0][0], 8)}, "
        f"{np.round(rep['absU2'][1][0], 8)}, {np.round(rep['absU2'][2][0], 8)}")

    rep = e4_preset("e4_tm2", E4["tm2"],
                    "PSL(2,7) Z2-partial survivor G_l = Z3, fixed column (1/3,1/3,1/3) = TM2", fixed_col)
    presets.append(rep)
    col2 = [rep["absU2"][i][1] for i in range(3)]
    chk("e4_tm2_chi2_and_trimaximal_col2",
        abs(rep["chi2_pmns"] - 7.6280) < 5e-5 and max(abs(c - 1 / 3) for c in col2) < 2e-6,
        f"{rep['chi2_pmns']:.10f} vs E4 {rep['e4_reference_chi2']:.10f}; |U_.2|^2 = {[round(c, 9) for c in col2]}")

    def psl_extra(rep, U, ent):
        A2 = np.abs(U) ** 2
        can = np.array(ent["absU2_canonical"])
        rep["e4_absU2_canonical"] = ent["absU2_canonical"]
        rep["absU2_vs_canonical_rows_reversed_maxdiff"] = float(np.max(np.abs(A2 - can[::-1])))
        rep["source_file"] = "out/yukawa.json residual_patterns.PSL (not in results.json)"
        # delta = 180 alternative for comparison: chi2 of the same angles with delta = 180
        Ualt = pdg_U(ent["best"]["s12sq"], ent["best"]["s13sq"], ent["best"]["s23sq"], math.pi)
        rep["absU2_with_delta_180_maxdiff_vs_canonical"] = float(np.max(np.abs(np.abs(Ualt) ** 2 - can[::-1])))

    rep = e4_preset("e4_psl_full_best", E4["psl"],
                    "PSL(2,7) full-residual best lepton pattern G1 = Z3, G2 = Z7, Dirac nu; values taken from "
                    "out/yukawa.json (results.json only stores the count of residual patterns).",
                    psl_extra)
    presets.append(rep)
    chk("e4_psl_full_best_chi2_162.1", abs(rep["chi2_pmns"] - E4["psl"]["chi2"]) < 1e-8,
        f"{rep['chi2_pmns']:.10f} vs E4 {E4['psl']['chi2']:.10f}; |U|^2 vs canonical (rows reversed) "
        f"{rep['absU2_vs_canonical_rows_reversed_maxdiff']:.1e}; in results.json: {E4['psl_in_results']}")

    # ---------------- general checks
    # (a) |O_ij|^2 = cos^2(angle between fixed axis i and rotated axis j), with the rotated axes built
    #     independently by Rodrigues rotations of the basis vectors (no matrix products).
    def rodrigues(v, k, phi):
        k = np.asarray(k, float)
        return v * math.cos(phi) + np.cross(k, v) * math.sin(phi) + k * (k @ v) * (1 - math.cos(phi))

    rng = np.random.default_rng(20261020)
    worst_a = 0.0
    for _ in range(200):
        t12, t13, t23 = rng.uniform(0, math.pi / 2, 3)
        s13p = math.sin(t13) * rng.choice([-1, 1])
        O, _ = cube_O(math.sin(t12), abs(s13p), math.sin(t23), 0.0 if s13p > 0 else math.pi)
        # O = R23 R13 R12 with R12 = Rz(-t12), R13 = Ry(asin s13'), R23 = Rx(-t23)
        t13s = math.asin(s13p)
        for j in range(3):
            v = np.eye(3)[j]
            v = rodrigues(v, [0, 0, 1], -t12)
            v = rodrigues(v, [0, 1, 0], t13s)
            v = rodrigues(v, [1, 0, 0], -t23)
            for i in range(3):
                ang = math.acos(max(-1.0, min(1.0, float(np.eye(3)[i] @ v) / np.linalg.norm(v))))
                worst_a = max(worst_a, abs(math.cos(ang) ** 2 - O[i, j] ** 2))
    chk("a_absO2_equals_cos2_axes", worst_a < 1e-12,
        f"max |cos^2(angle(e_i, O e_j)) - O_ij^2| over 200 random rotations = {worst_a:.2e}")

    # (b) delta = 180 deg: U real and equal to R23 R13(-theta13) R12
    worst_b_im, worst_b = 0.0, 0.0
    for _ in range(200):
        s12, s13, s23 = np.sin(rng.uniform(0, math.pi / 2, 3))
        U = pdg_U_from_sines(s12, s13, s23, math.pi)
        R = r23(s23).real @ r13_real(-s13) @ r12(s12).real
        worst_b_im = max(worst_b_im, float(np.max(np.abs(U.imag))))
        worst_b = max(worst_b, float(np.max(np.abs(U - R))))
    chk("b_delta180_real_equals_R23_R13minus_R12", worst_b < 1e-15 and worst_b_im < 1e-15,
        f"max |Im U| = {worst_b_im:.1e}, max |U - R23 R13(-th13) R12| = {worst_b:.1e}")

    # (c) only |U_mu1|^2, |U_mu2|^2, |U_tau1|^2, |U_tau2|^2 depend on delta
    var = np.zeros((3, 3))
    for _ in range(50):
        s12, s13, s23 = np.sin(rng.uniform(0.05, math.pi / 2 - 0.05, 3))
        stack = np.array([np.abs(pdg_U_from_sines(s12, s13, s23, d)) ** 2
                          for d in np.linspace(0, 2 * math.pi, 73)])
        var = np.maximum(var, stack.max(0) - stack.min(0))
    dep = sorted([(i, j) for i in range(3) for j in range(3) if var[i, j] > 1e-12])
    names = ["e", "mu", "tau"]
    chk("c_delta_dependent_entries", dep == [(1, 0), (1, 1), (2, 0), (2, 1)],
        "delta-dependent: " + ", ".join(f"|U_{names[i]}{j + 1}|^2" for i, j in dep)
        + f"; max variation of the other five = {max(var[i, j] for i in range(3) for j in range(3) if (i, j) not in dep):.1e}")

    # J sign convention: J = c12 s12 c23 s23 c13^2 s13 sin delta
    s12, s13, s23, d = 0.55, 0.15, 0.7, 1.1
    U = pdg_U_from_sines(s12, s13, s23, d)
    Jf = math.sqrt(1 - s12 ** 2) * s12 * math.sqrt(1 - s23 ** 2) * s23 * (1 - s13 ** 2) * s13 * math.sin(d)
    chk("J_formula_sign", abs(extract(U)["J"] - Jf) < 1e-15, f"J = {extract(U)['J']:.12f} vs closed form {Jf:.12f}")

    # extraction round trip for random angles
    worst_rt = 0.0
    for _ in range(200):
        a = rng.uniform(0.01, 0.99, 3)
        d = rng.uniform(0, 2 * math.pi)
        ex = extract(pdg_U(*a, d))
        worst_rt = max(worst_rt, abs(ex["s12sq"] - a[0]), abs(ex["s13sq"] - a[1]), abs(ex["s23sq"] - a[2]),
                       abs((ex["delta"] - d + math.pi) % (2 * math.pi) - math.pi))
    chk("extraction_roundtrip_random", worst_rt < 1e-10, f"max dev {worst_rt:.1e}")

    # cube consistency: O = U whenever delta is 0 or 180 (pmns presets with delta 0/180 or s13 = 0)
    chk("cube_exact_for_real_presets",
        all(p["max_abs_diff_O_vs_U"] < 1e-15 for p in presets if p["id"] in ("none", "tbm", "e4_psl_full_best")),
        {p["id"]: p["max_abs_diff_O_vs_U"] for p in presets if p["id"] in ("none", "tbm", "e4_psl_full_best")})

    # unitarity of every preset
    chk("unitarity_all_presets", max(p["unitarity_err"] for p in presets) < 1e-14,
        f"max |U^dag U - 1| = {max(p['unitarity_err'] for p in presets):.1e}")

    # E4 pull agreement
    e4p = [p for p in presets if p["id"].startswith("e4_")]
    chk("e4_pulls_agree", max(p["max_pull_diff_vs_e4"] for p in e4p) < 1e-8,
        {p["id"]: p["max_pull_diff_vs_e4"] for p in e4p})

    # delta extraction independent cross-check (|U_tau1|^2 route vs quartet route)
    alts = {p["id"]: p.get("delta_alt_tau1_minus_quartet_deg") for p in presets if "delta_alt_tau1_minus_quartet_deg" in p}
    chk("delta_two_routes_agree", all(abs(v) < 1e-6 for v in alts.values()), alts)

    # p-value formula sanity: 4-dof survival function vs numerical integration of chi2_4 pdf
    xs = np.linspace(0, 60, 600001)
    pdf = xs / 4 * np.exp(-xs / 2)
    for x in (2.1328, 7.628):
        m = xs >= x
        num = np.trapezoid(pdf[m], xs[m]) if hasattr(np, "trapezoid") else np.trapz(pdf[m], xs[m])
        chk(f"pvalue4_formula_x={x}", abs(num - pvalue4(x)) < 1e-6, f"closed {pvalue4(x):.8f}, numeric {num:.8f}")

    out = {"presets": presets, "checks": checks,
           "conventions": {"sigma_below_above": SIG, "UTfit": UTFIT}}
    with open(os.path.join(HERE, "crosscheck_mixing.json"), "w") as f:
        json.dump(out, f, indent=1)
    for p in presets:
        print(f"{p['id']:18s} chi2={p['chi2'] if p['chi2'] is None else round(p['chi2'], 6)} "
              f"s12sq={p['s12sq']:.8f} s13sq={p['s13sq']:.8f} s23sq={p['s23sq']:.8f} "
              f"delta={p['delta_deg']} J={p['J']:.6e} cube={p['cube_delta_deg']} dO={p['max_abs_diff_O_vs_U']:.4e} "
              f"p={p['p_value']} e4={p['e4_reference_chi2']}")
    for c in checks:
        print(("PASS " if c["holds"] else "FAIL ") + c["id"] + ": " + c["value"])


if __name__ == "__main__":
    main()
