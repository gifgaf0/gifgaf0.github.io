#!/usr/bin/env python3
"""foldin_v4_93_phase_b.py — FOLDS V4.93: the October 2026 audit follow-up, Phase B (papers and calculators).

Authorized by the author's brief of October 6, 2026 (audit_followup/inputs/BRIEF_2026-10-06_audit_followup.txt):
"Work out the blast radius every time. For each kill or downgrade, list every entry that depends on it and annotate those
entries in the same fold." / "One short fold per phase." / "Draft, don't publish or send." Base:
SQT_Master_Ledger_v4_92_CANONICAL.md (md5 a98cf1b6…, 1,800,402 B; produced by foldin_v4_92_phase_a.py).

Edits (all additive):
  E1 title; E2 As-of prepend; E3 the V4.93 fold-in record (before the V4.92 record);
  E5 §2.93 (after §2.92's last paragraph, before Cluster J);
  E6 in-line "[→ V4.93 …]" brackets at the end of each blast-radius line (inside the last cell for table rows);
  E7 three Part VI rows after the G-RCX1 row; E8 one changelog line.
(No E4: Phase B adds no Preamble rule.)
Anchors are read from the file and asserted unique; every fragment lands exactly once; the §2.52 Open 3 Part VI row is
asserted byte-identical; the reverse splice must reconstruct V4.92 byte-identically before the output is accepted.
"""
import hashlib

SRC = "/home/claude/fold/SQT_Master_Ledger_v4_92_CANONICAL.md"
OUT = "/home/claude/fold/SQT_Master_Ledger_v4_93_CANONICAL.md"
V492, V492_BYTES = "a98cf1b6f12578537e11270d2cdf0fda", 1800402
LS_REMOTE = "2026-10-07 19:05:01 UTC"            # main = 3587eb3 (PR #37); estate branch claude/audit-followup-oct6 = d21dcc4
ESTATE = "`audit_followup/` on branch `claude/audit-followup-oct6`"

s = open(SRC, encoding="utf-8").read()
assert hashlib.md5(s.encode("utf-8")).hexdigest() == V492, "base V4.92 md5 mismatch — halt"
assert len(s.encode("utf-8")) == V492_BYTES
L = s.split("\n")
assert len(L) == 4671 and L[-1] == "", "line structure changed — re-anchor"


def one_line(prefix):
    hits = [x for x in L if x.startswith(prefix)]
    assert len(hits) == 1, f"anchor not unique: {prefix!r} ({len(hits)})"
    assert s.count("\n" + hits[0] + "\n") == 1
    return hits[0]


O3 = one_line("| **§2.52 Open 3**")

# ---------------------------------------------------------------- E1 title
T_OLD = "# SQT Master Ledger — V4.92 Canonical\n"
T_NEW = "# SQT Master Ledger — V4.93 Canonical\n"
assert s.count(T_OLD) == 1 and L[0] + "\n" == T_OLD

# ---------------------------------------------------------------- E2 As-of
A_OLD = "**As of:** October 7, 2026 (V4.92 fold — "
assert s.count(A_OLD) == 1 and L[2].startswith(A_OLD)
A_NEW = ("**As of:** October 7, 2026 (V4.93 fold — **the October 2026 audit follow-up, Phase B (§2.93): B1 — the gauge "
         "paper's J = L_e₀ sign dressing (N-I) and sin θ_C = 3/13 excluded by PDG 2024 (+7.6σ/+8.5σ); PSL(2,7) is not the "
         "Császár polyhedron's symmetry group (AGL(1,7), order 42), and the paper never claimed it; v6.4 drafted; B2 — the "
         "PSL(2,7) note's v3 drafted (prior art cited; 146 circle-fixing elements, not 104); B3 — 'Zero Free Parameters' "
         "scoped and m_W = m₀φ²⁷, sin²θ_W = φ⁻³ retired in drafts of Paper VII and the three calculators; F₇* ⊄ PSL(2,7); "
         "quark L per tube diameter; B4 — the alpha-decay paper entered (51 steps; one robust break at Z = 88; ²⁰⁸Pb has "
         "Q_α > 0); B5 — the η/Flach item's purpose closed, a note drafted; B0 — no draft needed. Nothing published, "
         "deposited or sent.** V4.92 fold (October 7, 2026) — ")

# ---------------------------------------------------------------- E6 brackets (prefix, text, kind)
B1, B2, B3, B4, B5 = "§2.93.B1", "§2.93.B2", "§2.93.B3", "§2.93.B4", "§2.93.B5"
PREMISE = ("PSL(2,7) is the automorphism group of each face Fano plane, not of K₇ (S₇) or of the Császár face set "
           "(AGL(1,7))")
