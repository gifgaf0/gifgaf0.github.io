# SQT Master Ledger v4.24 — Five Perspectives (Format-Calibrated)

**Date:** 2026-06-03
**Reviewed:** `SQT_Master_Ledger_v4_24_CANONICAL.md` (558 KB): Preamble
(PAS, Eddington/M.SE, Vocabulary Substitution, Register System, **M.CW**,
**M.BRIDGE**), Part I (§§1.1–1.4), Part II (§§2.1–2.87.A), Part III
(retraction log), Part IV (conjectures), Part VI (consolidated open tasks).

> **Why these are different from the first five.** The v4.24 format already
> contains my earlier perspectives as *internal machinery*: §2.1's MANDATORY
> DISCLAIMER is the phenomenologist critique verbatim; the Eddington/M.SE
> guard is the philosopher-of-science critique; M.CW + the null tests are the
> numerology critique; the crypto-thread open tasks track the cryptographer
> critique. Re-running those would be telling you what you already tell
> yourself. These five instead audit **the auditing format** and the program
> it is steering — the layer the per-entry discipline structurally cannot see.

---

## Perspective 1 — The Meta-Auditor (referee *of the audit format*)

**Stance.** The format is world-class at suppressing **false positives**
(Eddington maneuvers, vocabulary substitution, premature promotion). I audit
what such a format is *structurally blind* to.

**Three blind spots the per-entry discipline cannot catch:**

1. **No program-level false-discovery rate.** The Prior Address Standard
   vets each constant's lineage *individually*, but the program runs hundreds
   of structural probes against a *small* library of "framework constants"
   (φ-class, 7-fold, the 20-element 5-fold inventory of §2.56). M.BRIDGE is an
   informal, prose version of the missing quantity. Formalize it: with N
   probes against M target constants at tolerance τ, the expected number of
   spurious <2% "hits" is ≈ N·M·(2τ). Until that number is computed and
   printed next to the hit counts (as `seven_circles_report.md` began to do
   with "~10× null enrichment"), "this constant keeps appearing" is an
   intuition the format has not actually earned program-wide.

2. **An incentive asymmetry that selects *against* physics.** The format only
   ever *punishes* a failed observable bridge (retraction log) and never
   *rewards* a risky one; internal combinatorial entries carry near-zero audit
   risk. So the optimization gradient points toward ever-finer internal
   structure (the §2.7x cluster) and away from falsifiable physics. This is
   *exactly* the accretion the version history shows. M.BRIDGE diagnoses the
   symptom ("surviving contributions are mathematical"); the cause is that the
   format's loss function has no term for "predictions risked."

3. **R3 is an absorbing state with no decay.** "Banked, not promoted" entries
   (C.COSM.1/2/3, ζ-tax, §2.63, §4.12–4.14) enter R3 and never leave. There
   are promotion gates but no *expiry*. A disciplined ledger should sunset R3
   entries that miss their promotion gate for K cycles, or the holding pen
   grows monotonically and dilutes the signal of the live work.

