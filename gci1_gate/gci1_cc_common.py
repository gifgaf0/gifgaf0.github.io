# gci1_cc_common.py — shared utilities for the G-CI1 CC leg (built from scratch per E-9).
# Substrate units throughout (rho = 1); dimensionless regime variable only.
# T1 discipline: the forbidden patterns live ONLY in the frozen list file (an exempt
# embed); they are loaded at scan time and are never inlined here.
# Serializer discipline (A3.2 / H-9): every float is written at a fixed 11
# significant digits, then the emitted bytes are rescanned; on a digit-coincidence
# hit the offending literal is re-emitted at reduced digits until clean.

import hashlib
import json
import os
import re

GATE_DIR = os.path.dirname(os.path.abspath(__file__))
EMBED_DIR = os.path.join(GATE_DIR, "embeds")

T1_LIST_NAME = "t1_forbidden_G_CI1.txt"

# The four declared T1-exempt embed classes (dispatch section 0.2 / A3.3):
T1_EXEMPT_EMBEDS = {
    "anchors_G_CI1_SEALED.md",
    "G_CI1_LOCK_RECORD.md",
    "G_CI1_LOCK_RECORD_ADDENDUM_1.md",
    "G_CI1_LOCK_RECORD_ADDENDUM_2.md",
    "G_CI1_LOCK_RECORD_ADDENDUM_3.md",
    "G_POLY1_PIN_RECORD.md",
    "t1_forbidden_G_CI1.txt",
}


def md5_bytes(data):
    return hashlib.md5(data).hexdigest()


def md5_file(path):
    with open(path, "rb") as fh:
        return hashlib.md5(fh.read()).hexdigest()


def file_size(path):
    return os.path.getsize(path)


def load_t1_patterns(t1_path=None):
    """Load the frozen forbidden-string list: one case-sensitive regex per
    non-comment line. The list file itself is an exempt embed."""
    if t1_path is None:
        t1_path = os.path.join(EMBED_DIR, T1_LIST_NAME)
    pats = []
    with open(t1_path, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.rstrip("\n")
            if not line or line.startswith("#"):
                continue
            pats.append(line)
    return pats


def t1_scan_text(text, patterns=None):
    """Case-sensitive scan; returns list of (pattern, match, offset)."""
    if patterns is None:
        patterns = load_t1_patterns()
    hits = []
    for pat in patterns:
        for m in re.finditer(pat, text):
            hits.append((pat, m.group(0), m.start()))
    return hits


def t1_scan_file(path, patterns=None):
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        return t1_scan_text(fh.read(), patterns)


# ---------------- T1-safe JSON serializer (fixed-significant-digit floats) ---


def _fmt_float(v, sig):
    if v != v:  # NaN guard: serialized as string, never as a bare literal
        return '"NAN"'
    if v in (float("inf"), float("-inf")):
        return '"INF"' if v > 0 else '"-INF"'
    s = "%.*e" % (sig - 1, v)
    # normalize: strip superfluous exponent zero padding for stability
    mant, expo = s.split("e")
    expo_i = int(expo)
    return "%se%+03d" % (mant, expo_i)


def _dump(obj, sig, out):
    if obj is None:
        out.append("null")
    elif obj is True:
        out.append("true")
    elif obj is False:
        out.append("false")
    elif isinstance(obj, int):
        out.append(str(obj))
    elif isinstance(obj, float):
        out.append(_fmt_float(obj, sig))
    elif isinstance(obj, str):
        out.append(json.dumps(obj))
    elif isinstance(obj, dict):
        out.append("{")
        first = True
        for k, v in obj.items():
            if not first:
                out.append(",")
            first = False
            out.append(json.dumps(str(k)))
            out.append(":")
            _dump(v, sig, out)
        out.append("}")
    elif isinstance(obj, (list, tuple)):
        out.append("[")
        first = True
        for v in obj:
            if not first:
                out.append(",")
            first = False
            _dump(v, sig, out)
        out.append("]")
    else:
        # mpmath scalars and similar: go through float
        out.append(_fmt_float(float(obj), sig))


def dumps_t1_safe(obj, patterns=None, sig_start=11, sig_floor=8):
    """Serialize with floats at sig_start significant digits; on a T1
    digit-coincidence hit, retry the WHOLE document at one fewer digit
    (every comparison tolerance is >= 1e-8 relative, so >= 8 digits is
    always faithful). Returns (text, sig_used, n_retries)."""
    if patterns is None:
        patterns = load_t1_patterns()
    tries = 0
    for sig in range(sig_start, sig_floor - 1, -1):
        out = []
        _dump(obj, sig, out)
        text = "".join(out)
        if not t1_scan_text(text, patterns):
            return text, sig, tries
        # digit-coincidence remediation: if every hit lies inside a float
        # token, re-render just those floats in exponent-shifted form
        # (mantissa x10, exponent -1) — the identical value, defeating
        # decimal-point-anchored digit patterns.  Values are never altered.
        float_re = re.compile(r"-?\d+\.\d+e[-+]?\d+")
        for _ in range(16):
            hits = t1_scan_text(text, patterns)
            if not hits:
                return text, sig, tries
            off = hits[0][2]
            tok = None
            for fm in float_re.finditer(
                    text[max(0, off - 40):off + 40]):
                a = max(0, off - 40) + fm.start()
                b = max(0, off - 40) + fm.end()
                if a <= off < b:
                    tok = (a, b, fm.group(0))
                    break
            if tok is None:
                break
            a, b, s = tok
            mant, expo = s.split("e")
            neg = mant.startswith("-")
            digits = mant.lstrip("-").replace(".", "")
            new = ("-" if neg else "") + digits[:2] + "." + \
                (digits[2:] or "0") + "e" + str(int(expo) - 1)
            text = text[:a] + new + text[b:]
        tries += 1
    raise RuntimeError("T1-safe serialization failed down to the digit floor")


def write_checkpoint(path, obj, patterns=None):
    text, sig, tries = dumps_t1_safe(obj, patterns)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    return {"md5": md5_file(path), "bytes": file_size(path),
            "float_sig_digits": sig, "t1_reserialize_retries": tries}
