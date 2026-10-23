#!/usr/bin/env python3
"""foldin_v4_102_e8_rigidity.py — fold V4.102: §2.102, E8 harmonic rigidity registered.

Registers the exploration entry of October 22, 2026 (`e8_rigidity/exploration_e8_harmonic_rigidity_2026-10-22.md`,
revision 2): the weighted-theta theorem for E8 at R0, its corollaries C1–C6 at R1 (one leg, one environment).

Base: SQT_Master_Ledger_v4_101_CANONICAL.md at the repository root (md5 4a67c760…, 1,926,632 B). Edits (all additive):
title; As-of prepend; the V4.102 fold-in record (before the V4.101 record); §2.102 (after §2.101, before Cluster J);
two in-line "[→ V4.102 (§2.102): …]" pointers (§1.3's closing paragraph; §2.69's retirement paragraph); one changelog
line. Anchors are read from the file and asserted unique; every fragment lands exactly once; the reverse splice must
reconstruct V4.101 byte-identically.
"""
import argparse
import hashlib
import os

ap = argparse.ArgumentParser()
ap.add_argument("--word", required=True, help="the author's word, verbatim")
ap.add_argument("--when", required=True, help="time of the word, e.g. '19:47 PDT'")
ap.add_argument("--date", required=True, help="fold date, e.g. 'October 22, 2026'")
ap.add_argument("--ls-remote", required=True, help="UTC time of the live git ls-remote")
ap.add_argument("--main", required=True, help="main's sha from that ls-remote")
ap.add_argument("--out", required=True, help="output path")
args = ap.parse_args()

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.normpath(os.path.join(HERE, "..", "..", "SQT_Master_Ledger_v4_101_CANONICAL.md"))
V4101 = "4a67c76037b63adc6037aec0d7f2ac4d"
DATE = args.date

s = open(SRC, encoding="utf-8").read()
assert hashlib.md5(s.encode("utf-8")).hexdigest() == V4101, "base V4.101 md5 mismatch — halt"
BASE_BYTES = len(s.encode("utf-8"))
assert "§2.102" not in s and "V4.102" not in s
L = s.split("\n")
assert len(L) == 4951 and L[-1] == "", "line structure changed — re-anchor"


def one_line(prefix):
    hits = [x for x in L if x.startswith(prefix)]
    assert len(hits) == 1, f"anchor not unique: {prefix!r} ({len(hits)})"
    assert s.count("\n" + hits[0] + "\n") == 1
    return hits[0]


T_OLD, T_NEW = "# SQT Master Ledger — V4.101 Canonical\n", "# SQT Master Ledger — V4.102 Canonical\n"
assert s.count(T_OLD) == 1 and L[0] + "\n" == T_OLD
A_OLD = "**As of:** October 13, 2026 (V4.101 fold — "
assert s.count(A_OLD) == 1 and L[2].startswith(A_OLD)
A_NEW = (f"**As of:** {DATE} (V4.102 fold — **E₈ harmonic rigidity registered (§2.102): every harmonic weighting of "
         "an E₈ shell sums to a level-1 cusp-form coefficient (R0), so a Fano or PSL(2,7) weighting of the integral "
         "octonions changes only constants that the norm-1 and norm-2 shells fix (C1–C6, R1, one leg); the full-shell "
         "octonion route is closed for SQT, and sums restricted to a congruence class stay open. Nothing published or "
         "sent.** V4.101 fold (October 13, 2026) — ")

P = "[→ V4.102 (§2.102): "
BR = [  # (host prefix, must-contain on the host, pointer text)
    ("These are mathematical facts about finite Coxeter groups.", "E₈ → H₄ → physical-prediction route",
     P + "a further fact about the E₈ lattice: every harmonic weighting of a shell of fixed norm sums to a coefficient "
         "of a level-1 cusp form, so at degree 8 it is τ(n) times a constant set by the 240 roots (R0; Venkov, Pache). "
         "A Fano or PSL(2,7) weighting of the integral octonions changes only such constants (R1).]"),
    ("**Retirement of the octonionic-structure hypothesis at 256-bit residue distribution scale.**",
     "for this bit-length range only",
     P + "the octonion side of the question is closed at every scale for full-shell sums. On the integral octonions "
         "(E₈), a Fano or PSL(2,7) weighting of the norm-n shell changes only constants fixed by the norm-1 and norm-2 "
         "shells. Sums restricted to a congruence class have level above 1, are not covered, and would need their own "
         "pre-registration.]"),
]
EDITS = []
for prefix, must, text in BR:
    old = one_line(prefix)
    assert must in old and "[→ V4.102" not in old and "\n" not in text and text.endswith("]") and "|" not in text
    assert not old.endswith(" |")
    EDITS.append((old, old + " " + text))
