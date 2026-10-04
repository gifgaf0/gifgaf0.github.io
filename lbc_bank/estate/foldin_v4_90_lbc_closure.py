#!/usr/bin/env python3
"""foldin_v4_90_lbc_closure.py — FOLDS V4.90: the paper-cited LBC numbers closed TWO-LEG (banking annotation, no gate).
Author-authorized October 4, 2026, 14:16 PDT ("Go ahead and fold v 4.90"), on the staging note
lbc_bank/closure/V4_90_STAGING.md (rendered here in ledger style; one clause added to the §2.91.V bracket: the 3D ratio
c2/cT 0.062 -> ~0.06, which the staging note's "3D shear speeds" line implies).
Four additive edits on SQT_Master_Ledger_v4_89_CANONICAL.md (md5 db01bd27…, 1,773,873 B):
  E1 title; E2 As-of prepend (accumulated); E3 V4.90 fold-in record (before the V4.89 record);
  E4 one bracket at the end of §2.91.V; E5 one changelog line.
Anchors read from the file and asserted unique; the §2.52 Open 3 Part VI row asserted byte-identical; reverse-splice must
reconstruct V4.89 byte-identically before the output is accepted. Append-only; nothing prior modified; no retraction.
Fold-time repository facts from a live `git ls-remote` immediately before the run (2026-10-04 21:20:40 UTC).
"""
import hashlib

SRC = "/home/claude/fold/SQT_Master_Ledger_v4_89_CANONICAL.md"
OUT = "/home/claude/fold/SQT_Master_Ledger_v4_90_CANONICAL.md"
V489, V489_BYTES = "db01bd273629ce7a385ff3c7fb6efdfc", 1773873
LS_REMOTE = "2026-10-04 21:20:40 UTC"   # main = a9b5cab…; claude/lbc-bank-v489 = 2ec5baf…; PR #35 open

s = open(SRC, encoding="utf-8").read()
assert hashlib.md5(s.encode("utf-8")).hexdigest() == V489, "base V4.89 md5 mismatch — halt"
assert len(s.encode("utf-8")) == V489_BYTES
L = s.split("\n")
assert len(L) == 4637 and L[-1] == "", "line structure changed — re-anchor"

# anchors read from the file (never retyped)
LINE_CH89 = L[4635]
assert LINE_CH89.startswith("*V4.89 (October 4, 2026): additions only") and s.count(LINE_CH89) == 1
V_LINE = L[1659]
assert V_LINE.startswith("**V. Longitudinal branch coupling on the instantiated supersolid") and s.count(V_LINE) == 1
O3 = [l for l in L if l.startswith("| **§2.52 Open 3**")]
assert len(O3) == 1 and s.count(O3[0]) == 1
O3_PRE = O3[0]

# ---------------------------------------------------------------- E1 title
T_OLD = "# SQT Master Ledger — V4.89 Canonical\n"
T_NEW = "# SQT Master Ledger — V4.90 Canonical\n"
assert s.count(T_OLD) == 1 and L[0] + "\n" == T_OLD

# ---------------------------------------------------------------- E2 As-of
A_OLD = "**As of:** October 4, 2026 (V4.89 fold — "
assert s.count(A_OLD) == 1 and L[2].startswith(A_OLD)
A_NEW = ("**As of:** October 4, 2026 (V4.90 fold — "
         "**the paper-cited LBC numbers closed TWO-LEG (§2.91.V bracket): the blind CC second leg (PR #36) matched 108/112; "
         "all four misses were first-leg defects (2D states under-converged within F9, the 3D basis at |G| ≤ 22, a scan-edge "
         "selection at the melting end); corrected first leg 112/112. c₂/c_T: 0.77 at Λ_c, peak 0.79 on the metastable "
         "branch, then softening to a long-wavelength instability at g ≈ 12.38–12.40 — never 1. Loss length unchanged "
         "(−39.2 orders).** Full V4.90 record below. V4.89 fold (October 4, 2026) — ")

# ---------------------------------------------------------------- E3 fold-in record
R_ANCH = "**V4.89 fold-in record (October 4, 2026):**"
assert s.count(R_ANCH) == 1 and L[38].startswith(R_ANCH) and L[37] == ""
RECORD = ("**V4.90 fold-in record (October 4, 2026):** BANKING ANNOTATION, no gate; register upgrade of the paper-cited "
          "numbers only; author-authorized (\"Go ahead and fold v 4.90\", October 4, 2026, 14:16 PDT; "
          "`FOLD_AUTHORIZATION_V4_90.md`). *Second leg:* CC, blind, `claude/new-session-rp548n`, dispatch `e5153dc5`; "
          "pre-consultation commit `667644a` (checkpoint `b19d8b62`), comparator commit `bd7169e`; PR #36 merged `a9b5cab`. "
          "*First comparison:* 112 checks, 108 PASS, 4 MISS, all first-leg — **H-LBC-1:** 2D states passing F9 (residual "
          "1.3–3.9×10⁻³) carry a constant ω² offset: c_T 0.45–1.1 % low at |q|a/2π ≤ 0.10; **H-LBC-2:** 3D at |G| ≤ 22 "
          "gives negative (clipped) Goldstone ω², c_T 5.4 % low at q = 0.15 — the basis, not the state (projected residual "
          "3×10⁻¹³); **H-LBC-3:** at g = 12.45 the scan's argmin took a collapsed uniform state, so \"branch end 12.47\" was "
          "an artifact. *Correction:* chat-side, own code (`lbc_bank/closure/`); checkpoint v2 `aa01ea0a`, post-comparison, "
          "v1 untouched; 112/112 against CC (2D ≤ 0.13 %, 3D ≤ 0.013 %); the a*-branch fold (12.3267) is CC-only, not "
          "cited. *Disclosures:* **D-LBC-CC-1:** a CC sub-agent probed a shadow-library host while fetching a reference — "
          "refused, nothing retrieved; **D-LBC-CC-2:** the extractor was held by the CC permission check until the author's "
          "go-ahead. *F9 note:* its thresholds admit the H-LBC-1 offset; G-TSH1's canonical numbers came from such a state "
          "(windows at larger q), G-TSH3 is clean; flagged, no verdict re-litigated. `git ls-remote` " + LS_REMOTE + ": "
          "main = `a9b5cab`; estate `claude/lbc-bank-v489` = `2ec5baf` (PR #35, open; also holds the Cox v4 read, no ledger "
          "effect). Store: V4.90 replaces V4.89 on the author's word. No Part VI row; no retraction; §2.52 Open 3 "
          "untouched.\n\n")

