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
keys = [(0, 0), (1.4, 0), (1.5, .6), (3.9, .6), (4.0, 0), (22.5, 0)]   # crowd only in the stadium scene
add(crowd * np.interp(tt, *zip(*keys)), 0, .28)
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
# events: few sounds, each one pays off; clear spoken lines carry the jokes
L = np.zeros(N)
def line(name, t0, g=1.0):
    s = V('lines/' + name); i = int(t0 * SR); n = min(len(s), N - i); L[i:i + n] += g * s[:n]
whoosh(0.0, .6); line('n_retired', 0.15)                                   # "Messi retired."
line('m_bye', 2.0, .95)                                                    # "Bye bye, national team."
for k in [0.5, 1.4, 2.0, 2.4, 2.7, 2.9, 3.05, 3.2, 3.3]: add(drum(130, .12), 4.0 + k, .55, True)
line('n_kept', 4.1)                                                        # "And then... he kept scoring."
add(V('cheer_crowd'), 7.3, .45, True); line('n_26', 7.35)                  # "Twenty six goals!"
add(drum(300, .15), 8.55, 1.0, True); boom(8.55)                           # BONK
line('n_boot', 8.95)                                                       # "Golden Boot. Again."
add(tone(np.linspace(300, 260, int(.6 * SR)), .6) * env(int(.6 * SR), .02, .3), 11.1, .15, True)
line('r_26', 12.0, 1.0); add(V('grumble_angry'), 12.85, .55, True)        # "Twenty six?!" + the one bit of gibberish
add(V('siu'), 13.6, .9, True); whoosh(13.6, .9); add(drum(300, .12), 14.5, .9, True); add(V('laugh_crowd'), 14.75, .4, True)
add(drum(500, .08), 15.9, .6, True); line('n_only', 16.1)                  # "Retired... from the national team only."
add(drum(200), 18.4, .5, True); add(drum(150), 18.6, .5, True); add(bell(1568, .6), 18.9, .3, True)   # ba-dum-tss
add(drum(300, .1), 21.05, .6, True); add(bell(1568, .6), 21.6, .4, True); line('n_follow', 21.55)
# duck the bed under speech
e = np.convolve(np.abs(L), np.ones(int(.08 * SR)) / int(.08 * SR), 'same'); e = np.clip(e / (e.max() * .15), 0, 1)
out = out * (1 - .55 * e) + L * (np.abs(out).max() / max(np.abs(L).max(), 1e-6)) * 1.1
out /= np.abs(out).max() * 1.1
with wave.open(sys.argv[1], 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.stack([out, out], 1) * 32767).astype('<i2').tobytes())
