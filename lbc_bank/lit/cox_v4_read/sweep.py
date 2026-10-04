import re, json, sys, collections
L = open('cox_v4.txt', encoding='utf-8').read().split('\n')
N = len(L)
# page map: printed page = footers before line + 1
page = []; p = 1
for s in L:
    page.append(p)
    if 'Mitchell A. Cox ↑ Contents v4.0' in s: p += 1
# section map from body headings: lines like "6.6.1 Title" or "25 Gravity" chapter starts after TOC
hdr_re = re.compile(r'^(?:[A-H]|\d{1,2})(?:\.\d{1,2}){0,3} [A-Z][^.]{2,90}$')
toc_end = 940
secs = []
for i in range(toc_end, N):
    s = L[i].strip()
    if hdr_re.match(s) and not s.startswith('THE COSSERAT') and len(s.split()) <= 14:
        secs.append((i, s))
def sec_of(i):
    lo, hi = 0, len(secs)-1; best = None
    for (j, s) in secs:
        if j <= i: best = s
        else: break
    return best
terms = collections.OrderedDict([
 ('second sound', r'second[\s-]+sound'),
 ('first sound', r'first[\s-]+sound'),
 ('fourth sound', r'fourth[\s-]+sound'),
 ('longitudinal', r'longitudinal'),
 ('compression', r'compress'),
 ('bulk modulus', r'bulk\s+modul'),
 ('Cherenkov', r'[CČ]h?erenkov|Cerenkov|Čerenkov|Tcherenkov'),
 ('Landau (crit/vel)', r'Landau\s+(critical|criterion|velocity)'),
 ('critical velocity', r'critical\s+(velocity|speed)'),
 ('drag', r'\bdrag'),
 ('friction', r'friction'),
 ('dissipat', r'dissipat'),
 ('Mach', r'\bMach\b'),
 ('supersonic', r'supersonic|transonic|intersonic'),
 ('superluminal', r'superluminal'),
 ('subluminal', r'subluminal'),
 ('aether wind', r'aether\s+wind|ether\s+wind'),
 ('Einstein-aether', r'Einstein[\s–-]+aether|khronometric'),
 ('GW170817', r'GW\s?170817'),
 ('Coleman-Glashow', r'Coleman|Glashow'),
 ('Moore-Nelson', r'Moore|Nelson'),
 ('two-fluid', r'two[\s-]+fluid'),
 ('superfluid fraction', r'superfluid\s+fraction|f_s|\bfs\b'),
 ('Goldstone', r'Goldstone'),
 ('phase mode', r'phase\s+mode|phase\s+field|condensate\s+phase'),
 ('Frank/Eshelby', r'\bFrank\b|Eshelby|Weertman'),
 ('relativistic dislocation', r'relativistic\s+(dislocation|contraction)|Lorentz\s+contraction'),
 ('speed limit', r'speed\s+limit|limiting\s+(speed|velocity)'),
 ('radiation reaction', r'radiation\s+reaction|radiation\s+damping|phonon\s+(emission|radiation|wind)'),
 ('sound speed', r'sound\s+speed|speed\s+of\s+sound'),
 ('c_L', r'\bc_?L\b|\bcL\b|\bc_l\b|\bvL\b'),
 ('Poli/Kunimi/Martone', r'Poli|Kunimi|Martone|Shlyapnikov|Astrakharchik|Pitaevskii'),
 ('Barcelo/Visser/Liberati', r'Barcel|Visser|Liberati|Weinfurtner'),
 ('mono-/bi-metric', r'bi-?metric|mono-?metric|multi-?metric'),
])
out = collections.OrderedDict()
for k, rx in terms.items():
    r = re.compile(rx, re.I if k not in ('Mach','c_L','superfluid fraction') else 0)
    hits = [i for i in range(toc_end, N) if r.search(L[i])]
    by = collections.Counter(sec_of(i) for i in hits)
    out[k] = dict(n=len(hits), lines=[i+1 for i in hits], top=by.most_common(12))
json.dump(dict(N=N, secs=[(i+1,s,page[i]) for i,s in secs], hits=out), open('sweep.json','w'), ensure_ascii=False, indent=0)
for k,v in out.items():
    print(f"{k:26s} {v['n']:5d}   " + '; '.join(f"{(s or '?')[:38]}×{c}" for s,c in v['top'][:6]))
print("sections found:", len(secs))
