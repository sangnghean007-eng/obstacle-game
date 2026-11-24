"""Ep41 v3 PODIUM FIGHT sound — fully synthesized. Trap bed; shove/strain, cliff-hang squeak, comeback kick launch,
Simeone's three goal hops, two penalties at the cup (sky, bonk on Simeone), pole climb, fake handover, three slaps, table reveal, CTA."""
import os, sys, numpy as np
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(H, '..', 'sfx'))
from music import Song, SR
from mix import Desk
from fx2 import Mix2
D = 26.2; d = Desk(D); m = Mix2(D, ep=413)
song = Song('trap', key='G', minor=True, seed=413).form([('intro', 2), ('verse', 3), ('drop', 3), ('break', 2), ('drop', 3), ('outro', 2)]); st = song.render()
L = min(len(st['drums']), int(D * SR)); env = np.ones(L)
for a, b, g in ((4.0, 5.6, 0.35), (15.9, 16.4, 0.15), (17.6, 18.8, 0.3)): env[int(a * SR):int(b * SR)] = g
env = np.convolve(env, np.ones(1500) / 1500, 'same'); d.add_stems({k: v[:L] * env for k, v in st.items()})
# A podium
m.crowd(0.1, 'cheer', 2.0, .3); m.xylo_rise(0.3, .15); m.vo('yamal', 'laugh', 1.2, .4, 0, 'snicker')
# B shove (9 wins), Yamal hangs off the edge (0-2), comeback kick
m.whoosh(2.4, .4, .35); [m.thump(2.7 + i * .25, .35) for i in range(5)]; m.vo('mbappe', 'grunt', 2.8, .5, -.3); m.vo('mbappe', 'grunt', 3.4, .5, -.3)
m.slide_whistle(4.0, False, .5, .25); m.squeak(4.2, .35); m.vo('yamal', 'yelp', 4.15, .55, .2); m.vo('mbappe', 'laugh', 4.6, .5, -.2, 'belly'); m.crowd(4.4, 'ooh', 1.2, .3)
m.whip(5.6, .6); m.boom(5.65, .55); m.slide_whistle(5.7, True, .7, .3); m.vo('mbappe', 'ow', 5.8, .6, -.3); m.thump(6.4, .7); m.crowd(5.9, 'cheer', 1.6, .4)
# D Simeone: three goal hops (3-0), then the whisper
for a in (7.2, 7.6, 8.0): m.spring(a, .3); m.cork(a + .05, .35)
m.vo('generic_m', 'grunt', 8.2, .5, .4); m.whoosh(8.6, .4, .3); m.vo('generic_m', 'hmm', 9.0, .5, -.4); m.vo('mbappe', 'gasp', 9.4, .55, -.2)
# E penalties at the cup: sky, bonk on Simeone; Yamal climbs the pole
m.thump(10.8, .7); m.whoosh(10.85, 1.0, .45); m.slide_whistle(10.9, True, 1.0, .28); m.vo('mbappe', 'no', 11.3, .55, -.3)
m.squeak(12.0, .4); m.bonk(12.45, .9); m.vo('generic_m', 'ow', 12.5, .55, .4); m.crowd(12.6, 'laugh', 1.2, .3)
[m.squeak(12.95 + i * .2, .15) for i in range(4)]; m.xylo(13.8, ['C6', 'E6', 'G6', 'C7'], .06, .2); m.vo('yamal', 'yay', 13.85, .55, .1)
# F fake handover + slaps
m.xylo(14.7, ['G5', 'C6'], .1, .14); m.vo('yamal', 'hmm', 14.8, .45, .1); m.vo('mbappe', 'yay', 15.45, .6, -.3)
m.whip(16.0, .6); m.record_scratch(16.02, .45); m.vo('yamal', 'laugh', 16.15, .45, .1, 'snicker')
for i, a in enumerate((16.4, 16.75, 17.1)): m.smack(a, .9 - i * .05, (-.3, .3)[i % 2]); m.vo('mbappe', 'ow', a + .04, .5, -.3)
m.spring(17.35, .3); m.whoosh(17.6, .4, .3); m.squeak(17.7, .3)
# G table + laugh/cry; CTA
m.sub_boom(18.6, .6); m.timpani(18.65, 72, .4, .5); [m.thump(19.0 + i * .25, .3) for i in range(3)]
m.crowd(19.4, 'cheer', 2.5, .35); m.vo('yamal', 'laugh', 19.6, .6, .1, 'belly'); m.vo('mbappe', 'cry', 19.9, .65, -.4, 'wail'); m.fail_horn(20.6, .16)
m.vo('generic_m', 'laugh', 21.8, .4, .4, 'snicker'); m.vo('mbappe', 'cry', 22.6, .55, -.4, 'sob')
m.cta(D - 2.4)  # end-card support call (cta2.js)
d.add('fx', (m.fx + m.music).T, 0, 1.0); d.add('vox', m.vox.T, 0, 1.25)
d.duck('music', [5.6, 10.8, 12.45, 16.0, 16.4, 18.6], .45, .15, .4); d.room('fx', 'stadium', .15)
print(d.master(sys.argv[1], os.path.join(H, 'release', 'stems')))
