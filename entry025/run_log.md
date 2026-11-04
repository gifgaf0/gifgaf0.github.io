# Entry 025 run log (append-only)

- 2026-11-03: rev. 3 approved by Matt (arm B 5,000 runs). Freeze package built: manifest.json (SHA-256 below).
- manifest.json sha256 2d8d8a0ddb8dfd3e9d2c66034501d548a70abda90116bf2b98ced7949d61c3ee
  - PREREGISTRATION.md 3998890be7c08b3f4cea64eeec6d6074eccf52ba7e206837032be0a4c55c271f
  - predict.py d6678d078daf489c9eb2da123312f967dcb9f26e5f2577f0efe0d222129d8f67
  - predictions.json 4d3e90346503cee2934ee9964beac3880562b934011b67328863c40a7b149059
  - gen.py ece8e3db6b3045e550c7e7ccfc3989ac6a91f1935fcd2cbe6901e78258301f74
  - analyze.py acfe74e6910541ae749cef3f5fde902fe9580f282318a1dfc21b9cca5b9ee098
- 2026-11-04: freeze commit 83080267043625571c4890a7d5f3d06a9a683815 pushed to gifgaf0/gifgaf0.github.io (branch ccr-8b0a23fb-g0djgx) at 2026-11-04T05:34:50Z (pusher's clock, UTC). All five manifest hashes verified before commit.
- Beacon named before publication: drand mainnet default chain (League of Entropy, 30 s period, genesis 1595431050). Push + 10 min = 05:44:50Z, so R = 6611336, published 2026-11-04T05:45:00Z. R and its time are to be confirmed against the chain's /info, and the randomness recorded, when fetched.
- 2026-11-04T16:21:35Z: fetched from api.drand.sh. /info confirms the default chain: hash 8990e7a9aaed2ffed73dbd7092123d6f289930540d7651336225dc172e51b2ce, genesis 1595431050, period 30 s. Round R = 6611336, published 2026-11-04T05:45:00Z.
  - randomness (SEED) 3ffa707eb1d3c2a115be7fa81c3af89618a7097e35632d140d8801224bda98da
  - signature b69813ad83d458d1085a44b05777a1c58f5163b5383963e4cf0aa8246e5cc9415a0c3af039bcece9ccc1c437b3565bd0082fcf7fef1109523f0bf5fc859662df4e33f3cc9e00a38c875b1e686cba2215b70945c6ed9b47b2d1122613957dde41
  - checked: sha256(signature) == randomness.
- Generation order: CCM_128, then DCM_256 (4 workers), then A37_64 and B37_128.
- 2026-11-04T18:29Z: CCM_128 generated (40,000 runs × 10,001 primes, seed above, 4 workers, 16:22–18:29Z). analyze.py (manifest check passed): integrity failures 0; RATE z = +0.19, R3 z = −0.17, LAG1|C z = +0.45, all as predicted. Output: results/CCM_128.json. Raw runs: data/archive/CCM_128_runs.tar.part00–04 (cat parts | tar -x), per-file hashes in CCM_128_runs.sha256.
- 2026-11-04T20:47Z: DCM_256 generated (10,000 runs × 10,001 primes, 18:29–20:47Z). analyze.py (manifest check passed): integrity failures 0; RATE z = −0.96, R3 z = +0.22, LAG1|C z = +0.63, all as predicted. Output: results/DCM_256.json. Raw runs: data/archive/DCM_256_runs.tar.part* (45 MB parts), per-file hashes in DCM_256_runs.sha256.
- 2026-11-04T20:47Z: started A37_64 (4,000 × 1,001), then B37_128 (5,000 × 1,001), same seed, 4 workers.
