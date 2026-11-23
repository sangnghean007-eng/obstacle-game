"""Ep40 v2 "Deckchair Keeper" sound — fully synthesized (ElevenLabs credits out until ~3 Dec):
surf-rock bed (deckchair beach vibe) new seed/key, fresh fx2 seeds, own whistle/page/sip/blop, vox2 for Mbappé / Yamal / Raphinha."""
import os, sys, numpy as np
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(H, '..', 'sfx'))
from music import Song, SR
from mix import Desk
from fx2 import Mix2
D = 26.5; d = Desk(D); m = Mix2(D, ep=402)
song = Song('surf', key='E', minor=False, seed=402).form([('intro', 2), ('verse', 3), ('drop', 3), ('break', 2), ('drop', 3), ('outro', 2)]); st = song.render()
L = min(len(st['drums']), int(D * SR)); env = np.ones(L)
for a, b, g in ((4.2, 5.4, 0.2), (10.0, 11.0, 0.2), (16.8, 17.8, 0.25), (23.8, 24.9, 0.15)): env[int(a * SR):int(b * SR)] = g
env = np.convolve(env, np.ones(1500) / 1500, 'same'); d.add_stems({k: v[:L] * env for k, v in st.items()})
r = np.random.default_rng(402)
def tt(dur): return np.arange(int(dur * SR)) / SR
def whistle(t, dur=.35, g=.35):
    k = tt(dur); x = np.sin(2 * np.pi * 3100 * k) * (0.6 + 0.4 * np.sin(2 * np.pi * 31 * k)) * np.minimum(1, k * 40) * np.minimum(1, (dur - k) * 30); m.f(x * g, t, .4)
def page(t, g=.3):  # newspaper flip: filtered noise swish + crinkle
    k = tt(.35); n = r.standard_normal(len(k)); sw = n * np.sin(np.pi * k / .35) ** 2; cr = (r.random(len(k)) > .985) * r.uniform(-1, 1, len(k)) * 3
    m.f((np.diff(np.concatenate([[0], sw])) * 4 + cr) * .25 * g, t, -.5)
def sip(t, g=.3):  # slurp: rising noisy whistle
    k = tt(.5); f = 500 + 900 * k; x = np.sin(2 * np.pi * np.cumsum(f) / SR) * r.standard_normal(len(k)) * .5 * np.sin(np.pi * k / .5); m.f(x * g, t, -.5)
def blop(t, g=.6):  # ball into coffee: low bloop + splash
    k = tt(.4); x = np.sin(2 * np.pi * np.cumsum(180 + 400 * np.exp(-k * 12)) / SR) * np.exp(-k * 8); s = r.standard_normal(len(tt(.6))) * np.exp(-tt(.6) * 7) * .4
    m.f(x * g, t, -.4); m.f(s * g, t + .03, -.4)
# A — establishing: crowd, keeper rustles the paper
m.crowd(0.1, 'cheer', 2.0, .22); page(1.2, .25); m.vo('mbappe', 'hmm', 2.4, .45, .2)
# B — Mbappé run-up, skied kick, keeper just turns the page
whistle(3.6, .4); [m.thump(4.2 + i * .2, .12) for i in range(4)]; m.thump(5.0, .7); m.whoosh(5.05, 1.4, .45); m.slide_whistle(5.1, True, 1.2, .3)
m.crowd(5.5, 'ooh', 1.6, .4); m.vo('mbappe', 'no', 5.6, .6, .2); page(5.6, .4); m.wahwah(6.6, .2)
# C — Yamal "watch this", ankle shank, keeper sips
m.vo('yamal', 'laugh', 8.9, .45, .2, 'snicker'); m.whip(9.0, .25); whistle(9.8, .3, .25); [m.thump(9.9 + i * .18, .1) for i in range(4)]
m.squeak(10.6, .45); m.thump(10.62, .35); m.kazoo(10.9, ['G4', 'F4', 'E4', 'D4'], .25, .15); sip(11.4, .4); m.crowd(11.6, 'laugh', 1.5, .3); m.vo('yamal', 'uhoh', 11.8, .5, .2)
# D — Raphinha snatches the ball
m.whoosh(13.0, .4, .3); m.whip(13.6, .5); m.vo('generic_m', 'hmph', 13.65, .6, .3); m.vo('yamal', 'yelp', 13.9, .5, -.2); m.honk(14.6, .2)
# E — Raphinha scores, keeper dives late
whistle(16.4, .35, .3); [m.thump(16.6 + i * .18, .12) for i in range(4)]; m.thump(17.4, .8); m.whoosh(17.45, .4, .4); m.boom(17.85, .45)
m.vo('generic_m', 'oof', 17.7, .4, -.4); m.crowd(17.9, 'cheer', 2.0, .45); m.vo('generic_m', 'yay', 18.3, .5, .3); m.cowbell(18.8, .2); m.cowbell(19.1, .2)
# F — split: worse miss?
m.timpani(20.2, 95, .5); m.vo('mbappe', 'hmph', 20.6, .45, -.4); m.vo('yamal', 'hmph', 20.9, .45, .4); m.whip(21.5, .35); m.vo('mbappe', 'no', 21.6, .4, -.4); m.vo('yamal', 'no', 21.8, .4, .4)
# G — the skied ball finally lands in the coffee
m.crowd(22.5, 'ooh', 1.8, .35); m.xylo_rise(22.9, .22); m.timpani(23.4, 80, .35, .4); m.slide_whistle(23.7, False, .8, .35); blop(24.4, .8); m.crowd(24.7, 'laugh', 1.7, .4); m.vo('generic_m', 'gasp', 24.6, .5, -.4); page(25.4, .25)
d.add('fx', (m.fx + m.music).T, 0, 1.0); d.add('vox', m.vox.T, 0, 1.2)
d.duck('music', [5.0, 10.6, 17.4, 24.4], .45, .15, .4); d.room('fx', 'room', .12)
print(d.master(sys.argv[1], os.path.join(H, 'release', 'stems')))
