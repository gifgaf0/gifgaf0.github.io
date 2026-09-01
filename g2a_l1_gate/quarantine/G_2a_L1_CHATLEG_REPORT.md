# Gate G-2a-L1 — CHAT LEG EXECUTION REPORT
## The Spin–Isospin Locking Assembly (targets §2.87.A's R3 sharpened postulate)

**Date:** 2026-07-11
**Leg:** chat (leg 1 of 2; CC leg pending)
**Locked pre-registration:** `G_2a_L1_EXECUTION_PREREGISTRATION.md` — md5 `da9c25d19ff91f2c0809ac0027a7bebb` (locked BEFORE leg execution; clean order register → lock → leg)
**Chat-leg script:** `g_2a_L1_chatleg.py` — md5 `2f0fa8f4abb85291250cb49a1bf756f2`
**Arithmetic:** exact throughout — ℚ(√2) Fraction pairs; Cℓ(3)^q both algebras for Parts 1–3; integer matrices; 𝔽₃ for the GL(2,3) discriminator. No floating point anywhere.
**Result:** ALL CHECKS PASS — **8,484 assertions.** One pre-registration correction (below, prominent) and one self-caught development bug, both logged.

---

## 0. THE PRE-REGISTRATION CORRECTION (F4/F5 fired-and-resolved-by-repose — the S7 Πε / S9 B1 precedent class)

The registration's D1 defined κ_χ := χ∘c as a ℤ/2-valued pushforward of the extension 1 → Γ̃ → Ñ → M → 1. **That pushforward provably does not exist**, and the machine exhibits the obstruction rather than assuming it:

- **z = [q̃₁, q̃₂] exactly** in the finite model (Clifford part −1, translation ≡ 0 mod 2ℤ³) — the central element is a **commutator**, hence killed by every abelian-valued homomorphism;
- exhaustively (word-cover + full homomorphy check over all 16×16 products): **Γ̃₂ has exactly 8 characters to ℤ/2 and every one of them kills z** — both Pin types.

So no homomorphism Γ̃ → ℤ/2 sends z ↦ −1, equivariantly or otherwise; the drafted κ_χ is type-impossible. Per the pre-committed F4/F5 provision ("halt, re-pose"), the re-pose IS the obstruction formulation, and it lands B1 in the registered SPLIT arm in sharpened form. The framing was corrected by canon's own machinery; the substantive question survives and is answered. (Also note: the N-native structures are trivial on Γ, so the alternative literal reading χ∘c ≡ +1 is degenerate — both readings fail, one vacuously, one by obstruction; the obstruction is the content.)

## 1. F1 regression pack + Part-2 constructions (both algebras) — all pass

Closures 768/384/16/8; h² = t₍₁,₁,₁₎ on the nose; glide = r₁∘(−I); meridian −1; ω² = −q; bivector squares −1 both algebras (the Pin-blind Spin sector — the license for running Parts 4–6 once); axial-law spot-checks (S10 regression); characters trivial on Γ.

**The motion group, built and verified (R1):** M = G_fin/Γ_fin with |M| = 48; coset multiplication associative with identity/inverses asserted; **Z(M) = ℤ/2 and the central class IS the −I class** (S9 dictionary regression); det is constant on cosets; **M⁺ = det-+1 classes has order 24 with conjugacy class sizes [1,3,6,6,8] and element orders {1,2,3,4} — S₄ exactly**; M = Z × M⁺ direct (48 distinct products). Both algebras.

## 2. B1 — which extension does the flat home induce? **NOT-INDUCED-BY-OBSTRUCTION (the SPLIT arm, sharpened) [R1, both Pin types]**

Two machine facts close the bit:

1. **The obstruction** (§0): z is a commutator in Γ̃₂; all 8 characters kill it; **no equivariant pushforward of 1 → Γ̃ → Ñ → M → 1 to a ℤ/2-extension of M exists.**
2. **The D2 collapse lemma, verified as registered:** |Ñ_fin/Γ̃_fin| = 48 = |M| — the two lifts of every motion land in one coset; the sign is absorbed because **z lies in the deck image** (the S8 non-splitness means the orbifold-native structures spend z as deck monodromy).

