#!/usr/bin/env python3
"""
ls_leg2.py -- blind second leg of LS_PREREG.md (lattice-spacing bound, October 7, 2026).

Written from LS_PREREG.md alone (no leg-1 code or numbers, no git history, no reports).
Implements LS_PREREG.md sections 1-9:
  s1  constants, md5 assertion of the four inputs (+ a soft check of the restated values),
      D_lt(z) by two independent quadratures (QUADPACK, tanh-sinh @40 digits) plus a
      fixed Gauss-Legendre rule and the analytic flat-LCDM closed form;
  s2  d_max = [tau_r / (Q_T^d k^4 D)]^(1/3), Q_T^d = Q_T^a / 8, validity checks (VOID logic),
      lattice-continuum and RVE reports;
  s3  every reading (E x D x k) x every configuration for arms A0-A4, bound of record,
      union edge, reference reading, reported-only readings, anchor reproduction (halt-on-fail),
      combined bound, decisive arm, R4 variants;
  s4  a_max(N) table;
  s5  texture bound t_max and the statistical-texture report;
  s6  dispersion bound a_max^disp, with an independent numerical check of the conversion;
  s7  combine a_max(N) = min(d_comb/N, a_max^disp);
  s8  EMPTY_P / EMPTY_D flags, N_P, N_D, placement of l_P and the declared band, R4 x10 variant;
  s9  output in the schema requested for the two-leg comparison.

Outputs (written next to this script):
  ls_leg2.json         -- the result, in the schema requested by the caller
  ls_leg2_extras.json  -- every other reported quantity and check
"""
import hashlib
import json
import math
import os
import re
import sys

import mpmath as mp
import numpy as np
from scipy import integrate

mp.mp.dps = 40  # working precision of the independent high-precision path

OUTDIR = os.path.dirname(os.path.abspath(__file__))
REPO = "/home/claude/gifgaf0.github.io"

# ============================================================================ s1 constants
HBAR = 1.054571817e-34           # J s
C = 299792458.0                  # m s^-1
QE = 1.602176634e-19             # C (= J per eV)
PC = 3.0856775814913673e16       # m
L_P = 1.616255e-35               # m   (CODATA 2018)
E_PL_GEV = 1.220890e19           # GeV (CODATA 2018)
H_PLANCK = 2.0 * math.pi * HBAR  # J s, h = 2 pi hbar (used for lambda = h c / E)
HBARC = HBAR * C                 # J m
MPC = 1.0e6 * PC
GPC = 1.0e9 * PC
JULIAN_GYR_S = 365.25 * 86400.0 * 1.0e9   # only for an informational lookback time

H0_KMS_MPC = 67.4
OMEGA_M = 0.315
TAU_R = 1.0                      # P-TRANS threshold, amplitude convention
W_EM_UNION = 3.7641664288e-33    # m, anchor of record
ANCHOR_TOL = 1.0e-7
DLT_TOL = 1.0e-10
BAND_LO, BAND_HI = 1.899e-34, 7.588e-34   # m, declared lattice band
NS = (20, 100, 1000)

# same constants for the independent mpmath path (exact decimal inputs)
MP_HBAR = mp.mpf("1.054571817e-34")
MP_C = mp.mpf(299792458)
MP_QE = mp.mpf("1.602176634e-19")
MP_PC = mp.mpf("3.0856775814913673e16")

INPUTS = [  # path relative to the repository root, md5, what is read
    ("gci1_gate/embeds/anchors_G_CI1_SEALED.md", "dd8fe2d364624750201ad9c9ffef575c", "anchor of record"),
    ("gci1_gate/ci1_phase2_cc.json", "f79113b7664addc9b1d96893aa883cbf", "fluctuation factor"),
    ("gs2c1_gate/cc_phase4.json", "4ebd0db2e2a494db3e66d35f90df7422", "lattice dispersion"),
    ("gmscs2_gate/g_mscs2_chatleg_checkpoint.json", "1c5b6b59829d2a6b9ae2b1a7a016832d", "texture birefringence"),
]

