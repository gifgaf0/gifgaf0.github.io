# E0 cross-check: the hexagon facts, recomputed a second time

*Independent second computation for experiment E0 (`seed/PLAN.md` §4), run October 19, 2026. Before computing and comparing, I read only PLAN.md, SEED.md, `hexagon_check.py`, the E0 report and its `results.json`. I read the original scripts afterwards, only to audit them.*

## Verdict: confirmed with corrections (wording only)

I recomputed all 19 headline quantities with separate code, mostly by different methods, and all 19 agree exactly. My script passes 81 of 81 checks (11.7 s, one thread).

I also reran the original `e0_exact.py` in a scratch copy:
- it passes 102 of 102 checks;
- its `results.json` is identical to the stored one apart from runtimes;
- `make_figures.py` reproduces the figure byte for byte.

No headline number and no seed verdict is wrong. There are five minor issues: one wrong sentence in a check title, two places where the verdict wording overstates, and two citation or labelling points.

## Methods: how they differ from the original

| part | original E0 | this cross-check |
|---|---|---|
| Q(zeta7) | 6-dim basis 1..zeta^5 | the group algebra Q[Z7] modulo the all-ones vector (basis zeta..zeta^6); also reduction mod p = 29 and 43 |
| group orders | BFS closure of exact matrices | Todd-Coxeter on a presentation (upper bound) with the relations checked exactly; Schreier-Sims (my own) on mod-p permutation images |
| classes, characters | classes of the exact matrix group | classes in the mod-p permutation image; traces of class representatives evaluated exactly; all 168 traces checked to be constant on classes |
| maximality of F21 | <F21, g> for 147 elements g; subgroup lattice | primitivity (2-transitivity on 8 cosets); lattice in the faithful degree-8 action; brute force as well |
| PSL(2,7) generators | Klein's R, Dk, C and the flipped copy | LNR's A, B from eqs. (22) and (23), which I read in the PDF myself; exact words linking them to D, C, Rf |
| A5 | 3-fold about (1,1,1), 2-fold about an edge midpoint | 72 deg turn about vertex (0,1,phi) (built from the axis-angle formula), 2-fold about z |
| Weyl / affine Weyl | Fractions in R^3 | integer 2x2 matrices in the basis b1, b2 of Lambda; my own G2 base (alpha1 = (-2,1,1)/3, theta = (0,-1,1)); exhaustive search for rotation centres on a 1/12 grid |
| octonions | C + C^3 model | Der(O) computed in the Fano-table model e_i e_{i+1} = e_{i+3}; the C + C^3 product checked symbolically (sympy: unital, alternative, N(xy) = N(x)N(y)) |
| 25 lines | regenerated from exact results | regenerated from my own values, then compared with a fresh run of hexagon_check.py |

## Agreement table

| quantity | original | cross-check | agree |
|---|---|---|---|
| hexagon_check.py lines | 25/25 identical | 25/25 identical | yes |
| 120 deg turn | x -> 4x | x -> 4x (C^-1 D C = D^4; the 240 deg turn gives 2x) | yes |
| Lambda + Zp | hexagonal, index 7, 6 shortest vectors | min norm^2 2/7, exactly 6 vectors, index 7 | yes |
| V - E + F | 7 - 21 + 14 = 0 | 7 - 21 + 14 = 0; 6-cycle links; orientable | yes |
| K7, Fano families, octonion lines | yes | yes; {i,i+1,i+3} and {i,i+2,i+3} | yes |
| cyclic Fano planes | 2 of 30 | 2 of 30 (7!/168 = 30), = the two families | yes |
| order of <D,C> | 21 | 21 (Todd-Coxeter; Schreier-Sims mod 29 and 43) | yes |
| Klein's copy / flipped copy | 168, 168 | 168, 168 (LNR presentation with Todd-Coxeter; Schreier-Sims) | yes |
| quartic invariance | both | both (exact, under the generators) | yes |
| maximal subgroups | 8 x 21, 7 x 24, 7 x 24 | 8 x 21, 7 x 24, 7 x 24; 179 subgroups in 15 classes; N(F21) = F21 | yes |
| PSL(2,7) chi_3 | 3, -1, 0, 1, b7, b7bar; FS 0 | the same, on classes 1, 21, 56, 42, 24, 24 | yes |
| F21 chi_3 | 3, 0, 0, b7, b7bar; FS 0 | the same | yes |
| A5 chi_3, chi_3' | 3, -1, 0, (1 ± sqrt5)/2; FS +1 | the same; other degrees forced to be (4,5) | yes |
| Weyl groups | orders 6, 12; turn actions; mirrors keeping the points 0/3, 0/6 | identical | yes |
| G2 affine Weyl group | (2,3,6); 6mm + 2 × 3m + 3 × 2mm: p6m | the same; SU(3): 3 × 3m = p3m1 | yes |
| 7-vertex torus | 120 labelled, one orbit, Aut 42, chiral | 120 simple 2-(7,3,2) designs, all tori, one orbit; Aut = AGL(1,7), 42/42 orientation-preserving | yes |
| Der(O) / Stab(e) | 14 / 8 | 14 / 8 (Fano-table model) | yes |
| <PSL(2,7), kappa> | 336 = PGL(2,7) | 336: kappa is an automorphism of O, conj(D) = D^6 lies in the other class (outer), and kappa swaps the S4 classes | yes |
| order-7 points with hexagonal L' | 12 of 48 | 12 of 48 (subgroups of D and of diag(z,z^4,z^2)) | yes |

