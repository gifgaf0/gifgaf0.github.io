<!--
COVER NOTE FOR THE AUTHOR (remove before submission)
Plain-language summary: if empty space were a material, matter and light would both be features of it and would need
one shared speed limit. One picture of this kind makes the material a supersolid (a crystal that is also a
superfluid), with light as its shear wave and particles as knotted whirlpools. This paper shows that a supersolid has
a second sound, that the whirlpools are coupled to it through their cores and through their own flow, and that nothing
ties its speed to the light speed. In a standard model supersolid it is slower than light, so fast matter would make a
sonic boom and lose its energy, unless the two speeds agreed to about one part in 10^23 or the coupling were tuned
almost to zero. We compute this in two and three dimensions, and in two dimensions up to the point where the crystal
melts; second sound always stays below the light speed. The converse needs a nearly incompressible, mostly superfluid
crystal or a continuous melting transition, and there the argument does not apply. The general worry is known; what is
new is the concrete supersolid calculation and its numbers.
Revised October 4, 2026, after an outside AI review, then checked by a second, fresh AI reviewer: Sec. 6 now derives
both ways a vortex reaches the density, and Secs. 9-10 withdraw two claims that the derivation does not support (that
a vortex still drives second sound through its circulation in Green's limit, and that vortex matter could outrun
light). Also: the loss length is tied to a proton-size defect; the survival conditions are complete; Sec. 8 separates
the vortex's flow vertex, which radiates but does not bind; the chemical potential is renamed mu_c, so unsubscripted
mu is only the shear modulus, and the Lorentz factor is Gamma; the P(c_*^2) typo; Table 2's notes and missing f_s; the
radiation ratio (now about 10^11).
Title: the abstract now names the corners where the argument does not apply. If you want the title to say so too,
"Second sound and the common light cone of a supersolid vacuum" is a neutral option. Your call.
Prior art: the one published supersolid-vacuum proposal (Ref. [28], Cox, v4) was read in full on October 4, 2026
(lbc_bank/lit/COX_V4_BODY_READ.md). It never treats second sound, the Landau velocity or Cherenkov drag. It keeps a
single longitudinal compression branch, made ~10^20 c by near-incompressibility (Green's route). At its own superfluid
fraction (4/5) our hydrodynamics puts its omitted second sound above the light speed, so the paper does not claim to
refute it; Secs. 1, 5, 9 and 10 say this (Green's-limit result checked twice, supplementary S6).
Status of numbers: every cited number was computed twice, though not every second computation was blind (below). The
blind second computation (lbc_bank/second_leg/) agreed with the first on 108 of 112 numbers. The four misses traced to
the first computation: 2D ground states not converged tightly enough (transverse speeds 0.5-1 % low), a 3D plane-wave
basis too small (transverse speeds up to 6 % low), and a selection artifact at the melting end. With those corrected
the two agree on all 112 (2D <= 0.13 %, 3D <= 0.02 %); the tables use the corrected values (lbc_bank/closure/).
Table 2 rows outside the blind comparison (g = 34, 20, 18, 15 and the metastable rows) and the newly filled f_s
entries were recomputed with the second computation's own code, run by us after the first values were known, so not
blind. All agree to 0.14 %, except c1 at g = 12.4: there that code's automatic labelling picks a gapped mode at the
two largest wavevectors, and following first sound continuously gives 7.3576, as in the table
(closure/table2_cc_g124_modecheck.log). The Green's-limit relation (Sec. 5) and the vortex couplings (Sec. 6) were
each derived twice, the second time blind (supplementary S6). The arithmetic behind the revision's new numbers is in
paper/revision_numbers_check.py; the second reviewer recomputed it independently, not blind.
Acknowledgments: they now say that every check was made by AI agents, not by human referees. The wording is yours to
confirm.
Citations: each was checked against its publisher, arXiv or INSPIRE record (see the citation log in lbc_bank/paper/).
Draft date: October 4, 2026.
-->

# Second sound breaks the common light cone of a supersolid vacuum

**Matt Gifford**
Independent researcher, Hollister, California, USA

## Abstract

Medium-based models of the vacuum must give matter and light one causal cone: every excitation that matter couples to must be at least as fast as light. A supersolid is the natural medium for one picture of this kind: its superfluid order hosts vortex-knot "matter" and its shear rigidity carries transverse "light". A supersolid, however, has two longitudinal sounds. Zero-temperature supersolid hydrodynamics gives the fraction of the density response carried by the lower one (second sound), $F_- = \rho_s (M-\rho\gamma)^2/[\rho^2\rho_n (c_+^2-c_*^2)(c_+^2-c_-^2)]$, which vanishes only without superflow or if two independent elastic coefficients coincide, $M=\rho\gamma$. Bogoliubov–de Gennes calculations for the soft-core Gross–Pitaevskii supersolid in two and three dimensions, checked against two sum rules and an independent static route, put second sound at 0.06–0.8 of the shear speed, with 0.2–41 % of the f-sum and 64–80 % of the static response. Toward melting (computed in two dimensions) $c_2/c_T$ rises to 0.77 at the first-order phase boundary and peaks at 0.79 on the metastable branch; it never reaches one. A moving vortex drives the density through its core and, independently, through its own flow, with a strength fixed by the circulation quantum, so fast matter radiates second sound, with a drag proportional to that branch's f-sum share. Ultra-high-energy cosmic rays then survive only if defects are kilometres across (a proton-size one falls short by about 19 orders of magnitude), if second sound is tuned to within $10^{-23}$ of the shear speed or its coupling to matter made 19 orders weaker, or if it is faster than shear. Hydrodynamics allows that near a continuous melting transition, or in Green's limit of the elastic ether: a nearly incompressible, isotropic three-dimensional supersolid with superfluid fraction above 3/4. This is a concrete instance of the fine-tuning problem of emergent Lorentz invariance, with roots in the nineteenth-century elastic-ether debate.

---

## 1. Introduction

Any attempt to model the vacuum as a medium has to pass a simple test. Matter and light must share one causal cone, and every excitation that matter couples to must propagate at least as fast as light. Otherwise sufficiently fast matter emits that excitation, as a supersonic body emits a wake, and loses energy.

In analogue gravity the test appears as the mono-metricity problem. A medium with several low-energy modes generically gives several effective metrics, and a single metric requires the mode speeds to coincide [1–5]. The coincidence is a tuning condition. Liberati, Visser and Weinfurtner showed explicitly that in a two-component condensate the two phonon branches share a limiting speed only under fine-tuning conditions [4,5]. In the emergent-gravity setting the same issue is the "additional fine-tuning problem" of Collins et al. [6], with Chadha–Nielsen [7] and Anber–Donoghue [8] showing that interactions can drive species toward a common speed only logarithmically. Volovik notes that near a Fermi point the different low-energy fermions share one "speed of light" only through a symmetry that connects the species [9,10].

The observational bite is severe. Coleman and Glashow assigned each species a maximal attainable velocity and pointed out that a charged particle faster than light "loses energy rapidly via vacuum Cerenkov radiation" [11,12]. Moore and Nelson turned the same argument on gravity. The survival of the highest-energy cosmic rays forces the graviton speed to exceed $c(1-2\times10^{-15})$ for a galactic origin [13]. In Einstein-aether theory [14] this excludes every subluminal mode to comparable precision [15]; see Ref. [16] for a review.

Medium vacua come in several flavours: superfluid vacua [9,17–20], crystal vacua in which curvature or matter are defects [21–24], and dualities that rewrite crystal phonons as gauge fields with defects as sources [25–27]. A recent proposal combines the two orders that a knot-and-wave picture needs. The vacuum is a supersolid, light is its transverse shear wave, and particles are its defects, chiefly dislocations, with the claim that the superfluid component "lets matter drift through without drag" [28]. That proposal has a single longitudinal compression branch, which near-incompressibility makes about $10^{20}$ times faster than light, and it does not treat second sound [28]. For an ordinary crystal there is a classic precedent: a moving dislocation has a limiting speed equal to the shear-wave speed, with Lorentz-like contraction of its strain field [29,30]. In an ordinary solid shear is the slowest sound, so the defect "light cone" and the shear "light cone" coincide naturally.

This paper makes one point. **A supersolid adds a second longitudinal sound whose speed nothing ties to the shear speed, and its defects couple to it.** The extra sound is second sound: the superfluid's phase mode hybridized with lattice compression. In the standard model supersolid it is slower than shear and carries a sizeable share of the density response, which is enough to break the common cone. We quantify how strongly a defect drives it through density, which a moving vortex reaches through its own flow even when its core carries no density deficit. We first derive a closed form for the second-sound share of the density response, which vanishes only by a coincidence of elastic coefficients. We then compute it for the soft-core Gross–Pitaevskii supersolid in two and three dimensions, follow it to the melting transition, and work out the drag, radiation, binding and loss length that follow. The general principle is that of Refs. [1–8,11–15]. What we add is a concrete instance in the supersolid class, with numbers; a direct test, in that model, of the claim that superfluidity removes drag; and the opposite corner, a nearly incompressible and mostly superfluid supersolid, in which second sound outruns shear and the argument does not apply (Secs. 5 and 9).

## 2. Why a supersolid

Two requirements single out the medium. If matter is to be made of vortex lines or vortex knots, the medium needs a condensate phase: vortices are the topological defects (first homotopy group $\mathbb Z$) of a U(1) order parameter. If light is to be a transverse wave, the medium needs shear rigidity, because a fluid, superfluid or not, has no propagating transverse sound. A medium with both orders at once is a supersolid [31,32].

The cleanest microscopic realization is a condensate of bosons with a soft-core repulsion, whose Fourier transform has a negative region (a roton). Above a critical coupling such a condensate crystallizes into a lattice of droplets that keeps global phase coherence [33–36]. In two dimensions the ground state is triangular. We use the Gross–Pitaevskii energy (units $\hbar=m=1$)
$$E[\psi]=\int \tfrac12|\nabla\psi|^2\,d^dr+\tfrac12\iint \rho(\mathbf r)\,U(\mathbf r-\mathbf r')\,\rho(\mathbf r')\,d^dr\,d^dr',\qquad U(r)=g\,\theta(R-r),$$
at mean density $\bar\rho=1$ and core radius $R=1$, so that $g$ is the only parameter. The uniform state becomes unstable to the roton at $g_c=14.74$ in 2D [35]. The superfluid–supersolid transition is first order and precedes the roton softening [35].

The supersolid has three gapless branches at long wavelength: one transverse, from shear, and two longitudinal, from the hybridization of the superfluid phase mode with lattice compression [35–38]. For the soft-core supersolid, Poli et al. found the transverse branch "always sandwiched in between the second sound mode and the first sound mode" [38]. The ordering is $c_2<c_T<c_1$, and second sound "has a weak density contribution" [38]. The question for a vacuum model is how weak, whether "weak" can be made zero, and what it implies for moving defects.

## 3. Longitudinal response of a supersolid

At zero temperature and long wavelength a supersolid is described by the superfluid phase $\theta$, the density deviation $\delta\rho$ and the lattice displacement $\mathbf u$ [39–41]. Along a longitudinal direction the quadratic Lagrangian density is
$$\mathcal L=-\delta\rho\,\dot\theta-\frac{\rho}{2}(\partial_x\theta)^2+\frac{\rho_n}{2}(\dot u-\partial_x\theta)^2-\frac{\alpha}{2}\delta\rho^2-\gamma\,\delta\rho\,\partial_xu-\frac{M}{2}(\partial_xu)^2-V\delta\rho .$$
Here $\rho=\rho_s+\rho_n$ splits into superfluid and normal (lattice-bound) parts, $\alpha=\partial^2e/\partial\rho^2$ is the inverse compressibility at fixed lattice, $M=C_{xxxx}$ is the uniaxial modulus at fixed density, $\gamma=\partial^2e/\partial\rho\,\partial(\partial_xu)$ is the density–strain coupling, and $V$ is an external potential that couples to density. Solving the linear equations of motion gives the density response $\delta\rho=\chi V$:
$$\chi(q,\omega)=\frac{q^2\left(\rho\rho_n\,\omega^2-\rho_sM\,q^2\right)}{\rho_n\omega^4-\left(M+\rho\rho_n\alpha-2\rho_n\gamma\right)q^2\omega^2+\rho_s\left(\alpha M-\gamma^2\right)q^4}
=\rho q^2\sum_{\nu=\pm}\frac{F_\nu}{\omega^2-c_\nu^2q^2}.$$
The two sound speeds are the roots of $x^2-ax+b=0$ with $a=\rho\alpha-2\gamma+M/\rho_n$ and $b=(\rho_s/\rho_n)(\alpha M-\gamma^2)$, the form of Refs. [38,41]. The weights $F_\pm$ sum to one, which is the f-sum rule. The zero of the numerator sits at $c_*^2=\rho_sM/(\rho\rho_n)$, so
$$F_-=\frac{c_*^2-c_-^2}{c_+^2-c_-^2},\qquad F_+=1-F_-.$$
Evaluating the monic dispersion polynomial $P(x)=x^2-ax+b=(x-c_+^2)(x-c_-^2)$, for which $\rho_nq^4P(\omega^2/q^2)$ is the denominator of $\chi$, at $c_*^2$ gives $P(c_*^2)=-\rho_s(M-\rho\gamma)^2/(\rho^2\rho_n)$, and therefore
$$\boxed{F_-=\frac{\rho_s\,(M-\rho\gamma)^2}{\rho^2\rho_n\,(c_+^2-c_*^2)(c_+^2-c_-^2)}}\tag{1}$$
The second-sound share vanishes in only two cases: without superflow ($\rho_s=0$, so no supersolid), or when the uniaxial modulus happens to equal $\rho$ times the density–strain coupling. Nothing in the symmetry of a supersolid relates these two independent second derivatives of the energy. Equation (1) also shows $F_-\propto\rho_s$, so second sound decouples from density in the deep-crystal limit, where it also becomes slow, and, through $c_+\to\infty$, in the incompressible limit of Secs. 5 and 9.

Two further identities are useful. The compressibility sum rule reads $\sum_\nu F_\nu/c_\nu^2=1/c_\kappa^2$ with $c_\kappa^2=\rho(\alpha-\gamma^2/M)$. The share of the static response carried by branch $\nu$ is $S_\nu=(F_\nu/c_\nu^2)\,c_\kappa^2$. Because $c_-<c_+$, second sound carries a larger share of the static response than of the f-sum. The spectral weight per unit $q$, i.e. the dynamic structure factor's coefficient $Z_\nu$ in $S(q,\omega)=\sum_\nu Z_\nu\delta(\omega-c_\nu q)$, is $Z_\nu=\rho qF_\nu/2c_\nu$. Both branches carry density weight in general, and measuring the two weights and speeds determines the superfluid fraction [42]. All of these were checked symbolically and by an independent re-derivation of the response from the Lagrangian (supplementary S6).

## 4. Numbers for the soft-core supersolid

**Method.** For each coupling $g$ we relax the Gross–Pitaevskii state on a primitive triangular cell ($96^2$ real-space grid), optimize the lattice constant at fixed mean density, and converge the state by quasi-Newton minimization of the energy at fixed norm, to a relative Gross–Pitaevskii residual below $4\times10^{-5}$. At that level no BdG eigenvalue near $\Gamma$ is negative, and the transverse speed at $q\to0$ equals the static value $\sqrt{\mu/\rho_n}$, with $\mu$ the shear modulus, to $5\times10^{-5}$. (A looser convergence leaves a slightly negative translational zero mode, which lowers every acoustic branch by a constant offset in $\omega^2$; at the wavevectors used below this biases the transverse speed low by up to 1 %.) Bogoliubov–de Gennes (BdG) excitations follow from the Hermitian form $L^{1/2}(L+2X)L^{1/2}$ in a basis of $32^2$ plane waves (checked at $40^2$). Here $L=-\tfrac12\nabla^2+U*\rho_0-\mu_c$, with $\mu_c$ the chemical potential, and $X f=\psi_0\,U*(\psi_0f)$. For each mode we compute the density matrix element $\rho_\nu(\mathbf q)=\int_{\rm cell}e^{-i\mathbf q\cdot\mathbf r}\psi_0 f_{+,\nu}$ with the BdG normalization $\int(|u|^2-|v|^2)=1$, and the weight $Z_\nu=|\rho_\nu|^2$. Two sum rules are imposed at every wavevector. The f-sum $\sum_\nu\omega_\nu Z_\nu=N_{\rm cell}q^2/2$, and the static sum $\sum_\nu 2Z_\nu/\omega_\nu$, which must equal a direct solution of $(L+2X)f=-2e^{i\mathbf q\cdot\mathbf r}\psi_0$. Both hold to $10^{-6}$ in every run. Modes are identified by polarization rather than by frequency order. The transverse mode is the gapless mode with zero density weight ($\le10^{-17}$ along both inequivalent mirror directions, parallel to a lattice vector and at 30° to it). The other two gapless modes are the longitudinal pair, so an inversion $c_2>c_T$ would be detected. Speeds are least-squares slopes over $|\mathbf q|a/2\pi\in[0.03,0.10]$ for $\mathbf q$ parallel to a lattice vector (the 30° direction agrees to 0.1 %). Weights are quoted at $|\mathbf q|a/2\pi=0.05$; across the fit window $Z_\nu/q$ varies by about 1 % at $g=22$ and by up to 20 % at $g=12.7$.

**The canonical state** ($g=22$, lattice constant $a=1.4575$, $\mu_c=55.85$) has superfluid fraction $f_s=0.095$. The three branches are $c_2=1.80$, $c_T=5.80$ and $c_1=11.17$, so second sound runs at $0.31\,c_T$. It carries $Z_2/Z_1=0.34$ of first sound's spectral weight, 5.1 % of the f-sum and 67 % of the static density response. Table 1 compares the BdG numbers with an independent static route. There the superfluid fraction comes from the energy of a phase twist [43], $E(k)-E(0)=\tfrac12Nf_sk^2$, and the moduli from finite strains of the relaxed cell; no excitation is computed. Inserted into Sec. 3, these give the BdG weights to 1 %. Along the way the elastic tensor turns out to be of Cauchy class: $C_{xxyy}/C_{xyxy}=0.998$. The ratio $c_T/c_1=0.52$ therefore lies below the Cauchy value $1/\sqrt3$ not because of the lattice, but because $c_T^2=\mu/\rho_n$ [41] while first sound is stiffened by the superfluid compressibility. In Eq. (1), $M/\rho\gamma=11.4$: the two coefficients whose equality would decouple second sound differ by an order of magnitude.

*Table 1. Canonical 2D state ($g=22$): BdG versus static hydrodynamics (speeds in units $\hbar/mR$). BdG speeds are least-squares slopes over $|\mathbf q|a/2\pi\in[0.03,0.10]$ and include the weak dispersion of the branches; at $q\to0$ the BdG values are $c_2=1.817$, $c_T=5.812$, $c_1=11.208$.*

| quantity | BdG | static route (Sec. 3) |
|---|---|---|
| $c_2$ (= $c_-$) | 1.803 | 1.817 |
| $c_T$ | 5.803 | 5.811 ($=\sqrt{\mu/\rho_n}$) |
| $c_1$ (= $c_+$) | 11.170 | 11.209 |
| $F_-$ (f-sum share) | 0.0515 | 0.0518 |
| $Z_2/Z_1$ | 0.336 | 0.337 |
| $S_-$ (static share) | 0.675 | 0.675 |
| $\chi(q\to0,0)$ per cell | 0.04275 | 0.04275 |
| inputs | — | $f_s=0.0952$, $\alpha=43.73$, $M=91.61$, $C_{xxyy}=30.51$, $\mu=30.56$, $\gamma=8.02$ |

**Generality.** Table 2 shows the interaction sweep from $g=44$ down to the melting transition, plus one state with a different kernel shape ($U=g\,e^{-(r/R)^6}$, $g=35$). Across the stable supersolid phase, up to the coexistence boundary $\Lambda_c$ of Sec. 5 (values there interpolated), second sound runs at 0.07–0.77 of the shear speed. It carries 0.3–41 % of the f-sum and 64–80 % of the static response. Its weight never vanishes, and it falls smoothly with $f_s$, as Eq. (1) requires.

*Table 2. Soft-core supersolid in 2D. Speeds in units $\hbar/mR$; $F_2$ and $S_2$ are second sound's shares of the f-sum and of the static response; $Z_2/Z_1$ is its spectral weight relative to first sound. Speeds are least-squares slopes over $|\mathbf q|a/2\pi\in[0.03,0.10]$; weights are read at 0.05. Near melting, gapped modes take up to 3 % of the f-sum at that wavevector and the branches disperse, so $Z_2/Z_1$ exceeds the two-branch value $[F_2/(1-F_2)](c_1/c_2)$ of Sec. 3 by up to 9 % (at $g=12.7$; 1.5 % at $g=13.5$). Dashes: not computed twice, so not cited.*

| $g$ | $a$ | $f_s$ | $c_2$ | $c_T$ | $c_1$ | $c_2/c_T$ | $F_2$ | $Z_2/Z_1$ | $S_2$ |
|---|---|---|---|---|---|---|---|---|---|
| 44 | 1.393 | 0.0055 | 0.596 | 8.709 | 16.09 | 0.068 | 0.003 | 0.088 | 0.70 |
| 34 | 1.417 | 0.018 | 0.950 | 7.464 | 14.03 | 0.127 | 0.010 | 0.149 | 0.69 |
| 28 | 1.435 | 0.039 | 1.288 | 6.658 | 12.67 | 0.194 | 0.021 | 0.215 | 0.68 |
| 22 | 1.457 | 0.095 | 1.803 | 5.803 | 11.17 | 0.311 | 0.051 | 0.336 | 0.67 |
| 20 | 1.467 | 0.132 | 2.039 | 5.508 | 10.62 | 0.370 | 0.072 | 0.403 | 0.68 |
| 18 | 1.477 | 0.189 | 2.326 | 5.208 | 10.04 | 0.447 | 0.104 | 0.501 | 0.68 |
| 16 | 1.488 | 0.278 | 2.689 | 4.906 | 9.41 | 0.548 | 0.160 | 0.665 | 0.70 |
| 15 | 1.495 | 0.345 | 2.912 | 4.754 | 9.05 | 0.613 | 0.206 | 0.807 | 0.71 |
| 14 | 1.502 | 0.436 | 3.173 | 4.604 | 8.65 | 0.689 | 0.278 | 1.059 | 0.74 |
| 13.5 | 1.506 | 0.497 | 3.317 | 4.529 | 8.42 | 0.732 | 0.335 | 1.295 | 0.77 |
| 13.0* | 1.510 | 0.576 | 3.451 | 4.455 | 8.13 | 0.775 | 0.423 | 1.787 | 0.81 |
| 12.7† | 1.513 | 0.640 | 3.475 | 4.410 | 7.88 | 0.788 | 0.513 | 2.596 | 0.86 |
| 12.5† | 1.515 | 0.698 | 3.321 | 4.379 | 7.61 | 0.758 | 0.615 | — | — |
| 12.4† | 1.517 | 0.74 | 2.878 | 4.362 | 7.36 | 0.660 | 0.691 | — | — |
| 35 ($e^{-r^6}$) | 1.438 | 0.094 | 2.177 | 6.647 | 13.53 | 0.328 | 0.043 | 0.281 | 0.64 |

\* 0.04 below the coexistence boundary $\Lambda_c=13.04$ (Sec. 5), on the metastable side; the stable-phase ranges in the text are taken at $\Lambda_c$. † metastable continuation of the crystal branch; below $g\approx12.38$–$12.40$ its long-wavelength second-sound frequency becomes imaginary (Sec. 5).

**Three dimensions.** In 3D the same functional (step kernel, $\Lambda=\bar\rho U_0R^3$ at twice its roton threshold) selects a close-packed stack. The hexagonal (AB) stacking is lowest, nearly degenerate with fcc. We computed the BdG weights on the AB crystal ($a=1.386$, $c=2.260$) in a basis of 3,455 plane waves ($|\mathbf G|\le30$), with the state converged inside that basis. (With 1,355 waves, $|\mathbf G|\le22$, the three translational Goldstone modes acquire small negative $\omega^2$ and the transverse speeds come out up to 6 % low.) The sum rules again hold to $10^{-6}$. At $|\mathbf q|=0.15$ second sound is at $c_2=0.471$, against shear speeds of 7.75–8.04 (the lattice is elastically anisotropic) and first sound at 16.1–17.0. That gives $c_2/c_T\simeq0.06$. Second sound carries only 0.17 % of the f-sum but $Z_2/Z_1=0.057$–$0.063$ and 66–69 % of the static response. The compressibility speed is $c_\kappa=9.38\approx1.2\,c_T$.

## 5. Approach to melting

Does $c_2/c_T$ reach one anywhere inside the supersolid phase? At fixed density the free energy per area of a phase is $f(\rho)=\rho\,\varepsilon(g\rho)$, where $\varepsilon(\Lambda)$ is the energy per particle at unit density and coupling $\Lambda$. For the uniform state $\varepsilon_u=\pi\Lambda/2$ and $\mu_u=\pi\Lambda$. Equal chemical potential and pressure between the crystal and the uniform phase (the common tangent) give the crystal-side boundary $\Lambda_c$ as the root of
$$\Lambda\,(\mu_c-\varepsilon_c)=\frac{\mu_c^2}{2\pi},$$
with $\mu_c$ the Gross–Pitaevskii chemical potential of the crystal. Following the crystal branch continuously (Table 2) gives $\Lambda_c=13.04$. The uniform-side boundary is $\Lambda_u=\mu_c(\Lambda_c)/\pi=12.23$, and the fixed-density energy crossing at $g=12.57$ lies between them, close to the 12.7 reported in Ref. [35].

Approaching the boundary, $c_2/c_T$ rises monotonically to 0.77 at $\Lambda_c$. On the metastable branch it peaks at 0.79 near $g=12.7$ and then falls (Table 2): second sound softens as the crystal approaches its spinodal, and below $g\approx12.38$–$12.40$ its long-wavelength frequency becomes imaginary, so the crystal stops being a local minimum. **The ratio never reaches one.** The end of the metastable branch realizes the labile limit of Sec. 9, $c_2\to0$, rather than a shared cone. This agrees with the ordering reported in Ref. [38] and extends it to the phase boundary. Coupling to the slow branch strengthens on the way: its f-sum share grows to 0.41 at $\Lambda_c$ and $Z_2$ comes to exceed $Z_1$. Moving the medium toward melting does not help.

Hydrodynamics does not exclude $c_->c_T$ in principle, and two routes lead there. If the modulation could vanish continuously, with $\rho_n$, $M$, $\gamma$ and $\mu$ all scaling as the modulation squared, the dispersion polynomial would factor as $(x-M/\rho_n)(x-\rho\alpha)$. The lower longitudinal speed would then tend to $\min(\sqrt{M/\rho_n},\sqrt{\rho\alpha})$, which can exceed $c_T=\sqrt{\mu/\rho_n}$. In the soft-core model the first-order transition intervenes first. The second route is Green's limit of Sec. 9, a nearly incompressible condensate ($\alpha\to\infty$). There $c_+\to\infty$ and
$$\frac{c_-^2}{c_T^2}\to f_s\,\frac{\tilde M}{\mu},\qquad \tilde M=\lim_{\alpha\to\infty}\Big(M-\frac{\gamma^2}{\alpha}\Big),$$
where $f_s=\rho_s/\rho$ and $\tilde M$ is the uniaxial modulus at fixed chemical potential ($\tilde M=M$ if $\gamma$ stays finite). For an isotropic lattice in $d$ dimensions, positive-definite energy requires $\alpha K>\gamma^2$, with $K$ the lattice bulk modulus at fixed density, so $\tilde M\ge2(d-1)\mu/d$. Second sound then outruns shear whenever $f_s>d/[2(d-1)]$: $f_s>3/4$ in three dimensions, whereas in two dimensions no $f_s<1$ suffices. These statements were derived twice, independently (supplementary S6). The soft-core crystal is far from this corner, since its first sound is only about twice the shear speed. Either way the two speeds are set by different material combinations, and equality is a coincidence.

## 6. How a vortex couples to the medium

A moving vortex reaches the density, and through it both longitudinal branches, in two independent ways.

*Through its core.* A vortex line in a one-component condensate has a node on its axis, so its core carries a density deficit of order $\rho\xi^2$ per unit length ($\xi$ the healing length). A second component can fill the core [44–46] and flatten the total-density dip. Exact cancellation of the total density everywhere, however, requires the symmetric point of the intra- and inter-component couplings together with a matched filling profile, a measure-zero condition. For immiscible components the interface between core and filling carries a density depression of its own. A generic localized knot therefore keeps a residual total-density deficit (or excess) $\epsilon\neq0$.

*Through its flow.* Write the phase as $\theta=\theta_v(\mathbf r-\mathbf vt)+\varphi$. Here $\theta_v$ is the phase of a vortex moving at velocity $\mathbf v$, $\mathbf v_s=\nabla\theta_v$ is its own superflow, divergence-free with circulation $\kappa=2\pi\hbar/m$, and $\varphi$ is the fluctuation. The quadratic Lagrangian of Sec. 3 omits the cubic part $-\tfrac12\delta\rho|\nabla\theta|^2$ of the Galilean-invariant superfluid term $-(\rho+\delta\rho)(\dot\theta+\tfrac12|\nabla\theta|^2)$, which around a vortex contributes at linear order. With $\dot\theta_v=-\mathbf v\cdot\mathbf v_s$, and $\rho_n$ constant as in Sec. 3, the terms linear in the fluctuations are
$$\mathcal L_1=-\delta\rho\left(\tfrac12|\mathbf v_s|^2-\mathbf v\cdot\mathbf v_s\right)-\rho_n\,\dot{\mathbf u}\cdot\mathbf v_s ,$$
since every cross term of $\mathbf v_s$ with $\nabla\varphi$, or with the longitudinal part of $\mathbf u$, integrates to zero against a divergence-free flow. The first term is a density potential, the Bernoulli pressure of the flow seen from the moving vortex ($\tfrac12|\mathbf v_s-\mathbf v|^2$ up to a constant), and it enters Eq. (2) with the same weights $F_\nu$, with $|V|^2$ averaged over each branch's Cherenkov cone. Its velocity-dependent part comes from $-\delta\rho\,\dot\theta$ alone, so the circulation quantum fixes its strength and no filling of the core removes it. For a vortex ring of radius $b$ moving along its axis $\hat{\mathbf z}$, the flow at $qb\ll1$ is $\mathbf v_s(\mathbf q)=\pi\kappa b^2(\hat{\mathbf z}-\hat{\mathbf q}\hat q_z)$, so $|\mathbf v\cdot\mathbf v_s(\mathbf q)|\le\pi\kappa b^2v$. The bound is nearly reached on the second-sound Cherenkov cone, whose wavevectors are almost perpendicular to the motion. For $b\approx\xi\approx\hbar/mc_\kappa$ and $v$ near $c_T$, this part alone exceeds the deficit vertex of Sec. 7 with $\epsilon=1$ by an order of magnitude. The second term of $\mathcal L_1$ is a force on the lattice. Its source $\mathbf v_s$ is transverse, so in an isotropic lattice it excites shear alone, and a vortex faster than $c_T$ radiates shear. $\mathcal L_1$ and the ring vertex were derived twice, the second time blind (supplementary S6). If $\rho_n$ depends on density and on lattice dilatation $\nabla\cdot\mathbf u$, as it generally does, $|\mathbf v_s|^2$ also couples to both, with coefficients $\tfrac12\partial\rho_n/\partial\rho$ and $\tfrac12\partial\rho_n/\partial(\nabla\cdot\mathbf u)$. That changes the coefficient of the static part, $\tfrac12$ above, and adds a coupling to lattice strain; we do not treat either.

## 7. Drag, radiation and loss length

**Landau criterion.** A defect moving at speed $v$ can emit into branch $\nu$ when $v>\min_q\omega_\nu(q)/q$. With several branches the critical speed is the smallest over the branches it couples to. A vortex couples to both longitudinal branches through density and to shear through the normal fraction (Sec. 6), so its critical speed is $\min(c_2,c_T)$; in the computed model that is $c_2$. The lowest supersolid branch also sets the Landau instability of superflow [37]. In stripe supersolids the critical velocity even vanishes for motion that is not parallel to the stripes [48].

**Drag.** For a defect that couples to density through a potential with Fourier transform $V(\mathbf q)$, Fermi's golden rule with the response of Sec. 3 gives the drag force from each supercritical branch:
$$F_d^{(3D)}=\sum_{\nu:\,c_\nu<v}\frac{\rho F_\nu}{4\pi v^2}\int_0^\infty q^3|V(q)|^2\,dq ,\qquad
f_d^{(\rm line)}=\sum_{\nu:\,c_\nu<v}\frac{\rho F_\nu}{2\pi v^2\sqrt{1-c_\nu^2/v^2}}\int_0^\infty q^2|V(q)|^2\,dq ,\tag{2}$$
for a point-like defect and per unit length of a straight filament, respectively. The drag is **proportional to the branch's f-sum share and, for an isotropic point source, independent of the branch speed** above threshold. For a single Bogoliubov branch with $F=1$, a contact vertex $V=g_i$ and the dispersion cutoff $q_{\max}=2\sqrt{v^2-c^2}$, Eq. (2) reduces to $F_d=n g_i^2(v^2-c^2)^2/(\pi v^2)$, which is Eq. (12) of Astrakharchik and Pitaevskii [47] in our units. Supersonic motion in a Gross–Pitaevskii fluid is genuinely dissipative: no finite-energy supersonic travelling waves exist [49].

**Radiation.** A source of multipole order $\ell$ oscillating at frequency $\Omega$ with a fixed density vertex puts power $P_\nu\propto F_\nu\,\Omega^{2\ell+d+1}/c_\nu^{2\ell+d+2}$ into branch $\nu$ in $d$ dimensions. A slow branch is therefore favoured by a high power of $c_1/c_2$. With the 3D numbers ($c_1/c_2=34$–$36$, $F_2/F_1=0.0017$) a quadrupole radiates about $10^{11}$ times more power into second sound than into first sound.

**Loss length.** As an order-of-magnitude estimate, take a defect of size $\xi$ with static deficit $\delta N=\epsilon\rho\xi^3$ and rest energy $E_0=\tau\rho c_T^2\xi^3$, with $\epsilon$ and $\tau$ dimensionless. The static relation $\delta n=\chi(q,0)V$ with $\chi(q\to0,0)=-\rho/c_\kappa^2$ gives $|V|\simeq c_\kappa^2\delta N/\rho$ up to $q\sim1/\xi$. Equation (2) then gives the energy-loss length of an ultrarelativistic defect with Lorentz factor $\Gamma$ ($v\to c_T$):
$$\ell\simeq\frac{16\pi\tau}{\epsilon^2}\left(\frac{c_T}{c_\kappa}\right)^4\frac{\Gamma\,\xi}{F_2}\approx1.5\times10^5\,\Gamma\,\xi ,\tag{3}$$
using the 3D values ($c_T\approx7.85$, the mean over directions and polarizations; $c_\kappa=9.38$; $F_2=0.0017$), $\tau=10$ and $\epsilon=1$. Two corrections roughly cancel. The flow vertex of Sec. 6 is larger by about an order of magnitude, which shortens $\ell$ by about two orders. Equation (3) also takes the hydrodynamic response up to $q\approx1/\xi\approx9$, past the 3D zone edge (1.4–3.0); cutting it at the zone edge would lengthen $\ell$ by two to three orders. Cosmic-ray protons of $3\times10^{11}$ GeV ($\Gamma\approx3.2\times10^{11}$) that cross the Galaxy (10 kpc) require $\ell\gtrsim3\times10^{20}$ m, hence $\xi\gtrsim6\times10^3$ m: defects kilometres across. A defect of proton size ($\xi\approx1$ fm) falls short by about 19 orders of magnitude, and one of Planck size by about 39. A more detailed evaluation with explicit two-component vortex-ring profiles gives $\xi\gtrsim2\times10^4$ m and the same Planck-size shortfall (supplementary S5). Since Eq. (2) has no near-threshold suppression for linear branches, at fixed coupling and defect size the only escape is kinematic: every particle must stay below $c_2$, which for the most energetic cosmic rays means
$$1-\frac{c_2}{c_T}\lesssim\frac{1}{2\Gamma^2}\approx5\times10^{-24},\tag{4}$$
the same order as Coleman and Glashow's bound on vacuum Cerenkov radiation of charged particles [12]. In the computed model $1-c_2/c_T$ lies between 0.21 and 0.94. The other way out is a weaker coupling: for a defect of proton size, every coupling to second sound some 19 orders of magnitude below the computed one. For the density vertices that means a second-sound share $F_2\propto(M-\rho\gamma)^2$ (Eq. 1) suppressed that far. Either $M$ and $\rho\gamma$ must then coincide to one part in $10^9$ or better, a fine-tuning of its own, or the medium must approach the incompressible limit of Sec. 9. Neither removes a coupling through lattice strain (Secs. 6 and 9).

## 8. Binding and drag

Two static defects with vertices $V_1$ and $V_2$ interact through the medium with $U_{\rm ind}(\mathbf q)=V_1(\mathbf q)V_2(\mathbf q)\,\chi(\mathbf q,0)$. For like defects this is attractive. Its range is set by the vertices, because $\chi(q,0)$ is finite as $q\to0$ in a compressible medium. The result is a short-range attraction over a healing length or lattice spacing, the analogue of the phonon-induced Yukawa attraction between impurities in a condensate [50,51]. In the stable supersolid, 64–80 % of $\chi(q,0)$ is carried by second sound, and more on the metastable branch (Tables 1–2). For a defect whose vertex does not depend on its velocity, such as a core deficit, the vertex that binds at short range is the vertex that makes it radiate when fast, and second sound carries most of the static response and all of the radiation below $c_T$. Neither can then be removed without most of the other. A moving vortex adds the velocity-dependent flow vertex of Sec. 6, which radiates but does not bind, so for vortex matter removing the binding would not remove the drag.

## 9. Escapes, and the elastic-ether debate

The difficulty is old. An elastic-solid ether carries a longitudinal wave as well as the transverse light wave. Green observed that the longitudinal wave could be avoided "by supposing its velocity to be indefinitely great or indefinitely small", and chose the former, an incompressible medium, because a medium with negative compressibility would be unstable [52,53]. Cauchy nonetheless adopted the latter: the contractile ether, of negative compressibility "such as to make the velocity of the longitudinal wave zero". Kelvin revived it as the labile ether [52,55]. MacCullagh took a third route. In his medium "the potential energy depends only on the rotation of the volume-elements", and "no longitudinal waves exist at any time" [52,54]. FitzGerald later mapped this medium onto Maxwell's equations [56,57]. Modern revivals of the incompressible choice exist [58].

Each route has a supersolid counterpart.

*Green's limit* ($\alpha\to\infty$) sends $c_+\to\infty$ and, by Eq. (1), $F_-\to0$, as $\alpha^{-2}$ at fixed $\gamma$ and as $\alpha^{-1}$ if $\gamma$ grows like $\sqrt\alpha$. Second sound decouples from density. It does not disappear, however: it survives at $c_-^2=f_s\tilde M/\rho_n$ (Sec. 5; this is $c_*^2$ at fixed $\gamma$) as a counterflow of superfluid against lattice that carries neither density nor mass current. With $\rho_n$ constant, as in Sec. 3, a vortex whose core shrinks with the healing length then no longer reaches it at linear order: its density vertices (Sec. 6) act through the density response, which vanishes in this limit, and its flow pushes on the lattice only transversely. A core that keeps a fixed deficit still couples, because the potential that holds the deficit grows like $c_\kappa^2\propto\alpha$ and offsets $F_-\propto\alpha^{-2}$. So does a vortex that strains the lattice, as it generically does through the strain dependence of $\rho_n$ (Sec. 6), and so does any defect that strains the lattice directly, as edge dislocations do. We do not evaluate these couplings. Where the branch sits is set by $f_s\tilde M/\mu$: in an isotropic three-dimensional lattice, a superfluid fraction above 3/4 puts it above the shear speed. Then every mode that matter couples to is at least as fast as light, the drag-free range of a defect that couples to shear ends at the shear speed, and the argument of this paper does not apply.

*The labile limit* ($c_-\to0$) is the worst case: every moving defect radiates. The soft-core crystal reaches it at the end of its metastable branch (Sec. 5).

*MacCullagh's medium* is the genuine exception, because it has no longitudinal restoring force at all. The longitudinal sector is excluded by initial conditions rather than by a large speed, and that is untenable once matter is a moving density source, which keeps generating compressional disturbances. A rotational medium also has no condensate phase. Adding superfluid order to host vortex matter brings back a compressional phase mode whose speed is set by compressibility, not by rotational stiffness.

The Cosserat-supersolid proposal [28] gives its nodes independent rotations, which MacCullagh's medium lacks, and keeps compression: it takes Green's route. Its superfluid enters as a bulk modulus $K_{\rm sf}\approx3\times10^{40}\mu$, which makes its one compression branch about $1.7\times10^{20}$ times faster than light, and it accepts the two causal cones and the preferred frame that result [28, Secs. 5.11, 5.12.4 and 6.6.1]. Its matter is crystal defects, chiefly dislocations, whose limiting speed it takes to be the shear speed [28, Secs. 6.7 and 20.2; 29,30]. It counts the superfluid phase mode among its Goldstone modes but gives it no branch of its own [28, Secs. 10.6.5, 20.10 and 25.9]. Its no-drag claim is asserted rather than derived. The friction it evaluates is Peierls and Bragg friction from the periodic potential [28, Secs. 9.6 and 20.2], and where its defects emit compression waves it treats them as a pilot wave or as background noise, never as a loss. The relation of Sec. 5 supplies the missing branch. At the proposal's superfluid fraction $f_s=4/5$ [28, Sec. 5.7.4], second sound lies at no less than $1.03\,c_T$ for any stable isotropic lattice ($1.10\,c_T$ if the lattice is taken as four-dimensional). With the Cauchy moduli the proposal quotes for its crystalline sector ($K/\mu=5/3$ [28, Sec. 25.3]) and a finite $\gamma$, it lies near $1.5\,c_T$. The Landau–Cherenkov drag of Sec. 7 is then closed to its matter, provided the medium obeys the hydrodynamics of Sec. 3; its further Cosserat branches are outside this analysis. The drag would open for $f_s\tilde M/\mu<1$, which needs $f_s<3/4$ ($2/3$ in four dimensions), for defects that strain the lattice, as edge dislocations do.

## 10. Discussion

In a supersolid model of the vacuum, matter's drag-free range ends at the slowest sound it couples to, and light's speed is the shear speed. A vortex couples to both longitudinal sounds through density and to shear through the normal fraction (Sec. 6), and no symmetry ties the speeds together. In the soft-core Gross–Pitaevskii supersolid second sound is slower than shear throughout the stable phase in two dimensions and in the three-dimensional crystal we computed, and the coupling to it is generic, Eq. (1). Fast matter therefore radiates into the vacuum, and a common causal cone requires second sound to come within about $10^{-23}$ of the shear speed, or its coupling to matter to be tuned away (Sec. 7). The general principle, that multiple sound speeds mean multiple metrics and tuning, is established [1–8]. This paper supplies the concrete mechanism and numbers for the supersolid class. Within it, superfluidity removes drag only below the slowest sound that matter couples to, and the superfluid itself supplies that sound.

The limitations are those of the model. We use mean-field Gross–Pitaevskii theory at zero temperature, one family of soft-core kernels plus one variant, and linear response. The size of the coupling is model-dependent, but the conclusion has a wide margin: even a defect of proton size falls short in Eq. (3) by about 19 orders of magnitude. The regime $c_2>c_T$ is not realized here. It is not excluded in media with a continuous transition, or in a nearly incompressible, isotropic three-dimensional supersolid with $f_s>3/4$ (Sec. 5). There every mode that matter couples to is at least as fast as light. Matter that couples to shear, which includes dislocations such as the defects of Ref. [28] and, through the normal fraction, vortices (Sec. 6), then has its drag-free range end at the shear speed, and the argument of this paper does not apply. Whether a real supersolid can reach that regime is the question this leaves open.

The contrast with relativistic field theory is instructive. In a Lorentz-invariant theory a moving soliton is the boost of a static one, so it never radiates, and matter and light share the cone automatically [62]. Skyrmions [59] and the knotted solitons of the Faddeev–Niemi model [60,61] realize "matter as knots" in that setting. A medium vacuum that wants knot matter has to reproduce this property, rather than approximate it by tuning.

## Acknowledgments

The author used an AI system (Claude, Anthropic) for the numerical work and the drafting, and takes full responsibility for the content. The checks were also made by AI agents, not by human referees. Separate AI reviewers re-derived the hydrodynamic formulas and checked the revised draft. A separate AI coding agent (Claude Code) recomputed the cited numbers in a blind second computation; the Table 2 rows outside that comparison and the added superfluid fractions were recomputed afterwards with its code, not blind (supplementary S8). Separate agent instances derived the analytic results of Secs. 5 and 6 a second time, blind.

## Data and code availability

All scripts and data are in the supplementary material (repository `gifgaf0/gifgaf0.github.io`, directory `lbc_bank/`; the index with paths and checksums is `lbc_bank/README.md`). S1 `lbc_weights.py` (2D BdG weights and sum rules); S2 `lbc_hydro.py` (static hydrodynamic route); S3 `lbc_3d.py` (3D weights); S4 `lbc_sweep_low.py`, `lbc_sweep_refine.py` (interaction sweep, coexistence boundary); S5 `step3_loss_length.py` (loss length with explicit two-component profiles); S6 `paper_identities_check.py` and the external re-derivation `verify_lbc_external.py`, plus the Green's-limit relation of Sec. 5 and the vortex couplings of Sec. 6, each derived twice (`green_limit_check.py` and the blind `green_limit_second_leg/`; `vortex_coupling_check.py` and the blind `vortex_coupling_second_leg/`); S7 `second_leg/` (the blind second computation; numbers it did not cover were recomputed in S8); S8 `closure/` (the corrected first computation: converged 2D states, the 3D basis at $|\mathbf G|\le30$, the melting end, and the comparison of the two computations; the tables of this paper are `closure/paper_tables_v2.json`, with the remaining superfluid fractions of Table 2 computed twice in `closure/fs_rows.py` and `closure/fs_rows_cc.py`, and the Table 2 rows outside the blind comparison recomputed with the second computation's code in `closure/table2_cc_rows.py` and `closure/table2_cc_g124_modecheck.py`); `paper/revision_numbers_check.py` (the arithmetic behind the derived numbers of Secs. 6–7 and the Table 2 notes); all JSON outputs, with checksums.

## References

[1] C. Barceló, S. Liberati, M. Visser, "Analogue gravity," Living Rev. Relativ. 14, 3 (2011) [first edition: 8, 12 (2005)].
[2] C. Barceló, S. Liberati, M. Visser, "Refringence, field theory, and normal modes," Class. Quantum Grav. 19, 2961 (2002), arXiv:gr-qc/0111059.
[3] M. Visser, S. Weinfurtner, "Massive Klein-Gordon equation from a Bose-Einstein-condensation-based analogue spacetime," Phys. Rev. D 72, 044020 (2005), arXiv:gr-qc/0506029.
[4] S. Liberati, M. Visser, S. Weinfurtner, "Naturalness in an emergent analogue spacetime," Phys. Rev. Lett. 96, 151301 (2006), arXiv:gr-qc/0512139.
[5] S. Liberati, M. Visser, S. Weinfurtner, "Analogue quantum gravity phenomenology from a two-component Bose–Einstein condensate," Class. Quantum Grav. 23, 3129 (2006), arXiv:gr-qc/0510125.
[6] J. Collins, A. Perez, D. Sudarsky, L. Urrutia, H. Vucetich, "Lorentz invariance and quantum gravity: an additional fine-tuning problem?," Phys. Rev. Lett. 93, 191301 (2004), arXiv:gr-qc/0403053.
[7] S. Chadha, H. B. Nielsen, "Lorentz invariance as a low energy phenomenon," Nucl. Phys. B 217, 125 (1983).
[8] M. M. Anber, J. F. Donoghue, "The emergence of a universal limiting speed," Phys. Rev. D 83, 105027 (2011), arXiv:1102.0789.
[9] G. E. Volovik, *The Universe in a Helium Droplet* (Oxford University Press, 2003).
[10] G. E. Volovik, "Reentrant violation of special relativity in the low-energy corner," JETP Lett. 73, 162 (2001), arXiv:hep-ph/0101286.
[11] S. Coleman, S. L. Glashow, "Cosmic ray and neutrino tests of special relativity," Phys. Lett. B 405, 249 (1997), arXiv:hep-ph/9703240.
[12] S. Coleman, S. L. Glashow, "High-energy tests of Lorentz invariance," Phys. Rev. D 59, 116008 (1999), arXiv:hep-ph/9812418.
[13] G. D. Moore, A. E. Nelson, "Lower bound on the propagation speed of gravity from gravitational Cherenkov radiation," JHEP 09 (2001) 023, arXiv:hep-ph/0106220.
[14] T. Jacobson, D. Mattingly, "Gravity with a dynamical preferred frame," Phys. Rev. D 64, 024028 (2001), arXiv:gr-qc/0007031.
[15] J. W. Elliott, G. D. Moore, H. Stoica, "Constraining the new aether: gravitational Cherenkov radiation," JHEP 08 (2005) 066, arXiv:hep-ph/0505211.
[16] T. Jacobson, S. Liberati, D. Mattingly, "Lorentz violation at high energy: concepts, phenomena and astrophysical constraints," Ann. Phys. 321, 150 (2006), arXiv:astro-ph/0505267.
[17] G. E. Volovik, "Superfluid analogies of cosmological phenomena," Phys. Rep. 351, 195 (2001), arXiv:gr-qc/0005091.
[18] K. Huang, "Dark energy and dark matter in a superfluid universe," Int. J. Mod. Phys. A 28, 1330049 (2013), arXiv:1309.5707.
[19] K. G. Zloshchastiev, "Logarithmic nonlinearity in theories of quantum gravity: origin of time and observational consequences," Grav. Cosmol. 16, 288 (2010), arXiv:0906.4282.
[20] V. I. Sbitnev, "Hydrodynamics of the physical vacuum: I. Scalar quantum sector," Found. Phys. 46, 606 (2016).
[21] H. Kleinert, "Gravity as a theory of defects in a crystal with only second gradient elasticity," Ann. Phys. (Leipzig) 499, 117 (1987).
[22] H. Kleinert, J. Zaanen, "Nematic world crystal model of gravity explaining absence of torsion in spacetime," Phys. Lett. A 324, 361 (2004), arXiv:gr-qc/0307033.
[23] M. Danielewski, "The Planck–Kleinert crystal," Z. Naturforsch. A 62, 564 (2007).
[24] S. Bernadotte, F. R. Klinkhamer, "Bounds on length scales of classical spacetime foam models," Phys. Rev. D 75, 024028 (2007), arXiv:hep-ph/0610216.
[25] J. Zaanen, Z. Nussinov, S. I. Mukhin, "Duality in 2+1D quantum elasticity: superconductivity and quantum nematic order," Ann. Phys. (N.Y.) 310, 181 (2004), arXiv:cond-mat/0309397.
[26] A. J. Beekman et al., "Dual gauge field theory of quantum liquid crystals in two dimensions," Phys. Rep. 683, 1 (2017), arXiv:1603.04254.
[27] M. Pretko, L. Radzihovsky, "Fracton-elasticity duality," Phys. Rev. Lett. 120, 195301 (2018), arXiv:1711.11044.
[28] M. A. Cox, "The Cosserat supersolid: deriving the constants of nature from vacuum lattice mechanics," Zenodo preprint, v4 (2026), doi:10.5281/zenodo.20705475.
[29] F. C. Frank, "On the equations of motion of crystal dislocations," Proc. Phys. Soc. A 62, 131 (1949).
[30] J. D. Eshelby, "Uniformly moving dislocations," Proc. Phys. Soc. A 62, 307 (1949).
[31] Y. Pomeau, S. Rica, "Dynamics of a model of supersolid," Phys. Rev. Lett. 72, 2426 (1994).
[32] C. Josserand, Y. Pomeau, S. Rica, "Coexistence of ordinary elasticity and superfluidity in a model of a defect-free supersolid," Phys. Rev. Lett. 98, 195301 (2007).
[33] N. Henkel, R. Nath, T. Pohl, "Three-dimensional roton excitations and supersolid formation in Rydberg-excited Bose-Einstein condensates," Phys. Rev. Lett. 104, 195302 (2010).
[34] S. Saccani, S. Moroni, M. Boninsegni, "Excitation spectrum of a supersolid," Phys. Rev. Lett. 108, 175301 (2012).
[35] T. Macrì, F. Maucher, F. Cinti, T. Pohl, "Elementary excitations of ultracold soft-core bosons across the superfluid-supersolid phase transition," Phys. Rev. A 87, 061602(R) (2013).
[36] F. Ancilotto, M. Rossi, F. Toigo, "Supersolid structure and excitation spectrum of soft-core bosons in three dimensions," Phys. Rev. A 88, 033618 (2013).
[37] M. Kunimi, Y. Kato, "Mean-field and stability analyses of two-dimensional flowing soft-core bosons modeling a supersolid," Phys. Rev. B 86, 060510(R) (2012), arXiv:1205.2126.
[38] E. Poli, D. Baillie, F. Ferlaino, P. B. Blakie, "Excitations of a two-dimensional supersolid," Phys. Rev. A 110, 053301 (2024), arXiv:2407.01072.
[39] A. F. Andreev, I. M. Lifshitz, "Quantum theory of defects in crystals," Sov. Phys. JETP 29, 1107 (1969).
[40] D. T. Son, "Effective Lagrangian and topological interactions in supersolids," Phys. Rev. Lett. 94, 175301 (2005).
[41] C.-D. Yoo, A. T. Dorsey, "Hydrodynamic theory of supersolids: variational principle, effective Lagrangian, and density-density correlation function," Phys. Rev. B 81, 134518 (2010).
[42] L. M. Platt, D. Baillie, P. B. Blakie, "Supersolid spectroscopy," Phys. Rev. A 111, 053305 (2025), arXiv:2412.15552.
[43] A. J. Leggett, "Can a solid be 'superfluid'?," Phys. Rev. Lett. 25, 1543 (1970).
[44] M. A. Metlitski, A. R. Zhitnitsky, "Vortex rings in two component Bose-Einstein condensates," JHEP 06 (2004) 017, arXiv:cond-mat/0307559.
[45] J. Ruostekoski, J. R. Anglin, "Creating vortex rings and three-dimensional skyrmions in Bose-Einstein condensates," Phys. Rev. Lett. 86, 3934 (2001), arXiv:cond-mat/0103310.
[46] R. A. Battye, N. R. Cooper, P. M. Sutcliffe, "Stable skyrmions in two-component Bose-Einstein condensates," Phys. Rev. Lett. 88, 080401 (2002), arXiv:cond-mat/0109448.
[47] G. E. Astrakharchik, L. P. Pitaevskii, "Motion of a heavy impurity through a Bose-Einstein condensate," Phys. Rev. A 70, 013608 (2004), arXiv:cond-mat/0307247.
[48] G. I. Martone, G. V. Shlyapnikov, "Drag force and superfluidity in the supersolid stripe phase of a spin-orbit-coupled Bose-Einstein condensate," JETP 127, 865 (2018), arXiv:1805.12552.
[49] P. Gravejat, "A non-existence result for supersonic travelling waves in the Gross–Pitaevskii equation," Commun. Math. Phys. 243, 93 (2003).
[50] A. Camacho-Guardian, G. M. Bruun, "Landau effective interaction between quasiparticles in a Bose-Einstein condensate," Phys. Rev. X 8, 031042 (2018).
[51] P. Naidon, "Two impurities in a Bose–Einstein condensate: from Yukawa to Efimov attracted polarons," J. Phys. Soc. Jpn. 87, 043002 (2018), arXiv:1607.04507.
[52] E. T. Whittaker, *A History of the Theories of Aether and Electricity* (Longmans, Green, London, 1910), ch. V.
[53] G. Green, "On the laws of the reflexion and refraction of light at the common surface of two non-crystallized media," Trans. Camb. Phil. Soc. 7, 1 (1838) [read December 1837].
[54] J. MacCullagh, "An essay towards a dynamical theory of crystalline reflexion and refraction," Trans. R. Irish Acad. 21, 17 [read December 1839].
[55] W. Thomson (Lord Kelvin), "On the reflexion and refraction of light," Phil. Mag. 26, 414 (1888).
[56] G. F. FitzGerald, "On the electromagnetic theory of the reflection and refraction of light," Phil. Trans. R. Soc. Lond. 171, 691 (1880).
[57] O. Darrigol, "James MacCullagh's ether: an optical route to Maxwell's equations?," Eur. Phys. J. H 35, 133 (2010).
[58] C. I. Christov, "On the nonlinear continuum mechanics of space and the notion of luminiferous medium," Nonlinear Anal. 71, e2028 (2009), arXiv:0804.4253.
[59] T. H. R. Skyrme, "A non-linear field theory," Proc. R. Soc. Lond. A 260, 127 (1961).
[60] L. Faddeev, A. J. Niemi, "Stable knot-like structures in classical field theory," Nature 387, 58 (1997), arXiv:hep-th/9610193.
[61] R. A. Battye, P. M. Sutcliffe, "Knots as stable soliton solutions in a three-dimensional classical field theory," Phys. Rev. Lett. 81, 4798 (1998), arXiv:hep-th/9808129.
[62] N. Manton, P. Sutcliffe, *Topological Solitons* (Cambridge University Press, 2004).
