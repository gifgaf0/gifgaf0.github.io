#!/usr/bin/env python3
# Fold-in splice: SQT Master Ledger V4.46 -> V4.47
# Gate G-INT1 (internal octonion-sector channel) -> STRUCTURAL-ONLY, as §2.88.D.2 + one Part VI row.
# All edits are additive / append-only. Verification: per-anchor uniqueness, md5 byte-reconstruction
# back to V4.46, and an explicit §2.52 Open 3 row byte-identical assertion (frozen-row guard).

import hashlib

SRC = "v4_46.md"
OUT = "/mnt/user-data/outputs/SQT_Master_Ledger_v4_47_CANONICAL.md"

with open(SRC, encoding="utf-8") as f:
    orig = f.read()
text = orig

# ---------------------------------------------------------------------------
# Edit 0 — H1 title (INTRA-LINE: version bump to V4.47; also corrects the stale "V4.45"
# title the V4.46 fold left unbumped — cf. the V4.40 fold correcting the stale "V4.38" title)
# ---------------------------------------------------------------------------
A0_old = "# SQT Master Ledger — V4.45 Canonical"
A0_new = "# SQT Master Ledger — V4.47 Canonical"

# ---------------------------------------------------------------------------
# Edit 1 — As-of header (INTRA-LINE: version bump V4.46->V4.47, date bump, prepend V4.47 summary)
# ---------------------------------------------------------------------------
A1_old = "**As of:** June 23, 2026 (V4.46 fold — **Two items"
A1_new = (
    "**As of:** June 28, 2026 (V4.47 fold — **One gate executed, one version bump — Gate G-INT1 "
    "EXECUTED (the internal octonion-sector channel of the instantiated substrate; successor to G-ζ1's "
    "density channel, §2.88.D.1), verdict STRUCTURAL-ONLY, folded as §2.88.D.2 + one Part VI row.** The "
    "internal sector carries a gapped, Fano-selective fluctuation channel but no import-free dynamical "
    "number. **R1:** the two-body internal sector is gapless — a theorem (L_⊥ψ₀ = 0 is the stationary GP "
    "equation, ψ₀ the exact internal zero mode); the oriented three-body term gaps/splits an internal mode "
    "**iff** the core winding is a Fano line (φ_abc = 0 off a line; the symmetric three-body term inert) — "
    "**extending the §3.4.4/§3.4.5 selection-rule ladder from the static charge Q_φ to the dynamical "
    "fluctuation spectrum**; 7 = 1⊕3⊕3̄ under F₂₁ (standard rep theory, classification only — prior-art "
    "flagged); the lifted subspace is a chiral pair ({0,±iσ}, count + chirality profile-independent). "
    "**Class-b:** σ = ‖φ|_line‖·λ·(profile), ‖φ|_line‖ = √3 (the structure-constant norm on a Fano line — "
    "NOT a representation number, NOT the p6m lattice √3), ∝ λ and μ-drifting — no λ-canceling pure number "
    "⇒ the breach arm does not fire; **λ (the oriented three-body coupling) is the located import of the "
    "internal channel.** **Cluster scope (corrected on fold):** G-INT1 characterizes the internal channel "
    "only; **§2.53/§2.64 are density-sector** and their import is the density-sector roton/healing-length "
    "import — a distinct import still **open (not located, not examined — G-ζ1 *used* the roton profile, "
    "did not derive it; the angle-3 ξ_vac/a-forcing test is unexecuted)**; so G-INT1 **eliminates the "
    "internal channel as a breach route**, §2.53/§2.64 stay on the density-sector import (angle-3 unrun), "
    "two channels examined / two distinct imports, **M.BRIDGE strengthened**; no claim that G-INT1 resolves "
    "the §2.53/§2.64 import. **Two-leg verified** (CC 41c6bb9 + independent second leg "
    "`verify_gint1_secondleg.py`: φ on the 7 Fano lines, 1⊕3⊕3̄, line eigenstructure {0,±i√3}, non-line "
    "inert). **Scope (honest):** Steps 1–2 in full; the structural verdicts are symmetry-determined / "
    "profile-independent (demonstrated on a representative core overlap); the full relaxed-N=160 "
    "7-component defect-core BdG eigenproblem was NOT performed and is NOT load-bearing (it would only pin "
    "the class-b σ magnitude — the M.CW not-worth-pursuing pattern), filed as optional low-priority "
    "R2-firming with the Gate-2a (§2.87.A) trigger flagged. **See-also (cross-ref only):** 3/3̄ = the "
    "QR/QNR split (the i√7 Gauss sum of 7th roots over the residue cosets) → §2.75/§2.76, §3.4.6. **No "
    "§3.x; no register change to anything prior; no observable bridge (M.BRIDGE intact, strengthened).** "
    "**Append-only:** this summary prepended + the V4.47 record at the top of the recent fold-in block "
    "(before V4.46); §2.88.D.2 after §2.88.D.1 (before §2.88.E); one Part VI row (after G-ζ1, before the "
    "M.ONT gate row); the title/As-of bump; one changelog line; nothing prior modified; the §2.52 Open 3 "
    "row untouched per standing instruction. Full V4.47 record below. V4.46 fold — **Two items"
)

