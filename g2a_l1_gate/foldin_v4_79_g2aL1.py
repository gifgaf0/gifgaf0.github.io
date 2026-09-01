#!/usr/bin/env python3
"""foldin_v4_79_g2aL1.py — STAGES V4.79: Gate G-2a-L1 (§2.87.J) — the spin–isospin locking assembly CLOSED two-leg + S9 cycle.
Eight additive edits on SQT_Master_Ledger_v4_78_CANONICAL.md (md5 98b9f63f...):
  E1 title; E2 As-of prepend (accumulated); E3 V4.79 fold-in record (before V4.78); E4 new §2.87.J
  (after §2.87.I, immediately before the §2.25 heading); E5 additive status annotation on §2.87.A's
  "Gate 2a, sharpened" paragraph; E6 P-4.b standing amendment (additive bracket at the P-4 origin,
  §2.91.L); E7 one Part VI gate row (after the G-BKZ32 row); E8 one changelog line.
§2.52 Open 3: untouched — the unique Part VI row asserted byte-identical pre/post, in addition to the
reverse-splice. Staging honesty: H-S9 (first Open 3 guard over-broad — matched all 131 lines MENTIONING
the row incl. the As-of header this fold edits; fail-closed halt fired before any write; guard narrowed
to the row itself). H-S10 (tooling: the staging script file was truncated by a failed open() with an
invalid newline argument during the guard patch; no ledger artifact was touched — the candidate had
never been written; script recreated whole).
Anchors asserted unique; reverse-splice reconstructs V4.78 byte-identically before the candidate is accepted."""
import hashlib

SRC = "/mnt/project/SQT_Master_Ledger_v4_78_CANONICAL.md"
OUT = "/mnt/user-data/outputs/SQT_Master_Ledger_v4_79_CANDIDATE.md"
V478 = "98b9f63f1158bd7e0af43f9129a51f06"
V478_BYTES = 1474281

s = open(SRC, encoding="utf-8").read()
assert hashlib.md5(s.encode("utf-8")).hexdigest() == V478, "base V4.78 md5 mismatch — halt"
assert len(s.encode("utf-8")) == V478_BYTES
L = s.split("\n")

# exact full anchors read from the file (never retyped)
ROW_BKZ   = L[4313]   # | **Gate G-BKZ32** (...) | **CLOSED (V4.78)** ... |
LINE_CH78 = L[4556]   # *V4.78 (August 27, 2026): additions only — ...*
assert ROW_BKZ.startswith("| **Gate G-BKZ32**") and s.count(ROW_BKZ) == 1
assert LINE_CH78.startswith("*V4.78 (August 27, 2026)") and s.count(LINE_CH78) == 1

# §2.52 Open 3 (directive item 5): the unique Part VI row line, captured verbatim (H-S9 narrowed guard)
O3_MARKS = [l for l in L if l.startswith("| **§2.52 Open 3**")]
assert len(O3_MARKS) == 1 and s.count(O3_MARKS[0]) == 1
O3_PRE = O3_MARKS[0]

# ---------------------------------------------------------------- E1 title
T_OLD = "# SQT Master Ledger — V4.78 Canonical\n"
T_NEW = "# SQT Master Ledger — V4.79 Canonical\n"
assert s.count(T_OLD) == 1

