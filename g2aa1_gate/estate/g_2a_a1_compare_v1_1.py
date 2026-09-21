#!/usr/bin/env python3
"""g_2a_a1_compare_v1_1.py — two-leg comparator for Gate G-2a-A1, v1.1 CANDIDATE (September 21, 2026; NOT frozen until the author's S9 election).

v1.1 = v1.0 (5afcd589) + the three recording-convention harmonizations R1.1-1..3 declared in schema v1.1 CANDIDATE r2
(comparison_rules.harmonizations_v1_1). Row count unchanged (436 on the canonical legs): each harmonized row replaces
its v1.0 row one-for-one and is vacuous-PASS only under the stated witness agreement; otherwise the v1.0 exact rule applies.

Compares the chat-leg and CC-leg E8 checkpoints against g_2a_a1_schema_v1_0.json.
Checks: C0 provenance + independence witness; C1 Phase 0; C2 Phase 1 (T1..T4, group1344);
C3 Phase 1b (P_C, H screen, I5); C4 Phase 2; C5 Phase 3 (verdict identity + verdict recomputed
from the booleans by the schema's rule + internal consistency). Free text is never compared.
Floats are checked per leg against the schema's rule (gt/le threshold), never across legs.

Usage:
  compare  : python3 g_2a_a1_compare_v1_1.py compare CHAT.json CC.json [--schema S.json] [--out OUT.json]
  selftest : python3 g_2a_a1_compare_v1_1.py selftest
Exit: 0 all PASS, 1 any MISS, 2 usage/fatal.
"""
import hashlib, json, sys, copy

SCHEMA_DEFAULT = "g_2a_a1_schema_v1_1_CANDIDATE_r2.json"
SCHEMA_MD5 = "88a92fe2bd17465841f2aacb323e2408"   # schema v1.1 CANDIDATE r2 md5; asserted at load

SORTED_LIST_KEYS = {"nu4_allowed", "admissible", "admissible_H", "tests_holding", "loop_images"}
CONTROL_TRUE = ["L_perp_zero_mode", "F21_split_1_3_3bar", "generic_so16_fails_margin_positive"]

def md5_file(p):
    return hashlib.md5(open(p, "rb").read()).hexdigest()

def load_schema(path):
    raw = open(path, "rb").read()
    h = hashlib.md5(raw).hexdigest()
    if SCHEMA_MD5 != "__SCHEMA_MD5__" and h != SCHEMA_MD5:
        raise SystemExit(f"FATAL: schema md5 {h} != frozen {SCHEMA_MD5}")
    return json.loads(raw.decode("utf-8")), h

def canon(v, key=None):
    if isinstance(v, list):
        if key and (key.endswith("_set") or key in SORTED_LIST_KEYS):
            return sorted(v, key=lambda x: json.dumps(x, sort_keys=True))
        return [canon(x) for x in v]
    if isinstance(v, dict):
        return {k: canon(v[k], k) for k in sorted(v)}
    return v

TYPE = {"int": int, "bool": bool, "str": str, "list": list}
def typed_ok(v, t):
    if t == "int": return isinstance(v, int) and not isinstance(v, bool)
    if t == "bool": return isinstance(v, bool)
    if t == "str": return isinstance(v, str)
    if t == "list": return isinstance(v, list)
    if isinstance(t, dict): return isinstance(v, dict)
    return False

class Rec:
    def __init__(self):
        self.rows = []
    def add(self, check, name, ok, a=None, b=None, note=""):
        self.rows.append({"check": check, "name": name, "pass": bool(ok), "chat": a, "cc": b, "note": note})
    def summary(self):
        n = len(self.rows); p = sum(r["pass"] for r in self.rows)
        return {"checks": n, "pass": p, "miss": n - p}

def get(d, path, default=None):
    cur = d
    for k in path.split("."):
        if not isinstance(cur, dict) or k not in cur: return default
        cur = cur[k]
    return cur