assert len({o for o, _ in EDITS}) == len(EDITS) == 2

J_ANCH = "## J. Multi-Lens Reference and Phase Incommensurability\n"
REG101 = one_line("**Registers and non-claims.** Estate facts only, as read at fold time. No verdict, register or row "
                  "status changes; the deposit and the edit are the author's")
assert s.count(REG101 + "\n\n" + J_ANCH) == 1

S2102 = [
    "### §2.102 — E₈ Harmonic Rigidity: Fano Structure Cannot Move the Octonion Prime Bias (V4.102)",
    f"*(Folded V4.102, {DATE}, on the author's word of {args.when} (\"{args.word}\"; `FOLD_AUTHORIZATION_V4_102.md`). "
    "It registers the exploration entry of October 22, 2026, revision 2 "
    "(`e8_rigidity/exploration_e8_harmonic_rigidity_2026-10-22.md`), which a Gemini review checked and which was "
    "corrected before registration; its §6 records what was adopted. §1 below is R0 prior art. C1–C6 are R1, computed "
    "once, in one environment (`e8_rigidity/e8_harmonic_rigidity.py` md5 `198f483e…`; `e8_rigidity/fano_cP_check.py` "
    "md5 `b9902b40…`; outputs beside them). §1.3 and §2.69 carry [→ V4.102 (§2.102)] pointers.)*",
    "**In plain language.** The integral octonions of norm p form a shell of the E₈ lattice with 240(1 + p³) points. "
    "The October 22 prime experiments measured how those octonions lean toward the 240 units, one harmonic degree at a "
    "time. This entry records why SQT's Fano and PSL(2,7) structure cannot change that picture. At degree 8, any "
    "weighting of the norm-n octonions gives Ramanujan's τ(n) times one constant, which the 240 units fix. Below degree "
    "8 every weighting gives zero or the plain count of the shell. Degree 20 is the first with any freedom, and the "
    "norm-1 and norm-2 shells fix that too. The Fano lines do appear once, as a constant: weighting by the 7 quaternion "
    "subalgebras gives +6 at degree 8, against +3 for the non-line planes rescaled to 7. So the Fano labelling can choose "
    "constants but cannot add arithmetic. This is the number-theory counterpart of Paper II §3.4's locality result and "
    "of G-VS1's transitivity lemma (§2.91.U). The one opening is a sum restricted to a congruence class (C6).",
    "**1. The theorem (R0).** For an even unimodular lattice Λ ⊂ ℝᵈ and a harmonic polynomial P of degree k > 0, "
    "Θ_{Λ,P}(q) = Σ_{x∈Λ} P(x) q^{|x|²/2} is a cusp form of weight d/2 + k for SL₂(ℤ) (Hecke 1940; Schoeneberg 1939; "
    "Ebeling, *Lattices and Codes*, ch. 3). For E₈, with the octonion norm N(x) = |x|²/2: odd k gives 0; k = 2, 4, 6 "
    "and 10 give 0 for every n (S₆ = S₈ = S₁₀ = S₁₄ = 0; each shell is a spherical 7-design, Venkov); k = 8 gives "
    "Σ_{N(x)=n} P(x) = τ(n)·Σ_{units u} P(u); k = 12, 14, 16, 18 and 22 give one eigenform's coefficient times a constant; "
    "k = 20 gives a mix of the two eigenforms of S₂₄, fixed by the n = 1 and n = 2 shells. A polynomial Q of even degree "
    "2m that is not harmonic decomposes as c₀|x|^{2m} + Σ_{j≥1} |x|^{2(m−j)} P_{2j}(x), so for 2m ≤ 6 its shell sum is "
    "c₀nᵐ·240σ₃(n), and for 2m = 8 it is c₀n⁴·240σ₃(n) + τ(n)·c_P. Venkov's theorem in Pache's Proposition B (the "
    "2m-shell of E₈ is a spherical 8-design if and only if τ(m) = 0) is the degree-8 case read backwards. Nothing in "
    "this item is new.",
    "**2. Corollaries (R1, full-shell sums only).**\n"
    "- **C1. No Fano signal below degree 8.** The orientation 3-form φ is odd and vanishes on a single vector. Every "
    "Fano-line or PSL(2,7)-orbit weighting of degree ≤ 7 gives zero if harmonic, and the plain count of the shell "
    "otherwise. G₂ is transitive on S⁶ ⊂ Im 𝕆, so a G₂-invariant weighting depends only on Re x and |Im x|. It is zonal "
    "about 1, which is the statistic the October 22 experiment already measured (the single-vector case of §2.91.U's "
    "transitivity lemma). A Fano-specific weighting must break G₂ down to a finite line-preserving group.\n"
    "- **C2. Degree 8 is one constant, nonzero for the Fano lines.** For any degree-8 weighting the n-dependence is "
    "τ(n), with L(Δ, s), root number +1 and the sign of the lean all fixed. Computed for "
    "Q_lines(x) = Σ_{7 lines} |proj_{span{1,e_a,e_b,e_c}} x|⁸: c_P = +6. The 7 imaginary 3-planes give +3.9375, and "
    "the 28 non-line 4-planes, rescaled to 7, give +3. Each shell is W(E₈)-invariant and the degree-8 W(E₈)-invariant "
    "harmonics form one dimension, which explains the single constant. It does not give τ(n), which needs item 1; "
    "W(E₈) does not contain G₂.\n"
    "- **C3. The seven maximal orders.** Statistics depending only on N(x) and ⟨x, 1⟩ are identical across them: any "
    "two copies of E₈ are isometric and W(E₈) is transitive on roots, so an isometry fixing 1 carries one order to "
    "another. Computed: of the 30 arrangements of 14 four-element blocks on {1, e₀, …, e₆} (each three points in "
    "exactly one block), exactly 7 give unit sets closed under multiplication. The 21 automorphisms "
    "e_k ↦ ±e_{ak+b} (a ∈ {1, 2, 4}) preserve the Fano lines (i, i+1, i+3) mod 7 and permute the seven orders "
    "transitively. The 8 sign changes fix each order. So line-built weightings agree across the orders, as c_P = +6 in "
    "all seven confirms.\n"
    "- **C4. Degree 20.** In the basis {ΔE₄³, Δ²} of S₂₄ the Hecke eigenforms are "
    "f_± = ΔE₄³ + (−156 ± 12√144169)Δ², with a(2) = 540 ± 12√144169. A cusp form of weight 24 is fixed by its q and q² "
    "coefficients (Sturm bound 2), so the n = 1 and n = 2 shells (240 and 2,160 vectors) fix any degree-20 weighting's "
    "mix. Primes cannot reveal it.\n"
    "- **C5. Consequence.** On the E₈ side, for full-shell sums, no PSL(2,7)- or Fano-derived weighting can produce a "
    "prime signal that the units and the norm-1 and norm-2 shells do not already fix. The full-shell octonion route is "
    "closed for SQT.\n"
    "- **C6. The opening.** Item 1 needs the whole norm-n shell. A sum over x ≡ v (mod M), or over a sublattice, has "
    "level M > 1; new cusp forms of that level enter, with their own L-functions and root numbers, and C1–C5 do not "
    "apply. Any SQT experiment of that kind needs its own pre-registration, with the level and its forms computed "
    "before measuring.",
    "**3. Checks (one leg).** `e8_harmonic_rigidity.py`: shells n = 1, 2, 3, 5, 7 of sizes 240σ₃(n); degrees 2, 4, 6 "
    "sum to ≤ 9 × 10⁻¹⁷ of the scale; degree 8 gives shell sum / (τ(n) · root sum) = 1.0000000000 for n = 2, 3, 5, 7 "
    "and three directions; degree 20 predicts n = 3, 5, 7 from n = 1, 2 to ≤ 2 × 10⁻¹³. `fano_cP_check.py`: the 30 "
    "designs, the 7 orders and their permutation; c_P as in C2, the same in all seven orders; the full degree-8 formula "
    "for Q_lines on the n = 2 shell (34,416 directly and from the formula); the S₂₄ eigenforms of C4.",
    "**4. Not settled here.** The October 22 tower result stands: quaternion and octonion primes lean toward the "
    "units, degree by degree, with the sign set by the root number and central vanishing. The sign rule itself is known "
    "(Sarnak's 2007 letter to Mazur on Chebyshev's bias for τ(p); Devin, *Math. Proc. Cambridge Philos. Soc.* 169 "
    "(2020) 103–140), so a write-up presents the geometric picture and its exact verification on S³ and S⁷ as an "
    "illustration of those results. Whether the lean converges when summed over all degrees is open; that part could "
    "be new. Restricted sums (C6) are open.",
    "**5. Related observation (no register; not a Phase B test).** The Phase B partitions of Entry 008 (P5 = {1} | "
    "{2,…,6}; P4 = P7 = {3,5} | {1,2,4,6}) were applied to the October 22 consecutive-prime counts mod 455 (primes to "
    "10¹⁰ and 10¹¹) against the wheel–Cramér sieve model. They show the same 10⁻⁴-scale model residuals as the "
    "quadratic-residue split, with no Fano-specific excess. The sieve model is a correct null for consecutive-pair "
    "statistics; it does not answer Entry 007's question for fixed-bit-length residue counts.",
    "**Registers and non-claims.** Item 1 is R0. C1–C6 are R1, one leg, one environment; no CC second leg was run. Item "
    "5 has no register. Citations tagged [memory] in the source entry (Schoeneberg 1939; Ebeling ch. 3) are to be "
    "checked before any external use. No verdict on any earlier entry changes; §2.69 keeps its scope and its V4.98 "
    "note. No observable bridge; no §3.x; §2.52 untouched. Nothing is published, deposited or sent.",
]
S2102_TXT = "\n\n".join(S2102) + "\n\n"
for blk in S2102:
    assert "\n\n" not in blk

