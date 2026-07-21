# G-TSH3 STAGING MEMO — the kernel-set-extension successor (axis-(ii) resolution, round 2)

**Status:** STAGED FOR AUTHOR REVIEW — NOT LOCKED. Lock = author word "Lock"; md5 of this file seals at that word, byte-identical thereafter.
**Date staged:** July 20, 2026 (chat leg).
**Lineage:** Executes the successor **registered, unopened** at V4.69 (§2.91.J; G-TSH2 lock §12 consequence routing). Canonical basis: SQT_Master_Ledger_v4_69_CANONICAL.md, md5 `23290cee45dddcf712dfaae1281b02b5` (seal re-verified this session).
**Author elections (July 20, 2026):** E1 = (c) both families, capped at 4 kernels; E2 = convention witness YES (quarantined, non-verdict-carrying); E3 = W-μ carry YES; E4 = CC full-from-scratch.

---

## §1 Question (re-posed)

G-TSH2 closed UNDERDETERMINED-2 with the 8-point certified set frozen at D_W = 6.947% / D_X = 7.007%. The inherited A-2 map is **arithmetically closed** on those statistics (D_W is frozen inside the dead zone; no extension can reach any A-2 arm), so the successor's map must be re-posed — announced here, pre-execution, with the inherited thresholds θ₁ = 3%, θ₂ = 10% in restated roles (this is role restatement on new statistics, not threshold motion on an observed one; T3 intact).

**Question:** Extending the certified kernel set by four kernels across two new analytic families, under the identical uniform per-kernel first-passing convention, does the extended R_T ≡ c_T/c_L1 set classify as **BAND** (one coarse class invariant), **FAMILY-INDEXED** (pinned per kernel family), or **KNOB**?

## §2 Import set

{ kernel forms **GEM-3, GEM-4, GEM-8, cap-p2** } — the one named new import — plus the read-only frozen anchors (8 certified points, G-TSH1/2 lineage, independent CC backing), g per the inherited E2(a) two-tier first-passing convention with the downward-extension clause and deep-fail bracket at g\*−5, ρ₀ = 1. Substrate units throughout (T4). The transverse scale import (any physical c_T = c statement) remains **named and unexercised**; no physical-c / GW170817 / φ-target string in any computation file (T1 self-grep at every invocation, both legs).

## §3 Kernel definitions and analytic facts

| kernel | U(r) | Û(k) | Q± basis |
|---|---|---|---|
| GEM-n, n ∈ {3,4,8} | exp(−rⁿ) | numeric Hankel | Likos criterion: Q± guaranteed for all n > 2 (the S-1 Gaussian defect was exactly the n = 2 marginal case) |
| cap-p2 | (1−r²)²₊ | 16π·J₃(k)/k³ (analytic) | Bessel oscillation ⇒ negative lobes guaranteed |

Anchor forms for reference: step = θ(1−r), Û = 2πJ₁(k)/k; γ-family = 1/(1+r^γ); cap-p1 = (1−r²)₊, Û = 4πJ₂(k)/k².

## §4 Pre-lock feasibility diagnostic (executed July 20; design-level, no gate quantity)

`gtsh3_feasibility_diag.py` — integrator validated to ≤ 4.4×10⁻¹⁶ against the three analytic forms; convention ħ = m = ρ₀ = 1, spinodal g_c = min_{Û<0} k²/(−4Û(k)). **Calibration against the three locked anchors: 3/3 PASS** — step 14.737 (target 14.74, 0.02%), γ6 31.880 (31.88, 0.00%), cap-p1 105.464 (105.5, 0.03%) — the convention is byte-equivalent in output to the 49b157ba diagnostic class.

| kernel | Q± | k_lobe | Û(k_lobe) | k_c | g_c |
|---|---|---|---|---|---|
| gem3 | Y | 4.971 | −0.0823 | 4.768 | 71.87 |
| gem4 | Y | 5.096 | −0.1568 | 4.835 | 39.19 |
| gem8 | Y | 5.271 | −0.2941 | 4.930 | 22.02 |
| cap-p2 | Y | 7.594 | −0.0309 | 7.351 | 451.24 |

