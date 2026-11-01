# E10 / Route B: non-abelian U(3) vortices — classification and plan

*November 1, 2026. Label: Exploration. Classification note. Nothing has been computed. It opens Route B of step 1 (`E9_three_strand_closure/prior/step1_classification.md`) after Route A came back negative in three stabilizer families (`E9_three_strand_closure/STATUS_step3.md`). Citations marked [checked] were confirmed against the source on November 1, 2026; [memory] ones have not been.*

## 0. Why Route B, and what it changes

In Route A the thirds needed an assumption: equal densities (A1). Step 2 also found the thirds **confined**. A single strand carries 1/3 of a flux quantum and costs energy that grows without bound when pulled out, so only the composite of all three is free.

Route B puts the thirds into the gauge group instead:
- **The thirds are exact, by group structure.** A1 is not needed.
- **The thirds are free.** The elementary string, carrying 1/3 of the U(1) flux, is a stable, finite-tension object on its own. The three strands become three independent strings that can braid and link.
- **Each strand has an internal orientation.** A point in CP², which can vary along the string and in time.

The second point reverses step 2's confinement picture. If confinement of the thirds is wanted, Route B does not give it. The third point is what Route A lacked: a field that lives only on the string, which is what a vorton needs.

## 1. The model (declared inputs)

**Fields.**
- U(3) gauge theory: SU(3) gauge field with coupling g, U(1) gauge field with coupling e.
- N_f = 3 flavours of scalars in the fundamental, arranged as a 3 × 3 complex matrix Φ (rows: colour, columns: flavour).
- D_μΦ = ∂_μΦ − i(g A^a_μ T^a + e A_μ c₀ 1)Φ. The normalization c₀ is to be fixed from the literature in B1.

**Potential.**

V = (λ_e/2) (Tr Φ†Φ − 3v²)² + (λ_g/2) Σ_a (Tr Φ†T^aΦ)².

**Vacuum.** Φ = v·1₃, the colour-flavour-locked vacuum. The symmetry breaks as U(3)_C × SU(3)_F → SU(3)_{C+F} [checked: Hanany and Tong, hep-th/0306150].

**BPS point.** There is a point where the quartic couplings equal the gauge couplings (λ_e ∝ e², λ_g = g², exact factors to be fixed in B1). There the vortices satisfy first-order equations and their tension is known exactly. This is the natural primary parameter choice. It is not a tuning toward stability: it is the point where everything checkable is known in closed form.

**Relation to Route A.**
- Route A is the diagonal truncation of this model: Φ = diag(ψ₁, ψ₂, ψ₃), with only the overall U(1) gauged.
- Route B adds the eight SU(3) gauge fields. They screen relative windings, which is why a single strand stops being confined.

A side note. Route A with an SU(3)-invariant potential (|ψ|² − v²)² instead of Σ_k(|ψ_k|² − 1)² would be the **semilocal** model [checked: Hanany and Tong §5]. In that model twisted, current-carrying strings exist without any added field, and have lower energy than the embedded ANO string [checked: Forgács, Reuillon and Volkov, hep-th/0602175]. Their stability was analysed in [checked: Garaud and Volkov, arXiv:0712.3589]. E9's per-component potential breaks SU(3), so this mechanism was not available in E9. It was never tested, and is recorded here as a gap.

## 2. The elementary string

**Profile.** The minimal vortex is Φ = diag(φ₁(r)e^{iθ}, φ₂(r), φ₂(r)), up to colour-flavour rotations. It carries a combination of U(1) flux and SU(3) flux along one Cartan direction, so 1/3 of the U(1) flux quantum [memory: Auzzi, Bolognesi, Evslin, Konishi and Yung, Nucl. Phys. B 673, 187 (2003); the citation is checked, the flux statement is memory].

**Tension.** At the BPS point, T = 2πv² per unit winding [checked as stated in Tong, "Vortices, Strings, and Vortex Strings" talk notes: T = v² Tr ∫F]. The abelian composite (all three entries winding) is three elementary strings with zero binding energy. Off the BPS point the composite either binds or repels; which one is the type I / type II question.

**Moduli.**
- The single string's orientation is a point in CP² = SU(3)_{C+F}/[SU(2) × U(1)] [checked: Tong review, arXiv:0809.5060; Eto et al., JHEP 11 (2010) 042].
- These are massless modes that propagate along the string. Their low-energy dynamics is a 2D CP² sigma model on the worldsheet [checked: Tong review]. The coupling is ∝ 4π/g² at the BPS point [memory].
- **This moduli field is the in-built analogue of option 4's σ.** It lives only on the string, so its charge cannot spread into the bulk as long as its frequency stays below the bulk mass gap. No added field and no assumption A3 are needed.

## 3. Closures Route B makes available

### B-i. The intrinsic vorton (primary)

A loop of elementary string whose CP² orientation rotates in time (charge Q under a U(1) inside SU(3)_{C+F}), and optionally winds along the loop (current k).

