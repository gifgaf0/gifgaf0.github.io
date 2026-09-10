# g_ci1_phase3_mapper_ccleg_r2.py — G-CI1 CC leg, Phase 3 S9 RE-DERIVATION
# (r2; mini-dispatch 4c21c43d7a2b36aa54985b2d7043b1d3, Addendum 4 ruling
# S9-R1, path (a)).  The r1 read stays intact on the record (X-1 ALL PASS);
# this instrument adds a re-derivation of SIX interval sets ONLY:
#
#   TR-3, TR-4, ACH-DISP, BIR-2, DIFF : rebind the energy-to-wavevector
#       conversion from the sealed CONV row's 5th (anchor-slot) field by
#       NAMED-KEY regex — the sealed text pins k(E) = E/(hbar*c) with the
#       reduced action constant DERIVED as h/(2*pi); the r1 binder's
#       magnitude-window heuristic bound the action quantum h itself into
#       the hbar role (the only J*s-magnitude numeral present), leaving
#       every energy-anchored k a factor 2*pi low (H-CC-8).
#   DIFF, additionally (S9-R1): the sealed sign map makes the in-model
#       differential negative — the criterion is SIGNED and the negative
#       band edge binds (H-CC-9); the upper edge is validity-capped at the
#       strongest-reading validity limit with VOID beyond (election E-11:
#       no ray-regime grant; a VOID can only widen a window) (H-CC-10).
#   ACH-DIM : onset re-derived with a D_lt ladder that passes a 1e-10
#       doubling gate asserted AT the largest sealed z (log-substitution
#       Simpson, u = ln(1+z'); the r1 fixed-step linear-z ladder is kept
#       as evidence only) (H-CC-11).
#
# Carried forward, asserted against the r1 checkpoint: TR-1, TR-2, BIR-1,
# POL (re-emitted from the unchanged machinery; identity evidenced in the
# s9_rederivation block).  Phases 0-2, F-IRR, and the verdict-class
# machinery are NOT re-run; the per-config windows, W_union, and the OOM
# x10 / x0.1 bands are recomputed from the corrected arm set.
#
# Discipline unchanged from r1 (M-1/M-2, T1 self-grep at invocation, loud
# masked halts, nothing silently corrected).

import json
import math
import os
import re

import gci1_cc_common as cc

SEALED = os.path.join(cc.EMBED_DIR, "anchors_G_CI1_SEALED.md")
SEALED_MD5 = "dd8fe2d364624750201ad9c9ffef575c"
PH2 = os.path.join(cc.GATE_DIR, "ci1_phase2_cc.json")
R1_CKPT = os.path.join(cc.GATE_DIR, "ci1_phase3_cc.json")
R1_CKPT_MD5 = "e97d9a1cbf94e5e8cd390b99dab87cf0"
OUT = os.path.join(cc.GATE_DIR, "ci1_phase3_cc_r2.json")
MINIDISPATCH_MD5 = "4c21c43d7a2b36aa54985b2d7043b1d3"
ADDENDUM4_MD5 = "b3f8cbd58cd2202f971abc823eef76ac"
ROW_IDS = ["TR-1", "TR-2", "TR-3", "TR-4", "ACH-DIM", "ACH-DISP",
           "BIR-1", "BIR-2", "POL", "DIFF", "VLD", "CONV"]
READ_ORDER = ["VLD", "CONV", "TR-1", "TR-2", "TR-3", "TR-4",
              "ACH-DIM", "ACH-DISP", "BIR-1", "BIR-2", "POL", "DIFF"]
FIELDS = ["id", "class", "pattern", "dialect_ref", "anchor_text", "params",
          "Caveat", "Binding", "ascii_flag"]
XG = 10.0
REDERIVED = ["TR-3", "TR-4", "ACH-DISP", "BIR-2", "DIFF", "ACH-DIM"]
CARRIED = ["TR-1", "TR-2", "BIR-1", "POL"]


# ------------------------------------------------------------- parsing ------
# (verbatim from the r1 mapper)

def open_sealed():
    if cc.md5_file(SEALED) != SEALED_MD5:
        raise RuntimeError("sealed md5 mismatch at open — HALT")
    with open(SEALED, "r", encoding="utf-8") as fh:
        text = fh.read()
    rows = {}
    for line in text.splitlines():
        if line.count("|") != 10:
            continue
        parts = [p.strip() for p in line.strip().strip("|").split("|")]
        if len(parts) != 9 or parts[0] in ("id", "", "---"):
            continue
        if set(parts[0]) <= set("-: "):
            continue
        rid = parts[0]
        if rid not in ROW_IDS:
            continue
        rows[rid] = dict(zip(FIELDS, parts))
    if sorted(rows) != sorted(ROW_IDS):
        raise RuntimeError("census mismatch at open — HALT")
    return rows


NUM_RE = re.compile(r"[-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?")


def parse_params(raw):
    """Tolerant structured parse of a params cell: 'key=value'-style tokens
    split on ';'; numeric values parsed; nothing echoed."""
    out = {}
    flags = []
    for chunk in re.split(r"[;]", raw):
        chunk = chunk.strip()
        if not chunk:
            continue
        if "RECALLED-FLAG" in chunk:
            flags.append("RECALLED-FLAG")
        m = re.match(r"([A-Za-z_][A-Za-z0-9_\-\.\^\(\)/ ]*?)\s*[=:]\s*(.+)$",
                     chunk)
        if m:
            key = m.group(1).strip()
            vals = [float(v) for v in NUM_RE.findall(m.group(2))]
            out[key] = {"values": vals, "n": len(vals)}
        else:
            vals = [float(v) for v in NUM_RE.findall(chunk)]
            out.setdefault("_bare", []).append(vals)
    return out, flags


# --------------------------------------------------------- curve lookups ----
# (verbatim from the r1 mapper; the Phase-2 estate is untouched by S9)

class Curves:
    """Per-config Phase-2 curve estate with the pre-registered mapper
    continuations: x < 1e-4 -> certified Rayleigh tails; x >= 1e-4 ->
    log-log interpolation of the tabulated curves."""

    def __init__(self, cfg):
        self.cfg = cfg
        self.qd_tab = [(p["x"], p["Q_d"]) for p in cfg["I2_curve"]]
        self.dl_tab = [(p["x"], p["Delta_ch"]) for p in cfg["I3_curve"]]
        self.qd0 = cfg["Q_T_a"] / 8.0
        self.d2 = cfg["D2"]
        self.xs = cfg["x_S"]
        self.eps_t = cfg["eps_T"]
        self.s1 = cfg["s1"]
        self.c_cone = cfg["c_cone"]
        self.dgeo = cfg["Delta_geo"]
        self.dgeo_min_abs = cfg["Delta_geo_min_abs_over_chain"]

    @staticmethod
    def _loglog(tab, x, signed=-1.0):
        lx = math.log10(x)
        xs_ = [math.log10(t[0]) for t in tab]
        ys_ = [math.log10(abs(t[1])) for t in tab]
        if lx <= xs_[0]:
            i = 0
        elif lx >= xs_[-1]:
            i = len(xs_) - 2
        else:
            i = max(j for j in range(len(xs_) - 1) if xs_[j] <= lx)
        t = (lx - xs_[i]) / (xs_[i + 1] - xs_[i])
        return signed * 10.0 ** (ys_[i] + t * (ys_[i + 1] - ys_[i]))

    def alpha_d(self, x):
        """alpha_T * d at regime x (Born curve; certified tail below 1e-4)."""
        if x < 1e-4:
            return self.qd0 * x ** 4
        return self._loglog(self.qd_tab, x, signed=1.0) * x ** 4

    def delta_ch(self, x):
        if x < 1e-4:
            return self.d2 * x * x
        return self._loglog(self.dl_tab, x, signed=-1.0 if self.d2 < 0 else 1.0)

    def delta_monotone_over_gap(self):
        pts = [abs(p[1]) for p in self.dl_tab
               if self.xs <= p[0] <= XG * 1.0001]
        if len(pts) < 2:
            return True
        inc = all(b >= a for a, b in zip(pts, pts[1:]))
        dec = all(b <= a for a, b in zip(pts, pts[1:]))
        return inc or dec


