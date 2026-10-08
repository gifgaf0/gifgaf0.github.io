#!/usr/bin/env python3
# =============================================================================
# edit_paper_VII_oct2026.py — SQT Paper VII -> October 2026 corrections (DRAFT).
# Items (B3 of the October 6, 2026 audit follow-up, with the A3 blast radius):
#   (1) "zero tuned / free parameters" withdrawn everywhere it is claimed; scoped
#       wording: one anchor (m_e), one selected scale (ξ_vac), per-particle
#       selections; a leading-order fit with residual dof −1 (ledger §2.92).
#   (2) m_W = m0·φ^27 and sin²θ_W = φ^-3 retired as predictions (PDG 2024 record).
#   (3) Borromean ropelength prediction falsified at leading order (ledger
#       §2.15 retracted to Conjecture): 58.006 is an upper bound; L_B = 60.194 is
#       m_p inverted; the n/p "test" is a calibration output.
#   (4) A = 20 is the diagonal Δ_B(t,t,t) value; the single-variable polynomial
#       named by §3.2's convention gives 70.
#   (5) F7* ≅ Z6 is not a subgroup of PSL(2,7) (no element of order 6); the
#       Fano-triangle stabilizer is S3 (b3_checks.py).
#   (6) The L column mixes conventions (quarks per diameter; L_e, L_B per radius).
# Authority: ledger V4.92 §2.92 (A3 two-leg 46/46); audit brief B3; b3_checks.py,
#   b3_numbers.py. DRAFT ONLY: the author decides whether and how to adopt it.
# Discipline: md5 precondition on the source; anchored unique replacements;
#   reverse splice must return the source byte-exact; must-be-gone and
#   must-be-present checks.
# Usage: python3 edit_paper_VII_oct2026.py [SRC.md] [OUT_DIR]
# =============================================================================
import hashlib, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "source", "sqt_paper_VII_verified_clean.md")
OUT = sys.argv[2] if len(sys.argv) > 2 else HERE
DST = os.path.join(OUT, "sqt_paper_VII_oct2026_DRAFT.md")
SRC_MD5 = "996da45df7358772e1ccafd5a927c4aa"

text = open(SRC, encoding="utf-8").read()
md5_before = hashlib.md5(text.encode("utf-8")).hexdigest()
assert md5_before == SRC_MD5, f"source is not the Paper VII text of record (md5 {md5_before})"
th = {"t": text}
HUNKS = []  # (id, item, description, old, new)

def splice(hid, item, desc, old, new):
    t = th["t"]
    assert t.count(old) == 1, f"{hid}: anchor not unique (count={t.count(old)}) — {old[:70]!r}"
    th["t"] = t.replace(old, new)
    assert th["t"].count(new) == 1, f"{hid}: new text not unique"
    HUNKS.append((hid, item, desc, old, new))
    print(f"[hunk] {hid} — {desc}")

def splice_span(hid, item, desc, start, end, new):
    """Replace from the unique marker `start` through the unique marker `end` (inclusive)."""
    t = th["t"]
    assert t.count(start) == 1 and t.count(end) == 1, f"{hid}: span markers not unique"
    i, j = t.index(start), t.index(end) + len(end)
    assert i < j
    splice(hid, item, desc, t[i:j], new)

