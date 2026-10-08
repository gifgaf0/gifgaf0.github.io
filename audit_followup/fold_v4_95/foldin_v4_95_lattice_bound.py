#!/usr/bin/env python3
"""foldin_v4_95_lattice_bound.py — FOLDS V4.95: the lattice-spacing bound (one short fold recording a bound).

Authorized by the author's brief of October 7, 2026 (audit_followup/inputs/BRIEF_2026-10-07_lattice_bound.txt):
"This computes a bound. It is not a verdict on anything already decided." / "One short fold recording the bound is
authorized. Put a plain-language summary first. Write to the repo." / "List what the result touches: the light-only
transverse carrier, the polycrystal-floor row, and the ANNEX-SC-1 / G-S2C1-W chain." Base:
SQT_Master_Ledger_v4_94_CANONICAL.md (md5 708df4cf…, 1,862,277 B; produced by foldin_v4_94_phase_c.py).

Edits (all additive):
  E1 title; E2 As-of prepend; E3 the V4.95 fold-in record (before the V4.94 record);
  E5 §2.95 (after §2.94's last paragraph, before Cluster J);
  E6 nine in-line "[→ V4.95 (§2.95): …]" pointers at the end of each touched line (inside the last cell for table rows);
  E7 one Part VI row after the polycrystal-floor row; E8 one changelog line.
Anchors are read from the file and asserted unique; every fragment lands exactly once; the reverse splice must
reconstruct V4.94 byte-identically.
"""
import hashlib

SRC = "/home/claude/fold/SQT_Master_Ledger_v4_94_CANONICAL.md"
OUT = "/home/claude/fold/SQT_Master_Ledger_v4_95_CANONICAL.md"
V494, V494_BYTES = "708df4cf8f4703088c89b4fad96584bd", 1862277
LS_REMOTE = "2026-10-08 01:36:53 UTC"            # main = 3587eb3; estate branch claude/audit-followup-oct6 = 1322b2b
HEAD_AT_FOLD = "1322b2b"
ESTATE = "`audit_followup/lattice_bound/` on branch `claude/audit-followup-oct6`"

s = open(SRC, encoding="utf-8").read()
assert hashlib.md5(s.encode("utf-8")).hexdigest() == V494, "base V4.94 md5 mismatch — halt"
assert len(s.encode("utf-8")) == V494_BYTES
assert "§2.95" not in s and "V4.95" not in s
L = s.split("\n")
assert len(L) == 4711 and L[-1] == "", "line structure changed — re-anchor"


def one_line(prefix):
    hits = [x for x in L if x.startswith(prefix)]
    assert len(hits) == 1, f"anchor not unique: {prefix!r} ({len(hits)})"
    assert s.count("\n" + hits[0] + "\n") == 1
    return hits[0]


# ---------------------------------------------------------------- E1 title
T_OLD = "# SQT Master Ledger — V4.94 Canonical\n"
T_NEW = "# SQT Master Ledger — V4.95 Canonical\n"
assert s.count(T_OLD) == 1 and L[0] + "\n" == T_OLD

# ---------------------------------------------------------------- E2 As-of
A_OLD = "**As of:** October 7, 2026 (V4.94 fold — "
assert s.count(A_OLD) == 1 and L[2].startswith(A_OLD)
A_NEW = ("**As of:** October 7, 2026 (V4.95 fold — **the lattice-spacing bound (§2.95): the photon data require grains "
         "d ≤ 2.08×10⁻³⁵ m (1.28 ℓ_P; LHAASO's Cygnus and Crab PeV photons; two-leg), so a lattice with N cells per grain "
         "needs a ≤ 2.08×10⁻³⁵ m/N — below ℓ_P for any N ≥ 2 — and the declared 12–47 ℓ_P lattice fits no cell; grain "
         "texture t₄ ≲ 10⁻³⁵; dispersion not binding. A bound, not a verdict; N stays the author's election. Nothing "
         "published or sent.** V4.94 fold (October 7, 2026) — ")