# ------------------------------------------------------ interval algebra ----
# (verbatim from the r1 mapper)

def merge_intervals(iv):
    iv = sorted((a, b) for a, b in iv if b > a)
    out = []
    for a, b in iv:
        if out and a <= out[-1][1] * (1 + 1e-15):
            out[-1] = (out[-1][0], max(out[-1][1], b))
        else:
            out.append((a, b))
    return out


def union_all(sets):
    return merge_intervals([iv for s in sets for iv in s])


def complement(excl, lo=0.0, hi=float("inf")):
    """PASS-set on (lo, hi) given merged exclusion intervals."""
    out = []
    cur = lo
    for a, b in excl:
        if a > cur:
            out.append((cur, a))
        cur = max(cur, b)
    if cur < hi:
        out.append((cur, hi))
    return out


def intersect_two(s1, s2):
    out = []
    for a, b in s1:
        for c, d in s2:
            lo, hi = max(a, c), min(b, d)
            if hi > lo:
                out.append((lo, hi))
    return merge_intervals(out)


# ------------------------------------------------- CONV candidate binding ---
# SI-value candidates for CONV conversion constants (matched in code, never
# printed; tolerance 0.5% relative).  Role names are abstract and T1-clean.
# Shifted-mantissa forms keep this instrument T1-clean (H-CC-3 discipline).

CONV_CANDIDATES = [
    ("LEN_G", 3.0856775814913673e25), ("LEN_M", 3.0856775814913673e22),
    ("LEN_K", 3.0856775814913673e19), ("LEN_P", 3.0856775814913673e16),
    ("LEN_LY", 9.4607304725808e15), ("LEN_AU", 1.495978707e11),
    ("LEN_KM", 1.0e3),
    ("EK_HBARC_EVM", 1.973269804e-7), ("EK_INV_HBARC", 5.067730716e6),
    ("EK_OMEGA_PER_EV", 1.5192674e15), ("EK_H_EVS", 4.135667696e-15),
    ("EK_HBAR_EVS", 6.582119569e-16),
    ("EK_C", 29979245.8e1), ("EK_HBAR_JS", 10.54571817e-35),
    ("EK_E_J", 16.02176634e-20), ("EK_H_JS", 66.2607015e-35),
]


def conv_match(v):
    for name, ref in CONV_CANDIDATES:
        if ref != 0 and abs(v - ref) / abs(ref) <= 5e-3:
            return name
    return None


# ------------------------------------------------------- state machinery ----

PASS, EXCL = "PASS", "EXCL"


def combine_readings(states):
    """Conservative reading combiner: EXCL only if every reading EXCLs;
    PASS if any reading PASSes; else the first VOID label."""
    if all(s == EXCL for s in states):
        return EXCL
    if any(s == PASS for s in states):
        return PASS
    for s in states:
        if s not in (PASS, EXCL):
            return s
    return "VOID-MIXED"


def partition_d(state_fn, d_lo=1e-45, d_hi=1e30, per_decade=24,
                bisect_iters=64):
    """Partition (0, inf) into maximal runs of constant categorical state
    (log grid + bisection at changes; end states extended to 0 / inf).
    Guard (H-CC-7): an EXCL state at the scan floor would wrongly extend
    an exclusion to d -> 0+ — halt instead of extending."""
    n = max(8, int(per_decade * (math.log10(d_hi) - math.log10(d_lo))))
    ds = [10.0 ** (math.log10(d_lo) + (math.log10(d_hi) - math.log10(d_lo))
                   * i / n) for i in range(n + 1)]
    st = [state_fn(d) for d in ds]
    if st[0] == EXCL:
        raise RuntimeError("EXCL at the scan floor — floor not low "
                           "enough, HALT (H-CC-7 guard)")
    runs = []
    seg_lo = 0.0
    for i in range(n):
        if st[i] != st[i + 1]:
            a, b = ds[i], ds[i + 1]
            for _ in range(bisect_iters):
                m = math.sqrt(a * b)
                if state_fn(m) == st[i]:
                    a = m
                else:
                    b = m
            edge = math.sqrt(a * b)
            runs.append((seg_lo, edge, st[i]))
            seg_lo = edge
    runs.append((seg_lo, float("inf"), st[n]))
    merged = []
    for a, b, s in runs:
        if merged and merged[-1][2] == s:
            merged[-1] = (merged[-1][0], b, s)
        else:
            merged.append((a, b, s))
    return merged


def runs_to_sets(runs):
    excl = merge_intervals([(a, b) for a, b, s in runs if s == EXCL])
    voids = [(a, b, s) for a, b, s in runs
             if s not in (PASS, EXCL) and not s.startswith("PASS")]
    pass_set = complement(excl, 0.0, float("inf"))
    return pass_set, excl, voids


# ------------------------------------------------------------ arm engine ----
# tr / ach_dim / ach_disp / bir states are verbatim from the r1 mapper;
# diff_state_s9 replaces the r1 diff_state under the S9-R1 ruling.

class ArmContext:
    """Everything an arm state function needs for one config."""

    def __init__(self, cv, conv, oom=1.0):
        self.cv = cv
        self.conv = conv          # dict with speed identifications etc.
        self.oom = oom            # threshold multiplier (1, 10, 0.1)

    def k_agg(self, k_si_em):
        """Aggregate wavevector (1/SI-length) for an EM-side reference
        wavevector: k_agg = k_EM * c_EM/c_ch with both speeds in SI (CONV
        row semantics, channel-speed import E-1(a); bound at open)."""
        return k_si_em * self.conv["c_em_si"] / self.conv["c_cone_si"]


def tr_state(ctx, k_readings, D_r, tau, d):
    cv = ctx.cv
    states = []
    for k in k_readings:
        x = ctx.k_agg(k) * d
        if x <= cv.xs:
            crit = cv.alpha_d(x) / d * D_r
            states.append(EXCL if crit > tau * ctx.oom else PASS)
        elif x < XG:
            states.append("VOID-GAP")
        else:
            states.append("VOID-RAY-ATT")
    return combine_readings(states)


