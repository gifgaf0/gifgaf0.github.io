#!/usr/bin/env python3
"""extract_embeds_G_S2C1_W.py — P-4 extractor for G_S2C1_W_CC_DISPATCH_INBAND.md (the ONLY reader of embedded artifacts, P-4.c).
Convention (recovered G-POLY1 extractor): payload = span between the BEGIN marker line's trailing newline and the newline
before the END marker line, plus one trailing newline. ARMORED embeds are base64 text; decoded bytes are written
(P-4.b for quarantined content; also used for byte-exactness of any artifact lacking a trailing newline).
Every extracted artifact is verified against the DECLARED (md5, bytes) table; any mismatch halts (verify-then-build)."""
import os, re, sys, base64, hashlib
DISPATCH = os.environ.get('GS2C1W_DISPATCH', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'G_S2C1_W_CC_DISPATCH_INBAND.md'))
OUT = os.path.join(os.path.dirname(os.path.abspath(DISPATCH)), 'embeds'); os.makedirs(OUT, exist_ok=True)
DECLARED = [  # (name, md5, bytes, armored)
    ('staging_memo_G_S2C1_W.md', '1ebb6a82fcb24e207b164a654eb94dd1', 32219, False),
    ('G_S2C1_W_LOCK_RECORD.md', '5f963ed8d7eff9f803da5c1eea2f841a', 10875, False),
    ('G_S2C1_W_LOCK_RECORD_ADDENDUM_1.md', '125809174278cc7738692fd783d4ecd7', 7207, False),
    ('t1_forbidden_G_S2C1_W.txt', '20ba1e7eab5a3bbffe510b4840edbc57', 1560, False),
    ('t1_forbidden_G_S2C1_W_A1.txt', '735eae308aa7baec19f23da5602a2d82', 39, True),
    ('pinned_inputs_G_S2C1_W.json', 'd1edc69b16dfd0b728a48cd8389b322b', 5769, True),
    ('anchors_G_S2C1_W_SEALED.md', '8c7d59f64057e372d7b1ff760667a7c2', 154, True),
    ('g_s2c1w_mapper_v6.py', 'e034d4281c4a2906377e1587672cc128', 26458, True),
    ('g_s2c1w_compare_v1_0.py', '007688e5d8ea45d6848fd8e99c57a7d8', 4665, False),
    ('g_s2c1w_schema_v1_0.json', 'dd014b8cc4c48e5dbf356e96baded753', 1382, False),
    ('MANIFEST_gpoly1_phase3.md5', '3b178fb26068050c9f8c4866edce4078', 792, False),
    ('t1_scan.py', 'ccd47ac5779c6592bb3c49d6890049e9', 2138, False),
    ('extract_embeds_G_S2C1_W.py', 'SELF', 0, False),
]
src = open(DISPATCH, 'rb').read().decode('utf-8'); fail = 0
for name, want, size, armored in DECLARED:
    m = re.search(r'<<<BEGIN ' + re.escape(name) + r'>>>\n(.*?)\n<<<END ' + re.escape(name) + r'>>>', src, re.S)
    if not m: print(f'MISSING {name}'); fail += 1; continue
    payload = m.group(1) + '\n'
    data = base64.b64decode(payload.encode('ascii')) if armored else payload.encode('utf-8')
    got = hashlib.md5(data).hexdigest()
    ok = (want == 'SELF') or (got == want and len(data) == size)
    print(f"{'OK  ' if ok else 'FAIL'} {name:42s} {got} {len(data):>7} B{'  [armored]' if armored else ''}")
    fail += 0 if ok else 1
    open(os.path.join(OUT, name), 'wb').write(data)
print('EXTRACTION', 'ALL OK' if not fail else f'FAILED x{fail}'); sys.exit(1 if fail else 0)
