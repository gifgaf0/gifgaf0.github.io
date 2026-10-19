#!/usr/bin/env python3
"""E7: scale and coupling audit of SEED.md section 8.  Reads hedgehog.json and hopfion.json
(run e7_hedgehog.py and e7_hopfion.py first), writes results.json.  Deterministic, < 10 s.

Units: hbar = c = 1 unless stated; hbar c = 197.3269804 MeV fm (CODATA 2022 via scipy).
Every number written to results.json carries its formula and inputs.
"""
import json, os, warnings
import numpy as np
import sympy as sp
from scipy import constants as K
from scipy.integrate import quad
from scipy.optimize import brentq, minimize_scalar

warnings.filterwarnings('ignore')
HERE = os.path.dirname(os.path.abspath(__file__))
E1_RESULTS = os.path.join(HERE, '..', 'E1_phi4', 'e1e_results.json')   # E1e (read-only, optional)
DL_DIGITIZED = os.path.join(HERE, 'dl_digitized.json')                   # e7_dl_digitize.py output


def dl_readings():
    """Demidov-Levkov curve values. Reconciliation: read from the PDF vector paths (e7_dl_digitize.py);
    version 1 used eye readings F = 4.45 (threshold) and 3.93 (g^2E = 11.5), the latter wrong by -0.085."""
    if os.path.exists(DL_DIGITIZED):
        d = json.load(open(DL_DIGITIZED))
        a, b = d['fig3b'], d['fig7b']
        return dict(F_thr=a['F_threshold_first_vertex']['F'], F_thr_g2E=a['F_threshold_first_vertex']['g2E'],
                    F_11p5=a['F_at_g2E_11p5'], F_min=a['F_min']['value'], F_min_g2E=a['F_min']['at_g2E'],
                    F_unc=a['reading_uncertainty'], left_axis_g2E=a['calibration']['left_axis_g2E'],
                    g2Nmin_hi=b['g2Nmin_high_energy_mean_8p5_to_10p5'], g2Nmin_hi_range=b['g2Nmin_high_energy_range'],
                    g2Nmin_thr=b['g2Nmin_near_threshold']['value'],
                    source='vector paths of arXiv:1103.0013v2 Fig. 3b and arXiv:1103.2133v2 Fig. 7b (dl_digitized.json)')
    # fallback: the same vector readings typed in
    return dict(F_thr=4.4801, F_thr_g2E=6.26, F_11p5=3.8460, F_min=3.8439, F_min_g2E=11.0, F_unc=0.002,
                left_axis_g2E=6.2326, g2Nmin_hi=3.977, g2Nmin_hi_range=[3.971, 3.983], g2Nmin_thr=4.55,
                source='typed-in fallback of the vector readings (dl_digitized.json absent)')

HBARC = K.hbar * K.c / (1e6 * K.e) * 1e15           # MeV fm
HBAR_GEV_S = K.hbar / (1e9 * K.e)                   # GeV s
G_N = K.G                                           # m^3 kg^-1 s^-2 (CODATA 2022)
M_PL = np.sqrt(K.hbar * K.c / G_N) * K.c**2 / (1e9 * K.e)   # GeV, unreduced
M_PL_RED = M_PL / np.sqrt(8 * np.pi)


def pdg_inputs():
    try:
        import pdg
        api = pdg.connect()
        me = api.get_particle_by_name('e-').mass * 1e3
        mp = api.get_particle_by_name('p').mass * 1e3
        mH = api.get_particle_by_name('H').mass
        rp = None
        for prop in api.get_particle_by_name('p').properties():
            if prop.description.strip() == 'p CHARGE RADIUS':
                rp = float(prop.best_summary().value)
        src = 'PDG 2026 (pdg python package)'
    except Exception as ex:   # fall back to CODATA/PDG values typed in
        me, mp, mH, rp, src = 0.51099895069, 938.27208943, 125.20, 0.84075, f'fallback constants ({ex})'
    return dict(m_e_MeV=me, m_p_MeV=mp, m_H_GeV=mH, r_p_fm=rp, source=src)


