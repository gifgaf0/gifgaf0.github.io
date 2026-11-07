/-!
# Entry 025: the 2-adic facts for y² = x³ − x

Classical input (Gauss's last diary entry; Herglotz 1921; Ireland–Rosen, Ch. 18, Thm. 5;
Ruíz Duarte, arXiv:1710.04887, Cor. 2.8): for a prime p ≡ 1 (mod 4),
  #E(𝔽_p) = p + 1 − 2α,  where p = α² + β²,
with α ≡ 1 (mod 4) if p ≡ 1 (mod 8) and α ≡ 3 (mod 4) if p ≡ 5 (mod 8).

This file does NOT formalize that theorem. It proves, from it, the two facts used in Entry 025:
  p ≡ 1 (mod 8)  ⇒  16 ∣ #E(𝔽_p)
  p ≡ 5 (mod 8)  ⇒  #E(𝔽_p) ≡ 8 (mod 16)    (so #E/8 is odd)
Core Lean 4 only; no Mathlib.
-/

/-- Reduce a quadratic expression in α, β modulo m ∣ 16 to the residues of α, β mod 16. -/
private theorem reduce16 (α β : Int) :
    ∃ r t q s : Int, α = r + 16 * q ∧ β = t + 16 * s ∧ 0 ≤ r ∧ r < 16 ∧ 0 ≤ t ∧ t < 16 := by
  refine ⟨α % 16, β % 16, α / 16, β / 16, ?_, ?_, ?_, ?_, ?_, ?_⟩
  · have := Int.emod_add_ediv α 16; omega
  · have := Int.emod_add_ediv β 16; omega
  · exact Int.emod_nonneg _ (by decide)
  · exact Int.emod_lt_of_pos _ (by decide)
  · exact Int.emod_nonneg _ (by decide)
  · exact Int.emod_lt_of_pos _ (by decide)

/-- The polynomial identity behind the reduction (checked by `grind`'s ring normalizer). -/
private theorem expand (r t q s : Int) :
    (r + 16*q)*(r + 16*q) + (t + 16*s)*(t + 16*s)
      = (r*r + t*t) + 16 * (2*q*r + 16*q*q + 2*s*t + 16*s*s) := by
  grind

private theorem core (r t : Int) (hr0 : 0 ≤ r) (hr : r < 16) (ht0 : 0 ≤ t) (ht : t < 16) :
    ((r % 4 = 1 ∧ (r*r + t*t) % 8 = 1) → (r*r + t*t + 1 - 2*r) % 16 = 0) ∧
    ((r % 4 = 3 ∧ (r*r + t*t) % 8 = 5) → (r*r + t*t + 1 - 2*r) % 16 = 8) := by
  have hr' : r = 0 ∨ r = 1 ∨ r = 2 ∨ r = 3 ∨ r = 4 ∨ r = 5 ∨ r = 6 ∨ r = 7 ∨ r = 8 ∨ r = 9 ∨
      r = 10 ∨ r = 11 ∨ r = 12 ∨ r = 13 ∨ r = 14 ∨ r = 15 := by omega
  have ht' : t = 0 ∨ t = 1 ∨ t = 2 ∨ t = 3 ∨ t = 4 ∨ t = 5 ∨ t = 6 ∨ t = 7 ∨ t = 8 ∨ t = 9 ∨
      t = 10 ∨ t = 11 ∨ t = 12 ∨ t = 13 ∨ t = 14 ∨ t = 15 := by omega
  rcases hr' with h|h|h|h|h|h|h|h|h|h|h|h|h|h|h|h <;>
  rcases ht' with k|k|k|k|k|k|k|k|k|k|k|k|k|k|k|k <;>
  (subst h; subst k; decide)

/-- p ≡ 1 (mod 8), α ≡ 1 (mod 4): 16 divides p + 1 − 2α. -/
theorem split_one_mod_eight (α β : Int) (hα : α % 4 = 1) (hp : (α*α + β*β) % 8 = 1) :
    (α*α + β*β + 1 - 2*α) % 16 = 0 := by
  obtain ⟨r, t, q, s, rfl, rfl, hr0, hr, ht0, ht⟩ := reduce16 α β
  have hx := expand r t q s
  have hα' : r % 4 = 1 := by omega
  have hp' : (r*r + t*t) % 8 = 1 := by omega
  have := (core r t hr0 hr ht0 ht).1 ⟨hα', hp'⟩
  omega

/-- p ≡ 5 (mod 8), α ≡ 3 (mod 4): p + 1 − 2α ≡ 8 (mod 16), i.e. #E/8 is odd. -/
theorem split_five_mod_eight (α β : Int) (hα : α % 4 = 3) (hp : (α*α + β*β) % 8 = 5) :
    (α*α + β*β + 1 - 2*α) % 16 = 8 := by
  obtain ⟨r, t, q, s, rfl, rfl, hr0, hr, ht0, ht⟩ := reduce16 α β
  have hx := expand r t q s
  have hα' : r % 4 = 3 := by omega
  have hp' : (r*r + t*t) % 8 = 5 := by omega
  have := (core r t hr0 hr ht0 ht).2 ⟨hα', hp'⟩
  omega

#print axioms split_one_mod_eight
#print axioms split_five_mod_eight

/-! Non-vacuity: p = 17 = 1² + 4² (α = 1, #E = 16) and p = 37 = (−1)² + 6² (α = −1, #E = 40). -/
example : ((1:Int)*1 + 4*4 + 1 - 2*1) % 16 = 0 := split_one_mod_eight 1 4 (by decide) (by decide)
example : ((-1:Int)*(-1) + 6*6 + 1 - 2*(-1)) % 16 = 8 := split_five_mod_eight (-1) 6 (by decide) (by decide)
