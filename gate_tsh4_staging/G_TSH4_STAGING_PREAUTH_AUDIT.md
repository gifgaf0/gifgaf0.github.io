# G-TSH4 Staging Memo — CC Pre-Authorization Design Audit

**Date:** 2026-07-23 · **Auditor:** CC · **Object:** `staging_memo_G_TSH4_3D_stack_gate.md` (the
3D-stack shear gate, §2.88.B). **Status of object:** STAGED, NOT LOCKED — "no computation has been
run; no pre-registration exists until the author's word."

> **This is a pre-lock design review, not a CC leg.** No pre-registration exists yet; the author
> owes the P / E1–E7 elections and "Lock." CC elects nothing and runs nothing here. (See §D for a
> consequential flag about a premature exposure of executed numbers.)

## §A. Load-bearing prior art — VERIFIED
The memo re-poses the gate on one decisive citation; it checks out:
- **Ancilotto, Rossi & Toigo, PRA 88, 033618 (2013), arXiv:1309.2769** — confirmed real and correctly
  characterized: mean-field (GP) 3D soft-core bosons form crystals of **nanoclusters with FCC
  ordering**, spectrum carrying a gauge-symmetry soft mode plus **longitudinal and transverse**
  phonon branches. This substantiates both design moves: (i) the 3D soft-core GP ground state is FCC,
  not a p6m stack ⇒ structure must be *determined* (Q-A), not assumed; (ii) the 3D transverse branch
  exists in prior art ⇒ Q-B is correctly a light, confirmatory instantiation.
- The Cluster-2 elasticity frame (3D hexagonal: 5 constants C11,C12,C13,C33,C44 with
  C66=(C11−C12)/2, SH/SV branches; full isotropy iff C11=C33 and C11−C12=2C44; cubic isotropy iff
  Zener A=2C44/(C11−C12)=1) is standard textbook and correctly stated.

## §B. Design discipline — SOUND (the S-1 catch and the Eddington guard)
- **S-1-class re-posing (the memo's core discipline win).** Framing the gate as "stack the p6m layers
  and measure shear" would mint it on a structure the substrate may not choose — the exact failure
  class of the G-TSH2 **S-1** Gaussian catch (a known-dead elected arm) and the G-TSH1 Amendment-1
  catch. The memo instead makes **structure determination Phase 0 (Q-A)** with the stack as a
  *hypothesis under test*. This is the correct, LSF-in-its-intended-direction move. ✓
- **Eddington guard (§9):** θ₁=3%, θ₂=10%, δ_E=1e-4 declared **before any computation**, immutable
  after lock (T3); structure-candidate list fixed at lock (no candidate added after seeing an energy
  except author-authorized pre-verdict amendment, the G-TSH1/2 class); KNOB forbids selecting a
  kernel by its answer. ✓
- **F-CONV pinned deep / fixed-a\* / continuation-seeded (§6)** — this is the V4.70 **H-6
  successor-binding lesson made memo-mandatory**, i.e. exactly the fragility my CC TSH3 F-CONV
  diagnosis surfaced. Correctly carried forward. ✓
- **F-ISO re-scoped correctly (§6, the sharpest design point).** In 2D, direction-independence was a
  *falsifier*; in 3D it is **the measurement** (Q-C). The falsifier is narrowed to in-basal-plane
  isotropy ≤2% (which p6m does force in-plane); **basal-vs-axial difference is data, never a
  falsifier.** Conflating the two would smuggle the answer into the instrument — the memo names this
  and avoids it. ✓
- **C-POS upgraded to a positive control on the anisotropy statistic A_3D** ("a control that only ever
  returns isotropic cannot certify ANISO-3D"). Correct — the anisotropy verdict needs a control that
  can *see* anisotropy. ✓
- **KNOB inherited verbatim** (no 3D result stated as a pinned ratio; every ratio kernel-labelled);
  §2.52 Open 3 frozen; §2.87.J reserved; gauge §7.4 firewall held; T4 grep-discipline binds both
  legs. ✓

## §C. Coupling to ANNEX-CDEF-1 (P-a/P-b) — consistent with prior CC audit
§5 item 3 correctly flags the **new load-bearing coupling**: an ANISO-3D outcome yields two shear
branches at different speeds, which turns the ANNEX-CDEF-1-routed carrier-identity claim ("EM and the
spin-2 sector share *the one* transverse channel") into a claim with an internal splitting problem —
the framework's own instance of the species-universality obligation (Collins et al. 2004;
Anber–Donoghue 2011) I verified in the CDEF-1 audit. This is properly **quarantined** (the gate
measures A_3D; no observable, no GW170817 comparison). The base disposition (P-a authorize V4.71 /
P-b hold against V4.70) is the author's; note V4.71/ANNEX-CDEF-1 is itself **still staged-unauthorized**
(per my CDEF-1 pre-auth audit), so P-b (anticipatory-only §5 status) is the disposition consistent with
the current authorization state. Base md5s (`9517f4fb`/`96912414`) are not verifiable from the CC repo.

## §D. CONSEQUENTIAL FLAG — independence already compromised for a future G-TSH4 CC leg
Before this staging memo arrived, an out-of-order delivery exposed CC to the **executed** chat-leg
G-TSH4 material — energies (68.41/99.06…), the C_ij, the falsifier fires, and the verdict
(hcp-ISO / fcc-ANISO). That content is now in the CC record (`G_TSH4_CC_CONSISTENCY_AUDIT.md`, filed
as an explicitly non-independent internal check). **Consequence:** any CC leg I subsequently author
for G-TSH4 **cannot be blind** — the two-leg independence the E6 standard depends on is broken for
this gate specifically, and the split-step-bias adjudication (the very thing the CC leg is meant to
independently settle) is exactly what a contaminated leg cannot credibly deliver.
**Recommendation:** the actual G-TSH4 CC leg should be run by a **fresh CC instance that has not seen
the exposed numbers**, dispatched blind with only the locked pre-registration + Amendment-1 Part A
in-band (the D5 standard). If instead this instance runs it, the leg must be recorded as
**non-blind / independence-caveated**, and the split-step-bias check flagged as only partially credible.

## §E. What this audit does / does not do
Does: verify the memo's load-bearing prior art, confirm the design discipline is Eddington-clean, and
flag the independence compromise. Does not: elect any option (P/E1–E7 are author-only; the memo's
recommendations — step+gem8, Route S+D, full structure set, high-symmetry sampling, full-from-scratch
CC — are the chat leg's, not CC's), lock anything, or run any computation. No register change.

---
*CC staging-memo pre-authorization audit filed 2026-07-23. Prior art verified; design discipline
sound; independence compromise flagged. Gate held for author elections + Lock; a clean blind CC
dispatch is recommended for the eventual leg.*
