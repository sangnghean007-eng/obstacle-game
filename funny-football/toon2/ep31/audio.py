"""Ep31 THE GROUP CHAT sound (engine v2): lofi chat groove (new genre for the run) that drops out for each stadium cutaway;
phone notification pings double as goal horns (sound gag); stadium roars with stadium reverb; channel sting at the end."""
import os, sys, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sfx'))
from music import Song, Inst, tt, SR
from mix import Desk
from fx2 import Mix2
D = 32.2; d = Desk(D); I = Inst(np.random.default_rng(31)); m = Mix2(D, ep=31)
CHAT = [(0, 3.5), (7.5, 9.2), (15, 16.5), (24.5, 30)]
song = Song('lofi', key='A', minor=True, seed=31).form([('verse', 8), ('drop', 8)]); st = song.render()
L = len(st['drums']); env = np.zeros(L)
for a, b in CHAT: i0, i1 = int(a * SR), int(b * SR); env[i0:i1] = 1; env[i1:i1 + int(.3 * SR)] = np.linspace(1, 0, int(.3 * SR))[: max(0, min(int(.3 * SR), L - i1))] if i1 < L else 0
env = np.convolve(env, np.ones(2000) / 2000, 'same')
d.add_stems({k: v * env[: len(v)] for k, v in st.items()})
def ping(t, g=.6, hi=False):
    n = tt(.22); x = (np.sin(2 * np.pi * (1568 if hi else 1318) * n) * np.exp(-n * 18) + .6 * np.sin(2 * np.pi * (2093 if hi else 1760) * n) * np.exp(-n * 14) * (n > .07)); d.add('fx', x, t, g, .2)
MSGT = [0.15, 0.75, 1.45, 2.2, 7.6, 8.0, 8.45, 15.05, 15.45, 15.85, 24.6, 25.3, 26.3, 27.4, 28.6]
for t in MSGT: ping(t, .45)
for a, b in [(2.6, 3.5), (8.9, 9.25), (16.2, 16.55)]:
    for k in np.arange(a, b, .22): d.add('fx', I.rim() * .3, k, .5, .3)
def roar(t, dur=2.5, g=.5):
    n = tt(dur); x = np.convolve(np.random.default_rng(int(t * 10)).standard_normal(len(n)), np.ones(60) / 60, 'same') * 6 * np.minimum(1, n / .15) * np.exp(-np.maximum(0, n - .6) * 1.4); d.add('crowd', np.stack([x, np.roll(x, 300)]), t, g)
def horn(t, g=.6):  # the "goal horn" is a giant notification ping (sound gag)
    n = tt(1.4); x = sum(np.sin(2 * np.pi * f * n) for f in (196, 247, 294)) / 3 * np.minimum(1, n / .05) * np.exp(-np.maximum(0, n - .8) * 3); d.add('fx', np.tanh(x * 2) * .7, t, g); ping(t, .9, True)
# 37' Haaland
for i, k in enumerate(np.arange(3.6, 5.9, .32)): d.add('drums', I.kick(.3, .8, 40) * .5, k, .5)
d.add('fx', I.riser(1.6), 4.3, .4); d.add('drums', I.kick(.5, 1.4, 45), 5.9, 1); horn(5.95); roar(6.0, 2.0, .45); m.vo('generic_m', 'yelp', 6.05, .4)
# bus: engine + horn honk
n = tt(2.0); d.add('fx', np.tanh(np.sin(2 * np.pi * 55 * n) * 3) * .25 * (1 + .3 * np.sin(2 * np.pi * 9 * n)), 9.2, .5); m.honk(10.2, .5)
# 83' Ødegaard curler
d.add('fx', I.riser(1.0), 11.9, .35); d.add('drums', I.kick(.4, 1.2, 50), 12.6, .9); d.add('fx', np.sin(2 * np.pi * np.cumsum(np.linspace(300, 1400, int(.8 * SR))) / SR) * np.exp(-tt(.8) * 2) * .2, 12.6, .6); d.add('drums', I.kick(.5, 1.4, 45), 13.3, 1); horn(13.35); roar(13.4, 1.6, .45)
# VAR: suspense beeps + crunch of popcorn + "HANDBALL" impact
for k in np.arange(16.6, 17.6, .25): d.add('fx', np.sin(2 * np.pi * 880 * tt(.08)) * np.exp(-tt(.08) * 30), k, .35)
for k in (16.9, 17.3, 18.1): d.add('fx', np.convolve(np.random.default_rng(int(k * 10)).standard_normal(int(.06 * SR)), np.ones(5) / 5, 'same') * .5, k, .5)
d.add('fx', I.impact(1.6), 17.7, .6)
# penalty: heartbeat in the close-up, slow-mo whoosh (pitched down), the strike, net smoke hiss, huge roar
for k in (19.2, 19.85): d.add('drums', I.kick(.35, .5, 38), k, .8)
w = np.convolve(np.random.default_rng(5).standard_normal(int(1.8 * SR)), np.ones(200) / 200, 'same') * np.sin(np.linspace(0, np.pi, int(1.8 * SR))) * 4; d.add('fx', w, 21.0, .35)
d.add('drums', I.kick(.6, 1.6, 42), 22.8, 1.1); d.add('fx', I.impact(2.0), 22.8, .7); horn(22.85, .8); roar(22.9, 3.0, .6)
n = tt(1.2); d.add('fx', np.convolve(np.random.default_rng(9).standard_normal(len(n)), np.ones(3) / 3, 'same') * np.exp(-n * 2.5) * .3, 22.9, .4)
# slow-mo bed: low drone + heartbeat so the tension never drops to silence
n = tt(2.6); dr = np.sin(2 * np.pi * 55 * n) * .5 + np.sin(2 * np.pi * 82.5 * n) * .3; d.add('music', dr * np.minimum(1, n / .3) * np.minimum(1, (2.6 - n) / .2), 20.3, .5)
for k in (20.6, 21.3, 22.0): d.add('drums', I.kick(.35, .5, 38), k, .7)
# finale: sad trombone for the Danish phone + party for Norway, then loop click
m.wahwah(30.1, .25)
for k in np.arange(30.0, 32.0, .23): d.add('drums', I.clap() * .4, k, .3)
d.duck('music', [5.9, 13.3, 17.7, 22.8], .6, .2, .6); d.room('crowd', 'stadium', .25); d.room('fx', 'hall', .12)
# merge the legacy Mix2 cartoon voices / gags into the new desk
d.add('fx', (m.fx + m.music).T, 0, 1.0); d.add('vox', m.vox.T, 0, 1.0)
print(d.master(sys.argv[1], os.path.join(os.path.dirname(os.path.abspath(__file__)), 'release', 'stems')))
