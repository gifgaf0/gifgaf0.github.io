# Q-D notes (cc second leg): drag prefactor, loss-length arithmetic, Eq. (3)/(4)

Files: `cc_loss.py` (reads `qb_results.json`, writes `qd_results.json`; runtime about 2 s), this note.
Units ħ = m = 1. Every number below is copied from `qd_results.json` (full repr there).

## 1. Conventions

- Defect at X(t) = v t couples to the medium density: H_int = ∫ d³r V(r − X(t)) n(r).
- Fourier convention: V(q) = ∫ d³r e^{−iq·r} V(r), so a contact vertex V(r) = g_d δ(r) has V(q) = g_d.
  (C depends on this. With the symmetric convention V_s = (2π)^{−3/2} V one would get C_s = 2π²
  = 19.739208802178716; recorded as an extra key, not used.)
- Medium response (retarded, linear branches):
  χ(q, ω) = ρ q² Σ_ν F_ν / ((ω + i0)² − c_ν² q²).
  Static limit χ(q, 0) = −ρ Σ F_ν/c_ν² = −ρ/c_κ² (negative, as it must be). The f-sum
  −(1/π)∫₀^∞ ω Im χ dω = ρq²/2 · Σ F_ν, so the F_ν are exactly the dispatch's f-sum shares.
- Im χ(q, ω) = −π ρ q² Σ_ν F_ν sgn(ω) δ(ω² − c_ν² q²).
- At T = 0 the dynamic structure factor per volume is S(q, ω) = −(1/π) Im χ(q, ω) for ω > 0, i.e.
  S(q, ω) = Σ_ν (ρ q F_ν / (2 c_ν)) δ(ω − c_ν q).

## 2. Route A: linear-response force

Force on the defect: F = −∂_X ∫ V(r − X) n(r) d³r. With δn(q, t) = χ(q, q·v) V(q) e^{−iq·vt} (the external
potential has frequency ω = q·v for wave vector q) one finds, after symmetrising q → −q and using
χ(−q, −ω) = χ(q, ω)*,

  F = ∫ d³q/(2π)³ q |V(q)|² Im χ(q, q·v).

Along v, with μ = cos θ and d³q = 2π q² dq dμ:

  F_∥ = (1/4π²) ∫ q² dq |V|² ∫_{−1}^{1} dμ q μ Im χ(q, q v μ).

Insert Im χ: δ(q²v²μ² − c²q²) has roots μ = ±c/v (they exist only for v > c), each with
|∂_μ(q²v²μ²)| = 2 q² v c. Both roots give the same sign of μ·sgn(μ) and contribute equally:

  ∫ dμ q μ Im χ = −π ρ F q³ · 2 · (c/v) / (2 q² v c) = −π ρ F q / v².

Hence F_∥ = −(1/4π²) · π ρ F v^{−2} ∫ q³ |V|² dq, i.e. a drag (antiparallel to v)

  **F_d = (1/4π) ρ F_ν v^{−2} ∫₀^∞ q³ |V(q)|² dq**,  C = 1/(4π) = 0.07957747154594767,

per branch with c_ν < v (branches with c_ν > v do not contribute: no root). For linear branches the result is
independent of c_ν apart from the threshold; the angular measure dμ is uniform, so no Mach factor appears.

## 3. Route B: Fermi golden rule / energy balance F v = dE/dt

Write H_int = Vol^{−1} Σ_q V(q) e^{−iq·vt} n_q^† (n_q = ∫ e^{−iq·r} n). Each term is a harmonic perturbation of
frequency q·v; the golden rule gives the absorption rate Γ_q = 2π Vol^{−1} |V(q)|² S(q, q·v) and the
energy-absorption rate

  dE/dt = ∫ d³q/(2π)³ 2π |V(q)|² (q·v) S(q, q·v).

With S = (ρ q F/(2c)) δ(ω − c q): only μ = c/v > 0 contributes,
∫ dμ (q v μ)(ρ q F/2c) δ(q v μ − c q) = (c q)(ρ q F/2c)/(q v) = ρ F q/(2v), and 2π·2π/(2π)³ = 1/(2π):

  dE/dt = (1/2π) ∫ q² dq |V|² ρ F q/(2v) = ρ F/(4π v) ∫ q³ |V|² dq,

