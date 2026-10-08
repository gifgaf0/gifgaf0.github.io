# A1 — Polarization gate: two-leg comparison, verdict and blast radius

**Plain-language summary.** Two independent derivations agree on every number: the wave that the ledger uses as its gravitational-wave channel is a vector wave, with no tensor part at all. Under the rule fixed in advance, the reading that gravitational waves share light's transverse channel is ruled out by the LIGO–Virgo polarization test of GW170817, which prefers a tensor wave over a vector wave by a factor of about 10²¹. The ledger's "GW170817 structural pass" is withdrawn wherever it appears, and the transverse line keeps only its light carrier. The framework is left with no carrier for gravitational waves.

**Pre-registration:** `A1_PREREG.md` md5 `d5f6aa3bd50743c5d69e54338494bb27`, locked by commit `44e12de` (pushed 2026-10-06 22:55 PDT) before any derivation existed. **Addendum 1** (`A1_PREREG_ADDENDUM_1.md`) was filed after the second leg returned and before this record: it adds the reading-Λ evaluation and changes nothing else.

---

## 1. Two-leg comparison (the step that decides the verdict)

| item | first leg (`a1_derivation.py`, 43 checks) | second leg (blind, `leg2/leg2_derive.py`, 74 checks) | agreement |
|---|---|---|---|
| Λ(k̂) sym(k̂⊗a) | ≡ 0, exact (rational parametrization) | ≡ 0, three proofs (spherical, polynomial mod \|k\|² = 1, general lemma) | identical |
| transverse wave, six-tensor coefficients | c_x = ½cosχ, c_y = ½sinχ, rest 0 | same | identical |
| longitudinal wave | c_l = 1/√2, rest 0 (no breathing) | same | identical |
| common grid (240 points × 7 numbers) | `leg1_grid.json` | `leg2_grid.json` | **max \|Δ\| = 3.3×10⁻¹⁶ over 1,680 values** (criterion 10⁻¹⁰) |
| spin weight in ψ | S2: \|m\| = 1 only; longitudinal: m = 0 only; tensor control \|m\| = 2 | same, plus finite arms (L/λ = 0.3) | identical |
| detector made of the medium | S = κ·D:ε, κ = 2(β − 1 − α₂/2) (vertical probe) or 2(β − 1 − α₂/2 + α₃/2) (perpendicular) | G = (1−β′)(x̂x̂−ŷŷ) − γ(ê₁ê₁ − ê₂ê₂); same two cases | identical up to notation (β′ − 1 ↔ α₂/2, γ ↔ α₃/2; lab vs material frame) |
| motion-induced TT fraction (reading Λ) | 0.67 (v/c)², phase normal | 0.65 (v/c)² phase normal; 2.6 (v/c)² ray; 0 tilted axis | consistent |
| second order | — | genuine ±2 at relative 10⁻²¹ (power 10⁻⁴²) | — |

The second leg also checked what the first leg did not: finite arms, non-universal mirror offsets (an equivalence-principle-violating dipole term, still spin weight ≤ 1), and multipath through texture (TT fraction ≲ 5×10⁻¹⁸). **No miss; no S9.**

## 2. Verdict

**The S2 response has no tensor component.**
- Reading S (spin weight): exactly none, at linear order, for any medium, any coupling and any detector motion.
- Reading Λ (TT projection): none in the untextured aggregate with the detector at rest. The bounded projections come from detector motion (≤ 2.6 (v/c)² ≈ 4×10⁻⁶ in power), texture (≈ 10⁻¹² in power) and second order (≈ 10⁻⁴²). Per Addendum 1, such a component would contribute a signal-to-noise ratio of at most 32.4 × √(4×10⁻⁶) ≈ 0.07 to GW170817. It is invisible, so the signal is effectively pure vector and the pure-vector comparison applies.

**Both readings lead to clause 1 of the locked rule.**

1. **FALSIFIED:** the reading "the spin-2 radiative sector shares the transverse channel". GW170817, with its sky position fixed, favours pure tensor over pure vector at log₁₀ B = 20.81 ± 0.08 (PRL 123, 011102 (2019)). With waveforms whose inclination dependence matches vector radiation, ln B = 21.1, or 51.0 with the jet prior (PRD 103, 064037 (2021)). GW170814 gives B > 200. GWTC-3 finds no evidence for non-tensor modes, pure or mixed.
   - R-2 rules out a vector+scalar escape: no helicity-0 branch of the substrate is on the light cone (c₂/c_T ≈ 0.06, c₁/c_T ≈ 2.0–2.2), so nothing could accompany the signal.
   - The ledger's own G-CI1 rule P-POL ("{±1}-only → FAIL"), never run, gives the same answer.
2. **WITHDRAWN wherever it appears:** the GW170817 "structural pass". See the list below.
3. **The transverse line keeps only the EM carrier.** CI-W/EM-IN's "S2 on the cone by assumption" now has no candidate carrier anywhere in the substrate: K = ∅, and the field content has no propagating rank-2 field (A1_DERIVATION §5). The gravitational-wave sector is an unaccounted-for import.

