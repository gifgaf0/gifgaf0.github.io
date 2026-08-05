# G-POLY1 — CC LEG EXECUTION REPORT — Phases 0a / 0b / 1 (+ full-precision layer)

**Date:** August 5, 2026. **Leg:** CC (Claude Code, remote container; two-leg full-from-scratch per activation flag 1 — no chat-leg code consulted; chat values consulted only after CC checkpoints existed and were hashed).
**Base:** SQT Master Ledger V4.73 CANONICAL `e48f5c52d91a9fb14fb13076ee394263`. **Dispatch:** `G_POLY1_CC_DISPATCH_INBAND.md` md5 `d134416ccb0a4b21290f27b23aa6ec02` (37,571 B — verified) + `G_POLY1_CC_DISPATCH_ADDENDUM_1.md` (X-1 closure).
**Formalism declared (flag 5):** Roy–Kube assembly (pin §E3 primary); hexagonal arm by exact-degree SO(3) quadrature (zyz Euler, GL cosβ n=10, uniform α,γ n=12; doubling control 20/24), validated against the pinned cubic machinery via the A-anchor. He-2 used only as the pinned redundancy record (Al benchmark control consumed).
**§C conventions acknowledgment:** all six §C declarations of Addendum 1 adopted — general VRH chain for C2; halfwidth = 100·(v_V−v_R)/(2·v_VRH); mixtures = two-phase VRH over phase Hill G; Φ_G = V_tot/G_V,pinned²; scattering reference = general Voigt λ̄, μ̄, ρ=1, a=1, d=2a; hex identity residual reported, not "fixed."

## 1. Verify-then-build

All nine embedded artifacts extracted per the declared span conventions and md5-verified byte-exact before any use: prereg `dab462d2…` (5,967 B), pin record `621120e5…` (10,759 B), input `poly_vrh_results.json` **`200e7a8b775577564369c6924d38a84c` (2,767 B — matches canonical; X-1 closed, C2 live)**, and the six chat-leg checkpoints (`00164bc8…`, `9fac990f…`, `b31a16a2…`, `9b931c70…`, `89ff1f21…`, `df413a7c…`). The instrument re-verifies the input md5 at every invocation before consuming it.

## 2. Instruments (CC-authored, from scratch)

| file | md5 | role |
|---|---|---|
| `poly1_phase0a_ccleg.py` | `2d4086a56f26d25c7d354594fe495ba6` | Phase 0a quoted layer (C1 control) |
| `poly1_fullprec_ccleg.py` | `a58482ef9ae367032eca82a92db13cba` | full-precision PRIMARY: C2, 0b-full, 1a, 1b + quoted phase-1 cross-check |
| `compare_cc_vs_chat.py` | `93b59c022b02dc6eb8899264509f5e4f` | two-leg C1–C6 checker (post-checkpoint only) |

**T1 quarantine (flag 2):** external `grep -i -F` against the §7 list run on every instrument before every invocation and on every checkpoint after — **zero hits, zero adjudications needed** (log: `t1_grep_log.txt`).

