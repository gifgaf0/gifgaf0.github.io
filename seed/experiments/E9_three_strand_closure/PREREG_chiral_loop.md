# E9 chiral loop pre-registration: does a chiral stiffness hold the twisted ring open?

*Draft for the author, October 31, 2026. Label: Exploration. Written after `REPORT_chiral1d.md` and `NOTE_chiral_term.md` Addendum A, before any loop with the chiral term has been computed. γ is a scanned coefficient: no unit model fixes it yet (`NOTE_chiral_term.md` §6).*

## 0. The question

Route A's twisted ring collapses at every (κ, η) tested (`REPORT_N1_rerun.md`, `REPORT_N1_cells.md`). The question here is whether adding the chiral term γψ*·(D×ψ), with the strands locked to space, gives that ring a finite size. If it does, does the result depend on the sign of γ, as a genuinely chiral mechanism must?

## 1. Model (declared inputs)

E9's energy (`gl3.py`, unchanged) plus the chiral term:

  E = E_gl3[ψ, A] + γ ∫ ψ*·(D × ψ),  D = ∇ − ieA.

- **A5 (locking).** Strand index k = 1, 2, 3 is identified with grid axes x, y, z. Under A5, E9's ring-axis choice is no longer arbitrary: the ring lies in the z = 0 plane, with axis along a cube axis of the locked frame. Other orientations, such as the body diagonal, are out of scope.
- **A6.** One-constant stiffness: E9's isotropic Σ|Dψ_k|², with no extra vector-gradient terms.
- **Fixed parameters.** κ = 2 (e = 1/√12), η = 0.1, h = 0.5, R₀ = 6, open boundaries. All as in Amendment B of `PREREG.md`.
- **Scanned coefficient.** γ ∈ {+0.1, +0.2, +0.3, −0.1, −0.2, −0.3}.
  - All six lie below the smallest 1D vacuum threshold γ_c = 0.3535 (diagonal, A free; `REPORT_chiral1d.md`), so the uniform vacuum is stable for every value.
  - γ = 0 is the existing result: COLLAPSE (`REPORT_N1_rerun.md`). It is not rerun, except as the regression in §3.

## 2. Lattice form of the term

Use the symmetric covariant difference on gl3's links:

D_jψ(x) = [U_j(x)ψ(x + ĵ) − U_j(x − ĵ)* ψ(x − ĵ)] / (2h), with U_j = exp(−iehA_j) as in `gl3.py`.

With this form, Σ_x ψ*(x)·(ε D ψ) = 2 Re Σ_x Σ ε_ijk ψ_i*(x) U_j(x) ψ_k(x + ĵ)/(2h). It is real by construction and gauge-covariant. On open boundaries the terms that cross the box are dropped.

## 3. Instrument checks (all before any verdict run)

1. **Gradient.** The chiral term's analytic gradient agrees with finite differences (worst relative error ≲ 1e-6; use a 5-point stencil if the gl3-style check is round-off-limited).
2. **Real and gauge-invariant.** Im/Re ≤ 1e-12 on random states. Invariance under a smooth gauge transformation to round-off.
3. **Parity.** Under a reflection x → −x, with ψ and A mapped as vectors, the chiral energy changes sign to round-off.
4. **Regression.** At γ = 0 the new code reproduces `trace_N1_B_N65_R6.json` exactly at every recorded iteration up to iteration 40: the same E, the same segment counts, the same Lk.
5. **Vacuum stability in the box, C0.** At γ = ±0.3, the uniform vacuum plus noise of amplitude 0.05 (fixed seed) relaxes back to the vacuum. Final E above vacuum ≤ 1e-5, no vortex segments. If C0 fails, that γ is dropped and recorded.

## 4. Runs

Grid 65³. Starts A (Hopf-linked) and B (helix) from `starts.py`, unchanged.

| run | starts | γ | count |
|---|---|---|---|
| main | A, B | each of the six γ | 12 |
| P1 control | N = 0 ring (`control_N0.py` start at 65³, R₀ = 6) | +0.3 and −0.3 | 2 |
| C0 | vacuum + noise | ±0.3 | 2 |
| box check | the same start and γ at 81³ | only for a run that does not collapse at 65³ | as needed |

**Instrument.** `trace_N1_chiral.py`, a copy of `trace_N1.py` that uses the new energy and adds the diagnostics below. It records every 2 iterations, with maxiter 4000. The report shows its diff from `trace_N1.py`.

