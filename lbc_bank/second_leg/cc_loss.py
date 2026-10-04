#!/usr/bin/env python3
"""cc_loss.py -- second leg, task Q-D (drag prefactor, loss-length arithmetic, Eq.(3)/(4) numbers).

Reads qb_results.json (this leg's own 3D BdG results) from the working directory and writes qd_results.json.
Everything is recomputed here; no number is typed in except the stated dispatch inputs (closure constants,
four maps, c_T = 7.68, tau = 10, eps = 1).

Part 1 (drag coefficient).  Analytic result (derived twice in QD_NOTES.md):
    F_d = C rho F_nu v^-2 int_0^inf q^3 |V(q)|^2 dq,   C = 1/(4 pi)      (3D point source, v > c_nu)
    F_d/L = (1/(2 pi)) rho F_nu v^-2 S(M) int_0^inf q^2 |V(q)|^2 dq       (filament = 2D analogue)
with V(q) = int d^3r exp(-i q.r) V(r).  Numerical confirmations done here:
  (a) linear-response force integral F = int d^3q/(2pi)^3 q |V|^2 Im chi(q, q.v) with a regularised retarded chi,
      extrapolated to zero damping (angular part alone with damping prop. to q, and the full (q, mu) double
      integral with constant damping and a Gaussian vertex);
  (b) Fermi golden rule, dE/dt = int d^3q/(2pi)^3 2pi |V|^2 (q.v) S(q, q.v), S from the f-sum normalisation,
      delta function replaced by a narrow Gaussian and extrapolated, F_d = (dE/dt)/v;
  (c) single Bogoliubov branch (exact dispersion), contact vertex, against the closed form
      g_d^2 n (v^2-c^2)^2/(pi v^2); 2D Bogoliubov against g_d^2 n (v^2-c^2)/v.
Part 2: loss-length arithmetic (dispatch Q-D item 2) and the four readings.
Part 3: Eq.(3) coefficient and 1/(2 gamma^2).
"""
import os
os.environ.setdefault("OMP_NUM_THREADS", "2")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "2")
os.environ.setdefault("MKL_NUM_THREADS", "2")
import json, math, time
import numpy as np
from scipy import integrate

HERE = os.path.dirname(os.path.abspath(__file__))
T0 = time.time()

# ----------------------------------------------------------------------------------------------------------
# inputs
# ----------------------------------------------------------------------------------------------------------
qb = json.load(open(os.path.join(HERE, "qb_results.json")))
c2 = float(qb["schema"]["c2"])                         # omega/q of branch 2 at q = 0.15 along x
f2_q015 = float(qb["schema"]["F2_basal_q015"])
f2_q03 = float(qb["extras"]["F2_basal_q03"])
c_kappa = float(qb["schema"]["c_kappa"])               # primary: q = 0.15 along x
c_kappa_q0 = float(qb["extras"]["c_kappa_q0_extrapolated"])
c_kappa_q03 = float(qb["extras"]["c_kappa_q03"])
c2_lsq = float(qb["extras"]["lsq_speeds"]["x"]["L2"])
ct_mean_own = float(qb["extras"]["cT_mean_all_dir_pol_q015"])
ct_min_own = float(qb["schema"]["cT_min"])
ct_max_own = float(qb["schema"]["cT_max"])

gamma = 3.1974e11
xi = 1.616255e-35          # metres (as given)
l_prop = 3.0857e20         # metres
phi = (1.0 + math.sqrt(5.0)) / 2.0
m_old = phi ** 2
c_t = 7.68                 # dynamical mean transverse speed, as given
points = {                 # (A, J, O, T = tau)
    "p1": (15.17, 4.68, 1.82, 8.06),
    "p2": (9.35, 0.61, 1.6401, 2.74),
    "p3": (13.73, 4.43, 1.20, 7.49),
    "p4": (18.26, 7.41, 0.45, 11.23),
}
channels = ("A", "J", "O")
tau_eq3 = 10.0
eps_eq3 = 1.0


def mach_s(m):
    """S(M) = (1 - 1/M^2)^(-1/2), M > 1."""
    return (1.0 - 1.0 / (m * m)) ** -0.5


