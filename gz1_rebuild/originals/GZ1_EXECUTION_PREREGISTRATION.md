# G-ζ1 Execution Pre-registration (chat-side instance)
Date: 2026-06-09. Written BEFORE any computation in this session runs.

## Gate (verbatim binding, ledger v4.35 §2.88.D, Part VI row)
Object: MV-G1 crystallized p6m state (V4.26 §3.4-SYM; roton-GP), imports
limited to the I1–I3 ticket — no freshly tuned model.
Computation: Bogoliubov–Bloch band structure of small oscillations on the
crystal; identify the channel mediating the pairwise pulsation coupling;
compute its per-layer amplitude factor t (in-gap decay factor or
forward-coherent retention, whichever the band structure selects).
Outcomes: PASS t = 0.0931 ± 0.005 (no input tuned to target);
INFORMATIVE-FAIL t computed ≠ 0.0931; DEGENERATE channel gapless/transparent
(t → 1).
Eddington guard: target value enters only at the comparison step.

## Model instantiation (the registered object, not a new model)
ℏ = m = 1, 2-D. E[ψ] = ∫½|∇ψ|² + ½∫∫ρ(x)U(x−x′)ρ(x′) − μ∫ρ.
Soft-core kernel U(r) = g·θ(R−r) with the MV-G1 canonical run values
g = 22.0, R = 1.0, ρ₀ = 1.0 (tools/mv_g1_minimiser.py defaults; the V4.26
R1 row). Continuum Fourier kernel Ũ(q) = 2πgR² J₁(qR)/(qR), Ũ(0) = gπR².
These three numbers are the I1–I3 instantiation already on the ledger;
nothing in this session is allowed to retune them.

## Analysis protocol (fixed now)
1. OBJECT REPRODUCTION: re-crystallize the big-box ground state at the
   canonical parameters (N=160, L=20, quench, seed 7) and confirm p6m
   (local ψ₆ dominant). Measure k_c. This is the R1 baseline check only.
2. PRIMITIVE CELL: relax the same action in the oblique triangular
   primitive cell; select the lattice constant a* by minimizing the
   energy density over a (the crystal picks its own a — no external
   input). Cross-check a* against the big-box k_c.
3. BANDS: plane-wave Bogoliubov–de Gennes on the crystallized cell.
   ω²f₊ = L(L+2X)f₊, L = −½∇² + (U*ρ₀) − μ (PSD; ψ₀ its ground state),
   X f = ψ₀·U*(ψ₀ f). Hermitian form via L^{1/2}(L+2X)L^{1/2}.
   Path Γ–M–K–Γ plus a dense normal-incidence line Γ→M_y (k_x = 0).
   Sanity gates that must pass before any t is quoted:
   (a) min eig L(Γ) ≈ 0 with eigenvector ≈ ψ₀;
   (b) Goldstone branches gapless at Γ (acoustic ω → 0);
   (c) band energies stable under plane-wave cutoff increase.
4. CHANNEL RULE (registered now, before bands are seen): a pulsating knot
   is an isotropic density (breathing) source; the mediating channel is the
   DENSITY response. "Per layer" = per close-packed row; the layer normal is
   ŷ = the Γ→M(b₂/2) direction; row spacing d = √3·a*/2.
   - For any frequency inside a band at normal incidence: the Bloch
     forward-coherent retention is 1 (lossless periodic medium) — that is
     the t the band structure selects there.
   - For any frequency inside a complete normal-incidence stop band:
     t(ω) = e^{−κ(ω)d}, κ from the steady-state driven evanescent decay,
     quoted at midgap (and the min over the gap reported).
   - NO frequency may be selected by proximity to any target value. The
     full t(ω) landscape is reported; selection arguments, if any, must be
     ledger-internal (CM-3 is R3 and is NOT used to pick a number here).
5. DECAY MEASUREMENT: frequency-domain driven strip (1 transverse period ×
   ~36 rows, periodic), GMRES on the linearized BdG response
   (L+X−ω−iη)u + Xv = −S, Xu + (L+X+ω+iη)v = 0, source = ψ₀-masked row;
   fit ln(row density-response amplitude) vs row index → κ. Controls: one
   in-band frequency (must show NO exponential decay) and one low-ω
   acoustic frequency (must show propagation).
6. COMPARISON (last, separate): only here is ζ = 1 − π/√12 loaded.
   PASS window [0.0881, 0.0981] per the registered tolerance.

## Outcome mapping (fixed now)
- If the density channel at the frequencies that can mediate a static/
  quasi-static pairwise coupling (ω → 0 acoustic sector) is gapless and
  transparent: that is the DEGENERATE arm for the per-layer-attenuation
  ontology, regardless of what gaps exist higher up.
- Any finite gaps found: their t values are reported and compared; a t in
  the PASS window would be reported as conditional on a frequency-selection
  mechanism that is itself not part of this gate (flagged, not claimed).
- t computed and outside the window at every non-tuned candidate frequency:
  INFORMATIVE-FAIL arm.
This mapping is written before the first eigenvalue is computed.