# ---------------------------------------------------------------- E6 pointers (prefix, text, kind)
P = "§2.95"
BR = [
    # the ANNEX-SC-1 / G-S2C1-W chain
    ("**DECLARED (reading (a); author word \"Lock\", July 22, 2026;",
     f"[→ V4.95 ({P}): the transverse scale import stays unexercised. The photon data now bound it: grains d ≤ "
     "2.08×10⁻³⁵ m (1.28 ℓ_P), so a lattice with N cells per grain needs a ≤ 2.08×10⁻³⁵ m/N. A bound, not a "
     "pinning.]", "para"),
    ("**H. Gate G-SCALE1 EXECUTED (declaration-type; V4.67)",
     f"[→ V4.95 ({P}): on the transverse line the photon data require d ≤ 2.08×10⁻³⁵ m; the declared chain's a_phys ≥ "
     "1.899×10⁻³⁴ m is 9.2 times that, so under the chain no allowed grain holds even one cell. No scale is re-pinned, "
     "and the longitudinal declaration is untouched.]", "para"),
    ("| **Gate G-S2C1-W** (the W_∪′ re-derivation mini-gate",
     f"[→ V4.95 ({P}): under its a_phys band (≥ 1.899×10⁻³⁴ m), no grain the photon data allow (d ≤ 2.08×10⁻³⁵ m) "
     "holds even one cell; the verdict stands as recorded.]", "row"),
    # W^EM_∪
    ("**N. Gate G-CI1 REGISTERED + LOCKED + EXECUTED",
     f"[→ V4.95 ({P}): the photon data as a whole bound grains 181 times tighter: d ≤ 2.08×10⁻³⁵ m (1.28 ℓ_P), set by "
     "LHAASO's PeV photons from the Cygnus region, with the Crab within 1.3% (two-leg); a ≤ 2.08×10⁻³⁵ m/N for N cells "
     "per grain. The window of record stands as computed from its sealed anchor, reproduced to 8.2×10⁻¹⁰.]", "para"),
    ("| **Gate G-CI1** (the Q3(1) carrier-identity gate:",
     f"[→ V4.95 ({P}): all photon arms together bound d ≤ 2.08×10⁻³⁵ m (1.28 ℓ_P; two-leg); the window of record "
     "stands.]", "row"),
    # the polycrystal-floor row
    ("| **Polycrystal validity floor** (§2.94.C2 P2",
     f"[→ V4.95 ({P}): for the election, a ≤ 2.08×10⁻³⁵ m/N: 0.128 ℓ_P at N = 10, 0.064 at 20, 0.026 at 50, 0.013 at "
     "100, 0.0013 at 1,000; the literature supports N ≈ 50–100; options in `lattice_bound/LS_RESULT.md`.]", "row"),
    # the light-only transverse carrier
    ("**E. What the substrate program still stands on.**",
     f"[→ V4.95 ({P}): the one transverse light carrier now has a bound on its medium: grains ≤ 1.28 ℓ_P, so its cells "
     "must be finer than ℓ_P for any N ≥ 2 cells per grain.]", "para"),
    # the texture
    ("**S. Gate G-MSCS2 REGISTERED + LOCKED + EXECUTED",
     f"[→ V4.95 ({P}): the banked b₁ turns the GRB vacuum-birefringence limit (Δn < 2×10⁻³⁷) into t₄ ≤ "
     "1.1–1.2×10⁻³⁵ (hex) and 4.4–5.3×10⁻³⁶ (cubic), or 0.9–2.5×10⁻³⁰ in any orientation; random grains lie 33–36 "
     "orders below.]", "para"),
    ("**T. Gate G-MSCS-A REGISTERED + LOCKED + EXECUTED",
     f"[→ V4.95 ({P}): the first-order polarization split (E-SA-1(b), unopened) now has an observational bound, t₄ ≲ "
     "10⁻³⁵ along the GRB sightlines; the successor stays unopened, and this gate's numbers stand.]", "para"),
]
EDITS = []
for prefix, text, kind in BR:
    old = one_line(prefix)
    assert "[→ V4.95" not in old and "\n" not in text
    assert text.startswith("[→ V4.95 (§2.95): ") and text.endswith("]")
    if kind == "para":
        assert not old.endswith(" |")
        new = old + " " + text
    else:
        assert old.endswith(" |") and old.startswith("| ") and "|" not in text
        new = old[:-2] + " " + text + " |"
    EDITS.append((old, new))
assert len({o for o, _ in EDITS}) == len(EDITS), "two pointers on one line"
NBR = len(EDITS)
assert NBR == 9