# ---------------------------------------------------------------- front matter and status note
STATUS = r"""> **Status note — October 2026 audit corrections (DRAFT, not adopted).**
> This draft corrects the claims below. The evidence is in the Master Ledger
> (V4.92, §2.92) and the audit follow-up record (Phase B, item B3). Sections not
> listed at the end are unchanged and still quote the pre-2024 PDG values.
>
> 1. **Parameter count.** "Zero tuned parameters" is withdrawn. The mass table is
>    a leading-order fit: one anchor ($m_e$), one shared selected scale
>    ($\xi_\text{vac} = 100\varphi$, with no combinatorial address) and per-row
>    selections — the knot, $A$, $Z_f$ and $L$ of each fermion, the $W$ exponent
>    27 and the $Z$ angle $\varphi^{-3}$. Eight comparison rows face eight per-row
>    selected inputs (the six fitted $Z_f$, the exponent, the angle) plus the
>    shared scale, so the residual degrees of freedom are $-1$ before the knot,
>    $A$ and $L$ choices are counted.
> 2. **Electroweak formulas retired as predictions.** $m_0\varphi^{27} = 82.13$ GeV
>    is 2.19% (132σ) above the PDG 2024 average $80.3692 \pm 0.0133$ GeV, and the
>    derived $m_Z = 93.96$ GeV is 3.04% above $91.1880 \pm 0.0020$ GeV.
>    $\varphi^{-3} = 0.23607$ is stated at no energy scale or scheme; it differs
>    from the standard definitions by −1.1% to +5.6%. §9 keeps both as a record.
> 3. **Borromean ropelength prediction falsified at leading order.** The ideal
>    Borromean ropelength is at most 58.006, the length of the best-known
>    configuration (Cantarella, Fu, Kusner, Sullivan & Wrinkle 2006). That is
>    below the window $60.194 \pm 0.3$ of Appendix E.1.2, and at 58.006 the mass
>    formula gives $m_p \approx 759$ MeV (−19%). $L_B = 60.194$ is $m_p$
>    inverted, so the proton's 0.000% and the neutron's −0.138% are calibration
>    outputs. Ledger §2.15 is retracted to Conjecture.
> 4. **$A = 20$.** It is the sum of squares of the diagonal specialization
>    $\Delta_B(t,t,t)$. The single-variable Alexander polynomial named by §3.2's
>    own convention, $(t-1)^4$ (Torres 1953), gives 70.
> 5. **$F_7^*$ and PSL(2,7).** $F_7^* \cong \mathbb{Z}_6$ is not a subgroup of
>    PSL(2,7), which has no element of order 6. The stabilizer of a Fano triangle
>    in PSL(2,7) ≅ GL(3,2) is $S_3$, also of order 6. Conjecture 1 ($Z_f = 6$)
>    stands as a conjecture; its §3.4 motivation is corrected.
> 6. **Mixed $L$ conventions.** The quark $L$ values are ideal ropelengths per
>    tube *diameter*: the trefoil's 16.372 is 32.743 per radius (Przybył &
>    Pierański, arXiv:1402.5760), and no nontrivial knot is below 31.32 per
>    radius (Denne, Diao & Sullivan, Geom. Topol. 10 (2006) 1–26). $L_e = 2\pi$
>    and the Borromean 58.006 are per *radius*, the convention of E.1.1.
> 7. **PDG 2024.** Against PDG 2024 (S. Navas et al., Phys. Rev. D 110, 030001)
>    only $b$, $t$ and $\tau$ are within 2%: $u$ −5.6% (outside $2.16 \pm 0.07$
>    MeV), $d$ −2.36%, $c$ −2.15%, $b$ −0.49%, $t$ −0.80%, $\tau$ −1.38%;
>    $W$ +2.19%, $Z$ +3.04%.
>
> Changed: Abstract; §3.2, §3.4, §3.5, §3.6; §7.4; §9 (head note, §9.1 rescoped,
> brackets in §9.2, §9.3, §9.6, §9.7); Chapter VI (OP.2, OP.8, "One
> Observational Anchor"); §12, §13, §15; E.1, E.1.2, E.1.3.
"""
splice("F1", "all", "front matter: draft line and the status note",
    "*OP.VIII.4 opened.*\n\n---\n\n# SQT Paper VII — Abstract",
    "*OP.VIII.4 opened.*\n*October 2026 audit corrections: DRAFT — see the status note below.*\n\n---\n\n"
    + STATUS + "\n---\n\n# SQT Paper VII — Abstract")

# ---------------------------------------------------------------- abstract
splice("A1", "1", "abstract: parameter claim scoped",
    r"""Gaussian throat curvature $K(0) = -\varphi^2$. Using the electron mass
$m_e$ as the sole physical anchor and zero tuned parameters, the
framework derives mass scales and fundamental couplings of the Standard
Model from the geometric and algebraic structure of the vacuum manifold.""",
    r"""Gaussian throat curvature $K(0) = -\varphi^2$. Using the electron mass
$m_e$ as the physical anchor, together with one selected length scale and
per-particle selections, the framework fits the mass scales of the
Standard Model at leading order to the geometric and algebraic structure
of the vacuum manifold *(October 2026: the earlier claim of "zero tuned
parameters" is withdrawn; see the status note)*.""")
splice("A2", "2,3,4,7", "abstract: results restated (PDG 2024, A = 20, W retired, ropelength falsified)",
    r"""We establish a topological dictionary mapping knot types to fermion
generations. For five of nine fundamental fermions — the Down, Charm,
Bottom, and Top quarks and the Tau lepton — mass predictions fall within
2% of PDG values. The framework provides a closed derivation of the
nucleon's topological floor ($A = 20$) from the multivariable Alexander
polynomial of the Borromean link, and retrodicts the inverse
fine-structure constant ($\alpha^{-1}$) to within 0.003% of observation
given the muonic proton radius as input. The $W$ boson mass is recovered
within 2.2% via the cubic vacuum lattice ($3^3 = 27$), and a primary
neutrino mass eigenstate of $\approx 0.044\,\text{eV}$ is predicted under
a volumetric delocalization conjecture.""",
    r"""We establish a topological dictionary mapping knot types to fermion
generations. Against PDG 2024, the fitted masses of three of nine
fundamental fermions — the Bottom and Top quarks and the Tau lepton —
fall within 2%; the Down and Charm quarks, within 2% of the older values
quoted in the body, are 2.4% and 2.1% low. The nucleon invariant $A = 20$
is computed from the diagonal specialization of the Borromean link's
multivariable Alexander polynomial (the single-variable polynomial gives
70). The framework retrodicts the inverse fine-structure constant
($\alpha^{-1}$) to within 0.003% of observation given the muonic proton
radius as input, and a primary neutrino mass eigenstate of
$\approx 0.044\,\text{eV}$ is predicted under a volumetric delocalization
conjecture. The electroweak formulas $m_W = m_0\varphi^{27}$ and
$\sin^2\theta_W = \varphi^{-3}$ are retired as predictions ($m_W$ is 2.2%,
132 standard deviations, above the measured value), and the Borromean
ropelength prediction for the proton mass is falsified at leading order.""")
splice("A3", "1,2", "abstract: inputs named; the retired Weinberg tension removed",
    r"""The framework operates under one observational anchor and five numbered
conjectures,""",
    r"""The framework operates under one observational anchor, one selected
scale, per-particle selections and five numbered conjectures,""")
splice("A4", "2", "abstract: tensions",
    r"""independent adjustment. Documented tensions include the Weinberg angle
($+5.9\%$ vs on-shell) and the neutrino mass sum ($10$–$30\%$ above the
Planck 2018 bound).""",
    r"""independent adjustment. Documented tensions include the neutrino mass
sum ($10$–$30\%$ above the Planck 2018 bound).""")

