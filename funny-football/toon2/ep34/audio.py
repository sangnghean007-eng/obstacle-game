"""Ep34 THE THROW-IN sound v3 — owner: "the sound repeats across videos". This episode's own palette, made for it (ElevenLabs, free credits):
music  snd/music.wav  — original tango-telenovela comedy bed (eleven_music_v2_5), starts at 1.5 s so its first break lands on the BONK
sfx    snd/bonk|stretch|whistle|crowd|hook.wav (eleven_text_to_sound_v3) — ball bonk, rubber arm, 3 whistle blasts + hit, crowd ooh→laugh, stage hook
voices snd/vo_*.wav (eleven_v4, premade/library voices, no cloning) — Tapia "On purpose! That's a RED!", Messi "I'm not Ronaldo", Ronaldo "What?! I just got here!"
No channel sting (it was the same in every episode); the music's own brass button ends it. Synth fx2 only for small fills."""
import os, sys, subprocess, numpy as np
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(H, '..', 'sfx'))
from music import SR
from mix import Desk
from fx2 import Mix2
from scipy.io import wavfile
S = 1.2   # the scene runs 1.2x slower (scene.html SLOW): every cue time below is in story time and scaled here; voices keep natural speed
D = 23.3 * S; d = Desk(D); m = Mix2(D, ep=34)
_add = d.add; d.add = lambda bus, x, t=0.0, g=1.0, pan=0.0: _add(bus, x, t * S, g, pan)
_duck = d.duck; d.duck = lambda bus, times, *a: _duck(bus, [x * S for x in times], *a)
for _n in ('whoosh', 'bonk', 'thump', 'spring', 'squeak', 'cork', 'honk', 'timpani', 'wahwah', 'whip', 'slide_whistle', 'boom', 'crowd'):
    if hasattr(m, _n): setattr(m, _n, (lambda f: lambda t, *a, **k: f(t * S, *a, **k))(getattr(m, _n)))
_vo = m.vo; m.vo = lambda who, what, t, *a, **k: _vo(who, what, t * S, *a, **k)
def snd(name, a=0, b=None, tempo=1.0):
    sr, x = wavfile.read(os.path.join(H, 'snd', name + '.wav')); x = x.astype(float).T / 32768
    x = x[:, int(a * SR): int(b * SR) if b else None]
    if tempo != 1.0:  # speed up a line without changing pitch (ffmpeg atempo)
        p = subprocess.run(['ffmpeg', '-v', 'error', '-f', 's16le', '-ar', str(SR), '-ac', '2', '-i', '-', '-af', f'atempo={tempo}', '-f', 's16le', '-'],
                           input=(x.T * 32767).astype('<i2').tobytes(), capture_output=True).stdout
        x = np.frombuffer(p, '<i2').reshape(-1, 2).T.astype(float) / 32768
    f = np.ones(x.shape[1]); k = min(220, len(f) // 2); f[:k] = np.linspace(0, 1, k); f[-k:] = np.linspace(1, 0, k); return x * f
# music bed
d.add('music', snd('music', tempo=1 / S), 1.5, .55)   # stretched with the picture so its breaks stay on the hits
# stadium air under everything (quiet), opening whistle + crowd before the music comes in
n = int(D * SR); d.add('crowd', np.stack([np.convolve(np.random.default_rng(4).standard_normal(n), np.ones(260) / 260, 'same') * 4] * 2), 0, .12)
d.add('fx', snd('whistle', 0, .45), 0.15, .45); d.add('crowd', snd('crowd', 0, 1.3), .4, .35)
m.vo('messi', 'hmph', 3.3, .35)
# the throw: whoosh → BONK (music break) → ooh→laugh, three bounces
m.whoosh(4.35, .3, .35); d.add('fx', snd('bonk'), 4.6, 1.0); m.thump(4.64, .5); d.add('crowd', snd('crowd'), 4.75, .6)
[m.spring(t0, .28) for t0 in (5.62, 6.02, 6.32)]; m.squeak(6.6, .25)
# Tapia complains, ref whistles
d.add('fx', snd('whistle', 0, 1.25), 8.15, .55)
d.add('vox', snd('vo_tapia', .05, 2.4, 1.15), 8.45, 2.3, .35)
# THE GAG: Messi's line → rubber arm → Ronaldo dragged in → RED (blasts + orchestral hit) → "I just got here?!" → stage hook
d.add('vox', snd('vo_messi', .15, 1.15), 10.02, 2.5, -.25)
d.add('fx', snd('stretch'), 10.0, 1.0, -.2); m.whoosh(10.4, .5, .3); m.thump(10.95, .6)
d.add('fx', snd('whistle', 0, 2.6), 10.85, .4); d.add('crowd', snd('crowd', 0, 1.4), 11.0, .25)
d.add('vox', snd('vo_ronaldo', .05, .75), 10.97, 2.3, .25); d.add('vox', snd('vo_ronaldo', .95, 2.3), 11.5, 2.3, .25)
m.cork(12.0, .2); d.add('fx', snd('hook'), 12.3, 1.0, .3); d.add('crowd', snd('crowd', 1.2), 12.6, .55)
# back in the match: Force-O-Meter, FT, training
m.honk(13.50, .25); m.timpani(14.00, 80, .45, roll=1.1); m.spring(15.20, .3); m.cork(15.25, .25); d.add('crowd', snd('crowd', 1.5), 15.3, .35)
d.add('fx', snd('whistle', 0, .45), 16.4, .4); d.add('fx', snd('whistle', 0, .45), 16.75, .4); m.wahwah(17.20, .28); d.add('crowd', snd('crowd', .6), 17.4, .35)
m.whoosh(18.35, .3, .3); d.add('fx', snd('bonk', 0, .6), 18.6, .8); m.thump(18.9, .5)
d.add('vox', snd('vo_messi', 1.25, 2.3), 21.3, 2.0, -.2)   # Messi's chuckle — the callback for the ending
d.add('crowd', snd('crowd', 1.4), 21.9, .3)
d.add('fx', (m.fx + m.music).T, 0, 1.0); d.add('vox', m.vox.T, 0, 1.0)
d.duck('music', [4.62, 10.95], .45, .15, .4); d.duck('music', [8.45, 10.02, 10.97, 11.5, 21.3], .6, 1.6, .3); d.room('fx', 'room', .12)
print(d.master(sys.argv[1], os.path.join(H, 'release', 'stems')))
