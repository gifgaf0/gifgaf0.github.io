#!/usr/bin/env python3
"""
E3 reconciliation, stability table: which (3,1)-block levels are zero modes and which are continuum?
(R = 40, nr = 40 column of the stability table, and the coarsest mesh nr = 15 of the R = 20 refinement)

The cross-check pointed out that in the R = 40, nr = 40 column the (3,1) levels 5.4e-5 (x3),
1.94e-4 (x3), 3.73e-4 (x3) were all read as "zero modes, then continuum".  This script settles
the assignment with the original Ritz machinery of e3_stability.py (same local quadratic form,
same hats x harmonic-polynomial basis, same quadrature):

(a) radial refinement at fixed R: continuum levels are mesh-converged, zero-mode levels fall;
(b) eigenvector content: for each Ritz eigenvector v_j (S-normalised) the squared S-norm of its
    projection onto the Ritz-space images of the exact zero modes,
      translations   phi = l_i = U0^T d_i U0                       (i = 1, 2, 3),
      iso-rotations  phi = U0^T T_a U0 - T_a,  T_a in su(2)_long    (a = 1, 2, 3),
      and both families together (6 modes),
    p_j = a_j^T G^-1 a_j with a_j[m] = v_j^T b_m, b_m = <basis, mode_m>_L2, G = B^T S^-1 B
    (1 = the eigenvector lies in the span, 0 = orthogonal to it).  A triplet is called a zero-mode
    triplet when its content in the 6-mode span exceeds 0.5, continuum otherwise.  (The exact
    translation and iso-rotation modes have opposite hedgehog parity, but the hats x harmonic-polynomial
    basis is not parity invariant, so near-degenerate Ritz zero modes mix the two characters.);
(c) the free-continuum reference (1/32)(pi/R)^2 of the decoupled (1,3) block.

Writes reconcile_stability_r40.json.  No number of the original stability run is changed.
"""
import json
import time
import numpy as np
from scipy.linalg import eigh
import e3_inertia as inr
import e3_stability as st

SECTOR = "long (3,1)"
E = st.SECTORS[SECTOR]
TL = st.TL
XL = st.XL


def mode_iso(T):
    def f(x, n):
        U, dU = inr.hedgehog_fields(XL, x, n)
        return np.einsum('gji,jk,gkl->gil', U, T, U) - T[None]
    return f


def mode_trans(i):
    def f(x, n):
        U, dU = inr.hedgehog_fields(XL, x, n)
        return np.einsum('gji,gjl->gil', U, dU[:, i])           # l_i = U^T d_i U
    return f


MODES = {"translation": [mode_trans(i) for i in range(3)],
         "iso-rotation": [mode_iso(TL[a]) for a in range(3)]}


def ritz_vectors(R, nr, lmax=3, nmu=14, nphi=28, nquad=4, nev=12):
    """same assembly as e3_stability.ritz, plus the L2 projections b_m of the exact zero modes"""
    d = E.shape[0]
    n, w = inr.angular_grid(nmu, nphi)
    Y = st.harmonic_basis(lmax, n, w)
    nY = len(Y)
    na = nY * d
    rn = st.hats(R, nr)
    K = nr
    H = np.zeros((K * na, K * na))
    S = np.zeros((K * na, K * na))
    allm = [(fam, k, f) for fam, fs in MODES.items() for k, f in enumerate(fs)]
    Bm = np.zeros((K * na, len(allm)))
    gq, gw = np.polynomial.legendre.leggauss(nquad)
    S0v = np.zeros((n.shape[0], na, 4 * d))
    S0g = np.zeros((n.shape[0], na, 4 * d))
    S1 = np.zeros((n.shape[0], na, 4 * d))
    Pall = np.zeros((n.shape[0], na))            # value of angular x internal basis function c at n, per internal A
    for y, (l, Pv, Yg) in enumerate(Y):
        for A in range(d):
            c = y * d + A
            S0v[:, c, A] = Pv
            Pall[:, c] = Pv
            for i in range(3):
                S0g[:, c, (i + 1) * d + A] = Yg[:, i]
                S1[:, c, (i + 1) * d + A] = n[:, i] * Pv
    Aidx = np.array([c % d for c in range(na)])
    for e in range(nr):
        r0, r1 = rn[e], rn[e + 1]
        for t, wt in zip(gq, gw):
            r = 0.5 * (r0 + r1) + 0.5 * (r1 - r0) * t
            wr = 0.5 * (r1 - r0) * wt * r**2
            M = st.local_forms(r, n, E)
            S0 = S0v + S0g / r
            MS0 = np.einsum('gij,gqj->giq', M, S0)
            MS1 = np.einsum('gij,gqj->giq', M, S1)
            wS0, wS1 = w[:, None, None] * S0, w[:, None, None] * S1
            A00 = np.tensordot(wS0, MS0, axes=([0, 2], [0, 1]))
            A01 = np.tensordot(wS0, MS1, axes=([0, 2], [0, 1]))
            A11 = np.tensordot(wS1, MS1, axes=([0, 2], [0, 1]))
            # angular x internal projections of the exact modes at this radius
            proj = np.zeros((na, len(allm)))
            for m, (_, _, f) in enumerate(allm):
                ph = f(r, n)
                cA = -np.einsum('aij,gji->ga', E, ph)            # B-components (E is B-orthonormal)
                proj[:, m] = np.einsum('g,gc,gc->c', w, Pall, cA[:, Aidx])
            hl, hr = (r1 - r) / (r1 - r0), (r - r0) / (r1 - r0)
            dl, dr = -1 / (r1 - r0), 1 / (r1 - r0)
            loc = [(e, hl, dl), (e + 1, hr, dr)]
            for (k1, h1, d1) in loc:
                if k1 >= K:
                    continue
                Bm[k1 * na:(k1 + 1) * na] += wr * h1 * proj
                for (k2, h2, d2) in loc:
                    if k2 >= K:
                        continue
                    blk = h1 * h2 * A00 + h1 * d2 * A01 + d1 * h2 * A01.T + d1 * d2 * A11
                    H[k1 * na:(k1 + 1) * na, k2 * na:(k2 + 1) * na] += wr * blk
                    S[k1 * na:(k1 + 1) * na, k2 * na:(k2 + 1) * na] += wr * h1 * h2 * np.eye(na)
    H = 0.5 * (H + H.T)
    ev, V = eigh(H, S, subset_by_index=[0, nev - 1])
    content = {}
    for fam in list(MODES) + ["all zero modes"]:
        cols = [m for m, (fa, _, _) in enumerate(allm) if fa == fam or fam == "all zero modes"]
        Bf = Bm[:, cols]
        G = Bf.T @ np.linalg.solve(S, Bf)
        a = V.T @ Bf                                   # (nev, 3)
        content[fam] = np.einsum('jm,mn,jn->j', a, np.linalg.inv(G), a)
    return ev, content


