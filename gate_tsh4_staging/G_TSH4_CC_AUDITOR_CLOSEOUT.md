# G-TSH4 — Exposed-Side Auditor Closeout

**Date:** 2026-07-28 · **Role:** CC as Auditor (exposed-side record); blind Executor-2 pending in a
fresh instance. Responding to `G_TSH4_TWO_LEG_STATUS.md`.

## §1. Dispatch integrity — VERIFIED end-to-end
The single artifact the blind leg will consume is confirmed:
- `G_TSH4_CC_DISPATCH_INBAND.md` md5 **`96eb8e8fe3f0311b62f82075e2fa2a82`** — matches the status memo's
  citation; my repo copy is byte-identical to the delivered file.
- Re-ran verify-then-build on it: embedded **pre-reg `e66b964d` ✓** and **Amendment-1 Part A
  `2c676701` ✓** still byte-exact.

## §2. Contamination hazard — acknowledged, mitigation correct
The status memo's flag is right and important: the exposed-side record (with chat-leg numbers) is now
committed to this repo (`fe5f4c3..74fb9d1`), so a fresh instance launched *inside this checkout* could
self-contaminate merely by listing or reading files. **The blind instance must be launched in a clean
working directory containing exactly one file — `G_TSH4_CC_DISPATCH_INBAND.md` (`96eb8e8f`) — and told
not to read/search any other SQT material.** The dispatch's HALT-on-exposure clause is the backstop,
not the plan (it is what I correctly triggered from this contaminated context). The paste-in dispatch
template in the status memo is sound.

## §3. Auditor input on the open A-2 election (author decides; I do not)
A-2 = residual validity gate ‖Hψ₀−μψ₀‖/μ ≤ 1e-6 on every reported ground state, both legs. **I have
first-hand independent evidence directly bearing on this**, so I put it on the record rather than
opine abstractly:
- My Phase-0 recompute converged to the **true discrete-GP minimum** and found it sits well below a
  split-step fixed point — the same S-class bias the chat leg caught (2.6–3.4% per particle).
- Critically, that bias **does not cancel in the decisive quantities**: it shifted the hcp–fcc gap
  enough to **flip the gem8 δ_E call** (split-step below δ_E → DEGENERATE; true-GP above → marginally
  STACK-SELECTED), and per the chat it inflated the elastic curvatures 14–18%.
- The bias scale (few %) is exactly where **θ₁ = 3%** lives — so a split-step-class blind solver could
  pass its own convergence practice and still land a foreseeable C1/C3 divergence.

**Evidence-based reading (informing, not making, the election):** A-2 is a bare residual bound — it
leaks no magnitudes, directions, or structure answers, so activating it does **not** compromise blind
independence; it only forecloses a known solver artifact. The independence-purist counterargument ("let
the blind leg discover the bias itself") is *also* validated by my leg — I did discover it — but only
because I chose a true-GP solver; a split-step blind leg would not, and would burn its budget on an S9
cycle. On the evidence, **A-2 ACTIVE is the lower-risk choice with no independence cost.** The author's
word decides; if A-2 is left inactive, the blind leg remains capable of surfacing the bias (as this
auditor did), at the cost of a possible C1/C3 divergence to resolve later.

## §4. Standing offer (author election D-3, pending)
The convention-robust FCC Zener-anisotropy corroboration remains available from this (exposed) side,
explicitly labelled **non-leg** (my own conventions, not the blind C1–C6). Now that the locked strain
instantiation is in hand (Amendment-1 Part A A-1.5: the hex identity |C66−(C11−C12)/2|/C66 and the
cubic Zener), I could run it to the locked *definitions* if elected — still non-blind, still an audit
annex, never a substitute for Executor-2. Awaiting the D-3 election.

## §5. Exposed-side audit annexes (final list, all committed)
1. Phase-0 independent recompute on the locked model (Q-A ordering confirmed; F-3 found independently,
   matching authorized A-1.1). 2. Phase-1/2 internal-consistency audit (21/21). 3. V4.71 ledger
   verification + the size audit that produced the chars-vs-bytes erratum. 4. In-band dispatch
   verification (D5-fix confirmed; seals + dispatch md5 `96eb8e8f` all verified). These enter the C1–C6
   record as exposed-side annexes, never as the blind leg.

---
*Auditor closeout filed 2026-07-28. Dispatch verified and ready; blind Executor-2 to run in a clean
one-file working directory; A-2 evidence on record for the author. §2.52 Open 3 frozen; §2.87.J
reserved; nothing fold-eligible pending a valid C1–C6.*
