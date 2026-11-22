"""Ep38 THE LIKE RACE sound: synth phonk (music.py — saves ElevenLabs credits for Ep36; genre not used in the last 6 episodes) +
own ElevenLabs pieces: notification-ping flood, ceiling smash + choir; race commentator (library voice 'British Football Announcer'): "And they're off!", "Ronaldo takes the lead!"."""
import os, sys, numpy as np
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(H, '..', 'sfx'))
from music import Song, SR
from mix import Desk
from fx2 import Mix2
from scipy.io import wavfile
D = 29.6; d = Desk(D); m = Mix2(D, ep=38)
def type_clicks(t0, dur, gap, g, hi=True):   # phone key taps (synth; typing forward = bright, backspace = duller)
    n = int(0.012 * SR); rng = np.random.default_rng(int(t0 * 100))
    for i in range(int(dur / gap)):
        c = rng.standard_normal(n) * np.exp(-np.linspace(0, 8, n)); c = c if hi else np.convolve(c, np.ones(6) / 6, 'same'); d.add('fx', c * g, t0 + i * gap + rng.uniform(-.01, .01), 1.0, .1)
def snd(name, a=0, b=None):
    sr, x = wavfile.read(os.path.join(H, 'snd', name + '.wav')); x = x.astype(float).T / 32768; x = x[:, int(a * SR): int(b * SR) if b else None]
    f = np.ones(x.shape[1]); k = min(220, len(f) // 2); f[:k] = np.linspace(0, 1, k); f[-k:] = np.linspace(1, 0, k); return x * f
song = Song('phonk', key='F', minor=True, seed=38).form([('intro', 2), ('verse', 3), ('drop', 4), ('break', 2), ('drop', 3), ('outro', 4)]); st = song.render()
L = min(len(st['drums']), int(D * SR)); env = np.ones(L)
for a, b, g in ((15.6, 21.5, 0.35), (20.4, 21.5, 0.12), (27.8, 29.6, 0.35)): env[int(a * SR):int(b * SR)] = g        # the scroll-back hush before the twist; soft tail
env = np.convolve(env, np.ones(1500) / 1500, 'same'); d.add_stems({k: v[:L] * env for k, v in st.items()})
d.add('fx', snd('pings', 0.6, 3.6), 0.5, .45, -.3); m.whoosh(0.35, .4, .25)                  # Messi's post fills with likes
m.whoosh(4.4, .3, .2); d.add('fx', snd('pings', 0.8, 2.6), 5.2, .35, -.1)                     # likes on his comment
m.whoosh(8.0, .5, .35); d.add('vox', snd('vo_off', 0.25), 8.6, 3.6)                          # "And they're off!"
d.add('fx', snd('pings', 0.6), 9.0, .55, .3)
d.add('vox', snd('vo_lead'), 11.85, 3.6); m.crowd(12.1, 'cheer', 1.6, .35)                  # "Ronaldo takes the lead!"
type_clicks(16.1, 1.2, .07, .16); m.squeak(17.5, .25); type_clicks(18.2, 0.85, .09, .2, hi=False); m.whoosh(19.3, .3, .25); m.wahwah(19.4, .2)   # types… sees 41M… deletes
m.slide_whistle(20.2, False, .8, .25); m.whoosh(20.6, .3, .3)                                  # Messi scrolls back…
m.timpani(21.3, 70, .4, roll=1.2); d.add('fx', snd('smash'), 22.55, 1.0); m.crowd(22.8, 'ooh', 1.6, .45)
[m.thump(25.8 + i * 0.22, .12) for i in range(18)]; m.crowd(27.6, 'laugh', 1.6, .3)            # +1 +1 +1 taps
d.add('fx', (m.fx + m.music).T, 0, 1.0); d.add('vox', m.vox.T, 0, 1.0)
d.duck('music', [22.55], .5, .3, .5); d.duck('music', [8.6, 11.85], .6, 1.3, .3); d.duck('drums', [8.6, 11.85], .78, 1.4, .3); d.duck('bass', [8.6, 11.85], .6, 1.4, .3); d.room('fx', 'room', .1)
print(d.master(sys.argv[1], os.path.join(H, 'release', 'stems')))
