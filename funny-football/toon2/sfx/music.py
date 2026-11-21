"""music.py — sound engine v2: real song structure, better instruments, a hook per episode (overhaul M1b, 21 Nov 2026).

    from music import Song
    s = Song('phonk', bpm=140, key='F#', minor=True, seed=31)
    s.form([('intro', 4), ('build', 4), ('drop', 8), ('break', 4), ('drop', 8), ('outro', 2)])   # bars
    stems = s.render()          # dict of stereo numpy arrays: drums, bass, chords, lead, fx
Everything is synthesised (no samples), seeded so each episode has its own hook but is reproducible.
"""
import numpy as np
from scipy.signal import butter, sosfilt, lfilter
SR = 44100
NOTE = {'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3, 'E': 4, 'F': 5, 'F#': 6, 'Gb': 6, 'G': 7, 'G#': 8, 'Ab': 8, 'A': 9, 'A#': 10, 'Bb': 10, 'B': 11}
def mtof(m): return 440.0 * 2 ** ((m - 69) / 12)
def T(d): return np.arange(int(max(1, d) * SR) if d >= 1 else max(1, int(d * SR))) / SR
def tt(d): return np.arange(max(1, int(d * SR))) / SR
def lp(x, f, o=2): return sosfilt(butter(o, min(f, SR / 2 - 200), 'low', fs=SR, output='sos'), x)
def hp(x, f, o=2): return sosfilt(butter(o, max(f, 20), 'high', fs=SR, output='sos'), x)
def bp(x, lo, hi, o=2): return sosfilt(butter(o, [max(lo, 20), min(hi, SR / 2 - 200)], 'band', fs=SR, output='sos'), x)
def adsr(n, a=.005, d=.1, s=.7, r=.1, hold=None):
    a, d, r = int(a * SR), int(d * SR), int(r * SR); hold = n - a - d - r if hold is None else hold; hold = max(0, hold)
    e = np.concatenate([np.linspace(0, 1, max(a, 1)), np.linspace(1, s, max(d, 1)), np.full(hold, s), np.linspace(s, 0, max(r, 1))])
    return np.pad(e, (0, max(0, n - len(e))))[:n]
def sat(x, k=2.0): return np.tanh(x * k) / np.tanh(k)

class Inst:
    """All instruments return mono numpy arrays; rng gives humanised variation per hit."""
    def __init__(self, rng): self.r = rng
    # ---- drums ----
    def kick(self, d=.45, punch=1.0, tone=50):
        t = tt(d); f = tone + (tone * 3.2) * np.exp(-t * 38 * punch); ph = 2 * np.pi * np.cumsum(f) / SR
        body = np.sin(ph) * np.exp(-t * 7); click = hp(self.r.standard_normal(len(t)), 2500) * np.exp(-t * 300) * .35
        return sat(body + click, 1.6) * .95
    def k808(self, note, d=.9, glide_from=None):
        t = tt(d); f0 = mtof(note); fs = mtof(glide_from) if glide_from else f0 * 2.2
        f = f0 + (fs - f0) * np.exp(-t * (18 if not glide_from else 6)); x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 2.2)
        return sat(x, 2.2) * adsr(len(t), .002, .05, 1, .08)
    def snare(self, d=.28, bright=1.0):
        t = tt(d); n = self.r.standard_normal(len(t)); body = np.sin(2 * np.pi * 185 * t) * np.exp(-t * 28) * .6
        wires = bp(n, 1800, 9000) * np.exp(-t * (16 / bright)) * .8; return sat(body + wires + lp(n, 3000) * np.exp(-t * 40) * .3, 1.3)
    def clap(self, d=.35):
        t = tt(d); n = bp(self.r.standard_normal(len(t)), 900, 6000); e = np.zeros(len(t))
        for k, o in enumerate((0, .011, .022, .034)): i = int(o * SR); e[i:] += np.exp(-(t[: len(t) - i]) * (90 if k < 3 else 14)) * (1 if k < 3 else .9)
        return n * e * .7
    def hat(self, open_=False):
        d = .35 if open_ else .05; t = tt(d); m = sum(np.sign(np.sin(2 * np.pi * f * t)) for f in (205.3, 304.4, 369.6, 522.7, 540, 800))
        x = lp(hp(m * .12 + self.r.standard_normal(len(t)) * .6, 7000), 14000); return x * np.exp(-t * (9 if open_ else 80)) * .3
    def rim(self): t = tt(.08); return bp(np.sin(2 * np.pi * 1700 * t) + self.r.standard_normal(len(t)) * .3, 1000, 5000) * np.exp(-t * 60)
    def shaker(self): t = tt(.09); return hp(self.r.standard_normal(len(t)), 5000) * adsr(len(t), .02, .03, .3, .03) * .35
    def conga(self, hi=True): t = tt(.3); f = (330 if hi else 220) * (1 + .3 * np.exp(-t * 40)); return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 12)
    def cowbell(self): t = tt(.25); return bp(np.sign(np.sin(2 * np.pi * 587 * t)) + np.sign(np.sin(2 * np.pi * 845 * t)), 500, 2500) * np.exp(-t * 14) * .25
    def crash(self, d=2.0): t = tt(d); return hp(self.r.standard_normal(len(t)), 4000) * np.exp(-t * 2.2) * .5
    def riser(self, d=2.0): t = tt(d); n = self.r.standard_normal(len(t)); return np.array([0.0]) if len(t) < 2 else bp(n, 400, 8000) * (t / d) ** 2 * .5 + np.sin(2 * np.pi * np.cumsum(200 + 1800 * (t / d) ** 2) / SR) * (t / d) ** 3 * .2
    def impact(self, d=2.5): t = tt(d); return sat(np.sin(2 * np.pi * np.cumsum(60 * np.exp(-t * 1.5) + 30) / SR) * np.exp(-t * 1.8) + lp(self.r.standard_normal(len(t)), 800) * np.exp(-t * 3), 1.5)
    # ---- tonal ----
    def sub(self, note, d): t = tt(d); return np.sin(2 * np.pi * mtof(note) * t) * adsr(len(t), .005, .05, .9, .06)
    def reese(self, note, d, cut=900):
        t = tt(d); f = mtof(note); x = sum(2 * ((t * f * k) % 1) - 1 for k in (1, 1.007, .993)) / 3 + .5 * np.sin(2 * np.pi * f / 2 * t)
        return lp(x, cut + 500 * np.sin(2 * np.pi * .5 * t).mean()) * adsr(len(t), .01, .1, .85, .08)
    def slap(self, note, d):  # vectorised Karplus-Strong pluck + pop
        n = max(2, int(d * SR)); L = max(2, int(SR / mtof(note))); x = np.zeros(n); x[:L] = self.r.uniform(-1, 1, L)
        a = np.zeros(L + 2); a[0] = 1; a[L] = -.497; a[L + 1] = -.497; y = lfilter([1], a, x); return lp(y, 3500) * adsr(n, .001, .1, .6, .05) * 1.2
    def pluck(self, note, d, bright=.5):
        n = max(2, int(d * SR)); L = max(2, int(SR / mtof(note))); x = np.zeros(n); x[:L] = lp(self.r.uniform(-1, 1, L + 64), 2000 + 6000 * bright)[:L]
        a = np.zeros(L + 2); a[0] = 1; a[L] = -.4985; a[L + 1] = -.4985; return lfilter([1], a, x) * .9
    def piano(self, note, d, vel=.8):
        t = tt(d); f = mtof(note); x = np.zeros(len(t))
        for k in range(1, 9): fk = f * k * np.sqrt(1 + .0004 * k * k); x += np.sin(2 * np.pi * fk * t) * (vel ** (k * .5)) / k * np.exp(-t * (1.2 + k * .6))
        ham = lp(self.r.standard_normal(len(t)), 3000) * np.exp(-t * 120) * .15; return (x + ham) * adsr(len(t), .002, .3, .6, .15) * .5
    def epiano(self, note, d):
        t = tt(d); f = mtof(note); mod = np.sin(2 * np.pi * f * 14 * t) * 1.2 * np.exp(-t * 9)
        return np.sin(2 * np.pi * f * t + mod) * np.exp(-t * 1.6) * adsr(len(t), .003, .2, .7, .12) * .5
    def organ(self, note, d): t = tt(d); f = mtof(note); x = sum(np.sin(2 * np.pi * f * m * t) * a for m, a in ((.5, .5), (1, 1), (2, .6), (3, .3), (4, .25))); return x * adsr(len(t), .01, .05, .9, .05) * (1 + .08 * np.sin(2 * np.pi * 6.5 * t)) * .22
    def strings(self, note, d, bright=1.0):
        t = tt(d); f = mtof(note); x = sum(2 * ((t * f * dt + ph) % 1) - 1 for dt, ph in ((1, 0), (1.004, .3), (.996, .6), (1.002, .1), (.998, .8))) / 5
        return lp(x, 1500 * bright + 800) * adsr(len(t), .25, .3, .8, .4) * (1 + .03 * np.sin(2 * np.pi * 5 * t)) * .35
    def brass(self, note, d):
        t = tt(d); f = mtof(note); x = sum(2 * ((t * f * k) % 1) - 1 for k in (1, 1.003)) / 2; env = adsr(len(t), .03, .1, .8, .08)
        return np.array([lp(x[i:i + 2048], 600 + 2600 * env[i]) for i in range(0, len(x), 2048)], dtype=object).sum() if False else lp(x, 2400) * env * .45
    def bell(self, note, d): t = tt(d); f = mtof(note); return np.sin(2 * np.pi * f * t + 2.5 * np.sin(2 * np.pi * f * 3.5 * t) * np.exp(-t * 3)) * np.exp(-t * 2.5) * .4
    def lead(self, note, d, kind='saw', vib=.012, porta_from=None):
        t = tt(d); f0 = mtof(note); f = f0 * (1 + vib * np.sin(2 * np.pi * 5.5 * t) * np.minimum(1, t * 4))
        if porta_from: f = f + (mtof(porta_from) - f0) * np.exp(-t * 30)
        ph = np.cumsum(f) / SR
        x = {'saw': sum(2 * ((ph * k) % 1) - 1 for k in (1, 1.006, .994)) / 3, 'square': np.sign(np.sin(2 * np.pi * ph)) * .6, 'sine': np.sin(2 * np.pi * ph),
             'chip': np.sign(np.sin(2 * np.pi * ph)) * .5 + (2 * ((ph * 2) % 1) - 1) * .1, 'whistle': np.sin(2 * np.pi * ph) + .05 * self.r.standard_normal(len(t)),
             'flute': np.sin(2 * np.pi * ph) + .3 * np.sin(4 * np.pi * ph) + .08 * lp(self.r.standard_normal(len(t)), 4000)}[kind]
        return lp(x, 5000 if kind != 'chip' else 12000) * adsr(len(t), .01 if kind not in ('flute', 'whistle') else .04, .08, .75, .06) * .4
    def vox_chop(self, note, d):  # formant "ah/oh" chop — hooky vocal-like stab (not a real voice)
        t = tt(d); f = mtof(note); src = sum(np.sin(2 * np.pi * f * k * t) / k for k in range(1, 18))
        x = bp(src, 650, 1100) + .6 * bp(src, 1000, 1400) + .3 * bp(src, 2400, 2800); return x * adsr(len(t), .01, .05, .8, .05) * .6

