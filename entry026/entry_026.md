## Entry 026 — Pre-Registration: the Size of Consecutive-Prime Correlations of χ₋₃, χ₋₄ and (·/5) against the Absorbed (Untruncated) Hardy–Littlewood Density (Revision 2, November 11, 2026)

**Status:** Revision 2, APPROVED by Matthew Gifford on 2026-11-12 ("Approve and I give permission to push"). Frozen at the commit that adds `manifest26.json` to gifgaf0/gifgaf0.github.io; the commit hash and push time are in `run_log_026.md`. Revision 1 applied Matthew's pre-freeze decisions of 2026-11-10; Revision 2 recorded the pre-freeze checks (reconciliation with the archived scripts; zbMATH pass). The freeze uses the beacon procedure in §Freeze. No data in the decisive ranges exist. None will be generated until the manifest commit is public and the beacon round fixed by it has been published. The only data seen that bear on this question are listed under Disclosures. Everything else in this entry is model values, synthetic dry runs, and smoke tests outside the decisive ranges.

### Question

The paper's §5.2 found that LO–S eq. (2.16) undershoots the mod-4 pair deficit by about 6%. Absorbing small primes into the modulus ("full HL") accounts for that shortfall, and for its decline with height (`mod4_untruncated_HL_exploratory.md`, seen data). Exploratory work on Entry 025's published sign controls found the same at q = 3 and 5: (2.16) misses by 5.0% and 11.5% in arm A, and full HL lands within 1σ (`exploratory_sign_size_2026-11-09.log`). Neither result was pre-registered. The paper lists the size as "a direct check for later work".

For χ ∈ {χ₋₃, χ₋₄, (·/5)} and three fresh heights:
1. Is E[χ(p_n)χ(p_{n+1})] more negative than (2.16) predicts? (T-216)
2. Does it equal the absorbed HL value within a frozen tolerance? (T-full)
3. Does the ratio to (2.16) fall with height, as a truncation effect must? (T-height)

**The S₅ link.** (·/5) is the sign of the S₅ Frobenius of Entry 025 on every prime (Stickelberger; Entry 025 checked it on all 7·10⁷ primes). So this entry measures the size of the abelian correlation that Entry 025's controls detected only by direction. It needs no factoring, and it is a (P+) entry.

### Heuristic and prior address

- **The model.** Hardy–Littlewood k-tuples (conjectural), through LO–S eq. (2.16), are evaluated at modulus Q = q·∏P and marginalised to classes mod q. This is the absorption of Entries 020 and 021 and §5.2. Absorbing p evaluates the local factor at p exactly, with every tuple size included, instead of truncating it at size 2.
- **What is known.**
  - The bias and (2.16) are LO–S's (PNAS 2016; arXiv:1603.03720). LO–S also state a conjecture for Σ(p_n/q)(p_{n+1}/q).
  - Absorption is this project's method.
  - Holt (arXiv:2405.03540) explains the same biases through the evolution of gap populations under the sieve, which is a different heuristic.
  - Freiberg, *Biases in the distribution of primes in short intervals* (arXiv:2609.33692v1, 27 September 2026), derives a second-order asymptotic for the share of short intervals holding m primes, under a uniform HL hypothesis. It cites LO–S and states that its statistic is the prime count in an interval, not the residue pattern of consecutive primes. It contains no character correlations. It is related in method (second-order HL truncation), with no overlap in statistic.
  - We found no earlier test of the untruncated size for these correlations: web and arXiv search (avenues note, 2026-11-09) and the zbMATH Open pass of 2026-11-10 (`claude/research/zbmath_pass_2026-11-10.md`).
    - "consecutive primes" & (bias | biases) returned eight records, all residue-pattern work: LO–S 2016 and 2020, David–Devin–Nam–Schlitt 2022, Holt 2016, Lichtblau 2019, Brothers 2016, Kuperberg 2025 and a proceedings volume.
    - Brothers 2016 visualises the biases with iterated function systems and gives no asymptotics.
    - Lichtblau 2019 was not checked beyond its zbMATH listing. It should be read before any novelty sentence in a write-up; no test or prediction here depends on it.
- **The S₅ sign.** As above: Stickelberger, as in Entry 025.

### Predictor (`predict_026.py`, `ladder_026.py`, `uniform_shift_026.py`, `make_pred_026.py`)

