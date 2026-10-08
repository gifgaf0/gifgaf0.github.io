#!/usr/bin/env python3
"""Step 4a: Paper VII and the two store calculators, archived at V4.97. Drafts; nothing deployed or deposited.

Plain-language summary: this starts from the Phase B drafts (B3), which already carry the October corrections, and
makes four changes the brief asks for:
  (1) the corrections are marked applied, not "DRAFT, not adopted";
  (2) Paper VII's §10 (gravitational waves crossing a conformal boundary) is removed, leaving a short note in its place
      so the section numbers and later cross-references still make sense;
  (3) "Theorem 1" is renamed "Fit 1", since the mass relation is a leading-order fit with named inputs;
  (4) each file gets an "Archived at V4.97" header; each calculator also gets a visible banner line at the top.
Every replacement is anchored and counted; the result must contain no "Theorem 1" and no "DRAFT" label.
"""
import hashlib, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
B3 = os.path.join(HERE, "../../../phase_b/B3")
SRC = {"paper": (os.path.join(B3, "paper_vii/sqt_paper_VII_oct2026_DRAFT.md"), "ccecfded6a3be4f5d04e2f25de92a649"),
       "v21": (os.path.join(B3, "store/SQTCalculator_v2_1_DRAFT.jsx"), "abad7f3db8d7dbf148dfc6962700c7bc"),
       "v191": (os.path.join(B3, "store/sqt_v19_1_DRAFT.jsx"), "c3dc019f8a95cee6aea8562014c68a94")}
OUT = {"paper": "sqt_paper_VII_ARCHIVED_V4_97.md", "v21": "SQTCalculator_v2_1_ARCHIVED_V4_97.jsx",
       "v191": "sqt_v19_1_ARCHIVED_V4_97.jsx"}
txt = {}
for k, (p, m) in SRC.items():
    t = open(p, encoding="utf-8").read()
    assert hashlib.md5(t.encode()).hexdigest() == m, k
    txt[k] = t


def once(k, old, new, label):
    assert txt[k].count(old) == 1, (k, label, txt[k].count(old))
    txt[k] = txt[k].replace(old, new, 1)
    print(f"[{k}] {label}")


def rename_theorem1(k):
    KEEP = ("(formerly Theorem 1)", "formerly called \"Theorem 1\"")
    for i, kp in enumerate(KEEP):
        txt[k] = txt[k].replace(kp, f"@@KEEP{i}@@")
    n0 = len(re.findall(r"Theorem 1(?!\d)", txt[k])) + len(re.findall(r"THEOREM 1(?!\d)", txt[k]))
    txt[k] = re.sub(r"Theorem 1(?!\d)", "Fit 1", txt[k])
    txt[k] = re.sub(r"THEOREM 1(?!\d)", "FIT 1", txt[k])
    assert not re.search(r"Theorem 1(?!\d)|THEOREM 1(?!\d)", txt[k])
    for i, kp in enumerate(KEEP):
        txt[k] = txt[k].replace(f"@@KEEP{i}@@", kp)
    print(f"[{k}] renamed Theorem 1 → Fit 1: {n0} occurrences")
    return n0


# ---------------------------------------------------------------- Paper VII
P = "paper"
HEADER = (
    "> **Archived at V4.97 (October 8, 2026).** The research program this paper belongs to, Superfluid Quantum\n"
    "> Topology, was closed on October 7, 2026 (Master Ledger V4.97, §2.97). This archived version is kept as a\n"
    "> record; nothing in it is a current claim. Three changes from the October draft:\n"
    "> - the October 2026 corrections are applied (the status note below);\n"
    "> - the mass relation formerly called \"Theorem 1\" is named **Fit 1**, because it is a leading-order fit with\n"
    ">   named inputs, not a theorem;\n"
    "> - the former §10 (gravitational waves crossing a conformal boundary) is removed, because the program's vacuum has\n"
    ">   no carrier for gravitational waves (ledger §2.92.A).\n\n")
once(P, "## A Topological Dictionary of the Particle Spectrum\n\n", "## A Topological Dictionary of the Particle Spectrum\n\n" + HEADER,
     "archived header")
once(P, "*October 2026 audit corrections: DRAFT — see the status note below.*",
     "*October 2026 audit corrections: applied — see the status note below.*", "corrections marked applied (1)")
once(P, "> **Status note — October 2026 audit corrections (DRAFT, not adopted).**",
     "> **Status note — October 2026 audit corrections (applied in this archived version).**",
     "corrections marked applied (2)")
once(P, "> This draft corrects the claims below.", "> This version corrects the claims below.", "corrections marked applied (3)")
s10a = txt[P].index("# SQT Paper VII — Draft Section\n## §10  Theorem 5 (Candidate): Cosmological Echoes and Gravity Filtration")
s10b = txt[P].index("# SQT Paper VII — Draft Section\n## Chapter V — S-Matrix Dissipation")
removed = txt[P][s10a:s10b]
assert removed.count("\n## ") == 1 and "### §10.5" in removed and "Chapter V" not in removed.split("*End of §10 draft.*")[0]
STUB = (
    "# SQT Paper VII — Draft Section\n"
    "## §10  Removed at V4.97 (formerly Theorem 5 (Candidate): Cosmological Echoes and Gravity Filtration)\n\n"
    "The former §10 described gravitational waves crossing a conformal boundary between aeons, attenuated by a\n"
    "filtration constant $\\kappa/4$, with a qualitative link to CMB ring anomalies. The program's vacuum has no carrier\n"
    "for gravitational waves: its transverse channel is pure vector, and GW170817 prefers tensor over vector\n"
    "polarization (Master Ledger §2.92.A). The section is removed. Later mentions of §10, $F_g$, $T_g$, OP.9 and OP.10\n"
    "refer to the removed text.\n\n---\n\n")
