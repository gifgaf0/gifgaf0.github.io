# OP-2.58.2d Item D1 — §3.6(b) F_L union dimension result

**Date:** May 27, 2026
**Brief:** CLAUDE_CODE_BRIEF_08 §4 (Item D1)
**Status:** Pre-freeze. Exact F_q-rank on the kernel basis only — no §2.58.B
attack executed at either q. Brief §7 permits both q values for D1.
**Feeds:** the §3.6(b) dimension pin.
**Input:** `op_2_58_2d_D1_fano_union_dimension.py`.

---

## 1. Results

| quantity | value |
|---|---|
| **rank_911** (q = 911) | **14** |
| **rank_spec** (q = 4,294,977,961) | **14** |

The two ranks **agree**; no q-dependent discrepancy to flag.

`M_union` is 16 × 56 (eight F_q-basis vectors per line × seven lines). Its
exact F_q-rank — computed by Gaussian elimination with modular inverses, not
floating-point SVD — is 14 at both primes. Cross-check: stacking all 7 × 12 =
84 raw kernel generators gives the identical rank 14 at both primes (rank is
basis-independent).

## 2. Sanity checks (§4.2 step 5)

At both q = 911 and q = 4,294,977,961:

- Every K_{a,b} (all 21 pairs) has F_q-rank **4** — the bases are non-degenerate.
- Every F_L (all 7 lines) has F_q-rank **8** — the "16→8" drop holds exactly.

So the 8-dimensionality of each individual subspace is confirmed at spec scale,
not only at toy scale.

## 3. Outcome classification (§4.3)

Rank 14 falls in the **"between 9 and 15"** band: the F_L overlap is partial but
real, and the union dimension (14) is meaningfully smaller than the naïve
disjoint expectation (56) and below the ambient dimension (16). This is the
**expected outcome given F4** (the seven F_L overlap). Neither edge case is hit:

- Not rank 8 (the F_L are not all the same subspace).
- Not rank 16 (the union does not span all of F_q^16 — a 2-dimensional
  complement of the ambient 16D block lies in no F_L).

No structural-finding paragraph is required for ledger escalation; the result is
the anticipated one.

## 4. §3.6(b) PATCH STRING

This one sentence replaces the Rev 3 §3.6(b) deferral "the exact dimension is
fixed by the rank of the stacked kernel basis at q":

> The union of the seven F_L has dimension **14** at q = 911 and dimension
> **14** at q = 4,294,977,961, computed as the exact F_q-rank of the stacked
> kernel basis (16 × 56) — see `tools/op_2_58_2d_D1_fano_union_dimension.py`.

## 5. Budget consequence note (§4.5; informational, no §4.2 change)

rank_spec = 14 is far below the disjoint expectation of 56, so the (b)
Fano-projected basis acts on a meaningfully smaller per-block subspace (14 of
the ambient 16 dimensions) than a disjoint-F_L assumption would predict. This is
favourable to the attacker (smaller lattice → faster BKZ). Per §4.5 this does
**not** trigger a §4.2 budget revision before freeze — the 30-day budget is a
hard ceiling either way. Noted only.
