# Q-C notes (approach to melting, step kernel, 2D) -- second leg, `cc2d_melt.py`

All numbers are copied programmatically from `qc_results.json` (repr, full precision). Units hbar = m = R = 1,
mean density 1, step kernel Uhat(k) = 2 pi g J1(k)/k.

## Headline

| key | value | bracket / note |
|---|---|---|
| Lambda_c (root of g(mu_c - eps_c) - mu_c^2/(2 pi)) | 13.044599196525805 | Brent evaluations bracket [13.04459917667258, 13.044599197025812] (values [-2.7027084570363513e-08, 6.805009888921632e-10]); branch sign change between [13.0, 13.25] |
| Lambda_u = mu_c(Lambda_c)/pi | 12.234459184904063 | mu_c(Lambda_c) = 38.435687095938775, eps_c = 20.411375350728306, a* = 1.509548785883096 |
| energy crossing (eps_c = pi g/2) | 12.570151217206702 | Brent evaluations bracket [12.570151092226975, 12.570151217706709] (values [1.752414746647446e-08, -6.975042765589023e-11]); branch sign change between [12.5, 12.75] |
| c2/cT at Lambda_c (LSQ speeds) | 0.7708764194235955 | c2 = 3.439683858993886, cT = 4.462043165836915, c1 = 8.160818867135768 |
| F2 at Lambda_c (|q|a/2pi = 0.05) | 0.4124515207565415 | Z21 = 1.7194726119726085, S2 = 0.8039433333460878 |
| max c2/cT along the metastable continuation | 0.7877276809284883 | at g = 12.717222586536337 (bounded Brent in g, xatol 1e-4; best grid point [12.7, 0.7876366775831014]) |
| branch end g (fold of the a*-branch) | 12.326704359054563 | bisection bracket [12.326704311370849, 12.32670440673828]; first bracket <= 0.005: [12.325, 12.328125]; 0.05-step continuation: lost at 12.3, ok at 12.35 |
| any c2 >= cT over every computed crystal state | False | 81 states with real BdG spectrum at the Q-A q (of 128 crystal states); max c2/cT over all = 0.7877276809284883 |
| BdG first fails (imaginary omega, q along a1) | 12.383498764038086 | at |q|a/2pi = 0.03, bracket [12.383498382568359, 12.383499145507812]; q -> 0 estimate 12.39501508076986 |

## Method

* Library: `cc2d.py` of this leg (plane-wave Galerkin, exact products on the 2N grid, Newton-Krylov ground states,
  never imaginary time). Production N = 64 (2773 plane waves), ground-state tolerance ||H psi - mu psi||/||psi|| < 1e-12
  (max over the branch 9.467202557182e-13), BdG Kcut = 80, q along a1 with |q|a/2pi in {0.03, 0.05, 0.075, 0.10},
  LSQ speeds through the origin, F2/Z21/S2 at 0.05 (cc2d.speeds). Threads 2.
* a*: the local minimum of e(a) = E_cell/A at fixed density, located as the root of the envelope-theorem derivative
  de/da (cc2d.dedA_envelope; precise to ~1e-15) by a downhill walk in a from the continuation guess (fresh ground
  state at every a, seeded by the nearest solved a) until de/da changes sign, then Brent (xtol 1e-14 a).
  d2e/da2 from central differences of de/da (steps 2h and h, Richardson; h = 1e-4 a* reduced automatically near the
  end so that a* +- 2h stay inside the fixed-cell existence interval). This differs from the Q-A Brent-on-e(a) value
  only by its round-off jitter (consistency table below).
* Seed: `WORK/qa_states.npz` state `step_g16_aroot`; continuation downward g = 16, 15.75, ... (step 0.25), 0.05 steps
  after the first loss, bisection to 1e-7; extra points every 0.05 in [12.5, 13]; upward g = 16.5 ... 44.
