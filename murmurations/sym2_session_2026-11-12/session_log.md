# Sym²-scale exploratory session: log (2026-11-12)

Mode: EXPLORATORY. Nothing frozen in the ledger sense and nothing decisive. Every variant tried is logged here (R9). Decisions come from Matthew (12:34 PT), applied to `claude/murmurations/sym2_scale_scoping_2026-11-12.md`.

## Step 0: prior numerics (done before any run)
Searched for Sutherland's degree-3 numerics and any published level-1 Sym² averages against p/X.
- Kundu–Müller (arXiv:2507.00738, Outlook) say Sutherland's numerical work suggests degree-3 L-functions look most regular in (P/N)^{1/3}. Their only Sutherland citation is a footnote, "Sutherland's letter to Rubinstein and Sarnak", which is unpublished. The bibliography has no Sutherland entry.
- Sutherland's public slides (MurmurationsNTW.pdf, MurmurationsSimons.pdf, MurmurationsUnanimated.pdf): no slide on degree-3, Sym² or GL(3) L-functions, nor on level-1 weight-aspect forms. The families shown are elliptic curves, Γ0(N) newforms, genus 2 and 3 curves, and products of elliptic curves.
- Lowry-Duda §5.3 / Remark 5 pose the question, with no plots. The He–Lee–Oliver–Pozdnyakov–Sutherland draft "Murmurations of L-functions" (2023) is listed at LIMS but its content is not accessible. Nothing else was found.
- Conclusion: no published data found that covers level-1 Sym² averages against p/X. The unpublished letter may contain degree-3 data, which could not be checked (no contact, per instructions). Proceeding.

## R8: PARI class numbers
- `qfbhclassno` documentation (PARI source tree bundled with cypari 2.5.4, PARI 2.15.2): "For x > 5·10^5, we assume the GRH, and use quadclassunit with default parameters." So `qfbhclassno` is NOT proven at the sizes used here (up to ~10^10).
- `qfbclassno(D)` documentation: for D < 0 with flag 0 (Shanks), it "gives unconditionnally correct results for |D| < 2·10^10".
- Decision: compute H(N) = Σ_{f²|N, −N/f² ≡ 0,1 (4)} qfbclassno(−N/f²)/w (w = 3 for −3, 2 for −4, else 1). Every N must be < 2·10^10; the code asserts this. Benchmark: 220–310 µs per H, faster than `qfbhclassno` (330–680 µs), with 0 mismatches in 1,200 samples.
- Caveat: the installed library is PARI 2.17.2, while the documentation read is 2.15.2's. The 2.17 text was not reachable from this session.

## Correction to the scoping doc (§2.4, path T)
The scoping doc said only "boundedly many m" contribute with a conductor window, and estimated A ≈ 8 Schwartz widths. With the compactly supported bump Φ chosen below, the k-sum W(α) decays only like a Gevrey bump (sub-exponential). Measured: |W| falls below 1e-4·max at α·K ≈ 200, i.e. m_cut ≈ 4,800 at x = 5, independent of K (≈ p·α²). The truncated path therefore costs ~2,400 class numbers per prime on average, not ~20–60. Feasibility is reduced accordingly (K ≤ 2500 here, primes subsampled).

## Frozen choices (fixed before computing any statistic)
- Trace: Tr_k(p²) = Σ_{f∈H_k} λ_f(p²), from Eichler–Selberg (squares paper, Lemma 1 / eq. (2)). k is even and ≥ 4; d_k = dim S_k(1).
- Sym² conductor proxy X_k = ((k−1)/2π)², with X = ((K−1)/2π)², and x = p/X. Range: all primes p with x ≤ 5 (prime p ≥ 2).
- Conductor window (primary): w_C(k) = Φ(X_k/X), Φ(u) = exp(−1/(1−v²)) for v = log₂u ∈ (−1, 1), else 0. So conductors lie in (X/2, 2X), i.e. k−1 ∈ ((K−1)/√2, √2(K−1)).
- Narrow window (only K ≤ 300, link to existing code): w_N(k) = H₀((k−K)/K^θ), H₀(v) = exp(−1/(1−v²)), θ = 0.9.
- Statistics: E_w(p) = Σ_k w(k) Tr_k(p²) / Σ_k w(k) d_k.
  - S1: unweighted.
  - Class panels: restrict w to k ≡ 0 (mod 4), resp. k ≡ 2 (mod 4), each normalized by its own Σ w d.
  - S2 = Σ w i^k Tr / Σ w d, only where path E (all t) is available, i.e. K ≤ 300. S2 at K = 1000 needs nearly all t (concentration at t ≈ 0) and is not affordable here.
  - No S4.
