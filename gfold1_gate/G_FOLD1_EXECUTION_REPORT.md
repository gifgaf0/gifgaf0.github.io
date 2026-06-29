# Gate G-FOLD1 — Execution Report

**Date:** 2026-06-18 · **Pre-registration:** `G_FOLD1_EXECUTION_PREREGISTRATION.md`
· **Instrument:** sympy, standalone (`gfold1_execute.py`), no framework imports under
test (Eddington guard). **Question:** does a fold-boundary crossing act on the photon's
time leg (boost → redshift+dilation) or only its spatial triad (rotation → z=0)?

## VERDICT

**LEMMA → R1 (secured).** **Physical branch → UNDETERMINED at the gate** (contingent on
the import I1, which is not declared and not derivable); **not promoted past R2.**

## What the computation established (all symbolic, exact)

| pre-reg step | result |
|---|---|
| 1. Λ ∈ O(3,1) | ΛᵀηΛ=η for boost, rotation, and Λ=R·B ✓ |
| 2. polar Λ=R·B | B symmetric; **R e₀ = e₀** (rotation fixes the time axis) ✓ |
| 3. decision scalar | **S = ⟨e₀,Λe₀⟩ = −Λ₀₀ = −cosh φ**, *R drops out* — depends only on the boost |
| 3. welding lemma | **(1+z) = ω_e/ω_r = Δτ_r/Δτ_e** identically (R1) |
| 4a. H_rot family | S = −1 exactly; **z = 0 for any photon direction** |
| 4b. H_boost family | S = −cosh φ; 1+z = e^φ; z = e^φ−1; **dilation factor = 1+z** |
| 5. import I1 | S = S(I1); gate reports, does not pick (see below) |
| falsifiers | lemma holds symbolically ✓; z independent of R ✓ |

## The R1 lemma (the part that vindicates "not tired light")

Because N_crests is invariant and ω = 2πN/Δτ, the redshift factor and the
time-interval-stretch factor are **the same number**: (1+z) = Δτ_r/Δτ_e, locked, no free
dial. Therefore **redshift-without-dilation (the tired-light signature) is unreachable**
inside any frame/metric fold mechanism — it would require breaking ω=2πN/Δτ (genuine
per-photon energy extraction), which the source doc explicitly disavows.

*This lemma is standard special relativity* (redshift ≡ time dilation in a frame
picture) — it is **not a novel result**, and the gate does not claim it as one. Its
role is classificatory: it shows where SQT's fold mechanism necessarily sits. It retires
the ledger's "tired light" hedge — that hedge guarded an *unpinned* mechanism; the lemma
pins it. **Any redshift a fold produces passes SNe Ia (1+z) light-curve stretch by
construction.** This is the clean, legitimate R1 win of the gate.

## The physical branch is the import I1 — and the gate refuses to launder it

S turns entirely on the boost rapidity φ, which is nonzero **iff the fold's
"orientation-change" 2-plane contains the time axis**. That plane-type is the import I1:

- **Spacelike 2-plane** (elliptic angle) ⟹ Λ = pure rotation ⟹ S = −1 ⟹ **z = 0**.
  → **INFORMATIVE-FAIL**: the mechanism produces *no redshift at all*; the cosmological
  claims (Hubble-tension component, BH-density reading, anisotropy) collapse for lack of
  a channel. The source doc's "same physical process as gravitational lensing" framing,
  taken literally, **is this branch** (deflection is frequency-neutral).
- **Time-containing 2-plane** (hyperbolic angle) ⟹ Λ has a boost ⟹ S = −cosh φ ⟹
  **z = e^φ−1 ≠ 0**, dilation locked. → **R2 (import-contingent)**: viable as a
  *contribution*, passes SNe Ia — but "frames in relative motion ∝ distance" **is
  recession**, hence **observationally degenerate with metric expansion on the dilation
  axis.** Any distinguishability lives only in anisotropy + H₀(z) drift.

Per **M.CW**, no combinatorial/incidence input fixes plane-type; it is a physical
postulate (M.ONT-adjacent). The pre-registration **does not declare I1 numerically**, so
the gate computes S(I1) and **stops** — it will not present the plane-choice as a
derivation. (Falsifier honored: had I1 been declared and the sign contradicted a branch,
we would accept the math's branch; no I1 was supplied to re-pick.)

## Eddington guard (§6) — held open, confirmed live

The boost-vs-rotation question *is* a "which 2π" question in the framework's idiom:
circular deflection (SO(3) budget, frequency-neutral) vs hyperbolic rapidity
(frequency-shifting). The source doc's "lensing = deflection" language **actively invites
conflating them** (lensing → deflection → rotation → but then claims z≠0). This is a
fourth instance of the documented distinct-2πs failure mode. **The gate's standing
result: "lensing" must not smuggle in a redshift it cannot produce.** A fold that is
literally a deflection yields z = 0; a fold that yields redshift is a boost (recession),
not a deflection. The doc cannot have both framings at once.

## What this settles / does not settle

- **Settles (R1):** the fold mechanism is structurally incapable of being tired light;
  any redshift it carries reproduces (1+z) dilation. The tired-light hedge retires.
- **Does not settle:** whether the fold produces redshift at all — that is the I1
  postulate, undetermined by the framework's combinatorics. No physical branch promoted
  past R2; the redshift cosmology rests on an undeclared, non-derivable plane-choice.
- **M.BRIDGE:** the gate engages the M.BRIDGE import I1 explicitly and **declares it as
  an import** rather than deriving it; no physical mechanism is promoted to the body.
  M.CW/M.ONT walls respected. §2.89 (scale-filtered locality) and M.ONT connections noted,
  not advanced.

## Proposed ledger rows (for auditor fold-in; canonical ledger not in this repo)
> **G-FOLD1 / Welding lemma** | 2026-06-18 | **R1** | (1+z)=Δτ_r/Δτ_e identically; fold
> redshift cannot be tired light, passes SNe Ia by construction; standard SR used
> classificatorily. Retires the tired-light hedge. | not body.
> **G-FOLD1 / physical branch** | 2026-06-18 | **R2 at most, UNDETERMINED** | S=−cosh φ
> turns on plane-type import I1 (not derivable, M.CW). Boost branch = recession,
> degenerate with expansion; rotation branch = z=0, claims collapse. Eddington
> distinct-2πs flag held open. | not body.

*Files: `gfold1_execute.py`, `gfold1_verdict.json`, this report,
`G_FOLD1_EXECUTION_PREREGISTRATION.md`; MANIFEST.md5 alongside.*