# ---------------------------------------------------------------- E2 As-of (accumulated prepend)
A_OLD = "**As of:** August 27, 2026 (V4.78 fold — "
A_SUM = ("**As of:** August 28, 2026 (V4.79 fold — **GATE G-2a-L1 CLOSED (two-leg + S9 resolution cycle) — the spin–isospin locking assembly, §2.87.J: the single physical identification standing between the framework and a derived μ_n is now a DERIVED-CONDITIONAL ASSEMBLY (R2, conditional on the enumerated imports), no longer a bare R3 postulate.** "
"Verdict of record, both legs identical at base: **B1 SPLIT** (sharpened NOT-INDUCED-BY-OBSTRUCTION — the spin sign is NOT induced by any pushforward ℤ/2-extension of the motion group M: z ∈ [Γ̃₂, Γ̃₂] and all 8 characters of Γ̃₂ kill it, the D2 naive quotient collapses to M (48), Pin-independent); "
"**B2 ASSEMBLED-RELOCATED** (the postulate's substrate lives in the point/motion sector: exactly 2 lifts over id_{S₄} between the spatial-image cover and the internal 2O, both fixing z; χ_{3/2} vanishes on every odd class; module transport unique; Pin-independent); "
"**B3 NEUTRAL** (the three admissibility lattices banked entry-for-entry with the parity law m ≠ 0 ⇒ J + I ∈ ℤ machine-verified on both legs; Assignment not forced). "
"Chat leg 2f0fa8f4 (8,484 assertions, locked prereg da9c25d1 July 11, 2026, re-executed byte-identical August 27); CC leg c3bea9ee (6,447 assertions, requested-variation methods: three-route B1 abelianization/𝔽₂-rank/brute-force, SU(2)/ℚ(ζ₈) internal 2O, Sym^n-trace characters, 𝔽₃ GL(2,3)); CC checkpoint 47ae0b85 deterministically regenerated chat-side. "
"S9 cycle: run-1 fired on four purely representational misses, all chat-side schema/comparator defects (H-S4..H-S7, + H-S8 add-on self-catch); comparator v1.1 faa233c0 FROZEN before either re-emission; run-2 C1–C6 ALL PASS both sides, base verdicts IDENTICAL. "
"D-CC-1 (pre-Phase-0 pager exposure) machine-scoped to chat-instrument lines 1–284 (Part 4 onward unexposed); weighting: B1 method-independent 2-of-3, exposure-partial; B2/B3 fully independent — not fold-blocking. LSF/collision check: novel-in-assembly verified both legs. "
"Standing amendment **P-4.b** adopted: quarantined embeds travel base64-armored. No μ_n; the dynamical clause remains open (M.CW); Gate 2a itself remains open; the §2.52 Open 3 row untouched. Full V4.79 record below. V4.78 fold (August 27, 2026) — ")
assert s.count(A_OLD) == 1

