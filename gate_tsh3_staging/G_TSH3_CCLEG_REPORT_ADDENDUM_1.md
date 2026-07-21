# G-TSH3 CC-Leg Report — ADDENDUM 1 (post-comparison closure)

**Date:** 2026-07-22. Original CC report seal untouched (append-only). Records three items that
landed after the initial CC leg: the from-scratch cap_p2 solve, the two-leg F-CONV (S9-lite)
closure, and an independent second-leg of the chat's H-6 witness correction.

## 1. cap_p2 — full from-scratch solve landed (C4 upgraded to fully-independent)
The background cap_p2 solve completed: **EXCLUDED**, R_T = 0.45094 (chat 0.45092, 0.00%), F-LIN L1
exponents **p_L1 = [0.986, 0.946, 0.987, 0.952] — identical to the chat's** (W2 = 0.946/0.952 <
0.95, strong-coupling L1 sublinearity at μ ≈ 418). C4 is now confirmed **from scratch on this
family**, not only by the cross-gate TSH2-K3 corroboration. cap_p2 remains excluded ⇒ not pooled ⇒
KNOB unaffected. (The recorded F-CONV 2.6e-5 is the same non-deep artifact; irrelevant — cap_p2 is
excluded on F-LIN L1.)

## 2. F-CONV divergence — closed two-leg (S9-lite), no full S9
My first `point`-run excluded gem8/gem4 on F-CONV ~4.5e-5. The chat ran a counter-cross-check
(`s9lite_fconv.py`, deep + fixed-a\*, Fourier-upsampled n=40) and my deep fixed-a\* diagnostic
(`tsh3_cc_fconv.py`) agree on the true truncation convergence:

| kernel | recorded (leg procedure) | chat S9-lite (deep, fixed-a\*) | CC (deep, fixed-a\*) |
|---|---|---|---|
| gem8@g20 | 4.1e-6 | 2.27e-9 | **9.9e-10** |
| gem4@g35 | 1.4e-6 | 1.11e-9 | **8.4e-10** |
| gem3@g70 | 3.8e-6 | 5.64e-10 | (certified, conv 1.1e-6 in point-run) |

All ~10⁻⁹–10⁻¹⁰, three-to-four decades inside the 5×10⁻⁶ gate. The divergence is **closed as
noise-at-a-fragile-gate** (a\*-reoptimization jitter + non-deep residuals, both ~10⁻⁵); full S9 not
triggered. All CERTIFIED statuses stand on both legs.

## 3. H-6 (chat witness-mechanism correction) — independently second-legged
My CC F-CONV diagnosis propagated back to correct a chat R2 annotation: the six witness F-CONV
drops were attributed to physical peak-sharpening, but are procedure noise. I independently
reproduced the chat's key evidence point:

**gem8 @ g_w = 33.03** (1.5·g_c): CC a\* = 1.42025 (chat 1.42025), R_T = 0.49945 (chat 0.49945,
0.00%), **deep fixed-a\* F-CONV = 1.87×10⁻¹⁰** (chat S9-lite 3.54×10⁻¹⁰; recorded drop 1.0×10⁻⁵).
→ **procedure-noise CONFIRMED** — the witness drop is not truncation. The drops stand as recorded
(T3, honest fires of the locked procedure); D_C stays degenerate; the §7 arm stays unqualified;
**KNOB unaffected.** γ8@34.1's F-LIN L1 component is a real sublinearity signature and is untouched
by this correction (the same strong-coupling L1 mechanism as cap_p2 / TSH2-K3).

## Standing
Two-leg verdict **ARM = KNOB** unchanged; C1–C6 all AGREE (`TWO_LEG_COMPARISON_G_TSH3.md`). The
successor-binding process lesson (pin F-CONV operationalization: deep, fixed-a\*, continuation-
seeded) is on record for future memos. Fold to §2.91.K + one Part VI row awaits explicit author
authorization.

---
*CC addendum filed 2026-07-22. cap_p2 from-scratch exclusion confirmed; F-CONV closed two-leg; H-6
independently second-legged. No S9.*