- **Code.** The on-the-fly marginal from the exploratory script, unchanged in substance. It reproduces the project's frozen values (`validate_predictor_026.log`):
  - mod-4 ε at 2^127.5: 0.0071637 (frozen 0.007164);
  - q = 5 same-residue share at 2^255.5: 0.238474 (frozen 0.23847);
  - mod-4 absorption ratios at 2^127.5 with {3}, {3,5}, {3,5,7}: 1.0130, 1.0172, 1.0182 (archived values identical);
  - mod-4 ε at 10⁹–2·10⁹: 0.0227317 against frozen 0.022729. The reconciliation below shows that this difference is not a quadrature effect: the archived range integrals omit the 1/(log y)² factor of the pair density.
- **Reconciliation with the archived scripts** (`reconcile_026.py`, `reconcile_026.log`; done 2026-11-11).
  - **Sources.** `run020/predict/los216.py` and `pair_absorb.py` were extracted in Matthew's Chrome from the Zenodo records: the 017–021 archive (10.5281/zenodo.23843120, `consecutive_pairs_017_021 (4).tar.gz`, SHA-256 9bece9eb…6077) and the exploratory mod-4 deposit (10.5281/zenodo.23843225, `exploratory_mod4.zip`). They were rebuilt here byte-identically (SHA-256 6bfd6a69…5214 and c6c39225…236d, checked against the browser's own hashes) and are kept in `archive/`.
  - **(2.16), all nine frozen cells**, recomputed with the archived `los216.density` under this entry's conventions: |difference| ≤ 5.8·10⁻¹⁰ (relative 7·10⁻⁹).
  - **Absorbed cells** (q = 3 and q = 5, absorbing through 11, at 1.01·10¹², 2^63.5 and 2^127.5): the archived `los216.density` evaluated directly at Q = q·∏P and marginalised agrees with `predict_026.py` to ≤ 6.4·10⁻¹⁰ in all 24 cells.
  - **Mod-4 ladder against the archived `pair_absorb.py`.**
    - Re-running `pair_absorb.py` reproduces its archived `mod4_result.json` exactly (difference 0).
    - At 2^63.5 and 2^127.5 it agrees with `predict_026.py` to ≤ 9.3·10⁻¹¹.
    - Over the range 10⁹–2·10⁹ the two differ by 3.2–3.5·10⁻⁶ at every rung.
  - **Source of that difference** (`range_weight_check_026.py`, `.log`). `pair_absorb.py` weights each Gauss node by y but drops the 1/(log y)² factor of the pair density.
    - With the factor restored, the archived `los216.density` gives 0.0227317039 at 6, 8 and 24 nodes, equal to `predict_026.py` to 2·10⁻¹⁰.
    - Without it, the archived code gives 0.0227285421 at every node count.
    - So the frozen Entry 024 value 0.022729 carries the same omission, 0.014% of ε. The absorption ratio is unchanged (1.06011 both ways), so the paper's Table 8 and §5.2 are unaffected.
    - This entry's arm-E prediction uses the full density with the factor, as the archived `los216.density` itself does.
- **Absorbed set (fixed here).** Every prime ≤ 19 not dividing q:
  - q = 3: {2, 5, 7, 11, 13, 17, 19};
  - q = 4: {3, 5, 7, 11, 13, 17, 19};
  - q = 5: {2, 3, 7, 11, 13, 17, 19}.
  - Reason: 19 is the largest prime at which every cell costs minutes per node. 23 multiplies the cost by 22. The choice is not blind; see Disclosures.
- **Arm E.** The pair density is integrated over [10¹², 1.02·10¹²) with 2-node Gauss–Legendre in log y and dy weight. 1, 2 and 4 nodes agree to 7·10⁻⁸, and 2 and 4 nodes agree to 3·10⁻¹³ (`conventions_check_026.log`).
- **Random arms.** Starts are uniform in y on [2^(b−1), 2^b). The model is therefore the uniform-in-y average of the normalised local table (4-node Gauss–Legendre in log y, dy weight), not the local density at 2^(b−0.5) used for the exploratory arm-B comparisons.
  - The shift is +3.5 to +4.2·10⁻⁵ at 64 bits and +1.0 to +1.2·10⁻⁵ at 128 bits.
  - It changes by less than 10⁻⁷ between absorbing through 11 and through 17 (`ushift_026.log`).
  - Rule: (2.16) is the uniform average itself, and full HL is the local value through 19 plus the shift computed through 17.
