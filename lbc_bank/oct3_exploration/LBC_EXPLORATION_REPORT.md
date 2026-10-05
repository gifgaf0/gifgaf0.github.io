# Longitudinal branch coupling in the instantiated supersolid — exploration report

**Mode:** exploration (author brief, Oct 3 2026). Base V4.88. No lock, no two-leg, no T1/sealed anchors, no fold, no canonical edit. Prior Address, Eddington quarantine and M.CW observed. Single chat leg plus one *internal* second route (static hydrodynamics, no BdG input). Substrate units throughout; "c" below means c_T under ANNEX-CDEF-1 only.

## The answer

**Both branches — and the second-sound coupling is generic, not symmetry-forbidden.** On the MV-G1 p6m state at the canonical point (g = 22 soft-core, a* = 1.45747, μ = 55.854), a localized density source couples to second sound (c₂ = 1.765 ≈ 0.31 c) with **one third of the spectral weight** it puts into first sound (c_L1 = 11.045 ≈ 1.91 c): Z₂/Z₁ = 0.334. Second sound carries 5.1 % of the f-sum but **67 % of the static (ω = 0) density response** — a knot at rest deforms the substrate mainly through the slow branch. The transverse branch carries zero weight (≤ 10⁻¹⁷, symmetry). In the 3D AB/hcp stack (G-TSH4 machinery) the same holds with a slower branch: c₂ = 0.477 ≈ 0.06 c, Z₂/Z₁ = 0.06, static share 66 %.

Consequence: the reading "first sound is superluminal, so the longitudinal channel is Cherenkov-safe" is not available. **KC3 and KC1 apply** to every knot whose coupling has a direct density term (the G-IIB-L1 T5 [static-core-direct] class). The only escape is the one already registered and unresolved: the drive-mediated/zero-independent-sourcing class of the M.ONT coupling-class annex.

## 1. Literature (first, per brief)

- **2D supersolid hydrodynamics at T = 0** — Yoo & Dorsey, PRB 81, 134518 (2010); Platt, Baillie & Blakie, *Excitations of a two-dimensional supersolid* (arXiv:2407.01072, 2024): sound speeds from a_Δ = ρα_ρρ − 2α_ρu + α_uu/ρ_n, b_Δ = (ρ_s/ρ_n)(α_ρρα_uu − α_ρu²); **c_t² = μ̃/ρ_n**; second sound has a "weak density contribution" (nonzero); hydrodynamics vs BdG "almost indiscernible". My derivation below reproduces their a_Δ, b_Δ exactly.
- **Weights never zero** — Platt, Baillie & Blakie, *Supersolid spectroscopy* (arXiv:2412.15552): both gapless branches carry density weight at small k; f_s is extracted from the two speeds and the compressibility speed (their Eq. 26); measuring χ^ρ_ν for both branches determines f_s. Yoo–Dorsey: "the onset of supersolidity produces peaks in the response function, corresponding to propagating second sound modes". In He-II, by contrast, the decoupling of second sound from density is *thermodynamic* (α_P ≈ 0, a temperature wave), not structural — it does not transfer to a T = 0 supersolid whose lower mode is superfluid–lattice counterflow.
- **Landau criterion with several branches** — Kunimi & Kato, PRB 86, 060510(R) (2012), *the same 2D soft-core model*: "The lowest branch in the SS phase is the Bogoliubov mode, which causes instabilities"; Landau/dynamical instabilities set at long wavelength by that branch. Danshita & Yamamoto, PRA 82, 013645 (2010): supersolid critical velocity "significantly smaller than that for a conventional superfluid", the lowest gapless branch going soft first. Rule: v_c = min over *coupled* branches of min_k ω/k.
- **Einstein-aether** — Elliott, Moore & Stoica, JHEP 08 (2005) 066 (with Moore–Nelson 2001): five propagating modes, all coupled to matter through the metric; UHE cosmic-ray survival forces every coupled mode to ≥ c (the "all modes ≥ c" practice); a mode escapes only if it does not couple at the relevant order. That is exactly the question computed here, and the answer is "it couples".
- **Classical escapes** (already in the V4.63 LSF; Whittaker, *History of the Theories of Aether and Electricity*): Green 1838 — longitudinal speed infinite (incompressible constraint sector); Cauchy — longitudinal speed zero (negative compressibility; Green: unstable); MacCullagh 1839 — rotational elasticity, no longitudinal mode. The instantiated substrate is none of these: it has two *finite-speed* longitudinal branches, one of them slow.
- A0 reading: nothing here is novel physics — the weights of a two-branch supersolid are textbook since Yoo–Dorsey; what is new to the ledger is only that the question was asked of *this* substrate.

