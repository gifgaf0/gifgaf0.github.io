# G-2a-L1 — S9 RESOLUTION MINI-DISPATCH (IN-BAND, P-4)
## Run-2 under checkpoint schema v1.1 — representation only; nothing recomputed; arms untouched

**Date:** August 27, 2026. **Trigger:** comparator v1.0 (md5 67ee429a) fired S9 on four misses in the CC return (checkpoint 47ae0b85, commit 75e185e). All 51 numeric/boolean items and all three lattices agree; the three arms agree at base. **All four misses are chat-side schema/comparator defects, owned below.** Per prereg §8 the arms were not re-tuned by either leg; this mini-dispatch fixes the instrument of comparison, frozen BEFORE either leg re-emits, and asks both legs to re-emit their checkpoints from values already computed.

## Root causes (chat-side honesty ledger)
- **H-S4** `Mplus_element_orders` — schema v1.0 wrote "(sorted list)"; the chat instrument asserts the SET {1,2,3,4} (line 237); CC emitted the per-class multiset. Same fact, two encodings. **v1.1: the set.**
- **H-S5** `arm_sharpened` — schema v1.0 declared it free text; comparator v1.0 compared it exactly. **v1.1: reported, never compared.**
- **H-S6** `GL23_transposition_class_size` — level unspecified; chat counts in PGL (6; instrument line 449), CC in GL (12). Both facts true and now both verified chat-side (add-on embedded: the 12 GL-preimages are all involutions). **v1.1: the field is retired; two fields `_PGL` = 6 and `_GL` = 12, each compared exactly.**
- **H-S7** `C5_B2.arm` — the dispatch permitted an optional suffix ("ASSEMBLED-RELOCATED"); comparator v1.0 compared exact strings, producing the DIVERGENT flag alone. **v1.1: base arm = the longest registered arm name the string starts with; suffix reported.** (Registered names with hyphens — 2O-INDUCED, OTHER-COVER, STRUCTURE-DEPENDENT, PIN-SPLIT, CONSTRAINS-I/II — are matched whole, not split.)
- **H-S8** (add-on self-catch) the add-on's first assertion expected 6 involutions among the 12 GL-preimages; the exhaustive computation gives 12 (both lifts m, −m of an involution are involutions). Assertion corrected; no result affected.

Comparator v1.1 retains every numeric/boolean exact-identity check of v1.0 (verified: it still fires on an arm flip, a single lattice entry, and a group-order change). Chat re-emission `g_2a_L1_chat_checkpoint_v1_1.json` carries a `reemission` block naming its v1.0 parent (476052b1) and the three representational changes; the chat instrument (2f0fa8f4) is untouched.

## Embed manifest
| Embed | md5 | bytes |
|---|---|---|
| `activation_S9_G_2a_L1.json` | 8dbe00b2ad3cb76024d0de9bff5ce5da | 879 |
| `g_2a_L1_compare_v1_1.py` | faa233c06c818b6168894c579ac35876 | 4989 |
| `g_2a_L1_chat_checkpoint_v1_1.json` | 8abda98d723c4ac7e23ff144ba780a11 | 2820 |
| `gl23_class_level_addon.py` | 9cc8d31488a54a0d3ea5fcd7c9f34383 | 2176 |
| `gl23_class_level_addon.log` | 6a231d9686ccc24b4db110b81c4f7c68 | 319 |
| `extract_embeds_G_2a_L1.py` | 63942160beed37c28aed4234c185c4a0 | 1464 |

