# g_ci1_phase2_regime_ccleg.py — G-CI1 CC leg, Phase 2 (E-9 full-from-scratch):
# 2.1 containment (s1 + Q_T^a from the tensors, <= 1e-6 relative vs banked digits;
#     A(theta)-anchor gate on the cubic tensors; isotropic-input null; Voigt control),
# 2.2 I-2 attenuation curve on the 33-point grid (Q^(a), Q^(d) = Q^(a)/8 per the
#     H-6 erratum reading, alpha_T*d, Im k/Re k; Rayleigh exponent control;
#     stochastic-asymptote control),
# 2.3 I-3 residual curve by the DIRECT principal-value route of record (E-12):
#     Delta_ch(x) = -[Re mt_T(x) - Re mt_T(0)]/2, on shell, static value
#     subtracted; per-point doubling gate; D2; large-x plateau,
# 2.4 ray bracket c_path vs {Voigt, Reuss, Hill, HS-, HS+} (E-11: ray-regime
#     attenuation VOID by default),
# 2.5 validity indicators (eps_T, coherent-wave, phase-perturbation, x_S; x_G=10).
#
# Substrate units (rho = 1); lengths in units of the SAF scale a inside the
# integrals; d = 2a so k0*a = x/2.  Everything is built from the pinned pieces
# of G_POLY1_PIN_RECORD.md (byte-verified): the SO(3) covariance Xi, the SAF
# spectrum ratio (1+q^2 a^2)^-2, the modal propagator with
# Im g0M ~ -pi*delta(s-k_M0)/(2 rho V_M0^2 k_M0), the Rayleigh assembly
# alpha_P*a = Q_P*(k_P0 a)^4, and the Voigt reference medium.
#
# Derived reduction used here (documented for the record):
#   mt_T(x) = -(1/(V_T0^2 k0^2)) Int d^3s SAF(|k-s|) *
#             sum_M W_TM(k,s) / (V_M0^2 (k_M0^2 - s^2 + i0)),
#   W_TM(k,s) = k0^2 s^2 Phi_TM(mu),  mu = k-hat . s-hat,
#   Phi_TM the same angular polynomial as the pinned Rayleigh assembly;
#   sign fixed by Im k >= 0 (pin convention (i)).  Consequences verified
#   in-instrument as falsifiers:
#     (F1) Im mt_T(x) = Q^(a)(x) x^3 / 4  (links I-3 to I-2 exactly),
#     (F2) Re mt_T(0) = Q_TT^a + Q_TL^a (V_L0/V_T0)^3 (closed form),
#     (F3) x->0 of Q^(a)(x) = Q_T^a (containment),
#     (F4) Rayleigh exponent 4.00 +- 0.02 on [1e-4, 1e-3],
#     (F5) stochastic asymptote Q^(a) x^2 -> Phi_TT(1)/V_T0^4.
#   The residual is integrated in the DIFFERENCE form
#     Delta_ch(x) = (1/2) sum_M c_M PV Int_0^inf N_M(s;x)/(k_M^2-s^2) ds,
#     N_M(s;x) = s^4 [F_M(s;x) - F_M(s;0)] + k_M^2 s^2 F_M(s;0),
#     c_M = 1/(V_T0^2 V_M0^2),
#   which is pointwise O(x^2) (no catastrophic small-x cancellation); the
#   PV pole is handled by exact subtraction with the exact truncated-range
#   log correction (the H-7(i) lesson); the s-panels always resolve the SAF
#   scale s ~ 1 (the H-7(ii) lesson); the far tail is mapped exactly via
#   t = 1/s (no truncation).

import math
import os
import sys
import time

import numpy as np
from mpmath import mp, mpf, log as mplog, pi as mppi

import gci1_cc_common as cc
from g_ci1_phase1_irrep_ccleg import (build_config_tensors, iso_tensor,
                                      voigt_avg_moduli, CONFIGS)

QUICK = "--quick" in sys.argv

# banked containment targets (dispatch section 2; order hex:step, hex:gem8,
# cubic:step, cubic:gem8)
BANKED_S1 = [1.51508022e-1, 1.81569447e-1, 2.33348904e-1, 2.84231508e-1]
BANKED_QTA = [3.519074e-2, 5.002055e-2, 5.407763e-2, 7.549430e-2]
BANKED_HS_MU = {
    "hex:step": [70.40652703751678, 70.97358894133485],
    "hex:gem8": [99.81834260491628, 101.05874270193425],
    "cubic:step": [60.196099, 61.904685],
    "cubic:gem8": [84.855805, 89.432106],
}
CONTAIN_TOL = 1e-6
DOUBLE_GATE = 1e-8
DOUBLE_FLOOR = 1e-6
X_GRID_N = [n / 2.0 for n in range(-16, 17)]          # exponents -8 .. 8 step 0.5
X_GRID = [10.0 ** e for e in X_GRID_N]
XG = 10.0


# ------------------------------------------------------ SO(3) covariance ----

def euler_zyz(al, be, ga):
    ca, sa = math.cos(al), math.sin(al)
    cb, sb = math.cos(be), math.sin(be)
    cg, sg = math.cos(ga), math.sin(ga)
    Rz1 = np.array([[ca, -sa, 0], [sa, ca, 0], [0, 0, 1.0]])
    Ry = np.array([[cb, 0, sb], [0, 1.0, 0], [-sb, 0, cb]])
    Rz2 = np.array([[cg, -sg, 0], [sg, cg, 0], [0, 0, 1.0]])
    return Rz1 @ Ry @ Rz2