**Geometric statement (R1 + R2 location):** in the flat home, every isometry acts **canonically** (unambiguously) on every orbifold-native spinor bundle — the static home manufactures **no** ℤ/2 cover of the motion group, neither 2O nor the other Schur cover. **The postulate's "spatial 2O" therefore lives in the loop/motion sector** — exactly where the chain already put its pieces: S4's FR theorem (exchange ≃ 2π) and S8's meridian −1 (the 2π loop's sign, derived, ontology-conditional). This is the registered SPLIT arm's location statement, now with the obstruction mechanism attached. The registration §7(a) point-group sketch is thereby superseded (neither 2O-INDUCED nor deck-DRESSED: the static extension question is closed by obstruction before dressing matters); §7(c)'s collapse expectation is confirmed.

## 3. F2 — the discriminator control (passes BEFORE framework identification)

- **2O** built by exact Clifford BFS (48 elements; **unique involution = −1**; double cover of O verified 24×2; O proper with S₄ class data [(1,1),(3,2),(6,2),(6,4),(8,3)]; [O,O] = A₄ = ker(sgn)); **every order-2 class of O lifts at order 4** — the binary-cover fingerprint.
- **GL(2,3)** built over 𝔽₃ (48 elements; PGL(2,3) = 24; the size-6 order-2 class located); **every element of that class has a genuine involution preimage** — the opposite fingerprint.
- The discriminator separates the two covers. (One self-caught development bug here: the first C₄-orientation assert was over-specified to one rotation direction; relaxed to the load-bearing invariant — order-4 proper rotation about e₃. No result affected; logged.)

## 4. B2 — the assembly on the relocated substrate. **ASSEMBLED-RELOCATED [R1 mechanics, R2 verdict]**

With the static home closed by B1, the assembly runs on the loop-sector substrate: the motion group's spatial image O ⊂ SO(3) (S4, R1) has Spin(3)-preimage = the 2O of Part 3 — classical, and machine-instantiated here. Transport along S5's canonical Φ (Aut(S₄) = Inn, so WLOG lifts over id):

- **Exactly 2 lifts** α: 2O → 2O cover the identity of the S₄ quotients (full 48-element homomorphy check per candidate) — the torsor over Hom(S₄, ℤ/2) = {1, sgn}; **both fix z**.
- **The sgn-twist acts trivially on the 4-dim module:** χ_{3/2} (computed exactly via Chebyshev U₃ on scalar parts; S1 regressions ⟨χ,χ⟩ = 1 and χ(z) = −4 re-verified) **vanishes on every odd class** — so the two lifts pull the module back identically. Combined with Φ's V₄-inner ambiguity (inner ⇒ module-isomorphic), **the module transport is UNIQUE outright.**

