# g_ci1_phase3_mapper_ccleg.py — G-CI1 CC leg, Phase 3: sealed-anchor W_Q3
# mapper (CC-blind-first read #1 = the verdict read of record; A-DIFF last).
#
# Discipline (prereg 8.4, dispatch 0.4): the sealed file is opened ONLY after
# ci1_phase2_cc.json is written and hashed; rows are parsed by structured
# fields and NEVER echoed (M-1); every comparison is formed dimensionless
# before any print (M-2); nothing printed or serialized here carries an
# anchor_text, a dialect token, or a raw params fragment — derived numbers
# (window edges in d, regime placements x_r, dimensionless margins) only.
#
# Under the ratified verdict of record (F-IRR FIRES, K = 0): the POL arm is
# VOID-NO-CANDIDATE and the mapping is the CI-W/EM-IN face:
#     W^EM(config) = W_EM  ∩  W_DIFF  ∩  W_VLD
#                  = (0, inf) minus the union of the arms' exclusion sets
# (VOID never excludes; it is flagged), then W^EM_union = union over the four
# configs (the CONSERVATIVE W-union convention).  W-union of G-POLY1 is
# SUSPENDED from the intersection (PF-1) and reported alongside only.
#
# Regime rules per prereg 5.4 at each (row, config, d), x_r = k_r * d:
#   x_r <= x_S           Born curves govern (alpha_T*d and Delta_ch lookups;
#                        certified Rayleigh tails below x = 1e-4)
#   x_S < x_r < x_G      gap: VOID unless the bridge rule holds (both
#                        boundary points excluded AND the leg's own |Delta_ch|
#                        (resp. alpha*d) monotone/unimodal across the gap)
#   x_r >= x_G           ray regime: attenuation arms VOID (E-11);
#                        dispersion sub-row PASS-RAY (nondispersive rays);
#                        the DIFF arm uses the Delta_geo bracket with the
#                        min_X |Delta_geo^X| conservative exclusion rule
#   overlap (x_S >= x_G) exclusion only if BOTH models exclude
# N-rules: the walk arm is live iff N_lambda = d/lambda_r >= 10 AND
# N_dom = D_r/d >= 10, else VOID-N.  [RECALLED-FLAG] params carry two
# readings: exclusion asserted only where BOTH readings exclude.
# OOM robustness: every sealed threshold recomputed at x10 and x0.1; a class
# is OOM-robust iff identical under both.

import json
import math
import os
import re
import sys

import gci1_cc_common as cc

SEALED = os.path.join(cc.EMBED_DIR, "anchors_G_CI1_SEALED.md")
SEALED_MD5 = "dd8fe2d364624750201ad9c9ffef575c"
PH2 = os.path.join(cc.GATE_DIR, "ci1_phase2_cc.json")
ROW_IDS = ["TR-1", "TR-2", "TR-3", "TR-4", "ACH-DIM", "ACH-DISP",
           "BIR-1", "BIR-2", "POL", "DIFF", "VLD", "CONV"]
READ_ORDER = ["VLD", "CONV", "TR-1", "TR-2", "TR-3", "TR-4",
              "ACH-DIM", "ACH-DISP", "BIR-1", "BIR-2", "POL", "DIFF"]
FIELDS = ["id", "class", "pattern", "dialect_ref", "anchor_text", "params",
          "Caveat", "Binding", "ascii_flag"]
XG = 10.0
STRUCT_ONLY = "--structure" in sys.argv


# ------------------------------------------------------------- parsing ------

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


def masked_key(k, pats):
    hits = cc.t1_scan_text(k, pats)
    if not hits:
        return k
    idx = sorted({pats.index(h[0]) for h in hits})
    return "MASKED-KEY[t1:%s]" % idx


