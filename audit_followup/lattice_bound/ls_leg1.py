#!/usr/bin/env python3
"""ls_leg1.py -- lattice-spacing bound, leg 1 (per LS_PREREG.md, locked at 65404f5).

Computes, in order: the anchor reproduction; d_max on every photon arm, reading and
configuration; the per-arm bound of record and the combined bound; the a_max(N) table
(metres and Planck-length units); the texture bound and the random-grain statistical
texture; the dispersion bound; the combination. Writes ls_leg1.json.

It does NOT evaluate EMPTY flags or compare with l_P or the declared band
(LS_PREREG §8: that is ls_compare.py, written after this output exists).
"""
import hashlib
import json
import math
import os
import re
import sys

from scipy.integrate import quad

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
HERE = os.path.dirname(os.path.abspath(__file__))

INPUTS = {
    "anchor": ("gci1_gate/embeds/anchors_G_CI1_SEALED.md", "dd8fe2d364624750201ad9c9ffef575c"),
    "phase2": ("gci1_gate/ci1_phase2_cc.json", "f79113b7664addc9b1d96893aa883cbf"),
    "phase4": ("gs2c1_gate/cc_phase4.json", "4ebd0db2e2a494db3e66d35f90df7422"),
    "b1": ("gmscs2_gate/g_mscs2_chatleg_checkpoint.json", "1c5b6b59829d2a6b9ae2b1a7a016832d"),
    "prereg": ("audit_followup/lattice_bound/LS_PREREG.md", "ea6651ce6b1b0c480476c8b506bc0d99"),
}


