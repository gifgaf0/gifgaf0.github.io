<!--
COVER NOTE FOR THE AUTHOR (remove before submission)
Plain-language summary: if empty space were a material, matter and light would both be features of it and would need
one shared speed limit. A popular version makes the material a supersolid (a crystal that is also a superfluid), with
light as its shear wave and particles as knotted whirlpools. This paper shows that a supersolid always has a second,
slower sound that the whirlpools are coupled to. Fast matter would make a sonic boom and lose its energy, unless that
sound speed equalled the light speed to about one part in 10^23. We compute this in a standard model supersolid in two
and three dimensions, up to the point where it melts; second sound always stays below the light speed. The general
worry is known; what is new is the concrete supersolid calculation and its numbers.
Status of numbers: every number below was computed once (single leg) with internal cross-checks (two sum rules, an
independent static hydrodynamic route, an external analytic re-derivation of the hydrodynamic formulas). A blind
second computation of the cited numbers is prepared (dispatch LBC_SECOND_LEG_DISPATCH_INBAND.md) but not yet run.
Citations: each was checked against its publisher, arXiv or INSPIRE record (see the citation log in lbc_bank/paper/).
Draft date: October 4, 2026.
-->

# Second sound breaks the common light cone of a supersolid vacuum

**Matt Gifford**
Independent researcher, Hollister, California, USA

## Abstract

Medium-based models of the vacuum must give matter and light one causal cone, and every excitation that matter couples to must be at least as fast as light. A supersolid is the natural medium for one popular picture: its superfluid order hosts vortex-knot "matter" and its shear rigidity carries transverse "light". We show that this picture fails generically. A supersolid has two longitudinal sounds. From zero-temperature supersolid hydrodynamics we obtain the fraction of the density response carried by the lower one (second sound), $F_- = \rho_s (M-\rho\gamma)^2/[\rho^2\rho_n (c_+^2-c_*^2)(c_+^2-c_-^2)]$. It vanishes only without superflow or under the coincidence $M=\rho\gamma$ between two independent elastic coefficients. We run Bogoliubov–de Gennes calculations for the soft-core Gross–Pitaevskii supersolid in two and three dimensions, checked against the f-sum and compressibility sum rules and against an independent static hydrodynamic route. Second sound comes out at 0.06–0.8 of the shear speed, carrying 0.2–41 % of the f-sum and 63–81 % of the static density response. Toward the first-order melting transition the ratio $c_2/c_T$ rises to 0.78 at the phase boundary and never reaches one. Vortex cores carry density deficits and circulation, so moving matter radiates second sound above $c_2<c_T$. The drag is proportional to the branch's f-sum share and independent of its speed, and the same vertex supplies the short-range static attraction between defects. Survival of ultra-high-energy cosmic rays then requires a macroscopic substrate scale ($\gtrsim 10^4$ m) or $|1-c_2/c_T| \lesssim 10^{-23}$. The result is a concrete instance of the fine-tuning problem of emergent Lorentz invariance, and we connect it to the nineteenth-century elastic-ether debate.

---

## 1. Introduction

Any attempt to model the vacuum as a medium has to pass a simple test. Matter and light must share one causal cone, and every excitation that matter couples to must propagate at least as fast as light. Otherwise sufficiently fast matter emits that excitation, as a supersonic body emits a wake, and loses energy.

In analogue gravity the test appears as the mono-metricity problem. A medium with several low-energy modes generically gives several effective metrics, and a single metric requires the mode speeds to coincide [1–5]. The coincidence is a tuning condition. Liberati, Visser and Weinfurtner showed explicitly that in a two-component condensate the two phonon branches share a limiting speed only under fine-tuning conditions [4,5]. In the emergent-gravity setting the same issue is the "additional fine-tuning problem" of Collins et al. [6], with Chadha–Nielsen [7] and Anber–Donoghue [8] showing that interactions can drive species toward a common speed only logarithmically. Volovik notes that near a Fermi point the different low-energy fermions share one "speed of light" only through a symmetry that connects the species [9,10].

