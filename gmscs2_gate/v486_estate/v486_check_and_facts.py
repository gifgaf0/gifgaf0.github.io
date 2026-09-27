#!/usr/bin/env python3
"""v486_check_and_facts.py — the V4.86 pre-fold check (the H-MS2-8 process note made executable).
1. `git ls-remote origin` (LIVE): refs/heads/main and any gmscs2-estate branch; the time.
2. If main is still 14bcf93 → exit 3 (HK-2 not merged; nothing to do).
3. Else full-refspec fetch; find the merge commit on main whose diff (vs first parent) lies entirely under gmscs2_gate/ and
   adds gmscs2_gate/estate/; read the PR number and branch from its message, the head from its second parent, the UTC date.
4. Verify the landed estate: every manifest entry byte-identical to /home/claude/hk2/estate (16/16), CC's landing note
   present, the merge diff touching nothing outside gmscs2_gate/. Any failure → exit 4 with the reason (the fold is NOT run).
5. Write /home/claude/v486/v486_facts.json for foldin_v4_86_hk_closeout.py (auth_md5/auth_bytes filled later by the runbook
   once FOLD_AUTHORIZATION_V4_86.md carries the observation) → exit 0.
Exit codes: 0 verified-and-ready, 3 not merged, 4 merged-but-verification-failed."""
import subprocess, re, json, hashlib, sys, datetime, os
R = '/home/claude/ccrepo'; H = '/home/claude/hk2/estate'
def git(*a): return subprocess.run(['git', '-C', R, *a], capture_output=True, text=True)
now = datetime.datetime.now(datetime.timezone.utc)
ls = git('ls-remote', 'origin').stdout
assert ls, "ls-remote returned nothing — remote unreachable; halt"
refs = {l.split('\t')[1]: l.split('\t')[0] for l in ls.strip().splitlines()}
main = refs['refs/heads/main']; est_branches = {k: v for k, v in refs.items() if k.startswith('refs/heads/') and 'gmscs2' in k and 'estate' in k}
obs = {'ls_remote_utc': now.strftime('%Y-%m-%d %H:%M:%S UTC'), 'main': main, 'main7': main[:7], 'estate_branches': est_branches}
print(f"ls-remote @ {obs['ls_remote_utc']}: refs/heads/main = {main[:7]}; estate branches: {list(est_branches) or 'none'}")
if main.startswith('14bcf93'):
    print("HK-2 not merged (main unchanged at 14bcf93)"); json.dump(obs, open('/home/claude/v486/last_lsremote.json', 'w'), indent=1); sys.exit(3)
git('config', 'remote.origin.fetch', '+refs/heads/*:refs/remotes/origin/*'); git('fetch', 'origin', '--prune', '--depth=300')
assert git('rev-parse', 'origin/main').stdout.strip() == main, "fetched origin/main != ls-remote main — halt"
log = git('log', 'origin/main', '--format=%H|%P|%cI|%s', '-20').stdout.strip().splitlines()
found = None
for line in log:
    h, parents, ci, subj = line.split('|', 3)
    ps = parents.split()
    if h.startswith('14bcf93'): break
    if len(ps) == 2:
        files = git('diff', '--name-only', ps[0], h).stdout.split()
        if files and all(f.startswith('gmscs2_gate/') for f in files) and any(f.startswith('gmscs2_gate/estate/') for f in files):
            m = re.search(r'Merge pull request #(\d+) from gifgaf0/(\S+)', subj)
            found = dict(merge=h[:7], merge_full=h, pr=f"#{m.group(1)}" if m else '?', branch=m.group(2) if m else '?', head=ps[1][:7], ci=ci, files=files, subj=subj); break
if not found:
    print("main moved but no gmscs2_gate/estate merge found in the last 20 commits — HALT, report"); json.dump(obs, open('/home/claude/v486/last_lsremote.json', 'w'), indent=1); sys.exit(4)
