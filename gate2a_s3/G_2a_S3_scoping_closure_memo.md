# G-2a-S3 — Scoping / Closure Memo: The Texture-Envelope Octahedral Rescue

**Status:** BANKED AS A FINDING — not a register-change fold. The verdict is a
**suggestive negative** (literature-informed), not a theorem; per standing discipline it is
recorded as an exploration/finding, and it does **not** change the register of any filed
result. The μ_n factor-of-4 register is unchanged; it is annotated as a **located and
likely-blocked import**.
**Date:** July 2, 2026
**Mode:** Literature-Search-First (constructive) + a bounded chat-side representation-theory check.
**Two-leg:** the decidable rep-theory piece is chat-side first-leg only (exploratory); the
suggestive-negative verdict is literature-based and needs no computational second leg. If ever
promoted past R3, the rep-theory piece would want a CC second leg.

---

## What G-2a-S3 tested

Under the two-component ontology (M.ONT adjudication, staged), the baryon is a filament core
(Borromean linking, ropelength mass) inside a texture envelope (rotor band, spin). The spin-3/2
quartet — the μ_n factor-of-4 — comes from the texture envelope's rotor band, not the filament
core. G-2a-S3 asks: **can the texture envelope carry octahedral (2O) symmetry**, which the
quartet requires, given that the filament core cannot (V4.50/CKS: capped at tetrahedral)?

This is the last surviving route to the factor-of-4: V4.50 closed the filament route for the
planar-strand case by a general theorem; the texture envelope, being a field rather than a link
embedding, is not covered by that theorem, so it was the open escape.

---

## Result 1 — the decidable representation-theory piece (R1, chat-side)

Sharpens V4.50's "2T = SL(2,3) has no 4-dim genuine irrep" into the precise mechanism:

