#!/usr/bin/env python3
"""edit_v6_4_final_pass.py — the author's final pass on the gauge paper's v6.4 (October 13, 2026).

Input:  Gifford_Csaszar_Gauge_Group_v6_4_2026_CLOSEOUT_DRAFT.md (md5 87278ffc…, the close-out draft).
Output: Gifford_Csaszar_Gauge_Group_v6_4_2026_FINAL.md (same directory as this script).

Only errors are fixed; no conclusion, number or reference entry changes. Hunks:
  P1  Section 6: subsections renumbered 6.1–6.3 (no Section 6.2 has existed since v5);
  P2  Section 5: a stray "(a)" with no "(b)", left when the sign dressing was withdrawn;
  P3  Sections 6.1 and 9: the |V_cb| comparison value 0.0408 ± 0.0014 is PDG 2022's, so it is labelled so;
  P4  Section 7.5 and Open Problem (i): a straight edge has no Frenet–Serret frame (zero curvature), so the frame is an
      adapted orthonormal frame with a chosen normal; T, N, B are vectors, so "four real quantities" loses "real";
  P5  Sections 7 and 12: the rank-4 problem is "addressed", as the abstract says, not "resolved", since the
      tensor-product realization is Open Problem (i);
  P6  Sections 6.1, 9 and 12: 3/13 and its integers are combinatorial, not topological, invariants (the rank of ∂₂ is
      the face count minus one, so it depends on the triangulation);
  P7  eleven run-in bold labels whose closing ** followed a space, which Markdown does not close;
  P8  Section 2: Heawood (1890) and Ringel & Youngs (1968) cited for the Heawood bound (the latter was listed, uncited);
  P9  abstract, Sections 7.3 and 9: the centralizer theorem stated for the Lie algebras, where it is proved (the
      centralizer of the group SU(3) in G₂ is its center ℤ₃, which is finite but not trivial);
  P10 Section 7.1: the conformal structure of a torus is fixed by its geometry, not its topology;
  P11 Section 7.2: the symbol W is defined;
  P12 the v6.4 revision note gains item (ix), listing P1–P6 and P8–P11 in plain terms.
Checks: every anchor is unique in the input and every replacement unique in the output; undoing the hunks in reverse
gives the close-out draft byte for byte; the targeted statements are gone; the references still run 1–27; every
reference is cited in the main text.
"""
import hashlib
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "Gifford_Csaszar_Gauge_Group_v6_4_2026_CLOSEOUT_DRAFT.md")
OUT = os.path.join(HERE, "Gifford_Csaszar_Gauge_Group_v6_4_2026_FINAL.md")
SRC_MD5 = "87278ffcd8d19fccab3ff97971c4ddce"

s = open(SRC, encoding="utf-8").read()
assert hashlib.md5(s.encode("utf-8")).hexdigest() == SRC_MD5, "close-out draft md5 mismatch"

H = []   # (label, old, new)

# P1 Section 6 numbering
H.append(("P1a", "## **6.3 The Complex Structure Asymmetry**", "## **6.2 The Complex Structure Asymmetry**"))
H.append(("P1b", "## **6.4 Open CKM Elements**", "## **6.3 Open CKM Elements**"))

# P2 Section 5
H.append(("P2", "is therefore confined to (a) the identification", "is therefore confined to the identification"))

# P3 PDG 2022 label for |V_cb|
H.append(("P3a", "reproduces the PDG value 0.0408 ± 0.0014 to 0.7%", "reproduces the PDG 2022 value 0.0408 ± 0.0014 to 0.7%"))
H.append(("P3b", "= 0.04108, within 0.7% of PDG. The golden ratio", "= 0.04108, within 0.7% of PDG 2022. The golden ratio"))

# P4 edge frames
H.append(("P4a",
          "Each edge e possesses a Frenet-Serret frame: a unit tangent T, principal normal N, and binormal B = T × N, "
          "together with a scalar density (the edge length or a local metric coefficient). These four real quantities "
          "(T, N, B, scalar) are assigned",
          "Each edge e carries an adapted orthonormal frame: the unit tangent T, a chosen unit normal N, and the binormal "
          "B = T × N, together with a scalar density (the edge length or a local metric coefficient). These four "
          "quantities (T, N, B, scalar) are assigned"))