- Decomposition, always plotted: hyperbolic line = Σ w(k)(−1/2 − p^{1−k}) / Σ w d; identity line = Σ w(k)(k−1)/(12p) / Σ w d; elliptic = remainder. The hyperbolic line is never absorbed (R1).
- Scalings: raw E; √X·E (primary); √p·E. The hyperbolic and identity lines are drawn in the same scaling.
- K values: path E (all t): K = 150 and 300 (x ≤ 5), K = 100 with c = 1 (p ≤ K², x ≤ 40.3, own plot). Path T (truncated, conductor window, S1 and class panels): K = 1000 and 2500. K = 2500 rather than 3000 keeps every N below 2·10^10 (unconditional class numbers).
- Truncation (path T): drop t with |W_class(α_t)| < τ·max_α|W_class| for each k-class, τ = 1e-4, using α_t = 2 arcsin√((2p−t)/4p). Validated against path E at K = 300.
- Prime subsampling: if π(5X) > 6000, take every r-th prime (in increasing order, starting from the first), r = ceil(π(5X)/6000).
- **Binning rule (fixed now):** 25 equal-width bins on x ∈ (0, 5], width 0.2, identical for every K, window, statistic and scaling. Bin value = unweighted mean over primes in the bin; error bar = sample sd/√n. Bins with n < 30 are not plotted as means (scatter only). Per-prime values are drawn as a faint scatter. The x^{1/3} view uses the same bins, placed at (mean x in bin)^{1/3}; no rebinning.
- K = 100 with c = 1 (p ≤ 10^4; X = 248.3, so x up to 40.3): same rule extended, bins of width 0.2 up to 40.4, plotted only as this one supplementary figure.

## Variants tried (append-only)
- 13:10 Path-E table built: 12·H(4p²−t²) for all 0 ≤ t < 2p, all 1,369 primes p ≤ 11,323 (1.446·10^7 values, unconditional qfbclassno, every N < 5.2·10^8). 28 min on 2 workers.
- 13:12 Bug fixed before any statistic: lazy npz indexing caused OOM in the loaders. No results affected.
- 13:15 Validation (data/validation.json):
  - V3b Kronecker–Hurwitz Σ_{|t|≤2p} H(4p²−t²) = 2p²+p: exact, 0 failures of 1,369 primes.
  - V3 dimension-zero k = 4, 6, 8, 10, 14, Tr T_{p²} = 0: modulo two 31-bit primes, 0 failures of 1,369 × 5 × 2.
  - V2 exact integer Tr T_{p²} vs trace of PARI mfheckemat: k ∈ {12, 16, 20, 24, 30, 36, 48}, p ≤ 47, 105/105 agree.
  - V4 k = 12 against τ(p)² − p^11: 78/78 primes p ≤ 400 agree.
  - V1 §2.2 identity (narrow window θ = 0.9; direct per-k Chebyshev sum vs Poisson closed form), 8 primes each at K = 150 and 300 across x ∈ (0.1, 5]. Elliptic numerators agree to ≤ 1.4·10^-4 relative at K = 150 and ≤ 2·10^-6 at K = 300. V_unw (√N scaling) agrees to ≤ 1.5·10^-5 absolute. D_K = Σh·d matches σĤ(0)(K−7)/24 to the printed digits. The identity holds numerically.
