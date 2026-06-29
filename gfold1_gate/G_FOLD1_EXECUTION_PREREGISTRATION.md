# G-FOLD1 — Execution Pre-Registration

**Question:** Does a single fold-boundary crossing act on the photon's time leg (a Lorentz **boost** → redshift, carrying time dilation) or only on its spatial triad (a **rotation** → frequency-neutral)?

**Status:** PRE-REGISTRATION (before compute). Hypotheses, decision scalar, and verdict matrix locked below; no transformation evaluated yet.
**Provenance:** Targets `SQT_Fold_Geometry_Redshift_April2026.docx` (R3, banked, "not integrated"). Downstream of the time-dilation analysis: SNe Ia light curves stretch by (1+z), so any sole-cause redshift mechanism must reproduce dilation or die.
**Register target:** Lemma → R1. Verdict (which branch SQT sits on) → **R2 at most**, because it is contingent on a declared import (see §4). The gate does **not** promote the physical verdict to R1.

---

## 1. Setup

Emission tetrad `e_a` (a = 0,1,2,3), η = diag(−1,1,1,1). The fold crossing maps it to a reception tetrad `e'_a = Λ e_a`, Λ ∈ O(3,1) (declared flat-frame change; see §4-I1). Photon 4-momentum `k`. Measured frequencies:

  ω_e = −⟨k, e_0⟩,  ω_r = −⟨k, Λe_0⟩,  **1+z = ω_e/ω_r = ⟨k,e_0⟩ / ⟨k, Λe_0⟩.**

**Decision scalar (the one number this gate turns on):**

  **S ≡ ⟨e_0, Λe_0⟩_η.**

- S = −1  ⟺  Λe_0 = e_0  ⟺  Λ ∈ Stab(e_0) = SO(3) (pure spatial rotation) ⟹ ω_r = ω_e, **z = 0**.
- S < −1  ⟺  Λ has a boost component, rapidity φ with cosh φ = −S ⟹ **z ≠ 0**.

S is computed **once the fold transformation is declared**, not before. Composition note: SO(3) is closed, so N pure-rotation crossings remain a rotation — H_rot gives z = 0 *cumulatively*, not just per-fold.

---

## 2. The Lemma (R1 target — the part that vindicates "not tired light")

**Welding identity.** For any frame/metric mechanism, the wavelength redshift factor and the time-interval stretch factor are *the same number*:

  N_crests is a Lorentz scalar; ω = 2πN/Δτ_proper ⟹ ω_r/ω_e = Δτ_e/Δτ_r ⟹ **(1+z) = Δτ_r/Δτ_e.**

Consequence: **z ≠ 0 ⟺ time dilation ≠ 0, locked to the same factor — no free dial between them.** Redshift-without-dilation (the tired-light signature) is *unreachable* inside the frame picture; it requires breaking ω = 2πN/Δτ, i.e. genuine per-photon energy extraction — which the source doc explicitly disavows ("not energy dissipation").

→ If confirmed symbolically, this is a clean R1 result: **the mechanism is structurally incapable of being tired light, and any redshift it produces passes SNe Ia by construction.** This is the rigorous form of the intuition. The ledger's "tired light" flag was a hedge against an *unpinned* mechanism, not a classification — this lemma retires the hedge.

---

## 3. Hypotheses

**H_boost (primary).** The fold crossing acts on the time leg (S < −1). Then redshift accrues, collinear rapidities add (φ_total = N·δφ ∝ distance), and 1+z = e^(N·δφ) — Hubble-linear at small z, dilation (1+z) automatic.
*Pre-registered prediction:* S < −1 for the declared fold transformation; z(D) linear at low z; the doc's anisotropy and H₀(z)-drift signatures have a real substrate.

**H_rot (null / informative-fail).** The fold crossing is a pure spatial reorientation (S = −1). Then **z = 0 exactly, cumulatively**. The "lensing" framing is literal (deflection is frequency-neutral), and the cosmological redshift claims — Hubble-tension component, black-hole-density reading, anisotropy — collapse for lack of a redshift channel.

