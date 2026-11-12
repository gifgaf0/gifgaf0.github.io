"""make_manifest_026.py -- write manifest26.json (run once at the freeze, after Matthew's approval).
Usage: make_manifest_026.py OUT.json [R64_RUNS R128_RUNS]   (run counts default to the entry's 10,000 / 20,000)
"""
import sys, json, hashlib, datetime as dt
FILES = ["entry_026.md", "predict_026.py", "ladder_026.py", "uniform_shift_026.py", "make_pred_026.py", "pred_026.json",
         "gen_E_026.c", "check_E_026.py", "gen_R_026.py", "build_026.py", "analyze_026.py", "make_dry_026.py",
         "beacon_round_026.py", "verify_beacon_026.py",
         "ladders_026.log", "ushift_026.log", "pred_026.log", "additivity_026.log", "conventions_check_026.log",
         "validate_predictor_026.log", "dryrun_null_026.log", "dryrun_effect_026.log", "beacon_tools_test_026.log",
         "drift_check_026.log", "manifest_check_test_026.log", "build_smoke_026.log", "build_negative_026.log",
         "make_manifest_026.py", "reconcile_026.py", "reconcile_026.log", "range_weight_check_026.py",
         "range_weight_check_026.log", "archive/los216.py", "archive/pair_absorb.py"]
out = sys.argv[1]; n64, n128 = (int(sys.argv[2]), int(sys.argv[3])) if len(sys.argv) > 3 else (10_000, 20_000)
m = {"entry": "026", "written_utc": dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
     "approved_by": "Matthew Gifford",
     "sha256": {f: hashlib.sha256(open(f, 'rb').read()).hexdigest() for f in FILES},
     "ranges": {"E": "all primes 1e12 <= p < 1.02e12, blocks of 1e8",
                "R64": f"runs 0..{n64 - 1}, 64-bit starts", "R128": f"runs 0..{n128 - 1}, 128-bit starts"},
     "runs": {"R64": n64, "R128": n128},
     "seed_rule": "SEED = randomness of drand mainnet default-chain round R (chain 8990e7a9...b2ce, genesis 1595431050, "
                  "period 30 s), R = first round published >= 10 min after the push of the commit adding this manifest; "
                  "run r of arm R{b} uses random.Random(f'{SEED}:R{b}:{r}')",
     "alpha_prime": 0.01 / 21, "decisive_tests": 21}
json.dump(m, open(out, 'w'), indent=1)
print(out, hashlib.sha256(open(out, 'rb').read()).hexdigest())
