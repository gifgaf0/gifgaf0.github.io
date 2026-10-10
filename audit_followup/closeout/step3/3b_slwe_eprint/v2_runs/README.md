# Runs added for version 2 of the SLWE note (October 10, 2026)

**Plain-language summary.** An independent audit of the first version of the SLWE negative-result note (Zenodo
10.5281/zenodo.23270249) found that some of its statements about earlier documents were wrong, and that one side remark
was false. These three scripts produce the numbers that the note's revision uses to correct them and to fill the gaps the note left
open. None of them changes the note's main result: the Singer-orbit matrix still has rank at most 76 for every module
rank. What they add:

- the parameters of the proposing paper's version 2, with a uniform matrix, come out at about 2^167 operations. Every lattice attack in
  the estimator's default set is below the 2^272 that Category 5 needs;
- with weight-64 secrets, the working specification's own security-table rows (q = 911 and q = 3329 at n = 512) fall
  below 2^128;
- decryption first becomes failure-free at the prime 1039, not "for any q > 1032";
- Table 1's k = 1..7 columns now have three seed sets and a uniform control, like the other columns. The values are
  unchanged.

## The scripts

| Script | What it computes | Output |
|---|---|---|
| `table1_k1to7.py` | Table 1 for k = 1..7: three seed sets and a uniform control per (p, k), at p = 911 and p = 4 294 977 961, in both rank implementations of `audit_followup/phase_c/C1/` (imported unchanged). All 14 rows match the printed table. | `table1_k1to7.json`, `table1_k1to7_output.txt` |
| `v2_estimator_run.py` | Lattice estimator (commit `53da5982`, passagemath 10.8.12, default attacks) for five cases: version 2 after the rank collapse (2^40.4), version 2's parameters with a uniform matrix (2^167.2; uSVP 2^253.9 at β = 800), the specification's q = 3329 row (2^112.2), q = 911 at n = 512 with a dense ternary secret (2^148.5), and version 1's setting with a dense ternary secret (2^52.9). | `v2_estimator_results.json`, `v2_estimator_run.log` |
| `dfr_exact.py` | With N ~ CBD(258) exactly: at q = 911, the tail P(\|N\| > 227) = 2^−353.52 and the failure rate under four decoding rules and two encodings (2^−353.91, or 2^−351.45 for the decoder of `tools/sqt_slwe.py` with its encoding m⌊q/2⌋); and, for every q from 900 to 5000, whether any \|N\| ≤ 258 decodes wrongly. q = 1033 fails under every rule; from q = 1036 nothing fails, so the first safe prime is 1039. | `dfr_exact.json`, `dfr_exact_output.txt` |

## How to run

```
python3 table1_k1to7.py                     # python-flint; seconds
python3 dfr_exact.py                        # standard library only; seconds
PYTHONPATH=<lattice-estimator checkout at 53da5982> sage -python v2_estimator_run.py    # a few minutes
```

The C1 runs that the note's first version already cites (weight-64 secrets at n = 512 with q = 4 294 977 961, 2731 and
911, and the rank collapse at the proposing paper's version 1 setting) are in `audit_followup/phase_c/C1/estimator/` and are not repeated here.

## Checksums

| File | md5 |
|---|---|
| `table1_k1to7.py` | `2c4a71529b351753e072421ad5ac2ee7` |
| `table1_k1to7.json` | `001956220c401dafde7f547dd6a52001` |
| `table1_k1to7_output.txt` | `39f25c7e12adea04704514610e7e9403` |
| `v2_estimator_run.py` | `70f4ab0990603cf51d954d8aeaaa7e69` |
| `v2_estimator_results.json` | `abdf4bfb0528d5818ff193b2dc8a02c0` |
| `v2_estimator_run.log` | `822ad2cb9f472f923fc45f0231c12a36` |
| `dfr_exact.py` | `60986210f64c97b7e9d855f443660b8d` |
| `dfr_exact.json` | `4fe2df56db46f08df288f2c849061634` |
| `dfr_exact_output.txt` | `30a6f18cda4b0345518d76a9c6ae59b7` |