The observational bite is severe. Coleman and Glashow assigned each species a maximal attainable velocity and pointed out that a charged particle faster than light "loses energy rapidly via vacuum Cerenkov radiation" [11,12]. Moore and Nelson turned the same argument on gravity. The survival of the highest-energy cosmic rays forces the graviton speed to exceed $c(1-2\times10^{-15})$ for a galactic origin [13]. In Einstein-aether theory [14] this excludes every subluminal mode to comparable precision [15]; see Ref. [16] for a review.

Medium vacua come in several flavours: superfluid vacua [9,17–20], crystal vacua in which curvature or matter are defects [21–24], and dualities that rewrite crystal phonons as gauge fields with defects as sources [25–27]. A recent proposal combines the two orders that a knot-and-wave picture needs. The vacuum is a supersolid, light is its transverse shear wave, and particles are its topological defects, with the claim that the superfluid component "lets matter drift through without drag" [28]. For an ordinary crystal there is a classic precedent: a moving dislocation has a limiting speed equal to the shear-wave speed, with Lorentz-like contraction of its strain field [29,30]. In an ordinary solid shear is the slowest sound, so the defect "light cone" and the shear "light cone" coincide naturally.

This paper makes one point. **A supersolid adds a sound slower than shear, and its defects couple to it.** The extra sound is second sound: the superfluid's phase mode hybridized with lattice compression. We quantify how strongly a density-coupled defect drives it. We first derive a closed form for the second-sound share of the density response, which vanishes only by a coincidence of elastic coefficients. We then compute it for the soft-core Gross–Pitaevskii supersolid in two and three dimensions, follow it to the melting transition, and work out the drag, radiation, binding and loss length that follow. The general principle is that of Refs. [1–8,11–15]. What we add is a concrete instance in the supersolid class, with numbers, and a direct test of the no-drag claim.

## 2. Why a supersolid

Two requirements single out the medium. If matter is to be made of vortex lines or vortex knots, the medium needs a condensate phase: vortices are the topological defects (first homotopy group $\mathbb Z$) of a U(1) order parameter. If light is to be a transverse wave, the medium needs shear rigidity, because a fluid, superfluid or not, has no propagating transverse sound. A medium with both orders at once is a supersolid [31,32].

The cleanest microscopic realization is a condensate of bosons with a soft-core repulsion, whose Fourier transform has a negative region (a roton). Above a critical coupling such a condensate crystallizes into a lattice of droplets that keeps global phase coherence [33–36]. In two dimensions the ground state is triangular. We use the Gross–Pitaevskii energy (units $\hbar=m=1$)
$$E[\psi]=\int \tfrac12|\nabla\psi|^2\,d^dr+\tfrac12\iint \rho(\mathbf r)\,U(\mathbf r-\mathbf r')\,\rho(\mathbf r')\,d^dr\,d^dr',\qquad U(r)=g\,\theta(R-r),$$
at mean density $\bar\rho=1$ and core radius $R=1$, so that $g$ is the only parameter. The uniform state becomes unstable to the roton at $g_c=14.74$ in 2D [35]. The superfluid–supersolid transition is first order and precedes the roton softening [35].

The supersolid has three gapless branches at long wavelength: one transverse, from shear, and two longitudinal, from the hybridization of the superfluid phase mode with lattice compression [35–38]. For the soft-core supersolid, Poli et al. found the transverse branch "always sandwiched in between the second sound mode and the first sound mode" [38]. The ordering is $c_2<c_T<c_1$, and second sound "has a weak density contribution" [38]. The question for a vacuum model is how weak, whether "weak" can be made zero, and what it implies for moving defects.

## 3. Longitudinal response of a supersolid

