#!/usr/bin/env python3
"""
Alpha-decay Q-value analysis from AME2020 mass excesses.
Even-even actinides, isotone step analysis.
Data: Wang et al., Chinese Physics C45, 030003 (2021)
"""
import statistics
from collections import defaultdict

# Delta(4He) mass excess
ME_He4 = 2424.91587  # keV

# AME2020 mass excesses in keV: (Z, A) -> ME
# Extracted from the full AME2020 mass table
# Only experimental values (no # estimates) unless noted
ME = {
    # ---- Z=80 (Hg) - daughters for Pb alpha decay ----
    (80,196): -31825.944,
    (80,198): -30954.315,
    (80,200): -29503.267,
    (80,202): -27345.310,
    (80,204): -24690.148,
    (80,206): -20945.728,
    (80,208): -13265.408,  # large unc

    # ---- Z=82 (Pb) ----
    (82,196): -25348.234,
    (82,198): -26067.443,
    (82,200): -26250.858,
    (82,202): -25940.608,
    (82,204): -25109.815,
    (82,206): -23785.506,
    (82,208): -21748.519,
    (82,210): -14728.429,
    (82,212):  -7548.929,
    (82,214):   -183.019,

    # ---- Z=84 (Po) ----
    (84,196): -13468.731,
    (84,198): -15473.278,
    (84,200): -16941.683,
    (84,202): -17941.569,
    (84,204): -18341.045,
    (84,206): -18188.668,
    (84,208): -17469.207,
    (84,210): -15953.060,
    (84,212): -10369.408,
    (84,214):  -4469.972,
    (84,216):   1782.336,
    (84,218):   8356.652,

    # ---- Z=86 (Rn) ----
    (86,196):   1975.169,
    (86,198):  -1230.320,
    (86,200):  -4000.454,
    (86,202):  -6274.561,
    (86,204):  -7970.115,
    (86,206):  -9132.918,
    (86,208):  -9655.389,
    (86,210):  -9604.764,
    (86,212):  -8659.219,
    (86,214):  -4319.664,
    (86,216):    253.312,
    (86,218):   5217.413,
    (86,220):  10611.994,
    (86,222):  16371.957,

    # ---- Z=88 (Ra) ----
    (88,202):   9074.900,
    (88,204):   6061.097,
    (88,206):   3565.613,
    (88,208):   1727.934,
    (88,210):    442.839,
    (88,212):   -198.763,
    (88,214):     92.740,
    (88,216):   3291.466,
    (88,218):   6645.556,
    (88,220):  10272.091,
    (88,222):  14320.205,
    (88,224):  18825.832,
    (88,226):  23667.576,
    (88,228):  28940.194,
    (88,230):  34516.306,
    (88,232):  40496.955,
    (88,234):  46930.629,

    # ---- Z=90 (Th) ----
    (90,208):  16688.041,
    (90,210):  14059.521,
    (90,212):  12110.886,
    (90,214):  10694.932,
    (90,216):  10298.537,
    (90,218):  12366.747,
    (90,220):  14689.538,
    (90,222):  17203.039,
    (90,224):  19995.581,
    (90,226):  23197.649,
    (90,228):  26770.899,
    (90,230):  30862.512,
    (90,232):  35446.710,
    (90,234):  40612.958,
    (90,236):  46255.203,

    # ---- Z=92 (U) ----
    (92,216):  23066.429,
    (92,218):  21894.655,
    (92,222):  24272.834,
    (92,224):  25742.690,
    (92,226):  27328.797,
    (92,228):  29220.001,
    (92,230):  31615.017,
    (92,232):  34609.445,
    (92,234):  38144.959,
    (92,236):  42444.582,
    (92,238):  47307.732,
    (92,240):  52715.497,

    # ---- Z=94 (Pu) ----
    (94,228):  36107.809,
    (94,232):  38360.915,
    (94,234):  40349.986,
    (94,236):  42901.508,
    (94,238):  46163.148,
    (94,240):  50125.319,
    (94,242):  54716.876,
    (94,244):  59806.021,
    (94,246):  65394.772,

    # ---- Z=96 (Cm) ----
    (96,234):  46722.411,
    (96,236):  47852.820,
    (96,238):  49445.203,
    (96,240):  51724.222,
    (96,242):  54803.699,
    (96,244):  58451.835,
    (96,246):  62616.912,
    (96,248):  67392.748,
    (96,250):  72989.588,

    # ---- Z=98 (Cf) ----
    (98,240):  57988.719,
    (98,242):  59386.982,
    (98,244):  61478.096,
    (98,246):  64090.228,
    (98,248):  67237.951,
    (98,250):  71170.336,
    (98,252):  76034.610,
    (98,254):  81341.395,

    # ---- Z=100 (Fm) ----
    (100,246):  70191.187,
    (100,248):  71897.793,
    (100,250):  74072.193,
    (100,252):  76816.611,
    (100,254):  80902.521,
    (100,256):  85484.796,

    # ---- Z=102 (No) ----
    (102,250):  82871.370,
    (102,252):  82871.370,  # check this value
    (102,254):  84723.312,
    (102,256):  87823.046,
}

