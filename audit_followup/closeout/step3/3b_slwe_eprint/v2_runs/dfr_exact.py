#!/usr/bin/env python3
"""SLWE note, version 2 (October 10, 2026): exact decryption-failure rates and the worst-case decoder scan of Section 5.

Model, as in the note and in audit_followup/phase_c/C1/c1_checks.py: given r and s of weight 64 and CBD(2) noise, the
decryption noise N = <e,r> - <s,e1> + e2 is exactly CBD(258) = Bin(516, 1/2) - 258, so |N| <= 258. Decryption forms
v = (m*D + N) mod q, with D = floor(q/2) (both reference codes) or D = ceil(q/2), and decodes v by one of four rules:

  threshold  1 iff q/4 < v < 3q/4 (exact comparison)
  nearest    the bit m whose point m*D is nearer to v on Z/q (ties to 0)
  sqt_slwe   ((v + q//4) * 2 // q) % 2            -- decaps() in tools/sqt_slwe.py
  round2v    round(2*c(v)/q) % 2, c(v) in (-q/2, q/2], round half to even
                                                   -- the rule m = round(2v/q) as the scheme is written, with v
                                                      centred (as slwe_2_58_B_reference.py codes it; that file is
                                                      not in this repository)

Outputs (dfr_exact.json, and a summary on stdout):
  (1) at q = 911: the tail P(|N| > 227) and the exact failure rate of every rule and encoding, message bit uniform;
  (2) for every q from 900 to 5000: whether some m in {0, 1} and |N| <= 258 decodes wrongly, for every rule and
      encoding; hence the least q from which decryption never fails, and the least prime from there;
  (3) the failing (m, N) at q = 1033, the first q above the naive bound 4*258 = 1032.
"""
import json, math, os
from fractions import Fraction
from math import comb

HERE = os.path.dirname(os.path.abspath(__file__))
T = 258                                          # 2*(h_r + h_s + 1) at h = 64, eta = 2; N ~ CBD(T)
W = {x: comb(2 * T, T + x) for x in range(-T, T + 1)}   # P(N = x) = W[x] / 2^(2T)
TOTAL_LOG2 = 2 * T


def c(v, q):
    """Representative of v mod q in (-q/2, q/2]."""
    v %= q
    return v - q if v > q // 2 else v


def threshold(v, q, D):
    return 1 if (4 * v > q and 4 * v < 3 * q) else 0


def nearest(v, q, D):
    return 1 if abs(c(v - D, q)) < abs(c(v, q)) else 0


def sqt_slwe(v, q, D):
    return ((v + q // 4) * 2 // q) % 2


def round2v(v, q, D):
    s = c(v, q)
    fl, rem = divmod(2 * s, q)                   # 2s/q = fl + rem/q, 0 <= rem < q
    if 2 * rem < q:
        r = fl
    elif 2 * rem > q:
        r = fl + 1
    else:
        r = fl if fl % 2 == 0 else fl + 1        # exact tie: half to even, as Python's round()
    return r % 2


def round2v_reference(v, q, D):                  # literal form: int(round(2 * signed(v) / q)) % 2, exact arithmetic
    return int(round(Fraction(2 * c(v, q), q))) % 2


RULES = {"threshold": threshold, "nearest": nearest, "sqt_slwe": sqt_slwe, "round2v": round2v}
ENCODINGS = {"floor(q/2)": lambda q: q // 2, "ceil(q/2)": lambda q: (q + 1) // 2}


def failures(rule, q, D):
    return [(m, x) for m in (0, 1) for x in range(-T, T + 1) if rule((m * D + x) % q, q, D) != m]


def log2_rate(fails):
    if not fails:
        return float("-inf")
    return math.log2(sum(W[x] for (_, x) in fails)) - (TOTAL_LOG2 + 1)      # message bit uniform: factor 1/2


def is_prime(n):
    if n < 2:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True


def main():
    out = {"model": "N ~ CBD(258) = Bin(516,1/2) - 258 exactly (weight-64 r and s, CBD(2) noise)", "rules": list(RULES),
           "encodings": list(ENCODINGS)}
    # sanity: the integer form of round2v equals the literal Fraction form
    for q in range(900, 1200):
        for D in (q // 2, (q + 1) // 2):
            assert all(round2v(v, q, D) == round2v_reference(v, q, D) for v in range(q))
    out["round2v_integer_form_checked_against_literal_form"] = "q = 900..1199, every v"

    # (1) q = 911
    q = 911
    tail = math.log2(2 * sum(W[x] for x in range(228, T + 1))) - TOTAL_LOG2
    out["q911"] = {"log2_P(|N|>227)": tail, "log2_failure_rate": {}}
    print(f"q = 911: log2 P(|N| > 227) = {tail:.4f}")
    for rn, rule in RULES.items():
        for en, Df in ENCODINGS.items():
            lr = log2_rate(failures(rule, q, Df(q)))
            out["q911"]["log2_failure_rate"][f"{rn} | m*{en}"] = lr
            print(f"  failure rate, {rn:9s} with m*{en:10s}: 2^{lr:.4f}")

    # (2) worst case for q = 900..5000
    QMAX = 5000
    scan = {}
    for rn, rule in RULES.items():
        for en, Df in ENCODINGS.items():
            bad = [q for q in range(900, QMAX + 1) if failures(rule, q, Df(q))]
            safe_from = max(bad) + 1
            scan[f"{rn} | m*{en}"] = {"failing_q_in_1025_1199": [q for q in bad if 1025 <= q <= 1199],
                                      "largest_failing_q": max(bad), "never_fails_for_q_from": safe_from}
            print(f"  {rn:9s} m*{en:10s}: largest failing q = {max(bad)}; failing q in 1025..1199: "
                  f"{[q for q in bad if 1025 <= q <= 1199][-6:]} (last six)")
    overall = max(v["never_fails_for_q_from"] for v in scan.values())
    first_prime = next(n for n in range(overall, overall + 100) if is_prime(n))
    out["worst_case_scan"] = {"q_range": [900, QMAX], "by_rule": scan,
                              "never_fails_under_every_rule_and_encoding_for_q_from": overall,
                              "least_prime_from_there": first_prime,
                              "naive_bound_from_258_lt_q_over_4": "q > 1032"}
    print(f"never fails under every rule and encoding for q >= {overall} (checked to {QMAX}); "
          f"least such prime: {first_prime}")

    # (3) q = 1033
    q = 1033
    out["q1033"] = {"is_prime": is_prime(q), "failing_(m,N)": {}}
    for rn, rule in RULES.items():
        for en, Df in ENCODINGS.items():
            f = failures(rule, q, Df(q))
            out["q1033"]["failing_(m,N)"][f"{rn} | m*{en}"] = f
    print("q = 1033 (prime: %s), failing (m, N):" % is_prime(q),
          {k: v for k, v in out["q1033"]["failing_(m,N)"].items()})
    with open(os.path.join(HERE, "dfr_exact.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1)
        fh.write("\n")


if __name__ == "__main__":
    main()
