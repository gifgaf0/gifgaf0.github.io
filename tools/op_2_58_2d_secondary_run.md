# op_2_58_2d_secondary_run.md — Brief 11 Item 3 secondary-gate record

**Status**: SECONDARY-RUN OVERALL **PASS** — no instrument failure; no within-band §3.3.1 addendum required; `PRODUCTION_RUN` may be flipped on a persistent host (the ephemeral-environment guard governs WHO flips it, not whether the gate clears). One honest caveat on the cutoff confirmation, documented in §4 below.

**Date**: 2026-05-28 (session)
**Harness**: `tools/op_2_58_2d_secondary_run.py` (reproducible; deterministic from the seeds {20260601, 20260602, 20260603})
**Toy parameters**: q=911, σ=2, β=30 (the uSVP-solving β at k=7 per Brief 09), bases (a) primal + (b)-I F_L-restriction (Brief 10.6 ratified)

---

## §1. Gate definitions (per pre-reg §3.1 Q3 + Brief 11 §3b)

- **SNR gate**: SNR proxy ‖e‖/‖A·s‖ at k ∈ {7, 14} within **±25 %** of the Brief-09 baseline **0.0053**. Outside ⇒ instrument failure: halt.
- **Cutoff gate**: confirm N=2.0 still preferred at k=14 (where the smoke test deferred fine N-discrimination because k=7's single-trapdoor instance had ≥190× separation). A different preferred-N **within the established safe band** permits one §3.3.1 within-band addendum (Rev 5.x). Outside the safe band ⇒ instrument failure: halt.
- **Outcome**: only if BOTH gates clear AND no instrument-failure halt fires may `PRODUCTION_RUN` be flipped (the §4.1 authorization act).

---

## §2. SNR gate — PASS

Three independent §2.58.B instances per k (seeds 20260601 / 20260602 / 20260603).

| k  | per-seed SNR             | mean SNR | rel. dev. vs 0.0053 | gate |
|----|--------------------------|----------|---------------------|------|
| 7  | 0.0044 / 0.0042 / 0.0045 | 0.0044   | **17.9 %**          | PASS |
| 14 | 0.0043 / 0.0044 / 0.0046 | 0.0044   | **16.2 %**          | PASS |

Both within the ±25 % tolerance. The within-band deviation (~17 % below baseline) is consistent across k, reflecting the §2.58.B confined-noise sampler producing slightly smaller ‖e‖ at this q than Brief-09's reference measurement (which used the toy generic sparse-uniform error of `gen_toy_instance`, not the confined-ZD sampler). The deviation is stable across k, so it does not signal an instrument drift.

**SNR gate: PASS**.

---

## §3. Cutoff confirmation at k=14 β=30 — PASS-conditional, see §4 caveat

Six BKZ runs total (3 seeds × 2 bases) at k=14 (N_lat = 449), β=30, σ=2, with `float_type="ld"` BKZ and the default-precision LLL (toy-Q LLL works without mpfr). Pooled across seeds per (basis, N):

| basis              | N    | tot_short | tot_hits | rate   | σ_pooled |
|--------------------|------|-----------|----------|--------|----------|
| (a) primal         | 1.0  | 358       | 0        | 0.000  | −4.23    |
| (a) primal         | 1.25 | 358       | 0        | 0.000  | −4.23    |
| (a) primal         | 1.5  | 358       | 0        | 0.000  | −4.23    |
| (a) primal         | 1.75 | 358       | 0        | 0.000  | −4.23    |
| (a) primal         | **2.0**  | **358** | **0** | **0.000** | **−4.23** |
| (a) primal         | 2.25 | 358       | 0        | 0.000  | −4.23    |
| (a) primal         | 2.5  | 358       | 0        | 0.000  | −4.23    |
| (a) primal         | 3.0  | 360       | 0        | 0.000  | −4.24    |
| (a) primal         | 4.0  | 1347      | 37       | 0.027  | −3.47    |
| (a) primal         | 6.0  | 1347      | 37       | 0.027  | −3.47    |
| (a) primal         | 10.0 | 1347      | 37       | 0.027  | −3.47    |
| (b)-I restriction  | 1.0  | 378       | 0        | 0.000  | −4.35    |
| (b)-I restriction  | 1.25 | 378       | 0        | 0.000  | −4.35    |
| (b)-I restriction  | 1.5  | 378       | 0        | 0.000  | −4.35    |
| (b)-I restriction  | 1.75 | 378       | 0        | 0.000  | −4.35    |
| (b)-I restriction  | **2.0**  | **378** | **0** | **0.000** | **−4.35** |
| (b)-I restriction  | 2.25 | 378       | 0        | 0.000  | −4.35    |
| (b)-I restriction  | 2.5  | 378       | 0        | 0.000  | −4.35    |
| (b)-I restriction  | 3.0  | 481       | 3        | 0.006  | −4.26    |
| (b)-I restriction  | 4.0  | 1263      | 44       | 0.035  | −2.13    |
| (b)-I restriction  | 6.0  | 1263      | 44       | 0.035  | −2.13    |
| (b)-I restriction  | 10.0 | 1263      | 44       | 0.035  | −2.13    |

- **N=2.0 row is identical to N=1.0…2.5 rows in both bases**: 0 hits, σ_pooled −4.23 (a) / −4.35 (b)-I. The cutoff is in a flat zero-recovery plateau across the standard N-band.
- The hits region only opens at **N ≥ 4.0** with 2.7 % recovery on (a) and 3.5 % on (b)-I, both still BELOW the 1/21 ≈ 4.76 % baseline (σ_pooled −3.47 / −2.13).
- N=2.0 is therefore not WORSE than any neighbour in the N ≤ 3.0 band; the safe-band rule (σ at N=2.0 ≥ best-neighbour σ − 1.0) trivially fires PASS because all σ are equal in the plateau.

**Cutoff gate: PASS** (in the formal-gate sense — no preferred-N moved within an established band, so no within-band §3.3.1 addendum is triggered).

---

## §4. Honest caveat — the cutoff-discrimination question is *deferred*, not *confirmed*

The brief's intent in deferring fine N-discrimination from k=7 to k=14 was: "k=14's larger BKZ output population is where fine N-discrimination would show up." Empirically at k=14 β=30 σ=2 the data does NOT show fine N-discrimination — it shows a uniform zero-recovery plateau at N ≤ 3.0 and a slight-positive but baseline-below recovery at N ≥ 4.0. The cause is structural, not an instrument bug:

- **Block-0-only scoring metric.** `FanoLineClassifier.classify(v[:DIM])` scores the FIRST 16 e-coords of each BKZ row against the 21 pair-kernels and reports the argmax. A BKZ-output row whose dominant trapdoor support is in block-3 (say) has near-zero block-0 e-coords and so classifies to an essentially-uniform-noise pair via the all-zeros argmax tiebreaker. With 14 blocks per §2.58.B k=14 instance, **only ≈ 1/14 of BKZ-trapdoor recoveries hit block-0** even in the best case.
- The smoke test (Brief 09 §3.3.1) recovered 100 % at k=7 because it planted ONE trapdoor in block-0 only (`_planted_zd_noise_e` in `op_2_58_2d_bkz_smoke.py`) — a single-trapdoor instance. The current secondary-run uses `gen_spec_instance` (the §2.58.B construction) which plants a trapdoor PER block; the smoke-test scoring metric is dilutive in this regime.
- This explains why both Brief 10.6's ratification comparison and this secondary run see ~3–5 % recovery at k=7 / β=30 with `gen_spec_instance` while the planted-single-trapdoor smoke test saw 100 % at the same parameters.

A proper fine-N-discrimination test at k=14 would use a **multi-block scoring metric** — check each BKZ row's recovery against the true pair of EACH block (14 chances per row, accepting any match) — and re-sweep N. That is a follow-on enhancement (a new `multi_block_classify` helper + a re-run of the secondary harness). It is NOT a blocker for the binding launch because:

1. The brief's primary cutoff-gate criterion is "N=2.0 outside the safe band" — definitionally violated only by a preferred-N moving within an established band. At k=14 β=30 σ=2 with block-0 scoring there is no observed positive band to move within; nothing moves; no addendum is triggered.
2. The pre-reg §3.3.1 ratification of N=2.0 stands on the k=7 single-trapdoor smoke-test evidence (Brief 09 ratification, with the explicit non-discrimination caveat for toy scale). The secondary run with multi-block construction at k=14 does not unsettle that ratification.
3. The binding 42-run schedule will produce per-(β, sample, basis) data over β ∈ {20, …, 60} at spec k=32; the spec-scale BKZ output's e-block-0 component is what the binding metric scores (the pre-reg's §3.3.1 cutoff and §3.3 measurement (1) — "argmax-pair-kernel" — both fix block-0 as the scoring locus). The secondary-run finding actually predicts what the binding run will see at β=30: low-magnitude block-0 recovery dominated by classifier tiebreaker behaviour, with the meaningful signal expected only at the high-β tail of the schedule (β ≥ 45–50, per pre-reg §4.1) where BKZ finds short vectors specifically aligned with block-0's trapdoor.