**Falsifiable test (audit the auditor's *recall*, not its precision).** Take
three already-closed-negative results (§3.06 chord-CR, §3.A.8 meson bridge,
the §3.04 Regge formula). For each, ask: *would the format have flagged this
if the author had not personally gone looking?* If the catches all trace to
human vigilance rather than a triggered rule, the format's recall is
unmeasured — and recall, not precision, is what a self-audit most needs.

---

## Perspective 2 — The Pure Mathematician (J. Algebra referee level)

**Stance.** I ignore every physical interpretation and ask only: what here is
**new, correct, and citable** as mathematics?

**The real asset register (math only):**

- **§1.1 (submitted, JALGEBRA-D-26-00651).** S₄-uniqueness in PSL(2,7),
  isotypic rigidity λ₁ = 2/3, Cheeger h = 8/21 on 2·K₇. Clean. *One referee
  hazard:* the flagged-open coincidence **h₂ = δ = 10/21**. An unexplained
  numerical coincidence sitting inside an otherwise tight algebra paper invites
  a scope objection — either give it a one-line representation-theoretic
  reason or move it to a remark. Do not let a Register-3 curiosity ride in a
  Register-1 paper.

- **The genuinely under-exploited asset: the §2.68 + §2.75–§2.81 cluster.**
  "PSL(2,7) does *not* act on the 42-pair Yang–Baxter family; **F₂₁** does,
  with two regular orbits of size 21" (§2.75), separated by a **Singer-chirality
  invariant** (§2.79); **even-term parity of clean sedenion zero divisors**
  (n=2: 84, n=3: 0, n=4: 1764, n=5: 0; §2.81); **prime-class independence**
  (p = 101, 103, 65537). This is a *second paper* — de-physicsable exactly as
  §1.1 was. Working title: *"The F₂₁ symmetry of sedenion zero-divisor
  Yang–Baxter pairs and its Singer-chirality invariant."*

- **The mathematician's M.CW — a prior-art wall.** Sedenion ZD combinatorics
  (box-kites, assessors) are *classically studied*: Moreno (1998),
  de Marrais (box-kites), Cawagas. The ledger already flags this honestly
  (OP-2.78.3: "classically understood … new content unlikely to live there").
  Take it as binding: before claiming novelty, do a formal prior-art pass and
  state the result *against* de Marrais/Cawagas/Moreno. The defensibly-new
  object is almost certainly the **Singer-chirality separator** of the two
  F₂₁ orbits (§2.79) — aim the paper there, not at the box-kite census, which
  a referee will call known.

**Falsifiable test.** Write the second paper's introduction *first*, as a
one-paragraph novelty claim positioned against the three prior-art references.
If you cannot state what is new in one sentence that a box-kite expert would
concede, the cluster is re-coordinatization, not discovery — and that verdict
is itself worth having.

---

## Perspective 3 — The Lattice Cryptographer (v4.24-grounded)

**Stance.** The v4.24 crypto thread is markedly more careful than the v2
ledger. I price what's actually decided versus what's outstanding.

**What v4.24 genuinely resolves (credit where due):**
- §2.66/§2.66.1: CBD-baseline DFR is a **null finding with ~10¹⁵ bits of
  headroom** against 2⁻¹²⁸. DFR is no longer a concern. (My earlier "48% DFR"
  alarm is explained: §2.69.4 Part III identifies it as the **§3.1
  ephemeral-distribution bug** — uniform `r` instead of sparse-ternary. Real
  bug, correctly diagnosed.)
- §2.69.4: ZD-noise SLWE rebuilt as inspectable code; **adjoint upgraded to a
  structural proof**; DFR = 0 at toy scale. Solid.

**The load-bearing crack — a Tier-2 empirical claim with unreproducible
provenance.** The Fano-line-leakage robustness claim (OP-2.58.2) rests on
"7 attacks at toy q = 911" from **§2.66.2** — and §2.69.1 records that
**§2.66.2's source script is not in the repo** ("attribution gap,"
unattributable-source disposition). So the program's central *security-relevant*
empirical result currently cannot be reproduced. The format has correctly
flagged this rather than hidden it, but the flag has not been discharged: a
leakage-robustness claim with no recoverable code should arguably be **demoted
from Tier 2** until §2.66.2 is recovered or re-derived (§2.66.3).

And the gates that actually *decide security* are all still open and all
standard-tool-shaped: **OP-2.58.2d** (LLL/BKZ via fpylll), **OP-2.58.2e**
(Leftover Hash Lemma for `A·s mod q` uniformity), **OP-2.58.2c**
(production-scale k=32, q=2³²), **OP-F** (LWE-estimator). This is M.BRIDGE in
the crypto sector: the surviving content is the ZD/F₂₁ *structure* (math); the
*security* is a bridge that has not yet crossed standard reduction tools.

**Falsifiable test (ordered).** (1) Recover or re-derive §2.66.2 so the
leakage audit has reproducible code; if it cannot be reproduced, demote the
claim. (2) *Then* run OP-2.58.2d (fpylll BKZ) and OP-F (lattice-estimator).
Until step 1, step 2's inputs are not trustworthy.

---

## Perspective 4 — The Physicist Who Takes M.BRIDGE Literally

**Stance.** M.BRIDGE + M.CW are not hedges; they are a *diagnosis with a
prescription the program has not yet acted on*. I follow it to its conclusion.

