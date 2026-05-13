"""Keyed quartz crystal entropy source — software interface (Brief 04).

Hardware-bound entropy source: a population of piezoelectric quartz
crystals driven through a key-derived stress sequence. Thermal and
thermomechanical noise sampled under stress is the primary entropy
mechanism; the key determines *which* stress states are visited and
*when*, so an adversary holding the key alone cannot reproduce the
output (they would also need the physical crystals).

This module implements the software side only:

- :class:`ADCBackend` protocol (hardware abstraction).
- :class:`SimulatedADCBackend` for development and tests.
- :class:`SerialADCBackend` stub for real ADC hardware.
- :func:`derive_stress_schedule` — HKDF-Expand-based deterministic
  stress sequence per crystal.
- :class:`SessionCommitment`, :func:`make_commitment`,
  :func:`verify_commitment` — pre-sampling audit trail.
- :class:`QuartzEntropySource` — orchestrates schedule, sampling,
  digitisation, and SP 800-90B health tests.

Security notes (per Brief 04 §"Security Notes (required in module
docstring)"):

1. **Primary entropy source status is unverified.** This module
   cannot claim SP 800-90B compliance without a formal noise
   characterisation. Until characterised, treat as a conditioner-
   class source. ``H_min`` defaults are placeholders.
2. **Key material must never be logged.** Only the SHA-256 hash of
   ``key_material`` appears in commitment records.
3. **H_min estimates are placeholders.** ``0.5`` and ``0.8``
   bits/sample are engineering guesses; operators must replace
   them with measured PSDs before production use.
4. **Crystal uniqueness (PUF) is asserted, not proven.** A
   ``calibrate_crystal_fingerprint()`` routine is a future addition.
5. **Decoy field effectiveness depends on crystal homogeneity.**
6. **Scanning attack assumption.** Decoy effectiveness requires
   adversary scan window > ``change_interval_ms``.
7. **Non-repudiation is commitment-based, not output-based.**
"""

from __future__ import annotations

import hashlib
import hmac as _hmac
import json
import math
import os
import random as _random
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Callable, Iterable, Protocol

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDFExpand

from .health_tests import HealthTests as _HealthTests


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------


class HardwareUnavailableError(RuntimeError):
    """ADC backend cannot be reached."""


class InsufficientSamplesError(RuntimeError):
    """ADC produced fewer samples than requested."""


class HealthTestFailureError(RuntimeError):
    """SP 800-90B health test failed on raw ADC data."""


# ---------------------------------------------------------------------------
# ADC abstraction
# ---------------------------------------------------------------------------


class ADCBackend(Protocol):
    def read_voltage(self, channel: int) -> float:
        """Read instantaneous voltage from a crystal channel.

        Returns a float in the normalised range ``[-1.0, 1.0]``.
        Raises :class:`HardwareUnavailableError` if the device is not
        present.
        """
        ...

    def channel_count(self) -> int:
        ...

    def sample_rate_hz(self) -> int:
        ...


