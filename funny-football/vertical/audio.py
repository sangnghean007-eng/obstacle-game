"""Synthesized soundtrack for the vertical short (crowd, whistles, cartoon SFX)."""
import sys, wave
import numpy as np

SR, T = 44100, 42
N = SR * T
rng = np.random.default_rng(2)
out = np.zeros(N)
tt = np.arange(N) / SR

def add(sig, t0, gain=1.0):
    i = int(t0 * SR); n = min(len(sig), N - i)
    out[i:i + n] += gain * sig[:n]

def env(n, a=0.01, r=0.05):
    e = np.ones(n); na, nr = max(1, int(a * SR)), max(1, int(r * SR))
    e[:na] = np.linspace(0, 1, na); e[-nr:] *= np.linspace(1, 0, nr); return e

def band(sig, lo, hi):
    f = np.fft.rfftfreq(len(sig), 1 / SR); S = np.fft.rfft(sig)
    S *= np.exp(-((np.log(f + 1) - np.log((lo * hi) ** .5)) ** 2) / (2 * (np.log(hi / lo) / 2) ** 2))
    return np.fft.irfft(S, len(sig))

def tone(freqs, dur): return np.sin(2 * np.pi * np.cumsum(freqs) / SR)

crowd = band(rng.standard_normal(N), 250, 1800); crowd /= np.abs(crowd).max()
keys = [(0, .5), (2.2, 1.0), (3.5, .45), (8, .4), (10, .95), (14.6, .8), (17, .25), (21.4, .7), (22.5, .3), (26, .6), (31, .9), (36.5, .3), (39.8, 1.0), (42, .3)]
add(crowd * np.interp(tt, *zip(*keys)) * (0.85 + 0.15 * np.sin(2 * np.pi * .7 * tt)), 0, .32)

def whistle(dur):
    n = int(dur * SR); t = np.arange(n) / SR; f = 2900 + 180 * np.sign(np.sin(2 * np.pi * 32 * t))
    return (tone(f, dur) + .3 * tone(2 * f, dur) + .15 * rng.standard_normal(n)) * env(n, .01, .04)

def slide(f0, f1, dur):
    n = int(dur * SR); t = np.arange(n) / SR; f = f0 * (f1 / f0) ** (t / dur) * (1 + .02 * np.sin(2 * np.pi * 6 * t))
    return (tone(f, dur) + .2 * tone(2 * f, dur)) * env(n, .02, .05)

def thud(f0=90, dur=.35):
    n = int(dur * SR); t = np.arange(n) / SR
    return np.sin(2 * np.pi * np.cumsum(f0 * np.exp(-t * 6)) / SR) * np.exp(-t * 9) + .4 * rng.standard_normal(n) * np.exp(-t * 40)

def bell(f, dur=1.2):
    n = int(dur * SR); t = np.arange(n) / SR
    return sum(a * np.sin(2 * np.pi * f * m * t) for m, a in [(1, 1), (2.01, .5), (3.02, .25)]) * np.exp(-t * 3)

def pop(f=600):
    n = int(.12 * SR); t = np.arange(n) / SR
    return np.sin(2 * np.pi * np.cumsum(f * (1 + 3 * np.exp(-t * 40))) / SR) * np.exp(-t * 30)

def scream(dur, base=380):
    n = int(dur * SR); t = np.arange(n) / SR
    f0 = (base + 160 * t / dur) * (1 + .05 * np.sin(2 * np.pi * 7 * t)); ph = 2 * np.pi * np.cumsum(f0) / SR; s = np.zeros(n)
    for k in range(1, 18):
        fk = k * f0.mean(); s += (np.exp(-((fk - 800) / 260) ** 2) + .6 * np.exp(-((fk - 1200) / 320) ** 2) + .15 / k) * np.sin(k * ph)
    return s / np.abs(s).max() * env(n, .05, .2)

def boing(dur=.5, f0=200):
    n = int(dur * SR); t = np.arange(n) / SR
    return tone(f0 * (1 + .5 * np.sin(2 * np.pi * 14 * t) * np.exp(-t * 4)) * np.exp(-t * .8), dur) * np.exp(-t * 4)

def drum(f0, dur=.35):
    n = int(dur * SR); t = np.arange(n) / SR
    return np.sin(2 * np.pi * np.cumsum(f0 * np.exp(-t * 3)) / SR) * np.exp(-t * 10)

# S1 hook
add(slide(900, 1300, .6), 0.4, .08); add(whistle(.3), 2.0, .2)
add(scream(1.3), 2.15, .22); add(thud(), 2.35, .9)
# S2 hair
add(boing(.6, 260), 4.9, .4)
for t0 in (5.1, 5.8, 6.5): add(pop(700), t0, .5)
for i in range(12): add(bell(2500 + 300 * (i % 4), .3), 5.9 + i * .1, .05)
add(slide(300, 1200, .5), 7.1, .15)
# S3 Mexico: step, roll, scream, peek
add(thud(140, .25), 9.8, 1.0); add(slide(1800, 2600, .15), 9.82, .15)
add(scream(4.2, 420), 10.3, .25)
for t0 in np.arange(10.0, 14.6, .1): add(thud(70 + rng.random() * 30, .12), t0, .25)
add(bell(1760, .8), 15.2, .2); add(whistle(.4), 16.2, .15)
# S4 stopwatch
for i, t0 in enumerate(np.arange(17.0, 21.4, .5)):
    n = int(.03 * SR); t = np.arange(n) / SR; add(np.sin(2 * np.pi * (1300 if i % 2 else 900) * t) * np.exp(-t * 150), t0, .4)
for t0 in (17.8, 18.6, 19.4, 20.2): add(bell(1320, .6), t0, .2)
add(drum(90, 1.0), 21.4, .8); add(bell(660, 2.0), 21.4, .3)
for i in range(4): add(pop(500 + i * 120), 23.2 + i * .35, .5)
# S5 fouls: boing on each jump + boot whooshes
for t0 in np.arange(26.2, 31, 0.449): add(boing(.35, 230), t0, .25)
for t0 in np.arange(26.6, 31, .55):
    n = int(.3 * SR); w = band(rng.standard_normal(n), 800, 4000); add(w / np.abs(w).max() * env(n, .1, .15), t0, .12)
# S6 meme: slide whistles for rollers
for i, t0 in enumerate((31.0, 31.6, 32.1, 32.6, 33.4, 34.0)): add(slide(500, 1500, .8) if i % 2 == 0 else slide(1500, 500, .8), t0, .12)
# S7 ending: fall + ba-dum-tss
add(scream(1.0), 39.65, .2); add(thud(), 39.95, .9)
n = int(1.2 * SR); t = np.arange(n) / SR; cym = band(rng.standard_normal(n), 5000, 12000); cym = cym / np.abs(cym).max() * np.exp(-t * 3.5)
add(drum(200), 40.9, .6); add(drum(150), 41.12, .6); add(cym, 41.33, .35)

out /= np.abs(out).max() * 1.1
with wave.open(sys.argv[1], 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.stack([out, out], 1) * 32767).astype('<i2').tobytes())