txt[P] = txt[P][:s10a] + STUB + txt[P][s10b:]
print(f"[paper] §10 removed ({len(removed)} chars) and replaced by a note")
once(P, "Theorems 1, 3, and §10", "Fit 1, Theorem 3 and the former §10", "special case: Theorems 1, 3")
once(P, "in Theorems 1 and 2.", "in Fit 1 and Theorem 2.", "special case: Theorems 1 and 2")
once(P, "Papers I–VI establish Theorems 1–3, the mass operator,", "Papers I–VI establish Fit 1 (formerly Theorem 1) and Theorems 2–3, the mass operator,", "special case: Theorems 1–3")
n_paper = rename_theorem1(P)

# ---------------------------------------------------------------- SQTCalculator v2.1
K = "v21"
JSX_HEAD = ("// ═══════════════════════════════════════════════════════════════\n"
            "//  ARCHIVED AT V4.97 (October 8, 2026). The research program this calculator belonged to (Superfluid\n"
            "//  Quantum Topology) was closed on October 7, 2026 (Master Ledger V4.97, §2.97). Kept as a record:\n"
            "//  a leading-order fit with named inputs, not a derivation.\n")
once(K, "import { useState } from \"react\";\n\n", "import { useState } from \"react\";\n\n" + JSX_HEAD, "archived header comment")
once(K, "//  v2.1 DRAFT (October 2026): status corrections per ledger §2.92; PDG 2024 values.",
     "//  v2.1 (October 2026): status corrections per ledger §2.92; PDG 2024 values. Archived at V4.97.", "label (comment)")
once(K, "          v2.1 DRAFT (October 2026): status corrections per ledger §2.92.",
     "          v2.1 (October 2026): status corrections per ledger §2.92. Archived at V4.97.", "label (footer)")
BAN = ("Archived at V4.97: a leading-order fit with named inputs; the program it belonged to is closed (Master Ledger §2.97).")
once(K, "        {/* Header */}\n        <div style={{ marginBottom: 24 }}>",
     "        {/* Archived banner */}\n"
     "        <div role=\"note\" style={{ background: \"#2a2410\", color: \"#f3e3a6\", border: \"1px solid #5a4a1a\", borderRadius: 4,"
     " padding: \"8px 12px\", fontSize: 12, marginBottom: 16 }}>\n          " + BAN + "\n        </div>\n\n"
     "        {/* Header */}\n        <div style={{ marginBottom: 24 }}>", "visible banner")
assert not re.search(r"Theorem 1(?!\d)", txt[K])

# ---------------------------------------------------------------- sqt v1.9.1
K = "v191"
once(K, "import { useState, useEffect } from \"react\";\n\n", "import { useState, useEffect } from \"react\";\n\n" + JSX_HEAD,
     "archived header comment")
once(K, "//  SQT v1.9.1 DRAFT (October 2026) · CONSTANTS:", "//  SQT v1.9.1 (October 2026; archived at V4.97) · CONSTANTS:",
     "label (comment)")
once(K, "SQT · v1.9.1 DRAFT · Matthew Gifford", "SQT · v1.9.1 (archived at V4.97) · Matthew Gifford", "label (header)")
once(K, "SQT v1.9.1 DRAFT (October 2026 status corrections) ·", "SQT v1.9.1 (October 2026 status corrections; archived at V4.97) ·",
     "label (footer)")
i_h1 = txt[K].index("        <h1 style={{ margin:\"0 0 4px\", fontSize:20, fontWeight:400, letterSpacing:-0.3 }}>")
line_start = txt[K].rfind("\n", 0, txt[K].rfind("SQT · v1.9.1 (archived at V4.97)", 0, i_h1))
ban_jsx = ("\n          <div role=\"note\" style={{ background:\"#2a2410\", color:\"#f3e3a6\", border:\"1px solid #5a4a1a\","
           " borderRadius:4, padding:\"8px 12px\", fontSize:12, margin:\"0 0 12px\" }}>" + BAN + "</div>")
# the banner goes just before the line that carries the version label (inside the same header block)
txt[K] = txt[K][:line_start] + ban_jsx + txt[K][line_start:]
print("[v191] visible banner")
n_v191 = rename_theorem1(K)

for k in txt:
    assert "DRAFT" not in txt[k], (k, [m.start() for m in re.finditer("DRAFT", txt[k])][:3])
    open(os.path.join(HERE, OUT[k]), "w", encoding="utf-8").write(txt[k])
    b = txt[k].encode()
    print(OUT[k], hashlib.md5(b).hexdigest(), len(b))
print("Theorem 1 renamed:", {"paper": n_paper, "v191": n_v191})
