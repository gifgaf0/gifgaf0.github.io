#!/usr/bin/env python3
"""Step 2c: the corrected version (v2) of the alpha-decay paper, from the project-store text, with the five §2.93.B4
corrections (phase_b/B4/B4_RESULT.md, "Corrections the author may want in the deposit") and the author's F3/F5 facts.

Plain-language summary: this rewrites the paper's claims so that it reports one robust break (at Z = 88) instead of two,
fixes the step count (51, not 74), and removes the two sections that leaned on the now-closed framework, together with
the citations that did not support them. The data, the Q-values and Table 1 are unchanged.

Input : ../../../phase_b/B4/source/alpha_decay_three_regime_paper.md (md5 770ac497…, the store copy, "Draft — May 2026").
        check_fixed_n.json (this directory: the fixed-N numbers, re-computed independently of B4 and checked against it).
Output: alpha_decay_isotone_steps_v2_DRAFT.md (text of record), v1_to_v2.diff, and, with --pdf,
        alpha_decay_isotone_steps_v2_DRAFT.pdf (pandoc + XeLaTeX, DejaVu Serif). Figure 1 is not in the store, so the PDF
        carries its caption and a placeholder; the figure is unchanged from version 1 except for its caption.
Every replacement is anchored and must match exactly once.
"""
import difflib
import hashlib
import json
import os
import subprocess
import sys
from decimal import Decimal, ROUND_HALF_UP

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "../../../phase_b/B4/source/alpha_decay_three_regime_paper.md")
SRC_MD5 = "770ac49755f559841e0e6d7c9b083f1b"
OUT = os.path.join(HERE, "alpha_decay_isotone_steps_v2_DRAFT.md")
DOI, DEPOSITED = "10.5281/zenodo.20448930", "May 29, 2026"          # the author's F3 (October 8, 2026)

s = open(SRC, encoding="utf-8").read()
assert hashlib.md5(s.encode("utf-8")).hexdigest() == SRC_MD5, "store copy md5 mismatch"
fx = json.load(open(os.path.join(HERE, "check_fixed_n.json"), encoding="utf-8"))
assert fx["steps_N_gt_128"] == 51 and fx["steps_all_N"] == 74 and fx["Q_values"] == 96


def r3(x):
    return str(Decimal(repr(x)).quantize(Decimal("0.001"), rounding=ROUND_HALF_UP))


def sgn(x):
    v = r3(x)
    return ("+" + v) if not v.startswith("-") else "−" + v[1:]


rows88 = "\n".join(f"| {n} | {r3(a)} | {r3(b)} | {sgn(b - a)} |" for n, a, b in fx["full"]["Z88"])
rows92 = "\n".join(f"| {n} | {r3(a)} | {r3(b)} | {sgn(b - a)} |" for n, a, b in fx["full"]["Z92"])
dmin = min(b - a for _, a, b in fx["full"]["Z88"]); dmax = max(b - a for _, a, b in fx["full"]["Z88"])
assert (r3(dmin), r3(dmax)) == ("0.090", "0.465")
NR = fx["full"]["N_by_regime"]
assert (NR["I"][0], NR["I"][-1], NR["II"][0], NR["II"][-1], NR["III"][0], NR["III"][-1]) == (130, 136, 130, 146, 134, 156)
thu = dict((n, d) for n, d in fx["ThU_drift"])
assert (r3(thu[136]), r3(thu[146])) == ("0.347", "0.937")

E = []      # (label, old, new)

E.append(("title", "# Three-Regime Structure in α-Decay Q-Value Isotone Steps  \n## in the Deformed Actinide Region",
          "# Isotone Steps of α-Decay Q-Values in the Deformed Actinide Region:  \n## A Robust Break at Radium (Z = 88)"))
E.append(("byline", "**M. Gifford** *(independent)*  \nDraft — May 2026",
          "**Matthew Gifford** *(independent researcher, Hollister, CA)*  \n"
          f"Version 2 — October 2026. Corrects version 1 (Zenodo, {DEPOSITED}, doi:{DOI}); see the note at the end."))

