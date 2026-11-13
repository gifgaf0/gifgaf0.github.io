# Sym²-scale exploratory session: short note (2026-11-12)

**Status: EXPLORATORY, unfrozen, nothing decisive.** These are numbers and pictures, not evidence for a theorem. Choices and the binning rule were fixed before any statistic was computed (`session_log.md`), and every variant run is listed there. No novelty is claimed. The question is posed in Lowry-Duda §5.3 / Remark 5. No one was contacted.

## Step 0: prior numerics
No published plot of level-1 Sym² family averages against p/X was found.
- Kundu–Müller (arXiv:2507.00738, Outlook) cite Sutherland's numerical work on degree-3 L-functions, which suggests (P/N)^{1/3} regularity. Their only Sutherland citation is an unpublished letter to Rubinstein and Sarnak.
- Sutherland's public murmuration slides contain no degree-3 or Sym² families.
- Sutherland's letter to Rubinstein and Sarnak (30 Aug 2022), read from the copy Matthew supplied (`sutherland_letter_check.md`), covers elliptic curves, Γ0(N) newforms of weights 2–6 and genus-2 families. It has no degree-3 family, no Sym² family and no (p/N)^{1/3} scaling. Kundu–Müller's statement that Sutherland's numerics favour (P/N)^{1/3} for degree-3 L-functions therefore has no identified source; the attribution is unverified.
- Lowry-Duda's SCGP handout (Nov 2024) describes Sym² murmurations via the GL(2) trace formulas as work in progress by Bober, Booker, Lee, Lowry-Duda and Seymour-Howell. It has no data. So nothing published covers this family, but others are working on it, which is one more reason to claim nothing.

## What was computed
E(p) = Σ_k w(k) Σ_f λ_f(p²) / Σ_k w(k) dim S_k(1), from Eichler–Selberg with unconditional class numbers.
- **Windows:** primary is the conductor window w(k) = Φ(X_k/X), X_k = ((k−1)/2π)², with Φ a smooth bump in log₂(X_k/X) on (−1, 1). The narrow window H₀((k−K)/K^0.9) appears only at K ≤ 300.
- **Variable:** x = p/X, X = ((K−1)/2π)², x ≤ 5.
- **S1 (unweighted):** at K = 150 and 300 (all t), and at K = 1000 and 2500 (t truncated near ±2p, τ = 1e-4; every 2nd and every 11th prime).
- **k-classes mod 4 and S2 (i^k):** at K = 150 and 300 only.
- **Supplementary:** K = 100 with c = 1 (p ≤ K²).

## Validation (all passed)

| Check | Scope | Result |
|---|---|---|
| Kronecker–Hurwitz (k = 2) | all 1,369 primes ≤ 11,323, exact | 0 failures |
| Dimension-zero k = 4, 6, 8, 10, 14: Tr T_{p²} = 0 | all primes, mod two 31-bit primes | 0 failures |
| Exact Tr T_{p²} vs PARI `mfheckemat` | k ≤ 48, p ≤ 47 | 105/105 |
| k = 12 against τ(p)² − p^11 | p ≤ 400 | 78/78 |
| §2.2 identity (Poisson closed form vs direct per-k sum, narrow window) | 16 primes, K = 150 and 300 | agrees to ≤ 1.5·10^-5 (√N scaling) |
| Truncation τ = 1e-4 vs all t | K = 300, 1,369 primes | Δ(√X·E) rms 1.0·10^-3, max 2.1·10^-3 (statistic rms 0.52) |

**Class numbers (R8).** PARI's own documentation says `qfbhclassno` assumes GRH above 5·10^5. So H was built from `qfbclassno` (Shanks), which the documentation calls unconditional for |D| < 2·10^10, and every discriminant used is below that (max 1.53·10^10). The documentation read is PARI 2.15.2's; the library run was 2.17.2.

**Correction to the scoping doc.** With a compactly supported bump Φ, the k-sum decays only sub-exponentially. The truncated path therefore needs ~5,000 class numbers per prime at x = 5, not "a few". That is why K stops at 2500.