**CC checkpoints (flag 3, one per phase, md5'd):**
`poly1_phase0a_cc.json` `bd873a7b8735fc78e716addb47329065` (3,003 B) · `poly1_phase0full_cc.json` `9b47afaeeb66beff1990e4c9db580236` (8,354 B) · `poly1_phase0bfull_cc.json` `e36e8b43c162d4e3f42edbb0b8eabe54` (2,215 B) · `poly1_phase1full_cc.json` `ec87e42f0f617b00c4985ba2aceac339` (8,140 B) · `poly1_phase1quoted_cc.json` `55334cdb0c3244350e3bc378aecef094` (6,801 B) · verdict `gpoly1_cc_verdict.json` `c5824a94cc949691da2ebcc3f7b59f18`.

## 3. Own-leg gates (all PASS before any chat comparison)

Phase 0a containment: PASS (all 12 quantities + both spans + controls). Full layer: input md5; Al benchmark (λ̄ 54.92, μ̄ 26.42, V_T 3128.13, V_L 6317.52 — ≤7e-7); Table-I bcc control vs (11)–(12) (≤7e-4, the source's own 4-digit rounding); iso-null Ξ 1.9e-13; Ξ shift-invariance control 2.7e-12; per config: V_tot closed-identity ≤1.4e-13, quadrature doubling ≤8.7e-13, mean-vs-Voigt-iso ≤6.2e-15, cubic (6/5)ν² collapse ≤1.4e-13, **A-anchor ≤2.5e-12 (the make-or-break wiring gate — passed first-wiring on the v2-corrected construction, see H-2)**, PMW product identities ≤3.3e-16, Richardson→closed ≤5.7e-6, fit-exponent within 0.0092 of 4.

## 4. Two-leg verdict table (C1–C6)

| criterion | items | worst rel. residual | threshold | verdict | worst item |
|---|---|---|---|---|---|
| C1 (Phase-0a containment, quoted) | 12 | **0.0** (bit-identical) | 1e-8 | **PASS** | step_hex.cont_vT |
| C2 (full-precision reproduction) | 53 | 6.7e-16 (+ verdict identity PASS; worst/tol 0.9597 both legs) | 1e-6 | **PASS** | gem8_cubic.AU |
| C3 (invariants, full layer) | 62 | 1.8e-12 | 1e-8 | **PASS** | gem8_hex.dc55_sq |
| C3 (quoted cross-check) | 56 | 1.2e-12 | 1e-8 | **PASS** | step_hex.dc55_sq |
| C4 (closed quantities, full) | 58 | 2.8e-12 | 1e-6 | **PASS** | gem8_hex.Q_L_a |
| C4 (quoted cross-check) | 33 | 7.0e-13 | 1e-6 | **PASS** | gem8_cubic.Qprime_G |
| C5 (finite-ka) | 8 fits | exponent 3.9908–3.9909 (class-4); prefactor 5.7e-6; α curves two-leg ≤4.9e-13 | ≤5% | **PASS** | — |
| C6 (status identity) | 8 | identical (all FULL; hex "K FULL; G PENDING"; quoted step_cubic PARTIAL) | — | **PASS** | — |

**No S9 items.** Headline CC values (full precision): Q_T^a = 3.519074e-2 (step_hex), 5.002055e-2 (gem8_hex), 5.407763e-2 (step_cubic, FULL with K=123.8325), 7.549430e-2 (gem8_cubic) — identical to chat §D. HS: gem8 μ ∈ [84.855805, 89.432106]; step_cubic v_T ∈ [7.758614, 7.867953]. Hex K_HS two-leg agreement 2.7e-11 (non-verdict, band degenerate at the input-identity-residual floor as declared). X-1 layer deltas reproduce §D exactly: +2.6096e-5 / +4.6833e-5 / +3.3411e-4.

**R2 structural flag (non-verdict):** CC's independent Q′_G quartet {2.592175e-3, 2.571752e-3, 2.590041e-3, 2.573207e-3} — span 0.79%, substrate pairing intact (step pair 0.08% apart, gem8 pair 0.05%) — **reinforces** the chat-leg observation; it does not dissolve.

## 5. H-items (CC leg, honesty ledger)

- **G-POLY1.H-2 (CC):** the CC instrument's first run gated the quadrature Ξ against a closed form built by consuming the pinned (A.3)–(A.4) b/c digit strings — despite the pin marking them corrupted/not-consumed — and failed that gate with max-element ratio 0.9183673… = **45/49, the same signature as the chat leg's H-1 failure**. No outputs were consumed; the gate was corrected to the pin-compliant form (A-anchor + machine-fit in the T-class basis). A comparison-script control bug (isotropic shift applied asymmetrically to c11/c12, changing ν) was fixed in the same revision; the corrected shift-invariance control passes at 2.7e-12.
- **G-POLY1.H-3 (CC, diagnostic for the ledger):** the machine-derived expansion of the exact cubic Ξ in the pinned T-class basis is a = 2ν²/1575 (matches the clean A-string at 9.1e-13), **b = +ν²/180 on T_B (24 latin↔greek matchings), c = −ν²/630 on T_C (72 mixed pairings)** — i.e. the corrupted transport of (A.4) is precisely a b↔c transposition (with sign carried). Fit residual 2.1e-12. This closes the provenance of both legs' 45/49 signatures mechanically.
- **G-POLY1.H-4 (CC):** the first run of the comparison checker paired CC **full-precision** gem8 HS against the chat **quoted-layer** HS block (inputs differ at ~1e-5), producing a spurious 1.7e-5 "miss." Corrected to matched inputs (CC quoted-layer HS computed and compared); no instrument values were changed.

## 6. Deviation log (operationalizations, logged pre-comparison where applicable)

1. Phase-0a hex chain: symmetry-pinned closed forms (K_V Berryman (22); K_R = C²/M and G_R of the 1606.03700 (4)–(5) class; G_V textbook hex form with quoted C66) — confirmed identical to the chat leg's chain (C1 bit-identical).
2. Quoted step_cubic covariance: c12 = 0 surrogate tensor (c11 = 2C′, quoted C44), exact by Ξ isotropic-shift invariance (control 2.7e-12), matching the chat leg's K-free treatment.
3. Hex K_HS operationalization: tightest-lower = max of K_HS(G) over G ∈ [0, min(C44, G_eff^r, C66)]; tightest-upper = min over G ∈ (max(C44, G_eff^v, C66), 200·max]; grid + golden-section refinement. Optimizers landed at [0, cap] for step (inverted residual ordering) and [C44, interior] for gem8 — two-leg K_HS agreement 2.7e-11.
4. The quoted-layer dev_dil/dev_voigtcontr/dev_cross entries of the chat Phase-1 embed were not independently reproduced (definitions not pinned in the dispatch; absent from the full-precision primary layer; non-verdict).
5. Finite-ka α_T: Born form α_T = Σ_M [k_T k_M³/(2V_T²V_M²)] ∫ Φ_TM(μ)(1+q²a²)⁻² dμ, q² = k_T²+k_M²−2k_Tk_Mμ — Rayleigh limit reproduces the pinned Q_P identically; two-leg α agreement ≤4.9e-13 confirms the same operationalization on both legs.

## 7. Open items

- **Hex G_HS (pin S2, elided (32) first term):** optional retrieval attempted this session — OSTI purl 1082188 and the SEP-125 node11 rendering both returned HTTP 403 through the session's egress proxy. **PENDING-verbatim stands**; V/R shear bracket remains the disclosed stand-in; obligation before Phase 3 unchanged. Not reconstructed from memory.
- Phases 2–3 are outside this dispatch; the sealed-anchor block was not present and nothing here read it.
- Fold authorization: per flag 7, nothing in V4.73 touched; fold awaits two-leg comparison acceptance and explicit author authorization.

## 8. Runtime / environment

Python 3 + NumPy 2.4.6, Linux container (Claude Code remote), no network access used by any instrument; full-precision instrument wall time ~21 s. All files in this directory; `MANIFEST.md5` covers the set.
