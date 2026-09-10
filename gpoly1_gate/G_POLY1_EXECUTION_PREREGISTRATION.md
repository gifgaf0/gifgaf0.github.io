# G-POLY1 EXECUTION PRE-REGISTRATION — LOCKED

**Locked:** August 1, 2026, author word "Lock it." against staging memo `staging_memo_G_POLY1_promotion.md` md5 `68623d68306b361bf48b738b794a3650` (14,512 B), base canonical V4.73 md5 `e48f5c52d91a9fb14fb13076ee394263` (1,384,536 B, verified in-session). Sealed anchors: `anchors_G_POLY1_SEALED.md` md5 `a1d19dd98151cd7299af41fb14584c6f` (2,470 B) — Phase-3 mapper only.
**Elections (T3-immutable):** E1 {step, gem8} true-optimum + cubic frozen-labelled sensitivity; E2 single-phase endpoints verdict-bearing, f_hcp ∈ {0, ½, 1} reported, two-phase covariance annotated non-verdict; E3 SK-1984/Weaver-1990 class per the pin below; E4 HS 1962 mandatory + Hill point (verdict speeds = Hill; HS bands = reported uncertainty); E5 path-random RMS residual estimator; E6 anchors as sealed, A-1 verdict-bearing; E7 thresholds below; E8 JSON checkpoint per completed phase; E9 verdict classes per staging memo §10, exact.

## Phases (order fixed; checkpoint at each completion)

- **Phase 0a** — VRH + A^U + containment vs banked values + mixture spans. Checkpoint `poly1_phase0.json`. Executable now on ledger-quoted inputs (below).
- **Phase 0b** — Hashin–Shtrikman bounds. **Gated on HS-PIN** (below). Must complete before Phase 3; does not block Phase 1.
- **Phase 1** — orientation covariance ⟨δC⊗δC⟩ + dimensionless Rayleigh coefficient Q_T + α_T·ℓ surface. **Gated on E3-PIN-COMPLETE** (below). Checkpoint `poly1_phase1.json`.
- **Phase 2** — finite-d/λ path-random residual estimator (E5), prefactor from Phase-1 covariance + the banked directional spreads. R2-estimate. Checkpoint `poly1_phase2.json`.
- **Phase 3** — QUARANTINED overlay, sole reader of the sealed anchor file, runs only after `poly1_phase0/1/2.json` exist and are hashed. Unit map via the standing transverse-scale import only. Checkpoint `poly1_phase3.json`.

## E3-PIN v1 (locked this session; transcription source open-access)

- **Correlation model:** exponential two-point SAF P(r) = e^(−r/a); spectrum P̃(k) = 8πa³/(1+k²a²)²; grain-diameter convention **d = 2a** — transcribed from He, arXiv:1706.09137, Eqs. (70), (71) and the (94)–(95) convention statement. The a/d convention factor is thereby FIXED (χ = 1/2), not a knob.
- **Dispersion-equation class:** transverse coherent wave k² − ω²/V̄_T² − M_T(k) = 0, M_T = M_TL + M_TT, FOSA/Born (He Eqs. (91), (96)–(97), with the Im-part integrals (104)–(105)); Weaver JMPS 38, 55 (1990) lineage; numerically identical dispersion to Stanke–Kino JASA 75, 665 (1984) per the published record (He §I; JASA 149, 2377 (2021)). α_T = Im k; Rayleigh limit = ka ≪ 1 asymptote of the Born mass operators (quartic law).
- **E3-PIN-COMPLETE (blocks Phase 1):** the polycrystal orientation-covariance instantiation — the eighth-rank ⟨δC⊗δC⟩ contractions entering M_TL/M_TT for single-phase untextured aggregates (cubic per Weaver 1990; hexagonal per the published generalization line, JASA 143, 219 (2018) refs / Yang et al.) — must be transcribed VERBATIM from source with equation numbers, hashed, and logged BEFORE any Phase-1 evaluation. Both legs independently derive the orientation covariance from the locked tensors and verify against the transcribed contraction identities. Any convention conflict between sources is resolved and documented pre-evaluation (E2-witness class). No post-hoc formalism switching.

## HS-PIN (blocks Phase 0b)

Cubic HS-1962 closed forms and hexagonal HS bounds (Peselnick–Meister 1965; Watt–Peselnick JAP 51, 1525 (1980) line) transcribed verbatim from source, with equation numbers, hashed, logged, BEFORE evaluation. No from-memory coefficients — the isotropy-limit degeneracy check is necessary but not sufficient, so transcription is mandatory.

## Input provenance (Phase 0a)

Transcribed from the V4.73 canonical text (all constants C/ρ; v_T = √G; substrate units):
- **step:AB hex (complete):** C11 238.42, C12 108.54, C13 57.48, C33 287.67, C44 60.03, C66 64.92 (V4.72 §2.91.L true-optimum record; identity residual 0.0269% quoted).
- **gem8:FCC cubic (complete):** C11 272.08, C12 179.38, C44 131.54 (Zener 2.838; V4.73 fresh polished-at-frozen measurement).
- **step:FCC cubic (G-sector):** C44 85.29, C′ 36.73 (Zener 2.322); C11, C12 individually not quoted → K and HS unavailable this leg.
- **gem8:AB hex: INPUT-GAP** — only C44 84.82, C66 88.68 quoted; {C11, C12, C13, C33} absent from the canonical text. Endpoint v_T = 10.0417 (quoted) used ONLY for the mixture-span containment, labelled derived-input.
- **Containment targets (quoted):** step hex 8.4191 [8.2883, 8.5478], A^U 0.318; gem8 cubic 9.3079 [8.7068, 9.8725], A^U 1.428; step cubic 7.7990 [7.4689, 8.1158], A^U 0.904; gem8 hex 10.0417; mixture spans 7.65/7.59% (mean-normalized).
- **Full-precision request (X-1):** `poly_vrh_results.json` (md5 `200e7a8b…`) and/or the V4.72 true-optimum data artifact (`18d826a7…`) into project knowledge. Quoted-precision containment governs this leg (tolerances below); the C2 full-precision criterion closes at the two-leg comparison on identical transcribed inputs.

## Thresholds & falsifiers

Containment (this leg, quoted precision): 5-sig-fig targets rel ≤ 2×10⁻⁴; 3-sig-fig (A^U) rel ≤ 5×10⁻³; spans rel ≤ 2×10⁻². Two-leg: C1 ≤ 1×10⁻⁸ (closed-form algebra, identical inputs); C2 ≤ 1×10⁻⁶ (vs `200e7a8b` when available); C3 ≤ 1×10⁻⁸; C4 ≤ 1×10⁻⁶; C5 exponent exact, prefactor ≤ 5%; C6 verdict-class identity. S9 on any miss. F-1 FAIL-EMPTY / F-2 KNOB-SPLIT / F-3 BIR-EXCESS / F-4 REDUCTION (not triggered at staging) / F-5 CONTAINMENT-HALT per staging memo §10. H-items G-POLY1.H-n.

## T1

Forbidden-string list per the sealed anchor file, checked by external grep at every Phase-0/1/2 instrument invocation; hit = halt + H-item. The sealed file is read by nothing except the Phase-3 mapper and the author.
