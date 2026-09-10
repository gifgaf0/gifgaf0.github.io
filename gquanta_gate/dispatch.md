# G-QUANTA — CC LEG DISPATCH (P-4 single-file in-band; P-4.b armor; P-4.c lone delivery)

**Gate:** G-QUANTA (Topological Stability & Composite Quanta Discriminator). **Date:** September 10, 2026.
**Base ledger:** `SQT_Master_Ledger_v4_81_CANONICAL.md` md5 `b4e55aaea76a2152f7b1873309aec077`.
**Lock chain:** memo `0039d001769569297c2aa8ccbded5a3b` (4,863 B) · lock record `947768bd6d9652f5fdbeb43ceaf16502` · comparator v1.0 `2be701be868259465525e29c79a4c621` · schema v1.0 `05e53dbb8e8e1f7669fa12b6fc55c260` — all FROZEN.
**Elections (T3-immutable):** E-Q-1 **(b)** promote standalone · E-Q-2 **(a)** E-perspective envelopes / L-perspective defects, extended defects in scope.
**Chat-leg state at dispatch:** evaluate + compare EXECUTED (checkpoint `55861161748fca634534790f366380fd`, compare `a5726e1efbc2feae46e43060df0250f5`); PC-1/PC-2/PC-3 met chat-side; F-QUANTA-1 inert-by-inventory; D-Q-1 (D-T1: T1 list not supplied chat-side, author-elected).

**ACTIVATION FLAG: `ACTIVATE: G-QUANTA-CC-LEG-1`** — proceed only if this line is present verbatim.

## 0. Blindness clause (read first)

Three embeds are **QUARANTINED** (base64-armored): the chat instrument, the chat checkpoint, the chat compare file. **Do not decode them until step 4.** Your instrument is built from the memo's §2 rules and §4 table ONLY, from scratch, in your own words and structure. Your checkpoint is committed BEFORE any armor is opened; cite that commit hash as the pre-consultation checkpoint in your return. Decoding order is audited by commit ordering (G-2a-L1 precedent).

## 1. Embed inventory

| Embed | md5 | Size | Handling |
|---|---|---|---|
| `staging_memo_G_QUANTA_v2.md` | `0039d001769569297c2aa8ccbded5a3b` | 4,863 B | plain |
| `G_QUANTA_LOCK_RECORD.md` | `947768bd6d9652f5fdbeb43ceaf16502` | 5,312 B | plain |
| `g_quanta_compare_v1_0.py` | `2be701be868259465525e29c79a4c621` | 11,960 B | plain |
| `g_quanta_schema_v1_0.json` | `05e53dbb8e8e1f7669fa12b6fc55c260` | 1,615 B | plain |
| `g_quanta_chatleg.py` | `79072196cdfc480f4073195d96100d2e` | 21,156 B | QUARANTINED (base64) |
| `g_quanta_chatleg_checkpoint.json` | `55861161748fca634534790f366380fd` | 4,605 B | QUARANTINED (base64) |
| `g_quanta_chatleg_compare.json` | `a5726e1efbc2feae46e43060df0250f5` | 1,333 B | QUARANTINED (base64) |

## 2. Verify-then-build

Save this file as `dispatch.md`, then run the extractor below **without** `--decode-quarantined`:

```python
import base64, hashlib, re, sys
src = open(sys.argv[1], 'rb').read()
pat = re.compile(rb'=====BEGIN-EMBED name=(\S+) md5=([0-9a-f]{32}) bytes=(\d+) encoding=(raw|base64)(?: armor_bytes=(\d+))?[^\n]*\n')
pos = 0
while True:
    m = pat.search(src, pos)
    if not m: break
    name, want, n, enc, armor = m.group(1).decode(), m.group(2).decode(), int(m.group(3)), m.group(4).decode(), m.group(5)
    start = m.end()
    if enc == 'raw':
        payload = src[start:start + n]
    else:
        if '--decode-quarantined' not in sys.argv:
            print(f'SKIP {name} (quarantined; not decoded)'); pos = start; continue
        payload = base64.decodebytes(src[start:start + int(armor)])
    got = hashlib.md5(payload).hexdigest()
    assert got == want and len(payload) == n, f'{name}: md5 {got} != {want} or length {len(payload)} != {n}'
    open(name, 'wb').write(payload); print(f'OK   {name}  {got}  {n:,} B'); pos = start
```

`python3 extract.py dispatch.md` → four `OK` lines (memo, lock record, comparator, schema) and three `SKIP` lines. Any assertion failure → HALT, report the md5 seen, do not build.

## 3. Build and run (blind)

1. Read `staging_memo_G_QUANTA_v2.md` §2 (C1, C2), §4 (inventory), §5 (hypotheses), §6 (falsifiers) and `G_QUANTA_LOCK_RECORD.md` §4 (PC-1/PC-2/PC-3, O-1).
2. Write `g_quanta_ccleg.py` from scratch. Requirements: md5-guard the memo against `0039d001769569297c2aa8ccbded5a3b` / 4,863 B before reading; parse the §4 table **at run time** (no hand-copied rows); C1 := ConfigSpace == Continuous AND InvariantType ≠ None (a non-None invariant over a Discrete space is NO); C2 := FunctionalClass ∈ {Rigid Constraint, Competing Exponents}; PASS := C1 ∧ C2; F-QUANTA-1 fires on FunctionalClass == Single Exponent; F-QUANTA-2 fires on any row whose Object contains `Tower` with C1 ∧ C2; F-QUANTA-3 state `REGISTERED_NOT_EXECUTED`; PC-1 := ≥1 PASS ∧ ≥1 FAIL; PC-2 := ≥1 PASS with FunctionalClass ≠ Rigid Constraint (witness list). No verdict text may appear in the instrument source. Requested variation (independence upgrade): implement C1/C2 by a second, structurally different route (e.g. a lookup table over the (ConfigSpace, InvariantType≠None, FunctionalClass) triple) and assert both routes agree per row.
3. T1: if you hold the T1 forbidden-string list (`04438b74`, 13 lines), self-grep instrument + memo + checkpoint at every invocation and report `CLEAN`; if not, record `D-T1 (CC)` in the checkpoint. Report hits by pattern index only, never by text.
4. Emit `g_quanta_ccleg_checkpoint.json` conforming to `g_quanta_schema_v1_0.json` (required_keys, result_keys, value domains; `invariant` is `null` for a trivial/absent invariant; `leg` = `cc`; real `instrument_md5`; no placeholders). **Commit** with the checkpoint md5 in the commit message. This is the pre-consultation checkpoint.
5. Emit `g_quanta_ccleg_compare.json` (your own §5 comparison: rows with `object`, `predicted`, `machine`, `concordant`; `PC-3_met`). Comparison is the LAST computation (Eddington quarantine).

## 4. Consult and compare

Only now: `python3 extract.py dispatch.md --decode-quarantined`, then

```
python3 g_quanta_compare_v1_0.py compare --chat g_quanta_chatleg_checkpoint.json --cc g_quanta_ccleg_checkpoint.json \
  --chat-cmp g_quanta_chatleg_compare.json --cc-cmp g_quanta_ccleg_compare.json --schema g_quanta_schema_v1_0.json \
  --out g_quanta_twoleg_comparison.json
```

Expected on a clean two-leg: `C1-C6 ALL PASS`. Any MISS is an S9 item: classify representational vs definitional in your return; do NOT edit either checkpoint to make it pass. The comparator and schema are frozen — if you believe the comparator is wrong, say so in H-CC and leave it unchanged.

## 5. Return (single file, P-4 mirrored)

One markdown file containing byte-exact embeds (same sentinel format) of: `g_quanta_ccleg.py`, `g_quanta_ccleg_checkpoint.json`, `g_quanta_ccleg_compare.json`, `g_quanta_twoleg_comparison.json`; plus the branch name and commit hashes (pre-consultation checkpoint commit first), the CC design register CC-DD-1..n, honesty items H-CC-1..n (self-caught bugs, halts), deviations, and the T1 state. Byte-label every artifact.

## 6. Deviations carried from the chat leg (for the record)

- **D-Q-1** — D-T1: T1 list not supplied chat-side (author-elected); chat self-grep state `LIST_ABSENT`.
- **D-Q-2** — cosmetic: chat instrument emits a Python `DeprecationWarning` (`datetime.utcnow`); no effect on any value; instrument left untouched (md5 preserved).
- **D-Q-3** — comparator v1.0 frozen AFTER the chat checkpoint was emitted (directive order); mitigated by 10 adversarial suites (verdict flip, criterion flip, class swap, falsifier state, witness set, placeholder md5, election letter, independence, missing compare) and a chat-vs-chat sanity run (255 checks, exactly the two INDEPENDENCE misses).

## 7. Embeds

=====BEGIN-EMBED name=staging_memo_G_QUANTA_v2.md md5=0039d001769569297c2aa8ccbded5a3b bytes=4863 encoding=raw=====
# STAGING MEMO — Gate G-QUANTA (Topological Stability & Composite Quanta Discriminator)

**Date:** September 10, 2026. **Base:** `SQT_Master_Ledger_v4_81_CANONICAL.md` (md5 `b4e55aaea76a2152f7b1873309aec077`). **Status: DRAFT — NOT LOCKED.** 

## 1. Object and Scope
To operationalize the "topological stability" concept as a machine-checkable discriminator across the framework's existing inventory, distinguishing genuine physical quanta (which possess an energy minimum preventing Derrick-collapse) from combinatorial labels. 

## 2. The Discriminator (Operational Definition)
An object in the framework is classified as a **STABLE QUANTUM** if and only if it satisfies TWO independent criteria:
1. **Continuous Topological Charge (C1):** It carries a conserved invariant under continuous deformation within a continuous configuration space (e.g., linking number, winding number, Hopf charge). Discrete group labels over discrete spaces evaluate to NO.
2. **Derrick-Evading Functional (C2):** Its configuration minimizes an energy functional that prevents dilation collapse/explosion via either:
    *   (a) Two terms with *competing dilation scaling exponents*.
    *   (b) A *rigid geometric constraint* (e.g., tube thickness τ ≥ 1).

## 3. Dimension, Perspective, and Functional Inventory (Imports)
Derrick's theorem is dimension-dependent. The rule evaluates objects within their locked perspective: the **E-Perspective (3D continuum effective field theory)** or the **L-Perspective (2D/3D discrete substrate)**. 

The framework's recognized C2-compliant functionals are:
*   **Ropelength (L_B):** Line tension vs. rigid thickness constraint (Gehring criticality).
*   **Gross-Pitaevskii (GP):** Gradient kinetic energy vs. interaction potential (setting a core-size healing length).

## 4. Instrument Encoding (The Execution Leg)
The instrument will ingest the following V4.81 inventory matrix and evaluate C1 and C2 for each object. A `PASS` requires `C1 == True AND C2 == True`. 

| Object | Ledger Ref | Perspective | Config Space | Invariant Type | Functional Class |
| :--- | :--- | :--- | :--- | :--- | :--- |
| L_B Borromean Baryon | §2.15/§2.51 | L-Perspective | Continuous | Linking Number | Rigid Constraint |
| K₇ Vortex | §3.4 | L-Perspective | Continuous | Fano Winding | Competing Exponents (GP) |
| Electron 2π Closure | §2.50.A | L-Perspective | Continuous | Winding Number | Rigid Constraint |
| Clifford Unknot / Rule 17 | §2.41 | L-Perspective | Continuous | None (Trivial Knot) | Rigid Constraint |
| CD Tower Rungs (e.g., 42/84) | §2.31/§2.75 | E-Perspective | Discrete | Chirality/Algebraic | None |
| Cluster M SLWE Matrices | §2.58 | E-Perspective | Discrete | None | None |

## 5. Hypotheses (M-Naive Expectations - NOT VERDICTS)
*Predicted* outcomes of the machine evaluation (H-Q-1..6):
*   **L_B Borromean Baryon:** PASS.
*   **K₇ Vortex (Independence Witness):** PASS. Validates the rule independently of ropelength, passing via the GP functional.
*   **Electron 2π Closure:** PASS. 
*   **Clifford Unknot:** FAIL. Evaluates to C1=False (an unknot can continuously deform to a point without topological obstruction).
*   **CD Tower Rungs:** FAIL. Evaluates to C1=False (configuration space is discrete, isolating its invariant from continuous deformation).
*   **SLWE Matrices:** FAIL (C1=False, C2=False).

## 6. Falsifiers
*   **F-QUANTA-1:** The instrument finds a stable finite-size object in the V4.81 ledger whose governing energy functional has only one scaling behavior under dilation and lacks a rigid constraint. (Contradicts Derrick).
*   **F-QUANTA-2:** The instrument finds a level in the combinatorial tower (e.g., 84) carrying a conserved continuous topological charge coupled with a competing-term energy bound. (Falsifies the Label/Quantum separation).
*   **F-QUANTA-3 (Dimensionless Binding - [REGISTERED, NOT EXECUTED]):** Any proposed framework level whose dimensionless binding energy ratio ($E_{binding} / E_{rest}$) approaches $\mathcal{O}(1)$ relative to the level below it fails to separate by scale and cannot be classified as a distinct composite quantum. *Note: Unexecutable at this gate as no derived $E_{binding}$ exists in the framework yet. Tests scale separation (§3), not the stability discriminator.*

## 7. Elections Requested (T3-Immutable on Lock)
*   **E-Q-1 (Promotion Path):** **(b) Promote standalone.** (The companion memo shares only the type-(b) tower claim, which is independently tested here).
*   **E-Q-2 (Dimension Perspective):** **(a) Lock E-perspective (3D) for envelopes and L-perspective (2D/3D) for defects.** *Note: This explicitly places infinite-energy extended defects (e.g., vortices) into scope, as their finite core sizes are stabilized by the GP gradient-vs-interaction balance, satisfying C2 without requiring finite total global energy.*
=====END-EMBED name=staging_memo_G_QUANTA_v2.md=====

=====BEGIN-EMBED name=G_QUANTA_LOCK_RECORD.md md5=947768bd6d9652f5fdbeb43ceaf16502 bytes=5312 encoding=raw=====
# LOCK RECORD — Gate G-QUANTA (Topological Stability & Composite Quanta Discriminator)

**Locked:** September 10, 2026 (chat leg). **Author authorization (verbatim):** "I explicitly AUTHORIZE the lock of `staging_memo_G_QUANTA_v2.md`".
**Base:** `SQT_Master_Ledger_v4_81_CANONICAL.md`, md5 `b4e55aaea76a2152f7b1873309aec077`.

## 1. Frozen artifact of record

| Artifact | md5 | Size |
|---|---|---|
| `staging_memo_G_QUANTA_v2.md` | `0039d001769569297c2aa8ccbded5a3b` | 4,863 B (50 lines) |

sha256 `9979e933ddbe7ab6d3b554b1773397458ad86062ef6c157244c16dcf69b564ef`.

