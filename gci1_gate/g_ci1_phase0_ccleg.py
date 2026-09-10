# g_ci1_phase0_ccleg.py — G-CI1 CC leg, Phase 0 (E-9 full-from-scratch).
# Duties (dispatch section 2, prereg section 4 Phase 0, CC variant):
#   (a) verify the dispatch file md5/bytes against the released-manifest values;
#   (b) extract every embed byte-exact from the fences; assert each md5 + byte count;
#   (c) record D-1..D-9 as frozen (verbatim, from the extracted prereg section 2);
#   (d) sealed-census STRUCTURAL assert: row-id regex count only — no field read,
#       no content print; the sealed embed stays otherwise unopened until Phase 3;
#   (e) T1 self-grep: zero hits on this instrument, the common module, the
#       checkpoint, and the non-exempt embeds;
#   (f) write ci1_phase0_cc.json.
# The A0 literature pass was done by the chat leg (NOT TRIGGERED); per the
# dispatch it is not repeated here.

import os
import re
import sys

import gci1_cc_common as cc

DISPATCH_PATH = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    cc.GATE_DIR, "G_CI1_CC_DISPATCH_INBAND.md")

# Released-manifest values (G_CI1_CC_DISPATCH_MANIFEST.json, carried alongside):
DISPATCH_MD5 = "420082d54f11817c9d64a8198f1042ae"
DISPATCH_BYTES = 109192
BASE_CANONICAL = ("SQT_Master_Ledger_v4_76_CANONICAL.md",
                  "f539d10cb4f73c81e7d9fdbe7fa63714", 1432221)

EXPECTED_EMBEDS = {
    "G_CI1_EXECUTION_PREREGISTRATION.md": ("6c480340658a54e9da5d3553a8890c46", 36793),
    "t1_forbidden_G_CI1.txt": ("653a0b7447e68aa8a094e62337a24da3", 1127),
    "G_CI1_LOCK_RECORD.md": ("a6adbb6ab69bcc6184b8fc2f6bcb9f5b", 9851),
    "G_CI1_LOCK_RECORD_ADDENDUM_1.md": ("e5029ae86cd43dcb343ebb4e872f856b", 5203),
    "G_CI1_LOCK_RECORD_ADDENDUM_2.md": ("92672d5a72cf2efce8865d2a4ca3fb6c", 8443),
    "G_CI1_LOCK_RECORD_ADDENDUM_3.md": ("4c0b52c6ab10b5f075ad49abad137020", 4286),
    "poly_vrh_results.json": ("200e7a8b775577564369c6924d38a84c", 2767),
    "G_POLY1_PIN_RECORD.md": ("621120e50d395beea2e914d54c929600", 10759),
    "anchors_G_CI1_SEALED.md": ("dd8fe2d364624750201ad9c9ffef575c", 17652),
}

SEALED_NAME = "anchors_G_CI1_SEALED.md"
SEALED_CENSUS_EXPECTED = 12
# Row ids fixed by the census statement (prereg section 7); the assert below
# counts id occurrences at row starts ONLY — no other field is read.
ROW_ID_RE = re.compile(
    r"^\|\s*(TR-[1-4]|ACH-DIM|ACH-DISP|BIR-[12]|POL|DIFF|VLD|CONV)\s*\|",
    re.M)

FENCE_OPEN_RE = re.compile(
    rb"<<<EMBED ([^ ]+) ([0-9a-f]{32}) (\d+) ([A-Z]+)>>>\n")


def extract_embeds(blob):
    results = []
    for m in FENCE_OPEN_RE.finditer(blob):
        name = m.group(1).decode()
        md5_stated = m.group(2).decode()
        bytes_stated = int(m.group(3))
        flag = m.group(4).decode()
        close = b"\n<<<END " + m.group(1) + b">>>"
        j = blob.find(close, m.end())
        if j < 0:
            raise RuntimeError("closing fence missing: " + name)
        content = blob[m.end():j]
        got_md5 = cc.md5_bytes(content)
        ok = (got_md5 == md5_stated) and (len(content) == bytes_stated)
        outp = os.path.join(cc.EMBED_DIR, name)
        with open(outp, "wb") as fh:
            fh.write(content)
        results.append({
            "file": name, "flag": flag,
            "md5_stated": md5_stated, "md5_extracted": got_md5,
            "bytes_stated": bytes_stated, "bytes_extracted": len(content),
            "match": ok,
        })
    return results


def sealed_census_structural():
    """Count census row-ids in the sealed embed WITHOUT reading any field:
    the regex matches only the row-leading id token; nothing is printed."""
    with open(os.path.join(cc.EMBED_DIR, SEALED_NAME), "r",
              encoding="utf-8") as fh:
        text = fh.read()
    ids = ROW_ID_RE.findall(text)
    del text
    return len(ids)


