"""Small original sound-design kit for the toon2 shorts (all sounds synthesized here, no samples).

Usage:  from synth import Mix;  m = Mix(T);  m.kick(1.0); ...;  m.write(path)
Everything is stereo. `m.music` holds the music bed, `m.fx` effects, `m.vox` voices;
write() ducks music under voices, adds reverb and normalizes.
"""
import os, wave, numpy as np
from scipy.signal import butter, sosfilt, fftconvolve

SR = 44100
HERE = os.path.dirname(os.path.abspath(__file__))
_rng = np.random.default_rng(3)


def T(d): return np.arange(int(d * SR)) / SR
def noise(d): return _rng.standard_normal(int(d * SR))
def env(n, a=.005, r=.1, shape=1.0):
    e = np.ones(n); na, nr = max(1, min(n, int(a * SR))), max(1, min(n, int(r * SR)))
    e[:na] = np.linspace(0, 1, na); e[-nr:] *= np.linspace(1, 0, nr) ** shape; return e
def dec(d, k): t = T(d); return np.exp(-t * k)
def bp(x, lo, hi, o=2): return sosfilt(butter(o, [lo, hi], 'band', fs=SR, output='sos'), x)
def lp(x, f, o=2): return sosfilt(butter(o, f, 'low', fs=SR, output='sos'), x)
def hp(x, f, o=2): return sosfilt(butter(o, f, 'high', fs=SR, output='sos'), x)
def osc(f, d, kind='sin'):
    f = np.broadcast_to(np.asarray(f, float), (int(d * SR),)); ph = np.cumsum(f) / SR
    if kind == 'sin': return np.sin(2 * np.pi * ph)
    if kind == 'saw': return 2 * (ph % 1) - 1
    if kind == 'sq': return np.sign(np.sin(2 * np.pi * ph))
    if kind == 'tri': return 2 * np.abs(2 * (ph % 1) - 1) - 1
def glide(f0, f1, d, curve=1.0): return f0 + (f1 - f0) * np.linspace(0, 1, int(d * SR)) ** curve
NOTE = {n: i for i, n in enumerate(['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'])}
def hz(name):  # 'C4', 'F#3'
    n, o = name[:-1], int(name[-1]); return 440 * 2 ** ((NOTE[n] + 12 * (o + 1) - 69) / 12)


