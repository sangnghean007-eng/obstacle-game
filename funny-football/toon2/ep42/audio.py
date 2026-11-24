"""Ep42 v2 THE CHASE sound — fully synthesized. Surf-rock chase bed; the president's horn plays a little fanfare (start + end callback),
kiss 'mwah' pops, wheelie rev + soot cough, camera shutter for the selfie, reel/zip per lunge, hook 'plink' + tow scrape, brake skid, SPLAT, CTA."""
import os, sys, numpy as np
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(H, '..', 'sfx'))
from music import Song, SR
from mix import Desk
from fx2 import Mix2
D = 25.0; d = Desk(D); m = Mix2(D, ep=420)
song = Song('surf', key='A', minor=True, seed=420).form([('intro', 2), ('verse', 3), ('drop', 3), ('break', 2), ('drop', 3), ('outro', 2)]); st = song.render()
L = min(len(st['drums']), int(D * SR)); env = np.ones(L)
for a, b, g in ((16.0, 19.6, 0.35), (19.6, D, 0.7)): env[int(a * SR):int(b * SR)] = g
env = np.convolve(env, np.ones(1500) / 1500, 'same'); d.add_stems({k: v[:L] * env for k, v in st.items()})
r = np.random.default_rng(420)
def tt(dur): return np.arange(int(dur * SR)) / SR
def engine(t0, t1, g=.1, f0=62):
    k = tt(t1 - t0); f = f0 * (1 + .05 * np.sin(2 * np.pi * .7 * k)); x = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * (0.6 + 0.4 * np.sin(2 * np.pi * 9 * k)); x = np.convolve(x, np.ones(40) / 40, 'same'); m.f(x * g, t0, .3)
def rev(t, g=.55):
    k = tt(1.2); f = 60 + 260 * np.minimum(1, k * 3) * np.exp(-k * 1.2); x = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)); x = np.convolve(x, np.ones(30) / 30, 'same') * np.exp(-k * 1.5); m.f(x * g, t, .3)
def horn(t, g=.35):  # scooter horn fanfare (own tune)
    for i, (n, dur) in enumerate(((523, .14), (659, .14), (784, .14), (1047, .4))):
        k = tt(dur); x = (np.sign(np.sin(2 * np.pi * n * k)) * .6 + np.sin(2 * np.pi * n * 1.5 * k) * .4) * np.minimum(1, k * 60) * np.minimum(1, (dur - k) * 30); m.f(x * g * .5, t + sum(d for _, d in ((523, .14), (659, .14), (784, .14), (1047, .4))[:i]), .3)
def shutter(t, g=.5):
    k = tt(.12); m.f(r.standard_normal(len(k)) * np.exp(-k * 60) * g, t, 0); m.f(r.standard_normal(len(k)) * np.exp(-k * 50) * g * .7, t + .07, 0)
def skid(t, g=.4):
    k = tt(.9); x = np.sin(2 * np.pi * np.cumsum(2200 + 400 * np.sin(2 * np.pi * 13 * k)) / SR) * r.standard_normal(len(k)) * .5 * np.exp(-k * 2); m.f(x * g, t, 0)
def scrape(t0, t1, g=.25):
    k = tt(t1 - t0); x = r.standard_normal(len(k)); x = x - np.convolve(x, np.ones(8) / 8, 'same'); m.f(x * g * (0.7 + 0.3 * np.sin(2 * np.pi * 11 * k)), t0, -.2)
engine(0.0, 16.1, .09); engine(19.6, D, .06, 70)
horn(0.3); m.vo('generic_m', 'laugh', 0.9, .4, .3, 'snicker')
for a in (1.25, 1.55, 1.85): m.cork(a, .3); m.xylo(a + .02, ['E7'], .04, .12)
[m.thump(2.6 + i * .14, .1) for i in range(16)]; m.vo('mbappe', 'gasp', 2.9, .5, -.3); m.slide_whistle(3.7, True, .5, .16)
m.vo('mbappe', 'grunt', 5.3, .45, -.2); m.vo('mbappe', 'grunt', 5.8, .45, -.2); m.vo('generic_m', 'laugh', 6.45, .5, .3, 'belly')
rev(6.8, .6); m.whoosh(6.85, .6, .4); m.vo('mbappe', 'oof', 7.25, .55, -.2); [m.vo('mbappe', 'grunt', 7.6 + i * .25, .3, -.2) for i in range(2)]
m.xylo(8.7, ['C6', 'E6', 'G6'], .08, .14); shutter(9.8, .6); m.cork(10.2, .3); m.vo('mbappe', 'cry', 10.6, .5, -.3, 'sob'); m.vo('generic_m', 'laugh', 10.9, .45, .3, 'snicker')
for a in (12.6, 13.3): m.vo('mbappe', 'grunt', a, .45, -.2); m.zip(a + .1, .3); m.spring(a + .15, .22)
m.vo('mbappe', 'grunt', 14.0, .45, -.2); m.xylo(14.05, ['C7'], .05, .2); m.vo('mbappe', 'yelp', 14.15, .55, -.2); scrape(14.2, 16.0, .3); m.vo('generic_m', 'laugh', 14.6, .5, .3, 'belly')
skid(16.0, .5); m.record_scratch(16.05, .3); m.whoosh(16.1, .6, .45); m.slide_whistle(16.15, True, .5, .25); m.smack(16.7, 1.0); m.thump(16.72, .7); m.sub_boom(16.75, .5)
m.slide_whistle(17.3, False, 1.0, .22); m.vo('mbappe', 'cry', 17.6, .55, -.2); m.fail_horn(18.2, .18)
horn(19.9, .35); m.vo('generic_m', 'laugh', 20.4, .4, .4, 'snicker'); m.vo('mbappe', 'cry', 21.0, .65, -.2, 'wail')
m.cta(D - 2.4)
d.add('fx', (m.fx + m.music).T, 0, 1.0); d.add('vox', m.vox.T, 0, 1.25)
d.duck('music', [6.8, 9.8, 14.0, 16.0, 16.7], .45, .15, .4); d.room('fx', 'room', .1)
print(d.master(sys.argv[1], os.path.join(H, 'release', 'stems')))
