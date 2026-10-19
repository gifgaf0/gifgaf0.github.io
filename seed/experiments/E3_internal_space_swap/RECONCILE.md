# E3 reconciliation

**Scope.** E3, swapping the internal space: G2 and SU(3)/T² (SEED.md §7.2; PLAN.md §4 E3).

**Inputs**
- The original run: `REPORT.md`, `results.json` and the scripts in `seed/experiments/E3_internal_space_swap/`.
- The independent cross-check in `crosscheck/` (`CROSSCHECK.md`, `crosscheck.json`, `cc_*.py`). Its verdict was "confirmed": 61 of 61 compared quantities agree, and it raised 8 issues, all minor.

**Method**
- Read both codes for every issue.
- Re-read Mayanskiy arXiv:1611.04070 §4 myself: fetched from the public arXiv mirror on GCS and converted with pdftotext into scratch, outside the repo.
- Settled the stability-table question with a new script that uses the original Ritz machinery: `reconcile_stability_r40.py`.
- Fixed `make_results.py` and `run_all.sh`, then ran `run_all.sh` once from scratch, end to end.
- Compared every regenerated output with a backup of the originals.
- Re-ran the cross-check's comparison script `cc_summary.py` against the new `results.json`, in a scratch copy, so `crosscheck/` was not modified.

**Outcome**
- The cross-check was right on all 8 issues.
- On one detail it was imprecise. In the original basis the unresolved 3.73e-4 triplet is not specifically the iso-rotation triplet: both Ritz zero-mode triplets mix translation and iso-rotation character.
- The same check found a second instance of the same ordering problem, which the cross-check had not flagged: the R = 20, nr = 15 refinement row.
- All issues are resolved. No original number changed, and no seed verdict changed.
- One seed row was split into two:
  - π₃(G2) = ℤ with the long-root hedgehog as a generator: CONFIRMED;
  - that hedgehog being the minimal-energy B = 1 configuration: OPEN.
- One AMENDED, attached to a PLAN note rather than a seed claim, was withdrawn.

## Issues