# Element names
ELEM = {80:"Hg",82:"Pb",84:"Po",86:"Rn",88:"Ra",90:"Th",
        92:"U",94:"Pu",96:"Cm",98:"Cf",100:"Fm",102:"No"}

# ================================================================
# Compute Q-values
# ================================================================
print("="*90)
print("ALPHA-DECAY Q-VALUES FOR EVEN-EVEN NUCLEI (AME2020)")
print("="*90)
print(f"{'Parent':>12} {'Z':>3} {'A':>4} {'N':>4} {'U':>3}  {'Daughter':>12}  {'Q_alpha (MeV)':>13}")
print("-"*90)

qvalues = {}  # (Z, N) -> Q in MeV

for Z in range(84, 104, 2):
    for A in sorted([a for (z,a) in ME if z == Z]):
        N = A - Z
        if N % 2 != 0:
            continue
        daughter = (Z-2, A-4)
        if daughter not in ME:
            continue
        
        Q_keV = ME[(Z,A)] - ME[daughter] - ME_He4
        Q_MeV = Q_keV / 1000.0
        U = Z - 80
        el_p = ELEM.get(Z, "?")
        el_d = ELEM.get(Z-2, "?")
        
        print(f"  {el_p}-{A:<3d}     {Z:3d} {A:4d} {N:4d} {U:3d}  {el_d}-{A-4:<3d}       {Q_MeV:13.4f}")
        
        if Q_MeV > 0:  # only physical alpha decays
            qvalues[(Z, N)] = Q_MeV

print(f"\nTotal Q-values computed: {len(qvalues)}")

# ================================================================
# Isotone step analysis
# ================================================================
print("\n" + "="*90)
print("ISOTONE STEPS: DeltaQ = Q(Z+2, N) - Q(Z, N)")
print("="*90)

by_N = defaultdict(dict)
for (Z, N), Q in qvalues.items():
    by_N[N][Z] = Q

boundaries = defaultdict(list)

for N in sorted(by_N.keys()):
    zvals = sorted(by_N[N].keys())
    if len(zvals) < 2:
        continue
    for i in range(len(zvals)-1):
        Z1, Z2 = zvals[i], zvals[i+1]
        if Z2 - Z1 != 2:
            continue
        U1, U2 = Z1-80, Z2-80
        dQ = by_N[N][Z2] - by_N[N][Z1]
        bnd = (U1, U2)
        boundaries[bnd].append((N, dQ))
        print(f"  N={N:3d}: {ELEM.get(Z1,'?')}->{ELEM.get(Z2,'?')} "
              f"(U={U1:2d}->{U2:2d})  DeltaQ = {dQ:+.4f} MeV")

# ================================================================
# Summary by boundary
# ================================================================
print("\n" + "="*90)
print("MEAN ISOTONE STEPS BY BOUNDARY")
print("="*90)
print(f"{'Boundary':>10} {'n':>3} {'<DQ> MeV':>10} {'sigma':>8} {'min':>8} {'max':>8}  {'Regime'}")
print("-"*75)

all_steps = []
regime_data = {1: [], 2: [], 3: []}

for bnd in sorted(boundaries.keys()):
    U1, U2 = bnd
    vals = [v[1] for v in boundaries[bnd]]
    n = len(vals)
    mean = statistics.mean(vals)
    stdev = statistics.stdev(vals) if n > 1 else 0
    all_steps.extend(vals)
    
    # Assign regime
    if U2 <= 8:
        regime = "I"
        regime_data[1].extend(vals)
    elif U2 <= 12:
        regime = "II"
        regime_data[2].extend(vals)
    else:
        regime = "III"
        regime_data[3].extend(vals)
    
    flag = " ***" if bnd == (12,14) else ""
    print(f"  {U1:2d} -> {U2:2d} {n:3d} {mean:10.4f} {stdev:8.4f} {min(vals):8.4f} {max(vals):8.4f}  {regime}{flag}")

print("-"*75)
if all_steps:
    print(f"  {'Overall':>7} {len(all_steps):3d} {statistics.mean(all_steps):10.4f} {statistics.stdev(all_steps):8.4f}")

# ================================================================
# Regime summary
# ================================================================
print("\n" + "="*90)
print("REGIME SUMMARY")
print("="*90)