# ----------------------------------------------------------------------------------------------------------
# Part 1: drag coefficient, analytic and numerical
# ----------------------------------------------------------------------------------------------------------
C_ANALYTIC = 1.0 / (4.0 * math.pi)
C2D_ANALYTIC = 1.0 / (2.0 * math.pi)     # filament / 2D coefficient multiplying S(M)


def im_chi_tilde(mu, v, c, eps, rho=1.0, fnu=1.0):
    """Im chi(q, q v mu)/q^0 for chi = rho q^2 F/((w + i eta)^2 - c^2 q^2) with eta = eps*c*q (q drops out)."""
    w = v * mu
    eta = eps * c
    den = (w * w - eta * eta - c * c) ** 2 + 4.0 * w * w * eta * eta
    return -rho * fnu * 2.0 * w * eta / den


def angular_3d(mach, eps):
    """I3 = int_{-1}^{1} dmu mu Im chi~(mu); exact limit -pi rho F / v^2. Returns I3 * (-v^2/pi)."""
    c, v = 1.0, mach
    mu0 = c / v
    f = lambda mu: mu * im_chi_tilde(mu, v, c, eps)
    w = eps * c / v                      # peak half-width in mu
    pts = {-1.0, 0.0, 1.0}
    for s0 in (-mu0, mu0):
        for k in (0.0, 1.0, -1.0, 10.0, -10.0, 100.0, -100.0, 1000.0, -1000.0):
            x = s0 + k * w
            if -1.0 < x < 1.0:
                pts.add(x)
    pts = sorted(pts)
    tot = 0.0
    for a, b in zip(pts[:-1], pts[1:]):
        val, _ = integrate.quad(f, a, b, limit=2000, epsabs=0.0, epsrel=1e-12)
        tot += val
    return tot * (-v * v / math.pi)


def angular_2d(mach, eps):
    """I2 = int_0^{2pi} dth cos th Im chi~(cos th); exact limit -2 pi rho F S(M)/v^2.
    Returns I2*(-v^2/(2 pi)), i.e. the numerically emerging Mach factor."""
    c, v = 1.0, mach
    th0 = math.acos(c / v)
    f = lambda th: math.cos(th) * im_chi_tilde(math.cos(th), v, c, eps)
    w = eps * c / (v * math.sin(th0))    # peak half-width in theta
    pts = {0.0, math.pi / 2, math.pi}
    for s0 in (th0, math.pi - th0):
        for k in (0.0, 1.0, -1.0, 10.0, -10.0, 100.0, -100.0, 1000.0, -1000.0):
            x = s0 + k * w
            if 0.0 < x < math.pi:
                pts.add(x)
    pts = sorted(pts)
    tot = 0.0
    for a, b in zip(pts[:-1], pts[1:]):
        val, _ = integrate.quad(f, a, b, limit=2000, epsabs=0.0, epsrel=1e-12)
        tot += val
    tot *= 2.0          # (pi, 2pi) mirrors (0, pi)
    return tot * (-v * v / (2.0 * math.pi))


def richardson(xs, ys, order=1):
    """polynomial extrapolation to x -> 0 using a fit in powers of x (degree len-1, starting at x^order)."""
    xs = np.asarray(xs, float)
    ys = np.asarray(ys, float)
    n = len(xs)
    cols = [np.ones(n)] + [xs ** (order + k) for k in range(n - 1)]
    a = np.vstack(cols).T
    sol = np.linalg.solve(a, ys)
    return float(sol[0])


part1 = {"convention": "V(q) = int d^3r exp(-i q.r) V(r); chi(q,w) = rho q^2 sum F_nu/((w+i0)^2 - c_nu^2 q^2); "
                       "force on defect F = int d^3q/(2pi)^3 q |V(q)|^2 Im chi(q, q.v)",
         "C_analytic": C_ANALYTIC, "C2D_analytic_times_S": C2D_ANALYTIC}

# (a1) angular integrals with damping proportional to q: q-integral factorises exactly
eps_list = [1e-3, 5e-4, 2.5e-4]
mach_list = [1.2, m_old, 5.0, c_t / c2]
ang = {}
for mach in mach_list:
    r3 = [angular_3d(mach, e) for e in eps_list]
    r2 = [angular_2d(mach, e) for e in eps_list]
    ang[repr(mach)] = {
        "eps": eps_list,
        "ratio3d_vs_exact_limit_1": r3,
        "ratio3d_extrap": richardson(eps_list, r3, order=1),
        "mach_factor_2d_numeric": r2,
        "mach_factor_2d_extrap": richardson(eps_list, r2, order=1),
        "S_of_M_exact": mach_s(mach),
    }
