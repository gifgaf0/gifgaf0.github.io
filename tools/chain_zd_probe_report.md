# Chain × ZD Labelling Probe (OP §2.24.2)

> *T1 = measured fact (script reproducible from
> `tools/chain_enumerate.py` + `tools/chain_zd_labelling.py`).
> T2 = structural argument used to interpret the measurement.
> Eddington-Maneuver filter applied per master doc §0: no
> hardness claim is made from labelling phenomena alone.*

## Verdict

**Chain-distinguishing.** [T1] All 7 chains
`A₄ᵢ < S₄ᵢ < PSL(2, 7)` (one per Fano point `i ∈ {1..7}`) induce
**pairwise distinct partitions** of the 84 sedenion zero-divisor
quadruples over F_911. None of the 21 chain-pairs gives identical
labellings; none gives the same partition up to a label
permutation; all 21 give different partitions.

But [T2]: the 7 chains are PSL(2, 7)-conjugate (they are the
point-stabilisers of conjugate Fano points). Under that
conjugation they collapse to **a single conjugacy class**. The
chain-distinguishing labelling is therefore a **coordinate-
labelling phenomenon** — knowing the labels tells you which
Fano point was used as the chain base, but the underlying
structure is invariant under the same PSL(2, 7) that already
acts on the 14-element basis. **No new hardness primitive
emerges.**

This is the Eddington-Maneuver flag in action: the "different
labellings" observation could be sold as "the chain parameter
adds entropy"; the honest reading is that the chain is one of
7 PSL(2, 7)-equivalent coordinate choices, observable to anyone
with access to the labelled data.

## Status of OP §2.24.2

OP §2.24.2 asks: *Does the 42-pair set decompose as 2 × 21
respecting Fano geometry?*

[T1] **Not as "2 × 21".** Each chain's A_4 has **8 orbits** on
the 84 quadruples, with sizes `2 × 6 + 6 × 12 = 12 + 72 = 84`.
The orbit sizes are not the 21 + 21 = 42 (at the index-pair
level) or 42 + 42 = 84 (at the quadruple level) that the
question literally asks about.

[T1] **A different chain-dependent decomposition does exist.**
Each chain partitions the 84 quadruples into 8 orbits, and the
seven chains give seven different partitions. So OP §2.24.2's
spirit (chain induces a decomposition) is confirmed; its letter
(2 × 21) is not.

[T2] **Open follow-up out of scope.** Per the brief: "if
chain-distinguishing, whether the chain parameter adds defensive
value is out of scope for this brief." Recorded for a future
brief.

## OP §2.24.1 — also closed by this brief

[T1] **Full PSL(2, 7) preserves the 84 ZD quadruples.** All 168
elements of PSL(2, 7) (constructed here as the GL(3, F_2) action
on Fano points, extended to {1..7, 9..15} by index shift)
permute the set of 84 quadruples into itself. The master doc
§1.2 had this confirmed only for the Z_7 Singer subgroup;
this brief extends it to the full group.

## Aut(MultTable) sub-probe

[T1, sample-bounded] No permutation outside PSL(2, 7) was found
that preserves the signed sedenion multiplication table within
**5000 random samples** drawn from `Aut(K₇,₇-matching) =
S_7 ≀ Z_2` (order ≈ 5 × 10⁷). PSL(2, 7) was hit 69 times within
the same sample (consistent with a relative-density estimate of
168 / |S_7 ≀ Z_2| ≈ 3.3 × 10⁻⁶ — though the sampling distribution
is uniform on `Aut(K₇,₇-matching)` and so over-represents PSL(2,
7) elements that have low-conflict ZD-preserving extensions).

[T2] **Not a proof Aut(MultTable) = PSL(2, 7).** With the
sample size used, we can only conclude *no counter-example was
found in the search budget*. A definitive answer would require
enumeration of all `Aut(K₇,₇-matching)` elements, or a structural
argument tying Aut(MultTable) to PSL(2, 7) explicitly. Recorded
as a residual open question.

## Concrete labelling difference (T1 example)

Showing the first four ZD quadruples in lex order and how chains
1 and 2 label them differently:

| ZD quadruple | Chain 1 label | Chain 2 label |
|---|---:|---:|
| `(1,10) ∪ (4,15)` | 0 | 0 |
| `(1,10) ∪ (5,14)` | 0 | 1 |
| `(1,10) ∪ (6,13)` | 1 | 0 |
| `(1,10) ∪ (7,12)` | 1 | 1 |

Chain 1 groups quadruples 1+2 and 3+4; chain 2 groups 1+3 and
2+4. Same four quadruples; different orbital structure under
the chain's A_4 action.

Orbit sizes per chain (sorted by lex-smallest orbit
representative):

| Chain at fixed point | Orbit sizes |
|---|---|
| 1 | [12, 12, 12, 12, 12, 6, 12, 6] |
| 2 | [12, 12, 12, 12, 6, 12, 12, 6] |
| 3 | [12, 12, 12, 12, 6, 12, 12, 6] |
| 4 | [12, 12, 12, 12, 6, 12, 12, 6] |
| 5 | [12, 12, 12, 12, 12, 12, 6, 6] |
| 6 | [12, 12, 12, 12, 6, 6, 12, 12] |
| 7 | [12, 12, 12, 12, 6, 12, 12, 6] |

(Same multiset `{12, 12, 12, 12, 12, 12, 6, 6}` for every chain
— what differs is *which* quadruples land in the 6-orbits vs
12-orbits.)

## CI-protected vs documentation-only

CI-protected (assertions in `hybrid_kem/tests/test_chain_zd.py`):

- `test_manifest_has_84_pairs_per_chain` — every chain labels
  exactly 84 quadruples.
- `test_manifest_covers_all_zd_pairs` — every chain labels the
  same set of 84 quadruples.
- `test_verdict_is_one_of_two_values` — labelling-step verdict
  is one of the two values the brief allows.

Documentation-only (in this report and the manifest JSON):

- The specific "chain-distinguishing" finding (the brief allows
  either answer; we report the one observed).
- The 8-orbits-not-7 finding (the brief assumed 7 labels per
  chain; we report 8 honestly).
- The full PSL(2, 7) preservation of the 84 quadruples
  (extension of OP §2.24.1).
- The Aut(MultTable) spot-check negative result (with sample
  bound).
- The orbit-size table and the chain-1/chain-2 comparison
  example.

## Evidence paths

- `tools/chain_enumerate.py` — builds PSL(2, 7), verifies ZD
  preservation, builds 7 chains, computes labellings.
- `tools/chain_zd_manifest.json` — full manifest of 7 × 84
  labels.
- `tools/chain_zd_labelling.py` — pairwise comparison, verdict.
- `tools/chain_zd_comparison.json` — comparison output.
- `hybrid_kem/tests/test_chain_zd.py` — 3 CI assertions.

## Reproducibility

```bash
python3 tools/chain_enumerate.py            # ~0.4 s
python3 tools/chain_zd_labelling.py         # <0.1 s
pytest hybrid_kem/tests/test_chain_zd.py -v # ~0.4 s
```

Pure CPython; no third-party deps beyond what the rest of the
testbed already pulls in. Wall clock under 1 s end to end.
