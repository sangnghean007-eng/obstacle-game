"""Ep13 v2 THE REVENGE sound: movie-trailer booms + slapstick + match sounds. No TTS.
hook 0 · euro 3.0 · wembley 7.4 · champs 12.4 · tunnel 16.4 · ballon 19.4 · arrive 24.4 · pen 27.6 · goals 33.0 · drama 37.4 · payoff 43.6 · question 47.6 · end 50.6"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sfx'))
from synth import *
END = 50.6; m = Mix(END)
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
def ghost(t, g=.3): tt = T(1.0); m.f(osc(glide(700, 350, 1.0, .7), 1.0) * (1 + .3 * np.sin(2 * np.pi * 6 * tt)) * env(len(tt), .1, .4), t, g, .3, .7)
def groan(t, g=.3): m.f(m.wav('grumble_sad'), t, g, -.2, .3)
def net(t, g=.8): m.net(t, g, .4); k808(t, 1.0); m.crash(t, .45)
# HOOK
braam(0, .55); m.whoosh(.1, .5, .3, True); braam(1.4, .4, 'A1'); riser(1.6, 1.2, .15); m.tape_rewind(2.4, .7, .35)
# EURO 2024 FINAL (sepia): cross, slide, goal, ghost, groan
t = 3.0; m.f(lp(noise(4.4), 600) * .25, t, .35, 0, .3); m.whoosh(t + .3, .4, .25, True, -.3); m.f(bp(noise(.4), 300, 2000) * dec(.4, 6), t + 1.2, .3)
net(t + 1.45, .6); m.f(m.wav('cheer_crowd'), t + 1.5, .3, .3, .3); ghost(t + 1.6); groan(t + 2.0, .35)
# WEMBLEY: slip, crossbar, Oyarzabal again
t = 7.4; m.f(lp(noise(5.0), 600) * .25, t, .35, 0, .3)
for k in range(4): m.footstep(t + k * .14, .3, -.2)
slide(t + .55, 1500, 400, .4, .3); m.f(m.wav('gasp'), t + .6, .35, 0, .2)
x = sum(a * osc(f, .8) for f, a in [(220, 1), (540, .5), (1210, .3)]) * dec(.8, 5); m.f(x, t + 1.05, .55, .3, .2); m.boing(t + 1.1, .3, .5, 400, 150); m.thud(t + 1.6, .6); m.tweet(t + 1.7, 4, .14)
for k in range(5): m.footstep(t + 2.2 + k * .12, .25, .4)
m.f(m.wav('cheer_crowd'), t + 2.8, .3, .3, .3); ghost(t + 2.9); m.f(m.wav('laugh_crowd'), t + 3.4, .3, 0, .3)
# CHAMPS: fanfare, then lounge guitar + counter dings
t = 12.4; m.brass_hit([hz('D3'), hz('A3'), hz('D4'), hz('F#4')], t, 1.0, .35); m.crash(t, .4); m.cheer_burst(t, .4); [m.firework(t + .2 + i * .4, .25, -.4 + i * .2) for i in range(4)]
guitar(t + 1.6, ['E4', 'F4', 'G#4', 'A4', 'B4', 'A4', 'G#4', 'F4', 'E4', 'F4', 'E4', 'D4', 'E4'], .18, .15)
for k, tt_ in enumerate([2.0, 2.4]): m.ding(t + tt_, 1568 + k * 200, .25)
m.slurp(t + 2.8, .6, .2)
# TUNNEL: drone, teeth chatter, heartbeat
t = 16.4; m.drone(hz('C2'), t, 3.0, .1); chatter(t + .2, 2.6, .2); m.heartbeat(t + .5, .35); m.heartbeat(t + 1.3, .35); m.heartbeat(t + 2.1, .35)
# BALLON D'OR: elegance, drumroll, reveal, Yamal's record scratch
t = 19.4; m.choir([hz('D4'), hz('F#4'), hz('A4')], t, 2.0, .08); m.sparkle(t + .2, 1.0, .1)
for k in range(28): m.snare(t + .6 + k * .05, .08 + .2 * k / 28)
m.f(m.wav('chuckle'), t + 1.0, .2, -.4, .2); m.scratch(t + 2.1, .4); braam(t + 2.15, .35, 'D2'); m.f(m.wav('cheer_crowd'), t + 2.2, .4, 0, .3)
m.harp_gliss(t + 2.4, ['D5', 'E5', 'F#5', 'A5', 'B5', 'D6'], .05, .12); m.f(m.wav('gasp'), t + 2.3, .3, -.4, .2)
# ARRIVE: footsteps, door, choir, then "uh oh"
t = 24.4
for k in range(2): k808(t + k * .3, .9); m.thud(t + k * .3, .5)
braam(t + .6, .6, 'D2'); m.f(lp(noise(.4), 1200) * dec(.4, 8), t + .6, .6); m.choir([hz('D4'), hz('F#4'), hz('A4'), hz('D5')], t + .7, 1.5, .14); m.f(m.wav('cheer_crowd'), t + 1.2, .3, 0, .3)
m.scratch(t + 2.2, .3); slide(t + 2.5, 900, 300, .5, .25); m.f(m.wav('gasp'), t + 2.5, .3, .3, .2)
# PEN: tackle, whistle, heartbeat, wobble, KICK, net, roar
t = 27.6; m.thud(t + .55, .6); m.f(bp(noise(.3), 200, 1500) * dec(.3, 8), t + .5, .4); whistle(t + .8, .4); m.f(m.wav('ooh_crowd'), t + .9, .3, 0, .3)
for k in range(5): m.heartbeat(t + 1.3 + k * .34, .45)
m.drone(hz('D2'), t + 1.3, 2.0, .1); slide(t + 2.55, 700, 900, .2, .2); slide(t + 2.8, 900, 650, .2, .2)
m.f(osc(1100, .12) * dec(.12, 20), t + 3.1, .25); m.thwack(t + 3.3, 1.0); m.whoosh(t + 3.3, .3, .4, True, .4)
net(t + 3.55); m.cheer_burst(t + 3.55, .5); m.brass_hit([hz('D3'), hz('A3'), hz('D4'), hz('F#4')], t + 3.6, 1.0, .35); drums(t + 3.8, t + 5.4, .7, 128)
# GOALS: Rice corner → Konsa header; White
t = 33.0; m.thwack(t + .4, .6); m.whoosh(t + .45, .4, .25, True); m.thud(t + .95, .5); net(t + 1.15); m.cheer_burst(t + 1.15, .45)
for k in range(5): m.footstep(t + 2.0 + k * .13, .25, .3)
m.thwack(t + 2.75, .8); net(t + 2.95); m.cheer_burst(t + 2.95, .45); m.boing(t + 3.25, .3, .4, 600, 200); drums(t + 1.2, t + 4.4, .5, 128)
# DRAMA: red card, Oyarzabal pen (ghost), Nico, heartbeat, final whistle
t = 37.4; m.f(bp(noise(.3), 200, 1500) * dec(.3, 8), t + .4, .4); m.thud(t + .5, .5); whistle(t + .6, .5, .35); m.brass_hit([hz('D3'), hz('G#3'), hz('D4')], t + .7, .7, .3)
m.thwack(t + 1.7, .7); k808(t + 1.95, .8); m.f(m.wav('cheer_crowd'), t + 1.95, .3, -.3, .3); ghost(t + 2.0, .3)
m.thwack(t + 2.9, .5); m.thwack(t + 3.25, .7); k808(t + 3.4, .8); m.f(m.wav('cheer_crowd'), t + 3.4, .3, -.3, .3); m.f(m.wav('ooh_crowd'), t + 3.6, .25, .3, .3)
for k in range(10): m.heartbeat(t + 2.0 + k * .33, .45 + k * .02)
for k in range(10): m.tick(t + 4.0 + k * .14, k % 2 == 0, .3)
m.drone(hz('C#2'), t + 2.0, 3.4, .12); riser(t + 4.2, 1.2, .2)
for k, d in enumerate([.25, .25, .7]): whistle(t + 5.4 + k * .32, d, .4)
# PAYOFF: shatter, anthem, fireworks, roar
t = 43.6; m.f(hp(noise(.4), 2500) * dec(.4, 8), t + .2, .5); m.thud(t + .9, .6); m.boing(t + .95, .3, .5, 300, 120)
for i, ch in enumerate([['D3', 'F#3', 'A3', 'D4'], ['G3', 'B3', 'D4', 'G4'], ['A3', 'C#4', 'E4', 'A4'], ['D4', 'F#4', 'A4', 'D5']]): m.brass_hit([hz(n) for n in ch], t + .3 + i * .8, .8, .3)
drums(t + .3, t + 4.0, .8, 120); m.cheer_burst(t + .3, .5); [m.firework(t + .4 + i * .55, .3, -.5 + i * .2) for i in range(6)]; m.scratch(t + 2.6, .25)
# QUESTION
t = 47.6; m.ding(t, 1318, .3); m.pop(t + .3, .3); m.pop(t + .45, .3, 1100); m.f(m.wav('ooh_crowd'), t + .3, .3, 0, .3); m.music_box(t + .9, ['D5', 'F#5', 'A5', 'D6'], .2, .12)
m.write(sys.argv[1])
