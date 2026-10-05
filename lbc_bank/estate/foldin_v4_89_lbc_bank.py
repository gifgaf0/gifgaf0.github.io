#!/usr/bin/env python3
"""foldin_v4_89_lbc_bank.py — FOLDS V4.89: the longitudinal-sector result BANKED (§2.91.V) — a banking fold, single
leg, no gate; author-authorized by the brief of October 3, 2026, 20:16 PDT ("Fold (author-authorized, conditional on
step 1)"), the step-1 check having cleared (no ledger item removes the knots' coupling to the longitudinal sector in the
transverse line). Carries the staged HK-5 housekeeping bracket (V4_89_HOUSEKEEPING_STAGING.md).
Eight additive edits on SQT_Master_Ledger_v4_88_CANONICAL.md (md5 66b0a634…, 1,768,607 B):
  E1 title; E2 As-of prepend (accumulated); E3 V4.89 fold-in record (before the V4.88 record); E4 new §2.91.V (bold-lettered
  paragraph after §2.91.U, immediately before the Cluster J heading); E5 one italic annotation paragraph after the §2.91.I
  headline paragraph (the head of the transverse line); E6 the HK-5 bracket after the V4.88 record's estate sentence;
  E7 a short HK-5 pointer after §2.91.U's estate sentence; E8 one changelog line.
Anchors read from the file and asserted unique; the §2.52 Open 3 Part VI row asserted byte-identical; reverse-splice must
reconstruct V4.88 byte-identically before the output is accepted. Append-only; nothing prior modified; no retraction.
"""
import hashlib, sys

SRC = "/home/claude/fold/SQT_Master_Ledger_v4_88_CANONICAL.md"
OUT = "/home/claude/fold/SQT_Master_Ledger_v4_89_CANONICAL.md"
V488, V488_BYTES = "66b0a634e3b087c85d4209f3e6bb6a28", 1768607

s = open(SRC, encoding="utf-8").read()
assert hashlib.md5(s.encode("utf-8")).hexdigest() == V488, "base V4.88 md5 mismatch — halt"
assert len(s.encode("utf-8")) == V488_BYTES
L = s.split("\n")
assert len(L) == 4630 and L[-1] == "", "line structure changed — re-anchor"

# anchors read from the file (never retyped)
LINE_CH88 = L[4628]
assert LINE_CH88.startswith("*V4.88 (October 2, 2026): additions only") and s.count(LINE_CH88) == 1
I_HEAD = L[1617]
assert I_HEAD.startswith("**I. Gate G-TSH1 REGISTERED + LOCKED + EXECUTED") and s.count(I_HEAD) == 1
assert L[1618] == "" and L[1619].startswith("**Controls, the F9 Ward falsifier")
O3 = [l for l in L if l.startswith("| **§2.52 Open 3**")]
assert len(O3) == 1 and s.count(O3[0]) == 1
O3_PRE = O3[0]

# ---------------------------------------------------------------- E1 title
T_OLD = "# SQT Master Ledger — V4.88 Canonical\n"
T_NEW = "# SQT Master Ledger — V4.89 Canonical\n"
assert s.count(T_OLD) == 1

# ---------------------------------------------------------------- E2 As-of
A_OLD = "**As of:** October 2, 2026 (V4.88 fold — "
A_NEW = ("**As of:** October 4, 2026 (V4.89 fold — **the longitudinal-sector result BANKED as §2.91.V (R2, single leg): the "
         "knots' total-density coupling survives into the transverse line; on the instantiated supersolid a density source "
         "drives the subluminal second-sound branch generically (2D 0.31 c_T, 3D 0.062 c_T), so KC3/KC1 limit matter; the "
         "V4.67 loss length re-evaluated on the measured 3D slow branch: −39.2 orders, FAIL; c₂/c_T ≤ 0.78 in the "
         "supersolid phase; HK-5 landed (PR #34 bd1354d).** Full V4.89 record below. V4.88 fold (October 2, 2026) — ")
assert s.count(A_OLD) == 1

# ---------------------------------------------------------------- E3 fold-in record
R_ANCH = "**V4.88 fold-in record (October 2, 2026):**"
assert s.count(R_ANCH) == 1
RECORD = ("**V4.89 fold-in record (October 4, 2026):** BANKING FOLD, single leg, no gate; author-authorized (brief of "
          "October 3, 2026, 20:16 PDT, conditional on the step-1 check, which cleared; `FOLD_AUTHORIZATION_V4_89.md`). "
          "§2.91.V; one annotation at the head of the transverse line; the staged HK-5 bracket (V4.88 record) and pointer "
          "(§2.91.U); title/As-of; changelog. No Part VI row; no retraction; §2.52 Open 3 untouched. `git ls-remote` "
          "2026-10-04 04:27:26 UTC: main = bd1354d. Estate `lbc_bank/` (branch claude/lbc-bank-v489): the October 3 report "
          "3bb916f0 with its scripts and JSON, step 3, step 4, the external check cc12e688, this script. Store: V4.89 "
          "replaces V4.88 on the author's word.\n\n")