# ---------------------------------------------------------------- E3 fold-in record
R_ANCH = "**V4.78 fold-in record (August 27, 2026):**"
RECORD = ("**V4.79 fold-in record (August 28, 2026):** GATE FOLD, Gate-2a chain, author-authorized (directive recorded verbatim in `FOLD_AUTHORIZATION_V4_79.md` ae1af6c5ad4d99bfa670cb1928342be9, 1,078 B; staged-candidate hash reported back for final authorization per the directive) — "
"**Gate G-2a-L1 CLOSED; §2.87.J written; the sharpened Gate 2a upgraded from R3 postulate to derived-conditional assembly (R2, imports enumerated).** "
"Registration and lock: pre-registration `G_2a_L1_EXECUTION_PREREGISTRATION.md` LOCKED July 11, 2026, md5 da9c25d19ff91f2c0809ac0027a7bebb (18,381 B), byte-identical at recovery (August 27, 2026) to the chat-leg header citation — clean order register → lock → leg; no re-lock; no new elections. "
"Chat leg `g_2a_L1_chatleg.py` 2f0fa8f4abb85291250cb49a1bf756f2 (23,048 B; 8,484 assertions; exact ℚ(√2)/Cℓ(3)^± arithmetic, both Pin types), executed July 11, re-executed fresh August 27 (exit 0, ~5 s, ALL CHECKS PASS, byte-identical); chat-leg report 753a34ec (11,868 B); estate recovered from author upload after project-knowledge storage exhaustion (RECOVERY_RECORD.md, outputs). "
"CC dispatch (P-4 in-band, nine embeds byte-exact, verify-then-build) `G_2a_L1_CC_DISPATCH_INBAND.md` 0c5588ee19c2acd5cedb13e9b7472870 (79,695 B); T1 list 04438b74 (13 pattern lines, zero hits every instrument and checkpoint, both legs, independently cross-scanned); frozen comparator v1.0 67ee429a. "
"CC leg (blind, full-from-scratch, requested variation) `g_2a_L1_ccleg.py` c3bea9ee71765b196263ff2e5203708a (6,447 assertions; B1 by THREE independent routes — derived-subgroup/abelianization, brute-force character enumeration, 𝔽₂ relation-matrix rank; internal 2O as exact SU(2) matrices over ℚ(ζ₈); all characters by explicit Sym^n traces; GL(2,3) over 𝔽₃; F2 discriminator run FIRST per the prereg clause), commits 75e185e (pre-consultation checkpoint 47ae0b85, blindness ordering verified: byte-identical at 75e185e and c87d2e9) and c87d2e9 on `claude/new-session-wrjklk`; chat-side determinism cross-check: the CC instrument re-executed on the chat machine REGENERATES the checkpoint at 47ae0b85 byte-identical. "
"S9 cycle (comparator v1.0): four misses, ALL representational, ALL chat-side — H-S4 (schema 'sorted list' vs the instrument's SET of M⁺ element orders), H-S5 (free-text arm_sharpened compared exactly), H-S6 (GL23 transposition class counted in PGL (6) vs GL (12), both facts verified both legs; chat add-on gl23_class_level_addon.py 9cc8d314, independent 𝔽₃ enumeration: the 12 GL-preimages are ALL involutions), H-S7 (the prereg-permitted optional arm suffix -RELOCATED vs exact-string comparison), H-S8 (add-on self-catch: expected involution count corrected 6 → 12 by the machine). "
"Resolution per the G-CI1 precedent: comparator v1.1 `g_2a_L1_compare_v1_1.py` faa233c06c818b6168894c579ac35876 + schema v1.1 FROZEN BEFORE either re-emission (retains every numeric/boolean exact-identity; verified to still fire on an arm flip, a lattice entry, a group order); chat re-emission 8abda98d; S9 mini-dispatch (P-4) 8e27f85f (18,721 B, six embeds); CC re-emission 33d60888 (transform script asserts the v1.0 parent first; instrument untouched; chat-side machine check: differs from parent by EXACTLY the sanctioned deltas), commit 5975467; run-2 chat side AND CC side: C1–C6 ALL PASS, zero misses, VERDICT (base arms) IDENTICAL = (SPLIT, ASSEMBLED, NEUTRAL) — **S9 CLOSED**. "
"Deviations: D-CC-1 (pre-Phase-0 pager exposure of dispatch lines 1–668 = chat-instrument lines 1–284 EXACTLY, machine-mapped; Part 4 (F2) through Part 6 never rendered; of CC's three B1 routes the abelianization and 𝔽₂-rank routes have no counterpart in the exposed code — weighting: B1 method-independent 2-of-3, exposure-partial; B2/B3 fully independent; NOT fold-blocking; blindness under P-4 is procedural per the G-POLY1 H-8 disclosure), D-CC-2 (LSF collision check run post-hash pre-consultation to keep trap 1 sealed — accepted), D-CC-3 (F2-first phase-file write order per the prereg's own clause — logged, not silent). CC honesty items H-CC-1..3 filed in the CC report 0d0bfbf. "
"Staging honesty: H-S9 (the fold script's first §2.52-Open-3 guard was over-broad — it matched every line MENTIONING the row, 131 incl. the As-of header this fold edits — and fail-closed halted before any write; narrowed to the unique Part VI row), H-S10 (the staging script file itself was truncated by a failed open() during the guard patch; no ledger artifact touched; recreated whole). "
"LSF/collision check (both legs): NO published derivation of a soliton spin–isospin locking from orbifold/crystallographic spin-structure data; the which-double-cover question untreated in the Hantzsche–Wendt family — novel-in-assembly VERIFIED; nearest adjacent literature banked (Spin^c on HW manifolds; HW coverings; double crystallographic groups, Bilbao; FR constraints read from field/ADHM data). "
"**Standing amendment P-4.b adopted (from D-CC-1):** quarantined embeds travel base64-armored inside the single dispatch file so no viewer/pager can render them in the clear; byte-exactness and the one-file rule preserved (additive bracket at the P-4 origin, §2.91.L). "
"Registers: every computation R1-machine (both legs, exact arithmetic); the assembly reading R2 CONDITIONAL on the prereg §9 import list; the dynamical selection NOT claimed (M.CW wall; the I1–I3 ticket); NO μ_n; NO observable; Assignment OPEN (B3 NEUTRAL); Gate 2a itself remains OPEN — G-2a-L1 discharges its structural next-target. Folded as §2.87.J + the §2.87.A status annotation + one Part VI row + P-4.b. Full V4.79 record below. "
)
assert s.count(R_ANCH) == 1

