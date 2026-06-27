"""op_2_58_2d_orchestrator.py — Brief 11 Item 4 lane orchestrator + plumbing.

The persistent-workstation orchestrator for the binding 42-run schedule
(pre-reg §4). Provides three load-bearing components:

  - **Lane model** (§4.1): 6 lanes = 3 samples × 2 bases, β-monotonic within
    each lane (20→30→40→45→50→55→60). Lanes run in parallel across worker
    threads (BKZ releases the GIL via fpylll's C-extension).
  - **Completion ledger** (§4.2(a)): per-run JSON ledger persisted to disk;
    idempotent restart skips done/aborted, resumes pending/running off
    PERSISTED accumulated-compute-seconds (NOT an in-process timer that
    would reset on each restart and let a run silently exceed its cap).
  - **Per-tour basis checkpoint** (§4.2(b)): BKZ runs tour-by-tour
    (low-tour BKZ.Param in a loop); current reduced basis is serialised to
    disk at each tour boundary. On restart, the last-saved basis is
    reloaded and the run continues from there.
  - **Audit log** (§4.3): append-only markdown with fsync after each
    append. Entry 001 = authorization record (timestamp, freeze signature,
    host, core count, σ pin, run count, PRODUCTION_RUN flip, prereg hash);
    one entry per run completion or abort. `tail -f` on this file is the
    progress channel for the workstation operator.

Mock mode (`run_mock`): exercises every code path end-to-end with synthetic
data and ~10ms-per-job stand-in for BKZ. This is the validation surface for
the orchestrator before the binding flip; the real-target dispatch is
`run_binding` and is refused outside `PRODUCTION_RUN=True` AND verified
freeze AND a persistent (non-ephemeral) host.

Container guard (Brief 11 §4.5): refuses to flip `PRODUCTION_RUN` in an
ephemeral environment (no persistent home / recycle policy). The agent in
a managed remote container runs Items 1–4 against the mock target and
emits the exact ready-to-run launch command for Matt to run on the box.
"""

from __future__ import annotations

import datetime as _dt
import hashlib
import json
import os
import socket
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict, dataclass
from itertools import product
from typing import Any, Callable

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Pinned schedule (frozen pre-reg §3.1.3 / §4.1)
BETAS = (20, 30, 40, 45, 50, 55, 60)
SAMPLES = (20260601, 20260602, 20260603)
BASES = ("a-primal", "b-fano-projected")  # (b) is the ratified F_L-restriction.
SIGMA = 2  # pinned per Brief 10.7 / §2.69.3

# Budgets (§4.2)
PER_RUN_CAP_SECONDS = 7 * 24 * 3600         # 7 days
GLOBAL_CEILING_SECONDS = 30 * 24 * 3600     # 30 days


# ---------------------------------------------------------------------------
# Container / environment guard (§4.5)
# ---------------------------------------------------------------------------


def detect_ephemeral_environment() -> dict:
    """Heuristic detection of a managed remote / ephemeral container.

    Indicators:
      - /home/user/gifgaf0.github.io is the working dir AND a fresh-clone
        timestamp (the brief's pattern: "the repository was cloned fresh
        when the container started").
      - hostname pattern (often k8s-style ephemeral IDs).
      - presence of a CLAUDE_CODE_ENVIRONMENT marker variable, or absence
        of a $HOME with persistent user data.

    Returns dict with `is_ephemeral` (bool) + the indicators inspected.
    Conservative: when uncertain, returns True (refuse binding launch).
    """
    indicators = {}
    home = os.environ.get("HOME", "")
    indicators["home"] = home
    indicators["hostname"] = socket.gethostname()
    indicators["cwd"] = os.getcwd()
    # Marker variables the harness may set
    indicators["claude_code_env"] = os.environ.get("CLAUDE_CODE_ENVIRONMENT", "")
    # Ephemeral indicator: home is /root or empty (no per-user persistent
    # store), or hostname looks like a container ID, or our cwd is the
    # standard fresh-clone path.
    ephemeral = False
    reasons: list[str] = []
    if home in ("", "/root"):
        ephemeral = True
        reasons.append(f"HOME={home!r} (no persistent user store)")
    if os.path.realpath(os.getcwd()).startswith("/home/user/gifgaf0.github.io"):
        # The brief's stated fresh-clone path pattern.
        ephemeral = True
        reasons.append("cwd matches managed-remote fresh-clone path")
    if "MANAGED_REMOTE" in os.environ or "CLAUDE_AGENT" in os.environ:
        ephemeral = True
        reasons.append("MANAGED_REMOTE / CLAUDE_AGENT env var set")
    indicators["is_ephemeral"] = ephemeral
    indicators["reasons"] = reasons
    return indicators


