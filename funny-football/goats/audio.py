"""Original synthesized soundtrack for 'The GOATs Clock Out' (no third-party audio)."""
import sys, wave
import numpy as np
SR, T = 44100, 22
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
keys = [(0, 1.0), (0.6, 0), (5.4, .4), (7.1, 1.0), (8.5, .4), (16.4, 0), (19.4, .9), (22, .5)]
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
# hook: bright SIU stab -> record scratch -> rain + violin
siu = tone(np.linspace(220, 440, int(.5 * SR)), .5) * env(int(.5 * SR), .01, .2); add(siu, 0.0, .35)
scratch(0.55); boom(0.6, .9); violin(0.65, [(392, .3), (349, .3), (330, .6)])
n = int(1.2 * SR); add(band(rng.standard_normal(n), 2000, 8000) * env(n, .1, .3), 0.6, .1)
n = int(.3 * SR); add(tone(np.linspace(1800, 300, n), .3) * env(n, .02, .05), 1.6, .15)
groove(1.9, 16.4, 110)
# Messi: slam, drawer pop, elevator ding, ba-dum-tss, tiny blip on the v3.0 easter egg
boom(2.2, 1.0); add(drum(300, .1), 2.55, .6); add(bell(1318), 2.7, .4); badum(3.3); add(bell(3136, .15), 4.15, .2)
# penalty: clock ticks, kick, SIUUU, slow claps
for k in range(8): n = int(.02 * SR); add(np.sin(2 * np.pi * 1200 * np.arange(n) / SR), 5.45 + k * .13, .3)
add(drum(120, .2), 5.4 + 1.0 / 1.3, 1.0); boom(7.1, .9); add(tone(np.linspace(180, 360, int(.9 * SR)), .9) * env(int(.9 * SR), .02, .3), 7.1, .3)
for k in range(4): add(clap(), 7.9 + k * .38, .7)
# camp: pop, long paper unroll, ka-ching, avalanche
boom(10.0, .7); n = int(.6 * SR); add(band(rng.standard_normal(n), 2000, 7000) * env(n, .05, .1), 10.3, .25)
add(bell(1568), 11.3, .5); add(bell(2093), 11.4, .5); add(bell(2637), 11.5, .4)
n = int(1.2 * SR); add(band(rng.standard_normal(n), 100, 900) * env(n, .1, .5), 11.5, .5); boom(12.0, .8); badum(12.6)
# technically: pen scratch + sneaky pizzicato + look-at-camera boom
n = int(.5 * SR); add(band(rng.standard_normal(n), 3000, 8000) * np.abs(np.sin(2 * np.pi * 14 * np.arange(n) / SR)), 14.2, .25)
pizz(13.6, [392, 330, 392, 330, 294, 330]); boom(15.0, .8)
# twist: rain, violin, synced boot hide, record scratch on the asterisk
n = int(3 * SR); add(band(rng.standard_normal(n), 2000, 8000) * env(n, .2, .3), 16.4, .08)
violin(16.5, [(392, .4), (370, .4)]); scratch(17.4); boom(17.5, .8); add(drum(200, .1), 18.2, .6); add(drum(200, .1), 18.25, .6)
groove(19.4, 21.6, 130)
for k in range(3): add(drum(300, .12), 19.6 + k * .785, .5)
out /= np.abs(out).max() * 1.1
with wave.open(sys.argv[1], 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.stack([out, out], 1) * 32767).astype('<i2').tobytes())
