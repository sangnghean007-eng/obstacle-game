"""Ep30 TWO ENDINGS sound (new style: emotional): soft felt piano + warm string pad. Messi scenes = warm major with distant crowd applause;
Ronaldo scenes = same theme in minor, empty-stadium room tone, one ball echo. Heartbeat under the close-ups, a lift when the two meet."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sfx'))
from fx2 import *
SEGS = [('e0', 2.5), ('e1', 3.0), ('e2', 3.0), ('e3', 3.0), ('e4', 2.5), ('e5', 3.0), ('e6', 3.5), ('e7', 2.5), ('e8', 3.0), ('e9', 2.5), ('e10', 3.5), ('e11', 2.5)]
ST = {}; _t = 0
for n, d in SEGS: ST[n] = _t; _t += d
END = _t; m = Mix2(END, ep=30); at = lambda n, z: ST[n] + z
def piano(t, note, d=1.8, g=.22):
    f = hz(note); n = int(d * SR); tt = np.arange(n) / SR
    x = (np.sin(2 * np.pi * f * tt) + .45 * np.sin(4 * np.pi * f * tt) * np.exp(-tt * 3) + .2 * np.sin(6 * np.pi * f * tt) * np.exp(-tt * 5)) * np.exp(-tt * 2.2) * np.minimum(1, tt * 200)
    m.m(x, t, g)
def pad(t, notes, d, g=.07):
    n = int(d * SR)
    for nn in notes:
        f = hz(nn); x = sum(osc(f * k, d, 'saw') for k in (1.0, 1.004, .996)) / 3; m.m(lp(x, 1400) * env(n, .6, .8), t, g)
def phrase(n, chords, mel, g=1.0):
    t0 = ST[n]; d = dict(SEGS)[n]; pad(t0, chords, d + .3, .06 * g)
    for i, nn in enumerate(mel): piano(t0 + .15 + i * d / len(mel), nn, 1.8, .2 * g)
MAJ = {'e0': (['C3', 'E3', 'G3'], ['E5', 'G5', 'C6']), 'e2': (['A2', 'C3', 'E3'], ['C6', 'B5', 'A5', 'E5']), 'e4': (['F2', 'A2', 'C3'], ['A5', 'C6', 'F6']), 'e6': (['G2', 'B2', 'D3'], ['D6', 'G5', 'B5', 'D6', 'G6']), 'e8': (['C3', 'E3', 'G3'], ['E6', 'D6', 'C6'])}
MIN = {'e1': (['A2', 'C3', 'E3'], ['E5', 'C5', 'A4']), 'e3': (['F2', 'A2', 'C3'], ['A4', 'C5', 'F5', 'E5']), 'e5': (['D2', 'F2', 'A2'], ['D5', 'F5', 'A4']), 'e7': (['E2', 'G#2', 'B2'], ['B4', 'E5', 'G#5']), 'e9': (['A2', 'C3', 'E3'], ['A4', 'E5', 'A5'])}
for n, (c, mel) in MAJ.items(): phrase(n, c, mel, 1.0)
for n, (c, mel) in MIN.items(): phrase(n, c, mel, .8)
phrase('e10', ['F2', 'A2', 'C3', 'E3'], ['C5', 'E5', 'G5', 'A5', 'C6', 'E6'], 1.0); phrase('e11', ['C3', 'E3', 'G3', 'B3'], ['G5', 'E5', 'C6'], 1.0)
def applause(t, d, g=.18): m.crowd(t, 'cheer', d, g)
for n in ('e0', 'e2', 'e4', 'e6', 'e8'): applause(ST[n] + .1, dict(SEGS)[n] - .2, .12 if n != 'e2' else .2)
for n in ('e1', 'e3', 'e5', 'e7', 'e9', 'e10'): nn = int(dict(SEGS)[n] * SR); m.f(lp(noise(dict(SEGS)[n]), 400) * env(nn, .2, .2), ST[n], .05)
# Ronaldo side: bench clock ticks, footsteps out, phone REC beep, notification pings, the light switch
for i in range(6): m.f(osc(1200, .03) * dec(.03, 60), at('e1', .3 + i * .45), .08)
for i in range(7): m.f(hp(noise(.05), 3000) * dec(.05, 50), at('e3', .2 + i * .37), .25)
m.timpani(at('e3', .9), 55, .45)
for i in range(8): m.footstep(at('e5', .2 + i * .32), .25, .3)
m.f(lp(noise(.5), 600) * dec(.5, 6), at('e5', 2.6), .25)
for i in range(6): m.f(osc(1567, .08) * dec(.08, 30), at('e7', .4 + i * .3), .08)
m.f(hp(noise(.04), 2500) * dec(.04, 60), at('e9', 1.8), .4)
# Messi: his last goal net + roar, the toss "whoosh", heartbeat in close-ups
m.thump(at('e4', 1.0), .5); m.crowd(at('e4', 1.05), 'cheer', 1.4, .35); m.whoosh(at('e6', .3), 1.2, .25, True)
for n in ('e2', 'e9'):
    for i in range(3): m.thump(at(n, .4 + i * .8), .22)
m.crowd(at('e10', 0.1), 'cheer', 3.0, .12)
print(round(END, 2)); m.write(sys.argv[1])
