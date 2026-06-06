"""Capillary variance detector for web endpoints.

A *capillary* probe does not flood a target with a large wordlist to
measure the whole "volume" of its response surface. Instead it learns a
small, statistically-stable *baseline* and then sends a handful of
deliberate mutations ("variants"), flagging only the ones whose response
deviates from that baseline by more than its own natural noise.

The key idea is that a single baseline request carries no notion of
variance. Real endpoints jitter: timestamps, CSRF tokens, rotating ads,
and load-dependent latency all change the response between two identical
requests. So a fixed "flag anything below 0.85 similarity" rule cannot
separate signal from noise. This module instead:

  1. Samples the unmutated endpoint N times to learn a noise floor --
     mean/stddev of response time and content length, plus the body's
     own self-similarity (how much it changes between identical requests).
  2. Scores each variant against that learned distribution (z-scores for
     time and length, adaptive similarity threshold for the body).
  3. Flags a variant only when it exits the baseline's natural envelope,
     and reports *which* signals fired and how strongly.

Intended for authorised security testing of systems you own or have
written permission to assess. Use the --delay / --samples knobs to stay
within the target's acceptable load.

Dependencies: requests (already used elsewhere in this repo's tooling).
"""

from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
import time
from dataclasses import dataclass, field
from typing import Any, Iterable

import requests

from capillary_robust import (
    RECOMMENDED_SAMPLES,
    RobustBaselineStats,
    all_pairs_min_similarity,
    decide_anomalous,
    score_length,
    score_timing,
)


# Body is normalised and capped before comparison so difflib stays cheap
# on large pages (its ratio is roughly O(n*m)).
_BODY_COMPARE_CAP = 100_000
_WHITESPACE = re.compile(r"\s+")
# Where a variant's parameters are injected into the request.
_INJECT_POINTS = {"query", "body", "json", "header", "path"}


def _normalise_body(text: str) -> str:
    """Collapse whitespace and cap length for stable, cheap comparison."""
    collapsed = _WHITESPACE.sub(" ", text).strip()
    return collapsed[:_BODY_COMPARE_CAP]


def _similarity(a: str, b: str) -> float:
    """Structural similarity in [0.0, 1.0]; 1.0 means identical."""
    # real_quick_ratio is a cheap upper bound -- if even that is low the
    # bodies cannot be similar, so we can skip the full comparison.
    matcher = difflib.SequenceMatcher(None, a, b, autojunk=False)
    if matcher.real_quick_ratio() < 0.1:
        return matcher.real_quick_ratio()
    return matcher.ratio()


@dataclass
class Sample:
    """One observation of the endpoint."""

    status_code: int
    content_length: int
    response_time: float
    header_keys: frozenset[str]
    body: str  # already normalised


@dataclass
class Baseline:
    """Statistically-described baseline learned from repeated sampling."""

    status_codes: set[int]
    # Robust centre/scale for length and timing (median + scaled MAD with
    # metric-appropriate floors); replaces the old mean/stddev z-scoring.
    stats: RobustBaselineStats
    # Header keys seen in *every* baseline sample (the stable set).
    stable_headers: frozenset[str]
    reference_body: str
    # Lowest self-similarity across *all* pairs of identical baseline
    # responses: the body's natural variance floor. A variant must drop
    # below this (scaled by the threshold) to count as anomalous.
    content_floor: float
    samples: list[Sample] = field(default_factory=list)

    def describe(self) -> str:
        return (
            f"status={sorted(self.status_codes)} "
            f"{self.stats.describe()} "
            f"content_floor={self.content_floor:.4f} "
            f"stable_headers={len(self.stable_headers)}"
        )


@dataclass
class VarianceReport:
    """Result of scoring one variant against the baseline."""

    name: str
    status_code: int
    status_changed: bool
    similarity: float
    similarity_threshold: float
    # length_z is 0.0 in the deterministic-length any-change branch; read
    # length_delta / length_reason there instead.
    length_z: float
    length_delta: float
    length_reason: str
    time_z: float
    time_delta: float
    time_reason: str
    header_diff: set[str]
    reflected: bool
    signals: list[str]
    anomalous: bool

    def to_dict(self) -> dict[str, Any]:
        d = self.__dict__.copy()
        d["header_diff"] = sorted(self.header_diff)
        return d


