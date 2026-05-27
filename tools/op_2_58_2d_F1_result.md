# OP-2.58.2d Item F1 — signed-lift discrimination test result

**Date:** May 27, 2026
**Brief:** CLAUDE_CODE_BRIEF_08 §3 (Item F1)
**Status:** Pre-freeze. Toy scale q=911, seed 20260527, N=500. No §2.58.B execution.
**Feeds:** the §3.3 placeholder replacement (the load-bearing pre-freeze edit).
**Inputs:** `op_2_58_2d_classifier_no_lift.py`, `op_2_58_2d_F1_signed_lift_test.py`.

---

## 1. Instrumentation — signed-lift was actually disabled (§3.1 / §3.3)

Disable-path validation on a candidate of large residues near q:

```
candidate (first 5)        : [910, 909, 908, 907, 906]
after lift ON  (production): [-1.0, -2.0, -3.0, -4.0, -5.0]
after lift OFF (disabled)  : [910.0, 909.0, 908.0, 907.0, 906.0]
disabled keeps ≥ q-5 (+910): True
production centres to neg  : True
DISABLE PATH VALID         : True
```

A residue of 910 (= −1 centred) reaches the Euclidean projection as **+910**
under the disabled lift, confirming the lift is off, and as **−1** under the
production lift. `_lift` is the classifier's sole centring entry point
(`fano_ratios`/`pair_ratios` → `_lift`; `classify` → those), so there is no
sibling path that re-applies the lift. The disable path is valid; the recovery
rates below are meaningful.

## 2. The 4-number matrix (§3.2 unattributable branch)

| classifier | with lift | without lift |
|---|---|---|
| **pair** | **96.2%** | **41.8%** |
| **line** | **88.0%** | **89.6%** |

Chance: pair 1/21 = 4.76%, line 1/7 = 14.29%. N = 500, seed 20260527.

The with-lift figures **reproduce the Brief-07 prefreeze report baseline
exactly** (96.2% pair, 88.0% line), confirming the harness matches the
commit-`766c6f5` Path B protocol.

## 3. L1 attribution (cited)

Per `op_2_58_2d_L1_attribution_note.md`: L1 resolves as **unattributable —
indeed unlocatable.** The §2.66.2 source, the SQT master ledger, and the
Phase-B audit log are all absent from the repo and its full git history; the
65.4%/93.0% numbers survive only as uncaptioned reference data. The F1
interpretation therefore follows the §3.2 **"unattributable"** branch.

## 4. Interpretation

§3.2 unattributable branch: "whichever metric drops to a number near 65.4% on
disable identifies which §2.66.2 number was which classifier, and
simultaneously confirms possibility (a). If neither drops to ~65%, possibility
(a) is ruled out for both classifiers and the F1 closure language is the (b/c)
variant."

- **Pair:** 96.2% → **41.8%** — a large drop, but **below** 65.4% and 23.6 pp
  away from it. Does not identify the pair classifier with the 65.4% number.
- **Line:** 88.0% → **89.6%** — essentially unchanged (robust to the lift);
  nowhere near 65.4%.

**Neither metric lands near 65.4% under disabled signed-lift.** Possibility (a)
(signed-lift was the §2.66.2 bug that produced 65.4%) is therefore **ruled out
for both classifiers.** This is consistent with — and independent of — the L1
"unattributable" resolution, which already selects (b/c). Both lines of
evidence converge on the (b/c) closure.

## 5. SELECTED F1 CLOSURE PARAGRAPH — §3.3 replacement string

This is the verbatim text that replaces the
`[PLACEHOLDER — PENDING SIGNED-LIFT DISCRIMINATION TEST]` paragraph in §3.3 of
the pre-registration. **Nothing else in the pre-registration is changed by this
brief's F1 edit.**

> The reconstruction implements the projection-ratio specification of §2.66.2
> but is not bit-exact with the §2.66.2 reference; bit-exactness is unverifiable
> due to source absence; the σ-statistics of §3.2 are computed against the
> reconstruction's own baseline established at the §3.1 secondary-run validation
> gate.

### Supplementary note appended to the §3.3 patch (not part of the paragraph)

Per §3.5, because L1 resolved unattributable the (b/c) paragraph is selected and
the disable-test 4-number matrix is appended as a supplementary note:

> F1 signed-lift discrimination (q=911, N=500, seed 20260527): pair recovery
> 96.2% (lift on) / 41.8% (lift off); line recovery 88.0% (lift on) / 89.6%
> (lift off). Neither metric approaches the §2.66.2 65.4% figure under disabled
> lift, so the "signed-lift was the §2.66.2 bug" possibility (a) is ruled out;
> the pair classifier depends on the signed-lift (collapses without it) while
> the line classifier does not.

## 6. SNR consequence (§3.6)

Outcome (b/c) is selected, **not** (a). Per brief §3.6: "If outcome (b/c) is
selected, no SNR consequence; the target stands." The §3.1 secondary-run target
SNR ≈ 0.0025 within 10% relative error is unaffected by this brief.

## 7. Sideband observation (not in the closure paragraph; brief §7)

The line classifier is robust to disabling the signed-lift (88.0% → 89.6%)
while the pair classifier collapses (96.2% → 41.8%). The 8D overlapping F_L
projection tolerates the +910 common-mode distortion that destroys the 4D
pair-kernel projection. This is a structural observation about the classifier,
recorded here as a sideband finding; it is **not** folded into the §3.3 closure
language.

---

## Marker

**This file's §5 paragraph is the §3.3 placeholder replacement string, plus its
§5 supplementary note. No other part of the OP-2.58.2d pre-registration is
modified by Item F1.**
