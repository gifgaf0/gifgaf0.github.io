# G-QUANTA — CC LEG RETURN (P-4 single-file in-band, mirrored)

**Gate:** G-QUANTA (Topological Stability & Composite Quanta Discriminator). **Date:** September 10, 2026. **Leg:** cc.
**Dispatch received:** `dispatch.md` md5 `cd758b4477b71c776e9379cc7e0908a8` (68,964 B), activation flag `ACTIVATE: G-QUANTA-CC-LEG-1` present verbatim.
**Base ledger:** `SQT_Master_Ledger_v4_81_CANONICAL.md` md5 `b4e55aaea76a2152f7b1873309aec077`.
**Lock chain verified on extraction:** memo `0039d001769569297c2aa8ccbded5a3b` (4,863 B) · lock record `947768bd6d9652f5fdbeb43ceaf16502` (5,312 B) · comparator v1.0 `2be701be868259465525e29c79a4c621` (11,960 B) · schema v1.0 `05e53dbb8e8e1f7669fa12b6fc55c260` (1,615 B) — all four `OK`, three quarantined embeds `SKIP` on the blind pass.

## 1. Headline

**`C1-C6 ALL PASS` — 255 checks, 0 miss.** Two-leg comparison `g_quanta_twoleg_comparison.json` md5 `525012b9107eb99ac402bc4df9e3044f`. No S9 items. Independence witness holds machine-side: instrument md5s differ (`79072196cdfc480f4073195d96100d2e` chat vs `4b1e700e3df9c1b5f51904fbf70ec219` cc) and the checkpoints are not byte-identical.

CC-leg machine verdicts (route A ∧ route B, asserted per row):

| Object | C1 | C2 | Verdict |
|---|---|---|---|
| L_B Borromean Baryon | True | True | PASS |
| K₇ Vortex | True | True | PASS |
| Electron 2π Closure | True | True | PASS |
| Clifford Unknot / Rule 17 | False | True | FAIL |
| CD Tower Rungs (e.g., 42/84) | False | False | FAIL |
| Cluster M SLWE Matrices | False | False | FAIL |

F-QUANTA-1 SILENT (inert-by-inventory: silence is not a test passed) · F-QUANTA-2 SILENT · F-QUANTA-3 REGISTERED_NOT_EXECUTED. PC-1 met (3 PASS / 3 FAIL) · PC-2 met, witness set {K₇ Vortex} (passes via Competing Exponents, not the ropelength class) · PC-3 met (6/6 concordant with H-Q-1..6).

## 2. Branch and commit ordering (decoding audit, G-2a-L1 precedent)

Branch: **`claude/new-session-no3u27`** (repo `gifgaf0/gifgaf0.github.io`), estate directory `gquanta_gate/`.

1. **Pre-consultation checkpoint commit (armor unopened): `7d41f246ae412680765380c2fec65c3fd38e4051`** — instrument + checkpoint (checkpoint md5 `ca0e69a75a521f3869726693b23e3dce` in the commit message), plus dispatch, extractor, and the four plain frozen artifacts.
2. CC compare commit (armor still unopened): `f59ed890dfd03316f9f1c6550c825c891fca49a6` — `g_quanta_ccleg_compare.json` md5 `e8890dc462e67aabd28e6425ae88f18d`.
3. Consultation commit: the commit introducing the decoded chat-leg artifacts, the two-leg comparison, and this return file. Its hash necessarily post-dates these bytes; it is the commit that carries this file and is reported in the session summary.

## 3. Artifact byte-labels

| Artifact | md5 | Size |
|---|---|---|
| `g_quanta_ccleg.py` (instrument, cc) | `4b1e700e3df9c1b5f51904fbf70ec219` | 14,859 B |
| `g_quanta_ccleg_checkpoint.json` | `ca0e69a75a521f3869726693b23e3dce` | 3,335 B |
| `g_quanta_ccleg_compare.json` | `e8890dc462e67aabd28e6425ae88f18d` | 919 B |
| `g_quanta_twoleg_comparison.json` | `525012b9107eb99ac402bc4df9e3044f` | 37,514 B |

## 4. CC design register

- **CC-DD-1** — §4 table parsed at run time (no hand-copied rows); vocabulary-locked: an unknown perspective, config space, or functional class halts with exit 1. Functional class normalized by stripping one trailing parenthetical (`Competing Exponents (GP)` → `Competing Exponents`) to land in the schema value domain.
- **CC-DD-2** — invariant handling: a cell beginning `None` (`None`, `None (Trivial Knot)`) records `invariant: null` and invariant-absent for C1; any other cell is recorded verbatim and counts as invariant-present. Per §2, a non-None invariant over a Discrete space still evaluates C1 = NO (`Chirality/Algebraic` row exercises this).
- **CC-DD-3** — independence upgrade implemented as dispatched: route A is predicate logic off §2; route B is a hand-written 16-entry literal lookup table over the (ConfigSpace, InvariantPresent, FunctionalClass) triple. Agreement asserted per row at evaluation time and over all 16 triples in selftest S1.
- **CC-DD-4** — no object→outcome mapping anywhere in the instrument source. The outcome vocabulary strings exist only as the boolean-to-label map required by the checkpoint schema, and in the compare command's §5 parser, which runs only after the checkpoint is on disk (Eddington quarantine); `evaluate` never touches §5.
- **CC-DD-5** — compare rows are keyed by the §4 object names; §5 hypothesis names are matched to inventory rows by substring after stripping a trailing parenthetical (`K₇ Vortex (Independence Witness)` → `K₇ Vortex`; `SLWE Matrices` ⊂ `Cluster M SLWE Matrices`), with uniqueness and full-coverage asserted (halt otherwise).
- **CC-DD-6** — `utc` emitted via timezone-aware `datetime.now(timezone.utc)`; the chat leg's D-Q-2 `DeprecationWarning` does not recur on this leg.
- **CC-DD-7** — extractor saved byte-for-byte from dispatch §2 as `extract.py`; blind pass gave four `OK` / three `SKIP`, decode pass gave seven `OK`, zero assertion failures.
- **CC-DD-8** — instrument selftests (3/3 green): S1 route agreement on all 16 triples; S2 six-case outcome truth table on synthetic rows; S3 one-byte memo tamper → halt, exit 1, no checkpoint written.

## 5. Honesty register

