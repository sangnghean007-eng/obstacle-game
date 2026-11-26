"""Ep46 v3 TOP FROM THE BOTTOM sound — fully synthesized. Chiptune bed (new genre in the last 6) that drops out for the flips;
lever clunks, big rotation whooshes + gear ratchets, a fanfare for the fake '2nd', champagne pop + cork BONK + foam fizz,
a deflating 19→18 kazoo, a spinning slide-whistle loop, VAR beeps + buzzer, a heavy CLUNK back to 19th, a banner unroll, sad trombone, CTA."""
import os, sys, numpy as np
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(H, '..', 'sfx'))
from music import Song, SR
from mix import Desk
from fx2 import Mix2
D = 27.0; d = Desk(D); m = Mix2(D, ep=46)
song = Song('chiptune', key='F', minor=False, seed=4619).form([('intro', 2), ('verse', 3), ('drop', 3), ('break', 2), ('drop', 3), ('outro', 3)]); st = song.render()
L = min(len(st['drums']), int(D * SR)); env = np.ones(L)
for a, b, g in ((0, 3.0, 0.4), (14.8, 15.6, 0.15), (20.4, 22.6, 0.25)): env[int(a * SR):int(b * SR)] = g
env = np.convolve(env, np.ones(1500) / 1500, 'same'); d.add_stems({k: v[:L] * env for k, v in st.items()})
r = np.random.default_rng(4619)
def tt(dur): return np.arange(int(dur * SR)) / SR
def fanfare(t, g=.3, notes=(523, 659, 784, 1046)):
    for i, f in enumerate(notes): k = tt(.14 if i < 3 else .5); m.f((np.sign(np.sin(2 * np.pi * f * k)) * .5 + np.sin(2 * np.pi * f * 2 * k) * .3) * np.minimum(1, k * 40) * np.minimum(1, ((.14 if i < 3 else .5) - k) * 20) * g * .5, t + i * .12, .2)
def ratchet(t, dur, rate=18, g=.18):
    n = int(dur * rate)
    for i in range(n): k = tt(.03); m.f(np.convolve(r.standard_normal(len(k)), np.ones(4) / 4, 'same') * np.exp(-k * 120) * g * 3, t + i / rate, -.2)
def beep(t, f=1400, g=.25): k = tt(.12); m.f(np.sign(np.sin(2 * np.pi * f * k)) * np.minimum(1, (0.12 - k) * 60) * g * .4, t, .3)
def buzzer(t, g=.3): k = tt(.6); m.f(np.sign(np.sin(2 * np.pi * 110 * k)) * np.minimum(1, (0.6 - k) * 20) * g * .5, t, 0)
def fizz(t, dur, g=.12): k = tt(dur); m.f(np.diff(np.concatenate([[0], r.standard_normal(len(k))])) * (r.random(len(k)) > .7) * np.minimum(1, (dur - k) * 3) * g, t, -.3)
# A: 19th
m.sub_boom(0.5, .5); m.wahwah(1.0, .18); m.vo('generic_m', 'hmm', 1.7, .5, .2)
# B: Pochettino walks in, pulls the lever, the tower flips → "2nd!"
m.whoosh(3.0, .5, .3); m.vo('generic_m', 'hmm', 3.2, .5, -.3); m.thump(3.55, .5); m.clang(3.6, .3, -.3); ratchet(3.8, .8); m.whoosh(3.8, .9, .5); m.slide_whistle(3.85, True, .7, .25)
m.thump(4.6, .8); fanfare(4.65, .35); m.crowd(4.7, 'cheer', 1.2, .35); m.vo('generic_m', 'yay', 4.75, .6, .3); m.vo('generic_m', 'yay', 4.95, .6, -.3)
# C: champagne, "so proud", cork BONK, foam
m.vo('generic_m', 'yay', 6.2, .6, -.3); m.kazoo(6.3, ['C5', 'E5', 'G5', 'C6'], .14, .15); m.cork(7.0, .55); m.whoosh(7.02, .4, .3); m.smack(7.45, .55); m.spring(7.5, .3); m.vo('generic_m', 'yelp', 7.5, .6, -.3); fizz(7.5, 1.8)
m.vo('generic_m', 'cry', 8.3, .45, -.3, 'wail')
# D: UCL tower, flip → only 18th
m.timpani(9.4, 70, .3); m.thump(10.35, .5); m.clang(10.4, .3, -.3); ratchet(10.6, .6); m.whoosh(10.6, .6, .45); m.thump(11.2, .6); m.kazoo(11.3, ['G4', 'F4'], .3, .2); m.crowd(11.4, 'laugh', 1.0, .2)
# E: spin harder
m.vo('generic_m', 'grunt', 12.7, .5, -.3)
for i in range(8): m.clang(12.8 + i * .25, .12, -.3)
ratchet(12.8, 2.0, 26, .14); [m.whoosh(12.9 + i * .6, .5, .35) for i in range(3)]; m.slide_whistle(13.0, True, .8, .2); m.slide_whistle(13.9, False, .8, .2); m.thump(14.8, .7); m.spring(14.85, .3); m.vo('generic_m', 'gasp', 15.0, .5, 0)
# F: VAR → back to 19th
for i in range(4): beep(15.9 + i * .18)
buzzer(16.4, .35); m.record_scratch(16.45, .4); m.vo('generic_m', 'gasp', 16.6, .5, -.3); m.clang(16.85, .3, -.3); ratchet(17.0, .6); m.whoosh(17.0, .6, .45); m.boom(17.6, .7); m.clang(17.62, .4); m.xylo_fall(17.7, .18)
# G: banner unroll "TOP 2", zoom to the asterisk, Bruno deadpan
m.zip(18.9, .3); m.spring(19.4, .2); fanfare(19.5, .3, (659, 784, 1046, 1318)); m.record_scratch(20.4, .45); m.sub_boom(20.5, .45)
for i in range(3): k = tt(.18); m.f(np.sin(2 * np.pi * 4300 * k) * (np.sin(2 * np.pi * 40 * k) > 0) * np.exp(-k * 8) * .16, 21.3 + i * .42, .5)   # crickets
# H: Pochettino leans on the lever → upside down again
m.whoosh(22.6, .4, .3); m.thump(23.0, .4); m.clang(23.05, .3, -.3); ratchet(23.2, .7); m.whoosh(23.2, .7, .45); m.thump(23.9, .7); m.vo('generic_m', 'yay', 23.95, .6, -.3); m.fail_horn(24.2, .2)
m.cta(D - 2.4)
d.add('fx', (m.fx + m.music).T, 0, 1.0); d.add('vox', m.vox.T, 0, 1.25)
d.duck('music', [3.8, 4.6, 7.0, 7.45, 10.6, 14.8, 16.4, 17.6, 20.4, 23.2], .45, .15, .4); d.room('fx', 'stadium', .1)
print(d.master(sys.argv[1], os.path.join(H, 'release', 'stems')))
