#!/usr/bin/env python3
# CC leg — embed extraction + verify-then-build for the G-POLY1 Phase 3 dispatch.
# Extraction convention (dispatch §1): payload = span between the BEGIN marker
# line's trailing newline and the newline before the END marker line; if the
# declared byte count indicates no trailing newline, strip the single added
# newline. On any mismatch: HALT and report.
import hashlib, os, re, sys

DISPATCH = '/root/.claude/uploads/fd51e6d6-bff6-58be-8501-73e857edc3dc/8194856d-G_POLY1_PHASE3_CC_DISPATCH_INBAND.md'
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'embeds')
os.makedirs(OUT, exist_ok=True)

DECLARED = [
    ('staging_memo_G_POLY1_phase3.md',            'e16a78906560d2bb076d0699966981ac', 7965),
    ('staging_memo_G_POLY1_phase3_ADDENDUM_1.md', 'ba75b113e8ad094cd752026df4e73977', 5066),
    ('staging_memo_G_POLY1_phase3_ADDENDUM_2.md', 'ac87bc92890c7bf6a08b3d67d493ec9c', 3567),
    ('staging_memo_G_POLY1_phase3_ADDENDUM_3.md', '257b81bf3924cb92ca9d1232fb94325c', 4247),
    ('G_POLY1_PHASE3_LOCK_RECORD.md',             'abb463d75a96fc9913123562ff1fecbf', 2167),
    ('G_POLY1_PHASE3_RELOCK_RECORD.md',           '7f4b53ad43af3aff55938726d8f26738', 1368),
    ('G_POLY1_PHASE3_RELOCK_RECORD_2.md',         'b1150c946f6986a9bc19ae2b073db83e',  963),
    ('G_POLY1_PHASE3_RELOCK_RECORD_3.md',         '6a7069b07c2184eea41dfc38b4446c9d', 1531),
    ('anchors_G_POLY1_SEALED.md',                 'a1d19dd98151cd7299af41fb14584c6f', 2470),
    ('g_poly1_phase3_mapper_v4.py',               '413996ae82cdb16545e5568622ee89ca', 24906),
    ('G_POLY1_PIN_ADDENDUM_1_hexGHS.md',          '57dfd40e5f0dbb311a64b30a67a47df6', 5441),
    ('G_POLY1_PIN_ADDENDUM_2_tetragonal.md',      '3d419b8f7196efd895fc5079df8760b4', 3449),
    ('poly_vrh_results.json',                     '200e7a8b775577564369c6924d38a84c', 2767),
    ('g_poly1_hexghs_chatleg_v3.py',              'fba6439a3a14d8cbab19939f4ff33f39', 13024),
    ('poly1_hexghs_chat.json',                    'd74916a22984deab514e11164ef88725', 4107),
]

src = open(DISPATCH, 'rb').read().decode('utf-8')
fail = 0
print(f'{"embed":45s} {"bytes":>6s}  md5                               verdict')
for name, want_md5, want_bytes in DECLARED:
    m = re.search(r'<<<BEGIN ' + re.escape(name) + r'>>>\n(.*?)\n<<<END ' + re.escape(name) + r'>>>',
                  src, re.S)
    if not m:
        print(f'{name:45s} MARKERS NOT FOUND — HALT'); fail += 1; continue
    payload = m.group(1) + '\n'                      # span keeps interior; END strips last \n, re-add
    data = payload.encode('utf-8')
    if len(data) == want_bytes + 1 and data.endswith(b'\n'):
        data = data[:-1]                             # declared count says no trailing newline
    got = hashlib.md5(data).hexdigest()
    ok = (got == want_md5 and len(data) == want_bytes)
    print(f'{name:45s} {len(data):6d}  {got}  {"PASS" if ok else "MISMATCH — HALT"}')
    if not ok: fail += 1
    open(os.path.join(OUT, name), 'wb').write(data)

if fail:
    print(f'\nVERIFY-THEN-BUILD: {fail} FAILURE(S) — HALT, nothing built.'); sys.exit(1)
print('\nVERIFY-THEN-BUILD: all 15 embeds re-extracted and md5-verified. PASS.')
