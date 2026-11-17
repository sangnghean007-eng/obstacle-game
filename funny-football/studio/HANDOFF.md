# HANDOFF: read this first in any new or continued session

This channel makes funny satirical football cartoon Shorts (YouTube channel **Soccer 365 – @Soccer365days**, plus TikTok, Instagram, Facebook and X).

## Who you work for and how
- Talk to the user **in Vietnamese**. Every deliverable (video text, titles, posts) is in **English**.
- Standing order: **the team decides, then builds** (LEAN mode: 1 combined reviewer, at most 1 fix round; see the PLAYBOOK "Lean review mode" section).
  - For every video, run the pre-production room (parallel agents), merge the best ideas, build the video, run the post-production review room, fix, and ship.
  - Do not stop to ask the user to approve a script.
- Facts must be real and checked against 2 or more sources (`toon2/epN/facts.md`). Everything else is labelled "parody".
- Never copy other creators' art or use copyrighted footage. Use inspiration only.
- **Automation (Nov 16 2026):** the scheduled task "Soccer 365 – daily trend scan + learning" runs every day at 02:44 Vietnam time (06:44 Sydney) in a fresh session: social trend scan → BIG_CHANNELS.md, 3 verified topics → IDEAS.md, a next-episode draft → studio/drafts/, one lesson → LEARNING_LOG.md (+ "Auto-learned" bullets in ENGAGEMENT.md), then commits to this branch and sends a Vietnamese summary. Read the newest draft + log before starting a new episode.
- **Act without asking (user, Nov 16 2026: "next time no need to ask me, as long as nothing goes over the limit")**: decide and do; only stop for things outside the limits (false facts, hate/insults, copying other creators, personal data, publishing on the user's behalf). Show results, not questions.
- **Research → remember → apply** (user, Nov 14 2026). Social posts only after the user signs off the video, then paste them in chat (SOCIAL_COPY.md §7). Also **read the intent, not the words** (ENGAGEMENT.md §11, Nov 15): expand every short brief into the full story with back-story and every key moment as a scene; portraits only for the 2–4 standout players (Nov 16), the rest are named minis:
  - Whenever you research something (platform rules, techniques, formats), write the findings into the studio docs right away, so the next session does not research it again. Use `PLAYBOOK.md` for production rules, `SOCIAL_COPY.md` for post writing, and `LEARNING_LOG.md` for other notes.
  - Apply the findings from then on without being asked.
  - Read those docs before starting a task.
- Do not create PRs unless asked. Keep the user's personal details private.

## Where things are
- Branch: **`claude/new-session-e2g4yg`** (all work is here).
- `studio/PLAYBOOK.md`: all rules. The latest sections win: "v3 house style" and "Approved template (Ep4 v4)".
- `studio/likeness/README.md`: **the likeness gate.** Every real player must pass it (portrait + chibi) before appearing in a video. Tools: `fetch_ref.sh`, `grid.py`, `overlay.js`, `overlay_sheet.py`.
- `studio/ENGAGEMENT.md`: **the watch, share, argue engine.** Score every script on its 10-question scorecard; produce only at 14+/20.
- `studio/SOCIAL_COPY.md`: **how to write the posts** for YouTube, TikTok, Instagram, Facebook and X (rules, templates, checklist). Read it before writing any dossier.
- `studio/REVIEW_ROOM.md`, `scorecard.csv`, `performance.csv`, `IDEAS.md`.
- Character systems:
  - `toon2/chibi.js` + `toon2/chibi_cast.js`: the **current style**, big-head chibi.
  - `toon2/toon2.js` + `cast.js`: the older style.
- Sound: `toon2/sfx/synth.py` (music and foley kit). Voices are not used by default. If one is ever needed, use `make_pico.py`.
- **Approved template:** `toon2/ep4/scene.html` (Ep4 v4 "CAN'T MOVE HIM") + `toon2/ep4/audio.py` + `toon2/ep4/release/*` (posts: YOUTUBE, TIKTOK, INSTAGRAM, FACEBOOK, X).
- Render: `node toon2/epN/render.js <outdir> 30` → ffmpeg H.264 1080x1920 30 fps + `python3 audio.py out.wav`.

## Episodes so far

| Episode | Topic | Status |
|---|---|---|
| Ep1 | "The GOATs Clock Out" (`goats/`) | Released earlier |
| Ep2 | "The GOAT Dictionary" (`toon2/ep2/`) | 3.1K views in 4 days, 89.2% avg viewed (best so far, 22 s) |
| Ep3 | "RETIRED?!" v4 (`toon2/ep3/`): Messi Golden Boot | Older style |
| Ep4 | v4 "CAN'T MOVE HIM" (`toon2/ep4/`): Traoré vs Cucurella | **User approved: "keep it up like this"** |
| Ep5 | "SECRET PLAN" spy mini-movie (`toon2/ep5/`) | Done |
| Ep6 | "WORST DISGUISE IN MIAMI" (`toon2/ep6/`) | REJECTED, do not reuse |
| Ep7 | "GOAT COURT" courtroom (`toon2/ep7/`) | Done (v3) |
| Ep8 | "ROAD TO 1000" mountain mini-movie (`toon2/ep8/`): Ronaldo 985 goals, 15-min hat-trick | Done, awaiting user feedback |
| Ep12 | v4 "THE 20-YEAR CHASE 🏆" (Messi & Ronaldo chase a runaway trophy 2006→2026, one slapstick gag per World Cup, Pelé/R9 in the VIP box) (`toon2/ep12/`) | Done, awaiting user feedback; v1 list and v2 "exes" kept in `review/` |
| Ep13 | v2 "THE REVENGE 😤" (50.6 s, 12 scenes, 9 portraits incl. Yamal & Oyarzabal; movie-trailer parody of Spain 2-3 England, Nov 15 2026: Kane slipped at Wembley → Ballon d'Or → scores the pen in Madrid; ends Spain's 43-game run) (`toon2/ep13/`) | Done, awaiting user feedback; post within 24 h |
| Ep14 | "CR7 ACADEMY 🚲" (lesson parody: Messi learns the bicycle kick from Ronaldo, fails, gets slapped, hands over a literal goat; Part 2 teased) (`toon2/ep14/`) | Signed off; posts written (Nov 16) |
| Ep15 | v4 "DON'T MESS WITH CR7 🏆" (CR7 combo → Rodri + Yamal payback → CR7 calls Messi → Messi barrage → CR7 K.O., everyone laughs; 51.7 s, almost no dialogue) (`toon2/ep15/`) | Signed off; posts written (Nov 17) |
| Ep9 | "NO RONALDO, NO PROBLEM?" how it started/how it's going (`toon2/ep9/`): Portugal 4-2 Denmark without him → 1-4 on his farewell night | Done (user-requested topic), awaiting feedback |
| Ep10 | "MESSI vs RONALDO: FINAL FIGHT" fighting-game remake of Ep7 (`toon2/ep10/`), viral-first, portraits | Done, awaiting feedback |
| Ep11 | "TWO LIVES" Ronaldo vs Messi split-screen timeline 2002→2026 (`toon2/ep11/`) | Done, awaiting user feedback |

## Environment setup for a fresh container
```
apt-get install -y -q libttspico-utils espeak-ng mbrola mbrola-us2 mbrola-us3
```
Playwright, Chromium, ffmpeg, numpy and scipy are already available.

## Next
- Ep9 "NO RONALDO, NO PROBLEM?" is done (user asked for Portugal's latest match, Nov 14 2026). Post it within 24-48 h.
- Ep8 "ROAD TO 1000" is done (Ronaldo 985 career goals as of Nov 12, 2026; mountain-expedition format; lean review FIX FIRST → 5 fixes → shipped). Waiting for user feedback.
- Before posting Ep8, re-check the goal count; if he has scored again, say "as of Nov 12" in captions.
- Ep8 sets up a **Road to 1000 series**: every few goals, a new climb episode (the goat keeps stealing the flag). The next episode should use a format different from Ep9's how-it-started/how-it's-going (rule: never the same format twice in a row), e.g. nature documentary or GOAT Court Part 2.
- Ask the user for platform stats after each release, and log them in `performance.csv`.
- Tool note: a fresh container may need `pip install scipy` for the audio scripts.

## Daily learning (scheduled task, 6:44 am Australia/Sydney)
- **What it does:** a fresh session runs every morning. It hunts 3 verified topic ideas (appended to `IDEAS.md`), learns one skill on the rotation (appended to `LEARNING_LOG.md`) and pushes to this branch.
- **Limits:** it never posts, never makes videos and never edits `PLAYBOOK.md` directly. Proposed playbook changes go in the log entry for the producer to apply.
- **Length rule (Nov 17):** one 30–45 s cut for ALL platforms, no subtitle files. Ep15 release = `toon2/ep15/release/dont-mess-with-cr7-32s-9x16.mp4` (v5, edge-detail fix). The 51 s master stays as the source.

- **Ep16 "The Team Photo" v1 (Nov 17)** `toon2/ep16/`: FIFPRO World 11 2026 snub (Kane + Ronaldo out). 31.9 s single cut, new format (sneak-in caper), 4 gags + bicycle-kick bowling payoff. Awaiting sign-off; posts after sign-off.
- **Ep17 "The Grass Is Greener" v1 (Nov 17)** `toon2/ep17/`: Mbappé left PSG for the UCL; PSG won 2025 + 2026 without him. Split-screen Paris/Madrid format, 31 s. New MBAPPE trait portrait (likeness gate pending user check). Awaiting sign-off.
- **Format v2 (user, Nov 17):** see `studio/FORMATS_V2.md`: data/quiz/ranking/reaction formats (content + speed), cartoon stories max 1/week. Pilot: Quiz 01 "Guess the player" (`toon2/quiz01/`).
- **Direction (user, Nov 17, after quiz test):** quiz/scoreboard videos got few views. Main line = caricature, satirical, exaggerated cartoons of famous exciting matches/comebacks (Ep18 Istanbul 2005 first), diverse formats, keep developing. Quizzes only as an occasional extra.