| # | issue (from the cross-check) | who was right | diagnosis | action | resolved |
|---|---|---|---|---|---|
| 1 | Verdict vocabulary: seed predictions and PLAN expectations labelled CALIBRATED | cross-check | PLAN §1 reserves CALIBRATED for literature targets. `make_results.py` hard-coded CALIBRATED for every passing row, including the rotor ladder, integer J, 7 branching, C₂, inertia blocks, moment map, π₂ and π₃ | `make_results.py` derives each verdict from its check through `cal()`, `conf()` and `chk()`. CALIBRATED: Mayanskiy indices and 14 branching, M_cl, Λ, I₂. CONFIRMED: inertia blocks, rotor ladder, integer J, moment map, π₂, π₃. CHECK PASSED: 7 branching, C₂ values, virial, su(3)-in-G2 trace normalisation, and the two no-negative-mode stability rows (formerly NO_TARGET). The cross-check suggested CONFIRMED for the 7 branching and C₂; I used CHECK PASSED because they are derived representation theory, neither a seed claim nor a literature target | yes |
| 2 | Stability table, (3,1) at R = 40, nr = 40: 1.94e-4 (×3) is continuum, not a zero mode | cross-check (one detail imprecise) | New `reconcile_stability_r40.py` projects each Ritz eigenvector onto the six exact zero modes. At R = 40, nr = 40 the zero-mode content is 0.994 (5.42e-5), 0.003 (1.94e-4) and 0.581 (3.73e-4). So 1.94e-4 is the first continuum level ((1/32)(π/40)² = 1.93e-4), lying between the two zero-mode triplets. At nr = 80 the zero-mode triplets drop to 1.62e-5 and 1.23e-4, while the continuum level stays put (1.9388e-4 → 1.9409e-4). The detail: the cross-check called 3.73e-4 "the unresolved iso-rotation triplet". In the original's linear-hat basis both triplets mix translation and iso-rotation character (32/68% and 39/19%), because the exact modes have opposite hedgehog parity and the basis is not parity invariant. The same check shows the R = 20, nr = 15 refinement row had the same problem: 7.93e-4 is continuum (content 0.056) and the second zero-mode triplet is at 1.11e-3 (content 0.86). The report's "7.9e-4 → 6.3e-5" should have read "1.11e-3 → 6.3e-5" | Stability table relabelled. Level-assignment table added. Refinement sentence corrected. Notes in `results.json` corrected. `reconcile_stability_r40.json` written. The script was added to `run_all.sh` | yes |
| 3 | "The centre element exp(2πT₃ᴸ)"; G2 has trivial centre | cross-check | It is the image of −1 ∈ SU(2)_L, central in SO(4) = (SU(2)_L×SU(2)_S)/ℤ₂ only. The code comment in `e3_g2_algebra.py` ("the centre of SU(2)_long") is correct and was left alone | Report wording corrected. The `results.json` note says it explicitly | yes |
| 4 | The "character of the stabiliser" argument does not exclude an SU(2)_short-invariant velocity-linear term along (3,1); AMENDED applied to a PLAN note | cross-check | Stabiliser invariance kills the su(2)_short part of c and forces the rest to be Ad(SU(2)_short)-invariant, i.e. to lie in su(2)_long. Spatial rotation equals right SU(2)_long (grand spin), and the adjoint of su(2) has no invariant vector, so c = 0. In SU(3) the same argument leaves exactly the U(1)_Y character, which is the WZ term's slot. PLAN §3 item 5 is a literature-check note, not a seed claim, so AMENDED is the wrong word | Findings §4 rewritten with the three-step argument. The PLAN §3.5 row reads "no verdict word (PLAN note); refined". It also states that E3 did not compute H⁵ itself | yes |
| 5 | Mayanskiy citation: indices 1 and 3 are not in Table 2 | cross-check | Verified in the PDF (v1, §4, p. 17). Table 2 ("Semisimple non-regular subalgebras") lists only A₁⁴ and A₁²⁸. The complete list after it reads "A₂, A₁ + Ã₁, A₁ = A₁¹, Ã₁ = A₁³, A₁⁴, A₁²⁸". Prop. 4.1 gives D½ ⊗ D3/2 for A₁ + Ã₁ and D₅ for A₁²⁸, as cited | Calibration table and `results.json` source strings now cite "§4: Table 2 (A₁⁴, A₁²⁸) and the list after it (A₁¹, A₁³)" | yes |
| 6 | "E2 parameters" are PLAN's rounded ANW point (129, 5.45), not E2's fit (129.26, 5.444) | cross-check | A declared deviation, but the wording implied E2's own fit. E2's fit is F_π = 129.2627 MeV, e = 5.443985 (E2 `results.json`) | `make_results.py` reads E2's fit and writes `parameter_point_E2_fit` with the first 10 levels. The report gets a new column: M = 865.75 MeV, 1/I₁ = 195.33, 1/I₂ = 512.69 MeV, 14–1 gap 708.0 MeV instead of 708.9; every level within 0.31%. The text says "PLAN's rounded ANW point" throughout | yes |
| 7 | `run_all.sh` never run end to end; the 27 min is a sum of step times | cross-check | `logs/run_all.log` was a SKIP_DONE resume that skipped the first five steps and never ran `e3_stability_refine` (that step and `make_results` ran separately). `run_all.sh` also ignored a `make_results` failure | `run_all.sh`: the reconcile step was added and a `make_results` failure is now fatal. Run once from scratch with 1 thread, all `.done` markers removed: exit 0, total wall 1710 s (28.5 min). Step times: algebra < 1 s, hedgehog 60 s, inertia 43 s, reps 2 s, branching < 1 s, stability 333 s, refine 227 s, reconcile_stability_r40 201 s, flag 843 s, make_results 1 s. This was on a shared 4-core machine with other jobs running; the original steps summed to about 27 min | yes |
| 8 | Seed row "the B = 1 fold is the long-root hedgehog: CONFIRMED" needs a global-minimality qualifier | cross-check | The evidence is B = 1 (a generator of π₃) and local linear stability. Minimality in the B = 1 sector was never tested | Split into two rows: "π₃(G2) = ℤ, generated by the long-root hedgehog: CONFIRMED" and "it is the minimal-energy B = 1 configuration in G2: OPEN". Findings §1 and §5 say the same | yes |

**Also carried over.** The E2 reconciliation established, from the sources, that the M_cl target's "[read]" label is overstated:
- 36.5 F_π/e is ANW's own value;
- Schechter–Weigel give 36.44 F_π/e;
- 1.2315 × 3π² is the standard form, not a value read in the cited texts.

E3 reused that target, so its provenance note was corrected too. M_cl passes against all three values: −0.004%, −0.11% and +0.05%.

## Literature checked

- **Mayanskiy, arXiv:1611.04070v1, §4** (pdftotext of the GCS mirror PDF):
  - Table 2 lists A₁⁴ and A₁²⁸ with explicit sl₂ triples.
  - The sentence after it gives the complete list of semisimple subalgebras: "A₂, A₁ + Ã₁, A₁ = A₁¹, Ã₁ = A₁³, A₁⁴, A₁²⁸".
  - Prop. 4.1:
    - A₁ + Ã₁: W = D½ ⊗ D3/2, so 14 = (3,1)+(1,3)+(2,4);
    - A₁²⁸: 14 = D₁ + D₅;
    - A₁⁴: 14 = D₁ + D₁ + D₁ + D₂;
    - Ã₁ = A₁³: 14 = D₁ + 2 D3/2 + 3 D₀.