GENRES = {  # bpm, swing, drum pattern (16 steps per bar: K kick, S snare, C clap, h hat, o open hat, r rim, s shaker), bass instrument, chord instrument, lead instrument
    'phonk':     dict(bpm=140, swing=0, drums={'kick': 'K.....K...K.....', 'snare': '....C.......C...', 'hat': 'hhhhhhhhhhhhhhhh', 'cowbell': '..x...x.x...x...'}, bass='k808', chords='strings', lead='bell'),
    'trap':      dict(bpm=145, swing=0, drums={'kick': 'K......K..K.....', 'snare': '........C.......', 'hat': 'h.h.hhh.h.h.hhhh'}, bass='k808', chords='epiano', lead='bell'),
    'funk':      dict(bpm=108, swing=.12, drums={'kick': 'K..K..K...K.K...', 'snare': '....S..s....S...', 'hat': 'h.hhh.hhh.hhh.ho'}, bass='slap', chords='epiano', lead='brass'),
    'western':   dict(bpm=92, swing=.08, drums={'kick': 'K.......K.......', 'rim': '....r.......r...', 'shaker': 's.s.s.s.s.s.s.s.'}, bass='pluck', chords='pluck', lead='whistle'),
    'chiptune':  dict(bpm=150, swing=0, drums={'kick': 'K...K...K...K...', 'snare': '....S.......S...', 'hat': 'hhhhhhhhhhhhhhhh'}, bass='chipbass', chords='chip', lead='chip'),
    'orchestral':dict(bpm=100, swing=0, drums={'kick': 'K.......K.......', 'snare': '............S...'}, bass='strings', chords='strings', lead='brass'),
    'latin':     dict(bpm=104, swing=.05, drums={'kick': 'K..K....K..K....', 'rim': '..r..r....r..r..', 'conga': 'x.x..xx.x.x..xx.', 'shaker': 'ssssssssssssssss'}, bass='sub', chords='piano', lead='flute'),
    'dancehall': dict(bpm=98, swing=.04, drums={'kick': 'K..K..K.K..K..K.', 'snare': '...S..S....S..S.', 'hat': 'h.h.h.h.h.h.h.h.'}, bass='sub', chords='organ', lead='vox'),
    'lofi':      dict(bpm=82, swing=.18, drums={'kick': 'K......K..K.....', 'snare': '....S.......S...', 'hat': 'h.h.h.h.h.h.h.hh'}, bass='sub', chords='epiano', lead='flute'),
    'surf':      dict(bpm=160, swing=0, drums={'kick': 'K...K...K...K...', 'snare': '....S.......S..S', 'hat': 'hhhhhhhhhhhhhhhh'}, bass='pluck', chords='organ', lead='pluck'),
    'noirjazz':  dict(bpm=76, swing=.22, drums={'rim': '....r.......r...', 'hat': 'h..h.hh..h.hh..h', 'kick': 'K.........K.....'}, bass='pluck', chords='piano', lead='sine'),
    'trailer':   dict(bpm=120, swing=0, drums={'kick': 'K.......K.....K.', 'snare': '........S.......'}, bass='reese', chords='strings', lead='brass'),
}
PROG = {False: [[0, 4, 7], [7, 11, 14], [9, 12, 16], [5, 9, 12]],  # major I V vi IV
        True: [[0, 3, 7], [8, 12, 15], [3, 7, 10], [10, 14, 17]]}  # minor i VI III VII
