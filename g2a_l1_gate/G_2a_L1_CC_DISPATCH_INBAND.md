# G-2a-L1 — CC-LEG DISPATCH (IN-BAND, P-4 SELF-CONTAINED)
## The Spin–Isospin Locking Assembly — leg 2 of 2

**Dispatch date:** August 27, 2026 (prepared chat-side on the author's recovery of the estate; the author's act of placing this file in the CC repo constitutes the dispatch).
**Standing rule P-4:** this is ONE self-contained file; every artifact it depends on is embedded below byte-exact with its md5 and byte count; no side-channel message is load-bearing. Verify-then-build: extract and md5-verify every embed BEFORE writing any code.
**Lock status:** the pre-registration was LOCKED July 11, 2026 at md5 `da9c25d19ff91f2c0809ac0027a7bebb` (18,381 B) before the chat leg executed (clean order register → lock → leg). It is embedded here byte-identical. **No new elections; no re-lock cycle.** The D5 lesson is honored: the locked artifact travels in-band.
**Ledger context:** the pre-registration was written against V4.62; canonical is now V4.78 (August 27, 2026). The ledger is append-only, so the S1–S10 chain content this gate consumes is byte-preserved; §2.87.J remains RESERVED for this gate (verified against V4.78: no §2.87.J exists; the G-2a-L1/§2.87.J fold has been carried RETARGETED at every fold since V4.63). Fold target: the next canonical after V4.78, per prereg §10 with the version number retargeted (section numbers are content-anchored).
**Chat leg of record:** `g_2a_L1_chatleg.py` md5 `2f0fa8f4abb85291250cb49a1bf756f2` (23,048 B) — 8,484 assertions, ALL CHECKS PASS; re-executed fresh chat-side August 27, 2026 (exit 0, ~5 s), byte-identical to the July 11 artifact cited in the chat-leg report. Its report, run log, and checkpoint are embedded QUARANTINED (see §3).

---

## 0. Embed manifest (verify all nine before anything else)

| Embed | md5 | bytes |
|---|---|---|
| `activation_G_2a_L1.json` | 80bcd166bdfee8a275d97d30a4e64ec7 | 1783 |
| `G_2a_L1_EXECUTION_PREREGISTRATION.md` | da9c25d19ff91f2c0809ac0027a7bebb | 18381 |
| `t1_forbidden_G_2a_L1.txt` | 04438b74e0ade26cc3f4415bb20e7b6d | 117 |
| `g_2a_L1_compare.py` | 67ee429aa8789188bbd4aee11951b15a | 3267 |
| `extract_embeds_G_2a_L1.py` | 63942160beed37c28aed4234c185c4a0 | 1464 |
| `g_2a_L1_chatleg.py` | 2f0fa8f4abb85291250cb49a1bf756f2 | 23048 |
| `g_2a_L1_run.log` | 30951582d29372ff68595c1876581a1f | 1807 |
| `g_2a_L1_chat_checkpoint.json` | 476052b1e075db43a6e8b7a2bb5b0be3 | 2296 |
| `G_2a_L1_CHATLEG_REPORT.md` | 753a34ec8347254801e9517ecb4d23a6 | 11868 |

Dispatch self-check performed chat-side at build time: every embed re-extracted from this file and md5/byte-verified (see the return of `extract_embeds_G_2a_L1.py` in the build log).

## 1. Verify-then-build (Phase 0)

1. Save the extractor below as `extract_embeds_G_2a_L1.py` (it is also embedded, so the byte-exact copy can be recovered from its own marker if the fenced copy is mangled by rendering).
2. Run `python3 extract_embeds_G_2a_L1.py G_2a_L1_CC_DISPATCH_INBAND.md .` — it must print nine `OK` lines and `extracted 9 embeds, all md5/byte-verified`. Any assertion failure ⇒ HALT and report; build nothing.
3. Confirm `md5sum G_2a_L1_EXECUTION_PREREGISTRATION.md` = `da9c25d19ff91f2c0809ac0027a7bebb`. Write `cc_phase0.json` {embeds: [name, md5, bytes]..., prereg_md5, verified: true}.
4. Read the pre-registration IN FULL. It is the object of record; this dispatch adds procedure only and cannot amend it.

```python
#!/usr/bin/env python3
# extract_embeds_G_2a_L1.py — byte-exact extraction of every embed in the
# G-2a-L1 in-band dispatch. Usage: python3 extract_embeds_G_2a_L1.py G_2a_L1_CC_DISPATCH_INBAND.md [outdir]
# Every embed is verified against the md5 and byte count declared in its BEGIN marker.
# Any mismatch aborts (verify-then-build: nothing is built on an unverified embed).
import sys, os, re, hashlib

BEGIN = "<<<EMBED-" + "BEGIN name=(\\S+) md5=([0-9a-f]{32}) bytes=(\\d+)>>>\n"
END   = "<<<EMBED-" + "END name=%s>>>"

def main(path, outdir="."):
    data = open(path, "rb").read()
    text = data.decode("utf-8")
    n = 0
    for m in re.finditer(BEGIN, text):
        name, md5, nbytes = m.group(1), m.group(2), int(m.group(3))
        start = m.end()
        endmark = (END % name)
        j = text.find(endmark, start)
        assert j > 0, "END marker missing for " + name
        payload = text[start:j].encode("utf-8")
        got = hashlib.md5(payload).hexdigest()
        assert len(payload) == nbytes, "byte count mismatch %s: %d vs %d" % (name, len(payload), nbytes)
        assert got == md5, "md5 mismatch %s: %s vs %s" % (name, got, md5)
        out = os.path.join(outdir, name)
        open(out, "wb").write(payload)
        print("OK  %s  %s  %d B" % (md5, name, nbytes))
        n += 1
    print("extracted %d embeds, all md5/byte-verified" % n)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else ".")
```

## 2. What the CC leg computes (the pre-registration's §3–§5, own method)

Rebuild the finite models yourself (768/384; 16/8), exact arithmetic, both Pin types (e_i² = +1 / −1), the M.2π loop dictionary, q-adaptive lifts by ρ-match. **Zero code reuse from the chat instrument** (its body is quarantined until §3 is satisfied; only its md5 is consulted in Phase 0). The S7 Γ/N presentation is the one flagged shared layer.

**Requested variation (prereg §8):** the direct cohomological route. Concretely —
- **B1 (obstruction/extension side):** decide whether the extension 1 → Γ̃ → Ñ → M → 1 admits an (equivariant) pushforward to a ℤ/2-extension of M by computing Hom(Γ̃₂, ℤ/2) via an INDEPENDENT route — e.g., the abelianization Γ̃₂^ab ⊗ 𝔽₂ from a relation matrix (Smith normal form) or an independent cocycle/coboundary solver on the finite model — and reading where the central element z lands. Verify the D2 collapse (|Ñ_fin/Γ̃_fin| vs |M|) by your own coset enumeration. Report the arm per prereg §4 (2O-INDUCED / OTHER-COVER / SPLIT / STRUCTURE-DEPENDENT / PIN-SPLIT), with the d-factor sub-arm.
- **F2 (discriminator, BEFORE any framework data):** build 2O and GL(2,3) abstractly by your own construction — the SU(2)/ℚ(i,√2) model for 2O is the requested form — and show the transposition-lift-order fingerprint separates them. Halt if it does not.
- **B2 (assembly):** enumerate lifts over id_{S₄} between the spatial-image cover and the internal 2O (S5 Φ; Aut(S₄) = Inn), count them, test whether each fixes z, compute χ_{3/2} on the SU(2) model (your own character route — traces, not Chebyshev on scalar parts) and record its values on odd classes; report the arm (ASSEMBLED / AMBIGUOUS / OBSTRUCTED) and the import list you can enumerate from the chain.
- **B3 (admissibility lattices):** m(J, I; χ_FR) = ⟨Res χ_J · Res χ_I, χ_FR⟩ over the diagonal lock for 2J ∈ {1,3,5,7}, 2I ∈ {1,3,5}, three tables: 2O-locked χ_FR = triv; 2O-locked χ_FR = sgn; 2T-restricted. Assert integrality and nonnegativity per cell. Check the parity law (m ≠ 0 ⇒ J + I ∈ ℤ) mechanically. Record the Assignment disposition bit.
- **Falsifiers and controls F1–F6, C1–C3** live, exactly as registered. F4/F5: note the pre-registration's own provision — "failure ⇒ halt, re-pose." If your D1 pushforward attempt fails, EXHIBIT the obstruction mechanically and state which registered arm the re-pose lands in; do not import the chat leg's framing (you cannot see it yet).
- **Eddington traps (prereg §6):** no physical quantum number or adjacent-dialect soliton value in any instrument or checkpoint — the T1 list enforces the vocabulary (exemptions: the locked pre-registration and the quarantined chat artifacts, which legitimately name the sealed dialect); the adjacent-dialect comparison may appear ONLY in your report, in a section written after your checkpoint is hashed, labeled adjacent-dialect.
- **LSF extension + in-execution collision check (prereg §2, mandatory both legs):** search for any published derivation of a soliton spin–isospin locking from orbifold/crystallographic spin-structure data, and for "which double cover of the isometry group does a flat-orbifold spin structure induce" in the #24/Hantzsche–Wendt family. Record queries and results verbatim; the registration-time expectation (novel-in-assembly) is to be verified, not assumed.

**Per-phase JSON checkpoints (E8):** `cc_phase0.json` (verify), `cc_phase1.json` (F1 + M), `cc_phase2.json` (F2), `cc_phase3.json` (B1), `cc_phase4.json` (B2), `cc_phase5.json` (B3), then the consolidated `g_2a_L1_cc_checkpoint.json`. Write each as its phase completes (the timeout-lost-modes lesson).

**CC checkpoint schema** — `g_2a_L1_cc_checkpoint.json` must carry exactly these blocks and keys (values are yours); the frozen comparator flattens and compares them exactly:

