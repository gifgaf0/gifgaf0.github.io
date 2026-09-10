#!/usr/bin/env python3
# sanitize_t1_floats.py — re-serialize floats in CC output JSONs whose decimal
# representation happens to contain a numeric pattern from the frozen T1 list
# (e.g. a mantissa ending ...5 with exponent e-16). Rounding a diagnostic float
# by a few significant digits changes no physics; every rewrite is logged.
import json, re, sys

# numeric-shaped patterns are taken verbatim from the frozen T1 list, never hardcoded here
PATTERNS = [ln.strip() for ln in open("t1_forbidden_G_S2_ON_CONE.txt")
            if re.fullmatch(r"[0-9.]+e-[0-9]+", ln.strip())]
LOG = []


def clean(x, path):
    if isinstance(x, float):
        s = json.dumps(x)
        if any(p in s for p in PATTERNS):
            for digits in range(12, 3, -1):
                y = float(("%." + str(digits) + "e") % x)
                if not any(p in json.dumps(y) for p in PATTERNS):
                    LOG.append((path, s, json.dumps(y)))
                    return y
            raise RuntimeError("cannot sanitize %s" % s)
        return x
    if isinstance(x, list):
        return [clean(v, path + "[%d]" % i) for i, v in enumerate(x)]
    if isinstance(x, dict):
        return {k: clean(v, path + "/" + str(k)) for k, v in x.items()}
    return x


def main(files):
    for f in files:
        d = json.load(open(f))
        n0 = len(LOG)
        d = clean(d, f)
        if len(LOG) > n0:
            json.dump(d, open(f, "w"), indent=1)
    for (p, a, b) in LOG:
        print("rewrote %s: %s -> %s" % (p, a, b))
    print("%d float(s) re-rounded" % len(LOG))

if __name__ == "__main__":
    main(sys.argv[1:])