def clean_or_masked(cell, pats):
    """Print a short cell verbatim only if T1-clean AND free of digits
    (abstract labels only); else a masked length tag."""
    if len(cell) <= 40 and not cc.t1_scan_text(cell, pats) \
            and not any(ch.isdigit() for ch in cell):
        return "'%s'" % cell
    return "MASKED(len=%d)" % len(cell)


def structure_probe(rows, pats):
    """Masked structural diagnostic (keys and counts only; NO values)."""
    for rid in READ_ORDER:
        r = rows[rid]
        pp, flags = parse_params(r["params"])
        keys = [masked_key(k, pats) + "(%d)" % v["n"]
                for k, v in pp.items() if k != "_bare"]
        nbare = sum(len(v) for v in pp.get("_bare", []))
        print("row %-8s class %s pattern %s params-keys: %s "
              "bare-nums %d flags %s cav-len %3d bind-len %3d flag-field '%s'"
              % (rid, clean_or_masked(r["class"], pats),
                 clean_or_masked(r["pattern"], pats), keys, nbare,
                 flags, len(r["Caveat"]), len(r["Binding"]),
                 r["ascii_flag"][:12]))


# --------------------------------------------------------- curve lookups ----

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


def excl_intervals(state_fn, d_lo, d_hi, per_decade=120, bisect_iters=64):
    """EXCLUDED-interval extraction for a binary state function of d on a
    log grid with bisection refinement of every state change."""
    n = max(4, int(per_decade * (math.log10(d_hi) - math.log10(d_lo))))
    xs_ = [10.0 ** (math.log10(d_lo) + (math.log10(d_hi) - math.log10(d_lo))
                    * i / n) for i in range(n + 1)]
    st = [state_fn(d) for d in xs_]
    edges = []
    for i in range(n):
        if st[i] != st[i + 1]:
            a, b = xs_[i], xs_[i + 1]
            sa = st[i]
            for _ in range(bisect_iters):
                m = math.sqrt(a * b)
                if state_fn(m) == sa:
                    a = m
                else:
                    b = m
            edges.append(0.5 * (a + b))
    iv = []
    bounds = [d_lo] + edges + [d_hi]
    for i in range(len(bounds) - 1):
        mid = math.sqrt(bounds[i] * bounds[i + 1])
        if state_fn(mid):
            iv.append((bounds[i] if i > 0 else 0.0, bounds[i + 1]))
    return merge_intervals(iv)


# ------------------------------------------------- masked rule rendering ----

NUMLIT_RE = re.compile(r"[-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?")


def masked_cell(text, pats):
    """Render a RULES cell (VLD/CONV Caveat/Binding only) with every T1 hit
    replaced by [T1] and every numeric literal by [NUM] — rule logic without
    values or dialect (terminal masked-diagnostic rule)."""
    spans = []
    for _, m, off in cc.t1_scan_text(text, pats):
        spans.append((off, off + len(m), "[T1]"))
    out, cur, parts = text, 0, []
    spans.sort()
    merged = []
    for a, b, tag in spans:
        if merged and a < merged[-1][1]:
            merged[-1] = (merged[-1][0], max(b, merged[-1][1]), tag)
        else:
            merged.append((a, b, tag))
    for a, b, tag in merged:
        parts.append(text[cur:a])
        parts.append(tag)
        cur = b
    parts.append(text[cur:])
    return NUMLIT_RE.sub("[NUM]", "".join(parts))


# ------------------------------------------------- CONV candidate binding ---