**Import list, enumerated (the verdict's conditionality):** (i) the S8 ontology axes (cone-π scaffolding + carrier identification) behind the FR sign −1↦−Id; (ii) the S4 ambient-motion realization layer (its shared-solver caveat carried); (iii) the S2/V4.50 octahedral-representative gap — the 2O lock is a **motion-group** statement; the rigid canonical representative supports only the 2T restriction (both lattices reported below); (iv) the χ_FR selection residue (new, located — §5); (v) the Spin-sector assembly is **Pin-independent** (bivector² regression), so the S9 Pin-type ℤ/2 import does not enter B2 — it stands unchanged elsewhere.

## 5. B3 — the admissibility lattices [R1] and dispositions

m(J,I;χ_FR) = ⟨Res χ_J · Res χ_I, χ_FR⟩ over the diagonal lock; exact ℚ(√2) sums, integrality and nonnegativity asserted per cell; ranges 2J ∈ {1,3,5,7}, 2I ∈ {1,3,5}. Nonzero entries, (2J,2I) → m:

- **2O-locked, χ_FR = triv:** {(1,1): 1, (3,3): 1, (3,5): 1, (5,3): 1, (5,5): 2, (7,1): 1, (7,3): 1, (7,5): 2} — **the unique lowest entry is (J,I) = (1/2, 1/2), multiplicity 1.**
- **2O-locked, χ_FR = sgn:** {(1,5): 1, (3,3): 1, (3,5): 1, (5,1): 1, (5,3): 1, (5,5): 1, (7,1): 1, (7,3): 1, (7,5): 2} — (1/2,1/2) NOT admissible.
- **2T-restricted (the rigid representative's group):** {(1,1): 1, (1,5): 1, (3,3): 2, (3,5): 2, (5,1): 1, (5,3): 2, (5,5): 3, (7,1): 2, (7,3): 2, (7,5): 4} — (1/2,1/2) admissible, multiplicity 1.

**Parity law (R1, machine-verified across all three tables):** m ≠ 0 ⇒ J + I ∈ ℤ. With the fermionic sector J half-integer (S8-conditional), **the diagonal lock forces half-integer isospin.**

**Adjacent-dialect comparison (unsealed AFTER the machine output, labeled, not imported):** the B=3 tetrahedrally-symmetric Skyrmion's ground state is (J,I) = (1/2, 1/2) (Carson; Krusch/Manton–Wood). The 2T-restricted lattice — the group matching that soliton's symmetry — admits (1/2,1/2) at multiplicity 1, and the 2O-locked lattice under χ_FR = triv has (1/2,1/2) as its **unique lowest** entry. Recorded as adjacent-dialect consistency; any physical reading is R3-quarantined. **The χ_FR selection is NOT derived here** — under sgn the (1/2,1/2) entry is absent — a located residue of the assembly (in the Skyrmion dialect this sign is Krusch's loop-homotopy datum; no SQT counterpart is computed by this gate).

**B3(ii) Assignment disposition: NEUTRAL.** The gate's internal side is the S5 line-stabilizer/Sym³ structure; nothing computed forces Assignment II or contradicts Assignment I (S1's transversality stands, cited not recomputed). Recorded as the registered disposition bit.

## 6. Verdict [R2; M.REL per-axis] — mixed, per the registered arms

**B1 SPLIT (sharpened: NOT-INDUCED-BY-OBSTRUCTION) / B2 ASSEMBLED-RELOCATED / B3 content-classified.** Scale — none. Metric — flat/ambient, inherited from the chain. Sign — the FR −1 remains S8's derived, ontology-conditional loop-sector fact; the new located residue is the χ_FR selection; no new sign import beyond it. Ontology — unchanged and quarantined. **Net for §2.87.A:** the sharpened postulate's structural content upgrades from bare R3 to **derived-conditional assembly** — the spatial 2O exists on the loop-sector substrate (not the static home, by obstruction), the identification with the internal 2O is unique at module level, the FR sign is supplied conditionally by S8 — with the import list of §4 and the χ_FR residue. The **dynamical** derivation clause of §2.87.A remains open (M.CW wall), untouched by design.

## 7. Honesty log

1. **Pre-registration correction (prominent, §0):** D1's pushforward type-impossible; F4/F5 fired as designed; re-posed to the obstruction theorem; B1 answered in the registered SPLIT arm. Precedent class: S7 Πε / S9 B1 ("the framing corrected by canon's own machinery").
2. **Self-caught development bug:** over-specified C₄-orientation assert in the F2 control (twisted-adjoint rotation-direction convention); relaxed to the invariant; no result affected.
3. Registration sketches: §7(c) confirmed (collapse); §7(a) superseded by the obstruction (the extension question closes before point-group leanings or deck dressing apply); §7(b) moot for B2 (Spin-sector Pin-blind; the Pin-type import untouched).

## 8. What this leg does NOT claim (§9 carried)

No Gate-2a closure — the assembly is conditional-R2 with the §4 import list, and the **dynamical selection** remains open (the I1–I3 wall; §2.52 Open 3 frozen and untouched). No μ_n; the octahedral-representative gap stands (both lattices reported precisely so the gap stays visible). No nucleon identification — the (1/2,1/2) entries are lattice facts plus a labeled adjacent-dialect comparison, R3 beyond that. No observables. No Assignment resolution. The gauge-paper §7.4 firewall held.

## 9. Status and next steps

- **Chat leg: COMPLETE (green).**
- **Awaiting: CC leg** — requested variation per §8: the direct H²(M, ℤ/2) cohomological route for the obstruction/extension side, and/or the SU(2)/ℚ(i,√2) model for the 2O side; CC's own LSF extension + in-execution collision check. (Chat-side in-execution collision check: run at registration for the locking-derivation and which-cover questions — no published counterpart of either found in the #24/HW family; to be re-run/extended by CC per standing practice, and re-verified chat-side at comparison.)
- Two-leg comparison → fold per §10 (§2.87.J, one Part VI row, additive annotation on §2.87.A's postulate paragraph; no §3.x; target V4.63) on author authorization.