Frozen byte-for-byte from the author-supplied text of September 10. The file in this estate is the artifact of record; if the author's local copy hashes differently, this md5 governs and the local copy is superseded (D5 lesson from G-TSH1: the locked artifact travels in-band).

The memo's own status line still reads `DRAFT — NOT LOCKED`; that line is inside the frozen bytes and is superseded by this record. No re-lock.

## 2. Elections (T3-immutable)

- **E-Q-1 (Promotion Path): (b) Promote standalone.** The graded-base companion memo shares only the type-(b) tower claim, which this gate tests independently.
- **E-Q-2 (Dimension Perspective): (a) E-perspective (3D) for envelopes, L-perspective (2D/3D) for defects.** Extended (infinite-total-energy) defects are explicitly in scope: C2 is satisfied by a finite core size from the GP gradient-vs-interaction balance, without requiring finite global energy.

## 3. What the lock fixes

- §2 discriminator: C1 (continuous topological charge over a continuous configuration space; discrete labels over discrete spaces = NO) and C2 (Derrick-evading functional: competing dilation exponents, or a rigid geometric constraint). PASS ⇔ C1 ∧ C2.
- §3 functional inventory: Ropelength (rigid constraint), Gross–Pitaevskii (competing exponents). Nothing else qualifies at this gate.
- §4 inventory matrix: six rows, six encoded columns. **This table is the sole input to the instrument.** No verdict text exists anywhere in the memo §4 or in the instrument.
- §5 hypotheses H-Q-1..6: predictions only, quarantined from evaluation; consulted only in the `compare` step, which runs last (Eddington quarantine).
- §6 falsifiers: F-QUANTA-1 (single-scaling stable object), F-QUANTA-2 (tower rung with continuous charge + competing-term bound), F-QUANTA-3 **REGISTERED, NOT EXECUTED**.

## 4. Lock-record annotations (not memo text; author may strike before the leg runs)

Promotion conditions carried from the September 10 review and accepted in the directive:

- **PC-1 non-trivial partition:** ≥ 1 PASS and ≥ 1 FAIL.
- **PC-2 independence witness:** ≥ 1 PASS via a functional class other than the ropelength class (Rigid Constraint), so the rule is not a restatement of L_B.
- **PC-3 concordance:** machine verdicts vs H-Q-1..6, evaluated in the separate `compare` step; any discordance is a finding (demotion or a hole in the rule), not a promotion.

**O-1 (observation, no verdict effect):** the two Discrete-space rows (tower rungs, SLWE matrices) are assigned E-Perspective, which §3 defines as the 3D continuum EFT. C1 fails on `Discrete` regardless of perspective, so the verdicts are unaffected; recorded for an optional amendment.

**F-QUANTA-1 is inert-by-inventory:** the locked table declares no `Single Exponent` functional class, so F-1 cannot fire on this run. Its silence is not a test passed and will be reported as such.

## 5. Instrument (chat leg)

| Artifact | md5 | Size | State |
|---|---|---|---|
| `g_quanta_chatleg.py` v1 | `79072196cdfc480f4073195d96100d2e` | 21,156 B | self-tests 9/9 GREEN; **evaluation of record NOT run** |

Behaviour: md5-guards the memo against the lock before reading (verified: a one-byte tamper halts with exit 1, no checkpoint written); T1 self-grep of instrument + memo before evaluation and of the checkpoint after; parses §4 at run time; vocabulary-locked (unknown class/space → halt); writes E8 JSON checkpoint `g_quanta_chatleg_checkpoint.json`; `compare` writes a separate `g_quanta_chatleg_compare.json` and never modifies the checkpoint.

Self-test suites: S1 parser/normalisation · S2 C1/C2 truth table (7 cases) · S3 F-QUANTA-2 firing · S4 F-QUANTA-1 firing + inert flag · S5 PC-1/PC-2 · S6 vocabulary lock · S7 md5 guard · S8 hypothesis match · S9 T1 scan mechanics.

**T1 requirement:** the run of record needs the T1 forbidden-string list (13 pattern lines, md5 `04438b74`, per the G-2a-L1 estate) supplied as `T1_forbidden_strings.txt` beside the memo, or via `--t1 PATH`. Without it the instrument halts; `--no-t1-halt` records deviation D-T1 instead. Hits are reported by pattern index, never by text.

## 6. Execution order from here

1. Author supplies the T1 list (or elects D-T1).
2. Author word to execute → `python3 g_quanta_chatleg.py evaluate` → checkpoint md5 reported.
3. `python3 g_quanta_chatleg.py compare` (PC-3), last.
4. P-4 single-file in-band CC dispatch: memo + lock record + instrument + T1 list as byte-exact embeds; CC leg blind, own implementation of the §2 rules.
5. Two-leg comparison C1–C6; S9 on any miss.
6. Fold authorization → V4.82 (after V4.81 is in project knowledge).

Nothing has been evaluated. No checkpoint exists. No prior ledger content touched.
=====END-EMBED name=G_QUANTA_LOCK_RECORD.md=====

=====BEGIN-EMBED name=g_quanta_compare_v1_0.py md5=2be701be868259465525e29c79a4c621 bytes=11960 encoding=raw=====
#!/usr/bin/env python3
"""g_quanta_compare_v1_0.py -- Gate G-QUANTA two-leg comparator, v1.0 (FROZEN September 10, 2026).

Usage
  compare  --chat CK --cc CK [--chat-cmp CMP --cc-cmp CMP] [--schema g_quanta_schema_v1_0.json] [--out OUT]
  selftest

Checks (every verdict-bearing quantity is a boolean or a short label -> EXACT identity;
free text is NEVER compared -- lesson H-S5 / H-W-6):
  C-Q-0  provenance: required keys per schema; memo_md5 == lock on both legs; instrument_md5 is a
         real 32-hex md5 on both legs; NO placeholder tokens; INDEPENDENCE WITNESS: the two
         instrument_md5 values differ and the two checkpoints are not byte-identical
  C1     lock identity: memo_md5 / memo_bytes / ledger_base_md5 identical on both legs
  C2     inventory identity: same objects in the same order; ledger_ref, perspective, config_space,
         invariant, functional_class identical per object
  C3     criteria identity: per-object C1 and C2 booleans identical
  C4     verdict identity: per-object PASS/FAIL identical
  C5     falsifier + promotion-condition identity: F-QUANTA-1/2/3 states; PC-1 met/n_pass/n_fail;
         PC-2 met + witness SET
  C6     compare-step identity (when both compare files supplied): per-row predicted/machine/
         concordant identical; PC-3_met identical. Elections compared by choice letter only.
Any MISS -> S9 counter-cross-check. Representational vs definitional classification is a
human step after the machine report; this file only reports.
"""
import argparse, hashlib, json, os, re, sys, copy, tempfile

MEMO_LOCK_MD5 = '0039d001769569297c2aa8ccbded5a3b'
MEMO_LOCK_BYTES = 4863
LEDGER_BASE_MD5 = 'b4e55aaea76a2152f7b1873309aec077'
PLACEHOLDER_TOKENS = ('TBD', 'PLACEHOLDER', 'xxxx', 'XXXX', '<', '>')
HEX32 = re.compile(r'^[0-9a-f]{32}$')
SCHEMA_DEFAULT = 'g_quanta_schema_v1_0.json'


def md5f(p): return hashlib.md5(open(p, 'rb').read()).hexdigest()


def getpath(d, dotted):
    cur = d
    for k in dotted.split('.'):
        if not isinstance(cur, dict) or k not in cur:
            return None, False
        cur = cur[k]
    return cur, True


def choice_letter(s):
    m = re.match(r'\s*\(([a-z])\)', str(s))
    return m.group(1) if m else None


def run_checks(chat, cc, schema, chat_cmp=None, cc_cmp=None, chat_bytes=None, cc_bytes=None):
    R = []

    def rec(check, item, ok, chat_v=None, cc_v=None):
        R.append({'check': check, 'item': item, 'result': 'PASS' if ok else 'MISS',
                  'chat': chat_v, 'cc': cc_v})

    # ---- C-Q-0 provenance
    for leg, ck in (('chat', chat), ('cc', cc)):
        for key in schema['required_keys']:
            _, present = getpath(ck, key)
            rec('C-Q-0', f'{leg}: required key {key}', present)
        for i, r in enumerate(ck.get('results', [])):
            for key in schema['result_keys']:
                rec('C-Q-0', f'{leg}: results[{i}].{key}', key in r)
        rec('C-Q-0', f'{leg}: memo_md5 == lock', ck.get('memo_md5') == MEMO_LOCK_MD5, ck.get('memo_md5'), MEMO_LOCK_MD5)
        rec('C-Q-0', f'{leg}: memo_bytes == lock', ck.get('memo_bytes') == MEMO_LOCK_BYTES, ck.get('memo_bytes'), MEMO_LOCK_BYTES)
        rec('C-Q-0', f'{leg}: instrument_md5 real 32-hex', bool(HEX32.match(str(ck.get('instrument_md5', '')))), ck.get('instrument_md5'))
        flat = json.dumps(ck, ensure_ascii=False)
        rec('C-Q-0', f'{leg}: no placeholder tokens', not any(t in flat for t in PLACEHOLDER_TOKENS if t not in '<>')
            and not re.search(r'<[a-z_ ]+>', flat))
    rec('C-Q-0', 'INDEPENDENCE: instrument_md5 differ', chat.get('instrument_md5') != cc.get('instrument_md5'),
        chat.get('instrument_md5'), cc.get('instrument_md5'))
    if chat_bytes is not None and cc_bytes is not None:
        rec('C-Q-0', 'INDEPENDENCE: checkpoints not byte-identical', chat_bytes != cc_bytes)

    # ---- C1 lock identity
    for key in ('memo_md5', 'memo_bytes', 'ledger_base_md5'):
        rec('C1', key, chat.get(key) == cc.get(key), chat.get(key), cc.get(key))
    rec('C1', 'ledger_base_md5 == V4.81', chat.get('ledger_base_md5') == LEDGER_BASE_MD5 == cc.get('ledger_base_md5'))

    # ---- C2 inventory identity
    a, b = chat.get('results', []), cc.get('results', [])
    rec('C2', 'row count', len(a) == len(b), len(a), len(b))
    for i, (ra, rb) in enumerate(zip(a, b)):
        for key in ('object', 'ledger_ref', 'perspective', 'config_space', 'invariant', 'functional_class'):
            rec('C2', f'[{i}].{key}', ra.get(key) == rb.get(key), ra.get(key), rb.get(key))
        # ---- C3 criteria, C4 verdict
        for key in ('C1', 'C2'):
            rec('C3', f'[{i}].{key} ({ra.get("object")})', ra.get(key) is rb.get(key) and isinstance(ra.get(key), bool),
                ra.get(key), rb.get(key))
        rec('C4', f'[{i}].verdict ({ra.get("object")})', ra.get('verdict') == rb.get('verdict') and ra.get('verdict') in ('PASS', 'FAIL'),
            ra.get('verdict'), rb.get('verdict'))

    # ---- C5 falsifiers + PCs
    for f in ('F-QUANTA-1', 'F-QUANTA-2', 'F-QUANTA-3'):
        va, _ = getpath(chat, f'falsifiers.{f}.state'); vb, _ = getpath(cc, f'falsifiers.{f}.state')
        rec('C5', f'{f}.state', va == vb and va is not None, va, vb)
    for key in ('PC-1_nontrivial_partition.met', 'PC-1_nontrivial_partition.n_pass',
                'PC-1_nontrivial_partition.n_fail', 'PC-2_independence_witness.met'):
        va, _ = getpath(chat, f'promotion_conditions.{key}'); vb, _ = getpath(cc, f'promotion_conditions.{key}')
        rec('C5', key, va == vb and va is not None, va, vb)
    wa, _ = getpath(chat, 'promotion_conditions.PC-2_independence_witness.witnesses')
    wb, _ = getpath(cc, 'promotion_conditions.PC-2_independence_witness.witnesses')
    rec('C5', 'PC-2 witness set', set(wa or []) == set(wb or []) and wa is not None, wa, wb)
    for e in ('E-Q-1', 'E-Q-2'):
        la, lb = choice_letter((chat.get('elections') or {}).get(e)), choice_letter((cc.get('elections') or {}).get(e))
        rec('C5', f'election {e} choice letter', la == lb and la is not None, la, lb)

    # ---- C6 compare step
    if chat_cmp is not None and cc_cmp is not None:
        ra, rb = chat_cmp.get('rows', []), cc_cmp.get('rows', [])
        rec('C6', 'row count', len(ra) == len(rb), len(ra), len(rb))
        for i, (x, y) in enumerate(zip(ra, rb)):
            for key in ('object', 'predicted', 'machine', 'concordant'):
                rec('C6', f'[{i}].{key}', x.get(key) == y.get(key), x.get(key), y.get(key))
        rec('C6', 'PC-3_met', chat_cmp.get('PC-3_met') is cc_cmp.get('PC-3_met') and isinstance(chat_cmp.get('PC-3_met'), bool),
            chat_cmp.get('PC-3_met'), cc_cmp.get('PC-3_met'))
    else:
        rec('C6', 'compare files supplied', False, chat_cmp is not None, cc_cmp is not None)

    misses = [r for r in R if r['result'] == 'MISS']
    return {'checks': R, 'n_checks': len(R), 'n_miss': len(misses), 'misses': misses,
            'S9_triggered': bool(misses), 'overall': 'C1-C6 ALL PASS' if not misses else 'MISS -> S9'}


