# E9 chiral loop: does a chiral stiffness hold the twisted ring open? Report

November 1, 2026. Label: Exploration. This report covers exactly the runs of `PREREG_chiral_loop.md` §4: starts A and B at the six γ values, the P1 control at γ = ±0.3, C0 at γ = ±0.3, and box checks (none were triggered). The energy is `gl3.py`'s plus the chiral term γψ*·(D×ψ), with strand k locked to grid axis k (A5) and one-constant stiffness (A6). Fixed parameters: κ = 2 (e = 1/√12), η = 0.1, h = 0.5, R₀ = 6, a 65³ grid (box half-width 16), open boundaries, the starts of `starts.py`, maxiter 4000, a record every 2 iterations. `gl3.py`, `starts.py`, `linking.py`, `trace_N1.py`, `control_N0.py`, every PREREG, `NOTE_chiral_term.md` and `STATUS_step3.md` are unchanged.

**Units.** All outputs are in model units, as in `REPORT_N1_cells.md`. Lengths are in `gl3.py` coordinate units (ξ = 1/√2), and the core-scale threshold 2ξ is 1.41. "E" is the energy minus `gl3.vacuum_energy()`, the uniform γ = 0 vacuum. At γ ≠ 0 with open boundaries that is no longer the box's lowest state (§3.5), so E goes negative late in every run. No physical identification is made or implied, and the sign of γ that is "favoured" is not to be read as any physical parity violation.

## Summary

| | Result |
|---|---|
| Instrument checks P0 (§3 items 1–4) | **Pass.** Gradient 2.3 × 10⁻⁷ (gl3 style, round-off limited) and 5.4 × 10⁻⁷ (5-point, excluding components whose gradient is exactly 0). Im/Re ≤ 6.3 × 10⁻¹⁶. Gauge change ≤ 3.0 × 10⁻¹⁵. Parity ratio −1 to 4 × 10⁻¹⁶. γ = 0 is bitwise identical to `gl3`, and it reproduces `trace_N1_B_N65_R6.json` exactly (E difference 0.0, same segment counts, same Lk) at every record to iteration 40. |
| C0 (§3 item 5), γ = ±0.3 | **Passes as written:** E_end = −141.46 ≤ 10⁻⁵ and no vortex segments. **Flag:** the noise does not relax to the uniform vacuum. It relaxes to a vortex-free state with a chiral surface twist at the open faces, 141.46 *below* the uniform vacuum (§3.5). Both signs were kept. |
| Sign convention vs `chiral1d.py` | **Same sign, same value.** A director helix agrees exactly (relative difference 0). A complex texture with A agrees to 1.2 × 10⁻⁴, the O((ehA)²) difference between the link and site forms of the A·S term (§2.4). |
| Starts | \|Lk12\| = \|Lk13\| = 1 for A and B at 65³ (Lk = −1 for both). |
| P1 (N = 0 ring at γ = ±0.3) | **Holds** at both signs: the ring collapses and all lines are gone by iteration 44. |
| Main runs, 12 | **All COLLAPSE.** No finite R*, and every run ends line-free. |
| Mechanisms | A, \|γ\| = 0.1: **point reconnection** (as at γ = 0). A, \|γ\| = 0.2 and 0.3: **point reconnection, then separation.** B, \|γ\| = 0.1: **merge onto the core** (as at γ = 0). B, \|γ\| = 0.2 and 0.3: **something else**: an early point crossing unlinks strand 1 (Lk = 0.000 exactly from iteration 10–16). Its loop then rides beside the composite as an unlinked coaxial loop, 1–3 grid spacings away, and the two shrink to zero together. |
| Parity classification | **COLLAPSE** at every (start, \|γ\|): 6 of 6. No CHIRAL-STABLE and no parity-even STABLE. |
| Delay | Not selected by sign. At each \|γ\| the +γ and −γ runs lose strand 1 at the same iteration. Compared with γ = 0, strand 1 survives longer by 0, 2 and 6 iterations (A) and 0, 2 and 2 (B) at \|γ\| = 0.1, 0.2, 0.3. E decreases at every record in every run, with no plateau. |
| P3 (±γ E differ by > 1 % at matched iterations) | **Holds literally at every \|γ\| for both starts**, but partly for a trivial reason. Restricted to records where strand 1's line exists in both runs, the maximum relative difference is 0.10 %, 0.68 % and 8.9 % (A) and 2.1 %, 7.1 % and 3.5 % (B). So in that window A at \|γ\| = 0.1 and 0.2 stays below 1 % (§6.3). |
| Virial residual | Never a test here (all COLLAPSE). The literal residual falls from 1.0 to below 0.10 only in the last few records with lines (A and B at \|γ\| = 0.3; one record of B at −0.2), while the loop is vanishing, and it is −0.26 in every final state. That is because it includes the boundary twist. With the final state's split subtracted, the residual stays ≥ 0.10 in every run while any line exists. |
| 81³ box checks | **None run.** None is triggered, because no run fails to collapse. |

## 1. Commands run

```
cd seed/experiments/E9_three_strand_closure
pip install scipy                                    # not present in the container (deviation 1)
python3 gl3_chiral.py                                # quick gradient check
python3 chiral_loop_checks.py > chiral_loop_checks_output.txt   # §3 items 1-3, gamma = 0 identity, starts, 1D sign check
# §3 item 4 (regression), in scratch copies so no official output is overwritten:
python3 trace_N1_chiral.py B 65 6 40 2 0             # default threads -> regression_trace_N1_chiral_B_N65_R6_g0_it40.json, log_regression_g0.txt
OMP_NUM_THREADS=1 python3 trace_N1_chiral.py B 65 6 40 2 0   # -> ..._it40_omp1.json, log_regression_g0_omp1.txt (deviation 4)
# §3 item 5 (C0), one BLAS thread each:
python3 c0_chiral.py 0.3  > log_c0_g+0.3.txt
python3 c0_chiral.py -0.3 > log_c0_g-0.3.txt
./run_chiral_loop.sh 1     # P1 controls at +-0.3, and A at +-0.1 (4 concurrent jobs)
./run_chiral_loop.sh 2     # after P1 was checked: the other 10 main runs (4 concurrent streams)
python3 tables_chiral_loop.py > log_tables_chiral_loop.txt   # read-only tables for this report
```

`run_chiral_loop.sh` runs `control_N0_chiral.py 65 6 ±0.3 4000 2` and `trace_N1_chiral.py <A|B> 65 6 4000 2 <γ>` for the six γ, with `OMP_NUM_THREADS = OPENBLAS_NUM_THREADS = MKL_NUM_THREADS = 1`. Stage 2 was started only after P1 had been read at ±0.3 (§4).

## 2. Instrument

### 2.1 `gl3_chiral.py`

`GL3Chiral` subclasses `GL3`. Its `energy_grad` is:
- γ = 0: `return GL3.energy_grad(self, v)`. This is the same call, so it gives the same result bit for bit (checked, §3.4).
- γ ≠ 0: the GL3 energy and gradient, plus the chiral term's.

The chiral term is the PREREG §2 form on gl3's links:

  E_χ = γ h³ Σ_x ψ*·(εDψ) = γ h² Re Σ_j Σ_{x, x+ĵ in box} U_j(x) W_j(x),  W_j(x) = ψ*(x)·(ê_j × ψ(x+ĵ)),  U_j = exp(−iehA_j).

In the symmetric difference the backward half of each link is the complex conjugate of its forward half. Dropping the box-crossing terms drops both halves of a link together. The gradient is analytic, in gl3's convention (the ψ block is 2∂E/∂ψ*):
- site x: γh² U_j (ê_j × ψ(x+ĵ));
- site x+ĵ: −γh² U_j* (ê_j × ψ(x));
- link A_j(x): γh² e h Im(U_j W_j).

The pin mask, which is unused here, is honoured. The file also provides the diagnostics:
- `chiral_complex`: both halves summed separately, for the reality check;
- `chiral_density`: site-local, summing to E_χ exactly;
- `split`: E_grad, E_mag, E_V, E_χ, E_χ(A·S), and the per-site covariant |Dψ|².

**The A·S part** is defined on the lattice as E_χ − E_χ[ψ, A = 0]. In the continuum this is −γe∫A·S, with S = iψ×ψ*. It is gauge dependent. The minimizer does no gauge fixing and starts from A = 0, so this part is reported in whatever gauge the L-BFGS path reaches (deviation 6).

### 2.2 `trace_N1_chiral.py`: diff against `trace_N1.py` (also in `diff_trace_N1_chiral.txt`)

```diff
--- trace_N1.py	2026-11-01 03:49:31.612523654 +0000
+++ trace_N1_chiral.py	2026-11-01 03:52:54.359600272 +0000
@@ -1,19 +1,24 @@
 """Diagnostic re-run of run_N1.py with fine-grained history. Same model, same start, same minimizer call
 (L-BFGS-B is deterministic, so the trajectory is the one run_N1.py follows); only the callback differs.
-usage: python3 trace_N1.py START N R0 MAXITER EVERY
+usage: python3 trace_N1_chiral.py START N R0 MAXITER EVERY GAMMA [SAVEDIR]
+(trace_N1_chiral.py: copy of trace_N1.py using gl3_chiral.GL3Chiral with gamma as an argument, plus the
+PREREG_chiral_loop.md §4 diagnostics: energy split, <|S|/|psi|^2> weighted by |D psi|^2, chiral energy within
+distance 3 of strand 1's line, virial residual.)
 Records every EVERY iterations: energy above vacuum, composite ring radius, strand 1 loop geometry,
 linking number of strand 1's vortex lines with strand 2's and strand 3's (linking.py), and the closest
 approach of any vortex line to the box faces. Prints no verdict.
 """
 import numpy as np, json, sys, time
-from gl3 import GL3
+from gl3_chiral import GL3Chiral, S_field
+from scipy.spatial import cKDTree
 from linking import vortex_segments, linking
 start, N, R0, maxiter, every = sys.argv[1], int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
-g = GL3(N=N, h=0.5, eta=0.1)
+gamma = float(sys.argv[6])
+g = GL3Chiral(N=N, h=0.5, eta=0.1, gamma=gamma)
 from starts import start_fields   # Amendment B: corrected starts
 psi = start_fields(g, start, R0); A = np.zeros((3, N, N, N))
 half = (N // 2) * g.h; ax0 = -half
-tag = f'trace_N1_{start}_N{N}_R{R0:g}'
+tag = f'trace_N1_chiral_{start}_N{N}_R{R0:g}_g{gamma:+g}'
 hist = []; t0 = time.time(); it = [0]
 
 def diag(v):
@@ -45,10 +50,24 @@
         d['gap12_min'] = float(dd.min()); d['gap12_mean'] = float(dd.mean())
     d['Lk12'] = float(linking(*s[0], *s[1])) if len(mid[0]) and len(mid[1]) else 0.0
     d['Lk13'] = float(linking(*s[0], *s[2])) if len(mid[0]) and len(mid[2]) else 0.0
-    d['R23_gl3'] = g.core_radius(p[1]); d['t'] = time.time() - t0
+    d['R23_gl3'] = g.core_radius(p[1])
+    # PREREG_chiral_loop.md §4 diagnostics
+    sp, w = g.split(p, a); d.update(sp)
+    rho = np.sum(np.abs(p) ** 2, axis=0); Sn = np.linalg.norm(S_field(p), axis=0)
+    ok = rho > 1e-12
+    d['S_rho_wgrad'] = float(np.sum(w[ok] * Sn[ok] / rho[ok]) / np.sum(w[ok])) if np.sum(w[ok]) > 0 else None
+    if len(mid[0]):
+        dist, _ = cKDTree(mid[0]).query(np.stack([g.x.ravel(), g.y.ravel(), g.z.ravel()], -1))
+        d['E_chi_near1'] = float(np.sum(g.chiral_density(p, a).ravel()[dist <= 3.0]))
+    else:
+        d['E_chi_near1'] = None
+    num = sp['E_grad'] - sp['E_mag'] + 2 * sp['E_chi'] + 3 * sp['E_V']
+    den = sp['E_grad'] + sp['E_mag'] + 2 * abs(sp['E_chi']) + 3 * sp['E_V']
+    d['virial'] = float(num / den) if den != 0 else None
+    d['t'] = time.time() - t0
     return d
 
-save = sys.argv[6] if len(sys.argv) > 6 else None
+save = sys.argv[7] if len(sys.argv) > 7 else None
 def cb(v):
     it[0] += 1
     if save and it[0] % every == 0 and it[0] <= 60:
@@ -59,5 +78,5 @@
 d0 = diag(g.pack(psi, A)); hist.append(d0); print(json.dumps(d0), flush=True)
 psi, A, r = g.minimize(psi, A, maxiter=maxiter, gtol=1e-5, callback=cb)
 final = diag(g.pack(psi, A)); final.update(converged=bool(r.success), msg=str(r.message), iters=int(r.nit))
-json.dump(dict(start=start, N=N, R0=R0, every=every, history=hist, final=final), open(f'{tag}.json', 'w'), indent=1)
+json.dump(dict(start=start, N=N, R0=R0, gamma=gamma, every=every, history=hist, final=final), open(f'{tag}.json', 'w'), indent=1)
 print('FINAL', json.dumps(final))
```

The changes:
- γ is `argv[6]`, so the optional save directory moves from `argv[6]` to `argv[7]`. It was not used.
- GL3 is replaced by GL3Chiral.
- The tag includes γ, and γ is added to the output JSON.
- The §4 diagnostics are added to each record. N was already an argument (`argv[2]`), so the 81³ check needs no further change.

The diagnostics:
- `E_grad`, `E_mag`, `E_V` (potential + Josephson above `vacuum_energy()`), `E_chi`, `E_chi_AS`;
- `S_rho_wgrad`: ⟨|S|/|ψ|²⟩ weighted by the covariant Σ_k Σ_j |D_jψ_k|² at each site, with |ψ|² = Σ_k|ψ_k|² and sites with |ψ|² ≤ 10⁻¹² excluded;
- `E_chi_near1`: Σ of `chiral_density` over sites within distance 3 of the midpoints of strand 1's dual segments;
- `virial`: (E_grad − E_mag + 2E_χ + 3E_V)/(E_grad + E_mag + 2|E_χ| + 3E_V).

### 2.3 `control_N0_chiral.py`: diff against `control_N0.py` (also in `diff_control_N0_chiral.txt`)

```diff
--- control_N0.py	2026-11-01 03:49:30.898682451 +0000
+++ control_N0_chiral.py	2026-11-01 03:53:11.033590172 +0000
@@ -1,24 +1,32 @@
-"""N = 0 control (P1): a composite ring with no twist should shrink. Free relaxation from R0."""
+"""N = 0 control (P1): a composite ring with no twist should shrink. Free relaxation from R0.
+control_N0_chiral.py: copy of control_N0.py using gl3_chiral.GL3Chiral with gamma as an argument; maxiter and the
+record interval are optional arguments (defaults 600 and 25, as in control_N0.py); each record adds the energy split and the vortex segment counts.
+usage: python3 control_N0_chiral.py N R0 GAMMA [MAXITER EVERY]"""
 import numpy as np, json, sys, time
-from gl3 import GL3
+from gl3_chiral import GL3Chiral
+from linking import vortex_segments
 N = int(sys.argv[1]) if len(sys.argv) > 1 else 49
 R0 = float(sys.argv[2]) if len(sys.argv) > 2 else 6.0
-g = GL3(N=N, h=0.5, eta=0.1)
+gamma = float(sys.argv[3])
+maxiter = int(sys.argv[4]) if len(sys.argv) > 4 else 600
+every = int(sys.argv[5]) if len(sys.argv) > 5 else 25
+g = GL3Chiral(N=N, h=0.5, eta=0.1, gamma=gamma)
 f = g.ring_field((0, 0, 0), (0, 0, 1), R0)
 psi = np.stack([f, f, f]); A = np.zeros((3, N, N, N))
 E0 = g.energy_grad(g.pack(psi, A))[0] - g.vacuum_energy()
 hist = []; t0 = time.time()
 def cb(v):
-    if len(hist) % 25 == 0:
-        p, _ = g.unpack(v); E = g.energy_grad(v)[0] - g.vacuum_energy()
-        hist.append(dict(it=len(hist), E=float(E), R2=g.core_radius(p[1]), R1=g.core_radius(p[0]), t=time.time() - t0))
+    if len(hist) % every == 0:
+        p, a_ = g.unpack(v); E = g.energy_grad(v)[0] - g.vacuum_energy()
+        hist.append(dict(it=len(hist), E=float(E), R2=g.core_radius(p[1]), R1=g.core_radius(p[0]), **g.split(p, a_)[0],
+                         nseg=[len(vortex_segments(p[k], g.h, -(N // 2) * g.h)[0]) for k in range(3)], t=time.time() - t0))
         print(json.dumps(hist[-1]), flush=True)
     else:
         hist.append(None)
-psi, A, r = g.minimize(psi, A, maxiter=600, callback=cb)
+psi, A, r = g.minimize(psi, A, maxiter=maxiter, callback=cb)
 E = g.energy_grad(g.pack(psi, A))[0] - g.vacuum_energy()
-out = dict(N=N, h=0.5, R0=R0, E_start=float(E0), E_end=float(E), R_end=g.core_radius(psi[1]),
+out = dict(N=N, h=0.5, R0=R0, gamma=gamma, maxiter=maxiter, every=every, split_end=g.split(psi, A)[0], nseg_end=[len(vortex_segments(psi[k], g.h, -(N // 2) * g.h)[0]) for k in range(3)], E_start=float(E0), E_end=float(E), R_end=g.core_radius(psi[1]),
            iters=int(r.nit), converged=bool(r.success), msg=str(r.message), seconds=time.time() - t0,
            history=[x for x in hist if x])
-json.dump(out, open(f'control_N0_N{N}_R{R0:g}.json', 'w'), indent=1)
+json.dump(out, open(f'control_N0_chiral_N{N}_R{R0:g}_g{gamma:+g}.json', 'w'), indent=1)
 print('FINAL', json.dumps({k: out[k] for k in ('E_start', 'E_end', 'R_end', 'iters', 'converged', 'seconds')}))
```

The changes:
- γ is an argument.
- maxiter and the record interval are optional arguments. They default to `control_N0.py`'s 600 and 25, and were run at 4000 and 2 (deviation 3).
- Each record adds the energy split and the vortex segment counts, and the end state adds both too. Without the counts P1 could not be read: `core_radius` alone does not show whether lines remain.
- The output name carries γ.

As in `control_N0.py`, the record's "it" is the callback count minus 1.

### 2.4 Sign convention against `chiral1d.py`

`chiral1d.Chain` (n̂ = z, P = 10, M = 20, so h = 0.5) was compared with `GL3Chiral.chiral_density` on a 41³ slab. The slab carries the same 1D state along z, repeated over two periods and uniform in x and y. Its density was averaged over interior sites (not on any face) and over exactly one period in z. Both are per unit volume.

