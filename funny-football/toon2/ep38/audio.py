"""Ep38 THE LIKE RACE sound: synth phonk (music.py — saves ElevenLabs credits for Ep36; genre not used in the last 6 episodes) +
own ElevenLabs pieces: notification-ping flood, ceiling smash + choir; race commentator (library voice 'British Football Announcer'): "And they're off!", "Ronaldo takes the lead!"."""
import os, sys, numpy as np
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(H, '..', 'sfx'))
from music import Song, SR
from mix import Desk
from fx2 import Mix2
from scipy.io import wavfile
D = 26.5; d = Desk(D); m = Mix2(D, ep=38)
def snd(name, a=0, b=None):
    sr, x = wavfile.read(os.path.join(H, 'snd', name + '.wav')); x = x.astype(float).T / 32768; x = x[:, int(a * SR): int(b * SR) if b else None]
    f = np.ones(x.shape[1]); k = min(220, len(f) // 2); f[:k] = np.linspace(0, 1, k); f[-k:] = np.linspace(1, 0, k); return x * f
song = Song('phonk', key='F', minor=True, seed=38).form([('intro', 2), ('verse', 3), ('drop', 4), ('break', 2), ('drop', 3), ('outro', 2)]); st = song.render()
L = min(len(st['drums']), int(D * SR)); env = np.ones(L)
for a, b, g in ((16.8, 17.9, 0.12), (24.6, 26.5, 0.35)): env[int(a * SR):int(b * SR)] = g        # the scroll-back hush before the twist; soft tail
env = np.convolve(env, np.ones(1500) / 1500, 'same'); d.add_stems({k: v[:L] * env for k, v in st.items()})
d.add('fx', snd('pings', 0.6, 3.6), 0.5, .45, -.3); m.whoosh(0.35, .4, .25)                  # Messi's post fills with likes
m.whoosh(4.4, .3, .2); d.add('fx', snd('pings', 0.8, 2.6), 5.2, .35, -.1)                     # likes on his comment
m.whoosh(8.0, .5, .35); d.add('vox', snd('vo_off', 0.25), 8.6, 3.6)                          # "And they're off!"
d.add('fx', snd('pings', 0.6), 9.0, .55, .3)
d.add('vox', snd('vo_lead'), 11.85, 3.6); m.crowd(12.1, 'cheer', 1.6, .35)                  # "Ronaldo takes the lead!"
m.slide_whistle(16.6, False, .8, .25); m.whoosh(17.0, .3, .3)                                  # Messi scrolls back…
m.timpani(17.7, 70, .4, roll=1.2); d.add('fx', snd('smash'), 18.95, 1.0); m.crowd(19.2, 'ooh', 1.6, .45)
[m.thump(22.2 + i * 0.22, .12) for i in range(18)]; m.crowd(24.0, 'laugh', 1.6, .3)            # +1 +1 +1 taps
d.add('fx', (m.fx + m.music).T, 0, 1.0); d.add('vox', m.vox.T, 0, 1.0)
d.duck('music', [18.95], .5, .3, .5); d.duck('music', [8.6, 11.85], .6, 1.3, .3); d.duck('drums', [8.6, 11.85], .78, 1.4, .3); d.duck('bass', [8.6, 11.85], .6, 1.4, .3); d.room('fx', 'room', .1)
print(d.master(sys.argv[1], os.path.join(H, 'release', 'stems')))