At zero temperature and long wavelength a supersolid is described by the superfluid phase $\theta$, the density deviation $\delta\rho$ and the lattice displacement $\mathbf u$ [39–41]. Along a longitudinal direction the quadratic Lagrangian density is
$$\mathcal L=-\delta\rho\,\dot\theta-\frac{\rho}{2}(\partial_x\theta)^2+\frac{\rho_n}{2}(\dot u-\partial_x\theta)^2-\frac{\alpha}{2}\delta\rho^2-\gamma\,\delta\rho\,\partial_xu-\frac{M}{2}(\partial_xu)^2-V\delta\rho .$$
Here $\rho=\rho_s+\rho_n$ splits into superfluid and normal (lattice-bound) parts, $\alpha=\partial^2e/\partial\rho^2$ is the inverse compressibility at fixed lattice, $M=C_{xxxx}$ is the uniaxial modulus at fixed density, $\gamma=\partial^2e/\partial\rho\,\partial\varepsilon_{xx}$ is the density–strain coupling, and $V$ is an external potential that couples to density. Solving the linear equations of motion gives the density response $\delta\rho=\chi V$:
$$\chi(q,\omega)=\frac{q^2\left(\rho\rho_n\,\omega^2-\rho_sM\,q^2\right)}{\rho_n\omega^4-\left(M+\rho\rho_n\alpha-2\rho_n\gamma\right)q^2\omega^2+\rho_s\left(\alpha M-\gamma^2\right)q^4}
=\rho q^2\sum_{\nu=\pm}\frac{F_\nu}{\omega^2-c_\nu^2q^2}.$$
The two sound speeds are the roots of $x^2-ax+b=0$ with $a=\rho\alpha-2\gamma+M/\rho_n$ and $b=(\rho_s/\rho_n)(\alpha M-\gamma^2)$, the form of Refs. [38,41]. The weights $F_\pm$ sum to one, which is the f-sum rule. The zero of the numerator sits at $c_*^2=\rho_sM/(\rho\rho_n)$, so
$$F_-=\frac{c_*^2-c_-^2}{c_+^2-c_-^2},\qquad F_+=1-F_-.$$
Evaluating the dispersion polynomial at $c_*^2$ gives $P(c_*^2)=-\rho_s(M-\rho\gamma)^2/\rho^2$, and therefore
$$\boxed{F_-=\frac{\rho_s\,(M-\rho\gamma)^2}{\rho^2\rho_n\,(c_+^2-c_*^2)(c_+^2-c_-^2)}}\tag{1}$$
The second-sound share vanishes in only two cases: without superflow ($\rho_s=0$, so no supersolid), or when the uniaxial modulus happens to equal $\rho$ times the density–strain coupling. Nothing in the symmetry of a supersolid relates these two independent second derivatives of the energy. Equation (1) also shows $F_-\propto\rho_s$, so second sound decouples from density only in the deep-crystal limit, where it also becomes slow.

Two further identities are useful. The compressibility sum rule reads $\sum_\nu F_\nu/c_\nu^2=1/c_\kappa^2$ with $c_\kappa^2=\rho(\alpha-\gamma^2/M)$. The share of the static response carried by branch $\nu$ is $S_\nu=(F_\nu/c_\nu^2)\,c_\kappa^2$. Because $c_-<c_+$, second sound carries a larger share of the static response than of the f-sum. The spectral weight per unit $q$, i.e. the dynamic structure factor's coefficient $Z_\nu$ in $S(q,\omega)=\sum_\nu Z_\nu\delta(\omega-c_\nu q)$, is $Z_\nu=\rho qF_\nu/2c_\nu$. Both branches carry density weight in general, and measuring the two weights and speeds determines the superfluid fraction [42]. All of these were checked symbolically and by an independent re-derivation of the response from the Lagrangian (supplementary S6).

## 4. Numbers for the soft-core supersolid