```
schema = "g2a_l1_checkpoint_v1"; gate = "G-2a-L1"; leg = "cc"; prereg_md5 = "da9c25d19ff91f2c0809ac0027a7bebb"
instrument_md5, run_log_md5, assertions, all_checks_pass, pin_types_run
C1_F1: closures_768_384_16_8, h_squared_eq_t111, glide_eq_r1_circ_minusI, meridian_minus_one, omega_squared_eq_minus_q, bivector_squares_minus_one_both_algebras, characters_trivial_on_Gamma   (booleans)
C2_M:  order_M, center_order, center_is_minusI_class, M_direct_Z2_x_Mplus, Mplus_order, Mplus_class_sizes (sorted list), Mplus_element_orders (sorted list)
C3_B1: z_is_commutator_q1_q2, num_characters_Gamma2_to_Z2, all_characters_kill_z, D2_collapse_quotient_order, arm, arm_sharpened, pin_dependence
C4_F2: 2O_order, 2O_unique_involution_is_minus_one, 2O_all_order2_classes_of_O_lift_at_order_4, O_class_data ([[size, order]...] sorted), GL23_order, GL23_transposition_class_size, GL23_transposition_class_has_involution_preimage, discriminator_separates
C5_B2: num_lifts_over_id_S4, both_lifts_fix_z, chi_3half_vanishes_on_all_odd_classes, chi_3half_norm, chi_3half_at_z, module_transport_unique, arm, pin_independent
C6_B3: lattice_2O_triv, lattice_2O_sgn, lattice_2T (dicts keyed "2J,2I" → m, NONZERO entries only), parity_law_all_tables, assignment_disposition
```
`arm` strings are the pre-registration's arm names verbatim (B1: one of 2O-INDUCED / OTHER-COVER / SPLIT / STRUCTURE-DEPENDENT / PIN-SPLIT; `arm_sharpened` free text; B2: ASSEMBLED / AMBIGUOUS / OBSTRUCTED, optionally suffixed; disposition: NEUTRAL / CONSTRAINS-I / CONSTRAINS-II). `pin_dependence`: "none" or the variation law.

## 3. Blindness clause (procedural — the G-POLY1 H-8 disclosure carried)

This dispatch necessarily carries the chat artifacts. Blindness is maintained procedurally, not by information barrier: you build your independent stack, write and `md5sum` your `g_2a_L1_cc_checkpoint.json`, commit it, and ONLY THEN open `G_2a_L1_CHATLEG_REPORT.md`, `g_2a_L1_run.log`, `g_2a_L1_chat_checkpoint.json`, or the body of `g_2a_L1_chatleg.py`. Record the commit hash of your checkpoint before the first consultation in your report (`H-CC-` item if any deviation). If you consult early for any reason, that is a logged deviation, not a silent one.

## 4. Comparison protocol (frozen)

After hashing your checkpoint: `python3 g_2a_L1_compare.py g_2a_L1_chat_checkpoint.json g_2a_L1_cc_checkpoint.json`. The comparator (md5 in the manifest, FROZEN pre-return) requires exact identity on C1–C6 and verdict identity on the three arms. Any MISS ⇒ S9 counter-cross-check protocol (prereg §8): fingerprint the divergence with its mechanism, do not re-tune, do not average representatives (F3), do not touch the registered arms; the chat side re-runs the same frozen comparator on return. Both outcomes are findings — an S9 fire on a real divergence is the two-leg protocol operating as designed.

## 5. Return manifest (what comes back, one commit on `claude/<descriptor>`)

- `g_2a_L1_ccleg.py` (or your instrument set) — md5 + bytes; T1 scan output showing zero hits on every instrument and checkpoint.
- `cc_phase0..5.json`, `g_2a_L1_cc_checkpoint.json` — md5 + bytes each; the checkpoint's pre-consultation commit hash.
- Comparator output (verbatim) — md5 of the captured output.
- `G_2a_L1_CCLEG_REPORT.md` — per-bit results with mechanisms; the honesty ledger `H-CC-1..n` (every self-catch numbered, none silent); deviations `D-CC-1..n`; the LSF/collision-check record; the adjacent-dialect comparison (if any) in a clearly separated post-hash section; explicit non-claims (prereg §9 carried verbatim).
- Branch name and commit hashes.

## 6. Non-claims (prereg §9, binding)

No Gate-2a closure (any ASSEMBLED outcome is conditional R2 with the enumerated import list); the dynamical selection remains open (M.CW wall; the I1–I3 ticket); no μ_n; no observable; no carrier identification; no Assignment resolution unless the machine forces one; the octahedral-representative gap stands; the gauge-paper §7.4 firewall held; the §2.52 Open 3 row untouched.

---

# EMBEDS (byte-exact; extract with the script in §1 — do not copy by hand)

### EMBED — ACTIVATION FLAGS (P-4) — `activation_G_2a_L1.json` (md5 80bcd166bdfee8a275d97d30a4e64ec7, 1783 B)

<<<EMBED-BEGIN name=activation_G_2a_L1.json md5=80bcd166bdfee8a275d97d30a4e64ec7 bytes=1783>>>
{
 "BLIND_UNTIL_CC_CHECKPOINT_HASHED": true,
 "BRANCH_NAMING": "claude/<descriptor>",
 "COMPARATOR_FROZEN": "g_2a_L1_compare.py (embedded; md5 in the manifest) \u2014 run it yourself after hashing your checkpoint; the chat side re-runs it on return",
 "EXECUTE_CC_LEG": true,
 "FOLD_TARGET": "next canonical after V4.78 (V4.79 at earliest), section \u00a72.87.J (reserved; content-anchored), per prereg \u00a710 \u2014 the prereg's 'V4.63' target is superseded by the sequential convention (V4.63 record clause)",
 "FORBIDDEN": "no modification of any embed; no consultation of the quarantined chat artifacts before the CC checkpoint is hashed; no physical quantum number or adjacent-dialect soliton value in any instrument or checkpoint (prereg \u00a76 trap 1); no dynamics (trap 7); no magnetic-moment content (trap 4); the \u00a72.52 Open 3 row untouched",
 "NEW_ELECTIONS": "none \u2014 the July 11, 2026 lock (da9c25d1) stands; no re-lock cycle",
 "PER_PHASE_JSON_CHECKPOINTS": true,
 "PIN_TYPES_REQUIRED": [
  "Pin+",
  "Pin-"
 ],
 "REQUESTED_VARIATION": "direct H^2(M,Z/2) cohomological route (independent cocycle/coboundary or abelianization solver) for B1; SU(2)/Q(i,sqrt2) model for the 2O side (B2/B3); own character route for the lattices",
 "S9_ON_ANY_MISS": true,
 "SHARED_LAYER_FLAGGED": "the S7 Gamma/N presentation (standing caveat); finite models REBUILT per leg, zero code reuse from the chat instrument",
 "T1_SCAN": "grep -n -i -F -f t1_forbidden_G_2a_L1.txt <every CC instrument and checkpoint> must return zero hits (pattern lines only, H-2 rule); justified exemptions: the locked pre-registration and the quarantined chat artifacts, which legitimately name the sealed dialect",
 "VERIFY_THEN_BUILD": true,
 "dispatch_date": "2026-08-27",
 "gate": "G-2a-L1"
}
<<<EMBED-END name=activation_G_2a_L1.json>>>

### EMBED — LOCKED PRE-REGISTRATION (July 11, 2026; md5 da9c25d1 — the object of record) — `G_2a_L1_EXECUTION_PREREGISTRATION.md` (md5 da9c25d19ff91f2c0809ac0027a7bebb, 18381 B)

<<<EMBED-BEGIN name=G_2a_L1_EXECUTION_PREREGISTRATION.md md5=da9c25d19ff91f2c0809ac0027a7bebb bytes=18381>>>
# G-2a-L1 EXECUTION PRE-REGISTRATION — The Spin–Isospin Locking Assembly: Does the Completed Flat-Home Chain Derive §2.87.A's Structural Locking?

**Date:** July 11, 2026
**Status:** DRAFT — LOCK REQUIRED BEFORE ANY LEG EXECUTES. md5 of the locked text to be recorded at lock. Declared clean order: register → lock → legs (the S10 chat-side standard; the header provision for lock-by-forwarding carried verbatim: if forwarding precedes an explicit lock, the deviation is logged per the S8/S9/S10 precedent and the locked text must be byte-identical to the forwarded draft).
**Targets:** §2.87.A's R3 core — *"Gate 2a, sharpened (R3 — the irreducibly-physical core). The baryon soliton's spatial frame is locked to an internal frame so that the spatial binary-octahedral 2O is identified with the 2O of the spin/isospin SU(2) (the ℂ⊗ℍ factor); the physical 2π spatial rotation is then the central element ↦ −Id on that 4, supplying the FR sign"* — and §2.87.A's own open list: *"the locking remains an R3 postulate; the dynamical derivation and the assignment question are open."* This gate executes the **structural** half only (see §9 for the M.CW scope wall).
**Ledger context at registration:** V4.62 CANONICAL (md5 d8005fb9). The §2.52 Open 3 row FROZEN per standing instruction and untouched by this gate.

---

## 1. Target and lineage (the assembly inventory — all R1/R2 unless noted)

The flat-home chain S1–S10 is structurally complete. The locking postulate's ingredients, as executed:

- **S1 (§2.87.B):** the FR/spinor-phase condition selects 2O's genuine sector; the 4-dim irrep is FORCED given octahedral 2O (D1 = 1); the locked spin-SU(2) must be **transverse to color** (D2) — admissibility established, locking NOT derived.
- **S2 + V4.50 (§2.87.B):** the canonical Borromean representative caps at **tetrahedral A₄** (every planar-per-strand embedding, by CKS §10.1) — the **octahedral premise is a located import**, standing.
- **S4 (§2.87.C):** motion group O ≅ S₄ with the parity law Πε = sgn(σ); exchange ≃ 2π (FR theorem); Sym³(ℂ²) the unique 4-dim S₃-isotypic.
- **S5 (§2.87.D):** the motion S₄ and the Fano line-stabilizer S₄ are **canonically identified** (Φ, equivariance-verified over all 72 pairs, unique up to the 4 inner automorphisms by V₄); Sym³(ℂ²)|₂O the unique genuine 4-dim — *"one S₄, one spinor lift, one 4-dim module, still bottlenecked on the single OPEN §2.50 per-strand spinor phase."*
- **S7 (§2.87.F):** the full motion group is realized STATICALLY in the flat orbifold home: Isom(E³/Γ) = N/Γ ≅ ℤ/2 × S₄, Φ_flat faithful, odd coset nonsymmorphic (½,½,½).
- **S8 (§2.87.G):** the spin extension over Γ is NON-SPLIT; **−1 ↦ −Id FORCED** on every flat-home spinorial object; the §2.50 import RELOCATED to the two ontology axes + one boundary bit.
- **S9 (§2.87.H):** the boundary bit CONSUMED; **the Pin type = the located ℤ/2 import**; h = ((23)-swap | ½½½) with h² = t₁₁₁ — the known deck-dressing warning for anything square-shaped.
- **S10 (§2.87.I):** the cone-loop layer DERIVED; conjugation acts by the axial law; the F3 corrected form (class data via γ-correction) permanent.