- **The ladder steps fall more slowly than 1/p².** Steps for absorbing 11, 13, 17, 19 (`ladders_026.log`; model values only):

| cell | step 11 | step 13 | step 17 | step 19 |
|---|---|---|---|---|
| E χ₋₃ | +9.0·10⁻⁵ | +8.5·10⁻⁵ | +6.4·10⁻⁵ | +5.9·10⁻⁵ |
| E χ₋₄ | −4.8·10⁻⁵ | +3.1·10⁻⁵ | +1.9·10⁻⁵ | +2.0·10⁻⁵ |
| E (·/5) | +1.5·10⁻⁴ | +8.3·10⁻⁵ | +4.1·10⁻⁵ | +3.1·10⁻⁵ |
| R64 χ₋₃ | +2.8·10⁻⁵ | +2.4·10⁻⁵ | +2.7·10⁻⁵ | +3.0·10⁻⁵ |
| R64 χ₋₄ | −3.9·10⁻⁵ | +1.5·10⁻⁵ | +3.4·10⁻⁶ | +6.4·10⁻⁶ |
| R64 (·/5) | +8.0·10⁻⁵ | +6.1·10⁻⁵ | +3.6·10⁻⁵ | +2.9·10⁻⁵ |
| R128 χ₋₃ | −1.0·10⁻⁶ | +1.3·10⁻⁶ | +5.3·10⁻⁶ | +8.7·10⁻⁶ |
| R128 χ₋₄ | −1.5·10⁻⁵ | +7.5·10⁻⁶ | +1.6·10⁻⁶ | +1.6·10⁻⁶ |
| R128 (·/5) | +1.8·10⁻⁵ | +2.1·10⁻⁵ | +1.7·10⁻⁵ | +1.5·10⁻⁵ |

  - **Mechanism.**
    - The exact local-factor correction at p, from tuples of size ≥ 3, is O(1/p²).
    - But absorbing p also scales Q/φ(Q) by p/(p − 1) = 1 + 1/p + O(1/p²).
    - That shifts α = 1 − Q/(φ(Q)L) and κ = Q/(φ(Q)αL) by relative amounts of order 1/p.
    - (2.16) keeps the expansion in κ only through the D₂ term, so the omitted higher-order terms move by O(1/p) at each step.
    - The net step is therefore O(1/p) in general, not O(1/p²). As more primes are absorbed, Q/φ(Q) grows like log P, so the truncation error does not vanish as the absorbed set grows. "Full HL" computed this way has an intrinsic ambiguity that one more prime will not remove.
  - **How well the cells follow it** (`drift_check_026.log`; p·step should be constant under O(1/p)).
    - E χ₋₃ is cleanly O(1/p): p·step = 9.9, 11.0, 10.8, 11.3 ·10⁻⁴ for p = 11, 13, 17, 19. So is R128 (·/5): 2.0, 2.8, 2.9, 2.8 ·10⁻⁴.
    - (·/5) at E and R64 decays faster, closer to 1/p² (p²·step 12.0, 11.3 and 10.5, 10.5 ·10⁻³ at 17, 19). There the 1/p term is evidently small against the local-factor term.
    - χ₋₃ at R64 and R128 decays more slowly than 1/p: p·step rises 3.1 → 5.7 and −0.1 → 1.7 ·10⁻⁴.
    - The χ₋₄ cells are small and change sign at 13.
    - The mechanism explains why the steps need not fall like 1/p². It does not give one power law for every cell, and it is not used quantitatively anywhere in this entry.
  - **Not additive.** The step for p measured against a small base differs from the ladder step in size and even in sign (`additivity_026.log`), so the tail cannot be estimated cheaply.
- **Model tolerance τ (fixed here; approved by Matthew Gifford, 2026-11-10):** τ = 3 × max(|step 13|, |step 17|, |step 19|) for each cell. It covers about three more steps of the observed size. It is a judgement, stated as one, and it was set after the ladder and the arm-A controls were inspected (Disclosures).