- **H-CC-1** — no self-caught bugs and no halts on this leg: selftests, `evaluate`, `compare`, extraction, and the frozen comparator all ran green on first invocation. Reported plainly, not as a virtue: the instrument is small and the table is six rows.
- **H-CC-2** — blindness bookkeeping: before extraction, the dispatch file was read into the assistant context as text, but the read was truncated at line 402 of 936 — before the first quarantined block (which begins at line 450). Embed boundaries were then located by grepping the sentinel lines only. No armored bytes entered the assistant context before the pre-consultation checkpoint commit; the quarantined payloads were decoded only by `extract.py --decode-quarantined`, after commit `7d41f24…`, and their contents were consumed only by the frozen comparator, never read by the assistant.
- **H-CC-3** — interpretation call on "no verdict text may appear in the instrument source": read as prohibiting any hand-coded object→outcome association (and any §5 consultation during `evaluate`), not the outcome vocabulary itself, which the checkpoint schema requires the instrument to emit. The chat instrument necessarily makes the same call; flagged for the author in case a stricter reading was intended.
- **H-CC-4** — comparator v1.0 and schema v1.0 left byte-identical to the frozen artifacts (md5s above); no edits were made to either checkpoint or compare file after emission. Nothing in the comparator appeared wrong on this run.

## 6. Deviations

- **D-Q-1 / D-T1 (CC)** — carried and re-elected on this leg: the T1 forbidden-string list (13 lines, md5 prefix `04438b74`) was not supplied in the dispatch (the §1 embed inventory contains no T1 embed). CC self-grep state `LIST_ABSENT`, recorded in the checkpoint as `D-T1 (CC)`. No hits reportable; no pattern text quoted anywhere, per the reporting rule.
- No new CC-side deviations. D-Q-2 (chat `DeprecationWarning`) does not recur here (CC-DD-6); D-Q-3 (comparator frozen after the chat checkpoint) required no CC-side action — the comparator was applied as frozen.

## 7. T1 state

`LIST_ABSENT` — deviation `D-T1 (CC)` in force, mirroring the chat leg's author-elected D-T1. If the author supplies `T1_forbidden_strings.txt` (13 lines, md5 prefix `04438b74`), the CC instrument's checkpoint should be regenerated with the self-grep executed; the verdict-bearing content is not expected to change.

## 8. Embeds (byte-exact, same sentinel format; all raw)

=====BEGIN-EMBED name=g_quanta_ccleg.py md5=4b1e700e3df9c1b5f51904fbf70ec219 bytes=14859 encoding=raw=====
#!/usr/bin/env python3
"""g_quanta_ccleg.py -- Gate G-QUANTA, CC-leg instrument (independent implementation).

Written from the frozen staging memo (md5 0039d001769569297c2aa8ccbded5a3b) sections 2 and 4
and the lock record section 4 ONLY. The chat-leg instrument, checkpoint, and compare file were
QUARANTINED (base64-armored, undecoded) at the time this file was written.

Commands
  evaluate   md5-guard the memo, parse the section-4 table at run time, evaluate the
             discriminator by two structurally different routes (asserting per-row agreement),
             and write g_quanta_ccleg_checkpoint.json.
  compare    read the checkpoint back and compare machine verdicts against the memo's
             section-5 hypotheses (parsed at run time); write g_quanta_ccleg_compare.json.
             Never modifies the checkpoint. Run LAST (Eddington quarantine).
  selftest   tamper-guard, route-agreement, and truth-table spot checks on synthetic rows.

Design notes (CC-DD register in the dispatch return):
  - The section-4 table is the sole input; no row values are hand-copied into this source.
  - No object-to-outcome mapping appears anywhere in this source; the outcome vocabulary
    strings exist only as the boolean-to-label map required by the checkpoint schema.
  - Route A is predicate logic; route B is a 16-entry literal lookup table over the
    (config_space, invariant_present, functional_class) triple. Both must agree per row.
  - T1 forbidden-string list was not supplied to the CC leg: deviation D-T1 (CC),
    state LIST_ABSENT, recorded in the checkpoint.
"""
import hashlib
import json
import re
import sys
from datetime import datetime, timezone

MEMO_PATH = 'staging_memo_G_QUANTA_v2.md'
MEMO_LOCK_MD5 = '0039d001769569297c2aa8ccbded5a3b'
MEMO_LOCK_BYTES = 4863
CHECKPOINT_PATH = 'g_quanta_ccleg_checkpoint.json'
COMPARE_PATH = 'g_quanta_ccleg_compare.json'

PERSPECTIVES = ('L-Perspective', 'E-Perspective')
CONFIG_SPACES = ('Continuous', 'Discrete')
FUNCTIONAL_CLASSES = ('Rigid Constraint', 'Competing Exponents', 'Single Exponent', 'None')
DERRICK_EVADING = ('Rigid Constraint', 'Competing Exponents')

# ---------------------------------------------------------------- memo guard


def load_memo_guarded():
    raw = open(MEMO_PATH, 'rb').read()
    got = hashlib.md5(raw).hexdigest()
    if got != MEMO_LOCK_MD5 or len(raw) != MEMO_LOCK_BYTES:
        print(f'HALT: memo guard failed: md5 {got} (want {MEMO_LOCK_MD5}), '
              f'{len(raw)} B (want {MEMO_LOCK_BYTES})', file=sys.stderr)
        sys.exit(1)
    return raw.decode('utf-8')


def memo_section(text, number):
    for chunk in text.split('\n## '):
        if chunk.startswith(f'{number}.'):
            return chunk
    print(f'HALT: memo section {number} not found', file=sys.stderr)
    sys.exit(1)


def ledger_base_md5(text):
    m = re.search(r'\*\*Base:\*\*\s+`[^`]+`\s+\(md5\s+`([0-9a-f]{32})`\)', text)
    if not m:
        print('HALT: ledger base md5 not found in memo header', file=sys.stderr)
        sys.exit(1)
    return m.group(1)

# ------------------------------------------------------------- table parsing


def parse_inventory(text):
    """Parse the section-4 matrix at run time. Vocabulary-locked: unknown values halt."""
    sec = memo_section(text, 4)
    rows = []
    for line in sec.splitlines():
        line = line.strip()
        if not line.startswith('|'):
            continue
        cells = [c.strip() for c in line.strip('|').split('|')]
        if len(cells) != 6 or cells[0] == 'Object' or set(cells[0]) <= set(':- '):
            continue
        obj, ref, persp, cspace, inv_raw, fc_raw = cells
        fc = re.sub(r'\s*\([^)]*\)\s*$', '', fc_raw)
        if persp not in PERSPECTIVES:
            print(f'HALT: unknown perspective {persp!r} in row {obj!r}', file=sys.stderr)
            sys.exit(1)
        if cspace not in CONFIG_SPACES:
            print(f'HALT: unknown config space {cspace!r} in row {obj!r}', file=sys.stderr)
            sys.exit(1)
        if fc not in FUNCTIONAL_CLASSES:
            print(f'HALT: unknown functional class {fc_raw!r} in row {obj!r}', file=sys.stderr)
            sys.exit(1)
        invariant_present = not inv_raw.startswith('None')
        rows.append({
            'object': obj,
            'ledger_ref': ref,
            'perspective': persp,
            'config_space': cspace,
            'invariant': inv_raw if invariant_present else None,
            'functional_class': fc,
            'invariant_present': invariant_present,
        })
    if not rows:
        print('HALT: no inventory rows parsed from section 4', file=sys.stderr)
        sys.exit(1)
    return rows