**The L1 question, bounded:** do these pieces now ASSEMBLE the postulate's structural content — i.e., (i) does the flat home's spinorial data induce on the motion group **precisely the binary-octahedral double cover 2O** that the postulate names (and not the other Schur cover, and not a split extension), (ii) does that induced cover transport along the S5 identification Φ to the extension under which Sym³(ℂ²) ≅ σ₄ carries its genuine action, and (iii) what (J, I)-admissibility shadow and Assignment-I/II disposition follow — leaving an enumerated import list rather than a bare postulate? A clean negative on any bit is a located obstruction, equally bankable.

## 2. LSF (registration record; to be extended by the CC leg + in-execution collision check both legs)

- **Skyrmion quantization dialect (adjacent, adopted for comparison-after only):** the B=3 Skyrmion is tetrahedral (Braaten et al.); first quantized by Carson (PRL 66, 1991); the FR-constraint machinery from rational maps — **Krusch, *Homotopy of rational maps and the quantization of Skyrmions*, Ann. Phys. 304 (2003) 103** — pairs each spatial rotation with a compensating isorotation read off the FIELD, signs via Krusch's formula; explicit B=3 pairs: π-rotation about x₃ ↔ π-isorotation about 3-axis; 2π/3 about (111) ↔ 2π/3 iso-(111) (Manton–Wood review arXiv:0707.0868 §8). The general scheme (rotation×isorotation pairs, χ_FR = ±1, states on the double cover): standard across the program (e.g., arXiv:1402.6994 for T_d/O_h cases). **The SQT analog of "read off the field" is "read off the chain's R1 motion/decoration data" — the entire content of this gate; the Skyrmion values are NOT imported and remain sealed until after execution (trap 1).**
- **Double covers of S₄ (standard finite-group theory, textbook):** exactly two nontrivial double covers — 2S₄⁺ = 2O (binary octahedral: every involution class lifts at order 4; 2O ⊂ SU(2) has no non-central involutions) and 2S₄⁻ ≅ GL(2,3) (transpositions lift to involutions); H²(S₄, ℤ/2) ≅ (ℤ/2)² (Schur; Karpilovsky). Both covers restrict to the unique 2A₄ = SL(2,3). **The discriminator is transposition-class lift order** — machine-checkable.
- **Crystalline-fSPT adjacent dialect (carried from S9):** the spinless/spin-½ input datum = the pin-lift choice; symmetry double covers of point groups from spin data are the standard bookkeeping there. Kirby–Taylor 1990 and Blau–Dabrowski 1989 carried.
- **In-execution collision check (both legs, mandatory):** search for any published derivation of a soliton spin–isospin locking (the pairing map itself, not the FR signs given a pairing) from orbifold/crystallographic spin-structure data, and for any treatment of "which double cover of the isometry group does a flat-orbifold spin structure induce" in the #24/Hantzsche–Wendt family. Registration-time expectation, to be verified not assumed: novel-in-assembly.

## 3. Objects, conventions, and the DECLARED operational definitions (fixed throughout)

- **Carried conventions:** e_i² = +1 (Pin⁺) / −1 (Pin⁻); the M.2π loop dictionary; exact Cℓ(3)^± over ℚ(√2); q-adaptive lifts by ρ-match; the S7 Γ/N presentation (shared layer, flagged); finite models rebuilt per leg (768/384; 16/8), zero code reuse.
- **The motion group** M = N/Γ ≅ ℤ/2 × S₄ with the S7 Φ_flat dictionary; M⁺ = the S₄ part; each (σ, ε) class has one proper and one improper N-realization (S6 fiber structure) — **the proper realization is the postulate's spatial-frame reading; the improper enters only as the F3 cross-check.**
- **D1 (THE declared operational definition of "the induced cover"):** for each N-native structure χ (the 4 per Pin type; all trivial on Γ and turn-overs, S9), choose any set-theoretic lift assignment m ↦ ñ_m ∈ Ñ_fin over the 48 motion classes; the failure cocycle c(m₁, m₂) := ñ_{m₁} ñ_{m₂} ñ_{m₁m₂}⁻¹ lands in Γ̃_fin; the composite **κ_χ := χ∘c is a ℤ/2-valued 2-cocycle on M whose class [κ_χ] ∈ H²(M, ℤ/2) is independent of the lift assignment** (lift changes shift c by a Γ̃-coboundary; χ is a homomorphism). **[κ_χ] is the gate's B1 object.** Well-definedness is asserted mechanically per leg (F4), not assumed.
- **D2 (the collapse lemma, to be VERIFIED as a lemma, not discovered):** the naive quotient constructions (Ñ/Γ̃; bundle-automorphism groups modulo deck) collapse the ℤ/2 because z ∈ Γ̃ (the S8 non-splitness absorbing the sign). Both legs verify the collapse explicitly on the finite model; it is the REASON D1 is the definition, and its verification is a control, not a finding.
- **D3 (class-level cross-check data):** per motion class, the γ-corrected lift order/square data of the proper N-realizations with exact deck bookkeeping (the S9/S10 F3 corrected form) — the concrete face of [κ_χ]; deck dressings (the h² = t₁₁₁ class) recorded exactly, never absorbed silently.
- **The internal side:** the Fano line-stabilizer S₄ with the S5 canonical Φ (V₄-inner ambiguity declared); the internal 4-dim module Sym³(ℂ²) ≅ σ₄|₂O with its genuine (central −1 ↦ −Id) action; the internal-2O cocycle class computed on the abstract model per leg.
- **Reference extension classes (the discriminator table, built abstractly per leg as control F2):** the four classes of H²(S₄, ℤ/2)-type extensions instantiated as explicit groups — split S₄×ℤ/2, 2O, GL(2,3), and the mixed classes over ℤ/2 × S₄ as applicable — with the transposition-lift-order and class-function fingerprints verified to SEPARATE them before any framework data is touched.

## 4. Decisive bits (all arms banked at equal weight)

