#!/usr/bin/env python3
"""co1_classify.py — CO-1: classify every Part VI row of the V4.96 ledger under §2.97.C rules (a)–(h).

Reads SQT_Master_Ledger_v4_96_CANONICAL.md (md5 120b076a…), parses every Part VI table row, and applies the hand-made
mapping below (one entry per row, keyed by the V4.96 line number). Writes CO1_CLASSIFICATION.md and
co1_classification.json. Checks: every table row is in the mapping exactly once, every mapping key is a table row,
each row's lead status agrees with its recorded label class, and the counts add up.

Scope (the brief's words): rows that are Open, Registered, Standing or Partially executed, judged by the row's lead
status (the status written first in its cell). Later in-cell updates decide only the pointer: a row whose own cell
already records it CLOSED, ANSWERED or ELECTED gets no pointer (the brief: none on rows already closed).
"""
import hashlib
import json
import re
import sys

SRC = "/home/claude/fold/SQT_Master_Ledger_v4_96_CANONICAL.md"
MD5 = "120b076a613b7ef4074193c03df2cf0d"
s = open(SRC, encoding="utf-8").read()
assert hashlib.md5(s.encode("utf-8")).hexdigest() == MD5, "base V4.96 md5 mismatch"
L = s.split("\n")
P6 = next(i for i, x in enumerate(L) if x.startswith("# PART VI — OPEN TASKS")) + 1          # 1-based
CL = next(i for i, x in enumerate(L) if x.startswith("## Closed / dropped (carried forward")) + 1

# ------------------------------------------------------------------ parse the Part VI tables
rows, sec = [], None
for n in range(P6, CL):
    x = L[n - 1]
    if x.startswith("## "):
        sec = x[3:]
    elif x.startswith("| ") and not x.startswith("| Task |") and not x.startswith("|---"):
        k = x.find(" | ", 2)                       # first cell separator (inner pipes carry no spaces around them)
        task, status = x[2:k], x[k + 3:]
        assert status.endswith(" |") or status.endswith("|"), n
        rows.append({"line": n, "section": sec, "task": task, "status": status.rstrip(" |")})
bullets = [n for n in range(CL + 1, len(L) + 1) if L[n - 1].startswith("- ")]
bullets = [n for n in bullets if n < next(i for i in range(CL, len(L)) if L[i].startswith("---")) + 1]

