# SQT Framework — Five Perspectives

**Date:** 2026-06-03
**Status:** Review document (no new T1/T2 claims; all assertions are reviewer
judgement unless they cite an existing ledger result).
**Scope reviewed:**
- Canonical ledger `tools/SLWE_Prime_Master_v2.md` (SQT-SLWE crypto subproject)
- `tools/sqt_slwe.py`, `tools/sqt_cryptanalysis.py`
- Immersive file `index.html` (Superfluid Quantum Topology — Geometric Mass Calculator v3)
- Grounding: `paper/X1_cos18_address.md`, `reports/seven_circles_report.md`

> **Method.** Five distinct disciplinary lenses, each structured as:
> *Stance → What genuinely holds up → The single load-bearing crack →
> One falsifiable next test.* Each lens is grounded in specific artifacts.
> Tier/Register language follows the ledger's own §0 conventions.

---

## Perspective 1 — The Concrete-Hardness Lattice Cryptographer

**Stance.** I price security in BKZ block size β against the *flattened*
lattice an adversary actually attacks in ℤ_q^512. I do not care what algebra
you used to *build* A; I care what geometry I see.

**What holds up.**
- The adjoint identity `lmm(a)ᵀ = lmm(conj(a))` is T1 and the conjugate-norm
  inner product makes decryption exact (0 violations). That is real and the
  correctness story is clean.
- The honesty is exemplary: §4.4 and §8 already state the load-bearing
  unproven claim out loud, and OP-G is logged rather than buried.
- The honeypot/canary key-ladder (§3) is genuinely novel — see Perspective 5.

**The load-bearing crack — the symmetry/rank dilemma.**
Brief 05 found the *pure* Singer A has F_p-rank **76 of 512** (column period
112). At that rank the primal lattice dimension is ≤ 112 and the security
table is void. Brief 06 restores rank 512 — but the ledger states it plainly:
at δ ≥ 1 over F_p the randomised matrix is *distributionally identical to a
uniform random matrix, and the PSL(2,7) symmetry in A is gone*. So:

> **You can have the PSL(2,7) structure (rank 76 → broken) or full rank
> (structure gone → vanilla Module-LWE). You cannot currently have both.**

This collapses the central thesis to a defensive one. The "algebraic shield"
(100% homomorphism failure) and "geometric shield" (five lattice tests) are
arguments that the sedenion structure *does not hurt* security — not that it
*provides* any. With the Brief-06 wrapper, SQT-SLWE's security is **parasitic
on standard Module-LWE at n=512**; the sedenion machinery is security-neutral
dressing. The §8 admission is exactly right: a lattice attacker works in
ℤ_q^512 and never engages 𝕊, so "non-associativity prevents folding" defends
against an attack the adversary is not obliged to mount.

Two unresolved sub-cracks:
- **GSO tail (Test 3, INVESTIGATE).** Steeper profile at indices 48–63 at
  N=64 is flagged but never re-run at N=512 *with the randomised
  construction*. Until then the geometric shield is unmeasured at scale.
- **Test 5 fixed-point subspace.** dim ker(P−I)=16 is dismissed because "A
  does not preserve it" — but a hybrid/dual attacker who *knows* the Singer
  origin may still use that 16D structure as a guessing coordinate. Untested.

**Falsifiable next test.** Run the public `lattice-estimator` (Albrecht et al.)
on the flattened lattice produced by `singer_a_randomized` at k=32, q=3329,
and report primal **and** dual **and** hybrid β — not the hand-rolled
`beta_from_delta` in `sqt_cryptanalysis.py`. Simultaneously confirm DFR ≤ 2⁻¹²⁸
at those parameters (current toy DFR is ~48% at k=4, q=911). If the estimator
returns the same β as a uniform random A of the same dimension, that *confirms*
the parasitic-security framing — which is publishable as
"Module-LWE with a security-neutral algebraic construction," provided the
sedenion claim is dropped from the security argument.

---

## Perspective 2 — The Division-Algebra Algebraist

