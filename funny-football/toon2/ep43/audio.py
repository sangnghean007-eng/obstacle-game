"""Ep43 STAIRWAY TO 1000 sound. Orchestral climb bed (new seed/key), the series' own Ronaldo takes from Ep35 (siu_b "Ssssiiuuuu!", vo_mine "No no no! MINE!"),
ghost 'woo', post CLANG flashback, kick + net, VAR beeps + drawer-slide + fall, Félix goal, step chimes, CTA."""
import os, sys, numpy as np
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(H, '..', 'sfx'))
from music import Song, SR
from mix import Desk
from fx2 import Mix2
from scipy.io import wavfile
D = 25.6; d = Desk(D); m = Mix2(D, ep=43)
def snd(name):
    sr, x = wavfile.read(os.path.join(H, 'snd', name + '.wav')); x = x.astype(float) / 32768
    x = x.T if x.ndim == 2 else np.vstack([x, x]); f = np.ones(x.shape[1]); k = min(220, len(f) // 2); f[:k] = np.linspace(0, 1, k); f[-k:] = np.linspace(1, 0, k); return x * f
song = Song('orchestral', key='D', minor=False, seed=43).form([('intro', 2), ('verse', 3), ('drop', 3), ('break', 2), ('drop', 3), ('outro', 2)]); st = song.render()
L = min(len(st['drums']), int(D * SR)); env = np.ones(L)
for a, b, g in ((2.6, 5.9, 0.35), (6.4, 8.2, 0.3), (9.7, 11.0, 0.25), (14.5, 16.2, 0.3)): env[int(a * SR):int(b * SR)] = g
env = np.convolve(env, np.ones(1500) / 1500, 'same'); d.add_stems({k: v[:L] * env for k, v in st.items()})
r = np.random.default_rng(43)
def tt(dur): return np.arange(int(dur * SR)) / SR
def beep(t, f=1400, g=.25): k = tt(.12); m.f(np.sign(np.sin(2 * np.pi * f * k)) * np.minimum(1, (0.12 - k) * 60) * g * .4, t, .3)
def woo(t, g=.25): k = tt(1.2); m.f(np.sin(2 * np.pi * np.cumsum(500 + 120 * np.sin(2 * np.pi * 2 * k)) / SR) * np.sin(np.pi * k / 1.2) * g * .5, t, .4)
def drawer(t, g=.4): k = tt(.45); x = r.standard_normal(len(k)); x = np.convolve(x, np.ones(20) / 20, 'same') * (1 + .6 * np.sign(np.sin(2 * np.pi * 30 * k))) * np.exp(-k * 3); m.f(x * g * 3, t, .3)
m.crowd(0.1, 'cheer', 1.6, .2); m.xylo_rise(0.4, .16)
m.timpani(2.6, 70, .35, .6); woo(2.9, .3); m.vo('ronaldo', 'hmm', 3.6, .45, 0)
m.whoosh(4.2, .3, .3); m.clang(4.6, .6, -.3); m.vo('ronaldo', 'gasp', 4.8, .45, 0)
m.thump(5.9, .8); m.whoosh(5.95, .4, .4); m.thump(6.33, .4); m.crowd(6.35, 'cheer', 2.0, .45); m.boom(6.4, .4)
d.add('vox', snd('siu_b'), 6.5, 2.4)                       # signature take from Ep35 (owner: 'Siuuu cho rõ')
for i in range(3): m.xylo(7.2 + i * .09, ['C6', 'E6', 'G6'][i:i + 1], .05, .18)
m.whoosh(8.9, .5, .35); m.vo('ronaldo', 'yay', 9.0, .6, 0); [beep(9.7 + i * .25) for i in range(3)]; m.record_scratch(10.25, .4); drawer(10.3, .5)
m.slide_whistle(10.4, False, .5, .28); m.thump(10.8, .8); m.smack(10.82, .5); m.vo('ronaldo', 'ow', 10.85, .55, 0); m.fail_horn(11.3, .16); m.vo('ronaldo', 'hmph', 12.0, .5, 0)
[m.thump(13.0 + i * .14, .12) for i in range(6)]; m.thump(13.9, .7); m.whoosh(13.95, .35, .35); m.crowd(14.25, 'cheer', 1.6, .4); m.vo('generic_m', 'yay', 14.3, .5, .3)
d.add('vox', snd('vo_mine'), 14.6, 2.2)                    # "No no no! MINE!" — series callback (Ep35)
m.vo('generic_m', 'hmph', 15.5, .6, .3); m.whip(15.55, .4); m.vo('ronaldo', 'cry', 16.0, .5, 0, 'sob')
m.timpani(17.0, 62, .4, .8); m.xylo_rise(17.4, .18); m.sub_boom(19.3, .4); [m.xylo(19.4 + i * .12, ['C7'], .04, .1) for i in range(3)]
m.vo('ronaldo', 'laugh', 21.4, .5, 0, 'snicker'); m.whoosh(21.2, .3, .25)
m.cta(D - 2.4)
d.add('fx', (m.fx + m.music).T, 0, 1.0); d.add('vox', m.vox.T, 0, 1.25)
d.duck('music', [5.9, 6.4, 10.3, 10.8, 13.9, 14.6], .45, .15, .4); d.room('fx', 'stadium', .12)
print(d.master(sys.argv[1], os.path.join(H, 'release', 'stems')))