# ---------------------------------------------------------------------------
# Edit 2 — V4.47 fold-in record (INSERT at top of recent fold-in block, before the V4.46 record)
# ---------------------------------------------------------------------------
A2_anchor = "**V4.46 fold-in record (June 23, 2026):** Two items, one version bump"
V47_RECORD = (
    "**V4.47 fold-in record (June 28, 2026):** One gate executed, one version bump — **Gate G-INT1 "
    "EXECUTED** (the internal octonion-sector channel of the instantiated substrate, V4.26 §3.4-SYM / the "
    "I1–I3 ticket; the successor to G-ζ1's density channel, §2.88.D.1), verdict **STRUCTURAL-ONLY** — the "
    "registered, a-priori-expected arm. Folded as **§2.88.D.2** under the G-ζ1 umbrella (after §2.88.D.1, "
    "before §2.88.E) + one Part VI row; **no body §2.x beyond §2.88.D.2, no §3.x, no register change to "
    "anything prior.** **Result.** The internal sector carries a gapped, **Fano-selective** fluctuation "
    "channel but **no import-free dynamical number**: *(R1)* the two-body internal sector is gapless — a "
    "theorem (the symmetric two-body kernel is Schur-forced to a single scalar K_ij = a(r)δ_ij per §3.4.4, "
    "so the interaction sees only ρ = |ψ|² and is accidentally O(16)-symmetric; the transverse operator "
    "L_⊥ = −½∇² + (U*ρ − μ) satisfies L_⊥ψ₀ = 0, the stationary GP equation, so ψ₀ is the exact internal "
    "zero mode — no framework content at two-body order, consistent with §3.4.4's vacuum locality); the "
    "oriented three-body term gaps/splits an internal mode **iff** the core winding directions form a Fano "
    "line (its coherent self-coupling on the winding triple is φ_abc, ±1 on a line and identically 0 off "
    "it; the symmetric three-body term is inert) — a binary that depends only on whether the structure "
    "constant vanishes, **extending the §3.4.4/§3.4.5 selection-rule ladder from the static charge Q_φ to "
    "the dynamical fluctuation spectrum** (§3.4.5 established it for the static linking charge only); the "
    "seven internal directions split **7 = 1 ⊕ 3 ⊕ 3̄** under the realized F₂₁ ⊂ G₂ (rank-3 transitive "
    "action, element orders {1:1, 3:14, 7:6}, character) — standard G₂/F₂₁ representation theory used to "
    "*classify* the channel, **not a novel claim** (prior-art discipline); the lifted subspace is a "
    "**chiral pair** (the oriented coupling is totally antisymmetric on the 3-element line, and any "
    "antisymmetric 3×3 has eigenstructure {0, ±iσ}, so the count = 2 and the ± chirality are "
    "profile-independent). *(class-b)* the splitting magnitude is σ = ‖φ|_line‖·λ·(profile integral), with "
    "**‖φ|_line‖ = √3** (the norm of the structure constants on a Fano line — relabeled from a chat-side "
    "draft's loose 'representation number', and explicitly NOT the p6m lattice √3); σ ∝ λ and μ-drifts, "
    "carrying no λ-canceling pure number — the registered a-priori expectation — so **the breach arm (a "
    "geometry-protected dimensionless dynamical quantity) does not fire, and λ (the oriented three-body "
    "coupling) is the located import of the internal channel.** **Cluster scope (corrected on fold — the "
    "load-bearing point).** G-INT1 characterizes the *internal* channel only. **§2.53 (fold convexity "
    "sign) and §2.64 (C = ξ_vac/a) are density-sector quantities**, and their import is the "
    "**density-sector roton/healing-length** import — a *distinct* import, still **open: not located, not "
    "examined** (G-ζ1 *used* the roton profile as an I1–I3 import; it did not derive it; the angle-3 "
    "ξ_vac/a-forcing test is **unexecuted**). So the cluster reads: G-INT1 **eliminates the internal "
    "channel as a breach route**; §2.53/§2.64 remain bottomed on the density-sector roton import, the live "
    "frontier with angle-3 unrun; §2.52 Open 3 frozen. **Two channels examined (density via G-ζ1, internal "
    "via G-INT1), two distinct imports — M.BRIDGE strengthened.** This fold does **not** claim G-INT1 "
    "resolves the §2.53/§2.64 import. **Two-leg verified:** first leg CC `41c6bb9` (built on `gz1_core.py`, "
    "the §2.88.D.1 instrument); independent second leg `verify_gint1_secondleg.py` (from-scratch "
    "octonion/F₂₁/eigenvalue build, importing no tool under test) — both reproduce φ supported on exactly "
    "the 7 Fano lines, 1⊕3⊕3̄, the line-core eigenstructure {0, ±i√3}, and the non-line core inert "
    "(‖coupling‖ = 0). **Scope (honest, carried from the audit):** Steps 1–2 (crystallization, two-body "
    "control) executed in full; the structural verdicts are symmetry-determined and profile-independent, "
    "demonstrated on a representative core overlap; the full relaxed-N=160 7-component defect-core BdG "
    "eigenproblem was **not** performed and is **not load-bearing** (it would only pin the σ magnitude, "
    "class-b regardless — spending the heavy solve to fix an import is the M.CW 'not worth pursuing' "
    "pattern), **filed as optional low-priority R2-firming**, with the **Gate-2a (§2.87.A spin-isospin "
    "locking)** trigger flagged for if/when the explicit chiral-mode structure on the core is needed; the "
    "error-prone oriented-second-variation touches only σ, while the 2-chiral count rests on φ's "
    "antisymmetry, which is exact. **See-also (cross-ref, not a claim):** the 3/3̄ split is the **QR/QNR "
    "split** (the i√7 Gauss sum of 7th roots over the residue cosets), threading to §2.75/§2.76 and the "
    "§3.4.6 sign(φ)↔QR/QNR map. **No observable bridge — M.BRIDGE intact and strengthened.** The Paper II "
    "§3.4.5 ladder-extension paragraph (the selection rule carried onto the fluctuation spectrum) is a "
    "queued paper-side companion (Paper II §3.4, **not** ledger §3.x), to be appended separately. "
    "**Provenance:** `G_INT1_EXECUTION_PREREGISTRATION.md` (pre-compute), CC `41c6bb9` (first leg), "
    "`verify_gint1_secondleg.py` (independent second leg), CC `5c1d98d` (verdict incorporation + the three "
    "audit corrections: 2-chiral→R1, √3 relabel, scope de-laundered), CC `21be734` (the density-import "
    "'examined→open' precision fix). **Append-only:** the V4.47 fold-in summary prepended within the As-of "
    "header (date June 23 → June 28, 2026); this record at the top of the recent fold-in block (before the "
    "V4.46 record); **§2.88.D.2** appended after §2.88.D.1 (before §2.88.E); **one Part VI row** (G-INT1 "
    "EXECUTED / STRUCTURAL-ONLY, after the G-ζ1 row, before the M.ONT gate row); the title/As-of header "
    "bump; one changelog line; **nothing prior modified; the §2.52 Open 3 row untouched per standing "
    "instruction.** This continues the V4.14+ pattern: a pre-registered gate executed exactly as "
    "registered, the bankable R1 structural content (the selection-rule ladder extended to the fluctuation "
    "spectrum) folded and the dynamical magnitude held at class-b with λ named as the import, two-leg "
    "verified, and the cluster scope corrected so a channel result is not laundered into a resolution of "
    "the density-sector gates.\n\n"
)
A2_new = V47_RECORD + A2_anchor

