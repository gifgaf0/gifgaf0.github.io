"""Crystal calibration for the quartz entropy source (Brief 05).

Promotes (or falsifies) the T3 PUF claim from Brief 04. Off-line tool:
runs at installation and periodically; not part of the runtime entropy
path. Produces and stores spectral fingerprints, runs a subset of the
SP 800-90B min-entropy estimators, and reports inter-crystal
discriminability so an operator can decide whether the PUF assumption
holds at their hardware.

Module layout:

- :class:`CrystalFingerprint`, :class:`CalibrationResult`,
  :class:`DiscriminabilityReport` — data records persisted to the
  calibration JSONL log and surfaced to the caller.
- :class:`CrystalCalibrator` — main entry point: ``calibrate``,
  ``identify``, ``discriminability_report``, ``update_health_test_params``,
  ``export_report``.
- :class:`SimulatedCalibrationError`, :class:`CalibrationNotFoundError`
  — fail-closed signals required by the brief.
- ``compute_psd`` / ``fingerprint_distance`` — public spectral
  helpers (thin wrappers over ``scipy.signal.welch`` and
  ``scipy.spatial.distance.jensenshannon``).

Security notes (verbatim from the brief, summarised here):

1. **Calibration DB is sensitive.** Protect with 0600 permissions on
   encrypted storage; the PSD profiles partially characterise the
   noise source.
2. **Simulated calibration results must be clearly labelled.** Every
   fingerprint stores its ``backend_class``;
   :meth:`update_health_test_params` refuses to return H_min from a
   simulated backend with :class:`SimulatedCalibrationError`.
3. **PUF falsification must be documented explicitly.** When
   ``discriminability_report`` returns ``puf_assessment='falsified'``,
   the caller is responsible for writing the falsification text to
   ``CALIBRATION_NOTES.md``; ``export_report`` emits the same text
   into its plain-text artefact.
4. **Intra-crystal drift** — recalibrate periodically (recommended
   monthly).
5. **IDENTITY_THRESHOLD** is an engineering placeholder; tune from
   :meth:`discriminability_report`'s output.
"""

from __future__ import annotations

import hashlib
import json
import math
import time
import zlib
from collections import Counter
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Iterable, Sequence

from scipy.signal import welch
from scipy.spatial.distance import jensenshannon

from .quartz_entropy_source import ADCBackend, HardwareUnavailableError


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------


class CalibrationNotFoundError(KeyError):
    """No stored fingerprint for the requested (crystal_id, stress_level)."""


class SimulatedCalibrationError(RuntimeError):
    """Refusal to surface H_min derived from a simulated backend."""


# ---------------------------------------------------------------------------
# Data records
# ---------------------------------------------------------------------------


@dataclass
class CrystalFingerprint:
    crystal_id: str
    stress_level: int
    psd_profile: list[float]
    psd_bin_hz: float
    h_min_estimate: float
    h_min_method: str            # "min(mcv, collision, markov, compression)"
    sample_count: int
    calibrated_at: str
    backend_class: str
    notes: str = ""

    def to_json_dict(self) -> dict:
        return asdict(self)


@dataclass
class CalibrationResult:
    crystal_id: str
    fingerprints: dict[int, CrystalFingerprint]
    inter_crystal_distance: float | None
    puf_claim_supported: bool | None
    puf_claim_tier: str
    notes: str


@dataclass
class DiscriminabilityReport:
    stress_level: int | None
    crystal_ids: list[str]
    pairwise_distances: dict[str, dict[str, float]]
    min_inter_distance: float | None
    mean_inter_distance: float | None
    max_inter_distance: float | None
    max_intra_distance: float | None
    puf_assessment: str          # 'supported' | 'inconclusive' | 'falsified'
    puf_tier: str                # 'T2' | 'T3' | 'falsified'
    recommended_h_min: float | None
    recommended_identity_threshold: float | None
    notes: str = ""


# ---------------------------------------------------------------------------
# PSD + distance helpers (public)
# ---------------------------------------------------------------------------