ABS_OLD = s[s.index("We report a three-regime structure"):s.index("a testable structural signature.") + len("a testable structural signature.")]
ABS_NEW = (
    "We report the behavior of the isotone step in alpha-decay Q-values,\n"
    "ΔQ(Z,N) = Q_α(Z+2,N) − Q_α(Z,N), across the deformed actinide region\n"
    "(N > 128). Using 51 isotone steps derived from 96 Q-values in the\n"
    "AME2020 atomic mass evaluation, we find one robust break, at Z = 88 (Ra).\n"
    "Grouped by proton number, the steps have means of 0.308 ± 0.059 MeV\n"
    "(Z = 84–88), 0.599 ± 0.179 MeV (Z = 88–92) and 1.007 ± 0.302 MeV\n"
    "(Z ≥ 92), and the pooled groups differ significantly (Welch t > 5.5).\n"
    "Pooling, however, mixes neutron numbers. Compared at fixed neutron\n"
    f"number, the step across Z = 88 rises at every shared N, by {r3(dmin)} to\n"
    f"{r3(dmax)} MeV, which coincides with the onset of permanent octupole\n"
    "deformation near Ra. The apparent second break at Z = 92 does not survive\n"
    "the same comparison: at fixed N it changes sign, and it is smaller than\n"
    "the drift of a single boundary's step with N. It reflects the different\n"
    "neutron coverage of the groups, and we do not claim it. N = 126\n"
    "shell-closure effects are excluded by the N > 128 restriction.")
E.append(("abstract", ABS_OLD, ABS_NEW))

INTRO_OLD = s[s.index("Z = 84–100) using the AME2020 atomic mass evaluation [7]. We find that"):
              s.index("examine against the existing dataset.") + len("examine against the existing dataset.")]
INTRO_NEW = (
    "Z = 84–100) using the AME2020 atomic mass evaluation [7]. Grouped by\n"
    "proton number, the 51 available steps fall into three groups with\n"
    "well-separated means. Compared at fixed neutron number, only the\n"
    "boundary at Z = 88 holds, and it coincides with the documented onset of\n"
    "octupole deformation near Ra. The apparent boundary at Z = 92 reflects\n"
    "the different neutron coverage of the groups.")
E.append(("introduction", INTRO_OLD, INTRO_NEW))

E.append(("§2 step count", "This\nyields 74 isotone step measurements.",
          "This\nyields 51 isotone step measurements (74 over all N)."))
E.append(("§2 fixed-N method", "n. Regime separation is assessed by Welch's two-sample t-test.",
          "n. Regime separation is assessed by Welch's two-sample t-test. Because\n"
          "the groups cover different ranges of N, each boundary is also tested by\n"
          "comparing the steps on either side of it at the same N (Section 3.3)."))
E.append(("§3.1 heading", "### 3.1 Three-Regime Structure", "### 3.1 Grouping by Proton Number"))
E.append(("§3.1 sentence", "with regime mean lines and boundaries indicated. The three-regime\nstructure is visually immediate.",
          "with regime mean lines and boundaries indicated. The grouping by Z is\n"
          "visually clear; Section 3.3 tests which of its boundaries survive at\nfixed N."))
E.append(("§3.2 close", "Both transitions are highly statistically significant. The regime\n"
          "structure is not an artifact of small sample size.",
          "Both pooled differences are statistically significant, so the grouping\n"
          "is not an artifact of small sample size. Pooling, however, mixes\n"
          "neutron numbers; Section 3.3 separates the two."))

S33_OLD = s[s.index("### 3.3 N-Dependence Within Regimes"):s.index("### 3.4 Exclusion of Shell-Closure Contamination")]
S33_NEW = (
    "### 3.3 Boundaries at Fixed Neutron Number\n\n"
    "Within the full dataset (N = 130 to 156), the mean ΔQ per isotone step\n"
    "increases with neutron number, with the steepest rise at N ≈ 138–140\n"
    "(the Ra-226 / Th-230 region). The groups also cover different N ranges:\n"
    f"Regime I has N = {NR['I'][0]}–{NR['I'][-1]}, Regime II has N = {NR['II'][0]}–{NR['II'][-1]}, "
    f"and Regime III has\nN = {NR['III'][0]}–{NR['III'][-1]}. A difference between pooled "
    "group means can therefore\nreflect N as well as Z. Table 2 compares the steps on either side of each\n"
    "boundary at the same N.\n\n"
    "**Table 2.** Isotone steps on either side of a boundary at equal N (MeV;\n"
    "differences computed before rounding).\n\n"
    "| N | Rn→Ra | Ra→Th | Across Z = 88 |\n|---|-------|-------|---------------|\n" + rows88 + "\n\n"
    "| N | Th→U | U→Pu | Across Z = 92 |\n|---|------|------|---------------|\n" + rows92 + "\n\n"
    "Across Z = 88 the step rises at every shared N. Across Z = 92 the\n"
    "difference changes sign (negative at N = 134, positive at N = 138–146) and\n"
    "falls toward zero at higher N. It is also smaller than the drift of the\n"
    f"Th→U step itself, which rises from {r3(thu[136])[:-1]} MeV at N = 136 to {r3(thu[146])[:-1]} MeV at\n"
    "N = 146. We therefore claim one robust break, at Z = 88. A claim of a\n"
    "break at Z = 92 would need a pre-registered test with controlled N\n"
    "coverage.\n\n")
E.append(("§3.3", S33_OLD, S33_NEW))

