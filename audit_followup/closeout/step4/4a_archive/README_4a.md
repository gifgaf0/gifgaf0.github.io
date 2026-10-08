# Paper VII and the two store calculators, archived at V4.97 (Step 4a)

**Plain-language summary.** Paper VII and the two calculators kept in the project store are prepared as archived records. Each starts from its Phase B draft, which already carries the October corrections, and gets four changes:
- the corrections are marked as applied, not "draft";
- Paper VII's §10, on gravitational waves crossing a conformal boundary, is removed, and a short note stands in its place;
- the mass relation called "Theorem 1" is renamed **Fit 1**, because it is a leading-order fit with named inputs;
- each file carries an "Archived at V4.97" header, and each calculator also shows a banner line at the top of its page.

Nothing is deployed or deposited.

| File | md5 | From |
|---|---|---|
| `sqt_paper_VII_ARCHIVED_V4_97.md` | `420b1f4d73bb5b1ce763bb7d02667262` | `phase_b/B3/paper_vii/sqt_paper_VII_oct2026_DRAFT.md` (`ccecfded…`) |
| `SQTCalculator_v2_1_ARCHIVED_V4_97.jsx` | `2b34a35e3c3e613e766fcc5e5a387fe8` | `phase_b/B3/store/SQTCalculator_v2_1_DRAFT.jsx` (`abad7f3d…`) |
| `sqt_v19_1_ARCHIVED_V4_97.jsx` | `859ba79fa4103f4602e107ae6be89e15` | `phase_b/B3/store/sqt_v19_1_DRAFT.jsx` (`c3dc019f…`) |
| `make_archived.py` | | Builds all three. Every replacement is anchored and counted, and the results contain no "Theorem 1" and no "DRAFT" label (`make_archived_output.txt`) |
| `v21arch.json`, `v191arch.json` | | Offline render checks of the two calculators (React 18, Babel, headless Chromium). Both compile and render with no errors except the server's missing favicon. Every tab and button of v1.9.1 was clicked through |

## What changed

**Paper VII**
- An "Archived at V4.97" note follows the title. The status note now reads "applied in this archived version", and the subtitle line reads "corrections: applied".
- **§10 is removed** (6,836 characters). A note under the heading "§10 Removed at V4.97 (formerly Theorem 5 (Candidate): Cosmological Echoes and Gravity Filtration)" says what the section was. It also says why it is gone: the vacuum has no carrier for gravitational waves (ledger §2.92.A). Section numbers stay as they were. The later mentions of §10, F_g, T_g, OP.9 and OP.10 (Chapter V, Chapter VI's register, §12–§14, the bibliography notes) are left in place, and the note says they refer to the removed text.
- **"Theorem 1" → "Fit 1"** in 23 places, plus three plural forms:
  - "Theorems 1, 3, and §10" → "Fit 1, Theorem 3 and the former §10";
  - "Theorems 1 and 2" → "Fit 1 and Theorem 2";
  - "Papers I–VI establish Theorems 1–3" → "… establish Fit 1 (formerly Theorem 1) and Theorems 2–3".

**SQTCalculator v2.1:** an archived header comment, a visible banner above the title, and "v2.1 DRAFT" → "v2.1 … Archived at V4.97" in the comment and the footer. It never says "Theorem 1".

**v1.9.1:** the same header comment and banner, and the version labels changed in three places. "Theorem 1" / "THEOREM 1" → "Fit 1" / "FIT 1" in four places, including the Mass Audit heading "FIT 1 · LOCAL MASS OPERATOR — LEADING-ORDER FIT AUDIT".

**Banner text (both calculators):** "Archived at V4.97: a leading-order fit with named inputs; the program it belonged to is closed (Master Ledger §2.97)."

## For you to decide

- **v1.9.1's "Cosmic Echoes" tab** is the calculator's version of Paper VII §10: gravitational waves crossing an aeon boundary, attenuated by κ/4. The brief named only Paper VII's §10, so the tab is kept as written, under the archive banner. Removing it is one more anchored edit.
- **Where the store copies live.** These files replace the store calculators and Paper VII only when you put them there. The project store is nearly full: see the report.