**Method.** For each coupling $g$ we relax the Gross–Pitaevskii state on a primitive triangular cell ($96^2$ real-space grid), optimize the lattice constant at fixed mean density, and polish the state with decreasing time steps until the translation Ward identity holds. Bogoliubov–de Gennes (BdG) excitations follow from the Hermitian form $L^{1/2}(L+2X)L^{1/2}$ in a basis of $32^2$ plane waves (checked at $40^2$). Here $L=-\tfrac12\nabla^2+U*\rho_0-\mu$ and $X f=\psi_0\,U*(\psi_0f)$. For each mode we compute the density matrix element $\rho_\nu(\mathbf q)=\int_{\rm cell}e^{-i\mathbf q\cdot\mathbf r}\psi_0 f_{+,\nu}$ with the BdG normalization $\int(|u|^2-|v|^2)=1$, and the weight $Z_\nu=|\rho_\nu|^2$. Two sum rules are imposed at every wavevector. The f-sum $\sum_\nu\omega_\nu Z_\nu=N_{\rm cell}q^2/2$, and the static sum $\sum_\nu 2Z_\nu/\omega_\nu$, which must equal a direct solution of $(L+2X)f=-2e^{i\mathbf q\cdot\mathbf r}\psi_0$. Both hold to $10^{-6}$ in every run. Modes are identified by polarization rather than by frequency order. The transverse mode is the gapless mode with zero density weight ($\le10^{-17}$ along both inequivalent mirror directions, parallel to a lattice vector and at 30° to it). The other two gapless modes are the longitudinal pair, so an inversion $c_2>c_T$ would be detected. Speeds are least-squares slopes over $|\mathbf q|a/2\pi\in[0.03,0.10]$ for $\mathbf q$ parallel to a lattice vector (the 30° direction agrees to 0.1 %). Weights are quoted at $|\mathbf q|a/2\pi=0.05$, where $Z_\nu/q$ is flat to 1 %.

**The canonical state** ($g=22$, lattice constant $a=1.4575$, $\mu=55.85$) has superfluid fraction $f_s=0.095$. The three branches are $c_2=1.80$, $c_T=5.77$ and $c_1=11.15$, so second sound runs at $0.31\,c_T$. It carries $Z_2/Z_1=0.33$ of first sound's spectral weight, 5.1 % of the f-sum and 67 % of the static density response. Table 1 compares the BdG numbers with an independent static route. There the superfluid fraction comes from the energy of a phase twist [43], $E(k)-E(0)=\tfrac12Nf_sk^2$, and the moduli from finite strains of the relaxed cell; no excitation is computed. Inserted into Sec. 3, these give the BdG weights to 1 %. Along the way the elastic tensor turns out to be of Cauchy class: $C_{xxyy}/C_{xyxy}=0.998$. The ratio $c_T/c_1=0.52$ therefore lies below the Cauchy value $1/\sqrt3$ not because of the lattice, but because $c_T^2=\mu/\rho_n$ [41] while first sound is stiffened by the superfluid compressibility. In Eq. (1), $M/\rho\gamma=11.4$: the two coefficients whose equality would decouple second sound differ by an order of magnitude.

*Table 1. Canonical 2D state ($g=22$): BdG versus static hydrodynamics (speeds in units $\hbar/mR$).*

| quantity | BdG | static route (Sec. 3) |
|---|---|---|
| $c_2$ (= $c_-$) | 1.802 | 1.817 |
| $c_T$ | 5.773 | 5.811 ($=\sqrt{\mu/\rho_n}$) |
| $c_1$ (= $c_+$) | 11.154 | 11.209 |
| $F_-$ (f-sum share) | 0.0513 | 0.0518 |
| $Z_2/Z_1$ | 0.334 | 0.337 |
| $S_-$ (static share) | 0.673 | 0.675 |
| $\chi(q\to0,0)$ per cell | 0.04276 | 0.04275 |
| inputs | — | $f_s=0.0952$, $\alpha=43.73$, $M=91.61$, $C_{xxyy}=30.51$, $\mu=30.56$, $\gamma=8.02$ |

**Generality.** Table 2 shows the interaction sweep from $g=44$ down to the melting transition, plus one state with a different kernel shape ($U=g\,e^{-(r/R)^6}$, $g=35$). Across the stable supersolid phase second sound runs at 0.07–0.78 of the shear speed. It carries 0.3–41 % of the f-sum and 63–81 % of the static response. Its weight never vanishes, and it falls smoothly with $f_s$, as Eq. (1) requires.

