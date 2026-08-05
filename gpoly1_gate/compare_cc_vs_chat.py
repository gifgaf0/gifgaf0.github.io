#!/usr/bin/env python3
# G-POLY1 two-leg comparison: CC checkpoints vs chat-leg embedded checkpoints.
# Run ONLY after all CC checkpoints exist (activation flag 1). No reconciliation:
# any criterion miss is reported raw (S9 rule).
import json, hashlib, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
def load(fn):
    return json.loads(open(os.path.join(HERE, fn), "rb").read())

cc0a = load("poly1_phase0a_cc.json")
cc0f = load("poly1_phase0full_cc.json")
cc0b = load("poly1_phase0bfull_cc.json")
cc1f = load("poly1_phase1full_cc.json")
cc1q = load("poly1_phase1quoted_cc.json")
ch0a = load("chatleg_phase0a.json")
ch0f = load("chatleg_phase0full.json")
ch0b = load("chatleg_phase0bfull.json")
ch1f = load("chatleg_phase1full.json")
ch1q = load("chatleg_phase1.json")
ch0bq = load("chatleg_phase0b.json")

rows = {}
def cmp_add(crit, label, a, b):
    if b == 0.0:
        r = abs(a - b)
    else:
        r = abs(a / b - 1.0)
    rows.setdefault(crit, []).append((label, a, b, r))
    return r

# ---------- C1: twelve Phase-0a containment quantities (quoted layer) ----------
for cfg in ("step_hex", "gem8_cubic", "step_cubic"):
    for q in ("cont_vT", "cont_vTR", "cont_vTV", "cont_AU"):
        cmp_add("C1", f"{cfg}.{q}", cc0a["configs"][cfg][q]["got"], ch0a["configs"][cfg][q]["got"])
for cfg in ("step", "gem8"):
    for q in ("v_f0", "v_f05", "v_f1", "span_pct"):
        cmp_add("C1x", f"mix.{cfg}.{q}", cc0a["mixtures"][cfg][q], ch0a["mixtures"][cfg][q])
cmp_add("C1x", "zener_derived_C44", cc0a["controls"]["zener_derived_C44"], ch0a["controls"]["zener_derived_C44"])
cmp_add("C1x", "hex_C66_identity_residual", cc0a["controls"]["hex_C66_identity_residual"], ch0a["controls"]["hex_C66_identity_residual"])

# ---------- C2: full-precision reproduction verdict + per-item agreement ----------
c2_id = (cc0f["C2_verdict"] == ch0f["C2_verdict"] == "PASS")
cmp_add("C2", "worst_residual_of_tol", cc0f["worst_residual_of_tol"], ch0f["worst_residual_of_tol"])
for blk, items in ch0f["C2"].items():
    key = blk if blk in cc0f["C2"] else {"mixture:step": "mixture:step", "mixture:gem8": "mixture:gem8"}[blk]
    for q, r in items.items():
        cmp_add("C2", f"{blk}.{q}", cc0f["C2"][key][q]["got"], r["got"])

# ---------- C3: covariance invariants (full layer primary; quoted cross-check) ----------
KEYS_1A = ("KV_pinned", "KR_pinned", "GV_pinned", "GR_pinned", "KV_gen", "GV_gen",
           "V_tot", "Phi_G", "Phi_full", "nu")
for cfg, blk in ch1f["phase1a"].items():
    for q in KEYS_1A:
        if q in blk:
            cmp_add("C3", f"full.{cfg}.{q}", cc1f["phase1a"][cfg][q], blk[q])
    for q, v in blk["pinned_46i_contractions"].items():
        cmp_add("C3", f"full.{cfg}.{q}", cc1f["phase1a"][cfg]["pinned_46i_contractions"][q], v)
for cfg, blk in ch1q["phase1a"].items():
    for q in KEYS_1A:
        if q in blk:
            cmp_add("C3q", f"quoted.{cfg}.{q}", cc1q["phase1a"][cfg][q], blk[q])
    for q, v in blk["pinned_46i_contractions"].items():
        cmp_add("C3q", f"quoted.{cfg}.{q}", cc1q["phase1a"][cfg]["pinned_46i_contractions"][q], v)