- 13:20 Path-E statistics written: K = 150 and 300 (conductor C and narrow N windows, x ≤ 5) and K = 100 (C, c = 1). Files data/E_*.csv.
- 13:22 Truncation check (path T rule with τ = 1e-4 applied to the K = 300 E table, conductor window, S1 elliptic part): over 1,369 primes, |Δ(√X·E)| max 2.05·10^-3, rms 1.0·10^-3; the rms of the statistic itself is 0.52. Accepted for exploratory plots. Path-T curves at K = 1000 and 2500 carry this level of truncation error, which is not in their error bars.
- 13:30 Under the frozen rule (n ≥ 30 per bin), K = 150 (409 primes, ~16 per bin) gets no binned means; it is shown as per-prime scatter only. The rule was not changed.
- 13:40 K = 100 (c = 1): 1,229 primes over 202 bins (~6 per bin), so the frozen rule gives no binned means; scatter only.
- 14:12 K = 1000 path-T table done (5,927 primes, every 2nd prime ≤ 5X; 1.36·10^7 class numbers, max N 2.4·10^9). Statistics: data/T_K1000_C_5.csv (S1 only; class panels invalid under S1 truncation).
- 14:48 K = 2500 path-T table done (5,753 primes, every 11th prime ≤ 5X; 1.33·10^7 class numbers, max N 1.53·10^10 < 2·10^10). Statistics: data/T_K2500_C_5.csv.
- 14:50 Descriptive comparison across K (data/describe.json; frozen bins, √X scaling, S1 conductor window). These are descriptions, not tests:
  - Over all 25 bins, the rms of bin-mean differences is 0.11 (300 vs 1000), 0.05 (1000 vs 2500) and 0.08 (300 vs 2500). The largest difference is always the first bin, x ∈ (0, 0.2], where the identity term is large and K-dependent.
  - Excluding the first bin: rms 0.040 for every pair; max |Δ| 0.105 / 0.105 / 0.088; bins with |z| > 2: 1 / 2 / 1 of 24; max |z| 2.6 / 2.6 / 3.9.
- 14:50 Window comparison at K = 150, 300 (C vs N): the per-prime values differ by rms 0.33–0.50. The binned S1 curves differ visibly for x ≈ 1.2–3. The hyperbolic lines differ by ~3% (−0.947 vs −0.975 at K = 300).
- Variants run in total: S1 {C at K = 150, 300, 1000, 2500; N at K = 150, 300}; k ≡ 0 and 2 (mod 4) panels and S2 {C and N at K = 150, 300}; S1 C at K = 100 with c = 1. Scalings raw / √X / √p; axes x and x^{1/3}. Nothing else was tried. No re-binning. τ was fixed once (1e-4).

## Addendum (resumed session, 2026-11-12 ~16:20 PT): Step 0 completed, no new runs
- Lowry-Duda's SCGP handout (Nov 2024, davidlowryduda.com/wp-content/uploads/2024/11/SCGP_handout.pdf), section "GL(3) murmuration — symmetric square": describes Sym² murmurations via Eichler–Selberg/Petersson on a_f(p²) as work in progress by BBLLDSH (Bober, Booker, Lee, Lowry-Duda, Seymour-Howell). The handout has no figures, data, normalization or weights for Sym². So: in progress elsewhere, but no published coverage of this family and normalization. Step 0 rule satisfied; the run stands. Novelty: none claimed, and none should be (others are working on it).
- Sutherland's letter to Rubinstein and Sarnak (the [KM] footnote) is posted at math.mit.edu/~drew/RubinsteinSarnakLetter.pdf, so it is public, not "unpublished" as written above. This session could not fetch it (allowlist). Whether it contains degree-3 data is still unchecked; Matthew can open it directly.
- The HLOPS paper "Murmurations of L-functions" is cited as 2026 in the published BBLL version (ANT 20:2). It was not found on arXiv from this session, and its content is unchecked.
- Timestamp note: the clock times in the 14:12, 14:48 and 14:50 entries above are later than the modification times of the files they describe (data/T_K1000_C_5.csv 13:48, data/T_K2500_C_5.csv 14:19, describe.json 14:19, container clock). The file timestamps are authoritative; the entry order is right.
- No computation was rerun or changed in the resumed session.
- Correction to the frozen-choices list above: it says path T covers "S1 and class panels" at K = 1000 and 2500. Only S1 was computed there, because the τ cut was taken on the combined S1 weight (sym2lib.alpha_cut), which does not bound the single-class sums. The 14:12 entry and the note say this correctly. Class panels and S2 exist only at K = 150 and 300 (path E).

