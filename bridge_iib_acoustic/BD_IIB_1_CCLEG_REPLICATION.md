# BD-IIB-1 — CC-leg replication (Paper II-B acoustic-metric R3 bridge)

**Date:** 2026-07-13 · **Memo:** `BRIDGE_DECLARATION_IIB_ACOUSTIC_METRIC_R3.md` (BD-IIB-1, R3
off-ledger) · **Script:** `bd_iib_ccleg.py` (exact ℚ(√5) arithmetic + dimensional check) ·
**Register:** R3 (staging replication only).

> **Scope wall (held).** This leg replicates the memo's §10 CC-leg items — **algebra and dimensions
> only, zero shared machinery.** It consults no data, evaluates no observable, and takes **no
> position** on the kill conditions (KC1 scalar radiation / KC2 aberration), the fluid/solid branch
> lock (I-CONST), or the A-SHEAR M.ONT-adjacent flag. It does **not** fold — per the memo, any fold
> is post-V4.63 at Matt's explicit authorization. It verifies *forms and values*, nothing physical.

## §10 items — all verified (exact)
| # | Claim | Result |
|---|---|---|
| 1 | **Dimensional identity** K = Z₀²/ρ_s = Pa | **✓** [Z₀²/ρ_s] = (kg,m,s) = (1,−1,−2) = [Pa]; A-Z0 [ρ_s·c_s]=(1,−2,−1)=[Z₀]; κ=K/(ρ_s c²) dimensionless |
| 2 | **Exact forms** φ⁻²=2−φ, φ⁻⁴=5−3φ | **✓** both exact in ℚ(√5) (from φ²=φ+1) |
| 3 | **Fluid branch** c_s/c = √κ = φ⁻² = 2−φ | **✓** = 0.381966011250 (κ=φ⁻⁴=0.145898033750; (φ⁻²)²=κ exact) |
| 4 | **Solid branch** c_L/c=√(κ+4/3), ν=(3κ−2)/(2(3κ+1)), stability | **✓** c_L/c=1.216236558850; ν=−0.543337382198; −1<ν<½ and ν<0 (auxetic) |
| 5 | **Lucas** φ⁴+φ⁻⁴ = 7 (L₄) | **✓** exact — **and its §2.3 exclusion honored: noted, given no mechanical role** |

Every memo decimal reproduced to 12 places; the exact-form identities (items 2, 5) are proven
symbolically in ℚ(√5), not just numerically. Method: independent golden-ratio field arithmetic
(a+b√5, a,b∈ℚ) + integer (kg,m,s) exponent-vector dimensional algebra — no shared code with the
chat-leg.

## What this leg deliberately does NOT do
- **No physics claim.** The acoustic-metric bridge, the c_s=φ⁻²c longitudinal speed, and the solid
  branch's auxetic ν are *replicated as algebra*; whether any of it is physically correct is untouched.
- **No branch adjudication.** Fluid (LOCKED) vs solid (RECORDED) — I verified both branches' numbers;
  I take no position on which is right (the memo's I-CONST amendment rule governs).
- **No KC/A-SHEAR position.** KC1/KC2 are stated as thresholds in the memo; the shared-dependency
  flag (both defenses route through Lemma 3.1) is the memo's own single-point-of-failure declaration.
  Not my call here.
- **No fold, no ledger anchor, no citation.** R3 off-ledger, MD5-locked at creation per the memo.

## Register / discipline
R3 staging replication. M.CW respected (the memo carries the form in κ, the scale in {ρ_s, Z₀}; I
confirmed κ dimensionless and K in Pa, no dimensionful constant produced from combinatorics). The
memo's §8 LSF precondition (BLOCKING before any II-B *compute*) is not engaged by this leg — a CC-leg
algebra replication is not II-B computation, exactly as §10 frames it. Promotion path unchanged:
CC-leg replication (this) → fold candidate after V4.63 + explicit authorization.