# ---------- C4: closed quantities (Q assembly + HS), <= 1e-6 ----------
KEYS_1B = ("mu_bar", "lam_bar", "VT0", "VL0", "int_Phi_TT", "int_Phi_TL",
           "Q_T_a", "Q_T_TT_a", "Q_T_TL_a", "Q_L_a", "Q_T_d", "Qprime_G",
           "eps_T", "eps_L")
for cfg, blk in ch1f["phase1b"].items():
    for q in KEYS_1B:
        if q in blk:
            cmp_add("C4", f"full.{cfg}.{q}", cc1f["phase1b"][cfg][q], blk[q])
for cfg in ("step_cubic", "gem8_cubic"):
    a, b = cc0b["phase0b"][cfg], ch0b["phase0b"][cfg]
    cmp_add("C4", f"hs.{cfg}.K", a["K"], b["K"])
    for i in (0, 1):
        cmp_add("C4", f"hs.{cfg}.mu_HS[{i}]", a["mu_HS"][i], b["mu_HS"][i])
        cmp_add("C4", f"hs.{cfg}.vT_HS[{i}]", a["vT_HS"][i], b["vT_HS"][i])
    cmp_add("C4", f"hs.{cfg}.HS_halfwidth_pct", a["HS_halfwidth_pct"], b["HS_halfwidth_pct"])
for cfg in ("step_hex", "gem8_hex"):
    a, b = cc0b["phase0b"][cfg], ch0b["phase0b"][cfg]
    for q in ("K_V", "K_R_berryman", "K_R_1606"):
        cmp_add("C4", f"hs.{cfg}.{q}", a[q], b[q])
    for i in (0, 1):
        cmp_add("C4x", f"hs.{cfg}.K_HS[{i}] (residual-floor, non-verdict)", a["K_HS"][i], b["K_HS"][i])
# quoted-layer C4 cross-check (main dispatch section 5 targets)
for cfg, blk in ch1q["phase1b"].items():
    for q in KEYS_1B:
        if q in blk and q in cc1q["phase1b"].get(cfg, {}):
            cmp_add("C4q", f"quoted.{cfg}.{q}", cc1q["phase1b"][cfg][q], blk[q])
for i in (0, 1):
    cmp_add("C4q", f"quoted.gem8_cubic.mu_HS[{i}]", cc1q["phase0b_quoted_gem8"]["mu_HS"][i],
            ch0bq["phase0b"]["gem8_cubic"]["mu_HS_lo" if i == 0 else "mu_HS_hi"])

# ---------- C5: finite-ka exponent class + prefactor ----------
c5_rows = []
for layer, cc, ch in (("full", cc1f, ch1f), ("quoted", cc1q, ch1q)):
    for cfg, blk in ch["phase1b"].items():
        if "fit_exponent" not in blk or cfg not in cc["phase1b"]:
            continue
        my = cc["phase1b"][cfg]
        expo_class = abs(my["fit_exponent"] - 4.0)
        pref = abs(my["Q_ext_richardson"] / my["Q_T_a"] - 1.0)
        dexp = abs(my["fit_exponent"] - blk["fit_exponent"])
        worst_alpha = max(abs(x / y - 1.0) for x, y in zip(my["alpha_T_a"], blk["alpha_T_a"]))
        c5_rows.append((f"{layer}.{cfg}", my["fit_exponent"], expo_class, pref, dexp, worst_alpha))

# ---------- C6: verdict / status identity ----------
def status_class(s):
    return s.split(":")[0].split("-")[0].strip().upper()
c6 = []
for cfg, blk in ch1f["phase1b"].items():
    c6.append((f"full.{cfg}", status_class(cc1f["phase1b"][cfg]["status"]), status_class(blk["status"])))
for cfg in ("step_hex", "gem8_hex"):
    c6.append((f"hs.{cfg}", cc0b["phase0b"][cfg]["status"], ch0b["phase0b"][cfg]["status"]))
c6.append(("quoted.step_cubic", status_class(cc1q["phase1b"]["step_cubic"]["status"]),
           status_class(ch1q["phase1b"]["step_cubic"]["status"])))
c6.append(("C2_verdict", cc0f["C2_verdict"], ch0f["C2_verdict"]))
c6_ok = all(a == b for _, a, b in c6)

