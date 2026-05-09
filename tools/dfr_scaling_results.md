# Module-SLWE empirical DFR scaling

| k | q | failures | trials | DFR | log2(DFR) | notes |
|---|---|---|---|---|---|---|
| 4 | 911 | 498 | 1000 | 4.980e-01 | -1.01 | completed in 4s |
| 8 | 911 | 460 | 1000 | 4.600e-01 | -1.12 | completed in 11s |
| 12 | 911 | 496 | 1000 | 4.960e-01 | -1.01 | completed in 22s |
| 16 | 911 | 487 | 1000 | 4.870e-01 | -1.04 | completed in 39s |

**Linear fit:** log2(DFR) ≈ 0.000 · k + -1.047

Slope is the number of bits of failure-rate reduction we get per unit increase in module rank, holding q fixed at the larger settings.
