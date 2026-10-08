#!/usr/bin/env python3
"""foldin_v4_94_phase_c.py — FOLDS V4.94: the October 2026 audit follow-up, Phase C (the crypto negative result and the
annotation batch).

Authorized by the author's brief of October 6, 2026 (audit_followup/inputs/BRIEF_2026-10-06_audit_followup.txt):
"C2. Annotation batch, one fold. Verify each item first." / "Work out the blast radius every time. For each kill or
downgrade, list every entry that depends on it and annotate those entries in the same fold." / "One short fold per phase."
/ "§2.52 Open 3. Add the G-ζ1 result, and leave the freeze in place." / "Draft, don't publish or send." Base:
SQT_Master_Ledger_v4_93_CANONICAL.md (md5 0aa63a0b…, 1,822,335 B; produced by foldin_v4_93_phase_b.py).

Edits (all additive):
  E1 title; E2 As-of prepend; E3 the V4.94 fold-in record (before the V4.93 record);
  E5 §2.94 (after §2.93's last paragraph, before Cluster J);
  E6 in-line "[→ V4.94 (§2.94.C1|C2): …]" brackets at the end of each blast-radius line (inside the last cell for table
     rows) — one of them the single authorized append to the §2.52 Open 3 row;
  E7 three Part VI rows after the Phase B rows; E8 one changelog line.
(No E4: Phase C adds no Preamble rule.)
Anchors are read from the file and asserted unique; every fragment lands exactly once; the §2.52 Open 3 row must equal the
V4.93 row plus exactly the authorized bracket; the reverse splice must reconstruct V4.93 byte-identically.
"""
import hashlib

SRC = "/home/claude/fold/SQT_Master_Ledger_v4_93_CANONICAL.md"
OUT = "/home/claude/fold/SQT_Master_Ledger_v4_94_CANONICAL.md"
V493, V493_BYTES = "0aa63a0bec9becbfb911dba3454255f2", 1822335
LS_REMOTE = "2026-10-07 21:35:09 UTC"            # main = 3587eb3 (PR #37); estate branch claude/audit-followup-oct6 = 53923fa
HEAD_AT_FOLD = "53923fa"
ESTATE = "`audit_followup/` on branch `claude/audit-followup-oct6`"

s = open(SRC, encoding="utf-8").read()
assert hashlib.md5(s.encode("utf-8")).hexdigest() == V493, "base V4.93 md5 mismatch — halt"
assert len(s.encode("utf-8")) == V493_BYTES
L = s.split("\n")
assert len(L) == 4695 and L[-1] == "", "line structure changed — re-anchor"


def one_line(prefix):
    hits = [x for x in L if x.startswith(prefix)]
    assert len(hits) == 1, f"anchor not unique: {prefix!r} ({len(hits)})"
    assert s.count("\n" + hits[0] + "\n") == 1
    return hits[0]


O3 = one_line("| **§2.52 Open 3**")

# ---------------------------------------------------------------- E1 title
T_OLD = "# SQT Master Ledger — V4.93 Canonical\n"
T_NEW = "# SQT Master Ledger — V4.94 Canonical\n"
assert s.count(T_OLD) == 1 and L[0] + "\n" == T_OLD

# ---------------------------------------------------------------- E2 As-of
A_OLD = "**As of:** October 7, 2026 (V4.93 fold — "
assert s.count(A_OLD) == 1 and L[2].startswith(A_OLD)
A_NEW = ("**As of:** October 7, 2026 (V4.94 fold — **the October 2026 audit follow-up, Phase C (§2.94): C1 — the SLWE "
         "crypto negative result: the Singer-orbit public matrix has rank 76 at every module rank k ≥ 7 (two-leg; a fixed "
         "256 × 112 factor of rank 76); the spec parameters reach 2^51, not 2^128, even with a uniform matrix (lattice "
         "estimator); decryption never fails (worst-case noise 258 < q/4, DFR = 0, replacing 2^(−6.4×10¹⁵)); the §3.05 "
         "correction carried into §§2.59–2.61; an ePrint note drafted. C2 — ζ-tax gate 3 CLOSED — FAILED as framed "
         "(tired-light class; DES b = 1.003 ± 0.011); §2.50.A, OP-2.14 and G-QUANTA's electron-2π and K₇-vortex PASSes "
         "CONDITIONAL on a ψ₀-weighted vacuum (I6); μ_n's 'factor of 4 = spin-3/2 quartet' DOWNGRADED (the 4 is the "
         "spin-½ weight 4/3; μ(Δ⁰) = 0); the polycrystal window 5–20 lattice cells, and ξ = ℓ_P not licensed on the "
         "transverse line; the G-ζ1 result added to §2.52 Open 3, freeze kept; fourteen math corrections. Nothing "
         "published, deposited or sent.** V4.93 fold (October 7, 2026) — ")

