#!/usr/bin/env python3
# G-POLY1 Phase 0a -- CC LEG (independent instrument, written from scratch).
# Ledger-quoted inputs transcribed from the dispatch (C/rho; v_T = sqrt(G); rho = 1).
# Cubic: closed VRH forms. Hexagonal: symmetry-pinned closed forms
# (K_V Berryman (22); K_R = Csq/M and G_R per the pinned 1606.03700 (4)-(5) class;
# G_V textbook hex form with quoted C66). Containment vs quoted targets.
import json, hashlib, math, sys, os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "poly1_phase0a_cc.json")

def cubic_vrh(c11, c12, c44):
    K = (c11 + 2.0 * c12) / 3.0
    GV = (c11 - c12 + 3.0 * c44) / 5.0
    GR = 5.0 * (c11 - c12) * c44 / (4.0 * c44 + 3.0 * (c11 - c12))
    GH = 0.5 * (GV + GR)
    AU = 5.0 * GV / GR + 1.0 - 6.0
    return dict(K=K, GV=GV, GR=GR, GH=GH, AU=AU)

def hex_vrh_pinned(c11, c12, c13, c33, c44, c66):
    KV = (2.0 * (c11 + c12) + 4.0 * c13 + c33) / 9.0
    M = c11 + c12 + 2.0 * c33 - 4.0 * c13
    Csq = (c11 + c12) * c33 - 2.0 * c13 * c13
    KR = Csq / M
    GV = (M + 12.0 * c44 + 12.0 * c66) / 30.0
    GR = 2.5 * (Csq * c44 * c66) / (3.0 * KV * c44 * c66 + Csq * (c44 + c66))
    GH = 0.5 * (GV + GR)
    AU = 5.0 * GV / GR + KV / KR - 6.0
    return dict(KV=KV, KR=KR, GV=GV, GR=GR, GH=GH, AU=AU)

def contain(got, target, rtol):
    return dict(got=got, target=target, rtol=rtol,
                ok=bool(abs(got - target) <= rtol * abs(target)))

def mix_vrh(g0, g1, f):
    gv = (1.0 - f) * g0 + f * g1
    gr = 1.0 / ((1.0 - f) / g0 + f / g1)
    return 0.5 * (gv + gr)

ck = {"gate": "G-POLY1", "phase": "0a", "leg": "cc", "controls": {}, "configs": {},
      "mixtures": {}, "failures": []}

# controls: isotropic-input null (cubic with c44 = (c11-c12)/2 exactly)
iso = cubic_vrh(200.0, 100.0, 50.0)
ck["controls"]["iso_null_GVminusGR"] = iso["GV"] - iso["GR"]
ck["controls"]["iso_null_AU"] = iso["AU"]
# Zener control (gem8 cubic): derived C44 from quoted Zener 2.838 x C'
zc = 2.838 * (272.08 - 179.38) / 2.0
ck["controls"]["zener_derived_C44"] = zc
ck["controls"]["zener_vs_quoted_C44"] = contain(zc, 131.54, 2e-4)
# hex C66 identity residual (relative to C66)
ck["controls"]["hex_C66_identity_residual"] = abs(64.92 - (238.42 - 108.54) / 2.0) / 64.92

# --- step:AB hex (quoted) ---
h = hex_vrh_pinned(238.42, 108.54, 57.48, 287.67, 60.03, 64.92)
vT, vTR, vTV = math.sqrt(h["GH"]), math.sqrt(h["GR"]), math.sqrt(h["GV"])
ck["configs"]["step_hex"] = {
    "BV": h["KV"], "BR": h["KR"], "GV": h["GV"], "GR": h["GR"], "GH": h["GH"],
    "AU": h["AU"], "vT": vT, "vT_R": vTR, "vT_V": vTV,
    "cont_vT": contain(vT, 8.4191, 2e-4), "cont_vTR": contain(vTR, 8.2883, 2e-4),
    "cont_vTV": contain(vTV, 8.5478, 2e-4), "cont_AU": contain(h["AU"], 0.318, 5e-3)}
