# §3.4 Bilateral-Fold → cos(π/10) Gate — ADVANCED (conditional R2): a Precisely-Located M.CW Instance (Topological Term Inert; the Fold Needs Two Metric Imports)

**Date:** 2026-06-06
**Register:** **R1** for the geometry (deficit Δ=36°) and the value identity
(cos18°=cos π/10); **R2 (conditional on an import)** for the gate's open step —
the bilateral split is forced *iff* the substrate fold-energy is strictly convex,
which the §3.4.4 GP kinetic term supplies. **Pre-registration:**
`reports/SQT_3.4_BILATERAL_FOLD_PREREGISTRATION.md` (criteria committed before
computing). **Tool:** `tools/bilateral_fold_check.py`.
**Eddington watch:** ACTIVE — the split θ was left **free** and the action chose
it; nothing reverse-engineered. **M.BRIDGE:** no observable asserted (the
(1−cos18°) void correction is downstream).

> **The gate is advanced, not closed — and attacked head-on it lands as a clean
> instance of M.CW** (combinatorics cannot fix the metric/sign). The topological
> deficit-angle (Regge) term is **split- and localization-indifferent** — it
> cannot force the fold (the genuinely informative R1 negative). Forcing the
> symmetric split requires a fold-energy **strictly convex in the split angle θ**,
> which is a **sign** (f″>0) — and a sign is exactly what M.CW says combinatorics
> can never supply. Worse, that convex energy **smears** the deficit (prefers
> N→∞ sub-folds), so the **single-seam localization is imposed *against* the
> metric** — a second, anti-GP import. So step (3) reduces to **two named
> metric-class imports** (convexity-in-θ; single-seam localization), not to a
> derivation "from lattice axioms alone." With (3) granted, cos18°=cos(π/10)
> follows (step 4). *(Updated 2026-06-06 after SQT-agent audit — see §3.)*

## §1 — The gate and what is genuinely at issue