if __name__ == "__main__":
    t0 = time.time()
    out = dict(sector=SECTOR, note="levels of the (3,1) block; content = squared S-norm of the projection of each "
               "S-normalised Ritz eigenvector onto the span of the exact zero modes of that family")
    runs = {}
    for R, nr in [(20.0, 15), (20.0, 30), (40.0, 40), (40.0, 80)]:
        ev, content = ritz_vectors(R, nr)
        key = f"R={R:g},nr={nr},lmax=3"
        runs[key] = dict(eigenvalues=ev.tolist(), translation_content=content["translation"].tolist(),
                         isorotation_content=content["iso-rotation"].tolist(),
                         zero_mode_content=content["all zero modes"].tolist(),
                         free_continuum_ref=(np.pi / R)**2 / 32)
        print(f"{key}  (free continuum (1/32)(pi/R)^2 = {(np.pi / R)**2 / 32:.4e})   [{time.time() - t0:.0f}s]", flush=True)
        for j, lam in enumerate(ev):
            print(f"   {j:2d}  lambda = {lam:.4e}   translation {content['translation'][j]:.3f}"
                  f"   iso-rotation {content['iso-rotation'][j]:.3f}   both {content['all zero modes'][j]:.3f}", flush=True)
    out["runs"] = runs

    # assignment of the three lowest triplets (R = 40, nr = 40: the stability table; R = 20, nr = 15: the
    # coarsest mesh of e3_stability_refine.py, which has the same ordering issue)
    def triplets(run):
        res = []
        for k in range(3):
            sl = slice(3 * k, 3 * k + 3)
            tc = float(np.mean(run["translation_content"][sl]))
            ic = float(np.mean(run["isorotation_content"][sl]))
            zc = float(np.mean(run["zero_mode_content"][sl]))
            lab = "zero-mode triplet (translation/iso-rotation mixture)" if zc > 0.5 else "continuum"
            res.append(dict(level=float(np.mean(run["eigenvalues"][sl])), translation_content=tc, isorotation_content=ic,
                            zero_mode_content=zc, assignment=lab))
        return res
    r40 = runs["R=40,nr=40,lmax=3"]
    r40f = runs["R=40,nr=80,lmax=3"]
    trip = triplets(r40)
    trip15 = triplets(runs["R=20,nr=15,lmax=3"])
    out["R40_nr40_triplets"] = trip
    out["R20_nr15_triplets"] = trip15
    # the continuum triplet should be mesh-converged, the zero-mode triplets should fall with nr
    out["R40_refinement_nr40_to_nr80"] = dict(nr40=r40["eigenvalues"][:9], nr80=r40f["eigenvalues"][:9])
    checks = dict(
        continuum_triplet_is_middle_one_at_nr40=trip[1]["assignment"] == "continuum",
        zero_mode_triplets_lowest_at_R20=bool(all(c > 0.5 for c in runs["R=20,nr=30,lmax=3"]["zero_mode_content"][:6])
                                              and all(c < 0.5 for c in runs["R=20,nr=30,lmax=3"]["zero_mode_content"][6:9])),
        zero_mode_triplets_first_and_third_at_R40_nr40=trip[0]["assignment"] != "continuum" and trip[2]["assignment"] != "continuum",
        continuum_level_mesh_converged_R40=bool(abs(trip[1]["level"] - min(
            r40f["eigenvalues"][j] for j in range(9) if r40f["zero_mode_content"][j] < 0.5)) / trip[1]["level"] < 0.01),
        continuum_level_near_free_value_R40=bool(abs(trip[1]["level"] / r40["free_continuum_ref"] - 1) < 0.02),
        R20_nr15_middle_triplet_is_continuum=trip15[1]["assignment"] == "continuum"
                                            and trip15[0]["assignment"] != "continuum" and trip15[2]["assignment"] != "continuum",
        no_negative_eigenvalue=bool(min(min(v["eigenvalues"]) for v in runs.values()) > -1e-6),
    )
    out["checks"] = checks
    out["runtime_s"] = time.time() - t0
    print("triplets at R=40, nr=40:", json.dumps(trip, indent=1))
    print("triplets at R=20, nr=15:", json.dumps(trip15, indent=1))
    print("checks:", checks)
    print("all checks pass:", all(checks.values()))
    with open("reconcile_stability_r40.json", "w") as fh:
        json.dump(out, fh, indent=1)
