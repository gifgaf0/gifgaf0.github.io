# E0 cross-check (round 2): the hexagon facts, recomputed a third time

*Independent second computation for experiment E0 (`seed/PLAN.md` §4), run October 19, 2026, after the original's confirmation rerun.*

Before computing and comparing, I read PLAN.md, SEED.md, `hexagon_check.py`, the E0 report, its `results.json` and the round-1 cross-check's write-up. I read the original scripts only afterwards, to audit them. My code is new: `xc2_lib.py` and `xc2_e0.py`. It uses different methods from both the original and the round-1 cross-check (`xc_e0.py`, kept in this folder).

## Verdict: confirmed with corrections (wording, verdict vocabulary, one citation)

All 19 headline quantities agree exactly.
- **My code:** `xc2_e0.py` passes 88 of 88 exact checks in 37 s on one thread.
- **The original, rerun in a scratch copy:** `e0_exact.py` passes 102 of 102 (4.1 s). Its `results.json` is identical apart from runtimes, its replica files are identical, and `make_figures.py` reproduces the figure byte for byte.
- **Round 1, rerun:** `xc_e0.py` passes 81 of 81. Laid out at its expected path, it finds `hexagon_check.py` and passes all checks.

No headline number and no seed verdict is wrong. Six minor issues remain (below). Three of them were already raised in round 1 and are still present after the rerun.

## Methods: how they differ

| part | original E0 | round 1 (`xc_e0.py`) | round 2 (this, `xc2_e0.py`) |
|---|---|---|---|
| Q(zeta7) | hand-written class, basis 1..zeta^5 | Q[Z7] modulo the all-ones vector; also mod 29 and 43 | sympy's `QQ.algebraic_field(exp(2 pi i/7))`, the preregistered route; sympy computes the minimal polynomial |
| group orders | BFS closure of exact matrices | Todd-Coxeter, plus Schreier-Sims on mod-p permutations | exact orbit-stabiliser chain on projective points [e1], [e2], [e3], [1:1:1]: 3 x 7 = 21 and 24 x 7 = 168, with no enumeration |
| identifying PSL(2,7) | "simple of order 168" (cited uniqueness) | presentation | explicit isomorphism onto the Moebius group PSL(2,F7) on P^1(F7), via the conjugation action on the 8 Sylow-7 subgroups |
| classes, characters | Cayley table of the matrix group | mod-p permutation image | classes in the PSL(2,F7) image; traces exact over Q(zeta7) and checked constant on classes; FS = (1/168) Σ chi(g^2) |
| simplicity | normal closures of classes | as original | class equation: no proper union of classes containing 1 has order dividing 168 (or 60) |
| subgroup lattice | closures of all pairs, with "all subgroups are 2-generated" assumed | degree-8 action | 2-generated closures, conjugation-closed, then a join-closure proof that the list is complete |
| A5 | 3-fold about (1,1,1) and 2-fold about an edge midpoint | 72 deg vertex turn and a 2-fold | brute force: every rotation sending an adjacent vertex pair to an adjacent pair and permuting the 12 vertices gives exactly 60 = 12 x 5 |
| Weyl / affine Weyl | Fractions in R^3 | integer 2x2 matrices, grid search | integer 2x2 matrices in Lambda coordinates; W(G2) = Aut(Lambda); my own G2 base (a1 = e2 - (1,1,1)/3, theta = (1,0,-1)); centres from (1-w)x = t (the same idea as the original) |
| triangulation, Fano | lattice basis (p, tp) | own | integer enumeration of Lambda + Zp; Fano planes by Steiner-triple-system backtracking; automorphisms by brute force over S7 |
| octonions | C + C^3 with basis {1, i sqrt7, ...} | Fano-table model | Cayley-Dickson doubling of the quaternions for Der(O); the report's C + C^3 model rechecked over Q(i) |
| PGL(2,7) | order 336 together with |Aut PSL(2,7)| = 336 (cited) | as original | kappa's action, transported to P^1(F7), is a Moebius map of non-square determinant, so <PSL, kappa> = PGL(2,F7) explicitly |

## Agreement table