| state | γ | `chiral1d` chiral/length | `gl3_chiral` density | rel. diff |
|---|---|---|---|---|
| director helix f(cos qz, sin qz, 0), A = 0 | +0.3 | −2.03951216 × 10⁻¹ | −2.03951216 × 10⁻¹ | 0 |
| (same) | −0.3 | +2.03951216 × 10⁻¹ | +2.03951216 × 10⁻¹ | 0 |
| complex relative-phase texture, A_∥ = 0.4 sin qz, A_⊥ = (0.3 cos qz, −0.2 + 0.1 sin qz) | +0.3 | +4.97581999 × 10⁻² (link +1.78 × 10⁻², A_⊥·S +3.19 × 10⁻²) | +4.97522480 × 10⁻² | 1.2 × 10⁻⁴ |
| (same) | −0.3 | −4.97581999 × 10⁻² | −4.97522480 × 10⁻² | 1.2 × 10⁻⁴ |

The helix value is the lattice −γf² sin(qh)/h = −0.20395, against the continuum −γf²q = −0.20735. That is the NOTE's convention: a right-handed helix gives a negative ψ*·(∇×ψ). For the A-carrying texture, `chiral1d` puts A_⊥ on sites and uses the linear −eA_⊥·S, while `gl3_chiral` puts it on x- and y-links as exp(−iehA). The difference, O((ehA)²) ≈ 10⁻⁴, is the expected discretization difference. **The two codes use the same sign of γ.**

## 3. Checks (PREREG §3), all before any verdict run

Software: Python 3.13.18, NumPy 2.5.3, SciPy 1.18.1 (pip). Linux container, 4 cores. Full output: `chiral_loop_checks_output.txt`.

### 3.1 Gradient (item 1)

| check | worst relative error |
|---|---|
| `gl3.check_grad()` (reference, no chiral term) | 2.09 × 10⁻⁷ |
| gl3-style check (N = 6, seed 0, 40 components, central step 10⁻⁶), full functional, γ = +0.3 | **2.29 × 10⁻⁷** |
| same, γ = −0.3 | 2.84 × 10⁻⁷ |
| 5-point stencil (step 10⁻³), full functional, 400 components, γ = +0.3 / −0.3 | **5.4 × 10⁻⁷** / 8.1 × 10⁻⁹ over the 381 components with g ≠ 0 |
| 5-point, chiral term alone, N = 7, 400 components | 1.4 × 10⁻⁹ |

The gl3-style check is round-off-limited, and its value matches gl3's own. In the 5-point check, 19 of the 400 components have an analytic gradient of exactly 0: they are links in the unused last slice of each A_j, which nothing depends on. There the finite difference is round-off, |fd| ≤ 3.8 × 10⁻¹¹. gl3's relative measure |fd − g|/(|fd| + 10⁻⁸) reads 4 × 10⁻³ on those components because of the 10⁻⁸ floor, so I excluded them and report them separately (deviation 7). **Both forms are ≲ 10⁻⁶.**

### 3.2 Real and gauge-invariant (item 2)

Five random states (N = 9, ψ and A standard normal):
- |Im|/|Re| of the complex symmetric-difference sum: ≤ 6.3 × 10⁻¹⁶.
- Its real part equals the code's E_χ to ≤ 4 × 10⁻¹⁵, and Σ density equals E_χ to ≤ 3.2 × 10⁻¹⁵.
- Smooth gauge transformation, α = 1.3 sin(0.4x + 0.2)cos(0.3y) + 0.7 sin(0.5z − 0.1x) + 0.5, applied as ψ → e^{iα}ψ and A_j → A_j + Δ_jα/(eh): E_χ changes by ≤ 3.0 × 10⁻¹⁵ relative, and the total energy at γ = 0.3 by ≤ 1.4 × 10⁻¹⁶. **Pass.**

### 3.3 Parity (item 3)

Inversion x → −x is exact on the odd, origin-centred grid. ψ → −ψ(−x), and A_j on link (y, y+ĵ) → −A_j on link (−y−ĵ, −y). This is the same map as `chiral_term_checks.py`. Over three random states:
- E_χ(Pψ)/E_χ(ψ) = −0.9999999999999996, −1.0 and −0.9999999999999997.
- E_{+γ}(Pψ) = E_{−γ}(ψ) to ≤ 1.3 × 10⁻¹⁶.

**Pass.**

### 3.4 Regression at γ = 0 (item 4)

- `GL3Chiral(γ = 0).energy_grad` equals `GL3.energy_grad` bit for bit (E and the whole gradient array, `np.array_equal`), on a random N = 9 state and on start B at 65³.
- `trace_N1_chiral.py B 65 6 40 2 0` (default threads, as the original run used) reproduces `trace_N1_B_N65_R6.json` at all 21 records, iterations 0–40. The E difference is 0.0 at every record, `nseg` is equal, and `Lk12` and `Lk13` are equal (`regression_trace_N1_chiral_B_N65_R6_g0_it40.json`). **Pass, exact.**
- The same regression with one BLAS thread matches to ≤ 3.6 × 10⁻¹³ relative in E, with identical segment counts and Lk (`..._omp1.json`). The production runs used one thread (deviation 4).

### 3.5 C0: vacuum + noise at γ = ±0.3 (item 5)

`c0_chiral.py`: the uniform vacuum √(1+η)(1,1,1), A = 0, plus N(0, 0.05) on every free variable (Re ψ, Im ψ, A), `default_rng(0)`. It uses the same minimizer call as the trace runs.

| γ | E_start | E_end | vortex segments | iterations | E_grad | E_mag | E_V | E_χ | E_χ(A·S) |
|---|---|---|---|---|---|---|---|---|---|
| +0.3 | 14847.5 | **−141.4629** | 0, 0, 0 | 90 (converged) | 46.15 | 2 × 10⁻⁶ | 96.82 | −284.42 | −0.003 |
| −0.3 | 14847.7 | **−141.4629** | 0, 0, 0 | 83 (converged) | 46.14 | 2 × 10⁻⁶ | 96.81 | −284.42 | −0.003 |

**Literal verdict: PASS** at both signs. "Final E above vacuum ≤ 10⁻⁵" holds, because −141.46 ≤ 10⁻⁵, and there are no vortex segments. Both γ were kept.

**Flag for the author: C0 does not relax "back to the vacuum".** With open boundaries the uniform vacuum is not a stationary point at γ ≠ 0. In the bulk the two link terms of the chiral gradient cancel, but at a face the outward link is missing. So each face carries a source γh²(ê_j × ψ), and the field relaxes to a vortex-free surface twist below the uniform vacuum. Its chiral energy by distance from the nearest face (γ = +0.3; −0.3 agrees to 10⁻³):

| layer (sites from face) | 0 | 1 | 2 | 3 | 4 | 5 | ≥ 6 |
|---|---|---|---|---|---|---|---|
| E_χ | −87.4 | −109.4 | −48.9 | −21.7 | −9.6 | −4.2 | −3.2 |
| mean \|S\| | 3.4 × 10⁻⁴ | 3.4 × 10⁻⁴ | 3.3 × 10⁻⁴ | 3.2 × 10⁻⁴ | 3.2 × 10⁻⁴ | 3.1 × 10⁻⁴ | 3.0 × 10⁻⁴ |

- The twist is confined to a few sites from the faces. It is real, director-type (|S| ≈ 3 × 10⁻⁴, against up to 3 in the 1D textures), and has no lines.
- Its energy is the same for ±γ: the handedness adapts.
- It scales close to γ²: every main run ends in the same line-free state, at −15.645 (|γ| = 0.1), −62.689 (0.2) and −141.463 (0.3). The ratios are 4.01 and 9.04.

This matters for reading the runs:
1. E late in every run is negative. That is the surface state, not a bound loop.
2. The surface twist forms within the first few iterations, and it makes up most of E_χ in every record (§6.4).
3. The scaling (virial) identity does not hold for this boundary-bound state. Its residual is −0.257 at |γ| = 0.3 and −0.258 at 0.1.

I did not run C0 at γ = 0, or at |γ| = 0.1 and 0.2, because PREREG §4 lists C0 only at ±0.3. The main runs' own final states give the surface energy at 0.1 and 0.2.

### 3.6 Starts

At 65³, R₀ = 6: `[{'nseg': [96, 96, 96], 'Lk12': -1.0, 'Lk13': -1.0, 'Lk23': 0.0}, {'nseg': [114, 96, 96], 'Lk12': -1.0000000000000004, 'Lk13': -1.0000000000000004, 'Lk23': 0.0}]`. So |Lk12| = |Lk13| = 1 for A and B, with Lk = −1. The starts have A = 0 and almost no chiral energy: E_χ at iteration 0 is −3.3 × 10⁻⁴ (A) and −6.9 × 10⁻⁴ (B) at γ = +0.3, linear in γ. So the ± runs start from the same E to 10⁻⁷.

### 3.7 Run times and convergence

Every run stopped on `CONVERGENCE: NORM OF PROJECTED GRADIENT <= PGTOL`.

| run | γ = +0.1 | −0.1 | +0.2 | −0.2 | +0.3 | −0.3 |
|---|---|---|---|---|---|---|
| A: iterations / s | 126 / 160 | 124 / 158 | 147 / 200 | 150 / 196 | 209 / 279 | 227 / 303 |
| B: iterations / s | 132 / 180 | 130 / 177 | 157 / 214 | 163 / 216 | 223 / 283 | 218 / 274 |
| control N = 0: iterations / s | — | — | — | — | 226 / 266 | 221 / 262 |

## 4. P1: the N = 0 ring at γ = ±0.3

`control_N0_chiral.py 65 6 ±0.3 4000 2`. Every 4th record is shown up to the first record with no lines. R is `gl3.core_radius`. nseg is the segment count of strands (1, 2, 3).

**γ = +0.3:** E_start 3031.0 E_end -141.4629 R_end 0.0 nseg_end [0, 0, 0] iters 226 CONVERGENCE: NORM OF PROJECTED GRADIENT <= PGTOL split_end {'E_grad': 46.14508274020832, 'E_mag': 2.594490669914337e-07, 'E_V': 96.81381408372727, 'E_chi': -284.42182435557396, 'E_chi_AS': -0.02136077639653422}

| it | E | R (strand 2) | R (strand 1) | nseg | E_grad | E_mag | E_V | E_χ | E_χ (A·S) |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 2870.7 | 6.02 | 6.02 | [94, 94, 132] | 2300.5 | 0.10 | 622.6 | -52.5 | 0.08 |
| 4 | 1356.1 | 5.81 | 5.81 | [92, 92, 96] | 1338.1 | 43.43 | 477.7 | -503.2 | 67.79 |
| 8 | 827.3 | 5.59 | 5.59 | [90, 90, 92] | 851.9 | 146.38 | 415.4 | -586.4 | 299.42 |
| 12 | 762.5 | 5.49 | 5.49 | [86, 86, 92] | 797.3 | 148.47 | 387.8 | -571.0 | 318.80 |
| 16 | 719.0 | 5.23 | 5.23 | [84, 84, 88] | 699.6 | 147.74 | 443.2 | -571.6 | 328.13 |
| 20 | 653.0 | 4.72 | 4.72 | [78, 78, 80] | 664.2 | 128.60 | 338.4 | -478.2 | 277.28 |
| 24 | 590.6 | 4.34 | 4.34 | [68, 68, 72] | 648.5 | 124.40 | 308.4 | -490.7 | 245.89 |
| 28 | 487.0 | 3.71 | 3.71 | [60, 60, 62] | 573.3 | 106.89 | 252.2 | -445.4 | 179.01 |
| 32 | 392.2 | 3.03 | 3.03 | [52, 52, 56] | 493.3 | 93.01 | 220.8 | -415.0 | 136.29 |
| 36 | 271.6 | 2.25 | 2.25 | [36, 36, 42] | 365.2 | 82.23 | 218.1 | -393.9 | 120.96 |
| 40 | 139.4 | 1.37 | 1.37 | [20, 20, 26] | 268.0 | 66.09 | 170.0 | -364.7 | 126.91 |
| 44 | -21.3 | 0.00 | 0.00 | [0, 0, 0] | 132.0 | 25.60 | 119.0 | -297.9 | 130.38 |

**γ = −0.3:** E_start 3031.0 E_end -141.4629 R_end 0.0 nseg_end [0, 0, 0] iters 221 CONVERGENCE: NORM OF PROJECTED GRADIENT <= PGTOL split_end {'E_grad': 46.144322591117316, 'E_mag': 6.99568514456845e-07, 'E_V': 96.8135747658016, 'E_chi': -284.4208216968635, 'E_chi_AS': -0.05475295952498982}

| it | E | R (strand 2) | R (strand 1) | nseg | E_grad | E_mag | E_V | E_χ | E_χ (A·S) |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 2870.7 | 6.02 | 6.02 | [94, 94, 130] | 2300.5 | 0.10 | 622.6 | -52.5 | 0.08 |
| 4 | 1356.1 | 5.81 | 5.81 | [92, 92, 96] | 1338.1 | 43.43 | 477.7 | -503.2 | 67.79 |
| 8 | 827.3 | 5.59 | 5.59 | [90, 90, 92] | 851.9 | 146.38 | 415.4 | -586.4 | 299.42 |
| 12 | 762.5 | 5.49 | 5.49 | [86, 86, 92] | 797.3 | 148.47 | 387.8 | -571.0 | 318.80 |
| 16 | 719.0 | 5.23 | 5.23 | [84, 84, 88] | 699.6 | 147.74 | 443.2 | -571.6 | 328.13 |
| 20 | 653.0 | 4.72 | 4.72 | [78, 78, 80] | 664.2 | 128.60 | 338.4 | -478.2 | 277.28 |
| 24 | 590.6 | 4.34 | 4.34 | [68, 68, 72] | 648.5 | 124.40 | 308.4 | -490.7 | 245.89 |
| 28 | 487.0 | 3.71 | 3.71 | [60, 60, 62] | 573.3 | 106.89 | 252.2 | -445.4 | 179.01 |
| 32 | 392.2 | 3.03 | 3.03 | [52, 52, 56] | 493.3 | 93.01 | 220.8 | -415.0 | 136.29 |
| 36 | 271.6 | 2.25 | 2.25 | [36, 36, 42] | 365.2 | 82.23 | 218.1 | -393.9 | 120.96 |
| 40 | 139.4 | 1.37 | 1.37 | [20, 20, 26] | 268.0 | 66.09 | 170.0 | -364.7 | 126.91 |
| 44 | -21.3 | 0.00 | 0.00 | [0, 0, 0] | 132.0 | 25.60 | 119.0 | -297.9 | 130.38 |

- **P1 holds at both signs.** The untwisted ring shrinks monotonically and all lines are gone by record 44. The run then relaxes to the same surface state as C0 (E_end = −141.4629, no segments).
- **The ±0.3 control trajectories are the same** to ≤ 1.5 × 10⁻⁷ relative over records 0–44. This is exact, not an accident. The control start ψ = (f, f, f), with f(−x) = f(x)*, is mapped to itself (up to a global sign, which is a gauge) by inversion combined with complex conjugation. Inversion flips E_χ, and conjugation leaves every term unchanged (`NOTE_chiral_term.md` §1.1). So the +γ and −γ functionals are exactly equivalent from this start.
- **The locked chiral term splits strand 3 from strands 1 and 2.** In γ = 0 runs all three coincide. Here strands 1 and 2 stay identical, while strand 3, along the ring axis, carries more segments (for example 26 against 20 at record 40). Strand 3 is the locked axis normal to the ring.
- The chiral coupling is not small in the control, against P1's stated reason. E_χ reaches −586 at record 8, and the A·S part is up to +328. Most of E_χ is the surface twist (−284 in the end state). The control still collapses.

## 5. Main runs: tables per γ

Columns are as in `REPORT_N1_cells.md` §4, with these differences:
- "R s2 / s3" and "len s2 / s3" are given separately for strands 2 and 3. In every chiral run they **do not coincide**: their segment counts differ from iteration 2 on (a γ = 0 run keeps them identical).
- "sep" is the min / mean distance from strand 1's line to strand 2's line, as in `trace_N1.py`.
- "Lk₁₂ / Lk₁₃" are both given.
- A non-integer Lk means touching lattice curves, where the linking number is undefined.
- E_χ near line 1 is the chiral energy within distance 3 of strand 1's line.
- ⟨|S|/|ψ|²⟩_w is weighted by |Dψ|².

Every recorded row is shown up to the first row with no lines, then the final record.

### 5.1 γ = +0.1

**Start A** (`trace_N1_chiral_A_N65_R6_g+0.1.json`). iters 126, CONVERGENCE: NORM OF PROJECTED GRADIENT <= PGTOL, final E -15.6452, nseg [0, 0, 0], all lines gone at it 28, line 1 gone at it 22, time 160 s.

Geometry:

| it | E | R s2 / s3 | len s2 / s3 | R line 1 | centroid x 1 | z_rms 1 | len 1 | wall gap 1 | open ends | W_z(1) | sep min / mean | Lk₁₂ / Lk₁₃ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 2895.3 | 5.92 / 5.92 | 48.0/48.0 | 6.15 | 6.13 | 4.18 | 48.0 | 3.75 | 0 | 0 | 5.49 / 5.76 | -1.000 / -1.000 |
| 2 | 2082.0 | 5.26 / 5.32 | 43.0/44.0 | 5.65 | 5.63 | 3.57 | 43.0 | 5.25 | 0 | 0 | 4.29 / 4.95 | -1.000 / -1.000 |
| 4 | 1747.6 | 5.18 / 5.15 | 43.0/42.0 | 5.81 | 5.80 | 3.45 | 40.0 | 5.25 | 0 | 0 | 3.92 / 4.82 | -1.000 / -1.000 |
| 6 | 1521.9 | 4.81 / 4.82 | 39.0/40.0 | 5.60 | 5.59 | 3.13 | 38.0 | 5.75 | 0 | 0 | 3.48 / 4.48 | -1.000 / -1.000 |
| 8 | 1276.6 | 4.24 / 4.26 | 35.0/35.0 | 5.28 | 5.24 | 2.61 | 34.0 | 6.75 | 0 | 0 | 2.42 / 3.73 | -1.000 / -1.000 |
| 10 | 1086.5 | 4.03 / 4.03 | 33.0/33.0 | 5.32 | 5.27 | 2.31 | 32.0 | 6.75 | 0 | 0 | 2.09 / 3.44 | -1.000 / -1.000 |
| 12 | 979.8 | 3.56 / 3.63 | 30.0/31.0 | 5.00 | 4.94 | 1.94 | 28.0 | 7.75 | 0 | 0 | 1.27 / 2.92 | -1.000 / -1.000 |
| 14 | 864.8 | 3.50 / 3.53 | 29.0/30.0 | 5.02 | 4.95 | 1.86 | 28.0 | 7.75 | 0 | 0 | 1.22 / 2.85 | -1.000 / -1.000 |
| 16 | 720.7 | 2.92 / 3.06 | 25.0/26.0 | 4.74 | 4.67 | 1.22 | 21.0 | 8.75 | 0 | 0 | 0.00 / 2.14 | -0.625 / -0.875 |
| 18 | 619.3 | 2.81 / 2.89 | 25.0/25.0 | 4.49 | 4.42 | 1.03 | 19.0 | 9.25 | 0 | 0 | 0.00 / 1.88 | -0.500 / -0.375 |
| 20 | 495.9 | 2.28 / 2.46 | 21.0/22.0 | 4.28 | 4.25 | 0.47 | 10.0 | 10.25 | 0 | 0 | 0.50 / 1.71 | -0.000 / -0.125 |
| 22 | 409.5 | 1.96 / 2.17 | 17.0/17.0 | — | — | — | 0.0 | — | — | — | — | 0 (no line 1) |
| 24 | 319.9 | 1.45 / 1.66 | 11.0/13.0 | — | — | — | 0.0 | — | — | — | — | 0 (no line 1) |
| 26 | 230.4 | 1.01 / 1.42 | 7.0/10.0 | — | — | — | 0.0 | — | — | — | — | 0 (no line 1) |
| 28 | 162.1 | — / — | 0.0/0.0 | — | — | — | 0.0 | — | — | — | — | 0 (no lines) |
| 126 (final) | -15.6 | — / — | 0.0/0.0 | — | — | — | 0.0 | — | — | — | — | 0 (no lines) |

