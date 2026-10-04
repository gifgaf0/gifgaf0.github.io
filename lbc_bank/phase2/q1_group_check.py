#!/usr/bin/env python3
"""q1_group_check.py - Phase 2, question 1 side check (exploration mode).

Published protection of a Borromean vortex link uses non-commuting vortex charges in the quaternion group Q8
(Annala, Zamora-Zamora & Mottonen, Commun. Phys. 5, 309 (2022)); non-crossing of non-Abelian vortices with charges
in the tetrahedral group T = A4 is shown by Kobayashi, Kawaguchi, Nitta & Ueda, PRL 103, 115301 (2009).
Question: which of these groups sit inside PSL(2,7) (the program's group) and inside its double cover SL(2,7)?
Method: enumerate SL(2,7) as 2x2 matrices over F_7 with det 1, and PSL(2,7) = SL(2,7)/{+-I}.
  Q8 inside G  <=>  there are a, b of order 4 with a^2 = b^2, b not in <a>, and b a b^-1 = a^-1.
  A4 inside G  <=>  there are a of order 3, b of order 2 with ab of order 3  (von Dyck (2,3,3) group = A4).
  S4 inside G  <=>  there are a of order 3, b of order 2 with ab of order 4  (von Dyck (2,3,4) group = S4).
"""
import itertools, json, hashlib

P = 7


def mul(a, b):
    return ((a[0] * b[0] + a[1] * b[2]) % P, (a[0] * b[1] + a[1] * b[3]) % P,
            (a[2] * b[0] + a[3] * b[2]) % P, (a[2] * b[1] + a[3] * b[3]) % P)


def build(projective):
    els = [m for m in itertools.product(range(P), repeat=4) if (m[0] * m[3] - m[1] * m[2]) % P == 1]
    if not projective:
        return els, (lambda m: m)
    canon = lambda m: min(m, tuple((-x) % P for x in m))
    return sorted({canon(m) for m in els}), canon


def analyse(projective):
    G, c = build(projective)
    e = c((1, 0, 0, 1))
    def order(g):
        k, x = 1, g
        while x != e:
            x, k = c(mul(x, g)), k + 1
        return k
    inv = {g: next(h for h in G if c(mul(g, h)) == e) for g in G}
    ords = {g: order(g) for g in G}
    hist = {}
    for g in G:
        hist[ords[g]] = hist.get(ords[g], 0) + 1
    o4 = [g for g in G if ords[g] == 4]
    q8 = None
    for a in o4:
        a2, ainv = c(mul(a, a)), inv[a]
        for b in o4:
            if b in (a, ainv) or c(mul(b, b)) != a2:
                continue
            if c(mul(mul(b, a), inv[b])) == ainv:
                q8 = (a, b); break
        if q8:
            break
    o3 = [g for g in G if ords[g] == 3]; o2 = [g for g in G if ords[g] == 2]
    a4 = next(((a, b) for a in o3 for b in o2 if ords[c(mul(a, b))] == 3), None)
    s4 = next(((a, b) for a in o3 for b in o2 if ords[c(mul(a, b))] == 4), None)
    return {"order": len(G), "element_orders": dict(sorted(hist.items())), "contains_Q8": q8 is not None,
            "Q8_generators": q8, "contains_A4": a4 is not None, "contains_S4": s4 is not None}


def main():
    res = {"PSL(2,7)": analyse(True), "SL(2,7)": analyse(False)}
    blob = json.dumps(res, indent=1, sort_keys=True) + "\n"
    open("q1_group_check.json", "w").write(blob)
    print(blob, end="")
    print("json md5", hashlib.md5(blob.encode()).hexdigest())


if __name__ == "__main__":
    main()
