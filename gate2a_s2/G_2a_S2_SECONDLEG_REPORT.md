# G-2a-S2 — Independent Second-Leg Verification

**Date:** 2026-06-30 · **Pre-registration:** `G_2a_S2_PREREGISTRATION.md` (Route-2 symmetry
step; ceiling **R2 conditional**) · **First leg:** `g_2a_s2_symmetry.py` (chat-side) ·
**Second leg:** `gate2a_s2_secondleg.py` (this — from scratch, two independent methods).
Required CC second leg before any ledger entry.

## Result: **CONFIRMS the first leg — TETRAHEDRAL (|G_rot| = 12, no C₄).**

The canonical three-golden-ellipse Borromean representative has rotational symmetry
**T = A₄** (binary lift **2T = SL(2,3)**), whose genuine irreps are {2,2,2} — **no 4-dim
genuine irrep.** So the spin-3/2 quartet / μ_n factor-of-4 is **not** geometrically
supported by this representative. **This conditions G-2a-S1's fold** (below).

## Two independent methods (both from scratch; the first leg used one sampled search)
- **(M1) sampling-free signature argument.** Since φ ≠ 1/φ, each ellipse has only in-plane
  C₂, so *every* symmetry permutes the three coordinate axes (a signed permutation). A signed
  perm preserves the config iff its axis-permutation preserves the **cyclic** ordered set of
  (major,minor) pairs {(x,y),(y,z),(z,x)} — preserved by A₃ (even), reversed by transpositions.
  Result (exact, integer): full point group 24, **rotational subgroup 12**.
- **(M2) sampled point-set cross-check** (my own 360-point sampling, exact integer rotation
  matrices): rotational preservers = **12**. **M1 and M2 agree** on the group.

## What the second leg verified
| check | result |
|---|---|
| \|G_rot\| | **12** (1 identity + 3 C₂ + 8 C₃) = **T = A₄** |
| rotation orders | {1, 2, 3} — **no order-4** |
| C₃ about (1,1,1) preserves | **True** (T element) |
| C₂ about z preserves | **True** (T element) |
| **C₄ about z** preserves | **False** (octahedral-only — correctly absent) |
| **C₂ face-diagonal** preserves | **False** (octahedral-only — correctly absent) |
| binary lift / quartet | 2T = SL(2,3), genuine {2,2,2} ⇒ **no 4-dim genuine irrep** |
| **NC5** strand-permutation group | **Z₃** (C₃ axis-cycle; the 3 C₂ fix strands) — all even, sgn=+1 |

The explicit C₄ and face-diagonal tests confirm **T not O directly** — not merely "a search
returned 12." A C₄ about z maps the xy-ellipse (major-x) to a major-y ellipse, which is **not**
in the config because φ ≠ 1/φ; the eccentricity breaks the octahedral C₄.

## NC5 is benign for a color-singlet baryon (confirms first leg)
The rotational symmetries induce only **even** strand permutations (the C₃'s give 3-cycles =
Z₃; the C₂'s fix all three strands). An even permutation acts on the color singlet ε^{abc}
by sgn(σ) = +1, so **the color charge is preserved** — spatial rotation does **not** leak
into color. NC5 is benign here; the residual is standard spin-statistics, not spin↔color
mixing.

## Feedback to G-2a-S1 — the conditioning (the point of running Route 2 first)
G-2a-S1 forced the spin-3/2 quartet (D1=1) **given octahedral 2O symmetry**. This gate shows
the canonical *topological-linking representative* is only **tetrahedral**. Therefore, at
fold time, **G-2a-S1's "forced quartet" must fold CONDITIONAL on octahedral soliton
symmetry**, with the octahedral premise named as a **located M.ONT / core-geometry import** —
not as an unconditional structural fact.

**Crucially this is a location, not a refutation.** The topology (the Borromean linking) is
config-independent; the *symmetry* is config-dependent, and the physical baryon's symmetry
may be **richer** than this minimal three-ellipse representative — supplied by the K₇ /
Szilassi / relaxed-core geometry. A tetrahedral verdict on the representative therefore
*locates* the octahedral premise as an import the representative does not carry; it does not
by itself refute μ_n.

## Discipline
Pure geometry; the config is the fixed canonical golden-ellipse Borromean (a=φ, b=1/φ);
nothing tuned to octahedral or to the factor-of-4 (Eddington). M.CW ceiling **R2** — no
dynamics, no substrate metric. §2.52 Open 3 untouched.

## Standing (joint with G-2a-S1)
**Two-leg verified.** Neither S1 nor S2 is folded yet; both are now ready for a **joint
conditional R2 entry**: *the spin-3/2 quartet / factor-of-4 is forced GIVEN octahedral 2O
symmetry (S1, D1=1), but the canonical Borromean representative is only tetrahedral (S2),
so the octahedral premise is a located M.ONT/core-geometry import — not unconditional.*
NC5 benign for the color singlet. The dynamical locking and Assignment I/II (Routes 2/3)
remain open. Fold is the SQT/author's to run.
