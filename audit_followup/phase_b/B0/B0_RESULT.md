# B0 — Second-sound paper: all eight items already applied (no new draft)

**Plain-language summary.** The brief listed eight fixes to make before posting the second-sound paper, and asked to skip any already applied. All eight are already in the posting version, v1. That is the text the author approved on October 4 ("Approved draft"); its October 4 revision answered an outside review that raised the same points. So there is no new draft. v1 can be posted as approved.

Phase A changes nothing in the paper either. The paper's results are about a one-component soft-core supersolid, plus a second component used only to fill a vortex core. Phase A's verdicts (gravitational-wave polarization, the 16-component internal sector, the proton length, gravity) concern the program's own vacuum, which the paper does not use. If anything, A2's finding that texture matter radiates at every speed sharpens the paper's general point.

## Item by item (`b0_check.py`; v1 md5 `0dc9b1ea59384bdca33e9980b6cbb8ef`, as recorded in `lbc_bank/paper/APPROVAL_V1.md`)

| # | Brief item | Where v1 has it |
|---|---|---|
| 1 | Derive the vortex couplings from the Lagrangian (Secs. 6, 9, 10) | Sec. 6 derives ℒ₁ = −δρ(½\|v_s\|² − v·v_s) − ρ_n u̇·v_s, twice (the second derivation blind; S6). The density vertex comes from −δρθ̇ alone, enters with the same F_ν weights, and has a strength fixed by the circulation quantum, so "no filling of the core removes it" (line 114). The flow drives shear through −ρ_n u̇·v_s (line 113). Sec. 9 re-derives the Green's-limit statements for constant ρ_n and leaves the strain couplings explicitly unevaluated (line 143). The two unsupported claims were withdrawn on October 4. |
| 2 | Anchor the loss length to the proton's size; abstract to match the text and to refer to defects | Sec. 7: ξ ≳ 6×10³ m, "defects kilometres across"; "a defect of proton size (ξ ≈ 1 fm) falls short by about 19 orders" (line 129). Abstract: "survive only if defects are kilometres across (a proton-size one falls short by about 19 orders of magnitude)" (line 8). |
| 3 | The \|1 − c₂/c_T\| bound is one-sided; Coleman–Glashow; Green's-limit exception | Abstract: "tuned to within 10⁻²³ of the shear speed … or if it is faster than shear", followed by the Green's-limit exception (line 8). Eq. (4) is one-sided, 1 − c₂/c_T ≲ 1/(2Γ²), "the same order as Coleman and Glashow's bound" (line 131). |
| 4 | μ is both chemical potential and shear modulus | Resolved by renaming the chemical potential instead: it is μ_c (μ_u for the uniform state), and μ is the shear modulus only (lines 51, 96–98). The mixed ratio is now f_s M̃/μ, with M̃ the uniaxial modulus at fixed chemical potential (line 104). |
| 5 | P(c*²) holds for the χ denominator, not the monic polynomial | v1 states it for the monic polynomial with the 1/ρ_n: P(c*²) = −ρ_s(M − ργ)²/(ρ²ρ_n) (line 43). Re-derived symbolically: correct, and ρ_n·P(c*²) = −ρ_s(M − ργ)²/ρ² is the χ-denominator form the brief quotes. |
| 6 | Table 2: window slopes vs weights at one q (up to 9 %); f_s for g ≥ 28 | The Table 2 caption gives the cause and size: "by up to 9 % (at g = 12.7; 1.5 % at g = 13.5)" (line 70). f_s is filled at g = 44, 34 and 28 (0.0055, 0.018, 0.039), computed twice (closure/fs_rows*.py). |
| 7 | c₁/c₂ in the radiation estimate (34–36, ~10¹¹); reconcile 64–80 % with 0.81 | "c₁/c₂ = 34–36 … about 10¹¹" (line 125), matching ledger V4.91. The 0.81 is the g = 13.0 row, flagged as 0.04 below the coexistence boundary on the metastable side; the text's 64–80 % is the stable phase taken at Λ_c (line 90). |
| 8 | "Popular picture" → a proposed picture; AI-run checks in the acknowledgments | "Popular" no longer appears; the abstract says "one picture of this kind". The acknowledgments read "The checks were also made by AI agents, not by human referees" (line 161). |

On item 4, the brief asked to rename the shear modulus, while v1 renamed the chemical potential instead. Both remove the clash. If the author prefers the brief's version (for example G for the shear modulus), that is a typesetting change and would need a v1.1 build.

**What is left for the author:** posting v1 on Zenodo with the supplementary zip, then the journal submission (`lbc_bank/paper/VENUE_AND_SUBMISSION.md`). Nothing is posted.

## Files

| File | md5 |
|---|---|
| `b0_check.py` | `aec9d33146a57bd04c58282af1b6a582` |
| `b0_check_output.txt` | `495f23d194b97ab6bc78c1669b6f4e05` |
