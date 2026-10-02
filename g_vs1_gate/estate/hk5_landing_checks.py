#!/usr/bin/env python3
"""hk5_landing_checks.py — HK-5 landing checks for the G-VS1 fold-side estate (run from the repository root, on the landing
branch, after the estate commit; read-only; CC may re-implement these checks in its own code — the D-HK2-3 practice — the
expected values are the tables below). Usage: python3 g_vs1_gate/estate/hk5_landing_checks.py"""
import ast, hashlib, os, subprocess, sys
def md5(b): return hashlib.md5(b).hexdigest()
def sh(*a): return subprocess.run(a, capture_output=True, text=True, check=True).stdout
def blob(p): return open(p, "rb").read()
fails = []
def check(name, cond, seen=""):
    print(("PASS  " if cond else "FAIL  ") + name + ("" if cond else f"   (seen: {seen})"))
    if not cond: fails.append(name)
G = "g_vs1_gate/"; E = G + "estate/"
# 1. the estate manifest (22 files, self-excluded) and every estate file at its md5 / byte count of record
ESTATE = {
    "G_VS1_TWOLEG_CLOSURE_MEMO.md":           ("a7e2604d4dc56b1c12310880d5407211", 23468),
    "FOLD_AUTHORIZATION_V4_88.md":            ("957f7bb65b6ea9677c7110032129769d", 4193),
    "foldin_v4_88_g_vs1.py":                  ("4f1f913684b736df5caa944f12dab031", 7777),
    "V4_88_DELTA_ONLY.txt":                   ("848ef11871ac3b43534c20ae7528f2cb", 10379),
    "verify_v4_88_additive.py":               ("1ae94b68021f7dbb6fefaa9ff23e6771", 4909),
    "verify_v4_88_additive.log":              ("88aed80860171b1ab815659277b757d3", 869),
    "g_vs1_compare_v1_1.py":                  ("736a8b82fbdf1ad891f1f545572b8e36", None),
    "s9_projection_v1_0.py":                  ("2833c0c276be35c5e05fc0406ff82ab5", None),
    "g_vs1_twoleg_comparison.json":           ("629b99aa0a4071b10c5656bc20f1ef73", 67715),
    "g_vs1_twoleg_comparison_preread.json":   ("707bbb72db288a697dedb979481b7f3d", 10586),
    "g_vs1_twoleg_comparison_v1_1_raw.json":  ("9c1e9b56c1f649c601f011aa015f873f", None),
    "g_vs1_twoleg_comparison_s9.json":        ("d4a9913e5abec4ddb32ae241fcad597a", None),
    "g_vs1_twoleg_comparison_preread_s9.json": ("27d988105b11af0cbde224a846c63519", None),
    "g_vs1_chatleg_checkpoint_s9.json":       ("63806cf56960ca303664a95c14089578", None),
    "g_vs1_ccleg_checkpoint_s9.json":         ("e20e7edc32072a2e5bd71f6a90fa5d2f", None),
    "g_vs1_chatleg_prereadcheckpoint_s9.json": ("405f273af2db039c21e531d1233553f4", None),
    "g_vs1_ccleg_prereadcheckpoint_s9.json":  ("a75c4adfc0116343d9fa231b4663fdb1", None),
    "run_compare.log":                        ("31944e07b860ecc8f49703967b05810d", None),
    "run_compare_v1_1_raw.log":               ("e96f2032d1d701244ba5bb9e1652f87d", None),
    "run_compare_s9.log":                     ("12895014f987a38032ce233e936bd109", None),
    "run_compare_preread_s9.log":             ("58d29297b2cad23baf12a58fd1e1553c", None),
}
man = dict((l.split()[1].lstrip("*"), l.split()[0]) for l in open(E + "ESTATE_MANIFEST.md5").read().split("\n") if l.strip())
check("manifest lists exactly the 22 estate files (the 21 above + this script; self-excluded)", set(man) == set(ESTATE) | {"hk5_landing_checks.py"} and "ESTATE_MANIFEST.md5" not in man, sorted(set(man) ^ (set(ESTATE) | {"hk5_landing_checks.py"})))
check("this script is the manifest's copy", man.get("hk5_landing_checks.py") == md5(blob(E + "hk5_landing_checks.py")), man.get("hk5_landing_checks.py"))
for f, (h, n) in sorted(ESTATE.items()):
    b = blob(E + f)
    check(f"estate/{f} md5 {h[:8]}" + (f" / {n:,} B" if n else ""), md5(b) == h and man.get(f) == h and (n is None or len(b) == n), f"{md5(b)} / {len(b)}")