# ---------------------------------------------------------------- §3 baryon sector
splice("S1", "4", "§3.2: A = 20 is the diagonal value; the single-variable polynomial gives 70",
    r"""Borromean topology assignment — which is forced by §3.1 — $A = 20$ follows
with no degrees of freedom.""",
    r"""Borromean topology assignment — which is forced by §3.1 — $A = 20$ follows
with no degrees of freedom.

*Status (October 2026).* The Convention above names the single-variable
Alexander polynomial. For a link of three or more components that polynomial
is $(t-1)\,\Delta_B(t,t,t)$ up to units (Torres 1953), here
$(t-1)^4 = t^4 - 4t^3 + 6t^2 - 4t + 1$, with $A = 1 + 16 + 36 + 16 + 1 = 70$.
The value 20 is the sum of squares of the diagonal specialization
$\Delta_B(t,t,t)$, a different invariant; choosing it is a convention, not a
consequence of §3.1 (ledger §2.92).""")
splice("S2", "5", "§3.4: F7* is not a subgroup of PSL(2,7); the triangle stabilizer is S3",
    r"""$$F_7^* \;=\; \{1,2,3,4,5,6\} \;\subset\; \text{PSL}(2,7),
  \qquad F_7^* \;\cong\; \mathbb{Z}_6$$""",
    r"""$$F_7^* \;=\; \{1,2,3,4,5,6\}, \qquad F_7^* \;\cong\; \mathbb{Z}_6$$

*Correction (October 2026).* $F_7^*$ is not a subgroup of PSL(2,7): the
element orders of PSL(2,7) are 1, 2, 3, 4 and 7, so it has no element of
order 6. $F_7^*$ is the diagonal torus of SL(2,7), and its image in
PSL(2,7) has order 3; on the projective line over $\mathbb{F}_7$, the maps
$x \mapsto ax$ lie in PSL(2,7) only for the squares $a \in \{1,2,4\}$. The
stabilizer of a Fano triangle in PSL(2,7) ≅ GL(3,2) is $S_3$, of order 6,
acting as all permutations of the three points. The order 6 is therefore
available as $|S_3|$, but not as a cyclic $F_7^*$ inside PSL(2,7).""")
splice("S3", "3", "§3.5: L_B relabelled an inversion",
    r"""$$\boxed{L_B \;=\; 60.194\,\text{fm}} \qquad \textbf{(Prediction)}$$""",
    r"""$$L_B \;=\; 60.194\,\text{fm} \qquad \textbf{(inverted from } m_p\textbf{)}$$""")
