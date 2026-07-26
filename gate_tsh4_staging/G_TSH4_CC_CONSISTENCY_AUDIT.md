# G-TSH4 — CC Internal-Consistency Audit (NOT the E6 independent leg)

**Date:** 2026-07-23 · **Auditor:** CC · **Objects:** `gtsh4_phase12_results.json`,
`gtsh4_qc_verdict.json`, `G_TSH4_PHASE12_EXECUTION_REPORT.md`, `G_TSH4_CC_HANDOFF.md`.
**Script:** `tsh4_audit.py`.

> **THIS IS NOT THE INDEPENDENT SECOND LEG.** It is an internal-consistency + discipline audit of
> the chat leg's *own* delivered numbers, blocked from a valid E6 run by the two items in §A. It
> verifies the chat's arithmetic/logic; it does **not** independently adjudicate the physics or the
> split-step bias — that requires the blind from-scratch leg with the locked instrument.

## §A. Two blockers to a valid CC leg (raised, not worked around)
1. **Independence quarantine broken.** The CC handoff quarantines the chat's Phase-0/1/2 reports,
   energies, constants, slopes, and verdict — "transport them to the comparison stage only after the
   CC leg has produced and frozen its own numbers." Those exact files were delivered **before** any
   independent CC numbers exist. A from-scratch leg authored now, having seen the chat's energies
   (68.41/99.06), C_ij, and verdict (hcp-ISO / fcc-ANISO), cannot be called blind — E6 independence
   is compromised. The split-step-bias adjudication in particular (the CC leg is meant to be the
   independent check of whether split-step energies sit ~2.6–3.4% high) is exactly what a
   contaminated leg cannot honestly deliver.
2. **Locked instrument not delivered.** The handoff states the dispatch carries
   `G_TSH4_EXECUTION_PREREGISTRATION.md` (md5 `e66b964d…`) + `G_TSH4_PREREG_AMENDMENT_1.md` Part A —
   the self-contained model spec (analytic Û̃, Λ=2.0Λ_c convention, cell/structure definitions, E4
   direction sets, Q-A rule, falsifier constants). **Neither was forwarded**, so the locked leg
   cannot be executed as specified.

Also pending: the **A-2 conditional** (discrete GP residual validity gate ‖Hψ₀−μψ₀‖/μ≤1e-6) awaits
explicit author authorization before it binds the CC leg.

## §B. Internal-consistency audit — 21/21 PASS (chat leg self-consistent)
Verified from the raw JSON with independent arithmetic:
- **Controls:** C-POS central-force cubic Cauchy relation (C12=C44 exactly, C11/C44=2) and hex/cubic
  Christoffel closed forms machine-exact (2e-16/2e-15); C-NEG uniform Bogoliubov err 2.3e-12.
- **Elastic→speed:** hex:step √C44=7.5066 and √C66=7.7970 reproduce the Route-D static references.
- **hex F-ISO identity:** |C66−(C11−C12)/2|/C66 = 3.252% (step) / 3.804% (gem8) — matches the reported
  residuals; both >2% → **F-ISO FIRED → static hex NOT verdict-eligible** (correct per the locked rule).
- **cubic anisotropy:** Zener A = C44/C′ = 2.3225 (step) / 2.8381 (gem8); A_3D max-from-mean over the
  transverse multiset = 24.74% / 30.18% — matches reported; both > θ₂=10% → **ANISO-3D** (correct).
- **Route-D static↔dynamical:** axial-z dynamical slopes agree with √C44 to 0.26%; dynamical basal
  F-ISO (Γ→K vs Γ→M) SV 0.001% / SH 0.65% — PASS ≤2% (the dynamical instantiation that the report
  uses to argue basal isotropy is real despite the static hex fire).
- **Q-A:** close-packed AB < non-close-packed BCC by 1.23e-2 (step) / 9.0e-3 (gem8) → STACK-SELECTED;
  sub-order AB<FCC<ABC.
- **Split-step bias (chat-internal comparison only):** step:AB 2.62%, gem8:AB 3.46% above the
  polished discrete-GP minimum — consistent with the reported 2.6–3.4% S-class finding.

## §C. What this establishes / does not
**Establishes:** the chat leg's reported quantities are internally consistent and its falsifier/verdict
logic is correctly applied to its own numbers (no arithmetic or logic error found). The F-ISO
static-fire → hex-not-eligible and the cubic ANISO-3D routing are self-consistent.

**Does NOT establish:** anything independent about the physics — the ground-state energies, the C_ij
values, the split-step-bias magnitude, and the hcp-ISO/fcc-ANISO finding are all taken from the chat
leg and only checked for internal consistency. A real second leg (independent solver, blind to these
numbers, on the locked instrument) is still required for C1–C6 and any fold. The split-step-bias
adjudication explicitly cannot be provided by this audit.

---
*CC consistency audit filed 2026-07-23. Not the E6 leg. Blockers in §A must be resolved for a valid
two-leg run; verdict remains SINGLE-LEG PROVISIONAL.*