| quantity | original | round 2 | agree |
|---|---|---|---|
| hexagon_check.py lines | 25/25 identical | 25/25 identical (rebuilt from my values) | yes |
| 120 deg turn | x -> 4x | x -> 4x (C^-1 D C = D^4; the 240 deg turn gives 2x) | yes |
| Lambda + Zp | hexagonal, index 7, 6 shortest vectors | min norm^2 2/7 attained by exactly 6 vectors; index 7; reduced Gram hexagonal | yes |
| V - E + F | 7 - 21 + 14 = 0 | 7 - 21 + 14 = 0; 6-cycle links; orientable | yes |
| K7, Fano families, octonion lines | yes; 'down' = {i,i+1,i+3} | yes; {i,i+1,i+3} and {i,i+2,i+3} | yes |
| cyclic Fano planes | 2 of 30 | 2 of 30; Aut 168, 168; intersection 21 | yes |
| order of <D,C> | 21 | 21 (orbit-stabiliser) | yes |
| Klein's copy / flipped copy | 168, 168 | 168, 168; flipped copy = flip(Klein)flip^-1 = LNR's <A,B> | yes |
| quartics | both invariant | both invariant (exact, generators and all 168 elements) | yes |
| maximal subgroups | 8 x 21, 7 x 24, 7 x 24 | the same; 179 subgroups in 15 classes, proven complete | yes |
| PSL(2,7) chi_3 | 3, -1, 0, 1, b7, b7bar; FS 0 | the same, both copies | yes |
| F21 chi_3 | 3, 0, 0, b7, b7bar; FS 0 | the same | yes |
| A5 chi_3, chi_3' | 3, -1, 0, (1 ± sqrt5)/2; FS +1 | the same; every element is conjugate to its inverse | yes |
| Weyl groups | orders 6, 12; turns 4x, 2x / 5x, 6x, 3x; mirrors keeping the points 0/3, 0/6 | identical | yes |
| G2 affine Weyl group | (2,3,6); 6mm + 2 × 3m + 3 × 2mm: p6m | the same; SU(3): 3 × 3m (p3m1) | yes |
| 7-vertex torus | 120, one orbit, Aut 42, chiral | the same; Aut = AGL(1,7) | yes |
| Der(O) / Stab(e) | 14 / 8 | 14 / 8 | yes |
| <PSL(2,7), kappa> | 336 = PGL(2,7) | 336 = PGL(2,F7) explicitly; swaps the S4 classes; the S4 classes give the two families | yes |
| order-7 points with hexagonal L' | 12 of 48 | 12 of 48 | yes |

**During development:** one of my checks failed (S4 classes to Fano families). The cause was an operator-precedence bug in my own code: a string suffix was attached to the wrong branch of a conditional expression. It is fixed; it was not a disagreement with the original.

## Closing the uniqueness argument of Finding 8

The report says the PSL(2,7) in U(3) that contains <D, C> is unique. It sketches the argument and takes "the only triplets are 3 and 3bar" from LNR. My section K computes the missing pieces:
- |Aut(F21)| = 42, by brute force over generator images.
- N_PGL(2,7)(F21) has order 42 and centralises only the identity, so every automorphism of F21 extends to an automorphism of PSL(2,7).
- The degree equation 1 + 9 + 9 + a² + b² + c² = 168, with every degree dividing 168, has only the solution (6, 7, 8). So the only triplets are 3 and 3bar.

With these, the argument closes:
1. Any PSL(2,7) in U(3) containing F21 can be adjusted by an automorphism so that it agrees with the flipped copy on F21.
2. Its 3-dim representation then has the same character, because chi(D) = b7 ≠ b7bar.
3. So the two representations are conjugate by a matrix commuting with the irreducible F21. By Schur's lemma that matrix is scalar, and the images coincide.

The claim is supported.

## Audit of the report

- **Numbers:** every number in REPORT.md matches `results.json` and my values. The rerun's declared fixes (calibration-table columns, the A5 source string, the docstring runtime, the regenerated run log) are present.
- **Figure:** `fig_torus_p6m.png` exists (163,640 bytes, under the 300 KB limit). Its labels sit at (j/7, 3j/7) mod 1, and the blue triangles are {i,i+1,i+3}.
- **LNR (arXiv:0709.1447v2), read myself:**
  - eq. (13): b7 = (-1+i√7)/2;
  - eq. (16): AB = diag(η, η², η⁴);
  - eqs. (22) and (23): A and B. I rebuilt both exactly; A = Rf, AB = D, and A² = B³ = (AB)⁷ = [A,B]⁴ = 1;
  - eq. (78): the mirror quartic;
  - §2: A5 has "five real irreducible representations, two of which are triplets";
  - §5: the Z7⋊Z3 table.
