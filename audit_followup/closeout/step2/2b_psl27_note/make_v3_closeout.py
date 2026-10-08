#!/usr/bin/env python3
"""Step 2b: three more tracked edits on the v3 draft of the PSL(2,7) note (after make_v3_tracked.py).

E11 abstract: "and establish four main results" → "and record four main results"
E12 abstract: "we establish via Smith's theorem" → "we record via Smith's theorem"
E13 title: "Spectral Rigidity and Crystallization / in the Coset Geometry of PSL(2,7)" → proposal A (or B)
E14 running head (header1.xml) to match
Every change is a <w:ins>/<w:del> by "Claude (audit draft)". Usage: python3 make_v3_closeout.py UNPACKED_DIR [A|B]
"""
import sys

UNP, CHOICE = sys.argv[1], (sys.argv[2] if len(sys.argv) > 2 else "A")
PATH = f"{UNP}/word/document.xml"
AUTHOR, DATE = "Claude (audit draft)", "2026-10-08T00:00:00Z"
TITLES = {"A": ("The Seven-Point Coset Geometry of PSL(2,7):", "Spectral Gap, Cheeger Constant and a Smith Obstruction"),
          "B": ("PSL(2,7) on Seven Points:", "A Spectral Record of the Gelfand Pair (PSL(2,7), S₄)")}
x = open(PATH, encoding="utf-8").read()
assert "w:id=\"91" not in x, "ids 91xx already used"
_id = [9100]


def nid():
    _id[0] += 1
    return _id[0]


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def r(text, rpr=""):
    return f'<w:r>{rpr}<w:t xml:space="preserve">{esc(text)}</w:t></w:r>'


def ins(text, rpr=""):
    return f'<w:ins w:id="{nid()}" w:author="{AUTHOR}" w:date="{DATE}">{r(text, rpr)}</w:ins>'


def dele(text, rpr=""):
    return (f'<w:del w:id="{nid()}" w:author="{AUTHOR}" w:date="{DATE}"><w:r>{rpr}'
            f'<w:delText xml:space="preserve">{esc(text)}</w:delText></w:r></w:del>')


def once(old, new, label):
    global x
    assert x.count(old) == 1, f"{label}: anchor count {x.count(old)}"
    x = x.replace(old, new)
    print("edit:", label)


# E11, E12: the abstract's verb
A1 = ('<w:r><w:t xml:space="preserve"> &lt; G of index 7, and establish four main results. First, among the maximal '
      'subgroups of G, the subgroup S</w:t></w:r>')
once(A1, r(" < G of index 7, and ") + dele("establish") + ins("record") +
     r(" four main results. First, among the maximal subgroups of G, the subgroup S"), "E11 abstract: establish → record")
A2 = ('<w:r><w:t xml:space="preserve"> ≤ 2h holds, with neither bound attained (Theorem 3.3). As a separate structural '
      'result, we establish via Smith’s theorem that PSL(2,7) cannot act freely on any sphere, so that S⁷/PSL(2,7) is an '
      'orbifold, not a manifold. Explicit generators for the flag stabilizer D</w:t></w:r>')
once(A2, r(" ≤ 2h holds, with neither bound attained (Theorem 3.3). As a separate structural result, we ") +
     dele("establish") + ins("record") +
     r(" via Smith’s theorem that PSL(2,7) cannot act freely on any sphere, so that S⁷/PSL(2,7) is an orbifold, not a "
       "manifold. Explicit generators for the flag stabilizer D"), "E12 abstract: establish → record")

# E13: the title (two centred lines)
RPR = '<w:rPr><w:b/><w:bCs/><w:sz w:val="36"/><w:szCs w:val="36"/></w:rPr>'
t1, t2 = TITLES[CHOICE]
once(f'<w:r>{RPR}<w:t>Spectral Rigidity and Crystallization</w:t></w:r>',
     dele("Spectral Rigidity and Crystallization", RPR) + ins(t1, RPR), f"E13 title line 1 ({CHOICE})")
once(f'<w:r>{RPR}<w:t>in the Coset Geometry of PSL(2,7)</w:t></w:r>',
     dele("in the Coset Geometry of PSL(2,7)", RPR) + ins(t2, RPR), f"E13 title line 2 ({CHOICE})")
open(PATH, "w", encoding="utf-8").write(x)

# E14: the running head (header1.xml), shortened to match the title
RUNNING = {"A": "The Seven-Point Coset Geometry of PSL(2,7)", "B": "PSL(2,7) on Seven Points"}
HP = f"{UNP}/word/header1.xml"
h = open(HP, encoding="utf-8").read()
HRPR = '<w:rPr><w:i/><w:iCs/><w:sz w:val="18"/><w:szCs w:val="18"/></w:rPr>'
old_h = f'<w:r>{HRPR}<w:t>Spectral Rigidity and Crystallization in PSL(2,7)</w:t></w:r>'
assert h.count(old_h) == 1, "E14 anchor"
h = h.replace(old_h, dele("Spectral Rigidity and Crystallization in PSL(2,7)", HRPR) + ins(RUNNING[CHOICE], HRPR))
open(HP, "w", encoding="utf-8").write(h)
print(f"edit: E14 running head ({CHOICE})")
print("tracked-change ids used: 9101 to", _id[0])