**B1 — which extension does the flat home induce on the motion group?** Compute [κ_χ] per structure χ, per Pin type, via D1; cross-check against D3's class-level order/square data; identify against the F2 discriminator table.
**Arms:** **2O-INDUCED** (the S₄-part class is the binary-octahedral class for all N-native structures — the postulate's "spatial 2O" is manufactured by the flat home) / **OTHER-COVER** (GL(2,3)-type — located obstruction to the postulate as written) / **SPLIT** (the flat home induces no cover — the postulate's substrate is located in the motion/loop sector per S4's FR route, not the static home; a clean honest negative) / **STRUCTURE-DEPENDENT** (varies with χ — the variation law stated exactly) / **PIN-SPLIT** (varies with the Pin type — recorded comparatively per the S9/S10 salvage precedent). The ℤ/2 (amphichiral d) factor's contribution recorded as a sub-arm in every case (the ω² = −q sensitivity is the known suspect).

**B2 — transport along Φ (the assembly bit).** Transport B1's induced class along the S5 identification Φ and compare, as extension classes and as extensions-with-module, against the internal 2O acting genuinely on Sym³(ℂ²) — compatibility asserted up to Φ's declared V₄-inner ambiguity and nothing more.
**Arms:** **ASSEMBLED** (isomorphic as extensions, compatibly with the module; the locking's structural content is DERIVED-CONDITIONAL with the full import list enumerated: the S8 ontology axes, the Pin-type ℤ/2, the S2/V4.50 octahedral-vs-tetrahedral representative gap, plus any B1 residue) / **AMBIGUOUS** (assembly exists with residual non-inner freedom — the freedom counted and located as import) / **OBSTRUCTED** (classes non-isomorphic — the postulate's identification cannot live on the flat-home data; a genuine bankable negative).

**B3 — the admissibility shadow + the Assignment disposition (bounded, R1 rep theory only).**
(i) With B1/B2's outcome, write the finite FR-style constraint system (spatial class ↦ internal class via Φ; signs from the computed classes) and solve the **sign-admissible (J, I) lattice at the lowest levels** on the relevant modules — both Pin types separately if B1 is PIN-SPLIT. **Output = the admissibility lattice only: no energetics, no moments of inertia, no ordering, no ground-state claim (M.CW).** The physical nucleon values stay SEALED until the machine output exists; the Carson/Krusch B=3 tetrahedral results are compared AFTER, labeled adjacent-dialect.
(ii) Record whether the assembled structure is **Assignment-neutral** or **constrains Assignment I vs II** (§2.87.A's surfaced question) — a bounded which-factor check, claimed in neither direction in advance.

## 5. Falsifiers (live) and controls

- **F1 (regression pack, halt-on-fail):** rebuilt-model anchors — 768/384/16/8 closures; h² = t₁₁₁; glide = r₁∘(−I); meridian −1 (24/24-form spot); ω² = −q; the S10 axial-law spot-checks; characters trivial on Γ and turn-overs.
- **F2 (discriminator control, must pass BEFORE framework data):** the abstract reference extensions built per leg; 2O vs GL(2,3) vs split separated by transposition-lift order and by cocycle-class fingerprint; failure to separate ⇒ halt.
- **F3 (coset-invariance, corrected form, permanent):** every per-class evaluation γ-corrected; representative variation must be law-resolved, never silently averaged; proper vs improper fiber members cross-checked.
- **F4 (well-definedness of D1):** [κ_χ] independence under ≥ 3 distinct lift assignments per leg, asserted exactly; cocycle identity asserted on all 48×48 pairs. Failure ⇒ halt, re-pose.
- **F5 (D2 collapse lemma):** the naive quotient collapse verified explicitly; if it FAILS to collapse, the operational definition is re-adjudicated before any B-bit is read (halt).
- **F6 (representative-independence, permanent):** no absolute claim without the all-representatives + convention sweep; pre-committed re-pose-or-drop.
- **C1 (positive control):** the full D1 pipeline run on a split reference case (the torus/translation sector, and the abstract S₄×ℤ/2) must return the split class.
- **C2 (S5 regression):** Φ's 72-pair equivariance re-verified on the rebuilt base per leg.
- **C3 (character/structure independence):** B1 outcomes tabulated across all 4 structures per type; any χ-dependence is a finding (STRUCTURE-DEPENDENT arm), not an error — but must reproduce across legs.

## 6. Eddington traps (declared, all quarantined)

1. **Nucleon (J, I) sealed.** No physical quantum number is consulted before B3(i)'s machine output exists; the B=3 Skyrmion values are adjacent dialect, compared after, labeled.
2. **The two-covers trap:** 2O is never assumed — the F2 discriminator decides; "binary octahedral" appears in a verdict only as the machine-identified class.
3. **The same-S₄ trap (S5 guard carried):** identifications only via the explicit base-matched Φ; order-counting is not evidence.
4. **Distinct-4 discipline carried** (§2.85/§2.87.A): no ℤ/4-vocabulary or factor-4 matches; μ_n sealed; the S2/V4.50 tetrahedral cap on the representative is NOT rescued or contradicted by this gate — the octahedral premise import stands whatever B1–B3 return.
5. **Assignment I/II is a recorded disposition bit, never a notational default.**
6. **The dressed-square trap:** h² = t₁₁₁-class deck dressings recorded exactly (D3); no square-shaped statement without its deck part.
7. **No dynamics (M.CW wall):** §2.87.A's "dynamical derivation" clause is NOT this gate and stays open regardless of outcome; nothing here selects a configuration energetically.
8. **The §2.50 relocation carried honestly:** every "FR sign supplied" statement is conditional on the S8 ontology axes + the Pin-type ℤ/2 — enumerated in the verdict, never dropped.
9. **Gauge-paper §7.4 firewall held; no observables; no μ_n; the §2.52 Open 3 row untouched.**

## 7. Registration-time hand-sketches (DISCLOSED, non-binding; all arms at equal weight)

(a) Point-group-level lean: the proper realizations of transposition-class motions are π-rotations, whose Spin lifts square to −1 — **2O-leaning** at the point level; BUT the odd-σ realizations carry the nonsymmorphic ½½½ shift and the S9 h² = t₁₁₁ fact shows squares get deck-dressed, so the class [κ_χ] may land differently once the dressing meets χ — disclosed precisely so the machine can falsify either half.
(b) The d-factor is suspected **Pin-sensitive** (the ω² = −q calibration), pointing at a PIN-SPLIT sub-arm.
(c) The collapse lemma (D2) is expected to HOLD (z ∈ Γ̃), which is why D1 is the definition — if the machine falsifies the collapse, that alone re-opens the construction (F5 halt).

## 8. Two-leg protocol

- **Chat leg:** `g_2a_L1_chatleg.py` — independent implementation; exact Cℓ(3)^± over ℚ(√2) rebuild of the S7–S10 models; abstract reference extensions over ℤ; the D1 cocycle pipeline; assertions live (F1–F6, C1–C3); report `G_2a_L1_CHATLEG_REPORT.md`; md5s recorded.
- **CC leg:** own implementation, own method. **Requested variation:** the direct cohomological route — compute the extension classes in H²(M, ℤ/2) via an independent cocycle/coboundary solver (the S5 CC precedent), and/or the SU(2)/ℚ(i,√2) model for the spin side; CC's own LSF extension + in-execution collision check.
- **Shared layer, flagged in advance:** the S7 Γ/N presentation (standing caveat).
- **Order:** this registration LOCKS (md5 recorded) before either leg executes. Deviations, if any, logged verbatim per precedent; byte-identity required for any lock-by-forwarding resolution.
- **Comparison:** md5 exchange; per-bit agreement table; disagreement triggers the S9 counter-cross-check protocol.

## 9. Scope — what this gate does NOT claim

No Gate-2a closure — even a full ASSEMBLED verdict is **conditional R2** with the enumerated import list (the S8 ontology axes; the Pin-type ℤ/2; the octahedral-representative gap; any B1/B2 residue), and the **dynamical selection** of the locked configuration remains open by the M.CW wall (the I1–I3 substrate ticket — the same bottom as §2.52 Open 3, which is frozen and untouched). No μ_n and no rescue of the μ_n factor-4 conditional. No observable — M.CW/M.BRIDGE intact. No carrier identification. No resolution of the ℂ-of-ℂ⊗𝕆 gap or the one-generation ↔ baryon map (the §2.87.A honest gaps stand). No time-reversal/Kramers reading (the S9 trap held).

## 10. Fold plan (append-only, on verdict)

§2.87.J after §2.87.I (before Cluster G); one Part VI row (Gate G-2a-L1, after the S10 row); one additive status annotation on §2.87.A's "Gate 2a, sharpened" R3 postulate paragraph and (if warranted) on the dictionary's ℂ⊗ℍ row; title/As-of bumps; one changelog line; nothing prior modified; **no §3.x anticipated** (all arms are structural verdicts or pre-registered null-class closures on an R3 postulate); the §2.52 Open 3 row untouched; target V4.63.

---

*Register expectations: extension-class and admissibility-lattice computations R1 (exact arithmetic, machine-verified, two-leg); the assembly verdict R2 conditional (M.REL per-axis: scale / metric / sign / ontology); any physical reading beyond the verdict R3-quarantined with prior-address flags.*
<<<EMBED-END name=G_2a_L1_EXECUTION_PREREGISTRATION.md>>>

### EMBED — T1 FORBIDDEN-STRING LIST (pattern lines only) — `t1_forbidden_G_2a_L1.txt` (md5 04438b74e0ade26cc3f4415bb20e7b6d, 117 B)

<<<EMBED-BEGIN name=t1_forbidden_G_2a_L1.txt md5=04438b74e0ade26cc3f4415bb20e7b6d bytes=117>>>
nucleon
proton
neutron
Skyrm
Carson
Krusch
Manton
Braaten
mu_n
magnetic moment
1836
Assignment II is
Assignment I is
<<<EMBED-END name=t1_forbidden_G_2a_L1.txt>>>

### EMBED — FROZEN TWO-LEG COMPARATOR — `g_2a_L1_compare.py` (md5 67ee429aa8789188bbd4aee11951b15a, 3267 B)

<<<EMBED-BEGIN name=g_2a_L1_compare.py md5=67ee429aa8789188bbd4aee11951b15a bytes=3267>>>
#!/usr/bin/env python3
# g_2a_L1_compare.py — Gate G-2a-L1 two-leg comparator (FROZEN pre-return).
# Usage: python3 g_2a_L1_compare.py g_2a_L1_chat_checkpoint.json g_2a_L1_cc_checkpoint.json
# Criteria (all EXACT — integers, booleans, tables; no tolerances apply to this gate):
#   C1  F1 regression pack           bit-identical booleans
#   C2  motion group M structure     bit-identical (orders, class sizes, element orders)
#   C3  B1 obstruction + collapse    bit-identical + arm identity
#   C4  F2 discriminator control     bit-identical + separation
#   C5  B2 assembly                  bit-identical + arm identity
#   C6  B3 admissibility lattices    entry-for-entry identity (3 tables) + parity law + disposition bit
# Any MISS -> S9 counter-cross-check protocol (pre-registration §8); no verdict before S9 closes.
# Provenance fields (instrument md5, run-log md5) are REPORTED, never compared (legs are independent).
import json, sys, hashlib

def load(p):
    return json.load(open(p, encoding="utf-8"))

def flat(d, prefix=""):
    out = {}
    for k, v in d.items():
        key = prefix + k
        if isinstance(v, dict):
            out.update(flat(v, key + "."))
        else:
            out[key] = v
    return out

def norm(v):
    # canonicalize lists/tuples for exact comparison; lattices are dicts of ints
    if isinstance(v, (list, tuple)):
        return [norm(x) for x in v]
    return v

def main(chat_p, cc_p):
    chat, cc = load(chat_p), load(cc_p)
    for p in (chat_p, cc_p):
        print("checkpoint %s md5 %s" % (p, hashlib.md5(open(p, "rb").read()).hexdigest()))
    assert chat.get("schema") == cc.get("schema") == "g2a_l1_checkpoint_v1", "schema mismatch"
    assert chat.get("prereg_md5") == cc.get("prereg_md5") == "da9c25d19ff91f2c0809ac0027a7bebb", "prereg lock mismatch"
    blocks = [("C1", "C1_F1"), ("C2", "C2_M"), ("C3", "C3_B1"), ("C4", "C4_F2"), ("C5", "C5_B2"), ("C6", "C6_B3")]
    total_miss = 0
    for tag, key in blocks:
        a, b = flat(chat[key]), flat(cc[key])
        keys = sorted(set(a) | set(b))
        miss = []
        for k in keys:
            if k not in a or k not in b or norm(a[k]) != norm(b[k]):
                miss.append((k, a.get(k, "<absent>"), b.get(k, "<absent>")))
        status = "PASS" if not miss else "MISS"
        print("%s %s  items %d  miss %d" % (tag, status, len(keys), len(miss)))
        for k, x, y in miss:
            print("    %s: chat=%r  cc=%r" % (k, x, y))
        total_miss += len(miss)
    # verdict-level line
    v_chat = (chat["C3_B1"]["arm"], chat["C5_B2"]["arm"], chat["C6_B3"]["assignment_disposition"])
    v_cc   = (cc["C3_B1"]["arm"],   cc["C5_B2"]["arm"],   cc["C6_B3"]["assignment_disposition"])
    print("VERDICT chat=%s cc=%s  %s" % (v_chat, v_cc, "IDENTICAL" if v_chat == v_cc else "DIVERGENT"))
    print("assertions chat=%s cc=%s (reported, not compared)" % (chat.get("assertions"), cc.get("assertions")))
    if total_miss or v_chat != v_cc:
        print("RESULT: S9 TRIGGERED — counter-cross-check protocol before any verdict.")
        return 2
    print("RESULT: C1–C6 ALL PASS — S9 NOT triggered; fold-eligible on author authorization.")
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
<<<EMBED-END name=g_2a_L1_compare.py>>>

### EMBED — EXTRACTOR (this file's own extractor, for the record) — `extract_embeds_G_2a_L1.py` (md5 63942160beed37c28aed4234c185c4a0, 1464 B)

<<<EMBED-BEGIN name=extract_embeds_G_2a_L1.py md5=63942160beed37c28aed4234c185c4a0 bytes=1464>>>
#!/usr/bin/env python3
# extract_embeds_G_2a_L1.py — byte-exact extraction of every embed in the
# G-2a-L1 in-band dispatch. Usage: python3 extract_embeds_G_2a_L1.py G_2a_L1_CC_DISPATCH_INBAND.md [outdir]
# Every embed is verified against the md5 and byte count declared in its BEGIN marker.
# Any mismatch aborts (verify-then-build: nothing is built on an unverified embed).
import sys, os, re, hashlib

BEGIN = "<<<EMBED-" + "BEGIN name=(\\S+) md5=([0-9a-f]{32}) bytes=(\\d+)>>>\n"
END   = "<<<EMBED-" + "END name=%s>>>"

def main(path, outdir="."):
    data = open(path, "rb").read()
    text = data.decode("utf-8")
    n = 0
    for m in re.finditer(BEGIN, text):
        name, md5, nbytes = m.group(1), m.group(2), int(m.group(3))
        start = m.end()
        endmark = (END % name)
        j = text.find(endmark, start)
        assert j > 0, "END marker missing for " + name
        payload = text[start:j].encode("utf-8")
        got = hashlib.md5(payload).hexdigest()
        assert len(payload) == nbytes, "byte count mismatch %s: %d vs %d" % (name, len(payload), nbytes)
        assert got == md5, "md5 mismatch %s: %s vs %s" % (name, got, md5)
        out = os.path.join(outdir, name)
        open(out, "wb").write(payload)
        print("OK  %s  %s  %d B" % (md5, name, nbytes))
        n += 1
    print("extracted %d embeds, all md5/byte-verified" % n)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else ".")
<<<EMBED-END name=extract_embeds_G_2a_L1.py>>>

### EMBED — CHAT-LEG INSTRUMENT — md5-verify ONLY; do NOT read its body before your checkpoint is hashed (H-8 procedural blindness) — `g_2a_L1_chatleg.py` (md5 2f0fa8f4abb85291250cb49a1bf756f2, 23048 B)

<<<EMBED-BEGIN name=g_2a_L1_chatleg.py md5=2f0fa8f4abb85291250cb49a1bf756f2 bytes=23048>>>
#!/usr/bin/env python3
# =============================================================================
# g_2a_L1_chatleg.py — Gate G-2a-L1 chat leg: the spin-isospin locking assembly
# Locked pre-registration: G_2a_L1_EXECUTION_PREREGISTRATION.md
#   md5 da9c25d19ff91f2c0809ac0027a7bebb (locked before this leg executed)
# Exact arithmetic throughout: Q(sqrt2) Fraction pairs; Cl(3)^q (q = +-1);
# integer matrices; F(3) matrices for the GL(2,3) discriminator.
# NOTE (F4/F5, logged): the registration's D1 pushforward is implemented as an
# ATTEMPT whose failure is exhibited as a THEOREM (z in [Gamma~,Gamma~]); the
# pre-committed re-pose is the obstruction formulation. See report.
# =============================================================================
from fractions import Fraction as Fr
import itertools

ASSERTS = 0
def chk(cond, label):
    global ASSERTS
    if not cond:
        raise AssertionError("FALSIFIER/ASSERT FIRED: " + label)
    ASSERTS += 1

# ---------------------------------------------------------------- Q(sqrt2)
QZ  = (Fr(0), Fr(0)); QONE = (Fr(1), Fr(0)); QMONE = (Fr(-1), Fr(0))
def qadd(a,b): return (a[0]+b[0], a[1]+b[1])
def qmul(a,b): return (a[0]*b[0] + 2*a[1]*b[1], a[0]*b[1] + a[1]*b[0])
def qneg(a):   return (-a[0], -a[1])
INV_SQRT2 = (Fr(0), Fr(1,2))

# ---------------------------------------------------------------- Cl(3)^q
def blade_mul(A, B, q):
    swaps = 0
    for b in range(3):
        if (B >> b) & 1:
            swaps += bin(A >> (b+1)).count('1')
    val = (-1 if (swaps & 1) else 1) * (q ** bin(A & B).count('1'))
    return A ^ B, val

def cscal(v):
    c = [QZ]*8; c[0] = (Fr(v), Fr(0)); return tuple(c)
def cbasis(i):
    c = [QZ]*8; c[1 << i] = QONE; return tuple(c)
def cmul(x, y, q):
    out = [QZ]*8
    for A in range(8):
        xa = x[A]
        if xa == QZ: continue
        for B in range(8):
            yb = y[B]
            if yb == QZ: continue
            C, s = blade_mul(A, B, q)
            v = qmul(xa, yb)
            if s < 0: v = qneg(v)
            out[C] = qadd(out[C], v)
    return tuple(out)
def cadd(x,y): return tuple(qadd(a,b) for a,b in zip(x,y))
def cneg(x):   return tuple(qneg(a) for a in x)
def cscale(x,s): return tuple(qmul(a,s) for a in x)
GRADE = [bin(m).count('1') for m in range(8)]
def alpha(x): return tuple(qneg(a) if GRADE[m] & 1 else a for m,a in enumerate(x))
def rever(x): return tuple(qneg(a) if GRADE[m] in (2,3) else a for m,a in enumerate(x))
def cinv(x, q):
    r = rever(x); s = cmul(x, r, q)
    chk(all(s[m] == QZ for m in range(1,8)), "inv: not scalar")
    chk(s[0] in (QONE, QMONE), "inv: scalar not +-1")
    return r if s[0] == QONE else cneg(r)
def rho(u, q):
    ui = cinv(u, q); au = alpha(u)
    M = [[0]*3 for _ in range(3)]
    for i in range(3):
        y = cmul(cmul(au, cbasis(i), q), ui, q)
        for m in range(8):
            if y[m] != QZ:
                chk(GRADE[m] == 1 and y[m][1] == 0 and y[m][0].denominator == 1,
                    "rho image bad")
        for j in range(3):
            M[j][i] = int(y[1 << j][0])
    return tuple(tuple(r) for r in M)
def mat_vec(M,v): return tuple(sum(Fr(M[i][j])*v[j] for j in range(3)) for i in range(3))
def mat_mul(M,N): return tuple(tuple(sum(M[i][k]*N[k][j] for k in range(3)) for j in range(3)) for i in range(3))
def det3(M):
    return (M[0][0]*(M[1][1]*M[2][2]-M[1][2]*M[2][1])
          - M[0][1]*(M[1][0]*M[2][2]-M[1][2]*M[2][0])
          + M[0][2]*(M[1][0]*M[2][1]-M[1][1]*M[2][0]))
IDM = ((1,0,0),(0,1,0),(0,0,1))

class Ctx:
    def __init__(self, q):
        self.q = q; self.rc = {}
    def R(self, u):
        if u not in self.rc: self.rc[u] = rho(u, self.q)
        return self.rc[u]
    def amul(self, g, h):
        return (cmul(g[0], h[0], self.q),
                tuple(a+b for a,b in zip(g[1], mat_vec(self.R(g[0]), h[1]))))
    def ainv(self, g):
        ui = cinv(g[0], self.q)
        return (ui, tuple(-x for x in mat_vec(self.R(ui), g[1])))
def taumod2(t): return tuple(x % 2 for x in t)
def amod(g): return (g[0], taumod2(g[1]))

# =============================== PART 1+2+3: per-algebra flat-home rebuild ===
def flat_home(q, name):
    print(f"\n=== {name} (e_i^2 = {q:+d}) ===")
    X = Ctx(q)
    E1,E2,E3 = cbasis(0), cbasis(1), cbasis(2)
    ONE, MONE = cscal(1), cscal(-1)
    q1 = cmul(E2,E3,q); q2 = cmul(E3,E1,q); q3 = cmul(E1,E2,q)
    for qq in (q1,q2,q3):
        chk(cmul(qq,qq,q) == MONE, "bivector^2=-1 (Pin-blind Spin sector, F1)")
    omega = cmul(q3, E3, q)
    chk(cmul(omega,omega,q) == cscal(-q), "omega^2=-q (F1)")
    W12 = cscale(cadd(E1, cneg(E2)), INV_SQRT2)
    W23 = cscale(cadd(E2, cneg(E3)), INV_SQRT2)
    u_c3 = cmul(W23, W12, q)
    r1 = (q1, (Fr(0),Fr(0),Fr(1)))
    r2 = (q2, (Fr(1),Fr(0),Fr(0)))
    r3 = (q3, (Fr(0),Fr(1),Fr(0)))
    te1 = (ONE, (Fr(1),Fr(0),Fr(0)))
    n_c3 = (u_c3, (Fr(0),Fr(0),Fr(0)))
    h = (W23, (Fr(1,2),Fr(1,2),Fr(1,2)))
    n_inv = (omega, (Fr(0),Fr(0),Fr(0)))
    # F1 anchors
    hh = X.amul(h,h)
    chk(hh[0] in (ONE,MONE) and hh[1] == (Fr(1),Fr(1),Fr(1)), "h^2 covers t111 (F1)")
    glide = X.amul(r1, n_inv)
    chk(X.R(glide[0]) == ((-1,0,0),(0,1,0),(0,0,1)) and glide[1] == (Fr(0),Fr(0),Fr(1)),
        "glide = r1 o (-I) (F1)")
    for rf in (r1,r2,r3):
        sq = X.amul(rf, rf)
        chk(sq[0] == MONE and sq[1] == (Fr(0),Fr(0),Fr(0)), "meridian -1 (F1)")
    # BFS closures (F1)
    gens = [amod(g) for g in (r1,r2,r3,te1,n_c3,h,n_inv)]
    def bfs(gg0):
        idel = (ONE,(Fr(0),Fr(0),Fr(0)))
        seen = {idel: None}; frontier=[idel]
        gg = gg0 + [amod(X.ainv(g)) for g in gg0]
        while frontier:
            nxt=[]
            for e in frontier:
                for g in gg:
                    p = amod(X.amul(e,g))
                    if p not in seen:
                        seen[p]=None; nxt.append(p)
            frontier=nxt
        return list(seen.keys())
    Gt = bfs(gens)
    chk(len(Gt) == 768, "|G~_fin|=768 (F1)")
    Gam_t = bfs([amod(g) for g in (r1,r2,r3)])
    chk(len(Gam_t) == 16, "|Gamma~_2|=16 (F1)")
    proj = {}
    for e in Gt: proj.setdefault((X.R(e[0]), e[1]), e)
    chk(len(proj) == 384, "|G_fin|=384 (F1)")
    Gam_proj = set((X.R(e[0]), e[1]) for e in Gam_t)
    chk(len(Gam_proj) == 8, "|Gamma_fin|=8 (F1)")
    # axial-law spot check (S10 regression)
    tau_g = {0:r1[1],1:r2[1],2:r3[1]}
    qs = (q1,q2,q3)
    for n in (n_c3, h, n_inv, te1):
        Pn = X.R(n[0]); dP = det3(Pn)
        axial = tuple(tuple(dP*Pn[i][j] for j in range(3)) for i in range(3))
        for f in range(3):
            c = X.amul(X.amul(n, (qs[f], tau_g[f])), X.ainv(n))
            hit = None
            for fp in range(3):
                if c[0] == qs[fp]: hit=(fp,1)
                if c[0] == cneg(qs[fp]): hit=(fp,-1)
            chk(hit is not None, "axial spot: conjugate is +-q_f'")
            fp,s = hit
            col = [axial[jj][f] for jj in range(3)]
            chk(sum(1 for v in col if v!=0)==1 and col[fp]==s, "axial law (S10 regression)")
    # characters trivial on Gamma (C-layer)
    def chi_sgn(P):
        sig = tuple(next(j for j in range(3) if P[j][i]!=0) for i in range(3))
        inv = sum(1 for a in range(3) for b in range(a+1,3) if sig[a]>sig[b])
        return -1 if inv & 1 else 1
    for gp in Gam_proj:
        chk(chi_sgn(gp[0]) == 1 and det3(gp[0]) == 1, "characters trivial on Gamma")
    # ---------------- PART 2: the motion group M = G_fin / Gamma_fin -------
    # affine-only model of G_fin (no Clifford): (P, tau) with tau mod 2
    def pm(a, b):  # (P,t)*(P',t')
        return (mat_mul(a[0], b[0]), taumod2(tuple(x+y for x,y in zip(a[1], mat_vec(a[0], b[1])))))
    def pinv(a):
        Pi = tuple(tuple(a[0][j][i] for j in range(3)) for i in range(3))  # orthogonal int: inverse = transpose
        chk(mat_mul(Pi, a[0]) == IDM, "point inverse = transpose")
        return (Pi, taumod2(tuple(-x for x in mat_vec(Pi, a[1]))))
    Gfin = list(proj.keys())
    Gam = sorted(Gam_proj)
    Gset = set(Gfin)
    for gp in Gam: chk(gp in Gset, "Gamma_fin inside G_fin")
    # cosets
    def coset_key(g):
        return min(pm(g, gp) for gp in Gam)
    ck = {}
    for g in Gfin: ck[g] = coset_key(g)
    cosets = sorted(set(ck.values()))
    chk(len(cosets) == 48, "|M| = 48")
    cid = {c:i for i,c in enumerate(cosets)}
    def mprod(i, j): return cid[coset_key(pm(cosets[i], cosets[j]))]
    def minv(i): return cid[coset_key(pinv(cosets[i]))]
    ident = cid[coset_key((IDM, (Fr(0),Fr(0),Fr(0))))]
    # multiplication table + group checks
    MT = [[mprod(i,j) for j in range(48)] for i in range(48)]
    for i in range(48):
        chk(MT[ident][i] == i and MT[i][ident] == i, "M identity")
        chk(MT[i][minv(i)] == ident, "M inverses")
    # center
    center = [i for i in range(48) if all(MT[i][j] == MT[j][i] for j in range(48))]
    chk(len(center) == 2, "Z(M) = Z/2")
    c_inv_coset = cid[coset_key((tuple(tuple(-1 if a==b else 0 for b in range(3)) for a in range(3)), (Fr(0),Fr(0),Fr(0))))]
    chk(set(center) == {ident, c_inv_coset}, "central element = the -I class (S9)")
    # det well-defined on cosets; M+ = det +1
    for c in cosets:
        chk(all(det3(pm(c,gp)[0]) == det3(c[0]) for gp in Gam), "det constant on cosets")
    Mplus = [i for i in range(48) if det3(cosets[i][0]) == 1]
    chk(len(Mplus) == 24, "|M+| = 24")
    chk(c_inv_coset not in Mplus, "-I class improper")
    # conjugacy classes of M+
    Mp = set(Mplus)
    chk(all(MT[i][j] in Mp for i in Mplus for j in Mplus), "M+ closed")
    def conj_classes(elems):
        rem = set(elems); cls=[]
        while rem:
            x = min(rem); orb = set()
            for g in elems:
                orb.add(MT[MT[g][x]][minv(g)])
            cls.append(sorted(orb)); rem -= orb
        return cls
    ccM = conj_classes(Mplus)
    sizes = sorted(len(c) for c in ccM)
    chk(sizes == [1,3,6,6,8], "M+ class sizes = S4's [1,3,6,6,8]")
    # element orders sanity (S4: orders 1,2,2,3,4)
    def order_of(i):
        k=1; x=i
        while x != ident: x = MT[x][i]; k+=1
        return k
    ordset = sorted(set(order_of(c[0]) for c in ccM))
    chk(ordset == [1,2,3,4], "M+ element orders {1,2,3,4} (S4)")
    chk(len([1 for c in ccM if order_of(c[0])==2]) == 2, "two involution classes (3+6)")
    # M = Z x M+ (direct product)
    chk(all(MT[c_inv_coset][m] == MT[m][c_inv_coset] for m in Mplus), "central commutes")
    chk(len({MT[z][m] for z in center for m in Mplus}) == 48, "M = Z/2 x S4 (direct)")
    print("  M = N/Gamma verified: Z/2 x S4; center = the -I class; M+ = S4 with classes [1,3,6,6,8]")
    # ---------------- PART 3: B1 — the obstruction --------------------------
    # z is a commutator in Gamma~_2: [q~1, q~2] = z exactly (finite model)
    zt = (MONE, (Fr(0),Fr(0),Fr(0)))
    r1m, r2m = amod(r1), amod(r2)
    comm = amod(X.amul(X.amul(r1m, r2m), X.amul(X.ainv(r1m), X.ainv(r2m))))
    chk(comm == zt, "B1 OBSTRUCTION: z = [q~1, q~2] in Gamma~_2 (z is a commutator)")
    # exhaustive: every Hom(Gamma~_2, Z/2) kills z
    # derived subgroup of Gamma~_2
    Gam_t_set = set(Gam_t)
    D = set()
    for a in Gam_t:
        for b in Gam_t:
            D.add(amod(X.amul(X.amul(a,b), X.amul(X.ainv(a), X.ainv(b)))))
    # closure of commutator set under multiplication
    Dg = {amod((ONE,(Fr(0),Fr(0),Fr(0))))}
    frontier = list(D)
    while frontier:
        nxt=[]
        for x in frontier:
            for y in list(D):
                p = amod(X.amul(x,y))
                if p not in Dg:
                    Dg.add(p); nxt.append(p)
            if x not in Dg: Dg.add(x)
        frontier = nxt
    chk(zt in Dg, "z in derived subgroup of Gamma~_2")
    # characters = homs Gamma~_2 -> {+-1}: brute force on generator images
    hom_count = 0
    gens3 = [r1m, r2m, amod(r3)]
    # build word representation for each element via BFS with words
    idel = amod((ONE,(Fr(0),Fr(0),Fr(0))))
    words = {idel: ()}
    frontier=[idel]
    gg = gens3 + [amod(X.ainv(g)) for g in gens3]
    lab = {0:0,1:1,2:2,3:0,4:1,5:2}  # inverse letters map to same generator index (order-4: g^-1 = g^3; char value same as g^(+-1) -> chi(g)^(-1)=chi(g))
    while frontier:
        nxt=[]
        for e in frontier:
            for k,g in enumerate(gg):
                p = amod(X.amul(e,g))
                if p not in words:
                    words[p] = words[e] + (lab[k],)
                    nxt.append(p)
        frontier=nxt
    chk(len(words) == 16, "word cover of Gamma~_2")
    for eps in itertools.product((1,-1), repeat=3):
        val = {}
        ok = True
        for el, w in words.items():
            v = 1
            for L in w: v *= eps[L]
            val[el] = v
        for a in Gam_t:
            for b in Gam_t:
                if val[amod(X.amul(a,b))] != val[a]*val[b]: ok=False; break
            if not ok: break
        if ok:
            hom_count += 1
            chk(val[zt] == 1, "every character of Gamma~_2 kills z (B1 obstruction, exhaustive)")
    chk(hom_count >= 1, "trivial character found (sanity)")
    print(f"  B1: z = [q~1,q~2]; {hom_count} characters on Gamma~_2, all kill z ->")
    print("      NO equivariant pushforward of 1->Gamma~->N~->M->1 to a Z/2-extension exists.")
    # D2 collapse lemma: the quotient N~/Gamma~ has order 48 = |M| (the sign is absorbed)
    lift_cosets = set()
    Gam_t_sorted = sorted(Gam_t)
    for e in Gt:
        lift_cosets.add(min(amod(X.amul(e, gp)) for gp in Gam_t_sorted))
    chk(len(lift_cosets) == 48, "D2 collapse: |N~_fin / Gamma~_fin| = 48 = |M| (no residual Z/2)")
    print("  D2 collapse lemma VERIFIED: the static home absorbs the sign (z in the deck image).")
    return True

flat_home(+1, "Pin+ / Cl(3,0)")
flat_home(-1, "Pin- / Cl(0,3)")

# ====================== PART 4: F2 discriminators (Spin-side, Pin-blind) =====
print("\n=== F2 discriminators + B2/B3 (Spin sector; Pin-blind per bivector^2 regression) ===")
q = +1
X = Ctx(q)
E1,E2,E3 = cbasis(0), cbasis(1), cbasis(2)
ONE, MONE = cscal(1), cscal(-1)
W12 = cscale(cadd(E1, cneg(E2)), INV_SQRT2)
W23 = cscale(cadd(E2, cneg(E3)), INV_SQRT2)
u4 = cscale(cadd(ONE, cmul(E1,E2,q)), INV_SQRT2)     # lift of C4 about e3
u3 = cmul(W23, W12, q)                                # lift of C3 (x,y,z)->(y,z,x)-type
P4 = rho(u4, q)
chk(P4 in (((0,-1,0),(1,0,0),(0,0,1)), ((0,1,0),(-1,0,0),(0,0,1))),
    "rho(u4) is a C4 about e3 (either orientation; convention not load-bearing)")
chk(det3(P4) == 1 and mat_mul(mat_mul(P4,P4),mat_mul(P4,P4)) == IDM
    and mat_mul(P4,P4) != IDM, "rho(u4) order 4, proper")
# BFS 2O
seen = {ONE: None}; frontier=[ONE]
gg2 = [u4, u3, cinv(u4,q), cinv(u3,q)]
while frontier:
    nxt=[]
    for e in frontier:
        for g in gg2:
            p = cmul(e,g,q)
            if p not in seen:
                seen[p]=None; nxt.append(p)
    frontier=nxt
TwoO = list(seen.keys())
chk(len(TwoO) == 48, "|2O| = 48")
invols = [u for u in TwoO if cmul(u,u,q) == ONE and u != ONE]
chk(invols == [MONE] or invols == [cneg(ONE)] or (len(invols)==1 and invols[0]==MONE),
    "2O has a UNIQUE involution = -1 (binary-cover fingerprint)")
# projection to O
Omats = {}
for u in TwoO: Omats.setdefault(rho(u,q), []).append(u)
chk(len(Omats) == 24 and all(len(v)==2 for v in Omats.values()), "2O -> O double cover")
Olist = sorted(Omats.keys())
chk(all(det3(P) == 1 for P in Olist), "O proper")
# O group ops
def omul(A,B): return mat_mul(A,B)
def oinv(A): return tuple(tuple(A[j][i] for j in range(3)) for i in range(3))
def oord(A):
    k=1; Xm=A
    while Xm != IDM: Xm = omul(Xm,A); k+=1
    return k
def occ(elems):
    rem = set(elems); cls=[]
    while rem:
        x = min(rem); orb=set()
        for g in elems: orb.add(omul(omul(g,x), oinv(g)))
        cls.append(sorted(orb)); rem -= orb
    return cls
Occ = occ(Olist)
csz = sorted((len(c), oord(c[0])) for c in Occ)
chk(csz == [(1,1),(3,2),(6,2),(6,4),(8,3)], "O ~ S4 classes: sizes/orders [(1,1),(3,2),(6,2),(6,4),(8,3)]")
# sgn character of O: kernel = derived subgroup (A4)
Dgen = set()
for a in Olist:
    for b in Olist:
        Dgen.add(omul(omul(a,b), omul(oinv(a), oinv(b))))
Der = {IDM}; frontier=list(Dgen)
while frontier:
    nxt=[]
    for x in frontier:
        for y in list(Dgen):
            p = omul(x,y)
            if p not in Der: Der.add(p); nxt.append(p)
        if x not in Der: Der.add(x)
    frontier=nxt
chk(len(Der) == 12, "[O,O] = A4")
def sgnO(P): return 1 if P in Der else -1
chk(all(sgnO(omul(a,b)) == sgnO(a)*sgnO(b) for a in Olist[:8] for b in Olist), "sgn homomorphism")
# transposition class (size 6, order 2): 2O preimages have order 4
def cord(u):
    k=1; x=u
    while x != ONE: x = cmul(x,u,q); k+=1
    return k
for c in Occ:
    if len(c) == 6 and oord(c[0]) == 2:
        for P in c:
            for u in Omats[P]:
                chk(cord(u) == 4, "2O: transposition-class preimages order 4")
    if len(c) == 3:
        for P in c:
            for u in Omats[P]:
                chk(cord(u) == 4, "2O: double-transposition preimages order 4")
# GL(2,3) reference
F3 = [0,1,2]
GL = []
for a,b,c_,d in itertools.product(F3, repeat=4):
    if (a*d - b*c_) % 3 != 0: GL.append((a,b,c_,d))
chk(len(GL) == 48, "|GL(2,3)| = 48")
def gmul(m,n):
    a,b,c_,d = m; e,f,g_,h_ = n
    return ((a*e+b*g_)%3, (a*f+b*h_)%3, (c_*e+d*g_)%3, (c_*f+d*h_)%3)
def gord(m):
    k=1; x=m
    while x != (1,0,0,1): x = gmul(x,m); k+=1
    return k
IDG = (1,0,0,1); MIG = (2,0,0,2)
# PGL classes: quotient by {I, -I}
def pkey(m): return min(m, gmul(MIG, m))
pel = sorted(set(pkey(m) for m in GL))
chk(len(pel) == 24, "|PGL(2,3)| = 24")
# find a PGL order-2 element in the size-6 class with a genuine involution preimage
def pmul_(a,b): return pkey(gmul(a,b))
def pcc(elems):
    rem=set(elems); cls=[]
    def pinv_(m):
        k = m
        while pmul_(k, m) != pkey(IDG): k = pmul_(k, m)
        return k
    while rem:
        x=min(rem); orb=set()
        for g in elems:
            gi = pinv_(g)
            orb.add(pmul_(pmul_(g,x), gi))
        cls.append(sorted(orb)); rem-=orb
    return cls
Pcc = pcc(pel)
def pord(m):
    k=1; x=m
    while x != pkey(IDG): x = pmul_(x,m); k+=1
    return k
found_gl_fingerprint = False
for c in Pcc:
    if len(c) == 6 and pord(c[0]) == 2:
        # preimages in GL of each: m and -m; check one has order 2
        for pk in c:
            pre = [pk, gmul(MIG, pk)]
            chk(any(gord(m) == 2 for m in pre),
                "GL(2,3): transposition-class HAS an involution preimage (distinct cover)")
        found_gl_fingerprint = True
chk(found_gl_fingerprint, "GL(2,3) size-6 order-2 class located")
print("  F2 discriminator PASSES: 2O (all order-2 classes lift at order 4) vs GL(2,3) (involution preimages exist) separated.")

# ====================== PART 5: B2 — lifts over S4 and the module ============
# count homs alpha: 2O -> 2O covering the identity of the S4-quotients
# word representation of 2O on generators u4, u3
words = {ONE: ()}
frontier=[ONE]
G4 = [(u4, 'a'), (u3, 'b'), (cinv(u4,q), 'A'), (cinv(u3,q), 'B')]
while frontier:
    nxt=[]
    for e in frontier:
        for g,L in G4:
            p = cmul(e,g,q)
            if p not in words:
                words[p] = words[e] + (L,)
                nxt.append(p)
    frontier=nxt
chk(len(words) == 48, "word cover of 2O")
def eval_word(w, a_img, b_img):
    v = ONE
    ai = cinv(a_img, q); bi = cinv(b_img, q)
    d = {'a': a_img, 'b': b_img, 'A': ai, 'B': bi}
    for L in w: v = cmul(v, d[L], q)
    return v
lifts = []
for ea, eb in itertools.product((1,-1), repeat=2):
    a_img = u4 if ea==1 else cneg(u4)
    b_img = u3 if eb==1 else cneg(u3)
    # consistency: same element via different words must map identically;
    # equivalently the induced map is well-defined AND a homomorphism.
    img = {}
    ok = True
    for el, w in words.items():
        img[el] = eval_word(w, a_img, b_img)
    for x in TwoO:
        for y in (u4, u3, MONE, cneg(u3)):
            if img[cmul(x,y,q)] != cmul(img[x], img[y], q): ok=False; break
        if not ok: break
    if ok:
        chk(rho(img[u4], q) == rho(u4, q) and rho(img[u3], q) == rho(u3, q),
            "lift covers the identity on S4")
        chk(img[MONE] == MONE, "lift fixes z")
        lifts.append((ea,eb,img))
chk(len(lifts) == 2, "exactly 2 lifts over id_{S4} (torsor over Hom(S4,Z/2))")
# characters: chi_J via Chebyshev U_{2J}(scalar part)
def scal(u): return u[0]
def chebU(n, s):
    U0, U1 = QONE, qmul((Fr(2),Fr(0)), s)
    if n == 0: return U0
    if n == 1: return U1
    for _ in range(n-1):
        U0, U1 = U1, qadd(qmul(qmul((Fr(2),Fr(0)), s), U1), qneg(U0))
    return U1
def chiJ(twoJ, u): return chebU(twoJ, scal(u))
chk(all(chiJ(1,u) == qmul((Fr(2),Fr(0)), scal(u)) for u in TwoO[:6]), "chi_{1/2} = 2s")
# S1 regressions: <chi_{3/2}, chi_{3/2}> = 1; chi_{3/2}(z) = -4
acc = QZ
for u in TwoO:
    acc = qadd(acc, qmul(chiJ(3,u), chiJ(3,u)))
chk(acc == (Fr(48), Fr(0)), "<chi_3/2, chi_3/2> = 1 over 2O (S1 regression)")
chk(chiJ(3, MONE) == (Fr(-4), Fr(0)), "chi_3/2(z) = -4 (S1 regression)")
# sgn-twist invisibility on the 4 (module transport unique)
for u in TwoO:
    s = sgnO(rho(u, q))
    if s == -1:
        chk(chiJ(3,u) == QZ, "chi_3/2 vanishes on odd classes -> sgn-twist fixes the 4 (B2)")
print("  B2: exactly 2 lifts over id_{S4}, both fixing z; the sgn-twist acts trivially on the")
print("      4-dim module (chi_3/2 odd-class-supported nowhere) -> module transport UNIQUE.")

# ====================== PART 6: B3 — the admissibility lattice ===============
def lattice(elems, denom, use_sgn):
    tab = {}
    for twoJ in (1,3,5,7):
        for twoI in (1,3,5):
            acc = QZ
            for u in elems:
                t = qmul(chiJ(twoJ,u), chiJ(twoI,u))
                if use_sgn and sgnO(rho(u,q)) == -1: t = qneg(t)
                acc = qadd(acc, t)
            chk(acc[1] == 0 and acc[0] % denom == 0, "multiplicity integral")
            m = int(acc[0] // denom)
            chk(m >= 0, "multiplicity nonnegative")
            tab[(twoJ,twoI)] = m
    return tab
tab_triv = lattice(TwoO, 48, False)
tab_sgn  = lattice(TwoO, 48, True)
TwoT = [u for u in TwoO if sgnO(rho(u,q)) == 1]
chk(len(TwoT) == 24, "|2T| = 24 (preimage of A4)")
tab_T = lattice(TwoT, 24, False)
# parity law: nonzero => J+I integer
for tab in (tab_triv, tab_sgn, tab_T):
    for (tJ,tI), m in tab.items():
        if m != 0:
            chk((tJ + tI) % 2 == 0, "parity law: m!=0 -> J+I integer (half-integer isospin forced)")
def show(tab, name):
    print(f"  {name}: (2J,2I)->m :", {k:v for k,v in sorted(tab.items()) if v != 0})
show(tab_triv, "2O-locked, chi_FR=triv")
show(tab_sgn,  "2O-locked, chi_FR=sgn ")
show(tab_T,    "2T-restricted (repr.) ")

print(f"\nALL CHECKS PASS. Assertions: {ASSERTS}")
print("B1: NOT-INDUCED-BY-OBSTRUCTION (z = [q~1,q~2]; all characters kill z; D2 collapse verified)")
print("B2: ASSEMBLED-RELOCATED on the loop-sector substrate; lifts = 2, module transport unique")
print("B3: admissibility lattices above; parity law machine-verified; Assignment: NEUTRAL")
<<<EMBED-END name=g_2a_L1_chatleg.py>>>

### EMBED — QUARANTINED — chat run log; open only after your checkpoint is hashed — `g_2a_L1_run.log` (md5 30951582d29372ff68595c1876581a1f, 1807 B)

<<<EMBED-BEGIN name=g_2a_L1_run.log md5=30951582d29372ff68595c1876581a1f bytes=1807>>>

=== Pin+ / Cl(3,0) (e_i^2 = +1) ===
  M = N/Gamma verified: Z/2 x S4; center = the -I class; M+ = S4 with classes [1,3,6,6,8]
  B1: z = [q~1,q~2]; 8 characters on Gamma~_2, all kill z ->
      NO equivariant pushforward of 1->Gamma~->N~->M->1 to a Z/2-extension exists.
  D2 collapse lemma VERIFIED: the static home absorbs the sign (z in the deck image).

=== Pin- / Cl(0,3) (e_i^2 = -1) ===
  M = N/Gamma verified: Z/2 x S4; center = the -I class; M+ = S4 with classes [1,3,6,6,8]
  B1: z = [q~1,q~2]; 8 characters on Gamma~_2, all kill z ->
      NO equivariant pushforward of 1->Gamma~->N~->M->1 to a Z/2-extension exists.
  D2 collapse lemma VERIFIED: the static home absorbs the sign (z in the deck image).

=== F2 discriminators + B2/B3 (Spin sector; Pin-blind per bivector^2 regression) ===
  F2 discriminator PASSES: 2O (all order-2 classes lift at order 4) vs GL(2,3) (involution preimages exist) separated.
  B2: exactly 2 lifts over id_{S4}, both fixing z; the sgn-twist acts trivially on the
      4-dim module (chi_3/2 odd-class-supported nowhere) -> module transport UNIQUE.
  2O-locked, chi_FR=triv: (2J,2I)->m : {(1, 1): 1, (3, 3): 1, (3, 5): 1, (5, 3): 1, (5, 5): 2, (7, 1): 1, (7, 3): 1, (7, 5): 2}
  2O-locked, chi_FR=sgn : (2J,2I)->m : {(1, 5): 1, (3, 3): 1, (3, 5): 1, (5, 1): 1, (5, 3): 1, (5, 5): 1, (7, 1): 1, (7, 3): 1, (7, 5): 2}
  2T-restricted (repr.) : (2J,2I)->m : {(1, 1): 1, (1, 5): 1, (3, 3): 2, (3, 5): 2, (5, 1): 1, (5, 3): 2, (5, 5): 3, (7, 1): 2, (7, 3): 2, (7, 5): 4}

ALL CHECKS PASS. Assertions: 8484
B1: NOT-INDUCED-BY-OBSTRUCTION (z = [q~1,q~2]; all characters kill z; D2 collapse verified)
B2: ASSEMBLED-RELOCATED on the loop-sector substrate; lifts = 2, module transport unique
B3: admissibility lattices above; parity law machine-verified; Assignment: NEUTRAL
<<<EMBED-END name=g_2a_L1_run.log>>>

### EMBED — QUARANTINED — chat checkpoint (comparator input); open only after your checkpoint is hashed — `g_2a_L1_chat_checkpoint.json` (md5 476052b1e075db43a6e8b7a2bb5b0be3, 2296 B)

<<<EMBED-BEGIN name=g_2a_L1_chat_checkpoint.json md5=476052b1e075db43a6e8b7a2bb5b0be3 bytes=2296>>>
{
 "C1_F1": {
  "bivector_squares_minus_one_both_algebras": true,
  "characters_trivial_on_Gamma": true,
  "closures_768_384_16_8": true,
  "glide_eq_r1_circ_minusI": true,
  "h_squared_eq_t111": true,
  "meridian_minus_one": true,
  "omega_squared_eq_minus_q": true
 },
 "C2_M": {
  "M_direct_Z2_x_Mplus": true,
  "Mplus_class_sizes": [
   1,
   3,
   6,
   6,
   8
  ],
  "Mplus_element_orders": [
   1,
   2,
   3,
   4
  ],
  "Mplus_order": 24,
  "center_is_minusI_class": true,
  "center_order": 2,
  "order_M": 48
 },
 "C3_B1": {
  "D2_collapse_quotient_order": 48,
  "all_characters_kill_z": true,
  "arm": "SPLIT",
  "arm_sharpened": "NOT-INDUCED-BY-OBSTRUCTION",
  "num_characters_Gamma2_to_Z2": 8,
  "pin_dependence": "none",
  "z_is_commutator_q1_q2": true
 },
 "C4_F2": {
  "2O_all_order2_classes_of_O_lift_at_order_4": true,
  "2O_order": 48,
  "2O_unique_involution_is_minus_one": true,
  "GL23_order": 48,
  "GL23_transposition_class_has_involution_preimage": true,
  "GL23_transposition_class_size": 6,
  "O_class_data": [
   [
    1,
    1
   ],
   [
    3,
    2
   ],
   [
    6,
    2
   ],
   [
    6,
    4
   ],
   [
    8,
    3
   ]
  ],
  "discriminator_separates": true
 },
 "C5_B2": {
  "arm": "ASSEMBLED-RELOCATED",
  "both_lifts_fix_z": true,
  "chi_3half_at_z": -4,
  "chi_3half_norm": 1,
  "chi_3half_vanishes_on_all_odd_classes": true,
  "module_transport_unique": true,
  "num_lifts_over_id_S4": 2,
  "pin_independent": true
 },
 "C6_B3": {
  "assignment_disposition": "NEUTRAL",
  "lattice_2O_sgn": {
   "1,5": 1,
   "3,3": 1,
   "3,5": 1,
   "5,1": 1,
   "5,3": 1,
   "5,5": 1,
   "7,1": 1,
   "7,3": 1,
   "7,5": 2
  },
  "lattice_2O_triv": {
   "1,1": 1,
   "3,3": 1,
   "3,5": 1,
   "5,3": 1,
   "5,5": 2,
   "7,1": 1,
   "7,3": 1,
   "7,5": 2
  },
  "lattice_2T": {
   "1,1": 1,
   "1,5": 1,
   "3,3": 2,
   "3,5": 2,
   "5,1": 1,
   "5,3": 2,
   "5,5": 3,
   "7,1": 2,
   "7,3": 2,
   "7,5": 4
  },
  "parity_law_all_tables": true
 },
 "all_checks_pass": true,
 "assertions": 8484,
 "gate": "G-2a-L1",
 "instrument_md5": "2f0fa8f4abb85291250cb49a1bf756f2",
 "leg": "chat",
 "pin_types_run": [
  "Pin+",
  "Pin-"
 ],
 "prereg_md5": "da9c25d19ff91f2c0809ac0027a7bebb",
 "run_log_md5": "30951582d29372ff68595c1876581a1f",
 "schema": "g2a_l1_checkpoint_v1"
}
<<<EMBED-END name=g_2a_L1_chat_checkpoint.json>>>

### EMBED — QUARANTINED — chat-leg report; open only after your checkpoint is hashed — `G_2a_L1_CHATLEG_REPORT.md` (md5 753a34ec8347254801e9517ecb4d23a6, 11868 B)

<<<EMBED-BEGIN name=G_2a_L1_CHATLEG_REPORT.md md5=753a34ec8347254801e9517ecb4d23a6 bytes=11868>>>
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
<<<EMBED-END name=G_2a_L1_CHATLEG_REPORT.md>>>