splice("S4", "3", "§3.5: the prediction paragraph corrected (58.006 is an upper bound)",
    r"""This is a **prediction**: the value $L_B = 60.194\,\text{fm}$ should
equal the ideal ropelength of the Borromean rings — the minimum
length-to-radius ratio at maximal tube width — which is a purely geometric
quantity independent of mass data. The current best numerical bounds
(Ashton et al. 2011) are $L_B^\text{ideal} \in [58.006,\,62.0]\,\text{fm}$.
The prediction lies within these bounds. This is necessary but not yet
sufficient: the bounds span 6.7\%, and confirmation requires a numerical
minimization closing the interval to $<1\%$ precision (Appendix E).""",
    r"""This was presented as a **prediction**: the value $L_B = 60.194\,\text{fm}$
should equal the ideal ropelength of the Borromean rings — the minimum
length-to-radius ratio at maximal tube width — which is a purely geometric
quantity independent of mass data. *Status (October 2026): falsified at
leading order.* The original text quoted bounds $[58.006,\,62.0]$ and placed
$L_B$ inside them. But 58.006 is the length of the best-known tight
configuration (Cantarella, Fu, Kusner, Sullivan & Wrinkle 2006), so it is an
**upper** bound on the ideal ropelength, not a lower one. The ideal length is
therefore at most 58.006, below the window $60.194 \pm 0.3$ of Appendix
E.1.2. At $L = 58.006$ the same formula gives $m_p \approx 758.7\,\text{MeV}$
(−19.1%). Ledger §2.15 is retracted to Conjecture (§2.92).""")
splice("S5", "3", "§3.5: the n/p comparison is a calibration output",
    r"""Topology predicts identical hadronic cores; QED generates the residual.
This is the first prescription in SQT history for which both $m_p$ and
$m_n$ are simultaneously within $0.15\%$ of observation.""",
    r"""Topology predicts identical hadronic cores; QED generates the residual.
*(October 2026: because $L_B$ is solved from $m_p$, the proton's 0.000% and
the neutron's −0.138% are calibration outputs, not tests.)*""")
splice("S6", "4", "§3.6: A = 20 row",
    r"""| $A = 20$ from Borromean polynomial | **Derivation ✓** | Complete (§3.2) |""",
    r"""| $A = 20$ from Borromean polynomial | **Convention** — diagonal $\Delta_B(t,t,t)$; the single-variable polynomial gives 70 | §3.2 status (Oct. 2026) |""")
splice("S7", "3", "§3.6: Ashton-bounds row withdrawn",
    r"""| $L_B = 60.194\,\text{fm}$ in Ashton bounds | **Necessary check ✓** | Confirmed |""",
    r"""| $L_B = 60.194\,\text{fm}$ in Ashton bounds | **Withdrawn** — 58.006 is an upper bound | §3.5 status (Oct. 2026) |""")
splice("S8", "3", "§3.6: ropelength row falsified",
    r"""| $L_B$ from ideal Borromean minimization | **Prediction** | Numerical minimization to $<1\%$ (Appendix E) |""",
    r"""| $L_B$ from ideal Borromean minimization | **Falsified at leading order** | Ideal length ≤ 58.006 (E.1.3) |""")
splice("S9", "3", "§3.6: closing sentence",
    r"""target and becomes a pure prediction from topology and field arithmetic.""",
    r"""target and becomes a pure prediction from topology and field arithmetic.
*(October 2026: with the ideal length at most 58.006, a proof of Conjecture 1
would give $m_p \approx 759$ MeV at leading order, so it would not restore the
mass prediction.)*""")

# ---------------------------------------------------------------- §7.4
splice("Q1", "1", "§7.4: 'zero free parameters' scoped",
    r"""$+0.003\%$. The formula has zero free parameters — $\kappa$ is derived
in Theorem 1, $8\pi$ is selected by the spinor audit, the bare coupling
is conjectured from PSL(2,7) geometry — and $r_p$ is substituted from
measurement, not fitted.""",
    r"""$+0.003\%$. The formula has no continuously adjusted parameter, but it is
not parameter-free *(October 2026 scoping)*: $8\pi$ was selected from three
candidate solid angles because only it puts the required $r_p$ in the
measured range (§7.3), the numerator 84 is Conjecture 2, $\kappa$ comes from
Theorem 1, and $r_p$ is substituted from measurement.""")

# ---------------------------------------------------------------- §9 electroweak
splice("W1", "2", "§9 status table: exponent row",
    r"""| $3^3 = 27$ as exponent motivation | Geometric assertion — derivation pending |""",
    r"""| $3^3 = 27$ as exponent motivation | Geometric assertion — never derived (OP.8); a selected input in the ledger's count |""")
splice("W2", "2", "§9 status table: m_W retired",
    r"""| $m_W = m_0\varphi^{27}$ | Prediction — **+2.18%** (Amber) |""",
    r"""| $m_W = m_0\varphi^{27}$ | **Retired** (Oct. 2026) — +2.19%, 132σ against PDG 2024 |""")
splice("W3", "2", "§9 status table: sin²θ_W retired",
    r"""| $\sin^2\theta_W = \varphi^{-3}$ | Prediction — +5.9% vs on-shell (Orange) |""",
    r"""| $\sin^2\theta_W = \varphi^{-3}$ | **Retired** (Oct. 2026) — no stated scale or scheme; +2.07% vs $\overline{\text{MS}}(M_Z)$, +5.63% vs on-shell |""")