Energy split and §4 diagnostics:

| it | E | E_grad | E_mag | E_V | E_χ | E_χ (A·S part) | ⟨\|S\|/\|ψ\|²⟩_w | E_χ near line 1 | virial |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 2895.3 | 1642.5 | 0.00 | 1252.8 | -0.0 | 0.00 | 0.561 | 0.24 | 1.000 |
| 2 | 2082.0 | 1098.0 | 14.82 | 1002.8 | -33.7 | -7.41 | 0.470 | -3.95 | 0.961 |
| 4 | 1747.6 | 870.4 | 15.73 | 920.4 | -59.0 | -8.07 | 0.519 | -4.12 | 0.929 |
| 6 | 1521.9 | 794.8 | 25.85 | 752.6 | -51.3 | -10.65 | 0.520 | -5.31 | 0.919 |
| 8 | 1276.6 | 753.3 | 62.33 | 510.1 | -49.1 | -12.28 | 0.517 | -7.83 | 0.869 |
| 10 | 1086.5 | 654.9 | 69.55 | 425.6 | -63.6 | -11.46 | 0.530 | -8.37 | 0.815 |
| 12 | 979.8 | 641.1 | 82.84 | 330.8 | -75.0 | -8.66 | 0.506 | -8.54 | 0.750 |
| 14 | 864.8 | 541.0 | 82.60 | 309.8 | -68.6 | -8.26 | 0.531 | -8.43 | 0.740 |
| 16 | 720.7 | 478.7 | 94.73 | 202.2 | -55.0 | -3.50 | 0.495 | -7.96 | 0.683 |
| 18 | 619.3 | 390.5 | 89.60 | 192.2 | -53.0 | -3.01 | 0.507 | -7.19 | 0.663 |
| 20 | 495.9 | 327.0 | 89.54 | 130.5 | -51.2 | -0.03 | 0.436 | -5.52 | 0.578 |
| 22 | 409.5 | 262.5 | 81.69 | 110.9 | -45.6 | 0.71 | 0.411 | — | 0.550 |
| 24 | 319.9 | 204.9 | 64.10 | 87.9 | -36.9 | 1.39 | 0.337 | — | 0.545 |
| 26 | 230.4 | 149.9 | 58.33 | 59.8 | -37.5 | 2.21 | 0.344 | — | 0.423 |
| 28 | 162.1 | 125.1 | 34.02 | 40.8 | -37.8 | 2.72 | 0.195 | — | 0.386 |
| 126 (final) | -15.6 | 5.0 | 0.00 | 10.6 | -31.3 | 0.00 | 0.000 | — | -0.258 |

Surface-subtracted virial residual (descriptive; §7): 0: +1.000, 2: +0.990, 4: +0.961, 6: +0.957, 8: +0.916, 10: +0.868, 12: +0.807, 14: +0.802, 16: +0.761, 18: +0.750, 20: +0.681, 22: +0.670, 24: +0.703, 26: +0.610.

**Start B** (`trace_N1_chiral_B_N65_R6_g+0.1.json`). iters 132, CONVERGENCE: NORM OF PROJECTED GRADIENT <= PGTOL, final E -15.6452, nseg [0, 0, 0], all lines gone at it 36, line 1 gone at it 36, time 180 s.

Geometry:

| it | E | R s2 / s3 | len s2 / s3 | R line 1 | centroid x 1 | z_rms 1 | len 1 | wall gap 1 | open ends | W_z(1) | sep min / mean | Lk₁₂ / Lk₁₃ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 2442.0 | 5.92 / 5.92 | 48.0/48.0 | 6.31 | 1.99 | 1.36 | 57.0 | 7.75 | 0 | 1 | 1.46 / 1.95 | -1.000 / -1.000 |
| 2 | 1649.9 | 5.37 / 5.38 | 43.0/44.0 | 5.64 | 1.52 | 1.25 | 53.0 | 8.75 | 0 | 1 | 1.22 / 1.64 | -1.000 / -1.000 |
| 4 | 1326.7 | 5.26 / 5.26 | 43.0/43.0 | 5.51 | 1.70 | 1.10 | 51.0 | 8.75 | 0 | 1 | 1.00 / 1.57 | -1.000 / -1.000 |
| 6 | 1180.6 | 5.02 / 5.04 | 43.0/41.0 | 5.30 | 1.54 | 0.94 | 47.0 | 9.25 | 0 | 1 | 0.94 / 1.40 | -1.000 / -1.000 |
| 8 | 982.6 | 4.61 / 4.61 | 39.0/38.0 | 4.88 | 1.44 | 0.83 | 43.0 | 9.75 | 0 | 1 | 0.61 / 1.22 | -1.000 / -1.000 |
| 10 | 853.3 | 4.41 / 4.48 | 35.0/36.0 | 4.68 | 1.29 | 0.76 | 40.0 | 10.25 | 0 | 1 | 0.50 / 1.15 | -1.000 / -0.875 |
| 12 | 799.4 | 4.24 / 4.27 | 36.0/35.0 | 4.53 | 1.24 | 0.65 | 40.0 | 10.25 | 0 | 1 | 0.00 / 0.93 | -0.500 / -0.750 |
| 14 | 761.6 | 4.09 / 4.14 | 35.0/33.0 | 4.30 | 1.04 | 0.49 | 37.0 | 10.75 | 0 | 1 | 0.35 / 0.84 | 0.000 / -0.625 |
| 16 | 726.1 | 3.91 / 4.00 | 33.0/33.0 | 4.08 | 0.82 | 0.49 | 34.0 | 11.25 | 0 | 1 | 0.35 / 0.74 | 0.125 / -0.250 |
| 18 | 699.8 | 3.80 / 3.85 | 32.0/33.0 | 3.97 | 0.80 | 0.47 | 34.0 | 11.25 | 0 | 1 | 0.50 / 0.70 | 0.000 / -0.500 |
| 20 | 662.6 | 3.64 / 3.69 | 32.0/31.0 | 3.72 | 0.56 | 0.39 | 31.0 | 11.75 | 0 | 1 | 0.00 / 0.59 | 0.125 / 0.250 |
| 22 | 615.1 | 3.37 / 3.39 | 28.0/29.0 | 3.34 | 0.31 | 0.25 | 27.0 | 12.25 | 0 | 1 | 0.00 / 0.58 | -0.375 / -0.500 |
| 24 | 559.8 | 3.13 / 3.18 | 27.0/25.0 | 3.06 | 0.26 | 0.25 | 24.0 | 12.75 | 0 | 1 | 0.00 / 0.61 | -0.125 / -0.500 |
| 26 | 508.6 | 2.90 / 2.89 | 25.0/23.0 | 2.73 | 0.15 | 0.24 | 22.0 | 13.25 | 0 | 1 | 0.00 / 0.61 | -0.500 / -0.500 |
| 28 | 452.1 | 2.61 / 2.63 | 22.0/21.0 | 2.37 | 0.21 | 0.24 | 20.0 | 13.25 | 0 | 1 | 0.00 / 0.50 | -0.250 / -0.250 |
| 30 | 370.5 | 2.15 / 2.18 | 18.0/17.0 | 1.84 | 0.22 | 0.24 | 16.0 | 13.75 | 0 | 1 | 0.00 / 0.50 | 0.125 / -0.000 |
| 32 | 309.9 | 1.76 / 1.76 | 13.0/14.0 | 1.46 | 0.27 | 0.24 | 13.0 | 14.25 | 0 | 1 | 0.00 / 0.47 | 0.250 / -0.125 |
| 34 | 199.9 | 1.21 / 1.10 | 8.0/8.0 | 0.61 | 0.25 | 0.22 | 5.0 | 15.25 | 0 | 1 | 0.00 / 0.44 | 0.250 / 0.875 |
| 36 | 100.2 | — / — | 0.0/0.0 | — | — | — | 0.0 | — | — | — | — | 0 (no lines) |
| 132 (final) | -15.6 | — / — | 0.0/0.0 | — | — | — | 0.0 | — | — | — | — | 0 (no lines) |

Energy split and §4 diagnostics:

| it | E | E_grad | E_mag | E_V | E_χ | E_χ (A·S part) | ⟨\|S\|/\|ψ\|²⟩_w | E_χ near line 1 | virial |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 2442.0 | 1687.0 | 0.00 | 755.0 | -0.0 | 0.00 | 0.427 | -0.06 | 1.000 |
| 2 | 1649.9 | 1096.8 | 20.32 | 560.1 | -27.4 | 0.78 | 0.337 | -6.33 | 0.947 |
| 4 | 1326.7 | 878.0 | 21.06 | 478.3 | -50.6 | 0.97 | 0.364 | -6.70 | 0.900 |
| 6 | 1180.6 | 787.6 | 34.06 | 403.4 | -44.4 | 2.42 | 0.379 | -8.62 | 0.884 |
| 8 | 982.6 | 683.1 | 84.49 | 254.9 | -39.9 | 8.82 | 0.410 | -13.29 | 0.796 |
| 10 | 853.3 | 598.9 | 103.92 | 199.5 | -49.0 | 11.55 | 0.417 | -14.83 | 0.711 |
| 12 | 799.4 | 548.4 | 128.81 | 177.3 | -55.1 | 14.68 | 0.411 | -16.41 | 0.638 |
| 14 | 761.6 | 492.6 | 139.82 | 185.5 | -56.3 | 15.48 | 0.405 | -16.28 | 0.612 |
| 16 | 726.1 | 443.3 | 157.22 | 177.3 | -51.8 | 16.71 | 0.406 | -15.95 | 0.578 |
| 18 | 699.8 | 410.3 | 164.89 | 173.0 | -48.4 | 16.53 | 0.404 | -15.34 | 0.561 |
| 20 | 662.6 | 376.9 | 168.66 | 162.3 | -45.2 | 14.93 | 0.398 | -13.95 | 0.539 |
| 22 | 615.1 | 341.5 | 168.76 | 147.9 | -43.1 | 10.69 | 0.408 | -11.09 | 0.510 |
| 24 | 559.8 | 316.7 | 149.09 | 135.9 | -41.9 | 6.79 | 0.402 | -8.73 | 0.513 |
| 26 | 508.6 | 301.1 | 125.48 | 121.3 | -39.3 | 4.02 | 0.388 | -6.89 | 0.530 |
| 28 | 452.1 | 285.6 | 97.50 | 107.2 | -38.3 | 2.57 | 0.357 | -5.82 | 0.555 |
| 30 | 370.5 | 251.9 | 79.08 | 78.5 | -39.0 | 1.20 | 0.341 | -4.08 | 0.513 |
| 32 | 309.9 | 220.8 | 62.55 | 63.1 | -36.6 | 1.14 | 0.302 | -3.27 | 0.503 |
| 34 | 199.9 | 145.0 | 34.61 | 47.9 | -27.6 | 2.43 | 0.262 | -1.78 | 0.525 |
| 36 | 100.2 | 79.8 | 24.90 | 26.0 | -30.5 | 2.54 | 0.180 | — | 0.295 |
| 132 (final) | -15.6 | 5.0 | 0.00 | 10.6 | -31.3 | 0.00 | 0.000 | — | -0.258 |

Surface-subtracted virial residual (descriptive; §7): 0: +1.000, 2: +0.985, 4: +0.949, 6: +0.940, 8: +0.866, 10: +0.786, 12: +0.711, 14: +0.684, 16: +0.651, 18: +0.635, 20: +0.616, 22: +0.591, 24: +0.603, 26: +0.632, 28: +0.673, 30: +0.653, 32: +0.673, 34: +0.764.

### 5.2 γ = -0.1

**Start A** (`trace_N1_chiral_A_N65_R6_g-0.1.json`). iters 124, CONVERGENCE: NORM OF PROJECTED GRADIENT <= PGTOL, final E -15.6452, nseg [0, 0, 0], all lines gone at it 28, line 1 gone at it 22, time 158 s.

Geometry:

| it | E | R s2 / s3 | len s2 / s3 | R line 1 | centroid x 1 | z_rms 1 | len 1 | wall gap 1 | open ends | W_z(1) | sep min / mean | Lk₁₂ / Lk₁₃ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 2895.3 | 5.92 / 5.92 | 48.0/48.0 | 6.15 | 6.13 | 4.18 | 48.0 | 3.75 | 0 | 0 | 5.49 / 5.76 | -1.000 / -1.000 |
| 2 | 2082.0 | 5.31 / 5.25 | 44.0/43.0 | 5.64 | 5.63 | 3.57 | 43.0 | 5.25 | 0 | 0 | 4.54 / 4.87 | -1.000 / -1.000 |
| 4 | 1747.6 | 5.14 / 5.19 | 42.0/43.0 | 5.81 | 5.80 | 3.44 | 40.0 | 5.25 | 0 | 0 | 4.11 / 4.87 | -1.000 / -1.000 |
| 6 | 1521.9 | 4.83 / 4.81 | 40.0/39.0 | 5.59 | 5.58 | 3.14 | 38.0 | 5.75 | 0 | 0 | 3.69 / 4.39 | -1.000 / -1.000 |
| 8 | 1276.7 | 4.25 / 4.24 | 35.0/35.0 | 5.27 | 5.24 | 2.61 | 34.0 | 6.75 | 0 | 0 | 2.76 / 3.63 | -1.000 / -1.000 |
| 10 | 1086.4 | 4.05 / 3.99 | 33.0/33.0 | 5.32 | 5.27 | 2.31 | 32.0 | 6.75 | 0 | 0 | 2.42 / 3.37 | -1.000 / -1.000 |
| 12 | 979.7 | 3.62 / 3.59 | 30.0/31.0 | 5.00 | 4.94 | 1.94 | 28.0 | 7.75 | 0 | 0 | 1.62 / 2.83 | -1.000 / -1.000 |
| 14 | 864.6 | 3.52 / 3.49 | 29.0/30.0 | 5.02 | 4.95 | 1.84 | 28.0 | 7.75 | 0 | 0 | 1.54 / 2.73 | -1.000 / -1.000 |
| 16 | 720.5 | 2.98 / 2.88 | 25.0/25.0 | 4.74 | 4.67 | 1.19 | 21.0 | 8.75 | 0 | 0 | 0.35 / 1.97 | -0.875 / -0.125 |
| 18 | 619.4 | 2.89 / 2.80 | 25.0/25.0 | 4.49 | 4.42 | 1.03 | 19.0 | 9.25 | 0 | 0 | 0.00 / 1.67 | -0.750 / -0.125 |
| 20 | 496.3 | 2.48 / 2.31 | 22.0/20.0 | 4.25 | 4.22 | 0.50 | 10.0 | 10.25 | 0 | 0 | 0.35 / 1.18 | -0.125 / 0.000 |
| 22 | 410.0 | 2.17 / 1.97 | 18.0/16.0 | — | — | — | 0.0 | — | — | — | — | 0 (no line 1) |
| 24 | 320.3 | 1.71 / 1.46 | 14.0/12.0 | — | — | — | 0.0 | — | — | — | — | 0 (no line 1) |
| 26 | 230.3 | 1.35 / 1.05 | 9.0/9.0 | — | — | — | 0.0 | — | — | — | — | 0 (no line 1) |
| 28 | 161.6 | — / — | 0.0/0.0 | — | — | — | 0.0 | — | — | — | — | 0 (no lines) |
| 124 (final) | -15.6 | — / — | 0.0/0.0 | — | — | — | 0.0 | — | — | — | — | 0 (no lines) |

Energy split and §4 diagnostics:

| it | E | E_grad | E_mag | E_V | E_χ | E_χ (A·S part) | ⟨\|S\|/\|ψ\|²⟩_w | E_χ near line 1 | virial |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 2895.3 | 1642.5 | 0.00 | 1252.8 | 0.0 | 0.00 | 0.561 | -0.24 | 1.000 |
| 2 | 2082.0 | 1098.0 | 14.82 | 1002.8 | -33.7 | -7.41 | 0.469 | -3.92 | 0.961 |
| 4 | 1747.6 | 870.5 | 15.73 | 920.4 | -59.0 | -8.07 | 0.518 | -4.10 | 0.929 |
| 6 | 1521.9 | 794.8 | 25.85 | 752.6 | -51.3 | -10.67 | 0.519 | -5.35 | 0.919 |
| 8 | 1276.7 | 753.3 | 62.31 | 510.3 | -49.3 | -12.37 | 0.514 | -8.12 | 0.868 |
| 10 | 1086.4 | 655.0 | 69.54 | 425.6 | -63.8 | -11.57 | 0.527 | -8.71 | 0.815 |
| 12 | 979.7 | 641.5 | 82.87 | 330.6 | -75.3 | -8.83 | 0.505 | -9.04 | 0.750 |
| 14 | 864.6 | 541.2 | 82.61 | 309.6 | -68.8 | -8.42 | 0.529 | -8.88 | 0.739 |
| 16 | 720.5 | 478.8 | 94.65 | 202.3 | -55.3 | -3.61 | 0.492 | -8.25 | 0.682 |
| 18 | 619.4 | 390.9 | 89.55 | 192.3 | -53.3 | -3.05 | 0.502 | -7.42 | 0.663 |
| 20 | 496.3 | 327.5 | 89.38 | 130.9 | -51.4 | 0.02 | 0.429 | -5.74 | 0.579 |
| 22 | 410.0 | 262.9 | 81.59 | 111.2 | -45.7 | 0.81 | 0.403 | — | 0.551 |
| 24 | 320.3 | 204.9 | 64.08 | 88.1 | -36.8 | 1.51 | 0.329 | — | 0.546 |
| 26 | 230.3 | 149.6 | 58.08 | 59.8 | -37.2 | 2.35 | 0.329 | — | 0.426 |
| 28 | 161.6 | 124.6 | 33.93 | 40.7 | -37.5 | 2.83 | 0.185 | — | 0.387 |
| 124 (final) | -15.6 | 5.0 | 0.00 | 10.6 | -31.3 | 0.00 | 0.000 | — | -0.258 |

