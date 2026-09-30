import hashlib
plain = open("G_MSCS_A_CC_RETURN_plaintext.md", "rb").read()
embeds = ["g_mscs_a_ccleg.py", "g_mscs_a_ccleg_prereadcheckpoint.json", "g_mscs_a_ccleg_checkpoint.json"]
out = bytearray(plain)
for name in embeds:
    b = open(name, "rb").read()
    out += f"=====BEGIN-EMBED name={name} md5={hashlib.md5(b).hexdigest()} bytes={len(b)} encoding=raw=====\n".encode()
    out += b
    if not b.endswith(b"\n"): out += b"\n"
    out += f"=====END-EMBED name={name}=====\n\n".encode()
open("G_MSCS_A_CC_RETURN_INBAND.md", "wb").write(out)
print("return", hashlib.md5(out).hexdigest(), len(out))