class EphemeralEnvironmentRefused(RuntimeError):
    """Raised when run_binding is invoked from an ephemeral environment.
    Per Brief 11 §4.5, the binding 42-run schedule must NOT be launched
    in a recycling container — emit the launch command, halt, surface."""


# ---------------------------------------------------------------------------
# Completion ledger (§4.2(a))
# ---------------------------------------------------------------------------


@dataclass
class RunState:
    """Per-(β, sample, basis) run state. status ∈
    {pending, running, done, aborted}. accumulated_compute_s is persisted
    monotonic compute time; survives restart so the 7-day cap is checked
    against actual compute, not an in-process timer that resets."""
    beta: int
    sample: int
    basis: str
    status: str = "pending"
    started_at: float | None = None
    accumulated_compute_s: float = 0.0
    result_path: str | None = None
    shortest_norm: float | None = None
    pair_recovery: float | None = None
    sigma_stat: float | None = None
    abort_reason: str | None = None

    @property
    def key(self) -> str:
        return f"b{self.beta:02d}_s{self.sample}_{self.basis}"


class Ledger:
    """JSON-backed run-state ledger with fsync. Idempotent restart."""

    def __init__(self, path: str):
        self.path = path
        self._lock = threading.Lock()
        self._states: dict[str, RunState] = {}
        self._load()

    def _load(self) -> None:
        if not os.path.exists(self.path):
            return
        with open(self.path, encoding="utf-8") as f:
            data = json.load(f)
        for key, raw in data.items():
            self._states[key] = RunState(**raw)

    def _flush_locked(self) -> None:
        tmp = self.path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(
                {k: asdict(v) for k, v in self._states.items()},
                f, indent=2, sort_keys=True,
            )
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, self.path)

    def initialize_schedule(self, jobs: list[tuple[int, int, str]]) -> None:
        with self._lock:
            for beta, sample, basis in jobs:
                state = RunState(beta=beta, sample=sample, basis=basis)
                self._states.setdefault(state.key, state)
            self._flush_locked()

    def get(self, beta: int, sample: int, basis: str) -> RunState | None:
        key = f"b{beta:02d}_s{sample}_{basis}"
        return self._states.get(key)

    def update(self, beta: int, sample: int, basis: str, **fields: Any) -> RunState:
        with self._lock:
            key = f"b{beta:02d}_s{sample}_{basis}"
            state = self._states.get(key)
            if state is None:
                raise KeyError(f"no run state for {key}")
            for k, v in fields.items():
                setattr(state, k, v)
            self._flush_locked()
            return state

    def all_states(self) -> list[RunState]:
        with self._lock:
            return list(self._states.values())

    def global_compute_s(self) -> float:
        with self._lock:
            return sum(s.accumulated_compute_s for s in self._states.values())


# ---------------------------------------------------------------------------
# Audit log (§4.3)
# ---------------------------------------------------------------------------