All four candidates are cluster-forming with finite spinodals; the GEM family's g_c range (22–72) brackets the anchor range. **Risk flag (pre-lock, disclosed):** cap-p2's shallow lobe puts its first-passing point deep in the strong-coupling regime (g\* plausibly ≳ 300, μ large) — the γ4/F-LIN exclusion class. Retained per [D4]: an exclusion there is itself informative (it would replicate the γ4 mechanism on a *different family*, evidencing the exclusion class is coupling-strength-sourced, not family-sourced — R2 annotation if it fires). No window motion in response (T3).

## §5 Frozen inputs

8-point certified set (read-only): step {0.5228, 0.5286, 0.5348, 0.5436}, γ6 0.4988, γ8 0.47791, γ12 0.48861, cap-p1 0.51622. Mean μ₀ = 0.51392; envelope [0.47791, 0.5436]; D₈ = 7.007%. **Family assignments (locked):** F_SS = {step×4, γ6, γ8, γ12}; F_CAP = {cap-p1, cap-p2}; F_GEM = {gem3, gem4, gem8}.

## §6 Certification criteria and falsifiers (inherited verbatim)

Per-kernel first passing under E2(a) two-tier (tier-2 three-random-init deep re-solves, machine-identity ≤ 10⁻¹⁵ rel); cell-level p6m CERT (global square/stripe phases out of scope, declared); BdG dense plane-wave Hermitian pencil (L+2X)η = ω²L⁻¹η with the σ-parity classifier; chat truncation n = 32 with F-CONV at n = 40; falsifiers F9 (Ward, gate as locked in TSH2), F-LIN (both locked windows, both branches), F-ISO (2% direction-pair), F-CONV (≤ 5×10⁻⁶), F-CLS, F-NEG; controls C-NEG (uniform Bogoliubov analytic match < 10⁻⁶, zero odd gapless) and C-POS (spring lattice c_L/c_T = √3, classifier labeling) both legs; a certified R_T requires a certified L1 **and** T. **Exclusion budget:** two exclusions among the four new kernels ⇒ return-to-author before any arm (inherited trigger).

## §7 Arm map (quarantined; θ's only executed appearance; run last)

Let P_ext = the 8 frozen points ∪ all newly certified points; D_ext = max-from-mean over P_ext (12-dp arithmetic; a |value − θ| < 10⁻⁶ boundary hit logs BOUNDARY and resolves by the strict rule).

- **BAND** — ≥ 3 of 4 new kernels certified [D3] **and** D_ext ≤ θ₂: R_T is a coarse class invariant of the p6m GP supersolid across ≥ 3 analytic families under the uniform first-passing convention; the band = the P_ext envelope; the ~7–10% width caveat travels with every downstream use; the first-passing convention is flagged as the residual convention import (informed, not decided, by the §8 witness).
- **FAMILY-INDEXED** — D_ext > θ₂ **and** the locked family containing the maximal-departure point has internal D_F ≤ θ₁: R_T is pinned per kernel family; a downstream author family-selection declaration is registered (which family instantiates the vacuum kernel — the G-C1 located roton-kernel import made concrete).
- **KNOB** — D_ext > θ₂ **and** that family's D_F > θ₁.

The trichotomy is exhaustive on the certified outcomes; no dead zone is required. UNDERDETERMINED cannot recur by construction except through the §6 return-to-author trigger.

## §8 E2 convention witness (quarantined, non-verdict-carrying)

Motivated by the G-TSH2 R2 annotation (cap non-displacing; within-family spread the driver): a locked secondary read of R_T at matched relative coupling **g_w = r₀·g_c(K), r₀ = 1.5** [D1], g_c per the §4 diagnostic. Witness set [D2] = {gem3, gem4, gem8, cap-p2} ∪ anchors {step, γ8, cap-p1}:

| point | g_c | g_w |
|---|---|---|
| step | 14.74 | 22.1 (≈ the certified g = 22 point; reuse rule: any g_w within 0.5 of an already-certified point reuses that certification) |
| γ8 | 22.75 | 34.1 |
| cap-p1 | 105.46 | 158.2 |
| gem3 | 71.87 | 107.8 |
| gem4 | 39.19 | 58.8 |
| gem8 | 22.02 | 33.0 |
| cap-p2 | 451.24 | 676.9 (likely-drop flag) |

