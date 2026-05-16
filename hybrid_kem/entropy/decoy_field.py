"""Decoy crystal field — physical steganography for the quartz source.

A surrounding population of crystals in independently varying stress
states, indistinguishable in signal space from the keyed crystals.
The keyed set produces the entropy; the decoys add noise channels
that an adversary scanning the aggregate cannot trivially separate
from the keyed channels.

See ``quartz_entropy_source.py`` for the surrounding architecture
and ``Brief 04 / Security Notes`` for the assumptions under which
this layer provides defensive value.
"""

from __future__ import annotations

import hashlib
import os
import random as _random

from .quartz_entropy_source import ScheduleEntry, StressSchedule


class DecoyField:
    """Manages an independent population of crystals in varying stress states."""

    def __init__(
        self,
        n_decoy_crystals: int,
        n_levels: int = 4,
        change_interval_ms: int = 200,
        rng_seed: bytes | None = None,
    ):
        if n_decoy_crystals < 1:
            raise ValueError("n_decoy_crystals must be >= 1")
        if n_levels < 1:
            raise ValueError("n_levels must be >= 1")
        if change_interval_ms <= 0:
            raise ValueError("change_interval_ms must be positive")
        self.n_decoy_crystals = n_decoy_crystals
        self.n_levels = n_levels
        self.change_interval_ms = change_interval_ms
        seed_bytes = rng_seed if rng_seed is not None else os.urandom(32)
        self._rng = _random.Random(int.from_bytes(seed_bytes[:8], "big"))
        self._current: list[tuple[int, int]] = []
        self.advance()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def current_schedule(self) -> list[tuple[int, int]]:
        """Return ``[(crystal_id, stress_level), ...]`` for the current slice."""
        return list(self._current)

    def advance(self) -> None:
        """Re-roll the decoy state to a new uniformly random configuration."""
        self._current = [
            (c, self._rng.randrange(0, self.n_levels))
            for c in range(self.n_decoy_crystals)
        ]

    def overlap_fraction(self, keyed_schedule: StressSchedule) -> float:
        """Fraction of keyed time slices where at least one decoy crystal is
        in the same stress level as some keyed crystal.

        Computed analytically across the union of slot starts: for each
        distinct keyed-slot start time, gather the set of keyed levels
        present, then test whether any decoy state (re-rolled afresh per
        keyed slot, mirroring the simulator's behaviour) hits one of
        those levels. Returns a float in ``[0, 1]``; higher is better
        for steganography. Tests expect ``> 0.5`` with the default
        parameters.
        """
        if not keyed_schedule:
            return 0.0
        # Group keyed slots by start time.
        by_start: dict[int, set[int]] = {}
        for e in keyed_schedule:
            by_start.setdefault(e.start_ms, set()).add(e.stress_level)
        n_slots = len(by_start)
        hits = 0
        for start, keyed_levels in by_start.items():
            decoy_levels = {self._rng.randrange(0, self.n_levels)
                            for _ in range(self.n_decoy_crystals)}
            if keyed_levels & decoy_levels:
                hits += 1
        return hits / n_slots