R_ANCH = "**V4.101 fold-in record (October 13, 2026):**"
assert s.count(R_ANCH) == 1 and L[38].startswith(R_ANCH) and L[37] == ""
RECORD = (f"**V4.102 fold-in record ({DATE}):** REGISTRATION — §2.102 and {len(EDITS)} in-line [→ V4.102] pointers "
          f"(§1.3, §2.69), on the author's word of {args.when} (\"{args.word}\"; `FOLD_AUTHORIZATION_V4_102.md`): E₈ "
          "harmonic rigidity, the weighted-theta theorem at R0 and its corollaries C1–C6 at R1 (one leg). A Fano or "
          "PSL(2,7) weighting of the integral octonions changes only constants that the norm-1 and norm-2 shells fix; "
          "the full-shell octonion route is closed for SQT; congruence-restricted sums stay open. No earlier verdict, "
          f"register or row changes; nothing published or sent. Estate: `e8_rigidity/`; `git ls-remote` "
          f"{args.ls_remote}: main = `{args.main}`. No §3.x; no observable bridge.\n\n")

LINE_CH101 = one_line("*V4.101 (October 13, 2026): additions only")
assert L[4949] == LINE_CH101 and L[4950] == ""
CH_NEW = (f"*V4.102 ({DATE}): additions only — title/As-of header bump; the V4.102 fold-in record; §2.102 (E₈ "
          f"harmonic rigidity, registered) after §2.101; {len(EDITS)} in-line [→ V4.102] pointers; reverse-splice "
          "byte-identical to V4.101 (`4a67c760`).*")