# ------------------------------------------------------- discriminator routes


def route_a(config_space, invariant_present, functional_class):
    """Route A: predicate logic straight off the section-2 definitions."""
    c1 = (config_space == 'Continuous') and invariant_present
    c2 = functional_class in DERRICK_EVADING
    return c1, c2


# Route B: exhaustive literal lookup over the (config_space, invariant_present,
# functional_class) triple. Written out by hand, entry by entry, as the structurally
# independent second route required by the dispatch.
ROUTE_B = {
    ('Continuous', True,  'Rigid Constraint'):    (True,  True),
    ('Continuous', True,  'Competing Exponents'): (True,  True),
    ('Continuous', True,  'Single Exponent'):     (True,  False),
    ('Continuous', True,  'None'):                (True,  False),
    ('Continuous', False, 'Rigid Constraint'):    (False, True),
    ('Continuous', False, 'Competing Exponents'): (False, True),
    ('Continuous', False, 'Single Exponent'):     (False, False),
    ('Continuous', False, 'None'):                (False, False),
    ('Discrete',   True,  'Rigid Constraint'):    (False, True),
    ('Discrete',   True,  'Competing Exponents'): (False, True),
    ('Discrete',   True,  'Single Exponent'):     (False, False),
    ('Discrete',   True,  'None'):                (False, False),
    ('Discrete',   False, 'Rigid Constraint'):    (False, True),
    ('Discrete',   False, 'Competing Exponents'): (False, True),
    ('Discrete',   False, 'Single Exponent'):     (False, False),
    ('Discrete',   False, 'None'):                (False, False),
}


def evaluate_row(row):
    key = (row['config_space'], row['invariant_present'], row['functional_class'])
    a = route_a(*key)
    b = ROUTE_B[key]
    assert a == b, f'route disagreement on {row["object"]!r}: A={a} B={b}'
    c1, c2 = a
    ok = c1 and c2
    return {
        'object': row['object'],
        'ledger_ref': row['ledger_ref'],
        'perspective': row['perspective'],
        'config_space': row['config_space'],
        'invariant': row['invariant'],
        'functional_class': row['functional_class'],
        'C1': c1,
        'C2': c2,
        'verdict': ('FAIL', 'PASS')[ok],
    }

# ------------------------------------------------------------------ evaluate


def cmd_evaluate():
    memo_text = load_memo_guarded()
    rows = parse_inventory(memo_text)
    results = [evaluate_row(r) for r in rows]

    f1_fires = any(r['functional_class'] == 'Single Exponent' for r in results)
    f2_fires = any('Tower' in r['object'] and r['C1'] and r['C2'] for r in results)
    n_pass = sum(1 for r in results if r['C1'] and r['C2'])
    n_fail = len(results) - n_pass
    witnesses = [r['object'] for r in results
                 if r['C1'] and r['C2'] and r['functional_class'] != 'Rigid Constraint']

    checkpoint = {
        'gate': 'G-QUANTA',
        'leg': 'cc',
        'instrument': 'g_quanta_ccleg.py',
        'instrument_md5': hashlib.md5(open(__file__, 'rb').read()).hexdigest(),
        'memo': MEMO_PATH,
        'memo_md5': MEMO_LOCK_MD5,
        'memo_bytes': MEMO_LOCK_BYTES,
        'ledger_base_md5': ledger_base_md5(memo_text),
        'elections': {
            'E-Q-1': '(b) promote standalone -- CC-leg wording',
            'E-Q-2': '(a) E-perspective for envelopes, L-perspective for defects; '
                     'extended defects in scope -- CC-leg wording',
        },
        'utc': datetime.now(timezone.utc).isoformat(timespec='seconds'),
        'inventory_rows': len(results),
        'results': results,
        'falsifiers': {
            'F-QUANTA-1': {'state': ('SILENT', 'FIRES')[f1_fires],
                           'note': 'inert-by-inventory: the locked table declares no '
                                   'Single Exponent row, so silence is not a test passed'},
            'F-QUANTA-2': {'state': ('SILENT', 'FIRES')[f2_fires]},
            'F-QUANTA-3': {'state': 'REGISTERED_NOT_EXECUTED'},
        },
        'promotion_conditions': {
            'PC-1_nontrivial_partition': {'met': n_pass >= 1 and n_fail >= 1,
                                          'n_pass': n_pass, 'n_fail': n_fail},
            'PC-2_independence_witness': {'met': len(witnesses) >= 1,
                                          'witnesses': witnesses},
        },
        'T1': {'state': 'LIST_ABSENT', 'deviation': 'D-T1 (CC)',
               'note': 'T1 forbidden-string list (13 lines, md5 prefix 04438b74) not '
                       'supplied to the CC leg; self-grep not performed'},
        'deviations': ['D-T1 (CC): T1 list absent, self-grep skipped, state LIST_ABSENT'],
        'route_agreement': 'route A (predicate) and route B (literal lookup) agreed on '
                           'every row (asserted per row at evaluation time)',
    }
    blob = json.dumps(checkpoint, ensure_ascii=False, indent=2)
    open(CHECKPOINT_PATH, 'w', encoding='utf-8').write(blob + '\n')
    md5 = hashlib.md5(open(CHECKPOINT_PATH, 'rb').read()).hexdigest()
    print(f'checkpoint written: {CHECKPOINT_PATH}  md5 {md5}')
    for r in results:
        print(f"  {r['verdict']}  C1={r['C1']!s:5} C2={r['C2']!s:5}  {r['object']}")
    print(f"  F-QUANTA-1 {checkpoint['falsifiers']['F-QUANTA-1']['state']} (inert-by-inventory) | "
          f"F-QUANTA-2 {checkpoint['falsifiers']['F-QUANTA-2']['state']} | "
          f"F-QUANTA-3 REGISTERED_NOT_EXECUTED")
    print(f"  PC-1 met={checkpoint['promotion_conditions']['PC-1_nontrivial_partition']['met']} "
          f"({n_pass} pass / {n_fail} fail) | PC-2 met="
          f"{checkpoint['promotion_conditions']['PC-2_independence_witness']['met']} "
          f"witnesses={witnesses}")

# ------------------------------------------------------------------- compare


