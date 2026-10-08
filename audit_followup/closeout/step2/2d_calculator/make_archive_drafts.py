#!/usr/bin/env python3
"""Step 2d: the public calculator, archived. Two drafts, nothing deployed.

(1) index_v3_1_archived_DRAFT.html: the Phase B v3.1 draft (phase_b/B3/site/index_v3_1_DRAFT.html, md5 b7fb8b39…) plus
    one static banner line above the app, the brief's text verbatim:
    "Archived, V4.97: a fitted mass table with named inputs; the program it belonged to is closed".
    The banner is plain HTML, so it shows even if the page's scripts fail to load. Nothing else changes, and removing the
    two hunks returns the v3.1 draft byte for byte.
(2) index_stub_DRAFT.html + archive/calculator_v3_1.html: the alternative. A one-screen index.html saying the calculator
    is archived and linking to the archived page, which is a copy of (1).
"""
import hashlib, os, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "../../../phase_b/B3/site/index_v3_1_DRAFT.html")
SRC_MD5 = "b7fb8b39652ebb0e54b659bcb910eb25"
BANNER = "Archived, V4.97: a fitted mass table with named inputs; the program it belonged to is closed."
s = open(SRC, encoding="utf-8").read()
assert hashlib.md5(s.encode()).hexdigest() == SRC_MD5
H = [("  </style>\n</head>",
      "    .archive-banner { background: #2a2410; color: #f3e3a6; border-bottom: 1px solid #5a4a1a; padding: 10px 16px;"
      " font-size: 14px; line-height: 1.4; text-align: center; }\n  </style>\n</head>"),
     ("<body>\n  <div id=\"root\"></div>",
      f"<body>\n  <div class=\"archive-banner\" role=\"note\">{BANNER}</div>\n  <div id=\"root\"></div>")]
out = s
for old, new in H:
    assert s.count(old) == 1 and out.count(old) == 1
    out = out.replace(old, new, 1)
rev = out
for old, new in reversed(H):
    rev = rev.replace(new, old, 1)
assert rev == s, "reverse splice failed"
A = os.path.join(HERE, "index_v3_1_archived_DRAFT.html")
open(A, "w", encoding="utf-8").write(out)
shutil.copyfile(A, os.path.join(HERE, "archive", "calculator_v3_1.html"))
STUB = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>SQT Geometric Mass Calculator (archived)</title>
  <style>
    html, body { background: #08080f; color: #d8d8f0; font-family: system-ui, -apple-system, sans-serif; margin: 0; }
    main { max-width: 640px; margin: 0 auto; padding: 48px 16px; line-height: 1.55; }
    h1 { font-size: 24px; margin: 0 0 16px; }
    a { color: #7fdcff; }
  </style>
</head>
<body>
  <main>
    <h1>SQT Geometric Mass Calculator: archived</h1>
    <p>This page hosted a calculator for a fitted mass table with named inputs. The research program it belonged to
       was closed in October 2026 (ledger V4.97).</p>
    <p>The last version of the calculator is kept, with that note at its top:
       <a href="archive/calculator_v3_1.html">calculator v3.1 (archived)</a>.</p>
  </main>
</body>
</html>
"""
open(os.path.join(HERE, "index_stub_DRAFT.html"), "w", encoding="utf-8").write(STUB)
for f in ("index_v3_1_archived_DRAFT.html", "archive/calculator_v3_1.html", "index_stub_DRAFT.html"):
    b = open(os.path.join(HERE, f), "rb").read()
    print(f, hashlib.md5(b).hexdigest(), len(b))