def cmp_exact_block(R, check, label, A, B, keys, harmonize=None):
    """harmonize: optional {key: fn(A, B) -> (ok, note)} replacing the v1.0 'equal' row for that key (R1.1-x)."""
    for k, t in keys.items():
        va, vb = (A or {}).get(k), (B or {}).get(k)
        if isinstance(t, dict):   # nested exact block (e.g. controls)
            cmp_exact_block(R, check, f"{label}.{k}", va or {}, vb or {}, t)
            continue
        okt = typed_ok(va, t) and typed_ok(vb, t)
        R.add(check, f"{label}.{k} typed", okt, va, vb, f"type {t}")
        if harmonize and k in harmonize:
            okh, note = harmonize[k](A or {}, B or {})
            R.add(check, f"{label}.{k} equal ({note})", okt and okh, va, vb, note)
        else:
            R.add(check, f"{label}.{k} equal", okt and canon(va, k) == canon(vb, k), va, vb)

# ---------------------------------------------------------------- v1.1 harmonizations (schema comparison_rules.harmonizations_v1_1)
def _norm_sym_int(D):
    lab, dim = D.get("sym_int_continuous"), D.get("sym_int_continuous_dim")
    if lab == "G2xU1_psi0" and isinstance(dim, int) and not isinstance(dim, bool):
        return ("G2", dim - 1)
    return (lab, dim)

def harm_sym_int_label(A, B):
    return _norm_sym_int(A)[0] == _norm_sym_int(B)[0], "7-sector normalized, R1.1-1"

def harm_sym_int_dim(A, B):
    return _norm_sym_int(A)[1] == _norm_sym_int(B)[1], "7-sector normalized, R1.1-1"

def harm_aut_count(A, B):
    ca, cb = A.get("spinor_2O_automorphism_count"), B.get("spinor_2O_automorphism_count")
    da, db = A.get("spinor_2O_min_automorphism_defect"), B.get("spinor_2O_min_automorphism_defect")
    def fl(x): return isinstance(x, (int, float)) and not isinstance(x, bool)
    vacuous = fl(da) and fl(db) and da > 1e-6 and db > 1e-6 and ca in (0, 1) and cb in (0, 1)
    return (ca == cb) or vacuous, "identity-convention normalized, R1.1-2"

def _h5_booking_consistent(h):
    code = h.get("code") or ""
    if not (isinstance(code, str) and code.startswith("EXCLUDED(") and "ii" in code and h.get("ii") == "fail"):
        return False
    inner = code[len("EXCLUDED("):].rstrip(")")
    toks = [t.strip() for t in inner.split(",")]
    if h.get("i") == "fail":
        return "i" in toks and "centrality" not in toks
    if h.get("i") == "pass":
        return "centrality" in toks and "i" not in toks
    return False

def make_h5_harmonizer(PC_a, PC_b, field):
    def f(HA, HB):
        pc_ok = all((PC or {}).get("e8_central") is False and (PC or {}).get("e8_anticommutes") is True for PC in (PC_a, PC_b))
        vacuous = pc_ok and _h5_booking_consistent(HA) and _h5_booking_consistent(HB)
        return (HA.get(field) == HB.get(field)) or vacuous, "P-C booking normalized, R1.1-3"
    return f

def cmp_float_block(R, check, label, A, B, keys):
    for k, rule in keys.items():
        for leg, D in (("chat", A), ("cc", B)):
            v = (D or {}).get(k)
            ok = isinstance(v, (int, float)) and not isinstance(v, bool)
            if ok:
                ok = (v > rule["threshold"]) if rule["rule"] == "gt" else (v <= rule["threshold"])
            R.add(check, f"{label}.{k} ({leg}) {rule['rule']} {rule['threshold']}", ok, v if leg == "chat" else None, v if leg == "cc" else None)

def domain_check(R, check, label, A, B, key, domain):
    for leg, D in (("chat", A), ("cc", B)):
        v = (D or {}).get(key)
        R.add(check, f"{label}.{key} ({leg}) in domain", v in domain, v if leg == "chat" else None, v if leg == "cc" else None)

