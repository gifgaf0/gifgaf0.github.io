# OP-2.58.2d BKZ smoke test — sweep results (Brief 09, Item 3)

**Date:** May 27, 2026
**Brief:** CLAUDE_CODE_BRIEF_09 §3.3 (Item 3)
**Status:** Pre-freeze. Toy scale q=911, k=7 (dim 225). No §2.58.B / spec execution.
**Harness:** `tools/op_2_58_2d_bkz_smoke.py` (fplll C++ BKZ, long-double GSO,
auto-abort, max_loops=8). Seeds 20260601/602/603.
**Feeds:** the §3.3.1 cutoff repin recommendation (`op_2_58_2d_Q2_cutoff_repin.md`).

---

## 1. Item 2 — known-leakage sanity check

The planted error `e` (a ZD-noise vector in K_{a,b} for a known pair) classifies
to its true pair with confidence ratio exactly 1.0:

```
planted e → argmax (1, 7) (true (1, 7)), ratio 1.0000 — PASS
```

The lattice→classifier handoff is sound; the rest of the brief proceeds.

## 2. Setup note — what the toy "leakage" instance is

The genuine §2.58.B Fano-line trapdoor is spec-only / post-freeze and is **not**
available at toy scale. To exercise the recovery metric we plant a ZD-noise
error `e ∈ K_{a,b}` (known pair) in block 0 of an otherwise generic toy LWE
instance, build the §3.6 primal lattice, and treat the planted pair as the
"true (a,b)". The unique shortest lattice vector is then `v_target = (e, s, 1)`
(‖v_target‖ ≈ 4–5, vs Gaussian heuristic ≈ 108 — a large-gap uSVP/BDD instance).

## 3. Cutoff sweep (per (β, seed, N); k=7)

Recovery = fraction of the short-set whose e-slice argmax-pair equals the true
pair. σ is against the 1/21 ≈ 4.762% baseline.

| β | seeds | min norm (BKZ) | uSVP solved | recovery vs N | σ |
|---|---|---|---|---|---|
| 20 | 601/602/603 | 911.00 (all) | **No** (all) | flat ≈ baseline (0–10%) | ≤ 3.8 per-seed, never 5σ |
| 30 | 601/602/603 | 4.58 / 4.36 / 4.12 | **Yes** (all) | **100% at every N ∈ {1.0…10.0}** | 4.47 per-seed |

### Pooled across the three seeds at each (β, N)

| β | N (all swept 1.0→10.0) | tot_short | tot_hits | rate | σ_pooled |
|---|---|---|---|---|---|
| 20 | 1.0 | 47 | 0 | 0.000 | −1.53 |
| 20 | 1.25 | 52 | 1 | 0.019 | −0.96 |
| 20 | 1.5 | 182 | 10 | 0.055 | 0.46 |
| 20 | 1.75 | 637 | 46 | 0.072 | 2.91 |
| 20 | 2.0 … 10.0 | 675 | 46 | 0.068 | 2.50 |
| 30 | **1.0 … 10.0 (every N)** | 3 | 3 | **1.000** | **7.75** |

(Full per-(β,seed,N) table is reproducible from the harness `main()`.)

## 4. Reading the data

**β = 30 (reduction succeeds).** Every seed solves the uSVP and recovers the
planted trapdoor. The next-shortest output vectors sit at ≈ 889 — a ≥190×
separation from the ≈ 4.5 trapdoor — so the short-set is a **singleton** for any
cutoff N up to ≈ 190. Recovery is therefore **100% at every swept N**, identical
across seeds, with pooled σ = 7.75 (well above the §3.2 5σ threshold). The curve
is perfectly flat: no discontinuity, no sample disagreement.

**β = 20 (reduction fails).** No seed reduces below the q-vectors (min norm
911). Recovery sits near/below the 1/21 baseline at every N. The per-seed σ
bumps up to ≈ 3.8 (and pooled 2.9 at N=1.75) are **not genuine leakage signal**:
exact q-multiple vectors signed-lift to the zero vector and fall through to the
classifier's argmax tie-break pair, a degenerate-input artifact, not a recovered
trapdoor. No σ reaches 5σ and no trapdoor was found.

**Stability.** At both β the recovery-vs-N curve is monotone/flat with no
discontinuity, and the three seeds agree (β=30: all 100%; β=20: all ≈ baseline).
This **rules out the §3.4(c) instability outcome** — the §5 goal of the smoke
test.

**Non-binding cutoff at toy scale.** Because the toy leakage instance produces a
single near-trapdoor vector separated from the bulk by ≫10×, the cutoff is
non-binding for any N in the swept range: at β=30 every N ∈ [1.0, ≈190] selects
exactly the trapdoor (recovery 100%); at β=20 no N surfaces signal. The toy data
cannot finely discriminate between candidate N values (e.g. 1.5 vs 2.0 vs 3.0)
because there is no graded short-vs-bulk norm band — exactly the regime Brief-07
Q2 predicted ("the cutoff is calibrated against BKZ output norm structure, not
the ambient distribution"). Fine calibration needs higher β or genuinely
multi-vector §2.58.B-structured leakage, and is deferred to the secondary-run
validation gate.

## 5. k = 14 not required

The brief makes k=14 conditional on the k=7 result being ambiguous. The k=7
result is unambiguous (clean ratify; instability ruled out), so the additional
six k=14 BKZ runs were not performed.
