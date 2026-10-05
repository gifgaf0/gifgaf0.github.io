# Cross-check with sympy.combinatorics: PSL(2,7) as Moebius maps on P^1(F_7) = {0..6, inf=7}
from sympy.combinatorics import Permutation, PermutationGroup
p = 7
def mob(a, b, c, d):
    img = []
    for x in range(p + 1):
        if x == p:  # infinity
            img.append(p if c % p == 0 else (a * pow(c, -1, p)) % p)
        else:
            num, den = (a * x + b) % p, (c * x + d) % p
            img.append(p if den == 0 else (num * pow(den, -1, p)) % p)
    return Permutation(img)
G = PermutationGroup([mob(1, 1, 0, 1), mob(0, p - 1, 1, 0), mob(3, 0, 0, 5)])
print("order", G.order())
P2 = G.sylow_subgroup(2)
els = list(P2.elements)
from collections import Counter
print("Sylow-2 order", P2.order(), "element orders", sorted(Counter(e.order() for e in els).items()),
      "abelian?", P2.is_abelian, "-> D4 (5 involutions) vs Q8 (1 involution)")
