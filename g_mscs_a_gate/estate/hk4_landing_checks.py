#!/usr/bin/env python3
"""hk4_landing_checks.py — HK-4 landing checks for the G-MSCS-A estate (run from the repository root, on the landing
branch, after the estate commit; read-only; CC may instead re-implement these checks in its own code — the D-HK2-3
practice — the expected values are the table below). Never prints a value of the sealed file: the sealed armor is
decoded only to assert its md5 and byte count.

Usage: python3 g_mscs_a_gate/estate/hk4_landing_checks.py
"""
import ast, base64, hashlib, os, subprocess, sys

def md5(b): return hashlib.md5(b).hexdigest()
def sh(*a): return subprocess.run(a, capture_output=True, text=True, check=True).stdout
def blob(path): return open(path, "rb").read()

fails = []
def check(name, cond, seen=""):
    print(("PASS  " if cond else "FAIL  ") + name + ("" if cond else f"   (seen: {seen})"))
    if not cond: fails.append(name)

G = "g_mscs_a_gate/"; E = G + "estate/"

# 1. The estate manifest (14 files, self-excluded) and every estate file at its md5 / byte count of record.
ESTATE = {
    "FOLD_AUTHORIZATION_V4_87.md":         ("65ab87e41ff297216ca90e5ce8429e1e", 4481),
    "G_MSCS_A_TWOLEG_CLOSURE_MEMO.md":     ("74072dcc8a4e9d8363e300ef5d81061d", None),
    "H_MS2_9_ERRATUM.md":                  ("13dc2e695c9c798aad44b1f49ca3d773", 5499),
    "V4_87_DELTA_ONLY.txt":                ("7238998bb403610dad6419a9ff40d339", 26737),
    "foldin_v4_87_g_mscs_a.py":            ("ed80ee80de2f758fc3befe4fa3b0abf2", 37093),
    "g_mscs_a_chatleg_checkpoint.json":    ("4a933fdb2ee24874bf26a921d4030196", 71354),
    "g_mscs_a_twoleg_comparison.json":     ("a29768908ad5b19e0d29b9e7b21ab2d0", None),
    "g_mscs_a_twoleg_comparison_s9.json":  ("32bad51a4a2454f16d46539542c243f3", None),
    "run_read.log":                        ("fd109fa8937b81526541ddd3f5f07f90", None),
    "s9_projection_v1_0.py":               ("6daf7c066d92031662159271a29591be", None),
    "sa_t1a1_build.py":                    ("dc7a747e91ce57cd8305296e579b09f3", 4367),
    "verify_v4_87_additive.log":           ("7e6a2d1c1038e47d6c2fc07ae5385b3a", 843),
    "verify_v4_87_additive.py":            ("4c268e917f9e7a7009cf3016a980f838", 4624),
}
man = open(E + "ESTATE_MANIFEST.md5").read().split("\n")
man = dict((l.split()[1].lstrip("*"), l.split()[0]) for l in man if l.strip())
check("manifest lists exactly the 14 estate files (the 13 above + this script; self-excluded)", set(man) == set(ESTATE) | {"hk4_landing_checks.py"} and "ESTATE_MANIFEST.md5" not in man, sorted(man))
check("this script is the manifest's copy", man.get("hk4_landing_checks.py") == md5(blob(E + "hk4_landing_checks.py")), man.get("hk4_landing_checks.py"))
for f, (h, n) in sorted(ESTATE.items()):
    b = blob(E + f)
    check(f"estate/{f} md5 {h[:8]}" + (f" / {n:,} B" if n else ""), md5(b) == h and man.get(f) == h and (n is None or len(b) == n), f"{md5(b)} / {len(b)}")