def recompute_controls(ck):
    c0 = get(ck, "phase0.controls", {}) or {}
    ok = all(c0.get(k) is True for k in CONTROL_TRUE)
    ok = ok and get(ck, "phase1.T1.control_sym3_quartet_mult") == 1
    ok = ok and get(ck, "phase1.T2.control_1344_all_automorphisms") is True
    ok = ok and get(ck, "phase1.T2.spinor_2O_quartet_mult") == 2
    ok = ok and get(ck, "phase1.T3.controls_pi4_S2") == "Z2"
    ok = ok and get(ck, "phase1.T3.controls_pi4_S3") == "Z2"
    ok = ok and get(ck, "phase1.T3.controls_pi1_SO3_mod_T") == 24
    ok = ok and get(ck, "phase1.T4.control_F21_unsigned_1_3_3bar") is True
    ok = ok and get(ck, "phase1.T4.nu2_unsigned_automorphism") is True
    ok = ok and get(ck, "phase2.O_zero_on_nonline") is True
    return bool(ok)

def recompute_verdict(ck):
    if not recompute_controls(ck): return "INDETERMINATE"
    if get(ck, "phase0.sym_int_pinned") is not True: return "UNDECIDED-BY-SUBSTRATE"
    holds = [get(ck, f"phase1.{t}.holds") for t in ("T1", "T2", "T3", "T4")]
    if get(ck, "phase0.spatial_internal_direct_product") is not True or any(h is not True for h in holds):
        return "ASSIGNMENT-II-REALIZABLE"
    return "ASSIGNMENT-I-FORCED"