# ---------------------------------------------------------------- E5 §2.95
J_ANCH = "## J. Multi-Lens Reference and Phase Incommensurability\n"
assert s.count(J_ANCH) == 1 and s.count("\n\n" + J_ANCH) == 1
REG94 = one_line("**Registers and non-claims.** C1: the ranks R1")
assert s.count(REG94 + "\n\n" + J_ANCH) == 1
S295 = [
    "### §2.95 — The Lattice-Spacing Bound: How Fine the Lattice Must Be for the Light Window (V4.95)",
    f"*(Folded V4.95, October 7, 2026, under the author's brief of October 7 — \"This computes a bound. It is not a "
    f"verdict on anything already decided.\"; \"One short fold recording the bound is authorized.\" Estate {ESTATE}: "
    "Prior Address `LS_PRIOR_ADDRESS.md`; pre-registration `LS_PREREG.md` ea6651ce, locked at 65404f5 before any "
    "computation; leg 1, then the comparison last; the pre-registered second-leg trigger fired, and a blind leg from the "
    "pre-registration alone agreed on 185/185 checks (worst 4.8×10⁻¹⁵). The touched entries carry [→ V4.95 (§2.95)] "
    "pointers. No scale is pinned or re-pinned.)*",
    "**In plain language.** Light here is a shear wave in a polycrystalline vacuum, and grains scatter it with a loss "
    "that grows as the fourth power of the photon energy and the cube of the grain size. LHAASO's PeV photons from the "
    "Cygnus region and the Crab Nebula therefore cap the grains at 2.1×10⁻³⁵ m, 1.28 Planck lengths: 181 times below "
    "W^EM_∪, whose anchor is a 0.73 TeV source. A grain of N cells then needs a lattice spacing a ≤ 2.1×10⁻³⁵ m/N, "
    "below the Planck length for any N ≥ 2; the declared 12–47 ℓ_P lattice does not fit a single cell. Any coherent "
    "grain alignment must be below about 10⁻³⁵, which random grains satisfy by more than 30 orders of magnitude. The "
    "lattice's own dispersion only requires a ≲ 10⁸ ℓ_P.",
    "**The bound (R1-machine two-leg).** Attenuation α = (Q_T^a/8)k⁴d³ (the G-CI1 machinery; Q_T^a = 0.0352–0.0755 "
    "from the G-TSH4-lineage tensors, i.e. α = c_geo ε_T²k⁴d³ with c_geo = 0.38–0.53); an arm excludes d when α·D > 1 "
    "under every reading, so each arm's bound is its most permissive reading (the lower energy, the shorter distance, "
    "the observed wavenumber) on the most permissive configuration (hex:step). d_max per arm: the anchor, 1ES 1101-232 "
    "at 0.733 TeV, z = 0.186: 3.764×10⁻³³ m (W^EM_∪ reproduced to 8.2×10⁻¹⁰); the Crab, 1.12 ± 0.09 PeV read at "
    "0.94 PeV and 1.54 kpc: 2.102×10⁻³⁵ m; the Cygnus region, 8 events above 1 PeV against 0.75 background, read at "
    "1 PeV and 1.25 kpc: 2.075×10⁻³⁵ m; GRB 221009A, 12.5 TeV read at 7.7 TeV, z = 0.151: 1.740×10⁻³⁴ m; Mrk 501 "
    "(HEGRA 1997), 16 TeV, z = 0.034: 1.049×10⁻³⁴ m. Every cell is deep in the Rayleigh regime (kd ≤ 2.6×10⁻¹³). "
    "**The data require d ≤ 2.075×10⁻³⁵ m = 1.284 ℓ_P** (decisive: Cygnus; the Crab is 1.3% above), **hence a ≤ "
    "1.04×10⁻³⁶ m (0.064 ℓ_P) at N = 20, 2.08×10⁻³⁷ m (0.013 ℓ_P) at N = 100 and 2.08×10⁻³⁸ m (0.0013 ℓ_P) at N = "
    "1,000** (with τ × 10, d ≤ 2.77 ℓ_P). The Planck length lies above a_max(N) for every N ≥ 2, and the declared "
    "band's lower edge, 1.899×10⁻³⁴ m, is 9.2 times d_max.",
    "**Texture and dispersion.** A textured aggregate is birefringent at first order, Δn = b₁t₄ (|b₁| = 0.0162–0.0455, "
    "§2.91.S). The GRB polarization limit σ < 10⁻³⁷ (Kostelecký & Mewes 2006) gives t₄ ≤ 1.1–1.2×10⁻³⁵ (hex) and "
    "4.4–5.3×10⁻³⁶ (cubic) along the burst sightlines; the cosmological spectropolarimetric level 2×10⁻³² gives t₄ ≤ "
    "0.9–2.5×10⁻³⁰ in any orientation. Random grains have a statistical texture of 10⁻⁶⁹–10⁻⁷² over a 1 Gpc Fresnel "
    "volume, so only a coherent large-scale alignment is restricted; the bound does not involve a. A centrosymmetric "
    "lattice has no dimension-5 term (ω² even and analytic in k; G-S2C1 A3), and LHAASO's quadratic bound E_QG,2 > "
    "6.9×10¹¹ GeV (subluminal) with a₂ = −0.0132 gives a ≤ 1.76×10⁻²⁷ m = 1.09×10⁸ ℓ_P, which never binds.",
    "**The floor, registers and non-claims.** The homogenization literature (atomistic nanocrystals: 15–27% soft at "
    "9–37 cells, within a few percent from about 55) supports N ≈ 50–100; the options are in `LS_RESULT.md`, and N "
    "stays the author's election (Part VI). The arms and the combined bound are R1-machine two-leg, the readings R2; "
    "the polycrystal postulate stays R3. Nothing already decided changes: W^EM_∪ of record, G-S2C1-W's verdict and the "
    "declared chain stand as recorded. The A1 polarization verdict, the A2 internal-mode friction, the second-sound drag "
    "and KC-EP are not touched. Nothing is published or sent.",
]
S295_TXT = "\n\n".join(S295) + "\n\n"

