"""script_gate.py — gate 2 (script) + gate 3 (shot list) + gate 6 (viral checklist) on an episode spec (overhaul M5, 21 Nov 2026).

    python3 toon2/script_gate.py toon2/ep31/spec.json

spec.json: { "logline": str, "beats": [{"shot": "low", "idea": str}], "techniques": [..], "gags": [..], "twist": str, "callback": str,
             "ending": str, "hidden_details": [..], "meme_frame": str, "hook_frame0": str, "style": str, "prev_style": str }
"""
import json, re, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
SHOTS = {'wide', 'cu', 'xcu', 'low', 'high', 'ots', 'dutch', 'split', 'slowmo', 'screen'}
TECH = {'rule-of-3', 'misdirection', 'escalation', 'cutaway', 'deadpan', 'anticlimax', '4th-wall', 'visual pun', 'sound gag', 'callback'}

def used_gags():
    t = open(os.path.join(HERE, '..', 'studio', 'GAG_BANK.md')).read(); sec = t.split('## FRESH')[0]
    return {re.sub(r'[^a-z0-9 ]', '', l.split('|')[2].strip().lower()) for l in sec.splitlines() if l.startswith('| U')}

def check(s):
    f = []; b = s.get('beats', [])
    if not s.get('logline') or len(s['logline'].split()) > 45: f.append('logline missing or longer than 45 words')
    if not 4 <= len(b) <= 8: f.append(f'{len(b)} beats (need 4–8)')
    shots = [x.get('shot') for x in b]; bad = [x for x in shots if x not in SHOTS]
    if bad: f.append(f'unknown shot types {bad}')
    if len(set(shots) - {'screen'}) < 5: f.append(f'only {len(set(shots) - {"screen"})} camera shot types (need ≥5, "screen" not counted)')
    for i in range(1, len(shots)):
        if shots[i] == shots[i - 1]: f.append(f'beats {i} and {i + 1} use the same shot ({shots[i]})')
    tech = set(t.lower() for t in s.get('techniques', [])); unk = tech - TECH
    if unk: f.append(f'unknown techniques {sorted(unk)}')
    if len(tech & TECH) < 4: f.append(f'{len(tech & TECH)} comedy techniques (need ≥4)')
    ug = used_gags()
    for g in s.get('gags', []):
        if re.sub(r'[^a-z0-9 ]', '', g.lower()) in ug: f.append(f'gag already USED: {g}')
    for k in ('twist', 'callback', 'ending', 'meme_frame', 'hook_frame0'):
        if not s.get(k): f.append(f'missing {k}')
    if len(s.get('hidden_details', [])) < 2: f.append('need ≥2 hidden details (rewatch value)')
    if s.get('style') and s.get('style') == s.get('prev_style'): f.append('style repeats the previous episode')
    for i, x in enumerate(b):
        if len(x.get('text', '').split()) > 7: f.append(f'beat {i + 1}: on-screen text over 7 words')
    return f

if __name__ == '__main__':
    s = json.load(open(sys.argv[1])); f = check(s)
    for x in f: print('  FAIL', x)
    print('SCRIPT GATE PASS' if not f else f'SCRIPT GATE FAIL ({len(f)})'); sys.exit(1 if f else 0)
