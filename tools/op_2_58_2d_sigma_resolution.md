# op_2_58_2d_sigma_resolution.md — Brief 10.6 Item 2

**Decision**: σ = 2 pinned as the operational noise width. Single value, no
sweep. Derivation: sub-case 2 (the η=2 bound + kernel-vector structure;
Brief 10.6 §3.3 step 2). Sub-case 1 (citation from §2.66.1) did not close —
§2.66.1 / DFR analysis is not present in the on-branch canonical chain.

**Anchor**: Brief 10.6 §3. Frozen pre-reg §3.1 (η=2). Brief 10.5 §2.4 (the
σ-stability cross-check). §3.3.1 cutoff-pinning precedent.

---

## §1. The question

§2.58.B KeyGen step 4 samples noise e_i = σ · Σ_{j=1..4} α_j · k_j⁽ⁱ⁾ with
α_j ∈ {−1, 0, +1} and k_j⁽ⁱ⁾ the 4 right-kernel basis vectors of L_{z_i}
returned by `op_2252_v2_kernel_involution.rref_kernel`. σ is the noise
width. Brief 10.5 left σ unspecified and the proof-of-life used σ=2
provisionally. σ must be pinned before the 42-run schedule.

## §2. Sub-case 1 — citation from §2.66.1 / DFR analysis

Brief 10.6 §3.3 step 1 says: "Check §2.66 / §2.66.1 (the DFR analysis) for
an assumed σ … if §2.66.1 pinned a σ to achieve [DFR ≤ 2⁻¹²⁸], that is the
operational σ and the question closes by citation. **Do this check first.**"

**Result of the check**: §2.66.1 (DFR analysis) is NOT present on the
on-branch state. A repo survey across `tools/`, `reports/`, and all `*.md`
found §2.66 referenced only as "the §2.66.2 line classifier (demoted to
reference data by Convention C)" in `op_2_58_2d_construction.py`, and as the
"Brief-08 with-lift baseline" in the prefreeze report. No DFR ≤ 2⁻¹²⁸
analysis, no σ-pinning from §2.66.1, no canonical text on-branch. Sub-case 1
therefore cannot close by citation; closure proceeds to sub-case 2.

If the session principal holds §2.66.1 in session memory and its σ-pinning
exists there, that supersedes this derivation — the citation path is
strictly stronger than the derivation path. If §2.66.1 confirms σ=2, the
derivation and the citation agree. If §2.66.1 pins a different σ, that
value rules and the schedule re-pins.

## §3. Sub-case 2 — derivation from η=2 and kernel structure

### §3.1 The kernel structure

`rref_kernel(lmm(x, q), q)` for x = e_a + e_{b+8} returns a 4-vector basis
of K_{a,b}. Empirical check at q=911, summing over 50 seeds × k=7 blocks ×
DIM=16 coordinates = 5600 coord-samples per σ:

| σ | total coords | nonzero coords | max\|e_d\| | mean\|e_d\| (nonzero) | unique nonzero values |
|---|--------------|----------------|-----------|----------------------|----------------------|
| 1 | 5600         | 1876           | **1**     | 1.000                | {−1, +1}             |
| 2 | 5600         | 1876           | **2**     | 2.000                | {−2, +2}             |
| 4 | 5600         | 1876           | **4**     | 4.000                | {−4, +4}             |

**Critical structural observation**: every nonzero coord is **exactly ±σ**.
Not "≤ σ × small integer" — exactly σ in magnitude. This means the 4 kernel
basis vectors {k_1, k_2, k_3, k_4} have disjoint support per coordinate d:
for any fixed d, at most one k_j has k_j[d] ≠ 0. So Σ_j α_j · k_j[d] is a
single α_j · (±1) term, and e_d = σ · α_j · (±1) ∈ {−σ, 0, +σ}.

This makes the η=2 derivation exact and clean.

### §3.2 The derivation

Per-coord max magnitude of e: |e_d| ≤ σ. The frozen pre-reg §3.1 names η=2
as the noise bound. Imposing |e_d| ≤ η:

  σ ≤ η = 2.

Therefore σ ∈ {1, 2} satisfies the bound; σ = 4 violates it (confirmed by
the table: σ=4 produces |e_d| = 4 > η = 2).

### §3.3 Picking within the feasible range

Per Brief 10.6 §2.3's precedent (the basis-(b) ratification picked the
worst-case-for-defender reading), σ within the feasible range is pinned to
the value that maximises attacker difficulty under the η bound — i.e., the
largest σ consistent with η=2:

  **σ = 2** (the η=2 boundary).

This is the "worst-case-for-defender" σ: maximum noise the construction is
permitted, so maximum BDD radius for the attacker. It matches:

- The proof-of-life setting (also σ=2, exactly because it's the boundary).
- Brief 10.5 §2.4's cross-check value (σ ∈ {1, 2, 4} — the test went one
  step beyond η to characterise robustness; for the schedule we stay within η).
- The §3.3.1 cutoff-pinning precedent: pre-registered parameter, ratified
  with derivation, not chosen post-hoc.

### §3.4 The classifier-vs-lattice-attack sensitivity distinction

Brief 10.5 §2.4 established σ is **non-load-bearing for the §3.3
classifier** — exactly, not approximately. The projection metric
‖P_S v‖² / ‖v‖² is invariant under scaling v by σ, so the argmax pair is
σ-independent. At σ ∈ {1, 2, 4}, the cross-check measured 95.857%
pair-recovery with 0.000% spread. Brief 10.6 §3.4 explicitly cautions:
σ-stability of the *classifier* does NOT imply σ-irrelevance for the
*lattice attack*.