Surface-subtracted virial residual (descriptive; §7): 0: +1.000, 2: +0.990, 4: +0.961, 6: +0.957, 8: +0.916, 10: +0.868, 12: +0.807, 14: +0.802, 16: +0.761, 18: +0.749, 20: +0.681, 22: +0.671, 24: +0.704, 26: +0.614.

**Start B** (`trace_N1_chiral_B_N65_R6_g-0.1.json`). iters 130, CONVERGENCE: NORM OF PROJECTED GRADIENT <= PGTOL, final E -15.6452, nseg [0, 0, 0], all lines gone at it 36, line 1 gone at it 36, time 177 s.

Geometry:

| it | E | R s2 / s3 | len s2 / s3 | R line 1 | centroid x 1 | z_rms 1 | len 1 | wall gap 1 | open ends | W_z(1) | sep min / mean | Lk₁₂ / Lk₁₃ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 2442.0 | 5.92 / 5.92 | 48.0/48.0 | 6.31 | 1.99 | 1.36 | 57.0 | 7.75 | 0 | 1 | 1.46 / 1.95 | -1.000 / -1.000 |
| 2 | 1649.9 | 5.40 / 5.35 | 44.0/43.0 | 5.64 | 1.51 | 1.24 | 53.0 | 8.75 | 0 | 1 | 1.00 / 1.44 | -1.000 / -1.000 |
| 4 | 1326.7 | 5.27 / 5.26 | 43.0/43.0 | 5.50 | 1.70 | 1.10 | 51.0 | 8.75 | 0 | 1 | 1.00 / 1.48 | -1.000 / -1.000 |
| 6 | 1180.5 | 5.04 / 5.00 | 42.0/42.0 | 5.30 | 1.52 | 0.97 | 48.0 | 9.25 | 0 | 1 | 0.87 / 1.29 | -1.000 / -1.000 |
| 8 | 982.5 | 4.63 / 4.61 | 39.0/38.0 | 4.89 | 1.43 | 0.83 | 43.0 | 9.75 | 0 | 1 | 0.50 / 1.04 | -1.000 / -1.000 |
| 10 | 853.3 | 4.43 / 4.44 | 35.0/36.0 | 4.68 | 1.28 | 0.76 | 40.0 | 10.25 | 0 | 1 | 0.35 / 0.92 | -0.875 / -0.875 |
| 12 | 799.4 | 4.28 / 4.22 | 36.0/35.0 | 4.51 | 1.23 | 0.66 | 40.0 | 10.25 | 0 | 1 | 0.00 / 0.71 | -0.625 / -0.750 |
| 14 | 761.5 | 4.14 / 4.09 | 35.0/33.0 | 4.29 | 1.05 | 0.50 | 36.0 | 10.75 | 0 | 1 | 0.00 / 0.65 | -0.250 / -0.500 |
| 16 | 726.1 | 3.98 / 3.92 | 33.0/33.0 | 4.08 | 0.82 | 0.49 | 34.0 | 11.25 | 0 | 1 | 0.00 / 0.60 | 0.000 / -0.375 |
| 18 | 699.8 | 3.88 / 3.77 | 32.0/32.0 | 3.97 | 0.80 | 0.47 | 34.0 | 11.25 | 0 | 1 | 0.50 / 0.61 | -0.000 / -0.250 |
| 20 | 662.6 | 3.73 / 3.63 | 32.0/30.0 | 3.72 | 0.56 | 0.40 | 31.0 | 11.75 | 0 | 1 | 0.00 / 0.60 | -0.000 / -0.000 |
| 22 | 615.0 | 3.38 / 3.29 | 28.0/29.0 | 3.36 | 0.30 | 0.25 | 27.0 | 12.25 | 0 | 1 | 0.00 / 0.72 | -0.500 / -0.125 |
| 24 | 559.6 | 3.17 / 3.12 | 27.0/25.0 | 3.05 | 0.25 | 0.25 | 24.0 | 12.75 | 0 | 1 | 0.00 / 0.77 | -0.500 / -0.500 |
| 26 | 508.3 | 2.84 / 2.87 | 24.0/24.0 | 2.67 | 0.18 | 0.24 | 22.0 | 13.25 | 0 | 1 | 0.00 / 0.72 | -0.500 / -0.375 |
| 28 | 451.6 | 2.47 / 2.63 | 20.0/21.0 | 2.37 | 0.21 | 0.24 | 20.0 | 13.25 | 0 | 1 | 0.00 / 0.60 | -0.250 / -0.375 |
| 30 | 368.8 | 2.06 / 2.14 | 16.0/17.0 | 1.84 | 0.22 | 0.24 | 16.0 | 13.75 | 0 | 1 | 0.00 / 0.58 | 0.000 / 0.000 |
| 32 | 307.8 | 1.67 / 1.72 | 13.0/14.0 | 1.43 | 0.29 | 0.24 | 13.0 | 14.25 | 0 | 1 | 0.00 / 0.50 | 0.375 / -0.000 |
| 34 | 195.8 | 1.07 / 1.19 | 7.0/10.0 | 0.61 | 0.25 | 0.22 | 5.0 | 15.25 | 0 | 1 | 0.00 / 0.43 | 0.375 / 0.375 |
| 36 | 95.1 | — / — | 0.0/0.0 | — | — | — | 0.0 | — | — | — | — | 0 (no lines) |
| 130 (final) | -15.6 | — / — | 0.0/0.0 | — | — | — | 0.0 | — | — | — | — | 0 (no lines) |

Energy split and §4 diagnostics:

| it | E | E_grad | E_mag | E_V | E_χ | E_χ (A·S part) | ⟨\|S\|/\|ψ\|²⟩_w | E_χ near line 1 | virial |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 2442.0 | 1687.0 | 0.00 | 755.0 | 0.0 | 0.00 | 0.427 | 0.06 | 1.000 |
| 2 | 1649.9 | 1096.8 | 20.32 | 560.1 | -27.4 | 0.78 | 0.337 | -6.36 | 0.947 |
| 4 | 1326.7 | 878.0 | 21.06 | 478.3 | -50.6 | 0.97 | 0.364 | -6.68 | 0.900 |
| 6 | 1180.5 | 787.6 | 34.07 | 403.4 | -44.4 | 2.43 | 0.379 | -8.65 | 0.884 |
| 8 | 982.5 | 683.0 | 84.50 | 254.8 | -39.8 | 8.85 | 0.409 | -13.28 | 0.796 |
| 10 | 853.3 | 598.8 | 103.93 | 199.5 | -48.9 | 11.60 | 0.417 | -14.78 | 0.712 |
| 12 | 799.4 | 548.4 | 128.82 | 177.3 | -55.1 | 14.74 | 0.418 | -16.38 | 0.638 |
| 14 | 761.5 | 492.5 | 139.81 | 185.5 | -56.3 | 15.54 | 0.415 | -16.28 | 0.612 |
| 16 | 726.1 | 443.3 | 157.21 | 177.4 | -51.8 | 16.76 | 0.416 | -16.00 | 0.578 |
| 18 | 699.8 | 410.4 | 164.85 | 173.0 | -48.5 | 16.57 | 0.412 | -15.44 | 0.560 |
| 20 | 662.6 | 376.9 | 168.62 | 162.3 | -45.3 | 14.96 | 0.395 | -14.05 | 0.538 |
| 22 | 615.0 | 341.6 | 168.71 | 147.9 | -43.1 | 10.72 | 0.392 | -11.16 | 0.510 |
| 24 | 559.6 | 316.6 | 149.01 | 135.8 | -41.9 | 6.85 | 0.385 | -8.74 | 0.514 |
| 26 | 508.3 | 300.9 | 125.55 | 121.0 | -39.2 | 4.07 | 0.375 | -6.84 | 0.530 |
| 28 | 451.6 | 285.6 | 96.95 | 107.3 | -38.2 | 2.62 | 0.344 | -5.74 | 0.556 |
| 30 | 368.8 | 251.0 | 78.77 | 77.9 | -38.9 | 1.25 | 0.333 | -3.97 | 0.512 |
| 32 | 307.8 | 219.7 | 61.65 | 62.9 | -36.4 | 1.20 | 0.297 | -3.15 | 0.505 |
| 34 | 195.8 | 141.6 | 34.26 | 47.2 | -27.3 | 2.48 | 0.265 | -1.77 | 0.522 |
| 36 | 95.1 | 77.1 | 23.84 | 25.3 | -31.1 | 2.58 | 0.171 | — | 0.280 |
| 130 (final) | -15.6 | 5.0 | 0.00 | 10.6 | -31.3 | -0.00 | 0.000 | — | -0.258 |

Surface-subtracted virial residual (descriptive; §7): 0: +1.000, 2: +0.985, 4: +0.949, 6: +0.940, 8: +0.866, 10: +0.786, 12: +0.711, 14: +0.684, 16: +0.651, 18: +0.635, 20: +0.616, 22: +0.591, 24: +0.603, 26: +0.632, 28: +0.675, 30: +0.653, 32: +0.676, 34: +0.763.

### 5.3 γ = +0.2

**Start A** (`trace_N1_chiral_A_N65_R6_g+0.2.json`). iters 147, CONVERGENCE: NORM OF PROJECTED GRADIENT <= PGTOL, final E -62.6894, nseg [0, 0, 0], all lines gone at it 30, line 1 gone at it 24, time 200 s.

Geometry:

| it | E | R s2 / s3 | len s2 / s3 | R line 1 | centroid x 1 | z_rms 1 | len 1 | wall gap 1 | open ends | W_z(1) | sep min / mean | Lk₁₂ / Lk₁₃ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 2895.3 | 5.92 / 5.92 | 48.0/48.0 | 6.15 | 6.13 | 4.18 | 48.0 | 3.75 | 0 | 0 | 5.49 / 5.76 | -1.000 / -1.000 |
| 2 | 1952.5 | 5.28 / 5.29 | 43.0/44.0 | 5.95 | 5.94 | 3.63 | 43.0 | 4.75 | 0 | 0 | 4.11 / 4.99 | -1.000 / -1.000 |
| 4 | 1687.5 | 5.19 / 5.19 | 43.0/42.0 | 5.83 | 5.82 | 3.54 | 41.0 | 5.25 | 0 | 0 | 3.92 / 4.87 | -1.000 / -1.000 |
| 6 | 1388.9 | 4.73 / 4.79 | 39.0/39.0 | 5.50 | 5.48 | 3.03 | 38.0 | 5.75 | 0 | 0 | 3.14 / 4.37 | -1.000 / -1.000 |
| 8 | 1168.9 | 4.32 / 4.35 | 36.0/37.0 | 5.46 | 5.41 | 2.67 | 35.0 | 6.25 | 0 | 0 | 2.09 / 3.85 | -1.000 / -1.000 |
| 10 | 1018.7 | 3.98 / 4.13 | 32.0/35.0 | 5.22 | 5.16 | 2.40 | 34.0 | 6.75 | 0 | 0 | 1.73 / 3.61 | -1.000 / -1.000 |
| 12 | 890.0 | 3.67 / 3.79 | 31.0/31.0 | 5.04 | 4.95 | 1.94 | 30.0 | 7.25 | 0 | 0 | 1.27 / 3.03 | -1.000 / -1.000 |
| 14 | 811.3 | 3.55 / 3.69 | 31.0/31.0 | 4.88 | 4.79 | 1.87 | 29.0 | 7.75 | 0 | 0 | 1.06 / 2.85 | -1.000 / -1.000 |
| 16 | 699.1 | 3.21 / 3.40 | 27.0/28.0 | 4.71 | 4.59 | 1.46 | 25.0 | 8.25 | 0 | 0 | 0.35 / 2.46 | -0.750 / -0.875 |
| 18 | 614.4 | 2.94 / 3.11 | 26.0/27.0 | 4.36 | 4.22 | 1.14 | 20.0 | 9.25 | 0 | 0 | 0.35 / 2.12 | -0.125 / -0.250 |
| 20 | 529.7 | 2.63 / 2.94 | 23.0/24.0 | 4.07 | 3.94 | 0.82 | 17.0 | 9.75 | 0 | 0 | 0.50 / 1.97 | -0.000 / -0.125 |
| 22 | 425.8 | 2.06 / 2.43 | 17.0/20.0 | 2.79 | 2.62 | 0.55 | 6.0 | 12.25 | 0 | 0 | 1.06 / 1.46 | -0.000 / -0.000 |
| 24 | 321.2 | 1.69 / 2.08 | 15.0/16.0 | — | — | — | 0.0 | — | — | — | — | 0 (no line 1) |
| 26 | 229.7 | 1.29 / 1.76 | 11.0/13.0 | — | — | — | 0.0 | — | — | — | — | 0 (no line 1) |
| 28 | 145.3 | 0.25 / 1.42 | 2.0/8.0 | — | — | — | 0.0 | — | — | — | — | 0 (no line 1) |
| 30 | 52.1 | — / — | 0.0/0.0 | — | — | — | 0.0 | — | — | — | — | 0 (no lines) |
| 147 (final) | -62.7 | — / — | 0.0/0.0 | — | — | — | 0.0 | — | — | — | — | 0 (no lines) |

Energy split and §4 diagnostics:

| it | E | E_grad | E_mag | E_V | E_χ | E_χ (A·S part) | ⟨\|S\|/\|ψ\|²⟩_w | E_χ near line 1 | virial |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 2895.3 | 1642.5 | 0.00 | 1252.8 | -0.0 | 0.00 | 0.561 | 0.48 | 1.000 |
| 2 | 1952.5 | 1076.6 | 13.01 | 1076.9 | -214.0 | -26.35 | 0.482 | -15.05 | 0.814 |
| 4 | 1687.5 | 926.7 | 15.29 | 986.4 | -241.0 | -31.11 | 0.513 | -16.53 | 0.773 |
| 6 | 1388.9 | 863.9 | 29.57 | 703.0 | -207.6 | -45.06 | 0.512 | -22.07 | 0.740 |
| 8 | 1168.9 | 774.6 | 56.84 | 550.9 | -213.5 | -50.66 | 0.540 | -29.85 | 0.668 |
| 10 | 1018.7 | 705.8 | 66.76 | 498.9 | -252.8 | -48.71 | 0.545 | -32.07 | 0.587 |
| 12 | 890.0 | 702.2 | 79.75 | 401.6 | -293.6 | -40.96 | 0.528 | -34.14 | 0.482 |
| 14 | 811.3 | 634.8 | 79.91 | 379.8 | -283.3 | -38.49 | 0.537 | -33.85 | 0.466 |
| 16 | 699.1 | 544.9 | 84.92 | 309.9 | -240.6 | -30.59 | 0.543 | -32.33 | 0.445 |
| 18 | 614.4 | 483.7 | 88.67 | 264.1 | -222.2 | -22.53 | 0.536 | -30.26 | 0.411 |
| 20 | 529.7 | 442.6 | 86.61 | 231.2 | -230.7 | -17.19 | 0.500 | -27.79 | 0.349 |
| 22 | 425.8 | 374.9 | 81.74 | 184.5 | -215.3 | -7.20 | 0.443 | -18.80 | 0.289 |
| 24 | 321.2 | 281.8 | 73.26 | 137.6 | -171.5 | -2.78 | 0.459 | — | 0.251 |
| 26 | 229.7 | 211.4 | 52.46 | 124.0 | -158.2 | -1.51 | 0.436 | — | 0.225 |
| 28 | 145.3 | 169.2 | 37.79 | 97.0 | -158.7 | 3.36 | 0.360 | — | 0.129 |
| 30 | 52.1 | 106.9 | 20.79 | 75.9 | -151.5 | 8.47 | 0.242 | — | 0.016 |
| 147 (final) | -62.7 | 20.3 | 0.00 | 42.7 | -125.7 | 0.00 | 0.000 | — | -0.258 |

Surface-subtracted virial residual (descriptive; §7): 0: +1.000, 2: +0.913, 4: +0.877, 6: +0.872, 8: +0.815, 10: +0.730, 12: +0.618, 14: +0.609, 16: +0.616, 18: +0.600, 20: +0.538, 22: +0.498, 24: +0.536, 26: +0.575, 28: +0.500.

**Start B** (`trace_N1_chiral_B_N65_R6_g+0.2.json`). iters 157, CONVERGENCE: NORM OF PROJECTED GRADIENT <= PGTOL, final E -62.6894, nseg [0, 0, 0], all lines gone at it 38, line 1 gone at it 38, time 214 s.

Geometry:

| it | E | R s2 / s3 | len s2 / s3 | R line 1 | centroid x 1 | z_rms 1 | len 1 | wall gap 1 | open ends | W_z(1) | sep min / mean | Lk₁₂ / Lk₁₃ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 2442.0 | 5.92 / 5.92 | 48.0/48.0 | 6.31 | 1.99 | 1.36 | 57.0 | 7.75 | 0 | 1 | 1.46 / 1.95 | -1.000 / -1.000 |
| 2 | 1521.3 | 5.33 / 5.35 | 43.0/44.0 | 5.64 | 1.68 | 1.19 | 52.0 | 8.75 | 0 | 1 | 1.06 / 1.75 | -1.000 / -1.000 |
| 4 | 1274.2 | 5.25 / 5.27 | 43.0/43.0 | 5.52 | 1.73 | 1.08 | 50.0 | 8.75 | 0 | 1 | 1.00 / 1.69 | -1.000 / -1.000 |
| 6 | 1068.6 | 5.00 / 5.04 | 40.0/41.0 | 5.30 | 1.64 | 1.01 | 47.0 | 9.25 | 0 | 1 | 0.87 / 1.65 | -1.000 / -1.000 |
| 8 | 868.2 | 4.61 / 4.64 | 38.0/38.0 | 4.89 | 1.42 | 0.80 | 42.0 | 9.75 | 0 | 1 | 0.00 / 1.37 | -0.500 / -0.750 |
| 10 | 792.1 | 4.45 / 4.53 | 36.0/37.0 | 4.76 | 1.27 | 0.79 | 41.0 | 10.25 | 0 | 1 | 0.00 / 1.33 | -0.250 / -0.250 |
| 12 | 733.7 | 4.31 / 4.37 | 35.0/36.0 | 4.57 | 1.23 | 0.73 | 39.0 | 10.25 | 0 | 1 | 0.50 / 1.37 | -0.000 / -0.125 |
| 14 | 709.7 | 4.22 / 4.34 | 35.0/35.0 | 4.48 | 1.15 | 0.70 | 38.0 | 10.25 | 0 | 1 | 0.50 / 1.29 | -0.000 / 0.000 |
| 16 | 673.3 | 3.94 / 4.03 | 32.0/34.0 | 4.18 | 0.94 | 0.53 | 36.0 | 10.75 | 0 | 1 | 0.50 / 1.14 | 0.000 / 0.000 |
| 18 | 642.2 | 3.88 / 4.00 | 31.0/33.0 | 4.06 | 0.80 | 0.53 | 33.0 | 11.25 | 0 | 1 | 0.71 / 1.12 | 0.000 / 0.000 |
| 20 | 609.8 | 3.62 / 3.74 | 30.0/32.0 | 3.73 | 0.52 | 0.54 | 31.0 | 11.75 | 0 | 1 | 0.71 / 1.06 | 0.000 / -0.000 |
| 22 | 573.5 | 3.51 / 3.66 | 29.0/30.0 | 3.56 | 0.48 | 0.53 | 30.0 | 11.75 | 0 | 1 | 0.50 / 1.01 | -0.000 / 0.000 |
| 24 | 539.6 | 3.15 / 3.24 | 27.0/27.0 | 3.06 | 0.21 | 0.41 | 25.0 | 12.75 | 0 | 1 | 0.50 / 0.88 | -0.000 / 0.000 |
| 26 | 481.7 | 2.96 / 3.15 | 24.0/26.0 | 2.96 | 0.19 | 0.41 | 25.0 | 12.75 | 0 | 1 | 0.50 / 0.90 | 0.000 / 0.000 |
| 28 | 422.3 | 2.67 / 2.74 | 23.0/23.0 | 2.53 | 0.18 | 0.33 | 21.0 | 13.25 | 0 | 1 | 0.50 / 0.84 | -0.000 / -0.125 |
| 30 | 368.4 | 2.35 / 2.48 | 19.0/20.0 | 2.21 | 0.34 | 0.33 | 19.0 | 13.25 | 0 | 1 | 0.50 / 0.77 | 0.000 / -0.375 |
| 32 | 294.0 | 1.87 / 1.96 | 15.0/15.0 | 1.65 | 0.27 | 0.25 | 12.0 | 14.25 | 0 | 1 | 0.50 / 0.67 | -0.000 / -0.500 |
| 34 | 224.2 | 1.64 / 1.69 | 13.0/14.0 | 1.42 | 0.54 | 0.24 | 12.0 | 14.25 | 0 | 1 | 0.00 / 0.50 | 0.125 / -0.250 |
| 36 | 130.3 | 0.88 / 1.16 | 6.0/9.0 | 0.65 | 0.50 | 0.25 | 3.0 | 15.25 | 0 | 0 | 0.50 / 0.61 | 0.000 / 0.250 |
| 38 | 71.6 | — / — | 0.0/0.0 | — | — | — | 0.0 | — | — | — | — | 0 (no lines) |
| 157 (final) | -62.7 | — / — | 0.0/0.0 | — | — | — | 0.0 | — | — | — | — | 0 (no lines) |