# ---------------------------------------------------------------------------
# Edit 3 — §2.88.D.2 entry (INSERT after §2.88.D.1 content, before the §2.88.E heading)
# ---------------------------------------------------------------------------
A3_anchor = "#### §2.88.E — Import and Consistency Accounting"
D2_ENTRY = (
    "#### §2.88.D.2 — Gate G-INT1 EXECUTED (V4.47, June 28, 2026): STRUCTURAL-ONLY — the Internal Octonion "
    "Channel Carries No Import-Free Dynamical Number; λ Located as Its Import\n\n"
    "**Sibling of §2.88.D.1.** G-ζ1 tested the *density* channel of the instantiated substrate (the I1–I3 "
    "ticket) for a per-layer attenuation and returned DEGENERATE/INFORMATIVE-FAIL; G-INT1 is the successor "
    "for the *internal octonion* channel. **Register:** the structural results (the gapless two-body "
    "theorem; S_Fano selectivity; the 1⊕3⊕3̄ multiplet; the 2-chiral count + chirality) → **R1**; the "
    "verdict (STRUCTURAL-ONLY — internal channel eliminated as a breach route, λ the located import) → "
    "**R2**, import-contingent. **Provenance:** pre-registration `G_INT1_EXECUTION_PREREGISTRATION.md` "
    "(before compute); first leg CC `41c6bb9` (built on `gz1_core.py`); independent second leg "
    "`verify_gint1_secondleg.py` (from-scratch octonion/F₂₁/eigenvalue build, no tool under test). "
    "**Two-leg verified.**\n\n"
    "**Scope and freeze (binding).** Substrate-instantiation work serving §2.53 / §2.64; **§2.52 Open 3 "
    "frozen and untouched** (standing instruction) — no target loaded, the comparison step never reached "
    "(no breach arm fired). The result characterizes one *channel* of the shared substrate; it does **not** "
    "advance, annotate, or touch the §2.52 row.\n\n"
    "**What the gate found.** *(1) Two-body internal sector gapless — a theorem (R1).* The symmetric "
    "two-body kernel is Schur-forced to a single scalar K_ij = a(r)δ_ij (§3.4.4), so the interaction sees "
    "only ρ = |ψ|² and is accidentally O(16)-symmetric; the transverse BdG operator is L_⊥ = −½∇² + "
    "(U*ρ − μ), and **L_⊥ψ₀ = 0 is the stationary GP equation itself**, so ψ₀ is an exact internal zero "
    "mode — the internal sector is gapless at Γ, roton-free, with no framework content at two-body order "
    "(consistent with §3.4.4's vacuum-locality result; a gap here would have been a bug, not a pass). "
    "*(2) S_Fano selective (R1, profile-independent).* A gapped/split internal mode appears around a "
    "defect core **iff** the core winding directions form a Fano line: the oriented three-body term's "
    "coherent self-coupling on the winding triple is φ_abc, which is ±1 on a Fano line and **identically 0 "
    "off it** (the symmetric three-body term is inert, §3.4.4) — a binary that depends only on whether the "
    "structure constant vanishes, not on the radial profile. This **extends the §3.4.4/§3.4.5 "
    "selection-rule ladder from the static charge Q_φ to the dynamical fluctuation spectrum** — the gate's "
    "R1 structural contribution; §3.4.5 established the rule for the static linking charge only. Verified "
    "on a Fano-line core {e₁,e₂,e₄} (modes lifted) vs a non-line control {e₁,e₂,e₃} (inert, ‖coupling‖ = "
    "0). *(3) Multiplet 1⊕3⊕3̄ (R1, classification).* The seven internal directions split as **7 = 1 ⊕ 3 ⊕ "
    "3̄** under the realized F₂₁ ⊂ G₂ (rank-3 transitive action; element orders {1:1, 3:14, 7:6}; "
    "character) — standard G₂/F₂₁ representation theory, used to *classify* the channel, **not a novel "
    "claim** (prior-art discipline; the framework-specific content is the ladder extension, not the group "
    "theory). *(4) 2 chiral modes (R1, forced).* On a Fano-line core the lifted subspace is a **chiral "
    "pair** (eigenvalues {0, ±iσ}): the oriented coupling is totally antisymmetric on the 3-element line, "
    "and any antisymmetric 3×3 has this eigenstructure, so the count (2) and the ± chirality are "
    "profile-independent. *(5) Breach test: class-(b) (R2).* The splitting *magnitude* is σ = "
    "‖φ|_line‖·λ·(profile integral), with **‖φ|_line‖ = √3** (the norm of the structure constants on a "
    "Fano line — NOT a representation number, and NOT the p6m lattice √3); σ ∝ λ and μ-drifts, so it "
    "carries **no λ-canceling pure number** — the registered a-priori expectation. **The breach arm (a "
    "geometry-protected dimensionless dynamical quantity) does not fire.**\n\n"
    "**Verdict (per the pre-registered arms): STRUCTURAL-ONLY** (the registered, a-priori-expected arm). "
    "The internal octonion sector carries a gapped, Fano-selective fluctuation channel but **no "
    "import-free dynamical number**; **λ (the oriented three-body coupling) is the located import of this "
    "channel.**\n\n"
    "**Cluster status (corrected — the load-bearing scope point).** G-INT1 characterizes the *internal* "
    "channel. **§2.53 (fold convexity sign) and §2.64 (C = ξ_vac/a) are density-sector quantities**, and "
    "their import is the **density-sector roton/healing-length** import — a *different* import, and one "
    "still **open: not located, not examined** (G-ζ1 *used* the roton profile as an I1–I3 import; it did "
    "not derive it; the angle-3 ξ_vac/a-forcing test is **unexecuted**). So the cluster reads: G-INT1 "
    "**eliminates the internal channel as a breach route**; §2.53 / §2.64 remain bottomed on the "
    "density-sector roton import, the live frontier with angle-3 unrun; §2.52 Open 3 frozen. **Two channels "
    "examined (density via G-ζ1, internal via G-INT1), two distinct imports** — M.BRIDGE strengthened (each "
    "channel needs its own import). This entry does **not** claim G-INT1 resolves the §2.53/§2.64 "
    "import.\n\n"
    "**Scope (honest, carried from the audit).** Steps 1–2 (crystallization, two-body control) executed in "
    "full; the structural verdicts (S_Fano, multiplet, 2-chiral count) are **symmetry-determined and "
    "profile-independent**, demonstrated on a representative core overlap — the full relaxed-N=160 "
    "7-component defect-core BdG eigenproblem was **not** performed, and is **not load-bearing**: it would "
    "only pin the σ magnitude, which is class-(b) regardless (spending the heavy solve to fix an import is "
    "the M.CW 'not worth pursuing' pattern, cf. the '100' search). **Filed as optional low-priority "
    "R2-firming**, with the **Gate-2a (§2.87.A spin-isospin locking)** trigger flagged for if/when the "
    "explicit chiral-mode structure on the core is needed. The error-prone oriented-second-variation "
    "touches only σ; the 2-chiral count rests on φ's antisymmetry, which is exact.\n\n"
    "**See-also (cross-ref, not a claim).** The 3/3̄ split is the **QR/QNR split** (the i√7 Gauss sum of "
    "7th roots over the residue cosets), threading to §2.75/§2.76 and the §3.4.6 sign(φ)↔QR/QNR map.\n\n"
    "**Eddington/discipline.** No ledger value loaded; λ never tuned; the full internal spectrum reported. "
    "§2.52 Open 3 untouched and frozen; nothing promoted to physical R1; M.BRIDGE intact and "
    "strengthened.\n\n"
)
A3_new = D2_ENTRY + A3_anchor