def compute_psd(samples: Sequence[float], sample_rate: int,
                n_fft: int = 512) -> tuple[list[float], float]:
    """Welch PSD with normalisation. Returns ``(psd_profile, bin_hz)``.

    PSD is normalised to sum to ``1.0`` so it can be treated as a
    discrete probability distribution and fed to Jensen-Shannon.
    """
    if len(samples) < 2:
        return [1.0], float(sample_rate) / 2.0
    import numpy as _np
    nperseg = min(n_fft, len(samples))
    freqs, psd = welch(_np.asarray(samples, dtype=_np.float64),
                       fs=sample_rate, nperseg=nperseg)
    total = float(psd.sum())
    if total <= 0:
        # degenerate (all-zero) input; return uniform PSD
        n = len(psd)
        return ([1.0 / n] * n), float(freqs[1] - freqs[0]) if len(freqs) > 1 else 1.0
    normalised = [float(x) / total for x in psd]
    bin_hz = float(freqs[1] - freqs[0]) if len(freqs) > 1 else float(sample_rate) / 2.0
    return normalised, bin_hz


def fingerprint_distance(p: Sequence[float], q: Sequence[float]) -> float:
    """Jensen-Shannon distance between two normalised PSDs.

    Always in ``[0, 1]``; lower means more similar. We pad the shorter
    profile with zeros to align lengths — Welch outputs the same length
    for samples taken with matching ``n_fft``, but calibrations done
    with different sample counts may yield slightly different bin
    counts.
    """
    pa = list(p)
    qa = list(q)
    if len(pa) != len(qa):
        n = max(len(pa), len(qa))
        pa = pa + [0.0] * (n - len(pa))
        qa = qa + [0.0] * (n - len(qa))
    if sum(pa) <= 0 or sum(qa) <= 0:
        return 1.0
    d = float(jensenshannon(pa, qa))
    # scipy returns NaN if either input is all-zero; guard.
    if math.isnan(d):
        return 1.0
    return d


# ---------------------------------------------------------------------------
# SP 800-90B subset of min-entropy estimators (§6.3, four of ten)
# ---------------------------------------------------------------------------


def _quantise_to_byte(samples: Sequence[float]) -> list[int]:
    out = []
    for v in samples:
        v = max(-1.0, min(1.0, float(v)))
        out.append(int(round((v + 1.0) * 127.5)))
    return out


def mcv_estimate(samples: Sequence[int]) -> float:
    """SP 800-90B §6.3.1 — Most Common Value estimator (simplified)."""
    if not samples:
        return 8.0
    counts = Counter(samples)
    p_max = max(counts.values()) / len(samples)
    if p_max <= 0:
        return 8.0
    return -math.log2(p_max)


def collision_estimate(samples: Sequence[int]) -> float:
    """SP 800-90B §6.3.2 — collision-rate-based estimator (simplified).

    The full §6.3.2 procedure involves an iterative root-find on a
    sample-size correction; we use the second-order Rényi entropy
    derived from the empirical pair-collision rate, halved to recover
    a conservative min-entropy bound. Brief 05 explicitly authorises
    this simplification (the four-estimator subset is the agreed scope,
    not a SP 800-90B submission).
    """
    n = len(samples)
    if n < 2:
        return 8.0
    pairs = sum(1 for i in range(n - 1) if samples[i] == samples[i + 1])
    if pairs == 0:
        return 8.0
    p_coll = pairs / (n - 1)
    if p_coll >= 1.0:
        return 0.0
    return -math.log2(p_coll) / 2.0


def markov_estimate(samples: Sequence[int]) -> float:
    """SP 800-90B §6.3.3 — first-order Markov chain estimator."""
    if len(samples) < 2:
        return 8.0
    # Count transitions
    pair_counts: Counter = Counter()
    prefix_counts: Counter = Counter()
    for a, b in zip(samples, samples[1:]):
        pair_counts[(a, b)] += 1
        prefix_counts[a] += 1
    max_cond = 0.0
    for (a, b), c in pair_counts.items():
        denom = prefix_counts[a]
        if denom == 0:
            continue
        p = c / denom
        if p > max_cond:
            max_cond = p
    if max_cond <= 0:
        return 8.0
    return -math.log2(max_cond)


def compression_estimate(samples: Sequence[int]) -> float:
    """SP 800-90B §6.3.4 — compression-based estimator (zlib proxy).

    We compress the byte representation of the sample stream and treat
    the compressed length as an upper bound on entropy. Per-sample
    min-entropy estimate is conservatively ``8 * ratio - safety_margin``,
    clipped to ``[0, 8]``. Documented as a proxy in CALIBRATION_NOTES.
    """
    if not samples:
        return 8.0
    raw = bytes(int(s) & 0xff for s in samples)
    compressed = zlib.compress(raw, level=9)
    ratio = len(compressed) / len(raw) if raw else 1.0
    return max(0.0, min(8.0, 8.0 * ratio - 0.5))