**The single upstream dependency.** M.CW says combinatorics cannot emit a
scale, a metric, or a sign; M.BRIDGE says every bridge that needed one has
failed. Trace the *open* physics gates and they all bottom out in the same
missing object: §2.7 ε-per-edge ("needs K₇ dihedral geometry"), §2.50 (2π
"from K₇ geometry without electron-mass circularity"), §2.45-NGA ("Bjerknes
gate, §3.4"), §2.85/§2.87 μ_n, the ζ-tax gates — **every one is waiting on the
§3.4 substrate action** (the Bjerknes/GP-type Lagrangian). The physics program
is not many open problems; it is **one** open problem (write the action) wearing
many combinatorial costumes. Opening more §2.x combinatorial gates cannot move
it, because none of them can supply what M.CW says combinatorics cannot.

**The one bridge attempt playing by the rules — watch it.** The μ_n thread
(§2.85 → §2.87 → §2.87.A) is trying to derive a **sign/parity** (the
Finkelstein–Rubinstein sign = APS η-parity) from **genuine algebra**
(Cℓ(6) = Spin(6) = SU(4)), not from incidence data. That is *precisely* the
move M.CW permits — a sign from algebraic structure rather than a bare graph.
**Gate 2a** (does baryon spin geometry = ρ₆/Cℓ(6), with the soliton locking
spatial 2O to spin/isospin 2O) is the most legitimate live bridge in the whole
document, because it is the only one not trying to get a forbidden quantity
from a forbidden source.

**Falsifiable test (a go/no-go the format has already half-specified).** Set a
bounded effort window on **§3.4**: can the substrate action be written down and
shown to (a) select the p6m ground state, (b) admit the Császár torus as a
soliton, (c) emit *one* dimensionful scale? If yes, bridges become possible and
the physics is alive. If no within the window, M.BRIDGE hardens from an R2
empirical generalization into a structural verdict, and the honest move is to
retire the physics interpretation to Tier 3, keep the math, and stop opening
combinatorial gates that M.CW guarantees cannot close the bridge. The bounded
sub-target the ledger already names — **soliton spin–isospin locking on the
K₇-tube (§2.87.A)** — is the right first probe.

---

## Perspective 5 — The Research Strategist (portfolio & closure dynamics)

**Stance.** I don't audit claims; I audit where finite effort is going and
whether the program is *converging or accreting*.

**The closure-dynamics finding.** V4.3 → V4.24 in ~6 weeks is ~20 patch
cycles, and the open-task list is **growing faster than it shrinks**: each
closure in the §2.7x cluster spawns successors (OP-2.74.1c → .i/.ii/.iii;
OP-2.78.1/2/3; OP-2.79.1/2; the §2.87 chain → §2.87.A → new gates). This is a
research-debt spiral, and it is *caused by the format's strength*: a system
that rewards rigorous sub-problem closure will manufacture sub-problems. The
audit format is a genuine asset with a genuine carrying cost, and the cost is
currently compounding.

**The asset register (what actually exists, stripped of the unified brand):**
| Asset | State | Bottleneck |
|---|---|---|
| §1.1 PSL(2,7) spectral geometry | **Submitted** | Referee turnaround; the 10/21 remark |
| §2.68/§2.75–§2.81 F₂₁/ZD cluster | **Citable, unwritten** | Prior-art pass vs de Marrais/Moreno |
| SQT-SLWE crypto | **Blocked on standard tools** | §2.66.2 reproducibility, then BKZ/estimator |
| SQT physics | **Blocked on one action** | §3.4 substrate Lagrangian |

**Recommendation — a framework freeze.** Declare a moratorium on new §2.x
*combinatorial* entries and spend the next cycle converting assets to external
outputs: (1) shepherd §1.1 through review; (2) write the F₂₁/ZD paper; (3) clear
the crypto reproducibility gap and run the two standard lattice tools (≈ a
weekend each); (4) one bounded §3.4 go/no-go (Perspective 4). This follows
M.BRIDGE's own *constructive consequence* ("the citable contributions to date
are the mathematical ones") and demotes the unification framing exactly as the
ledger's own meta-notes already imply it should be.

**Falsifiable test.** Maintain the asset register above as a living one-pager.
If, one cycle from now, the "citable" column has not produced a second external
output but the open-combinatorial-task count has risen, the freeze was
necessary and was not honored — and that, too, is a measurable verdict on the
program's direction.

---

## Convergence across the five

| | Reading |
|---|---|
| **The format's strength is also its trap** | It suppresses false positives superbly (P1), but its incentive gradient selects for low-risk internal combinatorics over falsifiable physics (P1, P4) and manufactures sub-problems faster than it closes them (P5). |
| **The surviving value is mathematical and already named by the format** | §1.1 + the F₂₁/ZD cluster are the citable core (P2); M.BRIDGE says so itself (P4). |
| **Two threads are blocked on a *single* object each** | Crypto on §2.66.2-reproducibility-then-standard-tools (P3); physics on the §3.4 action (P4). Neither is a many-problem blockage. |
| **The decisive next moves are external, not internal** | Write the second paper, run the standard crypto tools, give §3.4 a bounded go/no-go, freeze new combinatorial entries (P2, P3, P4, P5). |

*Reviewer judgement only. No register changes proposed; no ledger content
modified. These notes audit the program and its format, not individual T1/T2
claims — which the format itself already audits better than an outside reviewer
could.*
