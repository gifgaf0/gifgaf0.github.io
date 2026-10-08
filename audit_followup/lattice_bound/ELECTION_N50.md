# Polycrystal floor: the author's election, N = 50 (October 7, 2026)

**Plain-language summary.** The author has set the minimum size of a vacuum grain at 50 lattice cells. That is the low end of what the materials literature supports for a grain to behave like a bulk crystal. With that floor, the photon data require a lattice spacing of at most 4.15 × 10⁻³⁷ m, which is 0.026 Planck lengths, or 0.055 Planck lengths if ten times more scattering loss is allowed. The ledger's declared lattice is 12–47 Planck lengths, so it leaves no light window on any photon arm. That holds even for the original sub-TeV anchor on its own, whose window edge is 2.5 times smaller than 50 of the declared cells. These are consequences of the election computed from the two-leg numbers. They are not a new verdict, and no scale is pinned.

## The author's words

> I select N = 50

Received Wednesday, October 7, 2026, 19:16 PDT, in reply to the lattice-spacing-bound result. The options offered were N = 10, 20, 50, 100, 1,000 or no floor (`LS_RESULT.md`, "The polycrystal floor: options for the author").

## Consequences

These are computed by `ls_election_n50.py` from both legs' d_max values, which agree to 10⁻¹², using the pre-registered definitions (`LS_PREREG.md` §8). The script is arithmetic on the two-leg numbers, so no new derivation decides anything here.

| Arm | d_max (m) | a_max at N = 50 | EMPTY at ℓ_P? | Declared chain: 50 · a_phys,min ÷ d_max |
|---|---|---|---|---|
| A0 anchor (1ES 1101-232) | 3.764 × 10⁻³³ | 7.53 × 10⁻³⁵ m (4.66 ℓ_P) | no | 2.52, so empty |
| A1 Crab | 2.102 × 10⁻³⁵ | 4.20 × 10⁻³⁷ m (0.0260 ℓ_P) | yes | 452, so empty |
| **A2 Cygnus (decisive)** | **2.075 × 10⁻³⁵** | **4.15 × 10⁻³⁷ m (0.0257 ℓ_P)** | **yes** | 458, so empty |
| A3 GRB 221009A | 1.740 × 10⁻³⁴ | 3.48 × 10⁻³⁶ m (0.215 ℓ_P) | yes | 54.6, so empty |
| A4 Mrk 501 | 1.049 × 10⁻³⁴ | 2.10 × 10⁻³⁶ m (0.130 ℓ_P) | yes | 90.5, so empty |
| **Combined** | **2.075 × 10⁻³⁵** | **4.15 × 10⁻³⁷ m (0.0257 ℓ_P)** | **yes** | empty on every arm |

**Robustness.** With τ × 10 the combined bound is a ≤ 8.94 × 10⁻³⁷ m (0.0553 ℓ_P); with τ × 0.1 it is 0.0119 ℓ_P. The dispersion bound, a ≤ 1.76 × 10⁻²⁷ m, does not bind.

**The election, the bound and the declared chain together.**
- **(i) At the elected floor, the photon data require a ≤ 4.15 × 10⁻³⁷ m.** The light window stays open only for lattices finer than 0.026 ℓ_P.
- **(ii) Under the declared chain the light window is empty on every arm.** The chain is ξ = ℓ_P and C = ξ/a ∈ [0.0213, 0.0851], so a_phys ∈ [1.899, 7.588] × 10⁻³⁴ m. Fifty cells span 9.50 × 10⁻³³ to 3.79 × 10⁻³² m, which is wider than every arm's d_max. That includes W^EM_∪'s own edge, so the closure does not depend on the PeV arms. V4.94 had already recorded that N = 20 empties the window under the chain, and N = 50 does so with margin. The chain itself is G-S2C1-W's election E-W-1(a), which is not licensed on the transverse line, so (ii) is conditional on it.
- **(iii) Any Planck-scale lattice (a ≥ ℓ_P) leaves no window.** The combined bound allows at most 1.28 cells per grain at a = ℓ_P.

**What this does not do.**
- It does not re-pin ξ or any other scale, and it does not declare a lower limit on a.
- It does not change W^EM_∪ of record, the G-S2C1-W verdict or the polycrystal postulate's register (R3).
- It does not touch the A1 polarization verdict, the A2 internal-mode friction, the second-sound drag or KC-EP.

## Ledger

The election waits for a fold. A staged V4.96 fold is in `fold_v4_96/`, and it has been dry-run and verified. It records:
- the election, on the polycrystal-floor row;
- these consequences, in a short §2.96;
- pointers on:
  - §2.95 and the lattice-spacing-bound row;
  - §2.91.N and the G-CI1 row;
  - the G-S2C1-W row;
  - ANNEX-CDEF-1;
  - §2.92.E;
  - the polycrystal postulate's two homes (§2.91.M / G-POLY1 and the Part V VRH row).

It becomes canonical on the author's fold word.
