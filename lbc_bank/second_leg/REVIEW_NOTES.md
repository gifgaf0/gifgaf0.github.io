# Review notes: adversarial review of the second leg (before checkpoint assembly)

Reviewer task: find errors in everything under `lbc_bank/second_leg/` (code cc2d.py, cc2d_hydro.py, cc2d_melt.py,
cc3d.py, cc_loss.py, xcheck2d.py, xcheck3d.py; the seven results JSONs; the seven NOTES files) against the dispatch
plaintext (sections 1-3, 6, embed E4 skeleton) and the leg's SPEC. Units hbar = m = R = 1, mean density 1.
Numbers are repr (full precision). Nothing in this folder was edited except this file; one bytecode file that my
own import created (`__pycache__/xcheck2d.cpython-311.pyc`) was deleted again. No dispatch code was executed.
Reviewer scripts and outputs live in the scratch folder `work/review/` (rv_scan.py, rv_loss.py, rv_melt_xc.py,
rv_qa_xc.py, rv_fs_xc.py, rv_fold_xc.py and their JSON outputs); they are not part of the deliverable.

## 1. Verdict

* No BLOCKER. Every schema quantity of E4 is present in a results file, with the dispatch definition, and every
  numeric schema quantity has now been reproduced by at least one code path independent of the producing one
  (Sec. 7). The numerics are sound to about 1e-7 relative or better everywhere.
* The remaining risk of a comparator MISS is concentrated in reading choices of Q-D (band units, R3 with or
  without 1/F2) and, to a lesser degree, the branch-end definition. These are listed as MAJOR/MINOR below with the
  size of the effect, so the assembler can add the alternatives as extra (CC-only) keys.
* One hygiene defect must be fixed before scanning/committing: a stale bytecode file in `__pycache__/` scans HIT.

## 2. Findings (most severe first)

1. **MAJOR** hygiene: `lbc_bank/second_leg/__pycache__/cc2d.cpython-311.pyc` (written 14:45 by an agent that imported cc2d) contains a non-numeric T1 pattern (base-list index 9, twice; bytecode noise, not content). If the folder is added wholesale it will be committed and the E2 scan reports HIT. Fix: delete `__pycache__/` before scanning and committing, and run any later imports with PYTHONDONTWRITEBYTECODE=1 (a fresh import of xcheck2d also produced a pyc with a hit at index 10; I removed that one, it was mine).

2. **MAJOR** Q-D reading risk, `loss.band_orders` units: the leg reports the band as absolute headline values log10(l/L_prop) = best + factor orders = [-41.169440470745286, -38.38554633554141]. The dispatch sentence lists the band next to 'orders recovered' and 'headline', so the band could equally be meant in recovered orders: [0.791463854742054, 3.57535798994593] (already stored in qd_results.json alternatives.band_recovered_orders). The two readings differ by 41.96090432548734, so a mismatch is a certain MISS. I consider the headline reading slightly more natural ('band' of where l lands), but recommend carrying `band_orders_recovered` as an extra key in the checkpoint and stating the choice in the return note.

3. **MAJOR** Q-D reading risk, R3 'closure literal with M -> c_T/c2': the leg multiplies by (M_new/phi^2)/F2. Read literally, the closure l = gamma M tau xi / P contains no F, giving M_new/phi^2 = 6.234118601062868 (0.7947750602599088 orders). This moves the band upper edge from -38.38554633554141 to -39.14689297080844 (delta 0.76, > 0.1 tolerance). Both values are in qd_results.json (alternatives.band_orders_with_R3_without_F2). Including 1/F2 is defensible (the four readings are four versions of the same re-evaluation, in which only branch 2 radiates) but not the only natural reading; carry the alternative as an extra key.