splice("W4", "1,2", "§9: m_Z retired; retirement note; §9.1 retitled",
    r"""| $m_Z = m_W^\text{SQT}/\cos\theta_W^\text{SQT}$ | Prediction — **+3.05%** (Amber) |

---

### §9.1  The Framework's Single Observational Anchor""",
    r"""| $m_Z = m_W^\text{SQT}/\cos\theta_W^\text{SQT}$ | **Retired** (Oct. 2026) — +3.04%, 1388σ against PDG 2024 |

**Retirement (October 2026).** The formulas of §9.2–§9.6 are no longer
presented as predictions. The exponent 27 and the angle $\varphi^{-3}$ are
selected inputs (the ledger's fit count includes both, §2.92), the exponent's
derivation was never supplied (OP.8), and $\varphi^{-3}$ carries no energy
scale or renormalization scheme. Against PDG 2024 (S. Navas et al., Phys.
Rev. D 110, 030001): $m_W = 82.13$ GeV is +2.19% above $80.3692 \pm 0.0133$
GeV (132σ); $m_Z = 93.96$ GeV is +3.04% above $91.1880 \pm 0.0020$ GeV; and
$\varphi^{-3} = 0.23607$ is +2.07% above $\hat s^2_Z = 0.23129$
($\overline{\text{MS}}$ at $M_Z$), +5.63% above the on-shell
$s^2_W = 0.22348$, +1.92% above the effective leptonic $0.23161$, and 1.12%
below the low-energy $\hat s^2_0 = 0.23873$ (Electroweak review, Table 10.2).
§9.2–§9.6 are kept below as a record, with brackets; §9.1 is rescoped.

---

### §9.1  The Observational Anchor and the Selected Inputs""")
splice("W5", "1", "§9.1: opening sentence",
    r"""Before deriving the Weak sector, the status of $m_0$ must be stated
precisely, because the framework's "zero free parameters" claim depends on it.""",
    r"""The status of $m_0$, and of every other input the formulas take, must be
stated precisely.""")
splice("W6", "1,6", "§9.1: scoped wording — one anchor, one selected scale, per-particle selections, dof −1",
    r"""is derived from the Gaussian throat curvature $K(0) = -\varphi^2$ with no fitting.
The framework therefore has **one observational anchor** ($m_e$) and **zero tuned
parameters**. Every mass, coupling, and ropelength prediction follows from
$m_e$ plus geometry.""",
    r"""is taken from the Gaussian throat curvature $K(0) = -\varphi^2$.
The framework has **one observational anchor** ($m_e$), but it is **not**
zero-parameter *(October 2026 correction)*. The mass formula also takes one
shared selected scale, $\xi_\text{vac} = 100\varphi$, which has no
combinatorial address (ledger §2.64.A), and per-particle selections: the knot
assignment, $A$, $Z_f$ and $L$ of each fermion (the six $Z_f$ values are
fitted) and, for the bosons, the exponent 27 and the angle $\varphi^{-3}$.
Eight comparison rows face eight per-row selected inputs plus the shared
scale, so the residual degrees of freedom are $-1$ (ledger §2.92). The mass
results are a leading-order fit, not predictions from $m_e$ plus geometry.
The $L$ column also mixes conventions: the quark values are ideal
ropelengths per tube diameter, while $L_e = 2\pi$ and the Borromean length
are per radius.""")
splice("W7", "2", "§9.2: bracket on 'rigid and non-tuned'",
    r"""to "exponent 27 in $m_0\varphi^{27}$" is stated as a conjecture.
Closing it is Open Problem 8 (OP.8), to be addressed in Paper VIII.""",
    r"""to "exponent 27 in $m_0\varphi^{27}$" is stated as a conjecture.
Closing it is Open Problem 8 (OP.8), to be addressed in Paper VIII.
*[Retired, October 2026: nothing derived forces the exponent, which the
ledger counts as a selected input; see the note at the head of §9.]*""")
splice("W8", "2", "§9.3: bracket on 'neither fitted nor adjusted'",
    r"""loop corrections. It is neither fitted to the W mass nor adjusted post-hoc;
the formula was fixed by the cubic lattice argument.""",
    r"""loop corrections. It is neither fitted to the W mass nor adjusted post-hoc;
the formula was fixed by the cubic lattice argument.
*[Retired, October 2026: against PDG 2024 ($80.3692 \pm 0.0133$ GeV) the
formula is +2.19%, 132σ; see the note at the head of §9.]*""")
splice("W9", "1,2", "§9.6: bracket on 'no fitted parameters'",
    r"""motivated predictions to theorems.""",
    r"""motivated predictions to theorems.
*[Retired, October 2026: the exponent and the angle are selected inputs; see
the note at the head of §9.]*""")
splice("W10", "1,7", "§9.7: top Z_f is a fitted value; PDG 2024",
    r"""requires no additional conjecture beyond the knot assignment $8_1^9$
and ropelength $L = 37.31\,\text{fm}$.""",
    r"""requires no additional conjecture beyond the knot assignment $8_1^9$
and ropelength $L = 37.31\,\text{fm}$.
*[October 2026: $Z_f = \kappa/8$ is one of the six fitted $Z_f$ in the
ledger's count (§2.92); against PDG 2024 ($172.57 \pm 0.29$ GeV) the output
is −0.80%.]*""")