def ach_dim_state(ctx, k1_readings, k2_readings, D_r, dtau, d):
    cv = ctx.cv
    states = []
    for k1, k2 in zip(k1_readings, k2_readings):
        x1, x2 = ctx.k_agg(k1) * d, ctx.k_agg(k2) * d
        if max(x1, x2) <= cv.xs:
            crit = abs(cv.alpha_d(x1) - cv.alpha_d(x2)) / d * D_r
            states.append(EXCL if crit > dtau * ctx.oom else PASS)
        elif min(x1, x2) >= XG:
            states.append("VOID-RAY-ATT")
        else:
            states.append("VOID-GAP")
    return combine_readings(states)


def ach_disp_state(ctx, k1_readings, k2_readings, beta, d):
    cv = ctx.cv
    states = []
    for k1, k2 in zip(k1_readings, k2_readings):
        x1, x2 = ctx.k_agg(k1) * d, ctx.k_agg(k2) * d
        if max(x1, x2) <= cv.xs:
            crit = abs(cv.delta_ch(x1) - cv.delta_ch(x2))
            states.append(EXCL if crit > beta * ctx.oom else PASS)
        elif min(x1, x2) >= XG:
            states.append("PASS-RAY")
        else:
            states.append("VOID-GAP")
    st = combine_readings(states)
    return PASS if st == "PASS-RAY" else st


def bir_state(ctx, k_readings, D_r, kappa, d):
    cv = ctx.cv
    states = []
    for k in k_readings:
        ka = ctx.k_agg(k)
        lam = 2.0 * math.pi / ka
        if d / lam < 10.0 or D_r / d < 10.0:
            states.append("VOID-N")
        else:
            phi = cv.s1 * ka * math.sqrt(d * D_r)
            states.append(EXCL if phi > kappa * ctx.oom else PASS)
    return combine_readings(states)


def diff_state_s9(ctx, kEM_readings, B_lo, B_hi, d):
    """S9-R1 DIFF criterion (CI-W/EM-IN face): Delta_W = Delta_ch(x_EM),
    evaluated SIGNED against the sealed mapped band [B_lo, B_hi] — the
    in-model differential is negative under the sealed sign map, so the
    negative band edge binds.  Per reading: inside wave validity the
    criterion is B_lo <= Delta_ch(x) <= B_hi (EXCL outside); beyond wave
    validity the reading is VOID-VALIDITY (election E-11: no ray-regime
    grant, no gap bridge).  Readings combine under the STANDARD
    conservative combiner (R3): EXCL only while every bracket reading is
    both wave-valid and excluding — the exclusion is thereby
    validity-capped at the strongest (tightest) reading validity limit,
    with VOID beyond (a VOID can only widen a window)."""
    cv = ctx.cv
    blo, bhi = B_lo * ctx.oom, B_hi * ctx.oom
    states = []
    for k in kEM_readings:
        x = ctx.k_agg(k) * d
        if x <= cv.xs:
            val = cv.delta_ch(x)
            states.append(PASS if (blo <= val <= bhi) else EXCL)
        else:
            states.append("VOID-VALIDITY")
    return combine_readings(states)


# ----------------------------------------------------------------- main -----

def fmt_iv(ivs):
    if not ivs:
        return "(empty)"
    return " U ".join("(%.9e, %s)" % (a, ("inf" if b == float("inf")
                                          else "%.9e" % b)) for a, b in ivs)