* Every branch state: symmetric-sector constrained Hessian (A = L + 2X on real point-group-invariant perturbations
  orthogonal to psi0; 253 C6v orbit functions of the ground-state basis, cc2d `_Ctx.hess` applied column by column),
  the full Gamma-sector constrained Hessian (all irreps, complement of psi0, d_x psi0, d_y psi0, Kcut 60),
  the minimum eigenvalue of A(q) on a 6x6 BZ grid plus M and K (cc2d.stability_scan, Kcut 50), and the BdG along a1.
* Lambda_c and the energy crossing: scipy brentq (xtol 1e-9 in g) on the branch sign change, with a fresh
  a*-optimised solve at every evaluation.
* Branch end: a state is lost when (i) the seeded solve collapses to the uniform state at the guess, at the seed a
  and at five smaller a, (ii) the downhill walk in a finds no local minimum before the fixed-cell crystal ceases to
  exist (or within +-4 %), (iii) the symmetric-sector eigenvalue is negative, (iv) d2e/da2 <= 0.
* BdG instability onset: for each |q|a/2pi, bisection in g (to 1e-6) on Cholesky failure of A(q) (imaginary omega),
  fresh a*-optimised solve per evaluation. Extra q: 0.01 and 0.005 (q -> 0 trend).

## Branch end (what triggered)

Criterion that triggered: (ii), the a-curvature criterion. a-curvature: below the bracket the downhill walk in a finds no local minimum of e(a); de/da < 0 on the whole interval of a where the fixed-cell crystal exists, up to its right edge where the fixed-cell crystal folds (symmetric-sector eigenvalue -> 0) and the solve collapses to the uniform state. Above the bracket the minimum exists with d2e/da2 -> 0+ and the symmetric-sector eigenvalue small but positive: the minimum of e(a) merges with the maximum of e(a) that sits just inside the fixed-cell existence edge (fold of the a*-branch).

* Last ok state g = 12.32670440673828: a* = 1.5190258983151783, d2e/da2 = 3.763281134409018, lowest symmetric-sector eigenvalue = 0.010043248534904457, eps_c = 19.391717287230836, mu_c = 37.77134125478532,
  contrast = 7.808183198999409. The fixed-cell crystal exists up to a = [1.5190443422555038, 1.5190443422699902] (right edge, bisection), where the symmetric-sector
  eigenvalue has fallen to [5.053910389363153e-06, 39.72991010743438]; inside that interval de/da changes sign 2 times (minimum and maximum of e(a)),
  maximum of de/da = 7.126381107447344e-08, de/da just inside the edge = -9.921549524571915e-05.
* First lost state g = 12.326704311370849: the fixed-cell crystal exists for a in [1.5091522299761302, 1.5190442241031217] (left scan fails at 1.5083927170269726), de/da has 0 sign
  changes there (max -1.0912700589837954e-06): e(a) decreases monotonically up to the fixed-cell fold edge, so there is no local minimum.
* Approach: d2e/da2 and the symmetric-sector eigenvalue along the branch (table below) go to 0 together, d2e/da2 first
  (a linear fit of lambda_sym^2 in g over the last states would reach 0 at g = 12.326678881082715, below the fold). The bracket is
  unchanged for N = 48 and N = 80 ([(48, True, False), (80, True, False)]).
* Gaussian-droplet seeds (no continuation) over a in [1.30, 1.80] at g = [12.326704311370849, 12.226704, 12.0] find no crystal (n_crystal = [0, 0, 0]);
  weak evidence only (the uniform state is itself locally stable there), recorded for completeness.

## BdG dynamical stability along the continuation

A(q) on the 6x6 BZ grid (|q| >= |b1|/6) stays positive on every state (min 1.0764304770062385), and the Gamma sector is positive
(min 0.010043248534897268). The long-wavelength sector is not: the lower longitudinal branch softens (c2 -> 0) and omega^2 < 0 appears
at small q before the fold. Onset g (bisection) per |q|a/2pi:

| |q|a/2pi | onset bracket in g |
|---|---|
| 0.005 | [12.394685363769533, 12.394686126708987] |
| 0.01 | [12.393697357177736, 12.39369812011719] |
| 0.03 | [12.383498382568359, 12.383499145507812] |
| 0.05 | [12.365103149414065, 12.365103912353518] |
| 0.075 | [12.338195800781246, 12.3381965637207] |
| 0.1 | stable at every cached state |

So the first failure at the Q-A q values is at |q|a/2pi = 0.03, g = 12.383498764038086; the q -> 0 extrapolation (onset = g0 - kappa q^2
through 0.005 and 0.01) gives g0 = 12.39501508076986. Robust to N and Kcut ([(48, 80.0, False, True), (80, 80.0, False, True), (64, 60.0, False, True), (64, 100.0, False, True)]).
Between the onset and the fold (47 crystal states computed there) the a*-crystal is a minimum in the symmetric
sector and in a, but a saddle against long-wavelength density/strain modulations; c2 is imaginary there and c2/cT
is undefined. The maximum of c2/cT is interior, at g = 12.717222586536337, well above the onset.

## Branch table (selection; the full table with every check is `branch_table` in qc_results.json)

| g | a* | eps_c | mu_c | contrast | f(g) | eps_c - pi g/2 | d2e/da2 | lambda_sym | c2/cT | F2 |
|---|---|---|---|---|---|---|---|---|---|---|
| 44.0 | 1.3926604829399247 | 53.82803334215832 | 96.22867925018438 | 142730.0783634876 | 391.8602183924161 | -15.28700503681712 | 292.30980704836526 | 47.024858315373685 | 0.06837631020776232 | 0.003245978035107888 |
| 28.0 | 1.434440781135794 | 37.767525016818055 | 67.29892382231921 | 5335.613329237651 | 106.04332832608418 | -6.214772133439048 | 162.3620827633084 | 28.917515689864402 | 0.19338461665111123 | 0.021468325752376585 |
| 22.0 | 1.4573382531939647 | 31.266025774896338 | 55.85080532784255 | 1112.100662629704 | 44.411153781130224 | -3.2914934145913826 | 115.02705427452594 | 20.469050748476384 | 0.3105964600920088 | 0.05148207011257231 |
| 16.0 | 1.48819601935728 | 24.24982742122156 | 44.06180029698103 | 142.2745772661986 | 8.001435927556315 | -0.8829138074967844 | 64.50949789682504 | 10.230347470659797 | 0.5479794399530803 | 0.15972380564765357 |
| 15.75 | 1.4897564285614733 | 23.939264782143997 | 43.568873366678126 | 127.60932170031347 | 7.050985485217609 | -0.8007773648756249 | 62.149133484643365 | 9.732664867562082 | 0.5630256086988251 | 0.1695870358785723 |
| 15.5 | 1.4913484335808609 | 23.626627602030613 | 43.076839079817695 | 114.06559974915449 | 6.148126972834405 | -0.7207154632902828 | 59.74499060681877 | 9.225423657953263 | 0.5787139128218592 | 0.1804102180640974 |
| 15.25 | 1.4929742460092637 | 23.311796772412954 | 42.586007357260414 | 101.57004008091167 | 5.2933959835451105 | -0.6428472112092187 | 57.29108929202903 | 8.707652563439208 | 0.5950865286749527 | 0.1923467018622953 |
| 15.0 | 1.4946365046225132 | 22.99463945977365 | 42.096766175347284 | 90.05282700809386 | 4.487422370551883 | -0.5673054421497952 | 54.78020090580272 | 8.178184275536562 | 0.612188031819804 | 0.20558862019779198 |
| 14.75 | 1.4963384198142151 | 22.675006401528105 | 41.60960901806787 | 79.44735313565674 | 3.7309559309445604 | -0.494239418696619 | 52.203443977044 | 7.635593343963867 | 0.6300640811101799 | 0.22038144897060968 |
| 14.5 | 1.4980839881756212 | 22.352728342427252 | 41.12517577224972 | 69.68979813645625 | 3.02490248176224 | -0.42381839609874916 | 49.54969004464061 | 7.0781052027087386 | 0.6487584045693754 | 0.23704625059251266 |
| 14.25 | 1.499878323650885 | 22.027611199352695 | 40.644316013049256 | 60.71857546082566 | 2.3703762965572537 | -0.35623645747458 | 46.80465576055957 | 6.5034576518912335 | 0.668306194818845 | 0.25601509989119375 |
| 14.0 | 1.5017281929156265 | 21.699429261305248 | 40.16819160628066 | 52.4735349814422 | 1.7687795992266047 | -0.29171931382330385 | 43.949448447859886 | 5.908679732406976 | 0.6887195809276737 | 0.2778904337419373 |
| 13.75 | 1.5036429327840517 | 21.367915185439443 | 39.698453043801855 | 44.89468949333712 | 1.221929648527464 | -0.23053430799038566 | 40.95809427496875 | 5.289717250435508 | 0.7099544613809414 | 0.3035509275313597 |
| 13.5 | 1.5056361450314726 | 21.03274439760751 | 39.23756622675541 | 37.919937171793286 | 0.7322764444816983 | -0.17300601412359384 | 37.79300455216219 | 4.640748454654205 | 0.7318293683866207 | 0.33435609142135175 |
| 13.25 | 1.5077291618363957 | 20.693508793109075 | 38.7894828862156 | 31.480421878382668 | 0.3033124114385828 | -0.11954253692330497 | 34.39576065674999 | 3.9527987020745026 | 0.7538042049185872 | 0.3725856585215203 |
| 13.044599196525805 | 1.509548785883096 | 20.411375350728306 | 38.435687095938775 | 26.53029276911307 | -2.8421709430404007e-13 | -0.07903315168608671 | 31.362229499133264 | 3.3479503292491204 | 0.7708764194235955 | 0.4124515207565415 |
| 13.0 | 1.5099592443626995 | 20.349667211072404 | 38.36123241202788 | 25.48937683513351 | -0.059544381069457586 | -0.07068503726125286 | 30.665407807306924 | 3.2104929998948717 | 0.774264893311164 | 0.42253138289366904 |
| 12.95 | 1.510427237962319 | 20.280283656924905 | 38.279017327134625 | 24.33451960178953 | -0.12345811270418494 | -0.06152877506900367 | 29.86450272612396 | 3.0532613374145523 | 0.7778303947197885 | 0.43460068399852 |
| 12.9 | 1.5109044165973526 | 20.21067806158322 | 38.19830460191706 | 23.190977772265356 | -0.18426215729652995 | -0.052594554070946486 | 29.04034827687485 | 2.8923583418407137 | 0.78106889361677 | 0.4475990148892037 |
| 12.85 | 1.5113919279356682 | 20.14084157161891 | 38.11931579326607 | 22.056923400292654 | -0.24182691727506267 | -0.04389122769551079 | 28.189885258196366 | 2.727325707934373 | 0.7838670126264685 | 0.4616749017481141 |
| 12.8 | 1.5118912026209708 | 20.070764227435248 | 38.042327726087976 | 20.930129389640012 | -0.2959968693228632 | -0.035428755539427925 | 27.309305121731 | 2.557594343840886 | 0.786065828574929 | 0.4770146992292725 |
| 12.75 | 1.5124040626067947 | 20.000434686092856 | 37.96769373239698 | 19.807809721689274 | -0.3465817277037786 | -0.027218480542074985 | 26.39376226733269 | 2.3824422702665604 | 0.7874362779981551 | 0.4938558281407966 |
| 12.7 | 1.5129328893871443 | 19.92983983288252 | 37.89587665931583 | 18.68636950299053 | -0.3933430629320469 | -0.01927351741266392 | 25.436926187848268 | 2.2009293253871287 | 0.7876366775831014 | 0.5125056723530423 |
| 12.65 | 1.5134808983509764 | 19.858964216098517 | 37.8275027422573 | 17.560994263955127 | -0.43597303828610734 | -0.011609317856926538 | 24.43024873164777 | 2.011790813213602 | 0.7861348669410698 | 0.5333684313909691 |
| 12.6 | 1.5140526146768853 | 19.787789184741513 | 37.763455128673016 | 16.42493210459708 | -0.4740585028333726 | -0.004244532874182028 | 23.36168753028133 | 1.8132532544596502 | 0.7820543488223562 | 0.5569816492974903 |
| 12.570151217206702 | 1.5144078570404338 | 19.745147359245042 | 37.72779882468697 | 15.737694603773978 | -0.49439760628243334 | 3.588240815588506e-13 | 22.68724266587502 | 1.6892190323263307 | 0.7777936379611172 | 0.5726748480816823 |
| 12.55 | 1.514654767906371 | 19.716291489965688 | 37.705049825293905 | 15.268133784559593 | -0.5070153484374771 | 0.0027975886897344537 | 22.21329173578209 | 1.6026884654341713 | 0.7738383267787851 | 0.5840569723567002 |
| 12.5 | 1.51529816851384 | 19.64444082080988 | 37.65440509534132 | 14.074377300382919 | -0.5339547559050857 | 0.009486735873672103 | 20.956092892822912 | 1.3758887989859183 | 0.7584056532199732 | 0.615477956258856 |
| 12.45 | 1.516002330056777 | 19.572194910511367 | 37.615352096600596 | 12.81412729893136 | -0.5533637164903098 | 0.01578064191490469 | 19.53734744102772 | 1.125284206237272 | 0.7285123969085548 | 0.6519648783929366 |
| 12.4 | 1.5168103105250197 | 19.499487760492514 | 37.59636151706817 | 11.42140790027256 | -0.562112863736246 | 0.021613308235796325 | 17.838553729966737 | 0.8342246734451488 | 0.6599124594052883 | 0.6913590722198152 |
| 12.35 | 1.5178744771874821 | 19.426187733027383 | 37.62747379199431 | 9.658798470528064 | -0.5499484020423324 | 0.026853097110411284 | 15.415728871407348 | 0.4439877022173861 | - | - |
| 12.337499999999999 | 1.5182709483237502 | 19.407731859679895 | 37.66093009148745 | 9.017661031113887 | -0.5378888778803628 | 0.028032177847862272 | 14.398021196856382 | 0.29616644163352546 | - | - |
| 12.331249999999999 | 1.5185514971684946 | 19.398472888156867 | 37.69391012125313 | 8.56721224896747 | -0.5266443223542581 | 0.02859068336730175 | 13.559487465571609 | 0.19061282865420157 | - | - |
| 12.328125 | 1.5187698118839725 | 19.393831693653404 | 37.72582298111851 | 8.217775094814941 | -0.5162381788241817 | 0.028858227385068602 | 12.658478891156356 | 0.10786422656528867 | - | - |
| 12.32734375 | 1.5188581445080696 | 19.392669467229673 | 37.74047433171047 | 8.076507827363072 | -0.5115955907878913 | 0.028923185591647638 | 12.054910604925894 | 0.07421894784441091 | - | - |
| 12.326953125 | 1.518924744818119 | 19.39208787854701 | 37.752235802229855 | 7.969999135874192 | -0.5079249049128123 | 0.028955189224138422 | 11.258220404830736 | 0.04878529036718468 | - | - |
| 12.326757812499999 | 1.5189829722572086 | 19.391796894616032 | 37.763045569409506 | 7.876863593743837 | -0.5045931962881411 | 0.0289710014507385 | 9.529002747221838 | 0.026501018800404678 | - | - |
| 12.326708984375 | 1.5190170661272664 | 19.391724112312414 | 37.76961127052722 | 7.822316169978436 | -0.5025884678725845 | 0.02897491818651332 | 6.0873344569919245 | 0.01343156963286825 | - | - |
| 12.326705932617188 | 1.5190221654998401 | 19.39171956233053 | 37.770608623975285 | 7.814156445168584 | -0.5022851647441655 | 0.028975161894592816 | 4.977398965371929 | 0.011475412802091812 | - | - |
| 12.32670440673828 | 1.5190258983151783 | 19.391717287230836 | 37.77134125478532 | 7.808183198999409 | -0.5020625692426961 | 0.028975283639880445 | 3.763281134409018 | 0.010043248534904457 | - | - |