# ---------------------------------------------------------------- E7 Part VI row (after the polycrystal-floor row)
FLOOR = one_line("| **Polycrystal validity floor** (§2.94.C2 P2")
GC1 = one_line("| **G-C1 gate** (angle-3")
assert s.count("\n" + FLOOR + "\n" + GC1 + "\n") == 1
ROW = ("| **Lattice-spacing bound** (§2.95 — the largest lattice spacing all photon data allow, a_max(N), for N cells per "
       "grain; brief of October 7, 2026; pre-registration ea6651ce) | **RECORDED (V4.95) — a bound, not a verdict:** d ≤ "
       "2.08×10⁻³⁵ m (1.28 ℓ_P; decisive the Cygnus PeV arm, the Crab within 1.3%; two-leg), so a ≤ 1.04×10⁻³⁶ / "
       "2.08×10⁻³⁷ / 2.08×10⁻³⁸ m at N = 20 / 100 / 1,000; texture t₄ ≲ 10⁻³⁵ along the GRB sightlines; dispersion "
       "a ≤ 1.1×10⁸ ℓ_P, not binding. N stays the author's election (row above). |\n")
assert ROW.count("|") == 3

# ---------------------------------------------------------------- E3 fold-in record
R_ANCH = "**V4.94 fold-in record (October 7, 2026):**"
assert s.count(R_ANCH) == 1 and L[38].startswith(R_ANCH) and L[37] == ""
RECORD = ("**V4.95 fold-in record (October 7, 2026):** LATTICE-SPACING BOUND — one short fold recording a bound, under "
          "the author's brief of October 7, 2026 (\"This computes a bound. It is not a verdict on anything already "
          "decided.\"; \"One short fold recording the bound is authorized. Put a plain-language summary first. Write to "
          "the repo.\"; `FOLD_AUTHORIZATION_V4_95.md`). Prior Address and pre-registration (`LS_PREREG.md` ea6651ce, "
          "locked 65404f5) before any computation; leg 1 (a9e6091) committed before the comparison (ebf150c); the "
          "pre-registered second-leg trigger fired (the combined bound empty at N = 20 in both senses), the comparator "
          "was frozen (824f7fd), and a blind leg from the pre-registration alone agreed on 185/185 checks (worst "
          "4.8×10⁻¹⁵; 4a4b7b0). Result: d ≤ 2.08×10⁻³⁵ m (1.28 ℓ_P), so a ≤ 2.08×10⁻³⁵ m/N; texture t₄ ≤ "
          "1.1–1.2×10⁻³⁵ (hex) / 4.4–5.3×10⁻³⁶ (cubic) along the GRB sightlines; dispersion a ≤ 1.76×10⁻²⁷ m. Recorded "
          f"as §2.95, with {NBR} in-line [→ V4.95] pointers and one Part VI row. Nothing published or sent. Estate: "
          f"{ESTATE} (head at fold `{HEAD_AT_FOLD}`); `git ls-remote` {LS_REMOTE}: main = `3587eb3`. No §3.x; no "
          "observable bridge.\n\n")

