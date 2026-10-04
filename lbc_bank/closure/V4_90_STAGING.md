# V4.90 — staging note (not folded)

**Plain-language summary.** This proposes one short ledger record for the outcome of the second computation:
- the paper's numbers are now confirmed by two independent computations;
- three small first-computation defects are logged as honesty items;
- §2.91.V gets one bracket with the corrected values (0.77 and 0.79 instead of 0.78 and 0.80) and the new detail that second sound softens to zero at the end of the metastable branch.

Nothing here edits V4.89. It needs your word to fold.

## Base

- **Ledger:** V4.89, `SQT_Master_Ledger_v4_89_CANONICAL.md`, md5 `db01bd273629ce7a385ff3c7fb6efdfc`, 1,773,873 B. The project-store copy is byte-identical, read back on 2026-10-04.
- **Repository:** `main` = `a9b5cab` (PR #36, the second leg, merged 18:09:13 UTC). PR #35 (the V4.89 estate, `lbc_bank/`) is open and mergeable; this closure rides on it.

## Proposed insertions (additions only)

### 1. Title and As-of

Prepend to the As-of line:

> **As of:** October 4, 2026 (V4.90 fold — **the paper-cited LBC numbers closed TWO-LEG (§2.91.V bracket):** the blind CC second leg (PR #36) matched the first leg on 108/112, and the four misses traced to the first leg: 2D states under-converged within F9, the 3D basis at |G| ≤ 22, and a scan-edge selection at the melting end. Corrected first leg against CC: 112/112. c₂/c_T is 0.77 at Λ_c and peaks at 0.79 on the metastable branch, then second sound softens to a long-wavelength instability at g ≈ 12.38–12.40 — never 1. Loss length unchanged at −39.2 orders.** Full V4.90 record below. V4.89 fold (October 4, 2026) — …

### 2. Fold-in record (before the V4.89 record)

> **V4.90 fold-in record (October 4, 2026):** BANKING ANNOTATION, no gate; register upgrade of the paper-cited numbers only.
> - **Second leg:** CC, blind, branch `claude/new-session-rp548n`, from the dispatch `e5153dc5` (activation `ACTIVATE: LBC-2LEG-1`). Pre-consultation commit `667644a`; checkpoint `b19d8b62`; comparator commit `bd7169e`; PR #36 merged `a9b5cab`.
> - **First comparison:** 112 checks, 108 PASS, 4 MISS, all four first-leg:
>   - **H-LBC-1:** 2D states passing F9 (residual 1.3–3.9×10⁻³, w²min −0.013 … −0.056) bias the acoustic branches by a constant ω² offset, so c_T is 0.45–1.1 % low at |q|a/2π ≤ 0.10.
>   - **H-LBC-2:** 3D at |G| ≤ 22 gives clipped negative Goldstone ω² and c_T 5.4 % low at q = 0.15. The in-basis state was stationary (projected residual 3×10⁻¹³); the cause is the basis.
>   - **H-LBC-3:** at g = 12.45 the scan's argmin took a collapsed uniform state (a* at the window edge, contrast 2×10⁻⁷), so the "branch end 12.47" was an artifact.
> - **Correction:** chat-side, own code, defects fixed (`lbc_bank/closure/`). Checkpoint v2 `aa01ea0a`, labelled post-comparison; v1 untouched. Against CC: 112/112 (2D ≤ 0.13 %, 3D ≤ 0.013 %).
> - **Fold of the a*-branch (12.3267):** second leg only, not cited.
> - **Disclosures:** **D-LBC-CC-1:** a CC sub-agent probed a shadow-library host while fetching a reference; refused, nothing retrieved. **D-LBC-CC-2:** the extractor was blocked by the CC permission check until the author's go-ahead.
> - **F9 note:** the falsifier's thresholds admit the H-LBC-1 offset. G-TSH1's canonical numbers came from such a state (its windows sit at larger q); G-TSH3 is clean. Flagged for a check; no verdict re-litigated.
> - **Unchanged:** §2.52 Open 3 untouched; no Part VI row; no retraction.

### 3. §2.91.V bracket

Insert after "No KC re-litigated; no observable; §2.52 Open 3 untouched." (×1 in V4.89):

> [→ V4.90: **two-leg** (CC second leg PR #36; corrected first leg 112/112; `lbc_bank/closure/LBC_2LEG_CLOSURE_MEMO.md`).
> - **Corrected values:** c₂/c_T = 0.77 at Λ_c (13.04); metastable peak 0.79 near g ≈ 12.72; then second sound softens (c₂ → 0) to a long-wavelength instability at g ≈ 12.38–12.40, two-leg. The crystal branch folds at 12.33 (CC only). The first leg's "branch end 12.47" is withdrawn (H-LBC-3). Never 1.
> - **Transverse speeds:** g = 22 c_T = 5.80 (LSQ), 5.812 (q → 0), against the static 5.811. The 3D shear speeds are 7.75–8.04 (was 7.3–8.2). c₂ at the paper's window is 1.80; the 1.765 above is G-TSH1's window value.
> - **Unchanged:** Z₂/Z₁, F₂, the static share, −39.2 orders, ξ_req and the drag prefactor 1/4π (both legs).]

### 4. Changelog

> V4.90 (October 4, 2026): additions only — title/As-of; the V4.90 fold-in record; one bracket at §2.91.V. Nothing prior modified.

## Checks to run at fold time

The V4.89 discipline applies:
- anchors read from the file and asserted unique;
- a reverse splice equal to V4.89 byte for byte;
- an independent additivity check;
- `git ls-remote` at fold time.

Estimated size is about +2.4 kB. Whether the store has room for the swap needs checking at fold time.

*No fold is authorized by this note.*

---

*Folded on the author's word ("Go ahead and fold v 4.90", October 4, 2026, 14:16 PDT) as V4.90, md5 `ef69a573`. See `../estate/FOLD_AUTHORIZATION_V4_90.md`. The ledger text is this note rendered as single paragraphs, with one clause added to the §2.91.V bracket (the 3D ratio c₂/c_T ≈ 0.06, was 0.062).*
