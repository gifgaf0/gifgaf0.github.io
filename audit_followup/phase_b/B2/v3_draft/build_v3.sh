#!/usr/bin/env bash
# B2: rebuild the v3 DRAFT of the PSL(2,7) note from the author's v2.1 docx.
# Usage: build_v3.sh SOURCE_DOCX OUT_DIR DOCX_SKILL_DIR
#   SOURCE_DOCX    PSL27_Spectral_Rigidity_corrected_v2_1.docx (md5 9e80932408379a1c44813c56afa0327b)
#   OUT_DIR        empty working directory
#   DOCX_SKILL_DIR directory holding scripts/merge_runs.py, scripts/office/validate.py, scripts/accept_changes.py
# Result: OUT_DIR/PSL27_v3_DRAFT_tracked.docx (every change a tracked insertion or deletion by
#         "Claude (audit draft)") and OUT_DIR/PSL27_v3_DRAFT_clean.docx (all changes accepted).
# Check : word/document.xml of the tracked draft has md5 f667eaf71e53c1e42be1566e5e574271.
set -euo pipefail
SRC="$(readlink -f "$1")"; OUT="$(readlink -f "$2")"; SK="$(readlink -f "$3")"
HERE="$(cd "$(dirname "$0")" && pwd)"
test "$(md5sum < "$SRC" | cut -d' ' -f1)" = "9e80932408379a1c44813c56afa0327b" || { echo "source md5 mismatch"; exit 1; }
mkdir -p "$OUT/unpacked"
unzip -q "$SRC" -d "$OUT/unpacked"
find "$OUT/unpacked" -type l -delete
python3 "$SK/scripts/merge_runs.py" "$OUT/unpacked"
python3 "$HERE/make_v3_tracked.py" "$OUT/unpacked"
md5sum "$OUT/unpacked/word/document.xml"
(cd "$OUT/unpacked" && rm -f ../PSL27_v3_DRAFT_tracked.docx && zip -qXr ../PSL27_v3_DRAFT_tracked.docx .)
python3 "$SK/scripts/office/validate.py" "$OUT/PSL27_v3_DRAFT_tracked.docx" --original "$SRC" --author "Claude (audit draft)"
python3 "$SK/scripts/accept_changes.py" "$OUT/PSL27_v3_DRAFT_tracked.docx" "$OUT/PSL27_v3_DRAFT_clean.docx"