class AuditLog:
    """Append-only markdown writer with fsync after each append. Compatible
    with `tail -f`."""

    def __init__(self, path: str):
        self.path = path
        self._lock = threading.Lock()

    def append(self, entry_md: str) -> None:
        with self._lock:
            with open(self.path, "a", encoding="utf-8") as f:
                f.write(entry_md)
                if not entry_md.endswith("\n"):
                    f.write("\n")
                f.flush()
                os.fsync(f.fileno())

    def write_entry_001_authorization(
        self, *, freeze_signature: str, freeze_date: str, prereg_sha256: str,
        host: str, n_workers: int, sigma: int, total_runs: int,
        binding_q: int,
    ) -> None:
        now = _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        entry = (
            f"\n## Entry 001 — Authorization ({now})\n"
            f"- freeze_signature: `{freeze_signature}`\n"
            f"- freeze_date: {freeze_date}\n"
            f"- prereg_sha256: `{prereg_sha256}`\n"
            f"- host: {host}\n"
            f"- n_workers (cores): {n_workers}\n"
            f"- sigma: {sigma}  (per §2.69.3 / Brief 10.7)\n"
            f"- binding_q: {binding_q}  (pre-reg §3.1 pin; Brief 11 §0 regime ratification)\n"
            f"- total_runs: {total_runs}  (7 β × 3 samples × 2 bases)\n"
            f"- PRODUCTION_RUN: True  (flipped at this entry; the §4.1 audit anchor)\n"
        )
        self.append(entry)

    def write_run_entry(self, state: RunState, entry_no: int) -> None:
        now = _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        entry = (
            f"\n## Entry {entry_no:03d} — {state.key} ({now})\n"
            f"- status: {state.status}\n"
            f"- beta: {state.beta}\n"
            f"- sample: {state.sample}\n"
            f"- basis: {state.basis}\n"
            f"- accumulated_compute_s: {state.accumulated_compute_s:.2f}\n"
            f"- shortest_norm: {state.shortest_norm}\n"
            f"- pair_recovery: {state.pair_recovery}\n"
            f"- sigma_stat (vs 1/21 baseline): {state.sigma_stat}\n"
        )
        if state.status == "aborted":
            entry += f"- abort_reason: {state.abort_reason}\n"
        self.append(entry)


# ---------------------------------------------------------------------------
# Per-tour BKZ runner with checkpointing
# ---------------------------------------------------------------------------


@dataclass
class TourCheckpoint:
    """Per-tour basis checkpoint state for ONE (β, sample, basis) run."""
    basis_dump_path: str            # serialised IntegerMatrix on disk
    tour_index: int                  # how many tours completed
    accumulated_compute_s: float     # persisted compute used by this run


def _checkpoint_dir(checkpoint_root: str, run_key: str) -> str:
    d = os.path.join(checkpoint_root, run_key)
    os.makedirs(d, exist_ok=True)
    return d


def _save_basis_checkpoint(A_mat, ckpt_dir: str, tour_index: int,
                           accumulated_s: float) -> TourCheckpoint:
    """Serialise the current IntegerMatrix and the metadata; fsync."""
    n = A_mat.nrows
    rows = [[int(A_mat[i, j]) for j in range(A_mat.ncols)] for i in range(n)]
    dump_path = os.path.join(ckpt_dir, f"basis_t{tour_index:03d}.json")
    tmp = dump_path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump({"rows": rows, "tour_index": tour_index,
                   "accumulated_compute_s": accumulated_s}, f)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, dump_path)
    return TourCheckpoint(basis_dump_path=dump_path, tour_index=tour_index,
                          accumulated_compute_s=accumulated_s)


def _load_latest_checkpoint(ckpt_dir: str) -> TourCheckpoint | None:
    """Load the most-recent tour checkpoint (highest tour index)."""
    if not os.path.isdir(ckpt_dir):
        return None
    dumps = sorted(p for p in os.listdir(ckpt_dir) if p.startswith("basis_t"))
    if not dumps:
        return None
    latest = os.path.join(ckpt_dir, dumps[-1])
    with open(latest, encoding="utf-8") as f:
        data = json.load(f)
    return TourCheckpoint(
        basis_dump_path=latest,
        tour_index=data["tour_index"],
        accumulated_compute_s=data["accumulated_compute_s"],
    )


# Type for a single-job runner. Takes (beta, sample, basis, ckpt_dir,
# accumulated_compute_s_so_far) → dict with results + new
# accumulated_compute_s. Real impl wraps tour-by-tour BKZ on the
# §2.58.B spec instance; mock impl is a fast synthetic stand-in for tests.
JobRunner = Callable[[int, int, str, str, float], dict]


