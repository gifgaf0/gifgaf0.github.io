# estimator_setup.md — leaky-LWE-Estimator install + validation (Brief LEAKY-LWE Item 1)

**Status (2026-07-13, UPDATED): DONE IN-CONTAINER — validation gate PASSED.**
Sage **was** installed in this managed-remote container via **conda-forge / micromamba**
(not apt — `sagemath` is not packaged in Ubuntu noble, which is what the earlier
"cannot install" note actually hit), and the estimator reproduced its documented
validation bikz **exactly** (β=45.40; §3 below). The prior "instructions-for-Matt's-box,
container-can't-install" framing is superseded: the container *can* run the estimator; the
only caveat is **ephemerality** — the conda env does not persist across sessions and must be
recreated (~15–20 min, one command, §1), but the validation reproduces deterministically.
Per brief §2.2 the estimator remains minutes-scale, one-off, no persistent-compute
requirement; it also has no persistent-*install* requirement given the recreate command below.

**Discipline note (brief §2.2)**: Sage and the estimator are external
dependencies, deliberately NOT added to `pyproject.toml`. The estimator
runs in a **separate interpreter** from the project's fpylll/pytest suite.
The regression check for this brief is a confirmation the project suite is
still green — no project code changes, no new deps.

---

## §1. Sage install

### §1.0 What ACTUALLY worked in this container (2026-07-13) — reproduce this

apt `sagemath` is **not packaged in Ubuntu noble** (candidate: none, even with universe
enabled) — do not waste time on `apt-get install sagemath` here. conda-forge via a
static **micromamba** binary works cleanly (conda.anaconda.org is reachable through the
container proxy; micro.mamba.pm and GitHub *releases* are 403-blocked, so fetch micromamba
from the conda-forge channel directly):

```bash
# 1. micromamba (static binary) from the reachable conda-forge channel:
cd /root
curl -sSL -o micromamba.tar.bz2 \
  "https://conda.anaconda.org/conda-forge/linux-64/micromamba-2.8.1-0.tar.bz2"
tar xjf micromamba.tar.bz2 bin/micromamba
export MAMBA_ROOT_PREFIX=/root/micromamba

# 2. create the Sage env (~15–20 min, ~8 GB; downloads + links from conda-forge):
./bin/micromamba create -y -n sage -c conda-forge sage

# 3. verify:
./bin/micromamba run -n sage sage --version      # -> SageMath version 10.9, ...
```

