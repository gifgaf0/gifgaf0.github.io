"""op_2_58_2d_construction.py — §2.58.B Module-SLWE construction (Brief 10.5).

Implements §2.58.B KeyGen from canonical prose (V4.9 §2.58.B). Closes the L2
finding (§2.69.2) surfaced by the Brief-10 halt: the construction was not
present as executable code in the repo.

Toy-scale work; the spec-parameter gate (k=32, q=4_294_977_961) is enforced by
gen_spec_instance and shared with op_2_58_2d_lattice_attack. Nothing here runs
against §2.58.B at spec parameters.

SPECIFICATION GAPS (handled per Brief 10.5 discipline):
  * §2.3 public-matrix structure. "A ← 𝕊_p^{k×k} with PSL(2,7)/Singer orbit
    structure" is ambiguous (uniform / PSL(2,7)-equivariant / Singer-cycle).
    Only "uniform" (the conservative reading) is implemented; the other two
    halt with NotImplementedError citing §2.3 and §2.69.2, pending session
    resolution and a follow-on Brief 10.6.
  * §2.4 noise width σ. Unspecified at toy scale; `sigma` is a required
    parameter with no default. The cross-check utility characterises σ-stability.

TRAPDOOR SAMPLING NOTE: the trapdoor z_i is sampled over the 21 canonical
Convention-C cross-edge pairs (a<b in 1..7, z = e_a + e_{b+8}). These are the
subset of the 84 two-term ZDs over which Convention C's (a,b) pair label and the
§3.3 classifier's K_{a,b} subspaces are defined; each is a member of the 84-ZD
set. This is forced by the (a,b)-pair label convention, not an independent
structural choice.
"""

from __future__ import annotations

import os
import sys
from itertools import combinations
from typing import Literal

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sedenion_Fp import DIM, add_vec, basis_vec, mul_vec  # noqa: E402
from op_2252_v2_kernel_involution import (  # noqa: E402
    enumerate_two_term_ZDs,
    lmm,
    rref_kernel,
)
from op_2_58_2d_lattice_attack import _check_not_spec  # noqa: E402

TOY_P = 911


def _zd_vec_set(p: int) -> set[tuple[int, ...]]:
    return {tuple(d["vec"]) for d in enumerate_two_term_ZDs(p)}


def _fano_line_of_pair(a: int, b: int, p: int) -> frozenset[int]:
    """Line {a,b,c} with c read from e_a·e_b = ±e_c (single-term product)."""
    prod = mul_vec(basis_vec(a), basis_vec(b), p)
    nz = [i for i, v in enumerate(prod) if v % p != 0]
    assert len(nz) == 1, f"e_{a}·e_{b} not single-term: {nz}"
    return frozenset({a, b, nz[0]})


def gen_zd_noise_sample(
    p: int,
    k: int,
    sigma: int,
    rng: np.random.Generator,
    *,
    trapdoor_cardinality: Literal["fano_line_7", "pair_21", "kernel_42"] = "pair_21",
) -> dict:
    """Generate a §2.58.B (s, z, e) ZD-noise sample with trapdoor recorded.

    Steps 1, 2, 4 of §2.58.B KeyGen. See module docstring for the trapdoor
    sampling convention. Returns s/z/ell/pair/e plus alphas/kernels record-keeping.

    `trapdoor_cardinality` pins which trapdoor object is RECORDED as the label,
    per OP-2.58.B.card and §2.58.B.1 (the A1 42-kernel finding). The three
    geometrically distinct objects:

      - "fano_line_7":  the Fano line ell(z_i) in {1..7}   (cardinality 7)
      - "pair_21":      the unordered interior pair {a,b}   (cardinality 21)
      - "kernel_42":    the noise subspace ker(L_z)         (cardinality 42)

    The 84 two-term ZDs partition into 42 distinct ker(L_z), with 2 ZDs per
    kernel exchanged by the CD doubling involution e_i<->e_{i+8} (verified at
    p=911 and p=spec). 84 is therefore a 2-to-1 redundant labeling of 42, not a
    fourth object. Only "pair_21" is implemented; it is the §3.3 Convention-C
    target and recovers the pair label, a LOWER BOUND on kernel recovery (kernel
    => pair, not conversely). "kernel_42" needs a 42-class chirality-resolving
    classifier; "fano_line_7" needs the §2.66.2 line classifier (demoted to
    reference data by Convention C). Which object is the operative trapdoor is
    the open structural problem OP-2.58.B.card.

    The pair_21 default samples uniformly over the 21 canonical Convention-C
    cross-edge pairs (a<b, z=e_a+e_{b+8}); each such z is one of two ZDs sharing
    its kernel, so the sampler picks one specific kernel per pair (a
    chirality-discarding projection onto 21 of the 42 kernels).
    """
    if trapdoor_cardinality != "pair_21":
        raise NotImplementedError(
            f"OP-2.58.B.card: trapdoor_cardinality={trapdoor_cardinality!r} is "
            "not implemented. Per §2.58.B.1, the noise subspace ker(L_z) is one "
            "of 42 distinct kernels (2 per unordered pair, exchanged by the CD "
            "doubling involution e_i<->e_{i+8}). 'pair_21' (the §3.3 "
            "Convention-C target) is implemented and recovers the pair label, a "
            "LOWER BOUND on kernel recovery. 'kernel_42' needs a 42-class "
            "chirality-resolving classifier; 'fano_line_7' needs the §2.66.2 "
            "line classifier. Which object is the operative trapdoor is the "
            "open structural problem OP-2.58.B.card. See §2.58.B.1 in the "
            "canonical ledger."
        )
    zd_set = _zd_vec_set(p)
    pairs = list(combinations(range(1, 8), 2))

    s: list[list[int]] = []
    z: list[list[int]] = []
    ell: list[frozenset[int]] = []
    pair: list[tuple[int, int]] = []
    e: list[list[int]] = []
    alphas = np.zeros((k, 4), dtype=int)
    kernels = np.zeros((k, 4, DIM), dtype=int)

    for i in range(k):
        # Step 1: non-ZD secret coordinate (reject the 84 two-term ZDs).
        while True:
            sv = [int(rng.integers(p)) for _ in range(DIM)]
            if tuple(sv) not in zd_set:
                break
        s.append(sv)

        # Step 2: ZD trapdoor — canonical cross-edge pair (a<b), z = e_a+e_{b+8}.
        a, b = pairs[int(rng.integers(len(pairs)))]
        zv = add_vec(basis_vec(a), basis_vec(b + 8), p)
        z.append(zv)
        pair.append((a, b))
        ell.append(_fano_line_of_pair(a, b, p))

        # Step 4: kernel basis of L_{z_i}, then e_i = σ·Σ α_j k_j.
        kb = rref_kernel(lmm(zv, p), p)
        assert len(kb) == 4, f"kernel of L_z for pair {(a, b)} not 4D: {len(kb)}"
        al = rng.integers(-1, 2, size=4)
        ev = [0] * DIM
        for j, (aj, kv) in enumerate(zip(al, kb)):
            kernels[i, j] = [c % p for c in kv]
            for d in range(DIM):
                ev[d] = (ev[d] + sigma * int(aj) * kv[d]) % p
        alphas[i] = al
        e.append(ev)

    return {
        "s": s, "z": z, "ell": ell, "pair": pair, "e": e,
        "alphas": alphas, "kernels": kernels,
        "p": p, "k": k, "sigma": sigma,
    }