def so3_covariance(C, n_beta=12, n_ang=16):
    """Own quadrature: Haar average over zyz Euler angles; Gauss-Legendre in
    cos(beta) (integrand a polynomial of degree <= 8 there after the exact
    uniform alpha/gamma averages), uniform grids in alpha and gamma (band
    limit 8 < n_ang).  Returns (Xi as (81,81), mean C as (3,3,3,3))."""
    ub, wb = np.polynomial.legendre.leggauss(n_beta)
    angs = [2.0 * math.pi * (j + 0.5) / n_ang for j in range(n_ang)]
    mean1 = np.zeros(81)
    mean2 = np.zeros((81, 81))
    wsum = 0.0
    for ib in range(n_beta):
        be = math.acos(ub[ib])
        for al in angs:
            for ga in angs:
                R = euler_zyz(al, be, ga)
                Cr = np.einsum("ia,jb,kc,ld,abcd->ijkl", R, R, R, R, C,
                               optimize=True).reshape(81)
                w = wb[ib]
                mean1 += w * Cr
                mean2 += w * np.outer(Cr, Cr)
                wsum += w
    mean1 /= wsum
    mean2 /= wsum
    Xi = mean2 - np.outer(mean1, mean1)
    return Xi, mean1.reshape(3, 3, 3, 3)


def cubic_anchor_controls(Xi, nu):
    """Pin (69) family: contraction <(dC_nnmm)^2> = (nu^2/525)(3+cos^2 th)^2
    and the n^4 m^4 contraction (16 nu^2/525) P4(cos th)."""
    X = Xi.reshape((3,) * 8)
    worst_a = 0.0
    worst_p4 = 0.0
    for th in [0.0, math.pi / 6, math.pi / 4, math.pi / 3, math.pi / 2, 1.1]:
        n = np.array([0.0, 0.0, 1.0])
        m = np.array([math.sin(th), 0.0, math.cos(th)])
        got_a = np.einsum("ijklpqrs,i,j,k,l,p,q,r,s->", X,
                          n, n, m, m, n, n, m, m, optimize=True)
        ref_a = (nu * nu / 525.0) * (3.0 + math.cos(th) ** 2) ** 2
        got_p = np.einsum("ijklpqrs,i,j,k,l,p,q,r,s->", X,
                          n, n, n, n, m, m, m, m, optimize=True)
        u = math.cos(th)
        p4 = (35 * u ** 4 - 30 * u ** 2 + 3) / 8.0
        ref_p = (16.0 * nu * nu / 525.0) * p4
        worst_a = max(worst_a, abs(got_a - ref_a) / (nu * nu / 525.0 * 16.0))
        worst_p4 = max(worst_p4, abs(got_p - ref_p) / (nu * nu / 525.0 * 16.0))
    return worst_a, worst_p4


def delta_pairing_fit(Xi, nu):
    """Least-squares fit Xi = a T_A + b T_B + c T_C (pin (A.3)-(A.4));
    reference a = 2 nu^2/1575, b = -nu^2/630, c = nu^2/180."""
    import itertools
    d = np.eye(3)

    def pairing_tensor(pairs):
        T = np.ones((3,) * 8)
        out = np.zeros((3,) * 8)
        idx = np.indices((3,) * 8)
        mask = np.ones((3,) * 8, bool)
        for (u, v) in pairs:
            mask &= (idx[u] == idx[v])
        out[mask] = 1.0
        del T
        return out.reshape(81 * 81)

    lat = [0, 1, 2, 3]
    grk = [4, 5, 6, 7]

    def pair_ups(items):
        if not items:
            yield []
            return
        a0 = items[0]
        for j in range(1, len(items)):
            rest = items[1:j] + items[j + 1:]
            for tail in pair_ups(rest):
                yield [(a0, items[j])] + tail

    TA = np.zeros(81 * 81)
    for pl in pair_ups(lat):
        for pg in pair_ups(grk):
            TA += pairing_tensor(pl + pg)
    TB = np.zeros(81 * 81)
    for perm in itertools.permutations(grk):
        TB += pairing_tensor(list(zip(lat, perm)))
    TC = np.zeros(81 * 81)
    for ll in itertools.combinations(lat, 2):
        rest_l = [x for x in lat if x not in ll]
        for gg in itertools.combinations(grk, 2):
            rest_g = [x for x in grk if x not in gg]
            for perm in itertools.permutations(rest_g):
                TC += pairing_tensor([ll, gg] + list(zip(rest_l, perm)))
    M = np.stack([TA, TB, TC], axis=1)
    coef, res, _, _ = np.linalg.lstsq(M, Xi.reshape(-1), rcond=None)
    ref = np.array([2 * nu * nu / 1575.0, -nu * nu / 630.0, nu * nu / 180.0])
    resid = np.linalg.norm(M @ coef - Xi.reshape(-1)) / max(
        np.linalg.norm(Xi), 1e-300)
    return coef.tolist(), ref.tolist(), float(
        np.max(np.abs(coef - ref)) / (nu * nu / 180.0)), float(resid)


# ------------------------------------------------- Phi_TM(mu) polynomials ----

def phi_poly(Xi, mode_m):
    """Coefficients [phi_0..phi_4] of Phi_TM(mu) (external P = T averaged,
    intermediate M summed), plus purity diagnostics (odd/deg>4 content)."""
    X = Xi.reshape((3,) * 8)
    ph = np.array([0.0, 0.0, 1.0])
    Ep = (np.eye(3) - np.outer(ph, ph)) / 2.0
    nodes = np.cos(np.pi * np.arange(9) / 8.0)
    vals = []
    for mu in nodes:
        sq = math.sqrt(max(0.0, 1.0 - mu * mu))
        sv = np.array([sq, 0.0, mu])
        if mode_m == "L":
            Dm = np.outer(sv, sv)
        else:
            Dm = np.eye(3) - np.outer(sv, sv)
        v = np.einsum("ijklpqrs,ip,j,q,kr,l,s->", X, Dm, sv, sv, Ep, ph, ph,
                      optimize=True)
        vals.append(float(v))
    V = np.vander(nodes, 9, increasing=True)
    coefs = np.linalg.solve(V, np.array(vals))
    scale = max(abs(c) for c in coefs)
    impurity = max(abs(coefs[5]), abs(coefs[6]), abs(coefs[7]), abs(coefs[8]),
                   abs(coefs[1]), abs(coefs[3])) / max(scale, 1e-300)
    return coefs[:5].tolist(), float(impurity)


