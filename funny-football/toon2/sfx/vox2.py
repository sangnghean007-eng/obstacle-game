"""vox2: procedural cartoon voices (formant synthesis, no samples, no TTS, no real voices).

Every character gets a Voice profile (pitch, vocal-tract size, breathiness, vibrato, rasp) and every call
takes a variant seed, so no two laughs / cries / gasps in the series are the same waveform.

    from vox2 import Voice, crowd
    v = Voice('mbappe', ep=17); x = v.cry('sob', 1.6)   # numpy mono @ 44.1 kHz
"""
import numpy as np, zlib
from scipy.signal import butter, sosfilt
SR = 44100
FORM = {'a': (800, 1200, 2500), 'e': (500, 1900, 2500), 'i': (300, 2300, 3000), 'o': (500, 900, 2400), 'u': (350, 800, 2300),
        'uh': (650, 1200, 2500), 'ae': (700, 1700, 2500), 'aw': (600, 1000, 2400), 'eh': (550, 1750, 2450)}
PROFILES = {  # f0 Hz, tract scale (>1 = smaller head / higher formants), breath, vibrato depth, rasp
    'ronaldo': (150, 1.00, .10, .020, .05), 'messi': (175, 1.06, .18, .015, .02), 'yamal': (210, 1.12, .12, .025, .02),
    'kane': (125, 0.95, .08, .012, .08), 'mbappe': (165, 1.04, .10, .030, .03), 'rodri': (120, 0.94, .12, .010, .10),
    'haaland': (110, 0.90, .06, .010, .12), 'kid': (290, 1.25, .12, .03, .0), 'big': (90, 0.85, .08, .01, .2),
    'generic_m': (140, 1.0, .1, .02, .05), 'generic_f': (230, 1.15, .14, .02, .0)}

def _bp(x, lo, hi): lo = max(40, lo); hi = min(SR / 2 - 100, hi); return sosfilt(butter(2, [lo, hi], 'band', fs=SR, output='sos'), x)
def _lp(x, f): return sosfilt(butter(2, min(f, SR / 2 - 100), 'low', fs=SR, output='sos'), x)
def _hp(x, f): return sosfilt(butter(2, f, 'high', fs=SR, output='sos'), x)
def _env(n, a, r):
    e = np.ones(n); na, nr = max(1, min(n, int(a * SR))), max(1, min(n, int(r * SR))); e[:na] = np.linspace(0, 1, na); e[-nr:] *= np.linspace(1, 0, nr); return e


