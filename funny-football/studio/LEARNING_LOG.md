# Learning log (daily team learning, 6:44 am Sydney)

Rotation: (a) animation & timing → (b) gag writing → (c) retention & hooks → (d) platform algorithms & policy → (e) trending formats → (f) sound design.


## 2026-11-23 — first real numbers for the block-world test (Ep35, Instagram, ~12 h)
- **Result: the test WON.** 9,029 views / 6,749 reach in ~12 h ≈ 6x the channel's usual curve; skip rate 20.6% (better than our average), like rate 1.4% (better). → Block-world format goes into the rotation (≈1 in 5), and "Road to 1000" becomes a recurring block series (a new block at every real Ronaldo goal).
- **Where we lose people:** 100% → ~65% in the first 8 s (the crane-wide shot at 3.4–7 s makes the characters tiny), then ~50% holds to 25 s (story works), then a drop in the last 2 s (end card). → Keep faces big for the first 8 s; cut the hook→payoff gap; end on action so the loop restarts before people swipe.
- **Weak spots: shares 0.0%, comments 0.0%, 1 follow.** 99.9% of viewers were non-followers — the Reels algorithm is giving us reach, we are not converting it. → (1) end each video with a two-sided question ON SCREEN (not only in the caption), (2) a "Part 2 at goal 987 👀" series promise so following has a reason, (3) a pinned comment that starts the argument ("League or Opta — whose goal is it?").
- **Audience:** men 89%, 13–34 ≈ 78%; top countries Iran, Turkey, Brazil, Uzbekistan, India — mostly non-native English speakers. → Keep on-screen text tiny (numbers, emojis, ≤4 words); Ronaldo-centred stories travel best in these markets; voice lines short and visual.

## 24 Nov 2026: skills (owner sent a "find-skills" reel; "chủ động thông minh và linh hoạt")
- Installing third-party skills with `npx skills` is blocked in this environment (runs outside code); do not work around it. Instead read a skill repo as docs and port what helps.
- Read remotion-dev/skills (timing, transitions, light-leaks, motion-blur, sfx). Ported into our engine: `toon2/motion.js` (spring ease, cut transitions whip/flash/leak/iris, blur trail) and `fx2.py` record_scratch / sub_boom / fail_horn (own synthesis; no sampled meme audio).
- Packaged our own pipeline as a project skill: `.claude/skills/soccer365-episode/SKILL.md` (auto-loads in future sessions).
- Applied to Ep40 v4: transitions on every cut, spring stand-up/climb, record scratch on the "look at the ball" beat.
