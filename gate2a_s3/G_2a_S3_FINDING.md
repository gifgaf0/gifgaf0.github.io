# G-2a-S3 — Banked Finding (code-repo record)

**Date:** 2026-07-02 · **Memo:** `G_2a_S3_scoping_closure_memo.md` (SQT) · **Status:
BANKED AS A FINDING — not a register-change fold.** The μ_n factor-of-4 register is
**unchanged**; it is annotated as a **located and likely-blocked import**. G-2a-S1's forcing
result (D1=1) and V4.50's tetrahedral cap stand exactly as filed.

## What I verified (the decidable R1 piece) — CC second leg, proactive
The memo said a CC second leg on the rep-theory piece is wanted only *if promoted past R3*.
It's cheap and I had the 2O machinery, so I did it now (`gate2a_s3_repcheck_secondleg.py`,
independent SU(2)-matrix build + Chebyshev characters):

| quantity | result | meaning |
|---|---|---|
| \|2O\|, \|2T\| | 48, 24; 2T ⊂ 2O; −I ∈ 2T | ✓ |
| ⟨χ₃/₂,χ₃/₂⟩_2O | **1.0000** | spin-3/2 **irreducible** over 2O (the quartet) |
| ⟨χ₃/₂,χ₃/₂⟩_2T | **2.0000** | **splits 2+2** over 2T (two *distinct* genuine 2's) |
| ⟨χ₁/₂,χ₁/₂⟩_2T | 1.0000 | spin-1/2 stays an irreducible genuine 2 |
| χ₃/₂(−I)_2T | −4 | still genuine/FR |
| 2T irreps | 7 classes → 4 bosonic (A₄: 1,1,1,3) + 3 genuine (2,2,2) | **no 4-dim genuine irrep** |

So the memo's **Result 1 is confirmed**: the quartet does not vanish under tetrahedral
symmetry — it **fragments** into two of 2T's three 2's. This sharpens V4.50's "no 4-dim
irrep" into the precise mechanism. The rep-theory piece is now **two-leg verified** and
ready should it ever be promoted past R3.

**Reflections cannot reglue it (not separately computed — standard + cited).** The Borromean
config's full symmetry is T_d ≅ S₄, but T_d's extra elements are *reflections/improper*, not
in SO(3), so they don't lift to SU(2)=Spin(3) where spin-3/2 lives — they cannot fuse the
2+2 back into the 4. (Golubitsky et al., SIAM JADS: T_d and O are the two *inequivalent* S₄
subgroups of O(3); only the rotational doubling — the C₄'s of O — lives in SU(2).) Sound
standard reasoning; correctly cited as prior art.

## What I did NOT second-leg (correctly)
**Result 2 (R3, suggestive negative)** — that a texture-envelope (hopfion) with Borromean
core-topology *and* octahedral symmetry is non-generic — is **literature-based** (Sutcliffe
arXiv:0705.1468 hopfion taxonomy to Q=16, links at Q=5–6, trefoil at Q=7 with C₃-breaking;
Battye–Sutcliffe; Hietarinta–Salo; the structural Q = pairwise-linking vs μ̄₁₂₃ =
pairwise-unlinked mismatch). It is correctly banked as a **suggestive negative** needing no
computational second leg; the literature is cited as prior art, not claimed as new work. I
neither re-derived nor second-legged it — that would be inventing a compute the memo
explicitly and correctly declines.

## The convergence (faithful record)
The μ_n factor-of-4 needs octahedral 2O symmetry; the two-component baryon's two candidate
homes are both closed against it, for the **same** underlying reason (Borromean linking
resists the high symmetry the quartet requires):
- **filament core** (Borromean link embedding): **NO** — tetrahedral cap, V4.50/CKS
  general theorem (proven, planar-strand). The eccentricity needed to be Borromean without
  self-intersection is the same eccentricity that breaks octahedral C₄ (G-2a-S2, verified).
- **texture envelope** (hopfion field): **NO** (suggestive) — this memo.

## Disposition (as the memo sets it, faithfully)
- **No register change.** Banks as a finding; if ever folded, enters as an *exploration
  annotation* on the Gate-2a open-items row (factor-of-4 = located, two-reading-blocked
  import) + a cross-ref from §2.87.B / the M.ONT gate — **not** a new numbered gate, **not**
  a register change.
- **M.ONT decoupled.** Two-component ontology stands on its own merits (the baryon carries
  both a filament invariant = Borromean linking = baryon number/ropelength mass, and a
  texture invariant = rotor band = spin), **not** as a μ_n rescue — the rescue it would have
  been committed *for* does not materialize. The declaration is left to the author on the
  ropelength-mass-cleanness tradeoff.
- **Honest hedges carried:** suggestive not proven (a fine-tuned excited octahedral Borromean
  texture is not *formally* excluded); the ℂ⊗𝕆 exotic-target caveat (the structural Q vs μ̄
  point is target-general and survives; specific energetics may not transfer verbatim).
- **M.CW ceiling R2/R3**; §2.52 untouched; M.BRIDGE intact (admissibility, not a derived
  constant).

*Provenance: `gate2a_s3_repcheck_secondleg.py` (this decidable-piece second leg), the SQT
scoping/closure memo (archived), and the cited construction literature. Prior second legs:
`d89f591` (S1), `ec644c0` (S2).*