**Thin-ring balance, as in option 4.**
- The energy is 2πR·T plus a term in (k² + ω²) times the moduli "inertia" per unit length, I_m. Both pieces of that term scale as 1/R at fixed n and Q.
- An equilibrium needs k² + ω² ≈ T / I_m.
- With T ≈ 2πv² and I_m ∝ 1/g², this puts k² + ω² near g²v², the bulk mass scale m_bulk².
- Charge stays on the string only if ω < m_bulk.

**So the crude estimate puts the equilibrium right at the leak threshold.** In option 4 the same crude estimate was wrong, because the profile adjusts; the straight-string calculation (B3) decides.

**Two differences from option 4.**
- **The winding is not protected.** CP² has trivial π₁, so a winding k along the loop can unwind continuously. Only Q is conserved. A charge-only ring (k = 0) is therefore the cleaner first case.
- **There is no metastable "σ phase" in the bulk** for the charge to fill. The decay into a charged lump that made option 4's ring only metastable may not be open here. Charge that leaves the string must go into massive bulk modes.

**Prior art.**
- Vortons stabilized by non-abelian orientational moduli were built in a toy U(1) × SO(3) model, with an S² of moduli and a triplet condensing in the core. Converged solutions existed only as embeddings of the abelian case. Above a critical frequency they decayed into a spinning Q-ring with no vortex winding [checked: Tallarita, Peterson, Bolognesi and Bedford, Eur. Phys. J. C 80, 38 (2020)].
- **That paper does not treat the colour-flavour-locked U(N) case.** It lists more complicated non-abelian setups with non-abelian gauge fields as future directions [checked].
- Whether the U(3) case has been done since 2020 must be searched in B1.

**Quantum caveat.** The 2D CP² sigma model on the string is asymptotically free, and quantum mechanically the moduli acquire a gap. Everything here is classical. A classical STABLE result would say nothing about the quantum string.

### B-ii. Braided and linked elementary strings (secondary)

Three elementary strings with different orientations can braid, link, or close as one string wound three times (the q = 1, 2 closures of E9 Phase B).

**There is no protection here either.** A strand-permuting closure is just a twist of the orientation along the loop, which is continuous (CP² is connected). Linking is preserved only if strings cannot pass through each other. How non-abelian strings reconnect depends on their relative orientation [memory: Eto et al. (2006); the abstract of arXiv:1105.1547 discusses orientation-dependent reconnection and scattering, checked only at abstract level].

**Forces.** At the BPS point elementary strings exert no static force on each other. Off it the force depends on relative orientation [memory: Auzzi, Eto and Vinci (2008)].

This is lower priority than B-i, because it needs off-BPS forces before any closure question is meaningful.

## 4. Assumptions and Eddington guard

**What Route B removes.**
- A1 (equal densities) is not needed.
- A3 (an added σ) is not needed for B-i.
- No chiral term (A5, A6) is needed.

**What Route B adds.**
- The SU(3) gauge sector.
- Parameters g, e, λ_e, λ_g and v. The BPS point is the declared primary; off-BPS values are secondary, chosen by a rule fixed before any loop run.

**Unchanged.**
- No particle identification.
- B-i's orientation charge is not the electric charge. It is a charge of the global SU(3)_{C+F}.
- "Thirds" here are thirds of U(1) magnetic flux, as in step 1. Turning flux into electric charge still needs the duality step, which has not been taken.

## 5. Plan

| step | what | output | status |
|---|---|---|---|
| **B1** | Prior address: fix the normalizations (c₀, the BPS relations, the worldsheet coupling) from Shifman–Yung, Eto et al. and Tong; search for colour-flavour-locked vortons after 2020; check the [memory] items above. | `prior_address_routeB.md` | next |
| **B2** | Straight elementary string, radial ansatz, pre-registered like step 2. Check at the BPS point: T = 2πv², flux 1/3, composite = 3 × elementary. Off-BPS: the sign of the composite's binding (type I/II). Compute the moduli inertia I_m numerically, from the zero-mode normalization or a small rotating-moduli solve, and compare with the BPS worldsheet coupling. | PREREG + results | after B1 |
| **B3** | Straight-string fixed-charge scan, as in Phase 0: ℰ(k, q) with moduli current and charge. Thin-ring 𝒯 = 0 search against the leak threshold ω < m_bulk. Charge-only (k = 0) first. | PREREG + results | after B2 |
| **B4** | Axisymmetric loop, only if B3 finds a window, with controls fixed in advance. The passenger control becomes: the same SU(3)_{C+F} charge carried by a bulk configuration with no string (moduli do not exist without the string, so the comparison is against the cheapest charged bulk lump). | PREREG + results | after B3 |

**Cost.** B2 and B3 are 1D radial problems with a few profile functions, so minutes. B4 is an axisymmetric 2D problem with the U(3) fields, so hours. Full 3D is deferred.
