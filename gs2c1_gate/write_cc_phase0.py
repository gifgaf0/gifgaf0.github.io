#!/usr/bin/env python3
# write_cc_phase0.py — G-S2C1 CC leg, Phase 0 close: embed verification record.
# Re-hashes every extracted embed on disk against the dispatch manifest and writes cc_phase0.json.
import json, hashlib, os, datetime

MANIFEST = [
    # (name, md5, bytes, enc, quarantine)
    ("activation_G_S2C1.json", "7a37816df1bd076636d5c78ab7d04b1e", 3536, "raw", False),
    ("G_S2_ON_CONE_EXECUTION_PREREGISTRATION.md", "2ea8ec13ffa3c32898cc24a3be605c64", 12984, "raw", False),
    ("G_S2_ON_CONE_LOCK_RECORD.md", "f2f4d50029fb5be3122a885c48a7e04f", 3009, "raw", False),
    ("G_S2_ON_CONE_LOCK_RECORD_ADDENDUM_A1.md", "8bf51bd05c691f3f03d796b231cdd262", 1019, "raw", False),
    ("G_S2_ON_CONE_LOCK_RECORD_ADDENDUM_A2.md", "a9bda086213ee0afe1e2ba01055659cd", 1950, "raw", False),
    ("t1_forbidden_G_S2_ON_CONE.txt", "8cd89b9a82704accd89f7ff6f5e220b4", 144, "raw", False),
    ("g_s2c1_compare.py", "e730844e9cf9e722e0e7789f90f34489", 4643, "raw", False),
    ("extract_embeds_v2.py", "d4ac62219a95bea1e29d226e371ee39a", 2102, "raw", False),
    ("s2c1_chat_cmp_checkpoint.json", "2aa66ea21dd5cda16535d409654fe4dd", 2164, "b64", True),
    ("g_s2c1_phase0_close.py", "1882c941fc4288b031131fb8aacccf83", 11719, "b64", True),
    ("g_s2c1_phase1.py", "c987a1a6f3ec8c3308dfb3bb1279bb09", 17227, "b64", True),
    ("g_s2c1_phase1_ladder.py", "a9949649af4a2e99e3ae69186a066c23", 21163, "b64", True),
    ("s2c1_phase1_ladder_analysis.py", "a55b0544d3c5ce7ab050a4af01492b4e", 3134, "b64", True),
    ("gz1_core.py", "361b1743a9164d1f7ff2380f6b74840d", 18205, "b64", True),
    ("g_s2c1_phase0_checkpoint.json", "eae2bbd734f5129dd1e51efcbb55dd3d", 4555, "b64", True),
    ("g_s2c1_phase1_checkpoint.json", "eeedcfa594a24915fa9c10c6abbd0a4e", 2477, "b64", True),
    ("g_s2c1_phase1_ladder_checkpoint.json", "5ee152fc14ac55e72094fc660aff7a4a", 43647, "b64", True),
    ("s2c1_phase1_ladder_analysis.json", "bdfd3d01bc3f4cef0e22232bb7ff7eb5", 6507, "b64", True),
    ("s2c1_phase1_A2_evaluation.json", "77fea65fde95efd33d8990956c7c07ff", 2934, "b64", True),
    ("G_S2C1_PHASE0_REPORT.md", "5f678490ed33040705c372065cfd1124", 6556, "b64", True),
    ("G_S2C1_PHASE1_HALT_REPORT.md", "b0e6790c323764d7e93350d2b5ef09a8", 4107, "b64", True),
    ("G_S2C1_PHASE1_LADDER_REPORT.md", "6995cee96c9e696241b038a709dabcaf", 5341, "b64", True),
    ("psi0_gem8_n64.npy", "a56796186e5eaf78c2e513fc710cb143", 32896, "b64", True),
]

def md5f(p):
    return hashlib.md5(open(p, "rb").read()).hexdigest()

def main():
    rows, ok = [], True
    for name, md5, nbytes, enc, q in MANIFEST:
        p = os.path.join("QUARANTINE", name) if q else name
        h = md5f(p); n = os.path.getsize(p)
        good = (h == md5 and n == nbytes)
        ok = ok and good
        rows.append({"name": name, "md5_manifest": md5, "md5_on_disk": h, "bytes": n,
                     "enc": enc, "quarantined": q, "verified": good})
    out = {
        "gate": "G-S2C1", "leg": "cc", "phase": 0,
        "date": datetime.date.today().isoformat(),
        "dispatch_file": "G_S2C1_CC_DISPATCH_INBAND.md",
        "dispatch_md5": md5f("G_S2C1_CC_DISPATCH_INBAND.md"),
        "extractor": "extract_embeds_v2.py (embedded raw, md5 d4ac62219a95bea1e29d226e371ee39a)",
        "embeds_total": len(rows), "embeds_verified": sum(r["verified"] for r in rows),
        "quarantined_unread": True,
        "prereg_md5": "2ea8ec13ffa3c32898cc24a3be605c64",
        "lock_record_md5": "f2f4d50029fb5be3122a885c48a7e04f",
        "addendum_A1_md5": "8bf51bd05c691f3f03d796b231cdd262",
        "addendum_A2_md5": "a9bda086213ee0afe1e2ba01055659cd",
        "t1_md5": "8cd89b9a82704accd89f7ff6f5e220b4",
        "comparator_md5": "e730844e9cf9e722e0e7789f90f34489",
        "all_verified": ok,
        "embed_table": rows,
    }
    json.dump(out, open("cc_phase0.json", "w"), indent=1)
    print("cc_phase0.json written; all_verified =", ok)

if __name__ == "__main__":
    main()
