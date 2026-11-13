"""Synthesize cartoon voice SFX with espeak-ng (open-source TTS) + DSP. No recordings of real people.
Outputs 44.1 kHz mono WAVs: siu, siu_crowd, laugh_m, laugh_crowd, chuckle, grumble_angry, grumble_sad,
gasp, wail, ooh_crowd, cheer_crowd, bleat.
"""
import subprocess, wave, os, numpy as np
SR = 44100
rng = np.random.default_rng(3)
def espeak(text, voice='en+m3', speed=150, pitch=50, amp=180, gap=0):
    p = subprocess.run(['espeak-ng', '-v', voice, '-s', str(speed), '-p', str(pitch), '-a', str(amp), '-g', str(gap), '--stdout', text], capture_output=True, check=True).stdout
    import io; w = wave.open(io.BytesIO(p)); sr = w.getframerate(); x = np.frombuffer(w.readframes(w.getnframes()), '<i2').astype(np.float32) / 32768
    return np.interp(np.arange(0, len(x), sr / SR), np.arange(len(x)), x)
def shift(x, f):  # pitch+speed shift by resampling (cartoon effect)
    return np.interp(np.arange(0, len(x), f), np.arange(len(x)), x)
def trim(x, th=0.01):
    i = np.where(np.abs(x) > th)[0]; return x[i[0]:i[-1] + 1] if len(i) else x
def fade(x, a=.01, r=.08):
    n = len(x); e = np.ones(n); na, nr = int(a * SR), int(r * SR); e[:na] = np.linspace(0, 1, na); e[-nr:] *= np.linspace(1, 0, nr); return x * e
def norm(x, g=0.9): return x / (np.abs(x).max() + 1e-9) * g
def layer(parts, spread=0.25):
    L = max(len(p) for p in parts) + int(spread * SR); out = np.zeros(L)
    for p in parts: o = int(rng.random() * spread * SR); out[o:o + len(p)] += p
    return out
def band(x, lo, hi):
    f = np.fft.rfftfreq(len(x), 1 / SR); S = np.fft.rfft(x); S *= np.exp(-((np.log(f + 1) - np.log((lo * hi) ** .5)) ** 2) / (2 * (np.log(hi / lo) / 2) ** 2)); return np.fft.irfft(S, len(x))
def save(name, x):
    x = norm(fade(trim(x))); w = wave.open(f'{name}.wav', 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((x * 32767).astype('<i2').tobytes()); w.close(); print(name, round(len(x) / SR, 2), 's')

# SIUUU: one big shout, long rising-falling vowel
siu = espeak('see-oooooooooo', 'en+m7', speed=95, pitch=70, amp=200)
save('siu', shift(siu, 1.08))
# crowd SIUUU: many voices, detuned and offset
save('siu_crowd', layer([shift(espeak('see-ooooooo', v, 100, p, 180), f) for v, p, f in [('en+m1', 30, .95), ('en+m3', 45, 1.0), ('en+m7', 60, 1.05), ('en+f2', 55, 1.02), ('en+m2', 40, .97), ('en+f4', 65, 1.08), ('en+m4', 50, 1.0), ('en+m5', 35, .93)]], 0.15))
# laughs
save('laugh_m', shift(espeak('ha ha ha ha ha haa', 'en+m3', 210, 60, 200, 1), 1.05))
save('chuckle', shift(espeak('heh heh heh', 'en+m1', 190, 40, 170), 0.95))
save('laugh_crowd', layer([shift(espeak(t, v, 220, p, 160, 1), f) for t, v, p, f in [('ha ha ha ha ha', 'en+m3', 55, 1.0), ('ho ho ho ho', 'en+m1', 30, .92), ('he he he he he', 'en+f2', 70, 1.1), ('ha ha haa ha', 'en+f4', 60, 1.05), ('hah hah hah', 'en+m5', 40, .97), ('hee hee hee', 'en+f3', 80, 1.15)]], 0.3))
# gibberish "cursing": nonsense syllables, angry contour, sped up (meaningless on purpose)
syl = ['blarg', 'frumm', 'skadoo', 'nargh', 'brrrt', 'zibbit', 'flonk', 'grumbo', 'kraz', 'mufla', 'drabb', 'snorf']
def gib(n, voice, pitch, speed, f):
    return shift(espeak(' '.join(rng.choice(syl, n)) + '!', voice, speed, pitch, 200, 0), f)
save('grumble_angry', np.concatenate([gib(5, 'en+m7', 70, 230, 1.18), np.zeros(int(.08 * SR)), gib(4, 'en+m7', 85, 250, 1.25)]))
save('grumble_sad', gib(5, 'en+m3', 35, 170, 1.12))
save('gasp', shift(espeak('huh?!', 'en+m3', 140, 80, 200), 1.1))
save('wail', shift(espeak('waaaaaah waaaaaaaah', 'en+m3', 90, 90, 200), 1.12))
save('ooh_crowd', layer([shift(espeak('ooooooooh', v, 90, p, 170), f) for v, p, f in [('en+m1', 20, .95), ('en+m3', 40, 1.0), ('en+f2', 60, 1.03), ('en+m4', 30, .98), ('en+f4', 70, 1.06), ('en+m2', 45, 1.0)]], 0.12))
cheer = layer([shift(espeak(t, v, 160, p, 160), f) for t, v, p, f in [('yeaaah', 'en+m1', 40, 1.0), ('woooo', 'en+f2', 70, 1.05), ('yeah yeah', 'en+m3', 55, 1.02), ('goooal', 'en+m4', 30, .96), ('wooo hooo', 'en+f4', 75, 1.1), ('yeaaah', 'en+m5', 45, .98)]], 0.3)
n = len(cheer); noise = band(rng.standard_normal(n), 300, 2500); noise = noise / np.abs(noise).max() * 0.35 * np.minimum(1, np.arange(n) / (0.15 * SR))
save('cheer_crowd', cheer / np.abs(cheer).max() + noise)
# goat bleat: vibrato "meh" made from a voice + tremolo
b = shift(espeak('meeeeeh', 'en+f3', 110, 99, 200), 1.25); t = np.arange(len(b)) / SR
save('bleat', b * (0.6 + 0.4 * np.sin(2 * np.pi * 13 * t)))