part1["a1_linear_response_angular"] = ang
part1["a1_C_numeric_from_3d_angular_at_M_new"] = ang[repr(c_t / c2)]["ratio3d_extrap"] * C_ANALYTIC  # = (1/4pi)*ratio


# (a2) full (q, mu) double integral, constant damping eta, Gaussian vertex V = exp(-q^2/2) (int q^3 V^2 = 1/2)
def force_full_3d(v, c, eta, rho=1.0, fnu=1.0):
    def inner(q):
        mu0 = c / v
        def f(mu):
            w = q * v * mu
            den = (w * w - eta * eta - c * c * q * q) ** 2 + 4.0 * w * w * eta * eta
            return q * mu * (-rho * fnu * q * q * 2.0 * w * eta / den)
        tot = 0.0
        for a, b in ((-1.0, -mu0), (-mu0, 0.0), (0.0, mu0), (mu0, 1.0)):
            val, _ = integrate.quad(f, a, b, limit=1000, epsabs=0.0, epsrel=1e-12)
            tot += val
        return q * q * math.exp(-q * q) * tot
    val, _ = integrate.quad(inner, 0.0, 9.0, limit=400, epsabs=0.0, epsrel=1e-11)
    f_par = val / (4.0 * math.pi ** 2)          # 2pi q^2 dq dmu/(2pi)^3
    return -f_par * v * v / (rho * fnu * 0.5)   # C estimate


eta_list = [4e-3, 2e-3, 1e-3]
full3d = {}
for (v, c) in ((3.0, 1.0), (7.68, c2)):
    cs = [force_full_3d(v, c, e) for e in eta_list]
    full3d[f"v={v!r},c={c!r}"] = {"eta": eta_list, "C_numeric": cs,
                                  "C_extrap": richardson(eta_list, cs, order=1)}
part1["a2_linear_response_full_double_integral"] = full3d


# (b) golden rule with Gaussian-smeared delta, dE/dt then F = (dE/dt)/v; Gaussian vertex
def golden_3d(v, c, sig, rho=1.0, fnu=1.0):
    def inner(q):
        wq = c * q
        wt = rho * q * fnu / (2.0 * c)          # S = (rho q F/(2c)) delta(w - c q)  [f-sum weight rho q^2 F/2]
        def f(mu):
            w = q * v * mu
            return w * wt * math.exp(-0.5 * ((w - wq) / sig) ** 2) / (sig * math.sqrt(2.0 * math.pi))
        mu0 = c / v
        lo = max(0.0, mu0 - 12.0 * sig / (q * v))
        hi = min(1.0, mu0 + 12.0 * sig / (q * v))
        val, _ = integrate.quad(f, lo, hi, points=[mu0] if lo < mu0 < hi else None,
                                limit=500, epsabs=0.0, epsrel=1e-12)
        return q * q * math.exp(-q * q) * val
    val, _ = integrate.quad(inner, 1e-9, 9.0, limit=400, epsabs=0.0, epsrel=1e-11)
    de_dt = 2.0 * math.pi * 2.0 * math.pi * val / (2.0 * math.pi) ** 3
    return (de_dt / v) * v * v / (rho * fnu * 0.5)


sig_list = [4e-3, 2e-3, 1e-3]
gold = {}
for (v, c) in ((3.0, 1.0), (7.68, c2)):
    cs = [golden_3d(v, c, s) for s in sig_list]
    gold[f"v={v!r},c={c!r}"] = {"sigma": sig_list, "C_numeric": cs, "C_extrap": richardson(sig_list, cs, order=1)}
part1["b_golden_rule_energy_rate"] = gold