## Maximum of c2/cT

Bounded Brent in g between the grid neighbours [12.65, 12.75]; evaluations (g, ratio): [(12.68819660112501, 0.7874609682106793), (12.71180339887499, 0.7877189457244477), (12.726393202250021, 0.7877035299774934), (12.717414532808725, 0.7877276699649904), (12.717281863217366, 0.7877276798786762), (12.717222586536337, 0.7877276809284883), (12.717189064576111, 0.7877276807073746)]. At the maximum: c2 = 3.475998325968989, cT = 4.412690337188427,
F2 = 0.5058547002316478. N/Kcut variation of the ratio there: [(48, 0.7877276809747067), (64, 0.7877276809331234), (80, 0.7877276808630644)].
Near the BdG onset the LSQ c2 is dominated by the larger q (omega(q)/q rises strongly with q because c2(q->0) -> 0);
the ratio is the LSQ definition as specified, not a q -> 0 limit.

## Consistency with qa_results.json (same library, Q-A used Brent-on-e(a) a*)

| g | a* rel diff | c2 rel diff | cT rel diff | F2 rel diff | ratio (QC) | ratio (QA) | a* vs QA envelope root |
|---|---|---|---|---|---|---|---|
| 16 | 1.741931992692416e-08 | 3.807183751011404e-08 | 2.588895457038472e-08 | 3.315369490994741e-08 | 0.5479794399530803 | 0.5479794049038826 | 0.0 |
| 14 | 2.8606815446187532e-08 | 8.30841670429603e-08 | 3.502579688668251e-08 | 1.1462653501593937e-07 | 0.6887195809276737 | 0.6887196622723254 | 1.4785938359053417e-16 |
| 13.5 | 2.080050840652682e-08 | 6.798162609819568e-08 | 2.363981363017598e-08 | 1.0900501495561049e-07 | 0.7318293683866207 | 0.7318293013353648 | 0.0 |
| 13.25 | 2.2354385816716616e-08 | 7.872505836688702e-08 | 2.453847356340832e-08 | 1.3864989979485486e-07 | 0.7538042049185872 | 0.7538041270781088 | 2.9454176591581434e-16 |
| 13 | 2.5621391277241693e-08 | 9.873686553257073e-08 | 2.6591680754386166e-08 | 1.9292560527214262e-07 | 0.774264893311164 | 0.7742647962736801 | 1.4705337627754881e-15 |