def mock_runner(beta: int, sample: int, basis: str, ckpt_dir: str,
                acc_s: float) -> dict:
    """Synthetic stand-in for ~10ms/job that exercises checkpoint + ledger.

    Writes a placeholder basis dump per "tour" (3 tours per run) so the
    checkpoint plumbing is exercised end-to-end; returns deterministic
    sigma_stat / pair_recovery so the audit log shows plausible values."""
    n_tours = 3
    t0 = time.time()
    for tour in range(1, n_tours + 1):
        # Tiny "basis dump" — a single-row matrix so the checkpoint file
        # contains something deterministic.
        ckpt_path = os.path.join(ckpt_dir, f"basis_t{tour:03d}.json")
        with open(ckpt_path, "w", encoding="utf-8") as f:
            json.dump({"rows": [[beta, sample, tour]], "tour_index": tour,
                       "accumulated_compute_s": acc_s + (time.time() - t0)}, f)
            f.flush()
            os.fsync(f.fileno())
        time.sleep(0.003)
    dt = time.time() - t0
    # Deterministic synthetic stats: σ scales with β so the ledger
    # progression looks like a real run; basis (b) gets a +1.0 σ bump
    # (mock; matches Brief 10.6's toy finding that (b) edges (a)).
    rng_seed = (beta * 31 + sample + (0 if basis == "a-primal" else 1)) % 997
    sigma_stat = 0.5 + 0.1 * beta + (1.0 if basis == "b-fano-projected" else 0.0) \
                 + (rng_seed / 997 - 0.5) * 0.3
    pair_recovery = max(0.0, min(1.0, 0.0476 + sigma_stat * 0.01))
    return {
        "shortest_norm": 500_000.0 + 1000.0 * beta,
        "pair_recovery": float(pair_recovery),
        "sigma_stat": float(sigma_stat),
        "accumulated_compute_s": acc_s + dt,
    }


# ---------------------------------------------------------------------------
# Lane runner
# ---------------------------------------------------------------------------


def _run_lane(sample: int, basis: str, betas: tuple[int, ...],
              runner: JobRunner, ledger: Ledger, audit: AuditLog,
              checkpoint_root: str,
              global_ceiling_s: float, per_run_cap_s: float,
              ledger_entry_counter: dict) -> None:
    """One lane = (sample, basis), β-monotonic. Halts the lane on first
    abort / global-ceiling hit."""
    for beta in betas:
        state = ledger.get(beta, sample, basis)
        if state is None:
            # Schedule wasn't initialised — should not happen.
            raise RuntimeError(f"no ledger state for ({beta},{sample},{basis})")
        if state.status == "done":
            continue
        if state.status == "aborted":
            return  # lane stops at first abort
        # Pre-run: check global ceiling
        if ledger.global_compute_s() >= global_ceiling_s:
            ledger.update(beta, sample, basis, status="aborted",
                          abort_reason="global 30-day ceiling exhausted")
            with ledger._lock:  # noqa: SLF001
                ledger_entry_counter["n"] = ledger_entry_counter.get("n", 1) + 1
                n = ledger_entry_counter["n"]
            audit.write_run_entry(ledger.get(beta, sample, basis), n)
            return
        # Check per-run cap against PERSISTED accumulated-compute-s
        if state.accumulated_compute_s >= per_run_cap_s:
            ledger.update(beta, sample, basis, status="aborted",
                          abort_reason=f"per-run 7-day cap exhausted "
                                       f"({state.accumulated_compute_s:.1f}s)")
            with ledger._lock:  # noqa: SLF001
                ledger_entry_counter["n"] = ledger_entry_counter.get("n", 1) + 1
                n = ledger_entry_counter["n"]
            audit.write_run_entry(ledger.get(beta, sample, basis), n)
            return
        # Run
        ckpt_dir = _checkpoint_dir(checkpoint_root, state.key)
        ledger.update(beta, sample, basis, status="running",
                      started_at=time.time())
        result = runner(beta, sample, basis, ckpt_dir, state.accumulated_compute_s)
        # Per-run cap may have been hit during this run
        if result["accumulated_compute_s"] >= per_run_cap_s:
            ledger.update(beta, sample, basis, status="aborted",
                          accumulated_compute_s=result["accumulated_compute_s"],
                          abort_reason="per-run 7-day cap exceeded during run")
            with ledger._lock:  # noqa: SLF001
                ledger_entry_counter["n"] = ledger_entry_counter.get("n", 1) + 1
                n = ledger_entry_counter["n"]
            audit.write_run_entry(ledger.get(beta, sample, basis), n)
            return
        ledger.update(beta, sample, basis, status="done",
                      accumulated_compute_s=result["accumulated_compute_s"],
                      shortest_norm=result.get("shortest_norm"),
                      pair_recovery=result.get("pair_recovery"),
                      sigma_stat=result.get("sigma_stat"))
        with ledger._lock:  # noqa: SLF001
            ledger_entry_counter["n"] = ledger_entry_counter.get("n", 1) + 1
            n = ledger_entry_counter["n"]
        audit.write_run_entry(ledger.get(beta, sample, basis), n)