H.append(("P4b",
          "(a) If SU(2) acts on the Frenet-framing fibre (the four real quantities (T, N, B, scalar) per edge)",
          "(a) If SU(2) acts on the edge-framing fibre (the four quantities (T, N, B, scalar) per edge)"))

# P5 "resolve" -> "address"
H.append(("P5a", "We resolve it by showing that SU(2) and U(1)", "We address it by showing that SU(2) and U(1)"))
H.append(("P5b", "The rank-4 problem is resolved by the observation", "The rank-4 problem is addressed by the observation"))

# P6 combinatorial, not topological, invariants
H.append(("P6a", "The ratio 3/13 is a topological invariant of the Császár triangulation",
          "The ratio 3/13 is a combinatorial invariant of the Császár triangulation"))
H.append(("P6b", "(determined by the homology of the torus)", "(fixed by the face count and the homology of the torus)"))
H.append(("P6c", "Both integers are topological invariants of the Császár triangulation",
          "Both integers are combinatorial invariants of the Császár triangulation"))
H.append(("P6d", "built from two topological invariants of the polyhedron",
          "built from two combinatorial invariants of the polyhedron"))

# P7 run-in bold labels
BOLD = ["Homological derivation of 13.", "Physical interpretation.", "Note (unresolved conjecture).",
        "Stratum 0 (vertices).", "Stratum 1 (edges).", "Identification with the weak SU(2) (conjecture).",
        "Stratum 2 (surface).", "Vertices (0-dimensional) → 𝕆 → SU(3).", "Edge framings (1-dimensional) → ℍ → SU(2).",
        "Surface complex structure (2-dimensional) → ℂ → U(1)."]
for k, lab in enumerate(BOLD, 1):
    H.append((f"P7.{k}", f"**{lab} **", f"**{lab}** "))
H.append(("P7.11", "**Conjecture 1 (Chiral Coupling). ***", "**Conjecture 1 (Chiral Coupling).** *"))

# P8 Heawood bound citations
H.append(("P8", "V = 7 (Heawood bound)", "V = 7 (the Heawood bound; Heawood 1890, Ringel & Youngs 1968)"))

# P9 centralizer at the Lie-algebra level
H.append(("P9a", "G₂ itself is a theorem: the centralizer of color SU(3) in G₂ is trivial",
          "G₂ itself is a theorem: the centralizer of color su(3) in g₂ is trivial"))
H.append(("P9b", "commuting weak factor: the centralizer of the color SU(3) in G₂ is trivial.",
          "commuting weak factor: the centralizer of the color su(3) in g₂ is trivial."))
H.append(("P9c", "is a theorem: the centralizer of the color SU(3) in G₂ is trivial, since",
          "is a theorem: the centralizer of the color su(3) in g₂ is trivial, since"))

# P10 conformal structure
H.append(("P10", "This conformal data is determined by the surface topology and",
          "This conformal data is determined by the surface geometry and"))

# P11 W defined
H.append(("P11", "from the algebraic side: der(W) ⊂ tri(W) acts identically",
          "from the algebraic side: for a normed division algebra W, der(W) ⊂ tri(W) acts identically"))

# P12 revision note, item (ix)
H.append(("P12", "and the reference list now runs 1–27.*",
          "and the reference list now runs 1–27. (ix) Smaller corrections, none of which changes a conclusion. Section 6's "
          "subsections are renumbered 6.1–6.3; there had been no Section 6.2 since v5. Sections 6.1, 9 and 12 call 3/13 "
          "and its two integers combinatorial rather than topological invariants of the triangulation: the rank of ∂₂ "
          "is the number of faces minus one, so it depends on the triangulation. Sections 6.1 and 9 identify the "
          "|V_cb| comparison value, 0.0408 ± 0.0014, as PDG 2022's. The abstract and Sections 7.3 and 9 state the "
          "centralizer theorem for the Lie algebras, where it is proved: the centralizer of su(3) in g₂ is trivial. "
          "The centralizer of the group SU(3) in G₂ is its center ℤ₃, which is finite, so the conclusion that no weak "
          "factor inside G₂ commutes with color stands. Section 7.5 and Open Problem (i): a straight edge has no "
          "Frenet–Serret frame, since its curvature vanishes, so each edge carries an adapted orthonormal frame with a "
          "chosen normal. Section 7.1: the conformal structure of a torus is fixed by its geometry, not by its "
          "topology. Sections 7 and 12 say, as the abstract does, that the rank-4 problem is addressed rather than "
          "resolved, since the tensor-product realization is Open Problem (i). Section 2 cites Heawood (1890) and "
          "Ringel & Youngs (1968) for the Heawood bound; the latter had been listed but not cited. Section 7.2 says "
          "what W denotes, and a stray \"(a)\" is removed from Section 5.*"))

