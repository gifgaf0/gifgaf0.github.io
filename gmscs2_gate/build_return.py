import hashlib, sys
plain = open("G_MSCS2_CC_RETURN_plaintext.md", "rb").read()
embeds = ["g_mscs2_ccleg.py", "g_mscs2_ccleg_checkpoint.json", "g_mscs2_twoleg_comparison.json",
          "g_mscs2_chatleg_selfcompare_CCRERUN.json", "g_mscs2_ccleg_selfcompare.json", "g_mscs2_ccleg_compare.json"]
out = bytearray(plain)
for name in embeds:
    b = open(name, "rb").read()
    out += f"=====BEGIN-EMBED name={name} md5={hashlib.md5(b).hexdigest()} bytes={len(b)} encoding=raw=====\n".encode()
    out += b
    if not b.endswith(b"\n"): out += b"\n"
    out += f"=====END-EMBED name={name}=====\n\n".encode()
open("G_MSCS2_CC_RETURN_INBAND.md", "wb").write(out)
print("return", hashlib.md5(out).hexdigest(), len(out))