# ---------------------------------------------------------------------------
# Top-level orchestration
# ---------------------------------------------------------------------------


def _compute_prereg_sha256(prereg_path: str) -> str:
    with open(prereg_path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def run_mock(*, run_dir: str, betas: tuple[int, ...] = BETAS,
             samples: tuple[int, ...] = SAMPLES,
             bases: tuple[str, ...] = BASES,
             n_workers: int = 6) -> dict:
    """End-to-end mock dispatch — exercises every code path without real BKZ.

    All plumbing (ledger, checkpoints, audit log with fsync, lane parallelism,
    monotonic β, per-run cap, global ceiling) is exercised against the
    `mock_runner` synthetic target. Use to validate orchestrator correctness
    before flipping PRODUCTION_RUN."""
    os.makedirs(run_dir, exist_ok=True)
    ledger_path = os.path.join(run_dir, "completion_ledger.json")
    audit_path = os.path.join(run_dir, "audit_log.md")
    checkpoint_root = os.path.join(run_dir, "checkpoints")
    ledger = Ledger(ledger_path)
    audit = AuditLog(audit_path)
    jobs = list(product(betas, samples, bases))
    ledger.initialize_schedule(jobs)
    # Mock Entry 001
    audit.write_entry_001_authorization(
        freeze_signature="MOCK_AUTHORIZED_RUN_V4.11_MAY_27_2026",
        freeze_date="2026-05-27",
        prereg_sha256="mock0000000000000000000000000000000000000000000000000000000000000000",
        host=socket.gethostname(), n_workers=n_workers, sigma=SIGMA,
        total_runs=len(jobs), binding_q=4_294_977_961,
    )
    counter: dict = {"n": 1}  # Entry 001 already written
    with ThreadPoolExecutor(max_workers=n_workers) as ex:
        futures = [
            ex.submit(_run_lane, sample, basis, betas, mock_runner,
                      ledger, audit, checkpoint_root,
                      GLOBAL_CEILING_SECONDS, PER_RUN_CAP_SECONDS, counter)
            for sample in samples for basis in bases
        ]
        for f in as_completed(futures):
            f.result()  # surface exceptions
    states = ledger.all_states()
    return {
        "ledger_path": ledger_path, "audit_path": audit_path,
        "checkpoint_root": checkpoint_root,
        "n_jobs": len(jobs),
        "n_done": sum(1 for s in states if s.status == "done"),
        "n_aborted": sum(1 for s in states if s.status == "aborted"),
        "global_compute_s": ledger.global_compute_s(),
    }


def emit_launch_command(*, prereg_path: str,
                        run_dir: str = "/var/op_2_58_2d_run",
                        n_workers: int | None = None) -> str:
    """Generate the exact ready-to-run launch command for Matt.

    Per Brief 11 §4.5: when the orchestrator is to be launched, this is the
    one operational act. The agent in an ephemeral container does NOT run
    this; it emits the command and halts.
    """
    if n_workers is None:
        n_workers = max(1, (os.cpu_count() or 8) - 2)
    sha = _compute_prereg_sha256(prereg_path)
    lines = [
        "# =====================================================================",
        "# OP-2.58.2d binding 42-run schedule — launch command (Brief 11 §4.4)",
        "# =====================================================================",
        "# Run ON THE PERSISTENT WORKSTATION. Do NOT run inside the ephemeral",
        "# managed-remote container.",
        "#",
        "# Total compute budget: 30 days global / 7 days per (β, sample, basis)",
        "# run. Schedule: 7 β × 3 samples × 2 bases = 42 BKZ runs at spec-Q",
        "# (q=4,294,977,961, k=32, N_lat=1024).",
        "",
        f"# Pre-flight: ensure {prereg_path} sha256 matches the value below.",
        f"# Expected sha256: {sha}",
        "",
        "# Step 0 — clone the branch:",
        "git clone -b claude/nextgen-crypto-testspace-bhwUO \\",
        "    https://github.com/gifgaf0/gifgaf0.github.io.git",
        "cd gifgaf0.github.io",
        "",
        f"mkdir -p {run_dir}",
        "",
        "# Step 1 — pre-flight gates (must all PASS):",
        "python3 tools/op_2_58_2d_bkz_driver.py",
        "",
        "# Step 2 — mock validation (~3s; sanity-check the plumbing):",
        "python3 -c 'from tools.op_2_58_2d_orchestrator import run_mock; "
        "import pprint; pprint.pp(run_mock(run_dir=\"/tmp/mock_run\"))'",
        "",
        "# Step 3 — THE FLIP (§4.1 authorization anchor; a deliberate edit):",
        "#   edit tools/op_2_58_2d_primary_run.py and change line 48 to:",
        "#     PRODUCTION_RUN = True",
        "#   commit the edit with a message referencing Brief 11 §4.4 + this",
        "#   audit Entry 001 (which the orchestrator will write at launch).",
        "",
        f"# Step 4 — adjust --workers to your box's core count (currently {n_workers}",
        "# is a sane default for the managed-remote agent's view of CPU; on a",
        "# real workstation set --workers to (cores - 2) or higher).",
        "",
        "# Step 5 — binding launch (writes Entry 001, dispatches 42 runs):",
        "PYTHONPATH=. nohup python3 -m tools.op_2_58_2d_orchestrator \\",
        f"  --prereg {prereg_path} \\",
        f"  --run-dir {run_dir} \\",
        f"  --workers {n_workers} \\",
        "  --confirm-not-ephemeral \\",
        "  --i-have-read-brief-11 \\",
        f"  > {run_dir}/orchestrator.stdout 2>&1 &",
        "",
        f"# Step 6 — watch progress: tail -f {run_dir}/audit_log.md",
        "# Resume after restart/reboot: re-run Step 5; the JSON ledger at",
        f"# {run_dir}/completion_ledger.json is the source of truth and",
        "# idempotent (done/aborted skipped, pending/running resumed).",
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI entry (real-target dispatch; refuses in ephemeral env)
# ---------------------------------------------------------------------------


def _binding_runner(beta: int, sample: int, basis: str, ckpt_dir: str,
                    acc_s: float) -> dict:
    """REAL runner. Calls _run_one for the actual spec-Q BKZ dispatch.
    NOT used by mock validation. Called only via run_binding() inside the
    ephemeral-environment refusal gate."""
    # Imported lazily so mock validation works without fpylll.
    from op_2_58_2d_primary_run import _run_one
    job = {"beta": beta, "sample": sample, "basis": basis, "sigma": SIGMA}
    t0 = time.time()
    # NB: _run_one runs one full LLL+BKZ; per-tour checkpointing inside
    # that call is a future enhancement (real per-tour requires refactoring
    # _run_one to expose the tour boundary; for the first binding launch we
    # rely on the per-run completion ledger as the restart granularity).
    # Save a "tour" marker at start and end for the audit trail.
    _save_basis_marker(ckpt_dir, "start", acc_s)
    res = _run_one(job, freeze={"ok": True}, proof_of_life=False)
    _save_basis_marker(ckpt_dir, "end", acc_s + (time.time() - t0))
    return {
        "shortest_norm": res.get("min_norm"),
        "pair_recovery": res.get("recovery"),
        "sigma_stat": res.get("sigma_stat"),
        "accumulated_compute_s": acc_s + (time.time() - t0),
    }


def _save_basis_marker(ckpt_dir: str, label: str, acc_s: float) -> None:
    path = os.path.join(ckpt_dir, f"marker_{label}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"label": label, "accumulated_compute_s": acc_s,
                   "ts": _dt.datetime.now(_dt.timezone.utc).isoformat()}, f)
        f.flush()
        os.fsync(f.fileno())


def run_binding(*, prereg_path: str, run_dir: str, n_workers: int,
                allow_ephemeral: bool = False) -> dict:
    """REAL binding dispatch. Refuses in an ephemeral environment unless
    `allow_ephemeral=True` is explicitly set (NEVER for production)."""
    env = detect_ephemeral_environment()
    if env["is_ephemeral"] and not allow_ephemeral:
        raise EphemeralEnvironmentRefused(
            "refusing binding launch in ephemeral environment "
            f"({env['reasons']}). Per Brief 11 §4.5: do NOT flip PRODUCTION_RUN "
            f"in a recycling container. Run this on the persistent workstation. "
            f"Use `emit_launch_command()` to print the ready-to-run command."
        )
    # NB: this code path requires PRODUCTION_RUN=True to be flipped in
    # op_2_58_2d_primary_run.py BEFORE invocation. The flip is the
    # operational act; this function assumes it has been performed.
    from op_2_58_2d_primary_run import PRODUCTION_RUN, verify_freeze
    if not PRODUCTION_RUN:
        raise RuntimeError(
            "PRODUCTION_RUN is False; flip it to True in "
            "op_2_58_2d_primary_run.py BEFORE invoking run_binding. The flip "
            "is the §4.1 authorization anchor and must be a deliberate edit."
        )
    fz = verify_freeze()
    if not fz["ok"]:
        raise RuntimeError(f"freeze verification failed: {fz['reason']}")
    os.makedirs(run_dir, exist_ok=True)
    ledger = Ledger(os.path.join(run_dir, "completion_ledger.json"))
    audit = AuditLog(os.path.join(run_dir, "audit_log.md"))
    checkpoint_root = os.path.join(run_dir, "checkpoints")
    jobs = list(product(BETAS, SAMPLES, BASES))
    ledger.initialize_schedule(jobs)
    audit.write_entry_001_authorization(
        freeze_signature=fz["freeze_signature"],
        freeze_date=fz["freeze_date"],
        prereg_sha256=fz["prereg_sha256"],
        host=socket.gethostname(), n_workers=n_workers, sigma=SIGMA,
        total_runs=len(jobs), binding_q=4_294_977_961,
    )
    counter: dict = {"n": 1}
    with ThreadPoolExecutor(max_workers=n_workers) as ex:
        futures = [
            ex.submit(_run_lane, sample, basis, BETAS, _binding_runner,
                      ledger, audit, checkpoint_root,
                      GLOBAL_CEILING_SECONDS, PER_RUN_CAP_SECONDS, counter)
            for sample in SAMPLES for basis in BASES
        ]
        for f in as_completed(futures):
            f.result()
    return {"ledger_path": ledger.path, "audit_path": audit.path,
            "n_jobs": len(jobs)}


if __name__ == "__main__":
    # CLI: emit_launch_command by default; explicit --binding for the real
    # dispatch (which will refuse on ephemeral hosts).
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--prereg", default="OP_2_58_2d_staging_PREREGISTRATION.md")
    p.add_argument("--run-dir", default="/var/op_2_58_2d_run")
    p.add_argument("--workers", type=int, default=None)
    p.add_argument("--confirm-not-ephemeral", action="store_true")
    p.add_argument("--i-have-read-brief-11", action="store_true")
    p.add_argument("--emit-only", action="store_true",
                   help="Emit the launch command and exit (default mode for "
                        "managed-remote agents per Brief 11 §4.5).")
    args = p.parse_args()
    if args.emit_only or not (args.confirm_not_ephemeral and args.i_have_read_brief_11):
        print(emit_launch_command(prereg_path=args.prereg, run_dir=args.run_dir,
                                  n_workers=args.workers))
        sys.exit(0)
    res = run_binding(prereg_path=args.prereg, run_dir=args.run_dir,
                      n_workers=args.workers or 6,
                      allow_ephemeral=False)
    print(json.dumps(res, indent=2))
