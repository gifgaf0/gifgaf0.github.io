# leaky_lwe_ledger_entry.md — Ledger append for the leaky-LWE-Estimator stand-up

**Status**: Branch-resident mirror of the canonical R3 ledger entry, same
pattern as `tools/op_2_58_2d_dfr_reference.md` (§2.66.1 recovery) and
`tools/op_2_58_2d_provenance_correction.md` (Brief 11 Item 1). Proposed
canonical entry number: **§2.69.4** (adjacent to §2.69.1/2/3; not
overwriting; append-only).

**Tier**: R3 (analytic proxy / banked prediction). Not R1, not a closure.

**Anchor commit**: head of the Brief 11 chain (which itself sits on top of
Brief 10.6's basis-(b) ratification + Brief 10.7's σ pin).

---

## §1. Environment (Brief LEAKY-LWE Item 1) — **DONE IN-CONTAINER, validation PASSED (2026-07-13)**

Superseding the earlier "not installable here / deferred to Matt's box" status:

- **Sage version**: `SageMath version 10.9`, installed **in this managed-remote container**
  via **conda-forge / micromamba 2.8.1** (apt `sagemath` is not packaged in Ubuntu noble;
  conda.anaconda.org is reachable through the proxy). Reproduce command in
  `estimator_setup.md` §1.0. Caveat: env is non-persistent (recreate ~15–20 min/session).
- **leaky-LWE-Estimator commit hash**: `0a9caf8bf0f80097724e0c6147194c52c6b90f86`
  (cloned to `/root/leaky-LWE-Estimator`).
- **Validation bikz reproduction (blocking gate, brief §2.3): PASS — exact.** README n=70
  example (`initialize_from_LWE_instance(DBDD, 70, 3301, 70, ...)`): documented
  `dim=141  δ=1.012362  β=45.40`; reproduced `β=45.40  δ=1.012362  dim=141`. Since
  `estimate_attack()` is analytic/deterministic the match is exact, not merely within ±1.
  Script: `Sec5.2_validation/validate_readme.sage`.

Item 1 is now **complete end-to-end in this container** (setup note + install + instrument
validation). Item 3's bracket runs are thereby **unblocked** (Sage present, estimator
validated); the placeholder bikz values in §3 below can be produced here rather than on
Matt's box — pending go-ahead (kept illustrative-not-binding per brief §4.2).

## §2. Hint-structure reconnaissance (Brief LEAKY-LWE Item 2)

Full memo: `hybrid_kem/tools/op_2_58_2d_estimator_recon.md` (per-claim
provenance to file/function/line). Executive summary:

- **(a) LWE parameters** — read from `build_scalar_lwe`
  (`tools/op_2_58_2d_lattice_attack.py:111`):
  n = k·16 (512 spec / 112 k=7 / 224 k=14); q = 4,294,977,961 (spec) / 911
  (toy); m = n (one sample per scalar coord); secret sparse-ternary with
  h_s = 64 (spec) / round(64·k/32) (toy); error per-coord ∈ {−σ, 0, +σ}
  exactly, σ=2 pinned per §2.69.3; per-coord variance 1.33 (Brief 10.7
  §2.69.3 empirical).
- **(b) Hint subspaces** — F_L union rank **14** per block (D1,
  `op_2_58_2d_D1_fano_union_dimension.py`) → complement **2/block**;
  K_{a,b} rank **4** per block → complement **12/block**.
- **(c) LOAD-BEARING FORK — resolved PER-BLOCK. NO HALT.**
  `tools/op_2_58_2d_construction.py:130` samples `a, b = pairs[...]`
  INSIDE the `for i in range(k):` loop (line 121). `pair` is stored as a
  length-k list of tuples (line 116). Every block gets an independent
  uniform pair. **Joint pair guess space = 21^k**: feasible-with-effort
  at k=7 (1.8×10⁹), infeasible at k=14 (3.3×10¹⁸) and k=32 (**4.4×10⁴²**).
- **(d) All blocks carry ZD-noise**: yes. `for i in range(k):` is
  monolithic; no conditional. Hint count scales linearly with k.
- **(e) Ratified basis-(b) reading** = **(I) F_L-restriction** (per
  `tools/op_2_58_2d_basis_b_ratification.md`). DBDD correspondence:
  reading (I) restricted-to-14-dim ↔ 2 hints/block on the F_L⊥
  complement = **the weak bracket**. Strong bracket (12/block) is the
  oracle-with-per-block-pair scenario.

**Hint-count table** (from recon §2.3):

| bracket | hints/block | spec k=32 | toy k=7 | toy k=14 | attacker-free? |
|---------|-------------|-----------|---------|----------|----------------|
| Weak (F_L union complement) | 2 | 64 | 14 | 28 | YES |
| Strong (per-pair K_{a,b} complement) | 12 | 384 | 84 | 168 | requires 21^k pair guess |

## §3. Bracket bikz values (Brief LEAKY-LWE Item 3) — DEFERRED

The parameterised harness (`hybrid_kem/tools/op_2_58_2d_estimator.sage`)
is authored and syntax-checked as valid Python; delegation to the on-branch
kernel-basis machinery (`_fano_union_basis`,
`op_2252_v2_kernel_involution.rref_kernel`) is verified from this
container. The bracket bikz values themselves — the numbers this ledger
row should carry — are Matt's box's output, since Sage is not installable
here. Placeholders:

