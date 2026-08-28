#!/usr/bin/env python3
# gl23_class_level_addon.py — chat-side add-on for schema v1.1 field GL23_transposition_class_size_GL.
# The chat instrument (2f0fa8f4) asserts the PGL-level fact only (size-6 order-2 class, line 449).
# This computes, independently and exhaustively over F_3, the GL(2,3) preimage count of that class.
import itertools
F = 3
def mul(a, b):
    return ((a[0]*b[0]+a[1]*b[2]) % F, (a[0]*b[1]+a[1]*b[3]) % F,
            (a[2]*b[0]+a[3]*b[2]) % F, (a[2]*b[1]+a[3]*b[3]) % F)
I = (1,0,0,1)
GL = [m for m in itertools.product(range(F), repeat=4) if (m[0]*m[3]-m[1]*m[2]) % F]
assert len(GL) == 48
neg = lambda m: tuple((-x) % F for x in m)
Z = {I, neg(I)}
def order(m, mulf, ident):
    k, x = 1, m
    while x != ident: x = mulf(x, m); k += 1
    return k
# PGL = GL / {±I}: represent each coset by its min element
coset = lambda m: min(m, neg(m))
PGL = sorted({coset(m) for m in GL}); assert len(PGL) == 24
pmul = lambda a, b: coset(mul(a, b))
pI = coset(I)
# conjugacy classes in PGL
classes = []; seen = set()
for g in PGL:
    if g in seen: continue
    inv = {h for h in GL if mul(h, g) == I or mul(h, g) == neg(I)}  # unused guard
    cl = set()
    for h in GL:
        # h g h^-1 in PGL: find h^-1
        hinv = next(k for k in GL if mul(h, k) == I)
        cl.add(coset(mul(mul(h, g), hinv)))
    classes.append(cl); seen |= cl
sizes = sorted((len(c), order(next(iter(c)), pmul, pI)) for c in classes)
print("PGL(2,3) class (size, order):", sizes)
assert sizes == [(1,1),(3,2),(6,2),(6,4),(8,3)], "PGL(2,3) is S4 with the standard class data"
transp = next(c for c in classes if len(c) == 6 and order(next(iter(c)), pmul, pI) == 2)
pre = [m for m in GL if coset(m) in transp]
n_GL = len(pre)
n_inv = sum(1 for m in pre if order(m, mul, I) == 2)
print("GL(2,3) preimages of the size-6 PGL transposition class:", n_GL, "| genuine involutions among them:", n_inv)
assert n_GL == 12 and n_inv == 12   # H-S8: expected 6 at first writing; both lifts m, -m of an involution are involutions
print("RESULT GL23_transposition_class_size_PGL=6 GL23_transposition_class_size_GL=12 (all 12 preimages are involutions — the 2S4^- fingerprint a fortiori)")
