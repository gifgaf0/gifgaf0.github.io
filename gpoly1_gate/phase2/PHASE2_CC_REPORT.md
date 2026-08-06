# G-POLY1 PHASE 2 — CC LEG REPORT (election E5: finite-d/lambda birefringence estimator)

**Date:** August 6, 2026. **Leg:** CC, blind, full-from-scratch. **Base:** V4.74 CANONICAL md5 `13d5eda14c69d3f68468a6ccdb8c3257` (1,403,855 B). **Lock:** memo `35a6225c38b66d2ac497d9e9af447e71` (5,104 B), lock record `f1c1342c843e34ec40ae1eaab201b947` (3,001 B). **Elections (T3-immutable):** E2-1(a) independent-grain variance addition; E2-2 monodisperse d; E2-3 four configs, pure phases only.

**CC checkpoint:** `poly1_phase2_cc.json` md5 `3f0b951b24b48d79cd842ce7d1dfb1d6` (2,905 B) — written and hashed before the chat checkpoint was consulted numerically (see H-CC-3).

## 1. Verify-then-build

All five dispatch embeds re-extracted per the declared convention and md5-verified before any construction:

| embed | declared md5 | declared B | result |
|---|---|---|---|
| `staging_memo_G_POLY1_phase2_E5.md` | `35a6225c38b66d2ac497d9e9af447e71` | 5,104 | **OK** |
| `G_POLY1_PHASE2_LOCK_RECORD.md` | `f1c1342c843e34ec40ae1eaab201b947` | 3,001 | **OK** |
| `poly_vrh_results.json` (input X-1) | `200e7a8b775577564369c6924d38a84c` | 2,767 | **OK** |
| `poly1_phase2.json` (chat checkpoint) | `e5341b6d97a079ad5387ef77f2f80773` | 2,933 | **OK** |
| `g_poly1_phase2_chatleg.py` (reference-only) | `de1de47975aba83283455587fe486469` | 7,098 | **OK** |

The input is additionally byte-verified inside the instrument at every invocation. T1 forbidden-string self-grep: **PASS (0 hits)** at every invocation.

## 2. Zero-shared-machinery instrument (`g_poly1_phase2_ccleg.py`)

Deliberately different stack from the chat leg at every layer:

- **Quadrature:** Gauss–Legendre × Gauss–Legendre product — GL nodes in cos(theta) *and* GL nodes in phi (mapped to [0, 2π]) — not the chat's plain GL × uniform-azimuth product. Base **144×144**, doubling 288×288.
- **Eigen stack:** hand-written vectorized cyclic Jacobi rotations for the symmetric 3×3 Christoffel matrix — no library eigensolver.
- **Christoffel contraction:** tensordot + broadcast-sum construction, own Voigt→C4 expansion.

## 3. Law (C-P2-3 statement)

Reproduced verbatim from the LOCKED memo, §3(c), not from chat numerics:

> **(c) Path-random accumulation law (E2-1 declared convention).** A ray of length L crosses N = L/d independent, uncorrelated grains; per-grain splitting contributions add in variance; the accumulated RMS fractional polarization delay is
>   **δ_RMS(L) = s₁ · √(d/L).**

with B(n̂) = 2(v_qT1 − v_qT2)/(v_qT1 + v_qT2), the qT pair being the two smallest eigen-speeds, and s₁ = √⟨B²⟩ over the uniform sphere measure (psi-average exact — eigenvalues are polarization-frame independent).

## 4. CC-leg results (base 144×144)

| config | s₁ | mean B (non-verdict) | max B, grid (non-verdict) |
|---|---|---|---|
| hex:step | 0.151508022494 | 0.126158 | 0.241893 |
| hex:gem8 | 0.181569446593 | 0.151673 | 0.283958 |
| cubic:step | 0.233348903639 | 0.208823 | 0.415069 |
| cubic:gem8 | 0.284231507661 | 0.253817 | 0.509884 |

## 5. Gates (all hard except the witness)

| gate | requirement | CC value | verdict |
|---|---|---|---|
| F-ISO-NULL | exact isotropic (cubic:step K_VRH=123.832, G_VRH=60.825) max B ≤ 1e-12 | max B = 3.416e-16 | **PASS** |
| F-QUAD | doubling changes s₁ ≤ 1e-9 rel | 1.282e-14 / 1.284e-14 / 4.163e-15 / 4.492e-15 | **PASS** (all four) |
| qL-SEPARATION | min v_qL > max v_qT per config | 14.7220>10.0914; 18.5605>12.4058; 13.1467>9.2354; 16.4967>11.4692 | **PASS** (all four) |
| F-N1 | δ_RMS(d) = s₁ exactly | s₁·√(d/d) == s₁ identically | **PASS** |

