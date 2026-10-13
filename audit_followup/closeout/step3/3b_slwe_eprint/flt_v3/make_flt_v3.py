#!/usr/bin/env python3
"""make_flt_v3.py — FLT version 3 for upload: the version 2 text with the editorial suggestions taken out and the
October 2026 notice added (text from FLT_V3_NOTICE_DRAFT.md, with the SLWE note's all-versions DOI filled in).

Input:  FLT_v2_source.md (the author's upload of October 13, 2026, of the version 2 text; md5 bea51f5a…).
Output: FLT_v3.md.
Every removal and insertion is an exact, unique match; putting them back gives the input byte for byte.
"""
import hashlib
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC, OUT = os.path.join(HERE, "FLT_v2_source.md"), os.path.join(HERE, "FLT_v3.md")
SRC_MD5 = "bea51f5a512cb029ff9d0549716826fa"
s = open(SRC, encoding="utf-8").read()
assert hashlib.md5(s.encode()).hexdigest() == SRC_MD5

NOTICE = ("> **Notice (October 2026).** The cryptographic scheme in Section IV, Sedenion Module-LWE, is insecure at both "
          "parameter sets this paper published: version 1 (n = 512, q ≈ 2³²) and version 2 (k = 64, q = 911). Its "
          "Singer-orbit public matrix has rank at most 76 at every module rank. So the public key can be told apart from "
          "random, and recovering the noise reduces to a 76-dimensional problem. Replacing the matrix with a uniform one "
          "does not restore the claimed security either: version 1's parameters reach only about 2⁵¹ operations with "
          "weight-64 secrets and 2⁵³ with dense ones, and version 2's about 2¹⁶⁷, some 95 bits below the 2²⁶² that the "
          "same estimator gives ML-KEM-1024, a Category 5 standard. The NIST Category 5 claims in both versions are "
          "withdrawn. Details: M. Gifford, \"A rank collapse in a sedenion Module-LWE proposal, and why a uniform matrix "
          "does not repair it\", Zenodo, 2026, doi:10.5281/zenodo.23270248.")

H = [  # (label, old, new)
    ("version line", "**Version 2** (corrected) — May 2026",
     "**Version 3** — October 2026: the version 2 text (corrected, May 2026) with the notice below"),
    ("suggested title -> notice",
     "> *Suggested alternative title, more aligned with the corrected claims:*\n"
     "> *\"Sedenion Module-LWE and a Geometric Conjecture for the Proton Radius.\" Author's call; not load-bearing.*",
     NOTICE),
    ("author-to-supply 1", " **[AUTHOR TO SUPPLY: the exact convention.]**", ""),
    ("author-to-supply 2", " **[AUTHOR TO SUPPLY: the explicit map and any base constant, with prior addresses.]**", ""),
    ("author-to-supply 3", " **[AUTHOR TO SUPPLY: reconcile, or remove the unused constants.]**", ""),
    ("author-to-supply 4", " **[AUTHOR TO SUPPLY: explicit constraint count, or retain as heuristic.]**", ""),
    ("open note on 5 and 13",
     " *(Open: the roles of the factors 5 and 13, which do not correspond to element orders in PSL(2,7), should be "
     "justified or the condition tightened.)*", ""),
]

out = s
for lab, old, new in H:
    assert s.count(old) == 1 and out.count(old) == 1, lab
    out = out.replace(old, new, 1)
# reverse: the empty removals are put back at their recorded offsets, the replacements by text
rev = out
for lab, old, new in reversed(H):
    if new:
        assert rev.count(new) == 1, lab
        rev = rev.replace(new, old, 1)
# put each removed piece back after the 40 characters that preceded it in the input
t = rev
for lab, old, new in H:
    if not new:
        anchor_before = s[s.index(old) - 40:s.index(old)]      # the 40 characters before each removed piece
        assert t.count(anchor_before) == 1, lab
        k = t.index(anchor_before) + len(anchor_before)
        t = t[:k] + old + t[k:]
assert t == s, "REVERSE CHECK FAILED"
for marker in ("AUTHOR TO SUPPLY", "Suggested alternative title", "(Open: the roles"):
    assert marker not in out
open(OUT, "w", encoding="utf-8").write(out)
print(f"{os.path.basename(OUT)}: {len(s.encode())} -> {len(out.encode())} bytes | md5 {hashlib.md5(out.encode()).hexdigest()} | "
      f"{len(H)} edits | reverse check PASS")
