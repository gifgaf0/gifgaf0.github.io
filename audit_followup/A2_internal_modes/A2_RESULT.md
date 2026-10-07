# A2 — Internal modes of the 16-component substrate: results, two-leg comparison and verdicts

**Plain-language summary.**
- **Soft, slow waves.** Rotating the vacuum's sixteen-component field into its other directions costs no energy. Those directions carry seven extra wave branches whose frequency grows as the square of the wavenumber.
  - They are very heavy (10.5 times the bare mass in the 2D crystal, about 315 times in the 3D crystal) and very slow.
  - Their speed limit is zero: an object that couples to them can shed energy into them however slowly it moves.
- **Which matter couples.** The knots' declared density coupling does not reach these waves. Defects built from twisted internal directions do: the Fano-line cores, including the ledger's K₇ vortex. On the vacuum of record those defects feel friction at every speed.
- **The vortex-selection gate (G-VS1) counted under the wrong symmetry.** It used a global phase that the action of record breaks to a three-fold symmetry. Under the action's real symmetry, one allowed sixth-order term pins the internal phase. The "half-quantum" vortices G-VS1 found protected are then protected only by accident. Only windings of the real-unit component stay robustly protected.

**Pre-registration:** `A2_PREREG.md` md5 `fd2e95973de02d9a0e6d719cb579ccc0`, locked by commit `eefeef2` before any A2 file existed.

**Files, first leg:**
- `a2_band2d.py` (`6664964…`) → `a2_band2d_output.txt` (`3e4c493c…`), `.json` (`8e3cec5e…`);
- `a2_band3d.py` (`6733d389…`) → `a2_band3d_output.txt` (`86decba5…`), `.json` (`3390126b…`);
- `a2_algebra.py` (`4f3754fc…`) → `a2_algebra_output.txt` (`16ec377a…`), `.json` (`955e2691…`).

**Second leg:** `leg2/` (blind; `LEG2_REPORT.md` `c4de8b27…`, `A2_LEG2_RESULTS.json` `3f3c94e1…`, `MANIFEST.md5`).

---

## DR-A2-1. Dispersion at the vacuum of record

Internal fluctuations δψ_⊥ carry no density at linear order. They obey i∂_tδψ_⊥ = L_⊥δψ_⊥ with L_⊥ = −½∇² + U*ρ₀ − μ, so their frequencies are the Bloch eigenvalues of L_⊥ (first-order dynamics: ω = ε, not ω² = ε(…)). Each crystal was rebuilt exactly as its two-leg-closed first leg built it.

| crystal | ε₀(Γ) | small-q exponent | band mass m*/m | independent check (relaxed phase twist) | band width |
|---|---|---|---|---|---|
| 2D canonical (g = 22, a* = 1.45747, μ = 55.852; residual 1.2×10⁻⁵) | ≤ 2×10⁻¹¹ | 1.9999 (0°, 30°, 90°; n = 24/32/40) | **10.506**, isotropic | banked f_s = 0.095176 vs m/m* = 0.095181 (Δ = 6×10⁻⁵ relative) | 0.12 (M), 0.14 (K); next band 14.8 above |
| 3D AB/hcp (step kernel, Λ = 2Λ_c, μ = 117.80; projected residual 2×10⁻⁹) | 0 | 2.0000 basal, 1.9999 axial | **314.2 basal, 320.7 axial** | f_s = 0.003183 / 0.003118 vs m/m* = 0.003183 / 0.003118 (same to all printed digits) | ≈ 0.005 |

**Verdict (R1).** The internal sector of the vacuum of record is gapless and quadratic: ω ≈ q²/(2m*) with **m* = m/f_s**. Its **Landau critical velocity is 0**. The band is also very flat: in 2D its maximum ε/q is about 0.05, against c_T = 5.8. The identity m/m* = f_s holds because, by inversion symmetry, the density relaxes only at O(q⁴) under a phase twist. It ties the internal branches to a banked two-leg number.

**New number.** The 3D crystal's superfluid fraction is 0.32 %, which explains its small second-sound share (F₂ = 0.17 %, since F₋ ∝ ρ_s).

## DR-A2-2. Goldstone inventory per stratum (first leg `a2_algebra.py` = second leg `task4`, identical)

Watanabe–Murayama counting with the GP symplectic form. "Action" is G₂ × U(1)_ψ₀ (g₂ derived as the 14 derivations of the octonion table). "Accidental" is SO(7) × U(1)_ψ₀ × U(1)_7, the symmetry of every T-even potential of degree ≤ 4 under the action's group.