- **Original code:**
  - The octonion check uses the real basis {1, i√7, e_k, i√7 e_k} inside Q(zeta7). That is a legitimate R-basis, and the 64-pair automorphism checks are complete because the maps are R-linear.
  - The 36 × 36 polarisation check of N(xy) = N(x)N(y) is complete.
  - The replica lines are generated from the exact results, not hard-coded.

### Issues (all minor)

1. **A check title is false as worded.** `results.json` says "every 7-vertex triangulated closed surface is an orientable torus", and REPORT Method item 3 echoes it. The search covers only complexes in which every vertex pair lies in exactly 2 triangles, which is the chi = 0 case. 7-vertex triangulations of the sphere and of RP² exist; `xc2_e0.py` builds both. The numbers are right. This was raised in round 1 and is still unfixed.
   **Fix:** say "every 7-vertex triangulated surface with chi = 0 is an orientable torus (no 7-vertex Klein bottle)".
2. **CALIBRATED is used for seed-sourced targets.** Examples are x -> 4x, |<D,C>| = 21 and the Weyl turns, all with source "SEED §3". PLAN §1 reserves CALIBRATED for literature targets, so these rows should read CONFIRMED. Unfixed since round 1.
3. **AMENDED on "they don't stack into one clean tower" is interpretive.**
   - Every factual clause of the seed sentence holds.
   - The proposed chain G2 ⊃ SU(3)⋊Z2 ⊃ PGL(2,7) ⊃ PSL(2,7) ⊃ F21 is correct and verified here.
   - But its top steps (kappa, PGL(2,7)) swap the Fano families, which is exactly the seed's point.

   **Fix:** record "facts CONFIRMED; wording refinement suggested", and keep the chain with the note that the family split survives only up to PSL(2,7).
4. **Citation.** "S4, S4, 7:3" is sourced as "ATLAS; LNR §5 [read]". LNR §5 names only the isomorphism types. The two S4 conjugacy classes rest on ATLAS, which was not read; the computation itself shows them.
5. **Background claims carry a plain CONFIRMED in `results.json`.** These are "SU(3) is the color group" and "model-builders used both groups". E0 does not test them; the report body correctly says "CONFIRMED with a cited part".
6. **Unstated assumptions in the original code** (no result affected):
   - the subgroup lattice is built from 2-generated subgroups only, with completeness assumed in a comment;
   - PSL(2,7) is identified as "the simple group of order 168";
   - PGL(2,7) is identified through |Aut| = 336;
   - the Finding 8 uniqueness relies on LNR's character table.

   This cross-check supplies each by computation: join closure, explicit isomorphisms onto PSL(2,F7) and PGL(2,F7), and section K.

### Seed verdicts

I agree with every E0 verdict except the framing of the one AMENDED verdict (issue 3). That includes:
- the claim that Klein's copy contains Dk and not D. It follows from the quartic x³y + y³z + z³x alone: its diagonal symmetries in SU(3) are exactly the powers of Dk, and diag(z, z⁴, z²) = Dk² is among them;
- the claim that SEED's 120 deg turn is x -> 4x. This is a direction convention shared with `hexagon_check.py`; the opposite turn gives 2x.

The "only simple subgroups of SU(3)" part still rests on the 1916 classification via LNR, as the report says.

## Files (`seed/experiments/E0_hexagon_exact/crosscheck/`)

- **Round 2 (this):**
  - `xc2_lib.py`: sympy Q(zeta7) helpers, the projective orbit-stabiliser chain, permutation tools, PSL(2,F7), Q(sqrt5), exact linear algebra.
  - `xc2_e0.py`: all 88 checks; writes `xc2_checks.json` and `xc2_replica_lines.txt`.
  - `xc2_run_log.txt`: the transcript.
  - `make_crosscheck2_json.py`: builds `crosscheck.json`, comparing `xc2_checks.json` with `../results.json` field by field.
- **Round 1 (kept):**
  - `xc_lib.py`, `xc_e0.py`, `xc_checks.json`, `xc_run_log.txt`, `xc_replica_lines.txt`.
  - Its generator `make_crosscheck_json.py` now writes `crosscheck_round1.json`, which keeps the round-1 record.

## How to reproduce

    cd seed/experiments/E0_hexagon_exact/crosscheck
    NUMBA_NUM_THREADS=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 xc2_e0.py > xc2_run_log.txt   # ~40 s, exit 0 iff all 88 pass
    python3 make_crosscheck2_json.py
