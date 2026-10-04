# LBC SECOND-LEG DISPATCH (single file, in-band) — the numbers the supersolid-vacuum paper cites

**Plain-language summary.** A short paper argues that a supersolid "vacuum" cannot give matter and light one speed limit, because the medium's second sound is slower than its shear wave and couples to the knots. Every number it cites was computed once, by one route, with internal cross-checks. This dispatch asks for an independent, blind recomputation of exactly those numbers from the model definitions below. The first leg's results travel sealed inside this file. They are opened only after your own results are committed, then compared by the embedded comparator. This is not a gate: no lock, no fold, and no ledger edit rides on it. It is the two-leg check the author asked for on the paper's numbers.

**Activation.** Do not start until the author's message contains this exact line:
`ACTIVATE: LBC-2LEG-1`
On any other message, hold and say so.

## 1. Independence rules (binding)

1. Build from scratch. Do not import, copy or read the first leg's scripts (the `lbc_*.py`, `step3_*.py`, `paper_*.py` files; the earlier instruments `g_tsh1_chatleg.py`, `tsh4_core.py`, `tsh4_routeD.py`). The sealed embed E6 contains them for diagnosis only, after comparison.
2. Use a different method wherever you reasonably can. Examples: a Newton or preconditioned-gradient ground-state solver instead of split-step imaginary time; a real-space or finite-difference BdG, or your own plane-wave construction with a different basis cut; a different quadrature for the γ6 kernel transform; an independent derivation of the drag prefactor.
3. Do not decode embeds E5 or E6 until your checkpoint (Sec. 4) is written, scanned (Sec. 5) and committed on your branch. Record the commit hash.
4. Report every number at full precision. Do not round to match anything.
5. Work from `main`. Do not open, list or read anything under `lbc_bank/` except the `lbc_bank/second_leg/` folder you create, and do not check out or read the branch `claude/lbc-bank-v489` or its pull request. They hold the first leg's numbers and the paper draft in plain text. If `lbc_bank/` is already on `main` when you start, treat everything in it outside `second_leg/` as sealed, exactly like E5 and E6.

## 2. Model definitions (exact)

Units ħ = m = 1. Mean density ρ̄ = 1. Core radius R = 1.

**2D.** E[ψ] = ∫ ½|∇ψ|² d²r + ½ ∬ ρ(r) U(r − r′) ρ(r′) d²r d²r′, with ρ = |ψ|².
- Step kernel U(r) = g θ(R − r), Fourier transform Û(k) = 2πgR² J₁(kR)/(kR), Û(0) = πgR².
- γ6 kernel U(r) = g exp(−(r/R)⁶), Û(k) = 2πg ∫₀^∞ e^(−r⁶) J₀(kr) r dr.
- Crystal: triangular lattice, one droplet per primitive cell, a₁ = (a, 0), a₂ = (a/2, √3a/2). The lattice constant a is optimized at fixed ρ̄ (minimize energy per area).
- Uniform reference: energy per area πg/2, chemical potential πg (step kernel).

**3D.** e = ⟨½|∇ψ|²⟩ + (Λ/2)⟨n (Û ∗ n)⟩ with n = |ψ|² and ⟨n⟩ = 1; step kernel Û(k) = 4πR³[sin(kR) − kR cos(kR)]/(kR)³.
- Λ_c = min over k with Û(k) < 0 of [−k²/(4Û(k))] (expect Λ_c ≈ 21.71); use Λ = 2Λ_c.
- Structure: AB (hcp-type) stack in the orthorhombic cell (a, √3a, c) with sites at fractional (0,0,0), (½,½,0), (½,⅙,½), (0,⅔,½).
- Lattice parameters: a = 1.3859646002819213, c = 2.2595969088482843 (from an earlier optimization). Report results there, and optionally at your own optimum.

**Excitations.** Linearize the time-dependent GP equation about the ground state ψ₀ (Bogoliubov–de Gennes), Bloch wavevector q.
- Density matrix element of mode ν: ρ_ν(q) = ∫_cell e^(−iq·r) ψ₀ (u_ν + v_ν), with normalization ∫_cell (|u_ν|² − |v_ν|²) = 1.
- Spectral weight: Z_ν = |ρ_ν|² per cell.
- f-sum share: F_ν = ω_ν Z_ν / (N_cell q²/2), N_cell = ρ̄ × cell area (volume).
- Static share: S_ν = (2Z_ν/ω_ν) / Σ_μ(2Z_μ/ω_μ).
- Both sum rules are checks: Σ_ν ω_ν Z_ν = N_cell q²/2, and Σ_ν 2Z_ν/ω_ν must equal the directly solved static response (equivalently Σ_ν F_ν/c_ν² = 1/c_κ²).
- Identify modes by polarization, not frequency order. In 2D the transverse mode has zero density weight along mirror directions; the two remaining gapless modes are longitudinal, labelled 2 (lower) and 1 (upper). Detect and report c₂ > c_T if it occurs.