# (c) Bogoliubov single branch, contact vertex g_d = 1, n = 1, medium c = 1 (g n = c^2), m = hbar = 1
def bogo_golden(v, sig, dim=3, c=1.0, n=1.0):
    eps_b = lambda q: math.sqrt(c * c * q * q + 0.25 * q ** 4)
    qmax = 2.0 * math.sqrt(v * v - c * c)

    def inner(q):
        e = eps_b(q)
        wt = n * 0.5 * q * q / e                    # Z per volume (Feynman: S(q) = q^2/(2 eps))
        g = lambda w: math.exp(-0.5 * ((w - e) / sig) ** 2) / (sig * math.sqrt(2.0 * math.pi))
        if dim == 3:
            # integrate in w = q v mu over the Gaussian window only (Gaussian tails beyond 12 sigma negligible)
            lo, hi = max(0.0, e - 12.0 * sig), min(q * v, e + 12.0 * sig)
            if hi <= lo:
                return 0.0
            f = lambda w: w * wt * g(w) / (q * v)
            pts = [x for x in (e - sig, e, e + sig) if lo < x < hi]
            val, _ = integrate.quad(f, lo, hi, points=pts or None, limit=800, epsabs=0.0, epsrel=1e-12)
            return q * q * val * 2.0 * math.pi * 2.0 * math.pi / (2.0 * math.pi) ** 3
        f = lambda th: (q * v * math.cos(th)) * wt * g(q * v * math.cos(th))
        val, _ = integrate.quad(f, 0.0, math.pi / 2, points=[math.acos(e / (q * v))] if e < q * v else None,
                                limit=800, epsabs=0.0, epsrel=1e-12)
        return q * 2.0 * val * 2.0 * math.pi / (2.0 * math.pi) ** 2
    # the smeared Cherenkov edge sits at q_max with width ~ sigma/(v - d eps/dq) ~ sigma/v; split around it
    dq = sig / v
    brk = sorted({x for x in (qmax - 100 * dq, qmax - 10 * dq, qmax - dq, qmax, qmax + dq, qmax + 10 * dq,
                              qmax + 100 * dq) if 1e-9 < x < qmax * 1.3})
    edges = [1e-9] + brk + [qmax * 1.3]
    val = 0.0
    for a, b in zip(edges[:-1], edges[1:]):
        vv, _ = integrate.quad(inner, a, b, limit=800, epsabs=0.0, epsrel=1e-11)
        val += vv
    return val / v       # drag force


bog = {}
for v in (1.5, 2.5):
    exact3 = (v * v - 1.0) ** 2 / (math.pi * v * v)
    exact2 = (v * v - 1.0) / v
    f3 = [bogo_golden(v, s, 3) for s in sig_list]
    f2 = [bogo_golden(v, s, 2) for s in sig_list]
    qmax = 2.0 * math.sqrt(v * v - 1.0)
    bog[repr(v)] = {
        "F3d_exact_gd2_n_(v2-c2)^2/(pi v2)": exact3,
        "F3d_from_C_formula_C_n_v^-2_qmax^4/4": C_ANALYTIC * qmax ** 4 / 4.0 / (v * v),
        "F3d_numeric": f3, "F3d_numeric_extrap": richardson(sig_list, f3, order=1),
        "F2d_exact_gd2_n_(v2-c2)/v": exact2, "F2d_numeric": f2,
        "F2d_numeric_extrap": richardson(sig_list, f2, order=1),
        "AP_form_4pi_n_b2_m_v2_(1-c2/v2)^2_with_g=2pi_b": 4.0 * math.pi * (1.0 / (2.0 * math.pi)) ** 2 * v * v
        * (1.0 - 1.0 / (v * v)) ** 2,
    }
part1["c_bogoliubov_contact"] = bog
_c_routes = ([v["C_extrap"] for v in full3d.values()] + [v["C_extrap"] for v in gold.values()]
             + [ang[m]["ratio3d_extrap"] * C_ANALYTIC for m in ang])