# ---------- verdicts ----------
THRESH = {"C1": 1e-8, "C2": 1e-6, "C3": 1e-8, "C3q": 1e-8, "C4": 1e-6, "C4q": 1e-6}
verdict = {}
print("criterion  n_items  worst_rel_resid  threshold  verdict  worst_item")
for crit in ("C1", "C2", "C3", "C3q", "C4", "C4q"):
    rs = rows[crit]
    wl, wa, wb, wr = max(rs, key=lambda t: t[3])
    ok = wr <= THRESH[crit]
    verdict[crit] = {"n": len(rs), "worst_rel": wr, "worst_item": wl,
                     "threshold": THRESH[crit], "pass": bool(ok)}
    print(f"{crit:5s} {len(rs):8d} {wr:16.3e} {THRESH[crit]:9.0e}  {'PASS' if ok else 'MISS'}  {wl}")
wr_c1x = max(rows["C1x"], key=lambda t: t[3])
wr_c4x = max(rows["C4x"], key=lambda t: t[3])
print(f"C1-extras (non-verdict): n={len(rows['C1x'])} worst {wr_c1x[3]:.3e} at {wr_c1x[0]}")
print(f"hex K_HS (residual-floor, non-verdict): worst rel {wr_c4x[3]:.3e} at {wr_c4x[0]}")
verdict["C1_extras"] = {"n": len(rows["C1x"]), "worst_rel": wr_c1x[3], "worst_item": wr_c1x[0]}
verdict["hex_K_HS_floor"] = {"worst_rel": wr_c4x[3], "worst_item": wr_c4x[0],
                             "note": "degenerate-inverted band at input-identity-residual floor; "
                                     "optimizer operationalization documented in deviation log"}
c5_worst_pref = max(r[3] for r in c5_rows)
c5_worst_class = max(r[2] for r in c5_rows)
c5_ok = all(r[2] < 0.05 for r in c5_rows) and c5_worst_pref <= 0.05
verdict["C5"] = {"rows": [{"cfg": r[0], "fit_exponent": r[1], "dist_from_4": r[2],
                           "richardson_vs_closed": r[3], "exp_diff_vs_chat": r[4],
                           "worst_alpha_rel_vs_chat": r[5]} for r in c5_rows],
                 "pass": bool(c5_ok)}
print(f"C5    exponent-4 class worst |fit-4| {c5_worst_class:.4f}; prefactor worst {c5_worst_pref:.2e};"
      f" worst alpha two-leg rel {max(r[5] for r in c5_rows):.3e}  {'PASS' if c5_ok else 'MISS'}")
verdict["C6"] = {"rows": [{"item": i, "cc": a, "chat": b} for i, a, b in c6], "pass": bool(c6_ok)}
print(f"C6    status identity: {'PASS' if c6_ok else 'MISS'}  ({len(c6)} items)")
verdict["C2_verdict_identity"] = bool(c2_id)

# Qprime_G structural observation (R2-class, non-verdict)
qg = {cfg: cc1f["phase1b"][cfg]["Qprime_G"] for cfg in cc1f["phase1b"]}
verdict["R2_Qprime_G_cc"] = qg
smax, smin = max(qg.values()), min(qg.values())
print("R2 Qprime_G (CC leg):", {k: f"{v:.6e}" for k, v in qg.items()},
      f"span {100.0 * (smax - smin) / (0.5 * (smax + smin)):.2f}%")
# X-1 layer deltas vs chat's section-D values
verdict["x1_layer_deltas_cc"] = cc1q["x1_layer_deltas_fullprec_over_quoted"]

overall = all(verdict[c]["pass"] for c in ("C1", "C2", "C3", "C3q", "C4", "C4q", "C5", "C6")) and c2_id
verdict["OVERALL"] = "ALL CRITERIA PASS -- no S9 items" if overall else "S9: criterion miss (raw values above, no reconciliation)"
print("OVERALL:", verdict["OVERALL"])
blob = json.dumps(verdict, indent=1)
open(os.path.join(HERE, "gpoly1_cc_verdict.json"), "w").write(blob)
print("wrote gpoly1_cc_verdict.json md5", hashlib.md5(blob.encode()).hexdigest())
sys.exit(0 if overall else 9)