CONFIGS = ("hex:step", "hex:gem8", "cubic:step", "cubic:gem8")
QTA = {"hex:step": 0.035190738866, "hex:gem8": 0.050020548479,          # G-CI1 Phase 2 (of record)
       "cubic:step": 0.054077628247, "cubic:gem8": 0.075494302071}
QTA_BANKED = {"hex:step": 0.03519074, "hex:gem8": 0.05002055,
              "cubic:step": 0.05407763, "cubic:gem8": 0.0754943}
EPS_T = {"hex:step": 0.091333902531, "hex:gem8": 0.10912048635,
         "cubic:step": 0.1303772679, "cubic:gem8": 0.15743361577}
A2 = {"GK": -0.0132447218611613, "GM": -0.020633674570357804}   # per (ka)^2, a = p6m lattice constant
A2_CI = {"GK": 3.21e-5, "GM": 3.55e-5}
B1 = {"hex_step|a": 0.01624085410723511, "hex_step|b": 0.016241797577228063,
      "hex_gem8|a": 0.01817488251117739, "hex_gem8|b": 0.018174297109340813,
      "cubic_step|001": -0.03789870339598654, "cubic_step|111": -0.03789870339598654,
      "cubic_gem8|001": -0.04548125222774924, "cubic_gem8|111": -0.04548125222774924}
DN_MAX = {"R-T1": 2.0e-37, "R-T2": 4.0e-32, "R-T0": 2.0e-38}
C_TEX = {"hex": 9.0, "cubic": 21.0 / 4.0}   # 1/<P4^2> (hex), 1/<K4~^2> (cubic)

# ============================================================================ s3 arms
# energies in eV, distances in pc, kept as decimal strings so the float and mpmath paths
# start from identical exact inputs.  D = None means D_lt(z) (cosmological arm).
ARMS = {
    "A0": dict(src="1ES 1101-232, H.E.S.S. (Nature 440, 1018), TR-4 anchor", z="0.186",
               E_ref="2.916e12", E_alt="0.733e12", D_ref=None, D_alt=None),
    "A1": dict(src="Crab, LHAASO KM2A 1.12+-0.09 PeV; VLBI 1.90 (+0.22/-0.18) kpc", z="0",
               E_ref="1.12e15", E_alt="0.94e15", D_ref="1900", D_alt="1540"),
    "A2": dict(src="Cygnus, LHAASO Sci. Bull. 69, 449 (2024)", z="0",
               E_ref="2.5e15", E_alt="1.0e15", D_ref="1400", D_alt="1250"),
    "A3": dict(src="GRB 221009A, LHAASO KM2A (Sci. Adv. 9, eadj2778)", z="0.151",
               E_ref="12.5e12", E_alt="7.7e12", D_ref=None, D_alt=None),
    "A4": dict(src="Mrk 501, HEGRA 1997 (A&A 349, 11)", z="0.034",
               E_ref="21.45e12", E_alt="16e12", D_ref=None, D_alt=None),
}
# readings reported only (never enter a minimum): (arm, label, overrides)
REPORTED_ONLY = [
    ("A3", "E=17.8 TeV (log-parabola)", {"E": "17.8e12"}),
    ("A3", "E=13 TeV (abstract)", {"E": "13e12"}),
    ("A2", "D=1.6 kpc (Cyg OB2 Gaia)", {"D": "1600"}),
    ("A1", "D=2.0 kpc (classic)", {"D": "2000"}),
]


def rel(a, b):
    return abs(a - b) / abs(b)


# ============================================================================ s1 input checks
def md5_check():
    out = []
    for relpath, md5, what in INPUTS:
        p = os.path.join(REPO, relpath)
        if not os.path.isfile(p):
            out.append(dict(file=relpath, what=what, expected=md5, found=None, ok=None))
            continue
        with open(p, "rb") as fh:
            h = hashlib.md5(fh.read()).hexdigest()
        out.append(dict(file=relpath, what=what, expected=md5, found=h, ok=(h == md5)))
        assert h == md5, f"md5 mismatch for {relpath}: {h} != {md5}"
    return out


