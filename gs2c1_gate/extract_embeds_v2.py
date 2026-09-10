#!/usr/bin/env python3
# extract_embeds_v2.py — byte-exact extraction of every embed in a P-4 dispatch, with P-4.b base64 armor.
# Usage: python3 extract_embeds_v2.py <dispatch.md> [outdir] [--quarantine-dir DIR]
# Markers:  <<<EMBED-BEGIN name=NAME md5=HEX bytes=N enc=raw|b64 quarantine=0|1>>>  ...  <<<EMBED-END name=NAME>>>
# raw: payload is the file's UTF-8 text verbatim (file must end with a newline).  b64: payload is base64 (76-col lines).
# Every embed is verified against md5 + byte count; any mismatch aborts. quarantine=1 embeds are written to the
# quarantine dir (default ./QUARANTINE) and MUST NOT be opened before the CC checkpoint is hashed (procedural blindness).
import sys, os, re, base64, hashlib
BEGIN = "<<<EMBED-" + "BEGIN name=(\\S+) md5=([0-9a-f]{32}) bytes=(\\d+) enc=(raw|b64) quarantine=([01])>>>\n"
END = "<<<EMBED-" + "END name=%s>>>"
def main(path, outdir=".", qdir=None):
    qdir = qdir or os.path.join(outdir, "QUARANTINE"); os.makedirs(outdir, exist_ok=True); os.makedirs(qdir, exist_ok=True)
    text = open(path, "rb").read().decode("utf-8"); n = 0
    for m in re.finditer(BEGIN, text):
        name, md5, nbytes, enc, q = m.group(1), m.group(2), int(m.group(3)), m.group(4), m.group(5) == "1"
        j = text.find(END % name, m.end()); assert j > 0, "END marker missing: " + name
        seg = text[m.end():j]
        payload = seg.encode("utf-8") if enc == "raw" else base64.b64decode("".join(seg.split()))
        assert len(payload) == nbytes, "byte count mismatch %s: %d vs %d" % (name, len(payload), nbytes)
        assert hashlib.md5(payload).hexdigest() == md5, "md5 mismatch: " + name
        dest = os.path.join(qdir if q else outdir, name); open(dest, "wb").write(payload)
        print("OK  %s  %s  %d B  %s%s" % (md5, name, nbytes, enc, "  [QUARANTINE]" if q else "")); n += 1
    print("extracted %d embeds, all md5/byte-verified" % n)
if __name__ == "__main__":
    a = sys.argv[1:]; qd = None
    if "--quarantine-dir" in a: i = a.index("--quarantine-dir"); qd = a[i + 1]; a = a[:i] + a[i + 2:]
    main(a[0], a[1] if len(a) > 1 else ".", qd)