so F_d = (dE/dt)/v = (1/4π) ρ F v^{−2} ∫ q³ |V|² dq. Same C. (The momentum-transfer rate
∫ d³q/(2π)³ 2π |V|² q S(q, q·v) gives the identical force since ω = q·v on shell.) Route A uses both signs of
the frequency with the retarded Im χ; Route B uses only absorption with S from the f-sum; they agree because
of the T = 0 fluctuation–dissipation relation.

Numerical confirmation in `cc_loss.py` (`drag_derivation_checks`):
- (a1) angular integral with damping η = ε c q (then the q integral factorises exactly), ε → 0 by Richardson,
  at M ∈ {1.2, φ², 5, M_new}: ratio to the analytic limit 1 to ≤ 2.2e-9;
- (a2) full (q, μ) double integral with constant damping and a Gaussian vertex, η → 0;
- (b) golden rule with a Gaussian-smeared δ, σ → 0;
- all eight numerical C estimates agree with 1/(4π) to max relative deviation 2.1526629367940586e-09.

## 4. Single Bogoliubov branch, contact vertex; comparison with Astrakharchik & Pitaevskii

Bogoliubov: ε(q) = (c²q² + q⁴/4)^{1/2}, c² = g n; S(q, ω) = n (q²/2)/ε(q) · δ(ω − ε(q)), so the one branch
exhausts the f-sum at every q (F = 1 exactly, Feynman relation). Contact vertex V(q) = g_d.
The Cherenkov root is μ = ε(q)/(q v) ≤ 1, i.e. c² + q²/4 ≤ v², which cuts the q integral at
q_max = 2 (v² − c²)^{1/2} (the exact dispersion supplies the cut-off that a contact vertex with a linear branch
would lack). The μ integral still gives n q/(2v) for q < q_max, so the formula of Sec. 2 applies with the cut:

  F_d = (1/4π) n g_d² v^{−2} q_max⁴/4 = g_d² n (v² − c²)² / (π v²)  (ħ = m = 1)
     = g_d² n m³ (v² − c²)² / (π ħ⁴ v²)
     = 4π n b² m v² (1 − c²/v²)² Θ(v − c)  for g_d = 2πħ² b/m (heavy impurity, reduced mass → m).

Checked numerically (golden rule with exact dispersion, smeared δ, σ → 0) at v/c = 1.5 and 2.5: relative
deviation ≤ 7.2e-11.

AP comparison. The direct fetch of the paper (arXiv cond-mat/0307247, PRA 70, 013608) was refused by the
network egress proxy (arxiv.org, link.aps.org, osti.gov and researchgate.net all blocked by organization
policy). The only reachable material was search-engine text quoting the AP three-dimensional drag as
F = −4π n b² m v² (1 − c²/v²)² Θ(v − c), and a d-dimensional form
F_d(v) = [s_{d−1}/(2π)^{d−1}] m^d n g² ħ^{−(d+1)} [(v² − c²)/v]^{d−1} Θ(v − c) (s_{d−1} = 4π, 2π for d = 3, 2).
The reduction above reproduces both exactly (d = 3: s₂/(2π)² = 1/π). So C = 1/(4π) is consistent with the
AP three-dimensional result; the equation number "(12)" itself could not be verified first-hand, and the
quoted forms come from second-hand summaries — flagged in the return.

## 5. 2D (filament) analogue and the origin of S(M)

A straight filament along z moving transversely: V(q) = 2π δ(q_z) V_⊥(q_⊥), so per unit length the problem is
two-dimensional with ρ the 3D density (equivalently a point defect in a 2D medium). With q·v = q v cos θ and
the measure q dq dθ/(2π)²:

  ∫₀^{2π} dθ q cos θ Im χ(q, q v cos θ) = −π ρ F q³ Σ_roots (c/v) / (2 q² v c sin θ₀),

with four roots cos θ = ±c/v and |∂_θ(q²v²cos²θ)| = 2 q² v c sin θ₀, sin θ₀ = (1 − c²/v²)^{1/2}. Hence

  F_d/L = (1/2π) ρ F_ν v^{−2} S(M) ∫₀^∞ q² |V_⊥(q)|² dq,  S(M) = (1 − 1/M²)^{−1/2}, M = v/c_ν.