def cmd_compare(a):
    schema = json.load(open(a.schema, encoding='utf-8'))
    cb, ccb = open(a.chat, 'rb').read(), open(a.cc, 'rb').read()
    chat, cc = json.loads(cb), json.loads(ccb)
    chat_cmp = json.load(open(a.chat_cmp, encoding='utf-8')) if a.chat_cmp else None
    cc_cmp = json.load(open(a.cc_cmp, encoding='utf-8')) if a.cc_cmp else None
    out = run_checks(chat, cc, schema, chat_cmp, cc_cmp, cb, ccb)
    out.update({'comparator': os.path.basename(__file__), 'comparator_md5': md5f(os.path.abspath(__file__)),
                'schema_md5': md5f(a.schema), 'chat_checkpoint_md5': hashlib.md5(cb).hexdigest(),
                'cc_checkpoint_md5': hashlib.md5(ccb).hexdigest()})
    json.dump(out, open(a.out, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    for m in out['misses']:
        print(f'MISS {m["check"]:6} {m["item"]}  chat={m["chat"]!r} cc={m["cc"]!r}')
    print(f'{out["overall"]}  ({out["n_checks"]} checks, {out["n_miss"]} miss)  -> {a.out} {md5f(a.out)}')


# ---------------------------------------------------------------------- selftest
def _synthetic():
    rows = [('A', 'Continuous', 'Linking Number', 'Rigid Constraint', True, True, 'PASS'),
            ('K', 'Continuous', 'Fano Winding', 'Competing Exponents', True, True, 'PASS'),
            ('CD Tower', 'Discrete', None, 'None', False, False, 'FAIL')]
    ck = {'gate': 'G-QUANTA', 'leg': 'chat', 'instrument': 'x.py', 'instrument_md5': 'a' * 32,
          'memo': 'm', 'memo_md5': MEMO_LOCK_MD5, 'memo_bytes': MEMO_LOCK_BYTES,
          'ledger_base_md5': LEDGER_BASE_MD5, 'elections': {'E-Q-1': '(b) x', 'E-Q-2': '(a) y'},
          'utc': 't', 'inventory_rows': 3,
          'results': [{'object': o, 'ledger_ref': '§', 'perspective': 'L-Perspective', 'config_space': cs,
                       'invariant': inv, 'functional_class': fc, 'C1': c1, 'C2': c2, 'verdict': v}
                      for o, cs, inv, fc, c1, c2, v in rows],
          'falsifiers': {'F-QUANTA-1': {'state': 'SILENT'}, 'F-QUANTA-2': {'state': 'SILENT'},
                         'F-QUANTA-3': {'state': 'REGISTERED_NOT_EXECUTED'}},
          'promotion_conditions': {'PC-1_nontrivial_partition': {'met': True, 'n_pass': 2, 'n_fail': 1},
                                   'PC-2_independence_witness': {'met': True, 'witnesses': ['K']}}}
    cmp_ = {'rows': [{'object': 'A', 'predicted': 'PASS', 'machine': 'PASS', 'concordant': True}], 'PC-3_met': True}
    return ck, cmp_


def cmd_selftest(a):
    schema = json.load(open(a.schema, encoding='utf-8'))
    ck, cmp_ = _synthetic()
    cc = copy.deepcopy(ck); cc['leg'] = 'cc'; cc['instrument_md5'] = 'b' * 32
    cc['elections'] = {'E-Q-1': '(b) standalone (CC wording)', 'E-Q-2': '(a) defects in scope (CC wording)'}
    base = run_checks(ck, cc, schema, cmp_, copy.deepcopy(cmp_), b'chat', b'cc')
    assert base['n_miss'] == 0, base['misses']
    print('  green  S1 identical legs (different wording, different md5) -> ALL PASS')

    def expect_miss(name, mutate, check):
        c2 = copy.deepcopy(cc); mutate(c2)
        out = run_checks(ck, c2, schema, cmp_, copy.deepcopy(cmp_), b'chat', b'cc2')
        assert any(m['check'] == check for m in out['misses']), (name, out['misses'])
        print(f'  green  {name} -> fires {check}')

    expect_miss('S2 verdict flip', lambda c: c['results'][0].update(verdict='FAIL'), 'C4')
    expect_miss('S3 criterion flip', lambda c: c['results'][1].update(C2=False), 'C3')
    expect_miss('S4 functional class swap', lambda c: c['results'][1].update(functional_class='Rigid Constraint'), 'C2')
    expect_miss('S5 falsifier state', lambda c: c['falsifiers']['F-QUANTA-2'].update(state='FIRES'), 'C5')
    expect_miss('S6 witness set', lambda c: c['promotion_conditions']['PC-2_independence_witness'].update(witnesses=['A']), 'C5')
    expect_miss('S7 placeholder md5', lambda c: c.update(instrument_md5='<fill>'), 'C-Q-0')
    expect_miss('S8 election letter', lambda c: c['elections'].update({'E-Q-1': '(a) joint'}), 'C5')
    expect_miss('S9 independence (same instrument md5)', lambda c: c.update(instrument_md5='a' * 32), 'C-Q-0')
    out = run_checks(ck, cc, schema, cmp_, None, b'chat', b'cc')
    assert any(m['check'] == 'C6' for m in out['misses'])
    print('  green  S10 missing compare file -> C6 MISS')
    print(f'ALL 10/10 SUITES GREEN  (comparator {md5f(os.path.abspath(__file__))})')


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('cmd', choices=['compare', 'selftest'])
    p.add_argument('--chat'); p.add_argument('--cc')
    p.add_argument('--chat-cmp'); p.add_argument('--cc-cmp')
    p.add_argument('--schema', default=SCHEMA_DEFAULT)
    p.add_argument('--out', default='g_quanta_twoleg_comparison.json')
    a = p.parse_args()
    {'compare': cmd_compare, 'selftest': cmd_selftest}[a.cmd](a)


if __name__ == '__main__':
    main()
=====END-EMBED name=g_quanta_compare_v1_0.py=====

=====BEGIN-EMBED name=g_quanta_schema_v1_0.json md5=05e53dbb8e8e1f7669fa12b6fc55c260 bytes=1615 encoding=raw=====
{
  "gate": "G-QUANTA",
  "schema_version": "1.0",
  "frozen": "2026-09-10",
  "required_keys": [
    "gate", "leg", "instrument", "instrument_md5", "memo", "memo_md5", "memo_bytes",
    "ledger_base_md5", "elections.E-Q-1", "elections.E-Q-2", "utc", "inventory_rows", "results",
    "falsifiers.F-QUANTA-1.state", "falsifiers.F-QUANTA-2.state", "falsifiers.F-QUANTA-3.state",
    "promotion_conditions.PC-1_nontrivial_partition.met",
    "promotion_conditions.PC-1_nontrivial_partition.n_pass",
    "promotion_conditions.PC-1_nontrivial_partition.n_fail",
    "promotion_conditions.PC-2_independence_witness.met",
    "promotion_conditions.PC-2_independence_witness.witnesses"
  ],
  "result_keys": [
    "object", "ledger_ref", "perspective", "config_space", "invariant", "functional_class",
    "C1", "C2", "verdict"
  ],
  "compare_file_keys": ["rows", "PC-3_met"],
  "compare_row_keys": ["object", "predicted", "machine", "concordant"],
  "value_domains": {
    "perspective": ["L-Perspective", "E-Perspective"],
    "config_space": ["Continuous", "Discrete"],
    "functional_class": ["Rigid Constraint", "Competing Exponents", "Single Exponent", "None"],
    "verdict": ["PASS", "FAIL"],
    "falsifier_state": ["FIRES", "SILENT", "REGISTERED_NOT_EXECUTED"]
  },
  "notes": [
    "invariant is null for a trivial/absent invariant (the memo's 'None (Trivial Knot)').",
    "Free text (reasons, notes, election wording) is never compared; elections compare by choice letter only.",
    "Optional keys (T1_pre_evaluation, T1_post_write, C1_reason, C2_reason, design register) are reported, not compared."
  ]
}
=====END-EMBED name=g_quanta_schema_v1_0.json=====

=====BEGIN-EMBED name=g_quanta_chatleg.py md5=79072196cdfc480f4073195d96100d2e bytes=21156 encoding=base64 armor_bytes=28580 QUARANTINED=====
IyEvdXNyL2Jpbi9lbnYgcHl0aG9uMwoiIiJnX3F1YW50YV9jaGF0bGVnLnB5IC0tIEdhdGUgRy1R
VUFOVEEgY2hhdC1sZWcgaW5zdHJ1bWVudCwgdjEgKFNlcHRlbWJlciAxMCwgMjAyNikuCgpFdmFs
dWF0ZXMgdGhlIExPQ0tFRCBzZWN0aW9uLTQgaW52ZW50b3J5IG9mIHN0YWdpbmdfbWVtb19HX1FV
QU5UQV92Mi5tZCBhZ2FpbnN0IHRoZQpzZWN0aW9uLTIgZGlzY3JpbWluYXRvciAoQzEsIEMyKS4g
VGhpcyBmaWxlIGNvbnRhaW5zIE5PIHBlci1vYmplY3QgdmVyZGljdDogZXZlcnkKUEFTUy9GQUlM
IGlzIGNvbXB1dGVkIGF0IHJ1biB0aW1lIGZyb20gdGhlIGVuY29kZWQgY29sdW1ucyBvZiB0aGUg
bWVtbyB0YWJsZSwgd2hpY2gKaXMgbWQ1LWd1YXJkZWQgYWdhaW5zdCB0aGUgbG9jayBiZWZvcmUg
aXQgaXMgcmVhZC4KClN1YmNvbW1hbmRzCiAgc2VsZnRlc3QgICBpbnRlcm5hbCBzdWl0ZXMgb24g
c3ludGhldGljIHRhYmxlcyAobm8gbWVtbyByZWFkLCBubyBjaGVja3BvaW50IHdyaXR0ZW4pCiAg
ZXZhbHVhdGUgICBtZDUtZ3VhcmQgbWVtbyAtPiBUMSBzZWxmLWdyZXAgLT4gcGFyc2Ugc2VjdGlv
biA0IC0+IGV2YWx1YXRlIC0+IGNoZWNrcG9pbnQKICBjb21wYXJlICAgIHJ1biBMQVNUIChFZGRp
bmd0b24gcXVhcmFudGluZSk6IGNoZWNrcG9pbnQgdnMgc2VjdGlvbi01IGh5cG90aGVzZXMsCiAg
ICAgICAgICAgICB3cml0dGVuIHRvIGEgU0VQQVJBVEUgYXJ0aWZhY3Q7IHRoZSB2ZXJkaWN0IGNo
ZWNrcG9pbnQgaXMgbmV2ZXIgbW9kaWZpZWQKCkVuY29kaW5nIHJ1bGVzICh0cmFuc2NyaWJlZCBm
cm9tIG1lbW8gc2VjdGlvbiAyOyB0aGUgb25seSBsb2dpYyBpbiB0aGlzIGZpbGUpCiAgQzEgIDo9
IENvbmZpZ1NwYWNlID09IENvbnRpbnVvdXMgQU5EIEludmFyaWFudFR5cGUgIT0gTm9uZQogICAg
ICAgICAoYSBub24tTm9uZSBpbnZhcmlhbnQgb3ZlciBhIERpc2NyZXRlIHNwYWNlIGV2YWx1YXRl
cyB0byBOTywgcGVyIHNlY3Rpb24gMikKICBDMiAgOj0gRnVuY3Rpb25hbENsYXNzIGluIHtSaWdp
ZCBDb25zdHJhaW50LCBDb21wZXRpbmcgRXhwb25lbnRzfQogIFBBU1MgOj0gQzEgQU5EIEMyCkZh
bHNpZmllcnMKICBGLVFVQU5UQS0xICBmaXJlcyBvbiBhbnkgcm93IG9mIEZ1bmN0aW9uYWxDbGFz
cyA9PSBTaW5nbGUgRXhwb25lbnQKICAgICAgICAgICAgICAoc2luZ2xlIGRpbGF0aW9uIHNjYWxp
bmcsIG5vIGNvbnN0cmFpbnQpOyBpbmVydC1ieS1pbnZlbnRvcnkgaWYgbm8gc3VjaCByb3cKICBG
LVFVQU5UQS0yICBmaXJlcyBvbiBhbnkgdG93ZXIgcm93IHdpdGggQzEgQU5EIEMyCiAgRi1RVUFO
VEEtMyAgUkVHSVNURVJFRCwgTk9UIEVYRUNVVEVEIChubyBkZXJpdmVkIEVfYmluZGluZyBpbiB0
aGUgZnJhbWV3b3JrKQpQcm9tb3Rpb24gY29uZGl0aW9ucyAobG9jay1yZWNvcmQgYW5ub3RhdGlv
bnMgUEMtMS9QQy0yOyBQQy0zIGlzIHRoZSBjb21wYXJlIHN0ZXApCiAgUEMtMSAgbm9uLXRyaXZp
YWwgcGFydGl0aW9uOiA+PSAxIFBBU1MgYW5kID49IDEgRkFJTAogIFBDLTIgIGluZGVwZW5kZW5j
ZSB3aXRuZXNzOiA+PSAxIFBBU1Mgd2hvc2UgRnVuY3Rpb25hbENsYXNzIGlzIE5PVCB0aGUgcm9w
ZWxlbmd0aAogICAgICAgIGNsYXNzIChSaWdpZCBDb25zdHJhaW50KSwgaS5lLiB0aGUgcnVsZSBp
cyBub3QgYSByZXN0YXRlbWVudCBvZiBMX0IKIiIiCmltcG9ydCBhcmdwYXJzZSwgZGF0ZXRpbWUs
IGhhc2hsaWIsIGpzb24sIG9zLCBzeXMsIHRlbXBmaWxlCgojIC0tLS0tLS0tLS0tLS0tLS0tLS0t
LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tIGxvY2sgcGlucyAt
LS0KTUVNT19ERUZBVUxUICAgICAgPSAnc3RhZ2luZ19tZW1vX0dfUVVBTlRBX3YyLm1kJwpNRU1P
X0xPQ0tfTUQ1ICAgICA9ICcwMDM5ZDAwMTc2OTU2OTI5N2MyYWE4Y2NiZGVkNWEzYicKTUVNT19M
T0NLX0JZVEVTICAgPSA0ODYzCkxFREdFUl9CQVNFICAgICAgID0gJ1NRVF9NYXN0ZXJfTGVkZ2Vy
X3Y0XzgxX0NBTk9OSUNBTC5tZCcKTEVER0VSX0JBU0VfTUQ1ICAgPSAnYjRlNTVhYWVhNzZhMjE1
MmY3YjE4NzMzMDlhZWMwNzcnCkVMRUNUSU9OUyA9IHsKICAgICdFLVEtMSc6ICcoYikgUHJvbW90
ZSBzdGFuZGFsb25lLicsCiAgICAnRS1RLTInOiAnKGEpIEUtcGVyc3BlY3RpdmUgKDNEKSBmb3Ig
ZW52ZWxvcGVzLCBMLXBlcnNwZWN0aXZlICgyRC8zRCkgZm9yIGRlZmVjdHM7ICcKICAgICAgICAg
ICAgICdleHRlbmRlZCAoaW5maW5pdGUtZW5lcmd5KSBkZWZlY3RzIGV4cGxpY2l0bHkgaW4gc2Nv
cGUuJywKfQpDSEVDS1BPSU5UX0RFRkFVTFQgPSAnZ19xdWFudGFfY2hhdGxlZ19jaGVja3BvaW50
Lmpzb24nCkNPTVBBUkVfREVGQVVMVCAgICA9ICdnX3F1YW50YV9jaGF0bGVnX2NvbXBhcmUuanNv
bicKVDFfREVGQVVMVCAgICAgICAgID0gJ1QxX2ZvcmJpZGRlbl9zdHJpbmdzLnR4dCcKCiMgLS0t
LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLSB2
b2NhYnVsYXJ5IGxvY2sgLS0tCkNPTFVNTlMgICAgICAgICAgICA9IFsnT2JqZWN0JywgJ0xlZGdl
ciBSZWYnLCAnUGVyc3BlY3RpdmUnLCAnQ29uZmlnIFNwYWNlJywKICAgICAgICAgICAgICAgICAg
ICAgICdJbnZhcmlhbnQgVHlwZScsICdGdW5jdGlvbmFsIENsYXNzJ10KUEVSU1BFQ1RJVkVTICAg
ICAgID0geydMLVBlcnNwZWN0aXZlJywgJ0UtUGVyc3BlY3RpdmUnfQpDT05GSUdfU1BBQ0VTICAg
ICAgPSB7J0NvbnRpbnVvdXMnLCAnRGlzY3JldGUnfQpGVU5DVElPTkFMX0NMQVNTRVMgPSB7J1Jp
Z2lkIENvbnN0cmFpbnQnLCAnQ29tcGV0aW5nIEV4cG9uZW50cycsICdTaW5nbGUgRXhwb25lbnQn
LCAnTm9uZSd9CkMyX1BBU1NJTkcgICAgICAgICA9IHsnUmlnaWQgQ29uc3RyYWludCcsICdDb21w
ZXRpbmcgRXhwb25lbnRzJ30KUk9QRUxFTkdUSF9DTEFTUyAgID0gJ1JpZ2lkIENvbnN0cmFpbnQn
ICAgICAgIyBjbGFzcyBvZiB0aGUgbW90aXZhdGluZyBjYXNlIChMX0IpClRPV0VSX1RPS0VOICAg
ICAgICA9ICdUb3dlcicgICAgICAgICAgICAgICAgICMgaWRlbnRpZmllcyBjb21iaW5hdG9yaWFs
LXRvd2VyIHJvd3MgZm9yIEYtUVVBTlRBLTIKCgpkZWYgbWQ1YihiKTogcmV0dXJuIGhhc2hsaWIu
bWQ1KGIpLmhleGRpZ2VzdCgpCmRlZiBtZDVmKHApOiByZXR1cm4gbWQ1YihvcGVuKHAsICdyYicp
LnJlYWQoKSkKZGVmIGJ5dGVzX2xhYmVsKHApOiByZXR1cm4gZid7b3MucGF0aC5nZXRzaXplKHAp
Oix9IEInCgoKIyAtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0t
LS0tLS0tLS0tLS0tLS0tLS0tLS0gcGFyc2luZyAtLS0KZGVmIHNlY3Rpb24odGV4dCwgaGVhZGlu
Z19wcmVmaXgpOgogICAgbGluZXMgPSB0ZXh0LnNwbGl0KCdcbicpCiAgICB0cnk6CiAgICAgICAg
c3RhcnQgPSBuZXh0KGkgZm9yIGksIGwgaW4gZW51bWVyYXRlKGxpbmVzKSBpZiBsLnN0YXJ0c3dp
dGgoaGVhZGluZ19wcmVmaXgpKQogICAgZXhjZXB0IFN0b3BJdGVyYXRpb246CiAgICAgICAgcmFp
c2UgVmFsdWVFcnJvcihmJ3NlY3Rpb24ge2hlYWRpbmdfcHJlZml4IXJ9IG5vdCBmb3VuZCcpCiAg
ICBlbmQgPSBuZXh0KChpIGZvciBpIGluIHJhbmdlKHN0YXJ0ICsgMSwgbGVuKGxpbmVzKSkgaWYg
bGluZXNbaV0uc3RhcnRzd2l0aCgnIyMgJykpLCBsZW4obGluZXMpKQogICAgcmV0dXJuIGxpbmVz
W3N0YXJ0OmVuZF0KCgpkZWYgc3BsaXRfcm93KGxpbmUpOgogICAgcmV0dXJuIFtjLnN0cmlwKCkg
Zm9yIGMgaW4gbGluZS5zdHJpcCgpLnN0cmlwKCd8Jykuc3BsaXQoJ3wnKV0KCgpkZWYgcGFyc2Vf
aW52ZW50b3J5KHRleHQpOgogICAgcm93cyA9IFtsIGZvciBsIGluIHNlY3Rpb24odGV4dCwgJyMj
IDQuJykgaWYgbC5zdHJpcCgpLnN0YXJ0c3dpdGgoJ3wnKV0KICAgIGlmIGxlbihyb3dzKSA8IDM6
CiAgICAgICAgcmFpc2UgVmFsdWVFcnJvcignc2VjdGlvbiA0IHRhYmxlIG1pc3Npbmcgb3IgZW1w
dHknKQogICAgaGVhZGVyID0gc3BsaXRfcm93KHJvd3NbMF0pCiAgICBpZiBoZWFkZXIgIT0gQ09M
VU1OUzoKICAgICAgICByYWlzZSBWYWx1ZUVycm9yKGYnY29sdW1uIGhlYWRlciBtaXNtYXRjaDog
e2hlYWRlcn0nKQogICAgb3V0ID0gW10KICAgIGZvciByIGluIHJvd3NbMjpdOgogICAgICAgIGNl
bGxzID0gc3BsaXRfcm93KHIpCiAgICAgICAgaWYgbGVuKGNlbGxzKSAhPSBsZW4oQ09MVU1OUyk6
CiAgICAgICAgICAgIHJhaXNlIFZhbHVlRXJyb3IoZidyb3cgYXJpdHkge2xlbihjZWxscyl9ICE9
IHtsZW4oQ09MVU1OUyl9OiB7cn0nKQogICAgICAgIG91dC5hcHBlbmQoZGljdCh6aXAoQ09MVU1O
UywgY2VsbHMpKSkKICAgIHJldHVybiBvdXQKCgpkZWYgYmFzZV90b2tlbihzKToKICAgICIiIidD
b21wZXRpbmcgRXhwb25lbnRzIChHUCknIC0+ICdDb21wZXRpbmcgRXhwb25lbnRzJzsgJ05vbmUg
KFRyaXZpYWwgS25vdCknIC0+ICdOb25lJy4iIiIKICAgIHJldHVybiBzLnNwbGl0KCcoJylbMF0u
c3RyaXAoKQoKCmRlZiBwYXJzZV9oeXBvdGhlc2VzKHRleHQpOgogICAgIiIic2VjdGlvbiA1IGJ1
bGxldHMgb2YgdGhlIGZvcm0gJyogICAqKkxhYmVsOioqIFBBU1N8RkFJTCAuLi4nIC0+IHtsYWJl
bDogdmVyZGljdH0uIiIiCiAgICBoeXAgPSB7fQogICAgZm9yIGwgaW4gc2VjdGlvbih0ZXh0LCAn
IyMgNS4nKToKICAgICAgICBsID0gbC5zdHJpcCgpCiAgICAgICAgaWYgbm90IGwuc3RhcnRzd2l0
aCgnKicpOgogICAgICAgICAgICBjb250aW51ZQogICAgICAgIGlmICcqKicgbm90IGluIGw6CiAg
ICAgICAgICAgIGNvbnRpbnVlCiAgICAgICAgbGFiZWwgPSBsLnNwbGl0KCcqKicpWzFdLnJzdHJp
cCgnOicpLnN0cmlwKCkKICAgICAgICBsYWJlbCA9IGJhc2VfdG9rZW4obGFiZWwpCiAgICAgICAg
cmVzdCA9IGwuc3BsaXQoJyoqJylbMl0uc3RyaXAoKQogICAgICAgIHZlcmRpY3QgPSByZXN0LnNw
bGl0KCcuJylbMF0uc3BsaXQoJyAnKVswXS5zcGxpdCgnKCcpWzBdLnN0cmlwKCkKICAgICAgICBp
ZiB2ZXJkaWN0IG5vdCBpbiAoJ1BBU1MnLCAnRkFJTCcpOgogICAgICAgICAgICByYWlzZSBWYWx1
ZUVycm9yKGYndW5wYXJzZWFibGUgaHlwb3RoZXNpcyBsaW5lOiB7bH0nKQogICAgICAgIGh5cFts
YWJlbF0gPSB2ZXJkaWN0CiAgICByZXR1cm4gaHlwCgoKIyAtLS0tLS0tLS0tLS0tLS0tLS0tLS0t
LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0gZXZhbHVhdGlvbiAtLS0K
ZGVmIGV2YWx1YXRlX3Jvdyhyb3cpOgogICAgY3MsIHBlcnNwID0gcm93WydDb25maWcgU3BhY2Un
XSwgcm93WydQZXJzcGVjdGl2ZSddCiAgICBpZiBjcyBub3QgaW4gQ09ORklHX1NQQUNFUzoKICAg
ICAgICByYWlzZSBWYWx1ZUVycm9yKGYndW5rbm93biBDb25maWcgU3BhY2Uge2NzIXJ9IGluIHJv
dyB7cm93WyJPYmplY3QiXSFyfScpCiAgICBpZiBwZXJzcCBub3QgaW4gUEVSU1BFQ1RJVkVTOgog
ICAgICAgIHJhaXNlIFZhbHVlRXJyb3IoZid1bmtub3duIFBlcnNwZWN0aXZlIHtwZXJzcCFyfSBp
biByb3cge3Jvd1siT2JqZWN0Il0hcn0nKQogICAgaW52ID0gYmFzZV90b2tlbihyb3dbJ0ludmFy
aWFudCBUeXBlJ10pCiAgICBpbnYgPSBOb25lIGlmIGludiA9PSAnTm9uZScgZWxzZSBpbnYKICAg
IGZjID0gYmFzZV90b2tlbihyb3dbJ0Z1bmN0aW9uYWwgQ2xhc3MnXSkKICAgIGlmIGZjIG5vdCBp
biBGVU5DVElPTkFMX0NMQVNTRVM6CiAgICAgICAgcmFpc2UgVmFsdWVFcnJvcihmJ3Vua25vd24g
RnVuY3Rpb25hbCBDbGFzcyB7ZmMhcn0gaW4gcm93IHtyb3dbIk9iamVjdCJdIXJ9JykKCiAgICBp
ZiBjcyAhPSAnQ29udGludW91cyc6CiAgICAgICAgYzEsIGMxX3JlYXNvbiA9IEZhbHNlLCAnY29u
ZmlndXJhdGlvbiBzcGFjZSBpcyBEaXNjcmV0ZSAoc2VjdGlvbiAyOiBkaXNjcmV0ZSBsYWJlbHMg
ZXZhbHVhdGUgdG8gTk8pJwogICAgZWxpZiBpbnYgaXMgTm9uZToKICAgICAgICBjMSwgYzFfcmVh
c29uID0gRmFsc2UsICdubyBjb25zZXJ2ZWQgaW52YXJpYW50IGRlY2xhcmVkICh0cml2aWFsKScK
ICAgIGVsc2U6CiAgICAgICAgYzEsIGMxX3JlYXNvbiA9IFRydWUsIGYnY29udGludW91cyBjb25m
aWd1cmF0aW9uIHNwYWNlIHdpdGggaW52YXJpYW50IHtpbnZ9JwoKICAgIGMyID0gZmMgaW4gQzJf
UEFTU0lORwogICAgYzJfcmVhc29uID0gKGYnZnVuY3Rpb25hbCBjbGFzcyB7ZmN9IGlzIERlcnJp
Y2stZXZhZGluZycgaWYgYzIKICAgICAgICAgICAgICAgICBlbHNlIGYnZnVuY3Rpb25hbCBjbGFz
cyB7ZmN9IGlzIG5vdCBEZXJyaWNrLWV2YWRpbmcnKQogICAgcmV0dXJuIHsKICAgICAgICAnb2Jq
ZWN0Jzogcm93WydPYmplY3QnXSwgJ2xlZGdlcl9yZWYnOiByb3dbJ0xlZGdlciBSZWYnXSwgJ3Bl
cnNwZWN0aXZlJzogcGVyc3AsCiAgICAgICAgJ2NvbmZpZ19zcGFjZSc6IGNzLCAnaW52YXJpYW50
JzogaW52LCAnZnVuY3Rpb25hbF9jbGFzcyc6IGZjLAogICAgICAgICdDMSc6IGMxLCAnQzFfcmVh
c29uJzogYzFfcmVhc29uLCAnQzInOiBjMiwgJ0MyX3JlYXNvbic6IGMyX3JlYXNvbiwKICAgICAg
ICAndmVyZGljdCc6ICdQQVNTJyBpZiAoYzEgYW5kIGMyKSBlbHNlICdGQUlMJywKICAgIH0KCgpk
ZWYgZmFsc2lmaWVycyhyZXN1bHRzKToKICAgIGYxID0gW3JbJ29iamVjdCddIGZvciByIGluIHJl
c3VsdHMgaWYgclsnZnVuY3Rpb25hbF9jbGFzcyddID09ICdTaW5nbGUgRXhwb25lbnQnXQogICAg
ZjIgPSBbclsnb2JqZWN0J10gZm9yIHIgaW4gcmVzdWx0cyBpZiBUT1dFUl9UT0tFTiBpbiByWydv
YmplY3QnXSBhbmQgclsnQzEnXSBhbmQgclsnQzInXV0KICAgIHRvd2VyX3Jvd3MgPSBbclsnb2Jq
ZWN0J10gZm9yIHIgaW4gcmVzdWx0cyBpZiBUT1dFUl9UT0tFTiBpbiByWydvYmplY3QnXV0KICAg
IHJldHVybiB7CiAgICAgICAgJ0YtUVVBTlRBLTEnOiB7J3N0YXRlJzogJ0ZJUkVTJyBpZiBmMSBl
bHNlICdTSUxFTlQnLCAnaGl0cyc6IGYxLAogICAgICAgICAgICAgICAgICAgICAgICdpbmVydF9i
eV9pbnZlbnRvcnknOiBub3QgZjEgYW5kIGFsbChyWydmdW5jdGlvbmFsX2NsYXNzJ10gIT0gJ1Np
bmdsZSBFeHBvbmVudCcgZm9yIHIgaW4gcmVzdWx0cyksCiAgICAgICAgICAgICAgICAgICAgICAg
J25vdGUnOiAnZmlyZXMgb25seSBvbiBhIFNpbmdsZSBFeHBvbmVudCBmdW5jdGlvbmFsIGNsYXNz
OyB0aGUgbG9ja2VkIGludmVudG9yeSAnCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAn
ZGVjbGFyZXMgbm9uZSwgc28gc2lsZW5jZSBoZXJlIGlzIGluZXJ0LWJ5LWludmVudG9yeSwgbm90
IGEgdGVzdCBwYXNzZWQnfSwKICAgICAgICAnRi1RVUFOVEEtMic6IHsnc3RhdGUnOiAnRklSRVMn
IGlmIGYyIGVsc2UgJ1NJTEVOVCcsICdoaXRzJzogZjIsICd0b3dlcl9yb3dzX2V4YW1pbmVkJzog
dG93ZXJfcm93c30sCiAgICAgICAgJ0YtUVVBTlRBLTMnOiB7J3N0YXRlJzogJ1JFR0lTVEVSRURf
Tk9UX0VYRUNVVEVEJywKICAgICAgICAgICAgICAgICAgICAgICAnbm90ZSc6ICdubyBkZXJpdmVk
IEVfYmluZGluZyBleGlzdHMgaW4gdGhlIGZyYW1ld29yazsgdGVzdHMgc2NhbGUgc2VwYXJhdGlv
biwgJwogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgJ25vdCB0aGUgc3RhYmlsaXR5IGRp
c2NyaW1pbmF0b3InfSwKICAgIH0KCgpkZWYgcHJvbW90aW9uX2NvbmRpdGlvbnMocmVzdWx0cyk6
CiAgICBwYXNzZXMgPSBbciBmb3IgciBpbiByZXN1bHRzIGlmIHJbJ3ZlcmRpY3QnXSA9PSAnUEFT
UyddCiAgICBmYWlscyA9IFtyIGZvciByIGluIHJlc3VsdHMgaWYgclsndmVyZGljdCddID09ICdG
QUlMJ10KICAgIHdpdG5lc3NlcyA9IFtyWydvYmplY3QnXSBmb3IgciBpbiBwYXNzZXMgaWYgclsn
ZnVuY3Rpb25hbF9jbGFzcyddICE9IFJPUEVMRU5HVEhfQ0xBU1NdCiAgICByZXR1cm4gewogICAg
ICAgICdQQy0xX25vbnRyaXZpYWxfcGFydGl0aW9uJzogeydtZXQnOiBib29sKHBhc3NlcykgYW5k
IGJvb2woZmFpbHMpLAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICduX3Bh
c3MnOiBsZW4ocGFzc2VzKSwgJ25fZmFpbCc6IGxlbihmYWlscyl9LAogICAgICAgICdQQy0yX2lu
ZGVwZW5kZW5jZV93aXRuZXNzJzogeydtZXQnOiBib29sKHdpdG5lc3NlcyksICd3aXRuZXNzZXMn
OiB3aXRuZXNzZXMsCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgJ2V4Y2x1
ZGVkX2NsYXNzJzogUk9QRUxFTkdUSF9DTEFTU30sCiAgICAgICAgJ1BDLTNfY29uY29yZGFuY2Vf
d2l0aF9zZWN0aW9uXzUnOiAnREVGRVJSRUQgdG8gYGNvbXBhcmVgIChjb21wYXJpc29uIHN0ZXAg
bGFzdCknLAogICAgfQoKCmRlZiBldmFsdWF0ZV90ZXh0KHRleHQpOgogICAgcm93cyA9IHBhcnNl
X2ludmVudG9yeSh0ZXh0KQogICAgcmVzdWx0cyA9IFtldmFsdWF0ZV9yb3cocikgZm9yIHIgaW4g
cm93c10KICAgIHJldHVybiB7J2ludmVudG9yeV9yb3dzJzogbGVuKHJvd3MpLCAncmVzdWx0cyc6
IHJlc3VsdHMsCiAgICAgICAgICAgICdmYWxzaWZpZXJzJzogZmFsc2lmaWVycyhyZXN1bHRzKSwg
J3Byb21vdGlvbl9jb25kaXRpb25zJzogcHJvbW90aW9uX2NvbmRpdGlvbnMocmVzdWx0cyl9CgoK
IyAtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0t
LS0tLS0tLSBUMSBzZWxmLWdyZXAgLS0tCmRlZiB0MV9zY2FuKHBhdGhzLCB0MV9wYXRoKToKICAg
ICIiIlJldHVybnMgTm9uZSBpZiBubyBsaXN0IGlzIGF2YWlsYWJsZTsgZWxzZSBhIGxpc3Qgb2Yg
KHBhdGgsIHBhdHRlcm5faW5kZXgpIGhpdHMuCiAgICBQYXR0ZXJuIHRleHQgaXMgbmV2ZXIgZWNo
b2VkIChILTE2IG1hc2tpbmcgbGVzc29uKS4iIiIKICAgIGlmIG5vdCB0MV9wYXRoIG9yIG5vdCBv
cy5wYXRoLmV4aXN0cyh0MV9wYXRoKToKICAgICAgICByZXR1cm4gTm9uZQogICAgcGF0cyA9IFts
LnJzdHJpcCgnXG4nKSBmb3IgbCBpbiBvcGVuKHQxX3BhdGgsIGVuY29kaW5nPSd1dGYtOCcpCiAg
ICAgICAgICAgIGlmIGwuc3RyaXAoKSBhbmQgbm90IGwuc3RhcnRzd2l0aCgnIycpXQogICAgaGl0
cyA9IFtdCiAgICBmb3IgcCBpbiBwYXRoczoKICAgICAgICBkYXRhID0gb3BlbihwLCAncmInKS5y
ZWFkKCkuZGVjb2RlKCd1dGYtOCcsICdyZXBsYWNlJykKICAgICAgICBmb3IgaSwgcGF0IGluIGVu
dW1lcmF0ZShwYXRzKToKICAgICAgICAgICAgaWYgcGF0IGluIGRhdGE6CiAgICAgICAgICAgICAg
ICBoaXRzLmFwcGVuZCgocCwgaSkpCiAgICByZXR1cm4gaGl0cwoKCmRlZiB0MV9nYXRlKHBhdGhz
LCB0MV9wYXRoLCBhbGxvd19hYnNlbnQpOgogICAgaGl0cyA9IHQxX3NjYW4ocGF0aHMsIHQxX3Bh
dGgpCiAgICBpZiBoaXRzIGlzIE5vbmU6CiAgICAgICAgaWYgbm90IGFsbG93X2Fic2VudDoKICAg
ICAgICAgICAgc3lzLmV4aXQoJ0hBTFQ6IFQxIGZvcmJpZGRlbi1zdHJpbmcgbGlzdCBub3QgZm91
bmQ7IHN1cHBseSAtLXQxIFBBVEggb3IgcGFzcyAnCiAgICAgICAgICAgICAgICAgICAgICctLW5v
LXQxLWhhbHQgdG8gcmVjb3JkIHRoZSBvbWlzc2lvbiBhcyBhIGRldmlhdGlvbiAoRC1UMSkgYW5k
IGNvbnRpbnVlJykKICAgICAgICByZXR1cm4geydzdGF0ZSc6ICdMSVNUX0FCU0VOVCcsICdkZXZp
YXRpb24nOiAnRC1UMTogc2VsZi1ncmVwIHNraXBwZWQsIGxpc3Qgbm90IHN1cHBsaWVkJ30KICAg
IGlmIGhpdHM6CiAgICAgICAgc3lzLmV4aXQoJ0hBTFQ6IFQxIHNlbGYtZ3JlcCBISVQgJyArICcs
ICcuam9pbihmJ3twfSN7aX0nIGZvciBwLCBpIGluIGhpdHMpKQogICAgcmV0dXJuIHsnc3RhdGUn
OiAnQ0xFQU4nLCAnZmlsZXMnOiBbb3MucGF0aC5iYXNlbmFtZShwKSBmb3IgcCBpbiBwYXRoc119
CgoKIyAtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0t
LS0tLS0tLS0tLS0tIGNvbW1hbmRzIC0tLQpkZWYgY21kX2V2YWx1YXRlKGEpOgogICAgcmF3ID0g
b3BlbihhLm1lbW8sICdyYicpLnJlYWQoKQogICAgZ290ID0gbWQ1YihyYXcpCiAgICBpZiBnb3Qg
IT0gTUVNT19MT0NLX01ENSBvciBsZW4ocmF3KSAhPSBNRU1PX0xPQ0tfQllURVM6CiAgICAgICAg
c3lzLmV4aXQoZidIQUxUOiBtZW1vIGRvZXMgbm90IG1hdGNoIHRoZSBsb2NrIChtZDUge2dvdH0s
IHtsZW4ocmF3KX0gQjsgJwogICAgICAgICAgICAgICAgIGYnbG9jayB7TUVNT19MT0NLX01ENX0s
IHtNRU1PX0xPQ0tfQllURVN9IEIpJykKICAgIHQxX3ByZSA9IHQxX2dhdGUoW29zLnBhdGguYWJz
cGF0aChfX2ZpbGVfXyksIGEubWVtb10sIGEudDEsIGEubm9fdDFfaGFsdCkKCiAgICB0ZXh0ID0g
cmF3LmRlY29kZSgndXRmLTgnKQogICAgZXYgPSBldmFsdWF0ZV90ZXh0KHRleHQpCiAgICBjayA9
IHsKICAgICAgICAnZ2F0ZSc6ICdHLVFVQU5UQScsICdsZWcnOiAnY2hhdCcsICdpbnN0cnVtZW50
Jzogb3MucGF0aC5iYXNlbmFtZShfX2ZpbGVfXyksCiAgICAgICAgJ2luc3RydW1lbnRfbWQ1Jzog
bWQ1Zihvcy5wYXRoLmFic3BhdGgoX19maWxlX18pKSwKICAgICAgICAnbWVtbyc6IG9zLnBhdGgu
YmFzZW5hbWUoYS5tZW1vKSwgJ21lbW9fbWQ1JzogZ290LCAnbWVtb19ieXRlcyc6IGxlbihyYXcp
LAogICAgICAgICdsZWRnZXJfYmFzZSc6IExFREdFUl9CQVNFLCAnbGVkZ2VyX2Jhc2VfbWQ1Jzog
TEVER0VSX0JBU0VfTUQ1LAogICAgICAgICdlbGVjdGlvbnMnOiBFTEVDVElPTlMsICd1dGMnOiBk
YXRldGltZS5kYXRldGltZS51dGNub3coKS5pc29mb3JtYXQoKSArICdaJywKICAgICAgICAnVDFf
cHJlX2V2YWx1YXRpb24nOiB0MV9wcmUsICoqZXYsCiAgICB9CiAgICB3aXRoIG9wZW4oYS5jaGVj
a3BvaW50LCAndycsIGVuY29kaW5nPSd1dGYtOCcpIGFzIGY6CiAgICAgICAganNvbi5kdW1wKGNr
LCBmLCBlbnN1cmVfYXNjaWk9RmFsc2UsIGluZGVudD0yKQogICAgdDFfcG9zdCA9IHQxX2dhdGUo
W2EuY2hlY2twb2ludF0sIGEudDEsIFRydWUpCiAgICAjIGFwcGVuZCB0aGUgcG9zdC13cml0ZSBz
Y2FuIHJlc3VsdCB3aXRob3V0IGFsdGVyaW5nIHRoZSBldmFsdWF0aW9uIGNvbnRlbnQKICAgIGNr
WydUMV9wb3N0X3dyaXRlJ10gPSB0MV9wb3N0CiAgICB3aXRoIG9wZW4oYS5jaGVja3BvaW50LCAn
dycsIGVuY29kaW5nPSd1dGYtOCcpIGFzIGY6CiAgICAgICAganNvbi5kdW1wKGNrLCBmLCBlbnN1
cmVfYXNjaWk9RmFsc2UsIGluZGVudD0yKQoKICAgIHByaW50KGYnbWVtbyB7Z290fSAoe2xlbihy
YXcpOix9IEIpID09IGxvY2sgIHwgIGluc3RydW1lbnQge2NrWyJpbnN0cnVtZW50X21kNSJdfScp
CiAgICBwcmludChmJ1QxIHByZToge3QxX3ByZVsic3RhdGUiXX0gIHBvc3Q6IHt0MV9wb3N0WyJz
dGF0ZSJdfScpCiAgICBmb3IgciBpbiBldlsncmVzdWx0cyddOgogICAgICAgIHByaW50KGYne3Jb
InZlcmRpY3QiXTo0fSAgQzE9e2ludChyWyJDMSJdKX0gQzI9e2ludChyWyJDMiJdKX0gIHtyWyJv
YmplY3QiXX0gIFt7clsibGVkZ2VyX3JlZiJdfV0nKQogICAgZm9yIGssIHYgaW4gZXZbJ2ZhbHNp
ZmllcnMnXS5pdGVtcygpOgogICAgICAgIHByaW50KGYne2t9OiB7dlsic3RhdGUiXX0nICsgKGYn
ICBoaXRzPXt2WyJoaXRzIl19JyBpZiB2LmdldCgnaGl0cycpIGVsc2UgJycpKQogICAgcGMgPSBl
dlsncHJvbW90aW9uX2NvbmRpdGlvbnMnXQogICAgcHJpbnQoZidQQy0xIHBhcnRpdGlvbjoge3Bj
WyJQQy0xX25vbnRyaXZpYWxfcGFydGl0aW9uIl1bIm1ldCJdfSAgJwogICAgICAgICAgZicoe3Bj
WyJQQy0xX25vbnRyaXZpYWxfcGFydGl0aW9uIl1bIm5fcGFzcyJdfSBQQVNTIC8ge3BjWyJQQy0x
X25vbnRyaXZpYWxfcGFydGl0aW9uIl1bIm5fZmFpbCJdfSBGQUlMKScpCiAgICBwcmludChmJ1BD
LTIgd2l0bmVzczoge3BjWyJQQy0yX2luZGVwZW5kZW5jZV93aXRuZXNzIl1bIm1ldCJdfSAge3Bj
WyJQQy0yX2luZGVwZW5kZW5jZV93aXRuZXNzIl1bIndpdG5lc3NlcyJdfScpCiAgICBwcmludChm
J2NoZWNrcG9pbnQge2EuY2hlY2twb2ludH0ge21kNWYoYS5jaGVja3BvaW50KX0gKHtieXRlc19s
YWJlbChhLmNoZWNrcG9pbnQpfSknKQoKCmRlZiBtYXRjaF9oeXBvdGhlc2VzKHJlc3VsdHMsIGh5
cCk6CiAgICAiIiJNYXRjaCBlYWNoIHNlY3Rpb24tNSBsYWJlbCB0byBleGFjdGx5IG9uZSBpbnZl
bnRvcnkgb2JqZWN0IGJ5IHN1YnN0cmluZy4iIiIKICAgIHJvd3MgPSBbXQogICAgZm9yIGxhYmVs
LCBwcmVkaWN0ZWQgaW4gaHlwLml0ZW1zKCk6CiAgICAgICAgY2FuZHMgPSBbciBmb3IgciBpbiBy
ZXN1bHRzIGlmIGxhYmVsIGluIHJbJ29iamVjdCddXQogICAgICAgIGlmIGxlbihjYW5kcykgIT0g
MToKICAgICAgICAgICAgcmFpc2UgVmFsdWVFcnJvcihmJ2h5cG90aGVzaXMge2xhYmVsIXJ9IG1h
dGNoZXMge2xlbihjYW5kcyl9IG9iamVjdHMnKQogICAgICAgIHJvd3MuYXBwZW5kKHsnbGFiZWwn
OiBsYWJlbCwgJ29iamVjdCc6IGNhbmRzWzBdWydvYmplY3QnXSwKICAgICAgICAgICAgICAgICAg
ICAgJ3ByZWRpY3RlZCc6IHByZWRpY3RlZCwgJ21hY2hpbmUnOiBjYW5kc1swXVsndmVyZGljdCdd
LAogICAgICAgICAgICAgICAgICAgICAnY29uY29yZGFudCc6IHByZWRpY3RlZCA9PSBjYW5kc1sw
XVsndmVyZGljdCddfSkKICAgIHJldHVybiByb3dzCgoKZGVmIGNtZF9jb21wYXJlKGEpOgogICAg
Y2sgPSBqc29uLmxvYWQob3BlbihhLmNoZWNrcG9pbnQsIGVuY29kaW5nPSd1dGYtOCcpKQogICAg
cmF3ID0gb3BlbihhLm1lbW8sICdyYicpLnJlYWQoKQogICAgaWYgbWQ1YihyYXcpICE9IGNrWydt
ZW1vX21kNSddIG9yIG1kNWIocmF3KSAhPSBNRU1PX0xPQ0tfTUQ1OgogICAgICAgIHN5cy5leGl0
KCdIQUxUOiBtZW1vL2NoZWNrcG9pbnQvbG9jayBtZDUgZGlzYWdyZWVtZW50JykKICAgIGh5cCA9
IHBhcnNlX2h5cG90aGVzZXMocmF3LmRlY29kZSgndXRmLTgnKSkKICAgIHJvd3MgPSBtYXRjaF9o
eXBvdGhlc2VzKGNrWydyZXN1bHRzJ10sIGh5cCkKICAgIHVubWF0Y2hlZCA9IFtyWydvYmplY3Qn
XSBmb3IgciBpbiBja1sncmVzdWx0cyddIGlmIHJbJ29iamVjdCddIG5vdCBpbiB7eFsnb2JqZWN0
J10gZm9yIHggaW4gcm93c31dCiAgICBvdXQgPSB7J2dhdGUnOiAnRy1RVUFOVEEnLCAnc3RlcCc6
ICdjb21wYXJlIChQQy0zLCBjb21wYXJpc29uIGxhc3QpJywKICAgICAgICAgICAnY2hlY2twb2lu
dCc6IG9zLnBhdGguYmFzZW5hbWUoYS5jaGVja3BvaW50KSwgJ2NoZWNrcG9pbnRfbWQ1JzogbWQ1
ZihhLmNoZWNrcG9pbnQpLAogICAgICAgICAgICdtZW1vX21kNSc6IGNrWydtZW1vX21kNSddLCAn
cm93cyc6IHJvd3MsCiAgICAgICAgICAgJ29iamVjdHNfd2l0aG91dF9oeXBvdGhlc2lzJzogdW5t
YXRjaGVkLAogICAgICAgICAgICdQQy0zX21ldCc6IGFsbChyWydjb25jb3JkYW50J10gZm9yIHIg
aW4gcm93cykgYW5kIG5vdCB1bm1hdGNoZWQsCiAgICAgICAgICAgJ3V0Yyc6IGRhdGV0aW1lLmRh
dGV0aW1lLnV0Y25vdygpLmlzb2Zvcm1hdCgpICsgJ1onfQogICAgd2l0aCBvcGVuKGEub3V0LCAn
dycsIGVuY29kaW5nPSd1dGYtOCcpIGFzIGY6CiAgICAgICAganNvbi5kdW1wKG91dCwgZiwgZW5z
dXJlX2FzY2lpPUZhbHNlLCBpbmRlbnQ9MikKICAgIGZvciByIGluIHJvd3M6CiAgICAgICAgcHJp
bnQoZid7Ik9LICIgaWYgclsiY29uY29yZGFudCJdIGVsc2UgIk1JU1MifSAgSDp7clsicHJlZGlj
dGVkIl06NH0gTTp7clsibWFjaGluZSJdOjR9ICB7clsib2JqZWN0Il19JykKICAgIHByaW50KGYn
UEMtMyBjb25jb3JkYW5jZToge291dFsiUEMtM19tZXQiXX0gICB1bm1hdGNoZWQ9e3VubWF0Y2hl
ZH0nKQogICAgcHJpbnQoZidjb21wYXJlIHthLm91dH0ge21kNWYoYS5vdXQpfSAoe2J5dGVzX2xh
YmVsKGEub3V0KX0pJykKCgojIC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0t
LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tIHNlbGZ0ZXN0IC0tLQpTWU5fSEVBRCA9ICgnIyBz
eW50aGV0aWNcblxuIyMgNC4gSW5zdHJ1bWVudCBFbmNvZGluZ1xuXG4nCiAgICAgICAgICAgICd8
IE9iamVjdCB8IExlZGdlciBSZWYgfCBQZXJzcGVjdGl2ZSB8IENvbmZpZyBTcGFjZSB8IEludmFy
aWFudCBUeXBlIHwgRnVuY3Rpb25hbCBDbGFzcyB8XG4nCiAgICAgICAgICAgICd8IDotLS0gfCA6
LS0tIHwgOi0tLSB8IDotLS0gfCA6LS0tIHwgOi0tLSB8XG4nKQoKCmRlZiBzeW4ocm93cywgaHlw
PU5vbmUpOgogICAgdCA9IFNZTl9IRUFEICsgJycuam9pbignfCAnICsgJyB8ICcuam9pbihyKSAr
ICcgfFxuJyBmb3IgciBpbiByb3dzKQogICAgaWYgaHlwIGlzIG5vdCBOb25lOgogICAgICAgIHQg
Kz0gJ1xuIyMgNS4gSHlwb3RoZXNlc1xuJyArICcnLmpvaW4oZicqICAgKip7a306Kioge3Z9Llxu
JyBmb3IgaywgdiBpbiBoeXAuaXRlbXMoKSkKICAgIHQgKz0gJ1xuIyMgNi4gRW5kXG4nCiAgICBy
ZXR1cm4gdAoKCmRlZiBjbWRfc2VsZnRlc3QoYSk6CiAgICBvayA9IDAKCiAgICBkZWYgc3VpdGUo
bmFtZSwgZm4pOgogICAgICAgIG5vbmxvY2FsIG9rCiAgICAgICAgZm4oKTsgb2sgKz0gMTsgcHJp
bnQoZicgIGdyZWVuICB7bmFtZX0nKQoKICAgIGRlZiBzMSgpOiAgIyBwYXJzZXIgcm91bmQtdHJp
cCArIG5vcm1hbGlzYXRpb24KICAgICAgICByb3dzID0gcGFyc2VfaW52ZW50b3J5KHN5bihbWydB
JywgJ8KnMScsICdMLVBlcnNwZWN0aXZlJywgJ0NvbnRpbnVvdXMnLCAnTGlua2luZyBOdW1iZXIn
LCAnUmlnaWQgQ29uc3RyYWludCddLAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAg
ICBbJ0InLCAnwqcyJywgJ0UtUGVyc3BlY3RpdmUnLCAnRGlzY3JldGUnLCAnTm9uZSAoVHJpdmlh
bCknLCAnQ29tcGV0aW5nIEV4cG9uZW50cyAoR1ApJ11dKSkKICAgICAgICBhc3NlcnQgbGVuKHJv
d3MpID09IDIgYW5kIHJvd3NbMF1bJ09iamVjdCddID09ICdBJwogICAgICAgIGFzc2VydCBiYXNl
X3Rva2VuKHJvd3NbMV1bJ0ludmFyaWFudCBUeXBlJ10pID09ICdOb25lJwogICAgICAgIGFzc2Vy
dCBiYXNlX3Rva2VuKHJvd3NbMV1bJ0Z1bmN0aW9uYWwgQ2xhc3MnXSkgPT0gJ0NvbXBldGluZyBF
eHBvbmVudHMnCgogICAgZGVmIHMyKCk6ICAjIEMxL0MyIHRydXRoIHRhYmxlCiAgICAgICAgY2Fz
ZXMgPSBbKCdDb250aW51b3VzJywgJ1dpbmRpbmcgTnVtYmVyJywgJ1JpZ2lkIENvbnN0cmFpbnQn
LCBUcnVlLCBUcnVlLCAnUEFTUycpLAogICAgICAgICAgICAgICAgICgnQ29udGludW91cycsICdX
aW5kaW5nIE51bWJlcicsICdDb21wZXRpbmcgRXhwb25lbnRzJywgVHJ1ZSwgVHJ1ZSwgJ1BBU1Mn
KSwKICAgICAgICAgICAgICAgICAoJ0NvbnRpbnVvdXMnLCAnTm9uZScsICdSaWdpZCBDb25zdHJh
aW50JywgRmFsc2UsIFRydWUsICdGQUlMJyksCiAgICAgICAgICAgICAgICAgKCdDb250aW51b3Vz
JywgJ1dpbmRpbmcgTnVtYmVyJywgJ05vbmUnLCBUcnVlLCBGYWxzZSwgJ0ZBSUwnKSwKICAgICAg
ICAgICAgICAgICAoJ0Rpc2NyZXRlJywgJ0NoaXJhbGl0eS9BbGdlYnJhaWMnLCAnTm9uZScsIEZh
bHNlLCBGYWxzZSwgJ0ZBSUwnKSwKICAgICAgICAgICAgICAgICAoJ0Rpc2NyZXRlJywgJ0NoaXJh
bGl0eS9BbGdlYnJhaWMnLCAnQ29tcGV0aW5nIEV4cG9uZW50cycsIEZhbHNlLCBUcnVlLCAnRkFJ
TCcpLAogICAgICAgICAgICAgICAgICgnQ29udGludW91cycsICdXaW5kaW5nIE51bWJlcicsICdT
aW5nbGUgRXhwb25lbnQnLCBUcnVlLCBGYWxzZSwgJ0ZBSUwnKV0KICAgICAgICBmb3IgY3MsIGlu
diwgZmMsIGMxLCBjMiwgdiBpbiBjYXNlczoKICAgICAgICAgICAgciA9IGV2YWx1YXRlX3Jvdyh7
J09iamVjdCc6ICdYJywgJ0xlZGdlciBSZWYnOiAnwqcnLCAnUGVyc3BlY3RpdmUnOiAnTC1QZXJz
cGVjdGl2ZScsCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICdDb25maWcgU3BhY2UnOiBj
cywgJ0ludmFyaWFudCBUeXBlJzogaW52LCAnRnVuY3Rpb25hbCBDbGFzcyc6IGZjfSkKICAgICAg
ICAgICAgYXNzZXJ0IChyWydDMSddLCByWydDMiddLCByWyd2ZXJkaWN0J10pID09IChjMSwgYzIs
IHYpLCAoY3MsIGludiwgZmMsIHIpCgogICAgZGVmIHMzKCk6ICAjIEYtUVVBTlRBLTIgZmlyZXMg
b24gYSB0b3dlciByb3cgdGhhdCBpcyBjb250aW51b3VzICsgY29tcGV0aW5nCiAgICAgICAgZXYg
PSBldmFsdWF0ZV90ZXh0KHN5bihbWydDRCBUb3dlciBSdW5ncycsICfCpycsICdFLVBlcnNwZWN0
aXZlJywgJ0NvbnRpbnVvdXMnLCAnTGlua2luZyBOdW1iZXInLCAnQ29tcGV0aW5nIEV4cG9uZW50
cyddXSkpCiAgICAgICAgYXNzZXJ0IGV2WydmYWxzaWZpZXJzJ11bJ0YtUVVBTlRBLTInXVsnc3Rh
dGUnXSA9PSAnRklSRVMnCiAgICAgICAgZXYgPSBldmFsdWF0ZV90ZXh0KHN5bihbWydDRCBUb3dl
ciBSdW5ncycsICfCpycsICdFLVBlcnNwZWN0aXZlJywgJ0Rpc2NyZXRlJywgJ0NoaXJhbGl0eScs
ICdOb25lJ11dKSkKICAgICAgICBhc3NlcnQgZXZbJ2ZhbHNpZmllcnMnXVsnRi1RVUFOVEEtMidd
WydzdGF0ZSddID09ICdTSUxFTlQnCgogICAgZGVmIHM0KCk6ICAjIEYtUVVBTlRBLTEgZmlyZXMg
b24gU2luZ2xlIEV4cG9uZW50OyBpbmVydCBmbGFnIG90aGVyd2lzZQogICAgICAgIGV2ID0gZXZh
bHVhdGVfdGV4dChzeW4oW1snWicsICfCpycsICdMLVBlcnNwZWN0aXZlJywgJ0NvbnRpbnVvdXMn
LCAnV2luZGluZyBOdW1iZXInLCAnU2luZ2xlIEV4cG9uZW50J11dKSkKICAgICAgICBhc3NlcnQg
ZXZbJ2ZhbHNpZmllcnMnXVsnRi1RVUFOVEEtMSddWydzdGF0ZSddID09ICdGSVJFUycKICAgICAg
ICBldiA9IGV2YWx1YXRlX3RleHQoc3luKFtbJ1onLCAnwqcnLCAnTC1QZXJzcGVjdGl2ZScsICdD
b250aW51b3VzJywgJ1dpbmRpbmcgTnVtYmVyJywgJ1JpZ2lkIENvbnN0cmFpbnQnXV0pKQogICAg
ICAgIGYxID0gZXZbJ2ZhbHNpZmllcnMnXVsnRi1RVUFOVEEtMSddCiAgICAgICAgYXNzZXJ0IGYx
WydzdGF0ZSddID09ICdTSUxFTlQnIGFuZCBmMVsnaW5lcnRfYnlfaW52ZW50b3J5J10gaXMgVHJ1
ZQoKICAgIGRlZiBzNSgpOiAgIyBQQy0xIC8gUEMtMgogICAgICAgIG9ubHlfcm9wZSA9IHN5bihb
WydBJywgJ8KnJywgJ0wtUGVyc3BlY3RpdmUnLCAnQ29udGludW91cycsICdMaW5raW5nIE51bWJl
cicsICdSaWdpZCBDb25zdHJhaW50J10sCiAgICAgICAgICAgICAgICAgICAgICAgICBbJ0InLCAn
wqcnLCAnRS1QZXJzcGVjdGl2ZScsICdEaXNjcmV0ZScsICdOb25lJywgJ05vbmUnXV0pCiAgICAg
ICAgcGMgPSBldmFsdWF0ZV90ZXh0KG9ubHlfcm9wZSlbJ3Byb21vdGlvbl9jb25kaXRpb25zJ10K
ICAgICAgICBhc3NlcnQgcGNbJ1BDLTFfbm9udHJpdmlhbF9wYXJ0aXRpb24nXVsnbWV0J10gYW5k
IG5vdCBwY1snUEMtMl9pbmRlcGVuZGVuY2Vfd2l0bmVzcyddWydtZXQnXQogICAgICAgIHdpdGhf
Z3AgPSBzeW4oW1snQScsICfCpycsICdMLVBlcnNwZWN0aXZlJywgJ0NvbnRpbnVvdXMnLCAnTGlu
a2luZyBOdW1iZXInLCAnUmlnaWQgQ29uc3RyYWludCddLAogICAgICAgICAgICAgICAgICAgICAg
IFsnSycsICfCpycsICdMLVBlcnNwZWN0aXZlJywgJ0NvbnRpbnVvdXMnLCAnRmFubyBXaW5kaW5n
JywgJ0NvbXBldGluZyBFeHBvbmVudHMgKEdQKSddXSkKICAgICAgICBwYyA9IGV2YWx1YXRlX3Rl
eHQod2l0aF9ncClbJ3Byb21vdGlvbl9jb25kaXRpb25zJ10KICAgICAgICBhc3NlcnQgbm90IHBj
WydQQy0xX25vbnRyaXZpYWxfcGFydGl0aW9uJ11bJ21ldCddIGFuZCBwY1snUEMtMl9pbmRlcGVu
ZGVuY2Vfd2l0bmVzcyddWyd3aXRuZXNzZXMnXSA9PSBbJ0snXQoKICAgIGRlZiBzNigpOiAgIyB2
b2NhYnVsYXJ5IGxvY2sgcmVqZWN0cyB1bmtub3duIGNsYXNzZXMgLyBzcGFjZXMKICAgICAgICBm
b3IgYmFkIGluIFtkaWN0KGNzPSdDb250aW51b3VzJywgaW52PSdYJywgZmM9J1NvZnQgQ29uc3Ry
YWludCcpLAogICAgICAgICAgICAgICAgICAgIGRpY3QoY3M9J0Z1enp5JywgaW52PSdYJywgZmM9
J05vbmUnKV06CiAgICAgICAgICAgIHRyeToKICAgICAgICAgICAgICAgIGV2YWx1YXRlX3Jvdyh7
J09iamVjdCc6ICdYJywgJ0xlZGdlciBSZWYnOiAnwqcnLCAnUGVyc3BlY3RpdmUnOiAnTC1QZXJz
cGVjdGl2ZScsCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICdDb25maWcgU3BhY2UnOiBi
YWRbJ2NzJ10sICdJbnZhcmlhbnQgVHlwZSc6IGJhZFsnaW52J10sICdGdW5jdGlvbmFsIENsYXNz
JzogYmFkWydmYyddfSkKICAgICAgICAgICAgICAgIHJhaXNlIEFzc2VydGlvbkVycm9yKCdhY2Nl
cHRlZCBiYWQgdm9jYWJ1bGFyeScpCiAgICAgICAgICAgIGV4Y2VwdCBWYWx1ZUVycm9yOgogICAg
ICAgICAgICAgICAgcGFzcwoKICAgIGRlZiBzNygpOiAgIyBtZDUgZ3VhcmQ6IGEgdGFtcGVyZWQg
bWVtbyAob25lIGJ5dGUpIGlzIG5vdCB0aGUgbG9jawogICAgICAgIHJhdyA9IG9wZW4oYS5tZW1v
LCAncmInKS5yZWFkKCkgaWYgb3MucGF0aC5leGlzdHMoYS5tZW1vKSBlbHNlIGIneCcgKiBNRU1P
X0xPQ0tfQllURVMKICAgICAgICB0YW1wZXJlZCA9IHJhd1s6LTFdICsgKGInXG4nIGlmIHJhd1st
MTpdICE9IGInXG4nIGVsc2UgYicgJykKICAgICAgICBhc3NlcnQgbWQ1Yih0YW1wZXJlZCkgIT0g
TUVNT19MT0NLX01ENSBhbmQgbWQ1Yih0YW1wZXJlZCkgIT0gbWQ1YihyYXcpCgogICAgZGVmIHM4
KCk6ICAjIGh5cG90aGVzaXMgcGFyc2luZyArIG1hdGNoaW5nIChzdWJzdHJpbmcsIHVuaXF1ZSkK
ICAgICAgICB0ID0gc3luKFtbJ0NsdXN0ZXIgTSBTTFdFIE1hdHJpY2VzJywgJ8KnJywgJ0UtUGVy
c3BlY3RpdmUnLCAnRGlzY3JldGUnLCAnTm9uZScsICdOb25lJ10sCiAgICAgICAgICAgICAgICAg
WydDbGlmZm9yZCBVbmtub3QgLyBSdWxlIDE3JywgJ8KnJywgJ0wtUGVyc3BlY3RpdmUnLCAnQ29u
dGludW91cycsICdOb25lIChUcml2aWFsIEtub3QpJywgJ1JpZ2lkIENvbnN0cmFpbnQnXV0sCiAg
ICAgICAgICAgICAgICBoeXA9eydTTFdFIE1hdHJpY2VzJzogJ0ZBSUwnLCAnQ2xpZmZvcmQgVW5r
bm90JzogJ0ZBSUwnfSkKICAgICAgICBldiA9IGV2YWx1YXRlX3RleHQodCkKICAgICAgICByb3dz
ID0gbWF0Y2hfaHlwb3RoZXNlcyhldlsncmVzdWx0cyddLCBwYXJzZV9oeXBvdGhlc2VzKHQpKQog
ICAgICAgIGFzc2VydCBsZW4ocm93cykgPT0gMiBhbmQgYWxsKHJbJ2NvbmNvcmRhbnQnXSBmb3Ig
ciBpbiByb3dzKQogICAgICAgIHRyeToKICAgICAgICAgICAgbWF0Y2hfaHlwb3RoZXNlcyhldlsn
cmVzdWx0cyddLCB7J05vdGhpbmcnOiAnUEFTUyd9KTsgcmFpc2UgQXNzZXJ0aW9uRXJyb3IoJ21h
dGNoZWQgbm90aGluZycpCiAgICAgICAgZXhjZXB0IFZhbHVlRXJyb3I6CiAgICAgICAgICAgIHBh
c3MKCiAgICBkZWYgczkoKTogICMgVDEgc2NhbiBtZWNoYW5pY3M6IGFic2VudCBsaXN0IC0+IE5v
bmU7IHBsYW50ZWQgdG9rZW4gLT4gaGl0IGJ5IGluZGV4IG9ubHkKICAgICAgICB3aXRoIHRlbXBm
aWxlLlRlbXBvcmFyeURpcmVjdG9yeSgpIGFzIGQ6CiAgICAgICAgICAgIGxzdCA9IG9zLnBhdGgu
am9pbihkLCAndDEudHh0Jyk7IHRndCA9IG9zLnBhdGguam9pbihkLCAneC50eHQnKQogICAgICAg
ICAgICBvcGVuKGxzdCwgJ3cnKS53cml0ZSgnIyBjb21tZW50XG5aWlFYX1NFTEZURVNUX1RPS0VO
XG4nKQogICAgICAgICAgICBvcGVuKHRndCwgJ3cnKS53cml0ZSgnY2xlYW4gdGV4dCcpCiAgICAg
ICAgICAgIGFzc2VydCB0MV9zY2FuKFt0Z3RdLCBsc3QpID09IFtdCiAgICAgICAgICAgIG9wZW4o
dGd0LCAndycpLndyaXRlKCdoYXMgWlpRWF9TRUxGVEVTVF9UT0tFTiBpbnNpZGUnKQogICAgICAg
ICAgICBhc3NlcnQgdDFfc2NhbihbdGd0XSwgbHN0KSA9PSBbKHRndCwgMCldCiAgICAgICAgICAg
IGFzc2VydCB0MV9zY2FuKFt0Z3RdLCBvcy5wYXRoLmpvaW4oZCwgJ21pc3NpbmcudHh0JykpIGlz
IE5vbmUKCiAgICBmb3IgbmFtZSwgZm4gaW4gWygnUzEgcGFyc2VyL25vcm1hbGlzYXRpb24nLCBz
MSksICgnUzIgQzEvQzIgdHJ1dGggdGFibGUnLCBzMiksCiAgICAgICAgICAgICAgICAgICAgICgn
UzMgRi1RVUFOVEEtMiBmaXJpbmcnLCBzMyksICgnUzQgRi1RVUFOVEEtMSBmaXJpbmcgKyBpbmVy
dCBmbGFnJywgczQpLAogICAgICAgICAgICAgICAgICAgICAoJ1M1IFBDLTEvUEMtMicsIHM1KSwg
KCdTNiB2b2NhYnVsYXJ5IGxvY2snLCBzNiksICgnUzcgbWQ1IGd1YXJkJywgczcpLAogICAgICAg
ICAgICAgICAgICAgICAoJ1M4IGh5cG90aGVzaXMgbWF0Y2gnLCBzOCksICgnUzkgVDEgc2NhbiBt
ZWNoYW5pY3MnLCBzOSldOgogICAgICAgIHN1aXRlKG5hbWUsIGZuKQogICAgcHJpbnQoZidBTEwg
e29rfS85IFNVSVRFUyBHUkVFTiAgKGluc3RydW1lbnQge21kNWYob3MucGF0aC5hYnNwYXRoKF9f
ZmlsZV9fKSl9KScpCgoKZGVmIG1haW4oKToKICAgIHAgPSBhcmdwYXJzZS5Bcmd1bWVudFBhcnNl
cihkZXNjcmlwdGlvbj1fX2RvY19fLCBmb3JtYXR0ZXJfY2xhc3M9YXJncGFyc2UuUmF3RGVzY3Jp
cHRpb25IZWxwRm9ybWF0dGVyKQogICAgcC5hZGRfYXJndW1lbnQoJy0tbWVtbycsIGRlZmF1bHQ9
TUVNT19ERUZBVUxUKQogICAgcC5hZGRfYXJndW1lbnQoJy0tdDEnLCBkZWZhdWx0PVQxX0RFRkFV
TFQsIGhlbHA9J1QxIGZvcmJpZGRlbi1zdHJpbmcgbGlzdCAob25lIHBhdHRlcm4gcGVyIGxpbmUp
JykKICAgIHAuYWRkX2FyZ3VtZW50KCctLW5vLXQxLWhhbHQnLCBhY3Rpb249J3N0b3JlX3RydWUn
LCBoZWxwPSdyZWNvcmQgRC1UMSBpbnN0ZWFkIG9mIGhhbHRpbmcgd2hlbiB0aGUgbGlzdCBpcyBh
YnNlbnQnKQogICAgcC5hZGRfYXJndW1lbnQoJy0tY2hlY2twb2ludCcsIGRlZmF1bHQ9Q0hFQ0tQ
T0lOVF9ERUZBVUxUKQogICAgcC5hZGRfYXJndW1lbnQoJy0tb3V0JywgZGVmYXVsdD1DT01QQVJF
X0RFRkFVTFQsIGhlbHA9J2NvbXBhcmUtc3RlcCBvdXRwdXQgKHNlcGFyYXRlIGZyb20gdGhlIGNo
ZWNrcG9pbnQpJykKICAgIHAuYWRkX2FyZ3VtZW50KCdjbWQnLCBjaG9pY2VzPVsnc2VsZnRlc3Qn
LCAnZXZhbHVhdGUnLCAnY29tcGFyZSddKQogICAgYSA9IHAucGFyc2VfYXJncygpCiAgICB7J3Nl
bGZ0ZXN0JzogY21kX3NlbGZ0ZXN0LCAnZXZhbHVhdGUnOiBjbWRfZXZhbHVhdGUsICdjb21wYXJl
JzogY21kX2NvbXBhcmV9W2EuY21kXShhKQoKCmlmIF9fbmFtZV9fID09ICdfX21haW5fXyc6CiAg
ICBtYWluKCkK
=====END-EMBED name=g_quanta_chatleg.py=====

=====BEGIN-EMBED name=g_quanta_chatleg_checkpoint.json md5=55861161748fca634534790f366380fd bytes=4605 encoding=base64 armor_bytes=6221 QUARANTINED=====
ewogICJnYXRlIjogIkctUVVBTlRBIiwKICAibGVnIjogImNoYXQiLAogICJpbnN0cnVtZW50Ijog
ImdfcXVhbnRhX2NoYXRsZWcucHkiLAogICJpbnN0cnVtZW50X21kNSI6ICI3OTA3MjE5NmNkZmM0
ODBmNDA3MzE5NWQ5NjEwMGQyZSIsCiAgIm1lbW8iOiAic3RhZ2luZ19tZW1vX0dfUVVBTlRBX3Yy
Lm1kIiwKICAibWVtb19tZDUiOiAiMDAzOWQwMDE3Njk1NjkyOTdjMmFhOGNjYmRlZDVhM2IiLAog
ICJtZW1vX2J5dGVzIjogNDg2MywKICAibGVkZ2VyX2Jhc2UiOiAiU1FUX01hc3Rlcl9MZWRnZXJf
djRfODFfQ0FOT05JQ0FMLm1kIiwKICAibGVkZ2VyX2Jhc2VfbWQ1IjogImI0ZTU1YWFlYTc2YTIx
NTJmN2IxODczMzA5YWVjMDc3IiwKICAiZWxlY3Rpb25zIjogewogICAgIkUtUS0xIjogIihiKSBQ
cm9tb3RlIHN0YW5kYWxvbmUuIiwKICAgICJFLVEtMiI6ICIoYSkgRS1wZXJzcGVjdGl2ZSAoM0Qp
IGZvciBlbnZlbG9wZXMsIEwtcGVyc3BlY3RpdmUgKDJELzNEKSBmb3IgZGVmZWN0czsgZXh0ZW5k
ZWQgKGluZmluaXRlLWVuZXJneSkgZGVmZWN0cyBleHBsaWNpdGx5IGluIHNjb3BlLiIKICB9LAog
ICJ1dGMiOiAiMjAyNi0wOS0xMFQyMDowMjoxOC4wMzczMzZaIiwKICAiVDFfcHJlX2V2YWx1YXRp
b24iOiB7CiAgICAic3RhdGUiOiAiTElTVF9BQlNFTlQiLAogICAgImRldmlhdGlvbiI6ICJELVQx
OiBzZWxmLWdyZXAgc2tpcHBlZCwgbGlzdCBub3Qgc3VwcGxpZWQiCiAgfSwKICAiaW52ZW50b3J5
X3Jvd3MiOiA2LAogICJyZXN1bHRzIjogWwogICAgewogICAgICAib2JqZWN0IjogIkxfQiBCb3Jy
b21lYW4gQmFyeW9uIiwKICAgICAgImxlZGdlcl9yZWYiOiAiwqcyLjE1L8KnMi41MSIsCiAgICAg
ICJwZXJzcGVjdGl2ZSI6ICJMLVBlcnNwZWN0aXZlIiwKICAgICAgImNvbmZpZ19zcGFjZSI6ICJD
b250aW51b3VzIiwKICAgICAgImludmFyaWFudCI6ICJMaW5raW5nIE51bWJlciIsCiAgICAgICJm
dW5jdGlvbmFsX2NsYXNzIjogIlJpZ2lkIENvbnN0cmFpbnQiLAogICAgICAiQzEiOiB0cnVlLAog
ICAgICAiQzFfcmVhc29uIjogImNvbnRpbnVvdXMgY29uZmlndXJhdGlvbiBzcGFjZSB3aXRoIGlu
dmFyaWFudCBMaW5raW5nIE51bWJlciIsCiAgICAgICJDMiI6IHRydWUsCiAgICAgICJDMl9yZWFz
b24iOiAiZnVuY3Rpb25hbCBjbGFzcyBSaWdpZCBDb25zdHJhaW50IGlzIERlcnJpY2stZXZhZGlu
ZyIsCiAgICAgICJ2ZXJkaWN0IjogIlBBU1MiCiAgICB9LAogICAgewogICAgICAib2JqZWN0Ijog
IkvigocgVm9ydGV4IiwKICAgICAgImxlZGdlcl9yZWYiOiAiwqczLjQiLAogICAgICAicGVyc3Bl
Y3RpdmUiOiAiTC1QZXJzcGVjdGl2ZSIsCiAgICAgICJjb25maWdfc3BhY2UiOiAiQ29udGludW91
cyIsCiAgICAgICJpbnZhcmlhbnQiOiAiRmFubyBXaW5kaW5nIiwKICAgICAgImZ1bmN0aW9uYWxf
Y2xhc3MiOiAiQ29tcGV0aW5nIEV4cG9uZW50cyIsCiAgICAgICJDMSI6IHRydWUsCiAgICAgICJD
MV9yZWFzb24iOiAiY29udGludW91cyBjb25maWd1cmF0aW9uIHNwYWNlIHdpdGggaW52YXJpYW50
IEZhbm8gV2luZGluZyIsCiAgICAgICJDMiI6IHRydWUsCiAgICAgICJDMl9yZWFzb24iOiAiZnVu
Y3Rpb25hbCBjbGFzcyBDb21wZXRpbmcgRXhwb25lbnRzIGlzIERlcnJpY2stZXZhZGluZyIsCiAg
ICAgICJ2ZXJkaWN0IjogIlBBU1MiCiAgICB9LAogICAgewogICAgICAib2JqZWN0IjogIkVsZWN0
cm9uIDLPgCBDbG9zdXJlIiwKICAgICAgImxlZGdlcl9yZWYiOiAiwqcyLjUwLkEiLAogICAgICAi
cGVyc3BlY3RpdmUiOiAiTC1QZXJzcGVjdGl2ZSIsCiAgICAgICJjb25maWdfc3BhY2UiOiAiQ29u
dGludW91cyIsCiAgICAgICJpbnZhcmlhbnQiOiAiV2luZGluZyBOdW1iZXIiLAogICAgICAiZnVu
Y3Rpb25hbF9jbGFzcyI6ICJSaWdpZCBDb25zdHJhaW50IiwKICAgICAgIkMxIjogdHJ1ZSwKICAg
ICAgIkMxX3JlYXNvbiI6ICJjb250aW51b3VzIGNvbmZpZ3VyYXRpb24gc3BhY2Ugd2l0aCBpbnZh
cmlhbnQgV2luZGluZyBOdW1iZXIiLAogICAgICAiQzIiOiB0cnVlLAogICAgICAiQzJfcmVhc29u
IjogImZ1bmN0aW9uYWwgY2xhc3MgUmlnaWQgQ29uc3RyYWludCBpcyBEZXJyaWNrLWV2YWRpbmci
LAogICAgICAidmVyZGljdCI6ICJQQVNTIgogICAgfSwKICAgIHsKICAgICAgIm9iamVjdCI6ICJD
bGlmZm9yZCBVbmtub3QgLyBSdWxlIDE3IiwKICAgICAgImxlZGdlcl9yZWYiOiAiwqcyLjQxIiwK
ICAgICAgInBlcnNwZWN0aXZlIjogIkwtUGVyc3BlY3RpdmUiLAogICAgICAiY29uZmlnX3NwYWNl
IjogIkNvbnRpbnVvdXMiLAogICAgICAiaW52YXJpYW50IjogbnVsbCwKICAgICAgImZ1bmN0aW9u
YWxfY2xhc3MiOiAiUmlnaWQgQ29uc3RyYWludCIsCiAgICAgICJDMSI6IGZhbHNlLAogICAgICAi
QzFfcmVhc29uIjogIm5vIGNvbnNlcnZlZCBpbnZhcmlhbnQgZGVjbGFyZWQgKHRyaXZpYWwpIiwK
ICAgICAgIkMyIjogdHJ1ZSwKICAgICAgIkMyX3JlYXNvbiI6ICJmdW5jdGlvbmFsIGNsYXNzIFJp
Z2lkIENvbnN0cmFpbnQgaXMgRGVycmljay1ldmFkaW5nIiwKICAgICAgInZlcmRpY3QiOiAiRkFJ
TCIKICAgIH0sCiAgICB7CiAgICAgICJvYmplY3QiOiAiQ0QgVG93ZXIgUnVuZ3MgKGUuZy4sIDQy
Lzg0KSIsCiAgICAgICJsZWRnZXJfcmVmIjogIsKnMi4zMS/CpzIuNzUiLAogICAgICAicGVyc3Bl
Y3RpdmUiOiAiRS1QZXJzcGVjdGl2ZSIsCiAgICAgICJjb25maWdfc3BhY2UiOiAiRGlzY3JldGUi
LAogICAgICAiaW52YXJpYW50IjogIkNoaXJhbGl0eS9BbGdlYnJhaWMiLAogICAgICAiZnVuY3Rp
b25hbF9jbGFzcyI6ICJOb25lIiwKICAgICAgIkMxIjogZmFsc2UsCiAgICAgICJDMV9yZWFzb24i
OiAiY29uZmlndXJhdGlvbiBzcGFjZSBpcyBEaXNjcmV0ZSAoc2VjdGlvbiAyOiBkaXNjcmV0ZSBs
YWJlbHMgZXZhbHVhdGUgdG8gTk8pIiwKICAgICAgIkMyIjogZmFsc2UsCiAgICAgICJDMl9yZWFz
b24iOiAiZnVuY3Rpb25hbCBjbGFzcyBOb25lIGlzIG5vdCBEZXJyaWNrLWV2YWRpbmciLAogICAg
ICAidmVyZGljdCI6ICJGQUlMIgogICAgfSwKICAgIHsKICAgICAgIm9iamVjdCI6ICJDbHVzdGVy
IE0gU0xXRSBNYXRyaWNlcyIsCiAgICAgICJsZWRnZXJfcmVmIjogIsKnMi41OCIsCiAgICAgICJw
ZXJzcGVjdGl2ZSI6ICJFLVBlcnNwZWN0aXZlIiwKICAgICAgImNvbmZpZ19zcGFjZSI6ICJEaXNj
cmV0ZSIsCiAgICAgICJpbnZhcmlhbnQiOiBudWxsLAogICAgICAiZnVuY3Rpb25hbF9jbGFzcyI6
ICJOb25lIiwKICAgICAgIkMxIjogZmFsc2UsCiAgICAgICJDMV9yZWFzb24iOiAiY29uZmlndXJh
dGlvbiBzcGFjZSBpcyBEaXNjcmV0ZSAoc2VjdGlvbiAyOiBkaXNjcmV0ZSBsYWJlbHMgZXZhbHVh
dGUgdG8gTk8pIiwKICAgICAgIkMyIjogZmFsc2UsCiAgICAgICJDMl9yZWFzb24iOiAiZnVuY3Rp
b25hbCBjbGFzcyBOb25lIGlzIG5vdCBEZXJyaWNrLWV2YWRpbmciLAogICAgICAidmVyZGljdCI6
ICJGQUlMIgogICAgfQogIF0sCiAgImZhbHNpZmllcnMiOiB7CiAgICAiRi1RVUFOVEEtMSI6IHsK
ICAgICAgInN0YXRlIjogIlNJTEVOVCIsCiAgICAgICJoaXRzIjogW10sCiAgICAgICJpbmVydF9i
eV9pbnZlbnRvcnkiOiB0cnVlLAogICAgICAibm90ZSI6ICJmaXJlcyBvbmx5IG9uIGEgU2luZ2xl
IEV4cG9uZW50IGZ1bmN0aW9uYWwgY2xhc3M7IHRoZSBsb2NrZWQgaW52ZW50b3J5IGRlY2xhcmVz
IG5vbmUsIHNvIHNpbGVuY2UgaGVyZSBpcyBpbmVydC1ieS1pbnZlbnRvcnksIG5vdCBhIHRlc3Qg
cGFzc2VkIgogICAgfSwKICAgICJGLVFVQU5UQS0yIjogewogICAgICAic3RhdGUiOiAiU0lMRU5U
IiwKICAgICAgImhpdHMiOiBbXSwKICAgICAgInRvd2VyX3Jvd3NfZXhhbWluZWQiOiBbCiAgICAg
ICAgIkNEIFRvd2VyIFJ1bmdzIChlLmcuLCA0Mi84NCkiCiAgICAgIF0KICAgIH0sCiAgICAiRi1R
VUFOVEEtMyI6IHsKICAgICAgInN0YXRlIjogIlJFR0lTVEVSRURfTk9UX0VYRUNVVEVEIiwKICAg
ICAgIm5vdGUiOiAibm8gZGVyaXZlZCBFX2JpbmRpbmcgZXhpc3RzIGluIHRoZSBmcmFtZXdvcms7
IHRlc3RzIHNjYWxlIHNlcGFyYXRpb24sIG5vdCB0aGUgc3RhYmlsaXR5IGRpc2NyaW1pbmF0b3Ii
CiAgICB9CiAgfSwKICAicHJvbW90aW9uX2NvbmRpdGlvbnMiOiB7CiAgICAiUEMtMV9ub250cml2
aWFsX3BhcnRpdGlvbiI6IHsKICAgICAgIm1ldCI6IHRydWUsCiAgICAgICJuX3Bhc3MiOiAzLAog
ICAgICAibl9mYWlsIjogMwogICAgfSwKICAgICJQQy0yX2luZGVwZW5kZW5jZV93aXRuZXNzIjog
ewogICAgICAibWV0IjogdHJ1ZSwKICAgICAgIndpdG5lc3NlcyI6IFsKICAgICAgICAiS+KChyBW
b3J0ZXgiCiAgICAgIF0sCiAgICAgICJleGNsdWRlZF9jbGFzcyI6ICJSaWdpZCBDb25zdHJhaW50
IgogICAgfSwKICAgICJQQy0zX2NvbmNvcmRhbmNlX3dpdGhfc2VjdGlvbl81IjogIkRFRkVSUkVE
IHRvIGBjb21wYXJlYCAoY29tcGFyaXNvbiBzdGVwIGxhc3QpIgogIH0sCiAgIlQxX3Bvc3Rfd3Jp
dGUiOiB7CiAgICAic3RhdGUiOiAiTElTVF9BQlNFTlQiLAogICAgImRldmlhdGlvbiI6ICJELVQx
OiBzZWxmLWdyZXAgc2tpcHBlZCwgbGlzdCBub3Qgc3VwcGxpZWQiCiAgfQp9
=====END-EMBED name=g_quanta_chatleg_checkpoint.json=====

=====BEGIN-EMBED name=g_quanta_chatleg_compare.json md5=a5726e1efbc2feae46e43060df0250f5 bytes=1333 encoding=base64 armor_bytes=1804 QUARANTINED=====
ewogICJnYXRlIjogIkctUVVBTlRBIiwKICAic3RlcCI6ICJjb21wYXJlIChQQy0zLCBjb21wYXJp
c29uIGxhc3QpIiwKICAiY2hlY2twb2ludCI6ICJnX3F1YW50YV9jaGF0bGVnX2NoZWNrcG9pbnQu
anNvbiIsCiAgImNoZWNrcG9pbnRfbWQ1IjogIjU1ODYxMTYxNzQ4ZmNhNjM0NTM0NzkwZjM2NjM4
MGZkIiwKICAibWVtb19tZDUiOiAiMDAzOWQwMDE3Njk1NjkyOTdjMmFhOGNjYmRlZDVhM2IiLAog
ICJyb3dzIjogWwogICAgewogICAgICAibGFiZWwiOiAiTF9CIEJvcnJvbWVhbiBCYXJ5b24iLAog
ICAgICAib2JqZWN0IjogIkxfQiBCb3Jyb21lYW4gQmFyeW9uIiwKICAgICAgInByZWRpY3RlZCI6
ICJQQVNTIiwKICAgICAgIm1hY2hpbmUiOiAiUEFTUyIsCiAgICAgICJjb25jb3JkYW50IjogdHJ1
ZQogICAgfSwKICAgIHsKICAgICAgImxhYmVsIjogIkvigocgVm9ydGV4IiwKICAgICAgIm9iamVj
dCI6ICJL4oKHIFZvcnRleCIsCiAgICAgICJwcmVkaWN0ZWQiOiAiUEFTUyIsCiAgICAgICJtYWNo
aW5lIjogIlBBU1MiLAogICAgICAiY29uY29yZGFudCI6IHRydWUKICAgIH0sCiAgICB7CiAgICAg
ICJsYWJlbCI6ICJFbGVjdHJvbiAyz4AgQ2xvc3VyZSIsCiAgICAgICJvYmplY3QiOiAiRWxlY3Ry
b24gMs+AIENsb3N1cmUiLAogICAgICAicHJlZGljdGVkIjogIlBBU1MiLAogICAgICAibWFjaGlu
ZSI6ICJQQVNTIiwKICAgICAgImNvbmNvcmRhbnQiOiB0cnVlCiAgICB9LAogICAgewogICAgICAi
bGFiZWwiOiAiQ2xpZmZvcmQgVW5rbm90IiwKICAgICAgIm9iamVjdCI6ICJDbGlmZm9yZCBVbmtu
b3QgLyBSdWxlIDE3IiwKICAgICAgInByZWRpY3RlZCI6ICJGQUlMIiwKICAgICAgIm1hY2hpbmUi
OiAiRkFJTCIsCiAgICAgICJjb25jb3JkYW50IjogdHJ1ZQogICAgfSwKICAgIHsKICAgICAgImxh
YmVsIjogIkNEIFRvd2VyIFJ1bmdzIiwKICAgICAgIm9iamVjdCI6ICJDRCBUb3dlciBSdW5ncyAo
ZS5nLiwgNDIvODQpIiwKICAgICAgInByZWRpY3RlZCI6ICJGQUlMIiwKICAgICAgIm1hY2hpbmUi
OiAiRkFJTCIsCiAgICAgICJjb25jb3JkYW50IjogdHJ1ZQogICAgfSwKICAgIHsKICAgICAgImxh
YmVsIjogIlNMV0UgTWF0cmljZXMiLAogICAgICAib2JqZWN0IjogIkNsdXN0ZXIgTSBTTFdFIE1h
dHJpY2VzIiwKICAgICAgInByZWRpY3RlZCI6ICJGQUlMIiwKICAgICAgIm1hY2hpbmUiOiAiRkFJ
TCIsCiAgICAgICJjb25jb3JkYW50IjogdHJ1ZQogICAgfQogIF0sCiAgIm9iamVjdHNfd2l0aG91
dF9oeXBvdGhlc2lzIjogW10sCiAgIlBDLTNfbWV0IjogdHJ1ZSwKICAidXRjIjogIjIwMjYtMDkt
MTBUMjA6MDI6MTguMDgyMDI1WiIKfQ==
=====END-EMBED name=g_quanta_chatleg_compare.json=====

