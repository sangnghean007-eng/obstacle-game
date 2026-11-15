"""Ep13 THE REVENGE sound: movie-trailer booms + slapstick + match sounds. No TTS.
hook 0 · flash 2.6 · lounge 7.6 · arrive 11.2 · pen 15.2 · rush 20.2 · drama 23.6 · payoff 28.2 · question 31.6 · end 34.4"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sfx'))
from synth import *
END = 34.4; m = Mix(END)
def braam(t, g=.5, root='D2'):
    d = 2.2; tt = T(d); f = hz(root); x = sum(lp(osc(f * k * (1 + .003 * i), d, 'saw'), 700) for i, k in enumerate([1, 1.5, 2, 1.002])) + 1.2 * osc(f / 2, d)
    m.m(x * env(len(tt), .03, .9), t, g, 0, .4); m.kick(t, .9); m.crash(t, .35)
def riser(t, d=1.2, g=.25): tt = T(d); m.f(bp(noise(d), 400, 6000) * np.linspace(0, 1, len(tt)) ** 2, t, g, 0, .3); m.f(osc(glide(200, 1200, d, 2), d) * np.linspace(0, 1, len(tt)) * .3, t, g * .6, 0, .3)
def whistle(t, d=.35, g=.3): tt = T(d); m.f(osc(2900 + 150 * np.sin(2 * np.pi * 40 * tt), d) * env(len(tt), .01, .05), t, g, .1, .1)
def slide(t, f0, f1, d=.5, g=.3): tt = T(d); m.f(osc(glide(f0, f1, d), d) * env(len(tt), .01, .05), t, g, 0, .15)
def k808(t, g=.9): d = .5; m.m(osc(glide(110, 42, d, .3), d) * dec(d, 5) + .2 * lp(noise(d), 1500) * dec(d, 60), t, g, 0, .02)
def drums(t0, t1, g=.6, bpm=96):
    b = 60 / bpm; t = t0; i = 0
    while t < t1 - .02: m.kick(t, .7 * g); m.snare(t + b, .35 * g) if i % 2 else None; m.hat(t + b / 2, .06 * g); t += b; i += 1
def chatter(t, d, g=.18): [m.tick(t + k * .05, k % 2 == 0, g) for k in range(int(d / .05))]
def guitar(t0, notes, step=.18, g=.16): [m.pluck(hz(n), t0 + i * step, .5, g, -.3 + .1 * (i % 6), .7, .3) for i, n in enumerate(notes)]
# HOOK: BRAAAM + title, then tape rewind
braam(0, .55); m.whoosh(.1, .5, .3, True); braam(1.2, .4, 'A1'); m.tape_rewind(1.75, .8, .35); riser(1.4, 1.1, .15)
# FLASHBACK: muffled crowd, run-up, SLIP, crossbar, Spain score twice, laugh
t = 2.6; m.f(lp(noise(5.0), 600) * .25, t, .35, 0, .3)
for k in range(6): m.footstep(t + .25 + k * .17, .3, -.2)
slide(t + 1.15, 1500, 400, .4, .3); m.f(m.wav('gasp'), t + 1.2, .35, 0, .2); m.thwack(t + 1.25, .5)
x = sum(a * osc(f, .8) for f, a in [(220, 1), (540, .5), (1210, .3)]) * dec(.8, 5); m.f(x, t + 1.7, .55, .3, .2); m.boing(t + 1.75, .3, .5, 400, 150)
m.thud(t + 2.25, .6); m.tweet(t + 2.35, 4, .14)
m.f(m.wav('cheer_crowd'), t + 2.9, .25, .3, .3); m.f(m.wav('cheer_crowd'), t + 3.4, .25, .3, .3); m.ding(t + 2.85, 880, .25); m.ding(t + 3.4, 880, .25)
m.f(m.wav('laugh_crowd'), t + 3.5, .35, 0, .3); trom = [('D3', .25), ('C#3', .25), ('C3', .25), ('B2', .7)]
for i, (n, d) in enumerate(trom): tt = T(d); m.m(lp(osc(hz(n) * (1 + .02 * np.sin(2 * np.pi * 6 * tt)), d, 'saw'), 900) * env(len(tt), .02, .08), t + 3.7 + i * .27, .25, .2, .3)
# LOUNGE: smooth Spanish guitar + counter dings; England teeth chatter
t = 7.6; guitar(t, ['E4', 'F4', 'G#4', 'A4', 'B4', 'A4', 'G#4', 'F4', 'E4', 'F4', 'E4', 'D4', 'E4', 'F4', 'G#4', 'B4', 'A4', 'G#4', 'F4', 'E4'], .18, .15)
for k, tt_ in enumerate([.4, .9, 1.4]): m.ding(t + tt_, 1568 + k * 200, .25)
m.slurp(t + 1.0, .6, .2); m.whoosh(t + 1.7, .4, .25, True, .4); chatter(t + 1.9, 1.6, .2); m.f(m.wav('grumble_sad'), t + 2.3, .2, .4, .2)
# ARRIVE: three footstep booms, door bursts, choir + riser; reaction gulp
t = 11.2
for k in range(3): k808(t + k * .3, .9); m.thud(t + k * .3, .5)
braam(t + .8, .6, 'D2'); m.f(lp(noise(.4), 1200) * dec(.4, 8), t + .8, .6); m.choir([hz('D4'), hz('F#4'), hz('A4'), hz('D5')], t + .9, 1.8, .14); m.sparkle(t + 1.3, 1.0, .15)
drums(t + 1.2, t + 2.7, .7, 120); m.f(m.wav('cheer_crowd'), t + 1.7, .3, 0, .3)
m.scratch(t + 2.7, .3); slide(t + 3.0, 900, 300, .5, .25); m.f(m.wav('gasp'), t + 3.0, .3, .3, .2)
# PEN: whistle, gasp, heartbeat, wobble squeak, KICK, fireball, net, roar
t = 15.2; m.f(m.wav('cheer_crowd'), t, .15, 0, .3); m.thud(t + .6, .4); whistle(t + .9, .4); m.f(m.wav('ooh_crowd'), t + 1.0, .3, 0, .3)
for k in range(5): m.heartbeat(t + 1.2 + k * .32, .45)
m.drone(hz('D2'), t + 1.2, 1.6, .1); slide(t + 2.05, 700, 900, .2, .2); slide(t + 2.3, 900, 650, .2, .2)
m.f(osc(1100, .12) * dec(.12, 20), t + 2.6, .25); m.thwack(t + 2.8, 1.0); m.whoosh(t + 2.8, .3, .4, True, .4); m.f(bp(noise(.3), 300, 3000) * dec(.3, 6), t + 2.85, .35, .4)
m.net(t + 3.05, .8, .5); k808(t + 3.05, 1.0); m.crash(t + 3.05, .5); m.cheer_burst(t + 3.05, .5); m.brass_hit([hz('D3'), hz('A3'), hz('D4'), hz('F#4')], t + 3.1, 1.0, .35)
drums(t + 3.3, t + 5.0, .7, 128)
# RUSH: two slams
t = 20.2
for g_ in (.6, 1.7): m.whoosh(t + g_ - .45, .4, .3, True); k808(t + g_, 1.0); m.crash(t + g_, .45); m.ding(t + g_ + .05, 1760, .3); m.cheer_burst(t + g_, .35)
drums(t, t + 3.4, .6, 128); m.f(hp(noise(.15), 3000) * dec(.15, 20), t + 2.4, .4); m.pop(t + 2.45, .3, 1400)
# DRAMA: whistle + red card sting, Spain goals, alarm heartbeat, clock ticks, final whistle
t = 23.6; whistle(t + .05, .5, .35); m.brass_hit([hz('D3'), hz('G#3'), hz('D4')], t + .3, .7, .3)
for g_ in (1.05, 2.05): k808(t + g_, .8); m.f(m.wav('cheer_crowd'), t + g_, .3, -.3, .3); m.f(m.wav('ooh_crowd'), t + g_ + .2, .25, .3, .3)
for k in range(9): m.heartbeat(t + 1.0 + k * .33, .45 + k * .02)
for k in range(10): m.tick(t + 2.6 + k * .14, k % 2 == 0, .3)
m.drone(hz('C#2'), t + 1.0, 3.0, .12); riser(t + 2.8, 1.2, .2)
for k, d in enumerate([.25, .25, .7]): whistle(t + 4.0 + k * .32, d, .4)
# PAYOFF: shatter, anthem brass, fireworks, roar
t = 28.2; m.f(hp(noise(.4), 2500) * dec(.4, 8), t + .2, .5); m.thud(t + .9, .6); m.boing(t + .95, .3, .5, 300, 120)
for i, ch in enumerate([['D3', 'F#3', 'A3', 'D4'], ['G3', 'B3', 'D4', 'G4'], ['A3', 'C#4', 'E4', 'A4'], ['D4', 'F#4', 'A4', 'D5']]): m.brass_hit([hz(n) for n in ch], t + .3 + i * .7, .7, .3)
drums(t + .3, t + 3.4, .8, 120); m.cheer_burst(t + .3, .5); [m.firework(t + .4 + i * .5, .3, -.5 + i * .2) for i in range(6)]
# QUESTION
t = 31.6; m.ding(t, 1318, .3); m.pop(t + .3, .3); m.pop(t + .45, .3, 1100); m.f(m.wav('ooh_crowd'), t + .3, .3, 0, .3); m.music_box(t + .9, ['D5', 'F#5', 'A5', 'D6'], .2, .12)
m.write(sys.argv[1])
