#!/usr/bin/env python3
# Paper-side companion splice: Paper II §3.4 — append §3.4.7 (G-INT1 fluctuation-spectrum
# ladder extension) before the closing canonical line, and extend that line. Additive.

import hashlib

SRC = "paper_ii_34.md"
OUT = "/mnt/user-data/outputs/paper_II_section_3_4_CANONICAL_v5_with_3_4_7.md"

orig = open(SRC, encoding="utf-8").read()

CLOSING_OLD = ("*§3.4 canonical. §3.4–§3.4.3 filed May 12, 2026; §3.4.4 (internal symmetry & locality) "
               "added June 3, 2026; §3.4.5 (soliton selection rule & meson/baryon split) added June 4, "
               "2026; §3.4.6 (baryon triple-linking & two-sign chirality) added June 4, 2026.*")

assert orig.count(CLOSING_OLD) == 1, "closing-line anchor not unique"

S347 = """### 3.4.7 The selection rule on the fluctuation spectrum

§3.4.4 established that the framework's Fano content is invisible to the substrate vacuum at every local order and lives only on topological defect cores; §3.4.5 confirmed the resulting selection rule on the *static* φ-weighted linking charge Q_φ of a soliton. This subsection carries the same rule one level further — onto the *dynamical fluctuation spectrum* of the internal octonion directions around a defect core — and reports where that spectrum does and does not contain framework-independent content.

**The two-body internal sector is gapless.** Write the order parameter as ψ ∈ ℂ⊗𝕆 (§3.4.4). The symmetric two-body kernel is forced by Schur's lemma to the single scalar K_ij = a(r)δ_ij, so the contact interaction depends only on the total density ρ = |ψ|² = Σ_k|ψ_k|² and is accidentally invariant under the full O(16) acting on the sixteen real components — far larger than the physical ℂ⊗G₂ symmetry. The transverse (internal-direction) fluctuation operator is therefore L_⊥ = −½∇² + (U*ρ − μ) with no anomalous coupling, and the stationary Gross–Pitaevskii equation is precisely L_⊥ψ₀ = 0: the condensate is an exact zero mode of L_⊥, so the internal sector is gapless at the zone centre and carries no framework-specific structure at two-body order. This is the locality result of §3.4.4 re-expressed in the excitation spectrum — the vacuum's internal modes are featureless.

**The framework content enters only through the oriented three-body term on a defect core.** The accidental O(16) degeneracy is lifted only by the term that is not O(16)-invariant — the oriented three-form coupling O = ∫ φ_abc ψ_a ∂_x ψ_b ∂_y ψ_c of §3.4.4, a total derivative and so active only on a topological defect. Around a core whose internal winding lies in directions {a,b,c}, its contribution to the internal fluctuation operator is governed by the structure constant φ_abc: nonzero, and antisymmetric in the internal indices, when {a,b,c} is a Fano line; identically zero off a line. (The symmetric three-body term remains inert, as in §3.4.4.) Two consequences follow, both independent of the radial profile of the core. First, **the selection rule survives into the dynamical spectrum**: a Fano-line core lifts internal modes, a non-line core leaves them untouched — the §3.4.5 rule, now read off the excitations rather than a static charge. Second, **the lifted modes form a chiral pair**: an antisymmetric coupling on the three directions of a line has eigenstructure {0, ±iσ}, so the line carries one unaffected combination and a complex-conjugate (chiral) pair, with the splitting magnitude σ proportional to the oriented coupling strength. The seven internal directions organize as **1 ⊕ 3 ⊕ 3̄** under the realized F₂₁ ⊂ G₂ — the standard decomposition of the seven into the trivial plus a conjugate pair of triplets, whose 3/3̄ split is the quadratic-residue / non-residue partition of §§2.75–2.76.

**What the spectrum does and does not supply.** The selection rule and the multiplet structure are fixed by the octonion structure constants alone — framework-internal facts about which directions wind, carrying no scale. The *magnitude* of the chiral splitting, by contrast, is set by the oriented coupling and the core profile; it is a scale-dependent quantity of exactly the class the substrate action treats as an imported parameter, and it carries no scale-free pure number. The fluctuation spectrum of the internal sector therefore extends the framework's selection-rule ladder — vacuum-blind, defect-localized, Fano-line-selective, now in the excitations as well as the static charge — **without** supplying a parameter-free dynamical observable; the latter remains an imported scale, consistent with the substrate action's standing import structure. No observable bridge is asserted.

**Status and provenance.** The two-body gaplessness (an exact zero-mode identity), the Fano-line selectivity on the fluctuation spectrum, the 1 ⊕ 3 ⊕ 3̄ classification, and the two-chiral-mode count are **Register 1**, established by symmetry and verified independently in two computational environments; the chiral-splitting magnitude is an imported **Register 2** quantity. The supporting computations are recorded in the SQT Master Ledger as **Gate G-INT1 / §2.88.D.2 (V4.47)**, with the pre-registration `G_INT1_EXECUTION_PREREGISTRATION.md` and provenance scripts (first leg `gz1_core.py`-based; independent second leg `verify_gint1_secondleg.py`). This subsection extends the selection-rule ladder of §§3.4.4–3.4.6 into the excitation spectrum; it does **not** advance the load-bearing dynamical gates of the substrate action (the Bjerknes pulsation amplitude and the bilateral fold), which remain the §3.4 frontier.

---

"""

CLOSING_NEW = ("*§3.4 canonical. §3.4–§3.4.3 filed May 12, 2026; §3.4.4 (internal symmetry & locality) "
               "added June 3, 2026; §3.4.5 (soliton selection rule & meson/baryon split) added June 4, "
               "2026; §3.4.6 (baryon triple-linking & two-sign chirality) added June 4, 2026; §3.4.7 "
               "(selection rule on the fluctuation spectrum, Gate G-INT1 / §2.88.D.2) added June 28, 2026.*")

new_block = S347 + CLOSING_NEW
text = orig.replace(CLOSING_OLD, new_block, 1)

# byte-reconstruction
recon = text.replace(new_block, CLOSING_OLD, 1)
ok = (recon == orig)
print(f"orig md5 : {hashlib.md5(orig.encode()).hexdigest()}")
print(f"recon md5: {hashlib.md5(recon.encode()).hexdigest()}")
print(f"byte-reconstruction equals original: {ok}")
assert ok, "RECONSTRUCTION FAILED"
print(f"added chars: {len(text)-len(orig)}")
open(OUT, "w", encoding="utf-8").write(text)
print(f"wrote {OUT}")
print(f"new md5: {hashlib.md5(text.encode()).hexdigest()}")