## 2. Expectation, stated before computing

Filed as `EXPECTATION_pre_compute.md` (md5 a1712aa1, 01:23 UTC, before any weight was evaluated): both branches couple; from the T = 0 Lagrangian ℒ = −ρ(θ̇ + ½(∇θ)²) + ½ρ_n(u̇ − ∇θ)² − e(ρ, u_ij),

χ(q,ω) = q²(ρ_nρω² − ρ_s M q²) / [ρ_n ω⁴ − (M + ρ_nρα − 2ρ_nγ) q²ω² + ρ_s(αM − γ²) q⁴],

so the lower branch's f-sum share is **F₂ = (c_*² − c₂²)/(c₁² − c₂²) with c_*² = ρ_s M/(ρ_n ρ)** (M = uniaxial modulus at fixed density). F₂ = 0 only if c₂² = ρ_sM/(ρ_nρ): a tuning condition, no symmetry behind it. Expected at g = 22: F₂ ~ 0.1–0.3, Z₂/Z₁ ~ O(1), static response dominated by the slow branch. (Outcome: F₂ = 0.05, Z₂/Z₁ = 0.33, static 67 % — direction and orders right, F₂ at the low edge.)

## 3. Computation and result

**Instrument.** `lbc_weights.py` imports the G-TSH1 chat-leg instrument `g_tsh1_chatleg.py` unchanged (cell geometry, relax, dt-staged polish, F9 Ward check, the Hermitian pencil M = L^½(L+2X)L^½, the P/f_T classifier) and adds one quantity: the long-wavelength density matrix element of every BdG mode, ρ_ν(q) = ∫_cell e^{−iq·r} ψ₀ f₊,ν with ∫(|u|²−|v|²) = 1, Z_ν = |ρ_ν|². The state of record reproduces exactly (μ = 55.85362, E/A = 31.26603, Ward 1.9×10⁻³; branch frequencies identical to the §2.91.I rows). Two checks hold at every q, both directions, n = 32 and 40: the **f-sum rule** Σ_ν ω_ν Z_ν = N_cell q²/2 to 10⁻⁶, and the **static sum** Σ 2Z_ν/ω_ν equals a direct solve of (L+2X)f = −2Vψ₀ to 10⁻⁶. Gapped bands carry < 10⁻³ of the f-sum (∝ q⁴). T1 self-grep clean on all three files.

**Canonical point (Γ–M = Γ–K to 0.1 %; n = 32 = n = 40 to 4 digits; read at kf = 0.05 inside the locked windows; Z₂/q is flat to 1 % over kf 0.03–0.10 and to 2.5 % out to 0.15):**

| branch | speed (record) | Z/q per cell | f-sum share | static share |
|---|---|---|---|---|
| second sound | 1.765 (0.306 c) | **0.0260** | 5.1 % | **67 %** |
| transverse | 5.775 (≡ c) | ≤ 10⁻¹⁷ | 0 | 0 |
| first sound | 11.045 (1.91 c) | 0.0781 | 94.8 % | 33 % |

Z₂/Z₁ = 0.334. (At kf = 0.01 the lower weight reads 8 % low — the Goldstone floor of the record state; excluded, as the locked windows already do.)

