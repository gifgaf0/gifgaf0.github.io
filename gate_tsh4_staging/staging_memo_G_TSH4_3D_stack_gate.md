# STAGING MEMO — GATE G-TSH4: THE 3D-STACK SHEAR GATE
**Status:** STAGED FOR AUTHOR REVIEW — NOT LOCKED. No computation has been run. No pre-registration exists until the author's word.
**Date staged:** July 22, 2026 (chat leg)
**Registered address:** §2.91.I Q3 ledger item (3) — "the 2D→3D stack promotion (§2.88.B caveat)" — plus the V4.68 successor-surface item "the 3D-stack shear gate," registered-unopened since V4.68 and unconsumed through V4.70.
**Author sequencing election on record (July 22):** "Q3(4) declaration first, then the 3D-stack gate."

**BASE-PIN NOTICE (process, requires author disposition before lock).** The V4.71 fold (ANNEX-CDEF-1) is **staged and executed but NOT authorized** — candidate md5 `9517f4fb7aa2de65b0b4a69985962d8f`, produced by `foldin_v4_71_annex_cdef1.py` md5 `03b170bd42d300f81a35209a4f0be006` from base V4.70 md5 `969124145cd3070b266d3c5ecf44434e` (7 anchors unique, reverse-splice byte-identity verified). This memo is drafted against **V4.70 as the standing canonical**, with the ANNEX-CDEF-1 content treated as *staged, not consumed*. Two dispositions, author's election:
- **(P-a)** Authorize the V4.71 fold before this gate locks → the gate's base re-pins to V4.71 `9517f4fb` and §5's Q3(1) coupling below becomes a live canonical stake.
- **(P-b)** Hold V4.71 unauthorized → the gate locks against V4.70 and §5's coupling is recorded as *anticipatory only*, carrying no canonical weight.
The gate design is identical either way; only the base md5 and the §5 status line differ. **No lock will be taken without this disposition** (the D5 lock-transmission-gap fix and the standing register→lock→leg order both require an unambiguous base).

---

## §1. LSF-δ record (cross-dialect, run before staging per the standing rule)

Retrieval July 22, 2026, chat leg. Four clusters. **One cluster is a design-level catch and is flagged as such.**

**Cluster 1 — the 3D soft-core supersolid ground state (DECISIVE; S-1 class catch).**
- Ancilotto, Rossi & Toigo, *Supersolid structure and excitation spectrum of soft-core bosons in three dimensions*, **PRA 88, 033618 (2013)**, arXiv:1309.2769. Mean-field (GP) 3D soft-core bosons: the crystal is **nanoclusters arranged with FCC ordering**; the spectrum carries longitudinal **and transverse** phonon branches plus the gauge-symmetry soft mode; superfluid fraction drops first-order 1 → 0.4 at the transition.
- Classical GEM-α in 3D (arXiv:2007.08676): for α > 2 the pure phases are **FCC cluster crystals**; for α ≤ 2 a first-order **FCC↔BCC** structural transition with density. Cluster-internal packing in 3D is BCC/FCC, triangular only in 2D.
- **Consequence for the gate design.** The registered phrase "2D→3D **stack** promotion" *presupposes its own answer*: the literature's 3D soft-core GP ground state is **not** a stack of p6m layers, it is FCC. Framing the gate as "stack the p6m layers and measure the shear" would mint the gate on a structure the substrate may not choose — the exact failure class of the G-TSH2 **S-1** catch (an elected Gaussian probe that was analytically Q+, i.e. a known-dead arm) and of the G-TSH1 Amendment-1 catch. **The gate is therefore re-posed with structure determination as Phase 0 and the stack as a *hypothesis under test*, not a construction.** Confirmatory value: the transverse branch's *existence* in 3D is prior art (Ancilotto et al.), so Phase 1's existence question is light — the LSF rule operating in its intended direction (the G-C1/V4.48 pattern).

