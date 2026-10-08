#!/usr/bin/env bash
# Step 2b: rebuild the PSL(2,7) note v3 from the author's v2.1 docx with the Phase B edits (E1–E10) and the
# close-out edits (E11–E13). Usage: build_v3_closeout.sh SOURCE_DOCX OUT_DIR DOCX_SKILL_DIR [A|B]
set -euo pipefail
SRC="$(readlink -f "$1")"; OUT="$(readlink -f "$2")"; SK="$(readlink -f "$3")"; T="${4:-A}"
HERE="$(cd "$(dirname "$0")" && pwd)"
B2="$HERE/../../../phase_b/B2/v3_draft"
test "$(md5sum < "$SRC" | cut -d' ' -f1)" = "9e80932408379a1c44813c56afa0327b" || { echo "source md5 mismatch"; exit 1; }
rm -rf "$OUT/unpacked"; mkdir -p "$OUT/unpacked"
unzip -q "$SRC" -d "$OUT/unpacked"
find "$OUT/unpacked" -type l -delete
python3 "$SK/scripts/merge_runs.py" "$OUT/unpacked"
python3 "$B2/make_v3_tracked.py" "$OUT/unpacked"
python3 "$HERE/make_v3_closeout.py" "$OUT/unpacked" "$T"
md5sum "$OUT/unpacked/word/document.xml"
N="PSL27_v3_CLOSEOUT_DRAFT_title$T"
(cd "$OUT/unpacked" && rm -f "../${N}_tracked.docx" && zip -qXr "../${N}_tracked.docx" .)
python3 "$SK/scripts/office/validate.py" "$OUT/${N}_tracked.docx" --original "$SRC" --author "Claude (audit draft)"
python3 "$SK/scripts/accept_changes.py" "$OUT/${N}_tracked.docx" "$OUT/${N}_clean.docx"