# ---------------------------------------------------------------- E4 §2.87.J
SEC_ANCH = "\n### §2.25 — APS Boundary Term: Scalar Anchor Derivation\n"
assert s.count(SEC_ANCH) == 1
SEC = ("\n### §2.87.J Gate G-2a-L1 — The Spin–Isospin Locking Assembly: B1 SPLIT (the Spin Sign Is Not Induced by Any Pushforward Extension of the Motion Group), B2 ASSEMBLED-RELOCATED (the Locking Lives in the Point/Motion Sector; Exactly Two Lifts; Module Transport Unique), B3 Admissibility Lattices Banked with the Parity Law (Assignment NEUTRAL) — executed two-leg + S9 cycle, V4.79\n\n"
"**Date:** July 11, 2026 (lock + chat leg) → August 28, 2026 (fold). **Register:** R1-machine for every computation (both legs, exact arithmetic, both Pin types); R2 for the assembly reading, CONDITIONAL on the import list below. **Chain:** the Gate-2a bounded next target after S1–S10 (§2.87.B–§2.87.I); the §2.87.J reservation carried RETARGETED at every fold V4.63 → V4.78, discharged here.\n\n"
"**Lock and legs.** Pre-registration da9c25d1 (18,381 B) LOCKED July 11, 2026, before any leg ran; recovered byte-identical August 27 after project-knowledge storage exhaustion. Chat leg 2f0fa8f4 (23,048 B; 8,484 assertions; ℚ(√2)/Cℓ(3)^± exact; the D1 pushforward implemented as an ATTEMPT whose failure is exhibited as a theorem per the registration's own F4/F5 provision), re-executed fresh at recovery, byte-identical. CC leg c3bea9ee (6,447 assertions, blind, zero code reuse; requested variation delivered: B1 by three independent routes — derived-subgroup/abelianization quotient, brute-force character enumeration over all homomorphy products, 𝔽₂ relation-matrix rank — plus own coset enumeration for D2; internal 2O abstractly in SU(2) over ℚ(ζ₈); characters by explicit Sym^n(ℂ²) traces; GL(2,3) from scratch over 𝔽₃; the F2 discriminator run FIRST, before any framework data). Dispatch P-4 in-band 0c5588ee (79,695 B, nine embeds byte-exact); T1 04438b74 zero hits, both legs, cross-scanned. Determinism: the CC instrument re-executed chat-side regenerates its checkpoint 47ae0b85 byte-identical; the pre-consultation commit 75e185e carries the same bytes (blindness ordering verified).\n\n"
"**B1 — SPLIT (sharpened: NOT-INDUCED-BY-OBSTRUCTION), Pin-independent.** The spin sign carried by the flat home does NOT descend from any pushforward ℤ/2-extension of the motion group M ≅ ℤ/2 × S₄ (|M| = 48, center = the −I class): the candidate central element z is a commutator in Γ̃₂ (z = [q̃₁, q̃₂]), Hom(Γ̃₂, ℤ/2) has exactly 8 elements and every one kills z (chat: exhaustive word-cover + homomorphy; CC: abelianization, brute-force, and 𝔽₂-rank, mutually confirming), and the naive D2 quotient collapses to M itself (|Ñ/Γ̃| = 48). Both legs, both Pin types (e_i² = ±1), no Pin dependence. The obstruction is exhibited mechanically; the pre-committed re-pose lands the registered SPLIT arm.\n\n"
"**B2 — ASSEMBLED-RELOCATED, Pin-independent.** The locking's substrate is the point/motion sector: between the spatial-image cover and the internal 2O there exist EXACTLY 2 lifts over id_{S₄} (Aut(S₄) = Inn; S5 Φ), both fixing z; the spin-3/2 character χ_{3/2} vanishes on every odd class (chat: Chebyshev-on-scalar-parts; CC: Sym³ matrix traces — independent routes, identical values, ‖χ_{3/2}‖ = 1, χ_{3/2}(z) = −4); module transport is unique. The F2 discriminator (2O vs GL(2,3), transposition lifts order-4 vs involution preimages — CC additionally: the 12 GL-preimages of the size-6 PGL class form the single GL involution class) separates BEFORE any framework data, both legs.\n\n"
"**B3 — admissibility lattices banked; Assignment NEUTRAL.** The three multiplicity tables m(J, I; χ_FR) over the diagonal lock (2J ∈ {1,3,5,7}, 2I ∈ {1,3,5}; 2O-locked χ_FR = triv / sgn; 2T-restricted) agree entry-for-entry across the legs (8, 9, and 10 nonzero cells respectively), every entry a nonneg integer, and the parity law m ≠ 0 ⇒ J + I ∈ ℤ holds machine-verified in all three tables with mixed-parity control cells vanishing. The lattices do not force Assignment I vs II: disposition NEUTRAL, the discriminator remains a successor item.\n\n"
"**Two-leg comparison and the S9 cycle.** Run-1 (frozen comparator v1.0, 67ee429a): 51/51 numeric-boolean items and all three lattices IDENTICAL; S9 fired on four purely representational misses, every one a chat-side schema/comparator defect, owned as **H-S4** (set vs per-class list for the M⁺ element orders), **H-S5** (declared-free-text field compared exactly), **H-S6** (PGL-level 6 vs GL-level 12 for the transposition class; both true, both now verified both legs; chat add-on 9cc8d314 by independent 𝔽₃ enumeration), **H-S7** (the prereg-permitted -RELOCATED suffix vs exact-string comparison), plus **H-S8** (add-on self-catch: expected involution count 6 corrected to 12 by the machine — both lifts of an involution are involutions). Resolution per the G-CI1 precedent: comparator v1.1 faa233c0 + schema v1.1 FROZEN before either re-emission; chat re-emission 8abda98d; S9 mini-dispatch 8e27f85f (P-4, six embeds); CC re-emission 33d60888 (parent-md5-asserted transform, instrument untouched, machine-verified to differ by exactly the sanctioned deltas), commit 5975467. Run-2, chat side and CC side: C1–C6 ALL PASS, zero misses, base verdicts IDENTICAL — S9 CLOSED. Assertion counts 8,484 vs 6,447 reported, never compared.\n\n"
"**Deviations and honesty.** D-CC-1: a pager rendered dispatch lines 1–668 pre-Phase-0 = chat-instrument lines 1–284 exactly (machine-mapped); Part 4 (F2, line 317) through Part 6 never rendered; two of CC's three B1 routes have no counterpart in the exposed code; weighting — B1 method-independent 2-of-3, exposure-partial; B2/B3 fully independent; not fold-blocking (P-4 blindness is procedural, G-POLY1 H-8 carried). D-CC-2: LSF collision check post-hash pre-consultation (trap 1 kept sealed) — accepted. D-CC-3: F2-first write order per the prereg's own clause. CC's H-CC-1 (fail-stop ℚ(ζ₈) constructor crash pre-output), H-CC-2 (blind schema readings disclosed), H-CC-3 (arm-decision provenance) filed in the CC report 0d0bfbf. Staging: H-S9 (over-broad Open-3 guard, fail-closed halt, narrowed) and H-S10 (staging-script truncation by a failed open(); no ledger artifact touched; recreated) logged in the fold record. **P-4.b adopted from D-CC-1** (base64-armored quarantined embeds; see §2.91.L annotation).\n\n"
"**LSF / collision check (both legs, verbatim-logged).** No published derivation of a soliton spin–isospin locking from orbifold/crystallographic spin-structure data; the question 'which double cover of the isometry group does a flat-orbifold spin structure induce' is untreated in the #24/Hantzsche–Wendt family. Novel-in-assembly VERIFIED (registration-time expectation confirmed, not assumed). Nearest adjacent literature banked for the successor file: Spin^c structures on Hantzsche–Wendt manifolds; coverings of the HW manifold; double crystallographic groups (Bilbao server); FR constraints read from field data (pion-mass FR constraints; ADHM-data FR constraints).\n\n"
"**Imports and non-claims (prereg §9, binding).** The assembly reading is R2 CONDITIONAL on the enumerated imports (the S1–S10 chain content; the S7 Γ/N presentation as the one flagged shared layer; the diagonal lock; the χ_FR convention residue). Gate 2a is NOT closed: the dynamical selection of the locking is untouched (M.CW — combinatorics cannot produce dimensionful constants; the I1–I3 substrate-instantiation ticket), NO μ_n, NO observable, NO carrier identification, Assignment OPEN (B3 NEUTRAL; the discriminator is the named successor), the octahedral-representative gap stands, the gauge-paper §7.4 firewall held, the §2.52 Open 3 row untouched.\n\n"
"**Estate (md5 / bytes).** prereg da9c25d1/18,381; chat leg 2f0fa8f4/23,048; chat report 753a34ec/11,868; run log 30951582/1,807; dispatch 0c5588ee/79,695; T1 04438b74/117; comparator v1.0 67ee429a/3,267; chat ckpt v1.0 476052b1/2,296; CC leg c3bea9ee; CC ckpt v1.0 47ae0b85 (75e185e ≡ c87d2e9); CC report 0d0bfbf; comparator v1.1 faa233c0/4,989; chat ckpt v1.1 8abda98d/2,820; add-on 9cc8d314 + log; mini-dispatch 8e27f85f/18,721; CC ckpt v1.1 33d60888/3,226 (commit 5975467); CC v1.1 output 51f16e52; adjudication memo (chat) with run-1/run-2 records; fold authorization ae1af6c5/1,078.\n"
)