def compare(chat, cc, S):
    R = Rec()
    # ---------------- C0 provenance ----------------
    for k in S["required_top"]:
        R.add("C0", f"required key {k} present (chat)", k in chat)
        R.add("C0", f"required key {k} present (cc)", k in cc)
    for k in ("memo_lock_md5", "ledger_base_md5", "t1_list_md5", "action_extract_md5"):
        R.add("C0", f"{k} == schema (chat)", chat.get(k) == S[k], chat.get(k), S[k])
        R.add("C0", f"{k} == schema (cc)", cc.get(k) == S[k], cc.get(k), S[k])
    R.add("C0", "gate label", chat.get("gate") == S["gate"] and cc.get("gate") == S["gate"], chat.get("gate"), cc.get("gate"))
    R.add("C0", "leg labels chat/cc", chat.get("leg") == "chat" and cc.get("leg") == "cc", chat.get("leg"), cc.get("leg"))
    for f in S["t1_scan_required"]:
        R.add("C0", f"t1_scan.{f} CLEAN (chat)", get(chat, f"t1_scan.{f}") in S["t1_scan_domain"], get(chat, f"t1_scan.{f}"))
        R.add("C0", f"t1_scan.{f} CLEAN (cc)", get(cc, f"t1_scan.{f}") in S["t1_scan_domain"], None, get(cc, f"t1_scan.{f}"))
    R.add("C0", "elections == schema (chat)", chat.get("elections") == S["elections"], chat.get("elections"), S["elections"])
    R.add("C0", "elections == schema (cc)", cc.get("elections") == S["elections"], cc.get("elections"), S["elections"])
    R.add("C0", "independence witness: instrument_md5 differ", bool(chat.get("instrument_md5")) and bool(cc.get("instrument_md5")) and chat.get("instrument_md5") != cc.get("instrument_md5"), chat.get("instrument_md5"), cc.get("instrument_md5"))
    # ---------------- C1 phase0 ----------------
    P0 = S["phase0"]; A, B = chat.get("phase0", {}), cc.get("phase0", {})
    cmp_exact_block(R, "C1", "phase0", A, B, P0["exact_keys"],
                    harmonize={"sym_int_continuous": harm_sym_int_label, "sym_int_continuous_dim": harm_sym_int_dim})
    for k, dom in P0["domains"].items():
        if k == "H0": continue
        domain_check(R, "C1", "phase0", A, B, k, dom)
    for k in CONTROL_TRUE:
        R.add("C1", f"phase0.controls.{k} true both legs", get(A, f"controls.{k}") is True and get(B, f"controls.{k}") is True, get(A, f"controls.{k}"), get(B, f"controls.{k}"))
    spec = P0["list_keys"]["locking_inventory"]
    la, lb = A.get("locking_inventory"), B.get("locking_inventory")
    okl = isinstance(la, list) and isinstance(lb, list) and len(la) == len(lb)
    R.add("C1", "locking_inventory list length equal", okl, len(la) if isinstance(la, list) else None, len(lb) if isinstance(lb, list) else None)
    if okl:
        la = sorted(la, key=lambda x: x.get(spec["sort_by"], -1)); lb = sorted(lb, key=lambda x: x.get(spec["sort_by"], -1))
        for ia, ib in zip(la, lb):
            cmp_exact_block(R, "C1", f"locking_inventory[rank={ia.get('rank')}]", ia, ib, spec["item_keys"])
            R.add("C1", f"locking_inventory[rank={ia.get('rank')}].H0 in domain", ia.get("H0") in P0["domains"]["H0"] and ib.get("H0") in P0["domains"]["H0"], ia.get("H0"), ib.get("H0"))
    # ---------------- C2 phase1 ----------------
    P1 = S["phase1"]; A, B = chat.get("phase1", {}), cc.get("phase1", {})
    for blk in ("T1", "T2", "T3", "T4", "group1344"):
        cmp_exact_block(R, "C2", f"phase1.{blk}", A.get(blk), B.get(blk), P1[blk]["exact_keys"],
                        harmonize={"spinor_2O_automorphism_count": harm_aut_count} if blk == "T2" else None)
        if "float_keys" in P1[blk]:
            cmp_float_block(R, "C2", f"phase1.{blk}", A.get(blk), B.get(blk), P1[blk]["float_keys"])
    # ---------------- C3 phase1b ----------------
    P1b = S["phase1b"]; A, B = chat.get("phase1b", {}), cc.get("phase1b", {})
    cmp_exact_block(R, "C3", "phase1b.P_C", A.get("P_C"), B.get("P_C"), P1b["P_C"]["exact_keys"])
    for h in P1b["H_screen_candidates"]:
        ha, hb = get(A, f"H_screen.{h}"), get(B, f"H_screen.{h}")
        harm = None
        if h == "H5":
            harm = {"i": make_h5_harmonizer(A.get("P_C"), B.get("P_C"), "i"), "code": make_h5_harmonizer(A.get("P_C"), B.get("P_C"), "code")}
        cmp_exact_block(R, "C3", f"phase1b.H_screen.{h}", ha, hb, P1b["H_item_keys"], harmonize=harm)
        for crit in ("i", "ii", "iii", "iv"):
            domain_check(R, "C3", f"phase1b.H_screen.{h}", ha, hb, crit, P1b["H_criterion_domain"])
    cmp_exact_block(R, "C3", "phase1b", A, B, P1b["exact_keys"])
    # ---------------- C4 phase2 ----------------
    P2 = S["phase2"]; A, B = chat.get("phase2", {}), cc.get("phase2", {})
    cmp_exact_block(R, "C4", "phase2", A, B, P2["exact_keys"])
    cmp_float_block(R, "C4", "phase2", A, B, P2["float_keys"])
    domain_check(R, "C4", "phase2", A, B, "label", P2["domains"]["label"])
    # ---------------- C5 phase3 ----------------
    P3 = S["phase3"]; A, B = chat.get("phase3", {}), cc.get("phase3", {})
    cmp_exact_block(R, "C5", "phase3", A, B, P3["exact_keys"])
    domain_check(R, "C5", "phase3", A, B, "verdict", P3["verdict_domain"])
    for leg, ck, D in (("chat", chat, A), ("cc", cc, B)):
        rv = recompute_verdict(ck)
        R.add("C5", f"verdict recomputed == reported ({leg})", rv == D.get("verdict"), rv if leg == "chat" else None, rv if leg == "cc" else None, f"reported {D.get('verdict')}")
        rc = recompute_controls(ck)
        R.add("C5", f"controls_all_pass recomputed == reported ({leg})", rc == D.get("controls_all_pass"), rc if leg == "chat" else None, rc if leg == "cc" else None)
        th = sorted(t for t in ("T1", "T2", "T3", "T4") if get(ck, f"phase1.{t}.holds") is True)
        R.add("C5", f"tests_holding consistent with T*.holds ({leg})", sorted(D.get("tests_holding") or []) == th, th if leg == "chat" else None, th if leg == "cc" else None)
        R.add("C5", f"admissible_H == phase1b.admissible ({leg})", sorted(D.get("admissible_H") or []) == sorted(get(ck, "phase1b.admissible") or []), None, None)
        R.add("C5", f"I5 == phase1b.I5_registered ({leg})", D.get("I5") == get(ck, "phase1b.I5_registered"), None, None)
    return R