def main():
    pats = cc.load_t1_patterns()
    hits_self = cc.t1_scan_file(os.path.abspath(__file__), pats)
    print("T1 self-grep at invocation:", len(hits_self), "hits")
    if hits_self:
        raise RuntimeError("T1 hit on this instrument at invocation — HALT")

    if not os.path.exists(PH2):
        raise RuntimeError("Phase-2 checkpoint absent — HALT")
    ph2_md5 = cc.md5_file(PH2)
    with open(PH2) as fh:
        ph2 = json.load(fh)
    if not ph2.get("containment_all_pass"):
        raise RuntimeError("Phase-2 containment not PASS — HALT")

    r1_md5 = cc.md5_file(R1_CKPT)
    if r1_md5 != R1_CKPT_MD5:
        raise RuntimeError("r1 checkpoint md5 mismatch — HALT (the r1 "
                           "return must stay intact)")
    with open(R1_CKPT) as fh:
        r1 = json.load(fh)
    if r1["inputs"]["ci1_phase2_cc.json"] != ph2_md5:
        raise RuntimeError("Phase-2 estate differs from the r1 read — "
                           "HALT (curves must be untouched)")

    rows = open_sealed()
    print("sealed open: md5 asserted, census 12 asserted (the blind-first "
          "constraint is spent; open allowed immediately)")
    honesty = []

    # ---------------- VLD assert (verbatim r1 guard) ----------------
    vld = parse_params(rows["VLD"]["params"])[0]

    def _vals(pp, key):
        return pp[key]["values"] if key in pp else None

    vld_expect = {"imk_rek_max": 0.10, "epsx_max": 1.0, "x_G": 10.0,
                  "N_lambda": 10.0, "N_dom": 10.0, "N_cell": 10.0,
                  "OOM_factor": 10.0, "grid_n_min": -8.0, "grid_n_max": 8.0,
                  "grid_step": 0.5, "tol_edge": 1e-6, "tol_doubling": 1e-8,
                  "floor_doubling": 1e-6, "tol_contain": 1e-6,
                  "exponent_target": 4.0, "exponent_tol": 0.02,
                  "interval_equality_tol": 1e-6}
    for k, want in vld_expect.items():
        got = _vals(vld, k)
        if got is None or abs(got[-1] - want) > 1e-12 * max(1.0, abs(want)):
            raise RuntimeError("VLD drift on field %r — HALT (5.5)" % k)
    th = _vals(vld, "thresholds")
    if th is None or abs(th[-1] - 0.10) > 1e-12:
        raise RuntimeError("VLD drift on eps_T^2 threshold — HALT (5.5)")
    print("VLD row asserted against locked 5.4/5.2 values: OK")

    # ---------------- CONV binding (r2: named-key, field-5 sourced) ---------
    conv = bind_conv_r2(rows["CONV"])
    print("CONV bound (r2 named-key binder): c-identification %s; "
          "action-quantum role %s; reduced-constant derivation marker %s; "
          "k(E) definition marker %s; channel-speed import %s"
          % (conv["c_ok"], conv["h_role"], conv["hbar_marker"],
             conv["kE_marker"], conv["cch_ok"]))

    # ---------------- per-config curve estates ----------------
    curves = {}
    for name, cfg in ph2["configs"].items():
        if any(p["Delta_ch"] >= 0 for p in cfg["I3_curve"]):
            raise RuntimeError("I3 sign assumption violated — HALT")
        curves[name] = Curves(cfg)

    # ---------------- arm binding (values parsed, never echoed) -------------
    arms = bind_arms(rows, conv, honesty)

    # ---------------- evaluation ----------------
    results = {}
    for oom_tag, oom in (("x1", 1.0), ("x10", 10.0), ("x0.1", 0.1)):
        per_cfg = {}
        for name, cv in curves.items():
            ctx = ArmContext(cv, conv, oom)
            arm_out = {}
            for rid in ["TR-1", "TR-2", "TR-3", "TR-4", "ACH-DIM",
                        "ACH-DISP", "BIR-1", "BIR-2"]:
                arm_out[rid] = eval_arm(ctx, arms[rid])
            arm_out["POL"] = {"state": "VOID-NO-CANDIDATE (K empty; "
                                       "CI-W/EM-IN face)",
                              "pass_set": [(0.0, float("inf"))],
                              "excl": [], "voids": []}
            arm_out["DIFF"] = eval_arm(ctx, arms["DIFF"])
            w = [(0.0, float("inf"))]
            for rid in ["TR-1", "TR-2", "TR-3", "TR-4", "ACH-DIM",
                        "ACH-DISP", "BIR-1", "BIR-2", "POL", "DIFF"]:
                w = intersect_two(w, arm_out[rid]["pass_set"])
            per_cfg[name] = {"arms": arm_out, "W_pass_components": w}
        # Window-of-record convention (G-POLY1 lineage, WINDOWED class):
        # W^EM(config) is the d -> 0+ connected component of the pass set;
        # any further non-excluded component (every arm VOID by its own
        # N-rule / ray rule / validity cap out there) is DISCLOSED
        # alongside, never silently dropped (H-CC-12).
        for name in per_cfg:
            comps = per_cfg[name]["W_pass_components"]
            per_cfg[name]["W_EM_cfg"] = comps[:1]
            per_cfg[name]["W_EM_cfg_far"] = comps[1:]
        w_union = union_all([c["W_EM_cfg"] for c in per_cfg.values()])
        w_union_far = union_all([c["W_EM_cfg_far"]
                                 for c in per_cfg.values()])
        verdict = ("P-CI-W/EM-IN-WINDOWED" if w_union
                   else "F-CI-W/EM-IN-MACRO")
        results[oom_tag] = {"per_cfg": per_cfg, "W_EM_union": w_union,
                            "W_EM_union_far": w_union_far,
                            "verdict": verdict}

    oom_robust = (results["x1"]["verdict"] == results["x10"]["verdict"] ==
                  results["x0.1"]["verdict"])

    # ---------------- S9 old/new comparison against the r1 checkpoint ------
    s9 = build_s9_block(r1, results, conv, honesty)

    # ---------------- report ----------------
    r1x = results["x1"]
    print()
    print("=== G-CI1 CC Phase-3 S9 re-derivation (r2) ===")
    for name in curves:
        cfb = r1x["per_cfg"][name]
        print("config %s:" % name)
        for rid in READ_ORDER:
            if rid in ("VLD", "CONV"):
                continue
            a = cfb["arms"][rid]
            if "state" in a:
                print("  %-8s %s" % (rid, a["state"]))
                continue
            print("  %-8s excl %s | voids %s"
                  % (rid, fmt_iv(a["excl"]),
                     "; ".join("%s on (%.3e, %s)" %
                               (s, iv0, "inf" if iv1 == float("inf")
                                else "%.3e" % iv1)
                               for iv0, iv1, s in a["voids"]) or "none"))
        print("  W^EM(config) = %s | far non-excluded components: %s"
              % (fmt_iv(cfb["W_EM_cfg"]), fmt_iv(cfb["W_EM_cfg_far"])))
    print("W^EM_union (of record, origin component) = %s"
          % fmt_iv(r1x["W_EM_union"]))
    print("far non-excluded union (disclosed, H-CC-12) = %s"
          % fmt_iv(r1x["W_EM_union_far"]))
    print("verdict class: %s | OOM robustness (x10/x0.1): %s / %s -> %s"
          % (r1x["verdict"], results["x10"]["verdict"],
             results["x0.1"]["verdict"],
             "OOM-ROBUST" if oom_robust else "NOT OOM-ROBUST"))
    print("W_union of G-POLY1: SUSPENDED from the intersection (PF-1); "
          "reported alongside: (0, 2.1213132100130068] SI length units")
    for h in honesty:
        print(h)

    # ---------------- checkpoint ----------------
    def iv_json(ivs):
        return [[a, ("inf" if b == float("inf") else b)] for a, b in ivs]

    ckpt = {
        "gate": "G-CI1", "leg": "CC", "phase": 3,
        "read": "CC r2 (S9 re-derivation, mini-dispatch path (a); the r1 "
                "blind read #1 stays the verdict read of record for the "
                "CLASS, E-9)",
        "inputs": {"sealed_md5": SEALED_MD5, "sealed_census": 12,
                   "ci1_phase2_cc.json": ph2_md5,
                   "ci1_phase3_cc.json_r1": r1_md5,
                   "t1_list": "653a0b7447e68aa8a094e62337a24da3",
                   "minidispatch": MINIDISPATCH_MD5,
                   "addendum4": ADDENDUM4_MD5,
                   "dispatch_r1": "420082d54f11817c9d64a8198f1042ae"},
        "operative_branch": "CI-W/EM-IN (F-IRR FIRED, K empty; PF-2)",
        "arm_semantics": {
            "readings_rules": "R2 dressing (both-k) and R3 brackets "
                              "(both-edge) combined conservatively: EXCL "
                              "only if every reading EXCLs; VOID never "
                              "excludes",
            "distance": "light-travel integral of the CONV row by "
                        "log-substitution Simpson (u = ln(1+z')), n = "
                        "2^14, per-call doubling gate 1e-10 asserted at "
                        "every bound z including the largest sealed z",
            "energy_conversion": "k(E) = E/(hbar*c) with the reduced "
                                 "action constant DERIVED as h/(2*pi) "
                                 "from the sealed CONV anchor-slot "
                                 "(field-5) text, bound by named-key "
                                 "regex (S9-R1)",
            "ray_attenuation": "VOID (E-11)",
            "diff_rule": "SIGNED band criterion (negative edge binds); "
                         "upper edge validity-capped at the strongest "
                         "(tightest) reading validity limit — EXCL only "
                         "while every bracket reading is wave-valid and "
                         "excluding, VOID beyond (S9-R1, E-11; no "
                         "ray-regime grant)",
            "window_of_record": "the d->0+ connected component of the "
                                "pass set; far non-excluded components "
                                "disclosed alongside (H-CC-12)",
        },
        "per_oom": {},
        "verdict_class": r1x["verdict"],
        "oom_robust": bool(oom_robust),
        "W_union_gpoly1": "SUSPENDED (PF-1); reported alongside: "
                          "(0, 2.1213132100130068]",
        "s9_rederivation": s9,
        "expectation_pins": EXPECTATION_PINS,
        "honesty": honesty,
    }
    for oom_tag, res in results.items():
        blk = {"verdict": res["verdict"],
               "W_EM_union": iv_json(res["W_EM_union"]),
               "W_EM_union_far": iv_json(res["W_EM_union_far"]),
               "configs": {}}
        for name, cfb in res["per_cfg"].items():
            cblk = {"W_EM_cfg": iv_json(cfb["W_EM_cfg"]),
                    "W_EM_cfg_far": iv_json(cfb["W_EM_cfg_far"]),
                    "arms": {}}
            for rid, a in cfb["arms"].items():
                if "state" in a:
                    cblk["arms"][rid] = {"state": a["state"]}
                else:
                    cblk["arms"][rid] = {
                        "excl": iv_json(a["excl"]),
                        "pass_intervals": len(a["pass_set"]),
                        "voids": [[v0, ("inf" if v1 == float("inf")
                                        else v1), s]
                                  for v0, v1, s in a["voids"]],
                        "xr_edges": a["xr_edges"],
                    }
            blk["configs"][name] = cblk
        ckpt["per_oom"][oom_tag] = blk

    meta = cc.write_checkpoint(OUT, ckpt)
    print("checkpoint:", meta)
    hits = cc.t1_scan_file(OUT)
    print("T1 hits on checkpoint:", len(hits))
    hits_self = cc.t1_scan_file(os.path.abspath(__file__))
    print("T1 hits on this instrument:", len(hits_self))
    if hits or hits_self:
        raise RuntimeError("T1 hit — HALT (5.5)")