class CapillaryVarianceScanner:
    """Learn a baseline, then measure how far variants deviate from it."""

    def __init__(
        self,
        target_url: str,
        *,
        variance_threshold: float = 0.85,
        z_threshold: float = 3.0,
        samples: int = RECOMMENDED_SAMPLES,
        timeout: float = 10.0,
        delay: float = 0.0,
        method: str | None = None,
        inject: str = "query",
        path_marker: str = "FUZZ",
        path_baseline: str = "",
        verify_tls: bool = True,
    ) -> None:
        self.target_url = target_url
        # Body similarity below content_floor * threshold => flagged.
        self.variance_threshold = variance_threshold
        # How many stddevs of time/length deviation count as anomalous.
        self.z_threshold = z_threshold
        self.samples = max(2, samples)
        self.timeout = timeout
        self.delay = delay
        if inject not in _INJECT_POINTS:
            raise ValueError(
                f"inject must be one of {sorted(_INJECT_POINTS)}, got {inject!r}"
            )
        self.inject = inject
        # Path injection is positional: the variant value replaces a marker
        # in the URL itself, so the URL must contain that marker.
        self.path_marker = path_marker
        self.path_baseline = path_baseline
        if inject == "path" and path_marker not in target_url:
            raise ValueError(
                f"path injection requires the marker {path_marker!r} in the URL, "
                f"e.g. https://host/api/users/{path_marker}"
            )
        # Body/json variants ride in a request body, so default to POST
        # unless the caller pinned a method explicitly.
        default_method = "POST" if inject in ("body", "json") else "GET"
        self.method = (method or default_method).upper()
        self.baseline: Baseline | None = None

        # A single session reuses the TCP/TLS connection so per-request
        # timing reflects the server, not handshake setup.
        self.session = requests.Session()
        self.session.verify = verify_tls
        self.session.headers.update(
            {
                "User-Agent": "Capillary-Variance-Scanner/2.0",
                # Disable transparent compression so byte lengths are raw.
                "Accept-Encoding": "identity",
                # Avoid intermediary caches returning a stale, identical body.
                "Cache-Control": "no-cache",
            }
        )

    # -- request plumbing ---------------------------------------------------

    def _request(self, payload: dict | None = None) -> Sample:
        # Route the variant to the configured injection point. With no
        # payload (baseline sampling) the request rides the same method and
        # transport but carries no mutation.
        url = self.target_url
        kwargs: dict[str, Any] = {"timeout": self.timeout}
        if self.inject == "path":
            # Positional: substitute the marker with the variant value (or
            # the known-good baseline value when sampling the baseline).
            url = self._build_path_url(payload)
        elif payload:
            if self.inject == "query":
                kwargs["params"] = payload
            elif self.inject == "body":
                kwargs["data"] = payload
            elif self.inject == "json":
                kwargs["json"] = payload
            elif self.inject == "header":
                # Header values must be strings; coerce lists/ints.
                kwargs["headers"] = {k: str(v) for k, v in payload.items()}

        start = time.perf_counter()
        response = self.session.request(
            self.method,
            url,
            **kwargs,
        )
        elapsed = time.perf_counter() - start
        return Sample(
            status_code=response.status_code,
            content_length=len(response.content),
            response_time=elapsed,
            header_keys=frozenset(response.headers.keys()),
            body=_normalise_body(response.text),
        )

    def _build_path_url(self, payload: dict | None) -> str:
        """Substitute the path marker with the variant (or baseline) value.

        The substring is inserted verbatim -- no URL-encoding -- so
        traversal sequences like ``../`` or pre-encoded ``..%2f`` reach the
        server intact, which is the whole point of path probing.
        """
        if not payload:
            value = self.path_baseline
        else:
            # Multiple values join into nested segments; the common case is
            # a single value, e.g. {"seg": "../../etc/passwd"}.
            value = "/".join(str(v) for v in payload.values())
        return self.target_url.replace(self.path_marker, value)

    # -- baseline -----------------------------------------------------------

    def establish_baseline(self) -> bool:
        """Sample the unmutated endpoint repeatedly to learn its noise."""
        print(f"[*] Establishing baseline for: {self.target_url}")
        print(
            f"    method={self.method} inject={self.inject} "
            f"samples={self.samples}"
        )
        try:
            # Warm-up request primes the connection; discarded so the TLS
            # handshake does not inflate the timing baseline.
            self._request()

            samples: list[Sample] = []
            for i in range(self.samples):
                if self.delay:
                    time.sleep(self.delay)
                sample = self._request()
                samples.append(sample)
                print(
                    f"    sample {i + 1}/{self.samples}: "
                    f"status={sample.status_code} "
                    f"len={sample.content_length}B "
                    f"time={sample.response_time:.4f}s"
                )
        except requests.exceptions.RequestException as e:
            print(f"[-] Failed to establish baseline: {e}")
            return False

        lengths = [s.content_length for s in samples]
        times = [s.response_time for s in samples]
        header_sets = [s.header_keys for s in samples]

        # The body's natural variance floor: the worst self-similarity across
        # *all* pairs of identical baseline responses (a single-reference
        # floor can be skewed by one unlucky sample).
        bodies = [s.body for s in samples]
        content_floor = all_pairs_min_similarity(bodies, _similarity)

        self.baseline = Baseline(
            status_codes={s.status_code for s in samples},
            stats=RobustBaselineStats.from_samples(lengths, times),
            stable_headers=frozenset.intersection(*header_sets),
            reference_body=samples[-1].body,
            content_floor=content_floor,
            samples=samples,
        )
        print(f"[+] Baseline learned: {self.baseline.describe()}")
        return True

    # -- variance measurement ----------------------------------------------

    def measure_variance(
        self, name: str, sample: Sample, payload: dict
    ) -> VarianceReport:
        """Score one variant's response against the learned baseline."""
        assert self.baseline is not None
        b = self.baseline

        status_changed = sample.status_code not in b.status_codes

        # Robust scoring: median + scaled MAD with metric-appropriate floors.
        # Length self-selects an any-change rule when the baseline is
        # deterministic; timing always uses the floored robust z.
        time_v = score_timing(sample.response_time, b.stats, self.z_threshold)
        length_v = score_length(sample.content_length, b.stats, self.z_threshold)

        similarity = _similarity(b.reference_body, sample.body)
        # Adaptive threshold: a page that naturally jitters (low floor)
        # tolerates more variance before a variant counts as anomalous.
        sim_threshold = b.content_floor * self.variance_threshold

        header_diff = set(sample.header_keys) ^ set(b.stable_headers)

        reflected = self._is_reflected(payload, sample.body)

        signals: list[str] = []
        if status_changed:
            signals.append("status")
        if similarity < sim_threshold:
            signals.append("body")
        if length_v.fired:
            signals.append("length")
        if time_v.fired:
            signals.append("timing")
        if reflected:
            signals.append("reflection")
        if header_diff:
            signals.append("headers")

        # Strong signals (status/body/length/timing) flag on their own;
        # reflection elevates only in combination with another signal.
        anomalous = decide_anomalous(signals)

        return VarianceReport(
            name=name,
            status_code=sample.status_code,
            status_changed=status_changed,
            similarity=similarity,
            similarity_threshold=sim_threshold,
            length_z=length_v.z,
            length_delta=length_v.delta,
            length_reason=length_v.reason,
            time_z=time_v.z,
            time_delta=time_v.delta,
            time_reason=time_v.reason,
            header_diff=header_diff,
            reflected=reflected,
            signals=signals,
            anomalous=anomalous,
        )

    @staticmethod
    def _is_reflected(payload: dict, body: str) -> bool:
        """Whether any payload value appears verbatim in the response."""
        for value in payload.values():
            for item in value if isinstance(value, list) else [value]:
                token = str(item).strip()
                # Skip trivially-short tokens that match by chance.
                if len(token) >= 3 and token in body:
                    return True
        return False

    # -- driver -------------------------------------------------------------

    def scan(self, payloads: dict[str, dict]) -> list[VarianceReport]:
        """Inject each variant and collect its variance report."""
        if self.baseline is None:
            raise RuntimeError("Baseline not established; call establish_baseline().")

        print("\n[*] Capillary branching: probing variants...")
        reports: list[VarianceReport] = []
        for name, payload in payloads.items():
            if self.delay:
                time.sleep(self.delay)
            try:
                sample = self._request(payload)
            except requests.exceptions.RequestException as e:
                print(f"[-] Branch failure on {name}: {e}")
                continue

            report = self.measure_variance(name, sample, payload)
            reports.append(report)
            self._print_report(report)
        return reports

    @staticmethod
    def _print_report(r: VarianceReport) -> None:
        if r.anomalous:
            print(f"\n[!] VARIANT DETECTED: {r.name}  signals={r.signals}")
            print(f"    - status      : {r.status_code} (changed={r.status_changed})")
            print(
                f"    - similarity  : {r.similarity:.4f} "
                f"(threshold {r.similarity_threshold:.4f})"
            )
            print(f"    - length      : {r.length_reason}")
            print(f"    - timing      : {r.time_reason}")
            if r.reflected:
                print("    - reflection  : payload echoed in body")
            if r.header_diff:
                print(f"    - header drift: {', '.join(sorted(r.header_diff))}")
        else:
            note = " (reflected)" if r.reflected else ""
            print(
                f"[-] {r.name}: within baseline envelope "
                f"(sim {r.similarity:.4f}, time z {r.time_z:+.2f}){note}"
            )