# ---------------------------------------------------------------------------
# Edit 4 — Part VI row for G-INT1 (INSERT after the G-ζ1 row, before the M.ONT gate row)
# ---------------------------------------------------------------------------
A4_anchor = "| **M.ONT gate** (declare the canonical particle ontology"
GINT1_ROW = (
    "| **G-INT1** (internal octonion-sector channel of the instantiated substrate: BdG fluctuation "
    "spectrum around a Fano-line defect core with the oriented three-body term active; I1–I3 ticket + the "
    "§3.4.4 octonion structure; the successor to G-ζ1's density channel; pre-registered arms "
    "STRUCTURAL-ONLY / GAPPED-SCALE-FREE (breach) / DEGENERATE) | **EXECUTED V4.47 (June 28, 2026), "
    "outcome block §2.88.D.2: verdict STRUCTURAL-ONLY** (the registered, a-priori-expected arm). The "
    "internal sector carries a gapped, **Fano-selective** fluctuation channel but **no import-free "
    "dynamical number**. **R1:** the two-body internal sector is gapless (a theorem — L_⊥ψ₀ = 0, the "
    "stationary GP equation; ψ₀ the exact internal zero mode); the oriented three-body term gaps/splits an "
    "internal mode **iff** the core winding is a Fano line (φ_abc = 0 off a line; the symmetric three-body "
    "term inert) — **extending the §3.4.4/§3.4.5 selection-rule ladder from the static charge Q_φ to the "
    "dynamical fluctuation spectrum**; 7 = 1⊕3⊕3̄ under F₂₁ (rep-theory classification, prior-art "
    "flagged); the lifted subspace a chiral pair ({0, ±iσ}, count + chirality profile-independent). "
    "**Class-b:** σ = ‖φ|_line‖·λ·(profile), ‖φ|_line‖ = √3 (the structure-constant norm on a Fano line — "
    "not a representation number, not the p6m √3), ∝ λ and μ-drifting — no λ-canceling pure number ⇒ "
    "**breach arm does not fire; λ the located import of the internal channel.** **Cluster scope:** G-INT1 "
    "eliminates the internal channel as a breach route; **§2.53/§2.64 are density-sector and remain on the "
    "density roton/healing-length import — distinct, still open (angle-3 unrun; G-ζ1 used the roton "
    "profile, did not derive it)**; two channels examined, two distinct imports; M.BRIDGE strengthened; no "
    "claim that G-INT1 resolves the §2.53/§2.64 import. **Two-leg verified** (CC `41c6bb9` + independent "
    "second leg `verify_gint1_secondleg.py`). **Scope:** the full relaxed-N=160 7-component defect-core "
    "BdG NOT performed, not load-bearing (would only pin the class-b σ magnitude); filed optional "
    "R2-firming, Gate-2a (§2.87.A) trigger flagged. The §2.52 Open 3 row untouched per standing "
    "instruction. Provenance `G_INT1_EXECUTION_PREREGISTRATION.md`, `verify_gint1_secondleg.py`. |\n"
)
A4_new = GINT1_ROW + A4_anchor