**Independent static route (`lbc_hydro.py`, no BdG input).** Phase-twist superfluid fraction f_s = 0.0952 (x = y, k-independent to 2×10⁻⁵); strained-cell moduli α = 43.73, M = C_xxxx = 91.61 (= C_yyyy to 0.03 %), λ = C_xxyy = 30.51, μ = 30.56 (shear; = (C_xxxx−C_xxyy)/2 to 0.01 %), γ = 8.02 (x = y to 0.05 %). Hydrodynamic prediction vs BdG: c₁ 11.21 vs 11.05–11.17; c₂ 1.82 vs 1.77–1.81; **c_T = √(μ/ρ_n) = 5.81 vs 5.78** (√(μ/ρ) would give 5.53 — the ρ_n form is the right one); **F₂ = 5.2 % vs 5.1 %; Z₂/q = 0.0262 vs 0.0260; static share 0.675 vs 0.673; χ_static = 0.0428 vs 0.0428.** c_*² = 9.64 against c₂² ≈ 3.2: the lower weight is nonzero because f_sM/(ρ_nρ) is three times c₂², and nothing fixes those to be equal.

**Genericity across the G-TSH1 sweep (Γ–M, kf = 0.05):**

| point | c₂/c_T | Z₂/Z₁ | F₂ | static share |
|---|---|---|---|---|
| soft g = 22 | 0.315 | 0.334 | 5.1 % | 0.67 |
| soft g = 28 | 0.196 | 0.214 | 2.1 % | 0.68 |
| soft g = 34 | 0.129 | 0.148 | 1.0 % | 0.69 |
| soft g = 44 | 0.069 | 0.087 | 0.3 % | 0.70 |
| γ6 g = 35 | 0.332 | 0.279 | 4.3 % | 0.63 |

The weight decreases smoothly with f_s (as F₂ ≈ O(f_s) says) and never approaches zero; the slow branch keeps two thirds of the static response everywhere. **Verdict on the brief's question: generic, not symmetry.**

## 4. 3D check (G-TSH4 AB/hcp)

`lbc_3d.py` uses the CC route-D machinery verbatim (`tsh4_core.py`, `tsh4_routeD.py`, main) on the certified AB point (a = 1.38596, c = 2.25960, step kernel, Λ = 2Λ_c = 43.43, grid 42×72×68, g_cut = 22, NG = 1355), with the in-basis relax so the Goldstone floor is clean (L₀ zero mode 1.6×10⁻¹¹; four Goldstones at Γ; the three sublattice Josephson modes at 0.86–0.97 and the transverse pair carry no density weight, ≤ 10⁻²⁵). Sum rules hold to 10⁻⁶ at all nine q-points. Results (q = 0.15–0.6, basal Γ–M, Γ–K and axial): **c₂ = 0.477** (linear; the chat-leg G-TSH4 slope 0.47 confirmed), c_T = 7.6–8.0, c_L1 = 16.1 (basal) / 16.9 (axial); **c₂/c_T = 0.062**; Z₂/q = 0.0134–0.0140, Z₁/q = 0.22–0.23, **Z₂/Z₁ = 0.058–0.063**, F₂ = 0.17 %, **static share 0.66–0.69.** 3D does not rescue anything: the sourced slow branch sits at 6 % of c instead of 31 %.

## 5. KC3 and KC1 under the answer — plainly