*Table 2. Soft-core supersolid in 2D. Speeds in units $\hbar/mR$; $F_2$ and $S_2$ are second sound's shares of the f-sum and of the static response; $Z_2/Z_1$ is its spectral weight relative to first sound.*

| $g$ | $a$ | $f_s$ | $c_2$ | $c_T$ | $c_1$ | $c_2/c_T$ | $F_2$ | $Z_2/Z_1$ | $S_2$ |
|---|---|---|---|---|---|---|---|---|---|
| 44 | 1.393 | — | 0.595 | 8.669 | 16.07 | 0.069 | 0.003 | 0.087 | 0.70 |
| 34 | 1.417 | — | 0.948 | 7.432 | 14.01 | 0.128 | 0.010 | 0.148 | 0.69 |
| 28 | 1.435 | — | 1.286 | 6.630 | 12.65 | 0.194 | 0.021 | 0.214 | 0.68 |
| 22 | 1.458 | 0.095 | 1.802 | 5.773 | 11.15 | 0.312 | 0.051 | 0.334 | 0.67 |
| 20 | 1.467 | 0.132 | 2.038 | 5.479 | 10.61 | 0.372 | 0.072 | 0.400 | 0.68 |
| 18 | 1.477 | 0.189 | 2.326 | 5.179 | 10.03 | 0.449 | 0.104 | 0.498 | 0.68 |
| 16 | 1.488 | 0.278 | 2.688 | 4.876 | 9.39 | 0.551 | 0.159 | 0.661 | 0.70 |
| 15 | 1.495 | 0.345 | 2.911 | 4.724 | 9.04 | 0.616 | 0.205 | 0.801 | 0.71 |
| 14 | 1.502 | 0.436 | 3.172 | 4.570 | 8.64 | 0.694 | 0.277 | 1.050 | 0.74 |
| 13.5 | 1.506 | 0.497 | 3.315 | 4.492 | 8.40 | 0.738 | 0.333 | 1.284 | 0.77 |
| 13.0* | 1.510 | 0.576 | 3.449 | 4.408 | 8.10 | 0.783 | 0.422 | 1.772 | 0.81 |
| 12.7† | 1.513 | 0.640 | 3.469 | 4.348 | 7.84 | 0.798 | 0.513 | 2.583 | 0.86 |
| 12.5† | 1.516 | 0.699 | 3.290 | 4.260 | 7.52 | 0.772 | — | — | — |
| 35 (γ6) | 1.438 | — | 2.174 | 6.617 | 13.50 | 0.329 | 0.043 | 0.279 | 0.63 |

\* just below the coexistence boundary $\Lambda_c=13.04$ (Sec. 5). † metastable continuation of the crystal branch; the branch ends near $g=12.47$.

**Three dimensions.** In 3D the same functional (step kernel, $\Lambda=\bar\rho U_0R^3$ at twice its roton threshold) selects a close-packed stack. The hexagonal (AB) stacking is lowest, nearly degenerate with fcc. We computed the BdG weights on the AB crystal ($a=1.386$, $c=2.260$) in a basis of 1,355 plane waves, with the state relaxed inside that basis so that the Goldstone modes are exact. The sum rules again hold to $10^{-6}$. Second sound is at $c_2=0.477$, against shear speeds of 7.3–8.2 (the lattice is elastically anisotropic) and first sound at 15.8–16.9. That gives $c_2/c_T\simeq0.06$. Second sound carries only 0.17–0.18 % of the f-sum but $Z_2/Z_1=0.058$–$0.063$ and 66–69 % of the static response. The compressibility speed is $c_\kappa=9.38=1.22\,c_T$.

## 5. Approach to melting

