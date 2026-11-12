# Entry 026 run log (append-only)

- 2026-11-12: Revision 2 approved by Matthew Gifford ("Approve and I give permission to push"). The approval is recorded in the Status line of entry_026.md before hashing.
- 2026-11-12T16:44:45Z: manifest26.json written (34 files). sha256 0b94a92ded203c65375a6f136bc901f28373955da4cde918ede7d9c88dc309fa. All 34 hashes re-verified against the files before commit.
- 2026-11-12T16:44:58Z: freeze commit 2fa61a2ee7b637f9f6bf5b8e5cdc121fe0da74cd pushed to gifgaf0/gifgaf0.github.io, branch entry026-freeze (parent 3153aa8 = origin/main). Push time 16:44:58Z on the pusher's clock, taken right after the push returned.
  - GitHub's own record (repository Activity API, saved as provenance/freeze_push_activity.json): activity_type branch_creation, ref refs/heads/entry026-freeze, before 0000000, after 2fa61a2e..., timestamp 2026-11-12T16:44:58Z. Agrees with the pusher's clock.
- Beacon, named before publication: drand mainnet default chain (League of Entropy), chain hash 8990e7a9aaed2ffed73dbd7092123d6f289930540d7651336225dc172e51b2ce, genesis 1595431050, period 30 s; round r is published at genesis + (r - 1)*30.
  - Push + 10 min = 2026-11-12T16:54:58Z. Round 6635715 is published 16:54:30Z (too early); round 6635716 is published 2026-11-12T16:55:00Z. So **R = 6635716** (beacon_round_026.py). The rule picks the same round for any push time in (16:44:30Z, 16:45:00Z].
  - SEED will be the randomness of round 6635716. It is not known to anyone at the time of this entry.
- No data in the decisive ranges exist at this commit. Generation starts only after round 6635716 has been fetched and verified (verify_beacon_026.py).
- 2026-11-12T16:58:16Z: fetched from api.drand.sh (Matthew's Chrome): /info, round 6635716 and round 6635715, saved in provenance/. /info confirms the default chain (hash 8990e7a9...b2ce, genesis 1595431050, period 30 s, pedersen-bls-chained).
  - verify_beacon_026.py (provenance/drand_bls_verify_output.json): ALL_OK. BLS signature of round 6635716 valid; randomness = sha256(signature); previous_signature = round 6635715's signature; wrong-round and tampered-signature controls rejected.
  - **SEED = 18e802197c723ed7063b4bc3d19f7a654370f965174cf106eace585ec646f000** (round 6635716, published 2026-11-12T16:55:00Z).
  - signature a642645c74692553f8dac112ec79004f2a7a5fd503b6a3fdd8416bac754a236e8b0d70499fc2eb7009c3dbbc8d71317713eb0d2ead0ee4ac559bf155a9e7ebd6c856dbffed5a2df8aedaad45aba28abdba094f5016ede1e4eea5c41c41b5b63c
- 2026-11-12T16:58:16Z: manifest re-verified (34/34); generation commands, logged before running (data in /home/claude/run026, outside the repo; gen_E_026 compiled from the frozen gen_E_026.c):
    gen_E_026 1000000000000 1020000000000 100000000 E.bin ; python3 check_E_026.py 1e12 1.02e12 1e8 E_check.npz
    python3 gen_R_026.py 64  SEED R64  0 10000
    python3 gen_R_026.py 128 SEED R128 0 10000   &   python3 gen_R_026.py 128 SEED R128 10000 20000