Energy split and §4 diagnostics:

| it | E | E_grad | E_mag | E_V | E_χ | E_χ (A·S part) | ⟨\|S\|/\|ψ\|²⟩_w | E_χ near line 1 | virial |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 2442.0 | 1687.0 | 0.00 | 755.0 | -0.0 | 0.00 | 0.427 | -0.11 | 1.000 |
| 2 | 1521.3 | 1075.1 | 16.68 | 620.6 | -191.1 | 1.87 | 0.337 | -23.38 | 0.761 |
| 4 | 1274.2 | 929.1 | 19.79 | 535.2 | -209.9 | 3.30 | 0.365 | -26.22 | 0.704 |
| 6 | 1068.6 | 832.5 | 35.88 | 380.9 | -180.7 | 10.92 | 0.392 | -36.63 | 0.665 |
| 8 | 868.2 | 689.3 | 84.07 | 262.2 | -167.3 | 35.09 | 0.454 | -54.51 | 0.558 |
| 10 | 792.1 | 633.5 | 96.04 | 260.1 | -197.6 | 40.95 | 0.467 | -57.11 | 0.484 |
| 12 | 733.7 | 603.2 | 114.69 | 240.3 | -224.5 | 50.71 | 0.491 | -62.34 | 0.403 |
| 14 | 709.7 | 577.1 | 119.86 | 232.9 | -220.2 | 53.07 | 0.502 | -62.83 | 0.390 |
| 16 | 673.3 | 509.1 | 144.27 | 224.1 | -204.1 | 60.61 | 0.536 | -63.07 | 0.363 |
| 18 | 642.2 | 471.3 | 141.76 | 230.8 | -201.7 | 57.62 | 0.539 | -58.87 | 0.362 |
| 20 | 609.8 | 423.5 | 150.64 | 224.9 | -189.3 | 53.28 | 0.533 | -51.21 | 0.350 |
| 22 | 573.5 | 407.5 | 148.23 | 202.8 | -185.0 | 49.36 | 0.530 | -48.63 | 0.324 |
| 24 | 539.6 | 401.7 | 138.39 | 163.4 | -163.9 | 33.62 | 0.489 | -39.14 | 0.313 |
| 26 | 481.7 | 356.5 | 128.62 | 155.8 | -159.2 | 28.61 | 0.513 | -36.27 | 0.297 |
| 28 | 422.3 | 333.7 | 107.59 | 138.5 | -157.5 | 16.67 | 0.492 | -30.27 | 0.279 |
| 30 | 368.4 | 311.7 | 81.46 | 145.7 | -170.5 | 11.52 | 0.452 | -25.11 | 0.279 |
| 32 | 294.0 | 273.6 | 66.02 | 116.8 | -162.4 | 7.36 | 0.404 | -17.73 | 0.230 |
| 34 | 224.2 | 214.2 | 53.64 | 102.9 | -146.6 | 7.74 | 0.408 | -14.19 | 0.203 |
| 36 | 130.3 | 144.3 | 36.58 | 74.4 | -124.9 | 9.23 | 0.347 | -7.89 | 0.124 |
| 38 | 71.6 | 111.3 | 19.85 | 69.2 | -128.7 | 12.15 | 0.135 | — | 0.070 |
| 157 (final) | -62.7 | 20.3 | 0.00 | 42.7 | -125.7 | 0.00 | 0.000 | — | -0.258 |

Surface-subtracted virial residual (descriptive; §7): 0: +1.000, 2: +0.900, 4: +0.854, 6: +0.852, 8: +0.776, 10: +0.681, 12: +0.580, 14: +0.570, 16: +0.548, 18: +0.551, 20: +0.547, 22: +0.529, 24: +0.552, 26: +0.551, 28: +0.556, 30: +0.557, 32: +0.546, 34: +0.594, 36: +0.716.

### 5.4 γ = -0.2

**Start A** (`trace_N1_chiral_A_N65_R6_g-0.2.json`). iters 150, CONVERGENCE: NORM OF PROJECTED GRADIENT <= PGTOL, final E -62.6894, nseg [0, 0, 0], all lines gone at it 30, line 1 gone at it 24, time 196 s.

Geometry:

| it | E | R s2 / s3 | len s2 / s3 | R line 1 | centroid x 1 | z_rms 1 | len 1 | wall gap 1 | open ends | W_z(1) | sep min / mean | Lk₁₂ / Lk₁₃ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 2895.3 | 5.92 / 5.92 | 48.0/48.0 | 6.15 | 6.13 | 4.18 | 48.0 | 3.75 | 0 | 0 | 5.49 / 5.76 | -1.000 / -1.000 |
| 2 | 1952.5 | 5.29 / 5.29 | 44.0/43.0 | 5.95 | 5.94 | 3.63 | 43.0 | 4.75 | 0 | 0 | 4.51 / 4.93 | -1.000 / -1.000 |
| 4 | 1687.5 | 5.17 / 5.18 | 42.0/43.0 | 5.83 | 5.82 | 3.54 | 41.0 | 5.25 | 0 | 0 | 4.17 / 4.93 | -1.000 / -1.000 |
| 6 | 1388.9 | 4.79 / 4.73 | 39.0/39.0 | 5.50 | 5.48 | 3.03 | 38.0 | 5.75 | 0 | 0 | 3.67 / 4.36 | -1.000 / -1.000 |
| 8 | 1169.2 | 4.36 / 4.32 | 36.0/36.0 | 5.46 | 5.42 | 2.67 | 35.0 | 6.25 | 0 | 0 | 2.81 / 3.68 | -1.000 / -1.000 |
| 10 | 1018.1 | 4.07 / 4.01 | 33.0/35.0 | 5.22 | 5.16 | 2.41 | 34.0 | 6.75 | 0 | 0 | 2.32 / 3.48 | -1.000 / -1.000 |
| 12 | 888.6 | 3.79 / 3.66 | 31.0/31.0 | 5.05 | 4.96 | 1.96 | 30.0 | 7.25 | 0 | 0 | 1.84 / 2.90 | -1.000 / -1.000 |
| 14 | 810.0 | 3.71 / 3.55 | 31.0/31.0 | 4.85 | 4.76 | 1.84 | 28.0 | 7.75 | 0 | 0 | 1.62 / 2.69 | -1.000 / -1.000 |
| 16 | 699.0 | 3.38 / 3.22 | 28.0/27.0 | 4.71 | 4.59 | 1.47 | 25.0 | 8.25 | 0 | 0 | 0.87 / 2.13 | -1.000 / -0.375 |
| 18 | 614.7 | 3.11 / 2.88 | 25.0/26.0 | 4.37 | 4.24 | 1.12 | 20.0 | 9.25 | 0 | 0 | 0.00 / 1.75 | -0.625 / -0.000 |
| 20 | 531.1 | 2.94 / 2.63 | 24.0/23.0 | 3.94 | 3.82 | 0.91 | 19.0 | 9.75 | 0 | 0 | 0.00 / 1.51 | -0.375 / -0.000 |
| 22 | 428.7 | 2.39 / 2.11 | 20.0/18.0 | 2.24 | 2.04 | 0.62 | 6.0 | 13.25 | 0 | 0 | 1.06 / 1.55 | -0.000 / 0.000 |
| 24 | 323.5 | 2.10 / 1.79 | 17.0/15.0 | — | — | — | 0.0 | — | — | — | — | 0 (no line 1) |
| 26 | 233.5 | 1.70 / 1.33 | 12.0/11.0 | — | — | — | 0.0 | — | — | — | — | 0 (no line 1) |
| 28 | 147.9 | 1.38 / 0.61 | 6.0/5.0 | — | — | — | 0.0 | — | — | — | — | 0 (no line 1) |
| 30 | 51.4 | — / — | 0.0/0.0 | — | — | — | 0.0 | — | — | — | — | 0 (no lines) |
| 150 (final) | -62.7 | — / — | 0.0/0.0 | — | — | — | 0.0 | — | — | — | — | 0 (no lines) |

Energy split and §4 diagnostics:

| it | E | E_grad | E_mag | E_V | E_χ | E_χ (A·S part) | ⟨\|S\|/\|ψ\|²⟩_w | E_χ near line 1 | virial |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 2895.3 | 1642.5 | 0.00 | 1252.8 | 0.0 | 0.00 | 0.561 | -0.48 | 1.000 |
| 2 | 1952.5 | 1076.6 | 13.01 | 1077.0 | -214.0 | -26.38 | 0.481 | -15.11 | 0.814 |
| 4 | 1687.5 | 926.8 | 15.29 | 986.4 | -241.1 | -31.16 | 0.513 | -16.63 | 0.773 |
| 6 | 1388.9 | 864.2 | 29.57 | 703.1 | -208.0 | -45.25 | 0.510 | -22.78 | 0.739 |
| 8 | 1169.2 | 774.8 | 56.67 | 552.4 | -214.7 | -51.20 | 0.535 | -31.73 | 0.667 |
| 10 | 1018.1 | 706.4 | 66.70 | 499.2 | -254.1 | -49.53 | 0.541 | -34.68 | 0.586 |
| 12 | 888.6 | 703.4 | 79.73 | 400.9 | -295.4 | -42.16 | 0.526 | -37.60 | 0.480 |
| 14 | 810.0 | 636.4 | 79.92 | 378.8 | -285.1 | -39.64 | 0.534 | -36.99 | 0.463 |
| 16 | 699.0 | 547.4 | 84.77 | 309.8 | -243.0 | -31.58 | 0.538 | -34.77 | 0.443 |
| 18 | 614.7 | 486.5 | 88.21 | 264.4 | -224.4 | -23.12 | 0.531 | -32.10 | 0.409 |
| 20 | 531.1 | 445.7 | 86.03 | 232.1 | -232.7 | -17.40 | 0.496 | -30.06 | 0.349 |
| 22 | 428.7 | 377.6 | 80.56 | 186.9 | -216.2 | -6.78 | 0.441 | -20.29 | 0.293 |
| 24 | 323.5 | 283.6 | 72.07 | 141.0 | -173.2 | -2.62 | 0.460 | — | 0.256 |
| 26 | 233.5 | 212.6 | 52.63 | 124.1 | -155.8 | -0.66 | 0.429 | — | 0.232 |
| 28 | 147.9 | 170.2 | 37.10 | 97.7 | -157.0 | 4.11 | 0.336 | — | 0.138 |
| 30 | 51.4 | 103.9 | 22.37 | 74.6 | -149.4 | 9.06 | 0.241 | — | 0.010 |
| 150 (final) | -62.7 | 20.3 | 0.00 | 42.7 | -125.7 | 0.00 | 0.000 | — | -0.258 |

Surface-subtracted virial residual (descriptive; §7): 0: +1.000, 2: +0.913, 4: +0.876, 6: +0.871, 8: +0.814, 10: +0.728, 12: +0.615, 14: +0.606, 16: +0.612, 18: +0.597, 20: +0.536, 22: +0.502, 24: +0.539, 26: +0.589, 28: +0.519.

**Start B** (`trace_N1_chiral_B_N65_R6_g-0.2.json`). iters 163, CONVERGENCE: NORM OF PROJECTED GRADIENT <= PGTOL, final E -62.6894, nseg [0, 0, 0], all lines gone at it 40, line 1 gone at it 38, time 216 s.

Geometry:

| it | E | R s2 / s3 | len s2 / s3 | R line 1 | centroid x 1 | z_rms 1 | len 1 | wall gap 1 | open ends | W_z(1) | sep min / mean | Lk₁₂ / Lk₁₃ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 2442.0 | 5.92 / 5.92 | 48.0/48.0 | 6.31 | 1.99 | 1.36 | 57.0 | 7.75 | 0 | 1 | 1.46 / 1.95 | -1.000 / -1.000 |
| 2 | 1521.3 | 5.34 / 5.31 | 44.0/43.0 | 5.64 | 1.68 | 1.19 | 52.0 | 8.75 | 0 | 1 | 1.00 / 1.52 | -1.000 / -1.000 |
| 4 | 1274.2 | 5.30 / 5.24 | 43.0/43.0 | 5.52 | 1.72 | 1.09 | 50.0 | 8.75 | 0 | 1 | 1.00 / 1.48 | -1.000 / -1.000 |
| 6 | 1068.4 | 5.03 / 5.00 | 40.0/41.0 | 5.31 | 1.65 | 1.01 | 47.0 | 9.25 | 0 | 1 | 0.61 / 1.39 | -1.000 / -1.000 |
| 8 | 867.9 | 4.68 / 4.60 | 39.0/37.0 | 4.88 | 1.43 | 0.82 | 43.0 | 9.75 | 0 | 1 | 0.00 / 0.97 | -0.500 / -1.000 |
| 10 | 791.8 | 4.53 / 4.46 | 37.0/37.0 | 4.74 | 1.29 | 0.79 | 41.0 | 10.25 | 0 | 1 | 0.00 / 1.03 | -0.000 / -0.500 |
| 12 | 733.6 | 4.37 / 4.30 | 36.0/35.0 | 4.57 | 1.23 | 0.73 | 39.0 | 10.25 | 0 | 1 | 0.50 / 1.05 | 0.000 / -0.375 |
| 14 | 709.5 | 4.33 / 4.23 | 35.0/35.0 | 4.47 | 1.17 | 0.70 | 38.0 | 10.25 | 0 | 1 | 0.50 / 1.02 | 0.000 / -0.375 |
| 16 | 673.3 | 4.07 / 3.94 | 34.0/33.0 | 4.17 | 0.96 | 0.56 | 35.0 | 10.75 | 0 | 1 | 0.50 / 0.99 | 0.000 / -0.000 |
| 18 | 642.2 | 4.00 / 3.89 | 32.0/32.0 | 4.05 | 0.79 | 0.55 | 34.0 | 11.25 | 0 | 1 | 0.50 / 0.99 | -0.000 / 0.000 |
| 20 | 611.1 | 3.76 / 3.64 | 31.0/31.0 | 3.72 | 0.51 | 0.55 | 30.0 | 11.75 | 0 | 1 | 0.87 / 1.13 | 0.000 / 0.000 |
| 22 | 575.1 | 3.68 / 3.54 | 31.0/30.0 | 3.62 | 0.50 | 0.55 | 30.0 | 11.75 | 0 | 1 | 0.87 / 1.14 | 0.000 / 0.000 |
| 24 | 541.6 | 3.25 / 3.18 | 26.0/28.0 | 3.09 | 0.36 | 0.42 | 26.0 | 12.25 | 0 | 1 | 0.71 / 1.09 | 0.000 / 0.000 |
| 26 | 482.9 | 3.11 / 3.09 | 26.0/27.0 | 2.96 | 0.25 | 0.40 | 25.0 | 12.75 | 0 | 1 | 0.50 / 1.02 | 0.000 / -0.250 |
| 28 | 428.4 | 2.77 / 2.75 | 22.0/23.0 | 2.58 | 0.21 | 0.36 | 21.0 | 13.25 | 0 | 1 | 0.50 / 1.01 | 0.000 / -0.125 |
| 30 | 364.4 | 2.42 / 2.49 | 19.0/21.0 | 2.20 | 0.21 | 0.30 | 17.0 | 13.75 | 0 | 1 | 0.61 / 0.89 | 0.000 / -0.250 |
| 32 | 296.9 | 2.03 / 2.08 | 15.0/17.0 | 1.77 | 0.45 | 0.25 | 14.0 | 13.75 | 0 | 1 | 0.50 / 0.76 | 0.000 / -0.250 |
| 34 | 218.7 | 1.49 / 1.61 | 10.0/13.0 | 1.33 | 0.50 | 0.24 | 11.0 | 14.25 | 0 | 1 | 0.00 / 0.59 | 0.250 / -0.125 |
| 36 | 140.2 | 1.10 / 1.10 | 6.0/8.0 | 0.62 | 0.25 | 0.25 | 4.0 | 15.25 | 0 | 1 | 0.50 / 0.67 | 0.000 / -0.250 |
| 38 | 56.0 | — / 0.65 | 0.0/3.0 | — | — | — | 0.0 | — | — | — | — | 0.000 / 0.000 |
| 40 | 1.0 | — / — | 0.0/0.0 | — | — | — | 0.0 | — | — | — | — | 0 (no lines) |
| 163 (final) | -62.7 | — / — | 0.0/0.0 | — | — | — | 0.0 | — | — | — | — | 0 (no lines) |

Energy split and §4 diagnostics:

| it | E | E_grad | E_mag | E_V | E_χ | E_χ (A·S part) | ⟨\|S\|/\|ψ\|²⟩_w | E_χ near line 1 | virial |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 2442.0 | 1687.0 | 0.00 | 755.0 | 0.0 | 0.00 | 0.427 | 0.11 | 1.000 |
| 2 | 1521.3 | 1075.1 | 16.68 | 620.6 | -191.0 | 1.88 | 0.338 | -23.46 | 0.761 |
| 4 | 1274.2 | 929.1 | 19.79 | 535.2 | -209.9 | 3.32 | 0.367 | -26.33 | 0.704 |
| 6 | 1068.4 | 832.3 | 35.90 | 380.8 | -180.6 | 10.98 | 0.394 | -36.58 | 0.665 |
| 8 | 867.9 | 688.9 | 84.14 | 261.9 | -167.0 | 35.37 | 0.464 | -54.41 | 0.558 |
| 10 | 791.8 | 633.1 | 96.15 | 259.8 | -197.3 | 41.29 | 0.483 | -56.82 | 0.484 |
| 12 | 733.6 | 602.8 | 114.70 | 240.3 | -224.3 | 51.05 | 0.509 | -62.27 | 0.403 |
| 14 | 709.5 | 576.8 | 119.86 | 233.0 | -220.2 | 53.39 | 0.521 | -62.82 | 0.390 |
| 16 | 673.3 | 509.3 | 144.27 | 224.4 | -204.6 | 60.87 | 0.551 | -63.37 | 0.362 |
| 18 | 642.2 | 471.9 | 141.54 | 231.1 | -202.3 | 57.82 | 0.552 | -59.64 | 0.362 |
| 20 | 611.1 | 425.3 | 150.15 | 225.6 | -189.9 | 53.35 | 0.530 | -51.79 | 0.351 |
| 22 | 575.1 | 409.1 | 148.06 | 204.3 | -186.4 | 50.02 | 0.526 | -49.59 | 0.325 |
| 24 | 541.6 | 404.7 | 137.64 | 165.0 | -165.8 | 35.00 | 0.471 | -39.90 | 0.315 |
| 26 | 482.9 | 357.9 | 127.95 | 156.9 | -159.9 | 29.47 | 0.490 | -36.31 | 0.298 |
| 28 | 428.4 | 335.3 | 111.13 | 137.4 | -155.4 | 18.01 | 0.471 | -30.31 | 0.278 |
| 30 | 364.4 | 307.6 | 82.92 | 140.7 | -166.8 | 11.59 | 0.432 | -24.10 | 0.273 |
| 32 | 296.9 | 271.4 | 65.65 | 121.9 | -162.0 | 8.46 | 0.393 | -17.60 | 0.241 |
| 34 | 218.7 | 209.7 | 51.55 | 101.5 | -144.0 | 8.34 | 0.386 | -12.89 | 0.204 |
| 36 | 140.2 | 146.8 | 33.71 | 85.7 | -126.0 | 10.38 | 0.340 | -7.86 | 0.171 |
| 38 | 56.0 | 97.8 | 25.37 | 61.5 | -128.6 | 10.70 | 0.284 | — | -0.001 |
| 40 | 1.0 | 70.6 | 11.55 | 50.5 | -131.5 | 11.45 | 0.119 | — | -0.106 |
| 163 (final) | -62.7 | 20.3 | 0.00 | 42.7 | -125.7 | -0.00 | 0.000 | — | -0.258 |

Surface-subtracted virial residual (descriptive; §7): 0: +1.000, 2: +0.900, 4: +0.854, 6: +0.852, 8: +0.776, 10: +0.682, 12: +0.581, 14: +0.570, 16: +0.548, 18: +0.550, 20: +0.548, 22: +0.529, 24: +0.551, 26: +0.552, 28: +0.557, 30: +0.558, 32: +0.559, 34: +0.611, 36: +0.763, 38: +0.621.

### 5.5 γ = +0.3

**Start A** (`trace_N1_chiral_A_N65_R6_g+0.3.json`). iters 209, CONVERGENCE: NORM OF PROJECTED GRADIENT <= PGTOL, final E -141.4629, nseg [0, 0, 0], all lines gone at it 32, line 1 gone at it 28, time 279 s.

Geometry:

| it | E | R s2 / s3 | len s2 / s3 | R line 1 | centroid x 1 | z_rms 1 | len 1 | wall gap 1 | open ends | W_z(1) | sep min / mean | Lk₁₂ / Lk₁₃ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 2895.3 | 5.92 / 5.92 | 48.0/48.0 | 6.15 | 6.13 | 4.18 | 48.0 | 3.75 | 0 | 0 | 5.49 / 5.76 | -1.000 / -1.000 |
| 2 | 1793.4 | 5.31 / 5.31 | 44.0/44.0 | 5.96 | 5.95 | 3.68 | 43.0 | 4.75 | 0 | 0 | 4.11 / 5.07 | -1.000 / -1.000 |
| 4 | 1561.4 | 5.19 / 5.19 | 43.0/43.0 | 5.83 | 5.82 | 3.56 | 41.0 | 5.25 | 0 | 0 | 3.79 / 4.83 | -1.000 / -1.000 |
| 6 | 1279.4 | 4.70 / 4.74 | 39.0/40.0 | 5.48 | 5.45 | 2.95 | 38.0 | 5.75 | 0 | 0 | 2.62 / 4.32 | -1.000 / -1.000 |
| 8 | 1052.9 | 4.45 / 4.54 | 36.0/39.0 | 5.30 | 5.25 | 2.80 | 37.0 | 6.25 | 0 | 0 | 2.09 / 3.96 | -1.000 / -1.000 |
| 10 | 890.8 | 4.16 / 4.23 | 34.0/35.0 | 5.22 | 5.14 | 2.51 | 34.0 | 6.75 | 0 | 0 | 1.70 / 3.72 | -1.000 / -1.000 |
| 12 | 796.0 | 3.91 / 4.12 | 33.0/36.0 | 5.09 | 4.99 | 2.29 | 32.0 | 7.25 | 0 | 0 | 1.27 / 3.35 | -1.000 / -1.000 |
| 14 | 713.0 | 3.73 / 3.95 | 32.0/34.0 | 4.83 | 4.68 | 1.96 | 30.0 | 7.75 | 0 | 0 | 0.61 / 3.08 | -1.000 / -1.000 |
| 16 | 613.7 | 3.38 / 3.69 | 29.0/32.0 | 4.62 | 4.44 | 1.60 | 27.0 | 8.25 | 0 | 0 | 0.35 / 2.68 | -0.750 / -0.625 |
| 18 | 527.2 | 3.03 / 3.40 | 26.0/29.0 | 4.22 | 3.99 | 1.23 | 25.0 | 8.75 | 0 | 0 | 0.35 / 2.46 | -0.000 / 0.000 |
| 20 | 438.9 | 2.69 / 3.17 | 23.0/27.0 | 3.75 | 3.45 | 1.01 | 21.0 | 9.75 | 0 | 0 | 0.87 / 2.18 | 0.000 / -0.000 |
| 22 | 357.6 | 2.31 / 2.84 | 20.0/24.0 | 3.13 | 2.83 | 0.78 | 16.0 | 10.75 | 0 | 0 | 1.00 / 2.09 | 0.000 / 0.000 |
| 24 | 269.5 | 1.81 / 2.46 | 15.0/20.0 | 2.08 | 1.73 | 0.80 | 11.0 | 12.75 | 0 | 0 | 1.46 / 1.77 | 0.000 / -0.000 |
| 26 | 198.7 | 1.54 / 2.32 | 14.0/18.0 | 1.41 | 1.05 | 0.75 | 5.0 | 14.25 | 0 | 0 | 1.50 / 1.56 | -0.000 / -0.000 |
| 28 | 116.1 | 0.79 / 1.87 | 7.0/11.0 | — | — | — | 0.0 | — | — | — | — | 0 (no line 1) |
| 30 | 35.5 | — / 1.58 | 0.0/6.0 | — | — | — | 0.0 | — | — | — | — | 0.000 / 0.000 |
| 32 | -33.9 | — / — | 0.0/0.0 | — | — | — | 0.0 | — | — | — | — | 0 (no lines) |
| 209 (final) | -141.5 | — / — | 0.0/0.0 | — | — | — | 0.0 | — | — | — | — | 0 (no lines) |

Energy split and §4 diagnostics:

| it | E | E_grad | E_mag | E_V | E_χ | E_χ (A·S part) | ⟨\|S\|/\|ψ\|²⟩_w | E_χ near line 1 | virial |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 2895.3 | 1642.5 | 0.00 | 1252.8 | -0.0 | 0.00 | 0.561 | 0.72 | 1.000 |
| 2 | 1793.4 | 1136.0 | 11.42 | 1164.5 | -518.5 | -52.97 | 0.482 | -31.22 | 0.631 |
| 4 | 1561.4 | 1001.7 | 15.05 | 1080.7 | -536.0 | -67.42 | 0.503 | -36.09 | 0.592 |
| 6 | 1279.4 | 929.1 | 36.82 | 757.3 | -443.8 | -108.28 | 0.537 | -52.31 | 0.552 |
| 8 | 1052.9 | 818.2 | 48.27 | 691.9 | -505.5 | -115.97 | 0.558 | -61.64 | 0.464 |
| 10 | 890.8 | 840.8 | 62.92 | 601.7 | -614.6 | -118.58 | 0.544 | -69.92 | 0.344 |
| 12 | 796.0 | 828.5 | 69.40 | 534.9 | -636.9 | -115.18 | 0.540 | -74.33 | 0.289 |
| 14 | 713.0 | 755.2 | 72.72 | 481.0 | -596.0 | -109.82 | 0.549 | -74.17 | 0.270 |
| 16 | 613.7 | 677.6 | 78.50 | 441.0 | -583.5 | -98.83 | 0.550 | -73.76 | 0.233 |
| 18 | 527.2 | 641.5 | 81.50 | 412.9 | -608.7 | -88.63 | 0.514 | -70.40 | 0.183 |
| 20 | 438.9 | 564.0 | 80.96 | 348.2 | -554.3 | -76.85 | 0.496 | -68.03 | 0.150 |
| 22 | 357.6 | 484.3 | 74.85 | 279.4 | -481.0 | -66.16 | 0.490 | -60.97 | 0.121 |
| 24 | 269.5 | 400.4 | 63.19 | 256.5 | -450.5 | -52.46 | 0.467 | -48.40 | 0.096 |
| 26 | 198.7 | 354.9 | 54.78 | 242.5 | -453.5 | -44.07 | 0.440 | -36.90 | 0.059 |
| 28 | 116.1 | 283.0 | 36.90 | 216.8 | -420.6 | -30.24 | 0.392 | — | 0.030 |
| 30 | 35.5 | 199.4 | 26.35 | 182.6 | -372.9 | -17.22 | 0.380 | — | -0.016 |
| 32 | -33.9 | 152.5 | 15.21 | 166.1 | -367.7 | -8.56 | 0.276 | — | -0.071 |
| 209 (final) | -141.5 | 46.1 | 0.00 | 96.8 | -284.4 | 0.01 | 0.000 | — | -0.257 |

Surface-subtracted virial residual (descriptive; §7): 0: +1.000, 2: +0.799, 4: +0.766, 6: +0.779, 8: +0.678, 10: +0.523, 12: +0.461, 14: +0.456, 16: +0.422, 18: +0.358, 20: +0.344, 22: +0.356, 24: +0.356, 26: +0.310, 28: +0.317, 30: +0.338.

**Start B** (`trace_N1_chiral_B_N65_R6_g+0.3.json`). iters 223, CONVERGENCE: NORM OF PROJECTED GRADIENT <= PGTOL, final E -141.4629, nseg [0, 0, 0], all lines gone at it 40, line 1 gone at it 38, time 283 s.

Geometry:

| it | E | R s2 / s3 | len s2 / s3 | R line 1 | centroid x 1 | z_rms 1 | len 1 | wall gap 1 | open ends | W_z(1) | sep min / mean | Lk₁₂ / Lk₁₃ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 2442.0 | 5.92 / 5.92 | 48.0/48.0 | 6.31 | 1.99 | 1.36 | 57.0 | 7.75 | 0 | 1 | 1.46 / 1.95 | -1.000 / -1.000 |
| 2 | 1372.8 | 5.36 / 5.37 | 44.0/44.0 | 5.68 | 1.71 | 1.20 | 52.0 | 8.75 | 0 | 1 | 1.06 / 1.81 | -1.000 / -1.000 |
| 4 | 1167.5 | 5.27 / 5.28 | 42.0/43.0 | 5.58 | 1.71 | 1.09 | 50.0 | 8.75 | 0 | 1 | 1.00 / 1.75 | -1.000 / -1.000 |
| 6 | 943.4 | 4.97 / 5.02 | 41.0/41.0 | 5.22 | 1.45 | 1.00 | 48.0 | 9.25 | 0 | 1 | 0.35 / 1.58 | -0.875 / -0.875 |
| 8 | 787.1 | 4.77 / 4.82 | 39.0/39.0 | 5.02 | 1.43 | 0.95 | 44.0 | 9.75 | 0 | 1 | 0.00 / 1.58 | -0.500 / -0.500 |
| 10 | 685.7 | 4.62 / 4.66 | 38.0/38.0 | 4.91 | 1.42 | 0.81 | 42.0 | 9.75 | 0 | 1 | 0.00 / 1.55 | -0.250 / -0.125 |
| 12 | 636.1 | 4.45 / 4.53 | 36.0/37.0 | 4.75 | 1.24 | 0.79 | 40.0 | 10.25 | 0 | 1 | 0.50 / 1.57 | -0.000 / -0.000 |
| 14 | 600.6 | 4.34 / 4.46 | 37.0/35.0 | 4.62 | 1.17 | 0.78 | 39.0 | 10.25 | 0 | 1 | 0.50 / 1.54 | -0.000 / -0.000 |
| 16 | 573.7 | 4.24 / 4.32 | 35.0/36.0 | 4.41 | 0.99 | 0.79 | 37.0 | 10.75 | 0 | 1 | 0.87 / 1.56 | -0.000 / 0.000 |
| 18 | 542.2 | 4.00 / 4.16 | 35.0/35.0 | 4.15 | 0.75 | 0.77 | 34.0 | 11.25 | 0 | 1 | 1.00 / 1.54 | -0.000 / -0.000 |
| 20 | 515.7 | 3.85 / 4.09 | 32.0/34.0 | 4.01 | 0.71 | 0.75 | 33.0 | 11.25 | 0 | 1 | 1.00 / 1.50 | -0.000 / 0.000 |
| 22 | 477.3 | 3.52 / 3.73 | 31.0/31.0 | 3.62 | 0.48 | 0.62 | 29.0 | 11.75 | 0 | 1 | 1.00 / 1.36 | -0.000 / 0.000 |
| 24 | 434.6 | 3.31 / 3.54 | 28.0/29.0 | 3.35 | 0.34 | 0.62 | 28.0 | 12.25 | 0 | 1 | 1.00 / 1.33 | -0.000 / 0.000 |
| 26 | 384.6 | 3.01 / 3.21 | 27.0/27.0 | 2.96 | 0.29 | 0.60 | 24.0 | 12.75 | 0 | 1 | 1.00 / 1.23 | -0.000 / 0.000 |
| 28 | 339.1 | 2.71 / 2.95 | 22.0/25.0 | 2.68 | 0.41 | 0.59 | 22.0 | 12.75 | 0 | 1 | 1.00 / 1.16 | -0.000 / 0.000 |
| 30 | 289.6 | 2.46 / 2.74 | 22.0/23.0 | 2.45 | 0.30 | 0.58 | 20.0 | 13.25 | 0 | 1 | 1.00 / 1.19 | -0.000 / 0.000 |
| 32 | 218.8 | 1.96 / 2.22 | 16.0/17.0 | 1.85 | 0.30 | 0.54 | 16.0 | 13.75 | 0 | 1 | 1.00 / 1.14 | -0.000 / 0.000 |
| 34 | 142.9 | 1.45 / 1.78 | 13.0/14.0 | 1.41 | 0.45 | 0.49 | 11.0 | 14.25 | 0 | 1 | 0.94 / 1.07 | 0.000 / 0.000 |
| 36 | 57.2 | 0.88 / 1.37 | 7.0/11.0 | 0.73 | 0.42 | 0.47 | 6.0 | 14.75 | 0 | 1 | 1.00 / 1.07 | 0.000 / 0.125 |
| 38 | -24.4 | — / 1.13 | 0.0/2.0 | — | — | — | 0.0 | — | — | — | — | 0.000 / 0.000 |
| 40 | -84.4 | — / — | 0.0/0.0 | — | — | — | 0.0 | — | — | — | — | 0 (no lines) |
| 223 (final) | -141.5 | — / — | 0.0/0.0 | — | — | — | 0.0 | — | — | — | — | 0 (no lines) |

Energy split and §4 diagnostics:

| it | E | E_grad | E_mag | E_V | E_χ | E_χ (A·S part) | ⟨\|S\|/\|ψ\|²⟩_w | E_χ near line 1 | virial |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 2442.0 | 1687.0 | 0.00 | 755.0 | -0.0 | 0.00 | 0.427 | -0.17 | 1.000 |
| 2 | 1372.8 | 1137.9 | 13.59 | 691.4 | -470.0 | 2.24 | 0.338 | -48.78 | 0.542 |
| 4 | 1167.5 | 1000.8 | 18.42 | 618.9 | -470.7 | 6.17 | 0.363 | -57.35 | 0.497 |
| 6 | 943.4 | 847.2 | 45.98 | 404.7 | -354.4 | 34.32 | 0.442 | -92.86 | 0.464 |
| 8 | 787.1 | 745.9 | 64.02 | 378.0 | -400.9 | 53.76 | 0.478 | -107.49 | 0.369 |
| 10 | 685.7 | 732.7 | 81.67 | 347.9 | -476.7 | 74.73 | 0.498 | -121.93 | 0.264 |
| 12 | 636.1 | 719.2 | 97.46 | 319.7 | -500.2 | 94.02 | 0.525 | -133.56 | 0.209 |
| 14 | 600.6 | 665.8 | 105.91 | 310.5 | -481.7 | 102.63 | 0.554 | -135.18 | 0.198 |
| 16 | 573.7 | 613.5 | 111.09 | 319.6 | -470.5 | 105.32 | 0.570 | -131.12 | 0.198 |
| 18 | 542.2 | 569.6 | 123.42 | 327.8 | -478.6 | 111.27 | 0.573 | -124.69 | 0.179 |
| 20 | 515.7 | 547.4 | 125.03 | 308.1 | -464.8 | 110.87 | 0.571 | -121.35 | 0.165 |
| 22 | 477.3 | 496.4 | 122.00 | 286.1 | -427.2 | 93.33 | 0.565 | -104.82 | 0.162 |
| 24 | 434.6 | 468.0 | 107.62 | 272.5 | -413.5 | 72.69 | 0.550 | -93.41 | 0.158 |
| 26 | 384.6 | 454.6 | 90.85 | 237.9 | -398.8 | 50.95 | 0.525 | -82.85 | 0.136 |
| 28 | 339.1 | 427.4 | 88.38 | 199.4 | -376.1 | 45.38 | 0.541 | -78.23 | 0.099 |
| 30 | 289.6 | 390.8 | 69.69 | 202.1 | -373.0 | 40.99 | 0.522 | -68.32 | 0.100 |
| 32 | 218.8 | 346.7 | 53.37 | 201.0 | -382.3 | 34.50 | 0.471 | -51.84 | 0.075 |
| 34 | 142.9 | 292.5 | 42.65 | 183.1 | -375.4 | 33.30 | 0.443 | -37.39 | 0.030 |
| 36 | 57.2 | 212.3 | 32.41 | 152.8 | -340.4 | 35.73 | 0.386 | -23.96 | -0.031 |
| 38 | -24.4 | 135.7 | 21.97 | 113.2 | -295.3 | 38.69 | 0.305 | — | -0.126 |
| 40 | -84.4 | 93.3 | 12.02 | 101.5 | -291.2 | 40.55 | 0.190 | — | -0.198 |
| 223 (final) | -141.5 | 46.1 | 0.00 | 96.8 | -284.4 | -0.01 | 0.000 | — | -0.257 |

