# Staging Memo — Joint Fold: G-2a-S1 + G-2a-S2

**Status:** Both gates two-leg verified. G-2a-S2's sharpest claim (A₃-even restriction)
additionally corroborated by a third, sampling-free algebraic derivation (chat-side,
this session). Ready for staged fold. Not yet folded — SQT's to run.

---

## Entry (proposed canonical text)

**G-2a-S1/S2 — Soliton spin-isospin quartet: forced-but-conditional (R2).**

The Route-1 necessary-condition screen (G-2a-S1) establishes that IF the baryon soliton
carries octahedral (2O) rotational symmetry, the spin-3/2 quartet is FORCED and unique
(D1=1: 2O's genuine sector has irreps {2,2,4}; χ_{3/2} is the only 4-dim one, selected by
the FR/spinor-phase condition χ(−1)=−4). The locked spin-SU(2) cannot be hosted inside
color-SU(4) (D2=2, abelian commutant) and must be a transverse factor — supplied by the
ℂ⊗𝕆⊗ℍ arena already forced by the distinct-4 obstruction.

The Route-2 symmetry screen (G-2a-S2) tests whether the canonical topological-linking
representative (three mutually perpendicular golden ellipses, a=φ, b=1/φ; the Borromean
config used throughout §3.4-G2/§3.09) supplies that octahedral symmetry. It does not:
|G_rot| = 12 = T = A₄ (2T = SL(2,3), genuine irreps {2,2,2}, no 4-dim irrep), no C4. The
mechanism is structural, not numerical accident: octahedral symmetry requires C4, and any
C4 about a coordinate axis maps a major axis to a minor axis of a *different* ellipse
(since φ≠1/φ), which is not in the config — this failure is forced by the same eccentricity
that (per Freedman–Skora, §2.82) is required for the ellipses to realize the Borromean
rings without self-intersection in the first place. Round (circular) ellipses would restore
C4 but cannot form Borromean rings. So the planar three-ellipse representative is
**structurally capped at tetrahedral** — this is not a search artifact.

**NC5 disposition:** the rotational symmetries induce only the cyclic (even) strand
permutations {e, (123), (132)} — never a transposition. Acting on the color-singlet ε^{abc},
even permutations contribute only sgn=+1, so color charge is preserved under all admitted
spatial rotations. NC5 is therefore BENIGN for a color-singlet baryon: no spin↔color leakage
via this mechanism. (Independently re-derived, not just asserted: the induced ellipse-
permutation is π = m⁻¹ρm for the valid ρ, landing in the same even subgroup for all three.)

**Net disposition (R2, conditional):** the spin-3/2 / μ_n factor-of-4 is forced *given*
octahedral soliton symmetry (S1), but the topological-linking representative used to date
does not carry that symmetry (S2) — it caps at tetrahedral, with no 4-dim genuine irrep.
**The octahedral premise is a located M.ONT/core-geometry import**, not a structural
consequence of the topology, and not refuted. The topology (Borromean linking) is
config-independent; the symmetry is config-dependent, and the physical baryon's realized
symmetry may be richer than this minimal representative (via the K₇-tube/Szilassi/relaxed
core). Whether the richer core geometry is simultaneously octahedral *and* Borromean is now
the standing open question — flagged, not resolved.

**M.CW ceiling:** R2 throughout. No dynamics computed; the dynamical locking (does the
energy-minimizer actually realize whatever symmetry the core has) remains open (Routes 2/3
continuation). Assignment I vs II untouched by both gates.

## Verification trail

- **G-2a-S1:** chat-side `g_2a_s1_screen.py` (quaternion enumeration, cos-sum characters,
  own commutant solver) + CC second leg `d89f591` (SU(2) matrix-closure, Chebyshev
  characters, conjugacy-class D1 computation, independent nullspace solver). D1, D2, χ
  values agree exactly across zero shared machinery.
- **G-2a-S2:** chat-side `g_2a_s2_symmetry.py` (B3 brute-force point-cloud search) + CC
  second leg `ec644c0` (M1: sampling-free axis-permutation/signature argument; M2: own
  independent sampling) + chat-side third-method audit (this memo's session: conjugation
  argument ρm²=m²ρ, centralizer of a 3-cycle in S₃, algebraic — no sampling, no point
  cloud). All three agree: |G_rot|=12, T=A₄, no C4, even-only strand permutations.

## Imports declared

- G-2a-S1: none beyond finite-group/rep theory (R2 ceiling stated in its own pre-reg).
- G-2a-S2: the octahedral premise for the *physical* (core) baryon symmetry is now named
  as a live, unresolved import — location, not derivation, not refutation.

## Provenance

`G_2a_S1_PREREGISTRATION.md`, `g_2a_s1_screen.py`, `G_2a_S2_PREREGISTRATION.md`,
`g_2a_s2_symmetry.py` — all in outputs. CC commits d89f591, ec644c0.

## Forward pointer (not part of this fold)

The next bounded gate this surfaces: does the K₇-tube/Szilassi relaxed-core geometry admit
octahedral rotational symmetry while remaining a genuine (non-self-intersecting) Borromean
three-strand structure? This is the M.ONT/core-geometry chokepoint the S1/S2 pair converges
on, and the natural Route-2-continuation target.

§2.52 untouched. No observable bridge crossed (M.BRIDGE intact — this is admissibility, not
a derived constant).