**Directions and fits.** 2D: q parallel to a₁ (the first leg's instruments call this direction "GM"; geometrically it points toward K — the labels are inherited, the direction is what counts). Also report c_T at 30° to a₁, at |q|a/2π = 0.05. Speeds are least-squares slopes ω = c q through the origin over |q|a/2π ∈ {0.03, 0.05, 0.075, 0.10}. Weights are quoted at |q|a/2π = 0.05. 3D: q parallel to the x axis (along a) with |q| = 0.15 and 0.3 (units 1/R). Report the q = 0.15 values in the schema.

## 3. Tasks

**Q-A (2D weights).** For g ∈ {44, 28, 22, 16, 14, 13.5, 13.25, 13} (step kernel) and g = 35 (γ6 kernel), compute a, c₂, c_T, c₁, F₂, Z₂/Z₁, S₂. For the step points with g ≤ 22 also compute the superfluid fraction f_s from the phase-twist energy, E(k) − E(0) = ½ N f_s k² with the lattice held fixed and k small. At g = 22 also report the maximum sum-rule residuals over your q points and c_T at 30°.

**Q-A′ (static hydrodynamic route at g = 22, no excitations).** From finite strains of the relaxed cell, compute:
- f_s;
- α = ∂²e/∂ρ² (lattice fixed);
- M = C_xxxx (density fixed);
- C_xxyy;
- μ = C_xyxy (shear);
- γ = ∂²e/∂ρ∂ε_xx.

Then evaluate, with ρ_n = (1 − f_s)ρ and ρ_s = f_s ρ:
- a = ρα − 2γ + M/ρ_n and b = (ρ_s/ρ_n)(αM − γ²);
- c_±² = [a ± √(a² − 4b)]/2;
- c_T = √(μ/ρ_n);
- F₋ = (c_*² − c₋²)/(c₊² − c₋²), with c_*² = ρ_s M/(ρ ρ_n);
- the static share of the lower branch, (F₋/c₋²)/(F₋/c₋² + F₊/c₊²).

**Q-B (3D weights).** At the AB point, report:
- c₂ and the range of transverse speeds over your directions (c_T min and max);
- c₁, F₂, Z₂/Z₁ and S₂ at q = 0.15 along x;
- the compressibility speed c_κ = (vol/χ_static)^½ per unit density.

**Q-C (approach to melting, step kernel, 2D).** Follow the crystal branch downward in g (continuation seeding is fine) and report:
- the fixed-density coexistence boundary Λ_c, defined as the root of Λ(μ_c − ε_c) = μ_c²/(2π), where ε_c is the crystal energy per particle and μ_c its chemical potential;
- Λ_u = μ_c(Λ_c)/π;
- the fixed-density energy crossing (ε_c = πg/2);
- c₂/c_T and F₂ at Λ_c;
- the maximum of c₂/c_T along the metastable continuation, and the g at which the crystal branch ends;
- the boolean "c₂ ≥ c_T at any computed state".

**Q-D (loss length and formulas).**
1. Derive the drag on a point-like density-coupled defect of vertex V(q) moving at v through a medium with χ(q, ω) = ρq² Σ_ν F_ν/(ω² − c_ν² q²) (linear branches). Report the coefficient C in F_d = C ρ F_ν v⁻² ∫ q³|V|² dq. As a check, reduce to the single Bogoliubov branch with a contact vertex and compare with Astrakharchik & Pitaevskii, Phys. Rev. A 70, 013608 (2004), Eq. (12).
2. From the inputs below, recompute the loss-length re-evaluation.
   - Closure: ℓ = γ M τ̂ ξ / 𝒫 per channel, γ = 3.1974×10¹¹, ξ = 1.616255×10⁻³⁵ m (take as given), L_prop = 3.0857×10²⁰ m, M_old = φ² (φ the golden ratio).
   - Maps at four points (Â, Ĵ, Ô, T̂ = τ̂): (15.17, 4.68, 1.82, 8.06), (9.35, 0.61, 1.6401, 2.74), (13.73, 4.43, 1.20, 7.49), (18.26, 7.41, 0.45, 11.23).
   - Report the most- and least-favourable log₁₀(ℓ/L_prop) over points and channels.
   - Main re-evaluation: multiply ℓ by [S(φ²)/S(M_new)]/F₂ with S(M) = (1 − 1/M²)^(−½), M_new = c_T/c₂ from your Q-B (take c_T = 7.68 as the dynamical mean), and F₂ over your Q-B q points.
   - Report the orders recovered (min, max), the new most-favourable headline (min, max), the band over the four readings (fixed vertex filament / fixed vertex point source / closure literal with M → c_T/c₂ / fixed dressed static deficit with the factor divided by (c_κ/c_s)⁴, where c_s = c_T/φ²), and ξ_req = L_prop 𝒫/(γ M τ̂) divided by the main factor.
3. Evaluate the paper's estimate ℓ ≈ (16πτ/ε²)(c_T/c_κ)⁴ γξ/F₂ at τ = 10 and ε = 1 with your 3D c_κ and the smaller F₂; report the coefficient of γξ. Evaluate 1/(2γ²).

## 4. Checkpoint

Write `lbc_cc_checkpoint.json` in the schema of embed E4 (schema `lbc_2leg_schema_v1.0`, leg `cc`). Fill every null; arrays have the length shown. Units as in Sec. 2. Add any extra keys you like (they are reported as CC-only and not compared).

## 5. Procedure

1. Extract E1–E4 (the extractor at the end of this file prints and checks the md5 of every embed).
2. Build, compute, write the checkpoint.
3. Scan every file you wrote with E2 using the base list E1: `python3 t1_scan.py T1_base_author_20260919.txt <files>`. All files must be CLEAN, except that a file holding only the Q-D arithmetic may be exempted if its only hits are the stated inputs. Report hits by index only. (This file itself: the plaintext scans CLEAN under E1; the sealed base64 body of E6 contains chance substrings matching base indices 1, 9 and 10 (E5's body scans CLEAN) — armor-transport collisions of random characters, not references, the known class from earlier dispatches.)
4. Commit the checkpoint and your instrument on a new branch under `lbc_bank/second_leg/` and push. Record the commit hash: this is the pre-consultation checkpoint.
5. Only now extract E5 (and E6 if needed) and run `python3 lbc_2leg_compare.py lbc_chat_checkpoint.json lbc_cc_checkpoint.json compare_out.json`.
6. Report the comparator summary. For every MISS, state which leg you believe and why. A suspected first-leg error is diagnosed from E6 and reported as such; neither checkpoint is edited after comparison.
7. Commit `compare_out.json` and a short return note; open a pull request to `main`.

## 6. Tolerances (identical to the comparator's rules)

- Speeds: 1 % relative.
- 2D lattice constant: 0.5 %.
- Z₂/Z₁: 3 %.
- F₂: 3 % relative or 0.002 absolute (3D: 5 % or 0.0003).
- Static shares: 0.02 absolute (3D: 0.03).
- f_s and the moduli: 2 %.
- Sum-rule residuals: ≤ 10⁻⁴.
- Λ_c, Λ_u, energy crossing, branch end: 0.1 absolute.
- c₂/c_T at Λ_c and its maximum: 0.02 absolute; F₂ at Λ_c: 0.03.
- Boolean: equal.
- Loss-length orders: 0.1 absolute; ξ_req: 10 %; Eq. (3) coefficient: 5 %; 1/(2γ²): 1 %; drag coefficient C: 1 %.

## 7. Embeds

- E1 `T1_base_author_20260919.txt` (plaintext; md5 05302210cc4ceb70553acbe8379e9fc3).
- E2 `t1_scan.py` (plaintext; md5 6b86290090a8c84f1b1a0a99ec0bf697).
- E3 `lbc_2leg_compare.py` (plaintext).
- E4 `lbc_2leg_schema_v1.0_skeleton.json` (plaintext).
- E5 `lbc_chat_checkpoint.json` (SEALED, base64).
- E6 `lbc_chat_instruments.tar.gz` (SEALED, base64; the first leg's scripts and outputs, for diagnosis only).

The md5 of every embed is in the manifest below. The extractor writes each embed to the current directory and checks its md5. Run it for E1–E4 first; E5 and E6 only after step 4.