def md5(path):
    with open(path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()


for key, (rel, want) in INPUTS.items():
    got = md5(os.path.join(REPO, rel))
    if got != want:
        sys.exit("HALT: md5 mismatch on %s: %s != %s" % (rel, got, want))

# ---------------- constants (LS_PREREG §1) ----------------
HBAR = 1.054571817e-34
C = 299792458.0
E_CH = 1.602176634e-19
PC = 3.0856775814913673e16
KPC, MPC, GPC = 1e3 * PC, 1e6 * PC, 1e9 * PC
LP = 1.616255e-35
EPL_GEV = 1.220890e19
H0 = 67.4e3 / MPC
OM = 0.315
HBARC_EVM = HBAR * C / E_CH          # eV m
HC_EVM = 2 * math.pi * HBARC_EVM


def k_of_E(E_eV):
    return E_eV * E_CH / (HBAR * C)


def Hz(z):
    return H0 * math.sqrt(OM * (1 + z) ** 3 + 1 - OM)


def d_lt_quad(z):
    v, err = quad(lambda zp: 1.0 / ((1 + zp) * Hz(zp)), 0.0, z, epsabs=0.0, epsrel=1e-13, limit=200)
    return C * v


def d_lt_simpson_log(z, n):
    # u = ln(1+z'), dz' = (1+z') du  =>  integrand 1/H(e^u - 1) du
    U = math.log1p(z)
    h = U / n
    s = 0.0
    for i in range(n + 1):
        u = i * h
        f = 1.0 / Hz(math.expm1(u))
        w = 1 if i in (0, n) else (4 if i % 2 else 2)
        s += w * f
    return C * s * h / 3.0


D_LT = {}


def d_lt(z):
    if z == 0:
        return None
    if z not in D_LT:
        q = d_lt_quad(z)
        s1, s2 = d_lt_simpson_log(z, 2000), d_lt_simpson_log(z, 4000)
        gate = abs(s1 - s2) / abs(s2)
        cross = abs(q - s2) / abs(q)
        if gate > 1e-10 or cross > 1e-10:
            sys.exit("HALT: D_lt gate at z=%s (doubling %.2e, cross %.2e)" % (z, gate, cross))
        D_LT[z] = {"m": q, "Mpc": q / MPC, "simpson_doubling": gate, "quad_vs_simpson": cross}
    return D_LT[z]["m"]


# ---------------- inputs ----------------
anchor_txt = open(os.path.join(REPO, INPUTS["anchor"][0]), encoding="utf-8").read()
tr4 = [ln for ln in anchor_txt.splitlines() if "TR-4" in ln and "1101-232" in ln]
if len(tr4) != 1:
    sys.exit("HALT: TR-4 row not unique in the anchor file")
tr4 = tr4[0]
for needle in ("z = 0.186", "E_ref = 2.916e12 eV", "E_alt = 7.33e11 eV", "tau_r = 1.0", "BOTH E readings (R3)", "D_ref = D_lt(0.186)"):
    if needle not in tr4:
        sys.exit("HALT: anchor TR-4 row lacks %r" % needle)
conv = [ln for ln in anchor_txt.splitlines() if "CONV" in ln]
r2_ok = any("R2" in ln and "(1+z)" in ln for ln in conv)

ph2 = json.load(open(os.path.join(REPO, INPUTS["phase2"][0])))
CFGS = ["hex:step", "hex:gem8", "cubic:step", "cubic:gem8"]
QA = {c: ph2["configs"][c]["Q_T_a"] for c in CFGS}
QA_BANKED = {c: ph2["configs"][c]["Q_T_a_banked"] for c in CFGS}
EPS = {c: ph2["configs"][c]["eps_T"] for c in CFGS}
PRE_QA = {"hex:step": 0.035190738866, "hex:gem8": 0.050020548479, "cubic:step": 0.054077628247, "cubic:gem8": 0.075494302071}
PRE_EPS = {"hex:step": 0.091333902531, "hex:gem8": 0.10912048635, "cubic:step": 0.1303772679, "cubic:gem8": 0.15743361577}
for c in CFGS:
    assert abs(QA[c] - PRE_QA[c]) / PRE_QA[c] < 1e-10, c
    assert abs(EPS[c] - PRE_EPS[c]) / PRE_EPS[c] < 1e-10, c

ph4 = json.load(open(os.path.join(REPO, INPUTS["phase4"][0])))
A2 = {"GK": ph4["directions"]["GK"]["a2"], "GM": ph4["directions"]["GM"]["a2"]}
A2CI = {"GK": ph4["directions"]["GK"]["CI_a2_total"], "GM": ph4["directions"]["GM"]["CI_a2_total"]}
assert A2["GK"] == -0.0132447218611613 and A2["GM"] == -0.020633674570357804

b1ck = json.load(open(os.path.join(REPO, INPUTS["b1"][0])))
B1 = {k: v["biref_b1_VRH"] for k, v in b1ck["phase2"].items() if "biref_b1_VRH" in v}
PRE_B1 = {"hex_step|a": 0.01624085410723511, "hex_step|b": 0.016241797577228063,
          "hex_gem8|a": 0.01817488251117739, "hex_gem8|b": 0.018174297109340813,
          "cubic_step|001": -0.03789870339598654, "cubic_step|111": -0.03789870339598654,
          "cubic_gem8|001": -0.04548125222774924, "cubic_gem8|111": -0.04548125222774924}
assert set(B1) == set(PRE_B1), sorted(B1)
for k in PRE_B1:
    assert B1[k] == PRE_B1[k], k

# ---------------- arms (LS_PREREG §3) ----------------
ARMS = [
    {"id": "A0", "name": "1ES 1101-232 (anchor, TR-4)", "z": 0.186,
     "E_ref": 2.916e12, "E_alt": 7.33e11, "D_ref": "lt", "D_alt": "lt"},
    {"id": "A1", "name": "Crab Nebula (LHAASO)", "z": 0.0,
     "E_ref": 1.12e15, "E_alt": 0.94e15, "D_ref": 1.90 * KPC, "D_alt": 1.54 * KPC},
    {"id": "A2", "name": "Cygnus bubble (LHAASO)", "z": 0.0,
     "E_ref": 2.5e15, "E_alt": 1.0e15, "D_ref": 1.40 * KPC, "D_alt": 1.25 * KPC},
    {"id": "A3", "name": "GRB 221009A (LHAASO KM2A)", "z": 0.151,
     "E_ref": 12.5e12, "E_alt": 7.7e12, "D_ref": "lt", "D_alt": "lt"},
    {"id": "A4", "name": "Mrk 501 (HEGRA 1997)", "z": 0.034,
     "E_ref": 21.45e12, "E_alt": 16e12, "D_ref": "lt", "D_alt": "lt"},
]
REPORT_ONLY = [
    {"id": "A3-lp", "of": "A3", "note": "log-parabola highest event 17.8 TeV", "E": 17.8e12, "D": "lt", "z": 0.151},
    {"id": "A3-13", "of": "A3", "note": "abstract 'up to 13 TeV'", "E": 13e12, "D": "lt", "z": 0.151},
    {"id": "A2-gaia", "of": "A2", "note": "Cyg OB2 Gaia 1.6 kpc at E_alt", "E": 1.0e15, "D": 1.6 * KPC, "z": 0.0},
    {"id": "A1-2kpc", "of": "A1", "note": "classic 2.0 kpc at E_alt", "E": 0.94e15, "D": 2.0 * KPC, "z": 0.0},
]
TAU_R = 1.0
W_EM_RECORD = 3.7641664288e-33
NS = [20, 100, 1000]


def dist(spec, z):
    return d_lt(z) if spec == "lt" else spec


def dmax(qa, k, D, tau=TAU_R):
    qd = qa / 8.0
    return (tau / (qd * k ** 4 * D)) ** (1.0 / 3.0)


def validity(cfg, k, d):
    x = k * d
    qd = QA[cfg] / 8.0
    return {"x": x, "x_le_1e-4": x <= 1e-4, "epsT_x": EPS[cfg] * x, "epsT_x_le_1": EPS[cfg] * x <= 1,
            "Qx3": qd * x ** 3, "Qx3_le_0.10": qd * x ** 3 <= 0.10, "epsT2_le_0.10": EPS[cfg] ** 2 <= 0.10}


out = {"prereg_md5": INPUTS["prereg"][1], "inputs": {k: v[1] for k, v in INPUTS.items()},
       "constants": {"hbar": HBAR, "c": C, "e": E_CH, "pc_m": PC, "l_P": LP, "E_Pl_GeV": EPL_GEV,
                     "H0_km_s_Mpc": 67.4, "Omega_m": OM, "hbarc_eVm": HBARC_EVM},
       "anchor_R2_in_CONV": r2_ok, "arms": {}, "report_only": {}}

for arm in ARMS:
    z = arm["z"]
    readings = []
    for etag in ("E_ref", "E_alt"):
        for dtag in ("D_ref", "D_alt"):
            for ktag in (("k_obs", "k_1pz") if z > 0 else ("k_obs",)):
                E = arm[etag]
                D = dist(arm[dtag], z)
                k = k_of_E(E) * ((1 + z) if ktag == "k_1pz" else 1.0)
                per_cfg = {c: dmax(QA[c], k, D) for c in CFGS}
                readings.append({"E_tag": etag, "D_tag": dtag, "k_tag": ktag, "E_eV": E, "D_m": D,
                                 "k_per_m": k, "d_max": per_cfg})
    # bound of record = max over readings (per config); assert it is (E_alt, D_alt, k_obs)
    rec = {}
    for c in CFGS:
        best = max(readings, key=lambda r: r["d_max"][c])
        assert (best["E_tag"], best["D_tag"], best["k_tag"]) in (("E_alt", "D_alt", "k_obs"), ("E_alt", "D_ref", "k_obs")), (arm["id"], c)
        rec[c] = best["d_max"][c]
    rec_reading = [r for r in readings if r["E_tag"] == "E_alt" and r["D_tag"] == "D_alt" and r["k_tag"] == "k_obs"][0]
    for c in CFGS:
        assert rec_reading["d_max"][c] == rec[c]
    union_cfg = max(CFGS, key=lambda c: rec[c])
    assert union_cfg == "hex:step", (arm["id"], union_cfg)
    ref_reading = [r for r in readings if r["E_tag"] == "E_ref" and r["D_tag"] == "D_ref" and r["k_tag"] == "k_obs"][0]
    # validity at the arm's largest wavenumber and its bound of record
    kmax = max(r["k_per_m"] for r in readings)
    val = {c: validity(c, kmax, rec[c]) for c in CFGS}
    ok = all(v["x_le_1e-4"] and v["epsT_x_le_1"] and v["Qx3_le_0.10"] and v["epsT2_le_0.10"] for v in val.values())
    lam_rec = 2 * math.pi / rec_reading["k_per_m"]
    out["arms"][arm["id"]] = {
        "name": arm["name"], "z": z, "E_ref_eV": arm["E_ref"], "E_alt_eV": arm["E_alt"],
        "D_ref_m": dist(arm["D_ref"], z), "D_alt_m": dist(arm["D_alt"], z),
        "readings": readings, "record_per_config": rec, "record_union": rec[union_cfg],
        "union_config": union_cfg, "reference_union": ref_reading["d_max"][union_cfg],
        "reference_per_config": ref_reading["d_max"], "validity": val, "valid": ok,
        "E4D_record_eV4_m": arm["E_alt"] ** 4 * dist(arm["D_alt"], z),
        "grains_per_wavelength_cube_record": (lam_rec / rec[union_cfg]) ** 3,
        "lattice_k_a_at_N": {str(N): kmax * rec[union_cfg] / N for N in NS},
    }

for ro in REPORT_ONLY:
    D = dist(ro["D"], ro["z"])
    k = k_of_E(ro["E"])
    out["report_only"][ro["id"]] = {"of": ro["of"], "note": ro["note"], "E_eV": ro["E"], "D_m": D,
                                     "d_max_hex_step": dmax(QA["hex:step"], k, D)}

# anchor reproduction (halt-on-fail)
a0 = out["arms"]["A0"]
k_a0 = k_of_E(7.33e11)
D_a0 = d_lt(0.186)
rep_p2 = dmax(QA["hex:step"], k_a0, D_a0)
rep_bk = dmax(QA_BANKED["hex:step"], k_a0, D_a0)
dev_p2 = abs(rep_p2 - W_EM_RECORD) / W_EM_RECORD
dev_bk = abs(rep_bk - W_EM_RECORD) / W_EM_RECORD
out["anchor_reproduction"] = {"phase2_Q": rep_p2, "banked_Q": rep_bk, "record": W_EM_RECORD,
                              "rel_dev_phase2": dev_p2, "rel_dev_banked": dev_bk,
                              "per_config_banked_record": {c: dmax(QA_BANKED[c], k_a0, D_a0) for c in CFGS},
                              "pass": dev_p2 <= 1e-7 and dev_bk <= 1e-7}
if not out["anchor_reproduction"]["pass"]:
    print(json.dumps(out["anchor_reproduction"], indent=1))
    sys.exit("HALT: anchor reproduction failed")
assert rep_p2 == a0["record_union"]

# combined bound
valid_arms = [a for a in out["arms"] if out["arms"][a]["valid"]]
dec = min(valid_arms, key=lambda a: out["arms"][a]["record_union"])
d_comb = out["arms"][dec]["record_union"]
out["combined"] = {"d_comb": d_comb, "decisive_arm": dec, "valid_arms": valid_arms,
                   "R4_x10": d_comb * 10 ** (1 / 3), "R4_x0p1": d_comb * 10 ** (-1 / 3),
                   "ordering": sorted(valid_arms, key=lambda a: out["arms"][a]["record_union"])}

# table a_max(N)
table = {}
for a in out["arms"]:
    d = out["arms"][a]["record_union"]
    table[a] = {str(N): {"m": d / N, "lP": d / N / LP} for N in NS}
    table[a]["d_max"] = {"m": d, "lP": d / LP}
table["combined"] = {str(N): {"m": d_comb / N, "lP": d_comb / N / LP} for N in NS}
table["combined"]["d_max"] = {"m": d_comb, "lP": d_comb / LP}
table["combined_R4x10"] = {str(N): {"m": out["combined"]["R4_x10"] / N, "lP": out["combined"]["R4_x10"] / N / LP} for N in NS}
out["table"] = table

# texture (LS_PREREG §5)
DN = {"R-T1": 2e-37, "R-T2": 4e-32, "R-T0": 2e-38}
tex = {"Delta_n_max": DN, "t_max": {}}
for r, dn in DN.items():
    tex["t_max"][r] = {k: dn / abs(v) for k, v in B1.items()}
smallest_key = min(B1, key=lambda k: abs(B1[k]))
tex["headline_key"] = smallest_key
tex["headline"] = {r: DN[r] / abs(B1[smallest_key]) for r in DN}
cubic_keys = [k for k in B1 if k.startswith("cubic")]
hex_keys = [k for k in B1 if k.startswith("hex")]
fam = {"cubic": (21.0 / 4.0, min(cubic_keys, key=lambda k: abs(B1[k]))),
       "hex": (9.0, min(hex_keys, key=lambda k: abs(B1[k])))}
E_POL = 100e3
lam_pol = HC_EVM / E_POL
V_F = math.pi * lam_pol * GPC ** 2 / 6.0
stat = {"E_pol_eV": E_POL, "lambda_m": lam_pol, "D_m": GPC, "V_F_m3": V_F, "families": {}}
for f, (cc, key) in fam.items():
    tmax = DN["R-T1"] / abs(B1[key])
    Mmin = cc / tmax ** 2
    row = {"c": cc, "b1_key": key, "t_max_RT1": tmax, "M_min": Mmin, "at_d": {}}
    for dlabel, dval in (("anchor_edge", W_EM_RECORD), ("d_comb", d_comb)):
        M_F = V_F / dval ** 3
        sig = math.sqrt(cc / M_F)
        row["at_d"][dlabel] = {"d_m": dval, "L_min_m": dval * Mmin ** (1 / 3), "M_Fresnel": M_F,
                               "sigma_t_Fresnel": sig, "t_max_over_sigma_t": tmax / sig}
    stat["families"][f] = row
tex["statistical"] = stat
out["texture"] = tex

# dispersion (LS_PREREG §6)
EQG = {"record_6.9e11GeV": 6.9e11, "abstract_6e-8EPl": 6e-8 * EPL_GEV}
disp = {"E_QG2_GeV": EQG, "a2": A2, "a2_CI": A2CI, "a_max": {}}
for etag, eg in EQG.items():
    for dtag, a2 in A2.items():
        amax = HBARC_EVM / (eg * 1e9 * math.sqrt(2 * abs(a2)))
        disp["a_max"]["%s|%s" % (etag, dtag)] = {"m": amax, "lP": amax / LP}
rec_key = "record_6.9e11GeV|GK"
disp["record_key"] = rec_key
disp["record"] = disp["a_max"][rec_key]
assert disp["record"]["m"] == max(v["m"] for v in disp["a_max"].values())
# group-velocity cross-check of the conversion at the record reading
E_test = 1e12  # eV
a_r = disp["record"]["m"]
kk = k_of_E(E_test)
lhs = 3 * abs(A2["GK"]) * (kk * a_r) ** 2
rhs = 1.5 * (E_test / (6.9e11 * 1e9)) ** 2
disp["group_velocity_check_rel"] = abs(lhs - rhs) / rhs
assert disp["group_velocity_check_rel"] < 1e-12
disp["dim5_term"] = "absent by symmetry (centrosymmetric p6m / P6_3/mmc, finite-range analytic dynamical matrix); record: G-S2C1 A3 DISPERSIVE-O(k^2)"
out["dispersion"] = disp

# combine (LS_PREREG §7)
out["combined_a_max"] = {str(N): {"attenuation_m": d_comb / N, "dispersion_m": disp["record"]["m"],
                                  "a_max_m": min(d_comb / N, disp["record"]["m"]),
                                  "a_max_lP": min(d_comb / N, disp["record"]["m"]) / LP,
                                  "binding": "attenuation" if d_comb / N < disp["record"]["m"] else "dispersion"}
                         for N in NS}
out["c_geo"] = {c: QA[c] / (8 * EPS[c] ** 2) for c in CFGS}
out["D_lt"] = {str(z): v for z, v in D_LT.items()}

with open(os.path.join(HERE, "ls_leg1.json"), "w") as f:
    json.dump(out, f, indent=1, sort_keys=True)

# ---------------- text report ----------------
P = print
P("LS leg 1 (prereg %s)" % INPUTS["prereg"][1])
P("anchor reproduction: phase-2 Q %.10e (dev %.2e), banked Q %.10e (dev %.2e) vs record %.10e" %
  (rep_p2, dev_p2, rep_bk, dev_bk, W_EM_RECORD))
P("D_lt: " + ", ".join("z=%s %.6f Mpc" % (z, v["Mpc"]) for z, v in D_LT.items()))
P("c_geo = Q_T^a/(8 eps_T^2): " + ", ".join("%s %.4f" % (c, out["c_geo"][c]) for c in CFGS))
P("")
P("%-4s %-30s %-14s %-14s %-12s %-10s %-9s" % ("arm", "source", "d_rec (m)", "d_ref (m)", "x_max", "valid", "E4D rec"))
for a, v in out["arms"].items():
    P("%-4s %-30s %-14.6e %-14.6e %-12.3e %-10s %-9.3e" % (a, v["name"][:30], v["record_union"], v["reference_union"],
                                                          v["validity"]["hex:step"]["x"], v["valid"], v["E4D_record_eV4_m"]))
P("per-config bound of record:")
for a, v in out["arms"].items():
    P("  %s " % a + "  ".join("%s %.6e" % (c, v["record_per_config"][c]) for c in CFGS))
P("report-only readings (hex:step): " + "; ".join("%s %.4e m" % (k, v["d_max_hex_step"]) for k, v in out["report_only"].items()))
P("combined: d_comb = %.6e m (decisive %s); R4 x10 %.6e, x0.1 %.6e; ordering %s" %
  (d_comb, dec, out["combined"]["R4_x10"], out["combined"]["R4_x0p1"], out["combined"]["ordering"]))
P("")
P("a_max(N) = d_max/N  [metres | Planck lengths]")
P("%-14s" % "arm" + "".join("%-30s" % ("N=%d" % N) for N in NS))
for a in list(out["arms"]) + ["combined", "combined_R4x10"]:
    P("%-14s" % a + "".join("%-30s" % ("%.4e | %.4e" % (table[a][str(N)]["m"], table[a][str(N)]["lP"])) for N in NS))
P("")
P("texture: t_max = Dn_max/|b1|; headline key %s" % smallest_key)
for r in DN:
    P("  %s (Dn %.0e): headline %.4e; " % (r, DN[r], tex["headline"][r]) +
      ", ".join("%s %.4e" % (k, v) for k, v in tex["t_max"][r].items()))
for f, row in stat["families"].items():
    P("  stat %s (c=%.2f, key %s): t_max %.4e, M_min %.4e" % (f, row["c"], row["b1_key"], row["t_max_RT1"], row["M_min"]))
    for dl, x in row["at_d"].items():
        P("     at %s d=%.4e: L_min %.4e m, M_Fresnel %.4e, sigma_t %.4e, t_max/sigma_t %.4e" %
          (dl, x["d_m"], x["L_min_m"], x["M_Fresnel"], x["sigma_t_Fresnel"], x["t_max_over_sigma_t"]))
P("")
P("dispersion: a_max^disp = hbar c/(E_QG2 sqrt(2|a2|))")
for k, v in disp["a_max"].items():
    P("  %-28s %.4e m = %.4e l_P" % (k, v["m"], v["lP"]))
P("  record %s; group-velocity check %.1e" % (rec_key, disp["group_velocity_check_rel"]))
P("")
P("combined a_max(N) = min(d_comb/N, a_max^disp):")
for N in NS:
    v = out["combined_a_max"][str(N)]
    P("  N=%-5d %.4e m = %.4e l_P (binding: %s)" % (N, v["a_max_m"], v["a_max_lP"], v["binding"]))
