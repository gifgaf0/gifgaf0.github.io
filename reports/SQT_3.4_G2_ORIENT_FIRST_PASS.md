# §3.4-G2-orient First Pass — The Fano-Line Hopf Linking Charge on the 3-D Soliton

**Date:** 2026-06-03
**Register:** **R1** (the Hopf-charge computation, reproducible) + **R2** (the
selection-rule / associative-plane reading) + **R3** (the knot-type / Császár
identification, not done). **Tool:** `tools/g2_orient.py`.
**Program:** the single concrete forward gate of §3.4-SYM
(`reports/SQT_LEDGER_ENTRY_3.4.md` §3.4.F).
**Eddington watch:** ACTIVE — line vs non-line control; a wrong-parity
extrapolation from 2-D was caught by the computation and is logged below.

> **Question (G2-orient).** G1″ showed (in 2-D, on a skyrmion) that the
> octonion/Fano orientation is a topological charge selecting Fano-line windings.
> On the genuine 3-D knotted-vortex soliton (a Faddeev–Hopf hopfion), is the
> Hopf **linking charge, weighted by the octonion structure constant φ**, nonzero
> (a quantized linking number) **iff** the winding components form a Fano line?

## §G2.1 — Construction

A charge-1 hopfion n : ℝ³ → S² (inverse stereographic ℝ³→S³ then the Hopf map;
the simplest linked-ring soliton) is embedded in a 3-component subspace {a,b,c}
of the seven octonion imaginaries. The framework-observable charge replaces the
S² area form's Levi-Civita ε with the octonion 3-form φ restricted to {a,b,c}:

    F_jk = Σ_pqr φ|_{abc}[p,q,r] n_p ∂_j n_q ∂_k n_r ,  B_i = ½ε_ijk F_jk ,
    A = ∇×⁻¹ B (Coulomb gauge, FFT) ,  Q_φ = (1/16π²) ∫ A·B d³x.

## §G2.2 — Result (R1; grid 64³, box [−4,4])

| Quantity | Value | Meaning |
|---|---:|---|
| ‖n‖ | 1.0000 | unit field ✓ |
| ordinary Q_H (Levi-Civita) | **+0.987** | genuine charge-1 hopfion (≈ integer) ✓ |
| Q_φ, **Fano line** (0,1,3) | **+0.987** | nonzero quantized linking ✓ |
| Q_φ, **Fano line** (1,2,4) | **+0.987** | every line carries it ✓ |
| Q_φ, **non-line** (0,1,2) | **0.0** (\|B\|max = 0) | exactly zero ✓ |
| Q_φ under φ→−φ | **+0.987** (unchanged) | orientation-EVEN (see §G2.3) |

**Selection rule CONFIRMED at the Q_H = 1 level:** the framework-observable Hopf
linking charge is a nonzero, near-integer quantized linking number on **every**
Fano-line winding, and **exactly zero** on a non-line winding — even though the
*same field* carries an ordinary Hopf charge ≈ 1. The octonion structure "sees"
the soliton only through Fano lines.

## §G2.3 — A correction the computation forced (logged, not hidden)

The 2-D G1″ density O = ∫ φ ψ ∂ₓψ ∂_yψ is **linear** in φ, hence
orientation-**odd** (φ→−φ flips it). I extrapolated "orientation-odd" to 3-D in
the §3.4.F gate statement. That is **wrong**: the 3-D linking charge
Q_φ = (1/16π²)∫A·B has **both** A and B linear in φ, so Q_φ is **quadratic** in φ
— **orientation-EVEN** (φ→−φ leaves it unchanged, verified). The sign of Q_φ is
the intrinsic **linking number**, not a φ-sign. What carries over from 2-D is the
**selection rule** (line ⇒ quantized linking, non-line ⇒ 0), not the parity. The
§3.4.F wording "Faddeev–Hopf linking charge … orientation-odd" should be
corrected to "…orientation-even (quadratic); the selection rule is the content."

## §G2.4 — Geometric reading (R2)

φ|_{abc} ≠ 0 **exactly on the 7 Fano lines = the coordinate associative 3-planes
of 𝕆** (the φ-calibrated planes of G₂ geometry). So the framework-observable
soliton linking charge is supported **precisely on the associative 3-planes** —
only there does the octonion product supply the oriented area element a Hopf
charge requires. This is the clean structural statement behind the selection
rule, and it ties G2-orient to standard G₂ calibrated geometry rather than to a
bespoke construction.

## §G2.5 — Scope / what this does and does not establish

- **Does (R1):** establish the **selection rule** — a nonzero quantized Hopf
  linking charge on a Fano-line winding, exactly zero off the lines — on a
  genuine 3-D Faddeev–Hopf soliton, with the clean associative-3-plane reading.
- **Does NOT:** use the *specific* Császár-torus / knotted (trefoil, higher-Q_H)
  soliton — this is the simplest Q_H=1 (linked-rings) hopfion, the *generic*
  knotted-vortex soliton; identify the framework's particle with a specific knot;
  assert any observable bridge (mass/scale). The discrete Q_φ is near-integer
  (~1–2% grid error), not exactly 1.

## §G2.6 — Forward pointer (G2-knot)

> **G2-knot.** Replace the Q_H=1 hopfion with a **knotted** Faddeev–Hopf soliton
> (the framework's actual particle — Császár-torus topology / a specific knot at
> higher Q_H) and recompute the φ-weighted linking charge, then map it to the
> §2.15 Borromean three-strand structure. The selection rule (associative-plane
> support) should persist; the question is which knot/linking the physical
> minimiser selects and whether it matches the framework's particle assignment.

## §G2.7 — Proposed Part VI open-task update

| Task | Status |
|---|---|
| §3.4-G2-orient (Fano-line linking charge on the 3-D soliton) | **First pass CLOSED (R1+R2):** selection rule confirmed (Q_φ ≈ 1 on every Fano line, 0 off-line) on the Q_H=1 hopfion; supported on the associative 3-planes. Parity corrected: orientation-**even**, not odd. |
| §3.4-G2-knot (knotted soliton; Császár / §2.15 Borromean mapping) | **Open — the next physical gate.** |

*Reproduce: `python3 tools/g2_orient.py`. Append-only; no prior ledger content
modified. Cross-refs: §3.4-G1″ (2-D origin + the corrected parity), §3.4.F (gate
statement — wording correction noted), §2.15 (Borromean), §2.74 (YB), M.CW.*