S42_OLD = s[s.index("### 4.2 Z = 92 Boundary: Structural Change in the U Region"):s.index("### 4.3 What the Three-Regime Structure Reflects")]
S42_NEW = (
    "### 4.2 Z = 92: Not Supported at Fixed N\n\n"
    "The pooled means also change at Z = 92 (U). Empirical subdivision of the\n"
    "actinide region at approximately Z = 89–92 has also been employed for\n"
    "phenomenological Geiger-Nuttall fitting, where a single power-law\n"
    "relationship for the actinides requires separate fitting parameters in\n"
    "the Z < 92 and Z > 92 regions [9]. In the present data, however, the\n"
    "Z = 92 boundary does not survive the fixed-N comparison of Section 3.3:\n"
    "the difference across it changes sign and is smaller than the drift with\n"
    "N within a single boundary. We therefore do not claim a structural\n"
    "transition at Z = 92.\n\n")
E.append(("§4.2", S42_OLD, S42_NEW))

E.append(("§4.3 heading", "### 4.3 What the Three-Regime Structure Reflects", "### 4.3 What the Grouping Reflects"))
E.append(("§4.3 Regime III", "Regime III (Z ≥ 92) covers\nthe well-deformed actinides beyond the Z = 92 structural change, where\n"
          "the Q-value gradient with Z is largest and most consistent with\nsystematic Coulomb driving.",
          "Regime III (Z ≥ 92) covers\nthe well-deformed actinides, where the Q-value gradient with Z is largest\n"
          "and most consistent with systematic Coulomb driving; its higher mean also\n"
          "reflects its wider and higher range of N (Section 3.3)."))
E.append(("§4.4", "We discuss\nthe boundary locations in Section 4.5 below.",
          "The III/II\nratio compares groups with different N coverage (Section 3.3)."))

DROP = s[s.index("### 4.5 A Structural Account of the Boundary Locations"):s.index("### 4.7 Limitations")]
E.append(("drop §4.5–§4.6", DROP, ""))
E.append(("§4.7 → §4.5", "### 4.7 Limitations", "### 4.5 Limitations"))

NC_OLD = s[s.index("**N-correlation.**"):s.index("**Exclusion of odd-Z isotones.**")]
NC_NEW = (
    "**N-correlation.** The available isotone chains are not uniformly\n"
    "distributed in N across regimes (Section 3.3). The fixed-N comparison\n"
    "shows that this accounts for the apparent Z = 92 boundary, while the\n"
    "Z = 88 boundary holds at every shared N. A fully controlled comparison\n"
    "would require equal N coverage across regimes, not yet available from\n"
    "AME2020.\n\n")
E.append(("§4.7 N-correlation", NC_OLD, NC_NEW))

CON_OLD = s[s.index("The isotone step ΔQ(Z,N) = Q_α(Z+2,N) − Q_α(Z,N) in the deformed\nactinide region (N > 128) exhibits"):
            s.index("the Curium test.") + len("the Curium test.")]
CON_NEW = (
    "The isotone step ΔQ(Z,N) = Q_α(Z+2,N) − Q_α(Z,N) in the deformed\n"
    "actinide region (N > 128) shows one robust break, at Z = 88, over 51\n"
    "steps from AME2020. Grouped by Z, the steps form three groups whose pooled\n"
    "means differ significantly (t > 5.5), but compared at fixed N only the\n"
    "Z = 88 boundary holds: the step across it rises at every shared N. It\n"
    "coincides with the documented onset of octupole deformation at Ra. The\n"
    "apparent boundary at Z = 92 reflects the groups' different N coverage and\n"
    "is not claimed.\n\n"
    "This analysis is the first, to our knowledge, to characterize the\n"
    "isotone Q-value step as a primary observable across the deformed\n"
    "actinide series. The N > 128 restriction is essential: shell-closure\n"
    "effects at N = 126 would mask the structure entirely.\n\n"
    "Improved mass measurements for neutron-rich Po and Rn isotopes would\n"
    "sharpen the Regime I statistics, and wider N coverage would allow a\n"
    "controlled test at Z = 92.\n\n"
    "**Note on version 2.** Version 1 was deposited on Zenodo on " + DEPOSITED + " (doi:" + DOI + ").\n"
    "This version corrects it:\n"
    "(1) the N > 128 step count is 51, not 74 (74 counts all N);\n"
    "(2) only the Z = 88 break is claimed, and the Z = 92 boundary is shown not\n"
    "to survive a fixed-N comparison (Section 3.3, Table 2);\n"
    "(3) the former Sections 4.5–4.6 are removed: a structural account drawn\n"
    "from a separate framework, and the Curium prediction it motivated, which\n"
    "the data did not confirm. The reference cited for that account did not\n"
    "contain it;\n"
    "(4) an incomplete citation, and the sentence that relied on it, are\n"
    "removed;\n"
    "(5) the abstract's statement that half of the Curium prediction was\n"
    "confirmed is removed with it, since that step showed no significant\n"
    "elevation (t = +0.4).\n"
    "The data, the Q-values and Table 1 are unchanged.")
