# Brief 02 — Open Questions / Blockers

Two of the three Brief-02 deliverables are blocked on inputs that aren't
in this repository. Per the brief's stop conditions, this file logs
exactly what's needed before each can land.

## 1. Toy SLWE wrapper (Brief 02 §1) — BLOCKED

**Blocker:** `sqt_slwe__1_.py` is referenced in `SPEC.md` §2.6 and in the
brief itself, but it's not in this repository. Same for the master
document `SLWE_Prime_Master_v1.md` and the supporting files
`sqt_prime_core__1_.py` and `sedenion_Fp.py`.

**What's needed:**

- The SLWE source (`sqt_slwe__1_.py`) so the wrapper can call into it.
- The master doc (or just §2-§3 of it) so the wrapper agrees with the
  scheme on parameter names, secret/error distributions, and
  serialisation. Without it I'm guessing about the API.

**What I will NOT do unilaterally:**

- Re-derive the scheme from the high-level description in `SPEC.md`. The
  master doc presumably contains design choices (modulus splitting,
  rejection sampling, error distribution) that aren't recoverable from
  the spec alone, and inventing them silently would be worse than
  leaving the stub in place. A research-testbed wrapper has to wrap a
  specific construction; otherwise it's just a second stub with more
  code in it.

**Easy unblock:** copy `sqt_slwe__1_.py` (and the master doc) into the
repo at the project root, or paste the relevant function signatures.

## 2. Lattice-estimator integration (Brief 02 §2) — BLOCKED

**Blocker:** the Albrecht et al. lattice-estimator
<https://github.com/malb/lattice-estimator> is a SageMath library, not a
pip package. Probing the environment:

```text
$ which sage
(not found)

$ pip install lattice-estimator
ERROR: Could not find a version that satisfies the requirement lattice-estimator
```

`fpylll` (the underlying lattice library) installs cleanly, but the
estimator's public surface (`estimator.LWE.primal_usvp`, `estimator.LWE.dual`)
calls Sage symbols (`PolynomialRing`, `RR`, `BKZSimulator`) that aren't
provided by `fpylll` alone.

**What landed anyway:** `tools/lattice_estimate.py` — a real, runnable
script that produces the requested markdown table when executed under
SageMath with the estimator on `sys.path`. The parameter sets and the
assumptions are baked in; the only thing missing is the runtime. Run as:

```bash
sage -python tools/lattice_estimate.py --estimator-path /path/to/lattice-estimator
```

**What I will NOT do unilaterally:**

- Hard-code literature-derived numbers (e.g. from FIPS 203's security
  analysis) into `lattice_estimate_results.md` and pretend they came
  from a real estimator run. The brief explicitly says "don't paper over
  it"; that goes double for security cost numbers.

**Easy unblock options (pick one):**

1. Run the script on a Sage-equipped machine and commit the resulting
   `tools/lattice_estimate_results.md`.
2. Stand up a Docker image based on `sagemath/sagemath` and add a
   one-line CI job that produces the table.
3. Accept literature-only estimates with prominent labelling — but
   please sign off on this explicitly; I won't do it on my own
   authority.

## 3. DFR scaling (Brief 02 §3) — BLOCKED on §1

**Blocker:** `tools/dfr_scaling.py` uses
`SLWEWrapper(mode="toy", params={"k": k, "q": q})`. The wrapper still
raises `NotImplementedError` for non-stub modes (see Brief 02 §1).
Until §1 lands, this script can be reviewed but not executed.

**What's needed:** §1 unblocks §3. No additional inputs.

**Sub-question.** The brief says "k ∈ {4, 8, 12, 16}, q ≈ 2^24 for upper
sizes". Should the toy point (k=4) keep q=911, or should it use
q≈2^24 too so the linear fit is over a single q? My current script uses
(k=4, q=911) and (k≥8, q=2^24); flag if you want it homogeneous.