# --------------------------------------- exact/series SAF angular moments ----

def moments_In(A, B, nmax=4, am=None, ap=None):
    """I_n = Int_{-1}^{1} mu^n (A - B mu)^-2 dmu, n = 0..nmax (mpf).
    Series in beta = B/A for beta < 1/2, else the exact binomial form.
    am/ap: exact A-B and A+B (e.g. 1+(kp-s)^2, 1+(kp+s)^2) — passed in to
    avoid any large-argument cancellation."""
    A = mpf(A)
    B = mpf(B)
    if B == 0:
        return [mpf(2) / (A * A) / (n + 1) if n % 2 == 0 else mpf(0)
                for n in range(nmax + 1)]
    beta = B / A
    out = []
    if abs(beta) < 0.5:
        eps_stop = mpf(10) ** (-(mp.dps + 5))
        for n in range(nmax + 1):
            ssum = mpf(0)
            j = 0
            while True:
                if (n + j) % 2 == 0:
                    term = (j + 1) * beta ** j * mpf(2) / (n + j + 1)
                    ssum += term
                    if j > 2 and abs(term) < eps_stop * max(abs(ssum), mpf(1)):
                        break
                j += 1
                if j > 4000:
                    break
            out.append(ssum / (A * A))
        return out
    if ap is None:
        ap = A + B
    if am is None:
        am = A - B
    J = [2 * B / (ap * am), mplog(ap / am)]
    for k in range(2, nmax + 1):
        J.append((ap ** (k - 1) - am ** (k - 1)) / (k - 1))
    from math import comb
    for n in range(nmax + 1):
        ssum = mpf(0)
        for k in range(n + 1):
            ssum += comb(n, k) * (A ** (n - k)) * ((-1) ** k) * J[k]
        out.append(ssum / (B ** (n + 1)))
    return out


def moments_In_pair(A0, dA, B, nmax=4, am=None, ap=None):
    """Returns (I_n(A0+dA, B), I_n(A0, 0)-difference-free static moments,
    Delta I_n = I_n(A,B) - I_n(A0,0)) computed STABLY for small B:
    the static I_n(A0,0) has only the even 2/(n+1)/A0^2 terms; the
    difference uses (1/A^2 - 1/A0^2) = -dA (A+A0)/(A^2 A0^2) exactly."""
    A0 = mpf(A0)
    dA = mpf(dA)
    B = mpf(B)
    A = A0 + dA
    stat = [mpf(2) / (A0 * A0) / (n + 1) if n % 2 == 0 else mpf(0)
            for n in range(nmax + 1)]
    if B != 0 and abs(B / A) >= 0.5:
        full = moments_In(A, B, nmax, am=am, ap=ap)
        return full, stat, [full[n] - stat[n] for n in range(nmax + 1)]
    beta = B / A if B != 0 else mpf(0)
    inv_diff = -dA * (A + A0) / (A * A * A0 * A0)   # 1/A^2 - 1/A0^2, exact
    eps_stop = mpf(10) ** (-(mp.dps + 5))
    full = []
    delta = []
    for n in range(nmax + 1):
        # j = 0 term separated: (2/(n+1)) [1/A^2] for even n
        if n % 2 == 0:
            d0 = mpf(2) / (n + 1) * inv_diff
        else:
            d0 = mpf(0)
        tail = mpf(0)
        j = 1
        while B != 0:
            if (n + j) % 2 == 0:
                term = (j + 1) * beta ** j * mpf(2) / (n + j + 1)
                tail += term
                if j > 2 and abs(term) < eps_stop * max(abs(tail), mpf(1)):
                    break
            j += 1
            if j > 4000:
                break
        tail /= (A * A)
        delta.append(d0 + tail)
        full.append(stat[n] + d0 + tail)
    return full, stat, delta


# ------------------------------------------------------------ I-2 curve  ----

def q_of_x(phis, prefs, rmods, x, with_gl_gate=False):
    """Q^(a)(x) = sum_M pref_M * Int Phi_TM(mu) (1+q^2)^-2 dmu with
    q^2 = kp^2 + km^2 - 2 kp km mu, kp = x/2, km = r_M x/2 (a = 1 units).
    Exact/series moments; optional composite-GL doubling gate in log-u."""
    kp = mpf(x) / 2
    total = mpf(0)
    gate = 0.0
    for M in ("T", "L"):
        km = kp * rmods[M]
        A = 1 + kp * kp + km * km
        B = 2 * kp * km
        In = moments_In(A, B, 4, am=1 + (kp - km) ** 2, ap=1 + (kp + km) ** 2)
        val = sum(mpf(phis[M][n]) * In[n] for n in range(5))
        total += mpf(prefs[M]) * val
        if with_gl_gate:
            g1 = gl_log_u(phis[M], A, B, 20)
            g2 = gl_log_u(phis[M], A, B, 40)
            rel = abs(g2 - g1) / max(abs(g2), mpf(1) ** 0)  # placeholder
            rel = float(abs(g2 - g1) / abs(g2)) if g2 != 0 else 0.0
            gate = max(gate, rel,
                       float(abs(g2 - val) / abs(val)) if val != 0 else 0.0)
    return total, gate