**Cluster 2 — the symmetry/elasticity frame for the §2.88.B caveat (adopted).**
- A 3D hexagonal (transversely isotropic) medium has **five** independent constants C11, C12, C13, C33, C44 with C66 = (C11−C12)/2, and **two** transverse branches — SH (in-plane polarized) and SV — with direction-dependent speeds: v_SH(ψ)² = (C66 sin²ψ + C44 cos²ψ)/ρ, and the qP/qSV pair from the standard Christoffel solution (formula set as in arXiv:2104.02076 SI, eqs. S3–S7). Full isotropy requires **C11 = C33 and C11 − C12 = 2C44** (equivalently ΔP = ΔS1 = ΔS2 = 1 in the standard anisotropy ratios, arXiv:1612.04398).
- A cubic (FCC/BCC) medium has three constants C11, C12, C44 and is isotropic iff the Zener ratio A = 2C44/(C11−C12) = 1 — **generically ≠ 1**.
- 2D contrast, corpus-carried: Blakie et al., arXiv:2410.15754 — the 2D honeycomb supersolid elastic tensor is isotropic (Lamé λ, μ̃), consistent with Theorem 2.1′'s exact-2D p6m result.
- **Consequence.** §2.88.B's Theorem 2.1′ (p6m ⇒ exactly two invariant pair-symmetric tensors ⇒ exactly isotropic coarse-grained response, Hall viscosity killed) is a **2D** theorem. Neither 3D hexagonal nor 3D cubic inherits it automatically. **The caveat opened at V4.35 is precisely this gate's subject and it is a measurement, not a symmetry corollary.**

**Cluster 3 — the elastic-anisotropy measurement conventions (adopted for the instrument).** Standard Voigt/Christoffel machinery and the anisotropy indices (ΔP = C33/C11; ΔS1 = (C11+C33−2C13)/4C44; ΔS2 = 2C44/(C11−C12)); 2D-crystal fourth-rank tensor classification (Jasiukiewicz–Paszkiewicz–Wolski, cond-mat/0607156) carried for the in-plane cross-check.

**Cluster 4 — A0 collision check.** No published kernel-shape sweep of a shear/longitudinal speed **ratio** in a 3D GP supersolid, and no published comparison of stacked-triangular vs FCC elastic response in this kernel class, was found. Ancilotto et al. report one FCC point's branches, not a ratio family and not a structure-competition elastic comparison. **A0 NOT TRIGGERED** at staging; the in-execution collision check remains mandatory on both legs.

## §2. Standing constraints inherited (nothing modified by this memo)

- **V4.70 KNOB (binding).** R_T ≡ c_T/c_L1 is a kernel-shape knob (D_ext = 18.600%). **No 3D result may be stated as a pinned ratio; every reported ratio must name its kernel.** This gate therefore does **not** ask "what is R_T in 3D" as a pinning question — it asks structural questions (§3) whose answers are kernel-labelled.
- **F-CONV successor-binding pin (V4.70, mandatory here).** F-CONV must be operationalized **deep, at fixed a\*, continuation-seeded**, per the S9-lite closure. Pinned in §6 as required.
- **ANCHOR-SYS (V4.70).** Cross-era systematic ±1% speeds / ±0.8% R_T; cross-era comparison only. Any 2D anchor reused here inherits it.
- **T4 substrate-units discipline.** No physical-c, GW170817, or φ-target string in any computation file; grep-asserted every invocation, both legs. The transverse **scale** import stays named and unexercised.
- **§2.52 Open 3** frozen per standing instruction; **§2.87.J** reserved; the gauge-paper §7.4 firewall holds.

## §3. The bounded question, re-posed (four parts)

**Q-A (Phase 0, structure — the LSF-forced prior question).** At a named kernel and coupling, does the 3D relaxed ground state realize a **stacked p6m** structure (AA / AB / ABC), or a **non-stack** competitor (FCC / BCC), or is the competition **degenerate** within the declared margin? *The 2D p6m result is not assumed to survive dimensional promotion.*

