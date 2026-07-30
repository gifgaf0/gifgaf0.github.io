"""
G-TSH4 T1 self-grep gate (pre-reg sec.D).

Every computation file must assert the absence of forbidden physical-constant /
observable-target strings before execution: no physical-c, GW, or phi-target
string may appear.  The functional is purely dimensionless (one control
parameter Lambda); nothing here may reference a measured quantity.
"""
import os, re

# forbidden tokens (case-insensitive word-ish matches). Kept deliberately broad.
FORBIDDEN = [
    r"299792458", r"physical[_\- ]?c\b", r"speed[_\- ]?of[_\- ]?light",
    r"\bGW\b", r"gravitational", r"phi[_\- ]?target", r"golden",
    r"6\.25", r"6\.2500", r"137\.0", r"fine[_\- ]?structure",
    r"\bhbar\s*=\s*[0-9]", r"planck",
]
_pat = re.compile("|".join(FORBIDDEN), re.IGNORECASE)

# tokens that legitimately appear (this file names the forbidden set); skip self.
_SELF = os.path.basename(__file__)

def scan_text(text):
    hits = []
    for i, line in enumerate(text.splitlines(), 1):
        m = _pat.search(line)
        if m:
            hits.append((i, m.group(0), line.strip()[:80]))
    return hits

def assert_clean(files):
    for f in files:
        if os.path.basename(f) == _SELF:
            continue
        with open(f, "r") as fh:
            hits = scan_text(fh.read())
        if hits:
            raise AssertionError("T1 self-grep FAILED in %s: %s" % (f, hits[:3]))
    return True

if __name__ == "__main__":
    import glob
    files = [f for f in glob.glob("tsh4_*.py") if os.path.basename(f) != _SELF]
    assert_clean(files)
    print("T1 self-grep PASSED on:", sorted(os.path.basename(f) for f in files))
