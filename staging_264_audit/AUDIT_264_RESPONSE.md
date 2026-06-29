# Audit — §2.64 staging memo (vortex-log / ξ_vac anchor / chokepoint merger)

**Date:** 2026-06-23 · **Against:** the staging memo (prepared vs canonical V4.45) ·
**Mode:** derivation-standard audit · **Verification:** `audit_264_memo.py` (mpmath).

## Verdict: **FOLD-READY as staged**, with one flag strengthened (quantified) and one
flag added (Flag 6). The memo's registers are conservative and honest; the
"Zero Free Parameters → two anchors" correction is correct and important. No register
needs raising; one number (3.81%) needs a stated uncertainty.

## Checkable claims — all verified
| claim | memo | audit | status |
|---|---|---|---|
| Φ = 2π − φ²/(8π²) | 6.250028 | 6.2500275 | ✓ |
| 2π/Φ | 1.005305 | 1.0053052 | ✓ |
| e^(2π/Φ) | 2.73289 | **2.732741** | ⚠ memo's last 3 digits off (rounding); see note |
| m₀ = m_e/e^(2π/Φ) | 0.18699 MeV | 0.186992 | ✓ (anchor value unaffected) |
| ξ_vac = 100φ | 161.803 fm | 161.8034 | ✓ |
| r_eff(2π) = 1+ln(1+2π/ξ_vac) | 1.0381 | 1.0380972 | ✓ |
| slack = ln(1+2π/ξ_vac) | 3.81% | 3.8097% | ✓ |
| digamma identity Σ1/(C+n)=ψ(C+N)−ψ(C) | exact | **exact** (match to 30 dp) | ✓ |
| φ⁹, φ¹⁰ bracket 100 | 76.01, 122.99 | 76.013, 122.992 | ✓ |
| 100/168 | "40% away" | 0.595 | ✓ |

**Minor note (not a defect):** the memo's intermediate `e^(2π/Φ) = 2.73289` should be
**2.73274**; the quoted m₀ = 0.18699 MeV is correct to its precision regardless. Fix the
intermediate digit on fold.

## Item-by-item
- **Item 0/1 (R1):** confirmed exactly — §2.64's only non-anchored content is the single
  log term ln(1+2π/ξ_vac), i.e. ξ_vac alone. The "MeV scale carried by m_e, gate produces
  no scale" statement is sound. R1 stands.
- **Item A (R2):** the harmonic-sum ↔ digamma ↔ log chain is **exact pure math** (verified).
  The vortex-log self-energy ε ∼ stiffness·ln(R/a_core) is **standard superfluid physics**
  (textbook; Onsager/Feynman lineage) — the memo correctly files it as *imported*, not
  SQT-native (Flag 1), and does not claim the form as novel. R2 (form-identification) is
  the right register; the discrete-summand K₇ derivation is correctly retained open. **No
  over-claim.** (Prior-art discipline: the import is named, not laundered as a derivation.)
- **Item B (status correction, R2-backed):** the structural no-address search reproduces
  (100 strictly between φ⁹, φ¹⁰; not in {7,21,42,168,600}; 40% from |PSL(2,7)|). The
  "two anchors (m_e, ξ_vac)" correction is honest and **strengthens** credibility. The
  Eddington self-restraint — explicitly refusing to grab 168 to manufacture 100 — is
  exactly right. Flag 3 (search ≠ proof) correctly keeps the door open. **See Flag 6.**
- **Item C (R2, cross-cutting):** the §2.64 → I1–I3 reduction is sound (C = ξ_vac/a is a
  healing/spacing ratio, set by substrate dynamics), and the merge with §2.52 Open 3 /
  §2.53 at the one I1–I3 chokepoint is a legitimate M.BRIDGE-shape observation. The §2.52
  freeze is respected (observation only). Flag 5 correctly guards against "merged ⇒ solved."
  R2 stands.

## Flag 2 — STRENGTHENED (now quantified): the 3.81% is not robust
The memo flags the endpoint/running/artifact adjudication as R3-unadjudicated. The audit
makes it **material, not academic**: with a=1 fm (C=ξ_vac, closure L=2π → N≈6–7 cells), the
*discrete* harmonic sum gives the slack as
- **3.65%** at N=6 (sum₀⁵), vs **4.25%** at N=7 (sum₀⁶), vs **3.81%** continuum.

So the continuum 3.81% swings **+4% / −11% of itself** depending purely on the
discrete-cell count at closure — and the Euler–Maclaurin endpoint term 1/(2C) is **8.1% of
the slack** (vs the continuum-limit gap of only 0.30%). **Consequence:** "3.81%" must be
quoted as a *continuum-limit* value carrying an O(few-%, up to ~10%) model uncertainty
until the discrete summand is pinned; it is not a sharp prediction. This does not change
any register — it sharpens Flag 2 with numbers and should travel with the entry.

## Flag 6 — ADDED: the "two anchors total" claim vs the Z₀/ρ_s imports
Item B states the count as "two anchors (m_e, ξ_vac), zero further tuned parameters," and
claims "every mass ratio, coupling, **and ropelength** follows from geometry plus these
two." But the memo's own §2.64 stiffness table flags **Z₀ and ρ_s as "Imported"** (only
κ=φ⁻⁴ SQT-derived). For r_eff these cancel (the log coefficient normalizes to 1 at the
electron, so Z₀/ρ_s drop out of the *mass-ratio* spectrum — this is why ξ_vac is the sole
residual, and it is correct **for the mass spectrum**). **But the word "coupling" in the
claim reaches beyond the mass spectrum**, where Z₀/ρ_s may not cancel. **Audit ask:**
either (a) scope the two-anchor statement to the mass-ratio/ropelength spectrum (where it
is verified), or (b) demonstrate Z₀/ρ_s cancel in *all* quoted couplings too — else they
are additional imports and the count is not "two." Recommend (a) on fold: it is the
defensible, already-proven statement.

## What I did not do
Did not re-derive the framework, audit the K₇ discrete summand (correctly open), or touch
§2.52 (frozen). M.BRIDGE/M.CW/M.REL walls respected throughout — the memo uses them
correctly.

## Recommended fold disposition
Fold per the memo's §7 instructions, with: (i) the e^(2π/Φ)=2.73274 digit fix; (ii) Flag 2
carrying the quantified slack-uncertainty above; (iii) the two-anchor statement scoped to
the mass-ratio/ropelength spectrum (Flag 6), or Z₀/ρ_s cancellation shown for couplings.
The five original flags + these two travel with the entry. Append-only; no prior body
content modified; calculator/Paper VII "Zero Free Parameters" string update remains a
queued separate task (memo Flag 4).
