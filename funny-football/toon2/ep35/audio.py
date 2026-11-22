"""Ep35 BLOCK BY BLOCK sound — this episode's own palette (ElevenLabs, free credits; no shared library, no channel sting):
music  snd/music.wav  8-bit chiptune march (eleven_music_v2_5)
sfx    snd/slam (block thunk + shimmer), post (PING + clatter down steps), scrape (block sliding out + creak), robot (beeps + error buzz), goat (mocking bleat)
voices snd/vo_r986 "Nine eight six! SIUUU!" + vo_mine "No no no! MINE!" (premade voice 'Harry'), vo_bot "Own goal. Removing." (library voice 'Vector'). Invented lines."""
import os, sys, numpy as np
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(H, '..', 'sfx'))
from music import SR
from mix import Desk
from fx2 import Mix2
from scipy.io import wavfile
D = 27.0; d = Desk(D); m = Mix2(D, ep=35)
def snd(name, a=0, b=None):
    sr, x = wavfile.read(os.path.join(H, 'snd', name + '.wav')); x = x.astype(float).T / 32768; x = x[:, int(a * SR): int(b * SR) if b else None]
    f = np.ones(x.shape[1]); k = min(220, len(f) // 2); f[:k] = np.linspace(0, 1, k); f[-k:] = np.linspace(1, 0, k); return x * f
d.add('music', snd('music', 0, 27.0), 0, .5)
d.add('fx', snd('slam'), 0.93, 1.0); m.whoosh(0.7, .25, .3)
d.add('vox', snd('vo_r986'), 0.9, 2.3)                 # "Nine eight six!" on the slam, "SIUUU!" on the jump (2.3)
m.spring(1.25, .25); m.thump(2.95, .5); m.whoosh(3.5, .9, .25)
d.add('fx', snd('goat'), 5.6, .7, .3)                   # Ep8's goat at the summit
m.whoosh(7.0, .3, .2); m.thump(7.25, .3); [m.thump(t, .2) for t in (8.05, 8.2, 8.35)]; m.whoosh(8.5, .3, .4)
d.add('fx', snd('post'), 8.83, 1.0); m.slide_whistle(9.3, False, .9, .25)
d.add('crowd', snd('goat', .1, 1.4), 9.1, .35, .35)     # the post 'laughs' (bleat-laugh under the PING, quiet)
[m.thump(11.5 + i * 0.12, .18) for i in range(25)]      # the ball bouncing down the flights
for t0 in (12.2, 12.75): d.add('fx', snd('slam', 0, .5), t0, .7)
m.thump(13.3, .5); m.crowd(13.45, 'cheer', 1.6, .3)
d.add('fx', snd('robot'), 15.0, .8, -.3); d.add('vox', snd('vo_bot'), 15.55, 3.4, -.3)
d.add('fx', snd('scrape', 1.6), 16.4, 1.4); m.honk(17.4, .2)
m.whoosh(18.7, .5, .35); d.add('vox', snd('vo_mine'), 18.7, 2.3, .2); m.thump(19.25, .6)
d.add('fx', snd('slam'), 20.48, 1.0); m.spring(20.6, .3); m.whoosh(20.7, .6, .35); d.add('fx', snd('robot', .9, 1.9), 20.7, .5, -.5)
m.whoosh(22.2, .3, .2); d.add('fx', snd('slam', .2), 22.7, .45); d.add('fx', snd('goat'), 25.2, .45, .4)
d.add('fx', (m.fx + m.music).T, 0, 1.0); d.add('vox', m.vox.T, 0, 1.0)
d.duck('music', [0.93, 8.83, 20.48], .45, .15, .4); d.duck('music', [0.9, 2.3, 15.55, 16.6, 18.7, 19.7], .55, 1.0, .3); d.room('fx', 'room', .1)
print(d.master(sys.argv[1], os.path.join(H, 'release', 'stems')))
