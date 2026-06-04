# Ledger Entry — §3.4 — The Bjerknes Substrate Program: First Computational Arc

**Date:** June 3, 2026
**Register:** **R2** (the proof methodology + the structural theorem) · **R1**
(the four computations: orbit structure, GP ground state, multi-component
ordering, octonion 3-form topology — all exact or reproducible) · **R3** (the
candidate action and the forward soliton gate).
**Cluster:** Continuum-limit / substrate dynamics (Paper II scope).
**Status:** **Supersedes the bare "§3.4 Bjerknes-action audit — Open" placeholder**
in Part VI with a structured program AND its first results. Program of record;
the only physical *claim* promoted is a structural theorem about where the
framework's content can and cannot appear. No observable bridge is asserted.
**Eddington watch:** ACTIVE (high) — the G0 term list was pre-registered before
the ground state was computed (§3.4.3 discipline); every dynamical test carries
an explicit control.

---

## §3.4.A — What a proof of the action can mean (R2)

By **M.CW**, the substrate action cannot be *derived* from the
K₇/Fano/sedenion combinatorics — it carries a metric, a scale, and a sign, the
three quantities the Category Wall forbids combinatorics from producing. "Proof"
therefore means the standard physics statement: the action is the **minimal
local functional invariant under the framework's established symmetry**
(G₂ = Aut(𝕆); the Fano subgroup PSL(2,7) of §1.1) **whose ground state,
solitons, and excitations reproduce the existing T1/T2 structure**, importing
only:

- **I1** field target (ψ ∈ ℂ⊗𝕆), **I2** GP kinetic form, **I3** one scale (m₀).

This is the M.BRIDGE "ticket": three imports, declared up front. The candidate
is the Gross–Pitaevskii / Bjerknes superfluid functional with a roton kernel;
particles are knotted vortex solitons; the secondary Bjerknes force is the
inter-soliton interaction.

## §3.4.B — The structural theorem (R2, the principal result of this arc)

> **The framework-specific Fano/PSL(2,7) content is invisible to the substrate
> VACUUM at every local order. It can appear only on TOPOLOGICAL DEFECTS —
> soliton / vortex cores — where it is a topological orientation charge that
> selects Fano-LINE windings.**

Established by four computations, each ruling out a sector:

| Gate | Sector | Finding | Register | Tool |
|---|---|---|---|---|
| **MV-G1** | vacuum density | roton-GP action crystallises to **p6m** (local ψ₆≈0.83); g=0 control stays uniform. Mechanism **viable**; the roton profile is **imported**. | R1 | `tools/mv_g1_minimiser.py` |
| **G0** | symmetry-allowed terms | GL(3,2)=PSL(2,7) is **2-transitive** (invariant 2-tensors = {I, J}); triples split **7+28**. ⇒ contact potential forced to **standard GP**; 2-body kernel **scalar-per-channel**; Fano structure first possible at **3-body**. | R1+R2 | `tools/g0_invariants.py` |
| **G1′** | symmetric 3-body | the Fano density-product term is **inert** (line-lock Q=0.431=uniform baseline, 4 seeds), while a non-line control **orders** components (Q≈0.73). p6m survives both. Cause: the lines are a balanced **2-(7,3,1) design**. | R1+R2 | `tools/g1prime_fano3body.py` |
| **G1″** | oriented 3-body | φ(ψ,ψ,ψ)≡0 (antisymmetry); the orientation density O=∫φ ψ∂ₓψ∂_yψ is a **total derivative** (0 on all smooth fields); on a skyrmion it is nonzero & orientation-odd **iff** the winding components form a **Fano line** (line: O=−12.47; non-line: O=0). | R1+R2 | `tools/g1pp_orientation.py` |

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
| **§3.4-G0** (symmetry-allowed term list) | **First pass CLOSED (R1+R2); term list pre-registered.** Residual: full G₂ higher-quartic tensor tidy-up. |
| **§3.4-MV-G1** (roton → p6m vacuum) | **PASS as "mechanism viable" (R1).** Roton profile imported (not symmetry-forced). |
| **§3.4-G1′** (symmetric Fano 3-body) | **CLOSED — informative null (R1+R2):** inert by 2-design symmetry. |
| **§3.4-G1″** (oriented Fano 3-body) | **CLOSED (R1+R2):** orientation is topological, Fano-line-selective, defect-only. |
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

- Replace the Part VI "§3.4 Bjerknes-action audit (Paper II scope) — Open" line
  with the §3.4.G task block; this entry is its expansion.
- Register honesty: **nothing is an observable bridge.** The promoted content is
  the §3.4.B structural theorem (R2) resting on four R1 computations. Gate
  *targets* carry their own labels; only G2-orient is the live physical gate.
- The Eddington watch and the §3.4.A import ticket travel with every sub-gate
  until G2 is attempted.

*Append-only discipline preserved. No prior ledger content modified. Two surgical
additive updates proposed (Part VI §3.4 line → task block; cross-refs to §1.1,
§2.15, §2.74). June 3, 2026.*

---

## §3.4.J — Changelog line (drop into the ledger §9 / version history)

**Version-tag style (v4.x):**

> **v4.25** — June 3, 2026 — **§3.4 Bjerknes substrate program, first
> computational arc.** Supersede the bare "§3.4 audit — Open" placeholder with a
> structured proof program (gates G0–G5 + MV-G1) and its first results. Promote
> one **structural theorem (R2 on four R1 computations):** the Fano/PSL(2,7)
> content is invisible to the substrate vacuum at every local order — G0 forces
> the contact potential to standard GP (G₂ irreducible on ℝ⁷; PSL(2,7)
> 2-transitive ⇒ 2-body kernel scalar-per-channel); G1′ shows the symmetric
> Fano 3-body term is dynamically inert (balanced 2-(7,3,1) design; line-lock
> Q=0.43=baseline vs control 0.73); G1″ shows the orientation term is a
> topological total derivative — and the content lives ONLY on topological
> defects (soliton cores), selecting Fano-line windings (skyrmion: line O=−12.47,
> non-line O=0). MV-G1: roton-GP vacuum crystallises to p6m (mechanism viable;
> roton profile imported, not symmetry-forced). Declare the I1–I3 import ticket.
> Open **§3.4-G2-orient** (Fano-line linking charge on the knotted-vortex /
> Császár-torus soliton core) as the single concrete forward prediction. Tools:
> `mv_g1_minimiser.py`, `g0_invariants.py`, `g1prime_fano3body.py`,
> `g1pp_orientation.py`. **No observable bridge asserted.** Append-only.

**Table-row style (v2 §9 format):**

| Version | Date | Changes |
|---|---|---|
| v4.25 | Jun 3, 2026 | §3.4 Bjerknes program first arc. Structural theorem (R2/4×R1): Fano content invisible to the vacuum (G0→GP; G1′ 2-design-inert; G1″ orientation = topological total derivative), lives only on Fano-line soliton-core defects. MV-G1 vacuum = p6m (roton imported). Import ticket I1–I3 declared. Open §3.4-G2-orient. Append-only. |