## CC leg — do exactly this
1. Extract and verify (`python3 extract_embeds_G_2a_L1.py <this file> .` → six `OK` lines).
2. **Re-emit** `g_2a_L1_cc_checkpoint_v1_1.json` from your existing phase JSONs / instrument values — **no recomputation, instrument c3bea9ee untouched**: `schema` = `g2a_l1_checkpoint_v1_1`; `Mplus_element_orders` = the set; drop `GL23_transposition_class_size`, add `GL23_transposition_class_size_PGL` (6) and `GL23_transposition_class_size_GL` (12) from your own already-verified facts; `arm` strings unchanged; add a `reemission` block naming the v1.0 parent md5 and listing the changes. T1-scan it (zero hits). Hash and commit.
3. Run `python3 g_2a_L1_compare_v1_1.py g_2a_L1_chat_checkpoint_v1_1.json g_2a_L1_cc_checkpoint_v1_1.json`. Expected: C1–C6 ALL PASS, VERDICT IDENTICAL, `RESULT: … S9 CLOSED`. Any MISS ⇒ S9 stays open; fingerprint, do not re-tune, return.
4. Return per the activation flags — including the original v1.0 checkpoint, the CC report, and the CC instrument as FILES. The chat side runs run-2 itself on those; two-leg means both sides run the frozen comparator.

