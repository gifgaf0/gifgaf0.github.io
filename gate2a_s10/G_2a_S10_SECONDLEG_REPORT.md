# G-2a-S10 SECOND-LEG REPORT (CC, independent) — the ℤ/4 cone-loop layer

**Date:** 2026-07-11 · **Pre-registration:** `G_2a_S10_EXECUTION_PREREGISTRATION.md` (**DRAFT**) ·
**Script:** `gate2a_s10_secondleg.py` (exact Cℓ(3)± over ℚ(√2)) · **Base:** V4.61.

> **⚠ PROCESS DEVIATION — logged honestly.** This registration explicitly asked to *retire* the
> S8/S9 lock-by-forwarding: "the declared clean order is register → lock → legs." I attempted to
> obtain an explicit lock **twice** (a question tool); both failed on a technical error and you said
> "continue." Per the pre-reg's **own provision** — "If forwarding precedes an explicit lock, the
> deviation is logged per the S8/S9 precedent and the locked text must be byte-identical to the
> forwarded draft" — I executed the CC leg against the forwarded draft (byte-identical by
> construction) and **log the lock-by-forwarding deviation here.** This is the CC leg, **ahead of the
> chat leg** (no two-leg agreement yet); nothing folds without authorization.

## Method (independent) + the S9 lesson applied up front
Exact Cℓ(3)^q over ℚ(√2), q = e_i² = +1 (Pin⁺)/−1 (Pin⁻); cone-loop lifts = bivectors (order-4
π-rotation lifts, q_f = e_je_k). The pre-reg's requested method variation (mod-2 homology for the
equivariance bit) and the S9 γ-correction fixtures (C2) are honored. **F6 (representative-independence)
is applied from the start** — the whole point of S9's correction — so no absolute ± is asserted before
it passes an all-representatives check. Loop dictionary respected throughout (cone loop m_f = deck r_f,
lift q_f; ambient meridian μ_f = m_f² = deck r_f², monodromy q_f² = −1). Only the S7 Γ/N presentation
is shared (flagged).

## In-execution collision check (mandatory) — done
Searched for any published treatment of the order-4 cone-loop lift system of the #24 Borromean
orbifold in link-symmetry terms with the normalizer action. **None found** — the cone-manifold/Spin
literature (Boileau–Leeb–Porti; Cooper–Hodgson–Kerckhoff) treats meridian lift conditions generally
but not this assembled object. **Novel-in-assembly**, as registered. *(Sources at end.)*

## Controls (all pass)
- **F1 (order regression):** order(q_f) = 4 for every strand, both Pin types.
- **F2 (meridian regression, S8):** q_f² = −1 (the ambient-2π meridian μ_f), both types.
- **F5 (calibration):** ω² = −q (Pin⁺ −1, Pin⁻ +1).
- **C1 (torus positive control):** pure translations lift to (±1, t) and conjugate q_f trivially — the
  ℤ/4 cone structure is carried entirely by the rotational deck r_f; torus sector classical.
- **C3 (character independence):** S9 characters are trivial on Γ, so cone-loop monodromies are
  character-independent per Pin type (q_f undressed on N-native structures).

## B1 — lift-level relation + equivariance (proper sector)
- **B1(i) — relation defect [R1]:** the Γ-relation r₁r₂ = r₃·t (t = (−1,1,1) ∈ L, from S7) lifts to
  **q₁q₂(q₃)⁻¹ = −q** — a **central, q-dependent** defect (Pin⁺: −1, Pin⁻: +1). The cone-loop lifts
  obey the quaternion relations with a **chirality set by the Pin type** (q₁q₂ = −q·q₃). This is the
  *same bit* as ω²=−q — i.e. the Pin type itself — so it is **DERIVED**, not a new located datum.
- **B1(ii) — equivariance [R1]:** the motion-group S₄ conjugation acts on the triple as the **bare
  permutation-with-sign** (the 3-fold cycles q₁→q₂→q₃, no central dressing). **ARM: BARE** — the
  cone-loop analog of S8's "bare permutation representation, no t₁₁₁ correction."

