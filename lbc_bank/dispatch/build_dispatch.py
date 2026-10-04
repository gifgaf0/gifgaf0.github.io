#!/usr/bin/env python3
"""Assemble LBC_SECOND_LEG_DISPATCH_INBAND.md: the plaintext body + embeds E1-E4 in the clear + E5-E6 base64-sealed
+ manifest + a self-contained extractor."""
import base64, hashlib
body = open("dispatch_text.md", encoding="utf-8").read()
emb = [("E1", "T1_base_author_20260919.txt", False), ("E2", "t1_scan.py", False), ("E3", "lbc_2leg_compare.py", False),
       ("E4", "lbc_2leg_schema_v1.0_skeleton.json", False), ("E5", "lbc_chat_checkpoint.json", True),
       ("E6", "lbc_chat_instruments.tar.gz", True)]
md5 = lambda b: hashlib.md5(b).hexdigest()
out = [body, "\n## Manifest\n\n| embed | file | bytes | md5 | form |\n|---|---|---|---|---|\n"]
for tag, fn, sealed in emb:
    b = open(fn, "rb").read()
    out.append(f"| {tag} | `{fn}` | {len(b):,} | `{md5(b)}` | {'SEALED base64' if sealed else 'plaintext'} |\n")
for tag, fn, sealed in emb:
    b = open(fn, "rb").read()
    if sealed:
        enc = base64.b64encode(b).decode()
        lines = "\n".join(enc[i:i+100] for i in range(0, len(enc), 100))
        out.append(f"\n<!-- BEGIN {tag} {fn} SEALED-BASE64 md5={md5(b)} -->\n```\n{lines}\n```\n<!-- END {tag} -->\n")
    else:
        out.append(f"\n<!-- BEGIN {tag} {fn} PLAINTEXT md5={md5(b)} -->\n````text\n{b.decode('utf-8')}````\n<!-- END {tag} -->\n")
extractor = r'''
## Extractor

Save as `extract_embeds.py` next to this file and run `python3 extract_embeds.py LBC_SECOND_LEG_DISPATCH_INBAND.md E1 E2 E3 E4`
(later: `E5 E6`). Each embed is written to the current directory and its md5 checked against the BEGIN marker.

````python
import base64, hashlib, re, sys
src = open(sys.argv[1], encoding="utf-8").read()
for tag in sys.argv[2:]:
    m = re.search(r"<!-- BEGIN %s (\S+) (PLAINTEXT|SEALED-BASE64) md5=([0-9a-f]{32}) -->\n(?:````text|```)\n(.*?)\n?(?:````|```)\n<!-- END %s -->" % (tag, tag), src, re.S)
    fn, form, want, payload = m.group(1), m.group(2), m.group(3), m.group(4)
    data = base64.b64decode("".join(payload.split())) if form == "SEALED-BASE64" else (payload + ("\n" if not payload.endswith("\n") else "")).encode("utf-8")
    got = hashlib.md5(data).hexdigest()
    open(fn, "wb").write(data)
    print(tag, fn, len(data), "bytes", "md5 OK" if got == want else "MD5 MISMATCH " + got)
````
'''
out.append(extractor)
open("LBC_SECOND_LEG_DISPATCH_INBAND.md", "w", encoding="utf-8").write("".join(out))
print("written")