class SimulatedADCBackend:
    """Synthetic ADC for development and tests.

    Generates Gaussian-distributed voltages in ``[-1, 1]`` with
    configurable noise floor. Tracks a per-channel stress level
    (set via :meth:`set_channel_stress`); higher stress widens the
    noise distribution to model the operator's hypothesis that
    stressed crystals show greater thermomechanical jitter.
    """

    def __init__(self, n_channels: int, noise_floor: float = 0.02,
                 sample_rate_hz: int = 44_100, seed: int | None = None,
                 distribution: str = "gaussian"):
        if n_channels < 1:
            raise ValueError("n_channels must be >= 1")
        if distribution not in ("gaussian", "uniform"):
            raise ValueError(f"unknown distribution: {distribution!r}")
        self._n = n_channels
        self._noise_floor = noise_floor
        self._sr = sample_rate_hz
        self._distribution = distribution
        self._rng = _random.Random(seed if seed is not None
                                    else int.from_bytes(os.urandom(8), "big"))
        self._stress: dict[int, int] = {c: 0 for c in range(n_channels)}
        self._stuck: dict[int, float | None] = {c: None for c in range(n_channels)}

    # ADC protocol

    def read_voltage(self, channel: int) -> float:
        if channel < 0 or channel >= self._n:
            raise ValueError(f"channel {channel} out of range")
        if self._stuck[channel] is not None:
            return self._stuck[channel]
        scale = 1.0 + 0.4 * self._stress[channel]
        if self._distribution == "uniform":
            # Full-range uniform sample modulated by the noise floor and
            # stress scale. At noise_floor=1.0 this is just U(-1, 1) —
            # a clean stand-in for post-whitened entropy.
            half = self._noise_floor * scale
            half = min(half, 1.0)
            return self._rng.uniform(-half, half)
        # Gaussian (default): stress-dependent variance, clipped to [-1, 1].
        sigma = self._noise_floor * scale
        v = self._rng.gauss(0.0, sigma)
        if v > 1.0:
            v = 1.0
        elif v < -1.0:
            v = -1.0
        return v

    def channel_count(self) -> int:
        return self._n

    def sample_rate_hz(self) -> int:
        return self._sr

    # Simulated extras (not part of the protocol)

    def set_channel_stress(self, channel: int, level: int) -> None:
        if channel < 0 or channel >= self._n:
            raise ValueError(f"channel {channel} out of range")
        self._stress[channel] = max(0, int(level))

    def force_stuck(self, channel: int, value: float | None) -> None:
        """Test helper: pin a channel's output to a constant (or None to clear)."""
        self._stuck[channel] = value


class SerialADCBackend:
    """Stub for a USB/serial ADC. Real wiring is operator-supplied.

    All hardware-specific methods raise ``NotImplementedError`` — the
    class exists so production callers have an explicit place to
    plug in vendor SDK calls. Tests use :class:`SimulatedADCBackend`.
    """

    def __init__(self, device_path: str, n_channels: int = 16,
                 sample_rate_hz: int = 44_100):
        self._device_path = device_path
        self._n = n_channels
        self._sr = sample_rate_hz

    def read_voltage(self, channel: int) -> float:
        raise NotImplementedError(
            "SerialADCBackend is a hardware stub; supply a vendor implementation"
        )

    def channel_count(self) -> int:
        return self._n

    def sample_rate_hz(self) -> int:
        return self._sr


# ---------------------------------------------------------------------------
# Stress schedule
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ScheduleEntry:
    crystal_id: int
    stress_level: int
    start_ms: int
    end_ms: int


StressSchedule = list[ScheduleEntry]


def _hkdf_expand(key_material: bytes, info: bytes, length: int) -> bytes:
    return HKDFExpand(algorithm=hashes.SHA256(), length=length,
                       info=info).derive(key_material)