def _numbers(obj, acc):
    if obj is None or isinstance(obj, bool):
        return
    if isinstance(obj, (int, float)):
        if math.isfinite(float(obj)):
            acc.append(float(obj))
        return
    if isinstance(obj, str):
        try:
            v = float(obj)
            if math.isfinite(v):
                acc.append(v)
        except ValueError:
            pass
        return
    if isinstance(obj, dict):
        for v in obj.values():
            _numbers(v, acc)
    elif isinstance(obj, (list, tuple)):
        for v in obj:
            _numbers(v, acc)


def value_crosscheck():
    """Soft check: does each restated value occur (|.| match) in its input file?  Report only;
    the computation uses the values restated in LS_PREREG.md, as instructed."""
    def nearest(nums, target):
        if not nums:
            return None
        best = min(nums, key=lambda x: abs(abs(x) - abs(target)))
        return abs(abs(best) - abs(target)) / abs(target)

    rep = {}
    def load(relpath):
        p = os.path.join(REPO, relpath)
        if not os.path.isfile(p):
            return None
        with open(p) as fh:
            obj = json.load(fh)
        acc = []
        _numbers(obj, acc)
        return acc

    nums = load("gci1_gate/ci1_phase2_cc.json")
    if nums is not None:
        rep["ci1_phase2_cc.json"] = {
            **{f"Q_T_a {c}": nearest(nums, v) for c, v in QTA.items()},
            **{f"Q_T_a_banked {c}": nearest(nums, v) for c, v in QTA_BANKED.items()},
            **{f"eps_T {c}": nearest(nums, v) for c, v in EPS_T.items()},
        }
    nums = load("gs2c1_gate/cc_phase4.json")
    if nums is not None:
        rep["cc_phase4.json"] = {
            **{f"a2 {k}": nearest(nums, v) for k, v in A2.items()},
            **{f"a2_CI {k}": nearest(nums, v) for k, v in A2_CI.items()},
        }
    nums = load("gmscs2_gate/g_mscs2_chatleg_checkpoint.json")
    if nums is not None:
        rep["g_mscs2_chatleg_checkpoint.json"] = {f"b1 {k}": nearest(nums, v) for k, v in B1.items()}
    p = os.path.join(REPO, "gci1_gate/embeds/anchors_G_CI1_SEALED.md")
    if os.path.isfile(p):
        with open(p, encoding="utf-8", errors="replace") as fh:
            txt = fh.read()
        rep["anchors_G_CI1_SEALED.md (string present)"] = {
            s: bool(re.search(re.escape(s), txt)) for s in ("2.916", "0.733", "0.186", "3.7641664288")}
    return rep


# ============================================================================ s1 cosmology
H0_SI = H0_KMS_MPC * 1.0e3 / MPC     # s^-1
DH = C / H0_SI                       # Hubble distance c/H0, m


def _integrand(zp):
    return 1.0 / ((1.0 + zp) * math.sqrt(OMEGA_M * (1.0 + zp) ** 3 + 1.0 - OMEGA_M))


def dlt_quadpack(z):
    """Quadrature 1: QUADPACK adaptive Gauss-Kronrod (scipy.integrate.quad), double precision."""
    val, err = integrate.quad(_integrand, 0.0, z, epsabs=0.0, epsrel=1e-13, limit=200)
    return DH * val, DH * err


def dlt_gauss_legendre(z, n=48):
    """Fixed-order Gauss-Legendre rule (extra check)."""
    x, w = np.polynomial.legendre.leggauss(n)
    zp = 0.5 * z * (x + 1.0)
    f = 1.0 / ((1.0 + zp) * np.sqrt(OMEGA_M * (1.0 + zp) ** 3 + 1.0 - OMEGA_M))
    return DH * 0.5 * z * float(np.sum(w * f))


def _dh_mp():
    return MP_C * mp.mpf(10) ** 6 * MP_PC / (mp.mpf("67.4") * 1000)


def dlt_tanh_sinh(z_str):
    """Quadrature 2 (independent): tanh-sinh (mpmath) at 40 significant digits, exact decimal inputs."""
    om = mp.mpf("0.315")
    f = lambda t: 1 / ((1 + t) * mp.sqrt(om * (1 + t) ** 3 + 1 - om))
    val, err = mp.quad(f, [0, mp.mpf(z_str)], method="tanh-sinh", error=True)
    return _dh_mp() * val, _dh_mp() * err


