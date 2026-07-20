# G-TSH2 — CC-Leg Report (full-from-scratch E5(a): kernel-shape dependence of R_T)

**Date:** 2026-07-20 · **Lock (D5, verified byte-identical):** `G_TSH2_PREREGISTRATION_LOCKED.md`
md5 **`99eb26a5d8ff1e32c54d5cff40386098`** ✓ · **Base:** V4.68 CANONICAL · **Chat leg:**
`g_tsh2_chatleg.py` / `gtsh2_results.json` / `arm_mapper.py` / `arm_verdict.json` · **CC scripts:**
`tsh2_cc_reduce.py` (P4 + reduction audit), `tsh2_cc_solver.py` (fresh solver), `tsh2_cc_armmap.py`
(CC arm mapper + C1–C6).

> **Two-leg result: VERDICT-LEVEL AGREEMENT — ARM = UNDERDETERMINED-2. NO S9.** All C1–C6 pass
> (32/32): every kernel g\* exact, a\*/μ ≤0.02%, c_T/c_L1 ≤0.01%, R_T ≤0.01%, identical
> falsifier/exclusion states, D_W/D_X within 0.06 pp, arm identity. K3 excluded (F-LIN+F-ISO) on
> both legs; K6 W-MU-BAND witness on both.

## D5 lock + independence
- **D5 gate satisfied:** the locked instrument was received in-band and hashes byte-identical to
  `99eb26a5…` before any Phase-1 computation.
- **E5(a) full-from-scratch:** the gz1/tsh1 lineage was **not** imported — a fresh solver (`Lattice`
  class, own imaginary-time + preconditioned-descent polish, own σ-parity classifier, own
  zero-intercept reducer) at **own truncation n=34** (chat n=32; F-CONV cross-check at n=40). Own
  Hankel tables (own rmax/dr) for the γ-family; analytic cap. Substrate units ħ=m=ρ₀=1; **no
  physical-c/observable/KC anywhere** (T1 self-grep clean at every invocation).

## Per-kernel results (independent solver, n=34)
| K | kernel | g\* | a\* | μ | c_T | c_L1 | R_T | flags |
|---|---|---|---|---|---|---|---|---|
| K3 | γ=4 | 70 | 1.56241 | 341.832 | 5.3249 | 18.2761 | 0.29136† | **F-LIN, F-ISO → EXCLUDED** |
| K4 | γ=8 | 20 | 1.58888 | 66.898 | 4.6708 | 9.7731 | **0.47792** | — |
| K5 | γ=12 | 20 | 1.53766 | 58.687 | 5.1887 | 10.6192 | **0.48861** | — (GP-res 2.4e-6 > 1e-6; Ward re-check clean 7.3e-8 — H-1 analog) |
| K6 | cap | 90 | 1.18287 | 136.944 | 7.4310 | 14.3949 | **0.51622** | W-MU-BAND (wmu 0.466 < 0.5, non-falsifying) |

†uncertified (K3 excluded). Every kernel: F9 Ward passes by ≥5 orders (2×10⁻¹⁰–7×10⁻⁸); F-NEG never
fired; symmetry residual of ψ₀ ≤ 6×10⁻¹⁶; first passages bracketed by deep fails (K4 25→20 fail 15;
K5 20 fail 15; K6 110→90 fail 85; K3 85→70 fail 65 — all matching the chat's downward extensions).

## K3 exclusion (independently reproduced)
F-LIN fired on the L1 branch in **both** directions (p_W2 = 0.769 GM / 0.632 GK, my own log-log fit)
and F-ISO on L1 (2.60% > 2%) at K3's strong-coupling first-passing point (μ = 342). The T branch was
clean (p ∈ [0.985, 1.008], iso 0.90%) — the shear speed was measurable, but a certified R_T needs a
certified L1. One exclusion (below the two-exclusion return-to-author trigger). Independently
confirmed twice: from-scratch solve **and** the Part-1 reduction of the chat's own raw arrays.

## P4 arm verdict (quarantined; thresholds first appear here)
P_W (7 pts, K3 excluded) = {0.5228, 0.5286, 0.5348, 0.5436, 0.4988, 0.47792, 0.48861}: **D_W = 6.946%**.
P_X (8 pts) = P_W + {0.51622}: **D_X = 7.005%**. Both in the dead-zone (θ₁=3%, θ₂=10%] ⇒
**UNDERDETERMINED-2** (A-2 semantics). The within-γ-family spread (soft-shoulder γ=8,12 at 0.478–0.489
vs the step band 0.523–0.544 under the uniform first-passing convention) is real — ~7% motion, too
large for DERIVED, too small for KNOB; the cross-family cap point (0.51622) lands *inside* the γ-family
span (D_X ≈ D_W), so the out-of-family probe produces no displacement.

## C1–C6 comparison (all PASS; S9 not triggered)
| Item | Result |
|---|---|
| **C1** per-kernel g\* exact grid match | K3=70, K4=20, K5=20, K6=90 — **all exact** |
| **C2** a\*, μ ≤ 0.3% | max deviation **0.02%** (K3 μ) |
| **C3** c_T, c_L1 ≤ 0.5% | max deviation **0.01%** |
| **C4** R_T ≤ 0.5% | max deviation **0.01%** |
| **C5** D_W, D_X ≤ 0.3 pp + arm identity | D_W 6.946 vs 6.947, D_X 7.005 vs 7.007; **arm UNDERDETERMINED-2** |
| **C6** falsifier/control state identity | K3 excluded (F-LIN+F-ISO); K4/K5 clean; K6 W-MU-BAND; C-NEG+C-POS PASS — **identical** |

**Controls (own build):** C-NEG (step g=8 uniform): pipeline ω matches analytic Bogoliubov to <10⁻⁶,
exactly 1 gapless branch, 0 odd-parity gapless. C-POS (classical NN springs): c_L/c_T = √3 recovered to
2.8×10⁻⁸, polarization classifier labels T correctly.

## Anchor corroboration (bonus)
The read-only pool anchors (step R_T {0.5228,0.5286,0.5348,0.5436}, γ6 {0.4988}) were entered as-is per
the locked instrument. Note these are the G-TSH1 outputs, which **this CC lineage already independently
reproduced** in the G-TSH1 CC leg (step 0.52317/0.52861/0.53477/0.54365; γ6 0.49888) — so even the
frozen pool inputs carry independent CC backing.

## Scope / honesty
Cell-level CERT forces p6m periodicity; competing global phases (square/stripe) not tested — declared
instrument scope, carried as annotation. K5 GP-residual floor 2.4×10⁻⁶ (marginally above the 10⁻⁶
target); the locked §4 cure (Ward re-check before use) was performed — Ward 7.3×10⁻⁸, clean; state used
(the chat's H-1, independently reproduced). No KC evaluated; no observable; the transverse scale import
stays named and unexercised (M.CW/T4); Paper IIA §3–§4, T1–T5, the §2.91.H estate, §2.90, μ_n, the
gauge §7.4 firewall untouched. **§2.52 Open 3: frozen, untouched.**

## Consequence (concur with chat routing, §12 UNDERDETERMINED-2 arm)
A kernel-set-extension successor is registered, unopened. Two-leg agreement now achieved; **fold to a
V4.69 candidate awaits explicit author authorization** — agreement is necessary, not sufficient.

---
*Filed 2026-07-20. Fresh E5(a) solver (n=34), byte-identical lock, C1–C6 all pass, arm
UNDERDETERMINED-2; no S9.*
