#!/usr/bin/env python3
"""B0: check the second-sound paper v1 (approved October 4, 2026) against the brief's eight B0 items.

Locates each item's text in submission/second_sound_light_cone_v1.md and re-derives the one formula the brief
questions (item 5) symbolically. Run from the repository root:  python3 audit_followup/phase_b/B0/b0_check.py
"""
import hashlib, re, sympy as sp

V1 = "lbc_bank/paper/submission/second_sound_light_cone_v1.md"
DRAFT = "lbc_bank/paper/second_sound_light_cone_DRAFT.md"
v = open(V1, encoding="utf-8").read()
d = open(DRAFT, encoding="utf-8").read()
print("v1 md5   ", hashlib.md5(v.encode()).hexdigest(), "(APPROVAL_V1.md: 0dc9b1ea59384bdca33e9980b6cbb8ef)")
print("draft md5", hashlib.md5(d.encode()).hexdigest(), "(approved draft: a47080c26bb0a9c601912a5fa925a9f9)")

ITEMS = [
    ("1", "vortex density vertex from -δρθ̇, same F_ν weights", r"it enters Eq\. \(2\) with the same weights \$F_\\nu\$"),
    ("1", "strength fixed by the circulation quantum; core filling cannot remove it",
     r"circulation quantum fixes its strength and no filling of the core removes it"),
    ("1", "divergence-free flow drives shear through -ρ_n u̇·v_s", r"-\\rho_n\\,\\dot\{\\mathbf u\}\\cdot\\mathbf v_s"),
    ("1", "Green's-limit claims re-derived (ρ_n constant) or left open", r"With \$\\rho_n\$ constant, as in Sec\. 3, a vortex whose core shrinks"),
    ("2", "loss length anchored to proton size: ~19 orders short", r"A defect of proton size \(\$\\xi\\approx1\$ fm\) falls short by about 19 orders"),
    ("2", "abstract: defects kilometres across (text: 6×10³ m)", r"survive only if defects are kilometres across"),
    ("3", "abstract one-sided: within 10⁻²³ of shear, or faster than shear", r"or if it is faster than shear"),
    ("3", "Coleman–Glashow argument", r"the same order as Coleman and Glashow's bound"),
    ("3", "Green's-limit exception in the abstract", r"or in Green's limit of the elastic ether"),
    ("4", "chemical potential renamed μ_c; μ is the shear modulus only", r"with \$\\mu_c\$ the chemical potential"),
    ("4", "M̃ (fixed chemical potential) replaces the mixed ratio", r"\\tilde M\$ is the uniaxial modulus at fixed chemical potential"),
    ("5", "P(c*²) for the monic polynomial carries 1/ρ_n", r"P\(c_\*\^2\)=-\\rho_s\(M-\\rho\\gamma\)\^2/\(\\rho\^2\\rho_n\)"),
    ("6", "Table 2 note: window slopes vs weights at one q, up to 9%", r"by up to 9 % \(at \$g=12\.7\$"),
    ("6", "f_s filled for g ≥ 28", r"\| 44 \| 1\.393 \| 0\.0055 \|"),
    ("7", "c₁/c₂ = 34–36 giving ~10¹¹", r"c_1/c_2=34\$–\$36\$"),
    ("7", "64–80 % reconciled with the table's 0.81 (metastable row)", r"the stable-phase ranges in the text are taken at \$\\Lambda_c\$"),
    ("8", "acknowledgments: checks were AI-run", r"The checks were also made by AI agents, not by human referees"),
]
ok = True
for item, what, pat in ITEMS:
    m = re.search(pat, v)
    line = v[:m.start()].count("\n") + 1 if m else None
    ok &= bool(m)
    print(f"item {item}: {'PRESENT' if m else 'MISSING'} (v1 line {line}) — {what}")
popular = "popular" in v.lower()
ok &= not popular
print(f"item 8: {'MISSING' if popular else 'PRESENT'} — 'popular picture' gone")

# item 5: P(c*^2) for the monic polynomial and for the chi denominator
rs, rn, M, g, a = sp.symbols("rho_s rho_n M gamma alpha", positive=True)
rho = rs + rn
A = rho * a - 2 * g + M / rn
B = (rs / rn) * (a * M - g ** 2)
cstar2 = rs * M / (rho * rn)
P = sp.factor(sp.simplify(cstar2 ** 2 - A * cstar2 + B))
target_monic = -rs * (M - rho * g) ** 2 / (rho ** 2 * rn)
print("P(c*^2), monic:", P, "| equals -rho_s(M-rho*gamma)^2/(rho^2 rho_n):", sp.simplify(P - target_monic) == 0)
print("rho_n * P(c*^2) (chi denominator per q^4):", sp.factor(sp.simplify(rn * P)))
print("ALL B0 ITEMS PRESENT IN v1:", ok and sp.simplify(P - target_monic) == 0)
