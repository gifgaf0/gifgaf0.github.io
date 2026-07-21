# G-TSH3 Chat-Leg Report — ADDENDUM 1 (post-CC, S9-lite)
July 21, 2026. Original report seal e7036f1f68ec368840317e87da513601 untouched; this addendum is a separate sealed artifact (append-only discipline).

## S9-lite counter-cross-check (diagnosis-grade; no recorded gate outcome moves)
Trigger: CC's first run excluded gem8/gem4 on F-CONV ~4.5e-5; CC re-operationalized (deep solves, fixed a*) → ~1e-9 → CERTIFIED, matching chat. A unilateral re-operationalization that flips a status requires a chat-side counter-check before the two-leg record closes.
Instrument: `s9lite_fconv.py` — a* FIXED at the recorded optimum; deep solves (res 1e-12) at n=32 and n=40 (n=40 seeded by deterministic Fourier upsampling of the n=32 state); speeds at the locked AUTH-INST-1 instrument.
Results (chat leg):
| case | recorded conv (leg procedure) | conv (deep, fixed-a*) |
|---|---|---|
| gem8 @ g*=20 (P2, 1.2× margin) | 4.1e-6 | **2.27e-9** |
| gem4 @ g*=35 (P2) | 1.4e-6 | **1.11e-9** |
| gem3 @ g*=70 (P2) | 3.8e-6 | **5.64e-10** |
| gem8 @ g_w=33.03 (witness, DROPPED) | 1.0e-5 | **3.54e-10** |

**Closure:** CC's diagnosis is two-leg confirmed. The leg's recorded F-CONV values were dominated by a*-re-optimization jitter plus non-deep solver residuals, not truncation error; physical truncation convergence is ~1e-9–1e-10, three-to-four decades inside the 5e-6 gate. The initial CC gem8/gem4 divergence is closed as noise-at-a-fragile-gate; full S9 not required — this counter-check is the documented counter-cross-check. All CERTIFIED statuses stand on both legs.

## H-6 — witness-drop mechanism annotation corrected (self-caught via S9-lite)
The original report attributed the six witness F-CONV drops to physical truncation ("peaks sharpen at 1.5·g_c"). **Falsified** by the gem8@33.03 counter-check (3.5e-10): the fires were measurement-procedure noise under the leg's locked operationalization (re-optimized a*, non-deep). Correction scope:
- **The drops stand as recorded.** They were honest fires of the locked procedure; T3 forbids post-verdict re-measurement to harvest certified witness points. D_C stays degenerate; the witness stays uninformative; the §7 arm stands unqualified; nothing about KNOB moves.
- Exception note: γ8@34.1 dropped on **F-LIN L1** ([1.06, 0.923, 1.061, 0.928]) *and* F-CONV — the F-LIN component is a real sublinearity signature (γ4/cap_p2 class at elevated coupling) and is NOT touched by this correction.
- **Process lesson (successor-binding):** F-CONV operationalization was under-specified in the memo (a* fixed vs re-optimized; solver depth). Any successor memo pins it explicitly — recommended: deep, fixed-a*, continuation-seeded. The registered convention-resolution witness successor is the clean vehicle if a live D_C is wanted.

## Artifact seals (this addendum's set)
`s9lite_fconv.py`, `s9lite_fconv.json` — md5s in the updated manifest.
