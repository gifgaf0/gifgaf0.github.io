# E0 reconciliation

*October 19, 2026. Experiment E0 (`seed/PLAN.md` §4, "The hexagon facts, recomputed exactly"). Inputs:*
- *the original run in `seed/experiments/E0_hexagon_exact/`: 102 of 102 checks;*
- *the independent cross-check, round 2, in `crosscheck/` (`xc2_e0.py`): 88 of 88 checks; all 19 headline quantities agree exactly; six issues, all minor.*

*There were no blocking or major issues. Because each minor issue was quick to fix, all six were handled.*

## Summary
- The cross-check was right on all six issues.
- None of them affects a number. They concern:
  - one false sentence in a check title;
  - the verdict vocabulary (CALIBRATED vs CONFIRMED; AMENDED vs CONFIRMED);
  - one citation;
  - consistency of the "cited" qualifiers;
  - four assumptions the original code made without computing them.
- The original `e0_exact.py` was fixed and rerun.
  - 110 of 110 checks pass in 7.5 s on one thread: the original 102, one of them reworded, plus 8 new ones.
  - The 25 `hexagon_check.py` lines are still identical. `exact_replica_output.txt` and `hexagon_check_original_output.txt` are unchanged.
  - `make_figures.py` reproduces `fig_torus_p6m.png` byte for byte (md5 6806a6858883bf29317dcb89dd22d4a3, 163,640 bytes).
- Every value in `results.json` is unchanged except the additions noted below. Only verdict words, sources, notes and evidence text changed.

## Issues

### 1. The 7-vertex search was described too broadly (minor)
- **Issue.** A check title in `results.json` and REPORT Method item 3 said "every 7-vertex triangulated closed surface is an orientable torus".
- **Diagnosis.** The cross-check is right.
  - The search enumerates complexes in which every vertex pair lies in exactly 2 triangles.
  - On V = 7 vertices, 3F = 2E and E <= 21, so chi = 7 - E/3 >= 0, and chi = 0 holds iff E = 21, that is, iff every pair is an edge lying in 2 triangles.
  - So the search is exhaustive for chi = 0 and nothing else. 7-vertex spheres (chi 2) and projective planes (chi 1) exist.
  - The numbers (120 labelled, one orbit, |Aut| = 42, all orientation-preserving) were always right.
- **Action.**
  - Reworded the check: "every 7-vertex triangulated surface with chi = 0 (= every vertex pair in exactly 2 triangles) is an orientable torus, so there is no 7-vertex Klein bottle, and they form one relabelling orbit".
  - Added a decisive check that builds two counterexamples to the old wording:
    - the pentagonal bipyramid: V,E,F = 7,15,10, chi 2, a surface, orientable;
    - the hemi-icosahedron with one triangle subdivided: 7,18,12, chi 1, a surface, non-orientable.
  - `values.torus7_uniqueness` now records the scope and both examples.
  - REPORT Method item 3, Finding 6, the seed-claim evidence and Limitations are reworded.
- **Resolved:** yes.

### 2. CALIBRATED used for seed claims (minor)
- **Issue.** Headline rows whose target is a SEED.md claim carried CALIBRATED.
- **Diagnosis.** The cross-check is right: PLAN §1 reserves CALIBRATED for literature targets.
  - I applied the rule to each row's source column. That gives one difference from the cross-check's suggested list: the p6m row's target is sourced only to SEED §3 and PLAN E0, with no literature source read, so it is CONFIRMED.
  - The quartic row keeps CALIBRATED because its target includes LNR eq. 78 [read], LNR's basis keeps the mirror quartic, and that basis is exactly the flipped copy.
  - This is vocabulary only; the results hold either way.
- **Action.**
  - `calib()` now takes `kind`: "lit" gives CALIBRATED (or MISS); "seed" gives CONFIRMED (or REFUTED).
  - Now CONFIRMED (10 rows): hexagon_check lines, 120 deg turn, Lambda + Zp, V-E+F, K7/Fano/octonion lines, cyclic Fano planes, order 21, orders 168/168, Weyl groups, p6m.
  - Still CALIBRATED (5 rows): quartics, maximal subgroups, PSL(2,7) chi3, F21 chi3, A5 chi3.
  - The REPORT table is split into "Literature targets" and "Seed claims".
- **Resolved:** yes.

### 3. AMENDED on "they don't stack into one clean tower" (minor)
- **Issue.** The original amended the last sentence of §3.
- **Diagnosis.** The cross-check is right.
  - Every factual clause holds as written. F21, PSL(2,7) and the Fano split lie in SU(3), and the G2 turns that complete p6m swap the families.
  - The seed's gloss after the colon is about the family split, and the split indeed survives only up to PSL(2,7).
  - The original's new mathematics also holds. It was recomputed by both sides, and in the new check here kappa, kappa C and kappa C^-1 act as x -> 6x, 3x, 5x:
    - <flipped PSL(2,7), kappa> = PGL(2,7) inside G2;
    - the 180, 300 and 60 deg turns all lie in this PGL(2,7).
  - That is a refinement of the interpretation, not a correction of a fact. Under PLAN §1, "AMENDED: holds only with a correction" does not apply.
