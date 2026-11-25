"""make_manifest_028.py OUT FILE... -- manifest of SHA-256 hashes (paths relative to OUT's directory)."""
import sys, os, json, hashlib, datetime
out = sys.argv[1]; base = os.path.dirname(os.path.abspath(out))
m = {"entry": "028", "written_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
     "sha256": {os.path.relpath(os.path.abspath(f), base): hashlib.sha256(open(f, "rb").read()).hexdigest() for f in sys.argv[2:]},
     "band": "[1.05e12, 2.05e12), 2000 strata of 5e8; s_r = y_r + randrange(100_000_000); n = 12,500,000 lag-1 pairs per stratum (take n + 2 primes >= s_r, drop the first)",
     "seed_rule": "SEED = randomness of drand mainnet default-chain round R (chain 8990e7a9...b2ce, genesis 1595431050, "
                  "period 30 s), R = first round published >= 10 min after the push of the commit adding this manifest; "
                  "stratum r uses random.Random(f'{SEED}:E028:{r}'): first draw s_r offset, second draw pair index",
     "strata": 2000, "alpha_prime": 0.01 / 6, "decisive_tests": 6}
json.dump(m, open(out, "w"), indent=1); print(out, hashlib.sha256(open(out, "rb").read()).hexdigest())
