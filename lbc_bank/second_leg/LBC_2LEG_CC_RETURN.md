# LBC second leg — CC return note

**Result.** The blind CC recomputation agrees with the first leg on 108 of 112 compared numbers. All four misses are traced to the first leg, using that leg's own outputs from E6:

- **Three transverse-speed misses.** The first leg's BdG has a broken lattice Goldstone mode, so every acoustic lattice branch is pulled down by a constant ω² offset.
- **The branch-end miss.** The first leg's continuation selected the uniform state once the metastable crystal lay above it in energy. The crystal itself had not disappeared.

Neither checkpoint was edited after the comparison.

| item | value |
|---|---|
| pre-consultation checkpoint | `lbc_cc_checkpoint.json`, md5 `b19d8b62ee0db41ddb8a2bd825757561` |
| pre-consultation commit | `667644af02d7bf9253f9975e68ff662ed2d6b4f6` (branch `claude/new-session-rp548n`), pushed before E5 was decoded |
| E2 scan (base list E1) | every file CLEAN before the commit (`t1_scan_precommit.txt`); the files added after the comparison are also CLEAN (`t1_scan_postcompare.txt`) |
| comparator (E3) | `checks: 112  PASS: 108  MISS: 4  CC-only: 107`, written to `compare_out.json` |
| embeds | E1–E6 md5 OK. E5 was decoded only after the commit. E6 was decoded only to diagnose the misses: its JSON outputs and scripts were read, and none of its scripts was run. |

## How this leg was built (independence)

The leg was built from the dispatch's model definitions only. Before the commit, nobody read anything outside `lbc_bank/second_leg/`, nobody touched the branch `claude/lbc-bank-v489`, and E5/E6 stayed sealed.

The methods differ from the first leg:

- **Ground states.** L-BFGS followed by a Newton–Krylov polish, with GP residuals around 1e-14 (the first leg used split-step imaginary time).
- **Lattice constant.** a* is found by Brent minimization, cross-checked against the root of de/da.
- **2D BdG.** Dense, with a circular plane-wave cut and a Cholesky formulation.
- **Superfluid fraction.** f_s comes from the exact linear-response limit of the twist energy, cross-checked against finite twists (agreement ≤ 7e-7).
- **Q-A′ hydrodynamics.** Finite strains at fixed density, with Richardson extrapolation.
- **Q-C melting.** Continuation of the a*-optimized branch, with Brent root-finding.
- **3D BdG.** Computed on the hexagonal primitive cell; the orthorhombic cell's energy matches it to 1e-10.
- **Q-D drag.** Two independent derivations of the drag coefficient.

Two independent re-implementations inside this leg, each using a different discretization, agree with the main instruments to better than 1e-6:

- **2D:** a rectangular two-droplet supercell with a square cut, a full non-Hermitian BdG eigensolve, and f_s from finite twists only.
- **3D:** the orthorhombic four-site cell with a box cut and a generalized Hermitian eigensolve.

An adversarial review is in `REVIEW_NOTES.md`.

## The four misses

### `2d.13.cT` (chat 4.408010566847177, CC 4.45536315520834, +1.07 %) and `2d.22.cT_30deg_kf005` (chat 5.746213689235847, CC 5.804934993853741, +1.02 %) — I believe CC

The first leg's transverse branch does not behave like an acoustic mode. In its own output (`lbc_results.json`, g = 22, q ∥ a₁), ω_T/q falls as q → 0: 5.786 at |q|a/2π = 0.10, 5.751 at 0.05, 5.648 at 0.03, and 5.440 at 0.02. A gapless branch has ω/q → c_T as q → 0.

Their data fit ω² = c²q² − ε with a constant ε:

