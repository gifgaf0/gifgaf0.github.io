#!/usr/bin/env python3
"""C1 checks that need no second leg (C1_PREREG.md §4, plus the §3.05 carry-over for §§2.59–2.61).

(1) DR-C1-3: worst-case decryption-noise bound |N| ≤ B_e·h_r + B_e1·h_s + B_e2 against q/4, for CBD(η) noise and for the
    §2.58.B confined kernel noise (B = the largest entry of σ·(α0 k0 + … + α3 k3), σ = 2, α ∈ {−1,0,1}^4, computed from
    the reduced-echelon kernel basis of L_z for all 84 two-term cross-edge zero divisors z).
(2) The Gaussian-tail figure §2.66.1 quotes, recomputed, to show where it comes from.
(3) §3.05 carry-over: on the actual kernels, how many of the 21 interior pairs obey the 'sum-to-14 complement' rule that
    §§2.59–2.61 use (a + b + c + d = 14 for each partner pair {c, d}).
Sedenion table: tools/sedenion_Fp.py, imported unchanged. Exact linear algebra: python-flint nmod_mat.
"""
import contextlib, io, itertools, json, math, os, sys
import flint

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "tools"))
with contextlib.redirect_stdout(io.StringIO()):
    from sedenion_Fp import MULT                          # noqa: E402

Q = 4294977961
out = {}


def lmm(x, p):
    B = [[0] * 16 for _ in range(16)]
    for a in range(16):
        if x[a] % p:
            for c in range(16):
                for (idx, sgn) in MULT[a][c]:
                    B[idx][c] = (B[idx][c] + sgn * x[a]) % p
    return B


def kernel_rref(B, p):
    """Reduced-echelon basis of the right kernel {v : B v = 0} over F_p (free variables set to unit vectors)."""
    M = flint.nmod_mat(16, 16, [x for row in B for x in row], p).rref()[0]
    rows = [[int(M[i, j]) for j in range(16)] for i in range(16)]
    pivots, r = [], 0
    for i in range(16):
        nz = [j for j in range(16) if rows[i][j]]
        if nz:
            pivots.append(nz[0])
    free = [j for j in range(16) if j not in pivots]
    basis = []
    for f in free:
        v = [0] * 16
        v[f] = 1
        for i, pc in enumerate(pivots):
            v[pc] = (-rows[i][f]) % p
        basis.append(v)
    return basis


def centred(x, p):
    x %= p
    return x - p if x > p // 2 else x


# ---- the 84 two-term cross-edge zero divisors x = e_a + s·e_b, a in 1..7, b in 9..15, with a 4-dim kernel
p = 911
zds = []
for a in range(1, 8):
    for b in range(9, 16):
        for s in (1, -1):
            x = [0] * 16
            x[a], x[b] = 1, s % p
            ker = kernel_rref(lmm(x, p), p)
            if len(ker) == 4:
                zds.append((a, b, s, ker))
out["two_term_cross_edge_zds_with_4dim_kernel"] = len(zds)

# ---- (1) confined-noise entry bound: max |entry| of 2·Σ α_j k_j over α ∈ {−1,0,1}^4, all kernels
maxent, maxent_basis = 0, 0
for (_, _, _, ker) in zds:
    maxent_basis = max(maxent_basis, max(abs(centred(v, p)) for k in ker for v in k))
    for alpha in itertools.product((-1, 0, 1), repeat=4):
        e = [2 * sum(al * k[t] for al, k in zip(alpha, ker)) for t in range(16)]
        maxent = max(maxent, max(abs(centred(v, p)) for v in e))
out["kernel_basis_max_abs_entry"] = maxent_basis
out["confined_noise_max_abs_entry_sigma2"] = maxent

h_r = h_s = 64
rows = []
for label, Be, Be1, Be2 in (("CBD eta=2 (spec)", 2, 2, 2), ("CBD eta=512 (top of the §2.66.1 sweep)", 512, 512, 512),
                            ("confined kernel noise, sigma=2 (e, e1), CBD2 e2", maxent, maxent, 2)):
    bound = Be * h_r + Be1 * h_s + Be2
    rows.append({"noise": label, "worst_case_|N|": bound, "q_spec/4": Q / 4, "DFR_zero_at_spec": bound < Q / 4,
                 "margin_factor": round((Q / 4) / bound, 1), "q_min_for_DFR_zero": 4 * bound + 1,
                 "q911/4": 911 / 4, "DFR_zero_at_911": bound < 911 / 4})