Surface-subtracted virial residual (descriptive; §7): 0: +1.000, 2: +0.764, 4: +0.731, 6: +0.805, 8: +0.677, 10: +0.511, 12: +0.434, 14: +0.432, 16: +0.438, 18: +0.408, 20: +0.401, 22: +0.428, 24: +0.443, 26: +0.445, 28: +0.434, 30: +0.456, 32: +0.422, 34: +0.385, 36: +0.397, 38: +0.521.

### 5.6 γ = -0.3

**Start A** (`trace_N1_chiral_A_N65_R6_g-0.3.json`). iters 227, CONVERGENCE: NORM OF PROJECTED GRADIENT <= PGTOL, final E -141.4629, nseg [0, 0, 0], all lines gone at it 32, line 1 gone at it 28, time 303 s.

Geometry:

| it | E | R s2 / s3 | len s2 / s3 | R line 1 | centroid x 1 | z_rms 1 | len 1 | wall gap 1 | open ends | W_z(1) | sep min / mean | Lk₁₂ / Lk₁₃ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 2895.3 | 5.92 / 5.92 | 48.0/48.0 | 6.15 | 6.13 | 4.18 | 48.0 | 3.75 | 0 | 0 | 5.49 / 5.76 | -1.000 / -1.000 |
| 2 | 1793.4 | 5.33 / 5.30 | 44.0/44.0 | 5.96 | 5.95 | 3.68 | 43.0 | 4.75 | 0 | 0 | 4.54 / 5.03 | -1.000 / -1.000 |
| 4 | 1561.3 | 5.21 / 5.16 | 43.0/43.0 | 5.83 | 5.82 | 3.56 | 41.0 | 5.25 | 0 | 0 | 4.23 / 4.81 | -1.000 / -1.000 |
| 6 | 1279.7 | 4.71 / 4.69 | 40.0/40.0 | 5.48 | 5.45 | 2.95 | 38.0 | 5.75 | 0 | 0 | 3.37 / 4.08 | -1.000 / -1.000 |
| 8 | 1053.7 | 4.51 / 4.44 | 36.0/37.0 | 5.28 | 5.24 | 2.81 | 37.0 | 6.25 | 0 | 0 | 3.26 / 3.93 | -1.000 / -1.000 |
| 10 | 889.0 | 4.24 / 4.14 | 34.0/36.0 | 5.22 | 5.14 | 2.52 | 34.0 | 6.75 | 0 | 0 | 2.55 / 3.47 | -1.000 / -1.000 |
| 12 | 793.8 | 4.08 / 3.90 | 34.0/33.0 | 5.07 | 4.97 | 2.21 | 31.0 | 7.25 | 0 | 0 | 2.32 / 3.09 | -1.000 / -1.000 |
| 14 | 712.2 | 3.91 / 3.75 | 32.0/32.0 | 4.82 | 4.69 | 2.05 | 31.0 | 7.75 | 0 | 0 | 1.66 / 2.75 | -1.000 / -0.875 |
| 16 | 616.2 | 3.60 / 3.40 | 30.0/29.0 | 4.59 | 4.42 | 1.67 | 27.0 | 8.25 | 0 | 0 | 0.61 / 2.33 | -1.000 / -0.125 |
| 18 | 536.0 | 3.39 / 3.15 | 27.0/28.0 | 4.20 | 4.00 | 1.36 | 25.0 | 8.75 | 0 | 0 | 0.35 / 1.96 | -0.750 / -0.000 |
| 20 | 458.4 | 3.13 / 2.80 | 27.0/25.0 | 3.79 | 3.50 | 1.07 | 21.0 | 9.75 | 0 | 0 | 0.00 / 1.62 | -0.375 / -0.000 |
| 22 | 379.9 | 2.97 / 2.53 | 24.0/22.0 | 3.32 | 3.04 | 1.00 | 19.0 | 10.25 | 0 | 0 | 0.61 / 1.55 | -0.000 / -0.000 |
| 24 | 282.3 | 2.48 / 2.03 | 20.0/17.0 | 2.02 | 1.70 | 1.01 | 11.0 | 12.75 | 0 | 0 | 1.46 / 1.68 | -0.000 / 0.000 |
| 26 | 218.2 | 2.23 / 1.77 | 16.0/15.0 | 1.56 | 1.25 | 1.03 | 7.0 | 13.75 | 0 | 0 | 1.54 / 1.80 | 0.000 / -0.000 |
| 28 | 131.9 | 1.78 / 1.26 | 11.0/11.0 | — | — | — | 0.0 | — | — | — | — | 0 (no line 1) |
| 30 | 57.7 | — / 0.61 | 0.0/5.0 | — | — | — | 0.0 | — | — | — | — | 0.000 / 0.000 |
| 32 | -23.7 | — / — | 0.0/0.0 | — | — | — | 0.0 | — | — | — | — | 0 (no lines) |
| 227 (final) | -141.5 | — / — | 0.0/0.0 | — | — | — | 0.0 | — | — | — | — | 0 (no lines) |

Energy split and §4 diagnostics:

| it | E | E_grad | E_mag | E_V | E_χ | E_χ (A·S part) | ⟨\|S\|/\|ψ\|²⟩_w | E_χ near line 1 | virial |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 2895.3 | 1642.5 | 0.00 | 1252.8 | 0.0 | 0.00 | 0.561 | -0.72 | 1.000 |
| 2 | 1793.4 | 1136.0 | 11.42 | 1164.5 | -518.6 | -53.03 | 0.482 | -31.37 | 0.631 |
| 4 | 1561.3 | 1001.7 | 15.04 | 1080.8 | -536.2 | -67.55 | 0.502 | -36.44 | 0.592 |
| 6 | 1279.7 | 929.9 | 36.80 | 758.5 | -445.5 | -109.05 | 0.531 | -55.48 | 0.551 |
| 8 | 1053.7 | 818.9 | 47.83 | 694.2 | -507.4 | -117.04 | 0.552 | -65.61 | 0.464 |
| 10 | 889.0 | 842.3 | 62.66 | 602.7 | -618.6 | -120.77 | 0.538 | -77.79 | 0.342 |
| 12 | 793.8 | 832.0 | 69.33 | 534.6 | -642.2 | -117.99 | 0.535 | -83.13 | 0.286 |
| 14 | 712.2 | 760.1 | 72.31 | 481.4 | -601.6 | -113.11 | 0.545 | -84.29 | 0.267 |
| 16 | 616.2 | 685.9 | 77.38 | 441.5 | -588.7 | -102.35 | 0.543 | -81.42 | 0.231 |
| 18 | 536.0 | 652.1 | 79.38 | 420.5 | -615.9 | -92.87 | 0.514 | -79.88 | 0.187 |
| 20 | 458.4 | 588.2 | 78.40 | 377.1 | -585.3 | -81.79 | 0.495 | -70.99 | 0.159 |
| 22 | 379.9 | 506.3 | 72.19 | 311.0 | -509.7 | -72.06 | 0.492 | -64.98 | 0.137 |
| 24 | 282.3 | 411.1 | 64.26 | 244.3 | -437.3 | -52.98 | 0.484 | -50.64 | 0.098 |
| 26 | 218.2 | 373.9 | 54.47 | 243.1 | -453.3 | -44.21 | 0.443 | -39.46 | 0.069 |
| 28 | 131.9 | 299.5 | 39.59 | 231.3 | -438.5 | -30.68 | 0.395 | — | 0.040 |
| 30 | 57.7 | 219.0 | 26.46 | 193.9 | -381.7 | -13.42 | 0.340 | — | 0.007 |
| 32 | -23.7 | 158.0 | 16.54 | 169.9 | -368.1 | -8.75 | 0.273 | — | -0.060 |
| 227 (final) | -141.5 | 46.1 | 0.00 | 96.8 | -284.4 | 0.00 | 0.000 | — | -0.257 |

Surface-subtracted virial residual (descriptive; §7): 0: +1.000, 2: +0.799, 4: +0.766, 6: +0.778, 8: +0.677, 10: +0.520, 12: +0.456, 14: +0.451, 16: +0.419, 18: +0.360, 20: +0.341, 22: +0.357, 24: +0.371, 26: +0.323, 28: +0.308, 30: +0.355.

**Start B** (`trace_N1_chiral_B_N65_R6_g-0.3.json`). iters 218, CONVERGENCE: NORM OF PROJECTED GRADIENT <= PGTOL, final E -141.4629, nseg [0, 0, 0], all lines gone at it 40, line 1 gone at it 38, time 274 s.

Geometry:

| it | E | R s2 / s3 | len s2 / s3 | R line 1 | centroid x 1 | z_rms 1 | len 1 | wall gap 1 | open ends | W_z(1) | sep min / mean | Lk₁₂ / Lk₁₃ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 2442.0 | 5.92 / 5.92 | 48.0/48.0 | 6.31 | 1.99 | 1.36 | 57.0 | 7.75 | 0 | 1 | 1.46 / 1.95 | -1.000 / -1.000 |
| 2 | 1372.8 | 5.38 / 5.35 | 44.0/45.0 | 5.67 | 1.70 | 1.21 | 52.0 | 8.75 | 0 | 1 | 1.00 / 1.57 | -1.000 / -1.000 |
| 4 | 1167.4 | 5.32 / 5.26 | 42.0/43.0 | 5.57 | 1.72 | 1.08 | 50.0 | 8.75 | 0 | 1 | 0.94 / 1.51 | -1.000 / -1.000 |
| 6 | 943.0 | 5.02 / 4.96 | 42.0/41.0 | 5.22 | 1.45 | 1.01 | 48.0 | 9.25 | 0 | 1 | 0.35 / 1.16 | -1.000 / -1.000 |
| 8 | 786.2 | 4.84 / 4.78 | 40.0/39.0 | 5.04 | 1.43 | 0.96 | 44.0 | 9.75 | 0 | 1 | 0.00 / 1.15 | -0.250 / -0.875 |
| 10 | 684.9 | 4.68 / 4.59 | 38.0/38.0 | 4.87 | 1.41 | 0.81 | 42.0 | 9.75 | 0 | 1 | 0.35 / 1.15 | -0.000 / -0.500 |
| 12 | 635.4 | 4.56 / 4.43 | 38.0/36.0 | 4.74 | 1.24 | 0.81 | 40.0 | 10.25 | 0 | 1 | 0.50 / 1.20 | 0.000 / -0.250 |
| 14 | 599.9 | 4.45 / 4.31 | 36.0/35.0 | 4.61 | 1.16 | 0.79 | 39.0 | 10.25 | 0 | 1 | 0.61 / 1.23 | 0.000 / 0.000 |
| 16 | 573.0 | 4.37 / 4.20 | 36.0/35.0 | 4.44 | 1.01 | 0.79 | 37.0 | 10.75 | 0 | 1 | 0.94 / 1.31 | -0.000 / 0.000 |
| 18 | 541.5 | 4.18 / 4.02 | 35.0/34.0 | 4.15 | 0.76 | 0.78 | 34.0 | 11.25 | 0 | 1 | 1.00 / 1.47 | 0.000 / 0.000 |
| 20 | 515.0 | 4.07 / 3.90 | 35.0/32.0 | 4.00 | 0.70 | 0.76 | 33.0 | 11.25 | 0 | 1 | 1.06 / 1.48 | 0.000 / 0.000 |
| 22 | 476.4 | 3.68 / 3.57 | 31.0/30.0 | 3.58 | 0.50 | 0.61 | 29.0 | 11.75 | 0 | 1 | 1.00 / 1.45 | 0.000 / -0.000 |
| 24 | 433.2 | 3.40 / 3.42 | 27.0/29.0 | 3.33 | 0.34 | 0.59 | 28.0 | 12.25 | 0 | 1 | 1.00 / 1.39 | -0.000 / -0.000 |
| 26 | 382.5 | 3.13 / 3.09 | 26.0/27.0 | 2.97 | 0.29 | 0.55 | 24.0 | 12.75 | 0 | 1 | 1.00 / 1.36 | 0.000 / -0.000 |
| 28 | 335.6 | 2.82 / 2.81 | 23.0/24.0 | 2.63 | 0.41 | 0.50 | 22.0 | 12.75 | 0 | 1 | 0.87 / 1.19 | 0.000 / 0.125 |
| 30 | 285.7 | 2.53 / 2.60 | 20.0/23.0 | 2.38 | 0.28 | 0.52 | 20.0 | 13.25 | 0 | 1 | 1.00 / 1.17 | -0.000 / 0.250 |
| 32 | 214.0 | 1.97 / 2.12 | 15.0/18.0 | 1.87 | 0.45 | 0.49 | 15.0 | 13.75 | 0 | 1 | 0.87 / 1.08 | -0.000 / 0.250 |
| 34 | 137.9 | 1.49 / 1.79 | 11.0/15.0 | 1.42 | 0.48 | 0.46 | 11.0 | 14.25 | 0 | 1 | 0.87 / 1.10 | 0.000 / -0.000 |
| 36 | 57.5 | 1.20 / 1.31 | 6.0/11.0 | 0.86 | 0.46 | 0.40 | 7.0 | 14.75 | 0 | 1 | 1.00 / 1.21 | 0.000 / -0.000 |
| 38 | -20.3 | — / 0.62 | 0.0/4.0 | — | — | — | 0.0 | — | — | — | — | 0.000 / 0.000 |
| 40 | -76.5 | — / — | 0.0/0.0 | — | — | — | 0.0 | — | — | — | — | 0 (no lines) |
| 218 (final) | -141.5 | — / — | 0.0/0.0 | — | — | — | 0.0 | — | — | — | — | 0 (no lines) |

Energy split and §4 diagnostics:

| it | E | E_grad | E_mag | E_V | E_χ | E_χ (A·S part) | ⟨\|S\|/\|ψ\|²⟩_w | E_χ near line 1 | virial |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 2442.0 | 1687.0 | 0.00 | 755.0 | 0.0 | 0.00 | 0.427 | 0.17 | 1.000 |
| 2 | 1372.8 | 1137.8 | 13.60 | 691.3 | -470.0 | 2.26 | 0.341 | -48.80 | 0.542 |
| 4 | 1167.4 | 1000.7 | 18.43 | 618.9 | -470.7 | 6.23 | 0.366 | -57.51 | 0.497 |
| 6 | 943.0 | 846.7 | 46.07 | 404.3 | -354.1 | 34.69 | 0.450 | -92.58 | 0.464 |
| 8 | 786.2 | 744.9 | 64.22 | 377.4 | -400.3 | 54.44 | 0.495 | -107.16 | 0.369 |
| 10 | 684.9 | 731.5 | 81.88 | 347.6 | -476.0 | 75.59 | 0.520 | -121.13 | 0.264 |
| 12 | 635.4 | 717.9 | 97.60 | 319.6 | -499.6 | 94.87 | 0.548 | -132.73 | 0.209 |
| 14 | 599.9 | 664.7 | 105.97 | 310.9 | -481.6 | 103.21 | 0.575 | -135.33 | 0.198 |
| 16 | 573.0 | 612.9 | 111.06 | 320.2 | -471.2 | 105.58 | 0.589 | -131.61 | 0.198 |
| 18 | 541.5 | 569.9 | 123.13 | 328.8 | -480.3 | 111.18 | 0.585 | -126.33 | 0.179 |
| 20 | 515.0 | 548.1 | 124.59 | 309.1 | -466.7 | 110.78 | 0.581 | -122.96 | 0.165 |
| 22 | 476.4 | 497.6 | 121.08 | 286.8 | -429.1 | 93.69 | 0.562 | -106.72 | 0.162 |
| 24 | 433.2 | 468.7 | 106.30 | 272.3 | -414.2 | 73.10 | 0.540 | -94.72 | 0.158 |
| 26 | 382.5 | 453.4 | 89.16 | 238.0 | -398.1 | 52.42 | 0.508 | -82.77 | 0.137 |
| 28 | 335.6 | 424.5 | 86.29 | 198.5 | -373.7 | 47.54 | 0.518 | -76.67 | 0.101 |
| 30 | 285.7 | 387.4 | 68.52 | 200.4 | -370.5 | 42.89 | 0.498 | -65.80 | 0.099 |
| 32 | 214.0 | 340.2 | 52.80 | 201.7 | -380.7 | 36.50 | 0.450 | -50.33 | 0.075 |
| 34 | 137.9 | 286.1 | 41.66 | 182.9 | -372.7 | 35.03 | 0.421 | -36.31 | 0.029 |
| 36 | 57.5 | 214.2 | 32.69 | 150.9 | -340.4 | 36.94 | 0.372 | -24.41 | -0.034 |
| 38 | -20.3 | 138.3 | 23.36 | 117.1 | -299.0 | 39.50 | 0.311 | — | -0.119 |
| 40 | -76.5 | 100.8 | 9.93 | 103.8 | -291.1 | 40.24 | 0.152 | — | -0.179 |
| 218 (final) | -141.5 | 46.1 | 0.00 | 96.8 | -284.4 | -0.00 | 0.000 | — | -0.257 |

Surface-subtracted virial residual (descriptive; §7): 0: +1.000, 2: +0.764, 4: +0.731, 6: +0.806, 8: +0.678, 10: +0.511, 12: +0.435, 14: +0.432, 16: +0.437, 18: +0.406, 20: +0.399, 22: +0.427, 24: +0.444, 26: +0.448, 28: +0.442, 30: +0.461, 32: +0.426, 34: +0.391, 36: +0.391, 38: +0.488.

## 6. Verdicts (PREREG §5, applied literally)

### 6.1 Per run

PREREG §5 defines four outcomes:
- **STABLE:** the relaxation stops at R* > 2ξ with |Lk(strand 1, composite)| = 1, the 81³ check agrees, and the virial residual is < 0.10.
- **COLLAPSE:** the ring shrinks to core scale, or strand 1 unlinks.
- **MARGINAL:** a finite stop with residual ≥ 0.10, or a stop at R* ≤ 2ξ.
- **EXPANDS:** the ring grows to the box.

In all 12 runs:
- the composite radius falls monotonically through 2ξ = 1.41 to zero;
- strand 1 unlinks (Lk12 and Lk13 reach 0) or merges;
- every line vanishes (by iteration 28–40);
- E decreases at every record.

**All 12 are COLLAPSE.** No run has a finite stop, so MARGINAL does not arise. No line approaches a box face: strand 1's wall gap only grows, and there are never any open ends.