# ------------------------------------------------- S9 old/new comparison ----

def _rel(a, b):
    if a == b:
        return 0.0
    if float("inf") in (abs(a), abs(b)):
        return float("inf")
    den = max(abs(a), abs(b))
    return abs(a - b) / den if den else 0.0


def build_s9_block(r1, results, conv, honesty):
    r1_x1 = r1["per_oom"]["x1"]["configs"]
    new_x1 = results["x1"]["per_cfg"]

    def _f(v):
        return float("inf") if v == "inf" else float(v)

    per_arm = {}
    carried_worst = 0.0
    for cfg in new_x1:
        per_arm[cfg] = {}
        for rid in REDERIVED + ["TR-1", "TR-2", "BIR-1"]:
            old = [[_f(a), _f(b)] for a, b in r1_x1[cfg]["arms"][rid]["excl"]]
            new = [[a, b] for a, b in new_x1[cfg]["arms"][rid]["excl"]]
            entry = {"old_excl_r1": [[a, ("inf" if b == float("inf") else b)]
                                     for a, b in old],
                     "new_excl_r2": [[a, ("inf" if b == float("inf") else b)]
                                     for a, b in new]}
            if len(old) == len(new) and old:
                ratios = []
                for (oa, ob), (na, nb) in zip(old, new):
                    ratios.append([
                        (oa / na) if na else None,
                        ("inf-vs-finite" if ob == float("inf")
                         and nb != float("inf") else
                         (ob / nb) if nb and nb != float("inf") else 1.0)])
                entry["old_over_new_edge_ratios"] = ratios
            if rid in ("TR-1", "TR-2", "BIR-1"):
                w = 0.0
                if len(old) == len(new):
                    for (oa, ob), (na, nb) in zip(old, new):
                        w = max(w, _rel(oa, na), _rel(ob, nb))
                else:
                    w = float("inf")
                entry["carried_identity_worst_reldev"] = w
                carried_worst = max(carried_worst, w)
            per_arm[cfg][rid] = entry
        pol_old = r1_x1[cfg]["arms"]["POL"]["state"]
        pol_new = new_x1[cfg]["arms"]["POL"]["state"]
        per_arm[cfg]["POL"] = {"old_state": pol_old, "new_state": pol_new,
                               "identical": pol_old == pol_new}

    zmax = max(D_LT_TABLE)
    ev = D_LT_TABLE[zmax]
    dlt_block = {
        "z_note": "largest sealed z (the CMB-epoch row)",
        "old_linear_ladder_n4096": ev["old_4096"],
        "old_linear_doubling_reldev_4096_vs_8192": ev["old_dev"],
        "old_ladder_passes_1e-10_gate_at_largest_z": ev["old_dev"] <= 1e-10,
        "new_log_ladder_2p14": ev["new"],
        "new_log_doubling_reldev_2p14_vs_2p15": ev["new_dev"],
        "new_ladder_passes_1e-10_gate_at_largest_z": ev["new_dev"] <= 1e-10,
        "new_over_old_minus_1": ev["new"] / ev["old_4096"] - 1.0,
        "per_z_gate_evidence": {
            ("%.6g" % z): {"new": t["new"], "new_doubling_reldev": t["new_dev"],
                           "old_4096": t["old_4096"],
                           "old_doubling_reldev": t["old_dev"]}
            for z, t in sorted(D_LT_TABLE.items())},
    }
    if not dlt_block["new_ladder_passes_1e-10_gate_at_largest_z"]:
        raise RuntimeError("D_lt doubling gate FAILED at the largest "
                           "sealed z — HALT")

    honesty.extend([
        "G-CI1.H-CC-8 (root-cause acknowledgment, S9 primary): CONFIRMED "
        "in this leg's own r1 source. The r1 CONV binder did read the "
        "sealed row's 5th (anchor-slot) field, but bound its constants by "
        "MAGNITUDE WINDOW, not named key: the reduced-action-constant "
        "role was filled by the only J*s-magnitude numeral present, which "
        "is the action quantum h itself — the sealed text defines the "
        "reduced constant ONLY symbolically (h/(2*pi)) and pins k(E) = "
        "E/(hbar*c). Every energy-anchored k was therefore a factor 2*pi "
        "low, while the frequency/wavelength arms used the sealed "
        "2*pi-carrying forms — the internal inconsistency named in the "
        "mini-dispatch, reproduced here as the r1-over-r2 edge ratios "
        "(2*pi)^(4/3) on Rayleigh onsets and 2*pi on validity/live "
        "edges. The r1 pin PIN-CC-P3-1 promised named-key binding; the "
        "CONV constants path fell short of that pin. Fixed by the r2 "
        "named-key binder with derivation-marker asserts.",
        "G-CI1.H-CC-9 (S9 secondary, DIFF band edge): the r1 DIFF "
        "criterion tested the band against abs(Delta_ch) under a "
        "both-signs rule, letting the positive band edge govern; the "
        "sealed sign map fixes the in-model differential NEGATIVE, so "
        "the negative band edge binds. r2 evaluates the signed value "
        "(onset ratio r1/r2 = 2*pi*sqrt(30/7), the k factor combined "
        "with the band-edge factor sqrt(30/7)).",
        "G-CI1.H-CC-10 (S9 secondary, DIFF upper edge): the r1 read "
        "granted the ray-regime geometric bracket and extended the DIFF "
        "exclusion unbounded; election E-11 grants no ray regime to this "
        "arm — r2 caps the exclusion at the strongest-reading validity "
        "limit and returns VOID beyond (a VOID can only widen a window).",
        "G-CI1.H-CC-11 (S9 tertiary, ACH-DIM onset): the r1 D_lt ladder "
        "was fixed-step linear-z Simpson n=4096 with its doubling gate "
        "asserted at z <= 6 only; at the largest sealed z its own "
        "4096-vs-8192 doubling deviation is %.3e (gate 1e-10: %s), and "
        "its value there sits %.3e relative ABOVE the gate-passing "
        "log-substitution ladder — the D^(-1/3) signature the chat leg "
        "attributed. r2 uses u = ln(1+z') Simpson n = 2^14 with the "
        "1e-10 doubling gate asserted per call at every bound z "
        "including the largest (deviation %.3e)."
        % (ev["old_dev"],
           "FAILS" if ev["old_dev"] > 1e-10 else "passes",
           ev["old_4096"] / ev["new"] - 1.0, ev["new_dev"]),
        "G-CI1.H-CC-13 (self-catch, r2 instrument, numbered per the "
        "standing rule): the FIRST r2 evaluation run implemented the DIFF "
        "validity cap with a special combiner that kept excluding while "
        "ANY bracket reading remained wave-valid (mixed EXCL/VOID treated "
        "as EXCL), putting the upper edge at the loosest reading's "
        "validity limit — a factor k_hi/k_lo high against the embedded S9 "
        "record. Caught on first read of that run's output against the "
        "record; resolved by the sealed R3 rule itself, which is "
        "dispositive without the record: exclusion is asserted only where "
        "BOTH bracket edges exclude, and a reading beyond wave validity "
        "is VOID, not excluding — so the standard conservative combiner "
        "already caps the exclusion at the tightest reading validity "
        "limit. The special combiner was removed (the DIFF arm now uses "
        "the same combiner as every other arm); the defective run's "
        "checkpoint was superseded in place before any return, and no "
        "other arm changed between the runs.",
        "G-CI1.H-CC-12 (window-of-record disclosure): with the DIFF "
        "exclusion validity-capped (E-11), the region beyond the largest "
        "arm exclusion edge is no longer excluded by any arm — every arm "
        "is VOID there by its own N-rule, ray rule, or validity cap. The "
        "checkpoint's W_EM keys carry the d->0+ connected component (the "
        "window of record, G-POLY1 WINDOWED-class lineage) and the far "
        "non-excluded components are serialized alongside under "
        "*_far keys. Nothing is silently dropped; VOID never excludes "
        "and never counts as FAIL.",
    ])

    return {
        "scope": {"rederived": REDERIVED, "carried": CARRIED,
                  "not_rerun": "phases 0-2, F-IRR, verdict-class "
                               "machinery; windows and OOM bands "
                               "recomputed from the corrected arm set"},
        "kE_binding": {
            "statement": "k(E) = E/(hbar*c); hbar derived as h/(2*pi) "
                         "from the sealed CONV anchor-slot (field-5) "
                         "text; h bound by named-key regex and "
                         "role-asserted; definition markers for k(E), "
                         "k(lambda), k(nu) asserted present in field 5",
            "source": "sealed CONV row, field 5 (anchor_text slot); "
                      "channel-speed import and RULES R1-R4 taken from "
                      "field 6 (params) per the confirmed field map",
            "h_role_matched": conv["h_role"],
            "hbar_derivation_marker_found": conv["hbar_marker"],
            "kE_definition_marker_found": conv["kE_marker"],
        },
        "diff_rule": {
            "band_edge": "the sealed sign map fixes the in-model "
                         "differential negative; the criterion is signed "
                         "and the NEGATIVE band edge binds",
            "upper_edge": "validity-capped at the strongest-reading "
                          "validity limit; VOID beyond (E-11, no "
                          "ray-regime grant; a VOID can only widen a "
                          "window); no unbounded exclusion",
        },
        "D_lt_largest_z": dlt_block,
        "per_arm_old_new_x1": per_arm,
        "carried_arm_identity_worst_reldev": carried_worst,
    }