## Number changes

None of the original numbers changed. The fresh end-to-end run reproduces every original output:
- `algebra_results.json`, `hedgehog_results.json`, `inertia_results.json`, `reps_results.json`, `su3_branching_results.json`, `stability_results.json`, `stability_refine_results.json` and `flag_results.json`: every number and string identical. Only `runtime_s` differs.
- `g2_basis.npz`, `profile_e3.npz`, `fig_moment_map.png` and `fig_g2_spectrum.png`: byte-identical.
- `results.json`: all 17 original headline values and targets are identical; only verdict words, notes and sources changed. The only numbers that changed are on the E2 side of the profile comparison: E2's C (+4.5e-10, from E2's own reconciliation), and Λ and J₂ (1.3e-14).
- A second `make_results.py` run on the same inputs gives a byte-identical `results.json`.

New numbers:
- the (3,1) level assignment at R = 20 (nr = 15, 30) and R = 40 (nr = 40, 80);
- the ladder at E2's own fit;
- the E2 side of the profile comparison. E2's reconciliation moved its stored C by 4.5e-10, so the C comparison now reads 8.638578218067 vs 8.638578218219 (1.8e-11).

## Files changed

All in `seed/experiments/E3_internal_space_swap/`.

- **Scripts:**
  - `make_results.py`: verdict words derived from checks, notes, sources, the E2-fit point, `seed_claims`, `reconciliation` and `stability_R40_assignment`;
  - `run_all.sh`: new step, fatal `make_results`;
  - new `reconcile_stability_r40.py`.
- **Regenerated by the end-to-end rerun:**
  - all `*_results.json`, `g2_basis.npz`, `profile_e3.npz`, `fig_moment_map.png`, `fig_g2_spectrum.png` and `logs/`;
  - `results.json`;
  - new `reconcile_stability_r40.json`.
- **REPORT.md:** corrected text (returned to the orchestrator) with a Reconciliation section.
- **Not touched:** `crosscheck/` and every other experiment.
- **Backup:** the originals are in `/tmp/claude-0/-home-user-gifgaf0-github-io/235fe351-6f97-5895-b3fd-a90496179b3c/scratchpad/e3rec/orig/` (session scratchpad, outside the repo).

## Final consistency

- `run_all.sh`: exit 0, total wall 1710 s (28.5 min). Step times: algebra < 1 s, hedgehog 60 s, inertia 43 s, reps 2 s, branching < 1 s, stability 333 s, refine 227 s, reconcile_stability_r40 201 s, flag 843 s, make_results 1 s. This was on a shared 4-core machine with other jobs running; the original steps summed to about 27 min.
- `reconcile_stability_r40.py`: all checks pass.
- The cross-check's comparison script, re-run on the new `results.json` in a scratch copy: 61 of 61 agree. Its comparison lines are identical to `crosscheck/cc_summary.log`.
- The report's headline numbers, the `results.json` headline, `seed_claims`, and the verdicts agree with each other.
- Verdicts:
  - **CALIBRATED:** Dynkin indices 1, 3, 4, 28 and the 14 branching (Mayanskiy); M_cl; Λ; I₂ (weak: arctan-ansatz target).
  - **CHECK PASSED:** 7 branching; C₂(7), C₂(14); virial; su(3)-in-G2 normalisation; no negative Hessian mode (R = 20, 40; refinement); (3,1) level assignment.
  - **CONFIRMED (PLAN E3 predictions):** inertia I₁ (×3), I₂ (×8), 0 (×3); lowest states 1 (J=0), 14 (J=1), no 7; all J integer.
  - **NO_TARGET:** the 14–1 gap in MeV; the SU(3) refit point.
- Seed claims:
  - CONFIRMED: §2 bosons only; §3 SU(3) ⊂ G2 as the stabiliser of an imaginary octonion; §4 π₃(G2) = ℤ generated by the long-root hedgehog; §7.2 hexagon; π₂ = ℤ²; π₃ = ℤ.
  - Local linear stability: CONFIRMED, with global minimality OPEN.
  - The long-root hedgehog as the minimal-energy B = 1 configuration: OPEN.
  - PLAN §3.5: no verdict word (refined).
- **Open items:**
  - global minimality of the B = 1 hedgehog in G2, which needs full 3D minimisation in G2;
  - the projector-only π₃ route has still been computed only once: the cross-check did not re-implement it, though it checked the route's arithmetic.
