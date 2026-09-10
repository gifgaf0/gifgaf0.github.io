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