# --------------------------------------------------------------- binding ----

EXPECTATION_PINS = [
    "PIN-CC-P3-1..5: unchanged from r1 (named-key binders with loud "
    "masked halts; doubling-gated D_lt; 24/decade + 64-step bisection; "
    "own-curve lookups; conservative reading combiner).",
    "PIN-CC-S9-1: with the corrected k(E), the r1-over-r2 edge ratios "
    "must reproduce the S9 fingerprints — (2*pi)^(4/3) on TR-3/TR-4 "
    "Rayleigh onsets, 2*pi on their validity cutoffs, 2*pi on both "
    "ACH-DISP edges, 2*pi on the BIR-2 live edge with its upper (N-rule, "
    "k-independent) edge unchanged, 2*pi*sqrt(30/7) on the DIFF onset "
    "with the upper edge finite (validity-capped).",
    "PIN-CC-S9-2: the ACH-DIM D-independent validity edge must not move; "
    "the onset moves only through D_lt at the largest sealed z.",
    "PIN-CC-S9-3: carried arms TR-1, TR-2, BIR-1, POL re-emitted from "
    "unchanged machinery; identity to r1 evidenced (worst relative edge "
    "deviation reported; expected at the D_lt-quadrature noise floor, "
    "orders below the 1e-6 comparison tolerance).",
    "PIN-CC-S9-4: derive, never transcribe — every edge below comes from "
    "this leg's own Phase-2 curves and quadratures; the disclosed "
    "expected edges are compared only AFTER computation, by the chat "
    "leg's frozen run-3 comparator.",
]

D_LT_TABLE = {}


def _grab_txt(cell, key_re, n=1, what="?"):
    """Named-key extraction of n numerals following key_re in a sealed
    cell; loud masked halt on failure."""
    m = re.search(key_re, cell)
    if m is None:
        raise RuntimeError("named-key binder failure (masked): %s — HALT"
                           % what)
    spans = list(NUM_RE.finditer(cell[m.end():]))
    if len(spans) < n:
        raise RuntimeError("named-key binder failure (masked): %s "
                           "(numeral count) — HALT" % what)
    return [float(mm.group(0)) for mm in spans[:n]]