# 2. The CC leg's files (the PR #32 commit on main; the four later commits on the branch) at the md5s of record.
CC = {
    G + "g_mscs_a_ccleg.py":                        "a5263388f2db2ce676060551e5636d81",
    G + "g_mscs_a_ccleg_prereadcheckpoint.json":    "c9f8e4af305f579b1b19953725042d87",
    G + "g_mscs_a_ccleg_checkpoint.json":           "d0e129fc8c324f0779803a6e33068777",
    G + "G_MSCS_A_CC_RETURN_INBAND.md":             "1f4c66b950446bd04aacea31ec92f2b2",
    G + "G_MSCS_A_CC_RETURN_ADDENDUM_1.md":         "f364a802baa7322480187ff701472ce8",
    G + "G_MSCS_A_CC_RETURN_plaintext.md":          "8a2844c6663d0191fac0fcc899501347",
    G + "g_mscs_a_preread_twoleg_comparison.json":  "3e756acc7b5716dd7fbde46ff914dff5",
    G + "build_return.py":                          "4987626815f6206be010187415f3713c",
    G + "run_read.log":                             "5e2de03a6f887d3e4e14c3ab88309f1b",
    # the decoded quarantine (chat-side artifacts, committed by CC after its return)
    G + "g_mscs_a_chatleg.py":                      "0d0e5ecf610b34f21e8c22dd3938ce40",
    G + "g_mscs_a_chatleg_prereadcheckpoint.json":  "ccbb32077996833cdac2339938193ec1",
    G + "G_MSCS_A_MAPPER_FREEZE_AND_PREREAD_REPORT.md": "1bf60dd342adbe3f09043365cd25e021",
    # the locked artifacts and the pinned sources (on main since PR #32)
    G + "G_MSCS_A_LOCK_RECORD.md":                  "8116cc622279b5d4e73214178ae97cd8",
    G + "dispatch.md":                              "a934bc9463f9abf31cded093d750ed63",
    G + "staging_memo_G_MSCS_A_v2.md":              "6ea16b952db835bb351d3dc1b474c6ed",
    G + "pinned_inputs_G_MSCS_A.json":              "2d44ec01a66889f330d940dee3313bdc",
    G + "g_mscs_a_schema_v1_0.json":                "5323e11fc27d688f61aaf57302c875c0",
    G + "g_mscs_a_compare_v1_0.py":                 "c5b4a7aab2fc8651be6d26d1f3d25642",
    G + "sa_build_pinned_inputs.py":                "8189100ede80eac360b25a146e580abf",
    G + "sa_verify_pinned_inputs.py":               "cf004d517d2efe91a02c92a58e3df6bf",
    G + "sa_anchor_validate.py":                    "3a11c8f1421d26b882097dbd4e0759d7",
    G + "tools/t1/T1_forbidden_G_MSCS_A.txt":       "e274e58ea50b9ed347969e507d2a4f36",
    G + "tools/t1/t1_forbidden_G_MSCS_A_A1.txt":    "3b753b3a371a162fc2ab21b9eed51bd5",
    G + "tools/t1/T1_base_author_20260919.txt":     "05302210cc4ceb70553acbe8379e9fc3",
    G + "tools/t1/t1_scan.py":                      "6b86290090a8c84f1b1a0a99ec0bf697",
    G + "inputs/gmscs2_gate/g_mscs2_chatleg_checkpoint.json": "1c5b6b59829d2a6b9ae2b1a7a016832d",
    G + "inputs/gmscs2_gate/g_mscs2_ccleg_checkpoint.json":   "9961745d1e1857cfab6445d4754b5060",
    G + "inputs/gmscs2_gate/diag_quadform_basis.json":        "d84aa1fd",
    G + "inputs/gmscs2_gate/diag_kappa24.json":               "b7952dfc",
    G + "inputs/gmscs1_gate/g_mscs1_chatleg_checkpoint.json": "c04c0b8e",
    G + "inputs/gmscs1_gate/g_mscs1_ccleg_checkpoint.json":   "249e11dd",
    G + "inputs/gci1_gate/ci1_phase3_cc_r2.json":             "845ae6be",
    "gmscs2_gate/tools/t1/T1_forbidden_G_MSCS2.txt":          "be921b8c",
    "gmscs2_gate/G_MSCS2_LOCK_RECORD.md":                     "49232d4c",
    "gmscs2_gate/G_MSCS2_CC_RETURN_INBAND.md":                "290b3431",
}
for p, h in CC.items():
    ok = os.path.exists(p) and md5(blob(p)).startswith(h)
    check(f"{p} md5 {h[:8]}", ok, md5(blob(p)) if os.path.exists(p) else "MISSING")