**Frozen predictions** (`pred_026.json`; s.e. planned as binomial, √((1−c²)/N)):

| cell | (2.16) | full HL (through 19) | ratio | τ | τ/\|c\| | planned s.e. |
|---|---|---|---|---|---|---|
| E χ₋₃ | −0.078886 | −0.082552 | 1.0465 | 2.55·10⁻⁴ | 0.31% | 3.7·10⁻⁵ |
| E χ₋₄ | −0.073421 | −0.076983 | 1.0485 | 9.2·10⁻⁵ | 0.12% | 3.7·10⁻⁵ |
| E (·/5) | −0.065796 | −0.071462 | 1.0861 | 2.50·10⁻⁴ | 0.35% | 3.7·10⁻⁵ |
| R64 χ₋₃ | −0.053753 | −0.055741 | 1.0370 | 9.1·10⁻⁵ | 0.16% | 1.0·10⁻⁴ |
| R64 χ₋₄ | −0.050539 | −0.052234 | 1.0335 | 4.6·10⁻⁵ | 0.09% | 1.0·10⁻⁴ |
| R64 (·/5) | −0.046240 | −0.048580 | 1.0506 | 1.82·10⁻⁴ | 0.37% | 1.0·10⁻⁴ |
| R128 χ₋₃ | −0.030198 | −0.030901 | 1.0233 | 2.6·10⁻⁵ | 0.08% | 7.1·10⁻⁵ |
| R128 χ₋₄ | −0.028644 | −0.029169 | 1.0183 | 2.3·10⁻⁵ | 0.08% | 7.1·10⁻⁵ |
| R128 (·/5) | −0.026847 | −0.027578 | 1.0273 | 6.4·10⁻⁵ | 0.23% | 7.1·10⁻⁵ |

### Data (fresh)

| arm | data | pairs | generation |
|---|---|---|---|
| E | all primes 10¹² ≤ p < 1.02·10¹², in 200 blocks of 10⁸ integers | ≈ 7.24·10⁸ adjacent | `gen_E_026.c`, segmented sieve; ≈ 2 min |
| R64 | runs r = 0–9,999: start s from `random.Random(f"{SEED}:R64:{r}")`, uniform in [2⁶³, 2⁶⁴); 10⁴ + 1 consecutive primes from the first prime ≥ s, first dropped | 10,000 × 9,999 = 99,990,000 | `gen_R_026.py 64 SEED …`; ≈ 0.13 s per run, ≈ 22 core-min |
| R128 | runs r = 0–19,999, the same with `R128` and [2¹²⁷, 2¹²⁸) | 20,000 × 9,999 = 199,980,000 | ≈ 0.55 s per run, ≈ 3 core-h |

- **SEED** is the randomness (64 hex digits) of the drand round fixed by the beacon rule (§Freeze). Every chunk stores it.
- **Stored.** Lag-1 and lag-2 pair tables of residues mod 60 (the 16 units), per block (arm E) or per run. These determine every statistic for q = 3, 4, 5. No primes are stored for arm E. For the random arms, the first and last kept prime of each run and one sampled pair are stored.
- **Freshness.**
  - Arm E sits above every exhaustive range used by Entries 017–025 and above Part I's mod-5 counts (to 10¹⁰). LO–S's published counts for q = 3, 4 run to 10¹²; the window starts there.
  - The random starts depend on a beacon value published after the freeze, so they are fresh by construction and unknown to everyone at the freeze.
  - Dry runs and smoke tests use the seed strings `dry-1`, `dry-2` and `smoke-026`.
- **Integrity** (`build_026.py`, all expected to report zero failures):
  - E: the range header; the prime count, sum mod 2⁶⁴, xor, per-block counts, first and last primes, and both lag tables all equal to an independent numpy re-computation (`check_E_026.py`); lag totals equal to n − 1 and n − 2; the first and last prime of every block equal to PARI `nextprime` / `precprime`;
  - R: every chunk generated with the beacon seed; run indices exactly 0–9,999 and 0–19,999; 9,999 and 9,998 pairs per run; the first kept prime of every run equal to PARI `nextprime` from the seeded start; bit lengths; distinct starts; the sampled pair of every run proven prime by PARI `isprime` and consecutive by PARI `nextprime`.
