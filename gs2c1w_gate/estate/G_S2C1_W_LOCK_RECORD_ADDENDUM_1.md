# G-S2C1-W — LOCK RECORD ADDENDUM 1 (sealed anchors; T1-A1; declared CC checkpoint; delivery deviations)

**Date:** September 8, 2026. **Amends:** `G_S2C1_W_LOCK_RECORD.md` `5f963ed8d7eff9f803da5c1eea2f841a` (10,875 B) under its §7 gate sequence. **Memo:** `1ebb6a82fcb24e207b164a654eb94dd1` LOCKED (untouched). **Pinned inputs:** `pinned_inputs_G_S2C1_W.json` `d1edc69b16dfd0b728a48cd8389b322b` — **AUTHOR-VERIFIED** (directive of this date; §7 gate 3 GREEN).

## 1. Author directive (verbatim, operative clauses)

> The lock record, frozen T1 list, and the pinned inputs JSON are confirmed. I explicitly VERIFY the contents of `pinned_inputs_G_S2C1_W.json` (d1edc69b16dfd0b728a48cd8389b322b). I provide the sealed anchor file and the T1-A1 addition below.
> 1. Generate the Lock Record Addendum stating the MD5 of the sealed anchor file and the MD5 of T1-A1. 2. The sealed file contains 1 row (`disp` class). Confirm this census. 3. Build the chat instrument (mapper v6). Run the pre-read suites (C-SYN-D). 4. Build the frozen comparator and schema. 5. Construct the P-4/P-4.b/P-4.c single-file in-band CC dispatch (`G_S2C1_W_CC_DISPATCH_INBAND.md`). Ensure ALL constraints of P-4.c are met: the dispatch must be completely self-contained with no loose files. 6. The CC leg has been executed externally. The CC checkpoint md5 is: `97f26c04f982b1cc1694f4a47bdce882`. (Use this hash in the closure log). 7. Unseal the anchors, execute the Chat leg read, run the comparator against the CC checkpoint hash, and report the verdict.

## 2. SEALED — the anchor file (E-W-4(i), author-supplied)

`anchors_G_S2C1_W_SEALED.md` — md5 **`8c7d59f64057e372d7b1ff760667a7c2`**, **154 B**. Canonical serialization of record: the one row exactly as supplied between the author's BEGIN/END markers, followed by a single trailing newline (LF), UTF-8, no leading pipe. **Census (confirmed by machine): 1 row; per-class {`disp`: 1}; 8 pipe-delimited fields per row (7 content fields + the trailing empty field from the closing bar); separator guard PASS (no bar inside any field).** Field map bound by NAMED KEY (never by magnitude window — the G-CI1 S9 root cause (A) rule): f0 class, f1 anchor id, f2 source designation (masked in every artifact), f3 binding quantity q ∈ {phase, group}, f4 `B = <budget>`, f5 `k = <wavenumber> /m`, f6 Caveat/Binding clause (carried verbatim inside the sealed file only; masked elsewhere). The file is a justified T1-scan exemption (as at G-POLY1). Opened ONLY by the mapper phase, single read per leg, md5 + census asserted at open.

**C-W-3 pin for the CC leg:** the CC checkpoint must carry `sealed_md5 = 8c7d59f64057e372d7b1ff760667a7c2` and the same census; a differing sealed md5 on the CC side means a differing serialization (whitespace/newline), to be resolved by byte comparison of the two files, not by re-reading.

## 3. FROZEN — T1 Addendum 1