# ---------------------------------------------------------------- E8 changelog
LINE_CH94 = one_line("*V4.94 (October 7, 2026): additions only")
assert L[4709] == LINE_CH94 and L[4710] == ""
CH_NEW = (f"*V4.95 (October 7, 2026): additions only — title/As-of header bump; the V4.95 fold-in record; §2.95 (the "
          f"lattice-spacing bound) after §2.94; {NBR} in-line [→ V4.95] pointers; one Part VI row after the "
          "polycrystal-floor row; reverse-splice byte-identical to V4.94 (`708df4cf`).*")


def build():
    frags = [T_NEW, A_NEW, RECORD, S295_TXT, ROW, CH_NEW] + [n for _, n in EDITS]
    for fr in [A_NEW, RECORD, S295_TXT, ROW, CH_NEW]:
        assert s.count(fr) == 0
    out = s.replace(T_OLD, T_NEW, 1)
    out = out.replace(A_OLD, A_NEW, 1)
    out = out.replace(R_ANCH, RECORD + R_ANCH, 1)
    for old, new in EDITS:
        assert out.count("\n" + old + "\n") == 1
        out = out.replace("\n" + old + "\n", "\n" + new + "\n", 1)
    out = out.replace(REG94 + "\n\n" + J_ANCH, REG94 + "\n\n" + S295_TXT + J_ANCH, 1)   # §2.94's last line: no pointer
    out = out.replace("\n" + FLOOR_NEW + "\n", "\n" + FLOOR_NEW + "\n" + ROW, 1)
    out = out.replace("\n" + LINE_CH94 + "\n", "\n" + LINE_CH94 + "\n" + CH_NEW + "\n", 1)
    for fr in frags:
        assert out.count(fr) == 1, f"fragment count != 1: {fr[:60]!r}"
    assert out.count("[→ V4.95 (§2.95): ") == NBR
    # reverse splice
    rev = out.replace("\n" + LINE_CH94 + "\n" + CH_NEW + "\n", "\n" + LINE_CH94 + "\n", 1)
    rev = rev.replace("\n" + FLOOR_NEW + "\n" + ROW, "\n" + FLOOR_NEW + "\n", 1)
    rev = rev.replace(REG94 + "\n\n" + S295_TXT + J_ANCH, REG94 + "\n\n" + J_ANCH, 1)
    for old, new in EDITS:
        rev = rev.replace("\n" + new + "\n", "\n" + old + "\n", 1)
    rev = rev.replace(RECORD + R_ANCH, R_ANCH, 1)
    rev = rev.replace(A_NEW, A_OLD, 1)
    rev = rev.replace(T_NEW, T_OLD, 1)
    assert hashlib.md5(rev.encode("utf-8")).hexdigest() == V494 and rev == s, "REVERSE-SPLICE FAILED"
    return out


FLOOR_NEW = [n for o, n in EDITS if o == FLOOR][0]   # the floor row carries its pointer; the new row follows it

if __name__ == "__main__":
    out = build()
    open(OUT, "w", encoding="utf-8", newline="\n").write(out)
    b = open(OUT, "rb").read()
    print("V4.95 FOLDED:", OUT)
    print("bytes:", len(b), "(V4.94 %d B; delta +%d B); chars delta +%d" % (V494_BYTES, len(b) - V494_BYTES, len(out) - len(s)))
    print("md5:", hashlib.md5(b).hexdigest())
    print("pointers:", NBR, "| §2.95 chars:", len(S295_TXT), "| record chars:", len(RECORD), "| row chars:", len(ROW))
    print("reverse-splice: BYTE-IDENTICAL to V4.94 (%s) — PASS" % V494)
    print("all fragments landed exactly once — PASS")