def parse_hypotheses(text):
    """Parse section-5 predicted outcomes at run time (consulted only here, never in evaluate)."""
    sec = memo_section(text, 5)
    out = []
    for m in re.finditer(r'^\*\s+\*\*(.+?):\*\*\s+(PASS|FAIL)', sec, re.M):
        name = re.sub(r'\s*\([^)]*\)\s*$', '', m.group(1)).strip()
        out.append((name, m.group(2)))
    if not out:
        print('HALT: no hypotheses parsed from section 5', file=sys.stderr)
        sys.exit(1)
    return out


def cmd_compare():
    memo_text = load_memo_guarded()
    checkpoint = json.load(open(CHECKPOINT_PATH, encoding='utf-8'))
    hyps = parse_hypotheses(memo_text)
    results = checkpoint['results']
    rows = []
    for name, predicted in hyps:
        matches = [r for r in results if name in r['object'] or r['object'] in name]
        if len(matches) != 1:
            print(f'HALT: hypothesis {name!r} matches {len(matches)} inventory rows',
                  file=sys.stderr)
            sys.exit(1)
        r = matches[0]
        rows.append({'object': r['object'], 'predicted': predicted,
                     'machine': r['verdict'], 'concordant': predicted == r['verdict']})
    if len(rows) != len(results):
        print(f'HALT: {len(rows)} hypotheses vs {len(results)} inventory rows', file=sys.stderr)
        sys.exit(1)
    out = {'gate': 'G-QUANTA', 'leg': 'cc',
           'checkpoint_md5': hashlib.md5(open(CHECKPOINT_PATH, 'rb').read()).hexdigest(),
           'rows': rows, 'PC-3_met': all(r['concordant'] for r in rows)}
    blob = json.dumps(out, ensure_ascii=False, indent=2)
    open(COMPARE_PATH, 'w', encoding='utf-8').write(blob + '\n')
    md5 = hashlib.md5(open(COMPARE_PATH, 'rb').read()).hexdigest()
    print(f'compare written: {COMPARE_PATH}  md5 {md5}')
    for r in rows:
        mark = 'concordant' if r['concordant'] else 'DISCORDANT'
        print(f"  {mark}  predicted {r['predicted']} / machine {r['machine']}  {r['object']}")
    print(f"  PC-3_met={out['PC-3_met']}")

# ------------------------------------------------------------------ selftest


def cmd_selftest():
    import copy
    import os
    import tempfile
    # S1: every lookup-table entry agrees with route A over the full triple domain.
    for cs in CONFIG_SPACES:
        for inv in (True, False):
            for fc in FUNCTIONAL_CLASSES:
                assert route_a(cs, inv, fc) == ROUTE_B[(cs, inv, fc)], (cs, inv, fc)
    print('  green  S1 route A == route B on all 16 triples')
    # S2: outcome truth table spot checks (synthetic rows, no ledger objects named).
    mk = lambda cs, inv, fc: evaluate_row({'object': 'synthetic', 'ledger_ref': 'none',
                                           'perspective': 'L-Perspective', 'config_space': cs,
                                           'invariant': 'X' if inv else None,
                                           'functional_class': fc, 'invariant_present': inv})
    assert mk('Continuous', True, 'Rigid Constraint')['verdict'] == 'PASS'
    assert mk('Continuous', True, 'Competing Exponents')['verdict'] == 'PASS'
    assert mk('Continuous', False, 'Rigid Constraint')['verdict'] == 'FAIL'
    assert mk('Discrete', True, 'Competing Exponents')['verdict'] == 'FAIL'
    assert mk('Continuous', True, 'None')['verdict'] == 'FAIL'
    assert mk('Continuous', True, 'Single Exponent')['verdict'] == 'FAIL'
    print('  green  S2 truth-table spot checks (6 cases)')
    # S3: memo guard halts on a one-byte tamper.
    raw = bytearray(open(MEMO_PATH, 'rb').read())
    raw[100] ^= 1
    with tempfile.TemporaryDirectory() as td:
        tampered = os.path.join(td, MEMO_PATH)
        open(tampered, 'wb').write(bytes(raw))
        import subprocess
        p = subprocess.run([sys.executable, os.path.abspath(__file__), 'evaluate'],
                           cwd=td, capture_output=True, text=True)
        assert p.returncode == 1 and 'memo guard failed' in p.stderr, (p.returncode, p.stderr)
    print('  green  S3 one-byte memo tamper -> halt, exit 1, no checkpoint')
    print('ALL 3/3 SUITES GREEN')


def main():
    cmds = {'evaluate': cmd_evaluate, 'compare': cmd_compare, 'selftest': cmd_selftest}
    if len(sys.argv) != 2 or sys.argv[1] not in cmds:
        print(f'usage: {sys.argv[0]} {{evaluate|compare|selftest}}', file=sys.stderr)
        sys.exit(2)
    cmds[sys.argv[1]]()


if __name__ == '__main__':
    main()
=====END-EMBED name=g_quanta_ccleg.py=====

