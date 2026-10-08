#!/usr/bin/env python3
"""B2: build the v3 DRAFT of the PSL(2,7) note as tracked changes on the author's v2.1 docx.

Input : PSL27_Spectral_Rigidity_corrected_v2_1.docx (the attachment of October 7, 2026), unpacked and run-merged.
Output: word/document.xml edited in place inside the unpacked directory; every change is a <w:ins>/<w:del> by AUTHOR.
Usage : python3 make_v3_tracked.py UNPACKED_DIR
"""
import re, sys

UNP = sys.argv[1]
PATH = f"{UNP}/word/document.xml"
AUTHOR = "Claude (audit draft)"
DATE = "2026-10-07T00:00:00Z"
x = open(PATH, encoding="utf-8").read()
_id = [9000]

def nid():
    _id[0] += 1
    return _id[0]

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def rpr(sz=None, b=False, i=False, sub=False, sup=False):
    parts = []
    if b: parts.append("<w:b/><w:bCs/>")
    if i: parts.append("<w:i/><w:iCs/>")
    if sz: parts.append(f'<w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/>')
    if sub: parts.append('<w:vertAlign w:val="subscript"/>')
    if sup: parts.append('<w:vertAlign w:val="superscript"/>')
    return f"<w:rPr>{''.join(parts)}</w:rPr>" if parts else ""

def run(text, **kw):
    return f'<w:r>{rpr(**kw)}<w:t xml:space="preserve">{esc(text)}</w:t></w:r>'

def ins(*runs_):
    return f'<w:ins w:id="{nid()}" w:author="{AUTHOR}" w:date="{DATE}">{"".join(runs_)}</w:ins>'

def dele(text, **kw):
    return (f'<w:del w:id="{nid()}" w:author="{AUTHOR}" w:date="{DATE}"><w:r>{rpr(**kw)}'
            f'<w:delText xml:space="preserve">{esc(text)}</w:delText></w:r></w:del>')

def ins_para(ppr_inner, runs_):
    """A new tracked paragraph: paragraph mark inserted, every run inside <w:ins>."""
    mark = f'<w:rPr><w:ins w:id="{nid()}" w:author="{AUTHOR}" w:date="{DATE}"/></w:rPr>'
    return f"<w:p><w:pPr>{ppr_inner}{mark}</w:pPr>{ins(*runs_)}</w:p>"

def replace_once(old, new, label):
    global x
    assert x.count(old) == 1, f"{label}: anchor count {x.count(old)}"
    x = x.replace(old, new)
    print("edit:", label)

# E1 — date line
replace_once('<w:t>revised May 2026</w:t></w:r></w:p>',
             '<w:t>revised May 2026</w:t></w:r>' + ins(run(" and October 2026", sz=22)) + '</w:p>', "E1 date line")

# E2 — abstract: prior-art sentence
replace_once('<w:t>) are supplied in an appendix.</w:t></w:r></w:p>',
             '<w:t>) are supplied in an appendix.</w:t></w:r>' + ins(run(
                 " The statements of Theorem 2.3 and Lemmas 2.8–2.9 are instances of classical facts: G acts 2-transitively "
                 "on the seven cosets of S₄, so (G, S₄) is a Gelfand pair, and the distance-transitive representations of the "
                 "groups G with PSL₂(q) ◁ G ≤ PΓL₂(q) are classified [15]; this note records the case q = 7 in spectral "
                 "language.")) + '</w:p>', "E2 abstract")