def main():
    H = json.load(open(os.path.join(HERE, 'hedgehog.json')))
    HF = json.load(open(os.path.join(HERE, 'hopfion.json')))
    P = pdg_inputs()
    b = H['best']
    a1, Lam = b['a1'], b['Lambda']
    radii = dict(B=b['xrms_B'], M=b['xrms_M'], E=b['xrms_E'], half=b['x_half'])
    radius_names = dict(B='baryon-density rms radius = ANW isoscalar electric rms radius (identical by construction)',
                        M='ANW isoscalar magnetic rms radius', E='energy-density rms radius',
                        half='radius enclosing half the baryon number')
    R = {}
    R['inputs'] = dict(hbarc_MeV_fm=HBARC, **P, M_Planck_GeV=M_PL, M_Planck_reduced_GeV=M_PL_RED,
                       G_N_SI=G_N, hedgehog=dict(a1=a1, Lambda=Lam, **{f'x_{k}': v for k, v in radii.items()}))

    # ------------------------------------------------------------------ 1. Skyrme family scaling
    c0 = {k: a1 * v for k, v in radii.items()}
    sk = dict(formula="M = a1 F_pi/e, R = a2/(e F_pi), M R/(hbar c) = a1 a2/e^2 = c0/e^2 (F_pi in 186-MeV convention)",
              a1=a1, a2=radii, c0=c0, radius_definitions=radius_names)
    # symbolic check of the scaling: substitute r = x/(e F) into the hedgehog energy functional
    Fp, e_, r_, x_ = sp.symbols('F_pi e r x', positive=True)
    f = sp.Function('f')
    dens_r = sp.Rational(1, 8) * Fp**2 * (sp.diff(f(r_), r_)**2 + 2 * sp.sin(f(r_))**2 / r_**2) + \
        sp.Rational(1, 2) / e_**2 * sp.sin(f(r_))**2 / r_**2 * (sp.sin(f(r_))**2 / r_**2 + 2 * sp.diff(f(r_), r_)**2)
    g = sp.Function('g')     # g(x) = f(x/(e F))
    sub = {sp.diff(f(r_), r_): e_ * Fp * sp.Derivative(g(x_), x_), f(r_): g(x_), r_: x_ / (e_ * Fp)}
    integrand = sp.simplify((4 * sp.pi * r_**2 * dens_r).subs(sub) / (e_ * Fp))   # dr = dx/(eF)
    prefactor = sp.simplify(integrand / (4 * sp.pi * (sp.Rational(1, 8) * (x_**2 * sp.Derivative(g(x_), x_)**2 + 2 * sp.sin(g(x_))**2)
                                                   + sp.sin(g(x_))**2 * sp.Derivative(g(x_), x_)**2 + sp.sin(g(x_))**4 / (2 * x_**2))))
    sk['sympy_energy_prefactor'] = str(prefactor)     # expected F_pi/e
    sk['sympy_check_pass'] = bool(sp.simplify(prefactor - Fp / e_) == 0)

    # ANW parameters and our own fit to M_N, M_Delta
    FpiA, eA = 129.0, 5.45
    def model(Fpi, e):
        M = a1 * Fpi / e
        I1 = (2 * np.pi / 3) * Lam / (e**3 * Fpi)          # MeV^-1
        return M, I1, M + 3 / (8 * I1), M + 15 / (8 * I1)
    M_A, I1_A, MN_A, MD_A = model(FpiA, eA)
    # fit: M_D - M_N = 3/(2 I1); M = M_N - 3/(8 I1); F/e = M/a1; e^3 F = (2pi/3) Lam / I1
    MN, MD = 938.9, 1232.0
    I1f = 3 / (2 * (MD - MN)); Mf = MN - 3 / (8 * I1f)
    A = Mf / a1; Bq = (2 * np.pi / 3) * Lam / I1f
    e_fit = (Bq / A)**0.25; F_fit = A * e_fit
    lenA = HBARC / (eA * FpiA)                              # fm per unit x
    RB_A = radii['B'] * lenA; RM_A = radii['M'] * lenA
    proton = dict(
        ANW_parameters=dict(F_pi_MeV=FpiA, e=eA, length_unit_fm=lenA),
        M_classical_MeV=M_A, I1_inv_MeV=1 / I1_A, M_N_model_MeV=MN_A, M_Delta_model_MeV=MD_A,
        R_B_fm=RB_A, R_M_fm=RM_A, R_E_fm=radii['E'] * lenA, R_half_fm=radii['half'] * lenA,
        MR_classical=dict(value=M_A * RB_A / HBARC, formula="c0_B/e^2 = M_cl R_B/(hbar c)"),
        MR_nucleon_model=dict(value=939.0 * RB_A / HBARC, formula="M_N(939 MeV, fitted) * R_B(model)/(hbar c)",
                              target=2.8, tolerance="+-0.05 (2 significant figures of PLAN's '~2.8'; fixed before computing)"),
        MR_data=dict(value=P['m_p_MeV'] * P['r_p_fm'] / HBARC, formula="m_p r_p(charge, PDG 2026)/(hbar c) = r_p/lambda_C",
                     lambda_C_fm=HBARC / P['m_p_MeV']),
        rotor_over_mass=dict(value=(3 / (8 * I1_A)) / M_A, formula="(3/(8 I1))/M_cl = 9 e^4/(16 pi Lambda a1)"),
        own_fit_to_MN_MDelta=dict(M_N=MN, M_Delta=MD, F_pi_MeV=F_fit, e=e_fit,
                                  target=dict(F_pi_MeV=129.0, e=5.45, rel_tol=0.01),
                                  pass_=bool(abs(F_fit / 129 - 1) < 0.01 and abs(e_fit / 5.45 - 1) < 0.01)),
        calibration_radii=dict(R_B_target_fm=0.59, R_M_target_fm=0.92, tol_fm=0.01,
                               pass_B=bool(abs(RB_A - 0.59) <= 0.01), pass_M=bool(abs(RM_A - 0.92) <= 0.01),
                               source="ANW 1983 via secondary sources (PLAN E5)"))
    sk['proton'] = proton

    # semiclassical floor: E_rot/M = 9 e^4/(16 pi Lambda a1) <= rho  ->  e_max, (M R)_min = c0/e_max^2
    floor = {}
    for rho in [0.1, 0.3, 1.0]:
        emax = (16 * np.pi * Lam * a1 * rho / 9)**0.25
        floor[f'rot_over_M_le_{rho}'] = dict(e_max=emax, MR_min_B=c0['B'] / emax**2, MR_min_half=c0['half'] / emax**2)
    sk['semiclassical_floor'] = dict(formula="E_rot/M = 9 e^4/(16 pi Lambda a1) <= rho gives e <= e_max and M R >= c0/e_max^2", **floor)

    # electron
    me = P['m_e_MeV']
    lamC_e = HBARC / me
    el = dict(lambda_C_fm=lamC_e, bounds_fm=dict(LEP=1.1e-4, SEED=1e-3),
              LEP_bound_note=("Schael et al. 2013 (arXiv:1302.3415) Eq. (3.9): r_e < 1.1e-19 m. Model dependent: it converts "
                              "the VV contact-interaction scale (positive interference, electromagnetic coupling strength) "
                              "into a size; it is not a direct form-factor measurement."))
    for bname, Rmax in el['bounds_fm'].items():
        MRreq = me * Rmax / HBARC
        entry = dict(MR_required_max=MRreq, compton_over_R_min=1 / MRreq, log10_compton_over_R=np.log10(1 / MRreq))
        for k in radii:
            e_need = np.sqrt(c0[k] / MRreq)
            Fpi_need = me * e_need / a1
            rot = 9 * e_need**4 / (16 * np.pi * Lam * a1)
            entry[k] = dict(e_min=e_need, e2_min=e_need**2, F_pi_MeV=Fpi_need, eFpi_MeV=e_need * Fpi_need,
                            length_unit_fm=HBARC / (e_need * Fpi_need),
                            rot_over_M=rot, log10_rot_over_M=np.log10(rot),
                            hbar_over_MR=1 / MRreq, naive_loop_parameter_e2_over_16pi2=e_need**2 / (16 * np.pi**2))
        el[bname] = entry
    el['formula'] = ("e^2 >= c0 hbar c/(m_e R_max); F_pi = m_e e/a1; E_rot/M = 9 e^4/(16 pi Lambda a1); "
                     "loop expansion parameter ~ e^2 (action = S0/e^2), equivalently hbar/(M R) = e^2/c0")
    el['failure_factor_vs_floor'] = dict(
        value=floor['rot_over_M_le_1.0']['MR_min_B'] / el['LEP']['MR_required_max'],
        formula="(M R)_min of a semiclassical Skyrme fold (E_rot <= M) / (M R) allowed for the electron (LEP)")
    sk['electron'] = el

    # pion-mass family robustness
    fam = [d for d in H['pion_mass_family'] if 'error' not in d]
    sk['pion_mass_family'] = dict(note="beta = m_pi/(e F_pi); c0 = a1(beta) x_rms(beta)", rows=fam,
                                  c0_B_min=min(d['c0_B'] for d in fam), c0_half_min=min(d['c0_half'] for d in fam))
    R['skyrme'] = sk

    # ------------------------------------------------------------------ 1b. Faddeev-Skyrme hopfion
    c0h = HF['c0_hopf_rms']
    hop = dict(formula=HF['formula'], E_W_ansatz=HF['E_W_ansatz'], R_rms_ward=HF['R_rms_energy_ward'],
               R_ring_ward=HF['R_ring_ward'], c0_hopf_rms=c0h, c0_hopf_ring=HF['c0_hopf_ring'],
               c0_hopf_rms_lit_energy=HF['c0_hopf_rms_with_lit_energy'])
    for bname, Rmax in el['bounds_fm'].items():
        MRreq = me * Rmax / HBARC
        for suffix, cc in [('', c0h), ('_ring', HF['c0_hopf_ring'])]:
            k4 = MRreq / cc
            k2_sqrt = me / (16 * np.sqrt(2) * np.pi**2 * np.sqrt(k4) * HF['E_W_ansatz'])   # MeV
            hop[f'electron_{bname}{suffix}'] = dict(kappa4_max=k4, g2_min=1 / k4, sqrt_kappa2_MeV=k2_sqrt,
                                                    length_unit_fm=HBARC * np.sqrt(k4) / k2_sqrt,
                                                    radius='energy rms' if not suffix else 'ring (n = -e3)')
    R['hopfion'] = hop

    # ------------------------------------------------------------------ 2. pairs
    pairs = {}
    # Demidov-Levkov model (arXiv:1103.0013, 1103.2133): S = (1/g^2) int [ (d phi)^2/2 - V ],
    # V = (1/2)(phi+1)^2 [1 - v W((phi-1)/a)], W(x) = e^{-x^2}(x + x^3 + x^5), a = 0.4, v at delta rho = 0
    a = 0.4
    W = lambda x: np.exp(-x**2) * (x + x**3 + x**5)
    res = minimize_scalar(lambda x: -W(x), bounds=(0.5, 3), method='bounded', options=dict(xatol=1e-12))
    xstar = res.x; v = 1 / W(xstar); phip = 1 + a * xstar
    V = lambda p: 0.5 * (p + 1)**2 * (1 - v * W((p - 1) / a))
    g2MS = quad(lambda p: np.sqrt(max(2 * V(p), 0.0)), -1, phip, limit=400, points=[1.0])[0]
    mminus = 1.0
    mplus = np.sqrt((V(phip + 1e-4) - 2 * V(phip) + V(phip - 1e-4)) / 1e-8)
    dl = dl_readings()
    DL = dict(model="Demidov-Levkov 2011 (1+1)D scalar, V = (1/2)(phi+1)^2[1 - v W((phi-1)/a)], a = 0.4 [read]",
              v_degenerate=v, phi_plus=phip, m_minus=mminus, m_plus=mplus,
              g2_M_S_computed=g2MS, two_g2_M_S_computed=2 * g2MS,
              two_g2_M_S_read_from_axes=f"about 6.2 (axes); the left edge of Fig. 3b (tick labelled 2 g^2 M_S) is at g^2E = "
                                        f"{dl['left_axis_g2E']:.4f} in the vector data",
              F2_exponent_read=dict(at_threshold=dl['F_thr'], at_threshold_g2E=dl['F_thr_g2E'], at_g2E_11p5=dl['F_11p5'],
                                    minimum=dl['F_min'], minimum_at_g2E=dl['F_min_g2E'],
                                    uncertainty=f"+-{max(dl['F_unc'], 0.002):.3f} (vector path, axes calibrated on ticks)",
                                    source="arXiv:1103.0013v2 Fig. 3b upper panel (g^2 N = 0) [read, " + dl['source'] + "]",
                                    version1_eye_reading=dict(at_threshold=4.45, at_g2E_11p5=3.93,
                                                              note="3.93 was wrong by -0.085, outside its stated +-0.05")),
              g2Nmin_classical_read=dict(high_energy=dl['g2Nmin_hi'], high_energy_range=dl['g2Nmin_hi_range'],
                                         near_threshold=dl['g2Nmin_thr'],
                                         source="arXiv:1103.2133v2 Fig. 7b, delta rho -> 0 [read, vector path]"))
    F2 = dl['F_min']            # high-energy plateau (minimum of the plotted curve)
    F_thr = dl['F_thr']
    g2Nmin = dl['g2Nmin_hi']
    DL['kappa_suppression_per_pair_quantum'] = dict(
        value=[F2 / (2 * g2MS), F_thr / (2 * g2MS)],
        formula="P ~ exp(-F/g^2) = exp(-kappa N_pair), N_pair = 2 M_S/m_- = 2 g2MS/g^2; kappa = F/(2 g^2 M_S)")
    DL['Nmin_over_Npair'] = dict(value=g2Nmin / (2 * g2MS), formula="g^2 N_min / (2 g^2 M_S/m_-)")
    unsup = {}
    for Ptarget in [0.1, np.exp(-1), 0.5]:
        g2 = F2 / np.log(1 / Ptarget)
        unsup[f'P={Ptarget:.3g}'] = dict(g2=g2, M_S_over_m=g2MS / g2, N_pair=2 * g2MS / g2)
    DL['coupling_for_unsuppressed_two_particle_production'] = dict(
        formula=f"exp(-F_min/g^2) = P  ->  g^2 = F_min/ln(1/P), F_min = {F2:.3f} (high-energy plateau)", rows=unsup,
        caveat="extrapolates the leading semiclassical exponent to g^2 = O(1), where prefactors and higher orders are "
               "uncontrolled: indicative only")
    pairs['demidov_levkov'] = DL
    # phi^4 (SEED model A) in the same language: S = (1/g^2) int[(1/2)(d phit)^2 - (m^2/8)(phit^2-1)^2], g^2 = 2 lambda/m^2
    pairs['phi4'] = dict(
        convention="V = (lambda/4)(phi^2 - v^2)^2, m^2 = 2 lambda v^2, phi = v phit; S = (1/g^2) S0 with g^2 = 1/v^2 = 2 lambda/m^2",
        M_kink_over_m=dict(value_times_g2=2.0 / 3.0, formula="M_kink = m^3/(3 lambda) -> M/m = 2/(3 g^2)"),
        N_pair_times_g2=4.0 / 3.0,
        DSV_units_note="DSV units lambda = v = 1 (m = sqrt 2) have g^2 = 1, so N*lambda in those units equals g^2 N here",
        scaling_argument=("Classical solutions depend on (E, N) only through g^2 E and g^2 N (field rescaling phi = phit/g removes g "
                          "from the field equation); so if classical pair creation exists at all its lower boundary is "
                          "N_min = n0/g^2 with n0 a pure number of the classical theory, N_min ~ 1/lambda."))
    # E1e combination (PLAN E7 "Pairs"). Reconciliation: E1 finished after version 1 of this script ran.
    # e1e_results.json lists the smallest classical producers re-run at dx = 0.05; N = E/m (preregistered) and
    # N_lin (linear-quanta count). In E1 units N lambda/m^2 = E~/(2 sqrt2) and phi0^2 = m^2/(2 lambda), g^2 = 2 lambda/m^2.
    e1e = None
    if os.path.exists(E1_RESULTS):
        try:
            import hashlib
            raw = open(E1_RESULTS, 'rb').read()
            e1 = json.loads(raw)
            rep = [r for r in e1['gaussian_packets']['dx0.05_reproduction_of_smallest_producers'] if r.get('reproduced')]
            NE = min((2.0 / 3.0) * r['E_over_2M'] for r in rep)           # N = E/m in units of m^2/lambda
            NL = min(r['N_lin'] / 2.0 for r in rep)                        # N_lin/phi0^2 -> N_lin lambda/m^2
            e1e = dict(file='../E1_phi4/e1e_results.json', sha256_16=hashlib.sha256(raw).hexdigest()[:16],
                       N_min_lambda_over_m2=dict(N_E=NE, N_lin=NL, E1_implication_c=e1['implication']['c']),
                       g2_N_min=dict(N_E=2 * NE, N_lin=2 * NL), g2_N_pair=4.0 / 3.0,
                       Nmin_over_Npair=dict(N_E=2 * NE / (4 / 3), N_lin=2 * NL / (4 / 3)),
                       g2_for_classical_pair_from_2_quanta=dict(N_E=NE, N_lin=NL),
                       lambda_over_m2_for_2_quanta=dict(N_E=NE / 2, N_lin=NL / 2),
                       note=("upper bounds on the true classical minimum (scanned sets only); classical production from "
                             "N <= 2 quanta needs g^2 >= g^2 N_min/2. E1 is reconciled separately; numbers as read now."))
        except Exception as ex:
            e1e = dict(error=str(ex))
    pairs['E1e_phi4'] = e1e if e1e is not None else "E1_phi4/e1e_results.json not present; E1e not used, scaling derived analytically"
    pairs['E1e_input'] = 'used (see E1e_phi4)' if (e1e and 'error' not in e1e) else 'not used'
    # QED Breit-Wheeler
    alpha = K.fine_structure
    re_fm = alpha * HBARC / me
    def sigBW(beta):   # Breit-Wheeler total cross section / (pi r_e^2), beta = electron speed in CM
        return 0.5 * (1 - beta**2) * ((3 - beta**4) * np.log((1 + beta) / (1 - beta)) - 2 * beta * (2 - beta**2))
    bb = np.linspace(1e-4, 0.9999, 200001)
    sv = sigBW(bb); ib = np.argmax(sv)
    pairs['QED_breit_wheeler'] = dict(
        formula="sigma = (pi r_e^2/2)(1-b^2)[(3-b^4) ln((1+b)/(1-b)) - 2b(2-b^2)], r_e = alpha hbar c/(m_e c^2)",
        r_e_fm=re_fm, sigma_max_over_pi_re2=float(sv[ib]), beta_at_max=float(bb[ib]),
        sqrt_s_at_max_over_2me=float(1 / np.sqrt(1 - bb[ib]**2)),
        sigma_max_mb=float(sv[ib] * np.pi * re_fm**2 * 10.0),   # 1 fm^2 = 10 mb
        scaling="sigma ~ alpha^2/m_e^2: power-law (perturbative) in alpha, no exp(-c/alpha) factor",
        hypothetical_fold_suppression=dict(
            note=("illustration only: if the electron were a semiclassical fold with DL-like F ~ 3.8; depends on the "
                  "coupling identification: g^2 = alpha, or g^2 = e^2 = 4 pi alpha (the loop-counting coupling of QED)"),
            F_used=F2,
            exp_minus_F_over_alpha_log10=float(-F2 / alpha / np.log(10)),
            exp_minus_F_over_4pialpha_log10=float(-F2 / (4 * np.pi * alpha) / np.log(10))))
    R['pairs'] = pairs

    # ------------------------------------------------------------------ 3. vacuum tension
    Mpc_m = 3.0856775814913673e22
    def rho_crit_GeV4(H0):     # 3 H0^2 Mpl_red^2 in natural units
        H0_GeV = H0 * 1e3 / Mpc_m * HBAR_GEV_S
        return 3 * H0_GeV**2 * M_PL_RED**2
    vac = {}
    rows = {'Planck2018_TTTEEE_lowE_lensing': (67.36, 0.54, 0.6847, 0.0073), 'PLAN_rounded': (67.4, None, 0.685, None)}
    for name, (H0, dH, OL, dOL) in rows.items():
        rho = OL * rho_crit_GeV4(H0)
        d = dict(H0=H0, Omega_L=OL, rho_crit_GeV4=rho_crit_GeV4(H0), rho_L_GeV4=rho, rho_L_quarter_meV=rho**0.25 * 1e12,
                 rho_L_meV4=rho * 1e48)
        if dH:
            d['rel_unc_uncorrelated'] = float(np.hypot(2 * dH / H0, dOL / OL))
        vac[name] = d
    # Planck's own Omega_L h^2 = 0.3107 +- 0.0082 and Lambda = 4.24e-66 eV^2 [read, arXiv:1807.06209 Eq. (15) text]
    h2rho = rho_crit_GeV4(100.0)
    vac['Planck_OmegaLh2'] = dict(Omega_L_h2=0.3107, unc=0.0082, rho_L_GeV4=0.3107 * h2rho, rel_unc=0.0082 / 0.3107)
    Lam_eV2 = 4.24e-66
    vac['Planck_Lambda'] = dict(Lambda_eV2=Lam_eV2, rho_L_GeV4=Lam_eV2 * 1e-18 * M_PL_RED**2,
                                formula="rho_L = Lambda/(8 pi G) = Lambda Mpl_red^2",
                                Lambda_over_mPl2_quoted=2.846e-122, Lambda_over_mPl2_ours=Lam_eV2 * 1e-18 / M_PL**2)
    rhoL = vac['Planck2018_TTTEEE_lowE_lensing']['rho_L_GeV4']
    fpi = 130.2 / np.sqrt(2) / 1e3
    v_ew = 246.22
    scales = {
        'f_pi^4 (f_pi = 92.07 MeV = 130.2/sqrt2)': fpi**4,
        'f^4 of the ANW Skyrme fit (f = F_pi/2 = 64.5 MeV)': (0.0645)**4,
        'm_e^4': (me / 1e3)**4,
        'v_EW^4 (v = 246.22 GeV)': v_ew**4,
        'Higgs potential depth m_H^2 v^2/8': P['m_H_GeV']**2 * v_ew**2 / 8,
        'M_Pl^4 reduced (2.435e18 GeV)': M_PL_RED**4,
        'M_Pl^4 unreduced (1.221e19 GeV)': M_PL**4,
    }
    vac['ratios_scale4_over_rhoL'] = {k: dict(scale4_GeV4=s4, ratio=s4 / rhoL, log10=np.log10(s4 / rhoL)) for k, s4 in scales.items()}
    vac['targets'] = dict(rho_L=dict(target=2.5e-47, tol_rel=0.02, ours=rhoL, pass_=bool(abs(rhoL / 2.5e-47 - 1) < 0.02)),
                          rho_L_quarter_meV=dict(target=2.24, tol=0.01, ours=rhoL**0.25 * 1e12,
                                                 pass_=bool(abs(rhoL**0.25 * 1e12 - 2.24) < 0.01)),
                          f_pi4=dict(target='about 3e42', ours=fpi**4 / rhoL),
                          ew=dict(target='about 1e56', ours=v_ew**4 / rhoL),
                          planck=dict(target='about 1e123', ours=M_PL**4 / rhoL, note='unreduced; reduced gives ~1.4e120'))
    R['vacuum'] = vac

    # ------------------------------------------------------------------ 4. Weinberg-Witten selection rule
    # Brick-wall frame: a rotation by theta about q multiplies <h,p+q|O_{j,m}|h,p> by exp(2 i h theta) and the
    # operator component by exp(i m theta); a non-zero matrix element needs |m| = 2|h| <= j_max.
    # Conserved 4-vector current: spatial-rotation content j <= 1; symmetric 2-tensor T_mu nu: j <= 2.
    ww = {}
    for h in [0, 0.5, 1, 1.5, 2]:
        ww[str(h)] = dict(charge_under_covariant_current_allowed=bool(2 * h <= 1),
                          energy_under_covariant_Tmunu_allowed=bool(2 * h <= 2))
    R['weinberg_witten'] = dict(
        rule="non-zero forward matrix element needs 2|h| <= j_max; j_max = 1 (J^mu), 2 (T^mu nu)",
        table=ww,
        source="Weinberg & Witten, PLB 96, 59 (1980) (original not read); argument read in Porrati arXiv:0804.4672 Sec. 2",
        statements=[
            "A theory with a Lorentz-covariant conserved current J^mu has no massless particle of |h| > 1/2 carrying non-zero charge Q = int J^0.",
            "A theory with a Lorentz-covariant conserved T^mu nu has no massless particle of |h| > 1 (its forward matrix element must be p^mu p^nu/E by the equivalence principle).",
            "Both hold for composite and elementary particles alike; GR and supergravity evade them because the graviton/gravitino T^mu nu is not gauge invariant/Lorentz covariant.",
            "A neutral composite photon (|h| = 1, Q = 0) is not excluded; a composite graviton from a Lorentz-covariant matter sector with covariant conserved T^mu nu is."])
    with open(os.path.join(HERE, 'results_raw.json'), 'w') as fh:
        json.dump(R, fh, indent=1, default=float)
    # ------------------------------------------------------------------ printed checks
    pr = sk['proton']
    print("SKYRME SCALING")
    print(f"  a1 = {a1:.5f}; a2 (B, M, E, half) = " + ", ".join(f"{radii[k]:.5f}" for k in radii))
    print(f"  c0 (B, M, E, half) = " + ", ".join(f"{c0[k]:.3f}" for k in c0))
    print(f"  sympy energy prefactor = {sk['sympy_energy_prefactor']}  (pass={sk['sympy_check_pass']})")
    print(f"  ANW: M_cl={pr['M_classical_MeV']:.1f} MeV, M_N={pr['M_N_model_MeV']:.1f}, M_D={pr['M_Delta_model_MeV']:.1f}, "
          f"R_B={pr['R_B_fm']:.4f} fm (0.59), R_M={pr['R_M_fm']:.4f} fm (0.92)")
    print(f"  own fit: F_pi={F_fit:.2f} MeV, e={e_fit:.4f} (ANW 129, 5.45)")
    print(f"  proton MR: classical {pr['MR_classical']['value']:.3f}, nucleon-model {pr['MR_nucleon_model']['value']:.3f} (2.8), "
          f"data r_p/lambda_C {pr['MR_data']['value']:.3f};  E_rot/M = {pr['rotor_over_mass']['value']:.4f}")
    for kk, vv in floor.items():
        print(f"  floor {kk}: e_max={vv['e_max']:.3f}, (MR)_min(B)={vv['MR_min_B']:.3f}")
    for bname in ['LEP', 'SEED']:
        E = el[bname]
        print(f"  electron {bname}: (MR)_max={E['MR_required_max']:.3e}, lambda_C/R >= {E['compton_over_R_min']:.3e}; "
              f"e_min(B)={E['B']['e_min']:.4g}, F_pi={E['B']['F_pi_MeV']:.4g} MeV, E_rot/M={E['B']['rot_over_M']:.3e}, "
              f"e^2/16pi^2={E['B']['naive_loop_parameter_e2_over_16pi2']:.3e}")
    print(f"  pion-mass family c0_B min over beta<=16: {sk['pion_mass_family']['c0_B_min']:.2f}")
    print("HOPFION")
    print(f"  E_W(ansatz)={HF['E_W_ansatz']:.4f}, R_rms={HF['R_rms_energy_ward']:.4f}, c0_hopf={c0h:.1f}; "
          f"electron LEP: kappa4 <= {hop['electron_LEP']['kappa4_max']:.3e}, g^2 >= {hop['electron_LEP']['g2_min']:.3e}")
    print("PAIRS")
    print(f"  DL model: v={v:.5f} (paper ~0.75), phi+={phip:.4f}, 2 g^2 M_S = {2*g2MS:.4f} (axes ~6.2), m+={mplus:.3f}")
    print(f"  DL readings ({dl['source']}): F(threshold, g^2E={dl['F_thr_g2E']:.2f}) = {F_thr:.4f}, F(11.5) = {dl['F_11p5']:.4f}, "
          f"F_min = {F2:.4f}; g^2 N_min = {g2Nmin:.4f} (near threshold {dl['g2Nmin_thr']:.3f}); left axis g^2E = {dl['left_axis_g2E']:.4f}")
    print(f"  kappa = F/N_pair = {DL['kappa_suppression_per_pair_quantum']['value']}; N_min/N_pair = {DL['Nmin_over_Npair']['value']:.3f}")
    for kk, vv in unsup.items():
        print(f"  {kk}: g^2 = {vv['g2']:.3f}, M_S/m = {vv['M_S_over_m']:.3f}")
    if e1e and 'error' not in e1e:
        print(f"  E1e (phi^4): g^2 N_min <= {e1e['g2_N_min']['N_E']:.3f} (N = E/m) / {e1e['g2_N_min']['N_lin']:.3f} (N_lin); "
              f"N_min/N_pair <= {e1e['Nmin_over_Npair']['N_E']:.2f} / {e1e['Nmin_over_Npair']['N_lin']:.2f}; "
              f"2 quanta classically need g^2 >= {e1e['g2_for_classical_pair_from_2_quanta']['N_E']:.3f} / "
              f"{e1e['g2_for_classical_pair_from_2_quanta']['N_lin']:.3f}")
    else:
        print(f"  E1 input: {pairs['E1e_input']}")
    hfs = pairs['QED_breit_wheeler']['hypothetical_fold_suppression']
    print(f"  Breit-Wheeler: sigma_max = {sv[ib]:.4f} pi r_e^2 = {pairs['QED_breit_wheeler']['sigma_max_mb']:.1f} mb at sqrt(s) = "
          f"{1/np.sqrt(1-bb[ib]**2):.3f} x 2 m_e; fold-like suppression would be 10^{hfs['exp_minus_F_over_alpha_log10']:.1f} "
          f"(g^2 = alpha) or 10^{hfs['exp_minus_F_over_4pialpha_log10']:.1f} (g^2 = 4 pi alpha)")
    print("VACUUM")
    for kk in ['Planck2018_TTTEEE_lowE_lensing', 'PLAN_rounded', 'Planck_OmegaLh2', 'Planck_Lambda']:
        print(f"  {kk}: rho_L = {vac[kk]['rho_L_GeV4']:.4e} GeV^4")
    print(f"  (rho_L)^(1/4) = {rhoL**0.25*1e12:.4f} meV; Lambda/mPl^2 ours {vac['Planck_Lambda']['Lambda_over_mPl2_ours']:.4e} (quoted 2.846e-122)")
    for kk, vv in vac['ratios_scale4_over_rhoL'].items():
        print(f"  {kk:55s} ratio = {vv['ratio']:.3e}")
    print("WEINBERG-WITTEN helicity table (charged under J allowed?, carries covariant T allowed?)")
    for h, vv in ww.items():
        print(f"  |h|={h}: {vv['charge_under_covariant_current_allowed']}, {vv['energy_under_covariant_Tmunu_allowed']}")


if __name__ == '__main__':
    main()