# ------------------------------------------------------------------ the mapping
# label: lead-status class. rule: (a) (b-split) (b-math) (c) (d) (e) (f) (h) B.4, or OUT for rows out of scope.
# ptr: pointer kind for the fold (None = no pointer). note: why.
A, BS, BM, C, D, E, F, H, B4, OUT = "(a)", "(b) split", "(b) math", "(c)", "(d)", "(e)", "(f)", "(h)", "B.4", "out"
M = {
    # ---- High-priority structural gates
    4432: ("L4.5 gate", "Open", A, "a", "named in C(a)"),
    4433: ("§2.52 Open 3", "Open", F, None, "the freeze is honoured: no pointer, text untouched; listed as closed in the new 'Substrate program' row"),
    4434: ("§2.50 gate", "Open", A, "a", "named in C(a)"),
    4435: ("§4.7 / Conjecture 1 Item 2 (top-quark knot)", "Open", A, "a", "Part IV §4.7 named in C(a)"),
    4436: ("§2.7 ε-per-edge", "Open", A, "a", "named in C(a)"),
    4437: ("§2.45-NGA Bjerknes gate", "Open", A, "a", "named in C(a)"),
    4438: ("§2.53 bilateral fold from §3.4", "Partially executed (lead: ADVANCED)", A, "a",
           "ADVANCED read as partially executed (flagged); the open content is the substrate metric/dynamics import (I1–I3)"),
    4439: ("§2.70 verification check", "Closed", OUT, None, "CLOSED (V4.3)"),
    4440: ("§2.71 candidate-location audit", "Open", BM, None, "a structural cross-check between sections; stays open"),
    4441: ("G-ζ1", "Open (registered V4.35)", A, "a", "named in C(a); its cell records EXECUTED (V4.36, DEGENERATE)"),
    4442: ("G-INT1", "Executed", OUT, None, "EXECUTED (V4.47)"),
    4443: ("M.ONT gate", "Open (registered V4.35)", A, "a_mont", "named in C(a); its cell records DECLARED (V4.51) and the annexes"),
    4444: ("Gate G-κ1", "Open (registered V4.51)", A, "a", "named in C(a); its cell records EXECUTED (V4.52)"),
    4445: ("Gate G-2a-S4", "Executed", OUT, None, "EXECUTED (V4.53)"),
    4446: ("Gate G-2a-S5", "Executed", OUT, None, "REGISTERED + EXECUTED (V4.54)"),
    4447: ("Gate G-2a-S6", "Executed", OUT, None, "REGISTERED + EXECUTED (V4.55)"),
    4448: ("Gate G-2a-S7", "Executed", OUT, None, "REGISTERED + EXECUTED (V4.56)"),
    4449: ("Gate G-2a-S8", "Executed", OUT, None, "REGISTERED + EXECUTED (V4.57)"),
    4450: ("Gate G-2a-S9", "Executed", OUT, None, "REGISTERED + EXECUTED (V4.60)"),
    4451: ("Gate G-2a-S10", "Executed", OUT, None, "REGISTERED + LOCKED + EXECUTED (V4.62)"),
    4452: ("Gate G-IIB-L1", "Registered", A, "a", "named in C(a); its cell records EXECUTED (V4.64)"),
    4453: ("Gate G-CC-ε1", "Registered", A, "a", "named in C(a); its cell records EXECUTED (V4.66)"),
    4454: ("Gate G-SCALE1", "Registered", A, "a",
           "the substrate-scale import; its cell records DECLARED + EXECUTED, FAIL (V4.67); treated like the named executed gates"),
    4455: ("Gate G-TSH1", "Executed", OUT, None, "REGISTERED + LOCKED + EXECUTED (V4.68)"),
    4456: ("Gate G-TSH2", "Executed", OUT, None, "REGISTERED + LOCKED + EXECUTED (V4.69)"),
    4457: ("Gate G-TSH3", "Executed", OUT, None, "REGISTERED + LOCKED + EXECUTED (V4.70)"),
    4458: ("Gate G-TSH4", "Executed", OUT, None, "REGISTERED + LOCKED + EXECUTED (V4.72)"),
    4459: ("Gate G-POLY1", "Partially executed", A, None,
           "named in C(a), but its cell records CLOSED: GATE COMPLETE (V4.76), so no pointer (flagged)"),
    4460: ("Gate G-CI1", "Closed", OUT, None, "CLOSED (V4.77)"),
    4461: ("Gate G-BKZ32", "Closed", OUT, None, "CLOSED (V4.78)"),
    4462: ("Gate G-2a-L1", "Closed", OUT, None, "CLOSED (V4.79)"),
    4463: ("Gate G-S2C1", "Closed", OUT, None, "CLOSED (V4.80)"),
    4464: ("Gate G-S2C1-W", "Closed", OUT, None, "CLOSED (V4.81)"),
    4465: ("Gate G-QUANTA", "Closed", OUT, None, "CLOSED (V4.82); its discriminator is listed in the Successor intake by reference (C(e))"),
    4466: ("Gate G-MSCS1", "Closed", OUT, None, "CLOSED (V4.83)"),
    4467: ("Gate G-2a-A1", "Closed", OUT, None, "CLOSED (V4.84)"),
    4468: ("Gate G-MSCS2", "Closed", OUT, None, "CLOSED (V4.85)"),
    4469: ("Gate G-MSCS-A", "Closed", OUT, None, "CLOSED (V4.87)"),
    4470: ("Gate G-VS1", "Closed", OUT, None, "CLOSED (V4.88)"),
    4471: ("Audit follow-up, Phase A", "Closed", OUT, None, "CLOSED (V4.92)"),
    4472: ("Gate G-OBD1", "Registered", A, "a_obd", "named in C(a): closed unopened"),
    4473: ("Gate G-RCX1", "Registered", E, "e_rcx", "named in C(e); re-scoped in the intake block"),
    4474: ("Audit follow-up, Phase B", "Closed", OUT, None, "CLOSED (V4.93)"),
    4475: ("Phase B drafts awaiting the author", "Open", D, None, "named in C(d)"),
    4476: ("Alpha-decay paper: correction of the deposit", "Open", D, None, "named in C(d)"),
    4477: ("Audit follow-up, Phase C", "Closed", OUT, None, "CLOSED (V4.94)"),
    4478: ("Phase C draft awaiting the author", "Open", D, None, "named in C(d)"),
    4479: ("Polycrystal validity floor", "Open", A, None, "its cell records ELECTED (V4.96), so no pointer"),
    4480: ("Lattice-spacing bound", "Recorded", OUT, None, "RECORDED (V4.95), a bound, not a task"),
    4481: ("G-C1 gate", "Executed", OUT, None, "EXECUTED (V4.48)"),
    4482: ("G-2a-S1 / G-2a-S2", "Executed", OUT, None, "EXECUTED (V4.49)"),
    # ---- Cryptographic thread
    4488: ("OP-2.58.1.a", "Closed", OUT, None, "CLOSED by §2.66 + §2.66.1"),
    4489: ("OP-2.58.1.b", "Open", C, None, "crypto"),
    4490: ("OP-2.58.2", "Open", C, None, "crypto"),
    4491: ("OP-2.58.2c", "Open", C, None, "crypto (moot per §2.94.C1)"),
    4492: ("OP-2.58.2d", "Open", C, None, "crypto (closed at the public-matrix level, V4.78)"),
    4493: ("OP-2.58.2e", "Open", C, None, "crypto"),
    4494: ("OP-2.58.3", "Open", C, None, "crypto"),
    4495: ("OP-2.58.4", "Open", C, None, "crypto (its own words: a physics-crypto connection); untouched per C(c)"),
    4496: ("OP-2.58.5", "Open", C, None, "crypto"),
    4497: ("OP-2.59-A, B, C", "Open", C, None, "crypto"),
    4498: ("RD-01 to RD-04", "Open", C, None, "crypto"),
    4499: ("OP-2.62.3", "Open", C, None, "crypto thread"),
    4500: ("OP-2.62.4", "Open", C, None, "crypto thread"),
    4501: ("Phase B Entry 006", "Closed", OUT, None, "CLOSED by §2.69"),
    4502: ("§2.66.2 source recovery or §2.66.3 re-derivation", "Open", C, None, "crypto"),
    4503: ("Cluster M citation hygiene sweep", "Open", C, None, "crypto"),
    # ---- Sedenion / Fano-line
    4509: ("OP-2.25.2-V1", "Open", BM, None, "pure mathematics"),
    4510: ("OP-2.25.2-V2", "Closed", OUT, None, "CLOSED (superseded by §2.55)"),
    4511: ("OP-2.25.2-V3", "Closed", OUT, None, "CLOSED (V4.17)"),
    4512: ("OP-2.81.1", "Open", BM, None, "pure mathematics"),
    4513: ("OP-2.81.2", "Open", BM, None, "pure mathematics; its cell records CLOSED (V4.94)"),
    4514: ("OP-2.25.2-V4", "Closed", OUT, None, "CLOSED (V4.17)"),
    # ---- Capacity / statistics
    4520: ("OP-2.67.1", "Superseded", OUT, None, "Split by §2.68.5 into 1a / 1b / 1c (the children are rows)"),
    4521: ("OP-2.67.1a", "Closed", OUT, None, "CLOSED (Tier 2)"),
    4522: ("OP-2.67.1b (original)", "Superseded", OUT, None, "REFRAMED by §2.68.8.2 (the reframed row follows)"),
    4523: ("OP-2.67.1b reframed", "Open", BS, "b_6771b",
           "derive CD doubling from p6m capacity exhaustion: an algebraic question read physically (K₇ closures on the vacuum lattice)"),
    4524: ("OP-2.67.1c", "Open", A, "a_6771c", "its own words: a physical-mechanism question (exchange statistics)"),
    4525: ("OP-2.67.6", "Standing", B4, None, "named in §2.97.B.4: the gates stay in force for any statistics-from-geometry claim"),
    # ---- Geometric / combinatorial
    4531: ("OP-C7-1", "Open", H, None, "its target, '§2.7 Open Problem 3', is not defined in the ledger"),
    4532: ("OP-C7-2", "Open", BM, None, "pure mathematics (the K₇ embedding's symmetry)"),
    4533: ("OP-C7-3", "Open", BM, None, "pure mathematics"),
    4534: ("OP-C7-4", "Open", C, None, "crypto (its sub-items live in §§2.58, 2.62)"),
    4535: ("OP-2.56-A", "Open", BS, "b_256a", "tags framework numbers, mostly physical claims, against a mathematical inventory"),
    4536: ("OP-2.56-B", "Open (lead: Partially open)", BS, "b_256b", "asks whether two values are physical parameters; a geometric address is active"),
    4537: ("OP-2.56-C", "Open", BM, None, "pure mathematics (5-fold / 7-fold register coupling)"),
    4538: ("OP-2.63", "Open", BS, "b_263", "a geometry question about the vacuum fold of §2.26"),
    # ---- Lower-priority
    4544: ("'Zero Free Parameters' string update", "Open", D, None, "an author action (drafted at V4.93; Step 4a)"),
    4545: ("§2.46 simulation rerun", "Open", A, "a", "the four-prime ladder's physical scale intersections"),
    4546: ("§2.47 6% gap derivation", "Open", A, "a", "the proton estimate (mass table)"),
    4547: ("§3.4 Bjerknes-action Lagrangian audit", "Open", A, "a", "Bjerknes action, named in C(a)"),
    4548: ("§3.4-G0", "Closed", OUT, None, "CLOSED (V4.26)"),
    4549: ("§3.4-MV-G1", "Closed", OUT, None, "CLOSED (V4.26)"),
    4550: ("§3.4-G1′", "Closed", OUT, None, "CLOSED (V4.26)"),
    4551: ("§3.4-G1″", "Closed", OUT, None, "CLOSED (V4.26)"),
    4552: ("§3.4-G2-orient", "Closed", OUT, None, "CLOSED (R1, V4.27)"),
    4553: ("§3.4-G2-Borromean", "Closed", OUT, None, "CLOSED (V4.27)"),
    4554: ("§3.4-G2-Milnor", "Closed", OUT, None, "CLOSED (V4.29; retraction V4.31 reversed V4.32)"),
    4555: ("§3.4-G2-Milnor-INT", "Partially executed (lead: PARTIAL)", BS, "b_milnor",
           "curve computations (R1) joined to a physical sign reading (R3)"),
    4556: ("§3.4-G2-knot", "Open", E, "e", "named in C(e)"),
    4557: ("§3.4-G2-CHIRAL", "Open (V4.31)", E, None,
           "named in C(e), but its cell records ✓ CLOSED (V4.32, §3.09), so no pointer; listed in the intake by reference (flagged)"),
    4558: ("§3.4-SIGNPHI", "Confirmed", OUT, None, "Consistency-CONFIRMED (V4.33)"),
    4559: ("§3.4-G1‴ / G4", "Open", A, "a", "Bjerknes pulsation = ζ"),
    4560: ("§2.51", "Reserved", OUT, None, "Reserved; no content assigned"),
    # ---- §2.73 – §2.E-QQ
    4566: ("§2.73 Gate A", "Open", BS, "b_273", "serves the R3 physical mapping; §2.73's algebra is R2"),
    4567: ("§2.73 Gate B", "Open", BS, "b_273", "serves the R3 physical mapping; §2.73's algebra is R2"),
    4568: ("§2.74 Part IV physical mapping", "Open (R3)", BS, "b_274map", "the R3 mapping of §2.74's R2 duality"),
    4569: ("§2.74 Part VI OQ1", "Closed", OUT, None, "CLOSED (V4.5)"),
    4570: ("§2.74 Part VI OQ2", "Open", BM, None, "pure mathematics"),
    4571: ("§2.74 Part VI OQ3", "Open", BM, None, "a bilinear-form question on the Császár/Szilassi duality"),
    4572: ("OP-2.74.1c", "Closed", OUT, None, "CLOSED in §2.76"),
    4573: ("OP-2.74.1a", "Open", BM, None, "pure mathematics"),
    4574: ("OP-2.74.1b", "Open", BS, "b_2741b", "its own words: a physical mapping of the YB orbits"),
    4575: ("OP-2.74.1c.i", "Open", BM, None, "pure mathematics; its cell records ANSWERED (V4.94)"),
    4576: ("OP-2.74.1c.ii", "Open", BM, None, "pure mathematics"),
    4577: ("OP-2.74.1c.iii", "Open", BM, None, "pure mathematics; its cell records ANSWERED (V4.94)"),
    4578: ("OP-2.78.1", "Closed", OUT, None, "CLOSED (V4.17)"),
    4579: ("OP-2.78.2", "Closed", OUT, None, "CLOSED (V4.17)"),
    4580: ("OP-2.78.3", "Open (lead: Open / redirect)", BM, None, "pure mathematics"),
    4581: ("OP-2.79.1", "Closed", OUT, None, "CLOSED (V4.17)"),
    4582: ("§2.58.B implementation", "Closed", OUT, None, "CLOSED (V4.17)"),
    4583: ("§3.1 ephemeral-distribution fix", "Open", C, None, "crypto-side"),
    4584: ("OP-2.58.1a harness port", "Open", C, None, "crypto-side"),
    4585: ("`_cd_conj` shared-tool convergence", "Closed", OUT, None, "CLOSED (V4.17)"),
    4586: ("OP-2.79.2", "Open", BM, None, "pure mathematics (an intertwiner question)"),
    4587: ("OP-2.75-CR", "Closed", OUT, None, "CLOSED-with-result (V4.6)"),
    4588: ("OP-2.77-σ4", "Closed", OUT, None, "CLOSED-with-result (V4.6)"),
    4589: ("OP-2.77-WD", "Closed", OUT, None, "CLOSED-with-negative-result (V4.7)"),
    4590: ("OP-2.77-FB", "Open", H, None, "a terminology audit across physics and mathematics entries; no rule fits it cleanly"),
    4591: ("OP-2.25.2 branch (a)", "Closed", OUT, None, "CLOSED-NEGATIVE (V4.18)"),
    4592: ("OP-2.25.2 branch (b)", "Open", A, "a", "the proton-radius route r_p/λ̄_p = 4"),
    4593: ("§2.82 Eddington flags", "Standing (lead: ACTIVE)", B4, None, "Eddington guards; the standard stays in force (§2.97.B.4)"),
    4594: ("OP-2.E-QQ.QQ1", "Closed", OUT, None, "SCOPE-CORRECTED (V4.14), re-classified R2-forced"),
    4595: ("OP-2.E-QQ.QQ2", "Open (re-opened V4.14)", BM, None, "pure mathematics"),
    4596: ("OP-2.E-QQ.QQ3", "Open (lead: OPEN in full)", A, "a", "the ferromagnetism carrier mapping"),
    4597: ("§2.E-QQ promotion gate to R2", "Open (re-opened V4.14)", BS, "b_eqq", "R2 representation theory joined to an R3 physical reading"),
    4598: ("OP-2.E-QQ.G1", "Closed", OUT, None, "CLOSED-POSITIVE (V4.14)"),
    4599: ("OP-2.E-QQ.E1", "Open", BS, "b_e1", "its own words: a physical interpretation of an algebraic pair"),
    4600: ("OP-2.E-QQ.E2", "Open", BM, None, "pure mathematics (bookkeeping)"),
    4601: ("Reframed Gate 1 Condition 1 (ferromagnetism)", "Refuted", OUT, None, "Structurally refuted (V4.6); Path B is the QQ3 row"),
    # ---- §2.85 / §2.86
    4607: ("μ_n spinor-promotion gate", "Open", A, "a", "μ_n, named in C(a)"),
    4608: ("Kernel-level S₄-invariance of U(L)", "Closed", OUT, None, "CLOSED (V4.21)"),
    4609: ("σ₄ restricted to 2O ↔ spin-3/2", "Open", BS, None, "its cell records CLOSED-POSITIVE (V4.22), so no pointer"),
    4610: ("§2.85 Condition 3", "Open", A, "a", "downstream of the μ_n gate"),
    4611: ("§2.86 v₀-independence flag", "Closed", OUT, None, "CLOSED-NEGATIVE (V4.21)"),
    4612: ("§2.86 'faces = Clifford'", "Closed", OUT, None, "CLOSED-NEGATIVE (V4.21)"),
    # ---- §2.87
    4618: ("Gate 2a", "Open", A, "a", "named in C(a); its dynamical clause is the open content"),
    4619: ("ℂ⊗𝕆 ↔ octonion-substrate dictionary", "Open", BS, "b_dict", "algebraic identifications joined to a substrate and particle map"),
    4620: ("Full Donnelly η-defect sum", "Open", BS, None, "the split is already recorded (V4.93: the purpose closed at V4.84; the η sum stays open)"),
    4621: ("ρ₈ orbifold is bosonic", "Recorded", OUT, None, "Recorded finding (V4.22)"),
    4622: ("Factor-assignment question", "Open", A, None, "its cell records CLOSED (V4.84), so no pointer"),
    4623: ("Soliton spin-isospin locking derivation", "Open", A, "a", "Gate 2a's dynamical target"),
    4624: ("Single-σ₄ unification fork", "Closed", OUT, None, "CLOSED-NEGATIVE (V4.24)"),
    # ---- OP-2a / §2.41.B
    4630: ("G-2a.2", "Closed", OUT, None, "CLOSED (V4.23)"),
    4631: ("G-2a.3", "Closed", OUT, None, "CLOSED-NEGATIVE (V4.23)"),
    4632: ("G-2a.4", "Closed", OUT, None, "CLOSED-NEGATIVE (V4.24)"),
    4633: ("A2 alpha-decay count gate", "Open", BS, "b_a2", "a count (mathematics) against an ejection mechanism (physics)"),
    4634: ("§2.41 / §2.53 rung-numbering reconciliation", "Open", BS, "b_rung", "numbering conventions joined to the electron-anchor placement"),
    4635: ("§2.41.A rung-4 deferral", "Open (residual piece)", BM, None, "pure mathematics (the squaring-map link)"),
    # ---- ζ-tax
    4641: ("ζ-tax gate 1", "Open", A, "a", "named in C(a)"),
    4642: ("ζ-tax gate 2", "Open", A, "a", "named in C(a)"),
    4643: ("ζ-tax gate 3", "Open", A, None, "its cell records CLOSED — FAILED as framed (V4.94), so no pointer"),
    4644: ("ζ-tax gate 4", "Open", A, "a", "named in C(a)"),
}

