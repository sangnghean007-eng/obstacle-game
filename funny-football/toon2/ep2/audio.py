"""Original synthesized soundtrack for Episode 2 (no third-party audio)."""
import sys, wave, numpy as np
SR, T = 44100, 23.3
OFF = 1.3; N = int(SR * T); out = np.zeros(N); rng = np.random.default_rng(7); tt = np.arange(N) / SR
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
notif(0.5); boom(0.3, .6)
for k in range(3): add(tone(np.linspace(300, 260, int(.4 * SR)), .4) * env(int(.4 * SR), .02, .2), 2.7 + k * .4, .15)
boom(3.7); whoosh(4.0, .5); add(drum(300, .1), 4.4, .5)
notif(5.4); for_k = None
for k in range(10): add(np.sin(2 * np.pi * 1800 * np.arange(int(.02 * SR)) / SR), 5.25 + k * .09, .15)
whoosh(6.3, .3); add(drum(70, .4), 6.65, 1.0); boom(6.65, .8)
n = int(.6 * SR); add(band(rng.standard_normal(n), 300, 1500) * env(n, .1, .3), 7.6, .6)
for k in range(6): whoosh(8.62 + k * .13, .12)
for kt in (10.5, 13.3):
    for j in range(6): add(drum(80, .08), kt - .9 + j * .13, .4)
    add(drum(130, .2), kt, 1.0); boom(kt + .35, .9); add(tone(np.linspace(180, 360, int(.8 * SR)), .8) * env(int(.8 * SR), .02, .3), kt + .4, .28)
add(drum(130, .2), 12.0, .8); boom(12.2, .6)
add(tone(np.linspace(400, 200, int(.8 * SR)), .8) * env(int(.8 * SR), .02, .3), 14.1, .2)
notif(15.6); whoosh(15.5, 1.0); add(drum(60, .4), 16.5, 1.0); boom(16.5, .9)
for k in range(10): add(drum(250 + (k % 2) * 60, .08), 16.9 + k * .17, .35)
add(drum(200), 19.0, .6); add(drum(150), 19.2, .6)
n = int(1.0 * SR); c = band(rng.standard_normal(n), 5000, 12000); add(c / np.abs(c).max() * np.exp(-np.arange(n) / SR * 3.5), 19.4, .35)
# ---- voice SFX (synthesized with espeak-ng, see ../sfx/make_voices.py) ----
import os
def V(name):
    w = wave.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sfx', name + '.wav')); return np.frombuffer(w.readframes(w.getnframes()), '<i2').astype(np.float32) / 32768
add(V('cheer_crowd'), 0.2, .45); add(V('chuckle'), 1.3, .5)                     # hook: Barca fans + smug chuckle
add(V('gasp'), 3.65, .8); add(V('grumble_angry'), 3.9, .75)                     # Ronaldo at home: "0-2?!" + gibberish rant
add(V('chuckle'), 5.8, .5); add(V('ooh_crowd'), 7.6, .7); add(V('laugh_m'), 8.0, .45)   # Juve reply
add(V('cheer_crowd'), 10.85, .6); add(V('siu'), 10.95, .9)                       # penalty 1
add(V('cheer_crowd'), 12.2, .5)                                                   # McKennie
add(V('cheer_crowd'), 13.65, .6); add(V('siu_crowd'), 13.75, .8)                 # penalty 2
add(V('gasp'), 14.15, .7); add(V('grumble_sad'), 14.4, .6)                       # Messi reaction
add(V('bleat'), 16.75, .8); add(V('wail'), 17.0, .6); add(V('laugh_crowd'), 17.3, .55); add(V('bleat'), 18.0, .6)   # goat chase
add(V('siu_crowd'), 18.8, .7); add(V('laugh_crowd'), 20.2, .45); add(V('siu'), 20.6, .6)   # outro
# cold-open hook sounds (absolute times)
add(drum(70, .4), 0.0, 1.0, raw=True); boom(-OFF + 0.0, 1.0); add(V('siu_crowd'), 0.05, .7, raw=True); add(V('grumble_angry')[:int(.9 * SR)], 0.25, .6, raw=True)
add(drum(300, .12), 0.4, .7, raw=True); add(drum(300, .12), 0.8, .7, raw=True)
n = int(.3 * SR); add(band(rng.standard_normal(n), 800, 5000) * np.abs(np.sin(2 * np.pi * 9 * np.arange(n) / SR)), 1.15, .5, raw=True)
out /= np.abs(out).max() * 1.1
with wave.open(sys.argv[1], 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.stack([out, out], 1) * 32767).astype('<i2').tobytes())