- **Smoke tests**, outside the decisive ranges (`build_smoke_026.log`, `build_negative_026.log`):
  - [9.98·10¹¹, 9.982·10¹¹) and runs 0–2 at both bit lengths with seed `smoke-026`: 0 failures on all 22 checks.
  - The C generator and the numpy re-computation agreed exactly on 1–1.1·10⁹, and both matched PARI `primepi` (4,814,936).
  - The same smoke data checked against the decisive range, another seed and the decisive run counts failed 8 checks, as designed.
  - No correlation was computed on real smoke data.

### Statistics and decisive tests (`analyze_026.py`)

- **Startup checks.** The analysis refuses to run unless:
  1. every file in `manifest26.json` matches its SHA-256, including the running copy of `analyze_026.py`;
  2. the beacon round file satisfies randomness = sha256(signature);
  3. every R64/R128 chunk was generated with that randomness as its seed;
  4. the run indices are exactly 0..N − 1 for the manifest's N.

  The predictions are read from the manifest-hashed `pred_026.json`. The checks are tested in `manifest_check_test_026.log` on synthetic data with a stand-in beacon round. The consistent case passes; an edited entry, an edited analysis, an edited archived script, another round's randomness, tampered beacon randomness and a wrong run count are each refused with a named reason. `--dry` skips the checks and is for synthetic data only.
- **Estimator.** For a cell, ĉ = Σ_u S_u / Σ_u n_u, where S_u = Σ χ(p)χ(p′) over the pairs of unit u (a block or a run) and n_u is the number of pairs. The s.e. is the ratio-estimator s.e. over units, √(Σ(S_u − ĉ n_u)² · m/(m − 1)) / Σ n_u, with m units. Decisions use this s.e. The binomial s.e. is reported. In the null dry run the two agreed within 5%.
- **21 decisive tests, α′ = 0.01/21 = 4.76·10⁻⁴** (one-sided z 3.304, two-sided 3.494). Each has planned power, or for a consistency test planned pass probability, ≥ 0.8 (`pred_026.log`).

| test | count | what | rule | planned power / detectable miss |
|---|---|---|---|---|
| T-216 | 9 (3 arms × 3 χ) | observed more negative than (2.16) | z = (ĉ − c₂₁₆)/s.e. < −3.304 | ≥ 0.9999 in every cell, using the gap minus τ |
| T-full | 9 | consistent with full HL | \|ĉ − c_full\| ≤ τ + 3.494·s.e. | pass probability ≈ 1 if the absorbed model is right within τ. A miss detected with 80% probability: E 0.50%, 0.33%, 0.57%; R64 0.94%, 0.92%, 1.27%; R128 1.08%, 1.13%, 1.34% of the correlation (χ₋₃, χ₋₄, (·/5)) |
| T-height | 3 (per χ) | ratio to (2.16) falls from E to R128 | D = ĉ_E/c₂₁₆,E − ĉ₁₂₈/c₂₁₆,₁₂₈, z = D/s.e.(D) > 3.304 | predicted D = +0.023, +0.030, +0.059, at least +0.019, +0.028, +0.053 within τ; planned s.e.(D) 0.0024–0.0027; power 1.000 each |

- **What T-full can and cannot see.**
  - At arm E it is limited by τ, not by the data. The data alone would resolve 0.05%.
  - At 128 bits it is limited by the data. With 20,000 runs the miss detected at 80% (1.08–1.34%) is below the (2.16)-to-full gap there (2.33%, 1.83% and 2.73%), so T-full separates the two models at 128 bits as well.
- **Report-only:**
  - χ² of (ĉ − c_full)/√(s.e.² + τ²) over the 9 cells;
  - for each cell, the rung of the ladder closest to the data. This is only informative at arm E, where the s.e. is smaller than the steps;
  - R64 against (2.16) and full HL, as an ordering check between the decisive heights;
  - lag-2 correlations (no prediction computed in this entry);
  - full pair-share tables mod 3, 4 and 5 per arm.

### Outcomes