## Follow-up (2026-11-12 ~17:50 PT): reanalysis of existing data only, no new class numbers or traces
Script: followup_2026-11-12.py → followup.json. Every item below is a new variant, outside the frozen rule unless it says otherwise.
- F1 (NEW VARIANT, not the frozen rule): K = 100, c = 1 (data/E_K100_C_c1.csv, conductor window, √X scaling) rebinned with bins of width 2 on x ∈ (0, 42]. Each bin holds 50–94 primes; the last bin (40, 42] holds 5 and is ignored. Also pooled means for x > 5, 10, 20, and a least-squares line for the total over x > 5.
  - The elliptic part rises to about +0.70 by bin (4, 6], then fluctuates between +0.67 and +0.95 for 6 < x < 40. Pooled x > 10: +0.825 ± 0.029 (n = 862). Pooled x > 20: +0.859 ± 0.037.
  - The hyperbolic constant at K = 100 is −0.986, and the identity term is below 0.01 for x > 6.
  - Total: pooled x > 10 gives −0.158 ± 0.029, pooled x > 20 gives −0.125 ± 0.037. The fitted slope over x > 5 is +0.0040 ± 0.0025 per unit x.
- F2 (frozen bins): cross-K agreement of the S1 elliptic part alone, √X scaling, conductor window:

  | pair | rms of bin differences | bins with |z| > 2 (of 25) | max |z| |
  |---|---|---|---|
  | 300 vs 1000 | 0.039 | 0 | 1.6 |
  | 1000 vs 2500 | 0.039 | 2 | 2.6 |
  | 300 vs 2500 | 0.035 | 0 | 0.9 |

  Excluding the first bin changes rms by < 0.001 and no counts.
- F3 (frozen bins): window comparison at K = 300 (the only K with both windows and binned means), listing local extrema of the binned total and the smaller of the two steps to the neighbouring bins, in s.e. Also a weighted linear slope over x > 1.
  - Conductor window: min at 0.70 (−1.133, step 3.0 s.e.); max at 1.70 (−0.669, 0.7 s.e.); min at 2.30 (−0.894, 0.3 s.e.); slope +0.164.
  - Narrow window: min at 0.70 (−1.062, step 8.0 s.e.); rises monotonically through 1.1–2.1, flat 2.1–2.9 (shallow min at 2.71, 0.8 s.e.); slope +0.173.
  - Check of the conductor-only features at larger K (frozen bins): bump at 1.7 minus dip at 2.3 is 7.7 s.e. at K = 1000 and 5.4 s.e. at K = 2500; bump at 1.7 minus x = 1.3 is 5.4 and 4.4 s.e.
- F4 cost estimate only (not run). The existing path-E table (all t, all primes p ≤ 11,321) already reaches x ≤ 20.1 at K = 150 and x ≤ 11.3 at K = 200; only run_stats.py would be needed.
  - K = 200 to x ≤ 15: 1.02·10^7 new class numbers (primes 11,324–15,046), max N 9.1·10^8 (unconditional range). At the throughput measured for the path-E table (1.446·10^7 H in 28 min on 2 workers), about 20 min, plus about 40 MB of table.
  - K = 300 to x ≤ 15: 1.02·10^8 new class numbers, max N 4.6·10^9, about 3.5–4 h.