# Capillary variants: a few deliberate mutations, not a wordlist. Each
# probes a distinct parsing/handling assumption.
DEFAULT_VARIANTS: dict[str, dict] = {
    "Type_Confusion_Array": {"id[]": "1"},
    "Null_Byte_Injection": {"id": "1\x00"},
    "Parameter_Pollution": {"id": ["1", "2"]},
    "Method_Override": {"_method": "PUT", "id": "1"},
    "Path_Traversal_Subtle": {"id": "../1"},
    "SQL_Tautology": {"id": "1 OR 1=1"},
    "Oversized_Value": {"id": "9" * 256},
}


def load_variants(path: str | None) -> dict[str, dict]:
    if not path:
        return DEFAULT_VARIANTS
    with open(path, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    if not isinstance(data, dict):
        raise ValueError("Variants file must be a JSON object of name -> params.")
    return data


def parse_args(argv: Iterable[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Capillary variance detector: learn an endpoint's "
        "baseline noise, then flag variants that deviate beyond it.",
    )
    p.add_argument("url", help="Target URL (system you are authorised to test).")
    p.add_argument(
        "-t",
        "--threshold",
        type=float,
        default=0.85,
        help="Body similarity threshold, scaled by the learned content "
        "floor (default: 0.85).",
    )
    p.add_argument(
        "-z",
        "--z-threshold",
        type=float,
        default=3.0,
        help="Stddevs of time/length deviation that count as anomalous "
        "(default: 3.0).",
    )
    p.add_argument(
        "-n",
        "--samples",
        type=int,
        default=RECOMMENDED_SAMPLES,
        help="Number of baseline samples to learn the noise floor "
        f"(default: {RECOMMENDED_SAMPLES}; robust scale estimation needs "
        "~15-20, fewer widens the envelope).",
    )
    p.add_argument("--timeout", type=float, default=10.0, help="Per-request timeout (s).")
    p.add_argument(
        "--delay",
        type=float,
        default=0.0,
        help="Delay between requests (s) to respect target load.",
    )
    p.add_argument(
        "--method",
        default=None,
        help="HTTP method (default: GET, or POST when --inject is body/json).",
    )
    p.add_argument(
        "--inject",
        choices=sorted(_INJECT_POINTS),
        default="query",
        help="Where to inject each variant: query string, form body, JSON "
        "body, request headers, or URL path (default: query).",
    )
    p.add_argument(
        "--path-marker",
        default="FUZZ",
        help="Placeholder in the URL replaced by the variant value when "
        "--inject path is used (default: FUZZ).",
    )
    p.add_argument(
        "--path-baseline",
        default="",
        help="Known-good value substituted for the marker while learning the "
        "baseline under --inject path (e.g. a real resource id).",
    )
    p.add_argument(
        "--insecure",
        action="store_true",
        help="Do not verify TLS certificates.",
    )
    p.add_argument(
        "--variants",
        help="Path to a JSON file of {name: params} variants "
        "(default: built-in capillary set).",
    )
    p.add_argument("--json", dest="json_out", help="Write structured results to this path.")
    return p.parse_args(list(argv) if argv is not None else None)


def main(argv: Iterable[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        variants = load_variants(args.variants)
    except (OSError, ValueError, json.JSONDecodeError) as e:
        print(f"[-] Could not load variants: {e}", file=sys.stderr)
        return 2

    try:
        scanner = CapillaryVarianceScanner(
            args.url,
            variance_threshold=args.threshold,
            z_threshold=args.z_threshold,
            samples=args.samples,
            timeout=args.timeout,
            delay=args.delay,
            method=args.method,
            inject=args.inject,
            path_marker=args.path_marker,
            path_baseline=args.path_baseline,
            verify_tls=not args.insecure,
        )
    except ValueError as e:
        print(f"[-] {e}", file=sys.stderr)
        return 2

    if not scanner.establish_baseline():
        return 1

    reports = scanner.scan(variants)
    flagged = [r for r in reports if r.anomalous]
    print(f"\n[*] Done: {len(flagged)}/{len(reports)} variants flagged.")

    if args.json_out:
        payload = {
            "target": args.url,
            "baseline": scanner.baseline.describe() if scanner.baseline else None,
            "reports": [r.to_dict() for r in reports],
        }
        with open(args.json_out, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, indent=2)
        print(f"[+] Results written to {args.json_out}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