class Voice:
    def __init__(self, who, ep=0, var=0):
        f0, size, br, vib, rasp = PROFILES.get(who, PROFILES['generic_m'])
        self.rng = np.random.default_rng(zlib.crc32(f'{who}|{ep}|{var}'.encode()))
        j = self.rng.uniform(.94, 1.06)  # per-episode drift so the same character never sounds identical twice
        self.f0, self.size, self.br, self.vib, self.rasp = f0 * j, size * self.rng.uniform(.97, 1.03), br, vib, rasp

    # --- core: a voiced syllable with a pitch contour and (optionally) moving vowel ---
    def syl(self, vowel, d, p0=1.0, p1=1.0, g=1.0, h=0.0, shake=0.0, v2=None, breath=None):
        n = int(d * SR); t = np.arange(n) / SR; r = self.rng
        f = self.f0 * np.linspace(p0, p1, n) * (1 + self.vib * np.sin(2 * np.pi * r.uniform(5, 6.5) * t) + shake * np.sin(2 * np.pi * 9 * t) + .004 * r.standard_normal(n).cumsum() / np.sqrt(np.arange(1, n + 1)))
        ph = np.cumsum(f) / SR; src = 2 * (ph % 1) - 1; src = _lp(src, 4000) + (breath if breath is not None else self.br) * r.standard_normal(n)
        if self.rasp: src *= 1 + self.rasp * r.standard_normal(n)
        F1 = np.array(FORM[vowel]) * self.size; F2 = np.array(FORM[v2 or vowel]) * self.size
        k = np.linspace(0, 1, n) if v2 else None
        out = np.zeros(n)
        for i, (bw, gain) in enumerate(((90, 1.0), (120, .6), (180, .3))):
            if v2:  # crossfade two filtered versions for a vowel glide
                a = _bp(src, F1[i] - bw, F1[i] + bw); b = _bp(src, F2[i] - bw, F2[i] + bw); out += gain * (a * (1 - k) + b * k)
            else: out += gain * _bp(src, F1[i] - bw, F1[i] + bw)
        if h: hn = int(min(h, d * .6) * SR); out[:hn] = _bp(r.standard_normal(hn), 800, 4000) * .4 * np.linspace(.5, 1, hn)
        out *= _env(n, .015, min(.08, d * .4)); return out / (np.abs(out).max() + 1e-9) * g

    def _seq(self, parts, gaps):
        out = []
        for p, gp in zip(parts, gaps): out.append(p); out.append(np.zeros(int(max(0, gp) * SR)))
        return np.concatenate(out) if out else np.zeros(1)

    # --- laughs ---
    def laugh(self, kind='belly', d=1.4):
        r = self.rng
        if kind == 'giggle': n = int(d / .12); return self._seq([self.syl('i', .07, 1.5 + r.uniform(0, .2), 1.4, .7, h=.02) for _ in range(n)], [r.uniform(.04, .07)] * n)
        if kind == 'cackle':  # evil "mwa-ha-ha-haaa"
            parts = [self.syl('u', .16, .9, 1.0, .8, v2='a')] + [self.syl('a', .12, 1.15 - i * .04, 1.1 - i * .04, .9, h=.04) for i in range(4)] + [self.syl('a', .5, 1.1, .8, .9, h=.04)]
            return self._seq(parts, [.05, .06, .06, .06, .06, 0])
        if kind == 'snicker': n = int(d / .16); return self._seq([self.syl('eh', .06, 1.2, 1.25, .5, h=.05, breath=.5) for _ in range(n)], [.1] * n)
        if kind == 'point':  # "HA! ha ha" pointing laugh
            parts = [self.syl('a', .22, 1.4, 1.2, 1.0, h=.05)] + [self.syl('a', .11, 1.2 - i * .06, 1.15 - i * .06, .7, h=.04) for i in range(4)]
            return self._seq(parts, [.12, .07, .07, .07, 0])
        n = int(d / .19)  # belly laugh, descending
        return self._seq([self.syl('a', .13, 1.2 - i * .05, 1.15 - i * .05, .9 - i * .04, h=.05) for i in range(n)], [r.uniform(.05, .08)] * n)

    # --- cries ---
    def cry(self, kind='wail', d=1.6):
        r = self.rng
        if kind == 'wail':  # "waaah-aaah"
            return self._seq([self.syl('u', .25, 1.3, 1.9, 1.0, v2='a', shake=.02), self.syl('a', d - .35, 1.9, 1.3, 1.0, shake=.04)], [.02, 0])
        if kind == 'sob':  # "uh-huh-huh" + hiccup inhale
            parts, gaps = [], []
            for i in range(int(d / .3)):
                parts.append(self.syl('uh', .14, 1.4, 1.2, .8, h=.05, shake=.05)); gaps.append(.06)
                if i % 3 == 2: parts.append(_hp(r.standard_normal(int(.18 * SR)), 1500) * .25 * _env(int(.18 * SR), .05, .05)); gaps.append(.08)
            return self._seq(parts, gaps)
        if kind == 'whimper': return self._seq([self.syl('i', .35, 2.0, 1.6, .5, breath=.4, shake=.06) for _ in range(int(d / .5))], [.15] * int(d / .5))
        if kind == 'blubber':  # wet bawling with wobble
            return self.syl('aw', d, 1.6, 1.2, 1.0, shake=.12, h=.08)
        return self.cry('wail', d)

    # --- one-shots ---
    def oof(self): return self.syl('u', .22, 1.1, .7, 1.0, h=.06)
    def ow(self): return self.syl('a', .35, 1.7, 1.1, 1.0, v2='u')
    def yelp(self): return self.syl('i', .18, 2.4, 2.9, 1.0)
    def gasp(self): n = int(.35 * SR); return _bp(self.rng.standard_normal(n), 600, 3500) * _env(n, .25, .05) * .7
    def hmph(self): return self._seq([_bp(self.rng.standard_normal(int(.12 * SR)), 300, 1200) * .5, self.syl('u', .18, .9, .8, .7, breath=.4)], [0, 0])
    def yay(self): return self.syl('e', .5, 1.3, 1.8, 1.0, v2='i')
    def no(self, d=.9): return self.syl('o', d, 1.6, 1.1, 1.0, v2='u', shake=.03)
    def uhoh(self): return self._seq([self.syl('uh', .18, 1.3, 1.3, .9), self.syl('o', .35, 1.0, .9, .9)], [.05, 0])
    def hmm(self): return self.syl('u', .6, 1.0, 1.15, .6, breath=.2)
    def siu(self): return self._seq([_hp(self.rng.standard_normal(int(.18 * SR)), 3000) * .4, self.syl('i', .25, 1.3, 1.5, 1.0, v2='u'), self.syl('u', .6, 1.6, 1.4, 1.0)], [0, 0, 0])
    def grunt(self): return self.syl('uh', .25, .8, .7, 1.0, h=.03)
    def whistle(self, up=True): n = int(.5 * SR); t = np.arange(n) / SR; f = np.linspace(900, 2200, n) if up else np.linspace(2200, 900, n); return np.sin(2 * np.pi * np.cumsum(f) / SR) * _env(n, .05, .1) * .5


def crowd(kind='laugh', d=2.0, n=14, seed=0):
    rng = np.random.default_rng(seed); out = np.zeros(int((d + .6) * SR))
    for i in range(n):
        v = Voice(['generic_m', 'generic_f', 'big', 'kid'][i % 4], ep=seed, var=i)
        x = v.laugh(['belly', 'point', 'giggle', 'snicker'][i % 4], d * rng.uniform(.6, 1.0)) if kind == 'laugh' else v.yay() if kind == 'cheer' else v.gasp() if kind == 'gasp' else v.ow()
        o = int(rng.uniform(0, .4) * SR); m = min(len(x), len(out) - o); out[o:o + m] += x[:m] * rng.uniform(.3, .7)
    if kind == 'cheer': out += _bp(rng.standard_normal(len(out)), 300, 3000) * .15 * _env(len(out), .3, .8)
    return out / (np.abs(out).max() + 1e-9) * .9