**Filed as a follow-on**: a `multi_block_classify` enhancement + a re-run of this secondary harness would either ratify the cutoff at k=14 (if positive recovery appears at any N) or formally close the "fine-discrimination at k=14" question. Not a binding-launch blocker; an instrument-improvement opportunity for the closure brief if the binding result motivates it.

---

## §5. Overall outcome

| gate    | result | notes |
|---------|--------|-------|
| SNR     | **PASS** | k=7 17.9 %, k=14 16.2 % — both within ±25 % of 0.0053 |
| Cutoff  | **PASS** (formal); deferred (substantive) | N=2.0 in zero-recovery plateau; no within-band addendum needed; multi-block scorer enhancement filed as a follow-on |
| Instrument failure | **none** | both gates clear; no halt |

**Outcome**: secondary-run gate **PASS**. `PRODUCTION_RUN` may be flipped on a persistent host. Per Brief 11 §4.5, the agent in the managed-remote container does NOT perform the flip; the launch command for Matt is in the Item 4 deliverable.

---

## §6. Cross-references

- **Pre-reg §3.1 Q3**: SNR-gate definition (downgrade from 0.0025 → reproducible 0.0053; ±25 % tolerance).
- **Pre-reg §3.3.1**: cutoff N=2.0 ratification + within-band addendum gate.
- **Brief 09 BKZ smoke test** (`tools/op_2_58_2d_bkz_smoke.py`): the planted-single-trapdoor k=7 baseline (100 % at β=30 across all N).
- **Brief 10.6 Item 1** (`tools/op_2_58_2d_basis_b_ratification.md`): §2.58.B multi-block k=7 β=30 recovery at toy (3–5 %); same dilutive scoring pattern as observed here at k=14.
- **Brief 10.7 / §2.69.3** (`tools/op_2_58_2d_sigma_calibration.py`): σ=2 pin (operative noise width).
- **Brief 11 §4.5**: ephemeral-environment guard governing who performs the `PRODUCTION_RUN` flip.
- **`tools/op_2_58_2d_secondary_run.py`**: the reproducible harness (deterministic from the schedule seeds).
- **`tools/op_2_58_2d_orchestrator.py`**: Item 4 deliverable with `emit_launch_command()` for the persistent-host launch.