**Q-B (Phase 1, existence).** Does the certified 3D ground state support **propagating linear transverse branches**? (Confirmatory per Cluster 1; a light instantiation, not the gate's weight.)

**Q-C (Phase 2, the §2.88.B caveat — the gate's decisive content).** Is the coarse-grained 3D elastic response **isotropic** or only **transversely isotropic / cubic-anisotropic**? Measured as the direction-and-polarization spread of the transverse speeds over the declared sampling set.

**Q-D (Phase 3, kernel-labelled ratios).** Report the 3D ratio family — {c_SH/c_L, c_SV/c_L} along the declared directions — **as kernel-labelled data only**, no pinning claim (KNOB inherited).

## §4. Arms, pre-declared with thresholds

**Q-A arms** (energy per particle at fixed (kernel, g, ρ̄), relaxed cell shape; relative energy margin **δ_E = 10⁻⁴**):
- **STACK-SELECTED** — a stacked-p6m variant is lowest by > δ_E.
- **NON-STACK-SELECTED** — FCC or BCC lowest by > δ_E. *(The literature-favoured outcome; a clean, publishable negative — the §2.88.B "3D stack" framing would then be structurally retired and replaced by whatever the substrate chooses.)*
- **DEGENERATE-STRUCTURE** — spread ≤ δ_E across ≥ 2 candidates; Q-C/Q-D then run on **each** near-degenerate structure or the gate halts to author, per election E5.

**Q-C arms** (statistic **A_3D** = max-from-mean spread of the transverse speeds over the declared direction/polarization set; the TSH threshold structure and dead-zone discipline preserved):
- **ISO-3D** — A_3D ≤ θ₁ = **3%**: the 2D isotropy result survives promotion; §2.88.B's caveat closes in the favourable direction; the I4 1/r² dimension-sourcing statement keeps its isotropic backing.
- **ANISO-3D** — A_3D > θ₂ = **10%**: the coarse-grained substrate is **not** isotropic; §2.88.B's Theorem 2.1′ is confirmed 2D-only; the transverse sector carries **two distinct shear speeds**.
- **UNDERDETERMINED-3D** — θ₁ < A_3D ≤ θ₂: the pre-declared dead zone, **honored, not re-tuned** (T3 immutable, the G-TSH1/2 precedent); successor registered, no re-election of thresholds after seeing data.

**Q-B arm:** T-LINEAR-3D / T-ABSENT-3D (the latter would be adverse to A-SHEAR and is banked at equal weight).

## §5. Declared stakes — including one coupling that is new this session

1. **§2.88.B caveat (the registered stake).** ISO-3D closes it favourably; ANISO-3D confirms Theorem 2.1′ as a 2D-only result and opens an explicit anisotropy annotation on any downstream isotropy use.
2. **I4 / the 1/r² exponent (§2.88.E, §2.90).** The dimension-sourced exponent rests on three propagating dimensions with *isotropic* spherical shells (§2.88.B). ANISO-3D does not falsify I4 but **narrows its grounds** — an annotation obligation, pre-declared here, not an adjudication.
3. **The Q3(1) carrier-identity claim — NEW COUPLING, flagged because it is load-bearing.** ANNEX-CDEF-1 (staged V4.71) routes the surviving physics of c_T ≡ c to Q3 item (1): *"EM and the spin-2 radiative sector share the one transverse channel."* **A transversely isotropic or cubic-anisotropic 3D substrate has two shear branches with different speeds — so "the one transverse channel" would require naming which branch carries which sector, or deriving their degeneracy.** ANISO-3D therefore converts the routed carrier-identity claim from a clean assumption into a claim with an internal splitting problem — the framework's own instance of the emergent species-universality obligation (Collins et al. 2004; Anber–Donoghue 2011) that ANNEX-CDEF-1 attached to Q3(1). This is a **pre-declared consequence, quarantined**: the gate measures A_3D; it does **not** evaluate any observable, and no GW170817 comparison is performed or licensed. *Canonical weight of this stake depends on the P-a/P-b disposition above.*
4. **What is NOT at stake.** No KC; no magnitudes; Paper IIA §3–§4, T1–T5, the §2.91.H retired estate, §2.90's mechanism, μ_n — untouched. R_T's KNOB status is inherited, never softened.

## §6. Falsifiers and controls (instrument; locked at author's word, no post-hoc motion)

- **F9 (Ward).** 3D translation Ward identity (L+2X)∇ψ₀ = 0 on the relaxed state; three translational zero modes at Γ expected; gate ≤ the TSH-era threshold class. *Permanent since V4.68 — the H3 mechanism.*
- **F-LIN.** Fitted exponent p ∈ [0.95, 1.05] on both windows, every branch; the γ4-class strong-coupling sublinearity that excluded cap-p2 at V4.70 is the known failure mode.
- **F-CONV (pinned per the V4.70 successor-binding requirement).** Truncation convergence measured **deep, at fixed a\*, continuation-seeded**, gate ≤ 5×10⁻⁶. The V4.70 H-6 correction is the reason this is memo-pinned: shallow/moving-a\* measurement produced ~10⁻⁵ noise that spuriously dropped six witness points.
- **F-ISO, RE-SCOPED (design point, stated explicitly).** In 2D, direction-independence was a *falsifier*. In 3D it is **the measurement** (Q-C). The falsifier is therefore narrowed to **in-basal-plane isotropy ≤ 2%** (which p6m does force, in-plane); **basal-vs-axial difference is data, never a falsifier.** Conflating the two would smuggle the answer into the instrument.
- **F-NEG.** No spurious ω² < 0 outside the fit window.
- **C-NEG.** Uniform 3D fluid: zero shear branches, analytic Bogoliubov match.
- **C-POS.** 3D central-spring lattice with known analytic Christoffel speeds; the classifier must recover the correct labels **and** the known anisotropy — i.e. C-POS is now also a **positive control on the anisotropy statistic A_3D**, not just on branch labelling. (A control that only ever returns "isotropic" cannot certify ANISO-3D.)

## §7. Cost and scope — the honest flag, with an election

Full 3D GP relaxation + 3D Bogoliubov band structure at TSH-grade truncation is **substantially heavier than the 2D legs** and may exceed the sandbox at the accuracy the falsifiers demand. Two routes, both legitimate, pre-declared:
- **Route S (static-elastic).** Extract the elastic constants from strain-energy second derivatives on the relaxed 3D state (C11, C12, C13, C33, C44 or the cubic triple), form the Christoffel speeds analytically, compute A_3D. Cheap, and **calibrated**: the V4.69/V4.70 W-μ witness showed μ_s/(ρc_T²) → 1 as kernels soften (0.712 / 0.778 / 0.993), so the static route's relation to the dynamical speeds is measured, not assumed. Cost: the superfluid-fraction/normal-participation caveat is inherited and must be carried on every reported number.
- **Route D (dynamical).** Full 3D BdG branches, as in TSH1–3. Authoritative; expensive; may require a reduced kernel set (one kernel) and a coarser cell.
- **Route S+D (recommended).** Route S across the kernel set for Q-A and Q-C; Route D at **one** named kernel as a dynamical cross-check of A_3D and for Q-B. This mirrors the TSH-era witness/verdict separation and keeps the decisive statistic double-sourced.

## §8. Two-leg plan

Chat leg from-scratch; CC leg **full-from-scratch** (the E5(a)/E4 standard now established across TSH1–3, each time an independence upgrade). Quarantined arm-mapper as in TSH2/3: θ₁, θ₂ appear in the mapper file **only**, run last, with its own T1 self-grep. Comparison C1–C6; S9 on any verdict-level divergence; S9-lite counter-check available for gate-fragility disputes (the V4.70 precedent). The locked pre-registration **travels in-band** to the CC leg (the D5 fix, first applied at V4.69).

## §9. Eddington guard

Thresholds θ₁ = 3%, θ₂ = 10% and δ_E = 10⁻⁴ are declared **now, before any computation exists**, and are immutable after lock (T3). No observable, no physical-c, no GW comparison. Structure-candidate list (stacked-p6m AA/AB/ABC, FCC, BCC) is fixed at lock; **no candidate may be added after seeing an energy** except by author-authorized amendment filed at the catch, pre-verdict (the G-TSH1 Amendment-1 / G-TSH2 A-1 class). Kernel set is fixed at lock; the KNOB caveat forbids selecting a kernel by its answer.

## §10. Election block (author)

- **P — Base disposition:** (P-a) authorize V4.71 first, base re-pins to `9517f4fb` / (P-b) hold, lock against V4.70 `96912414`.
- **E1 — Kernel set:** (a) step + gem8 (two, recommended) / (b) step only / (c) step + gem8 + gem3 (three; cost-heavy).
- **E2 — Route:** S / D / **S+D (recommended)**.
- **E3 — Structure candidates:** {AA, AB, ABC, FCC, BCC} (recommended) / narrower.
- **E4 — Direction/polarization sampling set for A_3D:** (a) high-symmetry only (basal Γ→K, Γ→M; axial Γ→A; one oblique) — recommended / (b) uniform-random directional sampling at declared N.
- **E5 — DEGENERATE-STRUCTURE handling:** (a) run Q-C on each near-degenerate structure / (b) halt to author.
- **E6 — CC leg:** full-from-scratch (recommended) / permitted reuse.
- **E7 — Dead-zone discipline:** confirm θ₁/θ₂ as stated, T3 immutable.

*Author elections, then the word "Lock" — the memo then locks byte-identical, the pre-registration is minted from it and md5-sealed, and Phase 0 begins on the chat leg with the locked artifact transmitted in-band to CC.*