# ---------------------------------------------------------------- E6 brackets (prefix, text, kind, part)
C1, C2 = "§2.94.C1", "§2.94.C2"
DOWN = "§2.85 Part B, downgraded"
BR = [
    # ================= C1 — the crypto negative result (C1_RESULT.md, "Ledger annotations"; plus the fold-time sweep)
    ("The §§2.58–2.66 entries develop ",
     f"[→ V4.94 ({C1}): the construction fails at its spec parameters. The Singer-orbit public matrix has rank 76 for "
     "every module rank k ≥ 7 (it factors through a fixed 256 × 112 matrix of rank 76; two-leg); with a uniform matrix "
     "the spec parameters reach 2^51, not 2^128; decryption never fails (worst-case noise 258 < q/4). An ePrint note is "
     "drafted, not submitted.]", "para", "C1"),
    ("**Status: Tier 4 (theoretical ",
     f"[→ V4.94 ({C1}): KeyGen step 3's public matrix has rank exactly 76 at every k ≥ 7 (at p = 911 it falls short of "
     "full from k = 5), so (A, b) is distinguishable from uniform by elimination, and (R2) the noise is the short vector "
     "of a 76-dimensional LWE instance, estimated at 2^38.6. Even with a uniform matrix the spec parameters give 2^51 by "
     "the lattice estimator. DFR = 0 at spec.]", "para", "C1"),
    ("- **OP-2.58.1.a — CBD-baseline ",
     f"[→ V4.94 ({C1}): the closure stands on a worst-case bound, not a tail: the noise never exceeds 129η = 258 < q/4, "
     "so DFR = 0 exactly; '~10¹⁵ bits of headroom' was a Gaussian tail evaluated beyond the support of N.]", "para", "C1"),
    ("- **OP-2.58.5 (new, opened by ",
     f"[→ V4.94 ({C1}): criterion (iii) FAILS at spec: the lattice estimator gives 2^51.0 (bdd; usvp β = 72), and an "
     "independent core-SVP estimate agrees (β = 72). Criterion (ii) holds deterministically for any q > 1032 at η = 2. "
     "Whether any (q, η) meets (i)–(iii) at k = 32 was not searched.]", "para", "C1"),
    ("(a) The **sum-to-14 ZD complement ",
     f"[→ V4.94 ({C1}): this is the 'complement to 14' reading that §3.05 superseded on May 16. On the actual kernels it "
     "holds for 6 of the 21 pairs ({1,2}, {1,4}, {1,6}, {2,4}, {2,5}, {3,4}); the kernel supports are the co-line partners "
     "of the third point a⊕b of each pair's line (§2.55).]", "para", "C1"),
    ("**Negative result (R1, by exhaustive ",
     f"[→ V4.94 ({C1}): this compared (b) with the superseded rule. With the seven points read as the nonzero vectors of "
     "F₂³, the co-line partners of a⊕b are exactly its Hamming(7,4) syndrome class, so on the actual kernels (a) and (b) "
     "are one partition; the two-stage decoder rests on the superseded rule.]", "para", "C1"),
    ("**Result I (R1, graph-theoretic)",
     f"[→ V4.94 ({C1}): computed on the sum-14 rule that §3.05 superseded; on the actual kernels the complement "
     "structure is the co-line (XOR) partition of §2.55, so the 7 families, 13 components and zero-overlap figures "
     "describe the superseded rule.]", "para", "C1"),
    ("**Result I (R1, BFS verdict).*",
     f"[→ V4.94 ({C1}): the family automaton is §2.60's sum-14 families, i.e. the superseded rule; the BFS verdict and "
     "the 1/7 Law hold for that model, not for the actual kernels.]", "para", "C1"),
    ("- **RD-03: OSP-Lattice / Module-SLWE.",
     f"[→ V4.94 ({C1}): §2.58.B's Module-SLWE fails at spec (rank 76 at every k ≥ 7; 2^51 even with a uniform matrix); "
     "RD-03 inherits both unless the construction changes.]", "para", "C1"),
    ("**Production scaling at spec (k ",
     f"[→ V4.94 ({C1}): these figures are a Gaussian tail evaluated beyond the support of N. The worst case is 129η "
     "(258 at η = 2; 66,048 at η = 512), below q/4 throughout the sweep, so DFR = 0 for every η.]", "para", "C1"),
    ("- **The actually-binding parameter ",
     f"[→ V4.94 ({C1}): q does bind — on security, not DFR. With a uniform matrix the spec's q ≈ 2³² gives 2^51 by the "
     "lattice estimator, so hardness fails at spec before the leakage question of the next line arises. Descriptive: at "
     "n = 512 the two smallest primes ≡ 1 (mod 455) give 2^122.2 (q = 911) and 2^114.4 (q = 2731).]", "para", "C1"),
    ("For h_s = h_r = 64, η = 2: Var(N)",
     f"[→ V4.94 ({C1}): replaced by a worst-case bound. N lies in [−258, 258] (for CBD noise it is exactly CBD(258)), "
     "below q/4 ≈ 1.07×10⁹, so DFR = 0. The figure −6.4×10¹⁵ is a Gaussian tail at z ≈ 9.4×10⁷, about 4×10⁶ times "
     "beyond the largest value N can take.]", "para", "C1"),
    ("**Closure declaration.** OP-2.",
     f"[→ V4.94 ({C1}): the closure stands on the worst-case bound: DFR = 0 at spec for CBD(2) and for the §2.58.B "
     "confined noise (both bounded by 258), and for every η ≤ 512 in the sweep; deterministic correctness needs only "
     "q > 4·129η (q > 1032 at η = 2). The deferred estimator run is done: OP-2.58.5's criterion (iii) fails.]",
     "para", "C1"),
    ("**What this DOES establish.** The ",
     f"[→ V4.94 ({C1}): the toy runs used k = 7 and k = 14, where the Singer-orbit matrix has rank 76 (of 112 and 224); "
     "(A, b) is distinguishable from uniform by a rank computation at every k ≥ 5, so the null leakage results do not "
     "establish robustness.]", "para", "C1"),
    ("- **OP-2.58.2c** — Production-scale ",
     f"[→ V4.94 ({C1}): moot at spec — rank 76 at k = 32, and 2^51 even with a uniform matrix.]", "para", "C1"),
    ("- **OP-2.58.2e** — Leftover Hash ",
     f"[→ V4.94 ({C1}): false for the Singer matrix: A·s lies in a 76-dimensional subspace of F_q^(16k), far from "
     "uniform.]", "para", "C1"),
    ("**Closure conditions.** OP-2.58.",
     f"[→ V4.94 ({C1}): for the Singer matrix OP-2.58.2e cannot return a positive result and OP-2.58.2c is moot at spec; "
     "security at spec fails on other grounds (rank 76; 2^51 with a uniform matrix). The leakage question itself is not "
     "decided here.]", "para", "C1"),
    ("**Security reading (scoped, R2)",
     f"[→ V4.94 ({C1}): not specific to k = 32. M factors through a fixed 256 × 112 matrix of rank 76, so the rank is 76 "
     "at every k ≥ 7 (two legs: k = 8, 16, 32, 64 at both primes); at p = 911 it already falls short from k = 5 (72 of "
     "80), so 'k ≤ 7 (no periodicity, no collapse)' holds only for k ≤ 4.]", "para", "C1"),
    ("| **Gate G-BKZ32** (Cluster M ",
     f"[→ V4.94 ({C1}): rank 76 at every k ≥ 7, not only at k = 32 (two-leg).]", "row", "C1"),
    ("| **OP-2.58.1.a** (CBD-baseline ",
     f"[→ V4.94 ({C1}): DFR = 0 at spec by a worst-case bound (noise at most 258 < q/4).]", "row", "C1"),
    ("| **OP-2.58.1.b** (ZD-vs-CBD DFR ",
     f"[→ V4.94 ({C1}): at spec both noise models have DFR = 0 (worst case 258 for each); a differential needs "
     "q ≤ 1032.]", "row", "C1"),
    ("| **OP-2.58.2** (Fano-line class ",
     f"[→ V4.94 ({C1}): 'empirically robust' no longer stands — the toy runs were on rank-76 matrices — and hardness "
     "fails at spec independently of this question (rank 76 at every k ≥ 7; 2^51 with a uniform matrix). The leakage "
     "question itself is not decided.]", "row", "C1"),
    ("| **OP-2.58.2c** (production-scale ",
     f"[→ V4.94 ({C1}): moot — rank 76 at every k ≥ 7, and 2^51 at spec with a uniform matrix.]", "row", "C1"),
    ("| **OP-2.58.2d** (LLL/BKZ reduction ",
     f"[→ V4.94 ({C1}): the rank collapse holds at every k ≥ 7, not only at k = 32.]", "row", "C1"),
    ("| **OP-2.58.2e** (Leftover Hash ",
     f"[→ V4.94 ({C1}): false for the Singer matrix (A·s fills a 76-dimensional subspace).]", "row", "C1"),
    ("| **OP-2.58.5** (joint q-η optimization ",
     f"[→ V4.94 ({C1}): estimator run at spec — criterion (iii) FAILS (2^51.0 < 2^128); no (q, η) search made.]",
     "row", "C1"),
    ("| **OP-2.59-A, B, C** (decoder ",
     f"[→ V4.94 ({C1}): §2.59's outer stage is the superseded sum-to-14 rule, which on the kernels coincides with the "
     "inner Hamming partition; OP-2.59-C's encoder is §2.58.B.]", "row", "C1"),
    ("| **RD-01 to RD-04** (research ",
     f"[→ V4.94 ({C1}): RD-03's host, §2.58.B, fails at spec (rank 76; 2^51 with a uniform matrix).]", "row", "C1"),
    ("| **§2.66.2 source recovery or ",
     f"[→ V4.94 ({C1}): moot for any security reading — the toy runs were on rank-76 matrices.]", "row", "C1"),
    ("| **Cluster M citation hygiene ",
     f"[→ V4.94 ({C1}): any citation of §2.66.2 as evidence of robustness should also cite the rank collapse.]",
     "row", "C1"),
    ("| **§3.1 ephemeral-distribution ",
     f"[→ V4.94 ({C1}): the worst-case bound behind DFR = 0 assumes this fix (sparse ternary r, weight 64).]",
     "row", "C1"),
    ("| **OP-2.58.1a harness port** ",
     f"[→ V4.94 ({C1}): DFR at k = 32 is settled by the worst-case bound (DFR = 0 for any q > 1032 at η = 2); the port "
     "is not needed for DFR.]", "row", "C1"),
    ("- OQ-01 (orbit-schedule problem ",
     f"[→ V4.94 ({C1}): closed on §2.60's sum-14 model, the rule §3.05 superseded.]", "para", "C1"),
    ("- **OP-2.58.1.a** (CBD-baseline ",
     f"[→ V4.94 ({C1}): DFR = 0 exactly by the worst-case bound (noise at most 258 < q/4); the headroom figure is "
     "retired.]", "para", "C1"),

    # ================= C2 / P1 — ζ-tax gate 3
    ("| **ζ-tax gate 3** (cosmological ",
     f"[→ V4.94 ({C2}): **CLOSED — FAILED as framed.** The banked picture's redshift is a per-vertex amplitude penalty, "
     "Φ_out = Φ_in(1 − ζ), that leaves emission and arrival intervals unchanged: the tired-light class of the welding "
     "lemma (G-FOLD1, R1), which predicts no light-curve stretch (b = 0). DES measures b = 1.003 ± 0.005 (stat) ± 0.010 "
     "(sys) (White et al., MNRAS 533, 3365 (2024), arXiv:2406.05050), about 90σ from 0; read as adding to metric "
     "expansion, the penalty's share of ln(1+z) is 1 − b = −0.003 ± 0.011, consistent with zero. A frame/metric recast "
     "would dilate time by construction but abandons the amplitude mechanism.]", "row", "C2"),
    ("| `unaudited_conjecture_zeta_tax_unified_picture.",
     f"[→ V4.94 ({C2}): gate 3 CLOSED — FAILED as framed: the cosmological-redshift element is tired-light class and is "
     "excluded by supernova time dilation (DES b = 1.003 ± 0.011). Gates 1, 2 and 4 are unaffected; do-not-promote "
     "stands.]", "row", "C2"),
    ("| **G-FOLD1 gate + `SQT_Fold_Geometry_Redshift_April2026.",
     f"[→ V4.94 ({C2}): adjudicated — ζ-tax gate 3 CLOSED — FAILED as framed (the per-vertex reading predicts b = 0; "
     "DES: b = 1.003 ± 0.011).]", "row", "C2"),

    # ================= C2 / P2 — polycrystal floor and the ξ = ℓ_P license
    ("**N. Gate G-CI1 REGISTERED + LOCKED ",
     f"[→ V4.94 ({C2}): **validity floor.** The window describes grains much larger than a lattice cell, d ≫ a_phys. "
     "Under the declared chain (ξ = ℓ_P, C = ξ/a ∈ [0.0213, 0.0851] ⇒ a_phys ∈ [1.899, 7.588]×10⁻³⁴ m) the edge "
     "3.764×10⁻³³ m is 4.96–19.82 cells. A floor of N cells leaves (N·a_phys, 3.764×10⁻³³ m]: at N = 10 only "
     "a_phys ≤ 3.76×10⁻³⁴ m keeps a window, and at N = 20 none does. N is the author's election (Part VI); the chain "
     "itself is conditional (§2.91.H, V4.94).]", "para", "C2"),
    ("| **Gate G-CI1** (the Q3(1) carrier-identity ",
     f"[→ V4.94 ({C2}): the W^EM_∪ edge is 5–20 lattice cells under the declared a_phys chain; a grain ≫ lattice floor "
     "of 20 cells empties the window (§2.91.N).]", "row", "C2"),
    ("**H. Gate G-SCALE1 EXECUTED (declaration-type;",
     f"[→ V4.94 ({C2}): scope of ξ = ℓ_P. The declaration is a scale placement made for the longitudinal KC3 "
     "comparison, the test that retired the longitudinal bridge. It does not license ξ = ℓ_P on the transverse line: "
     "ANNEX-CDEF-1 (V4.71) records the transverse scale import as 'named and unexercised (… ξ = ℓ_P not licensed …)'. "
     "Its later transverse use, G-S2C1-W's election E-W-1(a) (V4.81), is a gate election, and that gate's reading is "
     "R2 conditional on it.]", "para", "C2"),
    ("**DECLARED (reading (a); author ",
     f"[→ V4.94 ({C2}): 'ξ = ℓ_P not licensed' stands. G-S2C1-W (V4.81) used the ξ = ℓ_P chain on the transverse line "
     "through its own election E-W-1(a), and its reading is conditional on that election; the transverse scale import "
     "remains unexercised.]", "para", "C2"),
    ("| **Gate G-S2C1-W** (the W_∪′ ",
     f"[→ V4.94 ({C2}): E-W-1(a)'s ξ = ℓ_P is an election inside this gate, not a license (ANNEX-CDEF-1: 'ξ = ℓ_P not "
     "licensed' on the transverse line); the a_phys band and the lattice floor are conditional on it.]", "row", "C2"),

    # ================= C2 / P3 — §2.50.A, OP-2.14, G-QUANTA conditional
    ("**Statement (R2, structural definition ",
     f"[→ V4.94 ({C2}): **CONDITIONAL.** The trap needs a vacuum on which a 2π phase winding cannot unwind. G-VS1 "
     "(§2.91.U) finds π₁ = 0 at the vacuum of record (the O(16) sphere), so no winding is protected there; on the polar "
     "strata the elementary winding is π, and that protection is accidental (§2.92.B); 2π windings are protected only "
     "where ψ₀ carries weight. Selecting such a vacuum is the import I6, registered and not made. The 2π trap, and with it "
     "the mechanism behind r_eff(electron) ≡ 1, holds only on a ψ₀-weighted vacuum.]", "para", "C2"),
    ("**Result (R2 → R1 candidate).*",
     f"[→ V4.94 ({C2}): 'minimum stable' rests on §2.50.A's trap, which is CONDITIONAL on a ψ₀-weighted vacuum (import "
     "I6) after G-VS1.]", "para", "C2"),
    ("**Result (R2, structural algebraic ",
     f"[→ V4.94 ({C2}): CONDITIONAL — the electron's L = 2π is §2.50/§2.50.A's protected 2π closure, which holds only "
     "on a ψ₀-weighted vacuum (import I6; G-VS1 finds π₁ = 0 at the vacuum of record). m₀ is fitted, so no number "
     "changes; the claim that the exponent is forced becomes conditional.]", "para", "C2"),
    ("- **OP-2.14** (m₀ exponent: 2π/Φ ",
     f"[→ V4.94 ({C2}): CLOSED-CONDITIONAL — the closure consumes §2.50.A's 2π trap, which holds only on a ψ₀-weighted "
     "vacuum (import I6, not forced; G-VS1).]", "para", "C2"),
    ("**P. Gate G-QUANTA REGISTERED ",
     f"[→ V4.94 ({C2}): the electron-2π and K₇-vortex PASS verdicts are CONDITIONAL: C1's conserved winding exists only "
     "on a vacuum with π₁ ≠ 0, and robustly only where ψ₀ carries weight (G-VS1 with §2.92.B); selecting that vacuum is "
     "import I6, not forced. The verdicts stand on the encoded table, not on the vacuum of record.]", "para", "C2"),
    ("| **Gate G-QUANTA** (§2.91.P — ",
     f"[→ V4.94 ({C2}): the electron-2π and K₇-vortex PASSes are CONDITIONAL on a ψ₀-weighted vacuum (import I6).]",
     "row", "C2"),
    ("| **Staging memo — stability and ",
     f"[→ V4.94 ({C2}): the K₇-vortex and electron-2π PASSes are CONDITIONAL on import I6 (§2.91.P).]", "row", "C2"),
    ("**U. Gate G-VS1 REGISTERED + LOCKED ",
     f"[→ V4.94 ({C2}): §2.50.A re-read — CONDITIONAL on I6; OP-2.14's closure and G-QUANTA's electron-2π and K₇-vortex "
     "PASSes made conditional.]", "para", "C2"),
    ("**Worked examples (corrected).",
     f"[→ V4.94 ({C2}): the count needs a vacuum manifold with π₁ = ℤ; the vacuum of record has π₁ = 0 (G-VS1), so "
     "'the vortex closes, winding 1' carries the vacuum-selection import I6.]", "para", "C2"),
    ("**Why the motivating frustration ",
     f"[→ V4.94 ({C2}): §2.50.A now carries a named import (I6, a ψ₀-weighted vacuum): R2, conditional.]", "para",
     "C2"),
    ("| `unaudited_conjecture_electron_cl2_filtration_floor.",
     f"[→ V4.94 ({C2}): §2.50.A's trap is CONDITIONAL on a ψ₀-weighted vacuum (I6); this restatement inherits the "
     "condition.]", "row", "C2"),
    ("- **Electron** at the tip (2π ",
     f"[→ V4.94 ({C2}): 'stable' is CONDITIONAL on import I6 (§2.50.A).]", "para", "C2"),

    # ================= C2 / P4 — μ_n: 'factor of 4 = spin-3/2 quartet' downgraded
    ("The constituent result μ_p = (4μ_u ",
     f"[→ V4.94 ({C2}): **DOWNGRADED — 'factor of 4 = the spin-3/2 quartet'.** In the SU(6) quark model the 4 in "
     "μ_p = (4μ_u − μ_d)/3 is a Clebsch–Gordan weight of the spin-½ proton: ⟨σ_z(u₁) + σ_z(u₂)⟩ = 4/3, "
     "⟨σ_z(d)⟩ = −1/3. The spin-3/2 states are the Δ quartet, with μ(Δ⁰) = μ_u + 2μ_d = 0 at μ_u = −2μ_d. So the −3/2 "
     "ratio is a spin-½ result, and a quartet programme targets the Δ, not μ_n (two-leg, exact). The S₃/S₄ "
     "representation theory of Parts B–D stands.]", "para", "C2"),
    ("Spin-3/2 is the **faithful** 4-dim ",
     f"[→ V4.94 ({C2}): the representation theory stands; 'the factor of 4' is not the spin-3/2 irrep (Part B, "
     "downgraded).]", "para", "C2"),
    ("The spinorial promotion −1 ↦ −Id ",
     f"[→ V4.94 ({C2}): the outcome map does not hold. A spin-3/2 udd state has the Δ⁰ moment μ_u + 2μ_d = 0 at "
     "μ_u = −2μ_d, not the −3/2 ratio, which needs the spin-½ nucleon state. Supplying −1 ↦ −Id does not by itself "
     "decide μ_n (Part B, downgraded).]", "para", "C2"),
    ("**The reduction [R1 core + R2].",
     f"[→ V4.94 ({C2}): 'the factor of 4' here is the dimension of spin-3/2, not μ_n's 4, which is the spin-½ weight "
     f"4/3 ({DOWN}); the FR/η reduction is unaffected as mathematics.]", "para", "C2"),
    ("So the fermionic geometry is *",
     f"[→ V4.94 ({C2}): μ_n's factor of 4 drops out of this convergence: it is the spin-½ weight 4/3, not a "
     f"4-dimensional representation ({DOWN}). The algebraic statements about σ₄, ρ₆ and Cℓ(6) are unaffected.]",
     "para", "C2"),
    ("**Net for μ_n.** Gate 2b is **",
     f"[→ V4.94 ({C2}): 'μ_n → −3/2 on that geometry' does not follow: a spin-3/2 udd state has μ = 0 (Δ⁰) at "
     f"μ_u = −2μ_d ({DOWN}).]", "para", "C2"),
    ("**The forced assignment question ",
     f"[→ V4.94 ({C2}): the baryon spin-3/2 of this paragraph and the last is the Δ quartet; the nucleon is spin-½, and "
     f"μ_n's 4 is its weight 4/3 ({DOWN}). The V4.84 assignment verdict is unaffected as algebra.]", "para", "C2"),
    ('**Refinement of the §2.87 "four-4 ',
     f"[→ V4.94 ({C2}): item (a) drops out — μ_n's 4 is the spin-½ weight 4/3, not a 4-dimensional space ({DOWN}).]",
     "para", "C2"),
    ("**Gate 2a, sharpened (R3 — the ",
     f"[→ V4.94 ({C2}): genuine spin-3/2 would give the Δ quartet, not 'the μ_n factor of 4' ({DOWN}); the locking "
     "question stands on its own.]", "para", "C2"),
    ("**Net (R2, conditional — the joint ",
     f"[→ V4.94 ({C2}): D1 = 1 is group theory and stands; its reading as 'the μ_n factor of 4' is downgraded — the "
     "forced quartet is Δ-type (§2.85 Part B).]", "para", "C2"),
    ("**Consequence — the octahedral ",
     f"[→ V4.94 ({C2}): both routes end at a spin-3/2 quartet, which is Δ-type, not μ_n's 4 — the spin-½ weight 4/3 "
     f"({DOWN}).]", "para", "C2"),
    ("**R. Gate G-2a-A1 REGISTERED + ",
     f"[→ V4.94 ({C2}): a spin-3/2 quartet built in the ℍ factor would be Δ-type; μ_n's 4 is the spin-½ weight 4/3 "
     f"({DOWN}). The verdict and T1–T4 are unaffected.]", "para", "C2"),
    ("| **G-2a-S1 / G-2a-S2** (Gate ",
     f"[→ V4.94 ({C2}): the 'μ_n factor-of-4' reading is downgraded — the forced quartet is Δ-type (§2.85 Part B).]",
     "row", "C2"),
    ("| **μ_n spinor-promotion gate*",
     f"[→ V4.94 ({C2}): **premise DOWNGRADED.** Making the 4-dim channel spin-3/2 gives Δ-type states: the udd quartet "
     "state has μ = μ_u + 2μ_d = 0 at μ_u = −2μ_d. The −3/2 ratio is the spin-½ SU(6) result, whose 4 is the weight "
     "4/3. The gate as posed does not decide μ_n (§2.85 Part B).]", "row", "C2"),
    ("| **σ₄\\|_{2O} ↔ spin-3/2** (does ",
     f"[→ V4.94 ({C2}): the restriction stands as representation theory; '= the factor of 4' is downgraded (§2.85 "
     "Part B).]", "row", "C2"),
    ("| **Gate 2a — is the baryon's ",
     f"[→ V4.94 ({C2}): the spin-3/2 identification does not stand between the framework and μ_n: a spin-3/2 udd state "
     f"is Δ⁰-like, μ = 0 ({DOWN}).]", "row", "C2"),
    ("| **Factor-assignment question*",
     f"[→ V4.94 ({C2}): 'μ_n's spin-3/2' is the Δ quartet; μ_n needs the spin-½ state ({DOWN}).]", "row", "C2"),
    ("| **Soliton spin-isospin locking ",
     f"[→ V4.94 ({C2}): the forced quartet is Δ-type; its link to μ_n is downgraded (§2.85 Part B).]", "row", "C2"),

    # ================= C2 / P5 — §2.52 Open 3: the single authorized append
    ("| **§2.52 Open 3** (pulsation ",
     f"[→ V4.94 ({C2}): the G-ζ1 result, added under the brief ('Add the G-ζ1 result, and leave the freeze in place'). "
     "G-ζ1 (§2.88.D.1, V4.36) computed the per-layer attenuation on the instantiated substrate (MV-G1, the I1–I3 ticket): "
     "DEGENERATE — the registered density channel is gapless and transparent (t → 1, 10.7× ζ); INFORMATIVE-FAIL on the "
     "most favourable reading — no probe enters the window [0.0881, 0.0981], and the closest, t = 0.36 ± 0.02, is 3.87× "
     "ζ. H′ retired (§3.A.9). The row stays Open and frozen.]", "row", "C2"),

    # ================= C2 / math
    # (a) OP-2.81.1/2 and §2.68.8.1
    ("- **OP-2.81.2 (R2).** Prove the ",
     f"[→ V4.94 ({C2}): CLOSED by Moreno's criterion (arXiv:q-alg/9710013): x = (a, b) is a zero divisor iff "
     "Re a = Re b = 0, |a| = |b| ≠ 0 and a ⊥ b. For a clean element |a|² and |b|² count its terms in each copy, so a "
     "clean zero divisor has no e₈ and equal counts, and n is even. Checked exactly on all 7,174,453 clean elements: 84, "
     "1,764, 11,200, 42,000, 40,320 and 4,480 zero divisors at n = 2–12, none at odd n or n = 14.]", "para", "C2"),
    ("| **OP-2.81.2** (prove the even-term ",
     f"[→ V4.94 ({C2}): CLOSED — Moreno's criterion forces equal term counts per copy and no e₈, so n is even; an exact "
     "census of all 7,174,453 clean elements agrees.]", "row", "C2"),
    ("- **OP-2.81.1 (R2).** Characterize ",
     f"[→ V4.94 ({C2}): partly answered. Moreno's criterion gives the count (1764 = 21 copy-A pairs × 84 completions) "
     "and rank 12, but not the kernel split: 84 kernels are spanned by four clean two-term zero divisors, 336 by two clean "
     "two-term and two clean four-term vectors, and 1,344 contain no clean two-term vector, a third class. The split and "
     "the box-kite link stay open.]", "para", "C2"),
    ("| **OP-2.81.1** (characterize ",
     f"[→ V4.94 ({C2}): partly answered — count and rank by Moreno's criterion; the kernel split 84 / 336 / 1,344 "
     "computed; the box-kite link open.]", "row", "C2"),
    ("*Why this excludes the identity ",
     f"[→ V4.94 ({C2}): the inference is invalid. e_a·e_{{a+8}} multiplies the two terms of one element and is never a "
     "term of x·y. Products e_i·e_{i⊕8} = ±e₈ do occur between terms of different zero divisors and cancel, e.g. "
     "(e₁+e₂+e₁₁+e₁₂)(e₃−e₄+e₁₃−e₁₄) = 0, and ⟨e₀, e₈⟩ is not the unique ZD-free plane (span(e₁, e₂) has none either). "
     "The exclusion of e_a ± e_{a+8} stands on §2.68.7 (full rank) and on Moreno's criterion ((e_a, ±e_a) is not "
     "orthogonal).]", "para", "C2"),
    ("| (ii) Derive K₇,₇ − M from capacity ",
     f"[→ V4.94 ({C2}): §2.68.8.1's argument is invalid; the algebraic fact stands on §2.68.7 and Moreno's criterion. No "
     "derivation from capacity exhaustion exists.]", "row", "C2"),
    ("| **OP-2.67.1b** (originally: ",
     f"[→ V4.94 ({C2}): sub-input (ii) should cite §2.68.7 and Moreno's criterion: §2.68.8.1's argument is invalid.]",
     "row", "C2"),
    ("*Forward pointer (v4.0 fold-in, May 19, 2026):* §2.68.1 ",
     f"[→ V4.94 ({C2}): two corrections. K₇,₇ − M has 651 size-2 matchings; the 42 unordered pairs are the matchings "
     "whose four labels form a Fano-line complement and whose all-plus diagonals annihilate (§2.68.1). And §2.68.8.1's "
     "mechanism is invalid — ⟨e₀, e₈⟩ is not the unique ZD-free plane — while the exclusion stands on §2.68.7 and "
     "Moreno's criterion.]", "para", "C2"),
    # (b) signed vs unsigned lifts (with the de Marrais pointer at §2.41.B)
    ("- The involutions and order-4 ",
     f"[→ V4.94 ({C2}): false with signs. Every one of the 168 collineations lifts to an octonion automorphism, with "
     "exactly 8 sign choices (a non-split 2³·PSL(2,7) of order 1344); only 21 lift unsigned (two-leg). 𝒴 is built from "
     "all-plus representatives: the sign-resolved YB family (504 signed pairs) is invariant under every signed lift, and "
     "signed lifts carry O_POS onto O_NEG. So 'PSL(2,7) does not act' and the O_POS/O_NEG split are artifacts of the "
     "all-plus convention.]", "para", "C2"),
    ("All 21 F₂₁ vertex-permutations ",
     f"[→ V4.94 ({C2}): with signs every element of PSL(2,7) lifts to an automorphism (8 sign choices each); F₂₁ is "
     "maximal only among unsigned lifts.]", "para", "C2"),
    ("Over 𝔽₉₁₁, classifying all 256 ",
     f"[→ V4.94 ({C2}): unsigned, each of the 147 collineations outside F₂₁ reverses exactly 4 of the 7 line "
     "orientations, so it is neither an automorphism nor an anti-automorphism — not an 'orientation-reverser' in the "
     "principal-anti-automorphism sense; with signs each lifts to an automorphism.]", "para", "C2"),
    ("**The 168 co-occurrence is a coincidence ",
     f"[→ V4.94 ({C2}): (1) 'only the 21 of F₂₁ preserve the annihilation graph' holds for unsigned lifts only: every "
     "collineation lifts with signs to an automorphism preserving it (all 2,688 signed lifts, two-leg), and the lifted "
     "group, a non-split 2³·PSL(2,7) of order 1344, is transitive on the 168 annihilating pairs with stabilizer of order "
     "8; its 2³ moves pairs, so no PSL(2,7) action results. The coincidence verdict is not re-tested. (2) Prior art: the "
     "7 components × 12 vertices are de Marrais's seven box-kites (each an octahedron), labelled by the strut constant — "
     "here the missing Fano index; de Marrais 2000 (arXiv:math/0011260), attributed at §2.78.]", "para", "C2"),
    ("| **G-2a.3 — the 168 = \\|PSL(2,",
     f"[→ V4.94 ({C2}): '21/168' holds for unsigned lifts only; with signs all 168 lift (a non-split 2³·PSL(2,7) of "
     "order 1344), transitive on the 168 pairs with stabilizer of order 8 — still no PSL(2,7) action. The 7 components "
     "are de Marrais's box-kites (§2.78).]", "row", "C2"),
    # (c) §2.77: inner/outer, the generated algebra, no order-24 element
    ("**(C) Lifted to SL(2,7):** Since ",
     f"[→ V4.94 ({C2}): s = diag(3,5) = −t, so conjugation by s sends u to u², not u³. No element of SL(2,7) conjugates "
     "u to u³: among its powers u is conjugate only to u, u², u⁴ (two-leg). χ extends to SL(2,7) only as an outer "
     "automorphism, e.g. conjugation by diag(3,1) ∈ GL(2,7), which carries σ₄ to σ₄′; the swap is visible on SL(2,7), "
     "not only on F₂₁.]", "para", "C2"),
    ("- **OP-2.75-CR (raised and CLOSED-with-result,",
     f"[→ V4.94 ({C2}): corrected at §2.77 Part I(C) — conjugation by s = diag(3,5) sends u to u², not u³; the QR↔QNR "
     "involution is induced only by an outer automorphism (e.g. conjugation by diag(3,1) ∈ GL(2,7)), which carries σ₄ "
     "to σ₄′.]", "para", "C2"),
    ("**Galois-twist relation (R2, now ",
     f"[→ V4.94 ({C2}): χ is not realized by s (s u s⁻¹ = u²); it is induced by an outer automorphism, conjugation by "
     "diag(3,1) ∈ GL(2,7), which carries σ₄ to σ₄′ on all of SL(2,7). The twist is visible on SL(2,7), not only at the "
     "F₂₁ restriction.]", "para", "C2"),
    ("| **OP-2.75-CR** (representation-theoretic ",
     f"[→ V4.94 ({C2}): the lift is outer, not inner — s = diag(3,5) = −t sends u to u²; χ is induced by conjugation by "
     "diag(3,1) ∈ GL(2,7) (§2.77).]", "row", "C2"),
    ("**Cℓ(0,3) collapse to Cℓ(0,2):",
     f"[→ V4.94 ({C2}): the last sentence is wrong as stated. Dimension 4 is the algebra of one anticommuting pair, i.e. "
     "of one Q₈ (there are 14). The 42 order-4 elements generate SL(2,7), so by Burnside their images generate all of "
     "M₄(ℂ), dimension 16 (two-leg); their linear span alone is the 15-dimensional space of traceless matrices. The "
     "census (168 pairs, 112 triples, 0 quadruples, ω = ±i·I₄) is confirmed.]", "para", "C2"),
    ("**Schur consistency:** The candidate ",
     f"[→ V4.94 ({C2}): SL(2,7) has no element of order 24; its element orders are 1, 2, 3, 4, 6, 7, 8 and 14. The "
     "conclusion is unaffected: ω = ±i·I₄ is scalar by direct computation for all 112 triples.]", "para", "C2"),
    ("**σ₄ does NOT natively harbor ",
     f"[→ V4.94 ({C2}): the order-4 images generate all of M₄(ℂ), the complexified Cℓ(1,3); what stands is narrower — "
     "no four order-4 images anticommute pairwise (0 quadruples), so no Dirac generating set lies among them, and each "
     "anticommuting pair generates one ℍ⊗ℂ.]", "para", "C2"),
    ("**V4.7 update (May 27, 2026):** The Dirac-bispinor ",
     f"[→ V4.94 ({C2}): see §2.E-WD's V4.7 closure as corrected: the order-4 images generate all of M₄(ℂ); only the "
     "absence of four pairwise-anticommuting images stands.]", "para", "C2"),
    # (d) the 42 size-2 matchings
    ("| ZD quadruples found | 42 (matches ",
     f"[→ V4.94 ({C2}): K₇,₇ − M has 651 size-2 matchings, not 42. The 42 quadruples are the matchings whose four "
     "labels form a Fano-line complement (84 such: the box-kite co-assessor pairs) and whose all-plus diagonals "
     "annihilate; the other 42 annihilate with a relative minus sign and are exactly 𝒴. '84 ordered / 2' conflates "
     "§2.31's 84 zero divisors with ordered pairs.]", "row", "C2"),
    ("**OP-2.67.1a — CLOSED (Tier 2)",
     f"[→ V4.94 ({C2}): the 42 quadruples are 42 of K₇,₇ − M's 651 size-2 matchings (§2.68.1); the Fano-complement and "
     "21 × 2 statements stand.]", "para", "C2"),
    ("**Resolved (Tier 2):** 42 Moreno ",
     f"[→ V4.94 ({C2}): the 42 quadruples are 42 of the 651 size-2 matchings — pairs of edges — not the 42 edges "
     "(§2.68.1).]", "para", "C2"),
    # (e) K₈ (with the (h) pointer), (f), (g)
    ("**Result (R2).** The complete ",
     f"[→ V4.94 ({C2}): K₈ has six non-isomorphic 1-factorizations, not two: 6,240 labelled ones in S₈-classes of sizes "
     "30, 420, 630, 960, 1,680 and 2,520 (automorphism groups of order 1344, 96, 64, 42, 24, 16). Every vertex "
     "relabelling is an automorphism of K₈, and the QR- and QNR-oriented cyclic constructions differ by x ↦ 3x and are "
     "isomorphic (order 1344). The order-8 stabilizer behind 168/8 = 21 is the flag stabilizer D₄, not V₄ (§2.62.C).]",
     "para", "C2"),
    ("| arctan(1/√2) | ≈ 54.74° | Császár ",
     f"[→ V4.94 ({C2}): arctan(1/√2) = 35.264° (0.61548 rad); 54.736° is its complement, arctan √2 = arccos(1/√3). The "
     "α⁻¹ term 84/arctan(1/√2) ≈ 136.48 uses 35.26°, which lies outside this section's 54°–60° band.]", "row", "C2"),
    ("**Result (R2).** The three phase ",
     f"[→ V4.94 ({C2}): log(4π)/log 7 = 1.30069 (ln 4π = 2.53102, ln 7 = 1.94591; the ratio is base-independent), not "
     "≈ 1.286.]", "para", "C2"),
    # (h) §2.62.B/C
    ("**Sign Duality.** The negated ",
     f"[→ V4.94 ({C2}): false. ker(L_x) = ker(L_{{−x}}) is true but beside the point: the negated orientation flips the "
     "relative sign (e_i − σe_{j+8}), not x ↦ −x, and gives 21 different 2D spaces (overlap 0). The two valid "
     "orientation triplets give 42 spaces, 21 flags × 2.]", "para", "C2"),
    ("**Orbit-stabilizer accounting:",
     f"[→ V4.94 ({C2}): the order-8 group is the flag stabilizer, which is D₄ (non-abelian, five involutions; "
     "two-leg); V₄ × {±1} is not a subgroup — PSL(2,7) has no C₂³. Under the unsigned lift V₄ fixes C(m, L), but the "
     "orbit is 168/4 = 42 spaces (the 21 canonical and the 21 of the negated orientation, §2.62.B), and the elements of "
     "D₄ outside V₄ swap C⁺(m, L) and C⁻(m, L).]", "para", "C2"),
    ("**Theorem 4.** The sedenion algebra ",
     f"[→ V4.94 ({C2}): the order-8 stabilizer in 168/8 = 21 is the flag stabilizer D₄, not V₄ × {{±1}} (§2.62.C).]",
     "para", "C2"),
    ('The label "PSL(2,p) ↔ Cl(p+1)" ',
     f"[→ V4.94 ({C2}): the flag stabilizer is D₄ (order 8; 168/8 = 21); V₄ is the pointwise line stabilizer, which "
     "fixes a code space whose orbit has 42 members (§2.62.C).]", "para", "C2"),
    # (i) §2.84A
    ("Fixing the imaginary unit e₇ leaves ",
     f"[→ V4.94 ({C2}): a labelling coincidence. In this entry's cyclic labels L_{{e₇}} pairs 1↔3, 2↔6, 4↔5 (a ↦ 3a on "
     "QR); in Cayley–Dickson labels it pairs a ↔ 7⊕a ≡ −a (mod 7). Only 12 of the 30 labelled Fano planes give a "
     "QR↔QNR swap, and J has 8 transversal 3+3 splits (4 with a Fano-line real triple), so su(3) and J do not single out "
     "QR/QNR.]", "para", "C2"),
    # (j) OP-2.74.1c.i / .iii
    ("- **OP-2.74.1c.i.** Characterize ",
     f"[→ V4.94 ({C2}): answered. With a ≤ 7 < b, TS_O1 = {{e_a·e_b = +e_{{a⊕b}}}} and TS_O2 = "
     "{e_a·e_b = −e_{a⊕b}} on all 42 twosets, and the sign is F₂₁-invariant: e₁e₁₄ = e₄e₁₁ = e₅e₁₀ = +e₁₅ and "
     "e₂e₁₃ = e₃e₁₂ = e₆e₉ = −e₁₅. The quadratic character χ does not separate them.]", "para", "C2"),
    ("- **OP-2.74.1c.iii.** Investigate ",
     f"[→ V4.94 ({C2}): a sign-convention artifact. T_A, T_B and T_C are pairwise co-assessors (box-kite 7). "
     "(T_A, T_C) has equal structure-constant signs and is YB with equal diagonal signs; (T_A, T_B) and (T_B, T_C) have "
     "opposite signs and are YB exactly when the diagonal signs are opposite. An automorphism maps (e₁+e₁₄, e₄+e₁₁) to "
     "the YB pair (e₁−e₁₄, e₂+e₁₃).]", "para", "C2"),
    ("| **OP-2.74.1c.i** (finer F₂₁-invariant ",
     f"[→ V4.94 ({C2}): ANSWERED — TS_O1/TS_O2 is the sign of e_a·e_b = ±e_(a⊕b) (a ≤ 7 < b).]", "row", "C2"),
    ("| **OP-2.74.1c.iii** ((T_A, T_C)",
     f"[→ V4.94 ({C2}): ANSWERED — a sign-convention artifact; all three pairs are YB with the matching relative "
     "sign.]", "row", "C2"),
    # (k) de Marrais (the §2.41.B pointer is combined with (b) above)
    ("- The 84 ZDs partition into **",
     f"[→ V4.94 ({C2}): prior art — these 7 orbits of 12 are de Marrais's seven box-kites, the 'missing element' m is "
     "the strut constant, and the kernels are spanned by co-assessor diagonals; de Marrais 2000 (arXiv:math/0011260), "
     "attributed at §2.78.]", "para", "C2"),
    ("The 42-edge combinatorial object ",
     f"[→ V4.94 ({C2}): prior art — the 42-edge object is de Marrais's 42 assessors (seven box-kites of six); "
     "de Marrais 2000 (arXiv:math/0011260), attributed at §2.78.]", "para", "C2"),
    # (l) α⁻¹
    ("α⁻¹ recovers the CODATA value ",
     f"[→ V4.94 ({C2}): 240/√3 = 138.5641 is 1.115% above CODATA 2022's 137.035999177 (1.103% of 240/√3), not 1.099%. "
     "§2.25.3–6 credits this same 0.003% retrodiction to a different leading value, 84/arctan(1/√2) = 136.4789, which "
     "lies 0.407% below. Neither place writes the formula, so the starting value of the match is not pinned.]",
     "para", "C2"),
    ("The α⁻¹ correction formula α⁻¹ ",
     f"[→ V4.94 ({C2}): 84/arctan(1/√2) = 136.4789 (radians) lies 0.407% below CODATA 2022's 137.035999177, so the "
     "subtracted correction terms must total −0.557, a net increase. §2.2 names a different leading value, "
     "240/√3 = 138.5641 (1.115% above), with proton-radius rather than APS-boundary corrections: one 0.003% match is "
     "credited to two starting values.]", "para", "C2"),
]
EDITS, PARTS = [], {"C1": 0, "C2": 0}
for prefix, text, kind, part in BR:
    old = one_line(prefix)
    assert "[→ V4.94" not in old and "\n" not in text
    assert text.startswith("[→ V4.94 (§2.94." + part + "): ") and text.endswith("]")
    if kind == "para":
        assert not old.endswith(" |")
        new = old + " " + text
    else:
        assert old.endswith(" |") and old.startswith("| ") and "|" not in text.replace("\\|", "")
        new = old[:-2] + " " + text + " |"
    EDITS.append((old, new))
    PARTS[part] += 1
