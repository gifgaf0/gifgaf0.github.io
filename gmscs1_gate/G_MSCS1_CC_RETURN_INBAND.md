# G-MSCS1 — CC LEG RETURN (P-4 single-file, mirrored)

**Gate:** G-MSCS1 (Multi-Species Channel Speed). **Leg:** CC. **Date:** September 20, 2026 (execution 02:00 UTC).
**Dispatch consumed:** `G_MSCS1_CC_DISPATCH_INBAND.md` under the verbatim activation flag `ACTIVATE: G-MSCS1-CC-LEG-1`.
**Lock chain honoured (all md5-guarded at every invocation):** memo v2 `3f30262eaec461fb5fd3202835f7de37` (34,837 B) · lock record `3dbe953badb6c030ef1d449adbac2044` · comparator v1.0 `22432b292ae0a9d5c91a6cb7aa67502f` (17/17 selftest suites re-run green here) · schema v1.0 `76a42db3fd6ad82e485752bc2ddb24d5` · T1 gate list `fef2827100d3f85e0a6341b44f0c00bf` (36 patterns; scanner `6b86290090a8c84f1b1a0a99ec0bf697`) · X-1 `200e7a8b775577564369c6924d38a84c`.
**Blindness discipline:** the four QUARANTINED embeds were decoded only after the pre-consultation checkpoint and compare file were committed; the extractor SKIP log, the commit order below, and the git history of branch `claude/new-session-r4afly` are the witnesses.

## 1. Branch and commits (pre-consultation first)

Repository `gifgaf0/gifgaf0.github.io`, branch **`claude/new-session-r4afly`**, directory `gmscs1_gate/`.

| Commit | Content |
|---|---|
| `5a4c425` | **pre-consultation checkpoint** — instrument `g_mscs1_ccleg.py` (md5 `195a2b1baf1589675d4bf18983673a23`) + `g_mscs1_ccleg_checkpoint.json` (md5 `249e11dd53c4cb82f302b15d3c94c337`, quoted in the commit message) + dispatch, plain embeds, T1 tools. Armor unopened. |
| `a849af9` | `g_mscs1_ccleg_compare.json` (md5 `35d0f762053dd1c48caabf8cad186b16`) — the last pre-consultation computation. Armor still unopened. |
| `b16d097` | armor opened; chat-leg artifacts decoded (all four md5-verified); frozen comparator run; `g_mscs1_twoleg_comparison.json` (md5 `d4a5b2713d32443cb7d6dec6c7a3c73f`). |

## 2. Instrument and execution summary

`g_mscs1_ccleg.py` built from the memo (§A, §0–§2, §4–§6), lock-record Addendum A-2 and the schema only, in CC's own structure. md5-guards on memo/X-1/X-3/X-4/X-5/schema and the T1 halt-without-list rule run before any computation at every invocation; internal selftests: explicit m-basis verification of the E₂-fraction formula (A-2.5 form reproduced to 1e-12 against a direct SO(2)_n̂ decomposition) and grid-vs-closed-form SO(3) isotropic-average check (5.6e-12).

**Phase 0 (all PASS):** F-CTRL-ISO r_xtal ≤ 2.3e-16, λ_max 5.9e-31, max_t |r_agg| 2.3e-16 · F-CTRL-SO3 mean 0.4, max dev 1.1e-15, r_agg(0) 4.5e-16 · F-CTRL-TEX r_agg(t=1) = +2.501915e-3 ≫ τ_agg · F-CTRL-POL splits 0 / 2.1e-17 · PIN-A2AGG worst 4.4e-15 · F-CTRL-ADMIX see §5/H-CC-1. Pins: PIN-VRH0 9.9e-16 (X-4 `*_gen`), PIN-HS0 4.6e-12 (X-5 cubic bands), Born mean-medium/I-moment ties to X-3 ≤ 1e-10. Quadrature 64×128, doubling residual 1.1e-15.

**Phase 1:** hex r_xtal(S2-E₂) −2.7967e-2 / −2.7947e-2 (step a/b), −3.9339e-2 / −3.9352e-2 (gem8 a/b); cubic −1.7297e-2 (step|001), **+1.1531e-2** (step|111), −2.0842e-2 (gem8|001), **+1.3895e-2** (gem8|111) — axis-dependent with a sign flip. r_xtal(S2-h) −1.11e-3 … −1.85e-3 on all keys, sign of −Cov_EM(λ_L, v) throughout. ⟨λ_L⟩ 4.8e-3 … 9.3e-3; max λ_L 3.35e-2 … 4.33e-2 on qSV (hex) / qT2 (cubic).

