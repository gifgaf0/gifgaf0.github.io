import PrimeCubeMurmurations.Limit

/-!
# The rate `O(κ²)` in Theorem A

Theorem A of the cube paper says that the finite-`K` main term
`(2ζ(2)Ĥ₀(0))⁻¹ Σ_t f₃(t) J_K(t)/J(0)` differs from the limit `Λ₃ = (2ζ(2))⁻¹ Σ_t f₃(t) J(t)/J(0)`
by `O(κ²)`. `Limit.lean` proves only the convergence (it uses `|J_K(t) − Ĥ₀(0)J(t)| ≤ Cκ|t|`).
This file proves the rate.

Proof. By `JK_eq_avg` (Fubini),
`J_K(t) − Ĥ₀(0)J(t) = ∫ H₀(v) · ½[J(t + h) + J(t − h) − 2J(t)] dv`, `h = tκv/2π`.
`J = 𝓕ψ₃` is a Schwartz function, so `|J''(u)| ≤ C₂/(1 + u²)²` (`Jdd_decay`). A symmetric second
difference is at most `2 sup|J''| h²` (`sym_diff_le`, two applications of the mean value theorem).
On the support of `H₀`, `|v| ≤ 1`, so for `|κ| ≤ π` the points `t ± h` lie within `|t|/2` of `t`,
where `1 + u² ≥ (1 + t²)/4`. Hence `|J_K(t) − Ĥ₀(0)J(t)| ≤ D κ²/(1 + t²)` (`JK_sub_sq`), and summing
against `|f₃(t)| ≤ C₀` gives the rate (`mainTerm_rate`, `theoremA_rate`).

STATUS: compiled against Mathlib `64fa0ec` (Lean v4.36.0-rc1); every theorem depends only on
`propext`, `Classical.choice`, `Quot.sound`.
-/

open scoped ContDiff Topology SchwartzMap FourierTransform
open Finset MeasureTheory Filter

namespace CubeMurmurations

set_option linter.unusedSectionVars false
set_option linter.deprecated false

/-! ## A symmetric second difference -/