def estimate_h_min(samples: Sequence[float]) -> tuple[float, str]:
    """Conservative H_min = ``min`` of the four estimators above.

    Returns ``(h_min, method_label)`` where the label notes which
    estimators were applied.
    """
    quant = _quantise_to_byte(samples)
    estimates = {
        "mcv": mcv_estimate(quant),
        "collision": collision_estimate(quant),
        "markov": markov_estimate(quant),
        "compression": compression_estimate(quant),
    }
    h_min = min(estimates.values())
    return h_min, "min(mcv,collision,markov,compression)"


# ---------------------------------------------------------------------------
# Identity threshold and PUF assessment heuristics
# ---------------------------------------------------------------------------


IDENTITY_THRESHOLD = 0.15
SUPPORTED_RATIO = 3.0
INCONCLUSIVE_RATIO = 1.0


def _puf_assessment(min_inter: float | None,
                    max_intra: float | None) -> tuple[str, str]:
    """Return ``(assessment, tier)`` from the brief's heuristic."""
    if min_inter is None:
        return "inconclusive", "T3"
    if max_intra is None or max_intra <= 0:
        # No intra-crystal data — assess only on inter distance scale.
        return ("supported" if min_inter > 0.01 else "falsified",
                "T2" if min_inter > 0.01 else "falsified")
    if min_inter > SUPPORTED_RATIO * max_intra:
        return "supported", "T2"
    if min_inter > INCONCLUSIVE_RATIO * max_intra:
        return "inconclusive", "T3"
    return "falsified", "falsified"


# ---------------------------------------------------------------------------
# CrystalCalibrator
# ---------------------------------------------------------------------------


_DEFAULT_DB_PATH = Path(__file__).parent / "calibration_db.jsonl"