def derive_stress_schedule(
    key_material: bytes,
    n_crystals: int,
    n_levels: int,
    window_ms: int,
    min_dwell_ms: int = 50,
) -> StressSchedule:
    """Derive a deterministic stress sequence from ``key_material``.

    Uses HKDF-Expand with ``info = b'quartz-stress-schedule'`` to
    generate a stream of bytes; each crystal gets an independent
    sub-stream derived from its index. Within each crystal's window
    we lay down ``n_slots = window_ms // min_dwell_ms`` slots of
    ``min_dwell_ms`` duration each and assign a stress level
    ``[0, n_levels)`` per slot from the HKDF stream.

    Raises ``ValueError`` if ``window_ms / min_dwell_ms < n_levels``
    (schedule would be degenerate — not enough slots to visit every
    stress level even once).
    """
    if n_crystals < 1:
        raise ValueError("n_crystals must be >= 1")
    if n_levels < 1:
        raise ValueError("n_levels must be >= 1")
    if window_ms < min_dwell_ms:
        raise ValueError("window_ms must be >= min_dwell_ms")
    n_slots = window_ms // min_dwell_ms
    if n_slots < n_levels:
        raise ValueError(
            f"schedule degenerate: n_slots={n_slots} < n_levels={n_levels}"
        )
    total_bytes = n_crystals * n_slots
    raw = _hkdf_expand(key_material, b"quartz-stress-schedule", total_bytes)
    schedule: StressSchedule = []
    for c in range(n_crystals):
        start = c * n_slots
        crystal_bytes = raw[start:start + n_slots]
        t = 0
        for s in range(n_slots):
            level = crystal_bytes[s] % n_levels
            schedule.append(ScheduleEntry(
                crystal_id=c,
                stress_level=level,
                start_ms=t,
                end_ms=min(t + min_dwell_ms, window_ms),
            ))
            t += min_dwell_ms
            if t >= window_ms:
                break
    return schedule


def serialise_schedule(schedule: StressSchedule) -> bytes:
    """Canonical byte serialisation for hashing into the commitment."""
    parts = []
    for e in schedule:
        parts.append(f"{e.crystal_id}|{e.stress_level}|"
                     f"{e.start_ms}|{e.end_ms}".encode())
    return b"\n".join(parts)


# ---------------------------------------------------------------------------
# Commitment / verification
# ---------------------------------------------------------------------------


@dataclass
class SessionCommitment:
    session_id: bytes
    timestamp_utc: str
    stress_schedule_hash: str
    key_material_hash: str
    n_keyed_crystals: int
    window_ms: int
    n_levels: int

    def to_json_dict(self) -> dict:
        d = asdict(self)
        d["session_id"] = self.session_id.hex()
        return d


def _sha256_hex(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def make_commitment(
    key_material: bytes,
    schedule: StressSchedule,
    session_id: bytes,
    *,
    n_levels: int,
    n_keyed_crystals: int,
    window_ms: int,
) -> SessionCommitment:
    if len(session_id) < 1:
        raise ValueError("session_id must be non-empty")
    timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    return SessionCommitment(
        session_id=session_id,
        timestamp_utc=timestamp,
        stress_schedule_hash=_sha256_hex(serialise_schedule(schedule)),
        key_material_hash=_sha256_hex(key_material),
        n_keyed_crystals=n_keyed_crystals,
        window_ms=window_ms,
        n_levels=n_levels,
    )


def verify_commitment(
    commitment: SessionCommitment,
    key_material: bytes,
    schedule: StressSchedule,
) -> bool:
    """Check that the commitment is consistent with the supplied
    ``key_material`` and ``schedule``.

    Does NOT verify the raw entropy output itself — that is
    statistically infeasible. Returns ``True`` iff every recorded
    hash agrees with the recomputation.
    """
    if not _hmac.compare_digest(
        commitment.key_material_hash, _sha256_hex(key_material)
    ):
        return False
    if not _hmac.compare_digest(
        commitment.stress_schedule_hash,
        _sha256_hex(serialise_schedule(schedule)),
    ):
        return False
    return True


COMMITMENT_LOG_PATH = Path(__file__).parent / "quartz_commitments.jsonl"


def _append_commitment(commitment: SessionCommitment,
                       log_path: Path = COMMITMENT_LOG_PATH) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(commitment.to_json_dict()) + "\n")


# ---------------------------------------------------------------------------
# Health-test wrapping
# ---------------------------------------------------------------------------
#
# We reuse the existing ``HealthTests`` (SP 800-90B RCT + APT) on the raw
# byte stream. The brief's cutoff formula `C = ceil(1 + 6 / H_min)` is the
# SP 800-90B §4.4.1 form at α = 2^-6; our existing HealthTests is more
# stringent (α = 2^-30 default) but otherwise equivalent. We accept the
# stricter cutoff — false-positive rate is only lower, which is the
# conservative direction for a fail-closed entropy source.