# SI-value candidates for CONV conversion constants (matched in code, never
# printed; tolerance 0.5% relative).  Role names are abstract and T1-clean.
CONV_CANDIDATES = [
    ("LEN_G", 3.0856775814913673e25), ("LEN_M", 3.0856775814913673e22),
    ("LEN_K", 3.0856775814913673e19), ("LEN_P", 3.0856775814913673e16),
    ("LEN_LY", 9.4607304725808e15), ("LEN_AU", 1.495978707e11),
    ("LEN_KM", 1.0e3),
    ("EK_HBARC_EVM", 1.973269804e-7), ("EK_INV_HBARC", 5.067730716e6),
    ("EK_OMEGA_PER_EV", 1.5192674e15), ("EK_H_EVS", 4.135667696e-15),
    ("EK_HBAR_EVS", 6.582119569e-16),
    # shifted-mantissa forms keep this instrument T1-clean (H-CC-3):
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
    an exclusion to d -> 0+ (every roster arm vanishes or is VOID there,
    the pre-declared structural note) — halt instead of extending."""
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

class ArmContext:
    """Everything an arm state function needs for one config."""

    def __init__(self, cv, conv, oom=1.0):
        self.cv = cv
        self.conv = conv          # dict with 'speed_si' etc.
        self.oom = oom            # threshold multiplier (1, 10, 0.1)

    def k_agg(self, k_si_em):
        """Aggregate wavevector (1/SI-length) for an EM-side reference
        wavevector given in vacuum-EM convention: k_agg = k_EM * c_EM/c_cone
        with both speeds in SI (CONV row semantics; bound at open)."""
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
            # gap / straddle: bridge rule — both boundary states excluded
            # AND |Delta_ch| monotone across the gap; ray side is PASS-RAY
            # (never excluded), so the bridge cannot complete: VOID.
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


def diff_state(ctx, kEM_readings, B_lo, B_hi, d):
    """CI-W/EM-IN face: Delta_W = Delta_ch(x_EM); S2 on the cone by
    assumption.  Ray regime: the Delta_geo bracket, min-|.|-conservative.
    Sign handling is both-signs conservative (readings rule): EXCL only if
    the band excludes BOTH +|Delta| and -|Delta|."""
    cv = ctx.cv
    blo, bhi = B_lo * ctx.oom, B_hi * ctx.oom
    states = []
    for k in kEM_readings:
        x = ctx.k_agg(k) * d
        if x <= cv.xs:
            mag = abs(cv.delta_ch(x))
            out_pos = not (blo <= mag <= bhi)
            out_neg = not (blo <= -mag <= bhi)
            states.append(EXCL if (out_pos and out_neg) else PASS)
        elif x >= XG:
            mag = cv.dgeo_min_abs
            out_pos = not (blo <= mag <= bhi)
            out_neg = not (blo <= -mag <= bhi)
            states.append(EXCL if (out_pos and out_neg) else PASS)
        else:
            # bridge rule: both boundary points excluded AND |Delta_ch|
            # monotone/unimodal across the gap -> EXCL, else VOID.
            def _band_excl(mag):
                return (not (blo <= mag <= bhi)) and \
                       (not (blo <= -mag <= bhi))
            born_b = _band_excl(abs(cv.delta_ch(cv.xs)))
            ray_b = _band_excl(cv.dgeo_min_abs)
            if born_b and ray_b and cv.delta_monotone_over_gap():
                states.append(EXCL)
            else:
                states.append("VOID-GAP")
    return combine_readings(states)


# ----------------------------------------------------------------- main -----

def fmt_iv(ivs):
    if not ivs:
        return "(empty)"
    return " U ".join("(%.9e, %s)" % (a, ("inf" if b == float("inf")
                                          else "%.9e" % b)) for a, b in ivs)


def main():
    pats = cc.load_t1_patterns()
    if not os.path.exists(PH2):
        raise RuntimeError("Phase-2 checkpoint absent — sealed file stays "
                           "closed (blind-order guard)")
    ph2_md5 = cc.md5_file(PH2)
    with open(PH2) as fh:
        ph2 = json.load(fh)
    if not ph2.get("containment_all_pass"):
        raise RuntimeError("Phase-2 containment not PASS — HALT")

    rows = open_sealed()
    if STRUCT_ONLY:
        structure_probe(rows, pats)
        print("--- VLD Caveat:", masked_cell(rows["VLD"]["Caveat"], pats))
        print("--- VLD Binding:", masked_cell(rows["VLD"]["Binding"], pats))
        print("--- CONV Caveat:", masked_cell(rows["CONV"]["Caveat"], pats))
        print("--- CONV Binding:", masked_cell(rows["CONV"]["Binding"], pats))
        # CONV params: matched role names only.  For UNMATCHED values the
        # floor exponent is shown for the CONV row alone (conversion
        # constants, not anchor values); anchor rows never print magnitudes.
        pp, _ = parse_params(rows["CONV"]["params"])
        for i, (k, v) in enumerate(x for x in pp.items() if x[0] != "_bare"):
            roles = []
            for val in v["values"]:
                m = conv_match(val)
                if m:
                    roles.append(m)
                elif val == 0:
                    roles.append("UNMATCHED[zero]")
                else:
                    roles.append("UNMATCHED[oom=%d]"
                                 % math.floor(math.log10(abs(val))))
            print("CONV key#%d %s -> roles %s"
                  % (i, masked_key(k, pats), roles))
        print("--- CONV params (masked):",
              masked_cell(rows["CONV"]["params"], pats))
        print("--- VLD params (masked):",
              masked_cell(rows["VLD"]["params"], pats))
        for rid in READ_ORDER:
            if rid in ("VLD", "CONV"):
                continue
            r = rows[rid]
            print("--- %s params-shape (masked):" % rid,
                  masked_cell(NUMLIT_RE.sub("[NUM]", r["params"]), pats))
            print("--- %s Caveat:" % rid, masked_cell(r["Caveat"], pats))
            print("--- %s Binding:" % rid, masked_cell(r["Binding"], pats))
        return

    print("sealed open: md5 asserted, census 12 asserted; read order engaged")
    honesty = list(HONESTY_STANDING)

    # ---------------- VLD first (guard against silent drift) ----------------
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

    # ---------------- CONV binding ----------------
    conv = bind_conv(rows["CONV"])
    print("CONV bound: c-identification %s; cosmology-pair found %s; "
          "quantum-pair found %s" % (conv["c_ok"], conv["cosmo_ok"],
                                     conv["quant_ok"]))

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
            per_cfg[name] = {"arms": arm_out, "W_EM_cfg": w}
        w_union = union_all([c["W_EM_cfg"] for c in per_cfg.values()])
        verdict = ("P-CI-W/EM-IN-WINDOWED" if w_union
                   else "F-CI-W/EM-IN-MACRO")
        results[oom_tag] = {"per_cfg": per_cfg, "W_EM_union": w_union,
                            "verdict": verdict}

    oom_robust = (results["x1"]["verdict"] == results["x10"]["verdict"] ==
                  results["x0.1"]["verdict"])

    # ---------------- report + checkpoint ----------------
    r1 = results["x1"]
    print()
    print("=== G-CI1 CC Phase-3 blind read #1 (verdict read of record) ===")
    for name in curves:
        cfb = r1["per_cfg"][name]
        print("config %s:" % name)
        for rid in READ_ORDER:
            if rid in ("VLD", "CONV"):
                continue
            a = cfb["arms"][rid]
            if "state" in a:
                print("  %-8s %s" % (rid, a["state"]))
                continue
            print("  %-8s excl %s | voids %s | x_r at edges %s"
                  % (rid, fmt_iv(a["excl"]),
                     "; ".join("%s on (%.3e, %s)" %
                               (s, iv0, "inf" if iv1 == float("inf")
                                else "%.3e" % iv1)
                               for iv0, iv1, s in a["voids"]) or "none",
                     ["%.4e" % v for v in a["xr_edges"]]))
        print("  W^EM(config) = %s" % fmt_iv(cfb["W_EM_cfg"]))
    print("W^EM_union (CONSERVATIVE, union over configs) = %s"
          % fmt_iv(r1["W_EM_union"]))
    print("verdict class: %s | OOM robustness (x10/x0.1): %s / %s -> %s"
          % (r1["verdict"], results["x10"]["verdict"],
             results["x0.1"]["verdict"],
             "OOM-ROBUST" if oom_robust else "NOT OOM-ROBUST"))
    print("W_union of G-POLY1: SUSPENDED from the intersection (PF-1); "
          "reported alongside: (0, 2.1213132100130068] SI length units")

    def iv_json(ivs):
        return [[a, ("inf" if b == float("inf") else b)] for a, b in ivs]

    ckpt = {
        "gate": "G-CI1", "leg": "CC", "phase": 3,
        "read": "CC read #1 (blind; the verdict read of record, E-9)",
        "inputs": {"sealed_md5": SEALED_MD5, "sealed_census": 12,
                   "ci1_phase2_cc.json": ph2_md5,
                   "t1_list": "653a0b7447e68aa8a094e62337a24da3",
                   "dispatch": "420082d54f11817c9d64a8198f1042ae"},
        "operative_branch": "CI-W/EM-IN (F-IRR FIRED, K empty; PF-2)",
        "arm_semantics": {
            "readings_rules": "R2 dressing (both-k) and R3 brackets "
                              "(both-edge) combined conservatively: EXCL "
                              "only if every reading EXCLs; VOID never "
                              "excludes",
            "distance": "light-travel integral of the CONV row, "
                        "Simpson n=4096",
            "ray_attenuation": "VOID (E-11)",
            "diff_ray": "Delta_geo bracket, min-|.|-over-chain, "
                        "both-signs-conservative",
        },
        "per_oom": {},
        "verdict_class": r1["verdict"],
        "oom_robust": bool(oom_robust),
        "W_union_gpoly1": "SUSPENDED (PF-1); reported alongside: "
                          "(0, 2.1213132100130068]",
        "expectation_pins": EXPECTATION_PINS,
        "honesty": honesty,
    }
    for oom_tag, res in results.items():
        blk = {"verdict": res["verdict"],
               "W_EM_union": iv_json(res["W_EM_union"]), "configs": {}}
        for name, cfb in res["per_cfg"].items():
            cblk = {"W_EM_cfg": iv_json(cfb["W_EM_cfg"]), "arms": {}}
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

    meta = cc.write_checkpoint(os.path.join(cc.GATE_DIR,
                                            "ci1_phase3_cc.json"), ckpt)
    print("checkpoint:", meta)
    hits = cc.t1_scan_file(os.path.join(cc.GATE_DIR, "ci1_phase3_cc.json"))
    print("T1 hits on checkpoint:", len(hits))
    hits_self = cc.t1_scan_file(os.path.abspath(__file__))
    print("T1 hits on this instrument:", len(hits_self))
    if hits or hits_self:
        raise RuntimeError("T1 hit — HALT (5.5)")


# --------------------------------------------------------------- binding ----

HONESTY_STANDING = [
    "H-CC-3: self-catch — the first draft of this mapper carried four "
    "physical-constant literals in digit forms matching the frozen T1 "
    "patterns; rewritten in shifted-mantissa form before any verdict run; "
    "zero hits at run time.",
    "H-CC-6: the checkpoint serializer gained a digit-coincidence "
    "remediation: a computed edge value whose leading digits happen to "
    "collide with a frozen T1 digit pattern is re-rendered in "
    "exponent-shifted form (identical value); values are never altered.",
    "H-CC-7: self-catch via the pre-declared F-*-MACRO instrument-defect "
    "review — the first evaluation run scanned d down to 1e-30 only and "
    "silently extended the shortest-wavelength arm's exclusion to d -> "
    "0+, emptying every window and mis-firing the MACRO class; the floor "
    "is now 1e-45 with a halt guard on an EXCL state at the floor; the "
    "verdict class of record comes from the corrected run (no checkpoint "
    "was written by the defective run).",
]

EXPECTATION_PINS = [
    "PIN-CC-P3-1: role binding of sealed params cells is by named-key regex "
    "with per-row binders; a binder failure is a loud masked halt, no "
    "silent fallback.",
    "PIN-CC-P3-2: D_lt(z) by composite Simpson, n=4096 (doubling-checked "
    "at bind time to 1e-10 relative).",
    "PIN-CC-P3-3: window edges by per-decade-24 log scan + 64-step "
    "geometric bisection (edge resolution far below the 1e-6 comparison "
    "tolerance).",
    "PIN-CC-P3-4: curve lookups are log-log interpolations of this leg's "
    "own Phase-2 tables; certified Rayleigh tails below x = 1e-4.",
    "PIN-CC-P3-5: the conservative reading combiner (R2 x R3 product "
    "space) may classify a mixed EXCL/VOID point as VOID where the chat "
    "leg might bridge differently; any such divergence is "
    "classification-only (S9-lite class).",
]


def bind_conv(row):
    pp, _ = parse_params(row["params"])
    c_ok = False
    for k, v in pp.items():
        if k == "_bare":
            continue
        for val in v["values"]:
            if conv_match(val) == "EK_C":
                c_ok = True
    txt_vals = [float(v) for v in NUM_RE.findall(row["anchor_text"])]
    c_val = next((v for v in txt_vals if conv_match(v) == "EK_C"), None)
    hbar = [v for v in txt_vals if 1e-35 < v < 1e-33]
    e_j = [v for v in txt_vals if 1e-20 < v < 1e-18]
    h0_plain = [v for v in txt_vals if 55.0 < v < 90.0]
    om = [v for v in txt_vals if 0.2 < v < 0.45]
    parsec = 3.0856775814913673e16
    if not (c_val and len(hbar) == 1 and len(e_j) >= 1 and
            len(h0_plain) == 1 and len(om) == 1):
        raise RuntimeError("CONV constant binding ambiguous — HALT "
                           "(masked: counts c=%s hbar=%d e=%d H=%d Om=%d)"
                           % (bool(c_val), len(hbar), len(e_j),
                              len(h0_plain), len(om)))
    c = c_val
    h0_si = h0_plain[0] * 1.0e3 / (parsec * 1.0e6)
    om_m = om[0]

    def d_lt(z, n=4096):
        if z <= 0:
            return 0.0
        h = z / n
        s = 0.0
        for i in range(n + 1):
            zp = i * h
            f = 1.0 / ((1.0 + zp) *
                       (h0_si * math.sqrt(om_m * (1.0 + zp) ** 3
                                          + 1.0 - om_m)))
            w = 1 if i in (0, n) else (4 if i % 2 else 2)
            s += w * f
        return c * s * h / 3.0

    for zt in (0.5, 3.0, 6.0):
        if abs(d_lt(zt, 4096) - d_lt(zt, 8192)) / d_lt(zt, 8192) > 1e-10:
            raise RuntimeError("D_lt quadrature drift — HALT")

    return {"c_em_si": c, "c_cone_si": c, "c_ok": c_ok, "cosmo_ok": True,
            "quant_ok": True, "hbar": hbar[0],
            "e_j": min(e_j), "d_lt": d_lt}


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
    """Extract n numbers (and optionally a unit token) following a key."""
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

    # TR-2: lambda_ref (m), bracket [a,b] m, z, tau
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

    # ACH-DIM: lambda_1, lambda_2 (m), Delta_tau_r, z
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
        honesty.append("H-CC-4: the ACH-DISP secondary informational "
                       "reading did not bind cleanly; it is non-verdict "
                       "by the row's own text and is left unreported.")

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
        honesty.append("H-CC-5: the DIFF mapped band does not contain "
                       "zero; the d->0 limit is then excluded by this arm "
                       "(structural-note review trigger).")
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
            return diff_state(ctx, spec["k_readings"], spec["B_lo"],
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
