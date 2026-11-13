"""Episode 3 v4 sound: few clean voice lines (SVOX Pico), scene music, foley. All synthesized."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sfx'))
from synth import *

S = dict(hook=0, aug=2.0, relax=5.0, g1=7.6, g2=9.6, g3=11.4, award=14.4, gym=18.0, end=20.8, cta=23.6)
m = Mix(25.1)
def L4(name, t, g=1.0): m.put(m.vox, m.wav('lines4/' + name), t, g, 0, 0)

B = 60 / 96; BAR = 4 * B
CH = [['C4', 'E4', 'G4'], ['A3', 'C4', 'E4'], ['F3', 'A3', 'C4'], ['G3', 'B3', 'D4']]
ROOT = ['C2', 'A1', 'F1', 'G1']
MEL = [[('E5', 0), ('G5', 1), ('E5', 2.5), ('D5', 3), ('C5', 3.5)], [('C5', 0), ('E5', 1), ('A5', 2), ('G5', 3)],
       [('A5', 0), ('F5', 1.5), ('C5', 2), ('D5', 3)], [('B4', 0), ('D5', 1), ('G5', 2), ('F5', 3.5)]]
def reggae(t0, t1, g=1.0, melody=True):
    bar = 0; t = t0
    while t < t1 - .05:
        c = bar % 4
        for k in range(8):
            tk = t + k * B / 2
            if tk >= t1: break
            m.hat(tk, .09 * g, k % 2 == 1)
            if k % 2 == 1: m.organ_stab([hz(n) for n in CH[c]], tk, g=.1 * g)
        if t + 2 * B < t1: m.kick(t + 2 * B, .75 * g); m.rim(t + 2 * B, .28 * g)
        m.bass(hz(ROOT[c]), t, B * 1.5, .42 * g)
        if melody:
            for n, b in MEL[c]:
                if t + b * B < t1: m.pluck(hz(n), t + b * B, .4, .18 * g, .3)
        t += BAR; bar += 1
def workout(t0, t1, g=1.0):
    b = 60 / 140; t = t0; i = 0; riff = ['E2', 'E2', 'G2', 'E2', 'A2', 'E2', 'B2', 'D3']
    while t < t1 - .02:
        m.kick(t, .9 * g)
        if i % 2: m.clap(t, .4 * g)
        m.hat(t + b / 2, .12 * g, True)
        for q in range(2): f = hz(riff[(i * 2 + q) % 8]); m.saw_chord([f, f * 1.5, f * 2], t + q * b / 2, b / 2 * .9, .06 * g, 1400, 0, .003, .05, .05)
        t += b; i += 1

# HOOK: asleep, "top scorer?!" sting, rewind
reggae(0, 1.75, .5, melody=False); m.snore(0.0, 1.6, .5); m.seagull(0.3, .1)
m.brass_hit([hz('C3'), hz('E3'), hz('G3'), hz('C4')], 0.7, .7, .24); m.crash(0.7, .3)
m.tape_rewind(1.75, .3, .4)
# AUG: goodbye stadium, crying fans
t = S['aug']
m.crowd(t, 3.0, .16, swell=False); m.music_box(t + .1, ['A4', 'C5', 'E5', 'D5', 'C5', 'B4', 'A4', None, 'E4', 'A4'], .26, .2)
L4('m_bye', t + .6)
m.f(m.wav('ooh_crowd'), t + 1.4, .35, 0, .3)
for k in range(6): m.pop(t + 1.0 + k * .28, .1, 1800 + 300 * (k % 3))   # tear drips
# RELAX
t = S['relax']
reggae(t, S['g1'], .8)
for k in range(6): m.footstep(t + k * .2, .25, -.5 + k * .1)
m.boing(t + 1.2, .35, .35, 160, 90); m.thud(t + 1.22, .45); m.slurp(t + 1.6, .5, .3); m.ding(t + 1.6, 2600, .15)
# G1: kid passes, volley, keeper dives wrong
t = S['g1']
reggae(t, S['g3'], 1.0)
m.thwack(t + .3, .5, -.4); m.whoosh(t + .32, .5, .25, True, -.2)
m.thwack(t + .85, .8); m.whoosh(t + .87, .3, .3, True, .3)
m.whoosh(t + .9, .3, .2, False, .5); m.thud(t + 1.2, .4, .5)
m.net(t + 1.2); m.crash(t + 1.2, .35); m.crowd(t + 1.2, 1.0, .3)
# G2: seagull, header, face-plant
t = S['g2']
m.seagull(t, .2, .4); m.slurp(t + .1, .6, .25)
m.whoosh(t + .55, .3, .25, False); m.boing(t + .85, .45, .45, 220, 520); m.whoosh(t + .88, .3, .3)
m.net(t + 1.25); m.thud(t + 1.45, .55, .4); m.crowd(t + 1.25, 1.0, .3)
for k in range(12): m.tick(t + 1.25 + k * .03, k % 2 == 0, .15)
# G3: slow-mo bubble goal, keeper surrenders
t = S['g3']
m.slowdown(t, .9, .45); m.drone(hz('C2'), t + .1, 1.5, .15); m.heartbeat(t + .25, .55); m.heartbeat(t + .95, .55); m.snore(t + .1, 1.3, .3)
m.whoosh(t + .1, .9, .18, False); m.boing(t + 1.0, .5, .4, 140, 70); m.pop(t + 1.3, .5, 600); m.whoosh(t + 1.15, .4, .4, True)
tg = t + 1.55
m.net(tg); m.kick(tg, 1.0); m.crash(tg, .45); m.brass_hit([hz('C3'), hz('G3'), hz('C4'), hz('E4'), hz('G4')], tg, 1.0, .28); m.cheer_burst(tg + .02, .5)
for k, p in enumerate((-.5, .5)): m.firework(tg + .15 + k * .25, .3, p)
for k in range(13): m.tick(tg + k * .04, k % 2 == 0, .14)
m.f(m.wav('chuckle'), tg + .6, .0)
reggae(tg + .4, S['award'], .9)
# AWARD: presenter
t = S['award']
for k in range(6): m.footstep(t + k * .12, .25, .5)
m.choir([hz('C4'), hz('E4'), hz('G4'), hz('C5')], t + .6, 1.6, .17); m.sparkle(t + .7, .8, .1)
L4('p_boot', t + .65)
m.whoosh(t + 2.2, .4, .25, False); m.thud(t + 2.6, .3); m.snore(t + 2.7, .9, .3)
for k in range(10): m.clap(t + 2.6 + k * .09, .12)
reggae(t + 2.5, S['gym'], .7)
# GYM: Ronaldo sees the news
t = S['gym']
workout(t, t + 1.0, .9)
m.ding(t + .55, 1760, .3); m.ding(t + .65, 2349, .25)
m.scratch(t + 1.0, .55); L4('r_what', t + 1.05)
m.whoosh(t + 1.5, .25, .25, False); m.thud(t + 1.75, .8); m.thud(t + 1.8, .6, .3); m.crash(t + 1.75, .2)
for k in range(6): m.footstep(t + 1.9 + k * .09, .3, .2 + k * .12)
m.whoosh(t + 1.95, .6, .4, True, .6)
# END
t = S['end']
workout(t, S['cta'], .6); m.f(m.wav('siu'), t + .05, .35, .3, .2)
m.whoosh(t + .5, .3, .3)
m.badumtss(t + 2.4, .5); m.seagull(t + 1.8, .1)
# CTA
t = S['cta']
m.ding(t + .05, 1568, .3); m.ding(t + .55, 2093, .3); m.pop(t + .5, .3)
L4('n_follow', t + .2)
m.write(sys.argv[1])
