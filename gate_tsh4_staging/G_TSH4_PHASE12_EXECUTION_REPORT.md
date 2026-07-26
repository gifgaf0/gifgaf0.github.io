# G-TSH4 — PHASE 1–2 EXECUTION REPORT (chat leg)
**Gate:** G-TSH4. Base canonical **V4.71** md5 `9517f4fb7aa2de65b0b4a69985962d8f`.
**Pre-registration:** md5 `e66b964d4467fcb9a5f328ef0db80a35` + **Amendment 1** (md5 sealed in outputs).
**Instruments (md5):** phase12 core `2eb95352`; polish2 `6b38db6f`; reeval2 `2cdd07df`; stress probe `95b191d1`; fine-grid check `3ce9ba13`; BdG extension `a0c4be36`; ext analysis `20c95167`; **quarantined mapper `4ba2d06f`** (θ₁, θ₂ appear only there; run last). Results `16b1fb46`; verdict `c72b6724`.
**STATUS: chat leg complete. Everything herein is SINGLE-LEG PROVISIONAL pending CC and C1–C6.**

---

## §1. S-CLASS INSTRUMENT FINDING — the split-step energy bias (H-protocol, self-caught)

**Discovery chain, in order, nothing silently corrected:**
1. Route-D at dx=0.18 returned all-zero ω and huge Ward residuals → outputs **DISCARDED** as invalid; a **validity gate** instituted: no BdG eigenvalue is reported unless the state's discrete GP residual ‖Hψ₀−μψ₀‖/μ ≤ 1e-6.
2. Polish v1 (fixed τ=0.6) **diverged** to a τ-limit plateau (2.04e-1 at two different grids); its F9 numbers are **VOID** and replaced.
3. Polish v2 (energy-backtracking preconditioned descent) converges: residual 7.2e-2 → ~5e-9. It revealed that **the split-step dt=0.01 fixed point sits ~1.79–3.52 per particle (2.6–3.4%) above the true discrete GP minimum.** Every Phase-0 absolute energy carries this bias.
4. A second self-caught bug (via C-NEG): the BdG exchange convolution must use Û̃(|G+q|), not Û̃(|G|) — the wrong form reproduced exactly the 3.15% analytic discrepancy; fixed, C-NEG now 2.3e-12.

**Consequence handling:** all Phase-0 energies were re-evaluated with polished states at the **frozen Phase-0 geometries** (residuals ≤5e-9), and the shear-decisive strain curvatures were re-measured at polished level for **both** kernels. Geometries were *not* re-optimized under polish — a declared caveat, quantified below.

## §2. Q-A re-confirmation at polished level (amended rule A-1.1)

| kernel | polished class minima (CP vs non-CP) | class gap | sub-order | sub-gap |
|---|---|---|---|---|
| step | AB 68.410074364 vs BCC 69.250055562 | **1.2279e-2** | AB, FCC, ABC | 1.2509e-4 |
| gem8 | AB 99.060711897 vs BCC 99.951847072 | **8.9958e-3** | AB, FCC, ABC | 1.1436e-4 |

**Q-A = STACK-SELECTED (close-packed p6m stack), both kernels, confirmed under polish** — the arm survives the S-class correction with two orders of margin. Sub-question data: hcp remains lowest and its sub-gap now *exceeds* δ_E in both kernels (was straddling at split-step level); the polished sub-order swaps FCC marginally below ABC. **Frozen-geometry caveat quantified:** the polished ABC–FCC split (nominally the same structure) is 2.3e-6 (step) / 3.2e-7 (gem8) — two orders below the sub-gap, so the caveat cannot flip the sub-ordering, but sub-question statements remain hcp-vs-fcc *near-degeneracy* statements.

## §3. Route S — elastic constants (C/ρ units; ε₀=0.005; quartic ≤3.7e-4; worst residual ≤5e-9)

**Polished (authoritative this leg):**

| | C44 | C66 | C11−C12 | identity resid. | C' | Zener C44/C' |
|---|---|---|---|---|---|---|
| step:AB | 56.3497 | 60.7928 | 117.6319 | **3.252% — F-ISO FIRED** | — | — |
| gem8:AB | 80.5371 | 84.7930 | 163.1357 | **3.803% — F-ISO FIRED** | — | — |
| step:FCC | 85.2934 | — | 73.4505 | — | 36.7252 | 2.322 |
| gem8:FCC | 131.5436 | — | 92.6998 | — | 46.3499 | 2.838 |

**Split-step comparison (superseded, retained for the audit):** step:AB C44 65.19→56.35 (−13.6%), C66 71.41→60.79 (−14.9%), dev 142.82→117.63 (−17.6%). The split-step curvatures were inflated 14–18%, and their perfect identity agreement (ratio 4.0004) is now known to be coincidental — the S-class bias does **not** cancel in curvatures.