# ---------------------------------------------------------------- Chapter VI
splice("R1", "3", "OP.2: resolved negative",
    r"""| OP.2 | Prediction (§3.5) | Borromean ropelength | Tighten Ashton bounds $[58.006, 62.0]$ fm (6.7% span) to $<1\%$ precision by numerical ideal-Borromean minimization. If minimized value falls at $60.194 \pm 0.3$ fm, $L_B$ prediction is confirmed. Window justified in Appendix E.1.2: a minimized value outside this range but inside Ashton bounds falsifies the prediction at leading-order precision. | §3.5 | Prediction/Test |""",
    r"""| OP.2 | Prediction (§3.5) | Borromean ropelength | **Resolved negative (October 2026).** The ideal Borromean ropelength is at most 58.006 (Cantarella, Fu, Kusner, Sullivan & Wrinkle 2006), below the window $60.194 \pm 0.3$: the $L_B$ prediction is falsified at leading order (E.1.3; ledger §2.15 retracted to Conjecture, §2.92). The original entry read 58.006 as a lower bound. | §3.5 | Falsified |""")
splice("R2", "2", "OP.8: formula retired",
    r"""Requires showing the lattice mode structure forces the $\varphi$-exponent to equal the volumetric degree count, not $\varphi^3$ (one axis) or $\varphi^9$ (face). | §9.2 | Open Problem |""",
    r"""Requires showing the lattice mode structure forces the $\varphi$-exponent to equal the volumetric degree count, not $\varphi^3$ (one axis) or $\varphi^9$ (face). The formula is retired as a prediction (October 2026); this derivation would be needed to revive it. | §9.2 | Open Problem (formula retired) |""")
splice_span("R3", "1,2,3", "Chapter VI 'One Observational Anchor': selected inputs named",
    "### One Observational Anchor\n",
    "above is the complete accounting of which results are theorems and which\nremain open.",
    r"""### One Observational Anchor and the Selected Inputs

*Corrected October 2026.* Every result in this paper chains back to one
measured input,

$$m_0 \;=\; \frac{m_e}{e^{2\pi/\Phi}},$$

where $m_e = 0.511\,\text{MeV}$ is the electron mass (measured) and $\Phi$
is taken from the Gaussian throat curvature. The results are not, however,
free of tuning: the mass formula also takes one shared selected scale
($\xi_\text{vac} = 100\varphi$, with no combinatorial address) and
per-particle selections — the knot, $A$, $Z_f$ and $L$ of each fermion (the
six $Z_f$ values are fitted), the $W$ exponent 27 and the $Z$ angle
$\varphi^{-3}$. Eight comparison rows face eight per-row selected inputs plus
the shared scale, so the mass table is a leading-order fit with residual
degrees of freedom $-1$ (ledger §2.92). Of the quantities this section once
listed as following from $m_e$ plus geometry, the gauge-boson masses are
retired as predictions (§9) and the Borromean ropelength prediction is
falsified at leading order (E.1.3).

The open problems listed above are derivations required to close specific
results as theorems. Resolving them would not by itself remove the selected
inputs. When any open problem is resolved, the framework either gains a
theorem (if the derivation succeeds) or loses a prediction (if it fails).""")

# ---------------------------------------------------------------- Chapter VII
splice("C1", "1", "§12: parameter claim scoped",
    r"""The framework operates from one observational anchor — the electron mass
$m_e = 0.511\,\text{MeV}$ — and zero tuned parameters. Every prediction
chains through:""",
    r"""The framework operates from one observational anchor — the electron mass
$m_e = 0.511\,\text{MeV}$ — together with one selected scale
($\xi_\text{vac} = 100\varphi$) and per-particle selections (knot, $A$,
$Z_f$, $L$); the mass table is a leading-order fit *(October 2026
correction)*. Every output chains through:""")
splice("C2", "1,7", "§12: table heading",
    r"""**Closed results (Theorems and Derivations):**""",
    r"""**Fitted results** *(values as originally quoted; the status note gives PDG 2024)*:""")
splice("C3", "2", "§12: W row retired",
    r"""| $W$ boson mass ($m_0\varphi^{27}$) | 82,128 MeV | 80,379 MeV | +2.18% | Amber |""",
    r"""| $W$ boson mass ($m_0\varphi^{27}$) | 82,128 MeV | 80,379 MeV | +2.18% | Retired (Oct. 2026) |""")
