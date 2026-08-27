#!/usr/bin/env python3
# extract_embeds_G_2a_L1.py — byte-exact extraction of every embed in the
# G-2a-L1 in-band dispatch. Usage: python3 extract_embeds_G_2a_L1.py G_2a_L1_CC_DISPATCH_INBAND.md [outdir]
# Every embed is verified against the md5 and byte count declared in its BEGIN marker.
# Any mismatch aborts (verify-then-build: nothing is built on an unverified embed).
import sys, os, re, hashlib

BEGIN = "<<<EMBED-" + "BEGIN name=(\\S+) md5=([0-9a-f]{32}) bytes=(\\d+)>>>\n"
END   = "<<<EMBED-" + "END name=%s>>>"

def main(path, outdir="."):
    data = open(path, "rb").read()
    text = data.decode("utf-8")
    n = 0
    for m in re.finditer(BEGIN, text):
        name, md5, nbytes = m.group(1), m.group(2), int(m.group(3))
        start = m.end()
        endmark = (END % name)
        j = text.find(endmark, start)
        assert j > 0, "END marker missing for " + name
        payload = text[start:j].encode("utf-8")
        got = hashlib.md5(payload).hexdigest()
        assert len(payload) == nbytes, "byte count mismatch %s: %d vs %d" % (name, len(payload), nbytes)
        assert got == md5, "md5 mismatch %s: %s vs %s" % (name, got, md5)
        out = os.path.join(outdir, name)
        open(out, "wb").write(payload)
        print("OK  %s  %s  %d B" % (md5, name, nbytes))
        n += 1
    print("extracted %d embeds, all md5/byte-verified" % n)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else ".")
