"""mix.py — mixing & mastering v2 (overhaul M1b, 21 Nov 2026).
Stereo buses with EQ + compression, sidechain ducking, room reverb, constant-power panning, master glue + limiter,
stems export so the music can be reused ("Soccer 365 – <name>" original sound).

    from mix import Desk
    d = Desk(dur)                      # seconds
    d.add('music', stereo_or_mono, t=0, pan=0)   # buses: music, drums, bass, fx, vox, crowd
    d.duck('music', times, depth=.45)  # sidechain under hits / voices
    d.room('fx', 'stadium')            # stadium | room | hall | phone | none
    d.master(path_wav, stems_dir=None) # writes 48 kHz 24-bit stereo, returns peak/RMS info
"""
import os, wave, numpy as np
from scipy.signal import butter, sosfilt, fftconvolve
SR = 44100

def _st(x):
    x = np.asarray(x, dtype=float)
    return np.stack([x, x]) if x.ndim == 1 else x
def pan_st(x, p):  # p -1..1, constant power
    a = (p + 1) * np.pi / 4; x = np.asarray(x, float)
    if x.ndim == 2: return np.stack([x[0] * np.cos(a) * 1.414, x[1] * np.sin(a) * 1.414])
    return np.stack([x * np.cos(a), x * np.sin(a)]) * 1.414
def shelf(x, f, gain_db, kind='low'):
    g = 10 ** (gain_db / 20) - 1; part = sosfilt(butter(2, f, 'low' if kind == 'low' else 'high', fs=SR, output='sos'), x, axis=-1); return x + part * g
def peak(x, lo, hi, gain_db):
    g = 10 ** (gain_db / 20) - 1; return x + sosfilt(butter(2, [lo, hi], 'band', fs=SR, output='sos'), x, axis=-1) * g
