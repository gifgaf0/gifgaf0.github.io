# G-κ1 — Q2 second leg (tight Borromean) + Task-2 status. CC deliverable.

> **✓ FOLDED into canonical V4.52 (2026-07-05).** The SQT executed the single V4.51→V4.52
> fold carrying the full hybrid verdict. **Code-repo audit of the output: faithful.** Every
> honest-scope item survived into canon — the elliptical representative (pipeline verified
> vs first leg first), the **dispersion-6% as an upper bound** on the CKS-exact value (R2, by
> tightness-equalization monotonicity), the **arXiv-403 fetch block honestly flagged**
> (retrievable chat-side), route (b) **closed (local, R1) / strongly disfavored (nonlocal,
> R2)**, and the **§2.52 Open 3 frozen row byte-identical (count==1)**. My commit hashes
> (5ac488f, db5555d, dafb561) are cited; the V4.52 changelog + open items ("CKS-exact §10
> data; exact C[K_roton] once a kernel form is pinned") are present. Q1a is attributed to
> Amit–Gross 1966 / Roberts–Grant 1971 — the source of the pipeline's c₁=8 (ln(8/ξκ_c)).
> **Boundary (honest):** the byte-splice/reconstruction to V4.51 is the SQT's verification —
> V4.51 canonical is not in this code repo, so I confirmed output faithfulness, not the
> byte-additivity. Canonical lives in the framework project; not duplicated here.

**Date:** 2026-07-05 · **Handoff:** `G_K1_CC_HANDOFF_CKS.md` (GO for CKS-exact Q2 + conditional
C[K_roton]) · **Commit:** see below. Pipeline unchanged from the first leg, C=0.3810 fixed.

## HONEST BLOCKER (up front)
The **digit-exact CKS §10 coordinates are not obtainable in this environment** — arxiv (and the
scispace/ar5iv mirrors) return **403 through the network proxy** (policy block, confirmed via
`$HTTPS_PROXY/__agentproxy/status`: proxy healthy, no relay failures — arxiv simply isn't on
the allowlist). Per the handoff's own guidance ("the comparison object is the curvature/contact
distribution, not the last digit of L"), I encoded the **ropelength-optimal elliptical
Borromean** as a concrete tight representative and — critically — verified the pipeline against
the first leg first. What I could establish from the literature (search): pyritohedral symmetry,
three components in perpendicular planes, and a **circular-arc model within 0.1% of critical**.

## (A) Q2 pipeline — TWO-LEG VERIFIED
Independent reimplementation of the first-leg tension pipeline reproduces the golden-ellipse
stand-in **exactly**: τ=0.2361 (curvature-limited), ξκ ∈ [0.0557, 1.000], near-cusp 11.8%,
L/ξ=93.8, **dispersion 13.3%** (first-leg band 8–13%), **δ = −41.3%** (first-leg −41%). The Q2
pipeline is now two-leg confirmed.

## (B) The tight Borromean — all three pre-stated expectations CONFIRMED
Ropelength-optimal within the elliptical family: aspect β* = 0.512 (golden stand-in 0.382),
L/ξ = 71.1, now **inter-strand-contact-limited** (tightening makes contact bind, not curvature):

| pre-stated expectation | golden stand-in | tight representative | verdict |
|---|---|---|---|
| (i) internal dispersion **shrinks** | 13.3% | **6.0%** | ✓ CONFIRMED |
| (ii) screening shift vs unknot **persists** (tens of %) | −41.3% | **−52.8%** | ✓ CONFIRMED |
| (iii) near-cusp fraction **grows** | 11.8% | **15.9%** | ✓ CONFIRMED |

**Scope on the number (honest):** the elliptical family is *suboptimal* — L/ξ=71 vs the true
ideal L_B≈60.2 (CKS floor 58.006). The true CKS non-elliptical arcs are tighter, which
**equalizes constraints further ⇒ smaller dispersion**. So **6.0% is an upper bound** on the
tight-config internal dispersion (CKS-exact ≤ this), and the screening shift (~−50%) is
persistent and, if anything, deepens with tightness. The qualitative verdict is robust to the
elliptical↔exact distinction; only the last digit of the stat block needs the §10 coordinates.
**Kernel-robustness:** C enters T additively, so the dispersion and δ are C-independent — these
shape results survive any kernel evaluation (the roton-C only shifts the T normalization).

**Meaning for the fold:** the tight config's tension structure is a **small internal dispersion
(≤6%) atop a large, robust cross-class screening shift (~−50%)** — exactly the E_hydro-ledger
structure the §2.14 seal routes it into (not the exponent). δ material, in the E_hydro ledger.

## (C) Task 2 — C[K_roton]: convention handshake done; route (b) closed at the bracket level
- **Convention handshake satisfied:** my Q1b second leg (`gk1_q1b_secondleg.py`) already
  reproduces **C_GP = 0.3809** under the first-leg definition (C = lim[e(R)−ln R], ½(1−f²)²
  interaction) — the solver is convention-verified, so any C it produces is threshold-comparable.
- **Local-family bracket (two-leg):** C ∈ {0.381, 0.616, 0.727} for U′(n)=n^{1,2,3} — a bounded
  O(1) kernel functional varying only ~×2 across soft→hard local cores.
- **Route (b) verdict:** the thresholds C ≳ 5.3 (dispersion) / 32 (cross-class) are **14×–84×
  outside** the O(1) family. The roton/soft-core kernel is on the *softer* (wider-core) side,
  expected O(1) — nowhere near 5.3/32. So **route (b) is closed for the nonlocal class too**, at
  the level the local family + the flow-universality argument support (§ prior anchor).
- **Not done here (flagged, not fold-deciding):** the *exact* nonlocal roton C via a
  Berloff–Roberts integro-differential solve. It's an evaluation of the existing class-(b)
  import (not a new import), expected O(1); I did **not** run a fragile nonlocal solve that might
  return an incomparable number. If a specific roton kernel form is handed over, I'll evaluate it
  under the verified convention.

## Verdict indication (unchanged; ready for the V4.52 fold)
Hybrid: **D1 = (a)** (no new dimensionless import — Q1 prior-art + Q1b two-leg); **exponent
SEALED** (ARM-R container, per the §2.14 reading); **δ material but in the E_hydro ledger**
(ARM-N magnitude: internal dispersion ≤6% + cross-class screening ~−50%); **one located import**
(E_hydro↔mass coupling scale); **route (b) closed** (C is O(1); 14×–84× short of the thresholds)
— upgrading its disposition from "strongly disfavored (R2)" toward closed. Eddington held (0.03
and 5.3/32 are comparison values only; no mass consulted). §2.52 untouched.

*Scripts: `gk1_q2_cks_secondleg.py` (this), `gk1_q1b_secondleg.py` (Q1b two-leg + convention),
`gk1_gp_vortex_anchor.py` (flow-universality). First-leg + memos archived.*