# ---------------------------------------------------------------- E4 §2.91.V
J_ANCH = "\n\n## J. Multi-Lens Reference and Phase Incommensurability\n"
assert s.count(J_ANCH) == 1
SEC_V = ("\n\n**V. Longitudinal branch coupling on the instantiated supersolid — BANKED (V4.89, October 4, 2026; R2: single "
         "chat leg + an internal hydrodynamic route + an external analytic re-derivation; not two-leg).** *Scope "
         "(checked before recording):* the V4.67 drag is a property of knots moving through the substrate, not of the "
         "gravity reading of the longitudinal channel. The coupling of record is Branch C (the channel reads the total "
         "density; ε ≠ 0 forced by core localization), never retired — V4.67 retired the bridge, not the coupling; G-VS1's "
         "Q-VS-2 restates it; the §2.91.D/H and ANNEX-CDEF-1 independence clauses scope radiation claims, not matter. "
         "KC3/KC1 therefore limit matter propagation in the instantiated substrate, and the transverse line inherits them. "
         "*Record:* on MV-G1 (g = 22) a localized density source drives both longitudinal branches — second sound "
         "c₂ = 1.765 ≈ 0.31 c_T with spectral weight Z₂/Z₁ = 0.33 (f-sum share 5.1 %, static share 67 %); transverse "
         "weight zero by symmetry; the lower-branch share F₋ = (c_*² − c₋²)/(c₊² − c₋²), c_*² = ρ_s M/(ρ_n ρ), vanishes only "
         "by tuning (BdG = static hydrodynamics to 1 %; f_s = 0.095; λ = μ to 0.2 %); generic over g = 13–44 and the γ6 "
         "kernel; 3D AB/hcp: c₂ = 0.062 c_T, F₂ = 0.17 %, static share 66 %. Below g = 22, c₂/c_T rises to 0.78 at the "
         "coexistence boundary Λ_c ≈ 13.0 (F₂ = 0.42), METASTABLE_CLAUSE — never 1. *Loss length:* drag through branch ν "
         "∝ F_ν, independent of c_ν (prefactor ρF_ν/4πv² in 3D, the Astrakharchik–Pitaevskii form); on the measured 3D "
         "slow branch the V4.67 headline −42.0 becomes −39.2 orders (closure readings −41.2 … −38.4; ξ_req ≈ 2×10⁴ m): "
         "FAIL. *Errata to the October 3 report:* (2) arXiv:2407.01072 is Poli, Baillie, Ferlaino & Blakie, PRA 110, "
         "053301 (2024), as V4.70 already pinned; (3) at a fixed density vertex a multipole-ℓ source puts power "
         "∝ F_ν Ω^(2ℓ+d+1)/c_ν^(2ℓ+d+2) into branch ν — the 3D quadrupole slow/fast ratio is ≈ 9×10¹⁰, not ~10⁶; (5) the "
         "coupling-class annex was not unresolved: Branch C declared ε ≠ 0, so the drive-mediated-only class does not "
         "describe the declared knots. Paper-cited numbers carry a prepared second-leg dispatch (not run). No KC "
         "re-litigated; no observable; §2.52 Open 3 untouched.")

# ---------------------------------------------------------------- E5 annotation at the head of the transverse line
ANNOT = ("\n\n*(V4.89 annotation — the transverse line's knots keep their total-density coupling (Branch C, never retired) "
         "and the instantiated substrate keeps two longitudinal branches, the slower subluminal (0.31 c_T in 2D at the "
         "canonical point, 0.062 c_T in 3D): the routing paragraph's 'transverse-only MacCullagh/Kelvin sector' framing "
         "describes the radiation claims, not the substrate; KC3/KC1 apply to matter on the measured slow branch "
         "(§2.91.V). The post-verdict Cauchy annotation re-reads: the static moduli are Cauchy-class (λ = μ to 0.2 %); "
         "R_T sits below 1/√3 because c_T² = μ/ρ_n while first sound is stiffened by the superfluid. No content of this "
         "section is modified.)*")