def comp(x, thr_db=-18, ratio=3, att=.008, rel=.12, makeup_db=0):
    lvl = np.abs(x).max(axis=0) if x.ndim == 2 else np.abs(x); env = np.zeros_like(lvl); a, r = np.exp(-1 / (att * SR)), np.exp(-1 / (rel * SR)); e = 0.0
    # block-wise envelope (fast enough, 64-sample hop)
    hop = 64; blocks = lvl[: len(lvl) // hop * hop].reshape(-1, hop).max(axis=1); out = np.zeros_like(blocks); ah, rh = a ** hop, r ** hop
    for i, v in enumerate(blocks): e = ah * e + (1 - ah) * v if v > e else rh * e + (1 - rh) * v; out[i] = e
    env = np.repeat(out, hop); env = np.pad(env, (0, len(lvl) - len(env)), mode='edge')
    db = 20 * np.log10(env + 1e-9); over = np.maximum(0, db - thr_db); gr = -over * (1 - 1 / ratio) + makeup_db; g = 10 ** (gr / 20)
    return x * g
def reverb_ir(kind):
    if kind == 'none': return None
    t60, pre, bright = {'stadium': (2.6, .03, 5000), 'hall': (1.8, .02, 6000), 'room': (.45, .005, 7000), 'phone': (.12, 0, 3000), 'tunnel': (1.4, .01, 3500)}[kind]
    n = int(t60 * SR); rng = np.random.default_rng(7); t = np.arange(n) / SR; ir = []
    for ch in range(2):
        x = rng.standard_normal(n) * np.exp(-6.9 * t / t60); x = sosfilt(butter(1, bright, 'low', fs=SR, output='sos'), x)
        x = np.concatenate([np.zeros(int(pre * SR)), x]); ir.append(x / np.sqrt((x ** 2).sum()))
    return np.stack(ir)

class Desk:
    BUS = ['music', 'drums', 'bass', 'fx', 'vox', 'crowd']
    def __init__(self, dur):
        self.n = int((dur + .5) * SR); self.b = {k: np.zeros((2, self.n)) for k in self.BUS}; self.sends = {k: ('none', 0) for k in self.BUS}; self.ducks = []
    def add(self, bus, x, t=0.0, g=1.0, pan=0.0):
        x = pan_st(x, pan) if (np.asarray(x).ndim == 1 or pan) else _st(x); i = int(t * SR)
        if i >= self.n: return
        m = min(x.shape[1], self.n - max(i, 0)); j = max(i, 0); self.b[bus][:, j:j + m] += x[:, (j - i):(j - i) + m] * g
    def add_stems(self, stems, t=0.0, g=1.0, widths=None):  # stems from music.Song.render()
        mp = {'drums': 'drums', 'bass': 'bass', 'chords': 'music', 'lead': 'music', 'fx': 'fx'}; widths = widths or {'chords': .6, 'lead': .25}
        TARGET = {'drums': -19, 'bass': -21, 'chords': -24, 'lead': -21, 'fx': -27}  # gain staging (dB RMS of the active part)
        for k, x in stems.items():
            act = x[np.abs(x) > 1e-4]; r = np.sqrt((act ** 2).mean()) if len(act) else 0
            if r > 0: x = x * 10 ** (TARGET.get(k, -22) / 20) / r
            w = widths.get(k, 0); st = np.stack([x, np.roll(x, int(.012 * SR) if w else 0)]) if w else _st(x)
            if w: st = np.stack([st[0] * (1 + w / 2) + st[1] * (1 - w / 2), st[1] * (1 + w / 2) + st[0] * (1 - w / 2)]) / 2
            self.add(mp[k], st, t, g)
    def duck(self, bus, times, depth=.45, hold=.08, release=.25):
        g = np.ones(self.n)
        for tm in times:
            i = int(tm * SR); a = int(.005 * SR); h = int(hold * SR); r = int(release * SR)
            seg = np.concatenate([np.linspace(1, 1 - depth, a), np.full(h, 1 - depth), np.linspace(1 - depth, 1, r)]); m = min(len(seg), self.n - i)
            if m > 0: g[i:i + m] = np.minimum(g[i:i + m], seg[:m])
        self.b[bus] *= g
    def room(self, bus, kind, wet=.18): self.sends[bus] = (kind, wet)
    def _bus_chain(self, k, x):
        if k == 'drums': x = shelf(x, 90, 2.5, 'low'); x = comp(x, -14, 4, .003, .08, 2)
        if k == 'bass': x = sosfilt(butter(2, 35, 'high', fs=SR, output='sos'), x, axis=-1); x = comp(x, -16, 4, .01, .15, 2)
        if k == 'music': x = peak(x, 250, 500, -2); x = shelf(x, 8000, 1.5, 'high'); x = comp(x, -20, 2, .02, .2, 1)
        if k == 'vox': x = sosfilt(butter(2, 120, 'high', fs=SR, output='sos'), x, axis=-1); x = peak(x, 2500, 5000, 2.5); x = comp(x, -20, 3.5, .005, .1, 3)
        if k == 'fx': x = comp(x, -12, 2.5, .002, .1, 0)
        kind, wet = self.sends[k]; ir = reverb_ir(kind)
        if ir is not None and wet > 0:
            src = x.mean(axis=0); w = np.stack([fftconvolve(src, ir[c])[: self.n] for c in range(2)]); x = x + w * wet
        return x
    def master(self, path, stems_dir=None, target_rms_db=-15.5):
        proc = {k: self._bus_chain(k, v) for k, v in self.b.items()}; mixd = sum(proc.values())
        mixd = comp(mixd, -10, 2, .01, .2, 0)  # glue
        rms = np.sqrt((mixd ** 2).mean()) + 1e-9; mixd *= 10 ** (target_rms_db / 20) / rms
        mixd = np.tanh(mixd * 1.1) / 1.1; pk = np.abs(mixd).max(); mixd *= min(1, .89 / pk) if pk > .89 else 1  # soft clip + ceiling ~ -1 dBFS
        _write(path, mixd)
        if stems_dir:
            os.makedirs(stems_dir, exist_ok=True)
            for k, v in proc.items():
                if np.abs(v).max() > 1e-4: _write(os.path.join(stems_dir, f'{k}.wav'), v / max(1, np.abs(v).max() / .89))
        return {'peak': float(np.abs(mixd).max()), 'rms_db': float(20 * np.log10(np.sqrt((mixd ** 2).mean()) + 1e-9))}

def _write(path, st):
    st = np.clip(st, -1, 1); d = (st.T * 32767).astype('<i2')
    with wave.open(path, 'wb') as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(d.tobytes())
