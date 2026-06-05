# §3.4-G2-Milnor — Sign-Map Registration (Pre-Commit)

**Date:** 2026-06-04
**Registered by:** M. Gifford (framework author), on the SQT-agent + CC audit of
`tools/g2_milnor.py`. **This is a PRE-COMMIT**, recorded *before* any sign is read
as confirmed physics, so that the consistency test below — not a post-hoc match —
is what decides it.
**Folds as:** V4.29 / Paper II §3.4.6 (V4.28 = the unrelated §2.45-PAIR increment).
**Eddington watch:** ACTIVE — "μ̄ flips under a mirror" must **not** be read as
confirmation of the substantive half (see §3).

---

## §1 — What is R1 (the factorization), and what is being registered (the map)

**R1 (established, not part of the pre-commit).** μ̄^φ = φ_{d₁d₂d₃} · μ̄(123)
carries **two independent sign degrees of freedom**, which flip under two
independent operations (all four combinations realized, `g2_milnor.py`):
- a **φ-orientation** sign — rigorous, algebraic (φ_abc) — flips under **QR↔QNR
  cyclic reassignment** of the windings;
- a **reflection-odd geometric handedness witness** — flips under a **spatial
  mirror**.

*Precision (per audit):* the geometric witness is a reflection-odd handedness
pseudoscalar; its **identification with the rigorous topological invariant
sign(μ̄)** is **R3-pending the third-order-helicity (Massey) integral**. So what
is R1 is the *two-independent-DOF factorization*, not "sign(μ̄)=this witness."
The magnitude method (Seifert triple-point count) is **config-specialized**
(exact for the orthogonal flat disks); the integral is the general authority.

## §2 — The registered physical sign-map (the pre-commit)

| Computed sign | Flips under | Registered physical chirality | Weight |
|---|---|---|---|
| **sign(μ̄)** (topological, pending integral) | spatial mirror | **spatial parity** | **Forced** — a reflection-odd invariant *is* parity-odd; NOT credited as a discovery |
| **sign(φ)** (φ-orientation, internal/algebraic) | QR↔QNR reassignment | **the QR/QNR algebraic chirality of §2.75/§2.76**, carrying the baryon's **matter/antimatter-type** chirality | **Substantive** — the registered commitment |

**Registered claim.** The baryon's matter/antimatter-type chirality rides on
**sign(φ)** (the internal QR/QNR orientation), **independent of** the spatial
parity carried by sign(μ̄). Parity and QR/QNR are registered as **two distinct
Z₂'s** (one in each sign), **not** coincident.

## §3 — The test (what makes this falsifiable — and what does NOT count)

**The test is CONSISTENCY, not the mirror.** The sign(φ)↔QR/QNR assignment is
checked against how the QR/QNR Z₂ **already** enters the framework, independently
of this computation:
- **§2.75/§2.76** — the F₂₁ QR↔QNR involution on the SL(2,7) spin representations
  (the Galois-twist, not a spin-flip);
- **§2.86C** — the principal anti-automorphism eᵢ→−eᵢ (𝕆↔𝕆^op);
- the existing **matter/antimatter** assignment.

**Falsification condition.** If the sign(φ) orientation that the baryon's
matter/antimatter chirality requires here is **inconsistent** with the QR↔QNR
orientation those sections already fix (e.g. it would force the opposite
anti-automorphism convention, or couple to spatial parity), the registration is
**falsified** and the map must be revised or retired.

**Explicitly NOT a confirmation (Eddington guard).** "sign(μ̄) flips under a
spatial mirror" is **forced** by topology and must not be cited as evidence for
the registered map. Only the §3 consistency of the *substantive* half
(sign(φ)↔QR/QNR) counts.

## §4 — Register and status

- **Factorization (two independent sign DOF):** R1 (verified).
- **sign(μ̄) ↔ spatial parity:** forced / near-definitional; R1 as a statement
  *about parity-oddness*, but the witness↔topological-sign identification is
  R3-pending the integral.
- **sign(φ) ↔ QR/QNR (the registered substantive map):** **R3 — a registered
  pre-committed prediction**, to be promoted only on passing the §3 consistency
  check, never on the mirror flip.

## §5 — What this does and does not do

- **Does:** register, before reading any result, that the baryon's
  matter/antimatter chirality is the QR/QNR sign(φ), distinct from spatial
  parity — turning the otherwise post-hoc-matchable sign into a falsifiable
  consistency claim against §2.75/§2.76/§2.86C.
- **Does NOT:** assert the map as confirmed (it is R3 pending the §3 check);
  supply the rigorous topological sign(μ̄) (pending the Massey integral); close
  §2.15; realize a Borromean *field* soliton (the deferred G2-knot).

*Cross-refs: `tools/g2_milnor.py`, `reports/SQT_3.4_G2_MILNOR_FIRST_PASS.md`,
§2.75/§2.76 (QR/QNR involution), §2.86C (principal anti-automorphism), §2.15
(Borromean baryon). Append-only.*
