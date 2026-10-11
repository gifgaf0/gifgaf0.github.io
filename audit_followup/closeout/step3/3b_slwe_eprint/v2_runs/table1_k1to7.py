#!/usr/bin/env python3
"""SLWE note, version 2 (October 10, 2026): the k = 1..7 columns of Table 1, run the way the k = 8, 16, 32, 64
columns were (three seed sets per case and a uniform control, at both primes, in both implementations).

Version 1 of the note said Table 1 had "three seed sets per case and a uniform control". In the repository that held
only for k in {8, 16, 32, 64}; for k = 1..7 each leg had one seed list at p = 911 and no control. This script closes
that gap. Both legs of audit_followup/phase_c/C1 are imported unchanged and their own randomness schemes are extended
to the new k (leg 1: random.Random("C1-leg1-<p>-<k>-<t>"); leg 2: rng_for("singer|p=<p>|k=<k>|set=<s>")). None of these
tags was used before, because the pre-registered runs covered only k in {8, 16, 32, 64}.

Run:  python3 table1_k1to7.py      (writes table1_k1to7.json next to this script; prints a summary)
"""
import importlib.util, json, os, platform, random, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
C1 = os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "phase_c", "C1"))


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


leg1 = load("c1_rank_leg1", os.path.join(C1, "leg1", "c1_rank_leg1.py"))
leg2 = load("c1_leg2", os.path.join(C1, "leg2", "c1_leg2.py"))
import flint                                                  # noqa: E402  (after the legs, which import it too)

PRIMES = (911, 4294977961)
KS = tuple(range(1, 8))
N_SETS = 3
TABLE1_SINGER = {1: 16, 2: 32, 3: 48, 4: 64, 5: 72, 6: 74, 7: 76}   # the values printed in Table 1


def quiet(_msg=""):
    pass


def main():
    t0 = time.time()
    sparse = {p: leg2.structure_sparse(p) for p in PRIMES}
    out = {"purpose": "Table 1, k = 1..7: three seed sets and a uniform control per (p, k), in both implementations",
           "legs": {"leg1": "audit_followup/phase_c/C1/leg1/c1_rank_leg1.py (reference construction, flint rank)",
                    "leg2": "audit_followup/phase_c/C1/leg2/c1_leg2.py (blind; flint rank and own exact elimination)"},
           "environment": {"python": platform.python_version(), "python_flint": flint.__version__},
           "rows": []}
    ok = True
    for p in PRIMES:
        for k in KS:
            row = {"p": p, "k": k, "n": 16 * k}
            r1 = []
            for t in range(N_SETS):
                rng = random.Random(f"C1-leg1-{p}-{k}-{t}")
                A = [leg1.singer_orbit([rng.randrange(p) for _ in range(16)], k) for _ in range(k)]
                r1.append(leg1.rank_mod(leg1.flatten(A, p), p))
            rng = random.Random(f"C1-leg1-control-{p}-{k}")
            U = [[[rng.randrange(p) for _ in range(16)] for _ in range(k)] for _ in range(k)]
            c1 = leg1.rank_mod(leg1.flatten(U, p), p)
            r2, r2own = [], []
            for s in range(N_SETS):
                rng = leg2.rng_for("singer|p=%d|k=%d|set=%d" % (p, k, s))
                seeds = [leg2.uniform_vector(rng, p) for _ in range(k)]
                rec = leg2.singer_run(p, k, seeds, sparse[p], quiet, "singer set %d" % s)
                r2.append(rec["rank_flint"])
                r2own.append(rec["rank_own"])
            crec = leg2.control_run(p, k, sparse[p], quiet)
            row.update({"leg1_singer": r1, "leg1_uniform": c1,
                        "leg2_singer_flint": r2, "leg2_singer_own": r2own,
                        "leg2_uniform_flint": crec["rank_flint"], "leg2_uniform_own": crec["rank_own"]})
            want = TABLE1_SINGER[k]
            row["matches_table1"] = (all(x == want for x in r1 + r2 + r2own)
                                     and c1 == crec["rank_flint"] == crec["rank_own"] == 16 * k)
            ok &= row["matches_table1"]
            out["rows"].append(row)
            print(f"p={p:<10d} k={k}  n={16*k:<4d} leg1 {r1} control {c1:<4d} | leg2 {r2} (own {r2own}) "
                  f"control {crec['rank_flint']} (own {crec['rank_own']})  matches Table 1: {row['matches_table1']}",
                  flush=True)
    out["all_match_table1"] = ok
    out["seconds"] = round(time.time() - t0, 1)
    print("all rows match Table 1 (Singer row 16, 32, 48, 64, 72, 74, 76; uniform row 16k):", ok)
    with open(os.path.join(HERE, "table1_k1to7.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1)
        fh.write("\n")


if __name__ == "__main__":
    main()