BR = [
    # ---- B1 blast radius (B1_RESULT.md, "Blast radius"; plus the fold-time sweep: §2.D-FC L534/L539, §2.74 Part II,
    #      the V4.7 §2.E-QQ entry, §2.86's cross-references)
    ("**Status:** Register 1 (direct consequence of SL(2,7) representation theory).",
     f"[→ V4.93 ({B1}): the SL(2,7) representation theory stands as R1, but its reading as the spin structure of K₇ or of "
     "the Császár polyhedron loses its premise — the symmetry-group sentence below is false as stated.]", "para"),
    ("**Cross-references:** §2.77 (V4.6, parent entry establishing the result); §2.E-WD",
     f"[→ V4.93 ({B1}): Paper I (v2.1, checked) calls PSL(2,7) the automorphism group of the Fano plane, and its 7-vertex "
     "coset graph is the multigraph 2·K₇; it never calls PSL(2,7) the automorphism group of K₇ (that is S₇) or of the "
     "Császár polyhedron.]", "para"),
    ("The K₇ (Császár polyhedron) symmetry group is PSL(2,7).",
     f"[→ V4.93 ({B1}): false as stated. PSL(2,7) ≅ GL(3,2) is the automorphism group of one face Fano plane (the "
     "octonion triple system). K₇'s automorphism group is S₇; the Császár face set's is AGL(1,7), of order 42, whose Schur "
     "multiplier is trivial (42 is squarefree), so it has no genuinely projective (spin) representations. Only the "
     "order-21 subgroup F₂₁ of PSL(2,7) preserves the whole face set.]", "para"),
    ("**Cross-references:** §2.29 Theorem 4 (Császár-Szilassi factorization 84 = 21 × 4)",
     f"[→ V4.93 ({B1}): misattributed — the gauge paper (v5, v6.3) never mentions PSL(2,7); the Császár face set's "
     "automorphism group is AGL(1,7), of order 42.]", "para"),
    ("2. The same automorphism group action on the 7-element basis.",
     f"[→ V4.93 ({B1}): the shared automorphism group is AGL(1,7), of order 42 (a map and its dual have the same "
     "automorphisms), not PSL(2,7); PSL(2,7) preserves only one of the two face Fano planes. The Part II conclusion rests "
     "on items 1 and 3 and stands.]", "para"),
    ("- **Császár automorphism group / PSL(2,7):** Gauge Group paper (v5).",
     f"[→ V4.93 ({B1}): misattributed — the gauge paper (v5, v6.3) never mentions PSL(2,7).]", "para"),
    ("**Cross-references:** §2.31 (sedenion ZD doubling-axis exclusion); §2.55",
     f"[→ V4.93 ({B1}): the gauge-paper attribution is wrong — the paper (v5, v6.3) never mentions PSL(2,7); the Császár "
     "face set's automorphism group is AGL(1,7).]", "para"),
    ("- **OP-2.75-CR (raised and CLOSED-with-result",
     f"[→ V4.93 ({B1}): premise restated — {PREMISE}; the SL(2,7) result stands as representation theory.]", "para"),
    ("The non-existence of a faithful 2-dim complex irrep of SL(2,7) is **not** a contingent feature",
     f"[→ V4.93 ({B1}): 'the K₇ symmetry group' — {PREMISE}; the SL(2, F_q) statement stands.]", "para"),
    ("§2.77 (V4.6, R1) established that the K₇ symmetry group's spin double cover",
     f"[→ V4.93 ({B1}): premise restated as at §2.D-FC — {PREMISE}; σ₄, σ₄' stand as SL(2,7) representation "
     "theory.]", "para"),
    ("- **§2.D-FC compliance.** §2.D-FC remains in force",
     f"[→ V4.93 ({B1}): 'K₇'s spin double cover' — premise restated as at §2.D-FC; the SL(2,7) fact stands.]", "para"),
    ("The three levels are not redundant; each carries a distinct algebraic phenomenon.",
     f"[→ V4.93 ({B1}): 'the discrete K₇ symmetry group' — {PREMISE}; the Q_8 ⊂ SL(2,3) ⊂ SL(2,7) chain stands as "
     "algebra.]", "para"),
    ("**Cross-references.** §2.74 (Császár/Szilassi = outer automorphism)",
     f"[→ V4.93 ({B1}): the gauge paper (v5, v6.3) treats the Fano planes but never mentions PSL(2,7).]", "para"),
    ("| **Gauge paper Furey-corpus prior-art memo + v6.2 attribution repairs**",
     f"[→ V4.93 ({B1}): CLOSED in the negative — the (b) sign dressing is not a reparametrization and is inconsistent "
     "(two legs, 32/32); claim (b) is withdrawn; sin θ_C = 3/13 is excluded by PDG 2024 (+7.6σ against |V_us|, +8.5σ "
     "against λ) and the tan θ_C agreement is post hoc; v6.4 drafted, awaiting the author.]", "row"),
    ("| **Gauge paper v6.3 attribution-completeness micro-edit + Zenodo publication**",
     f"[→ V4.93 ({B1}): v6.4 correction drafted (23 anchored hunks), not published.]", "row"),
    # ---- B2 (B2_RESULT.md, "Ledger annotations"; the §1.1 heading line is not bracketed — the Paper status bracket
    #      covers "SUBMISSION READY")
    ("**Theorem 2.1 (S₄ Uniqueness).**",
     f"[→ V4.93 ({B2}): superseded in the note — v2.1 (revised May 2026) lists the maximal subgroups as two S₄ classes "
     "(n₁ = 1 each, exchanged by the outer automorphism) and 7:3 (n₁ = 0), and calls D₄ the non-maximal Sylow "
     "2-subgroup; this copy predates v2.1 (checked by explicit computation).]", "para"),
    ("**Paper status:** Submitted to Journal of Algebra (JALGEBRA-D-26-00651)",
     f"[→ V4.93 ({B2}): stale, as is the heading's 'SUBMISSION READY' — per the V4.45 record the route ended at Finite "
     "Fields Appl. (FFA-26-260), declined without referee reports after transfer from J. Algebra; the note rests as the "
     "Zenodo deposit (v2, DOI 10.5281/zenodo.20532770); a v3 is drafted, not deposited.]", "para"),
    ("**Step (i): the paper's orbifold is ρ₈, hence bosonic",
     f"[→ V4.93 ({B2}): 146 elements, not 104 — the 42 elements of 4A also fix circles (ρ₈ fixed dimensions 4/2/2/2/2 "
     "on 2A/3A/4A/7A/7B), nested inside the S³ of their squares. The identification of the action as ρ₈ is unchanged. "
     "Corrected in the v3 draft of the note.]", "para"),
    # ---- B3 (B3_RESULT.md, "Ledger annotations"; plus the fold-time sweep: the W and Z rows, the §2.15 chain reading,
    #      the Flag 4 list item)
    ("The knot-to-particle mapping produces masses within 2%",
     f"[→ V4.93 ({B3}): the W and Z rows are retired as predictions (m_W = m₀φ²⁷; sin²θ_W = φ⁻³), so the fit is 6 rows "
     "against 6 fitted Z_f plus ξ_vac — dof still −1. The L values in the calculators and Paper VII mix conventions: the "
     "quark L are ropelengths per tube diameter (the up quark's 16.372 is the ideal trefoil, 32.743 per radius; every "
     "nontrivial knot has at least 15.66 per diameter), while L_e = 2π and L_B are per radius. Paper VII and the "
     "calculators are drafted with the scoped wording.]", "para"),
    ("| W boson | 82,128 MeV",
     f"[→ V4.93 ({B3}): retired as a prediction; PDG 2024 80.3692 ± 0.0133 GeV: +2.19%, 132σ.]", "row"),
    ("| Z boson | 93,964 MeV",
     f"[→ V4.93 ({B3}): retired with sin²θ_W = φ⁻³; PDG 2024 91.1880 ± 0.0020 GeV: +3.04%.]", "row"),
    ("- **Z_f = 6** from |F₇*| scalar action on the Fano plane",
     f"[→ V4.93 ({B3}): F₇* ≅ ℤ₆ is not a subgroup of PSL(2,7) (element orders 1, 2, 3, 4, 7), so it cannot act "
     "faithfully on PG(2,2) by collineations, and open verification (2)'s 'F₇*-orbit structure' is moot as stated. The "
     "order-6 stabilizer of a Fano triangle is S₃. §2.70's abstract ℤ/6 target is unaffected.]", "para"),
    ("- **Physical reading of the chain (R2, from §2.43):**",
     f"[→ V4.93 ({B3}): the order-6 stabilizer of a Fano triangle in PSL(2,7) is S₃, which is non-abelian; F₇* ≅ ℤ₆ is "
     "not a subgroup of PSL(2,7), which has no element of order 6.]", "para"),
    ("**C. Matter sector (A3) — §2.15 RETRACTED to Conjecture (two-leg, 46/46).**",
     f"[→ V4.93 ({B3}): lead confirmed — the quark L are ropelengths per tube diameter (the up quark's 16.372 is the "
     "ideal trefoil); L_e and L_B are per radius.]", "para"),
    ("This is *proven* exactly where the r_eff normalization to 1 at the electron",
     f"[→ V4.93 ({B3}): m_W = m₀·φ²⁷ and sin²θ_W = φ⁻³ are retired as predictions; of the three formulas only α⁻¹ remains "
     "on the list.]", "para"),
    ("**Load-bearing string flag (Flag 4).**",
     f"[→ V4.93 ({B3}): the string update is drafted for Paper VII, both store calculators and the public calculator, in "
     "the scoped wording; adoption pending the author.]", "para"),
    ("- **Flag 4 — the string-update task must not silently lapse.**",
     f"[→ V4.93 ({B3}): drafted; adoption pending the author.]", "para"),
    ("| **\"Zero Free Parameters\" string update**",
     f"[→ V4.93 ({B3}): drafted for Paper VII, `SQTCalculator.jsx`, `sqt_v20_merged.jsx` and the public calculator: one "
     "anchor (m_e), one selected scale (ξ_vac), per-particle selections, a leading-order fit; couplings excluded (Flag "
     "6). Open until the author adopts it.]", "row"),
    # ---- B4 (B4_RESULT.md, "Brackets"; plus the fold-time sweep: the M.CW instances line)
    ("**Instances.** Retired/thinned bridges:",
     f"[→ V4.93 ({B4}): the alpha-decay paper's text still claims two transitions (Z = 88 and Z = 92); at fixed N its own "
     "data show the Z = 88 break at every shared N and a Z = 92 difference that changes sign — consistent with this "
     "one-break record.]", "para"),
    ("**Statement (R2, current operative form).** For a phase-coupling function J(θ)",
     f"[→ V4.93 ({B4}, incidental): π/(2N) at N = 8 is π/16, not π/8; π/8 = 22.5° needs N = 4 (M.CW-b also pairs π/8 "
     "with a 4-fold operation). §2.18 and §2.20 use the 22.5° value.]", "para"),
    ("**Observation (R2).** Pb-208 is the heaviest stable doubly-magic nucleus.",
     f"[→ V4.93 ({B4}): Q_α(²⁰⁸Pb) = +516.7 keV (AME2020), and lighter lead isotopes have larger Q_α (²⁰⁶Pb +1134.9, "
     "²⁰⁴Pb +1968.5 keV). Alpha decay is already exothermic at and below ²⁰⁸Pb, which is stable in practice because the "
     "decay is unobservably slow; 'beyond which alpha-decay becomes thermodynamically inevitable' is false as stated.]",
     "para"),
    ("**Result (R2).** The U = 8 regime boundary in the alpha-decay slot framework",
     f"[→ V4.93 ({B4}): one even-Z step off — the regime I/II break is at Z = 88 (Ra), where the alpha-decay paper's data "
     "and the M.CW record put it; the closure invoked is at Z = 86 (Rn). (The paper counts U = Z − 80, so its U = 8 is "
     "Ra.) It also offers an atomic shell closure for a nuclear observable. The paper and the M.CW record attribute the "
     "Z = 88 break to octupole deformation. Not a prior address as stated.]", "para"),
    # ---- B5 (B5_RESULT.md, "Ledger bracket"; plus the fold-time sweep: §2.87's unification sentence)
    ("**The reduction [R1 core + R2].** An octahedral S₄-symmetric soliton",
     f"[→ V4.93 ({B5}): the internal-geometry half of this closed at V4.84 (§2.91.R: π₁(Orbit) = 0 — the 2π loop is "
     "contractible in the collective-coordinate orbit, so the substrate's internal geometry supplies no spin sign); the "
     "S⁷/PSL(2,7) η computation is no longer needed for that purpose.]", "para"),
    ("| **Full Donnelly η-defect sum for the FR parity**",
     f"[→ V4.93 ({B5}): its purpose — an FR spin sign from the internal geometry — closed at V4.84 (§2.91.R: "
     "π₁(Orbit) = 0). The S⁷/PSL(2,7) η remains a finite Donnelly sum over the conjugacy classes, computable in-house if "
     "still wanted. A short note to Flach is drafted, not sent.]", "row"),
]
EDITS = []
for prefix, text, kind in BR:
    old = one_line(prefix)
    assert "[→ V4.93" not in old
    if kind == "para":
        assert not old.endswith(" |")
        new = old + " " + text
    else:
        assert old.endswith(" |") and old.startswith("| ")
        new = old[:-2] + " " + text + " |"
    EDITS.append((old, new))