# ------------------------------------------------------------------ checks
by_line = {r["line"]: r for r in rows}
assert set(by_line) == set(M), ("mapping/table mismatch", sorted(set(by_line) ^ set(M)))
assert len(rows) == len(M) == 163

LEAD = {  # label class -> regex the lead status (first 160 chars, bold stripped) must match
    "Open": r"^(~~)?Open|OPEN", "Registered": r"^REGISTERED(,| \()", "Standing": r"^Standing", "Partially executed":
    r"PARTIALLY EXECUTED", "Closed": r"CLOSED|Rung-4", "Executed": r"EXECUTED", "Recorded": r"^(RECORDED|Recorded finding)",
    "Superseded": r"^(Split by|REFRAMED)", "Refuted": r"^Structurally refuted", "Reserved": r"^Reserved", "Confirmed":
    r"^Consistency-CONFIRMED",
}
SPECIAL = {4438: r"^ADVANCED", 4555: r"^PARTIAL \(", 4536: r"^Partially open", 4580: r"^Open / redirect", 4593: r"^ACTIVE",
           4595: r"RETRACTED as a finding.*Re-opened", 4596: r"OPEN in full", 4597: r"RE-OPENED", 4635: r"residual open piece",
           4594: r"SCOPE-CORRECTED", 4568: r"^Open R3"}
