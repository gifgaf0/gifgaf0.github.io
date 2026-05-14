# §X.1 — The cos 18° Prior Address

In the p6m lattice, three pentagons meeting at a vertex produce a 36°
angular deficit (3 × 108° = 324° ≠ 360°). The fold is bilateral, so
18° per side. cos(18°)¹ is the fraction of the void that survives a
seam crossing; ζ·(1 − cos 18°) is the fraction committed to maintaining it.

## Computation

| Factor | Value |
|---|---|
| ζ = 1 − π/√12 | 0.093100 |
| 1 − cos 18° | 0.048943 |
| ζ·(1 − cos 18°) | 0.004557 |

## Result

The uncorrected prediction ρ_structural = R_hyp × 49/4 undershoots the
muonic-hydrogen value (Pohl et al. 2013) by 0.4554% in ρ:

```
ρ_structural − ρ_muon = 3.980050 − 3.998261 = −0.018211   (−0.4554%)
```

Applying the void correction:

```
ρ = R_hyp × (49/4) × (1 + ζ·(1 − cos 18°)) = 3.998186
```

with post-correction residual

```
ρ − ρ_muon = 3.998186 − 3.998261 = −0.000076   (−0.0019%)
```

*Residual consistent with deeper geometric structure; see companion
framework documentation.*

The bilateral symmetry of the fold — the step from a 36° deficit to
18° per side — is stated here as a geometric fact. Its derivation from
the substrate action is not closed in the present work; until that
derivation lands, the cos 18° prior address is Register 2.

---

¹ Equivalent closed form: cos 18° = √(2 + φ)/2 with φ = (1 + √5)/2;
verified to 1e-12 in `tools/rho_derivation.py` (commit 4d6b612). For
the prior-address probe across the seven natural torus circles, see
the companion Brief 07 report (target: 14/40 chord positions at 0.05%
tolerance against the curated framework constant library; the loose
27/40 figure from the v1 scratch probe is not the citable count).