Where S(M) comes from: the Cherenkov condition is a δ function in the direction of q. On the circle the measure
is dθ = dμ/(1 − μ²)^{1/2}, so the Jacobian at μ = 1/M is (1 − 1/M²)^{−1/2} = S(M). On the sphere the measure
dμ is uniform and no such factor arises. In d dimensions the measure is (1 − μ²)^{(d−3)/2} dμ, giving
S(M)^{3−d}: d = 3 none, d = 2 one power. The numerical angular integrals (a1) reproduce S(M) in 2D to 4.4e-11
and a constant in 3D. The golden-rule route gives the same 2D result (two roots with μ > 0, Jacobian
1/(q v sin θ₀)). Bogoliubov 2D check: F = g_d² n (v² − c²)/v, numerically confirmed to 8.0e-11.

## 6. Loss-length arithmetic (dispatch Q-D item 2)

Inputs from this leg's `qb_results.json`: c₂ = 0.470555527432646 (ω/q at q = 0.15 along x),
F₂ = 0.0016666207042539045 (q = 0.15) and 0.001657360829173931 (q = 0.3), c_κ = 9.38464586499687
(q = 0.15 along x). Stated inputs: γ = 3.1974e11, ξ = 1.616255e-35 m, L_prop = 3.0857e20 m, M_old = φ²,
c_T = 7.68, the four maps (Â, Ĵ, Ô, T̂ = τ̂).

Closure ℓ = γ M_old τ̂ ξ/𝒫, 𝒫 ∈ {Â, Ĵ, Ô}, τ̂ = T̂ of the same point. log₁₀(ℓ/L_prop):

| point | Â | Ĵ | Ô |
|---|---|---|---|
| p1 | −43.63272210695509 | −43.12198237924249 | −42.71180791415344 |
| p2 | −43.89113261602559 | −42.705650840163834 | −43.13519133376428 |
| p3 | −43.621260287510744 | −43.129993476497056 | −42.56277099632161 |
| p4 | −43.569192584910276 | −43.177510019691326 | −41.96090432548734 |

- v467 best (most favourable = largest ℓ) = −41.96090432548734 (p4, Ô); worst = −43.89113261602559 (p2, Â).
- M_new = 7.68/c₂ = 16.321134387480537; S(φ²) = 1.0820445430988213; S(M_new) = 1.0018823232305865;
  S(φ²)/S(M_new) = 1.0800116121519645 (only 0.033428424992884655 orders).
- Main factor = [S(φ²)/S(M_new)]/F₂ = 648.0248381622338 (q = 0.15), 651.6454311824593 (q = 0.3).
- main_orders_recovered = [2.811591652275018, 2.814011354678906].
- main_headline_orders = [−39.14931267321232, −39.14689297080844].
- ξ_req (old closure, p4/Ô) = L_prop 𝒫/(γ M_old τ̂) = 14771146.547985597 m; divided by the main factor:
  xi_req_main_m = [22667.45969688186, 22794.105531318575] m.

### Four readings (this leg's interpretation)

c_s = c_T/φ² = 2.9334989664008075, (c_κ/c_s)⁴ = 104.74367263537826.

| reading | factor on ℓ | log₁₀ (q = 0.15 / q = 0.3) |
|---|---|---|
| R1 fixed vertex, filament | [S(φ²)/S(M_new)]/F₂ | 2.811591652275018 / 2.814011354678906 |
| R2 fixed vertex, point source | 1/F₂ | 2.7781632272821333 / 2.7805829296860214 |
| R3 closure literal, M → c_T/c₂ | (M_new/φ²)/F₂ | 3.572938287542042 / 3.57535798994593 |
| R4 fixed dressed static deficit | R1/(c_κ/c_s)⁴ | 0.791463854742054 / 0.7938835571459422 |

band_orders = best + [min, max] over the eight entries = [−41.169440470745286, −38.38554633554141]
(band in recovered orders [0.791463854742054, 3.57535798994593]).

Alternatives (extra keys): R3 without 1/F₂ (factor M_new/φ² = 6.234118601062868) → band
[−41.169440470745286, −39.14689297080844]; R4 applied to the point-source factor (1/F₂)/(c_κ/c_s)⁴ → band
[−41.20286889573817, −38.38554633554141]; c_κ at q → 0 (9.386022556462432) → band
[−41.169695289378026, −38.38554633554141]; c₂ from the LSQ slope over q = 0.15, 0.3 and the own mean transverse
speed instead of 7.68 move the orders by ≤ 4e-2 (see `alternatives`).

### Critique of the readings

