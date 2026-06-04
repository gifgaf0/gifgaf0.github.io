# Ledger Entry — §3.4-SYM — Symmetry & Locality Structure of the Bjerknes Vacuum Action

**Date:** June 3, 2026
**Register:** **R2** (the methodology + the locality/no-go observation) · **R1
— pending independent reproduction** (the four computations are reproducible
from committed code but have NOT yet been re-run in the canonical ledger
environment; do not promote on this self-report) · **R3** (the candidate action
and the forward soliton gate).
**Cluster:** Continuum-limit / substrate dynamics (Paper II scope).

> **SCOPE — READ FIRST.** This is **§3.4-SYM**, a *sub-result* about the symmetry
> and term structure of the Bjerknes vacuum action. **It does NOT advance the
> load-bearing §3.4 gates** — **§2.52 Open 3** (pulsation ratio = ζ without
> external fit, flagged as *the* most structurally important remaining gate) and
> **§2.45-NGA / §2.53** (the bilateral-fold derivation that prior-addresses
> cos(π/10)) — which remain **OPEN and untouched**, as does the Part VI
> "§3.4 Bjerknes-action audit — Open" row. File §3.4-SYM *beside* those gates,
> not as progress on them. **Constructive link:** §3.4-SYM *constrains* those
> gates — by the result below, if the pulsation-ζ and bilateral-fold closures
> are framework-specific they must live in the **soliton/defect sector**, not
> the vacuum.
>
> **The one conditional in the headline:** MV-G1's p6m selection is conditional
> on an **imported roton profile** (I1–I3 below). Its scope is "given the roton
> dispersion," **not** "from Császár/substrate axioms."

**Status:** Sub-result of record. The only promoted content is the §3.4.B
locality observation (R2). **No observable bridge is asserted; the §3.4 gates
are not closed or advanced.**
**Eddington watch:** ACTIVE (high) — the G0 term list was pre-registered before
the ground state was computed; every dynamical test carries an explicit control.
**Scaffolding-ratio caveat:** four tools / six reports / one figure / seven
commits underlie a single modest R2 claim; under the program's own
"acceleration is a warning sign" rule, weight the claim, not the volume.

---

## §3.4.A — What a proof of the action can mean (R2)

By **M.CW**, the substrate action cannot be *derived* from the
K₇/Fano/sedenion combinatorics — it carries a metric, a scale, and a sign, the
three quantities the Category Wall forbids combinatorics from producing. "Proof"
therefore means the standard physics statement: the action is the **minimal
local functional invariant under the framework's established symmetry** **whose
ground state, solitons, and excitations reproduce the existing T1/T2 structure**,
importing only:

- **I1** field target (ψ ∈ ℂ⊗𝕆), **I2** GP kinetic form, **I3** one scale (m₀).

**Three groups — keep them separate (§2.23 register split; corrected per §2.79).**
The action is built on the octonion product, so any *finite* symmetry of the
**action** must lift to an octonion automorphism:

- **G₂ = Aut(𝕆)** — the continuous symmetry of the action. It acts on the 7
  imaginary directions as its **irreducible 7**; this is what does the
  GP-forcing (Schur ⇒ unique invariant metric).
- **F₂₁** — the **realized finite Fano symmetry** on the algebra. By **§2.79**
  (R1, over 𝔽₉₁₁ and ℚ) only F₂₁ ⊂ PSL(2,7) lifts into G₂; the other 147/168
  collineations break the octonion sign rules and are **not** action symmetries.
- **PSL(2,7)** — automorphism group of the **bare Fano incidence only**, *not* a
  symmetry of the dynamical action. It is used solely for the **7 + 28**
  classification of 3-subsets into lines / non-lines (a genuine PSL(2,7)-orbit
  fact F₂₁ cannot supply, since 28 > 21) that G1′ / G1″ probe.

This is the M.BRIDGE "ticket": three imports, declared up front. The candidate
is the Gross–Pitaevskii / Bjerknes superfluid functional with a roton kernel;
particles are knotted vortex solitons; the secondary Bjerknes force is the
inter-soliton interaction.

## §3.4.B — The locality / no-go observation (R2, the one promoted claim)

*(Stated modestly: this is a locality statement about the vacuum action, not a
grand "theorem." It reduces to: the bulk vacuum action carries no Fano-sensitive
term at any local order, so the Fano content can only appear as an orientation
charge on defect cores.)*

> **The framework-specific Fano/PSL(2,7) content is invisible to the substrate
> VACUUM at every local order. It can appear only on TOPOLOGICAL DEFECTS —
> soliton / vortex cores — where it is a topological orientation charge that
> selects Fano-LINE windings.**

Supported by four computations (each **R1-pending-independent-reproduction** —
reproducible from the committed tools, not yet re-run in the canonical
environment), each ruling out a sector:

