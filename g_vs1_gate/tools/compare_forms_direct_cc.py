#!/usr/bin/env python3
"""compare_forms_direct.py -- the C-VS-4 per-form checks the frozen comparator cannot address (its dotted-path lookup
splits the schema's form names on '.'), run with the form name treated as a single key. Exact equality; same key lists
as schema v1.0 (per_form_compared_deg4 / per_form_compared_deg2, chosen by the chat leg's recorded degree).
usage: compare_forms_direct.py SCHEMA CHAT.json CC.json [out.json]"""
import json, sys
schema = json.load(open(sys.argv[1])); A = json.load(open(sys.argv[2])); B = json.load(open(sys.argv[3]))
def eq(a, b): return json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)
res = []
formsChat = (A.get('phase3') or {}).get('F_a', {}); formsCC = (B.get('phase3') or {}).get('F_a', {})
for form in schema['phase3']['forms']:
    ra, rb = formsChat.get(form, {}), formsCC.get(form, {})
    deg = ra.get('degree', rb.get('degree'))
    keys = schema['phase3']['per_form_compared_deg4'] if deg == 4 else schema['phase3']['per_form_compared_deg2']
    for k in keys:
        va, vb = ra.get(k, '<MISSING>'), rb.get(k, '<MISSING>')
        ok = eq(va, vb) and va != '<MISSING>'
        res.append(dict(check='C-VS-4-direct', form=form, key=k, result='PASS' if ok else 'MISS', chat=None if ok else va, cc=None if ok else vb))
n = len(res); miss = [r for r in res if r['result'] != 'PASS']
summary = dict(checks=n, passed=n - len(miss), misses=len(miss), chat_forms_present=sorted(formsChat), cc_forms_present=sorted(formsCC))
print('direct per-form comparison: %d checks, %d PASS, %d MISS' % (n, n - len(miss), len(miss)))
for r in miss: print('  MISS', r['form'], r['key'], '| chat:', json.dumps(r['chat'], ensure_ascii=False)[:200], '| cc:', json.dumps(r['cc'], ensure_ascii=False)[:200])
if len(sys.argv) > 4: open(sys.argv[4], 'w').write(json.dumps(dict(summary=summary, results=res), indent=1, sort_keys=True, ensure_ascii=False))
