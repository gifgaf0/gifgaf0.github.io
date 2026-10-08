# Public calculator, archived (Step 2d)

**Plain-language summary.** The public calculator on gifgaf0.github.io is very likely still live. The repository serves `main` as a website, and `main` carries "SQT Geometric Mass Calculator v3" (the F4 check; the site itself could not be fetched from here). Two ways to archive it are prepared. **Nothing is deployed.**
- **Option A: keep the calculator, with a banner.** The Phase B v3.1 page gets one line at the top, worded as the brief gives it.
- **Option B: replace the page with a stub.** A one-screen page says the calculator is archived and links to the v3.1 page, moved under `archive/`.

| File | What it is |
|---|---|
| `index_v3_1_archived_DRAFT.html` | **Option A.** The Phase B v3.1 draft (`phase_b/B3/site/index_v3_1_DRAFT.html`, md5 `b7fb8b39…`), plus the banner "Archived, V4.97: a fitted mass table with named inputs; the program it belonged to is closed." The banner is plain HTML above the app, so it shows even if the page's scripts fail. Two hunks (the banner and its style); removing them gives back the v3.1 draft byte for byte |
| `index_stub_DRAFT.html` | **Option B,** the new `index.html`. It says that the page hosted a calculator for a fitted mass table with named inputs, that the program was closed in October 2026 (ledger V4.97), and where the archived calculator is |
| `archive/calculator_v3_1.html` | **Option B,** the archived calculator. It is the same file as Option A, and the stub's link points to it |
| `make_archive_drafts.py` | Builds all three from the v3.1 draft. It checks the source md5 and the reverse splice (`make_archive_output.txt`) |

**Checked.** In a headless browser, the banner renders with the exact text, and the stub's link resolves to `archive/calculator_v3_1.html`. The calculator app itself is the Phase B v3.1 draft, unchanged, which was render-checked in Phase B (`phase_b/B3/site/render_v3_1_DRAFT.json`).

**To deploy** (your step, not done here):
- **Option A:** copy `index_v3_1_archived_DRAFT.html` to `index.html` on `main`.
- **Option B:** copy `index_stub_DRAFT.html` to `index.html` and `archive/calculator_v3_1.html` to `archive/` on `main`.

Either way it goes live on GitHub Pages within minutes.

**Optional, not done.** The page loads React and Babel from unpkg without exact versions (`react@18`, `@babel/standalone`). For an archive meant to keep working, pinning exact versions would protect it from future library changes.