# ---------------------------------------------------------------------------
# Edit 5 — changelog tail line for V4.47 (APPEND after the V4.45 changelog line)
# (V4.46 added no changelog line — its own omission; not backfilled per append-only.)
# ---------------------------------------------------------------------------
A5_anchor = (
    "*V4.45 (June 18, 2026): additions only — title/As-of header bump (V4.44 → V4.45; date June 18 "
    "retained), the V4.45 fold-in summary prepended within the accumulated As-of header and the full V4.45 "
    "record inserted at the top of the recent fold-in block (before V4.42), one Part V banked row (the R1 "
    "OP-PSL.3 finiteness obstruction), one additive cross-dialect refinement to the Literature-Search-First "
    "rule (before Part I), one provenance file (`psl2p_gelfand_finiteness_check.py`) + the closure memo "
    "registered; OP-PSL.3 closed as a tracked open direction (no §3.x; no body §2.x; no register change). "
    "Prior-art closure analogous to V4.42; one fresh R1 banked.*"
)
V47_CHANGELOG = (
    "\n\n*V4.47 (June 28, 2026): additions only — As-of header bump (V4.46 → V4.47, date June 23 → "
    "June 28) and H1 title bump (V4.45 → V4.47, correcting the stale title the V4.46 fold left unbumped — "
    "cf. the V4.40 fold correcting the stale V4.38 title), the V4.47 fold-in summary prepended within the "
    "accumulated As-of header and the full V4.47 record at the top of the recent fold-in block (before "
    "V4.46), §2.88.D.2 (Gate G-INT1 EXECUTED — "
    "STRUCTURAL-ONLY; the internal octonion-sector channel) after §2.88.D.1 (before §2.88.E), one Part VI "
    "row (G-INT1, after the G-ζ1 row, before the M.ONT gate row), and this line. (V4.46 added no changelog "
    "line — its own omission; not backfilled per append-only.) No prior body content modified; no §3.x; no "
    "register change to anything prior (the internal-channel structural results are new R1, the verdict R2; "
    "the §2.53/§2.64 density-sector import is left open — not resolved by this channel result); two-leg "
    "verified (CC 41c6bb9 + independent second leg); M.BRIDGE intact and strengthened; the §2.52 Open 3 row "
    "untouched per standing instruction.*"
)
A5_new = A5_anchor + V47_CHANGELOG