# 3. The sealed armor on main: md5 and byte count of the decoded file only (nothing of its content is read or printed).
arm = open(G + "sealed/anchors_G_MSCS_A_SEALED.md.b64", "rb").read()
body = b"".join(l for l in arm.splitlines(keepends=True) if not l.startswith(b"====="))
dec = base64.decodebytes(body)
check("sealed file decodes to md5 cfd62dcf… / 177 B (asserted, never printed)", md5(dec) == "cfd62dcf060427ac3402604e6c3284ff" and len(dec) == 177, f"{md5(dec)[:8]} / {len(dec)}")
del dec, body

# 4. The commits the V4.87 record cites (subjects by prefix; merges by parent count).
COMMITS = {
    "1752296": "G-MSCS-A CC leg: blind build + pre-read checkpoint",
    "21b7d79": "G-MSCS-A CC leg: pre-consultation checkpoint",
    "48fa2a3": "G-MSCS-A CC return (single file, in-band)",
    "620c421": "G-MSCS-A CC leg: quarantine opened",
    "13070d8": "G-MSCS-A CC return addendum 1",
    "6755cf7": "Merge pull request #32 from gifgaf0/claude/new-session-7flqwf",
    "e1fa071": "Merge pull request #31 from gifgaf0/claude/new-session-txamk5",
    "c351d2a": "HK-3 CC return (single file, in-band)",
    "304a099": "HK-2 CC return (single file, in-band)",
}
for sha, subj in COMMITS.items():
    try: s = sh("git", "log", "-1", "--format=%s", sha).strip()
    except subprocess.CalledProcessError: s = "MISSING"
    check(f"commit {sha}: '{subj[:40]}…'", s.startswith(subj), s[:60])
par = sh("git", "log", "-1", "--format=%P", "6755cf7").split()
check("6755cf7 is a two-parent merge whose second parent is 1752296", len(par) == 2 and par[1].startswith("1752296"), par)
anc = subprocess.run(["git", "merge-base", "--is-ancestor", "1752296", "HEAD"]).returncode == 0
check("HEAD (the landing branch) contains 1752296 (the PR #32 commit; main = 6755cf7 is its merge, so the PR onto main is a clean successor)", anc)
for sha in ("21b7d79", "48fa2a3", "620c421", "13070d8"):
    check(f"HEAD contains {sha} (the four post-PR-#32 commits ride this PR)", subprocess.run(["git", "merge-base", "--is-ancestor", sha, "HEAD"]).returncode == 0)

# 5. Internal citations of the record (the delta) and the authorization.
delta = blob(E + "V4_87_DELTA_ONLY.txt").decode()
auth = blob(E + "FOLD_AUTHORIZATION_V4_87.md").decode()
cnt = {h: delta.count(h) for h in ("13dc2e69", "74072dcc", "65ab87e4", "d4c42a53", "4a933fdb", "d0e129fc")}
check("delta cites erratum 13dc2e69 ×5, closure memo 74072dcc ×3, authorization 65ab87e4 ×2, base d4c42a53 ×2, chat checkpoint 4a933fdb ×4, CC checkpoint d0e129fc ×5",
      cnt == {"13dc2e69": 5, "74072dcc": 3, "65ab87e4": 2, "d4c42a53": 2, "4a933fdb": 4, "d0e129fc": 5}, cnt)