- **Action.**
  - Seed-claim verdict AMENDED -> CONFIRMED. The evidence carries the suggested wording: the chain G2 ⊃ SU(3)⋊Z2 ⊃ PGL(2,7) ⊃ PSL(2,7) ⊃ F21 exists, and the family split survives only up to PSL(2,7).
  - Added a check that the 60/180/300 deg G2 turns lie in PGL(2,7).
- **Resolved:** yes.

### 4. Citation for the two S4 classes (minor)
- **Issue.** The target "S4, S4, 7:3" was sourced as "ATLAS; LNR §5 [read]".
- **Diagnosis.** The cross-check is right.
  - I reread LNR (arXiv:0709.1447v2) §5: "PSL2(7) has two maximal subgroups, S4, the order 24 permutation group on four letters, and the order 21 Frobenius group Z7 ⋊ Z3".
  - LNR names the types only and does not say that S4 forms two conjugacy classes.
  - That statement comes from ATLAS, which was not read (it reached us via SEED §9), and from the computation.
- **Action.** The source now reads "ATLAS p.3 (via SEED §9, not read) for the two S4 classes and 7:3; LNR §5 [read] gives only the types S4 and Z7⋊Z3", with a note that the computation establishes the two classes. The seed-claim evidence and the REPORT table are updated.
- **Resolved:** yes.

### 5. Plain CONFIRMED for claims E0 does not compute (minor)
- **Issue.** In `results.json`, "SU(3) is the color group" and "model-builders used both groups" carried a plain CONFIRMED.
- **Diagnosis.** The cross-check is right. The REPORT body already said "CONFIRMED with a cited part", but `results.json` did not match.
- **Action.** Two qualifiers are now used identically in `results.json` and REPORT:
  - "CONFIRMED (cited)": E0 does not compute the claim. This covers the color/eightfold-way group and the model-builders claim.
  - "CONFIRMED (partly cited)": the computed part holds, and a stated remainder is cited. This covers:
    - the Klein quartic's full automorphism group (Hurwitz bound);
    - "only simple subgroup" (classification of finite subgroups of SU(3));
    - G2 ⊃ SU(3) at the group level (Günaydin–Gürsey).
- **Resolved:** yes.

### 6. Unstated assumptions in the original code (minor)
- **Issue.** The original code relied on four facts it did not compute:
  - (a) only 2-generated subgroups were enumerated, with completeness assumed in a comment;
  - (b) PSL(2,7) was identified as "a simple group of order 168";
  - (c) Aut(PSL(2,7)) = PGL(2,7) was inferred from the order 336;
  - (d) the uniqueness argument in Finding 8 used LNR's character table (only 3 and 3bar in degree 3).
- **Diagnosis.** None of these changes a result. All four can be computed cheaply, so they were.
- **Action.** New checks, all passing:
  - (a) The subgroup list is closed under H -> <H, g> for every element g. Every subgroup is reached from {1} by adding elements one at a time, so all 179 subgroups are present.
  - (b, c) Explicit isomorphisms.
    - D, C, Rf -> x+1, 2x, -1/x on P^1(F7), and Dk, C, R likewise. In each case the graph subgroup has order 168 and its image is all of PSL(2,F7).
    - Adding kappa -> -x (non-square determinant) gives a graph of order 336 whose image is all of PGL(2,F7).
    - Still cited: |Aut PSL(2,7)| = 336, used only to call this group "Aut".
  - (d) Degree equation: PSL(2,7) has 6 classes and is perfect (derived subgroup of order 168). Given 1, 3 and 3bar, the remaining degrees d >= 2 dividing 168 with Σ d^2 = 149 are forced to be (6,7,8).
  - Closing the uniqueness argument: |Aut F21| = 42 by a graph test over all images of D and C, and N_PGL(2,7)(F21) has order 42 with trivial centraliser, so every automorphism of F21 is induced inside PGL(2,7). A combined check records that the argument now rests only on computed facts.
- **Resolved:** yes.

## Files changed
- `e0_exact.py`:
  - reworded check;
  - 8 new checks;
  - `calib()` verdict logic;
  - sources, notes and seed-claim verdicts and evidence;
  - docstring runtime.
- `results.json`: regenerated. 110/110 checks, new `values.computed_replacements`, scope fields in `values.torus7_uniqueness`.
- `run_log.txt`: regenerated.
- `REPORT.md`: corrected text with a Reconciliation section, saved by the orchestrator.
- Not touched: `exact_fields.py`, `make_figures.py`, the figure, the replica files, and everything in `crosscheck/` (the other agent's files).

## Final verdicts
- **Headline rows:**
  - CONFIRMED (10): hexagon_check lines 25/25; x -> 4x; Lambda + Zp hexagonal, index 7; 7-21+14 = 0; K7 with two Fano families, one the octonion lines; 2 of 30 cyclic Fano planes; order 21; orders 168, 168; Weyl orders 6 and 12 with the stated actions; G2 affine Weyl group p6m.
  - CALIBRATED (5): quartics; maximal subgroups 8×21, 7×24, 7×24; PSL(2,7) and F21 complex triplets; A5 real triplets.
  - NO_TARGET (4): 7-vertex chi = 0 torus unique and chiral; Der(O) 14 and stabiliser 8; PGL(2,7) of order 336 in G2; 12 of 48 order-7 points.
- **Seed claims:** 20 CONFIRMED, 3 CONFIRMED (partly cited), 2 CONFIRMED (cited). None is AMENDED, REFUTED or OPEN.
- **Open items:** none.