SCALE = {False: [0, 2, 4, 5, 7, 9, 11], True: [0, 2, 3, 5, 7, 8, 10]}

class Song:
    def __init__(self, genre, bpm=None, key='C', minor=False, seed=0):
        g = GENRES[genre]; self.g = g; self.genre = genre; self.bpm = bpm or g['bpm']; self.root = 48 + NOTE[key]; self.minor = minor
        self.r = np.random.default_rng(seed); self.I = Inst(self.r); self.sections = []; self.hook = self._make_hook()
    def _make_hook(self):  # a 2-bar motif (call) + answer: catchy = repetition + one leap + rhythmic identity
        sc = SCALE[self.minor]; r = self.r; RH = [[0, 3, 6, 8, 10, 12], [0, 2, 3, 6, 8, 11, 14], [0, 4, 6, 7, 10, 12, 14], [0, 3, 4, 7, 8, 11, 12]]; rhythm = RH[int(r.integers(len(RH)))]
        deg = [0];
        for _ in range(len(rhythm) - 1): deg.append(int(np.clip(deg[-1] + int(r.choice([-2, -1, 1, 1, 2, 4, -3])), -3, 9)))
        call = [(s, deg[i]) for i, s in enumerate(rhythm)]; ans = [(s, d if i < len(rhythm) - 2 else (0 if i == len(rhythm) - 1 else d)) for i, (s, d) in enumerate(call)]
        ans = [(s, d + (1 if i == len(ans) // 2 else 0)) for i, (s, d) in enumerate(ans)]
        to_m = lambda d: self.root + 24 + 12 * (d // 7) + sc[d % 7]; return [(s, to_m(d)) for s, d in call], [(s, to_m(d)) for s, d in ans]
    def form(self, parts): self.sections = parts; return self
    @property
    def step(self): return 60 / self.bpm / 4
    def length(self): return sum(b for _, b in self.sections) * 16 * self.step
    def render(self):
        n = int((self.length() + 3) * SR); st = {k: np.zeros(n) for k in ('drums', 'bass', 'chords', 'lead', 'fx')}; hits = []
        def put(k, x, t, g=1.0):
            i = int(t * SR); m = min(len(x), n - i)
            if m > 0 and i >= 0: st[k][i:i + m] += x[:m] * g
        bar0 = 0; I = self.I; g = self.g; sp = self.step
        for sec, bars in self.sections:
            dens = {'intro': .3, 'build': .7, 'drop': 1.0, 'break': .4, 'outro': .3, 'verse': .8}.get(sec, .8)
            for b in range(bars):
                tb = (bar0 + b) * 16 * sp; chord = PROG[self.minor][(bar0 + b) % 4]
                # drums
                for part, pat in g['drums'].items():
                    if sec in ('intro', 'break') and part in ('kick', 'snare') and dens < .5 and b % 2: continue
                    for i, c in enumerate(pat):
                        if c == '.': continue
                        t = tb + i * sp + (g['swing'] * sp if i % 2 else 0) + self.r.normal(0, .003)
                        v = .85 + self.r.uniform(-.1, .1)
                        if part == 'kick': put('drums', I.kick(), t, v * (1 if sec != 'intro' else .6)); hits.append(t)
                        elif part == 'snare': put('drums', I.clap() if c == 'C' else I.snare(), t, v * (.6 if c == 's' else 1))
                        elif part == 'hat' and dens > .35: put('drums', I.hat(c == 'o'), t, v * .7)
                        elif part == 'rim': put('drums', I.rim(), t, v * .6)
                        elif part == 'shaker': put('drums', I.shaker(), t, v)
                        elif part == 'cowbell' and sec == 'drop': put('drums', I.cowbell(), t, v * .5)
                        elif part == 'conga': put('drums', I.conga(i % 3 == 0), t, v * .5)
                    if sec == 'build' and b == bars - 1:
                        for i in range(16): put('drums', I.snare(.12), tb + i * sp, .25 + .6 * i / 16)
                # bass
                rootn = self.root - 12 + chord[0]; bi = g['bass']
                for i in ([0, 6, 10] if bi in ('k808', 'sub', 'reese') else [0, 3, 6, 8, 10, 14]):
                    if dens < .5 and i: continue
                    d = sp * (6 if bi == 'k808' else 2.5); note = rootn + (12 if bi in ('slap', 'pluck', 'chipbass') and i in (3, 10) else 0)
                    x = {'k808': lambda: I.k808(note, d), 'sub': lambda: I.sub(note, d), 'reese': lambda: I.reese(note, d), 'slap': lambda: I.slap(note + 12, d),
                         'pluck': lambda: I.pluck(note + 12, d), 'strings': lambda: I.strings(note, d * 2), 'chipbass': lambda: I.lead(note + 12, d, 'chip', 0)}[bi]()
                    put('bass', x, tb + i * sp, .8)
                # chords
                ci = g['chords']; d = 16 * sp
                if ci in ('strings', 'organ'): [put('chords', getattr(I, ci)(self.root + 12 + c, d), tb, .5 * dens + .2) for c in chord]
                else:
                    for i in ((0, 6, 10) if ci != 'chip' else range(0, 16, 2)):
                        for c in chord:
                            x = {'epiano': lambda: I.epiano(self.root + 12 + c, sp * 4), 'piano': lambda: I.piano(self.root + 12 + c, sp * 5), 'pluck': lambda: I.pluck(self.root + 24 + c, sp * 3, .7),
                                 'chip': lambda: I.lead(self.root + 24 + c, sp * .9, 'chip', 0)}[ci]()
                            put('chords', x, tb + i * sp + (c % 5) * .004, (.35 if ci != 'chip' else .12) * (dens + .3))
                # lead hook: call on even bars, answer on odd bars, only in drops/verse (+ a hint in build)
                if sec in ('drop', 'verse') or (sec == 'build' and b == bars - 2):
                    call, ans = self.hook; motif = call if (bar0 + b) % 2 == 0 else ans; li = g['lead']
                    for k, (s, m) in enumerate(motif):
                        nxt = motif[k + 1][0] if k + 1 < len(motif) else 16; d = (nxt - s) * sp * .95
                        x = {'bell': lambda: I.bell(m, d * 1.5), 'brass': lambda: I.brass(m, d), 'whistle': lambda: I.lead(m, d, 'whistle'), 'chip': lambda: I.lead(m, d, 'chip', 0),
                             'flute': lambda: I.lead(m, d, 'flute'), 'pluck': lambda: I.pluck(m, d + .2, .9), 'sine': lambda: I.lead(m, d, 'sine'), 'vox': lambda: I.vox_chop(m, d)}[li]()
                        put('lead', x, tb + s * sp, .55 if sec != 'build' else .3)
                if sec == 'build' and b == 0: put('fx', I.riser(bars * 16 * sp), tb, .6)
                if sec == 'drop' and b == 0: put('fx', I.crash(), tb, .5); put('fx', I.impact(), tb, .35)
            bar0 += bars
        self.kick_times = hits; return st

if __name__ == '__main__':
    import sys
    s = Song(sys.argv[1] if len(sys.argv) > 1 else 'phonk', key='F#', minor=True, seed=31).form([('intro', 2), ('build', 2), ('drop', 4), ('break', 2), ('drop', 4)])
    st = s.render(); print({k: round(float(np.abs(v).max()), 2) for k, v in st.items()}, round(s.length(), 1), 's')