assert len({o for o, _ in EDITS}) == len(EDITS), "two brackets on one line"
NBR = len(EDITS)
assert (NBR, PARTS["C1"], PARTS["C2"]) == (113, 34, 79), (NBR, PARTS)
O3_NEW = [n for o, n in EDITS if o == O3]
assert len(O3_NEW) == 1, "the §2.52 Open 3 append must be exactly one"

# ---------------------------------------------------------------- E5 §2.94
J_ANCH = "## J. Multi-Lens Reference and Phase Incommensurability\n"
assert s.count(J_ANCH) == 1 and s.count("\n\n" + J_ANCH) == 1
REG93 = one_line("**Registers and non-claims.** B1's three verdicts R1 (pre-registered, two-leg).")
assert s.count(REG93 + "\n\n" + J_ANCH) == 1
S294 = [
    "### §2.94 — The October 2026 Audit Follow-Up, Phase C: the Crypto Negative Result and the Annotation Batch (V4.94)",
    f"*(Folded V4.94, October 7, 2026, under the author's brief of October 6 — \"Phase C: the crypto note draft and one "
    f"annotation fold\"; estate {ESTATE}. C1 and C2 were each pre-registered before any computation. The C1 rank and "
    "every C2 check that decides a downgrade, a closure or a reversal (P1, P3, P4 and the math reversals) had a second "
    "leg; everything else is an annotation, one leg, under the brief's proportionality rule. The affected entries carry "
    "[→ V4.94 (§2.94.C1)] or [→ V4.94 (§2.94.C2)] pointers. No §3.x: as at V4.92–V4.93, retirements and downgrades are "
    "recorded here and bracketed in place. The ePrint note is a draft — \"Draft, don't publish or send.\")*",
    "**C1. The SLWE negative result.** Pre-registration `C1_PREREG.md` 778e3d4a (locked at ce82bdc). (1) **DR-C1-1, "
    "PASS — WIDENED (R1, two legs; leg 1 committed before the blind leg 2 began).** The Singer-orbit public matrix of "
    "§2.58.B has rank exactly 76 at k = 8, 16, 32 and 64, at p = 911 and at the spec prime 4,294,977,961, for three seed "
    "sets each; uniform controls have full rank 16k. The cause is structural: M = (S ⊗ I₁₆)·N_k, where N is a fixed "
    "256 × 112 integer matrix of rank 76 (over ℚ and at both primes) and N_k repeats its seven column blocks with period "
    "7, so rank(M) ≤ 76 for every k and every seed. At p = 911 the rank falls short of full from k = 5 (16, 32, 48, 64, "
    "72, 74, 76, 76, … for k = 1 … 10), so §2.69.5's k = 32 scoping is lifted. Reading (R2): b − e = M·s lies in a "
    "76-dimensional subspace, so the noise is the short vector of a 76-dimensional LWE instance (estimator 2^38.6, "
    "descriptive). (2) **DR-C1-2, OP-2.58.5 criterion (iii) FAILS.** With a uniform matrix the spec parameters (n = 512, "
    "q = 4,294,977,961, a sparse ternary secret of weight 64, CBD(2) noise, m = 512) give 2^51.0 (bdd; usvp 2^52.1 at "
    "β = 72) under the lattice estimator (`malb/lattice-estimator` 53da5982, default attacks); an independent core-SVP "
    "estimate gives the same β = 72, and m = 1024 changes nothing. The modulus is far too large for the noise. "
    "Descriptive: the two smallest primes ≡ 1 (mod 455) give 2^122.2 (q = 911) and 2^114.4 (q = 2731) at n = 512; no "
    "(q, η) search was made. (3) **DR-C1-3, DFR = 0.** With the entries of e, e₁ and e₂ bounded by η and weights "
    "h_r = h_s = 64, the decryption noise satisfies |N| ≤ 129η: 258 at η = 2, for CBD noise and for the §2.58.B confined "
    "kernel noise alike, against q/4 ≈ 1.07×10⁹; for CBD noise N is exactly CBD(258). The figure 2^(−6.4×10¹⁵) was a "
    "Gaussian tail evaluated about 4×10⁶ times beyond the largest value N can take, and it is replaced. (4) **The §3.05 "
    "correction reaches §§2.59–2.61.** On the actual kernels (all 84 two-term cross-copy zero divisors) the supports are "
    "the co-line partners of the third point a⊕b, for all 21 pairs, as §2.55 says, and the sum-to-14 rule holds for 6 of "
    "the 21. With the seven points read as the nonzero vectors of F₂³, the co-line partners of a⊕b are its Hamming(7,4) "
    "syndrome class, so §2.59's two structures coincide; §2.60's families and components and §2.61's automaton describe "
    "the superseded rule. (5) §2.66.2's toy runs used k = 7 and 14, where the matrix already has rank 76. Two crypto-"
    "project files, `tools/lattice_estimate_results.md` (\"> 512 bits\") and `tools/SLWE_Prime_Master_v2.md` §4.4, do "
    "not describe the spec and are flagged for the author. C1 says nothing about the confined-noise trapdoor question "
    "(OP-2.58.2), which stays open as a question. **Draft:** `phase_c/C1/eprint_draft/` (4 pp.), for IACR ePrint, not "
    "submitted.",
    "**C2. The annotation batch.** Pre-registration `C2_PREREG.md` e538b2e5 (locked at d6fee69); every item verified "
    "before folding (`phase_c/C2/C2_RESULT.md`). **P1 — ζ-tax gate 3 CLOSED: FAILED as framed.** The banked entry makes "
    "the redshift a per-vertex amplitude penalty, Φ_out = Φ_in(1 − ζ), which leaves emission and arrival intervals "
    "unchanged: the tired-light class of the welding lemma (G-FOLD1, R1), which predicts no light-curve stretch. DES "
    "measures b = 1.003 ± 0.005 (stat) ± 0.010 (sys) (White et al., MNRAS 533, 3365 (2024), arXiv:2406.05050), about 90σ "
    "from b = 0. If the penalty instead adds to metric expansion, its share of ln(1+z) is 1 − b = −0.003 ± 0.011, "
    "consistent with zero. A frame or metric recast would dilate time by construction, but it abandons the amplitude "
    "mechanism and would be a new entry. **P2 — the polycrystal floor and the ξ license (annotation).** Under the "
    "declared chain (ξ = ℓ_P, C = ξ/a ∈ [0.0213, 0.0851] ⇒ a_phys ∈ [1.899, 7.588]×10⁻³⁴ m) the edge of W^EM_∪, "
    "3.764×10⁻³³ m, is 4.96–19.82 lattice cells. A grain ≫ lattice floor of N cells leaves (N·a_phys, 3.764×10⁻³³ m], "
    "which is empty at N = 20; N is the author's election (Part VI). ξ = ℓ_P is not licensed on the transverse line. "
    "G-SCALE1 declared it as a scale placement for the longitudinal KC3 test, and ANNEX-CDEF-1 records the transverse "
    "scale import as unexercised, \"ξ = ℓ_P not licensed\". Its one transverse use is G-S2C1-W's election E-W-1(a), and "
    "that gate's reading is conditional on it. **P3 — §2.50.A, OP-2.14 and G-QUANTA CONDITIONAL.** G-VS1 finds π₁ = 0 "
    "at the vacuum of record (the O(16) sphere). The elementary winding is π on the polar strata, where §2.92.B found the "
    "protection accidental, and 2π only where ψ₀ carries weight. Protection is a selection by the import I6, registered "
    "and not made. So §2.50.A's 2π trap, OP-2.14's closure and G-QUANTA's electron-2π and K₇-vortex PASSes hold only on "
    "a ψ₀-weighted vacuum. m₀ is fitted, so no number moves; what becomes conditional is the claim that the 2π, and "
    "with it the exponent 2π/Φ, is forced. **P4 — μ_n: 'factor of 4 = the spin-3/2 quartet' DOWNGRADED (two legs, "
    "exact).** In the SU(6) quark model μ_p = (4μ_u − μ_d)/3, with ⟨σ_z(u₁) + σ_z(u₂)⟩ = 4/3 and ⟨σ_z(d)⟩ = −1/3: the 4 "
    "is a Clebsch–Gordan weight of the spin-½ nucleon. The spin-3/2 states are the Δ quartet, with "
    "μ(Δ⁰) = μ_u + 2μ_d = 0 at μ_u = −2μ_d. Making the four-dimensional channel spin-3/2 therefore yields Δ-type moments, "
    "not the −3/2 ratio. The representation theory of §§2.85–2.87, of Gate 2a and of §2.91.R stands as R1; only its "
    "reading as μ_n's factor of 4 is withdrawn (eighteen pointers). **P5 — §2.52 Open 3.** The G-ζ1 result is appended "
    "to the frozen row, and the freeze stays, as the brief directs. **Math (fourteen items; second legs on every "
    "reversal).** (a) OP-2.81.2 is closed by Moreno's criterion (arXiv:q-alg/9710013): x = (a, b) is a zero divisor iff "
    "Re a = Re b = 0, |a| = |b| ≠ 0 and a ⊥ b, so a clean zero divisor has equal term counts and n is even; all "
    "7,174,453 clean elements were checked. OP-2.81.1 is partly answered: Moreno gives the count and the rank, and the "
    "kernel split 84 / 336 / 1,344 was computed. §2.68.8.1's argument is invalid, but its conclusion stands on §2.68.7 "
    "and Moreno. (b) Every collineation lifts with signs, with 8 sign choices each, forming a non-split 2³·PSL(2,7) of "
    "order 1344; only 21 lift unsigned. So 'does not act' and the O_POS/O_NEG split are artifacts of the all-plus "
    "convention. (c) §2.77's χ is outer: no element of SL(2,7) conjugates u to u³, and s = diag(3,5) = −t. The order-4 "
    "images generate M₄(ℂ), while their span is the 15-dimensional traceless space; no element has order 24. (d) "
    "K₇,₇ − M has 651 size-2 matchings. (e) K₈ has six 1-factorizations. (f) arctan(1/√2) = 35.26°. (g) "
    "log(4π)/log 7 = 1.3007. (h) The §2.62.C flag stabilizer is D₄, and §2.62.B's sign duality is false. (i) §2.84A's "
    "QR↔QNR swap is a labelling coincidence (a ↦ 3a in its own labels). (j) OP-2.74.1c.i is answered (TS_O1 is the + "
    "class), and OP-2.74.1c.iii is a sign-convention artifact. (k) de Marrais's box-kites are now pointed to in §2.55, "
    "§2.68.4 and §2.41.B. (l) The α⁻¹ entries credit one 0.003% match to two starting values on opposite sides of "
    "137.036 (84/arctan(1/√2) = 136.479; 240/√3 = 138.564, +1.115%).",
    "**Registers and non-claims.** C1: the ranks R1 (two-leg); the estimator figures and the worst-case bound R1 "
    "arithmetic; the reduced-instance reading R2. C2: P1, P3, P4 and the math reversals pre-registered with second legs "
    "(for P1 and P3, a verbatim re-reading of the quoted sources); P2 and P5 annotations. No register is promoted; no "
    "observable bridge (M.BRIDGE intact); nothing is published, deposited or sent. The §2.52 Open 3 row is touched only "
    "by the one authorized append.",
]
S294_TXT = "\n\n".join(S294) + "\n\n"