# ---------------------------------------------------------------------------
EDITS = [
    ("H1 title (V4.45 -> V4.47; stale-title correction)", A0_old,   A0_new),
    ("As-of header (V4.47 summary + version/date bump)", A1_old,    A1_new),
    ("V4.47 fold-in record (top of block)",              A2_anchor, A2_new),
    ("§2.88.D.2 entry (after D.1, before E)",            A3_anchor, A3_new),
    ("Part VI G-INT1 row (after G-ζ1, before M.ONT)",    A4_anchor, A4_new),
    ("changelog V4.47 line (after V4.45)",               A5_anchor, A5_new),
]

# ---- apply (each anchor must be present exactly once at apply time) ----
print("=== applying edits ===")
for label, old, new in EDITS:
    n = text.count(old)
    assert n == 1, f"[{label}] anchor count {n} != 1"
    assert old != new, f"[{label}] no-op edit"
    text = text.replace(old, new, 1)
    print(f"  applied: {label}")

# ---- byte-reconstruction: reverse every insertion, must equal the original V4.46 ----
recon = text
for label, old, new in reversed(EDITS):
    assert recon.count(new) == 1, f"[{label}] reverse anchor not unique"
    recon = recon.replace(new, old, 1)

ok = (recon == orig)
print("\n=== verification ===")
print(f"orig V4.46 md5 : {hashlib.md5(orig.encode()).hexdigest()}")
print(f"recon md5      : {hashlib.md5(recon.encode()).hexdigest()}")
print(f"byte-reconstruction equals original V4.46: {ok}")
assert ok, "RECONSTRUCTION FAILED — edit is not purely additive"

# ---- frozen-row guard: §2.52 Open 3 Part VI row byte-identical, count preserved ----
FROZEN = ("| **§2.52 Open 3** (pulsation = ζ from §3.4) | **Open** — most structurally important; "
          "closure of §2.52 Open 2 (anharmonic δ = 0.01829) gated on this |")
co, ct = orig.count(FROZEN), text.count(FROZEN)
print(f"\n§2.52 Open 3 frozen row count: orig={co}, V4.47={ct}  ->  "
      f"{'BYTE-IDENTICAL, untouched' if co == ct == 1 else 'FAIL'}")
assert co == ct == 1, "§2.52 Open 3 frozen-row guard FAILED"

# ---- append-only size sanity ----
print(f"\norig chars : {len(orig)}")
print(f"V4.47 chars: {len(text)}  (added {len(text) - len(orig)})")
print(f"net new lines: {text.count(chr(10)) - orig.count(chr(10))}")

with open(OUT, "w", encoding="utf-8") as f:
    f.write(text)
print(f"\nwrote {OUT}")
print(f"V4.47 md5: {hashlib.md5(text.encode()).hexdigest()}")