out["worst_case_bounds"] = rows

# ---- (2) the Gaussian-tail figure of §2.66.1, recomputed (Var N = (η/2)(h_s + h_r + 1) = 129 at η = 2)
sigma = math.sqrt(1.0 * (h_s + h_r + 1))
z = (Q / 4) / sigma
out["gaussian_tail_as_in_2_66_1"] = {"sigma_N": round(sigma, 2), "z": z,
                                    "log2_DFR_gaussian": -(z * z) / (2 * math.log(2)),
                                    "support_of_N": 258, "note": "the tail is evaluated ~4e6 times beyond the support"}

# ---- (3) the 'sum-to-14 complement' rule against the actual kernels
pairs = {}
for (a, b, s, ker) in zds:
    supp = sorted({t for k in ker for t in range(16) if k[t] % p})
    labels = sorted({t if t < 8 else t - 8 for t in supp})
    pairs.setdefault(frozenset((a, b - 8)), set()).update(labels)
fano_lines = [{1, 2, 3}, {1, 4, 5}, {1, 7, 6}, {2, 4, 6}, {2, 5, 7}, {3, 4, 7}, {3, 6, 5}]   # e_i e_j = ±e_(i xor j)
res = []
for pr, lab in sorted(pairs.items(), key=lambda kv: sorted(kv[0])):
    a, b = sorted(pr)
    c = a ^ b                                             # third point of the line through a, b
    partners = [tuple(sorted((x, c ^ x))) for x in range(1, 8) if x not in (a, b, c) and x < (c ^ x)]
    ok = all(a + b + sum(pp) == 14 for pp in partners)
    res.append({"pair": [a, b], "third_point": c, "kernel_support_labels": sorted(lab), "co_line_partners": partners,
                "sum_to_14_holds": ok})
out["sum_to_14_rule"] = {"pairs_checked": len(res), "holds": sum(r["sum_to_14_holds"] for r in res),
                         "fails": [r["pair"] for r in res if not r["sum_to_14_holds"]],
                         "partners_equal_kernel_support": all(
                             set(r["kernel_support_labels"]) - {0} == {x for pp in r["co_line_partners"] for x in pp}
                             or set(r["kernel_support_labels"]) == {x for pp in r["co_line_partners"] for x in pp}
                             for r in res),
                         "detail": res}
# ---- (4) exact tail for CBD noise: given r and s, each e_j·r_j and s_j·e1_j is an independent CBD(η) draw, so
#      N = <e,r> − <s,e1> + e2 is exactly CBD(η(h_r + h_s + 1)) = Bin(2T, 1/2) − T with T = 258 at η = 2, h = 64.
#      Decryption (the reference's branchless rounding) fails iff |N| exceeds about q/4.
T = 2 * (h_r + h_s + 1)
from math import comb
def log2_tail(t_excl):
    """log2 P(|N| > t_excl) for N = Bin(2T,1/2) − T (exact big-integer sum)."""
    if t_excl >= T:
        return float("-inf")
    num = 2 * sum(comb(2 * T, T + x) for x in range(t_excl + 1, T + 1))
    return math.log2(num) - 2 * T
out["exact_cbd_tail"] = {"N_distribution": f"CBD({T}) = Bin({2*T},1/2) - {T}",
                         "log2_P(|N|>227)_q911": log2_tail(227),
                         "log2_P(|N|>682)_q2731": log2_tail(682),
                         "log2_P(|N|>q_spec/4)": "-inf (support ends at 258)"}
json.dump(out, open(os.path.join(HERE, "c1_checks.json"), "w"), indent=1)
print("exact CBD tail:", out["exact_cbd_tail"])
print("zero divisors with a 4-dim kernel:", out["two_term_cross_edge_zds_with_4dim_kernel"])
print("kernel basis max |entry|:", maxent_basis, "| confined noise (σ=2) max |entry|:", maxent)
for r in rows:
    print(r)
g = out["gaussian_tail_as_in_2_66_1"]
print(f"Gaussian tail as in §2.66.1: σ_N = {g['sigma_N']}, z = {g['z']:.3e}, log2 DFR = {g['log2_DFR_gaussian']:.3e}")
s14 = out["sum_to_14_rule"]
print(f"sum-to-14 rule: holds for {s14['holds']} of {s14['pairs_checked']} interior pairs; fails for {s14['fails']}")
print("kernel supports = co-line partners of the third point:", s14["partners_equal_kernel_support"])