dt = datetime.datetime.fromisoformat(found['ci']); utc = dt.astimezone(datetime.timezone.utc); pdt = dt.astimezone(datetime.timezone(datetime.timedelta(hours=-7)))
print(f"merge: PR {found['pr']} {found['merge']} from {found['branch']} (head {found['head']}) at {utc:%Y-%m-%d %H:%M:%S} UTC; files: {len(found['files'])}")
# content verification
man = git('show', f"{main}:gmscs2_gate/estate/ESTATE_MANIFEST.md5").stdout
problems = []
if not man: problems.append("ESTATE_MANIFEST.md5 absent on main")
ok = 0; n = 0
for line in man.strip().splitlines():
    md, f = line.split(); f = f[2:] if f.startswith('./') else f; n += 1
    b = subprocess.run(['git', '-C', R, 'show', f"{main}:gmscs2_gate/estate/{f}"], capture_output=True).stdout
    loc = open(os.path.join(H, f), 'rb').read()
    if b == loc and hashlib.md5(b).hexdigest() == md: ok += 1
    else: problems.append(f"{f}: not byte-identical / md5 {hashlib.md5(b).hexdigest()[:8]} vs manifest {md[:8]}")
man_local = open(os.path.join(H, 'ESTATE_MANIFEST.md5')).read()
if man != man_local: problems.append("manifest on main != delivered manifest")
landing = subprocess.run(['git', '-C', R, 'show', f"{main}:gmscs2_gate/estate/CC_LANDING_VERIFICATION.md"], capture_output=True).stdout
if not landing: problems.append("CC_LANDING_VERIFICATION.md absent")
ret = subprocess.run(['git', '-C', R, 'show', f"{main}:gmscs2_gate/HK2_CC_RETURN_INBAND.md"], capture_output=True).stdout
outside = [f for f in found['files'] if not f.startswith('gmscs2_gate/')]
if outside: problems.append(f"merge touched outside gmscs2_gate/: {outside}")
print(f"estate on main: {ok}/{n} byte-identical to the delivered estate; landing note: {'present ' + hashlib.md5(landing).hexdigest()[:8] if landing else 'ABSENT'}; HK-2 return: {'present ' + hashlib.md5(ret).hexdigest()[:8] if ret else 'absent (delivered alone or not yet)'}")
if problems or ok != n or n != 16:
    print("VERIFICATION FAILED — the fold is NOT run:"); [print("  -", p) for p in problems]; json.dump({'obs': obs, 'found': found, 'problems': problems}, open('/home/claude/v486/last_lsremote.json', 'w'), indent=1, default=str); sys.exit(4)
facts = {
    'fold_date_long': f"{now:%B} {now.day}, {now.year}", 'fold_utc': now.strftime('%H:%M UTC'),
    'directive_stamp': 'September 27, 2026, 12:49 PDT', 'auth_md5': '⟨auth_md5⟩', 'auth_bytes': '⟨auth_bytes⟩',
    'hk2_pr': found['pr'], 'hk2_branch': found['branch'], 'hk2_head': found['head'], 'hk2_merge': found['merge'],
    'hk2_utc': utc.strftime('%Y-%m-%d %H:%M:%S'), 'hk2_pdt': pdt.strftime('%B %d, %H:%M:%S'),
    'landing_md5': hashlib.md5(landing).hexdigest(), 'landing_bytes': f"{len(landing):,}", 'estate_ok': f"{ok}/{n} byte-identical to the delivered estate (manifest 23d2dbf5), the manifest on main identical to the delivered one",
    'lsremote_main': main[:7], 'lsremote_utc': now.strftime('%Y-%m-%d %H:%M:%S'),
    'hk2_return': (f"`gmscs2_gate/HK2_CC_RETURN_INBAND.md` {hashlib.md5(ret).hexdigest()[:8]} on main" if ret else "delivered to the author outside the tree (not on main)"),
    'store_note': "uploaded byte-identical in place of V4.85 (the swap the author authorized for V4.84 → V4.85); the fold script and the authorization record in the estate (outputs/gmscs2/v486/) and, as the store allows, in project knowledge.",
    'estate_tar_md5': 'd86b9ffde9a6cf53fe11dd5009472b24', 'erratum_md5': '196dbe30e9f5ab71169e7f90c61a62c8',
    'observation': obs, 'merge_files': found['files'],
}
json.dump(facts, open('/home/claude/v486/v486_facts.json', 'w'), indent=1, ensure_ascii=False)
print("VERIFIED AND READY — v486_facts.json written (auth_md5/auth_bytes to be filled by the runbook)"); sys.exit(0)