assert len({o for o, _ in EDITS}) == len(EDITS), "two brackets on one line"
NBR = len(EDITS)

# ---------------------------------------------------------------- E5 §2.93
J_ANCH = "## J. Multi-Lens Reference and Phase Incommensurability\n"
assert s.count(J_ANCH) == 1 and s.count("\n\n" + J_ANCH) == 1
REG92 = one_line("**Registers and non-claims.** A1–A3 numerics R1 (two-leg).")
assert s.count(REG92 + "\n\n" + J_ANCH) == 1
S293 = [
    "### §2.93 — The October 2026 Audit Follow-Up, Phase B: Papers and Calculators (V4.93)",
    f"*(Folded V4.93, October 7, 2026, under the author's brief of October 6 — \"One short fold per phase\"; estate {ESTATE}. "
    "Only B1 had a verdict decided by a new derivation, so only B1 was pre-registered and given a blind second leg; B0 and "
    "B2–B5 are annotations under the brief's proportionality rule. Every draft named here is unpublished — \"Draft, don't "
    "publish or send. Zenodo versions, journal notes and the note to Flach come back to me for approval.\" The affected "
    "entries carry short [→ V4.93 (§2.93.Bx)] pointers. No §3.x: the retirements are recorded here and bracketed in place, "
    "as at V4.92.)*",
    "**B0. Second-sound paper — no new draft.** All eight items the brief listed are already in v1 (md5 0dc9b1ea…), the "
    "text the author approved on October 4 (`lbc_bank/paper/APPROVAL_V1.md`), whose revision answered an outside review "
    "raising the same points. On item 4, v1 renamed the chemical potential (μ_c) rather than the shear modulus; both remove "
    "the clash. Phase A changes nothing in the paper, which uses a one-component soft-core supersolid, not the program's "
    "vacuum. Posting v1 and the journal submission are the author's.",
    "**B1. Gauge paper v6.3 — correction drafted (v6.4).** Pre-registration `B1_PREREG.md` 5374289d (locked at c2148ae); "
    "two legs, 32/32, the second an octonion construction that read nothing outside its own directory. (1) **DR-B1-1, "
    "(N-I):** the paper's J = L_e₀ sign dressing of Furey's Q = N/3 is not a reparametrization, and it is inconsistent. "
    "Y = (0, 1/3, −2/3, 1) is not affine in N (second differences −4/3 and 8/3); the N = 1 and N = 2 sectors are always "
    "conjugate in color (1, 3, 3̄, 1 or 1, 3̄, 3, 1); none of Furey's eight options gives the paper's table; and with either "
    "color convention one quark sector violates the color–charge correlation. Claim (b) of §5 and §9 claim (3) are "
    "withdrawn; §5's novelty is the matching of the three modes to the polyhedron's three Hamiltonian cycles. "
    "(2) **DR-B1-2:** sin θ_C = 3/13 is excluded by PDG 2024 (+7.60σ against |V_us| = 0.22431(85); +8.47σ against "
    "λ = 0.22501(68)), and running moves λ only by O(10⁻⁴) (Grossman et al., JHEP 06 (2022) 065). The tan θ_C reading "
    "agrees within 0.8σ but was chosen after seeing the data — the Eddington Maneuver as the ledger defines it — so v6.4 "
    "keeps it only as a labelled post-hoc conjecture and closes Open Problem (ix) negative. (3) **DR-B1-3:** neither v6.3 "
    "nor v5 mentions PSL(2,7). The Császár face set's automorphism group is AGL(1,7), of order 42: every element preserves "
    "the torus orientation, and the Schur multiplier is trivial because 42 is squarefree. PSL(2,7) ≅ GL(3,2) is the "
    "automorphism group of each face Fano plane, and only its subgroup F₂₁ preserves the whole face set. The claim that "
    "PSL(2,7) is the symmetry group of K₇ or of the polyhedron is the ledger's own: it attributes the claim to the gauge "
    "paper three times and to Paper I once, and builds on it in §2.D-FC, §2.74, OP-2.75-CR, §2.77, §2.E-WD and §2.E-QQ "
    "(all bracketed). (4) The gauge paper is not on record as under review at *Finite Fields Appl.*: \"v5\" is its Zenodo "
    "version number (record 21316171, content v6.3), and the only FFA submission on record, FFA-26-260, is the PSL(2,7) "
    "note, declined (V4.45). Draft: `phase_b/B1/v6_4_draft/` (23 anchored hunks, reverse-splice verified).",
    "**B2. PSL(2,7) note — v3 drafted.** Checks by explicit computation, one leg (they correct a count, citations and a "
    "description of the literature, and downgrade no result). ρ₈ = Ind_B^G(χ) from the order-21 Borel subgroup has "
    "character (8, 0, −1, 0, 1, 1) on 1A, 2A, 3A, 4A, 7A, 7B and fixed dimensions 4/2/2/2/2 on 2A/3A/4A/7A/7B, so 146 "
    "elements fix a circle on S⁷. Open Problem 4.4 said 104, omitting the 42 elements of 4A, whose circles lie inside the "
    "S³ of their squares. The maximal subgroups are 7:3 and two classes of S₄; the 21 D₄ are Sylow 2-subgroups, none "
    "maximal — as v2.1 (revised May 2026) already states. v3 is tracked changes on the author's v2.1 file (10 anchored "
    "edits, validated, reproducible build). It cites the classical literature for the 2-transitive, Gelfand-pair and "
    "distance-transitivity facts behind Theorem 2.3 and Lemmas 2.8–2.9 (Faradžev–Ivanov 1990; Praeger–Saxl–Yokoyama 1987; "
    "Inglis–Liebeck–Saxl 1986); corrects 104 to 146; replaces the false statement that Kawasaki's theorem covers only "
    "isolated singularities (the problem reduces to equivariant index theory on S⁷, and the η-invariant is a finite "
    "Donnelly sum); and fixes Kawasaki's year (1979), an appendix label and a typo. Not deposited. The author is to "
    "confirm that v2.1 is the text deposited as Zenodo v2 (DOI 10.5281/zenodo.20532770).",
    "**B3. Paper VII and the calculators — scoped wording; the electroweak formulas retired.** \"Zero Free Parameters\" "
    "becomes a leading-order fit with one anchor (m_e), one selected scale (ξ_vac = 100φ) and per-particle selections "
    "(knot, A, Z_f, L); couplings are excluded (§2.64.A Flag 6). The brief offered retire or scope for the two electroweak "
    "formulas. Both are retired: scoping would need a stated scale and scheme for φ⁻³ and a derivation of 27, and neither "
    "exists. m_W = m₀φ²⁷ = 82.1275 GeV against PDG 2024's 80.3692 ± 0.0133 GeV (+2.19%, 132σ). sin²θ_W = φ⁻³ = 0.23607 "
    "states no scale or scheme (M̄S at M_Z, 0.23129(4): +2.07%; on-shell, 0.22348(10): +5.63%), and m_Z = m_W/cos θ_W then "
    "misses 91.1880 GeV by +3.04%. Without W and Z, §2.1 is 6 rows against 6 fitted Z_f plus ξ_vac: dof still −1. Two "
    "corrections travel with the drafts. **F₇* is not a subgroup of PSL(2,7)**, which has no element of order 6 (orders "
    "1, 2, 3, 4, 7), so it cannot act faithfully on PG(2,2) by collineations; the order-6 stabilizer of a Fano triangle is "
    "S₃, so Conjecture 1's 6 survives as |S₃|, and §2.70's abstract ℤ/6 is unaffected. **The L values mix conventions:** "
    "the quark L are ropelengths per tube diameter (the up quark's 16.372 is the ideal trefoil, 32.743 per radius; every "
    "nontrivial knot has at least 15.66 per diameter, Denne–Diao–Sullivan 2006), while L_e = 2π and L_B are per radius — "
    "§2.92.C(6)'s lead, closed. Drafts, each compiled and rendered headless with every tab visited: the public calculator "
    "v3.1 (29 hunks), `SQTCalculator.jsx` v2.1 (29), `sqt_v20_merged.jsx` v1.9.1 (54; the Weak Bosons tab retired) and "
    "Paper VII (46). None is deployed; the live `index.html` and the store files are unchanged.",
    "**B4. The alpha-decay paper — ledger entry.** \"Three-Regime Structure in α-Decay Q-Value Isotone Steps in the "
    "Deformed Actinide Region\" (M. Gifford, May 2026). Checked: the project-store text (md5 770ac497); the deposit's DOI "
    "and date are to be entered by the author. *Data (R1).* 96 even-even Q_α > 0 from AME2020, seven benchmarks to "
    "≤ 0.2 keV. For N > 128 the regime table reproduces exactly (0.308 / 0.599 / 1.007 MeV, n = 7 / 14 / 30). That is 51 "
    "steps; the text's 74 is the all-N count, for which regimes I and II do not separate. *Claims* (descriptive "
    "comparisons at fixed N; no verdict rests on them). The Z = 88 break holds at every shared N (+0.09 to +0.47 MeV over "
    "N = 130–136) and has the conventional octupole-deformation account (R2 observation). The Z = 92 break is not "
    "supported as a Z effect: at fixed N it changes sign (−0.16 to +0.25 MeV over N = 134–146), and it is smaller than the "
    "drift with N inside one boundary (Th→U, 0.35 to 0.94 MeV over N = 136–146). This agrees with the M.CW record that the "
    "finding reduced on audit to one real break, at Z = 88. §4.5–§4.6 rest on Lemma θ (§2.17, R2, whose π/8 sign flip "
    "and Route 1 sketch are retracted, §3.01–§3.02), in a form of J(θ) that is not the ledger's J₀ cos(Nθ), and §4.6 reads "
    "U = 16 as an algebra transition (2 × dim 𝕆), a capacity reading of the kind §3.A.2 retracted. Such readings depend "
    "on measuring U from Hg (Z = 80): from ²⁰⁸Pb the boundaries sit at ΔU = 6 and 10, as §4.5 notes, and the ledger's "
    "slot framework counts U differently (§2.45-NGA puts U = 8 at Rn; §3.A.4 puts ²⁴⁰Pu at U = 16). The cited gauge "
    "paper (ref. [11]) contains neither J(θ) nor Lemma θ. The Curium prediction failed, as §4.6 says (\"not "
    "confirmed\"); the abstract's \"Cm→Cf half … confirmed\" overstates a t = +0.4. *Retraction "
    "check.* No slot counting and no sin²(πU/4) (§3.A.3); §2.45-NGA is not used. The paper's \"terminus toward which all "
    "actinide chains converge\" is wrong — only the 4n series ends at ²⁰⁸Pb — and ledger §2.21 errs nearby "
    "(Q_α(²⁰⁸Pb) = +516.7 keV). *Disposition.* The data and the Z = 88 observation are banked (R2); the two-transition "
    "claim and §4.5–§4.6 are not supported; correcting the deposit is the author's decision (Part VI); a formal "
    "N-controlled test would need a pre-registered rule.",
    "**B5. The η/Flach item — purpose closed; note drafted.** The Part VI row \"Full Donnelly η-defect sum for the FR "
    "parity\" existed to decide whether the internal geometry fixes a Finkelstein–Rubinstein spin sign. That closed at "
    "V4.84 (§2.91.R: π₁(Orbit) = 0 — the 2π loop is contractible in the collective-coordinate orbit, so the internal "
    "geometry supplies no spin sign). The space on record is S⁷/PSL(2,7) (§2.87; the store addendum's step (iii)), not "
    "ℙ¹(2,3,7). If the S⁷/PSL(2,7) number is still wanted, Donnelly's equivariant η is a finite sum over the conjugacy "
    "classes, built from fixed-point data already on record (B2), and can be computed in-house. A short note to Flach "
    "covering both readings is drafted and not sent: on ℙ¹(2,3,7) the Dirac η vanishes by chirality, the order-2 cone "
    "point may obstruct a spin structure, and the meaningful version lives on Σ(2,3,7).",
    "**Registers and non-claims.** B1's three verdicts R1 (pre-registered, two-leg). B2: R1 for the computed facts. B3 and "
    "B4: R1 for the arithmetic, R2 for the dispositions. Nothing is published, deposited, deployed or sent; the drafts sit "
    "on a public branch of the repository until the author decides. No register promoted; no observable bridge (M.BRIDGE "
    "intact); §2.52 Open 3 untouched.",
]
S293_TXT = "\n\n".join(S293) + "\n\n"