**Stance.** I evaluate the sedenion/PSL(2,7)/Fano machinery as mathematics,
independent of any application. Is it correct, is it new, and does any of it
carry *hardness*?

**What holds up.**
- The 84 zero-divisor pairs, the K₇,₇-minus-perfect-matching graph, 6-regular
  bipartite, vertex/edge-transitive, Aut ⊇ S₇≀ℤ₂, prime-independence over
  F_p — all T1 and all correct. This is a clean, reproducible result.
- The chain-probe handling of OP §2.24.2 is the intellectual high point: the
  "2×21 Fano decomposition" was tested, found to be a **coordinate phenomenon
  equivalent under the PSL(2,7) action already present**, and *demoted* rather
  than promoted. That is precisely the right instinct (the Eddington filter
  working as designed).

**The load-bearing crack — OP §2.24.4, and it almost certainly resolves
against you.** The ledger itself flags this as "Critical for PQC": *is
zero-divisor membership polytime via Moreno's explicit classification?*
Moreno's classification of zero divisors in the sedenions (and the general
Cayley–Dickson picture) is *constructive and polynomial* — the ZD locus is the
cone over an explicit low-dimensional variety, and membership reduces to a rank
/ linear-algebra check. So the working assumption should be **yes, polytime**,
which means **no hardness can ever come from ZD membership**, exactly as the
ledger's own §2.24.4 warns. Any PQC direction that leans on ZD structure as a
primitive is dead on arrival; the construction is right to have pivoted to a
lattice (Module-LWE) primitive — but that pivot is also what made the algebra
security-neutral (Perspective 1).

Also flag, as T4, the **−2 anchor offset table** in §1.1 (Dim−2 = 2,6,14,30,
62,126 → H+He, C, Si, Zn, Sm, magic-126). Dim−2 for CD level n is just
2ⁿ⁺¹−2; the element/magic-number matches are *selective* (nuclear magic
numbers are 2,8,20,28,50,82,126 — they do **not** match 6,14,30,62). This is
pattern-match narrative and should stay demoted; it does no work and is a
credibility liability if it leaks into the crypto or physics arguments.

**Falsifiable next test.** Implement Moreno's explicit ZD parametrisation,
write `is_zero_divisor(x)` that runs in O(poly(dim)) with no search, and time
it against random elements. If it is polytime (expected), formally close
OP §2.24.4 **negative**, strike all ZD-hardness language from every document,
and redirect to closing OP §2.24.5 (`Aut(MultTable) = PSL(2,7)` exactly) —
a clean, decidable, finite (≈5·10⁷ candidate) result that stands on its own as
mathematics regardless of crypto or physics.

---

## Perspective 3 — The Particle Phenomenologist / Model-Builder

**Stance.** I have seen a hundred mass formulas. The question is always the
same: how many free knobs, and how many genuinely *blind* predictions?

**What holds up.**
- The bookkeeping honesty is unusually good for this genre: the electron is
  labelled *calibration, not prediction*; the top quark is shown as a
  multiplicative factor ×2.60, refusing the dishonest "+160000%"; PDG bands
  are hard-coded for pass/fail; the headline metric is the disciplined
  "TOP-FREE RATIOS WITHIN 8%."
- The **lepton sector is the real result.** μ and τ as (2,1)- and (3,1)-cable
  knots with L = 2L_q, 3L_q and a *shared* Zf = 1/(2π) is genuinely
  parameter-light: one generation index drives the ropelength, the topology
  factor is fixed across the family. That is a structural prediction, not a
  fit. **Press here.**