`t1_forbidden_G_S2C1_W_A1.txt` — md5 **`735eae308aa7baec19f23da5602a2d82`**, **39 B, 4 pattern lines** (author-supplied, byte-exact as delivered, LF-terminated). One line duplicates a base-list pattern (harmless; the scan is a set union). **Effective T1 of this gate = base `20ba1e7e` ∪ A1 `735eae30` = 37 distinct patterns**, scanned on every instrument invocation and on every artifact under the D-W-7 rule (numeric patterns: hit only when glued to a letter/underscore token; digit/sign/dot glue and exponent suffixes logged, not fatal). Two of the four A1 lines are numeric (the sealed budget and wavenumber): they will appear as parsed NUMBERS in both legs' checkpoints — expected LOGGED collisions, not hits; their appearance in any instrument SOURCE is a hit and a halt.

## 4. DECLARED — the CC checkpoint

CC leg executed EXTERNALLY by the author's direction before this addendum existed. Declared CC checkpoint md5: **`97f26c04f982b1cc1694f4a47bdce882`** (file name, byte size, branch, and commit NOT declared). This hash is the C-W identity anchor for the CC side. **The file itself is not in the chat workspace at the time of this addendum** — see D-W-10 and the re-lock-4 gate pattern (§7 gate 7: the CC checkpoint must be PRESENT AND HASHED in the chat workspace before comparison). Recovery attempt from the repository is logged in the closure log.

## 5. Deviations and honesty items logged AT DELIVERY (pre-instrument, pre-read)

- **H-W-2 (chat blindness burned at delivery).** The sealed row was delivered IN THE CLEAR inside the directive body (not as an armored file), so the chat leg read the anchor values before the chat instrument was written. Consequence (the G-POLY1 H-16 → E3-5(a) precedent): **the CC read is the verdict read of record for the CLASS (E-W-5(a) already elected); the chat read is a POST-EXPOSURE re-run** — its value is reproduction on an independent implementation plus the lexer/edge cross-check, not blind concurrence. The chat instrument is nevertheless written values-blind by construction (reads only the sealed file; contains no anchor string; T1 self-grep base ∪ A1 at every invocation) and its synthetic suites use values disjoint from the sealed ones.
- **D-W-8 (P-4.b not performed on the author→chat delivery).** Quarantined content travelled unarmored to the chat leg. P-4.b/P-4.c bind leg dispatches; the author→chat channel is not a leg dispatch, but the effect (exposure) is the same and is recorded as H-W-2.
- **D-W-9 (order deviation).** The CC leg executed before the in-band dispatch and the frozen comparator existed. The dispatch is built after the fact as the canonical package (for the record, for any S9 re-run, and for the return manifest); the comparator is frozen BEFORE the chat emission only — the "frozen before either emission" property holds on the chat side, not the CC side. Not fold-blocking; disclosed.
- **D-W-10 (CC checkpoint absent).** Hash declared, file absent; comparison C-W-1..6 cannot execute on a hash — a comparator compares VALUES. Status at addendum: OUTSTANDING pending the file (or its recovery from the repository), the D-S2C1-1 pattern.
- **Q-W-1 (query, recorded not acted on; R-B class, post-parse):** the sealed row binds a wavenumber field to a named source; the instrument reads the sealed text as dispositive (the G-CI1 rule) and does not re-derive k from the source's own emission. Any consistency question between the stated k and the named source's radiation wavenumber is the author's to answer in a sealed-file revision (which would be a new sealed md5 + a new addendum), never the instrument's to correct.

## 6. Gate status after this addendum (lock record §7)

1 sealed file — **GREEN** (`8c7d59f6`, census 1/disp). 2 T1-A1 — **GREEN** (`735eae30`). 3 JSON verified — **GREEN**. 4 chat instrument + suites — proceeds now (post-exposure, H-W-2). 5 comparator frozen pre-chat-emission — proceeds now (D-W-9). 6 dispatch — built now, after the fact (D-W-9); P-4/P-4.b/P-4.c honored in construction. 7 CC-blind-first read — **executed externally**, hash `97f26c04…` declared, file absent (D-W-10). 8 chat read + comparison — chat read proceeds; comparison contingent on the CC file.

Elections E-W-1..7 and defaults unchanged. No fold authorized by this addendum.
