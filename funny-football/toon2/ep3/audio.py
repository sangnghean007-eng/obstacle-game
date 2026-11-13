"""Original synthesized soundtrack for Episode 2 (no third-party audio)."""
import sys, wave, numpy as np
SR, T = 44100, 22.5
OFF = 0.0; N = int(SR * T); out = np.zeros(N); rng = np.random.default_rng(7); tt = np.arange(N) / SR
def add(s, t0, g=1.0, raw=False):
    i = int((t0 if raw else t0 + OFF) * SR); n = min(len(s), N - i); out[i:i + n] += g * s[:n]
def env(n, a=.01, r=.05):
    e = np.ones(n); na, nr = max(1, int(a * SR)), max(1, int(r * SR)); e[:na] = np.linspace(0, 1, na); e[-nr:] *= np.linspace(1, 0, nr); return e
def band(s, lo, hi):
    f = np.fft.rfftfreq(len(s), 1 / SR); S = np.fft.rfft(s); S *= np.exp(-((np.log(f + 1) - np.log((lo * hi) ** .5)) ** 2) / (2 * (np.log(hi / lo) / 2) ** 2)); return np.fft.irfft(S, len(s))
def tone(f, d): return np.sin(2 * np.pi * np.cumsum(np.broadcast_to(f, int(d * SR))) / SR)
def drum(f0, d=.3):
    n = int(d * SR); t = np.arange(n) / SR; return np.sin(2 * np.pi * np.cumsum(f0 * np.exp(-t * 3)) / SR) * np.exp(-t * 10)
def bell(f, d=.5):
    n = int(d * SR); t = np.arange(n) / SR; return sum(a * np.sin(2 * np.pi * f * m * t) for m, a in [(1, 1), (2.01, .5), (3.02, .25)]) * np.exp(-t * 6)
def boom(t0, g=.9):
    n = int(.7 * SR); t = np.arange(n) / SR; add(np.sin(2 * np.pi * np.cumsum(90 * np.exp(-t * 2.5) + 30) / SR) * np.exp(-t * 4), t0, g)
def notif(t0): add(bell(1568, .25), t0, .35); add(bell(2093, .3), t0 + .09, .3)
def whoosh(t0, d=.4):
    n = int(d * SR); add(band(rng.standard_normal(n), 800, 5000) * env(n, d * .25, d * .4), t0, .3)
_unused = None
crowd = band(rng.standard_normal(N), 250, 1800); crowd /= np.abs(crowd).max()
keys = [(0, .5), (2.6, 0), (5.2, .4), (8.6, 0), (9.6, .5), (10.9, 1.0), (11.5, .5), (13.7, 1.0), (14.3, .5), (18.6, .9), (22, .5)]
add(crowd * np.interp(tt, *zip(*keys)), 0, .28)
beat = .5; t = 0; i = 0
while t < 22:
    if not (2.6 <= t < 5.2):
        if i % 2 == 0: add(drum(60, .25), t, .5)
        n = int(.18 * SR); add(np.sin(2 * np.pi * 110 * [1, 1.5, 1.25, 1.5][i % 4] * np.arange(n) / SR) * env(n, .005, .08), t, .16)
    t += beat; i += 1
import os
def V(name):
    w = wave.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sfx', name + '.wav')); return np.frombuffer(w.readframes(w.getnframes()), '<i2').astype(np.float32) / 32768
def notif(t0): add(bell(1568, .25), t0, .35, True); add(bell(2093, .3), t0 + .09, .3, True)
def whoosh(t0, d=.4):
    n = int(d * SR); add(band(rng.standard_normal(n), 800, 5000) * env(n, d * .25, d * .4), t0, .3, True)
def boom(t0, g=.9):
    n = int(.7 * SR); t = np.arange(n) / SR; add(np.sin(2 * np.pi * np.cumsum(90 * np.exp(-t * 2.5) + 30) / SR) * np.exp(-t * 4), t0, g, True)
# beach bed: waves + ukulele-ish plucks (original)
n = N; w = band(rng.standard_normal(n), 200, 1200); w /= np.abs(w).max(); add(w * (0.5 + 0.5 * np.sin(2 * np.pi * 0.25 * tt)) * 0.12, 0, 1, True)
mel = [392, 494, 587, 494, 440, 523, 659, 523]
t = 0.0; i = 0
while t < 21.0:
    if not (11.0 <= t < 13.6):
        f = mel[i % 8]; m = int(.25 * SR); tt2 = np.arange(m) / SR; add(np.sin(2 * np.pi * f * tt2) * np.exp(-tt2 * 12) + .3 * np.sin(4 * np.pi * f * tt2) * np.exp(-tt2 * 18), t, .18, True)
        if i % 2 == 0: add(drum(60, .25), t, .4, True)
    t += .25; i += 1
# events
boom(0.0); add(V('laugh_m'), 0.3, .4, True); whoosh(0.2, .8); add(drum(70, .3), 1.1, .9, True)       # cold open: boot falling
add(V('grumble_sad'), 2.2, .45, True); add(bell(784, .8), 3.0, .3, True)                              # bye national team, shades
for k in [0.5, 1.4, 2.0, 2.4, 2.7, 2.9, 3.05, 3.2, 3.3]: add(drum(130, .12), 4.0 + k, .7, True); add(bell(2093, .15), 4.35 + k, .2, True)
add(V('cheer_crowd'), 4.9, .5, True); add(V('cheer_crowd'), 7.3, .55, True)
add(drum(300, .15), 8.55, 1.0, True); boom(8.55); add(V('gasp'), 8.65, .7, True); add(V('laugh_crowd'), 9.2, .5, True)   # BONK
add(V('cheer_crowd'), 9.6, .4, True)
add(tone(np.linspace(300, 260, int(.6 * SR)), .6) * env(int(.6 * SR), .02, .3), 11.1, .15, True)                     # Ronaldo desert
boom(12.0); add(V('grumble_angry'), 12.1, .75, True)
add(V('siu'), 13.6, .9, True); whoosh(13.6, .9); add(drum(300, .12), 14.5, .9, True); add(V('gasp'), 14.55, .6, True); add(V('laugh_crowd'), 14.9, .45, True)
add(drum(500, .08), 15.9, .6, True); add(V('chuckle'), 16.2, .5, True); add(drum(200), 17.0, .5, True); add(drum(150), 17.2, .5, True)
add(drum(300, .1), 21.05, .6, True); add(drum(500, .08), 21.55, .8, True); add(bell(1568, .6), 21.6, .5, True); add(bell(2093, .6), 21.7, .4, True); add(V('follow'), 21.65, .9, True)
out /= np.abs(out).max() * 1.1
with wave.open(sys.argv[1], 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.stack([out, out], 1) * 32767).astype('<i2').tobytes())
