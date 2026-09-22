# G-2a-A1 — CC instrument determinism witness (chat-side re-execution, September 21, 2026)

CC's instrument `g_2a_a1_ccleg.py` (md5 006cb5213208e41cc57cfe045b7d3dd4) was re-executed chat-side in a scratch
directory holding only the four guarded files (memo v2 626aa868, gate T1 list 2026b782, scanner 6b862900, extract
940b0bee). All md5 guards held; T1 self-scan CLEAN; runtime 2.57 s.

Result: the regenerated checkpoint (md5 9cc072119869986ec0175bacc18f9113) equals CC's returned checkpoint
(bbf94221122136f00c5ecad0b90e5313) in all 185 leaf values except `extras.elapsed_seconds` (3.88 -> 2.57).
Timing-stripped canonical JSON md5: 42a65c26ae895022b1a349b520437b0a on both. DETERMINISM: PASS.

The frozen comparator v1.0 (5afcd589) on chat 8f657a23 vs the re-executed checkpoint: 436 checks, 430 PASS, 6 MISS,
the same six rows as the run of record (g_2a_a1_twoleg_comparison_vs_REEXEC.json).