def dlt_closed_form(z_str):
    """Analytic flat matter+Lambda lookback time: t(a) = 2/(3 H0 sqrt(OL)) asinh(sqrt(OL/Om) a^(3/2))."""
    om = mp.mpf("0.315")
    ol = 1 - om
    r = mp.sqrt(ol / om)
    x = 2 / (3 * mp.sqrt(ol)) * (mp.asinh(r) - mp.asinh(r * (1 + mp.mpf(z_str)) ** mp.mpf("-1.5")))
    return _dh_mp() * x


# ============================================================================ s2 scattering
def k_float(E_eV, z, onepz):
    k = E_eV * QE / HBARC
    return k * (1.0 + z) if onepz else k


def k_mp(E_str, z_str, onepz):
    k = mp.mpf(E_str) * MP_QE / (MP_HBAR * MP_C)
    return k * (1 + mp.mpf(z_str)) if onepz else k


def dmax_float(qta, k, D, tau=TAU_R):
    qtd = qta / 8.0                      # Q_T^d = Q_T^a / 8 (erratum H-6)
    return math.cbrt(tau / (qtd * k ** 4 * D))


def dmax_mp(qta, k, D, tau=TAU_R):
    qtd = mp.mpf(repr(qta)) / 8
    return mp.cbrt(mp.mpf(tau) / (qtd * k ** 4 * D))


def validity(cfg, k_max, d_rec):
    x = k_max * d_rec
    qtd = QTA[cfg] / 8.0
    checks = {
        "x=k*d_max<=1e-4": [x, x <= 1.0e-4],
        "eps_T*x<=1": [EPS_T[cfg] * x, EPS_T[cfg] * x <= 1.0],
        "Q_T(x)*x^3<=0.10 (Q_T^d)": [qtd * x ** 3, qtd * x ** 3 <= 0.10],
        "Q_T(x)*x^3<=0.10 (Q_T^a, stricter)": [QTA[cfg] * x ** 3, QTA[cfg] * x ** 3 <= 0.10],
        "eps_T^2<=0.10": [EPS_T[cfg] ** 2, EPS_T[cfg] ** 2 <= 0.10],
    }
    return x, checks, all(v[1] for v in checks.values())


# ============================================================================ s6 dispersion
def a_disp(E_qg_GeV, a2):
    """a_max^disp = hbar c / (E_QG,2 sqrt(2|a2|))."""
    return HBARC / (E_qg_GeV * 1.0e9 * QE * math.sqrt(2.0 * abs(a2)))


def check_dispersion_conversion(E_qg_GeV, a2, a_val):
    """Independent numerical check of the conversion, at 60 digits:
    put the lattice dispersion E = hbar c k [1 + a2 (k a)^2] with a = a_val, solve for k at test
    photon energies, read off the E_QG implied by LHAASO's E^2 = p^2 c^2 [1 - (E/E_QG)^2] (s=+1),
    and compare with the input E_QG; also compare 1 - v_g/c from the two forms (numerical d/dk)."""
    out = {}
    with mp.workdps(60):
        hbarc = MP_HBAR * MP_C
        Eqg = mp.mpf(repr(E_qg_GeV)) * mp.mpf(10) ** 9 * MP_QE
        a = mp.mpf(repr(a_val))
        A = mp.mpf(repr(a2))
        for Et_eV in ("1e12", "1e15", "1e17"):
            Et = mp.mpf(Et_eV) * MP_QE
            k = mp.findroot(lambda kk: hbarc * kk * (1 + A * (kk * a) ** 2) - Et, Et / hbarc)
            pc = hbarc * k
            Eqg_implied = Et / mp.sqrt(1 - (Et / pc) ** 2)
            # group-velocity form: lattice v_g = d omega/dk; LHAASO E(p) = pc/sqrt(1+(pc/E_QG)^2)
            vg_lat = mp.diff(lambda kk: MP_C * kk * (1 + A * (kk * a) ** 2), k)
            v_lh = mp.diff(lambda pp: pp / mp.sqrt(1 + (pp / Eqg) ** 2), pc) * MP_C
            dv_lat = 1 - vg_lat / MP_C
            dv_lh = 1 - v_lh / MP_C
            out[Et_eV + " eV"] = dict(
                ka=float(k * a),
                Eqg_implied_over_input_minus_1=float(Eqg_implied / Eqg - 1),
                lattice_3a2ka2_over_LHAASO_1p5_EoverEqg2_minus_1=float(
                    (3 * abs(A) * (k * a) ** 2) / (mp.mpf(3) / 2 * (Et / Eqg) ** 2) - 1),
                dv_lattice_numeric_over_dv_LHAASO_numeric_minus_1=float(dv_lat / dv_lh - 1),
            )
    return out