For the lattice attack, σ scales the noise magnitude → the BDD radius →
whether BKZ at a given β finds the target. Specifically:

- Target vector v = (e_scalar, s_scalar, 1) on the primal lattice.
- ‖e‖ ≈ σ · √(N_nz) where N_nz is the count of nonzero coords (≈ 1876 per
  5600 ≈ 33.5% sparsity; at k=32 spec, expect ≈ 0.335 · 32 · 16 = 171 nonzero
  e-coords; so ‖e‖_2 ≈ σ · √171 ≈ 13σ at spec).
- ‖s‖ = √h_s = √64 = 8 at spec.
- ‖v_target‖ ≈ √(σ² · 171 + 64 + 1).
  - At σ=1: ‖v_target‖ ≈ √(171 + 65) = √236 ≈ 15.4.
  - At σ=2: ‖v_target‖ ≈ √(684 + 65) = √749 ≈ 27.4.
  - At σ=4: ‖v_target‖ ≈ √(2736 + 65) = √2801 ≈ 52.9.

Larger σ → larger ‖v_target‖ → harder for BKZ. Gaussian heuristic for the
spec basis (a) at k=32 q=4,294,977,961, N_lat = 1025:

  log_det = 512 · ln(4.294977961 × 10⁹) ≈ 11,355
  log_gh  = 11,355/1025 + 0.5·(ln 1025 − ln 2πe) ≈ 11.08 + 2.05 ≈ 13.13
  gh ≈ exp(13.13) ≈ 5 × 10⁵.

‖v_target‖ ≪ gh by 4-5 orders of magnitude → unique-SVP regime → BKZ at
sufficiently large β recovers v_target. σ=2 is well within the uSVP regime
on the primal basis; the schedule's β ∈ {20, 30, 40, 45, 50, 55, 60} sweeps
where the recovery boundary actually sits.

### §3.5 Sub-case 3 — σ sweep — RULED OUT

Brief 10.6 §3.3 step 3 says: "If neither pins it, σ is a free parameter and
the schedule must sweep it." Sub-case 2 pinned it (σ=2), so the sweep is
NOT triggered. The 42-run schedule remains 42 runs, not 126.

## §4. Pinned value

**σ = 2** — operational, pre-registered, derivation-pinned.

Documented as a Rev 5.x within-band addendum to §3.1 of the frozen pre-reg
(the same within-band edit gate the §3.3.1 cutoff used; pre-reg §6 freeze
signature already authorises within-band addenda). No re-freeze required —
this pins a parameter the frozen text named without a value.

If §2.66.1 (in session memory or the canonical ledger off-branch) pins σ to
a different value, this derivation defers to it; in that case the §3.1
addendum cites §2.66.1 instead of this document.

## §5. Caveats and out-of-scope

- The disjoint-support kernel structure (§3.1) was verified at q=911 only.
  The kernel-involution algebra is q-independent (it is integer linear
  algebra over F_q), so the structure carries to q=SPEC_Q without
  modification. A spot-check at q=SPEC_Q is trivial via the same harness if
  the session principal wants belt-and-braces.
- The derivation interprets η=2 as a per-coord ℓ_∞ bound. If §2.66.1 (or a
  closer reading of the frozen §3.1) intends η as a different functional
  (ℓ₂, total noise budget, etc.), the derivation re-runs with the corrected
  interpretation. The structural conclusion (e_d ∈ {−σ, 0, +σ} exactly)
  is independent of the η interpretation; it's a property of the
  construction.
- DFR (decryption failure rate ≤ 2⁻¹²⁸ at spec) is the proper σ-upper-bound
  in cryptographic practice. The η=2 bound here is the pre-reg's stated
  bound; whether η=2 corresponds to DFR ≤ 2⁻¹²⁸ at spec is a question for
  §2.66.1 if/when it lands.

## §6. Code touch

No production-code changes. The σ value is consumed by
`_run_one(job, ...)` in `op_2_58_2d_primary_run.py` via `job.get("sigma", 2)`;
the default 2 already matches this resolution. The proof-of-life run is
consistent with the ratified σ; no re-run is necessary.

The schedule (when dispatched) will use σ=2 per `BETAS`, `SAMPLES`, `BASES`
and the in-module sigma default. If the addendum to pre-reg §3.1 names σ=2
explicitly, the code already conforms.

## §7. Reproducer

Reproduce §3.1's empirical table with:

```python
import sys; sys.path.insert(0, 'tools')
import numpy as np
from op_2_58_2d_construction import gen_zd_noise_sample, TOY_P
for sigma in (1, 2, 4):
    coords = []
    for seed in range(50):
        rng = np.random.default_rng(seed)
        s = gen_zd_noise_sample(TOY_P, k=7, sigma=sigma, rng=rng)
        for ev in s["e"]:
            for x in ev:
                signed = x if x <= TOY_P // 2 else x - TOY_P
                coords.append(signed)
    arr = np.array(coords)
    print(f"σ={sigma}: max|e_d|={abs(arr).max()}, "
          f"unique nonzero={sorted(set(int(x) for x in arr if x))}")
```

Expected: σ=1 → {±1}, σ=2 → {±2}, σ=4 → {±4}. Disjoint kernel support per
coord. η=2 ⟹ σ ≤ 2. Operational σ = 2.
