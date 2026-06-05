# §3.4-G2-Milnor-SIGN — Pre-Registration (conventions + criteria, committed before computing)

**Date:** 2026-06-05
**Status:** PRE-REGISTRATION. Written and committed **before** any sign is
computed, so the criteria below — not a post-hoc match — decide the result.
**Scope:** this attempts the rigorous *topological* **sign(μ̄)** of the baryon
Milnor triple-linking, the open authority of §3.4-G2-Milnor-INT. Success would
promote the reflection-odd handedness *witness* of `g2_milnor.py` to the genuine
invariant. It does **NOT** touch the registered substantive map sign(φ)↔QR/QNR
(still R3-pending its §2.75/§2.76/§2.86C consistency check).
**Eddington watch:** ACTIVE — every clean-looking sign so far (det[normals]; the
naive solid-angle integral) was **reflection-even**; a wrong "clean ±1" is the
hazard. No result is faked; the controls decide.

## §1 — Conventions (fixed now)

- **Curves / orientation / ordering:** the three golden ellipses of `g2_milnor.py`
  (E₁ in z=0, E₂ in x=0, E₃ in y-plane), parametrised as given; component
  ordering (1,2,3); a spatial mirror is z→−z applied to positions with the
  parametrisation direction kept.
- **Seifert surfaces:** the flat elliptical disks bounded by each curve.
- **Method A — Seifert-intersection linking.** γ₁₂ := (the segment F₁∩F₂, the
  clip of the two disk-planes' intersection line to both disks) ∪ (an arc of C₁
  closing its endpoints). Then **μ̄_A := lk(C₃, γ₁₂)** by the Gauss integral. The
  arc choice is immaterial because the two arcs differ by all of C₁ and
  lk(C₃,C₁)=0. This is a genuine *linking number* ⇒ reflection-ODD by construction.
- **Method B — Massey jump-correction.** **μ̄_B := Σ over C₃'s piercings of the
  disk S₁ of [piercing sign] · Ω₂(piercing)/(4π)** — the reflection-ODD part of
  the solid-angle integral (Ω₂ = solid angle of C₂; the piece the reflection-even
  ∮Ω₁(B₂·dl₃) omitted). Normalization fixed by the Borromean magnitude.

## §2 — Validation criteria (committed; the result is judged against THESE)

| # | Criterion |
|---|---|
| **P1** | **split/unlink ⇒ μ̄ = 0** (both methods) |
| **P2** | **spatial mirror ⇒ μ̄ → −μ̄** (both methods reflection-odd — the whole point) |
| **P3** | **\|μ̄\| = 1** on the genuine Borromean (textbook integer) |
| **P4** | **cyclic consistency (Method A):** μ̄(123)=μ̄(231)=μ̄(312); μ̄(213)=−μ̄(123) |
| **P5** | **two-method agreement:** sign(μ̄_A) = sign(μ̄_B) and \|μ̄_A\|=\|μ̄_B\|=1 |

## §3 — Promotion rule (committed)

- If **P1–P3 hold for Method A AND (P4 cyclic-consistency) AND (P5 agreement
  with Method B)** → sign(μ̄) is **established (R1)**; the witness↔invariant
  identification of `g2_milnor.py` / the V4.29 record **promotes** out of
  R3-pending. The *value* of sign(μ̄) on the chosen Borromean is then a result.
- If a method is **reflection-even** (P2 fails) or non-integer (P3 fails) or the
  methods **disagree** (P5 fails) → the sign is **NOT** established; report
  honestly which criterion failed; the sign stays R3-pending. **No ±1 is faked.**
- **Either way**, the registered sign(φ)↔QR/QNR map is **untouched** (only its
  *consistency check* could promote it, never this computation), and the
  Eddington guard holds: a mirror flip is the *expected* behaviour of a correct
  reflection-odd sign, not independent "confirmation" of any physical map.

*Cross-refs: `tools/g2_milnor.py` (the witness), `tools/g2_milnor_int.py` (the
reflection-even magnitude integral), `reports/SQT_3.4_SIGNMAP_REGISTRATION.md`
(the map this would promote). Append-only.*