g_step_hex = h["GH"]

# --- gem8:FCC cubic (quoted) ---
c = cubic_vrh(272.08, 179.38, 131.54)
vT, vTR, vTV = math.sqrt(c["GH"]), math.sqrt(c["GR"]), math.sqrt(c["GV"])
ck["configs"]["gem8_cubic"] = {
    "K": c["K"], "GV": c["GV"], "GR": c["GR"], "GH": c["GH"], "AU": c["AU"],
    "vT": vT, "vT_R": vTR, "vT_V": vTV,
    "cont_vT": contain(vT, 9.3079, 2e-4), "cont_vTR": contain(vTR, 8.7068, 2e-4),
    "cont_vTV": contain(vTV, 9.8725, 2e-4), "cont_AU": contain(c["AU"], 1.428, 5e-3)}
g_gem8_cubic = c["GH"]

# --- step:FCC cubic (G-sector only: C44, C' quoted; c11-c12 = 2C') ---
dc = 2.0 * 36.73
c44s = 85.29
GV = (dc + 3.0 * c44s) / 5.0
GR = 5.0 * dc * c44s / (4.0 * c44s + 3.0 * dc)
GH = 0.5 * (GV + GR)
AU = 5.0 * GV / GR - 5.0
vT, vTR, vTV = math.sqrt(GH), math.sqrt(GR), math.sqrt(GV)
ck["configs"]["step_cubic"] = {
    "GV": GV, "GR": GR, "GH": GH, "AU": AU, "vT": vT, "vT_R": vTR, "vT_V": vTV,
    "cont_vT": contain(vT, 7.799, 2e-4), "cont_vTR": contain(vTR, 7.4689, 2e-4),
    "cont_vTV": contain(vTV, 8.1158, 2e-4), "cont_AU": contain(AU, 0.904, 5e-3)}
g_step_cubic = GH

# --- mixtures: two-phase VRH over phase Hill shear moduli; span mean-normalized ---
v0, v05, v1 = (math.sqrt(mix_vrh(g_step_cubic, g_step_hex, f)) for f in (0.0, 0.5, 1.0))
span = 100.0 * (v1 - v0) / (0.5 * (v0 + v1))
ck["mixtures"]["step"] = {"v_f0": v0, "v_f05": v05, "v_f1": v1, "span_pct": span,
                          "cont_span": contain(span, 7.65, 2e-2)}
g_gem8_hex_endpoint = 10.0417 ** 2  # derived-input label: from quoted endpoint vT
v0, v05, v1 = (math.sqrt(mix_vrh(g_gem8_cubic, g_gem8_hex_endpoint, f)) for f in (0.0, 0.5, 1.0))
span = 100.0 * (v1 - v0) / (0.5 * (v0 + v1))
ck["mixtures"]["gem8"] = {"v_f0": v0, "v_f05": v05, "v_f1": v1, "span_pct": span,
                          "cont_span": contain(span, 7.59, 2e-2),
                          "note": "hcp endpoint G from quoted vT (derived-input label)"}

# gates
for cfg, d in ck["configs"].items():
    for k, v in d.items():
        if isinstance(v, dict) and "ok" in v and not v["ok"]:
            ck["failures"].append(f"{cfg}.{k}")
for cfg, d in ck["mixtures"].items():
    if not d["cont_span"]["ok"]:
        ck["failures"].append(f"mix.{cfg}")
if abs(ck["controls"]["iso_null_GVminusGR"]) > 1e-12 or abs(ck["controls"]["iso_null_AU"]) > 1e-12:
    ck["failures"].append("iso_null")
ck["phase0a_containment"] = "PASS" if not ck["failures"] else "FAIL"

blob = json.dumps(ck, indent=1)
open(OUT, "w").write(blob)
print("phase0a", ck["phase0a_containment"], "md5", hashlib.md5(blob.encode()).hexdigest())
sys.exit(0 if not ck["failures"] else 9)