# 2. the CC leg's files on the branch and the dispatch's raw/quarantined embeds at their md5s of record
CC = {
    G + "g_vs1_ccleg.py":                        "0ba1abe47793375bf8d0b59573b99e64",
    G + "g_vs1_ccleg_prereadcheckpoint.json":    "7c4073730ddbe2b3f4ac5a13c0e24354",
    G + "g_vs1_ccleg_checkpoint.json":           "05e82029d8d978661bc200b9bec1755c",
    G + "G_VS1_CC_RETURN_INBAND.md":             "90af4af5c129f7005acfcfeaca3cdca8",
    G + "G_VS1_CC_COMPARISON_NOTE.md":           "e403b78f964f55236240156cada1b812",
    G + "g_vs1_twoleg_comparison_cc.json":       "629b99aa0a4071b10c5656bc20f1ef73",
    G + "g_vs1_twoleg_comparison_preread_cc.json": "707bbb72db288a697dedb979481b7f3d",
    G + "g_vs1_twoleg_forms_direct_cc.json":     "9f19862fc85f9e16ba972e593df3e455",
    G + "tools/compare_forms_direct_cc.py":      "7c79ab472786765a5b7817c39e9220e0",
    G + "staging_memo_G_VS1_v2.md":              "58fd02671ea77db63e22afdcc5ee93a0",
    G + "staging_memo_G_VS1_v1.md":              "bfe0336ae6b1c2f419e876568023dd4d",
    G + "G_VS1_LOCK_RECORD.md":                  "71711946d1c4abb06fa17402e8d5a6c9",
    G + "g_vs1_schema_v1_0.json":                "4690e07d5a22cc7a1c5d08db39eda3fe",
    G + "g_vs1_compare_v1_0.py":                 "69011375d28ec8f63f3ac76383e98321",
    G + "tools/t1/T1_forbidden_G_VS1.txt":       "324f577d20e2bfba3b594d96c4ca3ba7",
    G + "tools/t1/T1_base_author_20260919.txt":  "05302210cc4ceb70553acbe8379e9fc3",
    G + "tools/t1/t1_stratum_G_VS1.txt":         "d0916f06f63cb1f3aca7fb8432ed878f",
    G + "tools/t1/t1_scan.py":                   "6b86290090a8c84f1b1a0a99ec0bf697",
    G + "inputs/paper_II_3_4_4_and_3_4_7_extract.md": "940b0bee4b2112e911ae738c3db2bc3d",
    G + "V4_88_HOUSEKEEPING_STAGING.md":         "715b9d23ba2d2ff1a065e01dda8ab29a",
    G + "quarantine/g_vs1_chatleg.py":           "cb2e22308305cb6e2251531465984df5",
    G + "quarantine/g_vs1_chatleg_prereadcheckpoint.json": "b208db869bbc0c8c80c482737d957d9d",
    G + "quarantine/g_vs1_chatleg_checkpoint.json": "d3d1ed074259c8924d0c29a03d320918",
    G + "quarantine/G_VS1_CHATLEG_EXECUTION_REPORT.md": "50549ae835913d99849e875693258129",
    G + "quarantine/run_chatleg.log":            "4b3847fdc0d2eb9069a2ce4dfcb36bb9",
}
for p, h in CC.items():
    ok = os.path.exists(p) and md5(blob(p)) == h
    check(f"{p} md5 {h[:8]}", ok, md5(blob(p)) if os.path.exists(p) else "MISSING")
check("the chat-side comparator run of record is byte-identical to CC's", md5(blob(E + "g_vs1_twoleg_comparison.json")) == md5(blob(G + "g_vs1_twoleg_comparison_cc.json")))
check("the chat-side pre-read comparison is byte-identical to CC's", md5(blob(E + "g_vs1_twoleg_comparison_preread.json")) == md5(blob(G + "g_vs1_twoleg_comparison_preread_cc.json")))
# 3. the commits the record cites and the branch ancestry
COMMITS = {
    "82b2ff9": "G-VS1 CC leg: the thirteen raw dispatch embeds",
    "c44d731": "G-VS1 CC leg: pre-read checkpoint (Phase 0)",
    "f9b88d9": "G-VS1 CC leg: pre-consultation checkpoint",
    "d3577eb": "G-VS1 CC leg return (single file, in-band)",
    "c21a25f": "G-VS1 CC leg: armor opened; frozen comparator v1.0 runs",
    "7460a78": "Merge pull request #33 from gifgaf0/claude/new-session-7flqwf",
}
for sha, subj in COMMITS.items():
    try: s = sh("git", "log", "-1", "--format=%s", sha).strip()
    except subprocess.CalledProcessError: s = "MISSING"
    check(f"commit {sha}: '{subj[:44]}…'", s.startswith(subj), s[:60])
for sha in ("7460a78", "82b2ff9", "c44d731", "f9b88d9", "d3577eb", "c21a25f"):
    check(f"HEAD contains {sha}", subprocess.run(["git", "merge-base", "--is-ancestor", sha, "HEAD"]).returncode == 0)