The QC a* equals the Q-A envelope-root a* to round-off; the 1e-8..2e-7 differences are the Q-A Brent jitter.

## Checks and convergence

* Sum rules (full spectrum): f-sum residual <= 4.9964269457059474e-08 on states whose lowest omega^2 at the Q-A q exceeds 1e-3; it grows to
  9.96287867477527e-05 only within ~1e-4 of the q = 0.03 onset (omega_2 -> 0, conditioning of Z = omega |<t|w>|^2). Static residual
  <= 6.253894641297369e-10 everywhere. At Lambda_c: f-sum 3.188904284949734e-10, static 3.4393598344471323e-15.
* Lambda_c (g = 13.044599196525805): N = 48/64/80 -> a* [1.509548785883096, 1.509548785883096, 1.509548785883096]; c2/cT (Kcut 80) [0.77087641946182, 0.7708764194831674, 0.7708764194491851]; F2 [0.412451520956263, 0.41245152071116803, 0.41245152084691133]; Kcut 60/80/100 at N = 64 -> c2/cT [0.7708764194033348, 0.7708764194831674, 0.7708764196364741].
* ratio_max (g = 12.717222586536337): N = 48/64/80 -> a* [1.512748752623595, 1.512748752623595, 1.512748752623595]; c2/cT (Kcut 80) [0.7877276809747067, 0.7877276809331234, 0.7877276808630644]; F2 [0.5058547001160201, 0.5058547002481858, 0.5058547001913345]; Kcut 60/80/100 at N = 64 -> c2/cT [0.787727680942638, 0.7877276809331234, 0.7877276806734061].
* g12.4 (g = 12.4): N = 48/64/80 -> a* [1.5168103105250197, 1.5168103105250197, 1.5168103105250197]; c2/cT (Kcut 80) [0.6599124593921268, 0.6599124593226918, 0.6599124594571882]; F2 [0.6913590714841293, 0.6913590715979737, 0.6913590722222291]; Kcut 60/80/100 at N = 64 -> c2/cT [0.6599124593495381, 0.6599124593226918, 0.6599124591496115].
* N = 48, 64, 80 at g = Lambda_c: f and eps_c - pi g/2 agree across N to 1.9895196601282805e-13 and 1.4210854715202004e-14 (absolute), i.e. the roots
  move by far less than the Brent tolerance.