**During development:** two checks in my own script failed. Both were bugs on my side, not in the original, and both are fixed:
- I counted each oriented triangle three times when testing orientability.
- My first "5-fold" matrix was orthogonal and of order 5, and it did generate a group of order 60, but it was not a symmetry of the icosahedron (0, ±1, ±phi). I replaced it with the 72 deg rotation about a vertex, built from the axis-angle formula.

## Audit of the report

Everything numeric in REPORT.md matches `results.json` and my values. The figure exists (163,640 bytes); its point labels match the computed positions (j/7, 3j/7) mod 1 in Lambda coordinates. On the literature side, I read LNR (arXiv:0709.1447v2) myself:
- eq. (13): b7 = (-1+i√7)/2;
- eq. (16): AB = diag(η, η², η⁴);
- eqs. (22) and (23): the B and A matrices, which satisfy all relations exactly, with A = Rf;
- eq. (78): the mirror quartic;
- §2: A5 has "five real irreducible representations, two of which are triplets";
- §5: the Z7⋊Z3 table with b7.

The original's claim that the 36 × 36 polarisation points give a complete check of N(xy) = N(x)N(y) is right: a quadratic form on R^8 is fixed by its values at e_i and e_i + e_j. The changes in the confirmation rerun (git diff) match the four fixes it declares.

### Issues

1. **(minor) One check title is false as worded.** `results.json` and REPORT Method item 3 say "every 7-vertex triangulated closed surface is an orientable torus". 7-vertex triangulations of the sphere (pentagonal bipyramid, chi 2) and of RP² (chi 1) exist; `xc_e0.py` checks both. The search only covered complexes in which every vertex pair lies in exactly two triangles (chi = 0). The numbers 120, one orbit and |Aut| = 42 are correct.
   **Fix:** say "every 7-vertex triangulated surface with chi = 0".
2. **(minor) The AMENDED verdict on the tower sentence targets an interpretation, not a fact.**
   - Every factual clause of the sentence holds as written: F21, PSL(2,7) and the Fano split sit on the SU(3) rung, and the G2 turns that complete p6m swap the families.
   - kappa, and therefore PGL(2,7), also swaps the families.
   - The amendment's mathematics is verified: kappa normalises the flipped PSL(2,7) as an outer automorphism, and kappa lies in G2.

   **Fix:** record it as "facts CONFIRMED; wording AMENDED (interpretive)". Keep the chain G2 ⊃ SU(3)⋊Z2 ⊃ PGL(2,7) ⊃ PSL(2,7) ⊃ F21, noting that the family split survives only up to PSL(2,7).
3. **(minor) CALIBRATED is used for seed-sourced rows.** Examples are the order of <D,C>, x -> 4x and the Weyl turns, all with target source "SEED §3". PLAN §1 defines CALIBRATED as matching a literature target; these are CONFIRMED seed claims, and they appear again as CONFIRMED in `seed_claims`.
4. **(minor) Citation for the two S4 classes.** The target "S4, S4, 7:3" is cited as "ATLAS; LNR §5 [read]". LNR §5 lists only the two isomorphism types (S4 and Z7⋊Z3). The two conjugacy classes of S4 rest on ATLAS, which was not read. The computation itself shows the two classes.
5. **(minor) Cited claims carry a plain CONFIRMED in `results.json`.** The background and literature-only claims (SU(3) as the color group; model-builders using both groups) are not computed. The report body handles them correctly ("CONFIRMED with a cited part").

### Seed verdicts

I agree with every E0 verdict except the framing of the one AMENDED verdict (issue 2). That includes the claim that Klein's copy contains Dk and not D, which follows from Klein's quartic x³y + y³z + z³x alone: its only order-7 diagonal symmetries are the powers of Dk. One attribution point worth recording: LNR describe their A, which equals Rf rather than hexagon_check's R, as "reproducing Klein's involution". That is consistent with the report's reading that "Klein's own copy" is a coordinate-labelling convention.

## Files (`seed/experiments/E0_hexagon_exact/crosscheck/`)

- `xc_lib.py`: Q[Z7] field, Q(sqrt5), mod-p permutation representations, Schreier-Sims, Todd-Coxeter.
- `xc_e0.py`: all 81 checks; writes `xc_checks.json` and `xc_replica_lines.txt`.
- `xc_run_log.txt`: the transcript.
- `make_crosscheck_json.py`: builds `crosscheck.json` from `xc_checks.json` and the original `results.json`.
- `crosscheck.json`: agreement table, claim audit, issues, verdict.

## How to reproduce

    cd seed/experiments/E0_hexagon_exact/crosscheck
    NUMBA_NUM_THREADS=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 xc_e0.py > xc_run_log.txt   # ~12 s, exit 0 iff all pass
    python3 make_crosscheck_json.py