def build():
    frags = [T_NEW, A_NEW, RECORD, S2102_TXT, CH_NEW] + [n for _, n in EDITS]
    for fr in [A_NEW, RECORD, S2102_TXT, CH_NEW]:
        assert s.count(fr) == 0
    out = s.replace(T_OLD, T_NEW, 1)
    out = out.replace(A_OLD, A_NEW, 1)
    out = out.replace(R_ANCH, RECORD + R_ANCH, 1)
    for old, new in EDITS:
        assert out.count("\n" + old + "\n") == 1
        out = out.replace("\n" + old + "\n", "\n" + new + "\n", 1)
    out = out.replace(REG101 + "\n\n" + J_ANCH, REG101 + "\n\n" + S2102_TXT + J_ANCH, 1)
    out = out.replace("\n" + LINE_CH101 + "\n", "\n" + LINE_CH101 + "\n" + CH_NEW + "\n", 1)
    for fr in frags:
        assert out.count(fr) == 1, f"fragment count != 1: {fr[:60]!r}"
    assert out.count(P) == len(EDITS)
    rev = out.replace("\n" + LINE_CH101 + "\n" + CH_NEW + "\n", "\n" + LINE_CH101 + "\n", 1)
    rev = rev.replace(REG101 + "\n\n" + S2102_TXT + J_ANCH, REG101 + "\n\n" + J_ANCH, 1)
    for old, new in EDITS:
        rev = rev.replace("\n" + new + "\n", "\n" + old + "\n", 1)
    rev = rev.replace(RECORD + R_ANCH, R_ANCH, 1)
    rev = rev.replace(A_NEW, A_OLD, 1)
    rev = rev.replace(T_NEW, T_OLD, 1)
    assert hashlib.md5(rev.encode("utf-8")).hexdigest() == V4101 and rev == s, "REVERSE-SPLICE FAILED"
    return out


if __name__ == "__main__":
    out = build()
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    open(args.out, "w", encoding="utf-8", newline="\n").write(out)
    b = open(args.out, "rb").read()
    print("V4.102 written:", args.out)
    print("bytes:", len(b), "(V4.101 %d B; delta +%d B)" % (BASE_BYTES, len(b) - BASE_BYTES))
    print("md5:", hashlib.md5(b).hexdigest())
    print("pointers:", len(EDITS), "| §2.102 chars:", len(S2102_TXT), "| record chars:", len(RECORD))
    print("reverse-splice: BYTE-IDENTICAL to V4.101 (%s) — PASS" % V4101)
    print("all fragments landed exactly once — PASS")