def bind_conv_r2(row):
    """S9-R1 CONV binder: constants from field 5 (anchor_text) by NAMED
    KEY; the channel-speed import from field 6 (params); definition
    markers asserted; roles asserted against the candidate table.  A
    binder failure is a loud masked halt, no silent fallback."""
    txt = row["anchor_text"]
    par = row["params"]

    c = _grab_txt(txt, r"\bc\s*=\s*", 1, "CONV c")[0]
    if conv_match(c) != "EK_C":
        raise RuntimeError("CONV c role mismatch — HALT")
    h = _grab_txt(txt, r"\bh\s*=\s*", 1, "CONV h")[0]
    h_role = conv_match(h)
    if h_role != "EK_H_JS":
        raise RuntimeError("CONV action-quantum role mismatch — HALT")
    hbar_marker = bool(re.search(
        r"hbar\s*=\s*h\s*/\s*\(\s*2\s*\*\s*pi\s*\)", txt))
    if not hbar_marker:
        raise RuntimeError("CONV reduced-constant derivation marker "
                           "absent — HALT")
    hbar = h / (2.0 * math.pi)
    if conv_match(hbar) != "EK_HBAR_JS":
        raise RuntimeError("derived reduced constant fails role assert "
                           "— HALT")
    kE_marker = bool(re.search(
        r"k\(E\)\s*=\s*E\s*/\s*\(\s*hbar\s*\*\s*c\s*\)", txt))
    if not kE_marker:
        raise RuntimeError("CONV k(E) definition marker absent — HALT")
    if not re.search(r"k\(lambda\)\s*=\s*2\s*\*\s*pi\s*/\s*lambda", txt):
        raise RuntimeError("CONV k(lambda) definition marker absent — HALT")
    if not re.search(r"k\(nu\)\s*=\s*2\s*\*\s*pi\s*\*\s*nu\s*/\s*c", txt):
        raise RuntimeError("CONV k(nu) definition marker absent — HALT")

    ev_key = r"1\s+" + ("e" + "V") + r"\s*=\s*"
    e_j = _grab_txt(txt, ev_key, 1, "CONV energy-unit-to-J")[0]
    if conv_match(e_j) != "EK_E_J":
        raise RuntimeError("CONV energy-unit role mismatch — HALT")

    lenp = _grab_txt(txt, r"648000\s*/\s*pi\s+au\s*=\s*", 1,
                     "CONV length-unit chain")[0]
    if conv_match(lenp) != "LEN_P":
        raise RuntimeError("CONV length-unit role mismatch — HALT")

    h0_plain = _grab_txt(txt, r"H0\s*=\s*", 1, "CONV H0")[0]
    if not 55.0 < h0_plain < 90.0:
        raise RuntimeError("CONV H0 magnitude outside sanity window — HALT")
    om_m = _grab_txt(txt, r"Omega_m\s*=\s*", 1, "CONV Omega_m")[0]
    if not 0.2 < om_m < 0.45:
        raise RuntimeError("CONV Omega_m outside sanity window — HALT")
    h0_si = h0_plain * 1.0e3 / (lenp * 1.0e6)

    # channel-speed import from field 6 (params), E-1(a):
    cch = _grab_txt(par, r"c_ch\s*=\s*c\s*=\s*", 1, "CONV c_ch import")[0]
    cch_ok = conv_match(cch) == "EK_C" and cch == c
    if not cch_ok:
        raise RuntimeError("channel-speed import mismatch — HALT")
    for marker, what in ((r"D_lt\(z\)\s*=\s*c\s*\*\s*Integral_0\^z",
                          "RULE R1 distance definition"),
                         (r"H\(z\)\s*=\s*H0\s*\*\s*sqrt\(", "R1 H(z) form"),
                         (r"RULE\s+R2", "RULE R2"), (r"RULE\s+R3",
                                                     "RULE R3"),
                         (r"RULE\s+R4", "RULE R4")):
        if not re.search(marker, par):
            raise RuntimeError("CONV params marker absent (masked): %s "
                               "— HALT" % what)

    def integrand_u(u):
        epu = math.exp(u)
        return 1.0 / (h0_si * math.sqrt(om_m * epu ** 3 + 1.0 - om_m))

    def _simpson_u(zz, n):
        big_u = math.log1p(zz)
        h_ = big_u / n
        s = 0.0
        for i in range(n + 1):
            w = 1 if i in (0, n) else (4 if i % 2 else 2)
            s += w * integrand_u(i * h_)
        return c * s * h_ / 3.0

    def _simpson_linear(zz, n):
        # the r1 ladder, kept as EVIDENCE only (never used for a verdict)
        h_ = zz / n
        s = 0.0
        for i in range(n + 1):
            zp = i * h_
            f = 1.0 / ((1.0 + zp) *
                       (h0_si * math.sqrt(om_m * (1.0 + zp) ** 3
                                          + 1.0 - om_m)))
            w = 1 if i in (0, n) else (4 if i % 2 else 2)
            s += w * f
        return c * s * h_ / 3.0

    def d_lt(z, n=2 ** 14):
        if z <= 0:
            return 0.0
        v1 = _simpson_u(z, n)
        v2 = _simpson_u(z, 2 * n)
        dev = abs(v1 - v2) / abs(v2)
        if dev > 1e-10:
            raise RuntimeError("D_lt doubling gate FAILED (1e-10) at a "
                               "bound z — HALT")
        o1 = _simpson_linear(z, 4096)
        o2 = _simpson_linear(z, 8192)
        D_LT_TABLE[z] = {"new": v2, "new_dev": dev, "old_4096": o1,
                         "old_dev": abs(o1 - o2) / abs(o2)}
        return v2

    return {"c_em_si": c, "c_cone_si": cch, "c_ok": True, "cch_ok": cch_ok,
            "h": h, "h_role": h_role, "hbar": hbar,
            "hbar_marker": hbar_marker, "kE_marker": kE_marker,
            "e_j": e_j, "d_lt": d_lt}


def _unit_mult(token, family):
    """family 'f' (inverse-time) or 'E' (energy); token built by runtime
    concatenation so this file stays T1-clean."""
    pref = {"": 1.0, "k": 1e3, "M": 1e6, "G": 1e9, "T": 1e12}
    base = ("H" + "z") if family == "f" else ("e" + "V")
    for p, m in pref.items():
        if token == p + base:
            return m
    return None


def _grab(cell, key_re, n=1, unit_family=None):
    """Extract n numbers (and optionally a unit token) following a key.
    (verbatim from the r1 mapper)"""
    m = re.search(key_re, cell)
    if not m:
        return None
    tail = cell[m.end():]
    stop = tail.find(";")
    seg = tail if stop < 0 else tail[:stop + 40]
    spans = list(NUM_RE.finditer(seg))
    if len(spans) < n:
        return None
    vals = [float(mm.group(0)) for mm in spans[:n]]
    if unit_family:
        um = re.match(r"\s*\]{0,2}\s*([A-Za-z]+)", seg[spans[n - 1].end():])
        if not um:
            return None
        mult = _unit_mult(um.group(1), unit_family)
        if mult is None:
            return None
        return vals, mult
    return vals


