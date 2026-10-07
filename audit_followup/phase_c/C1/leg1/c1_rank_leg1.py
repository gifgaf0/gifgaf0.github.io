#!/usr/bin/env python3
"""C1 leg 1 — rank of the Singer-orbit SLWE public matrix at k = 8, 16, 32, 64 (pre-registration C1_PREREG.md §2).

The object is the reference construction itself: the sedenion table of tools/sedenion_Fp.py (imported unchanged) and the
Singer action and row-orbit rule of tools/sqt_slwe.py (apply_singer / singer_orbit, re-stated here line for line because
importing sqt_slwe.py fixes its prime at 911). The flattening is sqt_slwe.rank_flat's: block (i, j) of M is the 16×16
left-multiplication matrix of A[i][j], column c = A[i][j]·e_c. Ranks are exact, over F_p, via python-flint nmod_mat.
"""
import json, os, random, sys, time
import flint

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "..", "tools"))
import contextlib, io
with contextlib.redirect_stdout(io.StringIO()):          # the reference prints while building its table
    from sedenion_Fp import MULT, DIM                     # noqa: E402
assert DIM == 16

P_TOY, Q_SPEC = 911, 4294977961


def apply_singer(v):                                      # tools/sqt_slwe.py, verbatim logic
    result, temp = list(v), list(v)
    for old in range(1, 8):
        new = (old % 7) + 1
        result[new] = temp[old]
        result[new + 8] = temp[old + 8]
    return result


def singer_orbit(seed, k):
    orbit, cur = [seed[:]], seed[:]
    for _ in range(k - 1):
        cur = apply_singer(cur)
        orbit.append(cur[:])
    return orbit[:k]


def lmm(x, p):
    """16×16 left-multiplication matrix of x: column c is x·e_c."""
    B = [[0] * DIM for _ in range(DIM)]
    for a in range(DIM):
        if x[a]:
            for c in range(DIM):
                for (idx, sgn) in MULT[a][c]:
                    B[idx][c] = (B[idx][c] + sgn * x[a]) % p
    return B


def flatten(A, p):
    k = len(A)
    n = k * DIM
    rows = [[0] * n for _ in range(n)]
    for i in range(k):
        for j in range(k):
            B = lmm(A[i][j], p)
            for r in range(DIM):
                rows[i * DIM + r][j * DIM:(j + 1) * DIM] = B[r]
    return rows


def rank_mod(rows, p):
    n = len(rows)
    return flint.nmod_mat(n, n, [x for row in rows for x in row], p).rank()


def blocks_repeat(rows, k):
    """True if column block j equals column block j+7 for every j with j+7 < k."""
    for j in range(k - 7):
        for row in rows:
            if row[j * DIM:(j + 1) * DIM] != row[(j + 7) * DIM:(j + 8) * DIM]:
                return False
    return True


def main():
    out = {"construction": "tools/sqt_slwe.py keygen (Singer-orbit rows) + rank_flat flattening; table tools/sedenion_Fp.py",
           "runs": [], "controls": [], "curve_p911": []}
    for p in (P_TOY, Q_SPEC):
        for k in (8, 16, 32, 64):
            for t in range(3):
                rng = random.Random(f"C1-leg1-{p}-{k}-{t}")
                A = [singer_orbit([rng.randrange(p) for _ in range(DIM)], k) for _ in range(k)]
                t0 = time.time()
                M = flatten(A, p)
                rk = rank_mod(M, p)
                out["runs"].append({"p": p, "k": k, "trial": t, "n": 16 * k, "rank": rk,
                                    "blocks_period_7": blocks_repeat(M, k), "seconds": round(time.time() - t0, 1)})
                print(f"p={p} k={k:2d} trial={t} n={16*k:4d} rank={rk:4d} period7={out['runs'][-1]['blocks_period_7']}",
                      flush=True)
            rng = random.Random(f"C1-leg1-control-{p}-{k}")
            U = [[[rng.randrange(p) for _ in range(DIM)] for _ in range(k)] for _ in range(k)]
            rk = rank_mod(flatten(U, p), p)
            out["controls"].append({"p": p, "k": k, "n": 16 * k, "rank_uniform": rk})
            print(f"p={p} k={k:2d} CONTROL uniform rank={rk} of {16*k}", flush=True)
    for k in range(1, 11):                                # descriptive: where the collapse starts
        rng = random.Random(f"C1-leg1-curve-{k}")
        A = [singer_orbit([rng.randrange(P_TOY) for _ in range(DIM)], k) for _ in range(k)]
        out["curve_p911"].append({"k": k, "n": 16 * k, "rank": rank_mod(flatten(A, P_TOY), P_TOY)})
    print("curve p=911 (k, rank):", [(c["k"], c["rank"]) for c in out["curve_p911"]])
    ranks = [r["rank"] for r in out["runs"]]
    out["verdict_inputs"] = {"max_rank": max(ranks), "all_le_112": all(x <= 112 for x in ranks),
                             "all_controls_full": all(c["rank_uniform"] == c["n"] for c in out["controls"]),
                             "distinct_ranks": sorted(set(ranks))}
    print("verdict inputs:", out["verdict_inputs"])
    json.dump(out, open(os.path.join(HERE, "c1_rank_leg1.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