part1["summary"] = {
    "C_numeric_all_routes": _c_routes,
    "max_abs_rel_dev_C_numeric_vs_1_over_4pi": max(abs(x / C_ANALYTIC - 1.0) for x in _c_routes),
    "max_abs_rel_dev_2d_mach_factor_vs_S": max(abs(ang[m]["mach_factor_2d_extrap"] / ang[m]["S_of_M_exact"] - 1.0)
                                               for m in ang),
    "max_abs_rel_dev_bogoliubov_3d": max(abs(b["F3d_numeric_extrap"] / b["F3d_exact_gd2_n_(v2-c2)^2/(pi v2)"] - 1.0)
                                         for b in bog.values()),
    "max_abs_rel_dev_bogoliubov_2d": max(abs(b["F2d_numeric_extrap"] / b["F2d_exact_gd2_n_(v2-c2)/v"] - 1.0)
                                         for b in bog.values()),
    "C_if_V_uses_symmetric_(2pi)^-3/2_convention": 2.0 * math.pi ** 2,
    "C_2d_filament_per_length_times_S_of_M": C2D_ANALYTIC,
}
part1["web_lookup"] = ("arxiv.org, link.aps.org, osti.gov, researchgate.net: blocked by the egress proxy (organization "
                       "policy); only search-engine summaries were reachable. Equation number (12) not verified first-hand.")
part1["AP_comparison"] = ("3D Bogoliubov reduction gives F = g_d^2 n m^3 (v^2-c^2)^2/(pi hbar^4 v^2) = 4 pi n b^2 m v^2 "
                          "(1-c^2/v^2)^2 for g_d = 2 pi hbar^2 b/m (heavy impurity); identical to the AP 3D drag "
                          "as quoted by citing works; direct fetch of the paper was blocked by the egress proxy")

# ----------------------------------------------------------------------------------------------------------
# Part 2: loss-length arithmetic
# ----------------------------------------------------------------------------------------------------------
table = {}
best = (-math.inf, None, None)
worst = (math.inf, None, None)
for pname, (pa, pj, po, pt) in points.items():
    row = {}
    for ch, pv in zip(channels, (pa, pj, po)):
        ell = gamma * m_old * pt * xi / pv
        lg = math.log10(ell / l_prop)
        row[ch] = {"ell_m": ell, "log10_ell_over_Lprop": lg}
        if lg > best[0]:
            best = (lg, pname, ch)
        if lg < worst[0]:
            worst = (lg, pname, ch)
    table[pname] = row
v467_best, v467_worst = best[0], worst[0]
bp, bc = best[1], best[2]
p_best = dict(zip(channels, points[bp][:3]))[bc]
tau_best = points[bp][3]

m_new = c_t / c2
s_old = mach_s(m_old)
s_new = mach_s(m_new)
mach_ratio = s_old / s_new
c_s = c_t / m_old
f2s = {"q015": f2_q015, "q03": f2_q03}


def readings(f2, ck=c_kappa, m_n=m_new, mr=mach_ratio):
    main = mr / f2
    return {
        "R1_fixed_vertex_filament": main,
        "R2_fixed_vertex_point_source": 1.0 / f2,
        "R3_closure_literal_M_to_cT_over_c2": (m_n / m_old) / f2,
        "R4_fixed_dressed_static_deficit": main / (ck / c_s) ** 4,
    }


rd = {k: readings(f) for k, f in f2s.items()}
main_factor = {k: rd[k]["R1_fixed_vertex_filament"] for k in f2s}
main_logs = sorted(math.log10(v) for v in main_factor.values())
main_orders_recovered = [main_logs[0], main_logs[-1]]
main_headline_orders = [v467_best + main_logs[0], v467_best + main_logs[-1]]

all_rec = [math.log10(v) for k in rd for v in rd[k].values()]
band_orders = [v467_best + min(all_rec), v467_best + max(all_rec)]
band_recovered = [min(all_rec), max(all_rec)]