## B2 — the fate of the ± under the improper sector, comparatively
- **B2(i) — improper conjugation [R1]:** ω (=−I lift, the pseudoscalar, **central**) **fixes** every
  q_f; the glide lift e₁ **fixes q₁, inverts q₂,q₃**; the h lift (e₂−e₃)/√2 **swaps q₂↔q₃ with signs
  and inverts q₁**.
- **B2(ii) — invariance adjudication [R1, F6]:** ω and the glide represent the **same** N/Γ class (S9:
  glide∘(−I) = r₁ ∈ Γ), yet **−I fixes all q_f while the glide inverts two of them** — same class,
  opposite action. So the **absolute ± of q_f is deck-representative GAUGE**; **F6 fails** for any
  absolute ± claim, which is therefore re-posed/dropped (pre-committed, per the S7 Πε / S9 B1
  precedent — adopted *before* the computation this time, not discovered in correction).
- **Comparative across Pin types:** the improper conjugation action is **Pin-blind** (identical in
  Pin⁺ and Pin⁻). The only across-type difference is the B1(i) chirality — which is the DERIVED Pin
  type. **No new PIN-SPLIT** beyond S9's amphichiral-square distinguisher.

## Verdict — DERIVED (absolute ± GAUGE)
Per-sub-bit: B1(i) **DERIVED**; B1(ii) **BARE**; B2 **GAUGE** (absolute), Pin-blind (comparative).
Overall: **the ℤ/4 cone-loop layer carries NO NEW located data beyond (S8 meridian −1) + (S9 Pin
type).** Its entire invariant content is: order 4 (F1) squaring to the meridian −1 (F2); a
quaternion-relation chirality fixed by the Pin type (DERIVED); a bare S₄ permutation-with-sign
structure (B1(ii)); and an absolute ± that is representative/orientation **gauge** (F6). **Bank item
(a) closes with zero import delta** — a pre-registered null-class closure (the DERIVED/GAUGE arms;
no §3.x, no retraction per standing precedent). The registration-time sketch (improper lifts invert
the monodromies) is **partly falsified**: −I (central ω) does **not** invert — it fixes; only the
glide/off-diagonal representatives invert. The sketch's GAUGE-leaning conclusion for the absolute ±
is upheld, but by the representative-*disagreement*, not by uniform inversion.

- **M.REL:** scale — none; metric — flat (inherited); **sign — no new located datum (DERIVED); the
  absolute ± is gauge**; ontology — cone-π scaffolding + carrier identification unchanged/quarantined
  (neither made nor used).
- **Eddington:** no identification of the cone-loop ±i with any framework unit; distinct-4 held (the
  "order 4" is not matched to any other framework 4); μ_n sealed; m_f vs μ_f named at every step;
  §2.52 Open 3 untouched.

## Boundaries
- **Lock-by-forwarding deviation** (above) — executed ahead of explicit lock and ahead of the chat
  leg; ready to cross-check.
- **Shared presentation:** independence at the code + method level on the S7 Γ/N presentation; flagged.
- **F6 discipline held:** I did **not** assert an absolute ±; I tested representative-independence
  first and found it gauge — the S9 lesson applied prospectively.

## Verdict (second leg)
- **B1(i): DERIVED** — relation chirality = the Pin type (q₁q₂ = −q·q₃).
- **B1(ii): BARE** — motion-group conjugation is bare permutation-with-sign.
- **B2: GAUGE** (absolute ± representative-dependent, F6), **Pin-blind** comparatively; no new
  PIN-SPLIT.
- **Overall: DERIVED** — the ℤ/4 layer adds no new located import; bank item (a) closes at zero delta.
  No §2.50 closure; ontology quarantine intact; no μ_n; no time-reversal; §2.52 Open 3 untouched.

**Sources (collision check):** web.math.ucsb.edu Cooper–Hodgson–Kerckhoff (orbifolds & cone-manifolds);
Boileau–Leeb–Porti arXiv:math/0010184 (geometrization; Spin lifts of holonomy, meridian conditions);
arXiv:math/0504117 (global rigidity of cone-manifolds). None gives the order-4 cone-loop lift system of
#24's normalizer in link-symmetry terms.
