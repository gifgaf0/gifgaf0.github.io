import re, sys
L = [s.rstrip('\r') for s in open('cox_v4.txt', encoding='utf-8').read().split('\n')]
N = len(L)
odd = re.compile(r'^THE COSSERAT SUPERSOLID (\d{1,3})$')
even = re.compile(r'^(\d{1,3}) (?:\d{1,2}\.|[A-H]\.)? ?[A-Z][A-Z0-9 .,:’\'–\-()∗]+$')
sec = re.compile(r'^((?:\d{1,2}|[A-H])(?:\.\d{1,2}){1,3}) [A-Z0-9].{2,100}$')
page = [None]*N; cur = None; secname = [None]*N; cs = None
for i, s in enumerate(L):
    m = odd.match(s) or even.match(s)
    if m and i > 1300: cur = int(m.group(1)) 
    if i > 1300 and sec.match(s) and not s.endswith('. .') and '. . .' not in s: cs = s
    page[i] = cur; secname[i] = cs
def show(a, b):
    # page: header precedes the page body; text before first header on the page belongs to that header's page
    print(f"=== L{a}-{b}  p.{page[a-1]}  [{secname[a-1]}]")
    for j in range(a-1, b):
        print(f"{j+1:6d}  {L[j]}")
for arg in sys.argv[1:]:
    a, b = (arg.split('-') + [None])[:2]
    a = int(a); b = int(b) if b else a
    show(a, b)