- **All as predicted.** At three fresh heights the correlations of χ₋₃, χ₋₄ and (·/5) are more negative than (2.16), and equal the absorbed HL value within 0.3–0.6% at 10¹², 0.9–1.3% at 2⁶⁴ and 1.1–1.3% at 2¹²⁸. The ratio to (2.16) falls with height. So the (2.16) shortfall seen mod 4 (§5.2) and in Entry 025's controls is a truncation effect within Hardy–Littlewood, pre-registered for three characters including the S₅ sign.
- **T-216 fails** (observed at or above (2.16)) with T-full also failing: suspect the pipeline first.
- **T-full fails with T-216 passing.** The data lie between (2.16) and full HL, or beyond full HL, by more than τ. First suspect the κ-expansion ambiguity of the model (τ too small), then the integration conventions. Interpret only in a separate entry.
- **T-height fails:** the shortfall does not decline with height, which is not a truncation effect. This is the most informative possible failure.
- The analysis runs once.

### Freeze (beacon procedure, as Entry 025-K)

1. After Matthew's approval: `make_manifest_026.py manifest26.json` hashes this entry, the code, `pred_026.json`, the logs and the two archived scripts (34 files). The run counts are 10,000 / 20,000, and the seed rule is written into the manifest.
2. Commit and push the freeze package to the public GitHub repo (gifgaf0/gifgaf0.github.io, under `entry026/`). Record the commit hash and the push time in the run log, with GitHub's own push record as corroboration.
3. **Beacon, named before publication:** the drand mainnet default chain (League of Entropy):
   - chain hash 8990e7a9aaed2ffed73dbd7092123d6f289930540d7651336225dc172e51b2ce;
   - genesis 1595431050 and period 30 s; round r is published at genesis + (r − 1)·30.
   - R is the first round published at least 10 minutes after the push (`beacon_round_026.py PUSH_TIME`).
   - SEED is its randomness.
4. Fetch `/info`, round R and round R − 1. Verify with `verify_beacon_026.py`: chain identity, the BLS signature, randomness = sha256(signature), the chain link to R − 1, and two negative controls. Record R, its time, the randomness and the signature in the run log.
   - Both tools reproduce Entry 025-K's round 6611336 from its push time 2026-11-04T05:34:50Z, and its BLS check (`beacon_tools_test_026.log`).
5. Only then generate arm E and its independent check, R64 (`gen_R_026.py 64 SEED data/R64 0 10000`) and R128 (`… 128 SEED data/R128 0 20000`). Then build with integrity checks, and run `analyze_026.py manifest26.json round_R.json data/E.bin data/R64 data/R128` once.

### Code, dry runs and runtime

- **Code.**
  - `predict_026.py` (model), `ladder_026.py` and `uniform_shift_026.py` (model values), and `make_pred_026.py` (frozen values, τ, power) produce `pred_026.json`.
  - `gen_E_026.c`, `check_E_026.py`, `gen_R_026.py` and `build_026.py` handle data and integrity.
  - `analyze_026.py` runs the analysis.
  - `beacon_round_026.py`, `verify_beacon_026.py` and `make_manifest_026.py` handle the freeze.
  - `make_dry_026.py` makes synthetic data only.
