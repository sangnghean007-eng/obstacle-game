#!/usr/bin/env python3
"""post_gate.py — HARD gate for epNN/release/POSTS.md. Every owner rule about posts is a check here, not a note.
Usage:  python3 funny-football/studio/post_gate.py toon2/ep41/release/POSTS.md [...]
Hook:   python3 funny-football/studio/post_gate.py --hook   (PreToolUse on SendUserFile: blocks sending an episode whose posts fail)
Add a check here every time the owner corrects a post — that is how a lesson is kept."""
import re, sys, json, os, glob
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAPS_OK = {'MLS', 'UCL', 'PSG', 'VAR', 'GOAT', 'LIVE', 'POV'}

def section(md, name):
    m = re.search(r'^## ' + re.escape(name) + r'[^\n]*\n(.*?)(?=^## |\Z)', md, re.S | re.M); return m.group(1) if m else None
def between(txt, start, stops):
    i = txt.find(start); 
    if i < 0: return None
    s = txt[i + len(start):]; ends = [s.find(x) for x in stops if s.find(x) >= 0]; return (s[:min(ends)] if ends else s).strip()
def tags(s): return re.findall(r'#\w+', s)
def caps(s): return [w for w in re.findall(r"[A-Za-zÀ-ÿ']+", s) if len(w) >= 4 and w.isupper() and w not in CAPS_OK]

def check(path):
    md = open(path).read(); E = []
    def need(c, msg):
        if not c: E.append(msg)
    body = '\n'.join(l for l in md.splitlines() if not l.startswith(('Upload settings', '# ', 'Invented', 'Real:', 'Facts', 'Story by')))
    need(not re.search(r'\bAI\b|artificial intelligence|AI-', body), 'mentions AI (owner 22 Nov: never say AI in posts)')
    need(not re.search(r'[؀-ۿ]', md), 'Arabic text (owner 21 Nov: English only)')
    yt = section(md, 'YouTube Shorts'); need(yt, 'no YouTube section')
    if yt:
        t = between(yt, '):\n', ['\n']) or ''
        need(len(t) <= 100, f'YouTube title {len(t)} chars (>100)'); need('#shorts' in t.lower(), 'YouTube title lacks #shorts'); need(len(tags(t)) == 3, f'YouTube title has {len(tags(t))} hashtags (need 3)')
        d = between(yt, 'Description:', ['Tags']) or ''; need('?' in d, 'YouTube description has no question'); need('cartoon parody' in d.lower(), 'YouTube description lacks "Cartoon parody"')
        tg = between(yt, 'Tags field):', ['Upload settings']) or ''; need(tg and len(tg) <= 500, f'YouTube Tags missing or {len(tg)} chars (>500)')
        need('Upload settings' in yt, 'YouTube upload settings missing')
    tk = section(md, 'TikTok'); need(tk, 'no TikTok section')
    if tk:
        c = between(tk, 'Caption:', ['Settings:']) or ''; need(3 <= len(tags(c)) <= 5, f'TikTok {len(tags(c))} hashtags (3–5)'); need('?' in c, 'TikTok caption has no question'); need('cartoon parody' in c.lower(), 'TikTok lacks "Cartoon parody"')
    ig = section(md, 'Instagram'); need(ig, 'no Instagram section')
    if ig:
        c = between(ig, 'Caption:', ['Cover:', 'Alt text']) or ''; need(len(tags(c)) <= 8, f'Instagram {len(tags(c))} hashtags (≤8)'); need('?' in c, 'Instagram caption has no question')
        need('Alt text' in ig, 'Instagram alt text missing'); need('Pinned comment' in ig, 'Instagram pinned comment missing'); need('cartoon parody' in c.lower(), 'Instagram lacks "Cartoon parody"')
    x = section(md, 'X (Twitter)'); need(x, 'no X section')
    if x:
        c = (x.split('Alt text')[0]).strip(); need(len(c) <= 280, f'X post {len(c)} chars (>280)'); need(len(tags(c)) <= 3, f'X {len(tags(c))} hashtags (≤3)'); need('Alt text' in x, 'X alt text missing')
    fb = section(md, 'Facebook (Reels)'); need(fb, 'no Facebook section')
    if fb:
        c = fb.strip(); need(10 <= len(c) <= 350, f'Facebook caption {len(c)} chars (Meta: 10–400; ours ≤350)'); need(len(tags(c)) <= 3, f'Facebook {len(tags(c))} hashtags (≤3)')
        need(not re.search(r'https?://|www\.', c), 'Facebook caption has a link'); cp = caps(c); need(not cp, f'Facebook ALL-CAPS words {cp} (Meta flags excess capitals)')
        need('?' in c, 'Facebook caption has no question'); need('cartoon parody' in c.lower(), 'Facebook lacks "Cartoon parody"')
    return E

def main():
    if '--hook' in sys.argv:
        try: data = json.load(sys.stdin)
        except Exception: sys.exit(0)
        files = (data.get('tool_input') or {}).get('files') or []; eps = set()
        for f in files:
            m = re.search(r'(.*?/toon2/ep\d+)/', os.path.abspath(f) if not f.startswith('/') else f)
            if m and os.path.exists(m.group(1) + '/release/POSTS.md'): eps.add(m.group(1) + '/release/POSTS.md')
        bad = {p: check(p) for p in eps}; bad = {p: e for p, e in bad.items() if e}
        if bad:
            sys.stderr.write('POST GATE FAIL — fix the posts before sending:\n' + '\n'.join(f'{p}: ' + '; '.join(e) for p, e in bad.items()) + '\n'); sys.exit(2)
        sys.exit(0)
    paths = sys.argv[1:] or sorted(glob.glob(os.path.join(ROOT, 'toon2', 'ep*', 'release', 'POSTS.md')))
    fails = 0
    for p in paths:
        e = check(p); fails += bool(e); print(('FAIL ' if e else 'PASS ') + os.path.relpath(p, ROOT) + ('' if not e else '\n   - ' + '\n   - '.join(e)))
    sys.exit(1 if fails else 0)
if __name__ == '__main__': main()