par = sh("git", "log", "-1", "--format=%P", "7460a78").split()
check("7460a78 is a two-parent merge (PR #33) whose second parent is 1360578", len(par) == 2 and par[1].startswith("1360578"), par)
# 4. internal citations: the authorization, the fold script and the delta against the estate
auth = blob(E + "FOLD_AUTHORIZATION_V4_88.md").decode(); fs = blob(E + "foldin_v4_88_g_vs1.py").decode(); delta = blob(E + "V4_88_DELTA_ONLY.txt").decode()
check("authorization cites base dc243cb4… (1,757,725 B) and the closure memo a7e2604d… (23,468 B)", "dc243cb4fd98f8c79e2a139f138eb6b0" in auth and "1,757,725 B" in auth and "a7e2604d4dc56b1c12310880d5407211" in auth and "23,468 B" in auth)
check("fold script guards the base dc243cb4… / 1757725 B and the closure memo a7e2604d…", 'BASE_MD5 = "dc243cb4fd98f8c79e2a139f138eb6b0"' in fs and "BASE_BYTES = 1757725" in fs and 'MEMO_MD5 = "a7e2604d4dc56b1c12310880d5407211"' in fs)
check("delta lists the eight edits once each (E1..E8) with the bracket multiplicities ×2 and ×3", all(f"=== E{i}" in delta for i in range(1, 9)) and "(×2:" in delta and "(×3:" in delta and delta.count("[→ V4.88 housekeeping: HK-4 landed") == 1 and delta.count("[→ G-VS1 (V4.88) scoping:") == 1)
check("delta's record is the closure memo's record with the two placeholders filled", "**V4.88 fold-in record (October 2, 2026):** GATE FOLD" in delta and "⟨date/time⟩" not in delta and "⟨to be quoted at fold⟩" not in delta and "October 2, 2026, 14:51 PDT" in delta and "2026-10-02 21:52:01 UTC" in delta)
memo = blob(E + "G_VS1_TWOLEG_CLOSURE_MEMO.md").decode()
u = memo.split("**§2.91.U (new; after §2.91.T):** ")[1].split("\n\n**Part VI row")[0].strip()
check("delta's §2.91.U equals the closure memo's §2.91.U verbatim", u in delta and u.startswith("**U. Gate G-VS1 REGISTERED"))
row = memo.split("**Part VI row (after the G-MSCS-A row):** `")[1].split("`\n")[0]
check("delta's Part VI row equals the closure memo's row verbatim (3 cells)", row in delta and row.count("|") == 3)
log = blob(E + "verify_v4_88_additive.log").decode()
check("verifier log: ADDITIVE DIFF VERIFIED, 8 changed lines, 6 added lines", log.rstrip().endswith("ADDITIVE DIFF VERIFIED") and "changed lines: 8" in log and "added lines: 6" in log)
# 5. syntax of the four chat-side scripts (not executed: the canonicals are not in the repository)
for f in ("foldin_v4_88_g_vs1.py", "verify_v4_88_additive.py", "g_vs1_compare_v1_1.py", "s9_projection_v1_0.py"):
    try: ast.parse(blob(E + f).decode()); ok = True
    except SyntaxError: ok = False
    check(f"ast.parse {f}", ok)
# 6. the S9 result reproduced from the landed files: v1.1 on the projected checkpoints -> 445/445 and 71/71
for a, b, exp in (("g_vs1_chatleg_checkpoint_s9.json", "g_vs1_ccleg_checkpoint_s9.json", "445 checks, 445 PASS, 0 MISS"), ("g_vs1_chatleg_prereadcheckpoint_s9.json", "g_vs1_ccleg_prereadcheckpoint_s9.json", "71 checks, 71 PASS, 0 MISS")):
    r = subprocess.run([sys.executable, "estate/g_vs1_compare_v1_1.py", "compare", "estate/" + a, "estate/" + b], capture_output=True, text=True, cwd=G)   # the comparator reads the schema from its cwd (g_vs1_gate/)
    check(f"comparator v1.1 on the projected pair ({a[:8]}…): {exp}", exp in r.stdout, r.stdout[:120])
# 7. T1: every estate file under the gate list, A1-free (this gate has no A1), and the base
T = G + "tools/t1/"
for f in sorted(ESTATE) + ["ESTATE_MANIFEST.md5", "hk5_landing_checks.py"]:
    for lst in ("T1_forbidden_G_VS1.txt", "T1_base_author_20260919.txt"):
        r = subprocess.run([sys.executable, T + "t1_scan.py", T + lst, E + f], capture_output=True, text=True)
        last = (r.stdout.strip().split("\n") or [""])[-1]
        check(f"T1 {f} vs {lst[:22]}: {last[-45:]}", "CLEAN" in last and "hits=[]" in last, last[-80:])
print()
print("HK-5 LANDING CHECKS: " + ("ALL PASS" if not fails else f"{len(fails)} FAILED: " + "; ".join(fails)))
sys.exit(0 if not fails else 1)