class Mix:
    def __init__(self, dur):
        self.N = int(dur * SR); self.dur = dur
        self.music = np.zeros((self.N, 2)); self.fx = np.zeros((self.N, 2)); self.vox = np.zeros((self.N, 2)); self.wet = np.zeros((self.N, 2))

    # ---------- placing ----------
    def put(self, bus, s, t0, g=1.0, pan=0.0, rev=0.0):
        i = int(t0 * SR)
        if i >= self.N or len(s) == 0: return
        if i < 0: s = s[-i:]; i = 0
        n = min(len(s), self.N - i); L, R = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
        x = s[:n] * g; bus[i:i + n, 0] += x * L * 1.414; bus[i:i + n, 1] += x * R * 1.414
        if rev: self.wet[i:i + n, 0] += x * rev; self.wet[i:i + n, 1] += x * rev
    def m(self, s, t0, g=1, pan=0, rev=.15): self.put(self.music, s, t0, g, pan, rev)
    def f(self, s, t0, g=1, pan=0, rev=.1): self.put(self.fx, s, t0, g, pan, rev)
    def wav(self, name):
        w = wave.open(os.path.join(HERE, name + '.wav')); x = np.frombuffer(w.readframes(w.getnframes()), '<i2').astype(np.float32) / 32768
        if w.getnchannels() == 2: x = x.reshape(-1, 2).mean(1)
        return x
    def say(self, name, t0, g=1.0, pan=0.0, rev=.06):
        x = self.wav('lines/' + name if os.path.exists(os.path.join(HERE, 'lines', name + '.wav')) else name)
        self.put(self.vox, x, t0, g, pan, rev); return t0 + len(x) / SR

    # ---------- drums ----------
    def kick(self, t, g=1.0):
        d = .35; f = 45 + 110 * dec(d, 30); self.m(np.sin(2 * np.pi * np.cumsum(f) / SR) * dec(d, 9) + .3 * lp(noise(d), 2000) * dec(d, 80), t, g, 0, .02)
    def snare(self, t, g=.6, pan=0):
        d = .25; self.m(bp(noise(d), 1500, 7000) * dec(d, 18) + .5 * osc(190, d) * dec(d, 25), t, g, pan, .25)
    def clap(self, t, g=.5):
        d = .3; e = np.zeros(int(d * SR))
        for k in (0, .01, .02): i0 = int(k * SR); e[i0:] += np.exp(-np.arange(len(e) - i0) / SR * 30)
        self.m(bp(noise(d), 900, 4000) * e, t, g, 0, .35)
    def hat(self, t, g=.18, open_=False, pan=.3):
        d = .25 if open_ else .05; self.m(hp(noise(d), 7000) * dec(d, 12 if open_ else 80), t, g, pan, .05)
    def rim(self, t, g=.35): d = .08; self.m(bp(noise(d), 1500, 3500) * dec(d, 60) + osc(1700, d) * dec(d, 90) * .5, t, g, -.2, .2)
    def crash(self, t, g=.35): d = 1.6; self.m(hp(noise(d), 4000) * dec(d, 2.5), t, g, .2, .3)

    # ---------- instruments ----------
    def pluck(self, f, t, d=.35, g=.25, pan=0, bright=1.0, rev=.2):  # steel-drum / marimba-ish
        x = osc(f, d) + .45 * osc(f * 2.0, d) * dec(d, 14) + .25 * bright * osc(f * 3.01, d) * dec(d, 22)
        self.m(x * dec(d, 9) * env(len(x), .002, .05), t, g, pan, rev)
    def organ_stab(self, fs, t, d=.16, g=.12, pan=-.2):
        x = sum(osc(f, d, 'sq') * .5 + osc(f * 2, d) * .3 for f in fs); self.m(lp(x, 2500) * env(len(x), .004, .06), t, g, pan, .2)
    def bass(self, f, t, d=.4, g=.35):
        x = osc(f, d) + .3 * osc(f * 2, d, 'tri'); self.m(lp(x, 600) * env(len(x), .01, .08), t, g, 0, 0)
    def saw_chord(self, fs, t, d, g=.12, cut=1800, pan=0, a=.01, r=.2, rev=.3):
        x = sum(osc(f * (1 + det), d, 'saw') for f in fs for det in (-.004, 0, .005)); x = lp(x, cut) * env(len(x), a, r); self.m(x, t, g, pan, rev)
    def brass_hit(self, fs, t, d=.6, g=.2):
        x = sum(osc(f * (1 + det), d, 'saw') for f in fs for det in (-.006, .006)); fe = 600 + 3000 * dec(d, 6)
        y = np.zeros_like(x); chunk = 512  # time-varying low-pass
        for i in range(0, len(x), chunk): y[i:i + chunk] = lp(x[max(0, i - 2048):i + chunk], float(fe[i]))[-len(x[i:i + chunk]):]
        self.m(y * env(len(y), .01, .25) * dec(d, 1.5), t, g, 0, .4)
    def choir(self, fs, t, d, g=.16):
        x = sum(osc(f * (1 + .003 * np.sin(2 * np.pi * (5 + k) * T(d))), d, 'saw') for k, f in enumerate(fs))
        y = bp(x, 500, 900) * .8 + bp(x, 1000, 1400) * .5 + bp(x, 2400, 3000) * .2
        self.m(y * env(len(y), .4, .6), t, g, 0, .6)
    def harp_gliss(self, t, notes, step=.05, g=.18):
        for i, n in enumerate(notes): self.pluck(hz(n), t + i * step, .8, g, -.6 + 1.2 * i / len(notes), .6, .4)
    def music_box(self, t, notes, step=.25, g=.16):
        for i, n in enumerate(notes):
            if n: f = hz(n); d = .9; x = (osc(f, d) + .3 * osc(f * 4.02, d) * dec(d, 6)) * dec(d, 4); self.m(x, t + i * step, g, .2 * np.sin(i), .45)
    def drone(self, f, t, d, g=.12):
        x = osc(f, d, 'saw') + osc(f * 1.01, d, 'saw') + .5 * osc(f / 2, d); self.m(lp(x, 400) * env(len(x), .3, .4), t, g, 0, .3)

    # ---------- foley ----------
    def whoosh(self, t, d=.4, g=.35, up=True, pan=0):
        x = noise(d); n = len(x); y = np.zeros(n); seg = n // 8
        for k in range(8):
            c = (k + .5) / 8; f = 500 + 3500 * (c if up else 1 - c); y[k * seg:(k + 1) * seg] = bp(x[k * seg:(k + 1) * seg], f * .7, f * 1.3)
        self.f(y * np.sin(np.linspace(0, np.pi, n)) ** 1.5, t, g, pan, .1)
    def thwack(self, t, g=.8, pan=0):  # ball kick
        d = .18; self.f(bp(noise(d), 800, 3500) * dec(d, 45) + osc(glide(180, 80, d), d) * dec(d, 25), t, g, pan, .1)
    def net(self, t, g=.5, pan=.3):
        d = .5; x = bp(noise(d), 2500, 8000) * env(int(d * SR), .02, .3) * (0.6 + .4 * np.sin(2 * np.pi * 30 * T(d))); self.f(x, t, g, pan, .2)
    def thud(self, t, g=.6, pan=0): d = .3; self.f(lp(noise(d), 300) * dec(d, 15) + osc(glide(90, 50, d), d) * dec(d, 12), t, g, pan, .05)
    def bonk(self, t, g=.8, pan=0):
        d = .45; self.f(osc(glide(520, 260, d, .4), d) * dec(d, 9), t, g, pan, .15)
        self.f(bp(noise(.06), 1200, 5000) * dec(.06, 70), t, g * .7, pan, .1)
    def boing(self, t, g=.4, d=.5, f0=180, f1=420, pan=0):
        tt = T(d); f = glide(f0, f1, d, .5) * (1 + .08 * np.sin(2 * np.pi * 22 * tt)); self.f(osc(f, d) * dec(d, 4) * env(len(tt), .003, .1), t, g, pan, .1)
    def pop(self, t, g=.4, f=900, pan=0): d = .06; self.f(osc(glide(f * 1.5, f * .5, d), d) * dec(d, 50), t, g, pan, .1)
    def snore(self, t, d=1.6, g=.35, pan=-.2):
        tt = T(d); x = lp(noise(d), 500) * (.5 + .5 * np.sin(2 * np.pi * 60 * tt)) + .4 * osc(70 + 10 * np.sin(2 * np.pi * 3 * tt), d, 'saw')
        e = np.clip(np.sin(np.pi * tt / (d * .6)), 0, 1) ** 2; e[tt > d * .6] = 0; wh = hp(noise(d), 2000) * np.clip(np.sin(np.pi * (tt - d * .62) / (d * .35)), 0, 1) * .25
        self.f(lp(x, 900) * e + wh, t, g, pan, .05)
    def slurp(self, t, d=.8, g=.35, pan=-.1):
        x = noise(d); n = len(x); y = np.zeros(n); seg = n // 10
        for k in range(10): f = 600 + 1600 * k / 10; y[k * seg:(k + 1) * seg] = bp(x[k * seg:(k + 1) * seg], f, f * 1.5)
        self.f(y * (.5 + .5 * np.sign(np.sin(2 * np.pi * 14 * T(d)))) * env(n, .02, .1), t, g, pan, .05)
    def tweet(self, t, n=4, g=.18, pan=.3):
        for i in range(n): d = .12; self.f(osc(glide(2600, 3400, d) + 300 * np.sin(2 * np.pi * 40 * T(d)), d) * env(int(d * SR), .005, .05), t + i * .16, g, pan * (1 if i % 2 else -1), .2)
    def seagull(self, t, g=.15, pan=.5):
        for i in range(2): d = .3; f = glide(1700, 1000, d); x = osc(f, d, 'saw') * .4 + osc(f, d); self.f(bp(x, 800, 3000) * env(int(d * SR), .02, .15), t + i * .35, g, pan, .3)
    def crowd(self, t, d, g=.35, swell=True):
        x = bp(noise(d), 300, 2500) + .5 * bp(noise(d), 2500, 5000); n = len(x)
        e = np.sin(np.linspace(0, np.pi, n)) ** .6 if swell else env(n, .2, .5); self.f(x * e, t, g, 0, .3)
    def cheer_burst(self, t, g=.4): self.crowd(t, 1.8, g); self.f(self.wav('cheer_crowd'), t + .05, g * .9, 0, .2)
    def scratch(self, t, g=.5):
        d = .35; tt = T(d); f = 800 + 700 * np.sin(2 * np.pi * 6 * tt); x = noise(d); y = np.zeros_like(x); seg = len(x) // 14
        for k in range(14): c = f[k * seg]; y[k * seg:(k + 1) * seg] = bp(x[k * seg:(k + 1) * seg], c * .6, c * 1.6)
        self.f(y * env(len(y), .005, .05), t, g, 0, .05)
    def tape_rewind(self, t, d=.4, g=.3):
        tt = T(d); x = osc(glide(300, 1800, d), d, 'saw') * .3 + bp(noise(d), 2000, 6000) * .5; self.f(x * env(len(x), .01, .1), t, g, 0, .05)
    def tick(self, t, hi=True, g=.3): d = .05; self.f(bp(noise(d), 2500 if hi else 1600, 5000 if hi else 3000) * dec(d, 90) + osc(1800 if hi else 1300, d) * dec(d, 120), t, g, .4 if hi else -.4, .1)
    def kettle(self, t, d=.8, g=.15):
        tt = T(d); x = osc(2600 + 40 * np.sin(2 * np.pi * 7 * tt), d) * (.6 + .4 * np.sin(2 * np.pi * 13 * tt)) + .3 * bp(noise(d), 3000, 6000); self.f(x * env(len(x), .15, .2), t, g, .3, .2)
    def firework(self, t, g=.35, pan=0):
        self.f(lp(noise(.4), 800) * dec(.4, 10), t, g, pan, .4)
        R = np.random.default_rng(int(t * 100))
        for k in range(10): self.pop(t + .08 + R.random() * .5, g * .35, 1500 + R.random() * 2000, pan + R.uniform(-.4, .4))
    def ding(self, t, f=1568, g=.3, pan=0): d = .9; x = sum(a * osc(f * m, d) for m, a in [(1, 1), (2.76, .4), (5.4, .2)]) * dec(d, 5); self.f(x, t, g, pan, .4)
    def sparkle(self, t, d=.8, g=.12):
        R = np.random.default_rng(int(t * 33))
        for k in range(int(d * 14)): self.ding(t + k / 14, 2000 + R.random() * 2500, g * .5, R.uniform(-.7, .7))
    def footstep(self, t, g=.3, pan=0): d = .1; self.f(lp(noise(d), 900) * dec(d, 40), t, g, pan, .05)
    def heartbeat(self, t, g=.5):
        for k in (0, .22): d = .25; self.f(osc(glide(70, 40, d), d) * dec(d, 14), t + k, g * (1 if k == 0 else .7), 0, .05)
    def slowdown(self, t, d=.8, g=.4):  # "time slows" swoop
        tt = T(d); self.f(lp(osc(glide(800, 60, d, .5), d, 'saw'), 1200) * env(len(tt), .02, .3) + .5 * lp(noise(d), glide(3000, 200, d)[0]) * dec(d, 3), t, g, 0, .5)
    def badumtss(self, t, g=.5): self.snare(t, g * .8); self.snare(t + .14, g * .8); self.kick(t + .28, g * .6); self.crash(t + .28, g * .5)

    # ---------- render ----------
    def write(self, path, duck=.6, rev_time=1.4):
        v = self.vox; e = np.convolve(np.abs(v).mean(1), np.ones(int(.06 * SR)) / int(.06 * SR), 'same')
        e = np.clip(e / (np.percentile(e[e > 0], 90) + 1e-9) * 1.5, 0, 1) if (e > 0).any() else e
        e = np.convolve(e, np.ones(int(.15 * SR)) / int(.15 * SR), 'same')
        bed = self.music * (1 - duck * e)[:, None] + self.fx * (1 - .35 * duck * e)[:, None]
        n = int(rev_time * SR); ir = _rng.standard_normal((n, 2)) * np.exp(-np.arange(n) / SR * 4.5)[:, None]; ir[:int(.012 * SR)] = 0
        wet = np.stack([fftconvolve(self.wet[:, c], ir[:, c])[:self.N] for c in (0, 1)], 1); wet = lp(wet.T, 5000).T
        wet *= .25 / (np.abs(wet).max() + 1e-9) * max(np.abs(bed).max(), 1e-9)
        out = bed + wet
        out = out / (np.abs(out).max() + 1e-9) * .55 + v / (np.abs(v).max() + 1e-9) * .5
        out = np.tanh(out * 1.3) / np.tanh(1.3)  # soft clip / glue
        out /= np.abs(out).max() * 1.02
        with wave.open(path, 'wb') as w:
            w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out * 32767).astype('<i2').tobytes())
