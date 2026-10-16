#!/usr/bin/env python3
"""Mutation tests for the X-Wing low-order fix and its tests.

``tests/test_xwing_low_order.py`` pins how ``combiner/xwing.py`` handles
low-order X25519 points. This script checks that those tests have teeth: it
copies the package into a temporary directory, applies one mutation at a time
to the fix (or to the ML-KEM-1024 profile's X25519 leg), and runs the
low-order tests on the copy. Every mutant must make at least one test fail,
and the unmutated copy must pass.

Usage, from the repository root:

    python3 hybrid_kem/tests/low_order_mutants.py

Not collected by pytest (the file name does not start with ``test_``).
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile

PKG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # .../hybrid_kem
TEST = "hybrid_kem/tests/test_xwing_low_order.py"
XW = "hybrid_kem/combiner/xwing.py"
LEG = "hybrid_kem/kem_classical/x25519_kem.py"
U8B = "39382357235489614581723060781553021112529911719440698176882885853963445705823,\n"

# name -> list of (file, old, new); "none" is the control and must pass.
MUTATIONS = {
    "none": [],
    "no_fallback": [(XW,
        "    try:\n        return priv.exchange(peer)\n    except ValueError:\n"
        "        if _is_low_order(peer_pk):\n            return bytes(32)\n        raise\n",
        "    return priv.exchange(peer)\n")],
    "zeros_on_any_error": [(XW,
        "        if _is_low_order(peer_pk):\n            return bytes(32)\n        raise\n",
        "        return bytes(32)\n")],
    "drop_u8b": [(XW, "    " + U8B, "")],
    "no_top_bit_mask": [(XW,
        'value = int.from_bytes(u, "little") & ((1 << 255) - 1)',
        'value = int.from_bytes(u, "little")')],
    "no_mod_p": [(XW,
        "return value % _P25519 in _LOW_ORDER_U",
        "return value in _LOW_ORDER_U")],
    "decap_uses_raw_pyca": [(XW,
        "    ss_x = _x25519_dh(sk_x, ct_x)\n",
        "    ss_x = x25519.X25519PrivateKey.from_private_bytes(sk_x).exchange(\n"
        "        x25519.X25519PublicKey.from_public_bytes(ct_x))\n")],
    "encap_uses_raw_pyca": [(XW,
        "    ss_x = _x25519_dh(ek_x, pk_x)\n",
        "    ss_x = x25519.X25519PrivateKey.from_private_bytes(ek_x).exchange(\n"
        "        x25519.X25519PublicKey.from_public_bytes(pk_x))\n")],
    "fallback_returns_ones": [(XW,
        "            return bytes(32)\n",
        "            return b\"\\x01\" * 32\n")],
    "rfc9180_leg_also_maps_zeros": [(LEG,
        "        priv = x25519.X25519PrivateKey.from_private_bytes(sk)\n"
        "        return priv.exchange(x25519.X25519PublicKey.from_public_bytes(ct))\n",
        "        priv = x25519.X25519PrivateKey.from_private_bytes(sk)\n"
        "        try:\n"
        "            return priv.exchange(x25519.X25519PublicKey.from_public_bytes(ct))\n"
        "        except ValueError:\n"
        "            return bytes(32)\n")],
}


def run(name: str, edits: list, work: str) -> tuple[int, str]:
    tree = os.path.join(work, name)
    shutil.copytree(PKG, os.path.join(tree, "hybrid_kem"),
                    ignore=shutil.ignore_patterns("__pycache__", "analysis", "paper"))
    for path, old, new in edits:
        full = os.path.join(tree, path)
        with open(full) as f:
            src = f.read()
        if src.count(old) != 1:
            return -1, f"edit did not apply exactly once in {path}"
        with open(full, "w") as f:
            f.write(src.replace(old, new))
    r = subprocess.run([sys.executable, "-m", "pytest", TEST, "-q", "-p", "no:cacheprovider"],
                       cwd=tree, capture_output=True, text=True)
    lines = r.stdout.strip().splitlines()
    return r.returncode, (lines[-1] if lines else r.stderr.strip()[-200:])


def main() -> int:
    work = tempfile.mkdtemp(prefix="low-order-mutants-")
    ok = True
    for name, edits in MUTATIONS.items():
        code, summary = run(name, edits, work)
        good = (code == 0) if name == "none" else (code not in (0, -1))
        ok &= good
        print(f"{'OK ' if good else 'BAD'} {name:28s} {summary}")
    n = len(MUTATIONS) - 1
    print(f"\n{'all' if ok else 'NOT all'} {n} mutants caught; control "
          f"{'passes' if ok else 'checked'} (copies in {work})")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
