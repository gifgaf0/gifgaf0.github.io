"""Chain × ZD labelling — pairwise comparison and verdict.

Loads ``tools/chain_zd_manifest.json`` (produced by
``chain_enumerate.py``), compares the 7 chain labellings pairwise, and
classifies each pair as:

- **identical**: label_i(q) == label_j(q) for every quadruple q.
- **permutation**: same partition of the 84 quadruples (same orbits),
  with the orbit labels relabelled by some permutation of {0..L-1}.
- **distinct**: the orbit partitions themselves differ.

The verdict for OP §2.24.2:

- **chain_invariant**: all 21 chain-pairs are "permutation"-equivalent
  (i.e., every chain gives the same partition of the 84 ZD quadruples
  — the labels themselves are at most relabelled).
- **chain_distinguishing**: at least one chain pair is "distinct" (the
  partitions actually differ).

If chain-distinguishing, we also report how many distinct labelling
classes there are *as partitions* (i.e., quotienting by the trivial
label-permutation), and how many remain after quotienting by the
natural PSL(2,7) action that conjugates the 7 chains into each other.
"""

from __future__ import annotations

import json
from pathlib import Path


def load_manifest(path: Path) -> dict:
    return json.loads(path.read_text())


def labels_dict_for(chain: dict) -> dict[str, int]:
    return {entry["quad"]: entry["label"] for entry in chain["labels"]}


def partition_of(label_map: dict[str, int]) -> tuple[frozenset, ...]:
    """Return the partition (set of frozenset of quads) induced by ``label_map``,
    canonicalised so that two label maps with the same partition compare equal.
    """
    groups: dict[int, list[str]] = {}
    for q, lbl in label_map.items():
        groups.setdefault(lbl, []).append(q)
    return tuple(sorted((frozenset(grp) for grp in groups.values()),
                        key=lambda fs: sorted(fs)[0]))


def compare_chains(c_i: dict, c_j: dict) -> str:
    a = labels_dict_for(c_i)
    b = labels_dict_for(c_j)
    if a == b:
        return "identical"
    if partition_of(a) == partition_of(b):
        return "permutation"
    return "distinct"


def main() -> int:
    in_path = Path("tools/chain_zd_manifest.json")
    manifest = load_manifest(in_path)
    chains = manifest["chains"]
    n = len(chains)
    assert n == 7, n

    pair_results: dict[tuple[int, int], str] = {}
    for i in range(n):
        for j in range(i + 1, n):
            r = compare_chains(chains[i], chains[j])
            pair_results[(i, j)] = r

    counts = {"identical": 0, "permutation": 0, "distinct": 0}
    for r in pair_results.values():
        counts[r] += 1

    # Verdict.
    any_distinct = counts["distinct"] > 0
    verdict = "chain_distinguishing" if any_distinct else "chain_invariant"

    # Distinct partition classes.
    partitions = [partition_of(labels_dict_for(c)) for c in chains]
    distinct_partitions = list({p for p in partitions})
    n_partition_classes = len(distinct_partitions)
    chains_per_class = {}
    for idx, part in enumerate(partitions):
        for cls_id, dp in enumerate(distinct_partitions):
            if part == dp:
                chains_per_class.setdefault(cls_id, []).append(idx)
                break

    out = {
        "verdict": verdict,
        "n_chains": n,
        "n_pairs": len(pair_results),
        "pair_counts": counts,
        "pair_results": {f"{i},{j}": r for (i, j), r in pair_results.items()},
        "distinct_partition_classes": n_partition_classes,
        "chains_per_partition_class": {
            str(cls_id): [chains[idx]["fixed_point"] for idx in chain_idxs]
            for cls_id, chain_idxs in chains_per_class.items()
        },
        "note_on_psl_conjugation": (
            "The 7 chains are PSL(2,7)-conjugate (point-stabilisers of "
            "conjugate Fano points), so under that conjugation they collapse "
            "to a single class. The 'distinct_partition_classes' count above "
            "is the number of *as-labelled* partitions, BEFORE quotienting "
            "by that conjugation. Both numbers are reported because the "
            "operational question for OP §2.24.2 is whether the labels "
            "themselves carry chain-dependent information when computed "
            "in a fixed coordinate system."
        ),
    }
    Path("tools/chain_zd_comparison.json").write_text(json.dumps(out, indent=2)
                                                       + "\n")
    print(f"verdict: {verdict}")
    print(f"  pair counts: {counts}")
    print(f"  distinct partition classes: {n_partition_classes}")
    for cls_id, chain_idxs in chains_per_class.items():
        fps = [chains[idx]["fixed_point"] for idx in chain_idxs]
        print(f"    class {cls_id}: chains at fixed points {fps}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
