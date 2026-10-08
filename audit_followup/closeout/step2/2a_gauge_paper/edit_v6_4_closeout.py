#!/usr/bin/env python3
"""edit_v6_4_closeout.py — Step 2a of the close-out brief: the gauge paper's v6.4 draft gains three fixes and a title.

Input:  ../../../phase_b/B1/v6_4_draft/Gifford_Csaszar_Gauge_Group_v6_4_2026_DRAFT.md (md5 afbbf56d…, the Phase B draft).
Output: Gifford_Csaszar_Gauge_Group_v6_4_2026_CLOSEOUT_DRAFT.md (same directory as this script).

Hunks (brief, Step 2a):
  K1 the title (F6 default: "Gauge Group and Generation Structure from the Császár Polyhedron");
  K2 the v6.4 revision note, with items (v)–(viii) and the reference count;
  K3 Section 2: uniqueness of the 7-vertex torus credited to the classical sources (Möbius 1886; enumerated in
     Lutz 2008); Bokowski & Eggert (1991) classify its realizations in ℝ³;
  K4 Section 3: Aut(ℍ) = SO(3), with SU(2) as the unit quaternions acting by conjugation (kernel ±1);
  K5 Section 4: likewise;
  K6 Section 7.1: likewise (the same error, one paragraph later; outside the brief's list, fixed for consistency);
  K7 Section 7.4: the induced spin structure is even (Arf 0), not the all-periodic one;
  K8 Open Problem (xi): the diagonal action of the unit-quaternion groups;
  K9 references: Lutz (2008) and Möbius (1886) inserted alphabetically; the list renumbered 1–27.
Checks: every hunk lands exactly once; removing the hunks reconstructs v6.4 byte-exactly; the reference list runs 1–27
in sequence; no "Aut(ℍ) = SU(2)" remains, and none of the old Section 7.4 sentences survive.
"""
import hashlib
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "../../../phase_b/B1/v6_4_draft/Gifford_Csaszar_Gauge_Group_v6_4_2026_DRAFT.md")
OUT = os.path.join(HERE, "Gifford_Csaszar_Gauge_Group_v6_4_2026_CLOSEOUT_DRAFT.md")
SRC_MD5 = "afbbf56dc1f0b5573d8beb1431555567"

s = open(SRC, encoding="utf-8").read()
assert hashlib.md5(s.encode("utf-8")).hexdigest() == SRC_MD5, "v6.4 draft md5 mismatch"

H = []   # (old, new)

# K1 title
H.append(("**Gauge Group, Generation Structure, Hypercharge, and Quark Mixing**\n\n**from the Császár Polyhedron**",
          "**Gauge Group and Generation Structure**\n\n**from the Császár Polyhedron**"))

# K2 revision note
H.append((" Two references are added (Grossman et al. 2022; Particle Data Group 2024), and the reference list now runs "
          "1–25.*",
          " (v) Sections 3, 4 and 7.1 and Open Problem (xi): the automorphism group of the quaternions is SO(3), not "
          "SU(2). The unit quaternions, Sp(1) ≅ SU(2), act on ℍ by conjugation with kernel {±1}, so SU(2) is the double "
          "cover of Aut(ℍ), and it is this unit-quaternion group of each subalgebra that the construction uses. (vi) "
          "Section 7.4 stated the spin structure backwards. A torus embedded in ℝ³ inherits the structure induced from "
          "ℝ³, which is even (Arf invariant 0): antiperiodic around two of the three nonzero classes of H₁(T²; ℤ₂) and "
          "periodic around one. The all-periodic structure is the odd one, and no embedding induces it. (vii) Section 2: "
          "the uniqueness of the 7-vertex triangulation of the torus is classical (Möbius 1886; see the enumeration in "
          "Lutz 2008); Bokowski & Eggert (1991), cited for it before, classify its realizations in ℝ³. (viii) The title "
          "is shortened to what the paper still claims. Four references are added (Grossman et al. 2022; Lutz 2008; "
          "Möbius 1886; Particle Data Group 2024), and the reference list now runs 1–27.*"))

# K3 Section 2
H.append(("Its uniqueness as the only neighborly triangulation of the torus was proven by Bokowski & Eggert (1991).",
          "Its uniqueness is classical: the 7-vertex triangulation of the torus, Möbius' torus (Möbius 1886), is the only "
          "one with 7 vertices up to isomorphism (see the enumeration in Lutz 2008), and since a neighborly triangulation "
          "of the torus has exactly 7 vertices, it is the only neighborly one. Bokowski & Eggert (1991) classify its "
          "realizations in ℝ³."))

# K4 Section 3
H.append(("Three Fano⁺ lines through v₀ define three quaternionic subalgebras, each with Aut(ℍ) = SU(2), providing the "
          "weak gauge group.",
          "Three Fano⁺ lines through v₀ define three quaternionic subalgebras. The automorphism group of each is "
          "Aut(ℍ) ≅ SO(3), because the unit quaternions, Sp(1) ≅ SU(2), act on ℍ by conjugation with kernel {±1}; the "
          "unit-quaternion group Sp(1) ≅ SU(2) of each subalgebra, the double cover of its automorphism group, provides "
          "the weak gauge group. (Versions through v6.3 wrote Aut(ℍ) = SU(2).)"))