# ---------------------------------------------------------------- E5 §2.87.A status annotation
ANN_ANCH = "\n\n**What §2.87.A does NOT claim.**"
assert s.count(ANN_ANCH) == 1
ANNOT = ("\n\n**[V4.79 status annotation — Gate G-2a-L1, §2.87.J.]** The sharpened Gate 2a's *structural* content is upgraded from R3 postulate to **derived-conditional assembly (R2)**: B1 SPLIT (the spin sign is not induced by any pushforward ℤ/2-extension of M — obstruction exhibited, Pin-independent), B2 ASSEMBLED-RELOCATED (the locking's substrate is the point/motion sector: exactly 2 lifts over id_{S₄}, both fixing z; module transport unique), B3 lattices banked with the parity law (Assignment NEUTRAL). Conditional on the §2.87.J import list; the *dynamical* clause of the postulate remains open (M.CW; the I1–I3 ticket); no μ_n.")

# ---------------------------------------------------------------- E6 P-4.b amendment (additive bracket at the P-4 origin, §2.91.L)
P4_ANCH = "no side-channel ever load-bearing), folded this version together with"
assert s.count(P4_ANCH) == 1
P4_NEW = ("no side-channel ever load-bearing) **[V4.79 amendment P-4.b: quarantined embeds travel base64-armored within the single dispatch file, so no viewer/pager can render them in the clear; byte-exactness and the one-file rule preserved; adopted from G-2a-L1 D-CC-1 (§2.87.J)]**, folded this version together with")
assert s.count(P4_NEW) == 0

