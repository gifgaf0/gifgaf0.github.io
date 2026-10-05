# LBC second leg: closure memo

Two-leg closure of the numbers cited by the paper "Second sound breaks the common light cone of a supersolid vacuum". This was not a gate: no lock, and no fold rides on this memo. Written chat-side on 4 October 2026, after the merge of PR #36.

## Plain-language summary

**What happened.** The paper's numbers were computed a second time, independently and blind. On first comparison the two computations agreed on 108 of 112 numbers. I checked all four disagreements on my side, and every one was a defect in my first computation:
- **2D ground states.** They were not converged tightly enough. That made every sound speed in the crystal slightly too low, by 0.5–1 % for shear.
- **3D basis.** The plane-wave basis was too small. That made the 3D shear speeds up to 6 % too low.
- **Melting end.** The search for the end of the crystal branch mistook a collapsed, uniform state for the end of the branch.

**After correction.** I fixed the three defects and recomputed everything with my own code, otherwise unchanged. The two computations now agree on all 112 numbers within the comparator's tolerances:
- every speed and weight to 0.13 % or better;
- one weight read off at the melting boundary to 0.5 %;
- the loss-length results to 0.02 on the paper's log scale (4 % in the required length).

**Conclusions.** None changes:
- Second sound stays below the shear ("light") speed everywhere.
- It peaks at 0.79 of it on the metastable branch.
- The loss length stays about 39 orders of magnitude too short.

**One physical point is new.** Near the end of the metastable crystal branch, second sound does not approach the light speed. It softens toward zero, which is the crystal's spinodal instability.

## 1. What was run

| Item | Value |
|---|---|
| Dispatch | `LBC_SECOND_LEG_DISPATCH_INBAND.md`, md5 `e5153dc527bf989eed0261e8aed91831`, activation `ACTIVATE: LBC-2LEG-1` |
| Second leg (CC) | Branch `claude/new-session-rp548n`. Pre-consultation commit `667644a` (2026-10-04 17:48:05 UTC; checkpoint `lbc_cc_checkpoint.json`, md5 `b19d8b62ee0db41ddb8a2bd825757561`, identical on `main`). Comparator commit `bd7169e` (17:54:38 UTC). PR #36 merged as `a9b5cab` (18:09:13 UTC) |
| Embeds | E1–E4 as landed in `second_leg/dispatch_embeds/` match the dispatch manifest md5s. The comparator's "chat" side is the first leg's sealed checkpoint E5 (`299afd11…`) |
| First comparison | 112 checks: 108 PASS, 4 MISS, 107 CC-only extras (`second_leg/compare_out.json`) |

Order of operations checked chat-side:
- the checkpoint was committed before the comparison commit;
- neither checkpoint was edited afterwards;
- the CC leg read E6, the first leg's scripts, only to diagnose the misses and ran none of them, per its return note.

## 2. The four misses, adjudicated chat-side

### (a) `2d.13.cT` and `2d.22.cT_30deg_kf005`: second leg right; diagnosis confirmed

**Second leg's diagnosis.** The first leg's 2D states are not stationary enough. The negative translational zero mode is clipped away, and every acoustic branch is lowered by a constant offset in ω².

**Chat-side test.** I rebuilt the first leg's state at each of its own a* values. Each state was relaxed and polished exactly as before, then converged by L-BFGS at fixed norm (`gsolve2d.py`). I then reran the first leg's own BdG and mode identification, unchanged.

| Quantity | First leg | Converged (chat) | Second leg |
|---|---|---|---|
| GP residual, all 22 points | 1.3–3.9 × 10⁻³ | ≤ 3.8 × 10⁻⁵ | ~10⁻¹⁴ |
| Lowest ω² near Γ (Ward check), all points | −0.013 … −0.056 (clipped) | +0.0002 … +0.005 (the physical second-sound mode) | — |
| c_T, g = 22, 30°, kf = 0.05 | 5.7462 | 5.80388 | 5.80493 |
| c_T, g = 13 (LSQ, kf 0.03–0.10) | 4.4080 | 4.45459 | 4.45536 |
| c_T, g = 22, kf = 0.005 (≈ q → 0) | 5.4… at kf 0.02, 4.13 at kf 0.01 (falling) | 5.81163 | 5.81241 (q → 0) |
| Static route c_T = √(μ/ρ_n), g = 22 (no BdG) | 5.81137 | — | 5.81245 |