# ---------------------------------------------------------------- E6 / E7 HK-5 (staging note V4_89_HOUSEKEEPING_STAGING.md)
H1_ANCH = "together with the chat-side estate g_vs1_gate/estate/)."
assert s.count(H1_ANCH) == 1
H1_NEW = H1_ANCH + (" [→ V4.89 housekeeping: HK-5 landed — PR #34 (`bd1354d`, 2026-10-02 22:06:58 UTC) merged CC's five "
                    "G-VS1 commits (`82b2ff9` … `c21a25f`) and `g_vs1_gate/estate/` (23 files, manifest `28fb85d2`; "
                    "`CC_LANDING_VERIFICATION.md` `1f32f122`; `HK5_CC_RETURN_INBAND.md` `497326ad`); landing checks 122/122 "
                    "on both legs; T1 0 hits on every landed file (the five G-VS1 commit messages carry the harness "
                    "session-link trailer, a transport token scanning at base index 9 — D-HK5-CC-1, not rewritten); the "
                    "desk closed.]")
H2_ANCH = "the HK-5 PR lands both."
assert s.count(H2_ANCH) == 1
H2_NEW = H2_ANCH + " [→ V4.89 housekeeping: landed — PR #34, `bd1354d`, 2026-10-02 22:06:58 UTC; see the V4.88 record's bracket.]"

# ---------------------------------------------------------------- E8 changelog
CH_NEW = ("*V4.89 (October 4, 2026): additions only — title/As-of header bump; the V4.89 fold-in record; §2.91.V; one "
          "annotation at the head of the transverse line (§2.91.I); the HK-5 housekeeping bracket after the V4.88 record's "
          "estate sentence with a pointer at §2.91.U; reverse-splice byte-identical to V4.88 (`66b0a634`); the §2.52 "
          "Open 3 row untouched.*")


def build(metastable_clause):
    sec = SEC_V.replace("METASTABLE_CLAUSE", metastable_clause)
    assert "METASTABLE_CLAUSE" not in sec
    for frag in (A_NEW, RECORD, sec, ANNOT, H1_NEW, H2_NEW, CH_NEW):
        assert s.count(frag) == 0
    out = s.replace(T_OLD, T_NEW, 1)
    out = out.replace(A_OLD, A_NEW, 1)
    out = out.replace(R_ANCH, RECORD + R_ANCH, 1)
    out = out.replace(J_ANCH, sec + J_ANCH, 1)
    out = out.replace(I_HEAD + "\n", I_HEAD + ANNOT + "\n", 1)
    out = out.replace(H1_ANCH, H1_NEW, 1)
    out = out.replace(H2_ANCH, H2_NEW, 1)
    out = out.replace(LINE_CH88, LINE_CH88 + "\n" + CH_NEW, 1)
    O3_POST = [l for l in out.split("\n") if l.startswith("| **§2.52 Open 3**")]
    assert O3_POST == [O3_PRE] and out.count(O3_PRE) == 1, "§2.52 Open 3 row changed — halt"
    for frag in (T_NEW, A_NEW, RECORD, sec, ANNOT, H1_NEW, H2_NEW, CH_NEW):
        assert out.count(frag) == 1
    # reverse-splice
    rev = out.replace(LINE_CH88 + "\n" + CH_NEW, LINE_CH88, 1)
    rev = rev.replace(H2_NEW, H2_ANCH, 1)
    rev = rev.replace(H1_NEW, H1_ANCH, 1)
    rev = rev.replace(I_HEAD + ANNOT + "\n", I_HEAD + "\n", 1)
    rev = rev.replace(sec + J_ANCH, J_ANCH, 1)
    rev = rev.replace(RECORD + R_ANCH, R_ANCH, 1)
    rev = rev.replace(A_NEW, A_OLD, 1)
    rev = rev.replace(T_NEW, T_OLD, 1)
    assert hashlib.md5(rev.encode("utf-8")).hexdigest() == V488 and rev == s, "REVERSE-SPLICE FAILED"
    return out, sec


if __name__ == "__main__":
    clause = sys.argv[1]
    out, sec = build(clause)
    open(OUT, "w", encoding="utf-8", newline="\n").write(out)
    b = open(OUT, "rb").read()
    added = {k: len(v.encode("utf-8")) for k, v in (("E2 As-of", A_NEW[len("**As of:** October 4, 2026 ("):]),
                                                    ("E3 record", RECORD), ("E4 §2.91.V", sec), ("E5 annotation", ANNOT),
                                                    ("E6 HK-5", H1_NEW[len(H1_ANCH):]), ("E7 HK-5 pointer", H2_NEW[len(H2_ANCH):]),
                                                    ("E8 changelog", CH_NEW))}
    print("V4.89 FOLDED:", OUT)
    print("bytes:", len(b), "(V4.88 %d B; delta +%d B); chars delta +%d" % (V488_BYTES, len(b) - V488_BYTES,
                                                                            len(out) - len(s)))
    print("md5:", hashlib.md5(b).hexdigest())
    print("per-edit bytes:", added)
    print("reverse-splice: BYTE-IDENTICAL to V4.88 (%s) — PASS" % V488)
    print("§2.52 Open 3: Part VI row byte-identical and unique — PASS; edits E1..E8 landed exactly once — PASS")