**Additional diagnostics, per record:**
- The energy split: gradient, magnetic, potential + Josephson above vacuum (E_V), and chiral (E_χ). Separately, the A·S part of E_χ.
- ⟨|S|/|ψ|²⟩, weighted by |∇ψ|², and the chiral energy density integrated within distance 3 of strand 1's line.
- **The scaling (virial) residual.** Under x → λx (with A → A/λ), the pieces scale as follows:

  | piece | scales as |
  |---|---|
  | E_grad | λ |
  | E_mag | λ⁻¹ |
  | E_χ | λ² |
  | E_V | λ³ |

  So at any true stationary point E_grad − E_mag + 2E_χ + 3E_V = 0. Record the residual divided by (E_grad + E_mag + 2|E_χ| + 3E_V).

## 5. Predictions and outcome map (written now)

| | Prediction | Outcome |
|---|---|---|
| P0 | Instrument checks 1–5 pass. | Must hold, or stop. |
| P1 | The N = 0 ring collapses at γ = ±0.3. The composite ring has ψ ∝ (1,1,1) real, so S = 0 and almost no chiral coupling. | Control. Must hold, or stop that γ. |
| P2 (per run) | The free relaxation stops at R* > 2ξ (1.41) with \|Lk(strand 1, composite)\| = 1, and the 81³ box check agrees within 10 %. The virial residual is < 0.10. | **STABLE** |
| | The ring shrinks to core scale, or strand 1 unlinks (merge or reconnection, mechanism named as in `REPORT_N1_rerun.md`). | **COLLAPSE** |
| | A finite stop with a virial residual ≥ 0.10, or a stop at R* ≤ 2ξ. | **MARGINAL** (resolution-limited) |
| | The ring grows to the box. | **EXPANDS** (inconclusive) |

**The parity classification.** This is the headline. It is applied per (start, |γ|):

| +γ | −γ | classification |
|---|---|---|
| STABLE | COLLAPSE (or vice versa) | **CHIRAL-STABLE: handedness-selected closure.** The sign that holds is recorded with the start's twist sense. |
| STABLE | STABLE | **STABLE, parity-even.** The stabilization is not the linear chiral effect. Flag it, and compare E and R* between the signs. |
| COLLAPSE | COLLAPSE | **COLLAPSE.** Record whether collapse at the favourable sign is delayed (more iterations, or a plateau in E) compared with the unfavourable sign and with γ = 0. Descriptive only. |

**P3 (descriptive).** At every γ ≠ 0, ±γ runs that collapse still show different trajectories: E at matched iterations differs by more than 1 %. If they don't, the chiral term is not acting on the twisted texture at all.

**My prior, stated honestly.**
- Any STABLE: about 15 %.
- CHIRAL-STABLE: about 10 %.
- P3 different trajectories: about 70 %.

The 1D result says the chiral gain comes from a static 120° offset carrying a current aligned with S, not from winding. A twisted ring's texture may produce that locally, but nothing shows the gain is enough below γ_c. **The vacuum's stiffness, the very thing that keeps |γ| ≤ 0.3 safe, also limits the gain.** COLLAPSE everywhere is the most likely outcome.

## 6. Eddington guard

- **Fixed:** κ, η, h, R₀, the starts and the ring orientation. They are not re-tuned.
- **γ:** only the six values above. No γ between or beyond them is tried after seeing results. A finer scan, another ring orientation, or η ≠ 0.1 is a new pre-registration.
- **What a CHIRAL-STABLE result would show.** That the locked three-strand medium with this chiral coefficient supports a handedness-selected twisted closure. **It would not derive γ,** which needs the unit model of `NOTE_chiral_term.md` §6.
- No particle identification. The selected handedness is not to be read as any physical parity violation.

## 7. Prior art to verify before interpreting (all [memory] until checked)

- Bogdanov and Yablonskii (1989): chiral skyrmions stabilized by a Dzyaloshinskii–Moriya term.
- Sutcliffe, PRL 118, 247203 (2017): skyrmion knots (hopfions) in frustrated chiral magnets.
- Tai and Smalyukh, PRL 121, 187201 (2018): static Hopf solitons in noncentrosymmetric magnets.
- Ackerman and Smalyukh, PRX 7, 011006 (2017): hopfions and torons in chiral liquid crystals.
- Kaur, Agterberg and Sigrist, PRL 94, 137002 (2005): helical phases from Lifshitz invariants in noncentrosymmetric superconductors.
- Garaud, Carlström and Babaev, PRL 107, 197001 (2011): the 120° frustrated three-band state.

## 8. Cost

At γ = 0 each collapsing 65³ run took about 2 minutes. The chiral term adds roughly 30–50 % per evaluation. That is about 16 runs plus box checks: under an hour of compute on 4 cores, unless something stops.