| vacuum | symmetry | broken | quadratic (type B) | linear (type A) | what stays gapped / pinned |
|---|---|---|---|---|---|
| **P0, the vacuum of record** (any direction) | U(8) (two-body dynamics of record) | 15 | **7** | 1 (the phonon) | nothing: seven gapless quadratic internal branches |
| R (ψ ∝ e₀) | action or accidental | 1 | 0 | 1 | all 14 internal (7-sector) directions gapped by the real-unit-splitting term |
| P7 (ψ ∝ real n ∈ Im𝕆) | action / accidental | 6 / 7 | 0 | 6 / 7 | the 7th (7-sector phase) is accidental at degree ≤ 4 and pinned at degree 6 by Re S³; ψ₀ gapped |
| F7 (ψ ∝ (u + iv)/√2) | action or accidental | 11 | **5** | 1 | ψ₀ gapped |
| I7 | accidental | 12 | **5** | 2 | ψ₀ gapped |
| MP | accidental | 8 | 0 | 8 | — |
| MF | accidental | 12 | **5** | 2 | — |
| MI | accidental | 13 | **5** | 3 | — |

The internal sector is fully gapped only on **R**. P7 and MP have linear internal branches, whose speeds are set by the |S|² coefficient of the import. F7, I7, MF and MI keep five quadratic branches with zero Landau velocity.

## DR-A2-3. G-VS1 recount: verdict DOWNGRADE (half-quantum protection)

Exact invariant counts, all / T-even:
- First leg: a Molien–Weyl torus integral (exact quadrature, rounding ≤ 1.4×10⁻¹⁴), with the invariant rings written out and checked against it.
- Second leg: exact integer linear algebra on the 14 derived generators, plus a Molien count and a float kernel.
- The two legs agree on every entry.