def gl_log_u(phi, A, B, npan_nodes):
    """Int Phi(mu)(A-B mu)^-2 dmu via u = A - B mu, log-spaced panels."""
    if B == 0:
        return sum(mpf(phi[n]) * (mpf(2) / (A * A) / (n + 1))
                   for n in range(0, 5, 2))
    lo, hi = A - B, A + B
    ndec = float(mplog(hi / lo) / mplog(10)) if hi > lo else 0.0
    npan = max(2, int(3 * ndec) + 1)
    edges = [lo * (hi / lo) ** (mpf(j) / npan) for j in range(npan + 1)]
    nodes, wts = np.polynomial.legendre.leggauss(npan_nodes)
    tot = mpf(0)
    for j in range(npan):
        a1, b1 = edges[j], edges[j + 1]
        half = (b1 - a1) / 2
        mid = (b1 + a1) / 2
        for t, w in zip(nodes, wts):
            u = mid + half * mpf(float(t))
            mu = (A - u) / B
            p = sum(mpf(phi[n]) * mu ** n for n in range(5))
            tot += mpf(float(w)) * half * p / (u * u) / B
    return tot


# ------------------------------------------------------------ I-3 curve  ----

def residual_point(phis, prefs, rmods, Vt2VM2inv, x, nodes_per_panel):
    """Delta_ch(x) by the direct-PV difference route (docstring above).
    Returns (Delta, diag) with diag carrying the pole/tail bookkeeping."""
    kp = mpf(x) / 2
    nodes, wts = np.polynomial.legendre.leggauss(nodes_per_panel)
    nodes = [mpf(float(t)) for t in nodes]
    wts = [mpf(float(w)) for w in wts]
    total = mpf(0)

    def F_pair(M, s):
        """(F_M(s;x), DeltaF = F_M(s;x) - F_M(s;0)) with SAF units a=1:
        F = (2/pi) sum_n phi_n I_n(A,B), A = 1+kp^2+s^2, B = 2 kp s;
        exact A-B = 1+(kp-s)^2, A+B = 1+(kp+s)^2 (no cancellation)."""
        A0 = 1 + s * s
        dA = kp * kp
        B = 2 * kp * s
        am = 1 + (kp - s) * (kp - s)
        ap = 1 + (kp + s) * (kp + s)
        full, stat, delta = moments_In_pair(A0, dA, B, 4, am=am, ap=ap)
        f = sum(mpf(phis[M][n]) * full[n] for n in range(5))
        df = sum(mpf(phis[M][n]) * delta[n] for n in range(5))
        return (2 / mppi) * f, (2 / mppi) * df

    def F_static(M, s):
        A0 = 1 + s * s
        JM = sum(mpf(phis[M][n]) * mpf(2) / (n + 1)
                 for n in range(0, 5, 2))
        return (2 / mppi) * JM / (A0 * A0)

    for M in ("T", "L"):
        km = kp * rmods[M]

        def numer(s):
            fx, dfx = F_pair(M, s)
            f0 = F_static(M, s)
            return s ** 4 * dfx + km * km * s * s * f0

        nk = numer(km)

        # PV window: half-width min(km/2, 1/2) — the numerator varies on the
        # ABSOLUTE SAF scale (width ~ 1 forward peak), so the window and its
        # surrounding refinement must be absolute-scale, not relative-scale
        # (the large-x resolution lesson, H-logged).
        w_abs = min(km / 2, mpf(1) / 2)
        wlo, whi = km - w_abs, km + w_abs
        smax = max(mpf(10) ** 4, 20 * km, 20 * kp)
        edges = set()

        def cluster(center):
            """Geometric absolute-scale refinement around a feature at
            `center` (pole and/or SAF forward peak), out to center/2 and 2x."""
            w0 = min(center / 2, mpf(1) / 2)
            off = w0
            while off < center:
                for v in (center - off, center + off):
                    if 0 < v < smax:
                        edges.add(v)
                if off >= center / 2:
                    break
                off = min(off * 3, center / 2)

        cluster(km)                      # the PV pole
        if M == "L" and kp > 10:
            cluster(kp)                  # the SAF forward peak (TL: not at km)
        for f in (mpf(2), mpf(4)):
            if km * f < smax:
                edges.add(km * f)
        j = -6
        while mpf(10) ** (mpf(j) / 2) < smax:
            v = mpf(10) ** (mpf(j) / 2)
            if not (wlo < v < whi):
                edges.add(v)
            j += 1
        edges.add(mpf(0))
        edges.add(smax)
        edges = {v for v in edges if not (wlo < v < whi)} | {wlo, whi}
        edges = sorted(edges)

        seg_sum = mpf(0)
        for j in range(len(edges) - 1):
            a1, b1 = edges[j], edges[j + 1]
            half = (b1 - a1) / 2
            mid = (b1 + a1) / 2
            in_window = (a1 >= wlo - wlo * mpf("1e-30")) and \
                        (b1 <= whi + whi * mpf("1e-30"))
            for t, w in zip(nodes, wts):
                s = mid + half * t
                den = (km - s) * (km + s)
                if in_window:
                    val = (numer(s) - nk) / den
                else:
                    val = numer(s) / den
                seg_sum += w * half * val
        # exact PV log correction over the subtracted window
        pvlog = (mplog((km + whi) / (whi - km))
                 - mplog((km + wlo) / (km - wlo))) / (2 * km)
        seg_sum += nk * pvlog
        # exact far tail via t = 1/s on (0, 1/smax]
        tail = mpf(0)
        tlo, thi = mpf(0), 1 / smax
        for (ta, tb) in ((tlo, thi / 2), (thi / 2, thi)):
            half = (tb - ta) / 2
            mid = (tb + ta) / 2
            for t, w in zip(nodes, wts):
                tt = mid + half * t
                if tt == 0:
                    continue
                s = 1 / tt
                den = (km - s) * (km + s)
                tail += w * half * numer(s) / den / (tt * tt)
        seg_sum += tail
        total += mpf(Vt2VM2inv[M]) * seg_sum

    return total / 2, {"pole_at": [float(kp), float(kp * rmods["L"])]}


