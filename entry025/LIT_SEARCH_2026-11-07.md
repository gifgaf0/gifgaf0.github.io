# Entry 025 — literature pass 2 (2026-11-07)

This file follows up the pre-freeze literature pass. PREREGISTRATION §1 cites that pass as `LIT_SEARCH_2026-11-03.md`, but the file is not in this repository.

§1 lists three items as owed before submission:
1. forward citations of Zywina 2011 and of Lee–Mayle–Wang 2025;
2. a MathSciNet/zbMATH sweep;
3. LMW §8.

This pass is **partial**. The limits are stated first, because they decide what the findings can support.

## Method and limits

- **Only web search was available.** The session's network policy blocked every bibliographic source, whether queried directly or fetched as a page:
  - MathSciNet;
  - the zbMATH API;
  - Semantic Scholar;
  - OpenAlex;
  - Crossref;
  - arXiv.
- **What this means:**
  - No complete forward-citation list was obtained for either paper.
  - No MathSciNet/zbMATH sweep was possible.
  - No paper was read in full; everything below rests on search-result abstracts and snippets.
- **Searches run (2026-11-07):** papers citing Zywina 2011; papers citing LMW 2025; recent Koblitz-conjecture work from 2024–2026; numerical Koblitz tests at cryptographic sizes; Frobenius or prime-order correlations at consecutive primes; LMW §8 and its Magma code.
- **"Unverified" below** means the item appeared in only one search result, or its abstract could not be retrieved.

## Item 1 — forward citations (partial)

Papers found that cite or build on Zywina 2011 (*A refinement of Koblitz's conjecture*, IJNT; arXiv 0909.5280) or on LMW 2025 (*Opposing average congruence class biases in the cyclicity and Koblitz conjectures for elliptic curves*, Canad. J. Math., doi 10.4153/S0008414X25101156; arXiv 2408.16641):

| work | cites | relevance to Entry 025 | status |
|---|---|---|---|
| Güloğlu–Hamakiotes–Lee–Wang, *Average twin prime conjecture for elliptic curves in arithmetic progressions*, arXiv 2608.29938 | Zywina, LMW | Already cited in §1. Proves the AP version on average, and the average constant agrees with LMW's predicted constant. | seen in several results |
| Dey–Saha–Sivaraman–Vatwani, *On the refined Koblitz conjecture*, J. Math. Anal. Appl. (2025) | Zywina | Derives the conjectured constant under an elliptic analogue of Elliott–Halberstam. It supports the constant used in §2, but it is not a numerical test. | seen in several results |
| *Character sums for elliptic curve densities*, arXiv 1703.04154 (authors not retrieved) | Zywina | Its snippet discusses Zywina's corrected constant and notes it need not be positive. It is background for §3 (entanglement). | seen in results; contents not read |
| *Congruence obstructions in the refined Koblitz conjecture*, arXiv 2609.30573 | Zywina | Per its snippet, E has a congruence obstruction mod ℓ iff E is ℚ-isogenous to a curve with a rational ℓ-torsion point (via Katz). 37a1 has trivial torsion and no isogenies, so it has no obstruction, which is consistent with §3. The §3 "half the primes wasted" fact is a density-½ restriction, not an obstruction. | **unverified**: appeared in one result only; a second search did not find it |
| *Divisibility biases in the orders of elliptic curve reductions*, arXiv 2606.25067 | (unclear) | Possibly relevant to the R3 control, which is a mod-3 divisibility bias by congruence class of p. | **unverified**: abstract not retrieved |
| *On the density of coprime reductions of elliptic curves*, arXiv 2603.24915; and Hamakiotes–Lee–Mayle–Wang (2026 preprint, cited in 2606.25067) | Zywina-style method | A related density problem; no direct bearing on the tests. | seen in results |

## Item 2 — MathSciNet/zbMATH sweep

**Not done.** Both sources were blocked. This item stays owed.

## Item 3 — LMW §8

**Not done.**
- The arXiv and Cambridge texts could not be fetched, and no search snippet showed §8 content.
- LMW say an accompanying repository holds Magma code for the constants, but the repository was not located, and the function name `CyclicityKoblitzAPs` (§5) was not confirmed.
- §5's independent check of R3 = 5/4 rests on LMW's published class constants C₃,₁ and C₃,₂, and is unaffected.

## Bearing on the two narrow claims (PREREGISTRATION §1)

1. **"No numerical test of the Koblitz rate at ≥ 64 bits."**
   - No search returned such a test. The numerical work found stops at exhaustive ranges: Zywina to 10⁹; one CM example to 10⁷.
   - Dey et al. and Güloğlu et al. are theoretical.
   - The claim stands, but only as far as web search reaches.
2. **"No work on prime-order (or other Frobenius-derived) events at consecutive primes."**
   - No search returned work on correlations of prime-order events, or of a_p, at consecutive primes.
   - The nearest items:
     - Lemke Oliver–Soundararajan and its follow-ups for primes and for sums of two squares (David–Devin–Nam–Schlitt, already in §9);
     - *Expected biases in the distribution of consecutive primes*, arXiv 2405.03540, which argues the LO–S biases are transient but persist far beyond computable ranges. This is relevant to the report-only raw LAG1, which §6 expects to be negative because of LO–S;
     - Chebyshev-bias work for a_p (Mazur, Sarnak), which concerns signs on average, not consecutive pairs.
   - **One paper to read before submission:** *Learning Euler factors of elliptic curves*, arXiv 2502.10357. Its snippet says it tests whether a_p can be predicted from other a_q.
     - If "other" means neighbouring primes of the same curve, it is the closest existing work to LAG1|C and must be cited.
     - Any such predictability is expected to come from information about the curve, not from adjacency in the prime sequence, but that is an expectation until the paper is read.

## Still owed

- A complete forward-citation list for Zywina 2011 and LMW 2025, from Google Scholar, MathSciNet or zbMATH.
- The MathSciNet/zbMATH sweep.
- LMW §8, and the LMW Magma repository.
- Full reading of arXiv 2502.10357, and confirmation of arXiv 2609.30573 and 2606.25067.

None of these can change the frozen design or the results. They affect only the novelty claims and the citation list of the write-up.
