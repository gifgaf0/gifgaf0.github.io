# The revised SLWE note: what to deposit as version 2 on Zenodo (draft)

**Plain-language summary.** The revised note corrects four wrong statements in the deposited first version and adds
the numbers the first version left out. The main result is unchanged: the Singer-orbit matrix has rank at most 76,
which breaks both published parameter sets.
- The wrong statements are about other documents, plus one false side remark about which moduli are safe.
- An independent audit (October 10, 2026) found them. Three of the four came with the October 9 edits that tied the
  note to *Fluid Lattice Topology*: one sentence was new, and two older sentences took on a meaning they did not have.
- To publish it, open the record 10.5281/zenodo.23270249, choose **New version**, replace the PDF and paste the
  description below. Do this after the pull request is merged, because the PDF cites a commit that reaches GitHub only
  then. Nothing here is deposited.
- If you post the note to IACR ePrint, post the revised one.

## File

| File | md5 | |
|---|---|---|
| `slwe_negative_result_v2.pdf` | `312841740b484f731d452c11e445a260` | 6 pages. `build_v2.py` builds it from the first version's source and rebuilds it byte-identical |

## Record settings

- **Title:** unchanged, "A rank collapse in a sedenion Module-LWE proposal, and why a uniform matrix does not repair it".
  With the new estimates the title holds for both of the paper's parameter sets: a uniform matrix restores neither
  one's claimed security.
- **Version:** v2. **Licence:** CC BY 4.0, as before. **Publication date:** the day you deposit.
- **Related identifiers.** Zenodo links the new version to the first one by itself. Suggested additions:
  - doi:10.5281/zenodo.20078312 (*Fluid Lattice Topology*), relation "references";
  - `https://github.com/gifgaf0/gifgaf0.github.io/tree/4eb30148edfe6e4949e16b6ecfc6d04f4512b6e1`, relation
    "is supplemented by". This is the commit that the revised note's Section 7 cites, and it holds every script the
    note uses.

## Description (to paste)

> We report a negative result on SLWE, a Module-LWE variant over the 16-dimensional sedenion algebra that the author
> proposed in an earlier paper with a claim of NIST Category 5 security. Its public matrix is built from orbits of an
> order-7 coordinate permutation (a "Singer cycle"). First, the flattened public matrix factors through a fixed
> 256 × 112 integer matrix of rank 76. So its rank over F_q is at most 76 for every module rank k, and exactly 76 for
> generic seeds once k ≥ 7, whereas a uniform matrix of the same shape has rank 16k. This invalidates the security claim
> at both published parameter sets. Recovering the noise then reduces to an LWE instance of dimension 76, which the
> lattice estimator places at about 2^39 operations at the first set (n = 512, q ≈ 2^32) and 2^40 at the second
> (n = 1024, q = 911). Second, replacing the matrix by a uniform one does not restore the claim (centred binomial noise
> with η = 2, ternary secrets of weight 64): the estimator gives about 2^51 at the first set and about 2^167 at the
> second, against 2^262 for ML-KEM-1024, a Category 5 standard. Third, decryption at the first set never fails: the
> noise is bounded by 258, far below q/4. All computations are reproducible from public scripts.
>
> **Changes in this version.** The first version of this note contained four errors, corrected here.
> 1. Its abstract cited a failure rate of 2^(−6.4×10^15) as "reported earlier", which reads as a claim of the proposing
>    paper. The figure comes from the project's own ledger.
> 2. It said the project's working specification kept the parameters of the paper's version 1. That document targets
>    q ≈ 3329.
> 3. It presented the prime 4 294 977 961 and the secret weight 64 as the paper's version 1 parameters. They are the
>    note's instantiation.
> 4. It said decryption never fails for any q > 1032. It fails at q = 1033; the first prime at which it never fails is
>    1039.
>
> The first version also described Table 1 as having three seed sets and a uniform control for every k. That held only
> for k ≥ 8; the runs for k ≤ 7 are now made, with the same values. This version also gives the exact failure rate at
> q = 911 next to the tail. It adds estimates for the paper's version 2 parameters, after the rank collapse (2^40.4) and
> with a uniform matrix (2^167.2). Under the same estimator that falls between ML-KEM-512 and ML-KEM-768, and about 95
> bits below ML-KEM-1024. It also compares the working specification's own rows with their claims: at q = 911, at most
> about 2^127; at q = 3329, about 2^112.

## The notice for *Fluid Lattice Topology*

`FLT_V3_NOTICE_DRAFT.md` is updated to match. It now says that a uniform matrix restores neither version's security.
It cites the note as a whole, through the record's "all versions" DOI: Zenodo shows that DOI on the record page, under
"Cite all versions". A DOI for one version would leave readers on the first version.