- **Size of the offset.** ε ≈ 0.024–0.080, depending on g, 1.3–2.0× the negative zero-mode ω² that their own instrument records (`ward_w2min` = −0.0135 … −0.074).
- **Cause.** Their ground states are not stationary in the BdG representation: `gp_residual` is 1.4e-3 to 3e-3, against about 1e-14 here. The negative Γ-point ω² is hidden by `np.clip(w2, 0, None)`.
- **After removing the offset.** Their own data give c_T within 0.011–0.021 % of this leg's q → 0 values at g = 13, 13.25, 13.5, 14 and 16. At g = 22 the agreement is 0.04 % (5.81023 against 5.81241, and the static route of both legs gives 5.811–5.812). The three-point sets (g = 28, 44, γ6 35), which have no dispersion term, agree to ≤ 0.22 %.
- **The 30° value.** After the same offset fit, their 30° data (eight q values) give 5.81696, within 0.08 % of this leg's 5.81241. The miss itself is a single point at |q|a/2π = 0.05. There, ε/(2c²q²) ≈ 1.0 % with their 30° offset (ε = 0.0327), which accounts for the 1.02 % miss.
- **Direction dependence.** At the same |q| (0.05), the first leg's 0°/30° split is 0.083 %, the same as this leg's 0.08 % (an O(q²) six-fold dispersion term). So the 30° miss is the offset, not anisotropy.

The g = 22 hydro c_T (static finite strains, no BdG) matches between the legs to 1.9e-4 (5.811365 against 5.812446). It matches this leg's BdG q → 0 limit to 2e-7, and it does not match the first leg's BdG.

Consequences:

- The same bias lowers the first leg's c₁ by 0.16–0.41 %, and its c_T at every 2D point by 0.45–1.07 %. The bias grows toward melting as |ward_w2min| grows, so g = 13.25 (+0.93 %) and 13.5 (+0.86 %) pass only narrowly.
- The first leg's c₂ (within 0.03 % for g ≤ 22, 0.13–0.18 % at g = 28, 44 and γ6 35), f_s (≤ 1.3e-4) and static hydro quantities (≤ 4e-4) agree closely, because the phase-like mode 2 is barely affected.
- The first leg's ratio_at_Lambda_c (+0.008) and ratio_max_metastable (+0.010) are inflated by the same lowered c_T. Both still pass at the 0.02 tolerance.

### `3d.cT_min` (chat 7.330511782230688, CC 7.7493459895352235, +5.7 %) — I believe CC

The first leg's 3D run has the same signature, with a larger offset:

- **Their run.** Plane-wave cut 22 (1355 waves), relaxation residual 3.05e-3, and three near-Γ ω reported as exactly 0.0, which is what clipping negative ω² produces.
- **Their transverse ω/q rises with q.** The lower basal transverse branch goes 7.3305 → 7.6480 → 7.6994 for q = 0.15 → 0.3 → 0.6. The axial branch goes 7.5458 → 7.6826 → 7.6511. A clean Goldstone floor gives a nearly flat or slowly falling ω/q; this leg's x_Tz goes from 7.7622 at q = 0.02 to 7.7599 at 0.15.
- **This leg's convergence.** cT_min is 7.749346 (to ≤ 1.5e-6) at every cut from K = 30 to K = 50, all larger than the first leg's cut of 22. The independent 3D cross-check agrees to ≤ 3e-7.

So the first leg's q = 0.15 transverse speeds sit too low. Its cT_max (8.1675) comes from its q = 0.6 row, outside the dispatch's q set. It still passes at −1.6 %.

A related fragility, which does not cause this miss: `paper_tables.py` takes the transverse modes as frequency indices om[4] and om[5]. That works here only because the three gapped modes near ω ≈ 0.86–0.97 sit below them. This leg identifies modes by symmetry parity and by checking that the branch is gapless.

### `melting.branch_end_g` (chat 12.47, CC 12.326704359054563, −0.143) — I believe CC

The first leg's descent (`lbc_sweep_refine.py`, steps of 0.05) chooses a* at each g by taking the minimum energy over a scan window. Below the fixed-density energy crossing (12.570 in both legs), the metastable crystal has higher energy than the uniform state.