| | degree 2 | degree 4 | degree 6 |
|---|---|---|---|
| ℝ¹⁴, (a) G₂ × U(1)_global (G-VS1's group) | 1 / 1 | 2 / 2 | 2 / 2 |
| ℝ¹⁴, (b) G₂ × U(1)_ψ₀ | 3 / 2 | 6 / 4 | 10 / 6 |
| ℝ¹⁴, **(c) G₂ × U(1)_ψ₀ × ℤ₃ (the action's group)** | 1 / 1 | 2 / 2 | **4 / 3** |
| ℝ¹⁶, (a) | 2 / 2 | 6 / 5 | 10 / 8 |
| ℝ¹⁶, (b) | 4 / 3 | 10 / 7 | 20 / 13 |
| ℝ¹⁶, **(c)** | 2 / 2 | **4 / 4** | **8 / 7** |

**What changes.**
1. **G-VS1's inventory used U(1)_global.** E-VS-1(a) took the global phase as unbroken "on the vacuum sector" because O vanishes on uniform states. But the allowed local terms are fixed by the action's symmetry group, not by which terms happen to be present.
   - Under (c), the degree-4 locking terms Re/Im(ψ₀²S̄) are **forbidden**: U(1)_ψ₀ charge 2.
   - Under (c), a degree-6 term **Re S³** (T-even), and its T-odd partner Im S³, are **allowed**: ℤ₃ charge 0.
2. **Half-quantum protection.** On the polar orbit ψ₇ = e^{iθ}n, Re S³ = cos 6θ, and it is the only degree-6 invariant that depends on θ (second leg: exactly one θ-dependent kernel direction). With nonzero coefficient:
   - V_P7 = (S¹ × S⁶)/ℤ₂ → three disjoint copies of S⁶, so **π₀ = ℤ₃ and π₁ = 0**.
   - The half-quantum vortex becomes the end of three domain walls, and the 2π vortex the end of six.
   - Hence §2.91.U's protected half-quanta on P7 and I7 are **accidental**: exact at degree ≤ 4, or only if the allowed coefficient of Re S³ is selected to zero.
3. **Robust protection survives only for ψ₀ windings** (2π), on R, MP, MF and MI; U(1)_ψ₀ is an exact symmetry.
   - On the mixed strata under (c), π₁ = ℤ⊕ℤ at degree ≤ 4: the ψ₀ winding plus the 7-sector winding, since the ψ₀²S̄ lock is forbidden.
   - With Re S³, π₁ = ℤ (ψ₀ only) and π₀ = ℤ₃.
   - F7 is unchanged (π₁ = 0; Re S³ vanishes there).
4. **Memo slip (repository only, not in the ledger).** The G-VS1 memo gives dim Sym⁶(ℝ¹⁴) = 11,628. It is C(19,6) = 27,132; no count depended on it.

## DR-A2-4. Linear coupling and friction: verdict DOWNGRADE for texture-type matter

**(i) The declared coupling class does not reach the internal branches** (exact; both legs).
- δρ = 2Re(ψ_vac†δψ) = 0 for δψ ⊥ ψ_vac, and the internal current vanishes too. A defect that couples only through the total density (Branch C) or through the lattice velocity (−ρ_n u̇·v_s) has **no linear coupling** to the internal branches.
- The internal sector has no pairing term, and in the two-body dynamics of record the ⊥ particle number is an exact U(8) charge. So such a defect cannot create internal quanta at any order.
- Second-leg check: in an 8-component GP run with a moving density vertex, the ⊥ number is conserved to 8×10⁻¹³.
- Only the oriented term O (coupling λ, active only at defect cores) can change the ⊥ number.

**(ii) Defects with internal content.**
- **Texture type: Fano-line cores (G-INT1, G-2a-A1 Phase 2) and the K₇ vortex with its Fano winding.**
  - Their internal far field is the gapless Goldstone field itself. The pinned G-2a-A1 profile f = π/(1+r²) has a finite long-wavelength source: its dipolar transform → π per unit amplitude as k → 0 (computed: 3.133 at k = 0.003). A harmonic (Belavin–Polyakov-type) tail gives a source ∝ 2/k.
  - In the object's frame the far field obeys (−½∇² + imv·∇)χ = 0. Its only non-decaying solutions lie on the resonance sphere |k − mv| = mv, which passes through k = 0. So **no localized co-moving solution exists for any v > 0**: the object radiates.
  - The golden-rule drag at small v scales as **F ∝ m*² v in 2D and ∝ m*³ v² in 3D** (both legs; the second leg fits exponents 0.987 and 1.988 and checks a 1D simulation against the golden rule).
  - With m* = 10.5 or 315, the prefactor is large.
- **Bound type: the VC-B annular filament, or a filled core whose filling is bound.**
  - This needs the immiscibility import: at the O(16) point G-CC-ε1 found no stable annular carriers ("miscible probes empty"). An unbound filling is a texture and falls under the case above.
  - With the import, the internal content is a bound state of binding E_b. In a uniform medium the Galilean-boosted bound state is exact, so there is **no emission at any v** (second leg: overlap above 1 − 3×10⁻¹⁰ at v = 2).
  - In the crystal, emission needs **ħG·v ≥ E_b**, i.e. a threshold v_th = E_b/(ħ|G_min|). The second leg's simulated rates match the golden rule to 0.5 % above threshold.

**Verdict.**
- **DOWNGRADE (R1 mechanism, R2 reading).** On the vacuum of record, texture-type matter feels internal-sector friction at every speed. This covers the Fano-line cores and the K₇ vortex, G-QUANTA's independence witness. The vacuum of record cannot host such matter in motion unless an import gaps the internal directions it winds through.
- On stratum R the real-unit-splitting import gaps all seven internal directions. A 7-sector texture is then a localized excitation of a gapped sector, and the Landau speed √(2Δ/m*) must still reach c_T: Δ ≥ ½m*c_T² ≈ 177 ≈ 3.2μ in the 2D substrate units. That is another import-tuning condition, of the second-sound type.
- The VC-B filament with its import has only threshold emission. No downgrade beyond its existing dependence on that import, which belongs to the same class as I6.

## DR-A2-5. Order-by-disorder

Not run. It is registered as the named successor (**G-OBD1**): compute the zero-point (Bogoliubov) energy of each stratum with the G-ζ1/BdG machinery and see whether fluctuations select a stratum. That would turn I6 from an import into a computation. The relevant prior art is Turner et al., PRL 98, 190404 (2007), on order-by-disorder in spinor condensates.

## Honesty items

- **H-A2-1 (exposure, as H-A1-1).** The second leg returned before the first leg's code existed. The first leg's expected counts and Watanabe–Murayama numbers had been reasoned before the dispatch but not filed. Independence rests on the different methods (Molien–Weyl integral and explicit rings versus exact integer kernels) and on the f_s cross-check of m*, which comes from a different route.
- **H-A2-2.** No other items.

## Blast radius (annotations in the Phase A fold)

| entry | annotation |
|---|---|
| §2.91.U (G-VS1) | inventory computed under U(1)_global, which the action lacks; corrected counts; half-quantum protection accidental (lost to the ℤ₃-allowed Re S³); robust protection = ψ₀ windings; Re(ψ₀²S̄) forbidden; internal-branch inventory per stratum |
| §2.88.D.2 (G-INT1) | the gapless internal sector is quadratic (type B), m* = m/f_s (10.5 in 2D, 314–321 in 3D), Landau speed 0; texture-type defects radiate at every speed |
| §2.91.P (G-QUANTA), K₇-vortex row | its witness is texture-type: friction at every speed on the vacuum of record (a dynamical statement; C1/C2 are not re-scored) |
| M.ONT VC-B annex (V4.66) | the filament exists only with the immiscibility import; with it, its internal content is bound (threshold emission); without it, it is a texture |
| Part VI: G-VS1 row, I6 | the half-quantum downgrade; G-OBD1 registered |
