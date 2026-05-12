"""Empirical decryption-failure-rate scaling for Module-SLWE.

Per Brief 02 §3 (OP-C work). Runs SLWE keygen+encaps+decaps at increasing
module rank ``k`` and reports the empirical DFR for each parameter point.

Currently *not runnable* end-to-end: the wrapper's ``"toy"`` mode is still
a stub pending the upload of ``sqt_slwe__1_.py`` (see tools/QUESTIONS.md).
The script is wired so it will start producing real numbers as soon as
the toy and "scaled" modes are available; nothing in the surrounding
testbed needs to change when that happens.

Outputs:
- ``tools/dfr_scaling_results.md`` — the data points and a linear fit of
  ``log(DFR)`` vs. ``k`` (least-squares, slope reported in bits per unit k).

Stop conditions honoured:
- If a single parameter point exceeds 30 minutes of wall clock, we cut the
  trial count for that point and record the truncation.
- If the wrapper raises ``NotImplementedError`` (i.e. toy/scaled mode not
  wired yet), we exit cleanly with a non-zero return code so CI doesn't
  silently report success.
"""

from __future__ import annotations

import argparse
import math
import statistics
import time
from pathlib import Path
from typing import Iterable

from hybrid_kem.entropy.drbg import DRBG
from hybrid_kem.kem_slwe.slwe_wrapper import SLWEWrapper

DEFAULT_TRIALS = 10_000
TIME_BUDGET_SECONDS = 30 * 60


def _drbg(label: bytes) -> DRBG:
    d = DRBG()
    # Seeded from os.urandom for the measurement; deterministic seeding is
    # not the goal here. If you want reproducible runs, set a fixed entropy
    # buffer in this helper.
    import os
    d.instantiate(os.urandom(32), os.urandom(16), b"dfr-scaling:" + label)
    return d


def measure_dfr(k: int, q: int, trials: int) -> tuple[int, int, float]:
    """Return (failures, completed_trials, elapsed_seconds)."""
    failures = 0
    completed = 0
    started = time.monotonic()
    s = SLWEWrapper(mode="toy", params={"k": k, "q": q})
    for _ in range(trials):
        if time.monotonic() - started > TIME_BUDGET_SECONDS:
            break
        d = _drbg(b"trial")
        pk, sk = s.keygen(d)
        ct, ss_enc = s.encaps(pk, d)
        ss_dec = s.decaps(sk, ct)
        if ss_enc != ss_dec:
            failures += 1
        completed += 1
    return failures, completed, time.monotonic() - started


def linear_fit(xs: list[float], ys: list[float]) -> tuple[float, float]:
    """Return (slope, intercept) of an OLS fit y = slope * x + intercept."""
    if len(xs) < 2:
        return 0.0, ys[0] if ys else 0.0
    mean_x = statistics.mean(xs)
    mean_y = statistics.mean(ys)
    num = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys))
    den = sum((x - mean_x) ** 2 for x in xs)
    if den == 0:
        return 0.0, mean_y
    slope = num / den
    intercept = mean_y - slope * mean_x
    return slope, intercept


def write_report(points: Iterable[tuple[int, int, int, int, float]],
                 slope: float, intercept: float,
                 out: Path,
                 requested_trials: int) -> None:
    rows = []
    xs_for_fit: list[float] = []
    ys_for_fit: list[float] = []
    for k, q, fails, total, elapsed in points:
        if total == 0:
            rows.append(f"| {k} | {q} | 0 | 0 | 0 | n/a | timed out |")
            continue
        dfr = fails / total
        log_dfr = math.log2(dfr) if dfr > 0 else float("-inf")
        xs_for_fit.append(k)
        ys_for_fit.append(log_dfr if math.isfinite(log_dfr) else -64.0)
        cap_note = (
            f"hit {TIME_BUDGET_SECONDS}s cap after {total} trials"
            if total < requested_trials
            else f"completed in {elapsed:.0f}s"
        )
        rows.append(
            f"| {k} | {q} | {fails} | {total} | "
            f"{dfr:.3e} | {log_dfr:.2f} | {cap_note} |"
        )
    body = (
        "# Module-SLWE empirical DFR scaling\n\n"
        "| k | q | failures | trials | DFR | log2(DFR) | notes |\n"
        "|---|---|---|---|---|---|---|\n"
        + "\n".join(rows) + "\n\n"
        f"**Linear fit:** log2(DFR) ≈ {slope:.3f} · k + {intercept:.3f}\n\n"
        "Slope is the number of bits of failure-rate reduction we get per "
        "unit increase in module rank, holding q fixed at the larger "
        "settings.\n"
    )
    out.write_text(body, encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--trials", type=int, default=DEFAULT_TRIALS)
    p.add_argument("--out", type=Path,
                   default=Path("tools/dfr_scaling_results.md"))
    args = p.parse_args(argv)

    # Brief 02 §3 asks for k ∈ {4, 8, 12, 16} with q ≈ 2^24 at the larger
    # sizes. The supplied source (tools/sqt_slwe.py) has p = 911 hardcoded
    # (SPEC.md §2.6 toy parameters), so the q axis cannot vary without a
    # reparametrisation of the source. We measure along the k axis only;
    # the q field below records the fixed 911.
    plan = [(4, 911), (8, 911), (12, 911), (16, 911)]

    points: list[tuple[int, int, int, int, float]] = []
    try:
        for k, q in plan:
            fails, total, elapsed = measure_dfr(k, q, args.trials)
            points.append((k, q, fails, total, elapsed))
    except NotImplementedError as exc:
        sys.stderr.write(
            "SLWEWrapper raised NotImplementedError: "
            f"{exc}\nWire toy mode (Brief 02 §1) before running this script.\n"
        )
        return 3

    xs = [float(k) for k, _, _, total, _ in points if total > 0]
    ys = [math.log2(f / total) if f > 0 and total > 0 else -64.0
          for _, _, f, total, _ in points if total > 0]
    slope, intercept = linear_fit(xs, ys)
    write_report(points, slope, intercept, args.out, args.trials)
    return 0


if __name__ == "__main__":
    import sys
    raise SystemExit(main())