## What the plots show (descriptive only)
- **Fig. 1–2 (S1, √X·E).**
  - The hyperbolic term (the −1/2 in the trace formula) contributes a constant ≈ −0.93 to −0.95, drawn as its own line.
  - The total dips to about −1.1 near x ≈ 0.7, has a smaller bump near x ≈ 1.7 and a dip near x ≈ 2.3, then rises to about −0.2 to −0.3 at x ≈ 5.
  - The elliptic part alone (Fig. 1, middle) oscillates around a rising trend and reaches +0.64 to +0.71 by x ≈ 4.9.
  - Bin means at K = 300, 1000 and 2500 agree: rms difference 0.04 outside the first bin, and 1–2 of 24 bins with |z| > 2 per pair. The first bin (x ≤ 0.2) differs, because the identity term is large and K-dependent there.
  - At K = 150 and at K = 100 (c = 1), no bin reaches the frozen n ≥ 30, so those panels show scatter only.
- **Fig. 1 (right), x^{1/3} axis.** Same bins, relabelled. Nothing here distinguishes x from x^{1/3} as the better variable.
- **Fig. 3, scalings.** In raw E, the curves at different K are separated, roughly by the factor √X. In √X·E they overlap. In √p·E the hyperbolic line becomes −c√x and dominates the picture.
- **Fig. 4, classes and S2 (K = 300).** The k ≡ 0 and k ≡ 2 panels each look like S1 but noisier. S2 (i^k-weighted) is consistent with zero at this K: no bin with |z| > 2, χ²/dof 0.73 (conductor window) and 0.86 (narrow).
- **Fig. 5, window dependence (R4).** Per prime, the narrow and conductor windows differ by rms 0.33–0.50. The binned S1 curves differ visibly for x ≈ 1.2–3, where the narrow-window curve is smoother. The hyperbolic constants differ by ~3%.

## Follow-up readings (2026-11-12 evening; existing data only)
Each item is a **hypothesis read off the data**, not a conclusion. The variants are logged in `session_log.md` (Follow-up) and the numbers are in `followup.json` and `followup_extra.json`.

- **H1. Large x (question: does the total approach 0 for x ≫ 5?).**
  - Data: K = 100, c = 1, rebinned at width 2 (a new variant outside the frozen rule).
  - The elliptic part levels off at about +0.82 to +0.86 for 5 < x < 40 (pooled x > 10: +0.825 ± 0.029; x > 20: +0.859 ± 0.037). That is below the +0.986 needed to cancel the hyperbolic constant at this K.
  - The total stays near −0.16 ± 0.03 for x > 10 (−0.125 ± 0.037 for x > 20). The fitted slope is +0.004 ± 0.0025 per unit x.
  - So at K = 100 and x ≤ 40, the data do not show the total reaching 0. They are compatible with a slow approach, or with a nonzero offset, and do not decide between them.
  - Caveats: a single, small K (the hyperbolic constant itself moves from −0.986 at K = 100 to −0.930 at K = 2500); one window; error bars ignore correlation between neighbouring primes.
- **H2. Cross-K agreement of the elliptic part.** Frozen bins, √X scaling.

  | pair | rms of bin differences | bins with |z| > 2 (of 25) | max |z| |
  |---|---|---|---|
  | 300 vs 1000 | 0.039 | 0 | 1.6 |
  | 1000 vs 2500 | 0.039 | 2 | 2.6 |
  | 300 vs 2500 | 0.035 | 0 | 0.9 |

  Unlike the total, the first bin does not stand out, because the K-dependent identity term is removed. Read as: the elliptic part, as a function of x, looks K-independent over K = 300–2500. Not tested beyond that range.
- **H3. Window dependence** (K = 300, the only K with both windows binned).
  - Under both windows: the dip at x ≈ 0.7 (conductor −1.133, 3.0 s.e. below its neighbours; narrow −1.062, 8.0 s.e.) and the overall rise for x > 1 (weighted slopes +0.164 and +0.173 per unit x).
  - Only under the conductor window: the bump near 1.7 and the dip near 2.3. At K = 300 they are within noise (0.7 and 0.3 s.e. steps), but at K = 1000 and 2500 they recur clearly (bump minus dip 7.7 and 5.4 s.e.). Under the narrow window at K = 300 the total rises monotonically through 1.1–2.1, then flattens to 2.9.
  - Read as: the 0.7 dip and the rise are robust to the window; the 1.7/2.3 structure depends on it. The narrow window was not run at K ≥ 1000, so whether it would show the structure there is unknown.