# ============================================================================ main
def main():
    extras = {"spec": "LS_PREREG.md (October 7, 2026), leg 2 (blind)"}

    # ---------------- s1 inputs
    extras["md5"] = md5_check()
    extras["restated_value_crosscheck_min_rel_diff"] = value_crosscheck()

    # ---------------- s1 cosmology
    dlt, dlt_rep = {}, {}
    for zs in ("0.186", "0.151", "0.034"):
        z = float(zs)
        ts, ts_err = dlt_tanh_sinh(zs)
        qp, qp_err = dlt_quadpack(z)
        gl = dlt_gauss_legendre(z)
        cf = dlt_closed_form(zs)
        ts_f = float(ts)
        r_qp, r_gl, r_cf = rel(qp, ts_f), rel(gl, ts_f), float(abs(cf - ts) / ts)
        assert r_qp <= DLT_TOL, (zs, r_qp)
        assert r_gl <= DLT_TOL, (zs, r_gl)
        assert r_cf <= DLT_TOL, (zs, r_cf)
        dlt[zs] = ts_f
        dlt_rep[zs] = dict(
            D_lt_m_tanh_sinh_40dps=ts_f, tanh_sinh_err_est_m=float(ts_err),
            D_lt_m_quadpack=qp, quadpack_err_est_m=qp_err,
            D_lt_m_gauss_legendre48=gl, D_lt_m_closed_form=float(cf),
            rel_quadpack_vs_tanh_sinh=r_qp, rel_gauss_legendre_vs_tanh_sinh=r_gl,
            rel_closed_form_vs_tanh_sinh=r_cf,
            D_lt_Mpc=ts_f / MPC, lookback_Gyr_julian=ts_f / C / JULIAN_GYR_S)
    extras["D_lt"] = dict(hubble_distance_m=DH, H0_s=H0_SI, per_z=dlt_rep)
    dlt_mp = {zs: dlt_tanh_sinh(zs)[0] for zs in dlt}

    # ---------------- s3 rule consistency (the alt rules stated in the table)
    extras["alt_rule_checks"] = {
        "A1 E_alt = E_ref - 2*0.09 PeV": abs((1.12 - 2 * 0.09) - 0.94) < 1e-12,
        "A1 D_alt = D_ref - 2*0.18 kpc": abs((1.90 - 2 * 0.18) - 1.54) < 1e-12,
        "A2 D_alt = D_ref - 0.15 kpc": abs((1.40 - 0.15) - 1.25) < 1e-12,
        "A3 E_alt = E_ref - 2*2.4 TeV": abs((12.5 - 2 * 2.4) - 7.7) < 1e-12,
    }
    assert all(extras["alt_rule_checks"].values())

    # ---------------- s2/s3 every arm x reading x configuration
    arms_json, arms_ext = {}, {}
    mp_dev_max = 0.0
    for aid, arm in ARMS.items():
        zs = arm["z"]
        z = float(zs)
        cosmo = z > 0
        D_f = {t: (dlt[zs] if cosmo else float(arm[t]) * PC) for t in ("D_ref", "D_alt")}
        D_m = {t: (dlt_mp[zs] if cosmo else mp.mpf(arm[t]) * MP_PC) for t in ("D_ref", "D_alt")}
        ktags = ("k_obs", "k_1pz") if cosmo else ("k_obs",)
        readings, dmap, kvals = [], {}, []
        for Et in ("E_ref", "E_alt"):
            for Dt in ("D_ref", "D_alt"):
                for kt in ktags:
                    onepz = kt == "k_1pz"
                    k = k_float(float(arm[Et]), z, onepz)
                    km = k_mp(arm[Et], zs, onepz)
                    kvals.append(k)
                    dm = {}
                    for cfg in CONFIGS:
                        d = dmax_float(QTA[cfg], k, D_f[Dt])
                        dmp = dmax_mp(QTA[cfg], km, D_m[Dt])
                        mp_dev_max = max(mp_dev_max, float(abs(d - dmp) / dmp))
                        dm[cfg] = d
                    readings.append({"E_tag": Et, "D_tag": Dt, "k_tag": kt, "d_max": dm})
                    dmap[(Et, Dt, kt)] = dm
        k_max = max(kvals)
        # bound of record per configuration = largest d_max over readings; assert = (E_alt, D_alt, k_obs)
        rec_cfg, chk, void = {}, {}, {}
        for cfg in CONFIGS:
            mx = max(r["d_max"][cfg] for r in readings)
            assert dmap[("E_alt", "D_alt", "k_obs")][cfg] == mx, (aid, cfg, "monotonicity")
            rec_cfg[cfg] = mx
            x, checks, ok = validity(cfg, k_max, mx)
            void[cfg] = not ok
            lam_min = 2.0 * math.pi / k_max
            chk[cfg] = dict(
                x=x, checks=checks, VOID=not ok,
                lattice_continuum_k_dmax_over_N={str(N): k_max * mx / N for N in NS},
                RVE_grains_per_wavelength_cube_at_lambda_min=(lam_min / mx) ** 3)
        live = [c for c in CONFIGS if not void[c]]
        assert live, (aid, "all cells VOID")
        record_union = max(rec_cfg[c] for c in live)
        union_cfg = max(live, key=lambda c: rec_cfg[c])
        assert union_cfg == "hex:step", (aid, union_cfg)
        ref = dmap[("E_ref", "D_ref", "k_obs")]
        reference_union = max(ref[c] for c in live)
        assert max(live, key=lambda c: ref[c]) == "hex:step"
        arms_json[aid] = {"readings": readings, "record_union": record_union,
                          "reference_union": reference_union}
        arms_ext[aid] = dict(
            source=arm["src"], z=z, E_ref_eV=float(arm["E_ref"]), E_alt_eV=float(arm["E_alt"]),
            D_ref_m=D_f["D_ref"], D_alt_m=D_f["D_alt"], k_max_per_m=k_max,
            bound_of_record_per_config=rec_cfg, union_config=union_cfg,
            reference_per_config=ref, validity=chk,
            record_union_in_lP=record_union / L_P, reference_union_in_lP=reference_union / L_P)
    extras["float_vs_mpmath_dmax_max_rel_dev"] = mp_dev_max
    assert mp_dev_max < 1e-12
    extras["arms"] = arms_ext

    # reported-only readings (never in a minimum)
    rep_only = []
    for aid, label, ov in REPORTED_ONLY:
        arm = ARMS[aid]
        zs = arm["z"]
        z = float(zs)
        cosmo = z > 0
        Elist = [("override", ov["E"])] if "E" in ov else [("E_ref", arm["E_ref"]), ("E_alt", arm["E_alt"])]
        for Et, Es in Elist:
            D = float(ov["D"]) * PC if "D" in ov else (dlt[zs] if cosmo else float(arm["D_ref"]) * PC)
            for kt in (("k_obs", "k_1pz") if cosmo else ("k_obs",)):
                k = k_float(float(Es), z, kt == "k_1pz")
                rep_only.append(dict(arm=aid, reading=label, E_tag=Et, E_eV=float(Es), D_m=D, k_tag=kt,
                                     d_max={c: dmax_float(QTA[c], k, D) for c in CONFIGS}))
    extras["reported_only_readings"] = rep_only

    # ---------------- s3 anchor reproduction (halt-on-fail)
    a0 = ARMS["A0"]
    k_a0 = k_float(float(a0["E_alt"]), 0.186, False)
    d_a0_p2 = dmax_float(QTA["hex:step"], k_a0, dlt["0.186"])
    d_a0_bk = dmax_float(QTA_BANKED["hex:step"], k_a0, dlt["0.186"])
    dev_p2, dev_bk = rel(d_a0_p2, W_EM_UNION), rel(d_a0_bk, W_EM_UNION)
    extras["anchor_reproduction"] = dict(
        target_W_EM_union_m=W_EM_UNION, A0_hexstep_record_phase2_m=d_a0_p2,
        A0_hexstep_record_banked_m=d_a0_bk, rel_dev_phase2=dev_p2, rel_dev_banked=dev_bk,
        tolerance=ANCHOR_TOL, PASS=(dev_p2 <= ANCHOR_TOL and dev_bk <= ANCHOR_TOL))
    assert d_a0_p2 == arms_json["A0"]["record_union"]
    if not extras["anchor_reproduction"]["PASS"]:
        print(json.dumps(extras["anchor_reproduction"], indent=2))
        sys.exit("HALT: anchor reproduction failed")

    # ---------------- s3 combined bound
    unions = {aid: arms_json[aid]["record_union"] for aid in ARMS}
    decisive = min(unions, key=unions.get)
    d_comb = unions[decisive]
    second = sorted(unions.values())[1]
    # R4 band: tau_r x10 / x0.1 recomputed directly on the decisive arm's record reading
    darm = ARMS[decisive]
    D_dec = dlt[darm["z"]] if float(darm["z"]) > 0 else float(darm["D_alt"]) * PC
    k_dec = k_float(float(darm["E_alt"]), float(darm["z"]), False)
    r4_hi = dmax_float(QTA["hex:step"], k_dec, D_dec, tau=10.0)
    r4_lo = dmax_float(QTA["hex:step"], k_dec, D_dec, tau=0.1)
    assert rel(r4_hi, d_comb * 10 ** (1 / 3)) < 1e-12 and rel(r4_lo, d_comb * 10 ** (-1 / 3)) < 1e-12
    extras["combined"] = dict(
        d_comb_m=d_comb, decisive_arm=decisive, d_comb_in_lP=d_comb / L_P,
        runner_up_over_d_comb=second / d_comb, record_unions_m=unions,
        R4_x10_m=d_comb * 10 ** (1 / 3), R4_x0p1_m=d_comb * 10 ** (-1 / 3),
        R4_x10_direct_tau10_m=r4_hi, R4_x0p1_direct_tau0p1_m=r4_lo,
        intensity_convention_2alphaD_le_1_m=d_comb * 2 ** (-1 / 3))

    # ---------------- s6 dispersion
    EQG = {"6.9e11GeV": 6.9e11, "6e-8EPl": 6e-8 * E_PL_GEV}
    disp = {f"{ek}|{ak}": a_disp(ev, A2[ak]) for ek, ev in EQG.items() for ak in ("GK", "GM")}
    disp_record_key = "6.9e11GeV|GK"
    assert max(disp, key=disp.get) == disp_record_key   # the permissive reading is the largest
    a_disp_rec = disp[disp_record_key]
    extras["dispersion"] = dict(
        values_m=disp, values_in_lP={k: v / L_P for k, v in disp.items()},
        record_key=disp_record_key, E_QG_GeV=EQG,
        a2_CI_band_record_m=[a_disp(6.9e11, A2["GK"] - A2_CI["GK"]), a_disp(6.9e11, A2["GK"] + A2_CI["GK"])],
        conversion_check={k: check_dispersion_conversion(EQG[k.split("|")[0]], A2[k.split("|")[1]], v)
                          for k, v in disp.items()})

    # ---------------- s5 texture
    tex = {r: {k: dn / abs(b) for k, b in B1.items()} for r, dn in DN_MAX.items()}
    head_key = min(B1, key=lambda k: abs(B1[k]))
    fam_key = {f: min((k for k in B1 if k.startswith(f)), key=lambda k: abs(B1[k])) for f in ("hex", "cubic")}
    lam100 = H_PLANCK * C / (1.0e5 * QE)      # lambda = h c / E at E = 100 keV
    V_F = math.pi * lam100 * GPC ** 2 / 6.0   # first Fresnel volume, D = 1 Gpc
    stat = {}
    for dlab, d in (("d=3.7641664288e-33", W_EM_UNION), ("d=d_comb", d_comb)):
        for fam in ("hex", "cubic"):
            t = tex["R-T1"][fam_key[fam]]
            M_min = C_TEX[fam] / t ** 2
            M_F = V_F / d ** 3
            sig = math.sqrt(C_TEX[fam] / M_F)
            stat[f"{dlab}|{fam}"] = dict(
                b1_key=fam_key[fam], t_max_RT1=t, c=C_TEX[fam], M_min=M_min,
                L_min_m=d * M_min ** (1 / 3), lambda_100keV_m=lam100, V_F_m3=V_F, M_Fresnel=M_F,
                sigma_t_Fresnel=sig, t_max_over_sigma_t=t / sig)
    extras["texture"] = dict(headline_key=head_key, headline_t_max={r: tex[r][head_key] for r in DN_MAX},
                             per_family_key=fam_key, statistical_texture=stat)

    # ---------------- s2 restatement c_geo (reported, not used)
    extras["c_geo"] = {c: QTA[c] / (8.0 * EPS_T[c] ** 2) for c in CONFIGS}

    # ---------------- s7 combine, s8 flags
    a_max_N = {str(N): min(d_comb / N, a_disp_rec) for N in NS}
    EMPTY_P = {n: v < L_P for n, v in a_max_N.items()}
    EMPTY_D = {n: v < BAND_LO for n, v in a_max_N.items()}

    def placement(a):
        return dict(a_max_m=a, a_max_in_lP=a / L_P, lP_over_a_max=L_P / a,
                    band_lo_over_a_max=BAND_LO / a, band_hi_over_a_max=BAND_HI / a,
                    EMPTY_P=a < L_P, EMPTY_D=a < BAND_LO,
                    lP_position="above a_max" if L_P > a else "at/below a_max",
                    band_position=("entirely above a_max" if BAND_LO > a else
                                   ("straddles a_max" if BAND_HI > a else "entirely below a_max")))

    table = {}
    for aid in ARMS:
        d = arms_json[aid]["record_union"]
        table[aid] = dict(N_P=d / L_P, N_D=d / BAND_LO,
                          per_N={str(N): placement(min(d / N, a_disp_rec)) for N in NS},
                          d_over_N_m={str(N): d / N for N in NS})
    r4x10 = d_comb * 10 ** (1 / 3)
    table["combined"] = dict(N_P=d_comb / L_P, N_D=d_comb / BAND_LO,
                             per_N={str(N): placement(a_max_N[str(N)]) for N in NS})
    table["combined_R4x10"] = dict(N_P=r4x10 / L_P, N_D=r4x10 / BAND_LO,
                                   per_N={str(N): placement(min(r4x10 / N, a_disp_rec)) for N in NS})
    extras["table_s4_s8"] = table
    extras["second_leg_trigger_EMPTY_at_N20"] = EMPTY_P["20"] or EMPTY_D["20"]

    result = {
        "D_lt_m": dict(dlt),
        "arms": arms_json,
        "combined": {"d_comb": d_comb, "decisive_arm": decisive},
        "a_max_N_m": a_max_N,
        "EMPTY_P": EMPTY_P,
        "EMPTY_D": EMPTY_D,
        "dispersion_m": disp,
        "texture_t_max": tex,
    }
    with open(os.path.join(OUTDIR, "ls_leg2.json"), "w") as fh:
        json.dump(result, fh, indent=2)
        fh.write("\n")
    with open(os.path.join(OUTDIR, "ls_leg2_extras.json"), "w") as fh:
        json.dump(extras, fh, indent=2, default=str)
        fh.write("\n")
    print(json.dumps(result, indent=2))
    return result, extras


if __name__ == "__main__":
    main()