# K5 Section 4
H.append(("each carrying its own Aut(ℍ) = SU(2).",
          "each carrying its own unit-quaternion group Sp(1) ≅ SU(2), the double cover of Aut(ℍ) ≅ SO(3)."))

# K6 Section 7.1
H.append(("carries its own Aut(ℍ) = SU(2), and the weak SU(2) is identified",
          "carries its own unit-quaternion group Sp(1) ≅ SU(2) (the double cover of Aut(ℍ) ≅ SO(3)), and the weak SU(2) "
          "is identified"))

# K7 Section 7.4
H.append(("The Császár polyhedron, as a physical object in three-dimensional space, inherits a specific spin structure "
          "from ℝ³. The three abstract alternatives would require the edge framings to acquire sign flips around "
          "non-contractible cycles (antiperiodic boundary conditions), which the physical embedding does not produce.",
          "The Császár polyhedron, as a physical object in three-dimensional space, inherits a specific spin structure "
          "from ℝ³. That structure is even (Arf invariant 0): it is antiperiodic around two of the three nonzero classes "
          "of H₁(T²; ℤ₂) and periodic around one. The all-periodic structure is the odd one (Arf invariant 1), and no "
          "embedding induces it. (Versions through v6.3 stated the reverse, that the alternatives to the induced "
          "structure are those with antiperiodic conditions around non-contractible cycles.)"))

# K8 Open Problem (xi)
H.append(("the diagonal action of Aut(ℍ₁) × Aut(ℍ₂) × Aut(ℍ₃) on the generation structure",
          "the diagonal action of Sp(1)₁ × Sp(1)₂ × Sp(1)₃ on the generation structure (the unit-quaternion groups of "
          "ℍ₁, ℍ₂, ℍ₃, each the double cover of Aut(ℍᵢ) ≅ SO(3))"))

# K9 references
OLD_REFS_TAIL = ("[23] Particle Data Group (2022). Review of Particle Physics. PTEP 2022, 083C01.\n\n"
                 "[24] Particle Data Group (2024). Review of Particle Physics. Phys. Rev. D 110, 030001.\n\n"
                 "[25] Ringel, G. & Youngs, J. W. T. (1968). Solution of the Heawood map-coloring problem. PNAS 60(2), "
                 "438–445.")
NEW_REFS_TAIL = ("[23] Lutz, F. H. (2008). Enumeration and random realization of triangulated surfaces. In A. I. Bobenko "
                 "et al. (eds.), Discrete Differential Geometry, Oberwolfach Seminars 38, Birkhäuser, Basel, 235–254 "
                 "(arXiv:math/0506316).\n\n"
                 "[24] Möbius, A. F. (1886). Mittheilungen aus Möbius' Nachlass: I. Zur Theorie der Polyëder und der "
                 "Elementarverwandtschaft. In F. Klein (ed.), Gesammelte Werke II, Hirzel, Leipzig, 515–559.\n\n"
                 "[25] Particle Data Group (2022). Review of Particle Physics. PTEP 2022, 083C01.\n\n"
                 "[26] Particle Data Group (2024). Review of Particle Physics. Phys. Rev. D 110, 030001.\n\n"
                 "[27] Ringel, G. & Youngs, J. W. T. (1968). Solution of the Heawood map-coloring problem. PNAS 60(2), "
                 "438–445.")
H.append((OLD_REFS_TAIL, NEW_REFS_TAIL))

out = s
for old, new in H:
    assert s.count(old) == 1, ("anchor not unique", old[:70])
    assert out.count(old) == 1
    out = out.replace(old, new, 1)
for _, new in H:
    assert out.count(new) == 1, ("fragment count", new[:70])

# reverse splice
rev = out
for old, new in reversed(H):
    rev = rev.replace(new, old, 1)
assert rev == s and hashlib.md5(rev.encode("utf-8")).hexdigest() == SRC_MD5, "REVERSE SPLICE FAILED"

# structural checks
refs = out[out.index("# **References**"):]
nums = [int(m) for m in re.findall(r"^\[(\d+)\] ", refs, flags=re.M)]
assert nums == list(range(1, 28)), nums
assert "Aut(ℍ) = SU(2)" not in out.replace("(Versions through v6.3 wrote Aut(ℍ) = SU(2).)", "")
assert "which the physical embedding does not produce" not in out
assert "was proven by Bokowski & Eggert" not in out
assert not re.search(r"\[\d+\]", out[:out.index("# **References**")]), "bracket citation in the body"
for cite in ("Möbius 1886", "Lutz 2008"):
    assert out.count(cite) >= 2, cite      # cited in the body and named in the revision note

open(OUT, "w", encoding="utf-8").write(out)
print("wrote", OUT)
print("bytes:", len(s.encode()), "->", len(out.encode()), "| hunks:", len(H), "| md5:",
      hashlib.md5(out.encode("utf-8")).hexdigest())
print("reverse splice to v6.4 draft: PASS | references 1–27 in sequence: PASS | old statements gone: PASS")