# ---------------------------------------------------------------- selftest
def canonical_checkpoint(leg):
    """A synthetic checkpoint carrying the memo's a-priori expected values (H-A1-1..4). NOT a result —
    the instrument writes its own; this exists so the comparator's logic is exercised before any emission."""
    S = json.load(open(SCHEMA_DEFAULT, encoding="utf-8")) if _have_schema() else None
    prov = {k: (S[k] if S else "x") for k in ("memo_lock_md5", "ledger_base_md5", "t1_list_md5", "action_extract_md5")}
    el = S["elections"] if S else {f"E-A1-{i}": "a" for i in range(1, 9)}
    inv = [
        {"rank": 0, "H0": "G2", "H0_dim": 14, "pi0_generic": 1, "sl2_generator_jordan_type": [2, 2, 1, 1, 1], "sl2_generator_index": 1, "pi3_injective": True, "pi4_quotient": 0},
        {"rank": 1, "H0": "SU3", "H0_dim": 8, "pi0_generic": 1, "sl2_generator_jordan_type": [2, 2, 1, 1, 1], "sl2_generator_index": 1, "pi3_injective": True, "pi4_quotient": 0},
        {"rank": 2, "H0": "SU2_long", "H0_dim": 3, "pi0_generic": 1, "sl2_generator_jordan_type": [2, 2, 1, 1, 1], "sl2_generator_index": 1, "pi3_injective": True, "pi4_quotient": 0},
    ]
    ck = {
        "gate": "G-2a-A1", "leg": leg, "instrument_md5": "chat" * 8 if leg == "chat" else "cc00" * 8,
        **prov, "t1_scan": {"instrument": "CLEAN", "memo": "CLEAN", "extract": "CLEAN"}, "elections": el,
        "phase0": {"field_real_components": 16, "complex_amplitudes": 8, "spinor_index_present": False,
                   "spatial_internal_direct_product": True, "sym_int_pinned": True, "sym_int_continuous": "G2", "sym_int_continuous_dim": 14,
                   "g2_preserves_O": True, "generic_so16_breaks_O": True, "phase_subgroup_order": 3, "O_phase_invariant": False,
                   "conjugation_maps_O_to_conjugate": True, "two_body_symmetry": "O(16)", "vacuum_manifold_of_record": "S15", "pi1_V": 0, "pi4_V": 0,
                   "real_unit_splitting_term_present": False,
                   "controls": {"L_perp_zero_mode": True, "F21_split_1_3_3bar": True, "generic_so16_fails_margin_positive": True},
                   "locking_inventory": inv if leg == "chat" else list(reversed(inv))},
        "phase1": {
            "T1": {"holds": True, "chi32_norm": 1, "chi32_at_1": 4, "chi32_at_minus1": -4, "fs_indicator": -1, "seven_real": True, "quartet_multiplicity_upper": 0,
                   "phase_char_on_2O_trivial": True, "branching_long_root": [2, 2, 1, 1, 1], "branching_short_root": [3, 2, 2], "branching_su3_sl2": [3, 3, 1], "branching_principal": [7], "control_sym3_quartet_mult": 1},
            "T2": {"holds": True, "dim_der": 14, "dim_bivectors_7": 21, "dim_bivectors_6": 15, "g2_in_spin7": True, "dim_g2_cap_su4": 8, "spinor_2O_order": 48,
                   "spinor_2O_automorphism_count": 0, "spinor_2O_quartet_mult": 2, "sl27_order": 336, "sl27_sq1_count": 2, "fs_sum_ordinary": 22, "nu4_allowed": [-1, 0] if leg == "chat" else [0, -1],
                   "involution_trace": -1, "sigma_H_is_automorphism": True, "single_unit_negation_is_automorphism": False, "control_1344_all_automorphisms": True, "group1344_order": 1344,
                   "spinor_2O_min_automorphism_defect": 0.5 if leg == "chat" else 0.37},
            "T3": {"holds": True, "pi1_G2": 0, "pi3_G2": "Z", "pi4_G2": 0, "pi1_V": 0, "pi4_V": 0, "no_internal_double_cover": True, "envelope_in_O_kill": True,
                   "controls_pi4_S2": "Z2", "controls_pi4_S3": "Z2", "controls_pi1_SO3_mod_T": 24},
            "T4": {"holds": True, "lifts_total": 24, "order2_count": 12, "order2_traces_set": [-1], "order4_count": 12, "order4_traces_set": [3, -1] if leg == "chat" else [-1, 3],
                   "perm_char_involution": 3, "rho6_char_2A": 2, "gap": 4, "control_F21_unsigned_1_3_3bar": True, "nu2_unsigned_automorphism": True},
            "group1344": {"order": 1344, "split": False, "complements_found": 0, "lift_pairs_tested": 64},
        },
        "phase1b": {"P_C": {"complex_unit_central": True, "e8_anticommutes": True, "e8_central": False, "disposition": "CLOSED-BY-INSTANTIATION"},
                    "H_screen": {"H1": {"i": "fail", "ii": "pass", "iii": "fail", "iv": "n/a", "code": "EXCLUDED(i,iii)", "role": "control"},
                                 "H2": {"i": "pass", "ii": "pass", "iii": "pass", "iv": "dynamical", "code": "ADMISSIBLE-IMPORT", "role": "candidate"},
                                 "H3": {"i": "pass", "ii": "pass", "iii": "conditional", "iv": "kinematic", "code": "ADMISSIBLE-IMPORT", "role": "candidate"},
                                 "H4": {"i": "fail", "ii": "pass", "iii": "n/a", "iv": "n/a", "code": "EXCLUDED(i)", "role": "candidate"},
                                 "H5": {"i": "pass", "ii": "fail", "iii": "n/a", "iv": "n/a", "code": "EXCLUDED(ii,centrality)", "role": "candidate"}},
                    "I5_registered": True, "admissible": ["H2", "H3"] if leg == "chat" else ["H3", "H2"]},
        "phase2": {"object": "fano_line_texture_L124_homogeneous_GP_2D", "control_object": "nonline_texture_L123", "profile_id": "lockrec-A-2.6",
                   "O_nonzero_on_line": True, "O_zero_on_nonline": True, "stab_internal_image": "SO4_Stab_HL", "stab_kernel": "SU2_long", "stab_subdirect": True,
                   "pi0_stab": 1, "loop_images": ["Id", "sigma_H"], "sigma_H_eigen_plus1": 4, "sigma_H_eigen_minus1": 4, "label": "INTERNAL-HOLONOMY-GAUGE",
                   "pi1_orbit": 0, "chiral_pair_character_ordinary": True, "dimension_note": "2D witness; contractibility of the 2pi loop in the orbit only",
                   "O_line_abs": 0.2 if leg == "chat" else 0.31, "O_nonline_abs": 0.0},
        "phase3": {"verdict": "ASSIGNMENT-I-FORCED", "tests_holding": ["T1", "T2", "T3", "T4"], "admissible_H": ["H2", "H3"], "I5": True, "controls_all_pass": True},
    }
    return ck