4. **MINOR** Q-D `loss.eq3_coefficient` = 136027.3099135106 uses c_T = 7.68 (the dispatch's stated dynamical mean), c_kappa(q = 0.15) and the smaller F2 (q = 0.3). This is the most natural reading (item 3 names only 'your 3D c_kappa' and 'the smaller F2' as own inputs). Sensitivity: own mean transverse speed 7.846621816361291 gives 148221.81093728365 (+9.0 %, would MISS at 5 %); own cT_min gives 141007.24761122008 (+3.7 %). Keep, but record the alternatives (already in qd_results.json eq3_alternatives).

5. **MINOR** Q-D `loss.xi_req_main_m` uses the best point/channel (p4, O) and M = phi^2 (the old closure), then divides by the main factor: [22667.45969688186, 22794.105531318575] m (ascending; the element order differs from 'q = 0.15 first' but the two elements differ by only 0.56 %, inside the 10 % tolerance). Using M_new in the closure instead would divide by a further 6.234118601062868 (MISS). M = phi^2 is the natural reading because the main factor already carries the Mach dependence.

6. **MINOR** Branch end reading: `melting.branch_end_g` = 12.326704359054563 is the fold of the a*-branch (minimum of e(a) disappears). The crystal stops being a local minimum earlier, against long-wavelength density/strain modulations: BdG omega^2 < 0 first at g = 12.383498764038086 (|q|a/2pi = 0.03), q -> 0 estimate 12.39501508076986. The difference (0.068) is inside the 0.1 tolerance, but the margin against a first leg that used the dynamical criterion, or a coarse continuation step, is only about 0.03. The fold reading matches 'the g at which the crystal branch ends'; both values are recorded in qc_results.json; keep, and add the dynamical onset as an extra key.

7. **MINOR** c1 mislabel near the branch end (internal consistency, not a schema key): in cc2d.bdg the upper longitudinal mode '1' is the max-F mode among even modes 2-4. For 36 Q-C branch states with g in [12.383499145507812, 12.4] this picks the gapped optic mode at |q|a/2pi = 0.075 and 0.10 (e.g. g = 12.4: omega = 3.967985445587842 and 4.491511896648385 instead of the gapless 2.2849 and 3.0517; label1_is_second_even = False there). Their c1 jumps from 7.5071490327166694 (g = 12.45) to 10.7862703916574 (g = 12.4). c2, cT, F2, S2 and Z21 (taken at 0.05 where the label is correct) are unaffected, and every schema state (all Q-A points, Lambda_c, the ratio maximum) has label1_is_second_even = True at all four q. Do not quote branch-table c1 for g <= 12.4; a gaplessness criterion (omega proportional to q) would be the correct selector.

8. **MINOR** `2d.22.static_resid_max` / `fsum_resid_max` are maxima over the four a1 q points only. Including the 30-degree q point (also one of 'your q points' at g = 22) raises static_resid_max from 1.7859331850001767e-15 to 4.70800345396941e-15 (f-sum unchanged at 5.2653870924998635e-11). Irrelevant for the '<= 1e-4' rule; for literal completeness quote the max over all five q.

9. **MINOR** f_s reading: the dispatch asks for f_s 'from the phase-twist energy'; the schema values (2d.*.f_s and hydro_g22.f_s) are the linear-response limit 1 - (2/N)<d psi|L^-1|d psi>, which is the exact k -> 0 limit of the twist energy. The finite-twist extrapolations agree to <= 6.8e-7 relative (max at g = 13), and my independent dense LR values agree to <= 1.7e-8 (Sec. 7). No numeric consequence; mention in the checkpoint note.

10. **MINOR** `melting.any_c2_ge_cT` in qc_results.json covers the 81 step-kernel branch states with a real spectrum. The checkpoint boolean must be the OR over every crystal state of the leg: Q-A points incl. g6 (max c2/cT 0.7742647962736801 at g = 13; g6 0.3273831248199792), 3D (c2/cT_min 0.06072196648182799, also at the own optimum), cross-check states. All are False, so False stands; say so in the note.

11. **MINOR** 3D transverse speeds: cT_max = 8.04006531797928 is omega/q of the y-polarised branch along x at q = 0.15, i.e. just above its avoided crossing (q about 0.105) with the gapped A/B relative-phase mode (omega about 0.84). Level repulsion lifts it above its small-q value 8.026303479547606 (q = 0.02; in-plane partner Tx along y: 8.02602996437834), by +0.17 %; just below the crossing (q = 0.1) the same branch sits at 8.02250119648918. Correctly the gapless branch was taken (frequency ordering would give 5.62); the dispatch asks for q = 0.15 values, so keep. LSQ vs point speeds and c_kappa(q = 0.15) vs q -> 0 change the 3D keys by <= 0.33 % and 0.015 % respectively.

12. **MINOR** 3D given lattice is pre-stressed in this functional: the leg's own fixed-density optimum is at a = 1.3843727138396495, c = 2.258452154195673 (-0.115 %, -0.051 %). Consistent with that, the z-polarised transverse speed along x (7.762202290069347 at q = 0.02) and the x-polarised one along z (7.7548897229486045) differ by 9.4e-4, whereas a stress-free hexagonal crystal gives equal speeds (C44) up to the normal-density anisotropy, which predicts only -3.3e-5 (opposite sign) from f_s basal 0.0030815203840829364 vs axial 0.003016319145241142. Not an error (the dispatch asks for the given lattice); useful for post-comparison diagnosis. Also note the dispatch's c_T = 7.68 lies 0.9 % below this leg's cT_min 7.7493459895352235, so no mean over this leg's transverse speeds can equal it: the first leg's transverse speeds or their averaging differ by about 1-2 % (inside the 3 % tolerance for cT_min/cT_max, but watch them).

13. **MINOR** QA_NOTES.md states 'The task text describes the crystal below g ~ 14.737 as a metastable branch'. Neither the dispatch nor the SPEC says this (they only mention the uniform roton instability as a sanity value). Documentation inaccuracy only.

14. **MINOR** Q-D drag: the AP comparison rests on second-hand quotations (the Q-D agent's fetch of the paper was blocked; confirm that its task allowed web access). Independent support: the Bogoliubov contact-vertex reduction F = 4 pi n b^2 m v^2 (1 - c^2/v^2)^2 has the correct classical limit v >> c, F -> n sigma m v^2 with the s-wave cross-section sigma = 4 pi b^2, which fixes the prefactor, hence C = 1/(4 pi) = 0.07957747154594767 for V(q) = int d^3r exp(-iq.r) V(r). My own derivation (Sec. 5) gives the same C.

15. **MINOR** Portability/robustness: all instruments hard-code the session scratch path as WORK (caches not committed; the scripts recreate the folder, so a re-run works but recomputes everything). cc2d.pcg has no breakdown guard (documented in QC_NOTES; worked around in cc2d_melt) and cc2d.superfluid_fraction seeds the twist with the wrong sign of the first-order correction (documented in QA_PRIME_NOTES; I re-derived the sign: with |G + k|^2 the minimiser is psi0 + i k L^-1 d_x psi0; harmless, Newton converges to the same state).

16. **MINOR** Q-A schema a* is the bounded-Brent value (jitter <= 3.5e-8 relative) while hydro, Q-C and both cross-checks use the envelope-derivative root. Negligible against the 0.5 % tolerance; optional to switch.

## 3. (a) Schema definitions vs dispatch text (reading choices)

| key group | definition used | dispatch text | most natural? | sensitivity |
|---|---|---|---|---|
| 2d.*.astar | bounded Brent on e(a) = E_cell/A at rho = 1 | a optimised at fixed rho (min energy per area) | yes | root vs Brent <= 3.5e-8 |
| 2d.*.c2/cT/c1 | LSQ through origin, q parallel to a1, abs(q) = f 2pi/a*, f in {0.03,0.05,0.075,0.10}; T = mirror-odd, 2/1 = lower/upper mirror-even | same | yes | - |
| 2d.*.F2/Z21/S2 | at f = 0.05; F = omega Z/(N_cell q^2/2), N_cell = sqrt(3)/2 a*^2; S denominator = full-spectrum sum of 2Z/omega | same | yes | S vs chi_CG <= 5e-15 |
| 2d.22.cT_30deg_kf005 | omega_T/abs(q), abs(q)a/2pi = 0.05 at 30 deg (mirror line), T = mirror-odd | same | yes | - |
| 2d.22.*resid_max | max over the four a1 q | 'over your q points' | mostly | 30-deg point: static 4.708e-15 (Finding 8) |
| 2d.*.f_s | linear-response limit at fixed cell | 'from the phase-twist energy' | equivalent | <= 6.8e-7 rel (Finding 9) |
| hydro_g22.* | e(rho, eps) = E_cell/A_eps, cell rows (I+eps)a_i, N_cell = rho A_eps; mu = (1/4) d2e/ds2; gamma = d2e/drho deps_xx; f_s LR | same formulas | yes | q -> 0 BdG agreement ~2e-7 confirms conventions incl. sign of gamma |
| 3d.c2, cT_min/max | omega/q at q = 0.15; cT over x,y,z and both polarisations; gapless branch | 'Report the q = 0.15 values' | yes | LSQ: <= 0.33 % |
| 3d.*_basal_q015 | q = 0.15 along x; F with N_cell = primitive volume | same | yes | - |
| 3d.c_kappa | (V/chi_static)^(1/2), chi = 2 <s, A^-1 s> per cell at q = 0.15 along x | (vol/chi_static)^(1/2) per unit density | yes | q -> 0: 0.015 % |
| melting.Lambda_c/Lambda_u/energy_crossing | roots of g(mu_c - eps_c) - mu_c^2/(2 pi) and eps_c - pi g/2, fresh a* per evaluation | same | yes | - |
| melting.ratio_at_Lambda_c, F2_at_Lambda_c | LSQ speeds; F2 at 0.05 | same | yes | - |
| melting.ratio_max_metastable | max over real-spectrum states from Lambda_c down to the branch end | 'along the metastable continuation' | yes | restricting to g < energy crossing: 0.7777936379611172 (delta 0.0099) |
| melting.branch_end_g | fold of the a*-branch | 'the g at which the crystal branch ends' | yes | dynamical onset 12.395 (Finding 6) |
| melting.any_c2_ge_cT | c2 >= cT over computed states | same | yes | must OR over all tasks (Finding 10) |
| loss.drag_prefactor_3d_coeff | C = 1/(4 pi) with V(q) = int exp(-iq.r) V | coefficient in F_d = C rho F v^-2 int q^3 abs(V)^2 dq | yes | symmetric FT convention would give 2 pi^2 |
| loss.v467_* | max/min over 4 points x 3 channels of log10(gamma phi^2 T xi/P / L_prop) | same | yes | - |
| loss.main_* | factor [S(phi^2)/S(7.68/c2)]/F2, F2 at q = 0.15 and 0.3 | same | yes | LSQ c2: 4e-6 orders |
| loss.band_orders | headline values, 4 readings x 2 F2, R3 with 1/F2, R4 = R1/(c_kappa/c_s)^4 | 'band over the four readings' | ambiguous | Findings 2, 3 |
| loss.xi_req_main_m | L_prop P/(gamma phi^2 tau) at (p4, O) divided by the main factor | same | yes | Finding 5 |
| loss.eq3_coefficient | 16 pi tau (7.68/c_kappa)^4 / F2_min | same; c_T unspecified there | yes | Finding 4 |
| loss.eq4_bound | 1/(2 gamma^2) | same | yes | - |

SPEC vs dispatch: no disagreement that changes a number (S denominators differ in form only; identical to <= 1e-14).

## 4. (b) Internal consistency

* BdG vs static hydro at g = 22: polynomial-in-q^2 extrapolation of the BdG per-q data (my fit, 3 terms) gives c2(0) = 1.8167721641165717, c1(0) = 11.210455639810325, cT(0) = 5.812445978747623, F2(0) = 0.05181183934757882, S2(0) = 0.6753842234369021 against hydro 1.8167718025575543, 11.210456986512957, 5.812445879721162, 0.051811930464356795, 0.6753841581964672 (relative <= 2e-7; F2 and S2 <= 2e-6). The BdG static response chi/A(q -> 0) = 0.023242217406313537 vs hydro M/(rho(alpha M - gamma^2)) = 0.02324224864274319 (1.3e-6). Recomputing a, b, c+-, F-, the static share from the stored moduli reproduces every hydro output exactly.
* f_s: twist vs LR <= 6.8e-7 relative at every Q-A point (x and y), isotropy <= 4e-14; hydro f_s vs Q-A f_s 1.6e-8 (a* offset).
* Cross-checks: xcheck2d (supercell, square cut, full non-Hermitian BdG) vs cc2d <= 2.2e-7 on every overlapping quantity; xcheck3d (orthorhombic cell, box cut, L-Cholesky) vs cc3d <= 2.6e-7 (c2/Z21; eigh rounding, explained). Both cross-check agents read the same SPEC, so they cannot catch a shared misreading of the dispatch; Sec. 3 addresses that.
* Sum rules: 2D f-sum <= 1.8e-10, static <= 5e-15 (Q-A); Q-C <= 5.0e-8 except within ~1e-4 of the q = 0.03 onset (9.96e-5, conditioning as omega_2 -> 0; not a schema state); 3D f-sum <= 6.4e-11, static <= 5.7e-15. Weight sums at 0.05: F2 + F1 = 0.98-0.9994, S2 + S1 = 0.99964-0.999999 (rest in gapped modes), FT ~ 1e-31.
* Convergence tables (N, Kcut in 2D; K = 30..50 in 3D; N = 48/64/80 and Kcut 60/80/100 for the melting headline states) all show changes <= 3e-7 (2D) and <= 2.2e-8 between K = 40 and 50 (3D).
* Trends along g (128 branch states + Q-A): a*, eps_c, contrast, d2e/da2, lambda_sym, cT, F2, Z21, f_s are monotonic. mu_c and f(g) turn over below g ~ 12.4 near the fold (physical). c2 peaks near g = 12.75-12.8 and falls toward the long-wavelength instability (omega_2/q increases with q there: anomalous dispersion, physical). S2 is non-monotonic with a minimum near g = 22; consistent with the hydro estimate S- ~ 1 - (alpha - gamma^2/M)/(alpha - 2 gamma + M/rho_n). Only c1 jumps (Finding 7).
* Melting roots vs branch table: f changes sign between 13.0 (-0.059544381069457586) and 13.25 (0.3033124114385828); eps_c - pi g/2 between 12.55 (0.0027975886897344537) and 12.6 (-0.004244532874182028); Lambda_u = mu_c(Lambda_c)/pi reproduced; c2/cT and F2 at Lambda_c interpolate between the neighbours; the ratio maximum (12.717222586536337) lies between grid points 12.7 and 12.75 whose values bracket it.
* Boolean: c2 < cT at all 81 real-spectrum branch states (max 0.7877276809284883), all Q-A points, g6, 3D.

## 5. (c) Q-D: drag coefficient and loss arithmetic

Own derivation. H_int = int V(r - vt) n(r); delta n(q, t) = chi(q, q.v) V(q) exp(-i q.v t). The force F = int d^3r grad V(r - X) delta n(r) becomes, after symmetrising q -> -q with chi(-q, -w) = chi(q, w)*, F = int d^3q/(2pi)^3 q |V(q)|^2 Im chi(q, q.v). With Im chi = -pi rho q^2 sum F_nu sgn(w) delta(w^2 - c_nu^2 q^2): the mu = cos(theta) integral has roots mu = +-c/v, each with Jacobian 1/(2 q^2 v c), giving int dmu q mu Im chi = -pi rho F q / v^2; with the measure 2 pi q^2 dq dmu/(2 pi)^3 this yields F_d = (1/(4 pi)) rho F_nu v^-2 int q^3 |V|^2 dq for each branch with c_nu < v. C = 1/(4 pi) = 0.07957747154594767, identical to the leg. (Filament: four roots on the circle with Jacobian 1/(2 q^2 v c sin theta0) give the 2D form with S(M) = (1 - 1/M^2)^(-1/2), confirming the origin of the S-factor used in the main re-evaluation.)

Independent recomputation (rv_loss.py, reads only qb_results.json and the stated inputs): v467 best -41.96090432548734 (p4, O), worst -43.89113261602559 (p2, A); M_new 16.321134387480537; factors [648.0248381622338, 651.6454311824593]; recovered [2.811591652275018, 2.814011354678906]; headline [-39.14931267321232, -39.14689297080844]; band (leg's reading) [-41.169440470745286, -38.38554633554141]; xi_req [22667.45969688186, 22794.105531318575] m; eq3 136027.3099135106; eq4 4.890756751056831e-24. All nine schema outputs agree with qd_results.json to 0 relative difference (bitwise). Reading issues: Findings 2-5.

## 6. (d) Hygiene

* Own re-implementation of the stated scan rule (case-sensitive substrings for non-numeric patterns; for numeric patterns the maximal token of numeric characters, space excluded, must equal the pattern): all 21 text files (7 code, 7 JSON, 7 NOTES) and this file are CLEAN; every numeric match is a collision inside a longer token (e.g. a stated input 3.1974e11, long reprs). The only HIT is the bytecode file of Finding 1. This file was scanned the same way.
* No file references first-leg artifacts (grep for the forbidden script names, the sealed checkpoint name, the first-leg branch, uploads, other gate folders: no hits apart from compliance statements). Code reads only files in this folder and the leg's own scratch caches.

## 7. Reviewer's own re-computations (code path of xcheck2d.py, independent of cc2d; M = 14)

Q-C headline states (fresh a* = root of the analytic de/da at the leg's g values):

| g | a* | eps_c | mu_c | root function | c2/cT | F2(0.05) | leg value |
|---|---|---|---|---|---|---|---|
| 13.044599196525805 | 1.5095487858830967 | 20.411375350728306 | 38.43568709593875 | f = -2.5579538487363607e-13 | 0.7708764193999409 | 0.4124515207535878 | ratio 0.7708764194235955, F2 0.4124515207565415 |
| 12.570151217206702 | 1.5144078570404356 | 19.745147359245067 | 37.72779882468699 | eps_minus_pi_g_half = 3.836930773104541e-13 | - | - | ratio -, F2 - |
| 12.717222586536337 | 1.5127487526235939 | 19.954187212451203 | 37.92026134624036 | f = -0.37768513796433467 | 0.7877276809435254 | 0.5058547001972734 | ratio 0.7877276809284883, F2 0.5058547002316478 |

Lambda_u from my mu_c(Lambda_c): 12.234459184904058 (leg 12.234459184904063). The energy-crossing root function is 3.836930773104541e-13 at the leg's root, f(Lambda_c) = -2.5579538487363607e-13.

Branch end: scanning a upward from 1.517 at fixed g (continuation in g from 12.6): de/da changes sign (a local minimum of e(a) exists) at g = 12.335, 12.33, 12.328 (max de/da 0.08202510048141047, 0.04038730191996989, 0.01818206553129052) and not at g = 12.3265 (max de/da -0.0033451411597274746); at g = 12.325 and 12.32 no fixed-cell crystal is reached at a = 1.517. Fold bracket [12.3265, 12.328], containing the leg's 12.326704359054563.

Q-A points not covered by xcheck2d (relative difference reviewer - qa_results; residual = Q-A Brent a* jitter):

| g | a* | c2 | cT | c1 | F2 | Z21 | S2 | cT30 |
|---|---|---|---|---|---|---|---|---|
| 28 | 2.45e-08 | 3.04e-08 | -5.80e-08 | -6.96e-08 | -1.12e-08 | -1.12e-07 | -6.86e-08 | -5.78e-08 |
| 16 | 1.74e-08 | 3.81e-08 | -2.60e-08 | -4.70e-08 | 3.31e-08 | -4.69e-08 | -4.03e-08 | -2.56e-08 |
| 14 | -2.86e-08 | -8.31e-08 | 3.50e-08 | 9.11e-08 | -1.14e-07 | 1.68e-08 | 5.07e-08 | 3.34e-08 |
| 13.5 | 2.08e-08 | 6.79e-08 | -2.37e-08 | -7.39e-08 | 1.08e-07 | 2.18e-08 | -2.94e-08 | -2.27e-08 |
| 13 | 2.56e-08 | 9.88e-08 | -2.66e-08 | -1.11e-07 | 1.93e-07 | 1.35e-07 | -1.67e-08 | -2.49e-08 |

Full-precision reviewer values: g=28: a* 1.434440781135794, c2 1.2880195636663372, cT 6.660403428552385, c1 12.677499084303559, F2 0.02146832576188952, Z21 0.21538140255038407, S2 0.6787755718551318, cT30 6.660474672074667; g=16: a* 1.4881960193572803, c2 2.688616046985301, cT 4.906417742586147, c1 9.408902336970632, F2 0.15972380564480618, Z21 0.6656559261933499, S2 0.6992645692310361, cT30 4.910241627235179; g=14: a* 1.5017281929156263, c2 3.1714738398801305, cT 4.604884088438326, c1 8.65738849101535, F2 0.2778904337991564, Z21 1.0586611323252597, S2 0.7428987955073887, cT30 4.613121236469384; g=13.5: a* 1.5056361450314728, c2 3.315247375181705, cT 4.530082445961292, c1 8.422445703645801, F2 0.3343560912466053, Z21 1.294899732447858, S2 0.767138294106853, cT30 4.54064232440113; g=13: a* 1.5099592443627021, c2 3.4496311863662066, cT 4.4553630365096, c1 8.130682840818782, F2 0.42253138311952637, Z21 1.7862569672313455, S2 0.8089680437135819, cT30 4.469736872655208.

Linear-response f_s (dense Galerkin L at q = 0, x and y): g=22: 0.0951882368601189 (rel -1.61e-08); g=16: 0.2782140209272106 (rel -5.42e-09); g=14: 0.436120847147457 (rel 1.21e-09); g=13.5: 0.4971784698543996 (rel 1.09e-09); g=13.25: 0.53376403131894 (rel 2.47e-09); g=13: 0.5762926359854302 (rel 4.68e-09).

## 8. Schema source map (for the assembler; values as stored)

| key | value | source |
|---|---|---|
| 2d.44.astar | 1.3926604701432632 | qa_results.json summary |
| 2d.44.c2 | 0.5958886255965102 | qa_results.json summary |
| 2d.44.cT | 8.714840662432088 | qa_results.json summary |
| 2d.44.c1 | 16.105774372101827 | qa_results.json summary |
| 2d.44.F2 | 0.0032459780481869055 | qa_results.json summary |
| 2d.44.Z21 | 0.08774413933008127 | qa_results.json summary |
| 2d.44.S2 | 0.7026083483329414 | qa_results.json summary |
| 2d.28.astar | 1.4344407460001043 | qa_results.json summary |
| 2d.28.c2 | 1.2880195244675108 | qa_results.json summary |
| 2d.28.cT | 6.660403814583182 | qa_results.json summary |
| 2d.28.c1 | 12.67749996620366 | qa_results.json summary |
| 2d.28.F2 | 0.021468326001725047 | qa_results.json summary |
| 2d.28.Z21 | 0.21538142676197036 | qa_results.json summary |
| 2d.28.S2 | 0.6787756184033542 | qa_results.json summary |
| 2d.22.astar | 1.4573382222657398 | qa_results.json summary |
| 2d.22.c2 | 1.8028151316050003 | qa_results.json summary |
| 2d.22.cT | 5.8043651397829645 | qa_results.json summary |
| 2d.22.c1 | 11.172446904533974 | qa_results.json summary |
| 2d.22.F2 | 0.051482070039054396 | qa_results.json summary |
| 2d.22.Z21 | 0.335689301054332 | qa_results.json summary |
| 2d.22.S2 | 0.6747429043945447 | qa_results.json summary |
| 2d.22.f_s | 0.09518823839305457 | qa_results.json summary |
| 2d.22.fsum_resid_max | 5.2653870924998635e-11 | qa_results.json summary |
| 2d.22.static_resid_max | 1.7859331850001767e-15 | qa_results.json summary |
| 2d.22.cT_30deg_kf005 | 5.804934993853741 | qa_results.json summary |
| 2d.16.astar | 1.488195993433918 | qa_results.json summary |
| 2d.16.c2 | 2.688615944601287 | qa_results.json summary |
| 2d.16.cT | 4.906417869979765 | qa_results.json summary |
| 2d.16.c1 | 9.408902779193728 | qa_results.json summary |
| 2d.16.F2 | 0.15972380035221942 | qa_results.json summary |
| 2d.16.Z21 | 0.6656559574054087 | qa_results.json summary |
| 2d.16.S2 | 0.6992645974113894 | qa_results.json summary |
| 2d.16.f_s | 0.2782140224350095 | qa_results.json summary |
| 2d.14.astar | 1.501728235875289 | qa_results.json summary |
| 2d.14.c2 | 3.1714741032868843 | qa_results.json summary |
| 2d.14.cT | 4.60488392740682 | qa_results.json summary |
| 2d.14.c1 | 8.65738770247263 | qa_results.json summary |
| 2d.14.F2 | 0.27789046559555847 | qa_results.json summary |
| 2d.14.Z21 | 1.0586611144889737 | qa_results.json summary |
| 2d.14.S2 | 0.7428987578053835 | qa_results.json summary |
| 2d.14.f_s | 0.43612084661859807 | qa_results.json summary |
| 2d.13.5.astar | 1.505636113713476 | qa_results.json summary |
| 2d.13.5.c2 | 3.3152471499511345 | qa_results.json summary |
| 2d.13.5.cT | 4.5300825532700335 | qa_results.json summary |
| 2d.13.5.c1 | 8.422446326119438 | qa_results.json summary |
| 2d.13.5.F2 | 0.334356054974865 | qa_results.json summary |
| 2d.13.5.Z21 | 1.2948997041704637 | qa_results.json summary |
| 2d.13.5.S2 | 0.7671383166759972 | qa_results.json summary |
| 2d.13.5.f_s | 0.49717846931087406 | qa_results.json summary |
| 2d.13.astar | 1.5099592056754438 | qa_results.json summary |
| 2d.13.c2 | 3.4496308456926457 | qa_results.json summary |
| 2d.13.cT | 4.45536315520834 | qa_results.json summary |
| 2d.13.c1 | 8.130683743886095 | qa_results.json summary |
| 2d.13.F2 | 0.422531301376562 | qa_results.json summary |
| 2d.13.Z21 | 1.786256725595615 | qa_results.json summary |
| 2d.13.S2 | 0.8089680572046474 | qa_results.json summary |
| 2d.13.f_s | 0.5762926332873413 | qa_results.json summary |
| 2d.13.25.astar | 1.507729128132037 | qa_results.json summary |
| 2d.13.25.c2 | 3.386651802383835 | qa_results.json summary |
| 2d.13.25.cT | 4.492747758640106 | qa_results.json summary |
| 2d.13.25.c1 | 8.287295256049886 | qa_results.json summary |
| 2d.13.25.F2 | 0.37258560686256326 | qa_results.json summary |
| 2d.13.25.Z21 | 1.4848888199280448 | qa_results.json summary |
| 2d.13.25.S2 | 0.7846838338295686 | qa_results.json summary |
| 2d.13.25.f_s | 0.5337640299980182 | qa_results.json summary |
| 2d.35g6.astar | 1.4375363197237399 | qa_results.json summary |
| 2d.35g6.c2 | 2.176808658849081 | qa_results.json summary |
| 2d.35g6.cT | 6.649116872001452 | qa_results.json summary |
| 2d.35g6.c1 | 13.533101106902558 | qa_results.json summary |
| 2d.35g6.F2 | 0.04319824279623224 | qa_results.json summary |
| 2d.35g6.Z21 | 0.2808007782623577 | qa_results.json summary |
| 2d.35g6.S2 | 0.6356917220074685 | qa_results.json summary |
| hydro_g22.f_s | 0.09518823686011202 | qa_prime_results.json |
| hydro_g22.alpha | 43.726596216764335 | qa_prime_results.json |
| hydro_g22.M | 91.64325226773684 | qa_prime_results.json |
| hydro_g22.Cxxyy | 30.5059772184683 | qa_prime_results.json |
| hydro_g22.mu | 30.568637536439642 | qa_prime_results.json |
| hydro_g22.gamma | 8.017959775526625 | qa_prime_results.json |
| hydro_g22.F_minus | 0.051811930464356795 | qa_prime_results.json |
| hydro_g22.c_minus | 1.8167718025575543 | qa_prime_results.json |
| hydro_g22.c_plus | 11.210456986512957 | qa_prime_results.json |
| hydro_g22.c_T | 5.812445879721162 | qa_prime_results.json |
| hydro_g22.static_share_minus | 0.6753841581964672 | qa_prime_results.json |
| 3d.c2 | 0.470555527432646 | qb_results.json schema |
| 3d.cT_min | 7.7493459895352235 | qb_results.json schema |
| 3d.cT_max | 8.04006531797928 | qb_results.json schema |
| 3d.c1_basal_q015 | 16.13717890367541 | qb_results.json schema |
| 3d.F2_basal_q015 | 0.0016666207042539045 | qb_results.json schema |
| 3d.Z21_basal_q015 | 0.05734519151329853 | qb_results.json schema |
| 3d.S2_basal_q015 | 0.6629042326549988 | qb_results.json schema |
| 3d.c_kappa | 9.38464586499687 | qb_results.json schema |
| melting.Lambda_c | 13.044599196525805 | qc_results.json |
| melting.Lambda_u | 12.234459184904063 | qc_results.json |
| melting.energy_crossing | 12.570151217206702 | qc_results.json |
| melting.ratio_at_Lambda_c | 0.7708764194235955 | qc_results.json |
| melting.F2_at_Lambda_c | 0.4124515207565415 | qc_results.json |
| melting.ratio_max_metastable | 0.7877276809284883 | qc_results.json |
| melting.branch_end_g | 12.326704359054563 | qc_results.json |
| melting.any_c2_ge_cT | false | qc_results.json |
| loss.v467_best_orders | -41.96090432548734 | qd_results.json |
| loss.v467_worst_orders | -43.89113261602559 | qd_results.json |
| loss.main_orders_recovered | [2.811591652275018, 2.814011354678906] | qd_results.json |
| loss.main_headline_orders | [-39.14931267321232, -39.14689297080844] | qd_results.json |
| loss.band_orders | [-41.169440470745286, -38.38554633554141] | qd_results.json |
| loss.xi_req_main_m | [22667.45969688186, 22794.105531318575] | qd_results.json |
| loss.eq3_coefficient | 136027.3099135106 | qd_results.json |
| loss.eq4_bound | 4.890756751056831e-24 | qd_results.json |
| loss.drag_prefactor_3d_coeff | 0.07957747154594767 | qd_results.json |

Recommended extra (CC-only) keys: loss.band_orders_recovered [0.791463854742054, 3.57535798994593]; loss.band_orders_R3_without_F2 [-41.169440470745286, -39.14689297080844]; loss.eq3_coefficient_own_cT_mean 148221.81093728365; melting.bdg_onset_q0_estimate 12.39501508076986; 2d.22.static_resid_max_incl_30deg 4.70800345396941e-15; 2d.*.f_s_twist (finite-twist values).