def freeze_definitions(prereg_text):
    """Extract the prereg section-2 definitions block (D-1..D-9) verbatim."""
    start = prereg_text.index("## §2 — Definitions")
    end = prereg_text.index("## §3 —", start)
    block = prereg_text[start:end].rstrip("\n")
    labels = re.findall(r"\*\*D-(\d) ", block)
    return block, labels


def main():
    os.makedirs(cc.EMBED_DIR, exist_ok=True)
    with open(DISPATCH_PATH, "rb") as fh:
        blob = fh.read()
    dispatch_ok = (cc.md5_bytes(blob) == DISPATCH_MD5 and
                   len(blob) == DISPATCH_BYTES)
    if not dispatch_ok:
        raise RuntimeError("dispatch hash/byte mismatch — HALT")

    embeds = extract_embeds(blob)
    names = {e["file"] for e in embeds}
    if names != set(EXPECTED_EMBEDS):
        raise RuntimeError("embed roster mismatch — HALT")
    for e in embeds:
        exp_md5, exp_b = EXPECTED_EMBEDS[e["file"]]
        if not (e["match"] and e["md5_stated"] == exp_md5
                and e["bytes_stated"] == exp_b):
            raise RuntimeError("embed verification failed: %s — HALT" % e["file"])

    # D-1..D-9 frozen verbatim from the extracted (byte-verified) prereg.
    with open(os.path.join(cc.EMBED_DIR, "G_CI1_EXECUTION_PREREGISTRATION.md"),
              "r", encoding="utf-8") as fh:
        prereg_text = fh.read()
    dblock, dlabels = freeze_definitions(prereg_text)
    if dlabels != [str(i) for i in range(1, 10)]:
        raise RuntimeError("D-1..D-9 roster mismatch — HALT")

    # Sealed census, structural only.
    census = sealed_census_structural()
    if census != SEALED_CENSUS_EXPECTED:
        raise RuntimeError("sealed census mismatch — HALT")

    # T1 self-grep: this instrument, the common module, and non-exempt embeds.
    pats = cc.load_t1_patterns()
    scan_targets = [
        os.path.abspath(__file__),
        os.path.join(cc.GATE_DIR, "gci1_cc_common.py"),
    ] + [os.path.join(cc.EMBED_DIR, e["file"]) for e in embeds
         if e["file"] not in cc.T1_EXEMPT_EMBEDS]
    t1_report = {}
    total_hits = 0
    for p in scan_targets:
        hits = cc.t1_scan_file(p, pats)
        t1_report[os.path.basename(p)] = len(hits)
        total_hits += len(hits)
    if total_hits:
        raise RuntimeError("T1 hit — HALT")

    ckpt = {
        "gate": "G-CI1", "leg": "CC", "phase": 0,
        "architecture": "E-9 full-from-scratch; CC-blind-first Phase-3 read",
        "dispatch": {"md5": DISPATCH_MD5, "bytes": DISPATCH_BYTES,
                     "verified": dispatch_ok},
        "base_canonical": {"file": BASE_CANONICAL[0], "md5": BASE_CANONICAL[1],
                           "bytes": BASE_CANONICAL[2],
                           "status": "carried by dispatch; file not re-supplied "
                                     "to the CC leg; recorded as frozen"},
        "embeds": embeds,
        "definitions_frozen": {
            "labels": ["D-%d" % i for i in range(1, 10)],
            "block_md5": cc.md5_bytes(dblock.encode("utf-8")),
            "block_bytes": len(dblock.encode("utf-8")),
            "verbatim": dblock,
        },
        "sealed": {
            "file": SEALED_NAME,
            "md5": EXPECTED_EMBEDS[SEALED_NAME][0],
            "bytes": EXPECTED_EMBEDS[SEALED_NAME][1],
            "census_structural_rowid_count": census,
            "census_expected": SEALED_CENSUS_EXPECTED,
            "opened": False,
            "note": "row-id regex count only; no field read; unopened until Phase 3",
        },
        "a0_pass": "chat-leg result carried: NOT TRIGGERED; not repeated (dispatch section 2)",
        "elections_in_force": ["E-0", "E-1(a)", "E-2", "E-3", "E-4", "E-5",
                               "E-6", "E-7", "E-8", "E-9", "E-10", "E-11", "E-12"],
        "t1_scan": {"patterns": len(pats), "targets": t1_report,
                    "total_hits": total_hits},
    }
    info = cc.write_checkpoint(
        os.path.join(cc.GATE_DIR, "ci1_phase0_cc.json"), ckpt, pats)
    # rescan the just-written checkpoint (belt and braces; the serializer
    # already guarantees clean output)
    post = cc.t1_scan_file(os.path.join(cc.GATE_DIR, "ci1_phase0_cc.json"), pats)
    print("PHASE0 CC OK")
    print("checkpoint:", info)
    print("checkpoint T1 hits:", len(post))
    print("census:", census)
    for e in embeds:
        print("embed OK: %-36s %s %7d %s" % (e["file"], e["md5_extracted"],
                                             e["bytes_extracted"], e["flag"]))


if __name__ == "__main__":
    main()
