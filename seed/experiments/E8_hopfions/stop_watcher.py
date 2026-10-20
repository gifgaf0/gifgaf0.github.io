"""
stop_watcher.py -- compute-budget rule for the dx = 0.1 (N = 151) stages of the Q >= 4 runs.
A stage is ended (via the STOP file read by relax.py) once it has run for at least 20 flow-time
units and the relative energy change over the last 10 units is below 1e-6 (the preregistered
plan only needs energies to ~0.1%; the original rule was 1e-7 over 20 units).
Usage: python3 stop_watcher.py &   (polls every 30 s; writes runs/stop_watcher.log)
"""
import json
import os
import time

HERE = os.path.dirname(os.path.abspath(__file__))
RUNS = ['Q4_A22', 'Q6_L22', 'Q7_K32', 'Q5_K32']
N = 151
TMIN, TOL = 20.0, 1e-6


def check(run):
    p = os.path.join(HERE, 'runs', f'{run}.log')
    if not os.path.exists(p):
        return None
    lines = open(p).read().splitlines()
    start = None
    for i, l in enumerate(lines):
        if l.startswith(f'# stage N={N} '):
            start = i
    if start is None or any(l.startswith(f'# stage N={N} finished') for l in lines[start:]):
        return None
    recs = [json.loads(l) for l in lines[start:] if l.startswith('{')]
    if len(recs) < 2:
        return None
    a, b = recs[-2], recs[-1]
    rel = abs(a['E'] - b['E']) / b['E']
    if b['t'] >= TMIN and b['t'] - a['t'] >= 9.9 and rel < TOL:
        return b['t'], rel, b['E']
    return None


while True:
    for run in RUNS:
        stop = os.path.join(HERE, 'runs', f'STOP_{run}_N{N}')
        if os.path.exists(stop):
            continue
        r = check(run)
        if r is not None:
            open(stop, 'w').write(json.dumps(dict(t=r[0], rel_change_10=r[1], E=r[2])))
            with open(os.path.join(HERE, 'runs', 'stop_watcher.log'), 'a') as fh:
                fh.write(f'{time.ctime()} {run} N={N}: t={r[0]} rel change over last 10 units {r[1]:.2e} E={r[2]:.7f} -> stop\n')
    time.sleep(30)
