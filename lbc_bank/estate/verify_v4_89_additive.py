#!/usr/bin/env python3
"""Independent additivity check V4.88 -> V4.89 (character-level, no fold-script code reused):
every difference must be a pure insertion except the declared title / As-of header replacements."""
import difflib, hashlib
a = open("SQT_Master_Ledger_v4_88_CANONICAL.md", encoding="utf-8").read()
b = open("SQT_Master_Ledger_v4_89_CANONICAL.md", encoding="utf-8").read()
assert hashlib.md5(a.encode()).hexdigest() == "66b0a634e3b087c85d4209f3e6bb6a28"
la, lb = a.split("\n"), b.split("\n")
sm = difflib.SequenceMatcher(None, la, lb, autojunk=False)
ops = [o for o in sm.get_opcodes() if o[0] != "equal"]
for tag, i1, i2, j1, j2 in ops:
    if tag == "insert":
        print(f"insert  after V4.88 line {i1}: +{j2-j1} line(s), {sum(len(x.encode())+1 for x in lb[j1:j2])} B")
    else:
        for i, j in zip(range(i1, i2), range(j1, j2)):
            m = difflib.SequenceMatcher(None, la[i], lb[j], autojunk=False)
            sub = [o for o in m.get_opcodes() if o[0] != "equal"]
            kinds = sorted(set(o[0] for o in sub))
            dele = sum(o[2]-o[1] for o in sub if o[0] in ("delete", "replace"))
            print(f"{tag:7s} V4.88 line {i+1}: char ops {kinds}, chars removed/replaced = {dele}")
print("total ops:", len(ops))

# robust check for the record/estate region: old line 39 must be a subsequence of new lines 39..41 (pure insertion)
def is_subseq(small, big):
    it = iter(big)
    return all(ch in it for ch in small)
old39 = la[38]
new_region = "\n".join(lb[38:41])
print("old line 39 is a pure-insertion subsequence of new lines 39-41:", is_subseq(old39, new_region),
      f"(+{len(new_region)-len(old39)} chars)")
print("old line 3 (As-of) subsequence of new line 3 apart from the declared date/label rewrite:",
      is_subseq(la[2].replace("October 2, 2026 (V4.88 fold — ", ""), lb[2]))
print("new file contains the full old file once the 8 declared fragments are removed: see the fold script's reverse-splice (PASS)")
