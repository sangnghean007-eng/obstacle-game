"""novelty.py — gate 7: a new episode must not repeat recent ones (owner, 21 Nov 2026: "Đừng để các video trùng lặp nhau").

    python3 toon2/novelty.py                 # report: which axes repeat most across the registry
    python3 toon2/novelty.py candidate.csv   # check one candidate row (same header as studio/EPISODES.csv)

Rules (window = how many previous episodes are checked):
  format 4 · style 1 (and ≤1 in 4) · music 6 · lead: a person ≤2 times in the last 5 (incl. candidate) · setting 1 ·
  twist 3 · ending 3 · cover 1 · gags: never reused · overall similarity to ANY earlier episode ≤ 40 %.
"""
import csv, os, sys
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__)); REG = os.path.join(HERE, '..', 'studio', 'EPISODES.csv')
AXES = ['topic_group', 'lead', 'format', 'style', 'music', 'setting', 'shots', 'structure', 'techniques', 'gags', 'twist', 'ending', 'palette', 'cover']
S = lambda v: set(x.strip().lower() for x in (v or '').split(';') if x.strip() and x.strip().lower() != 'none')

def load(p):
    with open(p, newline='') as f: return list(csv.DictReader(f))

def sim(a, b):  # mean Jaccard over the 14 axes
    tot = 0
    for ax in AXES:
        x, y = S(a.get(ax)), S(b.get(ax)); tot += (len(x & y) / len(x | y)) if (x | y) else 0
    return tot / len(AXES)

def check(c, hist):
    fails = []
    def recent(n): return hist[-n:]
    def rule(ax, n, label):
        for h in recent(n):
            if S(c.get(ax)) & S(h.get(ax)): fails.append(f"{label}: '{c.get(ax)}' repeats Ep{h['ep']}"); return
    rule('format', 4, 'format (window 4)'); rule('style', 1, 'style (previous episode)'); rule('music', 6, 'music genre (window 6)')
    rule('setting', 1, 'main setting (previous episode)'); rule('twist', 3, 'twist (window 3)'); rule('ending', 3, 'ending type (window 3)'); rule('cover', 1, 'cover layout (previous)')
    if sum(1 for h in recent(4) if S(c.get('style')) & S(h.get('style'))) >= 1: pass
    cnt = Counter(p for h in recent(4) for p in S(h.get('lead')))
    for p in S(c.get('lead')):
        if cnt[p] + 1 > 2: fails.append(f"lead: {p} would appear {cnt[p] + 1}× in the last 5 episodes (max 2)")
    used = set(g for h in hist for g in S(h.get('gags')))
    for g in S(c.get('gags')) & used: fails.append(f"gag reused: {g}")
    worst = max(((sim(c, h), h['ep']) for h in hist), default=(0, None))
    if worst[0] > 0.40: fails.append(f"overall similarity {worst[0]:.0%} to Ep{worst[1]} (max 40%)")
    return fails, worst

def report(rows):
    print(f"{len(rows)} episodes in the registry\n")
    for ax in ['format', 'style', 'music', 'setting', 'shots', 'ending', 'cover', 'lead', 'palette']:
        c = Counter(v for r in rows for v in S(r.get(ax))); top = c.most_common(3)
        print(f"{ax:<9} " + ' · '.join(f"{k} ×{n}" for k, n in top))
    last = rows[-10:]; print('\nLast 10 episodes, pairwise max similarity:')
    for i, r in enumerate(last):
        w = max(((sim(r, h), h['ep']) for h in rows if h['ep'] != r['ep']), default=(0, '-'))
        print(f"  Ep{r['ep']:<3} most like Ep{w[1]:<3} {w[0]:.0%}{'  ← too similar' if w[0] > .40 else ''}")

if __name__ == '__main__':
    rows = load(REG)
    if len(sys.argv) < 2: report(rows); sys.exit(0)
    for c in load(sys.argv[1]):
        fails, worst = check(c, rows)
        print(f"Candidate Ep{c['ep']}: most similar Ep{worst[1]} {worst[0]:.0%}")
        for f in fails: print('  FAIL', f)
        print('NOVELTY PASS' if not fails else f'NOVELTY FAIL ({len(fails)})')
        sys.exit(1 if fails else 0)