splice("C4", "2", "§12: Z row retired",
    r"""| $Z$ boson mass | 93,964 MeV | 91,187.6 MeV | +3.05% | Amber |""",
    r"""| $Z$ boson mass | 93,964 MeV | 91,187.6 MeV | +3.05% | Retired (Oct. 2026) |""")
splice("C5", "2", "§12: Weinberg row retired",
    r"""| $\sin^2\theta_W$ | 0.23607 | 0.2229 (on-shell) | +5.91% | Orange |""",
    r"""| $\sin^2\theta_W$ | 0.23607 | 0.2229 (on-shell) | +5.91% | Retired (Oct. 2026) |""")
splice("C6", "2", "§12: Weinberg sentence",
    r"""concealed. The Weinberg angle at +5.9% off the on-shell definition is
the largest unexplained discrepancy in the primary derivations.""",
    r"""concealed. The Weinberg angle at +5.9% off the on-shell definition was
the largest unexplained discrepancy in the primary derivations; the formula
is retired as a prediction (October 2026).""")
splice("C7", "4", "§12: A = 20 row",
    r"""| Proton topology ($A = 20$) | Derivation from Borromean Alexander polynomial | Closed |""",
    r"""| Proton topology ($A = 20$) | Diagonal $\Delta_B(t,t,t)$; the single-variable polynomial gives 70 | Convention (Oct. 2026) |""")
splice("C8", "3", "§12: ropelength row falsified",
    r"""| Borromean ropelength ($L_B = 60.194$ fm) | Prediction within Ashton bounds | Pending verification |""",
    r"""| Borromean ropelength ($L_B = 60.194$ fm) | $m_p$ inverted; the ideal length is at most 58.006 | **Falsified at leading order** (Oct. 2026) |""")
splice("C9", "1", "§13: rigidity bracket",
    r"""rigidity: the predictions are not independently adjustable.""",
    r"""rigidity: the predictions are not independently adjustable.
*[October 2026: the mass table carries about as many selected inputs as
comparison rows (ledger §2.92), so this rigidity is not established for the
mass table.]*""")
splice("C10", "1,3", "§13: 'zero-free-parameter framework'",
    r"""This is the intended falsifiability structure of a zero-free-parameter
framework.""",
    r"""This is the intended falsifiability structure of the framework *(October
2026: the framework is not zero-parameter, and one of its tests — the
Borromean ropelength, E.1.3 — has already returned a negative result)*.""")
splice("C11", "1,7", "§15: dictionary item",
    r"""- A topological dictionary mapping knot types to quark and lepton
  generations, with 6 of 9 fermion masses predicted Green or near-Green
  from one observational anchor""",
    r"""- A topological dictionary mapping knot types to quark and lepton
  generations, fitted at leading order (one anchor, one selected scale,
  per-particle selections); against PDG 2024, 3 of 9 fermion masses are
  within 2% *(October 2026)*""")
splice("C12", "4", "§15: A = 20 item",
    r"""- $A = 20$ for the nucleon as a closed derivation from the Borromean
  Alexander polynomial — the first zero-free-parameter result for baryon
  topology in this framework""",
    r"""- $A = 20$ for the nucleon as the sum of squares of the diagonal
  specialization $\Delta_B(t,t,t)$ of the Borromean Alexander polynomial
  (the single-variable polynomial gives 70) *(October 2026)*""")
splice("C13", "1", "§15: α⁻¹ item",
    r"""- $\alpha^{-1}$ retrodicted to 0.003% given the muonic proton radius
  as input, via a formula with no fitted couplings""",
    r"""- $\alpha^{-1}$ retrodicted to 0.003% given the muonic proton radius
  as input, via a formula with no continuously fitted coupling (it carries
  the selected solid angle $8\pi$ and the conjectured numerator 84)""")
splice("C14", "2,3", "§15: 'has not established' — retired and falsified items",
    r"""- A resolution of the Weinberg angle at 5.9% off on-shell (OP.8)""",
    r"""- Electroweak boson masses or the Weinberg angle: the formulas are
  retired as predictions (§9, October 2026)
- A Borromean ropelength consistent with the proton mass: the prediction
  is falsified at leading order (E.1.3, October 2026)""")