---

## 4. Declared imports (state honestly; do not derive past these)

- **I1 (M.BRIDGE) — the fold-crossing transformation.** The explicit Λ: *which plane the "metric orientation change" lives in.* A spacelike 2-plane ⟹ elliptic angle ⟹ rotation ⟹ S = −1. A time-containing 2-plane ⟹ hyperbolic angle ⟹ boost ⟹ S < −1. **This choice is the import.** Per M.CW, no combinatorial/incidence input can settle plane-type — it is a physical postulate about what a fold *is* (M.ONT-adjacent). The gate's job is to make this explicit, compute S from it, and refuse to launder the choice as a derivation.
- **I2 (M.CW) — magnitude.** The *form* (rapidity, additive accumulation, z = e^(Nδφ)−1) is forced (R1). The *value* is not: a specific nonzero δφ needs a velocity scale (β = v/c), and the conversion N→z(D) needs the fold linear density (dimension 1/length). Both dimensionful → walled, same "Imported" status as ρ_s, Z₀. Combinatorics gives N ∝ D, never the scale.

---

## 5. Verdict matrix

| Outcome | Verdict | Meaning |
|---|---|---|
| Lemma holds | R1 | Tired-light branch unreachable; any fold redshift carries (1+z). Intuition vindicated. |
| S < −1 (H_boost) | R2 (import-contingent) | Mechanism viable **as a contribution**. Passes SNe Ia. But "frames in relative motion ∝ distance" *is* recession — **observationally degenerate with expansion on the dilation axis.** Distinguishability lives only in anisotropy + H₀(z). Catch #1, made rigorous. |
| S = −1 (H_rot) | INFORMATIVE-FAIL | **Mechanism produces no redshift at all.** Lensing-deflection framing is fatal. Cosmological claims retire. A legitimate negative result at full weight. |

Either physical branch is a finding. H_boost does not "win" — it survives at the cost of degeneracy with expansion; H_rot is a clean null. Neither is promoted past R2.

---

## 6. Eddington guard

The boost-vs-rotation question **is** a "which angle" question in the framework's own idiom: circular deflection (2π-C, the SO(3) budget, frequency-neutral) vs hyperbolic rapidity (frequency-shifting, dilation-carrying). Conflating them is a **fourth instance of the documented distinct-2πs failure mode**, and the source doc's "same physical process as gravitational lensing" framing actively *invites* the conflation (lensing = deflection = rotation = z 0). Flag held open: do not let "lensing" smuggle in a redshift it cannot produce.

---

## 7. Execution plan (on go)

Standalone, self-verifying, no framework imports under test (Eddington guard):

1. sympy: construct a general Λ ∈ O(3,1) (6 params: 3 rotation, 3 boost). Confirm Λᵀ η Λ = η.
2. Polar-decompose Λ = R·B (R ∈ SO(3), B symmetric boost). Confirm unique.
3. Symbolically verify 1+z depends **only** on B; R contributes 1. Verify the welding identity (1+z) = Δτ_r/Δτ_e on a parametrized wave train.
4. Two parametric families: (a) pure spatial-plane rotation → assert S = −1, z = 0; (b) time-plane rotation → assert S = −cosh φ, z = e^φ − 1, dilation = same factor.
5. Insert the **declared** fold transformation (I1) and report S. No tuning of I1 after seeing S.

**Falsifiers:** lemma fails symbolically (would break standard cosmology — treat as bug, not result); decomposition shows z depending on R (impossible — bug); declared I1 yields S whose sign contradicts whichever branch was argued for physically (→ accept the branch the math gives, do not re-pick I1).

---

*Pre-registration only. Not folded. Connects to the §2.89 scale-filtered-locality reading and to M.ONT. Execute as a separate gated step.*