bad = []
for n, (name, label, rule, ptr, note) in M.items():
    lead = re.sub(r"\*\*", "", by_line[n]["status"])
    cls = label.split(" (")[0]
    pat = SPECIAL.get(n, LEAD[cls])
    if not re.search(pat, lead[:900] if n in SPECIAL else lead[:160]):
        bad.append((n, label, lead[:80]))
    if rule == OUT:
        assert cls not in ("Open", "Registered", "Standing", "Partially executed"), n
    else:
        assert cls in ("Open", "Registered", "Standing", "Partially executed"), n
    assert (ptr is None) or rule in (A, BS, E), n
assert not bad, bad

inscope = {n: v for n, v in M.items() if v[2] != OUT}
tally = {}
for n, v in inscope.items():
    key = v[2] + (" + pointer" if v[3] else "")
    tally[key] = tally.get(key, 0) + 1
n_ptr = sum(1 for v in inscope.values() if v[3])
counts = {"table rows": len(rows), "in scope": len(inscope), "out of scope": len(M) - len(inscope),
          "pointers": n_ptr, "closed/dropped bullets (all out of scope)": len(bullets)}
assert counts["in scope"] + counts["out of scope"] == 163
for r in (A, BS, BM, C, D, E, F, H, B4):
    pass
print(json.dumps(counts, ensure_ascii=False))
print(json.dumps(dict(sorted(tally.items())), ensure_ascii=False))