- **spin-3/2 is irreducible over 2O** (⟨χ_{3/2},χ_{3/2}⟩_{2O} = 1: the quartet) but **splits as
  2+2 over 2T** (⟨χ_{3/2},χ_{3/2}⟩_{2T} = 2: two of 2T's 2-dim genuine irreps). The quartet
  does not vanish under tetrahedral symmetry — it *fragments*.
- **The reflections cannot reglue it.** The Borromean config's full symmetry is T_d (order 24 ≅
  S₄), doubling the rotational A₄ by reflections. But reflections are not in SU(2), where
  spin-3/2 lives, so they cannot fuse the two 2's back into the 4. Per Golubitsky et al. (SIAM
  J. Appl. Dyn. Syst., "Hopf Bifurcation with Tetrahedral and Octahedral Symmetry"), T_d and O
  are the two *inequivalent* S₄-representations in O(3) — T_d doubles A₄ by reflections, O by
  rotations — and only the rotational doubling (the C₄'s) lives in SU(2). So the quartet forms
  **iff the missing C₄ lifts to a grand-spin symmetry** via internal (isospin/color)
  compensation.
- **Abstract strand-action is permissive.** O = S₄ *can* act on the three colored strands:
  S₄ → S₃ = Weyl(SU(3)), with V₄ acting trivially (matching V4.50's "C₂'s fix all strands") and
  the C₄'s inducing color-Weyl transpositions. No group-theoretic obstruction. The diagonal lock
  is not *abstractly* forbidden — so the question is pushed to geometric existence.

Provenance: chat-side computation (`g_2a_s3_repcheck`, exploratory), building 2T/2O explicitly
and computing the spin-3/2 character norms and the S₄→S₃ strand action.

## Result 2 — the construction-literature verdict (R3, suggestive negative)

Whether a texture with Borromean core-topology and octahedral symmetry *exists* is not decidable
by representation theory (M.CW: permissive but cannot produce the field). The Faddeev–Skyrme /
hopfion construction literature (Battye–Sutcliffe; Sutcliffe, "Knots in the Skyrme-Faddeev
model", arXiv:0705.1468; Hietarinta–Salo) settles it as far as construction goes, and points
**against** the rescue:

1. **No Borromean core in the taxonomy.** Hopfions are computed up to Hopf charge 16; the
   multi-component cores that appear are *pairwise-linked* — links at charges 5–6, the trefoil
   knot at charge 7 — because the Hopf charge *is* a linking number. The Borromean rings are
   pairwise-*unlinked*, carry no pairwise linking, and appear nowhere in the taxonomy.
2. **Energetics disfavor the required symmetry.** The charge-7 trefoil hopfion's energy is
   *lowered by breaking* its potential cyclic C₃ symmetry — a knotted core relaxes away from
   symmetry. Octahedral symmetry (order 24) is far more disfavored. High-symmetry *single*
   hopfions are not the energetic norm.
3. **Octahedral hopfions exist only in crystals.** Cubic/octahedral hopfion configurations in
   the literature are periodic arrays (engineered via R⁴/rational-map lattice constructions),
   not single isolated solitons.
4. **Structural reason (also explains §3.4-G2).** The Hopf charge is cross-fiber pairwise
   linking; Borromean-ness is the same-fiber triple invariant μ̄₁₂₃, pairwise-unlinked and
   Q-invisible. The texture's energy and symmetry are driven by Q, which is blind to the
   Borromean structure — so the envelope's symmetry drivers are *decoupled* from the Borromean
   core, and there is no mechanism by which the Borromean structure would induce octahedral
   symmetry in the envelope. This is the mechanism behind §3.4-G2's "Hopf charge is blind to the
   Borromean baryon."

**Verdict:** the texture-envelope-octahedral rescue is non-generic on two independent counts
(Borromean cores are not selected by hopfion energetics; octahedral symmetry is energetically
disfavored for knotted/linked cores) and absent from the literature. Suggestive negative.

---

## The convergence — why this matters

The μ_n factor-of-4 requires octahedral (2O) symmetry. The two-component baryon has exactly two
places that symmetry could live, and both are now closed against it:

| component | octahedral? | basis |
|---|---|---|
| filament core (Borromean link embedding) | **NO** (tetrahedral cap) | V4.50/CKS general classification theorem — **proven**, planar-strand case |
| texture envelope (hopfion field) | **NO** (suggestive) | this memo — taxonomy + energetics + structural Q/μ̄₁₂₃ mismatch |

Octahedral symmetry is incompatible with Borromean-ness in **both** readings, for the **same
underlying reason**: Borromean linking structurally resists the high symmetry the quartet
requires (the eccentricity that a symmetric Borromean embedding needs to avoid self-intersection
is the same eccentricity that breaks the octahedral C₄; the pairwise-unlinked structure the
Borromean rings require is the same structure hopfion energetics does not select or symmetrize).
The μ_n line has converged to a structural impasse.

---

## Consequence for the M.ONT declaration

**Decouple the ontology declaration from the μ_n rescue.** Two-component remains the correct
*ontology* — the baryon demonstrably carries both a filament invariant (Borromean linking =
baryon number; ropelength mass) and a texture invariant (rotor band = spin; proton-as-hopfion),
and no single-component reading hosts both. That conclusion is independent of this memo. But
two-component does **not** rescue the factor-of-4 (both components fail the octahedral
requirement). So the M.ONT declaration should be made — or deferred — on its own merits: the
ropelength-mass-cleanness tradeoff (the clean single-monomial → two-term-sum cost), **not** as a
μ_n rescue. The rescue it would have been committed *for* does not materialize.

---

## Honest hedges

1. **Suggestive, not proven.** A fine-tuned, non-minimal, energetically-excited octahedral
   Borromean-core texture is not formally excluded — only unsupported by the taxonomy,
   energetically disfavored, and against the structural grain. A genuine construction (against
   the literature's grain) would overturn this; none exists.
2. **Exotic target caveat.** The SQT substrate target is ℂ⊗𝕆, not the standard S²; an exotic
   target could in principle shift the taxonomy/energetics. The core structural point (Q =
   pairwise linking; Borromean = pairwise-unlinked) is target-general and survives this caveat,
   but the specific energetics may not transfer verbatim.
3. **Not a register change.** The μ_n factor-of-4 register is unchanged. This memo relocates and
   annotates it (located, likely-blocked import); it does not close, retract, or downgrade any
   filed R1/R2 result. G-2a-S1's forcing result and V4.50's tetrahedral cap stand exactly as
   filed.

---

## Register and disposition

- **R1:** the spin-3/2 → 2+2 splitting over 2T; the permissive S₄→S₃ strand action (chat-side;
  CC second leg only if promoted).
- **R3 (suggestive):** the construction-literature negative on the octahedral Borromean texture.
- **No register change** to the μ_n factor-of-4 or to any prior entry.
- **Proposed disposition:** bank as a finding; if later folded, it enters as an *exploration*
  annotation on the Gate-2a open-items row (the factor-of-4 as a located, two-reading-blocked
  import) and a cross-reference from §2.87.B / the M.ONT gate — **not** as a new numbered gate
  and **not** as a register change. The M.ONT declaration is decoupled and left to the author on
  the ropelength-cleanness merits.

## Provenance

- Sutcliffe, P., "Knots in the Skyrme-Faddeev model", arXiv:0705.1468 (hopfion taxonomy to
  Q=16; links at Q=5,6; trefoil at Q=7; C₃-symmetry breaking of the Q=7 trefoil).
- Battye, R. A. & Sutcliffe, P. M., "Solitons, Links and Knots" (the core-link taxonomy);
  Hietarinta, J. & Salo, P., "Faddeev-Hopf knots: dynamics of linked un-knots".
- Golubitsky et al., "Hopf Bifurcation with Tetrahedral and Octahedral Symmetry", SIAM J. Appl.
  Dyn. Syst. (T_d and O as inequivalent S₄-representations in O(3)).
- Cantarella–Kusner–Sullivan, arXiv:math/0402212 §10.1 (the filament tetrahedral cap, V4.50).
- Chat-side `g_2a_s3_repcheck` (spin-3/2 ↓ 2T = 2+2; S₄→S₃ strand action).
- Cross-references: §2.87.B (V4.49/V4.50), §3.4-G2 (Hopf-blindness, now mechanized),
  M.ONT adjudication memo (the two-component declaration this decouples).
