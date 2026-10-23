"""
e8_harmonic_rigidity.py -- exploration check for the E8 harmonic-rigidity entry (Oct 22, 2026).

Claim checked. For a harmonic polynomial P of degree k > 0 on R^8, the weighted theta series
    Theta_P(q) = sum_{x in E8} P(x) q^{|x|^2/2}
is a level-1 cusp form of weight 4 + k (Hecke; Ebeling, Lattices and Codes, ch. 3).
  k = 8  : S_12 = C*Delta, so  sum_{|x|^2=2n} P(x) = tau(n) * sum_{roots} P(r)   for every n.
  k = 20 : dim S_24 = 2, so the n = 1 and n = 2 shells fix every later shell.
Test harmonics: zonal P_v(x) = |x|^k C_k^(3)(<x,v>/|x|) about a direction v (harmonic on R^8).
E8 in the even coordinate system: Z^8 or (Z+1/2)^8, coordinate sum even. Octonion norm N(x) = |x|^2/2.
Needs numpy, scipy. Runtime about a minute.
"""
import numpy as np
from scipy.special import eval_gegenbauer

def shell(n):
    """All E8 vectors with |x|^2 = 2n (n <= 7)."""
    out = []
    for vals in (np.arange(-3, 4), np.arange(-7, 8, 2) / 2):
        G = np.array(np.meshgrid(*[vals] * 8, indexing="ij")).reshape(8, -1).T
        s = G.sum(1)
        ok = (np.abs(s - np.round(s)) < 1e-9) & (np.round(s).astype(int) % 2 == 0) & (np.abs((G * G).sum(1) - 2 * n) < 1e-9)
        out.append(G[ok])
    return np.vstack(out)

def P(X, v, k):
    v = v / np.linalg.norm(v); r = np.linalg.norm(X, axis=1)
    return r ** k * eval_gegenbauer(k, 3, X @ v / r)

def qexp(N):
    """q-expansions to q^N of Delta and E4 (integer arithmetic)."""
    D = np.zeros(N + 1, dtype=object); D[0] = 1
    for m in range(1, N + 1):                       # prod (1-q^m)^24
        for _ in range(24):
            D[m:] = D[m:] - D[:N + 1 - m].copy()
    Delta = np.zeros(N + 1, dtype=object); Delta[1:] = D[:N]
    E4 = np.array([1] + [240 * sum(d ** 3 for d in range(1, m + 1) if m % d == 0) for m in range(1, N + 1)], dtype=object)
    return Delta, E4

def mul(a, b):
    N = len(a) - 1; c = np.zeros(N + 1, dtype=object)
    for i in range(N + 1):
        c[i:] = c[i:] + a[i] * b[:N + 1 - i]
    return c

ns = (1, 2, 3, 5, 7)
S = {n: shell(n) for n in ns}
sigma3 = lambda n: sum(d ** 3 for d in range(1, n + 1) if n % d == 0)
assert all(len(S[n]) == 240 * sigma3(n) for n in ns), "shell sizes"
print("shell sizes ok:", {n: len(S[n]) for n in ns})

rng = np.random.default_rng(1)
dirs = {"random v1": rng.normal(size=8), "random v2": rng.normal(size=8),
        "(1,1,1,0,0,0,0,0)": np.array([1, 1, 1, 0, 0, 0, 0, 0.])}
Delta, E4 = qexp(7); tau = {n: int(Delta[n]) for n in ns}

print("\nk=2,4,6: max |shell sum| / (shell size * max|P|)  (7-design => 0)")
for k in (2, 4, 6):
    worst = max(abs(P(S[n], v, k).sum()) / (len(S[n]) * np.abs(P(S[n], v, k)).max()) for n in ns for v in dirs.values())
    print(f"  k={k}: {worst:.1e}")

print("\nk=8: shell sum / (tau(n) * root sum)  (rigidity => 1)")
for name, v in dirs.items():
    c = P(S[1], v, 8).sum()
    print(f"  {name:18s}", " ".join(f"n={n}: {P(S[n], v, 8).sum() / (tau[n] * c):.10f}" for n in ns[1:]))

f1, f2 = mul(Delta, mul(E4, mul(E4, E4))), mul(Delta, Delta)      # basis of S_24
print("\nk=20: shells n=3,5,7 predicted from n=1,2 alone (relative error)")
for name, v in dirs.items():
    a = {n: P(S[n], v, 20).sum() for n in ns}
    A = np.array([[float(f1[1]), float(f2[1])], [float(f1[2]), float(f2[2])]])
    x, y = np.linalg.solve(A, [a[1], a[2]])
    print(f"  {name:18s}", " ".join(f"n={n}: {abs((x*float(f1[n]) + y*float(f2[n])) / a[n] - 1):.1e}" for n in (3, 5, 7)),
          f"  mixing ratio y/x = {y/x:+.6e}")
