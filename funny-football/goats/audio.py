"""Original synthesized soundtrack for 'The GOATs Clock Out' (no third-party audio)."""
import sys, wave
import numpy as np
SR, T = 44100, 21
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
keys = [(0, 1.0), (0.7, 0), (5.0, .4), (6.1, 1.0), (7.8, .4), (15.8, 0), (18.8, .9), (21, .5)]
add(crowd * np.interp(tt, *zip(*keys)), 0, .28)
def groove(t0, t1, root):
    beat = .5; t = t0; i = 0
    while t < t1:
        if i % 2 == 0: add(drum(60, .25), t, .55)
        else: add(snare(), t, .18)
        n = int(.18 * SR); add(np.sin(2 * np.pi * root * [1, 1.5, 1.25, 1.5][i % 4] * np.arange(n) / SR) * env(n, .005, .08), t, .18)
        hn = int(.03 * SR); add(band(rng.standard_normal(hn), 6000, 12000) * env(hn, .001, .02), t + beat / 2, .08)
        t += beat; i += 1
def violin(t0, notes):
    for f, d in notes:
        n = int(d * SR); t = np.arange(n) / SR; v = sum(a * np.sin(2 * np.pi * f * m * (t + .003 * np.sin(2 * np.pi * 5.5 * t))) for m, a in [(1, 1), (2, .5), (3, .3), (4, .15)])
        add(v * env(n, .06, .15), t0, .12); t0 += d
def pizz(t0, notes):
    for f in notes:
        n = int(.18 * SR); t = np.arange(n) / SR; add(np.sin(2 * np.pi * f * t) * np.exp(-t * 18), t0, .35); t0 += .2
# hook: two stamp thuds
add(drum(90, .2), 0.15, .9); add(drum(80, .2), 0.35, .9)
siu = tone(np.linspace(220, 440, int(.6 * SR)), .6) * env(int(.6 * SR), .01, .2); add(siu, 0.0, .35); boom(0.3, .7)
scratch(0.65); boom(0.7, .9); violin(0.75, [(392, .3), (349, .3), (330, .5)])
n = int(1.0 * SR); add(band(rng.standard_normal(n), 2000, 8000) * env(n, .1, .3), 0.7, .1)
n = int(.25 * SR); add(tone(np.linspace(1800, 300, n), .25) * env(n, .02, .05), 1.6, .15)
# Messi: sad sting on the score, slam, drawer pop, ding, ba-dum-tss, easter-egg blip
violin(1.9, [(330, .25), (294, .3)]); groove(2.4, 15.8, 110)
boom(2.45, .5); add(drum(300, .1), 2.85, .6); add(bell(1318), 2.95, .4); badum(3.6); add(bell(3136, .15), 4.15, .2)
# penalty: odometer ticks, kick, SIUUU, claps
for k in range(10): n = int(.02 * SR); add(np.sin(2 * np.pi * 1200 * np.arange(n) / SR), 5.05 + k * .12, .3)
add(drum(120, .2), 5.0 + 1.0 / 1.3, 1.0); boom(6.05, .9); add(bell(2093), 6.1, .4); add(tone(np.linspace(180, 360, int(.9 * SR)), .9) * env(int(.9 * SR), .02, .3), 6.7, .3)
for k in range(4): add(clap(), 7.2 + k * .38, .7)
# camp: pop, paper unroll, wallet, ka-ching avalanche, PAID
boom(9.6, .7); n = int(.5 * SR); add(band(rng.standard_normal(n), 2000, 7000) * env(n, .05, .1), 9.8, .3)
boom(11.0, .6); add(bell(1568), 11.2, .5); add(bell(2093), 11.3, .5); add(bell(2637), 11.4, .4)
n = int(1.2 * SR); add(band(rng.standard_normal(n), 100, 900) * env(n, .1, .5), 11.1, .5); boom(11.6, .8); badum(12.1)
# kind of: pen scratch + sneaky pizzicato + stare
n = int(.5 * SR); add(band(rng.standard_normal(n), 3000, 8000) * np.abs(np.sin(2 * np.pi * 14 * np.arange(n) / SR)), 13.8, .25)
pizz(13.2, [392, 330, 392, 330, 294, 330]); boom(14.4, .8)
# twist
n = int(3 * SR); add(band(rng.standard_normal(n), 2000, 8000) * env(n, .2, .3), 15.8, .08)
violin(15.9, [(392, .4), (370, .4)]); scratch(16.8); boom(16.9, .8); add(drum(200, .1), 17.6, .6); add(drum(200, .1), 17.65, .6)
groove(18.8, 21.0, 130)
for k in range(3): add(drum(300, .12), 19.0 + k * .785, .5)
out /= np.abs(out).max() * 1.1
with wave.open(sys.argv[1], 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.stack([out, out], 1) * 32767).astype('<i2').tobytes())