for r in [1,2,3]:
    if regime_data[r]:
        m = statistics.mean(regime_data[r])
        s = statistics.stdev(regime_data[r]) if len(regime_data[r]) > 1 else 0
        n = len(regime_data[r])
        print(f"  Regime {['I','II','III'][r-1]:>3s}: <DQ> = {m:.4f} +/- {s:.4f} MeV  (n={n})")

if regime_data[1] and regime_data[2]:
    r12 = statistics.mean(regime_data[2]) / statistics.mean(regime_data[1])
    print(f"\n  Ratio II/I  = {r12:.2f}")
if regime_data[2] and regime_data[3]:
    r23 = statistics.mean(regime_data[3]) / statistics.mean(regime_data[2])
    print(f"  Ratio III/II = {r23:.2f}")

# ================================================================
# Comparison with 4*m0
# ================================================================
print("\n" + "="*90)
print("COMPARISON WITH 4*m0")
print("="*90)
m0 = 0.187  # MeV, from SQT ropelength paper
four_m0 = 4 * m0
mean_all = statistics.mean(all_steps) if all_steps else 0
print(f"  m0 = m_e / exp(2pi/Phi) = {m0:.3f} MeV")
print(f"  4*m0 = {four_m0:.3f} MeV")
print(f"  <DQ>_all = {mean_all:.4f} MeV")
print(f"  Deviation = {abs(mean_all - four_m0)/four_m0*100:.2f}%")

# ================================================================
# Verification against known Q-values
# ================================================================
print("\n" + "="*90)
print("VERIFICATION: Known Q-values")
print("="*90)
known = {
    "Po-210": ((84,210), 5407.5),
    "Rn-222": ((86,222), 5590.3),
    "Ra-226": ((88,226), 4870.6),
    "Th-232": ((90,232), 4081.8),
    "U-238":  ((92,238), 4269.7),
    "Pu-240": ((94,240), 5255.8),
    "Cm-244": ((96,244), 5901.6),
}

for name, (key, q_known) in known.items():
    Z, A = key
    daughter = (Z-2, A-4)
    if key in ME and daughter in ME:
        q_calc = (ME[key] - ME[daughter] - ME_He4) / 1000.0
        diff = abs(q_calc - q_known/1000.0) * 1000  # keV
        print(f"  {name:>8s}: calc={q_calc*1000:.1f} keV  known={q_known:.1f} keV  diff={diff:.1f} keV")
    else:
        print(f"  {name:>8s}: missing data")


# ================================================================
# REFINED ANALYSIS: Separate shell-closure region from deformed region
# ================================================================
print("\n\n" + "="*90)
print("REFINED ANALYSIS: N > 128 (DEFORMED ACTINIDE REGION)")
print("="*90)
print("(Excluding N=126 magic number and N=128 transition)")

boundaries_deformed = defaultdict(list)
for N in sorted(by_N.keys()):
    if N <= 128:
        continue
    zvals = sorted(by_N[N].keys())
    if len(zvals) < 2:
        continue
    for i in range(len(zvals)-1):
        Z1, Z2 = zvals[i], zvals[i+1]
        if Z2 - Z1 != 2:
            continue
        U1, U2 = Z1-80, Z2-80
        dQ = by_N[N][Z2] - by_N[N][Z1]
        bnd = (U1, U2)
        boundaries_deformed[bnd].append((N, dQ))

print(f"\n{'Boundary':>10} {'n':>3} {'<DQ> MeV':>10} {'sigma':>8} {'min':>8} {'max':>8}")
print("-"*60)

regime_def = {1: [], 2: [], 3: []}
all_def = []
for bnd in sorted(boundaries_deformed.keys()):
    U1, U2 = bnd
    vals = [v[1] for v in boundaries_deformed[bnd]]
    n = len(vals)
    mean = statistics.mean(vals)
    stdev = statistics.stdev(vals) if n > 1 else 0
    all_def.extend(vals)
    
    if U2 <= 8:
        regime_def[1].extend(vals)
        r = "I"
    elif U2 <= 12:
        regime_def[2].extend(vals)
        r = "II"
    else:
        regime_def[3].extend(vals)
        r = "III"
    
    flag = " ***" if bnd == (12,14) else ""
    print(f"  {U1:2d} -> {U2:2d} {n:3d} {mean:10.4f} {stdev:8.4f} {min(vals):8.4f} {max(vals):8.4f}  {r}{flag}")

print("-"*60)
print(f"  {'Overall':>7} {len(all_def):3d} {statistics.mean(all_def):10.4f} {statistics.stdev(all_def):8.4f}")

print("\nRegime means (N>128 only):")
for r in [1,2,3]:
    if regime_def[r]:
        m = statistics.mean(regime_def[r])
        s = statistics.stdev(regime_def[r]) if len(regime_def[r]) > 1 else 0
        n = len(regime_def[r])
        print(f"  Regime {['I','II','III'][r-1]:>3s}: <DQ> = {m:.4f} +/- {s:.4f} MeV  (n={n})")