## Non-claims
Nothing here changes any value, arm, or verdict of either leg. No fold. D-CC-1 (partial pre-Phase-0 exposure of the chat instrument's first ~280 lines via the file viewer) and D-CC-2 (LSF collision check run post-hash) are adjudicated chat-side in the fold packet, not here.

---

# EMBEDS (byte-exact; extract with the embedded script)

### EMBED — ACTIVATION FLAGS (P-4) — `activation_S9_G_2a_L1.json` (md5 8dbe00b2ad3cb76024d0de9bff5ce5da, 879 B)

<<<EMBED-BEGIN name=activation_S9_G_2a_L1.json md5=8dbe00b2ad3cb76024d0de9bff5ce5da bytes=879>>>
{
 "ARMS": "untouched (prereg \u00a78); base-arm comparison is representational only",
 "COMPARATOR_FROZEN": "g_2a_L1_compare_v1_1.py md5 faa233c06c818b6168894c579ac35876 (frozen BEFORE either leg re-emitted)",
 "INSTRUMENT_UNTOUCHED_REQUIRED": true,
 "NEW_ELECTIONS": "none",
 "RECOMPUTE": false,
 "RETURN": "g_2a_L1_cc_checkpoint_v1_1.json (md5+bytes), comparator v1.1 output verbatim, plus the ORIGINAL cc checkpoint (47ae0b85...), G_2a_L1_CCLEG_REPORT.md and g_2a_L1_ccleg.py as files \u2014 the chat side runs run-2 itself and needs them",
 "RE_EMIT_CC_CHECKPOINT_SCHEMA_v1_1": true,
 "RUN2_CRITERION": "comparator v1.1 on (chat v1.1, cc v1.1) -> C1-C6 ALL PASS; any MISS -> S9 stays open",
 "T1_SCAN": "zero hits on the re-emitted checkpoint (t1_forbidden_G_2a_L1.txt, md5 04438b74)",
 "dispatch": "S9-RESOLUTION-MINI",
 "dispatch_date": "2026-08-27",
 "gate": "G-2a-L1"
}
<<<EMBED-END name=activation_S9_G_2a_L1.json>>>

### EMBED — FROZEN COMPARATOR v1.1 — `g_2a_L1_compare_v1_1.py` (md5 faa233c06c818b6168894c579ac35876, 4989 B)

<<<EMBED-BEGIN name=g_2a_L1_compare_v1_1.py md5=faa233c06c818b6168894c579ac35876 bytes=4989>>>
#!/usr/bin/env python3
# g_2a_L1_compare_v1_1.py — Gate G-2a-L1 two-leg comparator v1.1 (S9 resolution; FROZEN pre-re-emission).
# Usage: python3 g_2a_L1_compare_v1_1.py <chat_checkpoint.json> <cc_checkpoint.json>
#
# v1.0 (md5 67ee429a) fired S9 on four REPRESENTATIONAL misses, all traced to chat-side schema/comparator
# defects (H-S4..H-S7). v1.1 changes ONLY representation handling; every numeric/boolean identity of v1.0
# is retained unchanged. The four changes, each logged:
#   R1  `arm` fields compared on the REGISTERED BASE ARM (longest registered arm name the string starts
#       with); any suffix (e.g. "-RELOCATED") is reported, not compared.            [H-S7: "optionally suffixed" vs exact string]
#   R2  `arm_sharpened` is free text (schema v1.0 said so): reported side by side, never compared. [H-S5]
#   R3  `Mplus_element_orders` compared as a SET (schema v1.1: the set of element orders of M+).  [H-S4: "sorted list" ambiguity]
#   R4  `GL23_transposition_class_size` (level-ambiguous in v1.0) is RETIRED; schema v1.1 carries two
#       fields, `GL23_transposition_class_size_PGL` and `GL23_transposition_class_size_GL`, each compared
#       exactly. A checkpoint still carrying the v1.0 field is reported, not compared.     [H-S6]
# Any MISS -> S9 remains open (prereg §8). No tolerance anywhere; this gate is exact.
import json, sys, hashlib

REGISTERED_ARMS = {
    "C3_B1.arm": ["STRUCTURE-DEPENDENT", "2O-INDUCED", "OTHER-COVER", "PIN-SPLIT", "SPLIT"],
    "C5_B2.arm": ["ASSEMBLED", "AMBIGUOUS", "OBSTRUCTED"],
    "C6_B3.assignment_disposition": ["CONSTRAINS-II", "CONSTRAINS-I", "NEUTRAL"],
}
FREE_TEXT = {"C3_B1.arm_sharpened"}
RETIRED = {"C4_F2.GL23_transposition_class_size"}
SET_VALUED = {"C2_M.Mplus_element_orders"}

def load(p): return json.load(open(p, encoding="utf-8"))

def flat(d, prefix=""):
    out = {}
    for k, v in d.items():
        key = prefix + k
        if isinstance(v, dict): out.update(flat(v, key + "."))
        else: out[key] = v
    return out

def base_arm(key, s):
    s = str(s).strip()
    for name in sorted(REGISTERED_ARMS[key], key=len, reverse=True):
        if s == name or s.startswith(name + "-") or s.startswith(name + " "):
            return name, s[len(name):]
    return None, s   # unregistered arm string -> a MISS by construction

def canon(key, v):
    if key in REGISTERED_ARMS:
        return base_arm(key, v)[0]
    if key in SET_VALUED:
        return sorted(set(int(x) for x in v))
    if isinstance(v, (list, tuple)):
        return [canon(key, x) if isinstance(x, (list, tuple)) else x for x in v]
    return v

def main(chat_p, cc_p):
    chat, cc = load(chat_p), load(cc_p)
    for p in (chat_p, cc_p):
        print("checkpoint %s md5 %s" % (p, hashlib.md5(open(p, "rb").read()).hexdigest()))
    assert chat.get("prereg_md5") == cc.get("prereg_md5") == "da9c25d19ff91f2c0809ac0027a7bebb", "prereg lock mismatch"
    print("schema chat=%s cc=%s (v1.1 expected: g2a_l1_checkpoint_v1_1)" % (chat.get("schema"), cc.get("schema")))
    blocks = [("C1", "C1_F1"), ("C2", "C2_M"), ("C3", "C3_B1"), ("C4", "C4_F2"), ("C5", "C5_B2"), ("C6", "C6_B3")]
    total_miss = 0
    for tag, key in blocks:
        a, b = flat({key: chat[key]}), flat({key: cc[key]})
        keys = sorted(set(a) | set(b))
        miss, reported = [], []
        for k in keys:
            if k in FREE_TEXT or k in RETIRED:
                reported.append((k, a.get(k, "<absent>"), b.get(k, "<absent>"))); continue
            if k not in a or k not in b:
                miss.append((k, a.get(k, "<absent>"), b.get(k, "<absent>"))); continue
            if canon(k, a[k]) != canon(k, b[k]):
                miss.append((k, a[k], b[k]))
            elif k in REGISTERED_ARMS and base_arm(k, a[k])[1] != base_arm(k, b[k])[1]:
                reported.append((k + " [suffix]", a[k], b[k]))
        print("%s %s  compared %d  miss %d  reported-only %d" % (tag, "PASS" if not miss else "MISS",
              len(keys) - len(reported), len(miss), len(reported)))
        for k, x, y in miss:     print("    MISS %s: chat=%r  cc=%r" % (k, x, y))
        for k, x, y in reported: print("    note %s: chat=%r  cc=%r" % (k, x, y))
        total_miss += len(miss)
    vc = tuple(base_arm(k, chat[k.split(".")[0]][k.split(".")[1]])[0] for k in REGISTERED_ARMS)
    vcc = tuple(base_arm(k, cc[k.split(".")[0]][k.split(".")[1]])[0] for k in REGISTERED_ARMS)
    print("VERDICT (base arms) chat=%s cc=%s  %s" % (vc, vcc, "IDENTICAL" if vc == vcc else "DIVERGENT"))
    print("assertions chat=%s cc=%s (reported, not compared)" % (chat.get("assertions"), cc.get("assertions")))
    if total_miss or vc != vcc or None in vc or None in vcc:
        print("RESULT: S9 REMAINS OPEN — counter-cross-check before any verdict.")
        return 2
    print("RESULT: C1–C6 ALL PASS under schema v1.1 — S9 CLOSED; fold-eligible on author authorization.")
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
<<<EMBED-END name=g_2a_L1_compare_v1_1.py>>>

### EMBED — CHAT CHECKPOINT v1.1 (re-emission; values unchanged from 476052b1) — `g_2a_L1_chat_checkpoint_v1_1.json` (md5 8abda98d723c4ac7e23ff144ba780a11, 2820 B)

<<<EMBED-BEGIN name=g_2a_L1_chat_checkpoint_v1_1.json md5=8abda98d723c4ac7e23ff144ba780a11 bytes=2820>>>
{
 "C1_F1": {
  "bivector_squares_minus_one_both_algebras": true,
  "characters_trivial_on_Gamma": true,
  "closures_768_384_16_8": true,
  "glide_eq_r1_circ_minusI": true,
  "h_squared_eq_t111": true,
  "meridian_minus_one": true,
  "omega_squared_eq_minus_q": true
 },
 "C2_M": {
  "M_direct_Z2_x_Mplus": true,
  "Mplus_class_sizes": [
   1,
   3,
   6,
   6,
   8
  ],
  "Mplus_element_orders": [
   1,
   2,
   3,
   4
  ],
  "Mplus_order": 24,
  "center_is_minusI_class": true,
  "center_order": 2,
  "order_M": 48
 },
 "C3_B1": {
  "D2_collapse_quotient_order": 48,
  "all_characters_kill_z": true,
  "arm": "SPLIT",
  "arm_sharpened": "NOT-INDUCED-BY-OBSTRUCTION",
  "num_characters_Gamma2_to_Z2": 8,
  "pin_dependence": "none",
  "z_is_commutator_q1_q2": true
 },
 "C4_F2": {
  "2O_all_order2_classes_of_O_lift_at_order_4": true,
  "2O_order": 48,
  "2O_unique_involution_is_minus_one": true,
  "GL23_order": 48,
  "GL23_transposition_class_has_involution_preimage": true,
  "GL23_transposition_class_size_GL": 12,
  "GL23_transposition_class_size_PGL": 6,
  "O_class_data": [
   [
    1,
    1
   ],
   [
    3,
    2
   ],
   [
    6,
    2
   ],
   [
    6,
    4
   ],
   [
    8,
    3
   ]
  ],
  "discriminator_separates": true
 },
 "C5_B2": {
  "arm": "ASSEMBLED-RELOCATED",
  "both_lifts_fix_z": true,
  "chi_3half_at_z": -4,
  "chi_3half_norm": 1,
  "chi_3half_vanishes_on_all_odd_classes": true,
  "module_transport_unique": true,
  "num_lifts_over_id_S4": 2,
  "pin_independent": true
 },
 "C6_B3": {
  "assignment_disposition": "NEUTRAL",
  "lattice_2O_sgn": {
   "1,5": 1,
   "3,3": 1,
   "3,5": 1,
   "5,1": 1,
   "5,3": 1,
   "5,5": 1,
   "7,1": 1,
   "7,3": 1,
   "7,5": 2
  },
  "lattice_2O_triv": {
   "1,1": 1,
   "3,3": 1,
   "3,5": 1,
   "5,3": 1,
   "5,5": 2,
   "7,1": 1,
   "7,3": 1,
   "7,5": 2
  },
  "lattice_2T": {
   "1,1": 1,
   "1,5": 1,
   "3,3": 2,
   "3,5": 2,
   "5,1": 1,
   "5,3": 2,
   "5,5": 3,
   "7,1": 2,
   "7,3": 2,
   "7,5": 4
  },
  "parity_law_all_tables": true
 },
 "all_checks_pass": true,
 "assertions": 8484,
 "gate": "G-2a-L1",
 "instrument_md5": "2f0fa8f4abb85291250cb49a1bf756f2",
 "leg": "chat",
 "pin_types_run": [
  "Pin+",
  "Pin-"
 ],
 "prereg_md5": "da9c25d19ff91f2c0809ac0027a7bebb",
 "reemission": {
  "changes": [
   "schema string",
   "Mplus_element_orders declared as SET (value unchanged)",
   "GL23_transposition_class_size (PGL-level 6) split into _PGL=6 (instrument line 449) and _GL=12 (gl23_class_level_addon.py, independent F_3 enumeration)"
  ],
  "from_v1_checkpoint_md5": "476052b1e075db43a6e8b7a2bb5b0be3",
  "instrument_unchanged": true,
  "note": "C5_B2.arm keeps the -RELOCATED suffix; v1.1 compares the base arm and reports the suffix"
 },
 "run_log_md5": "30951582d29372ff68595c1876581a1f",
 "schema": "g2a_l1_checkpoint_v1_1"
}
<<<EMBED-END name=g_2a_L1_chat_checkpoint_v1_1.json>>>

### EMBED — CHAT-SIDE ADD-ON for the _GL field (independent F_3 enumeration) — `gl23_class_level_addon.py` (md5 9cc8d31488a54a0d3ea5fcd7c9f34383, 2176 B)

<<<EMBED-BEGIN name=gl23_class_level_addon.py md5=9cc8d31488a54a0d3ea5fcd7c9f34383 bytes=2176>>>
#!/usr/bin/env python3
# gl23_class_level_addon.py — chat-side add-on for schema v1.1 field GL23_transposition_class_size_GL.
# The chat instrument (2f0fa8f4) asserts the PGL-level fact only (size-6 order-2 class, line 449).
# This computes, independently and exhaustively over F_3, the GL(2,3) preimage count of that class.
import itertools
F = 3
def mul(a, b):
    return ((a[0]*b[0]+a[1]*b[2]) % F, (a[0]*b[1]+a[1]*b[3]) % F,
            (a[2]*b[0]+a[3]*b[2]) % F, (a[2]*b[1]+a[3]*b[3]) % F)
I = (1,0,0,1)
GL = [m for m in itertools.product(range(F), repeat=4) if (m[0]*m[3]-m[1]*m[2]) % F]
assert len(GL) == 48
neg = lambda m: tuple((-x) % F for x in m)
Z = {I, neg(I)}
def order(m, mulf, ident):
    k, x = 1, m
    while x != ident: x = mulf(x, m); k += 1
    return k
# PGL = GL / {±I}: represent each coset by its min element
coset = lambda m: min(m, neg(m))
PGL = sorted({coset(m) for m in GL}); assert len(PGL) == 24
pmul = lambda a, b: coset(mul(a, b))
pI = coset(I)
# conjugacy classes in PGL
classes = []; seen = set()
for g in PGL:
    if g in seen: continue
    inv = {h for h in GL if mul(h, g) == I or mul(h, g) == neg(I)}  # unused guard
    cl = set()
    for h in GL:
        # h g h^-1 in PGL: find h^-1
        hinv = next(k for k in GL if mul(h, k) == I)
        cl.add(coset(mul(mul(h, g), hinv)))
    classes.append(cl); seen |= cl
sizes = sorted((len(c), order(next(iter(c)), pmul, pI)) for c in classes)
print("PGL(2,3) class (size, order):", sizes)
assert sizes == [(1,1),(3,2),(6,2),(6,4),(8,3)], "PGL(2,3) is S4 with the standard class data"
transp = next(c for c in classes if len(c) == 6 and order(next(iter(c)), pmul, pI) == 2)
pre = [m for m in GL if coset(m) in transp]
n_GL = len(pre)
n_inv = sum(1 for m in pre if order(m, mul, I) == 2)
print("GL(2,3) preimages of the size-6 PGL transposition class:", n_GL, "| genuine involutions among them:", n_inv)
assert n_GL == 12 and n_inv == 12   # H-S8: expected 6 at first writing; both lifts m, -m of an involution are involutions
print("RESULT GL23_transposition_class_size_PGL=6 GL23_transposition_class_size_GL=12 (all 12 preimages are involutions — the 2S4^- fingerprint a fortiori)")
<<<EMBED-END name=gl23_class_level_addon.py>>>

### EMBED — ADD-ON OUTPUT — `gl23_class_level_addon.log` (md5 6a231d9686ccc24b4db110b81c4f7c68, 319 B)

<<<EMBED-BEGIN name=gl23_class_level_addon.log md5=6a231d9686ccc24b4db110b81c4f7c68 bytes=319>>>
PGL(2,3) class (size, order): [(1, 1), (3, 2), (6, 2), (6, 4), (8, 3)]
GL(2,3) preimages of the size-6 PGL transposition class: 12 | genuine involutions among them: 12
RESULT GL23_transposition_class_size_PGL=6 GL23_transposition_class_size_GL=12 (all 12 preimages are involutions — the 2S4^- fingerprint a fortiori)
<<<EMBED-END name=gl23_class_level_addon.log>>>

### EMBED — EXTRACTOR — `extract_embeds_G_2a_L1.py` (md5 63942160beed37c28aed4234c185c4a0, 1464 B)

<<<EMBED-BEGIN name=extract_embeds_G_2a_L1.py md5=63942160beed37c28aed4234c185c4a0 bytes=1464>>>
#!/usr/bin/env python3
# extract_embeds_G_2a_L1.py — byte-exact extraction of every embed in the
# G-2a-L1 in-band dispatch. Usage: python3 extract_embeds_G_2a_L1.py G_2a_L1_CC_DISPATCH_INBAND.md [outdir]
# Every embed is verified against the md5 and byte count declared in its BEGIN marker.
# Any mismatch aborts (verify-then-build: nothing is built on an unverified embed).
import sys, os, re, hashlib

BEGIN = "<<<EMBED-" + "BEGIN name=(\\S+) md5=([0-9a-f]{32}) bytes=(\\d+)>>>\n"
END   = "<<<EMBED-" + "END name=%s>>>"

def main(path, outdir="."):
    data = open(path, "rb").read()
    text = data.decode("utf-8")
    n = 0
    for m in re.finditer(BEGIN, text):
        name, md5, nbytes = m.group(1), m.group(2), int(m.group(3))
        start = m.end()
        endmark = (END % name)
        j = text.find(endmark, start)
        assert j > 0, "END marker missing for " + name
        payload = text[start:j].encode("utf-8")
        got = hashlib.md5(payload).hexdigest()
        assert len(payload) == nbytes, "byte count mismatch %s: %d vs %d" % (name, len(payload), nbytes)
        assert got == md5, "md5 mismatch %s: %s vs %s" % (name, got, md5)
        out = os.path.join(outdir, name)
        open(out, "wb").write(payload)
        print("OK  %s  %s  %d B" % (md5, name, nbytes))
        n += 1
    print("extracted %d embeds, all md5/byte-verified" % n)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else ".")
<<<EMBED-END name=extract_embeds_G_2a_L1.py>>>
