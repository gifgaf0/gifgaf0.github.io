"""verify_beacon_028.py -- BLS verification of the Entry 028 seed round (as verify_beacon_026.py, with the
chain hash AND public key pinned). Scheme pedersen-bls-chained: public key on G1, signature on G2,
message sha256(previous_signature || round as 8-byte big-endian).
Usage: verify_beacon_028.py INFO_JSON ROUND_JSON PREV_ROUND_JSON EXPECTED_ROUND"""
import json, sys, hashlib
from py_ecc.bls import G2Basic
CHAIN = "8990e7a9aaed2ffed73dbd7092123d6f289930540d7651336225dc172e51b2ce"
PUBLIC_KEY = "868f005eb8e6e4ca0a47c8a77ceaa5309a47978a7c71bc5cce96366b5d7a569937c529eeda66c7293784a9402801af31"
info = json.load(open(sys.argv[1])); r = json.load(open(sys.argv[2])); prev = json.load(open(sys.argv[3])); R = int(sys.argv[4])
pk = bytes.fromhex(PUBLIC_KEY); sig = bytes.fromhex(r["signature"]); ps = bytes.fromhex(r["previous_signature"])
msg = lambda rnd: hashlib.sha256(ps + rnd.to_bytes(8, "big")).digest()
out = {
 "chain_hash_is_mainnet_default": info["hash"] == CHAIN and info["period"] == 30 and info["genesis_time"] == 1595431050,
 "info_public_key_equals_pinned": info["public_key"] == PUBLIC_KEY,
 "scheme": info["schemeID"], "round": r["round"], "round_is_expected": r["round"] == R,
 "bls_valid_against_pinned_key": G2Basic.Verify(pk, msg(r["round"]), sig),
 "randomness_eq_sha256_sig": hashlib.sha256(sig).hexdigest() == r["randomness"],
 "previous_signature_eq_previous_round": prev["round"] == r["round"] - 1 and prev["signature"] == r["previous_signature"],
 "control_wrong_round_rejected": not G2Basic.Verify(pk, msg(r["round"] + 1), sig),
 "control_tampered_sig_rejected": not G2Basic.Verify(pk, msg(r["round"]), sig[:-1] + bytes([sig[-1] ^ 1])),
 "randomness": r["randomness"],
}
out["ALL_OK"] = all(v for k, v in out.items() if k not in ("scheme", "round", "randomness"))
print(json.dumps(out, indent=1))