# ---------------------------------------------------------------- E7 Part VI rows (after the Phase B rows)
ALPHA = one_line("| **Alpha-decay paper: correction of the deposit**")
GC1 = one_line("| **G-C1 gate** (angle-3")
assert s.count("\n" + ALPHA + "\n" + GC1 + "\n") == 1
ROWS = ("| **Audit follow-up, Phase C** (§2.94 — C1 the SLWE negative result; C2 the annotation batch; brief of October 6, "
        "2026; pre-registrations 778e3d4a (C1) and e538b2e5 (C2)) | **CLOSED (V4.94, October 7, 2026)** — C1: rank 76 at "
        "every k ≥ 7 (two-leg), 2^51 at spec with a uniform matrix, DFR = 0, the §3.05 correction carried; C2: ζ-tax "
        "gate 3 CLOSED — FAILED as framed; §2.50.A / OP-2.14 / G-QUANTA CONDITIONAL on I6; μ_n's factor-of-4 "
        "identification DOWNGRADED; the polycrystal floor and the ξ = ℓ_P license annotated; G-ζ1 appended to §2.52 "
        "Open 3 (freeze kept); fourteen math corrections. |\n"
        "| **Phase C draft awaiting the author** (the SLWE negative-result note → IACR ePrint; the crypto-project files "
        "`tools/lattice_estimate_results.md` and `tools/SLWE_Prime_Master_v2.md` §4.4 flagged as not describing the "
        "spec) | **Open — the author's approval** (V4.94; \"Draft, don't publish or send\") |\n"
        "| **Polycrystal validity floor** (§2.94.C2 P2 — elect N, the minimum number of lattice cells per grain for "
        "W^EM_∪; under the declared a_phys chain the edge is 4.96–19.82 cells, and N = 20 empties the window; the chain "
        "is itself conditional on G-S2C1-W's E-W-1(a)) | **Open — the author's election** (V4.94) |\n")

