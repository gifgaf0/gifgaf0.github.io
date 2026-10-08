#!/usr/bin/env python3
"""V4.99: the one check behind the §2.22 annotation (one leg; it confirms a fact, not a verdict).

§2.22 lists the Cayley–Dickson algebras ℝ → ℂ → ℍ → 𝕆 → 𝕊 as having "1, 2, 4, 8, 16 imaginaries, summing to 30
imaginaries plus 1 real = 31". An algebra of dimension 2ⁿ has one real unit and 2ⁿ − 1 imaginary units. This
script confirms, from the dimensions alone:
  - the imaginary units are 0, 1, 3, 7, 15 (and 3, 7, 15 for ℍ, 𝕆, 𝕊, the §2.53 correction of V4.98);
  - 1 + 2 + 4 + 8 + 16 = 31 = 2⁵ − 1 is the sum of the dimensions;
  - that sum is five real units plus 26 imaginaries, not 30 imaginaries plus 1 real.
It also confirms that the V4.98 text still carries the slip exactly as quoted, on one line.
"""
import hashlib, json

dims = {"R": 1, "C": 2, "H": 4, "O": 8, "S": 16}
imag = {k: d - 1 for k, d in dims.items()}
assert [imag[k] for k in "RCHOS"] == [0, 1, 3, 7, 15]
assert [imag[k] for k in "HOS"] == [3, 7, 15]
assert sum(dims.values()) == 31 == 2 ** 5 - 1
assert sum(imag.values()) == 26 and len(dims) == 5 and 26 + 5 == 31
assert sum(imag.values()) != 30

src = "/home/claude/fold/SQT_Master_Ledger_v4_98_CANONICAL.md"
b = open(src, "rb").read()
assert hashlib.md5(b).hexdigest() == "5c50db1147527b25c87b5962b5e955ed"
quote = "ℝ → ℂ → ℍ → 𝕆 → 𝕊 (1, 2, 4, 8, 16 imaginaries, summing to 30 imaginaries plus 1 real = 31 = 2⁵ − 1 generators)"
lines = [i + 1 for i, x in enumerate(b.decode("utf-8").split("\n")) if quote in x]
assert lines == [625], lines

out = {"dimensions": dims, "imaginary_units": imag, "sum_dimensions": 31, "sum_imaginaries": 26, "real_units": 5,
       "slip_line_in_V4.98": lines[0]}
json.dump(out, open("v499_checks.json", "w"), ensure_ascii=False, indent=1)
for k, v in out.items():
    print(k, ":", v)
print("ALL CHECKS PASS")