**The load-bearing crack — degrees of freedom.** The operator takes three
*assigned* inputs per particle (A, Zf, L) on top of the global m₀. The
framework claims these come from topology (A = crossing/Alexander, Zf =
topological partition, L = ropelength), but the actual Zf column reads:
1, 3, 9, 12, **1/48**, **1/144**, **0.75**, 1/(2π), 6. The fractional and
composite values (1/48 "bilateral octahedral inversion", 1/144 = 12²,
3/4 "C₃/C₄ phase lock") have the texture of *post-hoc topology assignments
chosen to land the mass*. With three adjustable structural integers per
particle and an 8% band, a formula of this shape can absorb almost any
spectrum. The two genuinely impressive single numbers are also the two most
tuned:
- **Proton radius to 0.0019%** — but ρ = R_hyp·(49/4)·(1 + ζ(1−cos18°)) has
  49/4 and the void correction *selected to hit μH*; that is a fit, not a
  prediction, until 49/4 is derived independently.
- **Top quark ×2.60 ≈ φ².** Rescuing a factor-2.6 miss by positing a new
  "load tax" that happens to sit next to φ² is the textbook unfalsifiable
  move. It only becomes physics if the same load tax is derived from geometry
  *and predicts a second, independent quantity*.

**Falsifiable next test.** **Freeze the framework and make one blind
prediction.** Pick a quantity *not used in construction* — neutron–proton mass
splitting, a meson mass (π, K), or a hadron outside the current table — assign
A, Zf, L from topology **before** looking at the PDG value, and record the
prediction in an append-only entry. One clean blind hit inside the PDG band is
worth more than the entire current post-fit table. If the assignment rules are
real, this is straightforward; if it is hard to do without peeking, that
*is* the finding.

---

## Perspective 4 — The Philosopher of Science / Epistemic Auditor

**Stance.** I don't check your arithmetic; I check whether your framework
*can be wrong*, and whether your discipline is doing what you think it is.

**What holds up — and it is rare.** The epistemic instrumentation here is
better than most peer-reviewed work: the T1–T4 tiers, Register 1/2/3, the
Prior Address Standard, the append-only ledger, the *pre-registered* prediction
in `three_perspectives.py`, and — the strongest single signal of integrity in
the whole corpus — the honest non-reproduction of the 27/40 seven-circles count
down to the verified 14/40, *without* tuning parameters to rescue the expected
number. That is exactly how this should be done.

**The load-bearing crack — local honesty, global unfalsifiability.** Every
*individual* claim is tiered and caveated. But the *framework as a whole* has
no declared kill shot. A theory that can route any miss into "Register 3
proximity," "structural anomaly (§4.10)," or "open sub-gap" is locally honest
and globally unfalsifiable — the discipline becomes a very sophisticated
mechanism for never being cornered. Concretely:
- The **Eddington maneuver flag** is self-aware (it names Eddington's
  fundamental-theory number-juggling). But *naming* a failure mode does not
  immunise against it. Apply the flag to your own keystone: Φ = 2π + K/(8π²)
  with K = −φ². The ledger admits **both** the K = −φ² derivation **and** the
  8π² normalisation are *open*. So Φ is, today, a two-parameter fit wearing a
  Gauss–Bonnet costume — the precise object the flag was written to catch.
- **Cross-project halo.** The crypto and physics subprojects share aesthetics
  (sedenion / Fano / PSL(2,7) / φ) but are *epistemically independent*. A win
  in one lends **zero** evidential weight to the other. The "one substrate
  underlies both" intuition is the most seductive and least supported claim in
  the corpus; guard it hardest.