# ---------------------------------------------------------------- E7 Part VI row
ROW = ("| **Gate G-2a-L1** (§2.87.J — the spin–isospin locking assembly, the Gate-2a bounded next target after S1–S10; prereg da9c25d1 LOCKED July 11, 2026; chat leg 2f0fa8f4 8,484 asserts; CC leg c3bea9ee 6,447 asserts, requested-variation three-route B1 + SU(2)/ℚ(ζ₈) + Sym^n traces + 𝔽₃ GL(2,3); P-4 dispatch 0c5588ee, nine embeds; commits 75e185e/c87d2e9/5975467 on claude/new-session-wrjklk) "
"| **CLOSED (V4.79)** — B1 SPLIT / NOT-INDUCED-BY-OBSTRUCTION (z ∈ [Γ̃₂,Γ̃₂], all 8 characters kill z, D2 collapse 48, Pin-independent); B2 ASSEMBLED-RELOCATED (2 lifts over id_{S₄}, both fix z; χ_{3/2} kills odd classes; transport unique); B3 lattices entry-for-entry with the parity law, Assignment NEUTRAL. S9 cycle: run-1 four representational misses, ALL chat-side (H-S4..H-S7 + H-S8 self-catch; staging H-S9/H-S10 in the fold record); comparator v1.1 faa233c0 frozen pre-re-emission; run-2 ALL PASS both sides, base verdicts IDENTICAL. D-CC-1 machine-scoped (instrument lines 1–284; Part 4+ unexposed): B1 method-independent 2-of-3, exposure-partial; B2/B3 fully independent. LSF: novel-in-assembly verified. R2 conditional on the §2.87.J imports; dynamical clause open (M.CW); no μ_n; Assignment discriminator + I1–I3 named successors; P-4.b adopted. |")
assert ROW.count("|") == ROW_BKZ.count("|"), "Part VI cell-count mismatch: %d vs %d" % (ROW.count("|"), ROW_BKZ.count("|"))
assert s.count(ROW) == 0