| Gate | Sector | Finding | Register | Tool |
|---|---|---|---|---|
| **MV-G1** | vacuum density | roton-GP action crystallises to **p6m** (local ψ₆≈0.83); g=0 control stays uniform. Mechanism **viable**; the roton profile is **imported**. | R1 | `tools/mv_g1_minimiser.py` |
| **G0** | symmetry-allowed terms | **G₂ acts on the 7 as its irreducible 7 ⇒ (Schur) a unique invariant symmetric 2-tensor = the metric ⇒ 2-body contact kernel is a SINGLE scalar** (stricter than the {I, J} the *permutation* rep would give — that is the wrong module). Contact potential forced to **standard GP**. PSL(2,7)-incidence gives the **7 + 28** line/non-line split ⇒ Fano structure first possible at **3-body**. | R1\*+R2 | `tools/g0_invariants.py`† |
| **G1′** | symmetric 3-body | the Fano density-product term is **inert** (line-lock Q=0.431=uniform baseline, 4 seeds), while a non-line control **orders** components (Q≈0.73). p6m survives both. Cause: the lines are a balanced **2-(7,3,1) design**. | R1+R2 | `tools/g1prime_fano3body.py` |
| **G1″** | oriented 3-body | φ(ψ,ψ,ψ)≡0 (antisymmetry); the orientation density O=∫φ ψ∂ₓψ∂_yψ is a **total derivative ⇒ 0 on topologically TRIVIAL configurations** (vacuum, 1-D, trivial smooth 2-D), but **integrates to the topological charge on a (smooth) skyrmion** — nonzero & orientation-odd **iff** the winding components form a **Fano line** (line: O=−12.47; non-line: O=0). | R1\*+R2 | `tools/g1pp_orientation.py` |

\* All four computations are **R1-pending-independent-reproduction**: reproducible
from the committed tools but not yet re-run in the canonical sandbox (house norm:
R1 closures are re-run at fold).  † `g0_invariants.py` correctly computes the
PSL(2,7)-on-incidence orbit structure (the valid 7 + 28 split); the *action*
2-body kernel is fixed instead by G₂-irreducibility (single scalar) — the tool's
{I, J} output is the permutation-rep invariant, not the action kernel.

The vacuum is **generic by necessity**: G0 forces GP, G1′ is symmetry-inert, G1″
is topologically trivial in the bulk. This is M.CW expressing itself sector by
sector — the orientation (an import) can attach only to topology.

## §3.4.C — Imported vs derived (M.CW ticket accounting)

| | Item |
|---|---|
| **Imported** | I1 (target ℂ⊗𝕆), I2 (GP kinetic form), I3 (one scale), and the roton **radial profile** a(r) (metric class — G0 §G0.4) |
| **Derived (R1)** | the symmetry-allowed term list; p6m vacuum; the GP-only contact potential; the scalar-per-channel 2-body kernel; the symmetric-term inertness; the topological, Fano-line-selective orientation charge |

## §3.4.D — Eddington / Vocabulary discipline (observed)

- **G0 pre-registration honoured:** the symmetry-allowed term list was recorded
  before computing the ground state.
- **Every dynamical test has a control:** G1′ ran a non-collinear-triple placebo;
  G1″ ran a non-line skyrmion and an orientation reversal. The findings are
  comparisons, not single-arm claims.
- **A numerical mis-step was logged, not hidden:** an adiabatic g-ramp in MV-G1
  damped the seed and stuck the system uniform; a deep quench + local ⟨|ψ₆|⟩
  fixed it. The false start is recorded in `reports/MV_G1_RESULT.md`.
- **No vocabulary drift:** "Bjerknes force" is kept as the literal secondary
  acoustic radiation force (1/d², phase-signed).

## §3.4.E — What this entry does and does not establish

- **Does (R1/R2):** locate the framework's dynamical fingerprint by exclusion —
  it is **topological, lives on soliton cores, and selects Fano lines**; and show
  the vacuum-formation mechanism (roton → p6m) is viable with one imported
  profile.
- **Does NOT:** assert any observable bridge (mass, scale, sign); close G1 as a
  *framework* result (the roton is imported, not symmetry-forced); claim the
  physical soliton realises a Fano-line core (that is the open G2 test);
  generalise the 2-D orientation charge to the genuine 3-D knotted vortex.

## §3.4.F — Forward gate (sharpened, the single concrete prediction)

> **G2-orient.** On the knotted-vortex (Császár-torus) soliton, classify the core
> by which octonion components wind. The framework **predicts a nonzero
> orientation / Faddeev–Hopf linking charge iff those components form a Fano
> line.** A Fano-line core confirms the orientation channel is physically
> realised; a non-line core is an informative null. This is the first
> framework-specific, falsifiable prediction in the soliton sector and the
> bridge to §2.15 (Borromean) and §2.74.

## §3.4.G — Proposed Part VI open-task entries

| Task | Status |
|---|---|
| **§3.4-G0** (symmetry-allowed term list) | **First pass CLOSED pending in-environment reproduction (R1\*+R2); term list pre-registered.** Kernel fixed by G₂-irreducibility (single scalar). Residual: F₂₁-invariant (not PSL-permutation) higher-order tidy-up. |
| **§3.4-MV-G1** (roton → p6m vacuum) | **PASS as "mechanism viable" (R1\*), conditional on the imported roton profile.** Not symmetry-forced. |
| **§3.4-G1′** (symmetric Fano 3-body) | **CLOSED pending in-environment reproduction — informative null (R1\*+R2):** inert by 2-design symmetry. |
| **§3.4-G1″** (oriented Fano 3-body) | **CLOSED pending in-environment reproduction (R1\*+R2):** orientation is topological, Fano-line-selective, defect-only. |
| **§3.4-G2-orient** (Fano-line linking charge on the soliton core) | **Open — the located fingerprint; the concrete G2 prediction.** |
| **§3.4-G1‴ / G4** (collective tiling; Bjerknes pulsation = ζ) | **Open — downstream of a soliton that locks a core.** |