# ---------------------------------------------------------------- Appendix E.1
splice("E1", "3", "E.1 status line",
    r"""*Status: Requirements locked. Mathematical execution pending.*""",
    r"""*Status (October 2026): Appendix E.1 is resolved negative — see E.1.3.
The Paper VIII preamble is unchanged.*""")
splice("E2", "3", "E.1 objective: the 6.7% window was a misreading",
    r"""Borromean rings ($L_{6a4}$) from their current $6.7\%$ window
$[58.006,\,62.0]\,\text{fm}$ to precision $\epsilon < 0.5\%$.""",
    r"""Borromean rings ($L_{6a4}$) from their current $6.7\%$ window
$[58.006,\,62.0]\,\text{fm}$ to precision $\epsilon < 0.5\%$.
*[October 2026: 58.006 is the length of the best-known configuration, an
upper bound on the ideal length; the "6.7% window" was a misreading.]*""")
splice("E3", "3", "E.1.2: the window cannot be reached",
    r"""either confirmed or falsified rather than merely consistent.""",
    r"""either confirmed or falsified rather than merely consistent.
*[October 2026: since the ideal length is at most 58.006, the window
$[59.894,\,60.494]$ cannot be reached.]*""")
splice("E4", "3", "E.1.3: outcome recorded",
    r"""*exactly* $60.194\,\text{fm}$ would require analytic methods beyond
numerical minimization.""",
    r"""*exactly* $60.194\,\text{fm}$ would require analytic methods beyond
numerical minimization.

**Outcome (October 2026).** The ideal Borromean ropelength is at most
58.006, the length of the configuration $B_0$ of Cantarella, Fu, Kusner,
Sullivan & Wrinkle (Geom. Topol. 10 (2006) 2055); the four-arc configuration
of Cantarella, Kusner & Sullivan (Invent. Math. 150 (2002)) has
$48\arctan\sqrt7 = 58.0526$. Both lie below 59.894, so the second row of the
table applies: **prediction falsified at leading order**. The table's third
row misreads 58.006 as a lower bound; a minimum below 58.006 would not
indicate an error in the bounds. Ledger §2.15 is retracted to Conjecture
(§2.92). At 58.006 the formula gives $m_p \approx 758.7$ MeV (−19.1%).""")

# ---------------------------------------------------------------- write + verify
final = th["t"]
os.makedirs(OUT, exist_ok=True)
open(DST, "w", encoding="utf-8").write(final)
md5_after = hashlib.md5(final.encode("utf-8")).hexdigest()
print(f"[source] md5 = {md5_before}")
print(f"[draft]  md5 = {md5_after}; bytes {len(text.encode())} -> {len(final.encode())}; "
      f"lines {len(text.splitlines())} -> {len(final.splitlines())}")
recon = final
for hid, item, desc, old, new in reversed(HUNKS):
    assert recon.count(new) == 1, f"reverse: {hid} new not unique"
    recon = recon.replace(new, old)
assert hashlib.md5(recon.encode("utf-8")).hexdigest() == md5_before, "reverse-splice FAILED"
print("reverse-splice reconstruction: OK (draft minus hunks == source byte-exact)")

must_be_gone = [
    "as the sole physical anchor and zero tuned parameters",
    "**one observational anchor** ($m_e$) and **zero tuned\nparameters**",
    "— and zero tuned parameters. Every prediction",
    "with zero additional tuning",
    "they do not introduce new free parameters",
    "The formula has zero free parameters",
    "the first zero-free-parameter result",
    "via a formula with no fitted couplings",
    "of a zero-free-parameter\nframework",
    "The prediction lies within these bounds.",
    "This is the first prescription in SQT history",
    r"\;\subset\; \text{PSL}(2,7)",
    r"60.194\,\text{fm}} \qquad \textbf{(Prediction)}",
    "| Pending verification |",
    "| **Necessary check ✓** | Confirmed |",
]
must_be_present = ["Status note — October 2026 audit corrections", "**Retirement (October 2026).**",
                   "**Outcome (October 2026).**", "*Correction (October 2026).*", "*Status (October 2026).* The Convention"]
issues = [f"still present: {s!r}" for s in must_be_gone if s in final]
issues += [f"missing: {s!r}" for s in must_be_present if final.count(s) != 1]
# every remaining paragraph that mentions zero tuned / zero free parameters must be a withdrawal or a definition
for para in final.split("\n\n"):
    low = " ".join(para.lower().split())
    if ("zero tuned" in low or "zero free" in low or "zero-free" in low or "zero-parameter" in low) and not (
            "withdrawn" in low or "not zero-parameter" in low or "not** zero" in low or "not a zero" in low
            or "**theorem** |" in low or "**zero new parameters.**" in low):
        issues.append("unscoped parameter claim: " + para[:90].replace("\n", " "))
print("checks:", issues if issues else "none")
assert not issues

rows = "\n".join(f"| {hid} | {item} | {desc.replace('|', chr(92) + '|')} |" for hid, item, desc, _, _ in HUNKS)
open(os.path.join(OUT, "paper_vii_hunk_table.md"), "w", encoding="utf-8").write(
    "| Hunk | Item (status note) | Description |\n|---|---|---|\n" + rows + "\n")
print(f"hunks: {len(HUNKS)}; table written to paper_vii_hunk_table.md")
with open(__file__, "rb") as fh:
    print("edit script md5:", hashlib.md5(fh.read()).hexdigest())