# ---------------------------------------------------------------- E8 changelog
CH_NEW = ("*V4.79 (August 28, 2026): additions only — title/As-of header bump (V4.78 → V4.79; As-of date August 27 → August 28), the V4.79 fold-in summary prepended within the accumulated As-of header and the full V4.79 record at the top of the recent fold-in block (before V4.78), "
"§2.87.J (Gate G-2a-L1 — the spin–isospin locking assembly CLOSED two-leg + S9 cycle: B1 SPLIT / NOT-INDUCED-BY-OBSTRUCTION, B2 ASSEMBLED-RELOCATED, B3 lattices banked with the parity law, Assignment NEUTRAL; the §2.87.J reservation carried since V4.63 discharged) inserted after §2.87.I (immediately before the §2.25 heading), "
"one additive status annotation on §2.87.A's \"Gate 2a, sharpened\" paragraph (structural content upgraded to derived-conditional assembly, R2, imports enumerated; dynamical clause open), "
"the P-4.b standing amendment (base64-armored quarantined embeds, from G-2a-L1 D-CC-1) as an additive bracket at the P-4 origin in §2.91.L, "
"one new Part VI row (Gate G-2a-L1, after the G-BKZ32 row, carrying H-S4..H-S8 and the D-CC-1 weighting), and this changelog line. The §2.52 Open 3 row untouched (asserted byte-identical). Reverse-splice byte-verified against V4.78 (98b9f63f).*")
assert s.count(CH_NEW) == 0

# ================================================================ apply (forward)
out = s.replace(T_OLD, T_NEW, 1)
out = out.replace(A_OLD, A_SUM, 1)
out = out.replace(R_ANCH, RECORD + R_ANCH, 1)
out = out.replace(SEC_ANCH, "\n" + SEC + "### §2.25 — APS Boundary Term: Scalar Anchor Derivation\n", 1)
out = out.replace(ANN_ANCH, ANNOT + "\n\n**What §2.87.A does NOT claim.**", 1)
out = out.replace(P4_ANCH, P4_NEW, 1)
out = out.replace("\n" + ROW_BKZ + "\n", "\n" + ROW_BKZ + "\n" + ROW + "\n", 1)
out = out.replace(LINE_CH78, LINE_CH78 + "\n" + CH_NEW, 1)

# §2.52 Open 3 untouched (directive item 5; H-S9 narrowed guard)
O3_POST = [l for l in out.split("\n") if l.startswith("| **§2.52 Open 3**")]
assert O3_POST == [O3_PRE] and out.count(O3_PRE) == 1, "§2.52 Open 3 row changed — halt"

open(OUT, "w", encoding="utf-8", newline="\n").write(out)

# ================================================================ reverse-splice
rev = open(OUT, encoding="utf-8").read()
rev = rev.replace(LINE_CH78 + "\n" + CH_NEW, LINE_CH78, 1)
rev = rev.replace("\n" + ROW_BKZ + "\n" + ROW + "\n", "\n" + ROW_BKZ + "\n", 1)
rev = rev.replace(P4_NEW, P4_ANCH, 1)
rev = rev.replace(ANNOT + "\n\n**What §2.87.A does NOT claim.**", ANN_ANCH, 1)
rev = rev.replace("\n" + SEC + "### §2.25 — APS Boundary Term: Scalar Anchor Derivation\n", SEC_ANCH, 1)
rev = rev.replace(RECORD + R_ANCH, R_ANCH, 1)
rev = rev.replace(A_SUM, A_OLD, 1)
rev = rev.replace(T_NEW, T_OLD, 1)
rmd5 = hashlib.md5(rev.encode("utf-8")).hexdigest()
assert rmd5 == V478, "REVERSE-SPLICE FAILED: %s" % rmd5

b = open(OUT, "rb").read()
print("V4.79 CANDIDATE STAGED:", OUT)
print("bytes:", len(b), " (V4.78 was %d B; delta +%d B)" % (V478_BYTES, len(b) - V478_BYTES))
print("md5:", hashlib.md5(b).hexdigest())
print("reverse-splice: BYTE-IDENTICAL to V4.78 (%s) — PASS" % V478)
print("§2.52 Open 3: the Part VI row byte-identical and unique — PASS")