1. Which branches radiate. At v = c_T = 7.68 the defect is supersonic for branch 2 (c₂ ≈ 0.47) and subsonic
   for branch 1 (c₁ ≈ 16.1), so only branch 2 contributes and the drag carries F₂ instead of the old F = 1.
   The transverse branch has zero density weight along mirror directions and does not couple to a
   density vertex (off-mirror it has a small weight, neglected). This is what R1 and R2 encode, and the
   1/F₂ is the whole effect: the Mach-factor ratio adds only 0.033 orders.
2. R1 vs R2. The filament formula carries S(M) (Sec. 5); the point-source formula does not (Sec. 2). At fixed v
   and fixed vertex the loss-length ratio is [S(M_old)/S(M_new)]/F₂ (filament) or 1/F₂ (point). Both assume the
   old closure is the one-branch, F = 1 limit of the same formula at Mach φ².
3. R3 is not derivable from either drag formula. At fixed v and fixed vertex M enters only through S(M)
   (filament) or not at all (point). If instead c is fixed and v = M c, F_d ∝ v^{−2} gives ℓ ∝ M² (times S),
   not ∝ M. The "closure literal" linear-M substitution is therefore a bookkeeping reading of
   ℓ = γ M τ̂ ξ/𝒫 that sets the upper edge of the band; it should not be read as physics.
4. R4 depends on what "dressed static deficit" means. Holding δN = |χ(0)| V = ρ V/c_κ² fixed gives V ∝ c_κ² and
   drag ∝ c_κ⁴, so ℓ picks up (c_s/c_κ)⁴ with the old medium's compressibility speed taken as c_s = c_T/φ²
   (i.e. assuming the old medium was a simple superfluid with M_old = c_T/c_s). But c_κ here is the
   lattice-relaxed static response, two thirds of which (S₂ = 0.6629042326549988) sits in the slow branch; a
   defect moving at v ≫ c₂ never establishes the slow-branch part of its deficit. Using the unrelaxed static
   response 1/c_u² = (1 − S₂)/c_κ² (c_u = 16.16371704213341) would lower R4 to log₁₀ −0.1530295463580978 /
   −0.15060984395420965 (recorded as a diagnostic, not in the band). The q = 0.15 vs q → 0 choice for c_κ is
   negligible (≤ 3e-4 orders).
5. Linear-branch scope. Every reading takes F₂ at q = 0.15–0.3 (the two values differ by 0.56 %). The drag
   integral weights |V(q)|² at all q. For a vertex whose support reaches q ~ 2π/a, the linear-branch form with
   q-independent F₂ fails there, and Cherenkov emission into gapped bands with ω_gap < q v becomes allowed.
   So the 1/F₂ suppression holds only for vertices that are smooth on the lattice scale. This is the main
   physical caveat on all four readings.
6. Band definition. This leg takes the band as min/max over the four readings × both F₂ values, with R3
   including 1/F₂. The dispatch wording ("closure literal with M → c_T/c₂") could also mean R3 without 1/F₂;
   that alternative changes the upper edge from −38.38554633554141 to −39.14689297080844 (recorded).

## 7. Eq. (3) and Eq. (4)

- Eq. (3): ℓ ≈ (16π τ/ε²)(c_T/c_κ)⁴ γξ/F₂ at τ = 10, ε = 1, c_T = 7.68, c_κ = 9.38464586499687,
  F₂ = min = 0.001657360829173931 (q = 0.3): coefficient of γξ = 136027.3099135106 (ℓ = 7.029638007781964e-19 m,
  log₁₀(ℓ/L_prop) = −38.642420738970465). With this leg's own mean transverse speed 7.846621816361291 instead
  of 7.68: 148221.81093728365. Other variants (c_κ at q → 0, F₂ at q = 0.15, own c_T min/max) are listed under
  `eq3_alternatives`.
- Eq. (4): 1/(2γ²) = 4.890756751056831e-24.

## 8. Checks, choices, flags

- Float arithmetic re-done independently with 40-digit `decimal` (separate scratch script, not shipped):
  max relative difference 2.6e-16 over all nine schema outputs.
- C numerics: three independent numerical routes, eight estimates, max deviation 2.2e-9 from 1/(4π).
- "Most favourable" = largest ℓ/L_prop (all values are ≪ 1).
- No dispatch/spec disagreement found for Q-D; the spec has no Q-D section.
- Flag: the AP equation number and exact printed form were not seen first-hand (egress blocked); the
  comparison is with second-hand quotations of the AP three-dimensional result, which agree exactly.