E.append(("conclusions + version note", CON_OLD, CON_NEW))

REF_OLD = s[s.index("[9] Andreyev, A.N. et al. (2020)."):s.index("---\n\n*Figure caption:*")]
REF_NEW = "[9] Akrawy, D.T. (2020). Z. Naturforsch. A 75, 1031.\n\n"
E.append(("references", REF_OLD, REF_NEW))
E.append(("figure caption", "Shaded regions and colors\nidentify the three regimes. Dashed vertical lines mark the regime\n"
          "boundaries at Z = 88 (Ra) and Z = 92 (U).",
          "Shaded regions and colors\nidentify the three groups. Dashed vertical lines mark the group\n"
          "boundaries at Z = 88 (Ra) and Z = 92 (U); only the first survives the\n"
          "fixed-N comparison of Section 3.3."))
NOTES_OLD = s[s.index("\n---\n\n*Draft notes for revision:*"):]
E.append(("drop draft notes", NOTES_OLD, "\n"))

out = s
for label, old, new in E:
    assert old and s.count(old) == 1, (label, s.count(old))
    assert out.count(old) == 1, label
    out = out.replace(old, new, 1)
    print("edit:", label)

# checks on the result
assert "74 isotone steps" not in out and "across 74 steps" not in out and "74 available" not in out
assert "Citation pending" not in out and "[11]" not in out and "[10]" not in out and "Andreyev" not in out
assert "terminus toward which all actinide chains converge" not in out and "No parameter is adjusted" not in out
assert "J(θ)" not in out and "Curium" not in out.replace("Curium prediction it motivated", "").replace(
    "half of the Curium prediction", "")
assert "it is not driven by a correlation" not in out
assert out.count("[9]") == 2 and "[8]" in out           # cited once in §4.2, listed once
assert "### 4.6" not in out and "### 4.7" not in out
open(OUT, "w", encoding="utf-8", newline="\n").write(out)
diff = difflib.unified_diff(s.splitlines(True), out.splitlines(True), "v1_store_copy.md", "v2_DRAFT.md")
open(os.path.join(HERE, "v1_to_v2.diff"), "w", encoding="utf-8").writelines(diff)
print("wrote", OUT, "md5", hashlib.md5(out.encode("utf-8")).hexdigest(), "bytes", len(out.encode("utf-8")))

if "--pdf" in sys.argv:
    t = out
    t = t.replace("# Isotone Steps of α-Decay Q-Values in the Deformed Actinide Region:  \n## A Robust Break at Radium (Z = 88)\n", "", 1)
    a0 = t.index("**Matthew Gifford**")
    a1 = t.index("\n---\n", a0)
    t = t[:a0] + t[a1 + len("\n---\n"):]
    t = t.replace("\n---\n", "\n")
    t = t.replace(":\n- Difference in means", ":\n\n- Difference in means")      # pandoc needs a blank line before a list
    t = t.replace("*Figure caption:* **Figure 1.**", "**[Figure 1: unchanged from version 1; insert fig1_regime_structure.pdf.]**\n\n**Figure 1.**", 1)
    meta = ("---\ntitle: |\n  Isotone Steps of α-Decay Q-Values in the Deformed Actinide Region: A Robust Break at Radium (Z\u00a0=\u00a088)\n"
            "author: |\n  Matthew Gifford, independent researcher, Hollister, CA\n"
            f"date: |\n  Version 2, October 2026 (corrects version 1, Zenodo, {DEPOSITED}, doi:{DOI})\n---\n\n")
    md = os.path.join(HERE, "_typeset_v2.md")
    open(md, "w", encoding="utf-8").write(meta + t)
    hdr = os.path.join(HERE, "_header_v2.tex")
    open(hdr, "w").write("\\usepackage[a4paper,margin=25mm]{geometry}\n\\usepackage{microtype}\n"
                         "\\usepackage[hidelinks]{hyperref}\n\\AtBeginEnvironment{longtable}{\\small}\n")
    pdf = OUT.replace(".md", ".pdf")
    subprocess.run(["pandoc", md, "-f", "markdown-implicit_figures", "-s", "-o", pdf, "--pdf-engine=xelatex", "-H", hdr,
                    "-V", "fontsize=11pt", "-V", "fontfamily=fontspec", "-V", "mainfont=DejaVu Serif", "-V", "monofont=DejaVu Sans Mono",
                    "-V", "linestretch=1.08"], check=True)
    os.remove(md); os.remove(hdr)
    print("wrote", pdf)