Does $c_2/c_T$ reach one anywhere inside the supersolid phase? At fixed density the free energy per area of a phase is $f(\rho)=\rho\,\varepsilon(g\rho)$, where $\varepsilon(\Lambda)$ is the energy per particle at unit density and coupling $\Lambda$. For the uniform state $\varepsilon_u=\pi\Lambda/2$ and $\mu_u=\pi\Lambda$. Equal chemical potential and pressure between the crystal and the uniform phase (the common tangent) give the crystal-side boundary $\Lambda_c$ as the root of
$$\Lambda\,(\mu_c-\varepsilon_c)=\frac{\mu_c^2}{2\pi},$$
with $\mu_c$ the Gross–Pitaevskii chemical potential of the crystal. Following the crystal branch continuously (Table 2) gives $\Lambda_c=13.04$. The uniform-side boundary is $\Lambda_u=\mu_c(\Lambda_c)/\pi=12.23$, and the fixed-density energy crossing at $g=12.57$ lies between them, close to the 12.7 reported in Ref. [35].

Approaching the boundary, $c_2/c_T$ rises monotonically to 0.78 at $\Lambda_c$. On the metastable branch it peaks at 0.80 near $g=12.7$ and then turns down before the branch ends near $g=12.47$. **The ratio never reaches one.** This agrees with the ordering reported in Ref. [38] and extends it to the phase boundary. Coupling to the slow branch strengthens on the way: its f-sum share grows to 0.41 at $\Lambda_c$ and $Z_2$ comes to exceed $Z_1$. Moving the medium toward melting does not help.

Hydrodynamics does not exclude $c_->c_T$ in principle. If the modulation could vanish continuously, with $\rho_n$, $M$ and $\mu$ all scaling as the modulation squared, the dispersion polynomial would factor as $(x-M/\rho_n)(x-\rho\alpha)$. The lower longitudinal speed would then tend to $\min(\sqrt{M/\rho_n},\sqrt{\rho\alpha})$, which can exceed $c_T=\sqrt{\mu/\rho_n}$. In the soft-core model the first-order transition intervenes first. Either way the two speeds are set by different material combinations, and equality is a coincidence.

## 6. Why defects couple to second sound

A vortex line in a one-component condensate has a node on its axis, so its core carries a density deficit of order $\rho\xi^2$ per unit length ($\xi$ the healing length). A second component can fill the core [44–46] and flatten the total-density dip. Exact cancellation of the total density everywhere, however, requires the symmetric point of the intra- and inter-component couplings together with a matched filling profile, a measure-zero condition. For immiscible components the interface between core and filling carries a density depression of its own. A generic localized knot therefore keeps a residual total-density deficit (or excess) $\epsilon\neq0$, and any $\epsilon\neq0$ suffices below. Independently, a vortex is a phase defect. When it moves it acts as a source for the superfluid phase field, and in the strongly modulated supersolid the lower longitudinal branch is predominantly that phase mode [38]. A density-neutral vortex therefore still couples to second sound through its circulation. We quantify only the density vertex here; the current vertex is a second, independent channel into the same branch.

## 7. Drag, radiation and loss length

**Landau criterion.** A defect moving at speed $v$ can emit into branch $\nu$ when $v>\min_q\omega_\nu(q)/q$. With several branches the critical speed is the smallest over the branches it couples to, here $c_2$. The lowest supersolid branch also sets the Landau instability of superflow [37]. In stripe supersolids the critical velocity even vanishes for motion that is not parallel to the stripes [48].

**Drag.** For a defect that couples to density through a potential with Fourier transform $V(\mathbf q)$, Fermi's golden rule with the response of Sec. 3 gives the drag force from each supercritical branch:
$$F_d^{(3D)}=\sum_{\nu:\,c_\nu<v}\frac{\rho F_\nu}{4\pi v^2}\int_0^\infty q^3|V(q)|^2\,dq ,\qquad
f_d^{(\rm line)}=\sum_{\nu:\,c_\nu<v}\frac{\rho F_\nu}{2\pi v^2\sqrt{1-c_\nu^2/v^2}}\int_0^\infty q^2|V(q)|^2\,dq ,\tag{2}$$
for a point-like defect and per unit length of a straight filament, respectively. The drag is **proportional to the branch's f-sum share and, for a point source, independent of the branch speed** above threshold. For a single Bogoliubov branch with $F=1$, a contact vertex $V=g_i$ and the dispersion cutoff $q_{\max}=2\sqrt{v^2-c^2}$, Eq. (2) reduces to $F_d=n g_i^2(v^2-c^2)^2/(\pi v^2)$, which is Eq. (12) of Astrakharchik and Pitaevskii [47] in our units. Supersonic motion in a Gross–Pitaevskii fluid is genuinely dissipative: no finite-energy supersonic travelling waves exist [49].