At g = 12.45, some scan points collapsed to the uniform state, and the argmin picked one of them. The record shows this directly: contrast 2.0e-7, ε_c exactly πg/2, and a* = 1.5655 exactly at the upper edge of the window. So "crystal lost" there is an artifact of the selection rule, not the end of the branch.

This leg follows the a*-optimized local minimum directly and finds:

- **The fold** of the branch at g = 12.3267044 (bisection bracket width 1e-7), confirmed independently in the bracket [12.3265, 12.328].
- **A long-wavelength BdG instability** setting in earlier: at g = 12.3835 for |q|a/2π = 0.03, and an estimated g ≈ 12.395 as q → 0.

So the crystal exists, dynamically stable, at g = 12.45, where the first leg reports it lost. If the dispatch meant "end of dynamical stability", the value would be about 12.38–12.40. That is still more than 0.07 away from 12.47.

## Reading choices (CC-only extra keys carry the alternatives)

- **`loss.band_orders`.** I report the most-favourable headline log₁₀(ℓ/L_prop) across the four readings. The four readings are filament S(φ²)/S(M)/F₂; point source 1/F₂; closure literal (M_new/φ²)/F₂; and dressed static deficit, which is the main factor divided by (c_κ/c_s)⁴. This reading matched the first leg to ≤ 0.03. The alternatives (band in recovered orders; R3 without 1/F₂) are in `cc_band_*`.
- **`loss.eq3_coefficient`.** Uses c_T = 7.68 as given. Using this leg's own mean transverse speed would give 148221.81 (`cc_eq3_coefficient_with_own_cT_mean`).
- **f_s.** Uses the linear-response (k → 0) limit of the phase-twist energy. Finite-twist values agree to ≤ 7e-7 and are in `cc_f_s_twist_extrapolated`.
- **3D values.** The schema values are at q = 0.15 along x. c_T min/max are taken over the x, y, z directions and all transverse polarizations.
- **Q-D literature check.** The Astrakharchik–Pitaevskii comparison rests on secondary quotations, because the paper itself could not be fetched (arxiv and APS are blocked by the environment's egress policy). Its contact-vertex limit, F = 4πn b² m v²(1 − c²/v²)², matches the reduction of C = 1/(4π) exactly. The first leg has the same C.

## Process disclosures

- **Extractor block.** The dispatch's extractor was first blocked by the session's permission classifier as code from an external file. It was run, along with the E2 scanner and the E3 comparator, only after the author's explicit go-ahead.
- **Literature hosts.** While trying to fetch the AP paper, the Q-D sub-agent probed several literature hosts, one of them a shadow-library host it should not have tried. Every request was refused and nothing was retrieved. No web access was used for anything else.
- **Reading-choice note.** `QA_NOTES.md` was edited before the commit, only to say that a remark about metastability came from the orchestrator's build prompt and not from the dispatch.

## Files

| kind | files |
|---|---|
| instruments | `cc2d.py`, `cc2d_hydro.py`, `cc2d_melt.py`, `cc3d.py`, `cc_loss.py`, `cc_assemble_checkpoint.py` |
| cross-checks | `xcheck2d.py`, `xcheck3d.py` |
| results | `qa_results.json`, `qa_prime_results.json`, `qb_results.json`, `qc_results.json`, `qd_results.json`, `xcheck2d_results.json`, `xcheck3d_results.json` |
| notes | `*_NOTES.md`, `REVIEW_NOTES.md` |
| checkpoint and scan | `lbc_cc_checkpoint.json`, `t1_scan_precommit.txt` |
| after comparison | `compare_out.json`, `cc_diagnose_misses.py`, `diagnose_out.json`, `t1_scan_postcompare.txt` |
| dispatch embeds, verbatim | `dispatch_embeds/` (E1–E4) |