# E3 — new 'Prior art' paragraph before 'Conventions.'
conv_start = x.index('<w:p w14:paraId="6647A2F5"')
ppr = '<w:spacing w:after="120" w:line="276" w:lineRule="auto"/><w:jc w:val="both"/>'
prior = ins_para(ppr, [
    run("Prior art. ", b=True),
    run("The spectral statements of Section 2 are instances of classical facts, recorded here for q = 7. The group G acts "
        "2-transitively on the seven cosets of S₄, so the permutation character is 1 + χ"),
    run("ρ₆", sub=True),
    run(" (Lemma 2.8) and (G, S₄) is a Gelfand pair; the rigidity of Lemma 2.9 is Schur’s lemma for this rank-2 action, and "
        "the eigenvalue 2/3 is read off from the central character of the class 2A on ρ₆. Multiplicity-free permutation representations of the finite linear groups were studied by Inglis, "
        "Liebeck and Saxl [16]. Praeger, Saxl and Yokoyama [18] reduced the classification of primitive distance-transitive "
        "graphs to the almost simple and affine cases, and Faradžev and Ivanov [15] classified the distance-transitive "
        "representations of the groups G with PSL₂(q) ◁ G ≤ PΓL₂(q). The terms "),
    run("spectral rigidity", i=True), run(" and "), run("spectral crystallization", i=True),
    run(" used in this note are descriptive names for these facts; no further theorem is attached to them, and no novelty "
        "is claimed for these statements."),
])
x = x[:conv_start] + prior + x[conv_start:]
print("edit: E3 prior-art paragraph")

# E4 — Open Problem 4.4: action specified, 4A added, 104 -> 146, index-theory sentences corrected
old_op = ('<w:r><w:t xml:space="preserve">By Proposition 4.2, the quotient S⁷/G is a 7-dimensional orbifold with non-isolated '
          'singular strata: S³ strata from the 21 class-2A elements </w:t><w:lastRenderedPageBreak/><w:t>(codimension 4) and '
          'S¹ strata from classes 3A, 7A, 7B (codimension 6, total 104 elements). The Kawasaki orbifold index theorem [8] '
          'applies only to isolated singularities. The mixed-dimensional, non-isolated stratification present in S⁷/G requires '
          'either the groupoid index theory of Pflaum–Posthuma–Tang [9] or the L²-cohomology methods for singular spaces '
          '(Cheeger). The η-invariant of S⁷/PSL(2,7) is currently unknown.</w:t></w:r>')
new_op = (run("By Proposition 4.2, the quotient S⁷/G")
          + ins(run(", for the action of G on S⁷ ⊂ ℝ⁸ through its 8-dimensional irreducible representation ρ₈,"))
          + run(" is a 7-dimensional orbifold with non-isolated singular strata: S³ strata from the 21 class-2A elements "
                "(codimension 4) and S¹ strata from classes 3A, ")
          + ins(run("4A, "))
          + run("7A, 7B (codimension 6, total ")
          + dele("104") + ins(run("146"))
          + run(" elements")
          + ins(run("; the circle fixed by an element of order 4 lies inside the 3-sphere fixed by its square"))
          + run("). ")
          + dele("The Kawasaki orbifold index theorem [8] applies only to isolated singularities. The mixed-dimensional, "
                 "non-isolated stratification present in S⁷/G requires either the groupoid index theory of "
                 "Pflaum–Posthuma–Tang [9] or the L²-cohomology methods for singular spaces (Cheeger). The η-invariant of "
                 "S⁷/PSL(2,7) is currently unknown.")
          + ins(run("Because S⁷/G is the quotient of a closed manifold by a finite group, index problems on it reduce to "
                    "G-equivariant ones on S⁷: the index on G-invariant sections is the average over G of the Lefschetz "
                    "numbers given by the Atiyah–Singer fixed-point formula, whose fixed-point sets may have any dimension "
                    "[13]. Kawasaki’s index theorem for compact V-manifolds [17], whose complex case is the Riemann–Roch "
                    "theorem of [8], treats the same problem intrinsically, and groupoid methods [9] extend it further. The "
                    "η-invariant of S⁷/PSL(2,7) is correspondingly the average over G of equivariant η-invariants [14], "
                    "a finite sum over conjugacy classes computable from the fixed-point data above; it is not computed "
                    "here.")))
replace_once(old_op, new_op, "E4 Open Problem 4.4")

# E5 — Open Problem 4.1: context for the coincidence
replace_once('representation-theoretic gap in L²(G).</w:t></w:r></w:p>',
             'representation-theoretic gap in L²(G).</w:t></w:r>' + ins(run(
                 " With the generating set S, the eigenvalues of the full group Laplacian on L²(G) are 0, 2/3, 1, 8/7 and 4/3 "
                 "on ρ₁, ρ₆, ρ₈, ρ₇ and ρ₃, so δ is one of several differences among them (the next eigenvalue above 2/3 "
                 "belongs to ρ₈); the coincidence should be weighed against that choice.")) + '</w:p>', "E5 Open Problem 4.1")