- **KC3 (Cherenkov / Landau) applies.** A knot with any direct density coupling emits into second sound above c₂: 0.31 c on the 2D canonical state, 0.07 c at g = 44, 0.06 c in the 3D stack. The coupling is not suppressed by any small parameter (Z₂/Z₁ = 0.33 in 2D, 0.06 in 3D), while the Moore–Nelson bound sits at the 10⁻¹⁵ level in 1 − c_g/c for gravitational-strength coupling — an O(10⁻¹)-weight branch at 0.3 c (or 0.06 c) is not in the same universe as that bound; no mechanism in the result supplies the missing orders. This is the superfluid-dialect twin exactly as Kunimi–Kato state it for this model, and the Einstein-aether rule applied to a coupled mode. The V4.67 kill is not re-litigated; this is a second, independent kill route on the measured substrate that the fluid-branch lock had hidden. G-IIB-L1 T4 (exact subsonic silence) still holds branch by branch — "subsonic" now means v < c₂.
- **KC1 applies, with the slow branch as the dominant radiator.** A density-coupled binary radiates into both branches with the T2/T3 multipole structure (dipole ⟺ non-universality; quadrupole generic). Kinematically, acoustic multipole power grows as an inverse power of the branch speed (3D: monopole c⁻¹, dipole c⁻³, quadrupole c⁻⁵), so at equal coupling the second-sound quadrupole channel outruns the first-sound one by ~(c₁/c₂)⁵·(Z₂/Z₁) ~ 10⁶ in 3D. Coupling magnitude stays M.CW-walled; the structural statement needs none: the longitudinal sector *is* an independently sourced propagating channel with a subluminal branch — the A1.3 single requirement fails for the direct-coupling class.
- KC2 (Carlip aberration), one line: the static near field is 67 % on the c₂ branch, so finite-speed retardation of a Bjerknes-type near field is set by 0.31 c (0.06 c in 3D), not by 1.91 c.
- What survives: the drive-mediated, zero-independent-sourcing class (T5 second branch, CM-2 "global drive") — a knot that responds to a global drive and sources nothing on its own does not excite either branch at linear order. It remains a declaration (the registered M.ONT coupling-class annex), and this result sharpens its stakes: the annex must now exclude *any* static-profile density term, since even a 6 %-weight slow branch is fatal.

## 6. Declarations: load-bearing here vs scaffolding for the dead fluid branch

**Load-bearing for this question**
- I1–I3 import ticket (§3.4-SYM, V4.26) and the MV-G1 state: the substrate itself.
- §2.88.D.1 (G-ζ1) R1 residue: "verified supersolid, Bogoliubov–Bloch instrument sound and reusable" — the instrument used.
- §2.91.I (G-TSH1): the state of record, the three branch speeds, the Phase-0 certification (Amendment 1), F9 Ward discipline, the locked k-windows.
- ANNEX-CDEF-1 (V4.71): c ≡ c_T — without it "0.31 c" and "1.91 c" are not statements.
- BD-IIB-1 + A1 *as a kill-set definition*: KC1(a)/(b), KC2, KC3 and the A1.3 single structural requirement; the §2.91.D blast radius.
- §2.91.F (G-IIB-L1) T2–T5: the multipole structure and the coupling-class dichotomy; the M.ONT coupling-class annex (V4.64) as the open hinge.
- §2.88.B 2D→3D caveat and §2.91.K (G-TSH4): the 3D stack and its certified AB point.
- T4 substrate-units discipline, M.CW: no magnitudes claimed.

**Scaffolding for the fluid branch (context only this session; two items are now known not to describe the substrate)**
- κ ≡ K/(ρ_s c²) = φ⁻⁴ ⇒ c_s = φ⁻²c = 0.382 c (BD-IIB-1): the instantiated substrate has no branch at 0.382 c and no modulus ratio near 0.146 — its lattice is Cauchy-class to 0.15 % (λ = 30.5, μ = 30.6, K₂D/μ = 2.0). κ's "sixth, mechanical role" never touched the instantiation (as the V4.63 record itself labels it: an import).
- The I-CONST fluid-branch LOCK and the G-TSH1 election D1(a) "fluid-as-locked": the device that kept this question closed. The recorded solid branch (c_L = 1.216 c, ν = −0.543 auxetic) is scaffolding too: it was κ-algebra, and the measured lattice has ν₂D = λ/(λ+2μ) = +0.33 and c_L1/c_T = 1.91 (2D) / 2.1 (3D).
- A-Z0 (Z₀ = ρ_s c_s) and K = Z₀²/ρ_s: single-branch impedance bookkeeping; with two branches it maps to neither without a new declaration.
- G-CC-ε1 / Branch C coupling annex / VC-B maps / the ε program, and ANNEX-SC-1 (ξ = ℓ_P) with its KC3 constraint curve: built to evaluate KC3 on the declared 0.382 c branch; their numbers do not transfer to c₂ without re-derivation (and the branch change only widens the Cherenkov cone).
- Orthogonal, untouched: A-SHEAR/the Q3 carrier-identity items and the GW170817 transverse pass (transverse channel only); §2.52 Open 3 (standing freeze).