## §3.4.H — Provenance

Tools (crypto repo, branch `claude/sqt-framework-perspectives-kMZyw`):
`tools/mv_g1_minimiser.py`, `tools/g0_invariants.py`,
`tools/g1prime_fano3body.py`, `tools/g1pp_orientation.py`.
Companion reports: `reports/SQT_3.4_PROOF_PROGRAM.md` (the full gate spec),
`reports/MV_G1_RESULT.md` (+ `reports/figures/mv_g1_groundstate.png`),
`reports/SQT_3.4_G0_FIRST_PASS.md`, `reports/SQT_3.4_G1prime_FIRST_PASS.md`,
`reports/SQT_3.4_G1pp_FIRST_PASS.md`. All reproducible with numpy.

## §3.4.I — Fold-in notes

- **KEEP** the standalone Part VI "§3.4 Bjerknes-action audit (Paper II scope) —
  Open" row (it is the load-bearing open gate) and **ADD the §3.4.G block beneath
  it** — do **not** replace it, or the open gate disappears into a list of
  mostly-"CLOSED" sub-tasks.
- **Version: this is v4.26**, not v4.25 (v4.25 is the §3.07 seven-circles fold-in).
- Register honesty: **nothing is an observable bridge.** The promoted content is
  the §3.4.B **locality observation** (R2) resting on four
  R1-pending-reproduction computations. Gate *targets* carry their own labels;
  only G2-orient is the live physical gate.
- The Eddington watch and the §3.4.A import ticket travel with every sub-gate
  until G2 is attempted.

*Append-only discipline preserved. No prior ledger content modified. Two surgical
additive updates proposed (Part VI §3.4 line → task block; cross-refs to §1.1,
§2.15, §2.74). June 3, 2026.*

---

## §3.4.J — Changelog line (drop into the ledger §9 / version history)

**Version-tag style (v4.x):**

> **v4.26** — June 3, 2026 — **§3.4-SYM: symmetry/locality structure of the
> Bjerknes vacuum action (a §3.4 sub-result; the load-bearing §3.4 gates §2.52
> Open 3 and §2.45-NGA/§2.53 remain OPEN and untouched; the Part VI "§3.4 audit
> — Open" row stands).** Add the symmetry sub-program (gates G0–G5 + MV-G1) and
> its first results. Promote one **locality observation (R2; supporting
> computations R1-pending-independent-reproduction):** the Fano content is
> invisible to the substrate vacuum at every local order — G0 forces the
> contact potential to standard GP (**G₂-irreducibility on the 7 ⇒ a
> single-scalar 2-body kernel**; the realized finite algebra symmetry is **F₂₁**,
> not PSL(2,7), per **§2.79**; PSL(2,7) supplies only the **7+28** line/non-line
> incidence split); G1′ shows the symmetric
> Fano 3-body term is dynamically inert (balanced 2-(7,3,1) design; line-lock
> Q=0.43=baseline vs control 0.73); G1″ shows the orientation term is a
> topological total derivative — and the content lives ONLY on topological
> defects (soliton cores), selecting Fano-line windings (skyrmion: line O=−12.47,
> non-line O=0). MV-G1: roton-GP vacuum crystallises to p6m (mechanism viable;
> roton profile imported, not symmetry-forced). Declare the I1–I3 import ticket.
> Open **§3.4-G2-orient** (Fano-line linking charge on the knotted-vortex /
> Császár-torus soliton core) as the single concrete forward prediction. Tools
> (crypto branch, re-verify before promotion): `mv_g1_minimiser.py`,
> `g0_invariants.py`, `g1prime_fano3body.py`, `g1pp_orientation.py`. **No
> observable bridge asserted; §3.4 load-bearing gates not advanced.** Append-only.

**Table-row style (v2 §9 format):**

| Version | Date | Changes |
|---|---|---|
| v4.26 | Jun 3, 2026 | §3.4-SYM (sub-result; §3.4 load-bearing gates §2.52 Open 3, §2.45-NGA remain open; audit row stands). Locality observation (R2; computations R1-pending-reproduction): Fano content invisible to the vacuum (G0→GP via G₂-irreducible single-scalar kernel; realized finite symmetry is F₂₁ not PSL(2,7), §2.79; PSL(2,7) only for the 7+28 split; G1′ 2-design-inert; G1″ orientation = topological, 0 on trivial configs, = charge on a Fano-line skyrmion), lives only on Fano-line soliton-core defects. MV-G1 vacuum = p6m **given an imported roton**. Import ticket I1–I3. Open §3.4-G2-orient. Append-only. |