# alternatives
alt = {}
r3_nof2 = m_new / m_old
rec_alt1 = [math.log10(v) for k in rd for name, v in rd[k].items() if not name.startswith("R3")] + [math.log10(r3_nof2)]
alt["R3_without_1_over_F2_factor"] = r3_nof2
alt["R3_without_1_over_F2_log10"] = math.log10(r3_nof2)
alt["band_orders_with_R3_without_F2"] = [v467_best + min(rec_alt1), v467_best + max(rec_alt1)]
r4_point = {k: (1.0 / f) / (c_kappa / c_s) ** 4 for k, f in f2s.items()}
alt["R4_on_point_source_factor"] = r4_point
rec_alt2 = all_rec + [math.log10(v) for v in r4_point.values()]
alt["band_orders_including_R4_point_source"] = [v467_best + min(rec_alt2), v467_best + max(rec_alt2)]
rd_q0 = {k: readings(f, ck=c_kappa_q0) for k, f in f2s.items()}
alt["readings_with_c_kappa_q0"] = rd_q0
rec_alt3 = [math.log10(v) for k in rd_q0 for v in rd_q0[k].values()]
alt["band_orders_with_c_kappa_q0"] = [v467_best + min(rec_alt3), v467_best + max(rec_alt3)]
rd_q03 = {k: readings(f, ck=c_kappa_q03) for k, f in f2s.items()}
rec_alt3b = [math.log10(v) for k in rd_q03 for v in rd_q03[k].values()]
alt["band_orders_with_c_kappa_q03"] = [v467_best + min(rec_alt3b), v467_best + max(rec_alt3b)]
alt["band_recovered_orders"] = band_recovered
# diagnostic (not in the band): "dressed" deficit taken from the unrelaxed static response, i.e. the slow branch
# removed from sum F/c^2 = 1/c_kappa^2:  1/c_u^2 = (1 - S2)/c_kappa^2  (S2 = static share of branch 2, q = 0.15 x)
s2_q015 = float(qb["schema"]["S2_basal_q015"])
c_unrelaxed = c_kappa / math.sqrt(1.0 - s2_q015)
alt["S2_q015_used"] = s2_q015
alt["c_unrelaxed_static_speed"] = c_unrelaxed
alt["R4_unrelaxed_deficit_factor"] = {k: main_factor_k / (c_unrelaxed / c_s) ** 4 for k, main_factor_k in
                                      ((kk, rd[kk]["R1_fixed_vertex_filament"]) for kk in rd)}
alt["R4_unrelaxed_deficit_log10"] = {k: math.log10(v) for k, v in alt["R4_unrelaxed_deficit_factor"].items()}
# variant: M_new from the LSQ c2 (q = 0.15 and 0.3)
m_new_lsq = c_t / c2_lsq
mr_lsq = s_old / mach_s(m_new_lsq)
rd_lsq = {k: readings(f, m_n=m_new_lsq, mr=mr_lsq) for k, f in f2s.items()}
rec_lsq = [math.log10(v) for k in rd_lsq for v in rd_lsq[k].values()]
alt["M_new_with_lsq_c2"] = m_new_lsq
alt["main_orders_recovered_lsq_c2"] = sorted(math.log10(rd_lsq[k]["R1_fixed_vertex_filament"]) for k in f2s)
alt["band_orders_lsq_c2"] = [v467_best + min(rec_lsq), v467_best + max(rec_lsq)]
# variant: own mean transverse speed instead of 7.68 (M_new and c_s change)
m_new_own = ct_mean_own / c2
mr_own = s_old / mach_s(m_new_own)
c_s_own = ct_mean_own / m_old
rd_own = {k: {"R1": mr_own / f, "R2": 1.0 / f, "R3": (m_new_own / m_old) / f,
              "R4": (mr_own / f) / (c_kappa / c_s_own) ** 4} for k, f in f2s.items()}
rec_own = [math.log10(v) for k in rd_own for v in rd_own[k].values()]
alt["own_cT_mean"] = ct_mean_own
alt["main_orders_recovered_own_cT"] = sorted(math.log10(rd_own[k]["R1"]) for k in f2s)
alt["band_orders_own_cT"] = [v467_best + min(rec_own), v467_best + max(rec_own)]
alt["readings_own_cT"] = rd_own

xi_req_old = l_prop * p_best / (gamma * m_old * tau_best)
xi_req = sorted(xi_req_old / v for v in main_factor.values())
alt["xi_req_old_closure_m"] = xi_req_old
alt["xi_req_check_ratio_to_xi_at_best_old"] = xi_req_old / xi        # = 10^(-v467_best)

