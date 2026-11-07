# Verify drand mainnet (pedersen-bls-chained) round signature with py_ecc.
# Scheme: pubkey on G1 (48 B), signature on G2 (96 B), DST BLS_SIG_BLS12381G2_XMD:SHA-256_SSWU_RO_NUL_,
# message = sha256(previous_signature || round as 8-byte big-endian).
import json, sys, hashlib
from py_ecc.bls import G2Basic
info = json.load(open(sys.argv[1])); r = json.load(open(sys.argv[2])); prev = json.load(open(sys.argv[3]))
pk = bytes.fromhex(info["public_key"]); sig = bytes.fromhex(r["signature"]); ps = bytes.fromhex(r["previous_signature"])
msg = lambda rnd, p=ps: hashlib.sha256(p + rnd.to_bytes(8, "big")).digest()
out = {
 "scheme": info["schemeID"], "chain_hash": info["hash"], "public_key": info["public_key"], "round": r["round"],
 "bls_valid": G2Basic.Verify(pk, msg(r["round"]), sig),
 "randomness_eq_sha256_sig": hashlib.sha256(sig).hexdigest() == r["randomness"],
 "previous_signature_eq_round_6611335_signature": prev["signature"] == r["previous_signature"] and prev["round"] == r["round"] - 1,
 "control_wrong_round_rejected": not G2Basic.Verify(pk, msg(r["round"] + 1), sig),
 "control_tampered_sig_rejected": not G2Basic.Verify(pk, msg(r["round"]), sig[:-1] + bytes([sig[-1] ^ 1])) if True else None,
 "py_ecc": __import__("importlib.metadata").metadata.version("py_ecc"),
}
print(json.dumps(out, indent=1))
