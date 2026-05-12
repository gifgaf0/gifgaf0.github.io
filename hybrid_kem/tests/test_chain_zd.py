"""Tests for the chain × ZD labelling probe (Brief 02_CHAIN_ZD).

Three exact-fact assertions on the artefacts produced by
``tools/chain_enumerate.py`` and ``tools/chain_zd_labelling.py``:

1. Every chain's manifest labels exactly 84 ZD quadruples.
2. Every ZD quadruple appears in every chain's manifest (no quadruple
   is lost or duplicated by the labelling).
3. The verdict produced by the labelling step is exactly one of the
   two values the brief allows: ``chain_distinguishing`` or
   ``chain_invariant``.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

_TOOLS = Path(__file__).resolve().parents[2] / "tools"
_MANIFEST = _TOOLS / "chain_zd_manifest.json"
_COMPARISON = _TOOLS / "chain_zd_comparison.json"


def _ensure_artefacts():
    if not _MANIFEST.exists():
        subprocess.run([sys.executable,
                        str(_TOOLS / "chain_enumerate.py")],
                       check=True, cwd=_TOOLS.parent)
    if not _COMPARISON.exists():
        subprocess.run([sys.executable,
                        str(_TOOLS / "chain_zd_labelling.py")],
                       check=True, cwd=_TOOLS.parent)


def test_manifest_has_84_pairs_per_chain():
    _ensure_artefacts()
    manifest = json.loads(_MANIFEST.read_text())
    assert manifest["num_quads"] == 84
    for chain in manifest["chains"]:
        assert len(chain["labels"]) == 84, (
            f"chain at fixed point {chain['fixed_point']} has "
            f"{len(chain['labels'])} labels, expected 84"
        )


def test_manifest_covers_all_zd_pairs():
    _ensure_artefacts()
    manifest = json.loads(_MANIFEST.read_text())
    # Reference: the set of 84 quadruple-keys from the first chain.
    first = {entry["quad"] for entry in manifest["chains"][0]["labels"]}
    assert len(first) == 84
    for chain in manifest["chains"][1:]:
        keys = {entry["quad"] for entry in chain["labels"]}
        assert keys == first, (
            f"chain at fixed point {chain['fixed_point']} covers a "
            f"different set of quadruples than chain 1"
        )


def test_verdict_is_one_of_two_values():
    _ensure_artefacts()
    comparison = json.loads(_COMPARISON.read_text())
    assert comparison["verdict"] in ("chain_distinguishing", "chain_invariant"), (
        f"unexpected verdict: {comparison['verdict']!r}"
    )
