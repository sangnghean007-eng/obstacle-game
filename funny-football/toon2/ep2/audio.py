"""Original synthesized soundtrack for Episode 2 (no third-party audio)."""
import sys, wave, numpy as np
SR, T = 44100, 22; N = SR * T; out = np.zeros(N); rng = np.random.default_rng(7); tt = np.arange(N) / SR
def add(s, t0, g=1.0):
    i = int(t0 * SR); n = min(len(s), N - i); out[i:i + n] += g * s[:n]
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
out /= np.abs(out).max() * 1.1
with wave.open(sys.argv[1], 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.stack([out, out], 1) * 32767).astype('<i2').tobytes())
