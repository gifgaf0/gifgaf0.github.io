"""test_refusals_028.py -- every startup refusal path of analyze_028.py on synthetic data.
A locally generated BLS key stands in for drand (its chain hash is patched into the module for the test
only; case 'mainnet constants' shows the unpatched module refuses it). Data: 2,000 synthetic strata with
correct pair counts. No real primes and no live beacon are used."""
import os, sys, json, shutil, hashlib, subprocess, random, tempfile
import numpy as np
from py_ecc.bls import G2Basic
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from read_028 import REC, MAGIC
from analyze_028 import beacon_round, GENESIS, PERIOD
P026 = "/home/claude/gifgaf0.github.io/entry026/provenance"
TESTHASH = "00" * 32; PUSH = "2026-11-24T00:00:00Z"; NPER = 12_500_000
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
def build_base(root):
    os.makedirs(root)
    for f in ("analyze_028.py", "read_028.py", "pred_028.json", "predict_026.py"): shutil.copy(os.path.join(HERE, f), root)
    open(os.path.join(root, "entry_028.md"), "w").write("stand-in entry for the refusal tests\n")
    files = ["entry_028.md", "analyze_028.py", "read_028.py", "pred_028.json", "predict_026.py"]
    m = {"entry": "028", "sha256": {f: sha(os.path.join(root, f)) for f in files}}
    json.dump(m, open(os.path.join(root, "manifest28.json"), "w"), indent=1)
    sk = G2Basic.KeyGen(b"entry028-refusal-test-key-0000000"); pk = G2Basic.SkToPk(sk)
    R = beacon_round(PUSH); prev_sig = G2Basic.Sign(sk, b"prev"); msg = hashlib.sha256(prev_sig + R.to_bytes(8, "big")).digest()
    sig = G2Basic.Sign(sk, msg); rnd = hashlib.sha256(sig).hexdigest()
    json.dump({"hash": TESTHASH, "genesis_time": GENESIS, "period": PERIOD, "public_key": pk.hex(), "schemeID": "pedersen-bls-chained"},
              open(os.path.join(root, "info.json"), "w"))
    json.dump({"round": R, "signature": sig.hex(), "previous_signature": prev_sig.hex(), "randomness": rnd}, open(os.path.join(root, "round.json"), "w"))
    json.dump({"round": R - 1, "signature": prev_sig.hex()}, open(os.path.join(root, "prev.json"), "w"))
    d = os.path.join(root, "data"); os.makedirs(d); rng = np.random.default_rng(5)
    for c0 in range(0, 2000, 50):
        recs = np.zeros(50, REC)
        for i, r in enumerate(range(c0, c0 + 50)):
            recs[i]["magic"] = MAGIC; recs[i]["r"] = r; recs[i]["nkept"] = NPER + 1
            recs[i]["lag1"] = rng.multinomial(NPER, np.full(256, 1 / 256)); recs[i]["lag2"] = rng.multinomial(NPER - 1, np.full(256, 1 / 256))
        recs.tofile(os.path.join(d, f"chunk_{c0:04d}.bin"))
        json.dump({"seed": rnd, "strata": list(range(c0, c0 + 50))}, open(os.path.join(d, f"chunk_{c0:04d}.json"), "w"))
    return sha(os.path.join(root, "manifest28.json")), R
def run(root, msha, push=PUSH, patch=True):
    pk = json.load(open(root + "/info.json"))["public_key"]
    code = (f"import sys; sys.path.insert(0, {root!r}); import analyze_028 as A\n"
            + (f"A.CHAIN_HASH = {TESTHASH!r}; A.PUBLIC_KEY = {pk!r}\n" if patch else "")
            + f"A.main(['analyze_028.py', {root + '/manifest28.json'!r}, {msha!r}, {root + '/info.json'!r}, "
              f"{root + '/round.json'!r}, {root + '/prev.json'!r}, {push!r}, {root + '/data'!r}])")
    p = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True)
    out = (p.stdout + p.stderr).strip().splitlines()
    ref = [l for l in out if l.startswith("REFUSED")]
    return (ref[0] if ref else ("RAN: " + (out[-1] if out else ""))), p.returncode
