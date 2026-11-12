"""Original synthesized soundtrack for 'The GOATs Clock Out' (no third-party audio)."""
import sys, wave
import numpy as np
SR, T = 44100, 28
N = SR * T; out = np.zeros(N); rng = np.random.default_rng(5); tt = np.arange(N) / SR
def add(sig, t0, g=1.0):
    i = int(t0 * SR); n = min(len(sig), N - i); out[i:i + n] += g * sig[:n]
def env(n, a=.01, r=.05):
    e = np.ones(n); na, nr = max(1, int(a * SR)), max(1, int(r * SR)); e[:na] = np.linspace(0, 1, na); e[-nr:] *= np.linspace(1, 0, nr); return e
def band(sig, lo, hi):
    f = np.fft.rfftfreq(len(sig), 1 / SR); S = np.fft.rfft(sig)
    S *= np.exp(-((np.log(f + 1) - np.log((lo * hi) ** .5)) ** 2) / (2 * (np.log(hi / lo) / 2) ** 2)); return np.fft.irfft(S, len(sig))
def tone(f, d): return np.sin(2 * np.pi * np.cumsum(np.broadcast_to(f, int(d * SR))) / SR)
def drum(f0, d=.3):
    n = int(d * SR); t = np.arange(n) / SR; return np.sin(2 * np.pi * np.cumsum(f0 * np.exp(-t * 3)) / SR) * np.exp(-t * 10)
def snare(d=.12):
    n = int(d * SR); t = np.arange(n) / SR; return rng.standard_normal(n) * np.exp(-t * 30) * .6 + drum(220, d) * .4
def cym(d=1.0):
    n = int(d * SR); t = np.arange(n) / SR; c = band(rng.standard_normal(n), 5000, 12000); return c / np.abs(c).max() * np.exp(-t * 3.5)
def badum(t0): add(drum(200), t0, .6); add(drum(150), t0 + .2, .6); add(cym(), t0 + .42, .35)
def bell(f, d=.6):
    n = int(d * SR); t = np.arange(n) / SR; return sum(a * np.sin(2 * np.pi * f * m * t) for m, a in [(1, 1), (2.01, .5), (3.02, .25)]) * np.exp(-t * 5)
def clap():
    n = int(.08 * SR); t = np.arange(n) / SR; return band(rng.standard_normal(n), 800, 3000) * np.exp(-t * 60)
def boom(t0, g=1.0):   # deep impact on every punchline
    n = int(.7 * SR); t = np.arange(n) / SR
    add(np.sin(2 * np.pi * np.cumsum(90 * np.exp(-t * 2.5) + 30) / SR) * np.exp(-t * 4), t0, g); add(rng.standard_normal(int(.05 * SR)) * .5, t0, .3)
def scratch(t0):
    n = int(.35 * SR); t = np.arange(n) / SR
    add(band(rng.standard_normal(n), 800, 5000) * np.abs(np.sin(2 * np.pi * 9 * t)) * env(n, .01, .1), t0, .6)
crowd = band(rng.standard_normal(N), 250, 1800); crowd /= np.abs(crowd).max()
keys = [(0, 0), (3, .3), (8.8, 1.0), (10, .3), (21.5, 0), (24.3, .8), (28, .5)]
add(crowd * np.interp(tt, *zip(*keys)), 0, .28)
def groove(t0, t1, root):
    beat = .5; t = t0; i = 0
    while t < t1:
        if i % 2 == 0: add(drum(60, .25), t, .55)
        else: add(snare(), t, .18)
        n = int(.18 * SR); add(np.sin(2 * np.pi * root * [1, 1.5, 1.25, 1.5][i % 4] * np.arange(n) / SR) * env(n, .005, .08), t, .18)
        hn = int(.03 * SR); add(band(rng.standard_normal(hn), 6000, 12000) * env(hn, .001, .02), t + beat / 2, .08)
        t += beat; i += 1
# sad violin under the hook and the outro (original phrase)
def violin(t0):
    for f, d in [(392, .5), (370, .5), (349, .5), (330, 1.0)]:
        n = int(d * SR); t = np.arange(n) / SR; v = sum(a * np.sin(2 * np.pi * f * m * (t + .003 * np.sin(2 * np.pi * 5.5 * t))) for m, a in [(1, 1), (2, .5), (3, .3), (4, .15)])
        add(v * env(n, .06, .15), t0, .12); t0 += d
violin(0.1); violin(21.6)
n = int(2.4 * SR); add(band(rng.standard_normal(n), 2000, 8000) * env(n, .2, .3), 0, .08)
scratch(0.3); boom(0.35, .8)
# rewind whoosh
n = int(.6 * SR); add(tone(np.linspace(1800, 300, n), .6) * env(n, .02, .1), 2.4, .15); add(band(rng.standard_normal(n), 1000, 6000) * env(n, .05, .2), 2.4, .25)
groove(3.0, 21.5, 110); groove(24.3, 27.5, 130)
for p in [4.41, 5.37, 8.83, 12.64, 15.69, 16.23, 19.04, 21.9]: boom(p, .9)
badum(6.0)
add(drum(120, .2), 7.0 + 1.0 / 1.2, 1.0); siu = tone(np.linspace(180, 360, int(.9 * SR)), .9) * env(int(.9 * SR), .02, .3); add(siu, 8.83, .3)
for k in range(5): add(clap(), 9.6 + k * .4, .7)
for k in range(9): add(drum(70, .1), 11.8 + k * .3, .35)
add(bell(2093), 12.64, .4); add(bell(2637), 12.76, .35)
add(bell(1568), 15.69, .5); add(bell(2093), 15.79, .5); add(bell(2637), 15.89, .4)
n = int(1.0 * SR); add(band(rng.standard_normal(n), 400, 3000) * env(n, .1, .5), 15.6, .3); badum(17.2)
for t0 in (19.04, 19.25): n = int(.06 * SR); add(rng.standard_normal(n) * np.exp(-np.arange(n) / SR * 80), t0, .9)
badum(20.2)
for k in range(4): add(drum(300, .12), 24.7 + k * .785, .5)
out /= np.abs(out).max() * 1.1
with wave.open(sys.argv[1], 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.stack([out, out], 1) * 32767).astype('<i2').tobytes())