**Radiation.** A source of multipole order $\ell$ oscillating at frequency $\Omega$ with a fixed density vertex puts power $P_\nu\propto F_\nu\,\Omega^{2\ell+d+1}/c_\nu^{2\ell+d+2}$ into branch $\nu$ in $d$ dimensions. A slow branch is therefore favoured by a high power of $c_1/c_2$. With the 3D numbers ($c_1/c_2=33.6$, $F_2/F_1=0.0017$) a quadrupole radiates $\approx9\times10^{10}$ times more power into second sound than into first sound.

**Loss length.** As an order-of-magnitude estimate, take a defect of size $\xi$ with static deficit $\delta N=\epsilon\rho\xi^3$ and rest energy $E_0=\tau\rho c_T^2\xi^3$, with $\epsilon$ and $\tau$ dimensionless. The static relation $\delta n=\chi(q,0)V$ with $\chi(q\to0,0)=-\rho/c_\kappa^2$ gives $|V|\simeq c_\kappa^2\delta N/\rho$ up to $q\sim1/\xi$. Equation (2) then gives the energy-loss length of an ultrarelativistic defect with Lorentz factor $\gamma$ ($v\to c_T$):
$$\ell\simeq\frac{16\pi\tau}{\epsilon^2}\left(\frac{c_T}{c_\kappa}\right)^4\frac{\gamma\,\xi}{F_2}\approx1.3\times10^5\,\gamma\,\xi ,\tag{3}$$
using the 3D values, $\tau=10$ and $\epsilon=1$. Cosmic-ray protons of $3\times10^{11}$ GeV ($\gamma\approx3.2\times10^{11}$) that cross the Galaxy (10 kpc) require $\ell\gtrsim3\times10^{20}$ m, hence $\xi\gtrsim10^4$ m: a macroscopic grain. At the Planck length Eq. (3) falls short by about 40 orders of magnitude. A more detailed evaluation with explicit two-component vortex-ring profiles gives the same order (supplementary S5). Since Eq. (2) has no near-threshold suppression for linear branches, the only escape is kinematic: every particle must stay below $c_2$, which for the most energetic cosmic rays means
$$1-\frac{c_2}{c_T}\lesssim\frac{1}{2\gamma^2}\approx5\times10^{-24},\tag{4}$$
the same order as Coleman and Glashow's bound on vacuum Cerenkov radiation of charged particles [12]. In the computed model $1-c_2/c_T$ lies between 0.2 and 0.94.

## 8. Binding and drag share a vertex

Two static defects with vertices $V_1$ and $V_2$ interact through the medium with $U_{\rm ind}(\mathbf q)=V_1(\mathbf q)V_2(\mathbf q)\,\chi(\mathbf q,0)$. For like defects this is attractive. Its range is set by the vertices, because $\chi(q,0)$ is finite as $q\to0$ in a compressible medium. The result is a short-range attraction over a healing length or lattice spacing, the analogue of the phonon-induced Yukawa attraction between impurities in a condensate [50,51]. In the supersolid, 63–81 % of $\chi(q,0)$ is carried by second sound (Tables 1–2). The vertex that binds defects at short range is the vertex that makes them radiate when fast, and the same branch carries most of both. One cannot be removed without most of the other.

## 9. Escapes, and the elastic-ether debate

