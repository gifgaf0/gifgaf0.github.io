# estimator_setup.md — leaky-LWE-Estimator install + validation (Brief LEAKY-LWE Item 1)

**Status**: Instrument-validation instructions for Matt's WSL/Ubuntu box.
This container (the OP-2.58.2d managed-remote agent) cannot install Sage
persistently (fresh clone on every session; `apt-get install sagemath`
attempted, unavailable in the container's package sources). Per brief §2.2,
the estimator runs on the existing dev box — it is minutes-scale,
one-off, no persistent-compute requirement.

**Discipline note (brief §2.2)**: Sage and the estimator are external
dependencies, deliberately NOT added to `pyproject.toml`. The estimator
runs in a **separate interpreter** from the project's fpylll/pytest suite.
The regression check for this brief is a confirmation the project suite is
still green — no project code changes, no new deps.

---

## §1. Sage install

Recommended: install SageMath 10.x from the distro package for
reproducibility.

**Ubuntu / WSL Ubuntu (22.04 or newer)**:

```bash
sudo apt-get update
sudo apt-get install -y sagemath
sage --version
# Expected: SageMath version 10.x, Release Date: ...
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

**Record for the ledger entry**:
- estimator commit hash: `_______________________` (fill in from `git rev-parse HEAD`)

Add the estimator's `framework/` directory to Sage's search path when
running the harness (see §4 below).

## §3. Validation gate (blocking)

Per brief §2.3, the estimator is not trusted until it reproduces a
documented example. The repo ships a validation suite under
`Sec5.2_validation/` (and a shorter README example). Run at least one and
compare the returned bikz to the documented reference value.

**Suggested validation example**: the DDGR paper's Frodo-976 or Kyber-512
DBDD reduction — either has a reproducible bikz reported in
`Sec5.2_validation/kyber512.py` (or the equivalent per the current
commit). Command:

```bash
cd ~/tools/leaky-LWE-Estimator
sage Sec5.2_validation/kyber512.py
# or the newer script name if the repo's layout differs
```

**Expected**: returned bikz ≈ the reference value in the paper / README
(±1 bikz tolerance; the estimator has stochastic components).

**Record**:
- validation script used: `_______________________`
- reference bikz (from paper/README): `_______________________`
- reproduced bikz (from your run): `_______________________`
- match within ±1: **PASS / FAIL**

If FAIL: halt — do not proceed to `op_2_58_2d_estimator.sage`. Surface the
failure. A mis-installed estimator gives wrong bikz for §2.58.B and would
be worse than no estimator at all.

## §4. Running the OP-2.58.2d harness (post-validation)

Once §3 is PASS:

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
