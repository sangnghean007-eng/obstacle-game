"""Tổng hợp âm thanh cho video: tiếng khán giả, còi, hiệu ứng hài (không dùng file ngoài)."""
import sys, wave
import numpy as np

SR, T = 44100, 34
N = SR * T
rng = np.random.default_rng(1)
out = np.zeros(N)
tt = np.arange(N) / SR

def add(sig, t0, gain=1.0):
    i = int(t0 * SR); n = min(len(sig), N - i)
    out[i:i + n] += gain * sig[:n]

def env(n, a=0.01, r=0.05):
    e = np.ones(n); na, nr = int(a * SR), int(r * SR)
    e[:na] = np.linspace(0, 1, na); e[-nr:] *= np.linspace(1, 0, nr); return e

def band(sig, lo, hi):
    f = np.fft.rfftfreq(len(sig), 1 / SR); S = np.fft.rfft(sig)
    S *= np.exp(-((np.log(f + 1) - np.log((lo * hi) ** .5)) ** 2) / (2 * (np.log(hi / lo) / 2) ** 2))
    return np.fft.irfft(S, len(sig))

def tone(freqs, dur):
    ph = 2 * np.pi * np.cumsum(freqs) / SR; return np.sin(ph)

# Tiếng khán giả
crowd = band(rng.standard_normal(N), 250, 1800); crowd /= np.abs(crowd).max()
keys = [(0, .55), (4, .45), (8, .5), (8.6, .9), (10.5, 1.0), (12.5, .6), (13.6, .08), (17.5, .08), (17.8, 1.0), (19.5, .7),
        (22, .6), (22.3, 1.0), (23.2, .35), (27, .8), (30.5, .5), (33, .3), (34, .1)]
cenv = np.interp(tt, [k[0] for k in keys], [k[1] for k in keys]) * (0.85 + 0.15 * np.sin(2 * np.pi * 0.7 * tt))
add(crowd * cenv, 0, 0.35)

def whistle(dur):
    n = int(dur * SR); t = np.arange(n) / SR
    f = 2900 + 180 * np.sign(np.sin(2 * np.pi * 32 * t))
    s = tone(f, dur) + 0.3 * tone(2 * f, dur) + 0.15 * rng.standard_normal(n)
    return s * env(n, .01, .04)

for t0, d in [(4.1, .35), (11.6, .5), (11.95, .5), (17.55, .25), (17.85, .25), (18.15, .7), (30.8, .3), (31.15, .3), (31.5, 1.0)]:
    add(whistle(d), t0, 0.22)

def slide(f0, f1, dur):
    n = int(dur * SR); t = np.arange(n) / SR
    f = f0 * (f1 / f0) ** (t / dur) * (1 + 0.02 * np.sin(2 * np.pi * 6 * t))
    return (tone(f, dur) + 0.2 * tone(2 * f, dur)) * env(n, .02, .05)

add(slide(400, 1600, 1.0), 8.2, .25); add(slide(1600, 300, 1.0), 9.2, .25)   # bay lộn vòng
add(slide(220, 55, 1.0), 7.0, .35)                                            # slow motion "wooom"

def thud(f0=90, dur=.35):
    n = int(dur * SR); t = np.arange(n) / SR
    s = np.sin(2 * np.pi * np.cumsum(f0 * np.exp(-t * 6)) / SR) * np.exp(-t * 9)
    return s + 0.4 * rng.standard_normal(n) * np.exp(-t * 40)

add(thud(), 10.2, .9); add(thud(120, .3), 22.0, 1.0); add(thud(70, .4), 22.5, .6)

def bell(f, dur=1.5):
    n = int(dur * SR); t = np.arange(n) / SR
    return sum(a * np.sin(2 * np.pi * f * m * t) for m, a in [(1, 1), (2.01, .5), (3.02, .25)]) * np.exp(-t * 3)

add(bell(1320), 10.65, .25); add(bell(1760), 10.85, .2)        # tượng Oscar
add(bell(990, 2.5), 25.4, .2); add(bell(1480, 2.5), 25.6, .15)  # vệ tinh

def scream(dur):
    n = int(dur * SR); t = np.arange(n) / SR
    f0 = (380 + 160 * t / dur) * (1 + 0.04 * np.sin(2 * np.pi * 7 * t))
    ph = 2 * np.pi * np.cumsum(f0) / SR; s = np.zeros(n)
    for k in range(1, 18):
        fk = k * f0.mean()
        a = np.exp(-((fk - 800) / 260) ** 2) + .6 * np.exp(-((fk - 1200) / 320) ** 2) + .15 / k
        s += a * np.sin(k * ph)
    return s / np.abs(s).max() * env(n, .05, .2)

add(scream(2.0), 8.2, .22)

for i, t0 in enumerate(np.arange(13.2, 17.5, .5)):                # tích tắc VAR
    n = int(.03 * SR); t = np.arange(n) / SR
    add(np.sin(2 * np.pi * (1300 if i % 2 else 900) * t) * np.exp(-t * 150), t0, .4)

n = int(3.4 * SR); t = np.arange(n) / SR                         # vút lên trời
wh = band(rng.standard_normal(n), 300, 3000) * env(n, .3, .6); wh /= np.abs(wh).max()
add(wh * (0.4 + 0.6 * t / 3.4) + 0.2 * slide(200, 900, 3.4), 22.0, .35)

def boing(dur=.6):
    n = int(dur * SR); t = np.arange(n) / SR
    f = 180 * (1 + 0.5 * np.sin(2 * np.pi * 14 * t) * np.exp(-t * 4)) * np.exp(-t * .8)
    return tone(f, dur) * np.exp(-t * 4)

add(boing(), 22.55, .45)

def drum(f0, dur=.35):
    n = int(dur * SR); t = np.arange(n) / SR
    return np.sin(2 * np.pi * np.cumsum(f0 * np.exp(-t * 3)) / SR) * np.exp(-t * 10)

n = int(1.2 * SR); t = np.arange(n) / SR                          # ba-dum-tss
cym = band(rng.standard_normal(n), 5000, 12000); cym = cym / np.abs(cym).max() * np.exp(-t * 3.5)
add(drum(200), 32.6, .6); add(drum(150), 32.85, .6); add(cym, 33.05, .35)

out /= np.abs(out).max() * 1.1
st = np.stack([out, out], 1)
with wave.open(sys.argv[1], 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((st * 32767).astype('<i2').tobytes())