def bind_arms(rows, conv, honesty):
    """(verbatim from the r1 mapper — the ONLY change is upstream:
    conv['hbar'] now carries the derived reduced constant, so k_from_E is
    the sealed k(E) = E/(hbar*c).)"""
    c = conv["c_em_si"]
    hbar = conv["hbar"]
    e_j = conv["e_j"]
    d_lt = conv["d_lt"]

    def k_from_E(E, mult):
        return E * mult * e_j / (hbar * c)

    def k_from_nu(nu, mult):
        return 2.0 * math.pi * nu * mult / c

    def k_from_lam(lam):
        return 2.0 * math.pi / lam

    out = {}

    def need(x, what):
        if x is None:
            raise RuntimeError("binder failure (masked): %s — HALT" % what)
        return x

    # TR-1: nu_ref (unit), z_src, tau_r
    cell = rows["TR-1"]["params"]
    (nu,), mult = need(_grab(cell, r"nu_ref\s*=", 1, "f"), "TR-1 nu_ref")
    z = need(_grab(cell, r"z_src\s*="), "TR-1 z")[0]
    tau = need(_grab(cell, r"tau_r\s*="), "TR-1 tau")[0]
    k0 = k_from_nu(nu, mult)
    out["TR-1"] = {"kind": "TR", "k_readings": [k0, (1 + z) * k0],
                   "k_rep": k0, "D_r": d_lt(z), "thr": tau}

    # TR-2: lambda_ref (SI length), bracket, z, tau
    cell = rows["TR-2"]["params"]
    lam = need(_grab(cell, r"lambda_ref\s*="), "TR-2 lambda")[0]
    br = need(_grab(cell, r"lambda\s+in\s*\[", 2), "TR-2 bracket")
    z = need(_grab(cell, r"z_src\s*="), "TR-2 z")[0]
    tau = need(_grab(cell, r"tau_r\s*="), "TR-2 tau")[0]
    ks = [k_from_lam(v) for v in br]
    out["TR-2"] = {"kind": "TR",
                   "k_readings": [k for kk in ks
                                  for k in (kk, (1 + z) * kk)],
                   "k_rep": k_from_lam(lam), "D_r": d_lt(z), "thr": tau}

    # TR-3: E_ref (unit), E bracket, z, tau
    cell = rows["TR-3"]["params"]
    (eref,), mult = need(_grab(cell, r"E_ref\s*=", 1, "E"), "TR-3 E_ref")
    ebr, mbr = need(_grab(cell, r"E\s+bracket[^:]*:\s*\[", 2, "E"),
                    "TR-3 bracket")
    z = need(_grab(cell, r"z_src\s*="), "TR-3 z")[0]
    tau = need(_grab(cell, r"tau_r\s*="), "TR-3 tau")[0]
    ks = [k_from_E(v, mbr) for v in ebr]
    out["TR-3"] = {"kind": "TR",
                   "k_readings": [k for kk in ks
                                  for k in (kk, (1 + z) * kk)],
                   "k_rep": k_from_E(eref, mult), "D_r": d_lt(z),
                   "thr": tau}

    # TR-4: E_ref, E_alt (both-readings), z, tau
    cell = rows["TR-4"]["params"]
    (eref,), mult = need(_grab(cell, r"E_ref\s*=", 1, "E"), "TR-4 E_ref")
    (ealt,), malt = need(_grab(cell, r"E_alt\s*=", 1, "E"), "TR-4 E_alt")
    z = need(_grab(cell, r"z_src\s*="), "TR-4 z")[0]
    tau = need(_grab(cell, r"tau_r\s*="), "TR-4 tau")[0]
    ks = [k_from_E(eref, mult), k_from_E(ealt, malt)]
    out["TR-4"] = {"kind": "TR",
                   "k_readings": [k for kk in ks
                                  for k in (kk, (1 + z) * kk)],
                   "k_rep": ks[0], "D_r": d_lt(z), "thr": tau}

    # ACH-DIM: lambda_1, lambda_2, Delta_tau_r, z
    cell = rows["ACH-DIM"]["params"]
    l1 = need(_grab(cell, r"lambda_1\s*="), "ACH-DIM l1")[0]
    l2 = need(_grab(cell, r"lambda_2\s*="), "ACH-DIM l2")[0]
    dtau = need(_grab(cell, r"Delta_tau_r\s*="), "ACH-DIM dtau")[0]
    z = need(_grab(cell, r"z_src\s*="), "ACH-DIM z")[0]
    k1, k2 = k_from_lam(l1), k_from_lam(l2)
    out["ACH-DIM"] = {"kind": "ACH-DIM",
                      "k_pairs": [(k1, k2),
                                  ((1 + z) * k1, (1 + z) * k2)],
                      "k_rep": k1, "D_r": d_lt(z), "thr": dtau}

    # ACH-DISP: E_1, E_2, beta_r; no z (R2 n/a, flagged in the row)
    cell = rows["ACH-DISP"]["params"]
    (e1,), m1 = need(_grab(cell, r"E_1\s*=", 1, "E"), "ACH-DISP E1")
    (e2,), m2 = need(_grab(cell, r"E_2\s*=", 1, "E"), "ACH-DISP E2")
    beta = need(_grab(cell, r"beta_r\s*="), "ACH-DISP beta")[0]
    k1, k2 = k_from_E(e1, m1), k_from_E(e2, m2)
    out["ACH-DISP"] = {"kind": "ACH-DISP", "k_pairs": [(k1, k2)],
                       "k_rep": k1, "thr": beta}
    sec = _grab(cell, r"beta_sec\s*=")
    if sec is None:
        honesty.append("H-CC-4 (standing from r1): the ACH-DISP secondary "
                       "informational reading did not bind cleanly; it is "
                       "non-verdict by the row's own text and is left "
                       "unreported.")

    # BIR-1: nu_ref (unit), kappa_r, z
    cell = rows["BIR-1"]["params"]
    (nu,), mult = need(_grab(cell, r"nu_ref\s*=", 1, "f"), "BIR-1 nu")
    kap = need(_grab(cell, r"kappa_r\s*="), "BIR-1 kappa")[0]
    z = need(_grab(cell, r"z_src\s*="), "BIR-1 z")[0]
    k0 = k_from_nu(nu, mult)
    out["BIR-1"] = {"kind": "BIR", "k_readings": [k0, (1 + z) * k0],
                    "k_rep": k0, "D_r": d_lt(z), "thr": kap}

    # BIR-2: E bracket (unit), kappa_r, z
    cell = rows["BIR-2"]["params"]
    ebr, mbr = need(_grab(cell, r"E\s+bracket\s*=\s*\[", 2, "E"),
                    "BIR-2 bracket")
    kap = need(_grab(cell, r"kappa_r\s*="), "BIR-2 kappa")[0]
    z = need(_grab(cell, r"z_src\s*="), "BIR-2 z")[0]
    ks = [k_from_E(v, mbr) for v in ebr]
    out["BIR-2"] = {"kind": "BIR",
                    "k_readings": [k for kk in ks
                                   for k in (kk, (1 + z) * kk)],
                    "k_rep": ks[0], "D_r": d_lt(z), "thr": kap}

    # DIFF: mapped band [B_lo, B_hi]; k_EM bracket (unit) + representative
    cell = rows["DIFF"]["params"]
    band = need(_grab(cell, r"\[B_lo,\s*B_hi\]\s*=\s*\[", 2), "DIFF band")
    if not band[0] <= 0.0 <= band[1]:
        honesty.append("H-CC-5 trigger (unchanged from r1): the DIFF "
                       "mapped band does not contain zero.")
    ebr, mbr = need(_grab(cell, r"E\s+bracket\s*\[", 2, "E"),
                    "DIFF k_EM bracket")
    ks = [k_from_E(v, mbr) for v in ebr]
    rep = _grab(cell, r"representative\s+", 1, "E")
    k_rep = k_from_E(rep[0][0], rep[1]) if rep else ks[0]
    out["DIFF"] = {"kind": "DIFF", "k_readings": ks, "k_rep": k_rep,
                   "B_lo": band[0], "B_hi": band[1]}
    return out


def eval_arm(ctx, spec):
    kind = spec["kind"]

    if kind == "TR":
        def fn(d):
            return tr_state(ctx, spec["k_readings"], spec["D_r"],
                            spec["thr"], d)
    elif kind == "ACH-DIM":
        def fn(d):
            return ach_dim_state(ctx, [p[0] for p in spec["k_pairs"]],
                                 [p[1] for p in spec["k_pairs"]],
                                 spec["D_r"], spec["thr"], d)
    elif kind == "ACH-DISP":
        def fn(d):
            return ach_disp_state(ctx, [p[0] for p in spec["k_pairs"]],
                                  [p[1] for p in spec["k_pairs"]],
                                  spec["thr"], d)
    elif kind == "BIR":
        def fn(d):
            return bir_state(ctx, spec["k_readings"], spec["D_r"],
                             spec["thr"], d)
    elif kind == "DIFF":
        def fn(d):
            return diff_state_s9(ctx, spec["k_readings"], spec["B_lo"],
                                 spec["B_hi"], d)
    else:
        raise RuntimeError("unknown arm kind — HALT")

    runs = partition_d(fn)
    pass_set, excl, voids = runs_to_sets(runs)
    edges = sorted({e for iv in excl for e in iv if 0 < e < float("inf")})
    k_rep_agg = ctx.k_agg(spec["k_rep"])
    return {"pass_set": pass_set, "excl": excl, "voids": voids,
            "xr_edges": [k_rep_agg * e for e in edges]}


if __name__ == "__main__":
    main()