if regime_def[1] and regime_def[2]:
    print(f"\n  Ratio II/I  = {statistics.mean(regime_def[2])/statistics.mean(regime_def[1]):.2f}")
if regime_def[2] and regime_def[3]:
    print(f"  Ratio III/II = {statistics.mean(regime_def[3])/statistics.mean(regime_def[2]):.2f}")

print(f"\n  <DQ>_all (N>128) = {statistics.mean(all_def):.4f} MeV")
print(f"  4*m0 = {four_m0:.3f} MeV")
print(f"  Deviation = {abs(statistics.mean(all_def) - four_m0)/four_m0*100:.2f}%")

# ================================================================
# Even more focused: N >= 134 (well into deformed region)
# ================================================================
print("\n\n" + "="*90)
print("FOCUSED ANALYSIS: N >= 134 (DEEP DEFORMED REGION)")
print("="*90)

boundaries_deep = defaultdict(list)
for N in sorted(by_N.keys()):
    if N < 134:
        continue
    zvals = sorted(by_N[N].keys())
    if len(zvals) < 2:
        continue
    for i in range(len(zvals)-1):
        Z1, Z2 = zvals[i], zvals[i+1]
        if Z2 - Z1 != 2:
            continue
        U1, U2 = Z1-80, Z2-80
        dQ = by_N[N][Z2] - by_N[N][Z1]
        bnd = (U1, U2)
        boundaries_deep[bnd].append((N, dQ))

print(f"\n{'Boundary':>10} {'n':>3} {'<DQ> MeV':>10} {'sigma':>8}")
print("-"*45)

regime_deep = {1: [], 2: [], 3: []}
all_deep = []
for bnd in sorted(boundaries_deep.keys()):
    U1, U2 = bnd
    vals = [v[1] for v in boundaries_deep[bnd]]
    n = len(vals)
    mean = statistics.mean(vals)
    stdev = statistics.stdev(vals) if n > 1 else 0
    all_deep.extend(vals)
    
    if U2 <= 8:
        regime_deep[1].extend(vals)
        r = "I"
    elif U2 <= 12:
        regime_deep[2].extend(vals)
        r = "II"
    else:
        regime_deep[3].extend(vals)
        r = "III"
    
    flag = " ***" if bnd == (12,14) else ""
    print(f"  {U1:2d} -> {U2:2d} {n:3d} {mean:10.4f} {stdev:8.4f}  {r}{flag}")

print("-"*45)
if all_deep:
    print(f"  {'Overall':>7} {len(all_deep):3d} {statistics.mean(all_deep):10.4f} {statistics.stdev(all_deep):8.4f}")

print("\nRegime means (N>=134 only):")
for r in [1,2,3]:
    if regime_deep[r]:
        m = statistics.mean(regime_deep[r])
        s = statistics.stdev(regime_deep[r]) if len(regime_deep[r]) > 1 else 0
        n = len(regime_deep[r])
        print(f"  Regime {['I','II','III'][r-1]:>3s}: <DQ> = {m:.4f} +/- {s:.4f} MeV  (n={n})")

if regime_deep[1] and regime_deep[2]:
    print(f"\n  Ratio II/I  = {statistics.mean(regime_deep[2])/statistics.mean(regime_deep[1]):.2f}")
if regime_deep[2] and regime_deep[3]:
    print(f"  Ratio III/II = {statistics.mean(regime_deep[3])/statistics.mean(regime_deep[2]):.2f}")

if all_deep:
    print(f"\n  <DQ>_all (N>=134) = {statistics.mean(all_deep):.4f} MeV")
    print(f"  4*m0 = {four_m0:.3f} MeV")
    print(f"  Deviation = {abs(statistics.mean(all_deep) - four_m0)/four_m0*100:.2f}%")

# ================================================================
# The N=126 shell effect
# ================================================================
print("\n\n" + "="*90)
print("SHELL CLOSURE EFFECT: N=126 vs N=130 comparison")
print("="*90)
for N_test in [126, 128, 130, 132, 134, 136, 138, 140, 142, 144, 146, 148, 150, 152, 154]:
    if N_test not in by_N:
        continue
    zvals = sorted(by_N[N_test].keys())
    steps_at_N = []
    for i in range(len(zvals)-1):
        if zvals[i+1] - zvals[i] == 2:
            dQ = by_N[N_test][zvals[i+1]] - by_N[N_test][zvals[i]]
            steps_at_N.append(dQ)
    if steps_at_N:
        print(f"  N={N_test:3d}: mean step = {statistics.mean(steps_at_N):.4f} MeV  "
              f"(n={len(steps_at_N)}, Z range {min(zvals)}-{max(zvals)})")

