"""Sieve mod-455 primes in a given range.

A "mod-455 prime" satisfies p ≡ 1 (mod 455). Since 455 = 5 · 7 · 13,
this is equivalent to p ≡ 1 (mod 5), p ≡ 1 (mod 7), p ≡ 1 (mod 13);
i.e., F_p× contains a Z₅, a Z₇, and a Z₁₃ subgroup.

Output: tools/mod455_primes.txt, one line per prime, with the
factorisation of p − 1 inline:

    p = <prime>     p-1 = <factor1> * <factor2> * ...

Brief 02 parameter-fix Task 1: range [2000, 50000].
"""

from __future__ import annotations

from pathlib import Path


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0:
        return False
    r = int(n ** 0.5) + 1
    for d in range(3, r + 1, 2):
        if n % d == 0:
            return False
    return True


def factor(n: int) -> list[tuple[int, int]]:
    out = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            e = 0
            while n % d == 0:
                n //= d
                e += 1
            out.append((d, e))
        d += 1
    if n > 1:
        out.append((n, 1))
    return out


def fmt_factor(facs: list[tuple[int, int]]) -> str:
    return " * ".join(f"{p}" if e == 1 else f"{p}^{e}" for p, e in facs)


def main() -> int:
    lo, hi = 2000, 50000
    primes: list[int] = []
    p = 1 + 455 * (lo // 455)   # smallest p ≡ 1 (mod 455) at or below lo
    if p < lo:
        p += 455
    while p <= hi:
        if is_prime(p):
            primes.append(p)
        p += 455

    out_path = Path("tools/mod455_primes.txt")
    lines = [
        f"# mod-455 primes in [{lo}, {hi}], {len(primes)} found",
        "# Each line: p, with the factorisation of p-1 (always divisible by 455 = 5*7*13).",
        "",
    ]
    for p in primes:
        lines.append(f"{p:>6d}    p-1 = {fmt_factor(factor(p - 1))}")
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {out_path}: {len(primes)} primes")
    print("first 10:", primes[:10])
    print("first prime > 5000:", next((q for q in primes if q > 5000), None))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