def _have_schema():
    try:
        open(SCHEMA_DEFAULT, "rb").close(); return True
    except OSError:
        return False

def run(chat, cc, S):
    R = compare(chat, cc, S); s = R.summary(); return R, s

def selftest():
    S, h = load_schema(SCHEMA_DEFAULT)
    suites = []
    def suite(name, mut, expect_miss_min=1, expect_pass=False):
        a, b = canonical_checkpoint("chat"), canonical_checkpoint("cc")
        mut(a, b)
        R, s = run(a, b, S)
        ok = (s["miss"] == 0) if expect_pass else (s["miss"] >= expect_miss_min)
        suites.append((name, ok, s))
        return R
    suite("S1 canonical legs (list orders permuted, floats differ) -> ALL PASS", lambda a, b: None, expect_pass=True)
    suite("S2 T1.holds flipped on cc -> C2 miss + C5 verdict mismatch", lambda a, b: b["phase1"]["T1"].__setitem__("holds", False), 2)
    suite("S3 missing required key (phase2) on chat", lambda a, b: a.pop("phase2"), 1)
    suite("S4 wrong election code", lambda a, b: a["elections"].__setitem__("E-A1-2", "b"), 1)
    suite("S5 T1 scan HIT on memo (cc)", lambda a, b: b["t1_scan"].__setitem__("memo", "HIT"), 1)
    suite("S6 verdict inconsistent with booleans (both legs report II while all hold)", lambda a, b: (a["phase3"].__setitem__("verdict", "ASSIGNMENT-II-REALIZABLE"), b["phase3"].__setitem__("verdict", "ASSIGNMENT-II-REALIZABLE")), 2)
    suite("S7 identical instrument md5 (independence witness)", lambda a, b: b.__setitem__("instrument_md5", a["instrument_md5"]), 1)
    suite("S8 float rule: automorphism defect below threshold (chat)", lambda a, b: a["phase1"]["T2"].__setitem__("spinor_2O_min_automorphism_defect", 1e-9), 1)
    suite("S9 control failure -> INDETERMINATE recomputed vs reported", lambda a, b: a["phase1"]["T3"].__setitem__("controls_pi4_S2", "0"), 1)
    suite("S10 provenance md5 mismatch (ledger base)", lambda a, b: a.__setitem__("ledger_base_md5", "deadbeef" * 4), 1)
    suite("S11 locking inventory H0 out of domain", lambda a, b: b["phase0"]["locking_inventory"][0].__setitem__("H0", "SO4"), 1)
    suite("S12 H-screen criterion out of domain", lambda a, b: a["phase1b"]["H_screen"]["H2"].__setitem__("iii", "maybe"), 1)
    suite("S13 direct product false on both legs -> verdict must be II (reported I) -> C5 miss", lambda a, b: (a["phase0"].__setitem__("spatial_internal_direct_product", False), b["phase0"].__setitem__("spatial_internal_direct_product", False)), 2)
    suite("S14 typed: int given as bool", lambda a, b: a["phase1"]["T4"].__setitem__("gap", True), 1)
    suite("S15 phase2 nonline O not zero (cc)", lambda a, b: b["phase2"].__setitem__("O_nonline_abs", 1e-3), 1)
    # ---- v1.1 harmonization suites
    def run1_conventions(a, b):
        a["phase0"]["sym_int_continuous"] = "G2xU1_psi0"; a["phase0"]["sym_int_continuous_dim"] = 15
        a["phase1"]["T2"]["spinor_2O_automorphism_count"] = 1
        a["phase1b"]["H_screen"]["H5"] = {"i": "fail", "ii": "fail", "iii": "n/a", "iv": "n/a", "code": "EXCLUDED(i,ii)", "role": "candidate"}
    suite("S16 run-1 recording conventions (chat G2xU1_psi0/15, count 1, H5 EXCLUDED(i,ii) vs cc G2/14, 0, EXCLUDED(ii,centrality)) -> ALL PASS", run1_conventions, expect_pass=True)
    suite("S17 R1.1-1 must not pass a genuine dimension disagreement (chat G2/15 vs cc G2/14)", lambda a, b: a["phase0"].__setitem__("sym_int_continuous_dim", 15), 1)
    suite("S18 R1.1-1 must not pass a genuine label disagreement (chat SU4 vs cc G2)", lambda a, b: a["phase0"].__setitem__("sym_int_continuous", "SU4"), 1)
    suite("S19 R1.1-2 must not pass count 2 vs 0", lambda a, b: a["phase1"]["T2"].__setitem__("spinor_2O_automorphism_count", 2), 1)
    suite("S20 R1.1-2 must not pass count 1 vs 0 when a leg's min defect is at the floor", lambda a, b: (a["phase1"]["T2"].__setitem__("spinor_2O_automorphism_count", 1), b["phase1"]["T2"].__setitem__("spinor_2O_min_automorphism_defect", 1e-9)), 1)
    suite("S21 R1.1-3 must not pass H5 ADMISSIBLE-IMPORT vs EXCLUDED, nor an inconsistent booking (i fail with 'centrality' code)", lambda a, b: a["phase1b"]["H_screen"].__setitem__("H5", {"i": "fail", "ii": "fail", "iii": "n/a", "iv": "n/a", "code": "EXCLUDED(ii,centrality)", "role": "candidate"}), 1)
    suite("S22 R1.1-3 must not pass when P_C disagrees (cc e8_central true)", lambda a, b: (run1_conventions(a, b), b["phase1b"]["P_C"].__setitem__("e8_central", True)), 1)
    allok = all(ok for _, ok, _ in suites)
    print(f"schema md5 {h}")
    for name, ok, s in suites:
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}  (checks={s['checks']}, pass={s['pass']}, miss={s['miss']})")
    print("SELFTEST", "PASS" if allok else "FAIL")
    return 0 if allok else 1

