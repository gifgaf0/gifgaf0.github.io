# Code-repo audit — Joint fold staging memo (G-2a-S1 + G-2a-S2)

**Date:** 2026-06-30 · **Memo:** `staging_memo_G2aS1_G2aS2_joint_fold.md` (SQT) ·
**Auditor:** CC (code side). **Verdict: fold-ready — faithful to both two-leg-verified
gates; the new mechanism strengthening independently confirmed.** Fold itself is the
SQT's to run (canonical lives in the framework project).

## Faithfulness vs my second legs
| memo claim | my second leg | status |
|---|---|---|
| S1: D1=1 (2O genuine {2,2,4}, χ₃/₂ the only 4-dim, FR χ(−1)=−4) | `d89f591` | ✓ matches |
| S1: D2=2 (abelian color commutant) → transverse ℂ⊗𝕆⊗ℍ factor | `d89f591` | ✓ |
| S2: \|G_rot\|=12=T=A₄, 2T=SL(2,3) genuine {2,2,2}, no 4-dim, no C₄ | `ec644c0` | ✓ |
| S2/NC5: strand perms {e,(123),(132)} even, sgn=+1 → color singlet preserved → benign | `ec644c0` (Z₃) | ✓ |
| Net: forced-but-conditional R2 (octahedral premise = located M.ONT import, not refuted) | both | ✓ faithful |

Sub-fact confirmed: 2T = SL(2,3) (order 24) has irreps {1,1,1,3 (bosonic, factor through A₄)}
+ {2,2,2 (genuine)}, Σd²=12+12=24 — **no 4-dim genuine irrep**, so no spin-3/2 quartet. Correct.

## The new mechanism strengthening — independently verified
The memo upgrades "φ≠1/φ breaks C₄" to a **structural cap**: the eccentricity that breaks
octahedral C₄ is the *same* eccentricity that lets the ellipses be Borromean at all (round
circles cannot form Borromean rings — Lindström–Zetterström 1991 / Freedman–Skora, framework
§2.82). `verify_eccentricity_cap.py` confirms the geometry half directly:
- golden eccentric (φ,1/φ): \|G_rot\|=12, no C₄ → **tetrahedral**
- **round circles (a=b=1): \|G_rot\|=24, C₄ present → octahedral**
- generic eccentric (1.3,0.7): \|G_rot\|=12 → tetrahedral

So **any** a≠b caps at tetrahedral; only a=b restores C₄ — and a=b can't be Borromean. The
cap is structural, not a golden-ratio artifact. The "circles impossible" half is a **real,
citable theorem** (Lindström–Zetterström), correctly used as prior art (not claimed novel) —
the gate's contribution is applying it to the symmetry-cap question. Sound.

## Audit notes / nothing blocking
- The third-method NC5 corroboration (induced strand-perm = centralizer content of a 3-cycle
  in S₃ → the even Z₃) is consistent with my second-leg Z₃; no conflict.
- M.CW ceiling R2 throughout; no dynamics; Assignment I/II untouched; §2.52 untouched;
  M.BRIDGE intact (admissibility, not a derived constant). All honored.
- The conditioning is correctly a **location, not a refutation** — the standing open question
  (is the richer K₇-tube/Szilassi/relaxed core simultaneously octahedral *and* Borromean?) is
  the right forward pointer and is flagged, not resolved.

## Disposition
Fold-ready as a **joint conditional-R2 entry** (G-2a-S1/S2). Register: R2 (admissibility,
conditional on the located octahedral import). Provenance: `d89f591` (S1 second leg),
`ec644c0` (S2 second leg), `verify_eccentricity_cap.py` (this mechanism check), plus the
chat-side first legs + third-method audit cited in the memo. The byte-splice into canonical
is the SQT's to run (V4.48 → next), §2.52 row byte-identical, same discipline.