**Secondary arms** (no decision weight):
- The double pulsar cannot confirm a vector channel. Its total power fixes a coupling; a Maxwell-type channel of Newtonian static strength radiates ¼ of GR's power.
- Pulsar timing: the S2 reading predicts the vector correlation curve ½[3 ln(2/(1−cos ξ)) − 4 cos ξ − 3], not Hellings–Downs. NANOGrav's HD preference (B = 200–1000) is mildly adverse; vector modes are untested there.

**Register.** The kinematic and antenna results are R1 (exact, two-leg). The verdict is R1 against the locked rule and the cited Bayes factors.

**Process finding (honesty item H-POL-1).** G-CI1 had already named this reading (CI-V, "the S2 sector is the helicity-±1 transverse acoustic wave itself"). It foreclosed CI-V as vocabulary substitution and set a tripwire (PF-3) with A-POL as its first surface. G-S2C1's election E-P2-1(a) adopted the same reading in substance two weeks later, and the tripwire did not fire. Proposed process pin: any election that re-identifies a radiative species must be screened against the PF list of the gate that defined that species.

## 3. Blast radius: every entry that leans on the GW pass or on c_GW = c_EM by carrier identity

Found by a full grep of V4.91 for GW170817, c_GW, carrier identity, spin-2, S2, tensor-vs-EM, W_∪, GW-side, species universality, A-SHEAR, two descriptors and radiative species. All are annotated in the Phase A fold (V4.92); no body text is changed.

| entry | what it leans on | annotation |
|---|---|---|
| M.ONT coupling-class annex (V4.65) | "A-SHEAR … the envelope-as-transverse-carrier consonance stays R3" | the consonance can concern the EM carrier only |
| M.ONT vacuum-composition annex (V4.66) | grounds include "the A-SHEAR transverse-carrier consonance" | that ground now covers the EM carrier only; the other grounds stand |
| ANNEX-CDEF-1 (iii)–(iv) (V4.71) | "EM and the spin-2 radiative sector share the one transverse channel"; "the GW170817 structural pass restates as single-channel carrier-identity consistency" | shared-channel claim falsified; pass withdrawn; the units election (c := the EM carrier's speed) stands |
| §2.88.E GW170817 reframe (V4.35) | "c_T = c_EM is structural … reads as a passed consistency test" | withdrawn |
| §2.91.A disclosure (V4.63) | "the GW170817 transverse-sector structural pass … motivated A-SHEAR" | that pass is withdrawn |
| §2.91.B A-SHEAR (V4.63) | "EM and emergent spin-2 radiative sectors both propagate on the transverse channel … required for the GW170817 structural pass" | spin-2 clause falsified; the EM clause remains an assumption |
| §2.91.D kill set (V4.63) | — (independence clause only) | the standing equivalence-principle kill condition KC-EP is added here (A4) |
| §2.91.H (V4.67) | "the A-SHEAR/transverse statements (c_T ≡ c; the GW170817 structural pass) … continue" | the pass does not continue; c_T ≡ c continues as the units election |
| §2.91.I Q3 item (1) (V4.68) | the carrier-identity claim | spin-2 half falsified; EM carrier only |
| §2.91.M G-POLY1 (V4.74–V4.76) | W_∪ governed by "GW170817-class transparency" of the S2 channel | GW-side window moot; the EM-side window is unaffected |
| §2.91.N G-CI1 (V4.77) | "the radiative B-2 burden transfers to the S2-on-cone assumption"; A-POL voided | CI-V adopted later without A-POL; run now, it fails; S2-on-cone has no candidate carrier |
| §2.91.O G-S2C1 / G-S2C1-W (V4.80–V4.81) | E-P2-1(a): "the aggregate S2 channel is the polarization-averaged shear cone itself" | E-P2-1(a) is CI-V; as a GW carrier it fails; dispersion numbers stand; W_∪′ moot |
| §2.91.Q G-MSCS1 (V4.83) | "EM and S2 are two descriptors of the one transverse phonon" | S2 carries no GW content; the identity and κ₂ stand as statements about two weightings of the EM carrier |
| §2.91.S G-MSCS2 (V4.85) | the S2-E₂ descriptor | as for §2.91.Q |
| §2.91.T G-MSCS-A (V4.87) | the sealed anchor bounded "the fractional tensor-vs-EM speed difference" | with no tensor carrier, the window constrains nothing observable: reading withdrawn, numbers stand |
| Part V polycrystal row (V4.73) | the GW-side window | moot; the EM-side window stays |
| Part VI rows G-TSH1, G-POLY1, G-CI1, G-S2C1, G-S2C1-W, G-MSCS1, G-MSCS2, G-MSCS-A | the readings above | one short pointer each |

**Not annotated:** the fold-in records and the As-of history, which are historical logs. The new V4.92 record and the As-of prepend name the withdrawal. **Public documents to correct** (Phase B): `STATUS.md` ("Light and gravitational waves in one channel: partly settled") and any paper text that counts GW170817 as passed.