def main():
    if len(sys.argv) < 2: print(__doc__); return 2
    if sys.argv[1] == "selftest": return selftest()
    if sys.argv[1] == "compare":
        args = sys.argv[2:]
        schema = SCHEMA_DEFAULT; out = None
        if "--schema" in args:
            i = args.index("--schema"); schema = args[i + 1]; del args[i:i + 2]
        if "--out" in args:
            i = args.index("--out"); out = args[i + 1]; del args[i:i + 2]
        if len(args) != 2: print(__doc__); return 2
        S, h = load_schema(schema)
        chat = json.load(open(args[0], encoding="utf-8")); cc = json.load(open(args[1], encoding="utf-8"))
        R, s = run(chat, cc, S)
        res = {"comparator": "g_2a_a1_compare_v1_1_CANDIDATE", "schema_md5": h, "chat_ckpt_md5": md5_file(args[0]), "cc_ckpt_md5": md5_file(args[1]),
               "summary": s, "misses": [r for r in R.rows if not r["pass"]], "rows": R.rows}
        txt = json.dumps(res, indent=1, ensure_ascii=False, sort_keys=True)
        if out: open(out, "w", encoding="utf-8").write(txt)
        print(f"G-2a-A1 two-leg comparison: checks={s['checks']} pass={s['pass']} miss={s['miss']}")
        for r in res["misses"]: print(f"  MISS [{r['check']}] {r['name']}: chat={r['chat']} cc={r['cc']} {r['note']}")
        return 0 if s["miss"] == 0 else 1
    print(__doc__); return 2

if __name__ == "__main__":
    sys.exit(main())