* Upward check (g = 16.5 ... 44): f > 0 and eps_c - pi g/2 < 0 throughout, so neither root lies above 16.

## Issue found in cc2d.py (documented, not patched)

`cc2d.pcg` has no breakdown guard: when the Krylov residual stagnates on a nearly singular constrained Hessian (fixed-cell
crystal close to its fold edge) rz underflows to exactly 0.0 and `p = z + (rz2/rz) p` raises ZeroDivisionError, which
propagates out of `cc2d.ground_state` instead of returning a non-converged state. It occurred only at fixed-cell solves
at the very edge of crystal existence near the branch end (never on a reported state). Workaround in cc2d_melt.solve_fixed:
catch it, retry once with tol 1e-11, and otherwise count the solve as failed (= no crystal at that a). No converged
result of cc2d is affected.

## Ambiguities and choices

* Branch end: taken, as instructed, as the fold of the a*-branch (criteria i-iv: symmetric sector and a only). If
  "local minimum" is read to include every Bloch sector, the crystal stops being a minimum earlier, at the long-wavelength
  BdG onset (q -> 0 estimate 12.39501508076986; at the smallest Q-A q 12.383498764038086). Both readings are recorded; `branch_end_g` is the fold.
* "Max of c2/cT along the metastable continuation": below the BdG onset c2 is imaginary, so the maximum is taken over the
  states with a real spectrum at the Q-A q; it is interior and does not depend on this choice.
* a*: envelope-derivative root (minimum of e(a)) instead of Brent on e(a); identical minimiser, no jitter.
* No disagreement between the spec and the dispatch was found for this task.

## Files

* `cc2d_melt.py` (subcommands branch, up, grid, roots, bdg, ratiomax, dyn, fold, conv, collect); caches in
  `WORK/qc/` (points.json, roots.json, fold.json, conv.json, st_<g>.npz).
* `qc_results.json`: headline keys Lambda_c, Lambda_u, energy_crossing, ratio_at_Lambda_c, F2_at_Lambda_c,
  ratio_max_metastable, branch_end_g, any_c2_ge_cT; brackets; full branch table; profiles; convergence; consistency.
