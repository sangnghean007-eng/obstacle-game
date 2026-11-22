"""Ep37 THE EXCUSES sound — own palette (ElevenLabs, free credits): big-band gala swing (music), drumroll+fanfare+applause, balloon deflate,
split-flap board, angry phone typing, mate slurp; Ronaldo lines (premade voice 'Harry', the channel's Ronaldo voice): "Unacceptable!", "Losing credibility!",
"The numbers don't deceive!" (his real words, short), "Ssssiiuuuu!" (own take). Messi never speaks — only the slurp."""
import os, sys, numpy as np
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(H, '..', 'sfx'))
from music import SR
from mix import Desk
from fx2 import Mix2
from scipy.io import wavfile
D = 28.0; d = Desk(D); m = Mix2(D, ep=37)
def snd(name, a=0, b=None):
    sr, x = wavfile.read(os.path.join(H, 'snd', name + '.wav')); x = x.astype(float).T / 32768; x = x[:, int(a * SR): int(b * SR) if b else None]
    f = np.ones(x.shape[1]); k = min(220, len(f) // 2); f[:k] = np.linspace(0, 1, k); f[-k:] = np.linspace(1, 0, k); return x * f
d.add('music', snd('music', 0, 26.0), 0, .5)
n = int(D * SR); d.add('crowd', np.stack([np.convolve(np.random.default_rng(37).standard_normal(n), np.ones(300) / 300, 'same') * 4] * 2), 0, .1)   # hall murmur
d.add('fx', snd('fanfare'), 0.1, .8); m.thump(1.25, .4); m.whoosh(1.55, .4, .3)
d.add('fx', snd('typing'), 4.3, .9, .2); d.add('vox', snd('vo_unacc'), 6.4, 4.0, .2)
d.add('fx', snd('fanfare', 1.0, 3.6), 8.5, .7); m.thump(9.0, .35); d.add('fx', snd('slurp', 0, 1.4), 9.6, .8, -.2)
d.add('vox', snd('vo_cred'), 11.5, 3.0, .3)
d.add('fx', snd('deflate'), 12.62, 1.0, -.3); m.cork(13.5, .35); m.spring(13.55, .3)
m.whoosh(14.2, .9, .35); [m.thump(14.3 + i * 0.18, .18) for i in range(5)]
d.add('vox', snd('vo_numbers'), 15.55, 3.0, .3)
m.whoosh(16.4, .4, .2); d.add('fx', snd('flap'), 17.2, 1.0); m.crowd(17.6, 'ooh', 1.4, .35); m.wahwah(18.1, .25)
m.whoosh(20.4, .6, .3); m.cork(21.3, .3); d.add('vox', snd('siu'), 21.9, 2.4, .2); m.crowd(22.6, 'cheer', 1.4, .25)
d.add('fx', snd('slurp'), 25.1, 1.2); m.crowd(26.4, 'laugh', 1.4, .3)
d.add('fx', (m.fx + m.music).T, 0, 1.0); d.add('vox', m.vox.T, 0, 1.0)
d.duck('music', [1.25, 17.2], .4, .15, .4); d.duck('music', [6.4, 11.5, 15.55, 21.9], .65, 1.4, .3); d.room('fx', 'room', .14); d.room('vox', 'room', .06)
print(d.master(sys.argv[1], os.path.join(H, 'release', 'stems')))