def bump_pair_count(T):
    a = np.fromfile(T + "/data/chunk_0000.bin", REC); a["lag1"][7, 0] += 1; a.tofile(T + "/data/chunk_0000.bin")
def edit_json(fn, f):
    j = json.load(open(fn)); f(j); json.dump(j, open(fn, "w"))
CASES = [
 ("consistent", lambda T: None, {}),
 ("wrong manifest sha256", lambda T: None, {"msha": "0" * 64}),
 ("edited entry", lambda T: open(T + "/entry_028.md", "a").write("x"), {}),
 ("edited analysis", lambda T: open(T + "/analyze_028.py", "a").write("\n# edit\n"), {}),
 ("edited archived script", lambda T: open(T + "/predict_026.py", "a").write("\n"), {}),
 ("mainnet constants (unpatched) on test chain", lambda T: None, {"patch": False}),
 ("wrong round for push time", lambda T: None, {"push": "2026-11-24T00:10:00Z"}),
 ("tampered signature", lambda T: edit_json(T + "/round.json", lambda j: j.update(signature=j["signature"][:-2] + ("00" if j["signature"][-2:] != "00" else "01"))), {}),
 ("tampered randomness", lambda T: edit_json(T + "/round.json", lambda j: j.update(randomness="ab" * 32)), {}),
 ("broken chain link", lambda T: edit_json(T + "/prev.json", lambda j: j.update(signature="cd" * 96)), {}),
 ("chunk seed mismatch", lambda T: edit_json(T + "/data/chunk_0100.json", lambda j: j.update(seed="dry-1")), {}),
 ("missing stratum chunk", lambda T: [os.remove(T + "/data/chunk_1950" + e) for e in (".bin", ".json")], {}),
 ("duplicate strata", lambda T: [shutil.copy(T + "/data/chunk_0000" + e, T + "/data/chunk_9999" + e) for e in (".bin", ".json")], {}),
 ("wrong pair count", bump_pair_count, {}),
 ("real drand round 6635716 (Entry 026), unpatched", lambda T: [shutil.copy(f"{P026}/drand_info.json", T + "/info.json"),
     shutil.copy(f"{P026}/drand_round_6635716.json", T + "/round.json"), shutil.copy(f"{P026}/drand_round_6635715.json", T + "/prev.json")],
  {"patch": False, "push": "2026-11-12T16:44:58Z", "expect": "REFUSED: data chunks not all generated with the beacon seed"}),
 ("wrong public key in /info, unpatched", lambda T: [shutil.copy(f"{P026}/drand_info.json", T + "/info.json"),
     shutil.copy(f"{P026}/drand_round_6635716.json", T + "/round.json"), shutil.copy(f"{P026}/drand_round_6635715.json", T + "/prev.json"),
     edit_json(T + "/info.json", lambda j: j.update(public_key="a" + j["public_key"][1:]))],
  {"patch": False, "push": "2026-11-12T16:44:58Z"}),
]
if __name__ == "__main__":
    work = tempfile.mkdtemp(); base = os.path.join(work, "base"); msha, R = build_base(base)
    print(f"stand-in round {R} for push {PUSH}; manifest sha {msha[:16]}...  (consistent case is expected to RUN; its\n"
          f"  synthetic tables are uniform, so its test verdicts are meaningless and only show the checks let it through)")
    allok = True
    for name, mutate, kw in CASES:
        T = os.path.join(work, name.replace(" ", "_")); shutil.copytree(base, T); mutate(T)
        res, rc = run(T, kw.get("msha", msha), kw.get("push", PUSH), kw.get("patch", True))
        expect_ok = name == "consistent"
        ok = (rc == 0 and res.startswith("RAN")) if expect_ok else res.startswith(kw.get("expect", "REFUSED"))
        allok &= ok
        print(f"  {'ok  ' if ok else 'BAD '} {name:45s} -> {res}")
    print("ALL REFUSAL PATHS BEHAVE AS DESIGNED" if allok else "SOME CASES MISBEHAVED"); sys.exit(0 if allok else 1)