# ----------------------------------------------------------------------------------------------------------
# Part 3: Eq.(3) and Eq.(4)
# ----------------------------------------------------------------------------------------------------------
f2_min = min(f2_q015, f2_q03)
eq3 = (16.0 * math.pi * tau_eq3 / eps_eq3 ** 2) * (c_t / c_kappa) ** 4 / f2_min
eq3_alt = {
    "with_own_cT_mean": (16.0 * math.pi * tau_eq3 / eps_eq3 ** 2) * (ct_mean_own / c_kappa) ** 4 / f2_min,
    "with_c_kappa_q0": (16.0 * math.pi * tau_eq3 / eps_eq3 ** 2) * (c_t / c_kappa_q0) ** 4 / f2_min,
    "with_F2_q015": (16.0 * math.pi * tau_eq3 / eps_eq3 ** 2) * (c_t / c_kappa) ** 4 / f2_q015,
    "with_own_cT_min": (16.0 * math.pi * tau_eq3 / eps_eq3 ** 2) * (ct_min_own / c_kappa) ** 4 / f2_min,
    "with_own_cT_max": (16.0 * math.pi * tau_eq3 / eps_eq3 ** 2) * (ct_max_own / c_kappa) ** 4 / f2_min,
}
eq3_ell_m = eq3 * gamma * xi
eq4 = 1.0 / (2.0 * gamma ** 2)

out = {
    "task": "Q-D (cc second leg)",
    "v467_best_orders": v467_best,
    "v467_worst_orders": v467_worst,
    "main_orders_recovered": main_orders_recovered,
    "main_headline_orders": main_headline_orders,
    "band_orders": band_orders,
    "xi_req_main_m": xi_req,
    "eq3_coefficient": eq3,
    "eq4_bound": eq4,
    "drag_prefactor_3d_coeff": C_ANALYTIC,
    "inputs": {
        "c2_q015_x": c2, "F2_q015": f2_q015, "F2_q03": f2_q03, "c_kappa_q015_x": c_kappa,
        "c_kappa_q0_extrapolated": c_kappa_q0, "c_kappa_q03": c_kappa_q03, "c2_lsq_x": c2_lsq,
        "cT_mean_own_q015": ct_mean_own, "cT_min_own": ct_min_own, "cT_max_own": ct_max_own,
        "gamma": gamma, "xi_m": xi, "L_prop_m": l_prop, "phi": phi, "M_old_phi2": m_old, "c_T_given": c_t,
        "points_A_J_O_T": points, "tau_eq3": tau_eq3, "eps_eq3": eps_eq3,
    },
    "intermediates": {
        "closure_table": table,
        "best_point_channel": [bp, bc], "worst_point_channel": [worst[1], worst[2]],
        "P_best": p_best, "tau_best": tau_best,
        "M_new": m_new, "S_M_old": s_old, "S_M_new": s_new, "mach_ratio_S_old_over_S_new": mach_ratio,
        "log10_mach_ratio": math.log10(mach_ratio),
        "c_s_cT_over_phi2": c_s, "c_kappa_over_c_s": c_kappa / c_s, "(c_kappa/c_s)^4": (c_kappa / c_s) ** 4,
        "main_factor": main_factor,
        "main_factor_log10": {k: math.log10(v) for k, v in main_factor.items()},
        "readings": rd,
        "readings_log10": {k: {n: math.log10(v) for n, v in rd[k].items()} for k in rd},
        "readings_headline": {k: {n: v467_best + math.log10(v) for n, v in rd[k].items()} for k in rd},
        "F2_min": f2_min, "eq3_ell_m_gamma_xi_times_coeff": eq3_ell_m,
        "eq3_log10_ell_over_Lprop": math.log10(eq3_ell_m / l_prop),
    },
    "alternatives": alt,
    "eq3_alternatives": eq3_alt,
    "drag_derivation_checks": part1,
    "timing_s": None,
}
out["timing_s"] = time.time() - T0


def clean(o):
    if isinstance(o, dict):
        return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [clean(v) for v in o]
    if isinstance(o, (np.floating,)):
        return float(o)
    return o


with open(os.path.join(HERE, "qd_results.json"), "w") as fh:
    json.dump(clean(out), fh, indent=1)       # json uses repr(float): 17 significant digits
print(json.dumps({k: out[k] for k in ("v467_best_orders", "v467_worst_orders", "main_orders_recovered",
                                      "main_headline_orders", "band_orders", "xi_req_main_m", "eq3_coefficient",
                                      "eq4_bound", "drag_prefactor_3d_coeff")}, indent=1))
print("timing_s", out["timing_s"])