**Verdict.** The diagnosis is correct. The signature is visible in the first leg's own output: ω_T/q fell as q → 0. Converging the state removes it, and the first leg's BdG then agrees with its own static route to 4 × 10⁻⁵. The bias at the paper's wavevectors was 0.45–1.1 % in c_T and 0.15–0.4 % in c₁. The effect on c₂, the weights and f_s was negligible, as the second leg said. Logs: `jobA_2d.log`, `t_g22.log`, `reconverge2d_g22.json`.

### (b) `3d.cT_min`: second leg's number right; the mechanism is the basis, not the ground state

**Second leg's diagnosis.** A ground-state residual of 3.05 × 10⁻³ produces the same ω² offset as in 2D.

**Chat-side finding.**
- **The state was stationary.** The first leg's in-basis state already satisfies the GP equation within its basis: the projected residual is 3.1 × 10⁻¹³. The reported 3.05 × 10⁻³ was the unprojected residual, which includes the out-of-basis tail of the nonlinear term.
- **The basis was the defect.** At |G| ≤ 22 (1,355 waves):
  - the in-basis energy sits 4.3 × 10⁻⁴ above the converged one;
  - the BdG interaction kernel is truncated, so the three translational Goldstone modes get negative ω² (clipped to 0 near Γ);
  - the transverse speeds at q = 0.15 come out 5.4 % low.
- **The larger basis fixes it.** At |G| ≤ 30 (3,455 waves; in-basis energy 6 × 10⁻⁷ above the full grid), the first leg's own `bdg_weights` gives the following (`jobB_3d.log`):

| q = 0.15 | Chat-side, \|G\| ≤ 30 | Second leg |
|---|---|---|
| c_T min / max | 7.75036 / 8.04104 | 7.74935 / 8.04007 |
| c₂ | 0.47059 | 0.47056 |
| c₁ (basal) | 16.1377 | 16.1372 |
| F₂, Z₂/Z₁, S₂ (basal) | 0.0016668, 0.05735, 0.6629 | 0.0016666, 0.05735, 0.6629 |
| c_κ | 9.38466 | 9.38465 |

### (c) `melting.branch_end_g`: second leg right

**From the first leg's own record.** At g = 12.45 the selected state is the uniform one: a* = 1.5655 sits at the edge of the scan window, the contrast is 2.0 × 10⁻⁷, and ε_c = πg/2 exactly. So the "branch end at 12.47" was an artifact of the selection rule.

**Chat-side continuation** (`jobC_melt.py`: seeded relaxation at the second leg's a*, converged, the first leg's BdG with the raw lowest ω²):

| g | Crystal? | ε_c − ε_u | Lowest ω², \|q\|a/2π = 0.03 / 0.05 | c₂/c_T (chat) | c₂/c_T (second leg) |
|---|---|---|---|---|---|
| 12.55 | yes | +0.0028 | +0.154 / +0.451 | 0.77384 | 0.77384 |
| 12.50 | yes | +0.0095 | +0.137 / +0.413 | 0.75841 | 0.75841 |
| 12.45 | yes | +0.0158 | +0.106 / +0.347 | 0.72851 | 0.72851 |
| 12.40 | yes | +0.0216 | +0.041 / +0.212 | 0.65991 | 0.65991 |
| 12.37 | yes | +0.0248 | **−0.050** / +0.042 | undefined | undefined |
| 12.35 | lost (solver collapsed to uniform) | — | — | — | — |