=====BEGIN-EMBED name=g_quanta_ccleg_checkpoint.json md5=ca0e69a75a521f3869726693b23e3dce bytes=3335 encoding=raw=====
{
  "gate": "G-QUANTA",
  "leg": "cc",
  "instrument": "g_quanta_ccleg.py",
  "instrument_md5": "4b1e700e3df9c1b5f51904fbf70ec219",
  "memo": "staging_memo_G_QUANTA_v2.md",
  "memo_md5": "0039d001769569297c2aa8ccbded5a3b",
  "memo_bytes": 4863,
  "ledger_base_md5": "b4e55aaea76a2152f7b1873309aec077",
  "elections": {
    "E-Q-1": "(b) promote standalone -- CC-leg wording",
    "E-Q-2": "(a) E-perspective for envelopes, L-perspective for defects; extended defects in scope -- CC-leg wording"
  },
  "utc": "2026-09-10T20:19:28+00:00",
  "inventory_rows": 6,
  "results": [
    {
      "object": "L_B Borromean Baryon",
      "ledger_ref": "§2.15/§2.51",
      "perspective": "L-Perspective",
      "config_space": "Continuous",
      "invariant": "Linking Number",
      "functional_class": "Rigid Constraint",
      "C1": true,
      "C2": true,
      "verdict": "PASS"
    },
    {
      "object": "K₇ Vortex",
      "ledger_ref": "§3.4",
      "perspective": "L-Perspective",
      "config_space": "Continuous",
      "invariant": "Fano Winding",
      "functional_class": "Competing Exponents",
      "C1": true,
      "C2": true,
      "verdict": "PASS"
    },
    {
      "object": "Electron 2π Closure",
      "ledger_ref": "§2.50.A",
      "perspective": "L-Perspective",
      "config_space": "Continuous",
      "invariant": "Winding Number",
      "functional_class": "Rigid Constraint",
      "C1": true,
      "C2": true,
      "verdict": "PASS"
    },
    {
      "object": "Clifford Unknot / Rule 17",
      "ledger_ref": "§2.41",
      "perspective": "L-Perspective",
      "config_space": "Continuous",
      "invariant": null,
      "functional_class": "Rigid Constraint",
      "C1": false,
      "C2": true,
      "verdict": "FAIL"
    },
    {
      "object": "CD Tower Rungs (e.g., 42/84)",
      "ledger_ref": "§2.31/§2.75",
      "perspective": "E-Perspective",
      "config_space": "Discrete",
      "invariant": "Chirality/Algebraic",
      "functional_class": "None",
      "C1": false,
      "C2": false,
      "verdict": "FAIL"
    },
    {
      "object": "Cluster M SLWE Matrices",
      "ledger_ref": "§2.58",
      "perspective": "E-Perspective",
      "config_space": "Discrete",
      "invariant": null,
      "functional_class": "None",
      "C1": false,
      "C2": false,
      "verdict": "FAIL"
    }
  ],
  "falsifiers": {
    "F-QUANTA-1": {
      "state": "SILENT",
      "note": "inert-by-inventory: the locked table declares no Single Exponent row, so silence is not a test passed"
    },
    "F-QUANTA-2": {
      "state": "SILENT"
    },
    "F-QUANTA-3": {
      "state": "REGISTERED_NOT_EXECUTED"
    }
  },
  "promotion_conditions": {
    "PC-1_nontrivial_partition": {
      "met": true,
      "n_pass": 3,
      "n_fail": 3
    },
    "PC-2_independence_witness": {
      "met": true,
      "witnesses": [
        "K₇ Vortex"
      ]
    }
  },
  "T1": {
    "state": "LIST_ABSENT",
    "deviation": "D-T1 (CC)",
    "note": "T1 forbidden-string list (13 lines, md5 prefix 04438b74) not supplied to the CC leg; self-grep not performed"
  },
  "deviations": [
    "D-T1 (CC): T1 list absent, self-grep skipped, state LIST_ABSENT"
  ],
  "route_agreement": "route A (predicate) and route B (literal lookup) agreed on every row (asserted per row at evaluation time)"
}
=====END-EMBED name=g_quanta_ccleg_checkpoint.json=====

=====BEGIN-EMBED name=g_quanta_ccleg_compare.json md5=e8890dc462e67aabd28e6425ae88f18d bytes=919 encoding=raw=====
{
  "gate": "G-QUANTA",
  "leg": "cc",
  "checkpoint_md5": "ca0e69a75a521f3869726693b23e3dce",
  "rows": [
    {
      "object": "L_B Borromean Baryon",
      "predicted": "PASS",
      "machine": "PASS",
      "concordant": true
    },
    {
      "object": "K₇ Vortex",
      "predicted": "PASS",
      "machine": "PASS",
      "concordant": true
    },
    {
      "object": "Electron 2π Closure",
      "predicted": "PASS",
      "machine": "PASS",
      "concordant": true
    },
    {
      "object": "Clifford Unknot / Rule 17",
      "predicted": "FAIL",
      "machine": "FAIL",
      "concordant": true
    },
    {
      "object": "CD Tower Rungs (e.g., 42/84)",
      "predicted": "FAIL",
      "machine": "FAIL",
      "concordant": true
    },
    {
      "object": "Cluster M SLWE Matrices",
      "predicted": "FAIL",
      "machine": "FAIL",
      "concordant": true
    }
  ],
  "PC-3_met": true
}
=====END-EMBED name=g_quanta_ccleg_compare.json=====