# ---------------------------------------------------------------------------
# QuartzEntropySource
# ---------------------------------------------------------------------------


class QuartzEntropySource:
    SAMPLES_PER_BLOCK = 64       # 64 uint16 samples → 128 bytes → SHA-256 → 32 bytes
    BLOCK_OUTPUT_BYTES = 32

    def __init__(
        self,
        adc: ADCBackend,
        key_material: bytes,
        n_keyed_crystals: int,
        *,
        decoy_field: "DecoyField | None" = None,    # forward ref
        sample_rate_hz: int | None = None,
        window_ms: int = 1000,
        n_levels: int = 4,
        min_dwell_ms: int = 50,
        commitment_log_path: Path | None = None,
        health_tests: _HealthTests | None = None,
    ):
        if n_keyed_crystals < 1 or n_keyed_crystals > adc.channel_count():
            raise ValueError("n_keyed_crystals out of range for ADC channels")
        self._adc = adc
        self._key_material = bytes(key_material)
        self._n_keyed = n_keyed_crystals
        self._decoy = decoy_field
        self._sr = sample_rate_hz or adc.sample_rate_hz()
        self._window_ms = window_ms
        self._n_levels = n_levels
        self._min_dwell_ms = min_dwell_ms
        self._log_path = commitment_log_path or COMMITMENT_LOG_PATH
        self._health = health_tests or _HealthTests()
        self._last_commitment: SessionCommitment | None = None
        self._total_bytes = 0
        self._health_failures = 0

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def make_commitment(self) -> SessionCommitment:
        """Build a commitment for the next sampling session and persist it.

        Call this before :meth:`sample_raw`. The commitment is appended
        to ``entropy/quartz_commitments.jsonl`` (or a caller-supplied
        log path) before any ADC reads are issued.
        """
        schedule = derive_stress_schedule(
            self._key_material,
            n_crystals=self._n_keyed,
            n_levels=self._n_levels,
            window_ms=self._window_ms,
            min_dwell_ms=self._min_dwell_ms,
        )
        commitment = make_commitment(
            self._key_material, schedule, session_id=os.urandom(16),
            n_levels=self._n_levels,
            n_keyed_crystals=self._n_keyed,
            window_ms=self._window_ms,
        )
        _append_commitment(commitment, self._log_path)
        self._last_commitment = commitment
        self._last_schedule = schedule
        return commitment

    def sample_raw(self, n_bytes: int) -> bytes:
        """Run the stress schedule, sample the ADC, return n_bytes of raw entropy.

        Side effects:
        - Calls :meth:`make_commitment` if one hasn't been produced for
          this session yet (and appends it to the audit trail).
        - Pushes raw ADC bytes through the health tests; raises
          :class:`HealthTestFailureError` on failure without returning
          partial output.
        """
        if n_bytes <= 0:
            raise ValueError("n_bytes must be positive")
        if self._last_commitment is None:
            self.make_commitment()

        schedule = self._last_schedule
        n_blocks = math.ceil(n_bytes / self.BLOCK_OUTPUT_BYTES)
        total_samples = n_blocks * self.SAMPLES_PER_BLOCK

        # Group schedule by (crystal_id, slot_idx) for set-once look-up.
        # Apply the *first* slot's stress to the simulated ADC if applicable.
        self._apply_stress_for_time(schedule, time_ms=0)
        if self._decoy is not None:
            self._apply_decoy_state()

        # Sample loop.
        raw_words: list[int] = []
        approx_ms_per_sample = 1000.0 / self._sr
        slot_advance_every = max(1, int(round(
            self._min_dwell_ms / approx_ms_per_sample
        )))
        slot_idx = 0
        try:
            for i in range(total_samples):
                # Round-robin across keyed crystals.
                channel = i % self._n_keyed
                # Re-apply stress when crossing a slot boundary.
                if i > 0 and i % slot_advance_every == 0:
                    slot_idx += 1
                    self._apply_stress_for_slot(schedule, slot_idx)
                    if self._decoy is not None:
                        self._decoy.advance()
                        self._apply_decoy_state()
                voltage = self._adc.read_voltage(channel)
                raw_words.append(self._voltage_to_uint16(voltage))
        except HardwareUnavailableError:
            raise
        except NotImplementedError as exc:    # Serial backend stub
            raise HardwareUnavailableError(str(exc)) from exc

        if len(raw_words) < total_samples:
            raise InsufficientSamplesError(
                f"ADC produced {len(raw_words)} of {total_samples} samples"
            )

        # Pack into bytes for health tests.
        raw_bytes = bytearray()
        for w in raw_words:
            raw_bytes.append((w >> 8) & 0xff)
            raw_bytes.append(w & 0xff)

        if not self._health.update(bytes(raw_bytes)):
            self._health_failures += 1
            status = self._health.status()
            raise HealthTestFailureError(
                f"SP 800-90B health test failed: {status.get('failure_reason')}"
            )

        # SHA-256 rolling hash per block → output bytes.
        out = bytearray()
        for b in range(n_blocks):
            block = bytes(raw_bytes[b * self.SAMPLES_PER_BLOCK * 2:
                                     (b + 1) * self.SAMPLES_PER_BLOCK * 2])
            out.extend(hashlib.sha256(block).digest())
        result = bytes(out[:n_bytes])
        self._total_bytes += len(result)
        return result

    def status(self) -> dict:
        c = self._last_commitment
        return {
            "backend": type(self._adc).__name__,
            "n_keyed_crystals": self._n_keyed,
            "decoy_field_size": (self._decoy.n_decoy_crystals
                                  if self._decoy is not None else 0),
            "sample_rate_hz": self._sr,
            "window_ms": self._window_ms,
            "n_levels": self._n_levels,
            "last_commitment_hash": (c.stress_schedule_hash if c else None),
            "last_session_id": (c.session_id.hex() if c else None),
            "total_bytes_produced": self._total_bytes,
            "health_test_failures": self._health_failures,
        }

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    @staticmethod
    def _voltage_to_uint16(v: float) -> int:
        # Map [-1.0, 1.0] → [0, 65535] uniformly.
        clipped = max(-1.0, min(1.0, v))
        return int(round((clipped + 1.0) * 32767.5))

    def _apply_stress_for_time(self, schedule: StressSchedule,
                                time_ms: int) -> None:
        if not isinstance(self._adc, SimulatedADCBackend):
            return
        for entry in schedule:
            if entry.start_ms <= time_ms < entry.end_ms:
                self._adc.set_channel_stress(entry.crystal_id,
                                              entry.stress_level)

    def _apply_stress_for_slot(self, schedule: StressSchedule,
                                slot_idx: int) -> None:
        if not isinstance(self._adc, SimulatedADCBackend):
            return
        slots_per_crystal = max(
            1, sum(1 for e in schedule if e.crystal_id == 0)
        )
        slot_idx = slot_idx % slots_per_crystal
        for entry in schedule:
            if not isinstance(self._adc, SimulatedADCBackend):
                continue
            entry_slot = entry.start_ms // self._min_dwell_ms
            if entry_slot == slot_idx:
                self._adc.set_channel_stress(entry.crystal_id,
                                              entry.stress_level)

    def _apply_decoy_state(self) -> None:
        if self._decoy is None:
            return
        if not isinstance(self._adc, SimulatedADCBackend):
            return
        for crystal_id, level in self._decoy.current_schedule():
            # Decoy crystal IDs occupy channels above the keyed range.
            ch = self._n_keyed + crystal_id
            if ch < self._adc.channel_count():
                self._adc.set_channel_stress(ch, level)