**Grid provenance:** the full step-kernel polished set reproduces at dx=0.04 (independent grids 36×64×60 and 50³) to ≤7e-11 relative; base energies to 3e-14. gem8 polished set is single-grid (residual-gated) — flagged for CC.

**F-ISO adjudication (the fired falsifier, investigated not excused):** the stress probe measured large linear strain coefficients at the polished state (AB: bi −92.426, zz −46.195, iso −138.637; FCC iso −138.645 — AB/FCC agree to 6e-5, same pressure state), i.e. the frozen-geometry reference is genuinely prestressed; a naive finite-stress closed-form prediction for the identity residual (7.907) **failed**, so the refined diagnosis is a **dev-channel outlier against a triple-sourced C66** (static xy curvature + independent-grid reproduction + dynamical SH slope, all within ~1%). Per the locked rule the fire **blocks static hex-class verdict eligibility this leg** — it is not argued away. The dynamical instantiation adjudicates the symmetry itself (§4).

## §4. Route D — Bloch-BdG on the polished state (step:AB; validity gate 4.96e-9 PASS)

Mode identification: modes 1–4 form a flat, q-insensitive Josephson/phase complex (ω ≈ 0.14–0.96); **the acoustic transverse pair is modes 5–6.** Two q per direction (0.3, 0.6); Richardson q→0 slopes (ω = cq + bq³); curvature 0.69–1.75%.

| direction | c(q→0) pair | static reference | deviation |
|---|---|---|---|
| axial z | 7.5066, 7.5481 | √C44 = 7.5066 | −0.0002%, +0.55% |
| basal x (Γ→K) | SV 7.6938, SH 7.8491 | √C44, √C66 = 7.797 | +2.49%, +0.67% |
| basal y (Γ→M) | SV 7.6937, SH 7.7981 | √C44, √C66 | +2.49%, +0.014% |

**Dynamical F-ISO (Γ→K vs Γ→M): SV 0.0009%, SH 0.65% — PASS at ≤2%.** Basal isotropy holds in the actual wave dynamics; the static fire is a channel artifact of the prestressed raw curvatures, exactly the class the re-scoped F-ISO was designed to separate from the measurement. Static–dynamic agreement ≤2.5% on every channel; the dynamical transverse spread is 2.28% (raw figure; arm mapping belongs to the mapper alone). Q-B: **T-LINEAR-3D** — propagating linear transverse branches exist (confirmatory, per the LSF prior).

## §5. Mapper verdicts (quarantined file, run last; single-leg provisional)

| class:kernel | A_3D | verdict |
|---|---|---|
| hex:step | 2.67% (indicative) | **NOT VERDICT-ELIGIBLE** — F-ISO fired on the static basis; indicative would-map ISO-3D |
| hex:gem8 | 1.81% (indicative) | **NOT VERDICT-ELIGIBLE** — same; indicative would-map ISO-3D |
| cubic:step | **24.74%** | **ANISO-3D** — robust (sensitivity band 22.7–26.9% stays above θ₂) |
| cubic:gem8 | **30.18%** | **ANISO-3D** — robust (28.2–32.3%) |

## §6. The finding, stated carefully

**The two near-degenerate ground states carry opposite isotropy characters.** The hcp stack is elastically near-isotropic on every basis available this leg (static indicative 1.8–2.7%; dynamical spread 2.3%; dynamical basal isotropy at the 0.65% level), while fcc is strongly anisotropic (25–30%, Zener 2.3–2.8) — in **both** kernels. The §2.88.B question therefore does not have a structure-independent answer: **isotropy survives dimensional promotion along the hcp branch and fails along the fcc branch**, and the branches sit 1.1–1.25e-4 apart with hcp marginally lower. The stacking sub-question, demoted at A-1.1, is thereby promoted in *consequence*: it now carries the §5.3 live canonical stake, since the fcc branch would put two shear speeds split by ~35–40% (e.g. step: √C44 = 9.235 vs √C' = 6.060) onto the Q3(1) carrier-identity claim, while the hcp branch keeps the splitting ≤3%. **No adjudication of the sub-question is made or licensed here.**

## §7. Non-claims and standing discipline
No observable, no magnitude, no comparison to any measured quantity. All ratios kernel-labelled; KNOB inherited; T4 grep clean on every file, every invocation; θ values confined to the mapper; dead zones untouched. §2.52 Open 3 frozen; §2.87.J reserved.

## §8. CC leg (dispatch package separate)
CC runs full-from-scratch: Phase 0 (independent solver — **the two-leg energy comparison now doubles as the independent adjudication of the split-step bias**), Route S full set, Route D full set on both structures per A-1.3. Chat-leg numbers are quarantined from the handoff. One conditional instrument item (residual validity gate as A-2) awaits the author's word.