| start | γ | verdict | mechanism | strand 1 unlinks (Lk12 / Lk13 → 0) | strand 1 gone | all lines gone | γ = 0 (rerun): strand 1 gone / all gone |
|---|---|---|---|---|---|---|---|
| A | +0.1 | COLLAPSE | point reconnection | it 20 / 20–22 (contact from it 16) | 22 | 28 | 22 / 28 |
| A | −0.1 | COLLAPSE | point reconnection | 20–22 / 20 | 22 | 28 | 22 / 28 |
| A | +0.2 | COLLAPSE | point reconnection, then separation | 20 / 22 | 24 | 30 | 22 / 28 |
| A | −0.2 | COLLAPSE | point reconnection, then separation | 22 / 18 | 24 | 30 | 22 / 28 |
| A | +0.3 | COLLAPSE | point reconnection, then separation | 18 / 18 | 28 | 32 | 22 / 28 |
| A | −0.3 | COLLAPSE | point reconnection, then separation | 22 / 18 | 28 | 32 | 22 / 28 |
| B | +0.1 | COLLAPSE | merge onto the core | unresolved (contact from it 12) | 36 | 36 | 36 / 36 |
| B | −0.1 | COLLAPSE | merge onto the core | unresolved (contact from it 10) | 36 | 36 | 36 / 36 |
| B | +0.2 | COLLAPSE | other: point crossing, then unlinked coaxial co-shrinking | 12 / 14 (contact it 8–10) | 38 | 38 | 36 / 36 |
| B | −0.2 | COLLAPSE | other: as +0.2 | 10 / 16 (contact it 8–10) | 38 | 40 | 36 / 36 |
| B | +0.3 | COLLAPSE | other: as +0.2 | 12 / 12 (contact it 6–10) | 38 | 40 | 36 / 36 |
| B | −0.3 | COLLAPSE | other: as +0.2 | 10 / 14 (contact it 6–10) | 38 | 40 | 36 / 36 |

(Records are every 2 iterations, so "it 20" means between 18 and 20.)

**Start A, |γ| = 0.1: point reconnection, as at γ = 0.**
- Strand 1's Hopf loop contracts while drawn inward. R falls 6.15 → 4.3 and its centroid x 6.13 → 4.25. The composite shrinks 5.92 → 2.3.
- At it 16–18 the lines touch at one place: min separation 0 to 0.35, mean 1.7–2.1.
- Lk is non-integer at it 16–18 and 0 by it 20–22. Strand 1's remnant (length 10, z_rms 0.5) vanishes at it 22.
- The composite (strands 2 and 3, now separate lines with R differing by ≤ 0.4) shrinks alone and vanishes at it 28. This is the γ = 0 sequence, iteration for iteration.

**Start A, |γ| = 0.2 and 0.3: point reconnection, then separation.**
- The same point contact occurs, at it 16 (+0.2, +0.3) or 18–20 (−0.2, −0.3), with mean separation ≥ 1.5.
- After the unlinking, strand 1's loop does not vanish at once. Its min separation from strand 2 rises: 0.50 → 1.06 at |γ| = 0.2; 0.35 → 0.87 → 1.00 → 1.46 → 1.50 over it 18–26 at +0.3, and 0.61 → 1.54 at −0.3.
- It shrinks on its own (R 3.1 → 1.4 at 0.3) and vanishes 2–4 (|γ| = 0.2) or 6–10 (|γ| = 0.3) iterations after unlinking.
- The composite vanishes at it 30 or 32. Strand 3's line outlives strand 2's by 2 iterations at |γ| = 0.3.
- As in `REPORT_N1_cells.md` §5.2, "separation" describes what happens after the crossing. It cannot be the unlinking mechanism itself.

**Start B, |γ| = 0.1: merge onto the core, as at γ = 0.**
- Contact begins at it 10–12. The min separation is 0 from it 20 on, with the mean ≤ 0.8, and strand 1's z_rms locks at 0.24–0.25 from it 22.
- The merged object shrinks to zero at it 36, the same iteration as γ = 0.
- Lk is non-integer from the first contact, so when the link was lost is not resolved, as at γ = 0.

**Start B, |γ| = 0.2 and 0.3: something else.** This is not a merge and not a separation.
1. **Early point crossing.** The helix touches the composite at one place at it 6–10: min separation 0, but the mean stays 1.0–1.6.
2. **Clean unlinking.** Lk12 and Lk13 then reach **0.000 exactly** at it 10–16, and the two lines no longer touch: min separation 0.5–1.0. So, unlike γ = 0, the unlinking is resolved. It is a point reconnection that converts the helix (once round the core, once round the z-axis) into an unlinked loop.
3. **Co-shrinking.** Strand 1 keeps W_z = 1, so it is a loop coaxial with the ring. It runs alongside the composite at mean separation 0.7–1.6 (1–3 grid spacings), with z_rms 0.3–0.8 against 0.24 for a merged line. The pair shrinks together, monotonically.
   - In the last records the separation falls (mean 0.5–0.7). At |γ| = 0.2 Lk13 turns non-integer again (it 26–36), meaning the lines touch.
   - All lines vanish at it 38–40.
- The separation is at the resolution limit (1–3 h). So "rides alongside" versus "merged with a lattice offset" is a distinction at one or two grid spacings. That the link itself is lost (Lk = 0.000) is resolved.

### 6.2 Parity classification per (start, |γ|)

| start | \|γ\| | +γ | −γ | classification |
|---|---|---|---|---|
| A | 0.1 | COLLAPSE | COLLAPSE | **COLLAPSE** |
| A | 0.2 | COLLAPSE | COLLAPSE | **COLLAPSE** |
| A | 0.3 | COLLAPSE | COLLAPSE | **COLLAPSE** |
| B | 0.1 | COLLAPSE | COLLAPSE | **COLLAPSE** |
| B | 0.2 | COLLAPSE | COLLAPSE | **COLLAPSE** |
| B | 0.3 | COLLAPSE | COLLAPSE | **COLLAPSE** |

No CHIRAL-STABLE. No STABLE, parity-even.

**Delay comparison (descriptive, as §5 requires for COLLAPSE).**
- **Favourable against unfavourable sign: no difference in timing.** At every (start, |γ|) the +γ and −γ runs lose strand 1 at the same recorded iteration. All lines go at the same record too, except B |γ| = 0.2, where −γ is one record later (40 against 38). In this sense neither sign is favourable: the start's twist sense (Lk = −1) selects neither.
- **Against γ = 0: a small delay that depends on |γ| only.** Strand 1 is gone at it 22 (γ = 0) and at 22, 24 and 28 (A, |γ| = 0.1, 0.2, 0.3). For B it is 36 against 36, 38 and 38. All lines go at it 28 against 28, 30 and 32 (A), and 36 against 36, 38–40 and 40 (B).
- **No plateau.** E decreases at every record in every run, and in the γ = 0 runs. The composite radius decreases through each run, up to lattice jitter of a few hundredths.
- E at matched iterations is lower than at γ = 0 from it 2 on. At it 8 (|γ| = 0.3) it is 1053 against 1221 (A) and 787 against 938 (B). The offset is mostly the surface twist forming (§6.4), not a property of the loop.

### 6.3 P3

P3: at every γ ≠ 0, the ±γ runs show "E at matched iterations differs by more than 1 %". Relative difference = |E₊ − E₋| / max(|E₊|, |E₋|), at matched recorded iterations.

| start | \|γ\| | any matched record (literal) | while strand 1 exists in both runs | max \|ΔE\| | P3 literal |
|---|---|---|---|---|---|
| A | 0.1 | 8.1 % (it 36) | **0.10 %** (it 20; \|ΔE\| 0.5) | 0.51 | holds |
| A | 0.2 | 9.9 % (it 32) | **0.68 %** (it 22; \|ΔE\| 2.9) | 3.8 | holds |
| A | 0.3 | 38.5 % (it 30) | **8.9 %** (it 26; \|ΔE\| 19.5); first > 1 % at it 18 | 22.2 | holds |
| B | 0.1 | 66 % (it 42) | **2.1 %** (it 34; \|ΔE\| 4.1); ≤ 0.7 % to it 32 | 5.1 | holds |
| B | 0.2 | 118 % (it 40) | **7.1 %** (it 36; \|ΔE\| 9.9); first > 1 % at it 28 | 15.6 | holds |
| B | 0.3 | 17 % (it 38) | **3.5 %** (it 34; \|ΔE\| 5.0); first > 1 % at it 28 | 7.9 | holds |

- **Literal reading** ("differs by more than 1 %" at some matched iteration): **P3 holds at every |γ| for both starts.**
- **But many of the largest values are trivial.** They come after strand 1 has gone, where E crosses zero on its way to the negative surface-state energy, so the relative difference of two small numbers is large.
- **Restricted to records where both runs still contain strand 1's line** (the twisted texture): the ±γ trajectories agree to **0.10 % (A, 0.1) and 0.68 % (A, 0.2)**, below the 1 % mark. They exceed it at A 0.3 (from it 18) and at B 0.1, 0.2, 0.3 (only in the last 2–5 records before strand 1 vanishes).
- **The two readings disagree at A |γ| = 0.1 and 0.2. Flagged for the author** (§8, ambiguity a).

What the ±γ difference consists of is visible in the tables. The sign of γ decides which of strands 2 and 3 lags: in start A at +0.3, strand 3's ring is the larger (R 2.46 against 1.81 at it 24), and at −0.3 strand 2's is (2.48 against 2.03). The energy split is nearly sign-even: E_χ and E_χ near line 1 have the same sign and nearly the same size for ±γ (−74 and −84 near line 1 at A it 14). **The texture takes whichever handedness γ favours, so the chiral energy acts at second order in γ, not as a parity-odd selection.**

### 6.4 The energy split and the virial residual

**Where the chiral energy sits.** At |γ| = 0.3:
- **Total E_χ:** −340 to −640 while the loop exists. Of that, about −284 is the surface twist of §3.5 (the end-state value), which forms within the first 2 iterations.
- **E_χ within distance 3 of strand 1's line:** −31 to −84 (A) and −49 to −135 (B). For comparison, E is 500–1800 over the same records.
- **A·S part:** in start A it is negative (−50 to −120). In start B and in the control it is positive (+2 to +111; up to +328 in the control), so there the A·S coupling costs energy in the gauge the minimizer reached. This is gauge dependent (§2.1).
- **⟨|S|/|ψ|²⟩_w:** 0.4–0.57 in the twisted textures, close to the 1D optimum's 0.54. The relative-phase sector is the one that is active, as in `REPORT_chiral1d.md`.

**Virial residual.**
- Literal, as PREREG §4 defines it: it starts at 1.000 for every run (A = 0 and E_χ ≈ 0 at the start, so the ratio is 1) and falls as the loop collapses. It goes below 0.10 only in the last records with lines: A ±0.3 from it 24, B ±0.3 from it 28–30, and B −0.2 at it 38 (one record). In every final (line-free) state it is −0.256 to −0.258.
- These low and negative values are **not** a stationary loop. They come from the surface twist, a boundary-bound state with no scaling symmetry, which enters E_grad, E_V and E_χ.
- **Surface-subtracted residual (descriptive, my addition).** I subtracted each run's final split from every record before forming the ratio, using absolute values of each piece in the denominator. This residual stays ≥ 0.31 (|γ| = 0.3), ≥ 0.50 (0.2) and ≥ 0.59 (0.1) at every record with lines. The loop is never close to a scaling-stationary point. This is consistent with COLLAPSE.
- The residual entered no verdict: STABLE needs a finite stop first, and none occurred.

### 6.5 Box checks at 81³

**Not run.** §4 runs one only for a 65³ run that does not collapse, and all 12 collapse.

## 7. Notes and caveats

1. As in the earlier reports, L-BFGS iterations are a minimizer path, not a time evolution. "Delay" means records along that path.
2. Statements at one grid spacing (h = 0.5 = 0.71ξ) are resolution-limited. The B |γ| ≥ 0.2 "alongside, not merged" distinction is at 1–3 grid spacings.
3. **"E above vacuum" changes meaning at γ ≠ 0.** The reference is `gl3.vacuum_energy()`, as PREREG and the scripts define it. The box's line-free minimum lies below it by 15.6, 62.7 and 141.5 at |γ| = 0.1, 0.2, 0.3, because of the open-boundary surface twist (§3.5). I have not changed the reference.
4. `trace_N1.py`'s "sep" and "R comp." refer to strand 2. In these runs strands 2 and 3 are separate lines, so strand 3 is reported in its own columns and Lk13 is given.
5. No field files were saved, as in the earlier reports. Final-state claims rest on the line detection and the energy split.

## 8. Deviations and ambiguities, collected

**Deviations**
1. **SciPy installed with pip.** It was not in the container, and `gl3.py` needs it.
2. **Branch.** All commits were pushed directly to `claude/seed-step3-first-closure`, on top of 6de2b27.
3. **The P1 controls were run at maxiter 4000 and a record every 2** (the brief's run settings), not at `control_N0.py`'s own 600 and 25. `REPORT_N1_cells.md` deviation 3 took the other reading. Here I made maxiter and the interval optional arguments, which default to the original values. The controls converged in 221–226 iterations, so 600 would also have sufficed. `control_N0_chiral.py` also records the energy split and segment counts, which `control_N0.py` does not. The counts were needed to read P1.
4. **Threads.** The regression (§3.4) was run with default threads, like the original, and is bit-exact. The production runs, C0 and the controls used one BLAS/OpenMP thread each, running 4 at a time. The one-thread regression differs from the original by ≤ 3.6 × 10⁻¹³ relative in E, with identical segment counts and Lk.
5. **Added files**, beyond the three named scripts:
   - `chiral_loop_checks.py` and its output;
   - `c0_chiral.py`, which runs C0, since no script for it existed;
   - `run_chiral_loop.sh`;
   - `tables_chiral_loop.py` and `log_tables_chiral_loop.txt`;
   - the two regression JSONs and logs;
   - `diff_*_chiral.txt`;
   - stage logs.
   None changes a run.
6. **A·S part.** It is defined on the lattice as E_χ − E_χ[ψ, A = 0], which is gauge dependent. It is reported in the minimizer's gauge.
7. **Gradient check, 5-point form.** 19 components with an exactly-zero analytic gradient (unused link slices) were excluded from the relative measure and reported separately (§3.1). gl3's own measure on them is a 10⁻⁸-floor artefact.
8. **Surface-subtracted virial residual and the P3 "strand 1 present" restriction.** Both are descriptive additions. The literal quantities are reported alongside them and used for the verdicts.
9. **C0 "noise"** was taken as N(0, 0.05) on every free variable (Re ψ, Im ψ, A), with `default_rng(0)`. This is the same reading as `REPORT_chiral1d.md` deviation 6.

**Ambiguities, flagged for the author.** Each was resolved by the most literal reading.
- **(a) P3's "differs by more than 1 %"** does not say over which iterations, or relative to what. Literally it holds everywhere. Restricted to the twisted texture's lifetime, it fails at A |γ| = 0.1 and 0.2 (§6.3).
- **(b) C0's "≤ 10⁻⁵"** is met by a negative value. "Relaxes back to the vacuum" is not met as such: the end state is the vacuum in the bulk plus a chiral surface twist. I kept both γ (§3.5). A periodic or twist-free boundary would remove the surface state, but that is a new pre-registration (PREREG §6).
- **(c) P1's reasoning** ("S = 0, almost no chiral coupling") does not hold in the run: E_χ reaches −586 and S develops. The prediction itself, collapse, holds.
- **(d) Parity classification "the sign that holds is recorded with the start's twist sense".** It is not applicable, because no sign holds. Both starts have Lk = −1. No mirror (Lk = +1) start was run, since PREREG §4 lists none. So "favourable" is defined here only as +γ against −γ on the same start.

No parameter outside the PREREG was used. γ ∈ {±0.1, ±0.2, ±0.3} only. κ, η, h, R₀, the box, the starts and the ring orientation are as fixed.

## 9. What is and isn't established

**Established, at κ = 2, η = 0.1, h = 0.5, 65³, open boundaries, R₀ = 6, starts A and B (Lk = −1), with the locked chiral term:**
- The instrument passes all §3 checks. Its γ = 0 path is gl3's own, bit for bit. Its sign convention matches `chiral1d.py`.
- At every pre-registered γ, both starts COLLAPSE. All 6 (start, |γ|) cells classify as **COLLAPSE**. No handedness-selected closure was found, and no parity-even stabilization.
- The chiral term changes the collapse path, by |γ| more than by sign:
  - Strands 2 and 3 split.
  - Start A's remnant separates before vanishing (|γ| ≥ 0.2).
  - Start B unlinks early by a point crossing and co-shrinks as an unlinked coaxial loop instead of merging (|γ| ≥ 0.2).
  - Strand 1's survival grows by up to 6 iterations (A) and 2 (B) compared with γ = 0. The delay is the same for ±γ.
- The ±γ trajectories are nearly the same while strand 1 exists: ≤ 0.7 % at A |γ| ≤ 0.2 and ≤ 9 % at most anywhere in that window. The chiral energy near the loop is negative for both signs: the texture adapts its handedness.
- With open boundaries the chiral term creates a vortex-free surface twist. It lies below the uniform vacuum by about 1570γ² (15.6, 62.7, 141.5).

**Not established:**
- That no chiral-stabilized twisted ring exists. Only these starts, one R₀, one orientation of the locked frame (ring axis = cube axis z), one resolution and one box were tried, with |γ| ≤ 0.3 < γ_c.
- Anything about a mirror start (Lk = +1), periodic or twist-free boundaries, η ≠ 0.1, or other ring orientations. Each would be a new pre-registration (PREREG §6).
- The exact iteration of unlinking where the lattice curves touch (B |γ| = 0.1, and the late contacts at B |γ| = 0.2).
- Any gauge-invariant meaning of the A·S split.
- Any value of γ from a unit model (`NOTE_chiral_term.md` §6), and any physical reading. No particle identification is made or implied.

## 10. Files committed

- Instrument: `gl3_chiral.py`, `trace_N1_chiral.py`, `control_N0_chiral.py`, with diffs `diff_trace_N1_chiral.txt` and `diff_control_N0_chiral.txt`.
- Checks:
  - `chiral_loop_checks.py`, `chiral_loop_checks_output.txt`;
  - `regression_trace_N1_chiral_B_N65_R6_g0_it40.json` and `_omp1.json`, with `log_regression_g0.txt` and `log_regression_g0_omp1.txt`;
  - `c0_chiral.py`, `c0_chiral_N65_g±0.3.json`, `log_c0_g±0.3.txt`.
- Runs:
  - `run_chiral_loop.sh`, `log_run_stage1.txt`, `log_run_stage2.txt`;
  - `trace_N1_chiral_{A,B}_N65_R6_g{±0.1,±0.2,±0.3}.json` with `log_trace_chiral_*.txt`;
  - `control_N0_chiral_N65_R6_g±0.3.json` with `log_control_N0_chiral_g±0.3.txt`.
- Tables: `tables_chiral_loop.py`, `log_tables_chiral_loop.txt`.
- `REPORT_chiral_loop.md` (this file).