The §2.45-NGA / §2.53 prior-address of cos(π/10) has four steps; the ledger marks
**only step (3)** open ("show the §3.4 substrate action forces bilateral
splitting; once shown, cos18°=cos(π/10) is fully prior-addressed"):

1. vacuum vertex: 3 hexagons × 120° = 360° → flat;
2. seam vertex: 3 pentagons × 108° = 324° → **deficit Δ = 36° = π/5**;
3. **the 36° splits bilaterally → 18° + 18°** — the open step;
4. cos(18°) = the surviving fraction across the seam.

The disciplined question is *what in the action forces (3)*. The split is a degree
of freedom (θ, Δ−θ), θ∈[0,Δ]; "bilateral" is the specific claim θ=Δ/2. I did **not**
assume it — I parametrized θ and asked each form of the §3.4 action which θ it
selects.

## §2 — Results (against the pre-registered criteria)

| # | Criterion | Result | |
|---|---|---|---|
| **B1** | deficit arithmetic | 360° (flat) → 324° → Δ=36°=π/5; Σ over 20 dodecahedral vertices = 720° = 4π | ✓ R1 |
| **B2** | θ=Δ/2 a symmetric critical point | reflection symmetry of the seam ⇒ E′(Δ/2)=0 for any symmetric f | ✓ (necessary) |
| **B3** | **convexity decides** | Regge f=θ: curvature 0 — **split-indifferent**; GP f=θ²: curvature +4 — **min at 18°**; concave f=√θ: curvature <0 — max | ✓ |
| **B4** | GP supplies it, Regge doesn't | the §3.4.4 gradient term is the convex one that forces the fold; the deficit-angle term is linear | ✓ |
| **B5** | the value | cos18° = cos(π/10) = √(10+2√5)/4 = √(2+φ)/2 = 0.951056516295; (1−cos18°)=0.048943 | ✓ R1 |
| **B6** | single-seam ansatz tested (E_N=N·f(Δ/N)) | convex/GP **smears** (E_N→0, N→∞) ⇒ single fold is its *worst* case; Regge **indifferent**; concave localizes | ✓ (anti-GP) |

**The substantive content (B3/B4).** With θ free, the fold-energy
E(θ)=f(θ)+f(Δ−θ) selects:

- **deficit-angle / Regge** (the topological term, **linear** in deficit): E is
  *constant* in θ — **every split is degenerate**. The bare topological action
  **cannot** force the bilateral fold. *This is the genuinely informative result*:
  a tempting reading — "the deficit/Regge action forces the symmetric fold" — is
  **false**.
- **GP / Bjerknes kinetic** (§3.4.4 gradient energy, **convex**): E is strictly
  convex with its unique minimum at θ=Δ/2=18°. The convex term **forces** the
  bilateral split.

So the operative mechanism is identified: **convexity of the kinetic term**, not
the topological term, forces step (3).

## §3 — Honest scope (corrected after SQT-agent audit): a precisely-located M.CW instance

The SQT-agent reproduced the tool, ran an independent check, and made three
sharpenings — the middle one substantive and reversing part of my first framing. I
verified each with my own code and **concur**:

1. **"GP" was window-dressing — the import is convexity-in-θ, a *sign*.** The
   "convex ⇒ midpoint" step is Jensen-standard, and *any* strictly convex f gives
   18° (θ², θ⁴, cosh, eᵗ all verified). So the load-bearing property is the **sign
   f″>0**, not "the GP functional" specifically. (Whether the *physical* ∫|∇ψ|²
   actually yields a convex E(θ) once competing terms are present is itself
   unverified; f=θ² only illustrates the mechanism.) Pinning the condition to a
   sign is the correct, and more deflationary, statement.
2. **The single-seam localization is load-bearing AND anti-GP** (the part my first
   pass missed; verified — B6). A convex gradient energy **smears**: distributing Δ
   over N sub-folds gives E_N = N·f(Δ/N) → 0 as N→∞, so the lowest-energy state has
   **no discrete fold at all**. The single 18°+18° seam is the convex energy's
   **worst** case, not its preference — localization is imposed *against* the
   metric, and only *after* exactly two folds are imposed does convexity
   symmetrize them. (My own scan adds: the linear/Regge term is **indifferent** to
   localization too — E_N=Δ for all N. So *neither* the topological nor the
   convex-metric term wants a single localized symmetric fold.) This deserves its
   own open item.
3. **Read through M.CW, this confirms the wall — it does not advance through it.**
   The topological/combinatorial (Regge) action is provably split- and
   localization-indifferent ⇒ cos(π/10) is **not** reachable from lattice axioms
   alone; the angle enters only with metric-class imports (convexity + imposed
   localization), and convexity is a **sign** — exactly what M.CW says
   combinatorics can never fix. So my first draft's "remaining closure = derive a
   convex kinetic energy from the lattice axioms" was wrong in spirit: by the
   framework's own **M.CW corollary that is not an achievable combinatorial task**
   (it asks combinatorics to fix a sign). The honest open item is *"this needs the
   instantiated substrate metric/dynamics, full stop"* — the same standing import
   (the I1–I3 roton ticket) that blocks §2.52 pulsation=ζ. **Both dynamical gates
   bottom out at the same place.**

4. **Step (4)** (cos18° as the surviving fraction) is the ledger's R2 projection
   ansatz, not re-derived; this report verifies the *identity* cos18°=cos(π/10) and
   that it follows once 18° is in hand. **No observable** ((1−cos18°) void) is
   asserted — M.BRIDGE.

**Net register (corrected).** The gate moves from **open** to **reduced to two
named metric-class imports** — (i) convexity-in-θ (a walled sign) and (ii)
single-seam localization (anti-GP). **R2, conditional.** This is **not** R1
closure, and — crucially — **not a breach of the wall: it is the wall, precisely
located.** The genuine new content is the **R1 Regge split/localization-
indifference negative** (the "topological action forces it" reading is false) plus
the exact identification of the two imports. The remaining closure is **not** a
combinatorial task (impossible by M.CW) but the standing substrate-instantiation
import shared with pulsation=ζ.

## §4 — Proposed canonical update (additive)

| Task | Status |
|---|---|
| §2.45-NGA / §2.53 bilateral-fold gate (step 3) | **ADVANCED — conditional R2; a precisely-located M.CW instance.** **R1:** deficit geometry (Δ=36°), value identity (cos18°=cos π/10=√(2+φ)/2), and the **Regge split- & localization-indifference negative** (topological action cannot force the fold). **R2 conditional:** the bilateral split is forced *iff* the fold-energy is **convex-in-θ (a sign)** AND the deficit is **localized to a single seam (an ansatz the convex energy opposes)**. Jensen-standard once convexity is granted. |
| remaining closure | **Open — re-framed (NOT a combinatorial task).** By M.CW, convexity is a sign combinatorics cannot fix, so this needs the **instantiated substrate metric/dynamics** — the standing I1–I3 roton import — **not** a derivation "from lattice axioms alone." |
| single-seam localization | **Open item (new, load-bearing & anti-GP):** the convex energy *smears* (prefers N→∞); localization is imposed against the metric and must come from elsewhere (topological defect pinning / ansatz). |
| §2.52 Open 3 (pulsation = ζ) | **open — same bottom:** likely the same metric-instantiation import; ζ≈0.0931 is dimensionless so M.CW permits it, but the test is whether ζ falls out of the instantiated action or imports a scale. |

*Reproduce: `python3 tools/bilateral_fold_check.py`. Pre-registration:
`SQT_3.4_BILATERAL_FOLD_PREREGISTRATION.md`. Append-only; asserts no observable
(M.BRIDGE) and flags the convex-kinetic + seam imports (M.CW). Cross-refs:
§2.45-NGA (gate + 4-step argument), §2.53 (Rung-2 face inheritance), Paper II
§3.4/§3.4.4 (substrate action + GP representation), §3.06/§3.07 (chord-CR and
enrichment routes to cos(π/10), both closed-negative).*