Incidental R2-grade observation (claims nothing): the G-TSH1/TSH2 annotation that R_T sits 6–9 % below the Cauchy value 1/√3 is explained by the two-fluid kinematics, not by the lattice — the elastic tensor *is* Cauchy-class; c_T² = μ/ρ_n while c_L1² = ½(a_Δ + √(a_Δ²−4b_Δ)) is stiffened by the superfluid compressibility (ρα − 2γ = 27.7 on top of M/ρ_n = 101.2).

## Limits and honesty

Single chat leg; no lock, no CC leg, no comparator — nothing here is registrable as it stands. The hydrodynamic route is an internal cross-check (independent inputs, same substrate), not a second leg. Speeds quoted from this run are per-rung ω/q at kf = 0.05 and differ from the record's window fits by 0.3–1 %. The 3D state's full-grid residual after the in-basis truncation is 3×10⁻³ (the basis-stationarity is exact, which is what the weights need) — same discipline as CC's `relax_truncated`. The project store is at its cap (≈5.8 kB free), so no artifact was written there.

## Artifacts (scratchpad `lbc/`)

`EXPECTATION_pre_compute.md` a1712aa1 · `lbc_weights.py` 1de2304d · `lbc_hydro.py` 9881f146 · `lbc_3d.py` 2927f844 · `lbc_results.json` 67337334 · `lbc_hydro.json` a7d83a1f · `lbc_3d.json` 8c0949f2. Inputs: `g_tsh1_chatleg.py` and `tsh4_core.py`/`tsh4_routeD.py` from the repo (branch claude/sqt-framework-perspectives-kMZyw at 4a370f2; main at bd1354d9), unmodified.

## Sources

- Platt, Baillie, Blakie, *Excitations of a two-dimensional supersolid*, arXiv:2407.01072 — https://arxiv.org/html/2407.01072v1
- Platt, Baillie, Blakie, *Supersolid spectroscopy*, arXiv:2412.15552 — https://arxiv.org/pdf/2412.15552
- Yoo & Dorsey, *Hydrodynamic theory of supersolids*, PRB 81, 134518 (2010) — https://arxiv.org/abs/1001.0621
- Kunimi & Kato, *Mean-field and stability analyses of two-dimensional flowing soft-core bosons modeling a supersolid*, PRB 86, 060510(R) (2012) — https://arxiv.org/html/1205.2126
- Danshita & Yamamoto, *Critical velocity of flowing supersolids of dipolar Bose gases in optical lattices*, PRA 82, 013645 (2010) — https://arxiv.org/html/1002.3925
- Elliott, Moore, Stoica, *Constraining the New Aether: gravitational Cherenkov radiation*, JHEP 08 (2005) 066 — https://ar5iv.arxiv.org/html/hep-ph/0505211
- Moore & Nelson, JHEP 09 (2001) 023 (ledger, V4.63 A1)
- Whittaker, *A History of the Theories of Aether and Electricity*, ch. V (Green 1838, MacCullagh 1839, Cauchy's contractile ether) — https://en.wikisource.org/wiki/A_History_of_the_Theories_of_Aether_and_Electricity/Chapter_5
- Ancilotto, Rossi, Toigo, *Supersolid structure and excitation spectrum of soft-core bosons in 3D*, PRA 88, 033618 (2013) — https://ar5iv.labs.arxiv.org/html/1309.2769