- **H4. Does the large-x offset of the total shrink with K?** Question asked of the data, not answered by it.
  - Data: K = 100, 150 and 200, conductor window, width-2 bins beyond x = 5. K = 150 to x ≤ 20 and K = 200 to x ≤ 11.3 came free from the existing table. K = 200 to x ≤ 15 needed 388 new primes (17 min, unconditional class numbers; Kronecker–Hurwitz and dimension-zero checks passed).
  - Over the common range x ∈ (5, 15] the total is −0.198 ± 0.042, −0.226 ± 0.029 and −0.210 ± 0.022 at K = 100, 150, 200. The elliptic part is +0.781, +0.735, +0.742, while the hyperbolic constant moves −0.986, −0.966, −0.956. For x ∈ (10, 15]: −0.232, −0.246, −0.221.
  - A K-independent offset fits (−0.214 ± 0.016, χ² 0.35 / 2 dof). An offset vanishing like 1/K fits poorly (χ² 13.7 / 2). A fit a + b/K leaves b unconstrained (1.7 ± 9.4).
  - Reading, as a hypothesis: over K = 100–200 there is no sign of the offset shrinking, and the simplest finite-K form (∝ 1/K) is disfavoured. But K spans only a factor of 2, slower rates (K^{-1/2}, 1/log K) were not tried, the three K share one class-number table, and the error bars ignore correlations. So shrink, stay fixed, or undecidable: **undecidable at these sizes**, with the data leaning toward "not shrinking like 1/K".
  - Within x ≤ 5 the last-bin totals at K = 300, 1000, 2500 (−0.30, −0.27, −0.22, s.e. 0.04–0.08) drift toward 0 by 0.4σ and 1.0σ per step. That does not bear on x ≫ 5.
- **Remark (heuristic rate, not checked).** At fixed K the binned total must tend to 0 as x → ∞. The family is finite, and each Sym²f is cuspidal on GL(3) (Gelbart–Jacquet), so the PNT for L(s, Sym²f) gives Σ_{p≤y} λ_f(p²) log p = o(y). Under GRH the decay of a bin mean could be as slow as about (log x)³/√x. So a nonzero offset over a finite x-window at fixed K is a finite-x effect, not a fixed-K limit, and the K = 100 data out to x = 40 neither confirm nor contradict this rate. The open question is about the K → ∞ limit curve M(x) and its behaviour as x → ∞, not about fixed K. In particular, whether M(x) → 0 as x → ∞ is not settled by these data.
- **Extension beyond x = 5.** K = 150 to x ≤ 20 and K = 200 to x ≤ 15 are now done (H4). Not run: K = 300 to x ≤ 15, about 1.0·10^8 new class numbers, about 3.5–4 h on 2 workers.

## Limitations
- **Not computed:**
  - Class panels and S2 at K ≥ 1000, which need t near 0; that is ~10× the class numbers.
  - The A-curve.
  - S4.
- **Statistics:**
  - Truncation error (~10^-3) is not in the error bars.
  - Error bars are prime-to-prime s.e. and ignore correlation between neighbouring primes.
  - The bump Φ, θ = 0.9, the bins and τ are single choices.
- **Not established:**
  - Whether there is a K → ∞ limit in either normalization.
  - Why the curves agree across K.

## Files
- `session_log.md`: frozen choices, validations, all variants.
- `sym2lib.py`, `htable.py`, `run_stats.py`, `validate.py`, `trunc_check.py`, `describe.py`, `plots.py`, `make_figs.py`: code.
- `validation.json`, `describe.json`, `cuts.json`: numbers quoted above.
- `followup_2026-11-12.py`, `largex_2026-11-12.py`, `followup.json` (keys F1–F3, F5, F5b), `followup_extra.json`: the follow-up readings.
- `validate_ext.py`, `validation_ext.json`: integrity checks on the K = 200 extension table.
- `README.md`: how to reproduce every figure and number.
- `figs/fig1`–`fig6` (PNG): uploaded to the project as files.