**Falsifiable next test.** Before the next analysis cycle, write a
pre-registered, append-only paragraph titled **"What would retire SQT"** — one
for the crypto subproject, one for the physics subproject — naming 1–3 concrete
observations that would force abandonment (e.g. crypto: "lattice-estimator
returns L1 security only with structure-free A"; physics: "the frozen blind
prediction of Perspective 3 misses the PDG band by >8%"). A framework that
cannot complete that paragraph has identified its real problem.

---

## Perspective 5 — The Adversarial Red-Team (with a Steelman)

**Stance.** I assume the grand claims are wrong and try to break them cheaply;
then I tell you what survives the wreckage.

**The cheapest break — the numerology null.** The seven-circles result rests on
matching cross-ratios to a **23-entry curated constant library** at 0.05%
tolerance. The report claims ~10× null enrichment, which is the *right kind* of
control — but it is incomplete. The decisive test is a **placebo library**: run
the identical pipeline against 23 *unrelated* constants (e, √2, Catalan's
constant, ln 2, π/5-free transcendentals…) and against *shuffled* torus
parameters. If cos 18° (or anything) still tops a placebo library at comparable
enrichment, the signal is pipeline geometry, not φ-structure. Until that placebo
run exists, "cos 18° is the joint-highest framework constant" is consistent with
a library-selection artifact. The same null applies to the whole physics side:
with φ, π, and small integers freely combinable, hitting a target to 8% is the
expected outcome of chance, not evidence.

**The single most defensible artifact in the entire project — the honeypot.**
The §3 canary key-ladder converts a *theoretical* hardness question into an
*empirical measurement*: deploy structural (mod-455/PSL(2,7)) and random keys
at equal bit-size and watch the fire order. If mod-455 fires first, the
structure is an attack surface; if not, it is security-neutral — and **either
outcome is publishable**, regardless of whether SQT-SLWE is secure. This is the
one place the project turns metaphysics into data. Prioritise it.

**The steelman — what survives even if every grand claim fails.**
1. A clean, reproducible **T1 result** on sedenion zero-divisor structure over
   F_p (84 pairs, K₇,₇-minus-matching) — a publishable note in computational
   algebra on its own.
2. A **production-quality Baillie–PSW prime library** (27/27 self-tests, the
   found-and-fixed Lucas off-by-one) — useful infrastructure independent of any
   theory.
3. A **novel honeypot methodology** for empirically probing algebraic attack
   surface — arguably the most original contribution in the corpus.
4. An **epistemic framework** (tiers/registers/PAS/Eddington flag) that other
   researchers could adopt wholesale.

**Falsifiable next test (two pre-registered runs).** (a) The placebo-library
numerology control above, with the predicted outcome written down first.
(b) An external/blind lattice-estimator cryptanalysis of `singer_a_randomized`
(Perspective 1). And the strategic recommendation: **decouple the brand.** Ship
the crypto as "Sedenion Module-LWE: a structured-MLWE case study" and the
physics as "a topological mass-formula exploration," each judged on its own
merits. The unified "Superfluid Quantum Topology explains crypto *and* particle
masses" framing is where credibility is most exposed and least supported.

---

## Where the five perspectives converge

| Theme | Consensus across lenses |
|---|---|
| **Biggest single risk** | The structure that is your *thesis* (PSL(2,7)/sedenion/φ) is, on current evidence, security-neutral in crypto (P1) and possibly fit-absorbing in physics (P3) — load-bearing in *neither* direction it claims (P2, P4). |
| **Biggest single strength** | The epistemic discipline itself (P4) and the honeypot empirical methodology (P5); the lepton-sector generation pattern (P3) and the T1 ZD algebra (P2) are the strongest *content*. |
| **The decisive missing experiment** | Crypto: real `lattice-estimator` on `singer_a_randomized` (P1). Physics: one *frozen blind* prediction (P3). Both: a placebo-library / "what would falsify this" pre-registration (P4, P5). |
| **Strategic move** | Decouple the two subprojects; stop letting the shared aesthetic transfer credibility (P4, P5). |

## Suggested priority order (reviewer recommendation, not a ledger decision)
1. **Close OP §2.24.4** with Moreno (P2) — cheap, and it settles whether *any*
   algebraic hardness is even on the table.
2. **Run the real lattice-estimator** on the Brief-06 construction (P1) —
   determines whether the security table survives contact with a standard tool.
3. **One frozen blind physics prediction** (P3) — the single highest-information
   experiment for the mass formula.
4. **Placebo-library numerology control** (P5) — guards the seven-circles /
   constant-matching results against selection artifacts.
5. **Write the two "what would retire SQT" paragraphs** (P4) — pre-register the
   kill shots before the next cycle.

*This document records reviewer judgement only. It introduces no new T1/T2
results and modifies no prior ledger content (append-only discipline
preserved).*
