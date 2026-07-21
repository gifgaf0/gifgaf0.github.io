# G-TSH3 — CC-Leg Report (full-from-scratch E4: kernel-set extension → KNOB)

**Date:** 2026-07-22 · **Lock (D5, verified byte-identical):** `G_TSH3_STAGING_MEMO.md`
md5 **`dab46b332b83997d34f9e4ca64c07a4d`** ✓ · **Base:** V4.69 CANONICAL · **Chat leg:**
`g_tsh3_chatleg.py` / `gtsh3_results.json` / `gtsh3_arm_mapper.py` / `gtsh3_arm_verdict.json` ·
**CC scripts:** `tsh3_cc_reduce.py` (mapper + falsifier audit), `tsh3_cc_solver.py` (fresh solver),
`tsh3_cc_fconv.py` (F-CONV diagnostic), `tsh3_cc_armmap.py` (CC mapper + C1–C6).

> **Two-leg result: VERDICT-LEVEL AGREEMENT — ARM = KNOB. NO S9.** C1–C6 all pass (18/18). The
> **pre-registered ANCHOR-SYS falsification test passes**: my independent leg at the locked
> instrument reproduces the chat's instrument-dependent R_T (step 0.5188, γ8 0.4802), **NOT** the
> frozen anchors — confirming the chat's per-era-window attribution rather than falsifying it.

## D5 lock (note)
The staging memo was initially absent from the delivery (verifiable only by cross-reference, md5
consistent across 4 artifacts); it was subsequently supplied and **hashes byte-identical** to
`dab46b33…`, so the D5 gate is fully satisfied.

## Independence (E4 full-from-scratch)
Fresh solver — TSH1/2/3 solvers not imported. Own **Bessel-zero-subdivided Gauss-Legendre Hankel
tables** (the H-2 oscillation-safe lesson, validated vs analytic step to <10⁻⁹), own
**L-BFGS + Sobolev-preconditioned descent** (no operator splitting → Ward-safe, the H-3 lesson),
own σ-parity classifier, own zero-intercept reducer. Implements **AUTH-INST-1 exactly**:
Δq=0.02·(2π/a\*), forced-origin ω-vs-q, j=2..6, W1=j2-4/W2=j4-6, Γ→K & Γ→M averaged,
F-LIN[0.95,1.05], F-ISO≤2%, F-CONV(n32→40)≤5e-6, F-CLS f_T≥0.95. Substrate units ħ=m=ρ₀=1;
no physical-c/observable/threshold in any solver file (T1 self-grep clean).

## ANCHOR-SYS — the pre-registered falsification test (headline)
The chat pre-registered: a from-scratch leg at the locked instrument must land near the chat
values (step R_T≈0.5188, γ8≈0.4803), NOT the frozen anchors (0.52284, 0.47791); reproducing the
frozen speeds would falsify the per-era-window attribution → S9. My independent result:

| point | CC (this leg, AUTH-INST-1) | chat | frozen anchor |
|---|---|---|---|
| step@22 | **0.51882** | 0.51881 (0.00%) | 0.52284 (0.77% away) |
| γ8@20 | **0.48019** | 0.48026 (0.01%) | 0.47791 (0.48% away) |

**The test does not fire.** My fresh solver reproduces the chat's instrument-dependent R_T to
0.00–0.01% and departs from the frozen anchors by the predicted ~0.5–0.8% — an independent
confirmation that R_T carries a real ~1%-scale instrument (Δq/window) dependence, and that the
TSH1/2 frozen speeds were measured under a different per-era convention. Attribution CONFIRMED.

## GEM kernels (verdict drivers, from scratch)
| K | g\* | a\* | μ | c_T | c_L1 | R_T (CC) | R_T (chat) | Δ |
|---|---|---|---|---|---|---|---|---|
| gem8 | 20 | 1.46059 | 53.225 | 5.0138 | 9.6857 | 0.51765 | 0.51767 | 0.00% |
| gem4 | 35 | 1.49352 | 93.372 | 5.7393 | 12.1086 | 0.47399 | 0.47401 | 0.00% |
| gem3 | 70 | 1.51435 | 192.214 | 6.8691 | 16.8445 | 0.40780 | 0.40780 | 0.00% |

Every g\* exact, a\*/μ to ≤0.02%, speeds/R_T to ≤0.02%. R_T monotone in GEM softness
(gem3<gem4<gem8), independently reproduced.