/-- `‖f(w + h) + f(w − h) − 2f(w)‖ ≤ 2 M h²` if `‖f''‖ ≤ M` on `[w − |h|, w + |h|]`. -/
lemma sym_diff_le (f : ℝ → ℂ) (hf : Differentiable ℝ f) (hf' : Differentiable ℝ (deriv f))
    (w h M : ℝ) (hM : ∀ u ∈ Set.Icc (w - |h|) (w + |h|), ‖deriv (deriv f) u‖ ≤ M) :
    ‖f (w + h) + f (w - h) - 2 * f w‖ ≤ 2 * M * h ^ 2 := by
  have hM0 : 0 ≤ M := (norm_nonneg _).trans (hM w ⟨by linarith [abs_nonneg h], by linarith [abs_nonneg h]⟩)
  -- `g(s) = f(w + s) + f(w − s) − 2 f(w)`, `g(0) = 0`, `g'(s) = f'(w + s) − f'(w − s)`
  set g : ℝ → ℂ := fun s => f (w + s) + f (w - s) - 2 * f w with hg
  have hgd : ∀ s, HasDerivAt g (deriv f (w + s) - deriv f (w - s)) s := by
    intro s
    have h1 : HasDerivAt (fun s => f (w + s)) (deriv f (w + s)) s := by
      have := (hf (w + s)).hasDerivAt.scomp s ((hasDerivAt_id' (x := s)).const_add w)
      simpa [Function.comp_def] using this
    have h2 : HasDerivAt (fun s => f (w - s)) (-deriv f (w - s)) s := by
      have := (hf (w - s)).hasDerivAt.scomp s ((hasDerivAt_id' (x := s)).const_sub w)
      simpa [Function.comp_def] using this
    have := (h1.add h2).sub_const (2 * f w)
    simpa [g, sub_eq_add_neg] using this
  -- `‖g'(s)‖ ≤ 2 M |h|` for `s` between `0` and `h`
  have hgb : ∀ s ∈ Set.uIcc 0 h, ‖deriv g s‖ ≤ 2 * M * |h| := by
    intro s hs
    rw [(hgd s).deriv]
    have hs' : |s| ≤ |h| := by
      rcases le_total 0 h with h0 | h0
      · rw [Set.uIcc_of_le h0] at hs
        rw [abs_of_nonneg hs.1, abs_of_nonneg h0]; exact hs.2
      · rw [Set.uIcc_of_ge h0] at hs
        rw [abs_of_nonpos hs.2, abs_of_nonpos h0]; linarith [hs.1]
    -- mean value theorem for `f'` on the segment between `w − s` and `w + s`
    have hsub : Set.uIcc (w - s) (w + s) ⊆ Set.Icc (w - |h|) (w + |h|) := by
      intro u hu
      have := Set.mem_uIcc.mp hu
      constructor <;> rcases this with ⟨h1, h2⟩ | ⟨h1, h2⟩ <;>
        linarith [abs_le.mp hs', neg_abs_le s, le_abs_self s]
    have mvt := (convex_uIcc (w - s) (w + s)).norm_image_sub_le_of_norm_deriv_le
      (f := deriv f) (C := M) (fun u _ => hf' u) (fun u hu => hM u (hsub hu))
      Set.left_mem_uIcc Set.right_mem_uIcc
    calc ‖deriv f (w + s) - deriv f (w - s)‖ ≤ M * ‖(w + s) - (w - s)‖ := mvt
      _ = M * (2 * |s|) := by rw [Real.norm_eq_abs]; congr 1; rw [show w + s - (w - s) = 2 * s by ring,
            abs_mul, abs_two]
      _ ≤ 2 * M * |h| := by nlinarith
  -- mean value theorem for `g` on the segment between `0` and `h`
  have mvt := (convex_uIcc (0 : ℝ) h).norm_image_sub_le_of_norm_deriv_le
    (f := g) (C := 2 * M * |h|) (fun s _ => (hgd s).differentiableAt) hgb
    Set.left_mem_uIcc Set.right_mem_uIcc
  have hg0 : g 0 = 0 := by simp [g]; ring
  rw [hg0, sub_zero, sub_zero, Real.norm_eq_abs] at mvt
  calc ‖f (w + h) + f (w - h) - 2 * f w‖ = ‖g h‖ := rfl
    _ ≤ 2 * M * |h| * |h| := mvt
    _ = 2 * M * h ^ 2 := by rw [mul_assoc, ← sq, sq_abs]

/-! ## Decay of `J''` -/

section Decay

variable {Φ : ℝ → ℝ} {a b : ℝ} (hΦ : ContDiff ℝ ∞ Φ) (ha : 0 < a)
  (hΦs : ∀ y, Φ y ≠ 0 → a ≤ y ∧ y ≤ b)

/-- `J = 𝓕ψ₃` as a Schwartz function. -/
noncomputable abbrev JS : 𝓢(ℝ, ℂ) := 𝓕 (psi3S hΦ ha hΦs)

lemma deriv_JS : deriv (JS hΦ ha hΦs : ℝ → ℂ) = (SchwartzMap.derivCLM ℝ ℂ (JS hΦ ha hΦs) : ℝ → ℂ) := by
  funext u; rw [SchwartzMap.derivCLM_apply]

lemma deriv_deriv_JS : deriv (deriv (JS hΦ ha hΦs : ℝ → ℂ)) =
    (SchwartzMap.derivCLM ℝ ℂ (SchwartzMap.derivCLM ℝ ℂ (JS hΦ ha hΦs)) : ℝ → ℂ) := by
  rw [deriv_JS]; funext u; rw [SchwartzMap.derivCLM_apply]

/-- **Decay of `J''`**: `‖J''(u)‖ ≤ C₂/(1 + u²)²`. -/
lemma Jdd_decay : ∃ C2 : ℝ, 0 ≤ C2 ∧ ∀ u : ℝ,
    ‖deriv (deriv (JS hΦ ha hΦs : ℝ → ℂ)) u‖ ≤ C2 / (1 + u ^ 2) ^ 2 := by
  set F2 := SchwartzMap.derivCLM ℝ ℂ (SchwartzMap.derivCLM ℝ ℂ (JS hΦ ha hΦs))
  set S0 := SchwartzMap.seminorm ℝ 0 0 F2
  set S4 := SchwartzMap.seminorm ℝ 4 0 F2
  refine ⟨2 * (S0 + S4), by positivity, fun u => ?_⟩
  rw [deriv_deriv_JS]
  have h0 := SchwartzMap.norm_le_seminorm ℝ F2 u
  have h4 := SchwartzMap.norm_pow_mul_le_seminorm ℝ F2 4 u
  rw [Real.norm_eq_abs, show |u| ^ 4 = (u ^ 2) ^ 2 by rw [← sq_abs u]; ring] at h4
  -- `(1 + u²)² ≤ 2 (1 + u⁴)`
  have hq : (1 + u ^ 2) ^ 2 ≤ 2 * (1 + (u ^ 2) ^ 2) := by nlinarith [sq_nonneg (u ^ 2 - 1)]
  rw [le_div_iff₀ (by positivity)]
  have hn := norm_nonneg (F2 u)
  nlinarith [mul_le_mul_of_nonneg_left hq hn]

end Decay

/-! ## `|J_K(t) − Ĥ₀(0)J(t)| ≤ D κ²/(1 + t²)` -/

section JKsq

variable {Φ : ℝ → ℝ} (hΦ : ContDiff ℝ ∞ Φ) {a b : ℝ} (ha : 0 < a) (hab : a ≤ b)
  (hΦs : ∀ y, Φ y ≠ 0 → a ≤ y ∧ y ≤ b)
  {H0 : ℝ → ℝ} (hG : IsBump H0) (heven : ∀ v, H0 (-v) = H0 v)

include hΦ ha hab hΦs in
/-- The second difference of `J` near `t`: for `|s| ≤ 1/2`,
`|J(t(1+s)) + J(t(1−s)) − 2J(t)| ≤ 32 C₂ s² t²/(1 + t²)²`. -/
lemma J1_sym_diff (C2 : ℝ) (hC2 : 0 ≤ C2)
    (hdd : ∀ u : ℝ, ‖deriv (deriv (JS hΦ ha hΦs : ℝ → ℂ)) u‖ ≤ C2 / (1 + u ^ 2) ^ 2)
    (t s : ℝ) (hs : |s| ≤ 1 / 2) :
    |J1 Φ a b (t * (1 + s)) + J1 Φ a b (t * (1 - s)) - 2 * J1 Φ a b t| ≤
      32 * C2 * s ^ 2 * t ^ 2 / (1 + t ^ 2) ^ 2 := by
  set F : ℝ → ℂ := (JS hΦ ha hΦs : ℝ → ℂ)
  have hFJ : ∀ w, F w = (J1 Φ a b w : ℂ) := fun w => by
    simp only [F, JS]; rw [fourier_psi3S, Jphi_eq_J1 ha hab hΦs]
  set h := t * s
  have hMb : ∀ u ∈ Set.Icc (t - |h|) (t + |h|), ‖deriv (deriv F) u‖ ≤ 16 * C2 / (1 + t ^ 2) ^ 2 := by
    intro u hu
    have hh : |h| ≤ |t| / 2 := by
      simp only [h]; rw [abs_mul]; nlinarith [abs_nonneg t]
    -- `|u| ≥ |t|/2`, so `1 + u² ≥ (1 + t²)/4`
    have hu2 : t ^ 2 / 4 ≤ u ^ 2 := by
      have : |t| / 2 ≤ |u| := by
        rcases le_total 0 t with h0 | h0
        · rw [abs_of_nonneg h0] at hh ⊢; rw [abs_of_nonneg (by linarith [hu.1])]; linarith [hu.1]
        · rw [abs_of_nonpos h0] at hh ⊢; rw [abs_of_nonpos (by linarith [hu.2])]; linarith [hu.2]
      have := mul_le_mul this this (by positivity) (abs_nonneg u)
      nlinarith [sq_abs t, sq_abs u]
    have hq : (1 + t ^ 2) / 4 ≤ 1 + u ^ 2 := by linarith
    have hq2 : (1 + t ^ 2) ^ 2 / 16 ≤ (1 + u ^ 2) ^ 2 := by
      have := mul_le_mul hq hq (by positivity) (by positivity); nlinarith
    refine (hdd u).trans ?_
    rw [div_le_div_iff₀ (by positivity) (by positivity)]
    nlinarith [mul_le_mul_of_nonneg_left hq2 hC2]
  have hdiff : Differentiable ℝ F := (JS hΦ ha hΦs).differentiable
  have hdiff' : Differentiable ℝ (deriv F) := by
    rw [deriv_JS]; exact (SchwartzMap.derivCLM ℝ ℂ (JS hΦ ha hΦs)).differentiable
  have key := sym_diff_le F hdiff hdiff' t h _ hMb
  have e1 : t * (1 + s) = t + h := by simp only [h]; ring
  have e2 : t * (1 - s) = t - h := by simp only [h]; ring
  rw [e1, e2]
  have hn : ‖F (t + h) + F (t - h) - 2 * F t‖ =
      |J1 Φ a b (t + h) + J1 Φ a b (t - h) - 2 * J1 Φ a b t| := by
    rw [hFJ, hFJ, hFJ, ← Real.norm_eq_abs, ← Complex.norm_real]; congr 1; push_cast; ring
  rw [← hn]
  refine key.trans (le_of_eq ?_)
  simp only [h]; ring

include hΦ ha hab hΦs hG heven in
/-- **The rate, pointwise**: for `|κ| ≤ π`, `|J_K(t) − Ĥ₀(0)J(t)| ≤ D κ²/(1 + t²)`. -/
theorem JK_sub_sq : ∃ D : ℝ, 0 ≤ D ∧ ∀ κ : ℝ, |κ| ≤ Real.pi → ∀ t : ℤ,
    |JK Φ H0 a b κ t - (∫ v, H0 v) * J1 Φ a b t| ≤ D * κ ^ 2 / (1 + (t : ℝ) ^ 2) := by
  obtain ⟨C2, hC2, hdd⟩ := Jdd_decay hΦ ha hΦs
  set IH := ∫ v, |H0 v|
  have hIH : 0 ≤ IH := integral_nonneg (fun _ => abs_nonneg _)
  have hpi := Real.pi_pos
  refine ⟨4 * C2 / Real.pi ^ 2 * IH, by positivity, fun κ hκ t => ?_⟩
  -- `J_K(t) − Ĥ₀(0)J(t) = ∫ H₀(v)(½[J(t(1+s)) + J(t(1−s))] − J(t)) dv`, `s = κv/2π`
  set avg : ℝ → ℝ := fun v => (J1 Φ a b ((t : ℝ) * (1 + κ * v / (2 * Real.pi))) +
      J1 Φ a b ((t : ℝ) * (1 - κ * v / (2 * Real.pi)))) / 2
  have hcont : Continuous (fun w => J1 Φ a b w) := by
    have : (fun w => J1 Φ a b w) = fun w => (JS hΦ ha hΦs w).re := by
      funext w; simp only [JS]; rw [fourier_psi3S, Jphi_eq_J1 ha hab hΦs, Complex.ofReal_re]
    rw [this]; exact Complex.continuous_re.comp (JS hΦ ha hΦs).continuous
  have hI1 : Integrable (fun v => H0 v * avg v) := by
    refine (hG.1.continuous.mul (by simp only [avg]; fun_prop)).integrable_of_hasCompactSupport
      (bump_hasCompactSupport hG).mul_right
  have hI2 : Integrable (fun v => H0 v * J1 Φ a b t) := (integrable_bump hG).mul_const _
  have e : JK Φ H0 a b κ t - (∫ v, H0 v) * J1 Φ a b t =
      ∫ v, H0 v * (avg v - J1 Φ a b t) := by
    rw [JK_eq_avg hΦ.continuous ha hab hG heven κ t, ← integral_mul_const, ← integral_sub hI1 hI2]
    refine integral_congr_ae (Eventually.of_forall (fun v => ?_))
    simp only [avg]; ring
  rw [e]
  -- pointwise bound on the support of `H₀`
  have hpt : ∀ v, ‖H0 v * (avg v - J1 Φ a b t)‖ ≤
      |H0 v| * (4 * C2 / Real.pi ^ 2 * κ ^ 2 / (1 + (t : ℝ) ^ 2)) := by
    intro v
    rw [Real.norm_eq_abs, abs_mul]
    by_cases hv : H0 v = 0
    · rw [hv, abs_zero, zero_mul, zero_mul]
    apply mul_le_mul_of_nonneg_left _ (abs_nonneg _)
    have hv1 := hG.2 v hv
    set s := κ * v / (2 * Real.pi)
    have hs : |s| ≤ 1 / 2 := by
      simp only [s]
      rw [abs_div, abs_mul, abs_of_pos (by positivity : (0 : ℝ) < 2 * Real.pi),
        div_le_iff₀ (by positivity)]
      nlinarith [abs_nonneg κ, abs_nonneg v]
    have hs2 : s ^ 2 ≤ κ ^ 2 / (4 * Real.pi ^ 2) := by
      simp only [s]
      rw [div_pow, mul_pow, mul_pow, div_le_div_iff₀ (by positivity) (by positivity)]
      have : v ^ 2 ≤ 1 := by nlinarith [sq_abs v, abs_nonneg v]
      nlinarith [mul_le_mul_of_nonneg_left this (by positivity : (0 : ℝ) ≤ κ ^ 2 * (4 * Real.pi ^ 2))]
    have hd := J1_sym_diff hΦ ha hab hΦs C2 hC2 hdd t s hs
    have e2 : avg v - J1 Φ a b t =
        (J1 Φ a b ((t : ℝ) * (1 + s)) + J1 Φ a b ((t : ℝ) * (1 - s)) - 2 * J1 Φ a b t) / 2 := by
      simp only [avg, s]; ring
    rw [e2, abs_div, abs_two]
    have ht : (t : ℝ) ^ 2 / (1 + (t : ℝ) ^ 2) ≤ 1 := by
      rw [div_le_one (by positivity)]; linarith
    calc _ ≤ 32 * C2 * s ^ 2 * (t : ℝ) ^ 2 / (1 + (t : ℝ) ^ 2) ^ 2 / 2 := by gcongr
      _ = 16 * C2 * s ^ 2 * ((t : ℝ) ^ 2 / (1 + (t : ℝ) ^ 2)) / (1 + (t : ℝ) ^ 2) := by
          field_simp; ring
      _ ≤ 16 * C2 * (κ ^ 2 / (4 * Real.pi ^ 2)) * 1 / (1 + (t : ℝ) ^ 2) := by gcongr
      _ = 4 * C2 / Real.pi ^ 2 * κ ^ 2 / (1 + (t : ℝ) ^ 2) := by field_simp; ring
  have hgi : Integrable (fun v => |H0 v| * (4 * C2 / Real.pi ^ 2 * κ ^ 2 / (1 + (t : ℝ) ^ 2))) :=
    (integrable_bump hG).abs.mul_const _
  have := norm_integral_le_of_norm_le hgi (Eventually.of_forall hpt)
  rw [Real.norm_eq_abs, integral_mul_const] at this
  refine this.trans (le_of_eq ?_)
  simp only [IH]; ring

end JKsq

/-! ## The rate for the main term -/

set_option maxHeartbeats 1000000 in
/-- **The rate `O(κ²)`**: for `|κ| ≤ π`,
`|Σ_t f₃(t) J_K(t) − Ĥ₀(0) Σ_t f₃(t) J(t)| ≤ C κ²`. -/
theorem mainTerm_rate {Φ : ℝ → ℝ} (hΦ : ContDiff ℝ ∞ Φ) {a b : ℝ} (ha : 0 < a) (hab : a ≤ b)
    (hΦs : ∀ y, Φ y ≠ 0 → a ≤ y ∧ y ≤ b)
    {H0 : ℝ → ℝ} (hG : IsBump H0) (heven : ∀ v, H0 (-v) = H0 v) :
    ∃ C : ℝ, 0 ≤ C ∧ ∀ κ : ℝ, |κ| ≤ Real.pi →
      ‖∑' t : ℤ, f3 t * (JK Φ H0 a b κ t : ℂ) -
        ((∫ v, H0 v : ℝ) : ℂ) * ∑' t : ℤ, f3 t * (Jphi Φ t : ℂ)‖ ≤ C * κ ^ 2 := by
  obtain ⟨D, hD, hJK⟩ := JK_sub_sq hΦ ha hab hΦs hG heven
  obtain ⟨CK, hCK, hdec⟩ := JK_decay hΦ.continuous ha hab hG heven hΦ hΦs
  obtain ⟨CJ, hCJ, hJdec⟩ := Jphi_decay ha hΦs hΦ
  have hC0 : 0 ≤ C0 := le_trans (norm_nonneg _) (norm_f3_le 0)
  set S := ∑' t : ℤ, 1 / (1 + (t : ℝ) ^ 2)
  have hS : 0 ≤ S := tsum_nonneg (fun t => by positivity)
  refine ⟨C0 * D * S, by positivity, fun κ hκ => ?_⟩
  set I0 : ℝ := ∫ v, H0 v
  -- summability of both series
  have hs1 : Summable (fun t : ℤ => f3 t * (JK Φ H0 a b κ t : ℂ)) := by
    refine Summable.of_norm_bounded (summable_inv_one_add_sq.mul_left (C0 * CK)) (fun t => ?_)
    rw [norm_mul, Complex.norm_real, Real.norm_eq_abs]
    calc _ ≤ C0 * (CK / (1 + (t : ℝ) ^ 2)) :=
          mul_le_mul (norm_f3_le t) (hdec κ hκ t) (abs_nonneg _) hC0
      _ = _ := by ring
  have hs2 : Summable (fun t : ℤ => f3 t * (Jphi Φ t : ℂ)) := by
    refine Summable.of_norm_bounded (summable_inv_one_add_sq.mul_left (C0 * CJ)) (fun t => ?_)
    rw [norm_mul, Complex.norm_real, Real.norm_eq_abs]
    calc _ ≤ C0 * (CJ / (1 + (t : ℝ) ^ 2)) :=
          mul_le_mul (norm_f3_le t) (hJdec t) (abs_nonneg _) hC0
      _ = _ := by ring
  rw [← tsum_mul_left, ← hs1.tsum_sub (hs2.mul_left _)]
  have hb : ∀ t : ℤ, ‖f3 t * (JK Φ H0 a b κ t : ℂ) - (I0 : ℂ) * (f3 t * (Jphi Φ t : ℂ))‖ ≤
      C0 * D * κ ^ 2 * (1 / (1 + (t : ℝ) ^ 2)) := by
    intro t
    have e : f3 t * (JK Φ H0 a b κ t : ℂ) - (I0 : ℂ) * (f3 t * (Jphi Φ t : ℂ)) =
        f3 t * ((JK Φ H0 a b κ t - I0 * J1 Φ a b t : ℝ) : ℂ) := by
      rw [Jphi_eq_J1 ha hab hΦs]; push_cast; ring
    rw [e, norm_mul, Complex.norm_real, Real.norm_eq_abs]
    calc _ ≤ C0 * (D * κ ^ 2 / (1 + (t : ℝ) ^ 2)) :=
          mul_le_mul (norm_f3_le t) (hJK κ hκ t) (abs_nonneg _) hC0
      _ = _ := by ring
  have hsum : HasSum (fun t : ℤ => C0 * D * κ ^ 2 * (1 / (1 + (t : ℝ) ^ 2))) (C0 * D * κ ^ 2 * S) :=
    summable_inv_one_add_sq.hasSum.mul_left _
  refine (tsum_of_norm_bounded hsum hb).trans (le_of_eq ?_)
  ring

/-- **Theorem A, the rate**: the finite-`K` main term `(2ζ(2)Ĥ₀(0))⁻¹ Σ_t f₃(t) J_K(t)/J(0)`
differs from `Λ₃ = (2ζ(2))⁻¹ Σ_t f₃(t) J(t)/J(0)` by at most `C κ²` for `|κ| ≤ π`. With
`κ = κK θ K = 2πK^θ/(K − 1)` this is `O(K^{−2(1−θ)})`. -/
theorem theoremA_rate {Φ : ℝ → ℝ} (hΦ : ContDiff ℝ ∞ Φ) {a b : ℝ} (ha : 0 < a) (hab : a ≤ b)
    (hΦs : ∀ y, Φ y ≠ 0 → a ≤ y ∧ y ≤ b) (hJ0 : Jphi Φ 0 ≠ 0)
    {H0 : ℝ → ℝ} (hG : IsBump H0) (heven : ∀ v, H0 (-v) = H0 v) (hI0 : ∫ v, H0 v ≠ 0) :
    ∃ C : ℝ, 0 ≤ C ∧ ∀ κ : ℝ, |κ| ≤ Real.pi →
      ‖(3 / (Real.pi ^ 2 * (∫ v, H0 v)) : ℂ) * ∑' t : ℤ, f3 t * (JK Φ H0 a b κ t : ℂ) / (Jphi Φ 0 : ℂ) -
        (3 / Real.pi ^ 2 : ℂ) * ∑' t : ℤ, f3 t * (Jphi Φ t : ℂ) / (Jphi Φ 0 : ℂ)‖ ≤ C * κ ^ 2 := by
  obtain ⟨C, hC, hrate⟩ := mainTerm_rate hΦ ha hab hΦs hG heven
  set I0 : ℝ := ∫ v, H0 v
  set Jz : ℝ := Jphi Φ 0
  have hpi : (Real.pi : ℂ) ≠ 0 := Complex.ofReal_ne_zero.mpr Real.pi_ne_zero
  have hI : (I0 : ℂ) ≠ 0 := Complex.ofReal_ne_zero.mpr hI0
  have hJ : (Jz : ℂ) ≠ 0 := Complex.ofReal_ne_zero.mpr hJ0
  refine ⟨3 / (Real.pi ^ 2 * |I0| * |Jz|) * C, by positivity, fun κ hκ => ?_⟩
  have e : (3 / (Real.pi ^ 2 * I0) : ℂ) * ∑' t : ℤ, f3 t * (JK Φ H0 a b κ t : ℂ) / (Jz : ℂ) -
      (3 / Real.pi ^ 2 : ℂ) * ∑' t : ℤ, f3 t * (Jphi Φ t : ℂ) / (Jz : ℂ) =
      (3 / (Real.pi ^ 2 * I0 * Jz) : ℂ) * (∑' t : ℤ, f3 t * (JK Φ H0 a b κ t : ℂ) -
        (I0 : ℂ) * ∑' t : ℤ, f3 t * (Jphi Φ t : ℂ)) := by
    rw [tsum_div_const, tsum_div_const]
    field_simp
  rw [e, norm_mul]
  have hn : ‖(3 / ((Real.pi : ℂ) ^ 2 * I0 * Jz))‖ = 3 / (Real.pi ^ 2 * |I0| * |Jz|) := by
    rw [norm_div, norm_mul, norm_mul, norm_pow, Complex.norm_real, Complex.norm_real,
      Complex.norm_real, Real.norm_eq_abs, Real.norm_eq_abs, Real.norm_eq_abs,
      abs_of_pos Real.pi_pos]
    norm_num
  rw [hn]
  refine (mul_le_mul_of_nonneg_left (hrate κ hκ) (by positivity)).trans (le_of_eq (by ring))

end CubeMurmurations