hdr = ("=== E8 H-MS2-9 bracket (×4) ===", "=== E9 H-SA-3 bracket (×3) ===", "=== E10 H-SA-4 κ₂₄ bracket (×4) ===", "=== E10 H-SA-4 S₄/b₁ bracket (×1) ===")
check("delta lists the three honesty brackets once each with their multiplicities (H-MS2-9 ×4, H-SA-3 ×3, H-SA-4 ×4 + ×1), 'V4.87' resolved, no 'V4.8x'",
      all(delta.count(h) == 1 for h in hdr) and delta.count("[H-MS2-9 (V4.87)") == 1 and delta.count("[H-SA-3 (V4.87)") == 1 and delta.count("[H-SA-4 (V4.87)") == 2 and "V4.8x" not in delta,
      ([delta.count(h) for h in hdr], delta.count("[H-MS2-9 (V4.87)"), delta.count("[H-SA-3 (V4.87)"), delta.count("[H-SA-4 (V4.87)")))
err = blob(E + "H_MS2_9_ERRATUM.md").decode()
import re
texts = re.findall(r"\[(H-MS2-9|H-SA-3|H-SA-4) \(V4\.8x\):(.*?)\]", err)
dtexts = re.findall(r"\[(H-MS2-9|H-SA-3|H-SA-4) \(V4\.87\):(.*?)\]\*\*", delta)
check("the four bracket texts in the delta equal the erratum's four bracket texts with 'V4.8x' → 'V4.87' (word-for-word)", [t for t in texts] == [t for t in dtexts], (len(texts), len(dtexts)))
check("delta carries the V4.86 correction (CC's branch claude/new-session-txamk5 retained; c351d2a)", "txamk5" in delta and "c351d2a" in delta and "304a099" in delta)
check("authorization cites base d4c42a53… (1,730,321 B), erratum 13dc2e69… (5499 B), closure memo 74072dcc…", "d4c42a53cbd6d325ebc740879288e844" in auth and "1,730,321 B" in auth and "13dc2e695c9c798aad44b1f49ca3d773" in auth and "5499 B" in auth and "74072dcc8a4e9d8363e300ef5d81061d" in auth)
check("verifier log ends 'ADDITIVE DIFF VERIFIED' (6 added lines; 7 changed: 2 header bumps + 5 bracketed)", blob(E + "verify_v4_87_additive.log").decode().rstrip().endswith("ADDITIVE DIFF VERIFIED") and "added lines: 6" in blob(E + "verify_v4_87_additive.log").decode() and "changed lines: 7" in blob(E + "verify_v4_87_additive.log").decode())

# 6. Syntax of the three chat-side scripts (not executed: the canonicals are not in the repository).
for f in ("foldin_v4_87_g_mscs_a.py", "verify_v4_87_additive.py", "s9_projection_v1_0.py", "sa_t1a1_build.py"):
    try: ast.parse(blob(E + f).decode()); ok = True
    except SyntaxError as e: ok = False
    check(f"ast.parse {f}", ok)

# 7. T1: every estate file under the gate list ∪ A1 ∪ base (hits by index only).
T = G + "tools/t1/"
for f in sorted(ESTATE) + ["ESTATE_MANIFEST.md5", "hk4_landing_checks.py"]:
    if not os.path.exists(E + f): continue
    for lst in ("T1_forbidden_G_MSCS_A.txt", "t1_forbidden_G_MSCS_A_A1.txt", "T1_base_author_20260919.txt"):
        r = subprocess.run([sys.executable, T + "t1_scan.py", T + lst, E + f], capture_output=True, text=True)
        last = (r.stdout.strip().split("\n") or [""])[-1]
        check(f"T1 {f} vs {lst[:22]}: {last[len(E + f) + 2:] if last.startswith(E + f) else last[-60:]}", "CLEAN" in last and "hits=[]" in last, last[-80:])

print()
print("HK-4 LANDING CHECKS: " + ("ALL PASS" if not fails else f"{len(fails)} FAILED: " + "; ".join(fails)))
sys.exit(0 if not fails else 1)