# ---------------------------------------------------------------- E7 Part VI rows (after the G-RCX1 row)
RCX1 = one_line("| **Gate G-RCX1** (registered by §2.92.C")
C1_ANCH = one_line("| **G-C1 gate** (angle-3")
assert s.count("\n" + RCX1 + "\n" + C1_ANCH + "\n") == 1
ROWS = ("| **Audit follow-up, Phase B** (§2.93 — B0 second-sound paper, B1 gauge paper, B2 PSL(2,7) note, B3 Paper VII "
        "and the calculators, B4 alpha-decay paper, B5 the η/Flach item; brief of October 6, 2026; B1 pre-registration "
        "5374289d) | **CLOSED (V4.93, October 7, 2026)** — B1 (N-I), sin θ_C = 3/13 excluded, the PSL(2,7)-symmetry claim "
        "restated; B2 v3 drafted; B3 the scoped wording and the electroweak retirement drafted (F₇* ⊄ PSL(2,7); L "
        "conventions); B4 entered; B5 purpose closed; B0 no draft needed. §2.52 Open 3 untouched. |\n"
        "| **Phase B drafts awaiting the author** (gauge paper v6.4 → Zenodo; PSL(2,7) note v3 → Zenodo; public calculator "
        "v3.1 → `index.html`; `SQTCalculator.jsx` v2.1 and `sqt_v20_merged.jsx` v1.9.1 → the store; the Paper VII October "
        "draft; the note to Flach; posting of the approved second-sound v1) | **Open — the author's approval** (V4.93; "
        "\"Draft, don't publish or send\"); the drafts sit on a public branch |\n"
        "| **Alpha-decay paper: correction of the deposit** (§2.93.B4 — 74 → 51 steps; one robust break at Z = 88, or a "
        "pre-registered N-controlled test before claiming Z = 92; §4.5–§4.6 and ref. [11]; the abstract's Curium "
        "sentence; the decay-chain endpoints; ref. [9]; the deposit's DOI and date to be entered) | **Open — the author's "
        "decision** (V4.93) |\n")