The difficulty is old. An elastic-solid ether carries a longitudinal wave as well as the transverse light wave. Green observed that the longitudinal wave could be avoided "by supposing its velocity to be indefinitely great or indefinitely small", and chose the former, an incompressible medium, because a medium with negative compressibility would be unstable [52,53]. Cauchy nonetheless adopted the latter: the contractile ether, of negative compressibility "such as to make the velocity of the longitudinal wave zero". Kelvin revived it as the labile ether [52,55]. MacCullagh took a third route. In his medium "the potential energy depends only on the rotation of the volume-elements", and "no longitudinal waves exist at any time" [52,54]. FitzGerald later mapped this medium onto Maxwell's equations [56,57]. Modern revivals of the incompressible choice exist [58].

Each route has a supersolid counterpart.

*Green's limit* ($\alpha\to\infty$) sends $c_+\to\infty$ and, by Eq. (1), $F_-\to0$ as $\alpha^{-2}$. Second sound decouples from density. It does not disappear, however: it survives at $c_*=\sqrt{\rho_sM/\rho\rho_n}$ as a density-free counterflow of superfluid against lattice, and a moving vortex still drives it through its circulation (Sec. 6). An incompressible medium also admits no core deficit, so Green's limit removes the density vertex but not the current vertex.

*The labile limit* ($c_-\to0$) is the worst case: every moving defect radiates.

*MacCullagh's medium* is the genuine exception, because it has no longitudinal restoring force at all. The longitudinal sector is excluded by initial conditions rather than by a large speed, and that is untenable once matter is a moving density source, which keeps generating compressional disturbances. A rotational medium also has no condensate phase. Adding superfluid order to host vortex matter brings back a compressional phase mode whose speed is set by compressibility, not by rotational stiffness. The Cosserat-supersolid proposal [28] belongs to this lineage. Our result is that its no-drag claim holds only if second sound is tuned to the shear speed, Eq. (4).

## 10. Discussion

In a supersolid model of the vacuum, matter's speed limit is set by the slowest longitudinal sound its cores couple to, and light's speed is the shear speed. No symmetry ties the two together. In the soft-core Gross–Pitaevskii supersolid second sound is slower than shear throughout the stable phase, in two and three dimensions, and the coupling to it is generic, Eq. (1). Fast matter therefore radiates into the vacuum, and a common causal cone requires the two speeds to agree to about $10^{-23}$. The general principle, that multiple sound speeds mean multiple metrics and tuning, is established [1–8]. This paper supplies the concrete mechanism and numbers for the supersolid class and refutes, within it, the claim that superfluidity lets matter move without drag.

The limitations are those of the model. We use mean-field Gross–Pitaevskii theory at zero temperature, one family of soft-core kernels plus one variant, and linear response. The size of the coupling is model-dependent, but the conclusion survives any reasonable change: the deficit in Eq. (3) is about 40 orders of magnitude. The regime $c_2>c_T$, where matter could outrun light, is not realized here. It is not excluded in media with a continuous transition, but it would fail the same test from the other side.

The contrast with relativistic field theory is instructive. In a Lorentz-invariant theory a moving soliton is the boost of a static one, so it never radiates, and matter and light share the cone automatically [62]. Skyrmions [59] and the knotted solitons of the Faddeev–Niemi model [60,61] realize "matter as knots" in that setting. A medium vacuum that wants knot matter has to reproduce this property, rather than approximate it by tuning.

## Acknowledgments

Numerical work and drafting were assisted by an AI system (Claude, Anthropic). The hydrodynamic formulas were re-derived independently by a separate reviewer.

## Data and code availability

All scripts and data are in the supplementary material (repository `gifgaf0/gifgaf0.github.io`, directory `lbc_bank/`; the index with paths and checksums is `lbc_bank/README.md`). S1 `lbc_weights.py` (2D BdG weights and sum rules); S2 `lbc_hydro.py` (static hydrodynamic route); S3 `lbc_3d.py` (3D weights); S4 `lbc_sweep_low.py`, `lbc_sweep_refine.py` (interaction sweep, coexistence boundary); S5 `step3_loss_length.py` (loss length with explicit two-component profiles); S6 `paper_identities_check.py` and the external re-derivation `verify_lbc_external.py`; `paper_tables.py` and all JSON outputs, with checksums.

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
