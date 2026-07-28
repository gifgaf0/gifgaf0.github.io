# G-TSH4 Phase 0 — CC Independent Recompute (structure determination, Q-A)

**Date:** 2026-07-23 · **Auditor/leg:** CC · **Base:** V4.71 (authorized P-a). **Objects:**
`gtsh4_phase0_core.py`, `gtsh4_phase0_results.json`, `G_TSH4_PHASE0_EXECUTION_REPORT.md` (chat, HALTED
under E5(b)). **CC script:** `tsh4_cc_phase0.py` (fresh solver; chat core NOT imported).

> **Independent, deterministic recompute of Phase-0 Q-A.** Own 3D solver, preconditioned descent to
> the **true discrete-GP minimum** (res ≤ 1e-8) — *not* the chat's split-step fixed point. Because
> Phase-0 is energy minimization, this is a legitimate second leg despite the earlier out-of-order
> exposure of the chat's numbers: an independent minimizer either reproduces the ordering or it does
> not, and (by design) it also independently checks whether Q-A is robust to the split-step bias. It
> is **not** the full Phase-1/2 leg (that needs the locked pre-registration and a resume).

## Result — Q-A ordering CONFIRMED (both kernels)
Ordering **AB < {FCC ≈ ABC} < BCC < AA** in both step and gem8 — matches the chat leg.

| kernel | CC AB→FCC gap (true-GP) | chat split-step gap | δ_E | polished-report gap |
|---|---|---|---|---|
| step | **1.248e-4** | 1.111e-4 | 1e-4 | 1.251e-4 |
| gem8 | **1.150e-4** | 9.08e-5 | 1e-4 | — |

My step gap (1.248e-4) matches the earlier *polished* execution report's gap (1.251e-4) to <0.3% —
strong evidence the gap is trustworthy even though absolute energies carry a dx=0.05 discretization
offset (see caveats). hcp (AB) is marginally lowest in both kernels.

## Three findings, stated carefully
**CC-1 — the hcp/fcc near-degeneracy is real (~1e-4), independently.** Both true-GP gaps are ~1.1–1.25e-4.
The 2D→3D structural question answers **yes on the structural side**: the 3D ground state is a
close-packed stack of triangular (p6m) layers; only the stacking sequence (hcp vs fcc) is near-degenerate.

**CC-2 — the F-3 arm-label defect is INDEPENDENTLY CONFIRMED.** ABC with free c/a relaxes to
**c/a = 2.45028 ≈ √6 = 2.44949** (the fcc geometry) and its energy equals the independently-seeded
cubic FCC energy to **1.7e-7 (step) / 1.9e-7 (gem8)**. Two different cell constructions, one energy:
**FCC *is* an ABC stack of triangular layers.** The locked STACK/NON-STACK map therefore does not
carve structure space (the chat's F-3); the honest re-carve {AA, BCC}=non-close-packed vs
{AB, ABC≡FCC}=close-packed p6m stacks is supported on a second, independent solver. (Re-labelling is
an author call, filed at the catch.)

**CC-3 — the E5(b) straddle is METHOD-SENSITIVE (S9-lite class, not a verdict divergence).** The chat's
**split-step** Phase-0 put gem8 at gap 9.08e-5 (< δ_E → DEGENERATE → halt) and step at 1.111e-4
(> δ_E → STACK-SELECTED). At the **true-GP** minimum both kernels sit *just above* δ_E (1.15e-4 /
1.25e-4 → both marginally STACK-SELECTED). The split-step energy bias (2.6–3.4% absolute, self-caught
by the chat) does **not** cancel in the ~1e-4 hcp–fcc difference — it shrinks the gap and pushes gem8
across δ_E. So the halt-triggering straddle is a **method artifact at the fragility floor**, exactly
the chat's F-4 ("any 'hcp beats fcc' statement is not robust"). This is **not** a verdict-level
divergence (both legs agree: hcp/fcc near-degenerate, hcp marginally lower, exact call below resolving
power) — it is a gate-fragility (S9-lite) observation that **reinforces the chat's E5(b)(a)
recommendation**: carry **both** hcp and fcc into Q-C, since the gate's real stake is isotropy and the
exact stacking order is below resolving power on either method.

## Honesty / caveats (this leg)
- **AA is unreliable in this leg.** My AA optimizer found a poorer local configuration (e≈74.7 at
  c/a≈0.97) than the chat's (≈71.6 split / 69.7 polished). AA is the highest-energy, non-competitive
  structure, so it does not affect the ordering or the verdict — but its exact energy from this leg
  should not be used. All competitive structures (AB, FCC, ABC, BCC) relaxed cleanly (res ≤ 1e-8,
  correct droplet counts, c/a matching: AB 1.632, ABC √6).
- **Absolute energies carry a dx=0.05 discretization offset** (my AB 68.342 vs polished 68.410; my
  cells ~1% more compact) — sharp droplets are marginally under-resolved at dx=0.05, biasing absolute
  energy low and geometry compact. The chat's definitive values used finer grids. I therefore compare
  **gaps and ordering** (robust; gap matches the polished report), never absolute energies.
- **This is Phase 0 (Q-A) only.** Q-B/Q-C/Q-D (existence, the decisive 3D-isotropy A_3D, ratios) are
  untouched — they need the locked `G_TSH4_EXECUTION_PREREGISTRATION.md` (`e66b964d`, not yet
  delivered) and a resume after the author resolves F-3 and E5(b).
- **Independence note (standing):** the earlier out-of-order exposure means a future *Phase-1/2* CC
  leg cannot be blind (see `G_TSH4_STAGING_PREAUTH_AUDIT.md` §D). The present Phase-0 recompute is
  robust to that exposure (deterministic minimization, different method, and it landed on a subtly
  different δ_E call — the signature of a genuine independent computation, not a tuned one).

## Standing discipline
No shear speed, ratio, anisotropy statistic, observable, or magnitude computed (Q-A is energies only).
KNOB inherited. T4 grep-clean. §2.52 Open 3 frozen; §2.87.J reserved. Nothing fold-eligible (Phase 0
only, gate HALTED to author).

---
*CC Phase-0 independent recompute filed 2026-07-23. Q-A ordering + hcp/fcc near-degeneracy + F-3
confirmed; E5(b) straddle shown method-sensitive (S9-lite, supports E5b(a)). Full leg awaits the
locked pre-registration and the author's F-3/E5(b) resolution.*
