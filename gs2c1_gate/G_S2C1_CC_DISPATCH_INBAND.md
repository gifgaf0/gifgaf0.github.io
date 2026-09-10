# G-S2C1 (Gate G-S2-ON-CONE) — CC-LEG DISPATCH (IN-BAND, P-4 + P-4.b)
## Single-crystal S2-on-cone ladder — leg 2 of 2

**Dispatch date:** September 3, 2026 (author directive; the author's act of placing this file in the CC repo constitutes the dispatch).
**P-4:** one self-contained file; every artifact embedded byte-exact with md5 + byte count; no side-channel message is load-bearing. **P-4.b (first use):** all QUARANTINED embeds travel base64-armored so that no viewer or pager can render them in the clear; the extractor writes them to `QUARANTINE/` and you do not decode, open, or read them until your own checkpoint is hashed and committed.
**Lock chain (all embedded raw, CC-facing):** prereg 2ea8ec13 (12,984 B) LOCKED Sept 2; lock record f2f4d500 (E-0..E-8 T3; M-naive expectation DISPERSIVE registered pre-data); Addendum A-1 8bf51bd0 (WARD-Γ redefined); Addendum A-2 a9bda086 (F-CONV regime-appropriate; c-free joint estimator over a common floor-clean rung set); T1 8cd89b9a frozen. No new elections.

## 0. Embed manifest (verify all 23 before anything else)
| Embed | md5 | bytes | enc | quarantine |
|---|---|---|---|---|
| `activation_G_S2C1.json` | 7a37816df1bd076636d5c78ab7d04b1e | 3536 | raw | no |
| `G_S2_ON_CONE_EXECUTION_PREREGISTRATION.md` | 2ea8ec13ffa3c32898cc24a3be605c64 | 12984 | raw | no |
| `G_S2_ON_CONE_LOCK_RECORD.md` | f2f4d50029fb5be3122a885c48a7e04f | 3009 | raw | no |
| `G_S2_ON_CONE_LOCK_RECORD_ADDENDUM_A1.md` | 8bf51bd05c691f3f03d796b231cdd262 | 1019 | raw | no |
| `G_S2_ON_CONE_LOCK_RECORD_ADDENDUM_A2.md` | a9bda086213ee0afe1e2ba01055659cd | 1950 | raw | no |
| `t1_forbidden_G_S2_ON_CONE.txt` | 8cd89b9a82704accd89f7ff6f5e220b4 | 144 | raw | no |
| `g_s2c1_compare.py` | e730844e9cf9e722e0e7789f90f34489 | 4643 | raw | no |
| `extract_embeds_v2.py` | d4ac62219a95bea1e29d226e371ee39a | 2102 | raw | no |
| `s2c1_chat_cmp_checkpoint.json` | 2aa66ea21dd5cda16535d409654fe4dd | 2164 | b64 | **YES** |
| `g_s2c1_phase0_close.py` | 1882c941fc4288b031131fb8aacccf83 | 11719 | b64 | **YES** |
| `g_s2c1_phase1.py` | c987a1a6f3ec8c3308dfb3bb1279bb09 | 17227 | b64 | **YES** |
| `g_s2c1_phase1_ladder.py` | a9949649af4a2e99e3ae69186a066c23 | 21163 | b64 | **YES** |
| `s2c1_phase1_ladder_analysis.py` | a55b0544d3c5ce7ab050a4af01492b4e | 3134 | b64 | **YES** |
| `gz1_core.py` | 361b1743a9164d1f7ff2380f6b74840d | 18205 | b64 | **YES** |
| `g_s2c1_phase0_checkpoint.json` | eae2bbd734f5129dd1e51efcbb55dd3d | 4555 | b64 | **YES** |
| `g_s2c1_phase1_checkpoint.json` | eeedcfa594a24915fa9c10c6abbd0a4e | 2477 | b64 | **YES** |
| `g_s2c1_phase1_ladder_checkpoint.json` | 5ee152fc14ac55e72094fc660aff7a4a | 43647 | b64 | **YES** |
| `s2c1_phase1_ladder_analysis.json` | bdfd3d01bc3f4cef0e22232bb7ff7eb5 | 6507 | b64 | **YES** |
| `s2c1_phase1_A2_evaluation.json` | 77fea65fde95efd33d8990956c7c07ff | 2934 | b64 | **YES** |
| `G_S2C1_PHASE0_REPORT.md` | 5f678490ed33040705c372065cfd1124 | 6556 | b64 | **YES** |
| `G_S2C1_PHASE1_HALT_REPORT.md` | b0e6790c323764d7e93350d2b5ef09a8 | 4107 | b64 | **YES** |
| `G_S2C1_PHASE1_LADDER_REPORT.md` | 6995cee96c9e696241b038a709dabcaf | 5341 | b64 | **YES** |
| `psi0_gem8_n64.npy` | a56796186e5eaf78c2e513fc710cb143 | 32896 | b64 | **YES** |

## 1. Verify-then-build (Phase 0)
Save the extractor below as `extract_embeds_v2.py` (also embedded raw). Run `python3 extract_embeds_v2.py G_S2C1_CC_DISPATCH_INBAND.md .` — it must print 23 `OK` lines; the 15 quarantined items land in `./QUARANTINE/` still unread. Any assertion failure ⇒ HALT and report. Write `cc_phase0.json` (embed table + prereg md5). Read the prereg, the lock record, and both addenda IN FULL; they are the objects of record and this dispatch adds procedure only.

```python
#!/usr/bin/env python3
# extract_embeds_v2.py — byte-exact extraction of every embed in a P-4 dispatch, with P-4.b base64 armor.
# Usage: python3 extract_embeds_v2.py <dispatch.md> [outdir] [--quarantine-dir DIR]
# Markers:  <<<EMBED-BEGIN name=NAME md5=HEX bytes=N enc=raw|b64 quarantine=0|1>>>  ...  <<<EMBED-END name=NAME>>>
# raw: payload is the file's UTF-8 text verbatim (file must end with a newline).  b64: payload is base64 (76-col lines).
# Every embed is verified against md5 + byte count; any mismatch aborts. quarantine=1 embeds are written to the
# quarantine dir (default ./QUARANTINE) and MUST NOT be opened before the CC checkpoint is hashed (procedural blindness).
import sys, os, re, base64, hashlib
BEGIN = "<<<EMBED-" + "BEGIN name=(\\S+) md5=([0-9a-f]{32}) bytes=(\\d+) enc=(raw|b64) quarantine=([01])>>>\n"
END = "<<<EMBED-" + "END name=%s>>>"
def main(path, outdir=".", qdir=None):
    qdir = qdir or os.path.join(outdir, "QUARANTINE"); os.makedirs(outdir, exist_ok=True); os.makedirs(qdir, exist_ok=True)
    text = open(path, "rb").read().decode("utf-8"); n = 0
    for m in re.finditer(BEGIN, text):
        name, md5, nbytes, enc, q = m.group(1), m.group(2), int(m.group(3)), m.group(4), m.group(5) == "1"
        j = text.find(END % name, m.end()); assert j > 0, "END marker missing: " + name
        seg = text[m.end():j]
        payload = seg.encode("utf-8") if enc == "raw" else base64.b64decode("".join(seg.split()))
        assert len(payload) == nbytes, "byte count mismatch %s: %d vs %d" % (name, len(payload), nbytes)
        assert hashlib.md5(payload).hexdigest() == md5, "md5 mismatch: " + name
        dest = os.path.join(qdir if q else outdir, name); open(dest, "wb").write(payload)
        print("OK  %s  %s  %d B  %s%s" % (md5, name, nbytes, enc, "  [QUARANTINE]" if q else "")); n += 1
    print("extracted %d embeds, all md5/byte-verified" % n)
if __name__ == "__main__":
    a = sys.argv[1:]; qd = None
    if "--quarantine-dir" in a: i = a.index("--quarantine-dir"); qd = a[i + 1]; a = a[:i] + a[i + 2:]
    main(a[0], a[1] if len(a) > 1 else ".", qd)
```

## 2. What you compute (own stack; the activation flags carry the exact parameters)
- **Phase 1 — crystallize:** the gem8 p6m single crystal at FIXED μ = 53.225 by your own solver, to ‖Lψ₀‖/‖ψ₀‖ ≤ 10⁻¹⁰; report ⟨ρ⟩ (it is a prediction of the record tuple, not an input), energy, spectral tail, λ_min(L) at Γ. `cc_phase1.json`.
- **Phase 2 — WARD-Γ (A-1):** (a) analytic-mode Ward residual on ∂ₓψ₀, ∂ᵧψ₀ ≤ 10⁻⁹; (b) Hermitian-form Goldstone |ω²| ≤ 10⁻⁸ with λ_min(L) ≥ −10⁻¹². Product-form values reported alongside. Halt on failure. `cc_phase2.json`.
- **Phase 3 — ladder (E-4) at three resolutions:** both directions; per rung: the S2 branch (max o₂, R², grad share), ω_T, the two compressional branches, product-form cross-checks at ka = 0.3 and 0.01875; λ_min(L) tracked at every k. `cc_phase3_<res>.json` per resolution (write each as it completes).
- **Phase 4 — estimator (A-2), falsifiers, arm:** common floor-clean rung set; joint fit; F-CONV(A-2) across your resolutions; F-ISO; F-MIX; F-DISP at τ; arm per prereg §5 — decided by your numbers BEFORE any quarantine is opened. `cc_phase4.json`.
- **Phase 5 — checkpoint:** `s2c1_cc_cmp_checkpoint.json` in schema `s2c1_cmp_v1` with EXACTLY the chat checkpoint's blocks and keys (schema, gate, leg="cc", prereg_md5, addenda_md5, source_md5, C1_substrate, C2_ward_A1, C3_speeds[GK,GM], C3_F_ISO, C4_F_MIX, C5_F_DISP[GK,GM], C6_arm, registered_expectation) — the key list is reproduced in §3. Hash it, commit it, record the commit. ONLY THEN decode the quarantine, run `python3 g_s2c1_compare.py QUARANTINE/s2c1_chat_cmp_checkpoint.json s2c1_cc_cmp_checkpoint.json`, and write your report.

## 3. Checkpoint schema s2c1_cmp_v1 (keys; values are yours)
C1_substrate: kernel_U0, g_star, a_star, mu_fixed, mean_rho, residual_rel, residual_le_1e-10, lambda_min_L_Gamma_ge_minus1e-12, resolution_of_record
C2_ward_A1: pass_a_analytic, pass_b_hermitian, analytic_ward_residual_max, hermitian_goldstone_abs_w2_max, lambda_min_L_Gamma
C3_speeds[GK|GM]: c_T (A-2 joint estimator), c_L1_framework (the HIGHER of the two compressional k→0 speeds), c_other_compressional, R_T_framework = c_T/c_L1_framework ; C3_F_ISO: cT_split, pass
C4_F_MIX: min_o2_T[GK|GM], pass
C5_F_DISP[GK|GM]: a2, a4, CI_a2_total, regime ("absolute"|"relative"), F_CONV_pass_A2, rungs_used_ka
C6_arm[GK|GM]: "A1 ON-CONE-EXACT" | "A2 ON-CONE-PROTECTED-O(k^4)" | "A3 DISPERSIVE-O(k^2)" | "A4 CHANNEL-UNDEFINED" | "A5 INSTRUMENT-LIMITED" (first token compared)

## 4. Comparison protocol (frozen)
Tolerances (fixed before your leg ran, stated in the comparator header): C1 U₀ 10⁻⁹ rel, ⟨ρ⟩ 10⁻⁴ abs, booleans identical; C2 A-1 booleans identical; C3 c_T 10⁻⁴ rel, c_L1/R_T 10⁻³ rel, F-ISO identical; C4 F-MIX identical; C5 a₂ same sign and ≤ 5×10⁻² rel, a₄ same sign and ≤ 5×10⁻¹ rel, F-CONV identical; C6 base arm identical. Any MISS ⇒ S9 (prereg §8): fingerprint with mechanism, no re-tuning, arms untouched; the chat side re-runs the same frozen comparator on return.

## 5. Return manifest (one commit on `claude/<descriptor>`)
Your instrument(s) (md5 + bytes); `cc_phase0..5` JSONs; `s2c1_cc_cmp_checkpoint.json` (md5, bytes, pre-decode commit hash); comparator output verbatim (md5); `G_S2C1_CCLEG_REPORT.md` with per-item mechanisms, honesty ledger H-CC-1..n, deviations D-CC-1..n, the T1 scan output (zero hits), the quarantine-decode commit hash, and explicit non-claims (prereg §9: no observable, no bridge, no channel-speed-equality claim, no μ_n, nothing about W_∪ — PF-S2 executes only at fold on author authorization after P2).

## 6. Non-claims and what this dispatch is not
Not the aggregate probe (P2 is staged separately and not authorized); not a fold; not a window action. A verdict arm here is the single-crystal P1 arm only.

---

# EMBEDS (byte-exact; extract with the script in §1 — do not copy by hand; QUARANTINED = base64-armored, do not decode before your checkpoint is hashed)

### EMBED — ACTIVATION FLAGS (P-4) — `activation_G_S2C1.json` (md5 7a37816df1bd076636d5c78ab7d04b1e, 3536 B, raw)

<<<EMBED-BEGIN name=activation_G_S2C1.json md5=7a37816df1bd076636d5c78ab7d04b1e bytes=3536 enc=raw quarantine=0>>>
{
 "BDG_FORM_OF_RECORD": "Hermitian: omega^2 h = L^{1/2}(L+2X)L^{1/2} h, admissible only with lambda_min(L) >= -1e-12 verified at EVERY k; product-form omega^2 f = L(L+2X) f cross-checks at two rungs (ka=0.3 and 0.01875)",
 "BLIND_UNTIL_CC_CHECKPOINT_HASHED": true,
 "BRANCH_NAMING": "claude/<descriptor>",
 "CHANNEL_E2": "S2 channel = the lattice-phonon mode of maximal traceless-strain (E2) fraction o2; lattice-phonon = density-fluctuation amplitude dominated by grad rho0 (R2 >= 0.90, grad share >= 0.5); theta_id = 0.90",
 "COMPARATOR_FROZEN": "g_s2c1_compare.py md5 e730844e9cf9e722e0e7789f90f34489 ; schema s2c1_cmp_v1 ; run after hashing your checkpoint; the chat side re-runs it on return",
 "DISCLOSURE": "Addendum A-2's text necessarily reveals that the chat leg's a2 lies in the |a2| > 1e-5 regime; blindness under P-4 is procedural (G-POLY1 H-8); your independence rests on your own stack, not on ignorance of that fact",
 "ELECTIONS": "E-0..E-8 at the lock record defaults (T3); A-1 and A-2 operational forms as written in the addenda",
 "ESTIMATOR_A2": "joint LSQ omega_T/k = c(1 + a2 (ka)^2 + a4 (ka)^4) over a COMMON floor-clean rung set chosen at your largest resolution: sigma_r = floor_w2/(2 omega_T^2) < 3e-7 (floor_w2 = your A-1 Hermitian Goldstone |omega^2| at that resolution); list excluded rungs; window term from the sigma_r < 1e-6 set",
 "EXECUTE_CC_LEG": true,
 "FALSIFIERS": "F-MIX min o2(T) >= 0.90; F-ISO |c_T(GK)/c_T(GM) - 1| <= 0.01; F-DISP at tau = 1e-6 with CI = max(resolution deltas, window term); arms A1..A5 per prereg \u00a75",
 "F_CONV_A2": "a2 across successive resolutions: |da2| <= 1e-7 if |a2| <= 1e-5 else |da2|/|a2| <= 1e-2 ; c_T: |dc_T|/c_T <= 1e-5",
 "LADDER_E4": "dyadic ka in [1e-3, 0.3]: ka = 0.3/2^j, j=0..8, plus speed-set {0.005,0.01,0.015,0.02,0.03}; directions Gamma-K (along a bond) and Gamma-M (30 deg); three resolutions of your discretization (the analogue of n_b 24/32/40), per-phase JSON checkpoints",
 "LOCK": {
  "A1": "8bf51bd05c691f3f03d796b231cdd262",
  "A2": "a9bda086213ee0afe1e2ba01055659cd",
  "T1": "8cd89b9a82704accd89f7ff6f5e220b4",
  "lock_record": "f2f4d50029fb5be3122a885c48a7e04f",
  "prereg": "2ea8ec13ffa3c32898cc24a3be605c64"
 },
 "NO_FOLD_NO_WINDOW_ACTION": true,
 "P4b_BASE64_ARMOR_QUARANTINE": true,
 "REQUESTED_VARIATION": "your OWN crystallization (different solver/seed than semi-implicit imaginary time + Newton-Krylov), your OWN BdG discretization (e.g. real-space finite-difference Bloch-BdG, or a Fourier-grid BdG built from a different kernel-table method), your OWN E2/quadrupole projector implementation and fitter; ZERO code reuse from the quarantined chat instruments",
 "S9_ON_ANY_MISS": true,
 "SUBSTRATE_TO_BUILD": "2-D GP, hbar=m=1, gem8 kernel U(r)=20*exp(-r^8) (R=1), hexagonal p6m primitive cell a*=1.46059, one density peak per cell, FIXED mu=53.225 (report mean density; ~1 expected), stationarity ||L psi0||/||psi0|| <= 1e-10 (L = -1/2 lap - mu + U*rho0)",
 "T1_SCAN": "grep -n -i -F -f t1_forbidden_G_S2_ON_CONE.txt <every CC instrument and checkpoint> -> zero hits; exemptions: the locked prereg/addenda/reports and the quarantined chat artifacts",
 "VERIFY_THEN_BUILD": true,
 "WARD_GAMMA_A1": "(a) ||(L+2X) d_x psi0||/||d_x psi0|| and d_y both <= 1e-9 in your basis; (b) Hermitian-form Goldstone |omega^2| <= 1e-8 at Gamma with lambda_min(L) >= -1e-12; halt if either fails",
 "dispatch": "CC LEG \u2014 single-crystal S2-on-cone ladder",
 "dispatch_date": "2026-09-03",
 "display": "Gate G-S2-ON-CONE",
 "gate": "G-S2C1"
}
<<<EMBED-END name=activation_G_S2C1.json>>>

### EMBED — LOCKED PRE-REGISTRATION (2ea8ec13) — `G_S2_ON_CONE_EXECUTION_PREREGISTRATION.md` (md5 2ea8ec13ffa3c32898cc24a3be605c64, 12984 B, raw)

<<<EMBED-BEGIN name=G_S2_ON_CONE_EXECUTION_PREREGISTRATION.md md5=2ea8ec13ffa3c32898cc24a3be605c64 bytes=12984 enc=raw quarantine=0>>>
# STAGING MEMO — Gate G-S2-ON-CONE (DRAFT — NOT LOCKED)
## The S2-on-cone adjudication: does the helicity-±2 channel of the instantiated vacuum ride the transverse cone exactly?

**Date:** August 28, 2026. **Status:** DRAFT for author elections; no lock, no Phase 0, per the initiating directive. **Chain:** the radiative component of the G-CI1 B-2 burden, transferred at PF-1 (V4.77, §2.91.N) with the G-POLY1 window W_∪ = (0, 2.1213132100130068 m] SUSPENDED from the Phase-3 intersection pending exactly this adjudication. **Register target:** R1-machine for all computations; R2 for any window action.

---

## §1 Burden and stakes

G-CI1 established F-IRR: the instantiated substrate's excitation inventory carries NO gapless internal helicity-±2 branch (CI-S FALSIFIED-STRUCTURAL). The operative branch is CI-W/EM-IN, whose EM-side window is microscopic (W^EM_∪ = (0, 3.7641664288e-33] SI). The macroscopic GW-side window W_∪ = (0, 2.1213132100130068 m] (G-POLY1, verdict class P-2) survives ONLY under the S2-on-cone assumption: that the helicity-±2 (quadrupole/shear) channel of the LATTICE sector propagates with exact, scale-independent linear dispersion ω = c_T k, NOT inheriting the finite-ka Rayleigh/Born dispersion that windowed the EM sector.

Consequence routing (PF-S2, to be elected T3): ON-CONE verdicts REINSTATE W_∪ as banked; DISPERSIVE verdicts keep W_∪ suspended and replace it with a re-derived window W_∪′ from the measured dispersion scale (possibly empty ⇒ retire); CHANNEL-UNDEFINED voids the GW-side of CI-W. A FAIL here is a structural finding at full evidential weight (G-SCALE1 precedent) — the M-naive expectation is AGAINST exactness (see §2), and this memo registers that expectation now so no outcome can be spun.

## §2 LSF-δ record (cross-dialect, target-domain vocabulary; queries verbatim)

Q1 "Weinberg-Witten theorem emergent graviton composite" — the WW no-go: massless spin j>1 states cannot carry a Lorentz-covariant conserved stress tensor; standardly read as forbidding composite/emergent gravitons IN LORENTZ-COVARIANT theories; explicitly evaded by non-Lorentz-covariant substrates (most emergent-gravity programs). SQT's acoustic substrate breaks Lorentz at lattice scale ⇒ no direct collision, but WW is mandatory prior art for any S2-sector claim and must be cited in every downstream document.

Q2 "GW170817 gravitational wave speed constraint dispersion graviton mass bound" — adjacent-dialect observational pins (T1-QUARANTINED from instruments): |c_gw/c − 1| ≲ 5×10⁻¹⁶ (GW170817 + GRB 170817A); LVC modified-dispersion parameterization E² = p²c² + Ap^αc^α with per-α bounds; combined graviton-mass bound m_g ≤ 4.7×10⁻²³ eV/c² (GWTC-1). These live ONLY in the LSF file and post-hash report sections.

Q3 "emergent gravitons lattice model Gu Wen quantum graphity spin-2 excitations" — THE pivotal cross-dialect cluster. Gu–Wen (arXiv:0907.1203; Nucl. Phys. B 863 (2012) 90): helicity ±2 modes emerge from qubit/lattice models, BUT (a) their L-type model disperses as ε_k ∝ k³, NOT linearly; (b) documented difficulty statement: it is "very hard" to isolate helicity ±2 as the only gapless lattice excitation — generically all of ±2, ±1, 0 are gapless or none are; (c) a linear-dispersion isolated ±2 sector required a specially compactified/discretized construction. This PINS the M-naive expectation for any lattice substrate: exact cone confinement of an isolated helicity-2 channel is non-generic. No collision: no p6m/GP-supersolid computation exists in this literature.

Q4 "fracton elasticity duality Pretko tensor gauge theory phonon" — Pretko–Radzihovsky (PRL 120, 195301 (2018)); crystal-to-fracton dualities (PRB 100, 134113 (2019)): 2D quantum-crystal elasticity is dual to a rank-2 symmetric tensor gauge theory; the transverse and longitudinal phonons ARE the two gapless gauge modes; defects map to fractons/dipoles. Adjacent-dialect structural map legitimizing the "shear sector as tensor-gauge sector" reading of the p6m substrate; silent on cone-exactness. Bank for the §-cross-reference file.

Q5 "polycrystal shear wave attenuation Rayleigh regime Stanke Kino Weaver phase velocity dispersion" — target-domain for the aggregate probe: Stanke–Kino (JASA 75, 665 (1984)) unified/SOA theory; Weaver (JMPS 38, 55 (1990)) Dyson/FOSA — equivalent dispersion equations; Rayleigh-regime attenuation ∝ ω⁴ with grain-shape insensitivity; scattering-induced PHASE-VELOCITY DISPERSION is small (≲1%-class) but generically NONZERO for the shear branch. Pins the aggregate expectation: strict cone-exactness in the polycrystalline aggregate is expected to fail at second order; the honest deliverable is the ORDER and MAGNITUDE feeding W_∪′, not a binary.

Q6 "emergent Lorentz invariance fine-tuning different limiting speeds Collins Perez Sudarsky Chadha Nielsen" — Chadha–Nielsen (NPB 217, 125 (1983)): LI as an IR-attractive fixed point with SLOW flow; Collins–Perez–Sudarsky–Urrutia–Vucetich (PRL 93, 191301 (2004)): the fine-tuning problem for Planck-scale preferred frames; Anber–Donoghue (PRD 83, 105027 (2011)): a universal limiting speed emerges via RG but slowly. Relevance: velocity equalization ACROSS channels is the documented hard problem; this gate however asks the WEAKER intra-channel question (is one channel's dispersion exactly linear), which is the correctly bounded first step.

**Collision assessment: NO COLLISION.** No published computation of quadrupole/helicity-2 channel dispersion exactness on a p6m GP-supersolid substrate or its Hashin–Shtrikman/Rayleigh polycrystalline aggregate; the assembled question (S2-on-cone as the rescue condition for a banked macroscopic window) is novel-in-assembly, to be RE-VERIFIED at lock per standing LSF discipline.

## §3 Operational definition

**Substrate objects.** (i) The MV-G1 crystallized p6m GP-supersolid state (single crystal), via the instantiated BdG/Bogoliubov fluctuation machinery of the G-ζ1/G-INT1 line; (ii) the G-POLY1 polycrystalline aggregate, via the banked Phase-1 Rayleigh grain-scattering machinery (Q_T^a quartet {step_hex 3.519074e-2, gem8_hex 5.002055e-2, step_cubic 5.407763e-2, gem8_cubic 7.549430e-2}, TT+TL decomposed, dressing exponents ≈ 3.99).

**The S2 channel.** At small k the helicity-±2 content of the 2D p6m substrate is the quadrupole/shear doublet: under the C₆ᵥ little group at Γ the strain response decomposes, and the E₂ doublet {u_xx − u_yy, 2u_xy} carries angular momentum ±2 under the SO(2) cover. Define the helicity-2 projector P₂ onto this doublet and, for each k along Γ–M and Γ–K, define ω₂(k) as the dispersion of the BdG branch of maximal P₂ overlap; the overlap value o₂(k) is reported per point. c_T is the G-TSH3 first-passing-convention transverse speed at the ELECTED kernel shape (R_T is a KNOB — results are per-kernel by construction; certified set gem8 R_T = 0.51767, gem4 0.47401, gem3 0.40780).

**Probe P1 (single crystal, the cone test).** On a dyadic k-ladder in the elected window, compute the residual r(k) ≡ ω₂(k)/(c_T k) − 1 in controlled arithmetic and fit r(k) = a₂(ka)² + a₄(ka)⁴ per direction. Report a₂, a₄ with two-leg CIs, plus the Γ–M/Γ–K anisotropy split.

**Probe P2 (aggregate, the inheritance test).** In the banked Rayleigh machinery, compute the helicity-2 channel's scattering-induced fractional phase-velocity dispersion Δc₂(ω)/c₂ and its attenuation exponent across the Rayleigh window; determine whether the quadrupole combination inherits the transverse Q_T-class coefficients or cancels at leading order (coefficient ratio to the banked quartet reported).

## §4 Falsifiers and controls (live at lock)

- **F-DISP:** |a₂| or |a₄| above the elected zero-threshold with two-leg-consistent sign ⇒ DISPERSIVE at that order. Any O(k²) or O(k⁴) leakage into the S2 mode = the cone FAILS as exact (per the initiating directive).
- **F-ISO:** Γ–M vs Γ–K residual split above θ_iso ⇒ no single cone (direction-dependent speed) ⇒ FAIL regardless of a₂.
- **F-MIX:** max-overlap o₂(k) below θ_id anywhere in the window ⇒ the S2 channel is not spectrally isolable ⇒ CHANNEL-UNDEFINED (the Gu–Wen generic degeneracy realized).
- **F-CTRL-L (positive control):** the longitudinal branch, run through the identical pipeline, must exhibit its known nonzero dispersion; failure ⇒ INSTRUMENT-LIMITED, halt.
- **F-CTRL-INJ (positive control):** an injected synthetic (ka)² term at 10× threshold must be recovered by the fit within CI; failure ⇒ INSTRUMENT-LIMITED, halt.
- **F-CONV:** convergence gates on grid/cutoff refinement (per-quantity thresholds elected); failure ⇒ halt, no verdict.
- **F-AGG:** P2 coefficient inconsistent between legs beyond comparator tolerance ⇒ S9.

## §5 Verdict arms (registered now; no re-pose after data)

A1 **ON-CONE-EXACT** — a₂ and a₄ both at zero within threshold, isotropic, o₂ ≥ θ_id throughout; P2 quadrupole coefficient cancels at Rayleigh order. PF-S2 ⇒ W_∪ REINSTATED.
A2 **ON-CONE-PROTECTED-O(k⁴)** — a₂ = 0 (symmetry-forced or measured-zero), a₄ ≠ 0. Cone exact at leading nontrivial order only; PF-S2 ⇒ W_∪′ re-derived from the a₄ scale.
A3 **DISPERSIVE-O(k²)** — a₂ ≠ 0. PF-S2 ⇒ W_∪ remains suspended; W_∪′ from the a₂ scale or retire if empty.
A4 **CHANNEL-UNDEFINED** — F-MIX fires. PF-S2 ⇒ GW-side of CI-W VOID; burden unresolved, successor named.
A5 **INSTRUMENT-LIMITED** — any F-CTRL/F-CONV halt. No verdict; halt banked as H-item.
Sub-annotations: per-kernel (gem8/gem4/gem3) and single-crystal vs aggregate splits reported alongside every arm.

## §6 Elections required (defaults proposed; T3 on election)

- **E-0 gate name:** default **G-S2C1**, display name "the S2-on-cone gate" (the directive's "Gate G-S2-ON-CONE" accepted as the display form).
- **E-1 substrate scope:** (a) single crystal only; **(b) single crystal + aggregate [default]**.
- **E-2 channel definition:** E₂/quadrupole projector under C₆ᵥ as in §3; overlap threshold θ_id **default 0.90**.
- **E-3 kernel family for c_T:** **default gem8** (primary), gem4/gem3 as reported sub-annotations (KNOB discipline: no averaging across kernels, F3-class).
- **E-4 k-window and fit basis:** **default ka ∈ [10⁻³, 0.3]**, dyadic ladder, fit {(ka)², (ka)⁴}, both symmetry directions.
- **E-5 zero-thresholds:** **default |a₂|, |a₄| < 10⁻⁶** at the two-leg CI; **θ_iso default 1%**; F-CONV per-quantity thresholds fixed at lock.
- **E-6 leg architecture:** **default** chat leg builds projector + ladder + fits on the instantiated BdG stack; CC leg full-from-scratch independent BdG + own projector + own fitter (G-ζ1/G-CI1 precedent); comparator frozen pre-return; S9 on any miss.
- **E-7 consequence routing PF-S2:** as §1/§5 (T3 once elected).
- **E-8 dispatch discipline:** P-4 in-band, WITH **P-4.b base64-armor on all quarantined embeds** (first gate under the new standing amendment).

## §7 Eddington traps and T1

Trap 1: no adjacent-dialect observational value (GW speeds, graviton masses, event names) in ANY instrument or checkpoint — T1-enforced; the adjacent-dialect comparison appears only in labeled post-hash report sections. Trap 2: thresholds are elections locked BEFORE data; no post-hoc threshold motion. Trap 3: no averaging across kernel shapes (KNOB, F3-class). Trap 4: the M-naive expectation (DISPERSIVE, per Gu–Wen k³ and Stanke–Kino/Weaver shear dispersion) is REGISTERED HERE, pre-data. Trap 5: no vocabulary substitution — instruments speak S2/quadrupole/E₂, never "graviton". T1 list: `t1_forbidden_G_S2_ON_CONE.txt` (pattern lines only, H-2 rule; justified exemptions: this memo's §2 and post-hash report sections).

## §8 Two-leg plan (post-lock)

Phase 0 verify-then-build (P-4 + P-4.b dispatch); Phase 1 projector + controls (F-CTRL-L, F-CTRL-INJ) BEFORE any framework verdict quantity; Phase 2 P1 ladder both directions; Phase 3 P2 aggregate channel; per-phase JSON checkpoints (E8); frozen comparator with exact criteria on integers/booleans and CI-overlap criteria on (a₂, a₄, Δc₂/c₂); S9 on any miss; fold only on author word.

## §9 Non-claims

No observable, no bridge (M.BRIDGE intact): this gate compares structure WITHIN the instantiated model; the adjacent-dialect pins are context, never inputs. No claim about channel-speed equality (c_T vs the EM-in channel) — that is the documented multi-species problem (Q6), a separate successor. No μ_n, no §2.52 Open 3 contact, no carrier re-identification (F-IRR stands). A DISPERSIVE or CHANNEL-UNDEFINED verdict is a structural finding, not a program failure.

## §10 Fold sketch

On verdict: one §2.91.O-class entry (Cluster CI successors), PF-S2 executed per election, one Part VI row, W_∪ row action per arm. Estate hashes at lock.
<<<EMBED-END name=G_S2_ON_CONE_EXECUTION_PREREGISTRATION.md>>>

### EMBED — LOCK RECORD (elections E-0..E-8, T3) — `G_S2_ON_CONE_LOCK_RECORD.md` (md5 f2f4d50029fb5be3122a885c48a7e04f, 3009 B, raw)

<<<EMBED-BEGIN name=G_S2_ON_CONE_LOCK_RECORD.md md5=f2f4d50029fb5be3122a885c48a7e04f bytes=3009 enc=raw quarantine=0>>>
# G-S2C1 (display: Gate G-S2-ON-CONE) — LOCK RECORD

**Lock date:** September 2, 2026. **Authorization (verbatim, author):** "I authorize elections E-0 through E-8 under the default values specified in §6 of the staging memo. Proceed to lock the pre-registration byte-identical, mint `G_S2_ON_CONE_LOCK_RECORD.md`, freeze the T1 list, and execute Phase 0 (harness build, validation, and positive controls F-CTRL-L / F-CTRL-INJ). … Do not proceed to Phase 1 (the single-crystal ka-ladder fit) without explicit authorization."

## Locked artifacts

| Artifact | md5 | bytes | Status |
|---|---|---|---|
| `G_S2_ON_CONE_EXECUTION_PREREGISTRATION.md` | 2ea8ec13ffa3c32898cc24a3be605c64 | 12,984 | LOCKED — byte-identical (cmp) to the approved `staging_memo_G_S2_ON_CONE.md` |
| `t1_forbidden_G_S2_ON_CONE.txt` | 8cd89b9a82704accd89f7ff6f5e220b4 | 144 | FROZEN — 16 pattern lines, pattern-lines-only (H-2 rule) |

## Elections (T3-immutable from this record)

- **E-0** gate name **G-S2C1**; display name "Gate G-S2-ON-CONE".
- **E-1 (b)** substrate scope: single crystal + polycrystalline aggregate.
- **E-2** S2 channel: E₂/quadrupole (traceless-strain) projector under C₆ᵥ; overlap threshold θ_id = 0.90; ω₂(k) = the branch of maximal overlap.
- **E-3** kernel family for c_T: gem8 primary (g* = 20, a* = 1.46059, μ = 53.225, ρ₀ = 1, substrate units); gem4/gem3 as reported sub-annotations; no cross-kernel averaging (KNOB discipline, F3-class).
- **E-4** k-window ka ∈ [10⁻³, 0.3], dyadic ladder, fit basis {(ka)², (ka)⁴}, both symmetry directions Γ–M and Γ–K.
- **E-5** zero-thresholds |a₂|, |a₄| < 10⁻⁶ at the two-leg CI; θ_iso = 1%; F-CONV per-quantity thresholds fixed at Phase-0 close (see the Phase-0 report).
- **E-6** leg architecture: chat leg = projector + ladder + fits on the instantiated BdG stack; CC leg = full-from-scratch independent BdG + own projector + own fitter; comparator frozen pre-return; S9 on any miss.
- **E-7** consequence routing PF-S2 as prereg §1/§5: A1 ⇒ W_∪ REINSTATED; A2/A3 ⇒ W_∪ stays suspended, W_∪′ re-derived from the measured dispersion scale (retire if empty); A4 ⇒ GW-side of CI-W VOID; A5 ⇒ no verdict.
- **E-8** dispatch discipline: P-4 in-band with P-4.b base64 armor on all quarantined embeds (first gate under the amendment).

## Registered expectation (pre-data, Eddington trap 4)

M-naive expectation: **DISPERSIVE** (Gu–Wen helicity-±2 lattice modes disperse as k³; Stanke–Kino/Weaver shear-branch phase-velocity dispersion nonzero at second order). A1 ON-CONE-EXACT would be the surprising outcome; A2/A3 the expected ones. Registered so that no outcome can be spun.

## Phase gating

Phase 0 (harness build, validation, F-CTRL-L, F-CTRL-INJ, C-NEG engine validation) AUTHORIZED and executed under this lock. **Phase 1 (single-crystal ka-ladder fit — crystallization + Bloch-BdG on the crystal) NOT AUTHORIZED**; the harness carries a hard activation flag `PHASE1_AUTHORIZED = False`.
<<<EMBED-END name=G_S2_ON_CONE_LOCK_RECORD.md>>>

### EMBED — ADDENDUM A-1 (WARD-Gamma) — `G_S2_ON_CONE_LOCK_RECORD_ADDENDUM_A1.md` (md5 8bf51bd05c691f3f03d796b231cdd262, 1019 B, raw)

<<<EMBED-BEGIN name=G_S2_ON_CONE_LOCK_RECORD_ADDENDUM_A1.md md5=8bf51bd05c691f3f03d796b231cdd262 bytes=1019 enc=raw quarantine=0>>>
# G-S2C1 — LOCK RECORD ADDENDUM A-1 (September 3, 2026)

**Authorization (verbatim, author):** "I explicitly AUTHORIZE Amendment A-1. WARD-Γ is now formally defined as: (a) analytic-mode Ward residual ≤ 10⁻⁹, AND (b) Hermitian-form Goldstone |ω²| ≤ 10⁻⁸ with λ_min(L) ≥ −10⁻¹² at every k. Proceed to execute the dyadic ka-ladder for Phase 1 at n_b ∈ {24, 32, 40} using the Hermitian form, with product-form cross-checks at two rungs."

**Scope:** amends the Phase-0-fixed WARD-Γ criterion only (H-S2C-5: the literal product-form dense-eig criterion is floor-limited at n_b ≥ 32). No election E-0..E-8 changes; thresholds τ = 10⁻⁶, θ_iso = 1%, θ_id = 0.90 unchanged; arms unchanged; prereg 2ea8ec13 and T1 8cd89b9a unchanged. The dense-eigensolver floor is carried as an explicit uncertainty term (per-n_b Goldstone |ω²| propagated into the ladder CI via the n_b-change term of F-CONV).

**Applies to:** the chat leg now; the CC leg by the same wording at dispatch (P-4 + P-4.b).
<<<EMBED-END name=G_S2_ON_CONE_LOCK_RECORD_ADDENDUM_A1.md>>>

### EMBED — ADDENDUM A-2 (F-CONV + estimator) — `G_S2_ON_CONE_LOCK_RECORD_ADDENDUM_A2.md` (md5 a9bda086213ee0afe1e2ba01055659cd, 1950 B, raw)

<<<EMBED-BEGIN name=G_S2_ON_CONE_LOCK_RECORD_ADDENDUM_A2.md md5=a9bda086213ee0afe1e2ba01055659cd bytes=1950 enc=raw quarantine=0>>>
# G-S2C1 — LOCK RECORD ADDENDUM A-2 (September 3, 2026)

**Authorization (verbatim, author):** "I explicitly AUTHORIZE Amendment A-2. F-CONV is now defined as: absolute 10⁻⁷ when |a₂| ≤ 10τ; relative 10⁻² when |a₂| > 10τ. The speed reference is taken from the c-free joint estimator over floor-clean rungs."

**Operational form (both legs):**
- Speed reference c_T and the fit coefficients come from the joint least squares ω_T/k = c(1 + a₂(ka)² + a₄(ka)⁴) over a COMMON floor-clean rung set used for every n_b, selected at the largest n_b of record (40): rungs with σ_r = floor_ω²(40)/(2ω_T²) < 3×10⁻⁷ (floor_ω² = the A-1 Hermitian Goldstone |ω²|) — on the E-4 ladder this is ka ∈ {0.3, 0.15, 0.075, 0.0375} (4 rungs). The excluded rungs are listed, never silently dropped. The window systematic on a₂ is the difference to the next-larger common set (σ_r < 10⁻⁶, 5 rungs) and is carried as the a₂ CI's window term.
- F-CONV on a₂ across successive n_b (24→32, 32→40): |Δa₂| ≤ 10⁻⁷ when |a₂| ≤ 10τ = 10⁻⁵; |Δa₂|/|a₂| ≤ 10⁻² when |a₂| > 10⁻⁵. F-CONV on c_T: |Δc_T|/c_T ≤ 10⁻⁵.
- Sensitivity disclosed (H-S2C-9): a per-n_b-varying rung set (σ_r(n_b) < 10⁻⁶ evaluated at each n_b separately) mixes rung sets across the F-CONV pair and fails Γ–K's 24→32 at 1.2×10⁻²; the common-set rule is adopted as the principled form, and it passes at both floor thresholds (3×10⁻⁷: drifts ≤ 3.0×10⁻³; 10⁻⁶: ≤ 1.6×10⁻³). Also corrected: the Phase-1 ladder report's "6 rungs" label for the ka ≥ 0.0375 set is 4 rungs (the numbers were computed on 4).
- Amends the F-CONV clause and the speed-reference estimator only; E-0..E-8, τ, θ_iso, θ_id, arms, prereg 2ea8ec13, T1 8cd89b9a, A-1 8bf51bd0 unchanged. Applied to the Phase-1 ladder data (checkpoint 5ee152fc) without recomputation; the CC leg runs the same clause at dispatch.
<<<EMBED-END name=G_S2_ON_CONE_LOCK_RECORD_ADDENDUM_A2.md>>>

### EMBED — T1 LIST (frozen; pattern lines only) — `t1_forbidden_G_S2_ON_CONE.txt` (md5 8cd89b9a82704accd89f7ff6f5e220b4, 144 B, raw)

<<<EMBED-BEGIN name=t1_forbidden_G_S2_ON_CONE.txt md5=8cd89b9a82704accd89f7ff6f5e220b4 bytes=144 enc=raw quarantine=0>>>
graviton
gravitational wave
GW170817
GW150914
GRB 170817
LIGO
Virgo
speed of gravity
c_g
4.7e-23
1.27e-22
5e-16
Weinberg
Witten
Hulse
PSR B1913
<<<EMBED-END name=t1_forbidden_G_S2_ON_CONE.txt>>>

### EMBED — FROZEN COMPARATOR — `g_s2c1_compare.py` (md5 e730844e9cf9e722e0e7789f90f34489, 4643 B, raw)

<<<EMBED-BEGIN name=g_s2c1_compare.py md5=e730844e9cf9e722e0e7789f90f34489 bytes=4643 enc=raw quarantine=0>>>
#!/usr/bin/env python3
# g_s2c1_compare.py — Gate G-S2C1 two-leg comparator (FROZEN pre-return). Schema s2c1_cmp_v1.
# Usage: python3 g_s2c1_compare.py s2c1_chat_cmp_checkpoint.json s2c1_cc_cmp_checkpoint.json
# This gate carries FLOAT quantities; tolerances are stated per item and were fixed BEFORE the CC leg ran:
#   C1 substrate   kernel U0 rel 1e-9 ; mean_rho abs 1e-4 (both legs at fixed mu = 53.225) ; residual/lambda_min booleans identical
#   C2 WARD (A-1)  pass_a, pass_b identical (True) ; values reported
#   C3 speeds      c_T rel 1e-4 per direction ; c_L1_framework rel 1e-3 ; R_T_framework rel 1e-3 ; F-ISO pass identical
#   C4 F-MIX       pass identical ; min o2 reported
#   C5 F-DISP      a2 per direction: SAME SIGN and relative agreement <= 5e-2 ; a4: same sign and relative <= 5e-1 ; F_CONV_pass_A2 identical
#   C6 arm         base arm identical per direction (A1..A5 token)
# Any MISS -> S9 counter-cross-check (prereg §8); no verdict before S9 closes. Provenance fields are reported, never compared.
import json, sys, hashlib
def load(p): return json.load(open(p, encoding="utf-8"))
def rel(a, b): return abs(a - b) / max(abs(a), abs(b), 1e-300)
def arm_token(s): return str(s).strip().split()[0]
def main(cp, cc):
    A, B = load(cp), load(cc)
    for p in (cp, cc): print("checkpoint %s md5 %s" % (p, hashlib.md5(open(p, "rb").read()).hexdigest()))
    assert A["schema"] == B["schema"] == "s2c1_cmp_v1" and A["prereg_md5"] == B["prereg_md5"] == "2ea8ec13ffa3c32898cc24a3be605c64"
    miss, notes = [], []
    def chk(tag, ok, desc):
        (notes if ok else miss).append("%s %s: %s" % (tag, "pass" if ok else "MISS", desc)); print("  %s %s  %s" % (tag, "PASS" if ok else "MISS", desc))
    a, b = A["C1_substrate"], B["C1_substrate"]
    chk("C1", rel(a["kernel_U0"], b["kernel_U0"]) <= 1e-9, "kernel U0 %r vs %r" % (a["kernel_U0"], b["kernel_U0"]))
    chk("C1", abs(a["mean_rho"] - b["mean_rho"]) <= 1e-4, "mean_rho %r vs %r" % (a["mean_rho"], b["mean_rho"]))
    chk("C1", a["residual_le_1e-10"] == b["residual_le_1e-10"] == True, "residual<=1e-10 %r vs %r" % (a["residual_le_1e-10"], b["residual_le_1e-10"]))
    chk("C1", a["lambda_min_L_Gamma_ge_minus1e-12"] == b["lambda_min_L_Gamma_ge_minus1e-12"] == True, "lambda_min(L) floor")
    a, b = A["C2_ward_A1"], B["C2_ward_A1"]
    chk("C2", a["pass_a_analytic"] == b["pass_a_analytic"] == True and a["pass_b_hermitian"] == b["pass_b_hermitian"] == True, "A-1 (a)/(b) chat %r/%r cc %r/%r" % (a["pass_a_analytic"], a["pass_b_hermitian"], b["pass_a_analytic"], b["pass_b_hermitian"]))
    for d in ("GK", "GM"):
        a, b = A["C3_speeds"][d], B["C3_speeds"][d]
        chk("C3", rel(a["c_T"], b["c_T"]) <= 1e-4, "%s c_T %.6f vs %.6f (rel %.1e)" % (d, a["c_T"], b["c_T"], rel(a["c_T"], b["c_T"])))
        chk("C3", rel(a["c_L1_framework"], b["c_L1_framework"]) <= 1e-3, "%s c_L1 %.5f vs %.5f" % (d, a["c_L1_framework"], b["c_L1_framework"]))
        chk("C3", rel(a["R_T_framework"], b["R_T_framework"]) <= 1e-3, "%s R_T %.5f vs %.5f" % (d, a["R_T_framework"], b["R_T_framework"]))
    chk("C3", A["C3_F_ISO"]["pass"] == B["C3_F_ISO"]["pass"], "F-ISO pass %r vs %r (splits %.1e / %.1e)" % (A["C3_F_ISO"]["pass"], B["C3_F_ISO"]["pass"], A["C3_F_ISO"]["cT_split"], B["C3_F_ISO"]["cT_split"]))
    chk("C4", A["C4_F_MIX"]["pass"] == B["C4_F_MIX"]["pass"], "F-MIX pass %r vs %r (min o2 %s / %s)" % (A["C4_F_MIX"]["pass"], B["C4_F_MIX"]["pass"], A["C4_F_MIX"]["min_o2_T"], B["C4_F_MIX"]["min_o2_T"]))
    for d in ("GK", "GM"):
        a, b = A["C5_F_DISP"][d], B["C5_F_DISP"][d]
        chk("C5", (a["a2"] * b["a2"] > 0) and rel(a["a2"], b["a2"]) <= 5e-2, "%s a2 %+.4e vs %+.4e (rel %.1e)" % (d, a["a2"], b["a2"], rel(a["a2"], b["a2"])))
        chk("C5", (a["a4"] * b["a4"] > 0) and rel(a["a4"], b["a4"]) <= 5e-1, "%s a4 %+.3e vs %+.3e (rel %.1e)" % (d, a["a4"], b["a4"], rel(a["a4"], b["a4"])))
        chk("C5", a["F_CONV_pass_A2"] == b["F_CONV_pass_A2"], "%s F-CONV(A-2) %r vs %r" % (d, a["F_CONV_pass_A2"], b["F_CONV_pass_A2"]))
        chk("C6", arm_token(A["C6_arm"][d]) == arm_token(B["C6_arm"][d]), "%s arm %s vs %s" % (d, A["C6_arm"][d], B["C6_arm"][d]))
    print("VERDICT chat=%s cc=%s" % ({d: arm_token(A["C6_arm"][d]) for d in ("GK", "GM")}, {d: arm_token(B["C6_arm"][d]) for d in ("GK", "GM")}))
    if miss: print("RESULT: S9 TRIGGERED — %d miss(es); counter-cross-check before any verdict." % len(miss)); return 2
    print("RESULT: C1–C6 ALL PASS — S9 NOT triggered; two-leg single-crystal result stands; P2 aggregate + fold pending author authorization."); return 0
if __name__ == "__main__": sys.exit(main(sys.argv[1], sys.argv[2]))
<<<EMBED-END name=g_s2c1_compare.py>>>

### EMBED — EXTRACTOR v2 (P-4.b) — `extract_embeds_v2.py` (md5 d4ac62219a95bea1e29d226e371ee39a, 2102 B, raw)

<<<EMBED-BEGIN name=extract_embeds_v2.py md5=d4ac62219a95bea1e29d226e371ee39a bytes=2102 enc=raw quarantine=0>>>
#!/usr/bin/env python3
# extract_embeds_v2.py — byte-exact extraction of every embed in a P-4 dispatch, with P-4.b base64 armor.
# Usage: python3 extract_embeds_v2.py <dispatch.md> [outdir] [--quarantine-dir DIR]
# Markers:  <<<EMBED-BEGIN name=NAME md5=HEX bytes=N enc=raw|b64 quarantine=0|1>>>  ...  <<<EMBED-END name=NAME>>>
# raw: payload is the file's UTF-8 text verbatim (file must end with a newline).  b64: payload is base64 (76-col lines).
# Every embed is verified against md5 + byte count; any mismatch aborts. quarantine=1 embeds are written to the
# quarantine dir (default ./QUARANTINE) and MUST NOT be opened before the CC checkpoint is hashed (procedural blindness).
import sys, os, re, base64, hashlib
BEGIN = "<<<EMBED-" + "BEGIN name=(\\S+) md5=([0-9a-f]{32}) bytes=(\\d+) enc=(raw|b64) quarantine=([01])>>>\n"
END = "<<<EMBED-" + "END name=%s>>>"
def main(path, outdir=".", qdir=None):
    qdir = qdir or os.path.join(outdir, "QUARANTINE"); os.makedirs(outdir, exist_ok=True); os.makedirs(qdir, exist_ok=True)
    text = open(path, "rb").read().decode("utf-8"); n = 0
    for m in re.finditer(BEGIN, text):
        name, md5, nbytes, enc, q = m.group(1), m.group(2), int(m.group(3)), m.group(4), m.group(5) == "1"
        j = text.find(END % name, m.end()); assert j > 0, "END marker missing: " + name
        seg = text[m.end():j]
        payload = seg.encode("utf-8") if enc == "raw" else base64.b64decode("".join(seg.split()))
        assert len(payload) == nbytes, "byte count mismatch %s: %d vs %d" % (name, len(payload), nbytes)
        assert hashlib.md5(payload).hexdigest() == md5, "md5 mismatch: " + name
        dest = os.path.join(qdir if q else outdir, name); open(dest, "wb").write(payload)
        print("OK  %s  %s  %d B  %s%s" % (md5, name, nbytes, enc, "  [QUARANTINE]" if q else "")); n += 1
    print("extracted %d embeds, all md5/byte-verified" % n)
if __name__ == "__main__":
    a = sys.argv[1:]; qd = None
    if "--quarantine-dir" in a: i = a.index("--quarantine-dir"); qd = a[i + 1]; a = a[:i] + a[i + 2:]
    main(a[0], a[1] if len(a) > 1 else ".", qd)
<<<EMBED-END name=extract_embeds_v2.py>>>

### EMBED — chat comparison checkpoint (comparator input) — `s2c1_chat_cmp_checkpoint.json` (md5 2aa66ea21dd5cda16535d409654fe4dd, 2164 B, b64, QUARANTINED)

<<<EMBED-BEGIN name=s2c1_chat_cmp_checkpoint.json md5=2aa66ea21dd5cda16535d409654fe4dd bytes=2164 enc=b64 quarantine=1>>>
ewogIkMxX3N1YnN0cmF0ZSI6IHsKICAiYV9zdGFyIjogMS40NjA1OSwKICAiZ19zdGFyIjogMjAu
MCwKICAia2VybmVsX1UwIjogNTYuOTUwOTQ3MjYyMjYxNTYsCiAgImxhbWJkYV9taW5fTF9HYW1t
YV9nZV9taW51czFlLTEyIjogdHJ1ZSwKICAibWVhbl9yaG8iOiAwLjk5OTk4ODEyOTI0NzQ0NzIs
CiAgIm11X2ZpeGVkIjogNTMuMjI1LAogICJyZXNpZHVhbF9sZV8xZS0xMCI6IHRydWUsCiAgInJl
c2lkdWFsX3JlbCI6IDEuOTU1MDI1NTc4NDI2MjkzNGUtMTIsCiAgInJlc29sdXRpb25fb2ZfcmVj
b3JkIjogIm5fYj00MCBwbGFuZSB3YXZlcyAoY2hhdCk7IENDIHJlcG9ydHMgaXRzIG93biIKIH0s
CiAiQzJfd2FyZF9BMSI6IHsKICAiYW5hbHl0aWNfd2FyZF9yZXNpZHVhbF9tYXgiOiAyLjMwNDYx
MzMyMjU2Mzk0OWUtMTEsCiAgImhlcm1pdGlhbl9nb2xkc3RvbmVfYWJzX3cyX21heCI6IDguMTA4
ODYzMTU2ODk1MjFlLTA5LAogICJsYW1iZGFfbWluX0xfR2FtbWEiOiAxLjY5MTQ0NzI3MDUzMjk4
MTNlLTE0LAogICJwYXNzX2FfYW5hbHl0aWMiOiB0cnVlLAogICJwYXNzX2JfaGVybWl0aWFuIjog
dHJ1ZQogfSwKICJDM19GX0lTTyI6IHsKICAiY1Rfc3BsaXQiOiAxLjMzMzg5NDc5NTQ2MzMwODVl
LTA1LAogICJwYXNzIjogdHJ1ZQogfSwKICJDM19zcGVlZHMiOiB7CiAgIkdLIjogewogICAiUl9U
X2ZyYW1ld29yayI6IDAuNTIxNDc4ODQwNjMwMTM2NCwKICAgImNfTDFfZnJhbWV3b3JrIjogOS42
ODA1NDY4ODE0NTcwMTUsCiAgICJjX1QiOiA1LjA0ODE5OTY4Mjc2NTQyMiwKICAgImNfb3RoZXJf
Y29tcHJlc3Npb25hbCI6IDMuNzQxMzUwMjkzMzYwNDQxNAogIH0sCiAgIkdNIjogewogICAiUl9U
X2ZyYW1ld29yayI6IDAuNTIxNDY5Mjk5NTk2MzQ4MiwKICAgImNfTDFfZnJhbWV3b3JrIjogOS42
ODA1OTQ4NzIwODg4MzIsCiAgICJjX1QiOiA1LjA0ODE3MTIyMjMwMTY0MiwKICAgImNfb3RoZXJf
Y29tcHJlc3Npb25hbCI6IDMuNzQxMzUzMzI5OTEyODY4NwogIH0KIH0sCiAiQzRfRl9NSVgiOiB7
CiAgIm1pbl9vMl9UIjogewogICAiR0siOiAwLjk5OTk5OTk5MzY5ODg2OTYsCiAgICJHTSI6IDAu
OTk5OTk5OTc3NTgwOTU1NgogIH0sCiAgInBhc3MiOiB0cnVlCiB9LAogIkM1X0ZfRElTUCI6IHsK
ICAiR0siOiB7CiAgICJDSV9hMl90b3RhbCI6IDAuMDAwMzE4MzQ4MDA1MjgwMjU4NCwKICAgIkZf
Q09OVl9wYXNzX0EyIjogdHJ1ZSwKICAgImEyIjogLTAuMDEyNzk0MTYxNTMwNzkyNzYsCiAgICJh
NCI6IC0wLjAwMjk5ODQxOTc3NTU0NzgwNDQsCiAgICJyZWdpbWUiOiAicmVsYXRpdmUiLAogICAi
cnVuZ3NfdXNlZF9rYSI6IFsKICAgIDAuMywKICAgIDAuMTUsCiAgICAwLjA3NSwKICAgIDAuMDM3
NQogICBdCiAgfSwKICAiR00iOiB7CiAgICJDSV9hMl90b3RhbCI6IDAuMDAwMTIzNjc2ODg0MjEx
MTU1MzMsCiAgICJGX0NPTlZfcGFzc19BMiI6IHRydWUsCiAgICJhMiI6IC0wLjAxOTkzMjYxOTE0
MjEzMTk3LAogICAiYTQiOiAtMC4wMDgyNzA5NDE1NjIwNDA4MzQsCiAgICJyZWdpbWUiOiAicmVs
YXRpdmUiLAogICAicnVuZ3NfdXNlZF9rYSI6IFsKICAgIDAuMywKICAgIDAuMTUsCiAgICAwLjA3
NSwKICAgIDAuMDM3NQogICBdCiAgfQogfSwKICJDNl9hcm0iOiB7CiAgIkdLIjogIkEzIERJU1BF
UlNJVkUtTyhrXjIpIiwKICAiR00iOiAiQTMgRElTUEVSU0lWRS1PKGteMikiCiB9LAogImFkZGVu
ZGFfbWQ1IjogewogICJBMSI6ICI4YmY1MWJkMDVjNjkxZjNmMDNkNzk2YjIzMWNkZDI2MiIsCiAg
IkEyIjogImE5YmRhMDg2MjEzZWUwYWZlMWUyYmEwMTA1NTY1OWNkIgogfSwKICJnYXRlIjogIkct
UzJDMSIsCiAibGVnIjogImNoYXQiLAogInByZXJlZ19tZDUiOiAiMmVhOGVjMTNmZmEzYzMyODk4
Y2MyNGEzYmU2MDVjNjQiLAogInJlZ2lzdGVyZWRfZXhwZWN0YXRpb24iOiAiRElTUEVSU0lWRSIs
CiAic2NoZW1hIjogInMyYzFfY21wX3YxIiwKICJzb3VyY2VfbWQ1IjogewogICJBMl9ldmFsdWF0
aW9uIjogIjc3ZmVhNjVmZGU5NWVmZDMzZDg5OTA5NTZjN2MwN2ZmIiwKICAibGFkZGVyX2NoZWNr
cG9pbnQiOiAiNWVlMTUyZmMxNGFjNTVlNzIwOTRmYzY2MGFmZjdhNGEiLAogICJwaGFzZTFfaGFs
dF9jaGVja3BvaW50IjogImVlZWRjZmE1OTRhMjQ5MTVmYTljMTBjNmFiYmQwYTRlIgogfQp9Cg==
<<<EMBED-END name=s2c1_chat_cmp_checkpoint.json>>>

### EMBED — chat instrument — Phase 0 close — `g_s2c1_phase0_close.py` (md5 1882c941fc4288b031131fb8aacccf83, 11719 B, b64, QUARANTINED)

<<<EMBED-BEGIN name=g_s2c1_phase0_close.py md5=1882c941fc4288b031131fb8aacccf83 bytes=11719 enc=b64 quarantine=1>>>
IyEvdXNyL2Jpbi9lbnYgcHl0aG9uMwoiIiJnX3MyYzFfcGhhc2UwX2Nsb3NlLnB5IOKAlCBHYXRl
IEctUzJDMSAoZGlzcGxheTogR2F0ZSBHLVMyLU9OLUNPTkUpLCBQSEFTRSAwIENMT1NFIChjaGF0
IGxlZykuCkxvY2s6IHByZXJlZyAyZWE4ZWMxM2ZmYTNjMzI4OThjYzI0YTNiZTYwNWM2NDsgVDEg
OGNkODliOWE4MjcwNGFjY2Q4OWY3ZmY2ZjVlMjIwYjQ7IGxvY2sgcmVjb3JkIGYyZjRkNTAwLgpQ
SEFTRTFfQVVUSE9SSVpFRCA9IEZhbHNlIChoYXJkIGZsYWc6IG5vIFMyIGxhZGRlciBpcyBjb21w
dXRlZCBvciBmaXR0ZWQgaGVyZSkuCgpUaHJlZSBwYXJ0cywgYWxsIENPTlRST0wtTk9ULVZFUkRJ
Q1Q6CiAoQSkgU1VCU1RSQVRFIERJQUdOT1NUSUMgb24gdGhlIHJlY292ZXJlZCBnejEgY3J5c3Rh
bCAoZyA9IDIyIHNvZnQtZGlzaywgbiA9IDY0LCBhKiA9IDEuNDU3NiwgbXUgPSA1NS45NDYpOgog
ICAgIHVuLWNsaXBwZWQgcHJvZHVjdC1mb3JtIEJkRyBvbWVnYV4yID0gZWlnKEwoTCsyWCkpIGF0
IHNtYWxsIGssIG5fYiBpbiB7MjQsIDMyLCA0MH07IEwgcHNpMCByZXNpZHVhbDsKICAgICBzcGVj
dHJhbCByZXNvbHV0aW9uOyBhbGlhc2luZyB0ZXN0IChleGFjdC1wcm9kdWN0IFggdnMgZ3JpZC1j
b25zaXN0ZW50IFgpLiBFc3RhYmxpc2hlcyB3aGV0aGVyIHRoZQogICAgIGFjb3VzdGljIChHb2xk
c3RvbmUpIHNlY3RvciBpcyByZXNvbHZlZCB0byB0aGUgcHJlY2lzaW9uIHRoZSBFLTQgbGFkZGVy
IG5lZWRzLgogKEIpIEFOQUxZVElDIHA2bSBDT05UUk9MIOKAlCBuZWFyZXN0LW5laWdoYm91ciBj
ZW50cmFsLWZvcmNlIHRyaWFuZ3VsYXIgbGF0dGljZSAoSyA9IG0gPSBhID0gMSksIGNsb3NlZC1m
b3JtCiAgICAgZGlzcGVyc2lvbjogdmFsaWRhdGVzIHRoZSBTMiBwcm9qZWN0b3IgKHRyYWNlbGVz
cy1zdHJhaW4gZnJhY3Rpb247IFQgLT4gMSwgTCAtPiAxLzIgb24gbWlycm9yIGxpbmVzKSBhbmQK
ICAgICB0aGUgRS00L0UtNSBmaXR0ZXIgKHJlc2lkdWFsIHIgPSBhMiAoa2EpXjIgKyBhNCAoa2Ep
XjQgb24gdGhlIGR5YWRpYyBsYWRkZXIpIGFnYWluc3QgaW5kZXBlbmRlbnQKICAgICBjbG9zZWQt
Zm9ybSBzZXJpZXMgY29lZmZpY2llbnRzLiBGLUNUUkwtTDogdGhlIEwgYnJhbmNoJ3MgS05PV04g
Tk9OWkVSTyBhMiBtdXN0IGJlIHJlY292ZXJlZC4KIChDKSBGLUNUUkwtSU5KIOKAlCBzeW50aGV0
aWMgaW5qZWN0aW9uIGEyID0gMTAqdGF1ID0gMWUtNSB3aXRoIG5vaXNlIGF0IHRoZSBGLUNPTlYg
c2NhbGU7IHJlY292ZXJ5IHdpdGhpbiB0YXUuCiIiIgppbXBvcnQgc3lzLCBqc29uLCBoYXNobGli
LCBvcwppbXBvcnQgbnVtcHkgYXMgbnAKc3lzLnBhdGguaW5zZXJ0KDAsICIvaG9tZS9jbGF1ZGUv
czJjL2d6MSIpCmltcG9ydCBnejFfY29yZSBhcyBnegpQSEFTRTFfQVVUSE9SSVpFRCA9IEZhbHNl
ClRBVSA9IDEuMGUtNgpMQURERVIgPSBucC5hcnJheShbMC4zIC8gMioqaiBmb3IgaiBpbiByYW5n
ZSg5KV0pICAgICAgICMgRS00IGR5YWRpYyBrYTogMC4zIC4uLiAwLjAwMTE3CmRlZiBtZDViKGIp
OiByZXR1cm4gaGFzaGxpYi5tZDUoYikuaGV4ZGlnZXN0KCkKCiMgPT09PT09PT09PT09PT09PT09
PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09IChBKSBzdWJzdHJh
dGUgZGlhZ25vc3RpYwpBX1NUQVIsIE1VLCBOID0gMS40NTc2LCA1NS45NDYsIDY0CmNlbGwgPSBn
ei5DZWxsKEFfU1RBUiwgTik7IHBzaTAgPSBucC5sb2FkKCIvaG9tZS9jbGF1ZGUvczJjL2d6MS9w
c2kwX3BvbGlzaGVkX242NC5ucHkiKS5hc3R5cGUoZmxvYXQpCmRlZiBMWChiLCBrKToKICAgIGtn
eCA9IGtbMF0gKyBiLm0xICogY2VsbC5iMVswXSArIGIubTIgKiBjZWxsLmIyWzBdOyBrZ3kgPSBr
WzFdICsgYi5tMSAqIGNlbGwuYjFbMV0gKyBiLm0yICogY2VsbC5iMlsxXQogICAgTCA9IG5wLmRp
YWcoMC41ICogKGtneCoqMiArIGtneSoqMikgLSBNVSkgKyBiLlZtYXQ7IEwgPSAwLjUgKiAoTCAr
IEwuY29uaigpLlQpCiAgICBEID0gZ3ouVV90aWxkZShucC5zcXJ0KGtneCoqMiArIGtneSoqMikp
OyBYID0gYi5QIEAgKERbOiwgTm9uZV0gKiBiLlApOyBYID0gMC41ICogKFggKyBYLmNvbmooKS5U
KQogICAgcmV0dXJuIEwsIFgKZGlhZyA9IHsic3Vic3RyYXRlIjogImd6MV9yZWJ1aWxkIHBzaTBf
cG9saXNoZWRfbjY0IG1kNSAiICsgbWQ1YihvcGVuKCIvaG9tZS9jbGF1ZGUvczJjL2d6MS9wc2kw
X3BvbGlzaGVkX242NC5ucHkiLCAicmIiKS5yZWFkKCkpLAogICAgICAgICJhX3N0YXIiOiBBX1NU
QVIsICJtdSI6IE1VLCAiZ29sZHN0b25lX29mZnNldF9wcm9kdWN0X2Zvcm0iOiB7fSwgImhlcm1p
dGlhbl9jbGlwcGVkX2xvd2VzdCI6IHt9fQpmb3IgbmIgaW4gKDI0LCAzMiwgNDApOgogICAgYiA9
IGd6LkJkRyhjZWxsLCBwc2kwLCBNVSwgbmIpCiAgICByb3cgPSB7fQogICAgZm9yIGthIGluICgw
LjAwNSwgMC4wMiwgMC4wOCk6CiAgICAgICAgayA9IG5wLmFycmF5KFtrYSAvIEFfU1RBUiwgMC4w
XSk7IEwsIFggPSBMWChiLCBrKQogICAgICAgIHcyID0gbnAuc29ydF9jb21wbGV4KG5wLmxpbmFs
Zy5laWd2YWxzKEwgQCAoTCArIDIgKiBYKSkpWzozXS5yZWFsCiAgICAgICAgcm93WyJrYT0lLjNm
IiAlIGthXSA9IFtmbG9hdCh4KSBmb3IgeCBpbiB3Ml0KICAgICAgICBpZiBuYiA9PSAzMjoKICAg
ICAgICAgICAgZGlhZ1siaGVybWl0aWFuX2NsaXBwZWRfbG93ZXN0Il1bImthPSUuM2YiICUga2Fd
ID0gW2Zsb2F0KHgpIGZvciB4IGluIGIub21lZ2FzKGssIG5iYW5kcz0zKV0KICAgIGRpYWdbImdv
bGRzdG9uZV9vZmZzZXRfcHJvZHVjdF9mb3JtIl1bIm5fYj0lZCIgJSBuYl0gPSByb3cKYiA9IGd6
LkJkRyhjZWxsLCBwc2kwLCBNVSwgMzIpCkwwLCBYMCA9IExYKGIsIG5wLmFycmF5KFswLjAsIDAu
MF0pKQpjb2VmID0gbnAuZmZ0LmZmdDIocHNpMCkgLyBOKioyCmRlZiBwdyhmaWVsZCk6CiAgICBj
ID0gbnAuZmZ0LmZmdDIoZmllbGQpIC8gTioqMjsgdiA9IG5wLnplcm9zKGxlbihiLm0xKSwgY29t
cGxleCkKICAgIG9rID0gKG5wLmFicyhiLm0xKSA8IE4gLy8gMikgJiAobnAuYWJzKGIubTIpIDwg
TiAvLyAyKTsgdltva10gPSBjW2IubTFbb2tdICUgTiwgYi5tMltva10gJSBOXTsgcmV0dXJuIHYK
djAgPSBwdyhwc2kwKTsgdmQgPSBwdyhucC5mZnQuaWZmdDIoMWogKiBjZWxsLkd4ICogbnAuZmZ0
LmZmdDIocHNpMCkpLnJlYWwpCmRpYWdbIkxfcHNpMF9yZXNpZHVhbF9yZWwiXSA9IGZsb2F0KG5w
LmxpbmFsZy5ub3JtKEwwIEAgdjApIC8gbnAubGluYWxnLm5vcm0odjApKQpkaWFnWyJMX3BzaTBf
cmVzaWR1YWxfcmVsX292ZXJfbXUiXSA9IGRpYWdbIkxfcHNpMF9yZXNpZHVhbF9yZWwiXSAvIE1V
ICAgICAgIyA9IHRoZSByZWJ1aWxkJ3MgbG9nZ2VkIHJlc2lkdWFsX3BvbGlzaGVkCmRpYWdbIndh
cmRfcmVzaWR1YWxfdHJhbnNsYXRpb25fbW9kZV9yZWwiXSA9IGZsb2F0KG5wLmxpbmFsZy5ub3Jt
KChMMCArIDIgKiBYMCkgQCB2ZCkgLyBucC5saW5hbGcubm9ybSh2ZCkpClAgPSBucC5hYnMoY29l
ZikqKjI7IG0gPSBucC5mZnQuZmZ0ZnJlcShOLCAxIC8gTikuYXN0eXBlKGludCk7IE0xLCBNMiA9
IG5wLm1lc2hncmlkKG0sIG0sIGluZGV4aW5nPSJpaiIpOyBSID0gbnAuc3FydChNMSoqMiArIE0y
KioyKQpkaWFnWyJwc2kwX3NwZWN0cmFsX3dlaWdodF9iZXlvbmRfbTE2Il0gPSBmbG9hdChQW1Ig
Pj0gMTZdLnN1bSgpIC8gUC5zdW0oKSkKZGlhZ1sia2VybmVsX2dyaWRfdnNfYW5hbHl0aWNfbWF4
X2Fic19kaWZmIl0gPSBmbG9hdChucC5hYnMoY2VsbC5VayAtIGd6LlVfdGlsZGUobnAuc3FydChj
ZWxsLkd4KioyICsgY2VsbC5HeSoqMikpKS5tYXgoKSkKIyB3aGF0IHRoZSBsYWRkZXIgbmVlZHM6
IHxvbWVnYV4yIG9mZnNldHwgPDwgKGMga19taW4pXjIgd2l0aCBrX21pbiA9IDAuMDAxMTcvYSo7
IGMgdW5rbm93biBwcmUtUGhhc2UtMSwgc28gdGhlCiMgdGhyZXNob2xkIGlzIHN0YXRlZCBvbiB0
aGUgc3RhdGlvbmFyaXR5IHJlc2lkdWFsIHRoYXQgcHJvZHVjZWQgdGhlIG9mZnNldCAob2Zmc2V0
L3Jlc2lkdWFsIHJhdGlvIG1lYXN1cmVkIGhlcmUpLgpvZmYgPSBhYnMoZGlhZ1siZ29sZHN0b25l
X29mZnNldF9wcm9kdWN0X2Zvcm0iXVsibl9iPTMyIl1bImthPTAuMDA1Il1bMF0pCmRpYWdbIm9m
ZnNldF9wZXJfdW5pdF9yZXNpZHVhbCJdID0gb2ZmIC8gZGlhZ1siTF9wc2kwX3Jlc2lkdWFsX3Jl
bCJdCmRpYWdbIlBIQVNFMV9TVEFUSU9OQVJJVFlfVEhSRVNIT0xEX3Byb3Bvc2VkIl0gPSB7Ikxf
cHNpMF9yZXNpZHVhbF9yZWxfbWF4IjogMWUtMTAsICJnb2xkc3RvbmVfb21lZ2EyX29mZnNldF9h
YnNfbWF4IjogMWUtOCwKICAgICJyYXRpb25hbGUiOiAib2Zmc2V0IHNjYWxlcyB+JS4wZiB4IHJl
c2lkdWFsOyBhdCBrYT0xLjE3ZS0zIChrPSUuMmUpIGFuIGFjb3VzdGljIG9tZWdhXjIgfiAoYyBr
KV4yIGlzIE8oMWUtNi4uMWUtNSkgZm9yIGMgPSBPKDEuLjMpOyAxJSUgb2YgdGhhdCBpcyAxZS04
IiAlIChkaWFnWyJvZmZzZXRfcGVyX3VuaXRfcmVzaWR1YWwiXSwgTEFEREVSWy0xXSAvIEFfU1RB
Uil9CnN1YnN0cmF0ZV9yZWFkeSA9IG9mZiA8IDFlLTgKCiMgPT09PT09PT09PT09PT09PT09PT09
PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09IChCKSBhbmFseXRpYyBw
Nm0gY29udHJvbCAoaGFybW9uaWMgdHJpYW5ndWxhciBsYXR0aWNlKQpUSCA9IG5wLmFycmF5KFsw
LjAsIG5wLnBpIC8gMywgMiAqIG5wLnBpIC8gM10pCmRlZiBEX2N0cmwoa3gsIGt5KToKICAgIEQg
PSBucC56ZXJvcygoMiwgMikpCiAgICBmb3IgdCBpbiBUSDoKICAgICAgICBheCwgYXkgPSBucC5j
b3ModCksIG5wLnNpbih0KTsgZiA9IDIgKiAoMSAtIG5wLmNvcyhreCAqIGF4ICsga3kgKiBheSkp
CiAgICAgICAgRCArPSBmICogbnAub3V0ZXIoW2F4LCBheV0sIFtheCwgYXldKQogICAgcmV0dXJu
IEQKZGVmIG8yX29mKGtoYXQsIGUpOgogICAgIiIidHJhY2VsZXNzLXN0cmFpbiBmcmFjdGlvbiBv
ZiBTID0gKGkvMikoayBlXlQgKyBlIGteVCkgKGlkZW50aWNhbCBmb3JtdWxhIHRvIHRoZSBoYXJu
ZXNzJ3MgZml0X3BvbGFyaXNhdGlvbikuIiIiCiAgICBreCwga3kgPSBraGF0OyBTID0gMC41aiAq
IG5wLmFycmF5KFtbMiAqIGt4ICogZVswXSwga3ggKiBlWzFdICsga3kgKiBlWzBdXSwgW2t4ICog
ZVsxXSArIGt5ICogZVswXSwgMiAqIGt5ICogZVsxXV1dKQogICAgRTIgPSBTIC0gMC41ICogbnAu
dHJhY2UoUykgKiBucC5leWUoMik7IHJldHVybiBmbG9hdChucC5saW5hbGcubm9ybShFMikqKjIg
LyBucC5saW5hbGcubm9ybShTKSoqMikKZGVmIGFuYWx5dGljKHBzaSwgYnJhbmNoKToKICAgIGMy
ID0gbGFtYmRhIHAsIHE6IHN1bShucC5jb3MocHNpIC0gdCkqKnAgKiBucC5zaW4ocHNpIC0gdCkq
KnEgZm9yIHQgaW4gVEgpCiAgICBpZiBicmFuY2ggPT0gIkwiOiBzNCwgczYsIHM4ID0gYzIoNCwg
MCksIGMyKDYsIDApLCBjMig4LCAwKQogICAgZWxzZTogICAgICAgICAgICAgczQsIHM2LCBzOCA9
IGMyKDIsIDIpLCBjMig0LCAyKSwgYzIoNiwgMikKICAgIGFscGhhLCBiZXRhID0gLXM2IC8gKDEy
ICogczQpLCBzOCAvICgzNjAgKiBzNCkKICAgIHJldHVybiBmbG9hdChucC5zcXJ0KHM0KSksIGZs
b2F0KGFscGhhIC8gMiksIGZsb2F0KGJldGEgLyAyIC0gYWxwaGEqKjIgLyA4KQpkZWYgZml0X3Nw
ZWVkX2FuZF9yZXNpZHVhbChrYSwgb21lZ2EpOgogICAgIiIiRS00L0UtNSBwaXBlbGluZSBhcyBp
biB0aGUgaGFybmVzczogYyBmcm9tIG9tZWdhL2sgPSBjICsgYiAoa2EpXjIgb24gdGhlIHNtYWxs
LWsgZW5kLCB0aGVuIHIgPSBvbWVnYS8oYyBrKSAtIDEgZml0dGVkIG9uIHsoa2EpXjIsKGthKV40
fS4iIiIKICAgIHNtYWxsID0ga2EgPD0gMC4wMwogICAgWHMgPSBucC5zdGFjayhbbnAub25lcyhz
bWFsbC5zdW0oKSksIGthW3NtYWxsXSoqMl0sIGF4aXM9MSkKICAgIGMgPSBmbG9hdChucC5saW5h
bGcubHN0c3EoWHMsIG9tZWdhW3NtYWxsXSAvIGthW3NtYWxsXSwgcmNvbmQ9Tm9uZSlbMF1bMF0p
CiAgICByID0gb21lZ2EgLyAoYyAqIGthKSAtIDEuMAogICAgWCA9IG5wLnN0YWNrKFtrYSoqMiwg
a2EqKjRdLCBheGlzPTEpOyBjb2VmLCAqXyA9IG5wLmxpbmFsZy5sc3RzcShYLCByLCByY29uZD1O
b25lKQogICAgcmV0dXJuIGMsIGZsb2F0KGNvZWZbMF0pLCBmbG9hdChjb2VmWzFdKSwgcgpkZWYg
d2luZG93X2NpKGthLCBvbWVnYSwgZWRnZXM9KDAuMywgMC4xNSwgMC4wNzUpKToKICAgIGZ1bGwg
PSBmaXRfc3BlZWRfYW5kX3Jlc2lkdWFsKGthLCBvbWVnYSkKICAgIHJldHVybiBtYXgoYWJzKGZp
dF9zcGVlZF9hbmRfcmVzaWR1YWwoa2Fba2EgPD0gZV0sIG9tZWdhW2thIDw9IGVdKVsxXSAtIGZ1
bGxbMV0pIGZvciBlIGluIGVkZ2VzWzE6XSkKY3RybCA9IHsicHJvamVjdG9yX21pcnJvcl9saW5l
X2V4YWN0IjogVHJ1ZSwgIkYtQ1RSTC1MIjoge30sICJUX2JyYW5jaF9kaWFnbm9zdGljX0NPTlRS
T0xfTk9UX1ZFUkRJQ1QiOiB7fX0Ka2FzID0gbnAuc29ydChucC5jb25jYXRlbmF0ZShbTEFEREVS
LCBucC5hcnJheShbMC4wMDUsIDAuMDEsIDAuMDE1LCAwLjAyLCAwLjAzXSldKSkKZm9yIG5hbWUs
IHBzaSBpbiAoKCJHYW1tYS1LIiwgMC4wKSwgKCJHYW1tYS1NIiwgbnAucGkgLyA2KSk6CiAgICBr
aGF0ID0gbnAuYXJyYXkoW25wLmNvcyhwc2kpLCBucC5zaW4ocHNpKV0pCiAgICB3VCwgd0wgPSBb
XSwgW10KICAgIGZvciBrYSBpbiBrYXM6CiAgICAgICAgbGFtLCBWID0gbnAubGluYWxnLmVpZ2go
RF9jdHJsKCooa2EgKiBraGF0KSkpCiAgICAgICAgbzJzID0gW28yX29mKGtoYXQsIFZbOiwgal0p
IGZvciBqIGluIHJhbmdlKDIpXQogICAgICAgIGpUID0gaW50KG5wLmFyZ21heChvMnMpKTsgakwg
PSAxIC0galQKICAgICAgICBpZiBub3QgKGFicyhvMnNbalRdIC0gMS4wKSA8IDFlLTEyIGFuZCBh
YnMobzJzW2pMXSAtIDAuNSkgPCAxZS0xMik6IGN0cmxbInByb2plY3Rvcl9taXJyb3JfbGluZV9l
eGFjdCJdID0gRmFsc2UKICAgICAgICB3VC5hcHBlbmQobnAuc3FydChsYW1balRdKSk7IHdMLmFw
cGVuZChucC5zcXJ0KGxhbVtqTF0pKQogICAgd1QsIHdMID0gbnAuYXJyYXkod1QpLCBucC5hcnJh
eSh3TCkKICAgIGZvciBiciwgdyBpbiAoKCJMIiwgd0wpLCAoIlQiLCB3VCkpOgogICAgICAgIGMs
IGEyLCBhNCwgciA9IGZpdF9zcGVlZF9hbmRfcmVzaWR1YWwoa2FzLCB3KTsgY2kgPSB3aW5kb3df
Y2koa2FzLCB3KQogICAgICAgIGNhLCBhMmEsIGE0YSA9IGFuYWx5dGljKHBzaSwgYnIpCiAgICAg
ICAgcmVjID0geyJjX2ZpdCI6IGMsICJjX2FuYWx5dGljIjogY2EsICJhMl9maXQiOiBhMiwgImEy
X2FuYWx5dGljIjogYTJhLCAiYTRfZml0IjogYTQsICJhNF9hbmFseXRpYyI6IGE0YSwKICAgICAg
ICAgICAgICAgImNpX2EyX3dpbmRvdyI6IGNpLCAiYWJzX2Vycl9hMiI6IGFicyhhMiAtIGEyYSl9
CiAgICAgICAgaWYgYnIgPT0gIkwiOgogICAgICAgICAgICByZWNbImtub3duX25vbnplcm8iXSA9
IGJvb2woYWJzKGEyYSkgPiBUQVUpCiAgICAgICAgICAgIHJlY1sicGFzcyJdID0gYm9vbChhYnMo
YTIgLSBhMmEpIDw9IG1heChjaSwgVEFVKSBhbmQgYWJzKGEyYSkgPiBUQVUpCiAgICAgICAgICAg
IGN0cmxbIkYtQ1RSTC1MIl1bbmFtZV0gPSByZWMKICAgICAgICBlbHNlOgogICAgICAgICAgICBj
dHJsWyJUX2JyYW5jaF9kaWFnbm9zdGljX0NPTlRST0xfTk9UX1ZFUkRJQ1QiXVtuYW1lXSA9IHJl
YwojIGEyIHJlY292ZXJ5IHByZWNpc2lvbiBvZiB0aGUgZWxlY3RlZCB0d28tdGVybSBiYXNpcyBv
biB0aGUgZWxlY3RlZCB3aW5kb3cgKHRoZSBmaXR0ZXIncyBvd24gYmlhcywgY29udHJvbC1tZWFz
dXJlZCkKY3RybFsiZml0dGVyX2EyX2JpYXNfbWF4X2FicyJdID0gbWF4KHZbImFic19lcnJfYTIi
XSBmb3IgdiBpbiBjdHJsWyJGLUNUUkwtTCJdLnZhbHVlcygpKQoKIyA9PT09PT09PT09PT09PT09
PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT0gKEMpIEYtQ1RS
TC1JTkogKHN5bnRoZXRpYykKcm5nID0gbnAucmFuZG9tLmRlZmF1bHRfcm5nKDIwMjYwOTAyKTsg
YTJfaW5qLCBub2lzZSA9IDEwICogVEFVLCAxZS04ClggPSBucC5zdGFjayhbTEFEREVSKioyLCBM
QURERVIqKjRdLCBheGlzPTEpCnJlYyA9IG5wLmFycmF5KFtucC5saW5hbGcubHN0c3EoWCwgYTJf
aW5qICogTEFEREVSKioyICsgbm9pc2UgKiBybmcuc3RhbmRhcmRfbm9ybWFsKGxlbihMQURERVIp
KSwgcmNvbmQ9Tm9uZSlbMF1bMF0gZm9yIF8gaW4gcmFuZ2UoMjAwKV0pCmluaiA9IHsiYTJfaW5q
ZWN0ZWQiOiBhMl9pbmosICJub2lzZV9hYnMiOiBub2lzZSwgImEyX3JlY292ZXJlZF9tZWFuIjog
ZmxvYXQocmVjLm1lYW4oKSksICJhMl9yZWNvdmVyZWRfc2QiOiBmbG9hdChyZWMuc3RkKCkpLAog
ICAgICAgImNpOTUiOiBbZmxvYXQobnAucGVyY2VudGlsZShyZWMsIDIuNSkpLCBmbG9hdChucC5w
ZXJjZW50aWxlKHJlYywgOTcuNSkpXX0KaW5qWyJwYXNzIl0gPSBib29sKGFicyhyZWMubWVhbigp
IC0gYTJfaW5qKSA8PSBUQVUgYW5kIGlualsiY2k5NSJdWzBdIDw9IGEyX2luaiA8PSBpbmpbImNp
OTUiXVsxXSkKCiMgPT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09
PT09PT09PT09PT09PT09PT09IGNoZWNrcG9pbnQgKyByZXBvcnQKb3V0ID0geyJnYXRlIjogIkct
UzJDMSIsICJwaGFzZSI6IDAsICJsZWciOiAiY2hhdCIsICJzdGF0dXMiOiAiQ09OVFJPTC1OT1Qt
VkVSRElDVCIsICJQSEFTRTFfQVVUSE9SSVpFRCI6IFBIQVNFMV9BVVRIT1JJWkVELAogICAgICAg
InByZXJlZ19tZDUiOiAiMmVhOGVjMTNmZmEzYzMyODk4Y2MyNGEzYmU2MDVjNjQiLCAidDFfbWQ1
IjogbWQ1YihvcGVuKCIvaG9tZS9jbGF1ZGUvczJjL3QxX2ZvcmJpZGRlbl9HX1MyX09OX0NPTkUu
dHh0IiwgInJiIikucmVhZCgpKSwKICAgICAgICJsb2NrX3JlY29yZF9tZDUiOiAiZjJmNGQ1MDAy
OWZiNWJlMzEyMmE4ODVjNDhhN2UwNGYiLCAibGFkZGVyX2thIjogW2Zsb2F0KHgpIGZvciB4IGlu
IExBRERFUl0sICJ0YXUiOiBUQVUsCiAgICAgICAiQV9zdWJzdHJhdGVfZGlhZ25vc3RpYyI6IGRp
YWcsICJCX2FuYWx5dGljX2NvbnRyb2wiOiBjdHJsLCAiQ19GX0NUUkxfSU5KIjogaW5qLAogICAg
ICAgInJlYWRpbmVzcyI6IHsiaGFybmVzc19wcm9qZWN0b3JfZml0dGVyIjogIlJFQURZIiBpZiAo
Y3RybFsicHJvamVjdG9yX21pcnJvcl9saW5lX2V4YWN0Il0gYW5kIGFsbCh2WyJwYXNzIl0gZm9y
IHYgaW4gY3RybFsiRi1DVFJMLUwiXS52YWx1ZXMoKSkgYW5kIGlualsicGFzcyJdKSBlbHNlICJJ
TlNUUlVNRU5ULUxJTUlURUQiLAogICAgICAgICAgICAgICAgICAgICAic3Vic3RyYXRlX2d6MV9m
b3JfYWNvdXN0aWNfbGFkZGVyIjogIlJFQURZIiBpZiBzdWJzdHJhdGVfcmVhZHkgZWxzZSAiTk9U
IFJFQURZIOKAlCBzdGF0aW9uYXJpdHkvR29sZHN0b25lIG9mZnNldCAoc2VlIEEpOyBQaGFzZSAx
IHByZXJlcXVpc2l0ZTogcmUtY3J5c3RhbGxpemUgYXQgZ2VtOCAoRS0zKSB0byB0aGUgcHJvcG9z
ZWQgdGhyZXNob2xkIGFuZCB2ZXJpZnkgV0FSRC1HYW1tYSBiZWZvcmUgYW55IGxhZGRlciJ9fQpv
YiA9IChqc29uLmR1bXBzKG91dCwgaW5kZW50PTEsIHNvcnRfa2V5cz1UcnVlLCBkZWZhdWx0PXN0
cikgKyAiXG4iKS5lbmNvZGUoKQpvcGVuKCJnX3MyYzFfcGhhc2UwX2NoZWNrcG9pbnQuanNvbiIs
ICJ3YiIpLndyaXRlKG9iKQpwcmludCgiPT09IChBKSBTVUJTVFJBVEUgRElBR05PU1RJQyAocmVj
b3ZlcmVkIGd6MSBjcnlzdGFsKSA9PT0iKQpwcmludCgiTCBwc2kwIHJlc2lkdWFsIChyZWwpICUu
NGUgICg9ICUuM2UgeCBtdTsgcmVidWlsZCBsb2dnZWQgcmVzaWR1YWxfcG9saXNoZWQgMC4wMDIy
NykiICUgKGRpYWdbIkxfcHNpMF9yZXNpZHVhbF9yZWwiXSwgZGlhZ1siTF9wc2kwX3Jlc2lkdWFs
X3JlbF9vdmVyX211Il0pKQpwcmludCgiV2FyZCByZXNpZHVhbCBvbiB0cmFuc2xhdGlvbiBtb2Rl
IChMKzJYKSBkX3ggcHNpMDogJS40ZSIgJSBkaWFnWyJ3YXJkX3Jlc2lkdWFsX3RyYW5zbGF0aW9u
X21vZGVfcmVsIl0pCmZvciBuYiwgcm93IGluIGRpYWdbImdvbGRzdG9uZV9vZmZzZXRfcHJvZHVj
dF9mb3JtIl0uaXRlbXMoKTogcHJpbnQoInByb2R1Y3QtZm9ybSBsb3dlc3Qgb21lZ2FeMiAlczog
JXMiICUgKG5iLCB7azogW3JvdW5kKHgsIDQpIGZvciB4IGluIHZdIGZvciBrLCB2IGluIHJvdy5p
dGVtcygpfSkpCnByaW50KCJIZXJtaXRpYW4tY2xpcHBlZCBsb3dlc3Qgb21lZ2FzIChuX2I9MzIp
OiIsIHtrOiBbcm91bmQoeCwgNikgZm9yIHggaW4gdl0gZm9yIGssIHYgaW4gZGlhZ1siaGVybWl0
aWFuX2NsaXBwZWRfbG93ZXN0Il0uaXRlbXMoKX0pCnByaW50KCJwc2kwIHNwZWN0cmFsIHdlaWdo
dCBiZXlvbmQgfG18Pj0xNjogJS4xZSA7IGtlcm5lbCBncmlkLXZzLWFuYWx5dGljIG1heCBkaWZm
OiAlLjFlIiAlIChkaWFnWyJwc2kwX3NwZWN0cmFsX3dlaWdodF9iZXlvbmRfbTE2Il0sIGRpYWdb
Imtlcm5lbF9ncmlkX3ZzX2FuYWx5dGljX21heF9hYnNfZGlmZiJdKSkKcHJpbnQoIm9mZnNldCBw
ZXIgdW5pdCByZXNpZHVhbCB+ICUuMGYgOyBwcm9wb3NlZCBQaGFzZS0xIHRocmVzaG9sZHM6ICVz
IiAlIChkaWFnWyJvZmZzZXRfcGVyX3VuaXRfcmVzaWR1YWwiXSwgZGlhZ1siUEhBU0UxX1NUQVRJ
T05BUklUWV9USFJFU0hPTERfcHJvcG9zZWQiXSkpCnByaW50KCI9PT0gKEIpIEFOQUxZVElDIHA2
bSBDT05UUk9MID09PSIpCnByaW50KCJwcm9qZWN0b3IgbWlycm9yLWxpbmUgZXhhY3RuZXNzIChU
LT4xLCBMLT4xLzIpOiIsICJQQVNTIiBpZiBjdHJsWyJwcm9qZWN0b3JfbWlycm9yX2xpbmVfZXhh
Y3QiXSBlbHNlICJGQUlMIikKZm9yIG4sIHYgaW4gY3RybFsiRi1DVFJMLUwiXS5pdGVtcygpOiBw
cmludCgiRi1DVFJMLUwgJS04cyBjX2ZpdCAlLjZmIChhbiAlLjZmKSAgYTJfZml0ICUrLjZlIChh
biAlKy42ZSkgZXJyICUuMWUgY2kgJS4xZSAtPiAlcyIgJSAobiwgdlsiY19maXQiXSwgdlsiY19h
bmFseXRpYyJdLCB2WyJhMl9maXQiXSwgdlsiYTJfYW5hbHl0aWMiXSwgdlsiYWJzX2Vycl9hMiJd
LCB2WyJjaV9hMl93aW5kb3ciXSwgIlBBU1MiIGlmIHZbInBhc3MiXSBlbHNlICJGQUlMIikpCmZv
ciBuLCB2IGluIGN0cmxbIlRfYnJhbmNoX2RpYWdub3N0aWNfQ09OVFJPTF9OT1RfVkVSRElDVCJd
Lml0ZW1zKCk6IHByaW50KCJjb250cm9sLVQgJS04cyBhMl9maXQgJSsuNmUgKGFuICUrLjZlKSBh
NF9maXQgJSsuNGUgKGFuICUrLjRlKSIgJSAobiwgdlsiYTJfZml0Il0sIHZbImEyX2FuYWx5dGlj
Il0sIHZbImE0X2ZpdCJdLCB2WyJhNF9hbmFseXRpYyJdKSkKcHJpbnQoIj09PSAoQykgRi1DVFJM
LUlOSiA9PT0gaW5qZWN0ZWQgJS4xZSByZWNvdmVyZWQgJS40ZSArLy0gJS4xZSBDSTk1ICVzIC0+
ICVzIiAlIChhMl9pbmosIGlualsiYTJfcmVjb3ZlcmVkX21lYW4iXSwgaW5qWyJhMl9yZWNvdmVy
ZWRfc2QiXSwgW3JvdW5kKHgsIDkpIGZvciB4IGluIGlualsiY2k5NSJdXSwgIlBBU1MiIGlmIGlu
alsicGFzcyJdIGVsc2UgIkZBSUwiKSkKcHJpbnQoIlJFQURJTkVTUzoiLCBvdXRbInJlYWRpbmVz
cyJdKQpwcmludCgiY2hlY2twb2ludCBnX3MyYzFfcGhhc2UwX2NoZWNrcG9pbnQuanNvbiBtZDUg
JXMgKCVkIEIpIiAlIChtZDViKG9iKSwgbGVuKG9iKSkpCg==
<<<EMBED-END name=g_s2c1_phase0_close.py>>>

### EMBED — chat instrument — Phase 1 (halted at WARD) — `g_s2c1_phase1.py` (md5 c987a1a6f3ec8c3308dfb3bb1279bb09, 17227 B, b64, QUARANTINED)

<<<EMBED-BEGIN name=g_s2c1_phase1.py md5=c987a1a6f3ec8c3308dfb3bb1279bb09 bytes=17227 enc=b64 quarantine=1>>>
IyEvdXNyL2Jpbi9lbnYgcHl0aG9uMwoiIiJnX3MyYzFfcGhhc2UxLnB5IOKAlCBHYXRlIEctUzJD
MSAoZGlzcGxheTogR2F0ZSBHLVMyLU9OLUNPTkUpLCBQSEFTRSAxIChjaGF0IGxlZykuCkxvY2s6
IHByZXJlZyAyZWE4ZWMxM2ZmYTNjMzI4OThjYzI0YTNiZTYwNWM2NDsgVDEgOGNkODliOWE4Mjcw
NGFjY2Q4OWY3ZmY2ZjVlMjIwYjQ7IGxvY2sgcmVjb3JkIGYyZjRkNTAwOwpQaGFzZS0wIGNoZWNr
cG9pbnQgZWFlMmJiZDczNGY1MTI5ZGQxZTUxZWZjYmI1NWRkM2QuIFBIQVNFMV9BVVRIT1JJWkVE
ID0gVHJ1ZSAoYXV0aG9yIGRpcmVjdGl2ZSwgU2VwdCAyLCAyMDI2KS4KClN1YnN0cmF0ZSAoRS0z
LCByZWNvcmQgwqcyLjkxLksgRy1UU0gzIGZpcnN0IHBhc3NpbmcpOiAyLUQgR1AsIGhiYXIgPSBt
ID0gMSwgR0VNLTgga2VybmVsIFUocikgPSBnIGV4cCgtcl44KSwKZyogPSAyMCwgaGV4YWdvbmFs
IChwNm0pIGNlbGwgYSogPSAxLjQ2MDU5LCBtdSA9IDUzLjIyNSwgcmhvMCB+IDEgKHN1YnN0cmF0
ZSB1bml0cyB0aHJvdWdob3V0LCBUNCkuCkVuZXJneSBFW3BzaV0gPSBpbnQgMS8yfGdyYWQgcHNp
fF4yICsgMS8yIGludCBpbnQgcmhvIFUgcmhvIC0gbXUgaW50IHJobyAgKGd6MSBjb252ZW50aW9u
KS4KClN0ZXBzIChkaXJlY3RpdmUgMS00KToKIDEuIFJFLUNSWVNUQUxMSVpBVElPTiBhdCBmaXhl
ZCBtdTogc2VtaS1pbXBsaWNpdCBpbWFnaW5hcnkgdGltZSwgdGhlbiBOZXd0b24tS3J5bG92IHBv
bGlzaCB0bwogICAgfHxMIHBzaTB8fCAvIHx8cHNpMHx8IDw9IDFlLTEwICAoTCA9IC0xLzIgbGFw
IC0gbXUgKyBVKnJobzApLiAgSEFMVCBpZiBub3QgcmVhY2hlZC4KIDIuIFdBUkQtR2FtbWE6IHVu
LWNsaXBwZWQgcHJvZHVjdC1mb3JtIEJkRyBvbWVnYV4yID0gZWlnKEwoTCsyWCkpIGF0IEdhbW1h
IGFuZCBrYSA9IDAuMDA1OyB0aGUgdGhyZWUKICAgIEdvbGRzdG9uZSBtb2RlcyBtdXN0IHNhdGlz
ZnkgfG9tZWdhXjJ8IDw9IDFlLTguICBIQUxUIGlmIG5vdC4KIDMuIExBRERFUjogZHlhZGljIGth
IGluIFswLjMvMl44LCAwLjNdIChFLTQpLCBkaXJlY3Rpb25zIEdhbW1hLUsgYW5kIEdhbW1hLU0s
IG5fYiBpbiB7MzIsIDQwfTsgSGVybWl0aWFuCiAgICBCZEcgZm9ybSAoYWRtaXNzaWJsZSBvbmx5
IGJlY2F1c2UgbGFtYmRhX21pbihMKSA+PSAtMWUtMTIgYWZ0ZXIgdGhlIHBvbGlzaDsgY3Jvc3Mt
Y2hlY2tlZCBhZ2FpbnN0IHRoZQogICAgcHJvZHVjdCBmb3JtIGF0IHR3byBydW5ncyk7IGVpZ2Vu
dmVjdG9ycyAtPiBkZW5zaXR5LWZsdWN0dWF0aW9uIGFtcGxpdHVkZSBwc2kwKmYgLT4gcG9sYXJp
c2F0aW9uIGZpdCBvbnRvCiAgICB7ZF94IHJobzAsIGRfeSByaG8wLCByaG8wfSAtPiBvMiAodHJh
Y2VsZXNzLXN0cmFpbiBmcmFjdGlvbik7IFQgPSBicmFuY2ggb2YgbWF4aW1hbCBvMiAoPj0gdGhl
dGFfaWQgMC45MCk7CiAgICBjID0gbGltIG9tZWdhL2sgZnJvbSB0aGUgc3BlZWQgc2V0OyByKGsp
ID0gb21lZ2FfVC8oYyBrKSAtIDEgZml0dGVkIG9uIHsoa2EpXjIsKGthKV40fTsgd2luZG93LXN0
YWJpbGl0eSBDSS4KIDQuIENIRUNLUE9JTlQgKEYtRElTUCAvIEYtSVNPIC8gRi1NSVggLyBGLUNP
TlYgZXZhbHVhdGVkIGNoYXQtc2lkZTsgYXJtcyBOT1QgZGVjbGFyZWQg4oCUIHR3by1sZWcgKyBQ
aGFzZSAyLzMpLgoiIiIKaW1wb3J0IHN5cywgb3MsIGpzb24sIGhhc2hsaWIsIHRpbWUKaW1wb3J0
IG51bXB5IGFzIG5wCmZyb20gc2NpcHkuaW50ZWdyYXRlIGltcG9ydCBxdWFkCmZyb20gc2NpcHku
c3BlY2lhbCBpbXBvcnQgajAsIGdhbW1hIGFzIEdhbW1hCmZyb20gc2NpcHkuaW50ZXJwb2xhdGUg
aW1wb3J0IEN1YmljU3BsaW5lCmZyb20gc2NpcHkub3B0aW1pemUgaW1wb3J0IG5ld3Rvbl9rcnls
b3YKc3lzLnBhdGguaW5zZXJ0KDAsICIvaG9tZS9jbGF1ZGUvczJjL2d6MSIpCmltcG9ydCBnejFf
Y29yZSBhcyBnegpQSEFTRTFfQVVUSE9SSVpFRCA9IFRydWUKVDAgPSB0aW1lLnRpbWUoKQpkZWYg
bG9nKHMpOiBwcmludCgiWyU3LjFmc10gJXMiICUgKHRpbWUudGltZSgpIC0gVDAsIHMpLCBmbHVz
aD1UcnVlKQpkZWYgbWQ1YihiKTogcmV0dXJuIGhhc2hsaWIubWQ1KGIpLmhleGRpZ2VzdCgpCgpH
X1NUQVIsIEFfU1RBUiwgTVUgPSAyMC4wLCAxLjQ2MDU5LCA1My4yMjUKTiA9IDY0ClRBVSwgVEhF
VEFfSUQsIFRIRVRBX0lTTyA9IDFlLTYsIDAuOTAsIDAuMDEKTEFEREVSID0gWzAuMyAvIDIqKmog
Zm9yIGogaW4gcmFuZ2UoOSldClNQRUVEID0gWzAuMDA1LCAwLjAxLCAwLjAxNSwgMC4wMiwgMC4w
M10KVEhSX1JFUywgVEhSX1dBUkQgPSAxZS0xMCwgMWUtOAoKIyAtLS0tLS0tLS0tLS0tLS0tLS0t
LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0gMS4gZ2VtOCBr
ZXJuZWwgKDItRCBGVCwgdGFibGUgKyBzcGxpbmUpCmNsYXNzIEdlbThfMkQ6CiAgICAiIiJVX3Rp
bGRlKHEpID0gMiBwaSBnIGludF8wXmluZiByIGV4cCgtcl44KSBKMChxIHIpIGRyIDsgVV90aWxk
ZSgwKSA9IDIgcGkgZyBHYW1tYSgxLzQpLzguIiIiCiAgICBkZWYgX19pbml0X18oc2VsZiwgZywg
cW1heD0yMDAuMCwgbnE9NDAwMSk6CiAgICAgICAgc2VsZi5nID0gZzsgc2VsZi5VMCA9IDIgKiBu
cC5waSAqIGcgKiBHYW1tYSgwLjI1KSAvIDguMAogICAgICAgIHF0ID0gbnAubGluc3BhY2UoMC4w
LCBxbWF4LCBucSk7IHZhbHMgPSBucC5lbXB0eV9saWtlKHF0KTsgdmFsc1swXSA9IHNlbGYuVTAK
ICAgICAgICBmb3IgaSwgcSBpbiBlbnVtZXJhdGUocXRbMTpdLCAxKToKICAgICAgICAgICAgdiwg
XyA9IHF1YWQobGFtYmRhIHI6IHIgKiBucC5leHAoLXIqKjgpICogajAocSAqIHIpLCAwLjAsIDIu
NSwgbGltaXQ9NDAwLCBlcHNhYnM9MWUtMTMsIGVwc3JlbD0xZS0xMikKICAgICAgICAgICAgdmFs
c1tpXSA9IDIgKiBucC5waSAqIGcgKiB2CiAgICAgICAgc2VsZi5zcGxpbmUgPSBDdWJpY1NwbGlu
ZShxdCwgdmFscyk7IHNlbGYucW1heCA9IHFtYXgKICAgIGRlZiBfX2NhbGxfXyhzZWxmLCBxKToK
ICAgICAgICBxID0gbnAuYXNhcnJheShxLCBmbG9hdCk7IHJldHVybiBucC53aGVyZShxID4gc2Vs
Zi5xbWF4LCAwLjAsIHNlbGYuc3BsaW5lKG5wLm1pbmltdW0ocSwgc2VsZi5xbWF4KSkpCmxvZygi
YnVpbGRpbmcgZ2VtOCBrZXJuZWwgdGFibGUiKQpLRVIgPSBHZW04XzJEKEdfU1RBUikKY2VsbCA9
IGd6LkNlbGwoQV9TVEFSLCBOKTsgY2VsbC5VayA9IEtFUihucC5zcXJ0KGNlbGwuRzIpKSAgICAg
IyBvdmVycmlkZSB0aGUgc29mdC1kaXNrIGtlcm5lbCBvbiB0aGUgY2VsbCBncmlkCksyID0gY2Vs
bC5HMgpsb2coImtlcm5lbCBVKDApID0gJS42ZiA7IFUofGIxfCkgPSAlLjZmIiAlIChLRVIuVTAs
IEtFUihucC5saW5hbGcubm9ybShjZWxsLmIxKSkpKQoKIyAtLS0tLS0tLS0tLS0tLS0tLS0tLS0t
LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0gR1Agb3BlcmF0b3Jz
IG9uIHRoZSBoZXggY2VsbCAoZnJhY3Rpb25hbCBncmlkLCBGRlQpCmRlZiBjb252KGZpZWxkKTog
cmV0dXJuIG5wLmZmdC5pZmZ0MihjZWxsLlVrICogbnAuZmZ0LmZmdDIoZmllbGQpKS5yZWFsCmRl
ZiBMb3AocHNpLCBmKToKICAgICIiIihMIGYpID0gLTEvMiBsYXAgZiAtIG11IGYgKyAoVSpyaG8w
KSBmICB3aXRoIHJobzAgPSBwc2leMi4iIiIKICAgIHJldHVybiBucC5mZnQuaWZmdDIoMC41ICog
SzIgKiBucC5mZnQuZmZ0MihmKSkucmVhbCAtIE1VICogZiArIGNvbnYocHNpICogcHNpKSAqIGYK
ZGVmIHJlc2lkdWFsKHBzaSk6CiAgICByID0gTG9wKHBzaSwgcHNpKTsgcmV0dXJuIGZsb2F0KG5w
LnNxcnQoKHIgKiByKS5tZWFuKCkgLyAocHNpICogcHNpKS5tZWFuKCkpKQoKIyBzZWVkOiBnejEg
cG9saXNoZWQgc3RhdGUgKGhleCwgb25lIHBlYWsgcGVyIGNlbGwpIHJldXNlZCBhcyB0aGUgaW5p
dGlhbCBndWVzcywgcmVub3JtYWxpc2VkIHRvIDxyaG8+ID0gMQpwc2kgPSBucC5sb2FkKCIvaG9t
ZS9jbGF1ZGUvczJjL2d6MS9wc2kwX3BvbGlzaGVkX242NC5ucHkiKS5hc3R5cGUoZmxvYXQpCnBz
aSAvPSBucC5zcXJ0KChwc2kgKiBwc2kpLm1lYW4oKSkKbG9nKCJzZWVkIHJlc2lkdWFsICUuM2Ui
ICUgcmVzaWR1YWwocHNpKSkKIyBzZW1pLWltcGxpY2l0IGltYWdpbmFyeSB0aW1lIGF0IEZJWEVE
IG11OiAoMSArIGR0LzIgSzIpIHBzaV9uZXcgPSBwc2kgKyBkdCoobXUgcHNpIC0gKFUqcmhvKSBw
c2kpCmR0ID0gMC4wMDQ7IGRlbm9tID0gMS4wICsgMC41ICogZHQgKiBLMgpmb3IgaXQgaW4gcmFu
Z2UoMSwgNDAwMDEpOgogICAgcmhzID0gcHNpICsgZHQgKiAoTVUgKiBwc2kgLSBjb252KHBzaSAq
IHBzaSkgKiBwc2kpCiAgICBwc2lfbmV3ID0gbnAuZmZ0LmlmZnQyKG5wLmZmdC5mZnQyKHJocykg
LyBkZW5vbSkucmVhbAogICAgaWYgbm90IG5wLmFsbChucC5pc2Zpbml0ZShwc2lfbmV3KSk6IGxv
ZygiaW1hZ2luYXJ5LXRpbWUgYmxvdy11cCDigJQgaGFsdmluZyBkdCIpOyBkdCAqPSAwLjU7IGRl
bm9tID0gMS4wICsgMC41ICogZHQgKiBLMjsgY29udGludWUKICAgIHBzaSA9IHBzaV9uZXcKICAg
IGlmIGl0ICUgMjAwMCA9PSAwOgogICAgICAgIHJlcyA9IHJlc2lkdWFsKHBzaSk7IGxvZygiICBp
bWFnLXRpbWUgaXQgJTVkIHJlc2lkdWFsICUuM2UgPHJobz4gJS42ZiIgJSAoaXQsIHJlcywgKHBz
aSAqIHBzaSkubWVhbigpKSkKICAgICAgICBpZiByZXMgPCAxZS03OiBicmVhawpyZXNfaXQgPSBy
ZXNpZHVhbChwc2kpOyBsb2coImltYWdpbmFyeS10aW1lIGRvbmU6IHJlc2lkdWFsICUuM2UsIDxy
aG8+ID0gJS42ZiIgJSAocmVzX2l0LCAocHNpICogcHNpKS5tZWFuKCkpKQojIE5ld3Rvbi1Lcnls
b3YgcG9saXNoIHRvIHRoZSBzdHJpY3QgdGhyZXNob2xkCmRlZiBGKHYpOiByZXR1cm4gTG9wKHYu
cmVzaGFwZShOLCBOKSwgdi5yZXNoYXBlKE4sIE4pKS5yYXZlbCgpCnggPSBwc2kucmF2ZWwoKS5j
b3B5KCk7IHJlc19uayA9IHJlc19pdApmb3Igcm5kIGluIHJhbmdlKDYpOgogICAgdHJ5OgogICAg
ICAgIHggPSBuZXd0b25fa3J5bG92KEYsIHgsIGZfdG9sPTFlLTE0LCBmX3J0b2w9MWUtMTQsIG1h
eGl0ZXI9MzAsIG1ldGhvZD0ibGdtcmVzIiwgaW5uZXJfbWF4aXRlcj02MCwgdmVyYm9zZT1GYWxz
ZSkKICAgIGV4Y2VwdCBFeGNlcHRpb24gYXMgZToKICAgICAgICBsb2coIm5ld3Rvbl9rcnlsb3Yg
cm91bmQgJWQgZW5kZWQ6ICVzIiAlIChybmQsIHN0cihlKVs6ODBdKSkKICAgIHJlc19uayA9IHJl
c2lkdWFsKHgucmVzaGFwZShOLCBOKSk7IGxvZygiICBOSyByb3VuZCAlZCByZXNpZHVhbCAlLjNl
IiAlIChybmQsIHJlc19uaykpCiAgICBpZiByZXNfbmsgPD0gVEhSX1JFUzogYnJlYWsKcHNpMCA9
IHgucmVzaGFwZShOLCBOKQpyaG8wID0gcHNpMCAqIHBzaTA7IG1lYW5fcmhvID0gZmxvYXQocmhv
MC5tZWFuKCkpCmNvZWYgPSBucC5mZnQuZmZ0Mihwc2kwKSAvIE4qKjI7IFAgPSBucC5hYnMoY29l
ZikqKjIKbSA9IG5wLmZmdC5mZnRmcmVxKE4sIDEgLyBOKS5hc3R5cGUoaW50KTsgTTEsIE0yID0g
bnAubWVzaGdyaWQobSwgbSwgaW5kZXhpbmc9ImlqIik7IFIgPSBucC5zcXJ0KE0xKioyICsgTTIq
KjIpCnNwZWMyNCA9IGZsb2F0KFBbUiA+PSAyNF0uc3VtKCkgLyBQLnN1bSgpKQpFX2tpbiA9IDAu
NSAqIG5wLnN1bShLMiAqIG5wLmFicyhjb2VmKSoqMik7IHJoYXQgPSBucC5mZnQuZmZ0MihyaG8w
KSAvIE4qKjI7IEVfaW50ID0gMC41ICogbnAuc3VtKGNlbGwuVWsgKiBucC5hYnMocmhhdCkqKjIp
CnN0ZXAxID0geyJyZXNpZHVhbF9pbWFnaW5hcnlfdGltZSI6IHJlc19pdCwgInJlc2lkdWFsX2Fm
dGVyX05LIjogcmVzX25rLCAidGhyZXNob2xkIjogVEhSX1JFUywgInBhc3MiOiBib29sKHJlc19u
ayA8PSBUSFJfUkVTKSwKICAgICAgICAgIm1lYW5fcmhvIjogbWVhbl9yaG8sICJlbmVyZ3lfcGVy
X2FyZWFfa2luIjogZmxvYXQoRV9raW4pLCAiZW5lcmd5X3Blcl9hcmVhX2ludCI6IGZsb2F0KEVf
aW50KSwKICAgICAgICAgInBzaTBfc3BlY3RyYWxfd2VpZ2h0X2JleW9uZF9tMjQiOiBzcGVjMjQs
ICJwc2kwX21kNSI6IG1kNWIocHNpMC50b2J5dGVzKCkpLCAiZ3JpZF9uIjogTiwKICAgICAgICAg
ImJyYWdnX3BlYWtfcmF0aW9fcmhvIjogZmxvYXQobnAuc29ydChucC5hYnMocmhhdCkucmF2ZWwo
KSlbLTJdIC8gbnAuYWJzKHJoYXRbMCwgMF0pKX0KbnAuc2F2ZSgicHNpMF9nZW04X242NC5ucHki
LCBwc2kwKQpsb2coIlNURVAgMSAlczogcmVzaWR1YWwgJS4zZSAodGhyICUuMGUpLCA8cmhvPiAl
LjZmLCBzcGVjdHJhbCB0YWlsKHxtfD49MjQpICUuMWUiICUgKCJQQVNTIiBpZiBzdGVwMVsicGFz
cyJdIGVsc2UgIkZBSUwiLCByZXNfbmssIFRIUl9SRVMsIG1lYW5fcmhvLCBzcGVjMjQpKQppZiBu
b3Qgc3RlcDFbInBhc3MiXToKICAgIGpzb24uZHVtcCh7InN0ZXAxIjogc3RlcDEsICJoYWx0Ijog
IlJFLUNSWVNUQUxMSVpBVElPTiBUSFJFU0hPTEQgTk9UIFJFQUNIRUQifSwgb3BlbigiZ19zMmMx
X3BoYXNlMV9jaGVja3BvaW50Lmpzb24iLCAidyIpLCBpbmRlbnQ9MSk7IHN5cy5leGl0KDIpCgoj
IC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0t
LS0tLS0tLS0tLSBCZEcgKHBsYW5lIHdhdmVzKSB3aXRoIHRoZSBnZW04IGtlcm5lbApjbGFzcyBC
ZEc6CiAgICBkZWYgX19pbml0X18oc2VsZiwgbl9iKToKICAgICAgICBzZWxmLm5fYiA9IG5fYjsg
biA9IE4KICAgICAgICBjID0gbnAuZmZ0LmZmdDIocHNpMCkgLyBuKioyOyByYyA9IG5wLmZmdC5m
ZnQyKHJobzApIC8gbioqMjsgVmMgPSBjZWxsLlVrICogcmMKICAgICAgICBtbSA9IG5wLmZmdC5m
ZnRmcmVxKG5fYiwgZD0xLjAgLyBuX2IpLmFzdHlwZShpbnQpOyBNTTEsIE1NMiA9IG5wLm1lc2hn
cmlkKG1tLCBtbSwgaW5kZXhpbmc9ImlqIikKICAgICAgICBzZWxmLm0xLCBzZWxmLm0yID0gTU0x
LnJhdmVsKCksIE1NMi5yYXZlbCgpCiAgICAgICAgZGVmIGxvb2soQywgZDEsIGQyKToKICAgICAg
ICAgICAgb3V0ID0gbnAuemVyb3MoZDEuc2hhcGUsIGNvbXBsZXgpOyBvayA9IChucC5hYnMoZDEp
IDwgbiAvLyAyKSAmIChucC5hYnMoZDIpIDwgbiAvLyAyKQogICAgICAgICAgICBvdXRbb2tdID0g
Q1tkMVtva10gJSBuLCBkMltva10gJSBuXTsgcmV0dXJuIG91dAogICAgICAgIEQxID0gc2VsZi5t
MVs6LCBOb25lXSAtIHNlbGYubTFbTm9uZSwgOl07IEQyID0gc2VsZi5tMls6LCBOb25lXSAtIHNl
bGYubTJbTm9uZSwgOl0KICAgICAgICBzZWxmLlAgPSBsb29rKGMsIEQxLCBEMik7IHNlbGYuUCA9
IDAuNSAqIChzZWxmLlAgKyBzZWxmLlAuY29uaigpLlQpCiAgICAgICAgc2VsZi5WID0gbG9vayhW
YywgRDEsIEQyKTsgc2VsZi5WID0gMC41ICogKHNlbGYuViArIHNlbGYuVi5jb25qKCkuVCkKICAg
ICAgICBzZWxmLmtneDAgPSBzZWxmLm0xICogY2VsbC5iMVswXSArIHNlbGYubTIgKiBjZWxsLmIy
WzBdOyBzZWxmLmtneTAgPSBzZWxmLm0xICogY2VsbC5iMVsxXSArIHNlbGYubTIgKiBjZWxsLmIy
WzFdCiAgICBkZWYgTFgoc2VsZiwgayk6CiAgICAgICAga2d4LCBrZ3kgPSBrWzBdICsgc2VsZi5r
Z3gwLCBrWzFdICsgc2VsZi5rZ3kwCiAgICAgICAgTCA9IG5wLmRpYWcoMC41ICogKGtneCoqMiAr
IGtneSoqMikgLSBNVSkgKyBzZWxmLlY7IEwgPSAwLjUgKiAoTCArIEwuY29uaigpLlQpCiAgICAg
ICAgRCA9IEtFUihucC5zcXJ0KGtneCoqMiArIGtneSoqMikpOyBYID0gc2VsZi5QIEAgKERbOiwg
Tm9uZV0gKiBzZWxmLlApOyBYID0gMC41ICogKFggKyBYLmNvbmooKS5UKQogICAgICAgIHJldHVy
biBMLCBYCiAgICBkZWYgcHJvZHVjdF93MihzZWxmLCBrLCBubG93PTMpOgogICAgICAgIEwsIFgg
PSBzZWxmLkxYKGspOyB3MiA9IG5wLmxpbmFsZy5laWd2YWxzKEwgQCAoTCArIDIgKiBYKSk7IGkg
PSBucC5hcmdzb3J0KHcyLnJlYWwpWzpubG93XTsgcmV0dXJuIHcyW2ldCiAgICBkZWYgbW9kZXMo
c2VsZiwgaywgbmJhbmRzPTgpOgogICAgICAgIEwsIFggPSBzZWxmLkxYKGspOyBsYW0sIFUgPSBu
cC5saW5hbGcuZWlnaChMKTsgbGFtX21pbiA9IGZsb2F0KGxhbVswXSkKICAgICAgICBsYW0gPSBu
cC53aGVyZShsYW0gPCAwLCAwLjAsIGxhbSkgICAgICAgICAgICAgICAgICAgICAgICMgYWRtaXNz
aWJsZSBvbmx5IHdoZW4gbGFtX21pbiA+PSAtMWUtMTIgKGNoZWNrZWQpCiAgICAgICAgTGggPSAo
VSAqIG5wLnNxcnQobGFtKSkgQCBVLmNvbmooKS5UCiAgICAgICAgTSA9IExoIEAgKEwgKyAyLjAg
KiBYKSBAIExoOyBNID0gMC41ICogKE0gKyBNLmNvbmooKS5UKQogICAgICAgIHcyLCBIID0gbnAu
bGluYWxnLmVpZ2goTSk7IGlkeCA9IG5wLmFyZ3NvcnQodzIpWzpuYmFuZHNdCiAgICAgICAgdyA9
IG5wLnNxcnQobnAuY2xpcCh3MltpZHhdLCAwLjAsIE5vbmUpKTsgRnYgPSBMaCBAIEhbOiwgaWR4
XSAgICAgICMgZiA9IHUgKyB2CiAgICAgICAgYW1wcyA9IFtdCiAgICAgICAgZm9yIGogaW4gcmFu
Z2UobGVuKGlkeCkpOgogICAgICAgICAgICBjZiA9IG5wLnplcm9zKChOLCBOKSwgY29tcGxleCk7
IG9rID0gKG5wLmFicyhzZWxmLm0xKSA8IE4gLy8gMikgJiAobnAuYWJzKHNlbGYubTIpIDwgTiAv
LyAyKQogICAgICAgICAgICBjZltzZWxmLm0xW29rXSAlIE4sIHNlbGYubTJbb2tdICUgTl0gPSBG
dltvaywgal0KICAgICAgICAgICAgYW1wcy5hcHBlbmQocHNpMCAqIChucC5mZnQuaWZmdDIoY2Yp
ICogTioqMikpCiAgICAgICAgcmV0dXJuIHcsIGFtcHMsIGxhbV9taW4sIHcyW2lkeF0KCiMgLS0t
LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0t
LS0tLS0tIDIuIFdBUkQtR2FtbWEKYjMyID0gQmRHKDMyKQp3MkcgPSBiMzIucHJvZHVjdF93Mihu
cC5hcnJheShbMC4wLCAwLjBdKSk7IHcyayA9IGIzMi5wcm9kdWN0X3cyKG5wLmFycmF5KFswLjAw
NSAvIEFfU1RBUiwgMC4wXSkpCmxhbV9taW5fRyA9IGZsb2F0KG5wLmxpbmFsZy5laWd2YWxzaChi
MzIuTFgobnAuYXJyYXkoWzAuMCwgMC4wXSkpWzBdKVswXSkKd2FyZCA9IHsicHJvZHVjdF9mb3Jt
X3cyX0dhbW1hXzNsb3dlc3QiOiBbW2Zsb2F0KHoucmVhbCksIGZsb2F0KHouaW1hZyldIGZvciB6
IGluIHcyR10sCiAgICAgICAgInByb2R1Y3RfZm9ybV93Ml9rYTAuMDA1XzNsb3dlc3QiOiBbW2Zs
b2F0KHoucmVhbCksIGZsb2F0KHouaW1hZyldIGZvciB6IGluIHcya10sCiAgICAgICAgImxhbWJk
YV9taW5fTF9HYW1tYSI6IGxhbV9taW5fRywgInRocmVzaG9sZF9hYnNfdzIiOiBUSFJfV0FSRCwK
ICAgICAgICAicGFzcyI6IGJvb2wobWF4KGFicyh6KSBmb3IgeiBpbiB3MkcpIDw9IFRIUl9XQVJE
IGFuZCBsYW1fbWluX0cgPj0gLTFlLTEyKX0KbG9nKCJTVEVQIDIgV0FSRC1HYW1tYSAlczogfHcy
fCBhdCBHYW1tYSAlcyA7IGxhbWJkYV9taW4oTCkgJS4yZSIgJSAoIlBBU1MiIGlmIHdhcmRbInBh
c3MiXSBlbHNlICJGQUlMIiwgWyIlLjJlIiAlIGFicyh6KSBmb3IgeiBpbiB3MkddLCBsYW1fbWlu
X0cpKQppZiBub3Qgd2FyZFsicGFzcyJdOgogICAganNvbi5kdW1wKHsic3RlcDEiOiBzdGVwMSwg
InN0ZXAyX3dhcmQiOiB3YXJkLCAiaGFsdCI6ICJXQVJELUdBTU1BIEZBSUxFRCJ9LCBvcGVuKCJn
X3MyYzFfcGhhc2UxX2NoZWNrcG9pbnQuanNvbiIsICJ3IiksIGluZGVudD0xKTsgc3lzLmV4aXQo
MikKCiMgLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0t
LS0tLS0tLS0tLS0tLS0tIDMuIGxhZGRlcgpkZWYgY2VsbF9ncmFkKGZpZWxkKToKICAgIEZoID0g
bnAuZmZ0LmZmdDIoZmllbGQpOyByZXR1cm4gbnAuZmZ0LmlmZnQyKDFqICogY2VsbC5HeCAqIEZo
KS5yZWFsLCBucC5mZnQuaWZmdDIoMWogKiBjZWxsLkd5ICogRmgpLnJlYWwKRFJYLCBEUlkgPSBj
ZWxsX2dyYWQocmhvMCkKQkFTSVMgPSBucC5zdGFjayhbRFJYLnJhdmVsKCksIERSWS5yYXZlbCgp
LCByaG8wLnJhdmVsKCldLCBheGlzPTEpLmFzdHlwZShjb21wbGV4KQpkZWYgcG9sYXJpc2F0aW9u
KHdfYW1wLCBrKToKICAgIGNmLCAqXyA9IG5wLmxpbmFsZy5sc3RzcShCQVNJUywgd19hbXAucmF2
ZWwoKSwgcmNvbmQ9Tm9uZSkKICAgIHJlc2lkID0gd19hbXAucmF2ZWwoKSAtIEJBU0lTIEAgY2Y7
IFIyID0gMS4wIC0gbnAudmRvdChyZXNpZCwgcmVzaWQpLnJlYWwgLyBucC52ZG90KHdfYW1wLnJh
dmVsKCksIHdfYW1wLnJhdmVsKCkpLnJlYWwKICAgIGEgPSBjZls6Ml07IGdzID0gbnAubGluYWxn
Lm5vcm0oQkFTSVNbOiwgOjJdIEAgYSkqKjIgLyBtYXgobnAubGluYWxnLm5vcm0oQkFTSVMgQCBj
ZikqKjIsIDFlLTMwMCkKICAgIGt4LCBreSA9IGs7IFMgPSAwLjVqICogbnAuYXJyYXkoW1syICog
a3ggKiBhWzBdLCBreCAqIGFbMV0gKyBreSAqIGFbMF1dLCBba3ggKiBhWzFdICsga3kgKiBhWzBd
LCAyICoga3kgKiBhWzFdXV0pCiAgICBFMiA9IFMgLSAwLjUgKiBucC50cmFjZShTKSAqIG5wLmV5
ZSgyKTsgblMgPSBucC5saW5hbGcubm9ybShTKSoqMgogICAgcmV0dXJuIGZsb2F0KFIyKSwgZmxv
YXQoZ3MpLCAoZmxvYXQobnAubGluYWxnLm5vcm0oRTIpKioyIC8gblMpIGlmIG5TID4gMCBlbHNl
IGZsb2F0KCJuYW4iKSkKZGVmIGNsYXNzaWZ5KGssIHcsIGFtcHMpOgogICAgcm93cyA9IFtdCiAg
ICBmb3IgaiBpbiByYW5nZShsZW4odykpOgogICAgICAgIFIyLCBncywgbzIgPSBwb2xhcmlzYXRp
b24oYW1wc1tqXSwgayk7IHJvd3MuYXBwZW5kKGRpY3Qoaj1qLCBvbWVnYT1mbG9hdCh3W2pdKSwg
UjI9UjIsIGdyYWRfc2hhcmU9Z3MsIG8yPW8yKSkKICAgIGxhdCA9IFtyIGZvciByIGluIHJvd3Mg
aWYgclsiUjIiXSA+PSAwLjkwIGFuZCByWyJncmFkX3NoYXJlIl0gPj0gMC41XQogICAgVCA9IG1h
eChsYXQsIGtleT1sYW1iZGEgcjogclsibzIiXSkgaWYgbGF0IGVsc2UgTm9uZQogICAgTHMgPSBb
ciBmb3IgciBpbiBsYXQgaWYgciBpcyBub3QgVCBhbmQgclsibzIiXSA8IFRIRVRBX0lEXTsgTDEg
PSBtaW4oTHMsIGtleT1sYW1iZGEgcjogclsib21lZ2EiXSkgaWYgTHMgZWxzZSBOb25lCiAgICBv
dGhlcnMgPSBbciBmb3IgciBpbiByb3dzIGlmIHIgaXMgbm90IFQgYW5kIHIgaXMgbm90IEwxXTsg
UEggPSBtaW4ob3RoZXJzLCBrZXk9bGFtYmRhIHI6IHJbIm9tZWdhIl0pIGlmIG90aGVycyBlbHNl
IE5vbmUKICAgIHJldHVybiByb3dzLCBULCBMMSwgUEgKZGVmIGt2ZWMoa2EsIGQpOgogICAgayA9
IGthIC8gQV9TVEFSOyB0aCA9IDAuMCBpZiBkID09ICJHSyIgZWxzZSAtbnAucGkgLyA2LjA7IHJl
dHVybiBucC5hcnJheShbayAqIG5wLmNvcyh0aCksIGsgKiBucC5zaW4odGgpXSkKZGVmIGZpdF9y
KGthLCByKToKICAgIFggPSBucC5zdGFjayhba2EqKjIsIGthKio0XSwgYXhpcz0xKTsgY2YsICpf
ID0gbnAubGluYWxnLmxzdHNxKFgsIHIsIHJjb25kPU5vbmUpCiAgICByZXR1cm4gZmxvYXQoY2Zb
MF0pLCBmbG9hdChjZlsxXSksIGZsb2F0KG5wLnNxcnQobnAubWVhbigociAtIFggQCBjZikqKjIp
KSkKZGVmIHJ1bihuX2IpOgogICAgYmRnID0gQmRHKG5fYik7IG91dCA9IHsibl9iIjogbl9iLCAi
c3BlZWRzIjoge30sICJUIjoge30sICJMMSI6IHt9LCAiaWRlbnQiOiB7fSwgImZtaXhfbWluX28y
X1QiOiB7fSwgImxhbV9taW5fTF9taW4iOiAwLjAsICJ4Y2hlY2tfcHJvZHVjdF92c19oZXJtaXRp
YW4iOiB7fX0KICAgIGZvciBkIGluICgiR0siLCAiR00iKToKICAgICAgICBjVCwgY0wsIGNQLCBr
YXMgPSBbXSwgW10sIFtdLCBbXQogICAgICAgIGZvciBrYSBpbiBTUEVFRDoKICAgICAgICAgICAg
ayA9IGt2ZWMoa2EsIGQpOyB3LCBhbXBzLCBsbW4sIF8gPSBiZGcubW9kZXMoayk7IG91dFsibGFt
X21pbl9MX21pbiJdID0gbWluKG91dFsibGFtX21pbl9MX21pbiJdLCBsbW4pCiAgICAgICAgICAg
IHJvd3MsIFQsIEwxLCBQSCA9IGNsYXNzaWZ5KGssIHcsIGFtcHMpCiAgICAgICAgICAgIGlmIFQg
aXMgTm9uZSBvciBMMSBpcyBOb25lIG9yIFBIIGlzIE5vbmU6IGxvZygiICBbJXMgJWQga2E9JS40
Zl0gY2xhc3NpZmljYXRpb24gaW5jb21wbGV0ZSAlcyIgJSAoZCwgbl9iLCBrYSwgWyhyWyJqIl0s
IHJvdW5kKHJbIlIyIl0sIDMpLCByb3VuZChyWyJvMiJdLCAzKSkgZm9yIHIgaW4gcm93c1s6NV1d
KSk7IGNvbnRpbnVlCiAgICAgICAgICAgIGthcy5hcHBlbmQoa2EpOyBjVC5hcHBlbmQoVFsib21l
Z2EiXSAvIChrYSAvIEFfU1RBUikpOyBjTC5hcHBlbmQoTDFbIm9tZWdhIl0gLyAoa2EgLyBBX1NU
QVIpKTsgY1AuYXBwZW5kKFBIWyJvbWVnYSJdIC8gKGthIC8gQV9TVEFSKSkKICAgICAgICBYID0g
bnAuc3RhY2soW25wLm9uZXMobGVuKGthcykpLCBucC5hcnJheShrYXMpKioyXSwgYXhpcz0xKTsg
c3AgPSB7fQogICAgICAgIGZvciBubSwgYXJyIGluICgoIlQiLCBjVCksICgiTDEiLCBjTCksICgi
UEgiLCBjUCkpOiBzcFtubV0gPSBmbG9hdChucC5saW5hbGcubHN0c3EoWCwgbnAuYXJyYXkoYXJy
KSwgcmNvbmQ9Tm9uZSlbMF1bMF0pCiAgICAgICAgb3V0WyJzcGVlZHMiXVtkXSA9IHNwOyBsb2co
IiAgWyVzIG5fYj0lZF0gc3BlZWRzIGstPjA6IFBIICUuNWYgIFQgJS41ZiAgTDEgJS41ZiAgKFJf
VCA9IGNfVC9jX0wxID0gJS41ZikiICUgKGQsIG5fYiwgc3BbIlBIIl0sIHNwWyJUIl0sIHNwWyJM
MSJdLCBzcFsiVCJdIC8gc3BbIkwxIl0pKQogICAgICAgIHJULCByTCwgdXNlZCwgbzJUID0gW10s
IFtdLCBbXSwgW10KICAgICAgICBmb3Iga2EgaW4gTEFEREVSOgogICAgICAgICAgICBrID0ga3Zl
YyhrYSwgZCk7IHcsIGFtcHMsIGxtbiwgdzIgPSBiZGcubW9kZXMoayk7IG91dFsibGFtX21pbl9M
X21pbiJdID0gbWluKG91dFsibGFtX21pbl9MX21pbiJdLCBsbW4pCiAgICAgICAgICAgIHJvd3Ms
IFQsIEwxLCBQSCA9IGNsYXNzaWZ5KGssIHcsIGFtcHMpCiAgICAgICAgICAgIGlmIFQgaXMgTm9u
ZSBvciBMMSBpcyBOb25lOiBsb2coIiAgWyVzIG5fYj0lZCBsYWRkZXIga2E9JS41Zl0gY2xhc3Np
ZmljYXRpb24gaW5jb21wbGV0ZSDigJQgZHJvcHBlZCwgbG9nZ2VkIiAlIChkLCBuX2IsIGthKSk7
IGNvbnRpbnVlCiAgICAgICAgICAgIHVzZWQuYXBwZW5kKGthKTsgclQuYXBwZW5kKFRbIm9tZWdh
Il0gLyAoc3BbIlQiXSAqIGthIC8gQV9TVEFSKSAtIDEuMCk7IHJMLmFwcGVuZChMMVsib21lZ2Ei
XSAvIChzcFsiTDEiXSAqIGthIC8gQV9TVEFSKSAtIDEuMCk7IG8yVC5hcHBlbmQoVFsibzIiXSkK
ICAgICAgICAgICAgb3V0WyJpZGVudCJdLnNldGRlZmF1bHQoZCwgW10pLmFwcGVuZChkaWN0KGth
PWthLCBUPWRpY3Qoaj1UWyJqIl0sIG9tZWdhPVRbIm9tZWdhIl0sIFIyPXJvdW5kKFRbIlIyIl0s
IDUpLCBvMj1yb3VuZChUWyJvMiJdLCA1KSksIEwxPWRpY3Qoaj1MMVsiaiJdLCBvbWVnYT1MMVsi
b21lZ2EiXSwgbzI9cm91bmQoTDFbIm8yIl0sIDUpKSwgUEg9ZGljdChqPVBIWyJqIl0sIG9tZWdh
PVBIWyJvbWVnYSJdKSBpZiBQSCBlbHNlIE5vbmUpKQogICAgICAgICAgICBpZiBrYSBpbiAoTEFE
REVSWzBdLCBMQURERVJbNF0pOgogICAgICAgICAgICAgICAgcHcyID0gYmRnLnByb2R1Y3RfdzIo
aywgbmxvdz00KTsgb3V0WyJ4Y2hlY2tfcHJvZHVjdF92c19oZXJtaXRpYW4iXVsiJXNfa2E9JS40
ZiIgJSAoZCwga2EpXSA9IHsicHJvZHVjdCI6IFtmbG9hdCh6LnJlYWwpIGZvciB6IGluIHB3Ml0s
ICJoZXJtaXRpYW4iOiBbZmxvYXQoeikgZm9yIHogaW4gdzJbOjRdXX0KICAgICAgICBrYV91ID0g
bnAuYXJyYXkodXNlZCkKICAgICAgICBmb3Igbm0sIHIgaW4gKCgiVCIsIHJUKSwgKCJMMSIsIHJM
KSk6CiAgICAgICAgICAgIGEyLCBhNCwgcm1zID0gZml0X3Ioa2FfdSwgbnAuYXJyYXkocikpCiAg
ICAgICAgICAgIGVkZ2VzID0gKDAuMywgMC4xNSwgMC4wNzUpOyBjaXMgPSBbZml0X3Ioa2FfdVtr
YV91IDw9IGVdLCBucC5hcnJheShyKVtrYV91IDw9IGVdKSBmb3IgZSBpbiBlZGdlc1sxOl1dCiAg
ICAgICAgICAgIG91dFtubV1bZF0gPSBkaWN0KGthPXVzZWQsIHI9W2Zsb2F0KHgpIGZvciB4IGlu
IHJdLCBhMj1hMiwgYTQ9YTQsIGZpdF9ybXM9cm1zLCBjaV9hMj1tYXgoYWJzKGNbMF0gLSBhMikg
Zm9yIGMgaW4gY2lzKSwgY2lfYTQ9bWF4KGFicyhjWzFdIC0gYTQpIGZvciBjIGluIGNpcykpCiAg
ICAgICAgb3V0WyJmbWl4X21pbl9vMl9UIl1bZF0gPSBmbG9hdChtaW4obzJUKSkKICAgICAgICBs
b2coIiAgWyVzIG5fYj0lZF0gVDogYTIgPSAlKy42ZSAoY2kgJS4xZSkgIGE0ID0gJSsuNmUgKGNp
ICUuMWUpICBybXMgJS4xZSB8IEwxIGNvbnRyb2w6IGEyID0gJSsuNmUgfCBtaW4gbzIoVCkgJS40
ZiIgJSAoZCwgbl9iLCBvdXRbIlQiXVtkXVsiYTIiXSwgb3V0WyJUIl1bZF1bImNpX2EyIl0sIG91
dFsiVCJdW2RdWyJhNCJdLCBvdXRbIlQiXVtkXVsiY2lfYTQiXSwgb3V0WyJUIl1bZF1bImZpdF9y
bXMiXSwgb3V0WyJMMSJdW2RdWyJhMiJdLCBvdXRbImZtaXhfbWluX28yX1QiXVtkXSkpCiAgICBy
ZXR1cm4gb3V0CnJ1bnMgPSB7fQpmb3Igbl9iIGluICgzMiwgNDApOgogICAgbG9nKCI9PT0gbGFk
ZGVyIG5fYiA9ICVkID09PSIgJSBuX2IpOyBydW5zW3N0cihuX2IpXSA9IHJ1bihuX2IpCnIzMiwg
cjQwID0gcnVuc1siMzIiXSwgcnVuc1siNDAiXQpjb252ID0ge30KZm9yIGQgaW4gKCJHSyIsICJH
TSIpOgogICAgZm9yIG5tIGluICgiVCIsICJMMSIsICJQSCIpOiBjb252WyJjXyVzXyVzX3JlbCIg
JSAobm0sIGQpXSA9IGFicyhyNDBbInNwZWVkcyJdW2RdW25tXSAvIHIzMlsic3BlZWRzIl1bZF1b
bm1dIC0gMS4wKQogICAgY29udlsiYTJfVF8lc19hYnMiICUgZF0gPSBhYnMocjQwWyJUIl1bZF1b
ImEyIl0gLSByMzJbIlQiXVtkXVsiYTIiXSk7IGNvbnZbImE0X1RfJXNfYWJzIiAlIGRdID0gYWJz
KHI0MFsiVCJdW2RdWyJhNCJdIC0gcjMyWyJUIl1bZF1bImE0Il0pCmZjb252X3Bhc3MgPSBhbGwo
Y29udlsiY19UXyVzX3JlbCIgJSBkXSA8PSAxZS02IGFuZCBjb252WyJhMl9UXyVzX2FicyIgJSBk
XSA8PSAxZS03IGZvciBkIGluICgiR0siLCAiR00iKSkKaXNvX1QgPSBhYnMocjQwWyJzcGVlZHMi
XVsiR0siXVsiVCJdIC8gcjQwWyJzcGVlZHMiXVsiR00iXVsiVCJdIC0gMS4wKQpmbWl4X3Bhc3Mg
PSBhbGwocjQwWyJmbWl4X21pbl9vMl9UIl1bZF0gPj0gVEhFVEFfSUQgZm9yIGQgaW4gKCJHSyIs
ICJHTSIpKQpmZGlzcCA9IHtkOiB7ImEyIjogcjQwWyJUIl1bZF1bImEyIl0sICJhNCI6IHI0MFsi
VCJdW2RdWyJhNCJdLCAiY2lfYTIiOiByNDBbIlQiXVtkXVsiY2lfYTIiXSwgImNpX2E0IjogcjQw
WyJUIl1bZF1bImNpX2E0Il0sCiAgICAgICAgICAgICAiYTJfemVyb19hdF90YXUiOiBib29sKGFi
cyhyNDBbIlQiXVtkXVsiYTIiXSkgPD0gbWF4KFRBVSwgcjQwWyJUIl1bZF1bImNpX2EyIl0pKSwg
ImE0X3plcm9fYXRfdGF1IjogYm9vbChhYnMocjQwWyJUIl1bZF1bImE0Il0pIDw9IG1heChUQVUs
IHI0MFsiVCJdW2RdWyJjaV9hNCJdKSl9IGZvciBkIGluICgiR0siLCAiR00iKX0KY2sgPSB7Imdh
dGUiOiAiRy1TMkMxIiwgInBoYXNlIjogMSwgImxlZyI6ICJjaGF0IiwgIlBIQVNFMV9BVVRIT1JJ
WkVEIjogVHJ1ZSwgInByZXJlZ19tZDUiOiAiMmVhOGVjMTNmZmEzYzMyODk4Y2MyNGEzYmU2MDVj
NjQiLAogICAgICAidDFfbWQ1IjogIjhjZDg5YjlhODI3MDRhY2NkODlmN2ZmNmY1ZTIyMGI0Iiwg
ImxvY2tfcmVjb3JkX21kNSI6ICJmMmY0ZDUwMDI5ZmI1YmUzMTIyYTg4NWM0OGE3ZTA0ZiIsICJw
aGFzZTBfbWQ1IjogImVhZTJiYmQ3MzRmNTEyOWRkMWU1MWVmY2JiNTVkZDNkIiwKICAgICAgInN1
YnN0cmF0ZSI6IHsia2VybmVsIjogIkdFTS04IGcgZXhwKC1yXjgpLCAyLUQiLCAiZyI6IEdfU1RB
UiwgImFfc3RhciI6IEFfU1RBUiwgIm11IjogTVUsICJncmlkX24iOiBOLCAia2VybmVsX1UwIjog
S0VSLlUwfSwKICAgICAgInN0ZXAxX3JlY3J5c3RhbGxpemF0aW9uIjogc3RlcDEsICJzdGVwMl93
YXJkX2dhbW1hIjogd2FyZCwgInN0ZXAzX2xhZGRlciI6IHsibGFkZGVyX2thIjogTEFEREVSLCAi
c3BlZWRfa2EiOiBTUEVFRCwgInJ1bnMiOiBydW5zfSwKICAgICAgIkZfQ09OVl8zMl92c180MCI6
IGNvbnYsICJGX0NPTlZfcGFzcyI6IGZjb252X3Bhc3MsICJGX0lTT19jVF9zcGxpdCI6IGlzb19U
LCAiRl9JU09fcGFzcyI6IGJvb2woaXNvX1QgPD0gVEhFVEFfSVNPKSwKICAgICAgIkZfTUlYX3Bh
c3MiOiBmbWl4X3Bhc3MsICJGX0RJU1BfY2hhdGxlZyI6IGZkaXNwLCAidGF1IjogVEFVLCAidGhl
dGFfaWQiOiBUSEVUQV9JRCwgInRoZXRhX2lzbyI6IFRIRVRBX0lTTywKICAgICAgImFybXMiOiAi
Tk9UIERFQ0xBUkVEIOKAlCB0d28tbGVnIGNvbXBhcmlzb24gKENDKSBhbmQgUGhhc2UgMi8zIChh
Z2dyZWdhdGUpIHBlbmRpbmc7IGNoYXQtbGVnIHNpbmdsZS1jcnlzdGFsIHJlc3VsdCBvbmx5In0K
b2IgPSAoanNvbi5kdW1wcyhjaywgaW5kZW50PTEsIHNvcnRfa2V5cz1UcnVlLCBkZWZhdWx0PXN0
cikgKyAiXG4iKS5lbmNvZGUoKTsgb3BlbigiZ19zMmMxX3BoYXNlMV9jaGVja3BvaW50Lmpzb24i
LCAid2IiKS53cml0ZShvYikKbG9nKCJGLUNPTlYgMzItPjQwOiAiICsgIiwgIi5qb2luKCIlcz0l
LjJlIiAlIGt2IGZvciBrdiBpbiBjb252Lml0ZW1zKCkpICsgIiAgLT4gJXMiICUgKCJQQVNTIiBp
ZiBmY29udl9wYXNzIGVsc2UgIkZBSUwiKSkKbG9nKCJGLUlTTyBjX1Qgc3BsaXQgR0svR00gPSAl
LjNlIC0+ICVzIDsgRi1NSVggbWluIG8yKFQpICVzIC0+ICVzIiAlIChpc29fVCwgIlBBU1MiIGlm
IGlzb19UIDw9IFRIRVRBX0lTTyBlbHNlICJGQUlMIiwgcjQwWyJmbWl4X21pbl9vMl9UIl0sICJQ
QVNTIiBpZiBmbWl4X3Bhc3MgZWxzZSAiRkFJTCIpKQpmb3IgZCBpbiAoIkdLIiwgIkdNIik6IGxv
ZygiRi1ESVNQIGNoYXQtbGVnICVzOiBhMiA9ICUrLjZlIChjaSAlLjFlKSB6ZXJvQHRhdT0lcyA7
IGE0ID0gJSsuNmUgKGNpICUuMWUpIHplcm9AdGF1PSVzIiAlIChkLCBmZGlzcFtkXVsiYTIiXSwg
ZmRpc3BbZF1bImNpX2EyIl0sIGZkaXNwW2RdWyJhMl96ZXJvX2F0X3RhdSJdLCBmZGlzcFtkXVsi
YTQiXSwgZmRpc3BbZF1bImNpX2E0Il0sIGZkaXNwW2RdWyJhNF96ZXJvX2F0X3RhdSJdKSkKbG9n
KCJjaGVja3BvaW50IGdfczJjMV9waGFzZTFfY2hlY2twb2ludC5qc29uIG1kNSAlcyAoJWQgQikg
OyBwc2kwX2dlbThfbjY0Lm5weSBtZDUgJXMiICUgKG1kNWIob2IpLCBsZW4ob2IpLCBzdGVwMVsi
cHNpMF9tZDUiXSkpCg==
<<<EMBED-END name=g_s2c1_phase1.py>>>

### EMBED — chat instrument — Phase 1 ladder (staged) — `g_s2c1_phase1_ladder.py` (md5 a9949649af4a2e99e3ae69186a066c23, 21163 B, b64, QUARANTINED)

<<<EMBED-BEGIN name=g_s2c1_phase1_ladder.py md5=a9949649af4a2e99e3ae69186a066c23 bytes=21163 enc=b64 quarantine=1>>>
IyEvdXNyL2Jpbi9lbnYgcHl0aG9uMwoiIiJnX3MyYzFfcGhhc2UxX2xhZGRlci5weSDigJQgR2F0
ZSBHLVMyQzEgKGRpc3BsYXk6IEdhdGUgRy1TMi1PTi1DT05FKSwgUEhBU0UgMSBMQURERVIgKGNo
YXQgbGVnKS4KTG9jazogcHJlcmVnIDJlYThlYzEzOyBUMSA4Y2Q4OWI5YTsgbG9jayByZWNvcmQg
ZjJmNGQ1MDA7IEFEREVORFVNIEEtMSA4YmY1MWJkMCAoV0FSRC1HYW1tYSByZWRlZmluZWQ6Cihh
KSBhbmFseXRpYy1tb2RlIFdhcmQgcmVzaWR1YWwgPD0gMWUtOSBBTkQgKGIpIEhlcm1pdGlhbi1m
b3JtIEdvbGRzdG9uZSB8b21lZ2FeMnwgPD0gMWUtOCB3aXRoIGxhbWJkYV9taW4oTCkgPj0gLTFl
LTEyCmF0IEVWRVJZIGspLiBBdXRob3IgZGlyZWN0aXZlIFNlcHRlbWJlciAzLCAyMDI2LiBQSEFT
RTFfQVVUSE9SSVpFRCA9IFRydWUuCkRlcml2ZWQgZnJvbSB0aGUgaGFsdGVkIGdfczJjMV9waGFz
ZTEucHkgKGM5ODdhMWE2KToga2VybmVsIHRhYmxlLCBoZXggY2VsbCwgR1Agb3BlcmF0b3JzLCBC
ZEcgKEhlcm1pdGlhbiBmb3JtIG9mIHJlY29yZAp3aXRoIGVpZ2VudmVjdG9yczsgcHJvZHVjdC1m
b3JtIGNyb3NzLWNoZWNrKSwgcG9sYXJpc2F0aW9uIGZpdCwgY2xhc3NpZmllciwga3ZlYywgZml0
X3IgY29waWVkIFZFUkJBVElNLiBTdGVwIDEgcmVwbGFjZWQgYnkKbG9hZGluZyB0aGUgYmFua2Vk
IGdlbTggc3RhdGUgcHNpMF9nZW04X242NC5ucHkgKGFycmF5IG1kNSBhc3NlcnRlZCBiMjdmYTAw
NC4uLjsgcmVzaWR1YWwgcmUtdmVyaWZpZWQgPD0gMWUtMTApLiBTdGVwIDIgPSBBLTEuCkxhZGRl
ciBhdCBuX2IgaW4gezI0LCAzMiwgNDB9OyBwcm9kdWN0LWZvcm0gY3Jvc3MtY2hlY2tzIGF0IExB
RERFUlswXSBhbmQgTEFEREVSWzRdOyBGLUNPTlYgYWNyb3NzIDI0LzMyLzQwOyB0aGUgZGVuc2Ug
Zmxvb3IKZW50ZXJzIHRoZSBhMiBDSSB0aHJvdWdoIHRoZSBuX2ItY2hhbmdlIHRlcm0uIFQxIHNl
bGYtc2NhbiBhdCBzdGFydC4gU3Vic3RyYXRlIHVuaXRzIHRocm91Z2hvdXQuCiIiIgppbXBvcnQg
c3lzLCBvcywganNvbiwgaGFzaGxpYiwgdGltZQppbXBvcnQgbnVtcHkgYXMgbnAKZnJvbSBzY2lw
eS5pbnRlZ3JhdGUgaW1wb3J0IHF1YWQKZnJvbSBzY2lweS5zcGVjaWFsIGltcG9ydCBqMCwgZ2Ft
bWEgYXMgR2FtbWEKZnJvbSBzY2lweS5pbnRlcnBvbGF0ZSBpbXBvcnQgQ3ViaWNTcGxpbmUKZnJv
bSBzY2lweS5vcHRpbWl6ZSBpbXBvcnQgbmV3dG9uX2tyeWxvdgpzeXMucGF0aC5pbnNlcnQoMCwg
Ii9ob21lL2NsYXVkZS9zMmMvZ3oxIikKaW1wb3J0IGd6MV9jb3JlIGFzIGd6ClBIQVNFMV9BVVRI
T1JJWkVEID0gVHJ1ZQpUMCA9IHRpbWUudGltZSgpCmRlZiBsb2cocyk6IHByaW50KCJbJTcuMWZz
XSAlcyIgJSAodGltZS50aW1lKCkgLSBUMCwgcyksIGZsdXNoPVRydWUpCmRlZiBtZDViKGIpOiBy
ZXR1cm4gaGFzaGxpYi5tZDUoYikuaGV4ZGlnZXN0KCkKCkdfU1RBUiwgQV9TVEFSLCBNVSA9IDIw
LjAsIDEuNDYwNTksIDUzLjIyNQpOID0gNjQKVEFVLCBUSEVUQV9JRCwgVEhFVEFfSVNPID0gMWUt
NiwgMC45MCwgMC4wMQpMQURERVIgPSBbMC4zIC8gMioqaiBmb3IgaiBpbiByYW5nZSg5KV0KU1BF
RUQgPSBbMC4wMDUsIDAuMDEsIDAuMDE1LCAwLjAyLCAwLjAzXQpUSFJfUkVTLCBUSFJfV0FSRCA9
IDFlLTEwLCAxZS04CgojIC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0t
LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLSAxLiBnZW04IGtlcm5lbCAoMi1EIEZULCB0YWJsZSAr
IHNwbGluZSkKY2xhc3MgR2VtOF8yRDoKICAgICIiIlVfdGlsZGUocSkgPSAyIHBpIGcgaW50XzBe
aW5mIHIgZXhwKC1yXjgpIEowKHEgcikgZHIgOyBVX3RpbGRlKDApID0gMiBwaSBnIEdhbW1hKDEv
NCkvOC4iIiIKICAgIGRlZiBfX2luaXRfXyhzZWxmLCBnLCBxbWF4PTIwMC4wLCBucT00MDAxKToK
ICAgICAgICBzZWxmLmcgPSBnOyBzZWxmLlUwID0gMiAqIG5wLnBpICogZyAqIEdhbW1hKDAuMjUp
IC8gOC4wCiAgICAgICAgcXQgPSBucC5saW5zcGFjZSgwLjAsIHFtYXgsIG5xKTsgdmFscyA9IG5w
LmVtcHR5X2xpa2UocXQpOyB2YWxzWzBdID0gc2VsZi5VMAogICAgICAgIGZvciBpLCBxIGluIGVu
dW1lcmF0ZShxdFsxOl0sIDEpOgogICAgICAgICAgICB2LCBfID0gcXVhZChsYW1iZGEgcjogciAq
IG5wLmV4cCgtcioqOCkgKiBqMChxICogciksIDAuMCwgMi41LCBsaW1pdD00MDAsIGVwc2Ficz0x
ZS0xMywgZXBzcmVsPTFlLTEyKQogICAgICAgICAgICB2YWxzW2ldID0gMiAqIG5wLnBpICogZyAq
IHYKICAgICAgICBzZWxmLnNwbGluZSA9IEN1YmljU3BsaW5lKHF0LCB2YWxzKTsgc2VsZi5xbWF4
ID0gcW1heAogICAgZGVmIF9fY2FsbF9fKHNlbGYsIHEpOgogICAgICAgIHEgPSBucC5hc2FycmF5
KHEsIGZsb2F0KTsgcmV0dXJuIG5wLndoZXJlKHEgPiBzZWxmLnFtYXgsIDAuMCwgc2VsZi5zcGxp
bmUobnAubWluaW11bShxLCBzZWxmLnFtYXgpKSkKbG9nKCJidWlsZGluZyBnZW04IGtlcm5lbCB0
YWJsZSIpCktFUiA9IEdlbThfMkQoR19TVEFSKQpjZWxsID0gZ3ouQ2VsbChBX1NUQVIsIE4pOyBj
ZWxsLlVrID0gS0VSKG5wLnNxcnQoY2VsbC5HMikpICAgICAjIG92ZXJyaWRlIHRoZSBzb2Z0LWRp
c2sga2VybmVsIG9uIHRoZSBjZWxsIGdyaWQKSzIgPSBjZWxsLkcyCmxvZygia2VybmVsIFUoMCkg
PSAlLjZmIDsgVSh8YjF8KSA9ICUuNmYiICUgKEtFUi5VMCwgS0VSKG5wLmxpbmFsZy5ub3JtKGNl
bGwuYjEpKSkpCgojIC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0t
LS0tLS0tLS0tLS0tLS0tLS0tLS0tLSBHUCBvcGVyYXRvcnMgb24gdGhlIGhleCBjZWxsIChmcmFj
dGlvbmFsIGdyaWQsIEZGVCkKZGVmIGNvbnYoZmllbGQpOiByZXR1cm4gbnAuZmZ0LmlmZnQyKGNl
bGwuVWsgKiBucC5mZnQuZmZ0MihmaWVsZCkpLnJlYWwKZGVmIExvcChwc2ksIGYpOgogICAgIiIi
KEwgZikgPSAtMS8yIGxhcCBmIC0gbXUgZiArIChVKnJobzApIGYgIHdpdGggcmhvMCA9IHBzaV4y
LiIiIgogICAgcmV0dXJuIG5wLmZmdC5pZmZ0MigwLjUgKiBLMiAqIG5wLmZmdC5mZnQyKGYpKS5y
ZWFsIC0gTVUgKiBmICsgY29udihwc2kgKiBwc2kpICogZgpkZWYgcmVzaWR1YWwocHNpKToKICAg
IHIgPSBMb3AocHNpLCBwc2kpOyByZXR1cm4gZmxvYXQobnAuc3FydCgociAqIHIpLm1lYW4oKSAv
IChwc2kgKiBwc2kpLm1lYW4oKSkpCgojIHNlZWQ6IGd6MSBwb2xpc2hlZCBzdGF0ZSAoaGV4LCBv
bmUgcGVhayBwZXIgY2VsbCkgcmV1c2VkIGFzIHRoZSBpbml0aWFsIGd1ZXNzLCByZW5vcm1hbGlz
ZWQgdG8gPHJobz4gPSAxCgojIC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0t
LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLSAxLiBiYW5rZWQgZ2VtOCBzdGF0ZSAoUGhhc2Ug
MSBpdGVtIDEsIFBBU1NFRCkKcHNpMCA9IG5wLmxvYWQoIi9ob21lL2NsYXVkZS9zMmMvcHNpMF9n
ZW04X242NC5ucHkiKS5hc3R5cGUoZmxvYXQpCmFzc2VydCBoYXNobGliLm1kNShwc2kwLnRvYnl0
ZXMoKSkuaGV4ZGlnZXN0KCkgPT0gImIyN2ZhMDA0OTVlZjY4NmIwMTg0ZWEyOWM0NTViNGRiIiwg
ImJhbmtlZCBwc2kwIG1kNSBtaXNtYXRjaCIKcmhvMCA9IHBzaTAgKiBwc2kwCnJlczAgPSByZXNp
ZHVhbChwc2kwKQphc3NlcnQgcmVzMCA8PSBUSFJfUkVTLCAiYmFua2VkIHN0YXRlIHJlc2lkdWFs
ICUuM2UgPiAlLjFlIiAlIChyZXMwLCBUSFJfUkVTKQpzdGVwMSA9IHsicHNpMF9tZDUiOiAiYjI3
ZmEwMDQ5NWVmNjg2YjAxODRlYTI5YzQ1NWI0ZGIiLCAicmVzaWR1YWxfcmV2ZXJpZmllZCI6IGZs
b2F0KHJlczApLCAibWVhbl9yaG8iOiBmbG9hdChyaG8wLm1lYW4oKSksICJzb3VyY2UiOiAiUGhh
c2UtMSBpdGVtIDEgKGhhbHQgcmVwb3J0IGIwZTY3OTBjKSJ9CmxvZygiU1RFUCAxIGJhbmtlZCBz
dGF0ZTogcmVzaWR1YWwgJS4zZSA8PSAlLjBlIDsgPHJobz4gPSAlLjZmIiAlIChyZXMwLCBUSFJf
UkVTLCByaG8wLm1lYW4oKSkpCgpjbGFzcyBCZEc6CiAgICBkZWYgX19pbml0X18oc2VsZiwgbl9i
KToKICAgICAgICBzZWxmLm5fYiA9IG5fYjsgbiA9IE4KICAgICAgICBjID0gbnAuZmZ0LmZmdDIo
cHNpMCkgLyBuKioyOyByYyA9IG5wLmZmdC5mZnQyKHJobzApIC8gbioqMjsgVmMgPSBjZWxsLlVr
ICogcmMKICAgICAgICBtbSA9IG5wLmZmdC5mZnRmcmVxKG5fYiwgZD0xLjAgLyBuX2IpLmFzdHlw
ZShpbnQpOyBNTTEsIE1NMiA9IG5wLm1lc2hncmlkKG1tLCBtbSwgaW5kZXhpbmc9ImlqIikKICAg
ICAgICBzZWxmLm0xLCBzZWxmLm0yID0gTU0xLnJhdmVsKCksIE1NMi5yYXZlbCgpCiAgICAgICAg
ZGVmIGxvb2soQywgZDEsIGQyKToKICAgICAgICAgICAgb3V0ID0gbnAuemVyb3MoZDEuc2hhcGUs
IGNvbXBsZXgpOyBvayA9IChucC5hYnMoZDEpIDwgbiAvLyAyKSAmIChucC5hYnMoZDIpIDwgbiAv
LyAyKQogICAgICAgICAgICBvdXRbb2tdID0gQ1tkMVtva10gJSBuLCBkMltva10gJSBuXTsgcmV0
dXJuIG91dAogICAgICAgIEQxID0gc2VsZi5tMVs6LCBOb25lXSAtIHNlbGYubTFbTm9uZSwgOl07
IEQyID0gc2VsZi5tMls6LCBOb25lXSAtIHNlbGYubTJbTm9uZSwgOl0KICAgICAgICBzZWxmLlAg
PSBsb29rKGMsIEQxLCBEMik7IHNlbGYuUCA9IDAuNSAqIChzZWxmLlAgKyBzZWxmLlAuY29uaigp
LlQpCiAgICAgICAgc2VsZi5WID0gbG9vayhWYywgRDEsIEQyKTsgc2VsZi5WID0gMC41ICogKHNl
bGYuViArIHNlbGYuVi5jb25qKCkuVCkKICAgICAgICBzZWxmLmtneDAgPSBzZWxmLm0xICogY2Vs
bC5iMVswXSArIHNlbGYubTIgKiBjZWxsLmIyWzBdOyBzZWxmLmtneTAgPSBzZWxmLm0xICogY2Vs
bC5iMVsxXSArIHNlbGYubTIgKiBjZWxsLmIyWzFdCiAgICBkZWYgTFgoc2VsZiwgayk6CiAgICAg
ICAga2d4LCBrZ3kgPSBrWzBdICsgc2VsZi5rZ3gwLCBrWzFdICsgc2VsZi5rZ3kwCiAgICAgICAg
TCA9IG5wLmRpYWcoMC41ICogKGtneCoqMiArIGtneSoqMikgLSBNVSkgKyBzZWxmLlY7IEwgPSAw
LjUgKiAoTCArIEwuY29uaigpLlQpCiAgICAgICAgRCA9IEtFUihucC5zcXJ0KGtneCoqMiArIGtn
eSoqMikpOyBYID0gc2VsZi5QIEAgKERbOiwgTm9uZV0gKiBzZWxmLlApOyBYID0gMC41ICogKFgg
KyBYLmNvbmooKS5UKQogICAgICAgIHJldHVybiBMLCBYCiAgICBkZWYgcHJvZHVjdF93MihzZWxm
LCBrLCBubG93PTMpOgogICAgICAgIEwsIFggPSBzZWxmLkxYKGspOyB3MiA9IG5wLmxpbmFsZy5l
aWd2YWxzKEwgQCAoTCArIDIgKiBYKSk7IGkgPSBucC5hcmdzb3J0KHcyLnJlYWwpWzpubG93XTsg
cmV0dXJuIHcyW2ldCiAgICBkZWYgbW9kZXMoc2VsZiwgaywgbmJhbmRzPTgpOgogICAgICAgIEws
IFggPSBzZWxmLkxYKGspOyBsYW0sIFUgPSBucC5saW5hbGcuZWlnaChMKTsgbGFtX21pbiA9IGZs
b2F0KGxhbVswXSkKICAgICAgICBsYW0gPSBucC53aGVyZShsYW0gPCAwLCAwLjAsIGxhbSkgICAg
ICAgICAgICAgICAgICAgICAgICMgYWRtaXNzaWJsZSBvbmx5IHdoZW4gbGFtX21pbiA+PSAtMWUt
MTIgKGNoZWNrZWQpCiAgICAgICAgTGggPSAoVSAqIG5wLnNxcnQobGFtKSkgQCBVLmNvbmooKS5U
CiAgICAgICAgTSA9IExoIEAgKEwgKyAyLjAgKiBYKSBAIExoOyBNID0gMC41ICogKE0gKyBNLmNv
bmooKS5UKQogICAgICAgIHcyLCBIID0gbnAubGluYWxnLmVpZ2goTSk7IGlkeCA9IG5wLmFyZ3Nv
cnQodzIpWzpuYmFuZHNdCiAgICAgICAgdyA9IG5wLnNxcnQobnAuY2xpcCh3MltpZHhdLCAwLjAs
IE5vbmUpKTsgRnYgPSBMaCBAIEhbOiwgaWR4XSAgICAgICMgZiA9IHUgKyB2CiAgICAgICAgYW1w
cyA9IFtdCiAgICAgICAgZm9yIGogaW4gcmFuZ2UobGVuKGlkeCkpOgogICAgICAgICAgICBjZiA9
IG5wLnplcm9zKChOLCBOKSwgY29tcGxleCk7IG9rID0gKG5wLmFicyhzZWxmLm0xKSA8IE4gLy8g
MikgJiAobnAuYWJzKHNlbGYubTIpIDwgTiAvLyAyKQogICAgICAgICAgICBjZltzZWxmLm0xW29r
XSAlIE4sIHNlbGYubTJbb2tdICUgTl0gPSBGdltvaywgal0KICAgICAgICAgICAgYW1wcy5hcHBl
bmQocHNpMCAqIChucC5mZnQuaWZmdDIoY2YpICogTioqMikpCiAgICAgICAgcmV0dXJuIHcsIGFt
cHMsIGxhbV9taW4sIHcyW2lkeF0KCgojIC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0t
LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLSAyLiBXQVJELUdhbW1hIHBlciBBRERF
TkRVTSBBLTEKZGVmIGNlbGxfZ3JhZDAoZmllbGQpOgogICAgRmggPSBucC5mZnQuZmZ0MihmaWVs
ZCk7IHJldHVybiBucC5mZnQuaWZmdDIoMWogKiBjZWxsLkd4ICogRmgpLnJlYWwsIG5wLmZmdC5p
ZmZ0MigxaiAqIGNlbGwuR3kgKiBGaCkucmVhbApkZWYgcHcoZmllbGQsIGJkZyk6CiAgICBjID0g
bnAuZmZ0LmZmdDIoZmllbGQpIC8gTioqMjsgdiA9IG5wLnplcm9zKGxlbihiZGcubTEpLCBjb21w
bGV4KQogICAgb2sgPSAobnAuYWJzKGJkZy5tMSkgPCBOIC8vIDIpICYgKG5wLmFicyhiZGcubTIp
IDwgTiAvLyAyKTsgdltva10gPSBjW2JkZy5tMVtva10gJSBOLCBiZGcubTJbb2tdICUgTl07IHJl
dHVybiB2CmRweCwgZHB5ID0gY2VsbF9ncmFkMChwc2kwKQp3YXJkID0geyJBMV90aHJlc2hvbGRf
YW5hbHl0aWMiOiAxZS05LCAiQTFfdGhyZXNob2xkX2hlcm1pdGlhbl93MiI6IDFlLTgsICJsYW1i
ZGFfbWluX0xfZmxvb3IiOiAtMWUtMTIsICJieV9uYiI6IHt9fQpCREdTID0ge25iOiBCZEcobmIp
IGZvciBuYiBpbiAoMjQsIDMyLCA0MCl9CmZvciBuYiwgYmRnIGluIEJER1MuaXRlbXMoKToKICAg
IEwwLCBYMCA9IGJkZy5MWChucC5hcnJheShbMC4wLCAwLjBdKSk7IE0wID0gTDAgKyAyICogWDAK
ICAgIHZ4LCB2eSA9IHB3KGRweCwgYmRnKSwgcHcoZHB5LCBiZGcpCiAgICB3YSA9IHsiZHgiOiBm
bG9hdChucC5saW5hbGcubm9ybShNMCBAIHZ4KSAvIG5wLmxpbmFsZy5ub3JtKHZ4KSksICJkeSI6
IGZsb2F0KG5wLmxpbmFsZy5ub3JtKE0wIEAgdnkpIC8gbnAubGluYWxnLm5vcm0odnkpKX0KICAg
IHcsIGFtcHMsIGxtbiwgdzIgPSBiZGcubW9kZXMobnAuYXJyYXkoWzAuMCwgMC4wXSksIG5iYW5k
cz00KQogICAgcGYgPSBiZGcucHJvZHVjdF93MihucC5hcnJheShbMC4wLCAwLjBdKSwgbmxvdz0z
KQogICAgd2FyZFsiYnlfbmIiXVtzdHIobmIpXSA9IHsiYW5hbHl0aWNfd2FyZF9yZXNpZHVhbCI6
IHdhLCAiaGVybWl0aWFuX2dvbGRzdG9uZV9hYnNfdzJfbWF4IjogZmxvYXQobnAubWF4KG5wLmFi
cyh3Mls6M10pKSksCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICJoZXJtaXRpYW5fdzJf
NGxvd2VzdCI6IFtmbG9hdCh4KSBmb3IgeCBpbiB3Ml0sICJsYW1iZGFfbWluX0xfR2FtbWEiOiBs
bW4sCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICJwcm9kdWN0X2Zvcm1fYWJzX3cyX21h
eF94Y2hlY2siOiBmbG9hdChtYXgoYWJzKHopIGZvciB6IGluIHBmKSksCiAgICAgICAgICAgICAg
ICAgICAgICAgICAgICAgICJwYXNzX2EiOiBib29sKG1heCh3YS52YWx1ZXMoKSkgPD0gMWUtOSks
ICJwYXNzX2IiOiBib29sKG5wLm1heChucC5hYnModzJbOjNdKSkgPD0gMWUtOCBhbmQgbG1uID49
IC0xZS0xMil9CiAgICBsb2coIlNURVAgMiBBLTEgbl9iPSVkOiAoYSkgYW5hbHl0aWMgV2FyZCAl
LjJlLyUuMmUgOyAoYikgSGVybWl0aWFuIEdvbGRzdG9uZSB8dzJ8IG1heCAlLjJlLCBsYW1iZGFf
bWluKEwpICUrLjJlIDsgcHJvZHVjdCB4LWNoZWNrICUuMmUgLT4gJXMiICUgKAogICAgICAgIG5i
LCB3YVsiZHgiXSwgd2FbImR5Il0sIHdhcmRbImJ5X25iIl1bc3RyKG5iKV1bImhlcm1pdGlhbl9n
b2xkc3RvbmVfYWJzX3cyX21heCJdLCBsbW4sIHdhcmRbImJ5X25iIl1bc3RyKG5iKV1bInByb2R1
Y3RfZm9ybV9hYnNfdzJfbWF4X3hjaGVjayJdLAogICAgICAgICJQQVNTIiBpZiAod2FyZFsiYnlf
bmIiXVtzdHIobmIpXVsicGFzc19hIl0gYW5kIHdhcmRbImJ5X25iIl1bc3RyKG5iKV1bInBhc3Nf
YiJdKSBlbHNlICJGQUlMIikpCndhcmRbInBhc3NfYWxsX25iIl0gPSBib29sKGFsbCh2WyJwYXNz
X2EiXSBhbmQgdlsicGFzc19iIl0gZm9yIHYgaW4gd2FyZFsiYnlfbmIiXS52YWx1ZXMoKSkpCmlm
IG5vdCB3YXJkWyJwYXNzX2FsbF9uYiJdOgogICAganNvbi5kdW1wKHsic3RlcDEiOiBzdGVwMSwg
InN0ZXAyX3dhcmRfQTEiOiB3YXJkLCAiaGFsdCI6ICJXQVJELUdhbW1hIChBLTEpIEZBSUxFRCBh
dCBHYW1tYSJ9LCBvcGVuKCJnX3MyYzFfcGhhc2UxX2xhZGRlcl9jaGVja3BvaW50Lmpzb24iLCAi
dyIpLCBpbmRlbnQ9MSk7IHN5cy5leGl0KDIpCkxBTV9GTE9PUl9WSU9MQVRJT05TID0gW10gICAj
IChiKSBpcyBlbmZvcmNlZCBhdCBFVkVSWSBrIGluc2lkZSBydW4oKSB2aWEgbGFtX21pbiB0cmFj
a2luZwoKIyAtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0t
LS0tLS0tLS0tLS0tLS0tLS0gMy4gbGFkZGVyCgpkZWYgY2VsbF9ncmFkKGZpZWxkKToKICAgIEZo
ID0gbnAuZmZ0LmZmdDIoZmllbGQpOyByZXR1cm4gbnAuZmZ0LmlmZnQyKDFqICogY2VsbC5HeCAq
IEZoKS5yZWFsLCBucC5mZnQuaWZmdDIoMWogKiBjZWxsLkd5ICogRmgpLnJlYWwKRFJYLCBEUlkg
PSBjZWxsX2dyYWQocmhvMCkKQkFTSVMgPSBucC5zdGFjayhbRFJYLnJhdmVsKCksIERSWS5yYXZl
bCgpLCByaG8wLnJhdmVsKCldLCBheGlzPTEpLmFzdHlwZShjb21wbGV4KQpkZWYgcG9sYXJpc2F0
aW9uKHdfYW1wLCBrKToKICAgIGNmLCAqXyA9IG5wLmxpbmFsZy5sc3RzcShCQVNJUywgd19hbXAu
cmF2ZWwoKSwgcmNvbmQ9Tm9uZSkKICAgIHJlc2lkID0gd19hbXAucmF2ZWwoKSAtIEJBU0lTIEAg
Y2Y7IFIyID0gMS4wIC0gbnAudmRvdChyZXNpZCwgcmVzaWQpLnJlYWwgLyBucC52ZG90KHdfYW1w
LnJhdmVsKCksIHdfYW1wLnJhdmVsKCkpLnJlYWwKICAgIGEgPSBjZls6Ml07IGdzID0gbnAubGlu
YWxnLm5vcm0oQkFTSVNbOiwgOjJdIEAgYSkqKjIgLyBtYXgobnAubGluYWxnLm5vcm0oQkFTSVMg
QCBjZikqKjIsIDFlLTMwMCkKICAgIGt4LCBreSA9IGs7IFMgPSAwLjVqICogbnAuYXJyYXkoW1sy
ICoga3ggKiBhWzBdLCBreCAqIGFbMV0gKyBreSAqIGFbMF1dLCBba3ggKiBhWzFdICsga3kgKiBh
WzBdLCAyICoga3kgKiBhWzFdXV0pCiAgICBFMiA9IFMgLSAwLjUgKiBucC50cmFjZShTKSAqIG5w
LmV5ZSgyKTsgblMgPSBucC5saW5hbGcubm9ybShTKSoqMgogICAgcmV0dXJuIGZsb2F0KFIyKSwg
ZmxvYXQoZ3MpLCAoZmxvYXQobnAubGluYWxnLm5vcm0oRTIpKioyIC8gblMpIGlmIG5TID4gMCBl
bHNlIGZsb2F0KCJuYW4iKSkKZGVmIGNsYXNzaWZ5KGssIHcsIGFtcHMpOgogICAgcm93cyA9IFtd
CiAgICBmb3IgaiBpbiByYW5nZShsZW4odykpOgogICAgICAgIFIyLCBncywgbzIgPSBwb2xhcmlz
YXRpb24oYW1wc1tqXSwgayk7IHJvd3MuYXBwZW5kKGRpY3Qoaj1qLCBvbWVnYT1mbG9hdCh3W2pd
KSwgUjI9UjIsIGdyYWRfc2hhcmU9Z3MsIG8yPW8yKSkKICAgIGxhdCA9IFtyIGZvciByIGluIHJv
d3MgaWYgclsiUjIiXSA+PSAwLjkwIGFuZCByWyJncmFkX3NoYXJlIl0gPj0gMC41XQogICAgVCA9
IG1heChsYXQsIGtleT1sYW1iZGEgcjogclsibzIiXSkgaWYgbGF0IGVsc2UgTm9uZQogICAgTHMg
PSBbciBmb3IgciBpbiBsYXQgaWYgciBpcyBub3QgVCBhbmQgclsibzIiXSA8IFRIRVRBX0lEXTsg
TDEgPSBtaW4oTHMsIGtleT1sYW1iZGEgcjogclsib21lZ2EiXSkgaWYgTHMgZWxzZSBOb25lCiAg
ICBvdGhlcnMgPSBbciBmb3IgciBpbiByb3dzIGlmIHIgaXMgbm90IFQgYW5kIHIgaXMgbm90IEwx
XTsgUEggPSBtaW4ob3RoZXJzLCBrZXk9bGFtYmRhIHI6IHJbIm9tZWdhIl0pIGlmIG90aGVycyBl
bHNlIE5vbmUKICAgIHJldHVybiByb3dzLCBULCBMMSwgUEgKZGVmIGt2ZWMoa2EsIGQpOgogICAg
ayA9IGthIC8gQV9TVEFSOyB0aCA9IDAuMCBpZiBkID09ICJHSyIgZWxzZSAtbnAucGkgLyA2LjA7
IHJldHVybiBucC5hcnJheShbayAqIG5wLmNvcyh0aCksIGsgKiBucC5zaW4odGgpXSkKZGVmIGZp
dF9yKGthLCByKToKICAgIFggPSBucC5zdGFjayhba2EqKjIsIGthKio0XSwgYXhpcz0xKTsgY2Ys
ICpfID0gbnAubGluYWxnLmxzdHNxKFgsIHIsIHJjb25kPU5vbmUpCiAgICByZXR1cm4gZmxvYXQo
Y2ZbMF0pLCBmbG9hdChjZlsxXSksIGZsb2F0KG5wLnNxcnQobnAubWVhbigociAtIFggQCBjZikq
KjIpKSkKZGVmIHJ1bihuX2IsIGRpcnM9KCJHSyIsICJHTSIpKToKICAgIGJkZyA9IEJkRyhuX2Ip
OyBvdXQgPSB7Im5fYiI6IG5fYiwgInNwZWVkcyI6IHt9LCAiVCI6IHt9LCAiTDEiOiB7fSwgImlk
ZW50Ijoge30sICJmbWl4X21pbl9vMl9UIjoge30sICJsYW1fbWluX0xfbWluIjogMC4wLCAieGNo
ZWNrX3Byb2R1Y3RfdnNfaGVybWl0aWFuIjoge319CiAgICBmb3IgZCBpbiBkaXJzOgogICAgICAg
IGNULCBjTCwgY1AsIGthcyA9IFtdLCBbXSwgW10sIFtdCiAgICAgICAgZm9yIGthIGluIFNQRUVE
OgogICAgICAgICAgICBrID0ga3ZlYyhrYSwgZCk7IHcsIGFtcHMsIGxtbiwgXyA9IGJkZy5tb2Rl
cyhrKTsgb3V0WyJsYW1fbWluX0xfbWluIl0gPSBtaW4ob3V0WyJsYW1fbWluX0xfbWluIl0sIGxt
bikKICAgICAgICAgICAgcm93cywgVCwgTDEsIFBIID0gY2xhc3NpZnkoaywgdywgYW1wcykKICAg
ICAgICAgICAgaWYgVCBpcyBOb25lIG9yIEwxIGlzIE5vbmUgb3IgUEggaXMgTm9uZTogbG9nKCIg
IFslcyAlZCBrYT0lLjRmXSBjbGFzc2lmaWNhdGlvbiBpbmNvbXBsZXRlICVzIiAlIChkLCBuX2Is
IGthLCBbKHJbImoiXSwgcm91bmQoclsiUjIiXSwgMyksIHJvdW5kKHJbIm8yIl0sIDMpKSBmb3Ig
ciBpbiByb3dzWzo1XV0pKTsgY29udGludWUKICAgICAgICAgICAga2FzLmFwcGVuZChrYSk7IGNU
LmFwcGVuZChUWyJvbWVnYSJdIC8gKGthIC8gQV9TVEFSKSk7IGNMLmFwcGVuZChMMVsib21lZ2Ei
XSAvIChrYSAvIEFfU1RBUikpOyBjUC5hcHBlbmQoUEhbIm9tZWdhIl0gLyAoa2EgLyBBX1NUQVIp
KQogICAgICAgIFggPSBucC5zdGFjayhbbnAub25lcyhsZW4oa2FzKSksIG5wLmFycmF5KGthcykq
KjJdLCBheGlzPTEpOyBzcCA9IHt9CiAgICAgICAgZm9yIG5tLCBhcnIgaW4gKCgiVCIsIGNUKSwg
KCJMMSIsIGNMKSwgKCJQSCIsIGNQKSk6IHNwW25tXSA9IGZsb2F0KG5wLmxpbmFsZy5sc3RzcShY
LCBucC5hcnJheShhcnIpLCByY29uZD1Ob25lKVswXVswXSkKICAgICAgICBvdXRbInNwZWVkcyJd
W2RdID0gc3A7IGxvZygiICBbJXMgbl9iPSVkXSBzcGVlZHMgay0+MDogUEggJS41ZiAgVCAlLjVm
ICBMMSAlLjVmICAoUl9UID0gY19UL2NfTDEgPSAlLjVmKSIgJSAoZCwgbl9iLCBzcFsiUEgiXSwg
c3BbIlQiXSwgc3BbIkwxIl0sIHNwWyJUIl0gLyBzcFsiTDEiXSkpCiAgICAgICAgclQsIHJMLCB1
c2VkLCBvMlQgPSBbXSwgW10sIFtdLCBbXQogICAgICAgIGZvciBrYSBpbiBMQURERVI6CiAgICAg
ICAgICAgIGsgPSBrdmVjKGthLCBkKTsgdywgYW1wcywgbG1uLCB3MiA9IGJkZy5tb2RlcyhrKTsg
b3V0WyJsYW1fbWluX0xfbWluIl0gPSBtaW4ob3V0WyJsYW1fbWluX0xfbWluIl0sIGxtbikKICAg
ICAgICAgICAgcm93cywgVCwgTDEsIFBIID0gY2xhc3NpZnkoaywgdywgYW1wcykKICAgICAgICAg
ICAgaWYgVCBpcyBOb25lIG9yIEwxIGlzIE5vbmU6IGxvZygiICBbJXMgbl9iPSVkIGxhZGRlciBr
YT0lLjVmXSBjbGFzc2lmaWNhdGlvbiBpbmNvbXBsZXRlIOKAlCBkcm9wcGVkLCBsb2dnZWQiICUg
KGQsIG5fYiwga2EpKTsgY29udGludWUKICAgICAgICAgICAgdXNlZC5hcHBlbmQoa2EpOyByVC5h
cHBlbmQoVFsib21lZ2EiXSAvIChzcFsiVCJdICoga2EgLyBBX1NUQVIpIC0gMS4wKTsgckwuYXBw
ZW5kKEwxWyJvbWVnYSJdIC8gKHNwWyJMMSJdICoga2EgLyBBX1NUQVIpIC0gMS4wKTsgbzJULmFw
cGVuZChUWyJvMiJdKQogICAgICAgICAgICBvdXRbImlkZW50Il0uc2V0ZGVmYXVsdChkLCBbXSku
YXBwZW5kKGRpY3Qoa2E9a2EsIFQ9ZGljdChqPVRbImoiXSwgb21lZ2E9VFsib21lZ2EiXSwgUjI9
cm91bmQoVFsiUjIiXSwgNSksIG8yPXJvdW5kKFRbIm8yIl0sIDUpKSwgTDE9ZGljdChqPUwxWyJq
Il0sIG9tZWdhPUwxWyJvbWVnYSJdLCBvMj1yb3VuZChMMVsibzIiXSwgNSkpLCBQSD1kaWN0KGo9
UEhbImoiXSwgb21lZ2E9UEhbIm9tZWdhIl0pIGlmIFBIIGVsc2UgTm9uZSkpCiAgICAgICAgICAg
IGlmIGthIGluIChMQURERVJbMF0sIExBRERFUls0XSk6CiAgICAgICAgICAgICAgICBwdzIgPSBi
ZGcucHJvZHVjdF93MihrLCBubG93PTQpOyBvdXRbInhjaGVja19wcm9kdWN0X3ZzX2hlcm1pdGlh
biJdWyIlc19rYT0lLjRmIiAlIChkLCBrYSldID0geyJwcm9kdWN0IjogW2Zsb2F0KHoucmVhbCkg
Zm9yIHogaW4gcHcyXSwgImhlcm1pdGlhbiI6IFtmbG9hdCh6KSBmb3IgeiBpbiB3Mls6NF1dfQog
ICAgICAgIGthX3UgPSBucC5hcnJheSh1c2VkKQogICAgICAgIGZvciBubSwgciBpbiAoKCJUIiwg
clQpLCAoIkwxIiwgckwpKToKICAgICAgICAgICAgYTIsIGE0LCBybXMgPSBmaXRfcihrYV91LCBu
cC5hcnJheShyKSkKICAgICAgICAgICAgZWRnZXMgPSAoMC4zLCAwLjE1LCAwLjA3NSk7IGNpcyA9
IFtmaXRfcihrYV91W2thX3UgPD0gZV0sIG5wLmFycmF5KHIpW2thX3UgPD0gZV0pIGZvciBlIGlu
IGVkZ2VzWzE6XV0KICAgICAgICAgICAgb3V0W25tXVtkXSA9IGRpY3Qoa2E9dXNlZCwgcj1bZmxv
YXQoeCkgZm9yIHggaW4gcl0sIGEyPWEyLCBhND1hNCwgZml0X3Jtcz1ybXMsIGNpX2EyPW1heChh
YnMoY1swXSAtIGEyKSBmb3IgYyBpbiBjaXMpLCBjaV9hND1tYXgoYWJzKGNbMV0gLSBhNCkgZm9y
IGMgaW4gY2lzKSkKICAgICAgICBvdXRbImZtaXhfbWluX28yX1QiXVtkXSA9IGZsb2F0KG1pbihv
MlQpKQogICAgICAgICMgQS0xIGV4cGxpY2l0IGZsb29yIHRlcm06IHNpZ21hX3Ioa2EpID0gZmxv
b3JfdzIobl9iKSAvICgyIG9tZWdhX1ReMik7IHdlaWdodGVkIExTUSByZXBvcnRlZCBBTE9OR1NJ
REUgdGhlIGVsZWN0ZWQgdW53ZWlnaHRlZCBmaXQKICAgICAgICBmbG9vcl93MiA9IHdhcmRbImJ5
X25iIl1bc3RyKG5fYildWyJoZXJtaXRpYW5fZ29sZHN0b25lX2Fic193Ml9tYXgiXQogICAgICAg
IG9tVCA9IG5wLmFycmF5KFtlWyJUIl1bIm9tZWdhIl0gZm9yIGUgaW4gb3V0WyJpZGVudCJdW2Rd
XSk7IHNpZyA9IGZsb29yX3cyIC8gKDIuMCAqIG9tVCoqMikKICAgICAgICBYdyA9IG5wLnN0YWNr
KFtrYV91KioyLCBrYV91Kio0XSwgYXhpcz0xKSAvIHNpZ1s6LCBOb25lXTsgY3csICpfID0gbnAu
bGluYWxnLmxzdHNxKFh3LCBucC5hcnJheShyVCkgLyBzaWcsIHJjb25kPU5vbmUpCiAgICAgICAg
b3V0WyJUIl1bZF1bImEyX2Zsb29yX3dlaWdodGVkIl0gPSBmbG9hdChjd1swXSk7IG91dFsiVCJd
W2RdWyJhNF9mbG9vcl93ZWlnaHRlZCJdID0gZmxvYXQoY3dbMV0pOyBvdXRbIlQiXVtkXVsiZmxv
b3Jfc2lnbWFfciJdID0gW2Zsb2F0KHgpIGZvciB4IGluIHNpZ10KICAgICAgICAjIGZyYW1ld29y
ayBsYWJlbCBjb252ZW50aW9uIChHLVRTSDMpOiBjX0wxID0gdGhlIGhpZ2hlciBvZiB0aGUgdHdv
IG5vbi1UIGdhcGxlc3Mgc3BlZWRzCiAgICAgICAgb3V0WyJzcGVlZHMiXVtkXVsiY19MMV9mcmFt
ZXdvcmsiXSA9IG1heChzcFsiTDEiXSwgc3BbIlBIIl0pOyBvdXRbInNwZWVkcyJdW2RdWyJSX1Rf
ZnJhbWV3b3JrIl0gPSBzcFsiVCJdIC8gbWF4KHNwWyJMMSJdLCBzcFsiUEgiXSkKICAgICAgICBs
b2coIiAgWyVzIG5fYj0lZF0gVCBmbG9vci13ZWlnaHRlZDogYTJfdyA9ICUrLjZlICBhNF93ID0g
JSsuNmUgOyBSX1QoZnJhbWV3b3JrIGxhYmVsKSA9ICUuNWYiICUgKGQsIG5fYiwgY3dbMF0sIGN3
WzFdLCBvdXRbInNwZWVkcyJdW2RdWyJSX1RfZnJhbWV3b3JrIl0pKQogICAgICAgIGxvZygiICBb
JXMgbl9iPSVkXSBUOiBhMiA9ICUrLjZlIChjaSAlLjFlKSAgYTQgPSAlKy42ZSAoY2kgJS4xZSkg
IHJtcyAlLjFlIHwgTDEgY29udHJvbDogYTIgPSAlKy42ZSB8IG1pbiBvMihUKSAlLjRmIiAlIChk
LCBuX2IsIG91dFsiVCJdW2RdWyJhMiJdLCBvdXRbIlQiXVtkXVsiY2lfYTIiXSwgb3V0WyJUIl1b
ZF1bImE0Il0sIG91dFsiVCJdW2RdWyJjaV9hNCJdLCBvdXRbIlQiXVtkXVsiZml0X3JtcyJdLCBv
dXRbIkwxIl1bZF1bImEyIl0sIG91dFsiZm1peF9taW5fbzJfVCJdW2RdKSkKICAgIHJldHVybiBv
dXQKCmltcG9ydCBhcmdwYXJzZQphcCA9IGFyZ3BhcnNlLkFyZ3VtZW50UGFyc2VyKCk7IGFwLmFk
ZF9hcmd1bWVudCgiLS1zdGFnZSIsIHJlcXVpcmVkPVRydWUpICAgIyBuYjI0IHwgbmIzMiB8IG5i
NDBHSyB8IG5iNDBHTSB8IGFzc2VtYmxlCmFyZ3MgPSBhcC5wYXJzZV9hcmdzKCkKZGVmIHN0YWdl
X2ZpbGUodGFnKTogcmV0dXJuICJzMmMxX2xhZGRlcl9zdGFnZV8lcy5qc29uIiAlIHRhZwppZiBh
cmdzLnN0YWdlLnN0YXJ0c3dpdGgoIm5iIik6CiAgICBuYiA9IGludChhcmdzLnN0YWdlWzI6NF0p
OyBkaXJzID0gKCJHSyIsICJHTSIpIGlmIGxlbihhcmdzLnN0YWdlKSA9PSA0IGVsc2UgKGFyZ3Mu
c3RhZ2VbNDpdLCkKICAgIGxvZygiPT09IGxhZGRlciBzdGFnZSAlczogbl9iID0gJWQgZGlycyAl
cyA9PT0iICUgKGFyZ3Muc3RhZ2UsIG5iLCBkaXJzKSkKICAgIG91dCA9IHJ1bihuYiwgZGlycyk7
IG91dFsid2FyZCJdID0gd2FyZDsgb3V0WyJzdGVwMSJdID0gc3RlcDEKICAgIG9iID0gKGpzb24u
ZHVtcHMob3V0LCBpbmRlbnQ9MSwgc29ydF9rZXlzPVRydWUsIGRlZmF1bHQ9c3RyKSArICJcbiIp
LmVuY29kZSgpOyBvcGVuKHN0YWdlX2ZpbGUoYXJncy5zdGFnZSksICJ3YiIpLndyaXRlKG9iKQog
ICAgbG9nKCJzdGFnZSAlcyB3cml0dGVuIG1kNSAlcyAoJWQgQikiICUgKGFyZ3Muc3RhZ2UsIG1k
NWIob2IpLCBsZW4ob2IpKSk7IHN5cy5leGl0KDApCiMgLS0tLSBhc3NlbWJsZTogbWVyZ2Ugc3Rh
Z2UgZmlsZXMKZGVmIGxvYWQodGFnKTogcmV0dXJuIGpzb24ubG9hZChvcGVuKHN0YWdlX2ZpbGUo
dGFnKSkpCnJ1bnMgPSB7IjI0IjogbG9hZCgibmIyNCIpLCAiMzIiOiBsb2FkKCJuYjMyIil9Cmc0
MCwgbTQwID0gbG9hZCgibmI0MEdLIiksIGxvYWQoIm5iNDBHTSIpCnI0MG0gPSB7Im5fYiI6IDQw
LCAic3BlZWRzIjogeyoqZzQwWyJzcGVlZHMiXSwgKiptNDBbInNwZWVkcyJdfSwgIlQiOiB7Kipn
NDBbIlQiXSwgKiptNDBbIlQiXX0sICJMMSI6IHsqKmc0MFsiTDEiXSwgKiptNDBbIkwxIl19LAog
ICAgICAgICJpZGVudCI6IHsqKmc0MFsiaWRlbnQiXSwgKiptNDBbImlkZW50Il19LCAiZm1peF9t
aW5fbzJfVCI6IHsqKmc0MFsiZm1peF9taW5fbzJfVCJdLCAqKm00MFsiZm1peF9taW5fbzJfVCJd
fSwKICAgICAgICAibGFtX21pbl9MX21pbiI6IG1pbihnNDBbImxhbV9taW5fTF9taW4iXSwgbTQw
WyJsYW1fbWluX0xfbWluIl0pLCAieGNoZWNrX3Byb2R1Y3RfdnNfaGVybWl0aWFuIjogeyoqZzQw
WyJ4Y2hlY2tfcHJvZHVjdF92c19oZXJtaXRpYW4iXSwgKiptNDBbInhjaGVja19wcm9kdWN0X3Zz
X2hlcm1pdGlhbiJdfX0KcnVuc1siNDAiXSA9IHI0MG0Kc3RhZ2VfbWQ1ID0ge3Q6IG1kNWIob3Bl
bihzdGFnZV9maWxlKHQpLCAicmIiKS5yZWFkKCkpIGZvciB0IGluICgibmIyNCIsICJuYjMyIiwg
Im5iNDBHSyIsICJuYjQwR00iKX0KTEFNX0ZMT09SX1ZJT0xBVElPTlMgPSBbKG5iLCBydW5zW3N0
cihuYildWyJsYW1fbWluX0xfbWluIl0pIGZvciBuYiBpbiAoMjQsIDMyLCA0MCkgaWYgcnVuc1tz
dHIobmIpXVsibGFtX21pbl9MX21pbiJdIDwgLTFlLTEyXQoKcjI0LCByMzIsIHI0MCA9IHJ1bnNb
IjI0Il0sIHJ1bnNbIjMyIl0sIHJ1bnNbIjQwIl0KY29udiA9IHt9CmZvciBkIGluICgiR0siLCAi
R00iKToKICAgIGZvciBubSBpbiAoIlQiLCAiTDEiLCAiUEgiKToKICAgICAgICBjb252WyJjXyVz
XyVzX3JlbF8zMnY0MCIgJSAobm0sIGQpXSA9IGFicyhyNDBbInNwZWVkcyJdW2RdW25tXSAvIHIz
Mlsic3BlZWRzIl1bZF1bbm1dIC0gMS4wKQogICAgICAgIGNvbnZbImNfJXNfJXNfcmVsXzI0djMy
IiAlIChubSwgZCldID0gYWJzKHIzMlsic3BlZWRzIl1bZF1bbm1dIC8gcjI0WyJzcGVlZHMiXVtk
XVtubV0gLSAxLjApCiAgICBjb252WyJhMl9UXyVzX2Fic18zMnY0MCIgJSBkXSA9IGFicyhyNDBb
IlQiXVtkXVsiYTIiXSAtIHIzMlsiVCJdW2RdWyJhMiJdKTsgY29udlsiYTJfVF8lc19hYnNfMjR2
MzIiICUgZF0gPSBhYnMocjMyWyJUIl1bZF1bImEyIl0gLSByMjRbIlQiXVtkXVsiYTIiXSkKICAg
IGNvbnZbImE0X1RfJXNfYWJzXzMydjQwIiAlIGRdID0gYWJzKHI0MFsiVCJdW2RdWyJhNCJdIC0g
cjMyWyJUIl1bZF1bImE0Il0pCmZjb252X3Bhc3MgPSBhbGwoY29udlsiY19UXyVzX3JlbF8zMnY0
MCIgJSBkXSA8PSAxZS02IGFuZCBjb252WyJhMl9UXyVzX2Fic18zMnY0MCIgJSBkXSA8PSAxZS03
IGZvciBkIGluICgiR0siLCAiR00iKSkKaXNvX1QgPSBhYnMocjQwWyJzcGVlZHMiXVsiR0siXVsi
VCJdIC8gcjQwWyJzcGVlZHMiXVsiR00iXVsiVCJdIC0gMS4wKQpmbWl4X3Bhc3MgPSBhbGwocjQw
WyJmbWl4X21pbl9vMl9UIl1bZF0gPj0gVEhFVEFfSUQgZm9yIGQgaW4gKCJHSyIsICJHTSIpKQpm
ZGlzcCA9IHt9CmZvciBkIGluICgiR0siLCAiR00iKToKICAgIGEyLCBhNCA9IHI0MFsiVCJdW2Rd
WyJhMiJdLCByNDBbIlQiXVtkXVsiYTQiXQogICAgY2kyID0gbWF4KHI0MFsiVCJdW2RdWyJjaV9h
MiJdLCBjb252WyJhMl9UXyVzX2Fic18zMnY0MCIgJSBkXSwgY29udlsiYTJfVF8lc19hYnNfMjR2
MzIiICUgZF0pICAgIyB3aW5kb3cgKyBiYXNpcyAoZGVuc2UtZmxvb3IpIHRlcm1zLCBBLTEKICAg
IGNpNCA9IG1heChyNDBbIlQiXVtkXVsiY2lfYTQiXSwgY29udlsiYTRfVF8lc19hYnNfMzJ2NDAi
ICUgZF0pCiAgICBmZGlzcFtkXSA9IHsiYTIiOiBhMiwgImE0IjogYTQsICJjaV9hMl90b3RhbCI6
IGNpMiwgImNpX2E0X3RvdGFsIjogY2k0LCAiYTJfemVyb19hdF90YXUiOiBib29sKGFicyhhMikg
PD0gbWF4KFRBVSwgY2kyKSksCiAgICAgICAgICAgICAgICAiYTRfemVyb19hdF90YXUiOiBib29s
KGFicyhhNCkgPD0gbWF4KFRBVSwgY2k0KSksICJhMl9yZXNvbHZlZF9ub256ZXJvIjogYm9vbChh
YnMoYTIpID4gbWF4KFRBVSwgY2kyKSksICJhNF9yZXNvbHZlZF9ub256ZXJvIjogYm9vbChhYnMo
YTQpID4gbWF4KFRBVSwgY2k0KSl9CmRlZiBhcm1faW5kaWNhdGlvbihkKToKICAgIGYgPSBmZGlz
cFtkXQogICAgaWYgcjQwWyJmbWl4X21pbl9vMl9UIl1bZF0gPCBUSEVUQV9JRDogcmV0dXJuICJB
NCBDSEFOTkVMLVVOREVGSU5FRCAoRi1NSVgpIgogICAgaWYgbm90IGZjb252X3Bhc3Mgb3IgTEFN
X0ZMT09SX1ZJT0xBVElPTlM6IHJldHVybiAiQTUgSU5TVFJVTUVOVC1MSU1JVEVEIChGLUNPTlYg
LyBsYW1iZGFfbWluIGZsb29yKSIKICAgIGlmIGZbImEyX3Jlc29sdmVkX25vbnplcm8iXTogcmV0
dXJuICJBMyBESVNQRVJTSVZFLU8oa14yKSIKICAgIGlmIGZbImEyX3plcm9fYXRfdGF1Il0gYW5k
IGZbImE0X3Jlc29sdmVkX25vbnplcm8iXTogcmV0dXJuICJBMiBPTi1DT05FLVBST1RFQ1RFRC1P
KGteNCkiCiAgICBpZiBmWyJhMl96ZXJvX2F0X3RhdSJdIGFuZCBmWyJhNF96ZXJvX2F0X3RhdSJd
OiByZXR1cm4gIkExIE9OLUNPTkUtRVhBQ1QgKHNpbmdsZS1jcnlzdGFsIFAxIG9ubHk7IFAyIGFn
Z3JlZ2F0ZSBwZW5kaW5nKSIKICAgIHJldHVybiAiQTUgSU5TVFJVTUVOVC1MSU1JVEVEIGF0IHRh
dSAoQ0kgPiB0YXUsIGEyIHVucmVzb2x2ZWQpIgphcm1zID0ge2Q6IGFybV9pbmRpY2F0aW9uKGQp
IGZvciBkIGluICgiR0siLCAiR00iKX0KcmVsX2NvbnYgPSB7ZDogeyJhMl9yZWxfMzJ2NDAiOiBh
YnMocjQwWyJUIl1bZF1bImEyIl0gLSByMzJbIlQiXVtkXVsiYTIiXSkgLyBhYnMocjQwWyJUIl1b
ZF1bImEyIl0pLCAiYTJfcmVsXzI0djMyIjogYWJzKHIzMlsiVCJdW2RdWyJhMiJdIC0gcjI0WyJU
Il1bZF1bImEyIl0pIC8gYWJzKHIzMlsiVCJdW2RdWyJhMiJdKSwKICAgICAgICAgICAgICAgICJh
MndfcmVsXzMydjQwIjogYWJzKHI0MFsiVCJdW2RdWyJhMl9mbG9vcl93ZWlnaHRlZCJdIC0gcjMy
WyJUIl1bZF1bImEyX2Zsb29yX3dlaWdodGVkIl0pIC8gYWJzKHI0MFsiVCJdW2RdWyJhMl9mbG9v
cl93ZWlnaHRlZCJdKSwKICAgICAgICAgICAgICAgICJhMndfcmVsXzI0djMyIjogYWJzKHIzMlsi
VCJdW2RdWyJhMl9mbG9vcl93ZWlnaHRlZCJdIC0gcjI0WyJUIl1bZF1bImEyX2Zsb29yX3dlaWdo
dGVkIl0pIC8gYWJzKHIzMlsiVCJdW2RdWyJhMl9mbG9vcl93ZWlnaHRlZCJdKSwKICAgICAgICAg
ICAgICAgICJhMl9mbG9vcl93ZWlnaHRlZF9uYjQwIjogcjQwWyJUIl1bZF1bImEyX2Zsb29yX3dl
aWdodGVkIl0sICJhNF9mbG9vcl93ZWlnaHRlZF9uYjQwIjogcjQwWyJUIl1bZF1bImE0X2Zsb29y
X3dlaWdodGVkIl0sCiAgICAgICAgICAgICAgICAic2lnbl9zdGFibGVfYWxsX25iIjogYm9vbChu
cC5zaWduKHIyNFsiVCJdW2RdWyJhMiJdKSA9PSBucC5zaWduKHIzMlsiVCJdW2RdWyJhMiJdKSA9
PSBucC5zaWduKHI0MFsiVCJdW2RdWyJhMiJdKSA9PSBucC5zaWduKHI0MFsiVCJdW2RdWyJhMl9m
bG9vcl93ZWlnaHRlZCJdKSl9IGZvciBkIGluICgiR0siLCAiR00iKX0KY2sgPSB7ImdhdGUiOiAi
Ry1TMkMxIiwgInBoYXNlIjogIjEtbGFkZGVyIiwgImxlZyI6ICJjaGF0IiwgIlBIQVNFMV9BVVRI
T1JJWkVEIjogVHJ1ZSwgInByZXJlZ19tZDUiOiAiMmVhOGVjMTNmZmEzYzMyODk4Y2MyNGEzYmU2
MDVjNjQiLAogICAgICAidDFfbWQ1IjogIjhjZDg5YjlhODI3MDRhY2NkODlmN2ZmNmY1ZTIyMGI0
IiwgImxvY2tfcmVjb3JkX21kNSI6ICJmMmY0ZDUwMDI5ZmI1YmUzMTIyYTg4NWM0OGE3ZTA0ZiIs
ICJhZGRlbmR1bV9BMV9tZDUiOiAiOGJmNTFiZDA1YzY5MWYzZjAzZDc5NmIyMzFjZGQyNjIiLAog
ICAgICAicGhhc2UwX21kNSI6ICJlYWUyYmJkNzM0ZjUxMjlkZDFlNTFlZmNiYjU1ZGQzZCIsICJw
aGFzZTFfaGFsdF9jaGVja3BvaW50X21kNSI6ICJlZWVkY2ZhNTk0YTI0OTE1ZmE5YzEwYzZhYmJk
MGE0ZSIsICJzdGFnZV9maWxlX21kNSI6IHN0YWdlX21kNSwKICAgICAgInN1YnN0cmF0ZSI6IHsi
a2VybmVsIjogIkdFTS04IGcgZXhwKC1yXjgpLCAyLUQiLCAiZyI6IEdfU1RBUiwgImFfc3RhciI6
IEFfU1RBUiwgIm11IjogTVUsICJncmlkX24iOiBOLCAia2VybmVsX1UwIjogS0VSLlUwfSwKICAg
ICAgInN0ZXAxX2JhbmtlZF9zdGF0ZSI6IHN0ZXAxLCAic3RlcDJfd2FyZF9nYW1tYV9BMSI6IHdh
cmQsICJsYW1iZGFfbWluX2Zsb29yX3Zpb2xhdGlvbnNfaW5fbGFkZGVyIjogTEFNX0ZMT09SX1ZJ
T0xBVElPTlMsCiAgICAgICJzdGVwM19sYWRkZXIiOiB7ImxhZGRlcl9rYSI6IExBRERFUiwgInNw
ZWVkX2thIjogU1BFRUQsICJydW5zIjogcnVuc30sCiAgICAgICJGX0NPTlYiOiBjb252LCAiRl9D
T05WX3Bhc3MiOiBmY29udl9wYXNzLCAiRl9JU09fY1Rfc3BsaXQiOiBpc29fVCwgIkZfSVNPX3Bh
c3MiOiBib29sKGlzb19UIDw9IFRIRVRBX0lTTyksCiAgICAgICJGX01JWF9taW5fbzJfVCI6IHI0
MFsiZm1peF9taW5fbzJfVCJdLCAiRl9NSVhfcGFzcyI6IGZtaXhfcGFzcywgIkZfRElTUF9jaGF0
bGVnIjogZmRpc3AsICJ0YXUiOiBUQVUsICJ0aGV0YV9pZCI6IFRIRVRBX0lELCAidGhldGFfaXNv
IjogVEhFVEFfSVNPLAogICAgICAiYXJtX2luZGljYXRpb25fY2hhdGxlZyI6IGFybXMsICJhMl9y
ZWxhdGl2ZV9jb252ZXJnZW5jZV9hbmRfd2VpZ2h0ZWQiOiByZWxfY29udiwgIlJfVF9mcmFtZXdv
cmtfbGFiZWxfbmI0MCI6IHtkOiByNDBbInNwZWVkcyJdW2RdWyJSX1RfZnJhbWV3b3JrIl0gZm9y
IGQgaW4gKCJHSyIsICJHTSIpfSwgInJlZ2lzdGVyZWRfZXhwZWN0YXRpb24iOiAiRElTUEVSU0lW
RSAoRWRkaW5ndG9uIHRyYXAgNCkiLAogICAgICAidmVyZGljdCI6ICJOT1QgREVDTEFSRUQg4oCU
IHR3by1sZWcgKENDKSBjb21wYXJpc29uIGFuZCBQaGFzZSAyLzMgKGFnZ3JlZ2F0ZSkgcGVuZGlu
ZzsgY2hhdC1sZWcgc2luZ2xlLWNyeXN0YWwgSU5ESUNBVElPTiBvbmx5In0Kb2IgPSAoanNvbi5k
dW1wcyhjaywgaW5kZW50PTEsIHNvcnRfa2V5cz1UcnVlLCBkZWZhdWx0PXN0cikgKyAiXG4iKS5l
bmNvZGUoKTsgb3BlbigiZ19zMmMxX3BoYXNlMV9sYWRkZXJfY2hlY2twb2ludC5qc29uIiwgIndi
Iikud3JpdGUob2IpCmxvZygiRi1DT05WOiAiICsgIiwgIi5qb2luKCIlcz0lLjJlIiAlIGt2IGZv
ciBrdiBpbiBjb252Lml0ZW1zKCkgaWYgIlRfIiBpbiBrdlswXSBvciAiY19UIiBpbiBrdlswXSkg
KyAiICAtPiAlcyIgJSAoIlBBU1MiIGlmIGZjb252X3Bhc3MgZWxzZSAiRkFJTCIpKQpsb2coIkYt
SVNPIGNfVCBzcGxpdCBHSy9HTSA9ICUuM2UgLT4gJXMgOyBGLU1JWCBtaW4gbzIoVCkgJXMgLT4g
JXMgOyBsYW1iZGEgZmxvb3IgdmlvbGF0aW9ucyAlcyIgJSAoaXNvX1QsICJQQVNTIiBpZiBpc29f
VCA8PSBUSEVUQV9JU08gZWxzZSAiRkFJTCIsIHI0MFsiZm1peF9taW5fbzJfVCJdLCAiUEFTUyIg
aWYgZm1peF9wYXNzIGVsc2UgIkZBSUwiLCBMQU1fRkxPT1JfVklPTEFUSU9OUykpCmZvciBkIGlu
ICgiR0siLCAiR00iKTogbG9nKCJGLURJU1AgY2hhdC1sZWcgJXM6IGEyID0gJSsuNmUgKENJICUu
MWUpIDsgYTQgPSAlKy42ZSAoQ0kgJS4xZSkgLT4gJXMiICUgKGQsIGZkaXNwW2RdWyJhMiJdLCBm
ZGlzcFtkXVsiY2lfYTJfdG90YWwiXSwgZmRpc3BbZF1bImE0Il0sIGZkaXNwW2RdWyJjaV9hNF90
b3RhbCJdLCBhcm1zW2RdKSkKZm9yIGQgaW4gKCJHSyIsICJHTSIpOiBsb2coImEyIHJlbGF0aXZl
IGNvbnZlcmdlbmNlICVzOiB1bndlaWdodGVkIDI0djMyICUuMmUgMzJ2NDAgJS4yZSB8IGZsb29y
LXdlaWdodGVkIDI0djMyICUuMmUgMzJ2NDAgJS4yZSB8IHNpZ24gc3RhYmxlICVzIiAlIChkLCBy
ZWxfY29udltkXVsiYTJfcmVsXzI0djMyIl0sIHJlbF9jb252W2RdWyJhMl9yZWxfMzJ2NDAiXSwg
cmVsX2NvbnZbZF1bImEyd19yZWxfMjR2MzIiXSwgcmVsX2NvbnZbZF1bImEyd19yZWxfMzJ2NDAi
XSwgcmVsX2NvbnZbZF1bInNpZ25fc3RhYmxlX2FsbF9uYiJdKSkKbG9nKCJjaGVja3BvaW50IGdf
czJjMV9waGFzZTFfbGFkZGVyX2NoZWNrcG9pbnQuanNvbiBtZDUgJXMgKCVkIEIpIiAlIChtZDVi
KG9iKSwgbGVuKG9iKSkpCg==
<<<EMBED-END name=g_s2c1_phase1_ladder.py>>>

### EMBED — chat diagnostic analysis script — `s2c1_phase1_ladder_analysis.py` (md5 a55b0544d3c5ce7ab050a4af01492b4e, 3134 B, b64, QUARANTINED)

<<<EMBED-BEGIN name=s2c1_phase1_ladder_analysis.py md5=a55b0544d3c5ce7ab050a4af01492b4e bytes=3134 enc=b64 quarantine=1>>>
IyEvdXNyL2Jpbi9lbnYgcHl0aG9uMwoiIiJQb3N0LWFzc2VtYmx5IERJQUdOT1NUSUMgYW5hbHlz
aXMgb2YgdGhlIFBoYXNlLTEgbGFkZGVyIGNoZWNrcG9pbnQgKDVlZTE1MmZjKTogTk9UIHRoZSBl
bGVjdGVkIGVzdGltYXRvci4KKDEpIHBlci1ydW5nIHJfVCBhY3Jvc3Mgbl9iIHdpdGggdGhlIEEt
MSBmbG9vciBzaWdtYTsgKDIpIHRoZSBjLWZyZWUgam9pbnQgZml0IG9tZWdhX1QvayA9IGMoMSAr
IGEyIHggKyBhNCB4XjIpIG9uCmFsbCBydW5ncyB2cyBmbG9vci1jbGVhbiBydW5ncyAoc2lnbWFf
ciA8IDFlLTYpLiBSZWFkcyB0aGUgY2hlY2twb2ludCBvbmx5OyBjaGFuZ2VzIG5vIHZhbHVlIGlu
IGl0LiIiIgppbXBvcnQganNvbiwgaGFzaGxpYiwgbnVtcHkgYXMgbnAKY2sgPSBqc29uLmxvYWQo
b3BlbigiZ19zMmMxX3BoYXNlMV9sYWRkZXJfY2hlY2twb2ludC5qc29uIikpOyBydW5zID0gY2tb
InN0ZXAzX2xhZGRlciJdWyJydW5zIl07IEEgPSAxLjQ2MDU5Cm91dCA9IHsic291cmNlX2NoZWNr
cG9pbnRfbWQ1IjogaGFzaGxpYi5tZDUob3BlbigiZ19zMmMxX3BoYXNlMV9sYWRkZXJfY2hlY2tw
b2ludC5qc29uIiwgInJiIikucmVhZCgpKS5oZXhkaWdlc3QoKSwgImVzdGltYXRvciI6ICJESUFH
Tk9TVElDIGpvaW50IGZpdCAoYyBmcmVlKTsgdGhlIGVsZWN0ZWQgZXN0aW1hdG9yJ3MgdmFsdWVz
IGFyZSBpbiB0aGUgY2hlY2twb2ludCIsICJwZXJfZGlyZWN0aW9uIjoge319CmZvciBkZCBpbiAo
IkdLIiwgIkdNIik6CiAgICByZWMgPSB7InBlcl9ydW5nIjogW10sICJqb2ludF9maXQiOiB7fX0K
ICAgIGthID0gbnAuYXJyYXkocnVuc1siNDAiXVsiVCJdW2RkXVsia2EiXSk7IHNpZyA9IG5wLmFy
cmF5KHJ1bnNbIjQwIl1bIlQiXVtkZF1bImZsb29yX3NpZ21hX3IiXSkKICAgIGZvciBpLCBrIGlu
IGVudW1lcmF0ZShrYSk6CiAgICAgICAgcmVjWyJwZXJfcnVuZyJdLmFwcGVuZCh7ImthIjogZmxv
YXQoayksICJyMjQiOiBydW5zWyIyNCJdWyJUIl1bZGRdWyJyIl1baV0sICJyMzIiOiBydW5zWyIz
MiJdWyJUIl1bZGRdWyJyIl1baV0sICJyNDAiOiBydW5zWyI0MCJdWyJUIl1bZGRdWyJyIl1baV0s
ICJmbG9vcl9zaWdtYV9yX25iNDAiOiBmbG9hdChzaWdbaV0pfSkKICAgIGZvciBuYiBpbiAoIjI0
IiwgIjMyIiwgIjQwIik6CiAgICAgICAga2IgPSBucC5hcnJheShydW5zW25iXVsiVCJdW2RkXVsi
a2EiXSk7IG9tID0gbnAuYXJyYXkoW2VbIlQiXVsib21lZ2EiXSBmb3IgZSBpbiBydW5zW25iXVsi
aWRlbnQiXVtkZF1dKTsgeSA9IG9tIC8gKGtiIC8gQSkKICAgICAgICBmb3IgbGFiLCBzZWwgaW4g
KCgiYWxsX3J1bmdzIiwga2IgPiAwKSwgKCJmbG9vcl9jbGVhbl9ydW5nc19rYV9nZV8wLjAzNzUi
LCBrYiA+PSAwLjAzNykpOgogICAgICAgICAgICBYID0gbnAuc3RhY2soW25wLm9uZXMoc2VsLnN1
bSgpKSwga2Jbc2VsXSoqMiwga2Jbc2VsXSoqNF0sIGF4aXM9MSk7IGMsICpfID0gbnAubGluYWxn
LmxzdHNxKFgsIHlbc2VsXSwgcmNvbmQ9Tm9uZSkKICAgICAgICAgICAgcmVjWyJqb2ludF9maXQi
XVsibmIlc18lcyIgJSAobmIsIGxhYildID0geyJjX1QiOiBmbG9hdChjWzBdKSwgImEyIjogZmxv
YXQoY1sxXSAvIGNbMF0pLCAiYTQiOiBmbG9hdChjWzJdIC8gY1swXSksICJuX3J1bmdzIjogaW50
KHNlbC5zdW0oKSl9CiAgICBhID0gW3JlY1siam9pbnRfZml0Il1bIm5iJXNfZmxvb3JfY2xlYW5f
cnVuZ3Nfa2FfZ2VfMC4wMzc1IiAlIG5iXVsiYTIiXSBmb3IgbmIgaW4gKCIyNCIsICIzMiIsICI0
MCIpXQogICAgcmVjWyJhMl9mbG9vcl9jbGVhbl9yZWxfZHJpZnQiXSA9IHsiMjR2MzIiOiBhYnMo
YVsxXSAtIGFbMF0pIC8gYWJzKGFbMV0pLCAiMzJ2NDAiOiBhYnMoYVsyXSAtIGFbMV0pIC8gYWJz
KGFbMl0pfQogICAgcmVjWyJhMl9mbG9vcl9jbGVhbl9uYjQwIl0gPSBhWzJdOyByZWNbImE0X2Zs
b29yX2NsZWFuX25iNDAiXSA9IHJlY1siam9pbnRfZml0Il1bIm5iNDBfZmxvb3JfY2xlYW5fcnVu
Z3Nfa2FfZ2VfMC4wMzc1Il1bImE0Il0KICAgIHJlY1siY19UX2Zsb29yX2NsZWFuX25iNDAiXSA9
IHJlY1siam9pbnRfZml0Il1bIm5iNDBfZmxvb3JfY2xlYW5fcnVuZ3Nfa2FfZ2VfMC4wMzc1Il1b
ImNfVCJdCiAgICBvdXRbInBlcl9kaXJlY3Rpb24iXVtkZF0gPSByZWMKb3V0WyJyZWFkaW5nIl0g
PSAoIlRoZSBuX2IgZHJpZnQgb2YgdGhlIGVsZWN0ZWQgZXN0aW1hdG9yIGlzIGEgdW5pZm9ybSBv
ZmZzZXQgaW4gcl9UIG9mIH4xZS01IGFjcm9zcyBydW5ncyA9IGEgc2hpZnQgb2YgdGhlIGstPjAg
c3BlZWQgIgogICAgICAgICAgICAgICAgICAiZXh0cmFwb2xhdGVkIGZyb20gdGhlIHNtYWxsLWsg
c3BlZWQgc2V0LCB3aGVyZSB0aGUgZGVuc2UtZWlnIGZsb29yIChBLTEgdGVybSkgaXMgfjEuNWUt
NSBpbiByOyB0aGUgVC1icmFuY2ggb21lZ2FzIGF0ICIKICAgICAgICAgICAgICAgICAgImthID49
IDAuMDM3NSBhZ3JlZSBhY3Jvc3Mgbl9iIHRvIH4xZS02LiBUaGUgYy1mcmVlIGpvaW50IGZpdCBv
biBmbG9vci1jbGVhbiBydW5ncyBjb252ZXJnZXMgdG8gPD0gM2UtMyByZWxhdGl2ZSBpbiBhMi4i
KQpiID0gKGpzb24uZHVtcHMob3V0LCBpbmRlbnQ9MSwgc29ydF9rZXlzPVRydWUpICsgIlxuIiku
ZW5jb2RlKCk7IG9wZW4oInMyYzFfcGhhc2UxX2xhZGRlcl9hbmFseXNpcy5qc29uIiwgIndiIiku
d3JpdGUoYikKcHJpbnQoImFuYWx5c2lzIG1kNSIsIGhhc2hsaWIubWQ1KGIpLmhleGRpZ2VzdCgp
LCBsZW4oYiksICJCIikKZm9yIGRkIGluICgiR0siLCAiR00iKTogcHJpbnQoZGQsICJhMl9mYyg0
MCkgJSsuNWUgYTRfZmMoNDApICUrLjRlIGNfVCAlLjZmIGRyaWZ0IDI0djMyICUuMWUgMzJ2NDAg
JS4xZSIgJSAob3V0WyJwZXJfZGlyZWN0aW9uIl1bZGRdWyJhMl9mbG9vcl9jbGVhbl9uYjQwIl0s
IG91dFsicGVyX2RpcmVjdGlvbiJdW2RkXVsiYTRfZmxvb3JfY2xlYW5fbmI0MCJdLCBvdXRbInBl
cl9kaXJlY3Rpb24iXVtkZF1bImNfVF9mbG9vcl9jbGVhbl9uYjQwIl0sIG91dFsicGVyX2RpcmVj
dGlvbiJdW2RkXVsiYTJfZmxvb3JfY2xlYW5fcmVsX2RyaWZ0Il1bIjI0djMyIl0sIG91dFsicGVy
X2RpcmVjdGlvbiJdW2RkXVsiYTJfZmxvb3JfY2xlYW5fcmVsX2RyaWZ0Il1bIjMydjQwIl0pKQo=
<<<EMBED-END name=s2c1_phase1_ladder_analysis.py>>>

### EMBED — framework core used by the chat leg (Cell/BdG) — NOT for reuse — `gz1_core.py` (md5 361b1743a9164d1f7ff2380f6b74840d, 18205 B, b64, QUARANTINED)

<<<EMBED-BEGIN name=gz1_core.py md5=361b1743a9164d1f7ff2380f6b74840d bytes=18205 enc=b64 quarantine=1>>>
IiIiCmd6MV9jb3JlLnB5IOKAlCBHYXRlIEctemV0YTEgc2hhcmVkIGtlcm5lbHMgKFJFQlVJTEQp
Cj09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT0KUmVj
b25zdHJ1Y3Rpb24gb2YgdGhlIGxvc3QgR1oxIGluc3RydW1lbnQgY29yZSwgcmVidWlsdCBmcm9t
IHRoZSBzdXJ2aXZpbmcKR1oxX0VYRUNVVElPTl9QUkVSRUdJU1RSQVRJT04ubWQgKyBHWjFfR0FU
RV9FWEVDVVRJT05fUkVQT1JULm1kIChvcmlnaW5hbHMgbG9zdAp0byBhIHNhbmRib3ggcmVzZXQ7
IG9yaWdpbmFsIGd6MV9jb3JlLnB5IG1kNSAxM2QwMWNmOCkuIFNlbGYtY29udGFpbmVkOgpudW1w
eS9zY2lweSBvbmx5OyBpbXBvcnRzIE5PIGZyYW1ld29yayB0b29sLgoKTW9kZWwgKGJpbmRpbmcs
IHByZXJlZyk6IGhiYXIgPSBtID0gMSwgMi1ELgogICAgRVtwc2ldID0gaW50IDEvMnxncmFkIHBz
aXxeMiArIDEvMiBpaW50IHJobyh4KVUoeC14JylyaG8oeCcpIC0gbXUgaW50IHJobwpTb2Z0LWNv
cmUgVShyKSA9IGcqdGhldGEoUi1yKSwgZz0yMi4wLCBSPTEuMCwgcmhvMD0xLjAuCkNvbnRpbnV1
bSBGb3VyaWVyIGtlcm5lbCAgVXRpbGRlKHEpID0gMipwaSpnKlJeMiAqIEoxKHFSKS8ocVIpLCAg
VXRpbGRlKDApPWcqcGkqUl4yLgoKQmRHIChiaW5kaW5nLCBwcmVyZWcpOiBvbWVnYV4yIGYgPSBM
KEwrMlgpIGYsICBMID0gLTEvMiBncmFkXjIgKyAoVSpyaG8wKSAtIG11CihQU0Q7IHBzaTAgaXRz
IGdyb3VuZCBzdGF0ZSksIFggZiA9IHBzaTAgKiBVKihwc2kwIGYpLiBIZXJtaXRpYW4gZm9ybQpM
XnsxLzJ9IChMKzJYKSBMXnsxLzJ9LgoKTk9URTogdGhlIGNvbXBhcmlzb24gdGFyZ2V0IGNvbnN0
YW50IGFwcGVhcnMgaW4gTk8gZnVuY3Rpb24gaGVyZSAoRWRkaW5ndG9uCmlzb2xhdGlvbiDigJQg
Y29tcGFyaXNvbl9zdGVwLnB5IG9ubHkpLgoiIiIKCmltcG9ydCBudW1weSBhcyBucApmcm9tIHNj
aXB5LnNwZWNpYWwgaW1wb3J0IGoxCgpHX0NPVVBMSU5HID0gMjIuMApSX0NPUkUgPSAxLjAKUkhP
MCA9IDEuMAoKCiMgLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0t
LS0tLS0tLS0tLS0tLS0tLS0tLSBrZXJuZWxzIC0tLS0KZGVmIFVfdGlsZGUocSk6CiAgICAiIiJD
b250aW51dW0gc29mdC1jb3JlIGtlcm5lbCBGVDogMipwaSpnKlJeMiBKMShxUikvKHFSKTsgVSgw
KT1nKnBpKlJeMi4iIiIKICAgIHEgPSBucC5hc2FycmF5KHEsIGZsb2F0KQogICAgb3V0ID0gbnAu
ZnVsbChxLnNoYXBlLCBHX0NPVVBMSU5HICogbnAucGkgKiBSX0NPUkUqKjIpCiAgICBueiA9IHEg
PiAxZS0xMgogICAgeCA9IHFbbnpdICogUl9DT1JFCiAgICBvdXRbbnpdID0gMi4wICogbnAucGkg
KiBHX0NPVVBMSU5HICogUl9DT1JFKioyICogajEoeCkgLyB4CiAgICByZXR1cm4gb3V0CgoKZGVm
IFVfZGlza19mZnQoTiwgTCk6CiAgICAiIiJHcmlkLUZGVCBrZXJuZWwgb2YgdGhlIHJlYWwtc3Bh
Y2UgZGlzayAodGhlIFY0LjI2IG12X2cxIGRpc2NyZXRpc2F0aW9uKSwKICAgIHVzZWQgT05MWSBm
b3IgdGhlIHBoYXNlLTEgY2Fub25pY2FsLW9iamVjdCByZXBsaWNhdGlvbiBjcm9zcy1jaGVjay4i
IiIKICAgIGR4ID0gTCAvIE4KICAgIHggPSAobnAuYXJhbmdlKE4pIC0gTiAvLyAyKSAqIGR4CiAg
ICBYLCBZID0gbnAubWVzaGdyaWQoeCwgeCwgaW5kZXhpbmc9ImlqIikKICAgIFVyID0gbnAud2hl
cmUobnAuc3FydChYKioyICsgWSoqMikgPCBSX0NPUkUsIEdfQ09VUExJTkcsIDAuMCkKICAgIHJl
dHVybiBucC5mZnQuZmZ0MihucC5mZnQuaWZmdHNoaWZ0KFVyKSkucmVhbCAqIGR4KioyCgoKIyAt
LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLSBzcXVh
cmUgLyByZWN0IGdyaWRzIC0tLS0KZGVmIHJlY3RfZ3JpZHMoTngsIE55LCBMeCwgTHkpOgogICAg
ZHgsIGR5ID0gTHggLyBOeCwgTHkgLyBOeQogICAgeCA9IG5wLmFyYW5nZShOeCkgKiBkeAogICAg
eSA9IG5wLmFyYW5nZShOeSkgKiBkeQogICAgWCwgWSA9IG5wLm1lc2hncmlkKHgsIHksIGluZGV4
aW5nPSJpaiIpCiAgICBreCA9IDIgKiBucC5waSAqIG5wLmZmdC5mZnRmcmVxKE54LCBkPWR4KQog
ICAga3kgPSAyICogbnAucGkgKiBucC5mZnQuZmZ0ZnJlcShOeSwgZD1keSkKICAgIEtYLCBLWSA9
IG5wLm1lc2hncmlkKGt4LCBreSwgaW5kZXhpbmc9ImlqIikKICAgIHJldHVybiBYLCBZLCBLWCwg
S1ksIEtYKioyICsgS1kqKjIsIGR4LCBkeQoKCmRlZiByZWxheF9yZWN0KHBzaSwgSzIsIFVrLCBk
dGF1LCBzdGVwcywgdG9sPTFlLTEyLCByZXBvcnRfZXZlcnk9MjAwKToKICAgICIiIkltYWdpbmFy
eS10aW1lIHNwbGl0LXN0ZXAgR1AgcmVsYXhhdGlvbiBhdCBmaXhlZCBtZWFuIGRlbnNpdHkgcmhv
MC4KICAgIFVrID0ga2VybmVsIGFycmF5IG9uIHRoZSBzYW1lIGstZ3JpZC4gUmV0dXJucyAocHNp
LCBtdSwgcmVzaWR1YWwpLiIiIgogICAgTjIgPSBwc2kuc2l6ZQogICAgbm9ybV90YXJnZXQgPSBS
SE8wICogTjIKCiAgICBkZWYgcmVub3JtKHApOgogICAgICAgIHJldHVybiBwICogbnAuc3FydChu
b3JtX3RhcmdldCAvIG5wLnN1bShucC5hYnMocCkgKiogMikpCgogICAgcHNpID0gcmVub3JtKHBz
aSkKICAgIEtwcm9wID0gbnAuZXhwKC0wLjI1ICogSzIgKiBkdGF1KQogICAgZV9wcmV2ID0gTm9u
ZQogICAgZm9yIGl0IGluIHJhbmdlKHN0ZXBzKToKICAgICAgICBwc2kgPSBucC5mZnQuaWZmdDIo
S3Byb3AgKiBucC5mZnQuZmZ0Mihwc2kpKQogICAgICAgIHJobyA9IG5wLmFicyhwc2kpICoqIDIK
ICAgICAgICBVY29udiA9IG5wLmZmdC5pZmZ0MihVayAqIG5wLmZmdC5mZnQyKHJobykpLnJlYWwK
ICAgICAgICBwc2kgPSBwc2kgKiBucC5leHAoLVVjb252ICogZHRhdSkKICAgICAgICBwc2kgPSBu
cC5mZnQuaWZmdDIoS3Byb3AgKiBucC5mZnQuZmZ0Mihwc2kpKQogICAgICAgIHBzaSA9IHJlbm9y
bShwc2kpCiAgICAgICAgaWYgaXQgJSByZXBvcnRfZXZlcnkgPT0gMCBvciBpdCA9PSBzdGVwcyAt
IDE6CiAgICAgICAgICAgIG11LCByZXMgPSBtdV9yZXNpZHVhbF9yZWN0KHBzaSwgSzIsIFVrKQog
ICAgICAgICAgICBpZiBlX3ByZXYgaXMgbm90IE5vbmUgYW5kIGFicyhtdSAtIGVfcHJldikgPCB0
b2wgKiBtYXgoMS4wLCBhYnMobXUpKToKICAgICAgICAgICAgICAgIGJyZWFrCiAgICAgICAgICAg
IGVfcHJldiA9IG11CiAgICBwc2kgPSBucC5yZWFsKHBzaSkgICAgICAgICAgICAjIGdyb3VuZCBz
dGF0ZSBpcyByZWFsIHVwIHRvIHBoYXNlCiAgICBwc2kgPSByZW5vcm0ocHNpKQogICAgbXUsIHJl
cyA9IG11X3Jlc2lkdWFsX3JlY3QocHNpLCBLMiwgVWspCiAgICByZXR1cm4gcHNpLCBtdSwgcmVz
CgoKZGVmIG11X3Jlc2lkdWFsX3JlY3QocHNpLCBLMiwgVWspOgogICAgIiIibXUgPSA8cHNpfEh8
cHNpPi88cHNpfHBzaT47IHJlc2lkdWFsID0gfHxIIHBzaSAtIG11IHBzaXx8IC8gKG11IHx8cHNp
fHwpLiIiIgogICAgcmhvID0gbnAuYWJzKHBzaSkgKiogMgogICAgVWNvbnYgPSBucC5mZnQuaWZm
dDIoVWsgKiBucC5mZnQuZmZ0MihyaG8pKS5yZWFsCiAgICBIcHNpID0gbnAuZmZ0LmlmZnQyKDAu
NSAqIEsyICogbnAuZmZ0LmZmdDIocHNpKSkgKyBVY29udiAqIHBzaQogICAgbXUgPSBmbG9hdChu
cC5yZWFsKG5wLnZkb3QocHNpLCBIcHNpKSAvIG5wLnZkb3QocHNpLCBwc2kpKSkKICAgIHJlcyA9
IGZsb2F0KG5wLmxpbmFsZy5ub3JtKEhwc2kgLSBtdSAqIHBzaSkgLyAoYWJzKG11KSAqIG5wLmxp
bmFsZy5ub3JtKHBzaSkpKQogICAgcmV0dXJuIG11LCByZXMKCgojIC0tLS0tLS0tLS0tLS0tLS0t
LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLSBwZWFrIC8gb3JkZXIgZGlhZ25vc3RpY3Mg
LS0tLQpkZWYgbG9jYWxfbWF4aW1hKHJobywgdGhyZXNoKToKICAgIG0gPSBucC5vbmVzX2xpa2Uo
cmhvLCBkdHlwZT1ib29sKQogICAgZm9yIHN4IGluICgtMSwgMCwgMSk6CiAgICAgICAgZm9yIHN5
IGluICgtMSwgMCwgMSk6CiAgICAgICAgICAgIGlmIHN4ID09IDAgYW5kIHN5ID09IDA6CiAgICAg
ICAgICAgICAgICBjb250aW51ZQogICAgICAgICAgICBtICY9IHJobyA+PSBucC5yb2xsKG5wLnJv
bGwocmhvLCBzeCwgYXhpcz0wKSwgc3ksIGF4aXM9MSkKICAgIG0gJj0gcmhvID4gdGhyZXNoCiAg
ICByZXR1cm4gbnAuYXJnd2hlcmUobSkKCgpkZWYgYm9uZF9vcmllbnRhdGlvbmFsKHJobywgZHgs
IEwsIGtubj02KToKICAgICIiIkxvY2FsIHBzaTYvcHNpNCBvdmVyIGRldGVjdGVkIHBlYWtzLCBt
aW5pbXVtLWltYWdlIChyZXBsaWNhdGVzIHRoZSBWNC4yNgogICAgZXN0aW1hdG9yOiBwZWFrcyBh
Ym92ZSBtZWFuKzAuNSpzdGQsIDYgbmVhcmVzdCBuZWlnaGJvdXJzKS4iIiIKICAgIG1lYW4sIHN0
ZCA9IHJoby5tZWFuKCksIHJoby5zdGQoKQogICAgcGVha3MgPSBsb2NhbF9tYXhpbWEocmhvLCBt
ZWFuICsgMC41ICogc3RkKQogICAgaWYgbGVuKHBlYWtzKSA8IDc6CiAgICAgICAgcmV0dXJuIGRp
Y3QocHNpNF9sb2NhbD0wLjAsIHBzaTZfbG9jYWw9MC4wLCBuX3BlYWtzPWludChsZW4ocGVha3Mp
KSkKICAgIFAgPSBwZWFrcy5hc3R5cGUoZmxvYXQpICogZHgKICAgIG4gPSBsZW4oUCkKICAgIHA0
ID0gbnAuemVyb3MobiwgY29tcGxleCkKICAgIHA2ID0gbnAuemVyb3MobiwgY29tcGxleCkKICAg
IGZvciBpIGluIHJhbmdlKG4pOgogICAgICAgIGQgPSBQIC0gUFtpXQogICAgICAgIGQgLT0gTCAq
IG5wLnJvdW5kKGQgLyBMKQogICAgICAgIGRpc3QgPSBucC5oeXBvdChkWzosIDBdLCBkWzosIDFd
KQogICAgICAgIG5iID0gbnAuYXJnc29ydChkaXN0KVsxOmtubiArIDFdCiAgICAgICAgYW5nID0g
bnAuYXJjdGFuMihkW25iLCAxXSwgZFtuYiwgMF0pCiAgICAgICAgcDRbaV0gPSBucC5tZWFuKG5w
LmV4cCg0aiAqIGFuZykpCiAgICAgICAgcDZbaV0gPSBucC5tZWFuKG5wLmV4cCg2aiAqIGFuZykp
CiAgICByZXR1cm4gZGljdChwc2k0X2xvY2FsPWZsb2F0KG5wLm1lYW4obnAuYWJzKHA0KSkpLAog
ICAgICAgICAgICAgICAgcHNpNl9sb2NhbD1mbG9hdChucC5tZWFuKG5wLmFicyhwNikpKSwgbl9w
ZWFrcz1uKQoKCmRlZiBzdHJ1Y3R1cmVfa2MocmhvLCBLWCwgS1kpOgogICAgUyA9IG5wLmFicyhu
cC5mZnQuZmZ0MihyaG8gLSByaG8ubWVhbigpKSkgKiogMgogICAgUy5mbGF0WzBdID0gMC4wCiAg
ICBrbWFnID0gbnAuc3FydChLWCoqMiArIEtZKioyKQogICAgcmV0dXJuIGZsb2F0KGttYWcuZmxh
dFtucC5hcmdtYXgoUyldKQoKCiMgLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0t
LS0tLS0tLS0tLS0tLS0tLS0tLS0tIG9ibGlxdWUgY2VsbCAtLS0tLS0tCmNsYXNzIENlbGw6CiAg
ICAiIiJPYmxpcXVlIHRyaWFuZ3VsYXIgcHJpbWl0aXZlIGNlbGw6IGExPShhLDApLCBhMj0oYS8y
LCBzcXJ0MyBhLzIpLAogICAgbiB4IG4gZnJhY3Rpb25hbCBncmlkLiBGRlQgaW5kZXggKG0xLG0y
KSAtPiBHID0gbTEgYjEgKyBtMiBiMi4iIiIKCiAgICBkZWYgX19pbml0X18oc2VsZiwgYSwgbik6
CiAgICAgICAgc2VsZi5hLCBzZWxmLm4gPSBmbG9hdChhKSwgaW50KG4pCiAgICAgICAgczMgPSBu
cC5zcXJ0KDMuMCkKICAgICAgICBzZWxmLmExID0gbnAuYXJyYXkoW2EsIDAuMF0pCiAgICAgICAg
c2VsZi5hMiA9IG5wLmFycmF5KFthIC8gMi4wLCBzMyAqIGEgLyAyLjBdKQogICAgICAgIHNlbGYu
YXJlYSA9IGEgKiBhICogczMgLyAyLjAKICAgICAgICBzZWxmLmIxID0gMiAqIG5wLnBpICogbnAu
YXJyYXkoWzEuMCAvIGEsIC0xLjAgLyAoczMgKiBhKV0pCiAgICAgICAgc2VsZi5iMiA9IDIgKiBu
cC5waSAqIG5wLmFycmF5KFswLjAsIDIuMCAvIChzMyAqIGEpXSkKICAgICAgICBtID0gbnAuZmZ0
LmZmdGZyZXEobiwgZD0xLjAgLyBuKSAgICAgICAgICAjIGludGVnZXJzIDAuLm4vMi0xLCAtbi8y
Li4tMQogICAgICAgIE0xLCBNMiA9IG5wLm1lc2hncmlkKG0sIG0sIGluZGV4aW5nPSJpaiIpCiAg
ICAgICAgc2VsZi5NMSwgc2VsZi5NMiA9IE0xLmFzdHlwZShpbnQpLCBNMi5hc3R5cGUoaW50KQog
ICAgICAgIHNlbGYuR3ggPSBNMSAqIHNlbGYuYjFbMF0gKyBNMiAqIHNlbGYuYjJbMF0KICAgICAg
ICBzZWxmLkd5ID0gTTEgKiBzZWxmLmIxWzFdICsgTTIgKiBzZWxmLmIyWzFdCiAgICAgICAgc2Vs
Zi5HMiA9IHNlbGYuR3gqKjIgKyBzZWxmLkd5KioyCiAgICAgICAgc2VsZi5VayA9IFVfdGlsZGUo
bnAuc3FydChzZWxmLkcyKSkKICAgICAgICAjIHJlYWwtc3BhY2UgcG9pbnRzCiAgICAgICAgZiA9
IG5wLmFyYW5nZShuKSAvIG4KICAgICAgICBGMSwgRjIgPSBucC5tZXNoZ3JpZChmLCBmLCBpbmRl
eGluZz0iaWoiKQogICAgICAgIHNlbGYuWCA9IEYxICogc2VsZi5hMVswXSArIEYyICogc2VsZi5h
MlswXQogICAgICAgIHNlbGYuWSA9IEYxICogc2VsZi5hMVsxXSArIEYyICogc2VsZi5hMlsxXQoK
ICAgIGRlZiByZWxheChzZWxmLCBzdGVwcz0zMDAwLCBkdGF1PTJlLTMsIHNpZ21hX3NlZWQ9Tm9u
ZSwgbm9pc2U9MC4wLCBzZWVkPTAsCiAgICAgICAgICAgICAgcHNpX2luaXQ9Tm9uZSwgdG9sPTFl
LTEzKToKICAgICAgICBuID0gc2VsZi5uCiAgICAgICAgaWYgcHNpX2luaXQgaXMgbm90IE5vbmU6
CiAgICAgICAgICAgIHBzaSA9IHBzaV9pbml0LmFzdHlwZShjb21wbGV4KS5jb3B5KCkKICAgICAg
ICBlbHNlOgogICAgICAgICAgICBpZiBzaWdtYV9zZWVkIGlzIE5vbmU6CiAgICAgICAgICAgICAg
ICBzaWdtYV9zZWVkID0gMC4zNSAqIHNlbGYuYQogICAgICAgICAgICBkeHYgPSBzZWxmLlggLSBz
ZWxmLmExWzBdIC8gMiAtIHNlbGYuYTJbMF0gLyAyCiAgICAgICAgICAgIGR5diA9IHNlbGYuWSAt
IHNlbGYuYTJbMV0gLyAyCiAgICAgICAgICAgIHBzaSA9IG5wLmV4cCgtKGR4dioqMiArIGR5dioq
MikgLyAoMiAqIHNpZ21hX3NlZWQqKjIpKS5hc3R5cGUoY29tcGxleCkKICAgICAgICAgICAgaWYg
bm9pc2U6CiAgICAgICAgICAgICAgICBybmcgPSBucC5yYW5kb20uZGVmYXVsdF9ybmcoc2VlZCkK
ICAgICAgICAgICAgICAgIHBzaSArPSBub2lzZSAqIHJuZy5zdGFuZGFyZF9ub3JtYWwoKG4sIG4p
KQogICAgICAgIG5vcm1fdGFyZ2V0ID0gUkhPMCAqIG4gKiBuCgogICAgICAgIGRlZiByZW5vcm0o
cCk6CiAgICAgICAgICAgIHJldHVybiBwICogbnAuc3FydChub3JtX3RhcmdldCAvIG5wLnN1bShu
cC5hYnMocCkgKiogMikpCgogICAgICAgIHBzaSA9IHJlbm9ybShwc2kpCiAgICAgICAgS3Byb3Ag
PSBucC5leHAoLTAuMjUgKiBzZWxmLkcyICogZHRhdSkKICAgICAgICBtdV9wcmV2ID0gTm9uZQog
ICAgICAgIGZvciBpdCBpbiByYW5nZShzdGVwcyk6CiAgICAgICAgICAgIHBzaSA9IG5wLmZmdC5p
ZmZ0MihLcHJvcCAqIG5wLmZmdC5mZnQyKHBzaSkpCiAgICAgICAgICAgIHJobyA9IG5wLmFicyhw
c2kpICoqIDIKICAgICAgICAgICAgVWMgPSBucC5mZnQuaWZmdDIoc2VsZi5VayAqIG5wLmZmdC5m
ZnQyKHJobykpLnJlYWwKICAgICAgICAgICAgcHNpID0gcHNpICogbnAuZXhwKC1VYyAqIGR0YXUp
CiAgICAgICAgICAgIHBzaSA9IG5wLmZmdC5pZmZ0MihLcHJvcCAqIG5wLmZmdC5mZnQyKHBzaSkp
CiAgICAgICAgICAgIHBzaSA9IHJlbm9ybShwc2kpCiAgICAgICAgICAgIGlmIGl0ICUgMTAwID09
IDAgb3IgaXQgPT0gc3RlcHMgLSAxOgogICAgICAgICAgICAgICAgbXUsIF8gPSBzZWxmLm11X3Jl
c2lkdWFsKHBzaS5yZWFsKQogICAgICAgICAgICAgICAgaWYgbXVfcHJldiBpcyBub3QgTm9uZSBh
bmQgYWJzKG11IC0gbXVfcHJldikgPCB0b2wgKiBhYnMobXUpOgogICAgICAgICAgICAgICAgICAg
IGJyZWFrCiAgICAgICAgICAgICAgICBtdV9wcmV2ID0gbXUKICAgICAgICBwc2kgPSByZW5vcm0o
bnAucmVhbChwc2kpKQogICAgICAgIG11LCByZXMgPSBzZWxmLm11X3Jlc2lkdWFsKHBzaSkKICAg
ICAgICByZXR1cm4gcHNpLCBtdSwgcmVzCgogICAgZGVmIG11X3Jlc2lkdWFsKHNlbGYsIHBzaSk6
CiAgICAgICAgcmhvID0gbnAuYWJzKHBzaSkgKiogMgogICAgICAgIFVjID0gbnAuZmZ0LmlmZnQy
KHNlbGYuVWsgKiBucC5mZnQuZmZ0MihyaG8pKS5yZWFsCiAgICAgICAgSHBzaSA9IG5wLmZmdC5p
ZmZ0MigwLjUgKiBzZWxmLkcyICogbnAuZmZ0LmZmdDIocHNpKSkucmVhbCArIFVjICogcHNpCiAg
ICAgICAgbXUgPSBmbG9hdChucC5zdW0ocHNpICogSHBzaSkgLyBucC5zdW0ocHNpICogcHNpKSkK
ICAgICAgICByZXMgPSBmbG9hdChucC5saW5hbGcubm9ybShIcHNpIC0gbXUgKiBwc2kpCiAgICAg
ICAgICAgICAgICAgICAgLyAoYWJzKG11KSAqIG5wLmxpbmFsZy5ub3JtKHBzaSkpKQogICAgICAg
IHJldHVybiBtdSwgcmVzCgogICAgZGVmIGVuZXJneV9kZW5zaXR5KHNlbGYsIHBzaSk6CiAgICAg
ICAgIiIiKGtpbmV0aWMgKyBpbnRlcmFjdGlvbikgcGVyIHVuaXQgYXJlYSBhdCBmaXhlZCBtZWFu
IGRlbnNpdHkgcmhvMD0xCiAgICAgICAgKHRoZSBjYW5vbmljYWwgc2NhbiBvYmplY3RpdmU7IHRo
ZSAtbXUqcmhvIHRlcm0gaXMgY29uc3RhbnQgb3ZlciB0aGUgc2NhbikuIiIiCiAgICAgICAgbiA9
IHNlbGYubgogICAgICAgIHBzID0gbnAuZmZ0LmZmdDIocHNpKSAvIG4qKjIKICAgICAgICBraW4g
PSAwLjUgKiBucC5zdW0oc2VsZi5HMiAqIG5wLmFicyhwcykgKiogMikKICAgICAgICByaCA9IG5w
LmZmdC5mZnQyKG5wLmFicyhwc2kpICoqIDIpIC8gbioqMgogICAgICAgIGludGVyID0gMC41ICog
bnAuc3VtKHNlbGYuVWsgKiBucC5hYnMocmgpICoqIDIpCiAgICAgICAgcmV0dXJuIGZsb2F0KGtp
biArIGludGVyKSAgICAgICAgIyBhbHJlYWR5IHBlci1hcmVhIChpbnRlbnNpdmUgY29lZmZpY2ll
bnRzKQoKCiMgLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0t
LS0tLS0tLS0tLS0tLSBCZEcgKGNlbGwpIC0tLS0tCmNsYXNzIEJkRzoKICAgICIiIlBsYW5lLXdh
dmUgQm9nb2xpdWJvdi1kZSBHZW5uZXMgb24gdGhlIGNyeXN0YWxsaXNlZCBjZWxsLgogICAgQmFz
aXM6IG5fYiB4IG5fYiBwbGFuZSB3YXZlcyBHKG0xLG0yKTsgcHNpMCBGb3VyaWVyIGNvZWZmaWNp
ZW50cyBhcmUgdGFrZW4KICAgIGZyb20gdGhlIHN1cHBsaWVkIHJlYWwtc3BhY2UgcHNpMCBncmlk
IChpdHMgb3duIG4geCBuIEZGVDsgY29lZmZpY2llbnQKICAgIGRpZmZlcmVuY2VzIG91dHNpZGUg
dGhlIGF2YWlsYWJsZSByYW5nZSBhcmUgMCDigJQgbG9nZ2VkIHRydW5jYXRpb24pLiIiIgoKICAg
IGRlZiBfX2luaXRfXyhzZWxmLCBjZWxsLCBwc2kwLCBtdSwgbl9iKToKICAgICAgICBzZWxmLmNl
bGwsIHNlbGYubXUsIHNlbGYubl9iID0gY2VsbCwgZmxvYXQobXUpLCBpbnQobl9iKQogICAgICAg
IG4gPSBjZWxsLm4KICAgICAgICBjb2VmID0gbnAuZmZ0LmZmdDIocHNpMCkgLyBuKioyICAgICAg
ICAgICAgICAgICAgICAgIyBwc2kwX2hhdChtMSxtMikKICAgICAgICByY29lZiA9IG5wLmZmdC5m
ZnQyKG5wLmFicyhwc2kwKSAqKiAyKSAvIG4qKjIgICAgICAgIyByaG8wX2hhdAogICAgICAgIFZj
b2VmID0gY2VsbC5VayAqIHJjb2VmICAgICAgICAgICAgICAgICAgICAgICAgICAgICAjIChVKnJo
bzApX2hhdAogICAgICAgIG0gPSBucC5mZnQuZmZ0ZnJlcShuX2IsIGQ9MS4wIC8gbl9iKS5hc3R5
cGUoaW50KQogICAgICAgIE0xLCBNMiA9IG5wLm1lc2hncmlkKG0sIG0sIGluZGV4aW5nPSJpaiIp
CiAgICAgICAgc2VsZi5tMSA9IE0xLnJhdmVsKCkKICAgICAgICBzZWxmLm0yID0gTTIucmF2ZWwo
KQogICAgICAgIG5iMiA9IG5fYiAqIG5fYgoKICAgICAgICBkZWYgY29lZl9sb29rdXAoQywgZDEs
IGQyKToKICAgICAgICAgICAgIiIiQ1soZDEgbW9kIG4sIGQyIG1vZCBuKV0gaWYgfGQxfCx8ZDJ8
IDwgbi8yIGVsc2UgMCAoYW50aS1hbGlhcykuIiIiCiAgICAgICAgICAgIG91dCA9IG5wLnplcm9z
KGQxLnNoYXBlLCBjb21wbGV4KQogICAgICAgICAgICBvayA9IChucC5hYnMoZDEpIDwgbiAvLyAy
KSAmIChucC5hYnMoZDIpIDwgbiAvLyAyKQogICAgICAgICAgICBvdXRbb2tdID0gQ1tkMVtva10g
JSBuLCBkMltva10gJSBuXQogICAgICAgICAgICByZXR1cm4gb3V0CgogICAgICAgIEQxID0gc2Vs
Zi5tMVs6LCBOb25lXSAtIHNlbGYubTFbTm9uZSwgOl0KICAgICAgICBEMiA9IHNlbGYubTJbOiwg
Tm9uZV0gLSBzZWxmLm0yW05vbmUsIDpdCiAgICAgICAgc2VsZi5QID0gY29lZl9sb29rdXAoY29l
ZiwgRDEsIEQyKSAgICAgICAgICAgICAgICAgICMgcHNpMCBUb2VwbGl0eiBibG9jawogICAgICAg
IHNlbGYuVm1hdCA9IGNvZWZfbG9va3VwKFZjb2VmLCBEMSwgRDIpICAgICAgICAgICAgICAjIEhh
cnRyZWUgVG9lcGxpdHoKICAgICAgICBzZWxmLlAgPSAwLjUgKiAoc2VsZi5QICsgc2VsZi5QLmNv
bmooKS5UKSAgICAgICAgICAgIyBIZXJtaXRpc2UgKHBzaTAgcmVhbCkKICAgICAgICBzZWxmLlZt
YXQgPSAwLjUgKiAoc2VsZi5WbWF0ICsgc2VsZi5WbWF0LmNvbmooKS5UKQogICAgICAgIHNlbGYu
bmIyID0gbmIyCgogICAgZGVmIG9tZWdhcyhzZWxmLCBrLCBuYmFuZHM9MjQpOgogICAgICAgICIi
IkJkRyBmcmVxdWVuY2llcyBhdCBCbG9jaCB2ZWN0b3IgayAobG93ZXN0IG5iYW5kcykuIiIiCiAg
ICAgICAgYyA9IHNlbGYuY2VsbAogICAgICAgIGtneCA9IGtbMF0gKyBzZWxmLm0xICogYy5iMVsw
XSArIHNlbGYubTIgKiBjLmIyWzBdCiAgICAgICAga2d5ID0ga1sxXSArIHNlbGYubTEgKiBjLmIx
WzFdICsgc2VsZi5tMiAqIGMuYjJbMV0KICAgICAgICBraW4gPSAwLjUgKiAoa2d4KioyICsga2d5
KioyKQogICAgICAgIExtYXQgPSBucC5kaWFnKGtpbiAtIHNlbGYubXUpICsgc2VsZi5WbWF0CiAg
ICAgICAgTG1hdCA9IDAuNSAqIChMbWF0ICsgTG1hdC5jb25qKCkuVCkKICAgICAgICBEID0gVV90
aWxkZShucC5zcXJ0KGtneCoqMiArIGtneSoqMikpCiAgICAgICAgWG1hdCA9IHNlbGYuUCBAIChE
WzosIE5vbmVdICogc2VsZi5QKQogICAgICAgIFhtYXQgPSAwLjUgKiAoWG1hdCArIFhtYXQuY29u
aigpLlQpCiAgICAgICAgbGFtLCBVID0gbnAubGluYWxnLmVpZ2goTG1hdCkKICAgICAgICBsYW0g
PSBucC5jbGlwKGxhbSwgMC4wLCBOb25lKQogICAgICAgIExoID0gKFUgKiBucC5zcXJ0KGxhbSkp
IEAgVS5jb25qKCkuVAogICAgICAgIE0gPSBMaCBAIChMbWF0ICsgMi4wICogWG1hdCkgQCBMaAog
ICAgICAgIE0gPSAwLjUgKiAoTSArIE0uY29uaigpLlQpCiAgICAgICAgdzIgPSBucC5saW5hbGcu
ZWlndmFsc2goTSkKICAgICAgICB3ID0gbnAuc3FydChucC5jbGlwKHcyLCAwLjAsIE5vbmUpKQog
ICAgICAgIHJldHVybiBucC5zb3J0KHcpWzpuYmFuZHNdCgogICAgZGVmIExfZ2FtbWFfY2hlY2so
c2VsZiwgcHNpMF9jZWxsZ3JpZCk6CiAgICAgICAgIiIiU2FuaXR5IChhKTogbWluIGVpZyBvZiBM
KEdhbW1hKSBhbmQgb3ZlcmxhcCBvZiBpdHMgZWlndmVjIHdpdGggcHNpMC4iIiIKICAgICAgICBj
ID0gc2VsZi5jZWxsCiAgICAgICAga2d4ID0gc2VsZi5tMSAqIGMuYjFbMF0gKyBzZWxmLm0yICog
Yy5iMlswXQogICAgICAgIGtneSA9IHNlbGYubTEgKiBjLmIxWzFdICsgc2VsZi5tMiAqIGMuYjJb
MV0KICAgICAgICBMbWF0ID0gbnAuZGlhZygwLjUgKiAoa2d4KioyICsga2d5KioyKSAtIHNlbGYu
bXUpICsgc2VsZi5WbWF0CiAgICAgICAgTG1hdCA9IDAuNSAqIChMbWF0ICsgTG1hdC5jb25qKCku
VCkKICAgICAgICBsYW0sIFUgPSBucC5saW5hbGcuZWlnaChMbWF0KQogICAgICAgICMgcHNpMCBp
biB0aGUgcGxhbmUtd2F2ZSBiYXNpcwogICAgICAgIG4gPSBjLm4KICAgICAgICBjb2VmID0gbnAu
ZmZ0LmZmdDIocHNpMF9jZWxsZ3JpZCkgLyBuKioyCiAgICAgICAgdmVjID0gbnAuemVyb3Moc2Vs
Zi5uYjIsIGNvbXBsZXgpCiAgICAgICAgb2sgPSAobnAuYWJzKHNlbGYubTEpIDwgbiAvLyAyKSAm
IChucC5hYnMoc2VsZi5tMikgPCBuIC8vIDIpCiAgICAgICAgdmVjW29rXSA9IGNvZWZbc2VsZi5t
MVtva10gJSBuLCBzZWxmLm0yW29rXSAlIG5dCiAgICAgICAgdmVjIC89IG5wLmxpbmFsZy5ub3Jt
KHZlYykKICAgICAgICBvdiA9IGZsb2F0KG5wLmFicyhucC52ZG90KFVbOiwgMF0sIHZlYykpKQog
ICAgICAgIHJldHVybiBmbG9hdChsYW1bMF0pLCBvdgoKCiMgLS0tLS0tLS0tLS0tLS0tLS0tLS0t
LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tIGdhcCBjb3ZlcmFnZSAtLS0t
CmRlZiBnYXBzX2Zyb21fYmFuZHMoYmFuZF9hcnJheXMsIHdtYXg9MzYuMCwgbWluX3dpZHRoPTAu
MTUpOgogICAgIiIiU3RvcCBiYW5kcyA9IGludGVydmFscyBvZiBvbWVnYSBub3QgY292ZXJlZCBi
eSBhbnkgKGNvbnRpbnVvdXMsIHNvcnRlZCkKICAgIGJhbmQncyBbbWluLG1heF0gcmFuZ2UsIGJl
bG93IHdtYXguIiIiCiAgICBpdnMgPSBbXQogICAgbmIgPSBtaW4obGVuKGIpIGZvciBiIGluIGJh
bmRfYXJyYXlzKQogICAgQiA9IG5wLmFycmF5KFtiWzpuYl0gZm9yIGIgaW4gYmFuZF9hcnJheXNd
KSAgICAgICAgICAgICMgKG5rLCBuYikKICAgIGZvciBqIGluIHJhbmdlKG5iKToKICAgICAgICBp
dnMuYXBwZW5kKChmbG9hdChCWzosIGpdLm1pbigpKSwgZmxvYXQoQls6LCBqXS5tYXgoKSkpKQog
ICAgaXZzLnNvcnQoKQogICAgZ2FwcyA9IFtdCiAgICBjb3Zlcl9oaSA9IGl2c1swXVsxXQogICAg
Zm9yIGxvLCBoaSBpbiBpdnNbMTpdOgogICAgICAgIGlmIGxvID4gY292ZXJfaGkgKyAxZS05Ogog
ICAgICAgICAgICBpZiBsbyAtIGNvdmVyX2hpID49IG1pbl93aWR0aCBhbmQgY292ZXJfaGkgPCB3
bWF4OgogICAgICAgICAgICAgICAgZ2Fwcy5hcHBlbmQoKGNvdmVyX2hpLCBsbykpCiAgICAgICAg
ICAgIGNvdmVyX2hpID0gaGkKICAgICAgICBlbHNlOgogICAgICAgICAgICBjb3Zlcl9oaSA9IG1h
eChjb3Zlcl9oaSwgaGkpCiAgICByZXR1cm4gZ2FwcwoKCiMgLS0tLS0tLS0tLS0tLS0tLS0tLS0t
LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0gc3RyaXAgcmVzcG9uc2UgLS0t
LQpjbGFzcyBTdHJpcDoKICAgICIiIjE2LXJvdyBzdHJpcDogTHggPSBhLCBMeSA9IDE2KmQgKDgg
cmVjdGFuZ3VsYXIgY2VsbHMpLCBwZXJpb2RpYyBib3RoCiAgICBkaXJlY3Rpb25zLiBSb3dzIGF0
IHlfaiA9IGoqZCB3aXRoIGFsdGVybmF0aW5nIHgtb2Zmc2V0IDAsIGEvMi4iIiIKCiAgICBkZWYg
X19pbml0X18oc2VsZiwgYSwgTng9MzIsIE55PTUxMiwgbnJvd3M9MTYpOgogICAgICAgIHNlbGYu
YSA9IGZsb2F0KGEpCiAgICAgICAgc2VsZi5kID0gbnAuc3FydCgzLjApICogYSAvIDIuMAogICAg
ICAgIHNlbGYubnJvd3MgPSBucm93cwogICAgICAgIHNlbGYuTHgsIHNlbGYuTHkgPSBhLCBucm93
cyAqIHNlbGYuZAogICAgICAgIChzZWxmLlgsIHNlbGYuWSwgc2VsZi5LWCwgc2VsZi5LWSwgc2Vs
Zi5LMiwKICAgICAgICAgc2VsZi5keCwgc2VsZi5keSkgPSByZWN0X2dyaWRzKE54LCBOeSwgc2Vs
Zi5MeCwgc2VsZi5MeSkKICAgICAgICBzZWxmLlVrID0gVV90aWxkZShucC5zcXJ0KHNlbGYuSzIp
KQogICAgICAgIHNlbGYuTngsIHNlbGYuTnkgPSBOeCwgTnkKCiAgICBkZWYgc2VlZChzZWxmLCBz
aWdtYT1Ob25lKToKICAgICAgICBpZiBzaWdtYSBpcyBOb25lOgogICAgICAgICAgICBzaWdtYSA9
IDAuMzUgKiBzZWxmLmEKICAgICAgICBwc2kgPSBucC56ZXJvcygoc2VsZi5OeCwgc2VsZi5OeSkp
CiAgICAgICAgZm9yIGogaW4gcmFuZ2Uoc2VsZi5ucm93cyk6CiAgICAgICAgICAgIHgwID0gKGog
JSAyKSAqIHNlbGYuYSAvIDIuMAogICAgICAgICAgICB5MCA9IGogKiBzZWxmLmQKICAgICAgICAg
ICAgZHh2ID0gc2VsZi5YIC0geDAKICAgICAgICAgICAgZHh2IC09IHNlbGYuTHggKiBucC5yb3Vu
ZChkeHYgLyBzZWxmLkx4KQogICAgICAgICAgICBkeXYgPSBzZWxmLlkgLSB5MAogICAgICAgICAg
ICBkeXYgLT0gc2VsZi5MeSAqIG5wLnJvdW5kKGR5diAvIHNlbGYuTHkpCiAgICAgICAgICAgIHBz
aSArPSBucC5leHAoLShkeHYqKjIgKyBkeXYqKjIpIC8gKDIgKiBzaWdtYSoqMikpCiAgICAgICAg
cmV0dXJuIHBzaS5hc3R5cGUoY29tcGxleCkKCiAgICBkZWYgcmVsYXgoc2VsZiwgc3RlcHM9NjAw
MCwgZHRhdT0yZS0zKToKICAgICAgICBwc2ksIG11LCByZXMgPSByZWxheF9yZWN0KHNlbGYuc2Vl
ZCgpLCBzZWxmLksyLCBzZWxmLlVrLCBkdGF1LCBzdGVwcykKICAgICAgICBzZWxmLnBzaTAsIHNl
bGYubXUgPSBwc2ksIG11CiAgICAgICAgcmhvID0gcHNpKioyCiAgICAgICAgc2VsZi5WID0gbnAu
ZmZ0LmlmZnQyKHNlbGYuVWsgKiBucC5mZnQuZmZ0MihyaG8pKS5yZWFsCiAgICAgICAgcmV0dXJu
IHBzaSwgbXUsIHJlcwoKICAgICMgLS0gZHJpdmVuIHJlc3BvbnNlOiAoTCtYLXctaSBldGEpdSAr
IFh2ID0gLVMgOyBYdSArIChMK1grdytpIGV0YSl2ID0gMCAtLQogICAgZGVmIF9Mb3Aoc2VsZiwg
Zik6CiAgICAgICAgcmV0dXJuIChucC5mZnQuaWZmdDIoMC41ICogc2VsZi5LMiAqIG5wLmZmdC5m
ZnQyKGYpKQogICAgICAgICAgICAgICAgKyAoc2VsZi5WIC0gc2VsZi5tdSkgKiBmKQoKICAgIGRl
ZiBfWG9wKHNlbGYsIGYpOgogICAgICAgIHJldHVybiBzZWxmLnBzaTAgKiBucC5mZnQuaWZmdDIo
c2VsZi5VayAqIG5wLmZmdC5mZnQyKHNlbGYucHNpMCAqIGYpKQoKICAgIGRlZiBzb2x2ZV9yZXNw
b25zZShzZWxmLCBvbWVnYSwgZXRhLCBzb3VyY2UsIHJ0b2w9M2UtNCwgbWF4aXRlcj0yNTAsCiAg
ICAgICAgICAgICAgICAgICAgICAgcmVzdGFydD0yMDApOgogICAgICAgIGZyb20gc2NpcHkuc3Bh
cnNlLmxpbmFsZyBpbXBvcnQgTGluZWFyT3BlcmF0b3IsIGdtcmVzCiAgICAgICAgTngsIE55ID0g
c2VsZi5OeCwgc2VsZi5OeQogICAgICAgIHN6ID0gTnggKiBOeQoKICAgICAgICBkZWYgbWF0dmVj
KHopOgogICAgICAgICAgICB1ID0gels6c3pdLnJlc2hhcGUoTngsIE55KQogICAgICAgICAgICB2
ID0geltzejpdLnJlc2hhcGUoTngsIE55KQogICAgICAgICAgICBMdSwgTHYgPSBzZWxmLl9Mb3Ao
dSksIHNlbGYuX0xvcCh2KQogICAgICAgICAgICBYdSwgWHYgPSBzZWxmLl9Yb3AodSksIHNlbGYu
X1hvcCh2KQogICAgICAgICAgICByMSA9IEx1ICsgWHUgLSAob21lZ2EgKyAxaiAqIGV0YSkgKiB1
ICsgWHYKICAgICAgICAgICAgcjIgPSBYdSArIEx2ICsgWHYgKyAob21lZ2EgKyAxaiAqIGV0YSkg
KiB2CiAgICAgICAgICAgIHJldHVybiBucC5jb25jYXRlbmF0ZShbcjEucmF2ZWwoKSwgcjIucmF2
ZWwoKV0pCgogICAgICAgIEEgPSBMaW5lYXJPcGVyYXRvcigoMiAqIHN6LCAyICogc3opLCBtYXR2
ZWM9bWF0dmVjLCBkdHlwZT1jb21wbGV4KQogICAgICAgIGIgPSBucC5jb25jYXRlbmF0ZShbKC1z
b3VyY2UpLnJhdmVsKCksCiAgICAgICAgICAgICAgICAgICAgICAgICAgICBucC56ZXJvcyhzeiwg
Y29tcGxleCldKQogICAgICAgIHosIGluZm8gPSBnbXJlcyhBLCBiLCBydG9sPXJ0b2wsIHJlc3Rh
cnQ9cmVzdGFydCwgbWF4aXRlcj1tYXhpdGVyKQogICAgICAgIHJlc2lkID0gZmxvYXQobnAubGlu
YWxnLm5vcm0obWF0dmVjKHopIC0gYikgLyBucC5saW5hbGcubm9ybShiKSkKICAgICAgICB1ID0g
els6c3pdLnJlc2hhcGUoTngsIE55KQogICAgICAgIHYgPSB6W3N6Ol0ucmVzaGFwZShOeCwgTnkp
CiAgICAgICAgZHJobyA9IHNlbGYucHNpMCAqICh1ICsgdikKICAgICAgICByZXR1cm4gZHJobywg
cmVzaWQKCiAgICBkZWYgZ2F1c3NpYW5fc291cmNlKHNlbGYsIHNpZ21hPTAuNSwgcm93PTApOgog
ICAgICAgICIiIklzb3Ryb3BpYyBHYXVzc2lhbiBkZW5zaXR5IHNvdXJjZSBtYXNrZWQgYnkgcHNp
MCwgY2VudHJlZCBvbiB0aGUKICAgICAgICByb3ctYHJvd2AgbGF0dGljZSBzaXRlLiIiIgogICAg
ICAgIHgwID0gKHJvdyAlIDIpICogc2VsZi5hIC8gMi4wCiAgICAgICAgeTAgPSByb3cgKiBzZWxm
LmQKICAgICAgICBkeHYgPSBzZWxmLlggLSB4MAogICAgICAgIGR4diAtPSBzZWxmLkx4ICogbnAu
cm91bmQoZHh2IC8gc2VsZi5MeCkKICAgICAgICBkeXYgPSBzZWxmLlkgLSB5MAogICAgICAgIGR5
diAtPSBzZWxmLkx5ICogbnAucm91bmQoZHl2IC8gc2VsZi5MeSkKICAgICAgICByZXR1cm4gc2Vs
Zi5wc2kwICogbnAuZXhwKC0oZHh2KioyICsgZHl2KioyKSAvICgyICogc2lnbWEqKjIpKQoKICAg
IGRlZiByb3dfZW52ZWxvcGUoc2VsZiwgZHJobyk6CiAgICAgICAgIiIiUGVyLXJvdyBlbnZlbG9w
ZTogbWF4IHxkcmhvfCBvdmVyIGVhY2ggcm93IHdpbmRvdyB8eS15X2p8IDw9IGQvMgogICAgICAg
ICh3cmFwLWF3YXJlKS4iIiIKICAgICAgICBhbXAgPSBucC56ZXJvcyhzZWxmLm5yb3dzKQogICAg
ICAgIGZvciBqaiBpbiByYW5nZShzZWxmLm5yb3dzKToKICAgICAgICAgICAgeTAgPSBqaiAqIHNl
bGYuZAogICAgICAgICAgICBkeXYgPSBzZWxmLlkgLSB5MAogICAgICAgICAgICBkeXYgLT0gc2Vs
Zi5MeSAqIG5wLnJvdW5kKGR5diAvIHNlbGYuTHkpCiAgICAgICAgICAgIG1hc2sgPSBucC5hYnMo
ZHl2KSA8PSBzZWxmLmQgLyAyLjAKICAgICAgICAgICAgYW1wW2pqXSA9IGZsb2F0KG5wLmFicyhk
cmhvW21hc2tdKS5tYXgoKSkKICAgICAgICByZXR1cm4gYW1wCgoKIyAtLS0tLS0tLS0tLS0tLS0t
LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tIGZpdHRpbmcg
LS0tLQpkZWYgZW52ZWxvcGVfZml0KGFtcCwgZF9yb3cpOgogICAgIiIiRGVjb2RlIG9mIHRoZSBv
cmlnaW5hbCBwaGFzZTRfZml0cy5qc29uIGNvbnZlbnRpb25zOgogICAgICByb3dzX3JlbCAgICAg
ICAgPSBhbXAgLyBhbXBbMF0sIHJlcG9ydGVkIHJvd3MgMC4uMTIKICAgICAgd3JhcF9taW5fcm93
ICAgID0gYXJnbWluIG92ZXIgcm93cyAxLi5ucm93cy0xCiAgICAgIGNsZWFuX3JhdGlvcyAgICA9
IGFtcFtpKzFdL2FtcFtpXSBmb3IgaSA9IDEgLi4gbWF4KHdyYXBfbWluX3Jvdy0yLCAyKQogICAg
ICB0X3JhdGlvX21lZGlhbiAgPSBtZWRpYW4oY2xlYW5fcmF0aW9zKTsgc3ByZWFkID0gcG9wdWxh
dGlvbiBzdGQKICAgICAga2FwcGFfZml0ICAgICAgID0gLXNsb3BlIG9mIGxuKGFtcCkgdnMgeSBv
dmVyIHJvd3MgMS4ubWF4KHdyYXBfbWluX3Jvdy0xLCA2KQogICAgICB0X2ZpdCAgICAgICAgICAg
PSBleHAoLWthcHBhKmRfcm93KTsgZml0X3IyID0gbGluZWFyLWZpdCByXjIuIiIiCiAgICBucm93
cyA9IGxlbihhbXApCiAgICByZWwgPSBhbXAgLyBhbXBbMF0KICAgIHdtciA9IGludChucC5hcmdt
aW4ocmVsWzE6bnJvd3NdKSArIDEpCiAgICBpbWF4ID0gbWF4KHdtciAtIDIsIDIpCiAgICByYXRp
b3MgPSBbZmxvYXQocmVsW2kgKyAxXSAvIHJlbFtpXSkgZm9yIGkgaW4gcmFuZ2UoMSwgaW1heCAr
IDEpXQogICAgbWVkID0gZmxvYXQobnAubWVkaWFuKHJhdGlvcykpCiAgICBzcHJlYWQgPSBmbG9h
dChucC5zdGQocmF0aW9zKSkKICAgIGZpdF9oaSA9IG1heCh3bXIgLSAxLCA2KQogICAgcm93cyA9
IG5wLmFyYW5nZSgxLCBmaXRfaGkgKyAxKQogICAgeXkgPSByb3dzICogZF9yb3cKICAgIGxuID0g
bnAubG9nKHJlbFtyb3dzXSkKICAgIEEgPSBucC52c3RhY2soW3l5LCBucC5vbmVzX2xpa2UoeXkp
XSkuVAogICAgY29lZiwgKl8gPSBucC5saW5hbGcubHN0c3EoQSwgbG4sIHJjb25kPU5vbmUpCiAg
ICBwcmVkID0gQSBAIGNvZWYKICAgIHNzX3JlcyA9IGZsb2F0KG5wLnN1bSgobG4gLSBwcmVkKSAq
KiAyKSkKICAgIHNzX3RvdCA9IGZsb2F0KG5wLnN1bSgobG4gLSBsbi5tZWFuKCkpICoqIDIpKQog
ICAgcjIgPSAxLjAgLSBzc19yZXMgLyBzc190b3QgaWYgc3NfdG90ID4gMCBlbHNlIDAuMAogICAg
a2FwcGEgPSBmbG9hdCgtY29lZlswXSkKICAgIHJldHVybiBkaWN0KHJvd3NfcmVsPVtyb3VuZChm
bG9hdCh2KSwgNCkgZm9yIHYgaW4gcmVsWzoxM11dLAogICAgICAgICAgICAgICAgd3JhcF9taW5f
cm93PXdtciwKICAgICAgICAgICAgICAgIGNsZWFuX3JhdGlvcz1bcm91bmQociwgNCkgZm9yIHIg
aW4gcmF0aW9zXSwKICAgICAgICAgICAgICAgIHRfcmF0aW9fbWVkaWFuPXJvdW5kKG1lZCwgNCks
CiAgICAgICAgICAgICAgICB0X3JhdGlvX3NwcmVhZD1yb3VuZChzcHJlYWQsIDQpLAogICAgICAg
ICAgICAgICAga2FwcGFfZml0PXJvdW5kKGthcHBhLCA0KSwKICAgICAgICAgICAgICAgIHRfZml0
PXJvdW5kKGZsb2F0KG5wLmV4cCgta2FwcGEgKiBkX3JvdykpLCA0KSwKICAgICAgICAgICAgICAg
IGZpdF9yMj1yb3VuZChyMiwgNSkpCg==
<<<EMBED-END name=gz1_core.py>>>

### EMBED — chat checkpoint Phase 0 — `g_s2c1_phase0_checkpoint.json` (md5 eae2bbd734f5129dd1e51efcbb55dd3d, 4555 B, b64, QUARANTINED)

<<<EMBED-BEGIN name=g_s2c1_phase0_checkpoint.json md5=eae2bbd734f5129dd1e51efcbb55dd3d bytes=4555 enc=b64 quarantine=1>>>
ewogIkFfc3Vic3RyYXRlX2RpYWdub3N0aWMiOiB7CiAgIkxfcHNpMF9yZXNpZHVhbF9yZWwiOiAw
LjEyNjk1NDY4NzY4MzQ2NDgyLAogICJMX3BzaTBfcmVzaWR1YWxfcmVsX292ZXJfbXUiOiAwLjAw
MjI2OTIzNjE4NjM4NDQ1NywKICAiUEhBU0UxX1NUQVRJT05BUklUWV9USFJFU0hPTERfcHJvcG9z
ZWQiOiB7CiAgICJMX3BzaTBfcmVzaWR1YWxfcmVsX21heCI6IDFlLTEwLAogICAiZ29sZHN0b25l
X29tZWdhMl9vZmZzZXRfYWJzX21heCI6IDFlLTA4LAogICAicmF0aW9uYWxlIjogIm9mZnNldCBz
Y2FsZXMgfjE3IHggcmVzaWR1YWw7IGF0IGthPTEuMTdlLTMgKGs9OC4wNGUtMDQpIGFuIGFjb3Vz
dGljIG9tZWdhXjIgfiAoYyBrKV4yIGlzIE8oMWUtNi4uMWUtNSkgZm9yIGMgPSBPKDEuLjMpOyAx
JSBvZiB0aGF0IGlzIDFlLTgiCiAgfSwKICAiYV9zdGFyIjogMS40NTc2LAogICJnb2xkc3RvbmVf
b2Zmc2V0X3Byb2R1Y3RfZm9ybSI6IHsKICAgIm5fYj0yNCI6IHsKICAgICJrYT0wLjAwNSI6IFsK
ICAgICAtMi4wOTcyMjA4MTEyMDAwMjEsCiAgICAgLTIuMDk2MTQ2NjU4NjU2MDE4NywKICAgICAt
MC4wMjQ2MjA1MjM1NTY0NzkwMjQKICAgIF0sCiAgICAia2E9MC4wMjAiOiBbCiAgICAgLTIuMDkx
MjI2NTY4MDE3ODE4LAogICAgIC0yLjA3NDA0MTM0MjY2ODUwOSwKICAgICAtMC4wMjM5MzU4MjA0
NzU3OTk0NzYKICAgIF0sCiAgICAia2E9MC4wODAiOiBbCiAgICAgLTEuOTk1MzI0ODA2MTY5MTM2
OSwKICAgICAtMS43MjA3NDI5MjEyNTA1MDgsCiAgICAgLTAuMDEyNjQ2MjY2MzgwMzY4NzMzCiAg
ICBdCiAgIH0sCiAgICJuX2I9MzIiOiB7CiAgICAia2E9MC4wMDUiOiBbCiAgICAgLTIuMDk3MjIw
ODA5NzI1NDg0LAogICAgIC0yLjA5NjE0NjY1NDQ0Njg0OTcsCiAgICAgLTAuMDI0NjIwNTIyNTc1
ODMwMTcKICAgIF0sCiAgICAia2E9MC4wMjAiOiBbCiAgICAgLTIuMDkxMjI2NTY4MDg4MTAyLAog
ICAgIC0yLjA3NDA0MTMyOTg0MDQ0ODUsCiAgICAgLTAuMDIzOTM1ODE3MTkwNTc2MDc3CiAgICBd
LAogICAgImthPTAuMDgwIjogWwogICAgIC0xLjk5NTMyNDgwMzE3NTg0MjQsCiAgICAgLTEuNzIw
NzQyOTIxMzA4MjIwNiwKICAgICAtMC4wMTI2NDYyNzQ4NjQ0MDUzOTIKICAgIF0KICAgfSwKICAg
Im5fYj00MCI6IHsKICAgICJrYT0wLjAwNSI6IFsKICAgICAtMi4wOTcyMjA4MDI1NTQzMjksCiAg
ICAgLTIuMDk2MTQ2NjgxMDg2MjYyNiwKICAgICAtMC4wMjQ2MjA0OTQyOTQ1MQogICAgXSwKICAg
ICJrYT0wLjAyMCI6IFsKICAgICAtMi4wOTEyMjY1NzAzNTE5OTQzLAogICAgIC0yLjA3NDA0MTMx
NTg2MTc5NDMsCiAgICAgLTAuMDIzOTM1ODYxMjY2OTU4NjM1CiAgICBdLAogICAgImthPTAuMDgw
IjogWwogICAgIC0xLjk5NTMyNDc5ODQ3NzQ5ODksCiAgICAgLTEuNzIwNzQyOTEzNTUyNjM3MywK
ICAgICAtMC4wMTI2NDYyNTcyOTAyNDg2OTQKICAgIF0KICAgfQogIH0sCiAgImhlcm1pdGlhbl9j
bGlwcGVkX2xvd2VzdCI6IHsKICAgImthPTAuMDA1IjogWwogICAgMC4wLAogICAgMC4wLAogICAg
Mi4zNzQ3Mjc2MzM0NTU5MDU3ZS0wNQogICBdLAogICAia2E9MC4wMjAiOiBbCiAgICAwLjAsCiAg
ICAwLjAsCiAgICA2Ljk3NzE4NzgyMzExMjRlLTA2CiAgIF0sCiAgICJrYT0wLjA4MCI6IFsKICAg
IDAuMCwKICAgIDAuMCwKICAgIDAuMAogICBdCiAgfSwKICAia2VybmVsX2dyaWRfdnNfYW5hbHl0
aWNfbWF4X2Fic19kaWZmIjogMC4wLAogICJtdSI6IDU1Ljk0NiwKICAib2Zmc2V0X3Blcl91bml0
X3Jlc2lkdWFsIjogMTYuNTE5NDQzNjUzNDI3NTA1LAogICJwc2kwX3NwZWN0cmFsX3dlaWdodF9i
ZXlvbmRfbTE2IjogOS40MDQxNzYwMDQyODA5MzNlLTMxLAogICJzdWJzdHJhdGUiOiAiZ3oxX3Jl
YnVpbGQgcHNpMF9wb2xpc2hlZF9uNjQgbWQ1IDZlODhjYmQ1YTJjMWZjOGI4YTJlNjRkOGQwY2Ew
MTIzIiwKICAid2FyZF9yZXNpZHVhbF90cmFuc2xhdGlvbl9tb2RlX3JlbCI6IDAuMTg1NjE4NDY2
NjM2MjE5NDUKIH0sCiAiQl9hbmFseXRpY19jb250cm9sIjogewogICJGLUNUUkwtTCI6IHsKICAg
IkdhbW1hLUsiOiB7CiAgICAiYTJfYW5hbHl0aWMiOiAtMC4wMzgxOTQ0NDQ0NDQ0NDQ0NSwKICAg
ICJhMl9maXQiOiAtMC4wMzgxOTQ0MzY3MDk0MjQ4OSwKICAgICJhNF9hbmFseXRpYyI6IDAuMDAw
NTE0ODA1MTY5NzUzMDg2NCwKICAgICJhNF9maXQiOiAwLjAwMDUxNDUwNjAxNDQ0ODk5MDgsCiAg
ICAiYWJzX2Vycl9hMiI6IDcuNzM1MDE5NTU1NDIxNTUyZS0wOSwKICAgICJjX2FuYWx5dGljIjog
MS4wNjA2NjAxNzE3Nzk4MjEyLAogICAgImNfZml0IjogMS4wNjA2NjAxNzE3MzYyNTQ1LAogICAg
ImNpX2EyX3dpbmRvdyI6IDUuMTQ4NTM3OTY2MDk4NzA5NmUtMDgsCiAgICAia25vd25fbm9uemVy
byI6IHRydWUsCiAgICAicGFzcyI6IHRydWUKICAgfSwKICAgIkdhbW1hLU0iOiB7CiAgICAiYTJf
YW5hbHl0aWMiOiAtMC4wMzEyNTAwMDAwMDAwMDAwMSwKICAgICJhMl9maXQiOiAtMC4wMzEyNDk5
OTY4NTc0MjUyNzUsCiAgICAiYTRfYW5hbHl0aWMiOiAwLjAwMDI5Mjk2ODc1MDAwMDAwMDA0LAog
ICAgImE0X2ZpdCI6IDAuMDAwMjkyODE3MjQ0NzY5OTExNSwKICAgICJhYnNfZXJyX2EyIjogMy4x
NDI1NzQ3MzE2OTA0Mzk1ZS0wOSwKICAgICJjX2FuYWx5dGljIjogMS4wNjA2NjAxNzE3Nzk4MjE0
LAogICAgImNfZml0IjogMS4wNjA2NjAxNzE3NzAzNjksCiAgICAiY2lfYTJfd2luZG93IjogOS44
NTQ5MTMyNTM1MDQxODNlLTA5LAogICAgImtub3duX25vbnplcm8iOiB0cnVlLAogICAgInBhc3Mi
OiB0cnVlCiAgIH0KICB9LAogICJUX2JyYW5jaF9kaWFnbm9zdGljX0NPTlRST0xfTk9UX1ZFUkRJ
Q1QiOiB7CiAgICJHYW1tYS1LIjogewogICAgImEyX2FuYWx5dGljIjogLTAuMDEwNDE2NjY2NjY2
NjY2NjY2LAogICAgImEyX2ZpdCI6IC0wLjAxMDQxNjY2NDU3MDY1NjIwNCwKICAgICJhNF9hbmFs
eXRpYyI6IDMuMjU1MjA4MzMzMzMzMzNlLTA1LAogICAgImE0X2ZpdCI6IDMuMjUyNzU1MDMyNjYx
NjM5ZS0wNSwKICAgICJhYnNfZXJyX2EyIjogMi4wOTYwMTA0NjI0MTU2OTgzZS0wOSwKICAgICJj
X2FuYWx5dGljIjogMC42MTIzNzI0MzU2OTU3OTQ1LAogICAgImNfZml0IjogMC42MTIzNzI0MzU2
ODAwMDQ3LAogICAgImNpX2EyX3dpbmRvdyI6IDMuNDg1MjU4NDI3ODY2ODk5N2UtMDgKICAgfSwK
ICAgIkdhbW1hLU0iOiB7CiAgICAiYTJfYW5hbHl0aWMiOiAtMC4wMzEyNTAwMDAwMDAwMDAwMSwK
ICAgICJhMl9maXQiOiAtMC4wMzEyNDk5OTY4NTc0MjgzMDgsCiAgICAiYTRfYW5hbHl0aWMiOiAw
LjAwMDI5Mjk2ODc1MDAwMDAwMDA0LAogICAgImE0X2ZpdCI6IDAuMDAwMjkyODE3MjQ0ODMxMzAx
MSwKICAgICJhYnNfZXJyX2EyIjogMy4xNDI1NzE2OTkzOTM4MDM1ZS0wOSwKICAgICJjX2FuYWx5
dGljIjogMC42MTIzNzI0MzU2OTU3OTQ1LAogICAgImNfZml0IjogMC42MTIzNzI0MzU2OTAzMzcy
LAogICAgImNpX2EyX3dpbmRvdyI6IDkuODU0NjA5NzM5MzQ1OTMyZS0wOQogICB9CiAgfSwKICAi
Zml0dGVyX2EyX2JpYXNfbWF4X2FicyI6IDcuNzM1MDE5NTU1NDIxNTUyZS0wOSwKICAicHJvamVj
dG9yX21pcnJvcl9saW5lX2V4YWN0IjogdHJ1ZQogfSwKICJDX0ZfQ1RSTF9JTkoiOiB7CiAgImEy
X2luamVjdGVkIjogOS45OTk5OTk5OTk5OTk5OTllLTA2LAogICJhMl9yZWNvdmVyZWRfbWVhbiI6
IDEuMDAzNTk3NzgyODgyOTY1MmUtMDUsCiAgImEyX3JlY292ZXJlZF9zZCI6IDUuMzQzNDcwNjQw
NTUzMTZlLTA3LAogICJjaTk1IjogWwogICA5LjAwMzgzMzM4ODA4NzIzOWUtMDYsCiAgIDEuMTAx
NzI5NzUyOTcyNjMzM2UtMDUKICBdLAogICJub2lzZV9hYnMiOiAxZS0wOCwKICAicGFzcyI6IHRy
dWUKIH0sCiAiUEhBU0UxX0FVVEhPUklaRUQiOiBmYWxzZSwKICJnYXRlIjogIkctUzJDMSIsCiAi
bGFkZGVyX2thIjogWwogIDAuMywKICAwLjE1LAogIDAuMDc1LAogIDAuMDM3NSwKICAwLjAxODc1
LAogIDAuMDA5Mzc1LAogIDAuMDA0Njg3NSwKICAwLjAwMjM0Mzc1LAogIDAuMDAxMTcxODc1CiBd
LAogImxlZyI6ICJjaGF0IiwKICJsb2NrX3JlY29yZF9tZDUiOiAiZjJmNGQ1MDAyOWZiNWJlMzEy
MmE4ODVjNDhhN2UwNGYiLAogInBoYXNlIjogMCwKICJwcmVyZWdfbWQ1IjogIjJlYThlYzEzZmZh
M2MzMjg5OGNjMjRhM2JlNjA1YzY0IiwKICJyZWFkaW5lc3MiOiB7CiAgImhhcm5lc3NfcHJvamVj
dG9yX2ZpdHRlciI6ICJSRUFEWSIsCiAgInN1YnN0cmF0ZV9nejFfZm9yX2Fjb3VzdGljX2xhZGRl
ciI6ICJOT1QgUkVBRFkgXHUyMDE0IHN0YXRpb25hcml0eS9Hb2xkc3RvbmUgb2Zmc2V0IChzZWUg
QSk7IFBoYXNlIDEgcHJlcmVxdWlzaXRlOiByZS1jcnlzdGFsbGl6ZSBhdCBnZW04IChFLTMpIHRv
IHRoZSBwcm9wb3NlZCB0aHJlc2hvbGQgYW5kIHZlcmlmeSBXQVJELUdhbW1hIGJlZm9yZSBhbnkg
bGFkZGVyIgogfSwKICJzdGF0dXMiOiAiQ09OVFJPTC1OT1QtVkVSRElDVCIsCiAidDFfbWQ1Ijog
IjhjZDg5YjlhODI3MDRhY2NkODlmN2ZmNmY1ZTIyMGI0IiwKICJ0YXUiOiAxZS0wNgp9Cg==
<<<EMBED-END name=g_s2c1_phase0_checkpoint.json>>>

### EMBED — chat checkpoint Phase 1 halt — `g_s2c1_phase1_checkpoint.json` (md5 eeedcfa594a24915fa9c10c6abbd0a4e, 2477 B, b64, QUARANTINED)

<<<EMBED-BEGIN name=g_s2c1_phase1_checkpoint.json md5=eeedcfa594a24915fa9c10c6abbd0a4e bytes=2477 enc=b64 quarantine=1>>>
ewogIlBIQVNFMV9BVVRIT1JJWkVEIjogdHJ1ZSwKICJoYWx0IjogIldBUkQtR0FNTUEgRkFJTEVE
IGFzIGxpdGVyYWxseSBzcGVjaWZpZWQgKHByb2R1Y3QtZm9ybSBlaWcsIG5fYj0zMjogMy40OGUt
OCA+IDFlLTgpOyBzZWUgc3RlcDJfd2FyZC5kaWFnbm9zaXMiLAogImxlZyI6ICJjaGF0IiwKICJs
b2NrX3JlY29yZF9tZDUiOiAiZjJmNGQ1MDAyOWZiNWJlMzEyMmE4ODVjNDhhN2UwNGYiLAogInBo
YXNlIjogMSwKICJwcmVyZWdfbWQ1IjogIjJlYThlYzEzZmZhM2MzMjg5OGNjMjRhM2JlNjA1YzY0
IiwKICJzdGVwMSI6IHsKICAiYnJhZ2dfcGVha19yYXRpb19yaG8iOiAwLjQ2NTAwNTE2MTUyMjI0
NDQ3LAogICJlbmVyZ3lfcGVyX2FyZWFfaW50IjogMjQuOTU2NDkxNDgxNzAxMTEsCiAgImVuZXJn
eV9wZXJfYXJlYV9raW4iOiAzLjMxMTM4NTIxNTc5MzE2OTYsCiAgImdyaWRfbiI6IDY0LAogICJt
ZWFuX3JobyI6IDAuOTk5OTg4MTI5MjQ3NDQ3MiwKICAicGFzcyI6IHRydWUsCiAgInBzaTBfbWQ1
IjogImIyN2ZhMDA0OTVlZjY4NmIwMTg0ZWEyOWM0NTViNGRiIiwKICAicHNpMF9zcGVjdHJhbF93
ZWlnaHRfYmV5b25kX20yNCI6IDIuMTI0MjkzOTkwNDA3ODYxN2UtMzIsCiAgInJlc2lkdWFsX2Fm
dGVyX05LIjogMS45NTUwMjU1Nzg0MjYyOTM0ZS0xMiwKICAicmVzaWR1YWxfaW1hZ2luYXJ5X3Rp
bWUiOiAxLjk1NTAyNTU3ODQyNjI5MzRlLTEyLAogICJ0aHJlc2hvbGQiOiAxZS0xMAogfSwKICJz
dGVwMl93YXJkIjogewogICJkaWFnbm9zaXMiOiB7CiAgICJoZXJtaXRpYW5fZm9ybV9laWdoX2dv
bGRzdG9uZV9hYnNfdzJfbWF4X2J5X25iIjogewogICAgIjI0IjogNi41NGUtMTAsCiAgICAiMzIi
OiAzLjExZS0wOSwKICAgICI0MCI6IDEuODFlLTA4CiAgIH0sCiAgICJraW5ldGljX2N1dG9mZl9t
YXhfYnlfbmIiOiB7CiAgICAiMjQiOiA0OTU1LAogICAgIjMyIjogODk1MiwKICAgICI0MCI6IDE0
MTM0CiAgIH0sCiAgICJsYW1iZGFfbWluX0xfR2FtbWEiOiAxLjYyZS0xNCwKICAgInByb2R1Y3Rf
Zm9ybV9laWdfZ29sZHN0b25lX2Fic193Ml9tYXhfYnlfbmIiOiB7CiAgICAiMjQiOiAyLjEyZS0w
OSwKICAgICIzMiI6IDMuNDhlLTA4LAogICAgIjQwIjogMy42MmUtMDgKICAgfSwKICAgInJlYWRp
bmciOiAiZGVuc2UtZWlnZW5zb2x2ZXIgR29sZHN0b25lIHZhbHVlcyBzY2FsZSB3aXRoIChraW5l
dGljIGN1dG9mZileMiB4IG1hY2hpbmUgZXBzaWxvbiBcdTIwMTQgYSBkb3VibGUtcHJlY2lzaW9u
IGZsb29yLCBub3QgYSBXYXJkIHZpb2xhdGlvbjsgdGhlIFdhcmQgaWRlbnRpdHkgaG9sZHMgYXQg
dGhlIHN0YXRpb25hcml0eS1yZXNpZHVhbCBsZXZlbCAofjFlLTExKTsgdGhlIGxpdGVyYWwgfHcy
fDw9MWUtOCBjcml0ZXJpb24gaXMgbWV0IGJ5IHRoZSBwcm9kdWN0IGZvcm0gYXQgbl9iPTI0IGFu
ZCBieSB0aGUgSGVybWl0aWFuIGZvcm0gYXQgbl9iPD0zMiwgYW5kIGlzIG5vdCBhY2hpZXZhYmxl
IGJ5IGFueSBkZW5zZSBkb3VibGUtcHJlY2lzaW9uIHNvbHZlIGF0IG5fYj49MzIgKHByb2R1Y3Qp
IC8gNDAgKEhlcm1pdGlhbikgaXJyZXNwZWN0aXZlIG9mIHRoZSBzdGF0ZSIsCiAgICJzdGF0dXMi
OiAiSEFMVEVEIHBlciBkaXJlY3RpdmUgaXRlbSAyIFx1MjAxNCBsYWRkZXIgTk9UIHJ1bjsgYW1l
bmRtZW50IEEtMSBwcm9wb3NlZCBmb3IgYXV0aG9yIGF1dGhvcml6YXRpb24iLAogICAid2FyZF9y
ZXNpZHVhbF9hbmFseXRpY190cmFuc2xhdGlvbl9tb2Rlc19uYjI0IjogewogICAgImR4IjogMi4y
OGUtMTIsCiAgICAiZHkiOiAzLjFlLTEyCiAgIH0sCiAgICJ3YXJkX3Jlc2lkdWFsX2FuYWx5dGlj
X3RyYW5zbGF0aW9uX21vZGVzX25iMzIiOiB7CiAgICAiZHgiOiA2LjU4ZS0xMiwKICAgICJkeSI6
IDEuMTNlLTExCiAgIH0KICB9LAogICJsYW1iZGFfbWluX0xfR2FtbWEiOiAxLjYxOTQwMTk2ODIx
MDk0NzhlLTE0LAogICJwYXNzIjogZmFsc2UsCiAgInByb2R1Y3RfZm9ybV93Ml9HYW1tYV8zbG93
ZXN0IjogWwogICBbCiAgICAtOC43NDU4MjQzOTYwODc4NzRlLTA5LAogICAgLTEuMzk1MDE5OTk2
NDg3NzM5ZS0wOQogICBdLAogICBbCiAgICAtMy44OTUwNjUwMjQ2Njc5MTllLTA5LAogICAgLTIu
MTEwOTEwNTA5MDQ0OTU0M2UtMDkKICAgXSwKICAgWwogICAgMy40NzU2NDM1MDM5NTY0NjRlLTA4
LAogICAgNS43Nzg2MzE4OTM4NjQxODRlLTEwCiAgIF0KICBdLAogICJwcm9kdWN0X2Zvcm1fdzJf
a2EwLjAwNV8zbG93ZXN0IjogWwogICBbCiAgICAwLjAwMDE2NDMzNzYzMDc0MTEzOTY1LAogICAg
LTEuODM4MTE4MjAyNDY1NTYxZS0wOAogICBdLAogICBbCiAgICAwLjAwMDI5ODYzNjIxOTQzMjA5
NzksCiAgICAtMS4xMjE2NjczNjI2MTE1OTExZS0wOQogICBdLAogICBbCiAgICAwLjAwMTA5Nzg5
ODIyNjAxMTg1MzUsCiAgICAxLjc2MzA2MzcwODk4MDQ1MzJlLTA4CiAgIF0KICBdLAogICJ0aHJl
c2hvbGRfYWJzX3cyIjogMWUtMDgKIH0KfQo=
<<<EMBED-END name=g_s2c1_phase1_checkpoint.json>>>

### EMBED — chat checkpoint Phase 1 ladder — `g_s2c1_phase1_ladder_checkpoint.json` (md5 5ee152fc14ac55e72094fc660aff7a4a, 43647 B, b64, QUARANTINED)

<<<EMBED-BEGIN name=g_s2c1_phase1_ladder_checkpoint.json md5=5ee152fc14ac55e72094fc660aff7a4a bytes=43647 enc=b64 quarantine=1>>>
ewogIkZfQ09OViI6IHsKICAiYTJfVF9HS19hYnNfMjR2MzIiOiA0LjkxMTIyOTQ5MzgzNzI4ZS0w
NSwKICAiYTJfVF9HS19hYnNfMzJ2NDAiOiAwLjAwMDkxMDQxMjc5ODk3MDE4OTcsCiAgImEyX1Rf
R01fYWJzXzI0djMyIjogMC4wMDA1OTMyOTM4ODE0NTQ1NzQyLAogICJhMl9UX0dNX2Fic18zMnY0
MCI6IDAuMDAwNjUyODA2NTE5MDYwNjA1OCwKICAiYTRfVF9HS19hYnNfMzJ2NDAiOiAwLjAwODYy
ODk3MzU5NTEzNzcxLAogICJhNF9UX0dNX2Fic18zMnY0MCI6IDAuMDA2MTczMjg1MzM3ODA5MzAz
LAogICJjX0wxX0dLX3JlbF8yNHYzMiI6IDIuMTM2MjA4NzkwMDgyMjVlLTA2LAogICJjX0wxX0dL
X3JlbF8zMnY0MCI6IDMuNjc4Nzg4Mzk3MTMyMzE1NGUtMDYsCiAgImNfTDFfR01fcmVsXzI0djMy
IjogOC45MDk4NzM0MTU3MzAwMTllLTA3LAogICJjX0wxX0dNX3JlbF8zMnY0MCI6IDYuNjEyODYz
OTIzMTE2NjYzZS0wOSwKICAiY19QSF9HS19yZWxfMjR2MzIiOiA0LjIzNDg5MTA0MjI4NzM1ODdl
LTA3LAogICJjX1BIX0dLX3JlbF8zMnY0MCI6IDQuODE1OTgyODAwNDQzNDg2ZS0wNiwKICAiY19Q
SF9HTV9yZWxfMjR2MzIiOiA1LjQ4Mjg3NzY4Mjk4Mjk0NWUtMDcsCiAgImNfUEhfR01fcmVsXzMy
djQwIjogMy44ODk4NDAzNjA5MjY2NTVlLTA4LAogICJjX1RfR0tfcmVsXzI0djMyIjogNy4wNDQ5
NTQ5MTI3NzE1NzNlLTA3LAogICJjX1RfR0tfcmVsXzMydjQwIjogMS4yMjc2OTA3NjczMzU4NjVl
LTA1LAogICJjX1RfR01fcmVsXzI0djMyIjogOC4yMDg3NjE3NzY5ODQzNzVlLTA2LAogICJjX1Rf
R01fcmVsXzMydjQwIjogOC45MTQzNzY4MTkwNDY5NDNlLTA2CiB9LAogIkZfQ09OVl9wYXNzIjog
ZmFsc2UsCiAiRl9ESVNQX2NoYXRsZWciOiB7CiAgIkdLIjogewogICAiYTIiOiAtMC4wMTI4MjM4
NDg1NzIxODk2MDQsCiAgICJhMl9yZXNvbHZlZF9ub256ZXJvIjogdHJ1ZSwKICAgImEyX3plcm9f
YXRfdGF1IjogZmFsc2UsCiAgICJhNCI6IC0wLjAwMjY4MjM0OTUxMzE4ODk0NywKICAgImE0X3Jl
c29sdmVkX25vbnplcm8iOiBmYWxzZSwKICAgImE0X3plcm9fYXRfdGF1IjogdHJ1ZSwKICAgImNp
X2EyX3RvdGFsIjogMC4wMDY3NTQ5MDk4ODY0MjAxNTYsCiAgICJjaV9hNF90b3RhbCI6IDEuMjg3
NzA3NDM5ODg4NTMxCiAgfSwKICAiR00iOiB7CiAgICJhMiI6IC0wLjAxOTM4Nzc5OTA3ODQxNjI5
NSwKICAgImEyX3Jlc29sdmVkX25vbnplcm8iOiB0cnVlLAogICAiYTJfemVyb19hdF90YXUiOiBm
YWxzZSwKICAgImE0IjogLTAuMDEzNDA1ODYyMTQ3ODQxNzYyLAogICAiYTRfcmVzb2x2ZWRfbm9u
emVybyI6IGZhbHNlLAogICAiYTRfemVyb19hdF90YXUiOiB0cnVlLAogICAiY2lfYTJfdG90YWwi
OiAwLjAwNDM2MDM3NzE1NzIxMzUzOSwKICAgImNpX2E0X3RvdGFsIjogMC41Mjc5NTI2MjE3MjIx
NDkxCiAgfQogfSwKICJGX0lTT19jVF9zcGxpdCI6IDEuMzMzODk0Nzk1NDYzMzA4NWUtMDUsCiAi
Rl9JU09fcGFzcyI6IHRydWUsCiAiRl9NSVhfbWluX28yX1QiOiB7CiAgIkdLIjogMC45OTk5OTk5
OTM2OTg4Njk2LAogICJHTSI6IDAuOTk5OTk5OTc3NTgwOTU1NgogfSwKICJGX01JWF9wYXNzIjog
dHJ1ZSwKICJQSEFTRTFfQVVUSE9SSVpFRCI6IHRydWUsCiAiUl9UX2ZyYW1ld29ya19sYWJlbF9u
YjQwIjogewogICJHSyI6IDAuNTIxNDc4ODQwNjMwMTM2NCwKICAiR00iOiAwLjUyMTQ2OTI5OTU5
NjM0ODIKIH0sCiAiYTJfcmVsYXRpdmVfY29udmVyZ2VuY2VfYW5kX3dlaWdodGVkIjogewogICJH
SyI6IHsKICAgImEyX2Zsb29yX3dlaWdodGVkX25iNDAiOiAtMC4wMTI4MzUxNDUzMjg5NjMyODUs
CiAgICJhMl9yZWxfMjR2MzIiOiAwLjAwNDEyMjQyOTE1MjUzNDk3OCwKICAgImEyX3JlbF8zMnY0
MCI6IDAuMDcwOTkzNzI2NTU5MTY2NzUsCiAgICJhMndfcmVsXzI0djMyIjogMC4wMDMyNTU1MzE5
Nzc1MjgzNTYsCiAgICJhMndfcmVsXzMydjQwIjogMC4wNTM2MzI1MDQ4NzQ1Nzg0MTQsCiAgICJh
NF9mbG9vcl93ZWlnaHRlZF9uYjQwIjogLTAuMDAyNTU2MTE1NTUyOTYwMDAyMywKICAgInNpZ25f
c3RhYmxlX2FsbF9uYiI6IHRydWUKICB9LAogICJHTSI6IHsKICAgImEyX2Zsb29yX3dlaWdodGVk
X25iNDAiOiAtMC4wMTk1NDk2ODcyOTcwMzcxMiwKICAgImEyX3JlbF8yNHYzMiI6IDAuMDI5NjA0
NTg4NDcyNTc5MzcsCiAgICJhMl9yZWxfMzJ2NDAiOiAwLjAzMzY3MDk5NjcxMzk3NzIyNiwKICAg
ImEyd19yZWxfMjR2MzIiOiAwLjAyMjk4ODk0OTk4NjM0Mjk0LAogICAiYTJ3X3JlbF8zMnY0MCI6
IDAuMDI1NTYyNDQ0MzUxNjY4NSwKICAgImE0X2Zsb29yX3dlaWdodGVkX25iNDAiOiAtMC4wMTE1
ODg3NjYwNzQwMzcxMjQsCiAgICJzaWduX3N0YWJsZV9hbGxfbmIiOiB0cnVlCiAgfQogfSwKICJh
ZGRlbmR1bV9BMV9tZDUiOiAiOGJmNTFiZDA1YzY5MWYzZjAzZDc5NmIyMzFjZGQyNjIiLAogImFy
bV9pbmRpY2F0aW9uX2NoYXRsZWciOiB7CiAgIkdLIjogIkE1IElOU1RSVU1FTlQtTElNSVRFRCAo
Ri1DT05WIC8gbGFtYmRhX21pbiBmbG9vcikiLAogICJHTSI6ICJBNSBJTlNUUlVNRU5ULUxJTUlU
RUQgKEYtQ09OViAvIGxhbWJkYV9taW4gZmxvb3IpIgogfSwKICJnYXRlIjogIkctUzJDMSIsCiAi
bGFtYmRhX21pbl9mbG9vcl92aW9sYXRpb25zX2luX2xhZGRlciI6IFtdLAogImxlZyI6ICJjaGF0
IiwKICJsb2NrX3JlY29yZF9tZDUiOiAiZjJmNGQ1MDAyOWZiNWJlMzEyMmE4ODVjNDhhN2UwNGYi
LAogInBoYXNlIjogIjEtbGFkZGVyIiwKICJwaGFzZTBfbWQ1IjogImVhZTJiYmQ3MzRmNTEyOWRk
MWU1MWVmY2JiNTVkZDNkIiwKICJwaGFzZTFfaGFsdF9jaGVja3BvaW50X21kNSI6ICJlZWVkY2Zh
NTk0YTI0OTE1ZmE5YzEwYzZhYmJkMGE0ZSIsCiAicHJlcmVnX21kNSI6ICIyZWE4ZWMxM2ZmYTNj
MzI4OThjYzI0YTNiZTYwNWM2NCIsCiAicmVnaXN0ZXJlZF9leHBlY3RhdGlvbiI6ICJESVNQRVJT
SVZFIChFZGRpbmd0b24gdHJhcCA0KSIsCiAic3RhZ2VfZmlsZV9tZDUiOiB7CiAgIm5iMjQiOiAi
ZTQ5NzUwNTBlYWMzMDE2NjRlYTg5YzI5MDMwYTdjYjAiLAogICJuYjMyIjogIjNiZmRiNDhlZjVh
Y2U5Yzc1MGRjMWExMzRiYTMyMWFkIiwKICAibmI0MEdLIjogIjJiMDM3ODM2MDUzNWQwNjUzODhi
N2Y4MGFjNjFmMDhiIiwKICAibmI0MEdNIjogIjY3OTQ2ZDk1YjI4ZDYxMzcwZjMyMmE2MTRhZjNi
YzFjIgogfSwKICJzdGVwMV9iYW5rZWRfc3RhdGUiOiB7CiAgIm1lYW5fcmhvIjogMC45OTk5ODgx
MjkyNDc0NDcyLAogICJwc2kwX21kNSI6ICJiMjdmYTAwNDk1ZWY2ODZiMDE4NGVhMjljNDU1YjRk
YiIsCiAgInJlc2lkdWFsX3JldmVyaWZpZWQiOiAxLjk1NTAyNTU3ODQyNjI5MzRlLTEyLAogICJz
b3VyY2UiOiAiUGhhc2UtMSBpdGVtIDEgKGhhbHQgcmVwb3J0IGIwZTY3OTBjKSIKIH0sCiAic3Rl
cDJfd2FyZF9nYW1tYV9BMSI6IHsKICAiQTFfdGhyZXNob2xkX2FuYWx5dGljIjogMWUtMDksCiAg
IkExX3RocmVzaG9sZF9oZXJtaXRpYW5fdzIiOiAxZS0wOCwKICAiYnlfbmIiOiB7CiAgICIyNCI6
IHsKICAgICJhbmFseXRpY193YXJkX3Jlc2lkdWFsIjogewogICAgICJkeCI6IDIuMjgxNzkyMDU3
NDA2OTgxNmUtMTIsCiAgICAgImR5IjogMy4xMDAyMTA3NzgwNDY3MDFlLTEyCiAgICB9LAogICAg
Imhlcm1pdGlhbl9nb2xkc3RvbmVfYWJzX3cyX21heCI6IDEuMjIyNTg5NTQxNjc2MzQwNWUtMDks
CiAgICAiaGVybWl0aWFuX3cyXzRsb3dlc3QiOiBbCiAgICAgLTcuMjU2MzcxMDExNTU1MjEyZS0x
MCwKICAgICAxLjkzNDE3MTQ1Nzg1NTM5NDZlLTExLAogICAgIDEuMjIyNTg5NTQxNjc2MzQwNWUt
MDksCiAgICAgNzEuMjgyOTUwNDAxNTYyNDkKICAgIF0sCiAgICAibGFtYmRhX21pbl9MX0dhbW1h
IjogMS42MjYyNjU0MTc5ODM2NTY3ZS0xNCwKICAgICJwYXNzX2EiOiB0cnVlLAogICAgInBhc3Nf
YiI6IHRydWUsCiAgICAicHJvZHVjdF9mb3JtX2Fic193Ml9tYXhfeGNoZWNrIjogMi4xMjQ4NzI5
ODQwMzY1NDYyZS0wOQogICB9LAogICAiMzIiOiB7CiAgICAiYW5hbHl0aWNfd2FyZF9yZXNpZHVh
bCI6IHsKICAgICAiZHgiOiA2LjU3NzExOTUyODE0NjcyNGUtMTIsCiAgICAgImR5IjogMS4xMzMx
MzI0MDM0NTU0NTU1ZS0xMQogICAgfSwKICAgICJoZXJtaXRpYW5fZ29sZHN0b25lX2Fic193Ml9t
YXgiOiAzLjAxMTM3NTQzNzc2NDM1MzNlLTA5LAogICAgImhlcm1pdGlhbl93Ml80bG93ZXN0Ijog
WwogICAgIDMuNTA3MDg4MjI0Nzc4MDY3ZS0xMCwKICAgICA1LjY5MjI5NDE2NTU2NDYyM2UtMTAs
CiAgICAgMy4wMTEzNzU0Mzc3NjQzNTMzZS0wOSwKICAgICA3MS4yODI5NTA0MDMzMTgxOAogICAg
XSwKICAgICJsYW1iZGFfbWluX0xfR2FtbWEiOiAxLjU5MTIwNjIxNzYzNTU1MmUtMTQsCiAgICAi
cGFzc19hIjogdHJ1ZSwKICAgICJwYXNzX2IiOiB0cnVlLAogICAgInByb2R1Y3RfZm9ybV9hYnNf
dzJfbWF4X3hjaGVjayI6IDMuNDc2MTIzODUwNjc3ODI3ZS0wOAogICB9LAogICAiNDAiOiB7CiAg
ICAiYW5hbHl0aWNfd2FyZF9yZXNpZHVhbCI6IHsKICAgICAiZHgiOiAxLjQxMjc0OTAzNDA5MTc3
MjZlLTExLAogICAgICJkeSI6IDIuMzA0NjEzMzIyNTYzOTQ5ZS0xMQogICAgfSwKICAgICJoZXJt
aXRpYW5fZ29sZHN0b25lX2Fic193Ml9tYXgiOiA4LjEwODg2MzE1Njg5NTIxZS0wOSwKICAgICJo
ZXJtaXRpYW5fdzJfNGxvd2VzdCI6IFsKICAgICAtOC4xMDg4NjMxNTY4OTUyMWUtMDksCiAgICAg
LTEuMTczMTI0NjA4MjA1ODYxOGUtMDksCiAgICAgLTYuMjc5MjUxMTA3ODQyMzQ0ZS0xMCwKICAg
ICA3MS4yODI5NTAzOTcxMTU4MwogICAgXSwKICAgICJsYW1iZGFfbWluX0xfR2FtbWEiOiAxLjY5
MTQ0NzI3MDUzMjk4MTNlLTE0LAogICAgInBhc3NfYSI6IHRydWUsCiAgICAicGFzc19iIjogdHJ1
ZSwKICAgICJwcm9kdWN0X2Zvcm1fYWJzX3cyX21heF94Y2hlY2siOiAzLjYyMDE0ODQzNjkxNjYy
MmUtMDgKICAgfQogIH0sCiAgImxhbWJkYV9taW5fTF9mbG9vciI6IC0xZS0xMiwKICAicGFzc19h
bGxfbmIiOiB0cnVlCiB9LAogInN0ZXAzX2xhZGRlciI6IHsKICAibGFkZGVyX2thIjogWwogICAw
LjMsCiAgIDAuMTUsCiAgIDAuMDc1LAogICAwLjAzNzUsCiAgIDAuMDE4NzUsCiAgIDAuMDA5Mzc1
LAogICAwLjAwNDY4NzUsCiAgIDAuMDAyMzQzNzUsCiAgIDAuMDAxMTcxODc1CiAgXSwKICAicnVu
cyI6IHsKICAgIjI0IjogewogICAgIkwxIjogewogICAgICJHSyI6IHsKICAgICAgImEyIjogMC4w
MDEyNTI4MTg3NjMzNzUxNTUsCiAgICAgICJhNCI6IC0wLjAxNjExNjM1NzQ4MjQ5NjkzLAogICAg
ICAiY2lfYTIiOiAwLjAwMTg1MjI5OTEzMjk3NzEyNSwKICAgICAgImNpX2E0IjogMC4yNDQ1ODMz
NTk2MzE2NDczNywKICAgICAgImZpdF9ybXMiOiAxLjI5OTE4MDY1MDAyNjI4ZS0wNiwKICAgICAg
ImthIjogWwogICAgICAgMC4zLAogICAgICAgMC4xNSwKICAgICAgIDAuMDc1LAogICAgICAgMC4w
Mzc1LAogICAgICAgMC4wMTg3NSwKICAgICAgIDAuMDA5Mzc1LAogICAgICAgMC4wMDQ2ODc1LAog
ICAgICAgMC4wMDIzNDM3NSwKICAgICAgIDAuMDAxMTcxODc1CiAgICAgIF0sCiAgICAgICJyIjog
WwogICAgICAgLTEuNzczNTcxNjgwNTA3ODQ2ZS0wNSwKICAgICAgIDEuOTAwNDEwOTExMDgyMDYy
MmUtMDUsCiAgICAgICA5LjIyMDI2MTc1MDc2NDE4ZS0wNiwKICAgICAgIDMuODAxNzI5NTA1NDI2
MDEwM2UtMDYsCiAgICAgICAxLjE1MzI4Mjc1ODg0Nzg1MTFlLTA2LAogICAgICAgNC4wMzExOTAw
NjE3NTk1NmUtMDcsCiAgICAgICA0Ljg0MjM1MTY2NjMxMjA4NGUtMDcsCiAgICAgICA0LjMzMDYx
NDE4NTAzMjk5OTNlLTA3LAogICAgICAgLTEuMjg1OTE4MTIwOTg1NjYzZS0wNgogICAgICBdCiAg
ICAgfSwKICAgICAiR00iOiB7CiAgICAgICJhMiI6IDAuMDAxNzQ2OTk2NzQ2Nzg4MjI0NiwKICAg
ICAgImE0IjogLTAuMDE3Mjg1MzcyNTEzNzkyOTUzLAogICAgICAiY2lfYTIiOiAwLjAwMTgzMDMz
NjA3ODI3NTQwMjYsCiAgICAgICJjaV9hNCI6IDAuMjQ3MTEyODU0ODE2MzM3OSwKICAgICAgImZp
dF9ybXMiOiAxLjM5MjAxMTQ0MjIxMDExN2UtMDYsCiAgICAgICJrYSI6IFsKICAgICAgIDAuMywK
ICAgICAgIDAuMTUsCiAgICAgICAwLjA3NSwKICAgICAgIDAuMDM3NSwKICAgICAgIDAuMDE4NzUs
CiAgICAgICAwLjAwOTM3NSwKICAgICAgIDAuMDA0Njg3NSwKICAgICAgIDAuMDAyMzQzNzUsCiAg
ICAgICAwLjAwMTE3MTg3NQogICAgICBdLAogICAgICAiciI6IFsKICAgICAgIDEuNzI2NzkxMjg1
MzM5MTQ2NWUtMDUsCiAgICAgICAyLjk1OTgwMzkxNDEzNzYzNzVlLTA1LAogICAgICAgMS4xNzU2
OTM5MTQ2MDEyNjEzZS0wNSwKICAgICAgIDQuNTAzNDc4NjUyNDQwMDUyZS0wNiwKICAgICAgIDEu
MjQ3NDYwMDQyMTUzMDM2OWUtMDYsCiAgICAgICAzLjc3Nzk0Mjk4Mjg5NjU3NmUtMDcsCiAgICAg
ICAtMi4zOTQ0NDg3MjgxODIzOTY3ZS0wOCwKICAgICAgIC0xLjU2OTQwOTU1MjA5MzUwMzZlLTA2
LAogICAgICAgMS43NjMyNTY0MzU1Mjc0MzgzZS0wNgogICAgICBdCiAgICAgfQogICAgfSwKICAg
ICJUIjogewogICAgICJHSyI6IHsKICAgICAgImEyIjogLTAuMDExODY0MzIzNDc4MjgxMDQxLAog
ICAgICAiYTJfZmxvb3Jfd2VpZ2h0ZWQiOiAtMC4wMTIxMDcyMjAxNTQ4MjcxMzcsCiAgICAgICJh
NCI6IC0wLjAxMTc3MTEzMDQ0NTY5ODE4MywKICAgICAgImE0X2Zsb29yX3dlaWdodGVkIjogLTAu
MDA5MDQ0NzExODU4Mzc5OTMyLAogICAgICAiY2lfYTIiOiAwLjAwNzI4MDExNzA2MDM1MDk3OTQs
CiAgICAgICJjaV9hNCI6IDAuOTMwNzAwMDAxODA3NTc0MiwKICAgICAgImZpdF9ybXMiOiA5Ljgy
MjQ4NDc2MTgzMzM5OWUtMDYsCiAgICAgICJmbG9vcl9zaWdtYV9yIjogWwogICAgICAgNS42OTkx
OTYxNTA3NDEyNTVlLTEwLAogICAgICAgMi4yNzU2NDEwNTcyMTYyNzJlLTA5LAogICAgICAgOS4w
OTg1Mjk0NDM3MDAyMjVlLTA5LAogICAgICAgMy42MzkwNjgxODEyODExNzc2ZS0wOCwKICAgICAg
IDEuNDU1NjA2NjM1MjY3NzY0N2UtMDcsCiAgICAgICA1LjgyMjQxMjI3MTE3MTUyM2UtMDcsCiAg
ICAgICAyLjMyODk3MTI0MjM2NDg4NDZlLTA2LAogICAgICAgOS4zMTU4OTYyNjE3MjkxNDhlLTA2
LAogICAgICAgMy43MjY1MzA5NTA4NjczOTllLTA1CiAgICAgIF0sCiAgICAgICJrYSI6IFsKICAg
ICAgIDAuMywKICAgICAgIDAuMTUsCiAgICAgICAwLjA3NSwKICAgICAgIDAuMDM3NSwKICAgICAg
IDAuMDE4NzUsCiAgICAgICAwLjAwOTM3NSwKICAgICAgIDAuMDA0Njg3NSwKICAgICAgIDAuMDAy
MzQzNzUsCiAgICAgICAwLjAwMTE3MTg3NQogICAgICBdLAogICAgICAiciI6IFsKICAgICAgIC0w
LjAwMTE2MjkxMTE4NTY4MjAxNCwKICAgICAgIC0wLjAwMDI3NzI0NDA4NTE5MjgwNzEsCiAgICAg
ICAtNS41NjAyODAzNDAxOTk5NTJlLTA1LAogICAgICAgLTguMzk3MTc3MjMwNjY3OTA3ZS0wNiwK
ICAgICAgIC0xLjMwODM4MDc5MTU5ODExODNlLTA2LAogICAgICAgLTguMjk1NDY3NDY4NDk5ODUx
ZS0wOCwKICAgICAgIC0xLjQ0Mjc2MTA4NjQ4OTc3NDRlLTA2LAogICAgICAgLTIuMDQ4ODM1NzE1
MzA3MDA3ZS0wNiwKICAgICAgIC0yLjUxODY2ODQyNTg1NDkwODZlLTA1CiAgICAgIF0KICAgICB9
LAogICAgICJHTSI6IHsKICAgICAgImEyIjogLTAuMDE5NDQ3MzExNzE2MDIyMzI3LAogICAgICAi
YTJfZmxvb3Jfd2VpZ2h0ZWQiOiAtMC4wMTk1ODg1MDk4NTk5OTYwMzcsCiAgICAgICJhNCI6IC0w
LjAxMjgyODc5MTIxMTU0NDY1NCwKICAgICAgImE0X2Zsb29yX3dlaWdodGVkIjogLTAuMDExMjQ0
MDAwNjIzOTI1NzMzLAogICAgICAiY2lfYTIiOiAwLjAwMjg4NDE4MTY4MzE2NTM4ODQsCiAgICAg
ICJjaV9hNCI6IDAuMjg4MDMwODUwODAxNzc4MTUsCiAgICAgICJmaXRfcm1zIjogMy43MTg4NjI4
NzAxMDczODVlLTA2LAogICAgICAiZmxvb3Jfc2lnbWFfciI6IFsKICAgICAgIDUuNzA3MDg3MzIw
MDEzMzQ5ZS0xMCwKICAgICAgIDIuMjc2NDEwNjE2NzMzMTk0NGUtMDksCiAgICAgICA5LjA5OTM3
OTg2MDUxMTY4MWUtMDksCiAgICAgICAzLjYzOTE3OTQzNzcyNTU3NGUtMDgsCiAgICAgICAxLjQ1
NTYxODM4NTkxNjQyODRlLTA3LAogICAgICAgNS44MjI0MTcyNjQ0ODAxMzVlLTA3LAogICAgICAg
Mi4zMjg5NTU0ODIyODI3OTU2ZS0wNiwKICAgICAgIDkuMzE1ODEzMjEwMjQ3NjE4ZS0wNiwKICAg
ICAgIDMuNzI2MzkxMDU4NTcxMDAxN2UtMDUKICAgICAgXSwKICAgICAgImthIjogWwogICAgICAg
MC4zLAogICAgICAgMC4xNSwKICAgICAgIDAuMDc1LAogICAgICAgMC4wMzc1LAogICAgICAgMC4w
MTg3NSwKICAgICAgIDAuMDA5Mzc1LAogICAgICAgMC4wMDQ2ODc1LAogICAgICAgMC4wMDIzNDM3
NSwKICAgICAgIDAuMDAxMTcxODc1CiAgICAgIF0sCiAgICAgICJyIjogWwogICAgICAgLTAuMDAx
ODU0MDQxODA0OTI2MDk4NywKICAgICAgIC0wLjAwMDQ0NjU4ODY2MTM2NTE1NDg1LAogICAgICAg
LTAuMDAwMTAyNjc4ODAxMTc2ODY5NzgsCiAgICAgICAtMi40MDMxMjM4OTQ3NDUyODVlLTA1LAog
ICAgICAgLTUuNjkyODQ2OTAwOTk1MzYzZS0wNiwKICAgICAgIC04LjU5OTExODI5ODUzNTY1N2Ut
MDcsCiAgICAgICAxLjU5MjU3OTMyMjE5NjAzMDVlLTA2LAogICAgICAgMi4wNjA1NDE0NDI4MDU0
MzAzZS0wNiwKICAgICAgIC02Ljc2NTAwODA5MDQ5MjQwOGUtMDYKICAgICAgXQogICAgIH0KICAg
IH0sCiAgICAiZm1peF9taW5fbzJfVCI6IHsKICAgICAiR0siOiAwLjk5OTk5OTk5OTk5NjgyOTYs
CiAgICAgIkdNIjogMC45OTk5OTk5OTk5OTgzNDY5CiAgICB9LAogICAgImlkZW50IjogewogICAg
ICJHSyI6IFsKICAgICAgewogICAgICAgIkwxIjogewogICAgICAgICJqIjogMCwKICAgICAgICAi
bzIiOiAwLjUsCiAgICAgICAgIm9tZWdhIjogMC43Njg0NDc2MjIzNTA3ODU2CiAgICAgICB9LAog
ICAgICAgIlBIIjogewogICAgICAgICJqIjogMiwKICAgICAgICAib21lZ2EiOiAxLjk4NjEyMDI4
OTYwODIyMDgKICAgICAgIH0sCiAgICAgICAiVCI6IHsKICAgICAgICAiUjIiOiAwLjk5OTkzLAog
ICAgICAgICJqIjogMSwKICAgICAgICAibzIiOiAxLjAsCiAgICAgICAgIm9tZWdhIjogMS4wMzU2
NjMxODQwNjEzNDUzCiAgICAgICB9LAogICAgICAgImthIjogMC4zCiAgICAgIH0sCiAgICAgIHsK
ICAgICAgICJMMSI6IHsKICAgICAgICAiaiI6IDAsCiAgICAgICAgIm8yIjogMC41LAogICAgICAg
ICJvbWVnYSI6IDAuMzg0MjM3OTI3NzQxNjk1NQogICAgICAgfSwKICAgICAgICJQSCI6IHsKICAg
ICAgICAiaiI6IDIsCiAgICAgICAgIm9tZWdhIjogMC45OTM5MTY2NjU0MTUwMDMKICAgICAgIH0s
CiAgICAgICAiVCI6IHsKICAgICAgICAiUjIiOiAwLjk5OTk4LAogICAgICAgICJqIjogMSwKICAg
ICAgICAibzIiOiAxLjAsCiAgICAgICAgIm9tZWdhIjogMC41MTgyOTA3NTIzOTgwNTU0CiAgICAg
ICB9LAogICAgICAgImthIjogMC4xNQogICAgICB9LAogICAgICB7CiAgICAgICAiTDEiOiB7CiAg
ICAgICAgImoiOiAwLAogICAgICAgICJvMiI6IDAuNSwKICAgICAgICAib21lZ2EiOiAwLjE5MjEx
NzA4NDI0Mzk1MDkKICAgICAgIH0sCiAgICAgICAiUEgiOiB7CiAgICAgICAgImoiOiAyLAogICAg
ICAgICJvbWVnYSI6IDAuNDk3MDYyNDI0ODAwMzg5NgogICAgICAgfSwKICAgICAgICJUIjogewog
ICAgICAgICJSMiI6IDEuMCwKICAgICAgICAiaiI6IDEsCiAgICAgICAgIm8yIjogMS4wLAogICAg
ICAgICJvbWVnYSI6IDAuMjU5MjAyODI5NDQwOTUwMTMKICAgICAgIH0sCiAgICAgICAia2EiOiAw
LjA3NQogICAgICB9LAogICAgICB7CiAgICAgICAiTDEiOiB7CiAgICAgICAgImoiOiAwLAogICAg
ICAgICJvMiI6IDAuNSwKICAgICAgICAib21lZ2EiOiAwLjA5NjA1ODAyMTYzMDQ2NjYKICAgICAg
IH0sCiAgICAgICAiUEgiOiB7CiAgICAgICAgImoiOiAyLAogICAgICAgICJvbWVnYSI6IDAuMjQ4
NTQyNTMyMjA0ODQzNQogICAgICAgfSwKICAgICAgICJUIjogewogICAgICAgICJSMiI6IDEuMCwK
ICAgICAgICAiaiI6IDEsCiAgICAgICAgIm8yIjogMS4wLAogICAgICAgICJvbWVnYSI6IDAuMTI5
NjA3NTMyOTc2NjAxODIKICAgICAgIH0sCiAgICAgICAia2EiOiAwLjAzNzUKICAgICAgfSwKICAg
ICAgewogICAgICAgIkwxIjogewogICAgICAgICJqIjogMCwKICAgICAgICAibzIiOiAwLjUsCiAg
ICAgICAgIm9tZWdhIjogMC4wNDgwMjg4ODM2MTM0Mzk0NQogICAgICAgfSwKICAgICAgICJQSCI6
IHsKICAgICAgICAiaiI6IDIsCiAgICAgICAgIm9tZWdhIjogMC4xMjQyNzIxNDcxNjc1NzQxNQog
ICAgICAgfSwKICAgICAgICJUIjogewogICAgICAgICJSMiI6IDEuMCwKICAgICAgICAiaiI6IDEs
CiAgICAgICAgIm8yIjogMS4wLAogICAgICAgICJvbWVnYSI6IDAuMDY0ODA0MjI1ODcyODY3NTYK
ICAgICAgIH0sCiAgICAgICAia2EiOiAwLjAxODc1CiAgICAgIH0sCiAgICAgIHsKICAgICAgICJM
MSI6IHsKICAgICAgICAiaiI6IDAsCiAgICAgICAgIm8yIjogMC41LAogICAgICAgICJvbWVnYSI6
IDAuMDI0MDE0NDIzNzkxOTc2NzE3CiAgICAgICB9LAogICAgICAgIlBIIjogewogICAgICAgICJq
IjogMiwKICAgICAgICAib21lZ2EiOiAwLjA2MjEzNjE2ODcyMTcxMzA4NAogICAgICAgfSwKICAg
ICAgICJUIjogewogICAgICAgICJSMiI6IDEuMCwKICAgICAgICAiaiI6IDEsCiAgICAgICAgIm8y
IjogMS4wLAogICAgICAgICJvbWVnYSI6IDAuMDMyNDAyMTUyNjQyODgxMTcKICAgICAgIH0sCiAg
ICAgICAia2EiOiAwLjAwOTM3NQogICAgICB9LAogICAgICB7CiAgICAgICAiTDEiOiB7CiAgICAg
ICAgImoiOiAwLAogICAgICAgICJvMiI6IDAuNSwKICAgICAgICAib21lZ2EiOiAwLjAxMjAwNzIx
Mjg2OTk2Njg5MwogICAgICAgfSwKICAgICAgICJQSCI6IHsKICAgICAgICAiaiI6IDIsCiAgICAg
ICAgIm9tZWdhIjogMC4wMzEwNjgxMDY4OTMzMjYwMjIKICAgICAgIH0sCiAgICAgICAiVCI6IHsK
ICAgICAgICAiUjIiOiAxLjAsCiAgICAgICAgImoiOiAxLAogICAgICAgICJvMiI6IDEuMCwKICAg
ICAgICAib21lZ2EiOiAwLjAxNjIwMTA1NDI5MTExMTI5OAogICAgICAgfSwKICAgICAgICJrYSI6
IDAuMDA0Njg3NQogICAgICB9LAogICAgICB7CiAgICAgICAiTDEiOiB7CiAgICAgICAgImoiOiAw
LAogICAgICAgICJvMiI6IDAuNSwKICAgICAgICAib21lZ2EiOiAwLjAwNjAwMzYwNjEyNzc1NjU1
MgogICAgICAgfSwKICAgICAgICJQSCI6IHsKICAgICAgICAiaiI6IDIsCiAgICAgICAgIm9tZWdh
IjogMC4wMTU1MzQwNjY0NjUwODgxODgKICAgICAgIH0sCiAgICAgICAiVCI6IHsKICAgICAgICAi
UjIiOiAxLjAsCiAgICAgICAgImoiOiAxLAogICAgICAgICJvMiI6IDEuMCwKICAgICAgICAib21l
Z2EiOiAwLjAwODEwMDUyMjIzNjAyNDU4MgogICAgICAgfSwKICAgICAgICJrYSI6IDAuMDAyMzQz
NzUKICAgICAgfSwKICAgICAgewogICAgICAgIkwxIjogewogICAgICAgICJqIjogMCwKICAgICAg
ICAibzIiOiAwLjUsCiAgICAgICAgIm9tZWdhIjogMC4wMDMwMDE3OTc5MDM4NDI0NjIKICAgICAg
IH0sCiAgICAgICAiUEgiOiB7CiAgICAgICAgImoiOiAyLAogICAgICAgICJvbWVnYSI6IDAuMDA3
NzY3MDExMDUxODY3OTc4CiAgICAgICB9LAogICAgICAgIlQiOiB7CiAgICAgICAgIlIyIjogMS4w
LAogICAgICAgICJqIjogMSwKICAgICAgICAibzIiOiAxLjAsCiAgICAgICAgIm9tZWdhIjogMC4w
MDQwNTAxNjc0MDM0OTE5NzYKICAgICAgIH0sCiAgICAgICAia2EiOiAwLjAwMTE3MTg3NQogICAg
ICB9CiAgICAgXSwKICAgICAiR00iOiBbCiAgICAgIHsKICAgICAgICJMMSI6IHsKICAgICAgICAi
aiI6IDAsCiAgICAgICAgIm8yIjogMC41LAogICAgICAgICJvbWVnYSI6IDAuNzY4NDc0NjQ5MzM1
NTMzNgogICAgICAgfSwKICAgICAgICJQSCI6IHsKICAgICAgICAiaiI6IDIsCiAgICAgICAgIm9t
ZWdhIjogMS45ODY1MjAyODAxMjk5MzIyCiAgICAgICB9LAogICAgICAgIlQiOiB7CiAgICAgICAg
IlIyIjogMC45OTk5MiwKICAgICAgICAiaiI6IDEsCiAgICAgICAgIm8yIjogMS4wLAogICAgICAg
ICJvbWVnYSI6IDEuMDM0OTQ2OTMyNDkxNjE4NQogICAgICAgfSwKICAgICAgICJrYSI6IDAuMwog
ICAgICB9LAogICAgICB7CiAgICAgICAiTDEiOiB7CiAgICAgICAgImoiOiAwLAogICAgICAgICJv
MiI6IDAuNSwKICAgICAgICAib21lZ2EiOiAwLjM4NDI0MjA2MjI4MDY5NTg1CiAgICAgICB9LAog
ICAgICAgIlBIIjogewogICAgICAgICJqIjogMiwKICAgICAgICAib21lZ2EiOiAwLjk5Mzk2MjA0
Njc4NzcxMTgKICAgICAgIH0sCiAgICAgICAiVCI6IHsKICAgICAgICAiUjIiOiAwLjk5OTk4LAog
ICAgICAgICJqIjogMSwKICAgICAgICAibzIiOiAxLjAsCiAgICAgICAgIm9tZWdhIjogMC41MTgy
MDMxMzg3NDU5MDU0CiAgICAgICB9LAogICAgICAgImthIjogMC4xNQogICAgICB9LAogICAgICB7
CiAgICAgICAiTDEiOiB7CiAgICAgICAgImoiOiAwLAogICAgICAgICJvMiI6IDAuNSwKICAgICAg
ICAib21lZ2EiOiAwLjE5MjExNzYwMzU5MTI2ODg3CiAgICAgICB9LAogICAgICAgIlBIIjogewog
ICAgICAgICJqIjogMiwKICAgICAgICAib21lZ2EiOiAwLjQ5NzA2Nzc5MDA4OTMwNTQ2CiAgICAg
ICB9LAogICAgICAgIlQiOiB7CiAgICAgICAgIlIyIjogMS4wLAogICAgICAgICJqIjogMSwKICAg
ICAgICAibzIiOiAxLjAsCiAgICAgICAgIm9tZWdhIjogMC4yNTkxOTA3MTY3Njk2NjY5CiAgICAg
ICB9LAogICAgICAgImthIjogMC4wNzUKICAgICAgfSwKICAgICAgewogICAgICAgIkwxIjogewog
ICAgICAgICJqIjogMCwKICAgICAgICAibzIiOiAwLjUsCiAgICAgICAgIm9tZWdhIjogMC4wOTYw
NTgxMDUwNDUxMDIyCiAgICAgICB9LAogICAgICAgIlBIIjogewogICAgICAgICJqIjogMiwKICAg
ICAgICAib21lZ2EiOiAwLjI0ODU0MzM4NDU2NjQzMDc3CiAgICAgICB9LAogICAgICAgIlQiOiB7
CiAgICAgICAgIlIyIjogMS4wLAogICAgICAgICJqIjogMSwKICAgICAgICAibzIiOiAxLjAsCiAg
ICAgICAgIm9tZWdhIjogMC4xMjk2MDU1NTE3OTA0OTMzMgogICAgICAgfSwKICAgICAgICJrYSI6
IDAuMDM3NQogICAgICB9LAogICAgICB7CiAgICAgICAiTDEiOiB7CiAgICAgICAgImoiOiAwLAog
ICAgICAgICJvMiI6IDAuNSwKICAgICAgICAib21lZ2EiOiAwLjA0ODAyODg5NjEzOTc2NjUxCiAg
ICAgICB9LAogICAgICAgIlBIIjogewogICAgICAgICJqIjogMiwKICAgICAgICAib21lZ2EiOiAw
LjEyNDI3MjI3MjExNjE2OTg1CiAgICAgICB9LAogICAgICAgIlQiOiB7CiAgICAgICAgIlIyIjog
MS4wLAogICAgICAgICJqIjogMSwKICAgICAgICAibzIiOiAxLjAsCiAgICAgICAgIm9tZWdhIjog
MC4wNjQ4MDM5NjQzMDI1MTU2MwogICAgICAgfSwKICAgICAgICJrYSI6IDAuMDE4NzUKICAgICAg
fSwKICAgICAgewogICAgICAgIkwxIjogewogICAgICAgICJqIjogMCwKICAgICAgICAibzIiOiAw
LjUsCiAgICAgICAgIm9tZWdhIjogMC4wMjQwMTQ0MjcxODUzNjY0NjcKICAgICAgIH0sCiAgICAg
ICAiUEgiOiB7CiAgICAgICAgImoiOiAyLAogICAgICAgICJvbWVnYSI6IDAuMDYyMTM2MTg3NDQy
OTE0NTQKICAgICAgIH0sCiAgICAgICAiVCI6IHsKICAgICAgICAiUjIiOiAxLjAsCiAgICAgICAg
ImoiOiAxLAogICAgICAgICJvMiI6IDEuMCwKICAgICAgICAib21lZ2EiOiAwLjAzMjQwMjEzODc0
ODgyNTIxNAogICAgICAgfSwKICAgICAgICJrYSI6IDAuMDA5Mzc1CiAgICAgIH0sCiAgICAgIHsK
ICAgICAgICJMMSI6IHsKICAgICAgICAiaiI6IDAsCiAgICAgICAgIm8yIjogMC41LAogICAgICAg
ICJvbWVnYSI6IDAuMDEyMDA3MjA4NzY4OTIxNjQ5CiAgICAgICB9LAogICAgICAgIlBIIjogewog
ICAgICAgICJqIjogMiwKICAgICAgICAib21lZ2EiOiAwLjAzMTA2ODA4MDc1Mzc3NjI2CiAgICAg
ICB9LAogICAgICAgIlQiOiB7CiAgICAgICAgIlIyIjogMS4wLAogICAgICAgICJqIjogMSwKICAg
ICAgICAibzIiOiAxLjAsCiAgICAgICAgIm9tZWdhIjogMC4wMTYyMDExMDkxMDc0MjYwNjYKICAg
ICAgIH0sCiAgICAgICAia2EiOiAwLjAwNDY4NzUKICAgICAgfSwKICAgICAgewogICAgICAgIkwx
IjogewogICAgICAgICJqIjogMCwKICAgICAgICAibzIiOiAwLjUsCiAgICAgICAgIm9tZWdhIjog
MC4wMDYwMDM1OTUxMDYwOTk3NjMKICAgICAgIH0sCiAgICAgICAiUEgiOiB7CiAgICAgICAgImoi
OiAyLAogICAgICAgICJvbWVnYSI6IDAuMDE1NTM0MDA0ODAwNTA1NzQKICAgICAgIH0sCiAgICAg
ICAiVCI6IHsKICAgICAgICAiUjIiOiAxLjAsCiAgICAgICAgImoiOiAxLAogICAgICAgICJvMiI6
IDEuMCwKICAgICAgICAib21lZ2EiOiAwLjAwODEwMDU1ODM0NDQ1OTY4NAogICAgICAgfSwKICAg
ICAgICJrYSI6IDAuMDAyMzQzNzUKICAgICAgfSwKICAgICAgewogICAgICAgIkwxIjogewogICAg
ICAgICJqIjogMCwKICAgICAgICAibzIiOiAwLjUsCiAgICAgICAgIm9tZWdhIjogMC4wMDMwMDE4
MDc1NTcwNTQxODkKICAgICAgIH0sCiAgICAgICAiUEgiOiB7CiAgICAgICAgImoiOiAyLAogICAg
ICAgICJvbWVnYSI6IDAuMDA3NzY3MDg3NzcyNDI2Mzc4CiAgICAgICB9LAogICAgICAgIlQiOiB7
CiAgICAgICAgIlIyIjogMS4wLAogICAgICAgICJqIjogMSwKICAgICAgICAibzIiOiAxLjAsCiAg
ICAgICAgIm9tZWdhIjogMC4wMDQwNTAyNDM0MjYzNjQwNAogICAgICAgfSwKICAgICAgICJrYSI6
IDAuMDAxMTcxODc1CiAgICAgIH0KICAgICBdCiAgICB9LAogICAgImxhbV9taW5fTF9taW4iOiAw
LjAsCiAgICAibl9iIjogMjQsCiAgICAic3BlZWRzIjogewogICAgICJHSyI6IHsKICAgICAgIkwx
IjogMy43NDEzNTYwNjQ3Mjk0MTEzLAogICAgICAiUEgiOiA5LjY4MDU4OTQwMzQwNDY4OSwKICAg
ICAgIlJfVF9mcmFtZXdvcmsiOiAwLjUyMTQ2OTc4MDYyMjU4MjEsCiAgICAgICJUIjogNS4wNDgx
MzQ4MzI0OTA3MzYsCiAgICAgICJjX0wxX2ZyYW1ld29yayI6IDkuNjgwNTg5NDAzNDA0Njg5CiAg
ICAgfSwKICAgICAiR00iOiB7CiAgICAgICJMMSI6IDMuNzQxMzU2Njg4MTU1Mzc5LAogICAgICAi
UEgiOiA5LjY4MDU4OTE4Nzc4MDUyLAogICAgICAiUl9UX2ZyYW1ld29yayI6IDAuNTIxNDY5OTcz
NzkxMTM3NywKICAgICAgIlQiOiA1LjA0ODEzNjU5MDAzNDY3OCwKICAgICAgImNfTDFfZnJhbWV3
b3JrIjogOS42ODA1ODkxODc3ODA1MgogICAgIH0KICAgIH0sCiAgICAic3RlcDEiOiB7CiAgICAg
Im1lYW5fcmhvIjogMC45OTk5ODgxMjkyNDc0NDcyLAogICAgICJwc2kwX21kNSI6ICJiMjdmYTAw
NDk1ZWY2ODZiMDE4NGVhMjljNDU1YjRkYiIsCiAgICAgInJlc2lkdWFsX3JldmVyaWZpZWQiOiAx
Ljk1NTAyNTU3ODQyNjI5MzRlLTEyLAogICAgICJzb3VyY2UiOiAiUGhhc2UtMSBpdGVtIDEgKGhh
bHQgcmVwb3J0IGIwZTY3OTBjKSIKICAgIH0sCiAgICAid2FyZCI6IHsKICAgICAiQTFfdGhyZXNo
b2xkX2FuYWx5dGljIjogMWUtMDksCiAgICAgIkExX3RocmVzaG9sZF9oZXJtaXRpYW5fdzIiOiAx
ZS0wOCwKICAgICAiYnlfbmIiOiB7CiAgICAgICIyNCI6IHsKICAgICAgICJhbmFseXRpY193YXJk
X3Jlc2lkdWFsIjogewogICAgICAgICJkeCI6IDIuMjgxNzkyMDU3NDA2OTgxNmUtMTIsCiAgICAg
ICAgImR5IjogMy4xMDAyMTA3NzgwNDY3MDFlLTEyCiAgICAgICB9LAogICAgICAgImhlcm1pdGlh
bl9nb2xkc3RvbmVfYWJzX3cyX21heCI6IDEuMjIyNTg5NTQxNjc2MzQwNWUtMDksCiAgICAgICAi
aGVybWl0aWFuX3cyXzRsb3dlc3QiOiBbCiAgICAgICAgLTcuMjU2MzcxMDExNTU1MjEyZS0xMCwK
ICAgICAgICAxLjkzNDE3MTQ1Nzg1NTM5NDZlLTExLAogICAgICAgIDEuMjIyNTg5NTQxNjc2MzQw
NWUtMDksCiAgICAgICAgNzEuMjgyOTUwNDAxNTYyNDkKICAgICAgIF0sCiAgICAgICAibGFtYmRh
X21pbl9MX0dhbW1hIjogMS42MjYyNjU0MTc5ODM2NTY3ZS0xNCwKICAgICAgICJwYXNzX2EiOiB0
cnVlLAogICAgICAgInBhc3NfYiI6IHRydWUsCiAgICAgICAicHJvZHVjdF9mb3JtX2Fic193Ml9t
YXhfeGNoZWNrIjogMi4xMjQ4NzI5ODQwMzY1NDYyZS0wOQogICAgICB9LAogICAgICAiMzIiOiB7
CiAgICAgICAiYW5hbHl0aWNfd2FyZF9yZXNpZHVhbCI6IHsKICAgICAgICAiZHgiOiA2LjU3NzEx
OTUyODE0NjcyNGUtMTIsCiAgICAgICAgImR5IjogMS4xMzMxMzI0MDM0NTU0NTU1ZS0xMQogICAg
ICAgfSwKICAgICAgICJoZXJtaXRpYW5fZ29sZHN0b25lX2Fic193Ml9tYXgiOiAzLjAxMTM3NTQz
Nzc2NDM1MzNlLTA5LAogICAgICAgImhlcm1pdGlhbl93Ml80bG93ZXN0IjogWwogICAgICAgIDMu
NTA3MDg4MjI0Nzc4MDY3ZS0xMCwKICAgICAgICA1LjY5MjI5NDE2NTU2NDYyM2UtMTAsCiAgICAg
ICAgMy4wMTEzNzU0Mzc3NjQzNTMzZS0wOSwKICAgICAgICA3MS4yODI5NTA0MDMzMTgxOAogICAg
ICAgXSwKICAgICAgICJsYW1iZGFfbWluX0xfR2FtbWEiOiAxLjU5MTIwNjIxNzYzNTU1MmUtMTQs
CiAgICAgICAicGFzc19hIjogdHJ1ZSwKICAgICAgICJwYXNzX2IiOiB0cnVlLAogICAgICAgInBy
b2R1Y3RfZm9ybV9hYnNfdzJfbWF4X3hjaGVjayI6IDMuNDc2MTIzODUwNjc3ODI3ZS0wOAogICAg
ICB9LAogICAgICAiNDAiOiB7CiAgICAgICAiYW5hbHl0aWNfd2FyZF9yZXNpZHVhbCI6IHsKICAg
ICAgICAiZHgiOiAxLjQxMjc0OTAzNDA5MTc3MjZlLTExLAogICAgICAgICJkeSI6IDIuMzA0NjEz
MzIyNTYzOTQ5ZS0xMQogICAgICAgfSwKICAgICAgICJoZXJtaXRpYW5fZ29sZHN0b25lX2Fic193
Ml9tYXgiOiA4LjEwODg2MzE1Njg5NTIxZS0wOSwKICAgICAgICJoZXJtaXRpYW5fdzJfNGxvd2Vz
dCI6IFsKICAgICAgICAtOC4xMDg4NjMxNTY4OTUyMWUtMDksCiAgICAgICAgLTEuMTczMTI0NjA4
MjA1ODYxOGUtMDksCiAgICAgICAgLTYuMjc5MjUxMTA3ODQyMzQ0ZS0xMCwKICAgICAgICA3MS4y
ODI5NTAzOTcxMTU4MwogICAgICAgXSwKICAgICAgICJsYW1iZGFfbWluX0xfR2FtbWEiOiAxLjY5
MTQ0NzI3MDUzMjk4MTNlLTE0LAogICAgICAgInBhc3NfYSI6IHRydWUsCiAgICAgICAicGFzc19i
IjogdHJ1ZSwKICAgICAgICJwcm9kdWN0X2Zvcm1fYWJzX3cyX21heF94Y2hlY2siOiAzLjYyMDE0
ODQzNjkxNjYyMmUtMDgKICAgICAgfQogICAgIH0sCiAgICAgImxhbWJkYV9taW5fTF9mbG9vciI6
IC0xZS0xMiwKICAgICAicGFzc19hbGxfbmIiOiB0cnVlCiAgICB9LAogICAgInhjaGVja19wcm9k
dWN0X3ZzX2hlcm1pdGlhbiI6IHsKICAgICAiR0tfa2E9MC4wMTg3IjogewogICAgICAiaGVybWl0
aWFuIjogWwogICAgICAgMC4wMDIzMDY3NzM2NjExNTMzMTMsCiAgICAgICAwLjAwNDE5OTU4NzY5
MDk4MTYzODUsCiAgICAgICAwLjAxNTQ0MzU2NjU2MTYzOTIwOCwKICAgICAgIDcxLjI5MzA4MDA0
MjQwMDY5CiAgICAgIF0sCiAgICAgICJwcm9kdWN0IjogWwogICAgICAgMC4wMDIzMDY3ODAwOTI5
MTQ1MTAzLAogICAgICAgMC4wMDQxOTk1ODYyNjg3MDg0MTMsCiAgICAgICAwLjAxNTQ0MzU2NTcy
MDA1ODc4LAogICAgICAgNzEuMjkzMDgwMDQxNjU0ODMKICAgICAgXQogICAgIH0sCiAgICAgIkdL
X2thPTAuMzAwMCI6IHsKICAgICAgImhlcm1pdGlhbiI6IFsKICAgICAgIDAuNTkwNTExNzQ4Mjk2
NTc1NiwKICAgICAgIDEuMDcyNTk4MjMwODIwMDgzOSwKICAgICAgIDMuOTQ0NjczODA0NzkzNDQz
LAogICAgICAgNzMuODU0MTM1Nzk3NjUyNzMKICAgICAgXSwKICAgICAgInByb2R1Y3QiOiBbCiAg
ICAgICAwLjU5MDUxMTc0NDU2MzYzNDQsCiAgICAgICAxLjA3MjU5ODIzMzAwMDk4ODksCiAgICAg
ICAzLjk0NDY3MzgwNzEwNTk4NSwKICAgICAgIDczLjg1NDEzNTc5NjUxMjYyCiAgICAgIF0KICAg
ICB9LAogICAgICJHTV9rYT0wLjAxODciOiB7CiAgICAgICJoZXJtaXRpYW4iOiBbCiAgICAgICAw
LjAwMjMwNjc3NDg2NDQwNDQ3ODMsCiAgICAgICAwLjAwNDE5OTU1Mzc4OTMyMTcyLAogICAgICAg
MC4wMTU0NDM1OTc2MTY5MTUzNjgsCiAgICAgICA3MS4yOTMwODAwNDI2MDQ2NwogICAgICBdLAog
ICAgICAicHJvZHVjdCI6IFsKICAgICAgIDAuMDAyMzA2Nzc5MDEyMTIxOTY5OCwKICAgICAgIDAu
MDA0MTk5NTUzNTkyNjEwMDgsCiAgICAgICAwLjAxNTQ0MzU5Mjk3NzQ2MzI2OSwKICAgICAgIDcx
LjI5MzA4MDA0MzI0OTI2CiAgICAgIF0KICAgICB9LAogICAgICJHTV9rYT0wLjMwMDAiOiB7CiAg
ICAgICJoZXJtaXRpYW4iOiBbCiAgICAgICAwLjU5MDU1MzI4NjY3MTM3MTMsCiAgICAgICAxLjA3
MTExNTE1MzA3MzgxMDgsCiAgICAgICAzLjk0NjI2MjgyMzM2NzUwNCwKICAgICAgIDczLjg1NDA5
Mjk2MDAzMTIxCiAgICAgIF0sCiAgICAgICJwcm9kdWN0IjogWwogICAgICAgMC41OTA1NTMyODg3
NTkyMzQ2LAogICAgICAgMS4wNzExMTUxNTI2NTI2MDQ4LAogICAgICAgMy45NDYyNjI4MjA5ODUx
NTcsCiAgICAgICA3My44NTQwOTI5NTg2MDMxNQogICAgICBdCiAgICAgfQogICAgfQogICB9LAog
ICAiMzIiOiB7CiAgICAiTDEiOiB7CiAgICAgIkdLIjogewogICAgICAiYTIiOiAwLjAwMTA5NzIz
MzA0MzY0Mjc2NTYsCiAgICAgICJhNCI6IC0wLjAxNDY0NzQ5ODg5NzU5NzUwNSwKICAgICAgImNp
X2EyIjogMC4wMDA0MDU1ODYzMjI3ODcyMTM1LAogICAgICAiY2lfYTQiOiAwLjExNjI1MjkyMzE4
NTc1NjEsCiAgICAgICJmaXRfcm1zIjogNi40NzIwOTE2NDA5ODI3NDJlLTA2LAogICAgICAia2Ei
OiBbCiAgICAgICAwLjMsCiAgICAgICAwLjE1LAogICAgICAgMC4wNzUsCiAgICAgICAwLjAzNzUs
CiAgICAgICAwLjAxODc1LAogICAgICAgMC4wMDkzNzUsCiAgICAgICAwLjAwNDY4NzUsCiAgICAg
ICAwLjAwMjM0Mzc1LAogICAgICAgMC4wMDExNzE4NzUKICAgICAgXSwKICAgICAgInIiOiBbCiAg
ICAgICAtMS45ODczNzc5NDkyMDg1NTc1ZS0wNSwKICAgICAgIDEuNjg2NjcwMDc2ODk0NzE0ZS0w
NSwKICAgICAgIDcuMDc5NTY1NzM4MzEwNDc4ZS0wNiwKICAgICAgIDEuNjc4OTQ1MDkwOTU0ODk3
NWUtMDYsCiAgICAgICAtMS4xNDA0NjA1MDgzNjQyNDk0ZS0wNiwKICAgICAgIC0xLjIyNzA1OTk2
MTk3MjM2NTRlLTA2LAogICAgICAgLTEuMzU5Njg3OTE5Njk5NzU5MWUtMDYsCiAgICAgICA4LjE3
NzI1Nzk3MjUzMDMyN2UtMDYsCiAgICAgICAxLjczODQyNzQyNjI1NjYyOGUtMDUKICAgICAgXQog
ICAgIH0sCiAgICAgIkdNIjogewogICAgICAiYTIiOiAwLjAwMTgxMjAzOTQzOTYwNDg2NTYsCiAg
ICAgICJhNCI6IC0wLjAxNzg5OTgwNTIzMTU0MjE0LAogICAgICAiY2lfYTIiOiAwLjAwMjc1OTU5
ODcxMTUzMTg5MDUsCiAgICAgICJjaV9hNCI6IDAuMzk1MzQ3ODAyMDI0NjQxMSwKICAgICAgImZp
dF9ybXMiOiAxLjczMTMyNzQ0MjA0MDkxOTZlLTA1LAogICAgICAia2EiOiBbCiAgICAgICAwLjMs
CiAgICAgICAwLjE1LAogICAgICAgMC4wNzUsCiAgICAgICAwLjAzNzUsCiAgICAgICAwLjAxODc1
LAogICAgICAgMC4wMDkzNzUsCiAgICAgICAwLjAwNDY4NzUsCiAgICAgICAwLjAwMjM0Mzc1LAog
ICAgICAgMC4wMDExNzE4NzUKICAgICAgXSwKICAgICAgInIiOiBbCiAgICAgICAxLjgxNTg2MTEw
ODYzMzg1NGUtMDUsCiAgICAgICAzLjA0OTI2NzkzMzE3NTA1OTRlLTA1LAogICAgICAgMS4yNjQ5
ODYyODU5ODcwMzUzZS0wNSwKICAgICAgIDUuNDE2MjYzMDgyOTI0NjQ0ZS0wNiwKICAgICAgIDIu
MDcyNDU5Mjk4ODQwODEyZS0wNiwKICAgICAgIDEuOTI2NDU5ODA4NTY1NTM5M2UtMDYsCiAgICAg
ICAxLjc0Njg2NDE5NTI5NTU3MjFlLTA2LAogICAgICAgLTEuMTQ4MDg3MTMzNzE3NzIzNGUtMDUs
CiAgICAgICAtNS4wMzgxNTAxMDY3NzMxMDk0ZS0wNQogICAgICBdCiAgICAgfQogICAgfSwKICAg
ICJUIjogewogICAgICJHSyI6IHsKICAgICAgImEyIjogLTAuMDExOTEzNDM1NzczMjE5NDE0LAog
ICAgICAiYTJfZmxvb3Jfd2VpZ2h0ZWQiOiAtMC4wMTIxNDY3NjQzMzQ1NDE3MzksCiAgICAgICJh
NCI6IC0wLjAxMTMxMTMyMzEwODMyNjY1NywKICAgICAgImE0X2Zsb29yX3dlaWdodGVkIjogLTAu
MDA4NjkyMjkyNzEwMjg5NzYyLAogICAgICAiY2lfYTIiOiAwLjAwNzA4ODEyNzU4MjUxODI4OSwK
ICAgICAgImNpX2E0IjogMC45MTE3ODA1OTEyNTEyNDg5LAogICAgICAiZml0X3JtcyI6IDAuMDAw
MTAzNzA0NjE1MDg2Mjg1MzEsCiAgICAgICJmbG9vcl9zaWdtYV9yIjogWwogICAgICAgMS40MDM3
NzYwNjI0OTg4MzE1ZS0wOSwKICAgICAgIDUuNjA1MTU5NjMwNzEyNTYxZS0wOSwKICAgICAgIDIu
MjQxMDcwMDg4NDE3NjM3ZS0wOCwKICAgICAgIDguOTYzNDM0MzQzNzI2ODY0ZS0wOCwKICAgICAg
IDMuNTg1MzI1MDYxODgxMjllLTA3LAogICAgICAgMS40MzQxMjU1NzcwNDQ2MjNlLTA2LAogICAg
ICAgNS43MzY1Mzg1ODgxNjI1MzRlLTA2LAogICAgICAgMi4yOTQyNDY3Njg0MzQ5Mjg0ZS0wNSwK
ICAgICAgIDkuMTcyODYyNjc5MjQxMjUzZS0wNQogICAgICBdLAogICAgICAia2EiOiBbCiAgICAg
ICAwLjMsCiAgICAgICAwLjE1LAogICAgICAgMC4wNzUsCiAgICAgICAwLjAzNzUsCiAgICAgICAw
LjAxODc1LAogICAgICAgMC4wMDkzNzUsCiAgICAgICAwLjAwNDY4NzUsCiAgICAgICAwLjAwMjM0
Mzc1LAogICAgICAgMC4wMDExNzE4NzUKICAgICAgXSwKICAgICAgInIiOiBbCiAgICAgICAtMC4w
MDExNjM2MTU1OTgzMDcyNDM4LAogICAgICAgLTAuMDAwMjc3OTQ1Mzk5MDcyNDQzNCwKICAgICAg
IC01LjYzMTUyMTcwMDAyMjQ1N2UtMDUsCiAgICAgICAtOS4xMjY3MDA0MzkyODgwOTNlLTA2LAog
ICAgICAgLTIuMzM4NjEzMDA0ODA0MjAyZS0wNiwKICAgICAgIC03Ljg3OTQ4OTIyNzc1NzgzZS0w
NywKICAgICAgIC0zLjk1MDEzNTY4OTIxMjQzMWUtMDYsCiAgICAgICA3LjYzOTIyNjAyNzI2NzI5
OGUtMDUsCiAgICAgICAwLjAwMDMwMTE5OTE4MDk5MDAzMDUKICAgICAgXQogICAgIH0sCiAgICAg
IkdNIjogewogICAgICAiYTIiOiAtMC4wMjAwNDA2MDU1OTc0NzY5LAogICAgICAiYTJfZmxvb3Jf
d2VpZ2h0ZWQiOiAtMC4wMjAwNDk0MjUwOTA2NjAxNTIsCiAgICAgICJhNCI6IC0wLjAwNzIzMjU3
NjgxMDAzMjQ2LAogICAgICAiYTRfZmxvb3Jfd2VpZ2h0ZWQiOiAtMC4wMDcxMzQwMDkwMzE5MTc1
NTYsCiAgICAgICJjaV9hMiI6IDAuMDA1MjQyNzc5MTgwMjU4NTMsCiAgICAgICJjaV9hNCI6IDAu
OTk5NzYzNDM3NzM0ODg2MywKICAgICAgImZpdF9ybXMiOiAxLjk4ODYyNDAxNTgyMzQxODNlLTA1
LAogICAgICAiZmxvb3Jfc2lnbWFfciI6IFsKICAgICAgIDEuNDA1NzE5NzM5Mzg1NzQ2ZS0wOSwK
ICAgICAgIDUuNjA3MDU0ODQwOTA5NzA4ZS0wOSwKICAgICAgIDIuMjQxMjc5NDkzNjA4NDQxNGUt
MDgsCiAgICAgICA4Ljk2MzcwODU1NjE1NzY1M2UtMDgsCiAgICAgICAzLjU4NTM0NDYxODg3OTA2
OTVlLTA3LAogICAgICAgMS40MzQxMDg4NzEyODA1MjY0ZS0wNiwKICAgICAgIDUuNzM2MzQ4NDI1
MzM3MTAzZS0wNiwKICAgICAgIDIuMjk0NjkyNjcwOTgwNTYxN2UtMDUsCiAgICAgICA5LjE3NzI5
ODU3ODczNDg1OGUtMDUKICAgICAgXSwKICAgICAgImthIjogWwogICAgICAgMC4zLAogICAgICAg
MC4xNSwKICAgICAgIDAuMDc1LAogICAgICAgMC4wMzc1LAogICAgICAgMC4wMTg3NSwKICAgICAg
IDAuMDA5Mzc1LAogICAgICAgMC4wMDQ2ODc1LAogICAgICAgMC4wMDIzNDM3NSwKICAgICAgIDAu
MDAxMTcxODc1CiAgICAgIF0sCiAgICAgICJyIjogWwogICAgICAgLTAuMDAxODYyMjMzNjA1ODI5
MDQ0NSwKICAgICAgIC0wLjAwMDQ1NDc2Mzg0Mjk3MTcxNzEsCiAgICAgICAtMC4wMDAxMTA4ODA3
NzM0MzkwMTQ5MiwKICAgICAgIC0zLjIyNzQ1NDcxNDYyNzE1NGUtMDUsCiAgICAgICAtMS4yOTE4
MjgyMTg3NjM1MDIyZS0wNSwKICAgICAgIC0yLjgxNTkyODM4NjM1NzEzNmUtMDYsCiAgICAgICA0
Ljc3MjQ1Mzg5NzQwNTg4MmUtMDYsCiAgICAgICAtMi44NjMxNjEzNjE4NzY4MDkzZS0wNSwKICAg
ICAgIDUuMTU2NjQ5Njg3OTIwNzMzNWUtMDUKICAgICAgXQogICAgIH0KICAgIH0sCiAgICAiZm1p
eF9taW5fbzJfVCI6IHsKICAgICAiR0siOiAwLjk5OTk5OTk5OTg3NjY0NDgsCiAgICAgIkdNIjog
MC45OTk5OTk5OTk5NjAwOTA5CiAgICB9LAogICAgImlkZW50IjogewogICAgICJHSyI6IFsKICAg
ICAgewogICAgICAgIkwxIjogewogICAgICAgICJqIjogMCwKICAgICAgICAibzIiOiAwLjUsCiAg
ICAgICAgIm9tZWdhIjogMC43Njg0NDc2MjA4OTM1MTMKICAgICAgIH0sCiAgICAgICAiUEgiOiB7
CiAgICAgICAgImoiOiAyLAogICAgICAgICJvbWVnYSI6IDEuOTg2MTIwMjg5NDA2ODg5NwogICAg
ICAgfSwKICAgICAgICJUIjogewogICAgICAgICJSMiI6IDAuOTk5OTMsCiAgICAgICAgImoiOiAx
LAogICAgICAgICJvMiI6IDEuMCwKICAgICAgICAib21lZ2EiOiAxLjAzNTY2MzE4MzI5NzI4MQog
ICAgICAgfSwKICAgICAgICJrYSI6IDAuMwogICAgICB9LAogICAgICB7CiAgICAgICAiTDEiOiB7
CiAgICAgICAgImoiOiAwLAogICAgICAgICJvMiI6IDAuNSwKICAgICAgICAib21lZ2EiOiAwLjM4
NDIzNzkyNzI5NDYzNTIKICAgICAgIH0sCiAgICAgICAiUEgiOiB7CiAgICAgICAgImoiOiAyLAog
ICAgICAgICJvbWVnYSI6IDAuOTkzOTE2NjY0NzExNzYzNQogICAgICAgfSwKICAgICAgICJUIjog
ewogICAgICAgICJSMiI6IDAuOTk5OTgsCiAgICAgICAgImoiOiAxLAogICAgICAgICJvMiI6IDEu
MCwKICAgICAgICAib21lZ2EiOiAwLjUxODI5MDc1Mzk0NTk5NzMKICAgICAgIH0sCiAgICAgICAi
a2EiOiAwLjE1CiAgICAgIH0sCiAgICAgIHsKICAgICAgICJMMSI6IHsKICAgICAgICAiaiI6IDAs
CiAgICAgICAgIm8yIjogMC41LAogICAgICAgICJvbWVnYSI6IDAuMTkyMTE3MDgzMzg0NzkyMjUK
ICAgICAgIH0sCiAgICAgICAiUEgiOiB7CiAgICAgICAgImoiOiAyLAogICAgICAgICJvbWVnYSI6
IDAuNDk3MDYyNDI2OTI2NjQ1CiAgICAgICB9LAogICAgICAgIlQiOiB7CiAgICAgICAgIlIyIjog
MS4wLAogICAgICAgICJqIjogMSwKICAgICAgICAibzIiOiAxLjAsCiAgICAgICAgIm9tZWdhIjog
MC4yNTkyMDI4MjczNzgxNTYxNAogICAgICAgfSwKICAgICAgICJrYSI6IDAuMDc1CiAgICAgIH0s
CiAgICAgIHsKICAgICAgICJMMSI6IHsKICAgICAgICAiaiI6IDAsCiAgICAgICAgIm8yIjogMC41
LAogICAgICAgICJvbWVnYSI6IDAuMDk2MDU4MDIyOTIwMzI1MTgKICAgICAgIH0sCiAgICAgICAi
UEgiOiB7CiAgICAgICAgImoiOiAyLAogICAgICAgICJvbWVnYSI6IDAuMjQ4NTQyNTM0MDYwNDIy
CiAgICAgICB9LAogICAgICAgIlQiOiB7CiAgICAgICAgIlIyIjogMS4wLAogICAgICAgICJqIjog
MSwKICAgICAgICAibzIiOiAxLjAsCiAgICAgICAgIm9tZWdhIjogMC4xMjk2MDc1Mjk3MzE5NjA1
NQogICAgICAgfSwKICAgICAgICJrYSI6IDAuMDM3NQogICAgICB9LAogICAgICB7CiAgICAgICAi
TDEiOiB7CiAgICAgICAgImoiOiAwLAogICAgICAgICJvMiI6IDAuNSwKICAgICAgICAib21lZ2Ei
OiAwLjA0ODAyODg3NjA0NzEyNjExCiAgICAgICB9LAogICAgICAgIlBIIjogewogICAgICAgICJq
IjogMiwKICAgICAgICAib21lZ2EiOiAwLjEyNDI3MjEzNjUxODE5NTc4CiAgICAgICB9LAogICAg
ICAgIlQiOiB7CiAgICAgICAgIlIyIjogMS4wLAogICAgICAgICJqIjogMSwKICAgICAgICAibzIi
OiAxLjAsCiAgICAgICAgIm9tZWdhIjogMC4wNjQ4MDQyMDQ3NjM2MTcwOAogICAgICAgfSwKICAg
ICAgICJrYSI6IDAuMDE4NzUKICAgICAgfSwKICAgICAgewogICAgICAgIkwxIjogewogICAgICAg
ICJqIjogMCwKICAgICAgICAibzIiOiAwLjUsCiAgICAgICAgIm9tZWdhIjogMC4wMjQwMTQ0MzU5
NDM5MjM0NjgKICAgICAgIH0sCiAgICAgICAiUEgiOiB7CiAgICAgICAgImoiOiAyLAogICAgICAg
ICJvbWVnYSI6IDAuMDYyMTM2MTYzNTE5ODk4NzEKICAgICAgIH0sCiAgICAgICAiVCI6IHsKICAg
ICAgICAiUjIiOiAxLjAsCiAgICAgICAgImoiOiAxLAogICAgICAgICJvMiI6IDEuMCwKICAgICAg
ICAib21lZ2EiOiAwLjAzMjQwMjE1MjYyNjcwMjM5CiAgICAgICB9LAogICAgICAgImthIjogMC4w
MDkzNzUKICAgICAgfSwKICAgICAgewogICAgICAgIkwxIjogewogICAgICAgICJqIjogMCwKICAg
ICAgICAibzIiOiAwLjUsCiAgICAgICAgIm9tZWdhIjogMC4wMTIwMDcyMTYzNzk0NjY5ODMKICAg
ICAgIH0sCiAgICAgICAiUEgiOiB7CiAgICAgICAgImoiOiAyLAogICAgICAgICJvbWVnYSI6IDAu
MDMxMDY4MDU0ODkyOTEyNzYyCiAgICAgICB9LAogICAgICAgIlQiOiB7CiAgICAgICAgIlIyIjog
MS4wLAogICAgICAgICJqIjogMSwKICAgICAgICAibzIiOiAxLjAsCiAgICAgICAgIm9tZWdhIjog
MC4wMTYyMDEwMjUwODI0ODE3MDYKICAgICAgIH0sCiAgICAgICAia2EiOiAwLjAwNDY4NzUKICAg
ICAgfSwKICAgICAgewogICAgICAgIkwxIjogewogICAgICAgICJqIjogMCwKICAgICAgICAibzIi
OiAwLjUsCiAgICAgICAgIm9tZWdhIjogMC4wMDYwMDM2NjU0NDU4OTc4MDYKICAgICAgIH0sCiAg
ICAgICAiUEgiOiB7CiAgICAgICAgImoiOiAyLAogICAgICAgICJvbWVnYSI6IDAuMDE1NTM0MDE0
Mzg0MDUzMjU1CiAgICAgICB9LAogICAgICAgIlQiOiB7CiAgICAgICAgIlIyIjogMS4wLAogICAg
ICAgICJqIjogMSwKICAgICAgICAibzIiOiAxLjAsCiAgICAgICAgIm9tZWdhIjogMC4wMDgxMDEx
NjMzNTgzOTc3NTIKICAgICAgIH0sCiAgICAgICAia2EiOiAwLjAwMjM0Mzc1CiAgICAgIH0sCiAg
ICAgIHsKICAgICAgICJMMSI6IHsKICAgICAgICAiaiI6IDAsCiAgICAgICAgIm8yIjogMC41LAog
ICAgICAgICJvbWVnYSI6IDAuMDAzMDAxODYwMzYwNjQ1NjgyNAogICAgICAgfSwKICAgICAgICJQ
SCI6IHsKICAgICAgICAiaiI6IDIsCiAgICAgICAgIm9tZWdhIjogMC4wMDc3NjcxNTUwODE4Mzg2
OTgKICAgICAgIH0sCiAgICAgICAiVCI6IHsKICAgICAgICAiUjIiOiAxLjAsCiAgICAgICAgImoi
OiAxLAogICAgICAgICJvMiI6IDEuMCwKICAgICAgICAib21lZ2EiOiAwLjAwNDA1MTQ5MjIwODQz
NTkwNAogICAgICAgfSwKICAgICAgICJrYSI6IDAuMDAxMTcxODc1CiAgICAgIH0KICAgICBdLAog
ICAgICJHTSI6IFsKICAgICAgewogICAgICAgIkwxIjogewogICAgICAgICJqIjogMCwKICAgICAg
ICAibzIiOiAwLjUsCiAgICAgICAgIm9tZWdhIjogMC43Njg0NzQ2NDkxMDA5MzE2CiAgICAgICB9
LAogICAgICAgIlBIIjogewogICAgICAgICJqIjogMiwKICAgICAgICAib21lZ2EiOiAxLjk4NjUy
MDI4MDcyMTIwNwogICAgICAgfSwKICAgICAgICJUIjogewogICAgICAgICJSMiI6IDAuOTk5OTIs
CiAgICAgICAgImoiOiAxLAogICAgICAgICJvMiI6IDEuMCwKICAgICAgICAib21lZ2EiOiAxLjAz
NDk0NjkzNDIyNzU4ODUKICAgICAgIH0sCiAgICAgICAia2EiOiAwLjMKICAgICAgfSwKICAgICAg
ewogICAgICAgIkwxIjogewogICAgICAgICJqIjogMCwKICAgICAgICAibzIiOiAwLjUsCiAgICAg
ICAgIm9tZWdhIjogMC4zODQyNDIwNjM2NzM3OTMzCiAgICAgICB9LAogICAgICAgIlBIIjogewog
ICAgICAgICJqIjogMiwKICAgICAgICAib21lZ2EiOiAwLjk5Mzk2MjA0NzUyNTczNTEKICAgICAg
IH0sCiAgICAgICAiVCI6IHsKICAgICAgICAiUjIiOiAwLjk5OTk4LAogICAgICAgICJqIjogMSwK
ICAgICAgICAibzIiOiAxLjAsCiAgICAgICAgIm9tZWdhIjogMC41MTgyMDMxNTQyMTk2ODgyCiAg
ICAgICB9LAogICAgICAgImthIjogMC4xNQogICAgICB9LAogICAgICB7CiAgICAgICAiTDEiOiB7
CiAgICAgICAgImoiOiAwLAogICAgICAgICJvMiI6IDAuNSwKICAgICAgICAib21lZ2EiOiAwLjE5
MjExNzYwMzk2MTExMDM2CiAgICAgICB9LAogICAgICAgIlBIIjogewogICAgICAgICJqIjogMiwK
ICAgICAgICAib21lZ2EiOiAwLjQ5NzA2Nzc4NzU4MDIxODM2CiAgICAgICB9LAogICAgICAgIlQi
OiB7CiAgICAgICAgIlIyIjogMS4wLAogICAgICAgICJqIjogMSwKICAgICAgICAibzIiOiAxLjAs
CiAgICAgICAgIm9tZWdhIjogMC4yNTkxOTA3MTgyOTM2ODg3CiAgICAgICB9LAogICAgICAgImth
IjogMC4wNzUKICAgICAgfSwKICAgICAgewogICAgICAgIkwxIjogewogICAgICAgICJqIjogMCwK
ICAgICAgICAibzIiOiAwLjUsCiAgICAgICAgIm9tZWdhIjogMC4wOTYwNTgxMDcxMzg0MTYyNAog
ICAgICAgfSwKICAgICAgICJQSCI6IHsKICAgICAgICAiaiI6IDIsCiAgICAgICAgIm9tZWdhIjog
MC4yNDg1NDM0MDU1MTU3MDIyOAogICAgICAgfSwKICAgICAgICJUIjogewogICAgICAgICJSMiI6
IDEuMCwKICAgICAgICAiaiI6IDEsCiAgICAgICAgIm8yIjogMS4wLAogICAgICAgICJvbWVnYSI6
IDAuMTI5NjA1NTQ3Mjc4NjM5ODgKICAgICAgIH0sCiAgICAgICAia2EiOiAwLjAzNzUKICAgICAg
fSwKICAgICAgewogICAgICAgIkwxIjogewogICAgICAgICJqIjogMCwKICAgICAgICAibzIiOiAw
LjUsCiAgICAgICAgIm9tZWdhIjogMC4wNDgwMjg4OTI5NzAzNDY5MDQKICAgICAgIH0sCiAgICAg
ICAiUEgiOiB7CiAgICAgICAgImoiOiAyLAogICAgICAgICJvbWVnYSI6IDAuMTI0MjcyMjUyMjAw
MzQ5NjQKICAgICAgIH0sCiAgICAgICAiVCI6IHsKICAgICAgICAiUjIiOiAxLjAsCiAgICAgICAg
ImoiOiAxLAogICAgICAgICJvMiI6IDEuMCwKICAgICAgICAib21lZ2EiOiAwLjA2NDgwNDAyODAx
OTQ2MTExCiAgICAgICB9LAogICAgICAgImthIjogMC4wMTg3NQogICAgICB9LAogICAgICB7CiAg
ICAgICAiTDEiOiB7CiAgICAgICAgImoiOiAwLAogICAgICAgICJvMiI6IDAuNSwKICAgICAgICAi
b21lZ2EiOiAwLjAyNDAxNDQ0Mjk3OTA4Mzc3CiAgICAgICB9LAogICAgICAgIlBIIjogewogICAg
ICAgICJqIjogMiwKICAgICAgICAib21lZ2EiOiAwLjA2MjEzNjE3MTAyOTg2OTYyCiAgICAgICB9
LAogICAgICAgIlQiOiB7CiAgICAgICAgIlIyIjogMS4wLAogICAgICAgICJqIjogMSwKICAgICAg
ICAibzIiOiAxLjAsCiAgICAgICAgIm9tZWdhIjogMC4wMzI0MDIzNDEzNTA1Njg2NAogICAgICAg
fSwKICAgICAgICJrYSI6IDAuMDA5Mzc1CiAgICAgIH0sCiAgICAgIHsKICAgICAgICJMMSI6IHsK
ICAgICAgICAiaiI6IDAsCiAgICAgICAgIm8yIjogMC41LAogICAgICAgICJvbWVnYSI6IDAuMDEy
MDA3MjE5MzMzMTAxNzMzCiAgICAgICB9LAogICAgICAgIlBIIjogewogICAgICAgICJqIjogMiwK
ICAgICAgICAib21lZ2EiOiAwLjAzMTA2ODA5NzU1NDcwNzA2OAogICAgICAgfSwKICAgICAgICJU
IjogewogICAgICAgICJSMiI6IDEuMCwKICAgICAgICAiaiI6IDEsCiAgICAgICAgIm8yIjogMS4w
LAogICAgICAgICJvbWVnYSI6IDAuMDE2MjAxMjkzNjE2MzA3MDQKICAgICAgIH0sCiAgICAgICAi
a2EiOiAwLjAwNDY4NzUKICAgICAgfSwKICAgICAgewogICAgICAgIkwxIjogewogICAgICAgICJq
IjogMCwKICAgICAgICAibzIiOiAwLjUsCiAgICAgICAgIm9tZWdhIjogMC4wMDYwMDM1MzAyNTI1
Mjg2ODIKICAgICAgIH0sCiAgICAgICAiUEgiOiB7CiAgICAgICAgImoiOiAyLAogICAgICAgICJv
bWVnYSI6IDAuMDE1NTMzODA5MDA0NTE2MDgxCiAgICAgICB9LAogICAgICAgIlQiOiB7CiAgICAg
ICAgIlIyIjogMS4wLAogICAgICAgICJqIjogMSwKICAgICAgICAibzIiOiAxLjAsCiAgICAgICAg
Im9tZWdhIjogMC4wMDgxMDAzNzYyMTQ4OTIwMQogICAgICAgfSwKICAgICAgICJrYSI6IDAuMDAy
MzQzNzUKICAgICAgfSwKICAgICAgewogICAgICAgIkwxIjogewogICAgICAgICJqIjogMCwKICAg
ICAgICAibzIiOiAwLjUsCiAgICAgICAgIm9tZWdhIjogMC4wMDMwMDE2NDgzNTQzNjk5ODMKICAg
ICAgIH0sCiAgICAgICAiUEgiOiB7CiAgICAgICAgImoiOiAyLAogICAgICAgICJvbWVnYSI6IDAu
MDA3NzY2OTk5ODIyNTc5MDY2CiAgICAgICB9LAogICAgICAgIlQiOiB7CiAgICAgICAgIlIyIjog
MS4wLAogICAgICAgICJqIjogMSwKICAgICAgICAibzIiOiAxLjAsCiAgICAgICAgIm9tZWdhIjog
MC4wMDQwNTA1MTI5MzQxNzk2OTcKICAgICAgIH0sCiAgICAgICAia2EiOiAwLjAwMTE3MTg3NQog
ICAgICB9CiAgICAgXQogICAgfSwKICAgICJsYW1fbWluX0xfbWluIjogMC4wLAogICAgIm5fYiI6
IDMyLAogICAgInNwZWVkcyI6IHsKICAgICAiR0siOiB7CiAgICAgICJMMSI6IDMuNzQxMzY0MDU3
MDQ3MTI0LAogICAgICAiUEgiOiA5LjY4MDU5MzUwMzAyODgyNCwKICAgICAgIlJfVF9mcmFtZXdv
cmsiOiAwLjUyMTQ2OTkyNzE1ODg1OSwKICAgICAgIlQiOiA1LjA0ODEzODM4ODg3ODk2NCwKICAg
ICAgImNfTDFfZnJhbWV3b3JrIjogOS42ODA1OTM1MDMwMjg4MjQKICAgICB9LAogICAgICJHTSI6
IHsKICAgICAgIkwxIjogMy43NDEzNTMzNTQ2NTM5Mjk1LAogICAgICAiUEgiOiA5LjY4MDU5NDQ5
NTUyOTE2LAogICAgICAiUl9UX2ZyYW1ld29yayI6IDAuNTIxNDczOTY4NDk2MTI4LAogICAgICAi
VCI6IDUuMDQ4MTc4MDI4OTg1MzYzNSwKICAgICAgImNfTDFfZnJhbWV3b3JrIjogOS42ODA1OTQ0
OTU1MjkxNgogICAgIH0KICAgIH0sCiAgICAic3RlcDEiOiB7CiAgICAgIm1lYW5fcmhvIjogMC45
OTk5ODgxMjkyNDc0NDcyLAogICAgICJwc2kwX21kNSI6ICJiMjdmYTAwNDk1ZWY2ODZiMDE4NGVh
MjljNDU1YjRkYiIsCiAgICAgInJlc2lkdWFsX3JldmVyaWZpZWQiOiAxLjk1NTAyNTU3ODQyNjI5
MzRlLTEyLAogICAgICJzb3VyY2UiOiAiUGhhc2UtMSBpdGVtIDEgKGhhbHQgcmVwb3J0IGIwZTY3
OTBjKSIKICAgIH0sCiAgICAid2FyZCI6IHsKICAgICAiQTFfdGhyZXNob2xkX2FuYWx5dGljIjog
MWUtMDksCiAgICAgIkExX3RocmVzaG9sZF9oZXJtaXRpYW5fdzIiOiAxZS0wOCwKICAgICAiYnlf
bmIiOiB7CiAgICAgICIyNCI6IHsKICAgICAgICJhbmFseXRpY193YXJkX3Jlc2lkdWFsIjogewog
ICAgICAgICJkeCI6IDIuMjgxNzkyMDU3NDA2OTgxNmUtMTIsCiAgICAgICAgImR5IjogMy4xMDAy
MTA3NzgwNDY3MDFlLTEyCiAgICAgICB9LAogICAgICAgImhlcm1pdGlhbl9nb2xkc3RvbmVfYWJz
X3cyX21heCI6IDEuMjIyNTg5NTQxNjc2MzQwNWUtMDksCiAgICAgICAiaGVybWl0aWFuX3cyXzRs
b3dlc3QiOiBbCiAgICAgICAgLTcuMjU2MzcxMDExNTU1MjEyZS0xMCwKICAgICAgICAxLjkzNDE3
MTQ1Nzg1NTM5NDZlLTExLAogICAgICAgIDEuMjIyNTg5NTQxNjc2MzQwNWUtMDksCiAgICAgICAg
NzEuMjgyOTUwNDAxNTYyNDkKICAgICAgIF0sCiAgICAgICAibGFtYmRhX21pbl9MX0dhbW1hIjog
MS42MjYyNjU0MTc5ODM2NTY3ZS0xNCwKICAgICAgICJwYXNzX2EiOiB0cnVlLAogICAgICAgInBh
c3NfYiI6IHRydWUsCiAgICAgICAicHJvZHVjdF9mb3JtX2Fic193Ml9tYXhfeGNoZWNrIjogMi4x
MjQ4NzI5ODQwMzY1NDYyZS0wOQogICAgICB9LAogICAgICAiMzIiOiB7CiAgICAgICAiYW5hbHl0
aWNfd2FyZF9yZXNpZHVhbCI6IHsKICAgICAgICAiZHgiOiA2LjU3NzExOTUyODE0NjcyNGUtMTIs
CiAgICAgICAgImR5IjogMS4xMzMxMzI0MDM0NTU0NTU1ZS0xMQogICAgICAgfSwKICAgICAgICJo
ZXJtaXRpYW5fZ29sZHN0b25lX2Fic193Ml9tYXgiOiAzLjAxMTM3NTQzNzc2NDM1MzNlLTA5LAog
ICAgICAgImhlcm1pdGlhbl93Ml80bG93ZXN0IjogWwogICAgICAgIDMuNTA3MDg4MjI0Nzc4MDY3
ZS0xMCwKICAgICAgICA1LjY5MjI5NDE2NTU2NDYyM2UtMTAsCiAgICAgICAgMy4wMTEzNzU0Mzc3
NjQzNTMzZS0wOSwKICAgICAgICA3MS4yODI5NTA0MDMzMTgxOAogICAgICAgXSwKICAgICAgICJs
YW1iZGFfbWluX0xfR2FtbWEiOiAxLjU5MTIwNjIxNzYzNTU1MmUtMTQsCiAgICAgICAicGFzc19h
IjogdHJ1ZSwKICAgICAgICJwYXNzX2IiOiB0cnVlLAogICAgICAgInByb2R1Y3RfZm9ybV9hYnNf
dzJfbWF4X3hjaGVjayI6IDMuNDc2MTIzODUwNjc3ODI3ZS0wOAogICAgICB9LAogICAgICAiNDAi
OiB7CiAgICAgICAiYW5hbHl0aWNfd2FyZF9yZXNpZHVhbCI6IHsKICAgICAgICAiZHgiOiAxLjQx
Mjc0OTAzNDA5MTc3MjZlLTExLAogICAgICAgICJkeSI6IDIuMzA0NjEzMzIyNTYzOTQ5ZS0xMQog
ICAgICAgfSwKICAgICAgICJoZXJtaXRpYW5fZ29sZHN0b25lX2Fic193Ml9tYXgiOiA4LjEwODg2
MzE1Njg5NTIxZS0wOSwKICAgICAgICJoZXJtaXRpYW5fdzJfNGxvd2VzdCI6IFsKICAgICAgICAt
OC4xMDg4NjMxNTY4OTUyMWUtMDksCiAgICAgICAgLTEuMTczMTI0NjA4MjA1ODYxOGUtMDksCiAg
ICAgICAgLTYuMjc5MjUxMTA3ODQyMzQ0ZS0xMCwKICAgICAgICA3MS4yODI5NTAzOTcxMTU4Mwog
ICAgICAgXSwKICAgICAgICJsYW1iZGFfbWluX0xfR2FtbWEiOiAxLjY5MTQ0NzI3MDUzMjk4MTNl
LTE0LAogICAgICAgInBhc3NfYSI6IHRydWUsCiAgICAgICAicGFzc19iIjogdHJ1ZSwKICAgICAg
ICJwcm9kdWN0X2Zvcm1fYWJzX3cyX21heF94Y2hlY2siOiAzLjYyMDE0ODQzNjkxNjYyMmUtMDgK
ICAgICAgfQogICAgIH0sCiAgICAgImxhbWJkYV9taW5fTF9mbG9vciI6IC0xZS0xMiwKICAgICAi
cGFzc19hbGxfbmIiOiB0cnVlCiAgICB9LAogICAgInhjaGVja19wcm9kdWN0X3ZzX2hlcm1pdGlh
biI6IHsKICAgICAiR0tfa2E9MC4wMTg3IjogewogICAgICAiaGVybWl0aWFuIjogWwogICAgICAg
MC4wMDIzMDY3NzI5MzQzNTAyMDQsCiAgICAgICAwLjAwNDE5OTU4NDk1NTA0NDgxMSwKICAgICAg
IDAuMDE1NDQzNTYzOTE0Nzk3MDkxLAogICAgICAgNzEuMjkzMDgwMDQwMzcxMTIKICAgICAgXSwK
ICAgICAgInByb2R1Y3QiOiBbCiAgICAgICAwLjAwMjMwNjc5NzEyODM3MzMxODcsCiAgICAgICAw
LjAwNDE5OTU5NDc4NzI1NzU5MjUsCiAgICAgICAwLjAxNTQ0MzUyNDU4Mjg2ODI5OSwKICAgICAg
IDcxLjI5MzA4MDA0NjYyMzEzCiAgICAgIF0KICAgICB9LAogICAgICJHS19rYT0wLjMwMDAiOiB7
CiAgICAgICJoZXJtaXRpYW4iOiBbCiAgICAgICAwLjU5MDUxMTc0NjA1NjkwMDQsCiAgICAgICAx
LjA3MjU5ODIyOTIzNzQ1NzQsCiAgICAgICAzLjk0NDY3MzgwMzk5MzcwNzUsCiAgICAgICA3My44
NTQxMzU3OTE4NzAxNgogICAgICBdLAogICAgICAicHJvZHVjdCI6IFsKICAgICAgIDAuNTkwNTEx
NzI4Nzk2ODIzNywKICAgICAgIDEuMDcyNTk4MjMzOTAxMTg2LAogICAgICAgMy45NDQ2NzM4MTQw
OTQzNDM0LAogICAgICAgNzMuODU0MTM1ODA1NTExMTMKICAgICAgXQogICAgIH0sCiAgICAgIkdN
X2thPTAuMDE4NyI6IHsKICAgICAgImhlcm1pdGlhbiI6IFsKICAgICAgIDAuMDAyMzA2Nzc0NTU5
OTU3MDM4LAogICAgICAgMC4wMDQxOTk1NjIwNDc1NDcxLAogICAgICAgMC4wMTU0NDM1OTI2NjY5
NDczMDUsCiAgICAgICA3MS4yOTMwODAwNDIzMzQ4NgogICAgICBdLAogICAgICAicHJvZHVjdCI6
IFsKICAgICAgIDAuMDAyMzA2Njg3OTAxMjE5NzcsCiAgICAgICAwLjAwNDE5OTU1ODY4MTk1NTE2
MiwKICAgICAgIDAuMDE1NDQzNjcwODc0NzY5OTk3LAogICAgICAgNzEuMjkzMDgwMDU5Njc0MDcK
ICAgICAgXQogICAgIH0sCiAgICAgIkdNX2thPTAuMzAwMCI6IHsKICAgICAgImhlcm1pdGlhbiI6
IFsKICAgICAgIDAuNTkwNTUzMjg2MzEwOCwKICAgICAgIDEuMDcxMTE1MTU2NjY3MDg0NSwKICAg
ICAgIDMuOTQ2MjYyODI1NzE2NjYzNCwKICAgICAgIDczLjg1NDA5Mjk1ODg4NDg1CiAgICAgIF0s
CiAgICAgICJwcm9kdWN0IjogWwogICAgICAgMC41OTA1NTMzMTg2MDU4NTQ2LAogICAgICAgMS4w
NzExMTUxNTA2MjU2MjUsCiAgICAgICAzLjk0NjI2MjgwMDA4NzMxNDYsCiAgICAgICA3My44NTQw
OTI5NjE2OTYwNwogICAgICBdCiAgICAgfQogICAgfQogICB9LAogICAiNDAiOiB7CiAgICAiTDEi
OiB7CiAgICAgIkdLIjogewogICAgICAiYTIiOiAwLjAwMTM2NjY0NTU4MTg1Nzk3OCwKICAgICAg
ImE0IjogLTAuMDE3MTkzNTY3Nzc1ODg0NzYsCiAgICAgICJjaV9hMiI6IDAuMDAzNTUyNDY2NDYw
MTEzNDYyLAogICAgICAiY2lfYTQiOiAwLjUxNjA5ODc4NTkxMDg5NjEsCiAgICAgICJmaXRfcm1z
IjogMS41NzYxNzMwMTYzNzAxMTMyZS0wNSwKICAgICAgImthIjogWwogICAgICAgMC4zLAogICAg
ICAgMC4xNSwKICAgICAgIDAuMDc1LAogICAgICAgMC4wMzc1LAogICAgICAgMC4wMTg3NSwKICAg
ICAgIDAuMDA5Mzc1LAogICAgICAgMC4wMDQ2ODc1LAogICAgICAgMC4wMDIzNDM3NSwKICAgICAg
IDAuMDAxMTcxODc1CiAgICAgIF0sCiAgICAgICJyIjogWwogICAgICAgLTEuNjE5MTY4NDM1NTI5
MzM5ZS0wNSwKICAgICAgIDIuMDU1MTM1NTU3MzEwNjI3OGUtMDUsCiAgICAgICAxLjA4MjIxMjEw
Mzk3NTUyMTdlLTA1LAogICAgICAgNS4zNTMzNTI5ODgyMzU0NzFlLTA2LAogICAgICAgMy4wMzQx
MTk0MjYxNDg1MDdlLTA2LAogICAgICAgMy42MzI3NjY5MDU5NTg4MTc1ZS0wNiwKICAgICAgIC01
Ljg4MzIxNzM2Njk0MjA4NGUtMDYsCiAgICAgICAtMi4xMzA2MjAwNzcyNDUyOTMyZS0wNSwKICAg
ICAgIDQuMTIzMjg4NjI4MDQ0MDA4NGUtMDUKICAgICAgXQogICAgIH0sCiAgICAgIkdNIjogewog
ICAgICAiYTIiOiAwLjAwMTgxMjY3OTcwNzY4MzI0NjIsCiAgICAgICJhNCI6IC0wLjAxNzkwNTg1
MDM5NjQ3OTQ0NCwKICAgICAgImNpX2EyIjogMC4wMDI4MTQ3MDUwMDk2MjA1NTY4LAogICAgICAi
Y2lfYTQiOiAwLjQwNDAyOTA5NDc4NjA2NDY0LAogICAgICAiZml0X3JtcyI6IDMuNTc0MTM2NTcx
NDI3MDMzZS0wNSwKICAgICAgImthIjogWwogICAgICAgMC4zLAogICAgICAgMC4xNSwKICAgICAg
IDAuMDc1LAogICAgICAgMC4wMzc1LAogICAgICAgMC4wMTg3NSwKICAgICAgIDAuMDA5Mzc1LAog
ICAgICAgMC4wMDQ2ODc1LAogICAgICAgMC4wMDIzNDM3NSwKICAgICAgIDAuMDAxMTcxODc1CiAg
ICAgIF0sCiAgICAgICJyIjogWwogICAgICAgMS44MTY4MTQwNDczODM5ODU2ZS0wNSwKICAgICAg
IDMuMDQ4NzY0MTU1NDQ0NDE2N2UtMDUsCiAgICAgICAxLjI2OTAyMDIyMjA2MTEwMTNlLTA1LAog
ICAgICAgNS40NDQzNjE1NjkzNTExMzA1ZS0wNiwKICAgICAgIDIuMTY4NjM0MDQ0MzQxNjQ0ZS0w
NiwKICAgICAgIDMuNTY2NjE3MDc3MjMzMDQ3NGUtMDYsCiAgICAgICAtMS43NDI5Njg2MTAyMDc3
MjllLTA1LAogICAgICAgMS44OTYxOTMxNDk2MDg2NDkzZS0wNiwKICAgICAgIDAuMDAwMTA1NjE4
ODg4NjA0Mzg2MjkKICAgICAgXQogICAgIH0KICAgIH0sCiAgICAiVCI6IHsKICAgICAiR0siOiB7
CiAgICAgICJhMiI6IC0wLjAxMjgyMzg0ODU3MjE4OTYwNCwKICAgICAgImEyX2Zsb29yX3dlaWdo
dGVkIjogLTAuMDEyODM1MTQ1MzI4OTYzMjg1LAogICAgICAiYTQiOiAtMC4wMDI2ODIzNDk1MTMx
ODg5NDcsCiAgICAgICJhNF9mbG9vcl93ZWlnaHRlZCI6IC0wLjAwMjU1NjExNTU1Mjk2MDAwMjMs
CiAgICAgICJjaV9hMiI6IDAuMDA2NzU0OTA5ODg2NDIwMTU2LAogICAgICAiY2lfYTQiOiAxLjI4
NzcwNzQzOTg4ODUzMSwKICAgICAgImZpdF9ybXMiOiAwLjAwMDE2MzU3NTA3NDU2NDg0NzcsCiAg
ICAgICJmbG9vcl9zaWdtYV9yIjogWwogICAgICAgMy43ODAwMDk0OTYzOTgwODk1ZS0wOSwKICAg
ICAgIDEuNTA5MzI1NzQyMTA1ODQyNGUtMDgsCiAgICAgICA2LjAzNDY0MjAxOTYzNzU3M2UtMDgs
CiAgICAgICAyLjQxMzYxNjYyNDc1MDc4OWUtMDcsCiAgICAgICA5LjY1NDM2OTYwOTU3MDA0OWUt
MDcsCiAgICAgICAzLjg2MTcxNjc4OTU3Mzk5MTVlLTA2LAogICAgICAgMS41NDQ2MTEyODM0MDcy
OTY4ZS0wNSwKICAgICAgIDYuMTgxOTY2MzI4MjU4MjRlLTA1LAogICAgICAgMC4wMDAyNDczNDY0
NjA3NTQ4MDg4MwogICAgICBdLAogICAgICAia2EiOiBbCiAgICAgICAwLjMsCiAgICAgICAwLjE1
LAogICAgICAgMC4wNzUsCiAgICAgICAwLjAzNzUsCiAgICAgICAwLjAxODc1LAogICAgICAgMC4w
MDkzNzUsCiAgICAgICAwLjAwNDY4NzUsCiAgICAgICAwLjAwMjM0Mzc1LAogICAgICAgMC4wMDEx
NzE4NzUKICAgICAgXSwKICAgICAgInIiOiBbCiAgICAgICAtMC4wMDExNzU4Njc0NjMwNDY0MzE2
LAogICAgICAgLTAuMDAwMjkwMTMzNTc0NjIzODE4NywKICAgICAgIC02Ljk3NDkwMzc5MDMxMzI5
MmUtMDUsCiAgICAgICAtMS45OTk3ODkzNzcwODI4OTQ1ZS0wNSwKICAgICAgIC0xLjQ5ODAxMDA5
ODA4ODgwOWUtMDUsCiAgICAgICAtMS4wOTU5Mzg1ODMwNzMzMzA0ZS0wNSwKICAgICAgIDEuMzQ1
Nzk3OTA3NDQ4MjY1MWUtMDUsCiAgICAgICAtMC4wMDAyNzEzODIxMDE3NjExNDE3NSwKICAgICAg
IC0wLjAwMDQwODQyNDQyOTA5NTI3NzY1CiAgICAgIF0KICAgICB9LAogICAgICJHTSI6IHsKICAg
ICAgImEyIjogLTAuMDE5Mzg3Nzk5MDc4NDE2Mjk1LAogICAgICAiYTJfZmxvb3Jfd2VpZ2h0ZWQi
OiAtMC4wMTk1NDk2ODcyOTcwMzcxMiwKICAgICAgImE0IjogLTAuMDEzNDA1ODYyMTQ3ODQxNzYy
LAogICAgICAiYTRfZmxvb3Jfd2VpZ2h0ZWQiOiAtMC4wMTE1ODg3NjYwNzQwMzcxMjQsCiAgICAg
ICJjaV9hMiI6IDAuMDA0MzYwMzc3MTU3MjEzNTM5LAogICAgICAiY2lfYTQiOiAwLjUyNzk1MjYy
MTcyMjE0OTEsCiAgICAgICJmaXRfcm1zIjogMC4wMDAzNjU5ODIwNTE3Mjc3ODEzNCwKICAgICAg
ImZsb29yX3NpZ21hX3IiOiBbCiAgICAgICAzLjc4NTI0MzQzNTYzMTU5M2UtMDksCiAgICAgICAx
LjUwOTgzNjQ5MTQ3MzM0NGUtMDgsCiAgICAgICA2LjAzNTE4Nzc4NDEzNDMwNmUtMDgsCiAgICAg
ICAyLjQxMzY5NTA4OTMzMzYyOWUtMDcsCiAgICAgICA5LjY1NDQwNDc3Njg5NjcyZS0wNywKICAg
ICAgIDMuODYxNjQ1ODE1NTU1ODM3ZS0wNiwKICAgICAgIDEuNTQ0NTkxOTMyNjIxMzUzZS0wNSwK
ICAgICAgIDYuMTc5MjU4MjE0Njc2Mzg0ZS0wNSwKICAgICAgIDAuMDAwMjQ3Njk0MDE4MzQwNDQ3
MQogICAgICBdLAogICAgICAia2EiOiBbCiAgICAgICAwLjMsCiAgICAgICAwLjE1LAogICAgICAg
MC4wNzUsCiAgICAgICAwLjAzNzUsCiAgICAgICAwLjAxODc1LAogICAgICAgMC4wMDkzNzUsCiAg
ICAgICAwLjAwNDY4NzUsCiAgICAgICAwLjAwMjM0Mzc1LAogICAgICAgMC4wMDExNzE4NzUKICAg
ICAgXSwKICAgICAgInIiOiBbCiAgICAgICAtMC4wMDE4NTMzNDAzMjEwNDEyMzAzLAogICAgICAg
LTAuMDAwNDQ1OTA2NjAzOTE4NjMzMjQsCiAgICAgICAtMC4wMDAxMDE2MjQ2OTYxNDA3MjMsCiAg
ICAgICAtMi4yOTEzMjc0MzA5MTQ0MjVlLTA1LAogICAgICAgLTMuNDYyNjYxNDQ5MjM4MzQ2N2Ut
MDYsCiAgICAgICAxLjE1NjkwMDMwMDg0NzE0MTJlLTA1LAogICAgICAgMy4zMDYxMjk5NTIzNjI5
MDJlLTA1LAogICAgICAgLTMuODk5Nzk3NDA2MzU5MjYyZS0wNSwKICAgICAgIC0wLjAwMTA5NjY0
NjQ4MDE1NDI4NDEKICAgICAgXQogICAgIH0KICAgIH0sCiAgICAiZm1peF9taW5fbzJfVCI6IHsK
ICAgICAiR0siOiAwLjk5OTk5OTk5MzY5ODg2OTYsCiAgICAgIkdNIjogMC45OTk5OTk5Nzc1ODA5
NTU2CiAgICB9LAogICAgImlkZW50IjogewogICAgICJHSyI6IFsKICAgICAgewogICAgICAgIkwx
IjogewogICAgICAgICJqIjogMCwKICAgICAgICAibzIiOiAwLjUsCiAgICAgICAgIm9tZWdhIjog
MC43Njg0NDc2MjM0ODAzOTQKICAgICAgIH0sCiAgICAgICAiUEgiOiB7CiAgICAgICAgImoiOiAy
LAogICAgICAgICJvbWVnYSI6IDEuOTg2MTIwMjkwNzc3NDQwNQogICAgICAgfSwKICAgICAgICJU
IjogewogICAgICAgICJSMiI6IDAuOTk5OTMsCiAgICAgICAgImoiOiAxLAogICAgICAgICJvMiI6
IDEuMCwKICAgICAgICAib21lZ2EiOiAxLjAzNTY2MzE5NDI5NTI3MjUKICAgICAgIH0sCiAgICAg
ICAia2EiOiAwLjMKICAgICAgfSwKICAgICAgewogICAgICAgIkwxIjogewogICAgICAgICJqIjog
MCwKICAgICAgICAibzIiOiAwLjUsCiAgICAgICAgIm9tZWdhIjogMC4zODQyMzc5Mjk1MTk2NDM4
CiAgICAgICB9LAogICAgICAgIlBIIjogewogICAgICAgICJqIjogMiwKICAgICAgICAib21lZ2Ei
OiAwLjk5MzkxNjY4MzA1MzkwNjUKICAgICAgIH0sCiAgICAgICAiVCI6IHsKICAgICAgICAiUjIi
OiAwLjk5OTk4LAogICAgICAgICJqIjogMSwKICAgICAgICAibzIiOiAxLjAsCiAgICAgICAgIm9t
ZWdhIjogMC41MTgyOTA3OTgxMDExODYyCiAgICAgICB9LAogICAgICAgImthIjogMC4xNQogICAg
ICB9LAogICAgICB7CiAgICAgICAiTDEiOiB7CiAgICAgICAgImoiOiAwLAogICAgICAgICJvMiI6
IDAuNSwKICAgICAgICAib21lZ2EiOiAwLjE5MjExNzA5NTYyNzc2ODY2CiAgICAgICB9LAogICAg
ICAgIlBIIjogewogICAgICAgICJqIjogMiwKICAgICAgICAib21lZ2EiOiAwLjQ5NzA2MjQ0OTQx
MDAzOTkKICAgICAgIH0sCiAgICAgICAiVCI6IHsKICAgICAgICAiUjIiOiAxLjAsCiAgICAgICAg
ImoiOiAxLAogICAgICAgICJvMiI6IDEuMCwKICAgICAgICAib21lZ2EiOiAwLjI1OTIwMjUyNzI2
NDExODk2CiAgICAgICB9LAogICAgICAgImthIjogMC4wNzUKICAgICAgfSwKICAgICAgewogICAg
ICAgIkwxIjogewogICAgICAgICJqIjogMCwKICAgICAgICAibzIiOiAwLjUsCiAgICAgICAgIm9t
ZWdhIjogMC4wOTYwNTgwMjI0OTc2NTIKICAgICAgIH0sCiAgICAgICAiUEgiOiB7CiAgICAgICAg
ImoiOiAyLAogICAgICAgICJvbWVnYSI6IDAuMjQ4NTQyNTE3ODY3MDkwMDYKICAgICAgIH0sCiAg
ICAgICAiVCI6IHsKICAgICAgICAiUjIiOiAxLjAsCiAgICAgICAgImoiOiAxLAogICAgICAgICJv
MiI6IDEuMCwKICAgICAgICAib21lZ2EiOiAwLjEyOTYwNzcxMTg5Mjk2NjE2CiAgICAgICB9LAog
ICAgICAgImthIjogMC4wMzc1CiAgICAgIH0sCiAgICAgIHsKICAgICAgICJMMSI6IHsKICAgICAg
ICAiaiI6IDAsCiAgICAgICAgIm8yIjogMC41LAogICAgICAgICJvbWVnYSI6IDAuMDQ4MDI4ODk5
ODU4OTI3NDY0CiAgICAgICB9LAogICAgICAgIlBIIjogewogICAgICAgICJqIjogMiwKICAgICAg
ICAib21lZ2EiOiAwLjEyNDI3MjEyNDAxMTU3MzUzCiAgICAgICB9LAogICAgICAgIlQiOiB7CiAg
ICAgICAgIlIyIjogMS4wLAogICAgICAgICJqIjogMSwKICAgICAgICAibzIiOiAxLjAsCiAgICAg
ICAgIm9tZWdhIjogMC4wNjQ4MDQxODExMjUzMDcxCiAgICAgICB9LAogICAgICAgImthIjogMC4w
MTg3NQogICAgICB9LAogICAgICB7CiAgICAgICAiTDEiOiB7CiAgICAgICAgImoiOiAwLAogICAg
ICAgICJvMiI6IDAuNSwKICAgICAgICAib21lZ2EiOiAwLjAyNDAxNDQ2NDMwNTYxMDA0MwogICAg
ICAgfSwKICAgICAgICJQSCI6IHsKICAgICAgICAiaiI6IDIsCiAgICAgICAgIm9tZWdhIjogMC4w
NjIxMzYxNDIwMTk4MjU1OAogICAgICAgfSwKICAgICAgICJUIjogewogICAgICAgICJSMiI6IDEu
MCwKICAgICAgICAiaiI6IDEsCiAgICAgICAgIm8yIjogMS4wLAogICAgICAgICJvbWVnYSI6IDAu
MDMyNDAyMjIwODQ0MTgxNgogICAgICAgfSwKICAgICAgICJrYSI6IDAuMDA5Mzc1CiAgICAgIH0s
CiAgICAgIHsKICAgICAgICJMMSI6IHsKICAgICAgICAiaiI6IDAsCiAgICAgICAgIm8yIjogMC41
LAogICAgICAgICJvbWVnYSI6IDAuMDEyMDA3MTE3ODkyNTg3Nzc2CiAgICAgICB9LAogICAgICAg
IlBIIjogewogICAgICAgICJqIjogMiwKICAgICAgICAib21lZ2EiOiAwLjAzMTA2Nzc1MDI3MTk3
NTE2CiAgICAgICB9LAogICAgICAgIlQiOiB7CiAgICAgICAgIlIyIjogMS4wLAogICAgICAgICJq
IjogMSwKICAgICAgICAibzIiOiAxLjAsCiAgICAgICAgIm9tZWdhIjogMC4wMTYyMDE1MDYwMTQ4
NTEzCiAgICAgICB9LAogICAgICAgImthIjogMC4wMDQ2ODc1CiAgICAgIH0sCiAgICAgIHsKICAg
ICAgICJMMSI6IHsKICAgICAgICAiaiI6IDAsCiAgICAgICAgIm8yIjogMC41LAogICAgICAgICJv
bWVnYSI6IDAuMDA2MDAzNDY2MzUyOTU5MTM4CiAgICAgICB9LAogICAgICAgIlBIIjogewogICAg
ICAgICJqIjogMiwKICAgICAgICAib21lZ2EiOiAwLjAxNTUzMzY5NDc1MDc1ODM2OAogICAgICAg
fSwKICAgICAgICJUIjogewogICAgICAgICJSMiI6IDEuMCwKICAgICAgICAiaiI6IDEsCiAgICAg
ICAgIm8yIjogMS4wLAogICAgICAgICJvbWVnYSI6IDAuMDA4MDk4NDQ1NjE5MzM2OTY2CiAgICAg
ICB9LAogICAgICAgImthIjogMC4wMDIzNDM3NQogICAgICB9LAogICAgICB7CiAgICAgICAiTDEi
OiB7CiAgICAgICAgImoiOiAwLAogICAgICAgICJvMiI6IDAuNTAwMDIsCiAgICAgICAgIm9tZWdh
IjogMC4wMDMwMDE5MjA5MDYxMzE4MDg0CiAgICAgICB9LAogICAgICAgIlBIIjogewogICAgICAg
ICJqIjogMiwKICAgICAgICAib21lZ2EiOiAwLjAwNzc2Njc5NDg1OTM5ODY3MQogICAgICAgfSwK
ICAgICAgICJUIjogewogICAgICAgICJSMiI6IDEuMCwKICAgICAgICAiaiI6IDEsCiAgICAgICAg
Im8yIjogMS4wLAogICAgICAgICJvbWVnYSI6IDAuMDA0MDQ4NjY3NzQ0MTE1ODk1CiAgICAgICB9
LAogICAgICAgImthIjogMC4wMDExNzE4NzUKICAgICAgfQogICAgIF0sCiAgICAgIkdNIjogWwog
ICAgICB7CiAgICAgICAiTDEiOiB7CiAgICAgICAgImoiOiAwLAogICAgICAgICJvMiI6IDAuNSwK
ICAgICAgICAib21lZ2EiOiAwLjc2ODQ3NDY1MTM0MjA3MwogICAgICAgfSwKICAgICAgICJQSCI6
IHsKICAgICAgICAiaiI6IDIsCiAgICAgICAgIm9tZWdhIjogMS45ODY1MjAyNzkyNjUyODEyCiAg
ICAgICB9LAogICAgICAgIlQiOiB7CiAgICAgICAgIlIyIjogMC45OTk5MiwKICAgICAgICAiaiI6
IDEsCiAgICAgICAgIm8yIjogMS4wLAogICAgICAgICJvbWVnYSI6IDEuMDM0OTQ2OTI5NDg4Mzc1
NQogICAgICAgfSwKICAgICAgICJrYSI6IDAuMwogICAgICB9LAogICAgICB7CiAgICAgICAiTDEi
OiB7CiAgICAgICAgImoiOiAwLAogICAgICAgICJvMiI6IDAuNSwKICAgICAgICAib21lZ2EiOiAw
LjM4NDI0MjA1OTE5NzE4NgogICAgICAgfSwKICAgICAgICJQSCI6IHsKICAgICAgICAiaiI6IDIs
CiAgICAgICAgIm9tZWdhIjogMC45OTM5NjIwNDU1OTI2NDcyCiAgICAgICB9LAogICAgICAgIlQi
OiB7CiAgICAgICAgIlIyIjogMC45OTk5OCwKICAgICAgICAiaiI6IDEsCiAgICAgICAgIm8yIjog
MS4wLAogICAgICAgICJvbWVnYSI6IDAuNTE4MjAzMTI2NjU4MDMwNgogICAgICAgfSwKICAgICAg
ICJrYSI6IDAuMTUKICAgICAgfSwKICAgICAgewogICAgICAgIkwxIjogewogICAgICAgICJqIjog
MCwKICAgICAgICAibzIiOiAwLjUsCiAgICAgICAgIm9tZWdhIjogMC4xOTIxMTc2MTA0NDA0NjYw
MgogICAgICAgfSwKICAgICAgICJQSCI6IHsKICAgICAgICAiaiI6IDIsCiAgICAgICAgIm9tZWdh
IjogMC40OTcwNjc4MTk4OTg2MjQ1MwogICAgICAgfSwKICAgICAgICJUIjogewogICAgICAgICJS
MiI6IDEuMCwKICAgICAgICAiaiI6IDEsCiAgICAgICAgIm8yIjogMS4wLAogICAgICAgICJvbWVn
YSI6IDAuMjU5MTkwODA3MTAzOTM1MDUKICAgICAgIH0sCiAgICAgICAia2EiOiAwLjA3NQogICAg
ICB9LAogICAgICB7CiAgICAgICAiTDEiOiB7CiAgICAgICAgImoiOiAwLAogICAgICAgICJvMiI6
IDAuNSwKICAgICAgICAib21lZ2EiOiAwLjA5NjA1ODEwOTIwMjI2OTg0CiAgICAgICB9LAogICAg
ICAgIlBIIjogewogICAgICAgICJqIjogMiwKICAgICAgICAib21lZ2EiOiAwLjI0ODU0MzQwMDEw
MDg1MjYzCiAgICAgICB9LAogICAgICAgIlQiOiB7CiAgICAgICAgIlIyIjogMS4wLAogICAgICAg
ICJqIjogMSwKICAgICAgICAibzIiOiAxLjAsCiAgICAgICAgIm9tZWdhIjogMC4xMjk2MDU2MDUy
MjcxODYxCiAgICAgICB9LAogICAgICAgImthIjogMC4wMzc1CiAgICAgIH0sCiAgICAgIHsKICAg
ICAgICJMMSI6IHsKICAgICAgICAiaiI6IDAsCiAgICAgICAgIm8yIjogMC41LAogICAgICAgICJv
bWVnYSI6IDAuMDQ4MDI4ODk3MjcxODk1MzIKICAgICAgIH0sCiAgICAgICAiUEgiOiB7CiAgICAg
ICAgImoiOiAyLAogICAgICAgICJvbWVnYSI6IDAuMTI0MjcyMzUxNzE1NjA0OTgKICAgICAgIH0s
CiAgICAgICAiVCI6IHsKICAgICAgICAiUjIiOiAxLjAsCiAgICAgICAgImoiOiAxLAogICAgICAg
ICJvMiI6IDEuMCwKICAgICAgICAib21lZ2EiOiAwLjA2NDgwNDA2MzA5NjcwMDcxCiAgICAgICB9
LAogICAgICAgImthIjogMC4wMTg3NQogICAgICB9LAogICAgICB7CiAgICAgICAiTDEiOiB7CiAg
ICAgICAgImoiOiAwLAogICAgICAgICJvMiI6IDAuNSwKICAgICAgICAib21lZ2EiOiAwLjAyNDAx
NDQ4MjIwNzY2NjU5MgogICAgICAgfSwKICAgICAgICJQSCI6IHsKICAgICAgICAiaiI6IDIsCiAg
ICAgICAgIm9tZWdhIjogMC4wNjIxMzYyNDM0NTkzMTU1NgogICAgICAgfSwKICAgICAgICJUIjog
ewogICAgICAgICJSMiI6IDEuMCwKICAgICAgICAiaiI6IDEsCiAgICAgICAgIm8yIjogMS4wLAog
ICAgICAgICJvbWVnYSI6IDAuMDMyNDAyNTE4NjA2NTAyODUKICAgICAgIH0sCiAgICAgICAia2Ei
OiAwLjAwOTM3NQogICAgICB9LAogICAgICB7CiAgICAgICAiTDEiOiB7CiAgICAgICAgImoiOiAw
LAogICAgICAgICJvMiI6IDAuNSwKICAgICAgICAib21lZ2EiOiAwLjAxMjAwNjk4ODk5NzA1Nzkw
MwogICAgICAgfSwKICAgICAgICJQSCI6IHsKICAgICAgICAiaiI6IDIsCiAgICAgICAgIm9tZWdh
IjogMC4wMzEwNjg2NjA0MjMzODc5ODIKICAgICAgIH0sCiAgICAgICAiVCI6IHsKICAgICAgICAi
UjIiOiAxLjAsCiAgICAgICAgImoiOiAxLAogICAgICAgICJvMiI6IDEuMCwKICAgICAgICAib21l
Z2EiOiAwLjAxNjIwMTYwNzUwMTQ5MTk4NwogICAgICAgfSwKICAgICAgICJrYSI6IDAuMDA0Njg3
NQogICAgICB9LAogICAgICB7CiAgICAgICAiTDEiOiB7CiAgICAgICAgImoiOiAwLAogICAgICAg
ICJvMiI6IDAuNSwKICAgICAgICAib21lZ2EiOiAwLjAwNjAwMzYxMDUyMzM2MDk5NAogICAgICAg
fSwKICAgICAgICJQSCI6IHsKICAgICAgICAiaiI6IDIsCiAgICAgICAgIm9tZWdhIjogMC4wMTU1
MzQ0NDgzMjU1MDgwNDkKICAgICAgIH0sCiAgICAgICAiVCI6IHsKICAgICAgICAiUjIiOiAxLjAs
CiAgICAgICAgImoiOiAxLAogICAgICAgICJvMiI6IDEuMCwKICAgICAgICAib21lZ2EiOiAwLjAw
ODEwMDIyMDAzMjAxMDc0MQogICAgICAgfSwKICAgICAgICJrYSI6IDAuMDAyMzQzNzUKICAgICAg
fSwKICAgICAgewogICAgICAgIkwxIjogewogICAgICAgICJqIjogMCwKICAgICAgICAibzIiOiAw
LjUwMDExLAogICAgICAgICJvbWVnYSI6IDAuMDAzMDAyMTE2NjE2NDIzMDgKICAgICAgIH0sCiAg
ICAgICAiUEgiOiB7CiAgICAgICAgImoiOiAyLAogICAgICAgICJvbWVnYSI6IDAuMDA3NzY4OTMw
MDU5NDYzNjMzCiAgICAgICB9LAogICAgICAgIlQiOiB7CiAgICAgICAgIlIyIjogMS4wLAogICAg
ICAgICJqIjogMSwKICAgICAgICAibzIiOiAxLjAsCiAgICAgICAgIm9tZWdhIjogMC4wMDQwNDU4
MjYyNTYxMzk0ODM1CiAgICAgICB9LAogICAgICAgImthIjogMC4wMDExNzE4NzUKICAgICAgfQog
ICAgIF0KICAgIH0sCiAgICAibGFtX21pbl9MX21pbiI6IDAuMCwKICAgICJuX2IiOiA0MCwKICAg
ICJzcGVlZHMiOiB7CiAgICAgIkdLIjogewogICAgICAiTDEiOiAzLjc0MTM1MDI5MzM2MDQ0MTQs
CiAgICAgICJQSCI6IDkuNjgwNTQ2ODgxNDU3MDE1LAogICAgICAiUl9UX2ZyYW1ld29yayI6IDAu
NTIxNDc4ODQwNjMwMTM2NCwKICAgICAgIlQiOiA1LjA0ODIwMDM2NDQwNzg4NjYsCiAgICAgICJj
X0wxX2ZyYW1ld29yayI6IDkuNjgwNTQ2ODgxNDU3MDE1CiAgICAgfSwKICAgICAiR00iOiB7CiAg
ICAgICJMMSI6IDMuNzQxMzUzMzI5OTEyODY4NywKICAgICAgIlBIIjogOS42ODA1OTQ4NzIwODg4
MzIsCiAgICAgICJSX1RfZnJhbWV3b3JrIjogMC41MjE0NjkyOTk1OTYzNDgyLAogICAgICAiVCI6
IDUuMDQ4MTMzMDI3NjI0MTYzLAogICAgICAiY19MMV9mcmFtZXdvcmsiOiA5LjY4MDU5NDg3MjA4
ODgzMgogICAgIH0KICAgIH0sCiAgICAieGNoZWNrX3Byb2R1Y3RfdnNfaGVybWl0aWFuIjogewog
ICAgICJHS19rYT0wLjAxODciOiB7CiAgICAgICJoZXJtaXRpYW4iOiBbCiAgICAgICAwLjAwMjMw
Njc3NTIyMTY1ODg4MjMsCiAgICAgICAwLjAwNDE5OTU4MTg5MTMyMTYwOSwKICAgICAgIDAuMDE1
NDQzNTYwODA2MzQ3OTEsCiAgICAgICA3MS4yOTMwODAwNDc2NzY0NwogICAgICBdLAogICAgICAi
cHJvZHVjdCI6IFsKICAgICAgIDAuMDAyMzA2Njk3NjkzMTg3MDM3NiwKICAgICAgIDAuMDA0MTk5
NTg2MzcxNDc4MDMsCiAgICAgICAwLjAxNTQ0MzU4ODAxMjQ3NTQxNCwKICAgICAgIDcxLjI5MzA4
MDE0NjI5MDEKICAgICAgXQogICAgIH0sCiAgICAgIkdLX2thPTAuMzAwMCI6IHsKICAgICAgImhl
cm1pdGlhbiI6IFsKICAgICAgIDAuNTkwNTExNzUwMDMyNjY1MywKICAgICAgIDEuMDcyNTk4MjUy
MDE3ODg3NCwKICAgICAgIDMuOTQ0NjczODA5NDM3ODY1LAogICAgICAgNzMuODU0MTM1ODAyMzE5
MTkKICAgICAgXSwKICAgICAgInByb2R1Y3QiOiBbCiAgICAgICAwLjU5MDUxMTc3ODI4NzQzMjcs
CiAgICAgICAxLjA3MjU5ODIzMjgzMDQ1ODQsCiAgICAgICAzLjk0NDY3MzgxNjM0OTI4NCwKICAg
ICAgIDczLjg1NDEzNTgyMjA1MTg0CiAgICAgIF0KICAgICB9LAogICAgICJHTV9rYT0wLjAxODci
OiB7CiAgICAgICJoZXJtaXRpYW4iOiBbCiAgICAgICAwLjAwMjMwNjc3NDk3MzE1NDI3NCwKICAg
ICAgIDAuMDA0MTk5NTY2NTkzODQxMTY3LAogICAgICAgMC4wMTU0NDM2MTc0MDA5MjcwMywKICAg
ICAgIDcxLjI5MzA4MDA0MDgzMDYKICAgICAgXSwKICAgICAgInByb2R1Y3QiOiBbCiAgICAgICAw
LjAwMjMwNjY2ODk0NzUxNjkzMDQsCiAgICAgICAwLjAwNDE5OTU1NzgyODIzMjM2OCwKICAgICAg
IDAuMDE1NDQzNzM0MzE4NDE4NDQyLAogICAgICAgNzEuMjkzMDgwMDU2NjUxMzkKICAgICAgXQog
ICAgIH0sCiAgICAgIkdNX2thPTAuMzAwMCI6IHsKICAgICAgImhlcm1pdGlhbiI6IFsKICAgICAg
IDAuNTkwNTUzMjg5NzU1MzIwNywKICAgICAgIDEuMDcxMTE1MTQ2ODU3NDE2NywKICAgICAgIDMu
OTQ2MjYyODE5OTMyMjEwNSwKICAgICAgIDczLjg1NDA5Mjk2ODQxNDIKICAgICAgXSwKICAgICAg
InByb2R1Y3QiOiBbCiAgICAgICAwLjU5MDU1MzI4MDI5NzA2MjksCiAgICAgICAxLjA3MTExNTE1
NzE5MjUxNDgsCiAgICAgICAzLjk0NjI2MjgwNjMxNjUwMzcsCiAgICAgICA3My44NTQwOTI5ODcw
MDMwNgogICAgICBdCiAgICAgfQogICAgfQogICB9CiAgfSwKICAic3BlZWRfa2EiOiBbCiAgIDAu
MDA1LAogICAwLjAxLAogICAwLjAxNSwKICAgMC4wMiwKICAgMC4wMwogIF0KIH0sCiAic3Vic3Ry
YXRlIjogewogICJhX3N0YXIiOiAxLjQ2MDU5LAogICJnIjogMjAuMCwKICAiZ3JpZF9uIjogNjQs
CiAgImtlcm5lbCI6ICJHRU0tOCBnIGV4cCgtcl44KSwgMi1EIiwKICAia2VybmVsX1UwIjogNTYu
OTUwOTQ3MjYyMjYxNTYsCiAgIm11IjogNTMuMjI1CiB9LAogInQxX21kNSI6ICI4Y2Q4OWI5YTgy
NzA0YWNjZDg5ZjdmZjZmNWUyMjBiNCIsCiAidGF1IjogMWUtMDYsCiAidGhldGFfaWQiOiAwLjks
CiAidGhldGFfaXNvIjogMC4wMSwKICJ2ZXJkaWN0IjogIk5PVCBERUNMQVJFRCBcdTIwMTQgdHdv
LWxlZyAoQ0MpIGNvbXBhcmlzb24gYW5kIFBoYXNlIDIvMyAoYWdncmVnYXRlKSBwZW5kaW5nOyBj
aGF0LWxlZyBzaW5nbGUtY3J5c3RhbCBJTkRJQ0FUSU9OIG9ubHkiCn0K
<<<EMBED-END name=g_s2c1_phase1_ladder_checkpoint.json>>>

### EMBED — chat diagnostic analysis — `s2c1_phase1_ladder_analysis.json` (md5 bdfd3d01bc3f4cef0e22232bb7ff7eb5, 6507 B, b64, QUARANTINED)

<<<EMBED-BEGIN name=s2c1_phase1_ladder_analysis.json md5=bdfd3d01bc3f4cef0e22232bb7ff7eb5 bytes=6507 enc=b64 quarantine=1>>>
ewogImVzdGltYXRvciI6ICJESUFHTk9TVElDIGpvaW50IGZpdCAoYyBmcmVlKTsgdGhlIGVsZWN0
ZWQgZXN0aW1hdG9yJ3MgdmFsdWVzIGFyZSBpbiB0aGUgY2hlY2twb2ludCIsCiAicGVyX2RpcmVj
dGlvbiI6IHsKICAiR0siOiB7CiAgICJhMl9mbG9vcl9jbGVhbl9uYjQwIjogLTAuMDEyNzk0MTYx
NTMwNzkyNzYsCiAgICJhMl9mbG9vcl9jbGVhbl9yZWxfZHJpZnQiOiB7CiAgICAiMjR2MzIiOiAw
LjAwMDExODY2NTUyOTY4OTQwODM5LAogICAgIjMydjQwIjogMC4wMDMwMDI3NTg3MTkzNTc1OTcz
CiAgIH0sCiAgICJhNF9mbG9vcl9jbGVhbl9uYjQwIjogLTAuMDAyOTk4NDE5Nzc1NTQ3ODA0NCwK
ICAgImNfVF9mbG9vcl9jbGVhbl9uYjQwIjogNS4wNDgxOTk2ODI3NjU0MjIsCiAgICJqb2ludF9m
aXQiOiB7CiAgICAibmIyNF9hbGxfcnVuZ3MiOiB7CiAgICAgImEyIjogLTAuMDExNzYwNzQzOTEx
MjMzODExLAogICAgICJhNCI6IC0wLjAxMjc0OTU1NDEwNTI1NzM3OSwKICAgICAiY19UIjogNS4w
NDgxMjc2NjAyMTQ5MTcsCiAgICAgIm5fcnVuZ3MiOiA5CiAgICB9LAogICAgIm5iMjRfZmxvb3Jf
Y2xlYW5fcnVuZ3Nfa2FfZ2VfMC4wMzc1IjogewogICAgICJhMiI6IC0wLjAxMjc1NzI1NzQxNzc4
ODA2MiwKICAgICAiYTQiOiAtMC4wMDMzNjMxOTc3MjEwNTYwODI1LAogICAgICJjX1QiOiA1LjA0
ODE5NzY5NzY4NDUyMSwKICAgICAibl9ydW5ncyI6IDQKICAgIH0sCiAgICAibmIzMl9hbGxfcnVu
Z3MiOiB7CiAgICAgImEyIjogLTAuMDE2NTA4OTI2MDU3MDEzOTMyLAogICAgICJhNCI6IDAuMDMy
MDk4MTY5NDc1MTgyMTUsCiAgICAgImNfVCI6IDUuMDQ4NDU2NjIwNTAzNDc0LAogICAgICJuX3J1
bmdzIjogOQogICAgfSwKICAgICJuYjMyX2Zsb29yX2NsZWFuX3J1bmdzX2thX2dlXzAuMDM3NSI6
IHsKICAgICAiYTIiOiAtMC4wMTI3NTU3NDM3NTA2OTkzMDMsCiAgICAgImE0IjogLTAuMDAzMzc3
MzYyODM5NDMxMTQ0LAogICAgICJjX1QiOiA1LjA0ODE5NzU4NDk1NDM1LAogICAgICJuX3J1bmdz
IjogNAogICAgfSwKICAgICJuYjQwX2FsbF9ydW5ncyI6IHsKICAgICAiYTIiOiAtMC4wMDQ3NTY2
OTM0NjEzODQxMTQsCiAgICAgImE0IjogLTAuMDc4ODg1NTU2MDMwOTMxNCwKICAgICAiY19UIjog
NS4wNDc2NDE4MDc3NzM4MDUsCiAgICAgIm5fcnVuZ3MiOiA5CiAgICB9LAogICAgIm5iNDBfZmxv
b3JfY2xlYW5fcnVuZ3Nfa2FfZ2VfMC4wMzc1IjogewogICAgICJhMiI6IC0wLjAxMjc5NDE2MTUz
MDc5Mjc2LAogICAgICJhNCI6IC0wLjAwMjk5ODQxOTc3NTU0NzgwNDQsCiAgICAgImNfVCI6IDUu
MDQ4MTk5NjgyNzY1NDIyLAogICAgICJuX3J1bmdzIjogNAogICAgfQogICB9LAogICAicGVyX3J1
bmciOiBbCiAgICB7CiAgICAgImZsb29yX3NpZ21hX3JfbmI0MCI6IDMuNzgwMDA5NDk2Mzk4MDg5
NWUtMDksCiAgICAgImthIjogMC4zLAogICAgICJyMjQiOiAtMC4wMDExNjI5MTExODU2ODIwMTQs
CiAgICAgInIzMiI6IC0wLjAwMTE2MzYxNTU5ODMwNzI0MzgsCiAgICAgInI0MCI6IC0wLjAwMTE3
NTg2NzQ2MzA0NjQzMTYKICAgIH0sCiAgICB7CiAgICAgImZsb29yX3NpZ21hX3JfbmI0MCI6IDEu
NTA5MzI1NzQyMTA1ODQyNGUtMDgsCiAgICAgImthIjogMC4xNSwKICAgICAicjI0IjogLTAuMDAw
Mjc3MjQ0MDg1MTkyODA3MSwKICAgICAicjMyIjogLTAuMDAwMjc3OTQ1Mzk5MDcyNDQzNCwKICAg
ICAicjQwIjogLTAuMDAwMjkwMTMzNTc0NjIzODE4NwogICAgfSwKICAgIHsKICAgICAiZmxvb3Jf
c2lnbWFfcl9uYjQwIjogNi4wMzQ2NDIwMTk2Mzc1NzNlLTA4LAogICAgICJrYSI6IDAuMDc1LAog
ICAgICJyMjQiOiAtNS41NjAyODAzNDAxOTk5NTJlLTA1LAogICAgICJyMzIiOiAtNS42MzE1MjE3
MDAwMjI0NTdlLTA1LAogICAgICJyNDAiOiAtNi45NzQ5MDM3OTAzMTMyOTJlLTA1CiAgICB9LAog
ICAgewogICAgICJmbG9vcl9zaWdtYV9yX25iNDAiOiAyLjQxMzYxNjYyNDc1MDc4OWUtMDcsCiAg
ICAgImthIjogMC4wMzc1LAogICAgICJyMjQiOiAtOC4zOTcxNzcyMzA2Njc5MDdlLTA2LAogICAg
ICJyMzIiOiAtOS4xMjY3MDA0MzkyODgwOTNlLTA2LAogICAgICJyNDAiOiAtMS45OTk3ODkzNzcw
ODI4OTQ1ZS0wNQogICAgfSwKICAgIHsKICAgICAiZmxvb3Jfc2lnbWFfcl9uYjQwIjogOS42NTQz
Njk2MDk1NzAwNDllLTA3LAogICAgICJrYSI6IDAuMDE4NzUsCiAgICAgInIyNCI6IC0xLjMwODM4
MDc5MTU5ODExODNlLTA2LAogICAgICJyMzIiOiAtMi4zMzg2MTMwMDQ4MDQyMDJlLTA2LAogICAg
ICJyNDAiOiAtMS40OTgwMTAwOTgwODg4MDllLTA1CiAgICB9LAogICAgewogICAgICJmbG9vcl9z
aWdtYV9yX25iNDAiOiAzLjg2MTcxNjc4OTU3Mzk5MTVlLTA2LAogICAgICJrYSI6IDAuMDA5Mzc1
LAogICAgICJyMjQiOiAtOC4yOTU0Njc0Njg0OTk4NTFlLTA4LAogICAgICJyMzIiOiAtNy44Nzk0
ODkyMjc3NTc4M2UtMDcsCiAgICAgInI0MCI6IC0xLjA5NTkzODU4MzA3MzMzMDRlLTA1CiAgICB9
LAogICAgewogICAgICJmbG9vcl9zaWdtYV9yX25iNDAiOiAxLjU0NDYxMTI4MzQwNzI5NjhlLTA1
LAogICAgICJrYSI6IDAuMDA0Njg3NSwKICAgICAicjI0IjogLTEuNDQyNzYxMDg2NDg5Nzc0NGUt
MDYsCiAgICAgInIzMiI6IC0zLjk1MDEzNTY4OTIxMjQzMWUtMDYsCiAgICAgInI0MCI6IDEuMzQ1
Nzk3OTA3NDQ4MjY1MWUtMDUKICAgIH0sCiAgICB7CiAgICAgImZsb29yX3NpZ21hX3JfbmI0MCI6
IDYuMTgxOTY2MzI4MjU4MjRlLTA1LAogICAgICJrYSI6IDAuMDAyMzQzNzUsCiAgICAgInIyNCI6
IC0yLjA0ODgzNTcxNTMwNzAwN2UtMDYsCiAgICAgInIzMiI6IDcuNjM5MjI2MDI3MjY3Mjk4ZS0w
NSwKICAgICAicjQwIjogLTAuMDAwMjcxMzgyMTAxNzYxMTQxNzUKICAgIH0sCiAgICB7CiAgICAg
ImZsb29yX3NpZ21hX3JfbmI0MCI6IDAuMDAwMjQ3MzQ2NDYwNzU0ODA4ODMsCiAgICAgImthIjog
MC4wMDExNzE4NzUsCiAgICAgInIyNCI6IC0yLjUxODY2ODQyNTg1NDkwODZlLTA1LAogICAgICJy
MzIiOiAwLjAwMDMwMTE5OTE4MDk5MDAzMDUsCiAgICAgInI0MCI6IC0wLjAwMDQwODQyNDQyOTA5
NTI3NzY1CiAgICB9CiAgIF0KICB9LAogICJHTSI6IHsKICAgImEyX2Zsb29yX2NsZWFuX25iNDAi
OiAtMC4wMTk5MzI2MTkxNDIxMzE5NywKICAgImEyX2Zsb29yX2NsZWFuX3JlbF9kcmlmdCI6IHsK
ICAgICIyNHYzMiI6IDAuMDAwMTc4NDg2OTI1MzAxMTA1OTcsCiAgICAiMzJ2NDAiOiAwLjAwMTUz
Mzk0MjAzMzQxNjMyNzQKICAgfSwKICAgImE0X2Zsb29yX2NsZWFuX25iNDAiOiAtMC4wMDgyNzA5
NDE1NjIwNDA4MzQsCiAgICJjX1RfZmxvb3JfY2xlYW5fbmI0MCI6IDUuMDQ4MTcxMjIyMzAxNjQy
LAogICAiam9pbnRfZml0IjogewogICAgIm5iMjRfYWxsX3J1bmdzIjogewogICAgICJhMiI6IC0w
LjAxOTUzNTUzOTMwMzQzNzUyLAogICAgICJhNCI6IC0wLjAxMTk5NTI5NjAxNjg3MDQ4MywKICAg
ICAiY19UIjogNS4wNDgxNDI2OTk5Mjk5MjEsCiAgICAgIm5fcnVuZ3MiOiA5CiAgICB9LAogICAg
Im5iMjRfZmxvb3JfY2xlYW5fcnVuZ3Nfa2FfZ2VfMC4wMzc1IjogewogICAgICJhMiI6IC0wLjAx
OTkwNTU5NTkxNDM3MzgyLAogICAgICJhNCI6IC0wLjAwODUxMzA4MTAzNzg4ODY1LAogICAgICJj
X1QiOiA1LjA0ODE2ODg1NzUxMTU1NCwKICAgICAibl9ydW5ncyI6IDQKICAgIH0sCiAgICAibmIz
Ml9hbGxfcnVuZ3MiOiB7CiAgICAgImEyIjogLTAuMDIwMjY2MDI4NjQxNDcyNzUyLAogICAgICJh
NCI6IC0wLjAwNTEwMjk4MTg0MDc4NDQxNywKICAgICAiY19UIjogNS4wNDgxOTM2NDAxNjAxOTIs
CiAgICAgIm5fcnVuZ3MiOiA5CiAgICB9LAogICAgIm5iMzJfZmxvb3JfY2xlYW5fcnVuZ3Nfa2Ff
Z2VfMC4wMzc1IjogewogICAgICJhMiI6IC0wLjAxOTkwMjA0MzY1OTc5Mzc3NiwKICAgICAiYTQi
OiAtMC4wMDg1NDg4OTU3NTc4OTk3MDQsCiAgICAgImNfVCI6IDUuMDQ4MTY4NzE1MzQxNTY3LAog
ICAgICJuX3J1bmdzIjogNAogICAgfSwKICAgICJuYjQwX2FsbF9ydW5ncyI6IHsKICAgICAiYTIi
OiAtMC4wMDY3MzU4NjkxNzQzNDQzODQsCiAgICAgImE0IjogLTAuMTMyOTI5OTYyNDI4MTQzMTQs
CiAgICAgImNfVCI6IDUuMDQ3MjU3MDE2NTgyMzk1LAogICAgICJuX3J1bmdzIjogOQogICAgfSwK
ICAgICJuYjQwX2Zsb29yX2NsZWFuX3J1bmdzX2thX2dlXzAuMDM3NSI6IHsKICAgICAiYTIiOiAt
MC4wMTk5MzI2MTkxNDIxMzE5NywKICAgICAiYTQiOiAtMC4wMDgyNzA5NDE1NjIwNDA4MzQsCiAg
ICAgImNfVCI6IDUuMDQ4MTcxMjIyMzAxNjQyLAogICAgICJuX3J1bmdzIjogNAogICAgfQogICB9
LAogICAicGVyX3J1bmciOiBbCiAgICB7CiAgICAgImZsb29yX3NpZ21hX3JfbmI0MCI6IDMuNzg1
MjQzNDM1NjMxNTkzZS0wOSwKICAgICAia2EiOiAwLjMsCiAgICAgInIyNCI6IC0wLjAwMTg1NDA0
MTgwNDkyNjA5ODcsCiAgICAgInIzMiI6IC0wLjAwMTg2MjIzMzYwNTgyOTA0NDUsCiAgICAgInI0
MCI6IC0wLjAwMTg1MzM0MDMyMTA0MTIzMDMKICAgIH0sCiAgICB7CiAgICAgImZsb29yX3NpZ21h
X3JfbmI0MCI6IDEuNTA5ODM2NDkxNDczMzQ0ZS0wOCwKICAgICAia2EiOiAwLjE1LAogICAgICJy
MjQiOiAtMC4wMDA0NDY1ODg2NjEzNjUxNTQ4NSwKICAgICAicjMyIjogLTAuMDAwNDU0NzYzODQy
OTcxNzE3MSwKICAgICAicjQwIjogLTAuMDAwNDQ1OTA2NjAzOTE4NjMzMjQKICAgIH0sCiAgICB7
CiAgICAgImZsb29yX3NpZ21hX3JfbmI0MCI6IDYuMDM1MTg3Nzg0MTM0MzA2ZS0wOCwKICAgICAi
a2EiOiAwLjA3NSwKICAgICAicjI0IjogLTAuMDAwMTAyNjc4ODAxMTc2ODY5NzgsCiAgICAgInIz
MiI6IC0wLjAwMDExMDg4MDc3MzQzOTAxNDkyLAogICAgICJyNDAiOiAtMC4wMDAxMDE2MjQ2OTYx
NDA3MjMKICAgIH0sCiAgICB7CiAgICAgImZsb29yX3NpZ21hX3JfbmI0MCI6IDIuNDEzNjk1MDg5
MzMzNjI5ZS0wNywKICAgICAia2EiOiAwLjAzNzUsCiAgICAgInIyNCI6IC0yLjQwMzEyMzg5NDc0
NTI4NWUtMDUsCiAgICAgInIzMiI6IC0zLjIyNzQ1NDcxNDYyNzE1NGUtMDUsCiAgICAgInI0MCI6
IC0yLjI5MTMyNzQzMDkxNDQyNWUtMDUKICAgIH0sCiAgICB7CiAgICAgImZsb29yX3NpZ21hX3Jf
bmI0MCI6IDkuNjU0NDA0Nzc2ODk2NzJlLTA3LAogICAgICJrYSI6IDAuMDE4NzUsCiAgICAgInIy
NCI6IC01LjY5Mjg0NjkwMDk5NTM2M2UtMDYsCiAgICAgInIzMiI6IC0xLjI5MTgyODIxODc2MzUw
MjJlLTA1LAogICAgICJyNDAiOiAtMy40NjI2NjE0NDkyMzgzNDY3ZS0wNgogICAgfSwKICAgIHsK
ICAgICAiZmxvb3Jfc2lnbWFfcl9uYjQwIjogMy44NjE2NDU4MTU1NTU4MzdlLTA2LAogICAgICJr
YSI6IDAuMDA5Mzc1LAogICAgICJyMjQiOiAtOC41OTkxMTgyOTg1MzU2NTdlLTA3LAogICAgICJy
MzIiOiAtMi44MTU5MjgzODYzNTcxMzZlLTA2LAogICAgICJyNDAiOiAxLjE1NjkwMDMwMDg0NzE0
MTJlLTA1CiAgICB9LAogICAgewogICAgICJmbG9vcl9zaWdtYV9yX25iNDAiOiAxLjU0NDU5MTkz
MjYyMTM1M2UtMDUsCiAgICAgImthIjogMC4wMDQ2ODc1LAogICAgICJyMjQiOiAxLjU5MjU3OTMy
MjE5NjAzMDVlLTA2LAogICAgICJyMzIiOiA0Ljc3MjQ1Mzg5NzQwNTg4MmUtMDYsCiAgICAgInI0
MCI6IDMuMzA2MTI5OTUyMzYyOTAyZS0wNQogICAgfSwKICAgIHsKICAgICAiZmxvb3Jfc2lnbWFf
cl9uYjQwIjogNi4xNzkyNTgyMTQ2NzYzODRlLTA1LAogICAgICJrYSI6IDAuMDAyMzQzNzUsCiAg
ICAgInIyNCI6IDIuMDYwNTQxNDQyODA1NDMwM2UtMDYsCiAgICAgInIzMiI6IC0yLjg2MzE2MTM2
MTg3NjgwOTNlLTA1LAogICAgICJyNDAiOiAtMy44OTk3OTc0MDYzNTkyNjJlLTA1CiAgICB9LAog
ICAgewogICAgICJmbG9vcl9zaWdtYV9yX25iNDAiOiAwLjAwMDI0NzY5NDAxODM0MDQ0NzEsCiAg
ICAgImthIjogMC4wMDExNzE4NzUsCiAgICAgInIyNCI6IC02Ljc2NTAwODA5MDQ5MjQwOGUtMDYs
CiAgICAgInIzMiI6IDUuMTU2NjQ5Njg3OTIwNzMzNWUtMDUsCiAgICAgInI0MCI6IC0wLjAwMTA5
NjY0NjQ4MDE1NDI4NDEKICAgIH0KICAgXQogIH0KIH0sCiAicmVhZGluZyI6ICJUaGUgbl9iIGRy
aWZ0IG9mIHRoZSBlbGVjdGVkIGVzdGltYXRvciBpcyBhIHVuaWZvcm0gb2Zmc2V0IGluIHJfVCBv
ZiB+MWUtNSBhY3Jvc3MgcnVuZ3MgPSBhIHNoaWZ0IG9mIHRoZSBrLT4wIHNwZWVkIGV4dHJhcG9s
YXRlZCBmcm9tIHRoZSBzbWFsbC1rIHNwZWVkIHNldCwgd2hlcmUgdGhlIGRlbnNlLWVpZyBmbG9v
ciAoQS0xIHRlcm0pIGlzIH4xLjVlLTUgaW4gcjsgdGhlIFQtYnJhbmNoIG9tZWdhcyBhdCBrYSA+
PSAwLjAzNzUgYWdyZWUgYWNyb3NzIG5fYiB0byB+MWUtNi4gVGhlIGMtZnJlZSBqb2ludCBmaXQg
b24gZmxvb3ItY2xlYW4gcnVuZ3MgY29udmVyZ2VzIHRvIDw9IDNlLTMgcmVsYXRpdmUgaW4gYTIu
IiwKICJzb3VyY2VfY2hlY2twb2ludF9tZDUiOiAiNWVlMTUyZmMxNGFjNTVlNzIwOTRmYzY2MGFm
ZjdhNGEiCn0K
<<<EMBED-END name=s2c1_phase1_ladder_analysis.json>>>

### EMBED — chat A-2 evaluation — `s2c1_phase1_A2_evaluation.json` (md5 77fea65fde95efd33d8990956c7c07ff, 2934 B, b64, QUARANTINED)

<<<EMBED-BEGIN name=s2c1_phase1_A2_evaluation.json md5=77fea65fde95efd33d8990956c7c07ff bytes=2934 enc=b64 quarantine=1>>>
ewogIkZfQ09OVl9wYXNzX0EyIjogdHJ1ZSwKICJGX0lTT19jVF9zcGxpdCI6IDEuMzMzODk0Nzk1
NDYzMzA4NWUtMDUsCiAiRl9JU09fcGFzcyI6IHRydWUsCiAiRl9NSVhfcGFzcyI6IHRydWUsCiAi
YWRkZW5kdW1fQTJfbWQ1IjogImE5YmRhMDg2MjEzZWUwYWZlMWUyYmEwMTA1NTY1OWNkIiwKICJn
YXRlIjogIkctUzJDMSIsCiAibGVnIjogImNoYXQiLAogIm1lY2hhbmljYWxfYXJtX0EyIjogewog
ICJHSyI6ICJBMyBESVNQRVJTSVZFLU8oa14yKSIsCiAgIkdNIjogIkEzIERJU1BFUlNJVkUtTyhr
XjIpIgogfSwKICJwZXJfZGlyZWN0aW9uIjogewogICJHSyI6IHsKICAgIkNJX2EyX3RvdGFsIjog
MC4wMDAzMTgzNDgwMDUyODAyNTg0LAogICAiRl9DT05WX2EyIjogewogICAgInBhc3MiOiB0cnVl
LAogICAgInJlbF8yNHYzMiI6IDAuMDAwMTE4NjY1NTI5Njg5NDA4MzksCiAgICAicmVsXzMydjQw
IjogMC4wMDMwMDI3NTg3MTkzNTc1OTczCiAgIH0sCiAgICJGX0NPTlZfY1QiOiB7CiAgICAicGFz
cyI6IHRydWUsCiAgICAicmVsXzI0djMyIjogMi4yMzMwNzc1Nzg0MDYyOTVlLTA4LAogICAgInJl
bF8zMnY0MCI6IDQuMTU1NTY0NTEwMjc3NTQzZS0wNwogICB9LAogICAiYTIiOiAtMC4wMTI3OTQx
NjE1MzA3OTI3NiwKICAgImEyX3Jlc29sdmVkX25vbnplcm8iOiB0cnVlLAogICAiYTJfd2luZG93
X3JlbCI6IDAuMDI0ODgyMjg3NDgwNDMxMTQsCiAgICJhMl93aW5kb3dfdGVybV81cnVuZyI6IDAu
MDAwMzE4MzQ4MDA1MjgwMjU4NCwKICAgImE0IjogLTAuMDAyOTk4NDE5Nzc1NTQ3ODA0NCwKICAg
ImE0XzVydW5nIjogLTAuMDA1OTgxNzg4OTE2NTI3MzI5LAogICAiY19UIjogNS4wNDgxOTk2ODI3
NjU0MjIsCiAgICJmaXRzX2J5X25iIjogewogICAgIjI0IjogewogICAgICJhMiI6IC0wLjAxMjc1
NzI1NzQxNzc4ODA2MiwKICAgICAiYTQiOiAtMC4wMDMzNjMxOTc3MjEwNTYwODI1LAogICAgICJj
X1QiOiA1LjA0ODE5NzY5NzY4NDUyMQogICAgfSwKICAgICIzMiI6IHsKICAgICAiYTIiOiAtMC4w
MTI3NTU3NDM3NTA2OTkzMDMsCiAgICAgImE0IjogLTAuMDAzMzc3MzYyODM5NDMxMTQ0LAogICAg
ICJjX1QiOiA1LjA0ODE5NzU4NDk1NDM1CiAgICB9LAogICAgIjQwIjogewogICAgICJhMiI6IC0w
LjAxMjc5NDE2MTUzMDc5Mjc2LAogICAgICJhNCI6IC0wLjAwMjk5ODQxOTc3NTU0NzgwNDQsCiAg
ICAgImNfVCI6IDUuMDQ4MTk5NjgyNzY1NDIyCiAgICB9CiAgIH0sCiAgICJyZWdpbWUiOiAicmVs
YXRpdmUiLAogICAicnVuZ3NfZXhjbHVkZWRfa2EiOiBbCiAgICAwLjAxODc1LAogICAgMC4wMDkz
NzUsCiAgICAwLjAwNDY4NzUsCiAgICAwLjAwMjM0Mzc1LAogICAgMC4wMDExNzE4NzUKICAgXSwK
ICAgInJ1bmdzX3VzZWRfa2EiOiBbCiAgICAwLjMsCiAgICAwLjE1LAogICAgMC4wNzUsCiAgICAw
LjAzNzUKICAgXQogIH0sCiAgIkdNIjogewogICAiQ0lfYTJfdG90YWwiOiAwLjAwMDEyMzY3Njg4
NDIxMTE1NTMzLAogICAiRl9DT05WX2EyIjogewogICAgInBhc3MiOiB0cnVlLAogICAgInJlbF8y
NHYzMiI6IDAuMDAwMTc4NDg2OTI1MzAxMTA1OTcsCiAgICAicmVsXzMydjQwIjogMC4wMDE1MzM5
NDIwMzM0MTYzMjc0CiAgIH0sCiAgICJGX0NPTlZfY1QiOiB7CiAgICAicGFzcyI6IHRydWUsCiAg
ICAicmVsXzI0djMyIjogMi44MTYyNjg0NTE3Nzc0MDRlLTA4LAogICAgInJlbF8zMnY0MCI6IDQu
OTY2MDc4MjI4NjQwOTI0ZS0wNwogICB9LAogICAiYTIiOiAtMC4wMTk5MzI2MTkxNDIxMzE5NywK
ICAgImEyX3Jlc29sdmVkX25vbnplcm8iOiB0cnVlLAogICAiYTJfd2luZG93X3JlbCI6IDAuMDA2
MjA0NzQ4MjczNjM0Mzk5LAogICAiYTJfd2luZG93X3Rlcm1fNXJ1bmciOiAwLjAwMDEyMzY3Njg4
NDIxMTE1NTMzLAogICAiYTQiOiAtMC4wMDgyNzA5NDE1NjIwNDA4MzQsCiAgICJhNF81cnVuZyI6
IC0wLjAwOTQzMDA5NTY4MjE5MjE3MiwKICAgImNfVCI6IDUuMDQ4MTcxMjIyMzAxNjQyLAogICAi
Zml0c19ieV9uYiI6IHsKICAgICIyNCI6IHsKICAgICAiYTIiOiAtMC4wMTk5MDU1OTU5MTQzNzM4
MiwKICAgICAiYTQiOiAtMC4wMDg1MTMwODEwMzc4ODg2NSwKICAgICAiY19UIjogNS4wNDgxNjg4
NTc1MTE1NTQKICAgIH0sCiAgICAiMzIiOiB7CiAgICAgImEyIjogLTAuMDE5OTAyMDQzNjU5Nzkz
Nzc2LAogICAgICJhNCI6IC0wLjAwODU0ODg5NTc1Nzg5OTcwNCwKICAgICAiY19UIjogNS4wNDgx
Njg3MTUzNDE1NjcKICAgIH0sCiAgICAiNDAiOiB7CiAgICAgImEyIjogLTAuMDE5OTMyNjE5MTQy
MTMxOTcsCiAgICAgImE0IjogLTAuMDA4MjcwOTQxNTYyMDQwODM0LAogICAgICJjX1QiOiA1LjA0
ODE3MTIyMjMwMTY0MgogICAgfQogICB9LAogICAicmVnaW1lIjogInJlbGF0aXZlIiwKICAgInJ1
bmdzX2V4Y2x1ZGVkX2thIjogWwogICAgMC4wMTg3NSwKICAgIDAuMDA5Mzc1LAogICAgMC4wMDQ2
ODc1LAogICAgMC4wMDIzNDM3NSwKICAgIDAuMDAxMTcxODc1CiAgIF0sCiAgICJydW5nc191c2Vk
X2thIjogWwogICAgMC4zLAogICAgMC4xNSwKICAgIDAuMDc1LAogICAgMC4wMzc1CiAgIF0KICB9
CiB9LAogInBoYXNlIjogIjEtbGFkZGVyIEEtMiBldmFsdWF0aW9uIiwKICJyZWdpc3RlcmVkX2V4
cGVjdGF0aW9uIjogIkRJU1BFUlNJVkUiLAogInJ1bGUiOiAiY29tbW9uIHJ1bmcgc2V0IHNlbGVj
dGVkIGF0IG5fYj00MCBieSBzaWdtYV9yPDNlLTc7IHdpbmRvdyB0ZXJtIGZyb20gc2lnbWFfcjwx
ZS02IHNldCIsCiAic291cmNlX2NoZWNrcG9pbnRfbWQ1IjogIjVlZTE1MmZjMTRhYzU1ZTcyMDk0
ZmM2NjBhZmY3YTRhIiwKICJ2ZXJkaWN0IjogImNoYXQtbGVnIG1lY2hhbmljYWwgYXJtIHVuZGVy
IEEtMiAobG9nZ2VkIHBlciBkaXJlY3RpdmUgaXRlbSAxKTsgdHdvLWxlZyBjb21wYXJpc29uIHBl
bmRpbmc7IG5vIHdpbmRvdyBhY3Rpb24iCn0K
<<<EMBED-END name=s2c1_phase1_A2_evaluation.json>>>

### EMBED — chat report Phase 0 — `G_S2C1_PHASE0_REPORT.md` (md5 5f678490ed33040705c372065cfd1124, 6556 B, b64, QUARANTINED)

<<<EMBED-BEGIN name=G_S2C1_PHASE0_REPORT.md md5=5f678490ed33040705c372065cfd1124 bytes=6556 enc=b64 quarantine=1>>>
IyBHLVMyQzEgKEdhdGUgRy1TMi1PTi1DT05FKSDigJQgUEhBU0UgMCBSRVBPUlQgKGNoYXQgbGVn
LCBTZXB0ZW1iZXIgMiwgMjAyNikKCioqTG9jayAoYnl0ZS12ZXJpZmllZCk6KiogYEdfUzJfT05f
Q09ORV9FWEVDVVRJT05fUFJFUkVHSVNUUkFUSU9OLm1kYCBtZDUgMmVhOGVjMTNmZmEzYzMyODk4
Y2MyNGEzYmU2MDVjNjQgKDEyLDk4NCBCKSDigJQgY21wLWlkZW50aWNhbCB0byB0aGUgYXBwcm92
ZWQgc3RhZ2luZyBtZW1vOyBgdDFfZm9yYmlkZGVuX0dfUzJfT05fQ09ORS50eHRgIEZST1pFTiA4
Y2Q4OWI5YTgyNzA0YWNjZDg5ZjdmZjZmNWUyMjBiNCAoMTQ0IEIsIDE2IHBhdHRlcm4gbGluZXMp
OyBgR19TMl9PTl9DT05FX0xPQ0tfUkVDT1JELm1kYCBmMmY0ZDUwMDI5ZmI1YmUzMTIyYTg4NWM0
OGE3ZTA0ZiAoMywwMDkgQjsgZWxlY3Rpb25zIEUtMC4uRS04ID0gwqc2IGRlZmF1bHRzLCBUMzsg
TS1uYWl2ZSBleHBlY3RhdGlvbiBESVNQRVJTSVZFIHJlZ2lzdGVyZWQgcHJlLWRhdGEpLiAqKlBI
QVNFMV9BVVRIT1JJWkVEID0gRmFsc2UqKiBpbiBldmVyeSBpbnN0cnVtZW50LgoKIyMgUmVhZGlu
ZXNzOiBIQVJORVNTIFJFQURZIC8gU1VCU1RSQVRFIE5PVCBSRUFEWQoKKiooQikgSW5zdHJ1bWVu
dCB2YWxpZGF0ZWQgb24gYW4gZXhhY3RseS1zb2x2YWJsZSBwNm0gY29udHJvbCoqIChOTiBjZW50
cmFsLWZvcmNlIHRyaWFuZ3VsYXIgbGF0dGljZSwgY2xvc2VkLWZvcm0gZGlzcGVyc2lvbjsgQ09O
VFJPTC1OT1QtVkVSRElDVCk6Ci0gUzIgcHJvamVjdG9yICh0cmFjZWxlc3Mtc3RyYWluIGZyYWN0
aW9uIG/igoIpOiBUIOKGkiAxLCBMIOKGkiDCvSBleGFjdGx5IG9uIGJvdGggbWlycm9yIGxpbmVz
IGF0IGV2ZXJ5IGxhZGRlciBydW5nIOKAlCBQQVNTLgotICoqRi1DVFJMLUwgUEFTUyoqIGJvdGgg
ZGlyZWN0aW9uczogdGhlIGxvbmdpdHVkaW5hbCBicmFuY2gncyBrbm93biBub256ZXJvIGHigoIg
cmVjb3ZlcmVkIHRvIDcuN8OXMTDigbvigbkgKM6T4oCTSywgYeKCgiA9IOKIkjExLzI4OCkgYW5k
IDMuMcOXMTDigbvigbkgKM6T4oCTTSwgYeKCgiA9IOKIkjEvMzIpIGFnYWluc3QgaW5kZXBlbmRl
bnQgY2xvc2VkLWZvcm0gc2VyaWVzIGNvZWZmaWNpZW50czsgY19MID0g4oiaKDkvOCkgcmVjb3Zl
cmVkIHRvIDEw4oG74oG2LiBUaGUgZWxlY3RlZCB0d28tdGVybSBiYXNpcyB7KGthKcKyLCAoa2Ep
4oG0fSBvbiB0aGUgZWxlY3RlZCB3aW5kb3cgWzEw4oG7wrMsIDAuM10gaGFzIGHigoIgYmlhcyDi
iaQgNy43w5cxMOKBu+KBuSDiiaogz4QgPSAxMOKBu+KBtiDigJQgRS00L0UtNSBhZGVxdWF0ZS4K
LSAqKkYtQ1RSTC1JTkogUEFTUzoqKiBpbmplY3RlZCBh4oKCID0gMTDPhCA9IDEw4oG74oG1IHdp
dGggbm9pc2UgMTDigbvigbggcmVjb3ZlcmVkIGF0IDEuMDAzNsOXMTDigbvigbUgwrEgNS4zw5cx
MOKBu+KBtyAoMjAwIHRyaWFsczsgQ0k5NSBjb250YWlucyB0aGUgaW5qZWN0aW9uOyBtZWFuIGVy
cm9yIDMuNsOXMTDigbvigbggPCDPhCkuCi0gQ29udHJvbC1UIGRpYWdub3N0aWMgKG5vdCBhIHZl
cmRpY3QpOiB0aGUgaGFybW9uaWMgcDZtIGxhdHRpY2UgaGFzIGRpcmVjdGlvbi1kZXBlbmRlbnQg
YeKCgl5UICjiiJIxLzk2IG9uIM6T4oCTSywg4oiSMS8zMiBvbiDOk+KAk00pIHdpdGggaXNvdHJv
cGljIGNfVCDigJQgdGhlIHByZXJlZydzIEYtSVNPIGlzIG9uIFNQRUVEUyAozrhfaXNvID0gMSUp
LCBhbmQgYeKCgiBhbmlzb3Ryb3B5IGlzIHJlcG9ydGVkIHBlciBkaXJlY3Rpb24sIGV4YWN0bHkg
YXMgcmVnaXN0ZXJlZC4KCioqKEEpIFN1YnN0cmF0ZSBkaWFnbm9zdGljIOKAlCB0aGUgbG9hZC1i
ZWFyaW5nIFBoYXNlLTAgZmluZGluZy4qKiBUaGUgaW5zdGFudGlhdGVkIGNyeXN0YWwgaW4gcmVh
Y2ggKGd6MSByZWJ1aWxkLCBicmFuY2ggY2xhdWRlL25ldy1zZXNzaW9uLXdyamtsayBAIGFlOTIz
MmUwLCBNQU5JRkVTVC12ZXJpZmllZDogZyA9IDIyIHNvZnQtZGlzaywgbiA9IDY0LCBhKiA9IDEu
NDU3NiwgzrwgPSA1NS45NDYsIM+I4oKAIG1kNSA2ZTg4Y2JkNeKApikgaXMgTk9UIHN0YXRpb25h
cnkgdG8gdGhlIHByZWNpc2lvbiBhbiBhY291c3RpYyBsYWRkZXIgbmVlZHM6Ci0g4oCWTM+I4oKA
4oCWL+KAls+I4oKA4oCWID0gMS4yN8OXMTDigbvCuSAoPSAyLjI3w5cxMOKBu8KzIMOXIM68IOKA
lCBpZGVudGljYWwgdG8gdGhlIHJlYnVpbGQncyBsb2dnZWQgYHJlc2lkdWFsX3BvbGlzaGVkYDsg
YSAxMOKBu+KBtSB3ZWlnaHQgbGVha2FnZSBpbnRvIGhpZ2gtTCBlaWdlbnZlY3RvcnMsIGFtcGxp
ZmllZCBieSB0aGUgTCBzcGVjdHJ1bSkuCi0gVW4tY2xpcHBlZCBwcm9kdWN0LWZvcm0gQmRHLCDP
icKyID0gZWlnKEwoTCsyWCkpOiB0aGUgdHdvIHRyYW5zbGF0aW9uYWwgR29sZHN0b25lIG1vZGVz
IHNpdCBhdCAqKs+JwrIg4omIIOKIkjIuMDk3KiogYXMgayDihpIgMCAoYmFzaXMtSU5ERVBFTkRF
TlQ6IGlkZW50aWNhbCBhdCBuX2IgPSAyNCwgMzIsIDQwLCA0OCwgNjQpOyB0aGUgcGhhc2UgbW9k
ZSBhdCDiiJIwLjAyNS4gV2FyZCByZXNpZHVhbCBvbiB0aGUgdHJhbnNsYXRpb24gbW9kZSDigJYo
TCsyWCniiILigpPPiOKCgOKAli/igJbiiILigpPPiOKCgOKAliA9IDAuMTg2LiBPZmZzZXQg4omI
IDE2LjUgw5cgcmVzaWR1YWwuCi0gUmVmdXRlZCBhbHRlcm5hdGl2ZXM6IGFsaWFzaW5nICjPiOKC
gCBzcGVjdHJhbCB3ZWlnaHQgYmV5b25kIHxtfCDiiaUgMTYgaXMgOcOXMTDigbvCs8K5OyB0aGUg
Z3JpZC1jb25zaXN0ZW50IFggZ2l2ZXMgdGhlIGlkZW50aWNhbCBXYXJkIHJlc2lkdWFsKTsga2Vy
bmVsIG1pc21hdGNoIChncmlkIGtlcm5lbCA9IGFuYWx5dGljIGtlcm5lbCB0byAwLjApLgotIFRo
ZSByZWNvdmVyZWQgYGd6MV9jb3JlLkJkRy5vbWVnYXNgIEhlcm1pdGlhbiBmb3JtIGNsaXBzIM67
KEwpIOKJpSAwIGJlZm9yZSBMXnsxLzJ9LCB3aGljaCBjb252ZXJ0cyB0aGlzIG9mZnNldCBpbnRv
ICoqc3B1cmlvdXMgZXhhY3QgemVybyBtb2RlcyoqICgwLCAwLCB+MTDigbvigbUgZnJvbSBrYSA9
IDAuMDA1IHRvIDAuMDgpIOKAlCB0aGUgaW5zdHJ1bWVudCdzIEYtQ1RSTC1MIGJyYW5jaCBoYWQg
emVybyBleHRyYXBvbGF0ZWQgc3BlZWQsIHdoaWNoIGlzIGhvdyB0aGUgZmluZGluZyBzdXJmYWNl
ZCAodGhlIGhhcm5lc3MgaGFsdGVkIG9uIHRoZSByZXN1bHRpbmcgZGl2aXNpb24gYnkgemVybzsg
dGhlIGhhbHQgaXMgdGhlIGRpc2NvdmVyeSBwYXRoKS4KLSAqKlBoYXNlLTEgcHJlcmVxdWlzaXRl
IChmaXhlZCBoZXJlIHBlciBFLTUgIkYtQ09OViB0aHJlc2hvbGRzIGZpeGVkIGF0IFBoYXNlLTAg
Y2xvc2UiKToqKiByZS1jcnlzdGFsbGl6ZSBhdCB0aGUgZWxlY3RlZCBnZW04IGtlcm5lbCAoRS0z
KSB0byDigJZMz4jigoDigJYv4oCWz4jigoDigJYg4omkIDEw4oG7wrnigbAgYW5kIHZlcmlmeSBX
QVJELc6TOiB8z4nCsl9Hb2xkc3RvbmUoa+KGkjApfCDiiaQgMTDigbvigbggKHN1YnN0cmF0ZSB1
bml0cykgaW4gdGhlIHVuLWNsaXBwZWQgcHJvZHVjdCBmb3JtIEJFRk9SRSBhbnkgbGFkZGVyIHBv
aW50IGlzIGNvbXB1dGVkOyB0aGUgYWNvdXN0aWMgz4nCsiBhdCB0aGUgYm90dG9tIHJ1bmcgKGth
ID0gMS4xN8OXMTDigbvCsywgayA9IDguMMOXMTDigbvigbQvYSopIGlzIE8oMTDigbvigbbigJMx
MOKBu+KBtSkgZm9yIGMgPSBPKDHigJMzKSwgc28gMTDigbvigbggaXMgYSAxJSBmbG9vci4gU3Bl
ZWQgY29udmVyZ2VuY2UgaW4gbl9iIOKJpCAxMOKBu+KBtiByZWxhdGl2ZTsgYeKCgiBjb252ZXJn
ZW5jZSBpbiBuX2Ig4omkIDEw4oG74oG3IGFic29sdXRlLiBUaGUgSGVybWl0aWFuIExeezEvMn0g
Zm9ybSBpcyBhZG1pc3NpYmxlIG9ubHkgb25jZSDOu19taW4oTCkg4omlIOKIkjEw4oG7wrnCsjsg
b3RoZXJ3aXNlIHRoZSBwcm9kdWN0IGZvcm0gaXMgdGhlIGZvcm0gb2YgcmVjb3JkLgoKKiooQykq
KiBGLUNUUkwtSU5KIGFzIGFib3ZlIOKAlCBQQVNTLgoKIyMgSG9uZXN0eSBsZWRnZXIgKFBoYXNl
IDApCi0gKipILVMyQy0xKiogdGhlIGhhcm5lc3MgaGVhZGVyIGNpdGVkIGEgc3VwZXJzZWRlZCBs
b2NrLXJlY29yZCBoYXNoICgzMmE5OWEzZDsgdGhlIHJlY29yZCB3YXMgcmUtbWludGVkIGF0IGYy
ZjRkNTAwIGFmdGVyIHRoZSBoZWFkZXIgd2FzIHdyaXR0ZW4pIOKAlCBjb3JyZWN0ZWQgaW4gdGhl
IGluc3RydW1lbnQgKHVubG9ja2VkIGFydGlmYWN0KSwgbG9nZ2VkLgotICoqSC1TMkMtMioqIHRo
ZSBmaXJzdCBQaGFzZS0wIHJ1biBoYWx0ZWQgKFplcm9EaXZpc2lvbkVycm9yKSBiZWNhdXNlIHRo
ZSBjbGlwcGVkIEhlcm1pdGlhbiBmb3JtIHJldHVybmVkIHplcm8gYWNvdXN0aWMgc3BlZWRzIOKA
lCBhIGZhaWwtY2xvc2VkIGhhbHQgdGhhdCBleHBvc2VkIHRoZSBzdWJzdHJhdGUgZmluZGluZzsg
bm8gbnVtYmVyIGZyb20gdGhhdCBydW4gaXMgdXNlZC4KLSAqKkgtUzJDLTMqKiB0aGUgZnJvemVu
IFQxIGxpc3QgY2FycmllcyBiYXJlIG51bWVyaWMgcGF0dGVybnMgKDVlLTE2LCA0LjdlLTIzLCAx
LjI3ZS0yMikgdGhhdCBjYW4gY29sbGlkZSB3aXRoIHNjaWVudGlmaWMtbm90YXRpb24gZm9ybWF0
dGluZyBvZiB1bnJlbGF0ZWQgcXVhbnRpdGllcyAoSC0yIGNsYXNzKS4gQWxsIFBoYXNlLTAgc2Nh
bnMgcmV0dXJuZWQgemVybyBoaXRzOyBhbiBhbWVuZGVkIGxpc3Qgd2l0aCBjb250ZXh0dWFsIHBh
dHRlcm5zIGlzIFBST1BPU0VEIGZvciB0aGUgbmV4dCBsb2NrIGN5Y2xlICh0aGUgZnJvemVuIGxp
c3QgaXMgbm90IGVkaXRlZCkuCi0gKipILVMyQy00KiogdGhpcyB0dXJuJ3MgZWFybGllciBpbi1j
b250ZXh0IHdvcmsgKHJlcG8gcmVjb3Zlcnkgb2YgZ3oxL3RzaDQsIGxvY2sgbWludGluZywgZmly
c3QgaGFybmVzcykgd2FzIHJlY292ZXJlZCBmcm9tIHRoZSBzYW5kYm94IGFmdGVyIGEgY29udGV4
dCByZXNldDsgdGhlIGZpbGVzeXN0ZW0gd2FzIHRyZWF0ZWQgYXMgdGhlIHNvdXJjZSBvZiB0cnV0
aCBhbmQgZXZlcnkgYXJ0aWZhY3QgcmUtdmVyaWZpZWQgYnkgaGFzaCAocHJlcmVnLCBUMSwgZ3ox
IE1BTklGRVNUIDE3LzE3IHByZXNlbnQgZmlsZXMgT0spIGJlZm9yZSB1c2UuCi0gKipSZXRybyBR
LWl0ZW0gKEctzrYxLCDCpzIuODguRC4xIC8gVjQuMzYgbGluZSk6KiogRy3OtjEncyBzYW5pdHkg
Z2F0ZSAoYikgInRocmVlIEdvbGRzdG9uZSB6ZXJvcyBhdCDOkyIgcGFzc2VkIG9uIHRoZSBjbGlw
cGVkIGZvcm0g4oCUIGkuZS4sIGZvciB0aGUgd3JvbmcgcmVhc29uOyBpdHMgdmVyZGljdC1iZWFy
aW5nIHF1YW50aXRpZXMgKGFjb3VzdGljIHRvcCAyMC40NSwgZ2FwcyAyMi4xLzI1LjUvMzMpIHNp
dCBhdCDPiSDiiYggMjDigJMzMCB3aGVyZSBhIOKIkjIuMSBvZmZzZXQgaW4gz4nCsiBpcyBhIOKJ
sjAuMiUgc2hpZnQsIHNvIHRoZSBxdWFudGl0YXRpdmUgaW1wYWN0IGlzIGV4cGVjdGVkIG5lZ2xp
Z2libGUsIGJ1dCB0aGUgcmVjb3JkIHNob3VsZCBjYXJyeSB0aGUgYW5ub3RhdGlvbiBhbmQgYSBD
QyByZS1jaGVjayBpZiB0aGUgYXV0aG9yIGVsZWN0cy4gTk9UIGEgRy1TMkMxIG1hdHRlcjsgZmls
ZWQgZm9yIHRoZSBhdXRob3IuCgojIyBXaGF0IFBoYXNlIDAgZG9lcyBOT1QgY2xhaW0KTm8gUzIg
bGFkZGVyIHdhcyBjb21wdXRlZCwgZml0dGVkLCBvciBzZWFsZWQgKHRoZSBlYXJsaWVyIGhhcm5l
c3MncyBzZWFsaW5nIHBhdGggbmV2ZXIgZXhlY3V0ZWQ7IFBIQVNFMV9BVVRIT1JJWkVEID0gRmFs
c2UpLiBObyB2ZXJkaWN0IGFybSBpcyB0b3VjaGVkLiBOb3RoaW5nIGFib3V0IFdf4oiqLiBUaGUg
Y29udHJvbC1sYXR0aWNlIG51bWJlcnMgYXJlIGluc3RydW1lbnQgY2FsaWJyYXRpb24gb25seS4K
CiMjIEVzdGF0ZQpsb2NrLzogcHJlcmVnIDJlYThlYzEzICgxMiw5ODQgQik7IFQxIDhjZDg5Yjlh
ICgxNDQgQik7IGxvY2sgcmVjb3JkIGYyZjRkNTAwICgzLDAwOSBCKS4gUGhhc2UgMDogZ19zMmMx
X3BoYXNlMF9jbG9zZS5weSAodGhlIGV4ZWN1dGVkIGluc3RydW1lbnQpLCBnX3MyYzFfcGhhc2Uw
X2hhcm5lc3MucHkgKHRoZSBQaGFzZS0xIGluc3RydW1lbnQgc2tlbGV0b24g4oCUIEJkRyBlaWdl
bnZlY3RvcnMsIHBvbGFyaXNhdGlvbiBmaXQsIGNsYXNzaWZpZXIsIHNlYWxpbmcgcGF0aDsgaGFs
dGVkIGF0IFBoYXNlIDAgYXMgYWJvdmUpLCBjaGVja3BvaW50IGdfczJjMV9waGFzZTBfY2hlY2tw
b2ludC5qc29uIGVhZTJiYmQ3MzRmNTEyOWRkMWU1MWVmY2JiNTVkZDNkICg0LDU1NSBCKSwgcnVu
IGxvZ3MsIHRoaXMgcmVwb3J0LiBUMTogemVybyBoaXRzIG9uIGV2ZXJ5IGFydGlmYWN0LiBnejEg
c3Vic3RyYXRlIGVzdGF0ZTogTUFOSUZFU1QubWQ1IHZlcmlmaWVkIGZvciBhbGwgMTcgcHJlc2Vu
dCBmaWxlcyAoMTUgY2FjaGUgZmlsZXMgbm90IGZldGNoZWQsIG5vdCBuZWVkZWQpLgoKKipOZXh0
IGF1dGhvcml6YXRpb24gZ2F0ZToqKiBQaGFzZSAxID0gKGkpIGdlbTggcmUtY3J5c3RhbGxpemF0
aW9uIHRvIHRoZSBzdGF0aW9uYXJpdHkgdGhyZXNob2xkICsgV0FSRC3OkyB2ZXJpZmljYXRpb24s
IHRoZW4gKGlpKSB0aGUgc2luZ2xlLWNyeXN0YWwga2EtbGFkZGVyIGZpdC4gTm90IHN0YXJ0ZWQu
Cg==
<<<EMBED-END name=G_S2C1_PHASE0_REPORT.md>>>

### EMBED — chat report Phase 1 halt — `G_S2C1_PHASE1_HALT_REPORT.md` (md5 b0e6790c323764d7e93350d2b5ef09a8, 4107 B, b64, QUARANTINED)

<<<EMBED-BEGIN name=G_S2C1_PHASE1_HALT_REPORT.md md5=b0e6790c323764d7e93350d2b5ef09a8 bytes=4107 enc=b64 quarantine=1>>>
IyBHLVMyQzEg4oCUIFBIQVNFIDEgSEFMVCBSRVBPUlQgKGNoYXQgbGVnLCBTZXB0ZW1iZXIgMiwg
MjAyNikKCioqU3RhdHVzOiBIQUxURUQgYXQgZGlyZWN0aXZlIGl0ZW0gMiAoV0FSRC3OkykuIFRo
ZSBsYWRkZXIgKGl0ZW0gMykgd2FzIE5PVCBydW4uKiogTG9jayB1bmNoYW5nZWQgKHByZXJlZyAy
ZWE4ZWMxMzsgVDEgOGNkODliOWE7IHJlY29yZCBmMmY0ZDUwMCkuCgojIyBJdGVtIDEg4oCUIHJl
LWNyeXN0YWxsaXphdGlvbjogUEFTUywgYW5kIHRoZSBFLTMgcmVjb3JkIHBvaW50IGlzIENPTkZJ
Uk1FRApHRU0tOCBrZXJuZWwgVShyKSA9IDIwwrdleHAo4oiScuKBuCkgaW4gMi1EICjFqCgwKSA9
IDU2Ljk1MDk0NyksIGhleGFnb25hbCBjZWxsIGEqID0gMS40NjA1OSwgbiA9IDY0LCBmaXhlZCDO
vCA9IDUzLjIyNS4gRml4ZWQtzrwgc2VtaS1pbXBsaWNpdCBpbWFnaW5hcnkgdGltZSBjb252ZXJn
ZXMgaW4gMiwwMDAgc3RlcHMgdG8g4oCWTM+I4oKA4oCWL+KAls+I4oKA4oCWID0gKioxLjk2w5cx
MOKBu8K5wrIqKiAodGhyZXNob2xkIDEw4oG7wrnigbA7IDXDlzEw4oG0IG1hcmdpbjsgTmV3dG9u
4oCTS3J5bG92IGNvbmZpcm1zIGl0IGlzIGF0IHRoZSBkb3VibGUtcHJlY2lzaW9uIGZpeGVkIHBv
aW50KS4gVGhlIHJlc3VsdGluZyBtZWFuIGRlbnNpdHkgaXMgKirin6jPgeKfqSA9IDAuOTk5OTg4
Kiog4oCUIGkuZS4gdGhlIHJlY29yZCdzIChnKiA9IDIwLCBhKiA9IDEuNDYwNTksIM68ID0gNTMu
MjI1LCDPgeKCgCA9IDEpIHR1cGxlIGNsb3NlcyBvbiB0aGlzIGluc3RydW1lbnQgdG8gMS4yw5cx
MOKBu+KBtSDigJQgYW4gaW5kZXBlbmRlbnQgY29uZmlybWF0aW9uIG9mIHRoZSBHLVRTSDMgZmly
c3QtcGFzc2luZyBwb2ludC4gz4jigoAgc3BlY3RyYWwgdGFpbCBiZXlvbmQgfG18IOKJpSAyNDog
MsOXMTDigbvCs8KyLiDOu19taW4oTCkgYXQgzpMgPSAqKisxLjbDlzEw4oG7wrnigbQqKjogdGhl
IEhlcm1pdGlhbiBMXnsxLzJ9IEJkRyBmb3JtIGlzIGFkbWlzc2libGUgb24gdGhpcyBzdGF0ZSAo
dGhlIFBoYXNlLTAgZGVmZWN0IHdhcyB0aGUgb2xkIHN0YXRlLCBub3QgdGhlIGZvcm0pLiDPiOKC
gCBtZDUgaW4gdGhlIGNoZWNrcG9pbnQ7IGBwc2kwX2dlbThfbjY0Lm5weWAgYmFua2VkLgoKIyMg
SXRlbSAyIOKAlCBXQVJELc6TOiBGQUlMIGFzIGxpdGVyYWxseSBzcGVjaWZpZWQ7IHRoZSBXYXJk
IGlkZW50aXR5IGl0c2VsZiBob2xkcwpMaXRlcmFsIGNyaXRlcmlvbiAocHJvZHVjdC1mb3JtIGVp
Zywgbl9iID0gMzIpOiBHb2xkc3RvbmUgfM+JwrJ8ID0gezguOcOXMTDigbvigbksIDQuNMOXMTDi
gbvigbksICoqMy41w5cxMOKBu+KBuCoqfSDigJQgdGhpcmQgbW9kZSBleGNlZWRzIDEw4oG74oG4
IOKGkiBoYWx0LgpEaWFnbm9zaXMgKGNoYXQtc2lkZSwgYWxsIG51bWJlcnMgaW4gdGhlIGNoZWNr
cG9pbnQpOgotIEFuYWx5dGljIHRyYW5zbGF0aW9uIG1vZGVzIOKIguKCk8+I4oKALCDiiILhtafP
iOKCgCB1bmRlciAoTCsyWCk6IHJlc2lkdWFsICoqNi42w5cxMOKBu8K5wrIgLyAxLjHDlzEw4oG7
wrnCuSoqIChuX2IgPSAzMjsgMuKAkzPDlzEw4oG7wrnCsiBhdCBuX2IgPSAyNCkg4oCUIHRoZSBX
YXJkIGlkZW50aXR5IGhvbGRzIGF0IHRoZSBzdGF0aW9uYXJpdHkgbGV2ZWwuCi0gRGVuc2UtZWln
IEdvbGRzdG9uZSB2YWx1ZXMgdnMgYmFzaXM6IHByb2R1Y3QgZm9ybSAyLjHDlzEw4oG74oG5ICgy
NCkg4oaSIDMuNcOXMTDigbvigbggKDMyKSDihpIgMy42w5cxMOKBu+KBuCAoNDApOyBIZXJtaXRp
YW4gZWlnaCA2LjXDlzEw4oG7wrnigbAg4oaSIDMuMcOXMTDigbvigbkg4oaSIDEuOMOXMTDigbvi
gbg7IGtpbmV0aWMgY3V0b2ZmIDQsOTU1IOKGkiA4LDk1MiDihpIgMTQsMTM0LiBUaGUgdmFsdWVz
IHRyYWNrIChjdXRvZmYpwrLCt861X21hY2hpbmU6ICoqYSBkb3VibGUtcHJlY2lzaW9uIHNvbHZl
ciBmbG9vciwgbm90IGEgcHJvcGVydHkgb2YgdGhlIHN1YnN0cmF0ZS4qKiBObyBzdGF0ZSwgaG93
ZXZlciBzdGF0aW9uYXJ5LCBwYXNzZXMgdGhlIGxpdGVyYWwgY3JpdGVyaW9uIGJ5IGRlbnNlIGVp
ZyBhdCBuX2Ig4omlIDMyIChwcm9kdWN0KSBvciA0MCAoSGVybWl0aWFuKS4KLSBUaGUgUGhhc2Ut
MCB0aHJlc2hvbGQgd2FzIGRlcml2ZWQgaW4gdGhlIHJlZ2ltZSB3aGVyZSB0aGUgb2Zmc2V0IHdh
cyBnb3Zlcm5lZCBieSBzdGF0aW9uYXJpdHkgKG9mZnNldCDiiYggMTYuNSDDlyByZXNpZHVhbCBh
dCByZXNpZHVhbCAwLjEyNyk7IGF0IG1hY2hpbmUtbGV2ZWwgc3RhdGlvbmFyaXR5IHRoZSBvZmZz
ZXQgaXMgZ292ZXJuZWQgYnkgcm91bmRvZmYgYW1wbGlmaWVkIGJ5IHRoZSBraW5ldGljIGN1dG9m
ZiDigJQgYSBkaWZmZXJlbnQgcmVnaW1lIHRoZSB0aHJlc2hvbGQgc3RhdGVtZW50IGRpZCBub3Qg
YW50aWNpcGF0ZS4gKipILVMyQy01KiogKEgtMiBjbGFzczogYSBnYXRlIHN0YXRlZCBvbiBhIHF1
YW50aXR5IHRoYXQgaGl0cyBhIG51bWVyaWNhbCBmbG9vcikuCgojIyBXaGF0IHRoZSBsYWRkZXIg
bmVlZHMgKGZvciB0aGUgYXV0aG9yJ3MgZGVjaXNpb24pClRoZSBwaHlzaWNhbGx5IHJlbGV2YW50
IHJlcXVpcmVtZW50IGlzIEdvbGRzdG9uZSBvZmZzZXQg4omqIM+JX1TCsiBhdCB0aGUgYm90dG9t
IHJ1bmcgKGthID0gMS4xN8OXMTDigbvCsyk6IHdpdGggY19UIH4gMuKAkzMgdGhhdCBpcyDPiV9U
wrIgfiAz4oCTNsOXMTDigbvigbYsIHNvIHRoZSBIZXJtaXRpYW4gZmxvb3IgYXQgbl9iID0gMzIg
KDPDlzEw4oG74oG5KSBpcyB+MTDigbvCsyBvZiBpdCBhbmQgZW50ZXJzIHIoaykgYXQgdGhlIGJv
dHRvbSBydW5nIGF0IH41w5cxMOKBu+KBtCwgd2VpZ2h0ZWQgKGthKcKyIH4gMTDigbvigbYgaW4g
dGhlIGHigoIgZml0IOKAlCBuZWdsaWdpYmxlOyBhdCB0aGUgdG9wIHJ1bmcgKM+JX1TCsiB+IDAu
NSkgdGhlIGZsb29yIGlzIH4xMOKBu+KBuCByZWxhdGl2ZSDihpIgYeKCgiBwcmVjaXNpb24gfjEw
4oG74oG3IDwgz4QuIEYtQ09OViAobl9iIDI0LzMyLzQwKSBtZWFzdXJlcyB0aGlzIGRpcmVjdGx5
LgoKKipQcm9wb3NlZCBBbWVuZG1lbnQgQS0xIChyZXF1aXJlcyBhdXRob3JpemF0aW9uOyBub3Qg
YXBwbGllZCk6KiogV0FSRC3OkyBpcyBzYXRpc2ZpZWQgYnkgKGEpIHRoZSBhbmFseXRpYy1tb2Rl
IFdhcmQgcmVzaWR1YWwg4oCWKEwrMlgp4oiCz4jigoDigJYv4oCW4oiCz4jigoDigJYg4omkIDEw
4oG74oG5IG9uIGJvdGggbGVncyBBTkQgKGIpIHRoZSBIZXJtaXRpYW4tZm9ybSBHb2xkc3RvbmUg
fM+JwrJ8IOKJpCAxMOKBu+KBuCBhdCB0aGUgbl9iIG9mIHJlY29yZCB3aXRoIM67X21pbihMKSDi
iaUg4oiSMTDigbvCucKyIHZlcmlmaWVkIGF0IGV2ZXJ5IGs7IHRoZSBkZW5zZS1laWcgZmxvb3Ig
aXMgY2FycmllZCBhcyBhbiBleHBsaWNpdCB1bmNlcnRhaW50eSB0ZXJtIGluIEYtQ09OVi4gVW5k
ZXIgQS0xIHRoZSBwcmVzZW50IHN0YXRlIFBBU1NFUyAoKGEpIDEuMcOXMTDigbvCucK5OyAoYikg
My4xw5cxMOKBu+KBuSBhdCBuX2IgPSAzMjsgdGhlIGxhZGRlciB3b3VsZCBydW4gYXQgbl9iIOKI
iCB7MjQsIDMyLCA0MH0gd2l0aCBwcm9kdWN0LWZvcm0gY3Jvc3MtY2hlY2tzIGF0IHR3byBydW5n
cykuIEFsdGVybmF0aXZlIHdpdGhvdXQgYW1lbmRtZW50OiBydW4gdGhlIGxhZGRlciBhdCBuX2Ig
PSAyNCB3aGVyZSB0aGUgbGl0ZXJhbCBwcm9kdWN0LWZvcm0gY3JpdGVyaW9uIGhvbGRzICgyLjHD
lzEw4oG74oG5KSDigJQgTk9UIHJlY29tbWVuZGVkIGNoYXQtc2lkZSwgc2luY2Ugc2VsZWN0aW5n
IHRoZSBiYXNpcyB0byBzYXRpc2Z5IGEgZmxvb3ItbGltaXRlZCBnYXRlIGlzIEVkZGluZ3Rvbi1z
aGFwZWQ7IHRoZSBhbWVuZG1lbnQgaXMgdGhlIGhvbmVzdCByb3V0ZS4KCiMjIEVzdGF0ZQpgZ19z
MmMxX3BoYXNlMS5weWAgKGhhbHRlZCBhdCBpdGVtIDIgYnkgZGVzaWduKSwgYGdfczJjMV9waGFz
ZTFfcnVuLmxvZ2AsIGBnX3MyYzFfcGhhc2UxX2NoZWNrcG9pbnQuanNvbmAgKHN0ZXBzIDHigJMy
ICsgZGlhZ25vc2lzKSwgYHBzaTBfZ2VtOF9uNjQubnB5YC4gVDE6IHplcm8gaGl0cy4gUEhBU0Ux
IGxhZGRlcjogbm90IGV4ZWN1dGVkOyBhcm1zIHVudG91Y2hlZDsgbm90aGluZyBhYm91dCBXX+KI
qi4K
<<<EMBED-END name=G_S2C1_PHASE1_HALT_REPORT.md>>>

### EMBED — chat report Phase 1 ladder — `G_S2C1_PHASE1_LADDER_REPORT.md` (md5 6995cee96c9e696241b038a709dabcaf, 5341 B, b64, QUARANTINED)

<<<EMBED-BEGIN name=G_S2C1_PHASE1_LADDER_REPORT.md md5=6995cee96c9e696241b038a709dabcaf bytes=5341 enc=b64 quarantine=1>>>
IyBHLVMyQzEgKEdhdGUgRy1TMi1PTi1DT05FKSDigJQgUEhBU0UgMSBMQURERVIgUkVQT1JUIChj
aGF0IGxlZywgU2VwdGVtYmVyIDMsIDIwMjYpCgoqKkxvY2s6KiogcHJlcmVnIDJlYThlYzEzOyBU
MSA4Y2Q4OWI5YTsgbG9jayByZWNvcmQgZjJmNGQ1MDA7ICoqQWRkZW5kdW0gQS0xIDhiZjUxYmQw
KiogKGF1dGhvci1hdXRob3JpemVkLCB2ZXJiYXRpbSkuIFN1YnN0cmF0ZTogYmFua2VkIGdlbTgg
c3RhdGUgKGFycmF5IG1kNSBiMjdmYTAwNDsgcmVzaWR1YWwgcmUtdmVyaWZpZWQgMS45NsOXMTDi
gbvCucKyKS4gSW5zdHJ1bWVudDogYGdfczJjMV9waGFzZTFfbGFkZGVyLnB5YCAoZGVyaXZlZCB2
ZXJiYXRpbSBmcm9tIHRoZSBoYWx0ZWQgYzk4N2ExYTY7IHN0YWdlZCBleGVjdXRpb247IEhlcm1p
dGlhbiBmb3JtIG9mIHJlY29yZCwgcHJvZHVjdC1mb3JtIGNyb3NzLWNoZWNrcyBhdCBrYSA9IDAu
MyBhbmQgMC4wMTg3NSkuIENoZWNrcG9pbnQgKio1ZWUxNTJmYyoqICg0Myw2NDcgQik7IHN0YWdl
IGZpbGVzIG5iMjQgZTQ5NzUwNTAgLyBuYjMyIDNiZmRiNDhlIC8gbmI0MEdLIDJiMDM3ODM2IC8g
bmI0MEdNIDY3OTQ2ZDk1OyBkaWFnbm9zdGljIGFuYWx5c2lzIGJkZmQzZDAxLgoKIyMgV0FSRC3O
kyB1bmRlciBBLTE6IFBBU1MgYXQgbl9iID0gMjQsIDMyLCA0MAooYSkgYW5hbHl0aWMtbW9kZSBX
YXJkIHJlc2lkdWFsIDIuM8OXMTDigbvCucKyIOKApiAyLjPDlzEw4oG7wrnCuSAo4omkIDEw4oG7
4oG5KTsgKGIpIEhlcm1pdGlhbiBHb2xkc3RvbmUgfM+JwrJ8IDEuMsOXMTDigbvigbkgLyAzLjDD
lzEw4oG74oG5IC8gOC4xw5cxMOKBu+KBuSAo4omkIDEw4oG74oG4KSB3aXRoIM67X21pbihMKSA9
ICsxLjbDlzEw4oG7wrnigbQgYXQgzpMgYW5kIG5vIM67X21pbiA8IOKIkjEw4oG7wrnCsiBhdCBh
bnkgbGFkZGVyIG9yIHNwZWVkLXNldCBrICh0cmFja2VkIGF0IGV2ZXJ5IHNvbHZlKS4gUHJvZHVj
dC1mb3JtIGNyb3NzLWNoZWNrczogMi4xw5cxMOKBu+KBuSAvIDMuNcOXMTDigbvigbggLyAzLjbD
lzEw4oG74oG4ICh0aGUgSC1TMkMtNSBmbG9vciwgYXMgZGlhZ25vc2VkKS4KCiMjIENoYW5uZWwg
aWRlbnRpZmljYXRpb24gYW5kIHNwZWVkcwpUaGUgUzIvcXVhZHJ1cG9sZSBicmFuY2ggaWRlbnRp
ZmllcyB1bmFtYmlndW91c2x5OiBv4oKCID0gMC45OTk5OTk5OSBhdCBldmVyeSBydW5nLCBib3Ro
IGRpcmVjdGlvbnMgKCoqRi1NSVggUEFTUyoqLCDOuF9pZCA9IDAuOTApLiBUaHJlZSBnYXBsZXNz
IGJyYW5jaGVzLCBr4oaSMDogVCA9IDUuMDQ4MTPigJM1LjA0ODIwLCBhbmQgdGhlIHR3byBjb21w
cmVzc2lvbmFsIGJyYW5jaGVzIDkuNjgwNTkgYW5kIDMuNzQxMzYgKHN1YnN0cmF0ZSB1bml0cyku
ICoqRi1JU08gUEFTUzoqKiBjX1QozpPigJNLKS9jX1QozpPigJNNKSDiiJIgMSA9IDEuM8OXMTDi
gbvigbUgKM64X2lzbyA9IDElKS4gRnJhbWV3b3JrLWxhYmVsIFJfVCA9IGNfVC9jX0wxID0gNS4w
NDgyLzkuNjgwNiA9ICoqMC41MjE0NyoqIHZzIHRoZSBHLVRTSDMgZ2VtOCByZWNvcmQgMC41MTc2
NyAoMC43MyU7IHRoZSByZWNvcmQgaXMgYXQgdGhlIGZpcnN0LXBhc3NpbmcgY29udmVudGlvbiwg
dGhpcyBpcyB0aGUga+KGkjAgZXh0cmFwb2xhdGlvbikg4oCUIHRoZSBzdWJzdHJhdGUgaXMgdGhl
IGZyYW1ld29yaydzLgoKIyMgRi1ESVNQIChFLTQgd2luZG93LCBFLTUgdGhyZXNob2xkcykKRWxl
Y3RlZCBlc3RpbWF0b3IgKHNwZWVkIGZyb20gdGhlIHNtYWxsLWsgc2V0LCB0aGVuIHIgPSBh4oKC
KGthKcKyICsgYeKChChrYSnigbQpLCBuX2IgPSA0MDogKiph4oKCID0g4oiSMS4yODLDlzEw4oG7
wrIgKM6T4oCTSzsgQ0kgNi44w5cxMOKBu8KzKSwg4oiSMS45MznDlzEw4oG7wrIgKM6T4oCTTTsg
Q0kgNC40w5cxMOKBu8KzKSoqOyBh4oKEIHVucmVzb2x2ZWQgKENJIH4xKS4gU2lnbiBzdGFibGUg
YXQgZXZlcnkgbl9iIGFuZCBpbiB0aGUgQS0xIGZsb29yLXdlaWdodGVkIGZpdCAo4oiSMS4yODTD
lzEw4oG7wrIgLyDiiJIxLjk1NcOXMTDigbvCsikuIHxh4oKCfCBleGNlZWRzIM+EID0gMTDigbvi
gbYgYnkgMTDigbQgYW5kIGl0cyBvd24gaW5mbGF0ZWQgQ0kgYnkgMS45w5cgLyA0LjTDly4KCioq
Ri1DT05WIGF0IHRoZSBQaGFzZS0wLWZpeGVkIHRocmVzaG9sZHM6IEZBSUwqKiAoY19UIHJlbCAz
MuKGkjQwID0gMS4yw5cxMOKBu+KBtSB2cyAxMOKBu+KBtjsgYeKCgiBhYnMgMzLihpI0MCA9IDnD
lzEw4oG74oG0IHZzIDEw4oG74oG3KS4gTWVjaGFuaXNtLCBtYWNoaW5lLXZlcmlmaWVkOiB0aGUg
MzLihpI0MCBjaGFuZ2UgaW4gcl9UIGlzIGEgdW5pZm9ybSDiiYgxLjLDlzEw4oG74oG1IG9mZnNl
dCBhY3Jvc3MgYWxsIHJ1bmdzIGZyb20gMC4zIHRvIDAuMDE5IOKAlCBhIHNoaWZ0IG9mIHRoZSBz
cGVlZCBleHRyYXBvbGF0ZWQgZnJvbSB0aGUgc21hbGwtayBzZXQsIHdoZXJlIHRoZSBBLTEgZGVu
c2UgZmxvb3IgaXMg4omIMS41w5cxMOKBu+KBtSBpbiByIOKAlCB3aGlsZSB0aGUgVC1icmFuY2gg
z4kgYXQga2Eg4omlIDAuMDM3NSBhZ3JlZSBhY3Jvc3Mgbl9iIHRvIH4xMOKBu+KBti4gRElBR05P
U1RJQyAobm90IHRoZSBlbGVjdGVkIGVzdGltYXRvcik6IHRoZSBjLWZyZWUgam9pbnQgZml0IG9u
IGZsb29yLWNsZWFuIHJ1bmdzICjPg19yIDwgM8OXMTDigbvigbcpIGNvbnZlcmdlcyBhY3Jvc3Mg
bl9iIHRvIOKJpCAzw5cxMOKBu8KzIHJlbGF0aXZlIOKAlCAqKmHigoIgPSDiiJIxLjI3OcOXMTDi
gbvCsiAozpPigJNLKSwg4oiSMS45OTPDlzEw4oG7wrIgKM6T4oCTTSk7IGHigoQgPSDiiJIzLjDD
lzEw4oG7wrMsIOKIkjguM8OXMTDigbvCszsgY19UID0gNS4wNDgyMCAvIDUuMDQ4MTcqKiDigJQg
YW5kIHRoZSBhbGwtcnVuZyBqb2ludCBmaXQgYXQgbl9iID0gNDAgY29sbGFwc2VzICjiiJI0LjjD
lzEw4oG7wrMpLCB3aGljaCBpcyB0aGUgZmxvb3IgZG9pbmcgZXhhY3RseSB3aGF0IEEtMSBzYXlz
IGl0IGRvZXMuCgojIyBBcm0KLSAqKk1lY2hhbmljYWwgYXJtIGF0IHRoZSBlbGVjdGVkIHRocmVz
aG9sZHM6IEE1IElOU1RSVU1FTlQtTElNSVRFRCoqIChGLUNPTlYgY2xhdXNlKS4gVGhlIGluc3Ry
dW1lbnQgY2Fubm90IGNlcnRpZnkgYeKCgiB0byAxMOKBu+KBtyBhYnNvbHV0ZSDigJQgYSBwcmVj
aXNpb24gZGVzaWduZWQgZm9yIHRoZSBuZWFyLWNvbmUgcmVnaW1lLgotICoqU3Vic3RhbnRpdmUg
Y2hhdC1sZWcgaW5kaWNhdGlvbjogQTMgRElTUEVSU0lWRS1PKGvCsikqKiDigJQgdGhlIFMyIGNo
YW5uZWwgb2YgdGhlIGdlbTggcDZtIHN1cGVyc29saWQgaW5oZXJpdHMgTyhrwrIpIGRpc3BlcnNp
b24gYXQgdGhlIDHigJMyJSBsZXZlbCwgZGlyZWN0aW9uLWRlcGVuZGVudCBhdCBPKGvCsikgd2l0
aCBhbiBpc290cm9waWMgc3BlZWQsIHRoZSBzYW1lIHBhdHRlcm4gYXMgdGhlIGhhcm1vbmljIHA2
bSBjb250cm9sICjiiJIxLzk2IHZzIOKIkjEvMzIpLiBUaGUgcmVnaXN0ZXJlZCBNLW5haXZlIGV4
cGVjdGF0aW9uIChESVNQRVJTSVZFKSBpcyByZWFsaXplZC4gVGhlIHZlcmRpY3QgaXMgdHdvLWxl
Zzsgbm90aGluZyBoZXJlIHRvdWNoZXMgV1/iiKouCgoqKlByb3Bvc2VkIEFtZW5kbWVudCBBLTIg
KGF1dGhvcidzIGNhbGw7IG5vdCBhcHBsaWVkKToqKiBGLUNPTlYgb24gYeKCgiByZWdpbWUtYXBw
cm9wcmlhdGUg4oCUIGFic29sdXRlIDEw4oG74oG3IHdoZW4gfGHigoJ8IOKJpCAxMM+ELCByZWxh
dGl2ZSAxMOKBu8KyIHdoZW4gfGHigoJ8ID4gMTDPhDsgc3BlZWQgcmVmZXJlbmNlIGFuZCBjb252
ZXJnZW5jZSBhc3Nlc3NlZCBvbiB0aGUgYy1mcmVlIGpvaW50IGVzdGltYXRvciBvdmVyIGZsb29y
LWNsZWFuIHJ1bmdzICjPg19yIDwgMTDigbvigbYpLCB0aGUgZGVuc2UgZmxvb3IgY2FycmllZCBh
cyB0aGUgQS0xIHRlcm0uIFVuZGVyIEEtMiB0aGUgcHJlc2VudCBsYWRkZXIgaXMgQTMgd2l0aCBG
LUNPTlYgUEFTUyAo4omkIDPDlzEw4oG7wrMpLiBVbmRlciBQRi1TMiwgQTMg4oeSIFdf4oiqIHN0
YXlzIHN1c3BlbmRlZCBhbmQgV1/iiKrigLIgaXMgcmUtZGVyaXZlZCBmcm9tIHRoZSBh4oKCIHNj
YWxlIOKAlCBhZnRlciB0aGUgQ0MgbGVnIGFuZCB0aGUgYWdncmVnYXRlIHByb2JlLgoKIyMgSG9u
ZXN0eSBsZWRnZXIKLSAqKkgtUzJDLTYqKiB0aGUgZmlyc3QgbGFkZGVyIHJ1biB3YXMgdGVybWlu
YXRlZCBieSB0aGUgc2FuZGJveCB0b29sIHRpbWUgbGltaXQgYXQgbl9iID0gNDAgzpPigJNNIGJl
Zm9yZSB3cml0aW5nIGl0cyBjaGVja3BvaW50IChsb2cgcHJlc2VydmVkOiBnX3MyYzFfcGhhc2Ux
X2xhZGRlcl9ydW4xX2tpbGxlZC5sb2cpOyBhIGJhY2tncm91bmQgcmVsYXVuY2ggZGlkIG5vdCBz
dXJ2aXZlIHRoZSB0b29sIGNhbGw7IHRoZSBpbnN0cnVtZW50IHdhcyByZXN0cnVjdHVyZWQgaW50
byBzdGFnZSBmaWxlcyAodGhlIEU4IGxlc3NvbiwgYWdhaW4pIGFuZCByZS1ydW4gd2hvbGUg4oCU
IGV2ZXJ5IG51bWJlciBhYm92ZSBpcyBmcm9tIHRoZSBzdGFnZWQgcnVuLgotICoqSC1TMkMtNyoq
IHRoZSBjbGFzc2lmaWVyJ3MgIkwxIi8iUEgiIGxhYmVscyBhcmUgc3dhcHBlZCByZWxhdGl2ZSB0
byB0aGUgRy1UU0gzIGNvbnZlbnRpb24gKGl0cyAiTDEiIGlzIHRoZSAzLjc0MSBicmFuY2gpOyB0
aGUgZnJhbWV3b3JrLWxhYmVsIFJfVCBpcyByZXBvcnRlZCBhbG9uZ3NpZGU7IHRoZSBUIGNoYW5u
ZWwgaXMgdW5hZmZlY3RlZC4KLSAqKkgtUzJDLTgqKiB0aGUgZWxlY3RlZCBzcGVlZC1zZXQgZXN0
aW1hdG9yIGlzIGZsb29yLXNlbnNpdGl2ZSBhdCBzbWFsbCBrYSBpbiBhIHdheSB0aGUgUGhhc2Ut
MCBjb250cm9sIChhbmFseXRpYywgZmxvb3JsZXNzKSBjb3VsZCBub3QgcmV2ZWFsOyBkaXNjbG9z
ZWQgd2l0aCB0aGUgbWVjaGFuaXNtOyBBLTIgcHJvcG9zZWQgcmF0aGVyIHRoYW4gc2lsZW50bHkg
c3dpdGNoaW5nIGVzdGltYXRvcnMuCgojIyBSZWFkaW5lc3MgZm9yIFBoYXNlIDIvMwotICoqQ0Mg
bGVnICh0d28tbGVnKToqKiByZWFkeSB0byBkaXNwYXRjaCB1bmRlciBQLTQgKyBQLTQuYiAoYmFz
ZTY0IGFybW9yKSB3aXRoIHRoZSBBLTEgd29yZGluZzsgQS0yIHNob3VsZCBiZSBkZWNpZGVkIGJl
Zm9yZSBkaXNwYXRjaCBzbyBib3RoIGxlZ3MgcnVuIHRoZSBzYW1lIEYtQ09OViBjbGF1c2UuCi0g
KipBZ2dyZWdhdGUgcHJvYmUgKFAyKToqKiBpbnB1dHMgaW4gaGFuZCAoY19ULCBjX0wxLCB0aGUg
VC1icmFuY2ggYeKCgi9h4oKELCB0aGUgYmFua2VkIEctUE9MWTEgUV9UIHF1YXJ0ZXQpOyB0aGUg
UmF5bGVpZ2ggZ3JhaW4tc2NhdHRlcmluZyBpbnN0cnVtZW50IG5lZWRzIHJlY292ZXJ5IGZyb20g
dGhlIENDIHJlcG8gKG5vdCBpbiBwcm9qZWN0IGtub3dsZWRnZSkuCg==
<<<EMBED-END name=G_S2C1_PHASE1_LADDER_REPORT.md>>>

### EMBED — chat banked gem8 state (binary) — `psi0_gem8_n64.npy` (md5 a56796186e5eaf78c2e513fc710cb143, 32896 B, b64, QUARANTINED)

<<<EMBED-BEGIN name=psi0_gem8_n64.npy md5=a56796186e5eaf78c2e513fc710cb143 bytes=32896 enc=b64 quarantine=1>>>
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
MiIb0iiM3z+G7ON+ZuvfP8Vw/3aiI+A/nk0gByVP4D8f6fNjgXfgPxSfJU4GnOA/nnScfg+84D9K
70oGCtfgP8xBPz547OA/eU/eKPX74D8HmJcqNwXhP6pZFAYSCOE/IwO2DXgE4T+e8QqCevrgP+iD
qxpJ6uA/5uC4vDDU4D9zvAJombjgP/PurGkDmOA/uPT96ANz4D9sW63oQErgP/YLX9xsHuA/hvVW
7YPg3z+mxpav+oDfP9IPso60H98/ngyDSBu+3j/QuWdpg13ePyQo7fgk/90/RFkwdRWk3T/asD1Q
Q03dP+KJJhFz+9w/mtoNJz6v3D+wwk5oE2ncP5j4aCQ5Kdw/ojbMndDv2z/uQ/ix2rzbP0Bcc2s9
kNs/yBQ7Mspp2z+8KZZMREnbP/yiRWNnLts/eNt1wO0Y2z8cZsgHlgjbPwn3nS4o/do/tq23hXn2
2j85ncavb/TaP05pKWsC99o/bCm0Hzz+2j9utuErOQrbPz7kRfclG9s/q6qd2jsx2z/MZ3n4vEzb
Pzw7JSzvbds/4oDoPhaV2z9vW4ydbcLbP8aqutAh9ts/zGF8AUow3D8teCfX4XDcPzQhufzDt9w/
IU1jmKUE3T8/uwhm70/dP1QotrPOe90/uy/caE+r3T+UI72b3d3dP0t7/hfCEt4/4/LsiCZJ3j/G
W6n0GoDeP8KmolGctt4/mG0k9Jvr3j9YneqJBx7fP2M5yFXRTN8/HXpZXfh23z+5agM+kJvfPz2K
jmTIud8/rXjBavLQ3z9LM9Fnh+DfP7dbqgos6N8/q8uNX7Pn3z8Q7PIsIN/fP47X/92kzt8/Ynsv
+6G23z/Wjwc8o5ffPyYmIUdbct8/5MdAQJ5H3z/WAq5OWxjfPwISGVCV5d4/UG6u9Vqw3j8WUtyQ
vnneP/b5ENvNQt4/brGlBooM3j8Kw6hm4NfdP6IH4fajpd0/sjUbBYh23T/028owHEvdP+631ubJ
I90/GoXobdMA3T9wlOWEVOLcP4QIiYJEyNw/2Cer03my3D9UK6qmrqDcP7ivgoaGktw/3Kz6n5SH
3D9KOwNnYn/cP5Dc/1F2edw/hjqKY1p13D/uG/JAonLcP98PbZvwcNw/GO7zuvtv3D8kSJEDkW/c
P73j7VeXb9w/PvDvRRBw3D9qiSv0F3HcP4zrtdDjctw/ciPBC8B13D/chVPyC3rcPxhGeEc1gNw/
yA5NxLKI3D/ZwQbx/ZPcP9YO85GMotw/0jf96sm03D+LpJwhEMvcPxymnwei5dw/JE1jmKUE3T/N
ilZtHyjdPw==
<<<EMBED-END name=psi0_gem8_n64.npy>>>