# E6 — AI declaration
replace_once('takes full responsibility for the content of the published article.</w:t></w:r></w:p>',
             'takes full responsibility for the content of the published article.</w:t></w:r>' + ins(run(
                 " The October 2026 revision (version 3) was prepared with the same assistance; its new counts were checked "
                 "by explicit computation.")) + '</w:p>', "E6 AI declaration")

# E7 — Kawasaki 1979 (Osaka J. Math. 16(1) is the 1979 volume)
replace_once('<w:r><w:rPr><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr><w:t xml:space="preserve">[8]  Kawasaki, T. (1978). The Riemann-Roch theorem for complex V-manifolds. </w:t></w:r>',
             run("[8]  Kawasaki, T. (", sz=22) + dele("1978", sz=22) + ins(run("1979", sz=22))
             + run("). The Riemann-Roch theorem for complex V-manifolds. ", sz=22), "E7 reference [8] year")

# E8 — Appendix A: 'M3 ≅ D4' (M3 is the line-stabilizer S4 of Theorem 2.1)
replace_once('<w:r><w:t>We realize M</w:t></w:r><w:r><w:rPr><w:vertAlign w:val="subscript"/></w:rPr><w:t>3</w:t></w:r>'
             '<w:r><w:t xml:space="preserve"> ≅ D</w:t></w:r>',
             run("We realize ") + dele("M") + dele("3", sub=True) + dele(" ≅ ") + run("D"), "E8 Appendix A label")

# E10 — Proposition 4.2 statement: the sphere S_n (subscript) is S^n, as in its proof
replace_once('<w:r><w:rPr><w:i/><w:iCs/></w:rPr><w:t>The group G = PSL(2,7) cannot act freely on any sphere S</w:t></w:r>'
             '<w:r><w:rPr><w:i/><w:iCs/><w:vertAlign w:val="subscript"/></w:rPr><w:t>n</w:t></w:r>',
             '<w:r><w:rPr><w:i/><w:iCs/></w:rPr><w:t>The group G = PSL(2,7) cannot act freely on any sphere S</w:t></w:r>'
             + dele("n", i=True, sub=True) + ins(run("n", i=True, sup=True)), "E10 Proposition 4.2 superscript")

# E9 — references [13]-[18] after [12]
wil_end = x.index('<w:p w14:paraId="5686694A"')
wil_end = x.index("</w:p>", wil_end) + len("</w:p>")
rppr = '<w:spacing w:after="80"/><w:jc w:val="both"/>'
refs = [
    ("[13]  Atiyah, M. F., & Singer, I. M. (1968). The index of elliptic operators: III. ", "Annals of Mathematics", ", 87, 546–604."),
    ("[14]  Donnelly, H. (1978). Eta invariants for G-spaces. ", "Indiana University Mathematics Journal", ", 27, 889–918."),
    ("[15]  Faradžev, I. A., & Ivanov, A. A. (1990). Distance-transitive representations of groups G with PSL₂(q) ◁ G ≤ PΓL₂(q). ",
     "European Journal of Combinatorics", ", 11, 347–356."),
    ("[16]  Inglis, N. F. J., Liebeck, M. W., & Saxl, J. (1986). Multiplicity-free permutation representations of finite linear groups. ",
     "Mathematische Zeitschrift", ", 192, 329–337."),
    ("[17]  Kawasaki, T. (1981). The index of elliptic operators over V-manifolds. ", "Nagoya Mathematical Journal", ", 84, 135–157."),
    ("[18]  Praeger, C. E., Saxl, J., & Yokoyama, K. (1987). Distance transitive graphs and finite simple groups. ",
     "Proceedings of the London Mathematical Society", " (3), 55, 1–21."),
]
block = "".join(ins_para(rppr, [run(a, sz=22), run(j, sz=22, i=True), run(c, sz=22)]) for a, j, c in refs)
x = x[:wil_end] + block + x[wil_end:]
print("edit: E9 references [13]-[18]")

open(PATH, "w", encoding="utf-8").write(x)
print("tracked-change ids used:", 9001, "to", _id[0])