def gen_public_matrix(
    p: int,
    k: int,
    rng: np.random.Generator,
    structure: Literal["uniform", "psl27_equivariant", "singer_cycle"],
) -> np.ndarray:
    """Sample public matrix A per §2.58.B step 3 (shape (k, k, DIM) over F_p).

    Only "uniform" (the §2.3 reading (a)) is implemented. The PSL(2,7)-equivariant
    and Singer-cycle readings are deliberately not implemented in Brief 10.5; they
    require session resolution of the §2.3 specification gap and a follow-on
    Brief 10.6. The NotImplementedError message cites §2.3 and §2.69.2 at runtime.
    """
    if structure == "uniform":
        return rng.integers(p, size=(k, k, DIM), dtype=np.int64)
    if structure in ("psl27_equivariant", "singer_cycle"):
        raise NotImplementedError(
            f"public-matrix structure {structure!r} is not implemented: the "
            "§2.58.B phrase 'PSL(2,7)/Singer orbit structure' is a specification "
            "gap (Brief 10.5 §2.3). This reading changes the attack surface and "
            "is a session-level structural decision (ledger §2.69.2), requiring a "
            "follow-on Brief 10.6. Only 'uniform' is implemented here."
        )
    raise ValueError(f"unknown structure {structure!r}")


def gen_spec_instance(
    p: int,
    k: int,
    sigma: int,
    rng: np.random.Generator,
    matrix_structure: Literal["uniform", "psl27_equivariant", "singer_cycle"] = "uniform",
    allow_spec_params: bool = False,
    *,
    trapdoor_cardinality: Literal["fano_line_7", "pair_21", "kernel_42"] = "pair_21",
) -> dict:
    """Generate a complete §2.58.B (A, s, z, ell, pair, e, b) instance.

    Composes gen_public_matrix + gen_zd_noise_sample, then b = A·s + e over 𝕊_p.
    Enforces the shared spec-parameter gate (SpecParamsRefused on spec scale).
    `trapdoor_cardinality` is propagated to gen_zd_noise_sample (see its
    docstring for OP-2.58.B.card / §2.58.B.1 framing).
    """
    _check_not_spec(p, k, allow_spec_params)
    A = gen_public_matrix(p, k, rng, matrix_structure)
    sample = gen_zd_noise_sample(p, k, sigma, rng,
                                 trapdoor_cardinality=trapdoor_cardinality)
    s, e = sample["s"], sample["e"]
    b: list[list[int]] = []
    for i in range(k):
        acc = [0] * DIM
        for j in range(k):
            acc = add_vec(acc, mul_vec([int(x) for x in A[i, j]], s[j], p), p)
        b.append(add_vec(acc, e[i], p))
    return {"A": A, "b": b, **sample}


if __name__ == "__main__":
    rng = np.random.default_rng(20260601)
    inst = gen_spec_instance(TOY_P, k=7, sigma=2, rng=rng)
    print(f"§2.58.B toy instance: p={TOY_P} k={inst['k']} sigma={inst['sigma']}")
    print(f"  pairs (trapdoor): {inst['pair']}")
    print(f"  lines: {[sorted(L) for L in inst['ell']]}")
    ok = all(all(x % TOY_P == 0 for x in mul_vec(inst['z'][i], inst['e'][i], TOY_P))
             for i in range(inst['k']))
    print(f"  kernel containment L_z·e = 0 (all coords): {ok}")