# ------------------------------------------------------------------ outputs
OUTJ = "/home/claude/gifgaf0.github.io/audit_followup/closeout/co1_classification.json"
json.dump({"base": SRC, "base_md5": MD5, "counts": counts, "tally": tally,
           "rows": [{"line": n, "section": by_line[n]["section"], "name": M[n][0], "label": M[n][1], "rule": M[n][2],
                     "pointer": M[n][3], "note": M[n][4], "task_head": by_line[n]["task"][:160]} for n in sorted(M)],
           "closed_bullets": [{"line": n, "text": L[n - 1][:160]} for n in bullets]},
          open(OUTJ, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote", OUTJ)

# ------------------------------------------------------------------ the report
SEC_SHORT = {
    "High-priority structural gates": "High-priority",
    "Cryptographic thread open problems": "Crypto",
    "Sedenion / Fano-line structure open problems": "Sedenion",
    "Capacity / statistics open problems (§2.67 / §2.68 thread)": "Capacity",
    "Geometric / combinatorial open problems": "Geometric",
    "Lower-priority items": "Lower-priority",
    "§2.73 / §2.74 / §2.75 / §2.76 / §2.77 / §2.E-WD / §2.E-QQ open items (added V4.3 / V4.4 / V4.5 / V4.6 / V4.7)": "§2.73–§2.E-QQ",
    "§2.85 / §2.86 open items (added V4.21)": "§2.85/§2.86",
    "§2.87 open items (added V4.22)": "§2.87",
    "OP-2a / §2.41.B open items (added V4.23)": "OP-2a",
    "ζ-tax unified picture promotion gates (banked entry; V4.4)": "ζ-tax",
}
RULE_WORDS = {A: "(a) closed with the program", BS: "(b) split: mapping closes, mathematics stays open",
              BM: "(b) mathematics, stays open", C: "(c) crypto, outside the closure", D: "(d) author action, open until done",
              E: "(e) successor intake, not closed", F: "(f) §2.52 Open 3, freeze honoured", H: "(h) unclassified: for the author",
              B4: "§2.97.B.4 standing method"}
out = []
w = out.append
w("# CO-1: Part VI rows classified under §2.97.C (V4.96 base)")
w("")
w("**Plain-language summary.** The close-out brief asks for every open item in the ledger's task list (Part VI) to be sorted by "
  "the closing entry's rules before V4.97 is folded. Part VI has 163 table rows:")
w(f"- **{counts['in scope']} are in scope**, because their status reads Open, Registered, Standing or Partially executed. Each "
  "has exactly one rule below.")
w(f"- **{counts['out of scope']} are out of scope**, because they are already closed, executed, recorded, superseded, refuted or "
  "reserved. They are listed at the end, so the count can be checked.")
w(f"- **{n_ptr} rows get a V4.97 pointer:** {tally.get(A + ' + pointer', 0)} closed with the program, "
  f"{tally.get(BS + ' + pointer', 0)} split (the physical reading closes, the mathematics stays open) and "
  f"{tally.get(E + ' + pointer', 0)} sent to the successor intake.")
w(f"- **{tally.get(H, 0)} rows could not be classified** and are left for the author: OP-C7-1 and OP-2.77-FB.")
w("")
w("Nothing here changes the ledger. The fold (V4.97) applies it. The 17 bullets of Part VI's \"Closed / dropped\" list are all "
  "out of scope; two of them repeat re-openings that are tracked by table rows below (QQ2 and the §2.E-QQ promotion gate).")
w("")
w("## How the scope and the pointers were decided")
w("")
w("- **Scope.** A row is in scope when the status written first in its cell is Open, Registered, Standing or Partially "
  "executed (the brief's words). Some cells use other words, read as follows:")
w("  - ADVANCED (§2.53) and PARTIAL (§3.4-G2-Milnor-INT) as Partially executed;")
w("  - Partially open, Open / redirect, Open R3, OPEN in full, Re-opened and the rung-4 \"residual open piece\" as Open;")
w("  - ACTIVE (the §2.82 Eddington flags) as Standing.")
w("- **Pointers.** A pointer goes on each in-scope row closed by (a), split by (b) or sent on by (e). There are three exceptions:")
w("  - Rows whose own cell already records CLOSED, ANSWERED or ELECTED get none, since the brief says no pointer on rows "
  "already closed. These are G-POLY1, the polycrystal floor, §3.4-G2-CHIRAL, σ₄ restricted to 2O ↔ spin-3/2, the factor-assignment "
  "question and ζ-tax gate 3.")
w("  - A gate whose cell records EXECUTED or DECLARED, under a status that still reads Open or Registered, does get one. "
  "§2.97.C(a) names four such gates: G-ζ1, G-κ1, G-IIB-L1 and G-CC-ε1. The same holds for the M.ONT gate and G-SCALE1.")
w("  - The Donnelly η row was already split at V4.93, so it gets no new pointer.")
w("- **(b), split or not.** \"(b) mathematics\" rows are pure mathematics and stay open with no pointer. \"(b) split\" rows join "
  "a mathematical question to a physical reading: the reading closes and the mathematics stays open.")
w("")
w("## In scope: the classification table")
w("")
w("| V4.96 line | Part VI section | Row | Status class | Rule | Pointer | Why |")
w("|---|---|---|---|---|---|---|")
for n in sorted(inscope):
    name, label, rule, ptr, note = M[n]
    w(f"| {n} | {SEC_SHORT[by_line[n]['section']]} | {name.replace('|', '¦')} | {label} | {rule} | {'yes' if ptr else 'no'} | "
      f"{note.replace('|', '¦')} |")
w("")
w("## Tally")
w("")
w("| Rule | Rows | With pointer |")
w("|---|---|---|")
for r in (A, BS, BM, C, D, E, F, H, B4):
    tot = sum(1 for v in inscope.values() if v[2] == r)
    wp = sum(1 for v in inscope.values() if v[2] == r and v[3])
    w(f"| {RULE_WORDS[r]} | {tot} | {wp} |")
w(f"| **Total in scope** | **{len(inscope)}** | **{n_ptr}** |")
w("")
w("## Not classified: for the author (rule (h))")
w("")
w("- **OP-C7-1** (\"category-mismatch metric; would close §2.7 Open Problem 3\", V4.96 line 4531). §2.7 is substrate physics "
  "(the meson-to-baryon ratio and the energy per edge). The ledger nowhere defines its \"Open Problem 3\", and the metric "
  "itself is a method question, so it could be read as either (a) or (b). No pointer was added.")
w("- **OP-2.77-FB** (the framework-wide terminology audit, line 4590). It would reword physics language (\"spinor doublet\", "
  "Dirac structure) wherever the ledger applies it to σ₄, which is a mathematical object. That is hygiene for the mathematics "
  "that carries forward, so the likely reading is (b), stays open. No rule names it. No pointer was added.")
w("")
w("## Readings to confirm")
w("")
w("- **§2.53 bilateral fold from §3.4** (line 4438). Its status reads ADVANCED, which I read as Partially executed. It is closed "
  "by (a): what is open there is the substrate import (I1–I3), and the cell's R1 parts are results, not open questions.")
w("- **§2.97.C(a) names G-POLY1**, but its row records CLOSED: GATE COMPLETE (V4.76), so it has no pointer.")
w("- **§2.97.C(e) names §3.4-G2-CHIRAL**, but its row records ✓ CLOSED (V4.32, §3.09).")
w("  - It is curve-level Milnor-invariant work on idealized curves, not Faddeev–Hopf soliton work.")
w("  - The Faddeev–Hopf rows are §3.4-G2-orient (closed, R1) and §3.4-G2-knot (open).")
w("  - It is listed in the intake by reference, with no pointer.")
w("- **§2.97.C(e) also names two items that are not open rows.** G-QUANTA's row is CLOSED (V4.82), and §2.84 Part C is a "
  "Part II section, not a row. Both are listed in the intake by reference.")
w("- **Two Standing rows are settled by §2.97.B.4, not by a C rule:** OP-2.67.6 (the statistics-from-geometry gates) and the "
  "§2.82 Eddington flags. Both stay standing, with no pointer.")
w("- **OP-2.58.4** sits in the crypto thread but calls itself \"a physics-crypto connection\". It is left untouched under (c).")
w("")
w("## Out of scope (already closed, executed, recorded, superseded, refuted or reserved)")
w("")
w("| V4.96 line | Row | Status |")
w("|---|---|---|")
for n in sorted(set(M) - set(inscope)):
    w(f"| {n} | {M[n][0].replace('|', '¦')} | {M[n][4].replace('|', '¦')} |")
w("")
w("## Count check")
w("")
w(f"- Table rows parsed from V4.96 Part VI (md5 `{MD5}`): **{len(rows)}**. Mapping entries: **{len(M)}**. They are the same set, "
  "so every row appears exactly once.")
w(f"- In scope **{len(inscope)}** + out of scope **{len(M) - len(inscope)}** = **{len(M)}**.")
w("- Every row's first status words were machine-checked against its recorded status class.")
w(f"- The \"Closed / dropped\" bullets: **{len(bullets)}**, all out of scope.")
w("")
w("Source: `co1_classify.py` (this table, `co1_classification.json`).")
OUTM = "/home/claude/gifgaf0.github.io/audit_followup/closeout/CO1_CLASSIFICATION.md"
open(OUTM, "w", encoding="utf-8").write("\n".join(out) + "\n")
print("wrote", OUTM)