## 6. Cross-leg comparison (C-P2)

| criterion | requirement | worst observed | verdict |
|---|---|---|---|
| C-P2-1 | 12 invariants (3 × 4 configs) ≤ 1e-8 rel | 8.101e-11 (cubic:gem8 inv_qT_lamsum) | **PASS** |
| C-P2-2 | four s₁ values ≤ 1e-6 rel | 1.063e-10 (cubic:gem8) | **PASS** |
| C-P2-3 | law-form identity, reproduced from LOCKED memo text | §3 above, verbatim | **PASS** |

Per-config s₁ cross-leg rel deltas: hex:step 3.3e-15, hex:gem8 4.4e-15, cubic:step 6.1e-11, cubic:gem8 1.1e-10. All 12 invariant rel deltas ≤ 8.1e-11 (hex configs at ≤1.3e-14; cubic at 1.8e-11–8.1e-11, consistent with the two legs' different residual quadrature tails at their respective 1e-9-gated bases). Grid-dependent non-verdict quantities (mean B, grid max B, grid min/max speeds) agree at the 1e-5–1.3e-3 level, as expected for extremum/slow-converging quantities sampled on different grids; not gated. **S9: NOT TRIGGERED — no misses.**

## 7. Honesty items (full parity)

- **H-CC-1 (eigen stack replaced pre-consultation):** the first CC eigen stack was a closed-form trigonometric (Cardano) solver; it failed F-ISO-NULL at max B = 1.798e-8 — the known ~√eps accuracy loss of the closed form at degenerate eigenvalue pairs, which is exactly the point the isotropic null probes. Replaced with hand-written vectorized cyclic Jacobi (backward stable at degeneracies); F-ISO-NULL then passed at 3.416e-16. No outputs consumed from the failed configuration.
- **H-CC-2 (base resolution ladder — parity with chat H-5):** the GL×GL ladder 18/36/72/144/288 gives s₁ rel deltas (cubic:step) 1.25e-3 / 1.13e-5 / 3.90e-9 / 4.16e-15 — geometric decay with the same long cubic harmonic tail the chat leg disclosed. A 72×72 base would fail the 1e-9 doubling gate on both cubic configs (3.9e-9, 5.4e-9). Base set to 144×144 within the memo's free resolution parameter; the pinned 1e-9 gate unchanged; no outputs consumed from sub-gate resolutions. Chat's H-5 (32×32 GL×uniform failure at 1.164e-6, base raised to 64×64) is carried here with full parity.
- **H-CC-3 (in-band dispatch structure):** this is a P-4 self-contained IN-BAND dispatch — the chat checkpoint and chat instrument are embedded in the same file, which was necessarily read in full at ingestion. Blind discipline was maintained procedurally, not by information barrier: the CC instrument was written zero-shared-machinery (different quadrature construction, different eigen stack, different contraction), and the CC checkpoint was written and md5-hashed before any numeric cross-leg comparison was performed.
- **H-CC-4 (W-ANISO reference figures unavailable):** the banked G-TSH4 ANISO-3D splitting figures are not embedded in this dispatch and do not appear in the working repo; the witness below therefore reports the CC max-B figures alongside the chat leg's for cross-leg consistency, with the G-TSH4 comparison itself deferred to a leg with access to the banked figures. Witness only — never a gate.

## 8. W-ANISO witness (non-gate)

Max single-grain qT split as % of mean, CC grid (chat grid in parentheses): hex:step 24.19 (24.18); hex:gem8 28.40 (28.40); cubic:step 41.51 (41.46); cubic:gem8 50.99 (50.92). Cross-leg consistent at the grid-extremum level; G-TSH4 comparison deferred per H-CC-4.

## 9. Standing discipline

Anchors `a1d19dd9` SEALED and not sought — θ appears nowhere in this leg (Phase 3 mapper only). The hex G_HS pin remains PENDING-verbatim, not consumed. §2.52 Open 3 frozen, untouched. No d derived or bounded (M.CW); Phase 2 delivers only the dimensionless coefficient s₁ of a law in d/L. E8 checkpoint discipline observed.

## 10. Verdict

**G-POLY1 Phase 2, CC leg: C-P2-1 PASS, C-P2-2 PASS, C-P2-3 PASS. All hard gates PASS. S9 not triggered.** Banked Phase-2 objects: the four s₁ values (§4) and the law δ_RMS(L) = s₁·√(d/L).