out = s
for lab, old, new in H:
    assert s.count(old) == 1, ("anchor not unique in the input", lab, s.count(old))
    assert out.count(old) == 1, ("anchor disturbed by an earlier hunk", lab)
    out = out.replace(old, new, 1)
for lab, _, new in H:
    assert out.count(new) == 1, ("replacement not unique in the output", lab, out.count(new))

# reverse splice
rev = out
for lab, old, new in reversed(H):
    rev = rev.replace(new, old, 1)
assert rev == s and hashlib.md5(rev.encode("utf-8")).hexdigest() == SRC_MD5, "REVERSE SPLICE FAILED"

# structural checks
ref_at = out.index("# **References**")
main = out[out.index("# **Abstract**"):ref_at]
heads6 = re.findall(r"^## \*\*(6\.\d) ", out, flags=re.M)
assert heads6 == ["6.1", "6.2", "6.3"], heads6
assert not re.search(r"^\*\*[^*\n]*\s\*\*", out, flags=re.M), "a run-in bold label still closes after a space"
assert "topological invariant" not in out.replace("rather than topological invariants of the triangulation", "")
assert "Frenet" not in main and out.count("Frenet") == 1                       # only in item (ix)
assert len(re.findall(r"centralizer of (the )?color SU\(3\) in G₂ is trivial", out)) == 1   # the v6 note only
assert "resolve it" not in out and "is resolved by" not in out
assert "PDG 2022 value 0.0408" in main and "within 0.7% of PDG 2022." in main
assert "Ringel & Youngs 1968" in main and "Heawood 1890" in main
assert "(a) the identification" not in out
assert re.search(r"normed division algebra W, der\(W\)", main)
refs = out[ref_at:]
nums = [int(m) for m in re.findall(r"^\[(\d+)\] ", refs, flags=re.M)]
assert nums == list(range(1, 28)), nums
assert refs == s[s.index("# **References**"):], "reference list changed"
# every reference is cited in the main text: its author form ("A", "A & B" or "A et al."), then its year within 60
# characters; a single author must not be followed by " &", so a two-author paper cannot stand in for it
cited = {}
for line in re.findall(r"^\[\d+\] (.+)$", refs, flags=re.M):
    authors, year = re.match(r"(.+?) \((\d{4}[a-c]?)\)\.", line).groups()
    if authors == "Particle Data Group":
        form, pat = "PDG", r"PDG"
    else:
        parts = authors.split(" & ")
        first = parts[0].split(",")[0]
        if len(parts) == 1:
            form, pat = first, re.escape(first) + r"(?! &)"
        elif parts[0].count(",") > 1:
            form = first + " et al."
            pat = re.escape(form)
        else:
            form = first + " & " + parts[1].split(",")[0]
            pat = re.escape(form)
    cited[f"{form} {year}"] = bool(re.search(pat + r".{0,60}?" + re.escape(year), main))
uncited = [k for k, v in cited.items() if not v]
assert not uncited, ("uncited references", uncited)

open(OUT, "w", encoding="utf-8").write(out)
lines = [f"wrote {OUT}",
         f"bytes: {len(s.encode())} -> {len(out.encode())} | hunks: {len(H)} | md5: "
         f"{hashlib.md5(out.encode('utf-8')).hexdigest()}",
         "reverse splice to the close-out draft: PASS | Section 6 numbered 6.1–6.3: PASS | bold labels closed: PASS",
         "targeted statements gone: PASS | references 1–27 unchanged: PASS | "
         f"all {len(cited)} references cited in the main text: PASS"]
print("\n".join(lines))
open(os.path.join(HERE, "final_pass_output.txt"), "w", encoding="utf-8").write("\n".join(lines) + "\n")
