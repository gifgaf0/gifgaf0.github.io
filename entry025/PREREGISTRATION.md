# Entry 025 — Prime-order reduction of a fixed curve over consecutive primes at 2^64–2^256

**Status: rev. 3, APPROVED by Matt on 2026-11-03 (arm B at 5,000 runs). Awaiting freeze.** Nothing in this entry is decisive until the manifest commit is public and the seed has been taken from a public beacon round published after that commit (§10).

## 1. Question and why it matters for cryptography

Fix an elliptic curve E/Q. Walk through consecutive primes p from a uniformly random b-bit start. How often is |E(F_p)|, or |E(F_p)|/t, prime?

The scan length a deployment should expect is 1/rate.

**Prior work** (literature pass of 2026-11-03: `LIT_SEARCH_2026-11-03.md`):

- **Koblitz (1988, §3)** proposes exactly this procedure, as the conjecture's original cryptographic motivation: choose a large random odd M, find the successive primes p among M, M+2, M+4, …, and compute |E mod p| each time.
- **Other directions.** Galbraith–McKee (2000) fix p and vary the curve; Castryck–Folsom–Hubrechts–Sutherland (2012) extend that to genus 2. Koblitz (Experiment. Math.) fixes a small field and varies the extension degree.
- **The constant.** Zywina (2011) refined it and checked it on exhaustive ranges up to 10⁹. His §1.1 (Jones's counterexample) is the entanglement phenomenon behind §3 here.
- **The R3 control.** Its published form is Lee–Mayle–Wang (Canad. J. Math. 2025, Conj. 1.6), Koblitz–Zywina in arithmetic progressions. Güloğlu–Hamakiotes–Lee–Wang (2026) prove it on average over a family.
- **The CM curve.** Iwaniec–Jiménez Urroz (2010) prove that |E|/8 is a P₂ infinitely often for y² = x³ − x, the CM curve used here.

**Claims of this entry, kept narrow:**

- We found no numerical test of the Koblitz rate at ≥ 64 bits.
- We found no work on prime-order (or any Frobenius-derived) events at *consecutive* primes, so LAG1|C appears unstudied.

The pass was web search only. Forward citations of Zywina 2011 and LMW 2025, a MathSciNet/zbMATH sweep, and LMW §8 are still owed before submission. They do not affect the design.

This entry is the elliptic-curve sibling of Entries 017–024:

- **(P+)-type:** the rate, and its dependence on congruence classes of p, is what the Galois-image heuristic predicts.
- **(P−)-type:** prime-order events at consecutive primes are correlated only through congruence data.

## 2. The conjecture used (Zywina 2011, Conj. 1.2, eq. (1.1))

P_{E,t}(x) ≈ C_{E,t} ∫_{t+1}^{x} du / ((log(u+1) − log t) · log u)

Among primes near u, the local rate is therefore C_{E,t} / (log(u+1) − log t).

## 3. Curves

| | curve | why | t | eligible p | constant |
|---|---|---|---|---|---|
| non-CM | **37a1**: y² + y = x³ − x | Serre curve: ℓ-adic image GL₂(Z_ℓ) for all ℓ; adelic index 2, level 74 (LMFDB) | 1 | all | C_{37a1} = C·(1 + 1/47881) = 0.5051767187 (Zywina Prop. 4.2, D = 37 ≡ 1 mod 4) |
| CM | **32a1**, via its isogenous model **32a2**: y² = x³ − x (same #E(F_p)) | CM by Z[i]; 4 \| #E always | 8 | p ≡ 1 (mod 4) | C_CM = 1.0673509290 (Zywina §7: 1.067350894) |

Here C = 0.505166168239435774, Zywina Remark 2.6. `predict.py` computes C_CM as (4/π)·∏_{ℓ odd}[f_ℓ/(1 − χ(ℓ)/ℓ)], which converges absolutely. It agrees with Zywina's value to 3·10⁻⁸ relative.

### Structural facts (deterministic; used as integrity checks, not tests)

All of these were found or confirmed while calibrating (§8).

- **CM:** for split p, p ≡ 1 (mod 8) ⇒ 16 | #E, so |E|/8 is even. p ≡ 5 (mod 8) ⇒ #E ≡ 8 (mod 16), which held for all 166,203 such p < 10⁷. So every prime-order event has p ≡ 5 (mod 8), and no further 2-adic channel remains.
- **37a1:** (p/37) = −1 ⇒ 2 | #E. This is the Serre-curve entanglement Q(√37) ⊂ Q(E[2]) ∩ Q(ζ₃₇). Frob_p acts on E[2] as an odd permutation exactly when (p/37) = −1, and an odd element of S₃ fixes a 2-torsion point. Every prime-order event has (p/37) = +1.

**Crypto reading:** half the primes in a fixed-curve scan are wasted for these curves, and a congruence test on p alone identifies them before any point counting.

## 4. Arms and data

Each run takes s uniform among b-bit integers with the top bit set and generates consecutive primes ≥ s with `gmpy2.next_prime`. The first prime of each run is dropped because its selection is gap-weighted. Primality is checked with `gmpy2.is_prime(·, 40)`.

**Point counting:**

- **CM:** PARI `ellap` (CM method), on every eligible prime.
- **37a1:** early-abort SEA, PARI `ellsea(E_p, 1)`. It returns 0 once it finds a small prime factor of #E; otherwise it returns #E exactly. The hit rule is a ≠ 0 and is_prime(a, 40). A nonzero return can still be composite.
  - None of the decisive tests needs #E itself, only the hit indicator.
  - One prime in 97 also gets a full `ellap` count for the integrity checks (§7).
  - On the 40-bit dry arm, the new code reproduces the old full-count code's hit vector bit for bit (§8).

| arm | curve | bits | runs × primes | eligible | expected hits | CPU-h (s/prime) |
|---|---|---|---|---|---|---|
| A37_64 | 37a1 | 64 | **4,000** × 1,001 | 4.0·10⁶ | 45,870 | 19 (0.017) |
| B37_128 | 37a1 | 128 | **5,000** × 1,001 | 5.0·10⁶ | 28,570 | 51 (0.037) |
| CCM_128 | 32a1/32a2 | 128 | 40,000 × 10,001 | 2.0·10⁸ | 2.47·10⁶ | 5.3 |
| DCM_256 | 32a1/32a2 | 256 | 10,000 × 10,001 | 5.0·10⁷ | 3.05·10⁵ | 6.7 |

The total is about 82 CPU-h. Arm B, the most novel arm, gets most of it. **Arm B at 5,000 runs was approved by Matt on 2026-11-03.**

## 5. Predictions (output of frozen `predict.py`; it reads no data)

| arm | rate | mean primes scanned per prime-order hit | R3 = rate(p≡1 mod 3)/rate(p≡2 mod 3) |
|---|---|---|---|
| A37_64 | 0.0114673 | 87.2 | 5/4 |
| B37_128 | 0.0057137 | 175.0 | 5/4 |
| CCM_128 | 0.0123627 (per split prime) | 161.8 (all primes) | 3/4 |
| DCM_256 | 0.0060971 (per split prime) | 328.0 (all primes) | 3/4 |

**The estimand.** Each run has a fixed number of primes from a start uniform on [2^{b−1}, 2^b). So the predicted pooled rate is the **unweighted** mean of C/(log(u+1) − log t) over that interval. Rev. 1 weighted by 1/log u; the change moves the 64–256-bit predictions by at most 2·10⁻⁵ relative.

**Where R3 comes from:**

- **37a1:** G(3) = GL₂(F₃), and 3 | #E ⇔ Frob has eigenvalue 1. Brute-force counts give 9/24 of det-1 elements and 12/24 of det-2 elements, so R3 = (1 − 3/8)/(1 − 1/2) = 5/4.
- **CM:** 3 is inert in Z[i], so for split p the Frobenius λ lies in F₉^×. Hecke equidistribution spreads it evenly over each norm fibre. P(λ = 1 | N(λ) = 1) = 1/4, and N(λ) = 2 excludes λ = 1. So R3 = (3/4)/1 = 3/4.

The two curves go in opposite directions.

**Independent check of 5/4 (LMW 2025).** Their family-average class constants are C_{3,1} = 0.280648 and C_{3,2} = 0.224518 (ratio 1.25000). These equal C·5/9 and C·4/9 to all six published digits, which is what the GL₂(F₃) count gives.
- For 37a1 itself (Serre curve, m_E = 74, coprime to 3), their Theorem 1.7 changes each class constant by at most a factor (1 ± 1/47881). So R3 moves by at most 4.2·10⁻⁵, far below the arms' R3 resolution.
- We could not run their Magma code (`CyclicityKoblitzAPs.m`) here.
- The CM value 3/4 has no counterpart in LMW. It rests on the derivation above, plus the 10⁹ count (662,879 / 885,887; §8) and the 48-bit run (0.7503 ± 0.0030).

## 6. Decisive tests

There are 12 decisive tests: 3 per arm. α′ = 0.01/12 two-sided, z_crit = 3.341. Every SE comes from a run-block bootstrap (B = 2000, fixed seed) over per-run sufficient statistics.

**Pair definition (LAG1).** A pair is two primes that are **adjacent in the full prime sequence and both eligible**. For 37a1 every prime is eligible, so pairs are simply consecutive primes. For CM, a pair is two consecutive primes that are both ≡ 1 (mod 4). It is *not* two neighbours in the subsequence of split primes. The bookkeeping uses the same pairs.

| test | statistic | predicted | 80%-detectable deviation (A / B / C / D) |
|---|---|---|---|
| RATE | hits / eligible | §5 | ±1.9% / ±2.5% / ±0.26% / ±0.76% (relative) |
| R3 (positive control) | class-rate ratio | 5/4 or 3/4 | ±0.049 / ±0.062 / ±0.004 / ±0.011; distance from 1 is 21σ / 17σ / 259σ / 91σ |
| LAG1\|C ((P−)-type) | lag-1 correlation of hit indicators over the pairs above, *minus* the congruence bookkeeping Σ_pairs μ_c μ_{c′}/N over the 4 classes c = (G-class) × [p ≡ 1 mod 3] | 0 | ±0.0021 / ±0.0019 / ±0.00042 / ±0.00084 |

The G-class is p ≡ 5 (mod 8) for CM and (p/37) = +1 for 37a1.

A test comes out as predicted if |z| < z_crit. Consistency tests pass with probability 1 − α′ under H₀, which meets the power rule. Their power is stated as the 80%-detectable sizes above.

The bookkeeping uses pooled class rates μ_c. Abelian-over-Q channels left out of the 4 classes (p mod ℓ for ℓ ≥ 5) contribute |ρ| ≲ 10⁻⁵, from the GL₂(F_ℓ) counts of §5 combined with LO–S pair shares. That is below every detectable size. What the "0" assumes beyond this is stated in §9.

**Report-only:**
- raw LAG1 and its bookkeeping value. Expected negative, because LO–S makes consecutive primes avoid the same class, and that pulls them away from the (G, G) pairs where hits occur.
- the waiting-time mean
- integrity failures

## 7. Integrity checks (all must be zero)

**Every eligible prime:**
- CM: the Hasse bound; 8 | #E; p ≡ 1 (8) ⇒ 16 | #E; p ≡ 5 (8) ⇒ #E ≡ 8 (16).
- 37a1: if (p/37) = −1, any nonzero early-abort return must be even. The abort need not fire: on the dry arm, one such prime returned the full, even #E.

**One prime in 97:**
- 37a1: a full `ellap` count must agree with the early-abort result. A nonzero return must equal #E, and a 0 return must not hide a prime #E. Also checked: the Hasse bound, (p/37) = −1 ⇒ 2 | #E, and [#E]P = O at a random point.
- CM: [#E]P = O.

**Every run:** 5 sampled consecutive pairs are checked against PARI `nextprime`. Runs are resumable, and a run file is never overwritten.

## 8. Pre-freeze evidence (exploratory, seen data; nothing here is a test)

**Pipeline against Zywina's published counts, x = 10⁹:**

| curve | Zywina actual | ours | Zywina expected | our integral |
|---|---|---|---|---|
| y² = x³ − x, t = 8, p ≡ 1 mod 4 | 1,548,766 | **1,548,766** | 1,549,657 | 1,549,656.6 |
| y² = x³ + 6x − 2 (Serre, D = −3), t = 1 | 1,456,288 | **1,456,288** | 1,456,166 | 1,456,166.0 |
| 37a1, t = 1 (new) | — | **1,310,342** (z ≈ −0.21); R3 = 728,118/582,224 = 1.2506 | — | 1,310,576.8 |

All 1,456,288 hits for Zywina's D = −3 Serre curve have p ≡ 1 (mod 3). This is the same entanglement mechanism as §3, with Q(√−3) in place of Q(√37), and it independently confirms that the structural fact is a Serre-curve phenomenon.

**Dry/exploratory runs at non-test heights** (fresh seeds, discarded after use; rates against the rev.-1 weighted prediction, which differs by < 6·10⁻⁵ relative):

| arm | n | RATE obs/pred | R3 | raw LAG1 | bookkeeping | LAG1\|C |
|---|---|---|---|---|---|---|
| CM, 48-bit, 1500 runs | 7.5·10⁶ split | 0.0344515 / 0.0345619 (z = −1.64) | 0.7503 ± 0.0030 | −0.00399 ± 0.00052 | −0.00416 | +0.00018 ± 0.00053 |
| 37a1, 40-bit, 300 runs | 3.0·10⁵ | 0.018167 / 0.018426 (z = −1.08) | 1.285 ± 0.036 | +0.0011 ± 0.0017 | −0.0005 | +0.0016 ± 0.0017 |

**Early-abort SEA validation:**
- Random starts against full `ellap`: 3,000 primes at 64 bits and 60 at 128 bits.
- No hit mismatches. Every nonzero return equalled #E.
- Composite nonzero returns: 212 of 245 at 64 bits and 3 of 4 at 128 bits.
- Speed: 9.2× at 64 bits and 14.4× at 128 bits.
- Equivalence: the 40-bit dry arm (seed `explore-v2`, 300,000 primes, 5,450 hits) was rerun with the rev.-2 generator, and hit, class, eligibility and residue vectors are identical.

**Logged design changes (pre-freeze):**

1. **The lag-1 test moved.** Rev. 1 predicted raw LAG1 = 0. The 48-bit exploratory run rejected that at z = −8.3. The cause is the congruence channel in §3, and the bookkeeping reproduces it, as the table shows. The decisive test was therefore moved to LAG1\|C, mirroring the Part II nulls of Entries 022–024.
2. **An integrity check was wrong.** The first rev.-2 integrity check assumed early abort *always* fires when (p/37) = −1. It flagged 1 prime (p = 768475322261, #E = 2·3²·34327·1243717): the abort did not fire there, and the return was the full, even count. The check now tests parity instead. The structural fact was never violated.

## 9. Scope and limitations

- **Coverage.** Two curves. t ∈ {1, 8}. Lag 1 only. Classes are built from the two known abelian channels plus p mod 3.
- **What the LAG1\|C = 0 prediction assumes.** For a split prime ℓ (CM curve), and for the non-abelian Frobenius of 37a1, whether ℓ | #E depends on Frobenius data beyond p mod ℓ: for CM, on π mod a prime above ℓ. So "0" is the (P−) hypothesis itself. For CM it amounts to this: consecutive primes show no bias in Gaussian (ray-class) residues beyond their own rational residue classes. Entry 023 tested this kind of independence for ray classes of Q(i) mod 7 and found none at its sensitivity.
  - The nearest existing heuristic is David–Devin–Nam–Schlitt, who model LO–S-type biases for consecutive sums of two squares. That is a related but different object, and it makes no prediction for this statistic.
  - Any such effect is expected to be well below the detectable sizes in §6, but that is an assumption, not a derivation.
- **The rate tests check Zywina's leading-order heuristic.** No second-order term is predicted. Arm C's ±0.26% sensitivity is the sharpest such test we know of; a miss there would mean a lower-order term, not necessarily a wrong constant.

## 10. Freeze procedure

1. Done: Matt approved rev. 3 on 2026-11-03.
2. Run `python3 predict.py > predictions.json` (done; it is the file hashed in the manifest).
3. Hash PREREGISTRATION.md, predict.py, predictions.json, gen.py and analyze.py into `manifest.json`. Commit and push to the public GitHub repo (gifgaf0). Record the commit hash and its push time in the run log.
4. **Seed from a public beacon.** The seed is the randomness of the drand mainnet round R. R is fixed by this rule: the first round whose publication time is at least 10 minutes after the push time in step 3. Record R, its time and its randomness in the run log.
   - This shows the freeze came first, and that nobody, the author included, could have chosen the seed.
   - It closes the timestamp gap Entries 017–024 left open.
   - The NIST beacon is an equivalent alternative. Name whichever is used in the log before the round is published.
5. Run `gen.py ARM SEED RUNS PRIMES OUTDIR` per arm, then `analyze.py OUTDIR ARM` once per arm. The analysis refuses to run on any hash mismatch.
