"""Original synthesized soundtrack for 'The GOATs Clock Out' (no third-party audio)."""
import sys, wave
import numpy as np
SR, T = 44100, 36
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
# crowd bed
crowd = band(rng.standard_normal(N), 250, 1800); crowd /= np.abs(crowd).max()
keys = [(0, .5), (3.5, .25), (9, .5), (10.4, 1.0), (12, .25), (14.5, .35), (23.5, 0), (28, .3), (32, .9), (36, .4)]
add(crowd * np.interp(tt, *zip(*keys)), 0, .3)
# upbeat bass+hat groove (original) under scenes 1-5 and 8
def groove(t0, t1, root):
    bpm = 120; beat = 60 / bpm; t = t0; i = 0
    while t < t1:
        add(drum(60, .25), t, .55 if i % 2 == 0 else .0); add(snare(), t + beat / 2, .18 if i % 2 else .0)
        n = int(.18 * SR); add(np.sin(2 * np.pi * root * [1, 1.5, 1.25, 1.5][i % 4] * np.arange(n) / SR) * env(n, .005, .08), t, .18)
        hn = int(.03 * SR); add(band(rng.standard_normal(hn), 6000, 12000) * env(hn, .001, .02), t + beat / 2, .08)
        t += beat; i += 1
groove(0, 23.5, 110); groove(32, 36, 130)
# S1 drum roll + hit
for k in range(40): add(snare(.06), 0.1 + k * .03, .25 + k * .01)
add(cym(1.2), 1.35, .4)
# S2 stamps + ba-dum-tss
add(drum(90, .2), 3.5 + 1.9, .9); add(drum(90, .2), 3.5 + 3.2, .9); badum(3.5 + 3.9)
# S3 kick, net swish, SIU, slow claps
add(drum(120, .2), 9 + 1.0, 1.0); n = int(.4 * SR); add(band(rng.standard_normal(n), 1500, 6000) * env(n, .02, .3), 9 + 1.35, .4)
siu = tone(np.linspace(180, 360, int(.9 * SR)), .9) * env(int(.9 * SR), .02, .3); add(siu + .4 * tone(np.linspace(360, 720, int(.9 * SR)), .9) * env(int(.9 * SR), .02, .3), 9 + 2.2, .35)
for k in range(6): add(clap(), 9 + 2.9 + k * .45, .7)
# S4 footsteps + cash register
for k in range(12): add(drum(70, .1), 14.5 + .4 + k * .32, .35)
add(bell(2093), 14.5 + 1.6, .4); add(bell(2637), 14.5 + 1.72, .35)
# S5 ka-ching + whoosh of bills
add(bell(1568), 19.5 + .9, .5); add(bell(2093), 19.5 + 1.0, .5); add(bell(2637), 19.5 + 1.1, .4)
n = int(1.2 * SR); add(band(rng.standard_normal(n), 400, 3000) * env(n, .1, .6), 19.5 + .8, .3); badum(19.5 + 2.6)
# S6 sad violin (original melody) + rain
mel = [(392, .6), (370, .6), (349, .6), (330, 1.6)]; t0 = 23.6
for f, d in mel:
    n = int(d * SR); t = np.arange(n) / SR; v = sum(a * np.sin(2 * np.pi * f * m * (t + .003 * np.sin(2 * np.pi * 5.5 * t))) for m, a in [(1, 1), (2, .5), (3, .3), (4, .15)])
    add(v * env(n, .08, .2), t0, .12); t0 += d
n = int(4.4 * SR); add(band(rng.standard_normal(n), 2000, 8000) * env(n, .3, .5), 23.5, .08)
# S7 knee cracks + punchline
for k, t0 in enumerate([29.2, 29.45]): n = int(.06 * SR); add(rng.standard_normal(n) * np.exp(-np.arange(n) / SR * 80), t0, .9)
badum(30.0)
# S8 bonks
for k in range(8): add(drum(300, .12), 32.4 + k * .785, .5)
out /= np.abs(out).max() * 1.1
with wave.open(sys.argv[1], 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.stack([out, out], 1) * 32767).astype('<i2').tobytes())
