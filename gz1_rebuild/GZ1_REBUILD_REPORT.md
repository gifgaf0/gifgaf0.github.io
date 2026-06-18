# GZ1 REBUILD REPORT

**Date:** 2026-06-13 · **Class:** REPRODUCTION (rebuild vs known R1 record; not a
new gate, not load-bearing) · **Commit:** `87a6666` (pushed to
`claude/sqt-framework-perspectives-kMZyw`, before this report per the persistence
protocol) · **Tarball:** `gz1_rebuild_20260613.tar.gz` · **Master Ledger: untouched.**

Self-contained instrument (numpy/scipy only; no framework tool imported). The
target ζ = 1 − π/√12 = 0.0931004 appears in exactly one file, `comparison_step.py`,
run last (Eddington isolation preserved). Rebuilt from the three surviving
documents only; the lost source code was not consulted (it is lost). Byte-identity
is therefore not expected (original md5s recorded in `REBUILD_NOTE.md` for
contrast); the rebuild is judged by **R1-record agreement**.

## Per-phase target-vs-rebuilt

### Phase 1 — object reproduction (big-box quench, N=160, L=20, seed 7)
| quantity | target (report §1) | tol | rebuilt | PASS |
|---|---|---|---|---|
| ψ₆ (local) | 0.834 | ±0.02 | **0.834** | ✅ (exact) |
| ψ₄ (local) | small | — | 0.111 | ✅ |
| density contrast | ≈1.6 | — | 1.63 | ✅ |
| n_peaks | 234 | — | 234 | ✅ |
| k_c → a | 1.44 (box-quantized) | — | 1.4406 | ✅ |
| p6m crystal | CONFIRMED | — | CONFIRMED | ✅ |

### Phase 2 — primitive cell (17-pt scan + parabolic refine + GP polish)
| quantity | target (report §2) | tol | rebuilt | PASS |
|---|---|---|---|---|
| a\* | 1.4576 | ±0.5% | **1.4576** | ✅ (exact) |
| μ (polished) | 55.86 | ±1% | 55.95 (+0.16%) | ✅ |
| GP residual | ≤ 1e-2 | — | 2.3e-3 | ✅ |
| d_row = √3·a\*/2 | 1.2623 | — | 1.2623 | ✅ |

### Phase 3a — Bogoliubov–Bloch bands (plane-wave BdG, n=32)
| sanity gate | required | rebuilt | PASS |
|---|---|---|---|
| (a) min eig L(Γ)≈0; eigvec=ψ₀ | overlap >0.999 | −0.0003; overlap 0.999987 | ✅ |
| (b) three Goldstone zeros at Γ | 3 lowest <0.5, 4th ≥5 | 0,0,0,22.14,25.50 | ✅ |
| (c) cutoff stability n32→n40 | ≤0.5% | 0.000% | ✅ |

| stop band | target edges (±1%) | rebuilt | PASS |
|---|---|---|---|
| density channel | gapless 0 → ~20.4 | gapless 0 → 20.45 | ✅ |
| Gap A | (20.405, 22.248) | (20.45, 22.14) [+0.22%, −0.49%] | ✅ |
| Gap A2 | (25.225, 25.615) | (25.13, 25.50) [−0.38%, −0.43%] | ✅ |
| Gap B | (29.838, 33.291) | (29.78, 33.18) [−0.19%, −0.34%] | ✅ |

### Phase 3b — Γ–M–K–Γ path
| target (report §3) | rebuilt | match |
|---|---|---|
| Gaps A, B persist over 2D path; A2 normal-incidence only | **all three filled on the K-path** | ⚠ DEVIATION (logged) |

### Phase 4 — driven-strip decay (16-row strip, GMRES, η=0.02)
| probe | ω | t target (report §4) | rebuilt κ | rebuilt t | match |
|---|---|---|---|---|---|
| Gap A midgap | 21.3 | 0.36 ± 0.02 (κ=0.806) | 0.573 | **0.485** | ⚠ κ −29% (logged) |
| Gap A2 midgap | 25.3 | 0.54 ± 0.03 (κ=0.470) | 0.448 | 0.568 | ✅ (κ −5%) |
| Gap B midgap | 31.5 | 0.75 ± 0.03 (κ=0.217) | 0.210 | 0.767 | ✅ (κ −3%) |
| in-band 13.4 | 13.4 | ≈1.00 (per-period 0.998) | 0.0007 | 0.999 | ✅ |
| in-band 20.0 | 20.0 | ≈0.98 | 0.040 | 0.951 | ✅ |
| acoustic 5.0 | 5.0 | no decay regime | −0.027 (r²=0.03) | →1 | ✅ (no clean decay) |

**η-independence at Gap A:** κ(η=0.02)=0.5732 vs κ(η=0.05)=0.5737 — **0.1% shift**
(original 0.3%). Confirms the Gap-A decay is a genuine evanescent stop-band decay
in the rebuild, despite the κ-value offset.

## t-landscape comparison (comparison_step.py — target enters here only)
PASS window [0.0881, 0.0981]. **No probe hits the window.**

| | rebuilt t | factor × target | original t (report §4) |
|---|---|---|---|
| Gap A midgap | 0.485 | 5.2× | 0.36 (3.9×) |
| Gap A2 midgap | 0.568 | 6.1× | 0.54 |
| Gap B midgap | 0.767 | 8.2× | 0.75 |
| in-band / acoustic | → 1 | ~10× | → 1 |
| quasi-static density channel | → 1 (gapless, 3 Goldstones) | ~10× | → 1 |

Closest approach = Gap A, **factor ~5× above target** (original ~3.9×); nothing in
the band structure approaches the window.

## Logged reconstruction choices (HARD RULE 4)
Full list in `REBUILD_NOTE.md`. Headline choices: quench internals from the
pre-registration-cited `mv_g1_minimiser.py` defaults; cell scan window centred on
the **target-independent** big-box k_c; BdG cutoff n_b=32; strip grid Nx=24, Ny=192
(report does not pin the strip grid; the report's "16-row strip" was followed over
the pre-registration's "~36 rows"); fit conventions decoded from the original
`phase4_fits.json` schema. **None resolved by reference to any target number.**

## Logged deviations
1. **Phase 3b path persistence:** rebuild fills A/B on the K-path (report: persist).
   Secondary 2D-path characterisation; does not enter the verdict.
2. **Gap A κ:** 0.573 vs 0.806 (t 0.485 vs 0.36). Largest deviation, concentrated
   at Gap A (midgap just above the gapless acoustic top, ω≈21.3 vs 20.45; coarser
   strip → wrap_min_row 8 vs 6, flatter fit window). Gaps A2/B match κ to a few %.

## VERDICT
**Reproduces the V4.36 R1 record.** The instrument reconstructs the gate's R1
content — p6m object (ψ₆ exact), primitive cell (a\* exact), the full supersolid
Bogoliubov spectrum (three Goldstones, cutoff-stable bands, normal-incidence stop
bands A/A2/B within ±1%, gapless density channel), η-independent evanescent strip
decay, and the comparison outcome: **DEGENERATE (primary)** — the registered
quasi-static density channel is gapless/transparent (t→1) — and
**INFORMATIVE-FAIL (alternative)** — minimum t ≈ 0.49 at Gap A, a factor ~5 above
ζ, with no probe in the PASS window. Quantitative decay constants reproduce within
a few % at Gaps A2/B and within ~30% at Gap A (largest, logged); the qualitative
physics and the gate verdict reproduce. Two deviations are logged (Phase-3b path
persistence; Gap A κ), neither altering the verdict.

Canonicalization is chat-side. Stopping after this report per the brief.
