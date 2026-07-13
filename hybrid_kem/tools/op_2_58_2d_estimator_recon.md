# op_2_58_2d_estimator_recon.md — hint-structure reconnaissance (Brief LEAKY-LWE Item 2)

**Status**: READ, not assumed. Every claim below cites a file/function/line
in the ratified construction. The §3.2(c) global-vs-per-block fork is
resolved: **PER-BLOCK, no halt** — code-determinable from a single loop
structure.

**Anchor commit**: head of the Brief 11 chain (which itself sits on top of
Brief 10.6's ratification of basis (b) → reading (I) F_L-restriction + σ=2
pin from Brief 10.7 §2.69.3).

**Location note**: the OP-2.58.2d source lives at `tools/` on this branch
(not `hybrid_kem/tools/` as the brief §3.1 lists). The recon memo cites
the actual paths; the harness (Item 3) reads from those same paths.

---

## §1. Question (a) — Base scalar-LWE parameters

The estimator consumes: `n` (LWE dim), `q` (modulus), `m` (samples),
secret distribution, error distribution.

| parameter | spec (k=32) | toy k=7 | toy k=14 | provenance |
|-----------|-------------|---------|----------|------------|
| `n` (LWE dim) = `n_eff` = k·16 | 512 | 112 | 224 | `tools/op_2_58_2d_lattice_attack.py:128` (`n_eff = k * DIM`) + docstring `n_eff` field spec (`build_scalar_lwe` return, line 120) |
| `q` (modulus) | 4,294,977,961 | 911 | 911 | Frozen pre-reg §3.1 (spec); `tools/op_2_58_2d_lattice_attack.py:48` (`TOY_Q = 911`); driver-pin assertion `tools/op_2_58_2d_bkz_driver.py:104-121` (`assert_spec_q`) |
| `m` (samples) | 512 | 112 | 224 | One LWE instance per construction; `b_scalar` has length `n_eff` per `tools/op_2_58_2d_lattice_attack.py:122` — this is the sample count in the estimator's sense (each `b_scalar[r]` is one sample) |
| secret weight `h_s` | 64 | 14 | 28 | Frozen pre-reg §3.1 (h_s=64 spec); `tools/op_2_58_2d_lattice_attack.py:291` (`h_s = round(64 * k / 32)` for toy) |
| secret distribution | sparse ternary | sparse ternary | sparse ternary | `tools/op_2_58_2d_lattice_attack.py:303-306`: `s_scalar[pos] = rng.choice((-1, 1))` at exactly `h_s` positions, elsewhere 0 |
| error width σ | 2 | 2 | 2 | Brief 10.7 / §2.69.3 (`tools/op_2_58_2d_sigma_resolution.md` §4); `tools/op_2_58_2d_primary_run.py:_run_one` `job.get("sigma", 2)` |
| error dist per-coord | {−σ, 0, +σ} exactly | same | same | Brief 10.7 §3.1 (empirical: kernel basis vectors have disjoint support per coord ⇒ no superposition; every nonzero `e_d` is exactly ±σ). See `tools/op_2_58_2d_sigma_calibration.py:_bases`/`confined_block` for the sampler and `tools/op_2_58_2d_sigma_resolution.md` §3.1 for the finding |
| per-coord error variance | 1.33 | 1.33 | 1.33 | Brief 10.7 §2.69.3 measurement (empirical); `tools/op_2_58_2d_sigma_calibration.py` `reconcile()` returns `conf_percoord_var` = 1.332 at N=50,000 |

**DBDD-consumable variance model**: the estimator typically wants
`sigma² = Var(e_d)` per-coordinate. For §2.58.B confined noise at σ=2, the
empirical per-coord variance is **1.33** (not 4 = σ²; the confinement to
K_{a,b} drops it below the "spend all σ² on each coord" default). Use
1.33 as the DBDD instance's error-variance-per-coord; document the
confined distribution's non-Gaussian shape (e_d ∈ {−2, 0, +2} with 33.5%
nonzero rate) as a modeling caveat separate from the point estimate.

---

## §2. Question (b) — Hint subspace and its perfect-hint vectors

The estimator integrates perfect hints as `⟨(s; e), v⟩ = l` where `v` has
support on the error block. Two candidate subspaces the attacker could
have hints on:

### §2.1 F_L union per block (rank 14 / block)

