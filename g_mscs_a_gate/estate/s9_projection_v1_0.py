#!/usr/bin/env python3
"""s9_projection_v1_0.py -- G-MSCS-A S9 path (a): a verdict-blind projection applied identically to BOTH Phase-3 checkpoints
before the frozen comparator is re-run. Neither checkpoint is edited; the projected copies are new files.

The two representational readings it reconciles (S9-SA-1, S9-SA-2; memo section 6.5, the path-(a) mini-dispatch pattern):
  S9-SA-1  phase3.rows[j] key set: the chat row carries gate_class_row, geom and q (memo 4.3 calls geom and q "serialized";
           A-2.4 says per-row mappings carry "the same structure as the combined one"); the CC row carries neither.
           Projection: keep only the common keys {id, row_md5, void_regime, contains_zero, families, exclusion, two_param}.
  S9-SA-2  the NULL-INERT record (the cubic t2 family): A-2.4 says "class NULL-INERT, window [-D, +D], the other fields null";
           the chat mapper wrote the four boolean flags as false, the CC mapper as null.
           Projection: on every record whose class is NULL-INERT, the four flags are set to null (the A-2.4 literal reading).
Nothing else is touched: no class, edge, flag of a mapped cell, identity field, control, null or count.
Usage: python3 s9_projection_v1_0.py IN.json OUT.json   (prints the md5 of the projected file and what it changed)"""
import hashlib, json, sys

COMMON_ROW_KEYS = {'id', 'row_md5', 'void_regime', 'contains_zero', 'families', 'exclusion', 'two_param'}
NULL_INERT_FLAGS = ('nu_is_inf', 'nullfloor_sensitive', 'resolution_sensitive', 'truncation_sensitive')


def project(ck):
    n_keys = n_flags = 0
    p3 = ck.get('phase3')
    if not p3:
        return ck, 0, 0
    for row in p3.get('rows') or []:
        for k in list(row):
            if k not in COMMON_ROW_KEYS:
                del row[k]; n_keys += 1
    def fams(block):
        nonlocal n_flags
        if not block or not block.get('families'):
            return
        for key, arms in block['families'].items():
            for arm, fam in arms.items():
                for f, rec in fam.items():
                    if rec.get('class') == 'NULL-INERT':
                        for fl in NULL_INERT_FLAGS:
                            if rec.get(fl) is not None:
                                rec[fl] = None; n_flags += 1
    fams(p3.get('combined'))
    for row in p3.get('rows') or []:
        fams(row)
    return ck, n_keys, n_flags


if __name__ == '__main__':
    ck = json.load(open(sys.argv[1]))
    ck, nk, nf = project(ck)
    data = (json.dumps(ck, indent=1, sort_keys=True, ensure_ascii=True, allow_nan=False) + '\n').encode('ascii')
    open(sys.argv[2], 'wb').write(data)
    print('%s -> %s  md5 %s  %d B  (row keys dropped %d; NULL-INERT flags set to null %d)' % (sys.argv[1], sys.argv[2], hashlib.md5(data).hexdigest(), len(data), nk, nf))