=====BEGIN-EMBED name=g_quanta_twoleg_comparison.json md5=525012b9107eb99ac402bc4df9e3044f bytes=37514 encoding=raw=====
{
  "checks": [
    {
      "check": "C-Q-0",
      "item": "chat: required key gate",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "chat: required key leg",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "chat: required key instrument",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "chat: required key instrument_md5",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "chat: required key memo",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "chat: required key memo_md5",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "chat: required key memo_bytes",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "chat: required key ledger_base_md5",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "chat: required key elections.E-Q-1",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "chat: required key elections.E-Q-2",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "chat: required key utc",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "chat: required key inventory_rows",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "chat: required key results",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "chat: required key falsifiers.F-QUANTA-1.state",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "chat: required key falsifiers.F-QUANTA-2.state",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "chat: required key falsifiers.F-QUANTA-3.state",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "chat: required key promotion_conditions.PC-1_nontrivial_partition.met",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "chat: required key promotion_conditions.PC-1_nontrivial_partition.n_pass",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "chat: required key promotion_conditions.PC-1_nontrivial_partition.n_fail",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "chat: required key promotion_conditions.PC-2_independence_witness.met",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "chat: required key promotion_conditions.PC-2_independence_witness.witnesses",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "chat: results[0].object",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "chat: results[0].ledger_ref",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "chat: results[0].perspective",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "chat: results[0].config_space",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "chat: results[0].invariant",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "chat: results[0].functional_class",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "chat: results[0].C1",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "chat: results[0].C2",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "chat: results[0].verdict",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "chat: results[1].object",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "chat: results[1].ledger_ref",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "chat: results[1].perspective",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "chat: results[1].config_space",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "chat: results[1].invariant",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "chat: results[1].functional_class",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "chat: results[1].C1",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "chat: results[1].C2",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "chat: results[1].verdict",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "chat: results[2].object",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "chat: results[2].ledger_ref",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "chat: results[2].perspective",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "chat: results[2].config_space",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "chat: results[2].invariant",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "chat: results[2].functional_class",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "chat: results[2].C1",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "chat: results[2].C2",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "chat: results[2].verdict",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "chat: results[3].object",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "chat: results[3].ledger_ref",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "chat: results[3].perspective",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "chat: results[3].config_space",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "chat: results[3].invariant",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "chat: results[3].functional_class",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "chat: results[3].C1",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "chat: results[3].C2",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "chat: results[3].verdict",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "chat: results[4].object",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "chat: results[4].ledger_ref",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "chat: results[4].perspective",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "chat: results[4].config_space",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "chat: results[4].invariant",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "chat: results[4].functional_class",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "chat: results[4].C1",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "chat: results[4].C2",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "chat: results[4].verdict",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "chat: results[5].object",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "chat: results[5].ledger_ref",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "chat: results[5].perspective",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "chat: results[5].config_space",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "chat: results[5].invariant",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "chat: results[5].functional_class",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "chat: results[5].C1",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "chat: results[5].C2",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "chat: results[5].verdict",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "chat: memo_md5 == lock",
      "result": "PASS",
      "chat": "0039d001769569297c2aa8ccbded5a3b",
      "cc": "0039d001769569297c2aa8ccbded5a3b"
    },
    {
      "check": "C-Q-0",
      "item": "chat: memo_bytes == lock",
      "result": "PASS",
      "chat": 4863,
      "cc": 4863
    },
    {
      "check": "C-Q-0",
      "item": "chat: instrument_md5 real 32-hex",
      "result": "PASS",
      "chat": "79072196cdfc480f4073195d96100d2e",
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "chat: no placeholder tokens",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "cc: required key gate",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "cc: required key leg",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "cc: required key instrument",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "cc: required key instrument_md5",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "cc: required key memo",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "cc: required key memo_md5",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "cc: required key memo_bytes",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "cc: required key ledger_base_md5",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "cc: required key elections.E-Q-1",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "cc: required key elections.E-Q-2",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "cc: required key utc",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "cc: required key inventory_rows",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "cc: required key results",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "cc: required key falsifiers.F-QUANTA-1.state",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "cc: required key falsifiers.F-QUANTA-2.state",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "cc: required key falsifiers.F-QUANTA-3.state",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "cc: required key promotion_conditions.PC-1_nontrivial_partition.met",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "cc: required key promotion_conditions.PC-1_nontrivial_partition.n_pass",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "cc: required key promotion_conditions.PC-1_nontrivial_partition.n_fail",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "cc: required key promotion_conditions.PC-2_independence_witness.met",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "cc: required key promotion_conditions.PC-2_independence_witness.witnesses",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "cc: results[0].object",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "cc: results[0].ledger_ref",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "cc: results[0].perspective",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "cc: results[0].config_space",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "cc: results[0].invariant",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "cc: results[0].functional_class",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "cc: results[0].C1",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "cc: results[0].C2",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "cc: results[0].verdict",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "cc: results[1].object",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "cc: results[1].ledger_ref",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "cc: results[1].perspective",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "cc: results[1].config_space",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "cc: results[1].invariant",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "cc: results[1].functional_class",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "cc: results[1].C1",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "cc: results[1].C2",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "cc: results[1].verdict",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "cc: results[2].object",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "cc: results[2].ledger_ref",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "cc: results[2].perspective",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "cc: results[2].config_space",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "cc: results[2].invariant",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "cc: results[2].functional_class",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "cc: results[2].C1",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "cc: results[2].C2",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "cc: results[2].verdict",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "cc: results[3].object",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "cc: results[3].ledger_ref",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "cc: results[3].perspective",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "cc: results[3].config_space",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "cc: results[3].invariant",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "cc: results[3].functional_class",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "cc: results[3].C1",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "cc: results[3].C2",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "cc: results[3].verdict",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "cc: results[4].object",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "cc: results[4].ledger_ref",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "cc: results[4].perspective",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "cc: results[4].config_space",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "cc: results[4].invariant",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "cc: results[4].functional_class",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "cc: results[4].C1",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "cc: results[4].C2",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "cc: results[4].verdict",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "cc: results[5].object",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "cc: results[5].ledger_ref",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "cc: results[5].perspective",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "cc: results[5].config_space",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "cc: results[5].invariant",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "cc: results[5].functional_class",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "cc: results[5].C1",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "cc: results[5].C2",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "cc: results[5].verdict",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "cc: memo_md5 == lock",
      "result": "PASS",
      "chat": "0039d001769569297c2aa8ccbded5a3b",
      "cc": "0039d001769569297c2aa8ccbded5a3b"
    },
    {
      "check": "C-Q-0",
      "item": "cc: memo_bytes == lock",
      "result": "PASS",
      "chat": 4863,
      "cc": 4863
    },
    {
      "check": "C-Q-0",
      "item": "cc: instrument_md5 real 32-hex",
      "result": "PASS",
      "chat": "4b1e700e3df9c1b5f51904fbf70ec219",
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "cc: no placeholder tokens",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C-Q-0",
      "item": "INDEPENDENCE: instrument_md5 differ",
      "result": "PASS",
      "chat": "79072196cdfc480f4073195d96100d2e",
      "cc": "4b1e700e3df9c1b5f51904fbf70ec219"
    },
    {
      "check": "C-Q-0",
      "item": "INDEPENDENCE: checkpoints not byte-identical",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C1",
      "item": "memo_md5",
      "result": "PASS",
      "chat": "0039d001769569297c2aa8ccbded5a3b",
      "cc": "0039d001769569297c2aa8ccbded5a3b"
    },
    {
      "check": "C1",
      "item": "memo_bytes",
      "result": "PASS",
      "chat": 4863,
      "cc": 4863
    },
    {
      "check": "C1",
      "item": "ledger_base_md5",
      "result": "PASS",
      "chat": "b4e55aaea76a2152f7b1873309aec077",
      "cc": "b4e55aaea76a2152f7b1873309aec077"
    },
    {
      "check": "C1",
      "item": "ledger_base_md5 == V4.81",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C2",
      "item": "row count",
      "result": "PASS",
      "chat": 6,
      "cc": 6
    },
    {
      "check": "C2",
      "item": "[0].object",
      "result": "PASS",
      "chat": "L_B Borromean Baryon",
      "cc": "L_B Borromean Baryon"
    },
    {
      "check": "C2",
      "item": "[0].ledger_ref",
      "result": "PASS",
      "chat": "§2.15/§2.51",
      "cc": "§2.15/§2.51"
    },
    {
      "check": "C2",
      "item": "[0].perspective",
      "result": "PASS",
      "chat": "L-Perspective",
      "cc": "L-Perspective"
    },
    {
      "check": "C2",
      "item": "[0].config_space",
      "result": "PASS",
      "chat": "Continuous",
      "cc": "Continuous"
    },
    {
      "check": "C2",
      "item": "[0].invariant",
      "result": "PASS",
      "chat": "Linking Number",
      "cc": "Linking Number"
    },
    {
      "check": "C2",
      "item": "[0].functional_class",
      "result": "PASS",
      "chat": "Rigid Constraint",
      "cc": "Rigid Constraint"
    },
    {
      "check": "C3",
      "item": "[0].C1 (L_B Borromean Baryon)",
      "result": "PASS",
      "chat": true,
      "cc": true
    },
    {
      "check": "C3",
      "item": "[0].C2 (L_B Borromean Baryon)",
      "result": "PASS",
      "chat": true,
      "cc": true
    },
    {
      "check": "C4",
      "item": "[0].verdict (L_B Borromean Baryon)",
      "result": "PASS",
      "chat": "PASS",
      "cc": "PASS"
    },
    {
      "check": "C2",
      "item": "[1].object",
      "result": "PASS",
      "chat": "K₇ Vortex",
      "cc": "K₇ Vortex"
    },
    {
      "check": "C2",
      "item": "[1].ledger_ref",
      "result": "PASS",
      "chat": "§3.4",
      "cc": "§3.4"
    },
    {
      "check": "C2",
      "item": "[1].perspective",
      "result": "PASS",
      "chat": "L-Perspective",
      "cc": "L-Perspective"
    },
    {
      "check": "C2",
      "item": "[1].config_space",
      "result": "PASS",
      "chat": "Continuous",
      "cc": "Continuous"
    },
    {
      "check": "C2",
      "item": "[1].invariant",
      "result": "PASS",
      "chat": "Fano Winding",
      "cc": "Fano Winding"
    },
    {
      "check": "C2",
      "item": "[1].functional_class",
      "result": "PASS",
      "chat": "Competing Exponents",
      "cc": "Competing Exponents"
    },
    {
      "check": "C3",
      "item": "[1].C1 (K₇ Vortex)",
      "result": "PASS",
      "chat": true,
      "cc": true
    },
    {
      "check": "C3",
      "item": "[1].C2 (K₇ Vortex)",
      "result": "PASS",
      "chat": true,
      "cc": true
    },
    {
      "check": "C4",
      "item": "[1].verdict (K₇ Vortex)",
      "result": "PASS",
      "chat": "PASS",
      "cc": "PASS"
    },
    {
      "check": "C2",
      "item": "[2].object",
      "result": "PASS",
      "chat": "Electron 2π Closure",
      "cc": "Electron 2π Closure"
    },
    {
      "check": "C2",
      "item": "[2].ledger_ref",
      "result": "PASS",
      "chat": "§2.50.A",
      "cc": "§2.50.A"
    },
    {
      "check": "C2",
      "item": "[2].perspective",
      "result": "PASS",
      "chat": "L-Perspective",
      "cc": "L-Perspective"
    },
    {
      "check": "C2",
      "item": "[2].config_space",
      "result": "PASS",
      "chat": "Continuous",
      "cc": "Continuous"
    },
    {
      "check": "C2",
      "item": "[2].invariant",
      "result": "PASS",
      "chat": "Winding Number",
      "cc": "Winding Number"
    },
    {
      "check": "C2",
      "item": "[2].functional_class",
      "result": "PASS",
      "chat": "Rigid Constraint",
      "cc": "Rigid Constraint"
    },
    {
      "check": "C3",
      "item": "[2].C1 (Electron 2π Closure)",
      "result": "PASS",
      "chat": true,
      "cc": true
    },
    {
      "check": "C3",
      "item": "[2].C2 (Electron 2π Closure)",
      "result": "PASS",
      "chat": true,
      "cc": true
    },
    {
      "check": "C4",
      "item": "[2].verdict (Electron 2π Closure)",
      "result": "PASS",
      "chat": "PASS",
      "cc": "PASS"
    },
    {
      "check": "C2",
      "item": "[3].object",
      "result": "PASS",
      "chat": "Clifford Unknot / Rule 17",
      "cc": "Clifford Unknot / Rule 17"
    },
    {
      "check": "C2",
      "item": "[3].ledger_ref",
      "result": "PASS",
      "chat": "§2.41",
      "cc": "§2.41"
    },
    {
      "check": "C2",
      "item": "[3].perspective",
      "result": "PASS",
      "chat": "L-Perspective",
      "cc": "L-Perspective"
    },
    {
      "check": "C2",
      "item": "[3].config_space",
      "result": "PASS",
      "chat": "Continuous",
      "cc": "Continuous"
    },
    {
      "check": "C2",
      "item": "[3].invariant",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C2",
      "item": "[3].functional_class",
      "result": "PASS",
      "chat": "Rigid Constraint",
      "cc": "Rigid Constraint"
    },
    {
      "check": "C3",
      "item": "[3].C1 (Clifford Unknot / Rule 17)",
      "result": "PASS",
      "chat": false,
      "cc": false
    },
    {
      "check": "C3",
      "item": "[3].C2 (Clifford Unknot / Rule 17)",
      "result": "PASS",
      "chat": true,
      "cc": true
    },
    {
      "check": "C4",
      "item": "[3].verdict (Clifford Unknot / Rule 17)",
      "result": "PASS",
      "chat": "FAIL",
      "cc": "FAIL"
    },
    {
      "check": "C2",
      "item": "[4].object",
      "result": "PASS",
      "chat": "CD Tower Rungs (e.g., 42/84)",
      "cc": "CD Tower Rungs (e.g., 42/84)"
    },
    {
      "check": "C2",
      "item": "[4].ledger_ref",
      "result": "PASS",
      "chat": "§2.31/§2.75",
      "cc": "§2.31/§2.75"
    },
    {
      "check": "C2",
      "item": "[4].perspective",
      "result": "PASS",
      "chat": "E-Perspective",
      "cc": "E-Perspective"
    },
    {
      "check": "C2",
      "item": "[4].config_space",
      "result": "PASS",
      "chat": "Discrete",
      "cc": "Discrete"
    },
    {
      "check": "C2",
      "item": "[4].invariant",
      "result": "PASS",
      "chat": "Chirality/Algebraic",
      "cc": "Chirality/Algebraic"
    },
    {
      "check": "C2",
      "item": "[4].functional_class",
      "result": "PASS",
      "chat": "None",
      "cc": "None"
    },
    {
      "check": "C3",
      "item": "[4].C1 (CD Tower Rungs (e.g., 42/84))",
      "result": "PASS",
      "chat": false,
      "cc": false
    },
    {
      "check": "C3",
      "item": "[4].C2 (CD Tower Rungs (e.g., 42/84))",
      "result": "PASS",
      "chat": false,
      "cc": false
    },
    {
      "check": "C4",
      "item": "[4].verdict (CD Tower Rungs (e.g., 42/84))",
      "result": "PASS",
      "chat": "FAIL",
      "cc": "FAIL"
    },
    {
      "check": "C2",
      "item": "[5].object",
      "result": "PASS",
      "chat": "Cluster M SLWE Matrices",
      "cc": "Cluster M SLWE Matrices"
    },
    {
      "check": "C2",
      "item": "[5].ledger_ref",
      "result": "PASS",
      "chat": "§2.58",
      "cc": "§2.58"
    },
    {
      "check": "C2",
      "item": "[5].perspective",
      "result": "PASS",
      "chat": "E-Perspective",
      "cc": "E-Perspective"
    },
    {
      "check": "C2",
      "item": "[5].config_space",
      "result": "PASS",
      "chat": "Discrete",
      "cc": "Discrete"
    },
    {
      "check": "C2",
      "item": "[5].invariant",
      "result": "PASS",
      "chat": null,
      "cc": null
    },
    {
      "check": "C2",
      "item": "[5].functional_class",
      "result": "PASS",
      "chat": "None",
      "cc": "None"
    },
    {
      "check": "C3",
      "item": "[5].C1 (Cluster M SLWE Matrices)",
      "result": "PASS",
      "chat": false,
      "cc": false
    },
    {
      "check": "C3",
      "item": "[5].C2 (Cluster M SLWE Matrices)",
      "result": "PASS",
      "chat": false,
      "cc": false
    },
    {
      "check": "C4",
      "item": "[5].verdict (Cluster M SLWE Matrices)",
      "result": "PASS",
      "chat": "FAIL",
      "cc": "FAIL"
    },
    {
      "check": "C5",
      "item": "F-QUANTA-1.state",
      "result": "PASS",
      "chat": "SILENT",
      "cc": "SILENT"
    },
    {
      "check": "C5",
      "item": "F-QUANTA-2.state",
      "result": "PASS",
      "chat": "SILENT",
      "cc": "SILENT"
    },
    {
      "check": "C5",
      "item": "F-QUANTA-3.state",
      "result": "PASS",
      "chat": "REGISTERED_NOT_EXECUTED",
      "cc": "REGISTERED_NOT_EXECUTED"
    },
    {
      "check": "C5",
      "item": "PC-1_nontrivial_partition.met",
      "result": "PASS",
      "chat": true,
      "cc": true
    },
    {
      "check": "C5",
      "item": "PC-1_nontrivial_partition.n_pass",
      "result": "PASS",
      "chat": 3,
      "cc": 3
    },
    {
      "check": "C5",
      "item": "PC-1_nontrivial_partition.n_fail",
      "result": "PASS",
      "chat": 3,
      "cc": 3
    },
    {
      "check": "C5",
      "item": "PC-2_independence_witness.met",
      "result": "PASS",
      "chat": true,
      "cc": true
    },
    {
      "check": "C5",
      "item": "PC-2 witness set",
      "result": "PASS",
      "chat": [
        "K₇ Vortex"
      ],
      "cc": [
        "K₇ Vortex"
      ]
    },
    {
      "check": "C5",
      "item": "election E-Q-1 choice letter",
      "result": "PASS",
      "chat": "b",
      "cc": "b"
    },
    {
      "check": "C5",
      "item": "election E-Q-2 choice letter",
      "result": "PASS",
      "chat": "a",
      "cc": "a"
    },
    {
      "check": "C6",
      "item": "row count",
      "result": "PASS",
      "chat": 6,
      "cc": 6
    },
    {
      "check": "C6",
      "item": "[0].object",
      "result": "PASS",
      "chat": "L_B Borromean Baryon",
      "cc": "L_B Borromean Baryon"
    },
    {
      "check": "C6",
      "item": "[0].predicted",
      "result": "PASS",
      "chat": "PASS",
      "cc": "PASS"
    },
    {
      "check": "C6",
      "item": "[0].machine",
      "result": "PASS",
      "chat": "PASS",
      "cc": "PASS"
    },
    {
      "check": "C6",
      "item": "[0].concordant",
      "result": "PASS",
      "chat": true,
      "cc": true
    },
    {
      "check": "C6",
      "item": "[1].object",
      "result": "PASS",
      "chat": "K₇ Vortex",
      "cc": "K₇ Vortex"
    },
    {
      "check": "C6",
      "item": "[1].predicted",
      "result": "PASS",
      "chat": "PASS",
      "cc": "PASS"
    },
    {
      "check": "C6",
      "item": "[1].machine",
      "result": "PASS",
      "chat": "PASS",
      "cc": "PASS"
    },
    {
      "check": "C6",
      "item": "[1].concordant",
      "result": "PASS",
      "chat": true,
      "cc": true
    },
    {
      "check": "C6",
      "item": "[2].object",
      "result": "PASS",
      "chat": "Electron 2π Closure",
      "cc": "Electron 2π Closure"
    },
    {
      "check": "C6",
      "item": "[2].predicted",
      "result": "PASS",
      "chat": "PASS",
      "cc": "PASS"
    },
    {
      "check": "C6",
      "item": "[2].machine",
      "result": "PASS",
      "chat": "PASS",
      "cc": "PASS"
    },
    {
      "check": "C6",
      "item": "[2].concordant",
      "result": "PASS",
      "chat": true,
      "cc": true
    },
    {
      "check": "C6",
      "item": "[3].object",
      "result": "PASS",
      "chat": "Clifford Unknot / Rule 17",
      "cc": "Clifford Unknot / Rule 17"
    },
    {
      "check": "C6",
      "item": "[3].predicted",
      "result": "PASS",
      "chat": "FAIL",
      "cc": "FAIL"
    },
    {
      "check": "C6",
      "item": "[3].machine",
      "result": "PASS",
      "chat": "FAIL",
      "cc": "FAIL"
    },
    {
      "check": "C6",
      "item": "[3].concordant",
      "result": "PASS",
      "chat": true,
      "cc": true
    },
    {
      "check": "C6",
      "item": "[4].object",
      "result": "PASS",
      "chat": "CD Tower Rungs (e.g., 42/84)",
      "cc": "CD Tower Rungs (e.g., 42/84)"
    },
    {
      "check": "C6",
      "item": "[4].predicted",
      "result": "PASS",
      "chat": "FAIL",
      "cc": "FAIL"
    },
    {
      "check": "C6",
      "item": "[4].machine",
      "result": "PASS",
      "chat": "FAIL",
      "cc": "FAIL"
    },
    {
      "check": "C6",
      "item": "[4].concordant",
      "result": "PASS",
      "chat": true,
      "cc": true
    },
    {
      "check": "C6",
      "item": "[5].object",
      "result": "PASS",
      "chat": "Cluster M SLWE Matrices",
      "cc": "Cluster M SLWE Matrices"
    },
    {
      "check": "C6",
      "item": "[5].predicted",
      "result": "PASS",
      "chat": "FAIL",
      "cc": "FAIL"
    },
    {
      "check": "C6",
      "item": "[5].machine",
      "result": "PASS",
      "chat": "FAIL",
      "cc": "FAIL"
    },
    {
      "check": "C6",
      "item": "[5].concordant",
      "result": "PASS",
      "chat": true,
      "cc": true
    },
    {
      "check": "C6",
      "item": "PC-3_met",
      "result": "PASS",
      "chat": true,
      "cc": true
    }
  ],
  "n_checks": 255,
  "n_miss": 0,
  "misses": [],
  "S9_triggered": false,
  "overall": "C1-C6 ALL PASS",
  "comparator": "g_quanta_compare_v1_0.py",
  "comparator_md5": "2be701be868259465525e29c79a4c621",
  "schema_md5": "05e53dbb8e8e1f7669fa12b6fc55c260",
  "chat_checkpoint_md5": "55861161748fca634534790f366380fd",
  "cc_checkpoint_md5": "ca0e69a75a521f3869726693b23e3dce"
}
=====END-EMBED name=g_quanta_twoleg_comparison.json=====

