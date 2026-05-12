# CBD(η=2) ZD-pair density over F_p^16

100 000 samples per prime; CBD(η=2) gives entries in {-2,-1,0,1,2} with weights (1,4,6,4,1)/16. A vector is counted as ZD-pair when it has exactly two non-zero entries whose indices are an unordered pair in the precomputed `zd_pairs` set (42 pairs).

| p | ok | zd-pair | (% of samples) | all-zero | rejection rate | E[|coef|] |
|---|---:|---:|---:|---:|---:|---:|
| 911 | 100000 | 0 | 0.0000% | 0 | 0.0000% | 0.750 |
| 8191 | 99998 | 2 | 0.0020% | 0 | 0.0020% | 0.750 |

Verdict: rejection sampling is viable iff zd-pair rate < 1%. Observed rate at both primes is 0.0020%.
