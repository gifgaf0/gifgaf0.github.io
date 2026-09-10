#!/usr/bin/env python3
"""Assemble the G-QUANTA CC-leg single-file return (P-4 mirrored, raw embeds)."""
import hashlib
import sys

EMBEDS = ['g_quanta_ccleg.py', 'g_quanta_ccleg_checkpoint.json',
          'g_quanta_ccleg_compare.json', 'g_quanta_twoleg_comparison.json']
OUT = 'G_QUANTA_CC_RETURN_INBAND.md'

header = open('return_header.md', 'rb').read()
parts = [header]
for name in EMBEDS:
    data = open(name, 'rb').read()
    md5 = hashlib.md5(data).hexdigest()
    parts.append(f'=====BEGIN-EMBED name={name} md5={md5} bytes={len(data)} encoding=raw=====\n'.encode())
    parts.append(data)
    if not data.endswith(b'\n'):
        parts.append(b'\n')
    parts.append(f'=====END-EMBED name={name}=====\n\n'.encode())
blob = b''.join(parts)
open(OUT, 'wb').write(blob)
print(f'{OUT}  md5 {hashlib.md5(blob).hexdigest()}  {len(blob):,} B')
