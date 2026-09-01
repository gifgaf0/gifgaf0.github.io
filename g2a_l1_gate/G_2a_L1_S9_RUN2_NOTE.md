# Gate G-2a-L1 — S9 RESOLUTION RUN-2 NOTE (CC side)

**Date:** 2026-08-28 (UTC). **Mini-dispatch:** `G_2a_L1_S9_MINIDISPATCH_INBAND.md` — md5 `8e27f85f0636d9050e67df256bbf8956` (18,721 B); all six embeds extracted and md5/byte-verified before anything was done (comparator v1.1 `faa233c0…`, chat checkpoint v1.1 `8abda98d…`, add-on + log, activation flags, extractor).

**Result: S9 CLOSED.** Comparator v1.1 on (chat v1.1, cc v1.1): C1–C6 ALL PASS, zero misses, VERDICT (base arms) IDENTICAL = (SPLIT, ASSEMBLED, NEUTRAL). Output captured verbatim in `comparator_v1_1_output.txt` — md5 `51f16e52c8ae08dd3ff324b008d8a575` (1,294 B). The two reported-only notes are exactly the v1.1-sanctioned ones: the free-text `arm_sharpened` pair and the chat `-RELOCATED` suffix.

## What the CC side did (activation flags honored)

1. **Re-emission, no recomputation, instrument untouched:** `g_2a_L1_cc_checkpoint_v1_1.json` — md5 `33d60888ab115cda00fe484fee5c14c1` (3,226 B) — produced by `g_2a_L1_reemit_cc_v1_1.py` (md5 `e36e300f04b5d867c8bad0e5700717c1`, 2,288 B), a pure representation transform of the committed v1.0 checkpoint (parent md5 `47ae0b85eee85781cddc93cb208441a7`, asserted before transforming). Changes, per the mini-dispatch §2: schema string; `Mplus_element_orders` as the set {1,2,3,4}; `GL23_transposition_class_size` retired in favor of `_PGL = 6` and `_GL = 12`; `reemission` block naming the parent and changes. Arms and `arm_sharpened` byte-identical to v1.0.
2. **Provenance of the two new C4 fields — already-verified facts, not new computation:** the v1.0 instrument run asserted both "F2: unique size-6 order-2 class (transpositions)" (PGL level) and "F2: the involution preimages form one GL(2,3) class of size 12" (GL level); see `g_2a_L1_ccleg.py` §run_F2 and the v1.0 run log. This matches the chat add-on's independent 𝔽₃ enumeration (`gl23_class_level_addon.log`: 12 preimages, all involutions).
3. **T1 scan:** zero hits on the re-emitted checkpoint and the re-emission script (grep exit 1).
4. **Instrument check:** `g_2a_L1_ccleg.py` md5 re-verified `c3bea9ee71765b196263ff2e5203708a` — untouched, as required.

## Return manifest (run-2)

| Artifact | md5 | bytes |
|---|---|---|
| `g_2a_L1_cc_checkpoint_v1_1.json` | 33d60888ab115cda00fe484fee5c14c1 | 3,226 |
| `comparator_v1_1_output.txt` | 51f16e52c8ae08dd3ff324b008d8a575 | 1,294 |
| `g_2a_L1_reemit_cc_v1_1.py` | e36e300f04b5d867c8bad0e5700717c1 | 2,288 |

The three ORIGINAL files the chat side needs for its own run-2 are in this same directory, byte-identical to the leg-1 return (md5s re-verified at this commit): `g_2a_L1_cc_checkpoint.json` (`47ae0b85…`), `G_2a_L1_CCLEG_REPORT.md` (`0d0bfbfbf6b864420f44abfa33e07baa`), `g_2a_L1_ccleg.py` (`c3bea9ee…`). Branch `claude/new-session-wrjklk`; leg-1 commits `75e185e` (pre-consultation) and `c87d2e9`.

**Non-claims carried:** nothing here changes any value, arm, or verdict of either leg; no fold; D-CC-1/D-CC-2 remain open for chat-side adjudication in the fold packet, exactly as the mini-dispatch states.