- Sutherland letter (sutherland_letter_check.md, read from the copy Matthew supplied): no degree-3, Sym² or (p/N)^{1/3} content. Kundu–Müller's degree-3 remark therefore has no identified source. The earlier note line "may cover this case and is still unchecked" is superseded.
- Reproducibility note: the F1 line fit and the F3 larger-K feature check were first run inline. They were then added to followup_2026-11-12.py, which writes them to followup_extra.json; the rerun reproduced the logged values. No new variant.

## Follow-up 2 (2026-11-12, 17:58–18:20 PT): large x at K = 150 and 200 (NEW VARIANTS)
Script: largex_2026-11-12.py → followup.json keys F5_largex, F5b_offset_vs_K. All values are S1, conductor window, √X scaling. Width-2 bins beyond x = 5 have edges 5, 7, 9, …, unlike F1's 0, 2, 4, …; bins with n < 30 are dropped. Pooled means and s.e. are over primes.
- 17:58 F5a (free rerun, existing path-E table): `run_stats.py data/HE 150 C 20` → data/E_K150_C_20.csv (1,359 primes, x ≤ 19.99) and `run_stats.py data/HE 200 C 11.3` → data/E_K200_C_11.3.csv (1,369 primes, x ≤ 11.29). About 10 s each.
- 17:58–18:15 F5c: new class-number table for K = 200 to x ≤ 15. 388 primes, 11,329 ≤ p ≤ 15,031, all t, 1.02·10^7 values, unconditional qfbclassno, max N 9.04·10^8. Job file data/jobs_E_ext200.json; tables data/HEx_w0/w1.npz; 17 min on 2 workers.
- Integrity checks on the new table (validate_ext.py → validation_ext.json): Kronecker–Hurwitz exact, and dimension-zero k = 4, 6, 8, 10, 14 mod two 31-bit primes. 0 failures on all 388 primes.
- `run_stats.py "data/HE*" 200 C 15` → data/E_K200_C_15.csv (1,757 primes, x ≤ 14.98). The glob reads the HE and HEx tables together.
- Results, total and elliptic part:

  | K | hyperbolic | own range x > 5 | own range x > 10 | common (5, 15] | common (10, 15] |
  |---|---|---|---|---|---|
  | 100 (x ≤ 40.2) | −0.986 | total −0.160 ± 0.026, ell +0.822 | total −0.158 ± 0.029, ell +0.825 | total −0.198 ± 0.042, ell +0.781 | total −0.232 ± 0.061, ell +0.749 |
  | 150 (x ≤ 20.0) | −0.966 | total −0.201 ± 0.024, ell +0.761 | total −0.197 ± 0.030, ell +0.766 | total −0.226 ± 0.029, ell +0.735 | total −0.246 ± 0.042, ell +0.717 |
  | 200 (x ≤ 15.0) | −0.956 | total −0.210 ± 0.022, ell +0.742 | total −0.221 ± 0.032, ell +0.733 | total −0.210 ± 0.022, ell +0.742 | total −0.221 ± 0.032, ell +0.733 |

  The "own range" rows cover different x-ranges per K, so only the "common" columns compare like with like.
- F5b fits of the common-range totals against K (3 points, K = 100, 150, 200):
  - (5, 15]: constant c = −0.214 ± 0.016 (χ² 0.35 / 2 dof). Pure b/K, i.e. an offset that vanishes like 1/K: χ² 13.7 / 2 dof. a + b/K: a = −0.224 ± 0.061, b = 1.7 ± 9.4.
  - (10, 15]: constant −0.230 ± 0.024 (χ² 0.23 / 2); pure b/K χ² 5.8 / 2.
  - No other rate (K^{-1/2}, 1/log K) was tried.
- Caveats: K spans only a factor of 2. All three K use one class-number table, so their per-prime values are not independent. Error bars ignore correlation between neighbouring primes. The hyperbolic constant moves with K (−0.986 → −0.956), and the elliptic part moves with it in the opposite direction.
