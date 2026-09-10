# G-TSH4 — C1–C6 CLOSURE MEMO + V4.72 FOLD-CANDIDATE INVENTORY
**Filed:** chat leg. Base canonical V4.71 `9517f4fb`. Verdict artifact `gtsh4_qc_verdict_v2.json` md5 `7e1d7aaa0d8f0ef3a379d2e1f90de6a7`; mapper v2 `e709487b`; true-optimum data `18d826a7`; queue `697366e8`.

## Comparison status — final
**C1 CLOSED.** Post geometry re-optimization the legs agree on absolute energies to ~5–6×10⁻⁶ (step:AB 68.342346561 vs 68.3427; gem8:AB 98.942311283 vs 98.9429) with fully independent solvers. The 0.067–0.118 offsets were the chat frozen-geometry penalty, as R-1 hypothesized; true optima sit −1.0 to −1.2% from the split-step geometries, c/a within 0.02% of ideal hcp.
**C2 CLOSED.** Q-A = STACK-SELECTED, argmin AB, both legs, both kernels; sub-order AB<FCC<ABC identical; sub-gap ~1.1–1.25×10⁻⁴ on both legs.
**C3 CLOSED (conforming).** Chat now carries the locked statistic with the full E4 multiset. Per-channel transverse speeds agree cross-leg to ~0.1–1% (axial 7.747 vs 7.74; basal SH 8.057 vs 8.0–8.15). Residual item **R-5** (multiset composition / oblique-angle convention behind chat 23.8% vs CC 13.9%) is S9-lite bookkeeping — **arm-invariant**, both compositions and both legs land the same arm.
**C4 CLOSED (two-leg, P-2a).** CC certified Route D (4 zero modes: 3 translations + U(1); no negative ω²); chat validity-gated Route D stands; dynamical F-ISO 0.65% (chat) / 0.79% (CC).
**C5 CLOSED.** The F-ISO static conflict is **resolved as chat frozen-geometry third-order contamination**: identity residual 3.25%/3.80% (frozen) → **0.0269%/0.0174%** (true optimum), matching CC. R-3 falsified circularity; R-4 retro-certified A-2 on the blind leg. Full H-estate listed below.
**C6 CLOSED — verdicts assembled (mapper v2, quarantined, run last):**

| class:kernel | eligibility | A_3D (8-el / 6-el) | **arm** |
|---|---|---|---|
| hex:step | F-ISO 0.027% ✓ | 23.84% / 22.67% | **ANISO-3D** |
| hex:gem8 | F-ISO 0.017% ✓ | 28.01% / 26.45% | **ANISO-3D** |
| cubic:step | (frozen-geom labelled) | 24.74% | **ANISO-3D** |
| cubic:gem8 | (frozen-geom labelled) | 30.18% | **ANISO-3D** |

**Q-C = ANISO-3D, unanimously: both structures, both kernels, both legs, both multiset compositions.** Driver: the oblique quasi-SV sheet (qSV(45°) = 10.08 / 12.38 vs the 7.7–9.2 shear band), set by the C13+C44 coupling — basal isotropy (real, ≤0.8% dynamically on both legs) does not extend to 3D.

## V4.72 fold-candidate inventory (fold script NOT minted; awaits the author's word)
1. **Gate record:** lock chain (staging `bfee456f` → prereg `e66b964d` → A-1 `908f4795`/Part A `2c676701` → dispatch `96eb8e8f`), both leg reports, comparison memos (`dd90d26b`, this memo), verdict `7e1d7aaa`.
2. **Verdicts:** Q-A STACK-SELECTED (AB argmin; stacking sub-question near-degenerate at ~1.2×10⁻⁴, hcp marginally lower, two-leg); Q-B T-LINEAR-3D; **Q-C ANISO-3D (all four combos, two-leg)**; Q-D kernel-labelled ratio family only (KNOB inherited verbatim).
3. **§2.88.B caveat closes in the anisotropic direction:** Theorem 2.1′ confirmed **2D-only**. Basal-plane isotropy survives promotion; 3D isotropy does not.
4. **I4 annotation obligation executes** (pre-declared, staging §5.2): the 1/r² dimension-sourcing keeps three propagating dimensions but loses the isotropic-spherical-shell backing; annotation text to be drafted in the fold.
5. **§5.3 live stake lands — adverse and unconditional:** the Q3(1) carrier-identity claim ("EM and spin-2 share the one transverse channel") now carries a **structure-independent splitting burden**: direction-dependent transverse speeds in every surviving structure at every elected kernel (hex qSV/axial split ~30–37%; cubic ~40%+). The near-degenerate stacking question no longer shields the claim — both branches split. This is the framework's own species-universality obligation made concrete, and it is recorded plainly.
6. **H-protocol estate:** S-class split-step energy bias (2.6–3.4%; flipped the gem8 δ_E call on the blind leg's evidence; does not cancel in curvatures, 14–18%); polish-v1 divergence (VOID F9); BdG exchange |G+q| fix; dx=0.18 discard + residual validity gate (A-2, retro-certified both legs); mapper v1→v2 lineage (locked-qSV omission flipped the indicative hex arm — caught by the blind leg's conforming statistic); chars-vs-bytes size erratum (`a5d88fd7`); queue-patch mishap (file mangled by ambiguous-anchor replace; clean rewrite, no data touched); two transmission-layer defects (reference-style handoff; A-2 activation never delivered).
7. **Standing-rule candidates for the fold:** P-4 (every dispatch is one self-contained file embedding its own activation flags); byte-labelled sizes in all fold memos (erratum rule).
8. **Registered successors:** R-5 convention alignment (S9-lite, arm-invariant, closable by exchange); optional FCC true-optimum magnitudes; E2 convention-resolution witness (standing); the Q3(1) gate now carrying the splitting burden.

## Awaiting the author
**P-4** election, and the word on **V4.72** (fold script minted and executed on it, then the standard reverse-splice + authorization cycle).
