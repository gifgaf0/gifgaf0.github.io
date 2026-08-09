#!/usr/bin/env python3
# compare_ghs.py — CC vs chat G_HS checkpoints (run only AFTER the CC checkpoint
# is written + hashed). Reports per-field deviations and a mechanism check: the
# CC family evaluated at the chat leg's grid-quantized dstar.
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
cc = json.load(open(os.path.join(HERE, 'poly1_hexghs_cc.json')))
ch = json.load(open(os.path.join(HERE, 'embeds', 'poly1_hexghs_chat.json')))

def rel(a, b):
    if a is None or b is None:
        return None
    den = max(abs(a), abs(b), 1e-300)
    return abs(a - b) / den

print('== CONTROLS: CC vs chat ==')
worst = 0.0
for name in ch['controls']:
    a, b = cc['controls'][name], ch['controls'][name]
    r_lo, r_hi = rel(a['mu'][0], b['mu'][0]), rel(a['mu'][1], b['mu'][1])
    worst = max(worst, r_lo, r_hi)
    print('{:14s} mu_lo rel {:.2e}   mu_hi rel {:.2e}   dstar cc={} chat={}'.format(
        name, r_lo, r_hi, a['dstar'], b['dstar']))
print('worst control band-edge rel deviation: {:.2e}'.format(worst))

print('\n== FRAMEWORK TENSORS: CC vs chat ==')
for cfg in ('hex:step', 'hex:gem8'):
    a, b = cc['results'][cfg], ch['results'][cfg]
    at, bt = a['tet_primary'], b['tet_primary']
    print(cfg)
    for f in ('mu_lo', 'mu_hi', 'vT_lo', 'vT_hi', 'halfwidth_pct'):
        print('  tet {:14s} cc {:.9g}   chat {:.9g}   rel {:.2e}'.format(
            f, at[f], bt[f], rel(at[f], bt[f])))
    print('  tet K_PM        cc [{:.6f},{:.6f}]  chat [{:.6f},{:.6f}]  rel [{:.1e},{:.1e}]'
          .format(at['K_PM'][0], at['K_PM'][1], bt['K_PM'][0], bt['K_PM'][1],
                  rel(at['K_PM'][0], bt['K_PM'][0]), rel(at['K_PM'][1], bt['K_PM'][1])))
    print('  tet dstar       cc {}   chat {}'.format(at['dstar'], bt['dstar']))
    for br in ('hex_measured_guarded', 'hex_exact_projection'):
        print('  {:20s} mu rel [{:.2e}, {:.2e}]'.format(
            br, rel(a[br]['mu_lo'], b[br]['mu_lo']), rel(a[br]['mu_hi'], b[br]['mu_hi'])))

# mechanism check: CC family at the chat dstar should reproduce the chat mu_hi
def pm_mu(c11, c12, c13, c33, c44, c66, df):
    KV = (2*(c11+c12) + 4*c13 + c33)/9.0
    GV = (c11 + c12 - 4*c13 + 2*c33)/6.0
    GR = ((c11+c12)*c33 - 2*c13*c13)/(6.0*KV)
    mu3 = (c11 - c12)/2.0
    G = GV*(1.0 + df)
    K = KV*(GR - G)/(GV - G)
    al = -1.0/(K + 4.0*G/3.0)
    be = 2.0*al/15.0 - 1.0/(5.0*G)
    ze = (G/6.0)*(9.0*K + 8.0*G)/(K + 2.0*G)
    s = (1.0 - al*(KV - K))/(GV + ze + (al/(2.0*be))*(KV - K))
    for c_, m_ in ((1.0, mu3), (2.0, c44), (1.0, c66)):
        s += c_/(m_ + ze)
    return 5.0/s - ze

vrh = json.load(open(os.path.join(HERE, 'embeds', 'poly_vrh_results.json')))
print('\n== MECHANISM CHECK: CC tet family evaluated AT the chat dstar ==')
for cfg in ('hex:step', 'hex:gem8'):
    p = vrh['vrh'][cfg]['C_over_rho']
    dch = ch['results'][cfg]['tet_primary']['dstar']
    mine_at_chat = pm_mu(p['C11'], p['C12'], p['C13'], p['C33'], p['C44'], p['C66'], dch)
    chat_hi = ch['results'][cfg]['tet_primary']['mu_hi']
    print('{:9s} mu(dstar_chat) cc {:.12f}  chat {:.12f}  rel {:.2e}'.format(
        cfg, mine_at_chat, chat_hi, rel(mine_at_chat, chat_hi)))