Per D1 (`tools/op_2_58_2d_D1_fano_union_dimension.py`), the F_L union has
F_q-rank **exactly 14** at both q=911 and q=SPEC_Q (verified in that
module's `compute()` at line 103–137). Per block of 16 sedenion
coordinates:

- **Confined subspace**: 14 dims (the F_L union).
- **Complement (perfect-hint dimensionality)**: **16 − 14 = 2 vectors per block**.
- **Hint total**: 2·k perfect hints.

Since e_i ∈ K_{a_i, b_i} ⊂ F_L (Brief 10.7 §3.1 confirms every K_{a,b} is
inside the F_L union), every complement vector `v` with `v ⊥ F_L` per
block gives `⟨e, v⟩ = 0` exactly. This holds **without knowing (a_i, b_i)**
— the union is fixed by the geometry, not by the trapdoor.

Complement basis: `null(F_union_basis)` per block where `F_union_basis` is
the rank-14 matrix from `tools/op_2_58_2d_lattice_attack.py:_fano_union_basis`
(the same 14-vector basis used by the ratified `build_fano_projected_lattice`).

### §2.2 Per-pair K_{a,b} (rank 4 / block)

Per §2.58.B.1 / brief 10.6 §2.4, K_{a,b} is the 4D kernel of L_{z_i} where
z_i = e_a + e_{b+8}. Per block:

- **Confined subspace**: 4 dims (K_{a,b}).
- **Complement**: **16 − 4 = 12 vectors per block**.
- **Hint total**: 12·k perfect hints.

Since e_i ∈ K_{a_i, b_i} exactly, every `v ⊥ K_{a_i, b_i}` per block
gives `⟨e, v⟩ = 0`. But this **requires knowing (a_i, b_i) per block** to
construct the correct 12-vector complement basis.

Complement basis: `null(kernel_basis(a_i, b_i))` per block where
`kernel_basis` is the same `rref_kernel(lmm(z_i, q), q)` machinery in
`tools/op_2252_v2_kernel_involution.py`.

### §2.3 Hint-count summary

| bracket | hints/block | spec k=32 | toy k=7 | toy k=14 |
|---------|-------------|-----------|---------|----------|
| **Weak** (F_L union complement) | 2 | **64** | 14 | 28 |
| **Strong** (per-pair K_{a,b} complement) | 12 | **384** | 84 | 168 |

Numbers match Brief §4.2. Weak-bracket hints are **attacker-free** (no
guessing); strong-bracket hints are **conditional** on the per-block pair
guess (see §3 below).

---

## §3. Question (c) — LOAD-BEARING FORK: pair is PER-BLOCK

**RESOLVED, code-determinable, no halt.**

The `gen_zd_noise_sample` function in `tools/op_2_58_2d_construction.py`
iterates `for i in range(k):` (line 121) and inside that loop, at
**line 130**:

```python
for i in range(k):
    ...
    # Step 2: ZD trapdoor — canonical cross-edge pair (a<b), z = e_a+e_{b+8}.
    a, b = pairs[int(rng.integers(len(pairs)))]
    zv = add_vec(basis_vec(a), basis_vec(b + 8), p)
    z.append(zv)
    pair.append((a, b))
    ...
```

Every iteration of the loop samples a **new** `(a, b)` independently and
uniformly from the 21 cross-edge pairs. The `pair` variable is a
`list[tuple[int, int]]` of length k (declared at
`tools/op_2_58_2d_construction.py:116`), storing the per-block trapdoor
sequence.

**Consequences for the estimator model** (per brief §3.2c):

- **Joint pair guess space** = **21^k** distinct pair-tuples.
  | k | 21^k | feasibility |
  |---|------|-------------|
  | 7 (toy)  | ≈ 1.80 × 10⁹  | feasible with GPU/parallel enumeration |
  | 14 (toy) | ≈ 3.25 × 10¹⁸ | infeasible on a workstation |
  | 32 (spec)| ≈ **4.4 × 10⁴²** | **infeasible on any known compute** |

- **Weak bracket** (F_L union complement, 2·k hints): attacker gets these
  hints for free — the union basis is fixed by the geometry, not by the
  trapdoor. DDGR-integrable directly.
- **Strong bracket** (per-pair complement, 12·k hints): attacker needs to
  guess all k pairs. Effective work factor = (estimator's strong-bracket
  bikz cost) × 21^k. At spec, 21^32 dominates any bikz reduction the hints
  could produce — the strong-bracket hints are lattice-informative but
  become computationally moot if the guess cost isn't refunded by
  meet-in-the-middle or similar (that is the session-side derivation Phase
  2 must supply, per brief §6 "The 21^32 guess-space cost — Session's
  job").

**No `halt-and-surface` fired**: the code is unambiguous.

---

## §4. Question (d) — Does every block carry ZD-noise?

**Yes, all k blocks.**

Provenance: `tools/op_2_58_2d_construction.py:121-147` — the
`for i in range(k):` loop has no conditional; every iteration writes into
`s.append(sv)`, `z.append(zv)`, `pair.append((a, b))`, `e.append(ev)`. The
loop body is monolithic (no `if skip_this_block:` or per-index gating).
Empirically Brief 10.7 §3.1 measured 5600 coord samples per σ across 50
seeds × k=7 × DIM=16 = 5600 — matches 100 % coverage across all blocks.

**Hint count scales with k**, not with an "occupied block count." Same
scaling for weak and strong brackets.

---

## §5. Question (e) — Ratified basis-(b) reading + estimator correspondence

Per `tools/op_2_58_2d_basis_b_ratification.md` (Brief 10.6 Item 1),
§3.6(b) was ratified to **reading (I) F_L-restriction** — the primal
basis with the e-side `q·I_n` rows replaced by `q · (F_L union basis)`
per block, dropping the F_L⊥ direction. Reading (II) augmentation was
**empirically inverted** (degenerate 0/294 pooled recovery at the §3.3.1
N=2.0 cutoff); reading (III) quotient rejected on prose grounds.

### §5.1 DBDD correspondence — the ratified reading = weak bracket

Reading (I) restricts the lattice to F_L-per-block. Under DDGR
"error-hints" (eprint 2020/292 §5), restricting to a subspace of
dimension `d` is *equivalent* to `(ambient − d)` perfect hints on the
orthogonal complement. The correspondence:

- (I) F_L-restriction: 14 dims/block confined ↔ 2 hints/block on the
  complement. **This IS the weak bracket.**
- (II) augmentation (rejected): would have added `unscaled` F_L basis
  vectors to the lattice; toy-invalidated by Brief 10.6 §4.
- (III) quotient (rejected): different problem — projecting *out* of
  F_L would model an attacker who removes the confined subspace before
  BKZ, changing the target.

The harness (Item 3) models both:
- **Weak bracket** = 2 hints/block = the ratified reading (I). This is
  the DBDD prediction *the primary run's basis (b) actually attacks*.
- **Strong bracket** = 12 hints/block = an oracle-attacker-with-per-block-pair
  scenario. Illustrative upper-bound on hint density; requires 21^k
  guessing per §3.

---

## §6. Assumptions vs. findings

- **No assumptions substituted for code.** Every table row in §1–§5 cites
  the file/function/line it came from.
- **No fork halted.** §3.2(c) resolved on a single-line loop-inside-`for i in range(k)`.
- **What is *not* determinable from the on-branch code**:
  - The DBDD-optimal `n × m` shape choice — the estimator has some slack
    in how it embeds the LWE (primal / dual / uSVP-embedding). This is a
    harness authoring detail, not a construction property.
  - The per-block pair enumeration cost model beyond 21^k naive — a
    meet-in-the-middle or Fano-line-structural refinement could reduce
    it. This is Phase 2's job (brief §6 "The 21^32 guess-space cost").

---

## §7. Cross-references

- **`tools/op_2_58_2d_construction.py`** — `gen_zd_noise_sample`
  (per-block pair loop), `gen_spec_instance` (composition + spec gate).
- **`tools/op_2_58_2d_lattice_attack.py`** — `build_scalar_lwe` (LWE
  parameters), `_fano_union_basis` (rank-14 F_L union basis),
  `build_fano_projected_lattice` (ratified (I) F_L-restriction),
  `gen_toy_instance` (h_s = round(64·k/32)).
- **`tools/op_2_58_2d_D1_fano_union_dimension.py`** — the rank-14 fact
  used by §2.1.
- **`tools/op_2252_v2_kernel_involution.py`** — `rref_kernel`, `lmm`
  (kernel basis machinery).
- **`tools/op_2_58_2d_basis_b_ratification.md`** — Brief 10.6 ratification
  of reading (I) with the toy-scale (I) vs (II) comparison.
- **`tools/op_2_58_2d_sigma_resolution.md`** + Brief 10.7 §2.69.3 — σ=2
  pin, per-coord variance 1.33.
- **DDGR 2020** (eprint 2020/292) — the perfect-hints-on-error framework
  the estimator implements; §5 "error hints" is the exact model here.
- **Frozen pre-reg §3.1, §3.6** — parameters and basis definitions.
