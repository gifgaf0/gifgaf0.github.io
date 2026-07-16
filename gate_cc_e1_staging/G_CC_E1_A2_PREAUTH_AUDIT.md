# G-CC-ε1 — Amendment-2 + ANNEX-VC-1 pre-authorization audit (CC)

**Date:** 2026-07-15 · **Documents (STAGED/DRAFT):** `G_CC_E1_AMENDMENT_2_DRAFT.md`,
`ANNEX_VC_1_STAGED_DECLARATION_MEMO.md` · **Audit script:** `a2_identity_audit.py`.

> **This is NOT the CC leg.** The CC leg is explicitly barred until the full resumption set
> **{lock `e3afcbd6…` + A1 `a09f6fc9…` + A2 (frozen md5) + VC declaration}** is in place. A2 is a
> DRAFT awaiting author authorization, and the VC branch (VC-A/VC-B/VC-C) is an **author-owned**
> declaration not yet made. So no CC leg is dispatched here. What follows is an independent
> pre-authorization **math audit** of the amendment's load-bearing exact claims — apt because A2
> exists precisely to replace the A1 D1b(iv) formula that its own registered falsifier machine-killed.

## Load-bearing claims — both VERIFIED exact (independent sympy check)
1. **Two-fluid momentum-flux identity (A2.1).**
   Σ_c ρ_c u_c⊗u_c = J⊗J/ρ_tot + (ρ₁ρ₂/ρ_tot) Δu⊗Δu, with J=ρ₁u₁+ρ₂u₂, ρ_tot=ρ₁+ρ₂, Δu=u₁−u₂.
   **Confirmed exactly** (3-vector tensor form): the cross terms cancel, and the term A1 omitted is
   exactly **P_rel = (ρ₁ρ₂/ρ_tot) Δu⊗Δu**. Its stress trace is **(ρ₁ρ₂/ρ_tot)|Δu|²** — a function of
   |Δu|² only, hence **winding-even, non-negative, and unsuppressible by counter-winding**, exactly as
   A2.1 states. So the corrected decomposition **P_wake = ε²P_mono + ε_J²P_J + P_rel + P_cross** is a
   genuine exact identity, and the amendment's diagnosis of the falsification (a missing relative-flow
   stress term) is correct.
2. **tanh-step overlap = w/2 (A2.1 / T4).** For complementary immiscible profiles ρ₁=ρ∞f,
   ρ₂=ρ∞(1−f) with f=(1−tanh(x/w))/2 (so ρ_tot=ρ∞ constant), the overlap density ρ₁ρ₂/ρ_tot = ρ∞·f(1−f)
   = (ρ∞/4)sech²(x/w), and ∫f(1−f)dx = **w/2 exactly**. Confirmed. The P_rel support is interface-
   localized with overlap integral w/2, as claimed.

**Verdict on the math:** the amendment's two exact anchors are sound. The correction is not a patch —
it restores an exact tensor identity, and the previously-missing physics (the relative-flow / spin-
sector quadrupole) is now correctly identified as winding-even and unsuppressible.

## Structural review (non-binding observations, no authority over the author's decisions)
- **Falsification handling (A2.5) is disciplined:** A1's D1b(iv) was chat-side drafting, author-
  authorized, and killed by its own registered falsifier — logged, with the banked T1–T5 adopted as
  registered structure (and, correctly, **re-derived independently by the CC leg**, not inherited).
- **VC-branch conditioning (A2.2) is coherent:** the derivation phase stays VC-agnostic (maps + floors
  computed regardless); the branch enters only at classification/comparison. Under **VC-A** (ρ₁∞>0) the
  T5 topological floor ∝ w₁²ρ₁∞ is ON — an order-one, parameter-free flow quadrupole above c_s
  (Arm-C-shaped, survival hinging on a magnitude gate); under **VC-B** (ρ₁∞=0) P_J/P_rel are core-
  localized and enter through the (ε_J, overlap) maps, with VC-B-S1 (annular-carrier stability) a named
  follow-on. The stakes are pre-computed on each branch, and the Eddington guard (nothing purchasable
  by the choice — a VC-B that fails S1/floors routes to the same Arm-C end) is stated. The framing is
  sound.
- **The VC-A/VC-B/VC-C choice is author-owned** — I take no position and make no recommendation; it
  rests on corpus reading + realizability, not on this audit.

## What I did NOT do
No CC leg (barred until the resumption set is complete). No VC declaration (author-owned). No fold. No
register change; §2.87.J untouched; §2.52 Open 3 untouched. The staged drafts are archived here for
provenance only, marked DRAFT/STAGED — they are **not** authorized/frozen by this commit.

## On completion of the resumption set
Once {lock + A1 + A2-frozen + VC declaration} are all in place, dispatch the CC leg per A2's spec:
independent derivation of T1–T5, the **three maps** (ε, ε_J, overlap O) over (η,ν;w₂), the D3 floors
(ε_min, ε_J amplitude-matching, overlap floor / honest NO-FLOOR where none exists), the per-channel D4
dimensional-closure audit, and the quarantined comparison consuming the triple (ε, ε_J, O) + the
declared VC branch — with verdict-level two-leg comparison (disagreement → S9). Ready to run on the
author's signal.