- **Dry runs** at full size (synthetic multinomial counts from mod-60 tables computed by the predictor at Q = 60·7·11·13; 200 blocks, 10,000 R64 runs and 20,000 R128 runs; `dryrun_null_026.log`, `dryrun_effect_026.log`):
  - *Null* (data at the model's values): 21 of 21 tests as predicted. T-216 z from −7.50 (R128 χ₋₄) to −158. T-full |z| without τ ≤ 1.87. T-height z = +8.3, +12.0, +22.5. Unit-based and binomial s.e. agree within 5%.
  - *Effect* (correlations mixed toward independence to the (2.16) level, with λ calibrated on χ₋₄): 16 of 21 tests fail, including every T-full cell.
    - Five still pass: T-216 for (·/5) at all three heights, T-216 for χ₋₃ at R64 (z −3.41, sampling), and T-height for (·/5).
    - A mixture calibrated on χ₋₄ moves (·/5) only part of the way to (2.16), because its full-HL/(2.16) ratio is larger.
- **Runtime.** Arm E generation ≈ 2 min plus ≈ 4 min for the independent check. R64 ≈ 22 core-min. R128 ≈ 3 core-h. All of it ≈ 2 h wall on 2 cores, chunked and resumable. The build is a few minutes and the analysis seconds. The predictions are already computed (≈ 1.4 core-h).

### Disclosures

- **Seen data.**
  - Entry 025's four control values (arm A at 2.0–3.0·10⁹, arm B at 128 bits), and the mod-4 note (Entries 022–024 and the 64/128-bit arms). Both are exploratory comparisons of these same models, and both motivated this entry.
  - The absorbed set "through 19" was the set used in the exploratory arm-A comparison, which fit within 1σ. Through 11 it was at +1.8σ and +2.5σ. A set chosen after seeing that would be a forking path. The stated reason, the largest set that is cheap in every cell, is true, but it is not blind.
  - Under the frozen rule, the seen Entry 025 controls would have passed T-full. Arm A τ: 2.5·10⁻⁴ (C5) and 4.3·10⁻⁴ (C3), against misses of 1.2·10⁻⁴ and 4·10⁻⁵. Arm B (C3) miss: −4.8·10⁻⁴ against a band of 7.6·10⁻⁴.
- **The τ rule was written after seeing the ladder** (model values, no data) and after seeing that the arm-A data sit within 1σ of the through-19 value. Matthew approved it on 2026-11-10 with this disclosure kept.
- **The uniform-in-y convention** was adopted after the first null dry run, on model values only, because it matches how the random starts are drawn. The local 2^(b−0.5) value differs by up to 4.2·10⁻⁵.

### Revision 1 (November 10, 2026; decisions by Matthew Gifford)

| # | change | reason |
|---|---|---|
| 1 | τ rule kept as drafted, with its disclosure | approved |
| 2 | Mechanism for the slow steps written out: absorbing p scales Q/φ(Q) by 1 + 1/p + O(1/p²), which moves α, κ and the truncated D₂ term by O(1/p). Each cell's fit to it is reported (`drift_check_026.log`) | requested; the cells do not all follow one power, which is now stated |
| 3 | R128: 10,000 → 20,000 runs (1.9998·10⁸ pairs). T-full miss at 80% falls from 1.49–1.80% to 1.08–1.34% | resolves the 1.8–2.7% full-HL shift at 128 bits |
| 4 | Power and both dry runs recomputed at the new size | requested |
| 5 | Archive scripts: not found in the workspace, the project or the GitHub repo, and Zenodo is not reachable from this session. Reconciliation remains a pre-freeze item | requested |
| 6 | arXiv:2609.33692 identified (Freiberg, 27 Sep 2026) and read; added to prior address (no overlap of statistic) | requested |
| 7 | `analyze_026.py` verifies `manifest26.json`, the beacon round and the data seed at startup, and refuses on any mismatch, as Entries 017–024 checked their manifests | requested |
| 8 | Beacon freeze as Entry 025-K. Random-arm seeds come from the drand round; run indices restart at 0 (were 100–10,099 with a fixed seed string). `beacon_round_026.py`, `verify_beacon_026.py` and `make_manifest_026.py` added; generator and builder take the seed | requested |

The Revision 0 draft and the five files changed since are kept in `claude/real_char_size/rev0/`; their hashes are listed in the Revision 0 entry. No Revision 0 code was run on decisive data.

### Revision 2 (November 11, 2026; pre-freeze checks)

| # | change | reason |
|---|---|---|
| 1 | Reconciliation done: the predictor agrees with the archived `los216.py` to ≤ 6.4·10⁻¹⁰ on every (2.16) and absorbed cell. The archived `pair_absorb.py` range values differ by 3.5·10⁻⁶ because they omit 1/(log y)² in the range weight; the frozen Entry 024 ε inherits this (0.014%) | required before the freeze |
| 2 | The zbMATH pass of 2026-11-10 is recorded in the prior address | rule 2 |
| 3 | The manifest now also hashes `reconcile_026.py`, `range_weight_check_026.py`, their logs, and the two archived scripts (34 files) | traceability |

No test, prediction, band or sample size changed. `pred_026.json` is unchanged.

### Before freezing

- Pre-freeze checks: done (Revision 2).
- Matthew's approval: given 2026-11-12, with permission to push. The freeze follows §Freeze.
- **Outside this entry** (for the paper's errata list, not a change to any frozen record): Entry 024's (2.16) ε at 10⁹–2·10⁹ and the mod-4 note's range values were integrated without the 1/(log y)² factor. The effect is 0.014% of ε, and the absorption ratios are unchanged.