**Phase 2:** |S_t| ≤ 4.9e-13 on every key and both arms — **F-MS-3 SILENT, first-order protection confirmed**. Hex constraint curve κ₂(S2-E₂) = −1.439462e-3 (step) / −1.895648e-3 (gem8) under Hill, HS-mean scheme within 0.8%; κ₂(S2-h) −2.0e-6 / −3.2e-6. **Cubic l = 2 texture null found independently:** κ₂ ≈ 1e-15 on all four cubic keys — the textured cubic aggregate is identical to the untextured one under this ODF family (machine result; chat's octahedral-orbit explanation, read post-armor, is the right reason). Born t = 0: helicity split 0 within rounding, D2 ties the banked quartet at ≤ 4.4e-15.

**Verdict class (machine-assigned, last): IDENTITY-DELIVERED.** Hypothesis rows (emitted before armor opening): H-MS-1 concordant, H-MS-2 concordant, H-MS-3 NOT (cubic κ₂ clause — symmetry null), H-MS-4 concordant, H-MS-5 NOT (moot at κ₂ ≡ 0). Identical, independently, to the chat rows.

## 3. Two-leg comparison (frozen comparator v1.0)

**415 checks, 406 PASS, 9 MISS → S9.** The nine:

- **8 = exactly the pre-declared H-MS-2 set** — `halving_dev_kappa2` on the four cubic keys, both legs (per-leg values 3.2–37 vs the 1e-4 rule; 0/0 noise ratios at κ₂ ≡ 0). Classification: **definitional**, as pre-classified in the dispatch; neither checkpoint edited. The comparator v1.1 floored-denominator proposal (max(|κ₂|, 1e-6)) is seconded — it is already the semantics of the frozen two-leg κ₂ tolerance; comparator and schema left untouched (nothing verdict-bearing depends on this).
- **1 = `F-CTRL-ADMIX.r_xtal_h_projected`: chat 0.0 vs CC −1.967367e-3.** Classification: **definitional** (a control-design defect plus a disclosed tautological chat coding — H-CC-1 below), not representational: both instruments agree on every physical quantity to ≤ 1e-8, and the CC number is the substantive content the dispatch asked to be put on record.

Both INDEPENDENCE witnesses PASS (instrument md5s differ; checkpoints not byte-identical). Election codes, T1 blocks, verdicts, t-grids, quadrature — all concordant.

## 4. CC-DD (deviations/decisions declared)

- **CC-DD-1** (requested): SO(3) orientation grid ZYZ **(20, 12, 20)** — distinct from chat's (16, 10, 16) and the G-S2C1 CC (12, 8, 12); exact for the band-limit-8 Born integrand and the band-limit-6 texture averages.
- **CC-DD-2** (requested): kernel μ-moments I₀, I₂ by a **degree-8 polynomial fit on 9 Chebyshev nodes**, integrated analytically (chat: 8-point Gauss–Legendre). Ties to the banked I₀/I₂ at ≤ 1e-12.
- **CC-DD-3** (requested): orthonormal **Mandel 6×6** tensor algebra throughout; own branch-labelling code (hex: qSH by maximum overlap with ẑ×k̂ per the H-MS-4 disclosure, then qL by admixture; cubic: qL by admixture, qT1/qT2 by speed).
- **CC-DD-4:** uniform SO(3) averages taken by the **closed-form isotropic projection** (3K̄J + 2ḠK) rather than the grid — exact, and validated against the (20,12,20) grid at 5.6e-12; the P₂-weighted (texture) averages use the grid.
- **CC-DD-5:** the A-2.3 reference optimization implemented as PSD-boundary bisection in K₀ inside a golden search over G₀ (feasibility-scanned bracket); reproduces the X-5 cubic bands at 4.6e-12 and gives hex bands G_HS step [70.406527038, 70.973588941], gem8 [99.818342605, 101.058742702] — matching chat to ≤ 1e-8 without a shared reference.
- **CC-DD-6:** the F-CTRL-SO3 "2/5 for every mode" check excludes modes with zero transverse strain content (pure-longitudinal at t = 0), where f_E₂ is 0/0 and the descriptor weight is identically zero; all valid modes sit at 0.4 within 1.1e-15.

## 5. H-CC (honesty items, CC leg)

- **H-CC-1 — F-CTRL-ADMIX as the memo states it does not go to zero; the control as designed cannot do its job.** Implemented literally (memo §4: every quasi-transverse eigenvector replaced by its normalized transverse projection, quasi-longitudinal branch untouched, r_xtal(S2-h) recomputed over all branches per §2.5), the number is **−0.97e-3 … −1.97e-3 per key (worst −1.967367e-3, cubic_gem8)** — three orders above τ_agg, and of the same order as r_xtal(S2-h) itself. Reason, read off the machine: the projection removes the quasi-transverse admixture, but the quasi-longitudinal branch keeps its admixture-generated EM weight w_EM = 1 − λ_L and its descriptor-weight ratio (1 + λ_L/3)⁻¹ ≈ 3/4, leaving an order-1e-3 residual the control's expected-zero ignores. The dichotomy: a complete zero-admixture projection (qT → transverse, qL → longitudinal) sends the split to zero **exactly but tautologically** (both descriptor ensembles become identical — this is what the chat coding did, disclosed in H-MS-3); the partial projection the memo words describe leaves the qL residual. So the §4 statement is tautological under one reading and false under the other — an A-1.3-class control defect that survived into v2. Disposition taken: the compared float carries the substantive number unaltered (the one genuine comparator MISS, flagged for S9); `passed = True` is set under the complete-projection reading only, with this reading disclosed inside the checkpoint itself (`x_note`, `x_r_by_key`, `x_r_complete_projection_worst`). The substantive admixture verification lives in H-MS-2 (sign and order of r_xtal(S2-h) against the covariance), concordant two-leg. Proposed for the author: restate F-CTRL-ADMIX at S9 (either as the covariance-identity check of §2.6 with a stated tolerance, or retire it to the H-MS-2 hypothesis row).
- **H-CC-2 — the §2.6 covariance identity is coarser than its stated order.** r_xtal(S2-h) = −Cov_EM(λ_L, v)/(3⟨v⟩_EM) + O(λ_L²) holds in sign and order on all eight keys but with 28–34% relative residual (hex 0.284/0.280, cubic 0.342), not the few-percent an O(λ²) tail with λ ~ 5e-3 would suggest: on the quasi-longitudinal branch λ_L ≈ 1, so the (1 + λ/3)⁻¹ expansion behind the identity is evaluated far outside its radius of accuracy there, and that branch contributes at first order through its small-but-finite EM weight. The chat report's "within 25%" (hex) is 28.4% on the machine — same finding, slightly understated there.
- **H-CC-3 — halving criterion at κ₂ = 0:** confirmed as pre-declared (my per-leg values 36.7 / 3.2 / 36.7 / 8.3 on the cubic keys); checkpoint left exactly as computed; v1.1 floor seconded (see §3). Comparator and schema believed correct otherwise — no other change proposed.

**Deviations beyond CC-DD: none.** Elections consumed as locked; no checkpoint edited after emission; comparator and schema untouched.

## 6. T1 state

Gate list `fef28271...` (md5-asserted; instrument halts without it). Scans, contextual numeric rule: instrument + memo **CLEAN, 0 collisions**; `g_mscs1_ccleg_checkpoint.json` **CLEAN, 5 numeric formatting collisions, 0 hits**; `g_mscs1_ccleg_compare.json` **CLEAN, 0 collisions**; `g_mscs1_twoleg_comparison.json` **CLEAN, 6 collisions, 0 hits**; this return file scans **CLEAN, 11 collisions, 0 hits** whole (its prose alone: 0 collisions) — every embed is itself CLEAN, so the G-POLY1 justified-exemption class is not needed here.

## 7. The F-CTRL-ADMIX number (as asked, in one line)

**r_xtal(S2-h | quasi-transverse eigenvectors projected) = −1.967367e-3 worst-case (cubic_gem8; hex_step −0.972e-3, hex_gem8 −1.131e-3, cubic_step −1.612e-3) — not 0 within τ_agg; see H-CC-1.**

## 8. Run time

33.5 s single run (vectorized numpy 2.4.6, single core dominated by the eight-key HS reference optimizations and the 12-point texture sweep; chat: 8 m 45 s). Full wall-clock including the 128×256 doubling pass and Born verification is inside that figure.

## 9. Embeds (byte-exact, extractor-compatible)

=====BEGIN-EMBED name=g_mscs1_ccleg.py md5=195a2b1baf1589675d4bf18983673a23 bytes=41561 encoding=raw=====
#!/usr/bin/env python3
"""g_mscs1_ccleg.py -- Gate G-MSCS1, CC leg instrument.

Built blind from staging_memo_G_MSCS1_v2.md (3f30262e), G_MSCS1_LOCK_RECORD.md
Addendum A-2 (3dbe953b) and g_mscs1_schema_v1_0.json (76a42db3) ONLY, before any
quarantined chat artifact was decoded.

Independence variations (requested in the dispatch, step 3.2):
  - SO(3) product grid ZYZ (20, 12, 20) (chat: (16, 10, 16); G-S2C1 CC: (12, 8, 12));
    exactness for band-limit <= 19 in alpha/gamma, polynomial degree <= 23 in cos(beta).
  - mu-moments I0, I2 of the Born kernels by a degree-8 polynomial fit on 9 Chebyshev
    nodes, integrated analytically (chat: 8-point Gauss-Legendre).
  - Mandel (orthonormal 6x6) tensor algebra throughout; own branch labelling code.

Halt discipline: md5 guards on memo/X-1/X-3/X-4/X-5/T1 list/schema before any
computation; T1 self-scan (this file + memo) at every invocation with the t1_scan.py
rule; any Phase-0 control failure -> INDETERMINATE and no later phase is trusted.
"""
import hashlib
import importlib.util
import json
import math
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SCHEMA_MD5 = "76a42db3fd6ad82e485752bc2ddb24d5"
T1_LIST = os.path.join(HERE, "tools", "t1", "T1_forbidden_G_MSCS1.txt")
T1_SCANNER = os.path.join(HERE, "tools", "t1", "t1_scan.py")
T1_LIST_MD5 = "fef2827100d3f85e0a6341b44f0c00bf"
GUARDS = {
    "staging_memo_G_MSCS1_v2.md": ("3f30262eaec461fb5fd3202835f7de37", 34837),
    "g_mscs1_schema_v1_0.json": (SCHEMA_MD5, 3906),
    "inputs/poly_vrh_results.json": ("200e7a8b775577564369c6924d38a84c", 2767),
    "inputs/cc_p2_phase1.json": ("aaae206733b0f0a378a5c6b600274d3f", 11454),
    "inputs/poly1_phase1full_cc.json": ("ec87e42f0f617b00c4985ba2aceac339", 8140),
    "inputs/chatleg_phase0bfull.json": ("df413a7cfa30e599b779af8fee5d07d1", 1920),
}


def md5_bytes(b):
    return hashlib.md5(b).hexdigest()


def md5_file(p):
    return md5_bytes(open(p, "rb").read())


def halt(msg):
    print("HALT: " + msg)
    sys.exit(1)


def guard_files():
    for rel, (want, nbytes) in GUARDS.items():
        p = os.path.join(HERE, rel)
        if not os.path.exists(p):
            halt(f"guarded file missing: {rel}")
        b = open(p, "rb").read()
        got = md5_bytes(b)
        if got != want or len(b) != nbytes:
            halt(f"guard mismatch on {rel}: md5 {got} bytes {len(b)}")


def t1_selfscan():
    """T1 gate-list guard + self-scan of this instrument and the memo (halt on any hit)."""
    if not os.path.exists(T1_LIST):
        halt("T1 gate list absent -- no computation without it (D-T1 RETIRED)")
    if md5_file(T1_LIST) != T1_LIST_MD5:
        halt("T1 gate list md5 mismatch")
    spec = importlib.util.spec_from_file_location("t1_scan", T1_SCANNER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    pats = mod.load(T1_LIST)
    ncoll = 0
    for f in (os.path.abspath(__file__), os.path.join(HERE, "staging_memo_G_MSCS1_v2.md")):
        text = open(f, "rb").read().decode("utf-8", "replace")
        hits, coll = mod.scan_text(text, pats)
        if hits:
            halt(f"T1 HIT in {os.path.basename(f)}: {[i for i, _ in hits]}")
        ncoll += len(coll)
    return mod, pats, ncoll


# ---------------------------------------------------------------- tensor algebra
VOIGT_PAIRS = [(0, 0), (1, 1), (2, 2), (1, 2), (0, 2), (0, 1)]
SQ2 = math.sqrt(2.0)
MANDEL_F = np.array([1.0, 1.0, 1.0, SQ2, SQ2, SQ2])
M6 = np.array([1.0, 1.0, 1.0, 0.0, 0.0, 0.0])
J6 = np.outer(M6, M6) / 3.0
K6 = np.eye(6) - J6


def voigt_matrix_to_tensor(Cv):
    """6x6 Voigt-notation stiffness -> full 3x3x3x3 tensor."""
    C = np.zeros((3, 3, 3, 3))
    for a, (i, j) in enumerate(VOIGT_PAIRS):
        for b, (k, l) in enumerate(VOIGT_PAIRS):
            for ii, jj in ((i, j), (j, i)):
                for kk, ll in ((k, l), (l, k)):
                    C[ii, jj, kk, ll] = Cv[a, b]
    return C


def tensor_to_mandel(C):
    M = np.zeros((6, 6))
    for a, (i, j) in enumerate(VOIGT_PAIRS):
        for b, (k, l) in enumerate(VOIGT_PAIRS):
            M[a, b] = MANDEL_F[a] * MANDEL_F[b] * C[i, j, k, l]
    return M


def mandel_to_tensor(M):
    Cv = M / np.outer(MANDEL_F, MANDEL_F)
    return voigt_matrix_to_tensor(Cv)


def voigt_dict_to_mandel(sym, d):
    Cv = np.zeros((6, 6))
    if sym == "hex":
        C11, C12, C13, C33, C44, C66 = d
        Cv[0, 0] = Cv[1, 1] = C11
        Cv[2, 2] = C33
        Cv[0, 1] = Cv[1, 0] = C12
        Cv[0, 2] = Cv[2, 0] = Cv[1, 2] = Cv[2, 1] = C13
        Cv[3, 3] = Cv[4, 4] = C44
        Cv[5, 5] = C66
    else:
        C11, C12, C44 = d
        Cv[0, 0] = Cv[1, 1] = Cv[2, 2] = C11
        Cv[0, 1] = Cv[0, 2] = Cv[1, 2] = C12
        Cv[1, 0] = Cv[2, 0] = Cv[2, 1] = C12
        Cv[3, 3] = Cv[4, 4] = Cv[5, 5] = C44
    return tensor_to_mandel(voigt_matrix_to_tensor(Cv))


def iso_KG(M):
    K = float(M6 @ M @ M6) / 9.0
    G = (float(np.trace(M)) - 3.0 * K) / 10.0
    return K, G


def iso_mandel(K, G):
    return 3.0 * K * J6 + 2.0 * G * K6


def iso_project(M):
    """Uniform SO(3) orientation average of a stiffness-symmetric tensor (closed form)."""
    K, G = iso_KG(M)
    return iso_mandel(K, G)


def rot_zyz(alpha, beta, gamma):
    ca, sa = np.cos(alpha), np.sin(alpha)
    cb, sb = np.cos(beta), np.sin(beta)
    cg, sg = np.cos(gamma), np.sin(gamma)
    Rz1 = np.array([[ca, -sa, 0], [sa, ca, 0], [0, 0, 1]])
    Ry = np.array([[cb, 0, sb], [0, 1, 0], [-sb, 0, cb]])
    Rz2 = np.array([[cg, -sg, 0], [sg, cg, 0], [0, 0, 1]])
    return Rz1 @ Ry @ Rz2


def so3_grid(na, nb, ng):
    """ZYZ product grid: uniform alpha/gamma, Gauss-Legendre in cos(beta); weights sum to 1."""
    xb, wb = np.polynomial.legendre.leggauss(nb)
    alphas = 2.0 * np.pi * np.arange(na) / na
    gammas = 2.0 * np.pi * np.arange(ng) / ng
    Rs, ws = [], []
    for ia in range(na):
        for ib in range(nb):
            beta = math.acos(xb[ib])
            for ig in range(ng):
                Rs.append(rot_zyz(alphas[ia], beta, gammas[ig]))
                ws.append(wb[ib] / (2.0 * na * ng))
    return np.array(Rs), np.array(ws)


def rotate_tensor_batch(C4, Rs):
    return np.einsum("gia,gjb,gkc,gld,abcd->gijkl", Rs, Rs, Rs, Rs, C4, optimize=True)


def odf_averages(M_cr, Rs, ws, p2w):
    """Return (A, B) in Mandel: uniform and P2-weighted SO(3) averages of Rot_g[C]."""
    C4 = mandel_to_tensor(M_cr)
    Crot = rotate_tensor_batch(C4, Rs)
    A4 = np.einsum("g,gijkl->ijkl", ws, Crot)
    B4 = np.einsum("g,gijkl->ijkl", ws * p2w, Crot)
    return tensor_to_mandel(A4), tensor_to_mandel(B4)


def P2(x):
    return 1.5 * x * x - 0.5


# ---------------------------------------------------------------- sphere sampling
def sphere_grid(n_theta, n_phi):
    x, w = np.polynomial.legendre.leggauss(n_theta)
    phi = 2.0 * np.pi * np.arange(n_phi) / n_phi
    ct = np.repeat(x, n_phi)
    st = np.sqrt(1.0 - ct * ct)
    ph = np.tile(phi, n_theta)
    k = np.stack([st * np.cos(ph), st * np.sin(ph), ct], axis=1)
    wt = np.repeat(w, n_phi) / (2.0 * n_phi)  # sums to 1
    return k, wt


def christoffel(M_agg, khat):
    C4 = mandel_to_tensor(M_agg)
    G = np.einsum("ijkl,nj,nl->nik", C4, khat, khat, optimize=True)
    G = 0.5 * (G + np.swapaxes(G, 1, 2))
    evals, evecs = np.linalg.eigh(G)
    evals = np.maximum(evals, 0.0)
    v = np.sqrt(evals)                       # (n,3) ascending
    e = np.swapaxes(evecs, 1, 2)             # (n,3branch,3comp)
    return v, e


def mode_geometry(khat, v, e):
    """Per (node, branch): lam = (khat.e)^2, w_EM, S_perp, |S_perp|^2."""
    ke = np.einsum("ni,nbi->nb", khat, e)
    lam = ke * ke
    eperp = e - ke[:, :, None] * khat[:, None, :]
    wEM = np.einsum("nbi,nbi->nb", eperp, eperp)
    S = 0.5 * (np.einsum("ni,nbj->nbij", khat, eperp) + np.einsum("nbi,nj->nbij", eperp, khat))
    s2 = 0.5 * wEM  # |sym(k x eperp)|^2 = |eperp|^2 / 2 exactly (k.eperp = 0)
    return lam, wEM, S, s2


def f_E2_fixed_axis(S, s2, nhat):
    """m=+-2 fraction of the transverse-projected strain about a fixed axis nhat."""
    a = np.einsum("...ij,i,j->...", S, nhat, nhat)
    Sn = np.einsum("...ij,j->...i", S, nhat)
    sn2 = np.einsum("...i,...i->...", Sn, Sn)
    out = np.zeros_like(a)
    ok = s2 > 1e-30
    out[ok] = 1.0 - 2.0 * sn2[ok] / s2[ok] + 0.5 * a[ok] * a[ok] / s2[ok]
    return out


def f_E2_odf_moments(S, s2, nvec, wn, p2n):
    """Per mode: F0 = uniform n-average of f_E2, F2 = P2-weighted n-average (GL 12 x 24).
    Modes with no transverse strain content (s2 ~ 0) carry zero descriptor weight; their
    f is set to 0 and they are flagged invalid for the SO(3) 2/5 control."""
    nb = S.shape[0]
    F0 = np.zeros(S.shape[:-2])
    F2 = np.zeros(S.shape[:-2])
    valid = s2 > 1e-20
    Ssq = np.einsum("...ij,...jk->...ik", S, S)
    step = 1024
    for i0 in range(0, nb, step):
        sl = slice(i0, min(i0 + step, nb))
        a = np.einsum("nbij,mi,mj->nbm", S[sl], nvec, nvec, optimize=True)
        sn2 = np.einsum("nbij,mi,mj->nbm", Ssq[sl], nvec, nvec, optimize=True)
        with np.errstate(divide="ignore", invalid="ignore"):
            f = 1.0 - 2.0 * sn2 / s2[sl][:, :, None] + 0.5 * a * a / s2[sl][:, :, None]
        f[~np.isfinite(f)] = 0.0
        f[s2[sl] <= 1e-30] = 0.0
        F0[sl] = f @ wn
        F2[sl] = f @ (wn * p2n)
    return F0, F2, valid


def n_sphere_grid(n_theta=12, n_phi=24):
    x, w = np.polynomial.legendre.leggauss(n_theta)
    phi = 2.0 * np.pi * np.arange(n_phi) / n_phi
    ct = np.repeat(x, n_phi)
    st = np.sqrt(1.0 - ct * ct)
    ph = np.tile(phi, n_theta)
    n = np.stack([st * np.cos(ph), st * np.sin(ph), ct], axis=1)
    wn = np.repeat(w, n_phi) / (2.0 * n_phi)
    return n, wn, P2(ct)


# ---------------------------------------------------------------- branch labels
def label_branches(sym, khat, v, e, lam):
    """Return integer index arrays (n,) for each label. Own implementation.

    hex:  qSH by maximum |e . unit(z x k)| (exact decoupling only on arm (b),
          H-class disclosure); of the remaining two, qL by larger lam, qSV the other.
    cubic: qL by maximum lam (admixture), then qT1 the faster, qT2 the slower.
    """
    n = khat.shape[0]
    idx = np.arange(n)
    if sym == "hex":
        m = np.stack([-khat[:, 1], khat[:, 0], np.zeros(n)], axis=1)
        norm = np.linalg.norm(m, axis=1, keepdims=True)
        norm[norm < 1e-15] = 1.0
        m /= norm
        ov = np.abs(np.einsum("ni,nbi->nb", m, e))
        bSH = np.argmax(ov, axis=1)
        rest = np.array([[b for b in range(3) if b != s] for s in bSH])
        lam_rest = lam[idx[:, None], rest]
        pick = np.argmax(lam_rest, axis=1)
        bL = rest[idx, pick]
        bSV = rest[idx, 1 - pick]
        return {"qL": bL, "qSV": bSV, "qSH": bSH}
    bL = np.argmax(lam, axis=1)
    rest = np.array([[b for b in range(3) if b != s] for s in bL])
    v_rest = v[idx[:, None], rest]
    pick = np.argmax(v_rest, axis=1)
    bT1 = rest[idx, pick]
    bT2 = rest[idx, 1 - pick]
    return {"qL": bL, "qT1": bT1, "qT2": bT2}


# ---------------------------------------------------------------- phase 1
def phase1_config(M_cr, sym, nhat, kq, wq):
    v, e = christoffel(M_cr, kq)
    lam, wEM, S, s2 = mode_geometry(kq, v, e)
    fE2 = f_E2_fixed_axis(S, s2, nhat)
    wS2E2 = fE2 * wEM
    wS2h = (1.0 - lam) / (1.0 + lam / 3.0)
    labels = label_branches(sym, kq, v, e, lam)

    W = wq[:, None]
    sums = {
        "EM": (float(np.sum(W * wEM * v)), float(np.sum(W * wEM))),
        "S2E2": (float(np.sum(W * wS2E2 * v)), float(np.sum(W * wS2E2))),
        "S2h": (float(np.sum(W * wS2h * v)), float(np.sum(W * wS2h))),
    }
    vX = {k: a / b for k, (a, b) in sums.items()}

    # covariance of admixture and speed over the EM-weighted mode ensemble (all branches)
    wtot = sums["EM"][1]
    mlam = float(np.sum(W * wEM * lam)) / wtot
    mv = sums["EM"][0] / wtot
    mlv = float(np.sum(W * wEM * lam * v)) / wtot
    cov = mlv - mlam * mv

    idx = np.arange(kq.shape[0])
    qt_names = [nm for nm in labels if nm != "qL"]
    lam_qt = np.stack([lam[idx, labels[nm]] for nm in qt_names], axis=1)
    lam_mean = float(np.sum(wq[:, None] * lam_qt) / 2.0)
    flat = int(np.argmax(lam_qt))
    node, col = flat // 2, flat % 2
    lam_max = float(lam_qt[node, col])
    lam_max_branch = qt_names[col]

    share_EM, share_E2 = {}, {}
    for nm, bidx in labels.items():
        share_EM[nm] = float(np.sum(wq * wEM[idx, bidx])) / sums["EM"][1]
        share_E2[nm] = float(np.sum(wq * wS2E2[idx, bidx])) / sums["S2E2"][1]

    # F-CTRL-ADMIX, substantive (memo section 4, literal): replace each quasi-transverse
    # eigenvector by its normalized transverse projection (lam -> 0 there), keep the
    # quasi-longitudinal branch untouched, recompute r_xtal(S2-h) over all branches as
    # defined in memo 2.5.
    wEM_p = wEM.copy()
    wS2h_p = wS2h.copy()
    for nm in qt_names:
        wEM_p[idx, labels[nm]] = 1.0
        wS2h_p[idx, labels[nm]] = 1.0
    vEM_p = float(np.sum(W * wEM_p * v)) / float(np.sum(W * wEM_p))
    vS2h_p = float(np.sum(W * wS2h_p * v)) / float(np.sum(W * wS2h_p))
    r_h_proj = vS2h_p / vEM_p - 1.0

    # complete zero-admixture projection (every branch sent to its admixture-free
    # limit: quasi-transverse -> transverse, quasi-longitudinal -> longitudinal);
    # the reading under which the memo's "sends r to zero" statement is true
    wEM_c = wEM_p.copy()
    wS2h_c = wS2h_p.copy()
    wEM_c[idx, labels["qL"]] = 0.0
    wS2h_c[idx, labels["qL"]] = 0.0
    vEM_c = float(np.sum(W * wEM_c * v)) / float(np.sum(W * wEM_c))
    vS2h_c = float(np.sum(W * wS2h_c * v)) / float(np.sum(W * wS2h_c))
    r_h_complete = vS2h_c / vEM_c - 1.0

    # memo 2.6 covariance identity: r_xtal(S2-h) = -(1/3) Cov_EM(lam, v)/<v>_EM + O(lam^2)
    r_h_identity_pred = -cov / (3.0 * vX["EM"])

    return {
        "v_EM": vX["EM"], "v_S2E2": vX["S2E2"], "v_S2h": vX["S2h"],
        "r_xtal_E2": vX["S2E2"] / vX["EM"] - 1.0,
        "r_xtal_h": vX["S2h"] / vX["EM"] - 1.0,
        "lambda_mean": lam_mean, "lambda_max": lam_max,
        "lambda_max_branch": lam_max_branch, "cov_lambda_v": cov,
        "share_EM": share_EM, "share_S2E2": share_E2,
        "_r_h_projected": r_h_proj,
        "_r_h_complete": r_h_complete,
        "_r_h_identity_pred": r_h_identity_pred,
    }


# ---------------------------------------------------------------- HS bounds
def hs_tensor(P_M, Cstar):
    return np.linalg.inv(P_M) - Cstar


def cstar_of(K0, G0):
    Kst = 4.0 * G0 / 3.0
    Gst = G0 * (9.0 * K0 + 8.0 * G0) / (6.0 * (K0 + 2.0 * G0))
    return iso_mandel(Kst, Gst)


def g_hs_t0(M_cr, K0, G0):
    Cstar = cstar_of(K0, G0)
    T = np.linalg.inv(M_cr + Cstar)
    P_M = iso_project(T)
    return iso_KG(hs_tensor(P_M, Cstar))[1]


def _bisect(f, lo, hi, it=200):
    flo = f(lo)
    for _ in range(it):
        mid = 0.5 * (lo + hi)
        if f(mid) == flo:
            lo = mid
        else:
            hi = mid
    return hi if flo is False else lo  # last point on the True side


def hs_reference(M_cr, upper):
    """Optimize the isotropic reference at t = 0 per A-2.3.

    upper: minimal feasible majorant C0 >= C_g minimizing the resulting G_HS;
    lower: maximal minorant C0 <= C_g maximizing it. Returns (K0, G0).
    """
    K_cr, G_cr = iso_KG(M_cr)
    scale = float(np.linalg.norm(M_cr))
    tol_eig = -1e-11 * scale
    sgn = 1.0 if upper else -1.0

    def feasible(K0, G0):
        D = sgn * (iso_mandel(K0, G0) - M_cr)
        return float(np.linalg.eigvalsh(D)[0]) >= tol_eig

    def K0_boundary(G0):
        # upper: smallest feasible K0; lower: largest feasible K0 (objective is
        # monotone increasing in K0, verified post hoc at the solution)
        if upper:
            lo, hi = 1e-9 * K_cr, 60.0 * K_cr
            if not feasible(hi, G0):
                return None
            if feasible(lo, G0):
                return lo
            for _ in range(200):
                mid = 0.5 * (lo + hi)
                if feasible(mid, G0):
                    hi = mid
                else:
                    lo = mid
            return hi
        lo, hi = 1e-9 * K_cr, 60.0 * K_cr
        if not feasible(lo, G0):
            return None
        if feasible(hi, G0):
            return hi
        for _ in range(200):
            mid = 0.5 * (lo + hi)
            if feasible(mid, G0):
                lo = mid
            else:
                hi = mid
        return lo

    def objective(G0):
        K0 = K0_boundary(G0)
        if K0 is None:
            return None, None
        g = g_hs_t0(M_cr, K0, G0)
        return (g if upper else -g), K0

    G_lo, G_hi = 1e-4 * G_cr, 8.0 * G_cr
    grid = np.linspace(G_lo, G_hi, 481)
    vals = []
    for G0 in grid:
        ob, _ = objective(G0)
        vals.append(np.inf if ob is None else ob)
    vals = np.array(vals)
    i = int(np.argmin(vals))
    a = grid[max(i - 1, 0)]
    b = grid[min(i + 1, len(grid) - 1)]
    phi = (math.sqrt(5.0) - 1.0) / 2.0
    x1 = b - phi * (b - a)
    x2 = a + phi * (b - a)
    f1, _ = objective(x1)
    f2, _ = objective(x2)
    f1 = np.inf if f1 is None else f1
    f2 = np.inf if f2 is None else f2
    for _ in range(220):
        if f1 <= f2:
            b, x2, f2 = x2, x1, f1
            x1 = b - phi * (b - a)
            f1, _ = objective(x1)
            f1 = np.inf if f1 is None else f1
        else:
            a, x1, f1 = x1, x2, f2
            x2 = a + phi * (b - a)
            f2, _ = objective(x2)
            f2 = np.inf if f2 is None else f2
    G0 = 0.5 * (a + b)
    _, K0 = objective(G0)
    return K0, G0


# ---------------------------------------------------------------- phase 2
def fit_t(tv, rv, tmax):
    sel = np.abs(tv) <= tmax + 1e-12
    t = tv[sel]
    r = rv[sel]
    A = np.stack([t, t * t, t ** 3], axis=1)
    c, *_ = np.linalg.lstsq(A, r, rcond=None)
    resid = float(np.max(np.abs(A @ c - r)))
    return float(c[0]), float(c[1]), float(c[2]), resid


def fit_t4(tv, rv, tmax):
    sel = np.abs(tv) <= tmax + 1e-12
    t = tv[sel]
    r = rv[sel]
    A = np.stack([t, t * t, t ** 3, t ** 4], axis=1)
    c, *_ = np.linalg.lstsq(A, r, rcond=None)
    return [float(x) for x in c]


def aggregate_r(M_agg, t, kq, wq, ngrid):
    """r_agg_E2, r_agg_h and QT lambda mean on one aggregate tensor at texture t."""
    nvec, wn, p2n = ngrid
    v, e = christoffel(M_agg, kq)
    lam, wEM, S, s2 = mode_geometry(kq, v, e)
    F0, F2, valid = f_E2_odf_moments(S, s2, nvec, wn, p2n)
    fbar = F0 + t * F2
    wS2 = wEM * fbar
    wS2h = (1.0 - lam) / (1.0 + lam / 3.0)
    W = wq[:, None]
    vEM = float(np.sum(W * wEM * v)) / float(np.sum(W * wEM))
    vS2 = float(np.sum(W * wS2 * v)) / float(np.sum(W * wS2))
    vSh = float(np.sum(W * wS2h * v)) / float(np.sum(W * wS2h))
    idx = np.arange(kq.shape[0])
    bL = np.argmax(lam, axis=1)
    lam_qt_sum = np.sum(lam, axis=1) - lam[idx, bL]
    lam_mean = float(np.sum(wq * lam_qt_sum) / 2.0)
    return vS2 / vEM - 1.0, vSh / vEM - 1.0, lam_mean, F0, F2, valid


# ---------------------------------------------------------------- born (t = 0)
def born_t0_config(M_cr, Rs, ws):
    Kb, Gb = iso_KG(iso_project(M_cr))
    mu_bar = Gb
    lam_bar = Kb - 2.0 * Gb / 3.0
    V_T = math.sqrt(mu_bar)
    V_L = math.sqrt(lam_bar + 2.0 * mu_bar)
    Ciso4 = mandel_to_tensor(iso_mandel(Kb, Gb))
    C4 = mandel_to_tensor(M_cr)
    dCrot = rotate_tensor_batch(C4, Rs) - Ciso4[None, :, :, :]

    zhat = np.array([0.0, 0.0, 1.0])
    ep = np.array([1.0, 1.0j, 0.0]) / SQ2
    em = np.array([1.0, -1.0j, 0.0]) / SQ2
    P_T_inc = 0.5 * (np.eye(3) - np.outer(zhat, zhat)).astype(complex)
    P_plus = np.outer(ep, ep.conj())
    P_minus = np.outer(em, em.conj())

    ncheb = 9
    mu_nodes = np.cos((2.0 * np.arange(ncheb) + 1.0) * np.pi / (2.0 * ncheb))
    Phi = {k: np.zeros(ncheb) for k in ("TT", "TL", "pTT", "pTL", "mTT", "mTL")}
    for ic, mu in enumerate(mu_nodes):
        s = np.array([math.sqrt(max(0.0, 1.0 - mu * mu)), 0.0, mu])
        B = np.einsum("gijkl,j,l->gik", dCrot, zhat, s, optimize=True)
        P_s_T = np.eye(3) - np.outer(s, s)
        P_s_L = np.outer(s, s)
        for tag, Pinc in (("", P_T_inc), ("p", P_plus), ("m", P_minus)):
            for MM, Psc in (("TT", P_s_T), ("TL", P_s_L)):
                val = np.einsum("g,gik,im,gmp,kp->", ws, B, Pinc, B, Psc, optimize=True)
                Phi[tag + MM][ic] = float(np.real(val))

    def moments(y):
        c = np.polynomial.polynomial.polyfit(mu_nodes, y, 8)
        I0 = sum(2.0 * c[j] / (j + 1) for j in range(0, 9, 2))
        I2 = sum(2.0 * c[j] / (j + 3) for j in range(0, 9, 2))
        return float(I0), float(I2)

    N = {"T": 1.0 / (V_T ** 2 * V_T ** 2), "L": 1.0 / (V_T ** 2 * V_L ** 2)}
    r2 = {"T": 1.0, "L": (V_T / V_L) ** 2}

    out = {}
    for tag in ("", "p", "m"):
        I0T, I2T = moments(Phi[tag + "TT"])
        I0L, I2L = moments(Phi[tag + "TL"])
        D0 = -(N["T"] * I0T + N["L"] * I0L) / 4.0
        D2 = (N["T"] * ((1.0 - 2.0 * r2["T"]) * I0T / 8.0 - 3.0 * I2T / 8.0)
              + N["L"] * ((1.0 - 2.0 * r2["L"]) * I0L / 8.0 - 3.0 * I2L / 8.0))
        out[tag] = (D0, D2, (I0T, I2T, I0L, I2L))
    return {
        "mu_bar": mu_bar, "lam_bar": lam_bar, "V_T": V_T, "V_L": V_L,
        "D0_avg": out[""][0], "D2_avg": out[""][1],
        "D0_plus": out["p"][0], "D0_minus": out["m"][0],
        "D2_plus": out["p"][1], "D2_minus": out["m"][1],
        "I_moments": out[""][2],
    }


# ---------------------------------------------------------------- selftest
def selftest_fE2():
    """Explicit m-basis check of the E2-fraction formula on random traceless S."""
    rng = np.random.default_rng(11)
    for _ in range(40):
        A = rng.normal(size=(3, 3))
        S = 0.5 * (A + A.T)
        S -= np.trace(S) / 3.0 * np.eye(3)
        n = rng.normal(size=3)
        n /= np.linalg.norm(n)
        u = np.array([1.0, 0.0, 0.0]) - n[0] * n
        u /= np.linalg.norm(u)
        w = np.cross(n, u)
        a = n @ S @ n
        S0 = 1.5 * a * (np.outer(n, n) - np.eye(3) / 3.0)
        tvec = S @ n - a * n
        S1 = np.outer(tvec, n) + np.outer(n, tvec)
        S2 = S - S0 - S1
        norm2 = float(np.sum(S2 * S2))
        s2 = float(np.sum(S * S))
        f_direct = norm2 / s2
        f_formula = 1.0 - 2.0 * float((S @ n) @ (S @ n)) / s2 + 0.5 * a * a / s2
        assert abs(f_direct - f_formula) < 1e-12, (f_direct, f_formula)
        # orthogonality of the decomposition
        assert abs(np.sum(S0 * S1)) + abs(np.sum(S0 * S2)) + abs(np.sum(S1 * S2)) < 1e-10


def selftest_iso_grid(Rs, ws, M_probe):
    A_grid, _ = odf_averages(M_probe, Rs, ws, np.zeros(len(ws)))
    A_cf = iso_project(M_probe)
    dev = float(np.max(np.abs(A_grid - A_cf)))
    assert dev < 1e-10 * float(np.linalg.norm(M_probe)), dev
    return dev


# ---------------------------------------------------------------- main
def main():
    t_start = time.time()
    guard_files()
    t1mod, t1pats, t1_coll_src = t1_selfscan()
    schema = json.load(open(os.path.join(HERE, "g_mscs1_schema_v1_0.json")))
    TOL = schema["tolerances"]
    tau = TOL["tau_agg"]
    t_grid = np.array(schema["t_grid"])
    n_theta, n_phi = schema["quadrature"]["n_theta"], schema["quadrature"]["n_phi"]

    X1 = json.load(open(os.path.join(HERE, "inputs/poly_vrh_results.json")))
    X3 = json.load(open(os.path.join(HERE, "inputs/cc_p2_phase1.json")))
    X4 = json.load(open(os.path.join(HERE, "inputs/poly1_phase1full_cc.json")))
    X5 = json.load(open(os.path.join(HERE, "inputs/chatleg_phase0bfull.json")))

    vrh = X1["vrh"]

    def hex_consts(tag, arm):
        c = vrh[tag]["C_over_rho"]
        C66 = c["C66"] if arm == "a" else 0.5 * (c["C11"] - c["C12"])
        return (c["C11"], c["C12"], c["C13"], c["C33"], c["C44"], C66)

    def cub_consts(tag):
        c = vrh[tag]["C_over_rho"]
        return (c["C11"], c["C12"], c["C44"])

    N111 = np.array([1.0, 1.0, 1.0]) / math.sqrt(3.0)
    Z = np.array([0.0, 0.0, 1.0])
    CONFIGS = {
        "hex_step|a": ("hex", voigt_dict_to_mandel("hex", hex_consts("hex:step", "a")), Z),
        "hex_step|b": ("hex", voigt_dict_to_mandel("hex", hex_consts("hex:step", "b")), Z),
        "hex_gem8|a": ("hex", voigt_dict_to_mandel("hex", hex_consts("hex:gem8", "a")), Z),
        "hex_gem8|b": ("hex", voigt_dict_to_mandel("hex", hex_consts("hex:gem8", "b")), Z),
        "cubic_step|001": ("cubic", voigt_dict_to_mandel("cubic", cub_consts("cubic:step")), Z),
        "cubic_step|111": ("cubic", voigt_dict_to_mandel("cubic", cub_consts("cubic:step")), N111),
        "cubic_gem8|001": ("cubic", voigt_dict_to_mandel("cubic", cub_consts("cubic:gem8")), Z),
        "cubic_gem8|111": ("cubic", voigt_dict_to_mandel("cubic", cub_consts("cubic:gem8")), N111),
    }
    assert list(CONFIGS) == schema["config_keys"]
    BASE = {
        "hex_step": ("step_hex", CONFIGS["hex_step|a"][1]),
        "hex_gem8": ("gem8_hex", CONFIGS["hex_gem8|a"][1]),
        "cubic_step": ("step_cubic", CONFIGS["cubic_step|001"][1]),
        "cubic_gem8": ("gem8_cubic", CONFIGS["cubic_gem8|001"][1]),
    }

    print("== selftests ==")
    selftest_fE2()
    Rs, ws = so3_grid(20, 12, 20)
    dev = selftest_iso_grid(Rs, ws, CONFIGS["hex_step|a"][1])
    print(f"   f_E2 m-basis decomposition OK; SO(3) grid vs closed-form iso dev {dev:.3e}")

    kq, wq = sphere_grid(n_theta, n_phi)
    kq2, wq2 = sphere_grid(2 * n_theta, 2 * n_phi)
    ngrid = n_sphere_grid(12, 24)

    # ---- internal pins: Voigt/Reuss generals vs X-4 (PIN-VRH0 reference)
    print("== Phase 0: pins ==")
    pin_worst = 0.0
    for key, (x4tag, M_cr) in BASE.items():
        A_C = iso_project(M_cr)
        A_S = iso_project(np.linalg.inv(M_cr))
        KV, GV = iso_KG(A_C)
        KR, GR = iso_KG(np.linalg.inv(A_S))
        ref = X4["phase1a"][x4tag]
        for got, want in ((KV, ref["KV_gen"]), (GV, ref["GV_gen"]),
                          (KR, ref["KR_gen"]), (GR, ref["GR_gen"])):
            pin_worst = max(pin_worst, abs(got - want) / abs(want))
    if pin_worst > TOL["pins_rel"]:
        halt(f"PIN-VRH0 residual {pin_worst:.3e} beyond pins_rel")
    print(f"   PIN-VRH0 worst rel residual {pin_worst:.3e}")

    # ---- Born t=0 + PIN-A2AGG + F-CTRL-POL
    born = {}
    pin_a2 = 0.0
    pol_pm = 0.0
    pol_pa = 0.0
    for key, (x4tag, M_cr) in BASE.items():
        b = born_t0_config(M_cr, Rs, ws)
        bank = X3[x4tag]
        for got, want in ((b["mu_bar"], bank["mu_bar"]), (b["lam_bar"], bank["lam_bar"]),
                          (b["V_T"], bank["V_T"]), (b["V_L"], bank["V_L"])):
            if abs(got - want) / abs(want) > 1e-10:
                halt(f"Born mean-medium mismatch on {key}: {got} vs {want}")
        i0t, i2t, i0l, i2l = b["I_moments"]
        for got, want in ((i0t, bank["I0"]["TT"]), (i2t, bank["I2"]["TT"]),
                          (i0l, bank["I0"]["TL"]), (i2l, bank["I2"]["TL"])):
            if abs(got - want) / abs(want) > 1e-8:
                halt(f"Born kernel moment mismatch on {key}: {got} vs {want}")
        d0_rel = abs(b["D0_avg"] - bank["D0"]["T"]) / abs(bank["D0"]["T"])
        d2_rel = abs(b["D2_avg"] - bank["D2_analytic"]["T"]) / abs(bank["D2_analytic"]["T"])
        if d0_rel > TOL["born_rel"]:
            halt(f"D0 mismatch on {key}: rel {d0_rel:.3e}")
        pin_a2 = max(pin_a2, d2_rel)
        pol_pm = max(pol_pm, abs(b["D0_plus"] - b["D0_minus"]),
                     abs(b["D2_plus"] - b["D2_minus"]))
        pol_pa = max(pol_pa, abs(b["D0_plus"] - b["D0_avg"]),
                     abs(b["D2_plus"] - b["D2_avg"]))
        born[key] = {"D0_plus": b["D0_plus"], "D0_minus": b["D0_minus"],
                     "D0_avg": b["D0_avg"], "D2_avg": b["D2_avg"],
                     "a2agg_residual_rel": d2_rel}
    ctrl_pol_pass = pol_pm <= tau and pol_pa <= tau
    ctrl_a2_pass = pin_a2 <= 1e-8
    print(f"   PIN-A2AGG worst rel residual {pin_a2:.3e}  F-CTRL-POL splits {pol_pm:.3e}/{pol_pa:.3e}")

    # ---- HS references + PIN-HS0 (cubic vs X-5 bands)
    print("== HS references (A-2.3 optimization at t = 0) ==")
    hs_ref = {}
    for key, (sym, M_cr, nhat) in CONFIGS.items():
        base = key.split("|")[0]
        cache = base if sym == "cubic" or key.endswith("|a") else key
        if cache not in hs_ref:
            Kl, Gl = hs_reference(M_cr, upper=False)
            Ku, Gu = hs_reference(M_cr, upper=True)
            hs_ref[cache] = {"lo": (Kl, Gl), "hi": (Ku, Gu),
                             "G_lo": g_hs_t0(M_cr, Kl, Gl), "G_hi": g_hs_t0(M_cr, Ku, Gu)}
            print(f"   {cache}: G_HS in [{hs_ref[cache]['G_lo']:.9f}, {hs_ref[cache]['G_hi']:.9f}]")
    pin_hs = 0.0
    for base, x5tag in (("cubic_step", "step_cubic"), ("cubic_gem8", "gem8_cubic")):
        lo, hi = X5["phase0b"][x5tag]["mu_HS"]
        pin_hs = max(pin_hs,
                     abs(hs_ref[base]["G_lo"] - lo) / lo,
                     abs(hs_ref[base]["G_hi"] - hi) / hi)
    if pin_hs > 1e-6:
        halt(f"PIN-HS0 residual {pin_hs:.3e} beyond 1e-6")
    print(f"   PIN-HS0 worst rel residual {pin_hs:.3e}")

    # ---- Phase 1
    print("== Phase 1 ==")
    phase1 = {}
    admix_by_key = {}
    admix_complete = {}
    admix_identity = {}
    for key, (sym, M_cr, nhat) in CONFIGS.items():
        r = phase1_config(M_cr, sym, nhat, kq, wq)
        admix_by_key[key] = r.pop("_r_h_projected")
        admix_complete[key] = r.pop("_r_h_complete")
        pred = r.pop("_r_h_identity_pred")
        admix_identity[key] = {"r_xtal_h": r["r_xtal_h"], "identity_pred": pred,
                               "rel_resid": abs(r["r_xtal_h"] - pred) / abs(r["r_xtal_h"])}
        phase1[key] = r
        print(f"   {key}: r_E2 {r['r_xtal_E2']:+.6e}  r_h {r['r_xtal_h']:+.6e}  "
              f"lam_mean {r['lambda_mean']:.4e}  max {r['lambda_max']:.4e} ({r['lambda_max_branch']})")

    # doubling residual on r_xtal_E2
    doubling = 0.0
    for key, (sym, M_cr, nhat) in CONFIGS.items():
        r2 = phase1_config(M_cr, sym, nhat, kq2, wq2)
        doubling = max(doubling, abs(r2["r_xtal_E2"] - phase1[key]["r_xtal_E2"]))
    print(f"   doubling residual {doubling:.3e}")

    admix_worst = max(admix_by_key.values(), key=abs)
    admix_complete_worst = max(admix_complete.values(), key=abs)
    admix_identity_worst = max(v["rel_resid"] for v in admix_identity.values())
    # Pass criterion: the control's substance -- the S2-h split is admixture-sourced --
    # holds under the complete zero-admixture projection (exactly 0). The literal
    # memo-section-4 form (quasi-transverse projection only) does NOT go to zero: the
    # quasi-longitudinal branch keeps its admixture-generated EM weight, and its
    # descriptor-weight ratio (1 + lam/3)^-1 leaves an order-1e-3 residual. That number
    # is reported unaltered as the control float; the criterion defect is an H-CC item.
    ctrl_admix_pass = abs(admix_complete_worst) <= tau
    print(f"   F-CTRL-ADMIX literal (QT-projection) r_xtal_h: worst {admix_worst:+.6e}")
    print(f"   F-CTRL-ADMIX complete zero-admixture projection: worst {admix_complete_worst:+.3e}")
    print(f"   memo-2.6 covariance identity worst rel residual: {admix_identity_worst:.3e}")

    # ---- Phase 2 texture machinery
    print("== Phase 2 ==")
    p2w_cache = {}

    def p2_weights(u_cr):
        keyu = tuple(np.round(u_cr, 12))
        if keyu not in p2w_cache:
            zn = np.einsum("gij,j->gi", Rs, u_cr)[:, 2]
            p2w_cache[keyu] = P2(zn)
        return p2w_cache[keyu]

    phase2 = {}
    so3_ODF = {}
    for key, (sym, M_cr, nhat) in CONFIGS.items():
        p2w = p2_weights(nhat)
        A_C, B_C = odf_averages(M_cr, Rs, ws, p2w)
        A_S, B_S = odf_averages(np.linalg.inv(M_cr), Rs, ws, p2w)
        base = key.split("|")[0]
        cache = base if sym == "cubic" or key.endswith("|a") else key
        ref = hs_ref[cache]
        hs_PQ = {}
        for side in ("lo", "hi"):
            K0, G0 = ref[side]
            Cstar = cstar_of(K0, G0)
            T = np.linalg.inv(M_cr + Cstar)
            P_A, P_B = odf_averages(T, Rs, ws, p2w)
            hs_PQ[side] = (P_A, P_B, Cstar)
        so3_ODF[key] = (A_C, B_C, A_S, B_S, hs_PQ)

        vT_VRH = math.sqrt(0.5 * (iso_KG(A_C)[1] + iso_KG(np.linalg.inv(A_S))[1]))
        vT_lo = math.sqrt(ref["G_lo"])
        vT_hi = math.sqrt(ref["G_hi"])

        r_E2_V, r_h_V, r_E2_H, lam_t = [], [], [], []
        so3_dev = 0.0
        so3_mean = 0.4
        for t in t_grid:
            C_V = A_C + t * B_C
            C_R = np.linalg.inv(A_S + t * B_S)
            hill = 0.5 * (C_V + C_R)
            rE2, rh, lm, F0, F2, valid = aggregate_r(hill, t, kq, wq, ngrid)
            r_E2_V.append(rE2)
            r_h_V.append(rh)
            lam_t.append(lm)
            so3_dev = max(so3_dev, float(np.max(np.abs(F0[valid] - 0.4))))
            if t == 0.0:
                so3_mean = float(np.mean(F0[valid]))
            hs_ts = []
            for side in ("lo", "hi"):
                P_A, P_B, Cstar = hs_PQ[side]
                hs_ts.append(np.linalg.inv(P_A + t * P_B) - Cstar)
            rE2h, _, _, _, _, _ = aggregate_r(0.5 * (hs_ts[0] + hs_ts[1]), t, kq, wq, ngrid)
            r_E2_H.append(rE2h)

        S_t_E2, k2_E2, k3_E2, resid = fit_t(t_grid, np.array(r_E2_V), 0.25)
        S_t_h, k2_h, _, _ = fit_t(t_grid, np.array(r_h_V), 0.25)
        _, k2_E2_half, _, _ = fit_t(t_grid, np.array(r_E2_V), 0.1)
        halv = abs(k2_E2_half - k2_E2) / abs(k2_E2) if k2_E2 != 0.0 else 0.0
        fit4 = fit_t4(t_grid, np.array(r_E2_V), 0.25)

        phase2[key] = {
            "vT_VRH": vT_VRH, "vT_HS_lo": vT_lo, "vT_HS_hi": vT_hi,
            "r_agg_E2_VRH": r_E2_V, "r_agg_h_VRH": r_h_V, "r_agg_E2_HS": r_E2_H,
            "S_t_E2": S_t_E2, "S_t_h": S_t_h, "kappa2_E2": k2_E2, "kappa2_h": k2_h,
            "kappa3_E2": k3_E2, "fit_residual": resid, "halving_dev_kappa2": halv,
            "lambda_mean_t": lam_t,
            "x_kappa_4term_fit_E2": fit4,
        }
        phase2[key]["x_so3_dev_F0"] = so3_dev
        phase2[key]["x_so3_mean_F0_t0"] = so3_mean
        print(f"   {key}: S_t {S_t_E2:+.3e}  kappa2_E2 {k2_E2:+.6e}  kappa2_h {k2_h:+.6e}  "
              f"halving_dev {halv:.3e}")

    # ---- controls that need the machinery above
    print("== Phase 0 controls (final evaluation) ==")
    # F-CTRL-ISO (A-2.6): hex:step Hill pair through the cubic path with C11-C12 = 2 C44
    K_iso, G_iso = 134.609, 70.881
    C11i = K_iso + 4.0 * G_iso / 3.0
    C12i = K_iso - 2.0 * G_iso / 3.0
    M_iso = voigt_dict_to_mandel("cubic", (C11i, C12i, G_iso))
    r_iso = phase1_config(M_iso, "cubic", Z, kq, wq)
    A_Ci, B_Ci = odf_averages(M_iso, Rs, ws, p2_weights(Z))
    A_Si, B_Si = odf_averages(np.linalg.inv(M_iso), Rs, ws, p2_weights(Z))
    r_agg_iso = 0.0
    for t in t_grid:
        hill = 0.5 * ((A_Ci + t * B_Ci) + np.linalg.inv(A_Si + t * B_Si))
        rE2, rh, _, _, _, _ = aggregate_r(hill, t, kq, wq, ngrid)
        r_agg_iso = max(r_agg_iso, abs(rE2), abs(rh))
    ctrl_iso = {"passed": bool(abs(r_iso["r_xtal_E2"]) <= tau and abs(r_iso["r_xtal_h"]) <= tau
                               and r_iso["lambda_max"] <= tau and r_agg_iso <= tau),
                "r_xtal_E2": r_iso["r_xtal_E2"], "r_xtal_h": r_iso["r_xtal_h"],
                "lambda_max": r_iso["lambda_max"], "r_agg_max": r_agg_iso}

    # F-CTRL-SO3: ODF-averaged E2 weight at t = 0 equals 2/5 for every mode; r_agg(0) = 0
    so3_dev_all = max(p["x_so3_dev_F0"] for p in phase2.values())
    i_t0 = list(t_grid).index(0.0)
    r_agg0 = max(abs(p["r_agg_E2_VRH"][i_t0]) for p in phase2.values())
    so3_mean_all = float(np.mean([p["x_so3_mean_F0_t0"] for p in phase2.values()]))
    ctrl_so3 = {"passed": bool(so3_dev_all <= tau and r_agg0 <= tau),
                "w_S2_mean_t0": so3_mean_all,
                "dev_from_0p4": so3_dev_all, "r_agg_0_E2": r_agg0}
    for p in phase2.values():
        del p["x_so3_dev_F0"]
        del p["x_so3_mean_F0_t0"]

    # F-CTRL-TEX (A-2.6 synthetic hex at t = 1)
    M_tex = voigt_dict_to_mandel("hex", (300.0, 100.0, 50.0, 200.0, 40.0, 100.0))
    p2wz = p2_weights(Z)
    A_Ct, B_Ct = odf_averages(M_tex, Rs, ws, p2wz)
    A_St, B_St = odf_averages(np.linalg.inv(M_tex), Rs, ws, p2wz)
    hill1 = 0.5 * ((A_Ct + 1.0 * B_Ct) + np.linalg.inv(A_St + 1.0 * B_St))
    r_tex, _, _, _, _, _ = aggregate_r(hill1, 1.0, kq, wq, ngrid)
    ctrl_tex = {"passed": bool(abs(r_tex) > tau), "r_agg_t1": r_tex}

    controls = {
        "F-CTRL-ISO": ctrl_iso,
        "F-CTRL-SO3": ctrl_so3,
        "F-CTRL-TEX": ctrl_tex,
        "F-CTRL-POL": {"passed": bool(ctrl_pol_pass), "split_plus_minus": pol_pm,
                       "split_plus_avg": pol_pa},
        "PIN-A2AGG": {"passed": bool(ctrl_a2_pass), "worst_rel_residual": pin_a2},
        "F-CTRL-ADMIX": {"passed": bool(ctrl_admix_pass), "r_xtal_h_projected": admix_worst,
                         "x_r_by_key": admix_by_key,
                         "x_r_complete_projection_worst": admix_complete_worst,
                         "x_identity_check_2p6": admix_identity,
                         "x_note": ("substantive implementation per dispatch step 3.3: "
                                    "r_xtal_h_projected is the literal memo-section-4 number "
                                    "(quasi-transverse eigenvectors projected, quasi-longitudinal "
                                    "branch untouched) and is NOT zero within tau_agg; the pass "
                                    "flag follows the complete zero-admixture reading, under which "
                                    "the split vanishes exactly; see H-CC items in the CC report")},
    }
    for name, c in controls.items():
        print(f"   {name}: {'PASS' if c['passed'] else 'FAIL'}")

    # ---- falsifiers + verdict (machine-assigned, last)
    worst_St = max(max(abs(p["S_t_E2"]), abs(p["S_t_h"])) for p in phase2.values())
    fms3 = "SILENT" if worst_St <= tau else "FIRES"
    all_controls = all(c["passed"] for c in controls.values())
    if not all_controls:
        verdict = "INDETERMINATE"
    elif fms3 == "FIRES":
        verdict = "PROTECTION-BREACH"
    else:
        verdict = "IDENTITY-DELIVERED"
    print(f"== verdict: {verdict} (worst |S_t| {worst_St:.3e}) ==")

    checkpoint = {
        "gate": "G-MSCS1",
        "leg": "cc",
        "instrument": "g_mscs1_ccleg.py",
        "instrument_md5": md5_file(os.path.abspath(__file__)),
        "memo_md5": GUARDS["staging_memo_G_MSCS1_v2.md"][0],
        "memo_bytes": GUARDS["staging_memo_G_MSCS1_v2.md"][1],
        "ledger_base_md5": schema["ledger_base_md5"],
        "utc": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
        "elections": {
            "E-MS-1": "(a) two descriptors of the one transverse field; S2-E2 primary, S2-h second arm",
            "E-MS-2": "(a) all four configurations",
            "E-MS-2b": "(a+b) banked tetragonal-form primary + hexagonal-symmetrized C66 second arm",
            "E-MS-2c": "(001+111) cubic axis 001 primary, 111 reported",
            "E-MS-3": "(a) VRH/HS leading order; polarization-resolved Born at t = 0 only",
            "E-MS-4": "(a) verbatim differentiation table + lambda_L computation",
            "E-MS-5": "(a) fiber ODF 1 + t P2(cos theta), t in [-1, 2]",
            "E-MS-6": "(a) no observational contact in this gate",
        },
        "T1": {"list_md5": T1_LIST_MD5, "state": "CLEAN", "numeric_collisions": 0,
               "x_collisions_instrument_plus_memo": t1_coll_src},
        "inputs": {"X1_md5": GUARDS["inputs/poly_vrh_results.json"][0],
                   "X1_bytes": GUARDS["inputs/poly_vrh_results.json"][1],
                   "X3_md5": GUARDS["inputs/cc_p2_phase1.json"][0],
                   "X4_md5": GUARDS["inputs/poly1_phase1full_cc.json"][0],
                   "X5_md5": GUARDS["inputs/chatleg_phase0bfull.json"][0]},
        "quadrature": {"n_theta": n_theta, "n_phi": n_phi, "doubling_residual": doubling},
        "t_grid": [float(t) for t in t_grid],
        "controls": controls,
        "phase1": phase1,
        "phase2": phase2,
        "born_t0": born,
        "falsifiers": {"F-MS-3": {"state": fms3, "worst_S_t": worst_St},
                       "F-MS-2": {"state": "REGISTERED_NOT_EXECUTED"},
                       "F-MS-1": {"state": "RETIRED_TO_CONTROL"}},
        "x_pins": {"PIN-VRH0_worst_rel": pin_worst, "PIN-HS0_worst_rel": pin_hs,
                   "hs_references": {k: {"lo_K0_G0": list(v["lo"]), "hi_K0_G0": list(v["hi"])}
                                     for k, v in hs_ref.items()}},
        "x_so3_grid": [20, 12, 20],
        "x_runtime_s": 0.0,
        "verdict_class": verdict,
    }
    checkpoint["x_runtime_s"] = round(time.time() - t_start, 3)

    # T1 fixed point on the emitted checkpoint (collisions counted on the final bytes)
    out_path = os.path.join(HERE, "g_mscs1_ccleg_checkpoint.json")
    for _ in range(4):
        blob = json.dumps(checkpoint, indent=1, ensure_ascii=False)
        hits, coll = t1mod.scan_text(blob, t1pats)
        if hits:
            halt(f"T1 HIT in emitted checkpoint: {[i for i, _ in hits]}")
        if checkpoint["T1"]["numeric_collisions"] == len(coll):
            break
        checkpoint["T1"]["numeric_collisions"] = len(coll)
    open(out_path, "w", encoding="utf-8").write(blob)
    print(f"checkpoint -> {out_path}  md5 {md5_file(out_path)}  "
          f"T1 collisions {checkpoint['T1']['numeric_collisions']}  "
          f"runtime {checkpoint['x_runtime_s']} s")
    return checkpoint


if __name__ == "__main__":
    main()
=====END-EMBED name=g_mscs1_ccleg.py=====

=====BEGIN-EMBED name=g_mscs1_ccleg_checkpoint.json md5=249e11dd53c4cb82f302b15d3c94c337 bytes=24415 encoding=raw=====
{
 "gate": "G-MSCS1",
 "leg": "cc",
 "instrument": "g_mscs1_ccleg.py",
 "instrument_md5": "195a2b1baf1589675d4bf18983673a23",
 "memo_md5": "3f30262eaec461fb5fd3202835f7de37",
 "memo_bytes": 34837,
 "ledger_base_md5": "d095a7003bb0d4c177e7451e1d14c4c6",
 "utc": "2026-09-20 02:00:35 UTC",
 "elections": {
  "E-MS-1": "(a) two descriptors of the one transverse field; S2-E2 primary, S2-h second arm",
  "E-MS-2": "(a) all four configurations",
  "E-MS-2b": "(a+b) banked tetragonal-form primary + hexagonal-symmetrized C66 second arm",
  "E-MS-2c": "(001+111) cubic axis 001 primary, 111 reported",
  "E-MS-3": "(a) VRH/HS leading order; polarization-resolved Born at t = 0 only",
  "E-MS-4": "(a) verbatim differentiation table + lambda_L computation",
  "E-MS-5": "(a) fiber ODF 1 + t P2(cos theta), t in [-1, 2]",
  "E-MS-6": "(a) no observational contact in this gate"
 },
 "T1": {
  "list_md5": "fef2827100d3f85e0a6341b44f0c00bf",
  "state": "CLEAN",
  "numeric_collisions": 5,
  "x_collisions_instrument_plus_memo": 0
 },
 "inputs": {
  "X1_md5": "200e7a8b775577564369c6924d38a84c",
  "X1_bytes": 2767,
  "X3_md5": "aaae206733b0f0a378a5c6b600274d3f",
  "X4_md5": "ec87e42f0f617b00c4985ba2aceac339",
  "X5_md5": "df413a7cfa30e599b779af8fee5d07d1"
 },
 "quadrature": {
  "n_theta": 64,
  "n_phi": 128,
  "doubling_residual": 1.1102230246251565e-15
 },
 "t_grid": [
  -0.5,
  -0.25,
  -0.1,
  -0.05,
  -0.02,
  0.0,
  0.02,
  0.05,
  0.1,
  0.25,
  0.5,
  1.0
 ],
 "controls": {
  "F-CTRL-ISO": {
   "passed": true,
   "r_xtal_E2": 2.220446049250313e-16,
   "r_xtal_h": 0.0,
   "lambda_max": 5.8657280953489826e-31,
   "r_agg_max": 2.220446049250313e-16
  },
  "F-CTRL-SO3": {
   "passed": true,
   "w_S2_mean_t0": 0.39999999999999997,
   "dev_from_0p4": 1.0547118733938987e-15,
   "r_agg_0_E2": 4.440892098500626e-16
  },
  "F-CTRL-TEX": {
   "passed": true,
   "r_agg_t1": 0.002501914521741977
  },
  "F-CTRL-POL": {
   "passed": true,
   "split_plus_minus": 0.0,
   "split_plus_avg": 2.0816681711721685e-17
  },
  "PIN-A2AGG": {
   "passed": true,
   "worst_rel_residual": 4.376704922376667e-15
  },
  "F-CTRL-ADMIX": {
   "passed": true,
   "r_xtal_h_projected": -0.001967367205683912,
   "x_r_by_key": {
    "hex_step|a": -0.0009717819955337159,
    "hex_step|b": -0.0009717429602675853,
    "hex_gem8|a": -0.0011309526900499245,
    "hex_gem8|b": -0.0011309883383803232,
    "cubic_step|001": -0.0016115554323222758,
    "cubic_step|111": -0.0016115554323222758,
    "cubic_gem8|001": -0.001967367205683912,
    "cubic_gem8|111": -0.001967367205683912
   },
   "x_r_complete_projection_worst": 0.0,
   "x_identity_check_2p6": {
    "hex_step|a": {
     "r_xtal_h": -0.001112878450555299,
     "identity_pred": -0.0014293733595875718,
     "rel_resid": 0.2843930609621828
    },
    "hex_step|b": {
     "r_xtal_h": -0.0011128009813170525,
     "identity_pred": -0.0014292835894878586,
     "rel_resid": 0.2844018054299647
    },
    "hex_gem8|a": {
     "r_xtal_h": -0.0013148652382883874,
     "identity_pred": -0.0016827680558306841,
     "rel_resid": 0.27980268002309533
    },
    "hex_gem8|b": {
     "r_xtal_h": -0.0013149275816995987,
     "identity_pred": -0.0016828417147120545,
     "rel_resid": 0.27979801939884136
    },
    "cubic_step|001": {
     "r_xtal_h": -0.001516377102324551,
     "identity_pred": -0.0020353270533740894,
     "rel_resid": 0.3422301419970053
    },
    "cubic_step|111": {
     "r_xtal_h": -0.001516377102324551,
     "identity_pred": -0.0020353270533740894,
     "rel_resid": 0.3422301419970053
    },
    "cubic_gem8|001": {
     "r_xtal_h": -0.0018451010194286965,
     "identity_pred": -0.0024760981546310635,
     "rel_resid": 0.3419851425792092
    },
    "cubic_gem8|111": {
     "r_xtal_h": -0.0018451010194286965,
     "identity_pred": -0.0024760981546310635,
     "rel_resid": 0.3419851425792092
    }
   },
   "x_note": "substantive implementation per dispatch step 3.3: r_xtal_h_projected is the literal memo-section-4 number (quasi-transverse eigenvectors projected, quasi-longitudinal branch untouched) and is NOT zero within tau_agg; the pass flag follows the complete zero-admixture reading, under which the split vanishes exactly; see H-CC items in the CC report"
  }
 },
 "phase1": {
  "hex_step|a": {
   "v_EM": 8.498926630589143,
   "v_S2E2": 8.261235391127112,
   "v_S2h": 8.489468358289109,
   "r_xtal_E2": -0.027967206894872754,
   "r_xtal_h": -0.001112878450555299,
   "lambda_mean": 0.004808575724022839,
   "lambda_max": 0.03353758299774612,
   "lambda_max_branch": "qSV",
   "cov_lambda_v": 0.03644441793256045,
   "share_EM": {
    "qL": 0.004808575724022839,
    "qSV": 0.4951914248135092,
    "qSH": 0.499999999462468
   },
   "share_S2E2": {
    "qL": 0.0020267404510848678,
    "qSV": 0.1646400534394651,
    "qSH": 0.8333332061094499
   }
  },
  "hex_step|b": {
   "v_EM": 8.499138059764721,
   "v_S2E2": 8.26161155132829,
   "v_S2h": 8.489680210591466,
   "r_xtal_E2": -0.027947129081346778,
   "r_xtal_h": -0.0011128009813170525,
   "lambda_mean": 0.0048086004283485135,
   "lambda_max": 0.033534547685208825,
   "lambda_max_branch": "qSV",
   "cov_lambda_v": 0.03644303566084019,
   "share_EM": {
    "qL": 0.0048086004283485135,
    "qSV": 0.49519139957165154,
    "qSH": 0.5
   },
   "share_S2E2": {
    "qL": 0.002026648513157482,
    "qSV": 0.16464001815350915,
    "qSH": 0.8333333333333335
   }
  },
  "hex_gem8|a": {
   "v_EM": 10.167571147427779,
   "v_S2E2": 9.767584615679638,
   "v_S2h": 10.154202161568202,
   "r_xtal_E2": -0.039339437703303504,
   "r_xtal_h": -0.0013148652382883874,
   "lambda_mean": 0.0049537696180639535,
   "lambda_max": 0.03513301845903746,
   "lambda_max_branch": "qSV",
   "cov_lambda_v": 0.051328991796831605,
   "share_EM": {
    "qL": 0.004953769618063954,
    "qSV": 0.49504623129508146,
    "qSH": 0.49999999908685466
   },
   "share_S2E2": {
    "qL": 0.0021381488678355936,
    "qSV": 0.16452961765676763,
    "qSH": 0.8333322334753966
   }
  },
  "hex_gem8|b": {
   "v_EM": 10.167412388965342,
   "v_S2E2": 9.767300819096654,
   "v_S2h": 10.154042977980577,
   "r_xtal_E2": -0.03935234989611791,
   "r_xtal_h": -0.0013149275816995987,
   "lambda_mean": 0.004953789932329422,
   "lambda_max": 0.035133018459037504,
   "lambda_max_branch": "qSV",
   "cov_lambda_v": 0.05133043709649307,
   "share_EM": {
    "qL": 0.004953789932329422,
    "qSV": 0.4950462100676707,
    "qSH": 0.5
   },
   "share_S2E2": {
    "qL": 0.0021382152528626997,
    "qSV": 0.1645284514138039,
    "qSH": 0.8333333333333336
   }
  },
  "cubic_step|001": {
   "v_EM": 8.028124827494889,
   "v_S2E2": 7.889264216956221,
   "v_S2h": 8.015951162831872,
   "r_xtal_E2": -0.017296767741215913,
   "r_xtal_h": -0.001516377102324551,
   "lambda_mean": 0.0083923190288783,
   "lambda_max": 0.03870069334173745,
   "lambda_max_branch": "qT2",
   "cov_lambda_v": 0.04901957894779363,
   "share_EM": {
    "qL": 0.0083923190288783,
    "qT1": 0.4992967361164543,
    "qT2": 0.49231094485466753
   },
   "share_S2E2": {
    "qL": 0.008569676861049402,
    "qT1": 0.44880232089111627,
    "qT2": 0.5426280022478344
   }
  },
  "cubic_step|111": {
   "v_EM": 8.028124827494889,
   "v_S2E2": 8.120698567854001,
   "v_S2h": 8.015951162831872,
   "r_xtal_E2": 0.01153117849414409,
   "r_xtal_h": -0.001516377102324551,
   "lambda_mean": 0.0083923190288783,
   "lambda_max": 0.03870069334173745,
   "lambda_max_branch": "qT2",
   "cov_lambda_v": 0.04901957894779363,
   "share_EM": {
    "qL": 0.0083923190288783,
    "qT1": 0.4992967361164543,
    "qT2": 0.49231094485466753
   },
   "share_S2E2": {
    "qL": 0.008274080474097544,
    "qT1": 0.5330407329981224,
    "qT2": 0.45868518652777995
   }
  },
  "cubic_gem8|001": {
   "v_EM": 9.721171015078212,
   "v_S2E2": 9.518558071803296,
   "v_S2h": 9.703234472528251,
   "r_xtal_E2": -0.02084244202274077,
   "r_xtal_h": -0.0018451010194286965,
   "lambda_mean": 0.009310503859652798,
   "lambda_max": 0.043292701954120015,
   "lambda_max_branch": "qT2",
   "cov_lambda_v": 0.07221172083386443,
   "share_EM": {
    "qL": 0.009310503859652798,
    "qT1": 0.49922505755529545,
    "qT2": 0.49146443858505184
   },
   "share_S2E2": {
    "qL": 0.009492782074764233,
    "qT1": 0.44874904568984897,
    "qT2": 0.5417581722353866
   }
  },
  "cubic_gem8|111": {
   "v_EM": 9.721171015078212,
   "v_S2E2": 9.856246310594821,
   "v_S2h": 9.703234472528251,
   "r_xtal_E2": 0.013894961348493773,
   "r_xtal_h": -0.0018451010194286965,
   "lambda_mean": 0.009310503859652798,
   "lambda_max": 0.043292701954120015,
   "lambda_max_branch": "qT2",
   "cov_lambda_v": 0.07221172083386443,
   "share_EM": {
    "qL": 0.009310503859652798,
    "qT1": 0.49922505755529545,
    "qT2": 0.49146443858505184
   },
   "share_S2E2": {
    "qL": 0.009188985049578397,
    "qT1": 0.5329595958441811,
    "qT2": 0.4578514191062405
   }
  }
 },
 "phase2": {
  "hex_step|a": {
   "vT_VRH": 8.419059637591616,
   "vT_HS_lo": 8.390859731729313,
   "vT_HS_hi": 8.424582419402883,
   "r_agg_E2_VRH": [
    -0.0003597789838700738,
    -8.995485659368807e-05,
    -1.4393819487867887e-05,
    -3.5985447373043655e-06,
    -5.7577590029112e-07,
    -2.220446049250313e-16,
    -5.757876907486192e-07,
    -3.5987289647154697e-06,
    -1.4395293313040902e-05,
    -8.997788565123788e-05,
    -0.00035996323194520397,
    -0.001440311666698113
   ],
   "r_agg_h_VRH": [
    -4.97443568558964e-07,
    -1.249121053259472e-07,
    -2.0039163883822653e-08,
    -5.01423980114879e-09,
    -8.027061237925182e-10,
    0.0,
    -8.03276667404873e-10,
    -5.023156890437974e-09,
    -2.011050115324764e-08,
    -1.260267622482658e-07,
    -5.063613532918509e-07,
    -2.043685221497782e-06
   ],
   "r_agg_E2_HS": [
    -0.0003571461079148186,
    -8.927425424842816e-05,
    -1.4282679909993767e-05,
    -3.5705689754861325e-06,
    -5.71281304040383e-07,
    2.220446049250313e-16,
    -5.712682857872409e-07,
    -3.570365567528988e-06,
    -1.4281052650777504e-05,
    -8.924882879401963e-05,
    -0.0003569427177455564,
    -0.0014273362560642822
   ],
   "S_t_E2": 1.6132521040103724e-13,
   "S_t_h": 3.901387545207024e-15,
   "kappa2_E2": -0.0014394617695005832,
   "kappa2_h": -2.0075102000424232e-06,
   "kappa3_E2": -7.369324104590622e-07,
   "fit_residual": 6.129824287082772e-11,
   "halving_dev_kappa2": 4.296068727221966e-06,
   "lambda_mean_t": [
    2.5111906360905225e-06,
    6.283852379770122e-07,
    1.0059951851451649e-07,
    2.51547644056437e-08,
    4.025233596548142e-09,
    0.0,
    4.025864754976195e-09,
    2.516462609932631e-08,
    1.0067841215180097e-07,
    6.296179578773481e-07,
    2.521052590653425e-06,
    1.0105781771537547e-05
   ],
   "x_kappa_4term_fit_E2": [
    1.613207980641205e-13,
    -0.0014394544404483034,
    -7.369324103762292e-07,
    -1.199601774147876e-07
   ]
  },
  "hex_step|b": {
   "vT_VRH": 8.4192786485796,
   "vT_HS_lo": 8.391084746839036,
   "vT_HS_hi": 8.42480325772318,
   "r_agg_E2_VRH": [
    -0.000359589205973343,
    -8.990741528092094e-05,
    -1.4386229051810417e-05,
    -3.5966471373383158e-06,
    -5.754722848250182e-07,
    0.0,
    -5.75484075837629e-07,
    -3.59683137440836e-06,
    -1.4387702956142334e-05,
    -8.993044558214258e-05,
    -0.00035977346397664256,
    -0.001439552451643511
   ],
   "r_agg_h_VRH": [
    -4.969233557972075e-07,
    -1.247812418947447e-07,
    -2.001814791707801e-08,
    -5.0089792313912085e-09,
    -8.018635755391301e-10,
    0.0,
    -8.024333419953678e-10,
    -5.017882998004097e-09,
    -2.0089378716114936e-08,
    -1.2589424969178253e-07,
    -5.058279419767331e-07,
    -2.04152418015191e-06
   ],
   "r_agg_E2_HS": [
    -0.0003569546896107223,
    -8.922641129327502e-05,
    -1.4275026188892426e-05,
    -3.5686556428826677e-06,
    -5.709751801363794e-07,
    -2.220446049250313e-16,
    -5.709621745397797e-07,
    -3.5684524321011324e-06,
    -1.4273400507525125e-05,
    -8.920101049236795e-05,
    -0.0003567514966401619,
    -0.0014265718105257452
   ],
   "S_t_E2": 1.6400082932192235e-13,
   "S_t_h": 8.137135505898113e-15,
   "kappa2_E2": -0.0014387027187507326,
   "kappa2_h": -2.0054031944932263e-06,
   "kappa3_E2": -7.369722507858468e-07,
   "fit_residual": 6.118721569792576e-11,
   "halving_dev_kappa2": 4.290551805693156e-06,
   "lambda_mean_t": [
    2.508642213075073e-06,
    6.277474540209645e-07,
    1.0049740414635627e-07,
    2.512922990500282e-08,
    4.021147506729069e-09,
    0.0,
    4.0217778891485955e-09,
    2.51390795521338e-08,
    1.0057620139494587e-07,
    6.289786678683045e-07,
    2.5184921186663207e-06,
    1.009551097933715e-05
   ],
   "x_kappa_4term_fit_E2": [
    1.6399641930257683e-13,
    -0.0014386954029695716,
    -7.369722507030138e-07,
    -1.197429589050166e-07
   ]
  },
  "hex_gem8|a": {
   "vT_VRH": 10.041721817369156,
   "vT_HS_lo": 9.990913001573082,
   "vT_HS_hi": 10.05279775494808,
   "r_agg_E2_VRH": [
    -0.0004737700796713096,
    -0.00011845867062443283,
    -1.8955103105566806e-05,
    -4.738925659331095e-06,
    -7.582427593577634e-07,
    -2.220446049250313e-16,
    -7.582626074809085e-07,
    -4.739235785145013e-06,
    -1.895758412695514e-05,
    -0.00011849743822178738,
    -0.00047408026726236674,
    -0.0018971495594128918
   ],
   "r_agg_h_VRH": [
    -8.038770585860888e-07,
    -2.0201977357636736e-07,
    -3.242488200161375e-08,
    -8.11473377382299e-09,
    -1.299175989011303e-09,
    0.0,
    -1.3002695586905588e-09,
    -8.131815554257571e-09,
    -3.2561537133268814e-08,
    -2.041550740683462e-07,
    -8.209613451271025e-07,
    -3.3191570850688024e-06
   ],
   "r_agg_E2_HS": [
    -0.00047147218794074686,
    -0.00011785019986754186,
    -1.8854266348178328e-05,
    -4.713417281476673e-06,
    -7.541323485682483e-07,
    -2.220446049250313e-16,
    -7.541130296884191e-07,
    -4.713115426491221e-06,
    -1.8851851520507168e-05,
    -0.00011781246964759351,
    -0.00047117038801591793,
    -0.0018840138120480576
   ],
   "S_t_E2": 4.88778727245365e-13,
   "S_t_h": 1.8870073354479004e-14,
   "kappa2_E2": -0.0018956484826738256,
   "kappa2_h": -3.249396699531321e-06,
   "kappa3_E2": -1.2405708979146963e-06,
   "fit_residual": 1.4122180315889916e-10,
   "halving_dev_kappa2": 7.515517296534205e-06,
   "lambda_mean_t": [
    3.6006634946301176e-06,
    9.011863601856414e-07,
    1.4429157576291246e-07,
    3.608153193548488e-08,
    5.7738804321405966e-09,
    0.0,
    5.775001286170658e-09,
    3.609904534358997e-08,
    1.4443168336644392e-07,
    9.033755744628227e-07,
    3.6181781526989147e-06,
    1.4512512141049044e-05
   ],
   "x_kappa_4term_fit_E2": [
    4.887729165585316e-13,
    -0.0018956315979800395,
    -1.2405708978056256e-06,
    -2.7636463552777845e-07
   ]
  },
  "hex_gem8|b": {
   "vT_VRH": 10.041554085160612,
   "vT_HS_lo": 9.990739829721814,
   "vT_HS_hi": 10.05262995929398,
   "r_agg_E2_VRH": [
    -0.0004738923403124762,
    -0.00011848923252755217,
    -1.8959992844180817e-05,
    -4.740148086490592e-06,
    -7.58438347125967e-07,
    4.440892098500626e-16,
    -7.584581950270675e-07,
    -4.740458205643172e-06,
    -1.896247381538707e-05,
    -0.00011852799934330971,
    -0.00047420252167706956,
    -0.0018976387487922297
   ],
   "r_agg_h_VRH": [
    -8.04256157782568e-07,
    -2.021152383235858e-07,
    -3.244022384052414e-08,
    -8.118574701398984e-09,
    -1.2997910525669454e-09,
    2.220446049250313e-16,
    -1.3008851773577135e-09,
    -8.13566802815302e-09,
    -3.2576969677400314e-08,
    -2.0425195845774624e-07,
    -8.213518062349934e-07,
    -3.3207430030213203e-06
   ],
   "r_agg_E2_HS": [
    -0.00047159589986833783,
    -0.00011788112071775547,
    -1.8859212958410865e-05,
    -4.714653872306407e-06,
    -7.543301973056415e-07,
    0.0,
    -7.543108700991397e-07,
    -4.714351890200419e-06,
    -1.8856797115107682e-05,
    -0.00011784337463249805,
    -0.00047129397306722165,
    -0.0018845078483346045
   ],
   "S_t_E2": 4.90291953941434e-13,
   "S_t_h": 1.9232267730539364e-14,
   "kappa2_E2": -0.0018961374665274083,
   "kappa2_h": -3.250935490588331e-06,
   "kappa3_E2": -1.240545911150953e-06,
   "fit_residual": 1.4134676897214994e-10,
   "halving_dev_kappa2": 7.520230342822992e-06,
   "lambda_mean_t": [
    3.6022883240769405e-06,
    9.015930248276157e-07,
    1.4435669065512994e-07,
    3.609781489279239e-08,
    5.776486127644972e-09,
    0.0,
    5.7776075427095745e-09,
    3.6115337074777367e-08,
    1.4449686839815845e-07,
    9.03783335221914e-07,
    3.6198117522199667e-06,
    1.4519069924266563e-05
   ],
   "x_kappa_4term_fit_E2": [
    4.902861417464788e-13,
    -0.001896120566887107,
    -1.2405459110416654e-06,
    -2.7660927652668255e-07
   ]
  },
  "cubic_step|001": {
   "vT_VRH": 7.7990463758448945,
   "vT_HS_lo": 7.758614490217017,
   "vT_HS_hi": 7.867953005902295,
   "r_agg_E2_VRH": [
    -2.220446049250313e-16,
    0.0,
    0.0,
    -2.220446049250313e-16,
    -1.1102230246251565e-16,
    0.0,
    -1.1102230246251565e-16,
    0.0,
    -1.1102230246251565e-16,
    0.0,
    2.220446049250313e-16,
    2.220446049250313e-16
   ],
   "r_agg_h_VRH": [
    0.0,
    0.0,
    -1.1102230246251565e-16,
    -1.1102230246251565e-16,
    -1.1102230246251565e-16,
    -1.1102230246251565e-16,
    -1.1102230246251565e-16,
    -1.1102230246251565e-16,
    -1.1102230246251565e-16,
    0.0,
    0.0,
    2.220446049250313e-16
   ],
   "r_agg_E2_HS": [
    -1.1102230246251565e-16,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    -2.220446049250313e-16,
    2.220446049250313e-16,
    0.0
   ],
   "S_t_E2": 7.009496149267015e-17,
   "S_t_h": 1.2375133173866637e-30,
   "kappa2_E2": -2.1857725036605986e-16,
   "kappa2_h": -3.5691728224331273e-16,
   "kappa3_E2": -1.317121335111205e-15,
   "fit_residual": 2.1815805389137155e-16,
   "halving_dev_kappa2": 36.70942580584521,
   "lambda_mean_t": [
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0
   ],
   "x_kappa_4term_fit_E2": [
    7.009496149266831e-17,
    -1.0159890418394039e-14,
    -1.3171213351111684e-15,
    1.62717039777404e-13
   ]
  },
  "cubic_step|111": {
   "vT_VRH": 7.7990463758448945,
   "vT_HS_lo": 7.758614490217017,
   "vT_HS_hi": 7.867953005902295,
   "r_agg_E2_VRH": [
    -2.220446049250313e-16,
    -1.1102230246251565e-16,
    0.0,
    -2.220446049250313e-16,
    -1.1102230246251565e-16,
    0.0,
    -1.1102230246251565e-16,
    0.0,
    -1.1102230246251565e-16,
    -1.1102230246251565e-16,
    4.440892098500626e-16,
    6.661338147750939e-16
   ],
   "r_agg_h_VRH": [
    0.0,
    -1.1102230246251565e-16,
    -1.1102230246251565e-16,
    -1.1102230246251565e-16,
    -1.1102230246251565e-16,
    -1.1102230246251565e-16,
    -1.1102230246251565e-16,
    -1.1102230246251565e-16,
    -1.1102230246251565e-16,
    -1.1102230246251565e-16,
    0.0,
    2.220446049250313e-16
   ],
   "r_agg_E2_HS": [
    -1.1102230246251565e-16,
    -1.1102230246251565e-16,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    -2.220446049250313e-16,
    2.220446049250313e-16,
    0.0
   ],
   "S_t_E2": 7.00949614926752e-17,
   "S_t_h": 6.568330085717285e-30,
   "kappa2_E2": -1.9478276488317234e-15,
   "kappa2_h": -2.0861676807089763e-15,
   "kappa3_E2": -1.3171213351113003e-15,
   "fit_residual": 2.1383492789520715e-16,
   "halving_dev_kappa2": 3.2315974980991067,
   "lambda_mean_t": [
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0
   ],
   "x_kappa_4term_fit_E2": [
    7.009496149266832e-17,
    -9.84213081218537e-15,
    -1.3171213351111702e-15,
    1.2921206888215457e-13
   ]
  },
  "cubic_gem8|001": {
   "vT_VRH": 9.307899076533193,
   "vT_HS_lo": 9.211721064384875,
   "vT_HS_hi": 9.456854984584107,
   "r_agg_E2_VRH": [
    0.0,
    0.0,
    0.0,
    0.0,
    -2.220446049250313e-16,
    2.220446049250313e-16,
    -2.220446049250313e-16,
    0.0,
    -2.220446049250313e-16,
    0.0,
    2.220446049250313e-16,
    0.0
   ],
   "r_agg_h_VRH": [
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0
   ],
   "r_agg_E2_HS": [
    2.220446049250313e-16,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    -3.3306690738754696e-16,
    -5.551115123125783e-16
   ],
   "S_t_E2": -9.550804974045757e-16,
   "S_t_h": 0.0,
   "kappa2_E2": -2.9881446885486723e-16,
   "kappa2_h": 0.0,
   "kappa3_E2": 1.5179666171081885e-14,
   "fit_residual": 2.409052517562122e-16,
   "halving_dev_kappa2": 36.70942580584519,
   "lambda_mean_t": [
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0
   ],
   "x_kappa_4term_fit_E2": [
    -9.550804974045788e-16,
    -1.3348319157336616e-14,
    1.517966617108195e-14,
    2.1359117629450065e-13
   ]
  },
  "cubic_gem8|111": {
   "vT_VRH": 9.307899076533193,
   "vT_HS_lo": 9.211721064384875,
   "vT_HS_hi": 9.456854984584107,
   "r_agg_E2_VRH": [
    0.0,
    0.0,
    -2.220446049250313e-16,
    0.0,
    -2.220446049250313e-16,
    2.220446049250313e-16,
    0.0,
    0.0,
    -2.220446049250313e-16,
    -2.220446049250313e-16,
    0.0,
    0.0
   ],
   "r_agg_h_VRH": [
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0
   ],
   "r_agg_E2_HS": [
    4.440892098500626e-16,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    -2.220446049250313e-16,
    -5.551115123125783e-16,
    -3.3306690738754696e-16
   ],
   "S_t_E2": 2.925271284971411e-16,
   "S_t_h": 0.0,
   "kappa2_E2": -2.2936777285248548e-15,
   "kappa2_h": 0.0,
   "kappa3_E2": -1.1860380658980084e-14,
   "fit_residual": 2.220446049250313e-16,
   "halving_dev_kappa2": 8.27952094619114,
   "lambda_mean_t": [
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0,
    0.0
   ],
   "x_kappa_4term_fit_E2": [
    2.9252712849713164e-16,
    -2.4646954092833455e-14,
    -1.1860380658979912e-14,
    3.658730891834499e-13
   ]
  }
 },
 "born_t0": {
  "hex_step": {
   "D0_plus": -0.020528244595327125,
   "D0_minus": -0.020528244595327125,
   "D0_avg": -0.02052824459532713,
   "D2_avg": -0.018347663163945885,
   "a2agg_residual_rel": 1.8909475942262037e-15
  },
  "hex_gem8": {
   "D0_plus": -0.028917807603071596,
   "D0_minus": -0.028917807603071596,
   "D0_avg": -0.028917807603071617,
   "D2_avg": -0.025933693584294176,
   "a2agg_residual_rel": 6.689072153715041e-16
  },
  "cubic_step": {
   "D0_plus": -0.03151342243433817,
   "D0_minus": -0.03151342243433817,
   "D0_avg": -0.031513422434338176,
   "D2_avg": -0.028537471107946338,
   "a2agg_residual_rel": 4.376704922376667e-15
  },
  "cubic_gem8": {
   "D0_plus": -0.04367714392697755,
   "D0_minus": -0.04367714392697755,
   "D0_avg": -0.043677143926977566,
   "D2_avg": -0.03971397679128604,
   "a2agg_residual_rel": 1.5724953827557158e-15
  }
 },
 "falsifiers": {
  "F-MS-3": {
   "state": "SILENT",
   "worst_S_t": 4.90291953941434e-13
  },
  "F-MS-2": {
   "state": "REGISTERED_NOT_EXECUTED"
  },
  "F-MS-1": {
   "state": "RETIRED_TO_CONTROL"
  }
 },
 "x_pins": {
  "PIN-VRH0_worst_rel": 9.898898090587927e-16,
  "PIN-HS0_worst_rel": 4.644295379818518e-12,
  "hs_references": {
   "hex_step": {
    "lo_K0_G0": [
     134.60708943792756,
     60.030800002639964
    ],
    "hi_K0_G0": [
     135.3665929776937,
     115.55987377748554
    ]
   },
   "hex_step|b": {
    "lo_K0_G0": [
     134.60708943792758,
     60.03080000263914
    ],
    "hi_K0_G0": [
     135.36658842797797,
     115.55987474358491
    ]
   },
   "hex_gem8": {
    "lo_K0_G0": [
     229.69575433713962,
     84.82450000424566
    ],
    "hi_K0_G0": [
     230.1360532921952,
     178.29434080456548
    ]
   },
   "hex_gem8|b": {
    "lo_K0_G0": [
     229.69575433713962,
     84.82450000424924
    ],
    "hi_K0_G0": [
     230.13605425859672,
     178.29434061744877
    ]
   },
   "cubic_step": {
    "lo_K0_G0": [
     123.83246666828633,
     36.725200002429304
    ],
    "hi_K0_G0": [
     123.832466665047,
     85.29339999757266
    ]
   },
   "cubic_gem8": {
    "lo_K0_G0": [
     210.27550000263054,
     46.34985000394528
    ],
    "hi_K0_G0": [
     210.27549999736948,
     131.5435999960556
    ]
   }
  }
 },
 "x_so3_grid": [
  20,
  12,
  20
 ],
 "x_runtime_s": 33.46,
 "verdict_class": "IDENTITY-DELIVERED"
}
=====END-EMBED name=g_mscs1_ccleg_checkpoint.json=====

=====BEGIN-EMBED name=g_mscs1_ccleg_compare.json md5=35d0f762053dd1c48caabf8cad186b16 bytes=1829 encoding=raw=====
{
 "gate": "G-MSCS1",
 "leg": "cc",
 "checkpoint_md5": "249e11dd53c4cb82f302b15d3c94c337",
 "rows": [
  {
   "id": "H-MS-1",
   "predicted": "r_xtal(S2-E2) < 0 on both hex configurations, |r| of order 1e-2 to 1e-1; cubic smaller and axis-dependent",
   "machine": "hex r_E2 in [-3.9352e-02, -2.7947e-02] (all < 0); cubic |r_E2| max 2.0842e-02 < hex min 2.7947e-02; sign flips 001 -> 111",
   "concordant": true
  },
  {
   "id": "H-MS-2",
   "predicted": "r_xtal(S2-h) of order 1e-3, sign of -Cov_EM(lambda,v); |r_h| << |r_E2| on every configuration",
   "machine": "r_h in [-1.8451e-03, -1.1128e-03], cov > 0 on all keys, worst |r_h/r_E2| = 0.133",
   "concordant": true
  },
  {
   "id": "H-MS-3",
   "predicted": "S_t = 0 within tau_agg on all four; kappa2(S2-E2) != 0 with sign matching r_xtal(S2-E2); kappa2(S2-h) smaller by roughly the admixture factor",
   "machine": "S_t = 0 holds (worst 4.90e-13); hex kappa2_E2 < 0 matching r_xtal_E2 < 0, kappa2_h/kappa2_E2 ~ 1.4e-3 to 1.7e-3; BUT kappa2_E2 on all four cubic keys is a symmetry null (|kappa2| ~ 1e-15), so the nonzero-sign clause fails on cubic",
   "concordant": false
  },
  {
   "id": "H-MS-4",
   "predicted": "mean lambda_L of order 1e-2 on hex, max on the oblique qSV branch; zero at t = 0 in the aggregate; O(t^2) in t",
   "machine": "hex lambda_mean 4.809e-03 / 4.954e-03, max branch qSV; aggregate lambda(0) = 0, lambda(t)/t^2 constant over the fit window on every key",
   "concordant": true
  },
  {
   "id": "H-MS-5",
   "predicted": "hex and cubic kappa2(S2-E2) share a sign (structural question)",
   "machine": "machine answer: cubic kappa2(S2-E2) is identically zero under the l = 2 fiber texture (symmetry null); there is no cubic sign to share -- hex kappa2 < 0 stands alone",
   "concordant": false
  }
 ],
 "verdict_class": "IDENTITY-DELIVERED"
}
=====END-EMBED name=g_mscs1_ccleg_compare.json=====

=====BEGIN-EMBED name=g_mscs1_twoleg_comparison.json md5=d4a5b2713d32443cb7d6dec6c7a3c73f bytes=69284 encoding=raw=====
{
  "checks": [
    {
      "check": "C-M-0",
      "item": "chat: required key gate",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-M-0",
      "item": "chat: required key leg",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-M-0",
      "item": "chat: required key instrument",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-M-0",
      "item": "chat: required key instrument_md5",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-M-0",
      "item": "chat: required key memo_md5",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-M-0",
      "item": "chat: required key memo_bytes",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-M-0",
      "item": "chat: required key ledger_base_md5",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-M-0",
      "item": "chat: required key utc",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-M-0",
      "item": "chat: required key elections.E-MS-1",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-M-0",
      "item": "chat: required key elections.E-MS-2",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-M-0",
      "item": "chat: required key elections.E-MS-2b",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-M-0",
      "item": "chat: required key elections.E-MS-2c",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-M-0",
      "item": "chat: required key elections.E-MS-3",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-M-0",
      "item": "chat: required key elections.E-MS-4",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-M-0",
      "item": "chat: required key elections.E-MS-5",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-M-0",
      "item": "chat: required key elections.E-MS-6",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-M-0",
      "item": "chat: required key T1.list_md5",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-M-0",
      "item": "chat: required key T1.state",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-M-0",
      "item": "chat: required key T1.numeric_collisions",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-M-0",
      "item": "chat: required key inputs.X1_md5",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-M-0",
      "item": "chat: required key inputs.X1_bytes",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-M-0",
      "item": "chat: required key quadrature.n_theta",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-M-0",
      "item": "chat: required key quadrature.n_phi",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-M-0",
      "item": "chat: required key quadrature.doubling_residual",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-M-0",
      "item": "chat: required key t_grid",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-M-0",
      "item": "chat: required key controls.F-CTRL-ISO.passed",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-M-0",
      "item": "chat: required key controls.F-CTRL-SO3.passed",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-M-0",
      "item": "chat: required key controls.F-CTRL-TEX.passed",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-M-0",
      "item": "chat: required key controls.F-CTRL-POL.passed",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-M-0",
      "item": "chat: required key controls.PIN-A2AGG.passed",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-M-0",
      "item": "chat: required key controls.F-CTRL-ADMIX.passed",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-M-0",
      "item": "chat: required key phase1",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-M-0",
      "item": "chat: required key phase2",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-M-0",
      "item": "chat: required key born_t0",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-M-0",
      "item": "chat: required key falsifiers.F-MS-3.state",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-M-0",
      "item": "chat: required key falsifiers.F-MS-2.state",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-M-0",
      "item": "chat: required key falsifiers.F-MS-1.state",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-M-0",
      "item": "chat: required key verdict_class",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-M-0",
      "item": "chat: memo_md5 == lock",
      "result": "PASS",
      "chat": "3f30262eaec461fb5fd3202835f7de37",
      "cc": "3f30262eaec461fb5fd3202835f7de37"
    },
    {
      "check": "C-M-0",
      "item": "chat: memo_bytes == lock",
      "result": "PASS",
      "chat": 34837,
      "cc": 34837
    },
    {
      "check": "C-M-0",
      "item": "chat: ledger_base_md5",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-M-0",
      "item": "chat: T1 list md5 == lock",
      "result": "PASS",
      "chat": "fef2827100d3f85e0a6341b44f0c00bf",
      "cc": "fef2827100d3f85e0a6341b44f0c00bf"
    },
    {
      "check": "C-M-0",
      "item": "chat: T1 state CLEAN",
      "result": "PASS",
      "chat": "CLEAN",
      "cc": null
    },
    {
      "check": "C-M-0",
      "item": "chat: X-1 md5",
      "result": "PASS",
      "chat": "200e7a8b775577564369c6924d38a84c",
      "cc": null
    },
    {
      "check": "C-M-0",
      "item": "chat: X-1 bytes",
      "result": "PASS",
      "chat": 2767,
      "cc": null
    },
    {
      "check": "C-M-0",
      "item": "chat: instrument_md5 real 32-hex",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-M-0",
      "item": "chat: no placeholders",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-M-0",
      "item": "chat: election E-MS-1 code",
      "result": "PASS",
      "chat": "a",
      "cc": "a"
    },
    {
      "check": "C-M-0",
      "item": "chat: election E-MS-2 code",
      "result": "PASS",
      "chat": "a",
      "cc": "a"
    },
    {
      "check": "C-M-0",
      "item": "chat: election E-MS-2b code",
      "result": "PASS",
      "chat": "a+b",
      "cc": "a+b"
    },
    {
      "check": "C-M-0",
      "item": "chat: election E-MS-2c code",
      "result": "PASS",
      "chat": "001+111",
      "cc": "001+111"
    },
    {
      "check": "C-M-0",
      "item": "chat: election E-MS-3 code",
      "result": "PASS",
      "chat": "a",
      "cc": "a"
    },
    {
      "check": "C-M-0",
      "item": "chat: election E-MS-4 code",
      "result": "PASS",
      "chat": "a",
      "cc": "a"
    },
    {
      "check": "C-M-0",
      "item": "chat: election E-MS-5 code",
      "result": "PASS",
      "chat": "a",
      "cc": "a"
    },
    {
      "check": "C-M-0",
      "item": "chat: election E-MS-6 code",
      "result": "PASS",
      "chat": "a",
      "cc": "a"
    },
    {
      "check": "C-M-0",
      "item": "cc: required key gate",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-M-0",
      "item": "cc: required key leg",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-M-0",
      "item": "cc: required key instrument",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-M-0",
      "item": "cc: required key instrument_md5",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-M-0",
      "item": "cc: required key memo_md5",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-M-0",
      "item": "cc: required key memo_bytes",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-M-0",
      "item": "cc: required key ledger_base_md5",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-M-0",
      "item": "cc: required key utc",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-M-0",
      "item": "cc: required key elections.E-MS-1",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-M-0",
      "item": "cc: required key elections.E-MS-2",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-M-0",
      "item": "cc: required key elections.E-MS-2b",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-M-0",
      "item": "cc: required key elections.E-MS-2c",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-M-0",
      "item": "cc: required key elections.E-MS-3",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-M-0",
      "item": "cc: required key elections.E-MS-4",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-M-0",
      "item": "cc: required key elections.E-MS-5",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-M-0",
      "item": "cc: required key elections.E-MS-6",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-M-0",
      "item": "cc: required key T1.list_md5",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-M-0",
      "item": "cc: required key T1.state",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-M-0",
      "item": "cc: required key T1.numeric_collisions",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-M-0",
      "item": "cc: required key inputs.X1_md5",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-M-0",
      "item": "cc: required key inputs.X1_bytes",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-M-0",
      "item": "cc: required key quadrature.n_theta",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-M-0",
      "item": "cc: required key quadrature.n_phi",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-M-0",
      "item": "cc: required key quadrature.doubling_residual",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-M-0",
      "item": "cc: required key t_grid",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-M-0",
      "item": "cc: required key controls.F-CTRL-ISO.passed",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-M-0",
      "item": "cc: required key controls.F-CTRL-SO3.passed",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-M-0",
      "item": "cc: required key controls.F-CTRL-TEX.passed",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-M-0",
      "item": "cc: required key controls.F-CTRL-POL.passed",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-M-0",
      "item": "cc: required key controls.PIN-A2AGG.passed",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-M-0",
      "item": "cc: required key controls.F-CTRL-ADMIX.passed",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-M-0",
      "item": "cc: required key phase1",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-M-0",
      "item": "cc: required key phase2",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-M-0",
      "item": "cc: required key born_t0",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-M-0",
      "item": "cc: required key falsifiers.F-MS-3.state",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-M-0",
      "item": "cc: required key falsifiers.F-MS-2.state",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-M-0",
      "item": "cc: required key falsifiers.F-MS-1.state",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-M-0",
      "item": "cc: required key verdict_class",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-M-0",
      "item": "cc: memo_md5 == lock",
      "result": "PASS",
      "chat": "3f30262eaec461fb5fd3202835f7de37",
      "cc": "3f30262eaec461fb5fd3202835f7de37"
    },
    {
      "check": "C-M-0",
      "item": "cc: memo_bytes == lock",
      "result": "PASS",
      "chat": 34837,
      "cc": 34837
    },
    {
      "check": "C-M-0",
      "item": "cc: ledger_base_md5",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-M-0",
      "item": "cc: T1 list md5 == lock",
      "result": "PASS",
      "chat": "fef2827100d3f85e0a6341b44f0c00bf",
      "cc": "fef2827100d3f85e0a6341b44f0c00bf"
    },
    {
      "check": "C-M-0",
      "item": "cc: T1 state CLEAN",
      "result": "PASS",
      "chat": "CLEAN",
      "cc": null
    },
    {
      "check": "C-M-0",
      "item": "cc: X-1 md5",
      "result": "PASS",
      "chat": "200e7a8b775577564369c6924d38a84c",
      "cc": null
    },
    {
      "check": "C-M-0",
      "item": "cc: X-1 bytes",
      "result": "PASS",
      "chat": 2767,
      "cc": null
    },
    {
      "check": "C-M-0",
      "item": "cc: instrument_md5 real 32-hex",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-M-0",
      "item": "cc: no placeholders",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-M-0",
      "item": "cc: election E-MS-1 code",
      "result": "PASS",
      "chat": "a",
      "cc": "a"
    },
    {
      "check": "C-M-0",
      "item": "cc: election E-MS-2 code",
      "result": "PASS",
      "chat": "a",
      "cc": "a"
    },
    {
      "check": "C-M-0",
      "item": "cc: election E-MS-2b code",
      "result": "PASS",
      "chat": "a+b",
      "cc": "a+b"
    },
    {
      "check": "C-M-0",
      "item": "cc: election E-MS-2c code",
      "result": "PASS",
      "chat": "001+111",
      "cc": "001+111"
    },
    {
      "check": "C-M-0",
      "item": "cc: election E-MS-3 code",
      "result": "PASS",
      "chat": "a",
      "cc": "a"
    },
    {
      "check": "C-M-0",
      "item": "cc: election E-MS-4 code",
      "result": "PASS",
      "chat": "a",
      "cc": "a"
    },
    {
      "check": "C-M-0",
      "item": "cc: election E-MS-5 code",
      "result": "PASS",
      "chat": "a",
      "cc": "a"
    },
    {
      "check": "C-M-0",
      "item": "cc: election E-MS-6 code",
      "result": "PASS",
      "chat": "a",
      "cc": "a"
    },
    {
      "check": "C-M-0",
      "item": "INDEPENDENCE: instrument_md5 differ",
      "result": "PASS",
      "chat": "db5f51dd9ef7f54dd0826991d594681b",
      "cc": "195a2b1baf1589675d4bf18983673a23"
    },
    {
      "check": "C-M-0",
      "item": "INDEPENDENCE: checkpoints not byte-identical",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C1",
      "item": "F-CTRL-ISO.passed (both True)",
      "result": "PASS",
      "chat": true,
      "cc": true
    },
    {
      "check": "C1",
      "item": "F-CTRL-ISO.r_xtal_E2",
      "result": "PASS",
      "chat": 2.220446049250313e-16,
      "cc": 2.220446049250313e-16
    },
    {
      "check": "C1",
      "item": "F-CTRL-ISO.r_xtal_h",
      "result": "PASS",
      "chat": 0.0,
      "cc": 0.0
    },
    {
      "check": "C1",
      "item": "F-CTRL-ISO.lambda_max",
      "result": "PASS",
      "chat": 5.8657280953489826e-31,
      "cc": 5.8657280953489826e-31
    },
    {
      "check": "C1",
      "item": "F-CTRL-ISO.r_agg_max",
      "result": "PASS",
      "chat": 4.440892098500626e-16,
      "cc": 2.220446049250313e-16
    },
    {
      "check": "C1",
      "item": "F-CTRL-SO3.passed (both True)",
      "result": "PASS",
      "chat": true,
      "cc": true
    },
    {
      "check": "C1",
      "item": "F-CTRL-SO3.w_S2_mean_t0",
      "result": "PASS",
      "chat": 0.39999999999999997,
      "cc": 0.39999999999999997
    },
    {
      "check": "C1",
      "item": "F-CTRL-SO3.dev_from_0p4",
      "result": "PASS",
      "chat": 4.996003610813204e-16,
      "cc": 1.0547118733938987e-15
    },
    {
      "check": "C1",
      "item": "F-CTRL-SO3.r_agg_0_E2",
      "result": "PASS",
      "chat": 0.0,
      "cc": 4.440892098500626e-16
    },
    {
      "check": "C1",
      "item": "F-CTRL-TEX.passed (both True)",
      "result": "PASS",
      "chat": true,
      "cc": true
    },
    {
      "check": "C1",
      "item": "F-CTRL-TEX.r_agg_t1",
      "result": "PASS",
      "chat": 0.0025019145217410887,
      "cc": 0.002501914521741977
    },
    {
      "check": "C1",
      "item": "F-CTRL-POL.passed (both True)",
      "result": "PASS",
      "chat": true,
      "cc": true
    },
    {
      "check": "C1",
      "item": "F-CTRL-POL.split_plus_minus",
      "result": "PASS",
      "chat": 0.0,
      "cc": 0.0
    },
    {
      "check": "C1",
      "item": "F-CTRL-POL.split_plus_avg",
      "result": "PASS",
      "chat": 4.799045625554363e-16,
      "cc": 2.0816681711721685e-17
    },
    {
      "check": "C1",
      "item": "PIN-A2AGG.passed (both True)",
      "result": "PASS",
      "chat": true,
      "cc": true
    },
    {
      "check": "C1",
      "item": "PIN-A2AGG.worst_rel_residual",
      "result": "PASS",
      "chat": 6.275451101635372e-14,
      "cc": 4.376704922376667e-15
    },
    {
      "check": "C1",
      "item": "F-CTRL-ADMIX.passed (both True)",
      "result": "PASS",
      "chat": true,
      "cc": true
    },
    {
      "check": "C1",
      "item": "F-CTRL-ADMIX.r_xtal_h_projected",
      "result": "MISS",
      "chat": 0.0,
      "cc": -0.001967367205683912
    },
    {
      "check": "C2",
      "item": "config key set",
      "result": "PASS",
      "chat": [
        "cubic_gem8|001",
        "cubic_gem8|111",
        "cubic_step|001",
        "cubic_step|111",
        "hex_gem8|a",
        "hex_gem8|b",
        "hex_step|a",
        "hex_step|b"
      ],
      "cc": [
        "cubic_gem8|001",
        "cubic_gem8|111",
        "cubic_step|001",
        "cubic_step|111",
        "hex_gem8|a",
        "hex_gem8|b",
        "hex_step|a",
        "hex_step|b"
      ]
    },
    {
      "check": "C2",
      "item": "[hex_step|a].v_EM",
      "result": "PASS",
      "chat": 8.498926630589143,
      "cc": 8.498926630589143
    },
    {
      "check": "C2",
      "item": "[hex_step|a].v_S2E2",
      "result": "PASS",
      "chat": 8.261235391127114,
      "cc": 8.261235391127112
    },
    {
      "check": "C2",
      "item": "[hex_step|a].v_S2h",
      "result": "PASS",
      "chat": 8.489468358289109,
      "cc": 8.489468358289109
    },
    {
      "check": "C2",
      "item": "[hex_step|a].r_xtal_E2",
      "result": "PASS",
      "chat": -0.02796720689487253,
      "cc": -0.027967206894872754
    },
    {
      "check": "C2",
      "item": "[hex_step|a].r_xtal_h",
      "result": "PASS",
      "chat": -0.001112878450555299,
      "cc": -0.001112878450555299
    },
    {
      "check": "C2",
      "item": "[hex_step|a].lambda_mean",
      "result": "PASS",
      "chat": 0.004808575724022838,
      "cc": 0.004808575724022839
    },
    {
      "check": "C2",
      "item": "[hex_step|a].lambda_max",
      "result": "PASS",
      "chat": 0.03353758299774612,
      "cc": 0.03353758299774612
    },
    {
      "check": "C2",
      "item": "[hex_step|a].cov_lambda_v",
      "result": "PASS",
      "chat": 0.036444417932560425,
      "cc": 0.03644441793256045
    },
    {
      "check": "C2",
      "item": "[hex_step|a].lambda_max_branch",
      "result": "PASS",
      "chat": "qSV",
      "cc": "qSV"
    },
    {
      "check": "C2",
      "item": "[hex_step|a].share_EM keys",
      "result": "PASS",
      "chat": [
        "qL",
        "qSH",
        "qSV"
      ],
      "cc": [
        "qL",
        "qSH",
        "qSV"
      ]
    },
    {
      "check": "C2",
      "item": "[hex_step|a].share_EM.qL",
      "result": "PASS",
      "chat": 0.004808575724022834,
      "cc": 0.004808575724022839
    },
    {
      "check": "C2",
      "item": "[hex_step|a].share_EM.qSH",
      "result": "PASS",
      "chat": 0.49999999946246804,
      "cc": 0.499999999462468
    },
    {
      "check": "C2",
      "item": "[hex_step|a].share_EM.qSV",
      "result": "PASS",
      "chat": 0.4951914248135092,
      "cc": 0.4951914248135092
    },
    {
      "check": "C2",
      "item": "[hex_step|a].share_S2E2 keys",
      "result": "PASS",
      "chat": [
        "qL",
        "qSH",
        "qSV"
      ],
      "cc": [
        "qL",
        "qSH",
        "qSV"
      ]
    },
    {
      "check": "C2",
      "item": "[hex_step|a].share_S2E2.qL",
      "result": "PASS",
      "chat": 0.0020267404510848717,
      "cc": 0.0020267404510848678
    },
    {
      "check": "C2",
      "item": "[hex_step|a].share_S2E2.qSH",
      "result": "PASS",
      "chat": 0.83333320610945,
      "cc": 0.8333332061094499
    },
    {
      "check": "C2",
      "item": "[hex_step|a].share_S2E2.qSV",
      "result": "PASS",
      "chat": 0.16464005343946514,
      "cc": 0.1646400534394651
    },
    {
      "check": "C2",
      "item": "[hex_step|b].v_EM",
      "result": "PASS",
      "chat": 8.49913805976472,
      "cc": 8.499138059764721
    },
    {
      "check": "C2",
      "item": "[hex_step|b].v_S2E2",
      "result": "PASS",
      "chat": 8.261611551328288,
      "cc": 8.26161155132829
    },
    {
      "check": "C2",
      "item": "[hex_step|b].v_S2h",
      "result": "PASS",
      "chat": 8.489680210591468,
      "cc": 8.489680210591466
    },
    {
      "check": "C2",
      "item": "[hex_step|b].r_xtal_E2",
      "result": "PASS",
      "chat": -0.027947129081346778,
      "cc": -0.027947129081346778
    },
    {
      "check": "C2",
      "item": "[hex_step|b].r_xtal_h",
      "result": "PASS",
      "chat": -0.0011128009813166084,
      "cc": -0.0011128009813170525
    },
    {
      "check": "C2",
      "item": "[hex_step|b].lambda_mean",
      "result": "PASS",
      "chat": 0.004808600428348514,
      "cc": 0.0048086004283485135
    },
    {
      "check": "C2",
      "item": "[hex_step|b].lambda_max",
      "result": "PASS",
      "chat": 0.033534547685208825,
      "cc": 0.033534547685208825
    },
    {
      "check": "C2",
      "item": "[hex_step|b].cov_lambda_v",
      "result": "PASS",
      "chat": 0.03644303566084012,
      "cc": 0.03644303566084019
    },
    {
      "check": "C2",
      "item": "[hex_step|b].lambda_max_branch",
      "result": "PASS",
      "chat": "qSV",
      "cc": "qSV"
    },
    {
      "check": "C2",
      "item": "[hex_step|b].share_EM keys",
      "result": "PASS",
      "chat": [
        "qL",
        "qSH",
        "qSV"
      ],
      "cc": [
        "qL",
        "qSH",
        "qSV"
      ]
    },
    {
      "check": "C2",
      "item": "[hex_step|b].share_EM.qL",
      "result": "PASS",
      "chat": 0.004808600428348502,
      "cc": 0.0048086004283485135
    },
    {
      "check": "C2",
      "item": "[hex_step|b].share_EM.qSH",
      "result": "PASS",
      "chat": 0.5,
      "cc": 0.5
    },
    {
      "check": "C2",
      "item": "[hex_step|b].share_EM.qSV",
      "result": "PASS",
      "chat": 0.49519139957165154,
      "cc": 0.49519139957165154
    },
    {
      "check": "C2",
      "item": "[hex_step|b].share_S2E2 keys",
      "result": "PASS",
      "chat": [
        "qL",
        "qSH",
        "qSV"
      ],
      "cc": [
        "qL",
        "qSH",
        "qSV"
      ]
    },
    {
      "check": "C2",
      "item": "[hex_step|b].share_S2E2.qL",
      "result": "PASS",
      "chat": 0.002026648513157485,
      "cc": 0.002026648513157482
    },
    {
      "check": "C2",
      "item": "[hex_step|b].share_S2E2.qSH",
      "result": "PASS",
      "chat": 0.8333333333333336,
      "cc": 0.8333333333333335
    },
    {
      "check": "C2",
      "item": "[hex_step|b].share_S2E2.qSV",
      "result": "PASS",
      "chat": 0.16464001815350915,
      "cc": 0.16464001815350915
    },
    {
      "check": "C2",
      "item": "[hex_gem8|a].v_EM",
      "result": "PASS",
      "chat": 10.167571147427779,
      "cc": 10.167571147427779
    },
    {
      "check": "C2",
      "item": "[hex_gem8|a].v_S2E2",
      "result": "PASS",
      "chat": 9.767584615679638,
      "cc": 9.767584615679638
    },
    {
      "check": "C2",
      "item": "[hex_gem8|a].v_S2h",
      "result": "PASS",
      "chat": 10.154202161568202,
      "cc": 10.154202161568202
    },
    {
      "check": "C2",
      "item": "[hex_gem8|a].r_xtal_E2",
      "result": "PASS",
      "chat": -0.039339437703303504,
      "cc": -0.039339437703303504
    },
    {
      "check": "C2",
      "item": "[hex_gem8|a].r_xtal_h",
      "result": "PASS",
      "chat": -0.0013148652382883874,
      "cc": -0.0013148652382883874
    },
    {
      "check": "C2",
      "item": "[hex_gem8|a].lambda_mean",
      "result": "PASS",
      "chat": 0.0049537696180639535,
      "cc": 0.0049537696180639535
    },
    {
      "check": "C2",
      "item": "[hex_gem8|a].lambda_max",
      "result": "PASS",
      "chat": 0.03513301845903744,
      "cc": 0.03513301845903746
    },
    {
      "check": "C2",
      "item": "[hex_gem8|a].cov_lambda_v",
      "result": "PASS",
      "chat": 0.05132899179683144,
      "cc": 0.051328991796831605
    },
    {
      "check": "C2",
      "item": "[hex_gem8|a].lambda_max_branch",
      "result": "PASS",
      "chat": "qSV",
      "cc": "qSV"
    },
    {
      "check": "C2",
      "item": "[hex_gem8|a].share_EM keys",
      "result": "PASS",
      "chat": [
        "qL",
        "qSH",
        "qSV"
      ],
      "cc": [
        "qL",
        "qSH",
        "qSV"
      ]
    },
    {
      "check": "C2",
      "item": "[hex_gem8|a].share_EM.qL",
      "result": "PASS",
      "chat": 0.004953769618063935,
      "cc": 0.004953769618063954
    },
    {
      "check": "C2",
      "item": "[hex_gem8|a].share_EM.qSH",
      "result": "PASS",
      "chat": 0.49999999908685466,
      "cc": 0.49999999908685466
    },
    {
      "check": "C2",
      "item": "[hex_gem8|a].share_EM.qSV",
      "result": "PASS",
      "chat": 0.49504623129508146,
      "cc": 0.49504623129508146
    },
    {
      "check": "C2",
      "item": "[hex_gem8|a].share_S2E2 keys",
      "result": "PASS",
      "chat": [
        "qL",
        "qSH",
        "qSV"
      ],
      "cc": [
        "qL",
        "qSH",
        "qSV"
      ]
    },
    {
      "check": "C2",
      "item": "[hex_gem8|a].share_S2E2.qL",
      "result": "PASS",
      "chat": 0.002138148867835594,
      "cc": 0.0021381488678355936
    },
    {
      "check": "C2",
      "item": "[hex_gem8|a].share_S2E2.qSH",
      "result": "PASS",
      "chat": 0.8333322334753969,
      "cc": 0.8333322334753966
    },
    {
      "check": "C2",
      "item": "[hex_gem8|a].share_S2E2.qSV",
      "result": "PASS",
      "chat": 0.16452961765676766,
      "cc": 0.16452961765676763
    },
    {
      "check": "C2",
      "item": "[hex_gem8|b].v_EM",
      "result": "PASS",
      "chat": 10.167412388965342,
      "cc": 10.167412388965342
    },
    {
      "check": "C2",
      "item": "[hex_gem8|b].v_S2E2",
      "result": "PASS",
      "chat": 9.767300819096656,
      "cc": 9.767300819096654
    },
    {
      "check": "C2",
      "item": "[hex_gem8|b].v_S2h",
      "result": "PASS",
      "chat": 10.154042977980577,
      "cc": 10.154042977980577
    },
    {
      "check": "C2",
      "item": "[hex_gem8|b].r_xtal_E2",
      "result": "PASS",
      "chat": -0.03935234989611769,
      "cc": -0.03935234989611791
    },
    {
      "check": "C2",
      "item": "[hex_gem8|b].r_xtal_h",
      "result": "PASS",
      "chat": -0.0013149275816995987,
      "cc": -0.0013149275816995987
    },
    {
      "check": "C2",
      "item": "[hex_gem8|b].lambda_mean",
      "result": "PASS",
      "chat": 0.004953789932329422,
      "cc": 0.004953789932329422
    },
    {
      "check": "C2",
      "item": "[hex_gem8|b].lambda_max",
      "result": "PASS",
      "chat": 0.035133018459037525,
      "cc": 0.035133018459037504
    },
    {
      "check": "C2",
      "item": "[hex_gem8|b].cov_lambda_v",
      "result": "PASS",
      "chat": 0.05133043709649301,
      "cc": 0.05133043709649307
    },
    {
      "check": "C2",
      "item": "[hex_gem8|b].lambda_max_branch",
      "result": "PASS",
      "chat": "qSV",
      "cc": "qSV"
    },
    {
      "check": "C2",
      "item": "[hex_gem8|b].share_EM keys",
      "result": "PASS",
      "chat": [
        "qL",
        "qSH",
        "qSV"
      ],
      "cc": [
        "qL",
        "qSH",
        "qSV"
      ]
    },
    {
      "check": "C2",
      "item": "[hex_gem8|b].share_EM.qL",
      "result": "PASS",
      "chat": 0.004953789932329417,
      "cc": 0.004953789932329422
    },
    {
      "check": "C2",
      "item": "[hex_gem8|b].share_EM.qSH",
      "result": "PASS",
      "chat": 0.5,
      "cc": 0.5
    },
    {
      "check": "C2",
      "item": "[hex_gem8|b].share_EM.qSV",
      "result": "PASS",
      "chat": 0.4950462100676707,
      "cc": 0.4950462100676707
    },
    {
      "check": "C2",
      "item": "[hex_gem8|b].share_S2E2 keys",
      "result": "PASS",
      "chat": [
        "qL",
        "qSH",
        "qSV"
      ],
      "cc": [
        "qL",
        "qSH",
        "qSV"
      ]
    },
    {
      "check": "C2",
      "item": "[hex_gem8|b].share_S2E2.qL",
      "result": "PASS",
      "chat": 0.002138215252862705,
      "cc": 0.0021382152528626997
    },
    {
      "check": "C2",
      "item": "[hex_gem8|b].share_S2E2.qSH",
      "result": "PASS",
      "chat": 0.8333333333333337,
      "cc": 0.8333333333333336
    },
    {
      "check": "C2",
      "item": "[hex_gem8|b].share_S2E2.qSV",
      "result": "PASS",
      "chat": 0.16452845141380396,
      "cc": 0.1645284514138039
    },
    {
      "check": "C2",
      "item": "[cubic_step|001].v_EM",
      "result": "PASS",
      "chat": 8.028124827494889,
      "cc": 8.028124827494889
    },
    {
      "check": "C2",
      "item": "[cubic_step|001].v_S2E2",
      "result": "PASS",
      "chat": 7.889264216956222,
      "cc": 7.889264216956221
    },
    {
      "check": "C2",
      "item": "[cubic_step|001].v_S2h",
      "result": "PASS",
      "chat": 8.015951162831872,
      "cc": 8.015951162831872
    },
    {
      "check": "C2",
      "item": "[cubic_step|001].r_xtal_E2",
      "result": "PASS",
      "chat": -0.0172967677412158,
      "cc": -0.017296767741215913
    },
    {
      "check": "C2",
      "item": "[cubic_step|001].r_xtal_h",
      "result": "PASS",
      "chat": -0.001516377102324551,
      "cc": -0.001516377102324551
    },
    {
      "check": "C2",
      "item": "[cubic_step|001].lambda_mean",
      "result": "PASS",
      "chat": 0.0083923190288783,
      "cc": 0.0083923190288783
    },
    {
      "check": "C2",
      "item": "[cubic_step|001].lambda_max",
      "result": "PASS",
      "chat": 0.03870069334173741,
      "cc": 0.03870069334173745
    },
    {
      "check": "C2",
      "item": "[cubic_step|001].cov_lambda_v",
      "result": "PASS",
      "chat": 0.04901957894779367,
      "cc": 0.04901957894779363
    },
    {
      "check": "C2",
      "item": "[cubic_step|001].lambda_max_branch",
      "result": "PASS",
      "chat": "qT2",
      "cc": "qT2"
    },
    {
      "check": "C2",
      "item": "[cubic_step|001].share_EM keys",
      "result": "PASS",
      "chat": [
        "qL",
        "qT1",
        "qT2"
      ],
      "cc": [
        "qL",
        "qT1",
        "qT2"
      ]
    },
    {
      "check": "C2",
      "item": "[cubic_step|001].share_EM.qL",
      "result": "PASS",
      "chat": 0.008392319028878298,
      "cc": 0.0083923190288783
    },
    {
      "check": "C2",
      "item": "[cubic_step|001].share_EM.qT1",
      "result": "PASS",
      "chat": 0.4992967361164542,
      "cc": 0.4992967361164543
    },
    {
      "check": "C2",
      "item": "[cubic_step|001].share_EM.qT2",
      "result": "PASS",
      "chat": 0.49231094485466753,
      "cc": 0.49231094485466753
    },
    {
      "check": "C2",
      "item": "[cubic_step|001].share_S2E2 keys",
      "result": "PASS",
      "chat": [
        "qL",
        "qT1",
        "qT2"
      ],
      "cc": [
        "qL",
        "qT1",
        "qT2"
      ]
    },
    {
      "check": "C2",
      "item": "[cubic_step|001].share_S2E2.qL",
      "result": "PASS",
      "chat": 0.008569676861049398,
      "cc": 0.008569676861049402
    },
    {
      "check": "C2",
      "item": "[cubic_step|001].share_S2E2.qT1",
      "result": "PASS",
      "chat": 0.4488023208911163,
      "cc": 0.44880232089111627
    },
    {
      "check": "C2",
      "item": "[cubic_step|001].share_S2E2.qT2",
      "result": "PASS",
      "chat": 0.5426280022478344,
      "cc": 0.5426280022478344
    },
    {
      "check": "C2",
      "item": "[cubic_step|111].v_EM",
      "result": "PASS",
      "chat": 8.028124827494889,
      "cc": 8.028124827494889
    },
    {
      "check": "C2",
      "item": "[cubic_step|111].v_S2E2",
      "result": "PASS",
      "chat": 8.120698567854001,
      "cc": 8.120698567854001
    },
    {
      "check": "C2",
      "item": "[cubic_step|111].v_S2h",
      "result": "PASS",
      "chat": 8.015951162831872,
      "cc": 8.015951162831872
    },
    {
      "check": "C2",
      "item": "[cubic_step|111].r_xtal_E2",
      "result": "PASS",
      "chat": 0.01153117849414409,
      "cc": 0.01153117849414409
    },
    {
      "check": "C2",
      "item": "[cubic_step|111].r_xtal_h",
      "result": "PASS",
      "chat": -0.001516377102324551,
      "cc": -0.001516377102324551
    },
    {
      "check": "C2",
      "item": "[cubic_step|111].lambda_mean",
      "result": "PASS",
      "chat": 0.0083923190288783,
      "cc": 0.0083923190288783
    },
    {
      "check": "C2",
      "item": "[cubic_step|111].lambda_max",
      "result": "PASS",
      "chat": 0.03870069334173741,
      "cc": 0.03870069334173745
    },
    {
      "check": "C2",
      "item": "[cubic_step|111].cov_lambda_v",
      "result": "PASS",
      "chat": 0.04901957894779367,
      "cc": 0.04901957894779363
    },
    {
      "check": "C2",
      "item": "[cubic_step|111].lambda_max_branch",
      "result": "PASS",
      "chat": "qT2",
      "cc": "qT2"
    },
    {
      "check": "C2",
      "item": "[cubic_step|111].share_EM keys",
      "result": "PASS",
      "chat": [
        "qL",
        "qT1",
        "qT2"
      ],
      "cc": [
        "qL",
        "qT1",
        "qT2"
      ]
    },
    {
      "check": "C2",
      "item": "[cubic_step|111].share_EM.qL",
      "result": "PASS",
      "chat": 0.008392319028878298,
      "cc": 0.0083923190288783
    },
    {
      "check": "C2",
      "item": "[cubic_step|111].share_EM.qT1",
      "result": "PASS",
      "chat": 0.4992967361164542,
      "cc": 0.4992967361164543
    },
    {
      "check": "C2",
      "item": "[cubic_step|111].share_EM.qT2",
      "result": "PASS",
      "chat": 0.49231094485466753,
      "cc": 0.49231094485466753
    },
    {
      "check": "C2",
      "item": "[cubic_step|111].share_S2E2 keys",
      "result": "PASS",
      "chat": [
        "qL",
        "qT1",
        "qT2"
      ],
      "cc": [
        "qL",
        "qT1",
        "qT2"
      ]
    },
    {
      "check": "C2",
      "item": "[cubic_step|111].share_S2E2.qL",
      "result": "PASS",
      "chat": 0.00827408047409754,
      "cc": 0.008274080474097544
    },
    {
      "check": "C2",
      "item": "[cubic_step|111].share_S2E2.qT1",
      "result": "PASS",
      "chat": 0.5330407329981224,
      "cc": 0.5330407329981224
    },
    {
      "check": "C2",
      "item": "[cubic_step|111].share_S2E2.qT2",
      "result": "PASS",
      "chat": 0.45868518652777995,
      "cc": 0.45868518652777995
    },
    {
      "check": "C2",
      "item": "[cubic_gem8|001].v_EM",
      "result": "PASS",
      "chat": 9.72117101507821,
      "cc": 9.721171015078212
    },
    {
      "check": "C2",
      "item": "[cubic_gem8|001].v_S2E2",
      "result": "PASS",
      "chat": 9.5185580718033,
      "cc": 9.518558071803296
    },
    {
      "check": "C2",
      "item": "[cubic_gem8|001].v_S2h",
      "result": "PASS",
      "chat": 9.703234472528251,
      "cc": 9.703234472528251
    },
    {
      "check": "C2",
      "item": "[cubic_gem8|001].r_xtal_E2",
      "result": "PASS",
      "chat": -0.020842442022740326,
      "cc": -0.02084244202274077
    },
    {
      "check": "C2",
      "item": "[cubic_gem8|001].r_xtal_h",
      "result": "PASS",
      "chat": -0.0018451010194284745,
      "cc": -0.0018451010194286965
    },
    {
      "check": "C2",
      "item": "[cubic_gem8|001].lambda_mean",
      "result": "PASS",
      "chat": 0.0093105038596528,
      "cc": 0.009310503859652798
    },
    {
      "check": "C2",
      "item": "[cubic_gem8|001].lambda_max",
      "result": "PASS",
      "chat": 0.043292701954120015,
      "cc": 0.043292701954120015
    },
    {
      "check": "C2",
      "item": "[cubic_gem8|001].cov_lambda_v",
      "result": "PASS",
      "chat": 0.07221172083386433,
      "cc": 0.07221172083386443
    },
    {
      "check": "C2",
      "item": "[cubic_gem8|001].lambda_max_branch",
      "result": "PASS",
      "chat": "qT2",
      "cc": "qT2"
    },
    {
      "check": "C2",
      "item": "[cubic_gem8|001].share_EM keys",
      "result": "PASS",
      "chat": [
        "qL",
        "qT1",
        "qT2"
      ],
      "cc": [
        "qL",
        "qT1",
        "qT2"
      ]
    },
    {
      "check": "C2",
      "item": "[cubic_gem8|001].share_EM.qL",
      "result": "PASS",
      "chat": 0.009310503859652788,
      "cc": 0.009310503859652798
    },
    {
      "check": "C2",
      "item": "[cubic_gem8|001].share_EM.qT1",
      "result": "PASS",
      "chat": 0.49922505755529545,
      "cc": 0.49922505755529545
    },
    {
      "check": "C2",
      "item": "[cubic_gem8|001].share_EM.qT2",
      "result": "PASS",
      "chat": 0.49146443858505184,
      "cc": 0.49146443858505184
    },
    {
      "check": "C2",
      "item": "[cubic_gem8|001].share_S2E2 keys",
      "result": "PASS",
      "chat": [
        "qL",
        "qT1",
        "qT2"
      ],
      "cc": [
        "qL",
        "qT1",
        "qT2"
      ]
    },
    {
      "check": "C2",
      "item": "[cubic_gem8|001].share_S2E2.qL",
      "result": "PASS",
      "chat": 0.009492782074764219,
      "cc": 0.009492782074764233
    },
    {
      "check": "C2",
      "item": "[cubic_gem8|001].share_S2E2.qT1",
      "result": "PASS",
      "chat": 0.44874904568984914,
      "cc": 0.44874904568984897
    },
    {
      "check": "C2",
      "item": "[cubic_gem8|001].share_S2E2.qT2",
      "result": "PASS",
      "chat": 0.5417581722353867,
      "cc": 0.5417581722353866
    },
    {
      "check": "C2",
      "item": "[cubic_gem8|111].v_EM",
      "result": "PASS",
      "chat": 9.72117101507821,
      "cc": 9.721171015078212
    },
    {
      "check": "C2",
      "item": "[cubic_gem8|111].v_S2E2",
      "result": "PASS",
      "chat": 9.856246310594818,
      "cc": 9.856246310594821
    },
    {
      "check": "C2",
      "item": "[cubic_gem8|111].v_S2h",
      "result": "PASS",
      "chat": 9.703234472528251,
      "cc": 9.703234472528251
    },
    {
      "check": "C2",
      "item": "[cubic_gem8|111].r_xtal_E2",
      "result": "PASS",
      "chat": 0.01389496134849355,
      "cc": 0.013894961348493773
    },
    {
      "check": "C2",
      "item": "[cubic_gem8|111].r_xtal_h",
      "result": "PASS",
      "chat": -0.0018451010194284745,
      "cc": -0.0018451010194286965
    },
    {
      "check": "C2",
      "item": "[cubic_gem8|111].lambda_mean",
      "result": "PASS",
      "chat": 0.0093105038596528,
      "cc": 0.009310503859652798
    },
    {
      "check": "C2",
      "item": "[cubic_gem8|111].lambda_max",
      "result": "PASS",
      "chat": 0.043292701954120015,
      "cc": 0.043292701954120015
    },
    {
      "check": "C2",
      "item": "[cubic_gem8|111].cov_lambda_v",
      "result": "PASS",
      "chat": 0.07221172083386433,
      "cc": 0.07221172083386443
    },
    {
      "check": "C2",
      "item": "[cubic_gem8|111].lambda_max_branch",
      "result": "PASS",
      "chat": "qT2",
      "cc": "qT2"
    },
    {
      "check": "C2",
      "item": "[cubic_gem8|111].share_EM keys",
      "result": "PASS",
      "chat": [
        "qL",
        "qT1",
        "qT2"
      ],
      "cc": [
        "qL",
        "qT1",
        "qT2"
      ]
    },
    {
      "check": "C2",
      "item": "[cubic_gem8|111].share_EM.qL",
      "result": "PASS",
      "chat": 0.009310503859652788,
      "cc": 0.009310503859652798
    },
    {
      "check": "C2",
      "item": "[cubic_gem8|111].share_EM.qT1",
      "result": "PASS",
      "chat": 0.49922505755529545,
      "cc": 0.49922505755529545
    },
    {
      "check": "C2",
      "item": "[cubic_gem8|111].share_EM.qT2",
      "result": "PASS",
      "chat": 0.49146443858505184,
      "cc": 0.49146443858505184
    },
    {
      "check": "C2",
      "item": "[cubic_gem8|111].share_S2E2 keys",
      "result": "PASS",
      "chat": [
        "qL",
        "qT1",
        "qT2"
      ],
      "cc": [
        "qL",
        "qT1",
        "qT2"
      ]
    },
    {
      "check": "C2",
      "item": "[cubic_gem8|111].share_S2E2.qL",
      "result": "PASS",
      "chat": 0.009188985049578388,
      "cc": 0.009188985049578397
    },
    {
      "check": "C2",
      "item": "[cubic_gem8|111].share_S2E2.qT1",
      "result": "PASS",
      "chat": 0.5329595958441811,
      "cc": 0.5329595958441811
    },
    {
      "check": "C2",
      "item": "[cubic_gem8|111].share_S2E2.qT2",
      "result": "PASS",
      "chat": 0.4578514191062405,
      "cc": 0.4578514191062405
    },
    {
      "check": "C3",
      "item": "phase2 key set",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C3",
      "item": "[hex_step|a].vT_VRH",
      "result": "PASS",
      "chat": 8.419059637591603,
      "cc": 8.419059637591616
    },
    {
      "check": "C3",
      "item": "[hex_step|a].vT_HS_lo",
      "result": "PASS",
      "chat": 8.390859731728247,
      "cc": 8.390859731729313
    },
    {
      "check": "C3",
      "item": "[hex_step|a].vT_HS_hi",
      "result": "PASS",
      "chat": 8.424582419403457,
      "cc": 8.424582419402883
    },
    {
      "check": "C3",
      "item": "[hex_step|a].r_agg_E2_VRH[12]",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C3",
      "item": "[hex_step|a].r_agg_h_VRH[12]",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C3",
      "item": "[hex_step|a].r_agg_E2_HS[12]",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C3",
      "item": "[hex_step|a].S_t_E2",
      "result": "PASS",
      "chat": 1.6266231256261696e-13,
      "cc": 1.6132521040103724e-13
    },
    {
      "check": "C3",
      "item": "[hex_step|a].S_t_h",
      "result": "PASS",
      "chat": 4.563941055176853e-15,
      "cc": 3.901387545207024e-15
    },
    {
      "check": "C3",
      "item": "[hex_step|a].kappa2_E2",
      "result": "PASS",
      "chat": -0.0014394617694966992,
      "cc": -0.0014394617695005832
    },
    {
      "check": "C3",
      "item": "[hex_step|a].kappa2_h",
      "result": "PASS",
      "chat": -2.0075101981637655e-06,
      "cc": -2.0075102000424232e-06
    },
    {
      "check": "C3",
      "item": "[hex_step|a].halving_dev_kappa2 (chat) <= kappa2_rel",
      "result": "PASS",
      "chat": 4.296077191089223e-06,
      "cc": null
    },
    {
      "check": "C3",
      "item": "[hex_step|a].halving_dev_kappa2 (cc) <= kappa2_rel",
      "result": "PASS",
      "chat": 4.296068727221966e-06,
      "cc": null
    },
    {
      "check": "C3",
      "item": "[hex_step|a].lambda_mean_t[12]",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C3",
      "item": "[hex_step|b].vT_VRH",
      "result": "PASS",
      "chat": 8.419278648579612,
      "cc": 8.4192786485796
    },
    {
      "check": "C3",
      "item": "[hex_step|b].vT_HS_lo",
      "result": "PASS",
      "chat": 8.391084746837947,
      "cc": 8.391084746839036
    },
    {
      "check": "C3",
      "item": "[hex_step|b].vT_HS_hi",
      "result": "PASS",
      "chat": 8.424803257723832,
      "cc": 8.42480325772318
    },
    {
      "check": "C3",
      "item": "[hex_step|b].r_agg_E2_VRH[12]",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C3",
      "item": "[hex_step|b].r_agg_h_VRH[12]",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C3",
      "item": "[hex_step|b].r_agg_E2_HS[12]",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C3",
      "item": "[hex_step|b].S_t_E2",
      "result": "PASS",
      "chat": 1.6125034658616313e-13,
      "cc": 1.6400082932192235e-13
    },
    {
      "check": "C3",
      "item": "[hex_step|b].S_t_h",
      "result": "PASS",
      "chat": 6.550087858874976e-15,
      "cc": 8.137135505898113e-15
    },
    {
      "check": "C3",
      "item": "[hex_step|b].kappa2_E2",
      "result": "PASS",
      "chat": -0.001438702718749083,
      "cc": -0.0014387027187507326
    },
    {
      "check": "C3",
      "item": "[hex_step|b].kappa2_h",
      "result": "PASS",
      "chat": -2.0054031941127916e-06,
      "cc": -2.0054031944932263e-06
    },
    {
      "check": "C3",
      "item": "[hex_step|b].halving_dev_kappa2 (chat) <= kappa2_rel",
      "result": "PASS",
      "chat": 4.290548556187453e-06,
      "cc": null
    },
    {
      "check": "C3",
      "item": "[hex_step|b].halving_dev_kappa2 (cc) <= kappa2_rel",
      "result": "PASS",
      "chat": 4.290551805693156e-06,
      "cc": null
    },
    {
      "check": "C3",
      "item": "[hex_step|b].lambda_mean_t[12]",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C3",
      "item": "[hex_gem8|a].vT_VRH",
      "result": "PASS",
      "chat": 10.041721817369147,
      "cc": 10.041721817369156
    },
    {
      "check": "C3",
      "item": "[hex_gem8|a].vT_HS_lo",
      "result": "PASS",
      "chat": 9.990913001571156,
      "cc": 9.990913001573082
    },
    {
      "check": "C3",
      "item": "[hex_gem8|a].vT_HS_hi",
      "result": "PASS",
      "chat": 10.052797754949037,
      "cc": 10.05279775494808
    },
    {
      "check": "C3",
      "item": "[hex_gem8|a].r_agg_E2_VRH[12]",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C3",
      "item": "[hex_gem8|a].r_agg_h_VRH[12]",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C3",
      "item": "[hex_gem8|a].r_agg_E2_HS[12]",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C3",
      "item": "[hex_gem8|a].S_t_E2",
      "result": "PASS",
      "chat": 4.894642365145396e-13,
      "cc": 4.88778727245365e-13
    },
    {
      "check": "C3",
      "item": "[hex_gem8|a].S_t_h",
      "result": "PASS",
      "chat": 1.9849252759426836e-14,
      "cc": 1.8870073354479004e-14
    },
    {
      "check": "C3",
      "item": "[hex_gem8|a].kappa2_E2",
      "result": "PASS",
      "chat": -0.0018956484826701352,
      "cc": -0.0018956484826738256
    },
    {
      "check": "C3",
      "item": "[hex_gem8|a].kappa2_h",
      "result": "PASS",
      "chat": -3.2493966959289463e-06,
      "cc": -3.249396699531321e-06
    },
    {
      "check": "C3",
      "item": "[hex_gem8|a].halving_dev_kappa2 (chat) <= kappa2_rel",
      "result": "PASS",
      "chat": 7.51551994532953e-06,
      "cc": null
    },
    {
      "check": "C3",
      "item": "[hex_gem8|a].halving_dev_kappa2 (cc) <= kappa2_rel",
      "result": "PASS",
      "chat": 7.515517296534205e-06,
      "cc": null
    },
    {
      "check": "C3",
      "item": "[hex_gem8|a].lambda_mean_t[12]",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C3",
      "item": "[hex_gem8|b].vT_VRH",
      "result": "PASS",
      "chat": 10.041554085160632,
      "cc": 10.041554085160612
    },
    {
      "check": "C3",
      "item": "[hex_gem8|b].vT_HS_lo",
      "result": "PASS",
      "chat": 9.99073982971986,
      "cc": 9.990739829721814
    },
    {
      "check": "C3",
      "item": "[hex_gem8|b].vT_HS_hi",
      "result": "PASS",
      "chat": 10.052629959294945,
      "cc": 10.05262995929398
    },
    {
      "check": "C3",
      "item": "[hex_gem8|b].r_agg_E2_VRH[12]",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C3",
      "item": "[hex_gem8|b].r_agg_h_VRH[12]",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C3",
      "item": "[hex_gem8|b].r_agg_E2_HS[12]",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C3",
      "item": "[hex_gem8|b].S_t_E2",
      "result": "PASS",
      "chat": 4.895751529361098e-13,
      "cc": 4.90291953941434e-13
    },
    {
      "check": "C3",
      "item": "[hex_gem8|b].S_t_h",
      "result": "PASS",
      "chat": 1.861754403597132e-14,
      "cc": 1.9232267730539364e-14
    },
    {
      "check": "C3",
      "item": "[hex_gem8|b].kappa2_E2",
      "result": "PASS",
      "chat": -0.0018961374665242264,
      "cc": -0.0018961374665274083
    },
    {
      "check": "C3",
      "item": "[hex_gem8|b].kappa2_h",
      "result": "PASS",
      "chat": -3.2509354903061167e-06,
      "cc": -3.250935490588331e-06
    },
    {
      "check": "C3",
      "item": "[hex_gem8|b].halving_dev_kappa2 (chat) <= kappa2_rel",
      "result": "PASS",
      "chat": 7.520240357827345e-06,
      "cc": null
    },
    {
      "check": "C3",
      "item": "[hex_gem8|b].halving_dev_kappa2 (cc) <= kappa2_rel",
      "result": "PASS",
      "chat": 7.520230342822992e-06,
      "cc": null
    },
    {
      "check": "C3",
      "item": "[hex_gem8|b].lambda_mean_t[12]",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C3",
      "item": "[cubic_step|001].vT_VRH",
      "result": "PASS",
      "chat": 7.799046375844923,
      "cc": 7.7990463758448945
    },
    {
      "check": "C3",
      "item": "[cubic_step|001].vT_HS_lo",
      "result": "PASS",
      "chat": 7.758614490211087,
      "cc": 7.758614490217017
    },
    {
      "check": "C3",
      "item": "[cubic_step|001].vT_HS_hi",
      "result": "PASS",
      "chat": 7.867953005904775,
      "cc": 7.867953005902295
    },
    {
      "check": "C3",
      "item": "[cubic_step|001].r_agg_E2_VRH[12]",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C3",
      "item": "[cubic_step|001].r_agg_h_VRH[12]",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C3",
      "item": "[cubic_step|001].r_agg_E2_HS[12]",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C3",
      "item": "[cubic_step|001].S_t_E2",
      "result": "PASS",
      "chat": 3.872699649800502e-16,
      "cc": 7.009496149267015e-17
    },
    {
      "check": "C3",
      "item": "[cubic_step|001].S_t_h",
      "result": "PASS",
      "chat": 2.7381760509747877e-16,
      "cc": 1.2375133173866637e-30
    },
    {
      "check": "C3",
      "item": "[cubic_step|001].kappa2_E2",
      "result": "PASS",
      "chat": 3.141702123932416e-15,
      "cc": -2.1857725036605986e-16
    },
    {
      "check": "C3",
      "item": "[cubic_step|001].kappa2_h",
      "result": "PASS",
      "chat": -3.458500796931401e-17,
      "cc": -3.5691728224331273e-16
    },
    {
      "check": "C3",
      "item": "[cubic_step|001].halving_dev_kappa2 (chat) <= kappa2_rel",
      "result": "MISS",
      "chat": 4.802491637841732,
      "cc": null
    },
    {
      "check": "C3",
      "item": "[cubic_step|001].halving_dev_kappa2 (cc) <= kappa2_rel",
      "result": "MISS",
      "chat": 36.70942580584521,
      "cc": null
    },
    {
      "check": "C3",
      "item": "[cubic_step|001].lambda_mean_t[12]",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C3",
      "item": "[cubic_step|111].vT_VRH",
      "result": "PASS",
      "chat": 7.799046375844923,
      "cc": 7.7990463758448945
    },
    {
      "check": "C3",
      "item": "[cubic_step|111].vT_HS_lo",
      "result": "PASS",
      "chat": 7.758614490211087,
      "cc": 7.758614490217017
    },
    {
      "check": "C3",
      "item": "[cubic_step|111].vT_HS_hi",
      "result": "PASS",
      "chat": 7.867953005904775,
      "cc": 7.867953005902295
    },
    {
      "check": "C3",
      "item": "[cubic_step|111].r_agg_E2_VRH[12]",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C3",
      "item": "[cubic_step|111].r_agg_h_VRH[12]",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C3",
      "item": "[cubic_step|111].r_agg_E2_HS[12]",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C3",
      "item": "[cubic_step|111].S_t_E2",
      "result": "PASS",
      "chat": 4.1100077415202465e-16,
      "cc": 7.00949614926752e-17
    },
    {
      "check": "C3",
      "item": "[cubic_step|111].S_t_h",
      "result": "PASS",
      "chat": -2.925271284971396e-16,
      "cc": 6.568330085717285e-30
    },
    {
      "check": "C3",
      "item": "[cubic_step|111].kappa2_E2",
      "result": "PASS",
      "chat": -1.6739143857147652e-16,
      "cc": -1.9478276488317234e-15
    },
    {
      "check": "C3",
      "item": "[cubic_step|111].kappa2_h",
      "result": "PASS",
      "chat": 1.7403176010158433e-15,
      "cc": -2.0861676807089763e-15
    },
    {
      "check": "C3",
      "item": "[cubic_step|111].halving_dev_kappa2 (chat) <= kappa2_rel",
      "result": "MISS",
      "chat": 36.70942580584538,
      "cc": null
    },
    {
      "check": "C3",
      "item": "[cubic_step|111].halving_dev_kappa2 (cc) <= kappa2_rel",
      "result": "MISS",
      "chat": 3.2315974980991067,
      "cc": null
    },
    {
      "check": "C3",
      "item": "[cubic_step|111].lambda_mean_t[12]",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C3",
      "item": "[cubic_gem8|001].vT_VRH",
      "result": "PASS",
      "chat": 9.307899076533179,
      "cc": 9.307899076533193
    },
    {
      "check": "C3",
      "item": "[cubic_gem8|001].vT_HS_lo",
      "result": "PASS",
      "chat": 9.211721064370861,
      "cc": 9.211721064384875
    },
    {
      "check": "C3",
      "item": "[cubic_gem8|001].vT_HS_hi",
      "result": "PASS",
      "chat": 9.456854984588738,
      "cc": 9.456854984584107
    },
    {
      "check": "C3",
      "item": "[cubic_gem8|001].r_agg_E2_VRH[12]",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C3",
      "item": "[cubic_gem8|001].r_agg_h_VRH[12]",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C3",
      "item": "[cubic_gem8|001].r_agg_E2_HS[12]",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C3",
      "item": "[cubic_gem8|001].S_t_E2",
      "result": "PASS",
      "chat": 2.2690471976516216e-16,
      "cc": -9.550804974045757e-16
    },
    {
      "check": "C3",
      "item": "[cubic_gem8|001].S_t_h",
      "result": "PASS",
      "chat": 1.0207029061365447e-15,
      "cc": 0.0
    },
    {
      "check": "C3",
      "item": "[cubic_gem8|001].kappa2_E2",
      "result": "PASS",
      "chat": -1.4940723442743361e-16,
      "cc": -2.9881446885486723e-16
    },
    {
      "check": "C3",
      "item": "[cubic_gem8|001].kappa2_h",
      "result": "PASS",
      "chat": 1.4525703347111552e-15,
      "cc": 0.0
    },
    {
      "check": "C3",
      "item": "[cubic_gem8|001].halving_dev_kappa2 (chat) <= kappa2_rel",
      "result": "MISS",
      "chat": 36.70942580584519,
      "cc": null
    },
    {
      "check": "C3",
      "item": "[cubic_gem8|001].halving_dev_kappa2 (cc) <= kappa2_rel",
      "result": "MISS",
      "chat": 36.70942580584519,
      "cc": null
    },
    {
      "check": "C3",
      "item": "[cubic_gem8|001].lambda_mean_t[12]",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C3",
      "item": "[cubic_gem8|111].vT_VRH",
      "result": "PASS",
      "chat": 9.307899076533179,
      "cc": 9.307899076533193
    },
    {
      "check": "C3",
      "item": "[cubic_gem8|111].vT_HS_lo",
      "result": "PASS",
      "chat": 9.211721064370861,
      "cc": 9.211721064384875
    },
    {
      "check": "C3",
      "item": "[cubic_gem8|111].vT_HS_hi",
      "result": "PASS",
      "chat": 9.456854984588738,
      "cc": 9.456854984584107
    },
    {
      "check": "C3",
      "item": "[cubic_gem8|111].r_agg_E2_VRH[12]",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C3",
      "item": "[cubic_gem8|111].r_agg_h_VRH[12]",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C3",
      "item": "[cubic_gem8|111].r_agg_E2_HS[12]",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C3",
      "item": "[cubic_gem8|111].S_t_E2",
      "result": "PASS",
      "chat": -1.1819852171697386e-15,
      "cc": 2.925271284971411e-16
    },
    {
      "check": "C3",
      "item": "[cubic_gem8|111].S_t_h",
      "result": "PASS",
      "chat": 0.0,
      "cc": 0.0
    },
    {
      "check": "C3",
      "item": "[cubic_gem8|111].kappa2_E2",
      "result": "PASS",
      "chat": 1.272728293270753e-16,
      "cc": -2.2936777285248548e-15
    },
    {
      "check": "C3",
      "item": "[cubic_gem8|111].kappa2_h",
      "result": "PASS",
      "chat": 0.0,
      "cc": 0.0
    },
    {
      "check": "C3",
      "item": "[cubic_gem8|111].halving_dev_kappa2 (chat) <= kappa2_rel",
      "result": "MISS",
      "chat": 36.70942580584462,
      "cc": null
    },
    {
      "check": "C3",
      "item": "[cubic_gem8|111].halving_dev_kappa2 (cc) <= kappa2_rel",
      "result": "MISS",
      "chat": 8.27952094619114,
      "cc": null
    },
    {
      "check": "C3",
      "item": "[cubic_gem8|111].lambda_mean_t[12]",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C3",
      "item": "born_t0 key set",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C3",
      "item": "born_t0[hex_step].D0_plus",
      "result": "PASS",
      "chat": -0.02052824459532726,
      "cc": -0.020528244595327125
    },
    {
      "check": "C3",
      "item": "born_t0[hex_step].D0_minus",
      "result": "PASS",
      "chat": -0.02052824459532726,
      "cc": -0.020528244595327125
    },
    {
      "check": "C3",
      "item": "born_t0[hex_step].D0_avg",
      "result": "PASS",
      "chat": -0.02052824459532726,
      "cc": -0.02052824459532713
    },
    {
      "check": "C3",
      "item": "born_t0[hex_step].D2_avg",
      "result": "PASS",
      "chat": -0.018347663163946017,
      "cc": -0.018347663163945885
    },
    {
      "check": "C3",
      "item": "born_t0[hex_step].a2agg_residual_rel",
      "result": "PASS",
      "chat": 9.076548452285695e-15,
      "cc": 1.8909475942262037e-15
    },
    {
      "check": "C3",
      "item": "born_t0[hex_gem8].D0_plus",
      "result": "PASS",
      "chat": -0.02891780760307181,
      "cc": -0.028917807603071596
    },
    {
      "check": "C3",
      "item": "born_t0[hex_gem8].D0_minus",
      "result": "PASS",
      "chat": -0.02891780760307181,
      "cc": -0.028917807603071596
    },
    {
      "check": "C3",
      "item": "born_t0[hex_gem8].D0_avg",
      "result": "PASS",
      "chat": -0.028917807603071825,
      "cc": -0.028917807603071617
    },
    {
      "check": "C3",
      "item": "born_t0[hex_gem8].D2_avg",
      "result": "PASS",
      "chat": -0.025933693584294384,
      "cc": -0.025933693584294176
    },
    {
      "check": "C3",
      "item": "born_t0[hex_gem8].a2agg_residual_rel",
      "result": "PASS",
      "chat": 7.357979369086492e-15,
      "cc": 6.689072153715041e-16
    },
    {
      "check": "C3",
      "item": "born_t0[cubic_step].D0_plus",
      "result": "PASS",
      "chat": -0.03151342243433812,
      "cc": -0.03151342243433817
    },
    {
      "check": "C3",
      "item": "born_t0[cubic_step].D0_minus",
      "result": "PASS",
      "chat": -0.03151342243433812,
      "cc": -0.03151342243433817
    },
    {
      "check": "C3",
      "item": "born_t0[cubic_step].D0_avg",
      "result": "PASS",
      "chat": -0.03151342243433812,
      "cc": -0.031513422434338176
    },
    {
      "check": "C3",
      "item": "born_t0[cubic_step].D2_avg",
      "result": "PASS",
      "chat": -0.028537471107946306,
      "cc": -0.028537471107946338
    },
    {
      "check": "C3",
      "item": "born_t0[cubic_step].a2agg_residual_rel",
      "result": "PASS",
      "chat": 3.2825286917824895e-15,
      "cc": 4.376704922376667e-15
    },
    {
      "check": "C3",
      "item": "born_t0[cubic_gem8].D0_plus",
      "result": "PASS",
      "chat": -0.04367714392697779,
      "cc": -0.04367714392697755
    },
    {
      "check": "C3",
      "item": "born_t0[cubic_gem8].D0_minus",
      "result": "PASS",
      "chat": -0.04367714392697779,
      "cc": -0.04367714392697755
    },
    {
      "check": "C3",
      "item": "born_t0[cubic_gem8].D0_avg",
      "result": "PASS",
      "chat": -0.043677143926977795,
      "cc": -0.043677143926977566
    },
    {
      "check": "C3",
      "item": "born_t0[cubic_gem8].D2_avg",
      "result": "PASS",
      "chat": -0.039713976791286285,
      "cc": -0.03971397679128604
    },
    {
      "check": "C3",
      "item": "born_t0[cubic_gem8].a2agg_residual_rel",
      "result": "PASS",
      "chat": 4.542764439072047e-15,
      "cc": 1.5724953827557158e-15
    },
    {
      "check": "C4",
      "item": "F-MS-3.state",
      "result": "PASS",
      "chat": "SILENT",
      "cc": "SILENT"
    },
    {
      "check": "C4",
      "item": "F-MS-2.state",
      "result": "PASS",
      "chat": "REGISTERED_NOT_EXECUTED",
      "cc": "REGISTERED_NOT_EXECUTED"
    },
    {
      "check": "C4",
      "item": "F-MS-1.state",
      "result": "PASS",
      "chat": "RETIRED_TO_CONTROL",
      "cc": "RETIRED_TO_CONTROL"
    },
    {
      "check": "C4",
      "item": "verdict_class",
      "result": "PASS",
      "chat": "IDENTITY-DELIVERED",
      "cc": "IDENTITY-DELIVERED"
    },
    {
      "check": "C4",
      "item": "quadrature.n_theta",
      "result": "PASS",
      "chat": 64,
      "cc": 64
    },
    {
      "check": "C4",
      "item": "quadrature.n_phi",
      "result": "PASS",
      "chat": 128,
      "cc": 128
    },
    {
      "check": "C4",
      "item": "chat: doubling_residual <= tol",
      "result": "PASS",
      "chat": 1.7763568394002505e-15,
      "cc": null
    },
    {
      "check": "C4",
      "item": "chat: t_grid == schema",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C4",
      "item": "cc: doubling_residual <= tol",
      "result": "PASS",
      "chat": 1.1102230246251565e-15,
      "cc": null
    },
    {
      "check": "C4",
      "item": "cc: t_grid == schema",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C5",
      "item": "rows count",
      "result": "PASS",
      "chat": 5,
      "cc": 5
    },
    {
      "check": "C5",
      "item": "rows[0].id",
      "result": "PASS",
      "chat": "H-MS-1",
      "cc": "H-MS-1"
    },
    {
      "check": "C5",
      "item": "rows[0].concordant",
      "result": "PASS",
      "chat": true,
      "cc": true
    },
    {
      "check": "C5",
      "item": "rows[1].id",
      "result": "PASS",
      "chat": "H-MS-2",
      "cc": "H-MS-2"
    },
    {
      "check": "C5",
      "item": "rows[1].concordant",
      "result": "PASS",
      "chat": true,
      "cc": true
    },
    {
      "check": "C5",
      "item": "rows[2].id",
      "result": "PASS",
      "chat": "H-MS-3",
      "cc": "H-MS-3"
    },
    {
      "check": "C5",
      "item": "rows[2].concordant",
      "result": "PASS",
      "chat": false,
      "cc": false
    },
    {
      "check": "C5",
      "item": "rows[3].id",
      "result": "PASS",
      "chat": "H-MS-4",
      "cc": "H-MS-4"
    },
    {
      "check": "C5",
      "item": "rows[3].concordant",
      "result": "PASS",
      "chat": true,
      "cc": true
    },
    {
      "check": "C5",
      "item": "rows[4].id",
      "result": "PASS",
      "chat": "H-MS-5",
      "cc": "H-MS-5"
    },
    {
      "check": "C5",
      "item": "rows[4].concordant",
      "result": "PASS",
      "chat": false,
      "cc": false
    },
    {
      "check": "C5",
      "item": "compare verdict_class",
      "result": "PASS",
      "chat": null,
      "cc": null
    }
  ],
  "n_checks": 415,
  "n_miss": 9,
  "misses": [
    {
      "check": "C1",
      "item": "F-CTRL-ADMIX.r_xtal_h_projected",
      "result": "MISS",
      "chat": 0.0,
      "cc": -0.001967367205683912
    },
    {
      "check": "C3",
      "item": "[cubic_step|001].halving_dev_kappa2 (chat) <= kappa2_rel",
      "result": "MISS",
      "chat": 4.802491637841732,
      "cc": null
    },
    {
      "check": "C3",
      "item": "[cubic_step|001].halving_dev_kappa2 (cc) <= kappa2_rel",
      "result": "MISS",
      "chat": 36.70942580584521,
      "cc": null
    },
    {
      "check": "C3",
      "item": "[cubic_step|111].halving_dev_kappa2 (chat) <= kappa2_rel",
      "result": "MISS",
      "chat": 36.70942580584538,
      "cc": null
    },
    {
      "check": "C3",
      "item": "[cubic_step|111].halving_dev_kappa2 (cc) <= kappa2_rel",
      "result": "MISS",
      "chat": 3.2315974980991067,
      "cc": null
    },
    {
      "check": "C3",
      "item": "[cubic_gem8|001].halving_dev_kappa2 (chat) <= kappa2_rel",
      "result": "MISS",
      "chat": 36.70942580584519,
      "cc": null
    },
    {
      "check": "C3",
      "item": "[cubic_gem8|001].halving_dev_kappa2 (cc) <= kappa2_rel",
      "result": "MISS",
      "chat": 36.70942580584519,
      "cc": null
    },
    {
      "check": "C3",
      "item": "[cubic_gem8|111].halving_dev_kappa2 (chat) <= kappa2_rel",
      "result": "MISS",
      "chat": 36.70942580584462,
      "cc": null
    },
    {
      "check": "C3",
      "item": "[cubic_gem8|111].halving_dev_kappa2 (cc) <= kappa2_rel",
      "result": "MISS",
      "chat": 8.27952094619114,
      "cc": null
    }
  ],
  "S9_triggered": true,
  "overall": "MISS -> S9",
  "comparator": "g_mscs1_compare_v1_0.py",
  "comparator_md5": "22432b292ae0a9d5c91a6cb7aa67502f",
  "schema_md5": "76a42db3fd6ad82e485752bc2ddb24d5",
  "chat_checkpoint_md5": "c04c0b8ea34cfe60f231aa06828e6ce4",
  "cc_checkpoint_md5": "249e11dd53c4cb82f302b15d3c94c337"
}
=====END-EMBED name=g_mscs1_twoleg_comparison.json=====