**Recorded (this container's run):**
- **Sage version: `SageMath version 10.9`**  · **install method: conda-forge via micromamba 2.8.1**
- Ephemerality caveat: the env lives under `/root/micromamba` and is **not** persistent across
  managed-remote sessions; re-run steps 1–3 each session (one-off, minutes-scale).

### §1.1 Alternatives (Matt's dev box)

On a persistent box the distro/other routes may be simpler:

```bash
# Ubuntu/WSL: NOTE sagemath is dropped from recent Ubuntu; prefer conda-forge below.
# conda-forge (works on WSL, macOS, Linux):
conda create -n sage -c conda-forge sage && conda activate sage && sage --version
```

If the distro Sage is older than 9.0 or unavailable, fall back to the
conda-forge Sage or the upstream binary:

```bash
# Option A — conda-forge (works on WSL, macOS, Linux):
conda create -n sage -c conda-forge sage
conda activate sage
sage --version

# Option B — Docker (no local install required):
docker pull sagemath/sagemath:latest
docker run -it --rm -v $(pwd):/work sagemath/sagemath sage
```

**Record for the ledger entry (§5 of the brief)**:
- exact Sage version string: `_______________________` (fill in after install)
- install method (apt / conda / docker): `_______________________`

## §2. leaky-LWE-Estimator install

Clone the repo INSIDE the Sage environment (not into the project venv):

```bash
mkdir -p ~/tools && cd ~/tools
git clone https://github.com/lducas/leaky-LWE-Estimator.git
cd leaky-LWE-Estimator
git rev-parse HEAD    # record this commit hash for the ledger
```

**Recorded (this container's run):**
- **estimator commit hash: `0a9caf8bf0f80097724e0c6147194c52c6b90f86`** (cloned to
  `/root/leaky-LWE-Estimator`; GitHub clone over https works through the proxy).

Add the estimator's `framework/` directory to Sage's search path when
running the harness (see §4 below).

## §3. Validation gate (blocking)

Per brief §2.3, the estimator is not trusted until it reproduces a
documented example. The repo ships a validation suite under
`Sec5.2_validation/` (and a shorter README example). Run at least one and
compare the returned bikz to the documented reference value.

**Validation example used (this container):** the estimator README's own worked example — a
small LWE instance (n=m=70, q=3301, centered-binomial-40 secret & error), whose *documented*
`estimate_attack()` output is `dim=141  δ=1.012362  β=45.40`. The estimate is analytic
(deterministic), so it must reproduce exactly, not just within ±1. Script
`Sec5.2_validation/validate_readme.sage`:

```sage
load("../framework/instance_gen.sage")
n = 70; m = n; q = 3301
D_s = build_centered_binomial_law(40); D_e = D_s
A, b, dbdd = initialize_from_LWE_instance(DBDD, n, q, m, D_e, D_s)
beta, delta = dbdd.estimate_attack()      # -> beta=45.40, delta=1.012362
```
```bash
cd /root/leaky-LWE-Estimator/Sec5.2_validation
MAMBA_ROOT_PREFIX=/root/micromamba /root/bin/micromamba run -n sage sage validate_readme.sage
```

**Record (this container's run):**
- validation script used: `Sec5.2_validation/validate_readme.sage` (README n=70 example)
- reference bikz (README): **β = 45.40** (δ=1.012362, dim=141)
- reproduced bikz (this run): **β = 45.40** (δ=1.012362, dim=141)
- match: **PASS** — exact (not merely within ±1). The estimator's own output line printed
  `dim=141  δ=1.012362  β=45.40`, identical to the README.

If FAIL: halt — do not proceed to `op_2_58_2d_estimator.sage`. Surface the
failure. A mis-installed estimator gives wrong bikz for §2.58.B and would
be worse than no estimator at all. **(Not triggered — gate PASSED.)**

## §4. Running the OP-2.58.2d harness (post-validation)

Once §3 is PASS (it is). **In THIS container**, invoke Sage via the micromamba wrapper —
`MAMBA_ROOT_PREFIX=/root/micromamba /root/bin/micromamba run -n sage sage <script>` — in place
of a bare `sage` below (the estimator was cloned to `/root/leaky-LWE-Estimator`, not `~/tools`):

```bash
# From the gifgaf0.github.io repo root, with leaky-LWE-Estimator cloned to ~/tools:
export LEAKY_LWE_PATH=~/tools/leaky-LWE-Estimator/framework
cd /path/to/gifgaf0.github.io

# Toy weak bracket (k=7, 14 hints):
sage hybrid_kem/tools/op_2_58_2d_estimator.sage --toy-k 7 --bracket weak

# Toy strong bracket (k=7, 84 hints):
sage hybrid_kem/tools/op_2_58_2d_estimator.sage --toy-k 7 --bracket strong

# Toy k=14 both brackets (larger; ~minutes each):
sage hybrid_kem/tools/op_2_58_2d_estimator.sage --toy-k 14 --bracket weak
sage hybrid_kem/tools/op_2_58_2d_estimator.sage --toy-k 14 --bracket strong

# Spec (k=32) — optional if fast; expect longer runtime for 384-hint strong:
sage hybrid_kem/tools/op_2_58_2d_estimator.sage --spec --bracket weak
sage hybrid_kem/tools/op_2_58_2d_estimator.sage --spec --bracket strong
```

Output: predicted bikz for each (params, bracket) tuple. **Illustrative
only** — labeled non-binding per brief §4.2. The binding single-number
bikz requires session-side integration of the per-block 21^k guess cost
(Phase 2).

## §5. No changes to project code

- **`pyproject.toml`**: unchanged.
- **Project pytest suite**: unchanged; the estimator lives in a separate
  interpreter.
- **ruff clean** on project code: confirmed.
- **`OP_2_58_2d_staging_PREREGISTRATION.md`**: unchanged. Running an
  estimator is not "running lattice-reduction code against the §2.58.B
  construction at the parameters of §3.1" (brief §5; frozen pre-reg §6's
  retraction clause is not engaged).

## §6. Cross-references

- **Brief** (this session's uploaded `CLAUDE_CODE_BRIEF_LEAKY_LWE_ESTIMATOR.md`).
- **Recon**: `hybrid_kem/tools/op_2_58_2d_estimator_recon.md` (Item 2).
- **Harness**: `hybrid_kem/tools/op_2_58_2d_estimator.sage` (Item 3).
- **DDGR 2020** (eprint 2020/292): the perfect-hints-on-error framework
  the estimator implements.
- **May–Nowakowski 2023** (eprint 2023/777): faster single-stroke
  integrator; fallback if DDGR successive integration is slow at the
  strong-bracket hint count.
- **2025 error-hints refinement** (eprint 2025/1128): later refinement.
- **`github.com/lducas/leaky-LWE-Estimator`**: the tool.
