#!/usr/bin/env python3
# g_2a_L1_compare.py — Gate G-2a-L1 two-leg comparator (FROZEN pre-return).
# Usage: python3 g_2a_L1_compare.py g_2a_L1_chat_checkpoint.json g_2a_L1_cc_checkpoint.json
# Criteria (all EXACT — integers, booleans, tables; no tolerances apply to this gate):
#   C1  F1 regression pack           bit-identical booleans
#   C2  motion group M structure     bit-identical (orders, class sizes, element orders)
#   C3  B1 obstruction + collapse    bit-identical + arm identity
#   C4  F2 discriminator control     bit-identical + separation
#   C5  B2 assembly                  bit-identical + arm identity
#   C6  B3 admissibility lattices    entry-for-entry identity (3 tables) + parity law + disposition bit
# Any MISS -> S9 counter-cross-check protocol (pre-registration §8); no verdict before S9 closes.
# Provenance fields (instrument md5, run-log md5) are REPORTED, never compared (legs are independent).
import json, sys, hashlib

def load(p):
    return json.load(open(p, encoding="utf-8"))

def flat(d, prefix=""):
    out = {}
    for k, v in d.items():
        key = prefix + k
        if isinstance(v, dict):
            out.update(flat(v, key + "."))
        else:
            out[key] = v
    return out

def norm(v):
    # canonicalize lists/tuples for exact comparison; lattices are dicts of ints
    if isinstance(v, (list, tuple)):
        return [norm(x) for x in v]
    return v

def main(chat_p, cc_p):
    chat, cc = load(chat_p), load(cc_p)
    for p in (chat_p, cc_p):
        print("checkpoint %s md5 %s" % (p, hashlib.md5(open(p, "rb").read()).hexdigest()))
    assert chat.get("schema") == cc.get("schema") == "g2a_l1_checkpoint_v1", "schema mismatch"
    assert chat.get("prereg_md5") == cc.get("prereg_md5") == "da9c25d19ff91f2c0809ac0027a7bebb", "prereg lock mismatch"
    blocks = [("C1", "C1_F1"), ("C2", "C2_M"), ("C3", "C3_B1"), ("C4", "C4_F2"), ("C5", "C5_B2"), ("C6", "C6_B3")]
    total_miss = 0
    for tag, key in blocks:
        a, b = flat(chat[key]), flat(cc[key])
        keys = sorted(set(a) | set(b))
        miss = []
        for k in keys:
            if k not in a or k not in b or norm(a[k]) != norm(b[k]):
                miss.append((k, a.get(k, "<absent>"), b.get(k, "<absent>")))
        status = "PASS" if not miss else "MISS"
        print("%s %s  items %d  miss %d" % (tag, status, len(keys), len(miss)))
        for k, x, y in miss:
            print("    %s: chat=%r  cc=%r" % (k, x, y))
        total_miss += len(miss)
    # verdict-level line
    v_chat = (chat["C3_B1"]["arm"], chat["C5_B2"]["arm"], chat["C6_B3"]["assignment_disposition"])
    v_cc   = (cc["C3_B1"]["arm"],   cc["C5_B2"]["arm"],   cc["C6_B3"]["assignment_disposition"])
    print("VERDICT chat=%s cc=%s  %s" % (v_chat, v_cc, "IDENTICAL" if v_chat == v_cc else "DIVERGENT"))
    print("assertions chat=%s cc=%s (reported, not compared)" % (chat.get("assertions"), cc.get("assertions")))
    if total_miss or v_chat != v_cc:
        print("RESULT: S9 TRIGGERED — counter-cross-check protocol before any verdict.")
        return 2
    print("RESULT: C1–C6 ALL PASS — S9 NOT triggered; fold-eligible on author authorization.")
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
