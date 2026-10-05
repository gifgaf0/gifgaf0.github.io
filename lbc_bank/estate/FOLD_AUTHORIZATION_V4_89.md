# FOLD AUTHORIZATION — V4.89 (banking fold: the longitudinal-sector result, §2.91.V)

**Recorded:** October 4, 2026, 04:30 UTC. **Base:** `SQT_Master_Ledger_v4_88_CANONICAL.md` md5 `66b0a634e3b087c85d4209f3e6bb6a28` (1,768,607 B). **Result:** `SQT_Master_Ledger_v4_89_CANONICAL.md` md5 `db01bd273629ce7a385ff3c7fb6efdfc` (1,773,873 B; +5,266 B / +5,115 characters). **Kind:** banking fold, single leg, no gate — §2.91.V; one annotation at the head of the transverse line (§2.91.I); the staged HK-5 housekeeping bracket after the V4.88 record's estate sentence with a short pointer after §2.91.U's estate sentence; the V4.89 fold-in record; the title/As-of bump; one changelog line. No Part VI row; no retraction; the §2.52 Open 3 row untouched; reverse-splice byte-identical to V4.88.

## The author's words (verbatim, brief of October 3, 2026, 20:16 PDT)

> Phase 1 records a result and prepares a paper. Keep the discipline proportionate: one short fold, no new gates, and full two-leg verification only for numbers the paper will cite (prepare that dispatch; don't run it). [...] The project store is full: write new files to the repo and keep ledger additions short.

> 1. Check the scope reading before recording it. Claim: the V4.67 drag is a property of knots moving through the substrate, not of the gravity reading of the longitudinal channel. So it limits matter propagation in the instantiated substrate, and the transverse line inherits it (same substrate, same knots). Search the ledger for anything that removes the knots' coupling to the longitudinal sector in the transverse line. If you find it, report it and skip step 2.

> 2. Fold (author-authorized, conditional on step 1): one short entry with the scope note, the LBC record at its honest register (single leg + internal hydro route + external analytic check), and items 2, 3 and 5 as errata. Add one annotation at the head of the transverse line, not one per row.

## The condition

Step 1 cleared: no ledger item removes the knots' coupling to the longitudinal sector in the transverse line (`STEP1_SCOPE_CHECK.md`). The fold proceeded on that condition.

## Carried housekeeping

The HK-5 bracket staged October 2, 2026 (`V4_89_HOUSEKEEPING_STAGING.md`, "the next fold carries") — PR #34 `bd1354d` merged 2026-10-02 22:06:58 UTC. Placed in full at the V4.88 record's estate sentence; at §2.91.U a pointer only, to keep the additions short.

## Repository state at fold (live `git ls-remote`, 2026-10-04 04:27:26 UTC)

`refs/heads/main` = `bd1354d9fb16cf3009b90dcedf2de774cef7e6c4` (PR #34). No canonical ledger on `main`.

## Project store

Not changed by this fold. The store has 5,829 units free; V4.89 is 5,266 B (5,115 characters) larger than V4.88, so the swap fits. The swap (delete V4.88, write V4.89) is left for the author's word, per the standing practice that the author authorizes each store swap.

## Verification

- `foldin_v4_89_lbc_bank.py` (md5 `c8e9b4a5daa9b8299c2329f13e2ba206`): anchors read from the file and asserted unique; every fragment lands exactly once; the §2.52 Open 3 Part VI row byte-identical and unique; reverse-splice reconstructs V4.88 byte-identically (asserted before output is accepted).
- `verify_v4_89_additive.py` (md5 `09ae37199431ae36490e6be7b3db5929`), independent of the fold script: line-level diff shows six change sites — the declared title and As-of rewrites, two pure insertions (the annotation paragraph and the changelog line), one in-line insertion (the §2.91.U pointer, zero characters removed), and the record region, where the old line is shown to be a pure-insertion subsequence of the new lines (+1,193 characters: the V4.89 record and the HK-5 bracket).