- **The softening branch.** It is second sound (c₂ → 0), so c₂/c_T falls toward the instability rather than rising.
- **Onset (two-leg).** The long-wavelength instability at |q|a/2π = 0.03 sets in between 12.37 and 12.40 on the chat side. The second leg puts it at 12.3835 (q → 0: 12.395).
- **Fold at 12.3267 (second leg only).** The chat-side loss of the crystal at 12.35 is inconclusive rather than contradictory: near the fold the second leg needed an a-walk with Newton–Krylov solves. The paper therefore cites the instability onset, not the fold.

## 3. Corrected first leg against the second leg

The corrected first leg is `lbc_chat_checkpoint_v2.json`, md5 `aa01ea0a64b8951a472590cca70e4e44`, labelled `chat-v2-corrected-post-comparison`.
- **What changed.** It was built after the comparison by `build_v2.py`, from `jobA_2d.json`, `jobB_3d.json` (|G| ≤ 30, q = 0.15, all directions, as the second leg defined it) and `jobC_melt.json`.
- **What did not change.** The static hydrodynamic route and f_s are carried over from v1, because the defects do not touch them; the second leg agrees with them to ≤ 1.3 × 10⁻⁴.
- **The v1 checkpoint is untouched.**

Comparator (E3 rules, unchanged) against `lbc_cc_checkpoint.json`: **112 checks, 112 PASS, 0 MISS** (`compare_v2_out.json`). Largest differences:
- **2D:** speeds ≤ 0.08 %, weights ≤ 0.13 %, a* ≤ 0.024 %, f_s ≤ 0.013 %.
- **3D:** ≤ 0.013 %.
- **Static hydrodynamics:** ≤ 0.05 %.
- **Melting:** Λ_c 13.0408 against 13.0446 (the first leg interpolates, the second leg root-finds); ratios ≤ 0.0004 absolute; F₂ at Λ_c 0.4146 against 0.4125 (0.5 %).
- **`branch_end_g`:** the chat value 12.37 is a bound (the lowest g at which the crystal was found), not a fold.
- **Loss:** ≤ 0.02 orders; ξ_req ≤ 4.3 %; Eq. (3) coefficient 0.57 % (at the dispatch's c_T = 7.68).

**Register.** The paper-cited numbers are two-leg, with one exception: the fold location (12.33) is second-leg only and is not cited.

## 4. What changes in the paper

- **2D shear speeds** rise by 0.45–1.1 % (e.g. 5.77 → 5.80 at g = 22) and c₁ by ≤ 0.4 %. Tables 1–2 now carry the corrected values; Table 2 gains a g = 12.4 row.
- **The ratio c₂/c_T** is 0.77 at Λ_c (was 0.78). The metastable peak is 0.79 near g = 12.7 (was 0.80). The branch then softens to the long-wavelength instability at g ≈ 12.38–12.40 (was "ends near 12.47"). The c₂ → 0 end connects to the labile ether of Sec. 9.
- **3D:**
  - c_T is 7.75–8.04 (was 7.3–8.2) and c₁ is 16.1–17.0 (was 15.8–16.9);
  - c₂ = 0.471 (was 0.477);
  - basis 3,455 waves, with the reason stated;
  - Eq. (3) coefficient ≈ 1.5 × 10⁵, using the corrected mean c_T ≈ 7.85 (was 1.3 × 10⁵ with 7.68), so ξ ≳ 6 × 10³ m and the deficit is about 39 orders.
- **The method paragraph** states the convergence criterion and what a looser one does.
- **Ranges:** S₂ 64–80 % in the stable phase (was 63–81 % over all rows); 1 − c₂/c_T between 0.21 and 0.94.
- **Unchanged:**
  - every conclusion;
  - the closed form for F₋;
  - the static route;
  - the weights (≤ 0.6 % shifts);
  - the drag coefficient 1/4π (both legs);
  - the loss-length re-evaluation (−39.2 orders on both legs).

## 5. What this implies for the ledger (for the author; nothing folded)

**§2.91.V (V4.89) quotes three items the closure changes:**
- "c₂/c_T rises to 0.78 at the coexistence boundary": now 0.77.
- "peaking at 0.80 on the metastable continuation (g ≈ 12.7) before turning down": now 0.79, then second-sound softening to a long-wavelength instability at g ≈ 12.38–12.40, two-leg.
- "Paper-cited numbers carry a prepared second-leg dispatch (not run)": now run and closed, two-leg after correction.

Unchanged in §2.91.V: −39.2 orders, ξ_req ≈ 2 × 10⁴ m, Z₂/Z₁ = 0.33 (0.336), F₂ = 5.1 %, the static share of 67 %, the 3D values, and "never 1".

The c₂ = 1.765 quoted there is G-TSH1's windowed value. The two-leg least-squares value over |q|a/2π ∈ [0.03, 0.10] is 1.803 (1.817 at q → 0). A staged V4.90 record is in `V4_90_STAGING.md`.

**Instrument note (F9).** The permanent F9 falsifier admits states that bias 2D transverse speeds low by 0.5–1.1 % at |q|a/2π ≤ 0.10, and by more at smaller q. Its thresholds are a post-polish residual ≤ 5 × 10⁻³ and a raw w²min > −0.05.
- **G-TSH1.** Its canonical c_T = 5.7749 and R_T = 0.52284 came from such a state (residual 1.9 × 10⁻³, w²min −0.015). Its locked windows sit at larger q, where the offset matters less.
- **G-TSH3.** Its states were descended to Ward ≤ 3.7 × 10⁻⁸ and are unaffected.
- **Recommendation.** Check whether any G-TSH1/G-TSH2 number quoted below 1 % inherits the offset. Nothing here re-litigates a verdict.

## 6. Disclosures carried from the second leg's return

- **Extractor.** The dispatch's extractor was blocked by the CC session's permission check until the author's go-ahead.
- **Literature hosts.** A CC sub-agent probed several literature hosts for the Astrakharchik–Pitaevskii paper, including one shadow-library host it should not have tried. Every request was refused and nothing was retrieved. The drag coefficient rests on two independent derivations plus secondary quotations; it equals the first leg's.
- **Notes edit.** `QA_NOTES.md` was edited before the pre-consultation commit, to attribute one remark to the CC orchestrator's prompt.

## 7. Files (`lbc_bank/closure/`)

| File | md5 | What |
|---|---|---|
| `gsolve2d.py` | 96856f30 | Tight 2D ground state (L-BFGS at fixed norm) |
| `reconverge2d.py` → `reconverge2d_g22.json` | fc9c222f / 2e8e5884 | First check of the 2D diagnosis at g = 22 |
| `t_g22.py` → `t_g22.log` | af784bf4 | q → 0 speeds at g = 22 (Table 1 caption) |
| `jobA_2d.py` → `jobA_2d.json`, `.log` | a2600ecf / 25dd3b22 | All 2D points of Table 2, converged |
| `jobB_3d.py` → `jobB_3d.json`, `.log` | 6558653a / 5428bf10 | 3D at \|G\| ≤ 22 (reproduces the first leg) and ≤ 30 |
| `jobC_melt.py` → `jobC_melt.json`, `.log` | c1d9e429 / b4e3f722 | Melting end, 12.55 → 12.35 |
| `chi_g22.py` → `chi_g22_v2.json` | 14a25355 / 6024804c | Static response at g = 22 (Table 1) |
| `build_v2.py` → `lbc_chat_checkpoint_v2.json`, `paper_tables_v2.json` | fb670f17 / aa01ea0a / c7aca424 | Corrected first leg in the schema; paper tables |
| `compare_v2_out.json` | 892a4bf1 | Comparator v1.0 rules: 112/112 |
| `V4_90_STAGING.md` | — | Proposed V4.90 record (not folded) |

The scripts import the first leg's instruments by the session paths listed in `../README.md`.