class CrystalCalibrator:
    """Off-line calibration and identification tool for the quartz source."""

    def __init__(
        self,
        db_path: str | Path = _DEFAULT_DB_PATH,
        n_fft_bins: int = 512,
        calibration_samples: int = 44_100,
    ):
        self._db_path = Path(db_path)
        self._n_fft = n_fft_bins
        self._n_samples = calibration_samples
        self._cache: list[CrystalFingerprint] | None = None

    @property
    def n_fft_bins(self) -> int:
        return self._n_fft

    # ------------------------------------------------------------------
    # DB persistence
    # ------------------------------------------------------------------

    def _load(self) -> list[CrystalFingerprint]:
        if self._cache is not None:
            return self._cache
        records: list[CrystalFingerprint] = []
        if self._db_path.exists():
            for line in self._db_path.read_text().splitlines():
                if not line.strip():
                    continue
                d = json.loads(line)
                records.append(CrystalFingerprint(**d))
        self._cache = records
        return records

    def _append(self, fp: CrystalFingerprint) -> None:
        self._db_path.parent.mkdir(parents=True, exist_ok=True)
        with self._db_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(fp.to_json_dict()) + "\n")
        if self._cache is not None:
            self._cache.append(fp)

    def all_fingerprints(self) -> list[CrystalFingerprint]:
        return list(self._load())

    # ------------------------------------------------------------------
    # Calibrate
    # ------------------------------------------------------------------

    def _collect_samples(self, channel: int, adc: ADCBackend) -> list[float]:
        out: list[float] = []
        for _ in range(self._n_samples):
            out.append(float(adc.read_voltage(channel)))
        return out

    def calibrate(
        self,
        crystal_id: str,
        channel: int,
        adc: ADCBackend,
        stress_levels: list[int],
        notes: str = "",
    ) -> CalibrationResult:
        if not stress_levels:
            raise ValueError("stress_levels must be non-empty")
        sample_rate = adc.sample_rate_hz()
        backend_class = type(adc).__name__

        fingerprints: dict[int, CrystalFingerprint] = {}
        for level in stress_levels:
            # Apply stress to the simulated backend if applicable; real
            # hardware backends would have an external stress controller.
            set_stress = getattr(adc, "set_channel_stress", None)
            if callable(set_stress):
                set_stress(channel, level)
            samples = self._collect_samples(channel, adc)
            psd, bin_hz = compute_psd(samples, sample_rate, self._n_fft)
            h_min, method = estimate_h_min(samples)
            fp = CrystalFingerprint(
                crystal_id=crystal_id,
                stress_level=level,
                psd_profile=psd,
                psd_bin_hz=bin_hz,
                h_min_estimate=h_min,
                h_min_method=method,
                sample_count=len(samples),
                calibrated_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                backend_class=backend_class,
                notes=notes,
            )
            self._append(fp)
            fingerprints[level] = fp

        # Inter-crystal distance only meaningful with >1 calibrated crystal.
        existing = self._load()
        other_ids = {fp.crystal_id for fp in existing
                     if fp.crystal_id != crystal_id}
        inter = None
        supported: bool | None = None
        tier = "T3"
        if other_ids:
            report = self.discriminability_report()
            inter = report.min_inter_distance
            supported = report.puf_assessment == "supported"
            tier = report.puf_tier
        return CalibrationResult(
            crystal_id=crystal_id,
            fingerprints=fingerprints,
            inter_crystal_distance=inter,
            puf_claim_supported=supported,
            puf_claim_tier=tier,
            notes=notes,
        )

    # ------------------------------------------------------------------
    # Identify
    # ------------------------------------------------------------------

    def identify(
        self,
        adc_samples: Sequence[float],
        stress_level: int,
        top_n: int = 3,
        sample_rate: int = 44_100,
    ) -> list[tuple[str, float]]:
        psd, _ = compute_psd(adc_samples, sample_rate, self._n_fft)
        candidates = [fp for fp in self._load() if fp.stress_level == stress_level]
        if not candidates:
            return []
        scored = []
        for fp in candidates:
            d = fingerprint_distance(psd, fp.psd_profile)
            scored.append((fp.crystal_id, d))
        scored.sort(key=lambda x: x[1])
        return scored[:top_n]

    # ------------------------------------------------------------------
    # Discriminability
    # ------------------------------------------------------------------

    def discriminability_report(
        self,
        stress_level: int | None = None,
    ) -> DiscriminabilityReport:
        records = [fp for fp in self._load()
                   if stress_level is None or fp.stress_level == stress_level]
        ids = sorted({fp.crystal_id for fp in records})
        # Group fingerprints by crystal_id (multiple entries → repeated
        # calibration on the same crystal = intra-crystal stability data).
        by_id: dict[str, list[CrystalFingerprint]] = {}
        for fp in records:
            by_id.setdefault(fp.crystal_id, []).append(fp)

        # Pairwise inter-crystal distance — using the first fingerprint per id
        # for each (crystal_id, stress_level) pair, but if there are multiple
        # fingerprints we take the min across them so we report the tightest
        # observed inter distance.
        pairwise: dict[str, dict[str, float]] = {a: {} for a in ids}
        inter_distances: list[float] = []
        for i, a in enumerate(ids):
            for j, b in enumerate(ids):
                if j <= i:
                    continue
                d_min = min(
                    fingerprint_distance(fa.psd_profile, fb.psd_profile)
                    for fa in by_id[a]
                    for fb in by_id[b]
                )
                pairwise[a][b] = d_min
                pairwise[b][a] = d_min
                inter_distances.append(d_min)

        # Intra-crystal distance: max JSD across repeated fingerprints
        intra_distances: list[float] = []
        for fps in by_id.values():
            for i in range(len(fps)):
                for j in range(i + 1, len(fps)):
                    intra_distances.append(
                        fingerprint_distance(
                            fps[i].psd_profile, fps[j].psd_profile
                        )
                    )

        min_inter = min(inter_distances) if inter_distances else None
        mean_inter = (sum(inter_distances) / len(inter_distances)
                      if inter_distances else None)
        max_inter = max(inter_distances) if inter_distances else None
        max_intra = max(intra_distances) if intra_distances else None

        assessment, tier = _puf_assessment(min_inter, max_intra)
        notes = ""
        if len(ids) < 2:
            assessment, tier = "inconclusive", "T3"
            notes = "Only one crystal calibrated; needs >= 2 for PUF assessment."

        # Recommended H_min: minimum across all relevant fingerprints
        # (operator gets the most conservative bound the calibration saw).
        rec_h_min = None
        if records:
            rec_h_min = min(fp.h_min_estimate for fp in records)
        # Recommended identity threshold per the brief: 2x max intra,
        # falling back to the static IDENTITY_THRESHOLD when no intra
        # data is available.
        rec_threshold = (2.0 * max_intra) if max_intra else IDENTITY_THRESHOLD

        return DiscriminabilityReport(
            stress_level=stress_level,
            crystal_ids=ids,
            pairwise_distances=pairwise,
            min_inter_distance=min_inter,
            mean_inter_distance=mean_inter,
            max_inter_distance=max_inter,
            max_intra_distance=max_intra,
            puf_assessment=assessment,
            puf_tier=tier,
            recommended_h_min=rec_h_min,
            recommended_identity_threshold=rec_threshold,
            notes=notes,
        )

    # ------------------------------------------------------------------
    # H_min → health-test param translation
    # ------------------------------------------------------------------

    def update_health_test_params(
        self,
        source,                # QuartzEntropySource; runtime-typed to avoid circular import
        stress_level: int,
        crystal_id: str,
    ) -> dict:
        for fp in self._load():
            if fp.crystal_id == crystal_id and fp.stress_level == stress_level:
                if "Simulated" in fp.backend_class:
                    raise SimulatedCalibrationError(
                        f"refusing to surface H_min from a simulated calibration "
                        f"(backend={fp.backend_class}); real hardware required"
                    )
                # SP 800-90B §4.4.1 / §4.4.2 conservative cutoffs.
                h = max(fp.h_min_estimate, 0.001)
                alpha = 2 ** -30
                rct_cutoff = int(math.ceil(1 + (-math.log2(alpha)) / h))
                apt_window = 1024
                # Critical binomial threshold approximation (normal-approx tail)
                p = 2 ** -h
                from math import sqrt
                mean = apt_window * p
                sigma = math.sqrt(apt_window * p * (1 - p))
                # 6-sigma overshoot for very small alpha; clamp to window
                apt_cutoff = int(min(apt_window, math.ceil(mean + 6 * sigma)))
                return {
                    "h_min": fp.h_min_estimate,
                    "rct_cutoff": rct_cutoff,
                    "apt_window": apt_window,
                    "apt_cutoff": apt_cutoff,
                    "source_crystal_id": crystal_id,
                    "source_stress_level": stress_level,
                    "calibrated_at": fp.calibrated_at,
                }
        raise CalibrationNotFoundError(
            f"no fingerprint for crystal_id={crystal_id!r} "
            f"stress_level={stress_level}"
        )

    # ------------------------------------------------------------------
    # Report
    # ------------------------------------------------------------------

    def export_report(self, path: str | Path,
                      stress_level: int | None = None) -> None:
        path = Path(path)
        report = self.discriminability_report(stress_level)
        lines = []
        lines.append("# Crystal Calibration — Discriminability Report")
        lines.append("")
        lines.append(f"Stress level filter: {stress_level}")
        lines.append(f"Crystals: {len(report.crystal_ids)} "
                     f"({', '.join(report.crystal_ids) or 'none'})")
        lines.append("")
        lines.append(f"min inter-crystal distance:  "
                     f"{_fmt_maybe(report.min_inter_distance)}")
        lines.append(f"mean inter-crystal distance: "
                     f"{_fmt_maybe(report.mean_inter_distance)}")
        lines.append(f"max inter-crystal distance:  "
                     f"{_fmt_maybe(report.max_inter_distance)}")
        lines.append(f"max intra-crystal distance:  "
                     f"{_fmt_maybe(report.max_intra_distance)}")
        lines.append("")
        lines.append(f"PUF assessment: {report.puf_assessment}  "
                     f"(tier {report.puf_tier})")
        lines.append(f"Recommended H_min: "
                     f"{_fmt_maybe(report.recommended_h_min)}")
        lines.append(f"Recommended identity threshold: "
                     f"{_fmt_maybe(report.recommended_identity_threshold)}")
        if report.puf_assessment == "falsified":
            lines.append("")
            lines.append(
                "**T3 PUF claim FALSIFIED** — crystal fingerprints are not "
                "reliably distinguishable at the measured stress levels. "
                "The decoy field steganographic property is NOT supported "
                "by this installation."
            )
        if report.notes:
            lines.append("")
            lines.append("Notes: " + report.notes)
        lines.append("")
        lines.append("## Pairwise distances")
        for a in report.crystal_ids:
            for b, d in report.pairwise_distances.get(a, {}).items():
                if a < b:
                    lines.append(f"  {a} ↔ {b}: {d:.4f}")
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _fmt_maybe(x: float | None) -> str:
    return "n/a" if x is None else f"{x:.4f}"