# ---------------------------------------------------------------- E3 fold-in record
R_ANCH = "**V4.93 fold-in record (October 7, 2026):**"
assert s.count(R_ANCH) == 1 and L[38].startswith(R_ANCH) and L[37] == ""
RECORD = ("**V4.94 fold-in record (October 7, 2026):** AUDIT FOLLOW-UP, PHASE C — two parts recorded as §2.94, under the "
          "author's brief of October 6, 2026 (\"C2. Annotation batch, one fold. Verify each item first.\"; \"Work out the "
          "blast radius every time … annotate those entries in the same fold\"; \"One short fold per phase\"; \"Draft, "
          "don't publish or send\"; `FOLD_AUTHORIZATION_V4_94.md`). C1 (pre-registration 778e3d4a, locked ce82bdc; two "
          "legs on the rank): rank 76 at k = 8, 16, 32, 64 at both primes; the lattice estimator gives 2^51.0 at spec "
          "with a uniform matrix (core-SVP cross-check β = 72); DFR = 0 by a worst-case bound; the sum-to-14 rule holds "
          "for 6 of 21 pairs; the ePrint note drafted, not submitted. C2 (pre-registration e538b2e5, locked d6fee69; "
          "second legs for P1, P3, P4 and the math reversals): ζ-tax gate 3 CLOSED — FAILED as framed; §2.50.A / OP-2.14 "
          "/ G-QUANTA CONDITIONAL; μ_n's factor-of-4 identification DOWNGRADED; the polycrystal floor and the ξ = ℓ_P "
          "license annotated; G-ζ1 appended to the §2.52 Open 3 row, the first fold authorized to touch it (\"Add the "
          "G-ζ1 result, and leave the freeze in place\"); fourteen math items. The blast radius is annotated in place: "
          f"{NBR} in-line [→ V4.94] brackets ({PARTS['C1']} C1, {PARTS['C2']} C2), plus three Part VI rows. Nothing "
          f"published, deposited or sent. Estate: {ESTATE} (head at fold `{HEAD_AT_FOLD}`); `git ls-remote` "
          f"{LS_REMOTE}: main = `3587eb3`. No §3.x; no observable bridge.\n\n")

