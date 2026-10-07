#!/usr/bin/env python3
"""C1 comparison of the two legs (DR-C1-1), plus a post-comparison check of leg 2's 'universal matrix' remark.

Reads leg1/c1_rank_leg1.json and leg2/leg2_results.json; applies the pre-registered rule (C1_PREREG.md §2): PASS iff both
legs give rank ≤ 112 at all four k (both primes, every seed set) and both legs' uniform controls are full rank.
Then (descriptive, written after leg 2 returned): builds leg 2's seed-independent matrix N (256 × 112,
N[16m + r][16j + c] = coefficient r of σ^j(e_m)·e_c) from the reference table and computes its rank over ℚ and mod p.
"""
import contextlib, io, json, os, sys
import flint

HERE = os.path.dirname(os.path.abspath(__file__))
L1 = json.load(open(os.path.join(HERE, "leg1", "c1_rank_leg1.json")))
L2 = json.load(open(os.path.join(HERE, "leg2", "leg2_results.json")))
out = {"rule": "C1_PREREG.md §2: PASS iff both legs give rank <= 112 at k in {8,16,32,64}, both primes, every seed set, "
               "and every uniform control is full rank"}

rows = []
for p in (911, 4294977961):
    for k in (8, 16, 32, 64):
        r1 = [r["rank"] for r in L1["runs"] if r["p"] == p and r["k"] == k]
        r2 = [r["rank_flint"] for r in L2["main_runs"] if r["prime"] == p and r["k"] == k]
        r2own = [r["rank_own"] for r in L2["main_runs"] if r["prime"] == p and r["k"] == k]
        c1 = [c["rank_uniform"] for c in L1["controls"] if c["p"] == p and c["k"] == k]
        c2 = [c["rank_flint"] for c in L2["controls"] if c["prime"] == p and c["k"] == k]
        rows.append({"p": p, "k": k, "n": 16 * k, "leg1": r1, "leg2_flint": r2, "leg2_own": r2own,
                     "control_leg1": c1, "control_leg2": c2,
                     "both_le_112": all(x <= 112 for x in r1 + r2 + r2own) and len(r1) == 3 and len(r2) == 3,
                     "controls_full": all(x == 16 * k for x in c1 + c2) and c1 and c2,
                     "exact_agreement": sorted(r1) == sorted(r2) == sorted(r2own)})
out["table"] = rows
curve1 = [(c["k"], c["rank"]) for c in L1["curve_p911"]]
curve2 = [(c["k"], c["rank_flint"]) for c in L2["curve_p911"]]
out["curve_p911"] = {"leg1": curve1, "leg2": curve2, "agree": curve1 == curve2}
out["PASS"] = all(r["both_le_112"] and r["controls_full"] for r in rows)
out["exact_ranks_agree_everywhere"] = all(r["exact_agreement"] for r in rows)

# ---- post-comparison: leg 2's universal matrix N, rebuilt from the reference table
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "tools"))
with contextlib.redirect_stdout(io.StringIO()):
    from sedenion_Fp import MULT                       # noqa: E402


def sigma_index(m, j):
    """Index of σ^j(e_m): σ sends e_i -> e_{(i mod 7)+1} and e_{i+8} -> e_{(i mod 7)+1+8}; fixes e_0, e_8."""
    for _ in range(j):
        if 1 <= m <= 7:
            m = (m % 7) + 1
        elif 9 <= m <= 15:
            m = ((m - 8) % 7) + 1 + 8
    return m


N = [[0] * 112 for _ in range(256)]
for m in range(16):
    for j in range(7):
        a = sigma_index(m, j)
        for c in range(16):
            for (idx, sgn) in MULT[a][c]:
                N[16 * m + idx][16 * j + c] += sgn
flatN = [x for row in N for x in row]
out["universal_N"] = {"shape": [256, 112],
                      "rank_Q": flint.fmpz_mat(256, 112, flatN).rank(),
                      "rank_mod_911": flint.nmod_mat(256, 112, [x % 911 for x in flatN], 911).rank(),
                      "rank_mod_spec": flint.nmod_mat(256, 112, [x % 4294977961 for x in flatN], 4294977961).rank()}
json.dump(out, open(os.path.join(HERE, "c1_compare.json"), "w"), indent=1)
for r in rows:
    print(f"p={r['p']:>10} k={r['k']:2d}  leg1 {r['leg1']}  leg2 {r['leg2_flint']} (own {r['leg2_own']})  "
          f"controls {r['control_leg1']} / {r['control_leg2']}  <=112: {r['both_le_112']}  full: {bool(r['controls_full'])}")
print("curve p=911 agree:", out["curve_p911"]["agree"], curve1)
print("exact ranks agree everywhere:", out["exact_ranks_agree_everywhere"])
print("universal N:", out["universal_N"])
print("DR-C1-1:", "PASS — WIDENED (rank <= 112 at every k tested, both legs)" if out["PASS"] else "FAIL/HALT")