# ---------------------------------------------------------------- E3 fold-in record
R_ANCH = "**V4.92 fold-in record (October 7, 2026):**"
assert s.count(R_ANCH) == 1 and L[38].startswith(R_ANCH) and L[37] == ""
RECORD = ("**V4.93 fold-in record (October 7, 2026):** AUDIT FOLLOW-UP, PHASE B — six parts recorded as §2.93, under the "
          "author's brief of October 6, 2026 (\"Work out the blast radius every time … annotate those entries in the same "
          "fold\"; \"One short fold per phase\"; \"Draft, don't publish or send\"; `FOLD_AUTHORIZATION_V4_93.md`). B0 "
          "second-sound paper: all eight items already in the approved v1; no draft. B1 gauge paper (pre-registered; "
          "two-leg, 32/32): the sign dressing (N-I), sin θ_C = 3/13 excluded, the PSL(2,7)-symmetry claim the ledger's own; "
          "v6.4 drafted. B2 PSL(2,7) note: v3 drafted (prior art; 104 → 146). B3: the scoped wording and the retirement of "
          "m_W = m₀φ²⁷ and sin²θ_W = φ⁻³ drafted for Paper VII, both store calculators and the public calculator; "
          "F₇* ⊄ PSL(2,7); the L-convention lead closed. B4: the alpha-decay paper entered (§2.93.B4). B5: the η/Flach "
          f"item's purpose closed; a note drafted. The blast radius is annotated in place: {NBR} in-line [→ V4.93] "
          "brackets, plus three Part VI rows. Nothing published, deposited, deployed or sent. Estate: " + ESTATE +
          " (head at fold `d21dcc4`); `git ls-remote` " + LS_REMOTE + ": main = `3587eb3` (PR #37). No §3.x; no "
          "observable bridge; §2.52 Open 3 untouched.\n\n")