# ------------------------------------------------------- sphere statistics --

def sphere_stats(C, n_th, n_ph):
    """Uniform-S^2 transverse eigen-speed statistics: pooled mean, eps_T,
    the s1 candidate family, harmonic path means, qL-separation diagnostic."""
    uu, ww = np.polynomial.legendre.leggauss(n_th)
    phis = 2.0 * math.pi * (np.arange(n_ph) + 0.5) / n_ph
    W = np.repeat(ww, n_ph) / (2.0 * n_ph)          # normalized S^2 measure
    ct = np.repeat(uu, n_th * 0 + n_ph)
    st = np.sqrt(np.clip(1.0 - ct * ct, 0.0, None))
    cp = np.tile(np.cos(phis), n_th)
    sp = np.tile(np.sin(phis), n_th)
    D = np.stack([st * cp, st * sp, ct], axis=1)
    G = np.einsum("ijkl,nj,nl->nik", C, D, D, optimize=True)
    evals, evecs = np.linalg.eigh(G)
    udotn = np.abs(np.einsum("nki,nk->ni", evecs, D))
    ql_idx = np.argmax(udotn, axis=1)
    order_mismatch = int(np.sum(ql_idx != 2))
    idx = np.arange(len(D))
    all_i = np.tile(np.arange(3), (len(D), 1))
    mask = all_i != ql_idx[:, None]
    tvals = evals[mask].reshape(len(D), 2)
    v_lo = np.sqrt(np.minimum(tvals[:, 0], tvals[:, 1]))
    v_hi = np.sqrt(np.maximum(tvals[:, 0], tvals[:, 1]))
    del idx
    m_pool = float(np.sum(W * (v_hi + v_lo)) / 2.0)
    eps_T = math.sqrt(float(np.sum(W * ((v_hi - m_pool) ** 2
                                        + (v_lo - m_pool) ** 2) / 2.0))) / m_pool
    split = v_hi - v_lo
    loc_mean = (v_hi + v_lo) / 2.0
    cands = {
        "rms_split_over_pool_mean": math.sqrt(float(np.sum(W * split ** 2))) / m_pool,
        "rms_of_local_ratio": math.sqrt(float(np.sum(W * (split / loc_mean) ** 2))),
        "rms_slowness_split_times_pool_mean": math.sqrt(float(np.sum(
            W * (1.0 / v_lo - 1.0 / v_hi) ** 2))) * m_pool,
        "half_rms_split_over_pool_mean": 0.5 * math.sqrt(float(
            np.sum(W * split ** 2))) / m_pool,
        "half_rms_of_local_ratio": 0.5 * math.sqrt(float(
            np.sum(W * (split / loc_mean) ** 2))),
        "rms_split_over_voigt": None,   # filled by caller (needs V_T0)
        "_rms_split": math.sqrt(float(np.sum(W * split ** 2))),
    }
    inv_sum = float(np.sum(W * (1.0 / v_hi + 1.0 / v_lo)))
    c_path = 2.0 / inv_sum
    c_fast = 1.0 / float(np.sum(W * (1.0 / v_hi)))
    c_slow = 1.0 / float(np.sum(W * (1.0 / v_lo)))
    return {"m_pool": m_pool, "eps_T": eps_T, "cands": cands,
            "c_path": c_path, "c_fast": c_fast, "c_slow": c_slow,
            "qL_order_mismatch_points": order_mismatch, "n_points": len(D)}


# --------------------------------------------------------------------- main --