# ---------------------------------------------------------------- E8 changelog
LINE_CH93 = one_line("*V4.93 (October 7, 2026): additions only")
assert L[4693] == LINE_CH93 and L[4694] == ""
CH_NEW = (f"*V4.94 (October 7, 2026): additions only — title/As-of header bump; the V4.94 fold-in record; §2.94 (audit "
          f"follow-up, Phase C) after §2.93; {NBR} in-line [→ V4.94] brackets on the blast-radius entries "
          f"({PARTS['C1']} C1, {PARTS['C2']} C2), one of them the single authorized append to the §2.52 Open 3 row; "
          "three Part VI rows after the Phase B rows; reverse-splice byte-identical to V4.93 (`0aa63a0b`).*")


def build():
    frags = [T_NEW, A_NEW, RECORD, S294_TXT, ROWS, CH_NEW] + [n for _, n in EDITS]
    for fr in [A_NEW, RECORD, S294_TXT, ROWS, CH_NEW]:
        assert s.count(fr) == 0
    out = s.replace(T_OLD, T_NEW, 1)
    out = out.replace(A_OLD, A_NEW, 1)
    out = out.replace(R_ANCH, RECORD + R_ANCH, 1)
    for old, new in EDITS:
        assert out.count("\n" + old + "\n") == 1
        out = out.replace("\n" + old + "\n", "\n" + new + "\n", 1)
    out = out.replace(REG93 + "\n\n" + J_ANCH, REG93 + "\n\n" + S294_TXT + J_ANCH, 1)   # §2.93's last line: no bracket
    out = out.replace("\n" + ALPHA + "\n", "\n" + ALPHA + "\n" + ROWS, 1)
    out = out.replace("\n" + LINE_CH93 + "\n", "\n" + LINE_CH93 + "\n" + CH_NEW + "\n", 1)
    o3_post = [x for x in out.split("\n") if x.startswith("| **§2.52 Open 3**")]
    assert o3_post == O3_NEW and out.count(O3_NEW[0]) == 1, "§2.52 Open 3 row is not V4.93 + the authorized append"
    assert O3_NEW[0].startswith(O3[:-2]) and O3_NEW[0].count("[→ V4.94") == 1
    for fr in frags:
        assert out.count(fr) == 1, f"fragment count != 1: {fr[:60]!r}"
    # reverse splice
    rev = out.replace("\n" + LINE_CH93 + "\n" + CH_NEW + "\n", "\n" + LINE_CH93 + "\n", 1)
    rev = rev.replace("\n" + ALPHA + "\n" + ROWS, "\n" + ALPHA + "\n", 1)
    rev = rev.replace(REG93 + "\n\n" + S294_TXT + J_ANCH, REG93 + "\n\n" + J_ANCH, 1)
    for old, new in EDITS:
        rev = rev.replace("\n" + new + "\n", "\n" + old + "\n", 1)
    rev = rev.replace(RECORD + R_ANCH, R_ANCH, 1)
    rev = rev.replace(A_NEW, A_OLD, 1)
    rev = rev.replace(T_NEW, T_OLD, 1)
    assert hashlib.md5(rev.encode("utf-8")).hexdigest() == V493 and rev == s, "REVERSE-SPLICE FAILED"
    return out


if __name__ == "__main__":
    out = build()
    open(OUT, "w", encoding="utf-8", newline="\n").write(out)
    b = open(OUT, "rb").read()
    print("V4.94 FOLDED:", OUT)
    print("bytes:", len(b), "(V4.93 %d B; delta +%d B); chars delta +%d" % (V493_BYTES, len(b) - V493_BYTES, len(out) - len(s)))
    print("md5:", hashlib.md5(b).hexdigest())
    print("brackets:", NBR, PARTS, "| §2.94 chars:", len(S294_TXT), "| record chars:", len(RECORD), "| rows chars:",
          len(ROWS))
    print("reverse-splice: BYTE-IDENTICAL to V4.93 (%s) — PASS" % V493)
    print("§2.52 Open 3: V4.93 row + exactly the one authorized append — PASS; all fragments landed exactly once — PASS")