# ---------------------------------------------------------------- E8 changelog
LINE_CH92 = one_line("*V4.92 (October 7, 2026): additions only")
assert L[4669] == LINE_CH92
CH_NEW = (f"*V4.93 (October 7, 2026): additions only — title/As-of header bump; the V4.93 fold-in record; §2.93 (audit "
          f"follow-up, Phase B) after §2.92; {NBR} in-line [→ V4.93] brackets on the blast-radius entries; three Part VI "
          "rows after the G-RCX1 row; reverse-splice byte-identical to V4.92 (`a98cf1b6`); the §2.52 Open 3 row "
          "untouched.*")


def build():
    frags = [T_NEW, A_NEW, RECORD, S293_TXT, ROWS, CH_NEW] + [n for _, n in EDITS]
    for fr in [A_NEW, RECORD, S293_TXT, ROWS, CH_NEW]:
        assert s.count(fr) == 0
    out = s.replace(T_OLD, T_NEW, 1)
    out = out.replace(A_OLD, A_NEW, 1)
    out = out.replace(R_ANCH, RECORD + R_ANCH, 1)
    for old, new in EDITS:
        assert out.count("\n" + old + "\n") == 1
        out = out.replace("\n" + old + "\n", "\n" + new + "\n", 1)
    out = out.replace(REG92 + "\n\n" + J_ANCH, REG92 + "\n\n" + S293_TXT + J_ANCH, 1)   # §2.92's last line carries no bracket
    out = out.replace("\n" + RCX1 + "\n", "\n" + RCX1 + "\n" + ROWS, 1)
    out = out.replace("\n" + LINE_CH92 + "\n", "\n" + LINE_CH92 + "\n" + CH_NEW + "\n", 1)
    O3_POST = [x for x in out.split("\n") if x.startswith("| **§2.52 Open 3**")]
    assert O3_POST == [O3] and out.count(O3) == 1, "§2.52 Open 3 row changed — halt"
    for fr in frags:
        assert out.count(fr) == 1, f"fragment count != 1: {fr[:60]!r}"
    # reverse splice
    rev = out.replace("\n" + LINE_CH92 + "\n" + CH_NEW + "\n", "\n" + LINE_CH92 + "\n", 1)
    rev = rev.replace("\n" + RCX1 + "\n" + ROWS, "\n" + RCX1 + "\n", 1)
    rev = rev.replace(REG92 + "\n\n" + S293_TXT + J_ANCH, REG92 + "\n\n" + J_ANCH, 1)
    for old, new in EDITS:
        rev = rev.replace("\n" + new + "\n", "\n" + old + "\n", 1)
    rev = rev.replace(RECORD + R_ANCH, R_ANCH, 1)
    rev = rev.replace(A_NEW, A_OLD, 1)
    rev = rev.replace(T_NEW, T_OLD, 1)
    assert hashlib.md5(rev.encode("utf-8")).hexdigest() == V492 and rev == s, "REVERSE-SPLICE FAILED"
    return out


if __name__ == "__main__":
    out = build()
    open(OUT, "w", encoding="utf-8", newline="\n").write(out)
    b = open(OUT, "rb").read()
    print("V4.93 FOLDED:", OUT)
    print("bytes:", len(b), "(V4.92 %d B; delta +%d B); chars delta +%d" % (V492_BYTES, len(b) - V492_BYTES, len(out) - len(s)))
    print("md5:", hashlib.md5(b).hexdigest())
    print("brackets:", NBR, "| §2.93 chars:", len(S293_TXT), "| record chars:", len(RECORD), "| rows chars:", len(ROWS))
    print("reverse-splice: BYTE-IDENTICAL to V4.92 (%s) — PASS" % V492)
    print("§2.52 Open 3: Part VI row byte-identical and unique — PASS; all fragments landed exactly once — PASS")