def main():
    t0 = time.time()
    pats = cc.load_t1_patterns()
    tensors, data = build_config_tensors()
    if cc.md5_file(os.path.join(cc.EMBED_DIR, "G_POLY1_PIN_RECORD.md")) != \
            "621120e50d395beea2e914d54c929600":
        raise RuntimeError("pin record hash mismatch — HALT")

    order = CONFIGS
    ckpt = {"gate": "G-CI1", "leg": "CC", "phase": 2,
            "inputs": {"poly_vrh_results.json": "200e7a8b775577564369c6924d38a84c",
                       "G_POLY1_PIN_RECORD.md": "621120e50d395beea2e914d54c929600"},
            "grid_exponents": X_GRID_N,
            "configs": {}, "controls": {}, "honesty": []}

    # ---------------- isotropic-input null (control) ----------------
    Ciso = iso_tensor(130.0, 65.0)
    Xi_iso, mean_iso = so3_covariance(Ciso, 12, 16)
    iso_null = float(np.max(np.abs(Xi_iso)) / np.max(np.abs(np.outer(
        mean_iso.reshape(81), mean_iso.reshape(81)))))
    ckpt["controls"]["isotropic_input_null"] = iso_null
    print("[%.0fs] iso null %.3e" % (time.time() - t0, iso_null))

    contain_all_pass = True
    for icfg, name in enumerate(order):
        C = tensors[name]
        e = data["vrh"][name]
        kv, gv = voigt_avg_moduli(C)
        Vt0 = math.sqrt(gv)
        Vl0 = math.sqrt(kv + 4.0 * gv / 3.0)
        rL = Vt0 / Vl0

        Xi, Cmean = so3_covariance(C, 12, 16)
        Xi2, _ = so3_covariance(C, 16, 20)          # doubling-style control
        xi_ctrl = float(np.max(np.abs(Xi2 - Xi)) / np.max(np.abs(Xi)))
        kvm, gvm = voigt_avg_moduli(Cmean)
        voigt_ctrl = abs(gvm - gv) / gv
        gv_vs_json = abs(gv - e["G_V"]) / e["G_V"]

        cfg = {"V_T0": Vt0, "V_L0": Vl0,
               "xi_quadrature_doubling_rel": xi_ctrl,
               "voigt_mean_consistency_rel": voigt_ctrl,
               "G_V_vs_json_rel": gv_vs_json}

        if name.startswith("cubic"):
            cco = e["C_over_rho"]
            nu = cco["C11"] - cco["C12"] - 2.0 * cco["C44"]
            wa, wp = cubic_anchor_controls(Xi, nu)
            coef, ref, cdev, cres = delta_pairing_fit(Xi, nu)
            cfg["A_theta_anchor_rel_worst"] = wa
            cfg["P4_contraction_rel_worst"] = wp
            cfg["delta_pairing"] = {"fit": coef, "pinned": ref,
                                    "max_rel_dev": cdev, "fit_residual": cres}
            if wa > 1e-9 or wp > 1e-9:
                raise RuntimeError("A(theta) anchor gate failed — HALT")

        # Phi polynomials
        phis = {}
        impur = {}
        for M in ("T", "L"):
            co, imp = phi_poly(Xi, M)
            phis[M] = co
            impur[M] = imp
        cfg["phi_TT_coeffs"] = phis["T"]
        cfg["phi_TL_coeffs"] = phis["L"]
        cfg["phi_impurity_max"] = max(impur.values())

        # Rayleigh assembly
        prefs = {"T": (1.0) ** 3 / (2.0 * Vt0 ** 2 * Vt0 ** 2),
                 "L": (Vt0 / Vl0) ** 3 / (2.0 * Vt0 ** 2 * Vl0 ** 2)}
        JT = sum(2.0 * phis["T"][n] / (n + 1) for n in range(0, 5, 2))
        JL = sum(2.0 * phis["L"][n] / (n + 1) for n in range(0, 5, 2))
        Q_TT = prefs["T"] * JT
        Q_TL = prefs["L"] * JL
        Q_Ta = Q_TT + Q_TL
        dev_q = abs(Q_Ta - BANKED_QTA[icfg]) / BANKED_QTA[icfg]
        cfg["Q_TT_a"] = Q_TT
        cfg["Q_TL_a"] = Q_TL
        cfg["Q_T_a"] = Q_Ta
        cfg["Q_T_a_banked"] = BANKED_QTA[icfg]
        cfg["Q_T_a_rel_dev"] = dev_q

        # sphere statistics: s1 candidates, eps_T, ray means (with doubling)
        st1 = sphere_stats(C, 256, 512)
        st2 = sphere_stats(C, 512, 1024)
        st1["cands"]["rms_split_over_voigt"] = st1["cands"]["_rms_split"] / Vt0
        st2["cands"]["rms_split_over_voigt"] = st2["cands"]["_rms_split"] / Vt0
        sphere_doub = max(
            abs(st2["eps_T"] - st1["eps_T"]) / st2["eps_T"],
            abs(st2["c_path"] - st1["c_path"]) / st2["c_path"],
            abs(st2["cands"]["rms_split_over_pool_mean"]
                - st1["cands"]["rms_split_over_pool_mean"])
            / st2["cands"]["rms_split_over_pool_mean"])
        s1_cands = {k: v for k, v in st2["cands"].items()
                    if not k.startswith("_")}
        s1_pass = {k: abs(v - BANKED_S1[icfg]) / BANKED_S1[icfg]
                   for k, v in s1_cands.items() if v is not None}
        best = min(s1_pass, key=lambda k: s1_pass[k])
        cfg["s1_candidates"] = s1_cands
        cfg["s1_candidate_rel_dev"] = s1_pass
        cfg["s1_convention_of_record"] = best
        cfg["s1"] = s1_cands[best]
        cfg["s1_banked"] = BANKED_S1[icfg]
        cfg["s1_rel_dev"] = s1_pass[best]
        cfg["sphere_quadrature_doubling_rel"] = sphere_doub
        cfg["eps_T"] = st2["eps_T"]
        cfg["eps_T_sq"] = st2["eps_T"] ** 2
        cfg["eps_T_sq_le_0p10"] = bool(st2["eps_T"] ** 2 <= 0.10)
        cfg["qL_separation_mismatch_points"] = st2["qL_order_mismatch_points"]

        contain_pass = (dev_q <= CONTAIN_TOL) and (s1_pass[best] <= CONTAIN_TOL)
        cfg["containment_pass"] = bool(contain_pass)
        contain_all_pass = contain_all_pass and contain_pass
        print("[%.0fs] %s containment: s1 dev %.2e (%s) | Q_T^a dev %.2e | %s"
              % (time.time() - t0, name, s1_pass[best], best, dev_q,
                 "PASS" if contain_pass else "FAIL"))
        if not contain_pass:
            ckpt["configs"][name] = cfg
            continue

        # D-2 cone speed
        remt0 = Q_TT + Q_TL * (Vl0 / Vt0) ** 3
        cfg["Re_mt_T_0"] = remt0
        cfg["c_cone_over_V_T0"] = 1.0 / (1.0 + remt0 / 2.0)
        cfg["c_cone"] = Vt0 / (1.0 + remt0 / 2.0)
        cfg["c_cone_between_Reuss_and_Hill"] = bool(
            e["vT_R"] <= cfg["c_cone"] <= e["vT_VRH"])

        # ---------------- I-2 curve ----------------
        mp.dps = 40
        rmods = {"T": 1.0, "L": rL}
        grid = X_GRID if not QUICK else [1e-8, 1e-4, 1e-3, 1e-2, 1.0, 1e2, 1e8]
        i2 = []
        for x in grid:
            qa, gate = q_of_x(phis, prefs, rmods, x, with_gl_gate=True)
            qa_f = float(qa)
            qd_f = qa_f / 8.0
            i2.append({"x": x, "Q_a": qa_f, "Q_d": qd_f,
                       "alpha_T_d": qd_f * x ** 4,
                       "Imk_over_Rek": qd_f * x ** 3,
                       "doubling_gate": gate})
        cfg["I2_curve"] = i2
        # controls
        q_small = i2[0]["Q_a"]
        cfg["I2_x0_recovers_Q_T_a_rel"] = abs(q_small - Q_Ta) / Q_Ta
        xs_fit = [p for p in i2 if 1e-4 <= p["x"] <= 1e-3]
        lg = [math.log(p["alpha_T_d"]) for p in xs_fit]
        lx = [math.log(p["x"]) for p in xs_fit]
        nfit = len(lg)
        sx = sum(lx)
        sy = sum(lg)
        sxx = sum(v * v for v in lx)
        sxy = sum(a * b for a, b in zip(lx, lg))
        slope = (nfit * sxy - sx * sy) / (nfit * sxx - sx * sx)
        cfg["rayleigh_exponent_fit"] = slope
        cfg["rayleigh_exponent_pass"] = bool(abs(slope - 4.0) <= 0.02)
        phi_tt_1 = sum(phis["T"])
        big = [p for p in i2 if p["x"] >= 1e7]
        if big:
            ratio = big[-1]["Q_a"] * big[-1]["x"] ** 2 * Vt0 ** 4 / phi_tt_1
            cfg["stochastic_asymptote_ratio_at_xmax"] = ratio
        cfg["I2_doubling_gate_worst"] = max(p["doubling_gate"] for p in i2)

        # ---------------- I-3 residual (direct PV route of record) --------
        Vt2VM2inv = {"T": 1.0 / (Vt0 ** 2 * Vt0 ** 2),
                     "L": 1.0 / (Vt0 ** 2 * Vl0 ** 2)}
        i3 = []
        escalated = []
        for x in grid:
            base_dps = 32 if x >= 1e-2 else int(34 + 2.5 * (-math.log10(x)))
            # Adaptive doubling ladder (H-CC-2): a first full pass with the
            # fixed 20/40 ladder attained (1e-8, 1e-6] at x in
            # {10^-6.5, 10^-6, 10^-5.5} for every config — inside the
            # recorded-value band but above the 1e-8 gate.  Escalate
            # per-point until the last-doubling estimate meets the gate or
            # the floor voids the point; the finest value is the value of
            # record and the gate is the last doubling.
            ladder = (20, 40, 80, 160)
            mp.dps = base_dps
            prev = residual_point(phis, prefs, rmods, Vt2VM2inv, x,
                                  ladder[0])[0]
            prev_s = prev / mpf(x) ** 2 if x <= 1e-2 else prev
            gate, d2v, scaled_2, n_used = None, None, None, ladder[0]
            for lvl, n in enumerate(ladder[1:]):
                mp.dps = base_dps + 6 * lvl
                d2v, diag = residual_point(phis, prefs, rmods, Vt2VM2inv,
                                           x, n)
                scaled_2 = d2v / mpf(x) ** 2 if x <= 1e-2 else d2v
                gate = float(abs(scaled_2 - prev_s) / abs(scaled_2)) \
                    if scaled_2 != 0 else 0.0
                n_used = n
                if gate <= DOUBLE_GATE:
                    break
                prev_s = scaled_2
            if n_used > 40:
                escalated.append((x, n_used, gate))
            void_num = gate > DOUBLE_FLOOR
            i3.append({"x": x, "Delta_ch": float(d2v),
                       "scaled_residual": float(scaled_2),
                       "doubling_gate": gate, "nodes_per_panel": n_used,
                       "void_num": bool(void_num), "dps": mp.dps})
            if void_num:
                ckpt["honesty"].append(
                    "H-CC: VOID-NUM at x=%.3e config %s (gate %.2e)"
                    % (x, name, gate))
        if escalated:
            ckpt["honesty"].append(
                "H-CC-2 (%s): self-catch — the fixed 20/40 ladder missed "
                "the 1e-8 doubling gate at %d point(s); escalated to the "
                "recorded nodes_per_panel; final last-doubling estimates: %s"
                % (name, len(escalated),
                   "; ".join("x=%.3e n=%d gate=%.2e" % t for t in escalated)))
        cfg["I3_curve"] = i3
        small = [p for p in i3 if p["x"] <= 1e-2]
        d2_coef = small[0]["scaled_residual"]
        cfg["D2"] = d2_coef
        cfg["D2_flatness_rel_max"] = max(
            abs(p["scaled_residual"] - d2_coef) / abs(d2_coef) for p in small)
        plat = [p for p in i3 if p["x"] >= 1e5]
        if plat:
            pv = plat[-1]["Delta_ch"]
            cfg["plateau"] = pv
            cfg["plateau_flatness_rel_max"] = max(
                abs(p["Delta_ch"] - pv) / abs(pv) for p in plat)
        cfg["I3_doubling_gate_worst"] = max(p["doubling_gate"] for p in i3)

        # falsifier F6: static-integral identity Int_0^inf s^2 F_M(s;0) ds
        # = J_M/2 exercised through the SAME panel/GL machinery (tests the
        # SAF-scale resolution of the s-quadrature independently of the pole)
        mp.dps = 40
        nodes40, wts40 = np.polynomial.legendre.leggauss(40)
        f6_worst = 0.0
        for M, JM in (("T", JT), ("L", JL)):
            edges6 = [mpf(0)] + [mpf(10) ** (mpf(j) / 2) for j in range(-6, 9)]
            tot6 = mpf(0)
            for jj in range(len(edges6) - 1):
                a1, b1 = edges6[jj], edges6[jj + 1]
                half = (b1 - a1) / 2
                mid = (b1 + a1) / 2
                for t, w in zip(nodes40, wts40):
                    s = mid + half * mpf(float(t))
                    tot6 += mpf(float(w)) * half * s * s * \
                        (2 / mppi) * mpf(JM) / (1 + s * s) ** 2
            thi6 = 1 / edges6[-1]
            for t, w in zip(nodes40, wts40):
                tt = thi6 / 2 + (thi6 / 2) * mpf(float(t))
                if tt == 0:
                    continue
                s = 1 / tt
                tot6 += mpf(float(w)) * (thi6 / 2) * s * s * \
                    (2 / mppi) * mpf(JM) / (1 + s * s) ** 2 / (tt * tt)
            f6_worst = max(f6_worst, float(abs(tot6 - mpf(JM) / 2)
                                           / (mpf(JM) / 2)))
        cfg["static_integral_identity_rel_worst"] = f6_worst

        # falsifier F1: Im side of the SAME operator vs I-2 (three probes)
        # (algebraically near-circular in this formulation — it certifies the
        # sign/normalization bookkeeping, not an independent quadrature)
        mp.dps = 40
        f1_worst = 0.0
        for x in (1e-4, 1.0, 100.0):
            kpb = mpf(x) / 2
            imm = mpf(0)
            for M in ("T", "L"):
                kmb = kpb * rmods[M]
                A = 1 + kpb * kpb + kmb * kmb
                B = 2 * kpb * kmb
                In = moments_In(A, B, 4, am=1 + (kpb - kmb) ** 2,
                                ap=1 + (kpb + kmb) ** 2)
                Fk = (2 / mppi) * sum(mpf(phis[M][n]) * In[n]
                                      for n in range(5))
                imm += mpf(Vt2VM2inv[M]) * mppi * kmb ** 3 * Fk / 2
            qa, _ = q_of_x(phis, prefs, rmods, x)
            ref = qa * mpf(x) ** 3 / 4
            f1_worst = max(f1_worst, float(abs(imm - ref) / ref))
        cfg["im_side_consistency_rel_worst"] = f1_worst

        # validity indicators + x_S
        xs_val = None
        for p in sorted(i2, key=lambda r: r["x"]):
            ok = (p["Imk_over_Rek"] <= 0.10) and (cfg["eps_T"] * p["x"] <= 1.0)
            if ok:
                xs_val = p["x"]
        cfg["x_S"] = xs_val
        cfg["x_G"] = XG
        cfg["void_gap_exists"] = bool(xs_val is not None and xs_val < XG)

        # ---------------- ray bracket ----------------
        chain = {"Voigt": e["vT_V"], "Reuss": e["vT_R"], "Hill": e["vT_VRH"],
                 "HS-": math.sqrt(BANKED_HS_MU[name][0]),
                 "HS+": math.sqrt(BANKED_HS_MU[name][1])}
        dgeo = {X: (st2["c_path"] - v) / v for X, v in chain.items()}
        cfg["c_path_mean_arrival"] = st2["c_path"]
        cfg["c_path_fast"] = st2["c_fast"]
        cfg["c_path_slow"] = st2["c_slow"]
        cfg["Delta_geo"] = dgeo
        cfg["Delta_geo_min_abs_over_chain"] = min(abs(v) for v in dgeo.values())
        cfg["Delta_geo_minmax"] = [min(dgeo.values()), max(dgeo.values())]
        cfg["ray_attenuation"] = "VOID (E-11: no prior-art form pinned; a VOID " \
                                 "only widens a window)"

        ckpt["configs"][name] = cfg
        print("[%.0fs] %s: D2 %.7e | plateau %.5e | c_cone/V_T0 %.6f | "
              "x_S %.3f | I3 gate worst %.2e"
              % (time.time() - t0, name, cfg["D2"], cfg.get("plateau", 0.0),
                 cfg["c_cone_over_V_T0"], cfg["x_S"],
                 cfg["I3_doubling_gate_worst"]))

    ckpt["containment_all_pass"] = bool(contain_all_pass)
    if not contain_all_pass:
        ckpt["HALT"] = "containment fail (X-1 unresolved)"

    ckpt["honesty"].insert(0,
        "H-CC-1: the banked s1 statistic is not restated in closed form in "
        "the dispatched texts; the CC instrument evaluated a pre-declared "
        "family of RMS transverse-splitting normalizations on the sphere and "
        "identified the convention of record by the 2.1 containment gate "
        "itself (winning candidate + full candidate table recorded in each "
        "config block); no curve or anchor was consulted.")

    info = cc.write_checkpoint(
        os.path.join(cc.GATE_DIR, "ci1_phase2_cc.json"), ckpt, pats)
    hits = 0
    for p in (os.path.abspath(__file__),
              os.path.join(cc.GATE_DIR, "gci1_cc_common.py"),
              os.path.join(cc.GATE_DIR, "ci1_phase2_cc.json")):
        hits += len(cc.t1_scan_file(p, pats))
    print("PHASE2 CC %s" % ("OK" if contain_all_pass else "HALT"))
    print("checkpoint:", info)
    print("T1 hits:", hits)
    if hits:
        raise RuntimeError("T1 hit — HALT")


if __name__ == "__main__":
    main()