# ---------------------------------------------------------------- E4 §2.91.V bracket
V_ANCH = "No KC re-litigated; no observable; §2.52 Open 3 untouched."
assert s.count(V_ANCH) == 1 and V_LINE.endswith(V_ANCH)
BRACKET = (" [→ V4.90: **two-leg** (PR #36; corrected first leg 112/112; `lbc_bank/closure/LBC_2LEG_CLOSURE_MEMO.md`). "
           "c₂/c_T = 0.77 at Λ_c (13.04), peak 0.79 near g ≈ 12.72, then c₂ → 0 at a long-wavelength instability, "
           "g ≈ 12.38–12.40 (two-leg; branch fold 12.33 CC-only; \"branch end 12.47\" withdrawn, H-LBC-3); never 1. g = 22: "
           "c_T = 5.80 (5.812 at q → 0; static 5.811); c₂ = 1.80 in the paper's window (1.765 above is G-TSH1's). 3D: "
           "c₂ = 0.471, shear 7.75–8.04 (was 7.3–8.2), c₂/c_T ≈ 0.06 (was 0.062, also at §2.91.I). Unchanged: Z₂/Z₁, F₂, "
           "static share, −39.2 orders, ξ_req, drag prefactor 1/4π.]")
V_NEW = V_ANCH + BRACKET

# ---------------------------------------------------------------- E5 changelog
CH_NEW = ("*V4.90 (October 4, 2026): additions only — title/As-of header bump; the V4.90 fold-in record; one bracket at "
          "§2.91.V; reverse-splice byte-identical to V4.89 (`db01bd27`); the §2.52 Open 3 row untouched.*")


def build():
    for frag in (A_NEW, RECORD, BRACKET, CH_NEW, T_NEW):
        assert s.count(frag) == 0
    out = s.replace(T_OLD, T_NEW, 1)
    out = out.replace(A_OLD, A_NEW, 1)
    out = out.replace(R_ANCH, RECORD + R_ANCH, 1)
    out = out.replace(V_ANCH, V_NEW, 1)
    out = out.replace(LINE_CH89, LINE_CH89 + "\n" + CH_NEW, 1)
    O3_POST = [l for l in out.split("\n") if l.startswith("| **§2.52 Open 3**")]
    assert O3_POST == [O3_PRE] and out.count(O3_PRE) == 1, "§2.52 Open 3 row changed — halt"
    for frag in (T_NEW, A_NEW, RECORD, BRACKET, CH_NEW):
        assert out.count(frag) == 1
    # reverse-splice
    rev = out.replace(LINE_CH89 + "\n" + CH_NEW, LINE_CH89, 1)
    rev = rev.replace(V_NEW, V_ANCH, 1)
    rev = rev.replace(RECORD + R_ANCH, R_ANCH, 1)
    rev = rev.replace(A_NEW, A_OLD, 1)
    rev = rev.replace(T_NEW, T_OLD, 1)
    assert hashlib.md5(rev.encode("utf-8")).hexdigest() == V489 and rev == s, "REVERSE-SPLICE FAILED"
    return out


if __name__ == "__main__":
    out = build()
    open(OUT, "w", encoding="utf-8", newline="\n").write(out)
    b = open(OUT, "rb").read()
    added = {"E2 As-of": len(A_NEW.encode("utf-8")) - len(A_OLD.encode("utf-8"))}
    added.update({k: len(v.encode("utf-8")) for k, v in (("E3 record", RECORD), ("E4 bracket", BRACKET),
                                                         ("E5 changelog", "\n" + CH_NEW))})
    print("V4.90 FOLDED:", OUT)
    print("bytes:", len(b), "(V4.89 %d B; delta +%d B); chars delta +%d" % (V489_BYTES, len(b) - V489_BYTES,
                                                                            len(out) - len(s)))
    print("md5:", hashlib.md5(b).hexdigest())
    print("per-edit bytes:", added)
    print("reverse-splice: BYTE-IDENTICAL to V4.89 (%s) — PASS" % V489)
    print("§2.52 Open 3: Part VI row byte-identical and unique — PASS; edits E1..E5 landed exactly once — PASS")
