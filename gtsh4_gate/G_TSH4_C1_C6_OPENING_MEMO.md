# G-TSH4 — C1–C6 COMPARISON, OPENING MEMO (both legs frozen)
**Filed:** chat leg. Legs: chat (Executor 1, reports `615702e3`/`3491541b`, verdict `c72b6724`) vs blind CC (Executor 2, branch `claude/new-session-17ziy6`, verify-then-build PASSED on `e66b964d`/`2c676701`). Comparison stage is now open; the quarantine that separated the legs is lifted **for adjudication material only**.

## C1 — Phase-0 energies: CONVERGENT, one check outstanding
CC (own solver, own optimized geometries) vs chat (polished at frozen split-step geometries), chat − CC per particle:
step: AB +0.0674, FCC +0.0678, ABC +0.0676, BCC +0.0590, AA +0.0110; gem8: +0.118, +0.118, +0.118, +0.095, +0.103.
CC uniformly **lower** — the correct sign and structure-dependent pattern for the chat leg's *declared* frozen-geometry caveat (the split-step optimizer placed each structure's geometry off its true optimum by a structure-dependent amount; chat polished the state but not the geometry). **Check requested (R-1):** CC's optimal (a, c)/L table vs chat's frozen values. If geometries differ at the ~1–2% level, C1 closes as explained; if they match to ≲0.1% while energies differ by 0.07–0.12, a functional-convention discrepancy exists → S9.

## C2 — Q-A: **CLOSED, TWO-LEG VERIFIED**
Both legs, both kernels: **STACK-SELECTED, argmin AB (hcp)**, identical sub-order AB < FCC < ABC.
Class margins: chat 1.228% / 0.900% vs CC 1.24% / 0.92%. Sub-gaps: chat 1.251e-4 / 1.144e-4 vs CC 1.185e-4 / 1.112e-4 — both legs independently place the hcp sub-gap just above δ_E = 1e-4. Containment check passes on both legs (chat 2.3e-6 polished-frozen; CC ~1e-5 at its optimizer tolerance). *This is the gate's Phase 0 done properly: two solvers, two geometry searches, one verdict.*

## C3 — Route S / Q-C: **NOT YET COMPARABLE — statistic nonconformance + one genuine conflict**
1. **Nonconformance (blocking):** the locked Q-C statistic is A_3D = max-from-mean spread of the **transverse speeds** over the E4/A-1.4 direction–polarization sets, mapped to ISO-3D / UNDERDETERMINED-3D / ANISO-3D. The blind leg reported an **axial-vs-basal compression anisotropy** (12.6% / 16.6%) under a non-arm label ("THREE-D-DISTINCT"). Different statistic, different channel. **R-2:** recompute the locked transverse A_3D from CC's own frozen C_ij — pure post-processing on their measurement JSONs, no new physics; their mapper stage re-run to the locked arms. (If the prereg's A_3D wording admitted their reading, that is an S9-lite convention finding to record, and the recompute proceeds regardless.)
2. **The F-ISO conflict (genuine, S9-opened):** chat static identity residual **3.25% / 3.80% — FIRED**; CC reports **1.3e-6 — PASS**. Two live hypotheses, both testable:
   (a) *Circularity on the CC side:* if their C66 was derived from (C11−C12)/2 rather than measured independently by xy-shear, their 1.3e-6 is definitional, not evidential. **R-3:** confirm C66's measurement independence.
   (b) *Frozen-geometry third-order contamination on the chat side:* curvatures measured at a reference displaced ~1–2% from the true optimum pick up e‴·δg cross-terms of exactly the observed few-% size — this would explain the chat fire (and its partially failed prestress closed-form) while CC, at true optima, measures clean. **Chat-side resolution offer (P-3):** re-measure the shear trio at true optima (CC's geometry table once shared under R-1, or independent chat-side re-optimization) and re-run the chat mapper. Note the chat *dynamical* F-ISO (0.65%) already sides with basal isotropy — hypothesis (b) would reconcile every number on both legs.
3. Cubic class: CC "FCC Zener 3D-distinct" is directionally consistent with chat ANISO-3D (Zener 2.32 / 2.84); numeric comparison waits on R-2.

## C4 — Route D: one-legged; CC deferral honest and logged
CC's BdG passed the uniform analytic control (2e-13) but could not certify the crystal spectrum (sign-indefinite operator; "ground-state/basis-consistency") and **deferred rather than report spurious ω²** — the exact failure class the chat leg hit and resolved (operator-consistent residual polish to ~5e-9 + validity gate ≤1e-6 before any eigenvalue is trusted). At comparison stage that mechanism is shareable. **Author election P-2:** (a) share it so CC certifies Route D and C4 becomes two-leg [recommended — cheap, and Route D is what adjudicated F-ISO dynamically on the chat side]; (b) accept Route D chat-single-leg with the deferral logged; (c) exclude Route D from the fold candidate.

## C5 — falsifier/control ledger
Convergent: C-NEG exact both legs; F-CONV pass both; T1 pass both; symmetry/containment pass both. Conflict: F-ISO static (above, S9). **Transmission gap logged (H-protocol):** the dispatch file traveled *without* the accompanying message — so **A-2 was never activated on the blind leg** (its conditional block requires the author's word in the dispatch message; CC itself noted "no accompanying instructions"). Their Route-D self-deferral suggests sound practice anyway; **R-4:** provide ground-state residual logs so A-2 compliance can be certified retroactively. Second consecutive transmission-layer defect (after the D5 reference-style handoff) — recommend a standing rule: *every dispatch is one self-contained file that embeds its own activation flags; no side-channel message is ever load-bearing.*

## C6 — verdict assembly: **BLOCKED** pending R-2 (CC mapper conformance) and S9-F-ISO resolution
Nothing is fold-eligible. V4.72 candidate assembles only after C3/C5/C6 close.

## Requests to the blind leg (no new physics compute; post-processing and logs only)
R-1 geometry table; R-2 locked transverse A_3D from frozen C_ij + conforming mapper; R-3 C66 independence; R-4 residual logs.

## Author elections
P-2 Route-D path (a/b/c; chat recommends a). P-3 chat-side true-optimum shear re-measurement to resolve S9-F-ISO (chat recommends yes). P-4 adopt the standing self-contained-dispatch rule (chat recommends yes).