- Weak bracket (2·k hints):
  - toy k=7 (14 hints): bikz = **_______** (illustrative not binding)
  - toy k=14 (28 hints): bikz = **_______** (illustrative not binding)
  - spec k=32 (64 hints): bikz = **_______** (illustrative not binding)
- Strong bracket (12·k hints):
  - toy k=7 (84 hints): bikz = **_______** (illustrative not binding)
  - toy k=14 (168 hints): bikz = **_______** (illustrative not binding)
  - spec k=32 (384 hints): bikz = **_______** (illustrative not binding; may be
    slow with DDGR successive integration → fallback to eprint 2023/777
    single-stroke integrator per brief §4.3)

Matt's Item-3 run will fill these values. Each is labelled **illustrative,
not the OP-2.58.2d prediction** per brief §4.2. The binding single-number
bikz is Phase 2's job (see §5 below).

## §4. Discipline statements (verbatim, per brief §5)

1. **R3 prediction/proxy**: every bikz produced by this stand-up is a
   banked prediction — an analytic upper bound on the pair-classifier β
   at which the schedule would fire, per brief §1. Never quoted as
   closure of OP-2.58.2 or OP-2.58.2d.
2. **Does not substitute for the 42-run empirical schedule**: the
   pre-registration §5 declarations require the empirical run. A proxy
   positive does not authorize skipping it; a proxy null does not
   authorize declaring §5.1.
3. **Does not close OP-2.58.2 or OP-2.58.5**: this brief informs the
   spend decision. Closure remains conditional on the empirical run per
   pre-reg §5.1 + one of {OP-2.58.2c, OP-2.58.2e} per §2.66.2 status.
4. **Frozen pre-registration untouched**: running the leaky-LWE-Estimator
   is not "running lattice-reduction code against the §2.58.B construction
   at the parameters of §3.1" (frozen pre-reg §6). §6's retraction clause
   is not engaged. No Rev 6. No §3.* retraction.

## §5. What's next (Phase 2 — session-side, not this brief)

The binding single-number bikz — the one that names which schedule β the
proxy predicts — requires:

1. **The weak-bracket bikz** (attacker-free hints; direct DBDD prediction)
   — from Matt's harness run once Sage + estimator + validation are in
   place.
2. **The strong-bracket bikz × 21^k guess factor** — the estimator models
   hint-reduction; the guess-space cost is the other half. At spec
   (21^32 ≈ 4.4×10^42), a naive multiplication of the strong-bracket
   bikz by 2^{142} is dominated by the guess factor, which effectively
   makes strong-bracket per-block pair enumeration infeasible unless a
   meet-in-the-middle or Fano-structural refinement collapses it.
3. **Whichever bracket bounds the pair-classifier β lower** — that is
   the binding proxy prediction.

Phase 2 is a separate session-side derivation. This brief does NOT
attempt it.

## §6. No code changes to project

- `pyproject.toml`: unchanged.
- Project pytest suite: unchanged (this brief adds no runnable Python
  tests; the .sage harness is a separate-interpreter deliverable).
- ruff clean: confirmed on `hybrid_kem/tools/` and unchanged `tools/`.
- Frozen `OP_2_58_2d_staging_PREREGISTRATION.md`: unchanged. SHA-256
  still `ecbb7dfc19d3491d37d6a6b961387b0e3e70637c0dd47a958d19d4fa5ffdd12e`
  (Brief 10.6 Item 3 anchor + Brief 11 Audit Entry 002 hash).

## §7. Cross-references

- **Brief LEAKY-LWE** (`CLAUDE_CODE_BRIEF_LEAKY_LWE_ESTIMATOR.md`, this
  session's upload).
- **`hybrid_kem/tools/estimator_setup.md`** — Item 1 setup + validation
  gate (Matt's action items).
- **`hybrid_kem/tools/op_2_58_2d_estimator_recon.md`** — Item 2 recon memo
  with per-claim provenance.
- **`hybrid_kem/tools/op_2_58_2d_estimator.sage`** — Item 3 parameterised
  harness.
- **DDGR 2020** (eprint 2020/292 §5): "error hints" framework.
- **May–Nowakowski 2023** (eprint 2023/777): faster single-stroke
  integrator; fallback for strong-bracket spec if DDGR successive
  integration is slow.
- **2025 error-hints refinement** (eprint 2025/1128).
- **`github.com/lducas/leaky-LWE-Estimator`** — the tool.
- **`tools/op_2_58_2d_provenance_correction.md`** (Brief 11 Item 1) — the
  branch-resident-mirror pattern used here.
- **`tools/op_2_58_2d_dfr_reference.md`** (Brief 10.7 Item 1) — same
  pattern, mirror of §2.66.1.
- **§2.58.B.1** (V4.11) — 42-kernel partition; pair-recovery is a lower
  bound on kernel-recovery, applies transitively to the R3 proxy here.

---

*R3 proxy stand-up: environment + validation protocol + recon + harness on-branch. Frozen pre-reg untouched. Binding single-number bikz is Phase 2 (session-side, awaits weak-bracket run + 21^k guess-cost derivation).*