Same falsifier bar; a failed witness point **drops with a log entry, no budget impact** (non-verdict-carrying). Statistic **D_C** = max-from-mean over certified witness points, computed in the quarantined mapper, reported as R2 annotation only. Locked interpretation guide (non-binding): D_C ≪ D_ext ⇒ the residual spread is convention-sourced ⇒ a convention-resolution successor (elevating this witness to verdict-carrying) registers, unopened; D_C ≈ D_ext ⇒ genuine kernel-shape dependence, the §7 arm stands unqualified.

## §9 E3 W-μ witness carry

E4(a) protocol as locked in TSH2: simple-shear deformed-cell static μ_s vs ρ·c_T² for every certified kernel; reported R2, non-falsifying; the TSH2 §8 W-MU-BAND flag band inherited unchanged.

## §10 Two-leg protocol (E4)

CC **full-from-scratch**: own lattice class, own Hankel tables, own imaginary-time + polish schedule, own σ-parity classifier and reducer, own truncation election; the TSH1/2/3 chat solvers not imported. **The locked memo travels in-band** (D5 standard); CC verifies byte-identity against the lock md5 before Phase 1. Comparison C1–C6 at verdict level (per-kernel g\*, a\*/μ, speeds, R_T, D-statistics, arm + witness D_C + W-μ); S9 counter-cross-check on any disagreement.

## §11 Consequence routing (pre-declared)

Per-arm as in §7. Under every arm: no KC evaluated; no observable; nothing prior modified; the transverse scale import unexercised; Paper IIA §3–§4, T1–T5, the §2.91.H retired estate, §2.90, μ_n, and the gauge-paper §7.4 firewall untouched; the §2.52 Open 3 row untouched per standing instruction. The V4.68 successor-surface items (four Q3 declarations; the 3D-stack shear gate) remain open as registered — not consumed here. Fold target: §2.91.K + one Part VI row, on author authorization.

## §12 LSF-δ log (July 20, 2026; formal re-check at lock)

Queries: "cluster crystal supersolid transverse longitudinal sound ratio potential shape"; "generalized exponential model GEM-4 cluster crystal negative Fourier component Likos criterion". Findings: (i) Likos Q± criterion (Likos et al. 2001) — GEM-n cluster-forming iff n > 2; 2D GEM-4 hexatic/cluster phases (Prestipino–Saija 2014); classical phonon dispersions of GEM cluster crystals (Neuhaus–Likos 2011) — classical-sector prior art, no GP supersolid modulus-ratio sweep. (ii) Blakie, honeycomb supersolid (arXiv:2410.15754): three sound speeds ↔ elastic parameters via hydrodynamics; shear instability — adjacent, different lattice, single interaction. (iii) A 2D-supersolid excitations study placing dipolar vs soft-core in "bulk-incompressible" vs "rigid-lattice" elastic limits — the nearest cross-family elastic-character statement; authorship to be pinned at the lock-time formal sweep; two-point, cross-setting, not a kernel-shape sweep at a uniform convention. **A0: NOT TRIGGERED** — no published kernel-shape sweep of c_T/c_L1 within the GP soft-core class at a uniform convention (author-side confirmation carried from the TSH2 sweep of Rakic–Ho–Lee arXiv:2403.13727, single potential family).

## §13 Defaults embedded (amendable at lock; author "Lock" adopts as-is)

[D1] r₀ = 1.5. [D2] witness anchor subset {step, γ8, cap-p1}. [D3] BAND requires ≥ 3 of 4 new certifications. [D4] cap-p2 retained despite the §4 strong-coupling risk flag.

## §14 Provenance staged with this memo

`gtsh3_feasibility_diag.py` (diagnostic, T1-clean by construction), `gtsh3_feasibility.json` (results incl. γ8/γ12 g_c completions). Lock sequence: author "Lock" → md5 seal → chat leg drafted (T1 self-grep at every invocation) → in-band CC handoff → P0–P4 → quarantined mapper last → comparison → fold on authorization.
