# G-TSH3 TWO-LEG COMPARISON RECORD (C1–C6)
July 21, 2026. Chat leg: `g_tsh3_chatleg.py` f23aaca3, results 91b67120, mapper 6485f839, verdict cd15b0ee. CC leg: full-from-scratch per E4, commits e2fe0ee..c899979; own Hankel tables (Bessel-zero-subdivided), own L-BFGS+Sobolev solver, own σ-parity classifier, own mapper; D5 lock verified byte-identical (dab46b33…).

## C1 — Controls
Chat: C-NEG 0.0 exact / zero odd gapless; C-POS √3 machine. CC: own build, both pass. **AGREE.**

## C2 — First passing (g*, a*, μ)
gem8 20/1.46059/53.225 · gem4 35/1.49352/93.372 · gem3 70/1.51435/192.214 · cap_p2 410/0.98099/417.691 — CC exact on g*, a*/μ to ≤0.02% class. **AGREE.**

## C3 — Speeds / R_T (locked instrument), incl. the pre-registered ANCHOR-SYS test
New kernels: gem8 0.51767/0.51765 · gem4 0.47401/0.47399 · gem3 0.40780/0.40780 (chat/CC) — ≤0.004%. **Anchor falsification test PASSED THE RIGHT WAY:** CC's independent solver landed step 0.51882 (chat 0.51881) and γ8 0.48019 (chat 0.48026) — on the instrument values, 0.5–0.8% from the frozen anchors, exactly as pre-registered. The per-era-window attribution (ANCHOR-SYS) is now two-leg confirmed: R_T carries a real ~1% instrument dependence; the frozen anchors were a different convention. **AGREE.**

## C4 — cap_p2 exclusion
Chat: full solve, F-LIN L1 W2 = 0.946/0.952 at μ = 417.7. CC: confirmed by independent Part-1 reduction of the chat frozen exponent arrays + the identical γ4-class mechanism CC reproduced from scratch in its TSH2 K3 leg (μ = 342); CC's own cap_p2 solve running in background for completeness (changes nothing — cap_p2 is not pooled; KNOB is arithmetically independent of it). Confirmation class: TSH2-K3 precedent (independent reduction) — **AGREE, with class noted.** Upgrade to full-independent recorded if/when CC's background solve lands.

## C5 — Witness + W-μ (non-verdict R2)
CC did not re-execute P3w / W-μ (stated scope, permitted by memo §8/§9 text — "both legs" binds controls, not the witness). CC verified the chat record. Witness item carries the **H-6 mechanism correction** (see Addendum 1): five pure-F-CONV drops were procedure-noise fires (chat counter-check 3.5e-10 at gem8@33.03); γ8's F-LIN component real; all drops stand as recorded; D_C degenerate; arm unqualified. W-μ 0.712/0.778/0.993, no flags, chat-leg record. **AGREE at the recorded scope.**

## C6 — Mapper / D-statistics / arm
Chat: D_ext 18.600%, D_F(GEM) 12.582%, farthest gem3, boundary False, ncert 3/4, exclusions 1 → KNOB. CC (own mapper): D_ext 18.600%, D_F 12.580% → KNOB. Δ ≤ 0.002 pp. **AGREE.**

## Disagreement log
One initial divergence: CC first-run F-CONV excluded gem8/gem4 (conv ~4.5e-5). Closed by CC diagnosis (noise at a fragile gate the chat leg had flagged at 1.2× margin) + chat S9-lite counter-cross-check (deep fixed-a* conv 2.3e-9/1.1e-9/5.6e-10 — Addendum 1). Resolution is two-leg documented; **full S9 not triggered.** No other divergence across C1–C6.

## Standing items at fold time
1. **VERDICT (two-leg): ARM = KNOB** — R_T is a kernel-shape knob; TSH1→TSH2 dead zone resolved on the kernel-shape axis.
2. D-3 (tier-2 identity 1e-8 operational vs memo 1e-15) — author veto standing; both legs' spreads residual-limited, outcome-invariant.
3. F-CONV operationalization pin — successor-binding process lesson (Addendum 1).
4. CC cap_p2 background solve — completeness upgrade only.
5. Fold target §2.91.K + one Part VI row — **author authorization required.**
