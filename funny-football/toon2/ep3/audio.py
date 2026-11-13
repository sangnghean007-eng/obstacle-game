"""Episode 3 v3 sound design: scene-specific music + foley + clear voice lines (all synthesized)."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sfx'))
from synth import *

S = dict(cold=0, quit=2.6, mA=4.4, mB=5.9, mC=7.5, boot=10.4, rA=13.8, rB=15.4, rC=16.8, end=20.1, cta=23.7)
m = Mix(25.2)

# ---------- music: Messi's lazy beach reggae (96 BPM, C - Am - F - G) ----------
B = 60 / 96; BAR = 4 * B
CH = [['C4', 'E4', 'G4'], ['A3', 'C4', 'E4'], ['F3', 'A3', 'C4'], ['G3', 'B3', 'D4']]
ROOT = ['C2', 'A1', 'F1', 'G1']
MEL = [[('E5', 0), ('G5', 1), ('E5', 2.5), ('D5', 3), ('C5', 3.5)], [('C5', 0), ('E5', 1), ('A5', 2), ('G5', 3)],
       [('A5', 0), ('F5', 1.5), ('C5', 2), ('D5', 3)], [('B4', 0), ('D5', 1), ('G5', 2), ('F5', 3.5)]]
def reggae(t0, t1, g=1.0, melody=True, drums=True):
    bar = 0; t = t0
    while t < t1 - .05:
        c = bar % 4
        for k in range(8):
            tk = t + k * B / 2
            if tk >= t1: break
            if drums: m.hat(tk, .1 * g, k % 2 == 1)
            if k % 2 == 1: m.organ_stab([hz(n) for n in CH[c]], tk, g=.11 * g)
        if drums and t + 2 * B < t1: m.kick(t + 2 * B, .8 * g); m.rim(t + 2 * B, .3 * g)
        m.bass(hz(ROOT[c]), t, B * 1.5, .45 * g)
        if t + 2.5 * B < t1: m.bass(hz(ROOT[c]) * 1.5, t + 2.5 * B, B, .35 * g)
        if melody:
            for n, b in MEL[c]:
                if t + b * B < t1: m.pluck(hz(n), t + b * B, .4, .2 * g, .3)
        t += BAR; bar += 1

# ---------- music: Ronaldo's workout beat (140 BPM, E minor power) ----------
def workout(t0, t1, g=1.0):
    b = 60 / 140; t = t0; i = 0
    riff = ['E2', 'E2', 'G2', 'E2', 'A2', 'E2', 'B2', 'D3']
    while t < t1 - .02:
        m.kick(t, .95 * g)
        if i % 2 == 1: m.clap(t, .45 * g)
        m.hat(t + b / 2, .14 * g, True)
        for q in range(2):
            n = riff[(i * 2 + q) % 8]; f = hz(n)
            m.saw_chord([f, f * 1.5, f * 2], t + q * b / 2, b / 2 * .9, .07 * g, 1400, 0, .003, .05, .05)
        t += b; i += 1

# ======================= TIMELINE =======================
# cold open: sleeping on the beach, then a goal without waking up
reggae(0.0, 2.6, .55, melody=False)
m.snore(0.0, 1.1, .45); m.seagull(0.5)
m.say('n_retired', 0.12)
m.whoosh(0.8, .35, .4, True, .4); m.thwack(1.12); m.whoosh(1.14, .34, .35, True, .3)
m.net(1.48); m.thud(1.48, .5, .4); m.crash(1.48, .45); m.cheer_burst(1.5, .45); m.say('n_goooal', 1.5, .9)
m.brass_hit([hz('C3'), hz('E3'), hz('G3'), hz('C4')], 1.75, .7, .22)
m.snore(1.95, 1.3, .45); m.pop(2.27, .45)

# flashback: Aug 31, 2026
m.tape_rewind(2.6, .35, .35); m.crowd(2.6, 1.8, .14, swell=False)
m.music_box(2.75, ['A4', 'C5', 'E5', 'D5', 'C5', 'B4', 'A4'], .22, .2)
m.say('m_bye', 2.8, .95)
m.ding(3.72, 2400, .18); m.sparkle(3.72, .3, .1)

# montage: goal 1, goal 10, goal 26
reggae(S['mA'], S['mC'], 1.0)
m.seagull(S['mA'] + .1, .12, -.5)
m.whoosh(S['mA'], .4, .35, True, -.4); m.thwack(S['mA'] + .42); m.whoosh(S['mA'] + .43, .28, .3)
m.net(S['mA'] + .72); m.crowd(S['mA'] + .72, 1.0, .25); m.say('n_goal1', S['mA'] + .78)
m.slurp(S['mB'], .85, .4); m.whoosh(S['mB'] + .1, .45, .3, True, .5)
m.boing(S['mB'] + .55, .45, .45, 220, 520); m.whoosh(S['mB'] + .6, .3, .25)
m.net(S['mB'] + .92); m.crash(S['mB'] + .92, .3); m.crowd(S['mB'] + .92, 1.0, .3); m.say('n_goal2', S['mB'] + .95)
for k in range(9): m.tick(S['mB'] + .95 + k * .04, k % 2 == 0, .2)
# slow motion
t = S['mC']
m.slowdown(t, .9, .5); m.drone(hz('C2'), t + .1, 1.5, .16); m.heartbeat(t + .25, .6); m.heartbeat(t + .95, .6)
m.snore(t + .1, 1.4, .35)
m.whoosh(t + .1, .9, .2, False)  # ball falling
m.boing(t + 1.0, .5, .4, 140, 70); m.pop(t + 1.3, .55, 600)
m.whoosh(t + 1.15, .4, .4, True)
tg = t + 1.55
m.net(tg); m.crash(tg, .5); m.kick(tg, 1.0)
m.brass_hit([hz('C3'), hz('G3'), hz('C4'), hz('E4'), hz('G4')], tg, 1.0, .28); m.cheer_burst(tg + .02, .55)
for k, p in enumerate((-.5, .5, 0)): m.firework(tg + .15 + k * .2, .3, p)
for k in range(16): m.tick(tg + k * .035, k % 2 == 0, .15)
m.say('n_asleep', tg + .1)
reggae(tg + .5, S['boot'], .9)

# golden boot from the sky, BONK, new pillow
t = S['boot']
m.choir([hz('C4'), hz('E4'), hz('G4'), hz('C5')], t, 1.0, .2); m.harp_gliss(t + .05, ['C4', 'E4', 'G4', 'C5', 'E5', 'G5', 'C6', 'E6'], .07); m.sparkle(t + .1, .8, .12)
m.whoosh(t + .82, .14, .3, False)
m.bonk(t + .95, .9); m.thud(t + .95, .6); m.crash(t + .95, .3); m.boing(t + 1.0, .25, .6, 300, 600); m.tweet(t + 1.1, 4, .14)
m.say('n_boot', t + 1.15)
m.whoosh(t + 1.75, .3, .25, False); m.thud(t + 2.05, .35); m.snore(t + 2.2, 1.2, .35)
reggae(t + 1.9, S['rA'], .6)

# Ronaldo: binoculars, 26?!, steam
t = S['rA']
m.scratch(t, .6)
for k, n in enumerate([['C2', 'G2'], ['C#2', 'G#2'], ['C2', 'F#2', 'C3']]): m.brass_hit([hz(x) for x in n], t + .05 + k * .2, .5 if k < 2 else .9, .28)
m.drone(hz('C2'), t + .6, 1.0, .12)
m.say('r_26', t + .62); m.kettle(t + .8, .8, .16); m.f(m.wav('grumble_angry'), t + 1.25, .35, .2)

# tries to relax: runs in, towel, tick tock
t = S['rB']
for k in range(5): m.footstep(t + k * .1, .3, .3 - k * .1)
m.whoosh(t + .45, .2, .25, False); m.thud(t + .55, .45); m.snore(t, .9, .2)
for k in range(4): m.tick(t + .6 + k * .2, k % 2 == 0, .35)

# can't relax: workout, SIUUU onto Messi
t = S['rC']
m.boing(t, .5, .35, 200, 700); m.pop(t + .02, .3, 400)
workout(t + .15, t + 2.2, 1.0)
for k in range(9): m.whoosh(t + .15 + k / 4.2, .16, .08, k % 2 == 0, .3 if k % 2 else -.3)
m.say('r_relax', t + .25)
m.crash(t + 2.15, .35); m.f(m.wav('siu'), t + 2.15, .9, 0, .25)
m.whoosh(t + 2.45, .4, .4, True, -.3)
m.bonk(t + 2.85, .8, -.3); m.tweet(t + 2.95, 3, .12, -.3); m.snore(t + 3.0, .9, .3)

# ending: both "retired"
t = S['end']
reggae(t, S['cta'], .75)
for k in range(int(3.6 / (60 / 140))): m.kick(t + k * 60 / 140, .35)
m.whoosh(t + .35, .3, .3)
m.say('n_only', t + .45)
m.badumtss(t + 2.65, .55)
m.seagull(t + 3.0, .1)

# CTA
t = S['cta']
m.ding(t + .05, 1568, .3); m.ding(t + .55, 2093, .3); m.pop(t + .5, .3)
m.say('n_follow', t + .2)
m.write(sys.argv[1])
