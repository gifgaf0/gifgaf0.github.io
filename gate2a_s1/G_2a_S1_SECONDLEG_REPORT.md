# G-2a-S1 — Independent Second-Leg Verification

**Date:** 2026-06-30 · **Pre-registration:** `G_2a_S1_PREREGISTRATION.md` (Route-1
necessary-condition screen for soliton spin-isospin locking, §2.87.A; ceiling **R2**) ·
**First leg:** `g_2a_s1_screen.py` (chat-side) · **Second leg:** `gate2a_s1_secondleg.py`
(this — from scratch, independent on every axis). The pre-reg requires a CC second leg
before any ledger entry; this is it.

## Result: **CONFIRMS the first leg — PASS-possible (R2); the factor-of-4 quartet is FORCED (D1=1).**

The necessary structural conditions for 2O_spatial → SU(2)_internal locking are met. The
screen **cannot** (and does not claim to) return the dynamical locking fact or settle
Assignment I vs II — M.CW ceiling. It greenlights Routes 2/3.

## Independence (how this leg differs from the first)
| axis | first leg | second leg (this) |
|---|---|---|
| 2O construction | 48 unit quaternions + quaternion ⊗ | **2×2 SU(2) matrices, closed under matrix mult** from 2 generators |
| spin-j characters | 2cos3φ + 2cosφ (cos-sum) | **Chebyshev χ_j = U₂ⱼ(tr/2)** |
| D1 (genuine-irrep count) | asserted dims {2,2,4} | **computed**: #classes(2O), #classes(O=2O/{±I}), counting |
| D2 (color commutant) | their commutant routine | **own [G,X]=0 nullspace solver** |

## What the second leg verified

| NC / scalar | result | status |
|---|---|---|
| **NC1** embedding 2O ↪ SU(2), central → −Id | \|2O\|=48 (matrix closure); −I in group | ✓ |
| **NC2** spin-3/2 = genuine quartet | χ₃/₂(I)=+4, **χ₃/₂(−I)=−4** (FR sign), ⟨3/2,3/2⟩=1 | ✓ |
| FR *selects* fermionic | χ₁(−I)=+3 (bosonic, excluded); χ₁/₂(−I)=−2 (genuine) | ✓ |
| **D1** quartet forcing | #classes(2O)=**8**; \|O\|=**24**, #classes(O)=**5** ⇒ 3 genuine, Σd²=24 ⇒ dims (2,2,4) ⇒ **D1=1** | ✓ **FORCED** |
| **D2** color-transversality | dim_ℂ commutant of SU(3)(3⊕1) in M₄ = **2** (abelian) ⇒ 2O (non-abelian) not hostable in color SU(4) | ✓ |
| transverse arena exists | [color⊗1, 1⊗spin] = 0 (tensor product ℂ⊗𝕆⊗ℍ) | ✓ |

**The D1=1 argument (independent).** From the matrix group: 2O has **8** conjugacy classes
(= 8 irreps); its quotient O = 2O/{±I} (order 24) has **5** classes (= 5 bosonic irreps,
those on which −I acts as +Id). So there are **3 genuine irreps**, with Σd² = 48 − 24 = 24.
Genuine irreps have even dimension (half-integer-spin content, faithful on the center);
three even dims with Σd² = 24, given spin-3/2 is a verified dim-4 genuine irreducible and
spin-1/2 a dim-2 genuine, force the third to be dim-2 → dims (2,2,4). Hence **exactly one
4-dim genuine irrep**: the factor-of-4 quartet is unique. (The binary octahedral character
table is textbook; this is a *confirmatory* screen, not a novel result.)

## What the screen provably cannot do (carried, binding)
- **M.CW ceiling (R2).** Whether the energy-minimizer *realizes* the locking is a
  metric/dynamical fact (which way the minimizer tips) — combinatorics cannot fix it. The
  screen returns only possible / impossible / forced, never "the locking happens."
- **Assignment I vs II** (spin in ℂ⊗ℍ vs ρ₆-ℂ⊗𝕆) is upstream and **not** settled here; both
  adopt the transverse-factor structure and both pass NC1–NC3.
- **NC5 (out of scope — the live obstruction site).** The §2.15 baryon is a 3-strand
  Borromean carrying color-3; a spatial 2O rotation that **permutes the three strands**
  would induce an S₃ ⊂ SU(3)_color action — spatial rotation leaking into color, breaking
  transversality *for the baryon specifically*. Whether it does is **geometry-gated** (where
  the strands sit vs the octahedral axes) — an M.ONT / Routes-2/3 input, not decidable by
  this pure-group screen. **This is the place a genuine obstruction could still live**, and
  the direct motivation for the Route-2 relaxed-core eigenproblem.

## Eddington / discipline
The spin-3/2 / factor-of-4 / μ_n target is the **object screened**, not a fitted parameter;
no continuous parameter is fit; the factor 4 enters only the final interpretation. Pure
group/Lie rep theory — no substrate metric, no GP dynamics, no I1–I3 ticket (so the R2
ceiling is structural). §2.52 Open 3 untouched.

## Standing
**Two-leg verified** (chat-side first leg + this independent from-scratch second leg). Per
the pre-registration, the gate is now eligible for a ledger entry at **R2 (admissibility):
PASS-possible, factor-of-4 quartet FORCED (D1=1)**, with the M.CW ceiling and the NC5
out-of-scope obstruction-site flag traveling with it. Routes 2/3 (the dynamical locking and
Assignment I/II) remain the open content. Fold is the SQT/author's to run into canonical.