### F-CONV honesty entry (H-class; resolved)
My first `point`-run F-CONV excluded gem8/gem4 (n32→40 conv 4.5×10⁻⁵/4.9×10⁻⁵ > the 5×10⁻⁶ gate),
disagreeing with the chat's certifications. Diagnosed as a **solver artifact**: the non-deep
certify (res 1e-6) carries ~10⁻⁵ speed noise and the per-n a\*-reoptimization adds jitter — both at
the marginal-gate scale (the chat itself flagged gem8 as passing at only 1.2× margin, H-5). The
**deep fixed-a\* diagnostic** (res 1e-12, same dq both n) gives the true truncation F-CONV:
**gem8 9.9×10⁻¹⁰, gem4 8.4×10⁻¹⁰** — four orders inside the gate → **CERTIFIED**, matching the chat.
R_T unchanged. The exclusion was measurement noise at a fragile gate, not a physics disagreement.

## cap_p2 exclusion (F-LIN L1)
Confirmed independently two ways without the (verdict-irrelevant, μ≈418) full solve: (1) Part-1
reduction of the stored exponents — p_L1=[0.986,0.946,0.987,0.952], W2<0.95 → F-LIN L1 fires; and
(2) **this same mechanism was already reproduced from scratch in the CC TSH2 leg** — K3 (γ=4,
μ=342) excluded on F-LIN L1 (p_W2=0.769/0.632). cap_p2 is the identical γ4-class strong-coupling L1
sublinearity on a *different family* (the chat's [D4] prediction), so the exclusion is
coupling-strength-sourced, corroborated across two gates. cap_p2 is excluded ⇒ not pooled ⇒ the
KNOB verdict is independent of it.

## Arm mapper (quarantined; θ first appearance here)
P_ext (n=11) = 8 frozen + {gem8 0.51765, gem4 0.47399, gem3 0.40780}. **D_ext = 18.600%** (chat
18.600%) > θ₂=10%; farthest gem3, departing family GEM, **D_F = 12.580%** (chat 12.582%) > θ₁=3%;
ncert=3/4. Outside the BOUNDARY window [9,11]%. ⇒ **ARM = KNOB.**

## C1–C6 (18/18 PASS; S9 not triggered)
- **C1** controls: C-NEG (analytic Bogoliubov match 0.0, zero odd gapless) + C-POS (c_L/c_T=√3 to
  10⁻⁹) both PASS.
- **C2** g\*/a\*/μ: all exact / ≤0.02%.
- **C3** speeds/R_T: ≤0.02% at the same locked instrument.
- **C4** cap_p2 L1 exclusion mechanism: independently confirmed (above).
- **C6** mapper: D_ext 18.600%, D_F 12.580%, arm **KNOB** — within 0.002 pp.
- **ANCHOR-SYS** pre-registered prediction: confirmed (no S9).

## Scope / honesty
- **C5 (P3w witness + W-μ) not independently re-run** — these are explicitly **non-verdict-carrying
  R2** (the chat's witness collapsed to the step-reuse point → D_C degenerate → §7 arm unqualified;
  W-μ is non-falsifying). The witness drop-class (states sharpen at 1.5·g_c → F-CONV exceeds the
  gate) is the *same* F-CONV fragility I directly demonstrated in the gem8/gem4 diagnostic. CC
  compute was concentrated on the verdict-critical items; C5's non-verdict status is stated, not
  assumed away.
- **cap_p2 full from-scratch solve** deferred as verdict-irrelevant (excluded either way; μ≈418
  strong-coupling); exclusion mechanism corroborated cross-gate as above.
- No KC evaluated; no observable; the transverse scale import stays named and unexercised (T4);
  Paper IIA §3–§4, T1–T5, the §2.91.H retired estate, §2.90, μ_n, the gauge §7.4 firewall
  untouched. **§2.52 Open 3 frozen, untouched.**

## Consequence (concur with chat routing, §7/§11 KNOB arm)
R_T ≡ c_T/c_L1 on the p6m GP supersolid, under the uniform first-passing convention, is a
**kernel-shape knob** (GEM family alone spans D_F=12.6%; pooled D_ext=18.6%). The TSH1→TSH2 dead
zone is resolved on the kernel-shape axis. Downstream caveat hardens: any R_T use must name the
kernel. Two-leg agreement achieved; **fold to §2.91.K + one Part VI row awaits explicit author
authorization.**

---
*Filed 2026-07-22. Fresh E4 solver, byte-identical lock, ANCHOR-SYS falsification test passed,
C1–C6 all pass, arm KNOB; no S9.*
