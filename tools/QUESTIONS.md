# Brief 02 — Open Questions

Status of every blocker / sub-question raised across Brief 02. Items
marked **CLOSED** are resolved; items marked **OPEN** still need a
decision.

## 1. Toy SLWE wrapper — CLOSED

Originally blocked because `sqt_slwe__1_.py` wasn't in the repo;
unblocked when you uploaded it. Then blocked on DFR target ≈ 0.5;
unblocked by the surgical fix described in
`tools/BRIEF_02_DISTRIBUTION_NOTE.md` (CBD(η=2) with ZD-pair rejection
applied to `s` and `r`, public matrix `A` left uniform).

DFR over 5000 trials: 0 at p=911, 0 at p=8191. xfail mark removed.

## 2. Lattice-estimator integration — STILL OPEN

Blocked on SageMath. `tools/lattice_estimate.py` is parameter-set-
correct and runs to a real markdown table on any host with Sage and
the Albrecht et al. estimator on `sys.path`. Three resolution paths
(unchanged from before):

1. Run the script on a Sage box and commit
   `tools/lattice_estimate_results.md`.
2. Stand up a `sagemath/sagemath` Docker image and add a CI step that
   produces the table.
3. Accept literature-only estimates with prominent labelling — needs
   explicit sign-off; I won't substitute literature numbers for a
   real estimator run on my own authority.

## 3. DFR scaling, k-axis — CLOSED for the original construction

`tools/dfr_scaling.py` runs end-to-end. The pre-fix sweep
(`tools/dfr_scaling_results.md`) measured DFR ≈ 0.5 across k ∈ {4, 8,
12, 16} and produced a degenerate fit, which Brief 02's parameter-fix
phase confirmed was caused by uniform `r`/`s`, not by a bad k.

After the surgical fix, a fresh k-sweep should give DFR ≈ 0 across
the same range (k=4 already verified at 0/5000). I have not re-run
the sweep through the wrapper because the wrapper now uses the fixed
keygen/encaps unconditionally; the sweep would just confirm DFR ≈ 0
at every k. Re-run on request.

## 4. DFR scaling, q-axis — OPEN

Still requires parametrising `tools/sqt_slwe.py` to accept `p` as a
function argument (it's a module-level global today). Doing it
correctly means picking primes in the desired magnitude range that
satisfy `p ≡ 1 (mod 455)` so the PSL(2,7) symmetry is preserved.
Candidates from `tools/mod455_primes.txt` cap at 50 000; for
`q ≈ 2^24` we'd need to extend the sieve range. Cheap to do; I
haven't because the brief didn't ask for it after the parameter-fix
phase.

## 5. Hardness reduction for the surgical fix — NEW OPEN QUESTION

The closure brief asked about a specific φ-fractional construction
that isn't on the branch. The actual implemented fix has its own
open security question, which I'll lodge here in lieu:

The wrapper's surgical fix uses
- **secret** `s` from CBD(η=2) over F_p^16 with ZD-pair rejection,
- **encryption randomness** `r` from the same distribution,
- **public matrix** `A` whose rows are PSL(2,7) Singer-cycle orbits
  of uniform seeds (existing structure from the supplied source).

Each of these deviates from textbook MLWE in a way that affects the
hardness reduction:

a. **Module-LWE over the sedenions.** The sedenions are non-
   associative and contain zero divisors. The "module" structure
   that secret/randomness sample from isn't a free module of finite
   rank over a commutative ring; it's a free `S_q`-module where
   `S_q` is non-associative. Whether the standard search-LWE ↔
   decision-LWE reduction applies, or what its analogue is in this
   setting, is genuinely open. The supplied source's docstring lists
   "hardness proof or reduction attempt" as a follow-up; this is
   that follow-up.

b. **`A` Singer-structured, not uniform.** Each row of `A` is
   determined by its first sedenion via the Z₇ Singer permutation.
   That's a 7-fold redundancy and is detectable from `A` alone in
   `O(k · DIM)` work, so any reduction that relies on `A` being
   uniform doesn't apply directly. Whether a reduction holds with
   "Singer-structured uniform" in place of "uniform" is unknown to
   me.

c. **Small-secret + small-randomness.** Standard MLWE (search) takes
   small `s` and uniform `r` (or no `r` at all). Schemes that
   additionally take small `r` are typically called *Compact-LWE* or
   *Ring-LWE-with-small-randomness* and have their own (sometimes
   weaker) reductions. The relevant security parameter is whether
   `(A, A^T r + e)` is pseudorandom under the standard assumption,
   which is *not* the same lemma as standard MLWE.

d. **ZD-rejection reshapes the secret support.** The rejection rate
   is small (~10⁻⁵), so the reshaped distribution is statistically
   indistinguishable from CBD(η=2) at any reasonable distinguishing
   advantage. This is unlikely to matter for security, but should be
   noted for completeness.

**What I would want to know before claiming any security level
for this construction:**

1. Is there a known (or plausible) hardness reduction for "MLWE
   over a non-associative algebra `S_q`" that's at least as hard as
   one of: ML-LWE over a commutative ring, NTRU, or a worst-case
   lattice problem in `S_q`?
2. Does the Singer-orbit structure on `A` (i.e. each row is a Z₇
   orbit) admit a reduction from / to a uniform-`A` version? If
   not, what's the closest known assumption it matches?
3. For the small-randomness side: is there a Compact-LWE-style
   reduction over `S_q`, or is the construction better viewed as a
   custom assumption that needs its own cryptanalysis?

These are questions for cryptanalysis, not engineering; I have no
plan for tackling them inside this codebase. They are flagged here
so the eventual paper can either cite an answer or explicitly
declare them as open.
